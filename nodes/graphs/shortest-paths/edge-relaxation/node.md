---
tag: 81HHQ6
kind: concept
slug: edge-relaxation
name: Edge relaxation
aliases:
- relaxing an edge
area: graphs/shortest-paths
level: intro
summary: Updating a distance estimate d(v) using edge (u,v) if d(u)+w(u,v) is smaller than d(v).
prereqs: [shortest-path, weighted-graph, directed-graph]
see_also: [generic-shortest-path-algorithm, dijkstra, bellman-ford, dag-shortest-paths, single-source-shortest-paths, upper-bound-property, shortest-path-tree, negative-cycle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction (initialization and relaxation, and the list of the properties of shortest paths and relaxation), and Section 22.5 (proofs of these properties)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths, Section 8.3 (the generic algorithm that relaxes tense edges)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.4, Shortest Paths (edge relaxation and vertex relaxation)
---

Edge relaxation is the basic step of almost every [single-source shortest-path](/single-source-shortest-paths/) algorithm: for an edge $(u, v)$ of a [weighted graph](/weighted-graph/), if the estimate $d[v]$ is larger than $d[u] + w(u, v)$, set $d[v]$ to $d[u] + w(u, v)$ and record $u$ as the predecessor of $v$. Each estimate is the length of some real path, so it never drops below the true distance, and it only goes down. [Dijkstra's algorithm](/dijkstra/), the [Bellman-Ford algorithm](/bellman-ford/) and [shortest paths in a DAG](/dag-shortest-paths/) differ only in the order in which they relax the edges.

## In plain words

You want the cheapest trip from home to each town. For each town you keep a note: "the best way I know costs this much, and its last road comes from that town". At the start, home costs nothing and every other town is "unknown".

Now take one road, from town A to town B. Ask: if I first go to A by my best known way and then take this road, is that cheaper than my note for B? If yes, write the new, smaller cost for B, with A as the town before B. That is one relaxation.

A note only goes down, and it always describes a real trip, so it is never below the true best cost. In a good order of roads, the notes reach the true costs quickly. If some loop of roads has a negative total, the notes can go down for ever.

## The idea

Let $G = (V, E)$ be a [directed graph](/directed-graph/) with a weight $w(u, v) \in \mathbb{R}$ on each edge and a source $s \in V$. Let $\delta(s, v)$ be the [shortest-path](/shortest-path/) distance: the infimum of the weights of the paths from $s$ to $v$. It is $+\infty$ when no path exists, and $-\infty$ when a path from $s$ to $v$ can pass through a cycle of negative total weight.

**Weight assumptions.** Relaxation itself works for any real weights, negative ones included. The facts below about upper bounds and predecessors hold for any real weights. The facts about convergence need that no cycle of negative weight is reachable from $s$, because only then is each $\delta(s, v)$ finite or $+\infty$. Integer weights are not needed, but with integer weights each estimate stays an integer.

**State.** Each vertex $v$ has an estimate $d[v] \in \mathbb{R} \cup \{+\infty\}$ and a predecessor $\pi[v] \in V \cup \{\text{nil}\}$. The arithmetic uses $+\infty + x = +\infty$ for each finite $x$, also for negative $x$.

```pseudo id=relax
INITIALIZE-SINGLE-SOURCE(G, s)
L1  for each v in V do
L2      d[v] ← ∞, π[v] ← nil
L3  d[s] ← 0

RELAX(u, v, w)
L4  if d[u] + w(u, v) < d[v] then
L5      d[v] ← d[u] + w(u, v)
L6      π[v] ← u
```

An edge with $d[u] + w(u, v) < d[v]$ is called *tense*. Relaxing a tense edge is the only way the estimates change. Relaxing an edge that is not tense does nothing. So after any sequence of relaxations each $d[v]$ is the minimum over time of the values it has had.

### The properties of relaxation

Assume that the estimates start with INITIALIZE-SINGLE-SOURCE and change only by RELAX. CLRS lists these properties at the start of Chapter 22 and proves them in Section 22.5.

1. **Each finite estimate is the length of a walk.** If $d[v] < \infty$, then there is a walk from $s$ to $v$ of weight exactly $d[v]$. *Proof.* By induction on the number of relaxations. At the start only $d[s] = 0$ is finite, the weight of the empty walk. When line L5 sets $d[v] = d[u] + w(u, v)$, the value $d[u]$ is finite, so by the hypothesis a walk from $s$ to $u$ of weight $d[u]$ exists. Add the edge $(u, v)$ to it. $\square$
2. **Upper-bound property.** $d[v] \ge \delta(s, v)$ at all times, for all $v$. *Proof.* If $d[v] = \infty$ there is nothing to show. Else by property 1, $d[v]$ is the weight of a walk from $s$ to $v$, and $\delta(s, v)$ is at most the weight of each such walk. $\square$ Since $d[v]$ never increases, once $d[v] = \delta(s, v)$ it never changes again. The page [upper-bound property](/upper-bound-property/) treats this fact on its own.
3. **No-path property.** If no path from $s$ to $v$ exists, then $d[v] = \infty$ at all times. This follows from property 1.
4. **Triangle inequality after relaxation.** Just after RELAX$(u, v, w)$, $d[v] \le d[u] + w(u, v)$. Line L4 either finds this true or makes it an equality. Later, $d[v]$ can only go down; $d[u]$ can go down too, so the edge can become tense again.
5. **Convergence property.** Let $s \leadsto u \to v$ be a shortest path to $v$. If $d[u] = \delta(s, u)$ at some time before RELAX$(u, v, w)$, then $d[v] = \delta(s, v)$ at all times after it. *Proof.* Just after the call, $d[v] \le d[u] + w(u, v) = \delta(s, u) + w(u, v) = \delta(s, v)$, because a prefix of a shortest path is a shortest path. With property 2, $d[v] = \delta(s, v)$, and it stays so. $\square$
6. **Path-relaxation property.** Assume that no negative cycle is reachable from $s$. Let $p = \langle v_0, v_1, \ldots, v_k \rangle$ be a shortest path with $v_0 = s$. If the edges $(v_0, v_1), (v_1, v_2), \ldots, (v_{k-1}, v_k)$ are relaxed in this order, with any other relaxations in between, then afterwards $d[v_k] = \delta(s, v_k)$. *Proof.* By induction on $i$: after the relaxation of $(v_{i-1}, v_i)$, $d[v_i] = \delta(s, v_i)$. For $i = 0$, $d[s] = 0$ from the start, and $d[s]$ never drops below $\delta(s, s) = 0$ by property 2 (here we use that there is no negative cycle through $s$). The step from $i - 1$ to $i$ is property 5, because each prefix $\langle v_0, \ldots, v_i \rangle$ of $p$ is a shortest path. $\square$
7. **Predecessor-subgraph property.** Assume that no negative cycle is reachable from $s$. Once $d[v] = \delta(s, v)$ for all $v$, the edges $(\pi[v], v)$ form a [shortest-path tree](/shortest-path-tree/) rooted at $s$. CLRS proves this in Section 22.5, together with the fact that the predecessor graph has no cycle while no negative cycle is reachable.

Property 6 is the reason for the different algorithms. Each shortest path has at most $n - 1$ edges when no negative cycle exists. The [Bellman-Ford algorithm](/bellman-ford/) relaxes all edges $n - 1$ times, so each path appears in order inside the sequence. [Shortest paths in a DAG](/dag-shortest-paths/) relax the edges in a topological order, so each path appears in order in one pass. [Dijkstra's algorithm](/dijkstra/) relaxes the edges out of each vertex at the moment its estimate is final, which needs nonnegative weights.

### Relaxation and negative cycles

If a cycle $C$ of negative weight is reachable from $s$, then some edge is tense after any finite sequence of relaxations. *Proof.* Fix a path $P$ from $s$ to a vertex of $C$. If some vertex of $P$ or of $C$ has $d = \infty$, walk along $P$ and then around $C$ from $s$, whose estimate is $0$. The first vertex with $d = \infty$ is entered by an edge $(u, v)$ with $d[u]$ finite, and this edge is tense. Otherwise all estimates on $C = \langle v_0, \ldots, v_k = v_0 \rangle$ are finite. Assume that no edge of $C$ is tense. Then $d[v_i] \le d[v_{i-1}] + w(v_{i-1}, v_i)$ for each $i$. Add these $k$ inequalities. The sum of $d[v_i]$ is the same on both sides, so $0 \le w(C)$, which is false. $\square$ So "no edge is tense" is a certificate that no negative cycle is reachable, and [negative-cycle detection](/negative-cycle-detection/) is a check for a tense edge after enough rounds.

### Vertex relaxation

Some books relax a vertex: RELAX$(u)$ relaxes all edges out of $u$. Sedgewick and Wayne use this form. It is the same operation applied to a group of edges, and it is the natural unit when the graph is stored as an [adjacency list](/adjacency-list/).

## Examples

**One relaxation.** Let $d[u] = 5$, $d[v] = 9$ and $w(u, v) = 3$. Then $d[u] + w(u, v) = 8 < 9$, so RELAX sets $d[v] = 8$ and $\pi[v] = u$. If instead $w(u, v) = 4$, the sum is $9$, which is not less than $9$, so nothing changes. The strict test $<$ keeps the old predecessor on a tie.

**The order matters.** Take the vertices $s, a, b, c, t$ and the edges $s \to a$ (4), $s \to b$ (1), $b \to a$ (2), $a \to c$ (1), $b \to c$ (5), $c \to t$ (3). The distances are $\delta = (0, 3, 1, 4, 7)$ for $(s, a, b, c, t)$. A pass relaxes each edge once, in a fixed order.

In the order listed above, one pass is enough, because the order follows each shortest path:

| edge relaxed | $s\,a\,b\,c\,t$ after it |
|---|---|
| start | 0 ∞ ∞ ∞ ∞ |
| $s \to a$ | 0 4 ∞ ∞ ∞ |
| $s \to b$ | 0 4 1 ∞ ∞ |
| $b \to a$ | 0 3 1 ∞ ∞ |
| $a \to c$ | 0 3 1 4 ∞ |
| $b \to c$ | 0 3 1 4 ∞ (not tense) |
| $c \to t$ | 0 3 1 4 7 |

In the reverse order, the passes give:

| after pass | $s\,a\,b\,c\,t$ | changes in the pass |
|---|---|---|
| 1 | 0 4 1 ∞ ∞ | $b = 1$, $a = 4$ |
| 2 | 0 3 1 5 ∞ | $c = 6$, then $c = 5$, then $a = 3$ |
| 3 | 0 3 1 4 8 | $t = 8$, then $c = 4$ |
| 4 | 0 3 1 4 7 | $t = 7$ |
| 5 | 0 3 1 4 7 | none |

The shortest path $s \to b \to a \to c \to t$ has 4 edges, and in the reverse order each pass advances the correct value by one edge. This is the worst case of property 6, and it is why Bellman-Ford needs up to $n - 1$ passes.

**An unreachable vertex.** Add a vertex $z$ with one edge $z \to t$ of weight $-10$ and no edge into $z$. Then $d[z] = \infty$ for ever. Relaxing $z \to t$ tests $\infty + (-10) < d[t]$, and $\infty + (-10) = \infty$, so nothing changes. A program that stores $\infty$ as a large integer must test $d[u] = \infty$ before the addition: with $\infty$ stored as $2^{63} - 1$, the sum $2^{63} - 11$ is smaller than "infinity" and would wrongly make $d[t]$ finite.

**A negative cycle.** Take $s \to x$ (1), $x \to y$ (2), $y \to x$ ($-3$). The cycle $x \to y \to x$ has weight $-1$. Relaxing $s \to x$, then $x \to y$ and $y \to x$ again and again gives $d[x] = 1, 0, -1, -2, \ldots$ and $d[y] = 3, 2, 1, \ldots$. The estimates go down by $1$ for each turn of the cycle and never stop, as the proof above shows. Here $\delta(s, x) = \delta(s, y) = -\infty$.

## Where it is used

- The [generic shortest-path algorithm](/generic-shortest-path-algorithm/) relaxes tense edges in any order until none is left. All the algorithms below are special orders of it.
- The [Bellman-Ford algorithm](/bellman-ford/) and its queue form [SPFA](/spfa/) relax in rounds and allow negative weights.
- [Dijkstra's algorithm](/dijkstra/), [Dial's algorithm](/dial-algorithm/) and [A* search](/a-star-search/) relax the edges out of the vertex with the least key, and need nonnegative (reduced) weights.
- [Shortest paths in a DAG](/dag-shortest-paths/) relax in a [topological order](/topological-sort/).
- The [Floyd-Warshall algorithm](/floyd-warshall/) relaxes the pair $(i, j)$ through an intermediate vertex $k$: $D[i][j] \leftarrow \min(D[i][j], D[i][k] + D[k][j])$, the same step on a matrix of estimates.
- [Johnson's algorithm](/johnson/) and [reduced costs](/potential-function-reduced-costs/) use a potential that has no tense edge, so that all reduced weights are nonnegative.
- In [difference constraints](/difference-constraints/), a tense edge is a violated constraint $x_v - x_u \le w(u, v)$, and relaxation repairs it.

## References
