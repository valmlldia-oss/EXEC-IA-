#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (Paragraph, Spacer, PageBreak, HRFlowable,
                                 NextPageTemplate, KeepTogether)
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate, Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

BASE   = os.path.dirname(__file__)
FD     = os.path.join(BASE, 'assets/fonts_pdf')
ASSETS = os.path.join(BASE, 'assets')
LOGO   = os.path.join(ASSETS, 'EXECIA_CONSULTING_zoomé.png')

for name, file in [
    ('CG',    'CormorantGaramond-Regular.ttf'),
    ('CG-B',  'CormorantGaramond-Bold.ttf'),
    ('CG-SB', 'CormorantGaramond-SemiBold.ttf'),
    ('CG-I',  'CormorantGaramond-Italic.ttf'),
    ('RL',    'Raleway-Regular.ttf'),
    ('RL-B',  'Raleway-Bold.ttf'),
    ('RL-SB', 'Raleway-SemiBold.ttf'),
    ('RL-I',  'Raleway-Italic.ttf'),
]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FD, file)))

TERRACOTTA  = colors.HexColor('#C75F62')
PRUNE       = colors.HexColor('#633B4A')
IVOIRE      = colors.HexColor('#F6F1EB')
TAUPE       = colors.HexColor('#847680')
IVOIRE_DARK = colors.HexColor('#E5D9D0')
TC_PALE     = colors.HexColor('#DDB0B2')
IVOIRE_MID  = colors.HexColor('#EDE4DC')
PRUNE_LIGHT = colors.HexColor('#8A5A68')

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 30*mm, 30*mm, 24*mm, 24*mm
CW     = PAGE_W - ML - MR
BAND_H = 175
OUTPUT = os.path.join(ASSETS, 'EXECIA_5_Priorites_IA_Dirigeants.pdf')

EXECIA = "EXEC’IA"


# ── Encadre bordure gauche ─────────────────────────────────────────────────────
class LBB(Flowable):
    def __init__(self, paragraphs, bg=IVOIRE_DARK, border=TERRACOTTA, bw=3.5, ph=12, pv=10):
        super().__init__()
        self.paragraphs = paragraphs
        self.bg = bg; self.border = border
        self.bw = bw; self.ph = ph; self.pv = pv
        self._w = CW; self._h = None

    def wrap(self, aw, ah):
        self._w = aw
        iw = self._w - self.bw - self.ph * 2
        h = self.pv
        for p in self.paragraphs:
            _, ph = p.wrap(iw, ah); h += ph + 3
        self._h = h + self.pv
        return self._w, self._h

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg); c.rect(0, 0, self._w, self._h, fill=1, stroke=0)
        c.setFillColor(self.border); c.rect(0, 0, self.bw, self._h, fill=1, stroke=0)
        iw = self._w - self.bw - self.ph * 2
        x = self.bw + self.ph; y = self._h - self.pv
        for p in self.paragraphs:
            _, ph = p.wrap(iw, self._h); y -= ph; p.drawOn(c, x, y); y -= 3


# ── CTA card (style site) ──────────────────────────────────────────────────────
class CTACard(Flowable):
    def __init__(self, s):
        super().__init__()
        self.s = s

    def _make_paras(self):
        st_title = ParagraphStyle('cct', fontName='CG-SB', fontSize=16, textColor=IVOIRE, leading=22)
        st_desc  = ParagraphStyle('ccd', fontName='RL',    fontSize=9,  textColor=colors.HexColor('#C4A8AC'), leading=13)
        st_tags  = ParagraphStyle('cctg', fontName='RL-SB', fontSize=8, textColor=TERRACOTTA, leading=12)
        self._title = Paragraph("Entretien préliminaire — offert", st_title)
        self._desc  = Paragraph("30 minutes pour comprendre votre situation et évaluer ensemble "
                                "comment " + EXECIA + " peut vous être utile.", st_desc)
        self._tags  = Paragraph("Sans engagement  ·  Confidentiel", st_tags)

    def wrap(self, aw, ah):
        self._w = aw
        BW = 108
        TW = aw - BW - 44
        self._make_paras()
        _, th = self._title.wrap(TW, ah)
        _, dh = self._desc.wrap(TW, ah)
        _, tgh = self._tags.wrap(TW, ah)
        self._h = max(64, th + dh + tgh + 30)
        self._TW = TW
        return self._w, self._h

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor('#7A4F62'))
        c.roundRect(0, 0, self._w, self._h, 5, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor('#9E7080'))
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self._w, self._h, 5, fill=0, stroke=1)
        BW, BH = 108, 28
        bx = self._w - BW - 14
        by = (self._h - BH) / 2
        c.setFillColor(PRUNE_LIGHT)
        c.roundRect(bx, by, BW, BH, 14, fill=1, stroke=0)
        c.setFont('RL-SB', 8.5)
        c.setFillColor(IVOIRE)
        c.drawCentredString(bx + BW / 2, by + 9, "Prendre rendez-vous")
        lm = 16
        TW = self._TW
        y = self._h - 12
        _, th = self._title.wrap(TW, self._h); y -= th
        self._title.drawOn(c, lm, y); y -= 5
        _, dh = self._desc.wrap(TW, self._h); y -= dh
        self._desc.drawOn(c, lm, y); y -= 5
        _, tgh = self._tags.wrap(TW, self._h); y -= tgh
        self._tags.drawOn(c, lm, y)


# ── Styles ─────────────────────────────────────────────────────────────────────
def S():
    s = {}
    s['section_num']   = ParagraphStyle('sn',  fontName='CG-B',  fontSize=52,   textColor=TC_PALE,    leading=62,  spaceAfter=0)
    s['section_title'] = ParagraphStyle('st',  fontName='CG-SB', fontSize=21,   textColor=PRUNE,      leading=29,  spaceAfter=0)
    s['domain']        = ParagraphStyle('dm',  fontName='RL-SB', fontSize=8.1,  textColor=TERRACOTTA, leading=11,  letterSpacing=2.5, spaceAfter=0)
    s['rubric']        = ParagraphStyle('rb',  fontName='RL-SB', fontSize=8.3,  textColor=TAUPE,      leading=12,  letterSpacing=2,   spaceAfter=2)
    s['body']          = ParagraphStyle('bd',  fontName='RL',    fontSize=9.5,  textColor=TAUPE,      leading=16)
    s['question']      = ParagraphStyle('qu',  fontName='RL-I',  fontSize=9.5,  textColor=PRUNE,      leading=16,  spaceAfter=4, leftIndent=5)
    s['vigil_label']   = ParagraphStyle('vl',  fontName='RL-SB', fontSize=8.3,  textColor=TERRACOTTA, leading=12,  letterSpacing=1.8)
    s['vigil_body']    = ParagraphStyle('vb',  fontName='RL',    fontSize=9,    textColor=TAUPE,      leading=14)
    s['asterism']      = ParagraphStyle('ast', fontName='CG',    fontSize=22,   textColor=TC_PALE,    alignment=1, leading=30)
    s['synth_rubric']  = ParagraphStyle('syr', fontName='RL-SB', fontSize=8.5,  textColor=colors.HexColor('#C4A8AC'), leading=12, letterSpacing=2)
    s['body_dark']     = ParagraphStyle('bdk', fontName='RL',    fontSize=10.5, textColor=IVOIRE,     leading=18,  spaceAfter=4)
    s['body_dark_sm']  = ParagraphStyle('bds', fontName='RL',    fontSize=9,    textColor=colors.HexColor('#C4A8AC'), leading=14, spaceAfter=3)
    s['cta_title']     = ParagraphStyle('ct',  fontName='CG-SB', fontSize=17,   textColor=IVOIRE,     leading=24,  spaceAfter=2)
    s['cta_email']     = ParagraphStyle('ce',  fontName='RL-B',  fontSize=11,   textColor=TERRACOTTA, leading=16)
    s['footer_dark']   = ParagraphStyle('fd',  fontName='RL',    fontSize=7.5,  textColor=colors.HexColor('#9E8080'), leading=10)
    s['offer_niveau']  = ParagraphStyle('on',  fontName='RL',    fontSize=6.5,  textColor=PRUNE_LIGHT, leading=10, letterSpacing=1.5)
    s['offer_dark']    = ParagraphStyle('od',  fontName='RL-SB', fontSize=9.5,  textColor=TC_PALE,    leading=14,  letterSpacing=0.5)
    s['level_label']   = ParagraphStyle('ll',  fontName='RL-SB', fontSize=8.5,  textColor=TERRACOTTA, leading=12,  letterSpacing=1)
    s['level_body']    = ParagraphStyle('lb',  fontName='RL',    fontSize=9,    textColor=colors.HexColor('#C4A8AC'), leading=14)
    s['dark_title']    = ParagraphStyle('dt',  fontName='CG-B',  fontSize=18,   textColor=IVOIRE,     leading=26)
    s['dark_title_tc'] = ParagraphStyle('dtc', fontName='CG-B',  fontSize=18,   textColor=TERRACOTTA, leading=26,  spaceAfter=2)
    s['ce_what']       = ParagraphStyle('cew', fontName='RL-SB', fontSize=8,    textColor=TERRACOTTA, leading=12,  letterSpacing=2)
    return s


# ── Backgrounds ────────────────────────────────────────────────────────────────
def bg_cover(canvas, doc):
    canvas.saveState()
    cx = PAGE_W / 2
    canvas.setFillColor(IVOIRE); canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(PRUNE);  canvas.rect(0, 0, PAGE_W, BAND_H, fill=1, stroke=0)
    canvas.setFillColor(TERRACOTTA); canvas.rect(0, BAND_H, PAGE_W, 1.2, fill=1, stroke=0)
    logo_w = CW * 0.72; logo_h = logo_w * (438 / 1526)
    logo_x = cx - logo_w / 2; logo_y = PAGE_H - MT - logo_h - 10
    canvas.drawImage(LOGO, logo_x, logo_y, width=logo_w, height=logo_h, mask='auto')
    sep_y = logo_y - 18
    canvas.setStrokeColor(TERRACOTTA); canvas.setLineWidth(0.7)
    canvas.line(cx - CW * 0.22, sep_y, cx + CW * 0.22, sep_y)
    canvas.setFont('CG-B', 21); canvas.setFillColor(PRUNE)
    canvas.drawCentredString(cx, sep_y - 38, "L'IA N'A PAS PRIS LE POUVOIR.")
    canvas.setFont('CG-B', 21); canvas.setFillColor(TERRACOTTA)
    canvas.drawCentredString(cx, sep_y - 64, "ELLE A OCCUPÉ LE VIDE.")
    canvas.setFont('CG-I', 12); canvas.setFillColor(TAUPE)
    canvas.drawCentredString(cx, sep_y - 90,
        "Cinq décisions que personne ne prendra à votre place.")
    canvas.setFont('CG-SB', 14); canvas.setFillColor(TERRACOTTA)
    canvas.drawCentredString(cx, sep_y - 114,
        "1  M I N U T E  P A R  D É C I S I O N")
    items = [
        ("01", "Vous savez que certains projets ne valent rien. Vous les financez encore."),
        ("02", "Vos meilleurs cadres font ce que l'IA pourrait faire. Et vous le savez."),
        ("03", "Un expert va partir. Vous n'avez pas décidé quoi faire avant."),
        ("04", "Votre client a décidé de partir avant votre prochain CODIR."),
        ("05", "Vos outils IA ont plus de pouvoir sur vos processus que vous."),
    ]
    y_band = BAND_H - 24
    for num, text in items:
        canvas.setFont('CG-SB', 8); canvas.setFillColor(TERRACOTTA)
        canvas.drawString(ML, y_band, num)
        canvas.setFont('RL', 7.5); canvas.setFillColor(IVOIRE)
        canvas.drawString(ML + 20, y_band, text)
        y_band -= 16
    canvas.setFont('RL', 7); canvas.setFillColor(colors.HexColor('#9E8080'))
    canvas.drawCentredString(cx, 14,
        "contact@exec-ia.ai  ·  © 2026 EXEC’IA Consulting  ·  Tous droits réservés")
    canvas.restoreState()


def bg_interior(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(IVOIRE); canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(TERRACOTTA); canvas.rect(13 * mm, MB, 0.75, PAGE_H - MT - MB, fill=1, stroke=0)
    canvas.setFont('RL', 7.5); canvas.setFillColor(TAUPE)
    canvas.drawRightString(PAGE_W - MR, 12 * mm, str(doc.page))
    canvas.setFont('RL', 7.5); canvas.setFillColor(colors.HexColor('#B8B1AA'))
    canvas.drawString(ML, 12 * mm, "EXEC’IA Consulting")
    canvas.restoreState()


def bg_dark(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PRUNE); canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont('RL', 7.5); canvas.setFillColor(colors.HexColor('#9E8080'))
    canvas.drawRightString(PAGE_W - MR, 16 * mm, str(doc.page))
    canvas.setFont('RL-SB', 8.5); canvas.setFillColor(colors.HexColor('#9E8080'))
    canvas.drawCentredString(PAGE_W / 2, 10 * mm,
        "EXEC’IA Consulting  ·  contact@exec-ia.ai  ·  © 2026  ·  Tous droits réservés")
    canvas.restoreState()


# ── Helpers ────────────────────────────────────────────────────────────────────
def sp(h=4):   return Spacer(1, h * mm)
def hr_tc():   return HRFlowable(width='100%', thickness=0.7, color=TERRACOTTA, spaceAfter=4, spaceBefore=2)
def hr_dim():  return HRFlowable(width='100%', thickness=0.35, color=PRUNE_LIGHT, spaceAfter=4, spaceBefore=2)
def rubric(s, t):  return Paragraph(t.upper(), s['rubric'])
def body(s, t):    return Paragraph(t, s['body'])


def pheader(s, num, domain, title):
    return [
        Paragraph(domain.upper(), s['domain']),
        sp(0.5),
        Paragraph(num, s['section_num']),
        sp(3),
        Paragraph(title.replace('\n', '<br/>'), s['section_title']),
        sp(1), hr_tc(), sp(2),
    ]


def conviction_block(s, text):
    return LBB(
        [Paragraph('CONVICTION ' + EXECIA, s['vigil_label']),
         Spacer(1, 2),
         Paragraph(text, s['vigil_body'])],
        bg=IVOIRE_DARK, border=TERRACOTTA, bw=3.5, ph=12, pv=9)


def codir_block(s, text):
    return LBB(
        [Paragraph('QUESTION DE CODIR', s['vigil_label']),
         Spacer(1, 2),
         Paragraph(text, s['vigil_body'])],
        bg=IVOIRE_MID, border=TERRACOTTA, bw=2.5, ph=12, pv=9)


def q_block(s, qs):
    return LBB(
        [Paragraph('— ' + q, s['question']) for q in qs],
        bg=IVOIRE_MID, border=TERRACOTTA, bw=2.5, ph=12, pv=9)


def offer_strip(s, niveau, service):
    return LBB(
        [Paragraph(niveau, s['offer_niveau']),
         Spacer(1, 2),
         Paragraph(service, s['offer_dark'])],
        bg=PRUNE, border=TERRACOTTA, bw=3.5, ph=14, pv=9)


def page_tail(s, conv_text, niveau, service):
    return KeepTogether([
        conviction_block(s, conv_text),
        sp(2),
        offer_strip(s, niveau, service),
    ])


# ── CONTENU ────────────────────────────────────────────────────────────────────
def build_interior(s):
    pages = []

    # ── P01
    pages += pheader(s, "01", "La décision d’investir",
                     "Vous savez que certains projets ne valent rien.\nVous les financez encore.")
    pages += [
        rubric(s, "Accroche"), sp(1),
        body(s, "Chaque décision reportée crée un coût. "
             "Peu d’organisations savent le mesurer."),
        sp(2),
        rubric(s, "Constat"), sp(1),
        body(s, "Vos budgets IA n’ont pas été arbitrés. Ils ont été absorbés. "
             "Sans critère d’arrêt, sans droit de veto, sans responsable du résultat, "
             "les projets continuent parce qu’arrêter obligerait à reconnaître "
             "qu’on s’est trompé. Dans une organisation, personne n’a officiellement ce mandat."),
        sp(2),
        body(s, "Ce que vous ne mesurez pas, c’est le coût de l’inaction. "
             "Chaque arbitrage repoussé immobilise un budget, retarde des revenus, "
             "ralentit des équipes — et laisse parfois un concurrent décider à votre place, "
             "dans un espace que vous avez laissé libre."),
        sp(3),
        codir_block(s, "Quelle décision critique votre comité repousse-t-il depuis plus "
                    "de trois mois — et quel coût cette attente produit-elle déjà ?"),
        sp(3),
        rubric(s, "Questions dirigeant"), sp(1),
        q_block(s, [
            "Qui, dans votre organisation, a formellement le mandat d’arrêter un projet IA "
            "— et ce mandat a-t-il déjà été exercé ?",
            "Quel projet seriez-vous incapable de défendre devant votre conseil dans 30 jours "
            "— et que faites-vous de cette réponse ?",
            "Quels processus créent réellement de la valeur dans votre modèle "
            "— et lesquels financez-vous encore sans arbitrage formalisé ?",
        ]),
        sp(3),
        page_tail(s,
            "Le coût d’une mauvaise décision est visible. "
            "Le coût d’une décision non prise reste invisible "
            "jusqu’au jour où il devient stratégique.",
            EXECIA + " Niveau I", "Diagnostic Exécutif IA"),
        PageBreak(),
    ]

    # ── P02
    pages += pheader(s, "02", "La décision de prioriser",
                     "Vos meilleurs cadres font ce que l’IA pourrait faire.\nEt vous le savez.")
    pages += [
        rubric(s, "Accroche"), sp(1),
        body(s, "La plupart des organisations cherchent à gagner du temps. "
             "Très peu ont décidé ce qu’elles feraient de ce temps."),
        sp(2),
        rubric(s, "Constat"), sp(1),
        body(s, "Vos collaborateurs les plus expérimentés sont absorbés par des réunions "
             "sans suite, des reportings, des validations et des recherches d’information. "
             "Ce temps existe dans vos charges. Il n’existe pas dans votre stratégie."),
        sp(2),
        body(s, "Libérer ce temps ne suffit pas. Décider formellement où le redéployer "
             "— avant de toucher aux outils — c’est ce qui crée de la valeur. "
             "La productivité sans direction ne transforme pas une organisation. "
             "Elle l’accélère dans la mauvaise direction."),
        sp(3),
        codir_block(s, "Si vos cinq meilleurs managers récupéraient une journée par semaine "
                    "demain matin, quelles décisions seraient enfin traitées ?"),
        sp(3),
        rubric(s, "Questions dirigeant"), sp(1),
        q_block(s, [
            "Sur quelles décisions stratégiques vos meilleurs cadres devraient-ils passer "
            "davantage de temps — et pourquoi ce n’est pas encore le cas ?",
            "Avez-vous formellement décidé où sera investi le temps libéré "
            "— ou laissez-vous chaque manager répondre seul à cette question ?",
            "Si vous supprimiez demain les trois tâches les plus chronophages de vos équipes, "
            "qui en bénéficierait — et qui résisterait ?",
        ]),
        sp(3),
        page_tail(s,
            "La productivité n’est pas un objectif. "
            "C’est une ressource supplémentaire. "
            "La question est de savoir qui décide de son utilisation.",
            EXECIA + " Niveau II", "Leadership &amp; Décision IA"),
        PageBreak(),
    ]

    # ── P03
    pages += pheader(s, "03", "La décision de transmettre",
                     "Un expert va partir.\nVous n’avez pas décidé quoi faire avant.")
    pages += [
        rubric(s, "Accroche"), sp(1),
        body(s, "Certaines connaissances critiques n’existent que dans la tête de quelques personnes. "
             "Vous ne le découvrez généralement qu’après leur départ."),
        sp(2),
        rubric(s, "Constat"), sp(1),
        body(s, "Une poignée d’experts concentre une part décisive du savoir critique de votre entreprise. "
             "Ces connaissances ne figurent dans aucun document. Elles vivent dans la tête de quelques personnes "
             "— les raccourcis, les arbitrages, les angles morts que personne d’autre ne connaît."),
        sp(2),
        body(s, "Ce raisonnement ne se reconstruit pas. Il ne se remplace pas avec un outil. "
             "Et aucune technologie ne peut exploiter ce qui n’a jamais été capturé."),
        sp(3),
        codir_block(s, "Si trois personnes quittaient votre organisation demain, "
                    "quelles décisions deviendraient impossibles à prendre "
                    "— et combien de temps durerait ce vide ?"),
        sp(3),
        rubric(s, "Questions dirigeant"), sp(1),
        q_block(s, [
            "Quelle décision critique repose aujourd’hui sur la mémoire d’une seule personne "
            "— et quel est votre plan concret si elle part dans 90 jours ?",
            "Avez-vous formellement désigné un responsable de la transmission du savoir stratégique "
            "— avec un budget, un périmètre, et une date ?",
            "Si vous deviez reconstruire votre avantage concurrentiel sans vos trois meilleurs experts, "
            "par où commenceriez-vous ?",
        ]),
        sp(3),
        page_tail(s,
            "Le savoir stratégique est un actif. "
            "Un actif qui n’est ni documenté, ni transmis, ni protégé "
            "finit toujours par disparaître.",
            EXECIA + " Niveau III", "Advisory de Direction"),
        PageBreak(),
    ]

    # ── P04
    pages += pheader(s, "04", "La décision de fidéliser",
                     "Votre client a décidé de partir\navant votre prochain CODIR.")
    pages += [
        rubric(s, "Accroche"), sp(1),
        body(s, "De nombreux clients perdus avaient déjà envoyé des signaux. "
             "Personne n’avait décidé de les regarder."),
        sp(2),
        rubric(s, "Constat"), sp(1),
        body(s, "Un client ne part pas soudainement. Il accumule des micro-déceptions, "
             "puis prend une décision silencieuse — plusieurs semaines avant que la rupture "
             "soit visible dans vos chiffres. Cette décision se prend dans trois moments précis "
             "de votre parcours. Ces moments ne sont presque jamais identifiés. "
             "Ils ne sont jamais assignés à un responsable."),
        sp(2),
        body(s, "L’écart entre les organisations qui fidélisent et celles qui subissent le churn "
             "n’est pas technologique. Il est décisionnel."),
        sp(3),
        codir_block(s, "Avez-vous identifié les trois moments précis où un client décide "
                    "de rester ou de partir — et qui dans votre organisation "
                    "en est formellement responsable ?"),
        sp(3),
        rubric(s, "Questions dirigeant"), sp(1),
        q_block(s, [
            "Combien de vos processus client ont été conçus pour protéger votre organisation "
            "— et combien pour créer une raison de rester ?",
            "Si votre principal concurrent déployait une IA sur votre meilleur segment client demain, "
            "combien de temps vous faudrait-il pour le détecter "
            "— et quelle décision auriez-vous déjà perdu ?",
            "Quelle information sur vos clients n’existe aujourd’hui que dans la tête de vos commerciaux "
            "— et qu’arrive-t-il quand ils partent ?",
        ]),
        sp(3),
        page_tail(s,
            "Les organisations perdent rarement leurs clients par surprise. "
            "Elles perdent surtout leur capacité à détecter "
            "les signaux qui annonçaient leur départ.",
            EXECIA + " Niveau III", "Advisory de Direction"),
        PageBreak(),
    ]

    # ── P05
    pages += pheader(s, "05", "La décision de gouverner",
                     "Vos outils IA ont plus de pouvoir\nsur vos processus que vous.")
    pages += [
        rubric(s, "Accroche"), sp(1),
        body(s, "Les outils se multiplient plus vite que les règles qui les encadrent. "
             "C’est ainsi que les décisions échappent progressivement à la gouvernance."),
        sp(2),
        rubric(s, "Constat"), sp(1),
        body(s, "Certaines décisions sont aujourd’hui prises par des outils. "
             "D’autres par des habitudes. D’autres encore par des experts "
             "que personne ne remet en question. La plupart des directions générales "
             "n’ont jamais formellement décidé jusqu’où elles faisaient confiance "
             "aux systèmes qui préparent ou prennent des décisions en leur nom."),
        sp(2),
        body(s, "Ce n’est pas un sujet de votre DSI. "
             "C’est votre responsabilité personnelle de dirigeant. "
             "Le sujet n’est pas l’IA. Le sujet est le contrôle."),
        sp(3),
        codir_block(s, "Quelles décisions critiques ne devraient jamais être déléguées "
                    "à un système automatisé — et lesquelles l’ont déjà été "
                    "sans que vous le sachiez ?"),
        sp(3),
        rubric(s, "Questions dirigeant"), sp(1),
        q_block(s, [
            "Avez-vous formellement décidé quelles décisions de votre organisation "
            "ne peuvent pas être déléguées — et cette liste est-elle connue de votre CODIR ?",
            "Si votre principal fournisseur IA augmentait ses tarifs de 40 % demain, "
            "quels processus métier seraient bloqués "
            "— et qui a le mandat de décider de la suite ?",
            "Qui, dans votre organisation, est responsable de la conformité "
            "au Règlement IA européen — depuis quand — et avec quels moyens ?",
        ]),
        sp(3),
        page_tail(s,
            "La gouvernance commence lorsqu’une organisation définit clairement "
            "ce qu’elle délègue, ce qu’elle supervise "
            "et ce qu’elle refuse d’abandonner.",
            EXECIA + " Niveau IV", "Mission de Transformation"),
    ]
    return pages


# ── CONCLUSION ─────────────────────────────────────────────────────────────────
def build_dark(s):
    return [
        sp(4),
        Paragraph("L'APPROCHE " + EXECIA, s['synth_rubric']),
        sp(2),
        Paragraph("L’IA redessine déjà les règles.", s['dark_title']),
        Paragraph("La question est de savoir qui tient encore le crayon.", s['dark_title_tc']),
        sp(3),
        Paragraph("Ce document ne parle pas d’intelligence artificielle.", s['body_dark']),
        Paragraph(
            "Il parle de gouvernance. Il parle de la capacité d’un dirigeant à rester "
            "l’auteur des décisions qui engagent son organisation. Il parle de ce qui se passe "
            "quand personne, dans une direction générale, n’a formellement décidé où s’arrête "
            "la machine et où recommence le jugement humain.",
            s['body_dark']),
        sp(3),
        Paragraph("CE QUE NOUS NE FAISONS PAS", s['ce_what']),
        sp(1),
        Paragraph(
            EXECIA + " ne vend pas des outils.<br/>"
            + EXECIA + " ne vend pas des prompts.<br/>"
            + EXECIA + " ne vend pas de la technologie.",
            s['body_dark']),
        sp(3),
        Paragraph("CE QUE NOUS FAISONS", s['ce_what']),
        sp(1),
        Paragraph(
            "Nous aidons les dirigeants à reprendre le contrôle des décisions "
            "qui engagent leur entreprise. Dans le bon ordre. Avec la bonne méthode. "
            "Avant que le coût de l’attente dépasse le coût de l’action.",
            s['body_dark']),
        sp(2),
        Paragraph(
            "L’IA ne prend pas le pouvoir.<br/>"
            "Elle occupe les espaces que la direction n’a pas encore revendiqués.",
            s['body_dark']),
        sp(2),
        KeepTogether([
            Paragraph(
                "Une organisation dont les décisions sont progressivement dictées "
                "par ses outils, ses fournisseurs ou ses contraintes "
                "n’est plus pleinement dirigée.<br/>"
                "Elle est progressivement administrée.",
                s['body_dark']),
            sp(4), hr_dim(), sp(3),
            Paragraph("4 NIVEAUX D’ENGAGEMENT", s['synth_rubric']),
            sp(2),
        ]),
        Paragraph("Diagnostic Exécutif IA", s['level_label']),
        sp(0.5),
        Paragraph("Identifier vos projets prioritaires. Formaliser vos critères d’arrêt. "
                  "Décider avant d’investir.", s['level_body']),
        sp(1.5),
        Paragraph("Leadership &amp; Décision IA", s['level_label']),
        sp(0.5),
        Paragraph("Comprendre où va l’attention de vos dirigeants. Décider où elle devrait aller. "
                  "Embarquer les équipes dans le bon ordre.", s['level_body']),
        sp(1.5),
        Paragraph("Advisory de Direction", s['level_label']),
        sp(0.5),
        Paragraph("Gouvernance du savoir et de la relation client. "
                  "Accompagnement stratégique continu.", s['level_body']),
        sp(1.5),
        Paragraph("Mission de Transformation", s['level_label']),
        sp(0.5),
        Paragraph("Reprendre le contrôle. Engager votre organisation dans la durée.", s['level_body']),
        sp(3),
        KeepTogether([
            Paragraph(
                "Les organisations qui tireront le plus de valeur de l’intelligence artificielle "
                "ne seront pas celles qui déploieront le plus d’outils. Ce seront celles qui "
                "conserveront la maîtrise de leurs priorités, de leurs arbitrages et de leurs décisions.",
                s['body_dark']),
            sp(3), hr_dim(), sp(3),
            CTACard(s),
        ]),
        sp(3),
        Paragraph("contact@exec-ia.ai", s['cta_email']),
        sp(3),
        Paragraph("·&nbsp;&nbsp;&nbsp;·&nbsp;&nbsp;&nbsp;·", s['asterism']),
        sp(6),
    ]


# ── BUILD ──────────────────────────────────────────────────────────────────────
def main():
    s = S()
    cover_frame    = Frame(ML, BAND_H + 10, CW, PAGE_H - MT - BAND_H - 10, id='cover')
    interior_frame = Frame(ML, MB, CW, PAGE_H - MT - MB, id='int')
    dark_frame     = Frame(ML, MB + 10, CW, PAGE_H - MT - MB - 10, id='dark')

    doc = BaseDocTemplate(OUTPUT, pagesize=A4,
                          leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)
    doc.addPageTemplates([
        PageTemplate('Cover',    [cover_frame],    onPage=bg_cover),
        PageTemplate('Interior', [interior_frame], onPage=bg_interior),
        PageTemplate('Dark',     [dark_frame],     onPage=bg_dark),
    ])

    story = (
        [NextPageTemplate('Cover'), Spacer(1, 1)]
        + [NextPageTemplate('Interior'), PageBreak()]
        + build_interior(s)
        + [NextPageTemplate('Dark'), PageBreak()]
        + build_dark(s)
    )
    doc.build(story)
    print(f"✓  {OUTPUT}")


if __name__ == '__main__':
    main()
