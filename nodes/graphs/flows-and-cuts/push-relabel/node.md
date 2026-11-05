---
tag: 56SN6Q
kind: algorithm
slug: push-relabel
name: Push-relabel algorithm
aliases:
- Goldberg-Tarjan algorithm
- preflow-push algorithm
area: graphs/flows-and-cuts
level: advanced
summary: Maintain a preflow and move excess locally using height labels until it becomes a flow.
solves: [max-flow-problem, min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^3 + n m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [preflow, residual-graph, max-flow-min-cut-theorem]
see_also: [distance-labeling, dinic, edmonds-karp, hao-orlin, mpm-algorithm, dynamic-tree, parametric-max-flow-problem, cost-scaling]
sources:
  - paper: doi:10.1145/48014.61051
    title: Andrew V. Goldberg and Robert E. Tarjan, A new approach to the maximum-flow problem, Journal of the ACM 35(4), 921 to 940 (1988)
    locator: the whole paper (the generic method, the FIFO version with its O(n^3) bound, and the dynamic tree version with O(nm log(n^2/m)))
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 26.4, Push-relabel algorithms, and Section 26.5, The relabel-to-front algorithm
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (the generic preflow-push algorithm, FIFO and highest-label versions)
  - paper: doi:10.1137/0218072
    title: Joseph Cheriyan and S. N. Maheshwari, Analysis of preflow push algorithms for maximum network flow, SIAM Journal on Computing 18(6), 1057 to 1086 (1989)
    locator: the whole paper (the O(n^2 m^(1/2)) bound for the highest-label rule)
---

The push-relabel algorithm of Goldberg and Tarjan computes a [maximum flow](/max-flow-problem/) by keeping a [preflow](/preflow/), in which vertices may hold excess, together with an integer height for each vertex. It repeatedly *pushes* excess from a vertex to a neighbor one level lower along an edge of the [residual graph](/residual-graph/), and *relabels* a vertex, raising its height, when no such neighbor exists. Excess that can reach the sink flows down to it; the rest climbs above the source's height and flows back. Any order of the operations gives a maximum flow with $O(n^2 m)$ operations; the first-in first-out order on this page takes $O(n^3)$ time, the highest-label order $O(n^2 \sqrt{m})$, and with [dynamic trees](/dynamic-tree/) $O(nm \log(n^2/m))$. In practice it is among the fastest maximum flow methods.

## In plain words

Think of the vertices as tanks on platforms of different heights, joined by pipes. Water only flows downhill, and only one step down at a time. At the start the source sits high above everything and floods all pipes that leave it; the water collects in the tanks next to it.

Then any tank that holds water tries to pour it into a pipe with room that leads one step down. If it cannot, because every pipe with room leads to a tank at its own height or higher, the tank is lifted a little, just above its lowest neighbor. Water that can reach the drain runs downhill to it. Water that cannot keeps rising until it is higher than the source, and then runs back to the source. When no tank holds water, the pipes carry a maximum flow.

## The problem

The input is a [flow network](/flow-network/): a directed graph $G = (V, E)$ with $n$ vertices, $m$ edges, capacities $c(e) \ge 0$ that may be integers or reals, a source $s$ and a sink $t \ne s$. Parallel edges are allowed. Antiparallel edges $(u, v)$ and $(v, u)$ stay separate edges, each with its own forward and backward residual edge. Edges of capacity 0 never carry flow, and self-loops are ignored. The output is a maximum $s$-$t$ flow and a [minimum cut](/min-cut-problem/). If $t$ is not reachable from $s$, the result is the zero flow; all excess returns to $s$.

## The algorithm

The vertices hold heights $h(v)$ and excesses $e(v)$. A residual edge $(u, w)$ is *admissible* if it has positive residual capacity and $h(u) = h(w) + 1$. Each vertex keeps a *current edge*, a pointer into its list of residual edges. Active vertices, those other than $s$ and $t$ with positive excess, wait in a first-in first-out queue.

```pseudo id=main
PUSH-RELABEL(G, c, s, t)
L1  h(v) ← 0 and e(v) ← 0 for each v; h(s) ← n
L2  for each edge (s, v): send c(s, v) along it, so e(v) ← e(v) + c(s, v)
L3  Q ← the vertices v ∉ {s, t} with e(v) > 0, in any order
L4  while Q is not empty do
L5      u ← DEQUEUE(Q)
L6      while e(u) > 0 do
L7          if the current edge of u is past the end of its list then
L8              h(u) ← 1 + min{ h(w) : (u, w) residual }; reset the current edge to the first   ▷ relabel
L9          else if the current edge r = (u, w) is admissible then
                push δ = min(e(u), c_f(r)) along r; if w ∉ {s, t} and w ∉ Q then ENQUEUE(Q, w)   ▷ push
L10         else advance the current edge
L11 return f, and the set S of vertices that s reaches in G_f
```

A push is *saturating* if $\delta = c_f(r)$ and *nonsaturating* otherwise; a nonsaturating push empties $u$. The discharge of $u$ in lines L6 to L10 runs until $u$ has no excess, relabeling as often as needed. Line L8 always has a residual edge to take the minimum over, because an active vertex has a residual path back to $s$.

## Example

The network has $s \to a$ (3), $s \to b$ (2), $a \to b$ (1), $a \to t$ (2), $b \to t$ (3). Line L2 sends 3 to $a$ and 2 to $b$, and $h(s) = 4$.

| step | vertex | operation | $h(a)$ | $h(b)$ | $e(a)$ | $e(b)$ | $e(t)$ |
|---|---|---|---|---|---|---|---|
| 0 | | initialize | 0 | 0 | 3 | 2 | 0 |
| 1 | $a$ | relabel to $1 + \min(h(s), h(b), h(t)) = 1$ | 1 | 0 | 3 | 2 | 0 |
| 2 | $a$ | push 1 along $a \to b$ (saturating) | 1 | 0 | 2 | 3 | 0 |
| 3 | $a$ | push 2 along $a \to t$ (saturating) | 1 | 0 | 0 | 3 | 2 |
| 4 | $b$ | relabel to $1 + h(t) = 1$ | 1 | 1 | 0 | 3 | 2 |
| 5 | $b$ | push 3 along $b \to t$ (saturating) | 1 | 1 | 0 | 0 | 5 |

The queue is empty, the flow is $3, 2, 1, 2, 3$ on the edges in the order above, and $S = \{s\}$, a minimum cut of capacity 5.

On the network $s \to a$ (10), $s \to b$ (10), $a \to b$ (2), $a \to c$ (4), $a \to d$ (8), $b \to d$ (9), $d \to c$ (6), $c \to t$ (10), $d \to t$ (10), the run takes 8 relabels and 12 pushes. Vertex $b$ cannot pass on 1 unit of its excess: it rises to height 7, above $h(s) = 6$, and pushes that unit back to $s$ along the backward edge of $s \to b$. The result is the maximum flow 19 with $S = \{s, b\}$.

Edge cases. An edge of capacity 0 is never admissible. If $t$ is not reachable from $s$, every unit of excess climbs above height $n$ and returns to $s$, and the value is 0.

## Correctness

Two invariants hold throughout: $f$ is a preflow, and $h$ is a valid labeling ($h(s) = n$, $h(t) = 0$, and $h(u) \le h(w) + 1$ for each residual edge $(u, w)$). A push along an admissible edge creates only the reverse edge $(w, u)$ with $h(w) = h(u) - 1$, and a relabel raises $h(u)$ to the largest value that keeps the edges out of $u$ valid. A valid labeling leaves no residual $s$-$t$ path, because such a path would have to drop $n$ levels in at most $n - 1$ steps. When the queue is empty, no vertex has excess, so the preflow is a flow with no augmenting path, hence maximum by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). The proof file below proves the invariants, the label bound $h(v) \le 2n - 1$, and the bounds on the number of operations.

## Complexity

The model is the [word RAM](/word-ram/); the bounds hold for real capacities as well, since none of them uses integrality.

- **Relabels.** Each vertex has height at most $2n - 1$, so there are fewer than $2n^2$ relabels. A relabel of $u$ scans its edges: $O(\deg u)$ each, $O(nm)$ in total. The current-edge pointer passes each edge of $u$ once per height of $u$, which is also $O(nm)$.
- **Saturating pushes.** Between two saturating pushes along the same residual edge $(u, w)$, the height of $w$ grows by at least 2, so there are at most $2nm$ of them.
- **Nonsaturating pushes.** In the generic method, at most $4n^2(n + m)$. With the FIFO queue, one per vertex per pass of the queue, and there are at most $4n^2$ passes, so at most $4n^3$.
- **Total.** $O(n^3 + nm)$ time for the FIFO version, which is $O(n^3)$ without parallel edges; $\Theta(n + m)$ space.

## Properties

- **Local.** Each operation looks at one vertex and its edges. This makes the method easy to run in parallel and fast in practice.
- **Not a path method.** Until the end, $f$ is not a flow, and its value is not known; $e(t)$ only grows.
- **Two phases.** In the first phase excess reaches $t$; in the second, the rest returns to $s$. A minimum cut is already known after the first phase, as the complement of the set of vertices that can reach $t$ in $G_f$.
- **Integral.** With integer capacities every push moves an integer amount, so the result is an integral flow.

## Variants and improvements

- **Highest-label.** Discharge an active vertex of largest height: $O(n^2 \sqrt{m})$ (Cheriyan and Maheshwari).
- **Relabel-to-front.** Keep the vertices in a list and move a relabeled vertex to the front: $O(n^3)$, as in Cormen et al.
- **Dynamic trees.** Push along whole paths of a [link-cut tree](/link-cut-tree/): $O(nm \log(n^2/m))$ (Goldberg and Tarjan).
- **Heuristics.** *Global relabeling* sets $h$ to the exact residual distance to $t$ by a backward [breadth-first search](/breadth-first-search/) from time to time; the *gap heuristic* lifts above $n$ every vertex above an empty height. Both matter a great deal in practice.
- **Other problems.** The same scheme gives [cost scaling](/cost-scaling/) for minimum-cost flow, the [Hao-Orlin](/hao-orlin/) global minimum cut, and the [parametric maximum flow](/parametric-max-flow-problem/) method of Gallo, Grigoriadis and Tarjan.

## When to use it

Use it for large dense networks and whenever a fast general maximum flow or minimum cut code is wanted; with the highest-label rule and the two heuristics it is a standard choice in practice. For unit capacities or bipartite matching, [Dinic](/dinic/) and [Hopcroft-Karp](/hopcroft-karp/) have better bounds. For very simple code on small inputs, [Edmonds-Karp](/edmonds-karp/) is shorter.

## Pitfalls

- **Starting with $h(s) = 0$.** Then excess flows straight back to $s$, and the result need not be maximum: the argument that no augmenting path is left needs $h(s) = n$.
- **Relabeling while an admissible edge exists.** Lines L7 and L8 relabel only when the current edge has passed the end of the list; a skipped edge cannot become admissible again before $u$ is relabeled.
- **Enqueueing $s$ or $t$.** They are never active; their excess is not discharged.
- **Merging antiparallel edges.** Each original edge needs its own residual pair, or the flow on each edge cannot be read back.
- **Reading the value too early.** The flow value is $e(t)$ only at the end; during the run, $f$ is not a flow.

## Implementations

## History

Goldberg introduced the method in a 1985 technical report, and Goldberg and Tarjan published it at STOC in 1986 and in the Journal of the ACM in 1988, with the generic $O(n^2 m)$ analysis, the FIFO $O(n^3)$ version and the dynamic tree version. It built on the preflows of Karzanov's blocking flow algorithm (1974). Cheriyan and Maheshwari proved the $O(n^2 \sqrt{m})$ bound of the highest-label rule in 1989.

## References
