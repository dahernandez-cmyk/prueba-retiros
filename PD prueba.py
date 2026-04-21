import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FORMULARIO ---
with st.form(key="retiro_form"):
    nombre = st.text_input("Nombre completo")
    motivo = st.selectbox("Motivo del retiro", ["Renuncia", "Despido", "Jubilación"])
    fecha = st.date_input("Fecha")
    boton_guardar = st.form_submit_button("Registrar")

if boton_guardar:
    if nombre:
        # 1. LEER los datos que ya están en el Google Sheet
        # Esto trae lo que ya han escrito tus compañeras
        df_actual = conn.read()
        
        # Limpiar filas vacías que Google Sheets a veces trae al final
        df_actual = df_actual.dropna(how="all")

        # 2. CREAR el nuevo registro
        nuevo_registro = pd.DataFrame([{
            "Nombre": nombre,
            "Motivo": motivo,
            "Fecha": str(fecha)
        }])

        # 3. UNIR los datos viejos con el nuevo (Append)
        # Esto pone la nueva fila al final de la lista
        df_actualizado = pd.concat([df_actual, nuevo_registro], ignore_index=True)

        # 4. ACTUALIZAR la hoja con la lista completa revisada
        conn.update(data=df_actualizado)
        
        st.success(f"¡Registro de {nombre} guardado exitosamente!")
    else:
        st.error("El nombre es obligatorio.")