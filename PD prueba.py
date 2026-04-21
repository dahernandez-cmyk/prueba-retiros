import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Registro de Retiros", page_icon="👥")
st.title("Formulario de Normalización de Retiros")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FORMULARIO DE ENTRADA ---
with st.form(key="formulario_retiros"):
    st.subheader("Ingrese los detalles del retiro")
    
    # Nuevo Campo: Fecha de la Novedad (Cuándo ocurrió el retiro)
    fecha_novedad = st.date_input("Fecha de la Novedad (Día del retiro)")
    
    # Campo: Nombre_Colaborador
    nombre = st.text_input("Nombre del Colaborador")
    
    # Campo: Motivo_Retiro
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
    
    submit_button = st.form_submit_button(label="Guardar Información")

if submit_button:
    if nombre:
        try:
            # 1. LEER datos actuales
            df_existente = conn.read().dropna(how="all")

            # 2. CREAR el nuevo registro con el campo Fecha_Novedad
            nuevo_registro = pd.DataFrame([{
                "Fecha_Registro": datetime.now().strftime("%Y-%m-%d"), # Automática
                "Fecha_Novedad": str(fecha_novedad),                 # Elegida por la usuaria
                "Nombre_Colaborador": nombre,
                "Motivo_Retiro": motivo,
                "Observaciones": observaciones
            }])

            # 3. UNIR datos (Append)
            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)

            # 4. ACTUALIZAR Google Sheets
            conn.update(data=df_actualizado)

            st.success(f"✅ ¡Registro de {nombre} guardado correctamente!")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error al guardar: {e}")
    else:
        st.warning("⚠️ El nombre es obligatorio.")

# Vista previa para verificar las columnas
if st.checkbox("Ver base de datos actual"):
    df_vista = conn.read().dropna(how="all")
    st.dataframe(df_vista)