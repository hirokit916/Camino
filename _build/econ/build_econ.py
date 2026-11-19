# -*- coding: utf-8 -*-
"""AP Micro/Macroeconomics pages in the AP Japanese layout. Usage: python3 build_econ.py /home/claude/camino-v2"""
import os, re, sys
ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'apjp'))
sys.path.insert(0, os.path.join(HERE, '..', 'univreq'))
import build_apjp as BA
import keypoints as KPM
import econ_data as D

step = BA.step
SRC = '出典：College Board「AP %s Course and Exam Description」（Effective Fall 2026）'


def units_html(S):
    tiles = ''.join('<button type="button" class="aut%s" data-u="%s" aria-expanded="%s" aria-controls="aub-%s"><span class="aut-n">%s</span><b>%s</b><small lang="en">%s</small><i class="aut-pj">%d〜%d%%</i></button>'
                    % (' on' if n == '1' else '', n, 'true' if n == '1' else 'false', n, n, ja, en, lo, hi) for n, ja, en, lo, hi, tp in S['units'])
    bub = ''.join('<div class="aub%s" id="aub-%s" data-u="%s"><p class="aub-h">単元%s　%sで学ぶトピック</p><ol class="aub-q">%s</ol><p class="aub-t"><span>選択式での出題比率</span>%d〜%d%%</p></div>'
                  % (' on' if n == '1' else '', n, n, n, ja, ''.join('<li>%s</li>' % t for t in tp), lo, hi) for n, ja, en, lo, hi, tp in S['units'])
    return (step(1, 'units', '6つの単元', '単元を押すと、その単元で学ぶトピックが表示されます') +
            '<p class="rlead">AP%sは、大学の入門の%sの授業1学期分にあたるコースです。6つの単元は、<b>4つの大きな考え方（Big Ideas）</b>、%sを軸に組み立てられています。'
            '右上の数字は、選択式の問題に占める各単元の出題比率です</p>' % (S['ja'], S['ja'], '、'.join(S['bigideas'])) +
            '<div class="au rise"><div class="au-g">%s</div><div class="au-bs">%s</div></div>' % (tiles, bub) +
            '<p class="apu-src">%s。トピック名の日本語は当サイトによる</p>' % (SRC % S['en']))


def exam_html(S):
    rows = [('sec', 'Section I', '選択式問題', 'Multiple-choice questions', '60', '66.65%', '70分', ''),
            ('sec', 'Section II', '記述問題', 'Free-response questions', '3', '33.35%', '60分', '10分の読む時間を含む'),
            ('q', 'Q1', '長い記述問題', 'Long', '', '10点', '', 'グラフ・説明・計算を組み合わせた大問'),
            ('q', 'Q2', '短い記述問題', 'Short', '', '5点', '', ''),
            ('q', 'Q3', '短い記述問題', 'Short', '', '5点', '', '')]
    body = ''.join('<tr class="apex-%s"><th scope="row"><span class="apex-tag" lang="en">%s</span><b>%s</b><small lang="en">%s</small>%s</th>'
                   '<td data-l="問題数">%s</td><td data-l="比重・配点">%s</td><td data-l="時間">%s</td></tr>'
                   % (k, t, ja, en, '<small class="apex-d">%s</small>' % d if d else '', n, w, tm) for k, t, ja, en, n, w, tm, d in rows)
    tbl = ('<div class="apex-w rise"><table class="apex"><thead><tr><th>問題の種類</th><th>問題数</th><th>比重・配点</th><th>時間</th></tr></thead><tbody>%s</tbody></table>'
           '<p class="apr-src">%sの試験形式表をもとに作成</p></div>' % (body, SRC % S['en']))
    return (step(2, 'exam', '試験の形式（2027年5月）', '試験時間は2時間10分。選択式のSection Iのあと、記述式のSection II') + tbl +
            '<ul class="apb rise"><li>2027年の試験日は%s。選択問題はBluebookで解答し、記述問題は紙の解答冊子に手書きで答えるハイブリッド形式</li>'
            '<li>四則演算の電卓（four-function calculator）は、両方のセクションで使える</li>'
            '<li>記述問題は長い問題1問（10点）と短い問題2問（各5点）。グラフを描く問題が、記述の配点の30〜50%%を占める</li></ul>' % S['date'])


def overview_html(S):
    top = max(u[4] for u in S['units'])
    rows = ''.join('<div class="apu2-r"><div class="apu2-u"><span class="apu2-n">%s</span><div><b>%s</b><small lang="en">Unit %s: %s</small></div></div>'
                   '<div class="apu2-w"><span class="apu2-p">%d〜%d%%</span><span class="apu2-bar" aria-hidden="true"><i style="left:%.1f%%;width:%.1f%%"></i></span></div></div>'
                   % (n, ja, n, en, lo, hi, lo / top * 100, (hi - lo) / top * 100) for n, ja, en, lo, hi, tp in S['units'])
    skills = ''.join('<li><b>%s</b>（%s）：選択問題の<b>%s</b></li>' % (j, e, p) for j, e, p in S['mc_skills'])
    fu = S['frq_units']
    return (step(3, 'overview', '単元と試験の関係', '選択式は単元ごとの比率が決まっていて、記述は複数の単元をまたいで出題') +
            '<p class="rlead">選択式の60問は、単元ごとに出題比率の幅が決められています。一方、記述問題は<b>1問の中で複数の単元を組み合わせる</b>のが特徴で、'
            'College Boardが示す例題では、Q1（長い問題）が単元%s、Q2（短い問題）が単元%sの内容を扱っています</p>' % (fu['q1'], fu['q2']) +
            '<div class="apu2 rise" role="table" aria-label="単元と選択式での出題比率"><div class="apu2-h"><span>単元</span><span>選択式セクションでの出題比率</span></div>%s</div>' % rows +
            '<p class="apr-src">%s</p>' % (SRC % S['en']) +
            '<p class="rlead">選択問題は、単元とは別に、次の3つの力（Skill Categories）の配分も決まっています。また、選択問題の<b>%s</b>が、数値の分析や計算を含みます</p>'
            '<ul class="apb rise">%s</ul>' % (S['mc_num'], skills))


def q_panel(S, pid):
    Q = S['qs'][pid]
    rows, strip = [], []
    for part, label, pts in Q['parts']:
        n = len(pts)
        tasks = []
        for p in pts:
            if p[2] not in tasks: tasks.append(p[2])
        pills = ''.join('<a class="apc-tip" href="#tip-%s-%s">%s</a>' % (pid, t, D.TASK[t][0]) for t in tasks)
        items = ''.join('<li><p class="apx-en" lang="en">%s</p><p class="apx-ja">%s</p><p class="eqt"><span>%s</span><small lang="en">Task type: %s</small><small>Skill %s</small><b>1点</b></p></li>'
                        % (en, ja, D.TASK[t][0], D.TASK[t][1], sk) for en, ja, t, sk in pts)
        rows.append('<div class="apc" id="row-%s-%s"><div class="apc-h"><span class="apc-p">%d<small>点</small></span><b>(%s)%s</b><span class="apc-ts">%s</span></div>'
                    '<div class="apx-top2"><ul class="apx-l">%s</ul></div></div>' % (pid, part, n, part, '　' + label if label else '', pills, items))
        strip.append('<a href="#row-%s-%s" style="flex:1"><b>%d<small>点</small></b><span><i>(%s)</i>%s</span></a>' % (pid, part, n, part, label))
    tot = Q['pts']
    h = ('<h4 class="apr-t">Q%s %s　<small>%s・例題・合計%d点</small></h4>' % (pid[1], '長い記述問題' if Q['kind'] == 'Long' else '短い記述問題', Q['kind'], tot) +
         '<p class="rlead"><b>%s</b>　%s。以下は、College Boardが公開している例題の採点基準です。経済の記述問題は、問題ごとに「何を書けば1点か」が決まっています</p>' % (Q['title'], Q['scene']) +
         '<div class="apk"><p class="apk-h">%d点の内訳<small>押すと、その小問の基準に移動します</small></p><div class="apk-b">%s</div></div>' % (tot, ''.join(strip)) +
         '<figure class="apr rise"><figcaption class="apr-h"><span class="apr-sc">%d<small>点</small></span><span><b>Scoring Guidelines for Question %s: %s</b><small>英語は原文のまま。1行が1点</small></span></figcaption>%s'
         '<p class="apr-src">%sのScoring Guidelines。© 2026 College Board. 英語は原文のまま。和訳とハイライトは当サイトによるもの</p></figure>'
         % (tot, pid[1], Q['kind'], ''.join(rows), SRC % S['en']))
    used = []
    for part, label, pts in Q['parts']:
        for p in pts:
            if p[2] not in used: used.append(p[2])
    order = [t for t in (G, E, N, A) if t in used]
    cards = ''.join('<article class="tp" id="tip-%s-%s" data-title="%s" data-sum="%s"><h4><span class="tp-no">%s</span>%s</h4><p class="tp-rd">%s</p></article>'
                    % (pid, t, D.COMMON_TIPS[t][0], D.COMMON_TIPS[t][0], D.TASK[t][0], D.COMMON_TIPS[t][0], D.COMMON_TIPS[t][1]) for t in order)
    tips = ('<div class="aps-tips"><p class="aps-th">Q%sのコツ<small>採点基準に基づく当サイトの解説。College Board公式の攻略法ではありません</small></p><div class="tps">%s</div></div>' % (pid[1], cards))
    return h + tips


G, E, N, A = D.G, D.E, D.N, D.A


def task_panel(S):
    rows = ''.join('<li><b>%s</b><small lang="en">（%s）</small>：記述の配点の<b>%s</b></li>' % (D.TASK[t][0], D.TASK[t][1], p) for t, p in S['frq_tasks'])
    return ('<h4 class="apr-t">記述問題の4つのタスク　<small>Section II全体の配点に占める割合</small></h4>'
            '<p class="rlead">記述の3問では、4種類のタスクで4つのスキルがすべて評価されます。配点の割合は次のとおりで、<b>グラフを描くタスクが最も大きい</b>のが経済の特徴です</p>'
            '<ul class="apb">%s</ul><p class="apr-src">%sのExam Information（Section II: Free-Response）</p>' % (rows, SRC % S['en']))


def verbs_panel(S):
    items = ''.join('<li><p class="apx-en" lang="en"><b>%s:</b> %s</p><p class="apx-ja">%s</p></li>' % (v, d, j) for v, d, j in D.VERBS)
    return ('<h4 class="apr-t">記述問題の指示語　<small>Task Verbs Used in Free-Response Questions</small></h4>'
            '<p class="rlead">問題文の動詞で、求められる答え方が決まります。とくに<b>Calculate</b>は途中の計算、<b>Draw / Show</b>はラベルが採点の条件です</p>'
            '<div class="apx-top2"><ul class="apx-l">%s</ul></div><p class="apr-src">%s。© 2026 College Board. 英語は原文のまま。和訳とハイライトは当サイトによるもの</p>' % (items, SRC % S['en']))


def scoring_html(S):
    P = [('q1', 'Q1', '長い記述問題（例題）', '10点', 'Long'), ('q2', 'Q2', '短い記述問題（例題）', '5点', 'Short'),
         ('task', 'タスク', '記述の4つのタスク', '配点', ''), ('verbs', '指示語', '問題文の動詞', '定義', '')]
    nav = ''.join('<button type="button" class="aps-b%s" data-p="%s" aria-controls="ap-%s" aria-selected="%s"><span class="aps-q">%s</span><span class="aps-n">%s<small>%s</small></span><span class="aps-pc">%s</span></button>'
                  % (' on' if k == 0 else '', p[0], p[0], 'true' if k == 0 else 'false', p[1], p[2], p[4], p[3]) for k, p in enumerate(P))
    bodies = {'q1': q_panel(S, 'q1'), 'q2': q_panel(S, 'q2'), 'task': task_panel(S), 'verbs': verbs_panel(S)}
    panels = ''.join('<section class="aps-p%s" id="ap-%s" aria-label="%s">%s</section>' % (' on' if k == 0 else '', p[0], p[2], bodies[p[0]]) for k, p in enumerate(P))
    return (step(4, 'scoring', '記述問題の採点基準と対策', '記述（スコア全体の33.35%）は、問題ごとの採点基準で1点ずつ採点') +
            '<p class="rlead">経済の記述問題には、AP日本語のような共通の採点基準はなく、<b>問題ごとに「何を書けば1点か」</b>が細かく決められています。'
            'ここでは、College BoardがCourse and Exam Descriptionで公開している例題の採点基準を、英語の原文と和訳で示します。Q3はQ2と同じ短い問題（5点）です</p>'
            '<div class="apsx rise"><div class="apsx-h"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>'
            '<b>採点基準一覧</b><span class="apsx-sw" role="group" aria-label="表示の切り替え"><button type="button" data-m="rub" aria-pressed="true">採点の内訳</button><button type="button" data-m="tips" aria-pressed="false">コツ</button></span></div>'
            '<div class="aps"><nav class="aps-nav" aria-label="採点基準の問題"><p class="aps-h">記述問題<b>33.35%%</b><small>選択式（66.65%%）は採点基準なし</small></p>%s</nav><div class="aps-ps">%s</div></div></div>' % (nav, panels))


def tocsum(S):
    u = S['units']; big = max(u, key=lambda x: x[4])
    return {
     'units': [('6つの単元', '、'.join(x[1] for x in u)), ('4つの大きな考え方', '、'.join(b.split('（')[0] for b in S['bigideas']))],
     'exam': [('選択式66.65%', '60問・70分'), ('記述33.35%', '3問・60分（長い問題10点、短い問題5点×2）'), ('ハイブリッド形式', '選択はBluebook、記述は紙に手書き。四則演算の電卓が使える')],
     'overview': [('選択式は単元ごとの比率', '最も比率が大きいのは単元%s「%s」（%d〜%d%%）' % (big[0], big[1], big[3], big[4])), ('記述は単元をまたぐ', '1問の中で複数の単元を組み合わせて出題')],
     'scoring': [('問題ごとの採点基準', '「何を書けば1点か」が小問ごとに決まっている'), ('グラフの配点が最大', '記述の配点の30〜50%がグラフ。ラベルがないと点にならない'), ('結論と理由をセットで', '「State … and explain …」の点は、結論と理由の両方が必要')],
    }


def kp(S):
    u = S['units']; big = max(u, key=lambda x: x[4])
    return [('試験は2時間10分', '選択式60問（66.65%%）と記述3問（33.35%%）。%s、選択はBluebook、記述は紙に手書き' % S['date']),
            ('6つの単元', '選択式は単元ごとに出題比率が決まっていて、最大は単元%s「%s」（%d〜%d%%）' % (big[0], big[1], big[3], big[4])),
            ('記述は単元をまたぐ', '長い問題（10点）1問と短い問題（5点）2問。1問の中で複数の単元を組み合わせて出題'),
            ('グラフが得点の柱', '記述の配点の30〜50%がグラフ。軸・曲線・記号のラベルが採点の条件'),
            ('結論と理由をセットで', '採点基準は小問ごとに1点ずつ。「増える・減る」の結論に、なぜそうなるかの説明を添える')]


EXTRA_CSS = '''<style id="econ-css">.eqt{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;margin:6px 0 2px!important}
.eqt span{font-size:11px;font-weight:700;color:#fff;background:var(--c,#16294d);padding:1px 8px}
.eqt small{font-size:11px;color:var(--muted,#5c6984)}.eqt b{margin-left:auto;font-size:12px;color:var(--navy,#0b1f4b)}
.apx-top2 .apx-l>li{padding-bottom:10px;margin-bottom:6px;border-bottom:1px dashed #d9e2ef}.apx-top2 .apx-l>li:last-child{border-bottom:0;margin-bottom:0}
.aut .aut-pj{font-family:var(--latin);letter-spacing:0}
.apk-b span i{display:block;font-style:normal;font-size:10.5px;opacity:.7}</style>
'''


def build(S):
    F = os.path.join(ROOT, 'subjects/ap', S['slug'], 'index.html')
    s = open(F, encoding='utf-8').read()
    ids = ('units', 'exam', 'overview', 'scoring', 'content')
    i = min(s.index('<div class="step" id="%s">' % k) for k in ids if '<div class="step" id="%s">' % k in s)
    w = s.rfind('<div class="ajs', 0, i)
    if w >= 0 and s.find('</div>', w, i) < 0:
        i = w
    j = s.index('<div class="step" id="camino">')
    parts = [units_html(S), exam_html(S), overview_html(S), scoring_html(S)]
    body = '\n'.join('<div class="ajs%s">%s</div>' % (' ajs-alt' if k % 2 else '', p) for k, p in enumerate(parts)) + '\n'
    s = s[:i] + body + s[j:]
    s = re.sub(r'(<div class="step" id="camino"><span class="step-n">)\d+', r'\g<1>5', s)
    toc = ('<li><a href="#units"><span>1</span>6つの単元</a></li><li><a href="#exam"><span>2</span>試験の形式</a></li>'
           '<li><a href="#overview"><span>3</span>単元と試験の関係</a></li><li><a href="#scoring"><span>4</span>記述問題の採点基準と対策</a></li>'
           '<li><a href="#camino"><span>5</span>家庭教師によるサポート</a></li>')
    s = re.sub(r'(<nav[^>]*class="otl"[^>]*><p>目次</p>(?:<p class="otl-note">.*?</p>)?<ol>).*?(</ol>)', lambda m: m.group(1) + toc + m.group(2), s, flags=re.S)
    # styles / scripts
    for sid in ('apjp-css', 'apc-units', 'econ-css', 'kp-css', 'apjp-toc'):
        s = re.sub(r'<style id="%s">.*?</style>\n' % sid, '', s, flags=re.S)
    apu2 = re.search(r"CSS = '''(<style id=\"apc-units\">.*?</style>\n)'''", open(os.path.join(HERE, '..', 'apsci', 'ap_content.py'), encoding='utf-8').read(), re.S).group(1)
    s = s.replace('</head>', BA.css() + apu2 + EXTRA_CSS + '</head>', 1)
    s = re.sub(r'<script id="apjp-js">.*?</script>\n', '', s, flags=re.S)
    s = s.replace('</body>', '<script id="apjp-js">' + open(os.path.join(HERE, '..', 'apjp', 'kt.js'), encoding='utf-8').read() + BA.APS_JS + BA.TOC_JS + '</script>\n</body>', 1)
    # hero: facts -> key points
    s = re.sub(r'<dl class="sj-facts">.*?</dl>', '', s, flags=re.S)
    s = re.sub(r'<!--kp-->.*?<!--/kp-->', '', s, flags=re.S)
    t = re.sub(r'<section class="aps-p" .*?</section>', '', s, flags=re.S)
    t = re.sub(r'<p class="apx-en".*?</p>', '', t, flags=re.S)
    mins = KPM.reading_minutes(t)
    m = re.search(r'<p class="lead">.*?</p>', s, flags=re.S)
    s = s[:m.end()] + ('<!--kp--><p class="rtime">%s読了目安：約%d分</p><div class="kp"><ul>%s</ul></div><!--/kp-->'
                       % (KPM.CLOCK, mins, ''.join('<li><b>%s：</b>%s</li>' % x for x in kp(S)))) + s[m.end():]
    s = s.replace('</head>', KPM.CSS.replace('<style id="kp-css">', '<style id="kp-css">.kp{max-width:none!important}') + '</head>', 1)
    lead_old = re.search(r'<p class="lead">.*?</p>', s, flags=re.S).group(0)
    lead_new = ('<p class="lead">College Boardが実施するAP %s（%s）を、2026年秋改訂のCourse and Exam Descriptionに沿って解説します。6つの単元、2027年5月の試験の形式、'
                '単元と試験の関係、記述問題の採点基準を、公式資料の英語と和訳で確認できます。Caminoでは、インター生・帰国子女を対象に、<b>AP %sの家庭教師</b>を行っています</p>' % (S['ja'], S['en'], S['ja']))
    s = s.replace(lead_old, lead_new, 1)
    desc = ('AP %s（%s）の6つの単元と出題比率、2027年5月の試験形式、記述問題の採点基準を、College Boardの2026年秋改訂の公式資料に沿って解説。'
            'インター生・帰国子女向けのAP家庭教師は対面／オンラインに対応。初回60分無料' % (S['ja'], S['en']))
    s = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*', lambda m: m.group(1) + desc, s)
    BA.TOCSUM = tocsum(S)
    s = BA.toc_with_summaries(s)
    open(F, 'w', encoding='utf-8').write(s)
    print('ok', S['slug'], mins)


if __name__ == '__main__':
    build(D.MICRO)
    build(D.MACRO)
