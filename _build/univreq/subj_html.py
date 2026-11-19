# -*- coding: utf-8 -*-
"""Section: 学部別に見るイギリス上位50校の入学要件 (+ US course expectations, AP notes)."""
import re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import subj_stats as SS, us_subj as USJ
import analysis_html as AN
from statistics import median
from collections import Counter, OrderedDict

U = SS.U
SN = {'Cambridge':'ケンブリッジ','Oxford':'オックスフォード','LSE':'LSE','St Andrews':'セント・アンドルーズ','Imperial':'インペリアル','Durham':'ダラム',
      'Warwick':'ウォーリック','Loughborough':'ラフバラ','Bath':'バース','Lancaster':'ランカスター','Exeter':'エクセター','Birmingham':'バーミンガム',
      'Sheffield':'シェフィールド','UCL':'UCL','Southampton':'サウサンプトン','KCL':'キングス・カレッジ・ロンドン','Bristol':'ブリストル','Leeds':'リーズ',
      'Edinburgh':'エディンバラ','York':'ヨーク','Surrey':'サリー','Liverpool':'リバプール','QUB':'クイーンズ大学ベルファスト','Manchester':'マンチェスター',
      'Dundee':'ダンディー','Nottingham':'ノッティンガム','Cardiff':'カーディフ','UAL':'UAL','Glasgow':'グラスゴー','Essex':'エセックス','Heriot-Watt':'ヘリオット・ワット','Aberdeen':'アバディーン','Leicester':'レスター','UEA':'イースト・アングリア','Newcastle':'ニューカッスル','Sussex':'サセックス','Northumbria':'ノーザンブリア','Harper Adams':'ハーパー・アダムス','Strathclyde':'ストラスクライド','QMUL':'クイーン・メアリー','Swansea':'スウォンジー','Royal Holloway':'ロイヤル・ホロウェイ','Reading':'レディング','Suffolk':'サフォーク','Oxford Brookes':'オックスフォード・ブルックス','Nottingham Trent':'ノッティンガム・トレント','Ulster':'アルスター','Brunel':'ブルネル','Bangor':'バンガー','Lincoln':'リンカーン','Portsmouth':'ポーツマス'}
G = SS.T2G
def gname(t):
    if t is None: return '—'
    if t in G: return G[t]
    lo = max(k for k in G if k < t); hi = min(k for k in G if k > t)
    return '%s〜%s' % (G[lo], G[hi])
SCI = {'MATH', 'FM', 'PHY', 'CHEM', 'BIO'}
def pct(a, b): return round(100 * a / b) if b else 0

def sfinding(n, title, body, viz=''):
    return ('<article class="vf rise"><p class="vf-n">学部別 %d</p><h4>%s</h4>%s<div class="vf-rd"><span>ポイント</span>%s</div></article>' % (n, title, viz, body))

def test_tokens(t):
    out = []
    for w in ('UCAT', 'LNAT', 'TMUA', 'ESAT', 'TARA', 'STEP'):
        if w in t and not re.search(r'（[^）]*%s' % w, t): out.append(w)
    if 'カレッジ' in t: out.append('カレッジ独自の筆記')
    return out

def build():
    st = SS.stats()
    M = SS.MAJ
    out = []
    nuni = len(SS.UNIS)
    n_cells = sum(len(st[m]['off']) for m, _ in M)
    verified = sum(1 for m, _ in M for k, r in st[m]['off'] if SS.tariff(r.get('al')))
    nver_uni = sum(1 for k in SS.UNIS if any(SS.tariff((SS.U.S.get((k, m)) or {}).get('al')) for m, _ in M))
    out.append('<p class="rlead">イギリスの大学は、学部（コース）ごとに必要な成績と科目が決まっています。the Complete University Guide 2027の上位50校（同順位を含め%d校）について、'
               '医学から英文学まで12の学部の要件を各大学の公式サイトで一つずつ確認し、学部ごとに集計しました。'
               'アメリカの上位50校についても、学部やカレッジごとに高校で求められる科目と、出願の仕組みを確認しています。'
               '「どの学部に、どのくらいの成績が必要か」「IB・A Level・APでどの科目を取っておくべきか」が、学部と順位によってどれほど違うかが見えてきます</p>' % nuni)
    out.append('<div class="rq-scope rise"><b>集計の方法</b>　イギリスは12学部（医学・コンピュータサイエンス・機械工学・数学・物理学・生物学・経済学・経営学・法学・心理学・歴史学・英文学）。'
               '各大学で最も一般的な単独のコース（例：Mathematics BSc）を選び、2027年入学の標準的なオファーを使いました（一部は2024〜2026年入学の掲載）。'
               '幅のある要件は高い方、UCASポイントで示す大学はA Level相当（112点＝BBC、120点＝BBB）に置き換えています。'
               '学部がない大学は「なし」、公式サイトで確認できなかった項目は計算から外し、A Levelの成績は%d件、必須科目は%d件を集計しました（%d校）。'
               '値はすべて中央値です。アメリカはU.S. News 2027の上位50校（同順位を含め51校）のうち、各大学の入学案内で確認できた%d校です</div>'
               % (verified, sum(len(st[m]['reqs']) for m, _ in M if m != 'ECON'), nver_uni, len(USJ.US50)))

    # ---- 1. grade by major x band
    BANDS = [('1〜10位', 1, 10), ('11〜30位', 11, 30), ('31〜50位', 31, 50)]
    rows = []
    for m, ja in M:
        s = st[m]; t = [v for _, v in s['tar']]
        if not t: continue
        astar = sum(1 for k, r in s['off'] if SS.grades(r.get('al')) and 'A*' in SS.grades(r.get('al')))
        b = []
        for bn, lo, hi in BANDS:
            v = [x for k, x in s['tar'] if lo <= SS.RANK[k] <= hi]
            b.append((median(v) if v else None, len(v)))
        rows.append(dict(m=m, ja=ja, n=len(t), astar=astar, med=median(t), b=b))
    rows.sort(key=lambda r: (-(r['b'][0][0] or 0), -r['astar'] / r['n']))
    def tcol(t):
        p = max(0, min(100, (t - 112) / (168 - 112) * 100)); return AN.heat(p)
    trs = []
    for r in rows:
        cells = []
        for (v, n), (bn, _, _) in zip(r['b'], BANDS):
            if v is None:
                cells.append('<td class="hz-na">—</td>'); continue
            bg, ink = tcol(v)
            cells.append('<td tabindex="0" style="background:%s;color:%s" data-tip="%s・%s：中央値 %s（%d校）">%s</td>' % (bg, ink, r['ja'], bn, gname(v), n, gname(v)))
        trs.append('<tr><th>%s</th>%s<td class="gb-a">%d%%<small>%d校中%d校</small></td></tr>' % (r['ja'], ''.join(cells), pct(r['astar'], r['n']), r['n'], r['astar']))
    viz1 = ('<figure class="vz"><figcaption><b>学部×順位帯で見るA Levelの標準オファー（イギリス上位50校）</b><small>各学部・順位帯の中央値。色が濃いほど高い成績。右端は、A*を1つ以上求める大学の割合（50校全体）</small></figcaption>'
            '<div class="vz-tw"><table class="vz-heat hz gb"><thead><tr><th></th>' + ''.join('<th>%s</th>' % b[0] for b in BANDS) + '<th>A*を求める大学</th></tr></thead><tbody>'
            + ''.join(trs) + '</tbody></table></div></figure>')
    R = {r['m']: r for r in rows}
    b3 = [R[m]['b'][2][0] for m in ('CS', 'ENG', 'MATH', 'PHYS', 'BIO', 'ECON', 'BUS', 'HIST', 'ENGL') if R[m]['b'][2][0]]
    out.append(sfinding(1, '必要な成績は「大学の順位」と「学部」の掛け算で決まる',
        '上位10校では、数学が<b>%s</b>、機械工学が<b>%s</b>なのに対し、生物学は<b>%s</b>と、同じ順位帯でも学部によって1〜2段階の差があります。'
        '31〜50位になると、多くの学部は<b>%s〜%s</b>まで下がりますが、医学は<b>%s</b>、法学は<b>%s</b>のままです。'
        '医学部は、大学の順位が下がっても成績の基準がほとんど下がりません。'
        'A*を1つ以上求める大学の割合は、機械工学・数学で%d%%・%d%%なのに対し、生物学は%d%%、歴史学は%d%%です。'
        '<b>志望校を考えるときは、大学の順位だけでなく、学部ごとの基準を表で確かめる</b>ことが欠かせません'
        % (gname(R['MATH']['b'][0][0]), gname(R['ENG']['b'][0][0]), gname(R['BIO']['b'][0][0]), gname(min(b3)), gname(max(b3)),
           gname(R['MED']['b'][2][0]), gname(R['LAW']['b'][2][0]),
           pct(R['ENG']['astar'], R['ENG']['n']), pct(R['MATH']['astar'], R['MATH']['n']), pct(R['BIO']['astar'], R['BIO']['n']), pct(R['HIST']['astar'], R['HIST']['n'])), viz1))

    # ---- 2. medicine: tests > grades
    med = st['MED']; nmed = len(med['off']); ucat = sum(1 for k, t in med['tests'] if 'UCAT' in t)
    medchem = sum(1 for k, p in med['reqs'] if 'CHEM' in p[0]); medreq = len(med['reqs'])
    na_med = [k for k in med['na']]
    grad = [k for k in na_med if 'note' in U.S[(k, 'MED')]]
    out.append(sfinding(2, '医学部は、どの順位帯でもAAAとUCATが基本',
        '高校卒業後に医学部へ出願できることを確認できたのは、上位50校のうち%d校です（%sは学士卒のみ、%sなど%d校は医学部なし）。'
        '標準オファーの中央値は<b>%s</b>で、A*を求める大学は%d%%です。上位10校の中央値は数学や機械工学より低い一方、31〜50位でもAAAが中心です。'
        'その代わり、<b>%d校すべてがUCAT（医学部の適性試験）を課しています</b>。'
        '科目では、%d校中%d校が<b>化学を必須</b>にしています。'
        '医学部を目指すなら、成績に加えて、UCATの準備と医療に関わる経験を早めに計画しておく必要があります'
        % (nmed, '・'.join(SN[k] for k in grad), '・'.join(SN[k] for k in na_med if k not in grad)[:0] + '・'.join(SN[k] for k in [x for x in na_med if x not in grad][:3]),
           len(na_med) - len(grad), gname(R['MED']['med']), pct(R['MED']['astar'], R['MED']['n']), ucat, medreq, medchem)))

    # ---- 3. required subjects heatmap
    COLS = [('MATH', '数学'), ('FM', '更なる数学'), ('PHY', '物理'), ('CHEM', '化学'), ('BIO', '生物'), ('OPT', '理系から1科目'), ('HIST', '歴史'), ('ENG', '英文学'), ('NONE', '指定なし')]
    hrows = []; tv = []; H = {}
    for m, ja in M:
        s = st[m]
        if m == 'ECON':
            al = [(k, r) for k, r in s['off'] if r.get('al')]
            c = sum(1 for k, r in al if '数学' in r['al']); n = len(al)
            vals = {'MATH': (c, n)}
        else:
            n = len(s['reqs']); vals = {}
            if not n: continue
            raw = dict((k, r.get('req') or '') for k, r in s['off'])
            for key, _ in COLS:
                if key == 'NONE': c = sum(1 for k, p in s['reqs'] if p[2])
                elif key == 'OPT': c = sum(1 for k, p in s['reqs'] if (any(g & SCI for g in p[1]) or '理系' in raw[k]) and not p[2])
                else: c = sum(1 for k, p in s['reqs'] if key in p[0])
                vals[key] = (c, n)
        H[m] = vals
        cells = []
        for key, cn in COLS:
            if key not in vals:
                cells.append('<td class="hz-na" aria-label="%s・%s：集計なし">—</td>' % (ja, cn)); continue
            c, n = vals[key]; p = pct(c, n); bg, ink = AN.heat(p)
            if c == 0:
                cells.append('<td tabindex="0" class="hz-0" data-tip="%s・%s：%d校中0校">0</td>' % (ja, cn, n)); continue
            cells.append('<td tabindex="0" style="background:%s;color:%s" data-tip="%s・%s：%d校中%d校（%d%%）">%d%%</td>' % (bg, ink, ja, cn, n, c, p, p))
        hrows.append('<tr><th>%s<small>%d校</small></th>%s</tr>' % (ja, vals[list(vals)[0]][1], ''.join(cells)))
    viz3 = ('<figure class="vz"><figcaption><b>A Levelで必須とされる科目（イギリス上位50校・学部別）</b><small>必須科目を確認できた大学のうち、その科目を必須にしている大学の割合。'
            '「理系から1科目」は、生物・化学・物理・数学などから1つを選ぶ条件。経済学は、オファーに数学の記載がある大学の割合のみ</small></figcaption>'
            '<div class="vz-tw"><table class="vz-heat hz"><thead><tr><th></th>' + ''.join('<th>%s</th>' % c for _, c in COLS) + '</tr></thead><tbody>' + ''.join(hrows) + '</tbody></table></div></figure>')
    def hp(m, key): c, n = H[m][key]; return pct(c, n)
    out.append(sfinding(3, '理系は「科目の指定」で、文系は「成績」で決まる',
        '数学を必須にする大学の割合は、数学（%d%%）・物理学（%d%%）・機械工学（%d%%）で9割を超え、コンピュータサイエンスでも%d%%です。'
        '物理学は%d%%が物理を、医学は%d%%が化学を求めます。'
        '一方、法学は<b>%d%%</b>、経営学は<b>%d%%</b>の大学が「科目の指定なし」です。歴史学で歴史を必須にする大学は%d%%、英文学で英文学を必須にする大学は%d%%にとどまり、'
        '文系の学部は科目より成績そのものが問われます。'
        '<b>理系の学部を考えているなら、IBやA Levelの科目選択（G10〜G11）の時点で志望学部を決めておく</b>必要があります。後から科目を足すことは難しいためです'
        % (hp('MATH','MATH'), hp('PHYS','MATH'), hp('ENG','MATH'), hp('CS','MATH'), hp('PHYS','PHY'), hp('MED','CHEM'), hp('LAW','NONE'), hp('BUS','NONE'), hp('HIST','HIST'), hp('ENGL','ENG')), viz3))

    # ---- 4. admissions tests
    T = OrderedDict()
    for m, ja in M:
        for k, t in st[m]['tests']:
            for w in test_tokens(t):
                T.setdefault(w, OrderedDict()).setdefault(ja, []).append(k)
    TJ = {'UCAT': 'UCAT（医学部の適性試験）', 'LNAT': 'LNAT（法学部の適性試験）', 'TMUA': 'TMUA（数学の適性試験）', 'ESAT': 'ESAT（理工系の適性試験）',
          'TARA': 'TARA（思考力の試験）', 'STEP': 'STEP（数学の記述試験）', 'カレッジ独自の筆記': 'カレッジ独自の筆記試験'}
    trs = []; test_unis = set()
    for w, byj in T.items():
        parts = []
        for ja, ks in byj.items():
            ks = sorted(set(ks), key=lambda k: SS.RANK[k]); test_unis |= set(ks)
            if w == 'UCAT': parts.append('%s：医学部のある%d校すべて' % (ja, len(ks)))
            else: parts.append('%s：%s' % (ja, '、'.join(SN[k] for k in ks)))
        trs.append('<tr><th>%s</th><td>%s</td></tr>' % (TJ.get(w, w), '<br>'.join(parts)))
    non_med = set(k for w, byj in T.items() if w != 'UCAT' for ks in byj.values() for k in ks)
    top16 = sum(1 for k in non_med if SS.RANK[k] <= 16)
    viz4 = ('<figure class="vz"><figcaption><b>入学試験を課す学部と大学（イギリス上位50校）</b><small>2027年入学で、出願者全員に受験を求める試験。条件緩和のためだけの試験は除く</small></figcaption>'
            '<div class="vz-tw"><table class="tz tz-test"><thead><tr><th>試験</th><th>学部：課している大学</th></tr></thead><tbody>' + ''.join(trs) + '</tbody></table></div></figure>')
    out.append(sfinding(4, '医学部以外の入学試験は、ごく一部の上位校に集中している',
        '医学部のUCATを除くと、入学試験を課す大学は%d校で、すべて総合%d位以内です。'
        'オックスフォード・ケンブリッジ・インペリアル・UCL・LSE・キングス・カレッジ・ロンドンなどでは、法学のLNAT、数学やコンピュータサイエンスのTMUA、理工系のESATが加わります。'
        '<b>試験の多くは、出願する年の夏から秋（G12の初め）に行われます</b>。上位校を目指す場合は、G11のうちに過去問で準備を始めるのが目安です'
        % (len(non_med), max(SS.RANK[k] for k in non_med)), viz4))

    # ---- 5. IB: HL7
    ibrows = []
    for m, ja in M:
        s = st[m]; v = [x for _, x in s['ib']]
        if not v: continue
        ibrows.append((ja, median(v), len(v), len(s['h7']), len(s['ibk'])))
    ibd = {r[0]: r for r in ibrows}
    h7_list = sorted([r for r in ibrows if r[3]], key=lambda r: -r[3] / r[4])
    viz5 = ('<figure class="vz"><figcaption><b>IBの要件（イギリス上位50校・学部別）</b><small>総合点の中央値と、特定の科目でHL 7を求める大学の数</small></figcaption>'
            '<div class="vz-tw"><table class="tz tz-ib"><thead><tr><th>学部</th><th>総合点（中央値）</th><th>特定の科目でHL 7</th></tr></thead><tbody>'
            + ''.join('<tr><th>%s</th><td><b>%s点</b><small>%d校</small></td><td>%s</td></tr>' % (ja, AN.fmt(md), n, ('<b>%d校</b>／%d校' % (h, nk)) if h else 'なし')
                      for ja, md, n, h, nk in ibrows) + '</tbody></table></div></figure>')
    out.append(sfinding(5, 'IBは総合点より「どの科目でHL 7を取るか」で差がつく',
        '総合点の中央値は、どの学部も%s〜%s点の範囲に収まり、学部による差は小さめです。差が出るのは科目の点数で、'
        '<b>数学（%d校）・コンピュータサイエンス（%d校）</b>では、数学のHLで7を求める大学が目立ちます。一方、法学・歴史学・英文学・心理学では、特定の科目でHL 7を求める大学はありませんでした。'
        '理系の上位校を目指すなら、<b>数学AA（Analysis and Approaches）のHLを選び、7を取れるかどうか</b>が最も大きな分かれ目になります'
        % (AN.fmt(min(r[1] for r in ibrows)), AN.fmt(max(r[1] for r in ibrows)), ibd['数学'][3], ibd['コンピュータサイエンス'][3]), viz5))

    # ---- 6. US: application structure + engineering course requirements
    import inter_lens as IL, us_data as UD, us_data2 as UD2
    ja_us = {d['en']: d['ja'] for d in UD.US + UD2.US3}
    rk_us = {d['en']: d['rank'] for d in UD.US + UD2.US3}
    def jn(en): return re.sub(r'（.*?）', '', ja_us.get(en, en))
    conf = {en: d for en, d in USJ.US50.items() if d.get('apply')}
    AP = [('U', '大学全体で出願し、入学後に専攻を決める', '--vc1', 'w'), ('S', '出願時に学部（スクール）を選ぶ', '--vc2', 'k'), ('M', '出願時に専攻を選び、工学やCSは入学時に選抜', '--vc3', 'k')]
    def grp(rows):
        return [(key, name, sum(1 for e in rows if conf[e]['apply'] == key), var, ink) for key, name, var, ink in AP]
    pub = [e for e in conf if e in IL.PUBLIC]; prv = [e for e in conf if e not in IL.PUBLIC]
    bars6 = [AN.seg_bar('私立', '確認できた%d校' % len(prv), grp(prv), len(prv)), AN.seg_bar('州立', '確認できた%d校' % len(pub), grp(pub), len(pub))]
    lists = '<ul class="ul2 sg-ul">' + ''.join('<li><b>%s</b>：%s</li>' % (name, '、'.join(jn(e) for e in sorted([e for e in conf if conf[e]['apply'] == key], key=lambda e: rk_us[e])))
                                              for key, name, _, _ in AP) + '</ul>'
    viz6a = ('<figure class="vz"><figcaption><b>出願の仕組み（アメリカ上位50校）</b><small>各大学の入学案内で確認できた%d校。私立と州立で比べたもの</small></figcaption>' % len(conf)
             + AN.legend([(n, v) for _, n, v, _ in AP]) + '<div class="vz-rows">' + ''.join(bars6) + '</div>' + lists + '</figure>')
    eng = [(en, d) for en, d in USJ.US50.items() if d.get('eng_kind') and d.get('eng') not in (None, '—')]
    ereq = [e for e, d in eng if d['eng_kind'] == '必須']; erec = [e for e, d in eng if d['eng_kind'] == '推奨']
    def has(w): return sum(1 for e, d in eng if w in d['eng'])
    usr = ''.join('<tr><th>%s</th><td>%s</td><td>%s</td></tr>' % (jn(en), d['eng_kind'], d['eng']) for en, d in sorted(eng, key=lambda x: (x[1]['eng_kind'] != '必須', rk_us[x[0]])))
    viz6b = ('<figure class="vz"><figcaption><b>工学系の出願者に求める高校の科目（アメリカ上位50校）</b><small>工学部や理工系の出願者向けの条件を確認できた%d校。「必須」は出願の条件、「推奨」は大学が勧める履修</small></figcaption>' % len(eng)
             + AN.legend([('必須', '--vo1'), ('推奨', '--vo2')])
             + '<div class="vz-rows">' + AN.seg_bar('工学系の条件', '確認できた%d校' % len(eng), [('r', '必須', len(ereq), '--vo1', 'w'), ('c', '推奨', len(erec), '--vo2', 'k')], len(eng)) + '</div>'
             + '<details class="vz-tv"><summary>%d校の条件を表で見る</summary><div class="vz-tw"><table class="tz"><thead><tr><th>大学</th><th>扱い</th><th>高校で履修しておく科目</th></tr></thead><tbody>' % len(eng)
             + usr + '</tbody></table></div></details></figure>')
    cU = sum(1 for e in prv if conf[e]['apply'] == 'U'); cPM = sum(1 for e in pub if conf[e]['apply'] == 'M')
    out.append(sfinding(6, 'アメリカは「出願の仕組み」が大学で違う。州立大学は専攻を決めて出願するのが主流',
        'アメリカの上位50校のうち、出願の仕組みを確認できた%d校を分類しました。私立%d校のうち%d校は大学全体で出願し、入学後に専攻を決める仕組みです。'
        '一方、州立%d校のうち<b>%d校は出願時に専攻を選び</b>、カリフォルニア大学バークレー校やワシントン大学などでは、CSや工学は入学時に専攻ごとの選抜があります。'
        'なお、アメリカでは医学部と法科大学院は大学卒業後に進む大学院のため、学部の段階では「医学」「法学」の専攻はありません'
        % (len(conf), len(prv), cU, len(pub), cPM), viz6a))
    out.append(sfinding(7, '工学系は高校の「微積分・物理・化学」が条件になりやすい',
        '工学部や理工系の出願者向けの条件を確認できた%d校のうち、<b>%d校が科目を「必須」</b>としています（%d校は推奨）。'
        '条件に挙がる科目は、微積分（%d校）・物理（%d校）・化学（%d校）が中心です。文系の学部やスクールでは「数学3年・理科3年」程度が一般的で、科目まで指定する大学は多くありません。'
        '<b>アメリカの工学系を考えているなら、高校で微積分・物理・化学を履修しておく</b>と、多くの大学の条件を満たせます。IBなら数学AAと物理・化学、A Levelなら数学と物理・化学がこれにあたります'
        % (len(eng), len(ereq), len(erec), has('微積分'), has('物理'), has('化学')), viz6b))

    # ---- guide: what to take
    GUIDE = [
        ('医学', '化学＋生物（数学か物理でも可の大学あり）', '化学＋生物（または数学・物理）', 'Chemistry・Biology'),
        ('コンピュータサイエンス', '数学AA（上位校は7）', '数学（上位校は更なる数学も）', 'Calculus BC（＋Computer Science A）'),
        ('機械工学', '数学AA・物理', '数学・物理（更なる数学があると有利）', 'Calculus BC・Physics C'),
        ('数学', '数学AA（上位校は7）', '数学・更なる数学', 'Calculus BC（＋Statistics）'),
        ('物理学', '数学AA・物理', '数学・物理', 'Calculus BC・Physics C'),
        ('生物学', '生物＋化学など理系1科目', '生物＋理系1科目', 'Biology・Chemistry'),
        ('経済学', '数学AA', '数学', 'Calculus BC・Microeconomics・Macroeconomics'),
        ('経営学', '指定なしが多い（数学があると選択肢が広がる）', '指定なしが多い', 'Calculus・Statistics'),
        ('法学', '指定なし（英語・歴史など文章を書く科目）', '指定なし', 'English Language・History'),
        ('心理学', '生物・化学・数学・心理学などから1科目', '理系か心理学から1科目', 'Psychology・Biology・Statistics'),
        ('歴史学', '歴史', '歴史', 'World History・European History など'),
        ('英文学', '英語A（文学）', '英文学', 'English Literature'),
    ]
    out.append('<div class="vz rise sg"><p class="vz-sub" style="margin-top:0">志望学部別：取っておきたい科目</p>'
               '<p class="sg-lead">上の集計で、必須とする大学が多かった科目をまとめました。APは、志望コースに合った科目を選ぶというケンブリッジ大学の方針に沿って、対応する科目の例を挙げています</p>'
               '<div class="vz-tw"><table class="tz"><thead><tr><th>志望学部</th><th>IB（HL）</th><th>A Level</th><th>AP（例）</th></tr></thead><tbody>'
               + ''.join('<tr><th>%s</th><td>%s</td><td>%s</td><td>%s</td></tr>' % g for g in GUIDE) + '</tbody></table></div>'
               '<ul class="ul2 sg-ul">' + ''.join('<li><b>%s</b>：%s</li>' % (d['uni'], d['text']) for d in USJ.UK_AP) + '</ul></div>')

    out.append('<div class="vf-sum rise"><p class="vf-sum-h">学部別の要件から見えること</p><ol>'
               '<li><b>科目選択の前に、志望学部の必須科目を確認する</b>：理系の学部は数学・物理・化学などの指定がほぼ必ずあります。IBのHLやA Levelの科目は、後から変えることが難しいためです</li>'
               '<li><b>大学名ではなく、学部ごとに必要な成績を見る</b>：同じ大学でも、数学や機械工学は生物学や英文学より1〜2段階高い成績を求められます</li>'
               '<li><b>アメリカは出願の仕組みを先に確認する</b>：州立大学は出願時に専攻を選ぶことが多く、CSや工学は入学後に移るのが難しい大学もあります</li>'
               '<li><b>試験のある学部は、G11のうちに準備を始める</b>：医学部のUCATや、上位校の法学・数学・理工系の試験は、出願する年の夏から秋に行われます</li></ol></div>')
    return '\n'.join(out)

def sources():
    seen = set(); src = []
    for (k, m), r in SS.U.S.items():
        for u in (r.get('src') or []):
            if u not in seen: seen.add(u); src.append((u, '%s（%s）：%s' % (SS.KEY.get(k, k), r.get('course') or '', u.split('//')[1].split('/')[0])))
    for d in USJ.UK_AP:
        if d['src'] not in seen: seen.add(d['src']); src.append((d['src'], '%s：%s' % (d['uni'], d['src'].split('//')[1].split('/')[0])))
    for en, d in USJ.US50.items():
        for u in d.get('src') or []:
            if u not in seen: seen.add(u); src.append((u, '%s（入学案内）：%s' % (en, u.split('//')[1].split('/')[0])))
    for u, t in [(U.UCAT, 'UCAT：参加大学の一覧'), (U.LNAT, 'LNAT：出願締切と参加大学')]:
        if u not in seen: seen.add(u); src.append((u, t))
    return src

CSS = '''
.hz{table-layout:fixed;min-width:560px}
.hz th:first-child{text-align:left;width:128px;white-space:normal}
.hz thead th{text-align:center;white-space:normal;line-height:1.35;font-size:11px;padding:6px 2px}
.hz td{min-width:0;padding:9px 2px;font-size:12.5px}
.hz td.hz-0{background:transparent;color:#a3adc2;font-weight:500}
.hz td.hz-na{background:transparent;color:var(--muted,#5c6984);font-weight:500}
.tz td,.tz th{white-space:normal;vertical-align:top;line-height:1.7}
.tz tbody th{min-width:150px}
.tz td small{display:block;font-size:11px;color:var(--muted,#5c6984);font-weight:500}
.tz-ib td,.tz-ib th{padding:6px 10px}
.tz-ib td small{display:inline;margin-left:6px}
.tz-test tbody th{width:190px}
.gb td{font-size:12.5px;white-space:nowrap}.gb td.gb-a{background:transparent;color:var(--navy,#0b1f4b);font-weight:700}.gb td.gb-a small{display:block;font-size:10.5px;font-weight:500;color:var(--muted,#5c6984)}
.sg{margin-top:18px}
.sg-lead{font-size:13.5px;line-height:1.85;margin:6px 0 4px;color:var(--ink,#0b1f4b)}
.sg-ul{margin:14px 0 0;font-size:13.5px}
@media(max-width:760px){.hz.gb{min-width:0;width:100%}.hz.gb th:first-child{width:76px;font-size:11.5px}.gb td{font-size:10.5px;white-space:normal;padding:8px 1px;line-height:1.3}.gb thead th{font-size:10px}.gb td.gb-a small{font-size:9.5px}.tz tbody th{min-width:110px}.tz-test tbody th{width:auto}.hz{min-width:500px}.hz th:first-child{width:92px;position:sticky;left:0;background:#fcfcfb;z-index:1;font-size:12px}}
'''

if __name__ == '__main__':
    h = build(); print(len(h)); print(re.sub(r'<[^>]+>', ' ', h)[:3000])
