---
tag: W784DG
kind: algorithm
slug: spfa
name: Shortest Path Faster Algorithm
aliases:
- SPFA
- queue-based Bellman-Ford
- FIFO label-correcting algorithm
area: graphs/shortest-paths
level: core
summary: Bellman-Ford that re-relaxes only vertices whose distance changed, using a queue; fast on average, worst case O(nm).
solves: [single-source-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [bellman-ford, edge-relaxation, queue, single-source-shortest-paths]
see_also: [bellman-ford, desopo-pape-algorithm, tarjan-subtree-disassembly, generic-shortest-path-algorithm, negative-cycle-detection, dijkstra, upper-bound-property, shortest-path-optimality-conditions]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Label-correcting algorithms (the modified label-correcting algorithm with a list of vertices, and its FIFO implementation in O(nm) time)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms
    locator: Chapter 7, Shortest paths (the labeling method and the breadth-first scanning order, which gives O(nm))
  - paper: "Edward F. Moore, The shortest path through a maze, Proceedings of an International Symposium on the Theory of Switching, Harvard University Press, 1959, 285 to 292"
    locator: the queue-based method for shortest paths
  - paper: doi:10.1007/s101070050058
    title: Boris V. Cherkassky and Andrew V. Goldberg, Negative-cycle detection algorithms, Mathematical Programming 85(2), 277 to 311 (1999)
    locator: the sections on the Bellman-Ford-Moore algorithm with a FIFO queue and on cycle detection strategies
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.1, The Bellman-Ford algorithm (the pass structure that bounds the FIFO order)
---

SPFA solves the [single-source shortest-path problem](/single-source-shortest-paths/) with any real weights and reports a [negative cycle](/negative-cycle/) that the source can reach. It is [Bellman-Ford](/bellman-ford/) with a first-in first-out [queue](/queue/) of vertices whose label has changed: only the arcs out of these vertices can give an improvement, so only they are scanned again. The worst-case time is $O(nm)$, the same as Bellman-Ford, but on many graphs it scans each vertex only a few times. Moore described the method in 1959; the name SPFA comes from a 1994 paper by Duan Fanding.

## In plain words

Bellman-Ford checks every road again and again. Most of that work is useless: a road can only give a cheaper cost if the cost at its start place has just gone down.

SPFA keeps a line of places whose cost has gone down. It takes the first place in the line and checks only the roads that leave it. When a road gives a cheaper cost at its end place, that place joins the back of the line, unless it is already in it. When the line is empty, all costs are the cheapest ones.

To catch a loop of roads with a negative total, SPFA also counts the roads of the route behind each cost. A route with as many roads as there are places must visit some place twice, and the cost can only get that low through a loop with a negative total.

## The problem

The input is a directed graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, weights $w : E \to \mathbb{R}$ and a source $s$. The output is $\delta(s, v)$ for every $v$, with $\infty$ for the vertices that $s$ cannot reach, and a [shortest-path tree](/shortest-path-tree/) as parent pointers; or the report that a negative cycle is reachable from $s$.

**Weight assumptions.** Any real weights, negative ones included. Negative cycles that $s$ cannot reach do not matter, and the distances are still correct. Integer weights are not needed.

## The algorithm

```pseudo id=main
SPFA(G, w, s)
L1  for each v in V do d(v) ← ∞, π(v) ← nil, k(v) ← 0
L2  d(s) ← 0; Q ← a queue that holds only s
L3  while Q is not empty do
L4      u ← DEQUEUE(Q)
L5      for each arc (u, v) out of u do
L6          if d(u) + w(u, v) < d(v) then
L7              d(v) ← d(u) + w(u, v); π(v) ← u; k(v) ← k(u) + 1
L8              if k(v) ≥ n then return "negative cycle"
L9              if v is not in Q then ENQUEUE(Q, v)
L10 return d, π
```

Line L7 is an [edge relaxation](/edge-relaxation/). The count $k(v)$ is the number of arcs of the walk whose weight is $d(v)$: the walk to $u$ followed by $(u, v)$. A walk with $n$ arcs has $n + 1$ vertices, so it visits some vertex twice. Line L9 keeps each vertex at most once in $Q$; a flag per vertex makes the test $O(1)$.

## Example

Take the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7), scanned in this order, with source $s$. The labels are for $(s, t, x, y, z)$.

| dequeue | successful relaxations | queue after | labels after |
|---|---|---|---|
| $s$ | $t = 6$, $y = 7$ | $t, y$ | $0, 6, \infty, 7, \infty$ |
| $t$ | $x = 11$, $z = 2$ | $y, x, z$ | $0, 6, 11, 7, 2$ |
| $y$ | $x = 4$ | $x, z$ | $0, 6, 4, 7, 2$ |
| $x$ | $t = 2$ | $z, t$ | $0, 2, 4, 7, 2$ |
| $z$ | none | $t$ | $0, 2, 4, 7, 2$ |
| $t$ | $z = -2$ | $z$ | $0, 2, 4, 7, -2$ |
| $z$ | none | empty | $0, 2, 4, 7, -2$ |

At the third row, $x$ is already in the queue, so it is not added again. SPFA does 7 dequeues and 7 successful relaxations; Bellman-Ford on the same graph does 4 full passes over the 10 arcs (the last pass only to see that nothing changes). The parents are $t : x$, $x : y$, $y : s$, $z : t$.

**A negative cycle.** Set $x \to t$ to $-6$. The cycle $t \to z \to x \to t$ has weight $-4 + 7 - 6 = -3$. The labels go down around it, and the walk behind $d(t)$ grows by 3 arcs at each turn. When some $k(v)$ reaches 5, line L8 returns "negative cycle".

**An unreachable negative cycle.** Add the vertices $a, b$ with the arcs $a \to b$ ($-1$), $b \to a$ ($-1$) and $a \to s$ (1). The source $s$ cannot reach $a$ or $b$, so they never enter the queue, their labels stay $\infty$, and SPFA returns the same distances as above.

## Correctness

**Theorem.** SPFA terminates. If a negative cycle is reachable from $s$, it returns "negative cycle". Otherwise it returns $d(v) = \delta(s, v)$ for every $v$, with $\infty$ exactly for the unreachable vertices, and $\pi$ is a shortest-path tree.

The proof has three parts. First, every finite $d(v)$ is the weight of a walk with $k(v)$ arcs, and if that walk repeats a vertex, the part between the two visits is a negative closed walk, because the label of the repeated vertex went strictly down between the two visits. So line L8 fires only when a negative cycle is reachable. Second, a vertex $u$ with an arc that violates $d(v) \le d(u) + w(u, v)$ is always in $Q$, so when $Q$ is empty the labels satisfy the [optimality conditions](/shortest-path-optimality-conditions/), which prove that the labels are the distances and that no negative cycle is reachable. Third, the labels are weights of walks with fewer than $n$ arcs, a finite set, and they only go down, so the loop ends. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Passes.** Split the run into passes: pass 0 is the dequeue of $s$, and pass $j + 1$ dequeues the vertices that are in $Q$ at the end of pass $j$. Each vertex is dequeued at most once per pass, because it is at most once in $Q$. The proof shows that a label set in pass $j$ has $k(v) \ge j + 1$, so pass $n - 1$ cannot set a label without reaching line L8. Hence there are at most $n$ passes, in all cases.
- **Time.** Only vertices reachable from $s$ enter $Q$, so a pass costs $O(n' + m)$, where $n' \le \min(n, m + 1)$ is the number of reachable vertices. The total is $O(nm)$ in the worst case, the same as Bellman-Ford. The best case is $\Theta(n + m)$ for the initialization and one scan of the reachable arcs, for example on a tree.
- **Space.** $\Theta(n)$ extra for $d$, $\pi$, $k$, the queue and the flags.

The $O(nm)$ bound is reached: there are graphs, with all weights nonnegative, on which SPFA in FIFO order scans $\Theta(n)$ times a set of $\Theta(m)$ arcs. Such graphs are well known in competitive programming. The claim of the 1994 paper that SPFA takes $O(m)$ time on average is not a proved theorem for any natural input model that we know of.

## Properties

- **Same answer as Bellman-Ford.** With no reachable negative cycle, both return the distances. The parent trees can differ when several shortest paths exist.
- **Incremental.** If labels that are weights of real walks, for example from an earlier run, are put in $Q$ instead of $s$ alone, SPFA continues from them. This is useful when a few weights go down.
- **Label correcting.** A vertex can be scanned many times, unlike in [Dijkstra's algorithm](/dijkstra/), where each vertex is scanned once.
- **Early detection.** Line L8 can fire long before pass $n$, as soon as some walk has $n$ arcs.

## Variants and improvements

- **Counting queue entries.** A common form stops when a vertex enters $Q$ for the $n$-th time. This is also correct for the FIFO order: with no reachable negative cycle, labels are set only in passes 0 to $n - 2$, and a vertex enters $Q$ at most once per pass. It can wait for many more relaxations than the arc count $k(v)$.
- **Walking the parents.** Every $n$ relaxations, follow the parent pointers and look for a cycle. A cycle in the parent graph is always negative. This finds the cycle itself, which line L8 does not.
- **Subtree disassembly.** [Tarjan's subtree disassembly](/tarjan-subtree-disassembly/) removes the subtree of $v$ from the parent tree when $d(v)$ goes down, since those labels are no longer final. It finds a negative cycle as soon as the parent graph has one, and it is one of the fastest methods in the experiments of Cherkassky and Goldberg.
- **Deque orders.** The [D'Esopo-Pape algorithm](/desopo-pape-algorithm/) puts a vertex at the front of a deque if it was in the queue before. It is often fast, but it is not in the $O(nm)$ class: some graphs make it take exponential time.
- **Small label first, large label last.** These heuristics move a vertex with a small label nearer to the front. They do not change the worst-case bound.
- **Stack order.** With a stack instead of a queue, the pass argument does not hold, and the time can be exponential.

## When to use it

Use SPFA for single-source shortest paths with negative arcs when a simple method is enough and the graph is not built to be hard, for example in difference-constraint systems of moderate size. For nonnegative weights, use [Dijkstra's algorithm](/dijkstra/), whose $O((n + m) \log n)$ bound holds on every graph; SPFA on such graphs has only the $O(nm)$ bound. For a reliable negative-cycle test on large graphs, use [subtree disassembly](/tarjan-subtree-disassembly/) or Goldberg's scaling algorithm.

## Pitfalls

- **Detection by "the label changed $n$ times".** This is wrong. In one pass a label can go down once for each arc into the vertex, so a vertex with many arcs in can change $n$ times with no negative cycle. Count the arcs of the walk, as in line L7, or count queue entries with a FIFO queue.
- **Checking $k(v) > n$ instead of $k(v) \ge n$.** The test still works, but one more turn around the cycle is needed. Checking $k(v) \ge n - 1$ is wrong: a shortest path can have $n - 1$ arcs.
- **Adding a vertex twice to $Q$.** Without the test of line L9, $Q$ can hold many copies of a vertex, and the pass bound fails. Keep a flag per vertex.
- **Infinity arithmetic.** With a large number as $\infty$ and negative arcs, $\infty + w(u, v) < \infty$ can be true for an unreachable $u$. SPFA only dequeues vertices with finite labels, so this cannot happen in line L6, but code that also scans other vertices must test $d(u) < \infty$ first.
- **Trusting average speed.** On adversarial inputs SPFA is as slow as Bellman-Ford, and slower in practice because of the queue work.

## Implementations

## History

Moore (1959) gave the shortest-path method with a first-in first-out list of vertices to scan, in a paper on paths through a maze; Bellman (1958) and Ford (1956) had given the pass-based relaxation. The result is often called the Bellman-Ford-Moore algorithm. Pape (1974), after D'Esopo, proposed a deque order. Duan Fanding published the queue method under the name Shortest Path Faster Algorithm in 1994, in the Journal of Southwest Jiaotong University, and the name became common in competitive programming. Tarjan (1983) analysed the breadth-first scanning order and gave subtree disassembly, and Cherkassky and Goldberg (1999) compared the main strategies for negative-cycle detection.

## References
