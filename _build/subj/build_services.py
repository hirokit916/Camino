# -*- coding: utf-8 -*-
"""Service pages (/services/...) and legal pages (/about/, /privacy/). usage: python3 build_services.py <site_root>"""
import sys as _sys
if '--force' not in _sys.argv:
    _sys.exit('This script regenerates pages from scratch and would overwrite later edits made directly in the HTML.\n'
              'Only use it to create brand-new pages, then run: python3 _build/run.py\n'
              'To run anyway: python3 %s <site root> --force' % __file__)
_sys.argv = [a for a in _sys.argv if a != '--force']

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from data_cambridge import IGCSE, ALEVEL
from data_ib import DP
from data_ap import AP
from data_mid import MID
URLS = []

def price_tbl(rows):
    return C.table(['プラン', '料金（税込）', '内容'], rows)

TRIAL = ('<ol class="sv-flow rise"><li><b>ヒアリング（10分）</b><span>保護者・生徒</span>現在の学習状況や学校の課題、ご要望を伺います</li>'
         '<li><b>体験授業（40分）</b><span>生徒</span>実際の授業を、宿題や苦手な単元を使って体験していただきます</li>'
         '<li><b>ご提案（10分）</b><span>保護者・生徒</span>今後の学習方針と指導内容をご提案します</li></ol>'
         '<p class="muted">初回60分は無料です（対面の場合は交通費のみご負担いただきます）。現在、平日は満員のため、無料体験は土日でご案内しています</p>')

POLICY = ('<ul class="sj-top two rise"><li><b>お支払い</b>：毎月末に、その月分の請求書をLINEまたはメールでお送りします。翌月10日までに銀行振込でお支払いください（振込手数料はご負担ください）</li>'
          '<li><b>振替</b>：24時間前までにご連絡いただいた場合、振替レッスンを行います。お休みされたレッスンから2ヶ月以内にご予約ください</li>'
          '<li><b>キャンセル</b>：やむを得ない理由（病気・けが・災害など）を除き、1週間前までにご連絡ください。3週間以上の長期のお休みは1ヶ月前までにご連絡ください</li>'
          '<li><b>入会金・解約金</b>：入会金・解約金・月額利用料はいただいておりません。対面授業の交通費と教材費は別途ご負担いただきます</li></ul>')

TUTOR_PRICE = price_tbl([('小学生（G1〜G5）', '¥10,000 / 60分', '国語・算数・理科・社会・英語など'), ('中学生（G6〜G8）', '¥12,000 / 60分', 'MYP・Lower Secondaryなど'),
                         ('高校生（G9〜G12）', '¥15,000 / 60分', 'IGCSE・MYP 4〜5年など'), ('高校生（IB DP・AP・Cambridge A Level）', '¥18,000 / 60分', '科目と指導内容に応じてご相談ください')])
LONG = '<p class="muted">90分・120分など、60分を超える授業も同じ時間単価でご利用いただけます</p>'
ONLINE = '神戸・芦屋・西宮・大阪は対面、それ以外の地域や海外からはオンラインで受講いただけます'

def sublinks(cards):
    return grid(cards)

def svc(slug, title, desc, h1, small, lead, sections, faq, nxt, cta, toc_items, service_name, extra_ld=None):
    path = '/services/%s/' % slug if slug else '/services/'
    body = ''
    for n, (id_, h, sub, html) in enumerate(sections):
        body += C.step(n + 1, id_, h, sub) + html
    ld = [{'@type': 'Service', 'name': service_name, 'serviceType': service_name, 'provider': {'@id': BASE + '/#organization'},
           'areaServed': ['神戸市', '芦屋市', '西宮市', '大阪市', 'オンライン'], 'url': BASE + path, 'inLanguage': 'ja'}]
    crumbs = [('サービス', '/services/')] + ([(h1 if len(h1) < 20 else service_name, path)] if slug else [])
    if not slug:
        crumbs = [('サービス', '/services/')]
    URLS.append(page(path, title, desc, h1, small, lead, body, crumbs, faq=faq, nxt=nxt, cta=cta,
                     nav=subnav('サービス', SVC_NAV, path), kind='svc', toc_items=toc_items, extra_ld=ld + (extra_ld or [])))

def cards_ib():
    return [('/subjects/ib/%s/' % d['slug'], None, 'IB %s' % d['ja'], d['en']) for d in DP]
def cards_cam():
    return [('/subjects/igcse/%s/' % d['slug'], d['code'].split('（')[0], 'IGCSE %s' % d['ja'], d['en']) for d in IGCSE] + \
           [('/subjects/a-level/%s/' % d['slug'], d['code'], 'A Level %s' % d['ja'], d['en']) for d in ALEVEL]
def cards_ap():
    return [('/subjects/ap/%s/' % d['slug'], None, 'AP %s' % d['ja'], d['en']) for d in AP]
def cards_mid():
    return [('/subjects/%s/%s/' % ('myp' if d['group'] == 'myp' else 'lower-secondary', d['slug']), None, ('MYP ' if d['group'] == 'myp' else 'Lower Secondary ') + d['ja'], d['en']) for d in MID]

CTA_T = ('まずは無料体験レッスンから', '初回60分は無料です。お子さんの学習状況やご要望を伺ったうえで、実際の授業を体験していただきます')
CTA_C = ('まずは無料電話相談から', '15分の無料電話相談で、お子さんの学習状況や進路についてのお悩みを伺います')

def build():
    # ---------------------------------------------------- international-school tutoring
    svc('international-school', 'インター生・帰国子女の家庭教師｜宿題・課題・試験対策｜神戸・大阪・オンライン｜Camino',
        'インターナショナルスクールに通うお子さん・帰国子女のための家庭教師。インター卒業生の講師が、学校の授業の理解、宿題・課題、定期試験の対策まで、日本語と英語を切り替えながらマンツーマンで指導します。神戸・芦屋・西宮・大阪は対面、全国・海外はオンライン。初回60分無料',
        'インター生・帰国子女の家庭教師', 'サービス',
        'インターナショナルスクールの授業・課題・定期試験から、日々の学習習慣づくりまで、幅広い科目に対応する個別指導です。講師は、インターナショナルスクールでIBディプロマを取得したインター卒業生で、<b>日本語と英語を、お子さんの理解度に合わせて切り替えながら</b>授業を行います',
        [('for', 'こんなご家庭に', '',
          '<ul class="sj-top one rise"><li>英語の授業についていけているか、家庭では確認しにくい</li><li>宿題・課題（エッセイ・プロジェクト）の進め方がわからない</li><li>定期試験や、IB・IGCSE・APの試験に向けて対策したい</li><li>帰国後、インターの授業や英語での学習に慣れるまでサポートがほしい</li><li>勉強の習慣を身につけさせたい</li><li>進路や科目選びについても相談できる先生がほしい</li></ul>'),
         ('what', '授業の内容', '一人ひとりに合わせて、科目・進め方・予定を決めます',
          '<ul class="sj-top one rise"><li><b>学校の授業の理解</b>：わからなかった単元を、日本語と英語で解説します</li><li><b>宿題・課題のサポート</b>：答えを教えるのではなく、自分で進められるように考え方を一緒に整理します</li><li><b>試験対策</b>：定期試験、IB・IGCSE・A Level・AP、Checkpointなどの過去問演習</li><li><b>学習習慣づくり</b>：家庭学習の計画づくりと振り返り</li><li><b>授業の報告</b>：授業ごとの内容と、今後の方針を保護者の方に共有します</li></ul>'),
         ('subjects', '対応科目', '国語・算数・数学・理科・社会・英語など、幅広い科目に対応します。カリキュラム別の科目ガイドもご覧ください', sublinks(
             [('/subjects/middle-school/', '中学', 'MYP・Lower Secondary', '理科・数学・英語'), ('/subjects/igcse/', 'G9〜G10', 'IGCSE', '14科目のシラバスと試験構成'),
              ('/subjects/ib/', 'G11〜G12', 'IB DP', '18科目の試験構成とIA'), ('/subjects/a-level/', 'G11〜G12', 'A Level', '13科目のシラバスと試験構成'), ('/subjects/ap/', 'G10〜G12', 'AP', '18科目の2027年の試験形式')])),
         ('price', '料金', '全プラン税込・授業料のみです', TUTOR_PRICE + LONG),
         ('trial', '無料体験レッスンの流れ', '', TRIAL),
         ('policy', 'お支払い・振替・キャンセル', '', POLICY)],
        [('授業は対面とオンラインのどちらですか？', ONLINE + '。対面の場合は、交通費を別途いただきます'),
         ('授業は日本語ですか、英語ですか？', 'お子さんの理解度やご希望に合わせて、日本語と英語を切り替えながら授業を行います'),
         ('どの学年から受けられますか？', '小学1年生（G1）から高校3年生（G12）まで対応しています。英検・TOEFL・IELTSなどの資格対策は、大人の方も受講いただけます'),
         ('授業の頻度や時間は決められますか？', 'はい。週1回・週2回などの頻度や、60分・90分・120分などの時間は、ご家庭のご希望に合わせて決めます')],
        [('/services/', 'Caminoのサービス一覧', '家庭教師・保護者の相談・資格対策', True), ('/subjects/', '科目別ガイド', 'IB・IGCSE・A Level・APの全科目', False), ('/area/kobe/', '神戸の家庭教師', '対面授業の対応エリア', False)],
        CTA_T, [('for', 'こんなご家庭に'), ('what', '授業の内容'), ('subjects', '対応科目'), ('price', '料金'), ('trial', '無料体験'), ('policy', 'お支払い・振替')],
        'インター生・帰国子女の家庭教師')

    # ---------------------------------------------------- IB
    svc('ib', 'IBの家庭教師｜DP・MYP・PYP、IA・EE・TOKまで｜神戸・大阪・オンライン｜Camino',
        '国際バカロレア（IB）のDP・MYP・PYPの家庭教師。IBディプロマを取得したインター卒業生の講師が、各科目の授業の理解と試験対策、IA・EE・TOKの進め方まで、日英バイリンガルでサポートします。神戸・芦屋・西宮・大阪は対面、オンラインにも対応。初回60分無料',
        'IB（国際バカロレア）の家庭教師', 'サービス',
        '講師は、インターナショナルスクールで<b>IBディプロマを取得した</b>インター卒業生です。DPの各科目の授業と試験対策に加えて、IA・EE・TOKなど、IB特有の課題の進め方もサポートします。MYP・PYPの授業にも対応します',
        [('what', 'IBの家庭教師でできること', '',
          '<ul class="sj-top one rise"><li><b>DPの各科目</b>：授業内容の理解、過去問演習、評価規準にもとづく答案の見直し</li><li><b>IA（内部評価）</b>：テーマ選び、研究課題の絞り込み、レポートの構成</li><li><b>EE（課題論文）</b>：研究課題の設定から、振り返り（RPPF）まで。<a href="/column/ee-tips/">EEのコツ</a></li><li><b>TOK</b>：エキシビションとエッセイの考え方。<a href="/column/tok-tips/">TOKのコツ</a></li><li><b>MYP</b>：評価規準（A〜D）を意識した課題の仕上げ方、eAssessment対策</li><li><b>PYP</b>：英語での学習の土台づくり、探究の学習のサポート</li></ul>'),
         ('subjects', 'IB DPの科目別ガイド', '各科目のSL・HLの試験構成と、学ぶ内容をまとめています', sublinks(cards_ib())),
         ('price', '料金', '全プラン税込・授業料のみです', TUTOR_PRICE + LONG),
         ('trial', '無料体験レッスンの流れ', '', TRIAL)],
        [('IBの家庭教師は、オンラインでも受けられますか？', 'はい。' + ONLINE),
         ('IA・EEを代わりに書いてもらえますか？', 'いいえ。IBの規則に反するため、代筆や答えの提供は行いません。テーマの考え方、構成、書き方の改善点を一緒に整理し、お子さんが自分で書き進められるようにサポートします'),
         ('IB DPの授業の料金はいくらですか？', 'IB DPの授業は60分¥18,000です（税込・授業料のみ）。MYPは中学生（G6〜G8）60分¥12,000、G9〜G10は60分¥15,000です')],
        [('/subjects/ib/', 'IB DPの科目別ガイド', '18科目の試験構成とIA', True), ('/ib/dp/', 'IBのDPとは？', '科目・HL/SL・TOK・EE・CAS', False), ('/ib/university/', 'IBと大学進学', '大学が求めるIBスコアの例', False)],
        CTA_T, [('what', 'できること'), ('subjects', '科目別ガイド'), ('price', '料金'), ('trial', '無料体験')], 'IBの家庭教師')

    # ---------------------------------------------------- Cambridge
    svc('igcse-a-level', 'IGCSE・A Levelの家庭教師｜Cambridgeの全科目対策｜神戸・大阪・オンライン｜Camino',
        'Cambridge IGCSE・AS & A Levelの家庭教師。インター卒業生の講師が、各科目の授業の理解、コースワーク、過去問（past papers）と採点基準（mark scheme）を使った試験対策まで、日英バイリンガルでサポートします。神戸・芦屋・西宮・大阪は対面、オンラインにも対応。初回60分無料',
        'IGCSE・A Level（Cambridge）の家庭教師', 'サービス',
        'ブリティッシュ系のインターで学ぶ<b>Cambridge IGCSE・AS & A Level</b>の授業と試験対策を行います。Cambridgeの試験は、過去問（past papers）と採点基準（mark scheme）を使った練習が得点に直結するため、答案の書き方まで丁寧に見ていきます',
        [('what', 'IGCSE・A Levelの家庭教師でできること', '',
          '<ul class="sj-top one rise"><li><b>授業の理解</b>：学校で習った単元を、日本語と英語で解説</li><li><b>過去問演習</b>：past papersを使い、mark schemeにもとづいて答案を見直します</li><li><b>CoreとExtended</b>：IGCSEで受けるレベルと、目標の成績に合わせた対策</li><li><b>コースワーク</b>：英語・地理・歴史などの課題の進め方</li><li><b>ASからA Levelへ</b>：AS Levelの内容を2年目まで保つ復習計画</li></ul>'),
         ('igcse', 'IGCSEの科目別ガイド', 'シラバスコード、ペーパーごとの時間・配点・比重をまとめています', sublinks(cards_cam()[:len(IGCSE)])),
         ('alevel', 'A Levelの科目別ガイド', 'ASとA Levelのペーパーの組み合わせをまとめています', sublinks(cards_cam()[len(IGCSE):])),
         ('price', '料金', '全プラン税込・授業料のみです', price_tbl([('高校生（IGCSE）', '¥15,000 / 60分', 'IGCSEの各科目'), ('高校生（Cambridge A Level）', '¥18,000 / 60分', 'A Levelの各科目。科目と指導内容に応じてご相談ください')]) + LONG),
         ('trial', '無料体験レッスンの流れ', '', TRIAL)],
        [('IGCSE・A Levelの家庭教師は、オンラインでも受けられますか？', 'はい。' + ONLINE),
         ('Cambridge以外の試験団体（Edexcelなど）のIGCSEにも対応していますか？', '科目の内容は共通する部分が多いため、対応できる場合があります。試験の形式は試験団体ごとに異なるため、まずはご相談ください'),
         ('料金はいくらですか？', 'IGCSEは高校生（G9〜G12）60分¥15,000、A Levelは60分¥18,000です（税込・授業料のみ）')],
        [('/subjects/igcse/', 'IGCSEの科目一覧', '14科目のシラバスと試験構成', True), ('/subjects/a-level/', 'A Levelの科目一覧', '13科目のシラバスと試験構成', False), ('/curriculum/cambridge/', 'Cambridgeのカリキュラムとは？', 'IGCSE・AS & A Level・AICE', False)],
        CTA_T, [('what', 'できること'), ('igcse', 'IGCSEの科目'), ('alevel', 'A Levelの科目'), ('price', '料金'), ('trial', '無料体験')], 'IGCSE・A Levelの家庭教師')

    # ---------------------------------------------------- AP
    svc('ap', 'APの家庭教師｜AP各科目の授業と5月の試験対策｜神戸・大阪・オンライン｜Camino',
        'AP（アドバンスト・プレースメント）の家庭教師。インター卒業生の講師が、AP各科目の授業の理解から、5月の試験に向けた過去の記述問題（free-response questions）の演習まで、日英バイリンガルでサポートします。神戸・芦屋・西宮・大阪は対面、オンラインにも対応。初回60分無料',
        'AP（アドバンスト・プレースメント）の家庭教師', 'サービス',
        'アメリカン系のインターで学ぶ<b>AP</b>の授業と、毎年5月の試験の対策を行います。APの試験は選択問題と記述問題で構成され、記述ではCollege Boardの採点基準にそった答え方が求められます',
        [('what', 'APの家庭教師でできること', '',
          '<ul class="sj-top one rise"><li><b>授業の理解</b>：大学1年生レベルの内容を、日本語と英語で解説</li><li><b>記述問題の対策</b>：College Boardが公開している過去の free-response questions と採点基準を使った練習</li><li><b>エッセイ</b>：English Language・Literature、History のエッセイ（DBQ・LEQ）の構成</li><li><b>学習計画</b>：5月の試験から逆算した、科目ごとの計画づくり</li><li><b>大学進学</b>：スコアの使われ方と、送るスコアの考え方。<a href="/curriculum/ap/university/">APと大学進学</a></li></ul>'),
         ('subjects', 'APの科目別ガイド', '2027年5月の試験の日程と形式をまとめています', sublinks(cards_ap())),
         ('price', '料金', '全プラン税込・授業料のみです', price_tbl([('高校生（IB DP・AP・Cambridge A Level）', '¥18,000 / 60分', 'APの各科目。科目と指導内容に応じてご相談ください')]) + LONG),
         ('trial', '無料体験レッスンの流れ', '', TRIAL)],
        [('APの家庭教師は、オンラインでも受けられますか？', 'はい。' + ONLINE),
         ('学校でAPの授業がなくても、試験の対策はできますか？', 'APの試験は、学校を通して申し込むのが一般的です。受験の方法は学校や試験会場に確認したうえで、学習内容と試験の対策をサポートします'),
         ('APの授業の料金はいくらですか？', 'APの授業は60分¥18,000です（税込・授業料のみ）')],
        [('/subjects/ap/', 'APの科目一覧', '18科目の2027年の試験形式', True), ('/curriculum/ap/', 'APとは？', '科目一覧・試験・スコア', False), ('/column/university/ap-results/', '国内インターのAPの結果', '各校が公表しているスコア', False)],
        CTA_T, [('what', 'できること'), ('subjects', '科目別ガイド'), ('price', '料金'), ('trial', '無料体験')], 'APの家庭教師')

    # ---------------------------------------------------- English tests
    svc('english-tests', '英検・TOEFL・IELTS・TOEIC対策の個別指導｜大人も受講可｜Camino',
        '英検・TOEFL iBT・IELTS・TOEICの個別対策。各試験の出題形式と評価基準をふまえて、現在の得点と技能別の課題を分析し、目標スコアに向けて重点的に指導します。インター生・帰国子女のほか、大人の方も受講いただけます。60分¥10,000、初回60分無料',
        '英検・TOEFL・IELTS・TOEIC対策', 'サービス',
        '目標スコアや現在の英語力に応じた個別対策です。各試験の<b>出題形式や評価基準</b>をふまえて、現在の得点と技能別の課題を分析し、優先的に取り組むべき分野を明確にして指導します。お子さんだけでなく、<b>大人の方も受講いただけます</b>',
        [('what', '授業の内容', '',
          '<ul class="sj-top one rise"><li><b>現状の分析</b>：直近のスコアや模試から、技能別の課題を整理</li><li><b>重点指導</b>：目標に対して伸ばしやすい分野から優先的に練習</li><li><b>ライティング・スピーキング</b>：実際の解答や発話をもとに、評価基準にそって具体的にフィードバック</li><li><b>学習方法の提案</b>：独学では気づきにくい弱点と、効果的な勉強法</li></ul>'),
         ('tests', '対応する試験', '各試験のしくみは、英語・資格のコラムで詳しく説明しています', sublinks(
             [('/column/english/eiken/', None, '英検', '8つの級・CSEスコア・試験日程'), ('/column/english/toefl/', None, 'TOEFL iBT', '2026年からの新形式・1〜6のスコア'),
              ('/column/english/ielts/', None, 'IELTS', 'AcademicとGeneral Training・バンドスコア'), ('/column/english/toeic/', None, 'TOEIC L&R', '構成・スコア・公開テスト日程')])),
         ('price', '料金', '税込・授業料のみです', price_tbl([('資格対策（英検・TOEFL・TOEIC・IELTS）', '¥10,000 / 60分', '目標スコアと現在の英語力に応じた個別対策')])),
         ('trial', '無料体験レッスンの流れ', '', TRIAL.replace('保護者・生徒', '受講者（お子さまの場合は保護者の方も）').replace('<span>生徒</span>', '<span>受講者</span>').replace('宿題や苦手な単元', '試験の問題'))],
        [('大人でも受講できますか？', 'はい。資格対策は、大学生・社会人の方も受講いただけます'),
         ('どの試験を受けるべきか、相談できますか？', 'はい。目的（大学出願、留学、就職など）と、提出先が認めている試験を確認したうえで、受ける試験と目標スコアを一緒に整理します'),
         ('授業はオンラインでも受けられますか？', 'はい。' + ONLINE)],
        [('/column/english/', '英検・TOEFL・IELTS・TOEICの違い', '4つの試験を比較', True), ('/services/', 'Caminoのサービス一覧', '家庭教師・保護者の相談', False)],
        CTA_T, [('what', '授業の内容'), ('tests', '対応する試験'), ('price', '料金'), ('trial', '無料体験')], '英語資格試験の対策')

    # ---------------------------------------------------- consultation
    svc('consultation', 'インター保護者の個別相談｜学習・カリキュラム・大学進学・就活｜Camino',
        'インターナショナルスクールに通うお子さんの保護者の方のための個別相談。日々の学習やカリキュラム・科目選択、国内外の大学進学、就職活動まで、インター卒業生の講師が疑問を整理し、今後の方針を一緒に考えます。60分¥5,000、15分の無料電話相談あり',
        'インター保護者の個別相談', 'サービス',
        'インターナショナルスクールでの学習・カリキュラム・進路選択について、保護者の方が抱える疑問や課題を整理し、<b>今後の方針や具体的な対応策を一緒に検討</b>します。まずは15分の無料電話相談からご利用いただけます',
        [('themes', 'ご相談のテーマ', 'ご家庭の状況やご関心に応じて、幅広くご相談いただけます',
          '<ul class="sj-top one rise"><li><b>日々の学習・カリキュラム</b>：宿題や課題への家庭での取り組み方、学習習慣の定着、IB・Cambridge・APの履修科目の選び方</li>'
          '<li><b>大学進学・受験</b>：志望大学・学部の選び方と出願の流れ、IB・A Levelの成績が評価されるしくみ、学年ごとの準備とスケジュール</li>'
          '<li><b>就職活動・キャリア</b>：インター卒業生・帰国生としての経験をふまえた、国内外の就職活動の進め方、英語面接・エントリーシートの準備、業界・企業選び</li></ul>'),
         ('price', '料金', '税込です', price_tbl([('無料電話相談', '¥0 / 15分', 'お悩みやご相談内容をお電話で伺います'), ('個別相談', '¥5,000 / 60分', '疑問や課題を整理し、今後の方針と具体的な対応策を一緒に検討します')])),
         ('read', '相談の前に読める記事', '', sublinks([('/column/university/', None, '大学進学のコラム', 'IB・A Level・APと大学出願'), ('/column/curriculum/', None, 'インターのカリキュラム', 'IB・Cambridge・APの違い'), ('/column/career/', None, '就職活動のコラム', 'キャリアフォーラム・日本の就活')]))],
        [('相談はオンラインですか？', '相談の方法（お電話・オンラインなど）は、ご都合に合わせてご相談ください。15分の無料電話相談はお電話で伺います'),
         ('子どもが同席してもいいですか？', 'はい。進路の相談などは、お子さんと一緒にお話しいただくこともできます'),
         ('無料電話相談のあとに、必ず申し込む必要がありますか？', 'いいえ。お話を伺ったうえで、必要なサポートがあればご提案します')],
        [('/services/parent-conference/', '保護者面談の同席・代理出席', '学校との面談をサポート', True), ('/column/university/after-graduation/', 'インター卒業後の進路', '海外大学・日本の大学への出願ルート', False)],
        CTA_C, [('themes', 'ご相談のテーマ'), ('price', '料金'), ('read', '関連する記事')], 'インター保護者の個別相談')

    # ---------------------------------------------------- parent conference
    svc('parent-conference', 'インターの保護者面談に同席・代理出席｜ペアレント・カンファレンス｜Camino',
        'インターナショナルスクールの保護者面談（ペアレント・カンファレンス）への同席・代理出席。英語での先生とのやりとりをはじめ、授業の進捗や学習状況、学校生活の確認まで、ご家庭のご要望に応じて対応し、内容を報告書にまとめて共有します。1科目¥5,000',
        '保護者面談の同席・代理出席（ペアレント・カンファレンス）', 'サービス',
        'インターナショナルスクールの保護者面談において、<b>学校とご家庭との円滑なコミュニケーション</b>をサポートします。英語での先生とのやりとりをはじめ、授業の進捗や学習状況、学校生活に関する確認など、ご家庭のご要望に応じて対応します',
        [('what', 'サポートの内容', '',
          '<ul class="sj-top one rise"><li><b>事前の打ち合わせ</b>：面談で確認したいことを、ご家庭と事前に整理します</li><li><b>面談への同席・代理出席</b>：英語での先生とのやりとりをサポートします</li><li><b>報告書</b>：話し合った内容、確認事項、今後の対応方針を報告書にまとめて共有します</li></ul>'),
         ('price', '料金', '税込です', price_tbl([('ペアレント・カンファレンス', '¥5,000 / 1科目', '面談の対象となる科目ごとの料金です')]))],
        [('どの学校の面談に対応していますか？', 'インターナショナルスクールの保護者面談に対応しています。面談の形式（対面・オンライン）や日程は、学校の案内にあわせてご相談ください'),
         ('英語が苦手でも大丈夫ですか？', 'はい。先生とのやりとりは講師がサポートし、内容は日本語の報告書でも共有します')],
        [('/services/consultation/', 'インター保護者の個別相談', '学習・進路・就活の相談', True), ('/services/international-school/', 'インター生の家庭教師', '授業の内容と料金', False)],
        ('保護者面談のサポートについて、相談したい方へ', '面談の日程と、確認したいことを伺ったうえでご案内します'), [('what', 'サポートの内容'), ('price', '料金')], 'ペアレント・カンファレンス')

    # ---------------------------------------------------- hub
    cards = [('/services/international-school/', '小学生〜高校生', 'インター生・帰国子女の家庭教師', '授業・宿題・課題・試験対策。60分¥10,000〜'),
             ('/services/ib/', 'PYP・MYP・DP', 'IBの家庭教師', '各科目とIA・EE・TOK。DPは60分¥18,000'),
             ('/services/igcse-a-level/', 'Cambridge', 'IGCSE・A Levelの家庭教師', 'past papersを使った試験対策'),
             ('/services/ap/', 'AP', 'APの家庭教師', '授業と5月の試験対策。60分¥18,000'),
             ('/services/english-tests/', '大人も受講可', '英検・TOEFL・IELTS・TOEIC対策', '目標スコアに向けた個別対策。60分¥10,000'),
             ('/services/consultation/', '保護者の方', 'インター保護者の個別相談', '学習・進路・就活。60分¥5,000、15分無料'),
             ('/services/parent-conference/', '保護者の方', '保護者面談の同席・代理出席', '報告書つき。1科目¥5,000'),
             ('/subjects/', '科目別ガイド', 'IB・IGCSE・A Level・APの科目別ガイド', '68科目の試験構成と出題範囲')]
    svc('', 'Caminoのサービスと料金｜インター生・帰国子女の家庭教師と保護者の相談｜Camino',
        'Caminoのサービス一覧。インター生・帰国子女の家庭教師（IB・IGCSE・A Level・AP）、英検・TOEFL・IELTS対策、保護者の個別相談、保護者面談の同席・代理出席。全プラン税込・授業料のみ、入会金なし。神戸・芦屋・西宮・大阪は対面、オンラインにも対応',
        'Caminoのサービスと料金', 'サービス',
        'お子さまの学習状況や目標、ご家庭のご要望を丁寧に伺い、一人ひとりに適した指導・サポートをご提供します。<b>全プラン授業料のみ（税込）</b>で、入会金・解約金・月額利用料はいただいておりません',
        [('list', 'サービス一覧', '', grid(cards, 'two')),
         ('price', '家庭教師の料金', '全プラン税込・授業料のみです', TUTOR_PRICE + LONG),
         ('policy', 'お支払い・振替・キャンセル', '', POLICY),
         ('legal', '運営者情報', '', '<p class="muted"><a href="/about/">運営者情報</a>　／　<a href="/privacy/">プライバシーポリシー</a></p>')],
        [('入会金はかかりますか？', 'いいえ。入会金・解約金・月額利用料はいただいておりません。授業料のほかに、対面授業の交通費と教材費を別途ご負担いただきます'),
         ('授業はどこで受けられますか？', ONLINE)],
        [('/subjects/', '科目別ガイド', 'IB・IGCSE・A Level・APの全科目', True), ('/area/kobe/', '対面授業の対応エリア', '神戸・芦屋・西宮・大阪', False)],
        CTA_T, [('list', 'サービス一覧'), ('price', '料金'), ('policy', 'お支払い・振替'), ('legal', '運営者情報')], 'Caminoの家庭教師・相談サービス')

LEGAL_CSS = """<style id="camino-legal">
.lg-main{background:#fff;color:#1c1c1c}
.lg-doc{max-width:760px;margin:0 auto;padding:72px max(20px,env(safe-area-inset-right,0px)) 96px max(20px,env(safe-area-inset-left,0px))}
.lg-doc h1{font-family:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho",serif!important;font-weight:600;font-size:30px;letter-spacing:.08em;line-height:1.4;margin:0;padding-bottom:20px;border-bottom:2px solid #1c1c1c;color:#1c1c1c}
.lg-doc .lg-meta{margin:12px 0 40px;text-align:right;font-size:13px;color:#555;letter-spacing:.04em}
.lg-doc p,.lg-doc li,.lg-doc td,.lg-doc th{font-size:15px;line-height:2;color:#1c1c1c;letter-spacing:.02em}
.lg-doc p{margin:0 0 14px}
.lg-doc,.lg-doc *{word-break:normal!important;overflow-wrap:anywhere;line-break:strict}
.lg-doc table{table-layout:fixed}
.lg-doc h2{font-family:"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho",serif!important;font-weight:600;font-size:17px;letter-spacing:.06em;margin:40px 0 12px;padding-bottom:8px;border-bottom:1px solid #c8c8c8;color:#1c1c1c}
.lg-doc ol.lg-items{list-style:none;padding:0;margin:0 0 14px;counter-reset:it}
.lg-doc ol.lg-items>li{counter-increment:it;position:relative;padding-left:2.6em;margin:2px 0}
.lg-doc ol.lg-items>li::before{content:"(" counter(it) ")";position:absolute;left:0}
.lg-doc ol.lg-paras{list-style:none;padding:0;margin:0 0 14px;counter-reset:pa}
.lg-doc ol.lg-paras>li{counter-increment:pa;position:relative;padding-left:1.6em;margin:0 0 8px}
.lg-doc ol.lg-paras>li::before{content:counter(pa);position:absolute;left:0}
.lg-doc table{width:100%;border-collapse:collapse;margin:8px 0 0;border-top:1px solid #1c1c1c}
.lg-doc th,.lg-doc td{border-bottom:1px solid #c8c8c8;padding:16px 14px;text-align:left;vertical-align:top}
.lg-doc th{width:26%;background:#f4f4f4;font-weight:600;white-space:nowrap}
.lg-doc a{color:#1c1c1c;text-decoration:underline;text-underline-offset:3px}
.lg-doc .lg-contact{margin-top:8px;padding:18px 20px;border:1px solid #c8c8c8}
.lg-doc .lg-contact p{margin:0}
.lg-doc .lg-end{margin-top:48px;text-align:right}
@media (max-width:600px){.lg-doc{padding-top:48px}.lg-doc h1{font-size:24px}.lg-doc th{width:32%;white-space:normal}.lg-doc th,.lg-doc td{padding:12px 10px}}
</style>"""

def legal_page(path, title, desc, h1, inner, ld_type='WebPage'):
    ld = {'@context': 'https://schema.org', '@graph': [{'@type': ld_type, 'name': h1, 'description': desc, 'inLanguage': 'ja', 'url': BASE + path,
           'isPartOf': {'@id': BASE + '/#website'}, 'dateModified': TODAY}]}
    head, hdr, tail = shell(path, title, desc, ld, nav='')
    head = head.replace('</head>', LEGAL_CSS + '\n</head>', 1)
    main = '<main class="lg-main">\n<article class="lg-doc">\n<h1>%s</h1>\n%s\n</article>\n' % (h1, inner)
    B.write(path.strip('/'), head + hdr + main + tail)
    URLS.append(BASE + path)

def legal():
    EMAIL = 'hirokit916@gmail.com'
    rows = [('名称', 'Camino Private Tutor'), ('運営者', '高島 宏樹'), ('所在地', '兵庫県神戸市'), ('メールアドレス', EMAIL),
            ('事業内容', '<ol class="lg-items"><li>インターナショナルスクールに在籍する児童・生徒及び帰国子女を対象とした家庭教師</li><li>英語資格試験（英検、TOEFL、IELTS、TOEIC等）の対策指導</li><li>保護者を対象とした学習・進路に関する個別相談</li><li>保護者面談への同席及び代理出席</li></ol>'),
            ('対応地域', '対面：兵庫県神戸市・芦屋市・西宮市、大阪府大阪市<br>オンライン：国内外')]
    about = '<p class="lg-meta">2026年11月14日現在</p>\n<table><tbody>%s</tbody></table>' % ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % r for r in rows)
    legal_page('/about/', '運営者情報｜Camino Private Tutor', 'Camino Private Tutor の運営者情報（名称、運営者、所在地、連絡先、事業内容）です。', '運営者情報', about, 'AboutPage')
    pp = """<p class="lg-meta">制定日：2026年11月14日</p>
<p>Camino Private Tutor（以下「当方」といいます。）は、当方が提供する家庭教師その他のサービス（以下「本サービス」といいます。）における利用者の個人情報の取扱いについて、以下のとおりプライバシーポリシー（以下「本ポリシー」といいます。）を定めます。</p>
<h2>第1条（個人情報）</h2>
<p>本ポリシーにおいて「個人情報」とは、個人情報の保護に関する法律（以下「個人情報保護法」といいます。）第2条第1項に定める個人情報をいいます。</p>
<h2>第2条（取得する個人情報）</h2>
<p>当方は、お問い合わせフォーム、電子メール、LINE、電話その他の方法により、次の個人情報を取得します。</p>
<ol class="lg-items"><li>氏名（保護者の氏名を含みます。）、メールアドレス、電話番号及びLINEのアカウント情報</li><li>生徒の学年、在籍する学校、学習状況、希望する授業形式・日時及び最寄駅</li><li>相談の内容並びに授業及び面談の記録</li></ol>
<h2>第3条（利用目的）</h2>
<p>当方は、取得した個人情報を次の目的のために利用します。</p>
<ol class="lg-items"><li>お問い合わせへの回答</li><li>無料体験、授業及び相談の日程調整並びに提供</li><li>授業内容の報告及び学習計画の提案</li><li>料金の請求及び支払いの確認</li><li>本サービスの改善</li></ol>
<h2>第4条（第三者提供）</h2>
<p>当方は、個人情報を第三者に提供しません。</p>
<h2>第5条（外部サービスの利用）</h2>
<p>当方は、お問い合わせフォームの送信にフォーム送信サービス（Formspree）を利用しています。フォームに入力された情報は、同サービスを経由して当方に送信されます。また、当方は、利用者との連絡に電子メール（Gmail）及びLINEを利用することがあります。</p>
<h2>第6条（安全管理措置）</h2>
<p>当方は、取り扱う個人情報の漏えい、滅失又は毀損の防止その他の個人情報の安全管理のために、必要かつ適切な措置を講じます。</p>
<h2>第7条（開示、訂正、利用停止等）</h2>
<p>当方は、本人から個人情報の開示、訂正、追加、削除、利用停止又は消去の請求があった場合には、本人であることを確認したうえで、個人情報保護法その他の法令に従い、遅滞なく対応します。</p>
<h2>第8条（本ポリシーの変更）</h2>
<p>当方は、必要に応じて本ポリシーを変更することがあります。変更後の本ポリシーは、本ウェブサイトに掲載した時点から効力を生じるものとします。</p>
<h2>第9条（お問い合わせ窓口）</h2>
<p>本ポリシーに関するお問い合わせは、下記の窓口までお願いいたします。</p>
<div class="lg-contact"><p>Camino Private Tutor</p><p>運営者：高島 宏樹</p><p>メールアドレス：%s</p></div>
<p class="lg-end">以上</p>""" % EMAIL
    legal_page('/privacy/', 'プライバシーポリシー｜Camino Private Tutor', 'Camino Private Tutor のプライバシーポリシー（個人情報の取扱いについて）です。', 'プライバシーポリシー', pp)

if __name__ == '__main__':
    build(); legal()
    open(os.path.join(HERE, 'urls_services.txt'), 'w').write('\n'.join(URLS))
    print(len(URLS), 'service/legal pages')
