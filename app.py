import streamlit as st
from src.data_loader import setup_cache, load_session
from src.analysis import get_driver_laps, only_accurate

setup_cache("data/cache")

@st.cache_resource(ttl=3600, show_spinner="Caricamento sessione...")
def carica_sessione_cache(anno, gp, tipo):
    return load_session(anno, gp, tipo)

st.title("Welcome to the F1 Dashboard, by Andrea Wloch")

gp = st.selectbox("Gran Premio", ["Monza", "Monaco"])
anno = st.selectbox("Anno", [2023, 2024, 2025])
pilota = st.selectbox("Pilota", ["VER", "HAM", "LEC", "RUS"])
tipo = st.selectbox("Tipo", ["R", "Q"])
accurate = st.checkbox("Mostra solo giri accurate")
 

st.write(f"Selezionato: {gp}, {anno}, {pilota}, in modalità {tipo}")

sessione = carica_sessione_cache(anno, gp, tipo)
pilota_scelto = get_driver_laps(sessione, pilota)

if accurate:
    pilota_scelto_accurate = only_accurate(pilota_scelto)
    st.dataframe(pilota_scelto_accurate[['LapNumber', 'LapTimeSec', 'Compound', 'Stint', 'TyreLife']])
else:
    st.dataframe(pilota_scelto[['LapNumber', 'LapTimeSec', 'Compound', 'Stint', 'TyreLife']])

