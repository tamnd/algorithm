---
tag: 9ECTG0
kind: problem
slug: word-alignment
name: Word alignment
aliases:
- bilingual word alignment
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Find which words of a sentence correspond to which words of its translation, as a set of links between positions.
prereqs: [parallel-corpus]
see_also: [ibm-model-1, hmm-alignment-model, fast-align, grow-diag-final-symmetrization, alignment-error-rate, sentence-alignment, phrase-pair-extraction, bipartite-matching]
sources:
  - paper: "Peter F. Brown, Stephen A. Della Pietra, Vincent J. Della Pietra and Robert L. Mercer, The mathematics of statistical machine translation: parameter estimation, Computational Linguistics 19(2), 1993, pages 263 to 311"
    title: Brown, Della Pietra, Della Pietra and Mercer 1993
    locator: the definition of an alignment as a set of connections between word positions, with the empty cept, and Models 1 to 5 with their Viterbi alignments
  - paper: "Franz Josef Och and Hermann Ney, A systematic comparison of various statistical alignment models, Computational Linguistics 29(1), 2003, pages 19 to 51"
    title: Och and Ney 2003
    locator: the statistical alignment models, the symmetrization of the two directions, and the evaluation with sure and possible links
  - paper: "Raghavendra Udupa and Hemanta K. Maji, Computational complexity of statistical machine translation, EACL 2006, pages 25 to 32, ACL Anthology E06-1004"
    title: Udupa and Maji 2006
    locator: the hardness of the Viterbi alignment for IBM Models 3 to 5
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 4 (word-based models), Section 4.5 (word alignment)"
---

Word alignment is the problem of finding, for a sentence and its translation, which words of one correspond to which words of the other. The answer is a set of links between word positions. A word can have no link, one link or many links, and the links can cross, because languages order words differently. Word alignments are seldom annotated, so they are usually learned without supervision from a [parallel corpus](/parallel-corpus/) of sentence pairs, with a probabilistic model such as [IBM Model 1](/ibm-model-1/) or the [HMM alignment model](/hmm-alignment-model/) trained by [expectation-maximization](/expectation-maximization/). The links are then used to extract [phrase pairs](/phrase-pair-extraction/) and translation lexicons. How hard it is to find the best alignment depends on the model: it is easy under Models 1 and 2 and the HMM, and NP-hard under IBM Model 3.

## In plain words

Take an English sentence and its French translation. Draw a line from each French word to the English word that means the same. Some lines are simple: "maison" goes to "house". Some French words need two English words, some English words have no partner, and the lines cross when the two languages put words in a different order. Word alignment is the task of drawing these lines by computer. Usually no one gives the computer any correct lines. It sees only many pairs of sentences, and it learns that words which often appear in the same pairs are likely to be translations. Then it picks the most probable lines for each pair.

## Definition

**Input.** A source sentence $f = f_1 \ldots f_m$ and a target sentence $e = e_1 \ldots e_l$ that translate each other, and, for the unsupervised problem, a corpus of such pairs with no links.

**Output.** A set of links $A \subseteq \{1, \ldots, m\} \times \{1, \ldots, l\}$, where $(j, i) \in A$ means that $f_j$ and $e_i$ are translations of each other, fully or in part.

**Directional form.** Most models restrict the output to a function $a : \{1, \ldots, m\} \to \{0, 1, \ldots, l\}$. Each source word has exactly one link, to a target word or to the null word $e_0$, which stands for "no target word" (Brown et al. 1993). A target word can still have many links. The links of the function are $\{(j, a_j) : a_j \ge 1\}$.

**Model form.** Given a model $p(f, a \mid e)$, the best (Viterbi) alignment of a pair is

$$\hat a = \arg\max_a p(a \mid f, e) = \arg\max_a p(f, a \mid e).$$

The quality of an output is measured against links that people made, for example by the [alignment error rate](/alignment-error-rate/).

## Variants

- **Direction.** The function form with $f$ as source is one direction, and the function with $e$ as source is the other. Each direction can express one-to-many links only on its own side. [Symmetrization](/grow-diag-final-symmetrization/) combines the two into one set of links.
- **One-to-one.** Each word has at most one link. With a score for each word pair, this is a maximum weight [bipartite matching](/bipartite-matching/).
- **Posterior links.** Instead of the Viterbi alignment, output every link whose posterior probability $p(a_j = i \mid f, e)$ is above a threshold. The [forward-backward](/forward-backward-algorithm/) algorithm gives these posteriors under the HMM model.
- **Supervised alignment.** A small set of pairs with gold links is used to train or tune a discriminative aligner.
- **Soft alignment.** A neural translation model with [attention](/additive-attention/) computes a weight for each pair of positions instead of discrete links.

## Examples

- **Monotone.** For "das Haus ist klein" and "the house is small", each word links to the word at the same position: $A = \{(1,1), (2,2), (3,3), (4,4)\}$.
- **Reordering.** For "klein ist das Haus" (source) and "the house is small" (target), $A = \{(1,4), (2,3), (3,1), (4,2)\}$. The links cross.
- **One-to-many and unaligned words.** For the source "je ne vais pas" and the target "I do not go", the directional alignment is $a = (1, 3, 4, 3)$: "je" to "I", "ne" and "pas" both to "not", and "vais" to "go". The word "do" has no link. In the other direction, with "I do not go" as source, "not" can link to only one of "ne" and "pas", so neither direction alone gives the alignment that a person would draw.
- **Counting.** A pair with $m = 4$ and $l = 4$ has $5^4 = 625$ directional alignments with the null word and $2^{16} = 65536$ link sets.

## Known algorithms

The cost is per sentence pair, with lengths $m$ and $l$, once the model parameters are known. Training repeats an E step that sums over alignments.

| Model or method | Best alignment | Cost | Note |
|---|---|---|---|
| [IBM Model 1](/ibm-model-1/) | exact, each word on its own | $\Theta(l m)$ | $a_j = \arg\max_i t(f_j \mid e_i)$ |
| [IBM Model 2](/ibm-model-2/), [fast_align](/fast-align/) | exact, each word on its own | $\Theta(l m)$ | the score has a position factor |
| [HMM alignment model](/hmm-alignment-model/) | exact, by the [Viterbi algorithm](/viterbi-algorithm/) | $\Theta(m l^2)$ | links depend on the previous link |
| [IBM Model 3](/ibm-model-3/) | approximate, by [hill climbing](/hill-climbing/) | polynomial per step | exact is NP-hard |
| [grow-diag-final](/grow-diag-final-symmetrization/) | combines two directions | $O(l m)$ per pass | a heuristic |
| one-to-one with scores | exact, by the [Hungarian algorithm](/hungarian-algorithm/) | $O(n^3)$ with $n = \max(l, m)$ | a matching |

Under Models 1 and 2, $p(f, a \mid e)$ is a product of one factor for each source word, and each factor depends only on $a_j$. So the maximum over $a$ is the product of the maxima over each $a_j$. Under the HMM model the factor of $a_j$ also depends on $a_{j-1}$, and dynamic programming over $j$ gives the exact answer.

## Bounds

- **Upper bounds.** The table above gives $\Theta(l m)$ for Models 1 and 2 and $\Theta(m l^2)$ for the HMM model, in the [real RAM](/real-ram/) model with table lookups of constant cost.
- **Search space.** There are $(l + 1)^m$ directional alignments and $2^{l m}$ link sets, so enumeration is exponential. The tests of the model pages use it only to check the exact algorithms.
- **Hardness.** For IBM Models 3, 4 and 5, finding the Viterbi alignment is NP-hard, and computing $p(f \mid e)$, the sum over all alignments, is #P-complete (Udupa and Maji 2006). So the best alignment has no polynomial algorithm unless P = NP, and the sum has none unless P = #P. Training these models uses the HMM model or Model 2 for a start and sums over a neighbourhood of the best alignment found by hill climbing (Brown et al. 1993).

## Reductions

- **Viterbi alignment to a path in a DAG.** Under the HMM model, the best alignment is a longest path in a layered graph with one layer for each source word and one node for each target position, which [dynamic programming on a DAG](/dag-dynamic-programming/) solves.
- **One-to-one alignment to bipartite matching.** With a score for each link and at most one link for each word, the best alignment is a maximum weight matching in the complete bipartite graph between the two sentences.
- **From sentence alignment.** Word alignment needs aligned sentence pairs, which [sentence alignment](/sentence-alignment/) produces from aligned documents. Sentence alignment is monotone, so a dynamic program like [edit distance](/edit-distance/) solves it; word alignment allows crossing links and has no such order.

## Applications

- **Phrase-based translation.** [Phrase pair extraction](/phrase-pair-extraction/) takes all phrase pairs that are consistent with the symmetrized links, and the [phrase-based translation model](/phrase-based-translation-model/) scores them.
- **Lexicon learning.** The table $t(f \mid e)$ that the models learn while aligning is a probabilistic bilingual dictionary.
- **Analysis of neural translation.** The [attention](/additive-attention/) weights of an [encoder-decoder model](/encoder-decoder-model/) can be turned into links and compared with the links of these models.
- **Speech.** [Forced alignment](/forced-alignment/) is a related problem that links audio frames to words of a known transcript, also with an HMM and the Viterbi algorithm, but with monotone links.

## References
