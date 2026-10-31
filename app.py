import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from src.data_loader import setup_cache, load_session, load_schedule
from src.analysis import get_driver_laps, only_accurate, filter_lap_range, filter_compounds, summarize_stints, get_fastest_lap
from src.plots import plot_lap_times, plot_stints, plot_speed_trace
from fastf1.exceptions import DataNotLoadedError
from datetime import date, datetime, timezone

setup_cache("data/cache")

@st.cache_resource(ttl=3600, show_spinner="Caricamento sessione...")
def carica_sessione_cache(anno, gp, tipo):
    return load_session(anno, gp, tipo)

@st.cache_data(ttl=3600, show_spinner="Caricamento calendario...")
def carica_calendario_cache(anno):
    return load_schedule(anno)

st.title("Welcome to the F1 Dashboard, by Andrea Wloch")

anno = st.selectbox("Anno", list(range(2018, date.today().year + 1)))

try:
    calendario = carica_calendario_cache(anno)
    if calendario.empty:
        st.warning("Assenza di eventi per l'anno selezionato")
        st.stop()
except ValueError:
    st.error("Il calendario non è stato caricato correttamente")
    st.stop()

gp = st.selectbox("Gran Premio", calendario['EventName'])

maschera = calendario['EventName'] == gp
evento = calendario[maschera].iloc[0]
sessioni_disponibili = evento[['Session1', 'Session2', 'Session3', 'Session4', 'Session5']].dropna()

tipo = st.selectbox("Tipo", sessioni_disponibili)
data_sessione = evento.get_session_date(tipo, utc=True)
ora_utc = datetime.now(timezone.utc).replace(tzinfo=None)

accurate = st.checkbox("Mostra solo giri accurati")

try:
    if pd.isna(data_sessione):
        st.warning("Data della sessione non disponibile nel calendario")
        st.stop()
    if data_sessione > ora_utc:
        st.warning("La sessione selezionata non è ancora iniziata")
        st.stop()
    sessione = carica_sessione_cache(anno, gp, tipo)
    if sessione.laps.empty:
        st.warning("Nessun giro disponibile per la sessione selezionata")
        st.stop()
    piloti_disponibili = sessione.laps['Driver'].unique()
    mostra_telemetria = st.checkbox("Mostra la telemetria di un pilota")
    if mostra_telemetria:
        st.header("Telemetria del giro più veloce")
        pilota_telemetria = st.selectbox(label="Pilota per la telemetria", options=piloti_disponibili)
        giri_telemetria = get_driver_laps(sessione, pilota_telemetria)
        giro_veloce = get_fastest_lap(giri_telemetria)
        if giro_veloce is None:
            st.warning("Il pilota non ha un giro veloce idoneo")
        else:
            try:
                telemetria = giro_veloce.get_car_data().add_distance()
            except DataNotLoadedError:
                st.error("Telemetria non disponibile per la sessione selezionata")
            else:
                if telemetria.empty:
                    st.warning("Dati della telemetria vuoti")
                else:
                    fig = plot_speed_trace(telemetria, pilota_telemetria)
                    st.pyplot(fig)
                    plt.close(fig)
    piloti = st.multiselect("Piloti: ", piloti_disponibili)
    if not piloti:
        st.warning("Non sono stati scelti piloti")
        st.stop()
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
        st.warning(f"Nessun giro per {pilota} con i filtri selezionati")
        continue
  
    col1, col2, col3 = st.columns(3)
    tempi_validi = giri['LapTimeSec'].dropna()
    if tempi_validi.empty:
        col1.metric("Miglior giro", "N/D")
    else:
        miglior_tempo = tempi_validi.min()
        col1.metric("Miglior giro", f"{miglior_tempo:.3f} s")
    numero_giri = len(giri)
    col2.metric("Giri considerati: ", numero_giri)
    if tempi_validi.empty:
        col3.metric("Tempo mediano", "N/D")
    else:
        tempo_mediano = tempi_validi.median()
        col3.metric("Tempo mediano", f"{tempo_mediano:.3f} s")

    tabella_export = giri[['LapNumber', 'LapTimeSec', 'Compound', 'Stint', 'TyreLife']]
    st.dataframe(tabella_export)
    csv_dati = tabella_export.to_csv(index=False)
    nome_file = f"{pilota}_{gp}_{anno}_{tipo}.csv"
    st.download_button(label = "Scarica CSV", data = csv_dati, file_name = nome_file, mime = "text/csv")

    st.write("Riepilogo stint sui giri filtrati")
    riepilogo_stint = summarize_stints(giri)
    st.dataframe(riepilogo_stint)

    fig = plot_stints(giri)
    st.pyplot(fig)
    plt.close(fig)