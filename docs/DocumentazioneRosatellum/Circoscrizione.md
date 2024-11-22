## Circoscrizione
La classe Circoscrizione rappresenta una suddivisione elettorale intermedia della Nazione nel contesto del sistema elettorale Rosatellum. Gestisce l'aggregazione dei voti, la distribuzione dei seggi e l'interazione con i collegi elettorali associati.

## Metaclasses
```yaml
metaclasses:
  - external
  - superdivision
  - totals
  - lanes
  ```
La classe Circoscrizione eredita dalle seguenti metaclassi:

+ external: Permette la gestione degli attributi che possono essere inizializzati tramite configurazioni esterne o tramite input runtime.
+ superdivision: Definisce la struttura gerarchica con sottodivisioni (collegi), consentendo di definire e accedere alle funzioni delle suddivisioni.
+ totals: Fornisce funzionalità di aggregazione e calcolo dei dati elettorali a livello di circoscrizione.
+ lanes: Gestisce le "lanes" di distribuzione, permettendo il flusso di informazioni sui seggi assegnati e le propagazioni a livello locale.
## External
```yaml
  seggi_plurinominale:
    init: True
  collegi:
    init: True
  voti_plurinominale:
    columns:
      - Partito
      - Coalizione
      - Voti
```
Gli attributi external della classe Circoscrizione sono:

+ seggi_plurinominale: Numero di seggi proporzionali assegnati alla circoscrizione. Inizializzato tramite il file di configurazione delle istanze.
+ collegi: Elenco dei collegi elettorali appartenenti alla circoscrizione. Inizializzato tramite il file di configurazione delle istanze.
+ voti_plurinominale: DataFrame che rappresenta i voti espressi per ogni partito e coalizione nella circoscrizione. Contiene le colonne Partito, Coalizione e Voti.
## Subdivisions
```yaml
subdivisions:
  collegi:
    type: Collegio
    functions:
      - name: get_vincente_uninominale
        source:
          type: fun
          name: self.get_vincente_uninominale
```
La classe Circoscrizione è suddivisa in collegi, definiti dal tipo Collegio.

+ get_vincente_uninominale: Espone la funzione di Collegio per determinare il vincitore del seggio uninominale. Può essere richiamata tramite self.subs_collegi_get_vincente_uninominale.
## Totals
```yaml
totals:
  aggrega_vincenti_collegi:
    type: aggregate
    source:
      type: fun
      name: self.subs_collegi_get_vincente_uninominale
    keys:
      - Partito
      - Coalizione
    ops:
      VotiVincenti: sum
```
La funzione totals aggrega_vincenti_collegi esegue l'aggregazione dei voti vincenti dei collegi:

+ Type: aggregate indica un'operazione di aggregazione.
+ Source: Utilizza la funzione self.subs_collegi_get_vincente_uninominale per ottenere i dati di voto dai collegi.
+ Keys: L'aggregazione avviene per Partito e Coalizione.
+ Ops: Somma il totale dei voti vincenti (VotiVincenti).
## Totals_Support
```yaml
totals_support:
  get_risultati:
    source:
      totals: aggrega_vincenti_collegi
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.unisci_voti_maggioritario_proporzionale
          kwargs:
            voti_proporzionale:
              source:
                type: fun
                name: self.get_voti_plurinominale
```
La funzione totals_support get_risultati unisce i risultati elettorali maggioritari e proporzionali:

+ Source: Utilizza totals aggrega_vincenti_collegi per ottenere i voti aggregati.
+ Type: transform indica una trasformazione dei dati.
+ Ops: Passa il risultato a Commons.unisci_voti_maggioritario_proporzionale, che combina i voti maggioritari e proporzionali per calcolare la cifra elettorale della circoscrizione.
## Lane Propose
```yaml
lanes_propose:
  seggi_circoscrizionali:
    source:
      type: fun
      name: Commons.distribuzione_seggi_circoscrizionali
      kwargs:
        district_votes:
          source:
            type: fun
            name: self.get_risultati
        seggi_circoscrizione:
          source:
            type: fun
            name: self.get_seggi_plurinominale
    distribution:
      - Partito
      - Seggi
    info:
      - Coalizione
      - Resto
      - SeggiCircoscrizione
```
La funzione lane_propose seggi_circoscrizionali genera la distribuzione dei seggi a livello di circoscrizione:

+ Source: Chiama Commons.distribuzione_seggi_circoscrizionali con i risultati della circoscrizione e il numero di seggi da distribuire.
+ Distribution: La distribuzione generata avrà le colonne Partito e Seggi.
+ Info: Include informazioni aggiuntive come Coalizione, Resto e SeggiCircoscrizione.
## Lane
```yaml
lane:
  plurinominale:
    node_type: tail
    info_name: Circoscrizione
```
La classe Circoscrizione definisce una lane denominata plurinominale con le seguenti caratteristiche:

+ Node Type: tail indica che questa è la coda di una sequenza di operazioni.
+ Info Name: Specifica che la distribuzione è a livello di Circoscrizione.