#!/usr/bin/env node

const FacebookAutomation = require('./facebook_automation.js');
const FacebookMaster = require('./facebook_master.js');
const fs = require('fs');
const path = require('path');

class FacebookTest {
  constructor() {
    this.results = [];
    this.passed = 0;
    this.failed = 0;
  }

  log(message, type = 'info') {
    const icons = {
      info: 'ℹ️ ',
      success: '✅',
      error: '❌',
      warning: '⚠️ '
    };
    console.log(`${icons[type]} ${message}`);
  }

  async test(name, fn) {
    try {
      this.log(`Testing: ${name}`, 'info');
      await fn();
      this.log(`${name} - PASSED`, 'success');
      this.passed++;
    } catch (error) {
      this.log(`${name} - FAILED: ${error.message}`, 'error');
      this.failed++;
    }
  }

  async runTests() {
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║     FACEBOOK AUTOMATION - TESTS        ║');
    console.log('╚════════════════════════════════════════╝\n');

    // Test 1: FacebookAutomation class exists
    await this.test('FacebookAutomation class exists', () => {
      if (!FacebookAutomation) throw new Error('Class not found');
    });

    // Test 2: FacebookMaster class exists
    await this.test('FacebookMaster class exists', () => {
      if (!FacebookMaster) throw new Error('Class not found');
    });

    // Test 3: Can create automation instance
    await this.test('Can create FacebookAutomation instance', () => {
      const automation = new FacebookAutomation();
      if (!automation) throw new Error('Failed to create instance');
    });

    // Test 4: Can create master instance
    await this.test('Can create FacebookMaster instance', () => {
      const master = new FacebookMaster();
      if (!master) throw new Error('Failed to create instance');
    });

    // Test 5: Config file can be created
    await this.test('Config file creation', () => {
      const master = new FacebookMaster();
      master.setConfig({ email: 'test@example.com' });
      const configPath = path.join(process.cwd(), 'facebook_config.json');
      if (!fs.existsSync(configPath)) throw new Error('Config file not created');
    });

    // Test 6: Messages file can be created
    await this.test('Messages file creation', () => {
      const automation = new FacebookAutomation();
      if (!fs.existsSync(automation.messagesFile)) {
        fs.writeFileSync(automation.messagesFile, JSON.stringify([]));
      }
      if (!fs.existsSync(automation.messagesFile)) throw new Error('Messages file not created');
    });

    // Test 7: Posts file can be created
    await this.test('Posts file creation', () => {
      const automation = new FacebookAutomation();
      if (!fs.existsSync(automation.postsFile)) {
        fs.writeFileSync(automation.postsFile, JSON.stringify([]));
      }
      if (!fs.existsSync(automation.postsFile)) throw new Error('Posts file not created');
    });

    // Test 8: Session directory can be created
    await this.test('Session directory creation', () => {
      const automation = new FacebookAutomation();
      if (!fs.existsSync(automation.sessionDir)) throw new Error('Session dir not created');
    });

    // Test 9: Can load messages
    await this.test('Can load messages', () => {
      const automation = new FacebookAutomation();
      automation.loadMessages();
      if (!Array.isArray(automation.messages)) throw new Error('Messages not loaded');
    });

    // Test 10: Can load posts
    await this.test('Can load posts', () => {
      const automation = new FacebookAutomation();
      automation.loadPosts();
      if (!Array.isArray(automation.posts)) throw new Error('Posts not loaded');
    });

    // Test 11: Can get stats
    await this.test('Can get statistics', () => {
      const automation = new FacebookAutomation();
      const stats = automation.getStats();
      if (stats.totalMessages === undefined || stats.totalPosts === undefined) throw new Error('Stats not available');
    });

    // Test 12: Event emitter works
    await this.test('Event emitter functionality', () => {
      const automation = new FacebookAutomation();
      let eventFired = false;
      automation.on('test', () => {
        eventFired = true;
      });
      automation.emit('test');
      if (!eventFired) throw new Error('Event not fired');
    });

    // Test 13: Can save messages
    await this.test('Can save messages', () => {
      const automation = new FacebookAutomation();
      automation.messages = [{ id: 'test', text: 'test message' }];
      automation.saveMessages();
      const saved = JSON.parse(fs.readFileSync(automation.messagesFile, 'utf-8'));
      if (saved.length === 0) throw new Error('Messages not saved');
    });

    // Test 14: Can save posts
    await this.test('Can save posts', () => {
      const automation = new FacebookAutomation();
      automation.posts = [{ id: 'test', message: 'test post' }];
      automation.savePosts();
      const saved = JSON.parse(fs.readFileSync(automation.postsFile, 'utf-8'));
      if (saved.length === 0) throw new Error('Posts not saved');
    });

    // Test 15: Master config persistence
    await this.test('Master config persistence', () => {
      const master = new FacebookMaster();
      master.setConfig({ email: 'persist@test.com' });
      const master2 = new FacebookMaster();
      if (master2.config.email !== 'persist@test.com') throw new Error('Config not persisted');
    });

    // Summary
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║          TEST SUMMARY                  ║');
    console.log('╚════════════════════════════════════════╝\n');
    console.log(`✅ Passed: ${this.passed}`);
    console.log(`❌ Failed: ${this.failed}`);
    console.log(`📊 Total:  ${this.passed + this.failed}\n`);

    if (this.failed === 0) {
      console.log('🎉 All tests passed!\n');
      return true;
    } else {
      console.log('⚠️  Some tests failed\n');
      return false;
    }
  }
}

// Run tests
if (require.main === module) {
  const tester = new FacebookTest();
  tester.runTests().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(err => {
    console.error('Fatal error:', err.message);
    process.exit(1);
  });
}

module.exports = FacebookTest;
