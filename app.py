import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Bunker App", page_icon="🍔", layout="wide")

# Estilos visuales
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 800; color: #1E1E1E; text-align: center; }
    .sub-header { font-size: 1rem; color: #E63946; text-align: center; font-weight: 600; margin-bottom: 2rem; }
    .stButton>button { width: 100%; background-color: #E63946; color: white; font-weight: bold; border-radius: 8px; height: 3em; border: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🍔 BUNKER APP</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>CONTROL DE VENTAS, COSTOS Y CANALES</div>", unsafe_allow_html=True)

tabs = st.tabs(["⚡ Despacho Rápido", "🧮 Calculadora de Combos", "📊 Balance & Caja", "⚙️ Gastos Fijos"])

if 'ventas' not in st.session_state:
    st.session_state.ventas = []

if 'combos' not in st.session_state:
    st.session_state.combos = {
        "Simple Bunker": {"costo_insumos": 2100, "markup_wa": 3.0, "comision_peya": 0.30},
        "Doble Bunker": {"costo_insumos": 3200, "markup_wa": 3.0, "comision_peya": 0.30},
        "Triple Bunker": {"costo_insumos": 4366, "markup_wa": 3.0, "comision_peya": 0.30},
        "Combo Extremo": {"costo_insumos": 4800, "markup_wa": 3.0, "comision_peya": 0.30},
    }

if 'gastos_fijos' not in st.session_state:
    st.session_state.gastos_fijos = {"Alquiler": 250000, "Luz / Gas": 80000, "Monotributo": 30000}

# 1. Despacho
with tabs[0]:
    st.subheader("Cargar Venta")
    combo_sel = st.selectbox("Combo", list(st.session_state.combos.keys()))
    canal = st.radio("Canal", ["WhatsApp / Local", "PedidosYa"], horizontal=True)
    cantidad = st.number_input("Cantidad", min_value=1, value=1)
    
    info = st.session_state.combos[combo_sel]
    costo_unit = info["costo_insumos"]
    
    if "WhatsApp" in canal:
        precio_unit = costo_unit * info["markup_wa"]
        comision_unit = 0
    else:
        precio_base = costo_unit * info["markup_wa"]
        precio_unit = precio_base / (1 - info["comision_peya"])
        comision_unit = precio_unit * info["comision_peya"]
        
    precio_total = precio_unit * cantidad
    costo_total = costo_unit * cantidad
    comision_total = comision_unit * cantidad
    ganancia = precio_total - costo_total - comision_total

    st.info(f"💰 **Total:** ${precio_total:,.2f} | **Ganancia Directa:** ${ganancia:,.2f}")
    
    if st.button("🚀 REGISTRAR VENTA"):
        st.session_state.ventas.append({
            "Fecha": datetime.datetime.now().strftime("%H:%M:%S"),
            "Combo": combo_sel,
            "Canal": canal,
            "Cantidad": cantidad,
            "Total": precio_total,
            "Ganancia": ganancia
        })
        st.success("¡Venta registrada!")

# 2. Calculadora
with tabs[1]:
    st.subheader("Combos y Precios")
    for c_nombre, c_data in st.session_state.combos.items():
        p_wa = c_data["costo_insumos"] * c_data["markup_wa"]
        p_peya = p_wa / (1 - c_data["comision_peya"])
        st.write(f"**{c_nombre}** | Costo: ${c_data['costo_insumos']} | WA: ${p_wa:,.2f} | PeYa: ${p_peya:,.2f}")

# 3. Balance
with tabs[2]:
    st.subheader("Balance del Día")
    if st.session_state.ventas:
        df = pd.DataFrame(st.session_state.ventas)
        st.dataframe(df)
        st.metric("Total Ventas", f"${df['Total'].sum():,.2f}")
        st.metric("Ganancia acumulada", f"${df['Ganancia'].sum():,.2f}")
    else:
        st.write("Sin ventas registradas hoy.")

# 4. Gastos
with tabs[3]:
    st.subheader("Gastos Fijos")
    st.json(st.session_state.gastos_fijos)
