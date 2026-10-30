import pandas as pd

def get_driver_laps(sessione, pilota):
    '''Ottiene i giri del pilota'''
    giri = sessione.laps
    driver = giri.pick_drivers(pilota).copy()
    driver["LapTimeSec"] = driver["LapTime"].dt.total_seconds()
    return driver


def only_accurate(giri):
    '''Mantiene solo i giri con IsAccurate vero'''
    driver_acc = giri[giri["IsAccurate"]].copy()
    return driver_acc


def filter_lap_range(giri, giro_inizio, giro_fine):
    '''Restituisce una copia dei giri nell'intervallo, estremi inclusi'''
    maschera = giri['LapNumber'].between(giro_inizio, giro_fine)
    return giri[maschera].copy()


def filter_compounds(giri, mescole_selezionate):
    '''Restituisce una copia dei giri con le mescole selezionate'''
    maschera_mescole = giri['Compound'].isin(mescole_selezionate)
    return giri[maschera_mescole].copy()


def summarize_stints(giri):
    '''Riepiloga gli stint dei giri forniti, per un singolo pilota.'''
    gruppi = giri.groupby('Stint')
    primi_giri = gruppi['LapNumber'].min()
    ultimi_giri = gruppi['LapNumber'].max()
    numero_giri = gruppi.size()
    mescole = gruppi['Compound'].first()
    riepilogo = pd.DataFrame({'Compound': mescole, 'FirstLap': primi_giri, 'LastLap': ultimi_giri, 'LapCount': numero_giri })
    riepilogo = riepilogo.reset_index()
    return riepilogo


def get_fastest_lap(giri):
    '''Restituisce il giro più veloce idoneo oppure None se non disponibile.'''    
    return giri.pick_fastest()