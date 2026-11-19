# -*- coding: utf-8 -*-
"""Official English scoring guidelines (AP Japanese CED, effective fall 2026, PDF pp.123-129, 140-148),
verbatim, with Japanese translation. Highlights: K() = keyword linked to a TIP (English), <b> = highlight (Japanese)."""

def K(n, t):
    return '<a class="kt" href="#tip-%d" data-tip="%d" aria-expanded="false">%s<span class="kt-n">TIP %d</span></a>' % (n, n, t, n)

OR = ('OR', 'または')
BRIEF = ('Are so brief that no relevant information can be conveyed, or are in a language other than the target language.',
         '短すぎて関連する情報が伝わらない、または日本語以外の言語で答えている')
PLAG = ('Plagiarize all content or make evident that it was largely created through electronic translation methods or generative AI.',
        '内容をすべて盗用している、または大部分が<b>機械翻訳や生成AIで作られたことが明らか</b>である')
NR0 = ('Does not respond to the prompt, is completely irrelevant, or is a restatement of the prompt.',
       '課題に答えていない、まったく関係がない、または課題文をそのまま繰り返している')
IRR = ('Provide cultural information that is irrelevant to the task or obviously erroneous.', '課題と関係のない、または明らかに誤った文化の情報を伝えている')
LIST = ('List or describe—without explanation or depth—cultural products, practices, and/or perspectives.',
        '文化的な産物・慣習・ものの見方を、<b>説明や深さのないまま、並べたり描写したりしている</b>')
TIME = ('Students might not start speaking immediately and might finish before the allotted time runs out. Students who do not use the entire time to speak but still satisfy the scoring criteria are eligible to receive the maximum number of points in this category.',
        'すぐに話し始めなかったり、時間が終わる前に話し終えたりすることもある。<b>時間を使い切らなくても、採点基準を満たしていれば、この観点で満点を得られる</b>')

def org(x, xj, lack1, lack1j, inc2, inc2j, nat, tip_inc, notes_first_limited):
    """Organization row (Q1 Row C, Q3 Row B, Q4 Row B)."""
    lv = [(2, [('Demonstrates an organizational structure with a ' + K(3, 'logical progression of ideas and information') + ' that enhances the comprehensibility of the %s.' % x,
                '考えや情報が<b>論理的に展開する構成</b>で、%sを理解しやすくしている' % xj),
               ('Effectively uses a ' + K(3, 'variety of cohesive devices') + '.', '<b>さまざまなつなぎの表現</b>を効果的に使っている')]),
          (1, [('Demonstrates some connection of ideas, but progression of information might not always be logical or structured.',
                '考えにある程度のつながりはあるが、情報の展開が論理的・構造的でないことがある'),
               ('Includes some cohesive devices, but the use is limited or inappropriate for the context.',
                'つなぎの表現をいくつか使っているが、使い方が限られている、または文脈に合っていない')]),
          (0, [('Lacks organization or coherence, which significantly impedes comprehension.', '構成やまとまりがなく、理解を大きく妨げている')])]
    t0 = [BRIEF, ('Present information randomly, which renders the %s difficult to follow.' % x, '情報を脈絡なく並べていて、%sが追いにくい' % xj)]
    if x == 'presentation':
        t0.append(PLAG)
    typ = [(2, [('Are easy to follow throughout.', '最初から最後まで追いやすい'),
                ('Include ' + K(tip_inc, inc2) + '.', '<b>%s</b>' % inc2j),
                ('Use cohesive devices %sto enhance the flow of the %s.' % ('naturally ' if nat else '', x), 'つなぎの表現%sで、%sの流れをよくしている' % ('を自然に使い' if nat else '', xj))]),
           (1, [('Contain parts that are easy to follow and parts that are difficult to follow.', '追いやすい部分と、追いにくい部分がある'),
                ('Show some organizational structure but may lack %s.' % lack1, 'ある程度の構成はあるが、%s' % lack1j),
                ('Use a limited set of cohesive devices repeatedly or omit cohesive devices entirely.', '限られたつなぎの表現を繰り返し使っている、またはまったく使っていない')]),
           (0, t0)]
    cd = ('Cohesive devices are not limited to specific words or phrases but encompass a variety of strategies, such as the use of relative pronouns, pronoun references, conjunctions, transitions, and any other elements that promote %sorganization and connection of ideas.' % ('the ' if x == 'email' else 'verbal '),
          'つなぎの表現は特定の語句に限らず、関係代名詞、代名詞による指示、接続詞、転換の表現など、言葉の組み立てと考えのつながりを助けるあらゆる方法を含む')
    lim = ('A%s %s that demonstrates limited language control but remains comprehensible and demonstrates organization can earn points in this row.' % ('n' if x == 'email' else '', x),
           '言葉の運用が限られていても、理解でき、構成が見られる%sは、<b>この観点で点を得られる</b>' % xj)
    return lv, typ, ([lim, cd] if notes_first_limited else [cd, lim])

def lc_written(x, xj, prec1, prec1j, register=False):
    """Language Control for the written tasks (Q3 Row C, Q4 Row C)."""
    l3 = [('Uses a wide variety of vocabulary, including words or culturally relevant expressions appropriate to the topic of the %s.' % x,
           '%sの話題にふさわしい語や<b>文化に関わる表現</b>を含む、<b>非常に幅広い語彙</b>を使っている' % xj),
          ('Demonstrates control of a ' + K(9, 'variety of grammatical structures') + '.', '<b>多様な文法構造</b>を使いこなしている')]
    l2 = [('Uses a range of vocabulary, occasionally including words or culturally relevant expressions appropriate to the topic of the %s.' % x,
           'ある程度幅のある語彙を使い、ときどき%sの話題にふさわしい語や文化に関わる表現を含む' % xj),
          ('Demonstrates control of a range of basic grammatical structures.', '基本的な文法構造を幅広く使いこなしている')]
    l1 = [('Uses a limited set of vocabulary that precludes %s.' % prec1, '語彙が限られていて、%s' % prec1j),
          ('Demonstrates control of a limited set of basic grammatical structures.', '限られた基本的な文法構造しか使いこなせていない')]
    if register:
        l3.append(('Consistently uses ' + K(8, 'appropriate register') + '.', '<b>一貫して、相手と場面に合った言葉遣い（丁寧さ）</b>を使っている'))
        l2.append(('Occasionally uses inappropriate register and/or shifts between registers.', 'ときどき<b>合わない言葉遣いになる</b>、または<b>途中で言葉遣いが切り替わる</b>'))
        l1.append(('Uses inappropriate register throughout.', '全体を通して、合わない言葉遣いを使っている'))
    l3.append(('Does not contain ' + K(9, 'errors that impede comprehensibility') + '.', '<b>理解を妨げる誤り</b>がない'))
    l2.append(('Contains errors that occasionally impede comprehensibility.', 'ときどき理解を妨げる誤りがある'))
    l1.append(('Contains errors that impede comprehensibility.', '理解を妨げる誤りがある'))
    lv = [(3, l3), (2, l2), (1, l1),
          (0, [('Contains errors or limitations in grammar and vocabulary that significantly impede comprehension.', '文法や語彙の誤り・制約が、理解を大きく妨げている')])]
    typ = [(3, [('Use a variety of simple and compound sentences.', '<b>単文と重文（文と文をつないだ文）</b>を多様に使っている'),
                ('Use a variety of vocabulary, sometimes even idioms, to fully convey ideas.', '多様な語彙、ときには慣用句まで使って、考えを十分に伝えている'),
                ('Do not contain errors related to grammar, word choice, or written language conventions (e.g., punctuation, orthography) that prevent comprehension of the response.',
                 '理解を妨げるような、文法、語の選び方、<b>書き言葉の決まり（句読点、表記など）</b>の誤りがない')]),
           (2, [('Use simple sentences and a few compound sentences.', '単文と、少しの重文を使っている'),
                ('Use vocabulary that is sometimes imprecise or does not fully convey ideas.', '語彙がときどき不正確、または考えを伝えきれていない'),
                ('Contain errors related to grammar, word choice, or written language conventions (e.g., punctuation, orthography) that occasionally prevent comprehension of the response.',
                 '文法、語の選び方、書き言葉の決まり（句読点、表記など）の誤りが、ときどき理解を妨げる')]),
           (1, [('Use strings of simple or fragmented sentences and phrases.', '単純な文や、断片的な文・語句を並べている'),
                ('Use mostly high-frequency vocabulary.', '主に、よく使われる基本的な語彙を使っている'),
                ('Contain errors related to grammar, word choice, or written language conventions (e.g., punctuation, orthography) that frequently prevent comprehension of the response.',
                 '文法、語の選び方、書き言葉の決まり（句読点、表記など）の誤りが、たびたび理解を妨げる')]),
           (0, [('Are incomprehensible or near incomprehensible due to limitations in grammar and word choice.', '文法や語の選び方の制約のため、理解できない、またはほぼ理解できない'),
                ('Mostly contain content in a language other than the target language.', '内容の大部分が日本語以外の言語である')])]
    return lv, typ, []

def lc_spoken(qa):
    """Language Control for the speaking tasks (Q1 Row D, Q2 Row C)."""
    topic = 'the exchange' if qa else 'the topic of the presentation'
    topicj = 'やりとり' if qa else '発表の話題'
    lv = [(3, [('Uses a wide variety of vocabulary, including words or culturally relevant expressions appropriate to %s.' % topic,
                '%sにふさわしい語や<b>文化に関わる表現</b>を含む、<b>非常に幅広い語彙</b>を使っている' % topicj),
               ('Demonstrates control of a ' + K(9, 'variety of grammatical structures') + '.', '<b>多様な文法構造</b>を使いこなしている'),
               ('Does not contain ' + K(9, 'errors that impede comprehensibility') + '.', '<b>理解を妨げる誤り</b>がない')]),
          (2, [('Uses a range of vocabulary, occasionally including words or culturally relevant expressions appropriate to %s.' % topic,
                'ある程度幅のある語彙を使い、ときどき%sにふさわしい語や文化に関わる表現を含む' % topicj),
               ('Demonstrates control of a range of basic grammatical structures.', '基本的な文法構造を幅広く使いこなしている'),
               ('Contains errors that occasionally impede comprehensibility.', 'ときどき理解を妨げる誤りがある')]),
          (1, [(('Uses a limited set of vocabulary, which precludes maintenance of the exchange.', '語彙が限られていて、やりとりを続けられない') if qa else
                ('Uses a limited set of vocabulary that precludes coverage of the topic of the presentation.', '語彙が限られていて、発表の話題を扱いきれない')),
               ('Demonstrates control of a limited set of basic grammatical structures.', '限られた基本的な文法構造しか使いこなせていない'),
               ('Contains errors that impede comprehensibility.', '理解を妨げる誤りがある')]),
          (0, [('Contains errors or limitations in grammar and vocabulary that %s impede comprehension.' % ('greatly' if qa else 'significantly'), '文法や語彙の誤り・制約が、理解を大きく妨げている')])]
    t3 = [('Use a variety of simple and compound sentences.', '<b>単文と重文（文と文をつないだ文）</b>を多様に使っている'),
          ('Use a variety of vocabulary, sometimes even idioms, to fully convey ideas.', '多様な語彙、ときには慣用句まで使って、考えを十分に伝えている'),
          ('Improve comprehensibility when attempting to ' + K(10, 'clarify or correct information') + '.', '補足や言い直しをするときに、<b>よりわかりやすく伝え直せる</b>')]
    if qa:
        t3.append(('Use effective communicative strategies, such as ' + K(10, 'circumlocution and paraphrasing') + '.', '<b>遠回しな説明や言い換え</b>など、効果的なコミュニケーションの方法を使っている'))
    t0 = [('Are incomprehensible or %s due to significant limitations in grammar and word choice.' % ('very difficult to understand' if qa else 'near incomprehensible'),
           '文法や語の選び方の大きな制約のため、理解できない、または%s' % ('非常にわかりにくい' if qa else 'ほぼ理解できない')),
          ('Are limited to single words, utterances, or phrases that do not convey meaning.', '意味の伝わらない単語、発話、語句だけにとどまる'),
          ('Are in a language other than the target language.', '日本語以外の言語で答えている')]
    if not qa:
        t0.append(PLAG)
    typ = [(3, t3),
           (2, [('Use simple sentences and a few compound sentences.', '単文と、少しの重文を使っている'),
                ('Use adequate vocabulary but word choice might limit expression of ideas.', '語彙は足りているが、語の選び方が考えの表現を狭めることがある'),
                ('Sometimes improve comprehensibility when attempting to clarify or correct information.', '補足や言い直しをすると、ときどきわかりやすくなる')]),
           (1, [('Repeatedly use simple or memorized phrases and high-frequency vocabulary.', '単純な、または<b>暗記した言い回し</b>と基本的な語彙を繰り返し使う'),
                ('Rely on English when lacking vocabulary.', '語彙が足りないときに<b>英語に頼る</b>'),
                ('Do not improve comprehensibility when attempting to clarify or %s.' % ('self-correct' if qa else 'correct information'), '補足や言い直しをしても、わかりやすくならない')]),
           (0, t0)]
    return lv, typ, []

ROWS = {}

# ---- Q1 Project Presentation (11) ----
ROWS['q1'] = [
 ('A', '課題の遂行', 'Task Execution', 2, (1,),
  [(2, [('Addresses the prompt, providing an explanation of ' + K(1, 'three or more factors with relevant details') + '.', '課題に答え、<b>3つ以上の要因</b>を、<b>関連する詳細</b>とともに説明している')]),
   (1, [('Partially addresses the prompt by either:', '次のどちらかで、課題に部分的に答えている'),
        ('discussing three or more factors with minimal or no relevant details', '3つ以上の要因を挙げているが、関連する詳細がほとんど、またはまったくない'), OR,
        ('providing an explanation of one to two factors with relevant details', '1〜2つの要因だけを、関連する詳細とともに説明している')]),
   (0, [('Does not address the prompt, is completely irrelevant, or is a restatement of the prompt.', '課題に答えていない、まったく関係がない、または課題文をそのまま繰り返している')])],
  [(2, [('Include detailed explanations, including examples and/or specific information for at least three factors.', '少なくとも3つの要因について、<b>例や具体的な情報</b>を含む詳しい説明がある'),
        ('Contain relevant details that are drawn from ' + K(1, 'well-researched information') + ' within the context of the task.', '課題の状況に沿って、<b>よく調べた情報</b>から引いた関連する詳細がある')]),
   (1, [('Might list factors but only explain one or two of them with details.', '要因を並べても、詳細つきで説明しているのは1〜2つだけ'),
        ('Mainly rely on personal anecdotes or general knowledge.', '主に<b>個人的な体験談や一般的な知識</b>に頼っている')]),
   (0, [BRIEF, ('Do not include factors or only list factors without explanation.', '要因がない、または説明なしに要因を並べているだけ'), PLAG])], []),
 ('B', '文化の理解', 'Cultural Understanding', 2, (2,),
  [(2, [('Provides relevant and specific examples that demonstrate understanding of a ' + K(2, 'relationship between cultural perspectives AND cultural products and/or practices') + '.',
         '<b>文化的なものの見方と、文化的な産物や慣習との関係</b>を理解していることを示す、関連する具体的な例を挙げている')]),
   (1, [('Provides relevant examples that discuss cultural products, practices, and/or perspectives within the context of the task. Examples might lack specificity and/or fail to explain a relationship between cultural perspectives AND cultural products and/or practices.',
         '課題の状況に沿って、文化的な産物・慣習・ものの見方を論じる関連した例を挙げている。ただし、例が具体性に欠ける、または<b>ものの見方と産物・慣習との関係を説明できていない</b>ことがある')]),
   (0, [('Provides little to no relevant examples or description of the target culture’s products, practices, and/or perspectives within the context of the task.',
         '課題の状況に沿った、日本語圏の文化の産物・慣習・ものの見方についての関連する例や説明が、ほとんど、またはまったくない')])],
  [(2, [('Explain how specific cultural products or practices exemplify cultural values, beliefs, or attitudes.', '具体的な産物や慣習が、<b>文化の価値観・信念・態度をどのように表しているか</b>を説明している')]),
   (1, [LIST, ('Demonstrate understanding of cultural products or practices but not their relationship to cultural values, beliefs, or attitudes.',
               '産物や慣習は理解しているが、それが文化の価値観・信念・態度とどう関係するかは示していない')]),
   (0, [BRIEF, IRR, PLAG])], []),
 ('C', '構成', 'Organization', 2, (3,)) + org('presentation', '発表', 'an introduction and/or conclusion', '導入や結論がないことがある',
                                           'an introduction and conclusion', '導入と結論がある', True, 3, True),
 ('D', '語彙・文法', 'Language Control', 3, (9, 10)) + lc_spoken(False),
 ('E', '話し方', 'Delivery', 2, (4,),
  [(2, [('Uses a rate of speech and intonation patterns that are effective for engaging an audience.', '聞き手を引き込むのに効果的な<b>話す速さと抑揚</b>'),
        ('Uses speech that is ' + K(4, 'smooth and confident with little hesitation') + '.', 'ためらいが少なく、<b>なめらかで自信のある</b>話し方'),
        ('Uses clear pronunciation.', '発音が明瞭'),
        ('Does not contain errors that impede comprehensibility.', '理解を妨げる誤りがない')]),
   (1, [('Uses a rate of speech and intonation patterns that are somewhat effective for engaging an audience.', '話す速さと抑揚が、聞き手を引き込むのにある程度効果的'),
        ('Uses speech that is hesitant, monotone, or disconnected at times.', 'ときどき、ためらう、単調になる、または途切れる'),
        ('Uses generally clear pronunciation.', '発音がおおむね明瞭'),
        ('Contains errors that occasionally impede comprehensibility.', 'ときどき理解を妨げる誤りがある')]),
   (0, [('Contains errors in pronunciation and/or intonation that significantly impede intelligibility, and uses an inappropriate rate of speech.', '発音や抑揚の誤りが聞き取りやすさを大きく損ない、話す速さも適切でない')])],
  [(2, [('Do not require listener effort.', '聞き手に努力を求めない'),
        ('Use a rate of speech that is even and controlled throughout.', '全体を通して、話す速さが一定でコントロールされている'),
        ('Are generally well paced and contain minimal pauses, filler words (e.g., umm, uh), and/or utterances that do not interrupt fluency of speech.',
         'おおむね適切なペースで、間やつなぎ言葉（「えーと」など）は少なく、話の流れを妨げない'),
        ('Frequently use effective intonation to engage the audience and contribute to comprehension.', '効果的な抑揚をよく使い、聞き手を引き込み、理解を助けている')]),
   (1, [('Occasionally require effort from the listener due to speaker hesitancy, unclear pronunciation, or ineffective intonation.', 'ためらい、不明瞭な発音、効果的でない抑揚のため、ときどき聞き手に努力を求める'),
        ('Use a rate of speech that might be uneven at times.', '話す速さが、ときどき一定でない'),
        ('Use repetition, filler words (e.g., umm, uh), and/or false starts that at times interrupt fluidity of speech and obscure comprehensibility.', '繰り返し、つなぎ言葉、言い直しが、ときどき話の流れを止め、内容をわかりにくくする'),
        ('Are generally able to sustain speech to complete the task.', 'おおむね、課題を終えるまで話し続けられる')]),
   (0, [('Use monotone speech throughout the presentation and ' + K(4, 'sound as if being read or recited from memory') + '.', '発表全体が単調で、<b>読み上げや暗唱のように聞こえる</b>'),
        ('Require significant listener effort.', '聞き手に大きな努力を求める'),
        ('Use a rate of speech that is uneven throughout.', '全体を通して、話す速さが一定でない'),
        ('Use frequent repetition, filler words (e.g., umm, uh), and/or utterances that interrupt fluency of speech, obscuring comprehensibility.', '繰り返し、つなぎ言葉、流れを妨げる発話が多く、内容がわかりにくい'),
        ('Are generally unable to sustain speech to complete the task, or are in a language other than the target language.', '課題を終えるまで話し続けられない、または日本語以外の言語で話している'),
        PLAG])], [TIME]),
]

# ---- Q2 Project Q&A (9) ----
ROWS['q2'] = [
 ('A', '質問への対応', 'Task Execution', 2, (5,),
  [(2, [('Maintains the exchange with a series of responses that address the prompts; minor inconsistencies with the prompts may be present.', '一連の回答で質問に答え、<b>やりとりを続けている</b>。質問との<b>小さなずれはあってもよい</b>')]),
   (1, [('Maintains the exchange with a series of responses that partially address the prompts; some responses are incomplete or irrelevant.', '質問に部分的に答える回答でやりとりを続けている。不完全な、または関係のない回答もある')]),
   (0, [('Minimally addresses the prompts, is completely irrelevant, or is a restatement of the prompts.', '質問に最低限しか答えていない、まったく関係がない、または質問を繰り返している')])],
  [(2, [('Respond appropriately, providing the requested information for ' + K(5, 'at least three of the prompts') + ' within the exchange.', '<b>少なくとも3問</b>で、求められた情報を伝えて適切に答えている'),
        ('Might demonstrate minor misunderstandings of the prompts.', '質問を少し誤解していることがある')]),
   (1, [('Include an appropriate response to one or two of the questions in the exchange, but the other responses are incomplete, irrelevant, and/or demonstrate misunderstandings of the prompts.',
         '1〜2問には適切に答えているが、ほかの回答は不完全、無関係、または質問を誤解している'),
        ('Might have some responses that do not address the prompts.', '質問に答えていない回答がいくつかあることがある')]),
   (0, [BRIEF])], []),
 ('B', '文化の理解', 'Cultural Understanding', 2, (2, 6),
  [(2, [('<i>In at least one question response in the exchange, within the context of the task:</i>', '<i>少なくとも1問の回答で、課題の状況に沿って</i>'),
        ('Provides a ' + K(6, 'cultural comparison') + '.', '<b>文化の比較</b>をしている'), OR,
        ('Reflects on the ' + K(2, 'relationship between cultural perspectives AND cultural products and/or practices') + '.', '<b>ものの見方と、産物や慣習との関係</b>を振り返っている')]),
   (1, [('<i>In at least one question response in the exchange, within the context of the task:</i>', '<i>少なくとも1問の回答で、課題の状況に沿って</i>'),
        ('Describes the target culture’s products, practices, and/or perspectives.', '日本語圏の文化の産物・慣習・ものの見方を<b>描写している</b>')]),
   (0, [('<i>In all of the responses in the exchange:</i>', '<i>すべての回答で</i>'),
        ('Provides little or no description of the target culture’s products, practices, and/or perspectives.', '日本語圏の文化の産物・慣習・ものの見方を、ほとんど、またはまったく描写していない')])],
  [(2, [('Compare – Describe similarities or differences between the target culture’s products, practices, and/or perspectives and students’ own or those of another community, using details and examples.',
         '<b>比較</b>：日本語圏の文化の産物・慣習・ものの見方と、<b>自分の（または別の）社会のもの</b>との共通点や違いを、詳細と例を使って描写する'), OR,
        ('Reflect – Explain, using details and examples, the relationship between cultural perspectives and cultural products and/or practices.',
         '<b>振り返り</b>：ものの見方と、産物や慣習との関係を、詳細と例を使って説明する')]),
   (1, [LIST]),
   (0, [BRIEF, IRR])], []),
 ('C', '語彙・文法', 'Language Control', 3, (9, 10)) + lc_spoken(True),
 ('D', '流暢さ', 'Fluency', 2, (5,),
  [(2, [('Uses a rate of speech and intonation patterns that are effective for interpersonal communication; speech is ' + K(5, 'fluid and automatic') + '.',
         '話す速さと抑揚が、相手とのやりとりに効果的。話し方が<b>なめらかで、自然に言葉が出てくる</b>'),
        ('Uses clear pronunciation.', '発音が明瞭'),
        ('Does not contain errors that impede comprehensibility.', '理解を妨げる誤りがない')]),
   (1, [('Uses a rate of speech and intonation patterns that are somewhat effective for interpersonal communication; speech is disconnected at times.', '話す速さと抑揚が、やりとりにある程度効果的。ときどき途切れる'),
        ('Uses generally clear pronunciation.', '発音がおおむね明瞭'),
        ('Contains errors that occasionally impede comprehensibility.', 'ときどき理解を妨げる誤りがある')]),
   (0, [('Contains errors in pronunciation and/or intonation that significantly impede intelligibility. Lacks fluidity when responding.', '発音や抑揚の誤りが聞き取りやすさを大きく損なう。答えるときになめらかさがない')])],
  [(2, [('Do not require listener effort.', '聞き手に努力を求めない'),
        ('Use fluid speech throughout, although there may be some natural pauses, filler words (e.g., umm, uh), and/or false starts.', '全体を通してなめらかに話している。<b>自然な間、つなぎ言葉、言い直しは多少あってもよい</b>'),
        ('Frequently use effective intonation to engage the interlocutor and contribute to comprehension.', '効果的な抑揚をよく使い、相手を引き込み、理解を助けている')]),
   (1, [('Occasionally require effort from the listener due to speaker hesitancy, unclear pronunciation, or ineffective intonation.', 'ためらい、不明瞭な発音、効果的でない抑揚のため、ときどき聞き手に努力を求める'),
        ('Use repetition, filler words (e.g., umm, uh), and/or false starts that at times interrupt fluidity of speech and obscure comprehensibility.', '繰り返し、つなぎ言葉、言い直しが、ときどき話の流れを止め、内容をわかりにくくする'),
        ('Are generally able to sustain speech to complete the task.', 'おおむね、課題を終えるまで話し続けられる')]),
   (0, [('Require significant listener effort.', '聞き手に大きな努力を求める'),
        ('Use frequent repetition, filler words (e.g., umm, uh), and/or false starts that interrupt fluency of speech, obscuring comprehensibility.', '繰り返し、つなぎ言葉、言い直しが多く、内容がわかりにくい'),
        ('Are generally unable to sustain speech to complete the task, or are in a language other than the target language.', '課題を終えるまで話し続けられない、または日本語以外の言語で話している')])], [TIME]),
]

# ---- Q3 Story Narration (8) ----
ROWS['q3'] = [
 ('A', '物語の展開', 'Narrative Development', 3, (7,),
  [(3, [('Narrates a complete story consistent with the pictures.', '絵と一致する、<b>完結した物語</b>を語っている'),
        (K(7, 'Integrates all four pictures') + ' into the narrative.', '<b>4コマすべて</b>を物語に組み込んでいる'),
        ('Provides ' + K(7, 'relevant details and/or dialogue') + '.', '関連する<b>詳細や会話</b>を入れている')]),
   (2, [('Narrates a story that might be incomplete.', '物語が完結していないことがある'),
        ('Produces a story that is mostly consistent with the pictures.', '物語がおおむね絵と一致している'),
        ('Incorporates at least three pictures into the narrative.', '少なくとも3コマを物語に組み込んでいる'),
        ('Provides some details and/or dialogue.', '詳細や会話がいくらかある')]),
   (1, [('Narrates an incomplete story.', '完結していない物語'),
        ('Produces a story that might be inconsistent with the pictures.', '物語が絵と一致しないことがある'),
        ('Incorporates one to two pictures into the narrative.', '物語に組み込んでいるのは1〜2コマだけ'),
        ('Provides minimal to no details.', '詳細がほとんど、またはまったくない')]),
   (0, [NR0])],
  [(3, [('Present clearly developed characters and/or events consistent with the pictures while including relevant details.', '関連する詳細を入れながら、絵と一致する登場人物や出来事をはっきり描いている'),
        ('Tell a narrative that would be ' + K(7, 'clear even without the images') + '.', '<b>絵がなくてもわかる</b>物語になっている')]),
   (2, [('Tell a complete story consistent with the pictures but without details and/or dialogue.', '絵と一致する完結した物語だが、詳細や会話がない'), OR,
        ('Tell most of the story with the relevant details and/or dialogue, but the story is incomplete.', '関連する詳細や会話を入れて話の大部分を語っているが、物語が完結していない'),
        ('Create confusion due to the omission of details or descriptions.', '詳細や描写が抜けていて、読み手が混乱する')]),
   (1, [('Include only descriptions of the pictures or lists of words with little or no narration.', '物語としての語りがほとんどなく、<b>絵の描写や単語の羅列だけ</b>'),
        ('Consist of vague descriptions of characters and lack a clear description of events.', '登場人物の説明があいまいで、出来事がはっきり描かれていない')]),
   (0, [BRIEF])], []),
 ('B', '構成', 'Organization', 2, (3, 7)) + org('story', '物語', 'clear stages of the story (beginning, middle, and end)', '物語の段階（始まり・中盤・終わり）がはっきりしないことがある',
                                          'clear stages of the story (beginning, middle, and end)', '物語の段階（始まり・中盤・終わり）がはっきりしている', False, 3, False),
 ('C', '語彙・文法', 'Language Control', 3, (9,)) + lc_written('story', '物語', 'narration of the story', '物語を語れない'),
]

# ---- Q4 Email Response (8) ----
ROWS['q4'] = [
 ('A', 'メールの内容', 'Message Development', 3, (8,),
  [(3, [('Responds to the email, providing ' + K(8, 'both pieces of requested information') + ' within the context of the task.', '課題の状況に沿って、求められた<b>2つの情報の両方</b>を返信で伝えている'),
        ('Provides relevant details and/or examples.', '関連する<b>詳細や例</b>を入れている')]),
   (2, [('Responds to the email, providing at least one piece of requested information within the context of the task.', '課題の状況に沿って、求められた情報の少なくとも1つを返信で伝えている'),
        ('Provides some details and/or examples.', '詳細や例がいくらかある')]),
   (1, [('Responds to the email but does not provide either of the requested pieces of information.', '返信はしているが、求められた情報をどちらも伝えていない'),
        ('Provides minimal to no details and/or examples.', '詳細や例がほとんど、またはまったくない')]),
   (0, [NR0])],
  [(3, [('Clearly and directly respond to both requests in the email, providing relevant details and/or examples.', 'メールの<b>2つの依頼の両方</b>に、関連する詳細や例をつけて、<b>はっきり直接</b>答えている')]),
   (2, [('Directly or indirectly respond to at least one of the requests in the email.', 'メールの依頼の少なくとも1つに、直接または間接的に答えている'),
        ('Respond to all requests from the email but include no details and/or examples.', 'すべての依頼に答えているが、詳細や例がない'),
        ('Respond to only one of the requests with some details and/or examples.', '1つの依頼にだけ、いくらかの詳細や例をつけて答えている')]),
   (1, [('Minimally respond to the requests in the prompt.', '依頼に最低限しか答えていない'),
        ('Respond to the email but do not address the requests.', '返信はしているが、依頼には触れていない'),
        ('Include mostly irrelevant information.', '大部分が関係のない情報')]),
   (0, [BRIEF])], []),
 ('B', '構成', 'Organization', 2, (8,)) + org('email', 'メール', 'a greeting and closing', 'あいさつや結びがないことがある',
                                        'a greeting and closing', 'あいさつと結びがある', False, 8, False),
 ('C', '語彙・文法', 'Language Control', 3, (8, 9)) + lc_written('email', 'メール', 'coverage of the topic of the email', 'メールの話題を扱いきれない', register=True),
]

# Task directions printed with Q3/Q4 ("In your response, you should:")
DIRECTIONS = {
 'q3': [('Narrate a complete story consistent with all four pictures, including relevant details.', '4コマすべてと一致する完結した物語を、関連する詳細を入れて語る'),
        ('Organize your story logically and use words and phrases that enhance the flow of the story.', '物語を論理的に組み立て、流れをよくする語句を使う'),
        ('Use a variety of vocabulary and grammatical structures as well as culturally relevant expressions.', '多様な語彙と文法構造、文化に関わる表現を使う')],
 'q4': [('Respond to both requests for information, providing details and examples.', '2つの依頼の両方に、詳細と例を挙げて答える'),
        ('Organize your email logically and use words and phrases that enhance the flow of the email.', 'メールを論理的に組み立て、流れをよくする語句を使う'),
        ('Use culturally relevant expressions and a variety of vocabulary and grammatical structures while maintaining an appropriate register.', '文化に関わる表現と多様な語彙・文法構造を使い、ふさわしい言葉遣いを保つ')],
}

DEFS = [
 ('Cultural products', '文化的な産物', 'are tangible and intangible artifacts of a culture, such as clothing, tools, food, monuments, artwork, and stories.',
  '形のあるもの・ないものを含む文化の産物。服、道具、食べ物、記念碑、芸術作品、物語など'),
 ('Cultural practices', '文化的な慣習', 'are patterns of social behaviors and interactions of a culture, such as how people greet each other, socialize, or celebrate holidays.',
  '社会の中での行動や人との関わり方の型。あいさつの仕方、人との付き合い方、祝日の祝い方など'),
 ('Cultural perspectives', '文化的なものの見方', 'are underlying cultural values, beliefs, and attitudes that inform a culture’s products and practices.',
  '産物や慣習のもとにある、文化の価値観・信念・態度'),
]

# ---------------- rendering ----------------
def items(lst):
    out = []
    for en, ja in lst:
        if en == 'OR':
            out.append('<li class="apx-or"><span lang="en">OR</span>または</li>')
        elif en.startswith('<i>'):
            out.append('<li class="apx-in"><p class="apx-en" lang="en">%s</p><p class="apx-ja">%s</p></li>' % (en, ja))
        else:
            out.append('<li><p class="apx-en" lang="en">%s</p><p class="apx-ja">%s</p></li>' % (en, ja))
    return '<ul class="apx-l">%s</ul>' % ''.join(out)

def levels(lv, maxp, typ=False):
    rows = []
    for sc, lst in lv:
        lab = ('Typical responses that %s' % ('do not earn points' if sc == 0 else 'earn %d point%s' % (sc, '' if sc == 1 else 's'))) if typ else ('%d point%s' % (sc, '' if sc == 1 else 's'))
        rows.append('<div class="apx-lv%s"><div class="apx-s"><b>%d<small>点</small></b><span lang="en">%s</span></div>%s</div>'
                    % (' apx-top' if sc == maxp else '', sc, lab, items(lst)))
    return ''.join(rows)

def row_html(r):
    letter, ja, en, maxp, tips, lv, typ, notes = r
    t = ''.join('<a class="apc-tip" href="#tip-%d">TIP %d</a>' % (i, i) for i in tips)
    nt = '<div class="apx-note"><p class="apx-nh">注<small lang="en">Additional Notes</small></p>%s</div>' % items(notes) if notes else ''
    top = ('<div class="apx-top2"><p class="apx-cap">満点（%d点）の基準<small lang="en">Scoring Criteria</small></p>%s'
           '<p class="apx-cap">満点になる典型的な回答<small lang="en">Typical responses that earn %d points</small></p>%s</div>'
           % (maxp, items(lv[0][1]), maxp, items(typ[0][1])))
    tmap = dict(typ)
    low = ''.join('<div class="apx-lv"><div class="apx-s"><b>%d<small>点</small></b></div><div><p class="apx-sub">基準</p>%s<p class="apx-sub">典型的な回答</p>%s</div></div>'
                  % (sc, items(lst), items(tmap.get(sc, []))) for sc, lst in lv[1:])
    return ('<div class="apc"><div class="apc-h"><span class="apc-p">%d<small>点</small></span><b>%s</b><small lang="en">Row %s　%s (0–%d points)</small>%s</div>'
            '%s%s<details class="apx-dr"><summary>%d点未満の基準と典型的な回答を見る</summary><div class="apx apx-lowg">%s</div></details></div>'
            % (maxp, ja, letter, en, maxp, '<span class="apc-ts">%s</span>' % t if t else '', top, nt, maxp, low))

def directions_html(q):
    if q not in DIRECTIONS:
        return ''
    return ('<div class="apx-dir"><p class="apx-nh"><span lang="en">In your response, you should:</span><small>問題文の指示</small></p>%s</div>' % items(DIRECTIONS[q]))

def defs_html():
    return ('<dl class="apdef rise">%s<div><dt>つなぎの表現<small lang="en">Cohesive devices</small></dt><dd><p class="apx-en" lang="en">Cohesive devices are not limited to specific words or phrases but encompass a variety of strategies, such as the use of relative pronouns, pronoun references, conjunctions, transitions, and any other elements that promote verbal organization and connection of ideas.</p>'
            '<p class="apx-ja">特定の語句に限らず、関係代名詞、代名詞による指示、接続詞、転換の表現など、言葉の組み立てと考えのつながりを助けるあらゆる方法</p></dd></div></dl>'
            % ''.join('<div><dt>%s<small lang="en">%s</small></dt><dd><p class="apx-en" lang="en"><b>%s</b> %s</p><p class="apx-ja">%s</p></dd></div>' % (j, e, e, de, dj) for e, j, de, dj in DEFS))

SRC = ('出典：College Board「AP Japanese Language and Culture Course and Exam Description」（Effective Fall 2026）の%s。'
       '© 2026 College Board. 英語は原文のまま。和訳とハイライトは当サイトによるもの')
