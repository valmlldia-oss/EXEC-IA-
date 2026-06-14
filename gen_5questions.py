#!/usr/bin/env python3
"""EXEC'IA — 5 Questions · Lead Magnet Q4 2026 · FR / EN / ES"""

from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

W, H = A4

PLUM       = HexColor('#633B4A')
PLUM_DARK  = HexColor('#3D2030')
PLUM_MID   = HexColor('#7A4D5C')
TERRA      = HexColor('#C75F62')
TERRA_PALE = HexColor('#F2E8E4')
IVORY      = HexColor('#F6F1EB')
IVORY2     = HexColor('#FAF6F2')
TEXT       = HexColor('#2A1020')
GREY       = HexColor('#847680')
GREY_PALE  = HexColor('#D9C9C3')

M  = 18*mm
CW = W - 2*M

SITE_URL  = 'https://www.exec-ia.ai'
OFFER_URL = 'https://www.exec-ia.ai/#offres'
MAIL      = 'contact@exec-ia.ai'

BASE   = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, 'assets')
FONTS  = os.path.join(ASSETS, 'fonts_pdf')
LOGO   = os.path.join(ASSETS, 'EXECIA_CONSULTING_zoomé.png')
if not os.path.exists(LOGO):
    LOGO = os.path.join(ASSETS, "EXEC'IA CONSULTING new.png")


def reg():
    fmap = {'IR': 'Inter-Regular.ttf', 'IM': 'Inter-Medium.ttf',
            'ISB': 'Inter-SemiBold.ttf', 'IB': 'Inter-Bold.ttf'}
    r = {}
    for k, f in fmap.items():
        p = os.path.join(FONTS, f)
        if os.path.exists(p):
            try: pdfmetrics.registerFont(TTFont(k, p)); r[k] = True
            except: pass
    return r

_r = reg()
IR  = 'IR'  if 'IR'  in _r else 'Helvetica'
IM  = 'IM'  if 'IM'  in _r else 'Helvetica'
ISB = 'ISB' if 'ISB' in _r else 'Helvetica-Bold'
IB  = 'IB'  if 'IB'  in _r else 'Helvetica-Bold'


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

def put(c, x, y, txt, font, size, col, maxw, lead):
    c.setFont(font, size); c.setFillColor(col)
    for ln in wrap(c, txt, font, size, maxw):
        c.drawString(x, y, ln); y -= lead
    return y

def th(c, txt, font, size, maxw, lead):
    return len(wrap(c, txt, font, size, maxw)) * lead


def header(c, lang):
    BH = 16*mm
    c.setFillColor(PLUM_DARK)
    c.rect(0, H - BH, W, BH, fill=1, stroke=0)
    c.setStrokeColor(TERRA); c.setLineWidth(1)
    c.line(0, H - BH, W, H - BH)
    if os.path.exists(LOGO):
        c.drawImage(LOGO, M, H - BH + 2*mm,
                    width=40*mm, height=10*mm,
                    preserveAspectRatio=True, mask='auto')
    else:
        c.setFont(IB, 10); c.setFillColor(white)
        c.drawString(M, H - BH + 5*mm, "EXEC'IA CONSULTING")
    tag = 'Q4 2026'
    tw = c.stringWidth(tag, ISB, 7)
    c.setFillColor(TERRA)
    c.roundRect(W - M - tw - 5*mm, H - BH + 3.5*mm, tw + 5*mm, 7*mm, 2*mm, fill=1, stroke=0)
    c.setFont(ISB, 7); c.setFillColor(white)
    c.drawString(W - M - tw - 2.5*mm, H - BH + 6*mm, tag)
    c.linkURL(SITE_URL, (M, H - BH, M + 44*mm, H), thickness=0)


LANG_URLS = {
    'fr': 'https://www.exec-ia.ai',
    'en': 'https://www.exec-ia.ai/index-en.html',
    'es': 'https://www.exec-ia.ai/index-es.html',
}

def footer(c, lang, pg=None):
    FH = 18*mm
    c.setFillColor(PLUM_DARK)
    c.rect(0, 0, W, FH, fill=1, stroke=0)
    c.setStrokeColor(TERRA); c.setLineWidth(0.7)
    c.line(0, FH, W, FH)

    c.setFont(ISB, 7.5); c.setFillColor(white)
    c.drawString(M, FH - 5*mm, "Valerie Mailland . Fondatrice EXEC'IA Consulting")
    c.setFont(IR, 7); c.setFillColor(GREY_PALE)
    c.drawString(M, FH - 10.5*mm, f'{MAIL}  .  exec-ia.ai')
    c.linkURL(f'mailto:{MAIL}', (M, FH - 13*mm, M + 52*mm, FH - 6.5*mm), thickness=0)
    c.linkURL(LANG_URLS.get(lang, SITE_URL), (M + 54*mm, FH - 13*mm, M + 77*mm, FH - 6.5*mm), thickness=0)

    copy = u'© 2026 Valerie Mailland · EXEC’IA · Tous droits reserves'
    c.setFont(IR, 6); c.setFillColor(GREY_PALE)
    c.drawRightString(W - M, FH - 4.5*mm, copy)

    # Flags langues
    flags = [('FR', 'fr', LANG_URLS['fr']),
             ('EN', 'en', LANG_URLS['en']),
             ('ES', 'es', LANG_URLS['es'])]
    fx = W - M
    for code, lcode, url in reversed(flags):
        fw = c.stringWidth(code, ISB, 7) + 4*mm
        fx -= fw + 1.5*mm
        if lcode == lang:
            c.setFillColor(TERRA)
            c.roundRect(fx, FH - 13*mm, fw, 6*mm, 1.5*mm, fill=1, stroke=0)
            c.setFont(ISB, 7); c.setFillColor(white)
        else:
            c.setFont(ISB, 7); c.setFillColor(GREY)
        c.drawCentredString(fx + fw/2, FH - 10*mm, code)
        c.linkURL(url, (fx, FH - 13*mm, fx + fw, FH - 4*mm), thickness=0)

    if pg:
        c.setFont(IR, 6); c.setFillColor(GREY)
        c.drawRightString(W - M, FH - 12*mm, f'{pg} / 7')


def cover(c, lang, content):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, lang)

    y = H - 30*mm

    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, y, content['cover_pretitle'])
    y -= 11*mm

    for line in content['cover_title']:
        c.setFont(IB, 21); c.setFillColor(PLUM_DARK)
        c.drawString(M, y, line); y -= 11*mm
    y -= 2*mm

    c.setStrokeColor(TERRA); c.setLineWidth(2)
    c.line(M, y, M + 18*mm, y)
    y -= 8*mm

    c.setFont(IM, 10); c.setFillColor(TEXT)
    c.drawString(M, y, content['cover_subtitle'])
    y -= 6*mm
    c.setFont(IR, 8); c.setFillColor(GREY)
    c.drawString(M, y, content['cover_caption'])
    y -= 13*mm

    c.setFont(ISB, 7.5); c.setFillColor(PLUM)
    c.drawString(M, y, content['cover_toc_label'].upper())
    y -= 8*mm

    BH = 12*mm; GAP = 3*mm
    for i, q in enumerate(content['questions']):
        pg_name = f'q{i+1}_{lang}'
        c.setFillColor(IVORY2)
        c.roundRect(M, y - BH + 3*mm, CW, BH, 3*mm, fill=1, stroke=0)
        c.setFillColor(TERRA)
        c.rect(M, y - BH + 3*mm, 3.5*mm, BH, fill=1, stroke=0)
        c.setFont(IB, 8); c.setFillColor(white)
        c.drawString(M + 1*mm, y - 2.5*mm, f'0{i+1}')
        c.setFont(IM, 9); c.setFillColor(PLUM_DARK)
        c.drawString(M + 8.5*mm, y - 2.5*mm, q['title'])
        c.setFont(IR, 10); c.setFillColor(TERRA)
        c.drawRightString(W - M - 3*mm, y - 2.5*mm, u'>')
        c.linkURL(OFFER_URL,
                  (M, y - BH + 3*mm, W - M, y + 3*mm),
                  thickness=0)
        y -= BH + GAP

    y -= 5*mm

    box_h = 20*mm
    c.setFillColor(TERRA_PALE)
    c.roundRect(M, y - box_h, CW, box_h, 4*mm, fill=1, stroke=0)
    c.setStrokeColor(TERRA); c.setLineWidth(0.8)
    c.roundRect(M, y - box_h, CW, box_h, 4*mm, fill=0, stroke=1)
    c.setFont(ISB, 9); c.setFillColor(PLUM_DARK)
    c.drawString(M + 6*mm, y - 5*mm, content['cover_cta_title'])
    c.setFont(IR, 8); c.setFillColor(GREY)
    c.drawString(M + 6*mm, y - 11*mm, content['cover_cta_sub'])
    btn_w = 40*mm
    c.setFillColor(TERRA)
    c.roundRect(W - M - btn_w - 2*mm, y - box_h + 4*mm, btn_w, 10*mm, 5*mm, fill=1, stroke=0)
    c.setFont(ISB, 7.5); c.setFillColor(white)
    c.drawCentredString(W - M - btn_w/2 - 2*mm, y - box_h + 8*mm, content['cover_cta_btn'])
    c.linkURL(OFFER_URL, (M, y - box_h, W - M, y), thickness=0)

    footer(c, lang)
    c.showPage()


OFFER_LEVELS = [
    'https://www.exec-ia.ai/#offres',
    'https://www.exec-ia.ai/#offres',
    'https://www.exec-ia.ai/#offres',
    'https://www.exec-ia.ai/#offres',
    'https://www.exec-ia.ai/#offres',
]

def inner(c, lang, qnum, q, pg):
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, lang)

    y = H - 27*mm

    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, y, f'0{qnum}  .  {q["cat"].upper()}')
    y -= 10*mm

    y = put(c, M, y, q['title'], IB, 17, PLUM_DARK, CW, 10.5*mm)
    y -= 4*mm

    c.setStrokeColor(TERRA); c.setLineWidth(1.5)
    c.line(M, y, M + 14*mm, y)
    y -= 9*mm

    # Box 1 — IDEE CLE fond blanc, bord prune
    idea_lines = q['idea']
    box1_h = sum(
        th(c, l, IR, 10, CW - 11*mm, 6*mm) if l else 3.5*mm
        for l in idea_lines
    ) + 16*mm
    box1_y = y - box1_h + 5*mm
    c.setFillColor(white)
    c.roundRect(M, box1_y, CW, box1_h, 3.5*mm, fill=1, stroke=0)
    c.setFillColor(PLUM)
    c.rect(M, box1_y, 3.5*mm, box1_h, fill=1, stroke=0)
    c.setFont(ISB, 6.5); c.setFillColor(PLUM)
    c.drawString(M + 8*mm, y, q['idea_label'].upper())
    y -= 7*mm
    for line in idea_lines:
        if not line:
            y -= 3.5*mm
        else:
            y = put(c, M + 8*mm, y, line, IR, 10, TEXT, CW - 11*mm, 6*mm)
    y -= 9*mm

    # Box 2 — QUESTION CODIR fond terracotta pâle, bord terra
    codir_text = q['codir']
    box2_h = th(c, codir_text, IM, 10, CW - 11*mm, 6*mm) + 18*mm
    box2_y = y - box2_h + 5*mm
    c.setFillColor(TERRA_PALE)
    c.roundRect(M, box2_y, CW, box2_h, 3.5*mm, fill=1, stroke=0)
    c.setFillColor(TERRA)
    c.rect(M, box2_y, 3.5*mm, box2_h, fill=1, stroke=0)
    c.setFont(ISB, 6.5); c.setFillColor(TERRA)
    c.drawString(M + 8*mm, y, q['codir_label'].upper())
    y -= 7*mm
    y = put(c, M + 8*mm, y, codir_text, IM, 10, PLUM_DARK, CW - 11*mm, 6*mm)
    y -= 9*mm

    # Box 3 — CONVICTION fond prune, texte blanc
    conv_lines = q['conviction']
    box3_h = sum(th(c, l, IM, 10, CW - 11*mm, 6*mm) + 1.5*mm for l in conv_lines) + 18*mm
    box3_y = y - box3_h + 5*mm
    c.setFillColor(PLUM)
    c.roundRect(M, box3_y, CW, box3_h, 3.5*mm, fill=1, stroke=0)
    c.setFont(ISB, 6.5); c.setFillColor(TERRA)
    c.drawString(M + 8*mm, y, q['conviction_label'].upper())
    y -= 7*mm
    for line in conv_lines:
        y = put(c, M + 8*mm, y, line, IM, 10, white, CW - 11*mm, 6*mm)
        y -= 1.5*mm
    y -= 8*mm

    # Lien offre cliquable bas de page
    offer_y = max(y, 28*mm)
    offer_text = q.get('offer_link', f'exec-ia.ai')
    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, offer_y, offer_text)
    c.linkURL(OFFER_LEVELS[qnum - 1], (M, offer_y - 2*mm, W - M, offer_y + 7*mm), thickness=0)

    footer(c, lang, pg)
    c.showPage()


def final(c, lang, content):
    c.setFillColor(PLUM_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, lang)

    y = H - 30*mm

    c.setFont(ISB, 7.5); c.setFillColor(TERRA)
    c.drawString(M, y, content['final_pretitle'])
    y -= 12*mm

    for line in content['final_title']:
        c.setFont(IB, 19); c.setFillColor(white)
        c.drawString(M, y, line); y -= 10*mm
    y -= 3*mm

    c.setStrokeColor(TERRA); c.setLineWidth(1.5)
    c.line(M, y, M + 16*mm, y)
    y -= 9*mm

    lines = content['final_body']
    bh = len(lines) * 7*mm + 10*mm
    c.setFillColor(IVORY2)
    c.roundRect(M, y - bh + 3*mm, CW, bh, 4*mm, fill=1, stroke=0)
    y -= 3*mm
    for line in lines:
        c.setFont(IR, 10); c.setFillColor(TEXT)
        c.drawString(M + 6*mm, y, line); y -= 7*mm
    y -= 10*mm

    c.setFont(ISB, 7); c.setFillColor(TERRA)
    c.drawString(M, y, content['final_domains_label'].upper())
    y -= 9*mm

    for i, d in enumerate(content['final_domains']):
        bg = PLUM_MID if i % 2 == 0 else HexColor('#6E4454')
        c.setFillColor(bg)
        c.roundRect(M, y - 8.5*mm, CW, 9*mm, 2.5*mm, fill=1, stroke=0)
        c.setFont(IB, 7.5); c.setFillColor(TERRA)
        c.drawString(M + 4*mm, y - 3.5*mm, f'0{i+1}')
        c.setFont(IM, 9); c.setFillColor(white)
        c.drawString(M + 11*mm, y - 3.5*mm, d)
        y -= 10.5*mm

    y -= 7*mm

    cta_h = 24*mm
    c.setFillColor(TERRA)
    c.roundRect(M, y - cta_h, CW, cta_h, 5*mm, fill=1, stroke=0)
    c.setFont(IB, 10.5); c.setFillColor(white)
    c.drawCentredString(W/2, y - 8*mm, content['final_cta_title'])
    c.setFont(IR, 8.5); c.setFillColor(IVORY)
    c.drawCentredString(W/2, y - 15*mm, content['final_cta_sub'])
    c.linkURL(OFFER_URL, (M, y - cta_h, W - M, y), thickness=0)
    y -= cta_h + 8*mm

    c.setFont(ISB, 8); c.setFillColor(white)
    c.drawCentredString(W/2, y, "Valerie Mailland . Fondatrice . EXEC'IA Consulting")
    y -= 5.5*mm
    c.setFont(IR, 7.5); c.setFillColor(GREY_PALE)
    c.drawCentredString(W/2, y, f'{SITE_URL}')
    c.linkURL(SITE_URL, (W/2 - 30*mm, y - 2*mm, W/2 + 30*mm, y + 7*mm), thickness=0)

    footer(c, lang)
    c.showPage()


CONTENT = {
'fr': {
    'cover_pretitle': 'Q4 2026  .  DIRECTION GENERALE  .  INTELLIGENCE ARTIFICIELLE',
    'cover_title': ['5 QUESTIONS QUI VALENT', "PLUS QU'UN NOUVEAU PROJET IA"],
    'cover_subtitle': 'La plupart des entreprises cherchent de nouvelles solutions.',
    'cover_caption': 'Les meilleures commencent par se poser les bonnes questions. 5 min de lecture.',
    'cover_toc_label': 'Cliquez sur la question qui vous concerne',
    'cover_cta_title': 'Entretien preliminaire offert',
    'cover_cta_sub': '30 minutes . Sans engagement . Confidentiel',
    'cover_cta_btn': 'Prendre rendez-vous',
    'questions': [
        {
            'title': 'Combien coute une decision reportee pendant 90 jours ?',
            'cat': 'Decision',
            'idea_label': 'Idee cle',
            'idea': [
                'Les dirigeants craignent les mauvaises decisions.',
                '',
                'Ils devraient davantage craindre les decisions qui n\'arrivent jamais.',
                'Chaque arbitrage repousse immobilise des ressources, ralentit les',
                'equipes et cree un cout invisible jusqu\'au jour ou il devient strategique.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quelle decision importante est discutee depuis plus de trois mois sans avoir ete prise ?',
            'conviction_label': "Conviction EXEC'IA",
            'conviction': [
                'Une decision imparfaite cree du mouvement.',
                'Une decision absente cree de l\'immobilisme.',
            ],
            'offer_link': '> NIVEAU I . CLARIFIEZ -- Seance de cadrage 490 E  .  exec-ia.ai',
        },
        {
            'title': '20 % du temps de vos managers cree-t-il reellement de la valeur ?',
            'cat': 'Productivite',
            'idea_label': 'Idee cle',
            'idea': [
                'Vos collaborateurs les plus experimentes sont absorbes par',
                'des reunions, des reportings et des recherches d\'information.',
                '',
                'Le sujet n\'est pas le temps perdu.',
                'Le sujet est la valeur qui n\'est jamais creee.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Si vous rendiez une journee par semaine a vos meilleurs managers, ou investiriez-vous ce temps ?',
            'conviction_label': "Conviction EXEC'IA",
            'conviction': [
                'Le gain de productivite n\'a aucune valeur',
                'tant qu\'il n\'est pas transforme en meilleure decision.',
            ],
            'offer_link': '> NIVEAU II . COMPRENEZ & EMBARQUEZ -- Leadership & Decision IA  .  exec-ia.ai',
        },
        {
            'title': 'Quelle partie de votre entreprise partirait a la retraite demain ?',
            'cat': 'Transmission',
            'idea_label': 'Idee cle',
            'idea': [
                'Les connaissances les plus strategiques ne figurent dans aucun document.',
                'Elles vivent dans la tete de quelques personnes cles.',
                '',
                'Quand elles partent, elles emportent les raccourcis, les arbitrages',
                'et la capacite de decider avec justesse.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Si trois personnes quittaient l\'entreprise demain, quelles decisions deviendraient impossibles ?',
            'conviction_label': "Conviction EXEC'IA",
            'conviction': [
                'La transmission n\'est pas un sujet RH.',
                'C\'est un sujet de continuite strategique.',
            ],
            'offer_link': '> NIVEAU III . DECIDEZ DANS LA DUREE -- Advisory de Direction  .  exec-ia.ai',
        },
        {
            'title': 'A quel moment precis vos clients commencent-ils a decrocher ?',
            'cat': 'Experience client',
            'idea_label': 'Idee cle',
            'idea': [
                'Les clients ne partent presque jamais brutalement.',
                'Ils accumulent des micro-deceptions, puis prennent une decision silencieuse.',
                '',
                'La plupart des entreprises detectent cette decision plusieurs semaines trop tard.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quels sont les trois moments ou un client decide de rester ou de partir ?',
            'conviction_label': "Conviction EXEC'IA",
            'conviction': [
                'Ce qui n\'est pas observe ne peut pas etre ameliore.',
            ],
            'offer_link': '> NIVEAU III . DECIDEZ DANS LA DUREE -- Advisory de Direction  .  exec-ia.ai',
        },
        {
            'title': 'Qui prend reellement les decisions dans votre organisation ?',
            'cat': 'Gouvernance',
            'idea_label': 'Idee cle',
            'idea': [
                'Certaines decisions sont prises par des outils.',
                'D\'autres par des habitudes. D\'autres encore par des experts',
                'que personne ne remet en question.',
                '',
                'Le sujet n\'est pas l\'IA. Le sujet est le controle.',
            ],
            'codir_label': 'Question de CODIR',
            'codir': 'Quelles decisions critiques ne devraient jamais etre deleguees ?',
            'conviction_label': "Conviction EXEC'IA",
            'conviction': [
                'Une organisation est gouvernee',
                'lorsqu\'elle sait pourquoi elle decide.',
            ],
            'offer_link': '> NIVEAU IV . TRANSFORMEZ -- Mission de Transformation  .  exec-ia.ai',
        },
    ],
    'final_pretitle': "L'APPROCHE EXEC'IA",
    'final_title': ['Decider avec clarte.', 'Dans un monde ou l\'IA redessine les regles.'],
    'final_body': [
        'Les entreprises ne manquent pas d\'outils.',
        'Elles manquent souvent de clarte sur ce qui merite',
        'reellement l\'attention de leur Direction Generale.',
    ],
    'final_domains_label': "EXEC'IA accompagne les dirigeants dans cinq domaines",
    'final_domains': [
        'Priorisation des investissements IA',
        'Productivite manageriale',
        'Transmission des savoirs critiques',
        'Experience client',
        'Gouvernance de l\'IA',
    ],
    'final_cta_title': '30 MINUTES . CONFIDENTIEL . SANS ENGAGEMENT',
    'final_cta_sub': 'Entretien preliminaire offert . contact@exec-ia.ai',
},
'en': {
    'cover_pretitle': 'Q4 2026  .  EXECUTIVE LEADERSHIP  .  ARTIFICIAL INTELLIGENCE',
    'cover_title': ['5 QUESTIONS WORTH MORE', 'THAN A NEW AI PROJECT'],
    'cover_subtitle': 'Most companies look for new solutions.',
    'cover_caption': 'The best ones start by asking the right questions. 5 min read.',
    'cover_toc_label': 'Click on the question that concerns you',
    'cover_cta_title': 'Preliminary interview - complimentary',
    'cover_cta_sub': '30 minutes . No commitment . Confidential',
    'cover_cta_btn': 'Book a call',
    'questions': [
        {
            'title': 'How much does a decision deferred for 90 days actually cost?',
            'cat': 'Decision',
            'idea_label': 'Key insight',
            'idea': [
                'Leaders fear making bad decisions.',
                '',
                'They should fear even more the decisions that never get made.',
                'Every postponed choice freezes resources, slows teams down',
                'and creates an invisible cost until it becomes strategic.',
            ],
            'codir_label': 'Board question',
            'codir': 'What important decision has been discussed for more than three months without being made?',
            'conviction_label': "EXEC'IA conviction",
            'conviction': [
                'An imperfect decision creates momentum.',
                'An absent decision creates stagnation.',
            ],
            'offer_link': '> LEVEL I . CLARIFY -- Strategic Framing Session 490 E  .  exec-ia.ai',
        },
        {
            'title': 'Do 20% of your managers\' time truly create value?',
            'cat': 'Productivity',
            'idea_label': 'Key insight',
            'idea': [
                'Your most experienced people are absorbed by meetings,',
                'reporting, validations and information searches.',
                '',
                'The issue is not wasted time.',
                'The issue is value that is never created.',
            ],
            'codir_label': 'Board question',
            'codir': 'If you gave your best managers one extra day per week, where would you invest that time?',
            'conviction_label': "EXEC'IA conviction",
            'conviction': [
                'Productivity gains have no value',
                'until transformed into better decisions.',
            ],
            'offer_link': '> LEVEL II . UNDERSTAND & ALIGN -- AI Leadership & Decision  .  exec-ia.ai',
        },
        {
            'title': 'What part of your company would retire tomorrow?',
            'cat': 'Knowledge transfer',
            'idea_label': 'Key insight',
            'idea': [
                'The most strategic knowledge lives in no document.',
                'It lives in the heads of a few key people.',
                '',
                'When they leave, they take the shortcuts, the judgment calls',
                'and the ability to decide with accuracy.',
            ],
            'codir_label': 'Board question',
            'codir': 'If three people left tomorrow, which decisions would become impossible to make?',
            'conviction_label': "EXEC'IA conviction",
            'conviction': [
                'Knowledge transfer is not an HR matter.',
                'It is a strategic continuity matter.',
            ],
            'offer_link': '> LEVEL III . DECIDE OVER TIME -- Executive Advisory  .  exec-ia.ai',
        },
        {
            'title': 'At what exact moment do your clients start disengaging?',
            'cat': 'Customer experience',
            'idea_label': 'Key insight',
            'idea': [
                'Clients almost never leave abruptly.',
                'They accumulate micro-disappointments then make a silent decision.',
                '',
                'Most companies detect this decision several weeks too late.',
            ],
            'codir_label': 'Board question',
            'codir': 'What are the three moments where a client decides to stay or to leave?',
            'conviction_label': "EXEC'IA conviction",
            'conviction': [
                'What is not observed cannot be improved.',
            ],
            'offer_link': '> LEVEL III . DECIDE OVER TIME -- Executive Advisory  .  exec-ia.ai',
        },
        {
            'title': 'Who is really making the decisions in your organisation?',
            'cat': 'Governance',
            'idea_label': 'Key insight',
            'idea': [
                'Some decisions are made by tools.',
                'Others by habits. Others still by experts no one ever questions.',
                '',
                'The issue is not AI. The issue is control.',
            ],
            'codir_label': 'Board question',
            'codir': 'Which critical decisions should never be delegated?',
            'conviction_label': "EXEC'IA conviction",
            'conviction': [
                'An organisation is well governed',
                'when it knows why it decides.',
            ],
            'offer_link': '> LEVEL IV . TRANSFORM -- Transformation Mission  .  exec-ia.ai',
        },
    ],
    'final_pretitle': "THE EXEC'IA APPROACH",
    'final_title': ['Decide with clarity.', 'In a world where AI rewrites the rules.'],
    'final_body': [
        'Companies don\'t lack tools.',
        'They often lack clarity on what truly deserves',
        'the attention of their Executive Committee.',
    ],
    'final_domains_label': "EXEC'IA supports executives across five domains",
    'final_domains': [
        'AI investment prioritisation',
        'Managerial productivity',
        'Critical knowledge transfer',
        'Customer experience',
        'AI governance',
    ],
    'final_cta_title': '30 MINUTES . CONFIDENTIAL . NO COMMITMENT',
    'final_cta_sub': 'Complimentary interview . contact@exec-ia.ai',
},
'es': {
    'cover_pretitle': 'Q4 2026  .  DIRECCION GENERAL  .  INTELIGENCIA ARTIFICIAL',
    'cover_title': ['5 PREGUNTAS QUE VALEN MAS', 'QUE UN NUEVO PROYECTO DE IA'],
    'cover_subtitle': 'La mayoria de las empresas buscan nuevas soluciones.',
    'cover_caption': 'Las mejores empiezan por hacerse las preguntas correctas. 5 min de lectura.',
    'cover_toc_label': 'Haga clic en la pregunta que le concierne',
    'cover_cta_title': 'Entrevista preliminar - gratuita',
    'cover_cta_sub': '30 minutos . Sin compromiso . Confidencial',
    'cover_cta_btn': 'Reservar una cita',
    'questions': [
        {
            'title': 'Cuanto cuesta una decision aplazada durante 90 dias?',
            'cat': 'Decision',
            'idea_label': 'Idea clave',
            'idea': [
                'Los directivos temen tomar malas decisiones.',
                '',
                'Deberian temer aun mas las decisiones que nunca se toman.',
                'Cada arbitraje aplazado inmoviliza recursos, ralentiza equipos',
                'y crea un coste invisible hasta que se vuelve estrategico.',
            ],
            'codir_label': 'Pregunta de Comite de Direccion',
            'codir': 'Que decision importante lleva mas de tres meses debatiendose sin haberse tomado?',
            'conviction_label': "Conviccion EXEC'IA",
            'conviction': [
                'Una decision imperfecta crea movimiento.',
                'Una decision ausente crea inmovilismo.',
            ],
            'offer_link': '> NIVEL I . CLARIFICAR -- Sesion de encuadre 490 E  .  exec-ia.ai',
        },
        {
            'title': 'El 20 % del tiempo de sus managers crea realmente valor?',
            'cat': 'Productividad',
            'idea_label': 'Idea clave',
            'idea': [
                'Sus colaboradores mas experimentados estan absorbidos por',
                'reuniones, informes y busquedas de informacion.',
                '',
                'El problema no es el tiempo perdido.',
                'El problema es el valor que nunca se crea.',
            ],
            'codir_label': 'Pregunta de Comite de Direccion',
            'codir': 'Si diera un dia extra a la semana a sus mejores managers, donde invertiria ese tiempo?',
            'conviction_label': "Conviccion EXEC'IA",
            'conviction': [
                'La ganancia de productividad no tiene valor',
                'hasta que se transforma en una mejor decision.',
            ],
            'offer_link': '> NIVEL II . COMPRENDA & ALINEE -- Liderazgo & Decision IA  .  exec-ia.ai',
        },
        {
            'title': 'Que parte de su empresa se jubilaria manana?',
            'cat': 'Transmision del conocimiento',
            'idea_label': 'Idea clave',
            'idea': [
                'El conocimiento mas estrategico no figura en ningun documento.',
                'Vive en la mente de unas pocas personas clave.',
                '',
                'Cuando se van, se llevan los atajos, los criterios',
                'y la capacidad de decidir con acierto.',
            ],
            'codir_label': 'Pregunta de Comite de Direccion',
            'codir': 'Si tres personas se marcharan manana, que decisiones serian imposibles de tomar?',
            'conviction_label': "Conviccion EXEC'IA",
            'conviction': [
                'La transmision del conocimiento no es un asunto de RRHH.',
                'Es un asunto de continuidad estrategica.',
            ],
            'offer_link': '> NIVEL III . DECIDIR EN EL TIEMPO -- Advisory de Direccion  .  exec-ia.ai',
        },
        {
            'title': 'En que momento exacto sus clientes empiezan a desconectarse?',
            'cat': 'Experiencia del cliente',
            'idea_label': 'Idea clave',
            'idea': [
                'Los clientes casi nunca se van de golpe.',
                'Acumulan micro-decepciones y luego toman una decision silenciosa.',
                '',
                'La mayoria de las empresas detectan esta decision',
                'varias semanas demasiado tarde.',
            ],
            'codir_label': 'Pregunta de Comite de Direccion',
            'codir': 'Cuales son los tres momentos en los que un cliente decide quedarse o marcharse?',
            'conviction_label': "Conviccion EXEC'IA",
            'conviction': [
                'Lo que no se observa no puede mejorarse.',
            ],
            'offer_link': '> NIVEL III . DECIDIR EN EL TIEMPO -- Advisory de Direccion  .  exec-ia.ai',
        },
        {
            'title': 'Quien toma realmente las decisiones en su organizacion?',
            'cat': 'Gobernanza',
            'idea_label': 'Idea clave',
            'idea': [
                'Algunas decisiones las toman las herramientas.',
                'Otras los habitos. Otras mas, expertos que nadie cuestiona.',
                '',
                'El problema no es la IA. El problema es el control.',
            ],
            'codir_label': 'Pregunta de Comite de Direccion',
            'codir': 'Que decisiones criticas nunca deberian delegarse?',
            'conviction_label': "Conviccion EXEC'IA",
            'conviction': [
                'Una organizacion esta bien gobernada',
                'cuando sabe por que decide.',
            ],
            'offer_link': '> NIVEL IV . TRANSFORMAR -- Mision de Transformacion  .  exec-ia.ai',
        },
    ],
    'final_pretitle': "EL ENFOQUE EXEC'IA",
    'final_title': ['Decidir con claridad.', 'En un mundo donde la IA redefine las reglas.'],
    'final_body': [
        'Las empresas no carecen de herramientas.',
        'A menudo carecen de claridad sobre que merece',
        'realmente la atencion de su Direccion General.',
    ],
    'final_domains_label': "EXEC'IA acompana a los directivos en cinco ambitos",
    'final_domains': [
        'Priorizacion de inversiones en IA',
        'Productividad directiva',
        'Transmision del conocimiento critico',
        'Experiencia del cliente',
        'Gobernanza de la IA',
    ],
    'final_cta_title': '30 MINUTOS . CONFIDENCIAL . SIN COMPROMISO',
    'final_cta_sub': 'Entrevista preliminar gratuita . contact@exec-ia.ai',
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
    c.setAuthor("Valerie Mailland . Fondatrice . EXEC'IA Consulting")
    c.setSubject(f'Lead Magnet Q4 2026 . {lang.upper()}')
    cover(c, lang, content)
    for i, q in enumerate(content['questions']):
        inner(c, lang, i + 1, q, i + 2)
    final(c, lang, content)
    c.save()
    print(f'[{lang.upper()}] {out}')

if __name__ == '__main__':
    for lang in ['fr', 'en', 'es']:
        generate(lang)
    print('Done.')
