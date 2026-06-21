import streamlit as st
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA PARA CELULARES
st.set_page_config(page_title="Agenda de Cobro V4", page_icon="📅", layout="centered")

# 1. INICIALIZAR LA BASE DE DATOS EN LA MEMORIA DE LA APP
if "clientes" not in st.session_state:
    st.session_state.clientes = [
        {"nombre": "Carlos Mendoza", "dia_pago": 8, "reagendado": None, "ya_pago": False},
        {"nombre": "Ana Gómez", "dia_pago": 15, "reagendado": None, "ya_pago": False},
        {"nombre": "Carlos Pérez", "dia_pago": 20, "reagendado": None, "ya_pago": False}
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
st.title("📅 Agenda Semáforo Inteligente")

# SIMULADOR DE DÍA
dia_actual = st.slider("Simular Día de Hoy del Mes:", min_value=1, max_value=31, value=datetime.now().day)

# =========================================================
# 3. SECCIÓN DE BÚSQUEDA Y REGISTRO DINÁMICO
# =========================================================
st.subheader("🔍 Buscar o Registrar Cliente")
nombre_buscar = st.text_input("Escribe el nombre del cliente:", placeholder="Empieza a escribir...")

existe_exacto = False

if nombre_buscar.strip():
    texto_limpio = nombre_buscar.strip().lower()
    
    # Filtrar coincidencias de toda la lista (estén ocultos o no)
    coincidencias = [(idx, c) for idx, c in enumerate(st.session_state.clientes) if texto_limpio in c["nombre"].lower()]
    
    if coincidencias:
        st.write(f"📂 **Coincidencias encontradas (Mostrando hasta 5):**")
        # Limitamos a un máximo de 5 como me pediste
        for idx, registro in coincidencias[:5]:
            if registro["nombre"].lower() == texto_limpio:
                existe_exacto = True
                
            # Calculamos su estado actual para mostrarlo en la tarjeta de búsqueda
            color_s, texto_s = obtener_color_y_estado(dia_actual, registro["dia_pago"], registro["reagendado"], registro["ya_pago"])
            if registro["ya_pago"]:
                texto_s = "✅ Ya pagó este mes"
            elif color_s == "oculto":
                texto_s = f"💤 Fuera de semáforo (Pago: Día {registro['dia_pago']})"
                
            # Tarjeta idéntica a la del semáforo principal
            titulo_tarjeta = f"{texto_s} | {registro['nombre']}"
            if registro['reagendado'] is not None:
                titulo_tarjeta += f" (Reagendado -> {registro['reagendado']})"
                
            with st.expander(titulo_tarjeta, expanded=True):
                st.write(f"**Configuración:** Día de pago fijo: {registro['dia_pago']}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("✅ Ya pagó", key=f"busq_pago_{idx}"):
                        st.session_state.clientes[idx]["ya_pago"] = True
                        st.rerun()
                with c2:
                    fecha_b = st.number_input("Día:", min_value=1, max_value=31, value=dia_actual, key=f"busq_num_{idx}")
                    if st.button("📅 Agendar", key=f"busq_reag_{idx}"):
                        st.session_state.clientes[idx]["reagendado"] = int(fecha_b)
                        st.session_state.clientes[idx]["ya_pago"] = False  # Por si ya había pagado y lo quieres reactivar
                        st.rerun()
                with c3:
                    if st.button("❌ Eliminar", key=f"busq_elim_{idx}"):
                        st.session_state.clientes.pop(idx)
                        st.rerun()
    else:
        st.info("💡 No hay ningún cliente con ese nombre.")

    # Sección automática para agregar si no hay coincidencia exacta
    if not existe_exacto:
        st.write("---")
        st.write(f"➕ **Registrar como nuevo cliente:** '{nombre_buscar.strip()}'")
        col_dia, col_btn = st.columns([2, 1])
        with col_dia:
            nuevo_dia = st.number_input("Asignar Día de Pago Fijo (1-31):", min_value=1, max_value=31, value=1, key="nuevo_dia_pago")
        with col_btn:
            st.write(" ") # Espacio estético
            if st.button("➕ Guardar", use_container_width=True):
                st.session_state.clientes.append({
                    "nombre": nombre_buscar.strip(),
                    "dia_pago": int(nuevo_dia),
                    "reagendado": None,
                    "ya_pago": False
                })
                st.success("¡Agregado!")
                st.rerun()

st.write("---")

# =========================================================
# 4. DESPLIEGUE DEL SEMÁFORO PRINCIPAL (RUTA DEL DÍA)
# =========================================================
st.subheader("📌 Clientes Activos en el Semáforo")

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
            if st.button("✅ Ya pagó", key=f"ruta_pago_{i}"):
                registro["ya_pago"] = True
                st.rerun()
                
        with col2:
            nueva_fecha = st.number_input(
                "Día:", 
                min_value=1, 
                max_value=31, 
                value=dia_actual, 
                key=f"ruta_num_{i}"
            )
            if st.button("📅 Reagendar", key=f"ruta_reag_{i}"):
                registro["reagendado"] = int(nueva_fecha)
                st.rerun()
                
        with col3:
            if st.button("❌ Eliminar", key=f"ruta_elim_{i}"):
                st.session_state.clientes.pop(i)
                st.rerun()

if not hay_clientes_visibles:
    st.info("No hay clientes programados para cobro en el día simulado de hoy.")

st.write("---")
# Botón de reinicio mensual
if st.button("🔄 Reiniciar Mes (Borra pagos y agendas temporales)"):
    for registro in st.session_state.clientes:
        registro["ya_pago"] = False
        registro["reagendado"] = None
    st.success("¡Todo listo para el nuevo ciclo mensual!")
    st.rerun()
