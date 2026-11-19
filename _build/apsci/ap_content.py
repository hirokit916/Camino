# -*- coding: utf-8 -*-
"""AP subject pages: drop the 押さえておきたいポイント section (all AP pages except Japanese),
and render 学ぶ内容 as a unit-weighting table for science/math subjects with confirmed official weightings.
Idempotent. Usage: python3 ap_content.py /home/claude/camino-v2"""
import os, re, sys
ROOT = sys.argv[1]
AP = os.path.join(ROOT, 'subjects/ap')

MC = '選択式セクションでの出題比率'
UNITS = {
 'biology': ('試験での出題比率', 'College Board「AP Biology Course and Exam Description」', [
   ('生命の化学', 'Chemistry of Life', 8, 11), ('細胞', 'Cells', 10, 13), ('細胞のエネルギー代謝', 'Cellular Energetics', 12, 16),
   ('細胞間の情報伝達と細胞周期', 'Cell Communication and Cell Cycle', 10, 15), ('遺伝', 'Heredity', 8, 11),
   ('遺伝子の発現と調節', 'Gene Expression and Regulation', 12, 16), ('自然選択', 'Natural Selection', 13, 20), ('生態学', 'Ecology', 10, 15)]),
 'calculus-ab': (MC, 'College Board「AP Calculus AB」コースページ（AP Central、2026-27年度）', [
   ('極限と連続性', 'Limits and Continuity', 10, 15), ('微分：定義と基本的な性質', 'Differentiation: Definition and Fundamental Properties', 10, 15),
   ('微分：合成関数・陰関数・逆関数', 'Differentiation: Composite, Implicit, and Inverse Functions', 5, 10),
   ('微分の文脈での応用', 'Contextual Applications of Differentiation', 10, 15), ('微分の解析的な応用', 'Analytical Applications of Differentiation', 15, 20),
   ('積分と変化の蓄積', 'Integration and Accumulation of Change', 15, 20), ('微分方程式', 'Differential Equations', 5, 10),
   ('積分の応用', 'Applications of Integration', 10, 15)]),
 'calculus-bc': (MC, 'College Board「AP Calculus BC」コースページ（AP Central、2026-27年度）', [
   ('極限と連続性', 'Limits and Continuity', 5, 10), ('微分：定義と基本的な性質', 'Differentiation: Definition and Fundamental Properties', 5, 10),
   ('微分：合成関数・陰関数・逆関数', 'Differentiation: Composite, Implicit, and Inverse Functions', 5, 10),
   ('微分の文脈での応用', 'Contextual Applications of Differentiation', 5, 10), ('微分の解析的な応用', 'Analytical Applications of Differentiation', 10, 15),
   ('積分と変化の蓄積', 'Integration and Accumulation of Change', 15, 20), ('微分方程式', 'Differential Equations', 5, 10),
   ('積分の応用', 'Applications of Integration', 5, 10),
   ('媒介変数表示・極座標・ベクトル値関数', 'Parametric Equations, Polar Coordinates, and Vector-Valued Functions', 10, 15),
   ('無限数列と級数', 'Infinite Sequences and Series', 15, 20)]),
 'statistics': (MC, 'College Board「AP Statistics」コースページ（AP Central、2026-27年度の改訂版）', [
   ('1変数データの探索とデータの集め方', 'Exploring One-Variable Data and Collecting Data', 20, 30),
   ('確率・確率変数・確率分布', 'Probability, Random Variables, and Probability Distributions', 15, 25),
   ('カテゴリデータの推測：割合', 'Inference for Categorical Data: Proportions', 15, 25),
   ('量的データの推測：平均', 'Inference for Quantitative Data: Means', 10, 20), ('回帰分析', 'Regression Analysis', 10, 20)]),
}

AS = 'College Board「%s」コースページ（AP Students）'
EX = '試験での出題比率'
UNITS.update({
 'chemistry': (EX, AS % 'AP Chemistry', [
   ('原子の構造と性質', 'Atomic Structure and Properties', 7, 9), ('化合物の構造と性質', 'Compound Structure and Properties', 7, 9),
   ('物質と混合物の性質', 'Properties of Substances and Mixtures', 18, 22), ('化学反応', 'Chemical Reactions', 7, 9), ('反応速度', 'Kinetics', 7, 9),
   ('熱化学', 'Thermochemistry', 7, 9), ('化学平衡', 'Equilibrium', 7, 9), ('酸と塩基', 'Acids and Bases', 11, 15),
   ('熱力学と電気化学', 'Thermodynamics and Electrochemistry', 7, 9)]),
 'physics-1': (MC, AS % 'AP Physics 1: Algebra-Based', [
   ('運動学', 'Kinematics', 10, 15), ('力と並進運動の力学', 'Force and Translational Dynamics', 18, 23), ('仕事・エネルギー・仕事率', 'Work, Energy, and Power', 18, 23),
   ('運動量', 'Linear Momentum', 10, 15), ('トルクと回転運動の力学', 'Torque and Rotational Dynamics', 10, 15),
   ('回転する系のエネルギーと運動量', 'Energy and Momentum of Rotating Systems', 5, 8), ('振動', 'Oscillations', 5, 8), ('流体', 'Fluids', 10, 15)]),
 'physics-c-mechanics': (MC, AS % 'AP Physics C: Mechanics', [
   ('運動学', 'Kinematics', 10, 15), ('力と並進運動の力学', 'Force and Translational Dynamics', 20, 25), ('仕事・エネルギー・仕事率', 'Work, Energy, and Power', 15, 25),
   ('運動量', 'Linear Momentum', 10, 20), ('トルクと回転運動の力学', 'Torque and Rotational Dynamics', 10, 15),
   ('回転する系のエネルギーと運動量', 'Energy and Momentum of Rotating Systems', 10, 15), ('振動', 'Oscillations', 10, 15)]),
 'environmental-science': (EX, AS % 'AP Environmental Science', [
   ('生物界：生態系', 'The Living World: Ecosystems', 6, 8), ('生物界：生物多様性', 'The Living World: Biodiversity', 6, 8), ('個体群', 'Populations', 10, 15),
   ('地球のシステムと資源', 'Earth Systems and Resources', 10, 15), ('土地と水の利用', 'Land and Water Use', 10, 15),
   ('エネルギー資源と消費', 'Energy Resources and Consumption', 10, 15), ('大気汚染', 'Atmospheric Pollution', 7, 10),
   ('水域と陸域の汚染', 'Aquatic and Terrestrial Pollution', 7, 10), ('地球規模の変化', 'Global Change', 15, 20)]),
 'computer-science-a': (EX, AS % 'AP Computer Science A', [
   ('オブジェクトとメソッドの利用', 'Using Objects and Methods', 15, 25), ('条件分岐と繰り返し', 'Selection and Iteration', 25, 35),
   ('クラスの作成', 'Class Creation', 10, 18), ('データコレクション（配列・リストなど）', 'Data Collections', 30, 40)]),
 'precalculus': (MC, AS % 'AP Precalculus', [
   ('多項式関数と有理関数', 'Polynomial and Rational Functions', 30, 40), ('指数関数と対数関数', 'Exponential and Logarithmic Functions', 25, 40),
   ('三角関数と極座標の関数', 'Trigonometric and Polar Functions', 30, 35),
   ('媒介変数・ベクトル・行列を含む関数', 'Functions Involving Parameters, Vectors, and Matrices', None, None)]),
})
UNITS['biology'] = (EX, 'College Board「AP Biology Course and Exam Description」', UNITS['biology'][2])

CSS = '''<style id="apc-units">.apu2{margin:6px 0 8px;border:2px solid var(--c,#16294d);background:#fff}
.apu2-h,.apu2-r{display:grid;grid-template-columns:minmax(0,1fr) 210px;align-items:center;column-gap:18px}
.apu2-h{background:var(--c,#16294d);color:#fff;padding:10px 16px;font-size:12.5px;font-weight:700}
.apu2-h span:last-child{text-align:left}
.apu2-r{padding:12px 16px;border-top:1px solid #dde5f1}
.apu2-r:nth-child(odd){background:#f6f9fd}
.apu2-u{display:flex;align-items:center;gap:12px;min-width:0}
.apu2-n{flex:none;width:34px;height:34px;display:grid;place-items:center;background:#dce9f8;color:var(--c,#16294d);font-weight:800;font-size:14px;font-family:var(--latin)}
.apu2-u b{display:block;font-size:15px;color:var(--navy,#0b1f4b);line-height:1.4}
.apu2-u small{display:block;font-size:11.5px;color:var(--muted,#5c6984);line-height:1.4}
.apu2-w{display:grid;grid-template-columns:72px 1fr;align-items:center;gap:10px}
.apu2-p{font-size:16px;font-weight:800;color:var(--navy,#0b1f4b);font-variant-numeric:tabular-nums;white-space:nowrap}
.apu2-bar{position:relative;height:8px;background:#e6edf7}
.apu2-bar i{position:absolute;top:0;bottom:0;background:var(--c,#16294d)}
.apu2-x{background:#fafafa}.apu2-x .apu2-p{font-size:12px;font-weight:700;color:var(--muted,#5c6984)}
.apu2-src{font-size:11.5px;color:var(--muted,#5c6984);margin:6px 0 18px;line-height:1.7}
@media(max-width:700px){.apu2-h,.apu2-r{grid-template-columns:minmax(0,1fr) 92px;column-gap:10px}.apu2-r{padding:11px 12px}.apu2-h{padding:9px 12px}
.apu2-w{grid-template-columns:1fr;gap:4px}.apu2-u{gap:9px}.apu2-n{width:28px;height:28px;font-size:12px}.apu2-u b{font-size:14px}.apu2-p{font-size:14px}}</style>
'''


def units_html(cap, src, rows):
    top = max(r[3] for r in rows if r[3])
    def row(k, ja, en, lo, hi):
        if lo is None:
            return ('<div class="apu2-r apu2-x"><div class="apu2-u"><span class="apu2-n">%d</span><div><b>%s</b><small lang="en">Unit %d: %s</small></div></div>'
                    '<div class="apu2-w"><span class="apu2-p">試験範囲外</span><span></span></div></div>' % (k, ja, k, en))
        return ('<div class="apu2-r"><div class="apu2-u"><span class="apu2-n">%d</span><div><b>%s</b><small lang="en">Unit %d: %s</small></div></div>'
                '<div class="apu2-w"><span class="apu2-p">%d〜%d%%</span><span class="apu2-bar" aria-hidden="true"><i style="left:%.1f%%;width:%.1f%%"></i></span></div></div>'
                % (k, ja, k, en, lo, hi, lo / top * 100, (hi - lo) / top * 100))
    body = ''.join(row(k, *r) for k, r in enumerate(rows, 1))
    return ('<div class="apu2 rise" role="table" aria-label="単元と出題比率"><div class="apu2-h"><span>単元</span><span>%s</span></div>%s</div>'
            '<p class="apu2-src">出典：%s。比率は幅で示されたもの</p>' % (cap, body, src))


def renumber(s):
    k = 0
    def step(m):
        nonlocal k; k += 1
        return m.group(1) + str(k)
    s = re.sub(r'(<div class="step" id="[a-z]+"><span class="step-n">)\d+', step, s)
    k2 = 0
    def toc(m):
        nonlocal k2; k2 += 1
        return m.group(1) + str(k2)
    nav = re.search(r'<nav class="otl" aria-label="目次">.*?</nav>', s, re.S)
    if nav:
        n2 = re.sub(r'(<li(?: class="[^"]*")?><a href="#[a-z]+"><span>)\d+', toc, nav.group(0))
        s = s[:nav.start()] + n2 + s[nav.end():]
    return s


for d in sorted(os.listdir(AP)):
    f = os.path.join(AP, d, 'index.html')
    if d == 'japanese' or not os.path.isfile(f):
        continue
    s = open(f, encoding='utf-8').read(); o = s
    if 'class="ajs' in s:  # page owned by a dedicated builder (apjp / econ / psych / math)
        continue
    i = s.find('<div class="step" id="point">')
    if i >= 0:
        ends = [x for x in (s.find('<div class="step"', i + 10), s.find('<!--mjreq-->', i)) if x > 0]
        s = s[:i] + s[min(ends):]
        s = re.sub(r'<li><a href="#point"><span>\d+</span>[^<]*</a></li>', '', s)
    if d in UNITS and '<div class="step" id="content">' in s:
        cap, src, rows = UNITS[d]
        i = s.find('<div class="step" id="content">')
        j = s.find('</div></div>', i) + len('</div></div>')
        ends = [x for x in (s.find('<div class="step"', j), s.find('<!--mjreq-->', j)) if x > 0]
        k = min(ends)
        s = s[:j] + '\n' + units_html(cap, src, rows) + '\n' + s[k:]
        s = (re.sub(r'<style id="apc-units">.*?</style>\n', lambda m: CSS, s, count=1, flags=re.S) if '<style id="apc-units">' in s else s.replace('</head>', CSS + '</head>', 1))
    s = renumber(s)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
        print('updated', d)
