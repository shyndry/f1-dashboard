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
