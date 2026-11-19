# -*- coding: utf-8 -*-
"""Apply edited wording (edits.json: id -> [original_render, new_text]) to the built AP Japanese page.
Blocks are matched by their rendered text (same rules as export_text.py), so it survives rebuilds."""
import json, os, re
from bs4 import BeautifulSoup, NavigableString, Comment

HERE = os.path.dirname(os.path.abspath(__file__))
INLINE = {'a', 'b', 'strong', 'em', 'i', 'small', 'span', 'br', 'sup', 'sub', 'code', 'mark', 'abbr', 'label', 'time'}
TEXTBOX = {'p', 'li', 'dd', 'dt', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'summary', 'figcaption', 'button'}
IGN_SEL = '.kt-n, .apc-tip, .apc-ts, .crumb, .byline, .sj-off, nav.otl, .step-n, .aut-n, .tp-no, .apx-ln, .amx-bs, .apo-dot, .cta, .nx, script, style, svg'


def md2html(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


def apply(html):
    E = json.load(open(os.path.join(HERE, 'edits.json'), encoding='utf-8'))
    M = {}
    for k, (o, n) in E.items():
        if k == '0002':
            continue
        if n.startswith('・'):
            n = n[1:]
        M[o] = n
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('main')
    ign = set(id(x) for x in main.select(IGN_SEL))

    def ignored(el):
        while el is not None and el.name != 'main':
            if id(el) in ign:
                return True
            el = el.parent
        return False

    def is_inline(el):
        if el.name not in INLINE:
            return False
        if el.name == 'a':
            p = el.parent
            for _ in range(3):
                if p is None:
                    break
                if p.name in TEXTBOX:
                    return True
                p = p.parent
            return False
        return True

    def segments(el):
        """Mirror export render(): returns (text, [segments]) where each segment is a list of nodes."""
        out, segs, cur = [], [], []
        prev = False
        for c in list(el.children):
            if isinstance(c, Comment):
                continue
            if isinstance(c, NavigableString):
                if c.strip():
                    if prev == 'span':
                        out.append(' ｜ '); segs.append(cur); cur = []
                    prev = False
                out.append(str(c)); cur.append(c); continue
            if id(c) in ign or not is_inline(c):
                continue
            if c.name == 'br':
                out.append(' / '); cur.append(c); continue
            if prev and c.get_text().strip() and c.name != 'a':
                out.append(' ｜ '); segs.append(cur); cur = []
            inner, _ = segments(c)
            if c.name in ('b', 'strong', 'em') and inner.strip():
                out.append('**%s**' % inner)
            elif c.name == 'small' and inner.strip():
                out.append(' ' + inner)
            else:
                out.append(inner)
            cur.append(c)
            prev = ('span' if c.name in ('span', 'i', 'small') else True) if c.get_text().strip() else False
        segs.append(cur)
        return re.sub(r'\s+', ' ', ''.join(out)).strip(), segs

    def block_of(node):
        p = node.parent
        while p is not None and is_inline(p):
            p = p.parent
        return p

    blocks, seen = [], set()
    for t in list(main.descendants):
        if isinstance(t, Comment) or not isinstance(t, NavigableString) or not t.strip():
            continue
        if ignored(t.parent):
            continue
        b = block_of(t)
        if id(b) in seen:
            continue
        seen.add(id(b)); blocks.append(b)

    done = 0
    for b in blocks:
        txt, segs = segments(b)
        if txt not in M:
            continue
        new = M[txt]
        parts = [p.strip() for p in new.split('｜')] if len(segs) > 1 else [new]
        if len(parts) != len(segs):
            print('skip (segments)', txt[:40]); continue
        oldparts = [p.strip() for p in txt.split('｜')] if len(segs) > 1 else [txt]
        W = lambda x: re.sub(r'\*\*|\s', '', x)
        for seg, part, op in zip(segs, parts, oldparts):
            if not part or W(part) == W(op):
                continue
            nodes = [n for n in seg if not (isinstance(n, NavigableString) and not n.strip())] or seg
            el = [n for n in nodes if not isinstance(n, NavigableString)]
            frag = BeautifulSoup(md2html(part), 'html.parser')
            if len(nodes) == 1 and el and el[0].name in ('b', 'strong'):
                # whole segment was bold: keep tag, set inner without ** markers
                el[0].clear(); el[0].append(BeautifulSoup(md2html(re.sub(r'^\*\*(.*)\*\*$', r'\1', part)), 'html.parser'))
            elif len(nodes) == 1 and el and el[0].name in ('span', 'small', 'i', 'em', 'a') and not el[0].find(['a']):
                el[0].clear(); el[0].append(frag)
            else:
                links = [(a.get_text(), a) for n in nodes if not isinstance(n, NavigableString) for a in ([n] if n.name == 'a' else n.find_all('a'))]
                wraps = [(x.get_text().strip(), x.name, dict(x.attrs)) for x in nodes if not isinstance(x, NavigableString) and x.name in ('small', 'a') and x.get_text().strip()]
                parent = nodes[0].parent
                first = nodes[0]
                anchor = soup.new_string('')
                first.insert_before(anchor)
                for n in nodes:
                    n.extract()
                for child in list(frag.contents):
                    anchor.insert_before(child)
                anchor.extract()
                for wt, wn, wa in wraps:
                    for t in list(parent.find_all(string=True, recursive=False)):
                        if wt in t:
                            pre, post = t.split(wt, 1)
                            tag = soup.new_tag(wn, attrs=wa); tag.string = wt
                            t.replace_with(tag)
                            if pre.strip() or pre: tag.insert_before(soup.new_string(pre.rstrip() if wn == 'small' else pre))
                            if post: tag.insert_after(soup.new_string(post))
                            break
                if links:
                    print('note: links in block', txt[:40])
        done += 1

    # popover data attributes follow the tip cards
    for art in main.select('article.tp'):
        h = art.find('h4'); g = art.select_one('.tp-gl')
        if h:
            t = ''.join(x if isinstance(x, str) else '' for x in h.strings)
            no = art.select_one('.tp-no')
            if no:
                t = h.get_text().replace(no.get_text(), '', 1)
            art['data-title'] = t.strip()
        if g:
            art['data-sum'] = g.get_text().strip()
    out = str(soup)
    # meta description
    o, n = E['0002']
    o = o.replace('（検索結果の説明文）', ''); n = n.replace('（検索結果の説明文）', '')
    out = out.replace(o, n)
    # TOC labels for edited section headings
    for k, (o2, n2) in E.items():
        out = out.replace('</span>%s</a></li>' % o2, '</span>%s</a></li>' % n2)
    out = out.replace('下線のある語句は、満点の条件に関わる言葉。押すとコツが表示されます', '下線の語句を押すと、満点に向けたコツを確認できます')
    out = out.replace('</i>どの単元の話題からも出題される</span>', '</i>6単元すべてが出題範囲</span>')
    out = re.sub(r'<h4>[^<]*(?:<small>[^<]*</small>)?\s*対象：インター生・帰国子女(?:</small>)?</h4>', '<h4>家庭教師<small>対象：インター生・帰国子女</small></h4>', out)
    out = re.sub(r'(\d+点の内訳)：(観点を選ぶと基準を確認できます)', r'\1<small>\2</small>', out)
    out = re.sub(r'(Q\dのコツ) ?(採点基準に基づく当サイトの解説。College Board公式の攻略法ではありません)', r'\1<small>\2</small>', out)
    out = out.replace('sj-plan-tg">授業料・受講方法<', 'sj-plan-tg">プラン<')
    print('applied', done, 'of', len(M))
    return out
