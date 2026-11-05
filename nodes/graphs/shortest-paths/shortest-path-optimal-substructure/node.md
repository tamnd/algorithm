---
tag: QQZG70
kind: concept
slug: shortest-path-optimal-substructure
name: Optimal substructure of shortest paths
aliases:
- optimal substructure
area: graphs/shortest-paths
level: intro
summary: Every subpath of a shortest path is itself a shortest path, which justifies dynamic programming and relaxation.
prereqs: [shortest-path, walk, optimal-substructure]
see_also: [optimal-substructure, edge-relaxation, bellman-ford, floyd-warshall, dag-shortest-paths, shortest-path-optimality-conditions, shortest-path-tree, longest-path-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction, the subsection Optimal substructure of a shortest path (the lemma that subpaths of shortest paths are shortest paths), and Section 14.3, Elements of dynamic programming (unweighted shortest and longest simple paths)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths, and Chapter 9, All-Pairs Shortest Paths (the recursive structure behind the dynamic programs)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 4, Section 4.4 (Dijkstra) and Section 4.6 (shortest paths with negative edges), and Chapter 6, Section 6.1 (shortest paths in dags, the canonical dynamic program)
---

Optimal substructure of shortest paths is the property that every subpath of a [shortest path](/shortest-path/) is itself a shortest path between its own ends. It holds whenever the distance between the ends of the whole path is finite, with any real weights. It is the reason that the distance to a vertex can be built from distances to its predecessors, which is the base of [edge relaxation](/edge-relaxation/), [Bellman-Ford](/bellman-ford/), [Floyd-Warshall](/floyd-warshall/) and the [dynamic program on a DAG](/dag-shortest-paths/). It is the graph form of the general [optimal substructure](/optimal-substructure/) of dynamic programming.

## In plain words

Suppose the best route from your home to the airport passes the station. Then the part of the route from your home to the station must also be the best route from your home to the station. If a better way to the station existed, you could use it, then continue to the airport as before, and you would get a better route to the airport. That is impossible, because the route was already the best.

So a best route is made of best routes. This lets a program find best routes step by step: the best route to a place is the best route to some place just before it, plus one more road.

## The idea

Let $G = (V, E)$ be a directed graph with weights $w : E \to \mathbb{R}$, and let $\delta$ be the [distance](/shortest-path/).

**Lemma (subpaths of shortest paths are shortest paths).** Let $p = \langle v_0, v_1, \ldots, v_k \rangle$ be a shortest path from $v_0$ to $v_k$, so $w(p) = \delta(v_0, v_k)$ is finite. For $0 \le i \le j \le k$ let $p_{ij} = \langle v_i, \ldots, v_j \rangle$. Then $p_{ij}$ is a shortest path from $v_i$ to $v_j$.

*Proof.* Write $p$ as $p_{0i}$, then $p_{ij}$, then $p_{jk}$, so $w(p) = w(p_{0i}) + w(p_{ij}) + w(p_{jk})$. Suppose some walk $q$ from $v_i$ to $v_j$ has $w(q) < w(p_{ij})$. Then $p_{0i}$, then $q$, then $p_{jk}$ is a walk from $v_0$ to $v_k$ of weight $w(p_{0i}) + w(q) + w(p_{jk}) < w(p) = \delta(v_0, v_k)$. This contradicts the definition of $\delta$ as an infimum. So no such $q$ exists, and $w(p_{ij}) = \delta(v_i, v_j)$. $\square$

The proof is a *cut and paste* argument: cut out a part, paste in a better part, and get a better whole. It needs only that weights add along a walk. It does not need nonnegative weights, integer weights or the absence of negative cycles anywhere in the graph; it needs only that $\delta(v_0, v_k)$ is finite, which holds as soon as $p$ is a shortest path.

**The Bellman equations.** Apply the lemma with $i = 0$ and $j = k - 1$. If $v \ne s$ and $\delta(s, v)$ is finite, a shortest path to $v$ ends with some arc $(u, v)$, and its prefix is a shortest path to $u$. Every arc gives a walk, so $\delta(s, v) \le \delta(s, u) + w(u, v)$ for every arc. Together:

$$\delta(s, s) = 0 \text{ (when no negative cycle is reachable from } s\text{)}, \qquad \delta(s, v) = \min_{(u, v) \in E} \big( \delta(s, u) + w(u, v) \big) \text{ for } v \ne s.$$

The inequality half is the triangle inequality. The page [shortest-path optimality conditions](/shortest-path-optimality-conditions/) turns these equations into a test of a candidate set of distances.

**Three ways to cut a path.** The dynamic programs differ in how they cut a shortest path into a smaller subproblem.

| cut | subproblem | algorithm |
|---|---|---|
| remove the last arc | distance with at most $\ell - 1$ arcs | [Bellman-Ford](/bellman-ford/), [slow APSP by matrix multiplication](/slow-apsp-matrix-multiplication/) |
| split at the middle arc count | two paths of at most $\ell / 2$ arcs | [repeated squaring](/apsp-repeated-squaring/) |
| split at the largest intermediate vertex | paths with intermediate vertices in $\{1, \ldots, k - 1\}$ | [Floyd-Warshall](/floyd-warshall/) |
| remove the last arc, in topological order | distance to an earlier vertex | [DAG shortest paths](/dag-shortest-paths/) |

Each cut keeps a shortest path inside the smaller subproblem because of the lemma. For the arc count, a shortest path with no negative cycle in reach can be taken simple, so it has at most $n - 1$ arcs and the recursion on arc counts stops at $n - 1$.

## Examples

**A shortest path and its pieces.** In the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7), the shortest path from $s$ to $z$ is $s \to y \to x \to t \to z$ with weight $7 - 3 - 2 - 4 = -2$. Its pieces and their distances:

| subpath | weight | distance between its ends |
|---|---|---|
| $s \to y \to x$ | 4 | $\delta(s, x) = 4$ |
| $y \to x \to t$ | $-5$ | $\delta(y, t) = -5$ |
| $x \to t \to z$ | $-6$ | $\delta(x, z) = -6$ |
| $y \to x \to t \to z$ | $-9$ | $\delta(y, z) = -9$ |

Every row agrees, as the lemma says, and the graph has three negative arcs.

**Non-example: longest simple paths.** Take the undirected triangle on $a, b, c$ with each edge of weight 1. The longest simple path from $a$ to $c$ is $a, b, c$ of weight 2. Its subpath $a, b$ has weight 1, but the longest simple path from $a$ to $b$ is $a, c, b$ of weight 2. The paste step fails: $a, c, b$ followed by $b, c$ is not simple, since $c$ repeats. So the [longest path problem](/longest-path-problem/) has no such substructure, and it is NP-hard in general. CLRS Section 14.3 uses the same kind of example.

**Non-example: shortest paths with a side constraint.** In the [constrained shortest path](/constrained-shortest-path/) problem, each arc also has a cost, and the total cost must stay below a budget. A cheap prefix may use too much budget, and the best feasible path to the airport need not start with the best feasible path to the station. The state must include the budget used, which is why the problem needs a larger dynamic program.

**Non-example: a reachable negative cycle.** If a negative cycle is reachable from $s$ and reaches $v$, there is no shortest path to $v$ at all, so the lemma says nothing. The equations above still hold with the value $-\infty$, but they no longer determine $\delta$.

## Where it is used

- [Edge relaxation](/edge-relaxation/): the step $d(v) \leftarrow \min(d(v), d(u) + w(u, v))$ is the Bellman equation used as an update.
- [Bellman-Ford](/bellman-ford/) and [SPFA](/spfa/): recursion on the number of arcs.
- [Dijkstra's algorithm](/dijkstra/): the prefix of a shortest path to the next vertex lies inside the set of finished vertices.
- [Floyd-Warshall](/floyd-warshall/): recursion on the set of allowed intermediate vertices.
- [Shortest-path tree](/shortest-path-tree/): the prefixes of shortest paths can be chosen to fit together into one tree.
- [Yen's algorithm](/yen-k-shortest-paths/): a spur path from a vertex of a known path is a shortest path in a smaller graph.

## References
