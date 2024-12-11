import pandas as pd

# Carica i file nei rispettivi dataframe
file1_path = 'Camera_VAosta_LivComune.txt'
file2_path = 'camera_italia_senzaVA.txt'

# Specifica il separatore come ";" e imposta le colonne
df1 = pd.read_csv(file1_path, delimiter=';')
df2 = pd.read_csv(file2_path, delimiter=';')

# Visualizza le colonne di riferimento del secondo file per adattare il formato del primo file
columns = [
    "DATAELEZIONE", "CODTIPOELEZIONE", "CIRC-REG", "COLLPLURI", "COLLUNINOM", "COMUNE",
    "ELETTORITOT", "ELETTORIM", "VOTANTITOT", "VOTANTIM", "SKBIANCHE", "VOTILISTA",
    "DESCRLISTA", "COGNOME", "NOME", "LUOGONASCITA", "DATANASCITA", "SESSO", "VOTICANDIDATO"
]

# Modifica il dataframe del primo file per adattarlo al formato del secondo
df1_adattato = pd.DataFrame(columns=columns)

# Mappatura dei dati del primo file al formato del secondo file
df1_adattato["DATAELEZIONE"] = df1["DATAELEZIONE"]
df1_adattato["CODTIPOELEZIONE"] = df1["CODTIPOELEZIONE"]
df1_adattato["CIRC-REG"] = "VALLE D'AOSTA"  # Definisci un valore costante per "CIRC-REG"
df1_adattato["COLLPLURI"] = None  # Nessun collegio plurinominale specificato per questo caso
df1_adattato["COLLUNINOM"] = df1["COLLEGIO"]
df1_adattato["COMUNE"] = df1["COMUNE"]
df1_adattato["ELETTORITOT"] = None  # Dato mancante, imposta come None
df1_adattato["ELETTORIM"] = None  # Dato mancante, imposta come None
df1_adattato["VOTANTITOT"] = None  # Dato mancante, imposta come None
df1_adattato["VOTANTIM"] = None  # Dato mancante, imposta come None
df1_adattato["SKBIANCHE"] = None  # Dato mancante, imposta come None
df1_adattato["VOTILISTA"] = None  # Dato mancante, imposta come None
df1_adattato["DESCRLISTA"] = df1["CONTRASSEGNO"]
df1_adattato["COGNOME"] = df1["COGNOME"]
df1_adattato["NOME"] = df1["NOME"]
df1_adattato["LUOGONASCITA"] = df1["LUOGONASCITA"]
df1_adattato["DATANASCITA"] = df1["DATANASCITA"]
df1_adattato["SESSO"] = df1["SESSO"]
df1_adattato["VOTICANDIDATO"] = df1["TOTVOTI"]

# Unisci i due dataframe
df_unito = pd.concat([df2, df1_adattato], ignore_index=True)

# Salva il dataframe unito nel file CSV finale
output_file_path = 'cameraitalia.txt'
df_unito.to_csv(output_file_path, index=False, sep=';')

print(f"File unito salvato in {output_file_path}")
