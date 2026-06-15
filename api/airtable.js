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

  const siteUrl = process.env.SITE_URL || `https://${req.headers.host}`;

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

    sendBrevoEmail({ fullname, email, langue: langue || 'FR', siteUrl }).catch(err =>
      console.error('Brevo error:', err)
    );

    return res.status(200).json({ success: true, id: atData.id });
  } catch (err) {
    console.error('Handler error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
};

const PDF_PATHS = {
  FR: '/assets/EXECIA_5Questions_Q4_2026_FR.pdf',
  EN: '/assets/EXECIA_5Questions_Q4_2026_EN.pdf',
  ES: '/assets/EXECIA_5Questions_Q4_2026_ES.pdf',
};

const EMAIL_COPY = {
  FR: {
    subject: "EXEC'IA — Les 5 Essentiels IA pour dirigeants",
    greeting: 'Bonjour',
    intro: "Merci de votre intérêt pour <strong>Les 5 Essentiels IA pour dirigeants</strong>. Retrouvez ci-dessous votre document à télécharger.",
    btn: 'Télécharger le document',
    note: "Ce lien vous permet d'accéder directement au PDF. Si le bouton ne s'affiche pas, copiez-collez ce lien dans votre navigateur :",
    rights: 'Tous droits réservés',
  },
  EN: {
    subject: "EXEC'IA — The 5 AI Essentials for Leaders",
    greeting: 'Hello',
    intro: "Thank you for your interest in <strong>The 5 AI Essentials for Leaders</strong>. Find your document below.",
    btn: 'Download the document',
    note: 'This link gives you direct access to the PDF. If the button does not display, copy and paste this link into your browser:',
    rights: 'All rights reserved',
  },
  ES: {
    subject: "EXEC'IA — Los 5 Esenciales de IA para Directivos",
    greeting: 'Hola',
    intro: "Gracias por su interés en <strong>Los 5 Esenciales de IA para Directivos</strong>. Encontrará su documento a continuación.",
    btn: 'Descargar el documento',
    note: 'Este enlace le da acceso directo al PDF. Si el botón no se muestra, copie y pegue este enlace en su navegador:',
    rights: 'Todos los derechos reservados',
  },
};

async function sendBrevoEmail({ fullname, email, langue, siteUrl }) {
  const lang = ['FR', 'EN', 'ES'].includes(langue) ? langue : 'FR';
  const copy = EMAIL_COPY[lang];
  const pdfUrl = siteUrl + PDF_PATHS[lang];

  const html = `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#F4EDE7;font-family:Helvetica,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F4EDE7;padding:40px 16px;">
<tr><td align="center">
<table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;">
  <tr>
    <td style="padding:0 0 28px 0;text-align:center;">
      <span style="font-family:Georgia,'Times New Roman',serif;font-size:22px;letter-spacing:.08em;color:#6B625D;font-weight:400;">EXEC'<span style="color:#C75F62;">IA</span></span>
    </td>
  </tr>
  <tr>
    <td style="background:#FAF6F2;border-radius:4px;padding:48px 44px;">
      <p style="font-family:Georgia,'Times New Roman',serif;font-size:26px;color:#6B625D;margin:0 0 20px 0;line-height:1.3;font-weight:400;">${copy.greeting} ${fullname},</p>
      <p style="font-size:15px;color:#6B625D;line-height:1.75;margin:0 0 36px 0;">${copy.intro}</p>
      <table cellpadding="0" cellspacing="0" style="margin:0 0 36px 0;">
        <tr>
          <td style="background:#C75F62;border-radius:2px;">
            <a href="${pdfUrl}" style="display:inline-block;padding:15px 36px;color:#FAF6F2;text-decoration:none;font-size:13px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;">${copy.btn}</a>
          </td>
        </tr>
      </table>
      <p style="font-size:12px;color:#B8B1AA;line-height:1.65;margin:0 0 8px 0;">${copy.note}</p>
      <p style="font-size:12px;color:#B8B1AA;line-height:1.65;margin:0;word-break:break-all;"><a href="${pdfUrl}" style="color:#B8B1AA;">${pdfUrl}</a></p>
    </td>
  </tr>
  <tr>
    <td style="padding:28px 0 0 0;text-align:center;">
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
      sender: { name: "EXEC'IA", email: 'contact@execia.fr' },
      to: [{ email, name: fullname }],
      subject: copy.subject,
      htmlContent: html,
    }),
  });

  if (!brevoRes.ok) {
    const errData = await brevoRes.json().catch(() => ({}));
    throw new Error(`Brevo ${brevoRes.status}: ${JSON.stringify(errData)}`);
  }
}
