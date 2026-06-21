import streamlit as st
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA PARA CELULARES
st.set_page_config(page_title="Agenda de Cobro V2", page_icon="📅", layout="centered")

# 1. INICIALIZAR LA BASE DE DATOS EN LA MEMORIA DE LA APP
if "clientes" not in st.session_state:
    st.session_state.clientes = [
        {"nombre": "Carlos Mendoza", "dia_pago": 8, "reagendado": None, "ya_pago": False},
        {"nombre": "Ana Gómez", "dia_pago": 15, "reagendado": None, "ya_pago": False}
    ]

# 2. MOTOR DE LOGÍSICA DEL SEMÁFORO
def obtener_color_y_estado(dia_actual, dia_pago, reagendado, ya_pago):
    if ya_pago:
        return "oculto", "Ya pagó"
    
    dia_referencia = reagendado if reagendado is not None else dia_pago
    dif = dia_referencia - dia_actual
    
    if 2 <= dif <= 5:
        return "verde", f"🟢 Falta poco ({dif} días)"
    elif dif == 1:
        return "azul", "🔵 Paga mañana"
    elif -5 <= dif <= 0:
        atraso = abs(dif)
        return "amarillo", f"🟡 Día de pago / Tolerancia (Día {atraso})"
    elif -10 <= dif <= -6:
        atraso = abs(dif)
        return "rojo", f"🔴 Vencido (Atraso de {atraso} días)"
    else:
        return "oculto", "Fuera de rango"

# --- INTERFAZ VISUAL ---
st.title("📅 Agenda Semáforo V2")

# SIMULADOR DE DÍA (Para hacer pruebas)
dia_actual = st.slider("Simular Día de Hoy del Mes:", min_value=1, max_value=31, value=datetime.now().day)

# 3. FORMULARIO PARA AGREGAR NUEVOS CLIENTES (CON DETECTOR DE DUPLICADOS)
with st.expander("➕ Agregar Nuevo Cliente", expanded=False):
    with st.form("nuevo_cliente_form", clear_on_submit=True):
        nuevo_nombre = st.text_input("Nombre del Cliente:")
        
        # Alerta en tiempo real mientras el usuario escribe
        if nuevo_nombre.strip():
            coincidencias = [c["nombre"] for c in st.session_state.clientes if nuevo_nombre.lower().strip() in c["nombre"].lower()]
            if coincidencias:
                st.warning(f"⚠️ Posibles duplicados: {', '.join(coincidencias)}")
                
        nuevo_dia = st.number_input("Día de Pago Fijo (1-31):", min_value=1, max_value=31, value=1)
        boton_guardar = st.form_submit_button("Guardar Cliente")
        
        if boton_guardar and nuevo_nombre:
            nombre_limpio = nuevo_nombre.strip()
            # Validación estricta para no duplicar exactamente el mismo nombre
            existe_exacto = any(c["nombre"].lower() == nombre_limpio.lower() for c in st.session_state.clientes)
            
            if existe_exacto:
                st.error(f"❌ El cliente '{nombre_limpio}' ya existe en la lista. No se agregó de nuevo.")
            else:
                nuevo_cliente = {
                    "nombre": nombre_limpio,
                    "dia_pago": int(nuevo_dia),
                    "reagendado": None,
                    "ya_pago": False
                }
                st.session_state.clientes.append(nuevo_cliente)
                st.success(f"¡{nombre_limpio} agregado con éxito!")
                st.rerun()

st.write("---")

# 4. DESPLIEGUE DEL SEMÁFORO DE CLIENTES
st.subheader("Clientes Activos en Ruta")

hay_clientes_visibles = False

# Recorremos la lista usando el índice para poder eliminar correctamente
for i, registro in enumerate(st.session_state.clientes):
    color, texto_estado = obtener_color_y_estado(
        dia_actual, 
        registro["dia_pago"], 
        registro["reagendado"], 
        registro["ya_pago"]
    )
    
    if color == "oculto":
        continue
        
    hay_clientes_visibles = True
    
    etiqueta_tarjeta = f"{texto_estado} | {registro['nombre']}"
    if registro['reagendado'] is not None:
        etiqueta_tarjeta += f" (Reagendado para el {registro['reagendado']})"
        
    with st.expander(etiqueta_tarjeta):
        st.write(f"**Día de cobro original:** Día {registro['dia_pago']} de cada mes.")
        
        # Agregamos tres columnas para los botones de acción rápidos en el celular
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Ya pagó", key=f"pago_{registro['nombre']}_{i}"):
                registro["ya_pago"] = True
                st.success("Marcado como pagado.")
                st.rerun()
                
        with col2:
            nueva_fecha = st.number_input(
                "Día:", 
                min_value=1, 
                max_value=31, 
                value=dia_actual, 
                key=f"input_{registro['nombre']}_{i}"
            )
            if st.button("📅 Reagendar", key=f"reagendar_{registro['nombre']}_{i}"):
                registro["reagendado"] = int(nueva_fecha)
                st.info(f"Reagendado para el {nueva_fecha}")
                st.rerun()
                
        with col3:
            # NUEVO BOTÓN PARA ELIMINAR EL CLIENTE DEFINITIVAMENTE
            if st.button("❌ Eliminar", key=f"eliminar_{registro['nombre']}_{i}"):
                st.session_state.clientes.pop(i)
                st.error(f"Cliente eliminado.")
                st.rerun()

if not hay_clientes_visibles:
    st.info("No hay clientes programados para cobro en el día simulado de hoy.")

# Botón al final de la pantalla para reiniciar el mes
if st.button("🔄 Reiniciar Mes (Borra pagos y agendas temporales)"):
    for registro in st.session_state.clientes:
        registro["ya_pago"] = False
        registro["reagendado"] = None
    st.success("¡Todo listo para el nuevo ciclo mensual!")
    st.rerun()
