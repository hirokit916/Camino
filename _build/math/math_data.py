# -*- coding: utf-8 -*-
"""AP Calculus AB/BC and Precalculus. Sources: Course and Exam Descriptions (Calculus AB and BC; Precalculus) as provided,
unit names/weightings as on AP Central (2026-27). Official English kept verbatim."""

CALC_TOPICS = {
 1: ['Introducing Calculus: Can Change Occur at an Instant?', 'Defining Limits and Using Limit Notation', 'Estimating Limit Values from Graphs', 'Estimating Limit Values from Tables',
     'Determining Limits Using Algebraic Properties of Limits', 'Determining Limits Using Algebraic Manipulation', 'Selecting Procedures for Determining Limits',
     'Determining Limits Using the Squeeze Theorem', 'Connecting Multiple Representations of Limits', 'Exploring Types of Discontinuities', 'Defining Continuity at a Point',
     'Confirming Continuity over an Interval', 'Removing Discontinuities', 'Connecting Infinite Limits and Vertical Asymptotes',
     'Connecting Limits at Infinity and Horizontal Asymptotes', 'Working with the Intermediate Value Theorem (IVT)'],
 2: ['Defining Average and Instantaneous Rates of Change at a Point', 'Defining the Derivative of a Function and Using Derivative Notation', 'Estimating Derivatives of a Function at a Point',
     'Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist', 'Applying the Power Rule',
     'Derivative Rules: Constant, Sum, Difference, and Constant Multiple', 'Derivatives of cos x, sin x, e<sup>x</sup>, and ln x', 'The Product Rule', 'The Quotient Rule',
     'Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions'],
 3: ['The Chain Rule', 'Implicit Differentiation', 'Differentiating Inverse Functions', 'Differentiating Inverse Trigonometric Functions',
     'Selecting Procedures for Calculating Derivatives', 'Calculating Higher-Order Derivatives'],
 4: ['Interpreting the Meaning of the Derivative in Context', 'Straight-Line Motion: Connecting Position, Velocity, and Acceleration', 'Rates of Change in Applied Contexts Other Than Motion',
     'Introduction to Related Rates', 'Solving Related Rates Problems', 'Approximating Values of a Function Using Local Linearity and Linearization',
     'Using L’Hospital’s Rule for Determining Limits of Indeterminate Forms'],
 5: ['Using the Mean Value Theorem', 'Extreme Value Theorem, Global Versus Local Extrema, and Critical Points', 'Determining Intervals on Which a Function Is Increasing or Decreasing',
     'Using the First Derivative Test to Determine Relative (Local) Extrema', 'Using the Candidates Test to Determine Absolute (Global) Extrema', 'Determining Concavity of Functions over Their Domains',
     'Using the Second Derivative Test to Determine Extrema', 'Sketching Graphs of Functions and Their Derivatives', 'Connecting a Function, Its First Derivative, and Its Second Derivative',
     'Introduction to Optimization Problems', 'Solving Optimization Problems', 'Exploring Behaviors of Implicit Relations'],
 6: ['Exploring Accumulations of Change', 'Approximating Areas with Riemann Sums', 'Riemann Sums, Summation Notation, and Definite Integral Notation',
     'The Fundamental Theorem of Calculus and Accumulation Functions', 'Interpreting the Behavior of Accumulation Functions Involving Area', 'Applying Properties of Definite Integrals',
     'The Fundamental Theorem of Calculus and Definite Integrals', 'Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation', 'Integrating Using Substitution',
     'Integrating Functions Using Long Division and Completing the Square', 'BC:Integrating Using Integration by Parts', 'BC:Integrating Using Linear Partial Fractions',
     'BC:Evaluating Improper Integrals', 'Selecting Techniques for Antidifferentiation'],
 7: ['Modeling Situations with Differential Equations', 'Verifying Solutions for Differential Equations', 'Sketching Slope Fields', 'Reasoning Using Slope Fields',
     'BC:Approximating Solutions Using Euler’s Method', 'Finding General Solutions Using Separation of Variables',
     'Finding Particular Solutions Using Initial Conditions and Separation of Variables', 'Exponential Models with Differential Equations', 'BC:Logistic Models with Differential Equations'],
 8: ['Finding the Average Value of a Function on an Interval', 'Connecting Position, Velocity, and Acceleration of Functions Using Integrals',
     'Using Accumulation Functions and Definite Integrals in Applied Contexts', 'Finding the Area Between Curves Expressed as Functions of x', 'Finding the Area Between Curves Expressed as Functions of y',
     'Finding the Area Between Curves That Intersect at More Than Two Points', 'Volumes with Cross Sections: Squares and Rectangles', 'Volumes with Cross Sections: Triangles and Semicircles',
     'Volume with Disc Method: Revolving Around the x- or y-Axis', 'Volume with Disc Method: Revolving Around Other Axes', 'Volume with Washer Method: Revolving Around the x- or y-Axis',
     'Volume with Washer Method: Revolving Around Other Axes', 'BC:The Arc Length of a Smooth, Planar Curve and Distance Traveled'],
 9: ['Defining and Differentiating Parametric Equations', 'Second Derivatives of Parametric Equations', 'Finding Arc Lengths of Curves Given by Parametric Equations',
     'Defining and Differentiating Vector-Valued Functions', 'Integrating Vector-Valued Functions', 'Solving Motion Problems Using Parametric and Vector-Valued Functions',
     'Defining Polar Coordinates and Differentiating in Polar Form', 'Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve', 'Finding the Area of the Region Bounded by Two Polar Curves'],
 10: ['Defining Convergent and Divergent Infinite Series', 'Working with Geometric Series', 'The nth Term Test for Divergence', 'Integral Test for Convergence', 'Harmonic Series and p-Series',
      'Comparison Tests for Convergence', 'Alternating Series Test for Convergence', 'Ratio Test for Convergence', 'Determining Absolute or Conditional Convergence', 'Alternating Series Error Bound',
      'Finding Taylor Polynomial Approximations of Functions', 'Lagrange Error Bound', 'Radius and Interval of Convergence of Power Series', 'Finding Taylor or Maclaurin Series for a Function',
      'Representing Functions as Power Series'],
}
CALC_UNITS = [  # n, ja, en, AB weight, BC weight
 (1, '極限と連続性', 'Limits and Continuity', (10, 15), (5, 10)),
 (2, '微分：定義と基本的な性質', 'Differentiation: Definition and Fundamental Properties', (10, 15), (5, 10)),
 (3, '微分：合成関数・陰関数・逆関数', 'Differentiation: Composite, Implicit, and Inverse Functions', (5, 10), (5, 10)),
 (4, '微分の文脈での応用', 'Contextual Applications of Differentiation', (10, 15), (5, 10)),
 (5, '微分の解析的な応用', 'Analytical Applications of Differentiation', (15, 20), (10, 15)),
 (6, '積分と変化の蓄積', 'Integration and Accumulation of Change', (15, 20), (15, 20)),
 (7, '微分方程式', 'Differential Equations', (5, 10), (5, 10)),
 (8, '積分の応用', 'Applications of Integration', (10, 15), (5, 10)),
 (9, '媒介変数表示・極座標・ベクトル値関数', 'Parametric Equations, Polar Coordinates, and Vector-Valued Functions', None, (10, 15)),
 (10, '無限数列と級数', 'Infinite Sequences and Series', None, (15, 20)),
]
CALC_BIG = ['変化（Change）', '極限（Limits）', '関数の分析（Analysis of Functions）']
CALC_EXAM = [('sec', 'Section I', '選択式問題', 'Multiple-choice questions', '42', '50%', '1時間40分', ''),
             ('part', 'Part A', 'グラフ電卓なし', 'Graphing calculator not permitted', '29', '35%', '62分', ''),
             ('part', 'Part B', 'グラフ電卓が必要', 'Graphing calculator required', '13', '15%', '38分', ''),
             ('sec', 'Section II', '記述問題', 'Free-response questions', '6', '50%', '1時間30分', ''),
             ('part', 'Part A', 'グラフ電卓が必要', 'Graphing calculator required', '2', '16.7%', '30分', ''),
             ('part', 'Part B', 'グラフ電卓なし', 'Graphing calculator not permitted', '4', '33.3%', '60分', '')]
CALC_MC_PR = [('数学的な処理を実行する', 'Implementing Mathematical Processes', '50〜70%'), ('表現をつなぐ', 'Connecting Representations', '15〜30%'), ('正当化', 'Justification', '10〜20%')]
CALC_FR_PR = [('数学的な処理を実行する', 'Implementing Mathematical Processes', '35〜60%'), ('表現をつなぐ', 'Connecting Representations', '10〜20%'),
              ('正当化', 'Justification', '35〜60%'), ('伝え方と記法', 'Communication and Notation', '10〜25%')]
CALC_VERBS = [
 ('Approximate', 'Use rounded decimal values or other estimates in calculations, which require writing an expression to show work.', '四捨五入した小数などの概算を使って計算する。<b>式を書いて途中を示す</b>ことが必要'),
 ('Calculate/Write an expression', 'Write an appropriate expression or equation to answer a question. Unless otherwise directed, calculations also require evaluating an expression or solving an equation, but the expression or equation must also be presented to show work.',
  '問いに答える式や方程式を書く。指示がなければ値の計算まで求められるが、<b>式そのものも書いて</b>途中を示す必要がある'),
 ('Determine', 'Apply an appropriate definition, theorem, or test to identify values, intervals, or solutions whose existence or uniqueness can be established.', '適切な定義・定理・判定法を使って、値・区間・解を特定する'),
 ('Estimate', 'Use models or representations to find approximate values for functions.', 'モデルや表現を使って、関数の近似値を求める'),
 ('Evaluate', 'Apply mathematical processes, including the use of appropriate rounding procedures, to find the value of an expression at a given point or over a given interval.', '適切な丸め方を含む数学的な処理で、式の値を求める'),
 ('Explain', 'Use appropriate definitions or theorems to provide reasons or rationales for solutions and conclusions.', '適切な定義や定理を使って、解や結論の理由を示す'),
 ('Identify/Indicate', 'Indicate or provide information about a specified topic, without elaboration or explanation.', '指定された内容を、説明を加えずに答える'),
 ('Interpret', 'Describe the connection between a mathematical expression or solution and its meaning within the realistic context of a problem, often including consideration of units.',
  '式や解が、問題の現実の場面で何を意味するかを説明する。<b>単位</b>まで考えることが多い'),
 ('Justify', 'Identify a logical sequence of mathematical definitions, theorems, or tests to support an argument or conclusion, explain why these apply, and then apply them.',
  '結論を支える定義・定理・判定法を順序立てて示し、<b>なぜそれが使えるか（条件）を説明したうえで</b>適用する'),
 ('Represent', 'Use appropriate graphs, symbols, words, and/or tables of numerical values to describe mathematical concepts, characteristics, and/or relationships.', 'グラフ・記号・言葉・数値の表で、数学的な概念や関係を表す'),
 ('Verify', 'Confirm that the conditions of a mathematical definition, theorem, or test are met in order to explain why it applies in a given situation. Alternately, confirm that solutions are accurate and appropriate.',
  '定義・定理・判定法の<b>条件が満たされていることを確認</b>して、それが使える理由を説明する。または、解が正確で適切かを確かめる'),
]
CALC_TIPS = [
 ('式を書いてから、電卓で値を出す', '「Calculate」「Approximate」は、式を書くことが条件です。電卓で出した数字だけでは点になりません。積分や微分の式を立ててから、値を書きます'),
 ('小数は3桁まで正確に', 'グラフ電卓のパートでは、途中で丸めずに計算し、答えは小数点以下3桁まで正確に書くのが原則です。途中の値は電卓に保存して使います'),
 ('「Justify」は定理の名前と条件までセットで', '平均値の定理や中間値の定理を使うときは、名前を書くだけでなく、<b>連続性・微分可能性などの条件</b>を満たしていることを示してから適用します。記述の配点では正当化が35〜60%を占めます'),
 ('答えは文脈と単位で言い直す', '「Interpret」では、値の意味を問題の場面に戻して、単位をつけて説明します。「t = 3のとき、水の量は毎分2.5リットルの割合で増えている」のように書きます'),
 ('記法を正しく使う', '極限・微分・積分の記法の誤り（lim の書き忘れ、dx の抜け、等号のつなぎ方）は、伝え方と記法の観点で減点の対象になります'),
]

PC_TOPICS = {
 1: ['Change in Tandem', 'Rates of Change', 'Rates of Change in Linear and Quadratic Functions', 'Polynomial Functions and Rates of Change', 'Polynomial Functions and Complex Zeros',
     'Polynomial Functions and End Behavior', 'Rational Functions and End Behavior', 'Rational Functions and Zeros', 'Rational Functions and Vertical Asymptotes', 'Rational Functions and Holes',
     'Equivalent Representations of Polynomial and Rational Expressions', 'Transformations of Functions', 'Function Model Selection and Assumption Articulation', 'Function Model Construction and Application'],
 2: ['Change in Arithmetic and Geometric Sequences', 'Change in Linear and Exponential Functions', 'Exponential Functions', 'Exponential Function Manipulation',
     'Exponential Function Context and Data Modeling', 'Competing Function Model Validation', 'Composition of Functions', 'Inverse Functions', 'Logarithmic Expressions',
     'Inverses of Exponential Functions', 'Logarithmic Functions', 'Logarithmic Function Manipulation', 'Exponential and Logarithmic Equations and Inequalities',
     'Logarithmic Function Context and Data Modeling', 'Semi-log Plots'],
 3: ['Periodic Phenomena', 'Sine, Cosine, and Tangent', 'Sine and Cosine Function Values', 'Sine and Cosine Function Graphs', 'Sinusoidal Functions', 'Sinusoidal Function Transformations',
     'Sinusoidal Function Context and Data Modeling', 'The Tangent Function', 'Inverse Trigonometric Functions', 'Trigonometric Equations and Inequalities',
     'The Secant, Cosecant, and Cotangent Functions', 'Equivalent Representations of Trigonometric Functions', 'Trigonometry and Polar Coordinates', 'Polar Function Graphs', 'Rates of Change in Polar Functions'],
 4: ['Parametric Functions', 'Parametric Functions Modeling Planar Motion', 'Parametric Functions and Rates of Change', 'Parametrically Defined Circles and Lines', 'Implicitly Defined Functions',
     'Conic Sections', 'Parametrization of Implicitly Defined Functions', 'Vectors', 'Vector-Valued Functions', 'Matrices', 'The Inverse and Determinant of a Matrix',
     'Linear Transformations and Matrices', 'Matrices as Functions', 'Matrices Modeling Contexts'],
}
PC_UNITS = [(1, '多項式関数と有理関数', 'Polynomial and Rational Functions', (30, 40)), (2, '指数関数と対数関数', 'Exponential and Logarithmic Functions', (25, 40)),
            (3, '三角関数と極座標の関数', 'Trigonometric and Polar Functions', (30, 35)), (4, '媒介変数・ベクトル・行列を含む関数', 'Functions Involving Parameters, Vectors, and Matrices', None)]
PC_EXAM = [('sec', 'Section I', '選択式問題', 'Multiple-choice questions', '42', '62.5%', '1時間45分', ''),
           ('part', 'Part A', '電卓なし', 'No calculator permitted', '29', '43.75%', '65分', ''),
           ('part', 'Part B', 'グラフ電卓が必要', 'Graphing calculator required', '13', '18.75%', '40分', ''),
           ('sec', 'Section II', '記述問題', 'Free-response questions', '4', '37.5%', '70分', '各6点。4問の比重は同じ'),
           ('part', 'Part A', 'グラフ電卓が必要', 'Graphing calculator required', '2', '18.75%', '35分', 'Q1 関数の概念、Q2 非周期的な現象のモデル化'),
           ('part', 'Part B', '電卓なし', 'No calculator permitted', '2', '18.75%', '35分', 'Q3 周期的な現象のモデル化、Q4 式の変形')]
PC_FTYPES = [('一般の関数（非解析的）', 'General Functions (non-analytical)', '1・2', '15〜25%'), ('多項式関数と有理関数', 'Polynomial and Rational Functions', '1', '20〜25%'),
             ('指数関数と対数関数', 'Exponential and Logarithmic Functions', '2', '20〜30%'), ('三角関数と極座標の関数', 'Trigonometric and Polar Functions', '3', '30〜35%')]
PC_PRACT = [('手続きと記号の運用', 'Procedural and Symbolic Fluency', '35〜50%'), ('複数の表現', 'Multiple Representations', '20〜30%'), ('伝え方と推論', 'Communication and Reasoning', '30〜40%')]
PC_FRQ = [
 ('Q1', '関数の概念', 'Function Concepts', '1・2', 'あり', 'なし',
  'Question 1: Function Concepts (graphing calculator) presents functions expressed graphically, numerically, and analytically. The question includes three parts and requires students to work with a variety of concepts. These may include function composition, inverse functions, function input-output values, zeros of a function, asymptotic behavior and end behavior of a function, and identification of an appropriate function type to construct a function model.',
  'グラフ・表・式で表された関数について、3つの小問に答える。合成関数、逆関数、入力と出力の値、関数の零点、漸近線と端の振る舞い、モデルに適した関数の種類の特定などを扱う'),
 ('Q2', '非周期的な現象のモデル化', 'Modeling a Non-Periodic Context', '1・2', 'あり', 'あり',
  'Question 2: Modeling a Non-Periodic Context (graphing calculator) presents a real-life context. In Part A, students use the given information to construct a function model by building a system of equations and finding the parameters using a method of choice. Function types include polynomial, piecewise-defined, exponential, and logarithmic. In Part B, students calculate and apply average rates of change and their units. In Part C, students answer a question about the model in context and justify a conclusion about assumptions or limitations of the model.',
  '現実の場面が示される。Part Aでは連立方程式を立ててパラメータを求め、関数モデルをつくる（多項式・区分的に定義された関数・指数・対数）。Part Bでは平均変化率とその<b>単位</b>を計算・活用し、Part Cではモデルの<b>前提や限界</b>について結論を正当化する'),
 ('Q3', '周期的な現象のモデル化', 'Modeling a Periodic Context', '3', 'なし', 'あり',
  'Question 3: Modeling a Periodic Context (no calculator) presents a real-life context that is modeled by a sinusoidal function. In Part A, students use the given information to identify coordinates of five labeled points on the graph of the sinusoidal function and its midline for two full cycles. In Part B, students find the parameters of an analytical presentation of the sinusoidal function. Both Parts A and B require students to construct the sinusoidal model by using the context to determine the vertical dilation and vertical translation of the sine or cosine function (amplitude and vertical shift), and the horizontal dilation and horizontal translation of the sine or cosine function (period and phase shift). In Part C, students answer questions about the behavior of the function, the concavity of the graph, and whether the rate of change is increasing or decreasing on a particular interval.',
  '正弦曲線で表される現実の場面。Part Aではグラフ上の5つの点と中心線の座標を特定し、Part Bでは式のパラメータを求める。どちらも<b>振幅・上下の平行移動・周期・位相のずれ</b>を場面から決める必要がある。Part Cでは関数の振る舞い、グラフの凹凸、変化率が増えるか減るかに答える'),
 ('Q4', '式の変形', 'Symbolic Manipulations', '2・3', 'なし', 'なし',
  'Question 4: Symbolic Manipulations (no calculator) presents several functions: exponential, logarithmic, trigonometric, and/or inverse trigonometric. Two parts of the question require students to solve equations using given functions. The third part of the question requires students to rewrite given function expressions in equivalent forms. In this question, students must (1) determine the exact values of expressions that can be obtained without a calculator (2) use algebraic methods and rules for exponents and logarithms to combine terms (3) show the work that leads to their answers in each part of the question.',
  '指数・対数・三角・逆三角関数が示される。2つの小問で方程式を解き、1つの小問で式を同値な形に書き換える。①電卓なしで<b>正確な値</b>を求める ②指数・対数の法則で項をまとめる ③<b>答えに至る途中の計算をすべて示す</b>ことが求められる'),
]
PC_SKILLPTS = {'Q1': (1, 0, 1, 2, 0, 1, 0, 1), 'Q2': (0, 1, 2, 0, 0, 0, 2, 1), 'Q3': (0, 0, 2, 1, 2, 1, 0, 0), 'Q4': (4, 2, 0, 0, 0, 0, 0, 0)}
PC_INSTR = [
 ('Show all of your work. Your work will be scored on the correctness and completeness of your responses, including your supporting work and answers. Answers without supporting work may not receive credit in cases where supporting work is requested.',
  '<b>途中の考え方をすべて書く</b>。答えだけでなく、途中の式や説明も含めて、正しさと完全さで採点される。途中の説明が求められている問題では、答えだけでは点にならないことがある'),
 ('Avoid rounding intermediate computations on the way to the final result. Unless otherwise specified, any decimal approximations reported in your work should be accurate to three places after the decimal point.',
  '途中の計算で丸めない。指示がなければ、小数の近似値は<b>小数点以下3桁まで</b>正確に書く（Part A）'),
 ('Unless otherwise specified, the domain of a function f is assumed to be the set of all real numbers x for which f (x) is a real number.', '指示がなければ、関数の定義域は f(x) が実数になるすべての実数 x とみなす'),
]
PC_VERBS = [
 ('Construct/write a function/expression/equation/model', 'Develop an analytical representation, with and without technology, that is consistent with a scenario, data set, or other criteria.', '場面やデータに合う式（関数・方程式・モデル）を、電卓を使って、または使わずにつくる'),
 ('Describe', 'Develop a verbal representation that is consistent with a scenario, data set, function representation, or other criteria.', '場面・データ・関数に合う内容を、言葉で表す'),
 ('Determine/Find/Identify', 'Apply appropriate methods or processes for answering a question.', '適切な方法で問いに答える'),
 ('Estimate/Compare', 'Use a function representation to find approximate values and/or compare results.', '関数の表現を使って近似値を求めたり、結果を比べたりする'),
 ('Explain/Give a reason/Provide a rationale/Justify', 'Use information from the scenario or function representation to provide reasons or rationales for solutions or conclusions.', '場面や関数の情報を使って、解や結論の理由を示す'),
 ('Express/Indicate', 'Provide information or a result in a desired form or include units as part of the answer to a question.', '求められた形で答える。<b>単位</b>を答えに含める'),
 ('Interpret', 'Describe the connection between a mathematical expression or solution and its meaning within the realistic context of a problem, often including consideration of units.', '式や解が、問題の現実の場面で何を意味するかを説明する。単位まで考えることが多い'),
 ('Plot and label, sketch and label', 'Develop a graphical representation that is consistent with a scenario, data set, or other criteria.', '場面やデータに合うグラフを描き、<b>ラベル</b>を付ける'),
 ('Rewrite', 'Apply appropriate methods to determine/find equivalent analytical representations of an expression.', '式を同値な別の形に書き換える'),
 ('Solve', 'Apply appropriate methods to determine/find solutions to an equation or inequality.', '方程式や不等式の解を求める'),
]
PC_TIPS = [
 ('途中の計算をすべて書く', '採点は「正しさと完全さ」で行われ、途中の説明が求められる問題では答えだけでは点になりません。とくにQ4（式の変形）は、使った指数・対数の法則が見えるように一行ずつ書きます'),
 ('平均変化率には単位をつける', 'Q2のPart Bでは、平均変化率の値だけでなく<b>単位</b>（例：人／年、ドル／月）まで答えます。単位がないと、場面に即した答えとみなされません'),
 ('正弦曲線は「振幅・中心線・周期・位相」を順に決める', 'Q3は電卓なしで、場面から正弦曲線のモデルをつくります。最大値と最小値から中心線と振幅、1周期の長さから周期、始まりの位置から位相のずれを順に決めると、グラフの5点も式も迷わず書けます'),
 ('モデルの前提と限界を、場面の言葉で言う', 'Q2のPart Cでは、モデルがどんな前提に立っているか、どこまで当てはまるかを、問題の場面の言葉で説明します。「このモデルは〜の範囲でしか成り立たない」のように具体的に書きます'),
 ('電卓パートは小数点以下3桁、電卓なしパートは正確な値', 'Part A（電卓あり）では途中で丸めず、答えは小数点以下3桁。Part B（電卓なし）では√2やπを含む<b>正確な値</b>で答えます。グラフ電卓は弧度法（radian）に設定しておきます'),
]
