# -*- coding: utf-8 -*-
"""Australia / Canada / Singapore top 5 x 12 majors (official pages, checked 2026-11).
fields: course, ib (int score or None), al (UK A level grade string or None), req (Japanese text; None=unverified), note, src
course: NA = not offered at undergraduate level for school leavers; None = unverified."""
NA = 'NA'
C = {}   # (country, uni) -> list of majors
S = {}
def add(cty, uni, m, **kw): S[(cty, uni, m)] = kw
UNI = {
 'AU': [('UNSW', 'ニューサウスウェールズ大学'), ('Melbourne', 'メルボルン大学'), ('Sydney', 'シドニー大学'), ('ANU', 'オーストラリア国立大学'), ('Monash', 'モナシュ大学')],
 'CA': [('McGill', 'マギル大学'), ('Toronto', 'トロント大学'), ('UBC', 'ブリティッシュコロンビア大学'), ('Alberta', 'アルバータ大学'), ('Waterloo', 'ウォータールー大学')],
 'SG': [('NUS', 'シンガポール国立大学'), ('NTU', '南洋理工大学'), ('SMU', 'シンガポール経営大学'), ('SUTD', 'シンガポール工科デザイン大学'), ('SIT', 'シンガポール工科大学')],
}
RANK_SRC = {'AU': 'https://www.topuniversities.com/university-rankings-articles/world-university-rankings/top-universities-australia',
            'CA': 'https://academica.ca/top-ten/qs-world-university-rankings-2027-released/'}
QS = {'UNSW': 19, 'Melbourne': 22, 'Sydney': 28, 'ANU': 29, 'Monash': 31, 'McGill': 30, 'Toronto': 32, 'UBC': 45, 'Alberta': 96, 'Waterloo': 113}
MAJ = ['MED','CS','ENG','MATH','PHYS','BIO','ECON','BUS','LAW','PSY','HIST','ENGL']

# ---------- Australia ----------
UNSW = 'https://www.unsw.edu.au/content/dam/pdfs/future-students/2027-int-ug-entry-table.pdf'
# UNSW A level: aggregate of 3 subjects, A*=6 A=5 B=4 C=3 -> 17=A*A*A, 15=AAA, 13=ABB, 12=BBB, 10=BCC
add('AU','UNSW','MED', course='Medical Studies / Doctor of Medicine', ib=40, al='A*A*A', req=None, test='UCAT ANZ・面接', src=[UNSW])
add('AU','UNSW','CS', course='B Science (Computer Science)', ib=34, al='BBB', req=None, src=[UNSW])
add('AU','UNSW','ENG', course='B Engineering (Hons)', ib=35, al='ABB', req=None, src=[UNSW])
add('AU','UNSW','MATH', course='B Science (Advanced Mathematics) (Hons)', ib=34, al='BBB', req=None, src=[UNSW])
add('AU','UNSW','PHYS', course='B Advanced Science (Hons)', ib=34, al='BBB', req=None, src=[UNSW])
add('AU','UNSW','BIO', course='B Science', ib=29, al='BCC', req=None, src=[UNSW])
add('AU','UNSW','ECON', course='B Economics', ib=33, al=None, req=None, src=[UNSW])
add('AU','UNSW','BUS', course='B Commerce', ib=36, al='AAA', req=None, src=[UNSW])
add('AU','UNSW','LAW', course='B Combined Law', ib=36, al='AAA', req=None, src=[UNSW])
add('AU','UNSW','PSY', course='B Psychology (Hons)', ib=36, al='AAA', req=None, src=[UNSW])
add('AU','UNSW','HIST', course='B Arts', ib=29, al='BCC', req=None, src=[UNSW])
add('AU','UNSW','ENGL', course='B Arts', ib=29, al='BCC', req=None, src=[UNSW])
SY = 'https://www.sydney.edu.au/dam/corporate/documents/study/guides/usyd-international-guide.pdf'
add('AU','Sydney','MED', course='B Science / Doctor of Medicine', ib=45, al=None, req='数学（Advanced）を前提。ほかの選考あり', src=[SY])
add('AU','Sydney','CS', course='B Advanced Computing', ib=34, al=None, req='数学（Extension 1相当）', src=[SY])
add('AU','Sydney','ENG', course='B Engineering Honours', ib=31, al=None, req='数学（Extension 1相当）、物理を推奨', src=[SY])
add('AU','Sydney','MATH', course='B Mathematical Sciences', ib=34, al=None, req='数学（Advanced）が必須', src=[SY])
add('AU','Sydney','PHYS', course='B Science', ib=29, al=None, req='数学（Advanced）を前提', src=[SY])
add('AU','Sydney','BIO', course='B Science', ib=29, al=None, req='数学（Advanced）を前提', src=[SY])
add('AU','Sydney','ECON', course='B Economics', ib=31, al=None, req='数学（Advanced）を前提', src=[SY])
add('AU','Sydney','BUS', course='B Commerce', ib=38, al=None, req='数学（Standard以上）を前提', src=[SY])
add('AU','Sydney','LAW', course='Combined Laws (B Arts / B Laws など)', ib=38, al=None, req='英語（Advanced）を前提', src=[SY])
add('AU','Sydney','PSY', course='B Psychology', ib=29, al=None, req='数学（Advanced）を前提', src=[SY])
add('AU','Sydney','HIST', course='B Arts', ib=26, al=None, req='指定なし', src=[SY])
add('AU','Sydney','ENGL', course='B Arts', ib=26, al=None, req='指定なし', src=[SY])
ME = 'https://study.unimelb.edu.au/how-to-apply/undergraduate-study/recognised-vce-equivalent-qualifications/qualifications/general-international-qualifications-international-baccalaureate-ib-diploma'
MEP = ['https://study.unimelb.edu.au/find/pathways/doctor/', 'https://study.unimelb.edu.au/find/pathways/lawyer/']
add('AU','Melbourne','MED', course=NA, note='医学は大学院（Doctor of Medicine）', src=MEP[:1])
add('AU','Melbourne','LAW', course=NA, note='法学は大学院（Juris Doctor）', src=MEP[1:])
for m in ('CS','ENG','MATH','PHYS','BIO'):
    add('AU','Melbourne',m, course='Bachelor of Science' + ('（工学は大学院で）' if m=='ENG' else ''), ib=31, al=None, req='数学（AA SL以上かAI HL）4以上＋生物・化学・物理のいずれか4以上', note='2026年入学の保証点', src=[ME])
add('AU','Melbourne','ECON', course='Bachelor of Commerce', ib=35, al=None, req='数学（AA SL以上かAI HL）4以上', note='2026年入学の保証点', src=[ME])
add('AU','Melbourne','BUS', course='Bachelor of Commerce', ib=35, al=None, req='数学（AA SL以上かAI HL）4以上', note='2026年入学の保証点', src=[ME])
for m in ('PSY','HIST','ENGL'):
    add('AU','Melbourne',m, course='Bachelor of Arts', ib=30, al=None, req='指定なし（英語のみ）', note='2026年入学の保証点', src=[ME])
ANU1 = 'https://programsandcourses.anu.edu.au/2026/program/AENGI'
add('AU','ANU','ENG', course='B Engineering (Honours)', ib=33, al=None, req='数学（AA・AI、SL以上）', src=[ANU1])
add('AU','ANU','CS', course='B Advanced Computing (Honours)', ib=33, al=None, req='数学（AA SL以上かAI HL）', src=['https://programsandcourses.anu.edu.au/program/AACOM-BCOMM'])
add('AU','ANU','PSY', course='B Science (Psychology)', ib=33, al=None, req='数学（AA・AI）', src=['https://programsandcourses.anu.edu.au/program/aacom-bspsy'])
for m in ('MED','MATH','PHYS','BIO','ECON','BUS','LAW','HIST','ENGL'): add('AU','ANU',m, course=None)
MO = 'https://www.monash.edu/__data/assets/pdf_file/0006/3936426/undergraduate-domestic-course-guide.pdf'
MON = 'オーストラリア国内で受けたIBの目安（2026年の最低選抜点）'
add('AU','Monash','MED', course='Medical Science and Doctor of Medicine', ib=None, al=None, req='英語・化学（SL5かHL4以上）', note=MON, src=[MO])
add('AU','Monash','CS', course='B Computer Science', ib=30, al=None, req='数学（レベル3）', note=MON, src=[MO])
add('AU','Monash','ENG', course='B Engineering (Honours)', ib=33, al=None, req='数学（レベル3）＋生物・化学・物理のいずれか', note=MON, src=[MO])
for m in ('MATH','PHYS','BIO'):
    add('AU','Monash',m, course='B Science', ib=31, al=None, req='理系科目1つ（SL4かHL3以上）', note=MON, src=[MO])
add('AU','Monash','ECON', course='B Commerce', ib=34, al=None, req='数学（レベル3）', note=MON, src=[MO])
add('AU','Monash','BUS', course='B Commerce', ib=34, al=None, req='数学（レベル3）', note=MON, src=[MO])
add('AU','Monash','LAW', course='B Laws (Honours)', ib=39, al=None, req='英語（レベル2）', note=MON, src=[MO])
add('AU','Monash','PSY', course='B Psychology', ib=34, al=None, req='指定なし（英語のみ）', note=MON, src=[MO])
add('AU','Monash','HIST', course='B Arts', ib=28, al=None, req='指定なし（英語のみ）', note=MON, src=[MO])
add('AU','Monash','ENGL', course='B Arts', ib=28, al=None, req='指定なし（英語のみ）', note=MON, src=[MO])

# ---------- Canada ----------
MG = 'https://www.mcgill.ca/undergraduate-admissions/apply/requirements/international/ib'
MGA = 'https://www.mcgill.ca/undergraduate-admissions/apply/requirements/international/advanced-levels'
add('CA','McGill','MED', course=None); add('CA','McGill','LAW', course=None)
add('CA','McGill','ENG', course='Engineering', ib=38, al='A*A*A*〜BBB（専攻による）', req='数学・化学・物理（うち1つ以上HL）', note='IB 38〜42点', src=[MG, MGA])
for m in ('CS','MATH','PHYS'):
    add('CA','McGill',m, course='Science（物理・数学・CS系）', ib=35, al='A*AA〜ABB', req='数学＋生物・化学・物理から2科目（うち1つ以上HL）', note='IB 35〜38点', src=[MG, MGA])
add('CA','McGill','BIO', course='Science（生物・医学系）', ib=36, al='A*AA〜ABB', req='数学＋生物・化学・物理から2科目（うち1つ以上HL）', note='IB 36〜39点', src=[MG, MGA])
add('CA','McGill','BUS', course='Management', ib=35, al='A*AA〜AAB', req='数学（HL、またはSLのAAで6以上）', note='IB 35〜38点', src=[MG, MGA])
for m in ('ECON','PSY','HIST','ENGL'):
    add('CA','McGill',m, course='Arts', ib=33, al='AAA〜ABB', req='指定なし', note='IB 33〜36点', src=[MG, MGA])
WA = 'https://uwaterloo.ca/future-students/admissions/admission-requirements/'
add('CA','Waterloo','CS', course='Computer Science', ib=32, al=None, req='数学AA HL（6以上）', note='最低点', src=[WA+'computer-science/high-school/international-system/ib'])
add('CA','Waterloo','MATH', course='Mathematics', ib=30, al=None, req='数学AA HL（6以上）', note='最低点', src=[WA+'mathematics/high-school/international-system/ib'])
add('CA','Waterloo','ENG', course='Mechanical Engineering', ib=None, al=None, req='数学AA・物理・化学（数学・物理はHLを推奨）', src=['https://uwaterloo.ca/engineering/future-students/applying/admission-requirements'])
for m in ('MED','PHYS','BIO','ECON','BUS','LAW','PSY','HIST','ENGL'): add('CA','Waterloo',m, course=None)
add('CA','UBC','ENG', course='Applied Science (Engineering)', ib=None, al=None, req='数学（AA SL以上かAI HL）・化学・物理', src=['https://you.ubc.ca/programs/integrated-engineering/'])
add('CA','UBC','BUS', course='Commerce', ib=None, al=None, req='数学（AA SL以上かAI HL）', src=['https://you.ubc.ca/programs/commerce/'])
for m in ('MED','CS','MATH','PHYS','BIO','ECON','LAW','PSY','HIST','ENGL'): add('CA','UBC',m, course=None)
AL = 'https://www.ualberta.ca/en/admissions/media-library/uai-assets/docs/undergraduateprogramsubjectrequirements.pdf'
add('CA','Alberta','ENG', course='Engineering', ib=None, al=None, req='数学・微積分・化学・物理', src=[AL])
for m in ('CS','MATH','PHYS','BIO'):
    add('CA','Alberta',m, course='Science', ib=None, al=None, req='数学＋生物・微積分・化学・物理から2科目', src=[AL])
add('CA','Alberta','ECON', course='Arts (Economics)', ib=None, al=None, req='数学（専攻に必要）', src=[AL])
add('CA','Alberta','PSY', course='Arts (Psychology)', ib=None, al=None, req='数学（専攻に必要）', src=[AL])
add('CA','Alberta','HIST', course='Arts', ib=None, al=None, req='指定なし', src=[AL])
add('CA','Alberta','ENGL', course='Arts', ib=None, al=None, req='指定なし', src=[AL])
for m in ('MED','BUS','LAW'): add('CA','Alberta',m, course=None)
for m in MAJ: add('CA','Toronto',m, course=None)

# ---------- Singapore ----------
NUS = 'https://www.nus.edu.sg/oam/docs/default-source/default-document-library/ibdp-sp.pdf?sfvrsn=4a0b7c43_8'
add('SG','NUS','MED', course='Medicine', ib=None, al=None, req='化学HL＋生物か物理のHL', test='UCAT・面接', src=[NUS])
add('SG','NUS','CS', course='Computer Science', ib=None, al=None, req='CS・数学AA・物理のいずれかHL（またはAA SL・AI HLで良好な成績）', src=[NUS])
add('SG','NUS','ENG', course='Engineering', ib=None, al=None, req='数学AA HL', src=[NUS])
add('SG','NUS','BUS', course='Business Administration', ib=None, al=None, req='数学（AA HL・AA SL・AI HLのいずれか）', src=[NUS])
add('SG','NUS','LAW', course='Law', ib=None, al=None, req='英語（SL/HL）5以上', test='面接', src=[NUS])
for m in ('MATH','PHYS','BIO','ECON','PSY','HIST','ENGL'): add('SG','NUS',m, course=None)
for u in ('NTU','SMU','SUTD','SIT'):
    for m in MAJ: add('SG',u,m, course=None)
NTU = 'https://www.ntu.edu.sg/docs/default-source/undergraduate-admissions/ibdiploma/emsr_ib.pdf?sfvrsn=2f837fcc_1'
for m, r in [('MED','化学HL＋生物か物理のHL'), ('CS','数学・物理・CSのいずれかHL'), ('ENG','数学HL＋物理・化学・生物・CSのいずれかHL'), ('MATH','数学HL'),
             ('PHYS','物理HL＋数学HL'), ('BIO','数学SL＋物理・化学・生物のいずれかHL'), ('ECON','数学SL・英語SLで良好な成績'), ('BUS','数学SL・英語SLで良好な成績'),
             ('PSY','数学SL・英語SLで良好な成績'), ('ENGL','英語SLで良好な成績')]:
    add('SG','NTU',m, course=m, ib=None, al=None, req=r, src=[NTU])
SMU = 'https://admissions.smu.edu.sg/admissions-requirements/ib-diploma'
add('SG','SMU','BUS', course='Business', ib=None, al=None, req='指定なし', src=[SMU])
add('SG','SMU','ECON', course='Economics', ib=None, al=None, req='数学（HLかSL）で良好な成績', src=[SMU])
add('SG','SMU','LAW', course='Law', ib=None, al=None, req='英語A（HLかSL）6以上', src=[SMU])
TO = 'https://discover.engineering.utoronto.ca/how-to-apply/outofcanada/'
add('CA','Toronto','ENG', course='Engineering', ib=30, al=None, req='数学（AA HLを強く推奨）・化学・物理', note='最低（予測点）', src=[TO])
