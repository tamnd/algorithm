---
tag: TAAD69
kind: problem
slug: clique-decision
name: Clique decision problem
aliases:
- k-clique problem
area: graphs/coloring-and-cliques
level: core
summary: Decide whether a graph contains a clique of size k; NP-complete.
prereqs: [clique, clique-number, np-complete]
see_also: [maximum-clique, clique-problem, independent-set, vertex-cover, parameterized-clique, clique-w1-completeness, clique-inapproximability, bron-kerbosch]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum (1972), 85 to 103
    locator: the list of 21 problems (Clique, reduced from SAT)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.3 (Vertex cover, Independent set and Clique are NP-complete) and Appendix A1.2, problem GT19, Clique
  - paper: doi:10.1137/0206038
    title: Robert Endre Tarjan and Anthony E. Trojanowski, Finding a maximum independent set, SIAM Journal on Computing 6(3), 537 to 546 (1977)
    locator: the O(2^(n/3)) algorithm for maximum independent set
  - paper: doi:10.1016/j.jcss.2006.04.007
    title: Jianer Chen, Xiuzhen Huang, Iyad A. Kanj and Ge Xia, Strong computational lower bounds via parameterized complexity, Journal of Computer and System Sciences 72(8), 1346 to 1362 (2006)
    locator: the theorem that k-Clique has no f(k) n^(o(k)) algorithm unless the exponential-time hypothesis fails
  - paper: doi:10.1007/BF02392825
    title: Johan Håstad, Clique is hard to approximate within n^(1-ε), Acta Mathematica 182(1), 105 to 142 (1999)
    locator: the main theorem
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of Max Clique and Chromatic Number, Theory of Computing 3, 103 to 128 (2007)
    locator: the main theorem (no n^(1-ε)-approximation of Max Clique unless P = NP)
  - url: https://dml.cz/dmlcz/106381
    title: Jaroslav Nešetřil and Svatopluk Poljak, On the complexity of the subgraph problem, Commentationes Mathematicae Universitatis Carolinae 26(2), 415 to 419 (1985)
    locator: the whole paper (k-clique detection by fast matrix multiplication)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13, Fixed-parameter intractability (Clique is W[1]-complete), and Chapter 14 (lower bounds under the exponential-time hypothesis)
---

The clique decision problem asks, for an undirected graph $G$ and an integer $k$, whether $G$ has a [clique](/clique/) of $k$ vertices, that is, $k$ vertices that are pairwise adjacent. Equivalently, it asks whether the [clique number](/clique-number/) $\omega(G)$ is at least $k$. It is one of Karp's 21 [NP-complete](/np-complete/) problems (1972). Trying all $k$-subsets takes $O(n^k k^2)$ time, which is polynomial for fixed $k$, but under the exponential-time hypothesis no algorithm runs in $f(k) \, n^{o(k)}$ time.

## In plain words

You have a group of people and you know who is friends with whom. You are given a number $k$. The question is whether there are $k$ people who are all friends with each other.

For a small $k$ you can check every group of $k$ people. The number of groups grows very fast with $k$, and no method is known that is fast for every $k$. Most experts think no such method exists.

A yes answer is easy to check: someone shows you the $k$ people, and you check each pair. This is what makes the problem a member of the class NP.

## Definition

Let $G = (V, E)$ be a finite simple undirected graph with $n = |V|$ and $m = |E|$. A set $K \subseteq V$ is a clique if $uv \in E$ for all distinct $u, v \in K$.

**CLIQUE.** Input: $G$ and an integer $k \ge 0$. Question: is there a clique $K \subseteq V$ with $|K| = k$?

A clique of size at least $k$ contains one of size exactly $k$, so the question is the same as "$\omega(G) \ge k$". The certificate is the set $K$, checked in $O(k^2)$ time with an adjacency matrix, so CLIQUE is in NP.

## Variants

- **Optimization.** Find a largest clique. See [maximum clique](/maximum-clique/). With a decision oracle, $\omega(G)$ is found by binary search over $k$, and a largest clique by deleting vertices whose removal keeps the answer yes.
- **Fixed $k$.** For each constant $k$ the problem is polynomial, by checking all $\binom{n}{k}$ subsets. For $k = 3$ it is triangle detection.
- **Parameterized by $k$.** [$k$-Clique](/parameterized-clique/) is W[1]-complete; it is the standard hard problem of the class W[1]. See [W[1]-completeness of clique](/clique-w1-completeness/).
- **Independent set and vertex cover.** $K$ is a clique of $G$ exactly when it is an [independent set](/independent-set/) of the [complement](/complement-graph/) $\overline G$, and exactly when $V \setminus K$ is a [vertex cover](/vertex-cover/) of $\overline G$.
- **Weighted clique.** Vertices carry weights and the question is whether some clique has total weight at least $k$.
- **Enumeration.** List all maximal cliques; see [Bron-Kerbosch](/bron-kerbosch/).

## Examples

Take the graph on vertices $0, \ldots, 6$ with the 11 edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 56, 06$. Its maximal cliques are $\{0,1,2\}$, $\{1,2,3\}$, $\{2,3,4\}$, $\{3,4,5\}$, $\{5,6\}$ and $\{0,6\}$.

- $(G, 3)$ is a yes instance, with certificate $\{1, 2, 3\}$: the pairs $12$, $13$, $23$ are edges.
- $(G, 4)$ is a no instance. Every clique lies in a maximal clique, and the largest maximal clique has 3 vertices.
- $(G, 0)$, $(G, 1)$ and $(G, 2)$ are yes instances for every graph with at least $k$ vertices and, for $k = 2$, at least one edge.

**Non-example of a certificate.** $\{0, 1, 2, 6\}$ is not a clique, since $16 \notin E$.

## Known algorithms

- **Brute force.** Test every $k$-subset: $O\big(\binom{n}{k} k^2\big)$ time.
- **Fast matrix multiplication.** For $k$ divisible by 3, build the graph whose vertices are the $k/3$-cliques of $G$ and find a triangle in it. This takes $O(n^{\omega_{\mathrm{mm}} k / 3})$ time, where $\omega_{\mathrm{mm}} < 2.372$ is the matrix multiplication exponent (Nešetřil and Poljak 1985).
- **Branch and bound.** [Bron-Kerbosch](/bron-kerbosch/) with pivoting lists all maximal cliques in $O(3^{n/3})$ time, the number of maximal cliques in the worst case. Branch and bound searches such as the [Carraghan-Pardalos algorithm](/carraghan-pardalos-algorithm/) and [Tomita's algorithm](/tomita-maximum-clique/) prune with coloring bounds and are fast in practice.
- **Exact exponential.** Maximum independent set in $\overline G$ solves the problem in $O(2^{n/3})$ time (Tarjan and Trojanowski 1977), and later algorithms improve the base.
- **Sparse graphs.** If $G$ has [degeneracy](/degeneracy/) $d$, every clique lies in $\{v\} \cup N^+(v)$ for its first vertex $v$ in a [degeneracy ordering](/degeneracy-ordering/), with $|N^+(v)| \le d$. So the problem is solved in $O(n \, 2^d \, d^2)$ time, and $k > d + 1$ is a no instance at once.

## Bounds

- **NP-completeness.** CLIQUE is NP-complete (Karp 1972; Garey and Johnson, problem GT19). So it has no polynomial algorithm unless P = NP.
- **Parameterized.** $k$-Clique is W[1]-complete, so it has no $f(k) \, n^{O(1)}$ algorithm unless FPT = W[1] (Cygan et al., Chapter 13).
- **Under the exponential-time hypothesis.** $k$-Clique has no $f(k) \, n^{o(k)}$ algorithm for any computable $f$ (Chen, Huang, Kanj and Xia 2006), so brute force is optimal up to the constant in the exponent. Also there is no $2^{o(n)}$ algorithm.
- **Approximation of $\omega$.** For every $\varepsilon > 0$, no polynomial algorithm approximates $\omega(G)$ within $n^{1 - \varepsilon}$ unless NP = ZPP (Håstad 1999), and unless P = NP (Zuckerman 2007). See [clique inapproximability](/clique-inapproximability/).

## Reductions

**From SAT.** Let $\varphi = C_1 \wedge \cdots \wedge C_q$ be a CNF formula. Make one vertex $(i, \ell)$ for each clause $C_i$ and each literal $\ell$ of $C_i$. Join $(i, \ell)$ and $(j, \ell')$ when $i \ne j$ and $\ell' \ne \lnot \ell$. Then $\varphi$ is satisfiable exactly when the graph has a clique of size $q$.

- If an assignment satisfies $\varphi$, pick one true literal in each clause. Two true literals are never complementary, so the $q$ picked vertices are pairwise adjacent.
- A clique of size $q$ has one vertex in each clause, since vertices of the same clause are not adjacent. Its literals contain no complementary pair, so setting them all true is consistent and satisfies every clause.

The graph has $\sum_i |C_i|$ vertices and is built in polynomial time.

*Example.* For $\varphi = (x \lor y) \wedge (\lnot x \lor y) \wedge (\lnot y \lor x)$, the graph has 6 vertices and 8 edges: of the 12 pairs in different clauses, the 4 complementary pairs are removed. The clique $(1, x)$, $(2, y)$, $(3, x)$ of size 3 gives the assignment $x = y = \text{true}$.

**To and from independent set and vertex cover.** $(G, k) \mapsto (\overline G, k)$ is a reduction from CLIQUE to INDEPENDENT SET, and $(G, k) \mapsto (\overline G, n - k)$ is one to VERTEX COVER. Both are reversible, so the three problems are equivalent under polynomial reductions. These maps take $O(n^2)$ time and do not preserve sparsity or the parameter.

**To SAT.** Variables $x_{v}$ for $v \in V$, the clause $\lnot x_u \lor \lnot x_v$ for each non-edge $uv$, and a cardinality constraint $\sum_v x_v \ge k$ encoded with a counter circuit.

## Applications

- **Bioinformatics.** Groups of proteins or genes that all interact, and alignment of structures by cliques in a product graph.
- **Social networks.** Groups in which everyone knows everyone else.
- **Chemistry and pattern matching.** A common substructure of two molecules or patterns is a clique in their modular product graph.
- **Coding theory.** A code with minimum distance $d$ is a clique in the graph that joins words at distance at least $d$.
- **Complexity theory.** CLIQUE is a standard source problem for NP-hardness, W[1]-hardness and fine-grained hardness reductions.

## References
