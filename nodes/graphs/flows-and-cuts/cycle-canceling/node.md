---
tag: M028R9
kind: algorithm
slug: cycle-canceling
name: Cycle-canceling algorithm
aliases:
- negative cycle canceling
- Klein's algorithm
area: graphs/flows-and-cuts
level: advanced
summary: Start from any feasible flow and cancel negative-cost cycles in the residual graph.
solves: [min-cost-flow-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, U: the largest capacity, C: the largest absolute cost}
  time: {worst: O(n m^2 C U)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1967
  people: [Morton Klein, Andrew V. Goldberg, Robert E. Tarjan]
  note: Klein proposed canceling negative cycles in 1967; Goldberg and Tarjan showed in 1989 that canceling a cycle of minimum mean cost is strongly polynomial.
prereqs: [min-cost-flow-problem, bellman-ford, residual-graph]
see_also: [negative-cycle-detection, minimum-mean-cycle-problem, successive-shortest-path, cost-scaling, network-simplex, circulation-problem, flow-decomposition, reduced-cost]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 9, Minimum Cost Flows, Basic Algorithms (negative cycle optimality conditions and the cycle-canceling algorithm) and Chapter 10, Minimum Cost Flows, Polynomial Algorithms (minimum mean cycle-canceling)
  - paper: doi:10.1287/mnsc.14.3.205
    title: Morton Klein, A primal method for minimal cost flows with applications to the assignment and transportation problems, Management Science 14(3), 205 to 220 (1967)
    locator: the whole paper (canceling negative cycles)
  - paper: doi:10.1145/76359.76368
    title: Andrew V. Goldberg and Robert E. Tarjan, Finding minimum-cost circulations by canceling negative cycles, Journal of the ACM 36(4), 873 to 886 (1989)
    locator: the whole paper (minimum mean cycle canceling and its strongly polynomial bound)
---

The cycle-canceling algorithm solves the [minimum-cost flow problem](/min-cost-flow-problem/) by local improvement. It first finds any flow of the required value, here a maximum flow, and then, as long as the [residual graph](/residual-graph/) has a cycle of negative total cost, it pushes flow around that cycle. Pushing around a cycle keeps every conservation constraint and the flow value, and lowers the cost. When no negative cycle is left, the flow is optimal: this is the negative cycle optimality theorem. With integer data the algorithm stops after at most $2mCU$ cancellations, and canceling a cycle of minimum mean cost makes it strongly polynomial.

## In plain words

Suppose you already ship the right amount of goods from the source to the drain, but some routes are expensive. Look for a loop of changes that saves money: send one more unit along some roads, and one less along others, so that every town still receives what it sends. If such a loop saves money, apply it as many times as the roads allow.

A loop like this never changes how much arrives at the drain, so the shipment stays correct while it gets cheaper. When no money-saving loop is left, no cheaper shipment exists at all, because the difference between your plan and any cheaper plan would itself split into loops, and one of them would save money.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, two vertices $s \ne t$, and for each edge a capacity $c(e) \ge 0$ and a cost $w(e)$ per unit of flow, of any sign. The output is a maximum [s-t flow](/s-t-flow/) $f$ whose total cost $\sum_e w(e) f(e)$ is least among all maximum flows. The same method solves minimum-cost circulations with demands: start from any feasible flow, found as on the page [circulation problem](/circulation-problem/).

**Assumptions.** Capacities and costs are integers; rational data works after scaling. With real data each cancellation still lowers the cost, but the plain rule need not stop. The graph is directed; give an undirected edge as two directed edges. Antiparallel, parallel and zero-capacity edges and self-loops are allowed, and each edge has its own pair of residual arcs: $e^+$ with cost $w(e)$ and $e^-$ with cost $-w(e)$. Antiparallel edges $(a, b)$ and $(b, a)$ form a residual cycle of cost $w(a, b) + w(b, a)$, which is canceled if negative. A self-loop of negative cost is a negative cycle of one arc and ends up full. A zero-capacity edge is never in $G_f$. If $t$ is not reachable from $s$, the maximum flow is 0, and the algorithm still cancels negative cycles elsewhere in the graph.

## The algorithm

```pseudo id=main
CYCLE-CANCELING(G, c, w, s, t)
L1  for each edge e do c_f(e⁺) ← c(e), w(e⁺) ← w(e);  c_f(e⁻) ← 0, w(e⁻) ← −w(e)
L2  find a maximum s-t flow f, for example by Edmonds-Karp, ignoring costs
L3  repeat
L4      run Bellman-Ford on the arcs with c_f > 0, starting with d[v] ← 0 for every v, for up to n rounds, recording π
L5      if round n changed no d[v] then leave the repeat loop
L6      x ← a vertex changed in round n;  repeat n times: x ← the tail of π[x]
L7      C ← the cycle of arcs π[x], π[tail of π[x]], ... back to x
L8      δ ← min { c_f(a) : a ∈ C };  for each arc a of C do c_f(a) ← c_f(a) − δ, c_f(reverse a) ← c_f(reverse a) + δ
L9  return f with f(e) = c_f(e⁻), and its cost
```

Line L4 is [negative cycle detection](/negative-cycle-detection/) by [Bellman-Ford](/bellman-ford/): starting every distance at 0 is the same as adding a source joined to every vertex by an arc of cost 0, so every negative cycle of $G_f$ is found, wherever it is. If round $n$ still lowers some $d[v]$, a negative cycle exists, and following predecessor arcs $n$ times from a changed vertex lands on a cycle of predecessor arcs, which has negative cost. Line L8 pushes the bottleneck amount around it, which empties at least one arc of the cycle.

## Example

The running network with costs: $s a$ (10, cost 2), $s c$ (10, 2), $a b$ (4, 6), $a c$ (2, 3), $a d$ (8, 1), $c d$ (9, 2), $d b$ (6, 1), $b t$ (10, 1), $d t$ (10, 3), where the pairs are capacity and cost.

**Line L2.** [Edmonds-Karp](/edmonds-karp/) gives the maximum flow with values $10, 9, 4, 0, 6, 9, 5, 9, 10$ on the edges in that order, value 19 and cost $20 + 18 + 24 + 0 + 6 + 18 + 5 + 9 + 30 = 130$.

**First cancellation.** The residual cycle $d\,b\,t\,d$ uses $d b$ forward (cost 1, room 1), $b t$ forward (cost 1, room 1) and the backward arc of $d t$ (cost $-3$, room 10). Its cost is $-1$ per unit and its bottleneck is 1. Moving one unit from $d t$ to $d\,b\,t$ gives cost 129.

**Second cancellation.** The cycle $a\,d\,t\,b\,a$ uses $a d$ forward (cost 1, room 2), $d t$ forward (cost 3, room 1), the backward arc of $b t$ (cost $-1$) and the backward arc of $a b$ (cost $-6$). Its cost is $-3$ and its bottleneck is 1. The unit that went $a\,b\,t$ now goes $a\,d\,t$, and the cost is 126.

**Stop.** The final flow is $10, 9, 3, 0, 7, 9, 6, 9, 10$ with cost 126. Bellman-Ford finds no negative cycle, so no maximum flow costs less. The value stayed 19 throughout.

**A negative cycle away from the path.** With $s \to t$ (capacity 2, cost 1) and the antiparallel pair $a \to b$ (3, cost $-2$) and $b \to a$ (5, cost 1), the maximum flow is 2 at cost 2, and the residual cycle $a\,b\,a$ has cost $-1$ and bottleneck 3. Canceling it gives cost $2 - 3 = -1$. The two edges between $a$ and $b$ keep separate flows, 3 each.

**Edge cases.** With $s \to a$ and $t \to a$ only, the maximum flow is 0 and the cost 0. An edge of capacity 0 with cost $-9$ is never used, because it is not in $G_f$.

## Correctness

Each cancellation moves flow around a cycle of $G_f$ by its bottleneck: conservation still holds at every vertex, the residual capacities stay nonnegative, and the net flow out of $s$ does not change, so $f$ stays a maximum flow, and its cost drops by $\delta \cdot |w(C)| > 0$. The key fact is the **negative cycle optimality theorem**: a maximum flow $f$ has least cost among maximum flows if and only if $G_f$ has no cycle of negative cost. One direction is the cancellation step itself. For the other, if $f^*$ is a cheaper maximum flow, the difference $f^* - f$, written on the residual arcs, is a circulation in $G_f$ of negative cost, and by [flow decomposition](/flow-decomposition/) it is a sum of cycles of $G_f$, one of which must have negative cost. With integer data each cancellation lowers the cost by at least 1, and the cost is bounded below, so the loop ends. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/) with integer capacities and costs. Let $U$ be the largest capacity and $C$ the largest $|w(e)|$.

- **Line L2.** One maximum flow, $O(nm^2)$ by Edmonds-Karp.
- **One cancellation.** Bellman-Ford costs $O(nm)$; extracting and canceling the cycle costs $O(n)$.
- **Number of cancellations.** Every flow with $0 \le f \le c$ has cost between $-mCU$ and $mCU$, and each cancellation lowers the cost by at least 1, since $\delta \ge 1$ and $w(C) \le -1$. So there are at most $2mCU$ cancellations.
- **Total.** $O(nm \cdot mCU) = O(nm^2 CU)$ time, which is pseudo-polynomial: it grows with the values $C$ and $U$, not their number of bits. Space is $\Theta(n + m)$.

A bad choice of cycles can need that many steps, which is why the rule for choosing the cycle matters (see below). The full argument is in the complexity proof below.

## Properties

- **Primal.** The flow is feasible and has the right value at every step; stopping early gives a feasible flow with a cost no larger than the start.
- **Integral.** With integer capacities each $\delta$ is an integer, so the final optimal flow is integral; this proves the integrality of minimum-cost flows.
- **Certificate.** When it stops, Bellman-Ford's distances $d$ are potentials with $w(a) + d(u) - d(v) \ge 0$ on every residual arc $a = (u, v)$: nonnegative [reduced costs](/reduced-cost/), the dual certificate of optimality.
- **Monotone.** The cost decreases strictly with each cancellation.

## Variants and improvements

- **Minimum mean cycle canceling.** Cancel a cycle of least mean cost $w(C)/|C|$, found by [Karp's algorithm](/karp-minimum-mean-cycle/) in $O(nm)$. Goldberg and Tarjan proved that the number of cancellations is then $O(nm \log(nC))$ for integer costs and $O(nm^2 \log n)$ for any real costs, so the method becomes strongly polynomial.
- **Maximum improvement.** Weintraub (1974) showed that canceling a cycle of largest improvement needs only polynomially many cancellations, but finding such a cycle is NP-hard; Barahona and Tardos (1989) gave a polynomial way to get a comparable improvement from a set of disjoint cycles.
- **Cancel-and-tighten.** Goldberg and Tarjan's faster variant cancels many cycles of a level graph at once and runs in $O(nm \log n \log(nC))$.
- **[Network simplex](/network-simplex/).** Pivots along cycles that a spanning tree defines; each pivot cancels a negative cycle of one non-tree arc, and it is the fastest in practice.
- **Other methods.** [Successive shortest paths](/successive-shortest-path/) keeps the flow optimal and grows its value, and [cost scaling](/cost-scaling/) keeps it nearly optimal and refines the precision.

## When to use it

Use cycle canceling when you already have a good feasible flow and want to improve it, when you need a simple and clearly correct minimum-cost solver for small instances, or when the cost function changes and you want to repair the old optimum. For large instances, [network simplex](/network-simplex/) or [cost scaling](/cost-scaling/) is much faster; for minimum-cost flows of small value, [successive shortest paths](/successive-shortest-path/) is simpler.

## Pitfalls

- **Detecting only cycles reachable from $s$.** A Bellman-Ford run from $s$ alone misses negative cycles that $s$ cannot reach. Start every distance at 0, as in line L4.
- **Taking a vertex changed in round $n$ as on the cycle.** It may only lead to the cycle; walk the predecessors $n$ times first, as in line L6.
- **Using arcs of zero residual capacity.** Bellman-Ford must use only arcs with $c_f > 0$, including backward arcs with cost $-w(e)$.
- **Merging antiparallel edges.** Edges $(a, b)$ and $(b, a)$ with different costs cannot share one residual entry: the backward arc of one has cost $-w$, the forward arc of the other a different cost. Keep one arc pair per edge, as in line L1.
- **Real or float costs.** The plain rule may not stop with irrational data, and rounding can make a cycle of cost 0 look negative; use the minimum mean rule or exact numbers.

## Implementations

The Python version takes the vertex count, a list of edges $(u, v, c, w)$ with integer capacity and cost, and $s, t$. It finds a maximum flow by Edmonds-Karp and then cancels negative cycles found by Bellman-Ford, and returns the flow value, the least cost and the flow on each input edge. An optional callback reports each cycle, its amount and its cost per unit. The tests compare it on 600 random small networks with an enumeration of all integral flows.

## History

Morton Klein published the cycle-canceling method in Management Science in 1967. Its running time stayed pseudo-polynomial until Andrew Goldberg and Robert Tarjan showed in 1988, published in the Journal of the ACM in 1989, that always canceling a cycle of minimum mean cost needs only a strongly polynomial number of cancellations.

## References
