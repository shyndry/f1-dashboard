import streamlit as st
import matplotlib.pyplot as plt
from src.data_loader import setup_cache, load_session
from src.analysis import get_driver_laps, only_accurate
from src.plots import plot_lap_times, plot_stints
from fastf1.exceptions import DataNotLoadedError

setup_cache("data/cache")

@st.cache_resource(ttl=3600, show_spinner="Caricamento sessione...")
def carica_sessione_cache(anno, gp, tipo):
    return load_session(anno, gp, tipo)

st.title("Welcome to the F1 Dashboard, by Andrea Wloch")

gp = st.selectbox("Gran Premio", ["Monza", "Monaco"])
anno = st.selectbox("Anno", [2024])
pilota = st.selectbox("Pilota", ["VER", "HAM", "LEC", "RUS"])
tipo = st.selectbox("Tipo", ["R", "Q"])
accurate = st.checkbox("Mostra solo giri accurate")
 

st.write(f"Selezionato: {gp}, {anno}, {pilota}, in modalità {tipo}")

try:
    sessione = carica_sessione_cache(anno, gp, tipo)
    pilota_scelto = get_driver_laps(sessione, pilota)
except DataNotLoadedError:
    st.error("Impossibile caricare i dati della sessione selezionata")
    st.stop()

if accurate:
    tabella= only_accurate(pilota_scelto)
else:
    tabella = pilota_scelto

st.dataframe(tabella[['LapNumber', 'LapTimeSec', 'Compound', 'Stint', 'TyreLife']])

fig = plot_lap_times({pilota: tabella}, f"Tempo sul giro di {pilota} a {gp}, anno {anno}")
st.pyplot(fig)
plt.close(fig)

fig = plot_stints(pilota_scelto)
st.pyplot(fig)
plt.close(fig)