
def estrai_circoscrizione(circoscrizione):
    """
    Estrae la regione dalla stringa della circoscrizione.

    Parameters
    ----------
    circoscrizione : str
        La stringa della circoscrizione nel formato "REGIONE - CODICE".

    Returns
    -------
    str
        La parte della stringa che rappresenta la regione.
    """
    return circoscrizione.split(' - ')[0]

# Definisci i partiti appartenenti alle coalizioni di centro-destra (CDX) e centro-sinistra (CSX)
cdx = ['FORZA ITALIA', "FRATELLI D'ITALIA CON GIORGIA MELONI", 'LEGA PER SALVINI PREMIER', 'NOI MODERATI/LUPI - TOTI - BRUGNARO - UDC']
csx = ['PARTITO DEMOCRATICO - ITALIA DEMOCRATICA E PROGRESSISTA', 'ALLEANZA VERDI E SINISTRA', '+EUROPA', 'IMPEGNO CIVICO LUIGI DI MAIO - CENTRO DEMOCRATICO']

def stampa(circoscrizioni):
    risultati = {}
    with open('../Data/Circoscrizione/voti_plurinominale.csv', 'w') as file:
        file.write(f"Circoscrizione,Coalizione,Partito,Voti\n")
        for chiave, voti in circoscrizioni.items():
            circoscrizione = chiave[0]
            coalizione = chiave[1]
            partito = chiave[2]
            file.write(f"{circoscrizione},{coalizione},{partito},{voti}\n")

def assegna_coalizione(row):
    descrlista = row.strip('"')
    if descrlista in cdx:
        return 'CDX'  # Assegna 'CDX' se il partito appartiene al centro-destra
    elif descrlista in csx:
        return 'CSX'  # Assegna 'CSX' se il partito appartiene al centro-sinistra
    else:
        return descrlista # Mantieni il nome del partito se non appartiene a CDX o CSX

dizionario = {}
with open('cameraitalia.txt', 'r') as file:
    next(file)
    # Leggi il file riga per riga
    for linea in file:
        campi = linea.split(';')
        if campi[3] == "" or campi[3] is None:
            continue
        circoscizione = estrai_circoscrizione(campi[3].strip('"'))
        partito = campi[12]
        coalizione = assegna_coalizione(campi[12])
        votint = campi[11].strip()
        voti = int(votint.strip('"'))
        chiave = (circoscizione, coalizione, partito)
        if(chiave not in dizionario.keys()):
            dizionario[chiave] = voti
            partitotemp = partito
        if (chiave in dizionario.keys() and partitotemp != partito):
            dizionario[chiave] = dizionario[chiave] + voti
            partitotemp = partito
stampa(dizionario)


