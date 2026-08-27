# ============================================================
# APP: EJERCICIO PARA COMPRENDER VECTORES
# ============================================================
#
# OBJETIVO DOCENTE:
# Cada estudiante ingresará 10 pacientes ficticios.
#
# Cada paciente tendrá cinco características:
#
# Edad - IMC - PAS - LDL - HbA1c
#
# Después utilizaremos estos datos para mostrar cómo
# un paciente puede representarse matemáticamente
# mediante un VECTOR.
# ============================================================


import streamlit as st
import pandas as pd
import gspread

from google.oauth2.service_account import Credentials


# ============================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
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

    Cada estudiante aportará **10 pacientes ficticios**.

    Cada paciente será descrito mediante cinco características:

    **Edad · IMC · PAS · LDL · HbA1c**
    """
)

st.info(
    "Posteriormente convertiremos estos datos en vectores "
    "y exploraremos relaciones y similitudes entre pacientes."
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


spreadsheet_id = st.secrets[
    "google_sheet"
]["spreadsheet_id"]


spreadsheet = client.open_by_key(
    spreadsheet_id
)


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
    "No utilice información identificable de pacientes reales. "
    "Este ejercicio utiliza datos ficticios."
)


# ============================================================
# 4. DATOS PREDETERMINADOS
# ============================================================
#
# Los estudiantes NO necesitan escribir todo desde cero.
#
# Los datos aparecen previamente llenos.
#
# Pueden modificarlos para crear diferentes perfiles.
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

    **Modifique algunos valores** para crear sus propios
    pacientes ficticios.
    """
)


datos_editados = st.data_editor(

    datos_iniciales,

    num_rows="fixed",

    hide_index=True,

    use_container_width=True,

    column_config={

        "Paciente": st.column_config.TextColumn(
            "Paciente"
        ),

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


# ============================================================
# 6. EXPLICACIÓN DEL VECTOR
# ============================================================

st.info(
    """
    💡 Cada fila contiene cinco características numéricas.

    Por ejemplo:

    **[68, 31, 148, 170, 7.2]**

    puede utilizarse como representación matemática
    de un paciente.
    """
)


# ============================================================
# 7. BOTÓN PARA GUARDAR LOS 10 PACIENTES
# ============================================================

st.divider()

st.header("💾 3. Agregue sus pacientes al dataset colectivo")


if st.button(
    "GUARDAR MIS 10 PACIENTES",
    type="primary",
    use_container_width=True
):

    # Comprobamos que el estudiante se identificó.

    if estudiante.strip() == "":

        st.error(
            "⚠️ Escriba primero el nombre o código de su grupo."
        )

    else:

        filas_nuevas = []


        # Convertimos cada fila de la tabla
        # en una fila para Google Sheets.

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


        # Guardamos las 10 filas de una sola vez.

        worksheet.append_rows(
            filas_nuevas,
            value_input_option="USER_ENTERED"
        )


        st.success(
            "✅ ¡Sus 10 pacientes fueron agregados "
            "al dataset colectivo!"
        )


# ============================================================
# 8. LEEMOS EL DATASET COLECTIVO
# ============================================================

datos_colectivos = worksheet.get_all_records()


if len(datos_colectivos) > 0:

    df_colectivo = pd.DataFrame(
        datos_colectivos
    )

else:

    df_colectivo = pd.DataFrame()


# ============================================================
# 9. CONTADOR COLECTIVO
# ============================================================

st.divider()

st.header("📊 Dataset colectivo")


if len(df_colectivo) > 0:

    numero_pacientes = len(
        df_colectivo
    )

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


# ============================================================
# 10. BARRA DE PROGRESO
# ============================================================
#
# Nuestra meta docente será inicialmente 100 pacientes.
# ============================================================

meta = 100


progreso = min(
    numero_pacientes / meta,
    1.0
)


st.progress(
    progreso
)


st.write(
    f"**{numero_pacientes} / {meta} pacientes recolectados**"
)


if numero_pacientes >= meta:

    st.success(
        "🎉 Dataset listo para analizar."
    )

else:

    faltantes = meta - numero_pacientes

    st.caption(
        f"Faltan {faltantes} pacientes para alcanzar "
        f"la meta docente de {meta}."
    )


# ============================================================
# 11. MOSTRAR LOS DATOS
# ============================================================

if len(df_colectivo) > 0:

    with st.expander(
        "🔎 Ver pacientes recolectados"
    ):

        st.dataframe(
            df_colectivo,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 12. PRÓXIMA ETAPA
# ============================================================

st.divider()

st.header("🧬 ¿Qué haremos con estos datos?")


st.write(
    """
    Una vez tengamos nuestros pacientes podremos:

    **1. Generar los vectores**

    **2. Normalizar los vectores**

    **3. Explorar relaciones mediante regresión lineal**

    **4. Visualizar similitudes entre pacientes en 3D**
    """
)


st.info(
    "Paciente → Vector → Normalización → "
    "Relaciones → Similitud → Patrones"
)
# ============================================================
# 13. GENERAR VECTORES
# ============================================================

st.divider()

st.header("🧮 Generar vectores")


if numero_pacientes == 0:

    st.warning(
        "Todavía no hay pacientes suficientes para generar vectores."
    )

else:

    st.write(
        """
        Cada paciente puede representarse mediante un conjunto
        ordenado de características numéricas.

        Utilizaremos:

        **Edad, IMC, PAS, LDL y HbA1c**
        """
    )

    st.info(
        "Vector = [Edad, IMC, PAS, LDL, HbA1c]"
    )


    if st.button(
        "GENERAR VECTORES",
        use_container_width=True
    ):

        # ----------------------------------------------------
        # Seleccionamos únicamente las variables numéricas
        # que formarán cada vector.
        # ----------------------------------------------------

        variables_vector = [
            "Edad",
            "IMC",
            "PAS",
            "LDL",
            "HbA1c"
        ]


        # ----------------------------------------------------
        # Creamos una copia de los datos.
        # ----------------------------------------------------

        df_vectores = df_colectivo.copy()


        # ----------------------------------------------------
        # Convertimos las columnas a valores numéricos.
        # ----------------------------------------------------

        for variable in variables_vector:

            df_vectores[variable] = pd.to_numeric(
                df_vectores[variable],
                errors="coerce"
            )


        # Eliminamos filas incompletas.

        df_vectores = df_vectores.dropna(
            subset=variables_vector
        )


        st.success(
            f"✅ Se generaron {len(df_vectores)} vectores."
        )


        # ----------------------------------------------------
        # Mostramos algunos ejemplos
        # ----------------------------------------------------

        st.subheader("Ejemplos")


        numero_ejemplos = min(
            10,
            len(df_vectores)
        )


        for i in range(numero_ejemplos):

            fila = df_vectores.iloc[i]

            vector = [
                fila["Edad"],
                fila["IMC"],
                fila["PAS"],
                fila["LDL"],
                fila["HbA1c"]
            ]


            st.code(
                f'{fila["Estudiante"]} - '
                f'{fila["Paciente"]} = {vector}'
            )


        # ----------------------------------------------------
        # Creamos la matriz completa
        # ----------------------------------------------------

        matriz_vectores = df_vectores[
            variables_vector
        ].to_numpy()


        st.subheader("Matriz de vectores")


        st.write(
            f"""
            Tenemos una matriz de:

            **{matriz_vectores.shape[0]} pacientes ×
            {matriz_vectores.shape[1]} características**
            """
        )


        st.dataframe(
            df_vectores[
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
            use_container_width=True,
            hide_index=True
        )


        st.info(
            """
            💡 Ahora el computador ya no necesita interpretar
            una historia clínica completa.

            Cada paciente está representado mediante números
            que pueden ser comparados y analizados matemáticamente.
            """
        )
