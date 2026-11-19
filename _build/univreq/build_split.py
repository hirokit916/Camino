# -*- coding: utf-8 -*-
"""Split pages: ① IB・A Level scores article, 12 by-major articles, SAT/English-test article.
Usage: python3 build_split.py /home/claude/camino-v2"""
import os, sys, re
from statistics import median
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'subj')); sys.path.insert(0, HERE)
import common as M
import build_req as BR
import analysis_html as AN
import subj_stats as SS
import subj_html as SJ
import acs_subj as A
import us_subj as USJ
import us_data as UD, us_data2 as UD2

C = M.C
M.TODAY = '2026-11-16'
DB = '/column/university/us-uk-requirements/'
SCORES = '/column/university/ib-scores-by-major/'
SCORES_AL = '/column/university/a-level-scores-by-major/'
OLD_SCORES = '/column/university/ib-alevel-scores/'
TESTS = '/column/university/sat-english-tests/'
SLUG = {'MED': 'medicine', 'CS': 'computer-science', 'ENG': 'engineering', 'MATH': 'mathematics', 'PHYS': 'physics', 'BIO': 'biology',
        'ECON': 'economics', 'BUS': 'business', 'LAW': 'law', 'PSY': 'psychology', 'HIST': 'history', 'ENGL': 'english'}
def mpath(m): return '/column/university/majors/%s/' % SLUG[m]
MAJ = SS.MAJ; MJ = dict(MAJ)
gname = SJ.gname; pct = SJ.pct
CTY = [('AU', 'オーストラリア'), ('CA', 'カナダ'), ('SG', 'シンガポール')]
UNIJA = {(c, k): j for c, lst in A.UNI.items() for k, j in lst}
SCI = {'MATH', 'FM', 'PHY', 'CHEM', 'BIO'}
BANDS = [('イギリス1〜10位', 1, 10), ('イギリス11〜30位', 11, 30), ('イギリス31〜50位', 31, 50)]
ST = SS.stats()
UK_RANK_SRC = BR.UK_RANK[0]

# ---------------- data helpers ----------------
def uk_rows(m):
    out = []
    for k in SS.UNIS:
        r = SS.U.S.get((k, m))
        if r is None or r.get('course') in (None, SS.U.NA): continue
        out.append((k, r))
    return out
def acs_rows(m, cty=None):
    out = []
    for c, lst in A.UNI.items():
        if cty and c != cty: continue
        for k, _ in lst:
            r = A.S.get((c, k, m))
            if r is None or r.get('course') in (None, A.NA): continue
            out.append((c, k, r))
    return out
def ib_uk(r): return SS.ibpts(r.get('ib'))
def tar(r): return SS.tariff(r.get('al'))
def band_med(m, lo, hi, f):
    v = [f(r) for k, r in uk_rows(m) if lo <= SS.RANK[k] <= hi and f(r)]
    return (median(v) if v else None), len(v)
def acs_ib_med(m, c):
    v = [r['ib'] for _, _, r in acs_rows(m, c) if r.get('ib')]
    return (median(v) if v else None), len(v)

REQ_COLS = [('MATH', '数学'), ('FM', '更なる数学'), ('PHY', '物理'), ('CHEM', '化学'), ('BIO', '生物'), ('OPT', '理系から1科目'), ('HIST', '歴史'), ('ENG', '英語・英文学'), ('NONE', '指定なし')]
def req_counts(pairs):
    """pairs: list of raw req strings (None excluded). -> {col: (c, n)}"""
    parsed = [(s, SS.req_parse(s)) for s in pairs if s is not None]
    n = len(parsed); out = {}
    for key, _ in REQ_COLS:
        if key == 'NONE': c = sum(1 for s, p in parsed if p[2])
        elif key == 'OPT': c = sum(1 for s, p in parsed if not p[2] and (any(g & SCI for g in p[1]) or '理系' in s))
        else: c = sum(1 for s, p in parsed if key in p[0])
        out[key] = (c, n)
    return out

def heat_td(label, c, n, tipname):
    if n == 0: return '<td class="hz-na">—</td>'
    p = pct(c, n)
    if c == 0: return '<td tabindex="0" class="hz-0" data-tip="%s：%d校中0校">0</td>' % (tipname, n)
    bg, ink = AN.heat(p)
    return '<td tabindex="0" style="background:%s;color:%s" data-tip="%s：%d校中%d校（%d%%）">%d%%</td>' % (bg, ink, tipname, n, c, p, p)
def grade_td(v, n, tipname, kind='al'):
    if v is None: return '<td class="hz-na">—</td>'
    if kind == 'al':
        t = gname(v); p = max(0, min(100, (v - 112) / (168 - 112) * 100))
    else:
        t = '%s点' % AN.fmt(v); p = max(0, min(100, (v - 26) / (42 - 26) * 100))
    bg, ink = AN.heat(p)
    return '<td tabindex="0" style="background:%s;color:%s" data-tip="%s：中央値 %s（%d校）">%s</td>' % (bg, ink, tipname, t, n, t)
def heat_table(cap, sub, cols, rows, cls='hz'):
    rows = [r.replace('>コンピュータサイエンス<', '>コンピュータ<wbr>サイエンス<') for r in rows]
    return ('<figure class="vz rise"><figcaption><b>%s</b><small>%s</small></figcaption><div class="vz-tw"><table class="vz-heat %s"><thead><tr><th></th>%s</tr></thead><tbody>%s</tbody></table></div></figure>'
            % (cap, sub, cls, ''.join('<th>%s</th>' % c for c in cols), ''.join(rows)))

def tier_list(vals, fmtf, order_desc=True):
    """vals: [(major_ja, value)] -> parallel grouped list"""
    g = {}
    for ja, v in vals:
        if v is None: continue
        g.setdefault(v, []).append(ja)
    items = sorted(g.items(), key=lambda x: -x[0] if order_desc else x[0])
    return '<ul class="tlv">' + ''.join('<li><b>%s</b><span>%s</span></li>' % (fmtf(v), '・'.join(js)) for v, js in items) + '</ul>'

# ---------------- ① scores article ----------------

# ---------------- country view ----------------
def uni_med(kind, cty, k):
    if cty == 'UK':
        f = ib_uk if kind == 'ib' else tar
        v = [f(SS.U.S.get((k, m)) or {}) for m, _ in MAJ]
    elif kind == 'ib':
        v = [(A.S.get((cty, k, m)) or {}).get('ib') for m, _ in MAJ]
    else:
        v = [SS.tariff((A.S.get((cty, k, m)) or {}).get('al')) for m, _ in MAJ]
    v = [x for x in v if x]
    return (median(v) if v else None), len(v)


SHORT = {'MED': '医学', 'CS': 'CS', 'ENG': '機械工学', 'MATH': '数学', 'PHYS': '物理学', 'BIO': '生物学', 'ECON': '経済学', 'BUS': '経営学', 'LAW': '法学', 'PSY': '心理学', 'HIST': '歴史学', 'ENGL': '英文学'}
def cell_val(kind, cty, k, m):
    if cty == 'UK':
        r = SS.U.S.get((k, m))
        if r is None: return None, False
        if r.get('course') == SS.U.NA: return None, True
        return (ib_uk(r) if kind == 'ib' else tar(r)), False
    r = A.S.get((cty, k, m))
    if r is None: return None, False
    if r.get('course') == A.NA: return None, True
    return (r.get('ib') if kind == 'ib' else SS.tariff(r.get('al'))), False

ACS_SN = {'Melbourne': 'メルボルン', 'Sydney': 'シドニー', 'UNSW': 'UNSW', 'ANU': 'ANU', 'Monash': 'モナシュ', 'McGill': 'マギル', 'Toronto': 'トロント', 'UBC': 'UBC', 'Alberta': 'アルバータ', 'Waterloo': 'ウォータールー'}
def uni_major_matrix(kind):
    groups = [('イギリス', [('UK', k, SJ.SN.get(k, k)) for k in SS.UNIS if SS.RANK[k] <= 10])]
    if kind == 'ib':
        groups += [('オーストラリア', [('AU', k, ACS_SN[k]) for k, j in A.UNI['AU']]), ('カナダ', [('CA', k, ACS_SN[k]) for k, j in A.UNI['CA']])]
    else:
        groups += [('オーストラリア', [('AU', 'UNSW', 'UNSW')]), ('カナダ', [('CA', 'McGill', 'マギル')])]
    rows = []
    for g, unis in groups:
        rows.append('<tr class="mx-g"><th colspan="13">%s</th></tr>' % g)
        for cty, k, ja in unis:
            cells = []
            for m, mja in MAJ:
                v, na = cell_val(kind, cty, k, m)
                if na: cells.append('<td class="hz-na mx-no">なし</td>')
                else: cells.append(grade_td(v, 1, '%s・%s' % (re.sub(r'（.*?）', '', ja), mja), kind).replace('：中央値 ', '：').replace('（1校）', ''))
            rows.append('<tr><th>%s</th>%s</tr>' % (re.sub(r'（.*?）', '', ja), ''.join(cells)))
    cap = '国×大学×学部で見る%s' % ('IBの総合点' if kind == 'ib' else 'A Levelの成績')
    sub = ('各大学の学部ごとの要件。UNSWはニューサウスウェールズ大学、ANUはオーストラリア国立大学、UBCはブリティッシュコロンビア大学。「なし」はその学部がない（または大学院で学ぶ）大学、「—」は公式サイトで確認できなかった項目です')
    return ('<figure class="vz rise"><figcaption><b>%s</b><small>%s</small></figcaption><div class="vz-tw"><table class="vz-heat hz umx"><thead><tr><th></th>%s</tr></thead><tbody>%s</tbody></table></div></figure>'
            % (cap, sub, ''.join('<th><a href="%s">%s</a></th>' % (mpath(m), SHORT[m]) for m, _ in MAJ), ''.join(rows)))

def country_section(kind, step):
    lo, hi = (26, 42) if kind == 'ib' else (104, 168)
    fmtv = (lambda v: '%s点' % AN.fmt(v)) if kind == 'ib' else gname
    groups = [('イギリス', 'the Complete University Guide 2027の1〜10位', [('UK', k, SS.JA[k], SS.RANK[k]) for k in SS.UNIS if SS.RANK[k] <= 10])]
    if kind == 'ib':
        groups += [('オーストラリア', 'QS世界大学ランキング2027の国内1〜5位', [('AU', k, j, i + 1) for i, (k, j) in enumerate(A.UNI['AU'])]),
                   ('カナダ', 'QS世界大学ランキング2027の国内1〜5位', [('CA', k, j, i + 1) for i, (k, j) in enumerate(A.UNI['CA'])])]
    else:
        groups += [('オーストラリア・カナダ', 'A Levelの条件を学部ごとに示している大学', [('AU', 'UNSW', UNIJA[('AU', 'UNSW')], 3), ('CA', 'McGill', UNIJA[('CA', 'McGill')], 1)])]
    MINN = 3
    rows = []; best = {}
    for gname_, gsub, unis in groups:
        rows.append('<p class="cv-g">%s<small>%s</small></p>' % (gname_, gsub))
        for cty, k, ja, rk in unis:
            v, n = uni_med(kind, cty, k)
            if v is None or n < MINN:
                rows.append('<div class="sbr cv-na"><span class="sb-l">%s<small>国内%d位</small></span><span class="sb-t"></span><span class="sb-v">—<small>%s</small></span></div>'
                            % (ja, rk, '学部ごとの点数の公表なし' if not n else '%d学部のみ' % n))
                continue
            best.setdefault(gname_, []).append(v)
            w = max(3, min(100, (v - lo) / (hi - lo) * 100))
            rows.append('<div class="sbr"><span class="sb-l">%s<small>国内%d位</small></span><span class="sb-t"><i style="width:%d%%"></i></span><span class="sb-v">%s<small>%d学部の中央値</small></span></div>'
                        % (ja, rk, w, fmtv(v), n))
    cap = ('各国の上位校が、IBで求める総合点' if kind == 'ib' else '各国の上位校が、A Levelで求める成績')
    sub = ('12学部のうち点数を確認できた学部の中央値（3学部以上の大学のみ）。イギリスは標準的なオファー、オーストラリアは入学の目安や保証点、カナダは大学が示す目安の下限です'
           if kind == 'ib' else '12学部のうち成績を確認できた学部の中央値（3学部以上の大学のみ）。イギリスとカナダは標準的なオファー（幅がある場合は高い方）、オーストラリアは大学がA Levelの合計点から換算して示す目安です')
    fig = '<figure class="vz rise"><figcaption><b>%s</b><small>%s</small></figcaption><div class="sb-wrap cv">%s</div></figure>' % (cap, sub, ''.join(rows))
    uk = best.get('イギリス', [])
    if kind == 'ib':
        au = best.get('オーストラリア', []); ca = best.get('カナダ', [])
        txt = ('<p class="mjq-p">イギリスの上位10校は%s〜%s点を求めます。これに対してオーストラリアの上位5校は%s〜%s点、カナダのマギル大学は%s点で、各国のトップ校でも求める総合点は同じではありません。'
               'ただし、点数の意味は国によって違います。イギリスの標準的なオファーは、合格した人が入学までに取る必要がある点数です。オーストラリアのメルボルン大学などは、その点数を取れば入学を保証する「保証点」を示しています。'
               'シンガポールの主要大学は、IBの点数の目安を学部ごとに公表していません</p>'
               % (AN.fmt(min(uk)), AN.fmt(max(uk)), AN.fmt(min(au)), AN.fmt(max(au)), AN.fmt(ca[0]) if ca else '—'))
    else:
        txt = ('<p class="mjq-p">イギリスの上位10校は%s〜%sが中心で、カナダのマギル大学は%s、オーストラリアのニューサウスウェールズ大学は%sです。'
               '同じ「国内トップクラス」の大学でも、A Levelで求める成績は国によって大きく違います</p>'
               % (gname(min(uk)), gname(max(uk)), gname(uni_med('al', 'CA', 'McGill')[0]), gname(uni_med('al', 'AU', 'UNSW')[0])))
    mx = uni_major_matrix(kind)
    if kind == 'ib':
        d = []
        for m, ja in MAJ:
            u, _ = band_med(m, 1, 10, ib_uk); a, _ = acs_ib_med(m, 'AU')
            if u and a: d.append((u - a, ja, u, a))
        d.sort()
        small = [x for x in d if x[0] <= 0]; big = d[-2:]
        parts = []
        for x, ja, u, a in small:
            parts.append(('%sはオーストラリアとイギリス上位10校が同じ%s点' % (ja, AN.fmt(a)), 'で') if x == 0 else
                         ('%sはオーストラリア（%s点）がイギリス上位10校（%s点）を上回り' % (ja, AN.fmt(a), AN.fmt(u)), ''))
        body_ = '、'.join(t + c for t, c in parts[:-1]) + ('、' if len(parts) > 1 else '') + parts[-1][0] + ('です' if parts[-1][1] else 'ます')
        mx += ('<p class="mjq-p">学部ごとに並べると、国による差の大きさは学部によって違います。%s。'
               '一方、差が最も大きいのは%sです</p>'
               % (body_,
                  '、'.join('%s（イギリス上位10校%s点、オーストラリア%s点）' % (ja, AN.fmt(u), AN.fmt(a)) for x, ja, u, a in reversed(big))))
    return [C.step(step, 'country', '国別に見ると：各国のトップ校は同じ水準？', '大学ごとの、12学部の要件'), fig, txt, mx]

def links_block(n, other, other_name):
    cards = ''.join('<a class="mj-card" href="%s"><b>%s</b><span>成績・必須科目・大学一覧</span></a>' % (mpath(m), ja) for m, ja in MAJ)
    return [C.step(n, 'majors', '学部別に詳しく見る', '大学ごとの要件と、IB・A Level・APの条件'),
            '<div class="mj-grid rise">%s</div>' % cards,
            '<p class="rnote">%sでの出願は<a href="%s">%s</a>へ。大学ごとの一覧は<a href="%s">出願要件データベース</a>へ。要件は毎年見直されるため、最新の情報は必ず各大学の公式サイトで確認してください</p>'
            % ('IB' if 'IB' in other_name else 'A Level', other, other_name, DB)]

def al_body():
    out = []
    out.append('<div class="us-note rise"><b>アメリカの大学が載っていない理由</b>アメリカの大学は、成績・エッセイ・課外活動などをあわせて評価するため、A Levelの成績の基準を学部ごとに公表していません。そのため、この記事では点数の基準を公表しているイギリスの大学（と、A Levelの条件を示しているオーストラリア・カナダの大学）を比べています。アメリカの大学のSAT・英語試験の扱いは<a href="%s">SAT・英語試験はどのくらい必要？</a>へ</div>' % TESTS)
    n_uk = len(SS.UNIS)
    out.append('<div class="rq-scope rise"><b>対象</b>　イギリスの上位50校（the Complete University Guide 2027、同順位を含め%d校）。オーストラリアとカナダの大学の条件は学部別の記事に掲載<br>'
               '<b>学部</b>　医学から英文学までの12学部。各大学で最も一般的なコース<br>'
               '<b>数値</b>　標準的なオファー（幅がある場合は高い方）をUCASポイント（A*=56、A=48、B=40）に換算した中央値。合格に必要な条件（最低ライン）であり、合格者の平均ではない<br>'
               '<b>時点</b>　2027年入学。2026年11月時点の各大学の公式サイトによる。確認できない項目と、学部がない大学は計算に含めない</div>' % n_uk)
    # 1. A Level grade by band
    rows = []; top = []; bot = []
    for m, ja in MAJ:
        cells = []
        for bn, lo, hi in BANDS:
            v, n = band_med(m, lo, hi, tar); cells.append(grade_td(v, n, '%s・%s' % (ja, bn)))
            if lo == 1: top.append((ja, v))
            if lo == 31: bot.append((ja, v))
        rows.append('<tr><th>%s</th>%s</tr>' % ('<a href="%s">%s</a>' % (mpath(m), ja), ''.join(cells)))
    out.append(C.step(1, 'alevel', '学部ごとに必要な成績', 'イギリス上位50校の標準的なオファー（中央値）'))
    out.append(heat_table('学部×順位帯で見るA Levelの標準オファー', '各学部・順位帯の大学の中央値。色が濃いほど高い成績', [b[0] for b in BANDS], rows, 'hz gb'))
    out.append('<div class="tl-wrap rise"><div><p class="tl-h">上位10校（中央値）</p>%s</div><div><p class="tl-h">31〜50位（中央値）</p>%s</div></div>'
               % (tier_list(top, gname), tier_list(bot, gname)))

    # 2. A Level required subjects
    rows = []
    for m, ja in MAJ:
        if m == 'ECON':
            al = [r for k, r in uk_rows(m) if r.get('al')]
            cnt = {'MATH': (sum(1 for r in al if '数学' in r['al']), len(al))}
        else:
            cnt = req_counts([r.get('req') for k, r in uk_rows(m)])
        n = max(v[1] for v in cnt.values())
        cells = [heat_td(ja, *cnt[key], '%s・%s' % (ja, cn)) if key in cnt else '<td class="hz-na">—</td>' for key, cn in REQ_COLS]
        rows.append('<tr><th>%s<small>%d校</small></th>%s</tr>' % (ja, n, ''.join(cells)))
    out.append(C.step(2, 'alevel-subj', '学部ごとに必須の科目', 'イギリス上位50校で、その科目を必須にしている大学の割合'))
    out.append(heat_table('A Levelで必須とされる科目', '必須科目を確認できた大学のうち、その科目を必須にしている大学の割合。「理系から1科目」は生物・化学・物理・数学などから1つを選ぶ条件。経済学は、オファーに数学の記載がある大学の割合のみ',
                          [c for _, c in REQ_COLS], rows))

    out += country_section('al', 3)
    out += links_block(4, SCORES, '国際バカロレア（IB）は何点必要？')
    return '\n'.join(out)

def ib_body():
    out = []
    out.append('<div class="us-note rise"><b>アメリカの大学が載っていない理由</b>アメリカの大学は、成績・エッセイ・課外活動などをあわせて評価するため、IBの総合点の基準を学部ごとに公表していません。そのため、この記事では点数の基準を公表しているイギリス・オーストラリア・カナダ・シンガポールの大学を比べています。アメリカの大学のSAT・英語試験の扱いは<a href="%s">SAT・英語試験はどのくらい必要？</a>へ</div>' % TESTS)
    n_uk = len(SS.UNIS)
    out.append('<div class="rq-scope rise"><b>対象</b>　イギリスの上位50校（the Complete University Guide 2027、同順位を含め%d校）、オーストラリアとカナダの各国上位5校（QS世界大学ランキング2027）、シンガポールの国立5大学<br>'
               '<b>学部</b>　医学から英文学までの12学部。各大学で最も一般的なコース<br>'
               '<b>数値</b>　中央値。合格に必要な条件（最低ライン）であり、合格者の平均点ではない<br>'
               '<b>時点</b>　2027年入学。2026年11月時点の各大学の公式サイトによる。確認できない項目と、学部がない大学は計算に含めない</div>' % n_uk)
    # 3. IB total by band + AU/CA
    cols = [b[0] for b in BANDS] + ['オーストラリア', 'カナダ']
    rows = []; top = []
    for m, ja in MAJ:
        cells = []
        for bn, lo, hi in BANDS:
            v, n = band_med(m, lo, hi, ib_uk); cells.append(grade_td(v, n, '%s・%s' % (ja, bn), 'ib'))
            if lo == 1: top.append((ja, v))
        for c, cn in CTY[:2]:
            v, n = acs_ib_med(m, c); cells.append(grade_td(v, n, '%s・%s' % (ja, cn), 'ib'))
        rows.append('<tr><th>%s</th>%s</tr>' % ('<a href="%s">%s</a>' % (mpath(m), ja), ''.join(cells)))
    out.append(C.step(1, 'ib', '学部ごとに必要な総合点', 'イギリス上位50校と、オーストラリア・カナダの主要5校（中央値）'))
    out.append(heat_table('学部×国で見るIBの総合点', 'イギリスは標準的なオファー、オーストラリアは入学の目安や保証点、カナダは大学が示す目安の下限。シンガポールの大学は、IBの点数の目安を学部ごとに公表していません',
                          cols, rows, 'hz gb ib'))
    out.append('<div class="tl-wrap rise"><div><p class="tl-h">イギリス上位10校（中央値）</p>%s</div></div>' % tier_list(top, lambda v: '%s点' % AN.fmt(v)))

    # 4. IB prerequisites AU/CA/SG
    ib_cols = [('MATH', '数学'), ('PHY', '物理'), ('CHEM', '化学'), ('BIO', '生物'), ('OPT', '理系から1科目'), ('ENG', '英語'), ('NONE', '指定なし')]
    rows = []
    for m, ja in MAJ:
        reqs = [r.get('req') for c, k, r in acs_rows(m)]
        cnt = req_counts(reqs); n = cnt['MATH'][1]
        cells = [heat_td(ja, *cnt[key], '%s・%s' % (ja, cn)) for key, cn in ib_cols]
        rows.append('<tr><th>%s<small>%d校</small></th>%s</tr>' % (ja, n, ''.join(cells)))
    out.append(C.step(2, 'ib-subj', '学部ごとに必須の科目', 'オーストラリア・カナダ・シンガポールの主要大学で、その科目を必須にしている大学の割合'))
    out.append(heat_table('IBで必須とされる科目', 'IBの科目条件を確認できた大学のうち、その科目を必須にしている大学の割合。HLかSLかの指定は大学により異なります。イギリスの大学の科目条件は、A Levelの記事を参照',
                          [c for _, c in ib_cols], rows))

    out += country_section('ib', 3)
    out += links_block(4, SCORES_AL, 'A Levelは何点必要？')
    return '\n'.join(out)

# ---------------- ② major article ----------------
AP_UK = USJ.UK_AP
def major_body(m, ja):
    out = []
    ukr = uk_rows(m)
    na = [k for k in SS.UNIS if (SS.U.S.get((k, m)) or {}).get('course') == SS.U.NA]
    out.append('<div class="rq-scope rise"><b>対象</b>　イギリスの上位50校（the Complete University Guide 2027）と、オーストラリア・カナダ・シンガポールの主要5校。イギリスで%sのコースがあるのは%d校、ないのは%d校<br>'
               '<b>数値</b>　合格に必要な条件（最低ライン）。合格者の平均ではない<br>'
               '<b>時点</b>　2027年入学（一部は2024〜2026年入学の掲載）。2026年11月時点の各大学の公式サイトによる。確認できない項目は「—」</div>' % (ja, len(ukr), len(na)))

    # 1 grades
    cells = []
    for bn, lo, hi in BANDS:
        v, n = band_med(m, lo, hi, tar); cells.append((bn, gname(v) if v else '—', n))
    ibc = []
    for bn, lo, hi in BANDS:
        v, n = band_med(m, lo, hi, ib_uk); ibc.append((bn, ('%s点' % AN.fmt(v)) if v else '—', n))
    for c, cn in CTY[:2]:
        v, n = acs_ib_med(m, c); ibc.append((cn, ('%s点' % AN.fmt(v)) if v else '—', n))
    def statrow(items):
        return '<div class="st-row rise">' + ''.join('<div class="st"><span>%s</span><b>%s</b><small>%d校の中央値</small></div>' % (a, b, n) if n else
                                                      '<div class="st"><span>%s</span><b>—</b><small>データなし</small></div>' % a for a, b, n in items) + '</div>'
    out.append(C.step(1, 'grades', '必要な成績', 'A LevelとIBの標準的なオファー（中央値）'))
    out.append('<p class="st-h">A Level（イギリス）</p>' + statrow(cells))
    out.append('<p class="st-h">国際バカロレア（IB）の総合点</p>' + statrow(ibc))

    # 2 subjects
    def bars(cnt, cols):
        rows = []
        for key, cn in cols:
            if key not in cnt: continue
            c, n = cnt[key]
            if not n: continue
            w = pct(c, n)
            rows.append('<div class="sbr"><span class="sb-l">%s</span><span class="sb-t"><i style="width:%d%%"></i></span><span class="sb-v">%d%%<small>%d校中%d校</small></span></div>' % (cn, w, w, n, c))
        return '<div class="sb-wrap">' + ''.join(rows) + '</div>'
    if m == 'ECON':
        al = [r for k, r in ukr if r.get('al')]
        cnt_uk = {'MATH': (sum(1 for r in al if '数学' in r['al']), len(al))}
        uk_note = 'オファーに数学の記載がある大学の割合'
    else:
        cnt_uk = req_counts([r.get('req') for k, r in ukr]); uk_note = '必須科目を確認できた大学のうち、その科目を必須にしている大学の割合'
    cnt_ib = req_counts([r.get('req') for c, k, r in acs_rows(m)])
    out.append(C.step(2, 'subjects', '必須の科目', 'その科目を必須にしている大学の割合'))
    out.append('<figure class="vz rise"><figcaption><b>A Level（イギリス上位50校）</b><small>%s</small></figcaption>%s</figure>' % (uk_note, bars(cnt_uk, REQ_COLS)))
    if cnt_ib['MATH'][1]:
        out.append('<figure class="vz rise"><figcaption><b>IB（オーストラリア・カナダ・シンガポール）</b><small>IBの科目条件を確認できた大学のうち、その科目を必須にしている大学の割合</small></figcaption>%s</figure>'
                   % bars(cnt_ib, [c for c in REQ_COLS if c[0] not in ('FM', 'HIST')]))

    # 3 tests
    T = {}
    for k, r in ukr:
        t = r.get('test') or ''
        if t and not t.startswith('なし') and '条件が変わる' not in t:
            for w in SJ.test_tokens(t): T.setdefault(w, []).append(k)
    out.append(C.step(3, 'tests', '入学試験', 'イギリス上位50校で、出願者全員に受験を求める試験'))
    if T:
        out.append('<div class="rq-t rq-mj">' + C.table(['試験', '課している大学'], [[w, '%d校：%s' % (len(set(ks)), '、'.join(SJ.SN.get(k, k) for k in sorted(set(ks), key=lambda k: SS.RANK[k])))] for w, ks in T.items()]) + '</div>')
    else:
        out.append('<p class="rnote">確認できた範囲では、イギリス上位50校で%sの出願者全員に入学試験を課している大学はありませんでした</p>' % ja)

    # 4 AP
    out.append(C.step(4, 'ap', 'AP（アドバンスト・プレイスメント）で出願する場合', 'イギリスの主な大学がAPに求める条件'))
    out.append('<ul class="ul2 rise">' + ''.join('<li><b>%s</b>：%s</li>' % (d['uni'], d['text']) for d in AP_UK) + '</ul>')
    if m in ('ENG', 'CS', 'PHYS', 'MATH'):
        eng = sorted([(en, d) for en, d in USJ.US50.items() if d.get('eng_kind') and d.get('eng') not in (None, '—')],
                     key=lambda x: (x[1]['eng_kind'] != '必須', rk_us[x[0]]))
        out.append(BR.more('アメリカの工学系で、高校に求められる科目', 'U.S. News上位50校のうち、条件を確認できた%d校' % len(eng), 'rq-mj', ['大学', '扱い', '高校で履修しておく科目'], [[jn(en), d['eng_kind'], d['eng']] for en, d in eng]))
    if m in ('MED', 'LAW'):
        out.append('<p class="rnote">アメリカとカナダでは、医学と法学は主に大学卒業後に進む専門課程（大学院）で学びます。オーストラリアでも、メルボルン大学のように大学院で学ぶ大学があります</p>')

    # 5 per-university tables
    head = ['順位', '大学', 'コース', 'A Level', 'IB', '必須科目', '入学試験']
    def ukrow(k, r):
        return [str(SS.RANK[k]), SS.JA[k], r.get('course') or '—', r.get('al') or '—', r.get('ib') or '—', r.get('req') or '—', r.get('test') or '—']
    out.append(C.step(5, 'list', '大学ごとの要件', 'イギリス上位50校と、オーストラリア・カナダ・シンガポールの主要5校'))
    out.append('<div class="rq-t rq-mj">' + C.table(head, [ukrow(k, r) for k, r in ukr if SS.RANK[k] <= 20]) + '</div>')
    rest = [ukrow(k, r) for k, r in ukr if SS.RANK[k] > 20]
    if rest: out.append(BR.more('イギリス21〜50位の%d校を表示' % len(rest), '', 'rq-mj', head, rest))
    arows = [[cn_of(c), UNIJA[(c, k)], r.get('course') or '—', r.get('al') or '—', ('%d点' % r['ib']) if r.get('ib') else '—', r.get('req') or '—', r.get('test') or r.get('note') or '—']
             for c, k, r in acs_rows(m)]
    if arows: out.append(BR.more('オーストラリア・カナダ・シンガポールの%d校を表示' % len(arows), '', 'rq-mj', ['国', '大学', 'コース', 'A Level', 'IB', '必須科目', '備考'], arows))
    out.append('<p class="rnote">要件は毎年見直されます。出願前に、必ず各大学の公式サイトで最新の情報を確認してください。ほかの学部との比較は<a href="%s">国際バカロレア（IB）は何点必要？</a>と<a href="%s">A Levelは何点必要？</a>、大学ごとの一覧は<a href="%s">出願要件データベース</a>へ</p>' % (SCORES, SCORES_AL, DB))
    return '\n'.join(out)

def cn_of(c): return dict(CTY)[c]
ja_us = {d['en']: d['ja'] for d in UD.US + UD2.US3}
rk_us = {d['en']: d['rank'] for d in UD.US + UD2.US3}
def jn(en): return re.sub(r'（.*?）', '', ja_us.get(en, en))

def major_sources(m):
    seen = set(); src = [(UK_RANK_SRC, 'The Complete University Guide：University League Tables 2027')]
    for k, r in uk_rows(m):
        for u in r.get('src') or []:
            if u not in seen: seen.add(u); src.append((u, '%s：%s' % (SS.KEY[k], u.split('//')[1].split('/')[0])))
    for c, k, r in acs_rows(m):
        for u in r.get('src') or []:
            if u not in seen: seen.add(u); src.append((u, '%s：%s' % (k, u.split('//')[1].split('/')[0])))
    for d in AP_UK:
        if d['src'] not in seen: seen.add(d['src']); src.append((d['src'], '%s：APの条件' % d['uni']))
    for c, u in A.RANK_SRC.items(): src.append((u, 'QS World University Rankings 2027（%s）' % dict(CTY)[c]))
    return src

CSS_X = '''
.us-note{border-left:4px solid var(--c,#16294d);background:#fff;border-radius:0 10px 10px 0;padding:14px 18px;margin:0 0 16px;font-size:14px;line-height:1.85;box-shadow:0 0 0 1px var(--line,#d9deea) inset}.us-note b{display:block;font-size:14.5px;color:var(--navy,#0b1f4b);margin-bottom:2px}.us-note a{color:var(--c,#16294d);font-weight:700}
.hz.umx{min-width:0;table-layout:fixed;width:100%}.hz.umx th:first-child{width:116px;min-width:0!important;text-align:left;font-size:12px;position:sticky;left:0;background:#fff;z-index:1}.hz.umx td{font-size:11px;padding:8px 1px;white-space:nowrap;min-width:0!important}
@media(max-width:760px){.hz.umx{min-width:760px}.hz.umx th:first-child{width:96px}}.hz.umx thead th{font-size:11px;white-space:nowrap}.hz.umx thead th a{color:inherit}
.mx-g th{background:#f3f5fa;font-size:12.5px;font-weight:700;color:var(--navy,#0b1f4b);text-align:left;padding:8px 10px!important}.mx-no{font-size:10.5px!important;color:var(--muted,#5c6984)}
.vz .mjq-p+.vz,.mjq-p+figure{margin-top:22px}
.cv-g{font-size:13.5px;font-weight:700;color:var(--navy,#0b1f4b);margin:16px 0 4px}.cv-g:first-child{margin-top:4px}.cv-g small{font-weight:500;color:var(--muted,#5c6984);font-size:11.5px;margin-left:8px}
.cv .sb-l small{display:block;font-size:10.5px;color:var(--muted,#5c6984)}.cv .sbr{grid-template-columns:170px 1fr 110px}.cv-na .sb-v{color:var(--muted,#5c6984);font-weight:500}
.mjq-p{font-size:14.5px;line-height:1.9;margin:14px 0 0}
@media(max-width:760px){.cv .sbr{grid-template-columns:104px 1fr 84px}}
.vf-wrap h3.acs-h,h3.acs-h{font-size:18px!important;font-weight:700;margin:40px 0 14px!important;color:var(--navy,#0b1f4b)!important}
.tl-wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:14px 0 26px}
.tl-wrap>div{border:1px solid var(--line,#d9deea);border-radius:12px;padding:14px 16px;background:#fff}
.tl-h{font-size:12.5px;font-weight:700;color:var(--muted,#5c6984);margin:0 0 8px}
.tlv{list-style:none;margin:0;padding:0}.tlv li{display:grid;grid-template-columns:96px 1fr;gap:10px;padding:6px 0;border-top:1px dashed var(--line,#e3e7f0);font-size:13.5px;line-height:1.6}
.tlv li:first-child{border-top:0}.tlv b{color:var(--navy,#0b1f4b)}
.vz-heat th a{color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
.hz.us{min-width:0;max-width:420px}
.mj-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin:8px 0 18px}
.mj-card{display:block;border:1px solid var(--line,#d9deea);border-radius:12px;padding:14px 16px;background:#fff;text-decoration:none;color:var(--navy,#0b1f4b)}
.mj-card b{display:block;font-size:15px}.mj-card span{display:block;font-size:12px;color:var(--muted,#5c6984);margin-top:4px}
.mj-card:hover,.mj-card:focus-visible{border-color:var(--c,#16294d)}
.st-h{font-size:13.5px;font-weight:700;margin:16px 0 8px;color:var(--navy,#0b1f4b)}
.st-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}
.st{border:1px solid var(--line,#d9deea);border-radius:10px;padding:10px 12px;background:#fff}
.st span{display:block;font-size:11.5px;color:var(--muted,#5c6984)}.st b{display:block;font-size:20px;color:var(--navy,#0b1f4b);margin:2px 0}.st small{font-size:10.5px;color:var(--muted,#5c6984)}
.sb-wrap{margin-top:8px}.sbr{display:grid;grid-template-columns:110px 1fr 92px;gap:10px;align-items:center;padding:4px 0;border-top:1px dashed var(--line,#e3e7f0)}.sbr:first-child{border-top:0}
.sb-l{font-size:13px}.sb-t{height:12px;background:#eef1f7;border-radius:6px;overflow:hidden}.sb-t i{display:block;height:100%;background:#2a78d6;border-radius:6px}
.sb-v{font-size:13px;font-weight:700;color:var(--navy,#0b1f4b)}.sb-v small{display:block;font-size:10.5px;font-weight:500;color:var(--muted,#5c6984)}
@media(min-width:760px){.rq-mj .etbl{table-layout:auto!important}.rq-mj .etbl th:nth-child(1),.rq-mj .etbl td:nth-child(1){white-space:nowrap}}
@media(max-width:760px){.vz-heat tbody th{min-width:7.6em!important;word-break:keep-all!important;overflow-wrap:normal!important}.hz.gb td{font-size:11px;padding-left:2px;padding-right:2px}.hz.gb{min-width:400px}}
@media(max-width:760px){.sbr{grid-template-columns:86px 1fr 74px}.hz.gb.ib{min-width:520px}}
'''

def write_page(path, title, desc, h1, lead, body, crumbs, faq, nxt, src, src_note, toc, js=True):
    url = M.page(path, title, desc, h1, 'コラム・大学進学', lead, body + ('\n' + AN.JS if js else ''), crumbs, faq=faq, nxt=nxt,
                 cta=('志望学部に合わせた準備を、相談したい方へ', 'IB・A Levelの科目選びから、志望校に必要な成績まで、学部から逆算した準備をご提案します。初回60分は無料体験です'),
                 src=src, src_note=src_note, nav=BR.M.COL_NAV, kind='uni', ld_type='Article', toc_items=toc)
    f = os.path.join(M.ROOT, path.strip('/'), 'index.html')
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<style id="rq-css">.*?</style>\n', '', s, flags=re.S)
    s = s.replace('</head>', BR.CSS_HEAD.replace('</style>', AN.CSS + SJ.CSS + CSS_X + '</style>') + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    return url

SRC_NOTE = '入学要件は、2026年11月時点の各大学の公式サイトによります。要件は変更されることがあるため、出願前に必ず各大学の公式サイトでご確認ください'

def scores_src(ib):
    src = [(UK_RANK_SRC, 'The Complete University Guide：University League Tables 2027')]
    if ib: src += [(u, 'QS World University Rankings 2027（%s）' % dict(CTY)[c]) for c, u in A.RANK_SRC.items()]
    seen = set(u for u, _ in src)
    for m, _ in MAJ:
        for k, r in uk_rows(m):
            for u in r.get('src') or []:
                if u not in seen: seen.add(u); src.append((u, '%s：%s' % (SS.KEY[k], u.split('//')[1].split('/')[0])))
        if ib:
            for c, k, r in acs_rows(m):
                for u in r.get('src') or []:
                    if u not in seen: seen.add(u); src.append((u, '%s：%s' % (UNIJA[(c, k)], u.split('//')[1].split('/')[0])))
    return src

def build_al():
    faq = [('ここに載っている成績を取れば合格できますか？', 'いいえ。ここに載っているのは各大学が示す標準的なオファーの中央値で、合格を保証するものではありません。実際の条件は大学とコースごとに確認してください'),
           ('A Levelは何科目必要ですか？', 'イギリスの大学の標準的なオファーは、3科目の成績で示されます。このページの成績も3科目分です')]
    nxt = [(SCORES, '国際バカロレア（IB）は何点必要？', '12学部別に見る総合点と必須科目', True),
           (mpath('MED'), '医学部に必要な成績と科目', '大学ごとの要件', False),
           (DB, '出願要件データベース', '5か国の大学を国・学部で絞り込める', False),
           ('/curriculum/cambridge/university/', 'A Levelで大学に出願するには？', 'イギリスの大学出願の基本', False)]
    u10 = [band_med(m, 1, 10, tar)[0] for m, _ in MAJ]; u3 = [band_med(m, 31, 50, tar)[0] for m, _ in MAJ]
    u10 = [x for x in u10 if x]; u3 = [x for x in u3 if x]
    lead = ('イギリスの大学がA Levelで求める成績は、順位と学部で大きく変わります。上位10校では学部ごとの中央値が%s〜%s、31〜50位では%s〜%sまで下がります。'
            '科目の条件も、数学や物理学ではほぼ全校が数学を必須にする一方、法学や経営学ではほとんど指定がありません。イギリス上位50校・12学部の入学要件から、学部ごとに必要な成績と必須科目を見ていきます'
            % (gname(min(u10)), gname(max(u10)), gname(min(u3)), gname(max(u3))))
    return write_page(SCORES_AL,
        'A Levelは何点必要？12学部別に見るイギリス上位50校の成績と必須科目',
        'イギリス上位50校がA Levelで求める成績と必須科目を、医学・工学・経済学・法学など12学部と順位帯ごとに比較。各国のトップ校の条件も並べて掲載（2027年入学）',
        'A Levelは<span class="nw">何点必要？</span>', lead, al_body(),
        [('コラム', '/column/'), ('大学進学', '/column/university/'), ('A Levelは何点必要？', SCORES_AL)], faq, nxt, scores_src(False), SRC_NOTE,
        [('alevel', '必要な成績'), ('alevel-subj', '必須の科目'), ('country', '国別に見ると'), ('majors', '学部別の記事')])

def build_ib():
    faq = [('ここに載っている点数を取れば合格できますか？', 'いいえ。ここに載っているのは各大学が示す標準的なオファーや目安の中央値で、合格を保証するものではありません。実際の条件は大学とコースごとに確認してください'),
           ('シンガポールの大学には、IBの点数の目安はありますか？', 'シンガポールの主要大学は、IBの点数の目安を学部ごとには公表していません。この記事では、シンガポールの大学は必須科目のみを扱っています')]
    nxt = [(SCORES_AL, 'A Levelは何点必要？', '12学部別に見る成績と必須科目', True),
           (mpath('MED'), '医学部に必要な成績と科目', '大学ごとの要件', False),
           ('/column/university/ib-scores/', '国内インターのIBスコア', '各校が公開している平均点', False),
           ('/ib/university/', 'IBで大学に出願するには？', '必要な点数の考え方', False)]
    uk = [v for v, n in (uni_med('ib', 'UK', k) for k in SS.UNIS if SS.RANK[k] <= 10) if v and n >= 3]
    au = [v for v, n in (uni_med('ib', 'AU', k) for k, _ in A.UNI['AU']) if v and n >= 3]
    medau = acs_ib_med('MED', 'AU')[0]; meduk = band_med('MED', 1, 10, ib_uk)[0]
    lead = ('海外の大学がIBで求める総合点は、国と学部によって大きく変わります。イギリスの上位10校は大学ごとの中央値で%s〜%s点、オーストラリアの上位5校は%s〜%s点。'
            'ただし医学では、オーストラリア（%s点）がイギリスの上位10校（%s点）を上回ります。イギリス上位50校とオーストラリア・カナダ・シンガポールの主要大学、12学部の入学要件から、必要な総合点と必須科目を見ていきます'
            % (AN.fmt(min(uk)), AN.fmt(max(uk)), AN.fmt(min(au)), AN.fmt(max(au)), AN.fmt(medau), AN.fmt(meduk)))
    return write_page(SCORES,
        '国際バカロレア（IB）は何点必要？12学部別に見る海外大学の総合点と必須科目',
        '国際バカロレア（IB）で海外の大学に必要な総合点と必須科目を、医学・工学・経済学・法学など12学部ごとに比較。イギリス上位50校とオーストラリア・カナダ・シンガポールの主要大学の入学要件による（2027年入学）',
        '国際バカロレア（IB）は<span class="nw">何点必要？</span>', lead, ib_body(),
        [('コラム', '/column/'), ('大学進学', '/column/university/'), ('国際バカロレア（IB）は何点必要？', SCORES)], faq, nxt, scores_src(True), SRC_NOTE,
        [('ib', '必要な総合点'), ('ib-subj', '必須の科目'), ('country', '国別に見ると'), ('majors', '学部別の記事')])

def build_major(m, ja):
    path = mpath(m)
    others = [(mpath(x), '%sに必要な成績と科目' % j, '', False) for x, j in MAJ if x != m][:3]
    nxt = [(SCORES, '国際バカロレア（IB）は何点必要？', '12学部の比較', True), (SCORES_AL, 'A Levelは何点必要？', '12学部の比較', False)] + others[:2]
    faq = [('ここに載っている成績を取れば合格できますか？', 'いいえ。ここに載っているのは各大学が示す標準的なオファーや目安で、合格を保証するものではありません。面接や入学試験、志望理由書などで選考する大学も多くあります'),
           ('大学ごとの最新の要件はどこで確認できますか？', '各大学の公式サイトのコースページで確認できます。このページの「大学ごとの要件」の表と出典から、各大学のページに進めます')]
    a10 = band_med(m, 1, 10, tar)[0]; i10 = band_med(m, 1, 10, ib_uk)[0]
    lead = (('%sに進むには、IBやA Levelでどのくらいの成績と、どの科目が必要なのか。イギリスの上位10校では、A Level %s・IB %s点が中心です。' % (ja, gname(a10), AN.fmt(i10))) if a10 and i10 else ('%sに進むには、IBやA Levelでどのくらいの成績と、どの科目が必要なのか。' % ja)) + \
           '必須の科目、入学試験、大学ごとの条件まで、イギリス上位50校とオーストラリア・カナダ・シンガポールの主要大学の入学要件から見ていきます'
    return write_page(path,
        '%sに必要な成績と科目｜国際バカロレア（IB）・A Level・AP（海外大学）' % ja,
        'イギリス上位50校とオーストラリア・カナダ・シンガポールの主要大学の、%sのコースに必要な国際バカロレア（IB）とA Levelの成績、必須科目、入学試験、APの条件。大学ごとの一覧つき（2027年入学）' % ja,
        '%sに必要な<span class="nw">成績と科目</span>' % ja, lead, major_body(m, ja),
        [('コラム', '/column/'), ('大学進学', '/column/university/'), (ja, path)], faq, nxt, major_sources(m), SRC_NOTE,
        [('grades', '必要な成績'), ('subjects', '必須の科目'), ('tests', '入学試験'), ('ap', 'APで出願する場合'), ('list', '大学ごとの要件')])

# ---------------- SAT / English tests article ----------------
def build_tests():
    html = AN.build_section()
    arts = re.findall(r'<article class="vf rise">.*?</article>', html, flags=re.S)
    keep = [arts[i] for i in (0, 1, 2, 6)]
    keep = [re.sub(r'<p class="vf-n">傾向 \d+</p>', '<p class="vf-n">傾向 %d</p>' % (i + 1), a) for i, a in enumerate(keep)]
    import acs_eng as AE
    keep.append('<h3 class="acs-h">オーストラリア・カナダ・シンガポールの主要大学では</h3>' + AE.findings(len(keep) + 1) + AE.table_html())
    head = html[:html.index('<article')]
    head = re.sub(r'<p class="rlead">.*?</p>', '', head, flags=re.S)
    head = re.sub(r'<div class="rq-scope rise">.*?</div>', '<div class="rq-scope rise"><b>順位帯</b>　1〜10位、11〜20位、21〜30位、31〜50位、51〜100位<br><b>数値</b>　中央値。公式サイトで確認できない大学は、その項目の計算に含めない<br><b>免除条件</b>　日本のインターナショナルスクールに通う、日本国籍の生徒を想定して分類</div>', head, flags=re.S)
    body = head + '\n'.join(keep)
    src = [(BR.US_RANK[0], 'U.S. News Best National Universities 2027（ランキング表：College Kickstart）'), (UK_RANK_SRC, 'The Complete University Guide：University League Tables 2027')]
    seen = set(u for u, _ in src)
    for d in BR.US + BR.US3 + BR.UK + BR.UK2 + BR.UK3:
        for u in d.get('src', []) or []:
            if u not in seen: seen.add(u); src.append((u, '%s：%s' % (d['en'], u.split('//')[1].split('/')[0])))
    for u, t in AE.sources():
        if u not in seen: seen.add(u); src.append((u, t))
    nxt = [(DB, '出願要件データベース', '5か国の大学を国・学部で絞り込める', True), ('/column/english/toefl/', 'TOEFL iBTとは？', '2026年の新形式とスコアの見方', False),
           ('/column/english/ielts/', 'IELTSとは？', '試験の形式とスコアの見方', False), (SCORES, '国際バカロレア（IB）は何点必要？', '12学部の比較', False)]
    faq = [('インターに通っていれば、TOEFLやIELTSは不要ですか？', '多くの大学で免除の対象になりますが、条件は大学ごとに違います。必要な在籍年数が異なり、在籍年数にかかわらず英語試験を求める大学もあるため、志望校ごとに確認してください')]
    lead = ('SAT・ACTを必須にする大学は、アメリカの上位10校では過半数、51〜100位では1割ほど。英語試験の基準も、順位によってはっきり分かれます。'
            'アメリカ・イギリスの上位100大学と、オーストラリア・カナダ・シンガポールの主要15校の入学要件から、SATと英語試験の傾向を読み解きます')
    return write_page(TESTS,
        'アメリカ・イギリス上位100大学のSAT・TOEFL・IELTSの傾向｜データで読む出願要件',
        'U.S. Newsとthe Complete University Guideのランキング上位100校と、オーストラリア・カナダ・シンガポールの主要15校の入学要件から読み解く、SAT・ACTの扱い、TOEFL・IELTSの基準、インター生の英語試験の免除条件の傾向（2027年秋入学）',
        'SAT・英語試験は<span class="nw">どのくらい必要？</span>', lead, body,
        [('コラム', '/column/'), ('大学進学', '/column/university/'), ('SAT・英語試験の傾向', TESTS)], faq, nxt, src, SRC_NOTE, [])

if __name__ == '__main__':
    print(build_ib()); print(build_al())
    for m, ja in MAJ: print(build_major(m, ja))
    print(build_tests())
