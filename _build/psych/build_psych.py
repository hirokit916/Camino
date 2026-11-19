# -*- coding: utf-8 -*-
"""AP Psychology page in the AP Japanese layout. Usage: python3 build_psych.py /home/claude/camino-v2"""
import os, re, sys
ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'econ'))
import build_econ as BE
import psych_data as P
BA, KPM, R = BE.BA, BE.KPM, BE.BA.R
step = BA.step
SRC = '出典：College Board「AP Psychology Course and Exam Description」（Effective Fall 2025）'
CIRC = '①②③④⑤⑥'
DATE = '2027年5月14日（金）午後'


def units_html():
    tiles = ''.join('<button type="button" class="aut%s" data-u="%s" aria-expanded="%s" aria-controls="aub-%s"><span class="aut-n">%s</span><b>%s</b><small lang="en">%s</small><i class="aut-pj">15〜25%%</i></button>'
                    % (' on' if n == '1' else '', n, 'true' if n == '1' else 'false', n, n, ja, en) for n, ja, en, tp in P.UNITS)
    bub = ''.join('<div class="aub%s" id="aub-%s" data-u="%s"><p class="aub-h">単元%s　%sで学ぶトピック</p><ol class="aub-q">%s</ol><p class="aub-t"><span>選択式での出題比率</span>15〜25%%</p></div>'
                  % (' on' if n == '1' else '', n, n, n, ja, ''.join('<li>%s</li>' % t for t in tp)) for n, ja, en, tp in P.UNITS)
    return (step(1, 'units', '5つの単元', '単元を押すと、その単元で学ぶトピックが表示されます') +
            '<p class="rlead">AP心理学は、大学の入門の心理学の授業1学期分にあたるコースです。5つの単元で心理学の概念を学ぶと同時に、<b>4つの科学的な実践（Science Practices）</b>、'
            '概念の応用、研究方法と研究デザイン、データの解釈、論証の力を身につけます。右上の数字は、選択式の問題に占める各単元の出題比率です</p>'
            '<div class="au rise"><div class="au-g">%s</div><div class="au-bs">%s</div></div>' % (tiles, bub) +
            '<p class="apu-src">%s。トピック名の日本語は当サイトによる</p>' % SRC)


def exam_html():
    rows = [('sec', 'Section I', '選択式問題', 'Multiple-Choice Questions', '75', '66.7%', '90分', ''),
            ('sec', 'Section II', '記述問題', 'Free-Response Questions', '2', '33.3%', '70分', ''),
            ('q', 'Q1', '論文分析問題（AAQ）', 'Article Analysis Question', '1', '16.65%', '25分', '研究論文の要約1本を読んで答える。7点。10分の読む時間を含む'),
            ('q', 'Q2', '根拠にもとづく問題（EBQ）', 'Evidence-Based Question', '1', '16.65%', '45分', '同じテーマの研究の要約3本を使って主張を論じる。7点。15分の読む時間を含む')]
    body = ''.join('<tr class="apex-%s"><th scope="row"><span class="apex-tag" lang="en">%s</span><b>%s</b><small lang="en">%s</small>%s</th>'
                   '<td data-l="問題数">%s</td><td data-l="比重">%s</td><td data-l="時間">%s</td></tr>'
                   % (k, t, ja, en, '<small class="apex-d">%s</small>' % d if d else '', n, w, tm) for k, t, ja, en, n, w, tm, d in rows)
    tbl = ('<div class="apex-w rise"><table class="apex"><thead><tr><th>問題の種類</th><th>問題数</th><th>比重</th><th>時間</th></tr></thead><tbody>%s</tbody></table>'
           '<p class="apr-src">%sの試験形式表をもとに作成</p></div>' % (body, SRC))
    return (step(2, 'exam', '試験の形式（2027年5月）', '試験時間は2時間40分。選択式75問と、論文を読んで答える記述2問') + tbl +
            '<ul class="apb rise"><li>2027年の試験日は%s。試験はすべてBluebookで受験する完全デジタル形式</li>'
            '<li>記述の2問はどちらも7点で、スコアに占める比重は同じ（各16.65%%）</li>'
            '<li>記述では、研究の要約（peer-reviewed researchの要約）を読み、研究方法・変数・倫理・統計を読み取ったり、根拠を使って主張を論じたりする</li></ul>' % DATE)


def overview_html():
    rows = ''.join('<div class="apu2-r"><div class="apu2-u"><span class="apu2-n">%s</span><div><b>%s</b><small lang="en">Unit %s: %s</small></div></div>'
                   '<div class="apu2-w"><span class="apu2-p">15〜25%%</span><span class="apu2-bar" aria-hidden="true"><i style="left:60%%;width:40%%"></i></span></div></div>'
                   % (n, ja, n, en) for n, ja, en, tp in P.UNITS)
    pr = ''.join('<li><b>%s</b>（%s）：選択問題の約<b>%s</b></li>' % x for x in P.PRACTICES)
    return (step(3, 'overview', '単元と試験の関係', '選択式は5単元から均等に、記述は研究を読み解く力を中心に評価') +
            '<p class="rlead">選択式の75問は、5つの単元がそれぞれ<b>15〜25%%</b>の幅で出題され、特定の単元に偏りません。記述の2問は単元ではなく<b>実践の力</b>を中心に評価され、'
            'College Boardが示す例題では、論文分析問題（AAQ）が単元2、根拠にもとづく問題（EBQ）が単元1の内容を主に扱っています</p>'
            '<div class="apu2 rise" role="table" aria-label="単元と選択式での出題比率"><div class="apu2-h"><span>単元</span><span>選択式セクションでの出題比率</span></div>%s</div>' % rows +
            '<p class="apr-src">%s</p>' % SRC +
            '<p class="rlead">選択問題では、4つの実践のうち3つが次の比率で評価されます。4つめの<b>論証（Argumentation）</b>は記述問題だけで評価され、'
            'AAQでは研究方法・データの解釈・論証、EBQでは概念の応用と論証が問われます</p><ul class="apb rise">%s</ul>' % pr)


def rubric_panel(pid, rows, name, en, scene, total):
    body = ''.join(R.row_html(r) for r in rows)
    body = body.replace('Typical responses that earn 1 points', 'Responses that earn this point').replace('Typical responses that earn 2 points', 'Responses that earn 2 points')
    body = body.replace('満点になる典型的な回答', '満点になる回答')
    for r in rows:
        body = body.replace('<div class="apc">', '<div class="apc" id="row-%s-%s">' % (pid, r[0].replace(' ', '').replace('(', '').replace(')', '')), 1)
    body = re.sub(r'<a class="apc-tip" href="#tip-(\d+)">TIP \d+</a>', lambda m: '<a class="apc-tip" href="#tip-%s-%s">コツ%s</a>' % (pid, m.group(1), CIRC[int(m.group(1)) - 1]), body)
    body = body.replace('Row ', 'Part ')
    strip = ''.join('<a href="#row-%s-%s" style="flex:1"><b>%d<small>点</small></b><span><i>Part %s</i>%s</span></a>'
                    % (pid, r[0].replace(' ', '').replace('(', '').replace(')', ''), r[3], r[0], r[1]) for r in rows)
    h = ('<h4 class="apr-t">Q%s %s　<small lang="en">%s・合計%d点</small></h4>' % (pid[1], name, en, total) +
         '<p class="rlead">%s。採点基準の枠組み（観点と配点）は毎年共通で、Decision Rulesの例は例題に合わせて書かれています</p>' % scene +
         '<div class="apk"><p class="apk-h">%d点の内訳<small>押すと、その観点の基準に移動します</small></p><div class="apk-b">%s</div></div>' % (total, strip) +
         '<figure class="apr rise"><figcaption class="apr-h"><span class="apr-sc">%d<small>点</small></span><span><b>Scoring Rubric for %s</b><small>英語は原文のまま。黄色のハイライトは満点の条件に関わる言葉</small></span></figcaption>%s'
         '<p class="apr-src">%sのScoring Rubric。© 2024 College Board. 英語は原文のまま。和訳とハイライトは当サイトによるもの</p></figure>' % (total, en, body, SRC))
    cards = ''.join('<article class="tp" id="tip-%s-%d" data-title="%s" data-sum="%s"><h4><span class="tp-no">コツ%s</span>%s</h4><p class="tp-rd">%s</p></article>'
                    % (pid, i, t, t, CIRC[i - 1], t, b) for i, (t, b) in enumerate(P.TIPS[pid], 1))
    tips = '<div class="aps-tips"><p class="aps-th">Q%sのコツ<small>採点基準に基づく当サイトの解説。College Board公式の攻略法ではありません</small></p><div class="tps">%s</div></div>' % (pid[1], cards)
    return h + tips


def verbs_panel():
    items = ''.join('<li><p class="apx-en" lang="en"><b>%s:</b> %s</p><p class="apx-ja">%s</p></li>' % v for v in P.VERBS)
    return ('<h4 class="apr-t">記述問題の指示語　<small lang="en">Task Verbs Used in the Free-Response Questions</small></h4>'
            '<p class="rlead">問題文の動詞で、求められる答え方が決まります。<b>Identify/State</b>は説明なしで答え、<b>Explain</b>は理由まで書きます</p>'
            '<div class="apx-top2"><ul class="apx-l">%s</ul></div><p class="apr-src">%s。© 2024 College Board. 英語は原文のまま。和訳は当サイトによるもの</p>' % (items, SRC))


def scoring_html():
    Pn = [('q1', 'Q1', '論文分析問題（AAQ）', '7点'), ('q2', 'Q2', '根拠にもとづく問題（EBQ）', '7点'), ('verbs', '指示語', '問題文の動詞', '定義')]
    nav = ''.join('<button type="button" class="aps-b%s" data-p="%s" aria-controls="ap-%s" aria-selected="%s"><span class="aps-q">%s</span><span class="aps-n">%s</span><span class="aps-pc">%s</span></button>'
                  % (' on' if k == 0 else '', p[0], p[0], 'true' if k == 0 else 'false', p[1], p[2], p[3]) for k, p in enumerate(Pn))
    bodies = {
     'q1': rubric_panel('q1', P.AAQ, '論文分析問題', 'Article Analysis Question (AAQ)', '研究論文の要約1本（例題はマルチビタミンの摂取と高齢者の認知機能を調べた実験）を読み、パートAからFの6つに答えます', 7),
     'q2': rubric_panel('q2', P.EBQ, '根拠にもとづく問題', 'Evidence-Based Question (EBQ)', '同じテーマの研究の要約3本（例題は中高生の始業時刻）を使い、主張を立てて、2つの根拠と心理学の概念で支えます', 7),
     'verbs': verbs_panel()}
    panels = ''.join('<section class="aps-p%s" id="ap-%s" aria-label="%s">%s</section>' % (' on' if k == 0 else '', p[0], p[2], bodies[p[0]]) for k, p in enumerate(Pn))
    return (step(4, 'scoring', '記述問題の採点基準と対策', '記述（スコア全体の33.3%）は、2問とも7点の共通の採点基準で採点') +
            '<p class="rlead">AP心理学の記述の2問には、<b>毎年共通の採点基準（Scoring Rubric）</b>があります。観点（Part）ごとに0〜1点または0〜2点で採点され、'
            '各観点は、何点ならどんな回答かを定めた<b>基準（Scoring Criteria）</b>と、点数を判断する目安の<b>典型的な回答（Decision Rules and Scoring Notes）</b>で書かれています。'
            'このページでは、満点の基準と満点になる回答を示し、それ未満は折りたたんでいます</p>'
            '<div class="apsx rise"><div class="apsx-h"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>'
            '<b>採点基準一覧</b><span class="apsx-sw" role="group" aria-label="表示の切り替え"><button type="button" data-m="rub" aria-pressed="true">採点の内訳</button><button type="button" data-m="tips" aria-pressed="false">コツ</button></span></div>'
            '<div class="aps"><nav class="aps-nav" aria-label="採点基準の問題"><p class="aps-h">記述問題<b>33.3%%</b><small>選択式（66.7%%）は採点基準なし</small></p>%s</nav><div class="aps-ps">%s</div></div></div>' % (nav, panels))


S = dict(slug='psychology', ja='心理学', en='Psychology', date=DATE)
TOCSUM = {
 'units': [('5つの単元', '、'.join(u[1] for u in P.UNITS)), ('4つの実践', '概念の応用、研究方法と研究デザイン、データの解釈、論証')],
 'exam': [('選択式66.7%', '75問・90分'), ('記述33.3%', '論文分析問題（AAQ）と根拠にもとづく問題（EBQ）の2問・70分。各7点'), ('完全デジタル', 'すべてBluebookで受験')],
 'overview': [('選択式は5単元から均等に', 'どの単元も15〜25%'), ('記述は実践の力が中心', '研究方法・データの解釈・論証・概念の応用を評価')],
 'scoring': [('毎年共通の採点基準', 'AAQはパートA〜Fの7点、EBQはパートA〜Cの7点'), ('研究を読み解く', '研究方法・操作的定義・統計・倫理・一般化を正確に'), ('根拠と心理学の概念', '出典を示した根拠を、授業で学んだ概念で主張につなげる')],
}
KP = [('試験は2時間40分', '選択式75問（66.7%%）と記述2問（33.3%%）。%s、すべてBluebookで受験' % DATE),
      ('5つの単元から均等に出題', '選択式では、どの単元も15〜25%。特定の単元に偏らない'),
      ('記述は研究を読み解く2問', '論文分析問題（AAQ）と根拠にもとづく問題（EBQ）。どちらも7点で、比重も同じ'),
      ('毎年共通の採点基準', '研究方法・変数・統計・倫理・一般化・論証（AAQ）と、主張・根拠・心理学の概念の応用（EBQ）が評価される'),
      ('概念は「応用」して初めて点になる', 'EBQの2点には、資料の言葉ではなく授業で学んだ心理学の概念で、根拠と主張をつなぐことが必要')]


def build():
    F = os.path.join(ROOT, 'subjects/ap/psychology/index.html')
    s = open(F, encoding='utf-8').read()
    ids = ('units', 'exam', 'overview', 'scoring', 'content')
    i = min(s.index('<div class="step" id="%s">' % k) for k in ids if '<div class="step" id="%s">' % k in s)
    w = s.rfind('<div class="ajs', 0, i)
    if w >= 0 and s.find('</div>', w, i) < 0:
        i = w
    j = s.index('<div class="step" id="camino">')
    parts = [units_html(), exam_html(), overview_html(), scoring_html()]
    s = s[:i] + '\n'.join('<div class="ajs%s">%s</div>' % (' ajs-alt' if k % 2 else '', p) for k, p in enumerate(parts)) + '\n' + s[j:]
    s = re.sub(r'(<div class="step" id="camino"><span class="step-n">)\d+', r'\g<1>5', s)
    toc = ('<li><a href="#units"><span>1</span>5つの単元</a></li><li><a href="#exam"><span>2</span>試験の形式</a></li>'
           '<li><a href="#overview"><span>3</span>単元と試験の関係</a></li><li><a href="#scoring"><span>4</span>記述問題の採点基準と対策</a></li>'
           '<li><a href="#camino"><span>5</span>家庭教師によるサポート</a></li>')
    s = re.sub(r'(<nav[^>]*class="otl"[^>]*><p>目次</p>(?:<p class="otl-note">.*?</p>)?<ol>).*?(</ol>)', lambda m: m.group(1) + toc + m.group(2), s, flags=re.S)
    for sid in ('apjp-css', 'apc-units', 'econ-css', 'kp-css', 'apjp-toc'):
        s = re.sub(r'<style id="%s">.*?</style>\n' % sid, '', s, flags=re.S)
    apu2 = re.search(r"CSS = '''(<style id=\"apc-units\">.*?</style>\n)'''", open(os.path.join(HERE, '..', 'apsci', 'ap_content.py'), encoding='utf-8').read(), re.S).group(1)
    s = s.replace('</head>', BA.css() + apu2 + BE.EXTRA_CSS + '</head>', 1)
    s = re.sub(r'<script id="apjp-js">.*?</script>\n', '', s, flags=re.S)
    s = s.replace('</body>', '<script id="apjp-js">' + open(os.path.join(HERE, '..', 'apjp', 'kt.js'), encoding='utf-8').read() + BA.APS_JS + BA.TOC_JS + '</script>\n</body>', 1)
    s = re.sub(r'<dl class="sj-facts">.*?</dl>', '', s, flags=re.S)
    s = re.sub(r'<!--kp-->.*?<!--/kp-->', '', s, flags=re.S)
    t = re.sub(r'<section class="aps-p" .*?</section>', '', s, flags=re.S)
    t = re.sub(r'<p class="apx-en".*?</p>', '', t, flags=re.S)
    mins = KPM.reading_minutes(t)
    lead_new = ('<p class="lead">College Boardが実施するAP 心理学（Psychology）を、最新のCourse and Exam Descriptionに沿って解説します。5つの単元、2027年5月の試験の形式、'
                '単元と試験の関係、記述問題の採点基準を、公式資料の英語と和訳で確認できます。Caminoでは、インター生・帰国子女を対象に、<b>AP 心理学の家庭教師</b>を行っています</p>')
    s = re.sub(r'<p class="lead">.*?</p>', lambda m: lead_new, s, count=1, flags=re.S)
    m = re.search(r'<p class="lead">.*?</p>', s, flags=re.S)
    s = s[:m.end()] + ('<!--kp--><p class="rtime">%s読了目安：約%d分</p><div class="kp"><ul>%s</ul></div><!--/kp-->'
                       % (KPM.CLOCK, mins, ''.join('<li><b>%s：</b>%s</li>' % x for x in KP))) + s[m.end():]
    s = s.replace('</head>', KPM.CSS.replace('<style id="kp-css">', '<style id="kp-css">.kp{max-width:none!important}') + '</head>', 1)
    desc = ('AP 心理学（Psychology）の5つの単元と出題比率、2027年5月の試験形式、記述問題（AAQ・EBQ）の採点基準を、College Boardの公式資料に沿って解説。'
            'インター生・帰国子女向けのAP家庭教師は対面／オンラインに対応。初回60分無料')
    s = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*', lambda m: m.group(1) + desc, s)
    BA.TOCSUM = TOCSUM
    s = BA.toc_with_summaries(s)
    open(F, 'w', encoding='utf-8').write(s)
    print('ok psychology', mins)


if __name__ == '__main__':
    build()
