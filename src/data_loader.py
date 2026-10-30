import fastf1

def setup_cache(percorso):
    '''Attiva la cache per la sessione di F1'''
    fastf1.Cache.enable_cache(percorso)

     
def load_session(anno, gp, tipo):
    ''' Carica la sessione in base ad Anno, Tipo e Gran Premio'''
    sessione = fastf1.get_session(anno, gp, tipo)
    sessione.load()
    return sessione


def load_schedule(anno):
    '''Restituisce il calendario dell'anno selezionato, esclusi i test prestagionali.'''
    return fastf1.get_event_schedule(anno, include_testing = False)