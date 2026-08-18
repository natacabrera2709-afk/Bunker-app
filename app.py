import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Bunker - Gestión Comercial", layout="wide")

st.title("🍔 Bunker - App de Gestión Integral")

# --- 1. BASE DE DATOS Y ESTADO DE LA APP ---
if 'insumos' not in st.session_state:
    st.session_state.insumos = pd.DataFrame([
        {"Insumo": "Medallón de Carne 90g", "Costo Unitario ($)": 1260.82},
        {"Insumo": "Pan de Papa 10cm", "Costo Unitario ($)": 410.00},
        {"Insumo": "Queso Cheddar (feta)", "Costo Unitario ($)": 151.12},
        {"Insumo": "Panceta Ahumada", "Costo Unitario ($)": 282.62},
        {"Insumo": "Papas 150g", "Costo Unitario ($)": 780.00},
        {"Insumo": "Packaging / Aderezos", "Costo Unitario ($)": 1500.00}
    ])

if 'ventas' not in st.session_state:
    st.session_state.ventas = pd.DataFrame(columns=[
        "Fecha", "Producto", "Canal", "Cantidad", "Precio Unitario ($)", 
        "Costo Insumo ($)", "Total Venta ($)", "Total Insumo ($)", "Comisión ($)"
    ])

if 'gastos_fijos' not in st.session_state:
    st.session_state.gastos_fijos = pd.DataFrame([
        {"Concepto": "Alquiler", "Monto ($)": 0.0},
        {"Concepto": "Luz / Gas / Agua", "Monto ($)": 0.0},
        {"Concepto": "Sueldos / Empleados", "Monto ($)": 0.0},
        {"Concepto": "Publicidad / Ads", "Monto ($)": 0.0}
    ])

# Pestañas del Sistema
tab_ventas, tab_historial, tab_insumos, tab_gastos, tab_balance = st.tabs([
    "🛒 Registrar Venta", 
    "📜 Historial de Ventas", 
    "🥩 Carga de Insumos", 
    "💡 Gastos Fijos", 
    "📊 Balance General"
])

# ==========================================
# MÓDULO 1: CARGA DE INSUMOS Y PRECIOS
# ==========================================
with tab_insumos:
    st.header("Modificación y Carga de Insumos Base")
    st.caption("Cambiá los precios acá y se actualizarán automáticamente en los costos de cada combo.")
    st.session_state.insumos = st.data_editor(st.session_state.insumos, num_rows="dynamic", use_container_width=True)

# Cálculo dinámico de costos por producto según la tabla de insumos
def obtener_costo_combo(carne_qty, cheddar_qty, panceta_qty=0):
    ins = st.session_state.insumos.set_index("Insumo")["Costo Unitario ($)"].to_dict()
    c_carne = ins.get("Medallón de Carne 90g", 0) * carne_qty
    c_pan = ins.get("Pan de Papa 10cm", 0)
    c_cheddar = ins.get("Queso Cheddar (feta)", 0) * cheddar_qty
    c_panceta = ins.get("Panceta Ahumada", 0) * panceta_qty
    c_papas = ins.get("Papas 150g", 0)
    c_pack = ins.get("Packaging / Aderezos", 0)
    return c_carne + c_pan + c_cheddar + c_panceta + c_papas + c_pack

# Carta de productos de Bunker
combos_config = {
    "Combo Bunker Simple": {"carne": 1, "cheddar": 2, "panceta": 0, "p_wa": 13100.0, "p_pya": 18714.29},
    "Combo Bunker Doble": {"carne": 2, "cheddar": 4, "panceta": 0, "p_wa": 17800.0, "p_pya": 25428.57},
    "Combo Bunker Triple": {"carne": 3, "cheddar": 6, "panceta": 0, "p_wa": 22500.0, "p_pya": 32142.86},
    "Combo Extremo Simple": {"carne": 1, "cheddar": 2, "panceta": 2, "p_wa": 15900.0, "p_pya": 22714.29},
    "Combo Extremo Doble": {"carne": 2, "cheddar": 4, "panceta": 2, "p_wa": 20600.0, "p_pya": 29428.57},
    "Combo Provo Burguer Doble": {"carne": 2, "cheddar": 4, "panceta": 2, "p_wa": 19500.0, "p_pya": 27857.14},
    "Combo Provo Burguer Cuádruple": {"carne": 4, "cheddar": 8, "panceta": 2, "p_wa": 28900.0, "p_pya": 41285.71},
}

# ==========================================
# MÓDULO 2: REGISTRAR VENTAS
# ==========================================
with tab_ventas:
    st.header("Cargar Pedido de Hamburguesas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        prod_sel = st.selectbox("Producto / Combo", list(combos_config.keys()))
    with col2:
        canal_sel = st.radio("Canal de Venta", ["WhatsApp", "PedidosYa"])
    with col3:
        cant_sel = st.number_input("Cantidad Vendida", min_value=1, value=1)

    cfg = combos_config[prod_sel]
    costo_u = obtener_costo_combo(cfg["carne"], cfg["cheddar"], cfg["panceta"])
    precio_u = cfg["p_wa"] if canal_sel == "WhatsApp" else cfg["p_pya"]
    comision_u = 0.0 if canal_sel == "WhatsApp" else precio_u * 0.30

    st.warning(f"📌 **Resumen:** Costo Insumo Unitario: **${costo_u:,.2f}** | Precio Venta Unitario: **${precio_u:,.2f}**")

    if st.button("🛒 Marcar Venta y Guardar en Historial", use_container_width=True):
        nueva_venta = {
            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Producto": prod_sel,
            "Canal": canal_sel,
            "Cantidad": cant_sel,
            "Precio Unitario ($)": precio_u,
            "Costo Insumo ($)": costo_u,
            "Total Venta ($)": precio_u * cant_sel,
            "Total Insumo ($)": costo_u * cant_sel,
            "Comisión ($)": comision_u * cant_sel
        }
        st.session_state.ventas = pd.concat([st.session_state.ventas, pd.DataFrame([nueva_venta])], ignore_index=True)
        st.success(f"¡Venta de {cant_sel}x {prod_sel} registrada exitosamente!")

# ==========================================
# MÓDULO 3: HISTORIAL DE VENTAS
# ==========================================
with tab_historial:
    st.header("Historial Completo de Ventas")
    if st.session_state.ventas.empty:
        st.info("Todavía no registraste ninguna venta.")
    else:
        st.dataframe(st.session_state.ventas, use_container_width=True)

# ==========================================
# MÓDULO 4: GASTOS FIJOS
# ==========================================
with tab_gastos:
    st.header("Registro de Gastos Fijos (Mensuales)")
    st.session_state.gastos_fijos = st.data_editor(st.session_state.gastos_fijos, num_rows="dynamic", use_container_width=True)

# ==========================================
# MÓDULO 5: BALANCE FINANCIERO GENERAL
# ==========================================
with tab_balance:
    st.header("Estado de Resultados y Ganancias")
    
    tot_v = st.session_state.ventas["Total Venta ($)"].sum() if not st.session_state.ventas.empty else 0.0
    tot_i = st.session_state.ventas["Total Insumo ($)"].sum() if not st.session_state.ventas.empty else 0.0
    tot_c = st.session_state.ventas["Comisión ($)"].sum() if not st.session_state.ventas.empty else 0.0
    tot_gf = st.session_state.gastos_fijos["Monto ($)"].sum()
    
    ganancia_neta = tot_v - tot_i - tot_c - tot_gf

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Ventas Totales Brutas", f"${tot_v:,.2f}")
    m2.metric("Total Gastos en Insumos", f"${tot_i:,.2f}")
    m3.metric("Comisiones PedidosYa", f"${tot_c:,.2f}")
    m4.metric("Total Gastos Fijos", f"${tot_gf:,.2f}")

    st.divider()
    if ganancia_neta >= 0:
        st.success(f"### 💵 Ganancia Neta Real: ${ganancia_neta:,.2f}")
    else:
        st.error(f"### ⚠️ Pérdida / Deficit: ${ganancia_neta:,.2f}")
