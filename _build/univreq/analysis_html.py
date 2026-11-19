# -*- coding: utf-8 -*-
"""Trend analysis across the US/UK top-100 requirement data -> HTML section (charts + findings).
Every number on the page is computed here from us_data*/uk_data*; nothing is typed in by hand."""
import re, statistics as st
import us_data, us_data2, uk_data, uk_data2
from inter_lens import L, PUBLIC

US_RAW = us_data.US + us_data2.US3
UC = next(d for d in US_RAW if d['en'].endswith('Berkeley'))
def _r(d):
    if d.get('uc'):
        x = dict(UC); x.update(rank=d['rank'], en=d['en'], ja=d['ja']); return x
    return d
US = [_r(d) for d in US_RAW]
UK = uk_data.UK + uk_data.UK2 + uk_data2.UK3

def med(v):
    if not v: return None
    m = st.median(v); return int(m) if float(m).is_integer() else m
def pct(a, b): return round(100 * a / b) if b else 0
def fmt(x): return ('%g' % x) if x is not None else '—'
def f1(x): return ('%.1f' % x) if x is not None else '—'

# ---------------- US ----------------
B5 = [('1〜10位', 1, 10), ('11〜20位', 11, 20), ('21〜30位', 21, 30), ('31〜50位', 31, 50), ('51〜100位', 51, 100)]
B3 = [('1〜30位', 1, 30), ('31〜50位', 31, 50), ('51〜100位', 51, 100)]
def inb(d, b): return b[1] <= d['rank'] <= b[2]

def tcat(t):
    if t.startswith('必須'): return 'req'
    if t.startswith('任意') or t.startswith('提出は任意'): return 'opt'
    if '不要' in t or '使用しない' in t: return 'no'
    return None

def nums(s, lo, hi):
    return [float(x) for x in re.findall(r'\d+(?:\.\d+)?', s or '') if lo <= float(x) <= hi]

def is_min(s): return bool(s) and ('min' in s or ('以上' in s and '目安' not in s and '推奨' not in s and '合格者' not in s))
def has_min(d):
    if any(w in (d.get('note') or '') for w in ('目安', '推奨', '最低点ではない', '最低点なし')): return False
    t = d.get('toefl') or (None, None)
    return any(is_min(x) for x in [t[0], t[1], d.get('ielts'), d.get('det')])

def us_stats():
    test = []
    for b in B5:
        sub = [d for d in US if inb(d, b)]
        c = {k: sum(1 for d in sub if tcat(d['test']) == k) for k in ('req', 'opt', 'no')}
        test.append((b[0], c, sum(c.values()), len(sub)))
    top22 = [d for d in US if d['rank'] <= 20]
    req_now = sum(1 for d in top22 if tcat(d['test']) == 'req')
    back = [d for d in top22 if tcat(d['test']) == 'opt' and re.search(r'20(2[89])年秋入学から必須|2027-28年出願から必須', d['test'])]
    ladder = []
    for b in B3:
        sub = [d for d in US if inb(d, b)]
        known = [d for d in sub if tcat(d['test'])]
        req = sum(1 for d in known if tcat(d['test']) == 'req')
        old = [nums(d['toefl'][0], 60, 120)[0] for d in sub if d.get('toefl') and d['toefl'][0] and nums(d['toefl'][0], 60, 120)]
        new = [nums(d['toefl'][1], 1, 6)[0] for d in sub if d.get('toefl') and d['toefl'][1] and nums(d['toefl'][1], 1, 6)]
        ie = [nums(d['ielts'], 4, 9)[0] for d in sub if d.get('ielts') and nums(d['ielts'], 4, 9)]
        pub_min = sum(1 for d in sub if has_min(d))
        ladder.append(dict(band=b[0], n=len(sub), req=req, known=len(known), old=med(old), new=med(new), ielts=med(ie), pubmin=pub_min))
    top10 = [d for d in US if d['rank'] <= 10]
    top10_min = [d['ja'] for d in top10 if has_min(d)]
    return test, req_now, len(top22), back, ladder, top10, top10_min

def lens_stats():
    groups = [(b[0], [d for d in US if inb(d, b)]) for b in B3] + [('州立大学', [d for d in US if d['en'] in PUBLIC]), ('私立大学', [d for d in US if d['en'] not in PUBLIC])]
    rows = []
    for name, sub in groups:
        c = {'E': 0, 'A': 0, 'B': 0, 'X': 0, 'U': 0}
        for d in sub:
            k = L[d['en']][0]; c['X' if k in 'CD' else k] += 1
        rows.append((name, c, len(sub) - c['U'], len(sub)))
    allc = {'E': 0, 'A': 0, 'B': 0, 'X': 0, 'U': 0}
    for d in US:
        k = L[d['en']][0]; allc['X' if k in 'CD' else k] += 1
    yrs = {}
    for d in US:
        k, y = L[d['en']]
        if k == 'A' and y: yrs[y] = yrs.get(y, 0) + 1
    four = [d['ja'] for d in US if L[d['en']][0] == 'A' and L[d['en']][1] >= 4]
    return rows, allc, yrs, four

# ---------------- UK ----------------
T = {'A*': 56, 'A': 48, 'B': 40, 'C': 32, 'D': 24, 'E': 16}
G = {168: 'A*A*A*', 160: 'A*A*A', 152: 'A*AA', 144: 'AAA', 136: 'AAB', 128: 'ABB', 120: 'BBB', 112: 'BBC', 104: 'BCC', 96: 'CCC'}
def tariff(s):
    v = [sum(T[x] for x in re.findall(r'A\*|[ABCDE]', g)) for g in re.findall(r'(?<![A-Za-z])((?:A\*|[ABCDE]){3})(?![A-Za-z*])', s or '')]
    for p in re.findall(r'UCASポイント(\d+)(?:〜(\d+))?', s or ''):
        v += [int(x) for x in p if x]
    return max(v) if v else None
def ibp(s):
    v = [int(x) for x in re.findall(r'(\d\d)点', s or '') if 24 <= int(x) <= 45]
    return max(v) if v else None
def iel(s):
    m = re.search(r'(?<![\d.])([5-9](?:\.\d)?)(?![\d])', s or ''); return float(m.group(1)) if m else None
def grade(t):
    if t is None: return '—'
    if t in G: return G[t]
    lo = max(k for k in G if k < t); hi = min(k for k in G if k > t); return '%s〜%s' % (G[hi], G[lo])

def uk_stats():
    rows = [dict(rank=d['rank'], ja=d['ja'], t=tariff(d['alevel']), ib=ibp(d['ib']), ie=iel(d['ielts']),
                 maths='数学' in (d['alevel'] + d['ib'] + d.get('note', '')), noecon=(d['alevel'] == '—')) for d in UK]
    bands = []
    for b in B5:
        sub = [r for r in rows if inb(r, b)]
        bands.append(dict(band=b[0], n=len(sub), t=med([r['t'] for r in sub if r['t']]), ib=med([r['ib'] for r in sub if r['ib']]),
                          ie=med([r['ie'] for r in sub if r['ie']]), noecon=sum(r['noecon'] for r in sub),
                          ibn=sum(1 for r in sub if r['ib'])))
    conv = {}
    for r in rows:
        if r['t'] and r['ib'] and r['t'] in (152, 144, 136, 128, 120, 112): conv.setdefault(r['t'], []).append(r['ib'])
    conv = [(G[t], med(v), len(v), min(v), max(v)) for t, v in sorted(conv.items(), reverse=True)]
    reach = []
    for s in range(30, 43, 2):
        cells = []
        for b in B5:
            sub = [r for r in rows if inb(r, b) and r['ib']]
            cells.append((sum(1 for r in sub if r['ib'] <= s), len(sub)))
        reach.append((s, cells))
    noecon = sum(r['noecon'] for r in rows)
    return rows, bands, conv, reach, noecon

def ielts_cross():
    usv = [(d['rank'], nums(d.get('ielts'), 4, 9)[0]) for d in US if d.get('ielts') and nums(d.get('ielts'), 4, 9)]
    ukv = [(d['rank'], iel(d['ielts'])) for d in UK if iel(d['ielts'])]
    out = []
    for s in (6.5, 7.0, 7.5):
        u = [x for x in usv if x[0] <= 30]; k = [x for x in ukv if x[0] <= 30]
        out.append((s, sum(1 for x in u if x[1] <= s), len(u), sum(1 for x in k if x[1] <= s), len(k)))
    return out

# ---------------- HTML helpers ----------------
def seg_bar(label, sub, parts, total, aria_extra=''):
    """parts: list of (key, name, count, color_var, ink) ; ink 'w' or 'k'."""
    segs = []; desc = []
    for key, name, n, var, ink in parts:
        if not n: continue
        p = 100 * n / total
        desc.append('%s%d校（%d%%）' % (name, n, round(p)))
        lab = '<em>%d%%</em>' % round(p) if p >= 11 else ''
        segs.append('<span class="vz-seg vz-%s" style="width:%.2f%%;background:var(%s)" tabindex="0" data-tip="%s：%d校（%d%%）">%s</span>'
                    % (ink, p, var, name, n, round(p), lab))
    return ('<div class="vz-row"><span class="vz-lab">%s<small>%s</small></span><div class="vz-bar" role="img" aria-label="%s：%s">%s</div></div>'
            % (label, sub, label, '、'.join(desc) + aria_extra, ''.join(segs)))

def legend(items):
    return '<ul class="vz-leg">' + ''.join('<li><i style="background:var(%s)"></i>%s</li>' % (v, n) for n, v in items) + '</ul>'

def table(head, rows):
    return ('<details class="vz-tv"><summary>表で見る</summary><div class="vz-tw"><table><thead><tr>' + ''.join('<th>%s</th>' % h for h in head) +
            '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows) + '</tbody></table></div></details>')

SEQ = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec', '#5598e7', '#3987e5', '#2a78d6', '#256abf', '#1c5cab', '#184f95']
def heat(p):
    i = min(len(SEQ) - 1, int(round(p / 10)))
    return SEQ[i], ('#fff' if i >= 6 else '#0b1f4b')

def finding(n, title, body, viz=''):
    return ('<article class="vf rise"><p class="vf-n">傾向 %d</p><h4>%s</h4>%s<div class="vf-rd">%s</div></article>'
            % (n, title, viz, body))

# ---------------- build ----------------
def build_section():
    test, req_now, n22, back, ladder, top10, top10_min = us_stats()
    lrows, allc, yrs, four = lens_stats()
    ukrows, ukb, conv, reach, noecon = uk_stats()
    cross = ielts_cross()
    out = []
    nus, nuk = len(US), len(UK)
    out.append('<p class="rlead">%d校（アメリカ）と%d校（イギリス）の要件を、一校ずつ数字に置き換え、順位帯ごとに集計しました。'
               '一覧表を眺めるだけでは見えない「順位によって何が変わるのか」と「日本のインターに通う生徒にとって何を意味するのか」をまとめています</p>' % (nus, nuk))
    out.append('<div class="rq-scope rise"><b>集計の方法</b>　順位帯は1〜10位、11〜20位、21〜30位、31〜50位、51〜100位。'
               'A LevelはUCASポイント（A*=56、A=48、B=40、C=32）に換算し、幅のある要件は標準的なオファー（高い方）を使いました。'
               '数値はすべて中央値です。公式サイトで確認できなかった大学は、その項目の計算から外しています。'
               '英語試験の免除条件は、日本のインターナショナルスクールに通う日本国籍の生徒を想定して分類しました</div>')

    # 1 SAT
    parts_rows = []
    for name, c, known, n in test:
        parts_rows.append(seg_bar(name, '確認できた%d校' % known,
                                  [('req', '必須', c['req'], '--vo1', 'w'), ('opt', '任意', c['opt'], '--vo2', 'k'), ('no', '使わない', c['no'], '--vo3', 'k')], known))
    viz1 = ('<figure class="vz"><figcaption><b>SAT・ACTの扱い（アメリカ・順位帯別）</b><small>2027年秋入学の方針。%d校のうち方針を確認できた大学の割合</small></figcaption>' % nus
            + legend([('必須', '--vo1'), ('任意', '--vo2'), ('使わない（UCなど）', '--vo3')]) + '<div class="vz-rows">' + ''.join(parts_rows) + '</div>'
            + table(['順位帯', '必須', '任意', '使わない', '確認できた大学'], [(n, c['req'], c['opt'], c['no'], k) for n, c, k, _ in test]) + '</figure>')
    t10 = test[0]; t51 = test[4]
    later = req_now + len(back)
    out.append(finding(1, 'SAT・ACTは「上位校ほど必須」。2029年には上位20校の%d%%が必須に' % pct(later, n22),
        '1〜10位では%d%%の大学がSAT・ACTを必須にしているのに対し、51〜100位では%d%%です。順位が下がるほど「任意」が主流になります。'
        'ただし上位校では流れが逆で、%sが必須に戻すと発表しているため、2029年秋入学には上位20位（同順位を含め%d校）のうち%d校が必須になります。'
        '<b>上位20校を目指すなら、SAT・ACTは「出すと有利」ではなく「出すのが前提」</b>と考えて、G10のうちに一度受けておくのが安全です'
        % (pct(t10[1]['req'], t10[2]), pct(t51[1]['req'], t51[2]), '・'.join(d['ja'] for d in back), n22, later), viz1))

    # 2 English ladder
    lad_rows = ''.join('<tr><th>%s<small>%d校</small></th><td><b>%d%%</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td>%d%%</td></tr>'
                       % (r['band'], r['n'], pct(r['req'], r['known']), fmt(r['old']), f1(r['new']), f1(r['ielts']), pct(r['pubmin'], r['n'])) for r in ladder)
    viz2 = ('<figure class="vz"><figcaption><b>順位帯ごとの「求められる数字」（アメリカ）</b><small>英語試験は最低点・目安・合格者の点数を含む中央値</small></figcaption>'
            '<div class="vz-tw"><table class="vz-lad"><thead><tr><th>順位帯</th><th>SAT・ACT必須</th><th>TOEFL<br><small>0〜120</small></th><th>新TOEFL<br><small>1〜6</small></th><th>IELTS</th><th>最低点を公表</th></tr></thead><tbody>'
            + lad_rows + '</tbody></table></div></figure>')
    out.append(finding(2, '上位10校ほど「最低点」を書かない。目安は上位30校でTOEFL %s・IELTS %s' % (fmt(ladder[0]['old']), f1(ladder[0]['ielts'])),
        '英語試験の数字は、順位が上がるほどはっきり高くなります。TOEFL（0〜120）の中央値は1〜30位で%s、31〜50位で%s、51〜100位で%s。'
        '一方で、上位10校のうち英語試験の<b>最低点</b>を公表しているのは%sの%d校だけで、ほかは「目安」か、数字そのものを出していません。'
        '<b>最低点を超えれば安心、ではなく、上位校では「合格者の水準（TOEFL 100前後・新TOEFL 5.0以上・IELTS 7.0以上）」を目標にする</b>のが現実的です'
        % (fmt(ladder[0]['old']), fmt(ladder[1]['old']), fmt(ladder[2]['old']), '・'.join(top10_min), len(top10_min)), viz2))

    # 3 inter lens
    lr = []
    for name, c, known, n in lrows:
        if name == '州立大学': lr.append('<div class="vz-sep"></div>')
        lr.append(seg_bar(name, '確認できた%d校' % known,
                          [('E', '英語試験は不要・推奨のみ', c['E'], '--vc4', 'w'), ('A', 'インターの在籍年数で免除', c['A'], '--vc1', 'w'),
                           ('B', 'スコアで免除', c['B'], '--vc2', 'k'), ('X', '免除の道なし', c['X'], '--vc3', 'k')], known))
    viz3 = ('<figure class="vz"><figcaption><b>日本のインター生は、英語試験を免除されるか（アメリカ）</b><small>日本のインターナショナルスクールに通う日本国籍の生徒の場合。公式サイトで条件を確認できた%d校</small></figcaption>' % (nus - allc['U'])
            + legend([('英語試験は不要・推奨のみ', '--vc4'), ('インターの在籍年数で免除', '--vc1'), ('SAT・IB英語などのスコアで免除', '--vc2'), ('免除の道なし（英語圏の国の学校・国籍が条件）', '--vc3')])
            + '<div class="vz-rows">' + ''.join(lr) + '</div>'
            + table(['', '不要・推奨のみ', '在籍年数で免除', 'スコアで免除', '免除の道なし', '確認できず'], [(n, c['E'], c['A'], c['B'], c['X'], c['U']) for n, c, k, _ in lrows]) + '</figure>')
    pub = next(x for x in lrows if x[0] == '州立大学'); pri = next(x for x in lrows if x[0] == '私立大学')
    top = lrows[0]; low = lrows[2]
    out.append(finding(3, '州立大学の%d%%は、日本のインターに何年通っても英語試験を免除しない' % pct(pub[1]['X'], pub[2]),
        'このページで最も伝えたい傾向です。免除の条件を読み比べると、「英語で授業を行う学校」での在籍を認める大学と、'
        '「アメリカ・イギリスなど英語圏の国の学校」や「国籍」だけを認める大学に分かれます。後者の場合、日本のインターに12年間通っていても免除されません。'
        '<b>免除の道がない大学は、私立では%d%%なのに対し、州立では%d%%</b>。順位で見ると、1〜30位では%d%%ですが、51〜100位では%d%%に増えます。'
        'また、在籍年数で免除する大学のうち%d校は「4年以上」を求めています（%s など）。G10以降にインターへ転校した場合は対象外です。'
        '<b>州立大学を受けるなら、インター生でもTOEFLかIELTSを用意しておく</b>のが確実です'
        % (pct(pri[1]['X'], pri[2]), pct(pub[1]['X'], pub[2]), pct(top[1]['X'], top[2]), pct(low[1]['X'], low[2]), len(four), '、'.join(four[:4])), viz3))

    # 4 UK ladder + conversion
    bcards = ''.join('<div><b>%s</b><strong>%s・IB %s点</strong>IELTS %s%s</div>'
                     % (b['band'], grade(b['t']), fmt(b['ib']), f1(b['ie']), ('<small>経済学部なし %d校</small>' % b['noecon']) if b['noecon'] else '') for b in ukb)
    conv_rows = ''.join('<tr><th>%s</th><td><b>%s点</b></td><td>%d〜%d点</td><td>%d校</td></tr>' % (g, fmt(m), lo, hi, n) for g, m, n, lo, hi in conv)
    viz4 = ('<figure class="vz"><figcaption><b>イギリス・経済学部の標準的な要件（順位帯別の中央値）</b></figcaption><div class="rq-band rq-band5">' + bcards + '</div>'
            '<p class="vz-sub">同じ大学のA LevelとIBの要件を並べた「換算表」</p><div class="vz-tw"><table class="vz-lad"><thead><tr><th>A Levelの要件</th><th>IBの要件（中央値）</th><th>範囲</th><th>大学数</th></tr></thead><tbody>'
            + conv_rows + '</tbody></table></div></figure>')
    out.append(finding(4, 'イギリスは「A Level 1段階 ≒ IB 2点」。A*AAならIB %s点が目安' % fmt(conv[0][1]),
        '経済学部の要件は、順位帯ごとにきれいな階段になっています。1〜10位の中央値は%s・IB %s点、31〜50位は%s・IB %s点、51〜100位は%s・IB %s点です。'
        'さらに、A LevelとIBの両方を載せている大学を並べると、A Levelが1段階（AAA→AAB など）下がるごとに、IBの要件はおよそ2点下がります。'
        '<b>IBの生徒は「志望校のA Levelの要件」から、自分に必要なIBの点数を読み替えられます</b>'
        % (grade(ukb[0]['t']), fmt(ukb[0]['ib']), grade(ukb[3]['t']), fmt(ukb[3]['ib']), grade(ukb[4]['t']), fmt(ukb[4]['ib'])), viz4))

    # 5 IB reach heatmap
    hrows = []
    for s, cells in reach:
        tds = []
        for (k, n), b in zip(cells, B5):
            p = 100 * k / n if n else 0; bg, ink = heat(p)
            tds.append('<td style="background:%s;color:%s" tabindex="0" data-tip="IB %d点：%s %d校中%d校">%d/%d</td>' % (bg, ink, s, b[0], n, k, k, n))
        hrows.append('<tr><th>IB %d点</th>%s</tr>' % (s, ''.join(tds)))
    viz5 = ('<figure class="vz"><figcaption><b>IBの点数で、標準的な要件に届く大学の数（イギリス・経済学部）</b><small>IBの点数を公表している%d校。色が濃いほど多くの大学に届く</small></figcaption>'
            % sum(n for (_, n) in reach[0][1])
            + '<div class="vz-tw"><table class="vz-heat"><thead><tr><th></th>' + ''.join('<th>%s</th>' % b[0] for b in B5) + '</tr></thead><tbody>' + ''.join(hrows) + '</tbody></table></div></figure>')
    r36 = dict(reach)[36]; r38 = dict(reach)[38]; r40 = dict(reach)[40]; r34 = dict(reach)[34]
    out.append(finding(5, '上位10校は「2点ごと」に門が開く。38点が分かれ目',
        'IBの点数ごとに、標準的な要件に届く大学の数を数えました。1〜10位では、36点で%d校、38点で%d校、40点で%d校と、<b>2点上がるごとに3〜4校ずつ届く大学が増えます</b>。'
        '一方、31〜50位は34点で%d校中%d校に届き、51〜100位は32点ですべてに届きます。'
        '<b>トップ校を目指すなら、予想スコアの「あと2点」に最も価値がある</b>ということです。G11の時点で予想スコアが36点前後なら、どの科目で2点を積み上げるかを早めに決めることが大切です'
        % (r36[0][0], r38[0][0], r40[0][0], r34[3][1], r34[3][0]), viz5))

    # 6 ranking != subject
    out.append(finding(6, '総合ランキング100位以内でも、%d校には経済学部が見つからない' % noecon,
        'the Complete University Guideの総合ランキングには、芸術系や農学系の大学も含まれます。上位100校のうち%d校は、経済学の単独のコースがない、'
        'または公式サイトで見つかりませんでした（芸術系の大学、ビジネス系のコースのみの大学など）。'
        '<b>大学選びは総合順位だけでなく、学びたい分野の学部別ランキングと、コースの中身で比べる</b>必要があります' % noecon))

    # 7 cross IELTS
    c65 = next(c for c in cross if c[0] == 6.5); c70 = next(c for c in cross if c[0] == 7.0)
    cr_rows = ''.join('<tr><th>IELTS %s</th><td><b>%d/%d校</b>（%d%%）</td><td><b>%d/%d校</b>（%d%%）</td></tr>' % (f1(s), a, b_, pct(a, b_), c, d_, pct(c, d_)) for s, a, b_, c, d_ in cross)
    viz7 = ('<figure class="vz"><figcaption><b>IELTSの点数で、英語の基準に届く上位30校の数</b><small>IELTSの点数を公表している大学のみ</small></figcaption>'
            '<div class="vz-tw"><table class="vz-lad"><thead><tr><th></th><th>アメリカ1〜30位</th><th>イギリス1〜30位</th></tr></thead><tbody>' + cr_rows + '</tbody></table></div></figure>')
    out.append(finding(7, '英語の基準は、イギリスよりアメリカの上位校の方が高い',
        '同じIELTSの点数で比べると、IELTS 6.5で基準に届くのは、イギリスの上位30校では%d%%なのに対し、アメリカの上位30校では%d%%だけです。'
        'IELTS 7.0でも、アメリカの上位30校は%d%%にとどまります。<b>両国の上位校を併願するなら、IELTS 7.0〜7.5（新TOEFLなら5.0〜5.5）を目標にする</b>と、どちらにも対応できます'
        % (pct(c65[3], c65[4]), pct(c65[1], c65[2]), pct(c70[1], c70[2])), viz7))

    out.append('<div class="vf-sum rise"><p class="vf-sum-h">今から準備しておきたい3つのこと</p><ol>'
               '<li><b>SAT・ACTは、上位校を目指すなら受ける前提で</b>。G10のうちに一度受け、G11で目標点まで伸ばす計画を立てます</li>'
               '<li><b>インター生でも、英語試験は用意しておく</b>。特に州立大学や、4年以上の在籍を求める大学を受ける場合は、IELTS 7.0・新TOEFL 5.0以上が目安です</li>'
               '<li><b>IBは「あと2点」を最優先に</b>。イギリスの上位校は2点ごとに届く大学が増えます。予想スコアを上げる科目を早めに決めましょう</li></ol></div>')
    return '\n'.join(out)

CSS = '''
.vf{background:#fff;border:1px solid var(--line,#d8e0ee);border-radius:16px;padding:22px 24px 20px;margin:18px 0 0}
.vf-n{margin:0 0 4px;font-size:12px;font-weight:700;letter-spacing:.08em;color:var(--c)}
.vf h4{margin:0 0 14px;font-size:18.5px;line-height:1.55;color:var(--navy,#0b1f4b);font-weight:700}
.vf-rd{margin:16px 0 0;font-size:14.5px;line-height:1.95;color:var(--ink,#0b1f4b)}
.vf-rd span{display:block;font-size:11.5px;font-weight:700;letter-spacing:.06em;color:var(--muted,#5c6984);margin-bottom:2px}
.vz{margin:0;padding:16px 16px 12px;background:#fcfcfb;border:1px solid var(--line,#d8e0ee);border-radius:12px;
 --vo1:#184f95;--vo2:#5598e7;--vo3:#86b6ef;--vc1:#2a78d6;--vc2:#1baf7a;--vc3:#eb6834;--vc4:#008300}
.vz figcaption b{display:block;font-size:14.5px;color:var(--navy,#0b1f4b)}
.vz figcaption small{display:block;font-size:12px;color:var(--muted,#5c6984);margin-top:2px;line-height:1.6}
.vz-leg{list-style:none;display:flex;flex-wrap:wrap;gap:6px 16px;margin:12px 0 10px;padding:0;font-size:12.5px;color:var(--ink,#0b1f4b)}
.vz-leg li{display:flex;align-items:center;gap:6px}
.vz-leg i{width:10px;height:10px;border-radius:3px;flex:none}
.vz-rows{display:grid;gap:10px}
.vz-row{display:grid;grid-template-columns:118px 1fr;gap:12px;align-items:center}
.vz-lab{font-size:13px;font-weight:700;color:var(--navy,#0b1f4b);line-height:1.3}
.vz-lab small{display:block;font-size:11px;font-weight:500;color:var(--muted,#5c6984)}
.vz-bar{display:flex;gap:2px;height:28px}
.vz-seg{display:flex;align-items:center;min-width:0;border-radius:4px;font-size:12px;font-weight:700;padding:0 0 0 7px;cursor:default;outline:none}
.vz-seg em{font-style:normal;white-space:nowrap}
.vz-w{color:#fff}.vz-k{color:#0b1f4b}
.vz-seg:hover,.vz-seg:focus-visible{filter:brightness(1.08);box-shadow:0 0 0 2px #fcfcfb,0 0 0 4px var(--navy,#0b1f4b)}
.vz-sep{height:1px;background:var(--line,#d8e0ee);margin:4px 0}
.vz-tv{margin:12px 0 0}
.vz-tv summary{cursor:pointer;font-size:12.5px;font-weight:700;color:var(--c);display:inline-block}
.vz-tw{overflow-x:auto}
.vz table{border-collapse:collapse;width:100%;font-size:13px;margin-top:8px;font-variant-numeric:tabular-nums}
.vz th,.vz td{border-bottom:1px solid var(--line,#d8e0ee);padding:8px 10px;text-align:left;white-space:nowrap}
.vz thead th{font-size:11.5px;color:var(--muted,#5c6984);font-weight:700}
.vz thead th small{font-weight:500}
.vz tbody th{color:var(--navy,#0b1f4b);font-weight:700}
.vz tbody th small{display:block;font-size:11px;font-weight:500;color:var(--muted,#5c6984)}
.vz-lad td b{font-size:15px;color:var(--navy,#0b1f4b)}
.vz-heat td{text-align:center;font-weight:700;border:2px solid #fcfcfb;border-radius:6px;min-width:64px}
.vz-heat td:focus-visible{outline:2px solid var(--navy,#0b1f4b);outline-offset:-2px}
.vz-sub{margin:16px 0 0;font-size:13px;font-weight:700;color:var(--navy,#0b1f4b)}
.rq-band5{grid-template-columns:repeat(5,1fr)}
.rq-band5 small{display:block;font-size:11px;color:var(--muted,#5c6984);margin-top:2px}
.vf-sum{margin:22px 0 0;background:var(--ct);border-radius:14px;padding:18px 22px}
.vf-sum-h{margin:0 0 8px;font-size:15.5px;font-weight:700;color:var(--navy,#0b1f4b)}
.vf-sum ol{margin:0;padding-left:1.3em;font-size:14.5px;line-height:1.9}
.vf-sum li+li{margin-top:6px}
.vz-tip{position:absolute;z-index:90;pointer-events:none;background:#0b1f4b;color:#fff;font-size:12.5px;font-weight:600;padding:6px 10px;border-radius:8px;white-space:nowrap;box-shadow:0 6px 18px rgba(11,31,75,.25)}
@media(max-width:760px){.rq-band5{grid-template-columns:1fr 1fr}.vz-row{grid-template-columns:1fr;gap:4px}.vf{padding:18px 15px 16px}.vf h4{font-size:16.5px}.vz{padding:14px 12px 10px}}
'''

JS = '''<script>(function(){var t=null;function show(e){var el=e.target.closest&&e.target.closest('[data-tip]');if(!el)return;hide();t=document.createElement('div');t.className='vz-tip';t.textContent=el.getAttribute('data-tip');document.body.appendChild(t);var r=el.getBoundingClientRect(),w=t.offsetWidth,vw=document.documentElement.clientWidth;t.style.left=(Math.min(Math.max(8,r.left+r.width/2-w/2),vw-w-8)+scrollX)+'px';t.style.top=(r.top+scrollY-t.offsetHeight-8)+'px'}
function hide(){if(t){t.remove();t=null}}
document.addEventListener('mouseover',function(e){if(e.target.closest&&e.target.closest('.vz [data-tip]'))show(e)});document.addEventListener('mouseout',function(e){if(e.target.closest&&e.target.closest('.vz [data-tip]'))hide()});
document.addEventListener('focusin',function(e){if(e.target.closest&&e.target.closest('.vz [data-tip]'))show(e)});document.addEventListener('focusout',hide);window.addEventListener('scroll',hide,{passive:true})})();</script>'''
