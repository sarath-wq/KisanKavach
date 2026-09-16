const http = require('http');
const next = require('next');

process.env.NODE_ENV = 'production';
const port = process.env.PORT || 3000;

let handle = null;
const nextApp = next({ dev: false, dir: __dirname });

// Bind socket IMMEDIATELY to stop cPanel's infinite loading spinner
const server = http.createServer((req, res) => {
  if (handle) {
    handle(req, res);
  } else {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`
      <div style="font-family: sans-serif; text-align: center; padding: 60px; line-height: 1.6;">
        <h2 style="color: #059669; font-size: 24px; margin-bottom: 8px;">🌾 KisanKavach Karnataka Platform Starting...</h2>
        <p style="color: #475569; font-size: 14px;">Next.js App Router engine is preparing pages in background.</p>
        <p style="color: #94a3b8; font-size: 12px;">Auto-refreshing in 3 seconds...</p>
        <script>setTimeout(() => window.location.reload(), 3000);</script>
      </div>
    `);
  }
});

server.listen(port, () => {
  console.log(`> KisanKavach server bound immediately on port ${port}`);
  nextApp.prepare().then(() => {
    handle = nextApp.getRequestHandler();
    console.log('> Next.js handler ready!');
  }).catch((err) => {
    console.error('Next.js prepare error:', err);
  });
});
