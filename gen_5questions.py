#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXEC\'IA — 5 Questions · Lead Magnet Q4 2026 · FR / EN / ES"""

from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

W, H = A4

# ── Palette EXEC\'IA — valeurs exactes, aucune autre ──────────────────────────
PLUM       = HexColor('#633B4A')   # prune bordeaux rosé
PLUM_DARK  = HexColor('#3D2030')   # prune profond
PLUM_BOX   = HexColor('#5A3542')   # box sur fond prune (légèrement plus clair)
TERRA      = HexColor('#C75F62')   # terracotta — LE SEUL CODE AUTORISÉ
TERRA_PALE = HexColor('#F0E6E3')   # terracotta très pâle pour fond card
IVORY      = HexColor('#F6F1EB')   # fond ivoire
IVORY2     = HexColor('#FAF6F2')   # cards légères
TEXT       = HexColor('#2A1020')   # corps de texte
GREY       = HexColor('#847680')   # texte secondaire
GREY_PALE  = HexColor('#D9C9C3')   # texte sur fond sombre

M  = 18*mm
CW = W - 2*M

SITE_URL  = 'https://www.exec-ia.ai'
OFFER_URL = 'https://www.exec-ia.ai/#offres'
MAIL      = 'contact@exec-ia.ai'

BASE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, 'assets')
FONTS  = os.path.join(ASSETS, 'fonts_pdf')


def reg():
    fmap = {
        'CGB':  'CormorantGaramond-Bold.ttf',
        'CGR':  'CormorantGaramond-Regular.ttf',
        'CGI':  'CormorantGaramond-Italic.ttf',
        'CGSB': 'CormorantGaramond-SemiBold.ttf',
        'IR':   'Inter-Regular.ttf',
        'IM':   'Inter-Medium.ttf',
        'ISB':  'Inter-SemiBold.ttf',
    }
    r = {}
    for k, f in fmap.items():
        p = os.path.join(FONTS, f)
        if os.path.exists(p):
            try: pdfmetrics.registerFont(TTFont(k, p)); r[k] = True
            except: pass
    return r

_r = reg()
CGB  = 'CGB'  if 'CGB'  in _r else 'Times-Bold'
CGR  = 'CGR'  if 'CGR'  in _r else 'Times-Roman'
CGI  = 'CGI'  if 'CGI'  in _r else 'Times-Italic'
CGSB = 'CGSB' if 'CGSB' in _r else 'Times-Bold'
IR   = 'IR'   if 'IR'   in _r else 'Helvetica'
IM   = 'IM'   if 'IM'   in _r else 'Helvetica'
ISB  = 'ISB'  if 'ISB'  in _r else 'Helvetica-Bold'


def wrap(c, txt, font, size, maxw):
    words = txt.split()
    lines, cur = [], []
    for w in words:
        if c.stringWidth(' '.join(cur + [w]), font, size) <= maxw:
            cur.append(w)
        else:
            if cur: lines.append(' '.join(cur))
            cur = [w]
    if cur: lines.append(' '.join(cur))
    return lines or ['']

def draw_text(c, x, y, txt, font, size, col, maxw, lead=None):
    if lead is None: lead = size * 1.4
    c.setFont(font, size); c.setFillColor(col)
    for ln in wrap(c, txt, font, size, maxw):
        c.drawString(x, y, ln); y -= lead
    return y

def text_h(c, txt, font, size, maxw, lead=None):
    if lead is None: lead = size * 1.4
    return len(wrap(c, txt, font, size, maxw)) * lead


# ── Barre verticale fine terracotta — identique site web ─────────────────────
def thin_bar(c, x, y_top, height, color=TERRA):
    """Ligne verticale fine (2pt) — exactement comme le site."""
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.line(x, y_top - height, x, y_top)


# ── FOOTER — identique site web ───────────────────────────────────────────────
BAND_H = 46*mm   # footer identique site web — logo + tagline + langues + copyright
LANG_URLS = {
    'fr': SITE_URL,
    'en': 'https://www.exec-ia.ai/index-en.html',
    'es': 'https://www.exec-ia.ai/index-es.html',
}
LANG_LABELS = {'fr': 'Français', 'en': 'English', 'es': 'Español'}

LOGO_FOOTER = os.path.join(ASSETS, 'EXECIA_CONSULTING_zoomé.png')
if not os.path.exists(LOGO_FOOTER):
    LOGO_FOOTER = os.path.join(ASSETS, "EXEC\'IA CONSULTING new.png")

def footer(c, lang, pg=None):
    """Footer identique site web — fond PLUM #633B4A."""
    c.setFillColor(PLUM)
    c.rect(0, 0, W, BAND_H, fill=1, stroke=0)
    c.setStrokeColor(TERRA); c.setLineWidth(0.6)
    c.line(0, BAND_H, W, BAND_H)

    # ── Logo EXEC\'IA CONSULTING centré en haut du footer ─────────────────────
    logo_w = 44*mm; logo_h = 12*mm
    logo_x = (W - logo_w) / 2
    logo_y = BAND_H - logo_h - 3*mm
    if os.path.exists(LOGO_FOOTER):
        # Fond blanc pour le logo (comme sur le site)
        c.setFillColor(white)
        c.roundRect(logo_x - 2*mm, logo_y - 1.5*mm,
                    logo_w + 4*mm, logo_h + 3*mm, 1.5*mm, fill=1, stroke=0)
        c.drawImage(LOGO_FOOTER, logo_x, logo_y, width=logo_w, height=logo_h,
                    preserveAspectRatio=True, mask='auto')
    else:
        c.setFont(ISB, 9); c.setFillColor(white)
        c.drawCentredString(W / 2, logo_y + 3*mm, "EXEC\'IA CONSULTING")
    c.linkURL(SITE_URL, (logo_x - 2*mm, logo_y - 1.5*mm,
                          logo_x + logo_w + 2*mm, logo_y + logo_h + 1.5*mm), thickness=0)

    # ── Tagline — Cormorant Garamond Italic terracotta (identique site) ───────
    tagline_y = logo_y - 7*mm
    c.setFont(CGI, 11); c.setFillColor(TERRA)
    c.drawCentredString(W / 2, tagline_y,
                        'Une expérience dirigeante au service de votre transformation IA')

    # ── Mention IA — Inter Regular gris pâle ─────────────────────────────────
    mention_y = tagline_y - 6*mm
    c.setFont(IR, 7); c.setFillColor(GREY_PALE)
    c.drawCentredString(W / 2, mention_y,
                        'Conception, contenus et automatisations assistés par Intelligence Artificielle · Validation humaine systématique')

    # ── Boutons langue — pill outline centrés (style site) ───────────────────
    btn_y = mention_y - 7.5*mm
    langs_to_show = [(lc, LANG_LABELS[lc]) for lc in ['fr', 'en', 'es'] if lc != lang]
    # Calculer largeur totale
    btn_w_list = [c.stringWidth(lbl, IR, 8) + 8*mm for _, lbl in langs_to_show]
    total_w = sum(btn_w_list) + 3*mm * (len(langs_to_show) - 1)
    bx = (W - total_w) / 2
    BH_BTN = 6.5*mm
    for i, ((lc, lbl), bw) in enumerate(zip(langs_to_show, btn_w_list)):
        c.setStrokeColor(GREY_PALE); c.setLineWidth(0.6)
        c.setFillColor(PLUM)
        c.roundRect(bx, btn_y - BH_BTN, bw, BH_BTN, BH_BTN / 2, fill=1, stroke=1)
        c.setFont(IR, 8); c.setFillColor(GREY_PALE)
        c.drawCentredString(bx + bw / 2, btn_y - BH_BTN + 1.5*mm, lbl)
        c.linkURL(LANG_URLS[lc], (bx, btn_y - BH_BTN, bx + bw, btn_y), thickness=0)
        bx += bw + 3*mm

    # ── Copyright — centré en bas ─────────────────────────────────────────────
    copy_y = 4*mm
    copy = "© 2026 Valérie Mailland · EXEC'IA · " + MAIL + " · Tous droits réservés"
    c.setFont(IR, 6.5); c.setFillColor(GREY_PALE)
    c.drawCentredString(W / 2, copy_y, copy)
    c.linkURL('mailto:' + MAIL,
              (W / 2 - 20*mm, copy_y - 2*mm, W / 2 + 20*mm, copy_y + 5*mm), thickness=0)

    if pg:
        c.setFont(IR, 6); c.setFillColor(GREY_PALE)
        c.drawRightString(W - M, copy_y, f'{pg}/7')


# ── COVER ─────────────────────────────────────────────────────────────────────
def cover(c, lang, content):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    TOP = H - 12*mm
    BOT = BAND_H + 7*mm
    y   = TOP

    # Pill Q4 2026 — haut droite
    tag = 'Q4 2026'
    tw  = c.stringWidth(tag, ISB, 7) + 5*mm
    c.setFillColor(TERRA)
    c.roundRect(W - M - tw, y - 9*mm, tw, 7.5*mm, 2*mm, fill=1, stroke=0)
    c.setFont(ISB, 7); c.setFillColor(white)
    c.drawCentredString(W - M - tw / 2, y - 5.5*mm, tag)
    y -= 16*mm

    # Pré-titre — Inter SemiBold terracotta, style "LE VÉRITABLE ENJEU" du site
    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, y, content['cover_pretitle'])
    y -= 11*mm

    # Titre — Cormorant Garamond Bold + barre verticale fine terracotta gauche
    title_lines = wrap(c, content['cover_title'][0], CGB, 28, CW)
    title_lines += wrap(c, content['cover_title'][1], CGB, 28, CW)
    t_lead = 28 * 1.2
    title_h = len(title_lines) * t_lead
    thin_bar(c, M, y + 2*mm, title_h + 2*mm)
    c.setFont(CGB, 28); c.setFillColor(PLUM_DARK)
    for ln in title_lines:
        c.drawString(M + 5*mm, y, ln); y -= t_lead
    y -= 6*mm

    # Sous-titre — Cormorant Garamond Italic gris, comme site
    c.setFont(CGI, 12); c.setFillColor(GREY)
    c.drawString(M, y, content['cover_subtitle'])
    y -= 7*mm
    c.setFont(IR, 8); c.setFillColor(GREY)
    c.drawString(M, y, content['cover_caption'])
    y -= 13*mm

    # ── 5 BOUTONS PILLS ───────────────────────────────────────────────────────
    NUM_R  = 4*mm
    TXT_X  = M + NUM_R * 2 + 5*mm
    TXT_W  = W - M - TXT_X - 5*mm
    GAP    = 2.5*mm
    CTA_H  = 16*mm
    CTA_GAP = 6*mm
    L_LEAD  = 9.5 * 1.35
    PAD_V   = 3.5*mm

    def btn_h(txt):
        return len(wrap(c, txt, IM, 9.5, TXT_W)) * L_LEAD + PAD_V * 2

    btn_heights = [btn_h(q['btn']) for q in content['questions']]
    total = sum(btn_heights) + GAP * 4 + CTA_H + CTA_GAP
    if total > y - BOT:
        ratio = max(0.8, (y - BOT - CTA_H - CTA_GAP - GAP * 4) / sum(btn_heights))
        PAD_V = PAD_V * ratio
        btn_heights = [btn_h(q['btn']) for q in content['questions']]

    for i, (q, bh) in enumerate(zip(content['questions'], btn_heights)):
        r = bh / 2
        # Fond ivoire, bord prune foncé fin
        c.setFillColor(IVORY2)
        c.roundRect(M, y - bh, CW, bh, r, fill=1, stroke=0)
        c.setStrokeColor(PLUM_DARK); c.setLineWidth(0.7)
        c.roundRect(M, y - bh, CW, bh, r, fill=0, stroke=1)
        # Cercle terracotta + numéro
        cx = M + r; cy = y - bh / 2
        c.setFillColor(TERRA)
        c.circle(cx, cy, NUM_R, fill=1, stroke=0)
        c.setFont(ISB, 7); c.setFillColor(white)
        c.drawCentredString(cx, cy - 2.5*mm, f'0{i+1}')
        # Texte — Inter Medium prune
        lines = wrap(c, q['btn'], IM, 9.5, TXT_W)
        th_txt = len(lines) * L_LEAD
        ty = cy + th_txt / 2 - L_LEAD * 0.25
        c.setFont(IM, 9.5); c.setFillColor(PLUM)
        for ln in lines:
            c.drawString(TXT_X, ty, ln); ty -= L_LEAD
        c.linkURL(OFFER_URL, (M, y - bh, W - M, y), thickness=0)
        y -= bh + GAP

    y -= CTA_GAP

    # CTA terracotta
    c.setFillColor(TERRA)
    c.roundRect(M, y - CTA_H, CW, CTA_H, 5*mm, fill=1, stroke=0)
    c.setFont(ISB, 8.5); c.setFillColor(white)
    c.drawCentredString(W / 2, y - 6.5*mm, content['cover_cta_title'])
    c.setFont(IR, 7.5); c.setFillColor(IVORY)
    c.drawCentredString(W / 2, y - 12.5*mm, content['cover_cta_sub'])
    c.linkURL(OFFER_URL, (M, y - CTA_H, W - M, y), thickness=0)

    footer(c, lang)
    c.showPage()


# ── PAGE INTÉRIEURE ───────────────────────────────────────────────────────────
def inner(c, lang, qnum, q, pg):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    TOP = H - 12*mm
    BOT = BAND_H + 8*mm
    y   = TOP
    IW  = CW - 8*mm
    PAD = 4.5*mm
    GAP = 5*mm

    # Pré-titre Inter SemiBold terracotta — style "LE VÉRITABLE ENJEU"
    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, y, f'0{qnum}  ·  {q["cat"].upper()}')
    y -= 10*mm

    # Titre Cormorant Garamond Bold + barre fine terracotta
    title_lines = wrap(c, q['title'], CGB, 21, CW - 6*mm)
    t_lead = 21 * 1.25
    title_h = len(title_lines) * t_lead
    thin_bar(c, M, y + 2*mm, title_h + 2*mm)
    c.setFont(CGB, 21); c.setFillColor(PLUM_DARK)
    for ln in title_lines:
        c.drawString(M + 5*mm, y, ln); y -= t_lead
    y -= 5*mm

    # Séparateur fin ivoire/gris
    c.setStrokeColor(GREY_PALE); c.setLineWidth(0.5)
    c.line(M, y, W - M, y)
    y -= 8*mm

    # Calcul dynamique hauteurs
    LEAD9 = 9.5 * 1.4
    LEAD11 = 11 * 1.38

    idea_h_txt = sum(
        text_h(c, l, IR, 9.5, IW, LEAD9) if l else 3*mm
        for l in q['idea']
    ) + 7.5*mm
    box1_h = idea_h_txt + PAD * 2

    box2_h = text_h(c, q['codir'], CGSB, 11.5, IW, LEAD11) + 7.5*mm + PAD * 2

    conv_h_txt = sum(
        text_h(c, l, CGI, 12, IW, 12 * 1.3) + 1.5*mm for l in q['conviction']
    )
    box3_h = conv_h_txt + 7.5*mm + PAD * 2

    offer_h = 9*mm
    total = box1_h + box2_h + box3_h + GAP * 2 + offer_h
    avail = y - BOT

    if total > avail:
        ratio = max(0.78, (avail - offer_h - GAP * 2) / (box1_h + box2_h + box3_h))
        PAD = PAD * ratio
        box1_h = idea_h_txt + PAD * 2
        box2_h = text_h(c, q['codir'], CGSB, 11.5, IW, LEAD11) + 7.5*mm + PAD * 2
        box3_h = conv_h_txt + 7.5*mm + PAD * 2

    # ── Box 1 : IDÉE CLÉ — fond ivoire 2, bord gauche fin prune ─────────────
    c.setFillColor(IVORY2)
    c.roundRect(M, y - box1_h, CW, box1_h, 3*mm, fill=1, stroke=0)
    thin_bar(c, M + 1*mm, y - 1*mm, box1_h - 2*mm, PLUM)
    c.setFont(ISB, 6.5); c.setFillColor(PLUM)
    c.drawString(M + 5*mm, y - PAD, q['idea_label'].upper())
    iy = y - PAD - 8*mm
    for line in q['idea']:
        if not line: iy -= 3*mm
        else: iy = draw_text(c, M + 5*mm, iy, line, IR, 9.5, TEXT, IW, LEAD9)
    y -= box1_h + GAP

    # ── Box 2 : QUESTION CODIR — fond terracotta pâle, bord fin terracotta ───
    c.setFillColor(TERRA_PALE)
    c.roundRect(M, y - box2_h, CW, box2_h, 3*mm, fill=1, stroke=0)
    thin_bar(c, M + 1*mm, y - 1*mm, box2_h - 2*mm, TERRA)
    c.setFont(ISB, 6.5); c.setFillColor(TERRA)
    c.drawString(M + 5*mm, y - PAD, q['codir_label'].upper())
    # Cormorant Garamond SemiBold pour la question
    draw_text(c, M + 5*mm, y - PAD - 8*mm, q['codir'], CGSB, 11.5, PLUM_DARK, IW, LEAD11)
    y -= box2_h + GAP

    # ── Box 3 : CONVICTION — fond PLUM, box intérieure légèrement plus claire ─
    c.setFillColor(PLUM)
    c.roundRect(M, y - box3_h, CW, box3_h, 3*mm, fill=1, stroke=0)
    # Box intérieure — couleur légèrement différente comme screenshot site
    inner_pad = 3*mm
    c.setFillColor(PLUM_BOX)
    c.roundRect(M + inner_pad, y - box3_h + inner_pad,
                CW - inner_pad * 2, box3_h - inner_pad * 2,
                2.5*mm, fill=1, stroke=0)
    c.setFont(ISB, 6.5); c.setFillColor(TERRA)
    c.drawString(M + 5*mm, y - PAD, q['conviction_label'].upper())
    cy = y - PAD - 8*mm
    for line in q['conviction']:
        cy = draw_text(c, M + 5*mm, cy, line, CGI, 12, white, IW, 12 * 1.3)
        cy -= 1.5*mm
    y -= box3_h + 4*mm

    # Lien offre
    off_y = max(y, BOT)
    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, off_y, q.get('offer_link', 'exec-ia.ai'))
    c.linkURL(OFFER_URL, (M, off_y - 2*mm, W - M, off_y + 7*mm), thickness=0)

    footer(c, lang, pg)
    c.showPage()


# ── PAGE FINALE ───────────────────────────────────────────────────────────────
def final(c, lang, content):
    # Fond prune profond — style section sombre du site
    c.setFillColor(PLUM_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    y = H - 13*mm

    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, y, content['final_pretitle'])
    y -= 13*mm

    # Titre Cormorant blanc + terracotta pour accroche
    for i, line in enumerate(content['final_title']):
        c.setFont(CGB, 24)
        c.setFillColor(TERRA if i == 1 else white)
        c.drawString(M, y, line); y -= 13*mm
    y -= 3*mm

    c.setStrokeColor(TERRA); c.setLineWidth(0.6)
    c.line(M, y, M + 18*mm, y)
    y -= 9*mm

    # Box intro — fond légèrement plus clair sur fond prune (style screenshot)
    lines = content['final_body']
    ih = sum(text_h(c, l, IR, 9.5, CW - 12*mm) for l in lines) + 11*mm
    c.setFillColor(PLUM_BOX)
    c.roundRect(M, y - ih, CW, ih, 3*mm, fill=1, stroke=0)
    iy = y - 4.5*mm
    for line in lines:
        iy = draw_text(c, M + 6*mm, iy, line, CGI, 11, white, CW - 12*mm, 11 * 1.35)
    y -= ih + 9*mm

    # 5 domaines
    c.setFont(ISB, 7); c.setFillColor(TERRA)
    c.drawString(M, y, content['final_domains_label'].upper())
    y -= 9*mm

    for i, d in enumerate(content['final_domains']):
        bg = HexColor('#7A4D5C') if i % 2 == 0 else HexColor('#6E4454')
        c.setFillColor(bg)
        c.roundRect(M, y - 8.5*mm, CW, 9*mm, 2.5*mm, fill=1, stroke=0)
        c.setFont(ISB, 7.5); c.setFillColor(TERRA)
        c.drawString(M + 4*mm, y - 3.5*mm, f'0{i+1}')
        c.setFont(IM, 9.5); c.setFillColor(white)
        c.drawString(M + 12*mm, y - 3.5*mm, d)
        y -= 10.5*mm

    y -= 7*mm

    cta_h = 24*mm
    c.setFillColor(TERRA)
    c.roundRect(M, y - cta_h, CW, cta_h, 5*mm, fill=1, stroke=0)
    c.setFont(ISB, 10); c.setFillColor(white)
    c.drawCentredString(W / 2, y - 8*mm, content['final_cta_title'])
    c.setFont(IR, 8.5); c.setFillColor(IVORY)
    c.drawCentredString(W / 2, y - 14.5*mm, content['final_cta_sub'])
    c.linkURL(OFFER_URL, (M, y - cta_h, W - M, y), thickness=0)
    y -= cta_h + 8*mm

    c.setFont(ISB, 8); c.setFillColor(white)
    c.drawCentredString(W / 2, y, "Valérie Mailland · Fondatrice · EXEC\'IA Consulting")
    y -= 6*mm
    c.setFont(IR, 7); c.setFillColor(GREY_PALE)
    c.drawCentredString(W / 2, y, SITE_URL)
    c.linkURL(SITE_URL, (W / 2 - 32*mm, y - 2*mm, W / 2 + 32*mm, y + 6*mm), thickness=0)

    footer(c, lang)
    c.showPage()


# ── CONTENUS — FRANÇAIS (accents complets) ────────────────────────────────────
CONTENT = {
'fr': {
    'cover_pretitle': 'DIRECTION GÉNÉRALE  ·  INTELLIGENCE ARTIFICIELLE  ·  Q4 2026',
    'cover_title': ['5 QUESTIONS QUI VALENT', "PLUS QU\'UN NOUVEAU PROJET IA"],
    'cover_subtitle': 'La plupart des entreprises cherchent de nouvelles solutions.',
    'cover_caption': 'Les meilleures commencent par se poser les bonnes questions.  5 min de lecture.',
    'cover_cta_title': 'Entretien préliminaire offert  ·  30 min  ·  Sans engagement  ·  Confidentiel',
    'cover_cta_sub': 'contact@exec-ia.ai  ·  exec-ia.ai',
    'questions': [
        {
            'btn': '0 dirigeant ne connaît le coût réel de l\'attente stratégique',
            'title': 'Combien coûte réellement une décision reportée de 90 jours ?',
            'cat': 'Décision stratégique',
            'idea_label': 'Idée clé',
            'idea': [
                'Les dirigeants craignent les mauvaises décisions.',
                '',
                'Ils devraient davantage craindre les décisions qui n\'arrivent jamais.',
                'Chaque arbitrage repoussé immobilise un budget, ralentit les équipes',
                'et crée un coût caché — invisible jusqu\'au jour où il devient stratégique.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quelle décision importante est discutée depuis plus de trois mois sans avoir été prise — et quel est le coût réel de ce report ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Une décision imparfaite crée du mouvement.',
                'Une décision absente crée de l\'immobilisme.',
            ],
            'offer_link': 'NIVEAU I · CLARIFIEZ  —  Séance de cadrage 490 €  ›  exec-ia.ai',
        },
        {
            'btn': '30 % du temps manager ne crée aucune valeur stratégique',
            'title': '20 % du temps de vos managers crée-t-il réellement de la valeur ?',
            'cat': 'Productivité managériale',
            'idea_label': 'Idée clé',
            'idea': [
                'Vos collaborateurs les plus expérimentés sont absorbés par des réunions,',
                'des reportings, des validations et des recherches d\'information.',
                '',
                'Le sujet n\'est pas le temps perdu.',
                'Le sujet est la valeur qui n\'est jamais créée.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Si vous rendiez une journée par semaine à vos 5 meilleurs managers, où investiriez-vous ce temps ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Le gain de productivité n\'a aucune valeur',
                'tant qu\'il n\'est pas transformé en meilleure décision.',
            ],
            'offer_link': 'NIVEAU II · COMPRENEZ & EMBARQUEZ  —  Leadership & Décision IA  ›  exec-ia.ai',
        },
        {
            'btn': '1 départ peut effacer 20 ans d\'expérience — sans aucun signal d\'alerte',
            'title': 'Quelle partie de votre entreprise partirait à la retraite demain ?',
            'cat': 'Transmission du savoir dirigeant',
            'idea_label': 'Idée clé',
            'idea': [
                '3 experts peuvent détenir 80 % du savoir critique de votre entreprise.',
                '',
                'Ces connaissances ne figurent dans aucun document.',
                'Elles vivent dans la tête de quelques personnes — raccourcis, arbitrages,',
                'intuitions. Quand elles partent, la capacité de décider part avec elles.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Si 3 personnes quittaient l\'entreprise demain, quelles décisions deviendraient impossibles à prendre ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'La transmission du savoir n\'est pas un sujet RH.',
                'C\'est un sujet de continuité stratégique.',
            ],
            'offer_link': 'NIVEAU III · DÉCIDEZ DANS LA DURÉE  —  Advisory de Direction  ›  exec-ia.ai',
        },
        {
            'btn': '1 client perdu sur 5 avait déjà envoyé des signaux — ignorés',
            'title': 'À quel moment précis vos clients commencent-ils à décrocher ?',
            'cat': 'Expérience client et rétention',
            'idea_label': 'Idée clé',
            'idea': [
                'Les clients ne partent presque jamais brutalement.',
                '',
                'Ils accumulent des micro-déceptions, puis prennent une décision silencieuse.',
                'La plupart des entreprises détectent cette décision plusieurs semaines trop',
                'tard — bien après que le client perdu a compté ses pertes.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quels sont les 3 moments où un client décide de rester ou de partir — et les observez-vous aujourd\'hui ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Un client perdu vaut plus que 100 leads.',
                'Ce qui n\'est pas observé ne peut pas être amélioré.',
            ],
            'offer_link': 'NIVEAU III · DÉCIDEZ DANS LA DURÉE  —  Advisory de Direction  ›  exec-ia.ai',
        },
        {
            'btn': '50 outils, 0 gouvernance — et si l\'IA décidait déjà à votre place ?',
            'title': 'Qui prend réellement les décisions dans votre organisation ?',
            'cat': 'Gouvernance de l\'IA',
            'idea_label': 'Idée clé',
            'idea': [
                'Certaines décisions sont prises par des outils.',
                'D\'autres par des habitudes. D\'autres encore par des experts',
                'que personne ne remet en question.',
                '',
                '10 projets en parallèle. 2 réellement stratégiques.',
                'Le sujet n\'est pas l\'IA. Le sujet est le contrôle.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quelles décisions critiques ne devraient jamais être déléguées — et lesquelles l\'ont déjà été sans que vous le sachiez ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Une organisation est bien gouvernée',
                'lorsqu\'elle sait pourquoi elle décide — pas seulement comment.',
            ],
            'offer_link': 'NIVEAU IV · TRANSFORMEZ  —  Mission de Transformation  ›  exec-ia.ai',
        },
    ],
    'final_pretitle': "L\'APPROCHE EXEC\'IA  ·  CONSULTING STRATÉGIQUE EN INTELLIGENCE ARTIFICIELLE",
    'final_title': ['Décider avec clarté.', 'Dans un monde où l\'IA redessine les règles.'],
    'final_body': [
        'Les entreprises ne manquent pas d\'outils ni d\'informations sur l\'IA.',
        'Elles manquent de clarté sur ce qui mérite réellement',
        'l\'attention — et la décision — de leur Direction Générale.',
    ],
    'final_domains_label': "EXEC\'IA accompagne les dirigeants dans cinq domaines",
    'final_domains': [
        'Priorisation des investissements IA',
        'Productivité managériale et gain de temps',
        'Transmission des savoirs critiques',
        'Expérience client et rétention',
        'Gouvernance de l\'IA',
    ],
    'final_cta_title': '30 MINUTES  ·  CONFIDENTIEL  ·  SANS ENGAGEMENT',
    'final_cta_sub': 'Entretien préliminaire offert  ·  contact@exec-ia.ai',
},
'en': {
    'cover_pretitle': 'EXECUTIVE LEADERSHIP  ·  ARTIFICIAL INTELLIGENCE  ·  Q4 2026',
    'cover_title': ['5 QUESTIONS WORTH MORE', 'THAN A NEW AI PROJECT'],
    'cover_subtitle': 'Most companies look for new solutions.',
    'cover_caption': 'The best ones start by asking the right questions.  5 min read.',
    'cover_cta_title': 'Complimentary interview  ·  30 min  ·  No commitment  ·  Confidential',
    'cover_cta_sub': 'contact@exec-ia.ai  ·  exec-ia.ai',
    'questions': [
        {
            'btn': '0 executives know the real cost of strategic waiting',
            'title': 'How much does a decision deferred for 90 days actually cost?',
            'cat': 'Strategic decision-making',
            'idea_label': 'Key insight',
            'idea': [
                'Leaders fear making bad decisions.',
                '',
                'They should fear even more the decisions that never get made.',
                'Every postponed choice freezes budget, slows teams and creates',
                'a hidden cost — invisible until the day it becomes strategic.',
            ],
            'codir_label': 'Board question',
            'codir': 'What important decision has been discussed for over three months without being made — and what is the real cost of that deferral?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "An imperfect decision creates momentum.",
                "An absent decision creates stagnation.",
            ],
            'offer_link': 'LEVEL I · CLARIFY  —  Strategic Framing Session 490 €  ›  exec-ia.ai',
        },
        {
            'btn': "30% of manager time creates no strategic value",
            'title': "Do 20% of your managers' time truly create value?",
            'cat': 'Managerial productivity',
            'idea_label': 'Key insight',
            'idea': [
                'Your most experienced people are absorbed by meetings,',
                'reporting, validations and information searches.',
                '',
                'The issue is not wasted time.',
                'The issue is value that is never created.',
            ],
            'codir_label': 'Board question',
            'codir': 'If you gave your top 5 managers one extra day per week, where would you invest that time?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "Productivity gains have no value",
                "until transformed into better decisions.",
            ],
            'offer_link': 'LEVEL II · UNDERSTAND & ALIGN  —  AI Leadership & Decision  ›  exec-ia.ai',
        },
        {
            'btn': '1 departure can erase 20 years of experience — without warning',
            'title': 'What part of your company would retire tomorrow?',
            'cat': 'Executive knowledge transfer',
            'idea_label': 'Key insight',
            'idea': [
                '3 experts may hold 80% of your company\'s critical knowledge.',
                '',
                'That knowledge lives in no document.',
                'It lives in a few people\'s heads — shortcuts, judgments, intuitions.',
                'When they leave, the ability to decide accurately leaves with them.',
            ],
            'codir_label': 'Board question',
            'codir': 'If 3 people left tomorrow, which decisions would become impossible to make?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "Knowledge transfer is not an HR matter.",
                "It is a strategic continuity matter.",
            ],
            'offer_link': 'LEVEL III · DECIDE OVER TIME  —  Executive Advisory  ›  exec-ia.ai',
        },
        {
            'btn': '1 in 5 lost clients had already sent signals — ignored',
            'title': 'At what exact moment do your clients start disengaging?',
            'cat': 'Customer experience and retention',
            'idea_label': 'Key insight',
            'idea': [
                'Clients almost never leave abruptly.',
                '',
                'They accumulate micro-disappointments, then make a silent decision.',
                'Most companies detect this decision several weeks too late —',
                'long after the lost client has moved on.',
            ],
            'codir_label': 'Board question',
            'codir': 'What are the 3 moments where a client decides to stay or leave — and are you observing them today?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "One lost client is worth more than 100 leads.",
                "What is not observed cannot be improved.",
            ],
            'offer_link': 'LEVEL III · DECIDE OVER TIME  —  Executive Advisory  ›  exec-ia.ai',
        },
        {
            'btn': '50 tools, 0 governance — what if AI was already deciding for you?',
            'title': 'Who is really making the decisions in your organisation?',
            'cat': 'AI governance',
            'idea_label': 'Key insight',
            'idea': [
                'Some decisions are made by tools.',
                'Others by habits. Others still by experts no one questions.',
                '',
                '10 projects running in parallel. 2 truly strategic.',
                'The issue is not AI. The issue is control.',
            ],
            'codir_label': 'Board question',
            'codir': 'Which critical decisions should never be delegated — and which have already been, without your knowledge?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "An organisation is well governed",
                "when it knows why it decides — not just how.",
            ],
            'offer_link': 'LEVEL IV · TRANSFORM  —  Transformation Mission  ›  exec-ia.ai',
        },
    ],
    'final_pretitle': "THE EXEC\'IA APPROACH  ·  STRATEGIC AI CONSULTING",
    'final_title': ['Decide with clarity.', 'In a world where AI rewrites the rules.'],
    'final_body': [
        'Companies don\'t lack tools or information about AI.',
        "They lack clarity on what truly deserves",
        "the attention — and the decision — of their Executive Committee.",
    ],
    'final_domains_label': "EXEC\'IA supports executives across five domains",
    'final_domains': [
        'AI investment prioritisation',
        'Managerial productivity and time savings',
        'Critical knowledge transfer',
        'Customer experience and retention',
        'AI governance',
    ],
    'final_cta_title': '30 MINUTES  ·  CONFIDENTIAL  ·  NO COMMITMENT',
    'final_cta_sub': 'Complimentary interview  ·  contact@exec-ia.ai',
},
'es': {
    'cover_pretitle': 'DIRECCIÓN GENERAL  ·  INTELIGENCIA ARTIFICIAL  ·  Q4 2026',
    'cover_title': ['5 PREGUNTAS QUE VALEN MÁS', 'QUE UN NUEVO PROYECTO DE IA'],
    'cover_subtitle': 'La mayoría de las empresas buscan nuevas soluciones.',
    'cover_caption': 'Las mejores empiezan por hacerse las preguntas correctas.  5 min de lectura.',
    'cover_cta_title': 'Entrevista preliminar gratuita  ·  30 min  ·  Sin compromiso  ·  Confidencial',
    'cover_cta_sub': 'contact@exec-ia.ai  ·  exec-ia.ai',
    'questions': [
        {
            'btn': '0 directivos conocen el coste real de la espera estratégica',
            'title': '¿Cuánto cuesta realmente una decisión aplazada 90 días?',
            'cat': 'Decisión estratégica',
            'idea_label': 'Idea clave',
            'idea': [
                'Los directivos temen tomar malas decisiones.',
                '',
                'Deberían temer aún más las decisiones que nunca se toman.',
                'Cada arbitraje aplazado inmoviliza un presupuesto, ralentiza equipos',
                'y crea un coste oculto — invisible hasta que se vuelve estratégico.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Qué decisión importante lleva más de tres meses debatiéndose — y cuál es el coste real de ese aplazamiento?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'Una decisión imperfecta crea movimiento.',
                'Una decisión ausente crea inmovilismo.',
            ],
            'offer_link': 'NIVEL I · CLARIFICAR  —  Sesión de encuadre 490 €  ›  exec-ia.ai',
        },
        {
            'btn': 'El 30 % del tiempo directivo no genera ningún valor estratégico',
            'title': '¿El 20 % del tiempo de sus managers crea realmente valor?',
            'cat': 'Productividad directiva',
            'idea_label': 'Idea clave',
            'idea': [
                'Sus colaboradores más experimentados están absorbidos',
                'por reuniones, informes, validaciones y búsquedas de información.',
                '',
                'El problema no es el tiempo perdido.',
                'El problema es el valor que nunca se crea.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Si diera un día extra a la semana a sus 5 mejores managers, dónde invertiría ese tiempo?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'La ganancia de productividad no tiene valor',
                'hasta que se transforma en una mejor decisión.',
            ],
            'offer_link': 'NIVEL II · COMPRENDA & ALÍNEE  —  Liderazgo & Decisión IA  ›  exec-ia.ai',
        },
        {
            'btn': '1 salida puede borrar 20 años de experiencia — sin ningún aviso',
            'title': '¿Qué parte de su empresa se jubilaria mañana?',
            'cat': 'Transmisión del conocimiento directivo',
            'idea_label': 'Idea clave',
            'idea': [
                '3 expertos pueden concentrar el 80 % del conocimiento crítico.',
                '',
                'Ese conocimiento no figura en ningún documento.',
                'Vive en la mente de unas pocas personas — atajos, criterios,',
                'intuiciones. Cuando se van, la capacidad de decidir se va con ellas.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Si 3 personas se marcharan mañana, qué decisiones serían imposibles de tomar?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'La transmisión del conocimiento no es un asunto de RRHH.',
                'Es un asunto de continuidad estratégica.',
            ],
            'offer_link': 'NIVEL III · DECIDIR EN EL TIEMPO  —  Advisory de Dirección  ›  exec-ia.ai',
        },
        {
            'btn': '1 de cada 5 clientes perdidos ya había enviado señales — ignoradas',
            'title': '¿En qué momento exacto sus clientes empiezan a desconectarse?',
            'cat': 'Experiencia del cliente y retención',
            'idea_label': 'Idea clave',
            'idea': [
                'Los clientes casi nunca se van de golpe.',
                '',
                'Acumulan micro-decepciones y luego toman una decisión silenciosa.',
                'La mayoría de las empresas detectan esta decisión varias semanas tarde',
                '— mucho después de que el cliente perdido haya tomado su decisión.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Cuáles son los 3 momentos en los que un cliente decide quedarse o marcharse — y los observa hoy?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'Un cliente perdido vale más que 100 leads.',
                'Lo que no se observa no puede mejorarse.',
            ],
            'offer_link': 'NIVEL III · DECIDIR EN EL TIEMPO  —  Advisory de Dirección  ›  exec-ia.ai',
        },
        {
            'btn': '50 herramientas, 0 gobernanza — ¿y si la IA ya decidiera por usted?',
            'title': '¿Quién toma realmente las decisiones en su organización?',
            'cat': 'Gobernanza de la IA',
            'idea_label': 'Idea clave',
            'idea': [
                'Algunas decisiones las toman las herramientas.',
                'Otras los hábitos. Otras más, expertos que nadie cuestiona.',
                '',
                '10 proyectos en paralelo. 2 realmente estratégicos.',
                'El problema no es la IA. El problema es el control.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Qué decisiones críticas nunca deberían delegarse — y cuáles ya lo han sido sin que usted lo supiera?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'Una organización está bien gobernada',
                'cuando sabe por qué decide — no solo cómo.',
            ],
            'offer_link': 'NIVEL IV · TRANSFORMAR  —  Misión de Transformación  ›  exec-ia.ai',
        },
    ],
    'final_pretitle': "EL ENFOQUE EXEC\'IA  ·  CONSULTORÍA ESTRATÉGICA EN INTELIGENCIA ARTIFICIAL",
    'final_title': ['Decidir con claridad.', 'En un mundo donde la IA redefine las reglas.'],
    'final_body': [
        'Las empresas no carecen de herramientas ni de información sobre IA.',
        'Carecen de claridad sobre lo que merece realmente',
        'la atención — y la decisión — de su Dirección General.',
    ],
    'final_domains_label': "EXEC\'IA acompaña a los directivos en cinco ámbitos",
    'final_domains': [
        'Priorización de inversiones en IA',
        'Productividad directiva y ahorro de tiempo',
        'Transmisión del conocimiento crítico',
        'Experiencia del cliente y retención',
        'Gobernanza de la IA',
    ],
    'final_cta_title': '30 MINUTOS  ·  CONFIDENCIAL  ·  SIN COMPROMISO',
    'final_cta_sub': 'Entrevista preliminar gratuita  ·  contact@exec-ia.ai',
},
}

OUTPUTS = {
    'fr': os.path.join(ASSETS, 'EXECIA_5Questions_Q4_2026_FR.pdf'),
    'en': os.path.join(ASSETS, 'EXECIA_5Questions_Q4_2026_EN.pdf'),
    'es': os.path.join(ASSETS, 'EXECIA_5Questions_Q4_2026_ES.pdf'),
}

def generate(lang):
    content = CONTENT[lang]
    out = OUTPUTS[lang]
    c = pdfcanvas.Canvas(out, pagesize=A4)
    c.setTitle(content['cover_title'][0] + ' ' + content['cover_title'][1])
    c.setAuthor("Valérie Mailland · Fondatrice · EXEC\'IA Consulting")
    c.setSubject('Lead Magnet Q4 2026 · ' + lang.upper())
    cover(c, lang, content)
    for i, q in enumerate(content['questions']):
        inner(c, lang, i + 1, q, i + 2)
    final(c, lang, content)
    c.save()
    print(f'[{lang.upper()}] {out}')

if __name__ == '__main__':
    import sys
    langs = sys.argv[1:] if len(sys.argv) > 1 else ['fr', 'en', 'es']
    for lang in langs:
        generate(lang)
    print('Done.')
