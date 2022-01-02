# Valle D'Aosta
Il file Valle_Aosta.yaml è il file di configurazione dell'entità Valle D'Aosta.

In questo file configureremo gli attributi che la Valle D'Aosta deve avere, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.

## Metaclasses

```yaml
metaclasses:
  - totals
  - lanes
  - external
```


---
## External
Qui definiamo quali parametri deve avere la Valle D'Aosta

```yaml
external:
  voti_valle_d_aosta:
    columns:
      - Partito
      - Voti
```

Valle D'Aosta ha il solo seguente attributo:
+ voti_valle_d_aosta: è la tabella dei voti della Valle D'Aosta, le cui colonne sono:
	-Partito
	-Voti
La tabella viene inizializzata tramite file [LeggiElettorali/Binomiale/Data/Valle_Aosta/voti_valle_d_aosta.csv]


---
## Totals
Qui definiamo delle funzioni di aggregazione, trasformazione e combinazioni di dati presi da dei dataframe pandas.

```yaml
totals:
  liste:
    type: aggregate
    source:
      type: fun
      name: self.valle_d_aosta
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

Il totals 'liste' ha questa configurazine :
- è di tipo aggregazione
- la sua input di dati è la funzione self.valle_d_aosta(vedere external per chiarimenti)
- ritorna un dataframe con le colonne | Seggi | Coalizione |
- aggrega i dati sulla chiave Coalizione
- sui dati aggregati esegue l'operazione sum sul campo Seggi



---
## Totals_support

```yaml
totals_support:
  valle_d_aosta:
    source:
      type: fun
      name: self.valle_d_aosta_coalizioni
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.calc_binomiale
  valle_d_aosta_coalizioni:
    # source:
    #   totals: liste
    source:
      type: fun
      name: self.get_voti_valle_d_aosta
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.fill_coalizione
```

Province avrà le seguenti funzioni totals_support chiambili:
+ valle_d_aosta: trasforma la funzione valle_d_aosta_coalizioni in un dataframe il cui valore di ritorno mi viene dato da calc_binomiale
+ valle_d_aosta_coalizioni: trasforma la funzione get_voti_valle_d_aosta in un dataframe il cui valore di ritorno mi viene dato da fill_coalizione

---
## Lane
Qui definiamo quali lanes ha l'entità Valle D'Aosta, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  valle_d_aosta:
    node_type: only
    order_number: 1
    # first_input: None
    distribution: binomiale
    info_name: valle_d_aosta
```

L'entità Valle D'Aosta avrà un lane con nome 'lista' così configurata:
- sarà di tipo 'only'
- avrà distribuonzione 'binomiale'
- il nome della lane è 'valle_d_aosta'


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

Valle D'Aosta ha le seguenti lanes_propose, funzioni che generano una distribuzione |PolEnt|Seggi|:
+ binomiale:
	-La dstribuzione generata avrà le colonne |Partito|Seggi| con i seggi assegnati nella circoscrizione.
	-Info avrà anche esso le colonne |Partito|Seggi|



