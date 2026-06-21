import streamlit as st
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA PARA CELULARES
st.set_page_config(page_title="Agenda de Cobro", page_icon="📅", layout="centered")

# 1. INICIALIZAR LA BASE DE DATOS EN LA MEMORIA DE LA APP
# Si es la primera vez que se abre, creamos una lista con un par de ejemplos
if "clientes" not in st.session_state:
    st.session_state.clientes = [
        {"nombre": "Carlos Mendoza", "dia_pago": 8, "reagendado": None, "ya_pago": False},
        {"nombre": "Ana Gómez", "dia_pago": 15, "reagendado": None, "ya_pago": False}
    ]

# 2. MOTOR DE LOGÍSICA DEL SEMÁFORO
def obtener_color_y_estado(dia_actual, dia_pago, reagendado, ya_pago):
    if ya_pago:
        return "oculto", "Ya pagó"
    
    # Si se reagendó, tomamos esa fecha para el cálculo de este mes
    dia_referencia = reagendado if reagendado is not None else dia_pago
    
    # Calculamos la diferencia de días
    dif = dia_referencia - dia_actual
    
    if 2 <= dif <= 5:
        return "verde", f"🟢 Falta poco ({dif} días)"
    elif dif == 1:
        return "azul", "🔵 Paga mañana"
    elif -5 <= dif <= 0:
        # 0 es el día de pago, hasta -5 son los 5 días de tolerancia
        atraso = abs(dif)
        return "amarillo", f"🟡 Día de pago / Tolerancia (Día {atraso})"
    elif -10 <= dif <= -6:
        # De 6 a 10 días de diferencia real significa que pasaron los 5 de tolerancia
        atraso = abs(dif)
        return "rojo", f"🔴 Vencido (Atraso de {atraso} días)"
    else:
        return "oculto", "Fuera de rango"

# --- INTERFAZ VISUAL ---
st.title("📅 Agenda Semáforo")

# SIMULADOR DE DÍA (Muy útil para hacer pruebas)
dia_actual = st.slider("Simular Día de Hoy del Mes:", min_value=1, max_value=31, value=datetime.now().day)

# 3. FORMULARIO PARA AGREGAR NUEVOS CLIENTES
with st.expander("➕ Agregar Nuevo Cliente", expanded=False):
    with st.form("nuevo_cliente_form", clear_on_submit=True):
        nuevo_nombre = st.text_input("Nombre del Cliente:")
        nuevo_dia = st.number_input("Día de Pago Fijo (1-31):", min_value=1, max_value=31, value=1)
        boton_guardar = st.form_submit_button("Guardar Cliente")
        
        if boton_guardar and nuevo_nombre:
            nuevo_cliente = {
                "nombre": nuevo_nombre,
                "dia_pago": int(nuevo_dia),
                "reagendado": None,
                "ya_pago": False
            }
            st.session_state.clientes.append(nuevo_cliente)
            st.success(f"¡{nuevo_nombre} agregado con éxito!")
            st.rerun()

st.write("---")

# 4. DESPLIEGUE DEL SEMÁFORO DE CLIENTES
st.subheader("Clientes Activos en Ruta")

hay_clientes_visibles = False

# Recorremos la lista de clientes para calcular su estado y dibujarlos
for registro in st.session_state.clientes:
    color, texto_estado = obtener_color_y_estado(
        dia_actual, 
        registro["dia_pago"], 
        registro["reagendado"], 
        registro["ya_pago"]
    )
    
    # Si el estado es oculto, el código se salta al cliente y no muestra nada
    if color == "oculto":
        continue
        
    hay_clientes_visibles = True
    
    # Diseñamos la tarjeta del cliente usando un bloque expandible interactivo
    etiqueta_tarjeta = f"{texto_estado} | {registro['nombre']}"
    if registro['reagendado'] is not None:
        etiqueta_tarjeta += f" (Reagendado para el {registro['reagendado']})"
        
    with st.expander(etiqueta_tarjeta):
        st.write(f"**Día de cobro original:** Día {registro['dia_pago']} de cada mes.")
        
        # Columnas para los botones de acción rápidos para el teléfono
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Ya pagó", key=f"pago_{registro['nombre']}"):
                registro["ya_pago"] = True
                st.success("Registrado. Desaparecerá del semáforo.")
                st.rerun()
                
        with col2:
            # Entrada para asignar una nueva fecha solo para este ciclo
            nueva_fecha = st.number_input(
                "Nueva fecha de pago:", 
                min_value=1, 
                max_value=31, 
                value=dia_actual, 
                key=f"input_{registro['nombre']}"
            )
            if st.button("📅 Reagendar", key=f"reagendar_{registro['nombre']}"):
                registro["reagendado"] = int(nueva_fecha)
                st.info(f"Reagendado para el día {nueva_fecha}")
                st.rerun()

if not hay_clientes_visibles:
    st.info("No hay clientes programados para cobro en el día simulado de hoy.")

# Botón al final de la pantalla para reiniciar el mes cuando sea necesario
if st.button("🔄 Reiniciar Mes (Borra pagos y agendas temporales)"):
    for registro in st.session_state.clientes:
        registro["ya_pago"] = False
        registro["reagendado"] = None
    st.success("¡Todo listo para el nuevo ciclo mensual!")
    st.rerun()
