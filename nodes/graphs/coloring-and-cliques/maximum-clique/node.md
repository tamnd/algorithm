---
tag: TGQNGH
kind: problem
slug: maximum-clique
name: Maximum clique problem
aliases:
- max clique
area: graphs/coloring-and-cliques
level: core
summary: Find a clique of largest size, or largest total weight in the weighted version.
prereqs: [clique, clique-number, np-complete]
see_also: [maximum-independent-set, clique-decision, maximal-clique-enumeration, bron-kerbosch, carraghan-pardalos-algorithm, tomita-maximum-clique, motzkin-straus-theorem, clique-inapproximability]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.3 (Vertex cover and Clique are NP-complete) and Appendix A1.2, problem GT19, Clique
  - paper: doi:10.1007/BF02392825
    title: Johan Håstad, Clique is hard to approximate within n^(1-ε), Acta Mathematica 182(1), 105 to 142 (1999)
    locator: the main theorem
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of Max Clique and Chromatic Number, Theory of Computing 3, 103 to 128 (2007)
    locator: the main theorem (no n^(1-ε)-approximation unless P = NP)
  - paper: doi:10.1016/0167-6377(90)90057-C
    title: Randy Carraghan and Panos M. Pardalos, An exact algorithm for the maximum clique problem, Operations Research Letters 9(6), 375 to 382 (1990)
    locator: the whole paper (branch and bound with the size bound)
  - paper: doi:10.1016/S0166-218X(01)00290-6
    title: Patric R. J. Östergård, A fast algorithm for the maximum clique problem, Discrete Applied Mathematics 120(1-3), 197 to 207 (2002)
    locator: the whole paper (the Cliquer algorithm with bounds from a reverse vertex order)
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapters 1, 2 and 6 (exact algorithms for independent set, which apply to the complement graph)
  - paper: "J. Nešetřil and S. Poljak, On the complexity of the subgraph problem, Commentationes Mathematicae Universitatis Carolinae 26(2), 415 to 419 (1985)"
    locator: the whole paper (k-clique by fast matrix multiplication)
  - paper: doi:10.1016/j.jcss.2006.04.007
    title: Jianer Chen, Xiuzhen Huang, Iyad A. Kanj and Ge Xia, Strong computational lower bounds via parameterized complexity, Journal of Computer and System Sciences 72(8), 1346 to 1367 (2006)
    locator: the lower bound for k-clique under the exponential time hypothesis
---

The maximum clique problem asks for a largest [clique](/clique/) of a graph: a largest set of vertices in which every two vertices are adjacent. Its value is the [clique number](/clique-number/) $\omega(G)$. It is NP-hard, it is the [maximum independent set problem](/maximum-independent-set/) on the [complement graph](/complement-graph/), and no polynomial-time algorithm approximates it within $n^{1-\varepsilon}$ unless $\mathrm{P} = \mathrm{NP}$. In practice, branch-and-bound algorithms with coloring bounds solve sparse instances with thousands of vertices.

## In plain words

In a social network, find the largest group of people who all know each other. Each person is a point, and each friendship is a line. You want the largest group of points where every pair has a line.

A group is easy to check: look at each pair. Finding the largest group is hard. The number of groups grows very fast with the number of people, and no known method avoids a search over a large part of them in the worst case. Good programs prune the search: they stop exploring a branch when it is sure that the branch cannot beat the best group found so far.

## Definition

**Input.** A finite simple undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$.

**Output.** A set $C \subseteq V$ such that

$$\forall u \ne v \in C: \{u, v\} \in E, \qquad |C| = \omega(G) = \max \{\, |D| : D \subseteq V \text{ is a clique} \,\}.$$

**Weighted version.** With weights $w : V \to \mathbb{R}_{\ge 0}$, find a clique of largest total weight $\sum_{v \in C} w(v)$.

## Variants

- **Decision.** Given $G$ and $k$, is $\omega(G) \ge k$? This is [clique decision](/clique-decision/), problem GT19 of Garey and Johnson.
- **Fixed size $k$.** For a constant $k$, test all $\binom{n}{k}$ sets in $O(n^k k^2)$ time. With $k$ as a parameter it is W[1]-complete; see [parameterized clique](/parameterized-clique/) and [clique W[1]-completeness](/clique-w1-completeness/). For $k = 3$ this is [triangle finding](/triangle-finding/).
- **Maximal clique.** One [maximal clique](/maximal-clique/) is easy to find. Listing all of them is [maximal clique enumeration](/maximal-clique-enumeration/).
- **Easy classes.** [Chordal graphs](/chordal-graph/) (scan a [perfect elimination ordering](/perfect-elimination-ordering/)), [perfect graphs](/perfect-graph/) (by the [Lovász theta function](/lovasz-theta-function/)), [planar graphs](/planar-graph/) (each clique has at most 4 vertices), and graphs of [degeneracy](/degeneracy/) $d$ (each clique lies in the closed later neighborhood of its first vertex in a degeneracy order, so the search is over sets of at most $d$ vertices).
- **Random graphs.** In $G(n, 1/2)$ the clique number is about $2 \log_2 n$ with high probability, but no known polynomial-time algorithm finds a clique of size $(1 + \varepsilon)\log_2 n$. The [planted clique](/planted-clique/) problem studies this gap.

## Examples

- **A small graph.** In the graph with edges $01, 02, 12, 13, 23, 34, 45$ (the example of the [maximal clique](/maximal-clique/) page), $\omega = 3$, with two maximum cliques $\{0, 1, 2\}$ and $\{1, 2, 3\}$.
- **Triangle-free graphs.** Each odd cycle $C_{2k+1}$ with $k \ge 2$, the Petersen graph and each bipartite graph with an edge have $\omega = 2$.
- **Complements of cycles.** $\omega(\overline{C_n}) = \alpha(C_n) = \lfloor n/2 \rfloor$: 2, 3, 3, 4 for $n = 5, 6, 7, 8$. The graph $\overline{C_7}$ has $\omega = 3$ and $\chi = 4$, so it is not [perfect](/perfect-graph/).
- **Complete multipartite graphs.** $K_{a_1, \ldots, a_r}$ with all $a_i \ge 1$ has $\omega = r$, and it has $\prod a_i$ maximum cliques.

## Known algorithms

- **Brute force.** Test all subsets, or all $k$-subsets for growing $k$: $O(2^n n^2)$.
- **Through independent set.** Run an exact [maximum independent set](/maximum-independent-set/) algorithm on $\overline{G}$, in $O(1.2109^n)$ time with Robson's algorithm; this is the best type of worst-case bound in $n$.
- **[Bron-Kerbosch](/bron-kerbosch/).** List all maximal cliques and keep the largest: $O(3^{n/3})$ in the worst case with pivoting.
- **[Carraghan-Pardalos](/carraghan-pardalos-algorithm/).** Branch and bound: extend the current clique by candidates, and prune when the clique size plus the number of candidates cannot beat the best clique found.
- **[Tomita's algorithms](/tomita-maximum-clique/) (MCQ, MCR, MCS).** Branch and bound with a greedy coloring of the candidates as the bound: a set colored with $c$ colors contains no clique of more than $c$ vertices. These and their descendants are among the fastest exact solvers in practice.
- **Östergård's Cliquer.** Process vertices in reverse order and keep, for each suffix of the order, the best clique size found, which gives a cheap and strong bound.
- **Matrix multiplication.** Nešetřil and Poljak find a $k$-clique for fixed $k$ divisible by 3 in $O(n^{\omega_{\mathrm{mm}} k/3})$ time, where $\omega_{\mathrm{mm}} < 2.372$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/).
- **Continuous form.** The [Motzkin-Straus theorem](/motzkin-straus-theorem/) writes $1 - 1/\omega$ as the maximum of a quadratic form over the simplex. This is the base of many local-search heuristics.

## Bounds

- **NP-hardness.** The decision version is NP-complete (Karp 1972; Garey and Johnson, Section 3.1.3). The proof reduces [vertex cover](/vertex-cover/), or [independent set](/maximum-independent-set/) through the complement.
- **Approximation.** For each $\varepsilon > 0$ there is no polynomial-time $n^{1-\varepsilon}$-approximation unless $\mathrm{NP} = \mathrm{ZPP}$ (Håstad 1999), and unless $\mathrm{P} = \mathrm{NP}$ (Zuckerman 2007). See [clique inapproximability](/clique-inapproximability/). The trivial algorithm that returns one vertex is an $n$-approximation, so the bound is almost tight.
- **Fine-grained.** Under the exponential time hypothesis there is no $f(k)\, n^{o(k)}$ algorithm for $k$-clique (Chen, Huang, Kanj and Xia 2006), and no $2^{o(n)}$ algorithm for maximum clique.

## Reductions

- **Independent set.** $C$ is a clique of $G$ if and only if $C$ is independent in $\overline{G}$. The reduction takes $O(n^2)$ time and keeps sizes, so it keeps exact and approximate solutions.
- **Vertex cover.** $C$ is a clique of $G$ if and only if $V \setminus C$ is a vertex cover of $\overline{G}$.
- **Coloring as a bound.** $\omega(G) \le \chi(G)$, because the vertices of a clique need distinct colors. Every heuristic coloring gives an upper bound, which is the base of Tomita's pruning.
- **Clique cover.** A clique cover of $G$ is a coloring of $\overline{G}$; the two are linked by $\alpha(G) \le \overline{\chi}(G)$, the [clique cover](/clique-cover/) number.

## Applications

- **Social and biological networks.** Dense groups of mutually linked nodes, such as communities, protein complexes and gene co-expression modules.
- **Pattern matching and vision.** Matching two structures is often a maximum clique in a compatibility graph (the association graph), as in [maximum common subgraph](/maximum-common-subgraph/) search.
- **Coding theory and combinatorics.** Many extremal questions, such as the largest code with a given distance, are clique problems in large structured graphs.
- **Lower bounds for coloring.** A large clique proves that a [coloring](/graph-coloring/) needs many colors, which lets an exact coloring solver stop early.

## References
