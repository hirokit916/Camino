(function(){var pop=null,src=null;
function close(){if(pop){pop.remove();pop=null}if(src){src.setAttribute('aria-expanded','false');src=null}}
function go(id){var c=document.getElementById(id);if(!c)return false;close();var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;c.scrollIntoView({behavior:rm?'auto':'smooth',block:'start'});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash');try{history.replaceState(null,'','#'+id)}catch(e){}return true}
document.addEventListener('click',function(e){
 var k=e.target.closest&&e.target.closest('a.kt');
 if(k){e.preventDefault();var was=(src===k);close();if(was)return;var n=k.getAttribute('data-tip'),card=document.getElementById('tip-'+n);if(!card)return;
  pop=document.createElement('div');pop.className='ktp';pop.setAttribute('role','dialog');var lab=(k.querySelector('.kt-n')||{}).textContent||'';pop.setAttribute('aria-label',lab);
  pop.innerHTML='<p class="ktp-l">'+lab+'</p><p class="ktp-t"></p><p class="ktp-s"></p><a class="ktp-go" href="#tip-'+n+'">詳しく見る ↓</a><button type="button" class="ktp-x" aria-label="閉じる">×</button>';
  pop.querySelector('.ktp-t').textContent=card.getAttribute('data-title');pop.querySelector('.ktp-s').textContent=card.getAttribute('data-sum');
  document.body.appendChild(pop);var r=k.getClientRects();r=r[r.length-1]||k.getBoundingClientRect();var vw=document.documentElement.clientWidth,w=pop.offsetWidth;
  pop.style.left=(Math.min(Math.max(12,r.left),vw-w-12)+window.scrollX)+'px';pop.style.top=(r.bottom+window.scrollY+10)+'px';
  src=k;k.setAttribute('aria-expanded','true');var pr=pop.getBoundingClientRect();if(pr.bottom>window.innerHeight-12){window.scrollBy({top:pr.bottom-window.innerHeight+24,behavior:'smooth'})}return}
 if(e.target.closest&&e.target.closest('.ktp-x')){close();return}
 var g=e.target.closest&&e.target.closest('.ktp-go,.tsum-l a');
 if(g){if(go(g.getAttribute('href').slice(1)))e.preventDefault();return}
 if(pop&&!(e.target.closest&&e.target.closest('.ktp')))close()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
window.addEventListener('resize',close);})();