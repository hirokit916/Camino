import re, sys, statistics as st
sys.path.insert(0,'.')
import uk_data, uk_data2
UK = uk_data.UK + uk_data.UK2 + uk_data2.UK3
T={'A*':56,'A':48,'B':40,'C':32,'D':24,'E':16}
def tariff(s):
    if not s: return None
    v=[]
    for g in re.findall(r'(?<![A-Za-z])((?:A\*|[ABCDE]){3})(?![A-Za-z*])', s):
        pts=sum(T[x] for x in re.findall(r'A\*|[ABCDE]', g)); v.append(pts)
    for p in re.findall(r'UCASポイント(\d+)(?:〜(\d+))?', s):
        v.append(int(p[0])); 
        if p[1]: v.append(int(p[1]))
    return (max(v), min(v)) if v else None
def ibpts(s):
    if not s: return None
    v=[int(x) for x in re.findall(r'(\d\d)点', s) if 24<=int(x)<=45]
    return (max(v), min(v)) if v else None
def ielts(s):
    if not s: return None
    m=re.search(r'(?<![\d.])([5-9](?:\.\d)?)(?![\d])', s)
    return float(m.group(1)) if m and 5<=float(m.group(1))<=9 else None
def band(r): return '1-10' if r<=10 else '11-20' if r<=20 else '21-30' if r<=30 else '31-50' if r<=50 else '51-100'
BANDS=['1-10','11-20','21-30','31-50','51-100']
rows=[]
for d in UK:
    t=tariff(d['alevel']); i=ibpts(d['ib']); e=ielts(d['ielts'])
    maths = '数学' in (d['alevel']+d['ib']+d.get('note',''))
    noecon = d['alevel']=='—'
    rows.append((d['rank'],d['en'],t,i,e,maths,noecon))
for b in BANDS:
    sub=[r for r in rows if band(r[0])==b]
    ts=[r[2][0] for r in sub if r[2]]; ib=[r[3][0] for r in sub if r[3]]; ie=[r[4] for r in sub if r[4]]
    print(b,'n',len(sub),'noecon',sum(r[6] for r in sub),'| tariff n',len(ts),'med',st.median(ts) if ts else None, sorted(ts),
          '| IB n',len(ib),'med',st.median(ib) if ib else None, sorted(ib),'| IELTS n',len(ie),'med',st.median(ie) if ie else None,sorted(ie),'| maths',sum(r[5] for r in sub))
# A level -> IB pairing
from collections import defaultdict
pair=defaultdict(list)
for r in rows:
    if r[2] and r[3]: pair[r[2][0]].append((r[3][0], r[1][:22]))
for k in sorted(pair, reverse=True): print('tariff',k, sorted(pair[k]))
# IB reach
print('== IB reach (standard offer <= score)')
for s in range(28,43,2):
    out=[]
    for b in BANDS:
        sub=[r for r in rows if band(r[0])==b and r[3]]
        out.append('%s %d/%d'%(b, sum(1 for r in sub if r[3][0]<=s), len(sub)))
    print(s, out)
for r in rows:
    if not r[2] or not r[3]: print('missing', r[0], r[1], r[2], r[3])
