---
tag: YVKN9D
kind: model
slug: dependency-model-with-valence
name: Dependency model with valence
aliases:
- DMV
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "Klein and Manning's generative model for unsupervised dependency induction, with stop and attach decisions on each side of a head, trained by EM."
history:
  year: 2004
  people: [Dan Klein, Christopher D. Manning]
  note: "Klein and Manning gave a head-outward generative model over part-of-speech tags whose stop decisions depend on whether a head already has a dependent, and trained it with EM from sentences without trees."
prereqs: [dependency-tree, expectation-maximization, inside-outside-algorithm]
see_also: [projective-dependency-tree, eisner-algorithm, attachment-score, lexicalized-pcfg, dependency-parsing, part-of-speech-tagging, head-rules, maximum-likelihood-estimation]
sources:
  - paper: doi:10.3115/1218955.1219016
    title: "Dan Klein and Christopher D. Manning, Corpus-Based Induction of Syntactic Structure, Models of Dependency and Constituency, ACL 2004"
    locator: "pp. 478-485; the DMV and its probability formula, the harmonic initializer, the WSJ10, NEGRA10 and CTB10 results, and the example of Figure 1"
  - paper: doi:10.3115/1034678.1034748
    title: "Jason Eisner and Giorgio Satta, Efficient Parsing for Bilexical Context-Free Grammars and Head Automaton Grammars, ACL 1999"
    locator: "pp. 457-464; the cubic-time parsing of grammars whose left and right dependents are generated independently"
---

The dependency model with valence (DMV) is a generative model of [dependency trees](/dependency-tree/) over part-of-speech tags, introduced by Dan Klein and Christopher Manning in 2004 for grammar induction: learning syntax from sentences that have no trees. Each head generates its dependents outward, first on one side and then on the other, and before each dependent it decides whether to stop. The stop decision depends on the head, the direction, and whether the head already has a dependent on that side. This last bit is the valence, and it lets the model learn, for example, that a verb usually takes one subject on its left. The parameters are trained by [expectation-maximization](/expectation-maximization/), with the [inside-outside algorithm](/inside-outside-algorithm/) as the E-step. On English sentences of at most 10 words, the DMV found 43.2% of the directed dependencies, well above the baselines, and many later models of unsupervised dependency parsing extend it.

## The machine

**Trees.** A sentence is a sequence of tags $x_1 \cdots x_n$. A tree is a [projective dependency tree](/projective-dependency-tree/) with an extra symbol ROOT. ROOT has exactly one dependent, the head of the sentence, and every word has exactly one head, which is ROOT for the head of the sentence.

**Parameters.** Two families of multinomials, with $\mathrm{dir} \in \{\text{left}, \text{right}\}$ and $\mathrm{adj} \in \{\text{true}, \text{false}\}$:

- $P_{\mathrm{STOP}}(\mathrm{STOP} \mid h, \mathrm{dir}, \mathrm{adj})$, the probability that head tag $h$ takes no more dependents in direction $\mathrm{dir}$, where $\mathrm{adj}$ is true if $h$ has no dependent in that direction yet;
- $P_{\mathrm{CHOOSE}}(a \mid h, \mathrm{dir})$, the probability that the next dependent of $h$ in direction $\mathrm{dir}$ has tag $a$.

ROOT chooses its single dependent with $P_{\mathrm{CHOOSE}}(a \mid \mathrm{ROOT})$. Klein and Manning use no smoothing.

**Generation.** A head generates its right dependents one by one, from the nearest outward, then STOP; then its left dependents in the same way, then STOP. Each dependent then generates its own subtree. The probability of the subtree $D(h)$ under a head $h$ is

$$P(D(h)) = \prod_{\mathrm{dir}} \Big[ \prod_{a \in \mathrm{deps}(h, \mathrm{dir})} P_{\mathrm{STOP}}(\neg \mathrm{STOP} \mid h, \mathrm{dir}, \mathrm{adj})\, P_{\mathrm{CHOOSE}}(a \mid h, \mathrm{dir})\, P(D(a)) \Big] \cdot P_{\mathrm{STOP}}(\mathrm{STOP} \mid h, \mathrm{dir}, \mathrm{adj}),$$

where in each factor $\mathrm{adj}$ is true exactly when no dependent of $h$ in direction $\mathrm{dir}$ has been generated before it. The probability of a sentence with its tree is $P_{\mathrm{CHOOSE}}(r \mid \mathrm{ROOT})\, P(D(r))$, where $r$ is the dependent of ROOT. The words themselves are not modeled, only their tags.

**Training.** The training data are tag sequences without trees. EM maximizes their likelihood $\prod_s \sum_t P(s, t)$ over the parameters. The E-step computes the expected number of each stop and choose decision with the inside-outside algorithm; the M-step sets each multinomial to its normalized expected counts.

**The harmonic initializer.** EM finds a local maximum, and the result depends on the start. Klein and Manning start with an M-step from an ad hoc posterior in which the chance that one word attaches to another is inversely proportional to a constant plus the distance between them. So short dependencies are favored at the start. This is a heuristic.

## What it counts

The model gives a joint probability $P(s, t)$ to a tag sequence and a tree, and a parser returns $\arg\max_t P(s, t)$. The quality of the induced trees is the fraction of words whose head matches the gold tree, the [attachment score](/attachment-score/), either directed or with the direction of each arc ignored.

**A worked tree.** The example of Klein and Manning is *Factory payrolls fell in September*, with the tags NN NNS VBD IN NN and the arcs ROOT to *fell*, *fell* to *payrolls*, *fell* to *in*, *in* to *September*, and *payrolls* to *Factory*. Its probability is the product of the factors

| head | factors |
|---|---|
| ROOT | $P_{\mathrm{CHOOSE}}(\mathrm{VBD} \mid \mathrm{ROOT})$ |
| *fell*, VBD | right: $P_{\mathrm{STOP}}(\neg\mathrm{STOP} \mid \mathrm{VBD}, \text{right}, \text{true})\, P_{\mathrm{CHOOSE}}(\mathrm{IN} \mid \mathrm{VBD}, \text{right})\, P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{VBD}, \text{right}, \text{false})$; left: $P_{\mathrm{STOP}}(\neg\mathrm{STOP} \mid \mathrm{VBD}, \text{left}, \text{true})\, P_{\mathrm{CHOOSE}}(\mathrm{NNS} \mid \mathrm{VBD}, \text{left})\, P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{VBD}, \text{left}, \text{false})$ |
| *payrolls*, NNS | right: $P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{NNS}, \text{right}, \text{true})$; left: $P_{\mathrm{STOP}}(\neg\mathrm{STOP} \mid \mathrm{NNS}, \text{left}, \text{true})\, P_{\mathrm{CHOOSE}}(\mathrm{NN} \mid \mathrm{NNS}, \text{left})\, P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{NNS}, \text{left}, \text{false})$ |
| *in*, IN | right: $P_{\mathrm{STOP}}(\neg\mathrm{STOP} \mid \mathrm{IN}, \text{right}, \text{true})\, P_{\mathrm{CHOOSE}}(\mathrm{NN} \mid \mathrm{IN}, \text{right})\, P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{IN}, \text{right}, \text{false})$; left: $P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{IN}, \text{left}, \text{true})$ |
| *Factory*, NN | $P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{NN}, \text{right}, \text{true})\, P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{NN}, \text{left}, \text{true})$ |
| *September*, NN | $P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{NN}, \text{right}, \text{true})\, P_{\mathrm{STOP}}(\mathrm{STOP} \mid \mathrm{NN}, \text{left}, \text{true})$ |

There are 19 factors: one for ROOT, two final STOP decisions for each of the 5 words, and two factors for each of the 4 arcs between words. In general a tree over $n$ words has $1 + 2n + 2(n - 1) = 4n - 1$ factors. The two nouns without dependents use the same two factors, which shows that the parameters are shared by tag, not by word.

**The valence matters.** Without the $\mathrm{adj}$ argument, the chance of stopping would be the same before the first dependent and before the second, so the number of dependents on each side would follow a geometric distribution. With it, the model can give a high chance of exactly one dependent, as for the subject of a verb.

## Relation to other models

- **Inside-outside algorithm.** The DMV is trained with the [inside-outside algorithm](/inside-outside-algorithm/), but it is not a general PCFG over phrase labels. It can be written as a PCFG whose nonterminals carry a head tag, a head position and a stage of the stop process. Run directly on that grammar, inside-outside takes time $O(n^5)$, like a [lexicalized PCFG](/lexicalized-pcfg/). Because the left and right dependents of a head are generated independently, the split-head construction behind the [Eisner algorithm](/eisner-algorithm/) applies and gives $O(n^3)$.
- **Expectation-maximization.** The DMV is a standard case of [EM](/expectation-maximization/) with hidden trees. EM does not decrease the likelihood, but the likelihood has many local maxima, so the induced trees depend on the initializer.
- **Lexicalized PCFG.** The head-outward generation with STOP decisions is the same as in the head-driven models of Collins. The DMV drops the phrase labels and the words, keeps only tags and arcs, and keeps one bit of history, the valence, in place of the distance measure.
- **Supervised dependency models.** With gold trees, the parameters are relative frequencies, the [maximum likelihood estimate](/maximum-likelihood-estimation/). Supervised [dependency parsing](/dependency-parsing/) usually uses discriminative models instead, which are much more accurate.

## Known results in the model

- **Projectivity (theorem).** Every tree with positive probability is projective, and ROOT has exactly one dependent. The model generates each subtree as a contiguous block of tags around its head.
- **Cubic inference (theorem).** Inside-outside, and Viterbi parsing, take time $O(n^3)$ for a fixed tag set with the split-head chart, and $O(n^5)$ with the plain lexicalized chart.
- **EM (theorem).** Each EM iteration does not decrease the likelihood of the training sentences.
- **WSJ10 accuracy (measurement).** WSJ10 is the set of Wall Street Journal sentences of at most 10 words after removing punctuation. The gold dependencies come from the treebank trees through the Collins [head rules](/head-rules/). Klein and Manning report directed and undirected accuracies of

  | model | directed | undirected |
  |---|---|---|
  | RANDOM | 30.1 | 45.6 |
  | ADJACENT | 33.6 | 56.7 |
  | DMV | 43.2 | 63.7 |

  ADJACENT links each word to its neighbor. When NP headship was changed so that determiners head noun phrases, the DMV reached 55.7 and 67.9 against the converted gold trees. This shows that part of the score depends on the head conventions of the gold trees, not on the model alone.
- **Other languages (measurement).** They report 55.8 undirected on the German NEGRA10 and 54.2 on the Chinese CTB10.
- **Initialization (heuristic).** These results use the harmonic initializer. EM from a different start point can reach a different local maximum and different trees.

## References
