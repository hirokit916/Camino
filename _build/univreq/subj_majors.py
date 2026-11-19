# -*- coding: utf-8 -*-
"""Inject '大学の学部では、この科目はどのくらい求められる？' into subject pages (IB / A Level / AP).
Idempotent (<!--mjreq-->...<!--/mjreq-->). Usage: python3 subj_majors.py /home/claude/camino-v2"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_split as B
SS, A, USJ, AN, SJ = B.SS, B.A, B.USJ, B.AN, B.SJ
ROOT = sys.argv[1]

AL = {'mathematics-9709': ('MATH', '数学'), 'further-mathematics-9231': ('FM', '更なる数学（Further Mathematics）'), 'physics-9702': ('PHY', '物理'),
      'chemistry-9701': ('CHEM', '化学'), 'biology-9700': ('BIO', '生物'), 'history-9489': ('HIST', '歴史'), 'literature-in-english-9695': ('ENG', '英文学')}
IB = {'mathematics-analysis-and-approaches': ('MATH', '数学'), 'mathematics-applications-and-interpretation': ('MATH', '数学'), 'physics': ('PHY', '物理'),
      'chemistry': ('CHEM', '化学'), 'biology': ('BIO', '生物'), 'history': ('HIST', '歴史'),
      'english-a-literature': ('ENG', '英語・英文学'), 'english-a-language-and-literature': ('ENG', '英語・英文学')}
AP = {'calculus-ab': '数学', 'calculus-bc': '数学', 'physics-1': '物理', 'physics-c-mechanics': '物理', 'chemistry': '化学', 'biology': '生物'}

def classify(s, t):
    hard, opt, none = SS.req_parse(s)
    if t in hard: return 'H'
    if any(t in g for g in opt) or (t in B.SCI and '理系' in s): return 'O'
    return '-'
def uk_counts(m, t):
    rows = B.uk_rows(m)
    if m == 'ECON':
        if t != 'MATH': return None
        al = [r for k, r in rows if r.get('al')]
        return (sum(1 for r in al if '数学' in r['al']), 0, len(al))
    rq = [r['req'] for k, r in rows if r.get('req') is not None]
    c = [classify(s, t) for s in rq]
    return (c.count('H'), c.count('O'), len(rq))
def acs_counts(m, t):
    rq = [r['req'] for c, k, r in B.acs_rows(m) if r.get('req') is not None]
    c = [classify(s, t) for s in rq]
    return (c.count('H'), c.count('O'), len(rq))

NONE = '--mjn'
def bars(cap, sub, legend, rows):
    """rows: (label, sublabel, [(name, count, var, ink)], total) ; total 0 -> no data."""
    out = []
    for lab, sl, parts, n in rows:
        if not n:
            out.append('<div class="vz-row"><span class="vz-lab">%s<small>%s</small></span><div class="vz-bar mjq-na">確認できたデータなし</div></div>' % (lab, sl)); continue
        plain = re.sub('<[^>]+>', '', lab)
        row = AN.seg_bar(plain, sl, [(str(i), nm, c, v, ink) for i, (nm, c, v, ink) in enumerate(parts)], n)
        out.append(row.replace('<span class="vz-lab">%s<small>' % plain, '<span class="vz-lab">%s<small>' % lab, 1))
    return ('<figure class="vz mjq-f"><figcaption><b>%s</b><small>%s</small></figcaption>%s<div class="vz-rows">%s</div></figure>'
            % (cap, sub, AN.legend(legend), ''.join(out)))

def rank_lead(stats, subj):
    """stats: (ja, h, o, n). Lists majors with the highest required share, then those where it is one option."""
    st = [x for x in stats if x[3]]
    req = sorted([x for x in st if x[1]], key=lambda x: (-x[1] / x[3], -x[2] / x[3]))
    opt = sorted([x for x in st if x[2] and (x[1] + x[2]) / x[3] >= 0.3 and (x[1] / x[3]) < 0.5], key=lambda x: -(x[1] + x[2]) / x[3])
    parts = []
    if req:
        parts.append('%sを必須にしている大学の割合が高い学部は、%sです' % (subj, '、'.join('%s（%d%%）' % (j, B.pct(h, n)) for j, h, o, n in req[:3])))
    else:
        parts.append('確認できた範囲では、%sを必須にしている学部はありません' % subj)
    opt = [x for x in opt if x not in req[:3]]
    if opt:
        parts.append('%sでは、ほかの科目と選べる条件の1つとして求められることが多くあります' % '、'.join('%s（%d%%）' % (j, B.pct(h + o, n)) for j, h, o, n in opt[:3]))
    none = [j for j, h, o, n in st if not h and not o]
    if none:
        parts.append('%sでは求められていません' % '・'.join(none))
    return '<p class="mjq-p">' + '。'.join(parts) + '。'

def sort_rows(rows, stats):
    keyed = list(zip(rows, stats))
    keyed.sort(key=lambda r: (0 if r[1][3] else 1, -(r[1][1] / r[1][3]) if r[1][3] else 0, -((r[1][1] + r[1][2]) / r[1][3]) if r[1][3] else 0))
    return [r for r, s in keyed]

LEG3 = [('必須', '--vo1'), ('選択肢の1つ', '--vo3'), ('求めていない', NONE)]
def uk_fig(t, subj, sub):
    rows, stats = [], []
    for m, ja in B.MAJ:
        r = uk_counts(m, t)
        name = '<a href="%s">%s</a>' % (B.mpath(m), ja)
        if r is None:
            continue
        h, o, n = r; stats.append((ja, h, o, n))
        rows.append((name, '%d校' % n, [('必須', h, '--vo1', 'w'), ('選択肢の1つ', o, '--vo3', 'k'), ('求めていない', n - h - o, NONE, 'k')], n))
    fig = bars('%sを求める大学の割合が高い学部の順' % subj, sub, LEG3, sort_rows(rows, stats))
    return fig, stats

UKSUB = 'イギリス上位50校（the Complete University Guide 2027）のA Levelの必須科目。各学部の大学を100%とした内訳で、必須の割合が高い学部から順に並べています。「選択肢の1つ」は「化学か生物」「理系から1科目」のように、ほかの科目と選べる条件。経済学は、オファーに数学の記載がある大学の割合のみ'
def uk_block(t, subj, step, curriculum):
    fig, stats = uk_fig(t, subj, UKSUB)
    lead = rank_lead(stats, subj) + '学部ごとの成績と必須科目は<a href="%s">A Levelは何点必要？</a>で比べられます</p>' % B.SCORES_AL
    return wrap(step, '大学の学部で、%sはどのくらい求められる？' % subj, 'イギリス上位50校×12学部の入学要件から集計（2027年入学）', fig + lead)

def ib_block(t, subj, step):
    rows, stats = [], []
    for m, ja in B.MAJ:
        name = '<a href="%s">%s</a>' % (B.mpath(m), ja)
        h, o, n = acs_counts(m, t)
        u = uk_counts(m, t)
        ref = ('参考：イギリスのA Levelで必須 %d%%' % B.pct(u[0], u[2])) if u and u[2] else ''
        stats.append((ja, h, o, n))
        rows.append((name, ('%d校' % n if n else '') + (' ／ ' + ref if ref and n else ref), [('必須', h, '--vo1', 'w'), ('選択肢の1つ', o, '--vo3', 'k'), ('求めていない', n - h - o, NONE, 'k')], n))
    fig = bars('%sを求める大学の割合が高い学部の順' % subj,
               'オーストラリア・カナダ・シンガポールの主要大学がIBの出願者に課す科目条件（確認できた大学のみ）。各学部の大学を100%とした内訳で、必須の割合が高い学部から順に並べています。HLかSLかの指定は大学により異なります。参考として、イギリス上位50校がA Levelで同じ科目を必須にしている割合を添えています', LEG3, sort_rows(rows, stats))
    lead = rank_lead(stats, 'IBの' + subj) + '学部ごとの成績と必須科目は<a href="%s">国際バカロレア（IB）は何点必要？</a>で比べられます</p>' % B.SCORES
    return wrap(step, '大学の学部で、%sはどのくらい求められる？' % subj, 'オーストラリア・カナダ・シンガポールの主要大学と、イギリス上位50校の要件から集計', fig + lead)

APT = {'calculus-ab': 'MATH', 'calculus-bc': 'MATH', 'physics-1': 'PHY', 'physics-c-mechanics': 'PHY', 'chemistry': 'CHEM', 'biology': 'BIO'}
def ap_block(w, step, slug):
    t = APT[slug]
    fig, stats = uk_fig(t, w, UKSUB.replace('A Levelの必須科目。', 'A Levelで課す必須科目（APで出願する場合の科目条件の目安）。'))
    extra = ''
    if slug in ('calculus-bc', 'physics-c-mechanics', 'calculus-ab', 'physics-1'):
        extra = '<p class="mjq-p">イギリスのケンブリッジ大学は、数学・更なる数学が必要なコースにはCalculus BC、物理が必要なコースにはPhysics C（2科目）を推奨しています</p>'
    lead = rank_lead(stats, w) + '学部ごとの成績と必須科目は<a href="%s">A Levelは何点必要？</a>で比べられます</p>' % B.SCORES_AL
    return wrap(step, '大学の学部で、%sはどのくらい求められる？' % w, 'イギリス上位50校×12学部の入学要件から集計（2027年入学）', fig + lead + extra)

def wrap(step, h3, sub, body):
    return (('<!--mjreq--><div class="step" id="majors"><span class="step-n">%d</span><div><h3>%s</h3><p class="step-sub">%s</p></div></div>\n<div class="mjq rise">%s</div>' % (step, h3, sub, body)) + AN.JS + '<!--/mjreq-->\n')

CSS = ('<style id="mjq-css">' + AN.CSS.replace('<style>', '').replace('</style>', '') + SJ.CSS +
       '.mjq{margin:6px 0 30px;--mjn:#e3e7ee}.mjq .vz-bar{min-height:30px}.mjq-na{display:flex;align-items:center;padding:0 10px;font-size:12px;color:var(--muted,#5c6984);background:#f4f6f9}.mjq .vz-lab a{color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}.mjq .vz{margin:0}.hz.mjq{min-width:0;max-width:640px}.hz.mjq th small{display:block;font-size:10.5px;font-weight:500;color:var(--muted,#5c6984)}'
       '.hz.mjq th a{color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}'
       '.mjq-p{font-size:14.5px;line-height:1.9;margin:14px 0 0}.mjq-p a{color:var(--c);font-weight:700}'
       '@media(max-width:760px){.hz.mjq tbody th{min-width:7.6em;word-break:keep-all}}</style>\n')

def renumber(s):
    k = [0]
    def st(m):
        k[0] += 1; return m.group(1) + str(k[0])
    s = re.sub(r'(<div class="step" id="[a-z]+"><span class="step-n">)\d+', st, s)
    nav = re.search(r'<nav[^>]*class="otl"[^>]*>.*?</nav>', s, re.S)
    if nav:
        k2 = [0]
        def toc(m):
            k2[0] += 1; return m.group(1) + str(k2[0])
        s = s[:nav.start()] + re.sub(r'(<li(?: class="[^"]*")?><a href="#[a-z]+"><span>)\d+', toc, nav.group(0)) + s[nav.end():]
    return s

def inject(rel, html):
    """Insert/replace the majors section right before the tutoring section, then renumber sections and TOC."""
    f = os.path.join(ROOT, rel, 'index.html'); s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!--mjreq-->.*?<!--/mjreq-->\n?', '', s, flags=re.S)
    s = re.sub(r'<li><a href="#majors"><span>\d+</span>[^<]*</a></li>', '', s)
    anchor = re.search(r'<div class="step" id="camino">', s)
    assert anchor, rel
    s = s[:anchor.start()] + html + s[anchor.start():]
    s = re.sub(r'(<li(?: class="[^"]*")?><a href="#camino">)', r'<li><a href="#majors"><span>0</span>大学の学部で求められる度合い</a></li>\1', s, count=1)
    if '<style id="mjq-css">' in s:
        s = re.sub(r'<style id="mjq-css">.*?</style>\n', lambda m: CSS, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', CSS + '</head>', 1)
    s = renumber(s)
    open(f, 'w', encoding='utf-8').write(s)
    print('ok', rel)

if __name__ == '__main__':
    for slug, (t, subj) in AL.items(): inject('subjects/a-level/' + slug, uk_block(t, subj, 4, 'A Level'))
    for slug, (t, subj) in IB.items(): inject('subjects/ib/' + slug, ib_block(t, subj, 4))
    for slug, w in AP.items(): inject('subjects/ap/' + slug, ap_block(w, 4, slug))
