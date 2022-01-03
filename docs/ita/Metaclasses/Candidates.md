# Candidate

**Funzione ad alto livello:** questa classe definisce le due funzioni necessarie per un candidato:
1. ricevere proposte di seggi dove si è stati eletti (e eventuali informazioni aggiuntive);
2. dove ci siano opportunità multiple il candidato deve scegliere quale accettare e quali rifiutare.

**Top level keyword:** `candidate`

## Configurazione

**Schema:**
+ `info_vars`: una lista di variabili della classe Candidato che saranno aggiunte alle informazioni
restituite quando un candidato viene eletto
+ `criteria`: può essere:
    + 'first' per indicare la prima proposta ricevuta
    + una lista di stringhe, le proposte vengono ordinate in base ai valori delle informazioni aggiuntive
    + il nome di una funzione