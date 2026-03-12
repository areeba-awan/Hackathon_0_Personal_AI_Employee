import time
import logging
import threading
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WatcherOrchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.logger = logging.getLogger('WatcherOrchestrator')
        self.observers = []
        self.running = False

    def start(self):
        self.running = True
        self.logger.info('Starting WatcherOrchestrator')

        # Start inbox watcher in separate thread
        try:
            inbox_thread = threading.Thread(
                target=self._run_inbox_watcher,
                daemon=True
            )
            inbox_thread.start()
            self.logger.info('Inbox watcher thread started')
        except Exception as e:
            self.logger.error(f'Failed to start inbox watcher: {e}')

        # Start Gmail watcher in separate thread
        try:
            gmail_thread = threading.Thread(
                target=self._run_gmail_watcher,
                daemon=True
            )
            gmail_thread.start()
            self.logger.info('Gmail watcher thread started')
        except Exception as e:
            self.logger.error(f'Failed to start gmail watcher: {e}')

        # Start WhatsApp watcher in separate thread
        try:
            whatsapp_thread = threading.Thread(
                target=self._run_whatsapp_watcher,
                daemon=True
            )
            whatsapp_thread.start()
            self.logger.info('WhatsApp watcher thread started')
        except Exception as e:
            self.logger.error(f'Failed to start whatsapp watcher: {e}')

        # Start LinkedIn watcher in separate thread
        try:
            linkedin_thread = threading.Thread(
                target=self._run_linkedin_watcher,
                daemon=True
            )
            linkedin_thread.start()
            self.logger.info('LinkedIn watcher thread started')
        except Exception as e:
            self.logger.error(f'Failed to start linkedin watcher: {e}')

    def _run_inbox_watcher(self):
        try:
            inbox_path = self.vault_path / 'Inbox'
            needs_action_path = self.vault_path / 'Needs_Action'

            if not inbox_path.exists():
                self.logger.warning(f'Inbox folder not found at {inbox_path}')
                return

            needs_action_path.mkdir(exist_ok=True)
            processed = set()

            self.logger.info('Inbox watcher polling started')

            while self.running:
                try:
                    # Check for new files in Inbox
                    for file_path in inbox_path.glob('*'):
                        if file_path.is_file() and file_path.name not in processed:
                            # Move file to Needs_Action with DROP_ prefix
                            dest_name = f"DROP_{file_path.name}"
                            dest_path = needs_action_path / dest_name

                            # Handle duplicates
                            counter = 1
                            base_dest = dest_path
                            while dest_path.exists():
                                stem = base_dest.stem
                                if '-' in stem and stem.rsplit('-', 1)[1].isdigit():
                                    stem = stem.rsplit('-', 1)[0]
                                dest_path = needs_action_path / f"{stem}-{counter}{base_dest.suffix}"
                                counter += 1

                            try:
                                file_path.rename(dest_path)
                                self.logger.info(f'Moved {file_path.name} to Needs_Action')
                                processed.add(file_path.name)
                            except Exception as e:
                                self.logger.error(f'Error moving {file_path.name}: {e}')

                    time.sleep(5)  # Check every 5 seconds
                except Exception as e:
                    self.logger.error(f'Inbox watcher polling error: {e}')
                    time.sleep(5)
        except Exception as e:
            self.logger.error(f'Inbox watcher error: {e}')

    def _run_gmail_watcher(self):
        try:
            from .gmail_watcher import GmailWatcher
            creds_path = self.vault_path / 'token.json'
            if creds_path.exists():
                watcher = GmailWatcher(
                    vault_path=str(self.vault_path),
                    credentials_path=str(creds_path),
                    check_interval=120
                )
                watcher.run()
        except Exception as e:
            self.logger.error(f'Gmail watcher error: {e}')

    def _run_whatsapp_watcher(self):
        try:
            from .whatsapp_watcher import WhatsAppWatcher
            session_path = self.vault_path / 'whatsapp_session'
            watcher = WhatsAppWatcher(
                vault_path=str(self.vault_path),
                session_path=str(session_path),
                check_interval=60
            )
            watcher.run()
        except Exception as e:
            self.logger.error(f'WhatsApp watcher error: {e}')

    def _run_linkedin_watcher(self):
        try:
            from .linkedin_watcher import LinkedInAutomationWatcher
            watcher = LinkedInAutomationWatcher(
                vault_path=str(self.vault_path),
                check_interval=30
            )
            watcher.run()
        except Exception as e:
            self.logger.error(f'LinkedIn watcher error: {e}')

    def stop(self):
        self.running = False
        self.logger.info('Stopping WatcherOrchestrator')
        for observer in self.watchers:
            observer.stop()
            observer.join()
        self.logger.info('All watchers stopped')

if __name__ == '__main__':
    orchestrator = WatcherOrchestrator('.')
    orchestrator.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        orchestrator.stop()
