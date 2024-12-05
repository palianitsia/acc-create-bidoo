# acc-create-bidoo
Il bot descritto nel codice ha la funzione principale di automatizzare la registrazione di account su it/es.bidoo.com

Il bot descritto nel codice ha la funzione principale di automatizzare la registrazione di account su un sito web specifico (in questo caso, bidoo.com). Ecco un riepilogo delle sue funzionalità:

Interfaccia Grafica: Utilizza PyQt5 per creare un'interfaccia utente che consente di inserire vari parametri per la registrazione.

Registrazione Multipla: Permette di registrare più account in un'unica esecuzione, specificando il numero di registrazioni desiderate e un intervallo di tempo tra ciascuna registrazione.

Generazione di Dati: Genera email, username e password casuali per ogni registrazione. Gli utenti possono anche scegliere di utilizzare una password fissa.

User -Agent Mobile: Utilizza una lista di user-agent mobili per simulare la registrazione da dispositivi mobili.

Salvataggio Dati: Scrive i dettagli degli account registrati in un file di testo chiamato accounts.txt.

Controllo di Sicurezza: Gestisce eventuali errori durante il processo di registrazione e mostra messaggi di errore tramite finestre di dialogo.

Requisiti per Utilizzare il Bot

Per utilizzare questo bot, sono necessari i seguenti requisiti:

Python: Assicurati di avere Python installato sul tuo sistema.

Librerie Necessarie: Devi installare le seguenti librerie Python:

PyQt5: Per l'interfaccia grafica.
playwright: Per l'automazione del browser.

Chrome: Devi avere Google Chrome installato sul tuo computer. Il bot richiede il percorso di chrome.exe per funzionare.

File di Configurazione: Il bot crea e utilizza un file chiamato chrome_path.txt per memorizzare il percorso di chrome.exe. Se questo file non esiste, il bot chiederà di selezionare il percorso di Chrome tramite una finestra di dialogo.

Connessione Internet: È necessaria una connessione a Internet per accedere al sito web e completare le registrazioni.

Permessi di Esecuzione: Assicurati di avere i permessi necessari per eseguire script Python e accedere ai file sul tuo sistema.

Per avviare bot accedi alla riga di commando cmd e inserisci "pip install PyQT5 playwright" dopo aver installato tutto inserisci "playwright install".

Conclusione

Questo bot è uno strumento utile per automatizzare la registrazione di account su un sito web, ma è importante utilizzarlo in conformità con i termini di servizio del sito web e le leggi locali.
