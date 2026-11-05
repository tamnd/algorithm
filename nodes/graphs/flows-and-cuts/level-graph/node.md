---
tag: VBVNFT
kind: concept
slug: level-graph
name: Level graph
aliases:
- layered network
area: graphs/flows-and-cuts
level: core
summary: Subgraph of the residual graph keeping only edges that increase BFS distance by one.
prereqs: [residual-graph, breadth-first-search, bfs-layers]
see_also: [blocking-flow, dinic, mpm-algorithm, edmonds-karp, hopcroft-karp, push-relabel, augmenting-path-flow]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (Dinitz's layered residual graph and blocking flows)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (layered networks and Dinic's algorithm)
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms
    locator: Chapter 8, Network Flows (the level graph and blocking flows)
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert Endre Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: the whole paper (layered networks with unit capacities and the O(m^(1/2)) and O(n^(2/3)) phase bounds)
---

The level graph of a [residual graph](/residual-graph/) $G_f$ keeps the vertices that the source $s$ reaches and only those residual edges $(u, v)$ with $d(v) = d(u) + 1$, where $d$ is the [breadth-first](/breadth-first-search/) distance from $s$ in $G_f$. Its $s$-$t$ paths are exactly the shortest augmenting paths, and after a [blocking flow](/blocking-flow/) in it is added to $f$, the distance from $s$ to $t$ grows by at least one. This is the phase structure of [Dinic's algorithm](/dinic/), of the [MPM algorithm](/mpm-algorithm/) and of [Hopcroft-Karp](/hopcroft-karp/).

## In plain words

Start at the source and sort every reachable point into rings: the source alone, the points one step away, the points two steps away, and so on. Now keep only the links that go from one ring to the very next ring outward. Links inside a ring, and links that step back toward the source, are thrown away.

What is left is a map in which every route from the source to the target is as short as possible, and every route only moves outward. Pushing goods along this map cannot loop back. When every outward route is blocked, the target can no longer be reached in the old number of steps, so the next map has more rings.

## The idea

**Setting.** $G = (V, E)$ is a directed graph with capacities $c : E \to \mathbb{R}_{\ge 0}$ (real; the definition does not need integers), a source $s$ and a sink $t \ne s$, and $f$ is an [$s$-$t$ flow](/s-t-flow/). The residual graph $G_f$ has, for each edge $e = (u, v)$, a forward edge $(u, v)$ of capacity $c(e) - f(e)$ and a backward edge $(v, u)$ of capacity $f(e)$, and only edges of positive residual capacity are kept. Antiparallel edges $(u, v)$ and $(v, u)$ of $G$ give four separate residual edges; they are not merged. An edge of capacity 0 that carries no flow has no residual edge at all.

**Definition.** Let $d(v)$ be the number of edges on a shortest $s$-$v$ path in $G_f$, and $d(v) = \infty$ if $s$ does not reach $v$. The level graph is $L_f = (V_L, E_L)$ with

$$V_L = \{ v : d(v) < \infty \}, \qquad E_L = \{ (u, v) \in E(G_f) : u \in V_L,\ d(v) = d(u) + 1 \},$$

each edge with its residual capacity. The set $\{ v : d(v) = i \}$ is level $i$; these are the [BFS layers](/bfs-layers/) of $G_f$. One breadth-first search builds $L_f$ in $O(n + m)$ time. Many implementations also drop the vertices with $d(v) \ge d(t)$ other than $t$, which cannot lie on a shortest $s$-$t$ path.

**Lemma 1 (shortest paths live in $L_f$).** An $s$-$t$ path in $G_f$ is a shortest one if and only if it is a path in $L_f$. *Proof.* Each edge $(u, v)$ of $G_f$ has $d(v) \le d(u) + 1$. Along a path $s = v_0, v_1, \ldots, v_k = t$, $d(t) = \sum_{i} (d(v_{i}) - d(v_{i-1})) \le k$, with equality exactly when every step raises $d$ by one, that is, when every edge is in $E_L$. $\square$

So $L_f$ is acyclic, it holds every shortest augmenting path, and it holds no other $s$-$t$ path.

**Lemma 2 (distances do not drop).** Let $g$ be a flow in the network $L_f$, and let $f' = f + g$, where flow on a backward residual edge cancels flow on the original edge. Let $d'$ be the distances in $G_{f'}$. Then $d'(v) \ge d(v)$ for every $v$, and if $g$ is a blocking flow of $L_f$, then $d'(t) > d(t)$. *Proof.* An edge of $G_{f'}$ is either an edge of $G_f$, so $d(\text{head}) \le d(\text{tail}) + 1$, or the reverse of an edge $(u, v)$ of $L_f$ that carries flow in $g$, which goes from $v$ to $u$ with $d(u) = d(v) - 1$. So every edge of $G_{f'}$ raises $d$ by at most one, and as in Lemma 1, every $s$-$v$ path in $G_{f'}$ has at least $d(v)$ edges. If an $s$-$t$ path in $G_{f'}$ had exactly $d(t)$ edges, every step would raise $d$ by exactly one; such an edge is not a reversed edge, so it is an edge of $L_f$ that still has residual capacity after $g$. That path would then be an $s$-$t$ path of $L_f$ on which $g$ saturates no edge, which a blocking flow does not allow. $\square$

**Number of phases.** If $t \in V_L$, then $1 \le d(t) \le n - 1$. Lemma 2 makes $d(t)$ grow in every phase that adds a blocking flow, so after at most $n - 1$ phases $t$ is unreachable and $f$ is a maximum flow by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

**No $s$-$t$ path.** If $t \notin V_L$, the level graph has no $s$-$t$ path. This is the stopping test of Dinic's algorithm, and $V_L$ is then the source side of a [minimum cut](/min-cut-problem/).

## Examples

The network has the edges $s \to a$ (10), $s \to b$ (10), $a \to b$ (2), $a \to c$ (4), $a \to d$ (8), $b \to d$ (9), $d \to c$ (6), $c \to t$ (10), $d \to t$ (10). Its maximum flow is 19.

**Phase 1, zero flow.** The residual graph is $G$ itself, since no edge carries flow and every backward edge has capacity 0. The levels are $\{s\}$, $\{a, b\}$, $\{c, d\}$, $\{t\}$.

| edge | levels | in $L_f$? |
|---|---|---|
| $s \to a$, $s \to b$ | $0 \to 1$ | yes |
| $a \to c$, $a \to d$, $b \to d$ | $1 \to 2$ | yes |
| $c \to t$, $d \to t$ | $2 \to 3$ | yes |
| $a \to b$ | $1 \to 1$ | no |
| $d \to c$ | $2 \to 2$ | no |

A blocking flow of $L_f$ sends 4 along $s, a, c, t$, 6 along $s, a, d, t$ and 4 along $s, b, d, t$, of value 14. It saturates $s \to a$, $a \to c$ and $d \to t$, so every $s$-$t$ path of $L_f$ is blocked, although 14 is not the maximum.

**Phase 2.** Now the residual edges include $s \to b$ (6), $b \to d$ (5), $d \to c$ (6), $c \to t$ (6), $a \to d$ (2), $a \to b$ (2), and the backward edges $d \to a$ (6), $c \to a$ (4), $b \to s$ (4) and others. The levels are $\{s\}$, $\{b\}$, $\{d\}$, $\{a, c\}$, $\{t\}$, so $d(t)$ went from 3 to 4. The level graph has the edges $s \to b$, $b \to d$, $d \to c$, $d \to a$ (a backward edge) and $c \to t$. The edge $d \to c$, excluded in phase 1, is now needed. The only $s$-$t$ path is $s, b, d, c, t$ with bottleneck 5, which brings the flow to 19. In phase 3, $s$ reaches only $\{s, b\}$, the minimum cut.

**A zero-capacity edge.** Add $s \to t$ of capacity 0. It has no residual edge, so it is not in any level graph, and $d(t)$ is still 3 in phase 1.

**Antiparallel edges.** Add $b \to a$ of capacity 5. At zero flow both $a \to b$ and $b \to a$ join levels 1 and 1 and are left out. They stay separate residual edges in later phases, and here the maximum flow becomes 20.

**No $s$-$t$ path.** With only $s \to a$ (3) and $b \to t$ (3), $V_L = \{s, a\}$, the level graph has no $s$-$t$ path, and the maximum flow is 0.

## Where it is used

- **[Dinic's algorithm](/dinic/)** repeats: build $L_f$, find a blocking flow in it, add it. With a depth-first search that deletes dead ends, a blocking flow takes $O(nm)$, so the total is $O(n^2 m)$; with [dynamic trees](/dynamic-tree/) it is $O(nm \log n)$.
- **The [MPM algorithm](/mpm-algorithm/)** finds a blocking flow of $L_f$ in $O(n^2)$ by pushing from the vertex of least throughput, for $O(n^3)$ in total.
- **Unit capacities.** Even and Tarjan showed that with unit capacities at most $O(\min(m^{1/2}, n^{2/3}))$ phases are needed; on bipartite matching networks this is [Hopcroft-Karp](/hopcroft-karp/) with $O(\sqrt{n})$ phases.
- **[Edmonds-Karp](/edmonds-karp/)** uses one shortest path at a time, which is a path in $L_f$; Lemma 2 is its monotone distance lemma.
- **[Push-relabel](/push-relabel/)** keeps distance labels that bound the true residual distance to $t$, a lazy form of the same levels taken from the sink side.

## References
