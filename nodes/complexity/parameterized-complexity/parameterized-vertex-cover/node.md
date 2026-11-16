---
tag: 2702D3
kind: problem
slug: parameterized-vertex-cover
name: Parameterized vertex cover
aliases:
- vertex cover parameterized by solution size
area: complexity/parameterized-complexity
level: intro
summary: "Decide whether a graph has a vertex cover of size at most k, with k as the parameter. FPT in time O(1.2738^k + kn), with a kernel of 2k vertices."
prereqs: [vertex-cover, fixed-parameter-tractable]
see_also: [buss-kernel, vertex-cover-branching, crown-reduction, nemhauser-trotter-theorem, parameterized-independent-set, parameterized-hitting-set, vertex-cover-2-approximation, konig-theorem]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Section 2.2.1 (the O(k^2) kernel), Section 2.3.1 (the crown kernel), Section 3.1 (branching), Section 3.4 (vertex cover above LP), Chapter 14 (the ETH lower bound) and Chapter 15 (kernel lower bounds)
  - paper: doi:10.1137/0222038
    title: "Jonathan F. Buss and Judy Goldsmith, Nondeterminism within P, SIAM Journal on Computing 22(3), 560-572 (1993)"
    locator: the kernel with O(k^2) edges
  - paper: doi:10.1016/j.tcs.2010.06.026
    title: "Jianer Chen, Iyad A. Kanj and Ge Xia, Improved upper bounds for vertex cover, Theoretical Computer Science 411(40-42), 3736-3756 (2010)"
    locator: the main theorem, O(1.2738^k + kn) time and polynomial space
  - paper: doi:10.4230/LIPIcs.STACS.2024.40
    title: "David G. Harris and N. S. Narayanaswamy, A faster algorithm for vertex cover parameterized by solution size, 41st Symposium on Theoretical Aspects of Computer Science (STACS 2024), LIPIcs 289, 40:1-40:18"
    locator: the main theorem, time O*(1.25284^k)
  - paper: doi:10.1145/2629620
    title: "Holger Dell and Dieter van Melkebeek, Satisfiability allows no nontrivial sparsification unless the polynomial-time hierarchy collapses, Journal of the ACM 61(4), article 23 (2014)"
    locator: no kernel or compression of O(k^(2-e)) bits unless NP is a subset of coNP/poly
  - paper: doi:10.1006/jagm.2001.1186
    title: "Jianer Chen, Iyad A. Kanj and Weijia Jia, Vertex cover: further observations and further improvements, Journal of Algorithms 41(2), 280-301 (2001)"
    locator: the kernel with at most 2k vertices
---

Parameterized vertex cover is the [vertex cover](/vertex-cover/) problem in its decision form, with the size $k$ of the cover as the [parameter](/parameter/). The classical problem is NP-complete, but with this parameter it is [fixed-parameter tractable](/fixed-parameter-tractable/), and it is the standard first example of the field: a [search tree](/vertex-cover-branching/) solves it in time $O(2^k (n + m))$, the [Buss kernel](/buss-kernel/) shrinks every instance to $O(k^2)$ edges, and the best known algorithm runs in time $O^*(1.25284^k)$. This page gives only the parameterized view. The [vertex cover](/vertex-cover/) page has the optimization problem, its [2-approximation](/vertex-cover-2-approximation/) and the polynomial case of bipartite graphs.

## In plain words

You have a network of points joined by lines. You want to place guards on at most $k$ points so that every line has a guard on at least one end. The question is whether $k$ guards are enough.

For large networks the question is hard in general. But if $k$ is small, there is a fast method. Take any line with no guard yet. One of its two ends must get a guard, so try both. Each try uses one guard, so after $k$ steps you stop. This gives at most $2^k$ cases, and that number does not depend on the size of the network.

## Definition

The input is a graph $G = (V, E)$ given by adjacency lists, with $n = |V|$ and $m = |E|$, and a number $k$. A set $S \subseteq V$ is a *vertex cover* if every edge has at least one endpoint in $S$. The least size of a vertex cover is $\tau(G)$.

**p-VERTEX-COVER**

- Instance: a graph $G = (V, E)$ and an integer $k \ge 0$.
- Parameter: $k$.
- Question: does $G$ have a vertex cover $S$ with $|S| \le k$?

The size of the instance is $n + m$ plus the length of $k$. A yes-instance has a certificate of $k$ vertex names. If $k \ge n$ the answer is always yes, so we can assume $k < n$.

## Variants

- *Parameter $n - k$.* With the parameter $\ell = n - k$, the question is whether $G$ has an independent set of size at least $\ell$, because $S$ is a vertex cover exactly when $V \setminus S$ is independent. This is [p-Independent-Set](/parameterized-independent-set/), which is W[1]-complete.
- *Parameter above a lower bound.* Each cover has size at least the size $\mu$ of a [maximum matching](/maximum-matching/) and at least the value $\mathrm{LP}$ of the [LP relaxation](/lp-relaxation/). With the parameters $k - \mu$ or $k - \mathrm{LP}$ the problem is still FPT; Cygan et al. give a branching algorithm in time $O^*(4^{k - \mathrm{LP}})$ for the second one. These parameters are useful when $\tau(G)$ is large but close to the bound.
- *Structural parameters.* With the [treewidth](/treewidth/) $t$ of a given tree decomposition as the parameter, dynamic programming solves the problem in time $O^*(2^t)$. This parameterization has no polynomial kernel unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.
- *Planar graphs.* On [planar graphs](/planar-graph/) the problem is solvable in [subexponential parameterized](/subexponential-parameterized-algorithm/) time $2^{O(\sqrt{k})} n^{O(1)}$ by [bidimensionality](/bidimensionality-theory/).
- *Hypergraphs.* Vertex cover is the case $d = 2$ of [d-hitting set](/parameterized-hitting-set/), where every edge has $d$ vertices. The special cases of [hitting set](/hitting-set/) and [set cover](/set-cover/) with unbounded set sizes are W[2]-complete.

## Examples

Let $G$ be the path $P_6$ with vertices $1, \ldots, 6$. Then $\tau(P_6) = 3$, with the cover $\{2, 4, 6\}$. So $(P_6, 3)$ is a yes-instance and $(P_6, 2)$ is a no-instance: each vertex covers at most 2 of the 5 edges, and two vertices cover at most 4.

The Petersen graph has 10 vertices, 15 edges and degree 3 at each vertex, and $\tau = 6$. A count gives the lower bound 5, since 4 vertices cover at most 12 edges. The bound is not tight: the largest independent set has 4 vertices, so the least cover has $10 - 4 = 6$. So (Petersen, 6) is a yes-instance and (Petersen, 5) is a no-instance.

A worked kernel. Let $G$ be the star with center 0 and leaves $1, \ldots, 6$, plus the edges $\{1, 2\}$, $\{3, 4\}$, $\{7, 8\}$, $\{8, 9\}$, and let $k = 3$. Vertex 0 has degree 6, more than 3, so it is in every cover of size at most 3. The Buss rules remove it, lower $k$ to 2, and drop the isolated vertices 5 and 6. The rest has 4 edges, which is at most $k^2 = 4$, but 7 vertices, which is more than $k^2 + k = 6$. So $(G, 3)$ is a no-instance. Indeed, the rest needs 3 vertices, one for each of $\{1, 2\}$, $\{3, 4\}$ and the path $7, 8, 9$, so $\tau(G) = 4$.

## Known algorithms

Time bounds are for a RAM, with $O^*$ hiding factors polynomial in $n$.

- Brute force over all sets of $k$ vertices: $O(n^k (n + m))$ time. This is an [XP](/xp/) algorithm and not FPT.
- [Edge branching](/vertex-cover-branching/): branch on the two ends of an uncovered edge, in $O(2^k (n + m))$ time.
- Branching on a vertex of degree at least 3, after solving graphs of maximum degree 2 directly: $O^*(1.4656^k)$. See [bounded search tree](/bounded-search-tree/).
- [Buss kernel](/buss-kernel/) followed by edge branching: $O(n + m + 2^k k^2)$.
- Chen, Kanj and Xia (2010): $O(1.2738^k + kn)$ time and polynomial space, by branching rules for vertices of small degree and a careful analysis of the search tree.
- Harris and Narayanaswamy (STACS 2024): $O^*(1.25284^k)$, the best bound known at the time of writing.

Kernels:

- [Buss kernel](/buss-kernel/): at most $k^2$ edges and $k^2 + k$ vertices, in $O(n + m)$ time.
- [Crown reduction](/crown-reduction/): at most $3k$ vertices.
- [Nemhauser-Trotter](/nemhauser-trotter-theorem/) and [LP kernelization](/lp-kernelization/): at most $2k$ vertices (Chen, Kanj and Jia, 2001).

## Bounds

- The classical problem is NP-complete, so no algorithm runs in time polynomial in $n$ and $k$ unless P = NP.
- Under the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), there is no algorithm in time $2^{o(k)} n^{O(1)}$. With the sparsification lemma, the usual reduction maps a 3-CNF formula with $N$ variables to a graph with $O(N)$ vertices, so $k \le n = O(N)$, and a $2^{o(k)}$ algorithm would decide 3-SAT in time $2^{o(N)}$, against ETH. This bound is separate from W-hardness, which does not apply because the problem is FPT.
- No kernel and no compression has $O(k^{2 - \varepsilon})$ bits for a constant $\varepsilon > 0$ unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$ (Dell and van Melkebeek, 2014). So no kernel has $O(k^{2 - \varepsilon})$ edges under the same assumption. The kernels above have $O(k^2)$ bits, so their bit size is close to optimal.

## Reductions

- *To and from independent set.* $S$ is a vertex cover of $G$ exactly when $V \setminus S$ is an independent set. The map $(G, k) \mapsto (G, n - k)$ is a polynomial-time reduction to independent set, but it is not a [parameterized reduction](/parameterized-reduction/), because the new parameter $n - k$ is not bounded by a function of $k$. This is why vertex cover is FPT while independent set is W[1]-complete.
- *To clique.* $G$ has a vertex cover of size $k$ exactly when the [complement graph](/complement-graph/) has a clique of size $n - k$. Again the parameter is not kept.
- *To d-hitting set.* Each edge is a set of size 2, so p-Vertex-Cover is the case $d = 2$ of [p-Hitting-Set](/parameterized-hitting-set/) with sets of bounded size, with the same parameter.
- *Bipartite graphs.* By [König's theorem](/konig-theorem/), $\tau(G)$ equals the size of a maximum matching when $G$ is bipartite, so the problem is in P there.

## Applications

- *Conflict removal.* Build a graph with a vertex for each record and an edge for each pair of records that conflict. A vertex cover of size $k$ is a set of $k$ records whose removal leaves a consistent set. When few records are bad, $k$ is small and the FPT algorithms are fast.
- *Preprocessing for exact solvers.* Exact vertex cover and independent set solvers apply the kernel rules first. Vertex cover was the problem of the PACE 2019 implementation challenge, and the winning solvers combined reduction rules with branching.
- *Teaching and testing.* The problem is the usual first example of a kernel and a search tree, and many new techniques are tried on it first.

## References
