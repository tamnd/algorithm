---
tag: A13K1H
kind: algorithm
slug: goldberg-scaling-sssp
name: Goldberg's scaling algorithm
aliases:
- Goldberg scaling shortest paths
area: graphs/shortest-paths
level: research
summary: Scaling algorithm for negative integer weights using potentials, running in O(sqrt(n) m log N) time.
solves: [single-source-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the largest absolute value of a negative weight (at least 2)}
  time: {worst: O(sqrt(n) m log N), best: Θ(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [potential-function-reduced-costs, scaling-technique, strongly-connected-components, dag-shortest-paths, dial-algorithm, gabow-scaling-sssp]
see_also: [bellman-ford, goldberg-radzik, near-linear-negative-sssp, johnson, negative-cycle-detection, cost-scaling, condensation-graph, tarjan-scc]
sources:
  - paper: "Andrew V. Goldberg, Scaling algorithms for the shortest paths problem, SIAM Journal on Computing 24(3), 494 to 504 (1995)"
    locator: the whole paper (bit scaling with reduced costs at least -1, improvable vertices, the admissible graph with its strongly connected components contracted, the cut-relabel and path-elimination steps, and the O(sqrt(n) m log N) bound)
  - paper: doi:10.1016/0022-0000(85)90039-X
    title: Harold N. Gabow, Scaling algorithms for network problems, Journal of Computer and System Sciences 31(2), 148 to 168 (1985)
    locator: bit scaling for shortest paths and the O(n^(3/4) m log N) bound for negative weights that Goldberg improves
  - paper: doi:10.1007/s101070050058
    title: Boris V. Cherkassky and Andrew V. Goldberg, Negative-cycle detection algorithms, Mathematical Programming 85(2), 277 to 311 (1999)
    locator: the description and experimental evaluation of Goldberg's scaling algorithm as a negative-cycle detection method
---

Goldberg's scaling algorithm solves [single-source shortest paths](/single-source-shortest-paths/) with integer weights that may be negative, or finds a [negative cycle](/negative-cycle/), in $O(\sqrt n\, m \log N)$ time, where $-N$ is the most negative weight. Like [Gabow's algorithm](/gabow-scaling-sssp/) it adds the bits of the weights one at a time and carries [potentials](/potential-function-reduced-costs/) from one scale to the next. With negative weights, each new scale starts with reduced costs of at least $-1$, and the work is to remove the $-1$ edges. Goldberg looks at the graph of edges with reduced cost at most 0: either many vertices with a $-1$ edge sit on one level of it, and one cut fixes them all, or they lie along one long path, and one bucket-based shortest-path sweep fixes them all. Either way $\sqrt k$ of the $k$ bad vertices are fixed in linear time, so a scale takes $O(\sqrt n\, m)$. Andrew Goldberg published it in 1993 (journal version 1995); it was the best bound for integer weights until the near-linear algorithms of 2022.

## In plain words

Some roads have negative lengths. The goal is to give every place a "height" so that, after adding height differences, no road is negative. Then [Dijkstra's algorithm](/dijkstra/) can finish the job. If no such heights exist, there is a loop of negative total length.

The algorithm first rounds every length to a coarse unit, where heights are easy, and refines the lengths one binary digit at a time. After each refinement the old heights, doubled, are almost right: every road is off by at most one unit. A place with an incoming road that is off by one is *improvable*.

If many improvable places sit on the same level of the network of non-positive roads, lowering everything from that level on fixes them all. Otherwise they lie along a long chain, and one sweep along it fixes the whole chain.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a source $s$, and an integer weight $w(u, v)$ on each edge. The output is the distance $\delta(s, v)$ for every vertex and a [shortest-path tree](/shortest-path-tree/), or a report that a negative cycle is reachable from $s$.

**Weight assumptions.** Every weight is an integer, negative weights allowed, with $w(u, v) \ge -N$; zero-weight cycles, parallel edges and self-loops are allowed, and non-integer weights are rejected. The algorithm first keeps only the vertices reachable from $s$. If a negative cycle is among them, it reports NEGATIVE-CYCLE; negative cycles that $s$ does not reach are ignored. Otherwise it returns the distances, with $+\infty$ for vertices that $s$ does not reach. With no negative weight at all there is nothing to scale, and the algorithm is a single run of Dijkstra's algorithm.

## The algorithm

For a potential $p$, the reduced cost of an edge is $c(u, v) = w'(u, v) + p(u) - p(v)$ for the current scaled weight $w'$. An edge is *admissible* if $c \le 0$, and a vertex is *improvable* if it has an incoming edge with $c = -1$. The *admissible graph* has the admissible edges.

```pseudo id=main
GOLDBERG-SCALING(G, w, s)
L1  keep the vertices reachable from s; b ← number of bits of N; p ← 0
L2  for i ← 1 to b do
L3      p ← 2p; w'(e) ← ⌈w(e) / 2^(b−i)⌉; now c(u, v) = w'(u, v) + p(u) − p(v) ≥ −1
L4      while some vertex is improvable (say k of them) do
L5          contract the strongly connected components of the admissible graph; if one contains a −1 edge, return NEGATIVE-CYCLE
L6          d(v) ← least cost of an admissible path ending at v (0 or less), on the contracted DAG
L7          if some level j has ≥ √k improvable vertices with d(v) = j: p(v) ← p(v) − 1 for all v with d(v) ≤ j
L8          else: take an admissible path to a vertex with the least d; let x_1, …, x_L be the heads of its −1 edges, in order
L9              D(v) ← min(0, min_j (dist⁺(x_j, v) − j)) with lengths max(c, 0), by Dial's buckets; p ← p + D
L10             if some x_j is still improvable, return NEGATIVE-CYCLE
L11 return the distances from s by Dijkstra with lengths w(u, v) + p(u) − p(v) ≥ 0, plus p(v) − p(s)
```

Line L3 rounds up, so that $\lceil w / 2^{b-i} \rceil \ge 2 \lceil w / 2^{b-i+1} \rceil - 1$ keeps reduced costs at least $-1$ after doubling. Line L5 uses [strongly connected components](/strongly-connected-components/): inside a component every admissible edge has cost 0 unless there is a negative cycle, so the components can be merged and the admissible graph becomes a DAG, where line L6 is a [DAG shortest-path](/dag-shortest-paths/) pass with costs 0 and $-1$. Line L7 is a *cut-relabel*: the set $\{v : d(v) \le j\}$ has no admissible edge leaving it, so lowering it by 1 makes every edge entering it one larger and every edge leaving it, which had cost at least 1, one smaller. Line L9 is the path step: $D$ lies between $-L$ and 0, so $L + 1$ buckets suffice.

## Example

The vertices are $s, a, b, c$ and the edges $s \to a$ ($-1$), $a \to b$ ($-3$), $a \to c$ (4). The most negative weight is $-3$, so $N = 3$ and $b = 2$ scales. The distances are $0, -1, -4, 3$.

**Scale 1.** The weights rounded up at half scale are $s \to a$: $\lceil -0.5 \rceil = 0$, $a \to b$: $\lceil -1.5 \rceil = -1$, $a \to c$: 2. With $p = 0$, only $b$ is improvable, $k = 1$. The admissible edges are $s \to a$ and $a \to b$, the levels are $d = (0, 0, -1, 0)$, and level $-1$ holds one improvable vertex, $1 \ge \sqrt 1$. The cut lowers $p(b)$ to $-1$, and now $a \to b$ costs $-1 + 0 + 1 = 0$. No vertex is improvable.

**Scale 2.** Doubling gives $p = (0, 0, -2, 0)$ for $s, a, b, c$. With the full weights, $c(s, a) = -1$, $c(a, b) = -3 + 0 + 2 = -1$ and $c(a, c) = 4$, so $a$ and $b$ are improvable, $k = 2$. The levels are $d(a) = -1$ and $d(b) = -2$: each level has one improvable vertex, fewer than $\sqrt 2$, so line L8 takes the path $s, a, b$ with $x_1 = a$, $x_2 = b$. The sweep gives $D = (0, -1, -2, 0)$; for example $c$ stays at 0 because $a \to c$ costs 4. Then $p = (0, -1, -4, 0)$ and the reduced costs are $s \to a$: 0, $a \to b$: 0, $a \to c$: 3. A single cut would not have done this: lowering $\{a, b\}$ would fix $a$ but leave $a \to b$ at $-1$.

**Last step.** Dijkstra with the reduced costs gives $0, 0, 0, 3$, and adding $p(v) - p(s)$ gives $\delta = (0, -1, -4, 3)$.

**Negative cycle.** With $s \to a$ (1), $a \to b$ ($-2$), $b \to a$ (1), scale 1 cuts $\{b\}$. In scale 2, $p = (0, 0, -2)$ and $c(a, b) = 0$, $c(b, a) = -1$, so $a$ and $b$ form one admissible component containing a $-1$ edge, and line L5 reports the cycle $a, b, a$ of weight $-1$.

**Unreachable vertices.** With the extra edges $x \to y$ ($-5$) and $y \to x$ (1), a negative cycle that $s$ does not reach, line L1 drops $x$ and $y$; the answer is unchanged, with $\infty$ for both.

## Correctness

**Theorem.** The algorithm returns NEGATIVE-CYCLE exactly when a negative cycle is reachable from $s$. Otherwise it returns $\delta(s, v)$ for every $v$ and a shortest-path tree.

The proof keeps two invariants during scale $i$: every reduced cost is at least $-1$, and no step creates a new $-1$ edge. Line L3 starts with costs at least $-1$ because of the rounding. The cut of line L7 keeps both, since no admissible edge leaves the cut set, and it fixes every improvable vertex at level $j$, because a $-1$ edge into level $j$ comes from level $j + 1$ or above, outside the set. The path step keeps both because $D(v) \le D(u) + \max(c(u, v), 0)$ for every edge, and it fixes every $x_j$ unless a negative cycle exists: a $-1$ edge $(y, x_j)$ left unfixed would need a path from some $x_i$, $i \ge j$, to $y$ shorter than $i - j + 1$ under $\max(c, 0)$, and together with the path from $x_j$ to $x_i$ (cost $-(i - j)$) and the edge $(y, x_j)$ that is a cycle of negative cost. A reported cycle has negative scaled weight, and rounding up only increases weights, so it is negative for $w$. If no step reports, the loop of line L4 ends with all reduced costs nonnegative, and after the last scale Dijkstra's algorithm is correct on the reduced costs, which change the length of every $s$-$v$ path by the same $p(s) - p(v)$. If a negative cycle is reachable, no potential can make all its reduced costs nonnegative, so some step must report it. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/).

- **One iteration.** Lines L5 and L6 are a strongly connected components computation and a pass over the DAG, $O(n + m)$. Line L7 is $O(n)$. Line L9 is a bucket sweep with $L + 1 \le n$ buckets, $O(n + m)$. So one iteration of line L4 costs $O(n + m)$.
- **Iterations per scale.** Each iteration fixes at least $\sqrt k$ improvable vertices and creates none. In the path case the path has $L$ improvable vertices, at least the number of nonempty levels, which is at least $k / \sqrt k$. From $k$ improvable vertices, it takes at most $2\sqrt k$ iterations to halve $k$, so $O(\sqrt n)$ iterations per scale.
- **Total.** There are $b = O(\log N)$ scales, so the time is $O(\sqrt n\, (n + m) \log N)$, which is $O(\sqrt n\, m \log N)$ when every vertex is reachable from $s$. The final Dijkstra run adds $O(m + n \log n)$, which this dominates for $N \ge 2$.
- **Best case.** Without negative weights, the work is the reachability search and one Dijkstra run; on a graph whose Dijkstra run is linear, such as a path, the time is $\Theta(n + m)$.
- **Space.** Potentials, levels, components and buckets take $O(n + m)$.

## Properties

- **Weakly polynomial.** The bound depends on $\log N$; for small integer weights it beats Bellman-Ford's $O(nm)$ by a factor of about $\sqrt n$.
- **Potentials as certificates.** On success the final $p$ makes every reduced cost nonnegative, which certifies that no negative cycle is reachable; on failure the reported component or cycle is a certificate of a negative cycle.
- **No new bad edges.** Both steps only ever fix $-1$ edges; the number of improvable vertices never grows within a scale.
- **Integer weights only.** The bound $-1$ on reduced costs after doubling depends on rounding integers; real weights need other methods, such as [Bellman-Ford](/bellman-ford/).

## Variants and improvements

- **Negative-cycle detection.** Cherkassky and Goldberg (1999) studied the algorithm as a negative-cycle detector, next to label-correcting methods such as [Goldberg-Radzik](/goldberg-radzik/).
- **Earlier scaling bounds.** Gabow (1985) solved each scale in $O(n^{3/4} m)$, and Gabow and Tarjan (1989) reached $O(\sqrt n\, m \log(nN))$ through the assignment problem. Goldberg's bound removes the $\log n$ inside the logarithm and works on the graph directly.
- **Near-linear time.** Bernstein, Nanongkai and Wulff-Nilsen (2022) keep the outer scaling loop and replace the $O(\sqrt n\, m)$ step by a randomized $O(m \log^2 n)$ step built on low-diameter decompositions; see [near-linear negative SSSP](/near-linear-negative-sssp/).
- **Cost scaling for flows.** The same scaling with potentials, and admissible graphs, drives [cost scaling](/cost-scaling/) for minimum-cost flow.

## When to use it

Use it for integer weights when the worst case matters, for example for feasibility of [difference constraints](/difference-constraints/) with small integer bounds, or as the potential-finding step of [Johnson's algorithm](/johnson/). For real weights, or when inputs are easy, label-correcting methods such as Goldberg-Radzik are simpler and usually fast. With nonnegative weights, use Dijkstra's algorithm directly.

## Pitfalls

- **Rounding down.** With $\lfloor \cdot \rfloor$ instead of $\lceil \cdot \rceil$, doubled potentials can leave reduced costs of $-2$, and the refinement does not apply.
- **Cutting several levels at once.** After one cut, the sets $\{v : d(v) \le j'\}$ for other levels need not be closed any more. Use one cut per iteration, or the path step, which is the correct way to handle many levels together.
- **Ignoring zero-cost cycles.** The admissible graph is a DAG only after its strongly connected components are contracted. Running the level computation on the raw admissible graph loops or gives wrong levels.
- **Unreachable vertices.** A negative cycle that $s$ does not reach would make the refinement fail. Restrict to the vertices reachable from $s$ before scaling.

## Implementations

The Python version restricts the graph to the vertices reachable from $s$, runs the scales with rounded-up weights, and in each refinement iteration computes the components of the admissible graph with an iterative Tarjan search, the levels on the contracted DAG, and then either a cut or the path step with a bucket sweep. It finishes with Dijkstra's algorithm on the reduced costs and can record each step as (scale, case, number of vertices fixed).

## History

Gabow (1985) introduced bit scaling for shortest paths, with $O(n^{3/4} m \log N)$ for negative weights, and Gabow and Tarjan (1989) improved this to $O(\sqrt n\, m \log(nN))$. Goldberg's algorithm, presented at SODA 1993 and published in the SIAM Journal on Computing in 1995, reached $O(\sqrt n\, m \log N)$ with a simpler, direct method. It stayed the best bound for integer weights for over 25 years, until Bernstein, Nanongkai and Wulff-Nilsen (2022) gave a near-linear algorithm.

## References
