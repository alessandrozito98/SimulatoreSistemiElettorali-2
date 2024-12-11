# Nazione
La classe Nazione rappresenta l'entità principale per la gestione e la simulazione delle elezioni a livello nazionale secondo il sistema elettorale del Rosatellum, che combina l'assegnazione di seggi in modo proporzionale e uninominale. La gestione comprende la suddivisione in circoscrizioni, l'assegnazione dei seggi e le operazioni di distribuzione e correzione dei seggi.
## Metaclasses 
```yaml
metaclasses:
  - external
  - superdivision
  - totals
  - lanes
  ```
La classe Nazione utilizza le seguenti metaclassi per definire il suo comportamento e le sue funzionalità:

+ external: Permette di gestire gli attributi di input/output che possono essere inizializzati tramite parametri esterni o configurazioni specifiche.
+ superdivision: Specifica che la classe ha una suddivisione gerarchica, in questo caso in circoscrizioni, e consente di definire funzioni per interagire con le sottodivisioni.
+ totals: Fornisce la possibilità di definire funzioni di aggregazione e calcolo su data frame di dati, utili per raccogliere e sommare risultati elettorali.
+ lanes: Rappresenta la gestione delle "lanes" di distribuzione dei seggi, permettendo la gestione del flusso di distribuzione e la propagazione delle informazioni tra livelli gerarchici.


## External

```yaml
external:
  totale_seggi_plurinominale:
    init: True
    type: int
  circoscrizioni:
    init: True
```
La classe Nazione ha i seguenti attributi external:

+ totale_seggi_plurinominale: Rappresenta il numero totale di seggi proporzionali da distribuire a livello nazionale. Questo attributo è inizializzato al momento della creazione dell'istanza e specifica il numero di seggi da distribuire nelle varie circoscrizioni.
+ circoscrizioni: Rappresenta l'elenco delle circoscrizioni elettorali presenti nella nazione. Questo attributo viene inizializzato al momento della creazione dell'istanza.

L'uso del prefisso self.get_ permette di accedere a questi attributi in modo strutturato all'interno delle funzioni di configurazione e distribuzione.

## Subdivisions
```yaml
subdivisions:
  circoscrizioni:
    type: Circoscrizione
    functions:
      - name: get_risultati
        source:
          type: fun
          name: self.get_risultati
```

La classe Nazione è suddivisa in circoscrizioni, che sono rappresentate da un attributo chiamato circoscrizioni di tipo Circoscrizione.

La funzione get_risultati della classe Circoscrizione è esposta in modo che possa essere richiamata dalla classe Nazione tramite il nome subs_circoscrizioni_get_risultati. Ciò consente a Nazione di ottenere i risultati aggregati dalle varie circoscrizioni per effettuare calcoli e distribuzioni a livello nazionale.

## Totals
```yaml
totals:
  aggrega_risultati_circoscrizioni:
    type: aggregate
    source:
      type: fun
      name: self.subs_circoscrizioni_get_risultati
    keys:
      - Partito
      - Coalizione
    ops:
      Voti: sum
      Cifra: sum
```
La funzione totals aggrega_risultati_circoscrizioni esegue un'aggregazione a livello nazionale dei risultati delle circoscrizioni:

+ Type: aggregate indica che si tratta di un'operazione di aggregazione.
+ Source: Utilizza la funzione subs_circoscrizioni_get_risultati per ottenere i dati aggregati dalle circoscrizioni.
+ Keys: L'aggregazione avviene per Partito e Coalizione.
+ Ops: Vengono eseguite operazioni di somma (sum) sulle colonne Voti e Cifra.

Questa funzione consente di ottenere un DataFrame con i risultati complessivi per partito e coalizione a livello nazionale.

## Totals_Support
```yaml
totals_support:
  assegna_seggi_nazione:
    source:
      totals: aggrega_risultati_circoscrizioni
      args:
        - soglia
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.distribuzione_hare_nazionale
          kwargs:
            seggi_totali:
              source:
                type: fun
                name: self.get_totale_seggi_plurinominale
```

La funzione totals_support assegna_seggi_nazione utilizza i risultati aggregati delle circoscrizioni per calcolare la distribuzione dei seggi a livello nazionale:

+ Source: Prende come input i risultati aggregati aggrega_risultati_circoscrizioni e applica una soglia di sbarramento.
+ Type: transform indica che si tratta di una trasformazione dei dati.
+ Ops: La trasformazione è effettuata tramite la funzione Commons.distribuzione_hare_nazionale, che utilizza il metodo Hare per la distribuzione proporzionale dei seggi.
+ Kwargs: Il numero totale di seggi da distribuire è determinato dall'attributo totale_seggi_plurinominale.

Il risultato è un DataFrame del tipo |Partito|Seggi| che rappresenta la distribuzione dei seggi per ogni partito a livello nazionale.

## Lane_Propose
```yaml
lanes_propose:
  seggi_nazionali:
    source:
      type: fun
      name: self.assegna_seggi_nazione
    distribution:
      - Partito
      - Seggi
    info:
      - Voti
```
La funzione lane_propose seggi_nazionali genera una distribuzione dei seggi a livello nazionale:

+ Source: Chiama la funzione assegna_seggi_nazione per calcolare la distribuzione.
+ Distribution: La distribuzione risultante avrà le colonne Partito e Seggi.
+ Info: Include informazioni aggiuntive sui Voti.

Questa funzione consente di propagare i dati di distribuzione dei seggi a livello delle varie lane.

## Lane
```yaml
lane:
  plurinominale:
    node_type: head
    order_number: 2
    sub_level: Circoscrizione
    info_name: Nazione
    first_input: seggi_nazionali
    operations:
      - collect_type: seggi_circoscrizionali
        ideal_distribution: $
        corrector: Commons.correggi_distribuzione_locale
```
La classe Nazione definisce una lane denominata plurinominale con le seguenti caratteristiche:

+ Node Type: head indica che la lane è la testa di una sequenza di operazioni.
+ Order Number: Definisce la priorità nella sequenza delle lane.
+ Sub Level: Specifica che la suddivisione avviene a livello di circoscrizione.
+ First Input: La distribuzione iniziale viene calcolata con seggi_nazionali.
+ Operations: Effettua operazioni di raccolta e correzione sui seggi distribuiti a livello di circoscrizione utilizzando Commons.correggi_distribuzione_locale.