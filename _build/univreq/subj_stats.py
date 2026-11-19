# -*- coding: utf-8 -*-
"""Statistics for UK top-30 x 12 majors (11 from uk_subj.py + Economics from uk_data.py)."""
import re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import uk_subj as U, uk_data as D
from statistics import median

KEY = {'Cambridge':'University of Cambridge','Oxford':'University of Oxford','LSE':'London School of Economics','St Andrews':'University of St Andrews',
 'Imperial':'Imperial College London','Durham':'Durham University','Warwick':'University of Warwick','Loughborough':'Loughborough University','Bath':'University of Bath',
 'Lancaster':'Lancaster University','Exeter':'University of Exeter','Birmingham':'University of Birmingham','Sheffield':'University of Sheffield','UCL':'University College London',
 'Southampton':'University of Southampton','KCL':"King's College London",'Bristol':'University of Bristol','Leeds':'University of Leeds','Edinburgh':'University of Edinburgh',
 'York':'University of York','Surrey':'University of Surrey','Liverpool':'University of Liverpool','QUB':"Queen's University Belfast",'Manchester':'University of Manchester',
 'Dundee':'University of Dundee','Nottingham':'University of Nottingham','Cardiff':'Cardiff University','UAL':'University of the Arts London','Glasgow':'University of Glasgow','Essex':'University of Essex'}
import uk_data2 as D2
KEY.update({'Heriot-Watt':'Heriot-Watt University','Aberdeen':'University of Aberdeen','Leicester':'University of Leicester','UEA':'University of East Anglia',
 'Newcastle':'Newcastle University','Sussex':'University of Sussex','Northumbria':'Northumbria University','Harper Adams':'Harper Adams University',
 'Strathclyde':'University of Strathclyde','QMUL':'Queen Mary University of London','Swansea':'Swansea University','Royal Holloway':'Royal Holloway, University of London',
 'Reading':'University of Reading','Suffolk':'University of Suffolk','Oxford Brookes':'Oxford Brookes University','Nottingham Trent':'Nottingham Trent University',
 'Ulster':'Ulster University','Brunel':'Brunel University of London','Bangor':'Bangor University','Lincoln':'University of Lincoln','Portsmouth':'University of Portsmouth'})
UKD = {d['en']: d for d in D.UK + D.UK2 + D2.UK3 if d['rank'] <= 50}
RANK = {k: UKD[v]['rank'] for k, v in KEY.items()}
JA = {k: UKD[v]['ja'] for k, v in KEY.items()}
UNIS = sorted(KEY, key=lambda k: (RANK[k], k))

MAJ = [('MED','医学'),('CS','コンピュータサイエンス'),('ENG','機械工学'),('MATH','数学'),('PHYS','物理学'),('BIO','生物学'),
       ('ECON','経済学'),('BUS','経営学'),('LAW','法学'),('PSY','心理学'),('HIST','歴史学'),('ENGL','英文学')]
MJ = dict(MAJ)

# Economics rows from uk_data
for k in UNIS:
    d = UKD[KEY[k]]
    if '経済学部なし' in (d.get('course') or ''):
        U.S[(k,'ECON')] = dict(course=None if False else U.NA)
        continue
    al = d.get('alevel') or ''
    U.S[(k,'ECON')] = dict(course=d['course'], al=None if '公式' in al else al, ib=None if '公式' in (d.get('ib') or '') else d.get('ib'),
                         req=('数学' if '数学' in al else None), test=('TMUA' if 'TMUA' in (d.get('note') or '') else None), src=list(d.get('src') or []))
# admissions tests for economics checked on course pages (2027 entry)
U.S[('Imperial','ECON')]['test'] = 'TMUA'
U.S[('Oxford','ECON')]['test'] = 'TARA'; U.S[('Oxford','ECON')]['src'].append(U.OX)

PTS = {'A*':56,'A':48,'B':40,'C':32,'D':24,'E':16}
def grades(al):
    if not al: return None
    m = re.match(r'\s*((?:A\*|[ABCDE])+)', al)
    if not m: return None
    g = re.findall(r'A\*|[ABCDE]', m.group(1))
    return g[:3] if len(g) >= 3 else None
def tariff(al):
    g = grades(al); return sum(PTS[x] for x in g) if g else None
T2G = {168:'A*A*A*',160:'A*A*A',152:'A*AA',144:'AAA',136:'AAB',128:'ABB',120:'BBB',112:'BBC',104:'BCC'}

def row(k, m): return U.S.get((k, m))
def offered(r): return r is not None and r.get('course') not in (None, U.NA) 
def is_na(r): return r is not None and r.get('course') is U.NA and 'course' in r

def ibpts(s):
    if not s: return None
    m = re.search(r'(\d{2})(?:〜\d{2})?点', s); return int(m.group(1)) if m else None
def hl7(s):
    if not s or '6か7' in s: return False
    return bool(re.search(r'(数学|物理|化学|生物|理系)[^）]*?7|HL7|で7', s))

TOK = [('FM','更なる数学'),('MATH','数学'),('PHY','物理'),('CHEM','化学'),('BIO','生物'),('HIST','歴史'),('ENG','英')]
def req_parse(s):
    """-> (hard set, optional-group list, none_flag)"""
    if s is None: return None
    s0 = re.sub(r'（[^）]*）', '', s)
    if s0.startswith('指定なし') or s0.strip() == '': return (set(), [], True)
    hard, opt = set(), []
    for cl in s0.split('＋'):
        choice = any(w in cl for w in ('いずれか','から','1科目','1つ','など')) or re.search(r'.か.', cl.replace('更なる数学か', '更なる数学/'))
        toks = set()
        c2 = cl
        if '更なる数学' in c2: toks.add('FM'); c2 = c2.replace('更なる数学', '')
        for t, w in TOK[1:]:
            if w in c2: toks.add(t)
        if '英' in cl and ('英文学' in cl or '英語' in cl): toks.add('ENG')
        if choice: opt.append(toks)
        else: hard |= toks
    return (hard, opt, False)

def stats():
    out = {}
    for m, ja in MAJ:
        rs = [(k, row(k, m)) for k in UNIS]
        off = [(k, r) for k, r in rs if offered(r)]
        na = [k for k, r in rs if r is not None and r.get('course') is U.NA]
        unk = [k for k, r in rs if r is None or r.get('course') is None]
        tar = [(k, tariff(r.get('al'))) for k, r in off if tariff(r.get('al'))]
        astar = [k for k, r in off if grades(r.get('al')) and 'A*' in grades(r.get('al'))]
        ib = [(k, ibpts(r.get('ib'))) for k, r in off if ibpts(r.get('ib'))]
        h7 = [k for k, r in off if r.get('ib') and hl7(r.get('ib'))]
        ibk = [k for k, r in off if r.get('ib')]
        tests = [(k, r.get('test')) for k, r in off if r.get('test') and not r['test'].startswith('なし') and '条件が変わる' not in r['test']]
        reqs = [(k, req_parse(r.get('req'))) for k, r in off if r.get('req') is not None]
        out[m] = dict(ja=ja, off=off, na=na, unk=unk, tar=tar, astar=astar, ib=ib, h7=h7, ibk=ibk, tests=tests, reqs=reqs)
    return out

if __name__ == '__main__':
    st = stats()
    for m, ja in MAJ:
        s = st[m]; t = [v for _, v in s['tar']]
        top = [v for k, v in s['tar'] if RANK[k] <= 10]; rest = [v for k, v in s['tar'] if RANK[k] > 10]
        print('%-4s %-10s off=%2d na=%2d unk=%2d | A-lvl n=%2d med=%s top10=%s rest=%s A*=%d/%d | IB n=%d med=%s | HL7 %d/%d | tests %d: %s' % (
            m, ja, len(s['off']), len(s['na']), len(s['unk']), len(t), T2G.get(median(t), median(t)) if t else '-',
            T2G.get(median(top), median(top)) if top else '-', T2G.get(median(rest), median(rest)) if rest else '-',
            len(s['astar']), len(t), len(s['ib']), median([v for _, v in s['ib']]) if s['ib'] else '-', len(s['h7']), len(s['ibk']),
            len(s['tests']), ','.join(sorted(set(re.split('[・（]', v)[0] for _, v in s['tests'])))))
        from collections import Counter
        hard = Counter(); none = 0
        for k, p in s['reqs']:
            if p[2]: none += 1
            for x in p[0]: hard[x] += 1
        print('      req n=%d none=%d hard=%s' % (len(s['reqs']), none, dict(hard)))
