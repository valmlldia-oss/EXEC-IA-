// Bulle « IA » : relaie la question du visiteur vers l'agent PHARE #1 (Make) et renvoie sa réponse.
// L'adresse du webhook reste côté serveur ; aucune donnée n'est stockée ici.
const WEBHOOK_URL = 'https://hook.eu1.make.com/hpwovottqaxnrjna3tyvv6b84v6dn1yx';

// Limite simple par adresse IP : 10 messages par tranche de 10 minutes
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 10;
const hits = new Map();

function tooMany(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  list.push(now);
  hits.set(ip, list);
  if (hits.size > 5000) hits.clear();
  return list.length > MAX_PER_WINDOW;
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { message, langue, page, website } = req.body || {};

  // Champ piège : un humain ne le remplit pas
  if (website) return res.status(200).json({ reply: null });

  const msg = typeof message === 'string' ? message.trim() : '';
  if (msg.length < 2 || msg.length > 1000) return res.status(400).json({ error: 'Invalid message' });

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (tooMany(ip)) return res.status(429).json({ reply: null });

  const lang = ['FR', 'EN', 'ES'].includes(String(langue).toUpperCase()) ? String(langue).toUpperCase() : 'FR';
  const from = typeof page === 'string' ? page.slice(0, 120) : '';

  try {
    const r = await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, langue: lang, page: from }),
      signal: AbortSignal.timeout(85000),
    });
    const text = await r.text();
    let reply = null;
    try { reply = JSON.parse(text).reply || null; } catch (e) { reply = null; } // « Accepted » : agent inactif
    return res.status(200).json({ reply });
  } catch (e) {
    console.error('PHARE relay error:', e.name);
    return res.status(200).json({ reply: null });
  }
};
