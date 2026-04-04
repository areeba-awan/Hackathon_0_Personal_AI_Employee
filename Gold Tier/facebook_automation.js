#!/usr/bin/env node

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const EventEmitter = require('events');

// Set Playwright browsers path to D drive
process.env.PLAYWRIGHT_BROWSERS_PATH = 'D:\\playwright-browsers';

class FacebookAutomation extends EventEmitter {
  constructor() {
    super();
    this.browser = null;
    this.context = null;
    this.page = null;
    this.sessionDir = path.join(process.cwd(), 'sessions', 'facebook');
    this.messagesFile = path.join(process.cwd(), 'facebook_messages.json');
    this.postsFile = path.join(process.cwd(), 'facebook_posts.json');
    this.isMonitoring = false;
    this.lastMessageCheck = 0;
    this.messageCheckInterval = 30000; // 30 seconds

    this.ensureDirectories();
    this.loadMessages();
    this.loadPosts();
  }

  ensureDirectories() {
    if (!fs.existsSync(this.sessionDir)) {
      fs.mkdirSync(this.sessionDir, { recursive: true });
    }
  }

  loadMessages() {
    if (fs.existsSync(this.messagesFile)) {
      try {
        this.messages = JSON.parse(fs.readFileSync(this.messagesFile, 'utf-8'));
      } catch (e) {
        this.messages = [];
      }
    } else {
      this.messages = [];
    }
  }

  loadPosts() {
    if (fs.existsSync(this.postsFile)) {
      try {
        this.posts = JSON.parse(fs.readFileSync(this.postsFile, 'utf-8'));
      } catch (e) {
        this.posts = [];
      }
    } else {
      this.posts = [];
    }
  }

  saveMessages() {
    fs.writeFileSync(this.messagesFile, JSON.stringify(this.messages, null, 2));
  }

  savePosts() {
    fs.writeFileSync(this.postsFile, JSON.stringify(this.posts, null, 2));
  }

  async initBrowser(headless = false) {
    if (!this.browser) {
      console.log('🌐 Initializing browser...');
      this.browser = await chromium.launchPersistentContext(this.sessionDir, {
        headless: headless,
        args: ['--disable-blink-features=AutomationControlled', '--no-sandbox']
      });
      this.page = await this.browser.newPage();
      console.log('✅ Browser initialized');
    }
    return this.page;
  }

  async closeBrowser() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.page = null;
      console.log('🔌 Browser closed');
    }
  }

  async login(email, password) {
    try {
      console.log('🔐 Checking login status...');
      await this.page.goto('https://www.facebook.com', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await this.page.waitForTimeout(2000);

      // Check if already logged in
      const isLoggedIn = await this.page.locator('[data-testid="feed"]').isVisible().catch(() => false);
      if (isLoggedIn) {
        console.log('✅ Already logged in');
        return { success: true, message: 'Already logged in' };
      }

      // Try to find login form
      const emailInput = this.page.locator('input[name="email"]');
      const emailExists = await emailInput.isVisible().catch(() => false);

      if (!emailExists) {
        console.log('✅ Session appears active');
        return { success: true, message: 'Session active' };
      }

      console.log('📝 Logging in...');
      await emailInput.fill(email);
      await this.page.locator('input[name="pass"]').fill(password);
      await this.page.locator('input[name="pass"]').press('Enter');

      await this.page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
      await this.page.waitForTimeout(3000);

      console.log('⏳ Waiting for 2FA verification (2 minutes)...');
      await this.page.waitForTimeout(120000);

      console.log('✅ Login successful');
      return { success: true, message: 'Login successful' };
    } catch (error) {
      console.error('❌ Login error:', error.message);
      return { success: false, error: error.message };
    }
  }

  async checkMessages() {
    try {
      console.log('📬 Checking for new messages...');

      // Navigate to messages
      await this.page.goto('https://www.facebook.com/messages', { waitUntil: 'domcontentloaded', timeout: 30000 });
      await this.page.waitForTimeout(3000);

      let newMessages = 0;

      // Try multiple selectors for message threads
      const selectors = [
        '[role="button"][data-testid*="message"]',
        '[data-testid="message-thread"]',
        'div[role="button"]:has(img)',
        'a[href*="/messages/t/"]'
      ];

      let threads = [];
      for (const selector of selectors) {
        try {
          const found = await this.page.locator(selector).all();
          if (found.length > 0) {
            threads = found;
            console.log(`Found ${threads.length} message threads using selector: ${selector}`);
            break;
          }
        } catch (e) {
          // Try next selector
        }
      }

      // Extract messages from threads
      for (let i = 0; i < Math.min(threads.length, 10); i++) {
        try {
          const thread = threads[i];
          const threadText = await thread.textContent().catch(() => '');
          const threadHtml = await thread.innerHTML().catch(() => '');

          if (!threadText || threadText.trim().length === 0) continue;

          // Create unique ID based on content hash
          const crypto = require('crypto');
          const messageHash = crypto.createHash('md5').update(threadText).digest('hex');
          const messageId = `msg_${messageHash}`;

          // Check if message already exists
          const existingMsg = this.messages.find(m => m.id === messageId);

          if (!existingMsg) {
            const newMsg = {
              id: messageId,
              text: threadText.substring(0, 200),
              fullText: threadText,
              timestamp: new Date().toISOString(),
              platform: 'facebook',
              read: false,
              source: 'real_facebook'
            };

            this.messages.push(newMsg);
            newMessages++;
            console.log(`✉️  New message: ${threadText.substring(0, 50)}...`);
            this.emit('newMessage', newMsg);
          }
        } catch (e) {
          console.log(`⚠️  Error processing thread ${i}: ${e.message}`);
        }
      }

      if (newMessages > 0) {
        this.saveMessages();
        console.log(`✅ Found ${newMessages} new messages`);
      } else {
        console.log('ℹ️  No new messages');
      }

      return { success: true, newMessages, totalMessages: this.messages.length };
    } catch (error) {
      console.error('❌ Message check error:', error.message);
      return { success: false, error: error.message };
    }
  }

  async post(message, imagePath = null) {
    try {
      console.log('📝 Creating post...');

      await this.page.goto('https://www.facebook.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
      await this.page.waitForTimeout(2000);

      // Check if logged in
      const isLoggedIn = await this.page.locator('[data-testid="feed"]').isVisible().catch(() => false);
      if (!isLoggedIn) {
        throw new Error('Not logged in to Facebook');
      }

      // Click create post button
      console.log('🖱️  Clicking create post...');
      await this.page.locator('text=/What\'s on your mind/i').first().click().catch(async () => {
        await this.page.locator('[aria-label="Create post"]').click();
      });

      await this.page.waitForTimeout(2000);

      // Type message
      console.log('✍️  Typing message...');
      const textbox = this.page.locator('[contenteditable="true"]').first();
      await textbox.click();
      await textbox.fill(message);

      // Upload image if provided
      if (imagePath && fs.existsSync(imagePath)) {
        console.log('🖼️  Uploading image...');
        const fileInput = this.page.locator('input[type="file"]').first();
        await fileInput.setInputFiles(imagePath);
        await this.page.waitForTimeout(3000);
      }

      // Click post button
      console.log('🚀 Posting...');
      await this.page.locator('button:has-text("Post")').last().click({ timeout: 15000 }).catch(async () => {
        await this.page.locator('div[role="button"]:has-text("Post")').click();
      });

      await this.page.waitForTimeout(3000);

      const postRecord = {
        id: `post_${Date.now()}`,
        message: message,
        image: imagePath || null,
        timestamp: new Date().toISOString(),
        platform: 'facebook',
        status: 'posted'
      };

      this.posts.push(postRecord);
      this.savePosts();

      console.log('✅ Post successful');
      this.emit('postCreated', postRecord);
      return { success: true, message: 'Posted successfully', postId: postRecord.id };
    } catch (error) {
      console.error('❌ Post error:', error.message);
      return { success: false, error: error.message };
    }
  }

  async startMonitoring(checkInterval = 30000) {
    if (this.isMonitoring) {
      console.log('⚠️  Already monitoring');
      return;
    }

    this.isMonitoring = true;
    console.log(`🔄 Starting monitoring (check every ${checkInterval / 1000}s)...`);

    const monitor = async () => {
      if (!this.isMonitoring) return;

      try {
        await this.checkMessages();
      } catch (error) {
        console.error('Monitor error:', error.message);
      }

      if (this.isMonitoring) {
        setTimeout(monitor, checkInterval);
      }
    };

    monitor();
  }

  async stopMonitoring() {
    this.isMonitoring = false;
    console.log('⏹️  Monitoring stopped');
  }

  getMessages() {
    return this.messages;
  }

  getPosts() {
    return this.posts;
  }

  getStats() {
    return {
      totalMessages: this.messages.length,
      unreadMessages: this.messages.filter(m => !m.read).length,
      totalPosts: this.posts.length,
      isMonitoring: this.isMonitoring
    };
  }
}

// CLI Usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  const automation = new FacebookAutomation();

  // Event listeners
  automation.on('newMessage', (msg) => {
    console.log(`\n📨 NEW MESSAGE: ${msg.text}\n`);
  });

  automation.on('postCreated', (post) => {
    console.log(`\n📤 POST CREATED: ${post.message}\n`);
  });

  (async () => {
    try {
      await automation.initBrowser(false); // headless: false - BROWSER KHUL JAYEGA

      if (command === 'login') {
        const email = args[1];
        const password = args[2];
        if (!email || !password) {
          console.error('Usage: node facebook_automation.js login <email> <password>');
          process.exit(1);
        }
        const result = await automation.login(email, password);
        console.log(JSON.stringify(result));
      } else if (command === 'post') {
        const message = args[1];
        const imagePath = args[2] || null;
        if (!message) {
          console.error('Usage: node facebook_automation.js post "message" [image_path]');
          process.exit(1);
        }
        const result = await automation.post(message, imagePath);
        console.log(JSON.stringify(result));
      } else if (command === 'check-messages') {
        const result = await automation.checkMessages();
        console.log(JSON.stringify(result));
      } else if (command === 'monitor') {
        const interval = parseInt(args[1]) || 30000;
        await automation.startMonitoring(interval);
        console.log('Monitoring active. Press Ctrl+C to stop.');
        // Keep process alive
        process.on('SIGINT', async () => {
          await automation.stopMonitoring();
          await automation.closeBrowser();
          process.exit(0);
        });
      } else if (command === 'stats') {
        const stats = automation.getStats();
        console.log(JSON.stringify(stats, null, 2));
      } else {
        console.log(`
Facebook Automation Tool

Commands:
  login <email> <password>     - Login to Facebook
  post "message" [image]       - Post to Facebook
  check-messages               - Check for new messages
  monitor [interval_ms]        - Start monitoring (default 30000ms)
  stats                        - Show statistics

Examples:
  node facebook_automation.js login user@gmail.com password123
  node facebook_automation.js post "Hello World"
  node facebook_automation.js post "Check this out" /path/to/image.jpg
  node facebook_automation.js monitor 30000
  node facebook_automation.js check-messages
        `);
      }
    } catch (error) {
      console.error('Fatal error:', error.message);
      process.exit(1);
    } finally {
      if (command !== 'monitor') {
        await automation.closeBrowser();
      }
    }
  })();
}

module.exports = FacebookAutomation;
