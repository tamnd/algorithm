---
tag: 1S3QJT
kind: problem
slug: maximum-independent-set
name: Maximum independent set problem
aliases:
- Independent set problem
- independent set problem
- k-independent set
- maximum stable set
- stable set
- vertex packing
area: graphs/coloring-and-cliques
level: core
summary: Find an independent set of largest size; equivalent to a maximum clique in the complement graph.
prereqs: [independent-set, independence-number, np-complete]
see_also: [maximum-clique, vertex-cover, maximal-independent-set, bipartite-maximum-independent-set, maximum-independent-set-in-trees, measure-and-conquer, branch-and-reduce, parameterized-independent-set]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.3 (Vertex cover, Clique and Independent set are NP-complete) and Appendix A1.2, problem GT20, Independent set
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 1 (a first branching algorithm for independent set), Chapter 2 (branching), Chapter 6 (measure and conquer for independent set)
  - paper: doi:10.1137/0206038
    title: Robert Endre Tarjan and Anthony E. Trojanowski, Finding a maximum independent set, SIAM Journal on Computing 6(3), 537 to 546 (1977)
    locator: the whole paper (an O(2^(n/3)) algorithm)
  - paper: doi:10.1016/0196-6774(86)90032-5
    title: J. M. Robson, Algorithms for maximum independent sets, Journal of Algorithms 7(3), 425 to 440 (1986)
    locator: the whole paper (O(2^(0.276 n)) time with exponential space)
  - paper: doi:10.1007/BF02392825
    title: Johan Håstad, Clique is hard to approximate within n^(1-ε), Acta Mathematica 182(1), 105 to 142 (1999)
    locator: the main theorem (no n^(1-ε) approximation unless NP = ZPP)
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of Max Clique and Chromatic Number, Theory of Computing 3, 103 to 128 (2007)
    locator: the main theorem (the same hardness unless P = NP)
---

The maximum independent set problem asks for a largest set of vertices of a graph with no edge inside it. Its value is the [independence number](/independence-number/) $\alpha(G)$. It is one of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/), it is the [maximum clique problem](/maximum-clique/) on the [complement graph](/complement-graph/), and its complement in $V$ is a minimum [vertex cover](/vertex-cover/). The best exact algorithms run in about $1.2^n$ time, and no polynomial-time algorithm approximates it within $n^{1-\varepsilon}$ unless $\mathrm{P} = \mathrm{NP}$.

## In plain words

You have a set of tasks, and some pairs of tasks conflict: they need the same machine at the same time, or they cannot both be chosen. You want to pick as many tasks as possible with no conflict between any two picked tasks. Draw a point for each task and a line for each conflict. You want the largest group of points with no line inside the group.

Checking a proposed group is easy. Finding the best group is hard: no known method is much faster than a clever search through many groups, and even a rough answer is hard to guarantee in general.

## Definition

**Input.** A finite simple undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$.

**Output.** A set $S \subseteq V$ such that

$$\forall u, v \in S: \{u, v\} \notin E, \qquad |S| = \alpha(G) = \max \{\, |T| : T \subseteq V \text{ independent} \,\}.$$

**Decision version.** Given $G$ and an integer $k$, decide whether $\alpha(G) \ge k$. This is problem GT20 of Garey and Johnson, and it is NP-complete.

## Variants

- **Weighted.** Each vertex has a weight $w(v) \ge 0$; maximize $w(S)$. The exact algorithms and the hardness carry over.
- **Maximal, not maximum.** Finding one [maximal independent set](/maximal-independent-set/) takes $O(n + m)$ time by a greedy pass. It is a different, easy problem.
- **Counting.** Counting the independent sets of a graph is #P-complete. In statistical physics this count is the partition function of the [hard-core model](/hard-core-model/) at fugacity 1.
- **Parameterized.** Deciding $\alpha(G) \ge k$ with $k$ as the parameter is W[1]-complete; see [parameterized independent set](/parameterized-independent-set/). The dual question, a vertex cover of size $n - k$, is [fixed-parameter tractable](/vertex-cover-branching/) in $n - k$.
- **Easy classes.** The problem is polynomial on [bipartite graphs](/bipartite-maximum-independent-set/) (by König's theorem, $\alpha = n - \nu$ where $\nu$ is the size of a maximum matching), on [trees](/maximum-independent-set-in-trees/) and graphs of bounded [treewidth](/treewidth/) (dynamic programming), on [chordal graphs](/chordal-graph/), on claw-free graphs, and on all [perfect graphs](/perfect-graph/) (by the [Lovász theta function](/lovasz-theta-function/) and the ellipsoid method).
- **Planar graphs.** It stays NP-hard, but [Baker's technique](/baker-planar-ptas/) gives a polynomial-time approximation scheme.

## Examples

- **Petersen graph.** $\alpha = 4$, for example $\{0, 2, 8, 9\}$ in the labels of the [independent set](/independent-set/) page.
- **Cycles and paths.** $\alpha(C_n) = \lfloor n/2 \rfloor$ and $\alpha(P_n) = \lceil n/2 \rceil$.
- **Complete and bipartite graphs.** $\alpha(K_n) = 1$ and $\alpha(K_{a,b}) = \max(a, b)$. The empty graph on no vertices has $\alpha = 0$.
- **Greedy is not enough.** In the star $K_{1,5}$, a greedy pass that takes the center first stops at $\{0\}$, while the leaves give $\alpha = 5$. Taking a vertex of smallest degree first, as in the [minimum-degree greedy](/greedy-independent-set/) rule, picks a leaf and finds the optimum here, but not on every graph.

## Known algorithms

- **Brute force.** Try all $2^n$ subsets and test each in $O(n^2)$ time: $O(2^n n^2)$.
- **Simple branching.** If every vertex has degree at most 2, the graph is a union of paths and cycles, and $\alpha$ is the sum of $\lceil k/2 \rceil$ over the paths and $\lfloor k/2 \rfloor$ over the cycles with $k$ vertices. Otherwise pick a vertex $v$ of degree at least 3. Either $v \notin S$, and we recurse on $G - v$, or $v \in S$, and we recurse on $G - N[v]$, which has at most $n - 4$ vertices. So $T(n) \le T(n - 1) + T(n - 4) + \mathrm{poly}(n)$, and $T(n) = O^*(\lambda^n)$ where $\lambda \approx 1.3803$ is the largest root of $x^4 = x^3 + 1$. This is the first example of Fomin and Kratsch.
- **Tarjan and Trojanowski (1977).** A careful case analysis gives $O(2^{n/3}) \approx O(1.2600^n)$ time with polynomial space.
- **Robson (1986).** $O(2^{0.276 n}) \approx O(1.2109^n)$ time, with exponential space for a table of small subgraphs.
- **Measure and conquer.** Fomin, Grandoni and Kratsch analyzed a short [branch-and-reduce](/branch-and-reduce/) algorithm with a weight on each vertex by its degree; see [measure and conquer](/measure-and-conquer/). Later work brought the bound with polynomial space below $1.2^n$.
- **Via cliques.** Any [maximum clique](/maximum-clique/) algorithm run on $\overline{G}$, such as [Tomita's algorithm](/tomita-maximum-clique/), solves it, at the cost of building the complement.

## Bounds

- **NP-hardness.** The decision version is NP-complete (Karp 1972; Garey and Johnson, Section 3.1.3).
- **Approximation.** For each $\varepsilon > 0$, no polynomial-time algorithm approximates $\alpha$ within $n^{1 - \varepsilon}$ unless $\mathrm{P} = \mathrm{NP}$ (Håstad 1999 under $\mathrm{NP} \ne \mathrm{ZPP}$, Zuckerman 2007 under $\mathrm{P} \ne \mathrm{NP}$). On graphs of maximum degree $\Delta$, a greedy set has at least $n / (\Delta + 1)$ vertices, so it is a $(\Delta + 1)$-approximation.
- **Exponential lower bound.** Under the exponential time hypothesis, no algorithm runs in $2^{o(n)}$ time, because the reduction from 3-SAT below maps a sparse formula with $N$ variables to a graph with $O(N)$ vertices after sparsification (Impagliazzo, Paturi and Zane).
- **Upper bound.** The best published bounds are below $1.2^n$, against the trivial $2^n$.

## Reductions

- **To and from clique.** $S$ is independent in $G$ if and only if $S$ is a clique in $\overline{G}$. Building $\overline{G}$ takes $O(n^2)$ time, so the two problems are equivalent. The reduction keeps the size of each solution, so it also keeps approximation ratios.
- **To and from vertex cover.** $S$ is independent if and only if $V \setminus S$ is a [vertex cover](/vertex-cover/). So $\alpha(G) = n - \beta(G)$. The optimal sets correspond, but approximation ratios do not: vertex cover has a [2-approximation](/vertex-cover-2-approximation/), while independent set has no $n^{1-\varepsilon}$-approximation.
- **From 3-SAT.** Given a formula with clauses $C_1, \ldots, C_q$, each with 3 literals, make a triangle for each clause, with one vertex for each literal. Join two vertices of different triangles when their literals are $x$ and $\neg x$. A set of one vertex per triangle with no edge picks a literal of each clause with no conflict, which extends to a satisfying assignment. Conversely, a satisfying assignment gives one true literal per clause, and two true literals are never complementary. So the formula is satisfiable if and only if $\alpha = q$. This is a [polynomial-time reduction](/polynomial-time-reduction/) from [3-SAT](/3-sat/).
- **To coloring.** The color classes of a coloring are independent sets, and [Lawler's algorithm](/lawler-chromatic-number/) for the chromatic number lists maximal independent sets.

## Applications

- **Scheduling and resource allocation.** Pick the most tasks that pairwise do not conflict.
- **Coding theory.** A code of length $\ell$ with minimum Hamming distance $d$ is an independent set in the graph on all words that joins words at distance less than $d$.
- **Map labeling and geometry.** Place the most labels that do not overlap; the conflict graph of the candidate positions is often an intersection graph.
- **Bioinformatics and data mining.** Pick non-redundant items, such as non-overlapping matches, and compute bounds in the clique formulations of the same data.

## References
