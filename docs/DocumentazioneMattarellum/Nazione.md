# Nazione
Questa classe rappresenta la nazione.


## Metaclasses 

```yaml
metaclasses:
  - external
  - superdivision
  - totals
  - lanes
```

Nazione eredita da:
+ external, per rappresentare i suoi attributi
+ superdivision, per rappresentare la divisione in circoscrizioni
+ totals, per poter avere delle funzioni totals di manipolazione dei dataframe
+ lanes, perché fa parte di almeno una lane



## External

```yaml
external:
  totale_seggi_plurinominale:
    init: True
    type: int
  circoscrizioni:
    init: True
```

Nazione ha i seguenti attributi:
+ totale_seggi_plurinominale: viene inizializzato tramite file di configurazione delle istanze
+ circoscrizioni: viene inizializzato tramite file di configurazione delle istanze


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

Nazione è divisa in cirscoscrizioni, contenute nell'attributo circoscrizioni. Espongo la funzione get_risultati di Circoscrizione , che si chiamerà Nazione.subs_circoscrizioni_get_risultati.


## Totals

```yaml 
totals:
    #restituisce |Partito|Voti|Cifra| a liv. nazionale
  aggrega_risultati_circoscrizioni: 
    type: aggregate
    source:
      type: fun
      name: self.subs_circoscrizioni_get_risultati
    keys:
      - Partito
    ops:
      Voti: sum
      Cifra: sum
```

Nazione avrà le seguenti funzioni totals, chiamabili tramite totals(nome, *sbarramenti):
+ aggrega_risultati_circoscrizioni: per ogni circoscrizione chiama get_risultati e aggrega i risultati, ottenendo un dataframe del tipo |Partito|Voti|Cifra| con i risultati della quota proporzionale a livello nazionale già scorporati.


## Totals_support

```yaml
totals_support:  
  # - source: prende il risultato di aggrega_risultati_circoscrizioni e applica soglia sbarr
  # - ops: applica metodo dei quoz per ottenere df |Partito|Seggi| a liv. nazionale
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
          name: Commons.hare_mattarellum
          kwargs:
            seggi_totali:
              source:
                type: fun
                name: self.get_totale_seggi_plurinominale
```

Nazione avrà le seguenti funzioni totals_support, chiamabili tramite nome(...):
+ assegna_seggi_nazione: chiama il totals aggrega_risultati_circoscrizioni, applicandogli la soglia di sbarramento del 4%. Fatto ciò, passa questo risultato e totale_seggi_plurinominale alla funziona hare_mattarellum, che determina la distribuzione nazionale dei voti, che è un dataframe del tipo |Partito|Seggi|


## Lane propose

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

Nazione ha le seguenti lanes_propose, funzioni che generano una distribuzione |PolEnt|Seggi|:
+ seggi_nazionali: chiama la funzione assegna_seggi_nazione e, con il dataframe risultante, genera la distribuzione usando le colonne "Partito" e "Seggi" e inserisce la colonna "Voti" tra le informazioni da propagare.


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
        corrector: Commons.correggi_mattarellum
```

Nazione è la testa lane "plurinominale". 
La prima distribuzione generate è data dalla propose "seggi_nazionali", poi questa viene passata a tutte le circoscrizioni, che la usano per generare una propria distribuzione locale tramite la propose "seggi_circoscrizionali". Infine, queste distribuzioni locali verranno correte tramite correggi_mattarellum