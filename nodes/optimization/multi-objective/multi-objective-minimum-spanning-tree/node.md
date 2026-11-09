---
tag: S1D2JF
kind: problem
slug: multi-objective-minimum-spanning-tree
name: Multi-objective minimum spanning tree
aliases:
- bicriteria spanning tree
- Pareto minimum spanning tree
- bi-objective minimum spanning tree
- multicriteria spanning tree
area: optimization/multi-objective
level: advanced
summary: Find all Pareto optimal spanning trees when each edge has several weights.
prereqs: [minimum-spanning-tree, kruskal, pareto-front]
see_also: [multi-objective-shortest-path, multi-objective-knapsack, spanning-tree-enumeration, approximate-pareto-set, weighted-sum-method, matroid, pareto-front-computation]
sources:
  - paper: doi:10.1007/BF02032304
    title: Horst W. Hamacher and Günter Ruhe, On spanning tree problems with multiple objectives, Annals of Operations Research 52(4), 1994
    locator: pages 209 to 230 (intractability, an exponential number of efficient trees, and an approximation of the efficient set)
  - paper: doi:10.1016/S0377-2217(97)00391-3
    title: R. M. Ramos, S. Alonso, J. Sicilia and C. González, The problem of the optimal biobjective spanning tree, European Journal of Operational Research 111(3), 1998
    locator: pages 617 to 628 (supported trees first, then branch and bound for the others)
  - paper: doi:10.1016/j.cor.2006.02.023
    title: Sarah Steiner and Tomasz Radzik, Computing all efficient solutions of the biobjective minimum spanning tree problem, Computers and Operations Research 35(1), 2008
    locator: pages 198 to 211 (a two-phase method with k-best spanning trees in the second phase)
  - paper: doi:10.1109/SFCS.2000.892068
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of Web sources, FOCS 2000
    locator: pages 86 to 92 (epsilon-approximate Pareto sets, and their construction when the exact version is pseudo-polynomial)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 9 (multicriteria spanning tree problems)
---

The multi-objective minimum spanning tree problem gives each edge of a connected graph $p \ge 2$ weights, such as building cost and failure risk, and asks for all [Pareto optimal](/pareto-optimality/) spanning trees. With one weight, [Kruskal's algorithm](/kruskal/) solves the [minimum spanning tree](/minimum-spanning-tree/) problem greedily. With two weights the greedy idea fails, the [Pareto front](/pareto-front/) can have exponentially many points (Hamacher and Ruhe, 1994), and deciding whether a tree within two bounds exists is NP-complete. The supported points are few and easy to find with weighted sums. The other points need enumeration, and in practice two-phase methods compute the whole front.

## In plain words

You must connect some towns with roads so that every town can reach every other town, using as few roads as possible. Each possible road has a building cost and a risk. One network beats another if it costs no more, has no more risk, and is better in one of the two. The task is to list all networks that no other network beats.

With one number per road, a simple rule works: take the cheapest roads first and skip a road that closes a loop. With two numbers, no such rule gives all good networks, and their number can grow very fast with the number of towns.

## Definition

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p$, and $y = f(x)$ is the image of $x$. Here $x$ is a spanning tree and $f(x)$ is its weight vector.

**Input.** A connected undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a weight vector $c(e) \in \mathbb{R}^p$ for each edge $e$.

**Feasible solutions.** The [spanning trees](/spanning-tree/) of $G$.

**Objectives.** $f_i(T) = \sum_{e \in T} c_i(e)$ for $i = 1, \ldots, p$.

**Output.** The nondominated set $Y_N$ of $\{f(T) : T \text{ a spanning tree}\}$, with one tree for each point. Unlike for paths, the sign of the weights does not matter: every spanning tree has $n - 1$ edges, so adding a constant to all weights of one objective moves all trees by the same amount.

## Variants

- **Bi-objective.** The case $p = 2$, the most studied one.
- **Weighted sum.** Minimize $\sum_i \lambda_i f_i(T)$: a minimum spanning tree with the edge weights $\sum_i \lambda_i c_i(e)$. It finds only supported points; see the [weighted sum method](/weighted-sum-method/).
- **Constrained spanning tree.** Minimize $f_1$ subject to $f_2(T) \le B$, one step of the [epsilon-constraint method](/epsilon-constraint-method/). It is NP-hard by the reduction below.
- **Bottleneck objectives.** An objective that is the largest weight in the tree, not the sum. Such objectives keep much of the greedy structure.
- **Matroid bases.** Spanning trees are the bases of the graphic [matroid](/matroid/). The same questions arise for the bases of any matroid with several weights.

## Examples

Take the vertices $1, 2, 3, 4$ and the edges with these weights:

| edge | $\{1, 2\}$ | $\{1, 3\}$ | $\{2, 3\}$ | $\{2, 4\}$ | $\{3, 4\}$ |
|---|---|---|---|---|---|
| weights | $(1, 6)$ | $(5, 1)$ | $(2, 3)$ | $(4, 2)$ | $(1, 5)$ |

The graph has eight spanning trees, with the weight vectors $(4, 14)$, $(6, 13)$, $(7, 11)$, $(7, 12)$, $(8, 9)$, $(10, 8)$, $(10, 9)$ and $(11, 6)$. The front is

$$Y_N = \{(4, 14),\ (6, 13),\ (7, 11),\ (8, 9),\ (10, 8),\ (11, 6)\}.$$

The lower left convex hull of these points passes through $(4, 14)$, $(8, 9)$ and $(11, 6)$. These three are the supported extreme points. The other three lie above the hull: the segment from $(4, 14)$ to $(8, 9)$ is at $11.5$ for $y_1 = 6$ and at $10.25$ for $y_1 = 7$, and the segment from $(8, 9)$ to $(11, 6)$ is at $7$ for $y_1 = 10$. So half of the front is out of reach for every weighted sum.

**Exponentially many points.** For $i = 0, \ldots, k - 1$, add a triangle on the vertices $v_i$, $v_{i+1}$ and $w_i$, with the weights $(2^i, 0)$ on $v_i v_{i+1}$, $(0, 2^i)$ on $v_i w_i$ and $(0, 0)$ on $w_i v_{i+1}$. The triangles share only the vertices $v_i$, so a spanning tree removes exactly one edge from each triangle. Removing the edge $w_i v_{i+1}$ keeps the weight $(2^i, 2^i)$ from that triangle, and removing $v_i w_i$ instead lowers $y_2$ by $2^i$, so such trees are dominated. The other trees remove $v_i v_{i+1}$ or $v_i w_i$ in each triangle, and have the weights $(\sigma, 2^k - 1 - \sigma)$, where $\sigma$ is any integer from $0$ to $2^k - 1$. These $2^k$ points lie on a line with negative slope, so none dominates another. So the graph with $n = 2k + 1$ vertices and $m = 3k$ edges has $|Y_N| = 2^k$.

## Known algorithms

**Supported points by weighted sums.** For $p = 2$, run Kruskal's algorithm with the weights $\lambda c_1(e) + (1 - \lambda) c_2(e)$. As $\lambda$ moves from $0$ to $1$, the order of the edges by weight changes only when two edges swap places, at most $m(m-1)/2$ times, and Kruskal's result depends only on the order. So there are at most $m(m-1)/2 + 1$ supported extreme points, and a dichotomic search finds all of them with $O(m^2)$ runs of Kruskal's algorithm. Each run with $\lambda$ strictly between $0$ and $1$ gives a Pareto optimal tree. At $\lambda = 0$ and $\lambda = 1$, break ties by the other weight.

**Two-phase methods.** Phase two looks for the unsupported points in each triangle between two neighboring supported points.

- Ramos, Alonso, Sicilia and González (1998) use branch and bound over the edges.
- Steiner and Radzik (2008) list spanning trees in order of the weighted sum for the normal of the triangle, with a k-best spanning tree algorithm, and stop when the weighted sum leaves the triangle.

**Enumeration.** For small graphs, list all spanning trees with a [spanning tree enumeration](/spanning-tree-enumeration/) algorithm and keep the nondominated ones by [Pareto front computation](/pareto-front-computation/). The number of trees can be $n^{n-2}$, so this works only for very small graphs.

**Approximation.** The exact version, "is there a spanning tree of weight exactly $B$?", has a pseudo-polynomial algorithm. By the theorem of Papadimitriou and Yannakakis (2000), an $\varepsilon$-approximate Pareto set of size polynomial in the input size and $1/\varepsilon$ can be computed in polynomial time for a fixed $p$ (see [approximate Pareto set](/approximate-pareto-set/)). Hamacher and Ruhe (1994) give a fast method that approximates the front by supported trees and their neighbors.

**No greedy rule.** For one objective, an edge can be judged alone by the cut and cycle rules. For two objectives, an edge can be in some Pareto optimal trees and not in others: in the example above, the edge $\{2, 4\}$ is in the trees of $(6, 13)$, $(7, 11)$, $(10, 8)$ and $(11, 6)$, but not in those of $(4, 14)$ and $(8, 9)$. So a rule that accepts or rejects each edge once gives one tree, not the front. Methods that build trees edge by edge must keep many partial trees and compare them.

## Bounds

- **Size of the front.** The triangle chain gives $|Y_N| = 2^k$ with $n = 2k + 1$ vertices, so $|Y_N| = 2^{\Omega(n)}$ in the worst case for $p = 2$.
- **Pseudo-polynomial size.** With integer weights in $\{0, \ldots, C\}$, the points of $Y_N$ have different values of $(y_1, \ldots, y_{p-1})$, each coordinate in $\{0, \ldots, (n-1) C\}$. So $|Y_N| \le ((n - 1) C + 1)^{p-1}$.
- **Supported points.** For $p = 2$ there are at most $m(m-1)/2 + 1$ supported extreme points, so they can all be found in polynomial time.
- **Hardness of one point.** Deciding whether a spanning tree $T$ has $f(T) \leqq b$ is NP-complete, by the reduction below.

## Reductions

- **From subset sum.** Given positive integers $a_1, \ldots, a_k$ and a target $t$, build the triangle chain with the weights $(a_i, 0)$, $(0, a_i)$ and $(0, 0)$ in triangle $i$. A spanning tree with $f(T) \leqq (t, \sum_i a_i - t)$ exists if and only if some subset of the $a_i$ sums to $t$. In one direction, take the edge with $(a_i, 0)$ for each $i$ in the subset and the edge with $(0, a_i)$ for the others. In the other direction, each triangle adds $a_i$ to at least one coordinate, so the two coordinates sum to at least $\sum_i a_i$, and the bound forces the sum of the $a_i$ counted in $y_1$ to be exactly $t$. So the problem is NP-hard via [subset sum](/subset-sum-problem/).
- **To the minimum spanning tree problem.** The weighted sum and the lexicographic version are minimum spanning tree problems with changed weights or a changed order of edges, solved by [Kruskal's](/kruskal/) or [Prim's](/prim/) algorithm.
- **From and to other combinatorial problems.** The triangle chain is the spanning tree form of the diamond chain for [multi-objective shortest path](/multi-objective-shortest-path/) and of the pairs of items for [multi-objective knapsack](/multi-objective-knapsack/). All three problems are intractable for the same reason.

## Applications

- **Network design.** Communication, power and water networks with cost and reliability, or cost and delay, as objectives.
- **Clustering.** Spanning trees with several distance measures between data points, cut into clusters.
- **Subproblems.** Bounds for multi-objective travelling salesman and network design problems, which use spanning trees as relaxations.

## References
