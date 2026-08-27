import streamlit as st

st.set_page_config(
    page_title="Vectores en Biomedicina",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Ejercicio para comprender vectores")

st.write(
    """
    En este ejercicio representaremos pacientes mediante números.

    Cada paciente tendrá cinco características:

    **Edad, IMC, PAS, LDL y HbA1c**

    Estas características formarán un vector.
    """
)

st.info(
    "Paciente → [Edad, IMC, PAS, LDL, HbA1c]"
)

st.success("Aplicación funcionando correctamente ✅")
