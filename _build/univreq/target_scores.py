# -*- coding: utf-8 -*-
"""Inject a '目的別：何点あれば十分か' section into the TOEFL and IELTS explainer pages,
computed from the US/UK top-100 requirement data. Idempotent (<!--target-->...<!--/target-->).
Usage: python3 target_scores.py /home/claude/camino-v2"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import analysis_html as A
from statistics import median
ROOT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/camino-v2'
REQ = '/column/university/us-uk-requirements/'
TESTS = '/column/university/sat-english-tests/'
NOTE_SKIP = ('目安', '推奨', '最低点ではない')

import math
def f(x, dec=True):
    if x is None: return '—'
    if not dec: return '%d' % round(x)
    if abs(x * 2 - round(x * 2)) < 1e-9: return '%.1f' % x
    lo = math.floor(x * 2) / 2; hi = math.ceil(x * 2) / 2
    return '%.1f〜%.1f' % (lo, hi)

def us_split(lo, hi, getter, rng):
    mins, tg = [], []
    for d in A.US:
        if not (lo <= d['rank'] <= hi): continue
        s = getter(d)
        if not s: continue
        v = A.nums(s, *rng)
        if not v: continue
        note = d.get('note') or ''
        if A.is_min(s) and not any(w in note for w in NOTE_SKIP):
            mins.append(v[0])
            m = re.search(r'推奨\s*([\d.]+)', s)
            if m: tg.append(float(m.group(1)))
        else:
            tg.append(v[0])
    return mins, tg

def m(v): return median(v) if v else None
def rng_txt(v, dec=True):
    if not v: return ''
    lo, hi = min(v), max(v)
    return '' if lo == hi else '<small class="tg-n">大学により%s〜%s</small>' % (f(lo, dec), f(hi, dec))

US_B = [('アメリカ 1〜30位', 1, 30), ('アメリカ 31〜50位', 31, 50), ('アメリカ 51〜100位', 51, 100)]

def toefl_rows():
    rows = []
    for name, lo, hi in US_B:
        nm, nt = us_split(lo, hi, lambda d: (d.get('toefl') or (None, None))[1], (1, 6))
        om, ot = us_split(lo, hi, lambda d: (d.get('toefl') or (None, None))[0], (60, 120))
        rows.append((name, nm, nt, om, ot))
    return rows

def ielts_rows():
    rows = []
    for name, lo, hi in US_B:
        mi, tg = us_split(lo, hi, lambda d: d.get('ielts'), (4, 9))
        rows.append((name, mi, tg))
    uk = []
    for name, lo, hi in [('イギリス 1〜10位', 1, 10), ('イギリス 11〜30位', 11, 30), ('イギリス 31〜100位', 31, 100)]:
        v = [(A.iel(d['ielts']), d['ielts']) for d in A.UK if lo <= d['rank'] <= hi and A.iel(d['ielts'])]
        comp = [float(x) for _, s in v for x in re.findall(r'各([\d.]+)', s)]
        uk.append((name, [x[0] for x in v], comp))
    return rows, uk

def cell(label, val, n):
    return '<td data-l="%s"><b>%s</b>%s</td>' % (label, val, ('<small class="tg-n">%d校</small>' % n) if n else '')

def toefl_block(step):
    rows = toefl_rows()
    trs = []
    for name, nm, nt, om, ot in rows:
        trs.append('<tr><th>%s</th>%s%s</tr>' % (
            name,
            cell('出願できる最低ライン（中央値）', '新TOEFL %s<br>旧スコア %s' % (f(m(nm)), f(m(om), False)), len(nm) + len(om)),
            cell('合格者の水準・大学の目安（中央値）', '新TOEFL %s<br>旧スコア %s' % (f(m(nt)), f(m(ot), False)) if len(nt) + len(ot) >= 3 else '大学ごとに確認', len(nt) + len(ot))))
    top = rows[0]; low = rows[2]
    body = ('<p class="tg-lead">「何点あれば十分か」は、志望校によって変わります。<a href="%s">アメリカ・イギリスの上位100大学の出願要件</a>を集計すると、目安は次のとおりです。'
            '「最低ライン」は大学が定める出願の基準、「合格者の水準」は合格者に多い点数や大学が勧める点数です</p>' % REQ
            + '<div class="ewrap rise"><table class="etbl stk tg-t"><thead><tr><th>志望校</th><th>出願できる最低ライン（中央値）</th><th>合格者の水準・大学の目安（中央値）</th></tr></thead><tbody>'
            + ''.join(trs) + '</tbody></table></div>'
            + '<ul class="ul2 tg-ul">'
            '<li><b>アメリカの上位30校</b>：最低点を超えるだけでは足りません。合格者の水準は<b>新TOEFL %s・旧スコア%s前後</b>です</li>'
            '<li><b>アメリカの51〜100位</b>：多くは<b>新TOEFL %s・旧スコア%s</b>で出願の基準を満たします</li>'
            '<li><b>イギリスの大学</b>：英語の基準はIELTSで示されることが多く、TOEFLの扱いは大学ごとに異なります。オックスフォード大学のように、2026年1月21日以降に受けた新しいTOEFLを、審査中として受け付けていない大学もあります</li>'
            '<li><b>インターに通っている場合</b>：英語で授業を行う学校に在籍していれば、英語試験が免除される大学もあります。ただし州立大学を中心に、日本のインターでは免除されない大学も少なくありません。<a href="%s">免除の条件の傾向</a>を確認してください</li></ul>'
            % (f(m(top[2])), f(m(top[4]), False), f(m(low[1])), f(m(low[3]), False), TESTS))
    return block(step, 'target', '目的別：何点あれば十分か', 'アメリカの上位100大学の要件から集計（2027年秋入学）', body)

def ielts_block(step):
    us, uk = ielts_rows()
    trs = []
    for name, mi, tg in us:
        trs.append('<tr><th>%s</th>%s%s</tr>' % (name, cell('出願できる最低ライン（中央値）', 'IELTS %s' % f(m(mi)), len(mi)),
                                                 cell('合格者の水準・目安／各技能', 'IELTS %s%s' % (f(m(tg)), rng_txt(tg)) if len(tg) >= 3 else '大学ごとに確認', len(tg))))
    for name, v, comp in uk:
        trs.append('<tr><th>%s<small>経済学部</small></th>%s%s</tr>' % (name, cell('出願できる最低ライン（中央値）', 'IELTS %s%s' % (f(m(v)), rng_txt(v)), len(v)),
                                                                 cell('合格者の水準・目安／各技能', '各技能 %s以上が中心' % f(m(comp)) if comp else '大学ごとに確認', 0)))
    usr = us; ukr = uk
    body = ('<p class="tg-lead">「何点あれば十分か」は、志望校によって変わります。<a href="%s">アメリカ・イギリスの上位100大学の出願要件</a>を集計すると、目安は次のとおりです。'
            'イギリスは経済学部の要件です。「最低ライン」は大学が定める出願の基準、「合格者の水準」は合格者に多い点数や大学が勧める点数です</p>' % REQ
            + '<div class="ewrap rise"><table class="etbl stk tg-t"><thead><tr><th>志望校</th><th>出願できる最低ライン（中央値）</th><th>合格者の水準・目安／各技能</th></tr></thead><tbody>'
            + ''.join(trs) + '</tbody></table></div>'
            + '<ul class="ul2 tg-ul">'
            '<li><b>イギリスの大学</b>：上位10校は<b>%s以上</b>、11〜30位は<b>%s</b>、31〜100位は<b>%s</b>が中心です。総合点に加えて、<b>各技能（Listening・Reading・Writing・Speaking）の最低点</b>も決められているので、苦手な技能を残さないことが大切です</li>'
            '<li><b>アメリカの大学</b>：同じ点数でも、イギリスより基準が高い傾向があります。上位30校を目指すなら<b>IELTS %s</b>が目安です</li>'
            '<li><b>両国を併願する場合</b>：IELTS 7.0〜7.5を目標にすると、どちらの上位校にも対応しやすくなります</li>'
            '<li><b>インターに通っている場合</b>：英語試験が免除される大学もありますが、条件は大学ごとに違います。<a href="%s">免除の条件の傾向</a>を確認してください</li></ul>'
            % (f(m(ukr[0][1])), f(m(ukr[1][1])), f(m(ukr[2][1])), f(m(usr[0][2])), TESTS))
    return block(step, 'target', '目的別：何点あれば十分か', 'アメリカ・イギリスの上位100大学の要件から集計（2027年秋入学）', body)

def block(step, sid, h3, sub, body):
    return ('<!--target--><div class="step" id="%s"><span class="step-n">%d</span><div><h3>%s</h3><p class="step-sub">%s</p></div></div>\n%s<!--/target-->'
            % (sid, step, h3, sub, body))

CSS = ('<style id="target-css">.tg-lead{font-size:15px;line-height:1.95;margin:0 0 14px}.tg-lead a,.ul2 a{color:var(--c);font-weight:700}'
       '.tg-t td b{font-size:15px;color:var(--navy,#0b1f4b)}.tg-t small.tg-n{display:block;font-size:11px;color:var(--muted,#5c6984);font-weight:500;margin-top:2px}'
       '.tg-ul{margin-top:18px}.tg-t th small{display:block;font-size:11px;font-weight:500;color:var(--muted,#5c6984)}</style>\n')

def inject(path, html, step, label):
    f_ = os.path.join(ROOT, path, 'index.html')
    s = open(f_, encoding='utf-8').read()
    s = re.sub(r'<!--target-->.*?<!--/target-->\n?', '', s, flags=re.S)
    s = re.sub(r'<style id="target-css">.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'<li><a href="#target">.*?</li>', '', s)
    anchor = '\n  </div>\n</section>\n<section class="sec" id="faq">'
    assert s.count(anchor) == 1, path
    s = s.replace(anchor, '\n' + html + anchor)
    toc_end = s.index('</ol></nav>', s.index('<nav class="otl"'))
    s = s[:toc_end] + '<li><a href="#target"><span>%d</span>%s</a></li>' % (step, label) + s[toc_end:]
    s = s.replace('</head>', CSS + '</head>', 1)
    open(f_, 'w', encoding='utf-8').write(s)
    print('injected', path)

def acs(kind):
    import acs_eng as AE
    v = AE.verified()
    if kind == 'toefl':
        rows = [[d['ja'] + '<br><small>%s</small>' % AE.CN[d['c']], d['toefl'], d['new'] or '—'] for d in v]
        head = ['大学', 'TOEFL（0〜120）', '新TOEFL（1〜6）']
        txt = ('オーストラリア・カナダ・シンガポールの主要15校では、TOEFL（0〜120）の最低点は80〜93で、中心は90です。新しいTOEFL（1〜6）は、基準を示している大学の多くが4.5（シンガポール経営大学は5.0）です。'
               'ニューサウスウェールズ大学は新形式を当面受け付けておらず、シドニー大学はTOEFLのオーストラリア向けの版のみを認めています')
    else:
        rows = [[d['ja'] + '<br><small>%s</small>' % AE.CN[d['c']], d['ielts']] for d in v]
        head = ['大学', 'IELTS（アカデミック）']
        txt = ('オーストラリア・カナダ・シンガポールの主要15校では、公表している13校のうち12校がIELTSの最低点を6.5（多くは各技能6.0以上）にしています。'
               'シンガポール経営大学は7.0、ニューサウスウェールズ大学の経営・法学も7.0で、学部によって上がる場合があります')
    c, n = AE.counts()
    txt2 = ('日本のインター生は、英語で学んだ学歴やIBの英語の成績で試験が不要になる大学も多くあります。大学ごとの条件は<a href="%s">SAT・英語試験はどのくらい必要？</a>へ' % TESTS)
    return ('<p class="tg-lead" style="margin-top:22px"><b>オーストラリア・カナダ・シンガポールでは</b>　' + txt + '</p>'
            + '<div class="rq-t rq-mj">' + A_table(head, rows) + '</div><p class="tg-lead">' + txt2 + '</p>')

def A_table(head, rows):
    sys.path.insert(0, os.path.join(HERE, '..', 'subj'))
    sys.argv = [sys.argv[0], ROOT]
    import common as M
    return M.C.table(head, rows)

if __name__ == '__main__':
    inject('column/english/toefl', toefl_block(8).replace('<!--/target-->', acs('toefl') + '<!--/target-->'), 8, '目的別の目標スコア')
    inject('column/english/ielts', ielts_block(7).replace('<!--/target-->', acs('ielts') + '<!--/target-->'), 7, '目的別の目標スコア')
