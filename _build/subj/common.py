# -*- coding: utf-8 -*-
"""Shared shell + components for services / subjects / legal pages. Reuses career/build.py shell (header, footer, CSS)."""
import os, re, sys, json, html as H, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1]
CAREER = os.path.join(HERE, '..', 'career')
sys.path.insert(0, CAREER)
import content as C
spec = importlib.util.spec_from_file_location('cbuild', os.path.join(CAREER, 'build.py'))
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
BASE = B.BASE
TODAY = '2026-11-14'

# programme colours (AP uses navy, never ochre)
COL = {'igcse': ('#1d7f86', '#e1f1f1'), 'a-level': ('#1d7f86', '#e1f1f1'), 'ib': ('#1d5bd8', '#eaf1fd'), 'ap': ('#16294d', '#e9edf5'),
       'mid': ('#0f6b70', '#e3f1ea'), 'svc': ('#1d5bd8', '#eaf1fd'), 'legal': ('#16294d', '#e9edf5')}

PRICE = {'el': ('小学生（G1〜G5）', '¥10,000'), 'ms': ('中学生（G6〜G8）', '¥12,000'), 'hs': ('高校生（G9〜G12）', '¥15,000'),
         'adv': ('高校生（IB DP・AP・Cambridge A Level）', '¥16,000')}

EXTRA_CSS = '''
.sj-facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:18px 0 6px;padding:0}
.sj-facts div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 14px;min-width:0}
.sj-facts dt{font-size:12px;color:var(--muted);margin:0}
.sj-facts dd{margin:2px 0 0;font-size:14.5px;font-weight:600;color:var(--ink);line-height:1.55}
.sj-top{list-style:none;margin:6px 0 14px;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px}
.sj-top li{background:#fff;border:1px solid var(--line);border-left:3px solid var(--c);border-radius:8px;padding:9px 12px;font-size:14px;line-height:1.6;min-width:0}
.sj-top.one{grid-template-columns:minmax(0,1fr)}.sj-top.two,.sj-grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
@media (max-width:640px){.sj-top.two,.sj-grid.two{grid-template-columns:minmax(0,1fr)}}
.sj-off{margin:14px 0 4px;display:flex;gap:10px;align-items:flex-start;flex-wrap:wrap}
.sj-off>p{margin:6px 0 0;font-size:12.5px;font-weight:700;color:var(--muted);white-space:nowrap}
.sj-off>div{display:flex;flex-wrap:wrap;gap:8px;min-width:0;flex:1}
.sj-off a{display:inline-flex;align-items:center;gap:7px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:6px 13px 6px 6px;font-size:13px;color:var(--ink);text-decoration:none;max-width:100%}
.sj-off a:hover{border-color:var(--c)}
.sj-off i{font-style:normal;font-size:11px;font-weight:700;color:#fff;background:var(--c);border-radius:999px;padding:2px 8px;white-space:nowrap}
.sj-note{background:var(--ct);border-radius:12px;padding:14px 18px;margin:6px 0 16px;font-size:15px;line-height:1.85}
.sj-cam{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:16px;margin:8px 0 18px}
.sj-cam>div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;min-width:0}
.sj-cam h4{margin:0 0 8px;font-size:15.5px;color:var(--ink)}
.sj-cam ul{margin:0;padding-left:1.2em}.sj-cam li{margin:4px 0;font-size:14.5px;line-height:1.7}
.sj-price{display:flex;flex-direction:column;gap:6px}
.sj-cam>div:not(.sj-plan){background:none;border:0;border-radius:0;padding:4px 0}
.sj-cam>div.sj-plan{background:#16294d;border-color:#16294d;color:#fff;box-shadow:0 14px 30px -18px rgba(11,31,75,.6)}
.sj-cam .sj-plan .sj-plan-tg{display:inline-block;align-self:flex-start;margin:0 0 2px;padding:2px 10px;border:0;border-radius:999px;background:#7cc0ff;color:#0b1f4b;font-size:11px;font-weight:800;letter-spacing:.08em}
.sj-cam .sj-plan h4{margin:0 0 4px;color:#fff;font-size:21px}.sj-cam .sj-plan h4 small{display:block;margin-top:2px;font-size:12px;font-weight:500;color:#c9d8ee}
.sj-cam .sj-plan p{border-bottom-color:rgba(255,255,255,.22);color:#dfe8f5;flex-wrap:wrap;row-gap:0}.sj-cam .sj-plan p b{margin-left:auto}
.sj-cam .sj-plan b{color:#fff;font-size:22px}.sj-cam .sj-plan b small{color:#c9d8ee}
.sj-cam .sj-plan .fine{color:#c9d8ee}
.sj-plan-cta{display:block;margin:8px 0 0;padding:11px 14px;border-radius:999px;background:#7cc0ff;color:#0b1f4b;font-weight:800;font-size:15px;text-align:center;text-decoration:none}
.sj-plan-cta:hover{background:#a3d3ff}.sj-plan-cta:focus-visible{outline:2px solid #fff;outline-offset:2px}
.sj-price p{margin:0;display:flex;justify-content:space-between;gap:10px;align-items:baseline;border-bottom:1px dashed var(--line);padding:4px 0;font-size:14px}
.sj-price b{font-size:18px;color:var(--ink);white-space:nowrap}.sj-price small{font-size:12px;color:var(--muted)}
.sj-price .fine{display:block;border:0;font-size:12.5px;color:var(--muted);line-height:1.7}
.sj-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin:8px 0 22px}
.sj-grid a{display:flex;flex-direction:column;gap:2px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px;text-decoration:none;color:var(--ink);min-width:0}
.sj-grid a:hover{border-color:var(--c)}
.sj-grid b{font-size:15px;line-height:1.5}.sj-grid span{font-size:12.5px;color:var(--muted);line-height:1.6}
.sj-grid i{font-style:normal;font-size:11.5px;font-weight:700;color:var(--c)}
.sj-h{font-size:18px;margin:26px 0 6px;color:var(--ink)}
.lg-tbl{width:100%;border-collapse:collapse;margin:8px 0 20px;font-size:14.5px;line-height:1.75;background:#fff}
.lg-tbl th,.lg-tbl td{border:1px solid var(--line);padding:10px 14px;text-align:left;vertical-align:top}
.lg-tbl th{width:30%;background:var(--ct);font-weight:600}
.lg-body h2{font-size:18px;margin:28px 0 6px}.lg-body p,.lg-body li{font-size:15px;line-height:1.85}
.sv-flow{list-style:none;padding:0;margin:8px 0 18px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.sv-flow li{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:14px;line-height:1.65}
.sv-flow b{display:block;font-size:15px}.sv-flow span{color:var(--muted);font-size:12.5px}
@media (max-width:760px){.sj-cam{grid-template-columns:1fr}.sv-flow{grid-template-columns:1fr}.lg-tbl th{width:36%}}
'''

def esc(s):
    return H.escape(s, quote=False)

COL_NAV = ('<nav class="toc gnav" aria-label="コラム"><div class="toc-in"><span class="gl">コラム</span><a href="/column/">すべて</a>'
           '<a href="/column/schools/"><i style="background:var(--cp)"></i>スクール選び</a><a href="/column/curriculum/" class="on" aria-current="page"><i style="background:var(--or)"></i>インターのカリキュラム</a>'
           '<a href="/column/university/"><i style="background:var(--uni)"></i>大学進学</a><a href="/column/english/"><i style="background:var(--myp)"></i>英語・資格</a>'
           '<a href="/column/career/"><i style="background:var(--ap)"></i>就職活動</a></div></nav>')

def shell(path, title, desc, ld, nav=None, en='/en/'):
    url = BASE + path
    head, hdr, tail = B.shell(url, title, desc, ld)
    head = head.replace('</style>\n</head>', EXTRA_CSS + '</style>\n</head>', 1)
    if nav != COL_NAV:
        hdr = hdr.replace(' class="on" href="/column/" aria-current="true"', ' href="/column/"')
    hdr = hdr.replace('href="/en/column/"', 'href="%s"' % en)
    hdr = re.sub(r'<nav class="toc gnav".*?</nav>', nav or '', hdr, flags=re.S)
    tail = re.sub(r'<nav class="toc gnav".*?</nav>', '', tail, flags=re.S)
    return head, hdr, tail

def subnav(label, items, on):
    a = ''.join('<a href="%s"%s>%s</a>' % (u, ' class="on" aria-current="page"' if u == on else '', n) for n, u in items)
    return '<nav class="toc gnav" aria-label="%s"><div class="toc-in"><span class="gl">%s</span>%s</div></nav>' % (label, label, a)

SUBJ_NAV = [('すべて', '/subjects/'), ('IB DP', '/subjects/ib/'), ('IGCSE', '/subjects/igcse/'), ('A Level', '/subjects/a-level/'), ('AP', '/subjects/ap/'), ('中学（MYP・Lower Secondary）', '/subjects/middle-school/')]
SVC_NAV = [('すべて', '/services/'), ('インター生の家庭教師', '/services/international-school/'), ('IB', '/services/ib/'), ('IGCSE・A Level', '/services/igcse-a-level/'),
           ('AP', '/services/ap/'), ('英語資格', '/services/english-tests/'), ('保護者の相談', '/services/consultation/'), ('面談の同席', '/services/parent-conference/')]

def facts(rows):
    return '<dl class="sj-facts">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % r for r in rows)

def toc(items):
    return '<nav class="otl" aria-label="目次"><p>目次</p><ol>%s</ol></nav>' % ''.join('<li><a href="#%s"><span>%d</span>%s</a></li>' % (i, n + 1, t) for n, (i, t) in enumerate(items))

def grid(cards, cls=''):
    return '<div class="sj-grid'+(' '+cls if cls else '')+'">%s</div>' % ''.join('<a href="%s">%s<b>%s</b><span>%s</span></a>' % (u, ('<i>%s</i>' % tag) if tag else '', b, d) for u, tag, b, d in cards)

def srcs(lst):
    return ''.join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, esc(n)) for u, n in lst)

def page(path, title, desc, h1, small, lead, body, crumbs, faq=None, nxt=None, cta=None, src=None, src_note='', nav=None, kind='svc',
         extra_hero='', toc_items=None, ld_type='WebPage', extra_ld=None):
    c, ct = COL[kind]
    sty = 'style="--c:%s;--ct:%s"' % (c, ct)
    items = [('Camino', '/')] + crumbs
    graph = [{'@type': ld_type, 'name': re.sub(r'<[^>]+>', '', h1), 'description': desc, 'inLanguage': 'ja', 'url': BASE + path,
              'isPartOf': {'@id': BASE + '/#website'}, 'dateModified': TODAY}, B.bc_ld(items)]
    if faq:
        graph.append({'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', a)}} for q, a in faq]})
    if extra_ld:
        graph += extra_ld
    ld = {'@context': 'https://schema.org', '@graph': graph}
    head, hdr, tail = shell(path, title, desc, ld, nav)
    out = ['<main>\n<section class="phero" %s>\n  <div class="wrap">\n    %s\n    <div class="ph"><h1><small>%s</small>%s</h1></div>\n    <p class="lead">%s</p>%s%s\n  </div>\n</section>\n' % (
        sty, B.crumbs([(n, u) for n, u in items[:-1]] + [(items[-1][0], None)]), small, h1, lead, extra_hero, toc(toc_items) if toc_items else '')]
    out.append('<section class="sec first th" %s>\n  <div class="wrap">\n%s\n  </div>\n</section>\n' % (sty, body))
    if faq:
        out.append('<section class="sec" id="faq">\n  <div class="wrap">\n    <div class="sec-h c"><div class="eyebrow">FAQ</div><h2>よくある質問</h2></div>\n    <div class="faq">%s</div>\n  </div>\n</section>\n'
                   % ''.join('<details><summary>%s</summary><div class="a">%s</div></details>' % qa for qa in faq))
    if nxt:
        out.append('<section class="sec sec-alt" id="next">\n  <div class="wrap">\n    <div class="sec-h"><div class="eyebrow">Next</div><h2>あわせて読みたい</h2></div>\n    %s\n  </div>\n</section>\n' % B.nx(nxt).replace('--k:#1d5bd8', '--k:%s' % c))
    if cta:
        out.append(B.cta(*cta) + '\n')
    if src:
        out.append('<section class="sec" style="padding:48px 0">\n  <div class="wrap src">\n    <h2>出典</h2>\n    <p>%s</p>\n    <ul>%s</ul>\n  </div>\n</section>\n' % (src_note, srcs(src)))
    B.write(path.strip('/'), head + hdr + ''.join(out) + tail)
    return BASE + path
