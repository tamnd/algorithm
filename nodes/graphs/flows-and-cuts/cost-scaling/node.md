---
tag: ZWH6V8
kind: algorithm
slug: cost-scaling
name: Cost scaling min-cost flow algorithm
aliases:
- Goldberg-Tarjan cost scaling
area: graphs/flows-and-cuts
level: research
summary: Scale costs and refine epsilon-optimal flows via push-relabel style operations.
solves: [min-cost-flow-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, C: the largest absolute edge cost}
  time: {worst: O(n m^2 + n^2 m log(n C))}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1987
  people: [Andrew V. Goldberg, Robert E. Tarjan]
  note: Goldberg and Tarjan presented cost scaling with push-relabel refinement at STOC 1987 and in Mathematics of Operations Research in 1990; epsilon-optimality goes back to Bertsekas and to Tardos.
prereqs: [min-cost-flow-problem, push-relabel, reduced-cost]
see_also: [cycle-canceling, successive-shortest-path, network-simplex, auction-algorithm, scaling-technique, capacity-scaling, minimum-mean-cycle-problem, assignment-problem]
sources:
  - paper: doi:10.1287/moor.15.3.430
    title: Andrew V. Goldberg and Robert E. Tarjan, Finding minimum-cost circulations by successive approximation, Mathematics of Operations Research 15(3), 430 to 466 (1990)
    locator: the sections on epsilon-optimality, the refine procedure and the generic, FIFO and dynamic tree bounds
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 10, Minimum Cost Flows, Polynomial Algorithms (the cost scaling algorithm, its lemmas on epsilon-optimal flows and its running time)
  - paper: doi:10.1006/jagm.1995.1048
    title: Andrew V. Goldberg, An efficient implementation of a scaling minimum-cost flow algorithm, Journal of Algorithms 22(1), 1 to 29 (1997)
    locator: the whole paper (the CS2 implementation and its heuristics)
---

Cost scaling is a method for the [minimum-cost flow problem](/min-cost-flow-problem/) that relaxes optimality instead of feasibility. A flow is $\varepsilon$-optimal for vertex potentials $p$ if every arc of the residual graph has [reduced cost](/reduced-cost/) at least $-\varepsilon$; with integer costs, $\varepsilon < 1/n$ already means optimal. The algorithm starts with a large $\varepsilon$ and halves it repeatedly, and each halving step, called refine, restores $\varepsilon$-optimality with the push and relabel operations of [push-relabel](/push-relabel/). This gives $O(\log(nC))$ refine steps, a weakly polynomial bound with no dependence on capacities, and Goldberg's CS2 code based on it has long been among the fastest practical min-cost flow solvers.

## In plain words

Each pipe has a price per unit. A plan is perfect if no rerouting around a loop saves money. Cost scaling first accepts plans that are nearly perfect, allowing any loop to save a little, up to a large tolerance. Then it halves the tolerance again and again. Each time, it first throws away flow on pipes that now look too expensive, which leaves some places with too much and some with too little, and then pushes the extra along cheap-looking pipes, raising or lowering place prices when stuck. When the tolerance is small enough, every loop costs at least nothing, and the plan is the cheapest.

## The problem

**Input.** A directed graph with vertices $0, \dots, n - 1$, edges $e = (u, v)$ with integer capacity $c(e) \ge 0$ and integer cost $w(e)$ of any sign, and a source $s$ and sink $t$.

**Output.** A maximum s-t flow of least total cost $\sum_e w(e) f(e)$.

The implementation first finds a maximum flow and then minimizes cost among flows of that value, which is a minimum-cost circulation in its residual graph; any min-cost flow instance with demands reduces to this form. Edges are directed; each edge $e$ has its own arc pair, forward with residual capacity $c(e) - f(e)$ and cost $w(e)$, backward with residual capacity $f(e)$ and cost $-w(e)$. Antiparallel edges are kept as two separate pairs, so a cheap edge $a \to b$ and an expensive edge $b \to a$ do not cancel each other. An edge of capacity 0 never has a residual arc. Capacities could be real numbers for the method itself, as no step divides them, but costs must be integers for the stopping rule; the code requires both to be integers.

## The algorithm

Write $c_p(x) = w(x) + p(v) - p(w)$ for the reduced cost of a residual arc $x = (v, w)$. The excess of $v$ is the net amount it has received since the start of the current refine; a vertex is active if its excess is positive. An arc is admissible if it is residual and $c_p(x) < 0$.

```pseudo id=main
COST-SCALING(G, c, w, s, t)
L1  f ← a maximum s-t flow;  p ← 0;  multiply every cost by n + 1
L2  ε ← max(1, max_e |w(e)|)
L3  repeat
L4      ε ← ⌈ε / 2⌉
L5      for each residual arc x with c_p(x) < 0 do push all of its residual capacity along x
L6      while some vertex v is active do
L7          if v has an admissible arc x = (v, u) then
L8              push min(excess(v), r_f(x)) along x
L9          else p(v) ← max { p(u) − w(x) : x = (v, u) residual } − ε
L10 until ε = 1
L11 return f
```

Line L1 uses [Edmonds-Karp](/edmonds-karp/); the flow it finds is $\max|w|$-optimal for $p = 0$, since every reduced cost is a cost. Lines L4 to L9 are refine. Line L5 makes every residual arc have $c_p \ge 0$, at the price of creating excesses and deficits. Lines L6 to L9 are push-relabel: line L8 pushes along an admissible arc, and line L9 relabels $v$ when it has none, lowering $p(v)$ so that its best arc gets reduced cost exactly $-\varepsilon$. Pushing never creates an arc with $c_p < -\varepsilon$, since the reverse of an admissible arc has positive reduced cost. The implementation scans arcs with a current-arc pointer per vertex and keeps active vertices in a queue.

## Example

The running network with costs: $s a$ (10, cost 2), $s c$ (10, 2), $a b$ (4, 6), $a c$ (2, 3), $a d$ (8, 1), $c d$ (9, 2), $d b$ (6, 1), $b t$ (10, 1), $d t$ (10, 3), where the pairs are capacity and cost. Here $n = 6$, so the costs are multiplied by 7, and the largest scaled cost is $42$.

**Line L1.** Edmonds-Karp gives the flow $10, 9, 4, 0, 6, 9, 5, 9, 10$ on the edges in that order, value 19 and cost 130, as on the page on [cycle canceling](/cycle-canceling/).

**First refine, $\varepsilon = 21$.** With $p = 0$, the backward arc of every edge that carries flow has negative reduced cost, so line L5 empties every edge: the flow becomes 0, $s$ has excess 19 and $t$ has excess $-19$. Lines L6 to L9 then send the 19 units from $s$ back to $t$, relabeling vertices as they run out of admissible arcs; this is like a shortest path computation with tolerance 21. The refine makes 33 pushes and 14 relabels and ends with the flow $10, 9, 3, 0, 7, 9, 6, 9, 10$ of cost 126.

**Later refines.** The values of $\varepsilon$ are 21, 11, 6, 3, 2 and 1, with 33, 18, 15, 14, 7 and 16 pushes and 14, 9, 8, 8, 3 and 10 relabels. The cost stays 126: the first refine already found an optimal flow, and the later ones only tighten the potentials until they prove it. After the refine with $\varepsilon = 1$, every residual arc has scaled reduced cost at least $-1$, so every residual cycle has scaled cost at least $-6 > -7$, and since scaled cycle costs are multiples of 7, no cycle has negative cost. The result agrees with cycle canceling.

**Edge cases.** With $s \to a$ and $t \to a$ only there is no s-t path, the maximum flow is 0, and refine finds no negative reduced cost, so the result is the zero flow of cost 0. An edge of capacity 0 with cost $-9$ has no residual arc and is never used. A negative cycle away from $s$ and $t$, such as $a \to b$ (capacity 3, cost $-2$) with its antiparallel edge $b \to a$ (5, cost 1), is saturated by line L5 and stays saturated: each of the two edges ends with flow 3, kept separately.

## Correctness

The [correctness proof](proofs/correctness.md) shows four facts. Refine keeps $\varepsilon$-optimality: line L5 makes all reduced costs nonnegative, a push only adds the reverse of an admissible arc, whose reduced cost is positive, and a relabel lowers $p(v)$ by at least $\varepsilon$ to exactly the level where the best arc has reduced cost $-\varepsilon$. Refine ends: an active vertex always has a residual path to a vertex of negative excess that is a reversed path of the flow at the start of the refine, which bounds the total drop of $p(v)$ by $3(n - 1)\varepsilon$ and so the relabels by $3n$ per vertex. When refine ends, all excesses are 0, so the flow conserves at every vertex other than $s$ and $t$ and keeps the maximum value. Finally, a 1-optimal flow for costs scaled by $n + 1$ has no negative residual cycle, so it is a cheapest maximum flow.

## Complexity

Line L1 costs $O(nm^2)$. The value of $\varepsilon$ starts at most $(n + 1)C$ and roughly halves, so there are $O(\log(nC))$ refines. In one refine, each vertex is relabeled at most $3n$ times, so there are $O(n^2)$ relabels, each costing $O(\deg v)$, for $O(nm)$ total. Between two relabels of $v$, each arc out of $v$ is saturated at most once, so there are $O(nm)$ saturating pushes. Non-saturating pushes are bounded by $O(n^2 m)$ with the usual potential argument of push-relabel for any order of processing, and by $O(n^3)$ for the first-in first-out order. So the total is $O(nm^2 + n^2 m \log(nC))$; the FIFO bound gives $O(n^3 \log(nC))$ for the refines, and Goldberg and Tarjan's dynamic tree version gives $O(nm \log(n^2/m) \log(nC))$. The extra space is $\Theta(n + m)$.

## Properties

- **Weakly polynomial.** The bound depends on $\log C$, not on capacities. Strongly polynomial variants exist, such as Goldberg and Tarjan's minimum mean cycle canceling and Orlin's algorithm.
- **Integral.** With integer capacities every push is an integer, so the result is an integral flow.
- **Potentials as a certificate.** The final potentials $p / (n + 1)$ satisfy $c_p(x) > -1$ on every residual arc in original units, and they can be rounded to an exact dual solution with one shortest path computation.
- **Not monotone in cost.** A refine may raise the cost temporarily, unlike cycle canceling, as line L5 throws flow away.

## Variants and improvements

- **Wave and FIFO orders** give $O(n^3)$ per refine; **dynamic trees** give $O(nm \log(n^2/m))$ per refine.
- **Heuristics of CS2** (Goldberg 1997): price updates by a Dijkstra-like search, arc fixing for arcs whose reduced cost is so large that they can never change, price refinement that checks whether the current flow is already optimal for a smaller $\varepsilon$, and push lookahead.
- **Double scaling** (Ahuja, Goldberg, Orlin and Tarjan) scales capacities and costs together for $O(nm \log\log U \log(nC))$.
- **Assignment problems.** The same method with $\varepsilon$-scaling is the cost scaling [auction algorithm](/auction-algorithm/) of Bertsekas and the Goldberg-Kennedy assignment code.
- **Exact alternatives.** [Network simplex](/network-simplex/) and [successive shortest paths](/successive-shortest-path/) are often used in practice too; the almost-linear algorithms of 2022 also solve min-cost flow, in theory much faster.

## When to use it

Use cost scaling for large min-cost flow and assignment instances with integer costs, where its bound does not depend on capacities and the CS2 heuristics make it fast. For small instances or teaching, [cycle canceling](/cycle-canceling/) or successive shortest paths are simpler. If costs are real numbers, scale and round them, or use a strongly polynomial method.

## Pitfalls

- **Forgetting to scale costs by $n + 1$** or using $\varepsilon \ge 1/n$ in original units as the stop: the result can then be off by a negative cycle.
- **Relabeling to the wrong value.** The new potential must be the maximum over residual arcs of $p(u) - w(x)$, minus $\varepsilon$; lowering by less does not create an admissible arc, lowering by more breaks the relabel bound.
- **Measuring excess against zero instead of the start of the refine** at $s$ and $t$: they carry net flow, and treating that as excess pushes it back.
- **Self-loops.** A self-loop with negative cost is a negative cycle by itself; the code fills it at the start and keeps it out of the push-relabel loop, where it could stall a relabel.
- **Merging antiparallel edges** with different costs changes the optimum.

## Implementations

The Python version takes the vertex count, a list of edges $(u, v, \text{cap}, \text{cost})$ with integer entries and $s, t$, and returns the value, the least cost and the flow on each input edge. It runs Edmonds-Karp, then refines with a first-in first-out queue of active vertices and current-arc pointers. An optional callback reports $\varepsilon$, the numbers of pushes and relabels, and the cost after each refine.

## History

The idea of $\varepsilon$-optimality, or $\varepsilon$-complementary slackness, comes from Bertsekas's auction algorithm (1979) and from Tardos's strongly polynomial algorithm (1985). Goldberg and Tarjan combined it with push-relabel and cost scaling in 1987, with the journal version in 1990. Goldberg's CS2 implementation of 1997 made it a standard practical solver.

## References
