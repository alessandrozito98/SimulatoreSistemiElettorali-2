"""
The system works in the following manner: Parties and independent candidates group themselves into lists or coalitions, basically electoral blocs. 
Each list proposes up to two candidates per electoral region, province, or other geographical unit. 
Votes are first tallied by list instead of by candidate, and unless the list which obtained the first majority has double the voting 
as the second majority, each of the two lists gets one of their candidates, the one who got the most voting, into office
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def fill_coalizione(*a, data, **kwargs):
    toReturn = data.copy()
    if ( 'Coalizione' not in toReturn.columns):
        toReturn['Coalizione'] = 'NO COALIZIONE'
    
    toReturn.loc[toReturn['Coalizione'] == 'NO COALIZIONE', 'Coalizione'] = toReturn['Partito']
    return toReturn

def calc_binomiale(*a, data, **kwargs):
    print(data)
    sorted_df = data.sort_values(['Voti'], ascending = (False))
    toReturn = pd.DataFrame({'Coalizione': [], 'Partito': [], 'Voti': [], 'Seggi': []})
    if (len(sorted_df.index) >= 2):
        if (sorted_df.iloc[0]['Voti'] < sorted_df.iloc[1]['Voti'] * 2):
            toReturn = toReturn.append({ 'Coalizione': sorted_df.iloc[0]['Coalizione'], 'Partito': sorted_df.iloc[0]['Partito'], 'Voti': sorted_df.iloc[0]['Voti'], 'Seggi': 1}, ignore_index=True)
            toReturn = toReturn.append({ 'Coalizione': sorted_df.iloc[1]['Coalizione'], 'Partito': sorted_df.iloc[1]['Partito'], 'Voti': sorted_df.iloc[1]['Voti'], 'Seggi': 1}, ignore_index=True)
        else:
            toReturn = toReturn.append({'Coalizione': sorted_df.iloc[0]['Coalizione'], 'Partito': sorted_df.iloc[0]['Partito'], 'Voti': sorted_df.iloc[0]['Voti'], 'Seggi': 2}, ignore_index=True)
    else:
        toReturn = toReturn.append({'Coalizione': sorted_df.iloc[0]['Coalizione'], 'Partito': sorted_df.iloc[0]['Partito'], 'Voti': sorted_df.iloc[0]['Voti'], 'Seggi': 2}, ignore_index=True)

    return toReturn

def show_binomiale_chart(result):
    df = pd.DataFrame(result, columns = ['Circoscrizione', 'Class', 'Partito', 'Seggi'])
    df = df.append({'Partito': "", 'Seggi': df['Seggi'].sum()}, ignore_index=True)

    df_res = df.groupby(['Partito']).sum().reset_index()
    base_colors = ['white', 'red', 'yellow', 'blue', 'grey', 'orange', 'violet', 'pink', 'green', 'black', 'lime', 'turquoise']
    
    df_res['Seggi'] = df_res['Seggi'].astype(int)
    df_res['Percentuali'] = round(df_res['Seggi'] / (df_res['Seggi'].sum() / 2), 5)   
    df_res = df_res.sort_values(['Seggi'], ascending = False)

    total_lists = df_res['Partito'].count()

    labels = []
    for index, row in df_res.iterrows():
        if row['Partito'] == "":
            labels.append("")
        else:
            labels.append("{:.2f}% ({:d} seats)".format(row['Percentuali'] * 100, row['Seggi']))
    
    fig, ax = plt.subplots(figsize=(15, 9), subplot_kw=dict(aspect="equal"))

    data = df_res['Seggi']
    partiti = df_res['Partito']
    colors = base_colors[0:total_lists]

    wedges, texts = ax.pie(data, labels = labels, labeldistance = 1.05,counterclock=False,
                                      textprops=dict(color="black"), colors = colors, explode = None)
    ax.legend((wedges[1::]), (partiti[1::]),
              title="Coalizione/Partito",
              loc="upper left",
              bbox_to_anchor=(1.01, 0.08, 0.5, 1))

    plt.setp(texts, size=4, weight="bold")

    ax.set_title("Distribuzione Nazionale Camera dei Deputati 2013 con Legge Binomiale", loc='left')
    ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))

    plt.rcParams['figure.dpi'] = 300

    ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))

    plt.show()
