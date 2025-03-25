frontend_errors = {

    # SUCCESS
    0: ('SUCCESS', 'Avvio:'),
    # INFO
    1: ('INFO', 'Inizializzazione dell\'interfaccia utente: '),
    2: ('INFO', 'Aggiornamento dell\'interfaccia utente: '),
    3: ('INFO', 'Costruzione dell\'interfaccia utente: '),
    4: ('INFO', 'Impostazione del colore di sfondo: '),
    5: ('INFO', 'Caricamento del file di stile: '),
    6: ('INFO', 'NOTIFICATO: '),
    # WARNING
    404: ('WARNING', 'Errore sconosciuto'),
    
    #sensori page
    100: ('INFO', 'Tentativo di eliminazione del sensore'),
    101: ('INFO', 'Apertura della schermata parametri per il sensore'),
    102: ('INFO', 'Popolamento delle aree di scorrimento con i widget dei sensori'),
    103: ('INFO', 'Creazione delle aree di scorrimento per sensori attivi e inattivi'),
    104: ('INFO', 'Pulsante "Aggiungi Sensore" cliccato'),
    105: ('INFO', 'Sensore cliccato per modifica'),
    106: ('INFO', 'Sensore selezionato'),
    107: ('INFO', 'Finita aggiunta o modifica sensore'),
    # ERROR
    401: ('ERROR', 'Errore nell\'aggiunta del sensore'),
    
    #stanza page
    200: ('INFO', 'Popolamento della scroll area con le stanze disponibili'),
    201: ('INFO', 'Stanza selezionata'),
    202: ('INFO', 'Popolamento della scroll area con i sensori per la stanza selezionata'),
    203: ('INFO', 'Pulsante "Aggiungi Stanza" cliccato'),
    204: ('INFO', 'Aggiunta nuova stanza'),
    # ERROR
    402: ('ERROR', 'Errore nell\'aggiunta della stanza'),
    
    #tastierino
    300: ('INFO', 'Codice Corretto'),
    301: ('INFO', 'Codice Errato'),
    302: ('INFO', 'Confermato Codice'),
    303: ('INFO', 'Cancellato Codice'),
    304: ('INFO', 'Disabilitati numeri'),
    305: ('INFO', 'Riabilitati Numeri'),
    # CRITICAL
    403: ('CRITICAL', 'Tentativo di forzatura'),


    #home_page
    500: ('INFO', 'apertura richiesta: '),
    501: ('INFO', 'resize'),
    502: ('INFO', 'icon resize')
}