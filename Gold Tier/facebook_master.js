#!/usr/bin/env node

const FacebookAutomation = require('./facebook_automation.js');
const fs = require('fs');
const path = require('path');

class FacebookMaster {
  constructor() {
    this.automation = new FacebookAutomation();
    this.configFile = path.join(process.cwd(), 'facebook_config.json');
    this.config = this.loadConfig();
    this.isRunning = false;
  }

  loadConfig() {
    if (fs.existsSync(this.configFile)) {
      try {
        return JSON.parse(fs.readFileSync(this.configFile, 'utf-8'));
      } catch (e) {
        return this.getDefaultConfig();
      }
    }
    return this.getDefaultConfig();
  }

  getDefaultConfig() {
    return {
      email: process.env.FACEBOOK_EMAIL || '',
      password: process.env.FACEBOOK_PASSWORD || '',
      autoPost: [],
      monitorInterval: 30000,
      autoLogin: true,
      headless: false,
      enabled: true
    };
  }

  saveConfig() {
    fs.writeFileSync(this.configFile, JSON.stringify(this.config, null, 2));
  }

  async start() {
    if (this.isRunning) {
      console.log('⚠️  Already running');
      return;
    }

    this.isRunning = true;
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║   FACEBOOK AUTOMATION - MASTER START   ║');
    console.log('╚════════════════════════════════════════╝\n');

    try {
      // Step 1: Initialize browser
      console.log('📱 Step 1: Initializing browser...');
      await this.automation.initBrowser(this.config.headless === true);
      console.log('✅ Browser ready\n');

      // Step 2: Auto-login if configured
      if (this.config.autoLogin && this.config.email && this.config.password) {
        console.log('🔐 Step 2: Auto-logging in...');
        const loginResult = await this.automation.login(this.config.email, this.config.password);
        if (loginResult.success) {
          console.log('✅ Login successful\n');
        } else {
          console.log('⚠️  Login failed:', loginResult.error);
          console.log('   Please login manually in the browser\n');
        }
      } else {
        console.log('🔐 Step 2: Waiting for manual login...');
        console.log('   Please login in the browser window\n');
      }

      // Step 3: Start monitoring
      console.log('🔄 Step 3: Starting message monitoring...');
      await this.automation.startMonitoring(this.config.monitorInterval);
      console.log(`✅ Monitoring active (every ${this.config.monitorInterval / 1000}s)\n`);

      // Step 4: Auto-post if configured
      if (this.config.autoPost && this.config.autoPost.length > 0) {
        console.log('📤 Step 4: Auto-posting messages...');
        for (const postConfig of this.config.autoPost) {
          try {
            const result = await this.automation.post(postConfig.message, postConfig.image || null);
            if (result.success) {
              console.log(`✅ Posted: "${postConfig.message.substring(0, 40)}..."`);
            } else {
              console.log(`❌ Failed to post: ${result.error}`);
            }
            await this.sleep(5000); // Wait 5 seconds between posts
          } catch (e) {
            console.log(`❌ Post error: ${e.message}`);
          }
        }
        console.log('');
      }

      // Step 5: Show status
      console.log('📊 Step 5: System Status');
      this.showStatus();

      console.log('\n✅ Facebook Automation is now running!');
      console.log('   Messages will be monitored automatically');
      console.log('   Press Ctrl+C to stop\n');

      // Keep process alive
      process.on('SIGINT', async () => {
        await this.stop();
      });

    } catch (error) {
      console.error('❌ Fatal error:', error.message);
      await this.stop();
      process.exit(1);
    }
  }

  async stop() {
    console.log('\n\n⏹️  Stopping Facebook Automation...');
    this.isRunning = false;
    await this.automation.stopMonitoring();
    await this.automation.closeBrowser();
    console.log('✅ Stopped\n');
    process.exit(0);
  }

  showStatus() {
    const stats = this.automation.getStats();
    console.log(`
    📬 Messages: ${stats.totalMessages} (${stats.unreadMessages} unread)
    📤 Posts: ${stats.totalPosts}
    🔄 Monitoring: ${stats.isMonitoring ? 'Active' : 'Inactive'}
    `);
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async postMessage(message, imagePath = null) {
    if (!this.isRunning) {
      console.log('❌ Automation not running');
      return;
    }
    const result = await this.automation.post(message, imagePath);
    return result;
  }

  async checkMessages() {
    const result = await this.automation.checkMessages();
    return result;
  }

  getMessages() {
    return this.automation.getMessages();
  }

  getPosts() {
    return this.automation.getPosts();
  }

  setConfig(newConfig) {
    this.config = { ...this.config, ...newConfig };
    this.saveConfig();
    console.log('✅ Config updated');
  }
}

// CLI Usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  const master = new FacebookMaster();

  if (command === 'start') {
    master.start().catch(err => {
      console.error('Error:', err.message);
      process.exit(1);
    });
  } else if (command === 'post') {
    const message = args[1];
    const imagePath = args[2] || null;
    if (!message) {
      console.error('Usage: node facebook_master.js post "message" [image_path]');
      process.exit(1);
    }
    (async () => {
      await master.automation.initBrowser(false);
      const result = await master.automation.post(message, imagePath);
      console.log(JSON.stringify(result, null, 2));
      await master.automation.closeBrowser();
    })();
  } else if (command === 'config') {
    const subcommand = args[1];
    if (subcommand === 'set') {
      const key = args[2];
      const value = args[3];
      if (!key || !value) {
        console.error('Usage: node facebook_master.js config set <key> <value>');
        process.exit(1);
      }
      master.config[key] = value === 'true' ? true : value === 'false' ? false : value;
      master.saveConfig();
      console.log(`✅ ${key} = ${value}`);
    } else if (subcommand === 'show') {
      console.log(JSON.stringify(master.config, null, 2));
    } else if (subcommand === 'add-post') {
      const message = args[2];
      if (!message) {
        console.error('Usage: node facebook_master.js config add-post "message"');
        process.exit(1);
      }
      master.config.autoPost.push({ message, image: null });
      master.saveConfig();
      console.log(`✅ Added post: "${message}"`);
    } else {
      console.log(`
Config Commands:
  config show              - Show current config
  config set <key> <val>   - Set config value
  config add-post "msg"    - Add auto-post message

Config Keys:
  email                    - Facebook email
  password                 - Facebook password
  autoLogin                - Auto-login (true/false)
  headless                 - Headless mode (true/false)
  monitorInterval          - Check interval in ms
      `);
    }
  } else {
    console.log(`
Facebook Master Automation

Commands:
  start                    - Start automation (login, monitor, post)
  post "message" [image]   - Post a message
  config show              - Show configuration
  config set <key> <val>   - Set configuration
  config add-post "msg"    - Add auto-post message

Quick Start:
  1. node facebook_master.js config set email your@email.com
  2. node facebook_master.js config set password yourpassword
  3. node facebook_master.js config add-post "Hello World"
  4. node facebook_master.js start

The browser will open automatically and:
  ✓ Login to Facebook
  ✓ Start monitoring messages
  ✓ Auto-post configured messages
    `);
  }
}

module.exports = FacebookMaster;
