---
tag: M8K2PR
kind: problem
slug: replacement-paths
name: Replacement paths
aliases:
- replacement path problem
area: graphs/shortest-paths
level: advanced
summary: For each edge e on a shortest s-t path, find the shortest s-t path avoiding e.
prereqs: [single-pair-shortest-path, shortest-path-tree, dijkstra]
see_also: [k-shortest-paths, yen-k-shortest-paths, single-pair-shortest-path, shortest-path-tree, dijkstra, all-pairs-shortest-paths, apsp-conjecture, potential-function-reduced-costs]
sources:
  - paper: "Kavindra Malik, Ashok K. Mittal and Santosh K. Gupta, The k most vital arcs in the shortest path problem, Operations Research Letters 8(4), 223 to 227 (1989)"
    locator: the O(m + n log n) method for one failed edge in undirected graphs, from the two shortest-path trees
  - paper: "John Hershberger and Subhash Suri, Vickrey prices and shortest paths, what is an edge worth?, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS), 2001, 252 to 259"
    locator: the undirected replacement paths algorithm and the Vickrey pricing application
  - paper: "John Hershberger, Subhash Suri and Amit Bhosle, On the difficulty of some shortest path problems, ACM Transactions on Algorithms 3(1), article 5 (2007)"
    locator: the Omega(m sqrt(n)) lower bound for directed replacement paths in the path-comparison model
  - paper: "Liam Roditty and Uri Zwick, Replacement paths and k simple shortest paths in unweighted directed graphs, ACM Transactions on Algorithms 8(4), article 33 (2012)"
    locator: the randomized O(m sqrt(n)) algorithm for unweighted directed graphs
  - paper: "Zvi Gotthilf and Moshe Lewenstein, Improved algorithms for the k simple shortest paths and the replacement paths problems, Information Processing Letters 109(7), 352 to 355 (2009)"
    locator: the O(mn + n^2 log log n) bound for weighted directed graphs
  - paper: doi:10.1145/3186893
    title: Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), article 27 (2018)
    locator: the subcubic equivalence of replacement paths and all-pairs shortest paths
  - paper: doi:10.1287/mnsc.17.11.712
    title: Jin Y. Yen, Finding the K shortest loopless paths in a network, Management Science 17(11), 712 to 716 (1971)
    locator: the spur computations, which are replacement-path computations with a fixed prefix
---

The replacement paths problem takes a shortest path $P$ from $s$ to $t$ and asks, for every arc $e$ of $P$, for the length of a shortest path from $s$ to $t$ in the graph without $e$. It models the failure of one link: each answer is the best route if that link breaks. The direct method runs a [single-pair](/single-pair-shortest-path/) algorithm once per arc of $P$, which is up to $n - 1$ runs of [Dijkstra](/dijkstra/). Undirected graphs need only $O(m + n \log n)$ time in total, from two [shortest-path trees](/shortest-path-tree/). Directed weighted graphs are as hard as [all-pairs shortest paths](/all-pairs-shortest-paths/) under subcubic reductions. The best replacement path is the second shortest simple path, so the problem is the core step of [k shortest paths](/k-shortest-paths/).

## In plain words

You know the best route from home to work. Now any one road on that route might be closed. For each road on the route, you want to know the best way to go if that road is closed.

The simple way is to close each road in turn and search again. That is one search for each road on the route. In a network where every road can be used both ways, one clever pass gives all the answers at once. With one-way roads, no method much faster than the simple way is known.

## Definition

Let $G = (V, E)$ be a directed graph with $n$ vertices, $m$ arcs and weights $w : E \to \mathbb{R}$, and let $s, t \in V$. Let $P = \langle s = v_0, v_1, \ldots, v_\ell = t \rangle$ be a shortest path from $s$ to $t$, with arcs $e_i = (v_{i-1}, v_i)$. For each $i = 1, \ldots, \ell$, the *replacement distance* is

$$d(s, t, e_i) = \delta_{G - e_i}(s, t),$$

the shortest-path weight from $s$ to $t$ in $G$ with the arc $e_i$ removed. The problem asks for all $\ell$ values, and often for a replacement path for each. The *vertex version* removes $v_i$ for $0 < i < \ell$ instead of an arc. In an undirected graph, the edges of $P$ are removed in both directions.

**Weight assumptions.**

- The standard setting is nonnegative real weights, so that Dijkstra applies.
- Negative weights are allowed if $G$ has no [negative cycle](/negative-cycle/). Removing arcs cannot create a negative cycle, so every $\delta_{G - e_i}$ is then well defined. One run of Bellman-Ford gives a [potential](/potential-function-reduced-costs/) $h$ with nonnegative reduced costs in $G$, and the same $h$ is feasible in each $G - e_i$, so the nonnegative algorithms then apply.
- If $G$ has a negative cycle reachable from $s$ that reaches $t$, then $P$ does not exist and the problem is not defined, even if some $G - e_i$ has no negative cycle.
- Integer weights are used only by the algorithms based on fast matrix multiplication.

**Unreachable cases.** If $t$ is not reachable from $s$, there is no $P$ and the output is empty. If removing $e_i$ cuts every path from $s$ to $t$, then $d(s, t, e_i) = +\infty$; such an arc is on every path from $s$ to $t$.

## Variants

- **Arc or vertex failures.** Removing a vertex of $P$ instead of an arc. Most algorithms handle both.
- **Undirected graphs.** Much easier; see the known algorithms.
- **Most vital arc.** Find the arc whose removal increases $\delta(s, t)$ the most, that is, the arc of $P$ with the largest $d(s, t, e_i)$. With $k$ removals it is NP-hard.
- **Second shortest simple path.** It is $\min_i d(s, t, e_i)$ with the path attached, since every other simple path misses some arc of $P$.
- **Single-source replacement paths.** For every target $v$ and every arc $e$ of the shortest-path tree, the distance from $s$ to $v$ in $G - e$.
- **Distance sensitivity oracles.** Preprocess $G$ so that a query $(u, v, e)$ returns $\delta_{G - e}(u, v)$ quickly, for all pairs.

## Examples

**A directed graph with nonnegative weights.** Take the arcs $C \to D$ (3), $C \to E$ (2), $D \to F$ (4), $E \to D$ (1), $E \to F$ (2), $E \to G$ (3), $F \to G$ (2), $F \to H$ (1) and $G \to H$ (2), with $s = C$ and $t = H$. The shortest path is $P = C E F H$ of weight 5.

| removed arc | replacement distance | a replacement path |
|---|---|---|
| $C \to E$ | 8 | $C D F H$ |
| $E \to F$ | 7 | $C E G H$ |
| $F \to H$ | 7 | $C E G H$ |

The second shortest simple path has weight $\min(8, 7, 7) = 7$.

**Negative weights, no negative cycle.** Take the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7). The shortest path from $s$ to $z$ is $s y x t z$ of weight $-2$. Removing $s \to y$, $y \to x$ or $x \to t$ gives 2 by $s t z$, and removing $t \to z$ gives 16 by $s y z$.

**A negative cycle.** In the last graph, change $x \to t$ to $-6$. The cycle $t \to x \to t$ has weight $-1$ and lies on walks from $s$ to $z$, so $\delta(s, z) = -\infty$ and there is no shortest path $P$ to start from. The graph without $x \to t$ has finite distances, but the problem as defined has no answer.

**A cut arc.** Take $s \to a$ (1), $a \to t$ (1), $s \to b$ (2) and $b \to a$ (2), so $P = s a t$ of weight 2. Removing $s \to a$ gives 5 by $s b a t$. Removing $a \to t$ leaves no path, so $d(s, t, a \to t) = +\infty$.

## Known algorithms

| algorithm | graph | time |
|---|---|---|
| one Dijkstra run per arc of $P$ | directed, $w \ge 0$ | $O(\ell (m + n \log n)) = O(mn + n^2 \log n)$ |
| Malik, Mittal and Gupta (1989); Hershberger and Suri (2001) | undirected, $w \ge 0$ | $O(m + n \log n)$ |
| Roditty and Zwick (2005) | directed, unweighted | $O(m \sqrt{n})$ expected, randomized |
| Gotthilf and Lewenstein (2009) | directed, $w \ge 0$ | $O(mn + n^2 \log \log n)$ |
| Vassilevska Williams (2011) | directed, integer weights in $[-M, M]$ | $\tilde{O}(M n^{\omega})$ |

**The undirected method.** Build a shortest-path tree $T_s$ from $s$ and a shortest-path tree $T_t$ into $t$, with distances $d_s$ and $d_t$. Removing the edge $e_i$ of $P$ from $T_s$ splits the vertices into the part $S_i$ that still holds $s$ and the rest. A shortest path in $G - e_i$ crosses from $S_i$ to the rest by some edge $(u, v) \ne e_i$, and with positive weights one can choose it so that its two ends are joined to $s$ and $t$ by tree paths. So

$$d(s, t, e_i) = \min \{ d_s(u) + w(u, v) + d_t(v) : u \in S_i,\ v \notin S_i,\ (u, v) \ne e_i \}.$$

The sets $S_1 \subseteq S_2 \subseteq \cdots$ grow along $P$, so each non-tree edge is a candidate for a contiguous range of indices $i$. A priority queue, or a union-find sweep over the edges in order of their value, gives all minima in $O(m + n \log n)$ time.

## Bounds

- **Lower bound.** $\Omega(m)$ to read the graph, so the undirected bound is optimal for sparse graphs up to the $n \log n$ term.
- **Path-comparison model.** Hershberger, Suri and Bhosle show $\Omega(m \sqrt{n})$ for directed graphs, for algorithms that only compare path lengths, when $m = O(n \sqrt{n})$.
- **Subcubic equivalence.** For directed graphs with integer weights, an $O(n^{3 - \varepsilon})$ algorithm exists for replacement paths if and only if one exists for [all-pairs shortest paths](/all-pairs-shortest-paths/) (Vassilevska Williams and Williams). By the [APSP conjecture](/apsp-conjecture/), the simple $\ell$ Dijkstra runs are near optimal for dense weighted directed graphs.
- **Unweighted directed graphs** are easier: $O(m \sqrt{n})$, which matches the path-comparison bound.

## Reductions

- **To single-pair shortest paths.** One run on each $G - e_i$.
- **Second shortest simple path to replacement paths.** Take the minimum of the answers. The other direction also holds under subcubic reductions for directed graphs.
- **To k shortest paths.** Yen's spur computation for the vertex $v_{i-1}$ is a replacement-path computation with the prefix $v_0, \ldots, v_{i-1}$ fixed and its vertices removed; Hershberger, Maxel and Suri use a replacement paths routine to do all the spurs of one path at once.
- **From negative weights to nonnegative weights.** One Bellman-Ford run and the reduced costs $w_h(u, v) = w(u, v) + h(u) - h(v)$ keep every $\delta_{G - e_i}$ up to the constant $h(s) - h(t)$.

## Applications

- **Network reliability.** Find the routes to use when one link fails, and find the links whose failure hurts the most.
- **Vickrey pricing.** In an auction for a path where each edge is owned by an agent, the truthful payment to the owner of $e_i$ is $d(s, t, e_i) - \delta(s, t) + w(e_i)$; Hershberger and Suri computed all these payments for undirected graphs in the time of one shortest-path run.
- **k shortest simple paths.** Replacement paths give the second shortest path and speed up the spur steps of Yen's algorithm.
- **Transport planning.** The most vital arc of a road or supply network shows where a closure causes the largest detour.

## References
