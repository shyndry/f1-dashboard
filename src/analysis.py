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