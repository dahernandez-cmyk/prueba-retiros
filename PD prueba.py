import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.title("Registro de Retiros (Sin sobreescritura)")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form(key="formulario_retiros"):
    fecha_novedad = st.date_input("Fecha de la Novedad")
    nombre = st.text_input("Nombre del Colaborador")
    motivo = st.selectbox("Motivo", ["Renuncia Voluntaria", "Terminación de Contrato", "Mejor Oferta", "Jubilación", "Despido", "Personal"])
    observaciones = st.text_area("Observaciones")
    submit_button = st.form_submit_button(label="Guardar")

if submit_button:
    if nombre:
        try:
            # --- CAMBIO CLAVE 1: ttl=0 para leer datos reales en tiempo real ---
            df_existente = conn.read(ttl=0)
            
            # --- CAMBIO CLAVE 2: Limpiar filas y columnas totalmente vacías ---
            if df_existente is not None:
                df_existente = df_existente.dropna(how="all").reset_index(drop=True)
            else:
                df_existente = pd.DataFrame()

            # Nuevo registro
            nuevo_registro = pd.DataFrame([{
                "Fecha_Registro": datetime.now().strftime("%Y-%m-%d"),
                "Fecha_Novedad": str(fecha_novedad),
                "Nombre_Colaborador": nombre,
                "Motivo_Retiro": motivo,
                "Observaciones": observaciones
            }])

            # --- CAMBIO CLAVE 3: Concatenación limpia ---
            if not df_existente.empty:
                df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
            else:
                df_actualizado = nuevo_registro

            # Subir todo
            conn.update(data=df_actualizado)
            st.success(f"Registrado correctamente en la fila {len(df_actualizado) + 1}")
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Escribe el nombre.")