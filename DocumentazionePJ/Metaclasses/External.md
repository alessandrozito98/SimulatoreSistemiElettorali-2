# External

In questa metaclasse vengono definite le variabili della classe creata, i loro valori saranno poi presi dai file d’instanziazione o da funzione specifiche.
Per ogni variabile è inoltre creato il corrispettivo metodo d'accesso.

## Configurazione

_Parola Chiave nel File :_ `external`

_Parametri :_ sono strutturati in un dizionario avente come chiavi delle stringhe che diventeranno poi i nomi delle variabili.
I valori associati alle chiavi sono dizionari aventi le seguenti chiavi :

- `init` : opzionale, valore di default `False`
- `default` : opzionale, compare solo dove `init` è `True` e indica il
  valore di default della variabile
- `targets` : opzionale, il valore associato è una lista di dizionari in cui ogni dizionario genera una funzione che accede alla stessa variabile ma restituisce informazioni diverse

Le seguenti chiavi sono mutualmente esclusive con `targets`:

- `name` : opzionale, di default il valore della chiave di primo livello,
  indica che nome dare alla funzione di accesso
- `columns` : opzionale, indica quali colonne restituire
- `type` : opzionale, converte il risultato, può essere:
  - `int`
  - `float`
  - il nome di una classe definita dall'utente

Le chiavi del dizionario interno a `targets` sono :

- `name`
- `columns`

_Risultati :_ vengono generate le variabili e le funzioni con il seguente schema :

- `give_{chiave_del_dizionario}`
- `get_{chiave_del_dizionario_o_name_o_chiave_di_external}`
- se `init` è `True` allora aggiunge un valore che è richiesto in fase d'istanziazione, a meno che default sia presente, in tal caso inserisce il valore di default
