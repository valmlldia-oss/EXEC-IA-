#!/usr/bin/env python3
"""EXEC'IA — Les 5 Priorités IA des Dirigeants · 4 pages"""

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
BORDER_BTN = HexColor('#7A5060')

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
    words = txt.split(); lines = []; cur = []
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

# ── BANDEAU BAS — identique sur toutes les pages ─────────────────────
BAND_B = 32*mm

def draw_band(c):
    c.setFillColor(PLUM); c.rect(0, 0, W, BAND_B, fill=1, stroke=0)
    # EXEC'IA — taille augmentée, bien centré verticalement dans le bandeau
    ew2   = c.stringWidth("EXEC'", TF, 26)
    lbl_x = W/2 - (ew2 + c.stringWidth("IA", TF, 26)) / 2
    c.setFont(TF, 26); c.setFillColor(HexColor('#FAF6F2'))
    c.drawString(lbl_x, 20*mm, "EXEC'")
    c.setFillColor(TERRACOTTA); c.drawString(lbl_x + ew2, 20*mm, "IA")
    # CONSULTING avec letter-spacing
    c.setFont(IR, 7); c.setFillColor(HexColor('#D9C9C3'))
    c._charSpace = 3
    c.drawCentredString(W/2, 13*mm, "CONSULTING")
    c._charSpace = 0
    # Copyright
    c.setFont(IR, 6.5); c.setFillColor(HexColor('#B8B1AA'))
    c.drawCentredString(W/2, 5.5*mm,
        "valerie@exec-ia.ai  ·  © 2026 Valérie Mailland  ·  EXEC'IA  ·  Tous droits réservés")

def header_logo(c):
    hx = M; hy = H - 11*mm
    ew = c.stringWidth("EXEC'", TF, 10)
    c.setFont(TF, 10); c.setFillColor(PLUM)
    c.drawString(hx, hy, "EXEC'")
    c.setFillColor(TERRACOTTA); c.drawString(hx + ew, hy, "IA")

BORDER_CARD = HexColor('#7A5060')   # prune bordeaux rosé

def card(c, x, y_top, w, h, bg):
    """Carte style pillar site : fond clair, border-left verticale prune bordeaux rosé."""
    R = 4*mm
    c.setFillColor(bg)
    c.roundRect(x, y_top - h, w, h, R, fill=1, stroke=0)
    c.setStrokeColor(BORDER_CARD); c.setLineWidth(2)
    c.line(x, y_top - R, x, y_top - h + R)
    c.setLineWidth(1)

EYE_COL = HexColor('#C8616480')  # terracotta opacity .85 simulé → légèrement atténué

def eyebrow_label(c, x, y, txt):
    """Strictement identique à .eyebrow du site : IR Regular 10pt, charSpace .2em, #C75F62 op.85"""
    c.setFont(IR, 10); c.setFillColor(TERRACOTTA)
    c._charSpace = 2.0   # 0.2em × 10pt
    c.drawString(x, y, txt.upper())
    c._charSpace = 0

def draw_p(c, x, y_top, p, mw=None):
    if mw is None: mw = CW

    # ── Tailles généreuses pour remplir la page ───────────────────────
    NBODY = 12.5   # corps constat
    NL    = 18.5   # interligne constat
    QBODY = 12.5   # corps questions
    QL    = 18.5   # interligne questions
    VL    = 18.0   # interligne vigilance
    IPAD  = 11*mm  # padding box (site : 36px)
    NW    = 8*mm   # col numéro

    y = y_top

    # Numéro grand
    c.setFont(TF, 44); c.setFillColor(TERRACOTTA)
    c.drawString(x, y, f"0{p['num']}")
    y -= 15*mm

    # Titre
    c.setFont(CSB, 20); c.setFillColor(PLUM_DARK)
    for ln in wrap(c, p['title'], CSB, 20, mw):
        c.drawString(x, y, ln); y -= 27
    y -= 12*mm

    # CONSTAT
    eyebrow_label(c, x, y, "Constat"); y -= 7*mm
    y = draw_text(c, x, y, p['constat'], CR, NBODY, TEXT, mw, NL); y -= 9*mm

    # ── BOX QUESTIONS ─────────────────────────────────────────────────
    QW     = mw - 2*IPAD - NW
    lbl_h  = 8*mm
    rows_h = sum(len(wrap(c, q, CI, QBODY, QW)) * QL + 4*mm
                 for q in p['questions']) - 4*mm
    q_h    = IPAD + lbl_h + 5*mm + rows_h + IPAD

    card(c, x, y, mw, q_h, WHITE)

    iy = y - IPAD
    eyebrow_label(c, x + IPAD, iy, "3 questions pour le dirigeant"); iy -= lbl_h + 5*mm

    for i, q in enumerate(p['questions'], 1):
        c.setFont(CR, 13); c.setFillColor(GREY)
        c.drawString(x + IPAD, iy, str(i))
        iy = draw_text(c, x + IPAD + NW, iy, q, CI, QBODY, TEXT, QW, QL)
        if i < len(p['questions']): iy -= 4*mm

    y -= (q_h + 5*mm)

    # ── BOX VIGILANCE ─────────────────────────────────────────────────
    VW    = mw - 2*IPAD
    v_lbl = 8*mm
    v_h   = IPAD + v_lbl + text_h(c, p['vigilance'], CI, QBODY, VW, VL) + IPAD

    card(c, x, y, mw, v_h, IVORY_TINT)

    vy = y - IPAD
    eyebrow_label(c, x + IPAD, vy, "Point de vigilance"); vy -= v_lbl
    draw_text(c, x + IPAD, vy, p['vigilance'], CI, QBODY, PLUM, VW, VL)

# ── DATA ─────────────────────────────────────────────────────────────
P = [
  dict(num=1,
    title="Savoir où l'IA vous rapporte de l'argent — avant d'en dépenser davantage",
    constat="La plupart des budgets IA 2024-2025 ont été alloués sans critère de retour sur investissement : des pilotes qui ne passent jamais en production, des équipes mobilisées sur des projets que personne ne sait évaluer. La question que peu de dirigeants peuvent encore éviter : où l'IA vous rapporte-t-elle concrètement de l'argent ?",
    questions=[
      "Sur vos trois derniers projets IA, quel gain réel pouvez-vous chiffrer — et qui peut le prouver ?",
      "Quels processus génèrent le plus de valeur dans votre modèle — et lesquels sont encore entièrement manuels ?",
      "Quel projet IA arrêteriez-vous demain si vous deviez justifier chaque euro investi devant votre conseil ?",
    ],
    vigilance="Un portefeuille de pilotes sans critère de rentabilité n'est pas une stratégie. C'est un budget R&D déguisé — sans les résultats. Et sans arbitrage, les mauvais projets survivent aux bons."),

  dict(num=2,
    title="Récupérer 20 % du temps de vos cadres — et décider quoi en faire",
    constat="Vos cadres passent 30 à 40 % de leur temps sur des tâches que l'IA peut traiter en secondes : synthèses, reporting, réponses standard, recherche documentaire. Ce temps existe dans vos charges. Il n'est pas récupéré. Chaque semaine sans décision sur ce sujet est une semaine de surcoût que vos concurrents n'ont peut-être plus.",
    questions=[
      "Quelles tâches à haute valeur de temps occupent vos meilleurs éléments chaque semaine — sans créer de valeur directe ?",
      "Si vos équipes gagnaient 20 % de capacité, sur quelles priorités stratégiques les redéployiez-vous en premier ?",
      "Avez-vous mesuré l'écart entre ce que vos cadres font et ce qu'ils devraient faire ?",
    ],
    vigilance="Libérer du temps sans décider comment l'utiliser génère de l'anxiété, pas de la performance. Le gain de productivité ne crée de valeur que s'il est fléché — c'est une décision managériale, pas une conséquence automatique."),

  dict(num=3,
    title="La connaissance qui quitte votre entreprise chaque vendredi soir",
    constat="Votre avantage concurrentiel repose sur des experts. Quand ils partent, ils emportent ce que votre organisation a mis des années à apprendre. Ce savoir n'est pas documenté. Il n'est pas transmissible. Il ne vaut rien sur un bilan — et pourtant c'est souvent lui qui justifie vos marges.",
    questions=[
      "Qu'est-ce que votre entreprise perdrait concrètement si votre meilleur expert partait dans 30 jours ?",
      "Quelle décision critique repose aujourd'hui sur la mémoire d'une seule personne ?",
      "En combien de temps un collaborateur récent peut-il accéder aux bonnes pratiques de votre organisation ?",
    ],
    vigilance="Un assistant IA interne n'est utile que si la connaissance qu'il exploite est structurée et à jour. Investir dans la technologie avant la gouvernance documentaire, c'est automatiser le désordre."),

  dict(num=4,
    title="Un client qui attend une réponse, c'est un concurrent qui avance",
    constat="En 2026, vos concurrents répondent en temps réel, personnalisent à l'échelle et détectent les signaux de désengagement avant vous. Ces capacités ne coûtent plus des millions. La question n'est plus 'si' — c'est 'combien de clients avez-vous perdus pendant que vous réfléchissiez'.",
    questions=[
      "Quel est votre taux de résolution client au premier contact — et quel est le coût financier de chaque échec ?",
      "Combien de temps faut-il à un conseiller pour avoir une vue complète d'un client avant chaque interaction ?",
      "Avez-vous identifié les trois moments où un client décide silencieusement de partir ?",
    ],
    vigilance="L'IA n'améliore pas une relation client défaillante — elle l'accélère. Sur un parcours moyen, elle produit de l'insatisfaction plus vite et à plus grande échelle. L'audit précède toujours le déploiement."),

  dict(num=5,
    title="Vous avez probablement déjà perdu le contrôle de vos coûts IA",
    constat="En 18 mois, la plupart des organisations ont construit une dépendance à deux ou trois fournisseurs IA sans contrat cadre, sans plan de continuité et sans cartographie des risques. Les tarifs augmentent. Les conditions changent. Le Règlement IA européen est en vigueur. Ce n'est plus un sujet technique — c'est votre responsabilité personnelle de dirigeant.",
    questions=[
      "Si votre principal fournisseur IA augmentait ses tarifs de 40 % demain, quels processus métier seraient bloqués ?",
      "Avez-vous une cartographie des décisions où l'IA intervient — avec leur niveau de risque réglementaire ?",
      "Qui, dans votre organisation, est responsable de la conformité au Règlement IA européen — et depuis quand ?",
    ],
    vigilance="La gouvernance IA n'est pas une contrainte réglementaire à gérer après coup. C'est la condition pour que votre stratégie reste souveraine. Et c'est votre signature, pas celle de votre DSI."),
]

# ════════════════════════════════════════════════════════════════════
c = pdfcanvas.Canvas(OUT, pagesize=A4)

# ── COVER ────────────────────────────────────────────────────────────
c.setFillColor(IVORY); c.rect(0, 0, W, H, fill=1, stroke=0)

c.setFont(TF, 118); c.setFillColor(PLUM)
c.drawCentredString(W/2, H - 58*mm, "5")

c.setFont(TF, 42); c.setFillColor(TERRACOTTA)
c.drawCentredString(W/2, H - 91*mm, "PRIORITÉS IA")

c.setFont(CI, 21); c.setFillColor(PLUM)
c.drawCentredString(W/2, H - 104*mm, "des Dirigeants")

c.setFont(ISB, 9.5); c.setFillColor(TERRACOTTA)
c.drawCentredString(W/2, H - 114*mm, "1 MINUTE PAR PRIORITÉ")

# ── BOUTONS pill maigres, bloc centré ────────────────────────────────
BTN_H  = 10*mm
BTN_R  = BTN_H / 2
H_PAD  = 6*mm
SEP_W  = 4*mm
N_BTN  = 5
BTN_GAP = 5*mm

BLOC_H   = N_BTN * BTN_H + (N_BTN - 1) * BTN_GAP
ZONE_MID = (BAND_B + (H - 114*mm)) / 2
ZONE_TOP = ZONE_MID + BLOC_H / 2

btn_titles = [
    ("01", "Savoir où l'IA vous rapporte de l'argent",              "p1"),
    ("02", "Récupérer 20 % du temps de vos cadres",                 "p2"),
    ("03", "La connaissance qui quitte votre entreprise",           "p3"),
    ("04", "Un client qui attend, c'est un concurrent qui avance",  "p4"),
    ("05", "Contrôler vos coûts IA avant qu'ils vous contrôlent",   "p5"),
]

for i, (num, title, bm) in enumerate(btn_titles):
    by_top = ZONE_TOP - i * (BTN_H + BTN_GAP)
    by_bot = by_top - BTN_H
    nw     = c.stringWidth(num,   TF,  18)
    tw     = c.stringWidth(title, IR,  9.5)
    BTN_W  = min(H_PAD + nw + SEP_W + tw + H_PAD, CW)
    bx     = (W - BTN_W) / 2
    pcy    = by_bot + BTN_H / 2

    c.setFillColor(IVORY_CARD)
    c.roundRect(bx, by_bot, BTN_W, BTN_H, BTN_R, fill=1, stroke=0)
    c.setStrokeColor(BORDER_BTN); c.setLineWidth(0.5)
    c.roundRect(bx, by_bot, BTN_W, BTN_H, BTN_R, fill=0, stroke=1)
    c.setLineWidth(1)

    c.setFont(TF, 18); c.setFillColor(TERRACOTTA)
    c.drawString(bx + H_PAD, pcy - 6, num)

    sep_x = bx + H_PAD + nw + SEP_W / 2
    c.setStrokeColor(ROSE_MIN); c.setLineWidth(0.4)
    c.line(sep_x, by_bot + 2*mm, sep_x, by_top - 2*mm)
    c.setLineWidth(1)

    c.setFont(IR, 9.5); c.setFillColor(PLUM_DARK)
    c.drawString(bx + H_PAD + nw + SEP_W, pcy - 3.5, title)

    c.linkAbsolute('', bm, Rect=(bx, by_bot, bx + BTN_W, by_top))

draw_band(c)
c.showPage()

# ── PAGES PRIORITÉS — 1 par page (cover + 5 + 1 CTA = 7 pages) ──────
P_TOP = H - 20*mm

for p in P:
    c.bookmarkPage(f'p{p["num"]}', fit='FitH', top=H)
    c.setFillColor(IVORY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFont(IR, 7.5); c.setFillColor(GREY)
    c.drawRightString(W - M, H - 11*mm, str(p['num']))
    draw_p(c, M, P_TOP, p)
    draw_band(c)
    c.showPage()

# ── PAGE CTA ─────────────────────────────────────────────────────────
c.setFillColor(IVORY); c.rect(0, 0, W, H, fill=1, stroke=0)
cy = H - 65*mm

c.setFont(CR, 18); c.setFillColor(PLUM_DARK)
c.drawCentredString(W/2, cy, "*     *     *"); cy -= 18*mm

# Pré-titre identique aux autres pages
eyebrow_label(c, M, cy, "L'APPROCHE EXEC'IA"); cy -= 13*mm

# Titre : une seule ligne, "décisions éclairées" en terracotta
c.setFont(CSB, 26); c.setFillColor(PLUM_DARK)
c.drawString(M, cy, "Des ")
xd = M + c.stringWidth("Des ", CSB, 26)
c.setFillColor(TERRACOTTA); c.drawString(xd, cy, "décisions éclairées.")
cy -= 20*mm

# Sous-titre offre
c.setFont(CSB, 15); c.setFillColor(PLUM_DARK)
c.drawString(M, cy, "Entretien préliminaire — offert"); cy -= 10*mm

# Description exacte du site
c.setFont(CR, 11); c.setFillColor(TEXT)
c.drawString(M, cy, "30 minutes pour comprendre votre situation et évaluer ensemble —"); cy -= 15
c.drawString(M, cy, "la façon dont je peux vous être utile."); cy -= 10*mm

# Réassurance exacte du site
c.setFont(IR, 9); c.setFillColor(GREY)
c.drawString(M, cy, "Sans engagement  ·  Confidentiel"); cy -= 13*mm

# Bouton terracotta
btn_txt = "Prendre rendez-vous"
btn_w   = c.stringWidth(btn_txt, IM, 11) + 18*mm
btn_h   = 11*mm
c.setFillColor(TERRACOTTA)
c.roundRect(M, cy - btn_h, btn_w, btn_h, btn_h/2, fill=1, stroke=0)
c.setFont(IM, 11); c.setFillColor(HexColor('#FAF6F2'))
c.drawString(M + 9*mm, cy - btn_h + 3.8*mm, btn_txt)

draw_band(c)
c.showPage()

c.save()
print(f"✅ {OUT}")
