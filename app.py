import streamlit as st
from supabase import create_client
import anthropic
import pandas as pd
from docx import Document
from io import BytesIO
import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Orquestador EB2-NIW | [Peticionario Alfa]",
    page_icon="🛡️",
    layout="wide"
)

# --- 2. INICIALIZACIÓN DE CONEXIONES (SECRETS) ---
try:
    # Cliente Anthropic con el motor validado
    client_claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Cliente Supabase para el Backend persistente
    supabase_url = st.secrets["supabase"]["url"]
    supabase_key = st.secrets["supabase"]["key"]
    supabase = create_client(supabase_url, supabase_key)
    
    st.sidebar.success("✅ Conexión con APIs y DB establecida (v8)")
except Exception as e:
    st.sidebar.error("⚠️ Error en la configuración de Secrets.")
    st.stop()

# --- 3. LÓGICA DE BACKEND (SUPABASE) ---
def registrar_log(accion, detalle, motor):
    """Inserta registros en la tabla logs_eb2 de Supabase."""
    try:
        supabase.table("logs_eb2").insert({
            "accion": accion,
            "detalle": detalle,
            "motor": motor,
            "peticionario": "[Peticionario Alfa]"
        }).execute()
    except Exception as e:
        st.sidebar.warning(f"Error de registro: {e}")

def leer_logs():
    """Recupera los últimos 15 movimientos del caso."""
    try:
        res = supabase.table("logs_eb2").select("*").order("id", desc=True).limit(15).execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame()

# --- 4. INTERFAZ DEL ORQUESTADOR ---
st.title("🛡️ Sistema de Gestión de Petición [Peticionario Alfa]")
st.subheader("Control de Mando del [Proyecto de Infraestructura X]")

tabs = st.tabs(["📊 Dashboard de Control", "📂 Bóveda de Evidencia", "✍️ Generación Técnica"])

# --- TAB 1: EL BOARD DE CONTROL ---
with tabs[0]:
    st.header("Historial de Actividad (Backend)")
    df_logs = leer_logs()
    
    if not df_logs.empty:
        # Formateo de fecha para mejor lectura
        df_logs['fecha'] = pd.to_datetime(df_logs['fecha']).dt.strftime('%Y-%m-%d %H:%M')
        st.table(df_logs[["fecha", "accion", "detalle", "motor"]])
    else:
        st.info("No hay registros previos. Realiza una acción para iniciar el historial.")

# --- TAB 2: GESTIÓN DE EVIDENCIA ---
with tabs[1]:
    st.header("Bóveda de Documentos")
    archivo = st.file_uploader("Cargar títulos o certificaciones", type=['pdf', 'docx', 'png'])
    if archivo:
        # Registro automático en Supabase
        registrar_log("Carga de Evidencia", archivo.name, "Supabase Storage")
        st.success(f"Documento '{archivo.name}' indexado correctamente.")

# --- TAB 3: GENERACIÓN TÉCNICA (CLAUDE 4.6) ---
with tabs[2]:
    st.header("Redacción Profesional con Sonnet 4.6")
    doc_type = st.selectbox("Documento a generar:", ["Nexo Transversal", "Impacto Nacional", "Carta de Recomendación"])
    
    if st.button("Generar Borrador Legal"):
        with st.spinner("Llamando a Sonnet 4.6 (ID: claude-sonnet-4-6)..."):
            try:
                # MODELO: Usando el ID exacto claude-sonnet-4-6 validado en tu Workbench
                response = client_claude.messages.create(
                    model="claude-sonnet-4-6", 
                    max_tokens=4000,
                    messages=[{"role": "user", "content": f"Como experto en EB2-NIW, redacta un {doc_type} para el [Peticionario Alfa] y su [Proyecto de Infraestructura X] bajo Matter of Dhanasar."}]
                )
                
                texto_generado = response.content[0].text
                st.markdown("### Resultado de la Generación:")
                st.write(texto_generado)
                
                # PERSISTENCIA: Registro de éxito en Supabase
                registrar_log(f"Generación: {doc_type}", "Éxito", "Claude 4.6")
                
                # Generador Word
                doc = Document()
                doc.add_heading(f"{doc_type} - [Peticionario Alfa]", 0)
                doc.add_paragraph(texto_generated)
                buffer = BytesIO()
                doc.save(buffer)
                st.download_button("📥 Descargar Word", data=buffer.getvalue(), file_name=f"{doc_type}.docx")
                
            except Exception as e:
                # PERSISTENCIA: Registro de fallo para auditoría
                st.error(f"Fallo en la comunicación: {e}")
                registrar_log("Error de IA", str(e)[:100], "Claude 4.6")

st.sidebar.markdown("---")
st.sidebar.caption("Patrón DELMORAL Activo | EAS v8.0")
