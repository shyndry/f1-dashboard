import streamlit as st
import matplotlib.pyplot as plt
from src.data_loader import setup_cache, load_session
from src.analysis import get_driver_laps, only_accurate, filter_lap_range, filter_compounds
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
    mescole_disponibili = sessione.laps['Compound'].unique()
    mescole_selezionate = st.multiselect("Mescole: ", mescole_disponibili, default = mescole_disponibili)
    if not mescole_selezionate:
        st.warning("Seleziona almeno una mescola")
        st.stop()
    giri_piloti = {}
    for pilota in piloti:
        giri = get_driver_laps(sessione, pilota)
        giri = filter_lap_range(giri, giro_inizio, giro_fine)
        giri = filter_compounds(giri, mescole_selezionate)
        if accurate:
            giri = only_accurate(giri)
        giri_piloti[pilota] = giri
except DataNotLoadedError:
    st.error("Impossibile caricare i dati della sessione selezionata")
    st.stop()

if all(giri.empty for giri in giri_piloti.values()):
    st.warning("Nessun giro disponibile con i filtri selezionati")
    st.stop()

piloti_con_giri = []

for pilota, giri in giri_piloti.items():
    if not giri.empty:
        piloti_con_giri.append(pilota)

nomi_piloti = ", ".join(piloti_con_giri)

fig = plot_lap_times(giri_piloti, f"Confronto dei tempi sul giro di {nomi_piloti} a {gp}, anno {anno}")
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

