import logging

# Simple file logger to diagnose calls from the runtime (MATT)
logging.basicConfig(filename='matt_calendar.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger('matt.google_calendar')


def google_calendar(parameters: dict, player=None) -> str:
    """Create a Google Calendar event using stored credentials.

    parameters (optional keys):
      - summary: event title
      - description: event description
      - start: ISO datetime string or 'YYYY-MM-DDTHH:MM:SS' (local)
      - end: ISO datetime string
      - minutes: duration in minutes (if start provided without end)

    Returns a user-friendly string with result.
    """
    try:
        logger.debug('google_calendar called with parameters: %s player=%s', parameters, getattr(player, '__class__', None))
        from pathlib import Path
        import datetime
        base = Path(__file__).resolve().parent.parent / 'config'
        creds_file = base / 'client_secret.json'
        token_file = base / 'token.json'

        SCOPES = ['https://www.googleapis.com/auth/calendar.events']

        # Lazy import Google libs to avoid hard dependency unless used
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
        except Exception as e:
            return f"Google API libraries missing: {e}"

        creds = None
        if token_file.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
            except Exception:
                creds = None

        if not creds or not creds.valid:
            if not creds_file.exists():
                return "No client_secret.json found in config/. Add Google OAuth credentials first."
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
            creds = flow.run_local_server(port=8888)
            try:
                token_file.write_text(creds.to_json(), encoding='utf-8')
            except Exception:
                pass

        service = build('calendar', 'v3', credentials=creds)

        # Use timezone-aware datetimes (local timezone) to satisfy Google API
        now = datetime.datetime.now().astimezone()
        local_tz = now.tzinfo
        summary = parameters.get('summary') if parameters else None
        description = parameters.get('description') if parameters else ''
        start = parameters.get('start') if parameters else None
        end = parameters.get('end') if parameters else None
        minutes = int(parameters.get('minutes')) if parameters and parameters.get('minutes') else 60

        if not summary:
            summary = 'Evento creado por MATT'

        if start and not end:
            try:
                dt_start = datetime.datetime.fromisoformat(start)
            except Exception:
                dt_start = now + datetime.timedelta(minutes=5)
            dt_end = dt_start + datetime.timedelta(minutes=minutes)
        elif start and end:
            try:
                dt_start = datetime.datetime.fromisoformat(start)
                dt_end = datetime.datetime.fromisoformat(end)
                if dt_start.tzinfo is None:
                    dt_start = dt_start.replace(tzinfo=local_tz)
                if dt_end.tzinfo is None:
                    dt_end = dt_end.replace(tzinfo=local_tz)
            except Exception:
                dt_start = now + datetime.timedelta(minutes=5)
                dt_end = dt_start + datetime.timedelta(minutes=minutes)
        else:
            dt_start = now + datetime.timedelta(minutes=5)
            dt_end = dt_start + datetime.timedelta(minutes=minutes)

        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': dt_start.isoformat()},
            'end': {'dateTime': dt_end.isoformat()},
        }

        ev = service.events().insert(calendarId='primary', body=event).execute()
        link = ev.get('htmlLink')
        logger.info('Event created, link=%s', link)
        return f"Evento creado: {link}" if link else "Evento creado correctamente."
    except Exception as e:
        logger.exception('Error creando evento')
        return f"Error creando evento: {e}"
