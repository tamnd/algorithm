---
tag: BEFWMZ
kind: problem
slug: low-stretch-spanning-tree
name: Low-stretch spanning tree problem
aliases:
- low-stretch tree
area: graphs/spanning-trees
level: research
summary: Find a spanning tree where tree distances between endpoints of every edge are small on average.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Ω(n + m)}
prereqs: [spanning-tree, weighted-graph, shortest-path, fundamental-cycle, minimum-spanning-tree]
see_also: [fundamental-cycle, cycle-basis, low-diameter-decomposition, laplacian-matrix, electrical-flow, preconditioning, k-server-problem, shortest-path-tree]
sources:
  - paper: doi:10.1137/S0097539792224474
    title: "Noga Alon, Richard M. Karp, David Peleg and Douglas West, A graph-theoretic game and its application to the k-server problem, SIAM Journal on Computing 24(1) (1995), 78-100"
    locator: the whole paper (the definition of average stretch, the upper bound exp(O(sqrt(log n log log n))), the Omega(log n) lower bound, and the game between a tree player and an edge player)
  - url: https://arxiv.org/abs/cs/0411064
    title: "Michael Elkin, Yuval Emek, Daniel A. Spielman and Shang-Hua Teng, Lower-stretch spanning trees, SIAM Journal on Computing 38(2) (2008), 608-628 (STOC 2005); the arXiv version is cs/0411064"
    locator: the main theorem (average stretch O(log^2 n log log n) by star decompositions, in nearly linear time)
  - url: https://arxiv.org/abs/0808.2017
    title: "Ittai Abraham, Yair Bartal and Ofer Neiman, Nearly tight low stretch spanning trees, FOCS 2008"
    locator: the main theorem (average stretch O(log n log log n (log log log n)^3))
  - paper: doi:10.1137/17M1115575
    title: "Ittai Abraham and Ofer Neiman, Using petal-decompositions to build a low stretch spanning tree, SIAM Journal on Computing 48(2) (2019), 227-248 (STOC 2012)"
    locator: the main theorem (average stretch O(log n log log n) in O(m log n log log n) time)
  - paper: doi:10.1137/090771430
    title: "Daniel A. Spielman and Shang-Hua Teng, Nearly linear time algorithms for preconditioning and solving symmetric, diagonally dominant linear systems, SIAM Journal on Matrix Analysis and Applications 35(3) (2014), 835-885"
    locator: the sections on preconditioners built from low-stretch spanning trees
  - paper: doi:10.1137/S0895480192237403
    title: "Leizhen Cai and Derek G. Corneil, Tree spanners, SIAM Journal on Discrete Mathematics 8(3) (1995), 359-387"
    locator: the whole paper (the tree t-spanner problem, NP-complete for each fixed t > 1 on weighted graphs and for each fixed t >= 4 on unweighted graphs)
  - paper: doi:10.1016/j.cosrev.2009.08.001
    title: "Telikepalli Kavitha, Christian Liebchen, Kurt Mehlhorn, Dimitrios Michail, Romeo Rizzi, Torsten Ueckerdt and Katharina A. Zweig, Cycle bases in graphs: characterization, algorithms, complexity, and applications, Computer Science Review 3(4) (2009), 199-243"
    locator: the sections on fundamental cycle bases (the minimum fundamental cycle basis problem is NP-hard)
---

The low-stretch spanning tree problem asks, for a connected undirected graph with positive edge lengths, for a [spanning tree](/spanning-tree/) $T$ in which the edges of the graph are, on average, not stretched much. The *stretch* of an edge $(u, v)$ is the length of the path between $u$ and $v$ in $T$ divided by the length of the edge. A tree edge has stretch 1. A non-tree edge has the stretch of its [fundamental cycle](/fundamental-cycle/) minus itself. Finding the tree of least average stretch exactly is NP-hard, so the research question is how small an average stretch can be guaranteed. Alon, Karp, Peleg and West showed in 1995 that some graphs force $\Omega(\log n)$ and that every graph allows $\exp(O(\sqrt{\log n \log\log n}))$. A sequence of papers brought the upper bound down to $O(\log n \log\log n)$ (Abraham and Neiman). These trees are a key ingredient of the nearly linear time solvers for Laplacian linear systems.

## In plain words

You have a road network and you may keep only a tree of its roads, so that every town is still reachable but there is just one route between any two towns. Some roads are dropped. A driver who used a dropped road between two neighbouring towns must now take the detour through the tree. The stretch of that road is how many times longer the detour is than the road itself.

A cheapest tree is not the goal here. The goal is a tree in which detours are short for most roads, measured relative to each road's own length. One very long detour is acceptable if most roads keep short detours. The question is how short the average detour can be made in the worst network.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, and a length $\ell : E \to \mathbb{R}_{>0}$. Lengths may tie. Parallel edges are allowed.

**Stretch.** For a spanning tree $T$ of $G$ and an edge $e = (u, v) \in E$, let $d_T(u, v)$ be the length of the path from $u$ to $v$ in $T$. The stretch of $e$ is

$$\mathrm{str}_T(e) = \frac{d_T(u, v)}{\ell(e)}.$$

The *total stretch* is $\mathrm{st}_T(G) = \sum_{e \in E} \mathrm{str}_T(e)$ and the *average stretch* is $\mathrm{st}_T(G) / m$.

**Output.** A spanning tree $T$ that minimizes the total stretch. In the research literature the problem is usually the existence question: find a tree whose average stretch is at most some function $f(n)$, for every graph.

**Notes on the definition.**

- If $e \in T$, then $d_T(u, v) = \ell(e)$ and $\mathrm{str}_T(e) = 1$.
- The stretch can be less than 1. This happens when $e$ is not a [shortest path](/shortest-path/) between its ends, since the tree path may be shorter than $e$. Many papers first delete such edges or replace $\ell(e)$ by the distance $d_G(u, v)$, which makes every stretch at least 1.
- **Connectivity.** If $G$ is not connected, it has no spanning tree. The natural output is then a [spanning forest](/spanning-forest/), with one tree per component. Every edge lies inside a component, so the total stretch is the sum over the components, and the problem splits into one problem per component.
- **Ties.** Equal lengths change nothing in the definition. With ties, and in particular with unit lengths, many trees can be optimal.
- **Weighted average.** Some uses need $\sum_e c(e)\,\mathrm{str}_T(e) / \sum_e c(e)$ for given weights $c(e) \ge 0$. The known algorithms handle this version too, and it is the form that the game of Alon et al. needs (see Reductions).

## Variants

- **Maximum stretch: tree spanners.** Minimize $\max_e \mathrm{str}_T(e)$. A tree with maximum stretch at most $t$ is a tree $t$-spanner. Deciding whether one exists is NP-complete for each fixed $t > 1$ on weighted graphs, and for each fixed $t \ge 4$ on unweighted graphs (Cai and Corneil, 1995). On the cycle $C_n$ every spanning tree has maximum stretch $n - 1$, so the maximum can be forced to be large even when the average is below 2.
- **Stretch over all pairs.** Average $d_T(u, v) / d_G(u, v)$ over all pairs of vertices, not only edges. A related problem drops the division and minimizes $\sum_{u, v} d_T(u, v)$ over all pairs. That problem is the [minimum routing cost spanning tree](/minimum-routing-cost-spanning-tree/) problem.
- **Distributions over trees.** Find a probability distribution over spanning trees such that every edge has *expected* stretch at most $\alpha$. By the minimax theorem this is equivalent to the weighted-average version for every weighting $c$ (see Reductions). If the trees may use new vertices and edges and only have to dominate the distances of $G$, the best $\alpha$ is $\Theta(\log n)$ (Fakcharoenphol, Rao and Talwar). For spanning trees, that is, subgraphs of $G$, $\alpha = O(\log n)$ is open.
- **Directed and dynamic versions.** These exist in the literature but are outside the scope of this page.

## Examples

**The cycle.** Let $G = C_n$ with unit lengths. Every spanning tree is a path obtained by removing one edge. The $n - 1$ tree edges have stretch 1 and the removed edge has stretch $n - 1$. So every tree is optimal, with total stretch $2(n - 1)$ and average $2(n - 1)/n < 2$.

**The complete graph.** Let $G = K_n$ with unit lengths, and let $T$ be the star at any vertex. Tree edges have stretch 1 and every other edge has stretch 2. The total $(n - 1) + 2\left(\binom{n}{2} - (n - 1)\right)$ is the least possible, because a non-tree edge in a graph without parallel edges always has stretch at least 2.

**The standard graph with unit lengths.** Take the vertices $a$ to $f$ and the nine edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$, all of length 1. Here $n = 6$ and $m = 9$, so the lower bound of the last example is $5 + 2 \cdot 4 = 13$. A search over all 55 spanning trees shows that exactly four trees reach 13. They are $\{ab, bc, cd, de, df\}$, $\{ab, bc, cd, de, ef\}$, $\{ac, bc, cd, de, df\}$ and $\{ac, bc, cd, de, ef\}$. In each of them, every non-tree edge closes a triangle. This shows that ties produce several optima. The tree $\{ac, bc, bd, ce, ef\}$ has total stretch 16, because $de$ has stretch 3 and $df$ has stretch 4. The worst trees reach 19.

**The same graph with lengths.** Now give the edges the lengths $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. Here the [minimum spanning tree](/minimum-spanning-tree/) $T = \{ac, bc, bd, ce, ef\}$ happens to have the least total stretch, $803/84 \approx 9.56$. The stretches are:

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| tree path length | 4 | 3 | 1 | 2 | 3 | 5 | 8 | 10 | 2 |
| stretch | 1 | 1 | 1 | 1 | 3/4 | 1 | 8/7 | 5/3 | 1 |

The edge $cd$ has stretch $3/4 < 1$, because the path $c, b, d$ of length 3 is shorter than $cd$ itself.

**A minimum spanning tree can be bad.** In general, an MST is not a low-stretch tree. Let $G = K_n$ on the vertices $p_1, \dots, p_n$. Give the path edges $p_i p_{i+1}$ length 1 and every other edge length $1 + \varepsilon$. The unique MST is the path. The edge $p_i p_j$ then has stretch $(j - i)/(1 + \varepsilon)$, and the total stretch is $(n - 1) + \left(\binom{n+1}{3} - (n - 1)\right)/(1 + \varepsilon)$, so the average is about $(n + 1)/(3(1 + \varepsilon))$. The star at $p_1$ gives every edge stretch at most $2 + 2\varepsilon$. For $n = 20$ and $\varepsilon = 1/10$, the average stretch is $6.37$ for the path and $1.91$ for the star.

## Known algorithms

All of these work for arbitrary positive lengths and for the weighted average. Each takes a connected graph and is applied per component to a disconnected one.

| year | authors | average stretch | method |
|---|---|---|---|
| 1995 | Alon, Karp, Peleg and West | $\exp(O(\sqrt{\log n \log\log n}))$ | clustering by length classes |
| 2005/2008 | Elkin, Emek, Spielman and Teng | $O(\log^2 n \log\log n)$ | star decompositions |
| 2008 | Abraham, Bartal and Neiman | $O(\log n \log\log n\,(\log\log\log n)^3)$ | refined star decompositions |
| 2012/2019 | Abraham and Neiman | $O(\log n \log\log n)$ | petal decompositions, $O(m \log n \log\log n)$ time |

These algorithms are recursive. They cut the graph into pieces of smaller radius (a [low-diameter decomposition](/low-diameter-decomposition/)), connect the pieces with a few edges, and recurse on each piece. An edge is cut at some level with probability proportional to its length divided by that level's radius, and summing over the levels gives the bound. Simple trees such as a [shortest path tree](/shortest-path-tree/) found by [Dijkstra's algorithm](/dijkstra/) or [breadth-first search](/breadth-first-search/), or a minimum spanning tree, carry no such guarantee. The previous example shows the MST failing.

For the exact optimum, brute force over all spanning trees works on tiny graphs, as in the examples. No polynomial algorithm is known, and with unit lengths the problem is NP-hard (see Reductions).

## Bounds

- **Lower bound.** Some graphs force an average stretch of $\Omega(\log n)$ for every spanning tree. Alon et al. prove this for the $\sqrt{n} \times \sqrt{n}$ grid with unit lengths. So the $O(\log n \log\log n)$ bound is tight up to the $\log\log n$ factor. Whether $O(\log n)$ is always achievable is open.
- **A trivial lower bound.** With unit lengths and no parallel edges, every spanning tree has total stretch at least $(n - 1) + 2(m - n + 1)$. Equality holds exactly when every non-tree edge closes a triangle with the tree.
- **A trivial upper bound.** With unit lengths, each stretch is at most $n - 1$, so the average stretch is at most $n - 1$ for every tree.
- **Time.** Any algorithm that returns a spanning tree must read the graph, so $\Omega(n + m)$ time is needed. The best known guarantee comes with $O(m \log n \log\log n)$ time.

## Reductions

- **From the minimum fundamental cycle basis (NP-hardness).** With unit lengths, $\mathrm{str}_T(e) = |C_T(e)| - 1$ for a non-tree edge $e$, where $C_T(e)$ is its fundamental cycle. So

$$\mathrm{st}_T(G) = (n - 1) + \sum_{e \notin T} \left(|C_T(e)| - 1\right) = \sum_{e \notin T} |C_T(e)| + 2(n - 1) - m.$$

The last two terms do not depend on $T$. So a tree of least total stretch is exactly a tree whose fundamental [cycle basis](/cycle-basis/) has the least total length, and that problem is NP-hard (see the survey of Kavitha et al.). This makes the exact low-stretch problem NP-hard already with unit lengths.

- **The game of Alon, Karp, Peleg and West.** A tree player picks a spanning tree and an edge player picks an edge. The payoff is the stretch of the edge. By the minimax theorem, the following two statements are equivalent. First, for every weighting $c \ge 0$ of the edges, some spanning tree has $c$-weighted average stretch at most $\alpha$. Second, some distribution over spanning trees gives every edge expected stretch at most $\alpha$. So the algorithms for the weighted average give distributions over trees, and those distributions are what the online and approximation applications use.

## Applications

- **Laplacian solvers.** To solve $L x = b$ for the [Laplacian matrix](/laplacian-matrix/) $L$ of a graph, the solvers of Spielman and Teng [precondition](/preconditioning/) with a low-stretch spanning tree plus a few extra edges. The condition number of the preconditioned system is bounded by the total stretch, so a low-stretch tree keeps the number of iterations small. These solvers lead to the nearly linear time algorithms for [electrical flows](/electrical-flow/) and for approximate maximum flow.
- **The k-server problem.** Alon et al. built low-stretch trees for a randomized online algorithm for the [k-server problem](/k-server-problem/) on graphs. Their approach is to solve the problem on a random tree, which is easier, and to pay the expected stretch as a factor.
- **Approximation algorithms on graphs.** Problems that are easy on trees, such as some network design and routing problems, can be approximated on a graph by solving them on a random low-stretch tree. The approximation factor is the expected stretch.

## References
