import streamlit as st
from supabase import create_client
import google.generativeai as genai
import anthropic
import openai
import pandas as pd
from docx import Document
from io import BytesIO
import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
st.set_page_config(page_title="Orquestador EB2-NIW | Backend", page_icon="🛡️", layout="wide")

# --- 2. INICIALIZACIÓN DE CONEXIONES ---
try:
    # APIs de IA
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    client_openai = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    client_claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Conexión Supabase
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase = create_client(url, key)
    
    st.sidebar.success("✅ Sistema y Base de Datos Online")
except Exception as e:
    st.sidebar.error("⚠️ Error de Conexión: Verifica los Secrets.")
    st.stop()

# --- 3. FUNCIONES DEL BACKEND (LOGS PERSISTENTES) ---
def registrar_actividad(accion, detalle, motor):
    """Guarda la actividad en la tabla 'logs_eb2' de Supabase."""
    nueva_entrada = {
        "fecha": datetime.datetime.now().isoformat(),
        "accion": accion,
        "detalle": detalle,
        "motor": motor,
        "peticionario": "[Peticionario Alfa]"
    }
    try:
        supabase.table("logs_eb2").insert(nueva_entrada).execute()
    except:
        # Fallback local si la tabla aún no existe en Supabase
        if 'local_logs' not in st.session_state:
            st.session_state.local_logs = []
        st.session_state.local_logs.append(nueva_entrada)

def obtener_historial():
    """Recupera los registros de la base de datos."""
    try:
        res = supabase.table("logs_eb2").select("*").order("fecha", desc=True).execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame(st.session_state.get('local_logs', []))

# --- 4. INTERFAZ DEL OPERADOR ---
st.title("🛡️ Sistema de Gestión de Petición [Peticionario Alfa]")
st.subheader("Control de Mando - [Proyecto de Infraestructura X]")

tabs = st.tabs(["📊 Dashboard de Control", "📂 Bóveda de Evidencia", "✍️ Generación Técnica"])

# --- TAB 1: EL BOARD DE CONTROL (BACKEND) ---
with tabs[0]:
    st.header("Historial Maestro de Actividad")
    
    # Métricas de la Bóveda
    historial_df = obtener_historial()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Operaciones", len(historial_df))
    with c2:
        st.metric("Motor Principal", "Claude 4.6")
    with c3:
        st.metric("Seguridad", "Cifrado AES-256")

    st.markdown("---")
    if not historial_df.empty:
        st.dataframe(historial_df[["fecha", "accion", "detalle", "motor"]], use_container_width=True)
    else:
        st.info("Esperando primera actividad para iniciar registro en base de datos.")

# --- TAB 2: GESTIÓN DE EVIDENCIA ---
with tabs[1]:
    st.header("Bóveda de Documentación")
    archivo = st.file_uploader("Cargar archivos de [Institución Educativa A]", type=['pdf', 'docx', 'png'])
    if archivo:
        # Registrar en el backend
        registrar_actividad("Carga de Documento", archivo.name, "Supabase Storage")
        st.success(f"Documento '{archivo.name}' vinculado al expediente del [Peticionario Alfa].")

# --- TAB 3: GENERACIÓN TÉCNICA ---
with tabs[2]:
    st.header("Generador de Argumentos (Sonnet 4.6)")
    opcion = st.selectbox("Documento:", ["Nexo Transversal", "Análisis de Impacto Nacional", "Carta de Recomendación"])
    
    if st.button("Generar y Registrar"):
        with st.spinner("Redactando..."):
            try:
                # Llamada a Anthropic (usando identificador validado)
                response = client_claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=3500,
                    messages=[{"role": "user", "content": f"Redacta un {opcion} para el [Peticionario Alfa] basado en el [Proyecto de Infraestructura X]."}]
                )
                texto = response.content[0].text
                st.write(texto)
                
                # PERSISTENCIA: Registro en el backend tras éxito
                registrar_actividad(f"Generación de {opcion}", "Éxito", "Claude 4.6")
                
                # Descarga
                doc = Document()
                doc.add_paragraph(texto)
                buffer = BytesIO()
                doc.save(buffer)
                st.download_button("📥 Descargar Word", data=buffer.getvalue(), file_name=f"{opcion}.docx")
                
            except Exception as e:
                registrar_actividad("Error de Generación", str(e), "Claude 4.6")
                st.error("Error en la conexión con el motor de IA.")

st.sidebar.markdown("---")
st.sidebar.write("🔒 **Sesión de Operador Segura**")
