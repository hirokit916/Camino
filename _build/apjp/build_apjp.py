# -*- coding: utf-8 -*-
"""AP Japanese subject page: units + essential questions, scoring-guideline breakdown, tips.
Rewrites the body between #exam and #camino of subjects/ap/japanese/index.html (idempotent).
Usage: python3 build_apjp.py /home/claude/camino-v2"""
import os, re, sys
ROOT = sys.argv[1]
F = os.path.join(ROOT, 'subjects/ap/japanese/index.html')
HERE = os.path.dirname(os.path.abspath(__file__))

def tbl(head, rows):
    h = ''.join('<th>%s</th>' % x for x in head)
    b = ''.join('<tr><th>%s</th>%s</tr>' % (r[0], ''.join('<td data-l="%s">%s</td>' % (head[i + 1], c) for i, c in enumerate(r[1:]))) for r in rows)
    return '<div class="ewrap rise"><table class="etbl stk"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (h, b)
def step(n, id_, h, sub=''):
    return '<div class="step" id="%s"><span class="step-n">%d</span><div><h3>%s</h3>%s</div></div>' % (id_, n, h, '<p class="step-sub">%s</p>' % sub if sub else '')

# ---------------- 1 exam ----------------
EXAM_ROWS = [
 ('sec', 'Section I', '記述・口述問題', 'Free-response questions', '4', '50%', '40〜45分'),
 ('part', 'Part A', 'スピーキング', 'Speaking', '2', '', '約15分'),
 ('q', 'Q1', 'プロジェクトの発表', 'Project Presentation', '', '20%', '', '事前に準備した研究を、骨子のメモを見ながら発表する（準備3分・発表3分）'),
 ('q', 'Q2', '発表への質問（4問）', 'Project Q&amp;A', '', '15%', '', '録音された質問に答える。各質問は2回流れ、1問あたり約40秒'),
 ('part', 'Part B', 'ライティング', 'Writing', '2', '', '30分'),
 ('q', 'Q3', '物語', 'Story Narration', '', '7.5%', '', '4コマの絵をもとに、物語を書く'),
 ('q', 'Q4', 'メールへの返信', 'Email Response', '', '7.5%', '', 'メールを読み、2つの依頼・質問に答える返信を書く'),
 ('sec', 'Section II', '選択式問題', 'Multiple-choice questions', '55', '50%', '65分'),
 ('part', 'Part A', 'リスニング', 'Listening', '25', '25%', '25分', '会話、報告、発表などを聞いて答える（5問×5セット）'),
 ('part', 'Part B', 'リーディング', 'Reading', '30', '25%', '40分', '記事、メール、文学作品、広告などを読んで答える（5問×6セット）'),
]
def exam_table():
    rows = []
    for r in EXAM_ROWS:
        kind, tag, ja, en, n, w, t = r[:7]
        note = '<small class="apex-d">%s</small>' % r[7] if len(r) > 7 else ''
        rows.append('<tr class="apex-%s"><th scope="row"><span class="apex-tag" lang="en">%s</span><b>%s</b><small lang="en">%s</small>%s</th>'
                    '<td data-l="問題数">%s</td><td data-l="比重">%s</td><td data-l="時間">%s</td></tr>' % (kind, tag, ja, en, note, n, w, t))
    return ('<div class="apex-w rise"><table class="apex"><thead><tr><th>問題の種類</th><th>問題数</th><th>比重</th><th>時間</th></tr></thead><tbody>%s</tbody></table>'
            '<p class="apr-src">出典：College Board「AP Japanese Language and Culture Course and Exam Description」（Effective Fall 2026）の試験形式の表をもとに作成</p></div>' % ''.join(rows))
EXAM = step(2, 'exam', '試験の形式（2027年5月）', '試験時間は約1時間50分。記述・口述のSection Iが先、選択式のSection IIが後') + exam_table() + \
 '<ul class="apb rise">' \
 '<li>試験はすべてBluebookで行い、スピーキングも録音で回答する。有線のマイク付きヘッドセットが必要で、紙の試験は廃止された</li>' \
 '<li>書く問題はキーボードで日本語を入力する。変換で正しい漢字やかなを選ぶ練習を、早めに始めておく</li>' \
 '<li>過去問は選択式の練習には今も使える。記述・口述は問題がすべて入れ替わったため、AP Classroomの新形式の練習問題で対策する</li>' \
 '<li>2025年の受験者は3,245人、平均3.55。学校で日本語を学んだ生徒（2024年の標準グループ）は平均2.66、5の割合は16.8%</li></ul>'

# ---------------- 2 units ----------------
UNITS = [
 ('1', '家族と地域社会', 'Families and Communities', '地域社会の活動、家族関係、社会的交流と人間関係、都市と田舎のコミュニティ',
  ['日本語を話す社会で、「家族」はどのように出来ていますか。', '日本語を話す社会で、家族の価値観や家庭生活の大切な事は何ですか。', '家族や地域社会は、今日の世界をどのように経験していますか。']),
 ('2', '言語と文化', 'Language and Culture', '習慣と祝祭、言語学、世界の中の日本語',
  ['言語と文化は、どのようにお互いに影響しあっていますか。', '言語と文化は、時間とともにどのように変化していきますか。', 'テクノロジーは、言語と文化にどのような影響を与えていますか。']),
 ('3', '芸術と創造性', 'Art and Creativity', '建築、芸術遺産、美と美学、ファッションとデザイン、文学、ビジュアルアーツと舞台芸術',
  ['芸術や創造性は、日常生活にどのような影響を与えていますか。', '芸術は、文化的な考え方をどのように表したり、変えたりしていますか。', '地域社会の人たちは、芸術や創造力をどのように大切にしていますか。', '芸術は、歴史を記録するためにどのように使われていますか。']),
 ('4', '科学と技術', 'Science and Technology', '革新と新技術、個人用のテクノロジーとコミュニケーション、日常生活の中の科学、科学技術の社会的影響',
  ['科学や技術の発展には、どんな理由やきっかけがありますか。', '技術は、国際コミュニケーションをどのように高めますか。', '科学や技術の進歩は、社会にどのような影響を与えていますか。']),
 ('5', '現代の生活', 'Contemporary Life', '教育とキャリア、エンターテインメントとメディア、食と健康、ポップカルチャー、スポーツとレジャー、旅行と観光',
  ['過去20年間で現代生活はどのように変化してきましたか。', '文化的な価値観や伝統は、現代生活にどのような影響を与えていますか。', '現代生活で、「何が重要か」という考え方に影響するのは何ですか。']),
 ('6', '世界とのつながり', 'Global Contexts', '国際コミュニケーション、自然界、歴史、政策と計画、交通',
  ['世界の出来事は、日本語を話す社会にどのような影響を与えていますか。', '人々は、世界の出来事をどのように理解し、どのように行動していますか。', '複雑な社会問題は、社会の文化にどのような影響を与えていますか。']),
]
def units_html():
    tiles = ''.join('<button type="button" class="aut%s" data-u="%s" aria-expanded="%s" aria-controls="aub-%s"><span class="aut-n">%s</span><b>%s</b><small lang="en">%s</small>%s</button>'
                    % (' on' if n == '1' else '', n, 'true' if n == '1' else 'false', n, n, ja, en, '<i class="aut-pj">2026-27年度のプロジェクト</i>' if n == '3' else '')
                    for n, ja, en, topics, qs in UNITS)
    bubbles = ''.join('<div class="aub%s" id="aub-%s" data-u="%s"><p class="aub-h">単元%s　%sの「問い」</p><ol class="aub-q">%s</ol><p class="aub-t"><span>扱う話題</span>%s</p></div>'
                      % (' on' if n == '1' else '', n, n, n, ja, ''.join('<li>%s</li>' % q for q in qs), topics)
                      for n, ja, en, topics, qs in UNITS)
    return (step(1, 'units', '6つの単元と「問い」', '単元を押すと、その単元の「問い」が表示されます') +
            '<p class="rlead">AP日本語は、大学の中級（3年目前後）にあたるコースです。授業はほぼすべて日本語で行い、6つの単元（テーマ）を、それぞれ<b>3〜4つの「問い」（Essential Questions）</b>を軸に学びます。'
            '問いは試験にそのまま出るわけではありませんが、発表や質問への回答で求められる「文化のものの見方」を考える出発点になります</p>'
            '<div class="au rise"><div class="au-g">%s</div><div class="au-bs">%s</div></div>' % (tiles, bubbles) +
            '<p class="apu-src">問いの日本語は、College Boardの公式資料に掲載されている日本語訳。単元名の日本語は当サイトによる</p>')

# ---------------- 3 project ----------------
PROJECT = step(4, 'project', 'コースプロジェクト', '2026-27年度のテーマは単元3「芸術と創造性」。音楽を通して、日本の文化を探ります') + '<p class="amx-back"><a href="#overview"><i class="apo-tm">テーマ</i>3の表で紺色の「テーマ」が、このプロジェクトです。試験ではQ1 発表とQ2 質問への回答で問われます</a></p>' + tbl(
 ['時期', 'すること'],
 [['2027年1月', 'College Boardから課題と資料（音声・図表・文章など6〜8点）がAP Digital Portfolioで配布される'],
  ['1〜4月', '授業15コマ程度で、調べる（5）・掘り下げる（4）・発表をつくる（3）・振り返る（3）の4段階で進める'],
  ['2027年4月30日まで', 'Personalized Project Reference（発表の骨子。字数の上限あり）をAP Digital Portfolioで提出。締切までは修正できる'],
  ['試験当日', '骨子を手元に置いて、準備3分・発表3分。続けて4つの質問に答える']]) + \
 '<ul class="apb rise"><li>調べものは日本語の資料だけで行う。辞書は使えるが、資料をまるごと機械翻訳することは認められていない</li>' \
 '<li>発表では、少なくとも1つは文化的なものの見方に関わる要因を含めて、3つの要因を詳しく説明する</li>' \
 '<li>骨子は原稿ではなく、キーワードと短い語句でつくる要点のメモ。先生は具体的な文言や例を示せず、本番で読み上げることもできない</li>' \
 '<li>プロジェクトは先生ではなく、AP採点官が試験当日の録音を採点する。発表（Q1）と質問への回答（Q2）で合計20点</li></ul>'

# ---------------- 4 rubric (official English + Japanese) ----------------
sys.path.insert(0, HERE)
import rubric_en as R

def figure(q, title, total, rows, src_name):
    return ('<figure class="apr rise"><figcaption class="apr-h"><span class="apr-sc">%d<small>点</small></span><span><b>%s</b>'
            '<small>下線のある語句は、満点の条件に関わる言葉。押すとコツが表示されます</small></span></figcaption>%s%s<p class="apr-src">%s</p></figure>'
            % (total, title, R.directions_html(q), ''.join(R.row_html(r) for r in rows), R.SRC % src_name))

COMMON = ('<p class="rlead">記述・口述の4問は、観点（Row）ごとに0〜3点または0〜2点で採点されます。各観点は、点数ごとの<b>採点基準（Scoring Criteria）</b>と、'
          'その点数になる<b>典型的な回答（Decision Rules and Scoring Notes）</b>の2段で書かれています。<b>日本語以外で答えた回答は、その観点で0点</b>。'
          'プロジェクトの発表では、<b>盗用や、機械翻訳・生成AIで作ったとわかる内容も0点</b>です</p>'
          '<p class="rlead">文化の理解の観点では、次の3つの言葉が決まった意味で使われます。採点基準の注（Additional Notes）にある定義です</p>' + R.defs_html())

Q1 = ('<h4 class="apr-t" id="r-present">Q1 プロジェクトの発表　<small>5つの観点・合計11点（スコア全体の20%）</small></h4>'
      '<p class="rlead">発表は、<b>中身（課題の遂行・文化の理解）</b>、<b>組み立て（構成）</b>、<b>言葉（語彙・文法）</b>、<b>話し方</b>の5つで採点されます。'
      '調べた内容が正確でも、文化の「ものの見方」に結びついていなければ、文化の理解で2点はとれません</p>'
      + figure('q1', 'Question 1: Project Presentation', 11, R.ROWS['q1'], 'Project Scoring Guidelines（Question 1）'))
Q2 = ('<h4 class="apr-t" id="r-qa">Q2 発表への質問　<small>4つの観点・合計9点（スコア全体の15%）</small></h4>'
      '<p class="rlead">質問は事前にわからず、録音された4問がそれぞれ2回流れ、約40秒で答えます。<b>4問のうち少なくとも3問に答えること</b>と、'
      '<b>どれか1問で比較か振り返りをすること</b>が、満点の境目です</p>'
      + figure('q2', 'Question 2: Project Q&amp;A', 9, R.ROWS['q2'], 'Project Scoring Guidelines（Question 2）'))
Q34 = ('<h4 class="apr-t" id="r-write">Q3 物語・Q4 メールへの返信　<small>各3つの観点・各8点（スコア全体の7.5%ずつ）</small></h4>'
       '<p class="rlead">書く2問は、<b>内容・構成・語彙と文法</b>の3つの観点で採点されます。構成の点は、語彙や文法が限られていても、話が通じて組み立てられていれば取れます</p>'
       + figure('q3', 'Question 3: Story Narration', 8, R.ROWS['q3'], 'Scoring Guidelines（Question 3）')
       + figure('q4', 'Question 4: Email Response', 8, R.ROWS['q4'], 'Scoring Guidelines（Question 4）'))

TIPS = [
 ('要因は「事実＋具体例」で一つずつ', 'Q1 課題の遂行', '3つ以上の要因を、具体的な情報や例で詳しく説明',
  '要因を3つ並べるだけでは1点にとどまります。要因ごとに「何が起きているか（事実）」と「たとえば（資料からの具体例）」を一組にして話します。資料にある数字や固有名詞を一つ入れるだけで、「よく調べた情報」にもとづく説明になります'),
 ('「何が」だけでなく「なぜそうなのか」まで言う', 'Q1・Q2 文化の理解', '産物・慣習が、どんな価値観・信念・態度を映しているかを説明',
  '「日本ではカラオケが人気です」は産物・慣習の描写で1点です。「仲間と同じ時間を楽しむことを大切にする考え方があるから」のように、<b>その背景にある価値観</b>まで言って2点になります。発表では、3つの要因のうち少なくとも1つを、ものの見方の要因にします'),
 ('最初に全体像、最後にまとめを言う', 'Q1 構成・Q3 構成', '論理的な流れで、つなぎの表現を効果的に使う',
  '発表の冒頭で「今日は〜について、3つの点から話します」と全体像を示し、「まず」「次に」「一方で」「このように」でつなぎます。物語も同じで、「ある日」「ところが」「その結果」「最後に」といった言葉が、始まり・展開・結末をはっきりさせます'),
 ('骨子はキーワードだけ。読み上げない', 'Q1 話し方', 'なめらかで自信のある話し方。読み上げや暗唱に聞こえると0点',
  'Personalized Project Referenceは原稿ではなく、キーワードと短い語句の要点メモです。全文を書いて読み上げると、話し方の観点で0点になり得ます。キーワードだけを見て、毎回少しずつ違う言い方で話す練習をしておきます'),
 ('答えを最初の一文で言い、残りの時間で広げる', 'Q2 質問への対応・流暢さ', '少なくとも3問で、求められた情報に答える',
  '約40秒は短く、前置きをしていると答える前に時間が終わります。最初の一文で質問に答え、残りで理由や例を足します。4問のうち3問に答えれば満点の条件を満たすので、1問で詰まっても次で取り返せます'),
 ('4問のうち1問は、比較か振り返りで答える', 'Q2 文化の理解', '少なくとも1問で、比較または振り返りを詳細と例で',
  '質問への回答のどれか1つで、「日本では〜ですが、私の住んでいる地域では〜です」という<b>比較</b>か、「これは〜を大切にする考え方の表れだと思います」という<b>振り返り</b>を入れます。描写だけでは1点にとどまります'),
 ('4コマすべてを使い、会話を入れる', 'Q3 物語の展開', '4コマすべてを組み込んだ完結した物語。詳細や会話がある',
  '1コマでも抜けると満点にはなりません。各コマに1〜2文を割り当て、登場人物の「」付きのせりふを1つ入れると、詳細と会話の条件を同時に満たせます。絵がなくても話がわかるか、書き終えてから確かめます'),
 ('2つの依頼に、段落を分けて答える', 'Q4 内容・構成', '2つの依頼の両方に直接答え、あいさつと結びがある',
  'メールを読んだら、まず依頼・質問を2つ探して印をつけます。返信は「あいさつ→1つ目への答えと理由→2つ目への答えと例→結び」の順で書きます。相手が友人なら普通体、地域の人や先生ならです・ます体を最後までそろえます'),
 ('完ぺきな文法より、「伝わらない誤り」をなくす', '語彙・文法（全問）', '理解を妨げる誤りがない',
  '基準が問題にするのは「理解を妨げる誤り」です。小さな助詞の誤りより、主語と述語が合わない文や、意味の通らない語の選び方を先に直します。そのうえで、単文だけでなく、「〜ので」「〜けれど」などで文と文をつないだ文を混ぜます。3点の典型的な回答は「単文と重文を多様に使っている」です'),
 ('わからない語は、英語ではなく言い換えで', '語彙・文法（話す問題）', '言い換えや遠回しの説明で、やりとりを続けられる',
  '語彙が足りないときに英語に頼ると、1点の特徴に当たります。「作曲家」が出てこなければ「曲を作る人」のように、知っている日本語で言い換えます。言い直して伝わりやすくできることも、3点の条件に入っています'),
]
QEN = {
 1: '“Addresses the prompt, providing an explanation of three or more factors with relevant details.”',
 2: '“…a relationship between cultural perspectives AND cultural products and/or practices”',
 3: '“Demonstrates an organizational structure with a logical progression of ideas and information… Effectively uses a variety of cohesive devices.”',
 4: '“Use monotone speech throughout the presentation and sound as if being read or recited from memory.”',
 5: '“Respond appropriately, providing the requested information for at least three of the prompts within the exchange.”',
 6: '“In at least one question response… Provides a cultural comparison. OR Reflects on the relationship between cultural perspectives AND cultural products and/or practices.”',
 7: '“Integrates all four pictures into the narrative. Provides relevant details and/or dialogue.”',
 8: '“Clearly and directly respond to both requests in the email…” “Include a greeting and closing.”',
 9: '“Does not contain errors that impede comprehensibility.”',
 10: '“Use effective communicative strategies, such as circumlocution and paraphrasing.”',
}
QJA = {4: '0点の典型的な回答：発表全体が単調で、読み上げや暗唱のように聞こえる'}
def tips_html():
    summ = ''.join('<li><a href="#tip-%d"><span class="tp-no">TIP %d</span><span class="tsum-t"><b>%s</b></span><span class="tsum-g">%s</span></a></li>' % (i, i, t, g.split(' ')[0])
                   for i, (t, g, q, body) in enumerate(TIPS, 1))
    cards = ''.join('<article class="tp" id="tip-%d" data-title="%s" data-sum="%s"><h4><span class="tp-no">TIP %d</span>%s</h4><div class="tp-ev"><span class="tp-tag">%s</span><div><p class="tp-q" lang="en">%s</p><p class="tp-gl">%s</p></div></div><p class="tp-rd"><span>ポイント</span>%s</p></article>'
                    % (i, t, q, i, t, g, QEN[i], QJA.get(i, q), body) for i, (t, g, q, body) in enumerate(TIPS, 1))
    return (step(7, 'tips', '採点基準から読み取れる10のコツ', 'コツはCollege Boardが示す攻略法ではなく、基準の言葉から読み取ったもの') +
            '<div class="tsum rise"><p class="tsum-h">10のコツの一覧<small>押すと、それぞれの解説に移動します</small></p><ol class="tsum-l">%s</ol></div><div class="tps">%s</div>' % (summ, cards))

def css():
    rb = open(os.path.join(HERE, 'rb.css'), encoding='utf-8').read()
    own = '''
.apr-t{font-size:18px;color:var(--navy,#0b1f4b);margin:34px 0 8px;scroll-margin-top:100px}.apr-t small{font-size:12px;color:var(--muted,#5c6984);font-weight:500}
.rlead{font-size:15px;line-height:1.95;margin:6px 0 18px;color:var(--ink,#1d2b45)}
.apu-g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:6px 0 8px}
.apu{background:#fff;border:1px solid var(--line,#d9deea);border-radius:16px;padding:18px 20px}
.apu header{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.apu-n{flex:none;width:38px;height:38px;border-radius:50%;background:var(--c,#16294d);color:#fff;display:grid;place-items:center;font-weight:700;font-size:17px}
.apu header b{display:block;font-size:17px;color:var(--navy,#0b1f4b)}.apu header small{display:block;font-size:11.5px;color:var(--muted,#5c6984)}
.apu-t{font-size:12.5px;line-height:1.75;color:var(--muted,#5c6984);margin:0 0 12px}
.apu-h{font-size:11.5px;font-weight:700;letter-spacing:.06em;color:var(--c,#16294d);margin:0 0 6px}
.apu-q{margin:0;padding:0;list-style:none;counter-reset:q}
.apu-q li{counter-increment:q;position:relative;padding:8px 0 8px 30px;border-top:1px dashed var(--line,#e3e7f0);font-size:14.5px;line-height:1.75;color:var(--navy,#0b1f4b);font-weight:600}
.apu-q li:first-child{border-top:0}
.apu-q li::before{content:"Q" counter(q);position:absolute;left:0;top:10px;font-size:11px;font-weight:800;color:var(--c,#16294d)}
.apu-src,.apr-src{font-size:11.5px;color:var(--muted,#5c6984);margin:8px 0 26px;line-height:1.7}
.apdef{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:0 0 26px}
.apdef div{background:#fff;border:1px solid var(--line,#d9deea);border-radius:12px;padding:12px 14px}
.apdef dt{font-size:13px;font-weight:700;color:var(--navy,#0b1f4b)}.apdef dd{margin:4px 0 0;font-size:13px;line-height:1.7;color:var(--muted,#5c6984)}
.apr{margin:4px 0 30px;background:#fff;border:1px solid var(--line,#d9deea);border-radius:16px;overflow:hidden}
.apr-h{display:flex;align-items:center;gap:14px;padding:16px 20px;background:var(--ct,#e9edf5);border-bottom:1px solid var(--line,#d9deea)}
.apr-sc{flex:none;width:54px;height:54px;border-radius:50%;background:var(--c,#16294d);color:#fff;display:grid;place-items:center;font-size:21px;font-weight:700;line-height:1}
.apr-sc small{font-size:10px;font-weight:600;margin-top:-10px}
.apr-h b{display:block;font-size:16px;color:var(--navy,#0b1f4b)}.apr-h small{display:block;font-size:11.5px;color:var(--muted,#5c6984)}
.apr .apr-src{margin:0;padding:10px 20px 14px}
.apc{padding:16px 20px;border-bottom:1px solid #edf0f5}
.apc-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin-bottom:10px}
.apc-p{font-size:22px;font-weight:700;color:var(--c,#16294d);line-height:1}.apc-p small{font-size:11px;margin-left:1px}
.apc-h>b{font-size:15.5px;color:var(--navy,#0b1f4b)}.apc-h>small{font-size:11.5px;color:var(--muted,#5c6984)}
.apc-ts{margin-left:auto;display:flex;gap:6px}
.apc-tip{font-size:10.5px;font-weight:800;color:#fff;background:var(--c,#16294d);border-radius:999px;padding:2px 9px;text-decoration:none}
.apc-d{margin:0;display:grid;gap:6px}
.apc-d>div{display:grid;grid-template-columns:112px 1fr;gap:10px;font-size:13.5px;line-height:1.8}
.apc-d dt{font-size:12px;font-weight:700;color:var(--muted,#5c6984);padding-top:2px}
.apc-d dd{margin:0;color:var(--ink,#1d2b45)}
.apc-d b{background:linear-gradient(transparent 58%,#fde7a8 58%);font-weight:700;color:var(--navy,#0b1f4b)}
.apc-full{background:#f4f7fc;border-radius:10px;padding:8px 10px;margin:0 -10px}
.apc-full dt{color:var(--c,#16294d)}
.apc-note dd{color:var(--muted,#5c6984)}
.apx-cap{margin:2px 0 8px;font-size:12px;font-weight:700;color:var(--navy,#0b1f4b)}.apx-cap small{margin-left:8px;font-weight:500;color:var(--muted,#5c6984)}
.apx{display:grid;gap:8px}
.apx-lv{display:grid;grid-template-columns:92px minmax(0,1fr);gap:14px;padding:10px 14px;border:1px solid #e8ecf3;border-radius:10px}
.apx-top{background:#f3f6fc;border-color:#d3ddef}
.apx-s b{display:block;font-size:21px;font-weight:700;color:var(--c,#16294d);line-height:1.1}.apx-s b small{font-size:11px;margin-left:1px}
.apx-s span{display:block;font-size:10.5px;line-height:1.45;color:var(--muted,#5c6984);margin-top:4px}
.apx-l{list-style:none;margin:0;padding:0}
.apx-l li{position:relative;padding:4px 0 4px 15px}
.apx-l li::before{content:"";position:absolute;left:0;top:14px;width:5px;height:5px;border-radius:1px;background:var(--c,#16294d);opacity:.7}
.apx-l li.apx-or,.apx-l li.apx-in{padding-left:0}.apx-l li.apx-or::before,.apx-l li.apx-in::before{display:none}
.apx-or{font-size:11.5px;font-weight:700;color:var(--muted,#5c6984)}.apx-or span{margin-right:8px;letter-spacing:.06em}
.apx-en{margin:0;font-family:Georgia,"Times New Roman",serif;font-size:14.5px;line-height:1.7;color:var(--ink,#1d2b45);overflow-wrap:break-word}
.apx-ja{margin:2px 0 0;font-size:13px;line-height:1.75;color:var(--muted,#5c6984)}
.apx-ja b{background:linear-gradient(transparent 58%,#fde7a8 58%);font-weight:700;color:var(--navy,#0b1f4b)}
.apx-in .apx-en,.apx-in .apx-ja{font-size:13px}
.apx-dr{margin:10px 0 0;border-top:1px dashed var(--line,#d9deea)}
.apx-dr summary{cursor:pointer;list-style:none;display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 10px;padding:10px 0 4px;font-size:13px;font-weight:700;color:var(--c,#16294d)}
.apx-dr summary::-webkit-details-marker{display:none}
.apx-dr summary::before{content:"+";display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;border:1.5px solid currentColor;font-size:13px;line-height:1}
.apx-dr[open] summary::before{content:"−"}
.apx-dr summary small{font-weight:500;color:var(--muted,#5c6984);font-size:12px}
.apx-dr .apx{margin-top:8px}
.apx-note,.apx-dir{margin:12px 0 0;background:#f8f9fc;border-left:3px solid var(--c,#16294d);border-radius:0 10px 10px 0;padding:10px 14px}
.apx-dir{margin:14px 20px 2px}
.apx-nh{margin:0 0 4px;font-size:12px;font-weight:700;color:var(--navy,#0b1f4b)}.apx-nh small{margin-left:8px;font-weight:500;color:var(--muted,#5c6984)}
.apdef dt small{display:block;font-size:11px;font-weight:500;color:var(--muted,#5c6984)}
.apdef dd .apx-en{font-size:13.5px;margin-top:4px}.apdef dd .apx-en b{font-weight:700}
.apdef div:last-child{grid-column:1/-1}
@media(max-width:760px){.apx-lv{grid-template-columns:1fr;gap:4px;padding:10px 12px}.apx-s{display:flex;align-items:baseline;gap:8px}.apx-s span{margin:0}.apx-dir{margin:12px 15px 2px}.apx-en{font-size:14px}}
.apex-w{margin:6px 0 18px}
.apex{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line,#d9deea);border-radius:14px;overflow:hidden;font-size:14px}
.apex thead th{background:var(--ct,#e9edf5);color:var(--navy,#0b1f4b);font-size:12.5px;font-weight:700;padding:11px 14px;text-align:center;border-bottom:2px solid var(--navy,#0b1f4b)}
.apex thead th:first-child{text-align:left}
.apex td{text-align:center;padding:10px 14px;color:var(--ink,#1d2b45);font-variant-numeric:tabular-nums;white-space:nowrap;vertical-align:middle}
.apex tbody th{text-align:left;font-weight:400;padding:10px 14px}
.apex tbody tr{border-top:1px dotted #cfd6e3}
.apex th b{font-weight:700;color:var(--navy,#0b1f4b)}
.apex th small{margin-left:8px;font-size:11.5px;color:var(--muted,#5c6984)}
.apex .apex-d{display:block;margin:3px 0 0;font-size:12px;line-height:1.6}
.apex-tag{display:inline-block;min-width:66px;font-size:11px;font-weight:700;color:var(--muted,#5c6984)}
.apex-sec{background:#f3f6fc;border-top:1px solid var(--line,#d9deea)!important}
.apex-sec th b{font-size:15.5px;color:var(--c,#16294d)}.apex-sec td{font-weight:700;font-size:15px;color:var(--c,#16294d)}.apex-sec .apex-tag{color:var(--c,#16294d)}
.apex-part th{padding-left:30px!important}
.apex-q{background:#fafbfd}.apex-q th{padding-left:74px!important}.apex-q .apex-tag{min-width:34px}
.apex-q .apex-d{margin-left:34px}.apex-part .apex-d{margin-left:66px}
.apex thead th{background:#dce9f8;border-bottom:0}
.apex tbody tr.apex-sec{background:var(--c,#16294d);border-top:0!important}
.apex-sec th b,.apex-sec td,.apex-sec .apex-tag{color:#fff!important}.apex-sec th small{color:rgba(255,255,255,.75)}
.apex tbody tr.apex-part{background:#edf3fb;border-top:1px solid #d6e2f3}
.apex-part .apex-tag{color:#2c5d9e}
.apex tbody tr.apex-q{background:#fff;border-top:1px dotted #d6deea}
.apex-q .apex-tag{color:#8a96ab}
.apex-q td,.apex-part td{color:var(--navy,#0b1f4b);font-weight:600}
@media(max-width:760px){.apex{font-size:13px}.apex thead th,.apex td{padding:9px 6px}.apex tbody th{padding:9px 8px}
.apex-part th{padding-left:14px!important}.apex-q th{padding-left:24px!important}.apex-tag{display:block;min-width:0}
.apex th small{display:block;margin:0}.apex .apex-d,.apex-q .apex-d,.apex-part .apex-d{margin-left:0}.apex thead th:not(:first-child),.apex td{width:52px}}
/* overview */
.apo-bar{display:flex;gap:3px;margin:8px 0 14px;border-radius:12px;overflow:hidden;min-height:76px}
.apo-bar>div{padding:12px 16px;display:flex;flex-direction:column;justify-content:center;min-width:0}
.apo-bar b{font-size:24px;line-height:1.1}.apo-bar span{font-size:13.5px;font-weight:700;margin-top:2px}.apo-bar small{font-size:11.5px;opacity:.85}
.apo-b1{background:#dce9f8;color:var(--navy,#0b1f4b)}
.apo-b2{background:var(--c,#16294d);color:#fff}
.apo-w{overflow-x:auto;margin:0 0 6px}
.apo{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line,#d9deea);font-size:13px}
.apo thead th{background:#dce9f8;color:var(--navy,#0b1f4b);padding:9px 6px;font-size:12px;vertical-align:bottom;text-align:center}
.apo thead th:first-child{text-align:left;padding-left:12px}
.apo thead th b{display:block;font-size:15px}.apo thead th small{display:block;font-weight:500;font-size:11px;line-height:1.35}
.apo tbody tr{border-top:1px solid #e6ebf3}
.apo tbody th{text-align:left;padding:9px 12px;font-weight:400;white-space:nowrap}.apo tbody th b{display:block;color:var(--navy,#0b1f4b)}.apo tbody th small{font-size:11px;color:var(--muted,#5c6984)}
.apo td{text-align:center;padding:8px 4px}
.apo-w td.apo-w,.apo td.apo-w{font-weight:700;color:var(--navy,#0b1f4b);font-variant-numeric:tabular-nums}
.apo-all span{color:#7ea3d4;font-size:13px}
.apo-no span{color:#c3cad6}
.apo-key{background:var(--c,#16294d)}.apo-key span{color:#fff;font-size:11px;font-weight:700}
.apo-pj{background:#f6f8fc}
.apo-lg{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12px;color:var(--muted,#5c6984);margin:6px 0 0}
.apo-lg span{display:inline-flex;align-items:center;gap:6px}.apo-dot{width:8px;height:8px;border-radius:50%;background:#7ea3d4;display:inline-block}
.apo-tm{font-style:normal;background:var(--c,#16294d);color:#fff;font-size:10px;font-weight:700;padding:1px 6px;border-radius:4px}
@media(max-width:600px){.apo{font-size:12px;table-layout:fixed}.apo thead th small,.apo tbody th small{display:none}
.apo thead th:first-child{width:96px;padding-left:8px}.apo thead th:nth-child(2){width:38px}.apo tbody th{white-space:normal;padding:8px;font-size:12px;line-height:1.4}
.apo td{padding:8px 0}.apo-key span{font-size:9px;letter-spacing:-.02em}.apo-bar b{font-size:20px}.apo-bar>div{padding:10px 12px}}
/* bullets */
.apb{margin:8px 0 16px;padding:0 0 0 1.2em;font-size:14.5px;line-height:1.85;color:var(--ink,#1d2b45)}
.apb li{margin:3px 0;padding-left:2px}.apb li::marker{color:var(--c,#16294d)}
/* unit tiles + bubble */
.au{margin:6px 0 8px}
.au-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.aut{position:relative;display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto;column-gap:12px;align-items:center;text-align:left;font:inherit;background:#fff;border:1px solid var(--line,#d9deea);border-radius:12px;padding:14px 14px;cursor:pointer;color:var(--navy,#0b1f4b);min-height:74px}
.aut:hover{border-color:var(--c,#16294d)}.aut:focus-visible{outline:2px solid var(--c,#16294d);outline-offset:2px}
.aut-n{grid-row:1/3;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:#dce9f8;color:var(--c,#16294d);font-weight:800;font-size:16px}
.aut b{font-size:15px;line-height:1.35}.aut small{font-size:11px;color:var(--muted,#5c6984)}
.aut-pj{position:absolute;top:-9px;right:10px;font-style:normal;font-size:10px;font-weight:700;background:#fff;color:var(--c,#16294d);border:1px solid var(--c,#16294d);border-radius:999px;padding:1px 8px}
.aut.on{background:var(--c,#16294d);border-color:var(--c,#16294d);color:#fff}.aut.on small{color:rgba(255,255,255,.75)}.aut.on .aut-n{background:#fff}
.au-bs{position:relative}
.aub{margin:12px 0 0;background:#fff;border:1.5px solid var(--c,#16294d);border-radius:14px;padding:16px 20px 14px;position:relative}
.au.js .aub{display:none}.au.js .aub.on{display:block;animation:aubIn .22s ease-out}
.aub::before{content:"";position:absolute;top:-9px;left:calc(var(--tx,60px) - 9px);width:16px;height:16px;background:#fff;border-left:1.5px solid var(--c,#16294d);border-top:1.5px solid var(--c,#16294d);transform:rotate(45deg)}
.au:not(.js) .aub::before{display:none}
@keyframes aubIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.au.js .aub.on{animation:none}}
.aub-h{margin:0 0 6px;font-size:13px;font-weight:700;color:var(--c,#16294d)}
.aub-q{margin:0;padding:0 0 0 1.6em;font-size:15.5px;line-height:1.8;font-weight:600;color:var(--navy,#0b1f4b)}.aub-q li{margin:3px 0}.aub-q li::marker{color:var(--c,#16294d);font-weight:800}
.aub-t{margin:10px 0 0;padding-top:10px;border-top:1px dashed var(--line,#d9deea);font-size:12.5px;line-height:1.7;color:var(--muted,#5c6984)}.aub-t span{font-weight:700;margin-right:10px;color:var(--navy,#0b1f4b)}
@media(max-width:700px){.au-g{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.aut{padding:12px 10px;column-gap:8px;min-height:64px}.aut-n{width:30px;height:30px;font-size:14px}.aut b{font-size:13.5px}.aut small{font-size:10px}.aut-pj{font-size:9px;right:6px}.aub{padding:14px 14px 12px}.aub-q{font-size:14.5px}}
/* matrix */
.amx-wr{margin:4px 0 6px}
.amx{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line,#d9deea);font-size:13.5px;table-layout:fixed}
.amx thead th{background:#dce9f8;color:var(--navy,#0b1f4b);padding:9px 4px;font-size:12px;vertical-align:bottom;text-align:center}
.amx thead th:first-child{text-align:left;padding-left:14px;width:34%}.amx thead th:nth-child(2){width:9%}
.amx-u b{display:block;font-size:15px}.amx-u small{display:block;font-weight:500;font-size:10.5px;line-height:1.3}
.amx tbody th{text-align:left;font-weight:400;padding:9px 14px}
.amx tbody th b{color:var(--navy,#0b1f4b)}
.amx-tag{display:inline-block;min-width:64px;font-size:11px;font-weight:700;color:var(--muted,#5c6984)}
.amx td{text-align:center;padding:8px 2px}
.amx-w{font-weight:700;color:var(--navy,#0b1f4b);font-variant-numeric:tabular-nums}
.amx tbody tr{border-top:1px solid #e6ebf3}
.amx tbody tr.amx-sec{background:var(--c,#16294d);border-top:0}.amx tbody tr.amx-sec th b,.amx tbody tr.amx-sec .amx-tag,.amx tbody tr.amx-sec .amx-w{color:#fff}.amx-sec th b{font-size:14.5px}
.amx tbody tr.amx-part{background:#edf3fb}.amx-part .amx-tag{color:#2c5d9e}.amx-part th{padding-left:30px}
.amx-q th{padding-left:52px!important}.amx-q .amx-tag{min-width:30px;color:#8a96ab}
.amx-all i{display:inline-block;width:10px;height:10px;border-radius:50%;background:#7ea3d4}
.amx-key{background:#16294d;background:var(--c,#16294d)}.amx-key span{color:#fff;font-size:11px;font-weight:700}
.amx-part .amx-key,.amx-q .amx-key{box-shadow:inset 0 0 0 1px #fff}
@media(max-width:700px){.amx{font-size:12px}.amx thead th:first-child{width:40%;padding-left:8px}.amx thead th:nth-child(2){width:12%}.amx-u small{display:none}
.amx tbody th{padding:8px 6px;line-height:1.35}.amx-tag{display:block;min-width:0;font-size:9.5px}.amx-part th{padding-left:10px}.amx-q th{padding-left:16px!important}
.amx-key span{font-size:0}.amx-key span::after{content:"★";font-size:12px}.apo-tm::before{content:"★ "}.amx-all i{width:8px;height:8px}}
.apg{margin:0 0 14px;padding:0}
.apg div{display:grid;grid-template-columns:230px 1fr;gap:12px;padding:8px 0;border-top:1px solid #e6ebf3}.apg div:last-child{border-bottom:1px solid #e6ebf3}
.apg dt{font-weight:700;color:var(--navy,#0b1f4b);font-size:14px}.apg dt small{display:block;font-weight:500;font-size:11.5px;color:var(--muted,#5c6984)}
.apg dd{margin:0;font-size:14px;line-height:1.75;color:var(--ink,#1d2b45)}
.apx-top2{background:#f3f6fc;border-radius:10px;padding:10px 14px 8px;margin:0 0 4px}
.apx-top2 .apx-cap{margin:6px 0 4px;color:var(--c,#16294d)}.apx-top2 .apx-cap:first-child{margin-top:0}
.apx-top2 .apx-cap+.apx-l{margin-bottom:8px}
.apx-dr summary{font-size:12.5px}
.apx-lowg .apx-lv{grid-template-columns:44px minmax(0,1fr)}
.apx-lowg .apx-s b{font-size:14px;color:var(--muted,#5c6984)!important}
.apx-lowg .apx-en{font-size:12.5px;line-height:1.6;color:var(--muted,#5c6984)}.apx-lowg .apx-ja{font-size:12px;line-height:1.6}
.apx-lowg .apx-ja b{background:none;font-weight:600}
.apx-sub{margin:4px 0 2px;font-size:11px;font-weight:700;color:var(--muted,#5c6984)}
@media(max-width:760px){.apg div{grid-template-columns:1fr;gap:2px}.apx-top2{padding:10px 10px 6px}.apx-lowg .apx-lv{grid-template-columns:1fr}}
.amx-key a{display:block;text-decoration:none}

.amx-link{position:relative;display:flex;align-items:center;gap:14px;margin:12px 0 0;padding:12px 16px;background:var(--c,#16294d);color:#fff;border-radius:10px;text-decoration:none}
.amx-link::before{content:"";position:absolute;top:-8px;left:calc(66.75% - 8px);width:16px;height:16px;background:var(--c,#16294d);transform:rotate(45deg)}
.amx-link:hover{filter:brightness(1.12)}
.amx-ln{flex:none;width:28px;height:28px;border-radius:50%;background:#fff;color:var(--c,#16294d);display:grid;place-items:center;font-weight:800;font-size:14px;position:relative}
.amx-link b{display:block;font-size:14.5px}.amx-link small{display:block;font-size:12px;opacity:.85;line-height:1.6}
.amx-link i{margin-left:auto;font-style:normal;font-size:18px;position:relative}
.amx-link>span{position:relative}
.amx-back{margin:0 0 10px}.amx-back a{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--c,#16294d);text-decoration:none;border-bottom:1px dotted currentColor}
@media(max-width:700px){.amx-link::before{left:calc(72% - 8px)}.amx-link{padding:12px 12px;gap:10px}.amx-link b{font-size:13.5px}}
.apk{margin:0 0 14px;position:sticky;top:144px;z-index:15;background:var(--bg,#fbfaf7);padding:8px 0 8px;box-shadow:0 6px 8px -8px rgba(11,31,75,.25)}
.apk-h{margin:0 0 6px;font-size:13px;font-weight:700;color:var(--navy,#0b1f4b)}.apk-h small{margin-left:8px;font-size:11.5px;font-weight:500;color:var(--muted,#5c6984)}
.apk-b{display:flex;gap:3px}
.apk-b a{min-width:0;display:flex;flex-direction:column;gap:2px;padding:9px 10px;background:#dce9f8;color:var(--navy,#0b1f4b);text-decoration:none;border-radius:4px}
.apk-b a:first-child{border-radius:10px 4px 4px 10px}.apk-b a:last-child{border-radius:4px 10px 10px 4px}
.apk-b a:nth-child(even){background:#c4d6ee}
.apk-b a:hover,.apk-b a.cur{background:var(--c,#16294d);color:#fff}
.apk-b b{font-size:18px;line-height:1.1}.apk-b b small{font-size:10.5px;margin-left:1px}
.apk-b span{font-size:12px;font-weight:600;line-height:1.35;overflow-wrap:anywhere}
.apc{scroll-margin-top:240px}
@media(max-width:900px){.apk{top:var(--apk-top,220px)}.apc{scroll-margin-top:310px}}
@media(max-width:700px){.apk-h small{display:none}.apk-b a{padding:7px 5px}.apk-b span{font-size:10.5px}.apk-b b{font-size:15px}}
.amx td.amx-bub{padding:4px 8px 4px 12px;vertical-align:middle;text-align:left}
.amx-bq{position:relative;display:block;background:#fff;border:1.5px solid var(--c,#16294d);border-radius:10px;padding:8px 11px;text-decoration:none;color:var(--ink,#1d2b45);font-size:12px;line-height:1.6}
.amx-bq::before{content:"";position:absolute;left:-7px;top:50%;margin-top:-6px;width:11px;height:11px;background:#fff;border-left:1.5px solid var(--c,#16294d);border-bottom:1.5px solid var(--c,#16294d);transform:rotate(45deg)}
.amx-bq:hover{background:#f3f6fc}.amx-bq:hover::before{background:#f3f6fc}
.amx-bq b{display:block;font-size:12.5px;color:var(--navy,#0b1f4b);margin-bottom:1px}
.amx-bq em{font-style:normal;font-weight:700;color:var(--c,#16294d);border-bottom:1px solid currentColor}
.amx-bs{display:none}
@media(max-width:700px){.amx td.amx-bub{padding:3px 3px 3px 9px}.amx-bq{padding:6px 6px;font-size:10.5px;line-height:1.45;border-radius:8px}.amx-bl{display:none}.amx-bs{display:block}.amx-bq::before{left:-6px;width:9px;height:9px;margin-top:-5px}}
.apsx{margin:14px -22px 10px;background:#e9f0f9;border:1px solid #d3deef;border-radius:18px;padding:0 22px 18px}
.apsx-h{display:flex;align-items:center;flex-wrap:wrap;gap:6px 12px;margin:0 -22px 18px;padding:12px 22px;background:var(--c,#16294d);color:#fff;border-radius:17px 17px 0 0}
.apsx-h svg{width:20px;height:20px;flex:none}.apsx-h b{font-size:15px;letter-spacing:.04em}

.apsx .aps{margin:0}
.apsx .apk{background:#e9f0f9}
.apsx .apk-b a{background:#fff;box-shadow:inset 0 0 0 1px #cfdcee}.apsx .apk-b a:nth-child(even){background:#f6f9fd}
.apsx .apk-b a:hover,.apsx .apk-b a.cur{background:var(--c,#16294d);color:#fff;box-shadow:none}
.apsx .aps-h small{color:#5c6984}
@media(max-width:900px){.apsx{margin:14px -12px 10px;padding:0 10px 14px;border-radius:14px}.apsx-h{margin:0 -10px 12px;padding:10px 12px;border-radius:13px 13px 0 0}.apsx .aps-nav{background:#e9f0f9}}
.apsx-sw{margin-left:auto;display:inline-flex;background:rgba(255,255,255,.14);border-radius:999px;padding:3px}
.apsx-sw button{font:inherit;font-size:12.5px;font-weight:700;color:#fff;background:none;border:0;border-radius:999px;padding:5px 14px;cursor:pointer}
.apsx-sw button[aria-pressed="true"]{background:#fff;color:var(--c,#16294d)}
.apsx-sw button:focus-visible{outline:2px solid #fff;outline-offset:2px}
.apsx:not(.m-tips) .aps-tips{display:none}
.apsx.m-tips .aps-p>:not(.aps-tips){display:none}
.apsx.m-tips .aps-tips{margin-top:4px}
.kp .kp-h{margin:0 0 6px;font-size:13.5px;font-weight:800;color:var(--c,#16294d)}.kp ul+.kp-h{margin-top:14px;padding-top:12px;border-top:1px solid var(--line,#d9deea)}
.kp li b{color:var(--navy,#0b1f4b)}
.apt-ch{margin:18px 0 8px;font-size:14px;font-weight:700;color:var(--navy,#0b1f4b)}
.apt-sum{margin:18px 0 6px;background:#fff;border:1.5px solid var(--c,#16294d);border-radius:14px;padding:14px 18px}
.apt-sh{margin:0 0 6px;font-size:14px;font-weight:800;color:var(--c,#16294d)}
.apt-sum ul{margin:0;padding-left:1.2em}.apt-sum li{font-size:14px;line-height:1.8}
.apt-sf{margin:8px 0 0;font-size:14px;color:var(--navy,#0b1f4b)}
.aps-th small[lang]{display:inline;margin-left:4px;font-size:12px}
.apsx .tp-rd{margin-top:0}
/* section rhythm */
.ajs{position:relative;padding:8px 0 40px}
.ajs-alt{background:#f1f5fb;box-shadow:0 0 0 100vmax #f1f5fb;clip-path:inset(0 -100vmax);padding:4px 0 44px;margin:28px 0}
.ajs+.ajs:not(.ajs-alt){margin-top:28px}
.step{display:grid!important;grid-template-columns:auto minmax(0,1fr);align-items:center!important;column-gap:16px!important;margin:44px 0 22px!important;padding:0 0 16px!important;border-bottom:2px solid var(--c,#16294d)!important}
.ajs:first-child .step{margin-top:16px!important}
.step-n{display:grid!important;place-items:center;width:52px!important;height:52px!important;border-radius:14px!important;background:var(--c,#16294d)!important;color:#fff!important;font-family:var(--latin)!important;font-size:22px!important;font-weight:800!important;line-height:1!important}
.step-n::after{content:none!important}
.step h3{font-size:clamp(21px,2.6vw,27px)!important;line-height:1.35!important;color:var(--navy,#0b1f4b)}
.step-sub{font-size:14px!important;margin-top:4px!important;color:var(--muted,#5c6984)}
@media(max-width:700px){.step{column-gap:12px!important}.step-n{width:42px!important;height:42px!important;font-size:18px!important;border-radius:11px!important}.ajs-alt{padding-bottom:32px}}
.ajs-alt .apex{border:2px solid var(--c,#16294d)!important;border-radius:0!important;box-shadow:none}
.ajs-alt .apex-w .apex{border-collapse:collapse}
.ajs-alt .apex td,.ajs-alt .apex tbody th{border-left:0}
.ajs-alt .apex td{border-left:1px solid #d3deee}
.ajs-alt .apex thead th:not(:first-child){border-left:1px solid #d3deee}
.ajs-alt .apex tbody tr.apex-sec td{border-left-color:rgba(255,255,255,.18)}
.ajs-alt .apex thead th{background:#fff;border-bottom:2px solid var(--c,#16294d)}
.ajs-alt .apex tbody tr.apex-part{background:#e4edf9;border-top:1px solid #cddbef}
.ajs-alt .apex tbody tr.apex-q{background:#fff}
.kp{max-width:none!important}
/* scoring panels */
.aps{display:grid;grid-template-columns:200px minmax(0,1fr);gap:22px;align-items:start;margin:8px 0 10px}
.aps-nav{position:sticky;top:160px;display:grid;gap:6px}
.aps-h{margin:0 0 4px;font-size:12px;font-weight:700;color:var(--muted,#5c6984)}.aps-h b{margin-left:6px;font-size:16px;color:var(--navy,#0b1f4b)}.aps-h small{display:block;font-weight:500;font-size:10.5px;line-height:1.5;margin-top:2px}
.aps-b{position:relative;display:grid;grid-template-columns:auto 1fr auto;align-items:baseline;gap:2px 8px;text-align:left;font:inherit;background:#fff;border:1px solid var(--line,#d9deea);border-radius:10px;padding:10px 12px 14px;cursor:pointer;color:var(--navy,#0b1f4b);overflow:hidden}
.aps-b:hover{border-color:var(--c,#16294d)}
.aps-b:focus-visible{outline:2px solid var(--c,#16294d);outline-offset:2px}
.aps-q{font-size:12px;font-weight:800;color:var(--c,#16294d)}
.aps-n{font-size:13px;font-weight:700;line-height:1.4}.aps-n small{display:block;font-size:10.5px;font-weight:500;color:var(--muted,#5c6984)}
.aps-pc{font-size:17px;font-weight:700;font-variant-numeric:tabular-nums}
.aps-m{position:absolute;left:0;bottom:0;height:4px;background:#b9cfec}
.aps-b.on{background:var(--c,#16294d);border-color:var(--c,#16294d);color:#fff}
.aps-b.on .aps-q,.aps-b.on .aps-n small{color:rgba(255,255,255,.8)}.aps-b.on .aps-m{background:#7ea3d4}
.aps-def{grid-template-columns:auto 1fr;padding-bottom:10px}
.aps.js .aps-p{display:none}.aps.js .aps-p.on{display:block}
.aps-p>.apr-t:first-child{margin-top:0}
.aps-tips{margin:6px 0 10px}
.aps-th{margin:0 0 10px;font-size:15px;font-weight:700;color:var(--navy,#0b1f4b)}.aps-th small{display:block;font-size:11.5px;font-weight:500;color:var(--muted,#5c6984)}
@media(max-width:900px){.aps{grid-template-columns:1fr;gap:12px}
.aps-nav{top:136px;z-index:20;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;background:var(--bg,#fbfaf7);padding:6px 0}
.aps-h{display:none}.aps-b{grid-template-columns:1fr;padding:7px 6px 10px;text-align:center;gap:0}.aps-n{font-size:10.5px;line-height:1.3}.aps-n small{display:none}.aps-pc{font-size:13px}.aps-def .aps-n{font-size:10.5px}}
@media(max-width:760px){.apu-g,.apdef{grid-template-columns:1fr}.apc{padding:14px 15px}.apc-d>div{grid-template-columns:1fr;gap:2px}.apc-ts{margin-left:0;width:100%}.apr-h{padding:14px 15px}}
/* flat: no boxes */
.apx{gap:0}
.apx-lv{border:0;border-radius:0;border-top:1px solid #eef1f6;padding:8px 0;grid-template-columns:72px minmax(0,1fr);gap:10px;background:none}
.apx-lv:first-child{border-top:0}
.apx-top{background:none}.apx-top .apx-s b{color:var(--c,#16294d)}
.apx-lv:not(.apx-top) .apx-s b{color:var(--muted,#5c6984)}
.apx-s b{font-size:17px}.apx-s span{display:none}
.apx-l li{padding:2px 0 2px 15px}.apx-l li::before{top:12px}
.apx-note,.apx-dir{background:none;border:0;border-radius:0;padding:0;margin:10px 0 0}
.apx-dir{margin:12px 20px 0}
.apdef{display:block;margin:0 0 22px}
.apdef div{background:none;border:0;border-radius:0;padding:5px 0 5px 15px;position:relative}
.apdef div::before{content:"";position:absolute;left:0;top:14px;width:5px;height:5px;border-radius:1px;background:var(--c,#16294d);opacity:.7}
.apdef dt{display:inline;font-size:14px}.apdef dt small{display:inline;margin-left:6px}
.apdef dd{margin:2px 0 0}
@media(max-width:760px){.apx-lv{grid-template-columns:1fr;gap:0;padding:8px 0}.apdef{display:block}}
'''
    return '<style id="apjp-css">' + rb + own + '</style>\n'

# ---------------- 1 overview: 6 units x exam ----------------
OV_ROWS = [  # (label, en, weight, key-only?)
 ('Q1 プロジェクトの発表', 'Project Presentation', '20%', True),
 ('Q2 発表への質問', 'Project Q&amp;A', '15%', True),
 ('Q3 物語', 'Story Narration', '7.5%', False),
 ('Q4 メールへの返信', 'Email Response', '7.5%', False),
 ('リスニング', 'Listening', '25%', False),
 ('リーディング', 'Reading', '25%', False),
]
MX = [  # kind, tag, ja, weight, mode ('key' = project unit only, 'all' = all units, None = band)
 ('sec', 'Section I', '記述・口述問題', '50%', None),
 ('part', 'Part A', 'スピーキング', '', None),
 ('q', 'Q1', 'プロジェクトの発表', '20%', 'key'),
 ('q', 'Q2', '発表への質問', '15%', 'key'),
 ('part', 'Part B', 'ライティング', '', None),
 ('q', 'Q3', '物語', '7.5%', 'all'),
 ('q', 'Q4', 'メールへの返信', '7.5%', 'all'),
 ('sec', 'Section II', '選択式問題', '50%', None),
 ('part', 'Part A', 'リスニング', '25%', 'all'),
 ('part', 'Part B', 'リーディング', '25%', 'all'),
]
def overview_html():
    heads = ''.join('<th scope="col" class="amx-u"><b>%s</b><small>%s</small></th>' % (n, ja) for n, ja, *_ in UNITS)
    body = ''
    for kind, tag, ja, w, mode in MX:
        if mode is None:
            cells = '<td class="amx-w">%s</td><td colspan="2"></td><td class="amx-c3"></td><td colspan="3"></td>' % w
        else:
            if mode == 'key':
                first = tag == 'Q1'
                cells = ('<td class="amx-w">%s</td><td class="amx-no"></td><td class="amx-no"></td>'
                         '<td class="amx-key"><a href="#project" aria-label="テーマ：4 コースプロジェクトへ"><span>テーマ</span></a></td>' % w)
                if first:
                    cells += ('<td colspan="3" rowspan="2" class="amx-bub"><a class="amx-bq" href="#project">'
                              '<span class="amx-bl"><b>事前準備はコースプロジェクト</b>1月から調べたテーマを試験当日に発表。詳しくは<em>4</em>へ</span>'
                              '<span class="amx-bs">準備は<em>4</em>のプロジェクトで</span></a></td>')
            else:
                cells = '<td class="amx-w">%s</td>' % w + ''.join(
                    '<td class="amx-all%s"><i></i></td>' % (' amx-c3' if n == '3' else '') for n, *_ in UNITS)
        body += '<tr class="amx-%s"><th scope="row"><span class="amx-tag" lang="en">%s</span><b>%s</b></th>%s</tr>' % (kind, tag, ja, cells)
    return (step(3, 'overview', '単元と試験の関係', '試験は6つの単元すべてから出題。そのうえで、プロジェクトのテーマになる単元がとくに重要') +
            '<p class="rlead">試験に「単元別の問題」はありません。<b>書く問題（Q3 物語・Q4 メールへの返信）</b>と<b>選択式のリスニング・リーディング</b>は、<b>6つの単元すべての話題</b>から出題されます。'
            '一方、<b>話す問題（Q1 プロジェクトの発表・Q2 発表への質問）</b>は、その年のコースプロジェクトの成果を答える問題で、2026-27年度は<b>単元3「芸術と創造性」</b>がテーマです。'
            'どの単元も大切で、そのうち単元3は、1年をかけて深く調べる単元になります</p>'
            '<div class="amx-wr rise"><table class="amx"><thead><tr><th scope="col">試験の問題</th><th scope="col">比重</th>@@H@@</tr></thead><tbody>@@B@@</tbody></table>'
            '</div>'
            '<p class="apo-lg"><span><i class="apo-dot"></i>どの単元の話題からも出題される</span><span><i class="apo-tm">テーマ</i>その年のプロジェクトのテーマ</span></p>'
            '<p class="apr-src">出典：College Board「AP Japanese Language and Culture Course and Exam Description」（Effective Fall 2026）。'
            '試験については「The exam assesses skills developed in each of the six thematic units」と記載</p>').replace('@@H@@', heads).replace('@@B@@', body)

# ---------------- 5 scoring: sticky score split + panels ----------------
PANELS = [  # id, label, name, pct, pts, html
 ('q1', 'Q1', 'プロジェクトの発表', '20%', 11, lambda: Q1),
 ('q2', 'Q2', '発表への質問', '15%', 9, lambda: Q2),
 ('q3', 'Q3', '物語', '7.5%', 8, None),
 ('q4', 'Q4', 'メールへの返信', '7.5%', 8, None),
]
TIPQ = {'q1': 'Q1', 'q2': 'Q2', 'q3': 'Q3', 'q4': 'Q4'}
NT = {
 'q1': ('Q1｜プロジェクトの発表', 'Project Presentation', [
   ('3つ以上の要因を、具体例とともに説明する', '要因を並べるだけでは不十分。調べた情報や具体例を使い、それぞれ詳しく説明する'),
   ('文化の背景にある価値観まで説明する', '「何があるか」だけでなく「なぜそうなのか」を説明する。文化的な産物や慣習と、価値観のつながりが重要'),
   ('導入・本論・結論を明確にする', '最初に発表の全体像を示し、「まず」「次に」「このように」などで論理的につなぐ'),
   ('原稿を読むのではなく、自分の言葉で話す', '骨子メモを手がかりに、自然な速さ・抑揚・明瞭な発音で伝える。単調な読み上げや暗唱を避ける')]),
 'q2': ('Q2｜発表への質問', 'Project Q&amp;A', [
   ('質問には結論から答える', '最初の一文で答え、理由や具体例を加える。4問すべてに答える練習をし、わからない質問があっても次に集中する'),
   ('文化の比較か振り返りを入れる', '少なくとも1問で、文化の共通点・違いを比較するか、文化的な産物・慣習と価値観の関係を具体的に説明する'),
   ('わからない言葉は日本語で言い換える', '英語に頼らず、知っている日本語で説明する。「作曲家」が出てこなければ「曲を作る人」と言い換える')]),
 'q3': ('Q3｜物語', 'Story Narration', [
   ('4コマすべてを使い、物語を完結させる', '絵の説明だけでなく、登場人物や出来事を具体的に描く。絵がなくても内容が伝わる物語にする'),
   ('始まり・展開・結末を明確にする', '「ある日」「ところが」「その結果」などを使い、出来事を自然につなぐ'),
   ('詳細や会話で物語を具体的にする', '人物の行動や状況を詳しく描く。必要に応じて会話を加え、物語をわかりやすくする')]),
 'q4': ('Q4｜メールへの返信', 'Email Response', [
   ('2つの依頼の両方に答える', 'メールで求められた2つの情報を確認し、それぞれ具体的な説明や例を添えて答える'),
   ('あいさつ・本文・結びを整える', 'あいさつ→2つの依頼への回答→結びの順に、読みやすく構成する'),
   ('相手に合った言葉遣いを使う', '友人や先生など、相手と場面に合わせた丁寧さを保つ。語彙や文型にも変化をつける')]),
}
NT_COMMON = ('伝わる日本語と、表現の幅を意識する', '理解を妨げる誤りを減らし、話題に合った語彙と多様な文型を使う。単純な文の繰り返しを避け、考えを正確に伝える')
NT_SUM = [('Q1 発表', '3つ以上の要因を具体例で説明し、文化の価値観まで掘り下げる'), ('Q2 質問', '質問に的確に答え、文化の比較や振り返りを示す'),
          ('Q3 物語', '4コマすべてを使い、具体的で筋の通った物語を書く'), ('Q4 メール', '2つの依頼に答え、相手に合った言葉遣いで書く')]
CIRC = '①②③④⑤⑥'
# old TIP number -> new tip per panel ('c' = 全問共通). Some depend on the linked phrase.
TMAP = {'q1': {1: 1, 2: 2, 3: 3, 4: 4, 9: 'c', 10: 'c'},
        'q2': {2: 2, 5: 1, 6: 2, 9: 'c', 10: 3},
        'q3': {3: 2, 7: 1, 9: 'c'},
        'q4': {3: 2, 8: 1, 9: 'c'}}
def tmap(pid, n, phrase=''):
    if pid == 'q3' and n == 7 and 'dialogue' in phrase: return 3
    if pid == 'q4' and n == 8:
        if 'greeting' in phrase: return 2
        if 'register' in phrase: return 3
    return TMAP[pid].get(n, 'c')
def tlabel(t):
    return '共通のコツ' if t == 'c' else 'コツ' + CIRC[t - 1]
def new_tip_card(pid, t):
    title, body = NT_COMMON if t == 'c' else NT[pid][2][t - 1]
    return ('<article class="tp" id="tip-%s-%s" data-title="%s" data-sum="%s"><h4><span class="tp-no">%s</span>%s</h4><p class="tp-rd">%s</p></article>'
            % (pid, t, title, body, tlabel(t), title, body))
def tips_block(pid):
    q, en, lst = NT[pid]
    cards = ''.join(new_tip_card(pid, i) for i in range(1, len(lst) + 1))
    summ = ('<div class="apt-sum"><p class="apt-sh">まとめ｜得点につながる4つのポイント</p><ul>%s</ul><p class="apt-sf">共通して重要なのは、<b>具体性・論理的な構成・伝わる日本語</b></p></div>'
            % ''.join('<li><b>%s：</b>%s</li>' % x for x in NT_SUM))
    return ('<div class="aps-tips"><p class="aps-th">%s<small lang="en">（%s）</small><small>採点基準に基づく当サイトの解説。College Board公式の攻略法ではありません</small></p>'
            '<div class="tps">%s</div><p class="apt-ch">全問共通｜語彙・文法のコツ</p><div class="tps">%s</div>%s</div>' % (q, en, cards, new_tip_card(pid, 'c'), summ))
def panel_body(pid):
    if pid == 'q1':
        h = Q1
    elif pid == 'q2':
        h = Q2
    else:
        lead = '<p class="rlead">書く2問は、<b>内容・構成・語彙と文法</b>の3つの観点で採点されます。構成の点は、語彙や文法が限られていても、話が通じて組み立てられていれば取れます</p>'
        if pid == 'q3':
            h = ('<h4 class="apr-t" id="r-write">Q3 物語　<small>3つの観点・合計8点（スコア全体の7.5%）</small></h4>' + lead +
                 figure('q3', 'Question 3: Story Narration', 8, R.ROWS['q3'], 'Scoring Guidelines（Question 3）'))
        else:
            h = ('<h4 class="apr-t" id="r-email">Q4 メールへの返信　<small>3つの観点・合計8点（スコア全体の7.5%）</small></h4>' + lead +
                 figure('q4', 'Question 4: Email Response', 8, R.ROWS['q4'], 'Scoring Guidelines（Question 4）'))
    rows = R.ROWS[pid]
    for r in rows:
        h = h.replace('<div class="apc">', '<div class="apc" id="row-%s-%s">' % (pid, r[0]), 1)
    tot = sum(r[3] for r in rows)
    strip = ('<div class="apk"><p class="apk-h">%d点の内訳<small>押すと、その観点の基準に移動します</small></p><div class="apk-b">%s</div></div>'
             % (tot, ''.join('<a href="#row-%s-%s" style="flex:%d"><b>%d<small>点</small></b><span>%s</span></a>' % (pid, r[0], r[3], r[3], r[1]) for r in rows)))
    h = h.replace('<figure class="apr rise">', strip + '<figure class="apr rise">', 1)
    def kt(m):
        n = int(m.group(2)); t = tmap(pid, n, m.group(4))
        return '%shref="#tip-%s-%s" data-tip="%s-%s"%s%s<span class="kt-n">%s</span></a>' % (m.group(1), pid, t, pid, t, m.group(3), m.group(4), tlabel(t))
    h = re.sub(r'(<a class="kt" )href="#tip-(\d+)" data-tip="\d+"( aria-expanded="false">)(.*?)<span class="kt-n">TIP \d+</span></a>', kt, h)
    def pills(m):
        ts = []
        for n in re.findall(r'href="#tip-(\d+)"', m.group(0)):
            t = tmap(pid, int(n))
            if t not in ts: ts.append(t)
        return '<span class="apc-ts">%s</span>' % ''.join('<a class="apc-tip" href="#tip-%s-%s">%s</a>' % (pid, t, tlabel(t)) for t in ts)
    h = re.sub(r'<span class="apc-ts">.*?</span>', pills, h)
    return h + tips_block(pid)
def scoring_html():
    nav = ''.join('<button type="button" class="aps-b%s" data-p="%s" aria-controls="ap-%s" aria-selected="%s"><span class="aps-q">%s</span><span class="aps-n">%s<small>%d点</small></span>'
                  '<span class="aps-pc">%s</span><i class="aps-m" style="width:%.0f%%"></i></button>'
                  % (' on' if k == 0 else '', p[0], p[0], 'true' if k == 0 else 'false', p[1], p[2], p[4], p[3], float(p[3][:-1]) / 20 * 100)
                  for k, p in enumerate(PANELS))
    nav += '<button type="button" class="aps-b aps-def" data-p="def" aria-controls="ap-def" aria-selected="false"><span class="aps-q">用語</span><span class="aps-n">採点基準の用語<small>定義</small></span></button>'
    panels = ''.join('<section class="aps-p%s" id="ap-%s" aria-label="%s %s">%s</section>' % (' on' if k == 0 else '', p[0], p[1], p[2], panel_body(p[0])) for k, p in enumerate(PANELS))
    panels += ('<section class="aps-p" id="ap-def" aria-label="採点基準の用語"><h4 class="apr-t">採点基準の用語</h4>'
               '<p class="rlead">文化の理解と構成の観点では、次の言葉が決まった意味で使われます。採点基準の注（Additional Notes）にある定義です</p>%s</section>' % R.defs_html())
    return (step(5, 'scoring', '採点基準を読み解く', '記述・口述の4問（スコア全体の50%）の採点基準。2026年秋の改訂版') +
            '<p class="rlead">4問は、観点（Row）ごとに0〜3点または0〜2点で採点されます。<b>日本語以外で答えた回答は、その観点で0点</b>。'
            'プロジェクトの発表では、<b>盗用や、機械翻訳・生成AIで作ったとわかる内容も0点</b>です。College Boardの採点基準は、観点ごとに次の2つで書かれています</p>'
            '<dl class="apg rise"><div><dt>基準<small lang="en">Scoring Criteria</small></dt><dd>何点ならどんな回答か、という公式の定義</dd></div>'
            '<div><dt>典型的な回答<small lang="en">Decision Rules and Scoring Notes</small></dt><dd>採点官が点数を判断するときの目安。抽象的な基準を、実際の回答の姿に置き換えたもの</dd></div>'
            '</dl>'
            '<p class="rlead">このページでは、観点ごとに<b>満点の基準と、満点になる典型的な回答</b>を示し、それ未満の点数は折りたたんでいます。英語は原文のまま、和訳とハイライトは当サイトによるものです。問題（Q1〜Q4）を選ぶと、その採点基準とコツが表示されます</p>'
            '<div class="apsx rise"><div class="apsx-h"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg><b>採点基準データベース</b><span class="apsx-sw" role="group" aria-label="表示の切り替え"><button type="button" data-m="rub" aria-pressed="true">採点の内訳</button><button type="button" data-m="tips" aria-pressed="false">コツ</button></span></div><div class="aps"><nav class="aps-nav" aria-label="採点基準の問題"><p class="aps-h">記述・口述<b>50%%</b><small>選択式（リスニング・リーディング）50%%は採点基準なし</small></p>%s</nav>'
            '<div class="aps-ps">%s</div></div></div>' % (nav, panels))

APS_JS = r"""(function(){var au=document.querySelector('.au');if(au){au.classList.add('js');au.addEventListener('click',function(e){var b=e.target.closest('.aut');if(!b)return;var u=b.getAttribute('data-u');au.querySelectorAll('.aut').forEach(function(t){var on=t===b;t.classList.toggle('on',on);t.setAttribute('aria-expanded',on?'true':'false')});au.querySelectorAll('.aub').forEach(function(x){x.classList.toggle('on',x.getAttribute('data-u')===u)});place()});function place(){var b=au.querySelector('.aut.on'),x=au.querySelector('.aub.on');if(!b||!x)return;var r=au.getBoundingClientRect(),br=b.getBoundingClientRect();x.style.setProperty('--tx',(br.left-r.left+br.width/2)+'px')}place();window.addEventListener('resize',place)}})();
(function(){var w=document.querySelector('.aps');if(!w)return;w.classList.add('js');
function show(id,scroll){w.querySelectorAll('.aps-b').forEach(function(b){var on=b.getAttribute('data-p')===id;b.classList.toggle('on',on);b.setAttribute('aria-selected',on?'true':'false')});
w.querySelectorAll('.aps-p').forEach(function(p){p.classList.toggle('on',p.id==='ap-'+id)});
if(scroll){var t=w.getBoundingClientRect().top;if(t<150||t>window.innerHeight*.6)window.scrollTo({top:window.scrollY+t-170,behavior:'smooth'})}}
w.addEventListener('click',function(e){var b=e.target.closest('.aps-b');if(b){show(b.getAttribute('data-p'),true)}});
var X=w.closest('.apsx');function mode(m){if(!X)return;X.classList.toggle('m-tips',m==='tips');X.querySelectorAll('.apsx-sw button').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-m')===m?'true':'false')})}
if(X&&X.querySelector('.apsx-sw')){X.querySelector('.apsx-sw').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;mode(b.getAttribute('data-m'));var t=X.getBoundingClientRect().top;if(t<0)window.scrollTo({top:scrollY+t-150})})}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#tip-q"],a[href^="#r-"]');if(!a||a.classList.contains('kt'))return;var m=a.getAttribute('href').match(/#tip-(q\d)/);if(m){show(m[1],false);mode('tips')}},true);
})();"""

KP = [('2026-27年度から試験が全面改訂', '2027年5月11日（火）にBluebookで受験。試験時間は約1時間50分'),
      ('4技能を新形式で評価', '記述・口述50%、リスニング25%、リーディング25%。発表・質疑応答、物語・メール作成、日本語入力などの対策が必要'),
      ('6単元すべてが出題範囲', '読む・聞く・書く問題は全単元、話す問題（Q1・Q2）はその年のプロジェクトが対象'),
      ('プロジェクトは試験全体の35%', '2026-27年度のテーマは「芸術と創造性」。本番の発表（20%）と質疑応答（15%）を採点'),
      ('得点の鍵は採点基準の理解', '具体例・文化の背景・論理的な構成・日本語の運用力が重要。採点基準と「コツ」を照らし合わせて確認')]
SUM = [('units', '6つの単元と「問い」', '家族と地域社会から世界とのつながりまで、6つのテーマを、それぞれ3〜4つの「問い」を軸に学ぶ。授業はほぼすべて日本語'),
       ('exam', '試験の形式', '約1時間50分。記述・口述（Q1〜Q4）が50%、リスニング・リーディングの選択式が50%'),
       ('overview', '単元と試験の関係', '書く問題とリスニング・リーディングは6単元すべてから出題。話す問題（Q1・Q2）はその年のプロジェクトのテーマの単元から'),
       ('project', 'コースプロジェクト', '1月に課題配布、4月30日までに発表の骨子を提出、試験当日に3分の発表と4つの質問'),
       ('scoring', '採点基準を読み解く', '満点には、要因を調べた情報で説明し、文化の価値観と結びつけること。日本語以外の回答や生成AIの使用は0点'),
       ('camino', '家庭教師によるサポート', '学校の授業の理解から、記述・口述の対策、コースプロジェクトの発表練習まで、インター生・帰国子女を家庭教師がサポート')]
OTL_CSS = r"""<style id="apjp-otl">.otl-hd{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line,#d9deea)}
.otl .otl-hd p{border-bottom:0}
.otl-sw{font:inherit;font-size:12.5px;font-weight:700;color:var(--c,#16294d);background:#fff;border:1.5px solid var(--c,#16294d);border-radius:999px;padding:4px 14px;cursor:pointer;margin-bottom:8px}
.otl-sw:hover,.otl-sw[aria-pressed="true"]{background:var(--c,#16294d);color:#fff}
.otl-sw:focus-visible{outline:2px solid var(--c,#16294d);outline-offset:2px}
.otl-sum{display:none;list-style:none;margin:0;padding:6px 0 4px}
.otl.sum ol{display:none}.otl.sum .otl-sum{display:block}
.otl-sum li{padding:9px 0;border-top:1px solid #eef1f6}.otl-sum li:first-child{border-top:0}
.otl-sum a{display:flex!important;gap:10px;padding:0!important;font-size:14.5px!important;font-weight:700;color:var(--navy,#0b1f4b)!important}
.otl-sum a span{flex:none;font-family:var(--latin);color:var(--muted,#5c6984);font-weight:700}
.otl-sum p{margin:2px 0 0 0;padding:0 0 0 22px!important;border:0!important;font-size:13.5px!important;font-weight:400!important;letter-spacing:0!important;line-height:1.75;color:var(--ink,#1d2b45)!important}</style>
"""
OTL_JS = r"""(function(){var nav=document.querySelector('.aps-nav');function setTop(){if(nav&&innerWidth<=900){document.documentElement.style.setProperty('--apk-top',(136+nav.offsetHeight)+'px')}}setTop();addEventListener('resize',setTop);function spy(){document.querySelectorAll('.aps-p.on .apk-b').forEach(function(b){var as=[].slice.call(b.querySelectorAll('a')),y=b.getBoundingClientRect().bottom+60,k=-1;as.forEach(function(a,i){var t=document.getElementById(a.getAttribute('href').slice(1));if(t&&t.getBoundingClientRect().top<y)k=i});as.forEach(function(a,i){a.classList.toggle('cur',i==k)})})}addEventListener('scroll',spy,{passive:true});document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.apk-b a');if(!a){setTimeout(spy,50);return}var t=document.getElementById(a.getAttribute('href').slice(1));if(!t)return;e.preventDefault();var k=a.closest('.apk'),sb=parseFloat(getComputedStyle(k).top)+k.offsetHeight;window.scrollTo({top:t.getBoundingClientRect().top+scrollY-sb-12,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});a.parentNode.querySelectorAll('a').forEach(function(x){x.classList.toggle('cur',x===a)})});spy()})();
(function(){var o=document.querySelector('nav.otl'),b=o&&o.querySelector('.otl-sw');if(!b)return;b.addEventListener('click',function(){var on=!o.classList.contains('sum');o.classList.toggle('sum',on);b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'目次に戻る':'まとめ'})})();"""
def hero(s):
    sys.path.insert(0, os.path.join(HERE, '..', 'univreq'))
    import keypoints as KPM
    s = re.sub(r'<dl class="sj-facts">.*?</dl>', '', s, flags=re.S)
    s = re.sub(r'<!--kp-->.*?<!--/kp-->', '', s, flags=re.S)
    s = re.sub(r'<style id="(kp-css|apjp-otl)">.*?</style>\n', '', s, flags=re.S)
    t = re.sub(r'<section class="aps-p" .*?</section>', '', s, flags=re.S)
    t = re.sub(r'<p class="apx-en".*?</p>|<p class="tp-q".*?</p>', '', t, flags=re.S)
    mins = KPM.reading_minutes(t)
    m = re.search(r'<p class="lead">.*?</p>', s, flags=re.S)
    s = s[:m.end()] + ('<!--kp--><p class="rtime">%s読了目安：約%d分</p><div class="kp"><ul>%s</ul></div><!--/kp-->'
                       % (KPM.CLOCK, mins, ''.join('<li><b>%s：</b>%s</li>' % x for x in KP))) + s[m.end():]
    s = s.replace('</head>', KPM.CSS + '</head>', 1)
    summ = '<ul class="otl-sum">%s</ul>' % ''.join('<li><a href="#%s"><span>%d</span>%s</a><p>%s</p></li>' % (i, k, t, d) for k, (i, t, d) in enumerate(SUM, 1))
    s = re.sub(r'<nav[^>]*class="otl"[^>]*>.*?</nav>',
               lambda mm: re.sub(r'^(<nav class="otl" aria-label="目次">)(?:<div class="otl-hd">)?<p>目次</p>(?:<button[^>]*>[^<]*</button></div>)?(<ol>.*?</ol>)(?:<ul class="otl-sum">.*?</ul>)?',
                                 lambda x: x.group(1) + '<p>目次</p>' + x.group(2), mm.group(0), flags=re.S),
               s, count=1, flags=re.S)
    return s

TOCSUM = {
 'units': [('6つの単元', '家族・言語・芸術・科学技術・現代生活・世界とのつながりを学ぶ'),
           ('「問い」（Essential Questions）', '文化の背景や価値観を考えるための軸。問い自体がそのまま出題されるわけではない')],
 'exam': [('記述・口述50%', '発表（Q1）、質疑応答（Q2）、物語（Q3）、メールへの返信（Q4）'),
          ('選択式50%', 'リスニング25%、リーディング25%'),
          ('完全デジタル試験', 'Bluebookでスピーキングを録音し、ライティングは日本語入力。新形式での練習が必要')],
 'overview': [('6単元すべてが重要', 'ライティング・リスニング・リーディングは全単元から出題'),
              ('スピーキングはプロジェクトが対象', '2026-27年度は単元3「芸術と創造性」を重点的に準備')],
 'project': [('2027年1月から準備', '課題と資料が公開され、4月30日までに発表用の要点メモを提出'),
             ('本番の回答が採点対象', 'Q1は3分間の発表、Q2は4つの質問への回答。合計35%'),
             ('原稿の読み上げは避ける', '日本語の資料で調べ、キーワードを手がかりに自分の言葉で説明する')],
 'scoring': [('採点基準と「コツ」をセットで確認', '何が評価されるかを理解し、必要な能力と練習方法を把握する')],
}
TOC_CSS = r"""<style id="apjp-toc">.otl-note{margin:10px 0 0!important;padding:0!important;border:0!important;font-size:12.5px!important;font-weight:400!important;letter-spacing:0!important;color:var(--muted,#5c6984)!important;line-height:1.7}
.otl-note b{color:var(--navy,#0b1f4b)}
.otl li.otl-it{display:flex;flex-wrap:wrap;align-items:center;column-gap:10px;border-bottom:1px solid #f0f2f6}
.otl li.otl-it>a{flex:1 1 auto;min-width:0}
.otl-mb{flex:none;font:inherit;font-size:11.5px;font-weight:700;color:var(--c,#16294d);background:#fff;border:1.5px solid var(--c,#16294d);border-radius:999px;padding:2px 11px;cursor:pointer}
.otl-mb:hover,.otl-mb[aria-expanded="true"]{background:var(--c,#16294d);color:#fff}
.otl-mb:focus-visible{outline:2px solid var(--c,#16294d);outline-offset:2px}
.otl-mp{flex:1 1 100%;margin:0 0 10px 32px;padding:10px 14px;background:#f3f6fc;border-radius:10px}
.otl-mp[hidden]{display:none}
.otl-mp ul{margin:0;padding-left:1.1em}.otl-mp li{font-size:13.5px;line-height:1.75;color:var(--ink,#1d2b45);margin:2px 0}.otl-mp li b{color:var(--navy,#0b1f4b)}
.otl-side .otl-mb,.otl-side .otl-mp{display:none!important}
@media(max-width:700px){.otl-mp{margin-left:0}}</style>
"""
TOC_JS = r"""(function(){document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.otl-mb');if(!b)return;var p=document.getElementById(b.getAttribute('aria-controls'));var on=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',on?'true':'false');if(p)p.hidden=!on})})();"""
def toc_with_summaries(s):
    s = re.sub(r'<style id="apjp-toc">.*?</style>\n', '', s, flags=re.S)
    s = s.replace('</head>', TOC_CSS + '</head>', 1)
    def item(m):
        hid, num, label = m.group(1), m.group(2), m.group(3)
        if hid not in TOCSUM:
            return m.group(0)
        pts = ''.join('<li><b>%s：</b>%s</li>' % x for x in TOCSUM[hid])
        return ('<li class="otl-it"><a href="#%s"><span>%s</span>%s</a><button type="button" class="otl-mb" aria-expanded="false" aria-controls="otl-mp-%s">まとめ</button>'
                '<div class="otl-mp" id="otl-mp-%s" hidden><ul>%s</ul></div></li>' % (hid, num, label, hid, hid, pts))
    def nav(mm):
        x = mm.group(0)
        x = re.sub(r'<p class="otl-note">.*?</p>', '', x, flags=re.S)
        x = x.replace('<p>目次</p>', '<p>目次</p><p class="otl-note"><b>時間がない方へ</b>　目次の各項目にある「まとめ」ボタンから、そのセクションの重要ポイントを手短に確認できます</p>', 1)
        x = re.sub(r'<li(?: class="otl-it")?><a href="#([a-z]+)"><span>(\d)</span>([^<]*)</a>(?:<button.*?</div>)?</li>', item, x, flags=re.S)
        return x
    return re.sub(r'<nav[^>]*class="otl"[^>]*>.*?</nav>', nav, s, count=1, flags=re.S)

def build():
    s = open(F, encoding='utf-8').read()
    i = min(s.index('<div class="step" id="%s">' % k) for k in ('overview', 'units', 'exam') if ('<div class="step" id="%s">' % k) in s); j = s.index('<div class="step" id="camino">')
    w = s.rfind('<div class="ajs', 0, i)
    if w >= 0 and s.find('</div>', w, i) < 0:
        i = w
    parts = [units_html(), EXAM, overview_html(), PROJECT, scoring_html()]
    body = '\n'.join('<div class="ajs%s">%s</div>' % (' ajs-alt' if k % 2 else '', p) for k, p in enumerate(parts)) + '\n'
    _unused = '\n'.join([EXAM, units_html(), PROJECT, step(4, 'scoring', '採点基準を読み解く', '記述・口述の4問（スコア全体の50%）の採点基準。2026年秋の改訂版') .replace('id="scoring"><span class="step-n">4</span>', 'id="scoring"><span class="step-n">4</span>') + COMMON,
                      Q1.replace(step(4, 'r-present', '採点基準：Q1 プロジェクトの発表', '5つの観点、合計11点（スコア全体の20%）'), '<h4 class="apr-t" id="r-present">Q1 プロジェクトの発表　<small>5つの観点・合計11点（スコア全体の20%）</small></h4>'),
                      Q2.replace(step(5, 'r-qa', '採点基準：Q2 発表への質問', '4つの観点、合計9点（スコア全体の15%）'), '<h4 class="apr-t" id="r-qa">Q2 発表への質問　<small>4つの観点・合計9点（スコア全体の15%）</small></h4>'),
                      Q34,
                      tips_html().replace('<span class="step-n">7</span>', '<span class="step-n">5</span>')]) + '\n'
    s = s[:i] + body + s[j:]
    s = re.sub(r'(<div class="step" id="camino"><span class="step-n">)\d+', r'\g<1>6', s)
    toc = ('<li><a href="#units"><span>1</span>6つの単元と「問い」</a></li><li><a href="#exam"><span>2</span>試験の形式</a></li>'
           '<li><a href="#overview"><span>3</span>単元と試験の関係</a></li><li><a href="#project"><span>4</span>コースプロジェクト</a></li>'
           '<li><a href="#scoring"><span>5</span>採点基準を読み解く</a></li><li><a href="#camino"><span>6</span>家庭教師によるサポート</a></li>')
    s = re.sub(r'(<nav[^>]*class="otl"[^>]*><p>目次</p>(?:<p class="otl-note">.*?</p>)?<ol>).*?(</ol>)', lambda m: m.group(1) + toc + m.group(2), s, flags=re.S)
    s = re.sub(r'<style id="apjp-css">.*?</style>\n', '', s, flags=re.S)
    s = s.replace('</head>', css() + '</head>', 1)
    s = re.sub(r'<script id="apjp-js">.*?</script>\n', '', s, flags=re.S)
    s = s.replace('</body>', '<script id="apjp-js">' + open(os.path.join(HERE, 'kt.js'), encoding='utf-8').read() + APS_JS + TOC_JS + '</script>\n</body>', 1)
    s = s.replace('2027年5月の試験の形式、学ぶ内容、コースプロジェクト、採点基準を、改訂版のCourse and Exam Descriptionに沿って解説します。',
                  '6つの単元と「問い」、2027年5月の試験の形式、コースプロジェクト、記述・口述の採点基準を、改訂版のCourse and Exam Descriptionに沿って解説します。')
    s = s.replace('6つの単元と「問い」、2027年5月の試験の形式、', '6つの単元と「問い」、2027年5月の試験の形式と単元との関係、')
    s = hero(s)
    import apply_edits as AE
    s = AE.apply(s)
    s = toc_with_summaries(s)
    open(F, 'w', encoding='utf-8').write(s)
    print('ok')

if __name__ == '__main__':
    build()
