# Province
Il file Province.yaml è il file di configurazione dell'entità Province.

In questo file configureremo gli attributi che la Province deve avere, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.


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
Qui definiamo quali parametri deve avere la Provincia

```yaml
external:
  voti_province:
    columns:
      - Partito
      - Voti
      - Coalizione
```
Cirscoscrizione ha il solo seguente attributo:
+ voti_province: è la tabella dei voti della provincia, le cui colonne sono:
	-Partito
	-Voti
	-Coalizione
La tabella viene inizializzata tramite file [LeggiElettorali/Binomiale/Data/Province/voti_province.csv]


---
## Totals
Qui definiamo delle funzioni di aggregazione, trasformazione e combinazioni di dati presi da dei dataframe pandas.

```yaml
totals:
  liste:
    type: aggregate
    source:
      type: fun
      name: self.province
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
- la sua input di dati è la funzione sself.province(vedere external per chiarimenti)
- ritorna un dataframe con le colonne |Seggi|Coalizione|
- aggrega i dati sulla chiave Coalizione
- sui dati aggregati esegue l'operazione sum sul campo Seggi

---
## Totals_support

```yaml
totals_support:
  province:
    source:
      type: fun
      name: self.province_coalizioni
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.calc_binomiale
  province_coalizioni:
    # source:
    #   totals: liste
    source:
      type: fun
      name: self.get_voti_province
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.fill_coalizione
```

Province avrà le seguenti funzioni totals_support chiambili:
+ province: trasforma la funzione province_coalizioni in un dataframe il cui valore di ritorno mi viene dato da calc_binomiale
+ province_coalizioni: trasforma la funzione get_voti_province in un dataframe il cui valore di ritorno mi viene dato da fill_coalizione


---
## Lane
Qui definiamo quali lanes ha l'entità Provincia, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  province:
    node_type: only
    order_number: 1
    # first_input: None
    distribution: binomiale
    info_name: province
```
L'entità Circoscrizione avrà un lane con nome 'lista' così configurata:
- sarà di tipo 'only'
- avrà distribuonzione 'binomiale'
- il nome della lane è 'province'


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

La proposta 'binomiale' ha questa configurazine:
- chiamerà la funzione liste
- la distribuzione ritornata avrà le colonne |Partito|Seggi|
- info avrà le colonne |Partito|Seggi|




