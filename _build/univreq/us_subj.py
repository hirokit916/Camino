# US: high-school course expectations by school/college (official admissions pages, checked 2026-11)
US_HS = [
 dict(uni='カリフォルニア工科大学（Caltech）', unit='全学', kind='必須', text='数学4年（微積分1年を含む）・物理1年・化学1年', src='https://www.admissions.caltech.edu/apply/first-year-applicants/academic-requirements-for-first-year-applicants'),
 dict(uni='コーネル大学', unit='工学部', kind='必須', text='数学4年（微積分を含む）・化学1年・物理1年', src='https://admissions.cornell.edu/apply/first-year-applicants/admission-requirements'),
 dict(uni='コーネル大学', unit='経営（Dyson）', kind='必須', text='数学4年（微積分を含む）・理科3年', src='https://admissions.cornell.edu/apply/first-year-applicants/admission-requirements'),
 dict(uni='コーネル大学', unit='文理学部', kind='必須', text='数学3年（プレカルキュラスまで）・理科3年（科目指定なし）', src='https://admissions.cornell.edu/apply/first-year-applicants/admission-requirements'),
 dict(uni='ミシガン大学', unit='工学部', kind='必須', text='数学4年（微積分を強く推奨）・理科3年（化学と物理は必須）', src='https://admissions.umich.edu/apply/first-year-applicants/college-preparation'),
 dict(uni='ミシガン大学', unit='経営（Ross）', kind='目安', text='数学4年・理科3年', src='https://admissions.umich.edu/apply/first-year-applicants/college-preparation'),
 dict(uni='ミシガン大学', unit='文理学部（LSA）', kind='目安', text='数学3年・理科3年', src='https://admissions.umich.edu/apply/first-year-applicants/college-preparation'),
 dict(uni='マサチューセッツ工科大学（MIT）', unit='全学', kind='推奨', text='微積分までの数学・物理・化学・生物', src='https://mitadmissions.org/apply/prepare/foundations/'),
 dict(uni='スタンフォード大学', unit='全学', kind='推奨', text='英語・数学（微積分を含む）各4年、歴史・理科・外国語各3年以上', src='https://admission.stanford.edu/apply/first-year/prepare.html'),
]
# UK: AP requirements (accepted-qualifications pages)
UK_AP = [
 dict(uni='ケンブリッジ大学', text='APで5点を5科目以上。数学・更なる数学が必要なコースはCalculus BC、物理が必要なコースはPhysics C（2科目）を推奨', src='https://www.undergraduate.study.cam.ac.uk/apply/before/accepted-qualifications'),
 dict(uni='インペリアル・カレッジ・ロンドン', text='AP 5科目で5,5,5,4,4以上。またはAP 3科目（5,5,4）＋高校卒業資格＋SAT 1460かACT 31', src='https://www.imperial.ac.uk/study/apply/undergraduate/entry-requirements/accepted-qualifications/'),
 dict(uni='LSE', text='AP 5科目以上（3年以内に受験）', src='https://www.lse.ac.uk/study-at-lse/undergraduate/entry-requirements'),
]

# ---- US top 50 (U.S. News 2027): application structure + HS course expectations
# apply: 'U' = apply to the university (major later), 'S' = choose a school/college at application, 'M' = some majors admit directly / limited
# eng_kind: '必須' required / '推奨' recommended / None not stated ; eng/gen: text for engineering / general applicants
US50 = {}
def us(en, **kw): US50[en] = kw
us('MIT', apply='U', eng_kind='推奨', eng='微積分までの数学・物理・化学・生物', gen='同左（必須科目なし）', src=['https://mitadmissions.org/apply/prepare/foundations/'])
us('Princeton University', apply='U', eng_kind='推奨', eng='工学（B.S.E.）：4年間の数学（できれば微積分）・物理・化学', gen='—', src=['https://engineering.princeton.edu/undergraduate-studies/admission-and-tours/high-school-guidance'])
us('Harvard University', apply='U', eng_kind='推奨', eng='—', gen='必須科目なし。数学4年・理科4年（生物・化学・物理と発展科目1つ）を推奨', src=['https://college.harvard.edu/resources/faq/are-there-secondary-school-course-requirements-admission'])
us('Yale University', apply='U', eng_kind=None, eng='—', gen='必須科目なし。英語・理科・数学・社会・外国語を毎年履修することを推奨', src=['https://admissions.yale.edu/course-selection'])
us('California Institute of Technology', apply='U', eng_kind='必須', eng='全員：数学4年（微積分1年を含む）・物理1年・化学1年', gen='同左', src=['https://www.admissions.caltech.edu/apply/first-year-applicants/academic-requirements-for-first-year-applicants'])
us('Stanford University', apply='U', eng_kind='推奨', eng='—', gen='英語・数学（微積分を含む）各4年、歴史・理科・外国語各3年以上を推奨', src=['https://admission.stanford.edu/apply/first-year/prepare.html'])
us('University of Pennsylvania', apply='S', eng_kind='推奨', eng='工学部：物理と数学（特に微積分）', gen='文理：科目指定なし／ウォートン（経営）：微積分を含む数学／看護：化学・生物', src=['https://admissions.upenn.edu/how-to-apply/preparing-your-application/academics'])
us('Cornell University', apply='S', eng_kind='必須', eng='工学部：数学4年（微積分を含む）・化学1年・物理1年', gen='文理：数学3年・理科3年／経営（Dyson）：微積分を含む数学4年・理科3年', src=['https://admissions.cornell.edu/apply/first-year-applicants/admission-requirements'])
us('University of Michigan–Ann Arbor', apply='S', eng_kind='必須', eng='工学部：数学4年（微積分を強く推奨）・理科3年（化学と物理は必須）', gen='文理（LSA）：数学3年・理科3年／経営（Ross）：数学4年・理科3年', src=['https://admissions.umich.edu/apply/first-year-applicants/college-preparation'])
us('Duke University', apply='S', eng_kind='必須', eng='工学部（Pratt）：微積分は必須、物理を強く推奨', gen='英語4年、数学・理科・外国語・社会各3年以上を推奨', src=['https://admissions.duke.edu/college-prep/'])
us('Johns Hopkins University', apply=None, eng_kind='推奨', eng='—', gen='必須科目なし。数学と実験を伴う理科（微積分・物理・化学など）各4年を推奨', src=['https://apply.jhu.edu/college-planning-guide/preparing-for-college/'])
us('Northwestern University', apply='S', eng_kind='推奨', eng='工学部（McCormick）：数学3.5〜4年（微積分が望ましい）・実験を伴う理科3年（化学・物理が望ましい）', gen='文理など：数学3年・実験を伴う理科2年以上', src=['https://admissions.northwestern.edu/faqs/high-school-courses/'])
us('Columbia University', apply='S', eng_kind='推奨', eng='工学部：物理と微積分', gen='コロンビア・カレッジ：科目指定なし', src=['https://undergrad.admissions.columbia.edu/apply/process'])
us('Carnegie Mellon University', apply='S', eng_kind='必須', eng='工学部：数学4年（微積分を強く推奨）・化学・物理・生物各1年／CS：数学4年・物理1年・化学か生物かCS 2年', gen='人文社会：数学3年・理科1年／経営（Tepper）：数学4年・化学・物理・生物各1年', src=['https://www.cmu.edu/admission/admission/academic-requirements-college-level-work'])
us('Dartmouth College', apply='U', eng_kind='推奨', eng='工学：理科4年（物理を含む）', gen='数学4年（理系は微積分まで）・実験を伴う理科3年を推奨', src=['https://admissions.dartmouth.edu/glossary-question/does-dartmouth-require-specific-high-school-courses'])
us('Rice University', apply=None, eng_kind='必須', eng='工学・自然科学：少なくとも三角法かプレカルキュラス、化学と物理（化学か生物の2年目で物理の代替可）', gen='全員：数学3年・実験を伴う理科2年以上', src=['https://ga.rice.edu/undergraduate-students/academic-policies-procedures/admission/'])
us('Vanderbilt University', apply='S', eng_kind='推奨', eng='工学部：微積分・微積分を使う物理・化学を強く推奨', gen='数学・理科各4年を推奨', src=['https://admissions.vanderbilt.edu/apply/expert-advice/'])
UC_AG = 'https://admission.universityofcalifornia.edu/admission-requirements/first-year-requirements/subject-requirement-a-g.html'
UC_GEN = 'UC共通（A-G）：数学3年（4年目を強く推奨）・理科2年（生物・化学・物理から2分野、3年目を推奨）'
us('University of California, Berkeley', apply='M', eng_kind='推奨', eng='工学部：数学4年（3年が最低）と物理（希望の専攻を選んで出願、工学部内の転専攻は難しい）', gen=UC_GEN, src=['https://engineering.berkeley.edu/admissions/undergraduate-admissions/prospective-freshman-faqs/', UC_AG])
us('University of California, Los Angeles', apply='M', eng_kind='推奨', eng='工学部：専攻（または工学部未定）を選んで出願。微積分かプレカルキュラスまでの数学を強く推奨', gen=UC_GEN, src=['https://www.seasoasa.ucla.edu/curric-24-25/13-ugprg-admis-24.html', UC_AG])
us('University of California, San Diego', apply='M', eng_kind=None, eng='CS・工学系・データサイエンスなどは「選抜専攻」（入学時に専攻の選抜あり）', gen=UC_GEN, src=['https://undergrad.ucsd.edu/academics/selective-major-process/selective-major-guidance.html', UC_AG])
us('University of Notre Dame', apply='U', eng_kind='必須', eng='工学：数学4年（プレカルキュラスか微積分まで）・化学・物理', gen='数学3年以上（4年が望ましい）・理科2年以上（4年が望ましい）', src=['https://admissions.nd.edu/apply/faqs/'])
us('Georgetown University', apply='S', eng_kind=None, eng='（工学部なし）', gen='経営（McDonough）：三角法までの数学3年・理科2年を推奨／看護・健康：数学3年・生物・化学各1年は必須', src=['https://bulletin.georgetown.edu/admissions/undergraduate-admissions/'])
us('University of North Carolina at Chapel Hill', apply=None, eng_kind=None, eng='—', gen='最低条件：数学4単位（代数2・幾何1・代数II以上の科目1）・理科3単位（生物系・物理系・実験各1）', src=['https://admissions.unc.edu/faqs/what-are-the-minimum-course-requirements-for-admission-to-carolina/'])
us('University of Southern California', apply=None, eng_kind='必須', eng='工学部（Viterbi）：数学4年（最終学年までに微積分が望ましい）・理科3年', gen='—', src=['https://esdcomm.usc.edu/uga/firstyear/prospective/viterbi.html'])
us('Georgia Institute of Technology', apply=None, eng_kind='必須', eng='全員：数学4単位・理科4単位', gen='同左', src=['https://admission.gatech.edu/first-year/academic-preparation'])
us('New York University', apply='S', eng_kind='推奨', eng='工学部（Tandon）：物理・化学・微積分（少なくともプレカルキュラス）', gen='経営（Stern）：微積分（少なくともプレカルキュラス）', src=['https://www.nyu.edu/admissions/undergraduate-admissions/how-to-apply/all-freshmen-applicants/additional-program-requirements.html'])
us('Tufts University', apply='U', eng_kind='推奨', eng='工学部：数学・理科各4年、物理と微積分を強く推奨（出願手続きは全学共通）', gen='—', src=['https://admissions.tufts.edu/apply/applying-to-tufts/school-of-engineering/'])
us('Boston University', apply='S', eng_kind='必須', eng='工学部：微積分1年は必須', gen='数学・実験を伴う理科各3〜4年を推奨／経営（Questrom）：微積分（またはプレカルキュラス＋AP統計）は必須', src=['https://www.bu.edu/admissions/apply/first-year/'])
us('University of Illinois Urbana-Champaign', apply=None, eng_kind='必須', eng='工学部（Grainger）全専攻：数学3.5年以上（三角法以上を含む）', gen='全員：数学3〜3.5年（4年を推奨）・実験を伴う理科2年（4年を推奨）／経営（Gies）：数学3.5年以上', src=['https://www.admissions.illinois.edu/first-year-requirements/'])
us('University of Texas at Austin', apply=None, eng_kind='必須', eng='工学部：出願時に微積分に進める段階まで数学を履修していること', gen='数学3単位（4を推奨）・理科2単位（4を推奨、生物・物理・化学が望ましい）', src=['https://admissions.utexas.edu/apply/application-materials/high-school-prerequisites/'])
us('University of Wisconsin–Madison', apply='M', eng_kind=None, eng='—', gen='数学3年・理科3年（出願時に第1・第2志望の専攻を選ぶ）', src=['https://admissions.wisc.edu/apply-as-a-freshman/'])
us('University of Florida', apply=None, eng_kind=None, eng='—', gen='数学4年（代数I以上）・理科3年（うち2年は実験付き）', src=['https://admissions.ufl.edu/apply/freshman/requirements'])
us('Wake Forest University', apply=None, eng_kind=None, eng='—', gen='数学3単位・理科1単位以上', src=['https://bulletin.wfu.edu/undergraduate/procedures/admission/'])
us('Northeastern University', apply='S', eng_kind='必須', eng='工学部：物理・化学・プレカルキュラス（数学・理科各3年以上）', gen='—', src=['https://coe.northeastern.edu/academics-experiential-learning/undergraduate-studies/undergraduate-admission-aid/'])
us('Case Western Reserve University', apply=None, eng_kind='推奨', eng='工学・理学：数学と実験を伴う理科をもう1年ずつ', gen='数学3年・理科3年（うち実験2年）', src=['https://case.edu/admission/apply/deadlines-and-requirements'])
us('Ohio State University', apply='M', eng_kind=None, eng='工学部：出願時に工学の専攻を選ぶ', gen='—', src=['https://engineering.osu.edu/undergraduate/future-students/admissions/new-students'])
us('University of Maryland, College Park', apply='M', eng_kind=None, eng='工学部は定員制（LEP）。航空宇宙・コンピュータ・電気・機械は入学時の直接選抜（定員に達すると一般工学に配属）', gen='—', src=['https://eng.umd.edu/freshmen-applicants/prepare'])
us('Villanova University', apply='S', eng_kind='必須', eng='工学部：物理とプレカルキュラスは必須、微積分を強く推奨', gen='経営（VSB）：数学4年（微積分があれば）は必須／看護：生物・化学各1年は必須', src=['https://www.villanova.edu/university/undergraduate-admission/applying-to-villanova/first-year-applicants.html'])
us('Lehigh University', apply='S', eng_kind='推奨', eng='工学部：微積分を含む数学を推奨', gen='最低：数学3・実験を伴う理科2（数学4・理科3を推奨）／経営：微積分を推奨', src=['https://catalog.lehigh.edu/informationofgeneralinterest/admissionanddeposit/'])
for _en in ('University of California, Davis', 'University of California, Irvine', 'University of California, Santa Barbara'):
    us(_en, apply=None, eng_kind=None, eng='—', gen=UC_GEN, src=[UC_AG])
us('University of Washington', apply='M', eng_kind=None, eng='CS・コンピュータ工学・工学の各専攻・経営は、入学時に専攻へ直接入学。入学後に移るのは非常に難しい', gen='—', src=['https://admit.washington.edu/apply/admission-to-majors/'])
us('Rutgers University–New Brunswick', apply='S', eng_kind='必須', eng='工学部：数学4年（プレカルキュラス以上）・物理1年・化学1年', gen='—', src=['https://soe.rutgers.edu/admissions-and-aid/undergraduate-admissions/undergraduate-admissions-requirements'])
us('Washington University in St. Louis', apply='S', eng_kind=None, eng='—', gen='出願時に文理・工学・経営・美術・建築から一つを選ぶ', src=['https://admissions.washu.edu/how-to-apply/common-questions/'])
