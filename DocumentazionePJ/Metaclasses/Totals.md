# Totali (elaborazione dati)
I totals possono funzionare in uno dei seguenti modi:
+ _aggregate_, prende un risultato con record omogenei duplicati e li somma, ma non lo fa trasformare in altro modo. Da molti (un numero arbitrario) a 1. Es:
    + _combination_, prende dati eterogenei e li combina in un unico risultato. Da n a 1;
    + _transformation_, prende un risultato e si trasforma in un altro, da 1 a 1;

Una combinazione di questi può essere ottenuta assegnando a ogni passaggio intermedio un valore diverso.

Il comportamento predefinito è applicare filtri (come definito nella metaclasse del filtro) all'output del
funzione e inoltrarla a diverse chiamate di funzione.

Più specificamente una chiamata al filtro può restituire:
+ `None`: il filtro deve essere applicato a valle, inoltrarlo;
+ Una funzione che può essere applicata a una riga del risultato e fornisce un risultato booleano, non inoltrare.

Se un filtro deve essere modificato, deve essere specificato nella definizione di una funzione di totali.

**Funzione ad alto livello:** questa metaclasse offre un sistema omogeneo per descrivere operazioni
su dataframe senza dover scrivere codice.

Vengono offerti due tipi di funzione:
+ totals: a queste funzioni si accede chiamando:
 `self.totals(nome_funzione, *sbarramenti, **kwargs)`
+ support: queste funzioni invece vengono chiamate come `self.nome_funzione(**kwargs)`

Oltre a questo l'unica differenza è che quando la funzione è definita come totals e `*sbarramenti` non è vuota. Il dataframe risultante è filtrato in base al contenuto di sbarramenti. Si veda la documentazione di `totFilter` per dettagli.

**Top level keyword:** `totals` o `totals_support`

**Schema:** entrambe si compongono di un dizionario dove le chiavi sono `nome_funzione` e i valori
sono dei dizionari con chiavi:

+ _rename_: un dizionario stringa-stringa, si comporta come rename in source;
+ _columns_: una lista di stringhe, si comporta come rename in source;
+ _type_: uno tra
    + _aggregate_;
    + _transform_;
    + _combination_.

Per aggregate e transform:
+ source: la source da chiamare per ricevere il dataframe di input. Qui è dove `**kwargs` e, dove necessario, `*sbarramenti` viene inoltrato.

Per aggregate:
+ _keys_: una lista di stringhe che indica quali colonne costituiscono la chiave;
+ _ops_: un dizionario nome_colonna -> operazione, dove operazione è:;
    + _mean_: per la media aritmetica;
    + _median_;
    + _sum_;
    + _prod_: per il prodotto;
    + o il nome di una funzione in commons.

Per combination:
+ _function_: una stringa che indica la funzione da chiamare, questa accettà:
    + 1 dataframe passato posizionalmente;
    + un numero arbitrario di argomenti posizionali;
    + un numero arbitrario di argomenti passati per chiave.
+ _merge_keys_: le chiavi da usare per combinare i vari dataframe;
+ _keys_: le chiavi da usare per dividere il dataframe combinato;
+ _args_: una lista di:
    + stringa o intero o booleano: uno scalare;
    + dizionario contenente le chiavi:
        + _type_: series, dataframe o scalar;
        + _source_.

Nota su combination, combination opera facendo il merge (su merge_keys) di tutti i dataframe e facendo groupby sul risultato (usando keys). Per ogni gruppo risultante sarà chiamata la funzione passando:
+ La slice di dataframe corrispondente;
+ Tutti i parametri scalari;
+ Per ogni series la linea corrispondente alla chiave del gruppo trattandola come un dizionariopassat o per kwargs.  

Una series è un oggetto di tipo dataframe con almeno le colonne keys, dove per ogni combinazione di keys c'è una e una sola linea.

Per transform:
+ _ops_: una lista di dizionari, a seconda del valore associato alla chiave `type` verrà trattato
come:
    + _transform column_: applica un'operazione a tutti gli elementi di una data colonna, sovrascrivendola o creando una nuova colonna;
    + _transform line_: chiama per ogni linea la funzione usando la linea come dizionario di `**kwargs`;
    + _transform dataframe_: applica la funzione a tutto il dataframe

    Le operazioni vengono eseguite in sequenza

Transform ops:
+ _column_:
    + _column_: la colonna da modificare
    + *column_type* (opzionale): se specificato converte le celle nel tipo dato (si veda `type` in 
    external)
    + *replace_name* (opzionale): di default uguale a column, indica il nome della colonna generata
    + _source_: la funzione da chiamare fornendo come parametro la cella
+ _line_:
    + _source_: la funzione da chiamare fornendo come kwargs il dizionario equivalente alla linea
    + *_column_name_*: che nome assegnare alla colonna risultante
+ _dataframe_:
    + _source_: la funzione cui passare il dataframe