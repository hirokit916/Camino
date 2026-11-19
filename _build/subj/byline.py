"""Add an author byline (small round photo + one-line credentials) to the top right
of every article hero, and an inline Person author to the page's JSON-LD.

Idempotent: the HTML block sits between <!--byline--> markers and the CSS in
<style id="byline-css">, both replaced on every run.

Usage: python3 byline.py /home/claude/camino-v2
Run after build_subjects / build_services / integrate / seo_titles.
"""
import json, os, re, sys

ROOT = sys.argv[1]
SECTIONS = ['ib', 'curriculum', 'column', 'subjects', 'en/ib', 'en/column', 'en/curriculum']
# listing pages that only link to articles: no byline
HUBS = {'column', 'en/column', 'subjects', 'subjects/ib', 'subjects/igcse', 'subjects/a-level',
        'subjects/ap', 'subjects/middle-school'}
# column category pages (lists of articles): no byline either
for _h in ['career', 'curriculum', 'english', 'schools', 'schools/kansai', 'schools/kanto', 'university']:
    HUBS.add('column/' + _h)
    HUBS.add('en/column/' + _h)

PHOTO = '/img/author.jpg'
JA = dict(href='/#profile', label='執筆者 高島 宏樹のプロフィール', role='執筆', name='高島 宏樹',
          desc=['Canadian Academy卒', 'IB取得', 'UCL修了', '米国教員資格'])
EN = dict(href='/en/#profile', label='About the author, Hiroki Takashima', role='WRITTEN BY',
          name='Hiroki Takashima', desc=['Canadian Academy alum', 'IB Diploma', 'UCL', 'US teaching certification'])

CSS = '''<style id="byline-css">
.bl-row{width:100%;max-width:none!important;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px;margin-bottom:24px}
.bl-row .crumb{margin-bottom:0}
.byline{margin-left:auto;display:inline-flex;align-items:center;gap:13px;text-decoration:none;color:var(--navy,#0b1f4b);line-height:1.3}
.byline img{width:48px;height:48px;border-radius:50%;object-fit:cover;flex:none;display:block;border:2px solid #fff;box-shadow:0 0 0 1px rgba(11,31,75,.14),0 6px 16px rgba(11,31,75,.14)}
.byline span{display:flex;flex-direction:column;gap:2px;min-width:0;padding-left:13px;border-left:1px solid rgba(11,31,75,.16)}
.byline i{font-style:normal;font-size:10px;font-weight:600;letter-spacing:.22em;color:var(--muted,#5c6984)}
.byline b{font-family:var(--serif,'Shippori Mincho',serif);font-size:16px;font-weight:600;letter-spacing:.06em;color:var(--navy,#0b1f4b)}
.byline small{display:block;overflow:hidden;font-size:11px;color:var(--soft,#3f4b66);letter-spacing:.02em}
.byline small s{display:flex;flex-wrap:wrap;margin-left:-1.2em;text-decoration:none}
.byline small em{font-style:normal;white-space:nowrap;margin-left:1.2em;position:relative}
.byline small em::before{content:"";position:absolute;left:-.62em;top:.32em;width:1px;height:.85em;background:currentColor;opacity:.3}
.byline:hover b{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.byline:focus-visible{outline:2px solid var(--navy,#0b1f4b);outline-offset:4px;border-radius:6px}
@media (min-width:1180px){body.has-side .ahero .bl-row{width:calc(100% + 280px);margin-right:-280px}}
@media (max-width:640px){.bl-row{margin-bottom:18px}.byline{gap:10px}.byline img{width:40px;height:40px}.byline span{padding-left:10px}.byline b{font-size:14.5px}.byline small{font-size:10.5px}}
</style>'''


def block(t):
    creds = ''.join('<em>%s</em>' % c for c in t['desc'])
    return ('<!--byline--><a class="byline" href="%s" aria-label="%s">'
            '<img src="%s" alt="" width="48" height="48" loading="lazy" decoding="async">'
            '<span><i>%s</i><b>%s</b><small><s>%s</s></small></span></a><!--/byline-->'
            % (t['href'], t['label'], PHOTO, t['role'], t['name'], creds))


def person(en):
    return {
        '@type': 'Person',
        '@id': 'https://caminotutor.com/#founder',
        'name': 'Hiroki Takashima' if en else '高島 宏樹',
        'alternateName': '高島 宏樹' if en else 'Hiroki Takashima',
        'url': 'https://caminotutor.com/en/#profile' if en else 'https://caminotutor.com/#profile',
        'image': 'https://caminotutor.com' + PHOTO,
        'alumniOf': [
            {'@type': 'EducationalOrganization', 'name': 'Canadian Academy'},
            {'@type': 'CollegeOrUniversity', 'name': 'University College London'},
        ],
    }


def fix_ld(s, en):
    def rep(m):
        d = json.loads(m.group(1))
        items = d.get('@graph', [d]) if isinstance(d, dict) else d
        changed = False
        for it in items:
            if it.get('@type') in ('Article', 'WebPage', 'TechArticle', 'BlogPosting', 'CollectionPage'):
                if it.get('@type') == 'CollectionPage':
                    continue
                it['author'] = person(en)
                changed = True
        if not changed:
            return m.group(0)
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, indent=2) + '</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', rep, s, flags=re.S)


def add_block(s, en):
    # remove a previous run
    s = re.sub(r'(\n    )?<div class="bl-row">(<div class="crumb">.*?</div>)?<!--byline-->.*?<!--/byline--></div>',
               lambda m: ((m.group(1) or '') + m.group(2)) if m.group(2) else '', s, flags=re.S)
    h = re.search(r'<section class="(phero|ahero)[^"]*"[^>]*>\s*<div class="wrap">', s)
    if not h:
        return s, False
    b = block(EN if en else JA)
    after = s[h.end():]
    c = re.match(r'(\s*)(<div class="crumb">.*?</div>)', after, flags=re.S)
    if c:
        new = c.group(1) + '<div class="bl-row">' + c.group(2) + b + '</div>' + after[c.end():]
    else:
        new = '\n    <div class="bl-row">' + b + '</div>' + after
    return s[:h.end()] + new, True


def add_css(s):
    s = re.sub(r'<style id="byline-css">.*?</style>\n', '', s, flags=re.S)
    return s.replace('</head>', CSS + '\n</head>', 1)


done, skipped = 0, []
for sec in SECTIONS:
    for dp, _, fs in os.walk(os.path.join(ROOT, sec)):
        if 'index.html' not in fs:
            continue
        rel = os.path.relpath(dp, ROOT)
        f = os.path.join(dp, 'index.html')
        if rel in HUBS:
            s = open(f, encoding='utf-8').read()
            s2 = re.sub(r'(\n    )?<div class="bl-row">(<div class="crumb">.*?</div>)?<!--byline-->.*?<!--/byline--></div>',
                        lambda m: ((m.group(1) or '') + m.group(2)) if m.group(2) else '', s, flags=re.S)
            s2 = re.sub(r'<style id="byline-css">.*?</style>\n', '', s2, flags=re.S)
            if s2 != s:
                open(f, 'w', encoding='utf-8').write(s2)
            continue
        s = open(f, encoding='utf-8').read()
        en = rel.startswith('en/')
        s2, ok = add_block(s, en)
        if not ok:
            skipped.append(rel)
            continue
        s2 = add_css(s2)
        s2 = fix_ld(s2, en)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2)
        done += 1
print('byline pages:', done)
if skipped:
    print('no hero found:', skipped)
