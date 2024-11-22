'''
Questo modulo contiene le funzioni necessarie alla simulazione elettorale del Rosatellum,
che implementa il metodo proporzionale misto per assegnare seggi a livello nazionale e
locale utilizzando i metodi Hare e D'Hondt.
'''
import warnings
from contextlib import nullcontext

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import plotly.express as px
from pandas.errors import PerformanceWarning
import logging

# Ignora specifici avvisi di pandas per evitare rumore nel log
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=PerformanceWarning)

# Impostazione di pandas per la gestione dei downcasting futuri
pd.set_option('future.no_silent_downcasting', True)


# Configurazione del logger per rosatellum
rosatellum_logger = logging.getLogger('rosatellum_logger')
rosatellum_logger.setLevel(logging.DEBUG)

# Creazione di un handler per scrivere su file
file_handler = logging.FileHandler('Rosatellum_Logs')
file_handler.setLevel(logging.DEBUG)

# Formattazione opzionale del log
formatter = logging.Formatter('%(message)s \n\n')
file_handler.setFormatter(formatter)
# Aggiunta dell'handler al logger
rosatellum_logger.addHandler(file_handler)
rosatellum_logger.propagate = False


#1
def seleziona_vincitore_collegio(*a, data, **kwargs):
    """
    Ordina i candidati in un collegio per numero di voti e seleziona il vincitore.

    Parameters
    ----------
    data : DataFrame
        DataFrame contenente i candidati e i loro voti.

    Returns
    -------
    DataFrame
        Contiene il partito collegato e i voti del vincitore.
    """
    # Ordina i candidati in base ai voti in ordine decrescente per trovare il vincitore
    data.sort_values('Voti', ascending=False, inplace=True, ignore_index=True)
    rosatellum_logger.info(f"Voti ordinati nel collegio:\n{data}")

    # Inizializza il DataFrame risultato con la struttura dei dati di output
    risultato = pd.DataFrame(columns=['Partito','Coalizione', 'VotiVincenti'])

    #aggiunge il vincitore
    nuova_riga = pd.DataFrame([{
        'Partito': data.at[0, 'Partito'],
        'Coalizione': data.at[0, 'Coalizione'],
        'VotiVincenti': data.at[0, 'Voti']
    }])
    risultato = pd.concat([risultato, nuova_riga], ignore_index=True)
    rosatellum_logger.info(f"Vincitore selezionato:\n{risultato}")
    return risultato

#2
def unisci_voti_maggioritario_proporzionale(data, voti_proporzionale):
    """
    Unisce i voti della parte maggioritaria e proporzionale

    Parameters
    ----------
    data : DataFrame
        DataFrame dei voti maggioritari.
    voti_proporzionale : DataFrame
        DataFrame dei voti proporzionali.

    Returns
    -------
    DataFrame
        DataFrame unito con le colonne 'Partito', 'Voti', e 'Cifra'.
    """

    # print("datarosa",data)
    # print("votirosa",voti_proporzionale)
    # Copia il DataFrame originale
    res = data.copy()

    # Unisce i voti proporzionali e maggioritari usando 'Partito' come chiave
    res = pd.merge(voti_proporzionale,res[['Partito']], on='Partito', how='outer')
    # Riempie i valori nulli e converte oggetti
    res = res.fillna({'Voti': 0, 'Partito': '', 'Coalizione': ''}).infer_objects(copy=False)

    # Converti in interi e calcola 'Cifra' come totale dei voti
    res['Voti'] = res['Voti'].astype(int)
    res['Cifra'] = res['Voti']
    rosatellum_logger.info(f"Unione dei voti uninominali e plurinominali:\n{res[['Partito', 'Coalizione', 'Voti', 'Cifra']]}")
    print("resrosa",res)
    return res[['Partito','Coalizione', 'Voti', 'Cifra']]

#3
def distribuzione_seggi_circoscrizionali(*, information, distribution, district_votes, seggi_circoscrizione, **kwargs):
    """
    Distribuisce i seggi proporzionali per circoscrizione usando il metodo hare.

    Parameters
    ----------
    information : dict
        Informazioni a livello nazionale.
    distribution : DataFrame
        Distribuzione dei seggi nazionali per ogni partito.
    district_votes : DataFrame
        Voti e cifre elettorali a livello di circoscrizione.
    seggi_circoscrizione : int
        Numero di seggi nella circoscrizione specifica.

    Returns
    -------
    DataFrame
        DataFrame con la distribuzione dei seggi per ogni partito nella circoscrizione.
    """
    # Imposta l'indice di district_votes per agevolare l'accesso ai dati
    district_votes.set_index('Partito', inplace=True)
    somma_cifre = district_votes['Cifra'].sum()
    q = somma_cifre / seggi_circoscrizione  # Divisore basato su somma delle cifre e seggi disponibili
    rosatellum_logger.info(f"Quoziente di distribuzione (Hare) per la circoscrizione: {q}")
    res = []
    for _, r in distribution.iterrows():
        cifra = district_votes.at[r['Partito'], 'Cifra']
        seggi_assegnati = cifra // q
        res.append(pd.Series({
            'Partito': r['Partito'],
            'Coalizione': r['Coalizione'],
            'Seggi': seggi_assegnati,
            'Resto': cifra / q - seggi_assegnati,
            'SeggiCircoscrizione': seggi_circoscrizione
        }))

    # Combina i risultati in un DataFrame e infine converte i tipi in oggetti adeguati
    res = pd.concat(res, axis=1).T.infer_objects(copy=False)
    return res

#4
def distribuzione_hare_nazionale(data, seggi_totali):
    """
    Distribuisce i seggi a livello nazionale per il Rosatellum usando il metodo Hare.

    Parameters
    ----------
    data : DataFrame
        DataFrame aggregato con i dati delle circoscrizioni e i voti per ogni partito.
    seggi_totali : int
        Numero di seggi totali per la distribuzione proporzionale.

    Returns
    -------
    DataFrame
        DataFrame con 'Partito', 'Coalizione', 'Voti', 'Cifra', 'Seggi', e 'Resto' per ciascun partito.
    """
    res = data.copy()
    rosatellum_logger.info(res)
    # Calcola il quoziente Hare
    quoziente_hare = res['Voti'].sum() / seggi_totali
    rosatellum_logger.info(f"Quoziente Hare nazionale: {quoziente_hare}")

    # Assegna i seggi interi a ciascun partito dividendo per il quoziente Hare
    res['Seggi'] = (res['Cifra'] / quoziente_hare).astype(int)

    # Calcola il resto per ciascun partito
    res['Resto'] = res['Cifra'] - (res['Seggi'] * quoziente_hare)
    rosatellum_logger.info(f"Seggi assegnati (prima della distribuzione dei resti):\n{res[['Partito', 'Seggi', 'Resto']]}")

    # Calcola i seggi rimanenti
    seggi_assegnati = res['Seggi'].sum()
    seggi_rimanenti = seggi_totali - seggi_assegnati

    # Assegna i seggi rimanenti ai partiti con i maggiori resti
    res = res.sort_values(by='Resto', ascending=False)
    # Seleziona le prime 'seggi_rimanenti' righe del DataFrame ordinato e incrementa di 1 il valore nella colonna 'Seggi' per ciascuna di queste righe.
    res.iloc[:seggi_rimanenti, res.columns.get_loc('Seggi')] += 1

    # Riordina e seleziona le colonne richieste
    res = res.sort_index()
    rosatellum_logger.info(f"Distribuzione finale dei seggi nazionali:\n{res[['Partito', 'Seggi']]}")
    return res[['Partito', 'Coalizione', 'Voti', 'Cifra', 'Seggi', 'Resto']]

#5
def correggi_distribuzione_locale(distretto, distribuzione_ideale, distribuzione_raccolta, info_locali, *info_comuni):
    """
    Corregge la distribuzione locale dei seggi in base ai resti e alla distribuzione ideale nazionale.

    Parameters
    ----------
    distretto : str
        Nome del distretto o area di calcolo.
    distribuzione_ideale : DataFrame
        Distribuzione ideale dei seggi a livello nazionale per partito.
    distribuzione_raccolta : dict
        Distribuzione locale dei seggi per circoscrizione.
    info_locali : dict
        Informazioni locali sui resti e seggi assegnabili.
    *info_comuni : args
        Informazioni generali comuni a tutte le lanes (non utilizzate qui).

    Returns
    -------
    dict
        Distribuzione corretta dei seggi per ogni circoscrizione.
    """
    # Imposta l'indice del DataFrame `distribuzione_ideale` sulla colonna 'Partito' per un accesso facilitato ai dati
    distribuzione_ideale.set_index('Partito', inplace=True)

    # Inizializza un dizionario per tracciare i seggi già assegnati a ciascun partito
    seggi_gia_assegnati = {}
    for circoscrizione, distribuzione in distribuzione_raccolta.items():
        # Itera sulle righe della distribuzione locale e somma i seggi assegnati a ciascun partito
        for _, row in distribuzione.iterrows():
            partito = row['Partito']
            seggi_gia_assegnati[partito] = seggi_gia_assegnati.get(partito, 0) + row['Seggi']
        # Reindicizza il DataFrame `distribuzione` per partito
        distribuzione.set_index('Partito', inplace=True)

    # Calcola quanti seggi spettano ancora a ciascun partito confrontando i seggi ideali con quelli già assegnati
    seggi_dovuti = distribuzione_ideale['Seggi'] - pd.Series(seggi_gia_assegnati).fillna(0)

    # Ordina le informazioni locali basandosi sul numero di seggi assegnabili nella circoscrizione
    for circoscrizione, info in sorted(info_locali.items(), key=lambda x: list(x[1].values())[0]['SeggiCircoscrizione']):
        distribuzione_locale = distribuzione_raccolta[circoscrizione]
        # Calcola quanti seggi rimangono da assegnare nella circoscrizione
        seggi_da_assegnare = list(info.values())[0]['SeggiCircoscrizione'] - distribuzione_locale['Seggi'].sum()

        # Crea una lista di partiti ordinata per resti per assegnare i seggi rimanenti
        partiti_ordinati = sorted(
            [(partito, data['Resto']) for partito, data in info.items() if seggi_dovuti.get(partito, 0) > 0],
            key=lambda x: x[1], reverse=True  # Ordina per resti in ordine decrescente
        )

        # Assegna i seggi rimanenti ai partiti, partendo da quelli con il maggior resto
        for partito, resto in partiti_ordinati:
            while seggi_dovuti[partito] > 0 and seggi_da_assegnare > 0:
                distribuzione_locale.at[partito, 'Seggi'] += 1  # Aggiungi un seggio al partito nella circoscrizione
                seggi_dovuti[partito] -= 1  # Riduci il numero di seggi ancora da assegnare al partito
                seggi_da_assegnare -= 1  # Riduci il numero di seggi disponibili nella circoscrizione

    # Gestione dei seggi residui che non sono ancora stati assegnati
    seggi_dovuti = seggi_dovuti[seggi_dovuti > 0]
    for partito, seggi_rimanenti in seggi_dovuti.items():
        # Ordina le circoscrizioni disponibili per il partito in base ai resti
        resti_disponibili = sorted(
            [(circ, info[partito]['Resto']) for circ, info in info_locali.items() if info[partito]['Resto'] > 0],
            key=lambda x: x[1], reverse=True  # Ordina per resti decrescenti
        )
        # Assegna i seggi rimanenti nelle circoscrizioni selezionate
        for circoscrizione, _ in resti_disponibili[:seggi_rimanenti]:
            distribuzione_raccolta[circoscrizione].at[partito, 'Seggi'] += 1

    # Restituisce la distribuzione corretta e reindicizza i risultati
    distribuzione_raccolta = {k: v.reset_index() for k, v in distribuzione_raccolta.items()}
    return distribuzione_raccolta, {}, {}

#6 applico i filtri in partito.py

def ordina_tuple(tuples):
    """
    Ordina una lista di tuple in base al secondo elemento.

    Parameters
    ----------
    tuples : list
        Lista di tuple da ordinare.
    """
    return sorted(tuples, key=lambda item: item[1])


def calcola_coordinate_parlamento(df, angle_total=180, rows=10, ratio=6, initial='PARTITO'):
    """
    Calcola le coordinate polari per disporre i seggi in un grafico parlamentare.

    Parameters
    ----------
    df : DataFrame
        DataFrame contenente le informazioni sui partiti.
    angle_total : int, opzionale
        Angolo totale del grafico, default a 180.
    rows : int, opzionale
        Numero di righe di seggi, default a 10.
    ratio : int, opzionale
        Fattore di scala per le righe, default a 6.
    initial : str, opzionale
        Colonna da cui ottenere l'iniziale, default a 'PARTITO'.
    """
    arco_totale = sum(math.pi * (ratio + i) for i in range(rows))
    angoli = [angle_total / round(math.pi * (ratio + i) / (arco_totale / len(df)), 0) for i in range(rows)]

    coord = []
    for idx, angolo_corrente in enumerate(angoli):
        current_angle = angolo_corrente / 2
        row_count = int(round(angle_total / angoli[idx], 0))
        for _ in range(row_count):
            coord.append((ratio + idx, current_angle))
            current_angle += angoli[idx]

    coord = ordina_tuple(coord)
    df["raggio"] = [r for r, _ in coord]
    df["theta"] = [theta for _, theta in coord]
    df["INIZIALE"] = df[initial].apply(lambda x: x[0])
    return df


def show_rosatellum_chart(final_result):
    """
    Genera e visualizza un grafico parlamentare e un grafico a torta per i seggi dei partiti.

    Parameters
    ----------
    final_result : list
        Lista di tuple contenenti informazioni sui partiti, il tipo di seggio e il numero di seggi.
    """
    # Creazione del DataFrame per i dati
    dati = [(partito, tipo) for circoscrizione, tipo, partito, seggi in final_result for _ in range(seggi)]
    #rosatellum_logger.info("dati",dati)
    df = pd.DataFrame(dati, columns=["PARTITO", "TIPO"])

    # Mappatura delle coalizioni
    mappa_coalizioni = {
        "FRATELLI D'ITALIA CON GIORGIA MELONI": "Centro-destra",
        "FORZA ITALIA": "Centro-destra",
        "LEGA PER SALVINI PREMIER": "Centro-destra",
        "NOI MODERATI/LUPI - TOTI - BRUGNARO - UDC": "Centro-destra",
        "MOVIMENTO 5 STELLE": "Centro",
        "PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA": "Centro-sinistra",
        "+EUROPA": "Centro-sinistra",
        "IMPEGNO CIVICO LUIGI DI MAIO - CENTRO DEMOCRATICO": "Centro-sinistra",
        "ALLEANZA VERDI E SINISTRA": "Centro-sinistra",
        "AZIONE - ITALIA VIVA - CALENDA": "Centro",
        "SUDTIROLER VOLKSPARTEI (SVP) - PATT": "Autonomie",
        "SUD CHIAMA NORD": "Autonomie",
        "VALLEE D?AOSTE ? AUTONOMIE PROGRES FEDERALISME" : "Autonomie"
    }
    df["COALIZIONE"] = df["PARTITO"].map(mappa_coalizioni)

    # Impostazione dei colori per ogni partito
    colori_mappa = {
        "FRATELLI D'ITALIA CON GIORGIA MELONI": "#0B3D91",
        "FORZA ITALIA": "#6BAED6",
        "LEGA PER SALVINI PREMIER": "#4F83CC",
        "NOI MODERATI/LUPI - TOTI - BRUGNARO - UDC": "#4F83CC",
        "PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA": "#FF7F0E",
        "ALLEANZA VERDI E SINISTRA": "#FFA54C",
        "+EUROPA": "#FFA54C",
        "IMPEGNO CIVICO LUIGI DI MAIO - CENTRO DEMOCRATICO": "#FFA54C",
        "AZIONE - ITALIA VIVA - CALENDA": "#800080",
        "MOVIMENTO 5 STELLE": "#FFD700",
        "SUDTIROLER VOLKSPARTEI (SVP) - PATT": "#FFE066",
        "SUD CHIAMA NORD": "#FFEB99",
        "VALLEE D?AOSTE ? AUTONOMIE PROGRES FEDERALISME": "#FFEB00"
    }
    df["COLORE"] = df["PARTITO"].map(colori_mappa)

    # Definisci l'ordine delle coalizioni
    ordine_coalizioni = {"Centro-destra": 1, "Centro": 2, "Autonomie": 3, "Centro-sinistra": 4}
    df['ORDINE_COALIZIONE'] = df['COALIZIONE'].map(ordine_coalizioni)

    # Ordina il DataFrame prima per coalizione e poi per partito
    df = df.sort_values(by=['ORDINE_COALIZIONE', 'PARTITO']).reset_index(drop=True)
    df = df.drop(columns=['ORDINE_COALIZIONE'])

    # Calcola le coordinate polari per il grafico parlamentare, ora i partiti saranno raggruppati
    df = calcola_coordinate_parlamento(df, angle_total=180, rows=10, ratio=6, initial="PARTITO")

    # Configurazione del grafico polar scatter
    fig = px.scatter_polar(
        df,
        r="raggio",
        theta="theta",
        color="PARTITO",
        color_discrete_map=colori_mappa,
        text="INIZIALE",
        start_angle=0,
        custom_data=["PARTITO", "COALIZIONE"],
        range_theta=[0, 180],
        direction="counterclockwise",
    )

    # Configurazione dell'aspetto del grafico
    fig.update_layout(
        #template="plotly_dark",
        height=600,
        width=1400,
        showlegend=True,
        legend=dict(
            title="Partiti",
            font=dict(size=15),
            orientation="v",
            yanchor="top",
            xanchor="left",
            itemsizing="constant",
            traceorder="normal"
        ),
        margin=dict(b=20, r=50, l=20, t=20),
        polar=dict(
            radialaxis=dict(showticklabels=False, ticks=""),
            angularaxis=dict(showticklabels=False, ticks="")
        ),
        paper_bgcolor='white',  # Sfondo bianco
        plot_bgcolor='white',  # Sfondo del grafico bianco
        uniformtext_minsize=8,
        uniformtext_mode="hide"
    )

    fig.update_traces(
        marker=dict(opacity=0.85, size=23),
        hovertemplate="<b>%{customdata[0]}</b> (<i>%{customdata[1]}</i>)<extra></extra>",
        textfont_size=12,
        textposition="middle center"
    )

    # Salva il grafico come immagine
    fig.write_image("parliament_chart.png", scale=2)

    # Generazione del grafico a torta con i partiti raggruppati per coalizione
    seggi_per_partito = {}
    for c, l, p, s in final_result:
        if p != "VALLEE D?AOSTE ? AUTONOMIE PROGRES FEDERALISME":  # Escludi il seggio di VALLEE D'AOSTE
            seggi_per_partito[p] = seggi_per_partito.get(p, 0) + s

    seggi_per_partito["PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA"] += 1
    # Prepara i dati per il grafico a torta
    partiti_seggi = [(p, s, mappa_coalizioni[p]) for p, s in seggi_per_partito.items()]
    partiti_seggi.sort(key=lambda e: (e[2], -e[1]))

    colori = [colori_mappa[p] for p, _, _ in partiti_seggi]
    etichette = [p for p, _, _ in partiti_seggi]
    dimensioni = [s for _, s, _ in partiti_seggi]
    # Creazione del grafico a torta
    plt.figure(figsize=(8, 8))
    plt.pie(
        dimensioni,
        labels=etichette,
        colors=colori,
        shadow=True,
        startangle=180
    )
    plt.axis('equal')
    plt.title('Distribuzione dei seggi per partito')
    plt.savefig('pie_chart.png', bbox_inches='tight')
    plt.close()


def show_rosatellum_chart1(final_result):
    '''
    Produce un output visuale dei risultati finali della simulazione, nello specifico un pie chart.

    Parameters
    ----------
    final_result: lista di tuple del tipo (distretto, lane, partito, seggi_assegnati)
    '''

    rosatellum_logger.info(f"Dati per la visualizzazione:\n{final_result}")
    # Ottengo dizionario del tipo partito: seggi_assegnati_totali
    seats_dict = {}
    for c, l, p, s in final_result:
        if p in seats_dict.keys():
            seats_dict[p] += s
        else:
            seats_dict[p] = s
    #rosatellum_logger.info(seats_dict)
    # Trasformo il dizionario in una lista di tuple ordinate per seggi decrescente
    part_seats = [(p, s) for p, s in seats_dict.items()]
    part_seats.sort(key=lambda e: e[1], reverse=True)

    # Output leggibile dei risultati finali
    rosatellum_logger.info(part_seats)

    # Ottengo la lista dei partiti
    labels_list = [p for p, s in part_seats]
    labels = (*labels_list,)

    # Ottengo la lista dei seggi
    sizes = [s for p, s in part_seats]

    # Ottengo la lista dei colori
    all_colors = ['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#00796B', '#6a3d9a', '#b15928',
                  '#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#4DB6AC', '#cab2d6', '#ffff99', '#9E9E9E']
    colors = [all_colors[i % len(all_colors)] for i in range(len(part_seats))]

    explode = (*[0.15 for _ in range(len(part_seats))],)

    # Genero e mostro il pie chart
    patches, texts, third = plt.pie(
        sizes,
        explode=explode,
        labels=labels,
        labeldistance=1.25,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=180
    )
    #plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    # Salva il grafico su file invece di mostrarlo
    plt.savefig('pie_chart.png')
    # Se desideri visualizzare il grafico e sei in un ambiente interattivo, decommenta la linea seguente
    plt.show()
