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
piloti = st.multiselect("Piloti: ", ["HAM", "LEC", "VER", "RUS"], default = ["HAM", "LEC"])
tipo = st.selectbox("Tipo", ["R", "Q"])
accurate = st.checkbox("Mostra solo giri accurate")
 
if not piloti:
    st.warning("Non sono stati scelti piloti")
    st.stop()

try:
    sessione = carica_sessione_cache(anno, gp, tipo)
    primo_giro = int(sessione.laps['LapNumber'].min())
    ultimo_giro = int(sessione.laps['LapNumber'].max())
    giro_inizio, giro_fine = st.slider(
        "Intervallo di giri",
        min_value=primo_giro,
        max_value=ultimo_giro,
        value=(primo_giro, ultimo_giro)
    )
    giri_piloti = {}
    for pilota in piloti:
        giri = get_driver_laps(sessione, pilota)
        maschera = giri['LapNumber'].between(giro_inizio, giro_fine)
        giri = giri[maschera].copy()
        if accurate:
            giri = only_accurate(giri)
        giri_piloti[pilota] = giri
except DataNotLoadedError:
    st.error("Impossibile caricare i dati della sessione selezionata")
    st.stop()

fig = plot_lap_times(giri_piloti, f"Confronto dei tempi sul giro di {piloti} a {gp}, anno {anno}")
st.pyplot(fig)
plt.close(fig)

for pilota, giri in giri_piloti.items():
    st.subheader(pilota)
    if giri.empty:
        st.warning("Non ci sono giri del pilota")
        continue
  
    col1, col2, col3 = st.columns(3)
    miglior_tempo = giri['LapTimeSec'].min()
    col1.metric("Miglior giro", f"{miglior_tempo:.3f} s")
    numero_giri = len(giri)
    col2.metric("Giri considerati: ", numero_giri)
    tempo_mediano = giri['LapTimeSec'].median()
    col3.metric("Tempo mediano: ", f"{tempo_mediano:.3f} s")
  
    st.dataframe(giri[['LapNumber', 'LapTimeSec', 'Compound', 'Stint', 'TyreLife']])
    fig = plot_stints(giri)
    st.pyplot(fig)
    plt.close(fig)

