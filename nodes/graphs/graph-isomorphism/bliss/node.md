---
tag: XYMF0D
kind: algorithm
slug: bliss
name: Bliss
aliases:
- bliss graph canonization
area: graphs/graph-isomorphism
level: advanced
summary: Junttila-Kaski canonical labeling and automorphism tool using individualization-refinement with pruning.
solves: [canonical-labeling, graph-automorphism, graph-isomorphism-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n! n m), best: O(n m)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [individualization-refinement, partition-refinement, nauty]
see_also: [nauty, canonical-labeling, graph-automorphism, weisfeiler-leman, automorphism-orbit, equitable-partition]
sources:
  - paper: doi:10.1137/1.9781611972870.13
    title: Tommi Junttila and Petteri Kaski, Engineering an efficient canonical labeling tool for large and sparse graphs, Proceedings of the Ninth Workshop on Algorithm Engineering and Experiments (ALENEX 2007), 135 to 149
    locator: Sections 2 to 5 (the partition data structure, refinement with certificates, the search and its pruning, and experiments)
  - paper: doi:10.1007/978-3-642-19754-3_16
    title: Tommi Junttila and Petteri Kaski, Conflict propagation and component recursion for canonical labeling, TAPAS 2011, Lecture Notes in Computer Science 6595, 151 to 162
    locator: the whole paper (failure recording, conflict propagation and component recursion added to bliss)
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60, 94 to 112 (2014)
    locator: Sections 2 and 3 (the common framework of nauty, Traces, bliss and saucy, and the pruning by node invariants)
---

Bliss, by Tommi Junttila and Petteri Kaski (2007), is a program for [canonical labeling](/canonical-labeling/) and [automorphism groups](/graph-automorphism/) that follows the [individualization-refinement](/individualization-refinement/) scheme of [nauty](/nauty/) but is built for large sparse graphs. Its partitions live in one array with cell boundaries, refinement works from a queue of splitter cells and costs time proportional to the edges it touches, and each refinement leaves a trace, the certificate of the node. Comparing certificates with the best path found so far cuts most branches early, and automorphisms cut the rest. It is widely used for symmetry detection in SAT, constraint and integer programming instances with millions of vertices.

## In plain words

Bliss solves the same task as nauty: give a network a standard numbering of its points, and list its symmetries. It sorts points into groups by how they connect, singles out one point when the groups stop splitting, and tries every choice of that point. The new idea is a record of how the groups split at every step, like a receipt. When a branch produces a receipt that is already worse than the best receipt seen, the branch cannot give the standard numbering, so bliss stops it at once instead of going down to the end. Branches that give exactly the same final picture show a symmetry, which lets it skip more branches.

## The problem

The input is a simple undirected graph on $V = \{0, \ldots, n-1\}$ with an optional vertex coloring; bliss itself also handles directed graphs. The output is a canonical labeling $\lambda$, such that $\lambda(G)$ is the same colored graph for all graphs isomorphic to $G$, generators of $\mathrm{Aut}(G)$, and $|\mathrm{Aut}(G)|$.

## The algorithm

A partition is an array of the vertices cut into cells; a cell is named by its start position. REFINE takes a queue of splitter cells; for a splitter it counts the neighbors of each vertex in it, splits every touched cell by these counts in increasing order, and appends the new pieces to the queue: all of them if the split cell was waiting in the queue, otherwise all but the first largest. Its trace lists the splitters and the starts, counts and sizes of the pieces. The target cell is the first largest cell of size at least 2.

```pseudo id=main
BLISS(G, colors)
L1  π0 ← cells of equal color in color order; trace0 ← REFINE(G, π0, every cell); cert ← [trace0]
L2  push the root frame (π0, empty prefix, cert)
L3  while the stack is not empty do
L4      if cert of the top frame is worse than the best key and is not a prefix of the first key then pop it
L5      else if the top partition π is discrete then pop it; key ← cert + (colors and rows of λ(G))
L6          if no leaf is stored then store it as the first leaf and the best leaf
L7          else if key equals the first or the best key then record the automorphism between the two labelings
L8          else if key is larger than the best key then make it the best leaf
L9      else C ← the target cell of π, chosen once per frame
L10         take the next w in C not in the orbit of a tried w' under the found automorphisms fixing the prefix; if none, pop
L11         π' ← π with w individualized; t ← REFINE(G, π', [the cell of w]); push (π', prefix + w, cert + [t])
L12 |Aut| ← the product over the first path of the orbit sizes of its first child; return the best leaf, the automorphisms and |Aut|
```

The refinement after individualization starts from the singleton $\{w\}$ alone: the old partition was equitable, so only the new cell can split anything.

## Example

The cycle $C_6$, vertices $0, \ldots, 5$. The root refinement processes the single cell and splits nothing, trace $(-1)$; the entry $-1 - s$ marks the splitter that starts at $s$. Individualizing 0 gives the cells $\{0\}, \{1, \ldots, 5\}$, and refinement goes as follows.

| splitter (start) | cell split (start) | pieces: count, size | cells afterwards |
|---|---|---|---|
| $\{0\}$ (0) | $\{1, 2, 3, 4, 5\}$ (1) | 0: 3, 1: 2 | $\{0\}, \{2, 3, 4\}, \{1, 5\}$ |
| $\{1, 5\}$ (4) | $\{2, 3, 4\}$ (1) | 0: 1, 1: 2 | $\{0\}, \{3\}, \{2, 4\}, \{1, 5\}$ |
| $\{3\}$ (1) | none | | stable |

The trace is $(-1;\ 1, 0, 3;\ 1, 1, 2;\ -5;\ 1, 0, 1;\ 1, 1, 2;\ -2)$. The piece $\{2, 3, 4\}$ of the first split is the largest, so it is not queued; $\{3\}$ enters the queue from the second split, and $\{2, 4\}$ does not. The search then runs like nauty's: individualizing 2 gives the first leaf, 4 gives an equal key and the reflection $(1\,5)(2\,4)$, the root child 1 gives the rotation and another reflection, and the remaining root children are in the orbit of 0. Seven refinements in all, three generators, and $|\mathrm{Aut}(C_6)| = 6 \cdot 2 = 12$.

On the Petersen graph this implementation does 21 refinements and finds $|\mathrm{Aut}| = 120$. With the first largest cell rule it does 83 refinements on the $4 \times 4$ rook's graph and 70 on the Shrikhande graph, against 43 and 21 for the first smallest rule of the [nauty](/nauty/) page; both get the right orders, 1152 and 192, and different canonical forms for these two strongly regular graphs. The choice of target cell matters, which is why bliss offers several rules.

## Correctness

The [full proof](proofs/correctness.md) follows the one for nauty, with the certificate added.

- **Invariance.** The splitter queue holds cell starts, cells are processed by start, pieces are ordered by count, and the piece kept out of the queue is the first largest. None of these depends on vertex names, and the trace records only these quantities. So renaming the graph renames the whole tree and keeps every certificate and key.
- **Certificate cut.** Every leaf below a node has a key that starts with the node's certificate. If the certificate is already smaller than the best key at the first place they differ, no leaf below can be the best.
- **Orbit cut.** An automorphism fixing the prefix maps one child's subtree onto another's with the same keys.
- **Group order.** Nodes whose certificate is a prefix of the first leaf's key are never cut by L4, so every child in the orbit of the first child reaches a leaf with the first key, which records an automorphism to it. The orbit sizes on the first path then multiply to $|\mathrm{Aut}(G)|$.

## Complexity

| case | time | space |
|---|---|---|
| one REFINE call | $O(m + n \log n)$ per splitter round in bliss; $O(n m)$ in this implementation | $O(n + m)$ |
| best case: the root refinement is discrete | $O(n m)$ here | $O(n + m)$ |
| worst case | $O(n! \cdot n m)$ | $O(n^2 + m)$ for the stack of partitions |

With the "all but the largest" rule each vertex is in a splitter $O(\log n)$ times along one refinement, so bliss refines in $O((n + m) \log n)$ time plus sorting, and it never scans untouched cells. As with nauty, the number of search nodes is the real cost: it is 1 for almost all graphs, small for most symmetric graphs met in practice, and exponential for the families of Neuen and Schweitzer (2018), on which every [individualization-refinement](/individualization-refinement/) algorithm fails.

## Properties

- **Exact.** Canonical form, generators and group order are exact.
- **Sparse.** Memory and refinement time grow with $n + m$, not $n^2$; bliss handles graphs with millions of vertices when they are not too symmetric in hard ways.
- **Certificates as node invariants.** The trace is a cheap and strong node invariant that comes for free from refinement.
- **Canonical only within one version and options.** The labeling depends on the target cell rule and other settings.

## Variants and improvements

- **Target cell rules.** bliss offers first, first smallest, first largest, and the first cell with the most non-trivial connections to other cells, smallest or largest among those.
- **Failure recording and conflict propagation** (Junttila and Kaski 2011) remember certificate prefixes that failed and stop refinement as soon as the trace departs from the best path.
- **Component recursion** (Junttila and Kaski 2011) searches the components of the remaining partition separately, which cuts the tree from a product to a sum on graphs that fall apart.
- **[nauty and Traces](/nauty/)** use the same framework with dense data structures (nauty) or breadth-first search and random automorphism finding (Traces).
- **saucy** computes automorphism groups only, without canonical forms, and is very fast on sparse graphs from circuit and SAT instances.

## When to use it

Use bliss for canonical forms or symmetries of large sparse graphs, for example symmetry breaking in SAT and constraint models, or deduplication of large structured graphs. For dense graphs and for generation of small graphs nauty is often faster; for very hard symmetric families Traces is often best. For approximate similarity, or when isomorphism of most pairs is excluded by [invariants](/isomorphism-invariant/), a [color refinement](/weisfeiler-leman/) hash filters cheaply before calling bliss.

## Pitfalls

- **Cutting the first path.** A node whose certificate equals a prefix of the first leaf's key must not be cut even if it is worse than the best key, or automorphisms that the group order needs are missed.
- **A trace that depends on names.** Recording vertex numbers in the trace, instead of starts, counts and sizes, makes certificates of isomorphic nodes differ.
- **Refining only from the new singleton when the parent was not equitable.** The shortcut in L11 is valid only because every node is equitable.
- **Expecting the same labeling as nauty.** Different tools, rules and versions give different canonical forms.
- **Recursion.** The tree can be $n - 1$ levels deep; this implementation uses an explicit stack.

## Implementations

## History

Tommi Junttila and Petteri Kaski presented bliss at ALENEX 2007, aiming at the large sparse graphs that come from SAT instances, where nauty's dense data structures were too slow. In 2011 they added failure recording, conflict propagation and component recursion. The program has since become a standard tool for symmetry detection in SAT solvers, constraint solvers and computer algebra systems.

## References
