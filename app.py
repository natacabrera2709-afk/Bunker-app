import streamlit as st
import pandas as pd
import datetime

# Configuración de página
st.set_page_config(page_title="Bunker - Control de Ventas", page_icon="🍔", layout="centered")

# Estilos personalizados
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #E63946; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1rem; color: #8D99AE; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; background-color: #E63946; color: white; border-radius: 8px; font-weight: bold; height: 3em; }
    .metric-card { background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Título Principal
st.markdown("<div class='main-header'>🍔 BUNKER</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>CONTROL DE VENTAS Y COSTOS</div>", unsafe_allow_html=True)

# Base de datos local de Combos (Precios y Costos para ganancia exacta)
COMBOS = {
    "Simple Bunker": {"precio": 6300, "costo": 2100},
    "Doble Bunker": {"precio": 8200, "costo": 2800},
    "Triple Bunker": {"precio": 9900, "costo": 3500},
    "Combo Extremo": {"precio": 12500, "costo": 4200}
}

# Inicializar historial de ventas en la sesión
if 'ventas' not in st.session_state:
    st.session_state.ventas = []

# Solapas principales
tab1, tab2, tab3 = st.tabs(["⚡ Despacho Rápido", "🧮 Calculadora", "📊 Resumen diario"])

# --- TAB 1: DESPACHO RÁPIDO ---
with tab1:
    st.subheader("Cargar Venta")
    combo_sel = st.selectbox("Combo", list(COMBOS.keys()))
    cantidad = st.number_input("Cantidad", min_value=1, value=1, step=1)
    metodo_pago = st.radio("Método de pago", ["Efectivo", "Transferencia / QR"], horizontal=True)
    
    precio_unitario = COMBOS[combo_sel]["precio"]
    costo_unitario = COMBOS[combo_sel]["costo"]
    
    total_venta = precio_unitario * cantidad
    total_ganancia = (precio_unitario - costo_unitario) * cantidad

    st.info(f"💰 **Total:** ${total_venta:,.2f}  |  **Ganancia:** ${total_ganancia:,.2f}")

    if st.button("🚀 REGISTRAR VENTA"):
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.ventas.append({
            "Hora": hora_actual,
            "Producto": combo_sel,
            "Cantidad": cantidad,
            "Pago": metodo_pago,
            "Total": total_venta,
            "Ganancia": total_ganancia
        })
        st.success(f"¡Venta de {combo_sel} registrada con éxito!")

# --- TAB 2: CALCULADORA ---
with tab2:
    st.subheader("Calculadora Personalizada")
    precio_custom = st.number_input("Precio de Venta ($)", min_value=0, value=5000, step=100)
    costo_custom = st.number_input("Costo de Insumos ($)", min_value=0, value=2000, step=100)
    cant_custom = st.number_input("Cantidad de unidades", min_value=1, value=1, step=1)

    ganancia_custom = (precio_custom - costo_custom) * cant_custom
    
    st.metric("Ganancia Total Estimada", f"${ganancia_custom:,.2f}")

# --- TAB 3: RESUMEN DIARIO ---
with tab3:
    st.subheader("Resumen de la Jornada")
    if st.session_state.ventas:
        df = pd.DataFrame(st.session_state.ventas)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Recaudado", f"${df['Total'].sum():,.2f}")
        with col2:
            st.metric("Ganancia Limpia", f"${df['Ganancia'].sum():,.2f}")

        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Limpiar historial del día"):
            st.session_state.ventas = []
            st.experimental_rerun()
    else:
        st.write("Aún no se registraron ventas hoy.")
