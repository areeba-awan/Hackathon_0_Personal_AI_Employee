#!/usr/bin/env node

const FacebookMaster = require('./facebook_master.js');
const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
const email = args[0];
const password = args[1];
const messages = args.slice(2);

if (!email || !password) {
  console.log(`
Usage: node facebook_run.js <email> <password> [message1] [message2] ...

Examples:
  node facebook_run.js user@gmail.com pass123
  node facebook_run.js user@gmail.com pass123 "Hello World"
  node facebook_run.js user@gmail.com pass123 "Post 1" "Post 2" "Post 3"
  `);
  process.exit(1);
}

(async () => {
  const master = new FacebookMaster();

  // Set email and password
  master.setConfig({
    email: email,
    password: password,
    autoLogin: true,
    headless: false
  });

  // Add messages if provided
  if (messages.length > 0) {
    master.config.autoPost = messages.map(msg => ({ message: msg, image: null }));
    master.saveConfig();
  }

  // Start automation
  await master.start();
})();
