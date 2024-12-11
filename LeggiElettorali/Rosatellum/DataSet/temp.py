import pandas as pd

# Carica il file CSV
data = pd.read_csv('voti_plurinominale.csv')  # Sostituisci con il tuo file

# Calcola la somma dei voti per ogni partito
somma_voti = data.groupby(['Coalizione', 'Partito'])['Voti'].sum().reset_index()

# Calcola il totale dei voti
totale_voti = somma_voti['Voti'].sum()

# Calcola la percentuale dei voti per ciascun partito
somma_voti['Percentuale'] = somma_voti['Voti'] / totale_voti

# Filtra i partiti che raggiungono almeno il 3% dei voti totali
somma_voti = somma_voti[somma_voti['Percentuale'] >= 0.03].reset_index(drop=True)

x= somma_voti['Voti'].sum()
print(x)
# Salva il risultato intermedio (opzionale)
somma_voti.to_csv('somma_voti_filtrato.csv', index=False)

# Numero di seggi totali da distribuire
seggi_totali = 245  # Imposta il numero di seggi desiderato

# Funzione per distribuire i seggi usando il metodo Hare
def distribuzione_hare(data, seggi_totali):
    # Calcola il quoziente Hare
    quoziente_hare = data['Voti'].sum() / seggi_totali
    print(f"Totale voti considerati: {data['Voti'].sum()}")
    print(f"Quoziente Hare: {quoziente_hare}")

    # Assegna i seggi interi a ciascun partito
    data['Seggi'] = (data['Voti'] / quoziente_hare).astype(int)

    # Calcola il resto per ciascun partito
    data['Resto'] = data['Voti'] - (data['Seggi'] * quoziente_hare)

    # Calcola i seggi rimanenti
    seggi_assegnati = data['Seggi'].sum()
    seggi_rimanenti = seggi_totali - seggi_assegnati

    # Assegna i seggi rimanenti ai partiti con i maggiori resti
    data = data.sort_values(by='Resto', ascending=False)
    data.iloc[:seggi_rimanenti, data.columns.get_loc('Seggi')] += 1

    # Riordina e seleziona le colonne richieste
    data = data.sort_index()
    return data[['Coalizione', 'Partito', 'Voti', 'Seggi', 'Resto']]

# Applica la funzione al DataFrame somma_voti filtrato
risultato = distribuzione_hare(somma_voti, seggi_totali)

# Salva il risultato finale
risultato.to_csv('risultato.csv', index=False)
