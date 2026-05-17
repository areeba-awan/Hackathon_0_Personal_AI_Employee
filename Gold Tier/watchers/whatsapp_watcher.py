import time
import logging
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Logging setup (terminal + file)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("whatsapp_watcher.log")]
)

# Keywords to monitor for urgent/important messages
URGENT_KEYWORDS = [
    'urgent', 'asap', 'emergency', 'critical', 'invoice', 'payment',
    'deadline', 'important', 'action required', 'confirm', 'verify',
    'alert', 'warning', 'error', 'failed', 'issue', 'problem'
]

class WhatsAppWatcher:
    def __init__(self, vault_path: str, session_path: str = "whatsapp_session", check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.needs_action.mkdir(exist_ok=True)

        self.session_path = Path(session_path)
        self.session_path.mkdir(exist_ok=True)

        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.info("Initializing WhatsAppWatcher...")
        print("Initializing WhatsAppWatcher...")

        self.driver = None
        self.processed_messages = set()

    def launch_browser(self):
        """Launch Selenium browser with persistent session"""
        try:
            self.logger.info(f"Launching browser with session: {self.session_path}")
            print(f"Launching browser with session: {self.session_path}")

            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            driver_path = ChromeDriverManager().install()
            # Fix path - remove THIRD_PARTY_NOTICES.chromedriver
            if 'THIRD_PARTY_NOTICES' in driver_path:
                driver_path = driver_path.replace('/THIRD_PARTY_NOTICES.chromedriver', '/chromedriver.exe')

            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            self.logger.info("Browser launched successfully")
            print("Browser launched ✓")

        except Exception as e:
            self.logger.error(f"Browser launch error: {e}")
            print(f"Browser launch error: {e}")
            raise

    def navigate_to_whatsapp(self):
        """Navigate to WhatsApp Web"""
        try:
            self.logger.info("Navigating to WhatsApp Web...")
            print("Navigating to WhatsApp Web...")

            self.driver.get('https://web.whatsapp.com')
            time.sleep(5)  # Initial wait for page load

            # Wait for chat list to load - try multiple selectors
            loaded = False
            try:
                WebDriverWait(self.driver, 45).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
                )
                loaded = True
                self.logger.info("Chat list loaded - already authenticated")
                print("Chat list loaded ✓")
            except:
                pass

            if not loaded:
                self.logger.info("Waiting for QR code scan...")
                print("Please scan QR code in browser window...")
                try:
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
                    )
                    self.logger.info("QR code scanned successfully")
                    print("QR code scanned ✓")
                except:
                    # Try alternative selector
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "chat")]'))
                    )
                    self.logger.info("Chat interface loaded")
                    print("Chat interface loaded ✓")

        except Exception as e:
            self.logger.error(f"Navigation error: {e}")
            print(f"Navigation error: {e}")
            raise

    def extract_messages(self) -> list:
        """Extract unread messages from chat list"""
        try:
            messages = []

            # Get all chat items using role-based selector
            chat_items = self.driver.find_elements(By.XPATH, '//div[@role="listitem"]')
            self.logger.info(f"Found {len(chat_items)} chat items")

            for chat_item in chat_items:
                try:
                    # Get chat name
                    try:
                        chat_name_elem = chat_item.find_element(By.XPATH, './/span[@dir="auto"]')
                        chat_name = chat_name_elem.text
                    except:
                        chat_name = "Unknown"

                    # Get last message preview
                    try:
                        msg_preview_elem = chat_item.find_element(By.XPATH, './/span[@class]')
                        msg_preview = msg_preview_elem.text
                    except:
                        msg_preview = ""

                    if not msg_preview or not chat_name:
                        continue

                    # Check if message contains urgent keywords
                    is_urgent = any(keyword.lower() in msg_preview.lower() for keyword in URGENT_KEYWORDS)

                    message_id = f"{chat_name}_{datetime.now().timestamp()}"

                    if message_id not in self.processed_messages:
                        messages.append({
                            'id': message_id,
                            'chat': chat_name,
                            'preview': msg_preview,
                            'urgent': is_urgent,
                            'timestamp': datetime.now().isoformat()
                        })
                        self.processed_messages.add(message_id)

                except Exception as e:
                    self.logger.warning(f"Error extracting message: {e}")
                    continue

            self.logger.info(f"Extracted {len(messages)} new messages")
            print(f"Found {len(messages)} new messages")
            return messages

        except Exception as e:
            self.logger.error(f"Message extraction error: {e}")
            print(f"Message extraction error: {e}")
            return []

    def create_action_file(self, message: dict) -> Path:
        """Create action file for urgent message"""
        try:
            priority = "high" if message['urgent'] else "medium"

            content = f'''---
type: whatsapp
from: {message['chat']}
message: {message['preview']}
received: {message['timestamp']}
priority: {priority}
status: pending
urgent: {message['urgent']}
---

## WhatsApp Message

**From:** {message['chat']}
**Preview:** {message['preview']}
**Received:** {message['timestamp']}

## Keywords Detected
{', '.join([kw for kw in URGENT_KEYWORDS if kw.lower() in message['preview'].lower()]) or 'None'}

## Suggested Actions
- [ ] Read full message
- [ ] Reply
- [ ] Forward to email
- [ ] Archive
'''

            # Use timestamp directly for filename
            import time as time_module
            timestamp_str = str(int(time_module.time() * 1000))
            filename = f"WHATSAPP_{message['chat'].replace(' ', '_')}_{timestamp_str}.md"
            filepath = self.needs_action / filename
            filepath.write_text(content, encoding='utf-8')

            self.logger.info(f"Created: {filepath}")
            print(f"Created file: {filepath.name}")
            return filepath

        except Exception as e:
            self.logger.error(f"File creation error: {e}")
            print(f"File error: {e}")
            return Path("error")

    def check_for_updates(self):
        """Check for new messages periodically"""
        try:
            messages = self.extract_messages()
            for message in messages:
                self.create_action_file(message)
        except Exception as e:
            self.logger.error(f"Check error: {e}")
            print(f"Check error: {e}")

    def run(self):
        """Main watcher loop"""
        try:
            self.launch_browser()
            self.navigate_to_whatsapp()

            self.logger.info(f"Starting polling every {self.check_interval}s")
            print(f"Polling started - every {self.check_interval} seconds (Ctrl+C to stop)")

            while True:
                try:
                    self.check_for_updates()
                except Exception as e:
                    self.logger.error(f"Loop error: {e}")
                    print(f"Loop error: {e}")

                time.sleep(self.check_interval)

        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            print(f"Fatal error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")
                print("Browser closed")


def main():
    vault = "."
    session_path = "whatsapp_session"
    check_interval = 60

    try:
        watcher = WhatsAppWatcher(vault, session_path, check_interval)
        watcher.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()

