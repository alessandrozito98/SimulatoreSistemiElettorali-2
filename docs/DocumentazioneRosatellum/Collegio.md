## Collegio
La classe Collegio rappresenta una suddivisione elettorale che gestisce i seggi uninominali, dove il candidato con il maggior numero di voti vince il seggio.

## Metaclasses
```yaml
metaclasses:
  - external
  - totals
  - lanes
  ```
La classe Collegio utilizza le seguenti metaclassi per definire il suo comportamento:

+ external: Gestisce gli attributi di input/output che possono essere inizializzati tramite configurazioni o parametri esterni.
+ totals: Permette di definire funzioni per l'aggregazione e la trasformazione dei dati elettorali a livello di collegio.
+ lanes: Gestisce le "lanes" di distribuzione, consentendo la propagazione delle informazioni relative ai seggi uninominali.
## External
```yaml
external:
  voti_uninominale:
    columns:
      - Candidato
      - Coalizione
      - Lista
      - Partito
      - Voti
```
Gli attributi external della classe Collegio includono:

+ voti_uninominale: È un DataFrame che contiene i voti espressi nel collegio per ciascun candidato. Le colonne includono Candidato, Coalizione, Lista, Partito e Voti. Questi dati vengono inizializzati tramite il file di configurazione o da fonti di dati esterne.
## Totals_Support
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
          name: Commons.seleziona_vincitore_collegio
```
La funzione totals_support get_vincente_uninominale calcola il vincitore del collegio uninominale:

+ Source: Utilizza la funzione self.get_voti_uninominale per ottenere i dati di voto relativi al collegio.
+ Type: transform indica una trasformazione dei dati.
+ Ops: Passa i dati a Commons.seleziona_vincitore_collegio, che determina il candidato vincente basato sul numero di voti ricevuti. Restituisce un DataFrame con Partito e VotiVincenti per il vincitore.
## Lanes_Propose
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
La funzione lanes_propose seggi_collegiali assegna il seggio uninominale al candidato con il maggior numero di voti:

+ Source: Chiama la funzione self.get_voti_uninominale per ottenere i dati di voto.
+ Distribution: Assegna il seggio al Partito del candidato che ha ricevuto il maggior numero di voti.
+ Key: Partito è il riferimento per l'assegnazione del seggio.
+ Seats: Assegna un solo seggio.
+ Selector: Seleziona il candidato con il numero di voti più alto (order: decreasing) e prende il primo (take: 1).
+ Info: Include informazioni aggiuntive sui Voti nel contesto della distribuzione.
## Lane
```yaml
lane:
  uninominale:
    node_type: only
    order_number: 1
    distribution: seggi_collegiali
    info_name: Collegio
```
La classe Collegio definisce una lane denominata uninominale con le seguenti caratteristiche:

+ Node Type: only indica che è l'unica lane per la gestione dei seggi uninominali.
+ Order Number: Definisce la priorità nel sistema di lane.
+ Distribution: La distribuzione è calcolata dalla funzione seggi_collegiali.
+ Info Name: Specifica che la distribuzione è a livello di Colle