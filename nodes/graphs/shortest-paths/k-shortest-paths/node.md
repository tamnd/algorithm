---
tag: Q9QKSN
kind: problem
slug: k-shortest-paths
name: K shortest paths
aliases:
- k shortest simple paths
- top-k paths
area: graphs/shortest-paths
level: advanced
summary: List the k shortest simple s-t paths in nondecreasing order of weight.
prereqs: [shortest-path, single-pair-shortest-path, dijkstra]
see_also: [yen-k-shortest-paths, eppstein-k-shortest-paths, replacement-paths, single-pair-shortest-path, dijkstra, shortest-path-tree, edge-disjoint-paths, second-best-mst]
sources:
  - paper: doi:10.1287/mnsc.17.11.712
    title: Jin Y. Yen, Finding the K shortest loopless paths in a network, Management Science 17(11), 712 to 716 (1971)
    locator: the statement of the loopless problem and the algorithm with O(K n) shortest-path calls
  - paper: doi:10.1137/S0097539795290477
    title: David Eppstein, Finding the k shortest paths, SIAM Journal on Computing 28(2), 652 to 673 (1998)
    locator: the introduction (the problem with and without repeated vertices, and the history) and the O(m + n log n + k) bound
  - paper: "Eugene L. Lawler, A procedure for computing the K best solutions to discrete optimization problems and its application to the shortest path problem, Management Science 18(7), 401 to 405 (1972)"
    locator: the partition of the solution space into subproblems
  - paper: "Naoki Katoh, Toshihide Ibaraki and Hisashi Mine, An efficient algorithm for K shortest simple paths, Networks 12(4), 411 to 427 (1982)"
    locator: the O(k (m + n log n)) bound for undirected graphs
  - paper: "John Hershberger, Matthew Maxel and Subhash Suri, Finding the k shortest simple paths, a new algorithm and its implementation, ACM Transactions on Algorithms 3(4), article 45 (2007)"
    locator: the replacement-path speed-up of Yen and the cases where it must fall back to Yen
  - paper: doi:10.1145/3186893
    title: Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), article 27 (2018)
    locator: the subcubic equivalence of all-pairs shortest paths with replacement paths and the second shortest simple path
  - url: https://en.wikipedia.org/wiki/K_shortest_path_routing
    title: Wikipedia, K shortest path routing
    locator: sections Algorithm (loopy and loopless variants) and Applications
---

The k shortest paths problem asks for the $k$ cheapest paths from $s$ to $t$, listed in nondecreasing order of weight. It has two main forms. In the *simple* (loopless) form a path may not repeat a vertex; [Yen's algorithm](/yen-k-shortest-paths/) solves it with $O(kn)$ calls of a [single-pair](/single-pair-shortest-path/) shortest-path algorithm. In the *walk* form vertices may repeat; [Eppstein's algorithm](/eppstein-k-shortest-paths/) solves it in $O(m + n \log n + k)$ time. Already for $k = 2$ the simple form in a directed graph is as hard as [all-pairs shortest paths](/all-pairs-shortest-paths/) under subcubic reductions, and it is closely tied to [replacement paths](/replacement-paths/).

## In plain words

A route planner often shows more than one route: the best one, then a second, then a third. This problem asks for the best few routes from a start to a goal, in order, cheapest first.

There are two versions. In the first, a route may not visit the same place twice. In the second, it may, so a route can go around a loop and come back. The two versions give different answers when the map has loops, and the second version is much easier to solve fast.

## Definition

Let $G = (V, E)$ be a directed graph with $n$ vertices, $m$ arcs and weights $w : E \to \mathbb{R}$, and let $s, t \in V$ and $k \ge 1$. Write $\mathcal{P}(s, t)$ for the set of simple paths from $s$ to $t$ and $w(p)$ for the sum of the weights of the arcs of $p$.

**The k shortest simple paths problem.** Output distinct paths $p_1, \ldots, p_{k'} \in \mathcal{P}(s, t)$, with $k' = \min(k, |\mathcal{P}(s, t)|)$, such that $w(p_1) \le \cdots \le w(p_{k'})$ and $w(p_{k'}) \le w(q)$ for every path $q \in \mathcal{P}(s, t)$ not in the list. Ties may be broken in any way.

**The k shortest walks problem.** The same with $\mathcal{P}(s, t)$ replaced by the set of all walks from $s$ to $t$, which is infinite when a cycle lies on some walk from $s$ to $t$.

**Weight assumptions.** Each algorithm states its own:

- Yen's algorithm and most algorithms for simple paths need nonnegative weights, so that Dijkstra can find the spur paths. With negative weights but no [negative cycle](/negative-cycle/), the same scheme works with Bellman-Ford, because deleting vertices and arcs cannot create a negative cycle.
- Eppstein's algorithm for walks needs no negative cycle on any walk from $s$ to $t$; otherwise the walk weights are unbounded below and the problem has no answer. Nonnegative weights are the usual case.
- With a negative cycle, the simple form is still well defined, since there are finitely many simple paths, but it is NP-hard already for $k = 1$: it contains the [longest path problem](/longest-path-problem/) after negating the weights.
- Integer weights are not needed except by algorithms based on fast matrix multiplication.

**Unreachable target.** If $t$ is not reachable from $s$, both sets are empty and the correct output is the empty list. If fewer than $k$ simple paths exist, the output has fewer than $k$ paths.

## Variants

- **Simple paths or walks.** The two forms above. In a DAG they agree.
- **Undirected graphs.** For simple paths, Katoh, Ibaraki and Mine get $O(k(m + n \log n))$, a factor $n$ better than Yen in directed graphs.
- **Second shortest path.** The case $k = 2$. The second shortest simple path is the best [replacement path](/replacement-paths/) over the arcs of the first path, so it is solved by one replacement paths computation.
- **Strictly larger weights.** List the $k$ smallest distinct path weights instead of $k$ distinct paths.
- **One source, all targets.** Eppstein also lists the $k$ shortest walks from $s$ to every vertex, in $O(m + n \log n + kn)$ total time.
- **Disjoint paths.** Asking for $k$ arc-disjoint or vertex-disjoint paths of least total weight is a different problem, solved by min-cost flow; see [edge-disjoint paths](/edge-disjoint-paths/).
- **Constrained and diverse paths.** Many applications ask for paths that differ enough from each other, or that meet a resource bound; these are often solved by listing paths in order until one fits.

## Examples

**Simple paths.** Take the arcs $C \to D$ (3), $C \to E$ (2), $D \to F$ (4), $E \to D$ (1), $E \to F$ (2), $E \to G$ (3), $F \to G$ (2), $F \to H$ (1) and $G \to H$ (2), with $s = C$ and $t = H$. The graph is acyclic and has seven paths from $C$ to $H$:

| rank | path | weight |
|---|---|---|
| 1 | $C E F H$ | 5 |
| 2 | $C E G H$ | 7 |
| 3 | $C D F H$ | 8 |
| 4 | $C E F G H$ | 8 |
| 5 | $C E D F H$ | 8 |
| 6 | $C D F G H$ | 11 |
| 7 | $C E D F G H$ | 11 |

For $k = 3$ any one of the three paths of weight 8 may be the third path. For $k = 10$ the output is all seven paths.

**Simple paths against walks.** Take the arcs $s \to a$ (1), $a \to t$ (1), $a \to b$ (1) and $b \to a$ (1). The only simple path is $s a t$ of weight 2, so the simple form with $k = 3$ outputs one path. The walks $s a t$, $s a b a t$ and $s a b a b a t$ have weights 2, 4 and 6, so the walk form with $k = 3$ outputs those three.

**A negative cycle.** Change $b \to a$ to $-3$. The cycle $a \to b \to a$ has weight $-2$, and the walks $s (a b)^j a t$ have weight $2 - 2j$, so the walk form has no answer. The simple form still has the answer $s a t$ (2), but a general algorithm cannot rely on Dijkstra or Bellman-Ford to find spur paths.

**Unreachable.** Remove the arc $a \to t$. No path or walk reaches $t$, and every algorithm must return the empty list.

## Known algorithms

| algorithm | form | graph | time |
|---|---|---|---|
| [Yen](/yen-k-shortest-paths/) (1971) with Dijkstra and a Fibonacci heap | simple | directed, $w \ge 0$ | $O(kn(m + n \log n))$ |
| Lawler (1972) | simple | directed, $w \ge 0$ | same worst case, fewer spur computations in practice |
| Katoh, Ibaraki and Mine (1982) | simple | undirected, $w \ge 0$ | $O(k(m + n \log n))$ |
| Hershberger, Maxel and Suri (2007) | simple | directed, $w \ge 0$ | about $O(k(m + n \log n))$ in most cases, Yen's bound in the worst case |
| [Eppstein](/eppstein-k-shortest-paths/) (1998) | walks | directed, no negative cycle | $O(m + n \log n + k)$, the paths given in an implicit form |

Eppstein's bound counts the output as a list of "sidetrack" arcs; writing out each path in full adds its length. For simple paths, all these methods follow the scheme of Lawler: the set of paths not yet output is split into subproblems, each a shortest-path problem with some arcs and vertices removed and a fixed prefix.

## Bounds

- **Output size.** Writing $k$ paths takes $\Omega(k)$ time, and up to $\Omega(kn)$ if each path is written in full; Eppstein's implicit form avoids the second term.
- **Second shortest simple path, directed.** Vassilevska Williams and Williams show that it is equivalent to all-pairs shortest paths under subcubic reductions. So by the [APSP conjecture](/apsp-conjecture/), no $O(n^{3 - \varepsilon})$ algorithm exists for dense graphs with large integer weights. For sparse weighted directed graphs, the best known bounds for $k = 2$ are about $O(mn)$, the cost of $n$ Dijkstra runs.
- **Simple paths in undirected graphs** are easier: the $O(k(m + n \log n))$ bound matches $k$ shortest-path computations.
- **Walks.** The $O(m + n \log n + k)$ bound is one Dijkstra run plus constant time per path, which is optimal for algorithms that must first find a shortest path.
- **Negative cycles.** The simple form is NP-hard for $k = 1$, as said in the definition.

## Reductions

- **To single-pair shortest paths.** Yen and Lawler reduce $k$ shortest simple paths to $O(kn)$ single-pair problems on subgraphs.
- **To replacement paths.** The second shortest simple path is $\min_e d_{G - e}(s, t)$ over the arcs $e$ of a shortest path, the minimum of the [replacement paths](/replacement-paths/) answers. Hershberger, Maxel and Suri use a replacement paths routine to do all the spur computations for one path at once.
- **From all-pairs shortest paths.** For $k = 2$ in directed graphs, a subcubic algorithm would give a subcubic APSP algorithm (Vassilevska Williams and Williams).
- **From longest paths.** With negative cycles allowed, $k = 1$ on $-w$ is the longest simple path problem.
- **To a heap of sidetracks (walks).** Every walk from $s$ to $t$ is described by the arcs where it leaves the [shortest-path tree](/shortest-path-tree/) into $t$; Eppstein orders these sets in a heap, so listing walks becomes a best-first search in a heap of bounded degree.

## Applications

- **Route planning.** Show a few alternative routes, or find the best route under a cost that the shortest-path algorithm cannot handle by listing paths by length and checking each.
- **Network routing.** K shortest path routing spreads traffic over several paths and keeps backup routes.
- **Constrained shortest paths.** For a resource bound, list paths by cost until one meets the bound; this is exact but can be slow.
- **Speech and language processing.** The $k$ best outputs of a decoder are the $k$ shortest paths in a weighted lattice; this is used for n-best lists.
- **Biology.** Alternative pathways in metabolic and signaling networks.
- **Sensitivity analysis.** The gap between the first and the second shortest path shows how stable the best route is.

## References
