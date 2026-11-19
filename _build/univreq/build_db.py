# -*- coding: utf-8 -*-
"""Interactive admissions database (US / UK / Canada / Australia / Singapore) at /column/university/us-uk-requirements/.
Usage: python3 build_db.py /home/claude/camino-v2"""
import os, sys, re, json, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_req as BR
import build_split as B
import acs_eng as AE
M, C, SS, A = BR.M, BR.C, B.SS, B.A
import uk_data as UKD, uk_data2 as UKD2, us_data as USD, us_data2 as USD2

PATH = '/column/university/us-uk-requirements/'
MAJ = B.MAJ

def strip(x): return re.sub(r'\s+', ' ', x or '').strip()

# ---------- data ----------
def us_records():
    out = []
    for d in USD.US + USD2.US3:
        src = BR.UC if d.get('uc') else d
        ex = src.get('exempt', '—')
        sat = src.get('test', '—')
        cat = 'req' if sat.startswith('必須') else ('no' if '使わない' in sat or 'blind' in sat else 'opt')
        if d.get('uc'): cat = 'no'
        out.append(dict(r=d['rank'], ja=d['ja'], en=d['en'], sat=sat, cat=cat, eng=BR.us_cell_scores(d),
                        ex='—' if ex in ('-', '') else ex, src=(src.get('src') or [''])[0]))
    return out

def uk_records():
    econ = {d['en']: d for d in UKD.UK + UKD.UK2 + UKD2.UK3}
    key_of = {v: k for k, v in SS.KEY.items()}
    out = []
    for en, d in sorted(econ.items(), key=lambda x: (x[1]['rank'], x[0])):
        rec = dict(r=d['rank'], ja=d['ja'], en=en, ielts=d.get('ielts') or '—', m={})
        rec['m']['ECON'] = dict(c=d.get('course') or '—', al=d.get('alevel') or '—', ib=d.get('ib') or '—', req=d.get('note') or '—', t='—',
                                src=(d.get('src') or [''])[0])
        k = key_of.get(en)
        if k:
            for m, _ in MAJ:
                if m == 'ECON': continue
                r = SS.U.S.get((k, m))
                if r is None: continue
                if r.get('course') == SS.U.NA: rec['m'][m] = dict(na=1); continue
                if r.get('course') is None: rec['m'][m] = dict(unk=1); continue
                rec['m'][m] = dict(c=r['course'], al=r.get('al') or '—', ib=r.get('ib') or '—', req=r.get('req') or '—', t=r.get('test') or '—',
                                   src=(r.get('src') or [''])[0])
        out.append(rec)
    return out

def acs_records(cty):
    eng = {d['ja']: d for d in AE.E if d['c'] == cty}
    out = []
    for i, (k, ja) in enumerate(A.UNI[cty]):
        e = eng.get(ja, {})
        rec = dict(r=i + 1, qs=A.QS.get(k), ja=ja, en=k, ielts=e.get('ielts') or '—', toefl=e.get('toefl') or '—',
                   inter=(AE.INTER[e['inter']][0] if e.get('inter') else (e.get('note') or '—')), m={})
        for m, _ in MAJ:
            r = A.S.get((cty, k, m))
            if r is None: continue
            if r.get('course') == A.NA: rec['m'][m] = dict(na=1); continue
            if r.get('course') is None: rec['m'][m] = dict(unk=1); continue
            rec['m'][m] = dict(c=r['course'], al=r.get('al') or '—', ib=('%d点' % r['ib']) if r.get('ib') else '—', req=r.get('req') or '—',
                               t=r.get('test') or r.get('note') or '—', src=(r.get('src') or [''])[0])
        out.append(rec)
    return out

DATA = {'US': us_records(), 'UK': uk_records(), 'CA': acs_records('CA'), 'AU': acs_records('AU'), 'SG': acs_records('SG')}

# ---------- flags (simplified, inline SVG 3:2) ----------
FLAG = {
 'US': '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#fff"/>' + ''.join('<rect y="%.3f" width="30" height="1.538" fill="#b22234"/>' % (i * 3.077) for i in range(7)) + '<rect width="13" height="10.77" fill="#3c3b6e"/>' + ''.join('<circle cx="%.1f" cy="%.1f" r=".55" fill="#fff"/>' % (1.6 + 2.2 * x + (1.1 if y % 2 else 0), 1.4 + 1.95 * y) for y in range(5) for x in range(5 if y % 2 == 0 else 5) if 1.6 + 2.2 * x + (1.1 if y % 2 else 0) < 12.5) + '</svg>',
 'UK': '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#012169"/><path d="M0 0L30 20M30 0L0 20" stroke="#fff" stroke-width="4"/><path d="M0 0L30 20M30 0L0 20" stroke="#c8102e" stroke-width="1.4"/><path d="M15 0V20M0 10H30" stroke="#fff" stroke-width="6"/><path d="M15 0V20M0 10H30" stroke="#c8102e" stroke-width="3.4"/></svg>',
 'CA': '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#fff"/><rect width="7.5" height="20" fill="#d52b1e"/><rect x="22.5" width="7.5" height="20" fill="#d52b1e"/><path d="M15 3.6l1 1.9 1.1-.5-.4 2.6 1.5-1.3.4.9 1.5-.3-.6 1.7.7.3-2.7 2.2.3 1-2.6-.4v2.6h-.4v-2.6l-2.6.4.3-1-2.7-2.2.7-.3-.6-1.7 1.5.3.4-.9 1.5 1.3-.4-2.6 1.1.5z" fill="#d52b1e"/></svg>',
 'AU': '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#012169"/><g><path d="M0 0L15 10M15 0L0 10" stroke="#fff" stroke-width="2"/><path d="M0 0L15 10M15 0L0 10" stroke="#e4002b" stroke-width=".8"/><path d="M7.5 0V10M0 5H15" stroke="#fff" stroke-width="3"/><path d="M7.5 0V10M0 5H15" stroke="#e4002b" stroke-width="1.7"/></g><circle cx="7.5" cy="15" r="1.7" fill="#fff"/><circle cx="22.5" cy="4" r=".9" fill="#fff"/><circle cx="19.5" cy="9" r=".9" fill="#fff"/><circle cx="25.5" cy="8" r=".9" fill="#fff"/><circle cx="22.5" cy="16" r=".9" fill="#fff"/><circle cx="24.2" cy="11.6" r=".5" fill="#fff"/></svg>',
 'SG': '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#fff"/><rect width="30" height="10" fill="#ef3340"/><circle cx="7" cy="5" r="3.6" fill="#fff"/><circle cx="8.4" cy="5" r="3.6" fill="#ef3340"/>' + ''.join('<circle cx="%.2f" cy="%.2f" r=".55" fill="#fff"/>' % p for p in [(10.2, 2.6), (12.2, 4.0), (11.4, 6.4), (9.0, 6.4), (8.2, 4.0)]) + '</svg>',
}
CTY = [('US', 'アメリカ', 'U.S. News 2027 上位100位'), ('UK', 'イギリス', 'Complete University Guide 2027 上位100位'),
       ('CA', 'カナダ', 'QS 2027 国内上位5校'), ('AU', 'オーストラリア', 'QS 2027 国内上位5校'), ('SG', 'シンガポール', '主要な国立5大学')]

def body():
    cards = ''.join('<button type="button" class="udb-c" data-c="%s" aria-pressed="%s"><span class="udb-flag">%s</span><b>%s</b><span class="udb-n">%d校</span><small>%s</small></button>'
                    % (c, 'true' if c == 'US' else 'false', FLAG[c], ja, len(DATA[c]), sub) for c, ja, sub in CTY)
    majopts = ''.join('<option value="%s"%s>%s</option>' % (m, ' selected' if m == 'ECON' else '', ja) for m, ja in MAJ)
    out = ['<div class="udb rise" id="udb">',
           '<p class="udb-h">国を選ぶ</p><div class="udb-cs" role="group" aria-label="国を選ぶ">%s</div>' % cards,
           '<div class="udb-bar">'
           '<label class="udb-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
           '<input type="search" id="udb-q" placeholder="大学名で探す（日本語・英語）" autocomplete="off"></label>'
           '<label class="udb-sel" id="udb-majw" hidden><span>学部</span><select id="udb-maj">%s</select></label>' % majopts +
           '<div class="udb-chips" id="udb-band" role="group" aria-label="順位で絞り込む"></div>'
           '<div class="udb-chips" id="udb-sat" role="group" aria-label="SAT・ACTで絞り込む"></div>'
           '</div>',
           '<p class="udb-meta" id="udb-meta" aria-live="polite"></p>',
           '<div class="udb-list" id="udb-list"></div>',
           '<p class="rnote" id="udb-note"></p>',
           '<noscript><p class="rnote">このデータベースの絞り込みにはJavaScriptを使います</p></noscript>',
           '</div>']
    return '\n'.join(out)

JS = r'''<script>
(function(){
var D=__DATA__,MJ=__MAJ__;
var st={c:'US',q:'',band:'all',sat:'all',m:'ECON'};
try{var h=location.hash.slice(1).split('-');if(D[(h[0]||'').toUpperCase()])st.c=h[0].toUpperCase();if(h[1]&&MJ[h[1].toUpperCase()])st.m=h[1].toUpperCase();}catch(e){}
var $=function(id){return document.getElementById(id)};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var BANDS={US:[['all','すべて'],['1-10','1〜10位'],['11-30','11〜30位'],['31-50','31〜50位'],['51-100','51〜100位']],UK:[['all','すべて'],['1-10','1〜10位'],['11-30','11〜30位'],['31-50','31〜50位'],['51-100','51〜100位']]};
var SATS=[['all','すべて'],['req','必須'],['opt','任意'],['no','使わない']];
function chips(el,list,cur,key){el.innerHTML=list.map(function(x){return '<button type="button" data-v="'+x[0]+'" aria-pressed="'+(x[0]===cur)+'">'+x[1]+'</button>'}).join('');
 el.onclick=function(e){var b=e.target.closest('button');if(!b)return;st[key]=b.getAttribute('data-v');render()}}
function inBand(r){if(st.band==='all')return true;var p=st.band.split('-');return r>=+p[0]&&r<=+p[1]}
function row(cells,cls){return '<div class="udb-r'+(cls?' '+cls:'')+'">'+cells.map(function(c){return '<div class="udb-d'+(c[2]?' '+c[2]:'')+'"><span class="udb-l">'+c[0]+'</span><span class="udb-v">'+c[1]+'</span></div>'}).join('')+'</div>'}
function name(d,rk){return '<span class="udb-rk">'+rk+'</span><b>'+esc(d.ja)+'</b><small>'+esc(d.en)+'</small>'}
function render(){
 var c=st.c,q=st.q.trim().toLowerCase(),list=D[c],html=[],n=0;
 [].forEach.call(document.querySelectorAll('.udb-c'),function(b){var on=b.getAttribute('data-c')===c;b.setAttribute('aria-pressed',on);if(on){var w=b.parentNode;if(w.scrollWidth>w.clientWidth)w.scrollLeft=b.offsetLeft-w.offsetLeft-16}});
 $('udb-majw').hidden=(c==='US');$('udb-maj').value=st.m;
 var bandEl=$('udb-band'),satEl=$('udb-sat');
 if(BANDS[c]){bandEl.hidden=false;chips(bandEl,BANDS[c],st.band,'band')}else{bandEl.hidden=true;st.band='all'}
 if(c==='US'){satEl.hidden=false;chips(satEl,SATS,st.sat,'sat')}else{satEl.hidden=true}
 var head;
 if(c==='US'){head=['大学','SAT・ACT','英語試験の基準・目安','英語試験が免除される条件'];
  list.forEach(function(d){if(!inBand(d.r))return;if(st.sat!=='all'&&d.cat!==st.sat)return;if(q&&(d.ja+d.en).toLowerCase().indexOf(q)<0)return;n++;
   html.push(row([[head[0],name(d,d.r+'位'),'udb-nm'],[head[1],esc(d.sat)],[head[2],d.eng],[head[3],esc(d.ex)]]))})}
 else{var m=st.m,uk=(c==='UK');
  head=['大学','コース','A Level','国際バカロレア（IB）','必須科目・条件',uk?'入学試験':'入学試験・備考',uk?'IELTS（経済学部）':'英語（IELTS／TOEFL）'];
  list.forEach(function(d){if(!inBand(d.r))return;if(q&&(d.ja+d.en).toLowerCase().indexOf(q)<0)return;
   var x=d.m[m],rk=uk?d.r+'位':(d.qs?'QS '+d.qs+'位':'国立');
   var eng=uk?esc(d.ielts):('IELTS '+esc(d.ielts)+'<br>TOEFL '+esc(d.toefl)+'<br><small>'+esc(d.inter)+'</small>');
   if(!x){if(uk&&d.r>50)return;n++;html.push(row([[head[0],name(d,rk),'udb-nm'],['','<span class="udb-mut">この学部の要件は、このデータベースの対象外です</span>','udb-wide']],'udb-off'));return}
   n++;
   if(x.na){html.push(row([[head[0],name(d,rk),'udb-nm'],['','<span class="udb-mut">学部課程にこの学部はありません（大学院で学ぶ場合を含む）</span>','udb-wide']],'udb-off'));return}
   if(x.unk){html.push(row([[head[0],name(d,rk),'udb-nm'],['','<span class="udb-mut">公式サイトで確認できませんでした</span>','udb-wide']],'udb-off'));return}
   html.push(row([[head[0],name(d,rk),'udb-nm'],[head[1],esc(x.c)+(x.src?' <a class="udb-src" href="'+esc(x.src)+'" target="_blank" rel="noopener">公式</a>':'')],[head[2],esc(x.al)],[head[3],esc(x.ib)],[head[4],esc(x.req)],[head[5],esc(x.t)],[head[6],eng]]))})}
 $('udb-list').className='udb-list udb-'+c.toLowerCase();
 $('udb-list').innerHTML=(n?'<div class="udb-r udb-hd">'+head.map(function(h){return '<div class="udb-d">'+h+'</div>'}).join('')+'</div>'+html.join(''):'<p class="udb-empty">条件に合う大学がありません</p>');
 var cn={US:'アメリカ',UK:'イギリス',CA:'カナダ',AU:'オーストラリア',SG:'シンガポール'}[c];
 $('udb-meta').innerHTML='<b>'+cn+'</b>'+(c!=='US'?'・'+MJ[st.m]:'')+'　'+n+'校';
 var notes={US:'「以上」は大学が定める最低点、「目安」「推奨」は合格者に多い点数や大学が勧める点数です。「新TOEFL」は2026年1月21日以降の1〜6のスコアです',
  UK:'標準的なオファー（合格に必要な条件）です。上位50校は12学部、51〜100位は経済学部のみを掲載しています。IELTSは経済学部の基準です',
  CA:'IBの点数は大学が示す目安の下限です。英語の「インター生の扱い」は、日本のインターに通う生徒を想定しています',
  AU:'IBの点数は入学の目安や保証点です。英語の「インター生の扱い」は、日本のインターに通う生徒を想定しています',
  SG:'シンガポールの大学は、IBの点数の目安を学部ごとに公表していません。英語試験は、指定された資格や英語以外で学ぶ資格の出願者に求められます'};
 $('udb-note').textContent=notes[c]+'。要件は毎年見直されるため、出願前に必ず各大学の公式サイトで確認してください';
 try{history.replaceState(null,'','#'+c.toLowerCase()+(c!=='US'?'-'+st.m.toLowerCase():''))}catch(e){}
}
document.querySelector('.udb-cs').onclick=function(e){var b=e.target.closest('.udb-c');if(!b)return;st.c=b.getAttribute('data-c');st.band='all';st.sat='all';render()};
$('udb-q').oninput=function(){st.q=this.value;render()};
$('udb-maj').onchange=function(){st.m=this.value;render()};
render();
})();
</script>'''

CSS = '''<style id="udb-css">
.udb{margin:4px 0 30px}
.udb-h{font-size:13px;font-weight:700;color:var(--muted,#5c6984);margin:0 0 10px;letter-spacing:.04em}
.udb-cs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.udb-c{display:flex;flex-direction:column;align-items:flex-start;gap:4px;text-align:left;background:#fff;border:1.5px solid var(--line,#d9deea);border-radius:14px;padding:14px 14px 12px;cursor:pointer;font:inherit;color:var(--navy,#0b1f4b);transition:border-color .15s,box-shadow .15s,transform .15s}
.udb-c:hover{transform:translateY(-2px);box-shadow:0 10px 22px -16px rgba(22,41,77,.6)}
.udb-c[aria-pressed="true"]{border-color:var(--navy,#16294d);box-shadow:0 0 0 2px var(--navy,#16294d) inset}
.udb-c:focus-visible{outline:3px solid #2a78d6;outline-offset:2px}
.udb-flag svg{display:block;width:42px;height:28px;border-radius:4px;box-shadow:0 0 0 1px rgba(0,0,0,.08)}
.udb-flag{margin-bottom:6px}
.udb-c b{font-size:16px}
.udb-n{font-size:12.5px;font-weight:700;color:var(--c,#16294d)}
.udb-c small{font-size:11px;color:var(--muted,#5c6984);line-height:1.5}
.udb-bar{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;margin:18px 0 0;padding:12px 0;background:var(--paper,#fcfcfb);border-bottom:1px solid var(--line,#e3e7f0)}
.udb-search{flex:1 1 260px;display:flex;align-items:center;gap:8px;background:#fff;border:1.5px solid var(--line,#d9deea);border-radius:999px;padding:8px 14px}
.udb-search svg{width:16px;height:16px;color:var(--muted,#5c6984);flex:none}
.udb-search input{border:0;outline:0;font:inherit;font-size:14px;width:100%;background:none;color:var(--navy,#0b1f4b)}
.udb-search:focus-within{border-color:var(--navy,#16294d)}
.udb-sel{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;color:var(--navy,#0b1f4b)}
.udb-sel select{font:inherit;font-size:14px;border:1.5px solid var(--line,#d9deea);border-radius:10px;padding:7px 10px;background:#fff;color:var(--navy,#0b1f4b)}
.udb-chips{display:flex;flex-wrap:wrap;gap:6px}
.udb-chips[hidden],.udb-sel[hidden]{display:none}
.udb-chips button{font:inherit;font-size:12.5px;font-weight:700;border:1.5px solid var(--line,#d9deea);background:#fff;color:var(--navy,#0b1f4b);border-radius:999px;padding:6px 12px;cursor:pointer}
.udb-chips button[aria-pressed="true"]{background:var(--navy,#16294d);border-color:var(--navy,#16294d);color:#fff}
.udb-meta{font-size:13px;color:var(--muted,#5c6984);margin:12px 0 8px}.udb-meta b{color:var(--navy,#0b1f4b)}
.udb-list{border:1px solid var(--line,#d9deea);border-radius:14px;overflow:hidden;background:#fff}
.udb-r{display:grid;border-top:1px solid #edf0f5}.udb-r:first-child{border-top:0}
.udb-us .udb-r{grid-template-columns:1.25fr .8fr 1.5fr 1.35fr}
.udb-uk .udb-r,.udb-ca .udb-r,.udb-au .udb-r,.udb-sg .udb-r{grid-template-columns:1.2fr 1fr .8fr .9fr 1.1fr .8fr 1fr}
.udb-d{padding:12px 12px;font-size:13px;line-height:1.65;color:var(--ink,#1d2b45);min-width:0;overflow-wrap:anywhere}
.udb-hd{background:#f4f6fa;position:sticky;top:0}.udb-hd .udb-d{font-size:11.5px;font-weight:700;color:var(--muted,#5c6984);padding:9px 12px}
.udb-l{display:none}
.udb-nm b{display:block;font-size:14px;color:var(--navy,#0b1f4b)}.udb-nm small{display:block;font-size:11px;color:var(--muted,#5c6984)}
.udb-rk{display:inline-block;font-size:10.5px;font-weight:700;color:#fff;background:var(--navy,#16294d);border-radius:5px;padding:1px 6px;margin-bottom:3px}
.udb-wide{grid-column:2/-1}.udb-mut{color:var(--muted,#5c6984);font-size:12.5px}
.udb-off .udb-nm b{color:var(--muted,#5c6984)}
.udb-src{font-size:11px;font-weight:700;color:var(--c,#16294d);border:1px solid currentColor;border-radius:4px;padding:0 4px;text-decoration:none;white-space:nowrap}
.udb-empty{padding:24px;text-align:center;color:var(--muted,#5c6984)}
.udb-d .rq-elp{display:inline-block;font-size:11px;font-weight:700;background:#eef2f8;border-radius:5px;padding:1px 6px;margin-bottom:3px}
@media(max-width:900px){.udb-cs{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:760px){
.udb-cs{display:flex;overflow-x:auto;gap:8px;padding-bottom:4px;scroll-snap-type:x mandatory}
.udb-c{flex:0 0 132px;scroll-snap-align:start;padding:12px}
.udb-flag svg{width:36px;height:24px}
.udb-bar{top:0}
.udb-r.udb-hd{display:none!important}
.udb-r{display:block!important;padding:12px 14px}
.udb-d{padding:4px 0;display:grid;grid-template-columns:96px 1fr;gap:8px}
.udb-nm{display:block}.udb-nm .udb-l,.udb-wide .udb-l{display:none}
.udb-l{display:block;font-size:11px;font-weight:700;color:var(--muted,#5c6984)}
.udb-wide{display:block}
}
</style>
'''

def build():
    nus, nuk = len(DATA['US']), len(DATA['UK'])
    lead = ('アメリカ・イギリス・カナダ・オーストラリア・シンガポールの大学の入学要件を、国・学部・順位で絞り込めるデータベースです。'
            'SAT・ACTの扱い、英語試験の基準と免除条件、国際バカロレア（IB）とA Levelの条件を、各大学の公式サイトの記載に基づいて掲載しています')
    faq = [('ランキングはどれを使っていますか？', 'アメリカはU.S. News「Best National Universities 2027」、イギリスはthe Complete University Guide 2027の総合ランキング、カナダとオーストラリアはQS世界大学ランキング2027の各国上位5校です。シンガポールは主要な国立5大学を掲載しています'),
           ('ここに載っている点数を取れば合格できますか？', 'いいえ。掲載しているのは出願や入学の条件・目安で、合格を保証するものではありません。アメリカの大学は成績や課外活動、エッセイなどを総合的に評価し、イギリスの大学も多くの場合、予想成績や志望理由書、面接や入学試験で選考します'),
           ('インターに通っていれば、TOEFLやIELTSは不要ですか？', '多くの大学で免除の対象になりますが、条件は大学ごとに違います。英語圏の国での在籍を条件にする大学もあるため、志望校ごとに確認してください')]
    nxt = [('/column/university/ib-scores-by-major/', '国際バカロレア（IB）は何点必要？', '12学部別に見る総合点と必須科目', True), ('/column/university/a-level-scores-by-major/', 'A Levelは何点必要？', '12学部別に見る成績と必須科目', False),
           ('/column/university/sat-english-tests/', 'SAT・英語試験はどのくらい必要？', '上位100大学のデータから', False), ('/column/destinations/', '同じインターでも、進学先の国はこんなに違う？', '各校の進学先を国・地域ごとに比較', False)]
    src = [(BR.US_RANK[0], 'U.S. News Best National Universities 2027（ランキング表：College Kickstart）'), (BR.UK_RANK[0], 'The Complete University Guide：University League Tables 2027')] + \
          [(u, 'QS World University Rankings 2027（%s）' % {'AU': 'オーストラリア', 'CA': 'カナダ'}[c]) for c, u in A.RANK_SRC.items()]
    seen = set(u for u, _ in src)
    for d in USD.US + USD2.US3 + UKD.UK + UKD.UK2 + UKD2.UK3:
        for u in d.get('src', []) or []:
            if u not in seen: seen.add(u); src.append((u, '%s：%s' % (d['en'], u.split('//')[1].split('/')[0])))
    for m, _ in MAJ:
        for u, t in B.major_sources(m):
            if u not in seen: seen.add(u); src.append((u, t))
    for u, t in AE.sources():
        if u not in seen: seen.add(u); src.append((u, t))
    js = JS.replace('__DATA__', json.dumps(DATA, ensure_ascii=False)).replace('__MAJ__', json.dumps(dict(MAJ), ensure_ascii=False))
    url = M.page(PATH,
        '海外大学の出願要件データベース｜アメリカ・イギリス・カナダ・オーストラリア・シンガポール（SAT・TOEFL・IELTS・国際バカロレア（IB）・A Level）',
        'アメリカ%d校・イギリス%d校とカナダ・オーストラリア・シンガポールの主要大学の入学要件を、国・学部・順位で絞り込めるデータベース。SAT・ACT、TOEFL・IELTSと免除条件、国際バカロレア（IB）とA Levelの条件（2027年入学）' % (nus, nuk),
        '海外大学の<span class="nw">出願要件データベース</span>', 'コラム・大学進学', lead, body() + js,
        [('コラム', '/column/'), ('大学進学', '/column/university/'), ('出願要件データベース', PATH)],
        faq=faq, nxt=nxt,
        cta=('志望校に合わせた準備を、相談したい方へ', 'SAT・英語試験・IBやA Levelの成績まで、志望校から逆算した準備をご提案します。初回60分は無料体験です'),
        src=src, src_note='入学要件は、2026年11月時点の各大学の公式サイト（一部はUCASの公式コースページ）によります。要件は変更されることがあるため、出願前に必ず各大学の公式サイトでご確認ください',
        nav=M.COL_NAV, kind='uni', ld_type='Article', toc_items=[])
    f = os.path.join(M.ROOT, PATH.strip('/'), 'index.html')
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<style id="(rq|db|udb)-css">.*?</style>\n', '', s, flags=re.S)
    s = s.replace('</head>', BR.CSS_HEAD + CSS + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    print(url, {k: len(v) for k, v in DATA.items()})

if __name__ == '__main__':
    build()
