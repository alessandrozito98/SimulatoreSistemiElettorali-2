# Superdivision

Definisce il nome delle superdivions (come aggregato) e la classe di cui è composta.

Ad esempio in _uninominale_ definirà sezioni come sottosezione e sezione come nome della classe

Fornirà funzioni di aggregazione concatenando diversi ritorni di chiamata applicati sul
sottosezioni. In questo modo i totali devono solo gestire l'input dalle funzioni. Questo sarà solo un
concatenazione semplice, che può essere gestita da un totale aggregante.

**Parola chiave nel file**: `subdivisions`

## Schema
**Schema della configurazione:** un dizionario di dizionari, le chiavi indicano la variabile in cui
salvare i nomi delle istanze di sottolivello

I valori sono dizionari con:
+ type: il nome della classe
+ functions: una lista di dizionari, ogni dizionario ha:
    + name: il nome della funzione da esporre
    + source: una definizione tramite source della funzione da eseguire. Si assume che 
    nell'esecuzione di source "self" nel namespace si riferirà ad una sottodivisione

La funzione data verrà chiamata su ogni istanza delle sottodivisioni e i risultati saranno 
aggregati:
+ Se di tipo "int" verranno sommati
+ Se di tipo dataframe verranno concatenati
+ Altrimenti concatenati in una lista