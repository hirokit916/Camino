# -*- coding: utf-8 -*-
"""Idempotent site-wide wiring: footer links (JA pages), home fees link, sitemap entries. usage: python3 integrate.py <site_root>"""
import os, sys, glob, re
ROOT = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
LINKS = ('<p class="ft-links"><a href="/about/">運営者情報</a>'
         '<a href="/privacy/">プライバシーポリシー</a></p>')
CSS = ('<style id="ft-links-css">.ft-links{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 16px;margin:14px 0 0;padding:0 16px;font-size:12.5px;line-height:1.8;width:100%}'
       '.foot .ft-links{justify-content:flex-end;padding:0}.ft-links a{color:inherit;opacity:.75;text-decoration:none}.ft-links a:hover{opacity:1;text-decoration:underline}</style>')
GN = '<a href="/subjects/"><i style="background:#1d7f86"></i>科目別ガイド</a>'
n = 0
for p in glob.glob(ROOT + '/**/index.html', recursive=True):
    rel = p[len(ROOT):]
    if rel.startswith('/_preview') or rel.startswith('/en/'): continue
    s = open(p).read()
    if 'http-equiv="refresh"' in s: continue
    o = s
    if 'class="ft-links"' in s:
        s = re.sub(r'<p class="ft-links">.*?</p>', LINKS, s)
    else:
        s = s.replace('</footer>', LINKS + '</footer>').replace('</head>', CSS + '</head>', 1)
    def _nav(m):
        x = m.group(0)
        return x.replace(GN, '')
    s = re.sub(r'<nav class="toc gnav" aria-label="コラム">.*?</nav>', _nav, s, flags=re.S)
    if s != o:
        open(p, 'w').write(s); n += 1
print('footer/nav updated on', n, 'pages')
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], ROOT]
from data_cambridge import IGCSE, ALEVEL
from data_ib import DP
from data_ap import AP
from data_mid import MID
SG_CSS = ('<style id="subj-guides-css">.sg-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin:10px 0 26px}'
          '.sg-grid a{display:flex;flex-direction:column;gap:2px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px;text-decoration:none;color:var(--ink);min-width:0}'
          '.sg-grid a:hover{border-color:var(--c,#1d5bd8)}.sg-grid b{font-size:15px;line-height:1.5}.sg-grid span{font-size:12.5px;color:var(--muted);line-height:1.6}'
          '.sg-grid i{font-style:normal;font-size:11.5px;font-weight:700;color:var(--c,#1d5bd8)}.sg-sub{font-size:16px;margin:18px 0 2px;color:var(--ink)}</style>')
def cards(lst):
    return '<div class="sg-grid">%s</div>' % ''.join('<a href="%s">%s<b>%s</b><span>%s</span></a>' % (u, ('<i>%s</i>' % t) if t else '', b, d) for u, t, b, d in lst)
def sec(h2, lead, groups, sty):
    body = ''.join(('<h3 class="sg-sub">%s</h3>' % gh if gh else '') + cards(cs) for gh, cs in groups)
    return ('<section class="sec sec-alt" id="subjects" %s>\n  <div class="wrap">\n    <div class="sec-h"><div class="eyebrow">Subjects</div><h2>%s</h2></div>\n'
            '    <p class="muted">%s</p>\n    %s\n  </div>\n</section>\n') % (sty, h2, lead, body)
LEAD = '科目ごとの試験の構成と出題範囲を、公式資料をもとにまとめています'
SECS = {
 'ib/dp': ('DPの科目別ガイド', [('', [('/subjects/ib/%s/' % d['slug'], None, d['ja'], d['en']) for d in DP])], 'style="--c:var(--dp)"'),
 'ib/myp': ('MYPの科目別ガイド', [('', [('/subjects/myp/%s/' % d['slug'], None, d['ja'].split('（')[0], d['en']) for d in MID if d['group'] == 'myp'])], 'style="--c:var(--myp)"'),
 'curriculum/cambridge': ('Cambridgeの科目別ガイド', [('IGCSE', [('/subjects/igcse/%s/' % d['slug'], d['code'].split('（')[0], d['ja'], d['en']) for d in IGCSE]),
                                                    ('AS & A Level', [('/subjects/a-level/%s/' % d['slug'], d['code'], d['ja'], d['en']) for d in ALEVEL]),
                                                    ('Lower Secondary（中学）', [('/subjects/lower-secondary/%s/' % d['slug'], d['code'], d['ja'].split('（')[0], d['en']) for d in MID if d['group'] == 'ls'])], 'style="--c:var(--cam)"'),
 'curriculum/ap': ('APの科目別ガイド', [('', [('/subjects/ap/%s/' % d['slug'], None, d['ja'], d['en']) for d in AP])], 'style="--c:var(--ap)"'),
}
for rel, (h2, groups, sty) in SECS.items():
    p = os.path.join(ROOT, rel, 'index.html'); s = open(p).read(); o = s
    s = re.sub(r'<section class="sec sec-alt" id="subjects".*?</section>\n', '', s, flags=re.S)
    s = s.replace('<section class="sec" id="faq">', sec(h2, LEAD, groups, sty) + '<section class="sec" id="faq">', 1)
    if 'subj-guides-css' not in s:
        s = s.replace('</head>', SG_CSS + '</head>', 1)
    m = re.search(r'(<nav class="otl"[^>]*>.*?<ol>)(.*?)(</ol>)', s, re.S)
    if m and '#subjects' not in m.group(2):
        k = m.group(2).count('<li>') + 1
        s = s[:m.start(2)] + m.group(2) + '<li><a href="#subjects"><span>%d</span>科目別ガイド</a></li>' % k + s[m.end(2):]
    if s != o:
        open(p, 'w').write(s); print('subject guides section:', rel)
hp = ROOT + '/index.html'; s = open(hp).read()
s2 = re.sub(r'<p class="phead-more"[^>]*>.*?</p>', '', s)
if s2 != s:
    open(hp, 'w').write(s2); print('home plan-page link removed')
sm = ROOT + '/sitemap.xml'; s = open(sm).read()
urls = []
for f in ('urls_subjects.txt', 'urls_services.txt'):
    urls += open(os.path.join(HERE, f)).read().split()
s = re.sub(r'  <url>\n    <loc>https://caminotutor.com/tokushoho/</loc>.*?</url>\n', '', s, flags=re.S)
add = ''
for u in urls:
    if '<loc>%s</loc>' % u in s: continue
    add += '  <url>\n    <loc>%s</loc>\n    <lastmod>2026-11-14</lastmod>\n    <xhtml:link rel="alternate" hreflang="ja" href="%s"/>\n  </url>\n' % (u, u)
s = s.replace('</urlset>', add + '</urlset>')
if s != open(sm).read():
    open(sm, 'w').write(s)
print('sitemap urls now', s.count('<url>'))
