# Lane

Una lane è il "direttore" di esecuzione per il sistema, verrà eseguita una sola lane per singolo tempo, una lane inizierà chiamando una funzione sulle istanze dell'inizio lane. Una volta che la funzione restituisce i risultati vengono raccolti in un set dall'hub e ripetuti fino all'effettivo eletto si ottengono risultati.

Ogni passaggio della lane deve anche essere in grado di mostrare quanti posti assegnerà, questo sarà impostato
in coda alla lane per impostazione predefinita, ma potrebbe essere sfocato o essere assegnato dinamicamente a un livello superiore.

I livelli più alti possono affrontarlo sommando i livelli più bassi. Durante la configurazione dovrei considerare
le seguenti opzioni, perché una lane può essere utilizzata per eleggere:
+ un numero fisso di candidati
+ fino ad un numero fisso di candidati
+ un numero di candidati determinato a tempo di esecuzione
+ fino a un numero determinato in fase di esecuzione

I registri potrebbero anche essere passati per fornire ulteriori informazioni, ad esempio nella lane per
rappresentanti plurinominali nel Rosatellum la Circoscrizione passerà un dizionario che per ogni Coalizione/Partito darà maggiori informazioni.

## Lane head
È qui che inizia la lane, la creazione della classe la registrerà con l'Hub.

Offrirà una funzione che, quando chiamata, restituirà un **insieme** di candidati che hanno ricevuto un'offerta iniziale per un posto.

Creerà la prima proposta senza alcun input esterno e quindi correggerà le opzioni di livello inferiore.

Infine passerà ad ogni istanza di livello inferiore le direttive che deve seguire e attenderà la restituzione. Il `return` sarà un elenco di insiemi che devono essere uniti.

## Lane Node
Un nodo di una lane si comporta come capo lane ad eccezione della funzione di proposta trasparente che verrà chiamata dal livello superiore, e per una funzione che si comporterà come start_lane, ma accettando una distribuzione come
un argomento.

## Lane tail
Questo si comporta come nodo di lane tranne per il fatto che invece di chiamare un sottolivello utilizza la distribuzione. Utilizza le informazioni che ha ricevuto per eleggere i candidati, questo avverrà prendendo la finale
dataframe ottenuto (che avrà colonne: ["PolEnt", "Posti da assegnare"]) e sulla prima colonna di ogni riga chiamando la funzione fornita dalla metaclasse dell'elettore

## Lane direct
Questo è utile per i sistemi che non si basano su livelli superiori per decidere la rappresentazione, questi sono
sistemi come FPTF, multi-distretti proporzionali ecc.

È concettualmente uguale a una lane avente la stessa classe di Lane-head e Lane-tail.