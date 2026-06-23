import streamlit as st
from datetime import datetime
import json
import os

# --- CONFIGURACIÓN CORPORATIVA PARA CELULARES ---
st.set_page_config(
    page_title="Grupo Alfa - Control de Cobranza", 
    page_icon="🏢", 
    layout="centered"
)

ARCHIVO_DATOS = "clientes.json"

# --- MÓDULO DE PERSISTENCIA DE DATOS ---
def cargar_clientes():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    # Base de datos oficial de la ruta
    return [
        {"nombre": "Guadalupe Torres Arvea", "dia_pago": 11, "reagendado": None, "ya_pago": False},
        {"nombre": "Beatriz Jaquelin Martinez Elias", "dia_pago": 9, "reagendado": None, "ya_pago": False},
        {"nombre": "Uriel Jorge de Gante", "dia_pago": 12, "reagendado": None, "ya_pago": False},
        {"nombre": "Jose Alberto Martinez Nava", "dia_pago": 7, "reagendado": None, "ya_pago": False},
        {"nombre": "Israel Figueroa Sedano", "dia_pago": 13, "reagendado": None, "ya_pago": False},
        {"nombre": "Orlando Santiago Rivera", "dia_pago": 12, "reagendado": None, "ya_pago": False},
        {"nombre": "Isabel Peña Ramirez", "dia_pago": 7, "reagendado": None, "ya_pago": False},
        {"nombre": "Sergio Olivares Vazquez", "dia_pago": 25, "reagendado": None, "ya_pago": False},
        {"nombre": "Dominga Lopez Martinez", "dia_pago": 1, "reagendado": None, "ya_pago": False},
        {"nombre": "Irene Hernandez Lopez", "dia_pago": 6, "reagendado": None, "ya_pago": False},
        {"nombre": "Reyna Juarez Santiago", "dia_pago": 6, "reagendado": None, "ya_pago": False},
        {"nombre": "Odilon Mejia", "dia_pago": 24, "reagendado": None, "ya_pago": False},
        {"nombre": "Rafaela Peña Rebollo", "dia_pago": 3, "reagendado": None, "ya_pago": False},
        {"nombre": "Monica Alvarado Peña", "dia_pago": 3, "reagendado": None, "ya_pago": False},
        {"nombre": "Nereyda Mireya Martinez", "dia_pago": 10, "reagendado": None, "ya_pago": False},
        {"nombre": "Rafael Santos Hernandez", "dia_pago": 26, "reagendado": None, "ya_pago": False},
        {"nombre": "Griselda Olivia Estrada Arella", "dia_pago": 26, "reagendado": None, "ya_pago": False},
        {"nombre": "Ricardo Tiburcio Albino", "dia_pago": 1, "reagendado": None, "ya_pago": False},
        {"nombre": "Jose Angel Marin Dominguez", "dia_pago": 1, "reagendado": None, "ya_pago": False},
        {"nombre": "Cecilia Carreon Solis", "dia_pago": 4, "reagendado": None, "ya_pago": False},
        {"nombre": "Jesus Beristain Garces", "dia_pago": 4, "reagendado": None, "ya_pago": False},
        {"nombre": "Elizabeth Evelia Castellanos Garcia", "dia_pago": 5, "reagendado": None, "ya_pago": False},
        {"nombre": "Esveidy Ruiz Ruiz", "dia_pago": 8, "reagendado": None, "ya_pago": False},
        {"nombre": "Anayeli Juarez Marquez", "dia_pago": 4, "reagendado": None, "ya_pago": False},
        {"nombre": "Juana Gabriela Alvarado Calixto", "dia_pago": 1, "reagendado": None, "ya_pago": False},
        {"nombre": "Yadira Araiza Sandoval", "dia_pago": 7, "reagendado": None, "ya_pago": False},
        {"nombre": "Tomasa Ayala Ramos", "dia_pago": 4, "reagendado": None, "ya_pago": False},
        {"nombre": "Mario Moreno Nicolas", "dia_pago": 7, "reagendado": None, "ya_pago": False},
        {"nombre": "Margarita Gabriel Morales", "dia_pago": 7, "reagendado": None, "ya_pago": False},
        {"nombre": "Leonel Martinez Morales", "dia_pago": 3, "reagendado": None, "ya_pago": False},
        {"nombre": "Mario Aguilar Tapia", "dia_pago": 11, "reagendado": None, "ya_pago": False},
        {"nombre": "Luis Enrique Castro Lopez", "dia_pago": 6, "reagendado": None, "ya_pago": False},
        {"nombre": "Jose Bernardino Lopez Coscati", "dia_pago": 10, "reagendado": None, "ya_pago": False},
        {"nombre": "Jose Alberto Santos Rodriguez", "dia_pago": 10, "reagendado": None, "ya_pago": False},
        {"nombre": "Alberto Hinostroza Hernandez", "dia_pago": 5, "reagendado": None, "ya_pago": False},
        {"nombre": "Jazmin Cadena Guzman", "dia_pago": 2, "reagendado": None, "ya_pago": False},
        {"nombre": "Carmen Zendejas Flores", "dia_pago": 6, "reagendado": None, "ya_pago": False},
        {"nombre": "Veronica Duran Gutierrez", "dia_pago": 23, "reagendado": None, "ya_pago": False},
        {"nombre": "Maria Cecilia Agustin Cruz", "dia_pago": 7, "reagendado": None, "ya_pago": False},
        {"nombre": "Angel Castellanos Garcia", "dia_pago": 7, "reagendado": None, "ya_pago": False}
    ]

def guardar_clientes():
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(st.session_state.clientes, f, ensure_ascii=False, indent=4)

# Inicialización de estado interno
if "clientes" not in st.session_state:
    st.session_state.clientes = cargar_clientes()

# --- MOTOR DE ASIGNACIÓN LOGÍSTICA (SEMÁFORO DE COBRO) ---
def obtener_color_y_estado(dia_actual, dia_pago, reagendado, ya_pago):
    if ya_pago:
        return "oculto", "Ya pagó"
    
    dia_referencia = reagendado if reagendado is not None else dia_pago
    dif = dia_referencia - dia_actual
    
    if 2 <= dif <= 5:
        return "verde", f"🟢 Próximo Vencimiento ({dif} días)"
    elif dif == 1:
        return "azul", "🔵 Programado para Mañana"
    elif -5 <= dif <= 0:
        atraso = abs(dif)
        return "amarillo", f"🟡 Periodo de Tolerancia (Día {atraso})"
    elif -10 <= dif <= -6:
        atraso = abs(dif)
        return "rojo", f"🔴 Cuenta Vencida ({atraso} días de atraso)"
    else:
        return "oculto", "Fuera de rango"

# --- ENTORNO VISUAL CORPORATIVO ---
st.title("🏢 GRUPO ALFA")
st.subheader("Sistema de Gestión y Control de Cobranza")
st.markdown("---")

# MÓDULO DE TIEMPO
dia_actual = st.slider("Seleccionar Día de Operación Actual:", min_value=1, max_value=31, value=datetime.now().day)

# =========================================================
# SECCIÓN 1: BÚSQUEDA Y REGISTRO DE TITULARES
# =========================================================
st.subheader("🔍 Consulta y Registro de Clientes")
nombre_buscar = st.text_input("Buscar cliente por nombre:", placeholder="Escriba para buscar en la base de datos...")

existe_exacto = False

if nombre_buscar.strip():
    texto_limpio = nombre_buscar.strip().lower()
    coincidencias = [(idx, c) for idx, c in enumerate(st.session_state.clientes) if texto_limpio in c["nombre"].lower()]
    
    if coincidencias:
        st.write(f"📂 **Registros coincidentes encontrados:**")
        for idx, registro in coincidencias[:5]:
            if registro["nombre"].lower() == texto_limpio:
                existe_exacto = True
                
            color_s, texto_s = obtener_color_y_estado(dia_actual, registro["dia_pago"], registro["reagendado"], registro["ya_pago"])
            if registro["ya_pago"]:
                texto_s = "✅ Ciclo Mensual Cubierto"
            elif color_s == "oculto":
                texto_s = f"💤 Inactivo en Semáforo (Fecha Base: Día {registro['dia_pago']})"
                
            titulo_tarjeta = f"{texto_s} | {registro['nombre']}"
            if registro['reagendado'] is not None:
                titulo_tarjeta += f" (Reagendado -> Día {registro['reagendado']})"
                
            with st.expander(titulo_tarjeta, expanded=True):
                st.write(f"**Parámetros:** Día de cobro estipulado: {registro['dia_pago']}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("✅ Registrar Pago", key=f"busq_pago_{idx}"):
                        st.session_state.clientes[idx]["ya_pago"] = True
                        guardar_clientes()
                        st.rerun()
                with c2:
                    fecha_b = st.number_input("Nueva Fecha:", min_value=1, max_value=31, value=dia_actual, key=f"busq_num_{idx}")
                    if st.button("📅 Reagendar", key=f"busq_reag_{idx}"):
                        st.session_state.clientes[idx]["reagendado"] = int(fecha_b)
                        st.session_state.clientes[idx]["ya_pago"] = False
                        guardar_clientes()
                        st.rerun()
                with c3:
                    if st.button("❌ Dar de Baja", key=f"busq_elim_{idx}"):
                        st.session_state.clientes.pop(idx)
                        guardar_clientes()
                        st.rerun()
    else:
        st.info("💡 No se encontraron registros con el nombre especificado.")

    if not existe_exacto:
        st.write("---")
        st.write(f"➕ **Alta de Nuevo Cliente:** '{nombre_buscar.strip()}'")
        col_dia, col_btn = st.columns([2, 1])
        with col_dia:
            nuevo_dia = st.number_input("Definir Día de Pago Fijo (1-31):", min_value=1, max_value=31, value=1, key="nuevo_dia_pago")
        with col_btn:
            st.write(" ")
            if st.button("➕ Dar de Alta", use_container_width=True):
                st.session_state.clientes.append({
                    "nombre": nombre_buscar.strip(),
                    "dia_pago": int(nuevo_dia),
                    "reagendado": None,
                    "ya_pago": False
                })
                guardar_clientes()
                st.success("¡Registro añadido exitosamente!")
                st.rerun()

st.write("---")

# =========================================================
# SECCIÓN 2: PANEL DE CONTROL DE RUTA DIARIA
# =========================================================
st.subheader("📌 Clientes con Acciones Requeridas Hoy")

hay_clientes_visibles = False

for i, registro in enumerate(st.session_state.clientes):
    color, texto_estado = obtener_color_y_estado(dia_actual, registro["dia_pago"], registro["reagendado"], registro["ya_pago"])
    
    if color == "oculto":
        continue
        
    hay_clientes_visibles = True
    etiqueta_tarjeta = f"{texto_estado} | {registro['nombre']}"
    if registro['reagendado'] is not None:
        etiqueta_tarjeta += f" (Reagendado para el {registro['reagendado']})"
        
    with st.expander(etiqueta_tarjeta):
        st.write(f"**Detalles:** Día de cobro regular asignado: {registro['dia_pago']}.")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Registrar Pago", key=f"ruta_pago_{i}"):
                registro["ya_pago"] = True
                guardar_clientes()
                st.rerun()
                
        with col2:
            nueva_fecha = st.number_input("Día:", min_value=1, max_value=31, value=dia_actual, key=f"ruta_num_{i}")
            if st.button("📅 Prórroga", key=f"ruta_reag_{i}"):
                registro["reagendado"] = int(nueva_fecha)
                guardar_clientes()
                st.rerun()
                
        with col3:
            if st.button("❌ Eliminar", key=f"ruta_elim_{i}"):
                st.session_state.clientes.pop(i)
                guardar_clientes()
                st.rerun()

if not hay_clientes_visibles:
    st.info("No se registran cuentas pendientes de cobro para el día de operación seleccionado.")

st.write("---")

# =========================================================
# SECCIÓN 3: HERRAMIENTAS DE SEGURIDAD Y RESPALDO
# =========================================================
with st.expander("💾 Seguridad de Datos y Respaldos Corporativos"):
    st.write("Utilice estas herramientas para salvaguardar el estado de la cobranza actual:")
    
    datos_json = json.dumps(st.session_state.clientes, ensure_ascii=False, indent=4)
    st.download_button(
        label="📥 Descargar respaldo de base de datos local",
        data=datos_json,
        file_name="respaldo_grupo_alfa.json",
        mime="application/json",
        use_container_width=True
    )
    
    st.write("---")
    archivo_subido = st.file_uploader("📤 Cargar base de datos desde respaldo anterior:", type=["json"])
    if archivo_subido is not None:
        try:
            datos_restaurados = json.load(archivo_subido)
            if st.button("⚠️ Confirmar Sobreescritura"):
                st.session_state.clientes = datos_restaurados
                guardar_clientes()
                st.success("¡Base de datos restaurada correctamente!")
                st.rerun()
        except:
            st.error("Archivo corrupto o formato no válido.")

st.write(" ")
if st.button("🔄 Cierre Mensual (Reiniciar Estatus de Cuentas)"):
    for registro in st.session_state.clientes:
        registro["ya_pago"] = False
        registro["reagendado"] = None
    guardar_clientes()
    st.success("¡Módulo reiniciado para el inicio del nuevo periodo mensual!")
    st.rerun()
