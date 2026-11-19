# -*- coding: utf-8 -*-
"""Reading time + key points at the top of every column article (not school profiles, area pages or hubs).
Idempotent (<!--kp-->...<!--/kp-->). Run AFTER any page generator.
Usage: python3 keypoints.py /home/claude/camino-v2"""
import os, re, sys, math, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = sys.argv[1]
import build_split as B
SS, A, AN = B.SS, B.A, B.AN

KP = {
 'career/career-forum': [
  '日英バイリンガルを対象にした採用イベント。事前に応募した企業の面接を会場で受け、その場で内定が出ることもある',
  'ボストン（11月）、ロンドン（2月）、東京（6月）などで開かれ、コンサル・金融から商社、官公庁、メーカーまで参加する',
  '多くの選考はフォーラムの数週間〜数か月前に始まる。締切は企業ごとに違い、当日の「ウォークイン」もある'],
 'career/japan-hiring-system': [
  '日本の新卒採用は、政府が企業に日程を要請している。広報は3月、選考は6月、正式な内定は10月1日以降',
  '卒業後3年以内は新卒枠で応募できるよう、国が企業に求めている。海外大生向けの選考を設ける企業もある',
  '大卒の約3割は3年以内に最初の会社を離れる。入社後に配属が決まる「総合職」が多いが、配属を約束するコースも出てきた'],
 'career/japan-tests': [
  '日本の企業や外資系の日本オフィスでは、面接の前に適性検査（Webテストなど）を受けるのが一般的',
  '主な検査はSPI３、玉手箱、GAB、TG-WEB。問われるのは言語・計数・論理・英語・性格の5つ',
  'インター出身でも免除されることは少ない。準備に最も時間がかかるのは、日本語の語彙と読解'],
 'career/japanese-vs-foreign': [
  '日系企業は卒業前年度の3月ごろから本選考が始まる例が多く、外資系は卒業前年の夏〜秋に締切が来る例が多い',
  'テストは、日系はSPI３などのテストセンター、外資系は企業独自のオンラインアセスメントを使う例がある',
  'コンサルの面接はケース面接が中心。外資系でも、日本オフィスの選考は日本語で行う例がある'],
 'career/routes': [
  '海外大生・インター出身者の就職ルートは、日本の就活と同じ流れ、キャリアフォーラム、インターンからの特別選考の3つ',
  '3つは並行して進められる。キャリアフォーラムなら、多くの企業の選考を数日間にまとめて受けられる',
  'どのルートでも、日英のレジュメ、Webテスト、日英の面接が求められることが多い'],
 'career/selection-steps': [
  '選考は、接点づくり・応募書類・テスト・面接・インターン・内定の6つのフェーズに分けられる',
  'テストは適性検査のほか、企業独自のオンラインアセスメントや録画面接・AI面接も使われている',
  '外資系でも、日本オフィスの面接は日本語の例がある。同じ経験を日英どちらでも話せる準備が必要'],
 'career/timeline': [
  '2028年卒の場合、国内の日程は広報が2027年3月、選考が6月、正式な内定が10月1日以降',
  '海外大生向けの選考は、卒業の1年半以上前に締切が来る例がある（外資系の本選考やサマーインターン）',
  '卒業前年の10月1日時点で7割以上が内定を得ている。4月入社が中心だが、秋入社を選べる企業もある'],
 'curriculum/accreditation': [
  'WASC・CISなどの「認定」は、学校全体を外部の団体が評価するしくみ',
  '文部科学省が挙げる6団体の認定校で12年の課程を修了すると、日本の大学入学資格が認められる',
  '「加盟（Member）」や「候補（Candidate）」は認定とは別。IB World Schoolなどの「認定」とも意味が違う'],
 'curriculum': [
  'インターの代表的なカリキュラムは、IB（国際バカロレア）・Cambridge（英国式）・AP（米国式）の3つ',
  'IBは4つのプログラムで学び、高校段階のDPは45点満点のディプロマ。CambridgeのIGCSE・A Levelは科目ごとの資格',
  'APは大学レベルの科目を高校で学び、5月の試験で1〜5のスコアが出る。学年を選ぶと、その時期に学ぶ内容がわかる'],
 'destinations': [
  'インター卒業生の進学先の国・地域は、学校によって傾向が分かれる',
  '米国式のカリキュラムの学校は米国、英国式の学校は英国への進学が目立ち、IB校は複数の地域に広がる傾向がある',
  'ある国の割合が低くても、その国に弱いという意味ではない。進学先が分散していれば、一国の割合は自然と小さくなる'],
 'ee-tips': [
  'EEの科目は「HL・進路・興味」の3つの視点で選ぶ',
  'リサーチクエスチョンは、4,000語で答えきれる範囲まで絞り、答えを出せる「問い」の形で立てる',
  '2027年からの新しい評価基準から逆算し、問いから結論まで一本の筋を通す'],
 'tok-tips': [
  'TOKの成績は、エッセイが3分の2、エキシビションが3分の1',
  'エッセイは、タイトルを自分の言葉で言い換えられるものを選び、主張と反論をセットで書く',
  'エキシビションは、実在する特定のオブジェクトを3つ選び、1つの問いに結びつける'],
 'english/eiken': [
  '英検は5級〜1級の8つの級。3級以上は一次試験（筆記）と二次試験（面接）の2段階',
  '合否は技能ごとの英検CSEスコアで判定され、4技能の合計でCEFRのどのレベルかもわかる',
  '2024年度から英作文が2題に、2025年度から準2級プラスが新設された'],
 'english/ielts': [
  'IELTSは、大学などで学ぶためのAcademicと、移住や仕事のためのGeneral Trainingの2種類',
  '結果は0〜9のバンドスコア。全体のバンドは4セクションの平均を0.5単位に丸めたもの',
  '海外の主要大学の最低ラインは6.5前後が多く、イギリスやアメリカの上位校では7.0以上が目安になる'],
 'english': [
  '代表的な英語の資格は、英検・TOEFL iBT・IELTS・TOEICの4つ。運営団体も、測る技能も、結果の出方も違う',
  '海外の大学ならTOEFL iBTかIELTS Academic、国内の入試・単位認定なら英検、ビジネスならTOEICが中心',
  '出願の締切から、試験日・結果が出るまでの期間・スコアの有効期限を逆算して選ぶ'],
 'english/toefl': [
  'TOEFL iBTは2026年1月から新しい形式になり、スコアは0〜120から1〜6（0.5刻み）に変わった',
  'リーディングとリスニングは、途中で難易度が変わる多段階適応型。結果は3日後にわかる',
  'アメリカの上位30校では、新TOEFL 5.0（旧スコア100）前後が出願の目安'],
 'english/toefl/rubric': [
  'TOEFL iBTのライティングとスピーキングは、採点基準（ルーブリック）に照らして採点される',
  '満点の5点の基準には、「何ができていれば満点か」がそのまま書かれている',
  '公式の5点の基準を原文と和訳で読み、基準の言葉から15のコツを読み取る'],
 'english/toeic': [
  'TOEIC L&Rは、リスニングとリーディングの2技能を測るテスト。合否はなく、10〜990点のスコアで示される',
  '問題はすべて英語のマークシート方式で、約2時間・200問',
  '2024年度の公開テストの平均は615点。スピーキングとライティングは別のテストで測る'],
 'university/after-graduation': [
  'インター卒業後の進路は、海外の大学にも日本の大学にも開かれている',
  'IBは「ディプロマの取得と合計点」、A Levelは「3科目の成績」、APは「単位や上級クラスへの配置」が主な使われ方',
  '日本の大学に出願するには、文部科学省が定める大学入学資格が必要。IBやA Level、認定校の卒業などで満たせる'],
 'university/without-ib-ap': [
  'IB・A Level・APがなくても、高校の卒業資格と成績があれば大学には出願できる',
  'そのかわり、SAT・ACTなどの統一テストと、英語力の証明を求められることが多い',
  '必要なものは国によって違う。アメリカならSAT・ACT、イギリスならAPやFoundation、カナダなら英語試験が鍵になる'],
 'university/ap-results': [
  'APのスコアは1〜5。多くの大学は、3以上を単位認定や上級クラスへの配置の目安にしている',
  'APの結果を公表している国内のインターは限られる。公表されている結果を、出典とともに掲載',
  '学校の結果は学校全体の数字で、大学の条件と比べるのは自分のスコア'],
 'university/ib-scores': [
  'IBディプロマの世界平均は30.88点（2026年）',
  '掲載校が公表している平均点は31.4〜42.7点。順位づけはしていない',
  '大学の数字は合格に必要な最低ラインで、比べるのは自分の予想点（Predicted Grades）'],
 'university/a-level-results': [
  'A Levelの成績はA*〜Eの6段階。イングランドなどのA Level全体では、A*〜Aの割合は28.5%（2026年）',
  '掲載校が公表しているA*〜Aの割合は40〜68%。順位づけはしていない',
  'イギリスの上位10校が3科目で求めるのはAAB〜A*A*A（最低ライン）'],
 'university/sat-english-tests': [
  'SAT・ACTを必須にする大学は、アメリカの上位10校で64%、51〜100位で12%。2029年には上位22校のうち15校が必須になる',
  '英語試験の基準は順位で分かれる。TOEFL（0〜120）の中央値は、上位30校で100、51〜100位で80',
  'オーストラリア・カナダ・シンガポールの主要大学はIELTS 6.5が共通の基準。インター生の免除の扱いは大学ごとに違う'],
  '_db_unused': [
  'アメリカ108校・イギリス100校の、SAT・ACT、英語試験、IB・A Levelの入学要件を大学ごとに掲載',
  'イギリスの大学は学部ごとに要件が違うため、代表例として経済学部の基準を載せている',
  '要件は毎年見直される。出願前には、必ず各大学の公式サイトで最新の情報を確認する'],
}

def ib_scores_kp():
    uk = [v for v, n in (B.uni_med('ib', 'UK', k) for k in SS.UNIS if SS.RANK[k] <= 10) if v and n >= 3]
    au = [v for v, n in (B.uni_med('ib', 'AU', k) for k, _ in A.UNI['AU']) if v and n >= 3]
    return ['イギリスの上位10校が求める総合点は、大学ごとの中央値で%s〜%s点。オーストラリアの上位5校は%s〜%s点' % (AN.fmt(min(uk)), AN.fmt(max(uk)), AN.fmt(min(au)), AN.fmt(max(au))),
            '国による差は学部で違う。医学はオーストラリア（%s点）がイギリスの上位10校（%s点）を上回る' % (AN.fmt(B.acs_ib_med('MED', 'AU')[0]), AN.fmt(B.band_med('MED', 1, 10, B.ib_uk)[0])),
            'ここでの点数は合格に必要な最低ライン。アメリカの大学は学部ごとの点数基準を公表していない']

def al_scores_kp():
    u10 = [x for x in (B.band_med(m, 1, 10, B.tar)[0] for m, _ in B.MAJ) if x]
    u3 = [x for x in (B.band_med(m, 31, 50, B.tar)[0] for m, _ in B.MAJ) if x]
    return ['イギリスの上位10校が求める成績は、学部ごとの中央値で%s〜%s。31〜50位では%s〜%s' % (B.gname(min(u10)), B.gname(max(u10)), B.gname(min(u3)), B.gname(max(u3))),
            '数学・物理学・機械工学ではほぼ全校が数学を必須にし、法学・経営学は科目の指定がない大学が大半',
            'カナダのマギル大学は%s、オーストラリアのニューサウスウェールズ大学は%s（12学部の中央値）' % (B.gname(B.uni_med('al', 'CA', 'McGill')[0]), B.gname(B.uni_med('al', 'AU', 'UNSW')[0]))]

def major_kp(m, ja):
    a10 = B.band_med(m, 1, 10, B.tar)[0]; i10 = B.band_med(m, 1, 10, B.ib_uk)[0]
    au = B.acs_ib_med(m, 'AU')[0]
    k1 = 'イギリスの上位10校では、A Level %s・IB %s点が中心（中央値）' % (B.gname(a10), AN.fmt(i10)) if a10 and i10 else None
    if au: k1 = (k1 + '。オーストラリアの主要大学はIB %s点' % AN.fmt(au)) if k1 else 'オーストラリアの主要大学はIB %s点が中心（中央値）' % AN.fmt(au)
    rows = B.uk_rows(m)
    if m == 'ECON':
        al = [r for k, r in rows if r.get('al')]
        c = sum(1 for r in al if '数学' in r['al']); k2 = 'A Levelで数学を条件に含める大学は%d%%（%d校中%d校）' % (B.pct(c, len(al)), len(al), c)
    else:
        cnt = B.req_counts([r.get('req') for k, r in rows])
        name = dict(B.REQ_COLS)
        hard = [(c, n, key) for key, (c, n) in cnt.items() if key not in ('NONE', 'OPT') and n and c / n >= .5]
        best = max(hard, key=lambda x: x[0]) if hard else max(((c, n, key) for key, (c, n) in cnt.items()), key=lambda x: x[0])
        if best[2] == 'NONE': k2 = 'A Levelで必須科目を指定しない大学が%d%%（%d校中%d校）' % (B.pct(best[0], best[1]), best[1], best[0])
        elif best[2] == 'OPT': k2 = 'A Levelでは、%d%%の大学が「理系から1科目」のような選べる条件を課す（%d校中%d校）' % (B.pct(best[0], best[1]), best[1], best[0])
        else: k2 = 'A Levelで%sを必須にする大学は%d%%（%d校中%d校）' % (name[best[2]], B.pct(best[0], best[1]), best[1], best[0])
    T = {}
    for k, r in rows:
        t = r.get('test') or ''
        if t and not t.startswith('なし') and '条件が変わる' not in t:
            for w in B.SJ.test_tokens(t): T.setdefault(w, set()).add(k)
    k3 = ('入学試験は、%s' % '、'.join('%s（%d校）' % (w, len(ks)) for w, ks in sorted(T.items(), key=lambda x: -len(x[1])))) if T else 'イギリス上位50校で、出願者全員に入学試験を課す大学は確認できなかった'
    if m in ('MED', 'LAW'): k3 += '。アメリカとカナダでは、主に大学卒業後の専門課程で学ぶ'
    return [x for x in (k1, k2, k3) if x]

def reading_minutes(s):
    m = s[s.find('<h1'):]
    for stop in ['id="faq"', '<h2>出典', 'id="next"', '<footer']:
        i = m.find(stop)
        if i > 0: m = m[:i]; break
    m = re.sub(r'<!--kp-->.*?<!--/kp-->', '', m, flags=re.S)
    tables = len(re.findall(r'<table|<figure', m))
    m = re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<table.*?</table>|<details.*?</details>|<svg.*?</svg>', '', m, flags=re.S)
    n = len(re.sub(r'\s', '', re.sub('<[^>]+>', '', m)))
    return max(2, math.ceil(n / 500 + 0.5 * tables))

CSS = ('<style id="kp-css">.rtime{font-size:12.5px;color:var(--muted,#5c6984);margin:10px 0 0;display:flex;align-items:center;gap:6px}'
       '.rtime svg{width:14px;height:14px}'
       '.kp{margin:16px 0 0;background:#fff;border:1px solid var(--line,#d9deea);border-left:4px solid var(--c,#16294d);border-radius:0 12px 12px 0;padding:14px 18px 14px 16px;max-width:760px}'
       '.kp ul{margin:0;padding:0;list-style:none}.kp li{position:relative;padding-left:16px;font-size:14.5px;line-height:1.8;color:var(--navy,#0b1f4b)}'
       '.kp li+li{margin-top:6px}.kp li::before{content:"";position:absolute;left:0;top:.72em;width:6px;height:6px;border-radius:50%;background:var(--c,#16294d)}'
       '@media(max-width:760px){.kp li{font-size:14px}}</style>\n')
CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'

def inject(rel, pts):
    f = os.path.join(ROOT, 'column', rel, 'index.html') if rel else os.path.join(ROOT, 'column', 'index.html')
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!--kp-->.*?<!--/kp-->', '', s, flags=re.S)
    s = re.sub(r'<style id="kp-css">.*?</style>\n', '', s, flags=re.S)
    mins = reading_minutes(s)
    m = re.search(r'<p class="lead">.*?</p>', s, flags=re.S)
    html = ('<!--kp--><p class="rtime">%s約%d分で読めます</p><div class="kp"><ul>%s</ul></div><!--/kp-->'
            % (CLOCK, mins, ''.join('<li>%s</li>' % p for p in pts)))
    s = s[:m.end()] + html + s[m.end():]
    s = s.replace('</head>', CSS + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    return mins

if __name__ == '__main__':
    pages = dict(KP)
    pages['university/ib-scores-by-major'] = ib_scores_kp()
    pages['university/a-level-scores-by-major'] = al_scores_kp()
    for m, ja in B.MAJ: pages['university/majors/' + B.SLUG[m]] = major_kp(m, ja)
    pages.pop('_db_unused', None)
    for rel, pts in pages.items():
        print(inject(rel, pts), rel)
