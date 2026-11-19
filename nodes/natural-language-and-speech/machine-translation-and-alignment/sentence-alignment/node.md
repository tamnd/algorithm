---
tag: JKYA5Q
kind: problem
slug: sentence-alignment
name: Sentence alignment
aliases:
- bitext alignment
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Pair the sentences of a document with those of its translation, allowing one-to-many, many-to-one and unmatched sentences.
prereqs: [parallel-corpus]
see_also: [gale-church-alignment, word-alignment, edit-distance, dynamic-time-warping, needleman-wunsch, banded-alignment, sentence-boundary-detection, dag-dynamic-programming]
sources:
  - paper: "William A. Gale and Kenneth W. Church, A program for aligning sentences in bilingual corpora, Computational Linguistics 19(1), 1993, pages 75 to 102"
    title: Gale and Church 1993
    locator: the problem of aligning sentences, the bead types and their frequencies, the dynamic program and its evaluation
  - paper: doi:10.3115/981344.981366
    title: Peter F. Brown, Jennifer C. Lai and Robert L. Mercer, Aligning sentences in parallel corpora, 29th Annual Meeting of the ACL, 1991, pages 169 to 176
    locator: sentence alignment of the Canadian Hansards from sentence lengths in words
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 2 (Words, Sentences, Corpora)"
---

Sentence alignment is the problem of pairing the sentences of a text with the sentences of its translation. Translators mostly keep the order of the sentences, but they sometimes split one sentence into two, merge two into one, or leave a sentence out. So the answer is a sequence of *beads*, each joining a short block of consecutive sentences of one text with a short block of the other, in order. Because the beads are in order, the problem is a monotone [dynamic program](/dag-dynamic-programming/) like [edit distance](/edit-distance/), solved in time proportional to the product of the numbers of sentences. Methods differ in the cost of a bead: [Gale and Church (1993)](/gale-church-alignment/) and Brown, Lai and Mercer (1991) use only sentence lengths, and other methods use lexical anchors, words that are known to translate each other. Sentence alignment turns aligned documents into the sentence pairs of a [parallel corpus](/parallel-corpus/), which [word alignment](/word-alignment/) and the training of translation models need.

## In plain words

You have a report in English and the same report in French. You want a list that says which French sentences translate which English sentences. Most of the time one sentence matches one sentence, and the order is the same. But a translator may cut a long sentence in two, join two short ones, or drop one. A program has to find the matches without understanding either language well. A simple clue is length: a long sentence usually has a long translation. A stronger clue is shared words, such as numbers, names, or words found in a dictionary. The program tries all ways to walk through both texts in order and picks the one with the best total score.

## Definition

**Input.** Two texts split into sentences, $u_1, \ldots, u_I$ and $v_1, \ldots, v_J$, that translate each other, and a set $T$ of allowed bead types $(p, q)$, usually $\{(1,1), (1,0), (0,1), (2,1), (1,2), (2,2)\}$.

**Output.** A sequence of beads $(p_1, q_1), \ldots, (p_K, q_K) \in T$ with $\sum_k p_k = I$ and $\sum_k q_k = J$. Bead $k$ joins the next $p_k$ sentences of the first text with the next $q_k$ sentences of the second. Every sentence is in exactly one bead, and the beads keep the order of both texts.

**Objective.** A cost $\mathrm{cost}(\text{block}_1, \text{block}_2)$ for each bead, often the negative log probability of the bead under a model. The task is to find the alignment of least total cost. The answer is only as good as the cost: the problem has no single correct cost, and gold alignments made by people are used to compare costs.

Equivalently, an alignment is a path from $(0, 0)$ to $(I, J)$ in the grid of pairs $(i, j)$, with steps $(p, q) \in T$.

## Variants

- **Bead types.** Some methods allow only 1-1, 1-0 and 0-1, and some allow larger blocks such as 1-3 or 3-1.
- **Length-based costs.** The cost uses only the lengths of the blocks, in characters (Gale and Church 1993) or in words (Brown, Lai and Mercer 1991). These need no knowledge of the languages.
- **Lexical costs.** The cost uses words that translate each other, from a dictionary, from shared strings such as numbers and names, or from a translation model. Such costs are more robust when the texts differ in places.
- **Paragraphs first.** Align the paragraphs or other markers first, then the sentences inside each pair of paragraphs. This makes the grids small.
- **Comparable corpora.** If the texts are not translations of each other but only on the same subject, the order is not kept, and the task becomes a search for good pairs anywhere in the two texts. That is not a monotone problem.

## Examples

- **One to one.** If both texts have three sentences of 40, 25 and 60 characters on one side and 42, 27 and 63 on the other, the alignment is three 1-1 beads.
- **A merge.** For lengths 30, 50, 20 in the first text and 32, 74 in the second, a good alignment is a 1-1 bead (30 with 32) and a 2-1 bead (50 and 20, total 70, with 74). A cost that compares block lengths prefers it to three beads that leave a sentence unmatched.
- **Counting.** With only the types 1-1, 1-0 and 0-1, the alignments are the lattice paths of the Delannoy numbers: 3 for $I = J = 1$ and 13 for $I = J = 2$. Their number grows like $(3 + 2\sqrt 2)^n / \sqrt n$ for $I = J = n$, so trying them one by one is out of the question.

## Known algorithms

| Algorithm | Cost of a bead | Time | Note |
|---|---|---|---|
| [Gale-Church alignment](/gale-church-alignment/) | bead prior and a Gaussian model of the length difference in characters | $\Theta(I J)$ | the code of the page has the six types above |
| Brown, Lai and Mercer (1991) | a probabilistic model of lengths in words | $\Theta(I J)$ | used on the Canadian Hansards |
| lexical methods | word correspondences or a translation model | $\Theta(I J)$ times the cost of one bead score | slower and more robust |
| [banded](/banded-alignment/) dynamic program | any of the above | $O((I + J) w)$ | only paths within $w$ of the diagonal |

The dynamic program is $D(0, 0) = 0$ and

$$D(i, j) = \min_{(p, q) \in T,\ p \le i,\ q \le j} D(i - p, j - q) + \mathrm{cost}(u_{i-p+1..i}, v_{j-q+1..j}),$$

with the best alignment found by [traceback](/traceback/). With [prefix sums](/prefix-sums/) of the lengths, each length-based bead cost takes constant time.

## Bounds

- **Upper bound.** With a fixed set $T$ and bead costs of constant time, the dynamic program takes $\Theta(I J)$ time and space. The space can be reduced to $O(I + J)$ by the divide and conquer method of Hirschberg, at a constant factor in time.
- **Band.** If the best path stays within $w$ cells of the diagonal from $(0, 0)$ to $(I, J)$, the banded program is exact in $O((I + J) w)$ time. If the band is too narrow, it returns the best path inside the band, which can be worse.
- **Input size.** Any exact algorithm must look at every sentence, so $\Omega(I + J)$ time is needed.

## Reductions

- **To a shortest path in a DAG.** The grid of pairs $(i, j)$ with the steps of $T$ is a directed acyclic graph, and the best alignment is a shortest path from $(0, 0)$ to $(I, J)$. [DAG dynamic programming](/dag-dynamic-programming/) solves it in time linear in the number of edges, $\Theta(|T| \, I J)$.
- **Edit distance as a special case.** With $T = \{(1,1), (1,0), (0,1)\}$, cost 0 for equal items and 1 otherwise, the problem is [edit distance](/edit-distance/). [Needleman-Wunsch](/needleman-wunsch/) and [dynamic time warping](/dynamic-time-warping/) are the same scheme with other steps and costs.
- **From sentence boundaries.** The input sentences come from [sentence boundary detection](/sentence-boundary-detection/). Its errors appear as extra 2-1 and 1-2 beads.

## Applications

- **Building parallel corpora.** Sentence alignment of documents such as parliament proceedings gives the sentence pairs on which [word alignment](/word-alignment/) and translation models are trained.
- **Translation memories and bilingual concordances.** Aligned sentences let translators and lexicographers search for a phrase and see its earlier translations.
- **Filtering.** Beads of high cost or of type 1-0 and 0-1 point to parts of the texts that are not translations of each other, which can then be removed.

## References
