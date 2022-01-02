# Circoscrizione Estera

Il file Circoscrizione_Estera.yaml è il file di configurazione dell'entità Circoscrizione Estera.

In questo file configureremo gli attributi che la Circoscrizione Estera deve avere, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.


---
## Metaclasses

```yaml
metaclasses:
  - totals
  - lanes
  - external
```


---
## External

Qui definiamo quali parametri deve avere la Circoscrizione

```yaml
external:
  voti_estero:
    columns:
      - Partito
      - Voti
      - Coalizione
```

Cirscoscrizione ha il solo seguente attributo:
+ voti_estero: è la tabella dei voti della Circoscrizione Estera, le cui colonne sono:
	-Partito
	-Voti
	-Coalizione
La tabella viene inizializzata tramite file [LeggiElettorali/Binomiale/Data/Circoscrizione_Estera/voti_estero.csv]


---
## Totals

```yaml
totals:
  liste:
    type: aggregate
    source:
      type: fun
      name: self.estero
    rename:
      Coalizione: Partito
    columns:
        - Seggi
        - Coalizione
    keys:
      - Coalizione
    ops:
      Seggi: sum
```

Il totals 'liste' ha questa configurazione:
- è di tipo aggregazione
- il suo input di dati è la funzione self.estero(vedere external per chiarimenti)
- ritorna un dataframe con le colonne |Seggi|Coalizione|
- aggrega i dati sulla chiave Coalizione
- sui dati aggregati esegue l'operazione sum sul campo Seggi

---
## Totals Support

```yaml
totals_support:
  estero:
    source:
      type: fun
      name: self.estero_coalizioni
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.calc_binomiale
  estero_coalizioni:
    # source:
    #   totals: liste
    source:
      type: fun
      name: self.get_voti_estero
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.fill_coalizione
```

Circoscrizione Estera avrà le seguenti funzioni totals_support chiamabili:
+ estero: trasforma la funzione estero_coalizioni in un dataframe il cui valore di ritorno mi viene dato da calc_binomiale
+ estero_coalizioni: trasforma la funzione get_voti_estero in un dataframe il cui valore di ritorno mi viene dato da fill_coalizione


---
## Lane

Qui definiamo quali lanes ha l'entità Circoscrizione Estera, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  estero:
    node_type: only
    order_number: 1
    # first_input: None
    distribution: binomiale
    info_name: Estero
```

L'entità Circoscrizione avrà un lane con nome 'lista' così configurata:
- sarà di tipo 'only'
- avrà distribuzione 'binomiale'
- il nome della lane è 'Estero'


---
## Lane propose

Qui definiamo quale funzione chiamare per generare la distribuzione, quali campi deve avere la distribuzione quando viene restituita e quali campi deve avere info quando viene restituito.


```yaml
lanes_propose:

  binomiale:
    source:
      totals: liste
    distribution:
      - Partito
      - Seggi
    info:
      - Partito
      - Seggi
```
Circoscrizione Estera ha le seguenti lanes_propose, funzioni che generano una distribuzione |PolEnt|Seggi|:
+ binomiale:
	-La distribuzione generata avrà le colonne |Partito|Seggi| con i seggi assegnati nella circoscrizione.
	-Info avrà anche esso le colonne |Partito|Seggi|



