---
tag: TTB56H
kind: problem
slug: treewidth-computation
name: Computing treewidth
aliases:
- treewidth at most k
area: graphs/tree-algorithms
level: advanced
summary: Decide whether a graph has treewidth at most k; NP-hard in general, fixed-parameter tractable in k.
prereqs: [treewidth, tree-decomposition, np-complete]
see_also: [tree-decomposition-construction, treewidth, path-decomposition, fixed-parameter-tractable, chordal-graph, graph-minor-theorem, unique-games-conjecture, dp-on-tree-decompositions]
sources:
  - paper: Stefan Arnborg, Derek G. Corneil and Andrzej Proskurowski, Complexity of finding embeddings in a k-tree, SIAM Journal on Algebraic and Discrete Methods 8(2), 277 to 284 (1987)
    locator: the NP-completeness of deciding treewidth at most k when k is part of the input, and an algorithm in time O(n^(k+2)) for fixed k
  - paper: Hans L. Bodlaender, A linear-time algorithm for finding tree-decompositions of small treewidth, SIAM Journal on Computing 25(6), 1305 to 1317 (1996)
    locator: the exact algorithm, linear in n for each fixed k
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7 (Treewidth), the section on computing treewidth and its bibliographic notes on exact and approximate algorithms
  - paper: Uriel Feige, MohammadTaghi Hajiaghayi and James R. Lee, Improved approximation algorithms for minimum weight vertex separators, SIAM Journal on Computing 38(2), 629 to 657 (2008)
    locator: the polynomial-time approximation of treewidth within a factor O((log OPT)^(1/2))
---

Computing treewidth is the problem of finding the [treewidth](/treewidth/) of a graph, or, in its decision form, of deciding for a graph $G$ and a number $k$ whether $\mathrm{tw}(G) \le k$, usually together with a [tree decomposition](/tree-decomposition/) of width $k$ as a certificate. The decision form is [NP-complete](/np-complete/), but it is [fixed-parameter tractable](/fixed-parameter-tractable/): for each fixed $k$ it takes time linear in $n$. Because the algorithms that use treewidth run in time exponential in the width of the decomposition they are given, both the exact algorithms and the approximations that run in time $2^{O(k)} n$ matter in practice.

## In plain words

Treewidth says how close a graph is to a tree. Many hard problems become easy on graphs that are close to trees, but only if you are given the tree-like structure, the decomposition. So before solving the real problem, you must find that structure, and you want it as thin as you can get.

Finding the thinnest structure exactly is itself a hard problem when the target width can be anything. When the target width is a small fixed number, it can be done in time that grows only in step with the size of the graph, although the time grows very fast with the width. Faster methods give a structure that is at most a few times thicker than the best one.

## Definition

**Input.** A simple undirected graph $G = (V, E)$ with the vertices $0, \ldots, n-1$, not weighted, and an integer $k \ge 0$.

**Decision version.** Is $\mathrm{tw}(G) \le k$?

**Search version.** If $\mathrm{tw}(G) \le k$, output a tree decomposition of $G$ of width at most $k$; otherwise say no.

**Optimization version.** Output $\mathrm{tw}(G)$ and a tree decomposition of that width.

**Approximate version.** For a function $g$, output a decomposition of width at most $g(k)$, or correctly say that $\mathrm{tw}(G) > k$. With $g(k) = c \cdot k + O(1)$ this is a $c$-approximation.

## Variants

- **Parameterized.** The parameter is $k$; the question is the dependence of the running time on $k$ and on $n$.
- **Special graph classes.** On a [chordal graph](/chordal-graph/), the treewidth is the largest clique minus one, found in linear time from a perfect elimination order. Trees and forests have treewidth at most 1, and graphs with no $K_4$ minor at most 2, both recognized in linear time. On planar graphs, whether the problem is NP-hard is open; the related branchwidth is computable in polynomial time there, which gives a constant-factor approximation of treewidth.
- **Pathwidth.** The same questions for [path decompositions](/path-decomposition/); also NP-complete, and also linear time for each fixed $k$.
- **Weighted and other widths.** Vertex weights in the bag sizes, or the total state space of the bags in probabilistic inference, change the objective but not the hardness.

## Examples

| graph | $n$ | treewidth | reason |
|---|---|---|---|
| a single vertex | 1 | 0 | no edges |
| the tree with the edges $01, 02, 13, 14, 25, 46, 47$, a path, a star | any | 1 | forests with an edge |
| the strip of triangles $01, 02, 12, 13, 23, 24, 34, 35, 45$ | 6 | 2 | a path of bags of size 3; it has a triangle |
| a cycle $C_n$ | $n$ | 2 | not a forest; bags $\{0, i, i+1\}$ |
| $K_4$ | 4 | 3 | a clique of 4 |
| the $3 \times 3$ grid | 9 | 3 | computed by the exact program over subsets |
| the $4 \times 4$ grid | 16 | 4 | the same |
| the Petersen graph | 10 | 4 | the same |

So on the strip of triangles, the answer is no for $k = 1$ and yes for $k = 2$, with the certificate $\{0, 1, 2\}, \{1, 2, 3\}, \{2, 3, 4\}, \{3, 4, 5\}$.

## Known algorithms

| algorithm | output | time |
|---|---|---|
| Brute force over elimination orders ($O^*$ hides polynomial factors) | exact | $O^*(n!)$ |
| Dynamic programming over vertex subsets, by elimination orders | exact | $O^*(2^n)$ |
| Arnborg, Corneil and Proskurowski | exact, fixed $k$ | $O(n^{k+2})$ |
| [Balanced separators](/tree-decomposition-construction/), after Robertson and Seymour | width at most $4k + 4$ | $O(27^k k^2 n^2)$ as given here |
| Bodlaender | exact | $2^{O(k^3)} n$ |
| Bodlaender, Drange, Dregi, Fomin, Lokshtanov and Pilipczuk | width at most $5k + 4$ | $2^{O(k)} n$ |
| Korhonen | width at most $2k + 1$ | $2^{O(k)} n$ |
| Feige, Hajiaghayi and Lee | width $O(k (\log k)^{1/2})$ | polynomial |
| Greedy elimination: minimum degree, minimum fill-in | no guarantee | $O(n^2)$ to $O(n^3)$ |

The subset program uses $\mathrm{TW}(S) = \min_{v \in S} \max(\mathrm{TW}(S \setminus \{v\}), |Q(S \setminus \{v\}, v)|)$, where $Q(S, v)$ is the set of vertices outside $S \cup \{v\}$ that $v$ reaches through $S$: the later neighbours of $v$ in the filled graph when the vertices of $S$ are eliminated first. Then $\mathrm{tw}(G) = \mathrm{TW}(V)$. It is the oracle of the tests of the [construction algorithm](/tree-decomposition-construction/), and it gave the grid and Petersen values above.

## Bounds

- **NP-completeness.** Deciding $\mathrm{tw}(G) \le k$ with $k$ in the input is NP-complete (Arnborg, Corneil and Proskurowski). It is in NP because a decomposition with at most $n$ bags is a certificate that can be checked in polynomial time.
- **Fixed-parameter tractability.** For each fixed $k$, the decision takes $f(k) \cdot n$ time (Bodlaender). Even without that algorithm, the graphs of treewidth at most $k$ are closed under minors, so by the [graph minor theorem](/graph-minor-theorem/) they are characterized by finitely many forbidden minors, and the test takes polynomial time for each fixed $k$; this argument does not say what the forbidden minors are.
- **Approximation.** The best known polynomial-time approximation factor is $O((\log \mathrm{tw}(G))^{1/2})$. Under the small set expansion hypothesis, a hypothesis close to the [unique games conjecture](/unique-games-conjecture/), no polynomial-time algorithm achieves a constant factor.
- **Lower bound by cliques.** $\mathrm{tw}(G) \ge \omega(G) - 1$, and more generally the treewidth is at least the minimum degree of every subgraph, which gives quick lower bounds for exact searches.

## Reductions

- **To chordal completion.** $\mathrm{tw}(G) \le k$ if and only if $G$ is a subgraph of a [chordal graph](/chordal-graph/) on the same vertices with no clique of more than $k + 1$ vertices. So computing treewidth is minimizing the clique number of a chordal supergraph, which differs from minimizing the number of added edges, the [fill-in](/fill-in/).
- **To elimination orders.** Equivalently, find an order of $V$ that minimizes the largest number of later neighbours in the filled graph, as in [elimination ordering](/elimination-ordering/). The exact algorithms search over these orders.
- **From the search to the decision.** With an oracle for the decision version, a decomposition can be found by adding edges one at a time while the answer stays yes, until the graph becomes a chordal graph of clique number $k + 1$, whose cliques give the bags.
- **Use in other problems.** Many problems reduce to computing a decomposition first and then running a [dynamic program over it](/dp-on-tree-decompositions/), so the width found enters the exponent of the total running time.

## Applications

- **Fixed-parameter algorithms.** Every algorithm that runs in $f(k) \cdot n$ time given a decomposition of width $k$ needs one; with Bodlaender's or Korhonen's algorithm the whole pipeline is $f'(k) \cdot n$.
- **Probabilistic inference.** Exact inference in Bayesian networks and Markov random fields builds a [junction tree](/junction-tree/), which is a tree decomposition found by an elimination order; its width decides the cost.
- **Sparse matrices.** Fill-reducing orders for Cholesky factorization are elimination orders of the same kind.
- **Constraint satisfaction and databases.** Solving constraint networks and evaluating conjunctive queries are fast when the underlying graph has a decomposition of small width.

## References
