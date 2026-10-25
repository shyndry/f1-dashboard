import matplotlib.pyplot as plt

def plot_lap_times(giri_piloti, titolo):
    '''Disegna il tempo sul giro di uno o più piloti nello stesso grafico'''
    for nome, pilota in giri_piloti.items():
        plt.scatter(pilota["LapNumber"], pilota["LapTimeSec"], label = nome)

    plt.title(titolo)
    plt.xlabel("Giri")
    plt.ylabel("Tempo sul giro (s)")
    plt.legend()
    plt.show()


def plot_stints(giri):
    '''Disegna i giri di un solo pilota, con un colore per ogni stint'''
    stints = giri["Stint"].unique()
    for s in stints:
        pilota_stint = giri[giri["Stint"] == s]
        plt.scatter(pilota_stint["LapNumber"], pilota_stint["LapTimeSec"], label = f"Stint {int(s)} - {pilota_stint['Compound'].iloc[0]}")

    plt.title(f"Stint di {giri['Driver'].iloc[0]}")
    plt.xlabel("Giri")
    plt.ylabel("Tempo sul giro (s)")
    plt.legend()
    plt.show()