import random
import re



def estrai_numero_comune(stringa):
    stringa.s
    # Usa una regex per trovare la parte desiderata
    match = re.search(r'U(\d{2}) \(([^:]+)', stringa)
    if match:
        # Estrai il numero e il nome
        numero = match.group(1)
        comune = match.group(2)
        risultato = f"{numero} - {comune}"
        return risultato
    else:
        # Se non corrisponde al formato previsto, restituisci None o un messaggio di errore
        return None

def partito_vincente_per_collegio(df):
    # Trova il partito con il numero massimo di voti in ogni collegio
    vincitori = df.loc[df.groupby('Collegio')['Voti'].idxmax()]
    # Seleziona solo le colonne rilevanti
    vincitori = vincitori[['Collegio', 'PartitoCollegato', 'Voti']]
    # Rinomina le colonne per chiarezza
    vincitori.rename(columns={'PartitoCollegato': 'PartitoVincente', 'Voti': 'VotiVincente'}, inplace=True)
    return vincitori

def formatta_collegio(input_string):
    # Usa una regex per estrarre il numero del collegio e il nome della città
    match = re.search(r'U(\d+)\s+\(([^:]+)', input_string)
    if match:
        numero_collegio = match.group(1).zfill(2)  # Aggiungi lo zero iniziale se necessario
        citta = match.group(2).strip()
        citta.replace(")","")
        return f"{numero_collegio} - {citta}"
    else:
        return "Formato non valido"

def scegli_partitoD():
    partiti = ['FRATELLI D\'ITALIA CON GIORGIA MELONI', 'LEGA PER SALVINI PREMIER', 'FORZA ITALIA']
    probabilita = [0.60, 0.21, 0.19]  # Percentuali convertite in probabilità

    # Seleziona un partito basato sulle probabilità specificate
    return random.choices(partiti, probabilita)[0]

def scegli_partitoS():
    partiti = ['PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA', 'ALLEANZA VERDI E SINISTRA']
    probabilita = [0.84, 0.16]  # Percentuali convertite in probabilità

    # Seleziona un partito basato sulle probabilità specificate
    return random.choices(partiti, probabilita)[0]

def trova_partito_maggiore_per_collegio(dizionario):
    risultati = {}
    with open('../Data/Collegio/voti_uninominale.csv', 'w') as file:
        file.write(f"Collegio,Candidato,Lista,Partito,PartitoCollegato,Voti\n")
        for chiave, voti in dizionario.items():
            collegio = chiave[0]
            partito = chiave[1]
            coalizione = chiave[2]
            candidato = chiave[3]
        # Se il collegio non è ancora nel dizionario risultati, o se il numero di voti è maggiore
        # rispetto a quello già registrato, aggiorna il dizionario
        if collegio not in risultati:
            risultati[collegio] = (candidato,coalizione,partito,partito,voti)

        if voti > risultati[collegio][4]:
            risultati[collegio] = (candidato,coalizione,partito,partito,voti)
            
            for collegio, (candidato, coalizione, partito, partito, voti) in risultati.items():
                file.write(f"{collegio},{candidato},{coalizione},{partito},{partito},{voti}\n")
        # Scrive i risultati su file

def stampa(dizionario):
    risultati = {}
    with open('../Data/Collegio/voti_uninominale.csv', 'w') as file:
        file.write(f"Collegio,Candidato,Coalizione,Lista,Partito,Voti\n")
        for chiave, voti in dizionario.items():
            collegio = chiave[0]
            partito = chiave[1]
            coalizione = chiave[2]
            candidato = chiave[3]
            file.write(f"{collegio},{candidato},{coalizione},{partito},{partito},{voti}\n")

# Funzione per assegnare coalizione CDX o CSX a seconda della lista del partito
def assegna_coalizione(row):
    descrlista = row.strip('"')
    if descrlista in cdx:
        return 'CDX'  # Assegna 'CDX' se il partito appartiene al centro-destra
    elif descrlista in csx:
        return 'CSX'  # Assegna 'CSX' se il partito appartiene al centro-sinistra
    else:
        return descrlista # Mantieni il nome del partito se non appartiene a CDX o CSX

# Definisci i partiti appartenenti alle coalizioni di centro-destra (CDX) e centro-sinistra (CSX)
cdx = ['FORZA ITALIA', "FRATELLI D'ITALIA CON GIORGIA MELONI", 'LEGA PER SALVINI PREMIER', 'NOI MODERATI/LUPI - TOTI - BRUGNARO - UDC']
csx = ['PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA', 'ALLEANZA VERDI E SINISTRA', '+EUROPA', 'IMPEGNO CIVICO LUIGI DI MAIO - CENTRO DEMOCRATICO']

dizionario = {}
coalizionetemp = ""
# Carica i dati dal file 'cameraitalia.txt'
with open('cameraitalia.txt', 'r') as file:
    next(file)
    # Leggi il file riga per riga
    for linea in file:
        campi = linea.split(';')
        collegio = formatta_collegio(campi[4].strip('"'))
        partito = campi[12]
        cognome = campi[13].strip('"')
        nome = campi[14].strip('"')
        candidato = cognome +' '+ nome
        votint = campi[18].strip()
        voti = int(votint.strip('"'))
        coalizione = assegna_coalizione(partito)
        chiave = (collegio,'x', coalizione , candidato)
        if(chiave not in dizionario.keys()):
            dizionario[chiave] = voti
            coalizionetemp = coalizione
        if (chiave in dizionario.keys() and coalizionetemp != coalizione):
            dizionario[chiave] = dizionario[chiave] + voti
            coalizionetemp = coalizione
dizionario2 = {}
for chiave, valore in dizionario.items():
    # Crea la nuova chiave sostituendo 'x' con il nome del partito
    if chiave[2] == 'CDX':
        partito = scegli_partitoD()
    # Azione se la condizione è vera
    elif chiave[2] == 'CSX':
        partito = scegli_partitoS()
    # Azione se la prima condizione è falsa e questa è vera
    else:
        partito = chiave[2]
    nuova_chiave = (chiave[0].replace(")", ""), partito, chiave[2],chiave[3])
    # Aggiungi l'elemento al nuovo dizionario
    dizionario2[nuova_chiave] = valore
    stampa(dizionario2)

"""""
with open('dizionario2.txt', 'w') as file:
    for chiave, valore in dizionario2.items():
            file.write(f'{chiave}:{valore}\n')

"""""