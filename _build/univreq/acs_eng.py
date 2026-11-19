# -*- coding: utf-8 -*-
"""English-test requirements, AU/CA/SG top 5 (official pages, checked 2026-11-16).
inter: how an IB / international-school student in Japan can meet the requirement
  'S' = English-medium schooling counts regardless of country
  'C' = schooling counts only in an English-speaking country (Japan's international schools don't qualify)
  'Q' = test needed only for listed national qualifications / non-English-medium qualifications (IB・A Level not listed)
  None = not confirmed"""
import analysis_html as AN

E = [
 dict(c='AU', ja='ニューサウスウェールズ大学', ielts='6.5（各6.0）。経営・法学は7.0', toefl='90。経営・法学は94', new='受け付けていない（当面）', inter='S',
      ib='IBを英語で学んでいれば満たせる。それ以外はEnglish A HL 4・SL 5、English B HL 7', note='',
      src='https://www.unsw.edu.au/study/how-to-apply/english-language-requirements'),
 dict(c='AU', ja='メルボルン大学', ielts='6.5（各6.0）', toefl='81', new=None, inter='C',
      ib='IB English A・B 4以上（SL・HL）', note='英語圏の国籍か10年以上の居住が前提の学歴免除のため、日本のインターは学歴では対象外',
      src='https://study.unimelb.edu.au/how-to-apply/english-language-requirements/undergraduate-english-language-requirements'),
 dict(c='AU', ja='シドニー大学', ielts='6.5（各6.0）', toefl='TOEFL Australia版のみ', new=None, inter='S',
      ib='—', note='入学前5年以内に、英語で授業を行う中等教育を修了していれば満たせる',
      src='https://www.sydney.edu.au/study/applying/how-to-apply/international-students/english-language-requirements.html'),
 dict(c='AU', ja='オーストラリア国立大学', ielts='6.5（各6.0）', toefl='80', new=None, inter='C',
      ib='IB English A（SL・HL）の合格', note='学歴免除は英語圏の国（Group A）での在籍が条件',
      src='https://policies.anu.edu.au/ppl/document/ANUP_000408'),
 dict(c='AU', ja='モナシュ大学', ielts=None, toefl=None, new=None, inter=None, ib=None, note='公式サイトで確認できず', src=None),
 dict(c='CA', ja='マギル大学', ielts='6.5（各6.0）', toefl='90。経営は100', new='4.5。経営は5.0', inter='C',
      ib='IB English A 5以上', note='英語圏以外の国で英語で授業を行う学校に通っても、学歴免除の対象外と明記',
      src='https://www.mcgill.ca/undergraduate-admissions/apply/english-proficiency'),
 dict(c='CA', ja='トロント大学', ielts='6.5（各6.0）', toefl='89', new='4.5', inter='C',
      ib='—', note='学歴免除は英語が主な言語の国で4年以上。国の一覧に日本はない',
      src='https://future.utoronto.ca/english-language-requirements'),
 dict(c='CA', ja='ブリティッシュコロンビア大学', ielts='6.5（各6.0）', toefl='90', new=None, inter='S',
      ib='IB English A 5以上', note='英語圏以外の国でも、IBなどを提供するインターに4年以上在籍していれば満たせる',
      src='https://you.ubc.ca/applying-ubc/requirements/english-language-competency/'),
 dict(c='CA', ja='アルバータ大学', ielts='6.5（各6.0）', toefl='90', new='4.5', inter=None,
      ib='IB English A 5以上、English B 6以上', note='CIS加盟校かアメリカの認定校に3年以上在籍し、最終学年の英語の授業に合格していれば満たせる（学校の所在国の条件は明記なし）',
      src='https://www.ualberta.ca/en/admissions/how-to-apply/admission-requirements/language-requirements/index.html'),
 dict(c='CA', ja='ウォータールー大学', ielts='6.5（ライティング・スピーキング6.5）', toefl='90', new='4.5', inter='S',
      ib='—', note='直近4年間、英語で授業を行う学校に通っていれば満たせる',
      src='https://uwaterloo.ca/future-students/admissions/english-language-requirements'),
 dict(c='SG', ja='シンガポール国立大学', ielts='6.5（リーディング・ライティング6.5）。法学は7.0', toefl='92〜93。法学は100', new=None, inter='Q',
      ib='—', note='英語試験は、ドイツのアビトゥアや中国の高考など指定された資格の出願者に求める（IB・A Levelは対象外）',
      src='https://nus.edu.sg/oam/docs/default-source/nus-publications/intlprospectus.pdf'),
 dict(c='SG', ja='南洋理工大学', ielts='6.5（ライティング・スピーキング6.5）', toefl='90', new='4.5', inter='Q',
      ib='—', note='英語試験は、指定された資格の出願者と、中学・高校で英語を学んでいない出願者に求める。SAT 1250（ERW 600）でも可',
      src='https://www.ntu.edu.sg/admissions/undergraduate/admission-guide/international-qualifications'),
 dict(c='SG', ja='シンガポール経営大学', ielts='7.0。法学は7.5', toefl='93。法学は100', new='5.0。法学は5.5', inter='Q',
      ib='IBディプロマなら試験の提出は不要', note='海外の資格で出願する人は、SAT・ACT・IELTS・TOEFLなどのいずれかを提出',
      src='https://admissions.smu.edu.sg/admissions-requirements/international-and-other-qualifications'),
 dict(c='SG', ja='シンガポール工科デザイン大学', ielts='公表なし', toefl='公表なし', new=None, inter='Q',
      ib='—', note='英語試験は、英語以外の言語で授業を行う資格の出願者に求める',
      src='https://www.sutd.edu.sg/admissions/undergraduate/admission-requirements/international-qualifications/'),
 dict(c='SG', ja='シンガポール工科大学', ielts='6.5', toefl='90', new=None, inter='Q',
      ib='—', note='英語試験は、英語以外の言語で授業を行う資格の出願者に求める',
      src='https://www.singaporetech.edu.sg/sites/default/files/2026-04/Application%20International%20Guide_06042026.pdf'),
]
CN = {'AU': 'オーストラリア', 'CA': 'カナダ', 'SG': 'シンガポール'}
INTER = {'S': ('国を問わず、英語で学んだ学歴で満たせる', '--vc1', 'w'), 'Q': ('IB・A Levelでの出願なら、原則として試験は不要', '--vc2', 'w'),
         'C': ('英語圏の国での在籍が条件（日本のインターは対象外）', '--vc3', 'w')}

def verified(): return [d for d in E if d['ielts'] and d['ielts'] != '公表なし']
def counts():
    v = [d for d in E if d['inter']]
    return {k: sum(1 for d in v if d['inter'] == k) for k in INTER}, len(v)

def table_html(cls='rq-mj'):
    import build_req as BR
    head = ['大学', 'IELTS', 'TOEFL（0〜120）', '新TOEFL（1〜6）', 'IBで満たせる条件', '日本のインター生の扱い']
    rows = [['%s<br><small>%s</small>' % (d['ja'], CN[d['c']]), d['ielts'] or '—', d['toefl'] or '—', d['new'] or '—', d['ib'] or '—',
             (INTER[d['inter']][0] + ('。' + d['note'] if d['note'] else '')) if d['inter'] else (d['note'] or '—')] for d in E]
    return BR.more('15校の英語の要件を表で見る', 'IELTS・TOEFLの最低点と、IBの英語の成績やインターの学歴で満たせる条件', cls, head, rows)

def findings(n0):
    v = verified()
    i65 = sum(1 for d in v if d['ielts'].startswith('6.5'))
    t90 = [d for d in v if d['toefl'] and d['toefl'][:2].isdigit()]
    newok = [d for d in E if d['new'] and d['new'][0].isdigit()]
    c, n = counts()
    parts = [(k, INTER[k][0], c[k], INTER[k][1], INTER[k][2]) for k in ('S', 'Q', 'C')]
    viz1 = ('<figure class="vz"><figcaption><b>IELTSの最低点（オーストラリア・カナダ・シンガポール）</b><small>全学共通の基準。学部によって上がる場合があります</small></figcaption>'
            + AN.legend([('6.5（多くは各技能6.0以上）', '--vo2'), ('7.0以上', '--vo1')]) + '<div class="vz-rows">'
            + AN.seg_bar('IELTSの最低点', '公表している%d校' % len(v), [('a', '6.5', i65, '--vo2', 'k'), ('b', '7.0以上', len(v) - i65, '--vo1', 'w')], len(v)) + '</div></figure>')
    f1 = AN.finding(n0, 'オーストラリア・カナダ・シンガポールは、IELTS 6.5・TOEFL 90がほぼ共通の基準',
        '<p>公表している%d校のうち%d校が、IELTSの最低点を6.5（多くは各技能6.0以上）にしています。TOEFL（0〜120）も80〜93に収まり、中心は90です。'
        'イギリスやアメリカの上位校のように順位で大きく変わることはなく、学部による差の方が目立ちます。ニューサウスウェールズ大学は経営・法学を7.0、シンガポール経営大学は全学7.0（法学7.5）、マギル大学は経営のTOEFLを100にしています。'
        '2026年1月からの新しいTOEFL（1〜6）は、%d校が4.5〜5.0の基準を示す一方、ニューサウスウェールズ大学は当面受け付けていません</p>' % (len(v), i65, len(newok)), viz1)
    viz2 = ('<figure class="vz"><figcaption><b>日本のインター生は、英語試験が必要か</b><small>条件を確認できた%d校。国ごとの内訳は下の表を参照</small></figcaption>' % n
            + AN.legend([(INTER[k][0], INTER[k][1]) for k in ('S', 'Q', 'C')]) + '<div class="vz-rows">'
            + AN.seg_bar('全体', '条件を確認できた%d校' % n, parts, n) + '</div></figure>')
    f2 = AN.finding(n0 + 1, '日本のインター生の英語試験は、国ではなく大学ごとに扱いが分かれる',
        '<p>%d校中%d校は、国を問わず「英語で授業を行う学校で学んだこと」で英語の要件を満たせます（シドニー、ブリティッシュコロンビア、ウォータールーなど）。'
        'シンガポールの%d校は、英語試験を求めるのが指定された国の資格や英語以外で学ぶ資格の出願者で、IBやA Levelで出願する場合は原則として不要です。'
        '一方、マギル、トロント、メルボルン、オーストラリア国立大学の%d校は、学歴での免除を英語圏の国での在籍に限っており、日本のインターは対象外です。'
        'ただしマギルはIB English A 5以上、メルボルンはIB Englishで4以上、オーストラリア国立大学はEnglish Aの合格でも満たせるため、IBの英語の成績が英語試験の代わりになります</p>'
        % (n, c['S'], c['Q'], c['C']), viz2)
    return f1 + f2

def sources():
    return [(d['src'], '%s：英語の要件' % d['ja']) for d in E if d['src']]
