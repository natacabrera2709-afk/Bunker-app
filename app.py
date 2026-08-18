import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Bunker - Gestión de Costos", layout="wide")

st.title("🍔 Bunker - Control de Costos y Precios")
st.caption("Modificá los precios base en la barra lateral para recalcular todo el menú al instante.")

# ==========================================
# 1. MATRIZ DE INSUMOS BASE (Sidebar)
# ==========================================
st.sidebar.header("⚙️ Precios Base de Insumos")

precio_carne = st.sidebar.number_input("Medallón de Carne 90g ($)", value=1260.82, step=50.0)
precio_pan = st.sidebar.number_input("Pan de Papa 10cm ($)", value=410.00, step=20.0)
precio_cheddar = st.sidebar.number_input("Queso Cheddar (feta) ($)", value=151.12, step=10.0)
precio_panceta = st.sidebar.number_input("Panceta Ahumada ($)", value=282.62, step=20.0)
precio_provolone = st.sidebar.number_input("Queso Dambo / Provo ($)", value=151.12, step=10.0)
precio_papas = st.sidebar.number_input("Papas 150g ($)", value=780.00, step=50.0)

st.sidebar.divider()
st.sidebar.header("📈 Márgenes y Comisiones")
multiplicador_margen = st.sidebar.number_input("Multiplicador de Costo (Ej: 3x)", value=3.0, step=0.1)
comision_pedidosya = st.sidebar.slider("Comisión PedidosYa (%)", min_value=15.0, max_value=35.0, value=30.0) / 100

# Packaging e insumos fijos promedio por combo (Caja, papel, sobres, potes)
costo_packaging_fijo = 1500.00

# ==========================================
# 2. LÓGICA DE CÁLCULO DE RECETAS
# ==========================================
def calcular_costo_combo(medallones, cheddar, panceta=0, es_provo=False, incluye_papas=True):
    queso_costo = precio_provolone if es_provo else precio_cheddar
    costo_hamb = (medallones * precio_carne) + precio_pan + (cheddar * queso_costo) + (panceta * precio_panceta)
    costo_extra = precio_papas if incluye_papas else 0
    return costo_hamb + costo_extra + costo_packaging_fijo

# Definición de la carta de combos
combos = [
    {"Nombre": "Combo Bunker Simple", "Medallones": 1, "Cheddar": 2, "Panceta": 0, "Provo": False},
    {"Nombre": "Combo Bunker Doble", "Medallones": 2, "Cheddar": 4, "Panceta": 0, "Provo": False},
    {"Nombre": "Combo Bunker Triple", "Medallones": 3, "Cheddar": 6, "Panceta": 0, "Provo": False},
    {"Nombre": "Extremo Simple c/ Panceta", "Medallones": 1, "Cheddar": 2, "Panceta": 2, "Provo": False},
    {"Nombre": "Extremo Doble c/ Panceta", "Medallones": 2, "Cheddar": 4, "Panceta": 2, "Provo": False},
    {"Nombre": "Extremo Triple c/ Panceta", "Medallones": 3, "Cheddar": 6, "Panceta": 2, "Provo": False},
    {"Nombre": "De Barrio Simple", "Medallones": 1, "Cheddar": 2, "Panceta": 0, "Provo": False},
    {"Nombre": "De Barrio Doble", "Medallones": 2, "Cheddar": 4, "Panceta": 0, "Provo": False},
    {"Nombre": "Provo Burguer Simple", "Medallones": 1, "Cheddar": 2, "Panceta": 2, "Provo": True},
    {"Nombre": "Provo Burguer Doble", "Medallones": 2, "Cheddar": 4, "Panceta": 2, "Provo": True},
    {"Nombre": "Provo Burguer Cuádruple", "Medallones": 4, "Cheddar": 8, "Panceta": 2, "Provo": True},
]

# Procesar datos
tabla_datos = []
for c in combos:
    costo_total = calcular_costo_combo(c["Medallones"], c["Cheddar"], c["Panceta"], c["Provo"])
    precio_wa = costo_total * multiplicador_margen
    precio_pya = precio_wa / (1 - comision_pedidosya)
    
    tabla_datos.append({
        "Producto / Combo": c["Nombre"],
        "Costo Total Insumos": f"${costo_total:,.2f}",
        "Precio Venta WhatsApp": f"${round(precio_wa, -2):,.0f}",
        "Precio Venta PedidosYa": f"${round(precio_pya, -2):,.0f}",
        "Ganancia Bruta (WA)": f"${(precio_wa - costo_total):,.2f}"
    })

# ==========================================
# 3. INTERFAZ Y VISUALIZACIÓN
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Precios Sugeridos por Combo")
    df_combos = pd.DataFrame(tabla_datos)
    st.dataframe(df_combos, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🧮 Simulación de Incremento de Carne")
    st.write(f"**Precio actual del medallón:** ${precio_carne:,.2f}")
    
    nuevo_precio_carne = st.number_input("Probar si la carne sube a ($):", value=precio_carne + 200.0, step=50.0)
    diferencia = nuevo_precio_carne - precio_carne
    
    st.warning(f"Aumento por medallón: +${diferencia:,.2f}")
    st.write(f"* **Combo Simple:** Subirá +${(diferencia * multiplicador_margen):,.0f} en WhatsApp")
    st.write(f"* **Combo Doble:** Subirá +${(diferencia * 2 * multiplicador_margen):,.0f} en WhatsApp")
    st.write(f"* **Combo Triple:** Subirá +${(diferencia * 3 * multiplicador_margen):,.0f} en WhatsApp")
