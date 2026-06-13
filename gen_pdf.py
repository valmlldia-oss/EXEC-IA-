#!/usr/bin/env python3
"""EXEC'IA — Les 5 Décisions IA des Dirigeants · 7 pages"""

from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

W, H = A4

PLUM       = HexColor('#633B4A')
PLUM_DARK  = HexColor('#3D2030')
TERRACOTTA = HexColor('#C75F62')
IVORY      = HexColor('#F4EDE7')
IVORY_CARD = HexColor('#FAF6F2')
IVORY_TINT = HexColor('#EDE3DD')
WHITE      = HexColor('#FCFCFA')
GREY       = HexColor('#9A8E8A')
TEXT       = HexColor('#3D2030')
ROSE_MIN   = HexColor('#D9C9C3')

M  = 18*mm
CW = W - 2*M

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fonts_pdf')
OUT = '/Users/valeriemailland/Desktop/execia-v1-prune/assets/EXECIA_5_Priorites_IA_Dirigeants.pdf'

def reg():
    fonts = {
        'CGB':  'CormorantGaramond-Bold.ttf',
        'CGR':  'CormorantGaramond-Regular.ttf',
        'CGI':  'CormorantGaramond-Italic.ttf',
        'CGSB': 'CormorantGaramond-SemiBold.ttf',
        'IR':   'Inter-Regular.ttf',
        'IM':   'Inter-Medium.ttf',
        'ISB':  'Inter-SemiBold.ttf',
    }
    r = {}
    for k, f in fonts.items():
        p = os.path.join(FONT_DIR, f)
        if os.path.exists(p):
            try: pdfmetrics.registerFont(TTFont(k, p)); r[k] = True
            except: pass
    return r

_r = reg()
TF  = 'CGB'  if 'CGB'  in _r else 'Times-Bold'
CR  = 'CGR'  if 'CGR'  in _r else 'Times-Roman'
CI  = 'CGI'  if 'CGI'  in _r else 'Times-Roman'
CSB = 'CGSB' if 'CGSB' in _r else 'Times-Bold'
IR  = 'IR'   if 'IR'   in _r else 'Helvetica'
IM  = 'IM'   if 'IM'   in _r else 'Helvetica'
ISB = 'ISB'  if 'ISB'  in _r else 'Helvetica-Bold'

def wrap(c, txt, font, size, mw):
    words = txt.split()
    lines = []; cur = []
    for w in words:
        if c.stringWidth(' '.join(cur + [w]), font, size) <= mw:
            cur.append(w)
        else:
            if cur: lines.append(' '.join(cur))
            cur = [w]
    if cur: lines.append(' '.join(cur))
    return lines

def draw_text(c, x, y, txt, font, size, col, mw, lead):
    for ln in wrap(c, txt, font, size, mw):
        c.setFont(font, size); c.setFillColor(col)
        c.drawString(x, y, ln); y -= lead
    return y

def text_h(c, txt, font, size, mw, lead):
    return len(wrap(c, txt, font, size, mw)) * lead

BAND_B = 28*mm

def draw_band(c):
    c.setFillColor(PLUM)
    c.rect(0, 0, W, BAND_B, fill=1, stroke=0)
    ew = c.stringWidth("EXEC'", TF, 20)
    lx = W/2 - (ew + c.stringWidth("IA", TF, 20)) / 2
    c.setFont(TF, 20); c.setFillColor(HexColor('#FAF6F2'))
    c.drawString(lx, 18.5*mm, "EXEC'")
    c.setFillColor(TERRACOTTA)
    c.drawString(lx + ew, 18.5*mm, "IA")
    c.setFont(IR, 8); c.setFillColor(HexColor('#C8B8B2'))
    c.drawCentredString(W/2, 10*mm, "contact@exec-ia.ai  ·  exec-ia.ai")
    c.linkURL('https://exec-ia.ai', (0, 7*mm, W, 13*mm))
    c.setFont(IR, 7); c.setFillColor(HexColor('#9A8E8A'))
    c.drawCentredString(W/2, 4*mm, "© 2026 EXEC'IA Consulting  ·  Tous droits réservés")

def eyebrow(c, x, y, txt, size=12):
    c.setFont(IR, size); c.setFillColor(TERRACOTTA)
    c._charSpace = 1.8
    c.drawString(x, y, txt.upper())
    c._charSpace = 0
    return size + 3

def thin_line(c, x, y, w):
    c.setStrokeColor(ROSE_MIN); c.setLineWidth(0.5)
    c.line(x, y, x + w, y)
    c.setLineWidth(1)

def left_bar(c, x, y_top, h, col=None):
    col = col or TERRACOTTA
    c.setStrokeColor(col); c.setLineWidth(0.6)
    c.line(x, y_top, x, y_top - h)
    c.setLineWidth(1)

# ── DATA ──────────────────────────────────────────────────────────────
P = [
  dict(
    num=1,
    pre="La décision d'investir",
    title_lines=["Vous savez que certains projets ne valent rien.", "Vous les financez encore."],
    constat=[
      "Vos budgets IA n'ont pas été arbitrés. Ils ont été absorbés. Sans critère d'arrêt, sans droit de veto, sans responsable du résultat. Les projets continuent parce qu'arrêter obligerait à reconnaître qu'on s'est trompé — et dans une organisation, personne n'a officiellement ce mandat.",
      "Ce n'est pas un problème de gestion. C'est un problème de décision non prise. Et sans arbitrage clair, les mauvais projets survivent toujours aux bons.",
    ],
    questions=[
      "Qui, dans votre organisation, a formellement le mandat d'arrêter un projet IA — et ce mandat a-t-il déjà été exercé ?",
      "Quels processus créent le plus de valeur dans votre modèle — et lesquels n'ont encore été touchés par rien ?",
      "Quel projet seriez-vous incapable de défendre devant votre conseil dans 30 jours — et que faites-vous de cette réponse ?",
    ],
    conviction="Un portefeuille sans critère d'arrêt n'est pas une ambition. C'est une accumulation. Et dans votre organisation, personne ne paie le prix de la mauvaise décision aussi longtemps que le dirigeant qui ne l'a pas prise.",
  ),
  dict(
    num=2,
    pre="La décision de prioriser",
    title_lines=["Vos meilleurs cadres font ce que l'IA pourrait faire.", "Et vous le savez."],
    constat=[
      "Vos cadres passent entre 30 et 40 % de leur temps sur des tâches sans valeur de décision : reporting, consolidation de données, réunions sans suite, emails sans enjeu. Ce temps existe dans vos charges. Il n'existe pas dans votre stratégie.",
      "Libérer ce temps ne crée pas de valeur. Décider formellement où le redéployer — avant de toucher aux outils — c'est ce qui crée de la valeur. Dans cet ordre seulement. La productivité sans direction ne transforme pas une organisation. Elle l'accélère dans la mauvaise direction.",
    ],
    questions=[
      "Sur quelles décisions stratégiques vos meilleurs cadres devraient-ils passer 20 % de temps supplémentaire — et pourquoi ce n'est pas encore le cas ?",
      "Avez-vous formellement décidé où sera investi le temps libéré par l'IA — ou laissez-vous chaque manager répondre seul à cette question ?",
      "Si vous supprimiez demain les trois tâches les plus chronophages de vos équipes, qui en bénéficierait — et qui résisterait ?",
    ],
    conviction="Libérer du temps sans décider comment l'utiliser produit de l'anxiété, pas de la performance. Le gain de productivité n'est une décision managériale que si quelqu'un a décidé où va le gain.",
  ),
  dict(
    num=3,
    pre="La décision de transmettre",
    title_lines=["Un expert va partir.", "Vous n'avez pas décidé quoi faire avant."],
    constat=[
      "Votre avantage concurrentiel repose sur deux ou trois personnes. Quand elles partent, elles n'emportent pas seulement leur savoir. Elles emportent le raisonnement qui a produit vos décisions les plus importantes — les arbitrages, les compromis, les angles morts que personne d'autre ne connaît.",
      "Ce raisonnement ne figure dans aucun processus. Il ne se reconstruit pas avec un outil. Et aucune IA ne peut exploiter ce qui n'a jamais été capturé.",
    ],
    questions=[
      "Quelle décision critique de votre organisation repose aujourd'hui sur la mémoire d'une seule personne — et quel est votre plan concret si elle part dans 90 jours ?",
      "Si cette personne partait dans 30 jours, quelle décision ne pourrait plus être prise — et combien de temps durerait ce vide ?",
      "Avez-vous formellement désigné un responsable de la transmission du savoir stratégique — avec un budget, un périmètre, et une date ?",
    ],
    conviction="Investir dans un outil de gestion des connaissances sans avoir d'abord défini ce qui mérite d'être conservé, c'est automatiser le désordre. La gouvernance du savoir précède toujours la technologie qui est censée le transmettre.",
  ),
  dict(
    num=4,
    pre="La décision de fidéliser",
    title_lines=["Votre client a décidé de partir", "avant votre prochain CODIR."],
    constat=[
      "Un client ne part pas soudainement. Il décide de partir — plusieurs semaines avant que la rupture soit visible. Cette décision se prend dans trois moments précis de votre parcours. Ces moments ne sont presque jamais identifiés. Ils ne sont jamais assignés à un responsable.",
      "Vos concurrents qui déploient l'IA sur la relation client ne gagnent pas en vitesse. Ils gagnent en mémoire : chaque interaction leur apprend quelque chose sur vos clients que vous n'avez pas encore formalisé. L'écart n'est pas technologique. Il est décisionnel.",
    ],
    questions=[
      "Avez-vous identifié les trois moments où un client décide silencieusement de rester ou de partir — et qui dans votre organisation en est formellement responsable ?",
      "Combien de vos processus client ont été conçus pour protéger votre organisation — et combien pour créer une raison de rester ?",
      "Si votre principal concurrent déployait une IA sur votre meilleur segment client demain, combien de temps vous faudrait-il pour le détecter — et quelle décision auriez-vous déjà perdu ?",
    ],
    conviction="L'IA n'améliore pas une relation client défaillante — elle l'accélère. Sur un parcours moyen, elle produit de l'insatisfaction plus vite et à plus grande échelle. L'audit du parcours précède toujours le déploiement de l'outil.",
  ),
  dict(
    num=5,
    pre="La décision de gouverner",
    title_lines=["Vos outils IA ont plus de pouvoir", "sur vos processus que vous."],
    constat=[
      "En dix-huit mois, la plupart des organisations ont construit une dépendance à deux ou trois fournisseurs IA — sans jamais avoir formellement décidé jusqu'où elles leur faisaient confiance. Les tarifs augmentent. Les conditions changent. Le Règlement IA européen est en vigueur.",
      "Ce n'est pas un sujet de votre DSI. C'est votre responsabilité personnelle de dirigeant — sur les systèmes qui prennent ou préparent des décisions dans votre organisation.",
    ],
    questions=[
      "Avez-vous formellement décidé quelles décisions de votre organisation ne peuvent pas être déléguées à un système automatisé — et cette liste est-elle connue de votre CODIR ?",
      "Si votre principal fournisseur IA augmentait ses tarifs de 40 % demain, quels processus métier seraient bloqués — et qui a le mandat de décider de la suite ?",
      "Qui, dans votre organisation, est responsable de la conformité au Règlement IA européen — depuis quand — et avec quels moyens ?",
    ],
    conviction="La gouvernance IA n'est pas une contrainte réglementaire à gérer après coup. C'est la condition pour que votre stratégie reste la vôtre. Et c'est votre signature — pas celle de votre DSI.",
  ),
]

# ════════════════════════════════════════════════════════════════════
c = pdfcanvas.Canvas(OUT, pagesize=A4)

# ── PAGE 1 : COVER ───────────────────────────────────────────────────
c.setFillColor(IVORY)
c.rect(0, 0, W, H, fill=1, stroke=0)

TITLE_SIZE = 34
title_lines = ["L'IA N'A PAS PRIS LE POUVOIR.", "ELLE A OCCUPÉ LE VIDE."]
title_lead  = TITLE_SIZE * 1.25

ty = H - 72*mm
for ln in title_lines:
    c.setFont(TF, TITLE_SIZE); c.setFillColor(PLUM_DARK)
    c.drawCentredString(W/2, ty, ln)
    ty -= title_lead

ty -= 10*mm

# Sous-titre simplifié
c.setFont(CI, 16); c.setFillColor(PLUM)
c.drawCentredString(W/2, ty, "5 priorités  ·  1 minute par priorité")
ty -= 22*mm

# ── NAVIGATION : 5 boutons ───────────────────────────────────────────
BTN_H   = 13*mm
BTN_R   = BTN_H / 2
BTN_GAP = 4.5*mm
NUM_SZ  = 14
TXT_SZ  = 11
SEP_OFF = 7*mm

nav_items = [
    ("01", "Savoir où l'IA vous rapporte de l'argent",       "p1"),
    ("02", "Récupérer 20 % du temps de vos cadres",          "p2"),
    ("03", "La connaissance qui quitte votre entreprise",     "p3"),
    ("04", "Un client qui attend, c'est un concurrent qui avance", "p4"),
    ("05", "Vous avez probablement déjà perdu le contrôle",  "p5"),
]

for i, (num, label, bm) in enumerate(nav_items):
    nw     = c.stringWidth(num, TF, NUM_SZ)
    tw     = c.stringWidth(label, IM, TXT_SZ)
    BTN_W  = SEP_OFF + nw + SEP_OFF + tw + SEP_OFF
    BTN_W  = max(BTN_W, 70*mm)
    bx     = (W - BTN_W) / 2
    by_top = ty - i * (BTN_H + BTN_GAP)
    by_bot = by_top - BTN_H
    mid_y  = by_bot + BTN_H / 2 - 4

    c.setFillColor(WHITE)
    c.roundRect(bx, by_bot, BTN_W, BTN_H, BTN_R, fill=1, stroke=0)
    c.setStrokeColor(PLUM); c.setLineWidth(0.7)
    c.roundRect(bx, by_bot, BTN_W, BTN_H, BTN_R, fill=0, stroke=1)
    c.setLineWidth(1)

    # Numéro en terracotta
    c.setFont(TF, NUM_SZ); c.setFillColor(TERRACOTTA)
    c.drawString(bx + SEP_OFF, mid_y, num)

    sep_x = bx + SEP_OFF + nw + SEP_OFF / 2
    c.setStrokeColor(ROSE_MIN); c.setLineWidth(0.4)
    c.line(sep_x, by_bot + 3*mm, sep_x, by_top - 3*mm)
    c.setLineWidth(1)

    c.setFont(IM, TXT_SZ); c.setFillColor(PLUM_DARK)
    c.drawString(sep_x + SEP_OFF / 2, mid_y, label)

    c.linkAbsolute('', bm, Rect=(bx, by_bot, bx + BTN_W, by_top))

draw_band(c)
c.showPage()

# ── PAGES 01–05 ──────────────────────────────────────────────────────
BODY_SZ = 11
BODY_LD = 16
Q_SZ    = 11
Q_LD    = 16
IPAD    = 8*mm
NW      = 6*mm

def draw_priority(c, p):
    y = H - 14*mm

    # Pré-titre
    eyebrow(c, M, y, p['pre'], size=12)
    y -= 9*mm

    # Numéro section
    c.setFont(TF, 34); c.setFillColor(PLUM)
    c.drawString(M, y, f"0{p['num']}")
    y -= 13*mm

    # Ligne fine sous numéro
    thin_line(c, M, y + 2*mm, CW)
    y -= 5*mm

    # Titre
    for ln in p['title_lines']:
        c.setFont(CSB, 19); c.setFillColor(PLUM_DARK)
        c.drawString(M, y, ln)
        y -= 22

    y -= 6*mm

    # CONSTAT
    eyebrow(c, M, y, "Constat", size=9)
    y -= 5*mm
    for para in p['constat']:
        y = draw_text(c, M, y, para, CR, BODY_SZ, TEXT, CW, BODY_LD)
        y -= 4*mm
    y -= 2*mm

    # BOX QUESTIONS
    QW   = CW - IPAD - NW - IPAD
    rows = []
    for q in p['questions']:
        qlines = wrap(c, q, CI, Q_SZ, QW)
        rows.append(qlines)
    rows_h = sum(len(r) * Q_LD for r in rows) + (len(rows) - 1) * 4*mm
    q_h = IPAD + 6*mm + 3*mm + rows_h + IPAD

    c.setFillColor(WHITE)
    c.rect(M, y - q_h, CW, q_h, fill=1, stroke=0)
    left_bar(c, M, y, q_h, TERRACOTTA)

    iy = y - IPAD
    eyebrow(c, M + IPAD, iy, "3 questions pour le dirigeant", size=9)
    iy -= 9*mm

    for i, (q, qlines) in enumerate(zip(p['questions'], rows)):
        c.setFont(IR, 9); c.setFillColor(PLUM)
        c.drawString(M + IPAD, iy, str(i + 1))
        qy = iy
        for ln in qlines:
            c.setFont(CI, Q_SZ); c.setFillColor(TEXT)
            c.drawString(M + IPAD + NW, qy, ln)
            qy -= Q_LD
        iy = qy
        if i < len(p['questions']) - 1:
            iy -= 4*mm

    y -= (q_h + 4*mm)

    # BOX CONVICTION
    VW  = CW - IPAD - IPAD
    v_h = IPAD + 6*mm + 3*mm + text_h(c, p['conviction'], CI, Q_SZ, VW, Q_LD) + IPAD

    c.setFillColor(IVORY_TINT)
    c.rect(M, y - v_h, CW, v_h, fill=1, stroke=0)
    left_bar(c, M, y, v_h, PLUM)

    vy = y - IPAD
    eyebrow(c, M + IPAD, vy, "La conviction Exec'ia", size=9)
    vy -= 9*mm
    draw_text(c, M + IPAD, vy, p['conviction'], CI, Q_SZ, PLUM_DARK, VW, Q_LD)

    # Numéro de page
    c.setFont(IR, 7); c.setFillColor(GREY)
    c.drawRightString(W - M, BAND_B + 6*mm, str(p['num'] + 1))

for p in P:
    c.bookmarkPage(f'p{p["num"]}', fit='FitH', top=H)
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_priority(c, p)
    draw_band(c)
    c.showPage()

# ── PAGE 7 : APPROCHE + CTA ──────────────────────────────────────────
c.setFillColor(IVORY)
c.rect(0, 0, W, H, fill=1, stroke=0)

cy = H - 40*mm

# L'APPROCHE EXEC'IA
c.setFont(IR, 13); c.setFillColor(TERRACOTTA)
c._charSpace = 1.8
c.drawString(M, cy, "L'APPROCHE EXEC'IA")
c._charSpace = 0
cy -= 8*mm

thin_line(c, M, cy + 2*mm, CW)
cy -= 9*mm

approach_paras = [
    "Ce document ne parle pas d'intelligence artificielle.",
    "Il parle de gouvernance.",
    "Il parle de la capacité d'un dirigeant à rester l'auteur des décisions qui engagent son organisation.",
    "Il parle de ce qui se passe quand personne, dans une direction générale, n'a formellement décidé où s'arrête la machine et où recommence le jugement humain.",
]
for para in approach_paras:
    cy = draw_text(c, M, cy, para, CR, 11.5, TEXT, CW, 17)
    cy -= 4*mm

cy -= 2*mm

approach_paras2 = [
    "L'IA ne prend pas le pouvoir.",
    "Elle occupe les espaces que la direction n'a pas encore revendiqués.",
]
for para in approach_paras2:
    cy = draw_text(c, M, cy, para, CI, 13, PLUM_DARK, CW, 19)
    cy -= 3*mm

cy -= 2*mm

approach_paras3 = [
    "Ce que nous faisons chez EXEC'IA n'est pas de déployer des outils.",
    "C'est d'aider les dirigeants à reprendre la main sur les cinq décisions de ce document — dans le bon ordre, avec la bonne méthode, avant que le coût de l'attente dépasse le coût de l'action.",
    "Parce qu'une organisation dont la trajectoire est pilotée par ses fournisseurs, ses outils et ses experts isolés n'est plus tout à fait dirigée.",
]
for para in approach_paras3:
    cy = draw_text(c, M, cy, para, CR, 11.5, TEXT, CW, 17)
    cy -= 4*mm

# Phrase finale
c.setFont(CSB, 14); c.setFillColor(PLUM_DARK)
c.drawString(M, cy, "Elle est administrée.")
cy -= 18*mm

# ── BLOC CTA dans un encadré ─────────────────────────────────────────
btn_txt  = "Réserver mon entretien →"
btn_w    = c.stringWidth(btn_txt, ISB, 11) + 18*mm
btn_h    = 12*mm

box_pad  = 10*mm
box_h    = box_pad + 8*mm + 5*mm + 7*mm + 4*mm + btn_h + box_pad

# Encadré
c.setFillColor(WHITE)
c.rect(M, cy - box_h, CW, box_h, fill=1, stroke=0)
c.setStrokeColor(TERRACOTTA); c.setLineWidth(0.8)
c.rect(M, cy - box_h, CW, box_h, fill=0, stroke=1)
c.setLineWidth(1)
left_bar(c, M, cy, box_h, TERRACOTTA)

iy = cy - box_pad

# "30 MINUTES · CONFIDENTIEL · SANS ENGAGEMENT"
c.setFont(IR, 9); c.setFillColor(TERRACOTTA)
c._charSpace = 1.5
c.drawString(M + box_pad, iy, "30 MINUTES  ·  CONFIDENTIEL  ·  SANS ENGAGEMENT")
c._charSpace = 0
iy -= 8*mm

# Titre de l'entretien
c.setFont(TF, 20); c.setFillColor(PLUM_DARK)
c.drawString(M + box_pad, iy, "Entretien préliminaire — offert")
iy -= 9*mm

# Description courte
c.setFont(CR, 10.5); c.setFillColor(PLUM)
c.drawString(M + box_pad, iy, "Identifier vos décisions prioritaires. Repartir avec une première orientation.")
iy -= (4*mm + btn_h)

# Bouton terracotta
c.setFillColor(TERRACOTTA)
c.roundRect(M + box_pad, iy, btn_w, btn_h, btn_h / 2, fill=1, stroke=0)
c.setFont(ISB, 11); c.setFillColor(HexColor('#FAF6F2'))
c.drawString(M + box_pad + 9*mm, iy + 3.8*mm, btn_txt)
c.linkURL('mailto:contact@exec-ia.ai', (M + box_pad, iy, M + box_pad + btn_w, iy + btn_h))

# Étoiles — juste avant la bande
c.setFont(CR, 12); c.setFillColor(GREY)
c.drawCentredString(W/2, BAND_B + 12*mm, "*     *     *")

# Numéro de page
c.setFont(IR, 7); c.setFillColor(GREY)
c.drawRightString(W - M, BAND_B + 6*mm, "7")

draw_band(c)
c.showPage()
c.save()
print(f"✅ {OUT}")
