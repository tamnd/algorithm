---
tag: YDXTEM
kind: concept
slug: clique-number
name: Clique number
aliases:
- omega(G)
area: graphs/coloring-and-cliques
level: intro
summary: Size of a largest clique in a graph.
prereqs: [clique, independent-set, complement-graph]
see_also: [chromatic-number, independence-number, maximum-clique, clique-decision, turan-theorem, ramsey-theorem, motzkin-straus-theorem, perfect-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.5, Perfect graphs (ω(G) and χ(G) ≥ ω(G)), Section 7.1, Subgraphs (Turán's theorem), and Section 9.1, Ramsey's original theorems
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.1, Vertex colorings and upper bounds (ω(G) ≤ χ(G)), and Section 5.2, Structure of k-chromatic graphs (Turán's theorem)
  - book: isbn:9780470170205
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, third edition, Wiley, 2008
    locator: the Probabilistic Lens on Turán's theorem (the bound of Caro and Wei on the independence number), and Chapter 4, The second moment method (the clique number of the random graph)
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of Max Clique and Chromatic Number, Theory of Computing 3, 103 to 128 (2007)
    locator: the main theorem (no n^(1-ε)-approximation of the clique number unless P = NP)
  - paper: doi:10.1016/j.ic.2017.06.001
    title: Mingyu Xiao and Hiroshi Nagamochi, Exact algorithms for maximum independent set, Information and Computation 255, 126 to 146 (2017)
    locator: the main theorem (1.1996^n n^O(1) time and polynomial space)
---

The clique number $\omega(G)$ of a [graph](/graph/) $G$ is the number of vertices of a largest [clique](/clique/), a largest set of pairwise adjacent vertices. It equals the [independence number](/independence-number/) of the [complement graph](/complement-graph/), and it is a lower bound on the [chromatic number](/chromatic-number/). Computing it is NP-hard, and for each $\varepsilon > 0$ no polynomial algorithm approximates it within $n^{1 - \varepsilon}$ unless P = NP. In a [perfect graph](/perfect-graph/) it equals the chromatic number and is computable in polynomial time.

## In plain words

Look for the largest group of people in a network in which everyone knows everyone else. The size of that group is the clique number.

It tells you something about coloring: the people of such a group need one color each, so you need at least that many colors. But the number of colors can be much larger.

It is easy to check a group, and hard to find the largest one. No known method is fast on every network, and even a rough estimate is hard to get in general.

## The idea

Let $G = (V, E)$ be a finite simple undirected graph with $n$ vertices and $m$ edges.

$$\omega(G) = \max \{ |K| : K \subseteq V,\ \{u, v\} \in E \text{ for all distinct } u, v \in K \}.$$

So $\omega(G) = 0$ for the empty graph, $\omega(G) = 1$ when $n \ge 1$ and $m = 0$, and $\omega(G) \ge 2$ when $m \ge 1$.

**Basic relations.**

- $\omega(G) = \alpha(\overline G)$, because the cliques of $G$ are the independent sets of $\overline G$.
- $\omega(G) \le \chi(G)$, because a clique needs a different color for each vertex.
- $\omega(G) \le \Delta(G) + 1$, because a vertex of a clique $K$ is adjacent to the other $|K| - 1$ vertices of $K$.
- $\omega(G) \le d + 1$, where $d$ is the [degeneracy](/degeneracy/): in a smallest-last order, the first vertex of $K$ to be removed still has the other $|K| - 1$ vertices of $K$ as neighbors, so $|K| - 1 \le d$.

**A lower bound from the degrees (Caro and Wei, for the complement).**

$$\omega(G) \ge \sum_{v \in V} \frac{1}{n - \deg(v)}.$$

*Proof.* Order $V$ by a uniformly random permutation. Let $S$ be the set of vertices $v$ that come before each of their non-neighbors. Two vertices $u, v$ of $S$ are adjacent: if they were not, each would have to come before the other. So $S$ is a clique. The vertex $v$ and its $n - 1 - \deg(v)$ non-neighbors are $n - \deg(v)$ vertices, and $v$ is the first of them with probability $1/(n - \deg(v))$. By linearity of expectation, $\mathbb{E}|S| = \sum_v 1/(n - \deg(v))$, so some order gives a clique at least this large. $\square$

**An upper bound from the edges ([Turán's theorem](/turan-theorem/)).** If $\omega(G) \le r$, then $m \le (1 - 1/r)\, n^2 / 2$. Equivalently, a graph with more than $(1 - 1/r)\, n^2/2$ edges has a clique of size $r + 1$.

**Ramsey bounds.** By [Ramsey's theorem](/ramsey-theorem/), each graph on $n \ge 1$ vertices has $\omega(G) \ge \frac12 \log_2 n$ or $\alpha(G) \ge \frac12 \log_2 n$. In the random graph $G(n, 1/2)$, $\omega$ is close to $2 \log_2 n$ with high probability.

**A continuous formula.** By the [Motzkin-Straus theorem](/motzkin-straus-theorem/), $\max \{ x^{\mathsf T} A x : x \ge 0,\ \sum_i x_i = 1 \} = 1 - 1/\omega(G)$, where $A$ is the [adjacency matrix](/adjacency-matrix/).

**Complexity.** Deciding $\omega(G) \ge k$ is the NP-complete [clique decision problem](/clique-decision/). It is W[1]-complete when parameterized by $k$ ([parameterized clique](/parameterized-clique/)). The exact value is the [maximum clique](/maximum-clique/) problem, solved in practice by branch and bound ([Carraghan-Pardalos](/carraghan-pardalos-algorithm/), [Tomita](/tomita-maximum-clique/)) and in theory in $O^*(1.1996^n)$ time and polynomial space by the algorithm of Xiao and Nagamochi (2017) for [maximum independent set](/maximum-independent-set/), run on the complement. No polynomial algorithm achieves the ratio $n^{1-\varepsilon}$ unless P = NP (see [clique inapproximability](/clique-inapproximability/)). On perfect graphs, $\omega(G)$ equals the [Lovász theta function](/lovasz-theta-function/) of the complement and is computable in polynomial time.

## Examples

| graph | $n$ | $m$ | $\omega$ | $\chi$ | a largest clique |
|---|---|---|---|---|---|
| empty graph | 0 | 0 | 0 | 0 | $\emptyset$ |
| path $P_4$ | 4 | 3 | 2 | 2 | an edge |
| cycle $C_5$ | 5 | 5 | 2 | 3 | an edge |
| $K_5$ | 5 | 10 | 5 | 5 | all vertices |
| $K_{3,3,3}$ | 9 | 27 | 3 | 3 | one vertex from each part |
| Petersen graph | 10 | 15 | 2 | 3 | an edge |
| Grötzsch graph | 11 | 20 | 2 | 4 | an edge |

**A worked case.** Take the graph on $0, \ldots, 6$ with the edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 06, 56$ (the example of the [clique](/clique/) page). Its degrees are $3, 3, 4, 4, 3, 3, 2$, so the Caro-Wei bound is

$$\frac14 + \frac14 + \frac13 + \frac13 + \frac14 + \frac14 + \frac15 = \frac{28}{15} \approx 1.87,$$

so $\omega \ge 2$. The true value is 3, for example $\{1, 2, 3\}$. There is no 4-clique. A 4-clique would contain a triangle and a fourth vertex adjacent to all of it. The graph has exactly 4 triangles, $\{0,1,2\}$, $\{1,2,3\}$, $\{2,3,4\}$ and $\{3,4,5\}$, and no vertex outside a triangle is adjacent to all three of its vertices. Its chromatic number is also 3.

**Turán check.** $K_5$ minus one edge has $n = 5$, $m = 9$. Turán's bound for $r = 3$ is $(1 - 1/3) \cdot 25 / 2 = 8.33$, and $9 > 8.33$, so it must contain a $K_4$. It does: the 4 vertices other than one end of the missing edge.

## Where it is used

- Lower bounds for [graph coloring](/graph-coloring/): branch-and-bound coloring algorithms start from a large clique, whose vertices get fixed distinct colors.
- [Perfect graphs](/perfect-graph/) are defined by $\chi(H) = \omega(H)$ for every induced subgraph $H$; in [chordal graphs](/chordal-graph-coloring/) both are found in linear time.
- Social and biological network analysis looks for large cliques as tightly knit groups; see [clique percolation](/clique-percolation-method/).
- Fine-grained complexity uses $k$-clique as a base problem ([parameterized clique](/parameterized-clique/)).
- Extremal graph theory: [Turán's theorem](/turan-theorem/) and [Ramsey's theorem](/ramsey-theorem/) are statements about $\omega$.

## References
