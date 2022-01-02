# Collegio
Questa classe rappresenta un collegio uninominale.

## Metaclasses

```yaml
metaclasses:
  - external
  - totals
  - lanes
```

Collegio eredita da:
+ external, per rappresentare i suoi attributi
+ totals, per poter avere delle funzioni totals di manipolazione dei dataframe
+ lanes, perché fa parte di almeno una lane


## External

```yaml
external:
  voti_uninominale:
    columns:
      - Candidato
      - Lista
      - Partito
      - PartitoCollegato
      - Voti
```

Collegio ha i seguenti attributi:
+ voti_uninominale: è la tabella dei voti del Collegio, viene inizializzato tramite file /LeggiElettorali/Mattarellum/Data/Collegio/voti_uninominale.csv


## Totals_support

```yaml
totals_support:
  get_vincente_uninominale:
    source:
      type: fun
      name: self.get_voti_uninominale
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.select_vincente_mattarellum
```

Collegio avrà le seguenti funzioni totals_support, chiamabili tramite nome(...):
+ get_vincente_uninominale: passa voti_uninominale alla funzione select_vincente_mattarellum, che determina il partito collegato al vincitore del collegio e il numero di seggi da scorporare. Restituisce un dataframe del tipo |PartitoCollegato|VotiVincenti| con una singola riga.


## Lanes_propose

```yaml
lanes_propose:
  seggi_collegiali:
    source:
      type: fun
      name: self.get_voti_uninominale

    distribution:
      key: Partito
      seats: 1
      selector:
              column: Voti
              order: decreasing
              take: 1
    info:
      - Voti
```

Collegio ha le seguenti lanes_propose, funzioni che generano una distribuzione |PolEnt|Seggi|:
+ seggi_collegiali: partendo da voti_uninominale, ordina per Voti decrescenti e assegna l'unico seggio del collegio al "Partito" del candidato che ha avuto più seggi


## Lane

```yaml
lane:
  uninominale:
    node_type: only
    order_number: 1
    distribution: seggi_collegiali
    info_name: Collegio
```

Collegio è l'unico nodo della lane "uninominale". La distribuzione dei seggi viene generata dalla propose "seggi_collegiali".