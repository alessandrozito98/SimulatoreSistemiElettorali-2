## Partito
La classe Partito rappresenta un'entità politica e gestisce la logica di filtraggio dei partiti in base alle soglie di sbarramento nazionali e di coalizione.

## Configurazione della Metaclasse
La classe Partito viene inizializzata tramite una configurazione YAML che definisce le metaclassi e le sottoclassi utilizzate per l'implementazione del comportamento.

Esempio di configurazione YAML
```yaml
metaclasses:
  - logger
  - PolEnt
  - party

subclass:
  - PolEnt
  ```
  
+ logger: Gestisce la registrazione degli eventi.
+ PolEnt: Definisce il comportamento di un'entità politica.
+ party: Aggiunge funzionalità specifiche per i partiti.

La configurazione viene caricata utilizzando yaml.safe_load(conf) e le metaclassi vengono create dinamicamente.

## Costanti di Classe
La classe definisce due costanti per le soglie di sbarramento:

+ SOGLIA_PARTITO: Soglia di sbarramento per i singoli partiti, definita come 0.03 (3%).
+ SOGLIA_COALIZIONE: Soglia di sbarramento per le coalizioni, definita come 0.10 (10%).
## Metodo di Filtraggio
filter
```python
def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs):
    if sbarramenti[0] == 'soglia' and district.type == 'Nazione':
        tot_voti = dataframe['Voti'].sum()
        p_voti = row['Voti']
        # Verifica se il partito è parte di una coalizione
        coalizione = row.get('Coalizione')
        if coalizione:
            # Somma i voti dei partiti appartenenti alla stessa coalizione
            voti_coalizione = dataframe[dataframe['Coalizione'] == coalizione]['Voti'].sum()
            return voti_coalizione >= tot_voti * self.SOGLIA_COALIZIONE
        else:
            return p_voti >= tot_voti * self.SOGLIA_PARTITO
    return True
```
    
Il metodo filter applica le soglie di sbarramento per determinare se un partito o una coalizione può accedere alla distribuzione dei seggi.

Parametri:
+ district: Rappresenta il distretto (es. nazionale o locale).
+ total: Il totale dei voti (non usato direttamente nel metodo).
+ row: Una riga del dataframe contenente i dettagli del partito.
+ dataframe: Un DataFrame contenente i dati di tutti i partiti e le loro coalizioni.
+ sbarramenti: Lista di soglie da applicare, es. ['soglia'].
+ kwargs: Parametri aggiuntivi opzionali.

Funzionamento:
+ Se il filtro riguarda una soglia e il distretto è di tipo "Nazione":
  + Calcola il totale dei voti.
  + Controlla se il partito fa parte di una coalizione:
    + Se sì, somma i voti di tutti i partiti della stessa coalizione e verifica se raggiunge la SOGLIA_COALIZIONE.
    + Se no, verifica se i voti del partito raggiungono la SOGLIA_PARTITO.
  + Se non sono applicabili le condizioni di soglia, il metodo restituisce True