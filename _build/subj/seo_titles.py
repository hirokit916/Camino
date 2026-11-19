# -*- coding: utf-8 -*-
"""Idempotent: set search titles + meta descriptions (Hiroki's list, 2026-11-14), and enforce 「国際バカロレア（IB）」 in every Japanese title/description.
Run after any builder. usage: python3 seo_titles.py <site_root>"""
import os, sys, re, glob, html
ROOT = sys.argv[1]

# path: (ja_title, ja_desc, en_title, en_desc)   — en_* None when there is no English page
T = {
 # Career
 '/column/career/career-forum/': ('ボストンキャリアフォーラムとは？開催時期・参加企業・選考の流れ', 'ボストンキャリアフォーラムなど海外大生向け就職イベントの開催時期、参加企業、応募方法、選考の流れ。海外大生の日本就職に向けた実践ガイド', None, None),
 '/column/career/': ('海外大学生・インター卒業生の日本就職ガイド', '海外大学生・インター卒業生の日本就職。新卒採用の仕組み、応募ルート、選考対策、就活スケジュール。海外経験を活かしたキャリア形成', None, None),
 '/column/career/japan-hiring-system/': ('日本の新卒採用とは？海外との違い・就活時期・内定の仕組み', '日本独自の新卒採用制度。一括採用、就活スケジュール、内定・入社時期、海外の採用制度との違い', None, None),
 '/column/career/japan-tests/': ('SPI・玉手箱・GAB・TG-WEBとは？日本の就職適性検査ガイド', '日本の就職活動で使われる適性検査。SPI・玉手箱・GAB・TG-WEBの出題形式、特徴、対策方法', None, None),
 '/column/career/routes/': ('海外大学生が日本で就職する3つの方法｜応募ルートと選考対策', '海外大学生の日本就職に向けた3つの応募ルート。キャリアフォーラム、一般応募、インターン経由の採用方法と特徴', None, None),
 '/column/career/selection-steps/': ('日本の就職活動の流れ｜ES・Webテスト・面接・インターン', '日本の就職活動における選考フロー。エントリーシート、Webテスト、面接、インターンで評価されるポイント', None, None),
 '/column/career/timeline/': ('日本の就活はいつから？大学・学年別スケジュール', '日本の就職活動の開始時期と年間スケジュール。大学・学年別の準備、応募、選考のタイミング', None, None),
 # Curriculum & accreditation
 '/column/curriculum/accreditation/': ('インターナショナルスクールの認定とは？WASC・CISと大学進学資格', 'インターナショナルスクールの認定・認証制度。WASC・CISなどの認定機関、認定校の確認方法、大学進学資格との関係',
     'International School Accreditation: WASC, CIS and University Recognition', 'International school accreditation explained. WASC, CIS and other accrediting bodies, how to verify accreditation and implications for university admissions'),
 '/column/curriculum/': ('IB・IGCSE・A Level・APの違いは？カリキュラムと大学進学を比較', 'IB・IGCSE・A Level・APの違いを徹底比較。学習内容、評価方法、科目選択、大学進学への活用。お子さまに合う教育課程を考えるための比較ガイド',
     'IB vs IGCSE vs A Levels vs AP: Curriculum and University Pathways', 'IB vs IGCSE vs A Levels vs AP. Curriculum structures, assessment, subject choices and university pathways. A comparison guide for families choosing an educational pathway'),
 # University (After Graduation = destinations data; University Pathways = application routes)
 '/column/destinations/': ('インターナショナルスクール卒業後の進路｜国内外の大学進学先', '日本のインターナショナルスクール卒業生の進学先。国内外の大学、進学先の国・地域、学校別の公開データ',
     'Where Do International School Graduates Go to University?', 'University destinations of international school graduates in Japan. Domestic and overseas universities, popular study destinations and published school data'),
 '/column/university/after-graduation/': ('インターナショナルスクールから大学進学｜日本・海外の出願方法', 'インターナショナルスクール卒業後の大学進学。日本・海外の大学の出願方法、必要資格、入試制度、進学ルートの違い',
     'University Admissions After International School: Japan and Overseas', 'University pathways after international school. Applications to universities in Japan and overseas, qualifications, admissions systems and key differences'),
 '/column/university/ib-scores/': ('日本のインターナショナルスクールのIB平均点・合格率｜学校別比較', '日本のインターナショナルスクールのIB平均点・Diploma取得率。学校別の実績、公開データ、年度ごとの比較',
     'IB Scores at International Schools in Japan: School-by-School Comparison', 'Average IB scores and Diploma pass rates at international schools in Japan. School-by-school results and comparisons based on published data'),
 '/column/university/': ('インター生の大学受験ガイド｜IB・A Level・APと出願条件', 'インター生の大学受験に必要な情報。IB・A Level・APの違い、国内外の大学の出願条件、必要スコア、科目選択',
     'University Admissions for International School Students: IB, A Levels and AP', 'University admissions for international school students. IB, A Levels, AP, entry requirements, score expectations and subject choices'),
 '/column/university/without-ib-ap/': ('IB・A Level・APなしでも大学進学できる？出願資格と代替ルート', 'IB・A Level・APを履修していない生徒の大学進学。SAT・ACT、高校卒業資格、国内外の大学の出願条件と代替ルート', None, None),
 # English tests
 '/column/english/eiken/': ('英検とは？全8級のレベル・試験内容・CSEスコア・合格基準', '英検の全8級のレベルと難易度、試験内容、CSEスコア、合格基準、試験日程。小学生から大学生・社会人までの英語力評価',
     'EIKEN Explained: Levels, Test Format, CSE Scores and Passing Criteria', 'EIKEN test guide. Eight levels, difficulty, test format, CSE scores, passing criteria and test dates'),
 '/column/english/ielts/': ('IELTSとは？Academic・Generalの違いとバンドスコア', 'IELTSの試験内容とスコア制度。Academic・General Trainingの違い、バンドスコア、各セクションの評価、大学出願での活用',
     'IELTS Explained: Academic vs General Training and Band Scores', 'IELTS test guide. Academic vs General Training, band scores, test sections and university admissions'),
 '/column/english/toefl/': ('TOEFL iBTとは？2026年新形式・試験内容・スコア制度', 'TOEFL iBTの試験構成とスコア制度。2026年新形式、各セクションの内容、大学出願で求められる英語力',
     'TOEFL iBT Explained: 2026 Test Format, Sections and Scoring', 'TOEFL iBT test guide. 2026 test format, section details, scoring system and university admissions'),
 '/column/english/toeic/': ('TOEIC L&Rとは？試験内容・問題形式・スコアの仕組み', 'TOEIC Listening & Readingの試験構成、問題形式、スコア制度、試験日程。大学・就職活動での活用',
     'TOEIC Listening and Reading: Test Format and Scoring Explained', 'TOEIC Listening & Reading test guide. Test structure, question types, scoring system and test dates'),
 # Schools (directory + regions)
 '/column/schools/': ('日本のインターナショナルスクール27校を比較｜地域・カリキュラム・進学先', '日本全国のインターナショナルスクール27校を地域別に比較。IB・A Level・APなどのカリキュラム、学校の特徴、大学進学先をまとめた学校選びガイド',
     '27 International Schools in Japan: Locations, Curricula and University Pathways', '27 international schools across Japan. A school comparison guide covering locations, IB, A Levels, AP, school characteristics and university destinations'),
 '/column/schools/kansai/': ('関西のインターナショナルスクール6校を比較｜大阪・神戸・京都', '大阪・神戸・京都を中心とした関西のインターナショナルスクール6校。カリキュラム、学校の特色、入学情報、大学進学先の比較',
     '6 International Schools in Kansai: Osaka, Kobe and Kyoto', 'Six international schools in Kansai, including Osaka, Kobe and Kyoto. Curriculum, school characteristics, admissions information and university destinations'),
 '/column/schools/kanto/': ('関東のインターナショナルスクール16校を比較｜東京・神奈川', '東京・神奈川を中心とした関東のインターナショナルスクール16校。カリキュラム、学校の特色、入学情報、大学進学先の比較',
     '16 International Schools in Kanto: Tokyo and Kanagawa', 'Sixteen international schools in Kanto, including Tokyo and Kanagawa. Curriculum, school characteristics, admissions information and university destinations'),
 # IB, AP & Cambridge
 '/curriculum/ap/': ('APとは？科目一覧・試験スコア・大学の単位認定', 'AP（Advanced Placement）の科目一覧と試験制度。科目ごとのスコア、大学での単位認定、高校での履修から大学進学まで',
     'What Is the AP Program? Courses, Exam Scores and University Credit', 'AP (Advanced Placement) programme. Course list, exam scores, university credit policies and academic pathways'),
 '/curriculum/ap/university/': ('APで大学進学｜必要スコア・科目選択・単位認定', 'APスコアを活用した大学進学。大学別の必要スコア、科目選択、単位認定、出願時のスコア提出方法',
     'Applying to University with AP: Scores, Subject Choices and Credit', 'University admissions with AP. Score expectations, subject selection, university credit and score submission'),
 '/curriculum/cambridge/': ('Cambridgeカリキュラムとは？IGCSE・A Levelの違い', 'Cambridgeカリキュラムの全体像。IGCSEとA Levelの違い、科目構成、評価方法、大学進学への活用',
     'Cambridge Curriculum Explained: IGCSE vs A Levels', 'Cambridge curriculum overview. IGCSE vs A Levels, subject structure, assessment and university pathways'),
 '/curriculum/cambridge/university/': ('A Levelで大学進学｜必要な成績・科目・出願条件', 'A Levelを活用した大学進学。大学・学部別の成績要件、必要科目、出願条件',
     'University Admissions with A Levels: Grades and Entry Requirements', 'University admissions with A Levels. University and course-specific grade requirements, subject prerequisites and entry criteria'),
 '/ib/cp/': ('IBのCPとは？科目構成・学習内容・進路', 'IB Career-related Programme（CP）の仕組み。対象生徒、科目構成、キャリア関連学習、進学・就職への活用',
     'What Is the IB Career-related Programme (CP)? Structure and Pathways', 'IB Career-related Programme (CP). Student eligibility, programme structure, career-related learning and future pathways'),
 '/ib/dp/ee/': ('IBのEEとは？テーマ選び・論文の書き方・評価基準', 'IB Extended Essay（EE）の進め方。テーマ選び、リサーチ、論文構成、評価基準、2027年の変更点',
     'IB Extended Essay (EE): Topic Selection, Writing and Assessment', 'IB Extended Essay (EE). Topic selection, research, essay structure, assessment criteria and 2027 changes'),
 '/ib/dp/': ('IBのDPとは？6教科・HL/SL・TOK・EE・CAS・45点満点', 'IB Diploma Programme（DP）の全体像。6教科群、HL・SL、TOK・EE・CAS、45点満点の評価制度',
     'IB Diploma Programme (DP): Subjects, HL/SL, TOK, EE, CAS and 45 Points', 'IB Diploma Programme (DP). Six subject groups, HL and SL, TOK, EE, CAS and the 45-point scoring system'),
 '/ib/dp/tok/': ('IBのTOKとは？エッセイ・エキシビション・評価方法', 'IB Theory of Knowledge（TOK）の課題と評価。エッセイ、エキシビション、評価基準、学習内容',
     'IB Theory of Knowledge (TOK): Essay, Exhibition and Assessment', 'IB Theory of Knowledge (TOK). Essay, exhibition, assessment criteria and course requirements'),
 '/ib/': ('国際バカロレア（IB）とは？PYP・MYP・DP・CPの違い', '国際バカロレア（IB）の全体像。PYP・MYP・DP・CPの違い、対象年齢、学習内容、評価方法',
     'What Is the International Baccalaureate (IB)? PYP, MYP, DP and CP', 'International Baccalaureate (IB) overview. PYP, MYP, DP and CP, age groups, curriculum and assessment'),
 '/ib/myp/': ('IBのMYPとは？8つの教科群・評価方法・Personal Project', 'IB Middle Years Programme（MYP）の学習内容。8つの教科群、評価方法、Personal Project、学習の特徴',
     'IB Middle Years Programme (MYP): Subjects, Assessment and Personal Project', 'IB Middle Years Programme (MYP). Eight subject groups, assessment, Personal Project and learning approach'),
 '/ib/pyp/': ('IBのPYPとは？6つの探究テーマ・学習内容・評価方法', 'IB Primary Years Programme（PYP）の学習内容。6つの探究テーマ、教科横断型学習、評価方法',
     'IB Primary Years Programme (PYP): Inquiry Themes and Learning', 'IB Primary Years Programme (PYP). Six transdisciplinary themes, inquiry-based learning and assessment'),
 '/ib/university/': ('IBで大学進学｜必要スコア・大学別の出願条件', 'IB Diplomaを活用した大学進学。大学別の必要スコア、科目選択、国内外の出願条件',
     'University Admissions with the IB Diploma: Scores and Entry Requirements', 'University admissions with the IB Diploma. Score expectations, subject selection and entry requirements in Japan and overseas'),
}

# Individual schools: the doc's format, limited to what each page actually covers (no tuition/admissions on these pages)
SCHOOL_JA = {'asij': 'アメリカンスクール・イン・ジャパン（ASIJ）'}
SCHOOL_EN = {'canadian-academy': 'Canadian Academy Kobe', 'asij': 'The American School in Japan (ASIJ)'}

def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))

def school_entries():
    out = {}
    for p in sorted(glob.glob(ROOT + '/column/schools/*/index.html')):
        slug = p.split('/')[-2]
        if slug in ('kansai', 'kanto'): continue
        s = open(p).read()
        if 'http-equiv="refresh"' in s: continue
        main = s[s.index('<main'):s.index('</main>')]
        toc = re.findall(r'<li><a href="#[^"]+"><span>\d+</span>([^<]+)</a>', s)
        dest = '卒業生の進学先' in toc
        # names come from the H1 (English name + Japanese name span), never from the title, so reruns are stable
        h = re.search(r'<h1>(.*?)<span[^>]*>(.*?)</span></h1>', s)
        ja = SCHOOL_JA.get(slug, html.unescape(h.group(2)).strip())
        txt = re.sub(r'(\s*\|\s*)+', '|', strip(re.sub(r'<(script|style|svg).*?</\1>', '', main, flags=re.S).replace('<', '|<')))
        i = txt.find('この学校で学べるカリキュラム|カリキュラムを'); j = txt.find('公表している結果', i)
        seg = txt[i:j]
        cur_ja, cur_en = [], []
        for prog, lv in re.findall(r'\|(IB|AP|Cambridge)\|([^|]+)\|しくみを読む', seg):
            if prog == 'IB':
                cur_ja.append('IBの' + lv); cur_en.append('IB ' + lv.replace('・', ', '))
            elif prog == 'AP':
                cur_ja.append('AP' if lv == 'AP' else 'AP試験'); cur_en.append('AP' if lv == 'AP' else 'AP (exams only)')
            else:
                cur_ja.append('Cambridge ' + lv); cur_en.append('Cambridge ' + lv.replace('・', ', '))
        cj = '・'.join(cur_ja); ce = ', '.join(cur_en)
        if slug == 'canadian-academy':
            jt = 'カナディアン・アカデミーとは？神戸のカリキュラム・大学進学'
        else:
            jt = '%sとは？カリキュラム・%s' % (ja, '進学先' if dest else '学校の基本情報')
        jd = '%sの教育内容と学校情報。%s所在地・対象学年などの基本情報、学校が公表している結果%s' % (ja, (cj + '、') if cj else '', '、大学進学先' if dest else '')
        e = ROOT + '/en/column/schools/%s/index.html' % slug
        en_name = SCHOOL_EN.get(slug)
        if not en_name and os.path.exists(e):
            en_name = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', open(e).read()).group(1))).strip()
        et = '%s: Curriculum and %s' % (en_name, 'University Destinations' if dest else 'Key Facts')
        ed = '%s. %s%s and key facts' % (en_name, (ce + ', published results') if ce else 'Published results', ', university destinations' if dest else '')
        out['/column/schools/%s/' % slug] = (jt, jd, et, ed)
    return out

# ---------------------------------------------------------------- 国際バカロレア（IB） rule
WORD_IB = re.compile(r'(?<![A-Za-z])IB(?![A-Za-z])')
def ib_ja(s):
    if '国際バカロレア（IB）' in s:
        return s
    if 'IB（国際バカロレア）' in s:
        return s.replace('IB（国際バカロレア）', '国際バカロレア（IB）', 1)
    if '国際バカロレア' in s:
        return s.replace('国際バカロレア', '国際バカロレア（IB）', 1)
    m = WORD_IB.search(s)
    if not m:
        return s
    rest = s[m.end():]
    if rest.startswith(' ') and rest[1:2] and re.match(r'[A-Za-z]', rest[1:2]):
        # "IB DP" / "IB Diploma" / "IB Extended Essay" → 国際バカロレア（IB）DP …
        rest = rest[1:]
    return s[:m.start()] + '国際バカロレア（IB）' + rest

def tidy(s):
    # avoid nested brackets around the long name
    s = re.sub(r'([^\s（、。｜]+)（国際バカロレア（IB）([^（）]*)）', r'国際バカロレア（IB）\2の\1', s)
    s = re.sub(r'国際バカロレア（IB）（([^（）]*)）', r'国際バカロレア（IB）の\1', s)
    return s

def set_meta(s, title, desc):
    t = html.escape(title, quote=False); d = html.escape(desc, quote=True)
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % t, s, count=1, flags=re.S)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'(<meta %s content=")[^"]*(")' % attr, lambda m: m.group(1) + d + m.group(2), s)
        s = re.sub(r'(<meta content=")[^"]*(" %s)' % attr, lambda m: m.group(1) + d + m.group(2), s)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'(<meta %s content=")[^"]*(")' % attr, lambda m: m.group(1) + html.escape(title, quote=True) + m.group(2), s)
        s = re.sub(r'(<meta content=")[^"]*(" %s)' % attr, lambda m: m.group(1) + html.escape(title, quote=True) + m.group(2), s)
    return s

def get_meta(s):
    t = html.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1).strip())
    m = re.search(r'<meta name="description" content="([^"]*)"', s) or re.search(r'<meta content="([^"]*)" name="description"', s)
    return t, html.unescape(m.group(1)) if m else ''

if __name__ == '__main__':
    T.update(school_entries())
    changed = 0
    for p in sorted(glob.glob(ROOT + '/**/index.html', recursive=True)):
        rel = '/' + p[len(ROOT) + 1:-len('index.html')]
        if rel.startswith('/_preview'): continue
        s = open(p).read()
        if 'http-equiv="refresh"' in s: continue
        en = rel.startswith('/en/')
        key = rel[3:] if en else rel
        t0, d0 = get_meta(s)
        t, d = t0, d0
        if key in T:
            jt, jd, et, ed = T[key]
            if en:
                if et: t, d = et, ed
            else:
                t, d = jt, jd
        if not en:
            t, d = tidy(ib_ja(t)), tidy(ib_ja(d))
        if (t, d) != (t0, d0):
            if os.environ.get('DRY'):
                print(rel, '\n  T:', t, '\n  D:', d)
            else:
                open(p, 'w').write(set_meta(s, t, d))
            changed += 1
    print('meta updated on', changed, 'pages')
