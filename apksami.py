import streamlit as st
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA PARA CELULARES
st.set_page_config(page_title="Agenda de Cobro V3", page_icon="📅", layout="centered")

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
st.title("📅 Agenda Semáforo V3")

# SIMULADOR DE DÍA (Para hacer pruebas en ruta)
dia_actual = st.slider("Simular Día de Hoy del Mes:", min_value=1, max_value=31, value=datetime.now().day)

# 3. SECCIÓN SE BUSCADOR Y REGISTRO DINÁMICO
with st.expander("🔍 Buscar o Agregar Cliente", expanded=False):
    nuevo_nombre = st.text_input("Escribe el nombre del cliente:")
    
    existe_exacto = False
    
    # Si el usuario empieza a escribir, el buscador se activa en tiempo real
    if nuevo_nombre.strip():
        nombre_buscado = nuevo_nombre.strip().lower()
        # Buscamos coincidencias en la base de datos actual
        coincidencias = [(idx, c) for idx, c in enumerate(st.session_state.clientes) if nombre_buscado in c["nombre"].lower()]
        
        if coincidencias:
            st.write("### 📂 Contactos detectados en el sistema:")
            for idx, registro in coincidencias:
                if registro["nombre"].lower() == nombre_buscado:
                    existe_exacto = True
                
                # Calculamos su estado aunque esté oculto en la pantalla principal
                color_b, texto_b = obtener_color_y_estado(
                    dia_actual, registro["dia_pago"], registro["reagendado"], registro["ya_pago"]
                )
                
                info_estado = texto_b if color_b != "oculto" else "🚫 Oculto (Fuera de rango o ya pagó)"
                
                # Desplegamos la tarjeta del cliente encontrado dentro del buscador
                st.warning(f"**{registro['nombre']}** | Estado: {info_estado} | Día fijo: {registro['dia_pago']}")
                
                # Botones de acción directa para solucionar el problema rápido
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("✅ Ya pagó", key=f"b_pago_{idx}"):
                        st.session_state.clientes[idx]["ya_pago"] = True
                        st.success("Marcado como pagado.")
                        st.rerun()
                with c2:
                    nueva_fecha_b = st.number_input(
                        "Traer a fecha:", min_value=1, max_value=31, value=dia_actual, key=f"b_in_{idx}"
                    )
                    if st.button("📅 Agendar Hoy", key=f"b_reag_{idx}"):
                        # Lo movemos a la fecha deseada y nos aseguramos de activar su estatus por si ya había pagado
                        st.session_state.clientes[idx]["reagendado"] = int(nueva_fecha_b)
                        st.session_state.clientes[idx]["ya_pago"] = False 
                        st.success(f"¡Reagendado para el día {nueva_fecha_b}! Ya aparecerá en el semáforo.")
                        st.rerun()
                with c3:
                    if st.button("❌ Eliminar Duplicado", key=f"b_elim_{idx}"):
                        st.session_state.clientes.pop(idx)
                        st.error("Cliente eliminado de la lista.")
                        st.rerun()
            st.write("---")

    # Formulario para registrar un cliente verdaderamente nuevo
    with st.form("guardar_cliente_form", clear_on_submit=True):
        st.write("**¿Es un cliente nuevo? asígnalo aquí:**")
        nuevo_dia = st.number_input("Día de Pago Fijo (1-31):", min_value=1, max_value=31, value=1)
        boton_guardar = st.form_submit_button("Guardar Nuevo Cliente")
        
        if boton_guardar and nuevo_nombre:
            nombre_limpio = nuevo_nombre.strip()
            if existe_exacto:
                st.error(f"❌ El cliente '{nombre_limpio}' ya existe en tu lista. Usa los botones amarillos de arriba para gestionarlo, no lo dupliques.")
            else:
                nuevo_cliente = {
                    "nombre": nombre_limpio,
                    "dia_pago": int(nuevo_dia),
                    "reagendado": None,
                    "ya_pago": False
                }
                st.session_state.clientes.append(nuevo_cliente)
                st.success(f"¡{nombre_limpio} agregado a la lista con éxito!")
                st.rerun()

st.write("---")

# 4. DESPLIEGUE DEL SEMÁFORO DE CLIENTES (PANTALLA PRINCIPAL EN RUTA)
st.subheader("Clientes Activos en Ruta")

hay_clientes_visibles = False

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
            if st.button("❌ Eliminar", key=f"eliminar_{registro['nombre']}_{i}"):
                st.session_state.clientes.pop(i)
                st.error(f"Cliente eliminado.")
                st.rerun()

if not hay_clientes_visibles:
    st.info("No hay clientes programados para cobro en el día simulado de hoy.")

# Botón de reinicio mensual
if st.button("🔄 Reiniciar Mes (Borra pagos y agendas temporales)"):
    for registro in st.session_state.clientes:
        registro["ya_pago"] = False
        registro["reagendado"] = None
    st.success("¡Todo listo para el nuevo ciclo mensual!")
    st.rerun()
