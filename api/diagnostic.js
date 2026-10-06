// Mini-diagnostic ROBOT : le visiteur demande un retour personnalisé.
// Uniquement si la case de consentement est cochée :
// 1) une ligne est ajoutée dans Airtable, table « Mini-diagnostic ROBOT »
//    (même base que « Les 5 Essentiels » : un lead magnet = une table) ;
// 2) le diagnostic arrive par e-mail (Brevo) dans la boîte EXEC'IA.
// Aucune IA ne répond au visiteur : Valérie répond elle-même.
const AT_TABLE = 'tblVi0h9xu20qIlHt'; // Mini-diagnostic ROBOT
const TO = { email: 'contact@exec-ia.ai', name: "EXEC'IA" };

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { email, consent, diagnostic, langue, page, website, pct } = req.body || {};

  // Champ piège : un humain ne le remplit pas
  if (website) return res.status(200).json({ ok: true });

  // Consentement obligatoire (RGPD) : sans case cochée, rien n'est envoyé
  if (consent !== true) return res.status(400).json({ error: 'Consent required' });

  const mail = typeof email === 'string' ? email.trim() : '';
  if (mail.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail)) return res.status(400).json({ error: 'Invalid email' });

  const diag = typeof diagnostic === 'string' ? diagnostic.trim() : '';
  if (diag.length < 10 || diag.length > 6000) return res.status(400).json({ error: 'Invalid diagnostic' });

  const lang = ['FR', 'EN', 'ES'].includes(String(langue).toUpperCase()) ? String(langue).toUpperCase() : 'FR';
  const from = typeof page === 'string' ? page.slice(0, 120) : '';

  const part = Number.isFinite(+pct) ? Math.max(0, Math.min(100, Math.round(+pct))) : null;

  // 1) Airtable (une erreur ici n'empêche pas l'e-mail)
  try {
    const fields = { 'Email professionnel': mail, 'Horodatage': new Date().toISOString(), 'Langue': lang, 'Consentement': true, 'Diagnostic': diag, 'Page': from, 'Statut': 'Nouveau' };
    if (part !== null) fields['Part robotisable (%)'] = part;
    const at = await fetch(`https://api.airtable.com/v0/${process.env.AIRTABLE_BASE_ID}/${AT_TABLE}`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${process.env.AIRTABLE_API_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ fields, typecast: true }),
    });
    if (!at.ok) console.error('Airtable diagnostic error:', at.status, JSON.stringify(await at.json().catch(() => ({}))));
  } catch (e) { console.error('Airtable diagnostic exception:', e.message); }

  // 2) E-mail
  const html = `<div style="font-family:Arial,sans-serif;color:#633B4A;line-height:1.6">
<p><strong>Nouveau mini-diagnostic ROBOT</strong> (${esc(lang)} · ${esc(from)})</p>
<p>Le visiteur a coché la case : il accepte d'être recontacté au sujet de ce diagnostic.</p>
<p>Répondre directement à : <strong>${esc(mail)}</strong></p>
<p style="white-space:pre-wrap;border-left:3px solid #C75F62;padding-left:12px">${esc(diag)}</p></div>`;

  const r = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': process.env.BREVO_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sender: { name: "Site EXEC'IA", email: 'valerie@exec-ia.ai' },
      to: [TO],
      replyTo: { email: mail },
      subject: `Mini-diagnostic ROBOT (${lang}) : ${mail}`,
      htmlContent: html,
    }),
  });

  if (!r.ok) {
    console.error('Brevo diagnostic error:', r.status);
    return res.status(502).json({ error: 'Send failed' });
  }
  return res.status(200).json({ ok: true });
};
