---
tag: THV087
kind: problem
slug: dependency-parsing
name: Dependency parsing
aliases:
- dependency analysis
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "Find the dependency tree of a sentence, the head and the relation label of each word."
prereqs: [dependency-tree]
see_also: [eisner-algorithm, mst-dependency-parsing, arc-standard-parsing, biaffine-dependency-parser, attachment-score, projective-dependency-tree, constituency-parsing, treebank]
sources:
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 2 (the parsing problem), Chapter 3 (transition-based parsing), Chapter 4 (graph-based parsing) and Chapter 6 (evaluation)"
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: "the transition systems, their soundness and completeness, and their complexity"
  - url: https://aclanthology.org/H05-1066/
    title: "Ryan McDonald, Fernando Pereira, Kiril Ribarov and Jan Hajič, Non-projective dependency parsing using spanning tree algorithms, HLT-EMNLP 2005"
    locator: the reduction of arc-factored non-projective parsing to the maximum spanning arborescence
  - url: https://aclanthology.org/E06-1011/
    title: "Ryan McDonald and Fernando Pereira, Online learning of approximate dependency parsing algorithms, EACL 2006"
    locator: second-order projective parsing in cubic time and the hardness of second-order non-projective parsing
  - url: https://aclanthology.org/W07-2216/
    title: "Ryan McDonald and Giorgio Satta, On the complexity of non-projective data-driven dependency parsing, IWPT 2007"
    locator: "the hardness results for non-projective parsing beyond arc-factored scores, and the partition function by the matrix-tree theorem"
---

Dependency parsing is the task of finding the [dependency tree](/dependency-tree/) of a sentence: for each word, the word it depends on, called its head, and the grammatical relation between them. A parser learns this from a [treebank](/treebank/) of sentences with gold trees and is judged by its [attachment score](/attachment-score/). There are two main families of methods. Graph-based parsers give a score to every possible arc and search for the best tree, exactly: the [Eisner algorithm](/eisner-algorithm/) for [projective trees](/projective-dependency-tree/) in $O(n^3)$ time, and the [Chu-Liu-Edmonds algorithm](/mst-dependency-parsing/) for all trees in $O(n^2)$. Transition-based parsers build the tree with a stack and a sequence of moves chosen by a classifier, in a linear number of steps, as in [arc-standard](/arc-standard-parsing/) and [arc-eager](/arc-eager-parsing/) parsing. Neural scorers, such as the [Chen-Manning parser](/chen-manning-parser/) and the [biaffine parser](/biaffine-dependency-parser/), fit into either family.

## In plain words

A sentence has a hidden structure: which word modifies which. In "the cat sat on the mat", "the" belongs to "cat", "cat" is the subject of "sat", and "mat" tells where the sitting happened. Dependency parsing writes this structure down as one arrow into each word, from the word it belongs to, plus a name on each arrow. The main verb gets its arrow from an extra start symbol. The arrows always form a tree, so there is no loop and every word connects to the start. A parser learns from many sentences that people have marked by hand. It either scores every possible arrow and picks the best tree, or reads the sentence from left to right and makes one small decision at a time.

## Definition

**Input.** A sentence $x = w_1 \cdots w_n$, often with a part-of-speech tag for each word, and a set $R$ of relation labels. The artificial root $w_0$ is added at the left edge.

**Output.** A dependency tree $y$: a head $h(d) \in \{0, \ldots, n\} \setminus \{d\}$ and a label $r(d) \in R$ for each word $d \in \{1, \ldots, n\}$, such that the arcs $(h(d), d, r(d))$ form a tree rooted at 0. Let $\mathcal{Y}(x)$ be the set of allowed trees: all trees, only the projective ones, and with or without the rule that the root has exactly one child.

**As a search problem.** Given a scoring function $s(x, y)$, find

$$\hat{y} = \operatorname{argmax}_{y \in \mathcal{Y}(x)} s(x, y).$$

The scores are **arc-factored** (first order) when $s(x, y) = \sum_{d = 1}^{n} s(h(d), d, r(d))$. Then the best label of each arc can be chosen first, independently, and the problem becomes the search over unlabeled trees with the arc scores $s(h, d) = \max_r s(h, d, r)$.

**As a learning problem.** Given a treebank of pairs $(x, y^\ast)$, choose the scoring function, or the transition classifier, so that the trees predicted on new sentences have a high attachment score.

**The root.** The definition allows the root to have several children. Universal Dependencies requires exactly one, and each method on these pages says whether it enforces that.

## Variants

- **Projective or not.** Restricting $\mathcal{Y}(x)$ to projective trees permits the cubic dynamic program and the stack-based transition systems. English treebanks converted from phrase structure are almost all projective; other languages and annotation schemes have more crossing arcs, and the non-projective methods are needed there.
- **Labeled or unlabeled.** Unlabeled parsing predicts the heads only. With arc-factored scores the labels add a factor $|R|$ to the cost of scoring the arcs and nothing to the search.
- **Higher order.** Second-order scores add terms for pairs of arcs, such as two adjacent dependents of one head (siblings) or a head and its own head (grandparent). Third-order scores add triples.
- **Transition-based.** The parser has no global score. A classifier picks the next move from the current configuration, and the tree is whatever the moves build. Beam search and global training give such a parser a score over whole move sequences.
- **Graphs instead of trees.** Enhanced and semantic dependency representations let a word have several heads or none. Those are graph parsing problems and are outside these pages.
- **One root child.** Requiring exactly one child of the root changes the best tree, and every exact algorithm has a variant for it.

## Examples

**A first-order instance.** For *John saw Mary*, with the root 0 and the words 1 to 3, let the arc scores $s(h, d)$ be the matrix (row $h$, column $d$)

| $h \backslash d$ | 1 John | 2 saw | 3 Mary |
|---|---|---|---|
| 0 root | 9 | 10 | 9 |
| 1 John | | 20 | 3 |
| 2 saw | 30 | | 30 |
| 3 Mary | 11 | 0 | |

The best tree is root $\to$ *saw*, *saw* $\to$ *John*, *saw* $\to$ *Mary*, with score $10 + 30 + 30 = 70$, head list `[-1, 2, 0, 2]`. It is projective and has one root child, so all four versions of the problem have the same answer here. Choosing the best head of each word on its own gives *John* $\leftarrow$ *saw* (30), *saw* $\leftarrow$ *John* (20) and *Mary* $\leftarrow$ *saw* (30), which is not a tree: *John* and *saw* head each other. The [MST page](/mst-dependency-parsing/) shows how Chu-Liu-Edmonds repairs this cycle.

**Projective and non-projective optima differ.** With other scores the best tree can be non-projective, for example the tree of *A hearing is scheduled on the issue today* on the [projective tree](/projective-dependency-tree/) page. Then the Eisner algorithm returns the best projective tree, whose score is lower. The tests of the Eisner page contain such a case: the best of all trees scores 40, and the best projective tree scores less.

**A transition sequence.** The arc-standard system builds the tree of *the cat sat on the mat* with the 12 moves SH SH LA-det SH LA-nsubj SH SH SH LA-det LA-case RA-obl RA-root, where SH moves a word onto the stack and LA and RA add an arc between the two top stack words.

## Known algorithms

| method | trees | scores | time | page |
|---|---|---|---|---|
| Eisner | projective | arc-factored | $O(n^3)$ | [eisner-algorithm](/eisner-algorithm/) |
| Chu-Liu-Edmonds | all | arc-factored | $O(n^2)$ dense (Tarjan 1977) | [mst-dependency-parsing](/mst-dependency-parsing/) |
| second-order Eisner | projective | sibling pairs | $O(n^3)$ (McDonald and Pereira 2006) | |
| arc-standard | projective | greedy classifier | $2n$ moves | [arc-standard-parsing](/arc-standard-parsing/) |
| arc-eager | projective | greedy classifier | at most $2n$ moves | [arc-eager-parsing](/arc-eager-parsing/) |
| arc-hybrid | projective | greedy classifier | $2n$ moves | [arc-hybrid-parsing](/arc-hybrid-parsing/) |
| swap | all | greedy classifier | at most $n + n^2$ moves | [swap-transition-system](/swap-transition-system/) |
| Chen-Manning | projective | feedforward network on arc-standard | $2n$ network calls | [chen-manning-parser](/chen-manning-parser/) |
| biaffine | all | biaffine arc scores | $O(n^2)$ scores, then a tree decoder | [biaffine-dependency-parser](/biaffine-dependency-parser/) |

The transition-based times count moves; each move costs one call of the classifier. The [dynamic oracle](/dynamic-oracle/) is a training method for the transition parsers, not a parser.

## Bounds

- **Search space.** There are $(n + 1)^{n - 1}$ unlabeled trees over $n$ words, and $n^{n - 1}$ with one root child; the projective trees number 1, 3, 12, 55, 273 for $n = 1$ to 5. Listing them is out of the question for real sentences, so every exact method uses the structure of the scores.
- **Input size.** Arc-factored scores form an $(n + 1) \times (n + 1)$ matrix, so any exact algorithm that reads them takes $\Omega(n^2)$ time. The $O(n^2)$ version of Chu-Liu-Edmonds meets this bound for dense scores. For projective trees the best known time is the $O(n^3)$ of Eisner; the older lexicalized CKY parsing of the same problem takes $O(n^5)$.
- **Hardness.** With second-order scores, non-projective parsing is NP-hard (McDonald and Pereira 2006; McDonald and Satta 2007), while projective second-order parsing stays cubic. Parsers for this case use approximate search.
- **Transition systems.** Arc-standard and arc-hybrid use exactly $2n$ moves, arc-eager at most $2n$, and swap at most $n + n^2$; with a classifier of constant cost these give linear time, and quadratic time in the worst case for swap.

## Reductions

- **To the maximum spanning arborescence.** First-order non-projective parsing is the maximum spanning [arborescence](/arborescence/) problem on the complete directed graph over $\{0, \ldots, n\}$ with weights $s(h, d)$, rooted at 0 (McDonald et al. 2005). [Edmonds' algorithm](/edmonds-arborescence/) solves it; it is usually stated for the [minimum arborescence](/minimum-arborescence/), and a parser negates the scores or takes maxima in place of minima.
- **To bilexical context-free parsing.** First-order projective parsing is a special case of parsing with a bilexical [context-free grammar](/context-free-grammar/), in which each phrase is named by its head word; the Eisner algorithm is a faster chart for that grammar.
- **From constituency trees.** [Head rules](/head-rules/) convert a [constituency](/constituency-parsing/) treebank into dependency trees, and that is how many dependency treebanks were first made.
- **Sums over trees.** For training with probabilities, the sum over all non-projective trees of the product of arc weights is a determinant, by the [matrix-tree theorem](/matrix-tree-theorem/). The sum over projective trees is the inside version of the Eisner algorithm.

## Applications

Dependency trees are an input to relation extraction and information extraction (the path between two words in the tree), [semantic role labeling](/semantic-role-labeling/), question answering, grammar checking, and the reordering step of some machine translation systems. Treebank projects use parsers to pre-annotate sentences for human correction. Parsing also serves to compare languages, since Universal Dependencies annotates many languages with the same labels.

## References
