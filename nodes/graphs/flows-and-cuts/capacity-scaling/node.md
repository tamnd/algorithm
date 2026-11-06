---
tag: H1FND5
kind: algorithm
slug: capacity-scaling
name: Capacity scaling max-flow algorithm
aliases:
- scaling max-flow
area: graphs/flows-and-cuts
level: advanced
summary: Augment only along paths with residual capacity above a decreasing threshold.
solves: [max-flow-problem, min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, U: "the largest capacity, integer capacities"}
  time: {worst: O(m^2 log U)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1972
  people: [Jack Edmonds, Richard M. Karp, Harold N. Gabow, Ravindra K. Ahuja, James B. Orlin]
  note: Edmonds and Karp introduced scaling for flow problems in 1972; Gabow (1985) applied bit scaling to maximum flow, and Ahuja and Orlin gave the capacity scaling form with shortest paths.
prereqs: [ford-fulkerson, residual-graph, breadth-first-search]
see_also: [fattest-augmenting-path, edmonds-karp, dinic, cost-scaling, cycle-canceling, augmenting-path-flow]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.3, Choosing Good Augmenting Paths (the scaling max-flow algorithm and its O(m^2 log C) bound)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (the capacity scaling algorithm)
  - paper: doi:10.1016/0022-0000(85)90039-X
    title: Harold N. Gabow, Scaling algorithms for network problems, Journal of Computer and System Sciences 31(2), 148 to 168 (1985)
    locator: the section on maximum flow (bit scaling)
---

Capacity scaling is the [Ford-Fulkerson method](/ford-fulkerson/) with a threshold $\Delta$: it augments only along paths whose every residual arc has capacity at least $\Delta$, and when no such path is left it halves $\Delta$. It starts with $\Delta$ the largest power of 2 not above the largest capacity $U$ and ends with $\Delta = 1$. Each phase does at most $2m$ augmentations, so the algorithm runs in $O(m^2 \log U)$ time for integer capacities. It gets the effect of the [fattest augmenting path](/fattest-augmenting-path/) rule with a plain graph search instead of a priority queue, and the same idea of scaling drives many faster flow algorithms.

## In plain words

Large pipes should be filled first. Capacity scaling asks only for routes on which every pipe has at least a big amount of spare room, and pushes along them. When none are left, it lowers its standard by half and looks again, and so on down to a single unit.

At the end of a round, the water still missing must fit through pipes that each have less than the current standard of spare room. So little water is missing, at most one standard per pipe. In the next round each push carries at least half the old standard, so only a few pushes, at most two per pipe, can happen before the round ends. The number of rounds is the number of halvings, which is the number of binary digits of the largest capacity.

## The problem

The input is a [flow network](/flow-network/) $N = (G, c, s, t)$ with a directed graph $G = (V, E)$ of $n$ vertices and $m$ edges, capacities $c(e) \ge 0$, and $s \ne t$. The output is a maximum [s-t flow](/s-t-flow/) and the source side of a minimum s-t cut.

**Assumptions.** Capacities are integers, and $U = \max_e c(e)$. Rational capacities work after scaling by a common denominator; real capacities do not fit the halving down to 1. The graph is directed; give an undirected edge as two directed edges. Antiparallel, parallel and zero-capacity edges and self-loops are allowed, and each edge has its own pair of residual arcs. A zero-capacity edge is never in $G_f$. If $U = 0$ or $t$ is not reachable from $s$, no augmentation happens and the answer is the zero flow.

## The algorithm

```pseudo id=main
CAPACITY-SCALING(G, c, s, t)
L1  for each edge e do c_f(e⁺) ← c(e), c_f(e⁻) ← 0
L2  Δ ← the largest power of 2 with Δ ≤ U  (Δ ← 0 if U = 0)
L3  while Δ ≥ 1 do
L4      while BFS from s over arcs with c_f ≥ Δ reaches t do
L5          P ← the path found;  δ ← min { c_f(x) : x on P }
L6          for each arc x on P do c_f(x) ← c_f(x) − δ, c_f(reverse x) ← c_f(reverse x) + δ
L7      Δ ← Δ / 2  (integer division)
L8  S ← the vertices reachable from s over arcs with c_f ≥ 1
L9  return f with f(e) = c_f(e⁻), and S
```

The *Δ-residual graph* $G_f(\Delta)$ keeps only the arcs with $c_f \ge \Delta$. Line L4 searches in it, and each augmentation in lines L5 and L6 carries $\delta \ge \Delta$. One pass of the outer loop is a *Δ-phase*. The last phase has $\Delta = 1$, where $G_f(1) = G_f$, so when it ends no augmenting path is left, and line L8 reads off the reachable set.

## Example

The network is the running example: $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10. So $U = 10$ and the first threshold is $\Delta = 8$. Each vertex scans its arcs in input order.

| $\Delta$ | path | $\delta$ | value | why the phase ends |
|---|---|---|---|---|
| 8 | $s\,a\,d\,t$ | 8 | 8 | arcs with $c_f \ge 8$ now reach only $c$, $d$ and, by the backward arc of $a d$, $a$ |
| 4 | $s\,c\,d\,b\,t$ | 6 | 14 | $c d$ drops to 3 and $s a$ is at 2, so $s$ reaches only $c$ |
| 2 | $s\,a\,b\,t$ | 2 | 16 | |
| 2 | $s\,c\,d\,t$ | 2 | 18 | $c d$ is at 1 and $d t$ is full |
| 1 | $s\,c\,d\,a\,b\,t$ | 1 | 19 | uses the backward arc of $a d$; then only $s$ and $c$ are reachable |

The final cut is $S = \{s, c\}$ with capacity $c(s, a) + c(c, d) = 19$. The first augmentation alone carries 8 of the 19 units. The flow found differs from that of [Edmonds-Karp](/edmonds-karp/): here $a d$ carries 7 and $a b$ carries 3.

**Edge cases.** With $s \to a$ 5 and $t \to a$ 5 every phase finds no path, the flow is 0 and $S = \{s, a\}$. With all capacities 0, $U = 0$ and the loop does not run; $S = \{s\}$. The bad case for plain Ford-Fulkerson, $s a$, $s b$, $a t$, $b t$ of capacity $X$ and $a b$ of capacity 1, takes two augmentations of $X$ in the first phase. The antiparallel network $s \to a$ 3, $a \to b$ 2, $b \to a$ 1, $b \to t$ 2, $s \to b$ 1 has maximum flow 2, and $a b$ and $b a$ keep separate flows.

## Correctness

Each augmentation is an ordinary augmentation along an s-t path of $G_f$ by its bottleneck $\delta > 0$, so by the augmentation lemma of [augmenting path](/augmenting-path-flow/) the flow stays feasible and integral and its value grows. Each phase ends, because each augmentation adds at least 1 to the value, which is bounded. The last phase has $\Delta = 1$ and ends when no s-t path with $c_f \ge 1$ exists; with integer capacities, $c_f \ge 1$ is the same as $c_f > 0$, so no augmenting path is left. Then $S$ of line L8 is the reachable set of $G_f$, every edge leaving $S$ is full and every edge entering it is empty, and $|f| = c(S, V \setminus S)$: the flow is maximum and the cut is minimum. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/) with integer capacities.

- **Phases.** $\Delta$ starts at most $U$ and halves until it is 0, so there are $\lfloor \log_2 U \rfloor + 1$ phases.
- **The residual bound.** At the end of a $\Delta$-phase, let $S$ be the set reachable from $s$ in $G_f(\Delta)$. Each edge crossing $S$ adds less than $\Delta$ to the residual capacity of the cut: an edge leaving $S$ has $c_f(e^+) < \Delta$, and an edge entering $S$ has $c_f(e^-) = f(e) < \Delta$. So the missing value $F - |f|$ is less than $m \Delta$.
- **Augmentations per phase.** In the next phase, with threshold $\Delta/2$, each augmentation carries at least $\Delta/2$, so there are fewer than $m\Delta / (\Delta/2) = 2m$ of them. The first phase has missing value at most $F \le mU < 2m\Delta$, which gives the same bound.
- **Total.** At most $2m$ augmentations per phase, each with a search of $O(n + m)$: $O(m^2 \log U)$ time, assuming $m \ge n - 1$. Space is $\Theta(n + m)$.

Using [Dinic's algorithm](/dinic/) or shortest augmenting paths with distance labels inside each phase lowers the bound to $O(nm \log U)$. The full argument is in the complexity proof below.

## Properties

- **Weakly polynomial.** The bound grows with $\log U$, the number of bits of the capacities.
- **Integral.** Every amount is an integer and the flow is integral.
- **Certificate.** $S$ is the source side of a minimum cut.
- **Large first.** Each phase carries at least half of the missing value at its start in a few big steps; most of the flow moves in the first phases.

## Variants and improvements

- **Shortest paths or blocking flows per phase.** Ahuja and Orlin combine scaling with distance labels for $O(nm \log U)$; Dinic per phase gives the same bound.
- **Bit scaling.** Gabow's form adds one bit of each capacity per phase: double the capacities and the flow, add the next bit, and repair with at most $m$ augmentations.
- **[Fattest augmenting path](/fattest-augmenting-path/).** Choose the widest path every time instead of any path above a threshold; $O(m \log F)$ augmentations, but each search needs a priority queue.
- **Scaling for minimum cost.** Edmonds and Karp first used scaling for [min-cost flow](/min-cost-flow-problem/); [cost scaling](/cost-scaling/) scales the costs instead of the capacities.
- **Goldberg and Rao.** Binary blocking flows with a length function based on $\Delta$ give $O(\min(n^{2/3}, m^{1/2})\, m \log(n^2/m) \log U)$.

## When to use it

Use capacity scaling when capacities are integers with a wide range, and you want a simple augmenting path code whose running time does not grow with the capacity values. For capacities in a small range, plain [Dinic](/dinic/) is faster and strongly polynomial. The scaling idea itself is worth knowing, since it underlies the best weakly polynomial flow algorithms.

## Pitfalls

- **Real capacities.** The halving stops at 1; with real capacities a final phase with $\Delta = 1$ does not see arcs with $0 < c_f < 1$, and the result is not maximum.
- **Starting $\Delta$ too low.** Starting below the largest power of 2 not above $U$ breaks the bound on the first phase, though not correctness.
- **Ending above 1.** The loop must run the phase with $\Delta = 1$; ending at $\Delta = 2$ leaves augmenting paths of capacity 1.
- **Merging antiparallel edges wrongly.** One residual entry per ordered pair must add the forward residual of $(u, v)$ and the backward residual of $(v, u)$. Keep one arc pair per edge, as in line L1.

## Implementations

The Python version takes the vertex count, a list of edges $(u, v, c)$ with integer $c$ and $s, t$, and returns the value, the flow on each input edge and the sorted source side of a minimum cut. It raises `TypeError` for non-integer capacities. An optional callback reports each threshold, path and amount; the tests use it to check that each amount is at least $\Delta$ and that no phase has more than $2m$ augmentations.

## History

Jack Edmonds and Richard Karp introduced scaling in their 1972 paper, for minimum-cost flows. Harold Gabow developed bit scaling for maximum flow, matching and shortest paths in 1985, and Ravindra Ahuja and James Orlin gave the capacity scaling form with shortest augmenting paths in $O(nm \log U)$ time. Kleinberg and Tardos present the simple $O(m^2 \log U)$ version as the first fix to the pseudo-polynomial bound of Ford-Fulkerson.

## References
