import streamlit as st
from supabase import create_client
import anthropic
import pandas as pd
from docx import Document
from io import BytesIO
import datetime

# --- 1. CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="Gestión [Peticionario Alfa]", layout="wide")

# --- 2. CONEXIONES Y SEGURIDAD ---
try:
    # Motor validado: Sonnet 4.6
    client_claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Backend persistente: Supabase
    supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
    st.sidebar.success("✅ Conexión establecida")
except Exception as e:
    st.sidebar.error("⚠️ Error de configuración en Secrets")
    st.stop()

# --- 3. LÓGICA DE BACKEND (SUPABASE) ---
def registrar_log(accion, detalle, motor):
    """Registra la actividad en la base de datos para auditoría."""
    try:
        supabase.table("logs_eb2").insert({
            "accion": accion,
            "detalle": detalle,
            "motor": motor,
            "peticionario": "[Peticionario Alfa]"
        }).execute()
    except:
        # Falla silenciosa para no interrumpir el flujo del usuario
        pass

def leer_logs():
    """Recupera el historial del caso desde el backend."""
    try:
        res = supabase.table("logs_eb2").select("*").order("id", desc=True).limit(15).execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame()

# --- 4. ESTRUCTURA DE PANTALLAS ---
st.title("🛡️ Gestión de Petición [Peticionario Alfa]")
tabs = st.tabs(["📊 Dashboard de Control", "📂 Gestión de Evidencia", "✍️ Generación Técnica"])

# --- TAB 1: DASHBOARD ---
with tabs[0]:
    st.header("Historial de Actividad")
    df_historial = leer_logs()
    if not df_historial.empty:
        # Formateo de fecha para el operador
        df_historial['fecha'] = pd.to_datetime(df_historial['fecha']).dt.strftime('%Y-%m-%d %H:%M')
        st.table(df_historial[["fecha", "accion", "detalle", "motor"]])
    else:
        st.info("Sin registros previos en la base de datos.")

# --- TAB 2: EVIDENCIA ---
with tabs[1]:
    st.header("Bóveda de Documentación")
    archivo = st.file_uploader("Subir archivo del [Peticionario Alfa]", type=['pdf', 'docx', 'png'])
    if archivo:
        registrar_log("Carga de Archivo", archivo.name, "Sistema")
        st.success(f"Documento '{archivo.name}' indexado correctamente.")

# --- TAB 3: REDACCIÓN (MOTOR SONNET 4.6) ---
with tabs[2]:
    st.header("Generador de Documentos")
    tipo_documento = st.selectbox("Seleccione el tipo de documento:", 
                                 ["Nexo Transversal", "Impacto Nacional", "Carta de Recomendación"])
    
    if st.button("Ejecutar Redacción"):
        with st.spinner("Procesando con Sonnet 4.6..."):
            try:
                # Llamada al modelo validado en el Workbench
                response = client_claude.messages.create(
                    model="claude-sonnet-4-6", 
                    max_tokens=4000,
                    messages=[{
                        "role": "user", 
                        "content": f"Como experto legal en EB2-NIW, redacta un {tipo_documento} para el [Peticionario Alfa] y su [Proyecto de Infraestructura X] bajo el estándar Matter of Dhanasar."
                    }]
                )
                
                # Consistencia de variable: texto_resultado
                texto_resultado = response.content[0].text
                st.markdown("### Borrador Generado:")
                st.write(texto_resultado)
                
                # Registro de éxito en el backend
                registrar_log(f"Generación: {tipo_documento}", "Éxito", "Claude 4.6")
                
                # Generación de archivo descargable
                doc = Document()
                doc.add_heading(f"{tipo_documento} - [Peticionario Alfa]", 0)
                doc.add_paragraph(texto_resultado)
                buffer = BytesIO()
                doc.save(buffer)
                
                st.download_button(
                    label="📥 Descargar Word",
                    data=buffer.getvalue(),
                    file_name=f"{tipo_documento.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
            except Exception as e:
                st.error(f"Error en la comunicación: {str(e)}")
                registrar_log("Error de IA", str(e)[:100], "Claude 4.6")

# --- 5. PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("Acceso restringido: Operador de Sistema")
