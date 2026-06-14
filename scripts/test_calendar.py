import pathlib
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def main():
    base = pathlib.Path(__file__).resolve().parent.parent / 'config'
    creds_file = base / 'client_secret.json'  # asegúrate de poner aquí tu JSON descargado
    if not creds_file.exists():
        print(f"No se encontró {creds_file}. Coloca tu client_secret.json en la carpeta 'config'.")
        return

    token_file = base / 'token.json'

    creds = None
    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
        creds = flow.run_local_server(port=8888)
        try:
            token_file.write_text(creds.to_json(), encoding='utf-8')
        except Exception:
            pass

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.now()
    start = (now + datetime.timedelta(minutes=5)).isoformat()
    end = (now + datetime.timedelta(minutes=65)).isoformat()

    event = {
      'summary': 'Prueba MATT – evento',
      'description': 'Evento creado para probar integración de Google Calendar desde MATT.',
      'start': {'dateTime': start},
      'end':   {'dateTime': end},
    }

    try:
        ev = service.events().insert(calendarId='primary', body=event).execute()
        print('Evento creado:', ev.get('htmlLink'))
    except Exception as e:
        print('Error al crear evento:', e)

if __name__ == '__main__':
    main()
