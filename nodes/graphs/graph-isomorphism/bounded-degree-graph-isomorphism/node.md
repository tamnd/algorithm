---
tag: 0TXVBY
kind: problem
slug: bounded-degree-graph-isomorphism
name: Bounded-degree graph isomorphism
aliases:
- graph isomorphism of bounded valence graphs
area: graphs/graph-isomorphism
level: advanced
summary: Graph isomorphism restricted to graphs whose maximum degree is bounded by a constant.
model: word-ram
complexity:
  vars: {n: the number of vertices, d: the maximum degree}
  time: {worst: n^(O((log d)^(O(1))))}
prereqs: [graph-isomorphism-problem, graph-automorphism-group]
see_also: [luks-algorithm, babai-quasipolynomial-algorithm, cai-furer-immerman-construction, k-dimensional-weisfeiler-leman, tree-isomorphism, planar-graph-isomorphism, gi-completeness]
sources:
  - paper: doi:10.1016/0022-0000(82)90009-5
    title: Eugene M. Luks, Isomorphism of graphs of bounded valence can be tested in polynomial time, Journal of Computer and System Sciences 25(1), 42 to 65 (1982)
    locator: Sections 2 to 4 (the reduction to color automorphism problems for groups with composition factors of bounded size, and the polynomial bound)
  - paper: "László Babai, William M. Kantor and Eugene M. Luks, Computational complexity and the classification of finite simple groups, Proceedings of the 24th IEEE Symposium on Foundations of Computer Science (FOCS 1983), 162 to 171"
    locator: the sections on graph isomorphism (the bound n^(O(d / log d)) for degree d)
  - paper: "Martin Grohe, Daniel Neuen and Pascal Schweitzer, A faster isomorphism test for graphs of small degree, Proceedings of the 59th IEEE Symposium on Foundations of Computer Science (FOCS 2018), 89 to 100"
    locator: the main theorem (time n^(polylog(d)) for graphs of maximum degree d)
---

Bounded-degree graph isomorphism is the [graph isomorphism problem](/graph-isomorphism-problem/) for graphs in which every vertex has at most $d$ neighbors, for a constant $d$. Luks (1982) solved it in polynomial time, $n^{O(d)}$, with the first algorithm that used the structure of permutation groups in an essential way, and his method became the basis of all later progress on general graph isomorphism. The best known bound today is $n^{\mathrm{polylog}(d)}$ by Grohe, Neuen and Schweitzer (2018). The case is not easy for combinatorial methods: the [CFI graphs](/cai-furer-immerman-construction/) have degree 3 but defeat every fixed level of the [Weisfeiler-Leman hierarchy](/k-dimensional-weisfeiler-leman/).

## In plain words

Two networks are given, and every point has only a few links, say at most three. Are the networks the same up to renaming of the points? Few links might seem to make the question easy, and indeed there is a method that is always fast enough in theory. But that method does not just compare neighborhoods. It builds the networks up step by step around a starting link, and at each step it keeps track of all possible symmetries as a group, which stays small and well behaved because of the low number of links.

## Definition

**Isomorphism of graphs of maximum degree $d$ ($\mathrm{GI}_d$).**
- Input: simple undirected graphs $G$ and $H$ on $n$ vertices, with maximum degree at most $d$, where $d$ is a fixed constant.
- Output: whether there is a bijection $\varphi : V(G) \to V(H)$ with $uv \in E(G) \iff \varphi(u)\varphi(v) \in E(H)$.

Colored, directed and edge-labeled versions behave the same way. When $d$ is part of the input, one asks how the running time depends on both $n$ and $d$.

## Variants

- **Trivalent graphs**, with $d = 3$: the case Luks treated first in detail, where all groups that arise are 2-groups, which makes the algorithm simple.
- **Bounded color class size.** Colored graphs whose color classes have at most $b$ vertices; Babai and Luks also solved this case with group methods, and it is a building block of bounded-degree algorithms.
- **Canonical forms.** Babai and Luks (1983) gave canonical labeling in time $n^{O(d)}$ as well.
- **Hypergraphs of bounded rank** and other structures of bounded degree reduce to the graph case.
- **Bounded degree and bounded genus or treewidth.** For these, [k-WL](/k-dimensional-weisfeiler-leman/) with fixed $k$ already suffices, unlike for bounded degree alone.

## Examples

All values below were computed with the implementations on the pages of [color refinement](/weisfeiler-leman/), [k-WL](/k-dimensional-weisfeiler-leman/) and [nauty](/nauty/).

| pair, all 3-regular or of maximum degree 3 | vertices | isomorphic? | color refinement | 2-WL |
|---|---|---|---|---|
| $K_{3,3}$ and the triangular prism | 6 | no ($\lvert \mathrm{Aut} \rvert = 72$ and 12) | not distinguished | distinguished |
| CFI graphs over $K_4$ | 40 | no (192 automorphisms each) | not distinguished | not distinguished |

The prism has triangles and $K_{3,3}$ has none, but every vertex in both has degree 3, so color refinement learns nothing. In the CFI pair 3-WL is needed, and for CFI graphs over larger base graphs of degree 3 no fixed dimension is enough, while Luks's algorithm handles all of them in polynomial time.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| brute force over bijections | $O(n! \cdot n d)$ | try every map |
| [Luks](/luks-algorithm/) (1982) | $n^{O(d)}$ | fix an edge; grow the graph by distance; compute automorphism groups of the layers with the color automorphism algorithm for groups in $\Gamma_d$ |
| Galil, Hoffmann, Luks, Schnorr and Weber (1987), $d = 3$ | $O(n^3 \log n)$ | a refined version for trivalent graphs |
| Babai, Kantor and Luks (1983) | $n^{O(d / \log d)}$ | better bounds on primitive groups, using the classification of finite simple groups |
| Grohe, Neuen and Schweitzer (2018) | $n^{O((\log d)^c)}$ for a constant $c$ | Babai's techniques adapted to groups in $\Gamma_d$ |
| [Babai](/babai-quasipolynomial-algorithm/) (2016), general graphs | $\exp((\log n)^{O(1)})$ | quasipolynomial, independent of $d$ |
| individualization-refinement ([nauty](/nauty/), [bliss](/bliss/)) | exponential in the worst case, even for $d = 3$ | fast in practice |

Here $\Gamma_d$ is the class of groups all of whose composition factors are subgroups of the symmetric group $S_d$. The point of Luks's method is that the automorphism group of the part of the graph within distance $r$ of a fixed edge, restricted to the next layer, lies in $\Gamma_d$, and primitive groups in $\Gamma_d$ are small: for fixed $d$ their order is polynomial in the size of the set they act on.

## Bounds

- **Upper bounds.** $n^{O(d)}$ (Luks 1982), $n^{O(d / \log d)}$ (Babai, Kantor and Luks 1983), $n^{\mathrm{polylog}(d)}$ (Grohe, Neuen and Schweitzer 2018).
- **Not polynomial for growing $d$.** No algorithm is known that is polynomial in both $n$ and $d$; such an algorithm would solve general GI in polynomial time, since every graph has degree at most $n - 1$.
- **Lower bounds for restricted methods.** CFI graphs of degree 3 need $\Omega(n)$-dimensional Weisfeiler-Leman, and graphs of bounded degree also make individualization-refinement take exponential time (Neuen and Schweitzer 2018).
- **Hardness.** For unbounded $d$ the problem is [GI-complete](/gi-completeness/).

## Reductions

- **To color automorphism.** Luks reduces $\mathrm{GI}_d$ to finding the automorphisms, within a group from $\Gamma_d$, of a colored set, and solves that by divide and conquer along orbits and block systems.
- **Isomorphism to automorphism.** $G \cong H$ is decided by asking whether some automorphism of the disjoint union $G \cup H$, with connected $G$ and $H$, swaps the two components.
- **From colored to uncolored**, with gadgets that keep the degree bounded.
- **[Tree isomorphism](/tree-isomorphism/)** and [planar graph isomorphism](/planar-graph-isomorphism/) are other restrictions solved in polynomial or linear time, by different methods.

## Applications

- Isomorphism of chemical graphs, whose atoms have small valence.
- A theoretical foundation: Luks's group-theoretic divide and conquer is the main tool in Babai's quasipolynomial algorithm and in the algorithms for bounded color class size, hypergraphs and groups.
- Polynomial-time isomorphism for graph classes that reduce to bounded degree, and the study of the Weisfeiler-Leman hierarchy on such graphs.

## References
