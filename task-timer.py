"""
task-timer.py — Task Timer locale
Uso:
  python task-timer.py help
  python task-timer.py start "nome del task"
  python task-timer.py stop
  python task-timer.py status
  python task-timer.py list
  python task-timer.py edit <numero> "nuovo nome"
  python task-timer.py delete <numero>
  python task-timer.py delete last
  python task-timer.py report
  python task-timer.py report week
  python task-timer.py report all
"""

import sys
import json
import csv
import os
from datetime import datetime, timedelta

# --- Percorsi file (stessa cartella dello script) ---
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "timer_state.json")
LOG_FILE   = os.path.join(BASE_DIR, "timer_log.csv")

# --- Helpers ---
def fmt_duration(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def append_log(task, start_str, end_str, duration_sec):
    is_new = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["data", "task", "inizio", "fine", "durata_hms", "durata_minuti"])
        date_str = datetime.fromisoformat(start_str).strftime("%Y-%m-%d")
        duration_min = round(duration_sec / 60, 2)
        writer.writerow([date_str, task, start_str, end_str, fmt_duration(duration_sec), duration_min])

def read_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_log(rows):
    """Riscrive il CSV completo (usato da edit e delete)."""
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["data", "task", "inizio", "fine", "durata_hms", "durata_minuti"])
        for r in rows:
            writer.writerow([r["data"], r["task"], r["inizio"], r["fine"],
                             r["durata_hms"], r["durata_minuti"]])

# --- Comandi ---

def cmd_help():
    print("""
┌─────────────────────────────────────────────────────────┐
│            task-timer.py — Task Timer locale            │
├──────────────────┬──────────────────────────────────────┤
│ COMANDO          │ DESCRIZIONE                          │
├──────────────────┼──────────────────────────────────────┤
│ help             │ Mostra questo aiuto                  │
├──────────────────┼──────────────────────────────────────┤
│ start "task"     │ Avvia il timer per il task indicato  │
│ stop             │ Ferma il timer e salva la sessione   │
│ status           │ Mostra il timer in corso             │
├──────────────────┼──────────────────────────────────────┤
│ list             │ Elenca tutte le sessioni con indice  │
│ edit N "nome"    │ Rinomina la sessione numero N        │
│ delete N         │ Elimina la sessione numero N         │
│ delete last      │ Elimina l'ultima sessione            │
├──────────────────┼──────────────────────────────────────┤
│ report           │ Report di oggi                       │
│ report week      │ Report di questa settimana           │
│ report all       │ Tutto lo storico                     │
└──────────────────┴──────────────────────────────────────┘

Esempi:
  python task-timer.py start "fix bug login"
  python task-timer.py stop
  python task-timer.py edit 3 "refactoring API"
  python task-timer.py delete last
  python task-timer.py report week

File generati (stessa cartella dello script):
  timer_log.csv    — storico completo, apribile in Excel
  timer_state.json — stato del timer attivo (temporaneo)
""")

def get_last_task():
    rows = read_log()
    if not rows:
        return None
    return rows[-1]["task"]

def cmd_start(task_name=None):
    state = load_state()
    if state:
        elapsed = (datetime.now() - datetime.fromisoformat(state["start"])).total_seconds()
        print(f"⚠️  Timer già attivo: '{state['task']}' (avviato {fmt_duration(elapsed)} fa)")
        print("   Fai 'stop' prima di iniziare un nuovo task.")
        return

    if not task_name:
        last = get_last_task()
        if last:
            answer = input(f"Ultimo task: '{last}'. INVIO per riusarlo, oppure scrivi un nuovo nome: ").strip()
            task_name = answer if answer else last
        else:
            task_name = input("Nome del task: ").strip()
        if not task_name:
            print("❌ Nessun nome inserito, timer non avviato.")
            return

    now = datetime.now().isoformat(timespec="seconds")
    save_state({"task": task_name, "start": now})
    print(f"▶  Timer avviato: '{task_name}'  [{datetime.now().strftime('%H:%M:%S')}]")

def cmd_stop():
    state = load_state()
    if not state:
        print("⚠️  Nessun timer attivo. Usa: python task-timer.py start \"nome task\"")
        return
    end   = datetime.now()
    start = datetime.fromisoformat(state["start"])
    secs  = (end - start).total_seconds()
    end_str = end.isoformat(timespec="seconds")
    append_log(state["task"], state["start"], end_str, secs)
    clear_state()
    print(f"⏹  Fermato: '{state['task']}'")
    print(f"   Durata: {fmt_duration(secs)}  ({round(secs/60, 1)} min)")
    print(f"   Salvato in: {LOG_FILE}")

def cmd_status():
    state = load_state()
    if not state:
        print("⏸  Nessun timer attivo.")
        return
    elapsed = (datetime.now() - datetime.fromisoformat(state["start"])).total_seconds()
    print(f"▶  In corso: '{state['task']}'")
    print(f"   Avviato alle: {datetime.fromisoformat(state['start']).strftime('%H:%M:%S')}")
    print(f"   Tempo trascorso: {fmt_duration(elapsed)}")

def cmd_list():
    rows = read_log()
    if not rows:
        print("📋 Nessuna sessione nel log.")
        return
    print(f"\n{'#':>4}  {'Data':<12} {'Inizio':>6}-{'Fine':<6}  {'Durata':<9}  Task")
    print("─" * 60)
    for i, r in enumerate(rows, 1):
        inizio = datetime.fromisoformat(r["inizio"]).strftime("%H:%M")
        fine   = datetime.fromisoformat(r["fine"]).strftime("%H:%M")
        print(f"  {i:>2}.  {r['data']:<12} {inizio:>5}-{fine:<5}  {r['durata_hms']:<9}  {r['task']}")
    print()

def cmd_edit(index_str, new_name):
    rows = read_log()
    if not rows:
        print("📋 Nessuna sessione nel log.")
        return
    try:
        idx = int(index_str) - 1
        if idx < 0 or idx >= len(rows):
            raise ValueError
    except ValueError:
        print(f"❌ Indice non valido: '{index_str}'. Usa 'list' per vedere i numeri.")
        return
    old_name = rows[idx]["task"]
    rows[idx]["task"] = new_name
    write_log(rows)
    print(f"✏️  Sessione {idx+1} aggiornata:")
    print(f"   '{old_name}'  →  '{new_name}'")

def cmd_delete(index_str):
    rows = read_log()
    if not rows:
        print("📋 Nessuna sessione nel log.")
        return
    if index_str.lower() == "last":
        idx = len(rows) - 1
    else:
        try:
            idx = int(index_str) - 1
            if idx < 0 or idx >= len(rows):
                raise ValueError
        except ValueError:
            print(f"❌ Indice non valido: '{index_str}'. Usa 'list' per vedere i numeri.")
            return
    removed = rows.pop(idx)
    write_log(rows)
    inizio = datetime.fromisoformat(removed["inizio"]).strftime("%H:%M")
    fine   = datetime.fromisoformat(removed["fine"]).strftime("%H:%M")
    print(f"🗑️  Eliminata sessione {idx+1}: '{removed['task']}'  "
          f"({removed['data']} {inizio}-{fine}, {removed['durata_hms']})")

def cmd_report(period="today"):
    rows = read_log()
    if not rows:
        print("📋 Nessun log trovato.")
        return
    today = datetime.now().date()
    if period == "today":
        label = f"Oggi ({today})"
        rows = [r for r in rows if r["data"] == str(today)]
    elif period == "week":
        start_week = today - timedelta(days=today.weekday())
        label = f"Questa settimana (dal {start_week})"
        rows = [r for r in rows if r["data"] >= str(start_week)]
    else:
        label = "Storico completo"
    if not rows:
        print(f"📋 Nessuna sessione per: {label}")
        return
    totals = {}
    for r in rows:
        t = r["task"]
        totals[t] = totals.get(t, 0) + float(r["durata_minuti"])
    total_min = sum(totals.values())
    print(f"\n📊 Report — {label}")
    print(f"{'─'*45}")
    for task, mins in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"  {fmt_duration(mins*60)}  │  {task}")
    print(f"{'─'*45}")
    print(f"  TOTALE: {fmt_duration(total_min*60)}  ({round(total_min, 1)} min)\n")
    print("  Dettaglio sessioni:")
    for r in rows:
        inizio = datetime.fromisoformat(r["inizio"]).strftime("%H:%M")
        fine   = datetime.fromisoformat(r["fine"]).strftime("%H:%M")
        print(f"  {r['data']}  {inizio}-{fine}  {r['durata_hms']}  │  {r['task']}")
    print()

# --- Main ---
def main():
    args = sys.argv[1:]
    if not args:
        cmd_help()
        return

    cmd = args[0].lower()

    if cmd in ("help", "--help", "-h"):
        cmd_help()
    elif cmd == "start":
        if len(args) < 2:
            cmd_start()
        else:
            cmd_start(" ".join(args[1:]))
    elif cmd == "stop":
        cmd_stop()
    elif cmd == "status":
        cmd_status()
    elif cmd == "list":
        cmd_list()
    elif cmd == "edit":
        if len(args) < 3:
            print('❌ Uso: python task-timer.py edit <numero> "nuovo nome task"')
        else:
            cmd_edit(args[1], " ".join(args[2:]))
    elif cmd == "delete":
        if len(args) < 2:
            print('❌ Uso: python task-timer.py delete <numero>  oppure  delete last')
        else:
            cmd_delete(args[1])
    elif cmd == "report":
        period = args[1].lower() if len(args) > 1 else "today"
        cmd_report(period)
    else:
        print(f'❌ Comando sconosciuto: "{cmd}"')
        print('   Scrivi "python task-timer.py help" per vedere i comandi disponibili.')

if __name__ == "__main__":
    main()
