# task-timer

Piccolo time tracker locale a riga di comando, in Python puro (nessuna
dipendenza esterna). Nessun cloud, nessun account: tutto salvato in un CSV
sul tuo PC.

## Uso rapido

```
python task-timer.py start "nome task"
python task-timer.py stop
python task-timer.py status
python task-timer.py list
python task-timer.py report
python task-timer.py report week
python task-timer.py report all
```

Lanciando `start` senza nome, propone di riusare l'ultimo task o di
scriverne uno nuovo.

Per usare il progetto come prefisso del task (finché non serve un campo
dedicato): `start "Drylite: fix bug login"`.

## Setup avvio/stop automatico

Vedi [SETUP.md](SETUP.md) per: comando rapido `tt`, prompt di avvio task
al login, stop automatico al logoff via Utilità di Pianificazione.

## File generati (non versionati, vedi .gitignore)

- `timer_log.csv` — storico sessioni
- `timer_state.json` — stato del timer attivo
