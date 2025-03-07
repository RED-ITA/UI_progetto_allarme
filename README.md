# Progetto: Gestione Schede Modbus con PyQt6 per Allarme

## Descrizione del Progetto  
L’applicazione gestisce diverse schede con ID e funzionamenti differenti, che leggono valori da sensori tramite rete Modbus. Il progetto utilizza un'interfaccia grafica sviluppata con PyQt6 e un servizio in background per gestire le operazioni principali. I dati vengono memorizzati localmente in un database SQLite3. Il sistema è progettato per essere resiliente, consentendo aggiornamenti delle impostazioni e la gestione degli errori, garantendo la continuità operativa.

---

## 1. Interfaccia Utente (UI - PyQt6)

### Caratteristiche principali:
- **User-friendly:** l'interfaccia è organizzata in diverse pagine per facilitare la gestione delle funzionalità:
  - **Home page**: panoramica dello stato del sistema.
  - **Pagina Sensori**: consente l'aggiunta, modifica e eliminazione dei sensori.
  - **Pagina Stanze**: permette di creare, eliminare e modificare le stanze, assegnare i sensori e visualizzare la piantina.
  - **Pagina Rilevamenti**: visualizza i rilevamenti degli allarmi attivati.
- **Threading separato**: l'interfaccia utente gira su un thread separato per mantenere la reattività.
- **Configurazione Modbus**: dalla pagina dei sensori è possibile aggiungere nuovi sensori al database e modificare quelli esistenti.
- **Soglie configurabili**: per ogni scheda, se supportato, è possibile modificare i valori di soglia dei sensori.
- **Monitoraggio allarmi**: la UI crea un thread che controlla ciclicamente il campo "allarme" nel database.
- **Aggiornamento impostazioni**: quando i parametri vengono modificati, il campo `update_settings` nel database viene aggiornato.
- **Gestione allarmi**: se viene attivato un allarme, il database viene aggiornato di conseguenza.

---

## 2. Servizio in Background

### Funzionalità principali:
- **Avvio automatico**: il servizio si avvia automaticamente all'apertura dell'applicazione, legge le impostazioni dal database SQLite3 e crea gli oggetti corrispondenti per ciascuna scheda configurata.
- **Gestione Modbus**: ogni scheda gestisce i propri registri e coil Modbus.
  - **Sensore di Movimento (PIR analogico)**:
    - REGISTER: `TRIGGER_MOVIM = 1`
    - COIL: `STATO = 0`, `VALUE = 8`, `ERROR = 16`
  - **Sensore Magnetico**:
    - REGISTER: Nessun registro.
    - COIL: `STATO = 0`, `VALUE = 8`, `ERROR = 16`
  - **Sensore di Vibrazione**:
    - REGISTER: `TRIGGER_VIBRA = 1`
    - COIL: `STATO = 0`, `VALUE = 8`, `ERROR = 16`
- **Sincronizzazione dati**: ogni scheda ha un thread per sincronizzare i dati con il database in modo asincrono.
- **Aggiornamento impostazioni**: se il campo `update_settings` nel database viene impostato a 1, i processi attuali vengono interrotti, le impostazioni aggiornate e i thread ricreati.
- **Gestione allarmi**: se il campo `STATO` nel database è impostato a 1, e un sensore si attiva, l'allarme viene impostato a 1.

---

## 3. Database Locale (SQLite3)

### Struttura delle Tabelle:

- **SENSORI**
  - `Id [int]`: indirizzo Modbus
  - `Tipo [int]`: tipo di sensore (0: movimento, 1: magnetico, 2: vibrazione)
  - `Data [date]`: data di aggiunta
  - `Stanza [str]`: nome della stanza
  - `Soglia [int]`: valore di soglia del sensore
  - `Error [int]`: stato di errore (0: no errore, 1: errore)
  
- **VALORI**
  - `Id [int]`: indirizzo Modbus
  - `Value [int]`: valore del sensore
  
- **SISTEMA**
  - `Allarme [int]`: stato allarme (0: inattivo, 1: attivo)
  - `Stato [int]`: stato sistema (0: spento, 1: acceso)
  - `Update [int]`: segnala aggiornamento parametri sensori
  - `Error [int]`: errore sensore
  
- **LOG**
  - `Id [int]`: ID sensore
  - `Tipo [int]`: tipo di sensore (0: movimento, 1: magnetico, 2: vibrazione)
  - `Stanza [str]`: nome della stanza
  - `Data [date]`: data di attivazione

---

## 4. Gestione dei Processi e Concorrenza

- **Thread separati**: ogni scheda ha un thread per la lettura dei dati e uno per la sincronizzazione con il database.
- **Gestione degli errori**: se una scheda presenta un errore:
  - Con l'allarme attivo, termina il processo della scheda problematica, segnalando l'errore nel database.
  - Con l'allarme spento, il processo problematico viene fermato e l'errore viene registrato.
- **Gestione concorrenza**: SQLite3 blocca la scrittura concorrente. Le operazioni sul database sono gestite in modo asincrono, utilizzando una coda per evitare conflitti. In caso di errore, vengono eseguiti fino a 5 tentativi di scrittura.

---

## 5. Ottimizzazione e Gestione Errori

- **Threading ottimizzato**: gestione dei thread tramite `queue.Queue` per prevenire deadlock.
- **Gestione avanzata degli errori**: sistema di logging dettagliato per monitorare la sincronizzazione e i processi.



```bash
    curl -X POST http://localhost:5001/sensor -H "Content-Type: application/json" -d '{"tipo": 1}'
```