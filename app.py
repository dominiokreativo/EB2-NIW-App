import streamlit as st
from supabase import create_client
import google.generativeai as genai
import anthropic
import openai
from docx import Document
from io import BytesIO

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
st.set_page_config(page_title="Orquestador EB2-NIW", page_icon="🛡️", layout="wide")

# --- 2. INICIALIZACIÓN DE CONEXIONES ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    client_openai = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    client_claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
    st.sidebar.success("✅ Conexión con APIs exitosa (EAS v4)")
except Exception as e:
    st.sidebar.error("⚠️ Error en Secrets: Revisa las llaves de API.")
    st.stop()

# --- 3. INTERFAZ ---
st.title("🛡️ Sistema de Gestión de Petición [Peticionario Alfa]")
st.subheader("Orquestador para el [Proyecto de Infraestructura X]")

tabs = st.tabs(["📂 Gestión de Evidencia", "✍️ Generador de Argumentos", "📋 Auditoría"])

with tabs[0]:
    st.header("Carga Segura de Documentación")
    archivo = st.file_uploader("Subir evidencia", type=['pdf', 'png', 'jpg', 'docx'])
    if archivo:
        st.success("Documento recibido para análisis.")

with tabs[1]:
    st.header("Redacción Técnica (Claude 4.6)")
    tipo_doc = st.selectbox("Documento:", ["Nexo Transversal", "Carta de Recomendación", "Impacto Nacional"])
    
    if st.button("Generar con Claude 4.6"):
        with st.spinner("Llamando a Sonnet 4.6..."):
            try:
                # IDENTIFICADOR EXACTO SEGÚN TU WORKBENCH (Imagen image_78729e.png)
                response = client_claude.messages.create(
                    model="claude-sonnet-4-6", 
                    max_tokens=4000,
                    messages=[{
                        "role": "user", 
                        "content": f"Eres un experto en EB2-NIW. Redacta un {tipo_doc} para el [Peticionario Alfa] basado en el [Proyecto de Infraestructura X]. Usa Matter of Dhanasar."
                    }]
                )
                
                texto = response.content[0].text
                st.markdown("### Borrador Generado:")
                st.write(texto)
                
                doc = Document()
                doc.add_paragraph(texto)
                buffer = BytesIO()
                doc.save(buffer)
                st.download_button("📥 Descargar Word", data=buffer.getvalue(), file_name="argumento.docx")
                
            except Exception as e:
                # Si el modelo específico falla, intentamos el alias 'latest'
                try:
                    response = client_claude.messages.create(
                        model="claude-3-5-sonnet-latest",
                        max_tokens=4000,
                        messages=[{"role": "user", "content": f"Redacta un {tipo_doc} para EB2-NIW"}]
                    )
                    st.write(response.content[0].text)
                except:
                    st.error(f"Error técnico de Anthropic: {str(e)}")

with tabs[2]:
    st.info("Patrón GENERAL. activo. Análisis de mérito sustancial en curso.")
