---
tag: 0RHMYD
kind: concept
slug: tutte-polynomial
name: Tutte polynomial
aliases:
- dichromatic polynomial
area: graphs/coloring-and-cliques
level: research
summary: Two-variable graph polynomial that generalizes the chromatic and flow polynomials.
prereqs: [deletion-contraction, chromatic-polynomial, spanning-tree]
see_also: [potts-model, counting-spanning-trees, matrix-tree-theorem, matroid, counting-graph-colorings, ising-model, treewidth, approximate-counting]
sources:
  - paper: doi:10.4153/CJM-1954-010-9
    title: W. T. Tutte, A contribution to the theory of chromatic polynomials, Canadian Journal of Mathematics 6, 80 to 91 (1954)
    locator: the definition of the dichromate and its deletion-contraction recurrence
  - paper: doi:10.1017/S0305004100068936
    title: F. Jaeger, D. L. Vertigan and D. J. A. Welsh, On the computational complexity of the Jones and Tutte polynomials, Mathematical Proceedings of the Cambridge Philosophical Society 108(1), 35 to 53 (1990)
    locator: the main theorem (the points where evaluation is easy and #P-hardness everywhere else)
  - paper: "R. P. Stanley, Acyclic orientations of graphs, Discrete Mathematics 5, 171 to 178 (1973)"
    locator: the number of acyclic orientations as the chromatic polynomial at minus one
  - paper: "A. Björklund, T. Husfeldt, P. Kaski and M. Koivisto, Computing the Tutte polynomial in vertex-exponential time, Proceedings of the 49th IEEE Symposium on Foundations of Computer Science, 677 to 686 (2008)"
    locator: the main theorem (time exponential in the number of vertices)
---

The Tutte polynomial $T(G; x, y)$ is a polynomial in two variables attached to a graph $G$ that contains, as special evaluations, the [chromatic polynomial](/chromatic-polynomial/), the flow polynomial, the number of [spanning trees](/spanning-tree/), the number of acyclic orientations, the reliability polynomial, and the partition function of the [Potts model](/potts-model/). It is the most general graph invariant that obeys the [deletion-contraction](/deletion-contraction/) recurrence. Computing it is #P-hard at almost every point (Jaeger, Vertigan and Welsh 1990), and the best exact algorithms take time exponential in the number of vertices.

## In plain words

Many counting questions about a network, such as how many ways there are to color it, how many trees reach every point, or how many ways to direct its links without making a loop, can all be answered by the same trick. Pick a link, and split the count into the cases with the link removed and with its two ends merged into one point.

The Tutte polynomial is a single formula that records the result of this trick in full. Plug in different pairs of numbers and it answers each of these questions. The price is that computing it is as hard as the hardest of them.

## The idea

**Definition by subsets.** Let $G = (V, E)$ be a graph, possibly with loops and parallel edges. For $A \subseteq E$ let $k(A)$ be the number of connected components of $(V, A)$ and $r(A) = |V| - k(A)$ its rank. Then

$$T(G; x, y) = \sum_{A \subseteq E} (x - 1)^{r(E) - r(A)} (y - 1)^{|A| - r(A)}.$$

The first exponent counts how many components $A$ has beyond those of $G$, and the second counts the independent cycles of $A$. This form, a rescaling of Whitney's rank generating function, shows that $T$ depends only on the cycle [matroid](/matroid/) of $G$ and is defined for every matroid.

**Deletion-contraction.** Write $G - e$ for deletion and $G / e$ for contraction. Then

- $T(G) = T(G - e) + T(G / e)$ if $e$ is neither a bridge nor a loop;
- $T(G) = x\, T(G / e)$ if $e$ is a bridge;
- $T(G) = y\, T(G - e)$ if $e$ is a loop;
- $T(G) = 1$ if $G$ has no edges.

Splitting the subsets $A$ by whether they contain $e$ proves these rules. Tutte (1954) proved the converse that gives the polynomial its importance: any graph invariant $f$ that satisfies $f(G) = a f(G - e) + b f(G / e)$ for ordinary edges, is multiplicative over disjoint unions and one-point joins, and is given on bridges and loops, is an evaluation of $T$ after rescaling. This is the recipe theorem.

**Main evaluations.** For a connected graph with $n$ vertices and $m$ edges (in general replace the exponents using $k(E)$ components):

| evaluation | counts |
|---|---|
| $T(1, 1)$ | spanning trees |
| $T(2, 1)$ | spanning forests (acyclic edge subsets) |
| $T(1, 2)$ | connected spanning subgraphs |
| $T(2, 2) = 2^m$ | all edge subsets |
| $T(2, 0)$ | acyclic orientations (Stanley 1973) |
| $T(0, 2)$ | totally cyclic orientations |
| $(-1)^{n - k} \lambda^k\, T(1 - \lambda, 0)$ | proper $\lambda$-colorings, the chromatic polynomial $P(G; \lambda)$ |
| $(-1)^{m - n + k}\, T(0, 1 - \lambda)$ | nowhere-zero $\mathbb{Z}_\lambda$-flows, the flow polynomial |

In the table $k = k(E)$. On the hyperbola $(x - 1)(y - 1) = q$, the polynomial is, up to a simple factor, the partition function of the $q$-state Potts model of statistical physics; $q = 2$ is the [Ising model](/ising-model/).

**Duality.** For a connected plane graph $G$ with dual $G^*$, $T(G^*; x, y) = T(G; y, x)$. So colorings of a plane graph correspond to flows of its dual, which is how the [four color theorem](/four-color-theorem/) can be stated as a statement about nowhere-zero 4-flows.

## Examples

| graph | $T(G; x, y)$ |
|---|---|
| a bridge | $x$ |
| a loop | $y$ |
| two parallel edges | $x + y$ |
| triangle $K_3$ | $x^2 + x + y$ |
| 4-cycle $C_4$ | $x^3 + x^2 + x + y$ |
| $K_4$ | $x^3 + 3x^2 + 2x + 4xy + 2y + 3y^2 + y^3$ |

For the triangle, delete an edge to get a path of two bridges, $T = x^2$, and contract it to get two parallel edges, $T = x + y$; the sum is $x^2 + x + y$. In general the $n$-cycle has $T = x^{n-1} + \cdots + x + y$.

For $K_4$: $T(1, 1) = 16$ spanning trees, as Cayley's formula $4^{4-2}$ and the [matrix-tree theorem](/matrix-tree-theorem/) give; $T(2, 0) = 24 = 4!$ acyclic orientations, one for each linear order; $T(2, 2) = 64 = 2^6$; and $-\lambda\, T(1 - \lambda, 0) = \lambda(\lambda - 1)(\lambda - 2)(\lambda - 3)$, which is 24 at $\lambda = 4$. For $C_4$, the chromatic polynomial from $T$ gives $2, 18, 84$ at $\lambda = 2, 3, 4$. All of these values agree with direct counts over all colorings, all flows and the subset expansion.

## Where it is used

- **Counting colorings, trees and orientations.** One computation of $T$ answers all the counting questions in the table at once, and the recipe theorem tells which new invariants are evaluations of $T$. See [counting graph colorings](/counting-graph-colorings/) and [counting spanning trees](/counting-spanning-trees/).
- **Complexity map.** Jaeger, Vertigan and Welsh (1990) proved that evaluating $T$ at a point $(x, y)$ of the complex plane is #P-hard unless $(x - 1)(y - 1) = 1$, where $T$ is a simple power, or $(x, y)$ is one of $(1, 1)$, $(-1, -1)$, $(0, -1)$, $(-1, 0)$, $(i, -i)$, $(-i, i)$, $(j, j^2)$, $(j^2, j)$ with $j = e^{2\pi i/3}$, where it is polynomial. $T(1,1)$ is polynomial because of the matrix-tree theorem, and $T(-1, -1)$ is related to the bicycle space. Approximate evaluation has its own map, with fully polynomial randomized schemes in some regions, such as the ferromagnetic Ising model, and hardness of [approximate counting](/approximate-counting/) in others.
- **Exact algorithms.** Deletion-contraction with merging of isomorphic graphs runs in time exponential in $m$. Björklund, Husfeldt, Kaski and Koivisto (2008) computed $T$ in time $\exp(O(n))$, exponential only in the number of vertices. For graphs of bounded [treewidth](/treewidth/) it is computable in polynomial time.
- **Statistical physics.** The Fortuin-Kasteleyn random cluster model is $T$ in other coordinates; the Potts partition function and its phase transitions are studied through the zeros of $T$.
- **Knot theory.** For an alternating link, the Jones polynomial is an evaluation of the Tutte polynomial of an associated plane graph (Thistlethwaite 1987), which is why the Jones polynomial is #P-hard to compute.
- **Network reliability.** The probability that a network stays connected when each edge fails independently with probability $p$ is an evaluation of $T$ along the line $x = 1$.
- **Coding theory.** The weight enumerator of a linear code is the Tutte polynomial of its matroid, and the MacWilliams identity is matroid duality $T(M^*; x, y) = T(M; y, x)$.

## References
