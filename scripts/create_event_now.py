import sys
from pathlib import Path

# Ensure project root is on sys.path so `actions` package can be imported
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from actions.google_calendar import google_calendar

params = {
    "summary": "Prueba rápida desde MATT",
    "description": "Evento creado mediante acciones desde el repo.",
    "minutes": 30
}

if __name__ == '__main__':
    res = google_calendar(params)
    print(res)
