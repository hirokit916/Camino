# -*- coding: utf-8 -*-
"""AP Micro / Macro data from the Course and Exam Descriptions (Effective Fall 2026, V.1). Official English kept verbatim."""

G, E, N, A = 'graph', 'explain', 'num', 'assert'
TASK = {G: ('グラフ・図を描く', 'Create graphs or visual representations'),
        E: ('説明する', 'Explain'),
        N: ('数値で分析する', 'Perform numerical analysis'),
        A: ('主張を述べる', 'Make an assertion')}

VERBS = [
 ('Identify. What? Which? Will? and other interrogatory words', 'Identify or provide information about a specified topic, without elaboration or explanation.',
  '指定された内容について、説明を加えずに答える'),
 ('Explain', 'Provide information about how or why a relationship, pattern, position, situation, or outcome occurs using evidence and/or reasoning. Graphs and symbols are acceptable as part of the explanation.',
  '関係・傾向・状況・結果が、どのように、なぜ起きるのかを、根拠や理由を示して説明する。説明の一部としてグラフや記号を使ってもよい'),
 ('Calculate', 'Perform mathematical steps to arrive at a final answer. Showing work is required.',
  '計算の手順を踏んで答えを出す。<b>途中の計算を示すことが必要</b>'),
 ('Draw a correctly labeled', 'Create a graph or visual representation that illustrates or explains relationships or phenomena. Labels are required.',
  '関係や現象を表すグラフ・図を描く。<b>ラベルが必要</b>'),
 ('Show/Label/Plot/Indicate', 'Show, label, plot, or indicate an economic scenario on a graph or visual representation created by the student. Clearly labeling all axes and curves and showing directional changes where relevant is required.',
  '自分で描いたグラフ・図の上に、経済の状況を示す。<b>すべての軸と曲線のラベル</b>と、必要に応じて<b>変化の方向</b>をはっきり示すことが必要'),
]

COMMON_TIPS = {
 G: ('軸・曲線・記号のラベルをすべて書く', '「Draw a correctly labeled」の問題は、ラベルがなければ点になりません。縦軸（Price）と横軸（Quantity）、D・S・MCなどの曲線、問題で指定された記号（QM、$5など）を、指定どおりの名前で書きます。変化を示すときは、新しい曲線（D1、D2など）と矢印で方向をはっきりさせます'),
 E: ('「結論」と「理由」をセットで書く', '採点基準の多くは「State that … and explain that …」の形です。増える・減るといった結論だけでは点にならず、「なぜそうなるのか」を経済の仕組みでつなげて、はじめて1点になります。because を使い、原因から結果までの流れを一文で示します'),
 N: ('式と途中の計算を必ず書く', '「Calculate」は途中の計算を示すことが求められます。答えの数字だけでなく、使った式と代入した数値を書きます。単位（$、%）も忘れずに付けます'),
 A: ('増える・減る・変わらないを、一言ではっきり言う', '「State that …」の点は、結論が正しく、はっきり書かれているかで決まります。「増える」「減る」「変わらない」「代替財である」のように、問われたことに一言で答えます。迷いを見せる書き方や、二つの答えを並べる書き方は避けます'),
}

MICRO = dict(
 slug='microeconomics', ja='ミクロ経済', en='Microeconomics', date='2027年5月4日（火）午後',
 bigideas=['希少性と市場（Scarcity and Markets）', '費用・便益と限界分析（Costs, Benefits, and Marginal Analysis）', '生産の選択と行動（Production Choices and Behavior）', '市場の非効率と公共政策（Market Inefficiency and Public Policy）'],
 units=[
  ('1', '基本的な経済概念', 'Basic Economic Concepts', 12, 15, ['希少性', '資源配分と経済体制', '生産可能性曲線', '比較優位と貿易', '費用便益分析', '限界分析と消費者の選択']),
  ('2', '需要と供給', 'Supply and Demand', 20, 25, ['需要', '供給', '需要の価格弾力性', '供給の価格弾力性', 'その他の弾力性', '市場均衡と消費者余剰・生産者余剰', '市場の不均衡と均衡の変化', '市場への政府介入の影響', '国際貿易と公共政策']),
  ('3', '生産・費用と完全競争モデル', 'Production, Cost, and the Perfect Competition Model', 22, 25, ['生産関数', '短期の生産費用', '長期の生産費用', '利潤の種類', '利潤最大化', '企業の短期の生産と長期の参入・退出の判断', '完全競争']),
  ('4', '不完全競争', 'Imperfect Competition', 15, 22, ['不完全競争市場とは', '独占', '価格差別', '独占的競争', '寡占とゲーム理論']),
  ('5', '生産要素市場', 'Factor Markets', 10, 13, ['生産要素市場とは', '要素需要と要素供給の変化', '完全競争の要素市場での利潤最大化', '買い手独占（モノプソニー）の市場']),
  ('6', '市場の失敗と政府の役割', 'Market Failure and the Role of Government', 8, 13, ['社会的に効率的な結果と非効率な結果', '外部性', '公共財と私的財', '市場構造ごとの政府介入の影響', '所得の不平等'])],
 mc_skills=[('原理とモデル', 'Principles and Models', '30〜42%'), ('結果の解釈', 'Interpretation', '37〜47%'), ('状況の操作・変化の予測', 'Manipulation', '16〜25%')],
 mc_num='20〜30%',
 frq_tasks=[(G, '30〜50%'), (E, '25〜35%'), (N, '15〜30%'), (A, '10〜20%')],
 frq_units={'q1': '2・3・5・6', 'q2': '4'},
 qs={
  'q1': dict(kind='Long', pts=10, title='完全競争の市場と価格の下限（ポテトの市場）',
     scene='完全競争で費用一定のポテト産業が長期均衡にあり、市場価格は1袋5ドル。政府が1袋7ドルの価格の下限を設け、余った分を買い取る',
     parts=[
      ('a', '市場と農家のグラフ', [
        ('Draw a correctly labeled graph of the potato market that shows the market equilibrium quantity and price labeled Q<sub>M</sub> and $5, respectively.', 'ポテト市場のグラフを正しいラベル付きで描き、市場の均衡数量と価格をそれぞれQ<sub>M</sub>と$5と示す', G, '4.A'),
        ('Draw a correctly labeled graph for farmer Lamo next to the graph of the potato market that shows a horizontal demand curve for Lamo coming from the market equilibrium price of $5.', '市場のグラフの隣に、農家ラモのグラフを正しいラベル付きで描き、市場価格$5から伸びる<b>水平な需要曲線</b>を示す', G, '4.A'),
        ('Show the profit-maximizing quantity Q<sub>L</sub>, where P = MC.', '利潤を最大にする数量Q<sub>L</sub>を、<b>P＝MC</b>となる点で示す', G, '4.B'),
        ('Show the ATC curve tangent to Lamo’s demand curve at Q<sub>L</sub>.', 'Q<sub>L</sub>でラモの需要曲線に<b>接するATC曲線</b>を示す', G, '4.B')]),
      ('b', '価格の下限の効果', [
        ('(i) On the graph from part (a), show the market quantity of potatoes that would be supplied at the price floor, labeled Q<sub>F</sub>.', '(i) (a)のグラフに、価格の下限のもとで供給される市場の数量を、Q<sub>F</sub>として示す', G, '4.C'),
        ('(ii) On the graph from part (a), show the profit farmer Lamo earns with the price floor, shaded completely.', '(ii) (a)のグラフに、価格の下限のもとでラモが得る利潤を、<b>すき間なく塗りつぶして</b>示す', G, '4.C')]),
      ('c', '消費者の支出', [
        ('State that consumer spending on potatoes will increase and explain that because the demand for potatoes is inelastic, the price increase will result in an increase in total spending. (It is also acceptable to explain that because demand is inelastic, the percentage increase in price outweighs the percentage decrease in the quantity demanded of potatoes, resulting in an increase in total spending on potatoes.)',
         'ポテトへの支出が<b>増える</b>と述べ、需要が<b>非弾力的</b>なので、価格の上昇が支出の総額の増加につながると説明する（需要が非弾力的なので、価格の上昇率が需要量の減少率を上回り、支出の総額が増える、という説明でもよい）', E, '3.C')]),
      ('d', '労働需要', [
        ('State that the demand for labor will increase and/or the demand curve will shift to the right.', '労働の需要が<b>増える</b>、または需要曲線が<b>右へ移動する</b>と述べる', A, '3.B')]),
      ('e', '関連する市場', [
        ('(i) State that the equilibrium price of corn will increase and the equilibrium quantity of corn will decrease.', '(i) トウモロコシの均衡価格は<b>上がり</b>、均衡数量は<b>減る</b>と述べる', A, '3.B'),
        ('(ii) State that potatoes and rice are substitutes in consumption.', '(ii) ポテトと米は、消費において<b>代替財</b>であると述べる', A, '2.A')])]),
  'q2': dict(kind='Short', pts=5, title='寡占とゲーム理論（2つの店の利得表）',
     scene='2つのディスカウント店が、人気の運動靴をセールに入れるかどうかを決める。利得表が与えられ、2店は協力しない',
     parts=[
      ('a', '利得表を読む', [('State that Bargain Floor’s profit will be $250.', 'Bargain Floorの利潤は<b>$250</b>と述べる', N, '1.C')]),
      ('b', '支配戦略', [('State yes and identify that including the shoes in its sale is the dominant strategy for Bargain Floor.', '「ある」と述べ、Bargain Floorにとって靴をセールに入れることが<b>支配戦略</b>だと示す', N, '1.C')]),
      ('c', 'ナッシュ均衡でない理由', [('Explain that it is not a Nash equilibrium because Bargain Floor has an incentive to move to including the shoes in its sale, earning $30 more ($250>$220).', 'Bargain Floorには靴をセールに入れる方へ変える<b>動機があり</b>、$30多く得られる（$250＞$220）ため、ナッシュ均衡ではないと説明する', E, '2.C')]),
      ('d', 'ナッシュ均衡', [('Identify the Nash equilibrium strategy for each store as choosing to include the shoes in the sale.', '各店のナッシュ均衡の戦略は、靴を<b>セールに入れる</b>ことだと示す', N, '2.C')]),
      ('e', '協力した場合', [('State yes and explain that by both agreeing to not include the shoes in their sales, they would both increase their profits.', '「変わる」と述べ、両店が靴をセールに入れないと合意すれば、<b>どちらも利潤が増える</b>と説明する', E, '3.C')])]),
 })

MACRO = dict(
 slug='macroeconomics', ja='マクロ経済', en='Macroeconomics', date='2027年5月7日（金）午後',
 bigideas=['経済の計測（Economic Measurements）', '市場（Markets）', 'マクロ経済のモデル（Macroeconomic Models）', 'マクロ経済政策（Macroeconomic Policies）'],
 units=[
  ('1', '基本的な経済概念', 'Basic Economic Concepts', 5, 10, ['希少性', '機会費用と生産可能性曲線', '比較優位と交易の利益', '需要', '供給', '市場の均衡・不均衡と均衡の変化']),
  ('2', '経済指標と景気循環', 'Economic Indicators and the Business Cycle', 12, 17, ['経済循環とGDP', 'GDPの限界', '失業', '物価指数とインフレ', 'インフレのコスト', '実質GDPと名目GDP', '景気循環']),
  ('3', '国民所得と物価水準の決定', 'National Income and Price Determination', 17, 27, ['総需要（AD）', '乗数', '短期総供給（SRAS）', '長期総供給（LRAS）', 'AD-ASモデルの均衡', 'AD-ASモデルの短期の変化', '長期の自己調整', '財政政策', '自動安定化装置']),
  ('4', '金融部門', 'Financial Sector', 18, 23, ['金融資産', '名目金利と実質金利', '貨幣の定義・計測・機能', '銀行と貨幣供給の拡大', '貨幣市場', '金融政策', '貸付資金市場']),
  ('5', '安定化政策の長期的な影響', 'Long-Run Consequences of Stabilization Policies', 20, 30, ['短期と長期の財政政策・金融政策', 'フィリップス曲線', '貨幣の増加とインフレ', '財政赤字と国の債務', 'クラウディングアウト', '経済成長', '公共政策と経済成長']),
  ('6', '開放経済：国際貿易と国際金融', 'Open Economy—International Trade and Finance', 10, 13, ['国際収支', '為替レート', '外国為替市場', '政策と経済状況の変化が外国為替市場に与える影響', '外国為替市場の変化と純輸出', '実質金利と国際的な資本の移動'])],
 mc_skills=[('原理とモデル', 'Principles and Models', '30〜40%'), ('結果の解釈', 'Interpretation', '25〜32%'), ('状況の操作・変化の予測', 'Manipulation', '30〜40%')],
 mc_num='16〜20%',
 frq_tasks=[(G, '30〜50%'), (E, '25〜35%'), (N, '10〜25%'), (A, '10〜20%')],
 frq_units={'q1': '3・4・6', 'q2': '2・3・5'},
 qs={
  'q1': dict(kind='Long', pts=10, title='AD-ASモデル・金融政策・外国為替（ゼートランド）',
     scene='ゼートランドは短期均衡にあり、実際の失業率（5%）が自然失業率（6%）を下回る。期待インフレ率は4%、均衡実質金利は3%',
     parts=[
      ('a', 'AD-ASのグラフ', [
        ('Draw a correctly labeled aggregate demand-aggregate supply graph that shows PL1 and Y1 at the intersection of AD and SRAS.', '総需要・総供給のグラフを正しいラベル付きで描き、<b>ADとSRASの交点</b>にPL1とY1を示す', G, '4.A'),
        ('For the second point, the graph must show a vertical LRAS curve to the left of Y1 and label the full employment output YF.', '2点目には、Y1の<b>左側に垂直なLRAS曲線</b>を描き、完全雇用の産出量YFとラベルを付ける必要がある', G, '4.B')]),
      ('b', '長期の自己調整', [
        ('Explain that short-run aggregate supply will decrease in the long run as a result of an increase in nominal wages, input prices, and/or inflationary expectations.', '名目賃金・投入物の価格・インフレ期待の<b>上昇</b>によって、長期的に<b>短期総供給が減少する</b>と説明する', E, '3.A')]),
      ('c', '金融政策', [
        ('State that the central bank would increase its administered interest rates (e.g., increase interest on reserves).', '中央銀行は、自ら設定する金利を<b>引き上げる</b>（例：準備預金への付利を引き上げる）と述べる', A, '2.A')]),
      ('d', '短期的な影響', [
        ('(i) State that the price of previously issued bonds in Zeetoland would decrease.', '(i) すでに発行された債券の価格は<b>下がる</b>と述べる', A, '3.A'),
        ('(ii) State that real output in Zeetoland would decrease and explain that the increase in nominal interest rates in Zeetoland would decrease interest-sensitive consumption and investment spending and decrease aggregate demand.', '(ii) 実質産出量は<b>減る</b>と述べ、名目金利の上昇が金利に敏感な<b>消費と投資を減らし、総需要を減らす</b>と説明する', E, '3.A'),
        ('(iii) State that Zeetoland will experience net financial capital inflows and explain that higher interest rates in Zeetoland will attract financial capital from other countries.', '(iii) 金融資本は<b>純流入</b>になると述べ、金利の上昇が<b>他国から資本を引き寄せる</b>と説明する', E, '3.B')]),
      ('e', '外国為替市場', [
        ('Draw a correctly labeled graph of the foreign exchange market for the zeet.', '通貨ジートの外国為替市場のグラフを、正しいラベル付きで描く', G, '4.A'),
        ('For the second point, the graph must show a rightward shift in the demand curve for the zeet and an increase in the exchange rate (an appreciation in the currency).', '2点目には、ジートの<b>需要曲線の右への移動</b>と、<b>為替レートの上昇（通貨高）</b>を示す必要がある', G, '4.C')]),
      ('f', '輸出', [
        ('State that Zeetoland’s exports will decrease and explain that the appreciation of the zeet will make Zeetoland’s goods and services relatively more expensive than other countries’ goods and services.', '輸出は<b>減る</b>と述べ、ジート高によってゼートランドの財・サービスが他国に比べて<b>相対的に高くなる</b>と説明する', E, '3.A')])]),
  'q2': dict(kind='Short', pts=5, title='経済指標の計算（フェーラン国のデータ）',
     scene='2011年と2012年の名目GDP、税収、政府支出、消費支出、人口、GDPデフレーターの表が与えられる',
     parts=[
      ('a', '実質GDPとインフレ率', [
        ('(i) Calculate Fehran’s real GDP in 2012 as $180,000 and show your work. ($225,000/125) × 100 = $180,000', '(i) 2012年の実質GDPを<b>$180,000</b>と計算し、途中の計算を示す　($225,000/125) × 100 = $180,000', N, '1.C'),
        ('(ii) Calculate the inflation rate in Fehran from 2011 to 2012 as 25% and show your work. [(125-100)/100] × 100 = 25%', '(ii) 2011年から2012年のインフレ率を<b>25%</b>と計算し、途中の計算を示す　[(125-100)/100] × 100 = 25%', N, '1.C')]),
      ('b', '輸出への影響', [('State that foreign importers of electric vehicles will buy fewer electric vehicles from Fehran in 2012 and explain that electric vehicles in Fehran are relatively more expensive as a result of the increase in the price level.', '海外の輸入業者は2012年にフェーランの電気自動車を<b>少なく買う</b>と述べ、物価水準の上昇で電気自動車が<b>相対的に高くなった</b>と説明する', E, '2.C')]),
      ('c', '生活水準', [('State that the standard of living of the average person in Fehran stayed the same and explain that real GDP per capita did not change from 2011 to 2012 or that it stayed at $1,500.', '平均的な国民の生活水準は<b>変わらない</b>と述べ、<b>1人あたり実質GDP</b>が2011年から2012年で変わらない（$1,500のまま）と説明する', E, '2.C')]),
      ('d', '国の債務', [('State that Fehran’s national debt will increase and explain that government outlays are greater than taxes and a government adds to the national debt when it runs a budget deficit.', '国の債務は<b>増える</b>と述べ、政府支出が税収を上回り、<b>財政赤字</b>になると国の債務が増えると説明する', E, '3.C')])]),
 })
