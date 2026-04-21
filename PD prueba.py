import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Título de la App
st.set_page_config(page_title="Registro de Retiros", page_icon="📝")
st.title("Sistema de Normalización de Retiros")

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulario
with st.form(key="retiro_form"):
    st.subheader("Datos del Colaborador")
    nombre = st.text_input("Nombre completo")
    
    # NORMALIZACIÓN: Aquí defines las categorías fijas para Power BI
    motivo = st.selectbox("Motivo del retiro (Categorizado)", [
        "Renuncia Voluntaria",
        "Mejor oferta laboral",
        "Motivos personales",
        "Terminación de contrato",
        "Despido con causa",
        "Jubilación"
    ])
    
    fecha = st.date_input("Fecha efectiva del retiro")
    comentarios = st.text_area("Detalles adicionales (opcional)")
    
    boton_guardar = st.form_submit_button("Registrar Retiro")

if boton_guardar:
    if nombre:
        # 1. Leer datos actuales
        df_existente = conn.read()
        
        # 2. Crear nueva fila
        nueva_fila = pd.DataFrame([{
            "Fecha_Registro": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "Nombre_Colaborador": nombre,
            "Motivo_Retiro": motivo,
            "Fecha_Retiro": str(fecha),
            "Observaciones": comentarios
        }])
        
        # 3. Concatenar y actualizar
        df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(data=df_final)
        
        st.success(f"✅ ¡Registro de {nombre} guardado con éxito!")
        st.balloons()
    else:
        st.warning("⚠️ Por favor ingresa el nombre del colaborador.")