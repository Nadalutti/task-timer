# Setup — Avvio e Stop Automatico

Requisito: Python installato e nel PATH (verifica con `python --version`).

## 1. Comando rapido `tt`

Nella cartella del progetto c'è `tt.bat`, che permette di scrivere `tt start`
invece di `python task-timer.py start`.

Per usarlo da qualsiasi cartella (senza `cd`):

1. `Win + R` → digita `sysdm.cpl` → invio
2. Tab "Avanzate" → "Variabili d'ambiente"
3. In "Variabili utente", seleziona `Path` → "Modifica" → "Nuovo"
4. Incolla il percorso della cartella, es. `C:\Users\lavoro\Documents\scripts\task-timer`
5. OK su tutte le finestre, poi riapri il cmd

Da ora: `tt start`, `tt stop`, `tt status`, `tt list`, `tt report` funzionano
da qualunque prompt.

## 2. Proposta di avvio task al login

Alla partenza del PC si apre un cmd che mostra lo stato attuale e chiede se
avviare un task (non parte mai da solo).

1. `Win + R` → digita `shell:startup` → invio (si apre la cartella di avvio)
2. Vai nella cartella del progetto, tasto destro su `avvia_task.bat` →
   "Crea collegamento"
3. Sposta il collegamento appena creato dentro la cartella aperta al punto 1

Da ora, ad ogni login si apre la finestra con il prompt.

## 3. Stop automatico al logoff/spegnimento

Windows non lascia eseguire codice Python "in ascolto" dello spegnimento
senza tenere un processo sempre attivo in background — la via più semplice
e affidabile è delegare a Utilità di Pianificazione di Windows, che
garantisce l'esecuzione dello script al logoff.

1. Apri "Utilità di pianificazione" (cerca nel menu Start)
2. Azione → "Crea attività..." (non "Crea attività di base")
3. Tab **Generale**: Nome `Stop Task Timer`
4. Tab **Attivazione** → Nuovo:
   - "Avvia l'attività": **Alla disconnessione alla sessione utente**
   - Utente: "Qualsiasi utente"
   - **Connessione da computer locale** (non "remoto" — importante, è l'opzione
     sbagliata di default in alcune versioni)
   - OK
5. Tab **Azioni** → Nuovo:
   - Programma/script: `python`
   - Aggiungi argomenti: `"C:\Users\lavoro\Documents\scripts\task-timer\task-timer.py" stop`
   - Inizia in: `C:\Users\lavoro\Documents\scripts\task-timer`
   - OK
6. Tab **Condizioni**:
   - Togli la spunta da "Avvia l'attività solo se il computer è alimentato
     da rete elettrica" (altrimenti non parte a batteria)
7. Salva con OK

Da ora, ogni logoff/spegnimento chiude automaticamente il task attivo
(se ce n'è uno), scrivendo la riga nel log.

## Riepilogo comandi

| Comando | Effetto |
|---|---|
| `tt start` | Avvia un task (propone l'ultimo usato) |
| `tt stop` | Ferma il task attivo |
| `tt status` | Mostra il task in corso |
| `tt list` | Elenca le sessioni registrate |
| `tt report` / `tt report week` / `tt report all` | Report tempi |

## File generati (non versionati su git)

- `timer_log.csv` — storico sessioni, dato personale
- `timer_state.json` — stato del timer attivo
