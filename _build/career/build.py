# -*- coding: utf-8 -*-
"""Build /column/career/ hub + articles on the column shell, rebuild the topic wheel, add 就職活動 to the column nav.
usage: python3 build.py <site_root>"""
import os, re, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C
ROOT = sys.argv[1]
SHELL = open(os.path.join(ROOT, 'column/english/eiken/index.html')).read()
BASE = 'https://caminotutor.com'
GNAV_CAREER = '<a href="/column/career/"><i style="background:var(--ap)"></i>就職活動</a>'

CSS = '''
.cr-p{font-size:15px;line-height:1.95;color:var(--ink);margin:6px 0 14px;max-width:820px}
.cr-h4{font-size:16px;font-weight:700;color:var(--ink);margin:26px 0 8px}
.cr-more{margin:4px 0 10px;font-size:14.5px}.cr-more a{color:var(--c);font-weight:700}
.cr-memo{position:relative;margin:14px 0 22px;padding:20px 22px 16px;background:var(--ct);border-radius:16px;border-left:4px solid var(--c)}
.cr-memo .cr-ml{margin:0 0 8px;font-size:12.5px;font-weight:700;letter-spacing:.06em;color:var(--c)}
.cr-memo p{font-size:14.5px;line-height:1.9;color:var(--ink);margin:0 0 8px}
.cr-memo .ul2 li{color:var(--ink)}
.cr-memo .ul2 li b{color:var(--ink);margin-right:4px}
.cr-flow{list-style:none;margin:10px 0 12px;padding:0;display:flex;flex-wrap:wrap;gap:8px 22px;counter-reset:f}
.cr-flow li{position:relative;display:flex;flex-direction:column;justify-content:center;min-width:96px;padding:10px 14px;background:#fff;border:1px solid var(--line);border-radius:12px}
.cr-flow li b{font-size:13.5px;color:var(--ink);line-height:1.5}
.cr-flow li span{font-size:12px;color:var(--soft);line-height:1.5}
.cr-flow li:not(:last-child)::after{content:"";position:absolute;right:-16px;top:50%;width:9px;height:9px;border-top:2px solid var(--c);border-right:2px solid var(--c);transform:translateY(-50%) rotate(45deg)}
.cr-cos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:8px 0 10px}
.cr-co{background:#fff;border:1px solid var(--line);border-top:4px solid var(--c);border-radius:18px;padding:20px 20px 14px;display:flex;flex-direction:column}
.cr-co header{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 12px;margin-bottom:10px}
.cr-co h4{margin:0;font-size:17px;color:var(--ink)}
.cr-tag{font-size:12px;font-weight:700;color:var(--c);background:var(--ct);border-radius:999px;padding:3px 10px}
.cr-co dl{margin:0 0 6px;display:grid;gap:6px}
.cr-co dl div{display:grid;grid-template-columns:76px minmax(0,1fr);gap:10px;font-size:13.5px;line-height:1.75}
.cr-co dt{color:var(--soft);font-weight:700}.cr-co dd{margin:0;color:var(--ink)}
.cr-co .cr-flow,.cr-vflow{flex-direction:column;flex-wrap:nowrap;gap:0;margin:8px 0 10px;padding:12px 14px;background:var(--ct);border-radius:12px}
.cr-co .cr-flow li{flex-direction:row;justify-content:flex-start;align-items:baseline;gap:10px;min-width:0;padding:4px 0 4px 20px;background:none;border:0;border-radius:0}
.cr-co .cr-flow li::before{content:"";position:absolute;left:3px;top:.95em;width:8px;height:8px;border-radius:50%;background:var(--c)}
.cr-co .cr-flow li:not(:last-child)::after{content:"";position:absolute;left:6.5px;top:1.3em;bottom:-.6em;right:auto;width:1.5px;height:auto;border:0;background:var(--c);opacity:.45;transform:none}
.cr-co .cr-flow li b{flex:none}
.cr-note{font-size:13px;line-height:1.8;color:var(--soft);margin:2px 0 8px}
.cr-src{margin:auto 0 0;padding-top:8px;border-top:1px dashed var(--line);font-size:12px;color:var(--muted)}
.cr-src a{color:var(--c)}
.cr-p b,.ul2 b,.cr-memo b,.phero .lead b,.cf-big-p b,.etbl td b,.flow b{color:var(--ink);font-weight:700;background:linear-gradient(transparent 60%,#cfe2fb 60%);padding:0 1px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.cf-big{margin:6px 0 30px;padding:30px 34px;border-radius:22px;background:#0b1f4b;color:#fff;position:relative;overflow:hidden}
.cf-big::after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;border:28px solid rgba(127,188,255,.16)}
.cf-big-h{position:relative;margin:0;font-family:var(--mincho,serif);font-size:30px;line-height:1.55;font-weight:600;letter-spacing:.02em}
.cf-big-h b{color:#7fbcff;font-weight:700}
.cf-big-p{position:relative;margin:14px 0 0;font-size:15px;line-height:1.95;color:rgba(255,255,255,.86);max-width:44em}
@media (max-width:600px){.cf-big{padding:24px 20px}.cf-big-h{font-size:22px}.cf-big-p{font-size:14px}}
.cf-ind{margin:8px 0 6px;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}
.cf-ind div{display:grid;grid-template-columns:170px minmax(0,1fr);gap:18px;align-items:baseline;padding:12px 22px;border-top:1px solid #edf1f7}
.cf-ind div:first-child{border-top:0}
.cf-ind div:nth-child(even){background:#fafbfd}
.cf-ind h4{margin:0;font-size:14px;font-weight:700;color:#1d5bd8}
.cf-ind p{margin:0;font-size:14px;line-height:1.85;color:var(--ink)}
@media (max-width:600px){.cf-ind div{grid-template-columns:1fr;gap:3px;padding:12px 16px}.cf-ind p{font-size:13.5px}}
.cr-ind{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:8px 0 6px}
.cr-ind div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.cr-ind h4{margin:0 0 6px;font-size:14.5px;color:var(--c)}
.cr-ind p{margin:0;font-size:13.5px;line-height:1.8;color:var(--ink)}
.cr-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:8px 0 6px}
.cr-two>div{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.cr-two>div.hl{border:2px solid var(--c)}
.cr-two h4{margin:0 0 8px;font-size:16px;color:var(--ink)}
.cr-two p{margin:0;font-size:14px;line-height:1.9;color:var(--ink)}
.cr-cot{table-layout:fixed;width:100%}
.cr-cot th,.cr-cot td{white-space:normal!important;word-break:normal;overflow-wrap:anywhere}
.cr-cot thead th:nth-child(1){width:17%}.cr-cot thead th:nth-child(2){width:11%}.cr-cot thead th:nth-child(3){width:40%}
.cr-tt thead th:nth-child(1){width:16%}.cr-tt thead th:nth-child(2){width:17%}.cr-tt thead th:nth-child(3){width:42%}
@media (max-width:760px){.cr-cot{table-layout:auto}.cr-cot thead th{width:auto!important}}
.cr-gh{font-family:var(--mincho,serif);font-size:22px;font-weight:600;color:var(--ink);margin:34px 0 14px;display:flex;align-items:center;gap:10px}
.cr-gh:first-child{margin-top:0}
.cr-gh::before{content:"";width:6px;height:22px;border-radius:3px;background:var(--c)}
.ss-map{list-style:none;margin:10px 0 18px;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;counter-reset:ph}
.ss-map>li{position:relative;background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px 12px 10px}
.ss-map>li:not(:last-child)::after{content:"";position:absolute;right:-8px;top:26px;width:7px;height:7px;border-top:2px solid var(--c);border-right:2px solid var(--c);transform:rotate(45deg);background:var(--paper,#fdfcfa)}
.ss-map .sm-h{display:flex;align-items:center;gap:8px;font-weight:700;font-size:14.5px;color:var(--ink);text-decoration:none;margin-bottom:8px}
.ss-map .sm-h:hover{color:var(--c)}
.ss-map .sm-h i{font-style:normal;flex:none;width:24px;height:24px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-size:12.5px}
.ss-map ul{list-style:none;margin:0;padding:0;display:grid;gap:5px}
.ss-map ul li{font-size:12.5px;line-height:1.5;color:var(--ink);background:var(--ct);border-radius:8px;padding:5px 8px}
@media (max-width:1100px){.ss-map{grid-template-columns:repeat(3,minmax(0,1fr))}.ss-map>li:nth-child(3n)::after{display:none}}
@media (max-width:600px){.ss-map{grid-template-columns:1fr}.ss-map>li::after{display:none}}
.cr-mxw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:6px 0 8px;border:1px solid var(--line);border-radius:16px;background:#fff}
.cr-mx{border-collapse:collapse;min-width:720px;width:100%;font-size:13px}
.cr-mx th,.cr-mx td{padding:10px 6px;border-bottom:1px solid var(--line);text-align:center;vertical-align:middle}
.cr-mx thead th{background:var(--ct);color:var(--ink);font-weight:700;font-size:11.5px;line-height:1.45}
.cr-mx tbody th{position:sticky;left:0;background:#fff;text-align:left;font-weight:700;color:var(--ink);white-space:nowrap;z-index:1;box-shadow:1px 0 0 var(--line)}
.cr-mx thead th:first-child{position:sticky;left:0;z-index:2;text-align:left}
.cr-mx tbody th small{display:block;font-weight:400;font-size:11.5px;color:var(--soft)}
.cr-mx .mx-y{font-style:normal;color:var(--c);font-size:15px}
.cr-mx .mx-n{color:#c3cad6}
.cr-mx tbody tr:last-child th,.cr-mx tbody tr:last-child td{border-bottom:0}
.tl{list-style:none;margin:8px 0 10px;padding:0;position:relative}
.tl::before{content:"";position:absolute;left:150px;top:6px;bottom:6px;width:2px;background:color-mix(in srgb,var(--c) 35%,#fff)}
.tl>li{position:relative;display:grid;grid-template-columns:150px minmax(0,1fr);gap:0 28px;padding:0 0 18px}
.tl>li::before{content:"";position:absolute;left:144px;top:6px;width:14px;height:14px;border-radius:50%;background:#fff;border:3px solid var(--c)}
.tl-when{text-align:right;padding-right:24px}
.tl-when b{display:block;font-size:14.5px;color:var(--ink);line-height:1.5}
.tl-when span{display:block;font-size:12px;color:var(--soft)}
.tl-what{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 16px}
.tl-what p{margin:0;font-size:14px;line-height:1.85;color:var(--ink)}
.tl-what p+p{margin-top:6px;padding-top:6px;border-top:1px dashed var(--line)}
@media (max-width:640px){.tl::before{left:7px}.tl>li{grid-template-columns:1fr;gap:6px;padding-left:30px}.tl>li::before{left:1px}.tl-when{text-align:left;padding:0;display:flex;gap:10px;align-items:baseline}}
.cr-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:10px 0 14px}
.cr-stats div{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px}
.cr-stats b{display:block;font-family:var(--latin,serif);font-size:36px;line-height:1.1;color:var(--c);font-weight:600}
.cr-stats p{margin:6px 0 4px;font-size:14px;font-weight:700;color:var(--ink);line-height:1.6}
.cr-stats span{display:block;font-size:12px;color:var(--soft);line-height:1.6}
.cr-el{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:8px 0 10px}
.cr-el div{background:#fff;border:1px solid var(--line);border-top:4px solid var(--c);border-radius:14px;padding:14px 14px 12px;display:flex;flex-direction:column;gap:6px}
.cr-el h4{margin:0;font-size:16px;color:var(--ink)}
.cr-el p{margin:0;font-size:13.5px;line-height:1.75;color:var(--ink)}
.cr-el span{margin-top:auto;font-size:12px;line-height:1.6;color:var(--soft);padding-top:6px;border-top:1px dashed var(--line)}
@media (max-width:900px){.cr-el{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.cr-el{grid-template-columns:1fr}}
.cr-hub{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.cr-hub a{display:flex;flex-direction:column;gap:8px;background:#fff;border:1px solid var(--line);border-top:5px solid var(--c);border-radius:20px;padding:22px 22px 18px;text-decoration:none;color:var(--ink);transition:transform .2s,box-shadow .2s}
.cr-hub a:hover{transform:translateY(-3px);box-shadow:0 16px 30px -22px rgba(0,0,0,.4)}
.cr-hub b{font-size:18px;line-height:1.5}.cr-hub span{font-size:14px;line-height:1.85;color:var(--soft)}
.cr-hub em{margin-top:auto;font-style:normal;font-size:13.5px;font-weight:700;color:var(--c)}
@media (max-width:900px){.cr-cos{grid-template-columns:1fr}.cr-ind{grid-template-columns:repeat(2,minmax(0,1fr))}.cr-hub{grid-template-columns:1fr}}
@media (max-width:600px){.cr-ind{grid-template-columns:1fr}.cr-two{grid-template-columns:1fr}
.cr-flow{flex-direction:column;flex-wrap:nowrap;gap:14px}.cr-flow li{flex-direction:row;justify-content:flex-start;align-items:baseline;gap:10px}
.cr-flow li:not(:last-child)::after{right:auto;left:22px;top:auto;bottom:-12px;transform:rotate(135deg)}
.cr-co .cr-flow{gap:0}.cr-co .cr-flow li:not(:last-child)::after{left:6.5px;bottom:-.6em;transform:none}
.cr-co dl div{grid-template-columns:76px minmax(0,1fr)}}
'''

def shell(url, title, desc, ld):
    h = SHELL
    head, body = h[:h.index('<body')], h[h.index('<body'):]
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, head)
    head = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + desc, head)
    head = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*', lambda m: m.group(1) + title, head)
    head = head.replace(BASE + '/column/english/eiken/', url)
    head = re.sub(r'<link rel="alternate" hreflang="en"[^>]*>\n?', '', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False, indent=1), head, count=1, flags=re.S)
    head = head.replace('</head>', '<style id="camino-career">%s%s</style>\n</head>' % (CSS, PMAP_CSS))
    hdr = body[:body.index('<main>')]
    hdr = hdr.replace('/en/column/english/eiken/', '/en/column/')
    tail = body[body.index('</main>'):]
    tail = re.sub(r'<nav class="toc gnav".*?</nav>', lambda m: gnav(m.group(0), True), tail, flags=re.S)
    return head, hdr, tail

def gnav(nav, on=False):
    nav = nav.replace(' class="on" aria-current="page"', '').replace(' aria-current="page" class="on"', '')
    if '/column/career/' not in nav:
        nav = nav.replace('</div></nav>', GNAV_CAREER + '</div></nav>')
    if on:
        nav = nav.replace('<a href="/column/career/">', '<a href="/column/career/" class="on" aria-current="page">')
    return nav

def crumbs(items):
    return ('<div class="crumb">' + '<span>›</span>'.join(('<a href="%s">%s</a>' % (u, n)) if u else '<span>%s</span>' % n for n, u in items) + '</div>')

def bc_ld(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + (u or '')} for i, (n, u) in enumerate(items) if u is not None]}

def nx(items):
    out = []
    for u, b, d, main in items:
        out.append('<a href="%s"%s style="--k:#1d5bd8">%s<b>%s</b><span class="d">%s</span><span class="go">詳しく見る →</span></a>' % (
            u, ' class="main"' if main else '', '<span class="tg">次に読む</span>' if main else '', b, d))
    return '<div class="nx rise">%s</div>' % ''.join(out)

def cta(h, p):
    return ('<section class="sec" style="border-top:none;padding-top:10px"><div class="wrap"><div class="cta rise"><div><h2>%s</h2><p>%s</p></div>'
            '<div class="cta-btns"><a class="btn btn-or" href="/#contact">無料体験・ご相談</a></div></div></div></section>') % (h, p)

def write(path, html):
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(html)
    print('wrote', path, len(html) // 1024, 'KB')

STY = 'style="--c:#1d5bd8;--ct:#eaf1fd;--ap:#1d5bd8;--ap-t:#eaf1fd"'

def article(a):
    url = BASE + '/column/career/%s/' % a['slug']
    items = [('Camino', '/'), ('コラム', '/column/'), ('就職活動', '/column/career/'), (a['crumb'], '/column/career/%s/' % a['slug'])]
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Article', 'headline': re.sub(r'<[^>]+>', '', a['h1']), 'description': a['desc'], 'inLanguage': 'ja', 'mainEntityOfPage': url,
         'author': {'@id': BASE + '/#organization'}, 'publisher': {'@id': BASE + '/#organization'}, 'datePublished': '2026-11-12', 'dateModified': '2026-11-12'},
        bc_ld(items),
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in a['faq']]}]}
    head, hdr, tail = shell(url, a['title'], a['desc'], ld)
    toc = ''.join('<li><a href="#%s"><span>%d</span>%s</a></li>' % (i, n + 1, t) for n, (i, t) in enumerate(a['toc']))
    main = ('<main>\n<section class="phero" %s>\n  <div class="wrap">\n    %s\n    <div class="ph"><h1><small>就職活動</small>%s</h1></div>\n    <p class="lead">%s</p>'
            '<nav class="otl" aria-label="目次"><p>目次</p><ol>%s</ol></nav>\n  </div>\n</section>\n'
            '<section class="sec first th" %s>\n  <div class="wrap">\n%s\n  </div>\n</section>\n'
            '<section class="sec" id="faq">\n  <div class="wrap">\n    <div class="sec-h c"><div class="eyebrow">FAQ</div><h2>よくある質問</h2></div>\n    <div class="faq">%s</div>\n  </div>\n</section>\n'
            '<section class="sec sec-alt" id="next">\n  <div class="wrap">\n    <div class="sec-h"><div class="eyebrow">Next</div><h2>あわせて読みたい</h2></div>\n    %s\n  </div>\n</section>\n'
            '%s\n<section class="sec" style="padding:48px 0">\n  <div class="wrap src">\n    <h2>出典</h2>\n    <p>本ページは、各社の公式の募集要項、イベントの主催者・参加企業の公式発表、官公庁の公開情報をもとに、整理したものです。Caminoは掲載している企業・団体と提携していません。日程や選考の流れは年度によって変わるため、最新の情報は各社・各団体の公式サイトをご確認ください</p>\n    <ul>%s</ul>\n  </div>\n</section>\n') % (
        STY, crumbs([(n, u) for n, u in items[:-1]] + [(a['crumb'], None)]), a['h1'], a['lead'], toc, STY, a['body'],
        ''.join('<details><summary>%s</summary><div class="a">%s</div></details>' % qa for qa in a['faq']),
        nx(a['next']), cta(*a['cta']), C.srcs(a['src']))
    write('column/career/%s' % a['slug'], head + hdr + main + tail)


PMAP_CSS = """
.pm{margin:8px 0 6px;--g:16px}
.cr-hubp .lead{margin-bottom:6px}
.cr-hubp{padding-top:22px!important;padding-bottom:24px!important}
.cr-hubp .ph{margin-bottom:6px}
.pm-cap{margin:0 0 12px;font-size:13px;color:var(--soft)}
.pmap{display:grid;grid-template-columns:150px minmax(0,1fr) 112px;align-items:center;gap:0}
.pm-n{display:flex;flex-direction:column;gap:3px;text-decoration:none;color:var(--ink);background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px 14px;transition:border-color .2s,transform .2s,box-shadow .2s}
a.pm-n:hover,a.pm-n:focus-visible{border-color:var(--k,var(--c));transform:translateY(-2px);box-shadow:0 12px 22px -18px rgba(0,0,0,.45)}
.pm-n b{font-size:14.5px;line-height:1.45}.pm-n span{font-size:12px;line-height:1.6;color:var(--soft)}
.pm-start .pm-n{background:var(--ct);border-color:transparent}
.pm-start,.pm-end{position:relative}
.pm-start::after,.pm-end::before{content:"";position:absolute;top:50%;width:16px;height:2px;background:#c9d3e3}
.pm-start::after{right:-15px}.pm-end::before{left:-15px}
.pm-end .pm-n{background:var(--ink);border-color:var(--ink);color:#fff;text-align:center;align-items:center;padding:18px 10px}
.pm-end .pm-n b{font-size:18px;letter-spacing:.1em}.pm-end .pm-n span{color:rgba(255,255,255,.75)}
.pm-lanes{position:relative;display:grid;grid-auto-rows:1fr;gap:var(--g);padding:0 34px}
.pm-lanes::before,.pm-lanes::after{content:"";position:absolute;top:calc((100% - 2*var(--g))/6);bottom:calc((100% - 2*var(--g))/6);width:2px;background:#c9d3e3}
.pm-lanes::before{left:14px}.pm-lanes::after{right:14px}
.pm-lane{position:relative;display:grid;grid-template-columns:172px minmax(0,1fr);align-items:center;gap:22px;background:color-mix(in srgb,var(--k) 6%,#fff);border:1px solid color-mix(in srgb,var(--k) 22%,#fff);border-radius:18px;padding:14px 16px}
.pm-lane::before,.pm-lane::after{content:"";position:absolute;top:50%;width:20px;height:2px;background:#c9d3e3}
.pm-lane::before{left:-21px}.pm-lane::after{right:-21px}
.pm-lh{background:var(--k)!important;border-color:var(--k)!important;color:#fff!important}
.pm-lh span{color:rgba(255,255,255,.82)!important}
.pm-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.pm-steps li{position:relative;display:flex}
.pm-steps li .pm-n{flex:1;justify-content:center}
.pm-steps li:not(:last-child)::after{content:"";position:absolute;right:-15px;top:50%;width:8px;height:8px;border-top:2px solid var(--k);border-right:2px solid var(--k);transform:translateY(-50%) rotate(45deg)}
.pm-br{grid-column:2;margin:-4px 0 0;font-size:12px;color:var(--k);font-weight:600;display:flex;align-items:center;gap:6px}
.pm-br::before{content:"";width:14px;height:0;border-top:1.5px dashed var(--k)}
.pm-more{margin:14px 0 0;display:flex;flex-wrap:wrap;gap:10px}
.pm-more a{display:inline-flex;align-items:center;gap:6px;padding:9px 16px;border-radius:999px;border:1.5px solid var(--c);color:var(--c);font-weight:700;font-size:14px;text-decoration:none;background:#fff}
.pm-more a:hover{background:var(--c);color:#fff}
.pmap2{grid-template-columns:minmax(0,1fr) 112px}
.pmap2 .pm-lanes{padding:0 34px 0 0}
.pmap2 .pm-lanes::before,.pmap2 .pm-lane::before{display:none}
.pmap2 .pm-lane{grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:18px;padding:8px 10px;border-radius:16px}
.pmap2 .pm-lanes{--g:14px;gap:14px}
.pmap2 .pm-lh{display:grid!important;grid-template-columns:auto auto 1fr;column-gap:10px;align-items:baseline;padding:9px 14px!important}
.pmap2 .pm-lh em{grid-column:1;background:rgba(255,255,255,.18);border-radius:999px;padding:1px 8px}
.pmap2 .pm-lh b{grid-column:2;font-size:17px!important}
.pmap2 .pm-lh small{grid-column:3}
.pmap2 .pm-lh span{grid-column:1/-1;margin-top:3px!important;font-size:12.5px!important;line-height:1.6!important}
.pmap2 .pm-steps{gap:20px}
.pmap2 .pm-steps .pm-n{padding:8px 8px;align-items:center;text-align:center}
.pmap2 .pm-steps .pm-n b{font-size:14.5px}
.pmap2 .pm-end .pm-n{padding:14px 8px}
.pm-lh{gap:4px!important;padding:14px 16px!important}
.pm-lh em{font-style:normal;font-size:11.5px;font-weight:700;letter-spacing:.06em;color:rgba(255,255,255,.8)}
.pm-lh b{font-size:18px!important}
.pm-lh small{font-family:var(--latin,serif);font-style:italic;font-size:13px;color:rgba(255,255,255,.85)}
.pm-lh span{margin-top:4px;font-size:12.5px!important;line-height:1.7!important;color:rgba(255,255,255,.92)!important}
.pm-intro{margin:0 0 10px;font-size:16px;line-height:1.9;color:var(--ink)}
.pm-intro b{color:var(--c)}
.pm-note{margin:10px 0 4px;padding:9px 14px;background:#fff;border:1px solid var(--line);border-radius:12px;font-size:13.5px;line-height:1.85;color:var(--ink)}
.pm-note b{color:var(--c);margin-right:6px}
.pmap2 .pm-n{position:relative}
.pmap2 .pm-steps .pm-n,.pmap2 .pm-lh{cursor:default}
.pmap2 .pm-n:hover{transform:none;box-shadow:none}
.pmap2 .pm-steps .pm-n:hover{border-color:var(--line)}
.pm-q{position:absolute;z-index:3;white-space:nowrap;font-size:12px;font-weight:700;line-height:1.3;color:var(--k);background:#fff;border:1.5px solid var(--k);border-radius:999px;padding:5px 11px;text-decoration:none;box-shadow:0 6px 14px -8px rgba(11,31,75,.45);transition:background .15s,color .15s,transform .15s}
.pm-q::after{content:"";position:absolute;width:8px;height:8px;background:#fff;border-right:1.5px solid var(--k);border-bottom:1.5px solid var(--k)}
.pm-q:hover,.pm-q:focus-visible{background:var(--k);color:#fff}
.pm-q:hover::after,.pm-q:focus-visible::after{background:var(--k)}
.pm-q.q-top{left:50%;bottom:calc(100% + 9px);transform:translateX(-50%)}
.pm-q.q-top::after{left:50%;bottom:-5.5px;transform:translateX(-50%) rotate(45deg)}
.pm-q.q-head{right:-14px;top:-14px;color:var(--k)}
.pm-q.q-head::after{left:18px;bottom:-5.5px;transform:rotate(45deg)}
.pm-q.q-head:hover{color:#fff}
.pmap2 .pm-lanes{padding-top:0}
@media (max-width:960px){.pmap2 .pm-lane{padding-top:30px;gap:36px}.pm-q.q-head{top:-27px;right:2px}}
@media (max-width:560px){.pm-q{font-size:11px;padding:4px 9px}.pmap2 .pm-lane{padding-top:30px!important;gap:34px!important}.pm-q.q-head{right:2px;top:-27px}.pm-q.q-top{bottom:calc(100% + 7px)}.pm-steps li:last-child .pm-q.q-top{left:auto;right:-4px;transform:none}.pm-steps li:last-child .pm-q.q-top::after{left:auto;right:22px;transform:rotate(45deg)}}
@media (max-width:560px){
 .pmap2 .pm-steps{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:14px!important}
 .pmap2 .pm-steps li:not(:last-child)::after{right:-11px!important;left:auto!important;top:50%!important;bottom:auto!important;width:6px!important;height:6px!important;transform:translateY(-50%) rotate(45deg)!important}
 .pmap2 .pm-steps .pm-n{padding:8px 4px}
 .pmap2 .pm-steps .pm-n b{font-size:13px;line-height:1.35}
 .pmap2 .pm-steps .pm-n span{font-size:10.5px}
 .pmap2 .pm-lane{gap:8px;padding:8px}
 .pmap2 .pm-lh span{font-size:12px!important}
 .pmap2{gap:14px}
 .pmap2 .pm-lanes{gap:8px}
}
@media (max-width:960px){
 .pmap{grid-template-columns:1fr;gap:26px}
 .pmap2 .pm-lanes{padding:0}
 .pmap2 .pm-lane{grid-template-columns:1fr}
 .pm-lanes{padding:0;grid-auto-rows:auto;gap:12px}.pm-lanes::after,.pm-lane::after,.pm-lane::before{display:none}
 .pm-lanes::before{display:none!important}
 .pm-start::after{display:none}
 .pm-end::before{left:50%;top:-22px;width:2px;height:18px}
 .pm-lane{grid-template-columns:1fr;gap:12px}
 .pm-br{grid-column:1}
}
@media (max-width:560px){
 .pm-steps{grid-template-columns:1fr;gap:14px}
 .pm-steps li:not(:last-child)::after{right:auto;left:50%;top:auto;bottom:-12px;transform:translateX(-50%) rotate(135deg)}
}
/* hub v3: plain lanes, highlighted forum lane, answer popovers */
.pm-lane.pm-plain{--k:#0b1f4b;background:#f8f9fb;border-color:#e3e7ee}
.pm-plain .pm-lh{background:#fff!important;border-color:#dfe4ec!important;color:var(--ink)!important}
.pm-plain .pm-lh em{background:#eef1f6!important;color:#5c6984!important}
.pm-plain .pm-lh small{color:#5c6984!important}
.pm-plain .pm-lh span{color:var(--soft)!important}
.pm-plain .pm-steps li:not(:last-child)::after{border-color:#a9b4c6!important}
.cr-hubp{--hl:#1d5bd8}.pm-intro b{color:var(--hl)}
.pm-lane.pm-key{--k:var(--hl);background:color-mix(in srgb,var(--hl) 7%,#fff);border:2px solid var(--hl);box-shadow:0 18px 34px -26px color-mix(in srgb,var(--hl) 80%,#000)}
.pm-lane.pm-key{padding-bottom:24px;margin-bottom:18px}
@media (min-width:1180px){.pmap2 .pm-lh{padding-left:12px!important;padding-right:12px!important}.pmap2 .pm-lh span{font-size:12px!important}.pmap2 .pm-lh span{white-space:nowrap}}
.pm-hl{position:absolute;left:14px;bottom:-1px;transform:translateY(50%);z-index:2;margin:0;display:flex;align-items:center;gap:0;max-width:calc(100% - 28px);padding:6px 14px;border-radius:18px;background:#fff;border:2px solid var(--hl);box-shadow:0 8px 18px -12px color-mix(in srgb,var(--hl) 80%,#000)}
.pm-hl b{flex:none;font-size:12.5px;font-weight:700;color:var(--hl);line-height:1.5}
.pm-hl span{font-size:12px;line-height:1.5;color:var(--ink);margin-left:10px;padding-left:10px;border-left:1px solid color-mix(in srgb,var(--hl) 30%,#fff)}
@media (min-width:961px){.pmap2 .pm-lane.pm-key::before{bottom:calc(-1 * var(--g) - 20px)}}
@media (max-width:960px){.pm-lane.pm-key{padding-bottom:60px;margin-bottom:44px}.pm-hl{left:12px;right:12px;max-width:none;flex-direction:column;align-items:flex-start;gap:3px;padding:8px 14px 9px}.pm-hl span{margin:0;padding:0;border:0}}
button.pm-q{font-family:inherit;cursor:pointer;margin:0}
.pm-plain .pm-q{--k:#0b1f4b}
.pm-cap2{margin:10px 0 0;font-size:13px;color:var(--soft)}
.pm-sites{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:stretch}
.pm-sites>span{flex-basis:100%;font-size:13px;font-weight:700;color:var(--soft)}
.pm-sites a{display:flex;flex-direction:column;gap:1px;padding:9px 16px;border-radius:12px;border:1.5px solid #cfe2fb;background:#f4f8fe;text-decoration:none;color:var(--ink)}
.pm-sites a:hover{border-color:#1d5bd8}
.pm-sites b{font-size:15px;color:#1d5bd8}
.pm-sites small{font-size:12px;color:var(--soft)}
.pm-ans{width:min(560px,calc(100vw - 32px));max-height:calc(100dvh - 48px);overflow:auto;margin:auto;border:0;border-radius:20px;padding:26px 28px 24px;background:#fff;color:var(--ink);box-shadow:0 30px 60px -20px rgba(11,31,75,.45);border-top:6px solid var(--hl)}
.pm-ans::backdrop{background:rgba(11,31,75,.38)}
.pm-ans h3{margin:0 36px 12px 0;font-family:var(--mincho,serif);font-size:21px;line-height:1.5;font-weight:600;color:var(--ink)}
.pm-ans p{margin:0 0 12px;font-size:15px;line-height:1.95}
.pm-ans p:last-of-type{margin-bottom:0}
.pm-ans-link{display:inline-flex;margin-top:16px;padding:9px 16px;border-radius:999px;border:1.5px solid var(--hl);background:var(--hl);color:#fff!important;font-weight:700;font-size:14px;text-decoration:none}
.pm-ans-link:hover{background:#0b1f4b;border-color:#0b1f4b}
.pm-x{position:absolute;top:14px;right:14px;width:34px;height:34px;border-radius:50%;border:1px solid var(--line);background:#fff;font-size:20px;line-height:1;color:var(--ink);cursor:pointer;font-family:inherit}
.pm-x:hover{background:#f1f3f7}
.pmap2 .pm-lanes{grid-auto-rows:auto}
@media (min-width:961px){.pmap2 .pm-lanes::after{display:none}
.pmap2 .pm-lane::before{display:block!important;content:"";position:absolute;left:auto;right:-22px;width:2px;height:auto;background:#c9d3e3;top:0;bottom:calc(-1 * var(--g) - 2px)}
.pmap2 .pm-lane:first-child::before{top:50%}
.pmap2 .pm-lane:last-child::before{top:-2px;bottom:50%}
.pm-key .pm-q.q-head{top:-20px}}
.cr-hub1{grid-template-columns:minmax(0,560px)}
@media (max-width:560px){.pm-ans{padding:22px 20px 20px}.pm-ans h3{font-size:18px}.pm-ans p{font-size:14.5px}}

@media (min-width:961px){.pmap2{position:relative;grid-template-columns:minmax(0,1fr) 112px}.pmap2 .pm-lanes{padding-right:40px!important}.pmap2{grid-template-columns:minmax(0,1fr) 84px!important}
@media (min-width:1180px){.pm-hl span{font-size:11.5px}}
@media (max-width:1179px){.pmap2 .pm-steps{gap:16px}.pmap2 .pm-steps .pm-n{padding:8px 4px}.pmap2 .pm-steps .pm-n b{font-size:13.5px}.pmap2 .pm-steps li:not(:last-child)::after{right:-12px}}
.pmap2 .pm-lane::before,.pmap2 .pm-lane::after,.pmap2 .pm-lanes::after,.pmap2 .pm-end::before{display:none!important}
.pm-arrows{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}}
@media (max-width:960px){.pm-arrows{display:none}.pmap2 .pm-end{display:none}}
@media (min-width:961px){.pmap2 .pm-end{align-self:stretch;display:flex}.pmap2 .pm-end .pm-n{flex:1;justify-content:center;border-radius:18px}.pmap2 .pm-end .pm-n b{font-size:22px;letter-spacing:.2em;writing-mode:vertical-rl}}
"""
def node(href, b, sp='', cls='pm-n'):
    return '<a class="%s" href="%s"><b>%s</b>%s</a>' % (cls, href, b, ('<span>%s</span>' % sp) if sp else '')
def lane_head(no, title, sub, desc, q=''):
    return '<div class="pm-n pm-lh"><em>%s</em><b>%s</b><small>%s</small><span>%s</span>%s</div>' % (no, title, sub, desc, q)
def step_box(b, sp='', q=''):
    return '<div class="pm-n"><b>%s</b>%s%s</div>' % (b, ('<span>%s</span>' % sp) if sp else '', q)
def bubble(pid, text, cls=''):
    return '<button type="button" class="pm-q %s" popovertarget="%s">%s</button>' % (cls, pid, text)

QA = [
 ('qa-forum', 'キャリアフォーラムって何？',
  ['日本語と英語を話す学生を対象に、日系企業や外資系企業がまとめて参加する就職イベントです。ボストン・ロンドン・東京などで開かれるキャリアフォーラムが代表的で、事前にWebで応募しておき、会場で企業との面談を受けます。会期中に内定が出ることもあります',
   'インター生の多くが、ここで就職先を見つけています'],
  ('/column/career/career-forum/', 'キャリアフォーラムについて詳しく見る')),
 ('qa-tests', '適性検査って何？',
  ['応募したあとに、Webや専用のテスト会場で受ける試験です。主に、文章や言葉を扱う「言語」、計算や図表の読み取りを扱う「非言語」、人柄や考え方の傾向を見る「性格検査」があり、企業によっては英語のテストが加わります',
   '非言語（数学）の問題は学校の数学に近い内容ですが、インター生は言語（国語）の問題を特にしっかり練習しておく必要があります。どの検査にも対策本がたくさん出ているので、早めに準備を始めましょう'],
  ('/column/career/japan-tests/', '適性検査について詳しく見る')),
 ('qa-mendan', '面談って何が聞かれるの？',
  ['聞かれることは国によって違いますが、業界ごとに傾向があります。就活サイトや、過去の質問が投稿されている体験談のサイトなどで、事前に調べておきましょう',
   '<span class="pm-sites"><span>過去の質問を調べられるサイトの例</span><a href="https://www.glassdoor.com/" target="_blank" rel="noopener"><b>Glassdoor</b><small>米国の企業の選考体験記</small></a><a href="https://www.onecareer.jp/" target="_blank" rel="noopener"><b>ONE CAREER</b><small>日本の企業の選考体験記</small></a></span>',
   '面談は、その国の言葉で行われることが多く、外資系企業では英語のこともあります。日本では日本語の面接が中心で、英語の面接が追加で行われることがよくあります。海外の大学から応募する場合でも、日本語と英語の両方で話せるように準備しておく必要があります'], None),
 ('qa-intern', 'インターンって何？',
  ['学生のうちに、企業で一定期間働く経験のことです。企業の募集を自分で探して応募するほか、大学のキャリアセンターに相談したり、教授から紹介してもらったりして見つかることもあります。待っていても声はかからないので、自分から積極的に探すことが大切です',
   '選び方は、働きたい企業、興味のある分野、身につけたいスキルや知識など、いろいろです。企業名で選ぶ人が多いのですが、面接で聞かれるのは「どこで」働いたかではなく「何を」したかです'], None),
]

def answers():
    out = []
    for pid, q, ps, link in QA:
        body = ''.join('<p>%s</p>' % x for x in ps)
        if link:
            body += '<a class="pm-ans-link" href="%s">%s →</a>' % link
        out.append('<div class="pm-ans" id="%s" popover role="dialog" aria-labelledby="%s-h"><button type="button" class="pm-x" popovertarget="%s" popovertargetaction="hide" aria-label="閉じる">×</button><h3 id="%s-h">%s</h3>%s</div>' % (pid, pid, pid, pid, q, body))
    return ''.join(out)

def pmap():
    lanes = [
        ('pm-plain', lane_head('ルート1', '通常選考', 'Official Route', '企業の採用ページから応募し、企業が決めた日程で選考を受ける、一般的なルート'),
         [step_box('応募'), step_box('適性検査', q=bubble('qa-tests', '適性検査って何？', 'q-top')), step_box('面接')], ''),
        ('pm-key', lane_head('ルート2', '就活イベント', 'Job Hunting Event', '多くの企業が集まるイベント（キャリアフォーラムなど）で数社まとめて応募・面談可能',
                                bubble('qa-forum', 'キャリアフォーラムって何？', 'q-head')),
         [step_box('応募'), step_box('適性検査'), step_box('面談', '', bubble('qa-mendan', '面談って何が聞かれるの？', 'q-top'))],
         '<p class="pm-hl"><b>インター生の多くが仕事を見つける重要なルート</b><span>講師自身も、インター時代の友人の多くも、キャリアフォーラムで就職先を見つけました</span></p>'),
        ('pm-plain', lane_head('ルート3', 'インターン', 'Internship', '企業のインターンに参加し、そこでの評価をもとに、特別選考に進む道',
                                bubble('qa-intern', 'インターンって何？', 'q-head')),
         [step_box('応募'), step_box('インターン参加'), step_box('特別選考')], ''),
    ]
    L = ''.join('<div class="pm-lane %s">%s<ol class="pm-steps">%s</ol>%s</div>' % (
        cls, head, ''.join('<li>%s</li>' % n for n in steps), extra) for cls, head, steps, extra in lanes)
    return ('<div class="pm rise"><p class="pm-intro">インター出身者が、海外や日本の大学に進み、その後就職するまでのアプローチは様々ですが、主なものは次の<b>3つ</b>。並行して進めることも可能</p>'
            '<div class="pmap pmap2" role="group" aria-label="就職までの3つのルート">'
            '<div class="pm-lanes">%s</div><div class="pm-end"><div class="pm-n"><b>内定</b></div></div><svg class="pm-arrows" aria-hidden="true"></svg></div><script>(function(){var m=document.querySelector(\'.pmap2\');if(!m)return;var sv=m.querySelector(\'.pm-arrows\');function d(){if(innerWidth<961){sv.innerHTML=\'\';return}var R=m.getBoundingClientRect(),E=m.querySelector(\'.pm-end .pm-n\').getBoundingClientRect(),L=m.querySelectorAll(\'.pm-lane\');var ex=E.left-R.left-3,ec=E.top+E.height/2-R.top,n=L.length,h=\'<defs><marker id="pa0" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#a3afc2"/></marker><marker id="pa1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1d5bd8"/></marker></defs>\';L.forEach(function(l,i){var b=l.getBoundingClientRect(),sx=b.right-R.left+2,sy=b.top+b.height/2-R.top,ty=ec+(i-(n-1)/2)*16,k=l.classList.contains(\'pm-key\'),mx=sx+(ex-sx)*.55;h+=\'<path d="M\'+sx+\' \'+sy+\'L\'+ex+\' \'+sy+\'" fill="none" stroke="\'+(k?\'#1d5bd8\':\'#a3afc2\')+\'" stroke-width="\'+(k?3:2)+\'" stroke-linecap="round" marker-end="url(#pa\'+(k?1:0)+\')"/>\'});sv.setAttribute(\'viewBox\',\'0 0 \'+R.width+\' \'+R.height);sv.innerHTML=h}d();addEventListener(\'resize\',d);if(document.fonts)document.fonts.ready.then(d);if(window.ResizeObserver)new ResizeObserver(d).observe(m)})();</script>'
            '<p class="pm-cap2">吹き出しを押すと、よくある質問への回答が開きます</p>%s</div>') % (L, answers())

def hub():
    h = C.HUB
    url = BASE + '/column/career/'
    items = [('Camino', '/'), ('コラム', '/column/'), ('就職活動', '/column/career/')]
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', 'name': '就職活動', 'description': h['desc'], 'inLanguage': 'ja', 'url': url,
         'hasPart': [{'@type': 'Article', 'headline': x[3][1], 'url': BASE + x[3][0]} for x in QA if x[3]]},
        {'@type': 'FAQPage', 'inLanguage': 'ja', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': __import__('re').sub(r'<[^>]+>', ' ', ''.join(x for x in ps if not x.startswith('<span class="pm-sites"')))}} for pid, q, ps, link in QA]},
        bc_ld(items)]}
    head, hdr, tail = shell(url, h['title'], h['desc'], ld)
    main = ('<main>\n<section class="phero cr-hubp" %s>\n  <div class="wrap">\n    <div class="ph"><h1>就職活動</h1></div>\n    <p class="lead">%s</p>\n    ' + pmap() + '\n  </div>\n</section>\n'
            '%s\n') % (
        STY, h['lead'],
        cta('就職活動について、相談したい方へ', 'インターや海外の大学から日本で働きたい方に、応募の進め方から面接の準備まで、日本語と英語でサポートします'))
    write('column/career', head + hdr + main + tail)

# ---------------------------------------------------------------- topic wheel: four outer segments, internships removed
def seg_path(a0, a1, R=286, r=186, cx=320, cy=320):
    p = lambda rad, a: (cx + rad * math.cos(math.radians(a)), cy + rad * math.sin(math.radians(a)))
    x0, y0 = p(R, a0); x1, y1 = p(R, a1); x2, y2 = p(r, a1); x3, y3 = p(r, a0)
    return 'M%.1f %.1fA%d %d 0 0 1 %.1f %.1fL%.1f %.1fA%d %d 0 0 0 %.1f %.1fZ' % (x0, y0, R, R, x1, y1, x2, y2, r, r, x3, y3)

def wheel(lang):
    en = lang == 'en'
    segs = [  # (center angle, label angle, href, color, title, lines[(text,size)], sub, live)
        (-90, -90, '/column/schools/', 'var(--cp)', 'Choosing a school' if en else 'インターナショナルスクール選び',
         [('Choosing', 19), ('a school', 19)] if en else [('インターナショナル', 18), ('スクール選び', 18)], '', True),
        (0, 0, '/column/curriculum/', 'var(--or)', 'Curricula' if en else 'インターのカリキュラム',
         [('Curricula', 18)] if en else [('インターの', 17), ('カリキュラム', 17)], 'G1–G12' if en else 'G1〜G12', True),
        (90, 90, '/column/university/', '#2f80c9', 'University' if en else '大学進学', [('University', 18)] if en else [('大学進学', 20)], '', True),
        (180, 180, '/column/career/', 'var(--ap)', 'Job hunting' if en else '就職活動', [('Job', 18), ('hunting', 18)] if en else [('就職活動', 19)],
         'Coming soon' if en else '', not en),
    ]
    out = []
    for c, la, href, col, title, lines, sub, live in segs:
        if en:
            href = '/en' + href
        d = seg_path(c - 43.5, c + 43.5)
        tx = 320 + 236 * math.cos(math.radians(la)); ty = 320 + 236 * math.sin(math.radians(la))
        n = len(lines) + (1 if sub else 0)
        y = ty - (n - 1) * 12.5 + 7
        t = ''
        for txt, sz in lines:
            t += '<text x="%.1f" y="%.1f" class="nm" font-size="%d">%s</text>' % (tx, y, sz, txt); y += 25
        if sub:
            t += '<text x="%.1f" y="%.1f" class="st">%s</text>' % (tx, y - 2, sub)
        if live:
            out.append('<a class="gw-seg" href="%s" style="--k:%s"><title>%s</title><path class="bg" d="%s"/>%s</a>' % (href, col, title, d, t))
        else:
            out.append('<g class="gw-seg off" style="--k:%s" aria-label="%s"><path class="bg" d="%s"/>%s</g>' % (col, title + (' (coming soon)' if en else ''), d, t))
    return ''.join(out)

def fix_wheel(path, lang):
    p = os.path.join(ROOT, path)
    s = open(p).read()
    a = s.index('<circle cx="320" cy="320" r="294" fill="#fff"/>') + len('<circle cx="320" cy="320" r="294" fill="#fff"/>')
    b = s.index('<circle cx="320" cy="320" r="166"')
    s = s[:a] + wheel(lang) + s[b:]
    open(p, 'w').write(s)
    print('wheel', path)


HUB_SPLIT_CSS = """<style id="hub-split">
.phero.hubh::before,.phero.hubh::after{display:none!important}
.hub-split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,540px);gap:24px 56px;align-items:center}
.hub-split .ph{margin:0}
.hub-split h1{font-size:clamp(30px,3.4vw,46px)!important;line-height:1.35!important}
.hub-split .hub-wheel .gw{width:100%;max-width:540px;margin:0 auto}
.phero.hubh{padding-bottom:40px!important}
@media (max-width:900px){.hub-split{grid-template-columns:1fr}.hub-split h1{font-size:clamp(24px,6vw,32px)!important}.hub-split .hub-wheel .gw{max-width:460px}}
</style>"""

def split_hub(path):
    p = os.path.join(ROOT, path)
    s = open(p).read()
    if 'class="wrap hub-split"' not in s:
        h0 = s.index('<section class="phero hubh"')
        h1 = s.index('</section>', h0)
        w0 = s.index('<div class="wrap">', h0)
        inner = s[w0 + len('<div class="wrap">'):s.rindex('</div>', w0, h1)]
        t0 = s.index('<section class="sec first" id="topics"')
        t1 = s.index('</section>', t0) + len('</section>')
        g0 = s.index('<p class="gw-tip">', t0)
        g1 = s.index('</svg></div>', t0) + len('</svg></div>')
        wheel_html = s[g0:g1]
        hero = s[h0:w0] + '<div class="wrap hub-split">' + inner.rstrip() + '\n    <div class="hub-wheel">' + wheel_html + '</div>\n  </div>\n'
        s = s[:h0] + hero + s[h1:t0].lstrip('\n') + s[t1:]
        s = s.replace('<div class="gw rise">', '<div class="gw">', 1)
    s = re.sub(r'<style id="hub-split">.*?</style>', '', s, flags=re.S)
    s = s.replace('</head>', HUB_SPLIT_CSS + '\n</head>', 1)
    open(p, 'w').write(s)

def add_gnav():
    n = 0
    for dp, dn, fn in os.walk(os.path.join(ROOT, 'column')):
        for f in fn:
            if f != 'index.html':
                continue
            p = os.path.join(dp, f)
            s = open(p).read()
            t = re.sub(r'<nav class="toc gnav".*?</nav>', lambda m: gnav(m.group(0), '/column/career' in p) if '/column/career' in p else (m.group(0) if '/column/career/' in m.group(0) else m.group(0).replace('</div></nav>', GNAV_CAREER + '</div></nav>')), s, flags=re.S)
            if t != s:
                open(p, 'w').write(t); n += 1
    print('gnav updated', n)

if __name__ == '__main__':
    for a in C.ARTICLES:
        article(a)
    hub()
    fix_wheel('column/index.html', 'ja')
    fix_wheel('en/column/index.html', 'en')
    split_hub('column/index.html')
    split_hub('en/column/index.html')
    add_gnav()
