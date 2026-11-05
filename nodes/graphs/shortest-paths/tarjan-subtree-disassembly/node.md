---
tag: 8J5TGF
kind: algorithm
slug: tarjan-subtree-disassembly
name: Tarjan's subtree disassembly
aliases:
- Tarjan negative cycle detection
- subtree disassembly
- Bellman-Ford-Tarjan algorithm
area: graphs/shortest-paths
level: advanced
summary: Detects negative cycles in a shortest-path tree by removing subtrees, often faster than Bellman-Ford in practice.
solves: [single-source-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [spfa, shortest-path-tree, negative-cycle-detection, upper-bound-property]
see_also: [spfa, bellman-ford, negative-cycle-detection, shortest-path-tree, desopo-pape-algorithm, generic-shortest-path-algorithm, goldberg-scaling-sssp, shortest-path-optimality-conditions]
sources:
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms
    locator: Chapter 7, Shortest paths (the labeling method, the breadth-first scanning order and the subtree disassembly that finds negative cycles)
  - paper: "Robert E. Tarjan, Shortest paths, technical report, AT&T Bell Laboratories, Murray Hill, 1981"
    locator: the subtree disassembly method
  - paper: doi:10.1007/s101070050058
    title: Boris V. Cherkassky and Andrew V. Goldberg, Negative-cycle detection algorithms, Mathematical Programming 85(2), 277 to 311 (1999)
    locator: the sections on subtree disassembly and subtree traversal and the experimental comparison
  - paper: "Boris V. Cherkassky, Loukas Georgiadis, Andrew V. Goldberg, Robert E. Tarjan and Renato F. Werneck, Shortest-path feasibility algorithms, an experimental evaluation, ACM Journal of Experimental Algorithmics 14 (2009)"
    locator: the comparison of subtree disassembly with other negative-cycle detection codes
---

Tarjan's subtree disassembly is a single-source shortest-path algorithm for arbitrary real weights that finds a [negative cycle](/negative-cycle/) as soon as one appears in its parent pointers. It is [SPFA](/spfa/), the queue-based [Bellman-Ford](/bellman-ford/), that keeps the current [shortest-path tree](/shortest-path-tree/) explicitly. When the label of $v$ goes down, every proper descendant of $v$ has a label that is now too high, so the algorithm removes the whole subtree below $v$ from the tree and from the queue. If the vertex $u$ that lowered $d(v)$ is itself in that subtree, the tree path from $v$ to $u$ and the arc $(u, v)$ form a negative cycle, which the algorithm returns. The worst-case time stays $O(nm)$, and in experiments it is one of the fastest practical methods for negative-cycle detection.

## In plain words

The program keeps a family tree of best-known routes: each place points to the place before it on its best route so far. When a place gets a cheaper cost, all places below it in the family tree got their costs through the old, worse cost, so those costs are out of date. The program cuts that whole branch off and stops working on those places for now; they will come back when the cheaper cost reaches them.

If the place that gave the cheaper cost is itself in the branch that is cut off, the routes go in a circle: a place made its own cost cheaper through a loop. That loop has a negative total, and the program reports it at once.

## The problem

The input is a directed graph $G = (V, E)$ with $n = |V|$, $m = |E|$, weights $w : E \to \mathbb{R}$ and a source $s$. The output is either $\delta(s, v)$ for every $v$, with $\infty$ for the vertices that $s$ cannot reach, and a shortest-path tree; or a negative cycle reachable from $s$, given as a list of vertices.

**Weight assumptions.** Any real weights, negative ones included. Negative cycles that $s$ cannot reach do not matter. Integer weights are not needed.

## The algorithm

$T$ is the current tree, rooted at $s$, with the parent pointers $\pi$. A vertex is *in the tree* when it has a finite label and has not been removed since its label was last set.

```pseudo id=main
SUBTREE-DISASSEMBLY(G, w, s)
L1  d(v) ← ∞, π(v) ← nil for all v; d(s) ← 0; T ← the tree with only s; Q ← a queue that holds only s
L2  while Q is not empty do
L3      u ← DEQUEUE(Q)
L4      for each arc (u, v) out of u do
L5          if d(u) + w(u, v) < d(v) then
L6              if v = u or v is an ancestor of u in T then     ▷ found while walking the subtree of v
L7                  return the cycle: the tree path from v to u, then the arc (u, v)
L8              for each proper descendant x of v in T do remove x from T and from Q; π(x) ← nil
L9              d(v) ← d(u) + w(u, v); make v a child of u in T; π(v) ← u
L10             if v is not in Q then ENQUEUE(Q, v)
L11 return d, π
```

Lines L6 and L8 are one walk over the subtree of $v$: the walk either meets $u$, which ends the run, or removes every vertex it meets. A removed vertex keeps its label but is not scanned until its label goes down again, which puts it back in the tree. With the tree stored as a doubly linked list in preorder, with the depth of each vertex, the walk takes $O(1)$ time per vertex it meets.

## Example

Take the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7), scanned in this order, with source $s$.

| scan | label changes | removed from the tree | queue after |
|---|---|---|---|
| $s$ | $t = 6$, $y = 7$ | none | $t, y$ |
| $t$ | $x = 11$, $z = 2$ | none | $y, x, z$ |
| $y$ | $x = 4$ (parent $t$ to $y$) | none, $x$ has no children | $x, z$ |
| $x$ | $t = 2$ (parent $s$ to $x$) | $z$, the child of $t$ | $t$ |
| $t$ | $z = -2$ | none | $z$ |
| $z$ | none | none | empty |

The distances are $(0, 2, 4, 7, -2)$ for $(s, t, x, y, z)$, with the parents $t : x$, $x : y$, $y : s$, $z : t$. In the fourth row, $d(z) = 2$ was computed from the old $d(t) = 6$, so it is out of date; SPFA scans $z$ anyway, without any effect, while subtree disassembly skips it. This run makes 6 scans against 7 for SPFA.

**A negative cycle.** Set $x \to t$ to $-6$. The first three scans are the same. Scanning $x$ sets $d(t) = 4 - 6 = -2$, makes $t$ a child of $x$, and removes $z$. Scanning $t$ then finds $d(t) + w(t, x) = -2 + 5 = 3 < 4 = d(x)$, and $x$ is the parent of $t$, so $x$ is an ancestor of $t$. Line L7 returns the cycle $x \to t \to x$ of weight $-6 + 5 = -1$, after only 5 scans. SPFA and Bellman-Ford need many more steps to report a cycle on this graph.

**Unreachable parts.** Vertices that $s$ cannot reach never get a finite label and never enter the tree, so a negative cycle among them is not reported, and their labels stay $\infty$.

## Correctness

**Theorem.** SUBTREE-DISASSEMBLY terminates. If it returns a cycle, the cycle is a negative cycle reachable from $s$. If it returns $d$ and $\pi$, then no negative cycle is reachable from $s$, $d(v) = \delta(s, v)$ for every $v$, and $\pi$ is a shortest-path tree. Hence it returns a cycle exactly when a negative cycle is reachable from $s$.

The key invariant is that every tree arc is tight: $d(x) = d(\pi(x)) + w(\pi(x), x)$. It holds because an arc enters the tree tight at line L9, and if the label of its tail goes down, line L8 removes its head first. So the tree path from $v$ to $u$ has weight $d(u) - d(v)$, and the cycle of line L7 has weight $d(u) + w(u, v) - d(v) < 0$. Tightness also shows that every label is the weight of a simple tree path from $s$, a finite set of values, so the labels can go down only finitely often and the run ends. At the end, every vertex with a finite label is back in the tree, and no arc with a finite tail is violated, so the [optimality conditions](/shortest-path-optimality-conditions/) give the distances. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Time.** $O(nm)$ in the worst case, as Tarjan shows for the breadth-first order: the passes of [SPFA](/spfa/) still bound the number of scans by $n$ per vertex, and removed vertices are only skipped. The removal work is paid by label changes: each vertex removed at line L8 was put into the tree by one earlier execution of line L9, and each execution of line L9 is caused by one arc relaxation. So the removals add $O(1)$ per relaxation. The best case is $\Theta(n + m)$, for example when the first labels are already the distances.
- **Space.** $\Theta(n)$ extra: labels, parents, the tree in preorder and the queue.

On graphs with a negative cycle, the algorithm usually stops far sooner than the $n$ passes of Bellman-Ford, because a negative cycle tends to appear in the parent pointers after a few turns of relaxation.

## Properties

- **Immediate detection.** The parent graph of label-correcting methods has a cycle only when there is a negative cycle. Subtree disassembly keeps the parent graph a tree at all times, and it reports a cycle at the first relaxation that would close one.
- **Fewer useless scans.** Removed vertices have labels that are known to be too high, so their arcs are not scanned until their labels improve.
- **Explicit cycle.** The output on failure is the cycle itself, a certificate that can be checked by adding its weights.
- **Same answer as Bellman-Ford.** With no reachable negative cycle, both give the distances; the trees can differ when there are ties.

## Variants and improvements

- **Subtree traversal without removal.** Walk the subtree of $v$ only to look for $u$, without removing anything. It detects cycles as early, but scans out-of-date vertices.
- **Walk to the root.** Instead of walking down from $v$, walk up from $u$ to $s$ and test whether $v$ is met. It costs the depth of $u$ per relaxation.
- **Subtree updates.** Instead of removing the subtree, lower every label in it by the improvement $\Delta$ and keep it in the tree. The tree arcs stay tight, so the method stays correct, and the subtree vertices are put in the queue with their new labels.
- **Amortized parent checking.** Cherkassky and Goldberg also study algorithms that look for cycles in the parent graph only every so many relaxations, which is cheaper per step but slower to detect.
- **With scaling.** Goldberg's scaling algorithm and its successors use the same kind of tree maintenance on reduced costs; see [Goldberg's scaling algorithm](/goldberg-scaling-sssp/).
- **Other orders.** Disassembly can be combined with other scanning orders, such as a [deque](/desopo-pape-algorithm/), but the $O(nm)$ bound depends on the FIFO order.

## When to use it

Use subtree disassembly when you need single-source shortest paths with negative weights and want negative cycles found fast, for example in [difference constraints](/difference-constraints/), in checking the feasibility of a schedule, or in min-cost flow codes that look for negative cycles. Experiments by Cherkassky and Goldberg rank it among the best practical methods. For a plain test with simple code, [SPFA](/spfa/) with an arc count is enough; for proved bounds better than $O(nm)$ with integer weights, use [Goldberg's scaling](/goldberg-scaling-sssp/) or the [near-linear algorithm](/near-linear-negative-sssp/).

## Pitfalls

- **Removing the subtree but keeping its parent pointers.** A removed vertex must get $\pi(x) = $ nil. If it keeps its old parent, a later cycle test can follow a pointer that is no longer a tight tree arc and report a cycle that is not negative.
- **Scanning removed vertices.** If a removed vertex stays in the queue and is scanned, the algorithm is still correct but loses its speed-up. Remove it, or skip it when it comes out of the queue.
- **Forgetting the self-loop.** A negative self-loop $(v, v)$ has $u = v$; the test of line L6 must include it, since $v$ is not a proper descendant of itself.
- **Removing $v$ itself.** Line L8 removes the proper descendants only. $v$ stays in the tree with its new parent $u$.
- **Checking the wrong direction.** The cycle exists when $u$ is a descendant of $v$, not when $v$ is a descendant of $u$. A relaxation from an ancestor $u$ to a descendant $v$ is normal and only moves the subtree.

## Implementations

## History

Tarjan described subtree disassembly in a 1981 technical report on shortest paths and in Chapter 7 of his 1983 book, as a change to the breadth-first labeling method that keeps the $O(nm)$ bound and finds negative cycles early. The method is sometimes called the Bellman-Ford-Tarjan algorithm. Cherkassky and Goldberg (1999) compared it with many other negative-cycle detection strategies and found it, together with Goldberg's scaling method, among the most robust; a later study by Cherkassky, Georgiadis, Goldberg, Tarjan and Werneck (2009) refined these comparisons.

## References
