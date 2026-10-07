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
        # Variantes « LF » : chiffres alignés (comme lnum sur le site), aucun gras 700
        'CGR':  'CormorantGaramond-Regular-LF.ttf',
        'CGI':  'CormorantGaramond-Italic-LF.ttf',
        'CGSB': 'CormorantGaramond-SemiBold-LF.ttf',
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


# ── MISE EN PAGE ÉDITORIALE (refonte du 07/10/2026) ───────────────────────────
# Mêmes polices que le site : Cormorant Garamond (400 / 600, italique) et Inter
# (400 / 500 / 600). Aucun gras 700. Logo encadré en haut à droite de chaque page.
import re

MIST    = HexColor('#D9C9C3')          # rose minéral pâle : bordures, texte sur prune
LOGO    = os.path.join(ASSETS, 'logo-execia-bords-prune.png')
LOGO_W  = 34*mm
LOGO_H  = LOGO_W * 212 / 450
BAND_H  = 24*mm                         # bandeau prune : couverture et page finale
FOOT_H  = 14*mm                         # pied de page fin : pages intérieures

LANG_URLS = {
    'fr': SITE_URL,
    'en': 'https://www.exec-ia.ai/index-en.html',
    'es': 'https://www.exec-ia.ai/index-es.html',
}
LANG_LABELS = {'fr': 'Français', 'en': 'English', 'es': 'Español'}
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

_HL = re.compile(r"^(.*?)(IA|AI)([.,;:!?»)]*)$")

def draw_hl(c, x, y, line, font, size, col, hl_col=TERRA, center=False):
    """Écrit une ligne en mettant « IA » / « AI » en terracotta, comme sur le site."""
    if center:
        x -= c.stringWidth(line, font, size) / 2
    c.setFont(font, size)
    sp = c.stringWidth(' ', font, size)
    for i, w in enumerate(line.split(' ')):
        m = _HL.match(w)
        if m and (m.group(1) == '' or m.group(1)[-1] in "'’(«"):
            parts = [(m.group(1), col), (m.group(2), hl_col), (m.group(3), col)]
        else:
            parts = [(w, col)]
        for txt, cc in parts:
            if not txt:
                continue
            c.setFillColor(cc)
            c.drawString(x, y, txt)
            x += c.stringWidth(txt, font, size)
        x += sp

def eyebrow(c, x, y, txt, col, size=7.2, center=False):
    """Libellé en petites capitales espacées (style des surtitres du site)."""
    txt = txt.upper()
    c.setFont(ISB, size); c.setFillColor(col)
    if center:
        x -= (c.stringWidth(txt, ISB, size) + 1.1 * (len(txt) - 1)) / 2
    c.drawString(x, y, txt, charSpace=1.1)

def thin_bar(c, x, y_top, height, color=TERRA, width=1.6):
    c.setStrokeColor(color); c.setLineWidth(width)
    c.line(x, y_top - height, x, y_top)

def logo_tr(c, on_dark=False):
    """Logo encadré, coin supérieur droit, cliquable vers le site."""
    x = W - M - LOGO_W
    y = H - 9*mm - LOGO_H
    if on_dark:
        c.setFillColor(IVORY2)
        c.roundRect(x - 1.5*mm, y + 1.5*mm, LOGO_W + 3*mm, LOGO_H - 3*mm, 1.5*mm, fill=1, stroke=0)
    if os.path.exists(LOGO):
        c.drawImage(LOGO, x, y, width=LOGO_W, height=LOGO_H, preserveAspectRatio=True, mask='auto')
    c.linkURL(SITE_URL, (x, y, x + LOGO_W, y + LOGO_H), thickness=0)

def footer_band(c, lang):
    """Bandeau prune (couverture et page finale) : accroche, langues, mentions."""
    tagline, mention, rights = FOOTER_TXT[lang]
    c.setFillColor(PLUM)
    c.rect(0, 0, W, BAND_H, fill=1, stroke=0)
    row_y = 14*mm
    c.setFont(ISB, 8); c.setFillColor(IVORY2)
    c.drawString(M, row_y + 0.6*mm, 'exec-ia.ai', charSpace=0.6)
    c.linkURL(SITE_URL, (M, row_y - 1*mm, M + 25*mm, row_y + 5*mm), thickness=0)
    draw_hl(c, W / 2, row_y + 0.3*mm, tagline, CGI, 13, IVORY2, center=True)
    BH = 6.2*mm
    langs = [(lc, LANG_LABELS[lc]) for lc in ['fr', 'en', 'es'] if lc != lang]
    widths = [c.stringWidth(lbl, IM, 7.8) + 9*mm for _, lbl in langs]
    bx = W - M - sum(widths) - 3*mm * (len(langs) - 1)
    for (lc, lbl), bw in zip(langs, widths):
        c.setStrokeColor(MIST); c.setLineWidth(0.6)
        c.roundRect(bx, row_y - 1.2*mm, bw, BH, BH / 2, fill=0, stroke=1)
        c.setFont(IM, 7.8); c.setFillColor(IVORY2)
        c.drawCentredString(bx + bw / 2, row_y + 0.9*mm, lbl)
        c.linkURL(LANG_URLS[lc], (bx, row_y - 1.2*mm, bx + bw, row_y + BH), thickness=0)
        bx += bw + 3*mm
    c.setFont(IR, 6.8); c.setFillColor(MIST)
    c.drawCentredString(W / 2, 7*mm, mention)
    c.setFont(IR, 6.3)
    c.drawCentredString(W / 2, 3.4*mm, "© 2026 Valérie Mailland · EXEC'IA · " + MAIL + ' · ' + rights)

def footer_slim(c, lang, pg):
    """Pied de page discret des pages intérieures : site, mention IA, pagination."""
    _, mention, rights = FOOTER_TXT[lang]
    y = 8*mm
    c.setFont(ISB, 7); c.setFillColor(PLUM)
    c.drawString(M, y, "EXEC'IA CONSULTING  ·  EXEC-IA.AI", charSpace=0.8)
    c.linkURL(SITE_URL, (M, y - 1.5*mm, M + 60*mm, y + 4*mm), thickness=0)
    c.setFont(IR, 6.5); c.setFillColor(PRUNE_LIGHT)
    c.drawCentredString(W / 2, y, mention)
    c.drawCentredString(W / 2, 4*mm, "© 2026 Valérie Mailland · EXEC'IA · " + rights)
    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawRightString(W - M, y, f'{pg:02d}  /  07')


# ── COUVERTURE ────────────────────────────────────────────────────────────────
def cover(c, lang, content):
    c.setFillColor(IVORY); c.rect(0, 0, W, H, fill=1, stroke=0)
    logo_tr(c)

    GUT = 14*mm
    LW  = CW * 0.55
    RX  = M + LW + GUT
    RW  = W - M - RX
    BOT = BAND_H + 11*mm

    # Colonne gauche : surtitre, titre, accroche
    y = H - 17*mm
    eyebrow(c, M, y, content['cover_pretitle'], TERRA)
    y -= 21*mm
    size = 40
    while size > 28 and any(c.stringWidth(p, CGR, size) > LW - 6*mm for p in content['cover_title_mc']):
        size -= 1
    lead = size * 1.1
    lines = []
    for part in content['cover_title_mc']:
        lines += wrap(c, part, CGR, size, LW - 6*mm)
    thin_bar(c, M, y + size * 0.78, len(lines) * lead - lead + size * 0.95)
    for ln in lines:
        draw_hl(c, M + 6*mm, y, ln, CGR, size, PLUM_DARK); y -= lead
    y -= 5*mm
    for ln in wrap(c, content['cover_subtitle'], CGI, 17, LW):
        c.setFont(CGI, 17); c.setFillColor(PLUM)
        c.drawString(M, y, ln); y -= 17 * 1.25
    y -= 1*mm
    for ln in wrap(c, content['cover_caption'], IR, 9.5, LW):
        draw_hl(c, M, y, ln, IR, 9.5, PRUNE_LIGHT); y -= 9.5 * 1.5

    # Encadré de prise de rendez-vous, en bas à gauche
    CTA_H = 30*mm
    cy0 = BOT
    c.setFillColor(IVORY2)
    c.roundRect(M, cy0, LW, CTA_H, 4*mm, fill=1, stroke=0)
    c.setStrokeColor(MIST); c.setLineWidth(0.7)
    c.roundRect(M, cy0, LW, CTA_H, 4*mm, fill=0, stroke=1)
    tx = M + 7*mm
    c.setFont(CGSB, 15); c.setFillColor(PLUM_DARK)
    c.drawString(tx, cy0 + CTA_H - 9.5*mm, content['cta_title'])
    btn = content['cta_btn']
    bw = c.stringWidth(btn, ISB, 8.5) + 12*mm; bh = 10*mm
    ly = cy0 + CTA_H - 15.5*mm
    for ln in wrap(c, content['cta_line1'] + ' ' + content['cta_line2'], IR, 8.6, LW - bw - 21*mm):
        c.setFont(IR, 8.6); c.setFillColor(TEXT)
        c.drawString(tx, ly, ln); ly -= 8.6 * 1.45
    eyebrow(c, tx, cy0 + 4.5*mm, content['cta_tags'], TERRA, 6.6)
    bx = M + LW - bw - 7*mm; by = cy0 + (CTA_H - bh) / 2
    c.setFillColor(TERRA)
    c.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    c.setFont(ISB, 8.5); c.setFillColor(IVORY2)
    c.drawCentredString(bx + bw / 2, by + bh / 2 - 1.1*mm, btn)
    c.linkURL(OFFER_URL, (M, cy0, M + LW, cy0 + CTA_H), thickness=0)
    assert y > cy0 + CTA_H + 4*mm, ('cover: titre trop long', lang, (y - cy0 - CTA_H) / mm)

    # Colonne droite : sommaire des 5 questions, cliquable
    top = H - 9*mm - LOGO_H - 9*mm
    c.setFillColor(IVORY2)
    c.roundRect(RX, BOT, RW, top - BOT, 4*mm, fill=1, stroke=0)
    c.setStrokeColor(MIST); c.setLineWidth(0.7)
    c.roundRect(RX, BOT, RW, top - BOT, 4*mm, fill=0, stroke=1)
    eyebrow(c, RX + 8*mm, top - 9*mm, content['index_label'], PLUM)
    qs = content['questions']
    zone_top = top - 15*mm
    step = (zone_top - BOT - 4*mm) / len(qs)
    TW = RW - 30*mm
    for i, q in enumerate(qs):
        ty = zone_top - i * step
        c.setFont(CGR, 26); c.setFillColor(TERRA)
        c.drawString(RX + 8*mm, ty - 9*mm, f'0{i+1}')
        lns = wrap(c, q['btn'], IM, 9.6, TW)
        ly = ty - 9*mm + (len(lns) - 1) * 9.6 * 1.4 / 2 + 1.2*mm
        for ln in lns:
            draw_hl(c, RX + 22*mm, ly, ln, IM, 9.6, PLUM); ly -= 9.6 * 1.4
        c.linkAbsolute('', f'question_{i+1}', (RX, ty - step, RX + RW, ty), thickness=0)

    footer_band(c, lang)
    c.showPage()


# ── PAGES INTÉRIEURES ─────────────────────────────────────────────────────────
def paragraphs(lines):
    out, cur = [], []
    for l in lines:
        if l: cur.append(l)
        elif cur: out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out

def inner(c, lang, qnum, q, pg):
    c.bookmarkPage(f'question_{qnum}')
    c.setFillColor(IVORY); c.rect(0, 0, W, H, fill=1, stroke=0)
    logo_tr(c)
    eyebrow(c, M, H - 15*mm, content_of[lang]['run_head'], PRUNE_LIGHT, 6.8)

    GUT = 16*mm
    LW  = 86*mm
    RX  = M + LW + GUT
    RW  = W - M - RX
    BOT = FOOT_H + 6*mm

    # Colonne gauche : grand numéro, catégorie, titre, niveau d'offre
    c.setFont(CGR, 112); c.setFillColor(TERRA)
    c.drawString(M - 2*mm, H - 62*mm, f'0{qnum}')
    y = H - 75*mm
    eyebrow(c, M, y, q['cat'], TERRA)
    y -= 11*mm
    for ln in wrap(c, q['title'], CGR, 26, LW):
        draw_hl(c, M, y, ln, CGR, 26, PLUM_DARK); y -= 26 * 1.14

    lvl, _, rest = q['offer_link'].partition(' · ')
    name, _, price = rest.partition(' · ')
    price = price.split(' › ')[0]
    oy = BOT + 13*mm
    thin_bar(c, M, oy + 4*mm, 15*mm)
    eyebrow(c, M + 5*mm, oy, f'{lvl} · {name}', TERRA, 6.8)
    c.setFont(IR, 8.6); c.setFillColor(PLUM)
    c.drawString(M + 5*mm, oy - 5.2*mm, price)
    c.setFont(ISB, 8); c.setFillColor(TERRA)
    c.drawString(M + 5*mm, oy - 10.2*mm, content_of[lang]['offer_cta'])
    c.linkURL(OFFER_URL, (M, oy - 12*mm, M + LW, oy + 5*mm), thickness=0)
    assert y > oy + 10*mm, ('inner: titre trop long', lang, qnum, (y - oy) / mm)

    # Colonne droite : idée clé, question de CODIR, conviction
    idea = paragraphs(q['idea'])
    top = H - 9*mm - LOGO_H - 9*mm
    GAP = 6*mm
    IW = RW - 16*mm

    def layout(k):
        f_l, f_i, f_q, f_c = 15 * k, 10.2 * k, 15.5 * k, 16.5 * k
        pad = 6.5*mm * k
        lead_h = text_h(c, idea[0], CGI, f_l, RW, f_l * 1.3)
        body_h = sum(text_h(c, t, IR, f_i, RW, f_i * 1.6) for t in idea[1:]) + 2.5*mm * max(0, len(idea) - 2)
        h1 = 9*mm + lead_h + (3*mm + body_h if len(idea) > 1 else 0)
        h2 = text_h(c, q['codir'], CGSB, f_q, IW, f_q * 1.3) + 9*mm + pad * 2
        h3 = sum(text_h(c, t, CGI, f_c, IW, f_c * 1.3) for t in q['conviction']) + 9*mm + pad * 2
        return f_l, f_i, f_q, f_c, pad, h1, h2, h3

    k = 1.15
    while True:
        f_l, f_i, f_q, f_c, pad, h1, h2, h3 = layout(k)
        if h1 + h2 + h3 + GAP * 2 <= top - BOT or k <= 0.78:
            break
        k -= 0.02
    spare = (top - BOT) - (h1 + h2 + h3 + GAP * 2)
    GAP += max(0, min(spare / 2, 6*mm))

    y = top
    eyebrow(c, RX, y - 4*mm, q['idea_label'], PLUM)
    iy = y - 12*mm
    for ln in wrap(c, idea[0], CGI, f_l, RW):
        draw_hl(c, RX, iy, ln, CGI, f_l, PLUM_DARK); iy -= f_l * 1.3
    iy -= 3*mm
    for t in idea[1:]:
        for ln in wrap(c, t, IR, f_i, RW):
            draw_hl(c, RX, iy, ln, IR, f_i, TEXT); iy -= f_i * 1.6
        iy -= 2.5*mm
    y -= h1 + GAP

    c.setFillColor(IVORY2)
    c.roundRect(RX, y - h2, RW, h2, 3.5*mm, fill=1, stroke=0)
    c.setStrokeColor(MIST); c.setLineWidth(0.6)
    c.roundRect(RX, y - h2, RW, h2, 3.5*mm, fill=0, stroke=1)
    thin_bar(c, RX + 0.8*mm, y - 4*mm, h2 - 8*mm, TERRA, 2)
    eyebrow(c, RX + 8*mm, y - pad - 2*mm, q['codir_label'], TERRA)
    qy = y - pad - 11*mm
    for ln in wrap(c, q['codir'], CGSB, f_q, IW):
        draw_hl(c, RX + 8*mm, qy, ln, CGSB, f_q, PLUM_DARK); qy -= f_q * 1.3
    y -= h2 + GAP

    c.setFillColor(PLUM)
    c.roundRect(RX, y - h3, RW, h3, 3.5*mm, fill=1, stroke=0)
    eyebrow(c, RX + 8*mm, y - pad - 2*mm, q['conviction_label'], MIST)
    cy = y - pad - 11.5*mm
    for t in q['conviction']:
        for ln in wrap(c, t, CGI, f_c, IW):
            draw_hl(c, RX + 8*mm, cy, ln, CGI, f_c, IVORY2); cy -= f_c * 1.3
    assert y - h3 >= BOT - 1, ('inner overflow', lang, qnum)

    footer_slim(c, lang, pg)
    c.showPage()


# ── PAGE FINALE ───────────────────────────────────────────────────────────────
def final(c, lang, content):
    c.setFillColor(PLUM_DARK); c.rect(0, 0, W, H, fill=1, stroke=0)
    logo_tr(c, on_dark=True)

    GUT = 14*mm
    LW  = CW * 0.52
    RX  = M + LW + GUT
    RW  = W - M - RX
    BOT = BAND_H + 10*mm

    # Colonne gauche : titre mémorable, encart, conviction
    y = H - 17*mm
    eyebrow(c, M, y, content['final_pretitle'], MIST, 6.8)
    y -= 17*mm
    for i, part in enumerate(content['final_title']):
        col = TERRA if i == 1 else IVORY2
        for ln in wrap(c, part, CGR, 27, LW):
            c.setFont(CGR, 27); c.setFillColor(col)
            c.drawString(M, y, ln); y -= 27 * 1.12
        y -= 2.5*mm
    y -= 5*mm

    body = content['final_body']
    BW = LW - 14*mm
    ih = sum(text_h(c, l, CGI, 12.5, BW, 12.5 * 1.35) for l in body) + 11*mm
    c.setFillColor(PLUM)
    c.roundRect(M, y - ih, LW, ih, 3.5*mm, fill=1, stroke=0)
    thin_bar(c, M + 0.8*mm, y - 3.5*mm, ih - 7*mm, TERRA, 2)
    iy = y - 8.5*mm
    for line in body:
        iy = draw_text(c, M + 8*mm, iy, line, CGI, 12.5, IVORY2, BW, 12.5 * 1.35)
    y -= ih + 8*mm
    for k, para in enumerate(paragraphs(content.get('final_body2', []))):
        col = IVORY2 if k == len(paragraphs(content['final_body2'])) - 1 else MIST
        for ln in wrap(c, para, IR, 9.8, LW):
            draw_hl(c, M, y, ln, IR, 9.8, col); y -= 9.8 * 1.55
        y -= 3*mm
    assert y > BOT - 4*mm, ('final: colonne gauche trop longue', lang, (y - BOT) / mm)

    # Colonne droite : les 5 domaines, puis la prise de rendez-vous
    y = H - 9*mm - LOGO_H - 9*mm
    eyebrow(c, RX, y, content['final_domains_label'], MIST, 6.8)
    y -= 5*mm
    ROW = 9.6*mm
    for i, d in enumerate(content['final_domains']):
        c.setFillColor(PLUM)
        c.roundRect(RX, y - ROW, RW, ROW, 2.5*mm, fill=1, stroke=0)
        c.setFont(CGR, 15); c.setFillColor(TERRA)
        c.drawString(RX + 5*mm, y - ROW / 2 - 1.8*mm, f'0{i+1}')
        draw_hl(c, RX + 16*mm, y - ROW / 2 - 1.3*mm, d, IM, 9.6, IVORY2)
        y -= ROW + 2.2*mm
    y -= 5*mm

    tl = wrap(c, content['final_cta_title'], CGSB, 16, RW - 14*mm)
    cta_h = len(tl) * 16 * 1.2 + 27*mm
    c.setFillColor(TERRA)
    c.roundRect(RX, y - cta_h, RW, cta_h, 4*mm, fill=1, stroke=0)
    ty = y - 10*mm
    c.setFont(CGSB, 16); c.setFillColor(IVORY2)
    for ln in tl:
        c.drawCentredString(RX + RW / 2, ty, ln); ty -= 16 * 1.2
    ty -= 1*mm
    c.setFont(IM, 8.4); c.setFillColor(IVORY2)
    c.drawCentredString(RX + RW / 2, ty, content['final_cta_sub'])
    ty -= 9*mm
    btn = content['cta_btn']
    bw = c.stringWidth(btn, ISB, 9) + 14*mm; bh = 9*mm
    bx = RX + (RW - bw) / 2
    c.setFillColor(IVORY2)
    c.roundRect(bx, ty - 2.6*mm, bw, bh, bh / 2, fill=1, stroke=0)
    c.setFont(ISB, 9); c.setFillColor(PLUM_DARK)
    c.drawCentredString(RX + RW / 2, ty + 0.4*mm, btn)
    c.linkURL(OFFER_URL, (RX, y - cta_h, RX + RW, y), thickness=0)
    y -= cta_h + 7*mm
    c.setFont(ISB, 8.4); c.setFillColor(IVORY2)
    c.drawCentredString(RX + RW / 2, y, content['final_signature'])
    y -= 5*mm
    c.setFont(IR, 8); c.setFillColor(MIST)
    c.drawCentredString(RX + RW / 2, y, MAIL + '  ·  exec-ia.ai')
    c.linkURL(SITE_URL, (RX, y - 2*mm, RX + RW, y + 4*mm), thickness=0)
    assert y > BAND_H + 3*mm, ('final: colonne droite trop longue', lang, (y - BAND_H) / mm)

    footer_band(c, lang)
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
                'La mayoría de las empresas detectan esta decisión varias semanas tarde,'
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



# ── Compléments de la refonte du 07/10/2026 ───────────────────────────────────
EXTRA = {
    'fr': {'cover_title_mc': ['5 questions qui valent', "plus qu'un nouveau projet IA"],
           'index_label': 'Les 5 questions', 'run_head': 'Les 5 Essentiels  ·  Q4 2026',
           'offer_cta': "Découvrir l'offre  ›", 'final_signature': "Valérie Mailland · Fondatrice · EXEC'IA Consulting"},
    'en': {'cover_title_mc': ['5 questions worth more', 'than a new AI project'],
           'index_label': 'The 5 questions', 'run_head': 'The 5 Essentials  ·  Q4 2026',
           'offer_cta': 'Discover the offer  ›', 'final_signature': "Valérie Mailland · Founder · EXEC'IA Consulting"},
    'es': {'cover_title_mc': ['5 preguntas que valen más', 'que un nuevo proyecto de IA'],
           'index_label': 'Las 5 preguntas', 'run_head': 'Los 5 Esenciales  ·  Q4 2026',
           'offer_cta': 'Descubrir la oferta  ›', 'final_signature': "Valérie Mailland · Fundadora · EXEC'IA Consulting"},
}
for _l, _d in EXTRA.items():
    CONTENT[_l].update(_d)
CONTENT['es']['questions'][2]['title'] = '¿Qué parte de su empresa se jubilaría mañana?'
content_of = CONTENT

OUTPUTS = {
    'fr': os.path.join(ASSETS, 'EXECIA_5 Essentiels_Q4_2026_FR.pdf'),
    'en': os.path.join(ASSETS, 'EXECIA_The 5 Essentials_Q4_2026_EN.pdf'),
    'es': os.path.join(ASSETS, 'EXECIA_Los 5 Esenciales_Q4_2026_ES.pdf'),
}

def generate(lang):
    content = CONTENT[lang]
    out = OUTPUTS[lang]
    c = pdfcanvas.Canvas(out, pagesize=landscape(A4), initialFontName=IR)
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

