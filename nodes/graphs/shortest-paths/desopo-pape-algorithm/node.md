---
tag: 5Q4Y55
kind: algorithm
slug: desopo-pape-algorithm
name: D'Esopo-Pape algorithm
area: graphs/shortest-paths
level: core
summary: Single-source shortest path algorithm that uses a deque, inserting nodes at the front or back depending on whether they were seen before.
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: 2^Ω(n), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [generic-shortest-path-algorithm, edge-relaxation, deque]
see_also: [spfa, bellman-ford, dijkstra, zero-one-bfs, goldberg-radzik, negative-cycle-detection, tarjan-subtree-disassembly, single-source-shortest-paths]
sources:
  - paper: doi:10.1007/BF01585517
    title: U. Pape, Implementation and efficiency of Moore-algorithms for the shortest route problem, Mathematical Programming 7, 212 to 222 (1974)
    locator: the whole paper (the deque rule, credited to D'Esopo, and its running times on test networks)
  - paper: doi:10.1145/355900.355919
    title: U. Pape, Algorithm 562, Shortest path lengths, ACM Transactions on Mathematical Software 6(3), 450 to 455 (1980)
    locator: the whole paper (a published code of the deque method)
  - paper: doi:10.6028/jres.086.013
    title: Douglas R. Shier and Christoph Witzgall, Properties of labeling methods for determining shortest path trees, Journal of Research of the National Bureau of Standards 86(3), 317 to 330 (1981)
    locator: the analysis of the deque (Pape) rule, including graphs on which it takes exponential time
  - paper: doi:10.1002/net.3230110410
    title: Aaron Kershenbaum, A note on finding shortest path trees, Networks 11(4), 399 to 400 (1981)
    locator: the whole note (the exponential worst case of the deque method)
  - paper: doi:10.1002/net.3230090304
    title: Robert Dial, Fred Glover, David Karney and Darwin Klingman, A computational analysis of alternative algorithms and labeling techniques for finding shortest path trees, Networks 9(3), 215 to 248 (1979)
    locator: the computational comparison of label-correcting methods, including the deque method
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Section 5.4, Special implementations of the modified label-correcting algorithm (the dequeue implementation)
---

The D'Esopo-Pape algorithm is a label-correcting method for [single-source shortest paths](/single-source-shortest-paths/) that keeps the vertices to be scanned in a [deque](/deque/): a vertex whose label drops goes to the back the first time it enters the deque and to the front on every later entry. The rule is a heuristic: a vertex that was scanned before already passed its label on to its neighbors, so fixing it at once stops wrong labels from spreading. It allows negative weights, and on sparse road-like networks it is often faster than the [FIFO queue](/spfa/), but on some graphs it takes exponential time. The method is credited to D'Esopo and was published by Pape (1974).

## In plain words

You keep a line of places whose best known cost has just dropped and whose neighbors must be told. Take the place at the front of the line, tell each neighbor the new cost through it, and add any neighbor whose cost drops.

Where to add it depends on its past. A place that has never been in line joins at the back, like everyone else. A place that was in line before has already told its neighbors an old, worse cost. Those neighbors now hold numbers that are too high, so this place jumps to the front to correct them quickly.

When the line is empty, every cost is final. If some loop of roads has a negative total, costs would drop forever, so the method also counts how many roads each cost was built from and stops when that count gets too large.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices, $m$ edges, a real weight $w(u, v)$ on each edge, and a source $s$. The output is $\delta(s, v)$ for every $v$ with a [shortest-path tree](/shortest-path-tree/), or a report that a [negative cycle](/negative-cycle/) is reachable from $s$.

**Weight assumptions.** Weights are any real numbers, negative ones included, and need not be integers. If no negative cycle is reachable from $s$, the algorithm returns the distances, with $+\infty$ for vertices that $s$ does not reach. The plain method of Pape loops forever when a negative cycle is reachable; the version below adds a count of edges per label and returns NEGATIVE-CYCLE instead. A negative cycle that $s$ cannot reach has no effect.

## The algorithm

Each vertex has a state: NEVER (not yet in the deque), IN (in the deque), or LEFT (was in the deque, now out). The count $h[v]$ is the number of edges of the walk whose weight is $d[v]$.

```pseudo id=main
DESOPO-PAPE(G, w, s)
L1  for each v do d[v] ← ∞, π[v] ← nil, h[v] ← 0, state[v] ← NEVER
L2  d[s] ← 0; Q ← deque holding s; state[s] ← IN
L3  while Q is not empty do
L4      u ← remove the front of Q; state[u] ← LEFT
L5      for each edge (u, v) do
L6          if d[u] + w(u, v) < d[v] then
L7              d[v] ← d[u] + w(u, v); π[v] ← u; h[v] ← h[u] + 1; if h[v] ≥ n then return NEGATIVE-CYCLE
L8              if state[v] = NEVER then add v at the back of Q
L9              else if state[v] = LEFT then add v at the front of Q
                state[v] ← IN                           ▷ a vertex already in Q stays where it is
L10 return d, π
```

Lines L5 to L7 are ordinary [edge relaxation](/edge-relaxation/). Only lines L8 and L9 differ from [SPFA](/spfa/), which always adds at the back. A vertex already in the deque is not added again.

## Example

The vertices are $s, a, b, c, d$ and the edges $s \to a$ (2), $s \to b$ (6), $s \to c$ (7), $a \to b$ (3), $a \to d$ (8), $b \to d$ (1), $c \to a$ ($-6$). Labels are listed in the order $s, a, b, c, d$.

| scan | changes | deque after | labels after |
|---|---|---|---|
| $s$ | $a = 2$, $b = 6$, $c = 7$, all at the back | $a, b, c$ | 0 2 6 7 ∞ |
| $a$ | $b = 5$ (already in), $d = 10$ at the back | $b, c, d$ | 0 2 5 7 10 |
| $b$ | $d = 6$ (already in) | $c, d$ | 0 2 5 7 6 |
| $c$ | $a = 1$, at the **front**, since $a$ has left | $a, d$ | 0 1 5 7 6 |
| $a$ | $b = 4$, at the **front**, since $b$ has left | $b, d$ | 0 1 4 7 6 |
| $b$ | $d = 5$ (already in) | $d$ | 0 1 4 7 5 |
| $d$ | none | empty | 0 1 4 7 5 |

So $\delta = (0, 1, 4, 7, 5)$, and the shortest path to $d$ is $s \to c \to a \to b \to d$ with weight $7 - 6 + 3 + 1 = 5$. When $c$ lowers $a$, the front rule makes $a$ and then $b$ pass on their new labels before $d$ is scanned, so $d$ is scanned once. With a FIFO queue, $a$ would join behind $d$, and $d$ would be scanned twice.

**Unreachable.** A vertex $z$ with edges out of it but none into it keeps $d[z] = \infty$ and is never put in the deque.

**A negative cycle.** Add the edge $b \to a$ ($-4$). The cycle $a \to b \to a$ has weight $3 - 4 = -1$. The labels of $a$ and $b$ keep dropping as the two vertices push each other to the front, and the counts $h$ grow by one per round, until one reaches $n = 5$ and the algorithm returns NEGATIVE-CYCLE.

## Correctness

**Theorem.** The algorithm ends. It returns NEGATIVE-CYCLE if and only if a negative cycle is reachable from $s$; otherwise it returns $d[v] = \delta(s, v)$ for every $v$, and the predecessors form a shortest-path tree.

The argument is the one for every label-correcting method; the order of the deque plays no part. Each label $d[v] < \infty$ is the weight of a walk $W_v$ from $s$ with $h[v]$ edges, built when $d[v]$ was last set. If $W_v$ repeats a vertex $x$, the two visits of $x$ come from two settings of $d[x]$, the later one strictly smaller, so the closed part of $W_v$ between them has negative weight and contains a negative cycle reachable from $s$. Hence without such a cycle every $W_v$ is a simple path, $h[v] \le n - 1$, each label is one of finitely many path weights, labels only decrease, and the loop ends. Each scan clears the tense edges out of the scanned vertex, and an edge $(u, v)$ becomes tense again only when $d[u]$ drops, which puts $u$ back in the deque. So an empty deque means no tense edge, which gives $d[v] \le \delta(s, v)$ along a shortest path; with $d[v] \ge \delta(s, v)$ from the walks, $d = \delta$. If a negative cycle is reachable, an empty deque would mean no tense edge on that cycle, which is impossible, so the labels drop forever, the walks cannot all stay simple, and line L7 returns NEGATIVE-CYCLE. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Worst case.** Exponential. Shier and Witzgall (1981) and Kershenbaum (1981) give graphs with nonnegative weights on which the front rule makes some vertices be scanned exponentially often. The count in line L7 does not change this: it bounds the length of the walks behind the labels, not the number of times a label can drop. The only general bound is the number of simple paths from $s$.
- **Best case.** If each vertex is scanned once, for example when the graph is a tree directed away from $s$, the time is $\Theta(n + m)$.
- **Space.** The labels, predecessors, counts, states and the deque take $\Theta(n)$ extra space.
- **In practice.** The computational study of Dial, Glover, Karney and Klingman (1979) and Pape's own tests found the deque method among the fastest label-correcting codes on sparse transportation networks, where the bad cases do not arise.

## Properties

- **Negative weights.** Allowed, like [Bellman-Ford](/bellman-ford/); negative cycles are detected only with the count of line L7 or a similar check.
- **Label-correcting.** A vertex can be scanned many times, unlike [Dijkstra's algorithm](/dijkstra/), which scans each vertex once.
- **Not polynomial.** Unlike Bellman-Ford and SPFA, whose worst case is $O(nm)$, it has no polynomial bound.
- **Order-dependent.** The number of scans depends on the order of the adjacency lists, but the result does not.
- **Simple.** A deque and one state per vertex are all that is added to the generic method.

## Variants and improvements

- **[SPFA](/spfa/).** Always add at the back: a FIFO queue, with the $O(nm)$ bound of Bellman-Ford.
- **Threshold algorithm.** Glover, Glover and Klingman split the queue into two lists by a threshold on the labels, scanning the low list first; it shares the good practical behavior.
- **Small label first and large label last.** Heuristics that put a vertex at the front only if its label is below that of the current front, or move large labels to the back; both keep the deque idea and avoid some bad cases in practice.
- **[0-1 BFS](/zero-one-bfs/).** With weights 0 and 1 only, a deque with "0-edges to the front, 1-edges to the back" gives an exact $O(n + m)$ algorithm. It looks similar but the rule is based on the edge weight, not on the history of the vertex.
- **[Goldberg-Radzik](/goldberg-radzik/)** scans in topological order of the admissible graph and keeps the $O(nm)$ bound with good practical speed.
- **Negative cycle detection.** Instead of the counts, check the predecessor graph for a cycle from time to time, or use [subtree disassembly](/tarjan-subtree-disassembly/).

## When to use it

Use it only when the graphs are known to be sparse and road-like and practical speed matters more than a guarantee, for example in older transportation codes. For a guarantee with negative weights, use [Bellman-Ford](/bellman-ford/), [SPFA](/spfa/) or [Goldberg-Radzik](/goldberg-radzik/); with nonnegative weights, use [Dijkstra](/dijkstra/), whose worst case is far better and which is about as fast in practice.

## Pitfalls

- **Looping forever on a negative cycle.** Without the count of line L7 or another check, the algorithm never ends when a negative cycle is reachable.
- **Assuming a polynomial bound.** The front rule can make the running time exponential even with nonnegative weights. It is not a safe default for adversarial input.
- **Adding a vertex twice.** A vertex that is already in the deque must stay where it is; adding it again (at either end) breaks the analysis and wastes scans.
- **Confusing it with 0-1 BFS.** The deque rule here depends on whether the vertex was seen before, not on the weight of the edge, and it does not make the labels final when scanned.

## Implementations

The Python version keeps three states per vertex and the edge count of each label, and returns `None` as soon as a count reaches $n$.

## History

Pape (1974) published the deque rule, credited to D. A. D'Esopo, as a fast implementation of Moore's label-correcting method for road networks, and later gave a code for it (1980). Computational studies of the late 1970s, such as that of Dial, Glover, Karney and Klingman (1979), placed it among the best methods in practice. Shier and Witzgall (1981) and Kershenbaum (1981) showed that its worst case is exponential.

## References
