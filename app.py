import streamlit as st
from supabase import create_client
import google.generativeai as genai

# Configuración de Seguridad y Título
st.set_page_config(page_title="Sistema EB2-NIW Master", layout="wide")
st.title("🛡️ Sistema de Gestión EB2-NIW (Patrón GENERAL.)")

# Conectar con tus llaves (Secrets)
try:
    supabase_url = st.secrets["supabase"]["url"]
    supabase_key = st.secrets["supabase"]["key"]
    supabase = create_client(supabase_url, supabase_key)
    
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("✅ Conexión con APIs exitosa")
except Exception as e:
    st.sidebar.error("❌ Falta configurar los Secrets en Streamlit")
    st.sidebar.info("Ve a 'Advanced Settings' en Streamlit Cloud y pega tus llaves.")

# Interfaz de usuario
st.write("Bienvenido al sistema de orquestación para el [Peticionario Alfa].")

tab1, tab2 = st.tabs(["📁 Gestión de Evidencia", "📝 Generación de Documentos"])

with tab1:
    st.subheader("Carga de Documentación")
    archivo = st.file_uploader("Subir evidencia para el [Proyecto de Infraestructura X]", type=['pdf', 'png', 'jpg'])
    if archivo:
        st.info("Archivo recibido. Procesando bajo protocolos de seguridad del Patrón GENERAL.")

with tab2:
    st.subheader("Generador de Argumentación Legal")
    if st.button("Sintetizar Nexo Transversal"):
        st.markdown("### Borrador Generado:")
        st.write("El [Peticionario Alfa] presenta un perfil de alto impacto nacional...")
        st.caption("Nota: Este borrador debe ser revisado por el equipo legal.")
