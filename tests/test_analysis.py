import pandas as pd
from src.analysis import only_accurate, filter_lap_range, filter_compounds, summarize_stints

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


def test_filter_lap_range_include_estremi():
    totale_giri1 = pd.DataFrame({'LapNumber': [1, 2, 3, 4, 5], })
    risultato = filter_lap_range(totale_giri1, 2, 4)
    assert risultato['LapNumber'].tolist() == [2, 3, 4]


def test_filter_lap_range_senza_giri():
    totale_giri1 = pd.DataFrame({'LapNumber': [1, 2, 3, 4, 5], })
    risultato = filter_lap_range(totale_giri1, 10, 20)
    assert risultato.empty


def test_filter_compounds_seleziona_mescole():
    giri = pd.DataFrame({'LapNumber': [1, 2, 3, 4], 'Compound': ["SOFT", "HARD", "MEDIUM", "HARD"]})
    risultato = filter_compounds(giri, ["HARD", "MEDIUM"])
    assert risultato['LapNumber'].tolist() == [2, 3, 4]


def test_filter_compounds_selezione_vuota():
    giri = pd.DataFrame({'LapNumber': [1, 2, 3, 4], 'Compound': ["SOFT", "HARD", "MEDIUM", "HARD"]})
    risultato = filter_compounds(giri, [])
    assert risultato.empty


def test_summarize_stints_giri_non_consecutivi():
    gruppo = pd.DataFrame({'LapNumber': [10, 11, 13, 14, 16], 'Stint' : [1, 1, 1, 2, 2], 'Compound' : ["MEDIUM", "MEDIUM", "MEDIUM", "HARD", "HARD"]})
    risultato = summarize_stints(gruppo)
    assert risultato['LapCount'].tolist() == [3, 2]
    assert risultato['FirstLap'].tolist() == [10, 14]
    assert risultato['LastLap'].tolist() == [13, 16]
    assert risultato['Compound'].tolist() == ["MEDIUM", "HARD"]
    assert risultato['Stint'].tolist() == [1, 2]


def test_filtri_combinati():
    giri = pd.DataFrame({'LapNumber': [9, 10, 11, 12, 13, 14], 'Compound': ["HARD", "HARD", "MEDIUM", "HARD", "HARD", "HARD"], 'IsAccurate': [True, True, True, False, True, True]})
    risultato = filter_lap_range(giri, 10, 13)
    risultato = filter_compounds(risultato, ["HARD"])
    risultato = only_accurate(risultato)
    assert risultato['LapNumber'].tolist() == [10, 13]