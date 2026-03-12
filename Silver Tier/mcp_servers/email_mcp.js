// const express = require('express');
// const nodemailer = require('nodemailer');
// const app = express();
// const port = 3000;

// app.use(express.json());

// // Gmail transporter (app password use karo)
// const transporter = nodemailer.createTransport({
//   service: 'gmail',
//   auth: {
//     user: 'awanareeba40@gmail.com',          // apna Gmail
//     pass: 'uiar zmjs olru yfdn'              // Gmail se app password banao
//   }
// });

// app.post('/send_email', async (req, res) => {
//   const { to, subject, body } = req.body;

//   try {
//     await transporter.sendMail({
//       from: 'YOUR_GMAIL@gmail.com',
//       to,
//       subject,
//       text: body
//     });
//     res.json({ success: true, message: 'Email sent successfully' });
//   } catch (error) {
//     res.status(500).json({ success: false, error: error.message });
//   }
// });

// app.listen(port, () => {
//   console.log(`MCP Email server running at http://localhost:${port}`);
// // });
// const express = require('express');
// const nodemailer = require('nodemailer');
// const { google } = require('googleapis');

// const app = express();
// const port = 3000;

// app.use(express.json());

// // === Naye Credentials (Web Client ke) ===
// const CLIENT_ID = '384544522431-g9sbpcbuqgi340cdeitfifvu99r1kcq0.apps.googleusercontent.com';      // ← Naya Web Client ID
// const CLIENT_SECRET = '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'; // ← Naya Client Secret
// const REFRESH_TOKEN = '1//04IndPJbGFsWfCgYIARAAGAQSNwF-L9IrVRvIEA0rpsmb9N73kGd-XjHf6OWJPsUBOQepRQqJ1GqxleOFXHNK_BsN2YnDOItKavc';    // ← Playground se naya mila
// const USER_EMAIL = 'awanareeba40@gmail.com';

// const oauth2Client = new google.auth.OAuth2(
//   CLIENT_ID,
//   CLIENT_SECRET,
//   'https://developers.google.com/oauthplayground'  // Exact redirect URI
// );

// oauth2Client.setCredentials({
//   refresh_token: REFRESH_TOKEN
// });

// const transporter = nodemailer.createTransport({
//   service: 'gmail',
//   auth: {
//     type: 'OAuth2',
//     user: USER_EMAIL,
//     clientId: CLIENT_ID,
//     clientSecret: CLIENT_SECRET,
//     refreshToken: REFRESH_TOKEN,
//     accessToken: await oauth2Client.getAccessToken()
//   }
// });

// app.post('/send_email', async (req, res) => {
//   const { to, subject, body } = req.body;

//   if (!to || !subject || !body) {
//     return res.status(400).json({ success: false, error: 'Missing fields: to, subject, body' });
//   }

//   try {
//     const info = await transporter.sendMail({
//       from: USER_EMAIL,
//       to: to,
//       subject: subject,
//       text: body
//     });
//     console.log('Email sent:', info.messageId);
//     res.json({ success: true, message: 'Email sent', messageId: info.messageId });
//   } catch (error) {
//     console.error('Send error:', error);
//     res.status(500).json({ success: false, error: error.message });
//   }
// });

// app.listen(port, () => {
//   console.log(`MCP Email server running at http://localhost:${port}`);
// });

// ############### NEW FILE WORK 

// const express = require('express');
// const nodemailer = require('nodemailer');
// const { google } = require('googleapis');

// const app = express();
// const port = 3000;

// app.use(express.json());

// // ===== Gmail OAuth2 Credentials =====
// const CLIENT_ID = '384544522431-g9sbpcbuqgi340cdeitfifvu99r1kcq0.apps.googleusercontent.com';
// const CLIENT_SECRET = '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';
// const REFRESH_TOKEN = '1//04IndPJbGFsWfCgYIARAAGAQSNwF-L9IrVRvIEA0rpsmb9N73kGd-XjHf6OWJPsUBOQepRQqJ1GqxleOFXHNK_BsN2YnDOItKavc';
// const USER_EMAIL = 'awanareeba40@gmail.com';

// // ===== OAuth2 Client =====
// const oauth2Client = new google.auth.OAuth2(
//   CLIENT_ID,
//   CLIENT_SECRET,
//   'https://developers.google.com/oauthplayground'
// );

// oauth2Client.setCredentials({
//   refresh_token: REFRESH_TOKEN
// });

// // ===== Create Transporter Function =====
// async function createTransporter() {

//   const accessToken = await oauth2Client.getAccessToken();

//   return nodemailer.createTransport({
//     service: 'gmail',
//     auth: {
//       type: 'OAuth2',
//       user: USER_EMAIL,
//       clientId: CLIENT_ID,
//       clientSecret: CLIENT_SECRET,
//       refreshToken: REFRESH_TOKEN,
//       accessToken: accessToken.token
//     }
//   });

// }

// // ===== Email Endpoint =====
// app.post('/send_email', async (req, res) => {

//   const { to, subject, body } = req.body;

//   if (!to || !subject || !body) {
//     return res.status(400).json({
//       success: false,
//       error: 'Missing fields: to, subject, body'
//     });
//   }

//   try {

//     const transporter = await createTransporter();

//     const info = await transporter.sendMail({
//       from: USER_EMAIL,
//       to: to,
//       subject: subject,
//       text: body
//     });

//     console.log('Email sent:', info.messageId);

//     res.json({
//       success: true,
//       message: 'Email sent successfully',
//       messageId: info.messageId
//     });

//   } catch (error) {

//     console.error('Send error:', error);

//     res.status(500).json({
//       success: false,
//       error: error.message
//     });

//   }

// });

// // ===== Start Server =====
// app.listen(port, () => {
//   console.log(`MCP Email server running at http://localhost:${port}`);
// });

// ******************* FINAL WORKING FILE *******************

const express = require('express');
const nodemailer = require('nodemailer');

const app = express();
const port = 3000;

app.use(express.json());

// Gmail details
const USER_EMAIL = 'awanareeba40@gmail.com';
const APP_PASSWORD = 'icnt jjiy uxgd iahi'; // یہاں اپنا App Password ڈالنا ہے

// Nodemailer transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: USER_EMAIL,
    pass: APP_PASSWORD
  }
});

// Email API
app.post('/send_email', async (req, res) => {

  const { to, subject, body } = req.body;

  if (!to || !subject || !body) {
    return res.status(400).json({
      success: false,
      error: 'Missing fields'
    });
  }

  try {

    const info = await transporter.sendMail({
      from: USER_EMAIL,
      to: to,
      subject: subject,
      text: body
    });

    console.log('Email sent:', info.messageId);

    res.json({
      success: true,
      message: 'Email sent successfully',
      id: info.messageId
    });

  } catch (error) {

    console.error(error);

    res.status(500).json({
      success: false,
      error: error.message
    });

  }

});

app.listen(port, () => {
  console.log(`Email MCP server running at http://localhost:${port}`);
});