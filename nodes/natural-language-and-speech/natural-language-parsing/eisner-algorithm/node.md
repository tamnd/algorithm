---
tag: JTW3A2
kind: algorithm
slug: eisner-algorithm
name: Eisner algorithm
aliases:
- Eisner projective parsing
area: natural-language-and-speech/natural-language-parsing
level: core
summary: An O(n^3) dynamic program over complete and incomplete spans that finds the best projective dependency tree under arc-factored scores.
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: the number of words of the sentence}
  time: {worst: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1996
  people: [Jason Eisner]
  note: "Eisner gave the cubic span-based chart for projective dependency parsing in 1996. McDonald, Crammer and Pereira made it the decoder of their discriminative graph-based parser in 2005."
prereqs: [projective-dependency-tree, dependency-parsing, optimal-substructure]
see_also: [mst-dependency-parsing, cyk-algorithm, probabilistic-cky, inside-outside-algorithm, lexicalized-pcfg, arc-hybrid-parsing, biaffine-dependency-parser, attachment-score]
sources:
  - url: https://aclanthology.org/C96-1058/
    title: "Jason M. Eisner, Three new probabilistic models for dependency parsing, an exploration, COLING 1996"
    locator: the parsing algorithm over spans whose heads are at their ends
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 4, Graph-Based Parsing (arc-factored models, the Eisner algorithm and its second-order extension)"
  - url: https://aclanthology.org/P05-1012/
    title: "Ryan McDonald, Koby Crammer and Fernando Pereira, Online large-margin training of dependency parsers, ACL 2005"
    locator: the use of the Eisner algorithm as the decoder of a first-order projective parser
  - url: https://aclanthology.org/E06-1011/
    title: "Ryan McDonald and Fernando Pereira, Online learning of approximate dependency parsing algorithms, EACL 2006"
    locator: "the second-order extension with sibling items, still in cubic time"
---

The Eisner algorithm finds the best [projective dependency tree](/projective-dependency-tree/) of a sentence when the score of a tree is the sum of the scores of its arcs. It is a dynamic program over spans of the sentence, like [CYK](/cyk-algorithm/), but each span keeps its head word at one of its two ends instead of anywhere inside. That one change brings the time from the $O(n^5)$ of lexicalized CKY down to $\Theta(n^3)$ for $n$ words. A span is complete when its head has all its dependents inside it, and incomplete when it is a single arc whose far end may still take dependents. Eisner described the method in 1996. It is the decoder of first-order and second-order projective graph-based parsers, and with sums in place of maxima it gives the partition function and the arc marginals that training needs.

## In plain words

A projective tree can be cut into pieces that are blocks of neighbouring words. Each piece has its main word at its left end or at its right end, and the rest of the piece hangs below that main word. Two kinds of pieces are enough. A finished piece is a word together with everything it governs on one side. An open piece is a word and one dependent, at the two ends of the block, with the words between them already attached on the correct sides. The algorithm builds the best piece of each kind for every block, from short blocks to long ones. An open piece joins two finished pieces that meet in the middle and adds one arrow. A finished piece joins an open piece with a finished piece. The best whole sentence is the best finished piece that starts at the root.

## The problem

The words are $1, \ldots, n$ and 0 is the artificial root, at the left edge. The input is a matrix of arc scores $s(h, d)$ for $h \in \{0, \ldots, n\}$ and $d \in \{1, \ldots, n\}$ with $h \neq d$; the scores are real numbers of any sign. For labeled parsing, take $s(h, d) = \max_r s(h, d, r)$ and keep the best label of each arc. The score of a [dependency tree](/dependency-tree/) $y$ with head function $h$ is $s(y) = \sum_{d = 1}^{n} s(h(d), d)$. The output is a projective tree of largest score, as a head list. In the main version the root may have any number of children; the single-root version, required by Universal Dependencies, gives the root exactly one child.

## The algorithm

For $0 \le i \le j \le n$ there are four tables. The arrow gives the side of the head:

- $C^{\to}[i, j]$: the best complete right span, a projective tree on the positions $i, \ldots, j$ rooted at $i$.
- $C^{\leftarrow}[i, j]$: the best complete left span, a projective tree on $i, \ldots, j$ rooted at $j$.
- $I^{\to}[i, j]$, for $i < j$: the best incomplete right span, a tree on $i, \ldots, j$ rooted at $i$ that contains the arc $i \to j$.
- $I^{\leftarrow}[i, j]$, for $0 < i < j$: the best incomplete left span, a tree on $i, \ldots, j$ rooted at $j$ that contains the arc $j \to i$.

Each table entry is a largest score, or "none" when no tree of that kind exists. In the pseudocode `CR`, `CL`, `IR` and `IL` stand for $C^{\to}$, $C^{\leftarrow}$, $I^{\to}$ and $I^{\leftarrow}$, and `max` skips the terms that are "none".

```pseudo id=main
EISNER(s, n)                                 ▷ arc scores s[h][d], words 1 … n, root 0
L1  for i <- 0 to n do CR[i, i] <- 0;  CL[i, i] <- 0
L2  for k <- 1 to n do                       ▷ the span length j - i
L3      for i <- 0 to n - k do
L4          j <- i + k;  m <- max over i <= r < j of CR[i, r] + CL[r + 1, j]
L5          if i > 0 then IL[i, j] <- m + s[j][i]          ▷ the arc j -> i
L6          IR[i, j] <- m + s[i][j]                         ▷ the arc i -> j
L7          CL[i, j] <- max over i <= r < j of CL[i, r] + IL[r, j]
L8          CR[i, j] <- max over i < r <= j of IR[i, r] + CR[r, j]
L9  return CR[0, n] and the tree read from the back pointers
```

Each maximum also stores its best split point $r$ as a back pointer. Line L9 reads the tree from them, top down from $C^{\to}[0, n]$, with an explicit stack: a complete span splits at its pointer into an incomplete span and a complete span, and an incomplete span adds its arc and splits into two complete spans. Line L5 skips $i = 0$, since no arc enters the root.

**One child of the root.** For the single-root version, line L4 uses only $r = 0$ when $i = 0$. Then $I^{\to}[0, j] = C^{\leftarrow}[1, j] + s(0, j)$: the root takes $j$ as its only dependent so far. Line L8 for $i = 0$ uses one such span and a complete span of $j$, so the root gets exactly one child.

## Example

Take *John saw Mary*, words 1 to 3, with the arc scores (row $h$, column $d$)

| $h \backslash d$ | 1 John | 2 saw | 3 Mary |
|---|---|---|---|
| 0 root | 9 | 10 | 9 |
| 1 John | | 20 | 3 |
| 2 saw | 30 | | 30 |
| 3 Mary | 11 | 0 | |

The four tables, span by span. A dash means "none".

| span $[i, j]$ | $I^{\leftarrow}$ | $I^{\to}$ | $C^{\leftarrow}$ | $C^{\to}$ |
|---|---|---|---|---|
| $[0, 1]$ | dash | 9 | dash | 9 |
| $[1, 2]$ | 30 | 20 | 30 | 20 |
| $[2, 3]$ | 0 | 30 | 0 | 30 |
| $[0, 2]$ | dash | 40 | dash | 40 |
| $[1, 3]$ | 31 | 23 | 31 | 50 |
| $[0, 3]$ | dash | 49 | dash | 70 |

Some of the entries in detail:

- $I^{\to}[0, 2]$: $m = \max(C^{\to}[0, 0] + C^{\leftarrow}[1, 2], C^{\to}[0, 1] + C^{\leftarrow}[2, 2]) = \max(0 + 30, 9 + 0) = 30$, so $I^{\to}[0, 2] = 30 + s(0, 2) = 40$. This is the root with the arc to *saw*, which already has *John* on its left.
- $C^{\to}[1, 3] = \max(I^{\to}[1, 2] + C^{\to}[2, 3], I^{\to}[1, 3] + C^{\to}[3, 3]) = \max(20 + 30, 23 + 0) = 50$: *John* heads *saw*, which heads *Mary*.
- $C^{\to}[0, 3] = \max(I^{\to}[0, 1] + C^{\to}[1, 3], I^{\to}[0, 2] + C^{\to}[2, 3], I^{\to}[0, 3] + C^{\to}[3, 3]) = \max(9 + 50, 40 + 30, 49 + 0) = 70$.

The back pointers give $C^{\to}[0, 3] \to I^{\to}[0, 2] + C^{\to}[2, 3]$, then $I^{\to}[0, 2] \to$ the arc $0 \to 2$ with $C^{\leftarrow}[1, 2]$, which holds the arc $2 \to 1$, and $C^{\to}[2, 3]$, which holds the arc $2 \to 3$. The tree is root $\to$ *saw*, *saw* $\to$ *John*, *saw* $\to$ *Mary*, with score 70 and head list `[-1, 2, 0, 2]`. It has one root child, so the single-root version returns the same tree. The best head of each word alone would give the cycle *John* $\leftrightarrow$ *saw*; the spans cannot express a cycle.

## Correctness

Each table entry is the best score over a set of projective trees on an interval with the head at one end. The proof rests on one fact about projective trees: the subtree of every word covers an interval. Take a tree counted by $I^{\to}[i, j]$, and remove the arc $i \to j$. The subtree of $j$ is an interval that ends at $j$, say $[r + 1, j]$, and the rest is a tree rooted at $i$ on $[i, r]$. So the tree is a complete right span on $[i, r]$, a complete left span on $[r + 1, j]$, and the arc; its score is the sum of the three parts. Conversely, every such pair of spans and the arc make a projective tree of the right kind. In the same way, a tree counted by $C^{\to}[i, j]$ with $i < j$ splits at the child $r$ of $i$ whose subtree contains $j$: the part with $i$, its children up to $r$, and the left side of $r$ is an incomplete span on $[i, r]$, and $r$ with its right descendants is a complete span on $[r, j]$. The parts are independent, so the best tree uses the best parts, and lines L4 to L8 compute every entry from shorter spans by induction on the length. The answer $C^{\to}[0, n]$ is the best projective tree on all positions rooted at 0. The full proof, including the single-root version and the reading of the tree, is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** For a span of length $k$, lines L4, L7 and L8 each try $k$ split points, and there are $n - k + 1$ spans of length $k$. The total number of terms is $3 \sum_{k = 1}^{n} k (n - k + 1) = n (n + 1)(n + 2) / 2$, each one addition and one comparison on the [word RAM](/word-ram/). So the time is $\Theta(n^3)$ for every input, since the loops do not depend on the scores. Reading the tree takes $O(n)$. With labels, choosing the best label of each arc first takes $O(n^2 |R|)$ more.

**Space.** The four tables and their four tables of back pointers have $O(n^2)$ entries each, so the space is $\Theta(n^2)$, back pointers included. Only the score $C^{\to}[0, n]$, without the tree, still needs the $\Theta(n^2)$ tables, because every span is read by longer spans.

## Properties

- **Exact.** It returns a tree of largest score among all projective trees, not an approximation.
- **Deterministic.** Ties are broken by the first split point $r$ in increasing order.
- **No spurious ambiguity.** Each projective tree has exactly one decomposition into spans. So with $(+, \times)$ in place of $(\max, +)$ the same loops sum over the trees, each tree once: with all weights 1 they count the projective trees, 1, 3, 12, 55, 273 for $n = 1$ to 5 and 1430715 for $n = 10$, which the tests check.
- **Semiring algorithm.** With log weights and log-sum-exp it gives the log of the partition function $\sum_y \exp s(y)$ over projective trees, the first half of the inside-outside computation of arc marginals.
- **Not online.** The long spans need the whole sentence.
- **Arc-factored only.** The score of a span must not depend on what lies outside it; this is what restricts the plain algorithm to first-order scores.

## Variants and improvements

- **Second order.** McDonald and Pereira (2006) add a sibling item, so that the score of an arc can depend on the previous dependent of the same head on the same side. The time stays $O(n^3)$.
- **Higher orders.** Items that also record a grandparent or more siblings give third-order parsers in $O(n^4)$ time.
- **Inside and outside.** Replacing max by log-sum-exp gives the inside scores, and a second pass gives the outside scores; their product is the marginal probability of each arc, as in the [inside-outside algorithm](/inside-outside-algorithm/). This trains a projective conditional model of trees.
- **Labels and features.** With arc-factored labeled scores, the labels are chosen per arc before the chart. Neural scorers such as the [biaffine parser](/biaffine-dependency-parser/) feed their arc scores to this chart when the output must be projective.
- **The same chart as a transition system.** Kuhlmann, Gómez-Rodríguez and Satta (2011) show that exact search over the computations of the [arc-hybrid](/arc-hybrid-parsing/) system with arc-factored scores is a cubic chart over items $[i, j]$ much like this one.
- **Non-projective trees.** Without the projective constraint, [Chu-Liu-Edmonds](/mst-dependency-parsing/) finds the best tree in $O(n^2)$.

## When to use it

Use the Eisner algorithm when the trees must be projective and the scores are arc-factored, or second order with the sibling extension: for English and other treebanks that are almost all projective, for projective conditional training, or to get a projective output from a neural scorer. For languages or schemes with many crossing arcs, use the maximum spanning arborescence. For very long inputs or when cubic time is too slow, transition-based parsers take a linear number of steps, at the price of exact search.

## Pitfalls

- **The root as a left dependent.** The incomplete left span with $i = 0$ would put an arc into the root. Line L5 must skip it.
- **The single-root rule.** Without it, the best tree may give the root several children. Taking the best tree and then deleting extra root arcs does not give the best single-root tree; restrict the root spans as above.
- **Ties and the back pointers.** If the back pointers store the wrong split when scores tie, the tree read out can score less than the table value. Store the split together with the maximum, in the same comparison.
- **Spurious counts.** A chart in which a tree has two decompositions gives the right maximum but wrong sums. The two-type split of this page has one decomposition per tree, so the counting check is a good test.
- **Underflow in the sum version.** A product of $n$ arc probabilities underflows for long sentences. Use log weights; the tests show a case where the plain sum is 0.0 and the log version is exact.
- **Not for non-projective gold trees.** Training a projective parser on a treebank with crossing arcs needs a policy for those trees, for example projectivizing them first.

## Implementations

## History

Before 1996, projective dependency parsing with lexical scores was done with lexicalized phrase structure charts, whose items carry a head word anywhere inside the span and take $O(n^5)$ time. Eisner (1996), comparing three probabilistic models of dependency structure, parsed with spans whose heads sit at their ends, which gives $O(n^3)$. McDonald, Crammer and Pereira (2005) used the algorithm as the decoder of a discriminative first-order parser trained online with large margins, and McDonald and Pereira (2006) extended it to second-order scores. It has remained the standard exact decoder for projective trees, also for neural arc scorers.

## References
