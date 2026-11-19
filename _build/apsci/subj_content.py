# -*- coding: utf-8 -*-
"""IB / MYP / IGCSE / A Level / Lower Secondary subject pages:
remove 押さえておきたいポイント, and render 学ぶ内容 as a structured, framed layout. Idempotent.
Usage: python3 subj_content.py /home/claude/camino-v2"""
import os, re, sys, glob, html as H
ROOT = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DIRS = ['ib', 'myp', 'igcse', 'a-level', 'lower-secondary']


def top_split(s, seps):
    out, buf, d = [], '', 0
    i = 0
    while i < len(s):
        c = s[i]
        if c in '（(':
            d += 1
        elif c in '）)':
            d = max(0, d - 1)
        hit = None
        if d == 0:
            for sp in seps:
                if s.startswith(sp, i):
                    hit = sp; break
        if hit:
            out.append(buf); buf = ''; i += len(hit); continue
        buf += c; i += 1
    out.append(buf)
    return [x.strip() for x in out if x.strip()]


def is_note(t):
    t2 = re.sub(r'<[^>]+>', '', t)
    return '。' in t2 or t2.endswith('ます') or t2.endswith('です') or t2.endswith('ません')


def head_parts(h):
    h = h.strip()
    m = re.match(r'^(.+?)　(.+)$', h)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r'^(.*?)(（[^）]*）)$', h)
    if m and m.group(1):
        return '', h
    return '', h


def chips(t):
    if is_note(t):
        return None
    for seps in (['／'], ['、'], [', ']):
        parts = top_split(t, seps)
        if len(parts) > 1:
            return parts
    return [t]


def parse(items):
    """items: list of (head, body or None). returns rows, notes"""
    rows, notes = [], []
    for head, body in items:
        if body is None:
            if is_note(head):
                notes.append(head); continue
            rows.append((head, None, None)); continue
        extra = None
        if '。' in body:
            a, b = body.split('。', 1)
            body, extra = a, b.strip()
        c = chips(body)
        if c is None:
            rows.append((head, None, body))
        else:
            rows.append((head, c, None))
        if extra:
            notes.append(extra)
    return rows, notes


def esc_title(t):
    m = re.match(r'^(.*?)(（[^）]*）)$', t)
    if m and m.group(1):
        return '%s<small>%s</small>' % (m.group(1), m.group(2))
    return t


def chip(x):
    m = re.match(r'^(.+?)（(.{12,})）$', x)
    if m:
        return '<li class="slc-w"><b>%s</b><span>%s</span></li>' % (m.group(1), m.group(2))
    return '<li>%s</li>' % x


def render(rows, notes):
    plain = all(c is None and p is None for h, c, p in rows)
    if plain and len(rows) >= 6:
        tiles = ''.join('<li><span class="slc-n">%d</span><b lang="en">%s</b></li>' % (k, esc_title(h)) for k, (h, c, p) in enumerate(rows, 1))
        body = '<div class="slc slc-grid rise"><div class="slc-h"><span>学ぶ内容</span><span>%d分野</span></div><ol class="slc-g">%s</ol></div>' % (len(rows), tiles)
    else:
        out = []
        for k, (h, c, p) in enumerate(rows, 1):
            tag, title = head_parts(h)
            t = ('<span class="slc-tag" lang="en">%s</span>' % tag if tag else '') + '<b>%s</b>' % esc_title(title)
            extra = ''
            if c:
                extra = '<ul class="slc-c">%s</ul>' % ''.join(chip(x) for x in c)
            elif p:
                extra = '<p class="slc-p">%s</p>' % p
            num = '<span class="slc-n">%d</span>' % k if len(rows) > 1 else ''
            out.append('<div class="slc-r%s">%s<div class="slc-b"><div class="slc-t">%s</div>%s</div></div>' % ('' if len(rows) > 1 else ' slc-one', num, t, extra))
        cnt = '<span>%d区分</span>' % len(rows) if len(rows) > 1 else ''
        body = '<div class="slc rise"><div class="slc-h"><span>学ぶ内容</span>%s</div>%s</div>' % (cnt, ''.join(out))
    if notes:
        body += '<ul class="apb rise">%s</ul>' % ''.join('<li>%s</li>' % n for n in notes)
    return body


CSS = '''<style id="slc-css">.slc{margin:6px 0 10px;border:2px solid var(--c,#16294d);background:#fff}
.slc-h{display:flex;justify-content:space-between;background:var(--c,#16294d);color:#fff;padding:10px 16px;font-size:12.5px;font-weight:700}
.slc-r{display:grid;grid-template-columns:40px minmax(0,1fr);gap:14px;padding:14px 16px;border-top:1px solid #dde5f1}
.slc-r:nth-child(even){background:#f6f9fd}
.slc-n{width:34px;height:34px;display:grid;place-items:center;background:#dce9f8;color:var(--c,#16294d);font-weight:800;font-size:14px;font-family:var(--latin)}
.slc-t{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;min-height:34px;align-content:center}
.slc-t b{font-size:15.5px;color:var(--navy,#0b1f4b);line-height:1.45}.slc-t b small{font-size:12px;font-weight:500;color:var(--muted,#5c6984);margin-left:2px}
.slc-tag{font-size:11px;font-weight:800;color:#fff;background:var(--c,#16294d);padding:2px 8px;letter-spacing:.02em}
.slc-c{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.slc-c li{font-size:12.5px;line-height:1.5;color:var(--ink,#1d2b45);background:#fff;border:1px solid #cfdbec;padding:3px 9px}
.slc-r:nth-child(even) .slc-c li{background:#fff}
.slc-one{grid-template-columns:1fr}
.slc-c li.slc-w{flex:1 1 100%;display:grid;grid-template-columns:minmax(110px,auto) 1fr;gap:10px;padding:6px 10px}.slc-w b{font-size:12.5px;color:var(--navy,#0b1f4b)}.slc-w span{font-size:12px;color:var(--muted,#5c6984)}
.slc+.apb{margin-top:14px}
.slc-p{margin:6px 0 0;font-size:13.5px;line-height:1.8;color:var(--ink,#1d2b45)}
.slc-g{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.slc-g li{display:flex;align-items:center;gap:12px;padding:12px 14px;border-top:1px solid #dde5f1;border-left:1px solid #dde5f1;min-width:0}
.slc-g li:nth-child(3n+1){border-left:0}
.slc-g b{font-size:14px;line-height:1.45;color:var(--navy,#0b1f4b);overflow-wrap:anywhere}.slc-g b small{display:block;font-size:11.5px;font-weight:500;color:var(--muted,#5c6984)}
.slc-g .slc-n{flex:none;width:30px;height:30px;font-size:13px}
@media(max-width:760px){.slc-c li.slc-w{grid-template-columns:1fr;gap:2px}.slc-g{grid-template-columns:repeat(2,minmax(0,1fr))}.slc-g li:nth-child(3n+1){border-left:1px solid #dde5f1}.slc-g li:nth-child(2n+1){border-left:0}
.slc-r{grid-template-columns:30px minmax(0,1fr);gap:10px;padding:12px}.slc-n{width:28px;height:28px;font-size:12px}.slc-t b{font-size:14.5px}.slc-g li{padding:10px;gap:8px}.slc-g b{font-size:13px}}
@media(max-width:420px){.slc-g{grid-template-columns:1fr}.slc-g li{border-left:0!important}}</style>
'''


def extract(block):
    m = re.search(r'<ul class="sj-top rise">(.*?)</ul>', block, re.S)
    if m:
        out = []
        for li in re.findall(r'<li>(.*?)</li>', m.group(1), re.S):
            parts = top_split(li, ['：'])
            if len(parts) >= 2:
                out.append((parts[0], '：'.join(parts[1:])))
            else:
                out.append((li, None))
        return out, m.span()
    m = re.search(r'<div class="ewrap rise"><table class="etbl stk">.*?</table></div>', block, re.S)
    if m:
        rows = re.findall(r'<tr><th>(.*?)</th><td[^>]*>(.*?)</td></tr>', m.group(0), re.S)
        if rows:
            return [(h, d) for h, d in rows], m.span()
    return None, None


def renumber(s):
    k = [0]
    def step(m):
        k[0] += 1; return m.group(1) + str(k[0])
    s = re.sub(r'(<div class="step" id="[a-z]+"><span class="step-n">)\d+', step, s)
    nav = re.search(r'<nav[^>]*class="otl"[^>]*>.*?</nav>', s, re.S)
    if nav:
        k2 = [0]
        def toc(m):
            k2[0] += 1; return m.group(1) + str(k2[0])
        n2 = re.sub(r'(<li(?: class="[^"]*")?><a href="#[a-z]+"><span>)\d+', toc, nav.group(0))
        s = s[:nav.start()] + n2 + s[nav.end():]
    return s


n = 0
for d in DIRS:
    for f in sorted(glob.glob(os.path.join(ROOT, 'subjects', d, '*', 'index.html'))):
        s = open(f, encoding='utf-8').read(); o = s
        i = s.find('<div class="step" id="point">')
        if i >= 0:
            ends = [x for x in (s.find('<div class="step"', i + 10), s.find('<!--mjreq-->', i)) if x > 0]
            s = s[:i] + s[min(ends):]
            s = re.sub(r'<li><a href="#point"><span>\d+</span>[^<]*</a></li>', '', s)
        i = s.find('<div class="step" id="content">')
        if i >= 0 and 'class="slc' not in s:
            j = s.find('</div></div>', i) + len('</div></div>')
            ends = [x for x in (s.find('<div class="step"', j), s.find('<!--mjreq-->', j)) if x > 0]
            k = min(ends)
            items, span = extract(s[j:k])
            if items:
                rows, notes = parse(items)
                s = s[:j + span[0]] + render(rows, notes) + s[j + span[1]:]
        if 'class="slc' in s:
            s = (re.sub(r'<style id="slc-css">.*?</style>\n', lambda m: CSS, s, count=1, flags=re.S) if '<style id="slc-css">' in s else s.replace('</head>', CSS + '</head>', 1))
        s = renumber(s)
        if s != o:
            open(f, 'w', encoding='utf-8').write(s); n += 1
print('updated', n)
