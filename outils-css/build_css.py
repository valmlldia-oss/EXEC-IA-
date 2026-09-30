# EXEC'IA · génération des feuilles de style
# Usage, après toute modification de assets/style.css :
#     python3 outils-css/build_css.py
# 1) style.css -> style.min.css (retire commentaires et blancs)
# 2) Chrome headless relève, page par page, les sélecteurs réellement présents
# 3) intègre dans chaque page, entre <style id="css-page"> et </style>, ses seules règles utiles
#    (ne jamais modifier ce bloc à la main : il est réécrit à chaque passage)
# Les classes posées par JavaScript et les états (:hover, [open]…) sont conservés.
# Ensuite : vérifier la mise en page (1440 et 390 px), puis déployer.
import re,json,glob,os,subprocess,time,html,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=open(R+'/assets/style.css',encoding='utf8').read()
out=[];i=0;q=None
while i<len(src):
    c=src[i]
    if q:
        out.append(c)
        if c=='\\': out.append(src[i+1]); i+=2; continue
        if c==q: q=None
        i+=1; continue
    if c in '"\'': q=c; out.append(c); i+=1; continue
    if src.startswith('/*',i):
        j=src.index('*/',i+2); i=j+2; continue
    out.append(c); i+=1
mn='\n'.join(l.strip() for l in ''.join(out).split('\n') if l.strip())+'\n'
open(R+'/assets/style.min.css','w',encoding='utf8').write(mn)



CSS=open(R+'/assets/style.min.css',encoding='utf8').read()
# ---------- parse ----------
def parse(s,i=0,end=None):
    items=[]; n=len(s)
    while i<n:
        while i<n and s[i] in ' \n\t': i+=1
        if i>=n: break
        if s[i]=='}': return items,i+1
        j=i; depth=0; q=None
        while j<n:
            c=s[j]
            if q:
                if c=='\\': j+=2; continue
                if c==q: q=None
            elif c in '"\'': q=c
            elif c=='(': depth+=1
            elif c==')': depth-=1
            elif c=='{' and depth==0: break
            elif c==';' and depth==0: break
            j+=1
        prelude=s[i:j].strip()
        if j>=n: break
        if s[j]==';':
            items.append(('stmt',prelude)); i=j+1; continue
        if prelude.startswith('@media') or prelude.startswith('@supports') or prelude.startswith('@layer'):
            kids,k=parse(s,j+1); items.append(('block',prelude,kids)); i=k; continue
        # rule or opaque at-rule : body jusqu'à l'accolade fermante équilibrée
        k=j+1; depth=1; q=None
        while k<n and depth:
            c=s[k]
            if q:
                if c=='\\': k+=2; continue
                if c==q: q=None
            elif c in '"\'': q=c
            elif c=='{': depth+=1
            elif c=='}': depth-=1
            k+=1
        body=s[j+1:k-1]
        items.append(('rule',prelude,body) if not prelude.startswith('@') else ('opaque',prelude,body)); i=k
    return items,i
ITEMS,_=parse(CSS)
# ---------- classes dynamiques ----------
# tous les scripts du site (script.js, assets/inline/*.js, chat-widget.js…) : les classes qu'ils posent doivent être gardées
js=' '.join(open(f,encoding='utf8').read() for f in sorted(glob.glob(R+'/assets/*.js')+glob.glob(R+'/assets/inline/*.js')))
inline=''
for f in glob.glob(R+'/*.html'):
    s=open(f,encoding='utf8').read()
    inline+=' '.join(re.findall(r'<script(?![^>]*ld\+json)[^>]*>(.*?)</script>',s,re.S))
# tout mot présent dans un script (y compris dans les gabarits HTML construits par JS : bandeau cookies, chat, simulateur…)
DYN=set(re.findall(r"[A-Za-z][\w-]*",js+inline))
DYN|={'open','active','visible','is-visible','scrolled','playing'}
def split_sel(sel):
    out=[];d=0;cur=''
    for c in sel:
        if c in '([': d+=1
        elif c in ')]': d-=1
        if c==',' and d==0: out.append(cur); cur=''
        else: cur+=c
    out.append(cur); return [x.strip() for x in out if x.strip()]
PSEUDO=r':(?:hover|focus-visible|focus-within|focus|active|visited|checked|target|placeholder-shown|disabled|enabled|autofill|-webkit-autofill|fullscreen|popover-open|user-invalid|invalid|valid|indeterminate|playing|paused)\b'
def base(sel):
    s=re.sub(r'::?(?:before|after|placeholder|selection|marker|backdrop|-webkit-[\w-]+|-moz-[\w-]+|first-letter|first-line|file-selector-button)\b(\([^)]*\))?','',sel)
    s=re.sub(PSEUDO,'',s)
    s=re.sub(r'\[(?:open|aria-[\w-]+|data-theme|hidden)(?:[~|^$*]?=[^\]]*)?\]','',s)
    def dropcls(m):
        return '' if m.group(1) in DYN else m.group(0)
    s=re.sub(r'\.([\w-]+)',dropcls,s)
    s=re.sub(r'\s*([>+~])\s*',r' \1 ',s.strip())
    toks=s.split()
    while toks and toks[-1] in '>+~': toks.pop()
    out=[]
    for t in toks:
        if t in ('>','+','~'):
            if not out or out[-1] in ('>','+','~'): out.append('*')
        out.append(t)
    return ' '.join(out) or '*'
SELS=set()
def collect(items):
    for it in items:
        if it[0]=='rule':
            for x in split_sel(it[1]): SELS.add(base(x))
        elif it[0]=='block': collect(it[2])
collect(ITEMS)
SELS=sorted(SELS)

LINK=re.compile(r'assets/(?:style\.min\.css|p/[\w-]+\.css)(?:\?v=\d+)?|<style id="css-page">')
PAGES=[os.path.basename(f) for f in sorted(glob.glob(R+'/*.html')) if LINK.search(open(f,encoding='utf8').read())]
TPL='''<!doctype html><body><pre id="o">RUNNING</pre><script>
const pages=%PAGES%, sels=%SELS%;
(async()=>{const res={};for(const p of pages){const f=document.createElement('iframe');f.style.cssText='position:absolute;left:0;top:0;border:0;width:1440px;height:900px';f.src='/'+p;document.body.appendChild(f);await new Promise(r=>{f.onload=()=>setTimeout(r,1800)});const d=f.contentDocument;
d.querySelectorAll('details').forEach(x=>x.open=true);
const used=[];sels.forEach((s,i)=>{let ok=true;try{ok=!!d.querySelector(s)}catch(e){ok=true}if(ok)used.push(i)});res[p]=used;f.remove()}
document.getElementById('o').textContent='DONE\\n'+JSON.stringify(res)})();
</script>'''
open(R+'/__pg.html','w').write(TPL.replace('%PAGES%',json.dumps(PAGES)).replace('%SELS%',json.dumps(SELS)))
srv=subprocess.Popen(['python3','-m','http.server','8781'],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(2)
out=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--window-size=1440,900','--virtual-time-budget=400000','--dump-dom','http://localhost:8781/__pg.html'],capture_output=True,text=True).stdout
srv.terminate(); os.remove(R+'/__pg.html')
t=re.sub(r'<[^>]*>','',out[out.index('<pre'):out.index('</pre>')])
USED=json.loads(html.unescape(t.split('\n',1)[1]))
json.dump({'sels':SELS,'used':USED},open('used.json','w'))
print(len(SELS),'sélecteurs,',len(PAGES),'pages')


idx={s:i for i,s in enumerate(SELS)}
def emit(items,used):
    out=[]
    for it in items:
        if it[0]=='stmt': out.append(it[1]+';')
        elif it[0]=='opaque': out.append(it[1]+'{'+it[2]+'}')
        elif it[0]=='rule':
            if any(idx[base(x)] in used for x in split_sel(it[1])): out.append(it[1]+'{'+it[2]+'}')
        elif it[0]=='block':
            inner=emit(it[2],used)
            if inner: out.append(it[1]+'{'+''.join(inner)+'}')
    return out

STYLE=re.compile(r'<style id="css-page">.*?</style>',re.S)
for p in PAGES:
    css='\n'.join(emit(ITEMS,set(USED[p])))
    # les url() de style.css sont relatives au dossier assets/ : on les rend relatives à la page
    css=re.sub(r'url\(\s*([\'"]?)(?!data:|https?:|/|#)([^)\'"]+)\1\s*\)',lambda m:'url('+m.group(1)+'assets/'+m.group(2)+m.group(1)+')',css)
    s=open(R+'/'+p,encoding='utf8').read()
    tag='<style id="css-page">\n'+css+'\n</style>'
    s=STYLE.sub(lambda m:tag,s) if STYLE.search(s) else re.sub(r'<link rel="stylesheet" href="assets/(?:style\.min\.css|p/[\w-]+\.css)(?:\?v=\d+)?">',lambda m:tag,s)
    open(R+'/'+p,'w',encoding='utf8').write(s)
print('pages',len(PAGES),'feuille de style intégrée dans chaque page')
