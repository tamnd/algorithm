---
tag: 4DDQYQ
kind: problem
slug: machine-translation
name: Machine translation
aliases:
- automatic translation
area: natural-language-and-speech/machine-translation-and-alignment
level: intro
summary: Translate a text in a source language into a fluent text in a target language with the same meaning.
prereqs: [language-model]
see_also: [noisy-channel-translation-model, phrase-based-translation-model, hierarchical-phrase-based-translation, encoder-decoder-model, word-alignment, parallel-corpus, bleu, phrase-based-stack-decoding]
sources:
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapters 4 to 11 (word-based, phrase-based and tree-based models, decoding, evaluation and tuning)"
  - book: isbn:9781108497329
    title: Philipp Koehn, Neural Machine Translation, Cambridge University Press, 2020
    locator: the neural encoder-decoder models, attention and the Transformer for translation
  - paper: doi:10.1145/1380584.1380586
    title: Adam Lopez, Statistical machine translation, ACM Computing Surveys 40(3), 2008, Article 8
    locator: the survey of translational equivalence models, parameter estimation, decoding and evaluation
  - paper: "Kevin Knight, Decoding complexity in word-replacement translation models, Computational Linguistics 25(4), 1999, pages 607 to 615, ACL Anthology J99-4005"
    title: Knight 1999
    locator: "Section 4 (M1-DECIDE is NP-complete), Section 4.1 (reduction from the Hamilton circuit problem) and Section 4.2 (reduction from minimum set cover)"
---

Machine translation is the problem of turning a text in one natural language, the source, into a text in another language, the target, that has the same meaning and reads as fluent text. It has no single correct answer: a sentence has many good translations, so systems are judged by people or by metrics such as [BLEU](/bleu/) against reference translations. Data-driven systems learn translation from a [parallel corpus](/parallel-corpus/) of sentence pairs; the statistical systems of about 1990 to 2015 split the problem into models of word and phrase correspondence, a [language model](/language-model/) and a search, and neural systems since about 2015 learn one network for the whole mapping. Search is the hard part in theory: finding the best translation under a model with free word reordering is NP-complete.

## In plain words

A translation must say the same thing as the original and sound natural in the new language. These two goals pull apart: a word-by-word version keeps the meaning of each word but often has the wrong word order and wrong grammar, while a smooth sentence may leave something out.

A computer learns to translate from many examples of sentences and their translations. Older systems learned which words and short phrases go together, learned separately what good sentences of the target language look like, and then searched for the output that did best on both. Newer systems learn a single neural network that reads the source sentence and writes the translation word by word. Either way, the system has to choose among a huge number of possible outputs, so it searches only the most promising ones.

## Definition

Write the source sentence as $f = f_1 \ldots f_m$ and the target sentence as $e = e_1 \ldots e_l$; translation runs from $f$ to $e$. The statistical form of the problem is: given a model that assigns a score $\mathrm{score}(e, f)$ to every target string $e$ for the source $f$, find

$$\hat e = \arg\max_e \mathrm{score}(e, f).$$

The [noisy channel model](/noisy-channel-translation-model/) uses $\mathrm{score} = \ln p(e) + \ln p(f \mid e)$, the [log-linear model](/log-linear-translation-model/) a weighted sum of features, and a neural model $\ln p(e \mid f)$ directly. Logs are natural. Most models also have a hidden structure, such as a [word alignment](/word-alignment/) or a segmentation into phrases, and the search usually maximizes over it too.

The quality of $\hat e$ is not part of this definition. It is measured afterwards, by human judgement or by a metric that compares $\hat e$ with one or more reference translations. So the problem has two parts with different natures: a *modelling* problem (find a score that prefers good translations), which is measured, and a *search* problem (find the best output under a given score), which can be stated exactly.

The search problem is a decision problem in its usual complexity form: given $f$, a model and a number $K$, is there a translation $e$ (with an alignment) whose score is at least $K$?

## Variants

- **Text and speech.** Speech translation takes audio as input, either through a speech recognizer or end to end.
- **Sentence and document.** Most systems translate one sentence at a time. Document-level translation also uses the context of other sentences, for pronouns and consistent terms.
- **Pairs and many languages.** One system per language pair, or one [multilingual model](/multilingual-neural-translation/) for many pairs, which helps pairs with little data.
- **Supervised and unsupervised.** With a parallel corpus, or with monolingual text only, for example with [back-translation](/back-translation/).
- **Simultaneous translation.** The output must start before the source sentence ends.

## Examples

**One sentence, several answers.** The German "morgen fliege ich nach Kanada" can be "tomorrow I will fly to Canada", "I will fly to Canada tomorrow" or "I am flying to Canada tomorrow". All three are good, and they differ in word order and tense. A word-by-word output "tomorrow fly I to Canada" has the right words in the wrong order.

**Reordering.** In German the verb of a subordinate clause goes to the end: "weil ich nach hause gehe" is "because I go home", so the last German word becomes the third English word. In Japanese the verb is at the end of every clause. Such pairs need models that reorder phrases across long distances.

**A small search problem.** On the [stack decoding](/phrase-based-stack-decoding/) page, the three-word sentence "morgen fliege ich" has 14 derivations under a small phrase table, and the decoder must compare them all, or prune.

## Known algorithms

The main families, in historical order:

| approach | model | search | page |
|---|---|---|---|
| word-based | IBM Models 1 to 5, HMM | stack or beam search | [IBM Model 1](/ibm-model-1/), [noisy channel](/noisy-channel-translation-model/) |
| phrase-based | phrase table, reordering, n-gram LM, log-linear | multi-stack beam search | [phrase-based model](/phrase-based-translation-model/), [stack decoding](/phrase-based-stack-decoding/) |
| hierarchical | synchronous CFG with one nonterminal | chart parsing with cube pruning | [Hiero](/hierarchical-phrase-based-translation/), [cube pruning](/cube-pruning/) |
| syntax-based | rules with target or source trees | chart parsing | [GHKM rules](/ghkm-rule-extraction/), [SCFG](/synchronous-context-free-grammar/) |
| neural | encoder-decoder with attention, Transformer | beam search | [encoder-decoder model](/encoder-decoder-model/), [Transformer](/transformer/) |

The statistical systems are trained in steps: [word alignment](/word-alignment/), [phrase pair extraction](/phrase-pair-extraction/) or rule extraction, the estimation of features, and the tuning of the feature weights with [minimum error rate training](/minimum-error-rate-training/). The neural systems are trained end to end by maximum likelihood, sometimes followed by [minimum risk training](/minimum-risk-training/).

## Bounds

- **Search is NP-complete (theorem).** For a word-based model in which the source words can be reordered freely (IBM Model 1) with a bigram language model, the decision version of decoding is [NP-complete](/np-complete/) (Knight 1999), so the optimization version is [NP-hard](/np-hard/). Phrase-based decoding with free reordering contains this case. So no polynomial algorithm decodes these models exactly unless P = NP, and decoders use [beam search](/beam-search/) and distortion limits.
- **Monotone search is polynomial.** Without reordering, or with reordering limited to a window of fixed size, a phrase-based model with an n-gram language model can be decoded exactly by dynamic programming in time polynomial in $m$, though exponential in the window size.
- **Synchronous grammars are polynomial in the sentence.** For a binary synchronous grammar, parsing the source side costs $O(m^3)$ times grammar factors, and adding an n-gram language model multiplies the cost by a polynomial in the vocabulary size; see [ITG](/inversion-transduction-grammar/) and [cube pruning](/cube-pruning/).
- **Quality has no bound.** There is no theorem on how good a translation can be; quality is a measurement.

## Reductions

- **From tours of a graph.** Knight (1999) reduced the [Hamiltonian cycle](/hamiltonian-cycle/) problem, a special case of the [traveling salesman problem](/traveling-salesman-problem/), to decoding: each vertex becomes a source word with one translation, the bigram scores of the language model encode the edges, and a good translation must order the words along a tour. This gives the NP-hardness of decoding. Choosing a translation word for each source word adds a second hard part, which Knight reduced from [set cover](/set-cover/).
- **To shortest paths.** Monotone decoding with a bigram language model is a shortest path problem in a [DAG](/dag-shortest-paths/) whose nodes are (position, last word).
- **To parsing.** Decoding with a synchronous grammar is parsing the source with the source side of the grammar and reading off the target side, a [CKY-style](/probabilistic-cky/) chart over spans.

## Applications

Machine translation is used to read foreign text on the web and in messages, to give translators a first draft that they correct (post-editing), to translate user interfaces and documentation, and to translate speech in real time. It is also a tool in other tasks: cross-lingual search, data augmentation by back-translation, and the alignment of multilingual corpora. Research on translation produced methods used much more widely, among them the [attention](/additive-attention/) mechanism and the Transformer.

## References
