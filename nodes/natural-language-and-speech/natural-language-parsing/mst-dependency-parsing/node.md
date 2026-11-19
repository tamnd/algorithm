---
tag: Z4H7TB
kind: algorithm
slug: mst-dependency-parsing
name: Maximum spanning tree dependency parsing
aliases:
- MST parser
- graph-based dependency parsing
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "Score every possible arc and take the maximum spanning arborescence by Chu-Liu-Edmonds, which allows non-projective trees."
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: the number of words of the sentence}
  time: {worst: O(n^3), best: Θ(n^2)}
  space: {extra: O(n^3)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2005
  people: [Ryan McDonald, Fernando Pereira, Kiril Ribarov, Jan Hajič]
  note: "McDonald, Pereira, Ribarov and Hajič cast non-projective dependency parsing with arc-factored scores as the maximum spanning arborescence problem, solved by the algorithm of Chu and Liu (1965) and Edmonds (1967)."
prereqs: [dependency-parsing, edmonds-arborescence]
see_also: [eisner-algorithm, minimum-arborescence, matrix-tree-theorem, cycle-contraction, biaffine-dependency-parser, swap-transition-system, projective-dependency-tree, structured-perceptron]
sources:
  - url: https://aclanthology.org/H05-1066/
    title: "Ryan McDonald, Fernando Pereira, Kiril Ribarov and Jan Hajič, Non-projective dependency parsing using spanning tree algorithms, HLT-EMNLP 2005"
    locator: "the reduction to the maximum spanning arborescence, the Chu-Liu-Edmonds algorithm in the maximum form, and online large-margin training"
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 4, Graph-Based Parsing (arc-factored models and the maximum spanning tree algorithm)"
  - paper: doi:10.6028/jres.071B.032
    title: "Jack Edmonds, Optimum branchings, Journal of Research of the National Bureau of Standards 71B(4) (1967), 233-240"
    locator: the contraction of cycles of best entering arcs
  - paper: "Y. J. Chu and T. H. Liu, On the shortest arborescence of a directed graph, Scientia Sinica 14 (1965), 1396-1400"
    locator: the same algorithm, found independently
  - paper: doi:10.1002/net.3230070103
    title: "Robert E. Tarjan, Finding optimum branchings, Networks 7(1) (1977), 25-35"
    locator: the O(n^2) implementation for dense graphs
  - url: https://aclanthology.org/D07-1015/
    title: "Terry Koo, Amir Globerson, Xavier Carreras and Michael Collins, Structured prediction models via the matrix-tree theorem, EMNLP-CoNLL 2007"
    locator: "the partition function and the arc marginals of non-projective trees, with and without one child of the root"
---

Maximum spanning tree (MST) dependency parsing finds the best [dependency tree](/dependency-tree/) of a sentence, projective or not, when the score of a tree is the sum of the scores of its arcs. The words and the artificial root are the nodes of a complete directed graph, each possible arc $h \to d$ carries the score $s(h, d)$, and a dependency tree is exactly a spanning [arborescence](/arborescence/) rooted at the root. So the parser takes a maximum spanning arborescence, with the algorithm of Chu and Liu (1965) and [Edmonds (1967)](/edmonds-arborescence/). Each word first takes its best head. If that makes a cycle, the cycle is contracted into one node, the arcs into it are rescored, and the smaller problem is solved; then the cycle is opened at the one word that takes a head from outside. McDonald, Pereira, Ribarov and Hajič (2005) introduced this view of parsing. The simple recursive form runs in $O(n^3)$ time for $n$ words, and Tarjan's form in $O(n^2)$, which is optimal for a dense score matrix. Unlike the [Eisner algorithm](/eisner-algorithm/), it can return crossing arcs.

## In plain words

Every word must choose one word it belongs to, or the start symbol, and each choice has a score. First let each word take its best choice alone. If the choices lead back to the start without loops, they form a tree and nothing can do better. If some words choose each other in a loop, at least one of them must look outside the loop instead. Treat the loop as one big word. Price each outside choice by how much it would cost the loop to accept it, that is, its score minus the score of the loop link it replaces. Solve this smaller problem in the same way. Then open the loop: the winning outside choice tells which word leaves the loop, and the other words keep their loop links.

## The problem

The words are $1, \ldots, n$ and 0 is the root. The input is a matrix of arc scores $s(h, d)$, real numbers of any sign, for $h \in \{0, \ldots, n\}$, $d \in \{1, \ldots, n\}$, $h \ne d$. For labeled parsing, take $s(h, d) = \max_r s(h, d, r)$ and keep the best label of each arc. The output is a head list $h(1), \ldots, h(n)$ that forms a tree rooted at 0 and maximizes $\sum_d s(h(d), d)$, over all trees, projective or not. In the main version the root may have any number of children. In the single-root version it has exactly one; the page shows how to enforce that below.

## The algorithm

The recursion works on a general directed graph with node set $V$, root $\rho$ and arc scores $w$. At the top level $V = \{0, \ldots, n\}$, $\rho = 0$ and $w(h, d) = s(h, d)$.

```pseudo id=main
CLE(V, rho, w)                               ▷ returns a head for every v in V other than rho
L1  for each v in V, v != rho: best[v] <- argmax over u of w(u, v)
L2  look for a cycle C in the arcs best[v] -> v
L3  if there is none then return best
L4  add a new node c that stands for C;  S <- sum over v in C of w(best[v], v)
L5  build w' on V' = (V - C) + {c}:
        for u outside C:  w'(u, c) <- max over v in C of w(u, v) - w(best[v], v) + S
        for d outside C:  w'(c, d) <- max over v in C of w(v, d)
        arcs between nodes outside C keep their scores
L6  head' <- CLE(V', rho, w')
L7  map head' back: the arc u -> c becomes u -> v for the v in C that gave its maximum,
        an arc c -> d becomes v -> d for the v in C that gave its maximum, others stay
L8  every v in C that got no head in L7 keeps best[v]
L9  return the heads
```

The parser calls `CLE({0, ..., n}, 0, s)`. Each maximum in line L5 also records which cycle node $v$ gave it, so that line L7 can undo the contraction.

**One child of the root.** For the single-root version, run CLE $n$ times. In run $m$, delete every root arc except $0 \to m$. Return the best of the $n$ trees. Each run gives the best tree in which the root has the single child $m$, so the best of them is the best single-root tree. Deleting the extra root arcs from the unconstrained tree does not work.

## Example

Take *John saw Mary*, words 1 to 3, with the scores (row $h$, column $d$)

| $h \backslash d$ | 1 John | 2 saw | 3 Mary |
|---|---|---|---|
| 0 root | 9 | 10 | 9 |
| 1 John | | 20 | 3 |
| 2 saw | 30 | | 30 |
| 3 Mary | 11 | 0 | |

**Line L1.** The best head of *John* is *saw* (30), of *saw* is *John* (20), and of *Mary* is *saw* (30).

**Line L2.** *John* and *saw* head each other: the cycle $C = \{1, 2\}$, with $S = 30 + 20 = 50$.

**Line L5.** Contract $C$ into $c$. The scores into $c$:

- from the root: through *John*, $9 - 30 + 50 = 29$; through *saw*, $10 - 20 + 50 = 40$. So $w'(0, c) = 40$, entering at *saw*.
- from *Mary*: through *John*, $11 - 30 + 50 = 31$; through *saw*, $0 - 20 + 50 = 30$. So $w'(3, c) = 31$, entering at *John*.

The scores out of $c$: $w'(c, 3) = \max(s(1, 3), s(2, 3)) = \max(3, 30) = 30$, leaving from *saw*. The root arc $w'(0, 3) = 9$ stays.

**Line L6.** In the graph on $\{0, 3, c\}$, the best head of $c$ is the root (40 against 31) and the best head of *Mary* is $c$ (30 against 9). There is no cycle, and the score is $40 + 30 = 70$.

**Lines L7 and L8.** The arc $0 \to c$ came through *saw*, so *saw* takes the root as head and the cycle arc *John* $\to$ *saw* is dropped. The arc $c \to 3$ came from *saw*, so *Mary* takes *saw*. *John* got no head from L7 and keeps *saw*. The result is the head list `[-1, 2, 0, 2]` with score $10 + 30 + 30 = 70$, the same as the value of the contracted problem. This tree is projective, so the Eisner algorithm finds it too.

**A non-projective answer.** With four words and the scores $s(0, 2) = s(2, 4) = s(4, 1) = s(2, 3) = 10$ and 0 for all other arcs, CLE returns `[-1, 4, 0, 2, 2]` with score 40. The arc $4 \to 1$ passes over word 2, the head of 4, so the tree is not projective, and the best projective tree scores less. The tests check both facts.

## Correctness

Line L1 gives an upper bound: every word gets its best entering arc, and no tree can score more than the sum of these. If these arcs have no cycle, they form a tree, and the bound is met. If there is a cycle $C$, a short exchange argument shows that some best tree contains all arcs of $C$ but one: take a best tree, find the first node of $C$ on its path from the root, and give every other node of $C$ its cycle arc; the result is still a tree and does not score less, since each new arc is the best into its node. The trees with this form correspond one to one to the trees of the contracted graph, and the rescoring of line L5 makes the scores equal: a tree that enters $C$ at $v$ from $u$ scores $w(u, v) + (S - w(best[v], v))$ plus its other arcs, which is $w'(u, c)$ plus the same arcs. So the best tree of the contracted graph, mapped back, is a best tree of the original graph. Induction on the number of nodes completes the proof, which is in [the correctness proof](proofs/correctness.md). The single-root version is correct because the $n$ runs cover all trees with one root child, each run exactly.

## Complexity

**Time.** Lines L1 to L5 and L7 to L8 touch each arc once, which is $O(|V|^2)$ for a dense graph. Each contraction removes at least one node, since a cycle has at least two nodes, so there are at most $n$ levels of recursion, on graphs of $n + 1, n, \ldots$ nodes. The total is $O(n^3)$ in the worst case, for example when every level finds a cycle of two nodes. The best case is $\Theta(n^2)$: reading the score matrix already costs that, and if the best heads form a tree, the algorithm stops after one level. Tarjan (1977) organizes the contractions so that the whole run takes $O(n^2)$ for dense graphs, which matches the input size. The single-root version by $n$ runs multiplies the time by $n$.

**Space.** The score matrix of each level is a new graph, and the recursion keeps all levels until it returns, so the simple form uses $O(n^3)$ extra space in the worst case. Overwriting the scores in place and storing only the cycle of each level, as Tarjan's form does, brings it down to $O(n^2)$.

## Properties

- **Exact over all trees.** It returns a tree of largest score among all $(n + 1)^{n - 1}$ trees, projective or not; the tests compare it with a search over all trees for small $n$.
- **Deterministic.** Ties in line L1 are broken by the first head in the order of the nodes.
- **Arc-factored only.** The proof needs the score of a tree to be the sum of independent arc scores. With second-order scores, non-projective parsing is NP-hard (McDonald and Pereira 2006; McDonald and Satta 2007).
- **Recursive.** Each contraction calls the algorithm on a smaller graph.
- **Not online.** The best head of each word depends on words to its right.
- **Sums are a determinant.** The sum over all trees of the product of arc weights $\exp s(h, d)$ is the determinant of a Laplacian minor, by the [matrix-tree theorem](/matrix-tree-theorem/), and its derivatives give the arc marginals. The code computes both exactly with fractions, with and without the single-root rule, and the tests check them against a sum over all trees.

## Variants and improvements

- **Tarjan's implementation.** $O(n^2)$ for dense graphs, and $O(m \log n)$ for $m$ arcs; the version of Gabow, Galil, Spencer and Tarjan takes $O(m + n \log n)$.
- **The root constraint in one run.** Faster methods than $n$ separate runs exist for the single-root version; Zmigrod, Vieira and Cotterell (2020) give an $O(n^2)$ method for dependency parsing.
- **K best trees.** Camerini, Fratta and Maffioli give an algorithm for the $k$ best arborescences, used for reranking.
- **Training.** McDonald et al. (2005) trained the arc scores with an online large-margin method, with CLE as the decoder in each update. The matrix-tree theorem gives the marginals needed for conditional training of a log-linear model over trees (Koo, Globerson, Carreras and Collins 2007), and the same holds for neural arc scorers such as the [biaffine parser](/biaffine-dependency-parser/).
- **Approximate second order.** McDonald and Pereira (2006) take the best projective second-order tree from the Eisner chart and then change heads one at a time, as long as the score rises and the result stays a tree.

## When to use it

Use MST parsing when the arc scores are arc-factored and the trees may have crossing arcs, as in languages with free word order or in treebanks with many non-projective arcs, and when an exact decoder is wanted. With a neural arc scorer it is the standard decoder. When the trees must be projective, use the Eisner algorithm. When the score must depend on pairs of arcs, exact non-projective search is NP-hard, and approximate search or a transition-based parser such as the [swap system](/swap-transition-system/) is the usual choice.

## Pitfalls

- **The root as a dependent.** The root must have no entering arc. Leave out the column of the root, or give it the score minus infinity.
- **Minimum or maximum.** Edmonds' algorithm is often stated for the [minimum arborescence](/minimum-arborescence/). Negate the scores, or take maxima everywhere; rescoring by subtraction must then use the maximum form of line L5.
- **Several root children.** The unconstrained answer may attach several words to the root. If the treebank requires one, use the single-root version; removing the extra arcs afterwards gives a tree that is not the best single-root tree.
- **Forgetting the map back.** The arcs into and out of $c$ must remember which cycle node gave their maximum. Without this record, the expansion attaches the wrong word.
- **Nested cycles.** A contracted node can lie on a new cycle at the next level. The recursion handles this, but an implementation that contracts only once does not; the tests include such a graph.
- **Ties in floating point.** With nearly equal scores, the cycle found can change with rounding; the score of the result is still optimal up to rounding, but the tree may differ between runs on different machines.

## Implementations

## History

Chu and Liu (1965) and Edmonds (1967) found the optimum branching algorithm independently, and Tarjan (1977) gave fast implementations. In parsing, Eisner's (1996) cubic chart had made projective arc-factored parsing exact, and transition-based parsers handled non-projective trees with pseudo-projective transformations. McDonald, Pereira, Ribarov and Hajič (2005) observed that dropping projectivity turns the arc-factored problem into a maximum spanning arborescence, which can be solved in $O(n^2)$, and showed good results on Czech. McDonald and Pereira (2006) and McDonald and Satta (2007) then showed that non-projective parsing becomes NP-hard as soon as the scores look at pairs of arcs. In 2007 several groups, among them Koo, Globerson, Carreras and Collins, used the matrix-tree theorem for the partition function. With neural arc scores, as in the biaffine parser of Dozat and Manning (2017), the arborescence decoder remains in common use.

## References
