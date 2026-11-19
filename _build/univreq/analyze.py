import re, sys, json, statistics as st
sys.path.insert(0,'.')
import us_data, us_data2, uk_data, uk_data2
US = us_data.US + us_data2.US3
UC = next(d for d in US if d['en'].endswith('Berkeley'))
def R(d):
    if d.get('uc'):
        x=dict(UC); x['rank']=d['rank']; x['en']=d['en']; x['ja']=d['ja']; return x
    return d
US=[R(d) for d in US]
UK = uk_data.UK + uk_data.UK2 + uk_data2.UK3
def band_us(r): return '1-10' if r<=10 else '11-20' if r<=20 else '21-30' if r<=30 else '31-50' if r<=50 else '51-100'
BANDS=['1-10','11-20','21-30','31-50','51-100']
def num(s, lo=None, hi=None):
    if not s: return None
    m=re.findall(r'\d+(?:\.\d+)?', s)
    v=[float(x) for x in m if (lo is None or float(x)>=lo) and (hi is None or float(x)<=hi)]
    return v
def kind(s):
    if not s: return None
    if 'min' in s or '以上' in s and '目安' not in s and '推奨' not in s: return 'min'
    return 'target'
# ---- US test policy
def tcat(t):
    if t.startswith('必須'): return 'required'
    if t.startswith('任意') or t.startswith('提出は任意'): return 'optional'
    if '不要' in t or '使用しない' in t: return 'not used'
    return 'other'
print('== US test policy by band')
for b in BANDS:
    sub=[d for d in US if band_us(d['rank'])==b]
    c={k:sum(1 for d in sub if tcat(d['test'])==k) for k in ['required','optional','not used','other']}
    print(b,len(sub),c)
print('reinstating:', [d['en']+':'+d['test'] for d in US if '必須）' in d['test'] or '必須に' in d['test']])
# ---- new TOEFL
print('== new TOEFL by band (first number, 1-6)')
for b in BANDS:
    sub=[d for d in US if band_us(d['rank'])==b]
    mins=[];tg=[]
    for d in sub:
        t=d.get('toefl')
        if t and t[1]:
            v=num(t[1],1,6)
            if v:
                (mins if kind(t[1])=='min' else tg).append(v[0] if kind(t[1])=='min' else v[-1] if '推奨' in t[1] and 'min' in t[1] else v[0])
    print(b,'n',len(sub),'min',sorted(mins),'target',sorted(tg))
print('== old TOEFL by band')
for b in BANDS:
    sub=[d for d in US if band_us(d['rank'])==b]
    vals=[]
    for d in sub:
        t=d.get('toefl')
        if t and t[0]:
            v=num(t[0],60,120)
            if v: vals.append(v[0])
    print(b,sorted(vals), 'median', st.median(vals) if vals else None)
print('== IELTS US by band')
for b in BANDS:
    vals=[num(d['ielts'],4,9)[0] for d in US if band_us(d['rank'])==b and d.get('ielts') and num(d['ielts'],4,9)]
    print(b,sorted(vals),'median',st.median(vals) if vals else None)
print('== no English minimum published / not required')
for b in BANDS:
    sub=[d for d in US if band_us(d['rank'])==b]
    nomin=[d['en'] for d in sub if not d.get('toefl') and not d.get('ielts')]
    print(b,len(nomin),nomin)
print('== exemption strings')
def ecat(d):
    e=d.get('exempt') or ''; elp=d.get('elp','')
    if elp.startswith('不要'): return 'not-required'
    if e in ('','-','—') or '公式サイトで確認' in e or 'なし（' in e: return 'none/unknown'
    school = bool(re.search(r'(英語で授業|英語のカリキュラム|英語が主な|主に英語|授業言語が英語|英語のみで授業|英語の高校|英語のみの授業|英語で教育|英語の学校|英語が主な授業言語|英語で授業を行う|直近\d年すべて英語|中等教育を通じて英語|教育が英語|英語を主な|English)', e))
    country = bool(re.search(r'(英語圏|指定国|米国の高校|米国・|米国で|米国の中等|米国市民|英語を母語とする国|英語が公用語|英語が母語の国|国籍|米・英|英語が第一言語|カナダ)', e))
    score = bool(re.search(r'(SAT|ACT|IB|AP|A Level|IGCSE)', e))
    return ('S' if school else '')+('C' if country else '')+('T' if score else '') or 'other'
for d in US:
    print(d['rank'], d['en'][:28], '|', ecat(d), '|', (d.get('exempt') or '')[:70])
