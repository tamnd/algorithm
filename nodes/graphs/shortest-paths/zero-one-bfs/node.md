---
tag: T8G377
kind: algorithm
slug: zero-one-bfs
name: 0-1 BFS
aliases:
- 0-1 breadth-first search
area: graphs/shortest-paths
level: intro
summary: Shortest paths in graphs with weights 0 or 1 using a deque, in linear time.
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: Θ(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [breadth-first-search, deque, dijkstra, shortest-path]
see_also: [breadth-first-search, dijkstra, dial-algorithm, bucket-queue, single-source-shortest-paths, shortest-path-tree, multi-source-bfs]
sources:
  - url: "https://cp-algorithms.com/graph/01_bfs.html"
    locator: CP-Algorithms, article 0-1 BFS (the algorithm, the deque argument and the generalization to small integer weights)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search, and Section 22.3, Dijkstra's algorithm (the proof of Dijkstra's algorithm, which 0-1 BFS follows)
  - paper: "Robert B. Dial, Algorithm 360, Shortest-path forest with topological ordering, Communications of the ACM 12(11), 632 to 633 (1969)"
    locator: the bucket method for small integer weights, which 0-1 BFS specializes to two buckets
---

0-1 BFS computes [single-source shortest paths](/single-source-shortest-paths/) in a directed or undirected graph whose arc weights are all 0 or 1, in $\Theta(n + m)$ time. It is [Dijkstra's algorithm](/dijkstra/) with a [deque](/deque/) in place of the priority queue: a vertex reached by an arc of weight 0 goes to the front, and one reached by an arc of weight 1 goes to the back. With only two weights, the deque always holds labels of two adjacent values in sorted order, so the front is a minimum. It is the standard tool for grid and state-space problems where some moves are free, and it removes the $\log n$ factor of a heap.

## In plain words

Plain breadth-first search finds the fewest moves when every move costs one. Here some moves are free. A free move must not push a place to the back of the line, because it is as close as the place it came from.

So the method keeps a line with two ends. It takes the place at the front. For each move out of it, if the move gives a cheaper cost to the next place, it records that cost. A free move puts the next place at the front of the line, and a move that costs one puts it at the back. The line then always holds places of two neighboring costs, the smaller ones first, so the front place is always one of the closest. A place can enter the line twice; the second copy is skipped.

## The problem

The input is a graph $G = (V, E)$, given as adjacency lists, with weights $w : E \to \{0, 1\}$, and a source $s$. The output is $d[v] = \delta(s, v)$ for each $v$, with $\infty$ for an unreachable vertex, and a parent $\pi[v]$ that forms a [shortest-path tree](/shortest-path-tree/).

**Weight assumptions.** Every weight is the integer 0 or the integer 1. So all weights are nonnegative, and no negative cycle exists. A negative weight or a weight above 1 is outside the problem; the implementation rejects it. Cycles of weight 0 are allowed.

## The algorithm

```pseudo id=main
ZERO-ONE-BFS(G, w, s)
L1  for each v in V do d[v] ← ∞, π[v] ← nil, done[v] ← false
L2  d[s] ← 0, D ← a deque that holds only s
L3  while D is not empty do
L4      u ← POP-FRONT(D)
L5      if done[u] then continue            ▷ a stale copy of u
L6      done[u] ← true
L7      for each arc (u, v) in E do
L8          if d[u] + w(u, v) < d[v] then
L9              d[v] ← d[u] + w(u, v), π[v] ← u
L10             if w(u, v) = 0 then PUSH-FRONT(D, v)
L11             else PUSH-BACK(D, v)
L12 return d, π
```

Each push in lines L10 and L11 is a copy of $v$ with the *key* $d[v]$ at that moment. When $d[v]$ drops again, a new copy is pushed and the old copy stays in the deque; line L5 skips it when it comes out. Line L6 marks $u$ as finished: its label is final from then on. The test of line L8 is the [relaxation](/edge-relaxation/) of Dijkstra. The only change from Dijkstra is the queue.

## Example

The graph has six vertices and the arcs $s \to a$ (1), $s \to b$ (0), $b \to a$ (0), $a \to c$ (1), $b \to d$ (1), $c \to t$ (0), $d \to c$ (0) and $d \to t$ (1). Each row pops the front copy, written as vertex and key, and shows the deque after the scan, front first.

| pop | relaxations | deque after |
|---|---|---|
| $s$ (0) | $a$ gets 1, to the back; $b$ gets 0, to the front | $b{:}0$, $a{:}1$ |
| $b$ (0) | $a$ gets 0, to the front; $d$ gets 1, to the back | $a{:}0$, $a{:}1$, $d{:}1$ |
| $a$ (0) | $c$ gets 1, to the back | $a{:}1$, $d{:}1$, $c{:}1$ |
| $a$ (1) | stale copy, skipped by line L5 | $d{:}1$, $c{:}1$ |
| $d$ (1) | $t$ gets 2, to the back; $d \to c$ gives 1, no change | $c{:}1$, $t{:}2$ |
| $c$ (1) | $t$ gets 1, to the front | $t{:}1$, $t{:}2$ |
| $t$ (1) | no arcs | $t{:}2$ |
| $t$ (2) | stale copy, skipped | empty |

The result is $d = (0, 0, 0, 1, 1, 1)$ for $(s, a, b, c, d, t)$, with $\pi(a) = b$, $\pi(b) = s$, $\pi(c) = a$, $\pi(d) = b$ and $\pi(t) = c$. In every row the keys in the deque are sorted and span at most two adjacent values. A plain BFS that ignores the weights would give $d(a) = 1$, and a BFS that pushes every vertex to the back would pop $a$ with key 1 before it learns the free route through $b$.

## Correctness

**Theorem.** When ZERO-ONE-BFS returns, $d[v] = \delta(s, v)$ for every vertex $v$, and for every $v \ne s$ with $d[v] < \infty$, $\pi[v]$ is a vertex with $d[\pi[v]] + w(\pi[v], v) = d[v]$, so the parents form a shortest-path tree.

The key invariant is about the keys in the deque. **(D)** If the keys of the copies in $D$, from front to back, are $k_1, \ldots, k_r$, then $k_1 \le k_2 \le \cdots \le k_r \le k_1 + 1$. Line L4 pops $k_1$, the least key, and the rest lie in $[k_1, k_1 + 1]$. A push to the front with key $k_1$ and a push to the back with key $k_1 + 1$ keep (D). So the algorithm pops the copies in order of nondecreasing key, exactly as Dijkstra extracts the minimum, and the proof of Dijkstra then gives that $d[u] = \delta(s, u)$ when $u$ is finished. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Time.** Line L1 takes $\Theta(n)$. Each vertex is finished at most once by line L6, so the loop of line L7 runs once for each arc out of a reachable vertex: $O(m)$ relaxations, each $O(1)$. Each push in lines L10 and L11 follows a successful relaxation, so there are at most $m + 1$ copies in total, and each pop of line L4 removes one copy. Deque operations take $O(1)$ time. The total is $\Theta(n + m)$ in the worst case on the word RAM: all of line L1 is always done, and when all vertices are reachable every arc is scanned.
- **A sharper count.** Each vertex is pushed at most twice. When $v$ first gets a finite label while $u$ with key $k$ is scanned, $d[v] \in \{k, k + 1\}$. Later scans have keys at least $k$, so $d[v]$ can only drop from $k + 1$ to $k$, one more time.
- **Space.** The arrays take $\Theta(n)$ and the deque holds at most $\min(2n, m + 1)$ copies, so the extra space is $O(n + m)$, and also $O(n)$ by the sharper count.

## Properties

- **Exact.** It returns the true distances, not an approximation, for weights in $\{0, 1\}$.
- **Label setting.** Like Dijkstra, it finishes each vertex once and never changes a finished label.
- **Not for other weights.** Invariant (D) breaks with a weight of 2: a back push would get key $k_1 + 2$.

## Variants and improvements

- **Without the done array.** Many codes drop lines L5 and L6 and rescan a vertex each time it is popped. A rescan of a vertex with an outdated copy finds no improvement, so the result is the same, and by the sharper count the time stays $O(n + m)$.
- **Small integer weights.** For weights in $\{0, 1, \ldots, C\}$, use $C + 1$ circular buckets in place of the deque. This is [Dial's algorithm](/dial-algorithm/), in $O(m + nC)$ time.
- **Several sources.** Put all sources in the deque with key 0, as in [multi-source BFS](/multi-source-bfs/).
- **Grid problems.** In a grid where moving in the current direction is free and turning costs 1, the state is a (cell, direction) pair, and 0-1 BFS on the states finds the least number of turns.

## When to use it

Use 0-1 BFS when every weight is 0 or 1: it is simpler and faster than Dijkstra with a [binary heap](/binary-heap/), which takes $O((n + m) \log n)$. If all weights are 1, plain [BFS](/breadth-first-search/) is enough. For small integer weights, use [Dial's algorithm](/dial-algorithm/) or a [radix heap](/radix-heap/). For general nonnegative weights, use Dijkstra. With negative weights, use [Bellman-Ford](/bellman-ford/).

## Pitfalls

- **A visited mark at push time.** BFS marks a vertex when it is pushed. Here that is wrong: line L8 must be able to lower a label after the push, as with $a$ in the example (key 1, then 0). The test with $s \to a$ (1), $s \to b$ (0), $b \to a$ (0) catches this: the wrong code returns $d(a) = 1$.
- **Pushing every vertex to the back.** With `PUSH-BACK` in line L10, the deque is no longer sorted, and a vertex can be finished with a key that is too large. The same test catches it.
- **Comparing with ≤.** With `d[u] + w(u, v) ≤ d[v]` in line L8, a relaxation that does not lower a label still changes the parent. On $s \to a$ (1), $a \to b$ (0), $b \to a$ (0), the scan of $b$ then sets $\pi[a] = b$, and $a$ and $b$ become each other's parents, which is not a tree. The test with this zero cycle catches it. Keep the strict test.
- **Weights outside {0, 1}.** A weight of 2 or $-1$ breaks invariant (D) and gives wrong answers without an error. Check the weights, or use a general algorithm.

## Implementations

## History

The bucket method for small integer weights is due to Dial (1969). The two-bucket case, with the deque, is folklore in competitive programming, where it is known as 0-1 BFS; the CP-Algorithms article is a standard reference. No first publication of the deque form is known to this page.

## References
