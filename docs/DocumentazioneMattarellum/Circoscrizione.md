# Circoscrizione
Questa classe rappresenta una circoscrizione plurinominale.

## Metaclasses

```yaml
metaclasses:
  - external
  - superdivision
  - totals
  - lanes
```
Circoscrizione eredita da:
+ external, per rappresentare i suoi attributi
+ superdivision, per rappresentare la divisione in circoscrizioni
+ totals, per poter avere delle funzioni totals di manipolazione dei dataframe
+ lanes, perché fa parte di almeno una lane

## External

```yaml
external:
  seggi_plurinominale:
    init: True
  collegi:
    init: True
  voti_plurinominale:
    columns:
      - Partito
      - Voti
```

Circoscrizione ha i seguenti attributi:
+ seggi_plurinominale: è il numero di seggi assegnati in quella circoscrizione nella quota proporzionale, viene inizializzato tramite il file di configurazione delle istanze
+ collegi: viene inizializzato tramite il file di configurazione delle istanze
+ voti_plurinominale: è la tabella dei voti della Circoscrizione, viene inizializzato tramite file /LeggiElettorali/Mattarellum/Data/Circoscrizione/voti_plurinominale.csv


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

Circoscrizione è divisa in collegi, contenuti nell'attributo collegi. Espongo la funzione get_vincente_uninominale di Collegio , che si chiamerà Circoscrizione.subs_collegi_get_vincente_uninominale.


## Totals

```yaml
totals:
  aggrega_vincenti_collegi: #restituisce |PartitoCollegato|VotiVincenti| a liv. di circoscrizione
    type: aggregate
    source:
      type: fun
      name: self.subs_collegi_get_vincente_uninominale
    keys:
      - PartitoCollegato
    ops:
      VotiVincenti: sum
```

Circoscrizione avrà le seguenti funzioni totals, chiamabili tramite totals(nome, *sbarramenti):
+ aggrega_vincenti_collegio: per ogni circoscrizione chiama get_vincente_collegio e aggrega i risultati, ottenendo un dataframe del tipo |PartitoCollegato|VotiVincenti|, che contiene il numero di voti da scorporare ad ogni partito a livello di circoscrizione


## Totals_support

```yaml
totals_support:
  get_risultati: # deve restituire |Partito|Voti|Cifra| a liv. di circoscrizione
    source: 
      totals: aggrega_vincenti_collegi
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.merge_votivincenti_mattarellum
          kwargs:
            voti_proporzionale:
              source:
                type: fun
                name: self.get_voti_plurinominale
```

Circoscrizione avrà le seguenti funzioni totals_support, chiamabili tramite nome(...):
+ get_risultati: chiama il totals aggrega_vincenti_collegi. Fatto ciò, passa questo risultato e voti_plurinominale alla funzione merge_votivincenti_mattarellum, che determina la cifra elettorale circoscrizionale dei partiti e restituisce un dataframe del tipo |Partito|Voti|Cifra| con i dati della circoscrizione.


## Lane propose

```yaml
lanes_propose:
  seggi_circoscrizionali:
    source:              
      type: fun                         
      name: Commons.assegna_seggi_circoscrizione_mattarellum 
      kwargs:
        district_votes:
          source:
            type: fun
            name: self.get_risultati # da |Partito|Voti|Cifra| a livello di circoscrizione
        seggi_circoscrizione:
          source:
            type: fun
            name: self.get_seggi_plurinominale
    distribution:
      - Partito
      - Seggi
    info: 
      - Resto
      - SeggiCircoscrizione
```

Circoscrizione ha le seguenti lanes_propose, funzioni che generano una distribuzione |PolEnt|Seggi|:
+ seggi_circoscrizionali: chiama la funzione assegna_seggi_circoscrizione_mattarellum, passandogli i risultati della circoscrizione (|Partito|Voti|Cifra|) e il numero di seggi da assegnare nella circoscrizione. Genera una distribuzione |Partito|Seggi| con i seggi assegnati sicuramente nella circoscrizione, mentre mette |Resto|SeggiCircoscrizione| nelle info da propagare.


## Lane

```yaml
lane:
  plurinominale:
    node_type: tail
    info_name: Circoscrizione
```

Circoscrizione è la coda della lane "plurinominale".