---
tag: 9RZ5Y5
kind: problem
slug: negative-triangle
name: Negative triangle
aliases:
- negative-weight triangle
area: complexity/fine-grained-complexity
level: advanced
summary: "Decide whether an edge-weighted graph on n vertices has a triangle of negative total weight. It is subcubic equivalent to APSP; a 2026 preprint gives O(n^2.9995) time."
prereqs: [all-pairs-shortest-paths, min-plus-matrix-multiplication]
see_also: [apsp-negative-triangle-equivalence, apsp-conjecture, zero-k-clique-hypothesis, min-weight-k-clique-hypothesis, triangle-detection-hypothesis, triangle-listing-by-degree, negative-cycle, fine-grained-equivalence-class]
sources:
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010, 645-654)"
    locator: the definition of negative triangle, its subcubic equivalence with APSP and the min-plus product, and the reduction from all-pairs negative triangle to detection; this page relies on the journal version
  - paper: "Liam Roditty and Virginia Vassilevska Williams, Minimum weight cycles and triangles: equivalences and algorithms, Proceedings of the 52nd IEEE Symposium on Foundations of Computer Science (FOCS 2011), 180-189"
    locator: the equivalence of minimum weight triangle and minimum weight cycle with APSP
  - paper: doi:10.1137/15M1024524
    title: "R. Ryan Williams, Faster all-pairs shortest paths via circuit complexity, SIAM Journal on Computing 47(5), 2018, 1965-1985 (conference version in STOC 2014)"
    locator: the main theorem (the min-plus product in n^3 / 2^(Omega(sqrt(log n))) time, randomized)
  - paper: doi:10.1145/3402926
    title: "Timothy M. Chan and R. Ryan Williams, Deterministic APSP, orthogonal vectors, and more: quickly derandomizing Razborov-Smolensky, ACM Transactions on Algorithms 17(1), 2021 (conference version in SODA 2016, 1246-1255)"
    locator: the deterministic form of the n^3 / 2^(Omega(sqrt(log n))) algorithm
  - paper: doi:10.1006/jcss.1997.1388
    title: "Noga Alon, Zvi Galil and Oded Margalit, On the exponent of the all pairs shortest path problem, Journal of Computer and System Sciences 54(2), 1997, 255-262"
    locator: the distance product of matrices with small integer entries by fast matrix multiplication
  - paper: doi:10.1137/09076619X
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Finding, minimizing, and counting weighted subgraphs, SIAM Journal on Computing 42(3), 2013, 831-854 (conference version in STOC 2009)"
    locator: the reductions to exact triangle and the search for minimum and maximum weight triangles
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: Theorem 2 (the min-plus product in deterministic time O(n^2.9995), and the real form in expected time O(n^2.998)) and Section 1.2 (negative triangle as the simplest problem of the APSP class); not yet refereed
  - paper: arxiv:2610.42012
    title: "Timothy M. Chan, Reina Itakura, Zhiyuan Ma and Yuancheng Yu, 3SUM made simpler (without matrix multiplication), k-SUM hypothesis refuted for odd k, and real 3SUM/APSP derandomized, arXiv preprint, October 2026"
    locator: Theorem 4.8 and Corollary 4.9 (deterministic real APSP in O(n^2.9997)); not yet refereed
---

Negative triangle asks whether a graph with integer edge weights has three vertices whose three edges have a negative total weight. It is the simplest problem in the class of problems that are subcubic equivalent to [all-pairs shortest paths](/all-pairs-shortest-paths/): Vassilevska Williams and Williams proved in 2010 that it has a truly subcubic algorithm if and only if APSP has one. So it is the usual starting point when a new problem is shown to be as hard as APSP.

The proof of the equivalence is on [APSP and negative triangle equivalence](/apsp-negative-triangle-equivalence/). The hypothesis is on [APSP conjecture](/apsp-conjecture/). This page is about the problem: its forms, its variants and the known bounds.

## In plain words

You have a map of towns and roads, and each road has a number on it, which can be negative. Is there a round trip through exactly three towns whose numbers add up to less than zero?

Checking every group of three towns works, but the number of groups grows like the cube of the number of towns. For a long time nobody could do much better. The question is important because it is exactly as hard as finding all cheapest routes between all pairs of towns: a fast method for one gives a fast method for the other.

## Definition

**Negative triangle**

- Instance: a graph $G = (V, E)$ with $n$ vertices, directed or undirected, and an integer weight $w(e) \in \{-M, \ldots, M\}$ for each edge, given as an $n \times n$ matrix with $\infty$ for a missing edge.
- Question: are there three distinct vertices $i$, $j$ and $k$ with edges $(i, j)$, $(j, k)$ and $(k, i)$ such that $w(i, j) + w(j, k) + w(k, i) < 0$?

**The model.** The measure is the time on the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits, as a function of $n$. The usual range is $M \le n^{c}$ for a constant $c$, so that every weight fits in $O(1)$ words. The input has $\Theta(n^2)$ entries, so the instance is dense; the size of the input is not the number of edges.

**The tripartite form.** The parts are $I$, $J$ and $K$ with $n$ vertices each, the edges go only between different parts, and the question asks for $i \in I$, $j \in J$ and $k \in K$ with a negative triangle. The two forms are equivalent with $O(n^2)$ extra time. From a general graph, take three copies of $V$ and copy the weight of $(u, v)$ to the edges from the copy of $u$ in one part to the copy of $v$ in the next part, in the cyclic order $I$, $J$, $K$. A triangle of the copy is then a directed cycle $u \to v \to x \to u$ of the graph, and its three vertices are distinct because the graph has no self-loops. An undirected graph is a directed graph with both directions of every edge.

The problem is also stated for real weights. Then the model is the [real RAM](/real-ram/) with exact addition, subtraction and comparison.

## Variants

- **Search.** Find a negative triangle. With a detector, halve each part and ask again on the 8 subgraphs; at most $8 \lceil \log_2 n \rceil$ calls find one. So search and decision are equivalent up to a log factor.
- **All-pairs negative triangle.** For every pair $(i, k)$, decide whether the edge $(k, i)$ lies on a negative triangle. It reduces to detection with $O(n^2 \log n)$ calls on graphs with $O(n^{1/3})$ vertices per part. This is the core of the equivalence proof.
- **Minimum weight triangle.** Find the least weight of a triangle. Subtracting a threshold $t$ from every edge between $K$ and $I$ in the tripartite form asks "is there a triangle of weight below $t$?", so binary search gives it with $O(\log M)$ calls to a detector. It is also equivalent to APSP (Roditty and Vassilevska Williams 2011), and it is the case $k = 3$ of the [min-weight k-clique hypothesis](/min-weight-k-clique-hypothesis/).
- **Exact triangle.** Decide whether some triangle has weight exactly 0. This is a different problem: APSP and 3SUM both reduce to it, and no reduction back to negative triangle is known. It is the case $k = 3$ of the [zero-k-clique hypothesis](/zero-k-clique-hypothesis/).
- **Unweighted triangle.** Without weights, the problem is triangle detection, which takes time $O(n^{\omega})$ with fast matrix multiplication. See [triangle detection hypothesis](/triangle-detection-hypothesis/).
- **Sparse graphs.** With $m$ edges, listing all triangles takes time $O(m^{3/2})$, for example by [listing by degree](/triangle-listing-by-degree/), and this also decides negative triangle. This is subcubic in $n$ only when $m = O(n^{2-\delta})$.

## Examples

**A directed graph.** Take the vertices $0, 1, 2, 3$ and the edges $0 \to 1$ of weight 2, $0 \to 2$ of weight 4, $1 \to 2$ of weight $-3$, $1 \to 3$ of weight 1, $2 \to 0$ of weight $-1$, $2 \to 3$ of weight 2 and $3 \to 0$ of weight $-2$. The directed triangles are $0 \to 1 \to 2 \to 0$ with weight $-2$, $0 \to 1 \to 3 \to 0$ with weight 1, and $0 \to 2 \to 3 \to 0$ with weight 4. The answer is yes. The same graph is the example of the [equivalence proof](/apsp-negative-triangle-equivalence/), where the min-plus product finds this triangle.

**Negative against exact.** Change the weight of $1 \to 2$ from $-3$ to $-1$. Now the three triangles weigh 0, 1 and 4. The answer to negative triangle is no, but the graph has a triangle of weight exactly 0, so the answer to exact triangle is yes.

**An undirected graph.** Take $K_4$ on $0, 1, 2, 3$ with $w(0,1) = 3$, $w(0,2) = -4$, $w(1,2) = 2$, $w(1,3) = -1$, $w(2,3) = -2$ and $w(0,3) = 5$. The four triangles weigh $\{0,1,2\}: 1$, $\{0,1,3\}: 7$, $\{0,2,3\}: -1$ and $\{1,2,3\}: -1$. The answer is yes, and the minimum weight triangle has weight $-1$. With the threshold $t = -1$, the question "is there a triangle of weight below $-1$?" has the answer no, which confirms the minimum.

## Known algorithms

All bounds are for $n$-vertex graphs and are unconditional.

- **Brute force.** Try all triples, in time $O(n^3)$ on the word RAM.
- **Through the min-plus product.** Compute $C = W \star W$, the [min-plus product](/min-plus-matrix-multiplication/), and test whether $C[i,k] + w(k, i) < 0$ for some pair. With the algorithm of Williams (STOC 2014, SIAM J. Comput. 2018), this takes time $n^3 / 2^{\Omega(\sqrt{\log n})}$, randomized; Chan and Williams (SODA 2016) made it deterministic.
- **Small weights.** The min-plus product with entries in $\{-M, \ldots, M\}$ takes time $\tilde{O}(M n^{\omega})$ (Alon, Galil and Margalit 1997), so negative triangle takes the same time. This is truly subcubic when $M \le n^{3 - \omega - \delta}$.
- **Sparse graphs.** Time $O(m^{3/2})$ by listing all triangles.
- **The 2026 preprint.** Alman and Vassilevska Williams (arXiv:2610.06783, not yet refereed) compute the min-plus product of matrices with entries bounded by a polynomial in $n$ in deterministic time $O(n^{2.9995})$. With the reduction above, negative triangle takes deterministic time $O(n^{2.9995})$, if the preprint is correct. For real weights, their algorithm takes expected time $O(n^{2.998})$, Las Vegas. Chan, Itakura, Ma and Yu (arXiv:2610.42012, not yet refereed) give deterministic real APSP in time $O(n^{2.9997})$, and the min-plus product reduces to APSP with real weights too.

## Bounds

- **Lower bound, unconditional.** Any algorithm must read $\Omega(n^2)$ entries in the worst case, so it needs time $\Omega(n^2)$. No better bound is known on the word RAM.
- **Lower bound, conditional on the APSP conjecture.** No $O(n^{3-\varepsilon})$ algorithm for any $\varepsilon > 0$. This bound is no longer useful if the 2026 preprint is correct, because the preprint refutes the APSP conjecture.
- **Upper bound.** $O(n^{2.9995})$, deterministic, from the 2026 preprint; before it, $n^3 / 2^{\Omega(\sqrt{\log n})}$.
- **The gap.** The true exponent is open: it is between 2 and $2.9995$.

## Reductions

- **APSP and the min-plus product.** Negative triangle reduces to one min-plus product with $O(n^2)$ extra work, and the min-plus product reduces to APSP on $3n$ vertices. In the other direction, the min-plus product reduces to all-pairs negative triangle with $O(\log M)$ calls, and all-pairs negative triangle reduces to detection with $O(n^2 \log n)$ calls on graphs with $O(n^{1/3})$ vertices per part. All these reductions are deterministic. See [APSP and negative triangle equivalence](/apsp-negative-triangle-equivalence/).
- **Minimum weight cycle.** Roditty and Vassilevska Williams (2011) show that minimum weight cycle in dense graphs is subcubic equivalent to minimum weight triangle, and so to negative triangle.
- **Exact triangle.** The min-plus product, and with it negative triangle, reduces to exact triangle (Vassilevska Williams and Williams 2013). Alman and Vassilevska Williams use this direction: their exact triangle algorithm, in time $O(n^{2.9983})$, gives the APSP bound.
- **To other APSP-equivalent problems.** Reductions from negative triangle show that metricity, the verification of a min-plus product, replacement paths, second shortest simple path, radius and betweenness centrality are as hard as APSP. See [fine-grained equivalence class](/fine-grained-equivalence-class/).

## Applications

- **A source for reductions.** It is a decision problem with a witness of three vertices, so it is easier to reduce from than APSP, which has $n^2$ outputs.
- **Short negative cycles.** In a graph with a [negative cycle](/negative-cycle/), a negative triangle is the shortest possible one in a simple graph. Testing for it is a special case of finding a short negative cycle.
- **A test case for new algorithms.** The 2026 algorithms come from new methods for triangle problems in sparse lopsided tripartite graphs, and the equivalence turns them into APSP algorithms.

## References
