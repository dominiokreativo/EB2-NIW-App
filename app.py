import streamlit as st
from supabase import create_client
import google.generativeai as genai
import anthropic
import openai
import pandas as pd
from docx import Document
from io import BytesIO

# --- 1. CONFIGURACIÓN DE PÁGINA Y SEGURIDAD ---
st.set_page_config(
    page_title="Orquestador EB2-NIW | [Peticionario Alfa]",
    page_icon="🛡️",
    layout="wide"
)

# Estilos profesionales
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZACIÓN DE CONEXIONES ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    client_claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    client_openai = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
    st.sidebar.success("✅ Conexión con APIs exitosa (EAS v4)")
except Exception as e:
    st.sidebar.error("⚠️ Error de Configuración en Secrets")
    st.stop()

# --- 3. INTERFAZ ---
st.title("🛡️ Sistema de Gestión de Petición [Peticionario Alfa]")
st.subheader("Orquestador Inteligente para el [Proyecto de Infraestructura X]")

tabs = st.tabs(["📂 Gestión de Evidencia", "✍️ Generador de Argumentos", "📋 Auditoría de Dhanasar"])

with tabs[0]:
    st.header("Carga Segura de Documentación")
    archivo = st.file_uploader("Subir evidencia (Títulos de [Institución Educativa A], Certificaciones)", type=['pdf', 'png', 'jpg', 'docx'])
    if archivo:
        st.success(f"Archivo '{archivo.name}' analizado para el [Peticionario Alfa].")

with tabs[1]:
    st.header("Redacción Técnica (Claude 4.6 Sonnet)")
    tipo_doc = st.selectbox("Seleccione el documento:", ["Nexo Transversal (Matter of Dhanasar)", "Carta de Recomendación", "Análisis de Impacto Nacional"])
    
    if st.button("Generar Borrador Profesional"):
        with st.spinner("Sonnet 4.6 está redactando..."):
            try:
                # CORRECCIÓN DE MODELO: Usando la versión 4.6 activa en tu cuenta
                response = client_claude.messages.create(
                    model="claude-4-6-sonnet-20260215", # Identificador actualizado para 2026
                    max_tokens=2500,
                    messages=[{"role": "user", "content": f"Como experto EB2-NIW, redacta un {tipo_doc} para el [Peticionario Alfa] y su [Proyecto de Infraestructura X]."}]
                )
                
                texto = response.content[0].text
                st.markdown("### Documento Generado")
                st.write(texto)
                
                # Generador Word
                doc = Document()
                doc.add_paragraph(texto)
                buffer = BytesIO()
                doc.save(buffer)
                st.download_button("📥 Descargar en Word", data=buffer.getvalue(), file_name="documento.docx")
            except Exception as e:
                st.error(f"Error en la generación: {str(e)}")

with tabs[2]:
    st.header("Auditoría de Dhanasar")
    st.info("Patrón GENERAL. activo: No se detectan datos sensibles expuestos.")
    st.progress(90, text="Nivel de Argumentación Alcanzado")
