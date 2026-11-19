# -*- coding: utf-8 -*-
"""Inject '大学の基準と比べると' (step 2) into the IB scores / A Level results pages.
Aggregate only: no school names, no ranking. Idempotent (<!--cmp-->...<!--/cmp-->).
Usage: python3 results_compare.py /home/claude/camino-v2"""
import os, re, sys
from statistics import median
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_split as B
SS, A, AN = B.SS, B.A, B.AN
ROOT = sys.argv[1]

def step(h3, sub):
    return '<div class="step" id="compare"><span class="step-n">2</span><div><h3>%s</h3><p class="step-sub">%s</p></div></div>' % (h3, sub)

def uni_meds(kind, cty, keys):
    return [v for v, n in (B.uni_med(kind, cty, k) for k in keys) if v is not None and n >= 3]

def band_range(lo, hi, f):
    v = [B.band_med(m, lo, hi, f)[0] for m, _ in B.MAJ]
    v = [x for x in v if x]
    return min(v), max(v)

def ib_block(s):
    sch = [float(x) for x in re.findall(r'<td data-l="平均点" class="s">([\d.]+)点</td>', s)]
    wavg = re.search(r'<em>IB（DP）</em>([\d.]+)点（(\d{4})年）', s)
    uk10 = uni_meds('ib', 'UK', [k for k in SS.UNIS if SS.RANK[k] <= 10])
    au = uni_meds('ib', 'AU', [k for k, _ in A.UNI['AU']])
    mc = B.uni_med('ib', 'CA', 'McGill')[0]
    b2 = band_range(11, 30, B.ib_uk); b3 = band_range(31, 50, B.ib_uk)
    lo, hi = 24, 45
    def pos(v): return (v - lo) / (hi - lo) * 100
    rows = [('掲載校の平均点', '各校が公表している平均点（%d校）' % len(sch), min(sch), max(sch), median(sch), 'sch'),
            ('イギリス上位10校', '大学ごとの12学部の中央値', min(uk10), max(uk10), None, 'ref'),
            ('イギリス11〜30位', '学部ごとの中央値の範囲', b2[0], b2[1], None, 'ref'),
            ('イギリス31〜50位', '学部ごとの中央値の範囲', b3[0], b3[1], None, 'ref'),
            ('オーストラリア上位5校', '大学ごとの12学部の中央値', min(au), max(au), None, 'ref'),
            ('カナダ（マギル大学）', '12学部の中央値', mc, mc, None, 'ref')]
    if wavg: rows.append(('世界平均（%s年）' % wavg.group(2), 'IB公式発表', float(wavg.group(1)), float(wavg.group(1)), None, 'w'))
    html = []
    for lab, sub, a, b, md, cls in rows:
        dots = ''.join('<i class="cr-dot" style="left:%.1f%%"></i>' % pos(v) for v in sch) if cls == 'sch' else ''
        if cls == 'ref':
            bar = ('<span class="cr-ext" style="left:%.1f%%;width:%.1f%%"></span><span class="cr-bar cr-ref" style="left:%.1f%%;width:%.1f%%"></span>'
                   % (pos(a), 100 - pos(a), pos(a), max(pos(b) - pos(a), 1.2)))
            val = ('%s〜%s点<small>以上が条件</small>' % (AN.fmt(a), AN.fmt(b))) if a != b else '%s点<small>以上が条件</small>' % AN.fmt(a)
        else:
            bar = '<span class="cr-bar cr-%s" style="left:%.1f%%;width:%.1f%%"></span>' % (cls, pos(a), max(pos(b) - pos(a), 1.2))
            val = ('%s〜%s点' % (AN.fmt(a), AN.fmt(b))) if a != b else '%s点' % AN.fmt(a)
        if md is not None: val += '<small>中央値 %s点</small>' % AN.fmt(md)
        html.append('<div class="cr-row"><span class="cr-l">%s<small>%s</small></span><span class="cr-t">%s%s</span><span class="cr-v">%s</span></div>' % (lab, sub, bar, dots, val))
    axis = '<div class="cr-row cr-ax"><span></span><span class="cr-t">%s</span><span></span></div>' % ''.join('<em style="left:%.1f%%">%d</em>' % (pos(v), v) for v in (24, 30, 35, 40, 45))
    fig = ('<figure class="vz rise"><figcaption><b>国内インターの平均点と、各国の大学が求める最低ライン</b><small>大学の数字は合格に必要な条件（最低ライン）で、濃い部分がその範囲、薄い部分は「それ以上」を表します。出典は<a href="%s">国際バカロレア（IB）は何点必要？</a>。掲載校の点は各校の平均点（学校名は省略）</small></figcaption>%s%s</figure>'
           % (B.SCORES, ''.join(html), axis))
    n_au = sum(1 for v in sch if v >= max(au)); n_uk = sum(1 for v in sch if v >= min(uk10))
    txt = ('<div class="cr-warn"><b>この比べ方で気をつけたいこと</b><ul>'
           '<li>大学の数字は<b>最低ライン</b>です。この点数を取れば合格できるわけではありません。イギリスの上位校では、条件を満たしたうえで、面接や入学試験、志望理由書などで選考されます</li>'
           '<li>学校の<b>平均点</b>は、一人ひとりの点数とは違います。平均点が最低ラインを超えていても、その学校の生徒の多くが条件を満たすという意味にはなりません</li>'
           '<li>最低ラインと比べるのは、自分の<b>予想点（Predicted Grades）</b>です。イギリスの上位校では、総合点に加えてHLの科目ごとの点数も条件になることが多くあります</li></ul></div>'
           '<p class="cr-p">掲載%d校の平均点は%s〜%s点（中央値%s点）、IBの世界平均は%s点です。志望する大学と学部の最低ラインは、<a href="%s">国際バカロレア（IB）は何点必要？</a>と学部別の記事で確認してください</p>'
           % (len(sch), AN.fmt(min(sch)), AN.fmt(max(sch)), AN.fmt(median(sch)), wavg.group(1) if wavg else '—', B.SCORES))
    return step('大学の基準と比べると', '各国の大学が求める最低ラインと、各校の平均点') + fig + txt

def al_block(s):
    rows = re.findall(r'<tr><th[^>]*>.*?</th>(.*?)</tr>', s[s.find('<tbody'):s.find('</tbody>')], flags=re.S)
    aa = []
    for r in rows:
        pass
    aa = [float(x) for x in re.findall(r'data-l="A\*〜A"[^>]*>([\d.]+)%', s)]
    uk10 = uni_meds('al', 'UK', [k for k in SS.UNIS if SS.RANK[k] <= 10])
    b3 = band_range(31, 50, B.tar)
    def g(v): return B.gname(v)
    tbl = B.C.table(['大学', '最低ライン（3科目の条件）', '集計の方法'],
                    [['イギリス上位10校', '%s〜%s' % (g(min(uk10)), g(max(uk10))), '大学ごとの12学部の中央値'],
                     ['イギリス31〜50位', '%s〜%s' % (g(b3[0]), g(b3[1])), '学部ごとの中央値の範囲'],
                     ['カナダ（マギル大学）', g(B.uni_med('al', 'CA', 'McGill')[0]), '12学部の中央値'],
                     ['オーストラリア（ニューサウスウェールズ大学）', g(B.uni_med('al', 'AU', 'UNSW')[0]), '12学部の中央値']])
    txt = ('<div class="cr-warn"><b>この比べ方で気をつけたいこと</b><ul>'
           '<li>大学の成績は<b>最低ライン</b>です。この成績を取れば合格できるわけではなく、イギリスの上位校では、条件を満たしたうえで面接や入学試験、志望理由書などで選考されます</li>'
           '<li>掲載校のA*〜Aの割合（%s〜%s%%）は、科目ごとの成績を合わせた数字です。3科目すべてで条件を満たした生徒の割合とは一致しません</li>'
           '<li>最低ラインと比べるのは、自分の<b>予想成績（Predicted Grades）</b>です</li></ul></div>'
           '<p class="cr-p">志望する大学と学部の最低ラインは、<a href="%s">A Levelは何点必要？</a>と学部別の記事で確認してください</p>'
           % (AN.fmt(min(aa)), AN.fmt(max(aa)), B.SCORES_AL)) if aa else ''
    return step('大学の基準と比べると', 'イギリス・カナダ・オーストラリアの大学が、A Levelで求める成績') + '<div class="rise">' + tbl + '</div>' + txt

CSS = ('<style id="cr-css">.cr-row{display:grid;grid-template-columns:170px 1fr 120px;gap:12px;align-items:center;padding:7px 0;border-top:1px dashed var(--line,#e3e7f0)}'
       '.cr-row:first-of-type{border-top:0}.cr-l{font-size:13px;font-weight:700;color:var(--navy,#0b1f4b);line-height:1.4}.cr-l small{display:block;font-size:10.5px;font-weight:500;color:var(--muted,#5c6984)}'
       '.cr-t{position:relative;height:14px;background:#eef1f7;border-radius:7px}.cr-bar{position:absolute;top:0;height:14px;border-radius:7px;background:#5598e7}.cr-bar.cr-sch{background:#c9dbf6}.cr-bar.cr-w{background:#9aa3b2}'
       '.cr-dot{position:absolute;top:2px;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#184f95;border:2px solid #fff;box-sizing:border-box}'
       '.cr-v{font-size:13px;font-weight:700;color:var(--navy,#0b1f4b)}.cr-v small{display:block;font-size:10.5px;font-weight:500;color:var(--muted,#5c6984)}'
       '.cr-ax{border-top:0;padding-top:0}.cr-ax .cr-t{background:none;height:16px}.cr-ax em{position:absolute;transform:translateX(-50%);font-style:normal;font-size:10.5px;color:var(--muted,#5c6984)}'
       '.cr-ext{position:absolute;top:0;height:14px;border-radius:0 7px 7px 0;background:linear-gradient(90deg,#c9dbf6,rgba(201,219,246,.15))}.cr-warn{background:#fff;border:1px solid var(--line,#d9deea);border-left:4px solid #eb6834;border-radius:0 10px 10px 0;padding:14px 18px;margin:16px 0 0;font-size:14px;line-height:1.85}.cr-warn>b{display:block;color:var(--navy,#0b1f4b);margin-bottom:4px}.cr-warn ul{margin:0;padding-left:1.2em}.cr-warn li{margin:4px 0}'
       '.cr-p{font-size:14.5px;line-height:1.9;margin:14px 0 26px}.cr-p a,.vz figcaption small a{color:var(--c,#16294d);font-weight:700}'
       '@media(max-width:760px){.cr-row{grid-template-columns:96px 1fr 70px;gap:8px}.cr-l{font-size:11.5px}.cr-v{font-size:11.5px}}</style>\n')

def inject(rel, fn):
    f = os.path.join(ROOT, rel, 'index.html'); s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!--cmp-->.*?<!--/cmp-->\n?', '', s, flags=re.S)
    s = re.sub(r'<style id="cr-css">.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'<li><a href="#compare">.*?</li>', '', s)
    html = fn(s)
    # insert after the results step's content: before the closing of the section that holds #results
    i = s.index('<div class="step" id="results">')
    j = s.index('\n  </div>\n</section>', i)
    s = s[:j] + '\n<!--cmp-->' + html + '<!--/cmp-->\n' + s[j:]
    s = s.replace('<span>1</span>各校が公表している結果</a></li></ol></nav>', '<span>1</span>各校が公表している結果</a></li><li><a href="#compare"><span>2</span>大学の基準と比べると</a></li></ol></nav>')
    need = '.vz{' not in s
    s = s.replace('</head>', ('<style>' + AN.CSS + '</style>\n' if need else '') + CSS + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s); print('ok', rel)

if __name__ == '__main__':
    inject('column/university/ib-scores', ib_block)
    inject('column/university/a-level-results', al_block)
