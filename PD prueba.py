import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Registro de Retiros", page_icon="👥")
st.title("Formulario de Normalización de Retiros")

# Establecer la conexión con los secrets que ya configuramos
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FORMULARIO DE ENTRADA ---
with st.form(key="formulario_retiros"):
    st.subheader("Ingrese los detalles del retiro")
    
    # Campo: Nombre_Colaborador
    nombre = st.text_input("Nombre del Colaborador")
    
    # Campo: Motivo_Retiro (Normalizado para Power BI)
    motivo = st.selectbox("Motivo del Retiro", [
        "Renuncia Voluntaria",
        "Terminación de Contrato",
        "Mejor Oferta Laboral",
        "Jubilación",
        "Despido con Causa",
        "Motivos Personales"
    ])
    
    # Campo: Observaciones
    observaciones = st.text_area("Observaciones adicionales")
    
    # Botón de envío
    submit_button = st.form_submit_button(label="Guardar Información")

if submit_button:
    if nombre:
        try:
            # 1. LEER los datos actuales de la hoja
            # Si la hoja está vacía, esto creará un DataFrame vacío
            df_existente = conn.read().dropna(how="all")

            # 2. CREAR el nuevo registro con TUS campos exactos
            # Fecha_Registro se genera automáticamente con la fecha de hoy
            nuevo_registro = pd.DataFrame([{
                "Fecha_Registro": datetime.now().strftime("%Y-%m-%d"),
                "Nombre_Colaborador": nombre,
                "Motivo_Retiro": motivo,
                "Observaciones": observaciones
            }])

            # 3. UNIR los datos previos con el nuevo registro
            # Esto evita que se borre lo anterior
            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)

            # 4. SUBIR todo de nuevo al Google Sheet
            conn.update(data=df_actualizado)

            st.success(f"✅ El registro de {nombre} ha sido guardado correctamente.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Hubo un error al conectar con Google Sheets: {e}")
    else:
        st.warning("⚠️ El campo 'Nombre del Colaborador' es obligatorio.")

# --- VISTA PREVIA OPCIONAL ---
if st.checkbox("Mostrar registros recientes"):
    df_vista = conn.read().dropna(how="all")
    st.dataframe(df_vista.tail(10)) # Muestra los últimos 10