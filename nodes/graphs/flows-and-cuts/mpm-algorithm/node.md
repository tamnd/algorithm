---
tag: QQPNK1
kind: algorithm
slug: mpm-algorithm
name: Malhotra-Pramodh Kumar-Maheshwari algorithm
aliases:
- MPM algorithm
area: graphs/flows-and-cuts
level: advanced
summary: Maximum flow algorithm that builds a layered network and repeatedly pushes flow through the vertex of least potential, running in O(V^3).
solves: [max-flow-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^3)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [dinic, level-graph, blocking-flow, residual-graph]
see_also: [push-relabel, edmonds-karp, ford-fulkerson, max-flow-min-cut-theorem, min-cut-problem, dynamic-tree, breadth-first-search]
sources:
  - paper: doi:10.1016/0020-0190(78)90016-9
    title: V. M. Malhotra, M. Pramodh Kumar and S. N. Maheshwari, An O(|V|^3) algorithm for finding maximum flows in networks, Information Processing Letters 7(6), 277 to 278 (1978)
    locator: the whole paper (the throughput of a vertex, the push and pull from the vertex of least throughput, and the O(|V|^3) bound)
  - paper: doi:10.1007/11685654_10
    title: Yefim Dinitz, Dinitz' algorithm, the original version and Even's version, in Theoretical Computer Science, Essays in Memory of Shimon Even, LNCS 3895, 218 to 240 (2006)
    locator: the whole chapter (layered networks and blocking flows, the setting in which MPM finds its blocking flow)
---

The Malhotra-Pramodh Kumar-Maheshwari (MPM) algorithm computes a [maximum flow](/max-flow-problem/) in $O(n^3)$ time. It follows [Dinic's algorithm](/dinic/): each phase builds the [level graph](/level-graph/) of the [residual graph](/residual-graph/) and finds a [blocking flow](/blocking-flow/) in it, and there are at most $n - 1$ phases. The difference is how the blocking flow is found. MPM gives each vertex a *potential*, the least of the capacity that can enter it and the capacity that can leave it, and repeatedly takes the vertex of least potential, pushes that much flow from it forward to the sink and pulls the same amount back from the source, layer by layer. The vertex is then saturated and leaves the level graph. This gives a blocking flow in $O(n^2)$ time, without the [dynamic trees](/dynamic-tree/) that other $O(n^2)$ methods need.

## In plain words

Picture a network drawn in rows: the source in the first row, then everything one step away, then two steps, and so on, with pipes only from one row to the next. Each junction has a limit, the smaller of what its incoming pipes and its outgoing pipes can carry.

Find the junction with the smallest limit. Because every other junction can handle at least that much, you can push that amount from it down to the drain, row by row, and pull the same amount up from the source, row by row, without getting stuck. That junction is now full and you can forget it. Repeat until no route is left in the rows, then redraw the rows and start again.

## The problem

The input is a [flow network](/flow-network/): a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, capacities $c(e) \ge 0$, integer or real, and a source $s \ne t$. Parallel edges, antiparallel edges, self-loops and edges of capacity 0 are allowed. Each edge gets its own residual pair, so two antiparallel edges are two separate pairs and are never merged; a self-loop never lies on a shortest path and carries 0. The output is a maximum flow, its value, and the source side of a [minimum cut](/min-cut-problem/). If $t$ is not reachable from $s$, the answer is the zero flow, found with no phase.

## The algorithm

In the level graph $L$ of the current residual graph, $\mathrm{in}(v)$ is the total residual capacity of the edges of $L$ that enter $v$, and $\mathrm{out}(v)$ of those that leave it. The *potential* is $p(v) = \min(\mathrm{in}(v), \mathrm{out}(v))$, with $p(s) = \mathrm{out}(s)$ and $p(t) = \mathrm{in}(t)$.

```pseudo id=main
MPM(G, c, s, t)
L1  f ← 0
L2  while t is reachable from s in the residual graph G_f do
L3      L ← the level graph of G_f; delete from L every vertex other than s that has no entering edge, and other than t that has no leaving edge, repeatedly
L4      while s and t are both in L do
L5          v ← a vertex of L with the least potential p(v)
L6          d ← p(v)
L7          push d units from v toward t, layer by layer: each vertex sends its excess along its leaving edges of L, in order, saturating all but the last
L8          pull d units into v from s, layer by layer, in the same way along entering edges
L9          add the d units to f; delete v, the saturated edges, and, repeatedly, every vertex that has lost all its entering or all its leaving edges
L10 return f and the set of vertices that s reaches in G_f
```

Each vertex of $L$ keeps a pointer into its list of leaving edges and another into its list of entering edges. A saturated edge is skipped for good, so each edge is saturated at most once per phase. Line L9 also deletes $s$ when $\mathrm{out}(s)$ falls to 0, and $t$ when $\mathrm{in}(t)$ does, which ends the phase.

## Example

The network has the edges $s \to a$ (10), $s \to b$ (10), $a \to b$ (2), $a \to c$ (4), $a \to d$ (8), $b \to d$ (9), $d \to c$ (6), $c \to t$ (10), $d \to t$ (10). The maximum flow is 19.

**Phase 1.** The levels are $s$: 0, $a, b$: 1, $c, d$: 2, $t$: 3. The edges $a \to b$ and $d \to c$ join vertices of the same level, so they are not in $L$.

| step | potentials | chosen $v$, $d$ | push and pull | deleted |
|---|---|---|---|---|
| 1 | $s$ 20, $a$ 10, $b$ 9, $c$ 4, $d$ 10, $t$ 20 | $c$, 4 | $c \to t$; $a \to c$, $s \to a$ | $c$ |
| 2 | $s$ 16, $a$ 6, $b$ 9, $d$ 10, $t$ 10 | $a$, 6 | $a \to d$, $d \to t$; $s \to a$ | $a$ |
| 3 | $s$ 10, $b$ 9, $d$ 4, $t$ 4 | $d$, 4 | $d \to t$; $b \to d$, $s \to b$ | $d$, $t$ |

The blocking flow has value 14. After step 3, $\mathrm{in}(t) = 0$, so $t$ is deleted and the phase ends.

**Phase 2.** In the new residual graph, the shortest path is $s, b, d, c, t$, of length 4: $s \to b$ has 6 left, $b \to d$ 5, $d \to c$ 6, $c \to t$ 6. The vertex $a$ is reached at level 3 through the reverse of $a \to d$, but it has no edge to level 4, so line L3 deletes it. The potentials are $s$ 6, $b$ 5, $c$ 6, $d$ 5, $t$ 6; the vertex $b$ is chosen with $d = 5$, and 5 units go along the path.

**Phase 3.** The residual graph has $s \to b$ with 1 unit left and $b \to d$ saturated, and $s \to a$ is saturated, so $s$ reaches only $\{s, b\}$. The value is $14 + 5 = 19$, and $\{s, b\}$ is a minimum cut, of capacity $10 + 9 = 19$.

Edge cases. An edge of capacity 0 has no residual capacity and never enters $L$. If $t$ is not reachable, line L2 stops at once and returns the zero flow and the set of vertices that $s$ reaches.

## Correctness

Within a phase, let $v$ be the chosen vertex. Every vertex $u$ of $L$ has $p(u) \ge d$. In the push of line L7, the excess at one layer adds up to at most $d$, because it all came from $v$, so each vertex $u$ with excess $x \le d \le \mathrm{out}(u)$ can send it all along its leaving edges, and the excess reaches $t$. The pull is symmetric. So the push and the pull add $d$ to the flow and keep capacity and conservation. After them, $p(v) = 0$, so $v$ is no longer on any $s$-$t$ path in $L$ and can be deleted, and the same holds for the vertices deleted at line L9. When $s$ or $t$ is deleted, every $s$-$t$ path of $L$ has a saturated edge or a deleted vertex, so the flow of the phase is blocking. The rest is the argument of Dinic's algorithm: after a blocking flow, the distance from $s$ to $t$ in the residual graph grows, so there are at most $n - 1$ phases, and at the end, the max-flow min-cut theorem shows that the flow is maximum. The proof file below gives each step.

## Complexity

The model is the [word RAM](/word-ram/); additions and comparisons of capacities take constant time.

- **Building $L$.** One [breadth-first search](/breadth-first-search/) and one pass over the edges: $O(n + m)$ per phase.
- **Steps per phase.** Each step deletes the chosen vertex, so there are at most $n$ steps. Finding the least potential by a scan is $O(n)$ per step, $O(n^2)$ per phase.
- **Pushes per phase.** Every push either saturates an edge, which then leaves $L$ for the phase, at most $m$ in all, or is the last push of a vertex in that step, at most $n$ per step. So $O(m + n^2)$ pushes per phase.
- **Deletions.** Each vertex and each edge is deleted at most once per phase: $O(n + m)$.
- **Total.** At most $n - 1$ phases of $O(n^2 + m) = O(n^2)$ each: $O(n^3)$ worst case. Space is $\Theta(n + m)$.

## Properties

- **Deterministic and strongly polynomial.** The bound does not depend on the capacities, so real capacities are fine.
- **Integrality.** With integer capacities, every potential and every push is an integer, so the flow is integral.
- **Simple data structures.** Only arrays and edge pointers; the $O(n^2)$ blocking flow needs no dynamic trees.
- **Layered.** Like Dinic's algorithm, it works on unit networks with the same phase bounds, $O(\sqrt{n})$ phases on unit-capacity graphs with unit vertex capacities.

## Variants and improvements

- **Dinic with dynamic trees.** Sleator and Tarjan's [dynamic trees](/dynamic-tree/) give a blocking flow in $O(m \log n)$, for $O(nm \log n)$ overall, which is better on sparse graphs.
- **Karzanov's preflows.** Karzanov found the first $O(n^2)$ blocking flow method, using preflows inside the level graph; MPM reaches the same bound with a simpler rule.
- **Push-relabel.** [Push-relabel](/push-relabel/) drops the phase structure and reaches $O(n^3)$ with a FIFO queue, $O(n^2 \sqrt{m})$ with the highest-label rule, and is usually faster in practice.
- **Heaps for the minimum.** Keeping potentials in a heap does not change the bound, since the pushes already cost $O(n^2)$ per phase.

## When to use it

Use it when an $O(n^3)$ maximum flow with a short proof is wanted, for dense graphs, or for teaching the idea of a blocking flow found by potentials. In practice, push-relabel with heuristics or Dinic's algorithm is usually faster, and on sparse graphs the $O(nm)$ algorithms are better.

## Pitfalls

- **Starting from a vertex whose potential is not the least.** The push can then get stuck, because some vertex on the way cannot pass on its excess.
- **Pushing depth first.** The push must go layer by layer, so that all excess of a vertex is collected before it sends; sending piecemeal works too, but each vertex must still send at most one partial push per step for the bound.
- **Keeping edges inside a layer.** Edges between vertices of the same level, or going back a level, are not in $L$; using them breaks the distance argument.
- **Forgetting to update the neighbors after a deletion.** When a vertex is deleted, its edges no longer count toward the in and out capacities of its neighbors, which may make more vertices dead ends.
- **Merging antiparallel edges.** Each edge needs its own reverse residual edge; folding $u \to v$ and $v \to u$ into one pair is possible but must be done consistently.

## Implementations

## History

Dinitz introduced layered networks and blocking flows in 1970, and Karzanov gave an $O(n^3)$ algorithm with preflows in 1974. Malhotra, Pramodh Kumar and Maheshwari published their simpler $O(n^3)$ method, based on the throughput of vertices, in Information Processing Letters in 1978.

## References
