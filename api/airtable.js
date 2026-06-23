const PDF_FILES = {
  FR: 'EXECIA_5%20Essentiels_Q4_2026_FR.pdf',
  EN: 'EXECIA_The%205%20Essentials_Q4_2026_EN.pdf',
  ES: 'EXECIA_Los%205%20Esenciales_Q4_2026_ES.pdf',
};

const PDF_NAMES = {
  FR: 'Les 5 Essentiels IA pour dirigeants — EXEC\'IA.pdf',
  EN: 'The 5 AI Essentials for Leaders — EXEC\'IA.pdf',
  ES: 'Los 5 Esenciales IA para Directivos — EXEC\'IA.pdf',
};

const EMAIL_COPY = {
  FR: {
    subject: "EXEC'IA — Les 5 Essentiels",
    greeting: 'Bonjour',
    body: (docName) => `Je suis heureuse de vous faire parvenir <strong>${docName}</strong>, que vous trouverez en pièce jointe.<br><br>Ces 5 questions sont celles que les directions générales ne peuvent plus se permettre d'ignorer. J'espère qu'elles nourriront votre réflexion.<br><br>Je reste disponible si vous souhaitez en échanger.<br><br>Bonne lecture,`,
    docName: 'Les 5 Essentiels IA pour dirigeants',
    rights: 'Tous droits réservés',
  },
  EN: {
    subject: "EXEC'IA — The 5 Essentials",
    greeting: 'Hello',
    body: (docName) => `I am pleased to share with you <strong>${docName}</strong>, which you will find attached.<br><br>These are the 5 questions no leadership team can afford to overlook. I hope they spark valuable reflection.<br><br>I am available should you wish to discuss them further.<br><br>Enjoy your reading,`,
    docName: 'The 5 AI Essentials for Leaders',
    rights: 'All rights reserved',
  },
  ES: {
    subject: "EXEC'IA — Los 5 Esenciales",
    greeting: 'Estimado/a',
    body: (docName) => `Me complace hacerle llegar <strong>${docName}</strong>, que encontrará en el archivo adjunto.<br><br>Estas son las 5 preguntas que ninguna dirección general puede permitirse ignorar. Espero que le aporten una reflexión valiosa.<br><br>Quedo a su entera disposición si desea comentarlas.<br><br>Buena lectura,`,
    docName: 'Los 5 Esenciales IA para Directivos',
    rights: 'Todos los derechos reservados',
  },
};

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { fullname, role, company, email, langue, document_telecharge, source } = req.body || {};

  if (!fullname || !email) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const now = new Date();
  const q = Math.ceil((now.getMonth() + 1) / 3);
  const trimestre = `Q${q} ${now.getFullYear()}`;

  const fields = {
    'Horodatage': now.toISOString(),
    'Trimestre': trimestre,
    'Statut': 'Nouveau',
    'Prénom_NOM': fullname,
    'Fonction': role || '',
    'Société': company || '',
    'Email professionnel': email,
    'Langue': langue || '',
    'Document téléchargé': document_telecharge || '',
    'Source acquisition': source || 'Direct',
  };

  const atUrl = `https://api.airtable.com/v0/${process.env.AIRTABLE_BASE_ID}/${encodeURIComponent(process.env.AIRTABLE_TABLE_NAME)}`;

  try {
    const atRes = await fetch(atUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.AIRTABLE_API_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ fields }),
    });

    const atData = await atRes.json();

    if (!atRes.ok) {
      console.error('Airtable error:', JSON.stringify(atData));
      return res.status(502).json({ error: 'Upstream error' });
    }

    try {
      await sendBrevoEmail({ fullname, email, langue: langue || 'FR' });
      console.log('Brevo OK:', email);
    } catch (err) {
      console.error('Brevo error:', err.message);
    }

    return res.status(200).json({ success: true, id: atData.id });
  } catch (err) {
    console.error('Handler error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

async function sendBrevoEmail({ fullname, email, langue }) {
  const lang = ['FR', 'EN', 'ES'].includes(langue) ? langue : 'FR';
  const copy = EMAIL_COPY[lang];
  const prenom = fullname.split(' ')[0];

  const baseUrl = process.env.SITE_URL || `https://${process.env.VERCEL_URL}`;
  const pdfUrl = `${baseUrl}/assets/${PDF_FILES[lang]}`;

  const signature = `
    <table cellpadding="0" cellspacing="0" style="margin-top:32px;border-top:1px solid #D9C9C3;padding-top:20px;">
      <tr>
        <td>
          <p style="margin:0 0 4px 0;font-family:Georgia,'Times New Roman',serif;font-size:15px;color:#6B625D;font-weight:400;">Valérie MAILLAND</p>
          <p style="margin:0 0 4px 0;font-size:13px;color:#B8B1AA;line-height:1.5;">Fondatrice &amp; Directrice Générale</p>
          <p style="margin:0 0 4px 0;font-size:13px;color:#B8B1AA;line-height:1.5;">
            <span style="font-family:Georgia,serif;color:#6B625D;">EXEC'<span style="color:#C75F62;">IA</span></span>
          </p>
          <p style="margin:8px 0 0 0;font-size:12px;color:#B8B1AA;line-height:1.6;">
            <a href="mailto:valerie@exec-ia.ai" style="color:#B8B1AA;text-decoration:none;">valerie@exec-ia.ai</a>
            &nbsp;|&nbsp;
            <a href="https://exec-ia.ai" style="color:#B8B1AA;text-decoration:none;">exec-ia.ai</a>
          </p>
        </td>
      </tr>
    </table>`;

  const html = `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#F4EDE7;font-family:Helvetica,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F4EDE7;padding:40px 16px;">
<tr><td align="center">
<table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;">
  <tr>
    <td style="padding:0 0 24px 0;text-align:center;">
      <span style="font-family:Georgia,'Times New Roman',serif;font-size:22px;letter-spacing:.08em;color:#6B625D;font-weight:400;">EXEC'<span style="color:#C75F62;">IA</span></span>
    </td>
  </tr>
  <tr>
    <td style="background:#FAF6F2;border-radius:4px;padding:44px;">
      <p style="font-family:Georgia,'Times New Roman',serif;font-size:22px;color:#6B625D;margin:0 0 28px 0;line-height:1.3;font-weight:400;">${copy.greeting} ${prenom},</p>
      <p style="font-size:15px;color:#6B625D;line-height:1.9;margin:0;">${copy.body(copy.docName)}</p>
      ${signature}
    </td>
  </tr>
  <tr>
    <td style="padding:24px 0 0 0;text-align:center;">
      <p style="font-size:11px;color:#B8B1AA;margin:0;line-height:1.6;font-family:Georgia,'Times New Roman',serif;">EXEC'<span style="color:#C75F62;">IA</span> &mdash; ${copy.rights}</p>
    </td>
  </tr>
</table>
</td></tr>
</table>
</body>
</html>`;

  const brevoRes = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: {
      'api-key': process.env.BREVO_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      sender: { name: "EXEC'IA — Valérie Mailland", email: 'valerie@exec-ia.ai' },
      to: [{ email, name: fullname }],
      subject: copy.subject,
      htmlContent: html,
      attachment: [{ url: pdfUrl, name: PDF_NAMES[lang] }],
    }),
  });

  if (!brevoRes.ok) {
    const errData = await brevoRes.json().catch(() => ({}));
    throw new Error(`Brevo ${brevoRes.status}: ${JSON.stringify(errData)}`);
  }
}
