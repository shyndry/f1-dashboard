import matplotlib.pyplot as plt

def plot_lap_times(giri_piloti, titolo):
    '''Disegna il tempo sul giro di uno o più piloti nello stesso grafico'''
    fig, ax = plt.subplots()
    for nome, pilota in giri_piloti.items():
        if pilota.empty:
            continue
        ax.scatter(pilota["LapNumber"], pilota["LapTimeSec"], label = nome)

    ax.set_title(titolo)
    ax.set_xlabel("Giri")
    ax.set_ylabel("Tempo sul giro (s)")
    ax.legend()
    return fig


def plot_stints(giri):
    '''Disegna i giri di un solo pilota, con un colore per ogni stint'''
    fig, ax = plt.subplots()
    stints = giri["Stint"].unique()
    for s in stints:
        pilota_stint = giri[giri["Stint"] == s]
        ax.scatter(pilota_stint["LapNumber"], pilota_stint["LapTimeSec"], label = f"Stint {int(s)} - {pilota_stint['Compound'].iloc[0]}")

    ax.set_title(f"Stint di {giri['Driver'].iloc[0]}")
    ax.set_xlabel("Giri")
    ax.set_ylabel("Tempo sul giro (s)")
    ax.legend()
    return fig


def plot_speed_trace(telemetrie_piloti):
    '''Disegna la velocità dei piloti in base alla distanza percorsa'''
    fig, ax = plt.subplots()
    for pilota, telemetria in telemetrie_piloti.items():
        ax.plot(telemetria['Distance'], telemetria['Speed'], label=pilota)
    ax.set_title("Confronto della velocità dei giri più veloci")
    ax.set_xlabel("Distanza (m)")
    ax.set_ylabel("Velocità (km/h)")
    ax.legend()
    return fig