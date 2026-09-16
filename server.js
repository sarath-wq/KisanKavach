const { createServer } = require('http');
const path = require('path');
const fs = require('fs');

process.env.NODE_ENV = 'production';

let app;
let handle;
let nextError = null;

try {
  const next = require('next');
  app = next({ dev: false, dir: __dirname });
  handle = app.getRequestHandler();
} catch (e) {
  nextError = e;
  console.error('Failed to load Next.js module:', e);
}

const port = process.env.PORT || 3000;

if (app) {
  app.prepare().then(() => {
    createServer((req, res) => {
      handle(req, res);
    }).listen(port, () => {
      console.log(`> KisanKavach ready on port ${port}`);
    });
  }).catch((err) => {
    console.error('Error preparing Next.js app:', err);
    // Fallback server to display error on browser instead of 500
    createServer((req, res) => {
      res.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`
        <h2>KisanKavach Server Startup Diagnostic</h2>
        <p><strong>Error:</strong> ${err.message}</p>
        <p>Check Node.js version in cPanel (Must be 18.x or 20.x).</p>
      `);
    }).listen(port);
  });
} else {
  createServer((req, res) => {
    res.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`
      <h2>KisanKavach Server Startup Diagnostic</h2>
      <p><strong>Module Error:</strong> ${nextError ? nextError.message : 'Unknown'}</p>
      <p>Please ensure node_modules directory is uploaded to server.</p>
    `);
  }).listen(port);
}
