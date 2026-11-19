# -*- coding: utf-8 -*-
"""AP Calculus AB / BC / Precalculus pages in the AP Japanese layout. Usage: python3 build_math.py <site root>"""
import os, re, sys
ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'econ'))
import build_econ as BE
import math_data as M
BA, KPM = BE.BA, BE.KPM
step = BA.step
CIRC = '①②③④⑤⑥'
DB_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>')


def topic_li(t, bc_page):
    if t.startswith('BC:'):
        t = t[3:]
        return '<li lang="en">%s <em class="mt-bc">%s</em></li>' % (t, 'BCのみ' if bc_page else 'BCのみ・ABの試験範囲外')
    return '<li lang="en">%s</li>' % t


def units_html(S):
    tiles, bub = [], []
    for n, ja, en, w, topics in S['units']:
        lab = '%d〜%d%%' % w if w else '試験範囲外'
        on = n == 1
        tiles.append('<button type="button" class="aut%s" data-u="%d" aria-expanded="%s" aria-controls="aub-%d"><span class="aut-n">%d</span><b>%s</b><small lang="en">%s</small><i class="aut-pj">%s</i></button>'
                     % (' on' if on else '', n, 'true' if on else 'false', n, n, ja, en, lab))
        bub.append('<div class="aub%s" id="aub-%d" data-u="%d"><p class="aub-h">単元%d　%sのトピック<small>（%d）</small></p><ol class="aub-q mt-q">%s</ol><p class="aub-t"><span>選択式での出題比率</span>%s</p></div>'
                   % (' on' if on else '', n, n, n, ja, len(topics), ''.join(topic_li(t, S['bc']) for t in topics), lab))
    return (step(1, 'units', '%d つの単元'.replace(' ', '') % len(S['units']), '単元を押すと、その単元のトピック（公式の英語名）が表示されます') +
            '<p class="rlead">%s</p>' % S['units_lead'] +
            '<div class="au rise"><div class="au-g">%s</div><div class="au-bs">%s</div></div>' % (''.join(tiles), ''.join(bub)) +
            '<p class="apu-src">%s。トピック名は公式資料の英語のまま</p>' % S['src'])


def exam_html(S):
    body = ''.join('<tr class="apex-%s"><th scope="row"><span class="apex-tag" lang="en">%s</span><b>%s</b><small lang="en">%s</small>%s</th>'
                   '<td data-l="問題数">%s</td><td data-l="比重">%s</td><td data-l="時間">%s</td></tr>'
                   % (k, t, ja, en, '<small class="apex-d">%s</small>' % d if d else '', n, w, tm) for k, t, ja, en, n, w, tm, d in S['exam'])
    tbl = ('<div class="apex-w rise"><table class="apex"><thead><tr><th>問題の種類</th><th>問題数</th><th>比重</th><th>時間</th></tr></thead><tbody>%s</tbody></table>'
           '<p class="apr-src">%sの試験形式表をもとに作成</p></div>' % (body, S['src']))
    return step(2, 'exam', '試験の形式（2027年5月）', S['exam_sub']) + tbl + '<ul class="apb rise">%s</ul>' % ''.join('<li>%s</li>' % x for x in S['exam_notes'])


def overview_html(S):
    ws = [u[3] for u in S['units'] if u[3]]
    top = max(w[1] for w in ws)
    rows = ''
    for n, ja, en, w, tp in S['units']:
        if w:
            r = '<span class="apu2-p">%d〜%d%%</span><span class="apu2-bar" aria-hidden="true"><i style="left:%.1f%%;width:%.1f%%"></i></span>' % (w[0], w[1], w[0] / top * 100, (w[1] - w[0]) / top * 100)
        else:
            r = '<span class="apu2-p">試験範囲外</span><span></span>'
        rows += ('<div class="apu2-r%s"><div class="apu2-u"><span class="apu2-n">%d</span><div><b>%s</b><small lang="en">Unit %d: %s</small></div></div><div class="apu2-w">%s</div></div>'
                 % ('' if w else ' apu2-x', n, ja, n, en, r))
    return (step(3, 'overview', '単元と試験の関係', S['ov_sub']) + '<p class="rlead">%s</p>' % S['ov_lead'] +
            '<div class="apu2 rise" role="table" aria-label="単元と選択式での出題比率"><div class="apu2-h"><span>単元</span><span>選択式セクションでの出題比率</span></div>%s</div>' % rows +
            '<p class="apr-src">%s</p>' % S['src'] + S['ov_extra'])


def verbs_panel(S):
    items = ''.join('<li><p class="apx-en" lang="en"><b>%s:</b> %s</p><p class="apx-ja">%s</p></li>' % v for v in S['verbs'])
    return ('<h4 class="apr-t">記述問題の指示語　<small lang="en">Task Verbs Used in Free-Response Questions</small></h4>'
            '<p class="rlead">問題文の動詞で、求められる答え方が決まります。数学の記述では、<b>式・途中の計算・理由づけ</b>を書くことが採点の前提です</p>'
            '<div class="apx-top2"><ul class="apx-l">%s</ul></div><p class="apr-src">%s。英語は原文のまま。和訳とハイライトは当サイトによるもの</p>' % (items, S['src']))


def tips_panel(S):
    cards = ''.join('<article class="tp" id="tip-m-%d" data-title="%s" data-sum="%s"><h4><span class="tp-no">コツ%s</span>%s</h4><p class="tp-rd">%s</p></article>'
                    % (i, t, t, CIRC[i - 1], t, b) for i, (t, b) in enumerate(S['tips'], 1))
    return ('<h4 class="apr-t">記述問題のコツ</h4><p class="aps-th"><small>公式資料の指示と指示語から読み取った当サイトの解説。College Board公式の攻略法ではありません</small></p>'
            '<div class="tps">%s</div>' % cards)


def scoring_html(S):
    P = S['panels'] + [('verbs', '指示語', '問題文の動詞', '定義', verbs_panel(S)), ('tips', 'コツ', '記述で点を取る', '%d' % len(S['tips']), tips_panel(S))]
    nav = ''.join('<button type="button" class="aps-b%s" data-p="%s" aria-controls="ap-%s" aria-selected="%s"><span class="aps-q">%s</span><span class="aps-n">%s</span><span class="aps-pc">%s</span></button>'
                  % (' on' if k == 0 else '', p[0], p[0], 'true' if k == 0 else 'false', p[1], p[2], p[3]) for k, p in enumerate(P))
    panels = ''.join('<section class="aps-p%s" id="ap-%s" aria-label="%s">%s</section>' % (' on' if k == 0 else '', p[0], p[2], p[4]) for k, p in enumerate(P))
    return (step(4, 'scoring', '記述問題の構成と対策', S['sc_sub']) + '<p class="rlead">%s</p>' % S['sc_lead'] +
            '<div class="apsx rise"><div class="apsx-h">%s<b>記述問題データベース</b></div>'
            '<div class="aps"><nav class="aps-nav" aria-label="記述問題の項目"><p class="aps-h">記述問題<b>%s</b><small>選択式（%s）とあわせて採点</small></p>%s</nav><div class="aps-ps">%s</div></div></div>'
            % (DB_ICON, S['fr_w'], S['mc_w'], nav, panels))


def li_list(rows):
    return '<ul class="apb">%s</ul>' % ''.join('<li><b>%s</b><small lang="en">（%s）</small>：%s</li>' % r for r in rows)


def calc(bc):
    units = [(n, ja, en, (bcw if bc else abw), M.CALC_TOPICS[n]) for n, ja, en, abw, bcw in M.CALC_UNITS if bc or abw]
    name = 'BC' if bc else 'AB'
    src = '出典：College Board「AP Calculus AB and BC Course and Exam Description」、単元名と出題比率はAP Central（2026-27年度）'
    frq = ('<h4 class="apr-t">記述問題の構成　<small lang="en">Section II: Free-Response</small></h4>'
           '<p class="rlead">記述は6問で、<b>Part A（グラフ電卓が必要）2問・30分</b>と<b>Part B（電卓なし）4問・60分</b>に分かれます。ABとBCの試験には、AB範囲の内容から出る<b>共通の3問</b>があり、'
           'どちらも少なくとも2問は現実の場面を題材にした問題です。手続き的な問題と概念的な問題が、ほぼ同じ割合で出題されます</p>'
           '<div class="apx-top2"><ul class="apx-l"><li><p class="apx-en" lang="en">The AB and BC Exams include three common free-response questions that assess content from the domain of the AB Calculus course. Both AP Exams include various types of functions and function representations and a roughly equal mix of procedural and conceptual tasks. They both also include at least two questions that incorporate a real-world context or scenario into the question.</p>'
           '<p class="apx-ja">ABとBCの試験には、AB範囲の内容を評価する<b>共通の記述問題が3問</b>ある。どちらの試験も、さまざまな関数と表現を扱い、<b>手続き的な課題と概念的な課題がほぼ半々</b>。また、<b>少なくとも2問</b>は現実の場面を取り入れた問題になる</p></li></ul></div>'
           '<p class="rlead" style="margin-top:16px">記述では4つの数学的な実践（Mathematical Practices）が評価され、配点の割合は次のとおりです。<b>正当化（Justification）</b>が最大で35〜60%を占めるのが特徴です</p>' + li_list([(a, b, '記述の配点の<b>%s</b>' % c) for a, b, c in M.CALC_FR_PR]) +
           '<p class="apr-src">%sのExam Information</p>' % src.split('、')[0])
    S = dict(slug='calculus-' + name.lower(), ja='微積分' + name, en='Calculus ' + name, bc=bc, units=units, src=src,
             units_lead=('AP微積分%sは、大学の微積分%sにあたるコースです。%sの単元を、<b>3つの大きな考え方（Big Ideas）</b>、%sを軸に学びます。右上の数字は、選択式の問題に占める各単元の出題比率です'
                         % (name, '（Calculus I・II）2学期分' if bc else '（Calculus I）1学期分', '10' if bc else '8', '、'.join(M.CALC_BIG))),
             exam=M.CALC_EXAM, exam_sub='試験時間は3時間10分。選択式と記述式が半分ずつ。どちらも電卓あり・なしのパートに分かれる',
             exam_notes=['2027年5月の試験から、選択問題は42問（Part A 29問・Part B 13問）、記述は6問（Part A 2問・Part B 4問）の形式',
                         'Part Bの選択問題と記述のPart Aでは、グラフ電卓が必要。それ以外は電卓なし',
                         'BCの試験にはABの範囲もすべて含まれ、BCの受験者にはAB部分のサブスコアも出る' if bc else 'ABとBCは同じ時間割・同じ形式で、記述のうち3問は共通'],
             ov_sub='選択式は単元ごとの比率が決まっていて、記述は単元をまたいで出題',
             ov_lead=('選択式の42問は、単元ごとに出題比率の幅が決まっています。%s記述の6問は、単元を組み合わせた問題が中心です'
                      % ('BCでは、BCだけの単元9（10〜15%）と単元10（15〜20%）が大きな比重を占め、AB範囲の単元はそれぞれ5〜20%です。' if bc else '比率が大きいのは単元5「微分の解析的な応用」と単元6「積分と変化の蓄積」（どちらも15〜20%）です。')),
             ov_extra='<p class="rlead">選択式では、4つの実践のうち3つが次の比率で評価されます（伝え方と記法は記述だけで評価）</p>' + li_list([(a, b, '選択問題の<b>%s</b>' % c) for a, b, c in M.CALC_MC_PR]),
             sc_sub='記述（スコア全体の50%）は、式・途中の計算・理由づけまで書いて点になる',
             sc_lead='数学の記述問題には、AP日本語のような共通の採点基準はなく、<b>問題ごとの採点基準</b>で採点されます。そのため、ここでは記述問題の構成、評価される実践の配分、問題文の指示語と、そこから読み取れるコツを示します',
             fr_w='50%', mc_w='50%', verbs=M.CALC_VERBS, tips=M.CALC_TIPS,
             panels=[('frq', '構成', '記述問題の構成', '6問', frq)])
    S['kp'] = [('試験は3時間10分', '選択式42問（50%）と記述6問（50%）。どちらも電卓あり・なしのパートに分かれる'),
               ('%sつの単元' % ('10' if bc else '8'), ('BCだけの単元9・10が大きな比重を占める（10〜20%）' if bc else '比率が大きいのは単元5・6（各15〜20%）')),
               ('記述は単元をまたぐ', 'ABとBCで共通の3問があり、少なくとも2問は現実の場面を題材にした問題'),
               ('正当化が記述の柱', '記述の配点の35〜60%が「正当化」。定理の名前と条件まで書く'),
               ('式と途中の計算を必ず書く', '電卓で出した数字だけでは点にならない。小数は小数点以下3桁まで正確に')]
    S['tocsum'] = {'units': [('%sつの単元' % ('10' if bc else '8'), '極限から%s' % ('級数まで' if bc else '積分の応用まで'))],
                   'exam': [('選択式50%', '42問・1時間40分（電卓なし29問・電卓あり13問）'), ('記述50%', '6問・1時間30分（電卓あり2問・電卓なし4問）')],
                   'overview': [('選択式は単元ごとの比率', S['kp'][1][1]), ('記述は単元をまたぐ', 'ABとBCで共通の3問')],
                   'scoring': [('正当化が最大', '記述の配点の35〜60%'), ('式と途中の計算', '電卓の数字だけでは点にならない')]}
    S['title_n'] = '%sつの単元' % ('10' if bc else '8')
    return S


def precalc():
    units = [(n, ja, en, w, M.PC_TOPICS[n]) for n, ja, en, w in M.PC_UNITS]
    src = '出典：College Board「AP Precalculus Course and Exam Description」、単元名と出題比率はAP Central（2026-27年度）'
    sk = ['1.A', '1.B', '1.C', '2.A', '2.B', '3.A', '3.B', '3.C']
    trs = ''.join('<tr class="apex-q"><th scope="row"><span class="apex-tag" lang="en">%s</span><b>%s</b><small lang="en">%s</small></th><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                  % (q, ja, en, u, c, ctx, '・'.join('%s×%d' % (sk[i], v) for i, v in enumerate(M.PC_SKILLPTS[q]) if v)) for q, ja, en, u, c, ctx, de, dj in M.PC_FRQ)
    tbl = ('<div class="apex-w"><table class="apex"><thead><tr><th>問題</th><th>単元</th><th>電卓</th><th>現実の場面</th><th>スキルごとの点数</th></tr></thead><tbody>%s</tbody></table></div>' % trs)
    desc = '<div class="apx-top2"><ul class="apx-l">%s</ul></div>' % ''.join('<li><p class="apx-en" lang="en">%s</p><p class="apx-ja">%s</p></li>' % (de, dj) for q, ja, en, u, c, ctx, de, dj in M.PC_FRQ)
    frq = ('<h4 class="apr-t">4つの記述問題　<small lang="en">Free-Response Task Models</small></h4>'
           '<p class="rlead">プレカルキュラスの記述4問は、<b>毎年、問題の型が決まっています</b>。各6点で、比重も同じです。下の表の「スキルごとの点数」は、6点がどのスキルに配分されているかを示します</p>' + tbl +
           '<p class="apr-src">%sのFree-Response Task Model OverviewとPoint Count by Skill</p>' % src.split('、')[0] + desc +
           '<p class="apr-src">英語は原文のまま。和訳とハイライトは当サイトによるもの</p>')
    instr = ('<h4 class="apr-t">記述問題の注意事項　<small lang="en">General Instructions</small></h4>'
             '<p class="rlead">試験当日に受験者に示される注意事項です。<b>途中の考え方をすべて書くこと</b>が、採点の前提になっています</p>'
             '<div class="apx-top2"><ul class="apx-l">%s</ul></div><p class="apr-src">%s。英語は原文のまま。和訳とハイライトは当サイトによるもの</p>'
             % (''.join('<li><p class="apx-en" lang="en">%s</p><p class="apx-ja">%s</p></li>' % x for x in M.PC_INSTR), src.split('、')[0]))
    S = dict(slug='precalculus', ja='プレカルキュラス', en='Precalculus', bc=False, units=units, src=src,
             units_lead='APプレカルキュラスは、大学の微積分の前に学ぶ関数のコースです。試験で問われるのは単元1〜3で、単元4は学校によって扱う追加の内容です。右上の数字は、選択式の問題に占める各単元の出題比率です',
             exam=M.PC_EXAM, exam_sub='試験時間は2時間55分。選択式42問と、各6点の記述4問',
             exam_notes=['2027年5月の試験から、選択問題は42問（Part A 29問・Part B 13問）の形式',
                         'グラフ電卓は弧度法（radian）に設定しておく', '試験範囲は単元1〜3。単元4は試験に出ない'],
             ov_sub='選択式は単元と関数の種類ごとに比率が決まり、記述は問題の型が決まっている',
             ov_lead='選択式の42問は、単元ごとの比率に加えて、<b>関数の種類ごと</b>の比率も決まっています。最も比率が大きいのは三角関数と極座標の関数（30〜35%）です',
             ov_extra=('<p class="rlead">選択式での関数の種類ごとの比率（目安）</p><ul class="apb">%s</ul>' % ''.join('<li><b>%s</b><small lang="en">（%s）</small>：単元%s・<b>%s</b></li>' % r for r in M.PC_FTYPES) +
                       '<p class="rlead">試験全体での3つの実践の比率</p>' + li_list([(a, b, '<b>%s</b>' % c) for a, b, c in M.PC_PRACT])),
             sc_sub='記述（スコア全体の37.5%）は、毎年決まった4つの型で出題',
             sc_lead='数学の記述問題は問題ごとの採点基準で採点されますが、プレカルキュラスは<b>4問の型が毎年決まっている</b>ため、何が問われるかを事前に知ることができます。ここでは4つの型、注意事項、指示語と、そこから読み取れるコツを示します',
             fr_w='37.5%', mc_w='62.5%', verbs=M.PC_VERBS, tips=M.PC_TIPS,
             panels=[('frq', '型', '4つの記述問題', '4問', frq), ('instr', '注意', '記述の注意事項', '3', instr)])
    S['kp'] = [('試験は2時間55分', '選択式42問（62.5%）と記述4問（37.5%）。電卓あり・なしのパートに分かれる'),
               ('試験範囲は単元1〜3', '単元4（媒介変数・ベクトル・行列）は試験に出ない'),
               ('関数の種類ごとに比率が決まる', '最も大きいのは三角関数と極座標の関数（30〜35%）'),
               ('記述は毎年同じ4つの型', '関数の概念、非周期的なモデル化、周期的なモデル化、式の変形。各6点'),
               ('途中の考え方をすべて書く', '答えだけでは点にならないことがある。単位と小数点以下3桁にも注意')]
    S['tocsum'] = {'units': [('4つの単元', '試験範囲は単元1〜3。単元4は学校によって扱う')],
                   'exam': [('選択式62.5%', '42問・1時間45分'), ('記述37.5%', '4問・70分。各6点')],
                   'overview': [('関数の種類ごとの比率', '三角関数と極座標の関数が30〜35%で最大')],
                   'scoring': [('4つの決まった型', 'Q1 関数の概念、Q2 非周期的なモデル化、Q3 周期的なモデル化、Q4 式の変形'), ('途中の考え方を書く', '正しさと完全さで採点')]}
    S['title_n'] = '4つの単元'
    return S


EXTRA = '''<style id="math-css">.mt-q{columns:2;column-gap:28px;padding-left:1.8em!important;font-size:13.5px!important;font-weight:500!important}.mt-q li{break-inside:avoid;margin:0 0 4px!important}
.mt-bc{font-style:normal;font-size:10.5px;font-weight:700;color:#fff;background:var(--c,#16294d);padding:0 6px;margin-left:4px;white-space:nowrap}
.aub-h small{font-weight:500;margin-left:4px}.apu2-x .apu2-p{font-size:12px;color:var(--muted,#5c6984)}
.aps>*{min-width:0}
@media(max-width:700px){.mt-q{columns:1}.aps-p .apex-w{overflow-x:auto;-webkit-overflow-scrolling:touch}.aps-p .apex{min-width:520px;font-size:12px}}</style>
'''


def build(S):
    F = os.path.join(ROOT, 'subjects/ap', S['slug'], 'index.html')
    s = open(F, encoding='utf-8').read()
    mj = re.search(r'<!--mjreq-->.*?<!--/mjreq-->\n?', s, re.S)
    mjb = mj.group(0) if mj else ''
    if mj:
        s = s[:mj.start()] + s[mj.end():]
    ids = ('units', 'exam', 'overview', 'scoring', 'content')
    i = min(s.index('<div class="step" id="%s">' % k) for k in ids if '<div class="step" id="%s">' % k in s)
    w = s.rfind('<div class="ajs', 0, i)
    if w >= 0 and s.find('</div>', w, i) < 0:
        i = w
    j = s.index('<div class="step" id="camino">')
    parts = [units_html(S), exam_html(S), overview_html(S), scoring_html(S)]
    body = '\n'.join('<div class="ajs%s">%s</div>' % (' ajs-alt' if k % 2 else '', p) for k, p in enumerate(parts)) + '\n'
    if mjb:
        mjb = re.sub(r'(<div class="step" id="majors"><span class="step-n">)\d+', r'\g<1>5', mjb)
    s = s[:i] + body + mjb + s[j:]
    s = re.sub(r'(<div class="step" id="camino"><span class="step-n">)\d+', r'\g<1>%d' % (6 if mjb else 5), s)
    toc = ('<li><a href="#units"><span>1</span>%s</a></li><li><a href="#exam"><span>2</span>試験の形式</a></li>'
           '<li><a href="#overview"><span>3</span>単元と試験の関係</a></li><li><a href="#scoring"><span>4</span>記述問題の構成と対策</a></li>' % S['title_n'])
    if mjb:
        toc += '<li><a href="#majors"><span>5</span>大学の学部で求められる度合い</a></li><li><a href="#camino"><span>6</span>家庭教師によるサポート</a></li>'
    else:
        toc += '<li><a href="#camino"><span>5</span>家庭教師によるサポート</a></li>'
    s = re.sub(r'(<nav[^>]*class="otl"[^>]*><p>目次</p>(?:<p class="otl-note">.*?</p>)?<ol>).*?(</ol>)', lambda m: m.group(1) + toc + m.group(2), s, flags=re.S)
    for sid in ('apjp-css', 'apc-units', 'econ-css', 'kp-css', 'apjp-toc', 'math-css'):
        s = re.sub(r'<style id="%s">.*?</style>\n' % sid, '', s, flags=re.S)
    apu2 = re.search(r"CSS = '''(<style id=\"apc-units\">.*?</style>\n)'''", open(os.path.join(HERE, '..', 'apsci', 'ap_content.py'), encoding='utf-8').read(), re.S).group(1)
    s = s.replace('</head>', BA.css() + apu2 + BE.EXTRA_CSS + EXTRA + '</head>', 1)
    s = re.sub(r'<script id="apjp-js">.*?</script>\n', '', s, flags=re.S)
    s = s.replace('</body>', '<script id="apjp-js">' + open(os.path.join(HERE, '..', 'apjp', 'kt.js'), encoding='utf-8').read() + BA.APS_JS + BA.TOC_JS + '</script>\n</body>', 1)
    s = re.sub(r'<dl class="sj-facts">.*?</dl>', '', s, flags=re.S)
    s = re.sub(r'<!--kp-->.*?<!--/kp-->', '', s, flags=re.S)
    t = re.sub(r'<section class="aps-p" .*?</section>', '', s, flags=re.S)
    t = re.sub(r'<p class="apx-en".*?</p>|<ol class="aub-q mt-q">.*?</ol>', '', t, flags=re.S)
    mins = KPM.reading_minutes(t)
    lead = ('<p class="lead">College Boardが実施するAP %s（%s）を、公式のCourse and Exam Descriptionに沿って解説します。単元とトピック、2027年5月の試験の形式、'
            '単元と試験の関係、記述問題の構成を、公式資料の英語と和訳で確認できます。Caminoでは、インター生・帰国子女を対象に、<b>AP %sの家庭教師</b>を行っています</p>' % (S['ja'], S['en'], S['ja']))
    s = re.sub(r'<p class="lead">.*?</p>', lambda m: lead, s, count=1, flags=re.S)
    m = re.search(r'<p class="lead">.*?</p>', s, flags=re.S)
    s = s[:m.end()] + ('<!--kp--><p class="rtime">%s読了目安：約%d分</p><div class="kp"><ul>%s</ul></div><!--/kp-->'
                       % (KPM.CLOCK, mins, ''.join('<li><b>%s：</b>%s</li>' % x for x in S['kp']))) + s[m.end():]
    s = s.replace('</head>', KPM.CSS.replace('<style id="kp-css">', '<style id="kp-css">.kp{max-width:none!important}') + '</head>', 1)
    desc = ('AP %s（%s）の単元と出題比率、2027年5月の試験形式、記述問題の構成と指示語を、College Boardの公式資料に沿って解説。'
            'インター生・帰国子女向けのAP家庭教師は対面／オンラインに対応。初回60分無料' % (S['ja'], S['en']))
    s = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*', lambda mm: mm.group(1) + desc, s)
    BA.TOCSUM = S['tocsum']
    s = BA.toc_with_summaries(s)
    open(F, 'w', encoding='utf-8').write(s)
    print('ok', S['slug'], mins)


if __name__ == '__main__':
    build(calc(False))
    build(calc(True))
    build(precalc())
