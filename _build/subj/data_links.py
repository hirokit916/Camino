# -*- coding: utf-8 -*-
"""Official page + PDF for every subject page (found via search on 2026-11-14). key = page path.
Each value: list of (label, url, kind) — kind 'page' | 'pdf' | 'pdf-ja'."""
IBP = 'https://ibo.org/programmes/diploma-programme/curriculum/'
IBG = 'https://www.ibo.org/globalassets/new-structure/'
CIP = 'https://www.cambridgeinternational.org/programmes-and-qualifications/'
APC = 'https://apcentral.collegeboard.org/courses/'
APM = 'https://apcentral.collegeboard.org/media/pdf/'

L = {}
# ---------------- IB DP
def ib(slug, page, pdfs):
    L['/subjects/ib/%s/' % slug] = [('国際バカロレア機構（IB）', page, 'page')] + pdfs
ib('mathematics-analysis-and-approaches', IBP + 'mathematics/', [('Subject brief', IBG + 'programmes/dp/pdfs/sb_maths_analysis_en.pdf', 'pdf'), ('Subject guide', IBG + 'university-admission/pdfs/dp-mathematics-analysis-and-approaches-guide-en.pdf', 'pdf')])
ib('mathematics-applications-and-interpretation', IBP + 'mathematics/', [('Subject brief', IBG + 'programmes/dp/pdfs/sb_maths_application_en.pdf', 'pdf'), ('Subject guide', 'https://ibo.org/globalassets/new-structure/university-admission/pdfs/dp-mathematics-applications-and-interpretation-guide-en.pdf', 'pdf')])
ib('physics', IBP + 'sciences/physics/', [('Subject brief', 'https://ibo.org/globalassets/new-structure/recognition/pdfs/dp_sciences_physics_subject-brief_jan_2022_e.pdf', 'pdf')])
ib('chemistry', IBP + 'sciences/chemistry/', [('Subject brief', IBG + 'recognition/pdfs/dp_sciences_chemistry_subject-brief_jan_2022_e.pdf', 'pdf')])
ib('biology', 'https://www.ibo.org/programmes/diploma-programme/curriculum/sciences/biology/', [('Subject brief', IBG + 'recognition/pdfs/dp_sciences_biology_subject-brief_jan_2022_e.pdf', 'pdf')])
ib('environmental-systems-and-societies', IBP + 'sciences/environmental-systems-and-societies/', [('Subject brief', 'https://ibo.org/globalassets/new-structure/university-admission/pdfs/environmental-systems-and-societies-en.pdf', 'pdf'), ('Subject guide', 'https://ibo.org/globalassets/new-structure/university-admission/pdfs/subject-guides/environmental-systems-societies-guide.pdf', 'pdf')])
ib('computer-science', IBP + 'sciences/computer-science/', [('Subject brief', IBG + 'university-admission/pdfs/dp_comp_sci_subjectbrief_en.pdf', 'pdf')])
ib('english-a-language-and-literature', IBP + 'language-and-literature/language-a-language-and-literature/', [])
ib('english-a-literature', IBP + 'language-and-literature/language-a-literature/', [('Subject guide', 'https://ibo.org/globalassets/new-structure/university-admission/pdfs/subject-guides/language-a-literature-guide.pdf', 'pdf')])
ib('japanese-a', IBP + 'language-and-literature/language-a-language-and-literature/', [('Language A: literature の公式ページ', IBP + 'language-and-literature/language-a-literature/', 'page'), ('Subject guide（literature）', 'https://ibo.org/globalassets/new-structure/university-admission/pdfs/subject-guides/language-a-literature-guide.pdf', 'pdf')])
ib('english-b', IBP + 'language-acquisition/language-b/', [('2029年からの変更', 'https://ibo.org/university-admission/latest-curriculum-updates/language-b-updates/', 'page')])
ib('japanese-b', IBP + 'language-acquisition/language-b/', [('2029年からの変更', 'https://ibo.org/university-admission/latest-curriculum-updates/language-b-updates/', 'page')])
ib('economics', 'https://www.ibo.org/en/programmes/diploma-programme/curriculum/individuals-and-societies/economics/', [('Subject brief（HL）', 'https://ibo.org/globalassets/new-structure/programmes/dp/pdfs/hl-economics-en.pdf', 'pdf')])
ib('business-management', IBP + 'individuals-and-societies/business-and-management/', [])
ib('history', IBP + 'individuals-and-societies/history/', [('Subject brief', 'https://ibo.org/globalassets/new-structure/programmes/dp/pdfs/dp-history-sb-en.pdf', 'pdf'), ('2028年からの変更', 'https://ibo.org/university-admission/latest-curriculum-updates/history-updates/', 'page')])
ib('geography', IBP + 'individuals-and-societies/geography/', [])
ib('psychology', IBP + 'individuals-and-societies/psychology/', [('Subject brief', 'https://ibo.org/globalassets/new-structure/programmes/dp/pdfs/dp_psychology_subjectbrief_en.pdf', 'pdf'), ('Subject guide', 'https://ibo.org/globalassets/new-structure/university-admission/pdfs/subject-guides/psychology-first-assessment-2027-guide-sbs.pdf', 'pdf')])
ib('global-politics', IBP + 'individuals-and-societies/global-politics/', [('Subject brief', IBG + 'university-admission/pdfs/global-politics-sl-hl-subject-brief-en.pdf', 'pdf')])

# ---------------- Cambridge (page slug on cambridgeinternational.org; syllabus PDF comes from the subject data)
CAM_PAGE = {
 'igcse/mathematics-0580': 'cambridge-igcse-mathematics-0580', 'igcse/additional-mathematics-0606': 'cambridge-igcse-mathematics-additional-0606',
 'igcse/physics-0625': 'cambridge-igcse-physics-0625', 'igcse/chemistry-0620': 'cambridge-igcse-chemistry-0620', 'igcse/biology-0610': 'cambridge-igcse-biology-0610',
 'igcse/co-ordinated-sciences-0654': 'cambridge-igcse-sciences-co-ordinated-double-0654', 'igcse/combined-science-0653': 'cambridge-igcse-science-combined-0653',
 'igcse/first-language-english-0500': 'cambridge-igcse-english-first-language-0500', 'igcse/literature-in-english-0475': 'english-literature-0475',
 'igcse/economics-0455': 'cambridge-igcse-economics-0455', 'igcse/business-0264': 'cambridge-igcse-business-0264', 'igcse/computer-science-0478': 'cambridge-igcse-computer-science-0478',
 'igcse/geography-0460': 'cambridge-igcse-geography-0460', 'igcse/history-0470': 'cambridge-igcse-history-0470',
 'a-level/mathematics-9709': 'cambridge-international-as-and-a-level-mathematics-9709', 'a-level/further-mathematics-9231': 'cambridge-international-as-and-a-level-mathematics-further-9231',
 'a-level/physics-9702': 'cambridge-international-as-and-a-level-physics-9702', 'a-level/chemistry-9701': 'cambridge-international-as-and-a-level-chemistry-9701',
 'a-level/biology-9700': 'cambridge-international-as-and-a-level-biology-9700', 'a-level/economics-9708': 'cambridge-international-as-and-a-level-economics-9708',
 'a-level/business-9609': 'cambridge-international-as-and-a-level-business-9609', 'a-level/computer-science-9618': 'cambridge-international-as-and-a-level-computer-science-9618',
 'a-level/english-language-9093': 'cambridge-international-as-and-a-level-english-language-9093', 'a-level/literature-in-english-9695': 'cambridge-international-as-and-a-level-english-literature-9695',
 'a-level/psychology-9990': 'cambridge-international-as-and-a-level-psychology-9990', 'a-level/geography-9696': 'cambridge-international-as-and-a-level-geography-9696',
 'a-level/history-9489': 'cambridge-international-as-and-a-level-history-9489',
}
CAM_JA = {  # Cambridge's own Japanese-language subject overviews
 'a-level/mathematics-9709': 'https://www.cambridgeinternational.org/jp/Images/765253-jp-cambridge-international-as-a-level-subject-mathematics-9709.pdf',
 'a-level/english-language-9093': 'https://www.cambridgeinternational.org/jp/Images/765251-jp-cambridge-international-as-a-level-subject-english-language-9093.pdf',
 'a-level/literature-in-english-9695': 'https://www.cambridgeinternational.org/jp/Images/765252-jp-cambridge-international-as-a-level-subject-literature-in-english-9695.pdf',
}
CAM_EXTRA = {
 'igcse/business-0264': [('0450と0264の違い（Cambridge）', 'https://help.cambridgeinternational.org/hc/en-gb/articles/37827932437010-What-is-the-difference-between-IGCSE-Business-Studies-0450-and-IGCSE-Business-0264', 'page'),
                         ('Syllabus update 2027–2029', 'https://www.cambridgeinternational.org/Images/730913-2027-2029-syllabus-update.pdf', 'pdf')],
 'igcse/combined-science-0653': [('Combined と Co-ordinated の違い（Cambridge）', 'https://help.cambridgeinternational.org/hc/en-gb/articles/23172961927698-What-is-the-difference-between-the-IGCSEs-in-Combined-Science-and-Coordinated-Science', 'page')],
 'igcse/co-ordinated-sciences-0654': [('Combined と Co-ordinated の違い（Cambridge）', 'https://help.cambridgeinternational.org/hc/en-gb/articles/23172961927698-What-is-the-difference-between-the-IGCSEs-in-Combined-Science-and-Coordinated-Science', 'page')],
}
LS_PAGE = {'science-0893': 'science/', 'mathematics-0862': 'mathematics/', 'english-0861': 'english/'}
for k, v in LS_PAGE.items():
    L['/subjects/lower-secondary/%s/' % k] = [('Cambridge International', CIP + 'cambridge-lower-secondary/curriculum/' + v, 'page'),
                                              ('Checkpoint 時間割（2027年3月）', 'https://www.cambridgeinternational.org/Images/760914-march-2027-checkpoint-final-timetable.pdf', 'pdf')]
L['/subjects/myp/sciences/'] = [('国際バカロレア機構（IB）', 'https://ibo.org/programmes/middle-years-programme/curriculum/science/', 'page'),
                                ('Subject brief', 'https://www.ibo.org/globalassets/new-structure/brochures-and-infographics/pdfs/myp-brief-sciences-en.pdf', 'pdf')]
L['/subjects/myp/mathematics/'] = [('国際バカロレア機構（IB）', 'https://ibo.org/programmes/middle-years-programme/curriculum/mathematics/', 'page'),
                                   ('Subject brief', 'https://www.ibo.org/globalassets/new-structure/brochures-and-infographics/pdfs/myp-brief-mathematics-en.pdf', 'pdf')]

# ---------------- AP (course page + Course and Exam Description)
AP_CED = {
 'calculus-ab': ('ap-calculus-ab', APM + 'ap-calculus-ab-and-bc-course-and-exam-description.pdf'),
 'calculus-bc': ('ap-calculus-bc', APM + 'ap-calculus-ab-and-bc-course-and-exam-description.pdf'),
 'precalculus': ('ap-precalculus', APM + 'ap-precalculus-course-and-exam-description.pdf'),
 'statistics': ('ap-statistics', APM + 'ap-statistics-course-and-exam-description-effective-fall-2026.pdf'),
 'physics-1': ('ap-physics-1', 'https://Apcentral.Collegeboard.org/media/pdf/ap-physics-1-course-and-exam-description.pdf'),
 'physics-c-mechanics': ('ap-physics-c-mechanics', APM + 'ap-physics-c-mechanics-course-and-exam-description-effective-fall-2024.pdf'),
 'chemistry': ('ap-chemistry', APM + 'ap-chemistry-course-and-exam-description-effective-fall-2024.pdf'),
 'biology': ('ap-biology', APM + 'ap-biology-course-and-exam-description.pdf'),
 'environmental-science': ('ap-environmental-science', 'https://Apcentral.Collegeboard.org/media/pdf/ap-environmental-science-course-and-exam-description.pdf'),
 'computer-science-a': ('ap-computer-science-a', 'https://Apcentral.Collegeboard.org/media/pdf/ap-computer-science-a-course-and-exam-description.pdf'),
 'english-language': ('ap-english-language-and-composition', 'https://apcentral.collegeboard.org/pdf/ap-english-language-and-composition-course-and-exam-description.pdf'),
 'english-literature': ('ap-english-literature-and-composition', 'https://Apcentral.Collegeboard.org/media/pdf/ap-english-literature-and-composition-course-and-exam-description.pdf'),
 'us-history': ('ap-united-states-history', APM + 'ap-us-history-course-and-exam-description.pdf'),
 'world-history': ('ap-world-history', 'https://apcentral.collegeboard.org/pdf/ap-world-history-modern-course-and-exam-description.pdf'),
 'macroeconomics': ('ap-macroeconomics', 'https://Apcentral.Collegeboard.org/media/pdf/ap-macroeconomics-course-and-exam-description.pdf'),
 'microeconomics': ('ap-microeconomics', APM + 'ap-microeconomics-course-and-exam-description.pdf'),
 'psychology': ('ap-psychology', 'https://apcentral.collegeboard.org/pdf/ap-psychology-course-and-exam-description.pdf'),
 'japanese': ('ap-japanese-language-and-culture', APM + 'ap-japanese-course-and-exam-description-effective-fall-2026.pdf'),
}
for slug, (cb, ced) in AP_CED.items():
    L['/subjects/ap/%s/' % slug] = [('College Board（AP Central）', APC + cb, 'page'), ('Course and Exam Description', ced, 'pdf')]

def cambridge_links(level, d):
    key = '%s/%s' % (level, d['slug'])
    out = [('Cambridge International', CIP + CAM_PAGE[key] + '/', 'page')]
    if d['src'][0].lower().endswith('syllabus.pdf'):
        out.append(('Syllabus', d['src'][0], 'pdf'))
    if key in CAM_JA:
        out.append(('日本語の科目概要', CAM_JA[key], 'pdf-ja'))
    return out + CAM_EXTRA.get(key, [])
