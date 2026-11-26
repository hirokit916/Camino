# -*- coding: utf-8 -*-
"""Subject pages: /subjects/{ib,igcse,a-level,ap,myp,lower-secondary}/<slug>/ + hubs. usage: python3 build_subjects.py <site_root>"""
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
from data_ap import AP, AC
from data_mid import MID, MYP_CRIT_SRC
from data_links import L as OFF, cambridge_links

def offbox(links):
    if not links:
        return ''
    tag = {'page': '公式ページ', 'pdf': 'PDF', 'pdf-ja': 'PDF・日本語'}
    a = ''.join('<a href="%s" target="_blank" rel="noopener"><i>%s</i>%s</a>' % (u, tag[k], esc(n)) for n, u, k in links)
    return '<div class="sj-off"><p>公式資料</p><div>%s</div></div>' % a

def addsrc(src, links):
    have = {u for u, n in src}
    return src + [(u, n) for n, u, k in links if u not in have]

URLS = []
SRC_NOTE = ('本ページの試験構成と出題範囲は、%sの公式の資料をもとに、日本語で整理したものです。Caminoは%sと提携していません。'
            '試験の形式や時間は改訂されることがあるため、受験する年の最新の公式資料をあわせてご確認ください')

def camino_block(kind, name, price_keys, items):
    pr = ''.join('<p><span>%s</span><b>%s<small> / 60分（税込）</small></b></p>' % PRICE[k] for k in price_keys)
    lis = ''.join('<li>%s</li>' % x for x in items)
    return ('<div class="sj-cam rise"><div><h4>%sの授業でできること</h4><ul>%s</ul></div>'
            '<div class="sj-price sj-plan"><p class="sj-plan-tg">プラン</p><h4>家庭教師<small>インター生・帰国子女</small></h4>%s'
            '<a class="sj-plan-cta" href="/#contact">無料体験を申し込む</a></div></div>') % (name, lis, pr)

def step(n, id_, h, sub=''):
    return C.step(n, id_, h, sub)

def topics(lst):
    return '<ul class="sj-top rise">%s</ul>' % ''.join('<li>%s</li>' % esc(t) for t in lst)

def related(cards):
    return cards[:6]

# ------------------------------------------------------------------ Cambridge
def cambridge_page(d, level):
    lv = 'IGCSE' if level == 'igcse' else 'A Level'
    full = 'Cambridge IGCSE' if level == 'igcse' else 'Cambridge International AS & A Level'
    code = d['code']
    c1 = code.split('（')[0]
    path = '/subjects/%s/%s/' % (level, d['slug'])
    name = '%s %s' % (lv, d['ja'])
    title = '%s %s（%s）の家庭教師｜試験構成と出題範囲｜Camino' % (lv, d['ja'], c1)
    if len(title) > 44:
        title = '%s %s（%s）の家庭教師・試験構成｜Camino' % (lv, d['ja'], c1)
    desc = ('%s %s（%s）の試験構成（ペーパーごとの時間・配点・比重）と出題範囲を、公式シラバスをもとにまとめました。'
            'インター生・帰国子女向けに、%s %sの家庭教師（神戸・芦屋・西宮・大阪の対面／オンライン）を行っています。初回60分無料') % (full, d['en'], code, lv, d['ja'])
    h1 = '%s %s<span class="nw">（%s %s）</span>' % (lv, d['ja'], d['en'], c1)
    lead = ('%s %s（シラバスコード%s）の試験の構成と出題範囲を、Cambridge Internationalの公式シラバスをもとにまとめました。'
            'Caminoでは、インター生・帰国子女を対象に、<b>%s %sの家庭教師</b>を行っています') % (full, d['en'], code, lv, d['ja'])
    age = '14〜16歳（G9〜G10ごろ）' if level == 'igcse' else '16〜19歳（G11〜G12ごろ）'
    fx = facts([('シラバスコード', code), ('このページの対象', d['years'] + 'の試験'), ('成績', d['grades']), ('一般的な学年', age)])
    head = ['ペーパー', '時間', '配点', '比重', '内容']
    tbl = C.table(head, [(esc(p[0]), p[1], p[2], p[3], esc(p[4]) or '—') for p in d['papers']])
    body = [step(1, 'exam', '試験の構成', '%sの各ペーパー（試験）の時間・配点・比重です' % name), tbl]
    body.append(step(2, 'content', '出題範囲', 'シラバスに示されている学習内容の区分です'))
    body.append(topics(d['topics']))
    body.append(step(3, 'point', '押さえておきたいポイント'))
    body.append('<p class="sj-note rise">%s</p>' % d['note'])
    items = ['学校の授業内容の理解と、わからないところの解説（日本語・英語）',
             '宿題・課題%sの進め方のサポート' % ('・コースワーク' if level == 'igcse' else ''),
             '過去問（past papers）と採点基準（mark scheme）を使った試験対策',
             '記述問題の答案の添削と、得点につながる書き方の練習']
    keys = ['ms', 'hs'] if level == 'igcse' else ['dp']
    body.append(step(4, 'camino', '%sの家庭教師によるサポート' % name, '講師は、インターナショナルスクールでIBディプロマを取得したインター卒業生です'))
    body.append(camino_block('igcse', name, keys, items))
    ex = ''
    if d.get('tiers'):
        ex = ('CoreとExtendedのどちらを受けるべきですか？', 'Coreで取れる成績の上限はCです。A Levelなどでこの科目を続ける予定がある場合や、A*〜Bを目指す場合は、Extendedを受けるのが一般的です。どちらで受けるかは学校が決めることが多いため、まず学校の先生に確認しましょう')
    elif level == 'a-level':
        ex = ('AS Levelだけでも資格になりますか？', 'はい。AS Levelはそれだけで独立した資格として成績（a〜e）が出ます。続けてA Levelを修了すると、ASの内容もA Level全体の成績に含まれます。この科目のASとA Levelの組み合わせは、上の「試験の構成」の表をご覧ください')
    else:
        ex = ('どの年度のシラバスを確認すればいいですか？', '受験する年のシラバスを確認します。このページは%sのシラバスをもとにしています。シラバスはCambridge Internationalの公式サイトから確認できます' % d['years'])
    faq = [('%sの家庭教師は、オンラインでも受けられますか？' % name, 'はい。神戸・芦屋・西宮・大阪は対面、それ以外の地域や海外からはオンラインで受講いただけます。初回60分は無料体験です'), ex,
           ('%sの授業の料金はいくらですか？' % name, ('中学生（G6〜G8）は60分¥12,000、高校生（G9〜G12）は60分¥15,000です（税込・授業料のみ）' if level == 'igcse' else 'A Levelの授業は60分¥15,000です（税込・授業料のみ）') + '。入会金や月額利用料はありません')]
    lst = IGCSE if level == 'igcse' else ALEVEL
    sib = [('/subjects/%s/%s/' % (level, x['slug']), '%s %s（%s）' % (lv, x['ja'], x['code'].split('（')[0]), x['en'], False) for x in lst if x is not d][:3]
    nxt = [('/subjects/%s/' % level, '%sの科目一覧' % lv, '%sの全科目の試験構成と出題範囲' % lv, True)] + sib + \
          [('/curriculum/cambridge/', 'Cambridgeのカリキュラムとは？', 'IGCSE・AS & A Level・AICEのしくみ', False), ('/services/igcse-a-level/', 'IGCSE・A Levelの家庭教師', 'Caminoの指導内容と料金', False)]
    links = cambridge_links(level, d)
    src = addsrc([d['src']] + ([d['src2']] if d.get('src2') else []), links)
    fx += offbox(links)
    URLS.append(page(path, title, desc, h1, '%s・科目別ガイド' % full, lead, '\n'.join(body),
                     [('コラム', '/column/'), ('Cambridge', '/curriculum/cambridge/'), (lv, '/subjects/%s/' % level), ('%s（%s）' % (d['ja'], c1), path)],
                     faq=faq, nxt=nxt, cta=('%sの家庭教師について、相談したい方へ' % name, '学校の授業のサポートから試験対策まで、お子さんの状況に合わせてご提案します。初回60分は無料体験です'),
                     src=src, src_note=SRC_NOTE % ('Cambridge International', 'Cambridge International'), nav=COL_NAV,
                     kind=level, extra_hero=fx, toc_items=[('exam', '試験の構成'), ('content', '出題範囲'), ('point', 'ポイント'), ('camino', '家庭教師によるサポート')]))

# ------------------------------------------------------------------ IB DP
def ib_page(d):
    path = '/subjects/ib/%s/' % d['slug']
    short = d.get('short')
    name = 'IB %s' % d['ja']
    kw = 'IB DP %s%s' % (d['ja'], '（ESS）' if short == 'ESS' else '')
    title = '%sの家庭教師｜試験構成とIA｜Camino' % kw
    desc = ('IB（国際バカロレア）DP %s（%s）のSL・HLの試験構成と内部評価（IA）、学ぶ内容を、IBの公式資料をもとにまとめました。'
            'インター生・帰国子女向けに、IB %sの家庭教師（神戸・芦屋・西宮・大阪の対面／オンライン）を行っています。初回60分無料') % (d['ja'], d['en'], d['ja'])
    h1 = 'IB DP %s<span class="nw">（%s）</span>' % (d['ja'], d['en'])
    lead = ('国際バカロレア（IB）ディプロマ・プログラム（DP）の %s（%s）の試験の構成と学ぶ内容を、IBの公式資料をもとにまとめました。'
            'Caminoでは、インター生・帰国子女を対象に、<b>IB %sの家庭教師</b>を行っています') % (d['ja'], d['en'], d['ja'])
    sci = d.get('sci')
    fx = facts([('このページの対象', d['fa'] + 'からの試験'), ('成績', '1〜7（DP全体は45点満点の一部）'), ('授業時間の目安', 'SL 150時間／HL 240時間'), ('一般的な学年', 'G11〜G12（16〜19歳）')])
    tbl = C.table(['評価', 'SL', 'HL', '比重', '内容'], [(esc(p[0]), p[1], p[2], p[3], esc(p[4])) for p in d['papers']])
    body = [step(1, 'exam', '試験と評価の構成', '外部評価（筆記試験）と内部評価（IA）の時間・比重です。「—」はそのレベルにはない評価です'), tbl]
    body.append(step(2, 'content', '学ぶ内容', 'IBの公式資料に示されている内容の区分です'))
    body.append(topics(d['topics']))
    body.append(step(3, 'point', '押さえておきたいポイント'))
    body.append('<p class="sj-note rise">%s</p>' % d['note'])
    items = ['学校の授業内容の理解と、わからないところの解説（日本語・英語）',
             '内部評価（IA）%sのテーマ選びと進め方のサポート' % ('・口頭試験' if 'Individual oral' in str(d['papers']) else ''),
             'IBの評価規準（markbands）にもとづいた答案・レポートの見直し', '過去問を使った試験対策と、Predicted gradeを意識した学習計画']
    body.append(step(4, 'camino', '%sの家庭教師によるサポート' % name, '講師は、インターナショナルスクールでIBディプロマを取得したインター卒業生です'))
    body.append(camino_block('ib', name, ['dp'], items))
    faq = [('%sの家庭教師は、オンラインでも受けられますか？' % name, 'はい。神戸・芦屋・西宮・大阪は対面、それ以外の地域や海外からはオンラインで受講いただけます。初回60分は無料体験です'),
           ('SLとHLでは何が違いますか？', 'IBの目安では、授業時間がSLは150時間、HLは240時間です。この科目では、上の表のとおり試験の時間や評価の比重もSLとHLで異なります'),
           ('%sの授業の料金はいくらですか？' % name, 'IB DPの授業は60分¥15,000です（税込・授業料のみ）。入会金や月額利用料はありません')]
    sib = [('/subjects/ib/%s/' % x['slug'], 'IB %s' % x['ja'], x['en'], False) for x in DP if x is not d][:3]
    nxt = [('/subjects/ib/', 'IB DPの科目一覧', 'IB DPの全科目の試験構成と学ぶ内容', True)] + sib + \
          [('/ib/dp/', 'IBのDPとは？', '科目・HL/SL・TOK・EE・CAS・45点満点', False), ('/services/ib/', 'IBの家庭教師', 'Caminoの指導内容と料金', False)]
    links = OFF.get(path, [])
    src = addsrc([d['src']] + ([d['src2']] if d.get('src2') else []), links)
    fx += offbox(links)
    URLS.append(page(path, title, desc, h1, '国際バカロレア（IB）DP・科目別ガイド', lead, '\n'.join(body),
                     [('コラム', '/column/'), ('国際バカロレア（IB）DP', '/ib/dp/'), ('科目別ガイド', '/subjects/ib/'), (d['ja'], path)],
                     faq=faq, nxt=nxt, cta=('%sの家庭教師について、相談したい方へ' % name, 'IAの進め方から試験対策まで、お子さんの状況に合わせてご提案します。初回60分は無料体験です'),
                     src=src, src_note=SRC_NOTE % ('国際バカロレア機構（IB）', 'IB'), nav=COL_NAV,
                     kind='ib', extra_hero=fx, toc_items=[('exam', '試験と評価の構成'), ('content', '学ぶ内容'), ('point', 'ポイント'), ('camino', '家庭教師によるサポート')]))

# ------------------------------------------------------------------ AP
def ap_page(d):
    path = '/subjects/ap/%s/' % d['slug']
    name = 'AP %s' % d['ja']
    title = 'AP %s（%s）の家庭教師｜試験形式と対策｜Camino' % (d['ja'], d['en'])
    if len(title) > 50:
        title = 'AP %s（%s）の家庭教師｜Camino' % (d['ja'], d['en'])
    desc = ('AP %s（%s）の2027年5月の試験の形式（セクションごとの問題数・時間・比重）と学ぶ内容を、College Boardの公式情報をもとにまとめました。'
            'インター生・帰国子女向けに、AP %sの家庭教師（対面／オンライン）を行っています。初回60分無料') % (d['ja'], d['en'], d['ja'])
    h1 = 'AP %s<span class="nw">（AP %s）</span>' % (d['ja'], d['en'])
    lead = ('College Boardが実施するAP %s（%s）の、2027年5月の試験の形式と学ぶ内容を、公式情報をもとにまとめました。'
            'Caminoでは、インター生・帰国子女を対象に、<b>AP %sの家庭教師</b>を行っています') % (d['ja'], d['en'], d['ja'])
    fx = facts([('2027年の試験日', d['date']), ('試験の形式', d['fmt']), ('スコア', '1〜5（多くの大学は3以上を単位認定の目安に）')])
    tbl = C.table(['セクション', '問題数', '時間', '比重', '内容'], [(esc(p[0]), p[1], p[2], p[3], esc(p[4]) or '—') for p in d['papers']])
    body = [step(1, 'exam', '試験の形式（2027年5月）', 'セクションごとの問題数・時間・スコアに占める比重です'), tbl]
    body.append(step(2, 'content', '学ぶ内容'))
    body.append(topics(d['topics']))
    body.append(step(3, 'point', '押さえておきたいポイント'))
    body.append('<p class="sj-note rise">%s</p>' % d['note'])
    items = ['学校の授業内容の理解と、わからないところの解説（日本語・英語）', '宿題・小テスト・定期試験に向けたサポート',
             'College Boardの過去の記述問題（free-response questions）と採点基準を使った対策', '5月の本番に向けた学習計画と模試形式の練習']
    body.append(step(4, 'camino', '%sの家庭教師によるサポート' % name, '講師は、インターナショナルスクール卒業生です'))
    body.append(camino_block('ap', name, ['adv'], items))
    faq = [('%sの家庭教師は、オンラインでも受けられますか？' % name, 'はい。神戸・芦屋・西宮・大阪は対面、それ以外の地域や海外からはオンラインで受講いただけます。初回60分は無料体験です'),
           ('%sのスコアは、大学でどう使われますか？' % name, 'APのスコアは1〜5で、多くの大学は3以上を単位認定や上級クラスへの配置の目安にしています。必要なスコアは大学・学部ごとに違うため、志望校の公式の基準を確認しましょう。詳しくは「APと大学進学」のページで説明しています'),
           ('%sの授業の料金はいくらですか？' % name, 'APの授業は60分¥18,000です（税込・授業料のみ）。入会金や月額利用料はありません')]
    sib = [('/subjects/ap/%s/' % x['slug'], 'AP %s' % x['ja'], x['en'], False) for x in AP if x is not d][:3]
    nxt = [('/subjects/ap/', 'APの科目一覧', 'APの各科目の試験形式と学ぶ内容', True)] + sib + \
          [('/curriculum/ap/university/', 'APと大学進学', '単位認定の調べ方とスコアの送り方', False), ('/services/ap/', 'APの家庭教師', 'Caminoの指導内容と料金', False)]
    links = OFF.get(path, [])
    src = addsrc([(AC % d['cb'], 'College Board（AP Central）：AP %s Exam' % d['en'])], links)
    fx += offbox(links)
    URLS.append(page(path, title, desc, h1, 'AP（アドバンスト・プレースメント）・科目別ガイド', lead, '\n'.join(body),
                     [('コラム', '/column/'), ('AP', '/curriculum/ap/'), ('科目別ガイド', '/subjects/ap/'), (d['ja'], path)],
                     faq=faq, nxt=nxt, cta=('%sの家庭教師について、相談したい方へ' % name, '授業のサポートから5月の試験対策まで、お子さんの状況に合わせてご提案します。初回60分は無料体験です'),
                     src=src, src_note=SRC_NOTE % ('College Board', 'College Board'), nav=COL_NAV,
                     kind='ap', extra_hero=fx, toc_items=[('exam', '試験の形式'), ('content', '学ぶ内容'), ('point', 'ポイント'), ('camino', '家庭教師によるサポート')]))

# ------------------------------------------------------------------ Middle school
def mid_page(d):
    g = d['group']
    folder = 'myp' if g == 'myp' else 'lower-secondary'
    path = '/subjects/%s/%s/' % (folder, d['slug'])
    if g == 'myp':
        name = 'MYP %s' % d['ja'].split('（')[0]
        title = 'IB MYP %sの家庭教師｜評価規準とeAssessment｜Camino' % d['ja'].split('（')[0]
        h1 = 'IB MYP %s' % d['ja']
        small = '国際バカロレア（IB）MYP・科目別ガイド'
        lead = ('国際バカロレア（IB）の中等教育プログラム（MYP）の%sについて、評価規準（A〜D）と任意のeAssessmentを、IBの公式資料をもとにまとめました。'
                'Caminoでは、インター生・帰国子女を対象に、<b>MYP %sの家庭教師</b>を行っています') % (d['ja'], d['ja'].split('（')[0])
        fx = facts([('対象', d['age']), ('評価', '4つの規準（A〜D）を各1〜8で評価'), ('最終学年の試験', '任意のeAssessment（MYP 5年目）')])
        tbl = C.table(['規準', '英語の名前', '内容'], [(c[0], c[1], c[2]) for c in d['crit']])
        body = [step(1, 'exam', '評価規準（A〜D）', '4つの規準は同じ重みで、それぞれ1〜8の8段階で評価されます'), tbl]
        body.append(step(2, 'content', '学ぶ内容と授業の形'))
        body.append(topics([d['org'], d['key']]))
        ea_txt, ea_rows = d['ea']
        body.append(step(3, 'ea', 'eAssessment（任意のオンスクリーン試験）', ea_txt))
        if ea_rows:
            body.append(C.table(['課題', '配点'], ea_rows))
        body.append('<p class="sj-note rise">%s</p>' % d['note'])
        keys = ['ms', 'hs']
        src = [d['src'], MYP_CRIT_SRC]
        nav_on = '/subjects/middle-school/'
        nx_curr = ('/ib/myp/', 'IBのMYPとは？', '8つの教科グループと評価のしくみ', False)
        org = ('国際バカロレア機構（IB）', 'IB')
        items = ['学校の授業内容の理解と、わからないところの解説（日本語・英語）', '課題（タスク）の進め方と、評価規準を意識した仕上げ方',
                 '実験レポート・調べ学習の構成と書き方のサポート' if 'sciences' in d['slug'] else '規準B・Dの課題での、考え方を言葉で説明する練習', 'DPやIGCSEに向けた土台づくり']
        tocs = [('exam', '評価規準'), ('content', '学ぶ内容'), ('ea', 'eAssessment'), ('camino', '家庭教師によるサポート')]
    else:
        name = 'Lower Secondary %s' % d['ja'].split('（')[0]
        title = 'Cambridge Lower Secondary %s（%s）の家庭教師｜Checkpoint｜Camino' % (d['ja'].split('（')[0], d['code'])
        h1 = 'Cambridge Lower Secondary %s' % d['ja']
        small = 'Cambridge Lower Secondary（中学）・科目別ガイド'
        lead = ('Cambridge Lower Secondaryの%sについて、学ぶ内容（strands）とStage 9の終わりに受けるCheckpointを、Cambridge Internationalの公式資料をもとにまとめました。'
                'Caminoでは、インター生・帰国子女を対象に、<b>中学生の%sの家庭教師</b>を行っています') % (d['ja'], d['ja'].split('（')[0])
        fx = facts([('対象', d['age']), ('Checkpoint', 'Stage 9の終わり・Cambridgeが採点'), ('結果', '0〜50のスコアと6段階の評価')])
        body = [step(1, 'content', '学ぶ内容（strands）', '2020年版のカリキュラム・フレームワーク（2021年から使用）の区分です')]
        body.append(C.table(['分野（strand）', '内容'], [(a, b) for a, b in d['strands']]))
        body.append(step(2, 'exam', 'Lower Secondary Checkpoint', 'Stage 9の終わりに受けるテストです（2027年3月シリーズの時間割より）'))
        body.append(C.table(['テスト', '時間'], d['chk']))
        body.append(step(3, 'point', '押さえておきたいポイント'))
        body.append('<p class="sj-note rise">%s</p>' % d['note'])
        keys = ['ms']
        src = [d['src'], d['src2']]

        nav_on = '/subjects/middle-school/'
        nx_curr = ('/curriculum/cambridge/', 'Cambridgeのカリキュラムとは？', '5つの段階とIGCSE・A Level', False)
        org = ('Cambridge International', 'Cambridge International')
        items = ['学校の授業内容の理解と、わからないところの解説（日本語・英語）', '宿題・小テストのサポートと、学習習慣づくり',
                 'Checkpointに向けた過去問演習', 'IGCSEに向けた土台づくり']
        tocs = [('content', '学ぶ内容'), ('exam', 'Checkpoint'), ('point', 'ポイント'), ('camino', '家庭教師によるサポート')]
    desc = re.sub(r'<[^>]+>', '', lead) + '。神戸・芦屋・西宮・大阪の対面／オンライン、初回60分無料'
    links = OFF.get(path, [])
    src = addsrc(src, links)
    fx += offbox(links)
    body.append(step(len([b for b in body if 'class="step"' in b]) + 1, 'camino', '%sの家庭教師によるサポート' % name, '講師は、インターナショナルスクールでIBディプロマを取得したインター卒業生です'))
    body.append(camino_block('mid', name, keys, items))
    faq = [('%sの家庭教師は、オンラインでも受けられますか？' % name, 'はい。神戸・芦屋・西宮・大阪は対面、それ以外の地域や海外からはオンラインで受講いただけます。初回60分は無料体験です'),
           ('中学生の授業の料金はいくらですか？', '中学生（G6〜G8）は60分¥12,000、G9以上は60分¥15,000です（税込・授業料のみ）。入会金や月額利用料はありません')]
    sib = [('/subjects/%s/%s/' % ('myp' if x['group'] == 'myp' else 'lower-secondary', x['slug']), ('MYP ' if x['group'] == 'myp' else 'Lower Secondary ') + x['ja'], x['en'], False) for x in MID if x is not d][:3]
    nxt = [('/subjects/middle-school/', '中学の科目一覧', 'MYPとCambridge Lower Secondary', True)] + sib + [nx_curr, ('/services/international-school/', 'インター生の家庭教師', 'Caminoの指導内容と料金', False)]
    URLS.append(page(path, title, desc, h1, small, lead, '\n'.join(body),
                     ([('コラム', '/column/'), ('MYP', '/ib/myp/')] if g == 'myp' else [('コラム', '/column/'), ('Cambridge', '/curriculum/cambridge/')]) + [('中学の科目別ガイド', '/subjects/middle-school/'), (d['ja'], path)],
                     faq=faq, nxt=nxt, cta=('%sの家庭教師について、相談したい方へ' % name, '日々の授業のサポートから、IGCSE・DPに向けた土台づくりまでご提案します。初回60分は無料体験です'),
                     src=src, src_note=SRC_NOTE % org, nav=COL_NAV,
                     kind='mid', extra_hero=fx, toc_items=tocs))

# ------------------------------------------------------------------ hubs
HUBS = {
 'ib': ('IB DPの科目別ガイドと家庭教師', 'IB DP 科目一覧｜各科目の試験構成と家庭教師｜Camino', 'IB（国際バカロレア）DP',
        'IB（国際バカロレア）DPの主な科目について、SL・HLの試験構成、内部評価（IA）、学ぶ内容を、IBの公式資料をもとにまとめました',
        lambda: [('/subjects/ib/%s/' % d['slug'], d['fa'].split('（')[0] + 'から', 'IB %s' % d['ja'], d['en']) for d in DP], 'ib'),
 'igcse': ('IGCSEの科目別ガイドと家庭教師', 'IGCSE 科目一覧｜シラバスコード・試験構成と家庭教師｜Camino', 'Cambridge IGCSE',
           'Cambridge IGCSEの主な科目について、シラバスコード、ペーパーごとの時間・配点・比重、出題範囲を、公式シラバスをもとにまとめました',
           lambda: [('/subjects/igcse/%s/' % d['slug'], d['code'].split('（')[0], 'IGCSE %s' % d['ja'], d['en']) for d in IGCSE], 'igcse'),
 'a-level': ('A Levelの科目別ガイドと家庭教師', 'A Level 科目一覧｜シラバスコード・試験構成と家庭教師｜Camino', 'Cambridge International AS & A Level',
             'Cambridge International AS & A Levelの主な科目について、シラバスコード、ASとA Levelのペーパーの組み合わせ、出題範囲を、公式シラバスをもとにまとめました',
             lambda: [('/subjects/a-level/%s/' % d['slug'], d['code'], 'A Level %s' % d['ja'], d['en']) for d in ALEVEL], 'a-level'),
 'ap': ('APの科目別ガイドと家庭教師', 'AP 科目一覧｜2027年の試験形式と家庭教師｜Camino', 'AP（アドバンスト・プレースメント）',
        'APの主な科目について、2027年5月の試験の日程・形式・セクションごとの問題数と時間を、College Boardの公式情報をもとにまとめました',
        lambda: [('/subjects/ap/%s/' % d['slug'], d['date'].split('（')[0].replace('2027年', ''), 'AP %s' % d['ja'], d['en']) for d in AP], 'ap'),
}

def hub(key):
    h1, title, small, lead, cards, kind = HUBS[key]
    path = '/subjects/%s/' % key
    cs = cards()
    body = step(1, 'list', '科目一覧', '科目を選ぶと、試験の構成・学ぶ内容・Caminoの指導内容を確認できます') + grid(cs)
    lead2 = lead + '。Caminoでは、インター生・帰国子女を対象に、各科目の家庭教師（神戸・芦屋・西宮・大阪の対面／オンライン）を行っています'
    nm = {'ib': 'IB', 'igcse': 'IGCSE', 'a-level': 'A Level', 'ap': 'AP'}[key]
    svc = {'ib': '/services/ib/', 'igcse': '/services/igcse-a-level/', 'a-level': '/services/igcse-a-level/', 'ap': '/services/ap/'}[key]
    nxt = [(svc, '%sの家庭教師' % nm, 'Caminoの指導内容と料金', True), ('/subjects/', '科目別ガイド', 'IB・IGCSE・A Level・AP・中学の全科目', False)]
    il = {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + u, 'name': b} for i, (u, t, b, d) in enumerate(cs)]}
    URLS.append(page(path, title, lead2, h1, small + '・科目別ガイド', lead2, body, [('コラム', '/column/'), ('科目別ガイド', '/subjects/'), (nm, path)],
                     nxt=nxt, cta=('%sの家庭教師について、相談したい方へ' % nm, '科目選びから試験対策まで、お子さんの状況に合わせてご提案します。初回60分は無料体験です'),
                     nav=COL_NAV, kind=kind, ld_type='CollectionPage', extra_ld=[il]))

def hub_mid():
    path = '/subjects/middle-school/'
    cs = [('/subjects/%s/%s/' % ('myp' if d['group'] == 'myp' else 'lower-secondary', d['slug']), 'IB MYP' if d['group'] == 'myp' else 'Cambridge',
           ('MYP ' if d['group'] == 'myp' else 'Lower Secondary ') + d['ja'], d['en']) for d in MID]
    lead = ('インターの中学（G6〜G9ごろ）で学ぶ、IB MYPとCambridge Lower Secondaryの主な科目について、評価のしくみと学ぶ内容を公式資料をもとにまとめました。'
            'Caminoでは、インター生・帰国子女を対象に、中学生の家庭教師（神戸・芦屋・西宮・大阪の対面／オンライン）を行っています')
    body = step(1, 'list', '科目一覧', '中学の理科・数学・英語は、IGCSEやDPの科目の土台になります') + grid(cs)
    nxt = [('/services/international-school/', 'インター生の家庭教師', 'Caminoの指導内容と料金', True), ('/subjects/igcse/', 'IGCSEの科目一覧', '中3〜高1で学ぶIGCSE', False), ('/ib/myp/', 'IBのMYPとは？', '8つの教科グループと評価', False)]
    il = {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + u, 'name': b} for i, (u, t, b, d) in enumerate(cs)]}
    URLS.append(page(path, 'インター中学生の家庭教師｜MYP・Lower Secondaryの理科・数学・英語｜Camino', lead, '中学（MYP・Lower Secondary）の科目別ガイド', 'インターの中学・科目別ガイド', lead, body,
                     [('コラム', '/column/'), ('科目別ガイド', '/subjects/'), ('中学', path)], nxt=nxt, cta=('中学生の家庭教師について、相談したい方へ', '日々の授業のサポートから学習習慣づくりまで、お子さんに合わせてご提案します。初回60分は無料体験です'),
                     nav=COL_NAV, kind='mid', ld_type='CollectionPage', extra_ld=[il]))

def hub_all():
    path = '/subjects/'
    lead = ('インター生が学ぶIB（MYP・DP）、Cambridge（Lower Secondary・IGCSE・A Level）、APの主な科目について、試験の構成と学ぶ内容を、各試験団体の公式資料をもとにまとめました。'
            'Caminoでは、インター生・帰国子女を対象に、各科目の家庭教師（神戸・芦屋・西宮・大阪の対面／オンライン）を行っています')
    secs = [('IB DP', '/subjects/ib/', [(('/subjects/ib/%s/' % d['slug']), None, 'IB %s' % d['ja'], d['en']) for d in DP]),
            ('Cambridge IGCSE', '/subjects/igcse/', [(('/subjects/igcse/%s/' % d['slug']), d['code'].split('（')[0], 'IGCSE %s' % d['ja'], d['en']) for d in IGCSE]),
            ('Cambridge AS & A Level', '/subjects/a-level/', [(('/subjects/a-level/%s/' % d['slug']), d['code'], 'A Level %s' % d['ja'], d['en']) for d in ALEVEL]),
            ('AP', '/subjects/ap/', [(('/subjects/ap/%s/' % d['slug']), None, 'AP %s' % d['ja'], d['en']) for d in AP]),
            ('中学（MYP・Lower Secondary）', '/subjects/middle-school/', [(('/subjects/%s/%s/' % ('myp' if d['group'] == 'myp' else 'lower-secondary', d['slug'])), None, ('MYP ' if d['group'] == 'myp' else 'Lower Secondary ') + d['ja'], d['en']) for d in MID])]
    body = ''
    for n, (nm, u, cs) in enumerate(secs):
        body += step(n + 1, u.strip('/').split('/')[-1], nm, '<a href="%s">%sの科目一覧 →</a>' % (u, nm)) + grid(cs)
    URLS.append(page(path, '科目別ガイド｜IB・IGCSE・A Level・APの家庭教師｜Camino', lead, '科目別ガイド<span class="nw">（IB・IGCSE・A Level・AP）</span>', 'インター生の科目別ガイド', lead, body,
                     [('科目別ガイド', path)], nxt=[('/services/', 'Caminoのサービス', '家庭教師・保護者の相談・資格対策', True)],
                     cta=('科目の家庭教師について、相談したい方へ', '学校の授業のサポートから試験対策まで、お子さんの状況に合わせてご提案します。初回60分は無料体験です'),
                     nav=COL_NAV, kind='svc', ld_type='CollectionPage',
                     toc_items=[(u.strip('/').split('/')[-1], nm) for nm, u, cs in secs]))

import re
if __name__ == '__main__':
    for d in IGCSE: cambridge_page(d, 'igcse')
    for d in ALEVEL: cambridge_page(d, 'a-level')
    for d in DP: ib_page(d)
    for d in AP: ap_page(d)
    for d in MID: mid_page(d)
    for k in HUBS: hub(k)
    hub_mid(); hub_all()
    open(os.path.join(HERE, 'urls_subjects.txt'), 'w').write('\n'.join(URLS))
    print(len(URLS), 'subject pages')
