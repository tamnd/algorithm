---
tag: 8NFD2B
kind: algorithm
slug: weisfeiler-leman
name: Weisfeiler-Leman algorithm
aliases:
- 1-WL
- color refinement
- colour refinement
area: graphs/graph-isomorphism
level: core
summary: Refines vertex colors by multisets of neighbor colors until stable; a fast test that separates almost all non-isomorphic pairs but fails on regular graphs of equal degree.
solves: [graph-isomorphism-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n (n + m) log n), best: O(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [graph-isomorphism-definition, adjacency-list, equivalence-relation]
see_also: [partition-refinement, equitable-partition, k-dimensional-weisfeiler-leman, individualization-refinement, nauty, cai-furer-immerman-construction, tree-isomorphism, graph-isomorphism-problem]
sources:
  - paper: doi:10.1137/0209047
    title: László Babai, Paul Erdős and Stanley M. Selkow, Random graph isomorphism, SIAM Journal on Computing 9(3), 628 to 635 (1980)
    locator: the whole paper (a refinement by degrees canonically labels almost all graphs)
  - paper: doi:10.1007/978-1-4612-4478-3_5
    title: Neil Immerman and Eric Lander, Describing graphs, a first-order approach to graph canonization, in Complexity Theory Retrospective, Springer, 1990, 59 to 81
    locator: the whole chapter (color refinement and counting logic with two variables; trees are identified)
  - paper: doi:10.1007/s00224-016-9686-0
    title: Christoph Berkholz, Paul Bonsma and Martin Grohe, Tight lower and upper bounds for the complexity of canonical colour refinement, Theory of Computing Systems 60(4), 581 to 614 (2017)
    locator: the whole paper (O((n + m) log n) algorithm and a matching lower bound for partition-based methods)
  - book: isbn:9781107014527
    title: Martin Grohe, Descriptive Complexity, Canonisation, and Definable Graph Structure Theory, Cambridge University Press, 2017
    locator: Chapter 3, Section on the Weisfeiler-Leman algorithm (color refinement, its logical characterization and its limits)
  - paper: "Boris Weisfeiler and Andrei Leman, The reduction of a graph to canonical form and the algebra which appears therein, Nauchno-Technicheskaya Informatsia, Seriya 2, 9, 12 to 16 (1968)"
    locator: the whole paper (the original refinement, on pairs of vertices)
---

The Weisfeiler-Leman algorithm in dimension one, also called color refinement, gives every vertex a color and then repeats one step: the new color of a vertex is its old color together with the multiset of its neighbors' colors. When a step creates no new color, the coloring is stable. If two graphs, refined together, end with different numbers of vertices of some color, they are not isomorphic. If the counts agree, the test gives no answer: it fails on all pairs of regular graphs of the same degree and size, but it separates almost all graphs and all trees, and it is the first step of every practical isomorphism solver.

## In plain words

Paint every point of a network with the same color. Then give each point a new color that describes its old color and the colors of its neighbors, counted with repetition. Two points get the same new color only if their descriptions are equal. Repeat this until the number of colors stops growing. Do the same to a second network with the same rules, so that the colors mean the same thing in both. If the two networks end with different numbers of points of some color, they cannot be the same network with the points renamed. If the numbers agree, they may or may not be the same, and you need a stronger method to decide.

## The problem

The input is one graph $G = (V, E)$, or two graphs $G$ and $H$ with the same number $n$ of vertices. Graphs are undirected and simple, with an optional initial vertex coloring $c_0 : V \to \mathbb{N}$; edges are unlabeled. The output of the refinement is the stable coloring $c_\infty$, which is the coarsest [equitable partition](/equitable-partition/) that refines $c_0$. The isomorphism test answers "not isomorphic" or "possibly isomorphic". Directed graphs and edge labels need the variant below, which uses in-neighbors, out-neighbors and labels in the signature.

## The algorithm

Colors are small integers. The signature of $v$ in round $i$ is the pair of its color and the sorted list of its neighbors' colors; the new color is the rank of the signature among all signatures in the round.

```pseudo id=main
COLOR-REFINEMENT(G, c0)
L1  c ← c0, with its values replaced by their ranks 0, 1, 2, ...
L2  repeat
L3      for each v in V: sig(v) ← (c(v), the sorted list of c(w) over the neighbors w of v)
L4      c' ← the rank of sig(v) among the sorted distinct signatures, for each v
L5      if c' has as many distinct values as c then return c
L6      c ← c'

WL-TEST(G, H)
L7  c ← COLOR-REFINEMENT(G ⊎ H, the union of the initial colors)
L8  if the multiset of c over V(G) ≠ the multiset of c over V(H) then return "not isomorphic"
    else return "possibly isomorphic"
```

Line L7 refines the disjoint union, so a color means the same thing in both graphs. Since the signature contains the old color, $c'$ refines $c$, and equal numbers of colors in L5 mean equal partitions.

## Example

Take the graph on $\{0, \ldots, 5\}$ with edges $01, 12, 23, 34, 25, 35$: the path $0 - 1 - 2 - 3 - 4$ with vertex 5 joined to 2 and 3. All vertices start with color 0.

| round | signatures | colors of 0, 1, 2, 3, 4, 5 | number of colors |
|---|---|---|---|
| 0 | | 0, 0, 0, 0, 0, 0 | 1 |
| 1 | $(0, 0)$ for 0 and 4; $(0, 00)$ for 1 and 5; $(0, 000)$ for 2 and 3 | 0, 1, 2, 2, 0, 1 | 3 |
| 2 | 0: $(0, 1)$; 1: $(1, 02)$; 2: $(2, 112)$; 3: $(2, 012)$; 4: $(0, 2)$; 5: $(1, 22)$ | 0, 2, 5, 4, 1, 3 | 6 |
| 3 | all signatures distinct, as in round 2 | 0, 2, 5, 4, 1, 3 | 6 |

Round 1 is the degree partition. In round 2 vertex 1 (next to a leaf) and vertex 5 (next to two degree-3 vertices) split, and so do 2 and 3 and the leaves 0 and 4. Round 3 adds no color, so the algorithm stops after 2 refining rounds with a discrete coloring: every vertex has its own color. This graph is [asymmetric](/asymmetric-graph/), and color refinement alone identifies it.

**A failure.** For the 6-cycle and two disjoint triangles, both 2-regular, round 1 gives every vertex the signature $(0, 00)$, so the coloring is stable at once with one color and 6 vertices of it in each graph. The test answers "possibly isomorphic", but the graphs are not isomorphic. The same happens for the $4 \times 4$ rook's graph and the Shrikhande graph, which are 6-regular on 16 vertices.

## Correctness

Write $c_i$ for the coloring after $i$ rounds on the union $G \uplus H$. Three facts hold; the [full proof](proofs/correctness.md) gives the details.

- **Termination.** Each $c_{i+1}$ refines $c_i$, so the number of colors grows or the loop stops. It is at most $2n$, so there are at most $2n$ rounds.
- **Invariance.** For every isomorphism $\varphi : G \to H$ that keeps the initial colors, $c_i(\varphi(v)) = c_i(v)$ for all $i$ and $v$, by induction on $i$: $\varphi$ maps the neighbors of $v$ bijectively onto those of $\varphi(v)$, so the signatures are equal. Hence isomorphic graphs have equal color multisets, and the answer "not isomorphic" is always right.
- **Stability.** The returned coloring is equitable: two vertices of the same color have the same number of neighbors of each color. It is the coarsest equitable partition that refines $c_0$, so it does not depend on the order of the steps.

The converse fails: equal multisets do not imply isomorphism. Color refinement does not separate $G$ and $H$ exactly when they have a fractional isomorphism, a doubly stochastic matrix $X$ with $A_G X = X A_H$ (Tinhofer 1986; Ramana, Scheinerman and Ullman 1994), and exactly when they satisfy the same sentences of first-order logic with two variables and counting quantifiers (Immerman and Lander 1990).

## Complexity

| case | rounds | time as written |
|---|---|---|
| best: one round, for example a regular graph | 1 | $O(n + m)$ plus sorting |
| typical random graph | 2 or 3 | $O((n + m) \log n)$ |
| worst | up to $n - 1$ | $O(n (n + m) \log n)$ |

Each round sorts the neighbor lists and the signatures, in $O((n + m) \log n)$ time, or $O(n + m)$ with [radix sort](/radix-sort/). The number of rounds is at most $n - 1$ on one graph, and the path $P_n$ needs about $n / 2$ of them; Kiefer and McKay (2020) showed that $n - 1$ rounds are needed for infinitely many $n$. A smarter [partition refinement](/partition-refinement/) that processes only the smaller pieces of each split cell, in the style of [Hopcroft's minimization](/hopcroft-minimization/), computes the same stable partition in $O((n + m) \log n)$ time (Cardon and Crochemore 1982; Paige and Tarjan 1987). Berkholz, Bonsma and Grohe (2017) proved that this bound is tight for a natural class of refinement algorithms. Space is $O(n + m)$.

## Properties

- **Deterministic and canonical.** The color names depend only on the isomorphism type of the colored graph, so the stable coloring is an isomorphism invariant.
- **One-sided error.** "Not isomorphic" is always right. "Possibly isomorphic" can be wrong.
- **Strong on random graphs.** Babai, Erdős and Selkow (1980) proved that a refinement by degrees gives every vertex its own color in almost all graphs, so color refinement decides isomorphism and gives a canonical labeling for almost all graphs.
- **Identifies trees.** A tree and any graph not isomorphic to it get different color multisets (Immerman and Lander 1990), so color refinement decides [tree isomorphism](/tree-isomorphism/). It also identifies forests and other classes called amenable.
- **Blind to regularity.** On a $d$-regular graph the stable coloring has one color. So two $d$-regular graphs with the same number of vertices are never separated.
- **Iterative.** No recursion; the loop keeps two arrays of colors.

## Variants and improvements

- **Directed and edge-labeled graphs.** Put the multiset of out-neighbor colors, of in-neighbor colors, and of (edge label, neighbor color) pairs into the signature. The same proofs apply.
- **Hopcroft-style refinement.** Keep a queue of splitter cells and, when a cell splits, enqueue all new pieces except the largest; this is the $O((n + m) \log n)$ method of [partition refinement](/partition-refinement/).
- **[$k$-dimensional Weisfeiler-Leman](/k-dimensional-weisfeiler-leman/).** Color $k$-tuples of vertices instead of vertices. It is strictly stronger for each larger $k$, separates the rook's graph from the Shrikhande graph at $k = 3$, and is still incomplete for every fixed $k$ ([Cai, Fürer and Immerman](/cai-furer-immerman-construction/)).
- **[Individualization-refinement](/individualization-refinement/).** When the stable coloring is not discrete, give one vertex of a non-singleton cell a unique color and refine again, branching over the choices. This turns color refinement into a complete algorithm, used by [nauty](/nauty/) and [bliss](/bliss/).
- **Weisfeiler-Leman graph kernels and graph neural networks.** Counting colors per round gives a feature vector for machine learning. Message-passing neural networks separate no more pairs than color refinement (Xu, Hu, Leskovec and Jegelka 2019; Morris and others 2019).

## When to use it

Use it as the first test in any isomorphism or canonical labeling routine: it runs in near-linear time and decides most pairs that occur in practice. Use it to compute a vertex invariant for hashing graphs. Do not use it alone when inputs are regular, strongly regular, or built to be symmetric; then use [nauty](/nauty/), [bliss](/bliss/), or [VF2](/vf2-algorithm/), which add search on top of refinement.

## Pitfalls

- **Refining the graphs separately.** Color names from two separate runs are not comparable. Refine the disjoint union, or use canonical signatures with a shared dictionary.
- **Comparing only the number of colors.** Two graphs can have the same number of colors but different counts per color. Compare the full multisets.
- **Treating "possibly isomorphic" as "isomorphic".** Regular graphs of equal degree and size always pass the test.
- **Dropping the old color from the signature.** Then the new partition need not refine the old one, and the stopping test in L5 can stop too early or never.
- **Conventions for dimension.** Some papers call color refinement 1-WL and the 1968 algorithm on pairs 2-WL; others number from 1 for the pair version. The [k-dimensional page](/k-dimensional-weisfeiler-leman/) fixes one convention.
- **Hash collisions.** Implementations that replace signatures by hashes can merge different signatures. Use exact ranks, as here, or check collisions.

## Implementations

## History

Weisfeiler and Leman published in 1968 a refinement on ordered pairs of vertices, which is now called the 2-dimensional version. The vertex version is older folklore in chemistry: Morgan's 1965 algorithm for chemical structures uses the same idea of extended connectivity. Babai, Erdős and Selkow showed in 1980 that degree refinement works for almost all graphs. Cardon and Crochemore (1982) and Paige and Tarjan (1987) gave $O((n + m) \log n)$ refinement. Immerman and Lander (1990) linked the method to counting logic, and Cai, Fürer and Immerman (1992) showed its limits in every dimension. Since 2019 the algorithm has been the standard yardstick for the power of graph neural networks.

## References
