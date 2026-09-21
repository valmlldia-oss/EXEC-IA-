// Formulaire « Une question ? » : la question arrive par e-mail (Brevo) dans la boîte EXEC'IA.
// Aucune donnée n'est stockée ici ; aucune IA ne répond au visiteur.
const TO = { email: 'contact@exec-ia.ai', name: "EXEC'IA" };

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { message, email, langue, page, website } = req.body || {};

  // Champ piège : un humain ne le remplit pas
  if (website) return res.status(200).json({ ok: true });

  const msg = typeof message === 'string' ? message.trim() : '';
  const mail = typeof email === 'string' ? email.trim() : '';
  if (msg.length < 3 || msg.length > 2000) return res.status(400).json({ error: 'Invalid message' });
  if (mail.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail)) return res.status(400).json({ error: 'Invalid email' });

  const lang = ['FR', 'EN', 'ES'].includes(String(langue).toUpperCase()) ? String(langue).toUpperCase() : 'FR';
  const from = typeof page === 'string' ? page.slice(0, 120) : '';

  const html = `<div style="font-family:Arial,sans-serif;color:#633B4A;line-height:1.6">
<p><strong>Nouvelle question depuis exec-ia.ai</strong> (${esc(lang)} · ${esc(from)})</p>
<p style="white-space:pre-wrap;border-left:3px solid #C75F62;padding-left:12px">${esc(msg)}</p>
<p>Répondre directement à : <strong>${esc(mail)}</strong></p></div>`;

  const r = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': process.env.BREVO_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sender: { name: "Site EXEC'IA", email: 'valerie@exec-ia.ai' },
      to: [TO],
      replyTo: { email: mail },
      subject: `Question du site (${lang}) — ${mail}`,
      htmlContent: html,
    }),
  });

  if (!r.ok) {
    console.error('Brevo question error:', r.status);
    return res.status(502).json({ error: 'Send failed' });
  }
  return res.status(200).json({ ok: true });
};
