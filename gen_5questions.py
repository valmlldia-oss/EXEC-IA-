#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXEC\'IA — 5 Questions · Lead Magnet Q4 2026 · FR / EN / ES"""

from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

W, H = landscape(A4)

# ── Palette EXEC\'IA — valeurs exactes, aucune autre ──────────────────────────
PLUM       = HexColor('#633B4A')   # prune bordeaux rosé
PLUM_DARK  = HexColor('#4F2F3B')   # prune foncé officiel (jamais plus sombre)
PLUM_BOX   = HexColor('#633B4A')   # box sur fond prune foncé
TERRA      = HexColor('#C75F62')   # terracotta — LE SEUL CODE AUTORISÉ
TERRA_PALE = HexColor('#F0E6E3')   # terracotta très pâle pour fond card
IVORY      = HexColor('#F4EDE7')   # ivoire rosé officiel
IVORY2     = HexColor('#FAF6F2')   # cards légères
TEXT       = HexColor('#4F2F3B')   # corps de texte, prune foncé
PRUNE_LIGHT = HexColor('#8A5A68')  # texte secondaire
GREY_PALE  = HexColor('#D9C9C3')   # rose minéral pâle : texte sur fond sombre

M  = 18*mm
CW = W - 2*M

SITE_URL  = 'https://www.exec-ia.ai'
OFFER_URL = 'https://calendly.com/exec-ia'
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
# ── FOOTER — empilement strict de bas en haut, aucun overlap ─────────────────
#
#  [BAND_H=50mm]
#  top:    logo centré (fond blanc) 12mm         y=35..47mm
#          tagline Cormorant Italic terracotta    y=30mm
#          mention IA Inter Regular gris          y=24mm
#          boutons langue pill                    y=15..21mm
#          copyright Inter 6.5pt                 y=4mm
#  bottom: 0

BAND_H = 30*mm
LANG_URLS = {
    'fr': SITE_URL,
    'en': 'https://www.exec-ia.ai/index-en.html',
    'es': 'https://www.exec-ia.ai/index-es.html',
}
LANG_LABELS = {'fr': 'Français', 'en': 'English', 'es': 'Español'}

LOGO_FOOTER = os.path.join(ASSETS, 'logo-execia-bords-prune.png')

FOOTER_TXT = {
    'fr': ('Une expérience dirigeante au service de votre transformation IA',
           'Conception, contenus et automatisations assistés par IA · Validation humaine systématique',
           'Tous droits réservés'),
    'en': ('Executive experience in service of your AI transformation',
           'Design, content and automations assisted by AI · Systematic human validation',
           'All rights reserved'),
    'es': ('Una experiencia directiva al servicio de su transformación con IA',
           'Diseño, contenidos y automatizaciones asistidos por IA · Validación humana sistemática',
           'Todos los derechos reservados'),
}

def footer(c, lang, pg=None):
    """Pied de page compact, fond prune : logo à gauche, accroche au centre, langues à droite."""
    tagline, mention, rights = FOOTER_TXT[lang]
    c.setFillColor(PLUM)
    c.rect(0, 0, W, BAND_H, fill=1, stroke=0)
    c.setStrokeColor(TERRA); c.setLineWidth(0.8)
    c.line(0, BAND_H, W, BAND_H)

    # Ligne haute : logo (cartouche ivoire), accroche, boutons de langue
    row_y = 17*mm
    logo_h = 9*mm; logo_w = 34*mm
    if os.path.exists(LOGO_FOOTER):
        c.setFillColor(IVORY2)
        c.roundRect(M - 2*mm, row_y - 2*mm, logo_w + 4*mm, logo_h + 2*mm, 1.5*mm, fill=1, stroke=0)
        c.drawImage(LOGO_FOOTER, M, row_y - 1*mm, width=logo_w, height=logo_h,
                    preserveAspectRatio=True, mask='auto')
    else:
        c.setFont(CGB, 13); c.setFillColor(IVORY2)
        c.drawString(M, row_y + 1*mm, "EXEC'IA")
    c.linkURL(SITE_URL, (M - 2*mm, row_y - 2*mm, M + logo_w + 2*mm, row_y + logo_h), thickness=0)

    c.setFont(CGI, 12.5); c.setFillColor(IVORY2)
    c.drawCentredString(W / 2, row_y + 2.2*mm, tagline)

    BH_BTN = 6.5*mm
    langs_to_show = [(lc, LANG_LABELS[lc]) for lc in ['fr', 'en', 'es'] if lc != lang]
    btn_w_list = [c.stringWidth(lbl, IM, 8) + 9*mm for _, lbl in langs_to_show]
    bx = W - M - sum(btn_w_list) - 3*mm * (len(langs_to_show) - 1)
    for (lc, lbl), bw in zip(langs_to_show, btn_w_list):
        c.setStrokeColor(GREY_PALE); c.setLineWidth(0.6)
        c.roundRect(bx, row_y - 0.5*mm, bw, BH_BTN, BH_BTN / 2, fill=0, stroke=1)
        c.setFont(IM, 8); c.setFillColor(IVORY2)
        c.drawCentredString(bx + bw / 2, row_y + 1.6*mm, lbl)
        c.linkURL(LANG_URLS[lc], (bx, row_y - 0.5*mm, bx + bw, row_y + BH_BTN), thickness=0)
        bx += bw + 3*mm

    # Mention IA puis copyright
    c.setFont(IR, 7); c.setFillColor(GREY_PALE)
    c.drawCentredString(W / 2, 9*mm, mention)
    copy = "© 2026 Valérie Mailland · EXEC'IA · " + MAIL + " · " + rights
    c.setFont(IR, 6.5); c.setFillColor(GREY_PALE)
    c.drawCentredString(W / 2, 4*mm, copy)
    c.linkURL('mailto:' + MAIL, (W / 2 - 22*mm, 3*mm, W / 2 + 22*mm, 7*mm), thickness=0)
    if pg:
        c.setFont(IM, 7); c.setFillColor(GREY_PALE)
        c.drawRightString(W - M, 4*mm, f'{pg}/7')


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
    c.setFont(ISB, 7); c.setFillColor(IVORY2)
    c.drawCentredString(W - M - tw / 2, y - 5.5*mm, tag)
    y -= 12*mm

    # Pré-titre — Inter SemiBold terracotta, style "LE VÉRITABLE ENJEU" du site
    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, y, content['cover_pretitle'], charSpace=0.9)
    y -= 10*mm

    # Titre — Cormorant Garamond Bold + barre verticale fine terracotta gauche
    title_lines = wrap(c, content['cover_title'][0], CGB, 28, CW)
    title_lines += wrap(c, content['cover_title'][1], CGB, 28, CW)
    t_lead = 28 * 1.2
    title_h = len(title_lines) * t_lead
    thin_bar(c, M, y + 2*mm, title_h + 2*mm)
    c.setFont(CGB, 28); c.setFillColor(PLUM_DARK)
    for ln in title_lines:
        c.drawString(M + 5*mm, y, ln); y -= t_lead
    y -= 4*mm

    # Sous-titre — Cormorant Garamond Italic gris, comme site
    c.setFont(CGI, 14); c.setFillColor(PLUM)
    c.drawString(M, y, content['cover_subtitle'])
    y -= 7*mm
    c.setFont(IR, 8); c.setFillColor(PRUNE_LIGHT)
    c.drawString(M, y, content['cover_caption'])
    y -= 10*mm

    # ── 5 BOUTONS — pills avec cercle terracotta + numéro ────────────────────
    NUM_R  = 4*mm
    TXT_X  = M + NUM_R * 2 + 5*mm
    TXT_W  = W - M - TXT_X - 5*mm
    GAP    = 2.5*mm
    L_LEAD = 9.5 * 1.35
    PAD_V  = 3.5*mm

    def btn_h(txt):
        return len(wrap(c, txt, IM, 9.5, TXT_W)) * L_LEAD + PAD_V * 2

    CTA_H   = 26*mm
    CTA_GAP = 4*mm

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
        c.setFont(ISB, 7); c.setFillColor(IVORY2)
        c.drawCentredString(cx, cy - 0.9*mm, f'0{i+1}')
        # Texte Inter Medium prune
        lines = wrap(c, q['btn'], IM, 9.5, TXT_W)
        th_txt = len(lines) * L_LEAD
        ty = cy + (len(lines) - 1) * L_LEAD / 2 - 9.5 * 0.35
        c.setFont(IM, 9.5); c.setFillColor(PLUM)
        for ln in lines:
            c.drawString(TXT_X, ty, ln); ty -= L_LEAD
        c.linkAbsolute("", f"question_{i+1}", (M, y - bh, W - M, y), thickness=0)
        y -= bh + GAP

    y -= CTA_GAP

    # ── CTA — identique site : "Entretien préliminaire — offert" ─────────────
    # Box fond terracotta pâle + bord terracotta + bouton PLUM_DARK à droite
    c.setFillColor(TERRA_PALE)
    c.roundRect(M, y - CTA_H, CW, CTA_H, 5*mm, fill=1, stroke=0)
    c.setStrokeColor(TERRA); c.setLineWidth(0.8)
    c.roundRect(M, y - CTA_H, CW, CTA_H, 5*mm, fill=0, stroke=1)

    # Texte gauche
    c.setFont(CGB, 13); c.setFillColor(PLUM_DARK)
    c.drawString(M + 6*mm, y - 7.5*mm, content['cta_title'])
    c.setFont(IR, 8.5); c.setFillColor(TEXT)
    c.drawString(M + 6*mm, y - 13*mm, content['cta_line1'])
    c.drawString(M + 6*mm, y - 17.5*mm, content['cta_line2'])
    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M + 6*mm, y - 22.5*mm, content['cta_tags'])

    # Bouton Terracotta à droite — "Prendre rendez-vous"
    btn_txt = content['cta_btn']
    bw = c.stringWidth(btn_txt, ISB, 8.5) + 10*mm
    bx = W - M - bw - 4*mm
    by = y - CTA_H / 2 - 6*mm
    bh2 = 12*mm
    c.setFillColor(TERRA)
    c.roundRect(bx, by, bw, bh2, bh2 / 2, fill=1, stroke=0)
    c.setFont(ISB, 8.5); c.setFillColor(IVORY2)
    c.drawCentredString(bx + bw / 2, by + bh2 / 2 - 1.1*mm, btn_txt)
    assert y - CTA_H >= BAND_H + 3*mm, ('cover overflow', (y - CTA_H) / mm)
    c.linkURL(OFFER_URL, (bx, by, bx + bw, by + bh2), thickness=0)
    c.linkURL(OFFER_URL, (M, y - CTA_H, W - M, y), thickness=0)

    footer(c, lang)
    c.showPage()


# ── PAGE INTÉRIEURE ───────────────────────────────────────────────────────────
def label(c, x, y, txt, col, size=7.5):
    """Libellé en capitales espacées (style « LE VÉRITABLE ENJEU » du site)."""
    c.setFont(ISB, size); c.setFillColor(col)
    c.drawString(x, y, txt.upper(), charSpace=0.9)

def paragraphs(lines):
    """Les lignes coupées à la main deviennent des paragraphes pleine largeur."""
    out, cur = [], []
    for l in lines:
        if l: cur.append(l)
        elif cur: out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out

def inner(c, lang, qnum, q, pg):
    c.bookmarkPage(f"question_{qnum}")
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    TOP = H - 13*mm
    BOT = BAND_H + 9*mm
    y   = TOP
    IW  = CW - 12*mm
    GAP = 5*mm

    label(c, M, y, f'0{qnum}  ·  {q["cat"]}', TERRA)
    y -= 11*mm

    title_lines = wrap(c, q['title'], CGSB, 25, CW - 6*mm)
    t_lead = 25 * 1.2
    thin_bar(c, M, y + 2.5*mm, len(title_lines) * t_lead + 2*mm)
    c.setFont(CGSB, 25); c.setFillColor(PLUM_DARK)
    for ln in title_lines:
        c.drawString(M + 5*mm, y, ln); y -= t_lead
    y -= 6*mm

    idea = paragraphs(q['idea'])
    offer_h = 8*mm

    def layout(k):
        f_i, f_q, f_c = 10.5 * k, 14 * k, 15.5 * k
        pad = 5.5*mm * k
        h1 = sum(text_h(c, t, IR, f_i, IW, f_i * 1.5) for t in idea) + 2.5*mm * (len(idea) - 1) + 8*mm + pad * 2
        h2 = text_h(c, q['codir'], CGSB, f_q, IW, f_q * 1.3) + 8*mm + pad * 2
        h3 = sum(text_h(c, t, CGI, f_c, IW, f_c * 1.3) + 1.5*mm for t in q['conviction']) + 8*mm + pad * 2
        return (f_i, f_q, f_c, pad, h1, h2, h3)

    k = 1.22                                   # on remplit la page, puis on réduit si besoin
    while True:
        f_i, f_q, f_c, pad, h1, h2, h3 = layout(k)
        if h1 + h2 + h3 + GAP * 2 + offer_h <= y - BOT or k <= 0.8: break
        k -= 0.02

    # Idée clé : fond ivoire clair, filet prune
    c.setFillColor(IVORY2)
    c.roundRect(M, y - h1, CW, h1, 3*mm, fill=1, stroke=0)
    thin_bar(c, M + 1*mm, y - 1*mm, h1 - 2*mm, PLUM)
    label(c, M + 6*mm, y - pad - 1*mm, q['idea_label'], PLUM)
    iy = y - pad - 9*mm
    for t in idea:
        iy = draw_text(c, M + 6*mm, iy, t, IR, f_i, TEXT, IW, f_i * 1.5) - 2.5*mm
    y -= h1 + GAP

    # Question de CODIR : fond terracotta pâle, filet terracotta
    c.setFillColor(TERRA_PALE)
    c.roundRect(M, y - h2, CW, h2, 3*mm, fill=1, stroke=0)
    thin_bar(c, M + 1*mm, y - 1*mm, h2 - 2*mm, TERRA)
    label(c, M + 6*mm, y - pad - 1*mm, q['codir_label'], TERRA)
    draw_text(c, M + 6*mm, y - pad - 10*mm, q['codir'], CGSB, f_q, PLUM_DARK, IW, f_q * 1.3)
    y -= h2 + GAP

    # Conviction : aplat prune, filet terracotta, texte ivoire
    c.setFillColor(PLUM)
    c.roundRect(M, y - h3, CW, h3, 3*mm, fill=1, stroke=0)
    thin_bar(c, M + 1*mm, y - 1*mm, h3 - 2*mm, TERRA)
    label(c, M + 6*mm, y - pad - 1*mm, q['conviction_label'], GREY_PALE)
    cy = y - pad - 10.5*mm
    for t in q['conviction']:
        cy = draw_text(c, M + 6*mm, cy, t, CGI, f_c, IVORY2, IW, f_c * 1.3) - 1.5*mm
    y -= h3 + 6*mm

    off_y = max(y, BOT - 2*mm)
    c.setFont(ISB, 8); c.setFillColor(TERRA)
    c.drawString(M, off_y, q.get('offer_link', 'exec-ia.ai'), charSpace=0.3)
    c.linkURL(OFFER_URL, (M, off_y - 2*mm, W - M, off_y + 7*mm), thickness=0)
    assert off_y >= BAND_H + 4*mm, ('inner overflow', qnum, off_y / mm)

    footer(c, lang, pg)
    c.showPage()


# ── PAGE FINALE ───────────────────────────────────────────────────────────────
def final(c, lang, content):
    """Page finale sur deux colonnes : conviction à gauche, 5 domaines et prise de rendez-vous à droite."""
    c.setFillColor(PLUM_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    GUT = 12*mm
    LW  = CW * 0.52                      # colonne gauche
    RX  = M + LW + GUT                   # colonne droite
    RW  = W - M - RX
    TOP = H - 14*mm

    # ── Colonne gauche ──────────────────────────────────────────────────────
    y = TOP
    c.setFont(ISB, 7.5); c.setFillColor(GREY_PALE)
    c.drawString(M, y, content['final_pretitle'])
    y -= 13*mm
    for i, line in enumerate(content['final_title']):
        size = 25
        col = TERRA if i == 1 else IVORY2
        for ln in wrap(c, line, CGB, size, LW):
            c.setFont(CGB, size); c.setFillColor(col)
            c.drawString(M, y, ln); y -= size * 1.15
        y -= 2*mm
    y -= 2*mm
    c.setStrokeColor(TERRA); c.setLineWidth(0.8)
    c.line(M, y, M + 18*mm, y)
    y -= 9*mm

    lines = content['final_body']
    BW = LW - 12*mm
    ih = sum(text_h(c, l, CGI, 12, BW, 12 * 1.35) for l in lines) + 9*mm
    c.setFillColor(PLUM_BOX)
    c.roundRect(M, y - ih, LW, ih, 3*mm, fill=1, stroke=0)
    thin_bar(c, M + 1*mm, y - 1*mm, ih - 2*mm, TERRA)
    iy = y - 7.5*mm
    for line in lines:
        iy = draw_text(c, M + 6*mm, iy, line, CGI, 12, IVORY2, BW, 12 * 1.35)
    y -= ih + 8*mm

    # Conviction : paragraphes recomposés pour la largeur de colonne
    paras, cur = [], []
    for line in content.get('final_body2', []):
        if line: cur.append(line)
        elif cur: paras.append(' '.join(cur)); cur = []
    if cur: paras.append(' '.join(cur))
    for k, para in enumerate(paras):
        col = IVORY2 if k == len(paras) - 1 else GREY_PALE
        y = draw_text(c, M, y, para, IR, 10, col, LW, 10 * 1.5)
        y -= 3*mm

    # ── Colonne droite ──────────────────────────────────────────────────────
    y = TOP
    c.setFont(ISB, 7.5); c.setFillColor(GREY_PALE)
    c.drawString(RX, y, content['final_domains_label'].upper())
    y -= 6*mm
    ROW = 10*mm
    for i, d in enumerate(content['final_domains']):
        c.setFillColor(PLUM_BOX)
        c.roundRect(RX, y - ROW, RW, ROW, 2.5*mm, fill=1, stroke=0)
        cx = RX + 6*mm; cy = y - ROW / 2
        c.setFillColor(TERRA)
        c.circle(cx, cy, 3.4*mm, fill=1, stroke=0)
        c.setFont(ISB, 7.5); c.setFillColor(IVORY2)
        c.drawCentredString(cx, cy - 1.3*mm, f'0{i+1}')
        c.setFont(IM, 10); c.setFillColor(IVORY2)
        c.drawString(RX + 13*mm, cy - 1.7*mm, d)
        y -= ROW + 2.5*mm
    y -= 6*mm

    # Encadré de prise de rendez-vous
    tl = wrap(c, content['final_cta_title'], CGB, 15, RW - 12*mm)
    cta_h = len(tl) * 15 * 1.2 + 26*mm
    c.setFillColor(TERRA)
    c.roundRect(RX, y - cta_h, RW, cta_h, 4*mm, fill=1, stroke=0)
    ty = y - 9*mm
    c.setFont(CGB, 15); c.setFillColor(IVORY2)
    for ln in tl:
        c.drawCentredString(RX + RW / 2, ty, ln); ty -= 15 * 1.2
    ty -= 1.5*mm
    c.setFont(IM, 8.5); c.setFillColor(IVORY2)
    c.drawCentredString(RX + RW / 2, ty, content['final_cta_sub'])
    ty -= 8*mm
    btn = content['cta_btn']
    bw = c.stringWidth(btn, ISB, 9) + 12*mm; bh = 8.5*mm
    bx = RX + (RW - bw) / 2
    c.setFillColor(IVORY2)
    c.roundRect(bx, ty - 2.5*mm, bw, bh, bh / 2, fill=1, stroke=0)
    c.setFont(ISB, 9); c.setFillColor(PLUM_DARK)
    c.drawCentredString(RX + RW / 2, ty + 0.3*mm, btn)
    c.linkURL(OFFER_URL, (RX, y - cta_h, RX + RW, y), thickness=0)
    y -= cta_h + 8*mm

    c.setFont(ISB, 8.5); c.setFillColor(IVORY2)
    c.drawCentredString(RX + RW / 2, y, "Valérie Mailland · Fondatrice · EXEC\'IA Consulting")
    y -= 5.5*mm
    c.setFont(IR, 8); c.setFillColor(GREY_PALE)
    c.drawCentredString(RX + RW / 2, y, content.get('final_cta_email', MAIL) + '  ·  exec-ia.ai')
    c.linkURL(SITE_URL, (RX, y - 2*mm, RX + RW, y + 5*mm), thickness=0)

    footer(c, lang)
    c.showPage()


# ── CONTENUS — FRANÇAIS (accents complets) ────────────────────────────────────
CONTENT = {
'fr': {
    'cover_pretitle': 'DIRECTION GÉNÉRALE  ·  INTELLIGENCE ARTIFICIELLE  ·  Q4 2026',
    'cover_title': ['5 QUESTIONS QUI VALENT', "PLUS QU\'UN NOUVEAU PROJET IA"],
    'cover_subtitle': 'La plupart des entreprises cherchent de nouvelles solutions.',
    'cover_caption': "L'IA redessine déjà les règles. La question est de savoir qui tient encore le crayon.  5 min de lecture.",
    'cover_cta_title': 'Entretien préliminaire · offert',
    'cover_cta_sub': 'contact@exec-ia.ai  ·  exec-ia.ai',
    'cta_title': 'Entretien préliminaire · offert',
    'cta_line1': '30 minutes pour comprendre votre situation et évaluer ensemble,',
    'cta_line2': 'la façon dont je peux vous être utile.',
    'cta_tags': 'Sans engagement  ·  Confidentiel',
    'cta_btn': 'Prendre rendez-vous',
    'questions': [
        {
            'btn': 'Peu de dirigeants connaissent le coût réel de l\'attente stratégique',
            'title': 'Combien coûte réellement une décision reportée de 90 jours ?',
            'cat': 'Décision stratégique',
            'idea_label': 'Idée clé',
            'idea': [
                'Les dirigeants craignent les mauvaises décisions.',
                '',
                'Ils devraient davantage craindre les décisions qui n\'arrivent jamais.',
                'Chaque arbitrage repoussé immobilise un budget, retarde des revenus,',
                'ralentit les équipes et laisse parfois un concurrent décider avant vous.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quelle décision importante est discutée depuis plus de trois mois sans avoir été prise, et quel est le coût réel de ce report ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Une décision imparfaite crée du mouvement.',
                'Une décision absente crée de l\'immobilisme.',
            ],
            'offer_link': 'NIVEAU I · CLARIFIEZ · 910 € HT solo / 1 490 € HT en CODIR › exec-ia.ai',
        },
        {
            'btn': 'Une partie significative du temps managérial ne crée aucune valeur stratégique',
            'title': '20 % du temps de vos managers crée-t-il réellement de la valeur ?',
            'cat': 'Productivité managériale',
            'idea_label': 'Idée clé',
            'idea': [
                'Vos collaborateurs les plus expérimentés sont absorbés par des réunions,',
                'des reportings, des validations et des recherches d\'information.',
                '',
                'Le sujet n\'est pas le temps perdu.',
                'Le sujet est la valeur, les décisions et les opportunités qui ne seront jamais créées.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Si vous rendiez une journée par semaine à vos 5 meilleurs managers, où investiriez-vous ce temps ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Le gain de productivité n\'a aucune valeur',
                'tant qu\'il n\'est pas transformé en meilleure décision.',
            ],
            'offer_link': 'NIVEAU I · CLARIFIEZ · 910 € HT solo / 1 490 € HT en CODIR › exec-ia.ai',
        },
        {
            'btn': '1 départ peut effacer 20 ans d\'expérience, sans aucun signal d\'alerte',
            'title': 'Quelle partie de votre entreprise partirait à la retraite demain ?',
            'cat': 'Transmission du savoir dirigeant',
            'idea_label': 'Idée clé',
            'idea': [
                'Une poignée d\'experts peut concentrer une part décisive du savoir critique de votre entreprise.',
                '',
                'Ces connaissances ne figurent dans aucun document.',
                'Elles vivent dans la tête de quelques personnes : raccourcis, arbitrages,',
                'intuitions. Quand elles partent, certaines décisions deviennent plus lentes, plus risquées ou plus coûteuses.',
                'Un dirigeant ressent immédiatement le danger.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Si 3 personnes quittaient l\'entreprise demain, quelles décisions deviendraient impossibles à prendre ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'La transmission du savoir n\'est pas un sujet RH.',
                'C\'est un sujet de continuité stratégique.',
            ],
            'offer_link': 'NIVEAU II · DÉCIDEZ DANS LA DURÉE · 3 910 € HT le programme › exec-ia.ai',
        },
        {
            'btn': 'De nombreux clients perdus avaient déjà envoyé des signaux faibles',
            'title': 'À quel moment précis vos clients commencent-ils à décrocher ?',
            'cat': 'Expérience client et rétention',
            'idea_label': 'Idée clé',
            'idea': [
                'Les clients ne partent presque jamais brutalement.',
                '',
                'Ils accumulent des micro-déceptions, puis prennent une décision silencieuse.',
                'La plupart des entreprises détectent cette décision plusieurs semaines trop',
                'tard, bien après que le client perdu a compté ses pertes.',
                '',
                'Un client perdu ne représente pas seulement un chiffre d\'affaires disparu.',
                'Il représente souvent des années de confiance, de recommandations et d\'opportunités.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quels sont les 3 moments où un client décide de rester ou de partir, et les observez-vous aujourd\'hui ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Un client perdu vaut plus que 100 leads.',
                'Ce qui n\'est pas observé ne peut pas être amélioré.',
            ],
            'offer_link': 'NIVEAU II · DÉCIDEZ DANS LA DURÉE · 3 910 € HT le programme › exec-ia.ai',
        },
        {
            'btn': '50 outils, 0 gouvernance : et si l\'IA décidait déjà à votre place ?',
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
            'codir': 'Quelles décisions critiques ne devraient jamais être déléguées, et lesquelles l\'ont déjà été sans que vous le sachiez ?',
            'conviction_label': "Conviction EXEC\'IA",
            'conviction': [
                'Une organisation est bien gouvernée',
                'lorsqu\'elle sait pourquoi elle décide : pas seulement comment.',
            ],
            'offer_link': 'NIVEAU III · TRANSFORMEZ · Sur devis, à partir de 6 910 € HT › exec-ia.ai',
        },
    ],
    'final_pretitle': "L\'APPROCHE EXEC\'IA  ·  CONSULTING STRATÉGIQUE EN INTELLIGENCE ARTIFICIELLE",
    'final_title': ['L\'IA redessine déjà les règles.', 'La question est de savoir qui tient encore le crayon.'],
    'final_body': [
        "Les entreprises ne manquent pas d'outils.",
        "Elles manquent souvent de clarté sur les décisions qui ne devraient jamais être déléguées.",
    ],
    'final_domains_label': "Ces cinq questions sont au cœur de nos missions",
    'final_domains': [
        'Priorisation des investissements IA',
        'Productivité managériale et gain de temps',
        'Transmission des savoirs critiques',
        'Expérience client et rétention',
        'Gouvernance de l\'IA',
    ],
    'final_cta_title': '30 minutes pour prendre du recul sur les décisions qui comptent.',
    'final_cta_sub': 'Entretien préliminaire confidentiel  ·  Sans engagement',
    'final_cta_email': 'contact@exec-ia.ai',
    'final_body2': [
        'Les organisations qui prennent ces cinq questions au sérieux découvrent',
        'généralement que leur principal sujet n\'est ni technologique ni opérationnel.',
        'Il est stratégique.',
        '',
        'La question n\'est pas de savoir si l\'IA transformera votre organisation.',
        'La question est de savoir si votre organisation décidera de cette transformation',
        'ou la subira.',
    ],
},
'en': {
    'cover_pretitle': 'EXECUTIVE LEADERSHIP  ·  ARTIFICIAL INTELLIGENCE  ·  Q4 2026',
    'cover_title': ['5 QUESTIONS WORTH MORE', 'THAN A NEW AI PROJECT'],
    'cover_subtitle': 'Most companies look for new solutions.',
    'cover_caption': 'AI is already rewriting the rules. The question is who still holds the pen.  5 min read.',
    'cover_cta_title': 'Complimentary preliminary interview',
    'cover_cta_sub': 'contact@exec-ia.ai  ·  exec-ia.ai',
    'cta_title': 'Complimentary preliminary interview',
    'cta_line1': '30 minutes to understand your situation and assess together,',
    'cta_line2': 'how I can be of use to you.',
    'cta_tags': 'No commitment  ·  Confidential',
    'cta_btn': 'Book a meeting',
    'questions': [
        {
            'btn': 'Few executives know the real cost of strategic waiting',
            'title': 'How much does a decision deferred for 90 days actually cost?',
            'cat': 'Strategic decision-making',
            'idea_label': 'Key insight',
            'idea': [
                'Leaders fear making bad decisions.',
                '',
                'They should fear even more the decisions that never get made.',
                'Every postponed choice freezes budget, delays revenue, slows teams',
                'and sometimes lets a competitor decide before you.',
            ],
            'codir_label': 'Board question',
            'codir': 'What important decision has been discussed for over three months without being made, and what is the real cost of that deferral?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "An imperfect decision creates momentum.",
                "An absent decision creates stagnation.",
            ],
            'offer_link': 'LEVEL I · CLARIFY · €910 excl. VAT solo / €1,490 excl. VAT leadership team › exec-ia.ai',
        },
        {
            'btn': "A significant portion of management time creates no strategic value",
            'title': "Do 20% of your managers' time truly create value?",
            'cat': 'Managerial productivity',
            'idea_label': 'Key insight',
            'idea': [
                'Your most experienced people are absorbed by meetings,',
                'reporting, validations and information searches.',
                '',
                'The issue is not wasted time.',
                'The issue is the value, decisions and opportunities that will never be created.',
            ],
            'codir_label': 'Board question',
            'codir': 'If you gave your top 5 managers one extra day per week, where would you invest that time?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "Productivity gains have no value",
                "until transformed into better decisions.",
            ],
            'offer_link': 'LEVEL I · CLARIFY · €910 excl. VAT solo / €1,490 excl. VAT leadership team › exec-ia.ai',
        },
        {
            'btn': '1 departure can erase 20 years of experience, without warning',
            'title': 'What part of your company would retire tomorrow?',
            'cat': 'Executive knowledge transfer',
            'idea_label': 'Key insight',
            'idea': [
                'A handful of experts may hold a decisive share of your company\'s critical knowledge.',
                '',
                'That knowledge lives in no document.',
                'It lives in a few people\'s heads: shortcuts, judgments, intuitions.',
                'When they leave, certain decisions become slower, riskier or more costly.',
                'A leader feels the danger immediately.',
            ],
            'codir_label': 'Board question',
            'codir': 'If 3 people left tomorrow, which decisions would become impossible to make?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "Knowledge transfer is not an HR matter.",
                "It is a strategic continuity matter.",
            ],
            'offer_link': 'LEVEL II · DECIDE OVER TIME · €3,910 excl. VAT for the programme › exec-ia.ai',
        },
        {
            'btn': 'Many lost clients had already sent weak signals',
            'title': 'At what exact moment do your clients start disengaging?',
            'cat': 'Customer experience and retention',
            'idea_label': 'Key insight',
            'idea': [
                'Clients almost never leave abruptly.',
                '',
                'They accumulate micro-disappointments, then make a silent decision.',
                'Most companies detect this decision several weeks too late,',
                'long after the lost client has moved on.',
                '',
                'A lost client is not just lost revenue.',
                'It often represents years of trust, referrals and opportunities that will never return.',
            ],
            'codir_label': 'Board question',
            'codir': 'What are the 3 moments where a client decides to stay or leave, and are you observing them today?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "One lost client is worth more than 100 leads.",
                "What is not observed cannot be improved.",
            ],
            'offer_link': 'LEVEL II · DECIDE OVER TIME · €3,910 excl. VAT for the programme › exec-ia.ai',
        },
        {
            'btn': '50 tools, 0 governance: what if AI were already deciding for you?',
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
            'codir': 'Which critical decisions should never be delegated, and which have already been, without your knowledge?',
            'conviction_label': "EXEC\'IA conviction",
            'conviction': [
                "An organisation is well governed",
                "when it knows why it decides: not just how.",
            ],
            'offer_link': 'LEVEL III · TRANSFORM · Quoted, from €6,910 excl. VAT › exec-ia.ai',
        },
    ],
    'final_pretitle': "THE EXEC\'IA APPROACH  ·  STRATEGIC AI CONSULTING",
    'final_title': ['AI is already rewriting the rules.', 'The question is who still holds the pen.'],
    'final_body': [
        "Companies don't lack tools.",
        "They often lack clarity on the decisions that should never be delegated.",
    ],
    'final_domains_label': "These five questions are at the heart of our work",
    'final_domains': [
        'AI investment prioritisation',
        'Managerial productivity and time savings',
        'Critical knowledge transfer',
        'Customer experience and retention',
        'AI governance',
    ],
    'final_cta_title': '30 minutes to step back on the decisions that matter.',
    'final_cta_sub': 'Confidential preliminary interview  ·  No commitment',
    'final_cta_email': 'contact@exec-ia.ai',
    'final_body2': [
        'Organisations that take these five questions seriously typically discover',
        'their main challenge is neither technological nor operational.',
        'It is strategic.',
        '',
        'The question is not whether AI will transform your organisation.',
        'The question is whether your organisation will decide that transformation',
        'or be swept along by it.',
    ],
},
'es': {
    'cover_pretitle': 'DIRECCIÓN GENERAL  ·  INTELIGENCIA ARTIFICIAL  ·  Q4 2026',
    'cover_title': ['5 PREGUNTAS QUE VALEN MÁS', 'QUE UN NUEVO PROYECTO DE IA'],
    'cover_subtitle': 'La mayoría de las empresas buscan nuevas soluciones.',
    'cover_caption': 'La IA ya está redibujando las reglas. La pregunta es quién sigue sosteniendo el lápiz.  5 min de lectura.',
    'cover_cta_title': 'Entrevista preliminar · gratuita',
    'cover_cta_sub': 'contact@exec-ia.ai  ·  exec-ia.ai',
    'cta_title': 'Entrevista preliminar · gratuita',
    'cta_line1': '30 minutos para comprender su situación y evaluar juntos,',
    'cta_line2': 'cómo puedo serle de utilidad.',
    'cta_tags': 'Sin compromiso  ·  Confidencial',
    'cta_btn': 'Reservar una cita',
    'questions': [
        {
            'btn': 'Pocos directivos conocen el coste real de la espera estratégica',
            'title': '¿Cuánto cuesta realmente una decisión aplazada 90 días?',
            'cat': 'Decisión estratégica',
            'idea_label': 'Idea clave',
            'idea': [
                'Los directivos temen tomar malas decisiones.',
                '',
                'Deberían temer aún más las decisiones que nunca se toman.',
                'Cada arbitraje aplazado inmoviliza un presupuesto, retrasa ingresos, ralentiza equipos',
                'y a veces deja que un competidor decida antes que usted.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Qué decisión importante lleva más de tres meses debatiéndose, y cuál es el coste real de ese aplazamiento?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'Una decisión imperfecta crea movimiento.',
                'Una decisión ausente crea inmovilismo.',
            ],
            'offer_link': 'NIVEL I · CLARIFICAR · 910 € +IVA individual / 1.490 € +IVA comité › exec-ia.ai',
        },
        {
            'btn': 'Una parte significativa del tiempo directivo no genera ningún valor estratégico',
            'title': '¿El 20 % del tiempo de sus managers crea realmente valor?',
            'cat': 'Productividad directiva',
            'idea_label': 'Idea clave',
            'idea': [
                'Sus colaboradores más experimentados están absorbidos',
                'por reuniones, informes, validaciones y búsquedas de información.',
                '',
                'El problema no es el tiempo perdido.',
                'El problema es el valor, las decisiones y las oportunidades que nunca se crearán.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Si diera un día extra a la semana a sus 5 mejores managers, dónde invertiría ese tiempo?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'La ganancia de productividad no tiene valor',
                'hasta que se transforma en una mejor decisión.',
            ],
            'offer_link': 'NIVEL I · CLARIFICAR · 910 € +IVA individual / 1.490 € +IVA comité › exec-ia.ai',
        },
        {
            'btn': '1 salida puede borrar 20 años de experiencia, sin ningún aviso',
            'title': '¿Qué parte de su empresa se jubilaria mañana?',
            'cat': 'Transmisión del conocimiento directivo',
            'idea_label': 'Idea clave',
            'idea': [
                'Un puñado de expertos puede concentrar una parte decisiva del conocimiento crítico.',
                '',
                'Ese conocimiento no figura en ningún documento.',
                'Vive en la mente de unas pocas personas: atajos, criterios,',
                'intuiciones. Cuando se van, ciertas decisiones se vuelven más lentas, más arriesgadas o más costosas.',
                'Un directivo siente el peligro de inmediato.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Si 3 personas se marcharan mañana, qué decisiones serían imposibles de tomar?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'La transmisión del conocimiento no es un asunto de RRHH.',
                'Es un asunto de continuidad estratégica.',
            ],
            'offer_link': 'NIVEL II · DECIDA A LARGO PLAZO · 3.910 € +IVA el programa › exec-ia.ai',
        },
        {
            'btn': 'Muchos clientes perdidos ya habían enviado señales débiles',
            'title': '¿En qué momento exacto sus clientes empiezan a desconectarse?',
            'cat': 'Experiencia del cliente y retención',
            'idea_label': 'Idea clave',
            'idea': [
                'Los clientes casi nunca se van de golpe.',
                '',
                'Acumulan micro-decepciones y luego toman una decisión silenciosa.',
                'La mayoría de las empresas detectan esta decisión varias semanas tarde',
                'mucho después de que el cliente perdido haya tomado su decisión.',
                '',
                'Un cliente perdido no representa solo un volumen de negocio perdido.',
                'Representa a menudo años de confianza, recomendaciones y oportunidades que no volverán.',
            ],
            'codir_label': 'Pregunta de Comité de Dirección',
            'codir': '¿Cuáles son los 3 momentos en los que un cliente decide quedarse o marcharse, y los observa hoy?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'Un cliente perdido vale más que 100 leads.',
                'Lo que no se observa no puede mejorarse.',
            ],
            'offer_link': 'NIVEL II · DECIDA A LARGO PLAZO · 3.910 € +IVA el programa › exec-ia.ai',
        },
        {
            'btn': '50 herramientas, 0 gobernanza: ¿y si la IA ya decidiera por usted?',
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
            'codir': '¿Qué decisiones críticas nunca deberían delegarse, y cuáles ya lo han sido sin que usted lo supiera?',
            'conviction_label': "Convicción EXEC\'IA",
            'conviction': [
                'Una organización está bien gobernada',
                'cuando sabe por qué decide: no solo cómo.',
            ],
            'offer_link': 'NIVEL III · TRANSFORMAR · Presupuesto a medida, desde 6.910 € +IVA › exec-ia.ai',
        },
    ],
    'final_pretitle': "EL ENFOQUE EXEC\'IA  ·  CONSULTORÍA ESTRATÉGICA EN INTELIGENCIA ARTIFICIAL",
    'final_title': ['La IA ya está redibujando las reglas.', 'La pregunta es quién sigue sosteniendo el lápiz.'],
    'final_body': [
        "Las empresas no carecen de herramientas.",
        "A menudo les falta claridad sobre las decisiones que nunca deberían delegarse.",
    ],
    'final_domains_label': "Estas cinco preguntas están en el corazón de nuestras misiones",
    'final_domains': [
        'Priorización de inversiones en IA',
        'Productividad directiva y ahorro de tiempo',
        'Transmisión del conocimiento crítico',
        'Experiencia del cliente y retención',
        'Gobernanza de la IA',
    ],
    'final_cta_title': '30 minutos para tomar perspectiva sobre las decisiones que importan.',
    'final_cta_sub': 'Entrevista preliminar confidencial  ·  Sin compromiso',
    'final_cta_email': 'contact@exec-ia.ai',
    'final_body2': [
        'Las organizaciones que toman en serio estas cinco preguntas descubren',
        'generalmente que su principal desafío no es tecnológico ni operativo.',
        'Es estratégico.',
        '',
        'La pregunta no es si la IA transformará su organización.',
        'La pregunta es si su organización decidirá esa transformación',
        'o la sufrirá.',
    ],
},
}

OUTPUTS = {
    'fr': os.path.join(ASSETS, 'EXECIA_5 Essentiels_Q4_2026_FR.pdf'),
    'en': os.path.join(ASSETS, 'EXECIA_The 5 Essentials_Q4_2026_EN.pdf'),
    'es': os.path.join(ASSETS, 'EXECIA_Los 5 Esenciales_Q4_2026_ES.pdf'),
}

def generate(lang):
    content = CONTENT[lang]
    out = OUTPUTS[lang]
    c = pdfcanvas.Canvas(out, pagesize=landscape(A4))
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
