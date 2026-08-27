import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA APP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Vectores en Biomedicina",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Ejercicio para comprender vectores")

st.write(
    """
    Esta aplicación permitirá registrar pacientes ficticios
    y posteriormente convertirlos en vectores para analizarlos.
    """
)


# ---------------------------------------------------------
# CONEXIÓN CON GOOGLE SHEETS
# ---------------------------------------------------------

# Definimos los permisos que necesita nuestra cuenta de servicio.

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# Leemos las credenciales privadas desde Streamlit Secrets.

credentials = Credentials.from_service_account_info(
    dict(st.secrets["gcp_service_account"]),
    scopes=scopes
)


# Creamos la conexión con Google Sheets.

client = gspread.authorize(credentials)


# Leemos el ID de la hoja que guardamos en Secrets.

spreadsheet_id = st.secrets["google_sheet"]["spreadsheet_id"]


# Abrimos el archivo de Google Sheets.

spreadsheet = client.open_by_key(spreadsheet_id)


# Abrimos la primera pestaña de la hoja.

worksheet = spreadsheet.sheet1


# ---------------------------------------------------------
# FORMULARIO DE PRUEBA
# ---------------------------------------------------------

st.subheader("1. Ingrese un paciente de prueba")

estudiante = st.text_input(
    "Nombre o código del estudiante",
    value="Estudiante 1"
)

paciente = st.text_input(
    "Paciente",
    value="Paciente 1"
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    edad = st.number_input(
        "Edad",
        min_value=18,
        max_value=100,
        value=68
    )

with col2:
    imc = st.number_input(
        "IMC",
        min_value=10.0,
        max_value=60.0,
        value=31.0
    )

with col3:
    pas = st.number_input(
        "PAS",
        min_value=70,
        max_value=250,
        value=148
    )

with col4:
    ldl = st.number_input(
        "LDL",
        min_value=20,
        max_value=400,
        value=170
    )

with col5:
    hba1c = st.number_input(
        "HbA1c",
        min_value=3.0,
        max_value=20.0,
        value=7.2
    )


# ---------------------------------------------------------
# GUARDAR PACIENTE
# ---------------------------------------------------------

if st.button(
    "💾 GUARDAR PACIENTE",
    type="primary"
):

    nueva_fila = [
        estudiante,
        paciente,
        edad,
        imc,
        pas,
        ldl,
        hba1c
    ]

    worksheet.append_row(
        nueva_fila,
        value_input_option="USER_ENTERED"
    )

    st.success(
        "✅ Paciente guardado correctamente en Google Sheets"
    )


# ---------------------------------------------------------
# CONTADOR
# ---------------------------------------------------------

datos = worksheet.get_all_records()

st.divider()

st.metric(
    "Pacientes registrados",
    len(datos)
)
