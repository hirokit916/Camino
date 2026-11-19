# -*- coding: utf-8 -*-
import json, re, sys
from bs4 import BeautifulSoup, NavigableString, Comment
F = '/home/claude/camino-v2/subjects/ap/japanese/index.html'
soup = BeautifulSoup(open(F, encoding='utf-8').read(), 'html.parser')
INLINE = {'a', 'b', 'strong', 'em', 'i', 'small', 'span', 'br', 'sup', 'sub', 'code', 'mark', 'abbr', 'label', 'time'}
TEXTBOX = {'p', 'li', 'dd', 'dt', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'summary', 'figcaption', 'button'}
main = soup.find('main')
for x in main.find_all(['script', 'style', 'svg']): x.decompose()
for x in main.select('.kt-n, .apc-tip, .apc-ts, .crumb, .byline, .sj-off, nav.otl, .step-n, .aut-n, .tp-no, .apx-ln, .amx-bs, .apo-dot, .cta, .nx'): x.decompose()
def is_inline(el):
    if el.name not in INLINE: return False
    if el.name == 'a':
        p = el.parent
        for _ in range(3):
            if p is None: break
            if p.name in TEXTBOX: return True
            p = p.parent
        return False
    return True
def block_of(node):
    p = node.parent
    while p is not None and is_inline(p): p = p.parent
    return p
blocks = []
seen = set()
for t in main.descendants:
    if isinstance(t, Comment) or not isinstance(t, NavigableString): continue
    if not t.strip(): continue
    b = block_of(t)
    if id(b) in seen: continue
    seen.add(id(b)); blocks.append(b)
def render(el):
    out = []; prev_el = False
    for c in el.children:
        if isinstance(c, Comment): continue
        if isinstance(c, NavigableString):
            if c.strip():
                if prev_el == 'span': out.append(' ｜ ')
                prev_el = False
            out.append(str(c)); continue
        if not is_inline(c): continue
        if prev_el and c.name != 'br' and c.get_text().strip() and c.name not in ('a',): out.append(' ｜ ')
        prev_el = ('span' if c.name in ('span', 'i', 'small') else True) if (c.name != 'br' and c.get_text().strip()) else False
        if c.name == 'br': out.append(' / '); continue
        inner = render(c)
        if c.name in ('b', 'strong', 'em') and inner.strip(): out.append('**%s**' % inner)
        elif c.name == 'small' and inner.strip(): out.append(' ' + inner)
        else: out.append(inner)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()
def has_cls(el, cls):
    while el is not None and el.name != 'main':
        if cls in (el.get('class') or []): return True
        el = el.parent
    return False
def all_en(el):
    texts = [t for t in el.find_all(string=True) if t.strip()]
    if not texts: return False
    def en(t):
        p = t.parent
        while p is not None and p is not el.parent:
            if p.get('lang') == 'en': return True
            p = p.parent
        return False
    return all(en(t) for t in texts)
def section_of(el):
    return None
items = []
for b in blocks:
    txt = render(b)
    if not txt: continue
    lock = None
    if has_cls(b, 'apx-en') or has_cls(b, 'tp-q'): lock = 'College Boardの採点基準の英語原文'
    elif has_cls(b, 'aub-q'): lock = 'College Boardの公式日本語訳（問い）'
    elif all_en(b): lock = '英語の公式名称・原文'
    head = b.name in ('h1', 'h2', 'h3')
    items.append((txt, lock, b.name, head))
meta = [('title', soup.title.string.strip())]
md = soup.find('meta', attrs={'name': 'description'})
if md: meta.append(('description', md['content']))
lines = ['# AP 日本語と日本文化 ページ本文（編集用テキスト）', '',
 '## 編集のルール（このファイルを編集するAIへ）', '',
 '- 各行の先頭の番号 [0001] は、戻すときの目印です。消したり、順番を変えたり、行を結合・分割したりしないでください',
 '- 🔒 の行は変更不可です（College Boardの英語原文、公式の日本語訳、英語の公式名称）。そのまま残してください',
 '- 直してよいのは、🔒 のない日本語（当サイトの説明文・和訳・見出し・コツなど）です',
 '- `**太字**` はページ上のハイライトです。ハイライトしたい語句の範囲は変えてよいですが、`**` の記号は残してください',
 '- 行の中の英語の部分（Project Presentation、Scoring Criteria など）は公式の名称なので変えないでください',
 '- 事実（点数、比重、日付、時間、問題数、名称）は変えないでください',
 '- 文末の「。」は付けません（「A。B。」なら最後だけ取る）',
 '- 「〜しました」「〜をまとめています」のような作業報告の言い方は使わず、専門家が書いた文章にしてください',
 '- 和訳は、英語原文の意味からずれないようにしてください（意訳しすぎない）',
 '- 同じ文（和訳や見出し）が何度も出てくる場合は、すべて同じ直し方にしてください',
 '- 「｜」は、ページ上で別の部品（ラベル・数字・英語名など）に分かれている区切りです。消さずに残してください',
 '- 「/」は改行の位置です', '',
 '## ページ情報', '']
n = 0; MAP = {}
for k, v in meta:
    n += 1; key = '%04d' % n; MAP[key] = {'kind': 'meta-' + k, 'text': v}
    lines.append('[%s] （%s）%s' % (key, 'ページタイトル' if k == 'title' else '検索結果の説明文', v))
lines += ['', '## 本文', '']
for txt, lock, tag, head in items:
    n += 1; key = '%04d' % n; MAP[key] = {'tag': tag, 'text': txt, 'lock': bool(lock)}
    if head: lines.append('')
    pre = '#' * (2 if tag == 'h1' else 3) + ' ' if head else ''
    lines.append('[%s] %s%s%s' % (key, pre, '🔒 ' if lock else '', txt))
open('export/ap-japanese-text.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
json.dump(MAP, open('export/ap-japanese-map.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(n, sum(1 for v in MAP.values() if v.get('lock')))
