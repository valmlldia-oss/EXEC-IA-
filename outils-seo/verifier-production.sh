#!/bin/bash
# Contrôle HTTP réel du site en production (à lancer APRÈS le déploiement).
# Usage : bash outils-seo/verifier-production.sh [https://exec-ia.ai]
B="${1:-https://exec-ia.ai}"; ok=0; ko=0
t(){ if [ "$2" = "$3" ]; then ok=$((ok+1)); echo "OK   $1"; else ko=$((ko+1)); echo "ERREUR $1 : obtenu « $3 », attendu « $2 »"; fi; }
red(){ # source, destination attendue (code 301 ou 308 accepté)
  r=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' "$B$1"); c=${r%% *}; l=${r#* }
  [ "$c" = 301 ] || [ "$c" = 308 ] && c=redir
  t "redirection $1" "redir $B$2" "$c $l"; }
echo "== Redirections (Vercel renvoie 308 pour « permanent », équivalent d'une 301) =="
red /expertise.html /offres.html#expertise-strategique
red /expertise-en.html /offres-en.html#expertise-strategique
red /expertise-es.html /offres-es.html#expertise-strategique
red /expertise /offres.html#expertise-strategique
red /articles.html /perspectives.html
red /articles /perspectives.html
red /index.html /
echo "== Pages (200 attendu) =="
for p in / accueil.html a-propos.html offres.html solutions.html agents-ia.html realisations.html temoignages.html ressources.html perspectives.html contact.html conformite-ia-pme.html plan-du-site.html \
  index-en.html a-propos-en.html offres-en.html solutions-en.html agents-ia-en.html realisations-en.html ressources-en.html perspectives-en.html contact-en.html \
  index-es.html a-propos-es.html offres-es.html solutions-es.html agents-ia-es.html realisations-es.html ressources-es.html perspectives-es.html contact-es.html \
  sitemap.xml robots.txt assets/anchor-open.js assets/inline/conformite-countdown.js; do
  t "$p" 200 "$(curl -s -o /dev/null -w '%{http_code}' "$B/${p#/}")"; done
echo "== Canonical et hreflang =="
for p in a-propos.html offres.html solutions.html perspectives.html; do
  h=$(curl -s "$B/$p"); c=$(echo "$h" | grep -o '<link rel="canonical" href="[^"]*"' | head -1)
  t "canonical $p" "<link rel=\"canonical\" href=\"https://exec-ia.ai/$p\"" "$c"
  n=$(echo "$h" | grep -c 'hreflang='); t "hreflang $p (4 balises)" 4 "$n"; done
echo "== Sitemap : toutes les URL répondent 200 =="
for u in $(curl -s "$B/sitemap.xml" | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g'); do
  c=$(curl -s -o /dev/null -w '%{http_code}' "$u"); [ "$c" = 200 ] || { ko=$((ko+1)); echo "ERREUR sitemap $u : $c"; }; done
echo "== En-têtes de sécurité =="
t "Content-Security-Policy présent" 1 "$(curl -sI "$B/" | grep -ci '^content-security-policy')"
echo; echo "Résultat : $ok OK, $ko erreur(s)"
