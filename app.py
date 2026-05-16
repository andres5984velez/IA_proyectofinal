import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA (Minimalista y limpia)
st.set_page_config(page_title="ClearPath", page_icon="🎯", layout="centered")

# CSS Personalizado para ocultar menús por defecto de Streamlit y dar estilo "Startup"
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .tarea-destacada {
        background-color: #1E293B; /* Azul oscuro elegante */
        border-left: 5px solid #38BDF8; /* Borde neón */
        padding: 30px;
        border-radius: 10px;
        font-size: 24px;
        color: #F8FAFC;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO DE LA APP
st.title("🎯 ClearPath")
st.markdown("### El fin de la parálisis por análisis.")
st.markdown("Dinos cuál es tu gran proyecto. Nosotros te daremos **solo una tarea** para hoy.")

# 3. CONEXIÓN SEGURA CON LA IA
# Streamlit leerá la API Key desde su configuración de seguridad secreta
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.warning("⚠️ La API de IA no está conectada aún. Por favor, configura los Secrets en Streamlit.")

# Estado temporal para guardar la tarea generada en la pantalla
if 'tarea_generada' not in st.session_state:
    st.session_state.tarea_generada = ""

# 4. PANTALLA DE INGRESO
proyecto_usuario = st.text_area(
    "¿Cuál es tu proyecto y para cuándo lo necesitas?", 
    placeholder="Ej: Tengo que entregar una tesis de 50 páginas en 3 meses..."
)

# 5. BOTÓN DE ACCIÓN
if st.button("🚀 Despejar el camino", type="primary", use_container_width=True):
    if proyecto_usuario:
        # Animación de carga para que el usuario sienta que el sistema está trabajando
        with st.spinner('Calculando ruta óptima para proteger tu energía mental...'):
            try:
                # El "Prompt" estricto que obliga a la IA a dar UNA sola respuesta
                prompt_sistema = f"""
                Eres ClearPath, un sistema experto diseñado para curar la sobrecarga cognitiva. 
                El usuario tiene el siguiente gran proyecto: '{proyecto_usuario}'.
                Tu única función es decirle la PRIMERA, ÚNICA Y MÁS PEQUEÑA tarea accionable que debe hacer HOY para empezar o avanzar.
                REGLAS ESTRICTAS:
                - Cero saludos ni despedidas.
                - Cero viñetas, viñetas de lista o explicaciones largas.
                - Redacta UNA sola instrucción clara, directa y corta.
                - Ejemplo válido: "Hoy: Busca 3 artículos académicos sobre la historia de tu tema y descarga los PDFs."
                """
                # Llamada a la IA
                respuesta = modelo.generate_content(prompt_sistema)
                st.session_state.tarea_generada = respuesta.text
                
            except Exception as e:
                st.error(f"Hubo un error al generar la ruta. Detalles exactos: {e}")
    else:
        st.info("Por favor, escribe tu proyecto arriba para poder ayudarte.")

# 6. PANTALLA DE FOCO DIARIO (Solo aparece cuando la IA responde)
if st.session_state.tarea_generada:
    # Muestra la tarea en el cuadro de diseño personalizado
    st.markdown(f"<div class='tarea-destacada'>{st.session_state.tarea_generada}</div>", unsafe_allow_html=True)
    
    # Botón para cerrar el ciclo
    if st.button("✅ Completado por hoy", use_container_width=True):
        st.balloons() # Animación de celebración nativa de Streamlit
        st.success("¡Excelente trabajo! Has protegido tu energía mental. Vuelve mañana para tu siguiente instrucción.")
        st.session_state.tarea_generada = "" # Borra la tarea para reiniciar