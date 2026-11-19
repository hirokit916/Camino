# -*- coding: utf-8 -*-
"""AP Psychology (CED Effective Fall 2025, V.1). Rubric text verbatim. Row = (letter, ja, en, max, tips, levels, typical, notes)."""
OR = ('OR', 'または')

UNITS = [
 ('1', '行動の生物学的基盤', 'Biological Bases of Behavior', ['遺伝と環境の相互作用', '神経系の概要', 'ニューロンと神経の発火', '脳', '睡眠', '感覚']),
 ('2', '認知', 'Cognition', ['知覚', '思考・問題解決・判断・意思決定', '記憶とは', '記憶の符号化', '記憶の貯蔵', '記憶の検索', '忘却とその他の記憶の問題', '知能と学力']),
 ('3', '発達と学習', 'Development and Learning', ['発達心理学のテーマと方法', '生涯にわたる身体の発達', 'ジェンダーと性的指向', '生涯にわたる認知の発達', 'コミュニケーションと言語の発達', '生涯にわたる社会的・情緒的発達', '古典的条件づけ', 'オペラント条件づけ', '学習の社会的・認知的・神経的要因']),
 ('4', '社会心理学とパーソナリティ', 'Social Psychology and Personality', ['帰属理論と対人認知', '態度の形成と変化', '社会的状況の心理学', '精神力動論と人間性心理学のパーソナリティ理論', '社会的認知理論と特性論', '動機づけ', '感情']),
 ('5', '心と身体の健康', 'Mental and Physical Health', ['健康心理学とは', 'ポジティブ心理学', '心理的障害の説明と分類', '主な心理的障害', '心理的障害の治療']),
]
PRACTICES = [('概念の応用', 'Concept Application', '65%'), ('研究方法と研究デザイン', 'Research Methods and Design', '25%'), ('データの解釈', 'Data Interpretation', '10%')]

NO_EV = ('The response identifies no evidence.', '根拠を挙げていない')
NOT_CITED = ('The evidence is not correctly cited.', '出典を正しく示していない')
NONSPEC = ('The evidence is nonspecific.', '根拠が具体的でない')
NOT_REL = ('The response provides evidence not relevant to the claim.', '主張と関係のない根拠を挙げている')
CITE_STYLE = ('Responses that use a correct citation style other than the methods prescribed by the question can earn this point for citing the source.',
              '問題で指定された方法以外でも、正しい形式で出典を示していれば、この点を得られる')
ACCURATE = ('“Accurate evidence” refers to the accuracy of the general pattern of the evidence cited. Since citing specific numbers is not required to score the point, slight errors in reporting specific data can still earn the point when the direction of the difference or relationship of the data cited is correct.',
            '「正確な根拠」とは、引用した根拠の<b>大まかな傾向</b>が正確であること。具体的な数字の引用は必須ではないため、差や関係の<b>向きが正しければ</b>、数字に少し誤りがあっても点を得られる')
CITE_POS = ('The presence of a citation indicates the sentence or phrase is intended to be evidence. All text prior to the citation will be considered evidence. Text after a citation will be considered reasoning, unless accompanied by another citation.',
            '出典の表示は、その文や語句が根拠であることを示す。<b>出典より前の文は根拠、後の文は理由づけ</b>とみなされる（別の出典が続く場合を除く）')
BANNED = ('Concepts used in the sources that are not eligible to be used for the application point are “academic performance/achievement,” “sleep,” “mean,” “standard deviation,” “variable,” “statistically significant,” “sleep deprivation,” “convenience sample,” “survey,” “percentage,” “adolescents,” “quality of life,” “physical/mental health,” “sleep-wake cycle,” “anxiety disorders,” “mood disorders,” “stimulants,” “caffeine,” and “chronic sleepiness.”',
          '資料の中に出てくる用語（「学業成績」「睡眠」「平均」「標準偏差」「変数」「統計的に有意」「睡眠不足」「便宜的標本」「調査」「割合」「青年」「生活の質」「心身の健康」「睡眠・覚醒サイクル」「不安症」「気分障害」「興奮剤」「カフェイン」「慢性的な眠気」）は、<b>応用の点には使えない</b>')
EXP0 = [('The response does not accurately interpret the evidence.', '根拠を正確に解釈していない'),
        ('The response identifies evidence without explanation of how it relates to the claim.', '根拠を挙げているが、主張との関係を説明していない'),
        ('The response provides opinions with no reference to the sources provided.', '資料に触れず、意見を述べているだけ')]
LV1_EXP = ('Explains the relationship between the evidence and the claim', '根拠と主張の関係を説明している')
LV0_EXP = ('Does not explain the relationship between the evidence and the claim', '根拠と主張の関係を説明していない')

AAQ = [
 ('A', '研究方法', 'Research Method', 1, (1,),
  [(1, [('Accurately identifies the research method used in the study', '研究で使われた<b>研究方法を正確に特定</b>している')]),
   (0, [('Does not accurately identify the research method used in the study', '研究で使われた研究方法を正確に特定していない')])],
  [(1, [('The response accurately identifies the research method used in the study as an experiment.', '研究方法を<b>実験</b>と正確に特定している')]),
   (0, [('The response does not accurately identify the research method used in the study.', '研究方法を正確に特定していない'),
        ('The response includes no identification of the research method used in the study.', '研究方法をまったく特定していない')])], []),
 ('B', '研究の変数', 'Research Variable', 1, (2,),
  [(1, [('States a measurable or quantifiable definition of the identified variable as used in the study', '研究で使われた変数について、<b>測定・数量化できる定義</b>（操作的定義）を述べている')]),
   (0, [('Does not state a measurable or quantifiable definition of the identified variable used in the study', '変数について、測定・数量化できる定義を述べていない')])],
  [(1, [('The response states that the operational definition of executive functioning is whether the participant correctly identified the second set of objects shown as being the same or different more quickly.',
         '実行機能の操作的定義は、参加者が2組目の物体が同じか違うかを、より速く正しく見分けられたかどうかだと述べている'),
        ('The response states that the operational definition of executive functioning is the scores on the test.', '実行機能の操作的定義は、テストの得点だと述べている')]),
   (0, [('The response states a definition of the identified variable in the study that is not measurable or quantifiable.', '変数の定義を述べているが、測定・数量化できるものではない'),
        ('The response does not state a measurable or quantifiable definition of the identified variable as used in the study.', '研究で使われた変数について、測定・数量化できる定義を述べていない')])], []),
 ('C', '統計の解釈', 'Statistic Interpretation', 1, (3,),
  [(1, [('Accurately describes the identified statistic in relation to the study', '示された統計値を、<b>研究の内容と結びつけて</b>正確に説明している')]),
   (0, [('Does not accurately describe the identified statistic in relation to the study', '示された統計値を、研究と結びつけて正確に説明していない')])],
  [(1, [('The response accurately describes what the difference in means indicates for the immediate recall task for the multivitamin group as compared to the placebo group in relation to the study.',
         '即時再生課題での平均値の差が、マルチビタミン群とプラセボ群の比較として何を示すかを、研究に即して正確に説明している'),
        ('The response accurately describes that the means show that the multivitamin group recalled more than the placebo group.', '平均値から、マルチビタミン群の方がプラセボ群より<b>多く思い出せた</b>と正確に説明している')]),
   (0, [('The response restates the differences in the means for the immediate recall task between the multivitamin group and the placebo group without directly relating it to the study.', '平均値の差を<b>繰り返すだけ</b>で、研究と直接結びつけていない'),
        ('The response does not accurately describe what is indicated by the differences in the means for the immediate recall task between the multivitamin group and the placebo group in relation to the study.', '平均値の差が何を示すかを、研究に即して正確に説明していない'),
        ('The response provides a definition of the differences in the means for the immediate recall task between the multivitamin group and the placebo group but does not accurately describe its meaning in relation to the study.', '平均値の差の定義を述べているが、研究における意味を正確に説明していない')])], []),
 ('D', '倫理指針', 'Ethical Guidelines', 1, (4,),
  [(1, [('Accurately identifies one ethical guideline described in the study', '研究に書かれている<b>倫理指針を1つ</b>正確に特定している'), ('<i>AND</i>', '<i>かつ</i>'),
        ('Accurately describes one way the researchers in the study applied this ethical guideline', '研究者がその指針を<b>どのように適用したか</b>を1つ正確に説明している')]),
   (0, [('Does not accurately identify one ethical guideline described in the study', '研究に書かれている倫理指針を1つ正確に特定していない'), ('<i>AND/OR</i>', '<i>かつ／または</i>'),
        ('Does not correctly describe one way the researchers in the study applied this ethical guideline', '研究者がその指針をどのように適用したかを正しく説明していない')])],
  [(1, [('The response identifies confidentiality and describes that the researchers applied it in the study when researchers ensured that the individual participants could not be identified from the data collected.', '<b>守秘義務</b>を挙げ、収集したデータから個々の参加者が特定されないようにしたと説明している'), OR,
        ('The response identifies informed consent and describes that the researchers applied it in the study when participants agreed to be in the study and knew they could back out at any time.', '<b>インフォームド・コンセント</b>を挙げ、参加者が同意したうえで、いつでも辞退できると知っていたと説明している'), OR,
        ('The response identifies protection from harm and describes that the researchers considered/eliminated factors that might impose a burden/difficulty/stress for participants.', '<b>危害からの保護</b>を挙げ、参加者の負担・困難・ストレスになりうる要因を考慮した／取り除いたと説明している')]),
   (0, [('The response does not identify and/or describe the ethical guideline applied by researchers in the study.', '研究者が適用した倫理指針を特定していない、または説明していない'),
        ('The response identifies and describes an ethical guideline that researchers should have applied but was not described in the study.', '適用すべきだったが、<b>研究には書かれていない</b>倫理指針を挙げている'),
        ('The response identifies and describes an ethical guideline not identified in the question.', '問題で示されていない倫理指針を挙げている'),
        ('The response identifies and describes other features of the study that are not ethical guidelines.', '倫理指針ではない、研究のほかの特徴を挙げている')])], []),
 ('E', '一般化可能性', 'Generalizability', 1, (5,),
  [(1, [('Explains the extent to which the study is generalizable using specific and relevant evidence referencing participant variables from the study', '研究の<b>参加者に関する具体的な根拠</b>を使って、研究がどの程度<b>一般化できるか</b>を説明している')]),
   (0, [('Does not propose a claim regarding the generalizability of the study to a population (general or specific).', '研究を母集団（一般または特定）に一般化できるかについて、主張を述べていない'), OR,
        ('Does not use specific and relevant evidence that references participant variables which would impact the generalizability of the study.', '一般化に影響する参加者の変数について、具体的で関連する根拠を使っていない')])],
  [(1, [('The response proposes a claim about generalizability that references a population (the “larger population” or a population relevant to the study’s participants) to explain the extent of the generalizability of the study.', '<b>母集団</b>（「より大きな母集団」や参加者に関係する母集団）に触れて、一般化できる範囲を説明している'),
        ('The response proposes that the study is or is not generalizable to the population relevant to the study because of specific and relevant evidence derived from the participant information from the study.', '<b>参加者の情報</b>から得た具体的な根拠をもとに、研究が関係する母集団に一般化できる／できないと述べている')]),
   (0, [('The response proposes no claim regarding the generalizability of the conclusion of the study.', '研究の結論を一般化できるかについて、主張がない'),
        ('The response proposes a claim regarding the generalizability of the conclusion of the study but makes no reference to a population (general or specific).', '一般化について述べているが、<b>母集団に触れていない</b>'),
        ('The response uses evidence that does not apply to the generalizability of the conclusion of the study (e.g., reliability, validity, sample size).', '一般化に関係しない根拠（信頼性、妥当性、標本の大きさなど）を使っている')])],
  [('If the response asserts the study is “partly” generalizable or asserts the study is both generalizable and not generalizable, their evidence must support their assertion by showing ways the study is both generalizable and not generalizable to earn 1 point.',
    '「部分的に」一般化できる、または一般化できる面とできない面の両方があると述べる場合は、<b>両方の面</b>を根拠で示して、はじめて1点になる')]),
 ('F', '論証', 'Argumentation', 2, (6,),
  [(2, [('Uses a specific result from the study to explain how the results support or refute the psychological concept or hypothesis presented in the question. The results are accurately interpreted.',
         '研究の<b>具体的な結果</b>を使って、問題で示された心理学の概念や仮説を、結果がどのように<b>支持または反証するか</b>を説明している。結果の解釈が正確である')]),
   (1, [('Uses the results of the study but does not explain how the psychological concept or hypothesis is supported or refuted', '研究の結果を使っているが、概念や仮説がどのように支持・反証されるかを説明していない'), OR,
        ('Explains that the psychological concept or hypothesis is supported or refuted but does not use any results from the study', '概念や仮説が支持・反証されると説明しているが、研究の結果を使っていない')]),
   (0, [('Does not accurately explain how the results of the study support or refute the psychological concept or hypothesis presented in the question.', '研究の結果が、問題で示された概念や仮説をどのように支持・反証するかを正確に説明していない')])],
  [(2, [('The response uses at least one of the research findings to accurately explain how taking a multivitamin slows cognitive decline later in life. The results of the study are accurately interpreted.', '研究結果の少なくとも1つを使って、マルチビタミンの摂取が老年期の認知機能の低下を遅らせる仕組みを正確に説明している。結果の解釈が正確である')]),
   (1, [('The response proposes that the evidence alone is sufficient to demonstrate that taking a multivitamin slows cognitive decline in later life without additional explanation.', '追加の説明なしに、<b>根拠だけで</b>マルチビタミンが認知機能の低下を遅らせることを示せるとしている'),
        ('The response uses at least one of the research findings to explain how taking a multivitamin slows cognitive decline later in life. However, the interpretation of the results of the study includes some inaccuracies.', '研究結果を使って説明しているが、結果の解釈に<b>不正確な点</b>がある')]),
   (0, [('The response does not explain how at least one of the research findings support or refute that taking a multivitamin slows cognitive decline in later life.', '研究結果の少なくとも1つが、仮説の支持・反証にどうつながるかを説明していない'),
        ('The response does not accurately explain how at least one of the research findings support or refute that taking a multivitamin slows cognitive decline in later life.', '研究結果が仮説の支持・反証にどうつながるかを、正確に説明していない')])], []),
]

EBQ = [
 ('A', '主張', 'Claim', 1, (1,),
  [(1, [('Proposes a claim that is relevant to the question', '問いに関連する<b>主張</b>を述べている')]),
   (0, [('Does not propose a claim that is relevant to the question', '問いに関連する主張を述べていない')])],
  [(1, [('The response proposes a specific effect on the question.', '問いに対する<b>具体的な効果</b>を主張している'),
        ('The response proposes a claim that suggests a positive or negative effect on the question.', '問いに対して、良い効果または悪い効果を示す主張をしている'),
        ('The response proposes a recommendation for the application of the question.', '問いの内容をどう実行すべきか、<b>提案</b>をしている')]),
   (0, [('The response describes the question without making a claim.', '主張をせず、問いの内容を説明しているだけ'),
        ('The response proposes a claim unrelated to the question.', '問いと関係のない主張をしている'),
        ('The response proposes an oversimplified conclusion or evidence from a provided source.', '単純化しすぎた結論、または資料の根拠をそのまま主張にしている')])],
  [('A claim that meets the criteria can be awarded the point regardless of whether the responses in parts B and C successfully support the claim.', '基準を満たす主張であれば、パートBとCで主張を十分に支えられたかどうかに関係なく、この点を得られる')]),
 ('B (i)', '根拠①', 'Evidence', 1, (2,),
  [(1, [('Uses one piece of correctly cited, specific, accurate, and relevant evidence from one of the provided sources to support the claim', '与えられた資料の1つから、<b>正しく出典を示した</b>、具体的で正確な、関連する根拠を1つ使って主張を支えている')]),
   (0, [('Does not identify nor correctly cite one piece of specific evidence from one of the provided sources to support the claim. Any evidence provided is not relevant to the question.', '資料から具体的な根拠を1つ挙げていない、または正しく出典を示していない。示した根拠が問いと関係ない')])],
  [(1, [('The evidence is correctly cited and provides specific and accurate evidence relevant to the claim.', '根拠の出典が正しく示され、主張に関連する具体的で正確な根拠になっている')]),
   (0, [NO_EV, NOT_CITED, NONSPEC, NOT_REL])], [CITE_STYLE, ACCURATE]),
 ('B (ii)', '説明と応用①', 'Explanation and Application', 2, (3,),
  [(2, [('Applies a psychological perspective, theory, concept, or research finding to explain how the evidence supports the claim', '<b>心理学の視点・理論・概念・研究知見</b>を応用して、根拠がどのように主張を支えるかを説明している')]),
   (1, [LV1_EXP]), (0, [LV0_EXP])],
  [(2, [('The response correctly interprets the evidence and applies a psychological perspective, theory, concept, or research finding correctly.', '根拠を正しく解釈し、心理学の視点・理論・概念・研究知見を正しく応用している')]),
   (1, [('The response correctly interprets the evidence in supporting the claim, but does not apply a psychological perspective, theory, concept, or research finding.', '根拠が主張を支えることを正しく解釈しているが、心理学の視点・理論・概念・研究知見を<b>応用していない</b>')]),
   (0, EXP0)],
  [('The explanation and application points can be earned even if the response did not earn the point in B (i) due to incorrectly cited and/or non-specific evidence.', 'B (i)で出典の誤りや根拠のあいまいさにより点を得られなくても、説明と応用の点は得られる'),
   ('The use of a psychological perspective, theory, concept, or research finding explicitly identified in the <i>AP Psychology Course and Exam Description</i> (2024) is preferred but not required. The application of a psychological perspective, theory, concept, or research finding that is not explicitly included in the <i>AP Psychology Course and Exam Description</i> (2024) must demonstrate psychological knowledge and not popular understanding.',
    'Course and Exam Descriptionに明記された視点・理論・概念・研究知見を使うのが望ましいが、必須ではない。明記されていないものを使う場合は、<b>一般的な理解ではなく心理学の知識</b>であることを示す必要がある'),
   CITE_POS, BANNED]),
 ('C (i)', '根拠②', 'Evidence', 1, (2,),
  [(1, [('Uses a different piece of correctly cited, specific, and relevant evidence from either of the other two provided sources to support the claim', '残り2つの資料のどちらかから、<b>別の</b>正しく出典を示した具体的で関連する根拠を使って主張を支えている')]),
   (0, [('Does not identify nor correctly cite a different piece of specific evidence from either of the other two provided sources to support the claim', '残り2つの資料から別の具体的な根拠を挙げていない、または正しく出典を示していない')])],
  [(1, [('The response provides specific and correctly cited evidence relevant to the claim that is from a different source than the one used in part B.', 'パートBとは<b>別の資料</b>から、主張に関連する具体的で出典の正しい根拠を挙げている')]),
   (0, [NO_EV, NOT_CITED, NONSPEC, ('The evidence is from the same source as the one used in part B.', 'パートBと<b>同じ資料</b>の根拠を使っている'), NOT_REL])], [CITE_STYLE, ACCURATE]),
 ('C (ii)', '説明と応用②', 'Explanation and Application', 2, (3,),
  [(2, [('Applies a different psychological perspective, theory, concept, or research finding to explain how the evidence supports the claim. The psychological perspective, theory, concept, or research finding is different from the one used in part B (ii).',
         '<b>B (ii)とは別の</b>心理学の視点・理論・概念・研究知見を応用して、根拠がどのように主張を支えるかを説明している')]),
   (1, [LV1_EXP]), (0, [LV0_EXP])],
  [(2, [('The response correctly interprets the evidence and applies a psychological perspective, theory, concept, or research finding that is different from the one used in part B.', '根拠を正しく解釈し、パートBとは<b>別の</b>心理学の視点・理論・概念・研究知見を応用している')]),
   (1, [('The response correctly interprets the evidence, but does not apply a psychological perspective, theory, concept, or research finding.', '根拠を正しく解釈しているが、心理学の視点・理論・概念・研究知見を応用していない'),
        ('The response applies the same psychological perspective, theory, concept, or research finding that was used in part B; however, the response explains the relationship between the evidence and the claim that does not rely on the application.', 'パートBと<b>同じ</b>視点・理論などを使っているが、応用に頼らずに根拠と主張の関係を説明している')]),
   (0, EXP0)],
  [('The explanation and application points can be earned even if the response did not earn the point in C (i) due to incorrectly cited and/or non-specific evidence.', 'C (i)で出典の誤りや根拠のあいまいさにより点を得られなくても、説明と応用の点は得られる'),
   ('The explanation and application points can be earned if the response uses the same source in both Parts B and C, provided that the evidence used in part B and part C is different.', 'パートBとCで同じ資料を使っても、<b>根拠が異なれば</b>、説明と応用の点は得られる'),
   ('The use of a different psychological perspective, theory, concept, or research finding explicitly identified in the <i>AP Psychology Course and Exam Description</i> (2024) is preferred but not required. The application of a different psychological perspective, theory, concept, or research finding that is not explicitly included in the <i>AP Psychology Course and Exam Description</i> (2024) must demonstrate psychological knowledge and not popular understanding.',
    'Course and Exam Descriptionに明記された別の視点・理論・概念・研究知見を使うのが望ましいが、必須ではない。明記されていないものを使う場合は、一般的な理解ではなく心理学の知識であることを示す必要がある'),
   CITE_POS, BANNED]),
]

TIPS = {
 'q1': [('研究方法を、名前で正確に答える', '実験、相関研究、事例研究、調査など、研究方法の名前で答えます。独立変数を操作し、参加者を条件に分けていれば「実験」です。説明を足しても、名前が違えば点になりません'),
        ('操作的定義は「何を、どう測ったか」', '変数の意味ではなく、研究の中で<b>どう測定したか</b>を書きます。「記憶力」ではなく「テストで思い出せた単語の数」のように、数えられる形にします'),
        ('統計は、数字の「意味」まで説明する', '平均値を写すだけでは点になりません。「マルチビタミン群の方が多く思い出せた」のように、その数字が研究の比較について何を示すかを言葉で説明します'),
        ('倫理指針は「名前」と「この研究での使い方」をセットで', '守秘義務、インフォームド・コンセント、危害からの保護などの名前を挙げ、<b>この研究で</b>研究者が実際にどうしたかを書きます。研究に書かれていない指針や、すべきだったことを書いても点になりません'),
        ('一般化は、参加者の特徴を根拠にする', '「一般化できる」と言うだけでは点になりません。年齢、人数、性別、地域など<b>参加者の情報</b>を根拠に、どの母集団まで当てはまるかを説明します。信頼性や標本の大きさは、この点の根拠になりません'),
        ('結果を1つ引用し、仮説につなげる', '満点には、研究の<b>具体的な結果</b>を使い、それが仮説を支持するか反証するかを説明することが必要です。結果だけ、または説明だけでは1点にとどまります')],
 'q2': [('主張は具体的に、立場をはっきり', '「睡眠は大切」のような一般論ではなく、「中高生の始業は9時以降にすべき」のように、問いに対する<b>具体的な効果や提案</b>を一文で述べます'),
        ('根拠には必ず出典を付け、B と C で資料を変える', '根拠の文には「(Source 1)」のように出典を付けます。C (i)では<b>B (i)とは別の資料</b>から根拠を選びます。数字は多少ずれても、差や関係の向きが正しければ点になります'),
        ('心理学の概念で、根拠と主張をつなぐ', '2点を取るには、根拠がなぜ主張を支えるのかを、<b>授業で学んだ心理学の概念や理論</b>で説明します。資料に出てくる「睡眠」「平均」などの語は応用の点に使えず、C (ii)ではB (ii)と<b>別の概念</b>を使います')],
}

VERBS = [
 ('Describe', 'Provide the relevant characteristics of a specified topic.', '指定された内容の、関連する特徴を述べる'),
 ('Explain', 'Provide information about how or why a relationship, process, pattern, position, situation, or outcome occurs, using evidence and/or reasoning to support or qualify a claim. Explain “how” typically requires analyzing the relationship, process, pattern, position, situation, or outcome; Explain “why” typically requires analysis of motivations or reasons for the relationship, process, pattern, position, situation, or outcome.',
  '関係・過程・傾向・状況・結果が、どのように、なぜ起きるのかを、根拠や理由を使って説明する。「how」は関係や過程の分析、「why」は動機や理由の分析が求められることが多い'),
 ('Identify/State', 'Indicate or provide information about a specified topic, without elaboration or explanation.', '指定された内容について、説明を加えずに答える'),
 ('Propose', 'Provide a claim for a specific topic using your own words.', '自分の言葉で、具体的な主張を述べる'),
 ('Support or Refute', 'Provide reasoning that explains whether a claim or evidence should be upheld or rejected.', '主張や根拠を支持すべきか退けるべきかを、理由を示して説明する'),
 ('Use evidence', 'Provide information from a study (i.e., data, rationales, conclusions, hypotheses) that is specific and relevant to a given topic.', '研究から、テーマに関連する具体的な情報（データ、理由、結論、仮説）を示す'),
]
