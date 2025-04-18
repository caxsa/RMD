
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import os

# Ruta del archivo Excel
file_path = "RegistroMateriales_App.xlsx"

# Cargar datos existentes si el archivo ya existe
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=["Solicitante", "Proyecto", "Material", "Cantidad", "Unidad", "Fecha"])

st.title("📦 Registro de Materiales Usados en Proyectos")

st.sidebar.header("➕ Ingresar nuevo material")

# Formulario para agregar nuevo registro
with st.sidebar.form("form_material"):
    solicitante = st.text_input("Nombre del solicitante")
    proyecto = st.text_input("Nombre del proyecto")
    material = st.text_input("Material")  # campo editable
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    unidad = st.selectbox("Unidad", ["Unidades"])
    fecha = st.date_input("Fecha de uso", value=datetime.today())
    submit = st.form_submit_button("Registrar material")

    if submit:
        nuevo_registro = {
            "Solicitante": solicitante,
            "Proyecto": proyecto,
            "Material": material,
            "Cantidad": cantidad,
            "Unidad": unidad,
            "Fecha": fecha
        }
        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        df.to_excel(file_path, index=False)
        st.success("✅ Material registrado correctamente.")

# Visualizar los datos actuales
st.subheader("📋 Materiales registrados")
st.dataframe(df)

# Filtros
st.subheader("🔍 Filtrar por solicitante")
solicitantes = df["Solicitante"].dropna().unique()
selected_solicitante = st.selectbox("Seleccionar solicitante", ["Todos"] + list(solicitantes))

if selected_solicitante != "Todos":
    filtrado = df[df["Solicitante"] == selected_solicitante]
else:
    filtrado = df

# Mostrar resumen filtrado
st.subheader("📊 Resumen de materiales utilizados")
st.write(f"Total de materiales usados por '{selected_solicitante}': {filtrado['Cantidad'].sum()}")
st.dataframe(filtrado)

# Descargar como Excel
excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False, engine="openpyxl")
excel_buffer.seek(0)
st.download_button(
    label="⬇️ Descargar registro total (Excel)",
    data=excel_buffer,
    file_name="Registro_Materiales_Completo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
