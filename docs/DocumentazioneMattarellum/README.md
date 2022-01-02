In questa directory si trova la documentazione di Davide Maioli per l'esame Progetto di Ingegneria Informatica.

Oltre ad alcuni bugfix, il mio lavoro è si è concentrato sui file nella directory LeggiElettorali/Mattarellum e sul file src/Commons/mattarellum.py:

+ In LeggiElettorali/Mattarellum/Classes si trovano le definizioni delle classi
+ In LeggiElettorali/Mattarellum/Instances si trovano le definizioni delle istanze
+ In LeggiElettorali/Mattarellum/Data si trovano i dati in formato csv usati per simulare l'elezione del 2001
+ In LeggiElettorali/Mattarellum/DataSet si trovano i dati originali del Ministero dell'Interno e due script, uno è il web scraper mentre l'altro è stato usato per la pulizia dei dati
+ Il modulo /src/Commons/mattarellum.py contiene alcune funzioni necessarie al funzionamento del Mattarellum


Riguardo alla documentazione, che si trova tutta in questa directory:

+ La relazione del progetto è il file Relazione.pdf
+ La documentazione delle classi definite tramite file yaml, cioè Collegio, Circoscrizione e Nazione, è nei file Collegio.md, Circoscrizione.md e Nazione.md
+ La documentazione dei file python Partito.py e mattarellum.py, è nei file Partito.html e mattarellum.html. Gli script scraper.py e estractor.py, che si trovano in LeggiElettorali/Mattarellum/DataSet, non sono stati documentati a parte ma sono ordinati e ben commentati per essere utilizzati come punto di partenza nel caso qualcun altro dovesse ottenere i dati nello stesso modo.
+ I dettagli della configurazione del framework sono nel file Configurazione.md.