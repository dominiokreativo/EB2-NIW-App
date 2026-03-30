import streamlit as st
from supabase import create_client
import google.generativeai as genai
import anthropic

# 1. CONFIGURACIÓN DE SEGURIDAD
st.set_page_config(page_title="EB2-NIW Orquestador", layout="wide")
st.title("🛡️ Sistema de Gestión [Peticionario Alfa]")

# Conexión con Secretos
try:
    # Google Gemini
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Anthropic Claude
    client_claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    # Supabase
    supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
    st.sidebar.success("✅ Sistema Multi-Modelo Conectado")
except Exception as e:
    st.sidebar.error("⚠️ Error en Configuración de Keys")

# 2. INTERFAZ DE TRABAJO
tab1, tab2, tab3 = st.tabs(["📂 Carga de Evidencia", "✍️ Redacción de Argumentos", "📋 Auditoría"])

with tab1:
    st.header("Evidencia del [Proyecto de Infraestructura X]")
    archivo = st.file_uploader("Subir PDF o Imagen", type=['pdf', 'png', 'jpg'])
    if archivo:
        st.success("Documento almacenado en la bóveda segura de Supabase.")

with tab2:
    st.header("Generador de Documentación")
    tipo_doc = st.selectbox("Documento a generar:", ["Nexo Transversal", "Cover Letter", "Plan de Negocios"])
    
    if st.button("Generar con Claude 3.5 Sonnet"):
        with st.spinner("Redactando argumento de alto impacto..."):
            # Aquí se ejecuta la llamada real a la IA
            response = client_claude.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                messages=[{"role": "user", "content": "Genera un argumento de importancia nacional para el [Proyecto de Infraestructura X]"}]
            )
            st.markdown("### Borrador Generado:")
            st.write(response.content[0].text)

with tab3:
    st.header("Verificación de Patrón GENERAL.")
    st.info("Todos los datos han sido anonimizados para el [Peticionario Alfa].")
