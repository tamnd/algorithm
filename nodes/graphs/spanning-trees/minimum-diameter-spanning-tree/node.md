---
tag: NX7H0P
kind: problem
slug: minimum-diameter-spanning-tree
name: Minimum diameter spanning tree problem
aliases:
- min-diameter spanning tree
area: graphs/spanning-trees
level: advanced
summary: Find a spanning tree whose longest path between any two vertices is as short as possible.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m n log n)}
prereqs: [spanning-tree, shortest-path-tree, eccentricity, tree-diameter]
see_also: [minimum-routing-cost-spanning-tree, minimum-spanning-tree, tree-center, all-pairs-shortest-paths, dijkstra, breadth-first-search, steiner-tree-problem, np-hard]
sources:
  - paper: doi:10.1016/0020-0190(94)00183-Y
    title: Refael Hassin and Arie Tamir, On the minimum diameter spanning tree problem, Information Processing Letters 53(2) (1995), 109-111
    locator: the whole paper (the reduction to the absolute 1-center and the shortest path tree from it)
  - paper: doi:10.1287/opre.12.3.450
    title: S. L. Hakimi, Optimum locations of switching centers and the absolute centers and medians of a graph, Operations Research 12(3) (1964), 450-459
    locator: the definition of the absolute center of a graph
  - paper: doi:10.1137/0137040
    title: O. Kariv and S. L. Hakimi, An algorithmic approach to network location problems. I, The p-centers, SIAM Journal on Applied Mathematics 37(3) (1979), 513-538
    locator: the algorithm for the absolute 1-center
  - paper: doi:10.1137/0220060
    title: Jan-Ming Ho, D. T. Lee, Chia-Hsiang Chang and C. K. Wong, Minimum diameter spanning trees and related problems, SIAM Journal on Computing 20(5) (1991), 987-997
    locator: the whole paper (the geometric version for points in the plane, with one or two centers)
---

The minimum diameter spanning tree problem asks for a [spanning tree](/spanning-tree/) of a weighted graph whose diameter, the longest distance between two vertices measured inside the tree, is as small as possible. Unlike many other spanning tree problems with a min-max objective, it is solvable in polynomial time. Hassin and Tamir showed that the optimum is a [shortest path tree](/shortest-path-tree/) grown from the *absolute center* of the graph, a point that may lie inside an edge, and that the optimal diameter is twice the absolute radius. The variant that adds a weight budget, or asks for a cheapest tree with a diameter bound, is [NP-hard](/np-hard/).

## In plain words

You must connect a set of sites with a tree of links, using only links from a given list. Each link has a length. Messages travel along the tree, and you care about the worst case: the longest trip between any two sites. You want to make this worst trip as short as possible.

The answer is to find the best place for a hub. The hub may sit at a site or part way along a link. Pick the place where the farthest site is as near as possible. Then connect every site to the hub by its shortest route. Any trip goes to the hub and back out, so it is at most twice the distance to the farthest site, and no tree can do better.

## Definition

**Input.** A finite connected undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and lengths $w(e) \ge 0$. Parallel edges and self-loops are allowed; a self-loop is never in a tree, and of parallel edges only the shortest matters.

**Output.** A spanning tree $T$ that minimizes

$$\operatorname{diam}(T) = \max_{u, v \in V} d_T(u, v),$$

where $d_T(u, v)$ is the total length of the path from $u$ to $v$ in $T$.

**Absolute center.** Think of each edge $uv$ as a segment of length $w(uv)$ whose inner points are possible locations. For a point $p$, let $e(p) = \max_{x \in V} d_G(p, x)$, the distance to the farthest vertex. The *absolute radius* is $r^\ast = \min_p e(p)$, and a point that attains it is an *absolute center*. It can be better than every vertex, the vertex [eccentricity](/eccentricity/) minimum.

**Theorem (Hassin and Tamir 1995).** The minimum diameter of a spanning tree is $2 r^\ast$, and a shortest path tree rooted at an absolute center attains it.

*Proof.* Let $T$ be any spanning tree, and let $p$ be the midpoint of a longest path of $T$, its [center](/tree-center/) as a point. Every vertex is within $\operatorname{diam}(T)/2$ of $p$ in $T$, and distances in $G$ are at most distances in $T$, so $r^\ast \le e(p) \le \operatorname{diam}(T) / 2$. Conversely, let $p$ be an absolute center on the edge $uv$, and let $T$ be a shortest path tree from $p$ in the graph with $p$ added as a vertex that splits $uv$. Each vertex has tree distance at most $r^\ast$ from $p$, so any two vertices are at most $2 r^\ast$ apart in $T$. If $T$ uses both halves of $uv$, joining them back gives the edge $uv$ with the same distances. If it uses only the half to $u$, drop $p$: all paths between vertices then avoid $p$, and their lengths do not grow. Either way the result is a spanning tree of $G$ with diameter at most $2 r^\ast$. $\square$

**Connectivity.** The graph must be [connected](/connected-graph/). For a disconnected graph one can ask for a spanning forest whose largest component diameter is least; the theorem then applies to each component on its own.

**Ties.** Lengths may tie. The optimal value $2 r^\ast$ is unique, but there can be many absolute centers, many shortest path trees from one center, and optimal trees that are not shortest path trees from any center. Any shortest path tree from any absolute center is optimal, so ties need no special rule.

**Negative lengths** are not allowed; the result relies on distances in $G$ being shortest path distances.

## Variants

- **Unit lengths (hop diameter).** With all lengths 1, an absolute center is a vertex or the midpoint of an edge, so one [breadth-first search](/breadth-first-search/) from each vertex and each edge midpoint finds it.
- **Geometric version.** For points in the plane with Euclidean distances, Ho, Lee, Chang and Wong showed that some optimal tree has one hub or two adjacent hubs, with all other points joined to a hub, and gave a polynomial algorithm.
- **Bounded diameter minimum spanning tree.** Find a spanning tree of least total weight among those with diameter at most $D$. This is NP-hard, and it is a standard hard network design problem.
- **Minimum diameter with a weight budget.** Minimize the diameter subject to total weight at most $B$; also NP-hard.
- **Sum instead of maximum.** Minimizing the sum of all pairwise tree distances is the [minimum routing cost spanning tree](/minimum-routing-cost-spanning-tree/) problem, which is NP-hard.

## Examples

**The weighted example graph.** Take the graph on $a$ to $f$ with lengths $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. The best vertex is $c$, with eccentricity 7, but the absolute center is the point $p$ on $ce$ at distance 2 from $c$ and 3 from $e$, with $r^\ast = 5$:

| vertex | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
|---|---|---|---|---|---|---|
| distance from $p$ | 5 | 3 | 2 | 5 | 3 | 5 |

The shortest path tree from $p$ is $\{ac, bc, bd, ce, ef\}$, with diameter $10 = 2 r^\ast$, for example from $a$ to $f$. A search over all 55 spanning trees confirms that it is the only tree of diameter 10. Here it is also the minimum spanning tree, which is a coincidence. The graph itself has diameter 10, so no tree could be shorter.

**The same graph with unit lengths.** The best vertex, $b$, $c$ or $d$, has eccentricity 2, which gives a tree of diameter 4. The midpoint of the edge $bd$ is better: every vertex is within $3/2$ of it, so $r^\ast = 3/2$ and the optimum is 3. The tree $\{bd, ab, bc, de, df\}$ attains it, and a search shows that 8 of the 55 trees have diameter 3. So the center inside an edge matters.

**A path.** A path is its own only spanning tree, and its diameter is its length. Its absolute center is the midpoint.

**A cycle with unit lengths.** For $C_n$ with $n \ge 3$, every spanning tree is a path with $n - 1$ edges, so the minimum diameter is $n - 1$. This agrees with the theorem: for even $n$ the midpoint of an edge has its farthest vertices at distance $(n - 1)/2$, and for odd $n$ a vertex has its farthest vertices at distance $(n - 1)/2$, so $r^\ast = (n - 1)/2$ in both cases. Ties are total here: all $n$ trees are optimal.

**A disconnected graph** has no spanning tree; two disjoint triangles with unit lengths give a forest of two paths, each of diameter 2.

## Known algorithms

| method | time | notes |
|---|---|---|
| Try all spanning trees | exponential | for tiny graphs and testing |
| Absolute center, then a shortest path tree (Hassin and Tamir) | $O(mn \log n)$ | with the absolute 1-center method of Kariv and Hakimi |
| Unit lengths, search vertices and edge midpoints | $O(m(n + m))$ | one BFS for each candidate |

**Finding the absolute center.** First compute all distances, with [Dijkstra's algorithm](/dijkstra/) from each vertex or another [all-pairs](/all-pairs-shortest-paths/) method. For an edge $uv$ of length $w$ and a point at distance $t$ from $u$, the distance to $x$ is $\min(d(u, x) + t,\ d(v, x) + w - t)$, a function with a peak. The upper envelope of these $n$ functions is piecewise linear in $t$, and its lowest point is the best point on $uv$. Kariv and Hakimi find it for each edge by sorting the vertices by $d(u, x)$ and scanning, so the edges together cost $O(mn \log n)$, after $O(mn + n^2 \log n)$ for all distances. The best point over all edges is an absolute center. A shortest path tree from it then costs one more Dijkstra run.

## Bounds

**Lower bound on the value.** Every spanning tree has diameter at least the diameter of the graph, $\max_{u, v} d_G(u, v)$, since tree distances are at least graph distances. It also has diameter at least $2 r^\ast$, which is the exact answer. The graph diameter $D_G$ and $r^\ast$ satisfy $D_G / 2 \le r^\ast \le D_G$, so the optimal tree is within a factor 2 of the graph diameter.

**Lower bound on time.** Any algorithm must read all edges, so $\Omega(n + m)$ time is needed. No algorithm much faster than all-pairs distances is known for general weighted graphs.

## Reductions

- **To the absolute 1-center.** The problem is equivalent to finding an absolute center, by the theorem.
- **To shortest paths.** Given the center, one shortest path computation finishes the task.
- **Hardness of the constrained forms.** Adding a weight objective or a weight budget makes the problem NP-hard.

## Applications

- **Communication networks.** A tree with small diameter bounds the worst delay of any message, and the hub is the natural place for a central switch.
- **Overlay and multicast networks.** Low diameter trees bound the latency of broadcast from any member.
- **Clustering and data structures.** Small diameter trees serve as backbones with bounded query paths.
- **Facility location.** The absolute center is the classic answer to the question of where to put one emergency facility on a road network.

## References
