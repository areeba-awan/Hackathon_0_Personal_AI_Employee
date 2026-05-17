
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