# -*- coding: utf-8 -*-
"""Column: US/UK top university requirements (2027 entry). Usage: python3 build_req.py /home/claude/camino-v2"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'subj'))
sys.path.insert(0, HERE)
import common as M
from us_data import US, RANK_SRC as US_RANK
from uk_data import UK, UK2, RANK_SRC as UK_RANK
from us_data2 import US3
from uk_data2 import UK3
import analysis_html as AN
import subj_html as SJ

M.COL['uni'] = ('#16294d', '#e9edf5')
M.COL_NAV = M.COL_NAV.replace('<a href="/column/curriculum/" class="on" aria-current="page">', '<a href="/column/curriculum/">') \
                     .replace('<a href="/column/university/">', '<a href="/column/university/" class="on" aria-current="page">')
C = M.C
PATH = '/column/university/us-uk-requirements/'

UC = next(d for d in US if d['en'].endswith('Berkeley'))

import re as _re
def _n(x):
    x = _re.sub(r'min (\S+?) / 推奨 (\S+)', r'\1以上（推奨\2）', x)
    x = _re.sub(r'min (\S+)', r'\1以上', x)
    return x

def us_cell_scores(d):
    if d.get('uc'):
        d = UC
    t = d.get('toefl')
    parts = ['<span class="rq-elp">%s</span>' % d['elp']]
    if t:
        old, new = t
        if old: parts.append('TOEFL：' + _n(old))
        if new: parts.append('新TOEFL：' + _n(new))
    if d.get('ielts'):
        parts.append('IELTS：' + _n(d['ielts']))
    if d.get('det'):
        parts.append('Duolingo：' + _n(d['det']))
    if d.get('note'):
        parts.append('<small>%s</small>' % d['note'])
    return parts[0] + '<br>'.join(parts[1:])

def us_rows(lst):
    rows = []
    for d in lst:
        src = UC if d.get('uc') else d
        name = '<span class="rq-rk">%d位</span>%s<small>%s</small>' % (d['rank'], d['ja'], d['en'])
        ex = src.get('exempt', '—')
        rows.append((name, src['test'], us_cell_scores(d), '—' if ex in ('-', '') else ex))
    return rows

def uk_rows(lst):
    return [('<span class="rq-rk">%d位</span>%s<small>%s</small><small class="rq-course">コース：%s</small>' % (d['rank'], d['ja'], d['en'], d['course']),
             d['alevel'], d['ib'], d['ielts'] + (('<br><small>%s</small>' % d['note']) if d.get('note') else '')) for d in lst]

top_us = [d for d in US if d.get('tier') != 2]
t2_us = [d for d in US if d.get('tier') == 2]
us3a = [d for d in US3 if d['rank'] <= 50]
us3b = [d for d in US3 if d['rank'] > 50]
uk3a = [d for d in UK3 if d['rank'] <= 50]
uk3b = [d for d in UK3 if d['rank'] > 50]
ALLUS = US + US3


def count(pred, lst):
    return sum(1 for d in lst if pred(UC if d.get('uc') else d))

req = count(lambda d: d['test'].startswith('必須'), top_us)
req30 = count(lambda d: d['test'].startswith('必須'), top_us + t2_us)
req_rest = count(lambda d: d['test'].startswith('必須'), US3)
later = [d for d in top_us if not d.get('uc') and '必須）' in d['test'] and d['test'].startswith('任意')]
later_n = len(later)

CSS_HEAD = '''<style id="rq-css">
.rq-rk{display:inline-block;min-width:3.2em;font-size:11px;font-weight:700;color:#fff;background:var(--c);border-radius:999px;padding:1px 8px;margin-right:8px;text-align:center;vertical-align:1px}
.etbl th small,.etbl td small{display:block;font-size:11.5px;font-weight:400;color:var(--muted,#5c6984);line-height:1.6;margin-top:2px}
.rq-key{display:grid;gap:12px;margin:16px 0 4px}
.rq-key li{list-style:none;background:#fff;border:1px solid var(--line,#d8e0ee);border-left:4px solid var(--c);border-radius:10px;padding:14px 18px;line-height:1.85}
.rq-key li b{display:block;font-size:15.5px;color:var(--navy,#0b1f4b);margin-bottom:2px}
.rq-key{padding:0}
.rq-scope{background:var(--ct);border-radius:12px;padding:14px 18px;font-size:13.5px;line-height:1.9;margin:14px 0 0}
.rq-scope b{color:var(--navy,#0b1f4b)}
.etbl th small.rq-course{color:var(--c);font-weight:600;margin-top:4px}
.rq-elp{display:block;font-weight:700;color:var(--navy,#0b1f4b);margin-bottom:2px}
.rq-more{margin:14px 0 6px;border:1px solid var(--line,#d8e0ee);border-radius:14px;background:#fff}
.rq-more>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 18px;font-weight:700;color:var(--navy,#0b1f4b);font-size:15px}
.rq-more>summary::-webkit-details-marker{display:none}
.rq-more>summary::after{content:"";flex:none;width:9px;height:9px;border-right:2px solid var(--c);border-bottom:2px solid var(--c);transform:rotate(45deg);margin-top:-4px;transition:transform .2s}
.rq-more[open]>summary::after{transform:rotate(225deg);margin-top:4px}
.rq-more>summary small{display:block;font-size:12.5px;font-weight:500;color:var(--muted,#5c6984);margin-top:2px}
.rq-more>summary:focus-visible{outline:2px solid var(--c);outline-offset:2px;border-radius:12px}
.rq-more>.rq-t{padding:0 12px 12px}
.rq-band-h{margin:22px 0 0;font-size:14px;font-weight:700;color:var(--navy,#0b1f4b)}
.rq-band{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0 4px}
.rq-band div{background:#fff;border:1px solid var(--line,#d8e0ee);border-radius:12px;padding:12px 14px;font-size:13px;line-height:1.7}
.rq-band b{display:block;font-size:12px;color:var(--c);margin-bottom:2px}
.rq-band strong{display:block;font-size:15.5px;color:var(--navy,#0b1f4b)}
@media(max-width:760px){.rq-band{grid-template-columns:1fr 1fr}}
@media(min-width:760px){.rq-t .etbl{table-layout:fixed;min-width:0}.rq-t .etbl th,.rq-t .etbl td{overflow-wrap:anywhere;white-space:normal}.rq-us thead th:nth-child(1){width:29%}.rq-us thead th:nth-child(2){width:15%}.rq-us thead th:nth-child(3){width:30%}.rq-us thead th:nth-child(4){width:26%}.rq-uk thead th:nth-child(1){width:31%}.rq-uk thead th:nth-child(2){width:21%}.rq-uk thead th:nth-child(3){width:24%}.rq-uk thead th:nth-child(4){width:24%}}
</style>
'''

def more(title, sub, table_cls, head, rows):
    return ('<details class="rq-more"><summary><span>%s<small>%s</small></span></summary>' % (title, sub)
            + '<div class="rq-t %s">' % table_cls + C.table(head, rows) + '</div></details>')

def build():
    nus = len(ALLUS); nuk = len(UK) + len(UK2) + len(UK3)
    lead = ('アメリカとイギリスの上位100大学の入学要件を、大学ごとに引けるデータベースです。SAT・ACTの扱い、英語試験の基準と免除条件、国際バカロレア（IB）とA Levelの条件を、各大学の公式サイトの記載に基づいて掲載しています。'
            '出願前には、必ず各大学の公式サイトで最新の要件を確認してください')
    scope = ('<div class="rq-scope rise"><b>このページの対象</b>　2027年秋入学（2026〜27年の出願）の学部1年次の入学<br>'
             '<b>大学の選び方</b>　アメリカはU.S. News「Best National Universities 2027」、イギリスはthe Complete University Guide 2027の総合ランキングの上位100位まで。'
             '同順位があるため、アメリカは%d校、イギリスは%d校です<br>'
             '<b>イギリスの要件</b>　学部ごとに異なるため、代表例として経済学部（Economics）の基準を掲載。経済学部がない大学はその旨を記載<br>'
             '<b>確認日</b>　2026年11月。要件は毎年変わるため、最新の情報は必ず各大学の公式サイトで確認してください<br>'
             '<b>あわせて読む</b>　学部ごとの成績と科目は<a href="/column/university/ib-scores-by-major/">国際バカロレア（IB）は何点必要？</a>と<a href="/column/university/a-level-scores-by-major/">A Levelは何点必要？</a>、SATと英語試験の傾向は<a href="/column/university/sat-english-tests/">SAT・英語試験はどのくらい必要？</a>へ</div>') % (nus, nuk)
    band = ('<div class="rq-band rise">'
            '<div><b>1〜20位</b><strong>A*AA・IB 36〜42点</strong>数学はほぼ必須</div>'
            '<div><b>21〜30位</b><strong>AAA〜AAB・IB 34〜36点</strong>A*AAの大学も</div>'
            '<div><b>31〜50位</b><strong>AAB〜BBC・IB 30〜34点</strong>QMULはAAA・36点</div>'
            '<div><b>51〜100位</b><strong>BBC前後・IB 26〜30点</strong>UCASポイント112前後</div></div>')
    key = [
        ('SAT・ACTが必要な大学は、上位ほど多い',
         'U.S. Newsの上位30校では%d校がSAT・ACTを必須としているのに対し、31〜100位では%d校中%d校です。さらにプリンストン、コロンビア、ノートルダムは2028年秋入学から、ヴァンダービルトは2029年秋入学から必須に戻すと発表しています。'
         'トップ校を目指すなら、いま高校2年生（G11）以下の生徒はSAT・ACTを受ける前提で準備を進めるのが安全です。一方、カリフォルニア大学（UC）の各校はSAT・ACTを合否に使いません' % (req30, len(US3), req_rest)),
        ('新しいTOEFLでは、上位30校は「5.0〜5.5」、31〜100位は「4.0〜4.5」が目安',
         '2026年1月からTOEFL iBTのスコアが1〜6に変わりました。MIT、イェール、カリフォルニア工科大学、デューク、コーネルなど上位校は5.0以上を目安にし、ブラウン、エモリー、ノートルダムは5.5です。'
         '31〜100位の多くは最低点を4.0〜4.5としており、ここでも順位による差がはっきり表れています。なお、オックスフォード大学は2026年1月21日以降に受けたTOEFLを、審査が終わるまで受け付けていません'),
        ('インター生でも、英語試験が免除されるとは限らない',
         '多くの大学は「英語で授業を行う学校に通っている」場合に英語試験を免除しますが、必要な在籍年数は大学ごとに違います。'
         'イェール、ダートマス、ライスは2年、ペンシルベニア、プリンストン、タフツは3年、コーネル、エモリー、ノースイースタンは4年です。'
         'フォーダム大学のように、英語が母語でない場合は在籍年数にかかわらず英語試験を求める大学もあります'),
        ('イギリスは、順位ごとに求められる成績がはっきり分かれる',
         '経済学部で比べると、上位20校はA Level A*AA・IB 36〜42点が標準で、ほぼすべてで数学が必須です。21〜30位はAAA〜AAB・IB 34〜36点、31〜50位はAAB〜BBC・IB 30〜34点、51〜100位はBBC前後（UCASポイント112前後）・IB 26〜30点が中心です。'
         'IELTSも、上位校の6.5〜7.5に対して、100位前後では6.0（各5.5以上）が一般的です'),
        ('学部によって、必要な成績と科目は大きく違う',
         'イギリス上位50校を12学部で比べると、上位10校では数学がA*A*A、生物学はAABと、同じ順位帯でも学部で差があります。31〜50位では多くの学部がABB〜BBBまで下がる一方、医学部はAAAのままで、全校がUCATを課します。'
         '数学・物理学・機械工学では、ほぼすべての大学が数学を必須にしています。'
         '法学や経営学は科目の指定がない大学が大半です。理系の学部を考えているなら、IBやA Levelの科目を選ぶ前に、志望学部の必須科目を確認しておく必要があります'),
        ('IBの英語Aで、英語の要件を満たせる大学も',
         'LSEはIBの英語A（HL）を取っていれば成績を問わず、SLなら6以上で英語の要件を満たせます。リーズ大学も英語A（SL・HL）5以上を認めています。'
         'アメリカでも、マイアミ大学はAP・IB HLの英語でAかB、レンセラー工科大学はIB英語A HL6以上で英語試験を免除します。IELTSやTOEFLを受ける前に、志望校がIBの英語の成績を認めるかを確認しておくと、受験の負担を減らせます'),
    ]
    keyhtml = '<ul class="rq-key">' + ''.join('<li class="rise"><b>%s</b>%s</li>' % kv for kv in key) + '</ul>'
    us_head = ['大学', 'SAT・ACT', '英語試験と基準・目安', '英語試験が免除される条件']
    uk_head = ['大学（経済学部のコース）', 'A Level', '国際バカロレア（IB）', '英語（IELTSなど）']
    note_us = '<p class="rnote">「以上」は大学が定める最低点、「目安」「推奨」は合格者に多い点数や大学が勧める点数で、足切りではありません。「TOEFL」は2026年1月20日までに受けた0〜120点のスコア、「新TOEFL」は2026年1月21日以降の1〜6のスコアです</p>'
    body = [
        scope,
        C.step(1, 'us-top', 'アメリカの上位20校', 'U.S. News「Best National Universities 2027」1〜20位（同順位を含め22校）'),
        '<div class="rq-t rq-us">' + C.table(us_head, us_rows(top_us)) + '</div>', note_us,
        C.step(2, 'us-next', 'アメリカの21〜30位', 'U.S. News「Best National Universities 2027」21〜30位（8校）'),
        '<div class="rq-t rq-us">' + C.table(us_head, us_rows(t2_us)) + '</div>',
        C.step(3, 'us-50', 'アメリカの31〜50位', 'U.S. News「Best National Universities 2027」31〜49位（同順位を含め%d校）' % len(us3a)),
        more('31〜50位の%d校を表示' % len(us3a), 'ボストン・カレッジ、ニューヨーク大学、テキサス大学オースティン校など', 'rq-us', us_head, us_rows(us3a)),
        C.step(4, 'us-100', 'アメリカの51〜100位', 'U.S. News「Best National Universities 2027」52〜100位（同順位を含め%d校）' % len(us3b)),
        more('51〜100位の%d校を表示' % len(us3b), 'パデュー大学、ジョージ・ワシントン大学、テキサスA&M大学など', 'rq-us', us_head, us_rows(us3b)),
        C.step(5, 'uk-top', 'イギリスの上位20校', 'the Complete University Guide 2027 総合1〜20位。経済学部（Economics）の標準的な入学要件'),
        '<div class="rq-t rq-uk">' + C.table(uk_head, uk_rows(UK)) + '</div>',
        '<p class="rnote">イギリスの大学は、学部ごとに必要な成績と科目が違います。医学・工学・法学など12学部の要件は<a href="/column/university/a-level-scores-by-major/">A Levelは何点必要？</a>で比べられます</p>',
        C.step(6, 'uk-next', 'イギリスの21〜30位', 'the Complete University Guide 2027 総合21〜30位'),
        '<div class="rq-t rq-uk">' + C.table(uk_head, uk_rows(UK2)) + '</div>',
        C.step(7, 'uk-50', 'イギリスの31〜50位', 'the Complete University Guide 2027 総合31〜50位（同順位を含め%d校）' % len(uk3a)),
        more('31〜50位の%d校を表示' % len(uk3a), 'クイーン・メアリー、ロイヤル・ホロウェイ、レディング大学など', 'rq-uk', uk_head, uk_rows(uk3a)),
        C.step(8, 'uk-100', 'イギリスの51〜100位', 'the Complete University Guide 2027 総合52〜98位（同順位を含め%d校）' % len(uk3b)),
        more('51〜100位の%d校を表示' % len(uk3b), 'シティ・セントジョージズ、ケント大学、SOAS など', 'rq-uk', uk_head, uk_rows(uk3b)),
        '<p class="rnote">「公式サイトで確認」は、公式サイトから確認できる情報が十分に得られなかった項目です。不確かな数字は載せていません。芸術系や農学系の大学など、経済学部がない大学はその旨を記載しています</p>',
    ]
    faq = [
        ('ランキングはどれを使っていますか？', 'アメリカはU.S. News「Best National Universities 2027」、イギリスはthe Complete University Guide 2027の総合ランキングです。どちらもそれぞれの国で広く参照されているランキングで、このページではそれぞれ上位100位までを載せています'),
        ('インターに通っていれば、TOEFLやIELTSは不要ですか？', '多くの大学で免除の対象になりますが、条件は大学ごとに違います。英語で授業を行う学校に2年以上、3年以上、4年以上など、必要な在籍年数が異なり、在籍年数にかかわらず英語試験を求める大学もあるため、志望校ごとに確認してください'),
        ('イギリスの大学には、SATは必要ですか？', 'イギリスの大学は、主にA LevelやIBの成績で選考します。このページで紹介したイギリスの大学の経済学部は、A LevelとIBの成績を入学要件としています'),
        ('ここに載っている点数を取れば合格できますか？', 'いいえ。ここに載っているのは出願や入学の基準・目安で、合格を保証するものではありません。アメリカの大学は成績や課外活動、エッセイなどを総合的に評価し、イギリスの大学も多くの場合、予想成績や志望理由書で選考します'),
    ]
    nxt = [('/column/university/ib-scores-by-major/', '国際バカロレア（IB）は何点必要？', '12学部別に見る総合点と必須科目', True), ('/column/university/a-level-scores-by-major/', 'A Levelは何点必要？', '12学部別に見る成績と必須科目', False),
           ('/column/university/sat-english-tests/', 'SAT・英語試験はどのくらい必要？', '上位100大学のデータから', False),
           ('/column/destinations/', '同じインターでも、進学先の国はこんなに違う？', '各校の進学先を国・地域ごとに比較', False),
           ('/column/english/toefl/', 'TOEFL iBTとは？', '2026年の新形式とスコアの見方', False)]
    src = [(US_RANK[0], 'U.S. News Best National Universities 2027（ランキング表：College Kickstart）'), (US_RANK[1], 'U.S. News 2027 上位50校の一覧（Ivy Talent Education）'),
           ('https://poetsandquantsforundergrads.com/news/u-s-news-best-colleges-ranking-2027-mit-ends-princetons-long-run-at-the-top/2/', 'U.S. News 2027 上位100校の一覧（Poets&Quants for Undergrads）'),
           (UK_RANK[0], 'The Complete University Guide：University League Tables 2027')]
    seen = set(u for u, _ in src)
    for d in US + US3 + UK + UK2 + UK3:
        for u in d.get('src', []) or []:
            if u not in seen:
                seen.add(u); src.append((u, '%s：%s' % (d['en'], u.split('//')[1].split('/')[0])))

    M.TODAY = '2026-11-16'
    url = M.page(PATH,
           'アメリカ・イギリス上位100大学の出願要件データベース｜SAT・TOEFL・IELTS・国際バカロレア（IB）・A Level',
           'U.S. Newsとthe Complete University Guideのランキング上位100校（アメリカ%d校・イギリス%d校）について、SAT・ACTの扱い、TOEFL・IELTSの基準、英語試験の免除条件、国際バカロレア（IB）とA Levelの入学要件を、各大学の公式サイトで確認して一覧にしました（2027年秋入学）' % (nus, nuk),
           'アメリカ・イギリス上位100大学の<span class="nw">出願要件データベース</span>',
           'コラム・大学進学', lead, '\n'.join(body),
           [('コラム', '/column/'), ('大学進学', '/column/university/'), ('米英上位100大学の出願要件データベース', PATH)],
           faq=faq, nxt=nxt,
           cta=('志望校に合わせた準備を、相談したい方へ', 'SAT・英語試験・IBやA Levelの成績まで、志望校から逆算した準備をご提案します。初回60分は無料体験です'),
           src=src, src_note='入学要件は、2026年11月時点の各大学の公式サイト（一部はUCASの公式コースページ）によります。ランキングはU.S. Newsとthe Complete University Guideの公開情報によります。要件は変更されることがあるため、出願前に必ず各大学の公式サイトでご確認ください',
           nav=M.COL_NAV, kind='uni', ld_type='Article',
           toc_items=[('us-top', 'アメリカ1〜20位'), ('us-next', 'アメリカ21〜30位'), ('us-50', 'アメリカ31〜50位'), ('us-100', 'アメリカ51〜100位'),
                      ('uk-top', 'イギリス1〜20位'), ('uk-next', 'イギリス21〜30位'), ('uk-50', 'イギリス31〜50位'), ('uk-100', 'イギリス51〜100位')])
    f = os.path.join(M.ROOT, PATH.strip('/'), 'index.html')
    s = open(f, encoding='utf-8').read()
    import re as R2
    s = R2.sub(r'<style id="rq-css">.*?</style>\n', '', s, flags=R2.S)
    s = s.replace('</head>', CSS_HEAD.replace('</style>', AN.CSS + '</style>') + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    print(url, nus, nuk, req30, req_rest)

if __name__ == '__main__':
    build()
