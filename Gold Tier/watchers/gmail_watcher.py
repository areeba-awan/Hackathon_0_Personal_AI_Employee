import os.path
import time
import logging
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# Logging setup (terminal + file)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("gmail_watcher.log")]
)

# Scopes: sirf read karne ke liye (change kar sakti ho agar reply bhi chahiye)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher:
    def __init__(self, vault_path: str, credentials_path: str, token_path: str = 'token.json', check_interval: int = 120):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.needs_action.mkdir(exist_ok=True)
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.info("Initializing GmailWatcher...")
        print("Initializing GmailWatcher...")

        self.creds = None

        # Agar token.json mojood hai toh load karo
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # Agar creds nahi hain ya invalid hain → browser flow chalao
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.logger.info("Refreshing expired token...")
                print("Refreshing token...")
                self.creds.refresh(Request())
            else:
                self.logger.info("No valid token - starting OAuth flow (browser will open)")
                print("No valid token found - opening browser for login...")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)  # Yeh browser kholega

                # Token save kar do agle baar ke liye
                with open(token_path, 'w') as token_file:
                    token_file.write(self.creds.to_json())
                self.logger.info("Token saved to token.json")
                print("Login successful! Token saved to token.json")

        # Gmail service banao
        self.service = build('gmail', 'v1', credentials=self.creds)
        self.logger.info("Gmail service connected successfully")
        print("Gmail connected successfully ✓")

        self.processed_ids = set()

    def check_for_updates(self) -> list:
        try:
            # Debug ke liye: pehle sirf 'is:unread' use karo, baad mein 'is:important' add kar lena
            query = 'is:unread is:important'  # ← test ke liye sirf unread
            self.logger.info(f"Querying Gmail: {query}")
            print(f"Polling Gmail with query: {query}")

            results = self.service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])
            new_messages = [m for m in messages if m['id'] not in self.processed_ids]

            self.logger.info(f"Found {len(new_messages)} new unread messages")
            print(f"Found {len(new_messages)} new messages")

            return new_messages
        except Exception as e:
            self.logger.error(f"Query error: {e}")
            print(f"Query error: {e}")
            return []

    def create_action_file(self, message) -> Path:
        try:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            content = f'''---
type: email
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: high
status: pending
---

## Email Content
{msg.get('snippet', '[No content]')}

## Suggested Actions
- [ ] Reply
- [ ] Archive
'''
            filepath = self.needs_action / f"EMAIL_{message['id']}.md"
            filepath.write_text(content, encoding='utf-8')
            self.processed_ids.add(message['id'])

            self.logger.info(f"Created: {filepath}")
            print(f"Created file: {filepath.name}")
            return filepath
        except Exception as e:
            self.logger.error(f"File creation error: {e}")
            print(f"File error: {e}")
            return Path("error")

    def run(self):
        self.logger.info(f"Starting polling every {self.check_interval}s")
        print(f"Polling started - every {self.check_interval} seconds (Ctrl+C to stop)")
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
            except Exception as e:
                self.logger.error(f"Loop error: {e}")
                print(f"Loop error: {e}")
            time.sleep(self.check_interval)


if __name__ == "__main__":
    vault = "."
    creds_path = "credentials.json"
    token_path = "token.json"

    try:
        watcher = GmailWatcher(vault, creds_path, token_path)
        watcher.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to exit...")