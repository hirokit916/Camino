import sys; sys.path.insert(0,'.')
import us_data, us_data2, uk_data, uk_data2, re
from inter_lens import L, PUBLIC
from collections import Counter
US=us_data.US+us_data2.US3
print('public n', sum(1 for d in US if d['en'] in PUBLIC))
for grp,f in [('public',lambda d:d['en'] in PUBLIC),('private',lambda d:d['en'] not in PUBLIC)]:
    c=Counter(L[d['en']][0] for d in US if f(d)); print(grp, sum(c.values()), dict(sorted(c.items())))
# test policy public vs private
UC=next(d for d in US if d['en'].endswith('Berkeley'))
def R(d): return UC if d.get('uc') else d
for grp,f in [('public',lambda d:d['en'] in PUBLIC),('private',lambda d:d['en'] not in PUBLIC)]:
    c=Counter('req' if R(d)['test'].startswith('必須') else 'opt' if R(d)['test'].startswith('任意') else 'other' for d in US if f(d)); print('test',grp,dict(c))
# IELTS reach across countries
def ie(s):
    if not s: return None
    m=re.search(r'(?<![\d.])([5-9](?:\.\d)?)(?![\d])', s); return float(m.group(1)) if m else None
usv=[(d['rank'],ie(R(d).get('ielts'))) for d in US]; usv=[x for x in usv if x[1]]
UK=uk_data.UK+uk_data.UK2+uk_data2.UK3
ukv=[(d['rank'],ie(d['ielts'])) for d in UK]; ukv=[x for x in ukv if x[1]]
print('US ielts n',len(usv),'UK ielts n',len(ukv))
for s in [6.0,6.5,7.0,7.5]:
    for nm,v in [('US',usv),('UK',ukv)]:
        top=[x for x in v if x[0]<=30]; rest=[x for x in v if x[0]>30]
        print(s,nm,'top30 %d/%d'%(sum(1 for x in top if x[1]<=s),len(top)),'31-100 %d/%d'%(sum(1 for x in rest if x[1]<=s),len(rest)))
