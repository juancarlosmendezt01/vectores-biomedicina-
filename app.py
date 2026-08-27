# ============================================================
# APP COMPLETA
# EJERCICIO PARA COMPRENDER VECTORES EN BIOMEDICINA
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import gspread
import plotly.express as px
import plotly.graph_objects as go

from google.oauth2.service_account import Credentials
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from sklearn.linear_model import LinearRegression


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Vectores en Biomedicina",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Ejercicio para comprender vectores")

st.write(
    """
    En este ejercicio construiremos colectivamente un pequeño
    conjunto de datos biomédicos.

    Cada estudiante aportará **10 pacientes ficticios** y veremos cómo:

    **Paciente → Vector → Normalización → Relaciones → Similitud → Patrones**
    """
)

st.info(
    "Cada paciente será representado mediante: "
    "[Edad, IMC, PAS, LDL, HbA1c]"
)


# ============================================================
# 2. CONEXIÓN CON GOOGLE SHEETS
# ============================================================

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    dict(st.secrets["gcp_service_account"]),
    scopes=scopes
)

client = gspread.authorize(credentials)

spreadsheet_id = st.secrets["google_sheet"]["spreadsheet_id"]

spreadsheet = client.open_by_key(spreadsheet_id)

worksheet = spreadsheet.sheet1


# ============================================================
# 3. IDENTIFICACIÓN DEL ESTUDIANTE
# ============================================================

st.divider()

st.header("👨‍⚕️ 1. Identifique su grupo")

estudiante = st.text_input(
    "Nombre, iniciales o código del estudiante/grupo",
    placeholder="Ejemplo: Grupo 3"
)

st.caption(
    "Use únicamente datos ficticios. No ingrese información "
    "identificable de pacientes reales."
)


# ============================================================
# 4. DATOS PREDETERMINADOS
# ============================================================

datos_iniciales = pd.DataFrame(
    {
        "Paciente": [
            "Paciente 1",
            "Paciente 2",
            "Paciente 3",
            "Paciente 4",
            "Paciente 5",
            "Paciente 6",
            "Paciente 7",
            "Paciente 8",
            "Paciente 9",
            "Paciente 10"
        ],

        "Edad": [
            68, 65, 25, 28, 72,
            70, 44, 46, 55, 58
        ],

        "IMC": [
            31.0, 30.0, 21.0, 22.0, 33.0,
            32.0, 27.0, 28.0, 24.0, 25.0
        ],

        "PAS": [
            148, 145, 108, 112, 155,
            150, 125, 128, 118, 120
        ],

        "LDL": [
            170, 165, 85, 92, 190,
            180, 120, 125, 105, 110
        ],

        "HbA1c": [
            7.2, 7.0, 5.0, 5.2, 8.1,
            7.8, 5.8, 6.0, 5.4, 5.5
        ]
    }
)


# ============================================================
# 5. TABLA EDITABLE
# ============================================================

st.divider()

st.header("📝 2. Ingrese sus 10 pacientes")

st.write(
    """
    Los datos ya están llenos para facilitar el ejercicio.

    Puede modificar los valores antes de guardarlos.
    """
)

datos_editados = st.data_editor(
    datos_iniciales,
    num_rows="fixed",
    hide_index=True,
    use_container_width=True,

    column_config={
        "Paciente": st.column_config.TextColumn("Paciente"),

        "Edad": st.column_config.NumberColumn(
            "Edad",
            min_value=18,
            max_value=100,
            step=1
        ),

        "IMC": st.column_config.NumberColumn(
            "IMC",
            min_value=10.0,
            max_value=60.0,
            step=0.1,
            format="%.1f"
        ),

        "PAS": st.column_config.NumberColumn(
            "PAS",
            min_value=70,
            max_value=250,
            step=1
        ),

        "LDL": st.column_config.NumberColumn(
            "LDL",
            min_value=20,
            max_value=400,
            step=1
        ),

        "HbA1c": st.column_config.NumberColumn(
            "HbA1c",
            min_value=3.0,
            max_value=20.0,
            step=0.1,
            format="%.1f"
        )
    }
)

st.info(
    "💡 Cada fila podrá convertirse en un vector: "
    "[Edad, IMC, PAS, LDL, HbA1c]"
)


# ============================================================
# 6. GUARDAR LOS 10 PACIENTES
# ============================================================

st.divider()

st.header("💾 3. Agregue sus pacientes al dataset colectivo")

if st.button(
    "GUARDAR MIS 10 PACIENTES",
    type="primary",
    use_container_width=True
):

    if estudiante.strip() == "":

        st.error(
            "⚠️ Escriba primero el nombre o código de su grupo."
        )

    else:

        filas_nuevas = []

        for _, fila in datos_editados.iterrows():

            filas_nuevas.append(
                [
                    estudiante,
                    fila["Paciente"],
                    int(fila["Edad"]),
                    float(fila["IMC"]),
                    int(fila["PAS"]),
                    int(fila["LDL"]),
                    float(fila["HbA1c"])
                ]
            )

        worksheet.append_rows(
            filas_nuevas,
            value_input_option="USER_ENTERED"
        )

        st.success(
            "✅ Sus 10 pacientes fueron agregados al dataset colectivo."
        )


# ============================================================
# 7. LEER DATASET COLECTIVO
# ============================================================

datos_colectivos = worksheet.get_all_records()

if len(datos_colectivos) > 0:

    df_colectivo = pd.DataFrame(datos_colectivos)

else:

    df_colectivo = pd.DataFrame()


# ============================================================
# 8. CONTADORES
# ============================================================

st.divider()

st.header("📊 Dataset colectivo")

if len(df_colectivo) > 0:

    numero_pacientes = len(df_colectivo)

    numero_participantes = (
        df_colectivo["Estudiante"]
        .astype(str)
        .nunique()
    )

else:

    numero_pacientes = 0
    numero_participantes = 0


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "👥 Pacientes registrados",
        numero_pacientes
    )

with col2:
    st.metric(
        "🎓 Estudiantes / grupos",
        numero_participantes
    )


meta = 100

progreso = min(
    numero_pacientes / meta,
    1.0
)

st.progress(progreso)

st.write(
    f"**{numero_pacientes} / {meta} pacientes recolectados**"
)


if numero_pacientes > 0:

    with st.expander("🔎 Ver pacientes recolectados"):

        st.dataframe(
            df_colectivo,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 9. PREPARACIÓN DE DATOS
# ============================================================

variables_vector = [
    "Edad",
    "IMC",
    "PAS",
    "LDL",
    "HbA1c"
]

if numero_pacientes > 0:

    df_analisis = df_colectivo.copy()

    for variable in variables_vector:

        df_analisis[variable] = pd.to_numeric(
            df_analisis[variable],
            errors="coerce"
        )

    df_analisis = df_analisis.dropna(
        subset=variables_vector
    )

    matriz_vectores = df_analisis[
        variables_vector
    ].to_numpy(dtype=float)


# ============================================================
# 10. GENERAR VECTORES
# ============================================================

st.divider()

st.header("🧮 4. Generar vectores")

if numero_pacientes == 0:

    st.warning("Todavía no hay pacientes registrados.")

else:

    st.write(
        """
        Cada paciente puede representarse mediante un vector numérico.
        """
    )

    st.info(
        "Vector = [Edad, IMC, PAS, LDL, HbA1c]"
    )

    if st.button(
        "GENERAR VECTORES",
        use_container_width=True
    ):

        st.success(
            f"✅ Se generaron {len(df_analisis)} vectores."
        )

        st.subheader("Ejemplos")

        numero_ejemplos = min(
            20,
            len(df_analisis)
        )

        for i in range(numero_ejemplos):

            fila = df_analisis.iloc[i]

            vector = [
                int(fila["Edad"]),
                round(float(fila["IMC"]), 1),
                int(fila["PAS"]),
                int(fila["LDL"]),
                round(float(fila["HbA1c"]), 1)
            ]

            st.code(
                f'{fila["Estudiante"]} - '
                f'{fila["Paciente"]} = {vector}'
            )

        st.info(
            """
            💡 Ahora cada paciente está representado mediante números.

            Esto permite comparar matemáticamente sus características.
            """
        )


# ============================================================
# 11. NORMALIZACIÓN
# ============================================================

st.divider()

st.header("⚖️ 5. Normalizar vectores")

if numero_pacientes > 1:

    st.write(
        """
        Las variables tienen escalas diferentes.

        Por ejemplo:

        - LDL puede tener valores cercanos a 170
        - HbA1c puede tener valores cercanos a 7

        Si usamos los valores originales, una variable podría tener
        más peso solamente porque sus números son mayores.

        Por eso realizamos una **estandarización**.
        """
    )

    if st.button(
        "NORMALIZAR VECTORES",
        use_container_width=True
    ):

        scaler = StandardScaler()

        matriz_normalizada = scaler.fit_transform(
            matriz_vectores
        )

        df_normalizado = pd.DataFrame(
            matriz_normalizada,
            columns=variables_vector
        )

        st.success(
            "✅ Los vectores fueron normalizados."
        )

        st.subheader("Vector original")

        ejemplo_original = [
            round(float(x), 2)
            for x in matriz_vectores[0]
        ]

        st.code(
            str(ejemplo_original)
        )

        st.subheader("Vector normalizado")

        ejemplo_normalizado = [
            round(float(x), 2)
            for x in matriz_normalizada[0]
        ]

        st.code(
            str(ejemplo_normalizado)
        )

        st.write(
            """
            Ahora todas las variables están en una escala comparable.

            **Un valor grande ya no tendrá más peso solamente por
            tener una magnitud numérica mayor.**
            """
        )

        st.dataframe(
            df_normalizado.round(2),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 12. REGRESIÓN LINEAL
# ============================================================

st.divider()

st.header("📈 6. Explorar relaciones con regresión lineal")

if numero_pacientes > 2:

    col_x, col_y = st.columns(2)

    with col_x:

        variable_x = st.selectbox(
            "Variable X",
            variables_vector,
            index=0
        )

    with col_y:

        variable_y = st.selectbox(
            "Variable Y",
            variables_vector,
            index=3
        )

    if variable_x == variable_y:

        st.warning(
            "Seleccione dos variables diferentes."
        )

    else:

        if st.button(
            "GENERAR REGRESIÓN LINEAL",
            use_container_width=True
        ):

            X_reg = df_analisis[
                [variable_x]
            ].values

            y_reg = df_analisis[
                variable_y
            ].values

            modelo = LinearRegression()

            modelo.fit(
                X_reg,
                y_reg
            )

            predicciones = modelo.predict(
                X_reg
            )

            residuos = (
                y_reg - predicciones
            )

            df_regresion = pd.DataFrame(
                {
                    variable_x:
                        df_analisis[variable_x].values,

                    variable_y:
                        df_analisis[variable_y].values,

                    "Predicción":
                        predicciones,

                    "Residuo":
                        residuos
                }
            )


            fig = px.scatter(
                df_regresion,
                x=variable_x,
                y=variable_y,
                title=f"{variable_x} vs {variable_y}"
            )


            orden = np.argsort(
                df_regresion[variable_x].values
            )


            fig.add_trace(
                go.Scatter(
                    x=df_regresion[
                        variable_x
                    ].values[orden],

                    y=predicciones[orden],

                    mode="lines",

                    name="Regresión lineal"
                )
            )


            indice_residuo = int(
                np.argmax(
                    np.abs(residuos)
                )
            )


            x_res = df_regresion.iloc[
                indice_residuo
            ][variable_x]

            y_real = df_regresion.iloc[
                indice_residuo
            ][variable_y]

            y_pred = df_regresion.iloc[
                indice_residuo
            ]["Predicción"]


            fig.add_trace(
                go.Scatter(
                    x=[x_res, x_res],
                    y=[y_pred, y_real],
                    mode="lines+markers",
                    name="Residuo"
                )
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


            pendiente = modelo.coef_[0]

            r2 = modelo.score(
                X_reg,
                y_reg
            )


            st.subheader("Interpretación")

            if pendiente > 0:

                st.write(
                    f"""
                    En esta muestra existe una tendencia positiva:

                    a medida que aumenta **{variable_x}**,
                    también tiende a aumentar **{variable_y}**.
                    """
                )

            elif pendiente < 0:

                st.write(
                    f"""
                    En esta muestra existe una tendencia negativa:

                    a medida que aumenta **{variable_x}**,
                    **{variable_y}** tiende a disminuir.
                    """
                )

            else:

                st.write(
                    "No se observa una tendencia lineal clara."
                )


            st.write(
                f"**Pendiente:** {pendiente:.2f}"
            )

            st.write(
                f"**R²:** {r2:.2f}"
            )

            st.info(
                """
                💡 El **residuo** representa la diferencia entre
                el valor observado y el valor predicho por la línea.
                """
            )


            if variable_x == "Edad" and pendiente > 0:

                st.caption(
                    "😄 Versión docente no científica: "
                    "parece que envejecer viene con actualizaciones... "
                    "pero no todas son mejoras."
                )


# ============================================================
# 13. SIMILITUD ENTRE PACIENTES EN 3D
# ============================================================

st.divider()

st.header("🧭 7. Similitud entre pacientes en 3D")

if numero_pacientes >= 3:

    st.write(
        """
        Utilizaremos las cinco variables simultáneamente.

        Primero normalizamos los datos y luego aplicamos PCA
        para representar los pacientes en tres dimensiones.

        **Puntos cercanos = perfiles matemáticamente similares.**
        """
    )

    if st.button(
        "GENERAR MAPA 3D DE SIMILITUD",
        use_container_width=True
    ):

        scaler = StandardScaler()

        X_std = scaler.fit_transform(
            matriz_vectores
        )


        distancias = pairwise_distances(
            X_std,
            metric="euclidean"
        )


        dist_busqueda = distancias.copy()

        np.fill_diagonal(
            dist_busqueda,
            np.inf
        )


        pos_min = np.unravel_index(
            np.argmin(dist_busqueda),
            dist_busqueda.shape
        )

        i_similar = pos_min[0]
        j_similar = pos_min[1]


        pos_max = np.unravel_index(
            np.argmax(distancias),
            distancias.shape
        )

        i_diferente = pos_max[0]
        j_diferente = pos_max[1]


        pca = PCA(
            n_components=3
        )

        coordenadas = pca.fit_transform(
            X_std
        )


        df_pca = pd.DataFrame(
            {
                "PC1":
                    coordenadas[:, 0],

                "PC2":
                    coordenadas[:, 1],

                "PC3":
                    coordenadas[:, 2],

                "Paciente":
                    df_analisis[
                        "Paciente"
                    ].astype(str).values,

                "Estudiante":
                    df_analisis[
                        "Estudiante"
                    ].astype(str).values,

                "Edad":
                    df_analisis[
                        "Edad"
                    ].values,

                "IMC":
                    df_analisis[
                        "IMC"
                    ].values,

                "PAS":
                    df_analisis[
                        "PAS"
                    ].values,

                "LDL":
                    df_analisis[
                        "LDL"
                    ].values,

                "HbA1c":
                    df_analisis[
                        "HbA1c"
                    ].values
            }
        )


        fig3d = px.scatter_3d(
            df_pca,
            x="PC1",
            y="PC2",
            z="PC3",

            hover_name="Paciente",

            hover_data=[
                "Estudiante",
                "Edad",
                "IMC",
                "PAS",
                "LDL",
                "HbA1c"
            ],

            title="Mapa 3D de similitud entre pacientes"
        )


        fig3d.update_traces(
            marker=dict(
                size=6
            )
        )


        st.plotly_chart(
            fig3d,
            use_container_width=True
        )


        nombre_similar_1 = (
            df_analisis.iloc[
                i_similar
            ]["Paciente"]
        )

        nombre_similar_2 = (
            df_analisis.iloc[
                j_similar
            ]["Paciente"]
        )


        nombre_diferente_1 = (
            df_analisis.iloc[
                i_diferente
            ]["Paciente"]
        )

        nombre_diferente_2 = (
            df_analisis.iloc[
                j_diferente
            ]["Paciente"]
        )


        st.subheader(
            "👥 Pacientes más similares"
        )

        st.write(
            f"""
            **{nombre_similar_1}**
            y
            **{nombre_similar_2}**

            Distancia estandarizada:
            **{distancias[i_similar, j_similar]:.2f}**
            """
        )


        st.dataframe(
            df_analisis.iloc[
                [i_similar, j_similar]
            ][
                [
                    "Estudiante",
                    "Paciente",
                    "Edad",
                    "IMC",
                    "PAS",
                    "LDL",
                    "HbA1c"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )


        st.subheader(
            "↔️ Pacientes más diferentes"
        )

        st.write(
            f"""
            **{nombre_diferente_1}**
            y
            **{nombre_diferente_2}**

            Distancia estandarizada:
            **{distancias[i_diferente, j_diferente]:.2f}**
            """
        )


        st.dataframe(
            df_analisis.iloc[
                [i_diferente, j_diferente]
            ][
                [
                    "Estudiante",
                    "Paciente",
                    "Edad",
                    "IMC",
                    "PAS",
                    "LDL",
                    "HbA1c"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )


        informacion_3d = (
            pca.explained_variance_ratio_
            .sum()
            * 100
        )


        st.info(
            f"""
            Las tres dimensiones de esta gráfica conservan
            aproximadamente **{informacion_3d:.1f}%**
            de la variabilidad de los datos.
            """
        )


        st.write(
            """
            **Interpretación:**

            Los pacientes cercanos en el espacio tridimensional
            tienen perfiles globales más parecidos considerando
            simultáneamente Edad, IMC, PAS, LDL y HbA1c.

            Los pacientes más alejados presentan perfiles más
            diferentes dentro de esta muestra.
            """
        )

        st.warning(
            """
            Similitud matemática no significa necesariamente
            similitud diagnóstica.
            """
        )


# ============================================================
# 14. CIERRE DOCENTE
# ============================================================

st.divider()

st.header("🎯 Idea para llevar a casa")

st.success(
    """
    Paciente
    → Vector
    → Normalización
    → Relaciones
    → Distancia
    → Similitud
    → Patrones
    """
)

st.write(
    """
    La inteligencia artificial y el aprendizaje automático
    parten muchas veces de algo conceptualmente sencillo:

    **convertir observaciones del mundo real en representaciones
    matemáticas que puedan ser comparadas y analizadas.**
    """
)
