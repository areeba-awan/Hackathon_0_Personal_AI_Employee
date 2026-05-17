import os
import time
import logging
import json
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("linkedin_watcher.log")]
)

class LinkedInAutomationWatcher:
    def __init__(self, vault_path: str, check_interval: int = 30):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.needs_action.mkdir(exist_ok=True)
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.info("Initializing LinkedIn Automation Watcher...")
        print("\n" + "="*70)
        print("LINKEDIN AUTOMATION WATCHER")
        print("="*70)

        self.driver = None
        self.is_logged_in = False
        self.session_file = Path("linkedin_session.json")
        self.processed_posts = set()
        self.load_session()

    def load_session(self):
        """Load previous session data"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    self.processed_posts = set(data.get('processed_posts', []))
                    self.logger.info("Session loaded")
                    print("[INFO] Session loaded from file")
            except Exception as e:
                self.logger.warning(f"Could not load session: {e}")

    def save_session(self):
        """Save session data"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump({'processed_posts': list(self.processed_posts)}, f)
        except Exception as e:
            self.logger.error(f"Could not save session: {e}")

    def setup_driver(self):
        """Setup Chrome driver"""
        try:
            print("\n[SETUP] Initializing Chrome driver...")
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-crash-reporter")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            self.logger.info("Chrome driver initialized")
            print("[OK] Chrome driver ready")
            return True
        except Exception as e:
            self.logger.error(f"Driver setup failed: {e}")
            print(f"[ERROR] Driver setup failed: {e}")
            return False

    def open_linkedin(self):
        """Open LinkedIn login page"""
        try:
            print("\n[ACTION] Opening LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            print("[OK] LinkedIn login page opened in browser")
            print("[WAIT] Please login manually in the browser window...")
            self.logger.info("LinkedIn login page loaded")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open LinkedIn: {e}")
            print(f"[ERROR] Failed to open LinkedIn: {e}")
            return False

    def wait_for_login(self) -> bool:
        """Wait for user to login"""
        try:
            print("\n[WAIT] Waiting for login (max 5 minutes)...")

            selectors = [
                (By.XPATH, "//div[@data-test-id='feed-container']"),
                (By.XPATH, "//main"),
                (By.XPATH, "//div[contains(@class, 'feed')]"),
            ]

            for selector in selectors:
                try:
                    WebDriverWait(self.driver, 300).until(
                        EC.presence_of_element_located(selector)
                    )
                    self.logger.info("Login detected!")
                    print("[OK] Login successful!")
                    return True
                except:
                    continue

            return False
        except Exception as e:
            self.logger.debug(f"Login wait error: {e}")
            return False

    def extract_feed_posts(self) -> list:
        """Extract posts from feed"""
        try:
            posts = []

            # Scroll to load more posts
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

            post_selectors = [
                "//div[@data-test-id='feed-container']//article",
                "//article",
            ]

            post_elements = []
            for selector in post_selectors:
                try:
                    post_elements = self.driver.find_elements(By.XPATH, selector)
                    if post_elements:
                        break
                except:
                    continue

            print(f"\n[SCAN] Found {len(post_elements)} posts on feed")

            for idx, post in enumerate(post_elements[:3]):
                try:
                    post_id = post.get_attribute("data-urn")
                    if not post_id:
                        post_id = f"post_{idx}_{datetime.now().timestamp()}"

                    if post_id in self.processed_posts:
                        continue

                    # Extract text
                    text_elem = post.find_elements(By.XPATH, ".//span[@dir='ltr']")
                    post_text = " ".join([elem.text for elem in text_elem if elem.text.strip()])[:300]

                    if not post_text:
                        text_elem = post.find_elements(By.XPATH, ".//p")
                        post_text = " ".join([elem.text for elem in text_elem if elem.text.strip()])[:300]

                    # Extract author
                    author_elem = post.find_elements(By.XPATH, ".//a[@data-test-id='feed-item-actor-name']")
                    author = author_elem[0].text if author_elem else "Unknown"

                    if post_text and post_text.strip():
                        posts.append({
                            'id': post_id,
                            'author': author,
                            'text': post_text,
                            'timestamp': datetime.now().isoformat()
                        })
                        print(f"[NEW] Post from {author}: {post_text[:50]}...")
                except Exception as e:
                    self.logger.debug(f"Error extracting post: {e}")
                    continue

            return posts
        except Exception as e:
            self.logger.error(f"Feed extraction error: {e}")
            print(f"[ERROR] Feed extraction: {e}")
            return []

    def post_comment_to_linkedin(self, post: dict, comment: str) -> bool:
        """Post engagement comment directly to LinkedIn post"""
        try:
            print(f"\n[POST] Attempting to post comment to {post['author']}'s post...")

            # Find the post element
            post_elements = self.driver.find_elements(By.XPATH, "//article")

            for post_elem in post_elements:
                try:
                    post_id = post_elem.get_attribute("data-urn")
                    if post_id != post['id']:
                        continue

                    # Scroll to post
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", post_elem)
                    time.sleep(1)

                    # Find comment button
                    comment_btn = post_elem.find_elements(By.XPATH, ".//button[contains(@aria-label, 'Comment')]")
                    if not comment_btn:
                        comment_btn = post_elem.find_elements(By.XPATH, ".//button[contains(@aria-label, 'comment')]")

                    if comment_btn:
                        comment_btn[0].click()
                        print("[ACTION] Comment box opened")
                        time.sleep(1)

                        # Find comment text area
                        comment_area = self.driver.find_elements(By.XPATH, "//div[@contenteditable='true'][@role='textbox']")
                        if comment_area:
                            comment_area[0].click()
                            comment_area[0].send_keys(comment)
                            print("[ACTION] Comment typed")
                            time.sleep(1)

                            # Find and click post button
                            post_btn = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Post')]")
                            if not post_btn:
                                post_btn = self.driver.find_elements(By.XPATH, "//button[@type='submit']")

                            if post_btn:
                                post_btn[0].click()
                                print("[OK] Comment posted successfully!")
                                self.logger.info(f"Posted comment to {post['author']}'s post")
                                return True
                except Exception as e:
                    self.logger.debug(f"Error posting to this post: {e}")
                    continue

            print("[WARN] Could not find post to comment on")
            return False
        except Exception as e:
            self.logger.error(f"Post comment error: {e}")
            print(f"[ERROR] Could not post comment: {e}")
            return False

    def auto_post_comments(self, posts: list) -> None:
        """Automatically post generated comments to LinkedIn"""
        try:
            print(f"\n[AUTO-POST] Starting auto-post for {len(posts)} posts...")

            for post in posts:
                try:
                    comment = self.generate_engagement_comment(post)
                    success = self.post_comment_to_linkedin(post, comment)

                    if success:
                        print(f"[SUCCESS] Posted to {post['author']}'s post")
                        time.sleep(3)  # Wait between posts
                    else:
                        print(f"[SKIP] Could not post to {post['author']}'s post")

                except Exception as e:
                    self.logger.error(f"Auto-post error for post: {e}")
                    print(f"[ERROR] Auto-post failed: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"Auto-post loop error: {e}")
            print(f"[ERROR] Auto-post error: {e}")

    def create_automation_task(self, post: dict) -> Path:
        """Create automation task in Needs_Action"""
        try:
            task_id = post['id'].replace(':', '_')
            engagement_comment = self.generate_engagement_comment(post)

            content = f"""---
type: linkedin_post
author: {post['author']}
source: LinkedIn Feed
detected: {post['timestamp']}
priority: high
status: pending
automation: true
---

## Post Content
{post['text']}

## Generated Engagement Comment
{engagement_comment}

## Automation Tasks
- [ ] Post engagement comment
- [ ] Schedule repost
- [ ] Add to content calendar
- [ ] Extract key insights
- [ ] Create follow-up post

## Suggested Actions
- Review and post comment
- Share with network
- Save for later reference
"""
            filepath = self.needs_action / f"LINKEDIN_{task_id}.md"
            filepath.write_text(content, encoding='utf-8')
            self.processed_posts.add(post['id'])
            self.save_session()

            self.logger.info(f"Created task: {filepath.name}")
            print(f"[TASK] Created: {filepath.name}")
            return filepath
        except Exception as e:
            self.logger.error(f"Task creation error: {e}")
            print(f"[ERROR] Task creation: {e}")
            return Path("error")

    def run(self):
        """Main automation loop"""
        if not self.setup_driver():
            print("[FATAL] Failed to setup driver")
            return

        if not self.open_linkedin():
            print("[FATAL] Failed to open LinkedIn")
            self.driver.quit()
            return

        if not self.wait_for_login():
            self.logger.error("Login timeout")
            print("[FATAL] Login timeout")
            self.driver.quit()
            return

        self.is_logged_in = True

        print("\n" + "="*70)
        print("AUTOMATION STARTED - MONITORING FEED")
        print("="*70)
        print(f"[INFO] Checking feed every {self.check_interval} seconds")
        print("[INFO] Auto-posting comments enabled")
        print("[INFO] Press Ctrl+C to stop\n")

        try:
            while True:
                try:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking feed...")
                    posts = self.extract_feed_posts()

                    if posts:
                        print(f"[PROCESS] Processing {len(posts)} new posts...")
                        for post in posts:
                            self.create_automation_task(post)
                            time.sleep(1)

                        # Auto-post comments
                        print(f"\n[AUTO-POST] Auto-posting comments to {len(posts)} posts...")
                        self.auto_post_comments(posts)
                    else:
                        print("[INFO] No new posts")

                    time.sleep(self.check_interval)
                except Exception as e:
                    self.logger.error(f"Loop error: {e}")
                    print(f"[ERROR] {e}")
                    time.sleep(5)
        except KeyboardInterrupt:
            self.logger.info("Watcher stopped by user")
            print("\n\n[STOP] Automation stopped")
        finally:
            self.driver.quit()
            self.logger.info("Driver closed")
            print("[OK] Browser closed")


if __name__ == "__main__":
    vault = "."

    try:
        watcher = LinkedInAutomationWatcher(vault, check_interval=30)
        watcher.run()
    except Exception as e:
        print(f"[FATAL] {e}")
        input("Press Enter to exit...")
