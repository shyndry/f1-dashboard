import pandas as pd
from src.analysis import only_accurate

def test_only_accurate():
    '''Testing di only_accurate'''
    giri = pd.DataFrame({"LapNumber": [1, 2, 3, 4, 5], "IsAccurate": [True, False, True, True, False]})
    driver_acc = only_accurate(giri)
    assert len(driver_acc) == 3


def test_only_accurate_non_modifica_originale():
    '''Testing di only_accurate per verificare se non modifica il DataFrame originale'''
    giri2 = pd.DataFrame({"LapNumber": [1, 2, 3, 4, 5], "IsAccurate": [True, False, True, True, False]})
    driver_acc = only_accurate(giri2)
    assert len(giri2) == 5



def test_all_false():
    '''Testing di only_accurate su valori tutti False'''
    giri3 = pd.DataFrame({"LapNumber": [1, 2, 3, 4, 5], "IsAccurate": [False, False, False, False, False]})
    driver_acc = only_accurate(giri3)
    assert len(driver_acc) == 0
