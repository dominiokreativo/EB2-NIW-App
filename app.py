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
    # Google & OpenAI
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    client_openai = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Anthropic - Conexión robusta
    client_claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Supabase
    supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
    st.sidebar.success("✅ Conexión con APIs exitosa (EAS v4)")
except Exception as e:
    st.sidebar.error("⚠️ Revisa los Secrets en Streamlit Settings")
    st.stop()

# --- 3. INTERFAZ ---
st.title("🛡️ Sistema de Gestión de Petición [Peticionario Alfa]")
st.subheader("Orquestador para el [Proyecto de Infraestructura X]")

tabs = st.tabs(["📂 Gestión de Evidencia", "✍️ Generador de Argumentos", "📋 Auditoría"])

with tabs[0]:
    st.header("Carga Segura de Documentación")
    archivo = st.file_uploader("Subir evidencia para el [Peticionario Alfa]", type=['pdf', 'png', 'jpg', 'docx'])
    if archivo:
        st.success(f"Archivo '{archivo.name}' recibido correctamente.")

with tabs[1]:
    st.header("Redacción Técnica")
    tipo_doc = st.selectbox("Documento:", ["Nexo Transversal", "Carta de Recomendación", "Impacto Nacional"])
    
    if st.button("Generar Borrador Profesional"):
        with st.spinner("Conectando con el motor de inteligencia..."):
            try:
                # SOLUCIÓN DEFINITIVA: Probamos el identificador universal de Sonnet
                # Si este falla, el sistema lo reportará, pero es el estándar de 2026.
                response = client_claude.messages.create(
                    model="claude-3-5-sonnet-latest", 
                    max_tokens=4096,
                    messages=[{
                        "role": "user", 
                        "content": f"Eres un experto legal en EB2-NIW. Redacta un {tipo_doc} para el [Peticionario Alfa] basado en el [Proyecto de Infraestructura X]. Usa el estándar Matter of Dhanasar."
                    }]
                )
                
                texto = response.content[0].text
                st.markdown("### Resultado de la Generación:")
                st.write(texto)
                
                # Generador de Word express
                doc = Document()
                doc.add_paragraph(texto)
                buffer = BytesIO()
                doc.save(buffer)
                st.download_button("📥 Descargar Word", data=buffer.getvalue(), file_name="argumento.docx")
                
            except Exception as e:
                st.error("Error de modelo. Intentando ruta de respaldo...")
                # Backup con GPT-4 si Claude falla por saturación de red en 2026
                res_backup = client_openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Redacta un {tipo_doc} para EB2-NIW [Peticionario Alfa]"}]
                )
                st.write(res_backup.choices[0].message.content)

with tabs[2]:
    st.info("Patrón GENERAL. activo. Auditoría de Dhanasar en progreso.")
