---
tag: AM5BV8
kind: algorithm
slug: ford-fulkerson
name: Ford-Fulkerson algorithm
aliases:
- Ford-Fulkerson method
- augmenting path method
area: graphs/flows-and-cuts
level: intro
summary: Repeatedly augment flow along s-t paths in the residual graph until none remain.
solves: [max-flow-problem, min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, F: the value of a maximum flow (integer capacities)}
  time: {worst: O((n + m) F)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1956
  people: [L. R. Ford Jr., D. R. Fulkerson]
  note: Ford and Fulkerson published the max-flow min-cut theorem in 1956 and a labeling method that finds augmenting paths in 1957.
prereqs: [flow-network, s-t-flow, residual-graph, augmenting-path-flow, depth-first-search]
see_also: [edmonds-karp, dinic, max-flow-min-cut-theorem, flow-integrality-theorem, capacity-scaling, fattest-augmenting-path, push-relabel, bipartite-matching]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2, The Ford-Fulkerson method (residual networks, augmenting paths, cuts, the max-flow min-cut theorem, the basic algorithm and its O(E f*) analysis with integer capacities)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.1, The Maximum-Flow Problem and the Ford-Fulkerson Algorithm, and Section 7.2, Maximum Flows and Minimum Cuts in a Network
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (Ford and Fulkerson's augmenting-path algorithm, its integer analysis, and the example with irrational capacities)
  - paper: doi:10.4153/CJM-1956-045-5
    title: L. R. Ford Jr. and D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics 8, 399 to 404 (1956)
    locator: the whole paper (the max-flow min-cut theorem)
---

The Ford-Fulkerson algorithm solves the [maximum flow problem](/max-flow-problem/): starting from the zero flow, it finds a path from $s$ to $t$ in the [residual graph](/residual-graph/), pushes as much flow as the path allows, and repeats until no such [augmenting path](/augmenting-path-flow/) is left. The final residual graph also gives a [minimum cut](/min-cut-problem/). With integer capacities it ends after at most $F$ augmentations, where $F$ is the maximum flow value, so it takes $O((n + m) F)$ time; with irrational capacities it may never end. It is a method more than one algorithm: the rule that picks the path decides the running time, and [Edmonds-Karp](/edmonds-karp/), [the fattest path rule](/fattest-augmenting-path/) and [capacity scaling](/capacity-scaling/) are choices of this rule.

## In plain words

You have a network of one-way pipes, each with a limit, and you want to send as much water as you can from the source to the drain. Start with no water. Look for any route from the source to the drain on which every pipe can take more. A route may also go backwards through a pipe that already carries water: that means sending less water through that pipe, which frees it for a better plan.

When you find a route, send as much as its tightest step allows, and update what each pipe can still take. Then look for another route. When no route is left, stop. At that moment the places you can still reach from the source form a wall; every pipe through the wall is full, so nothing more can get through, and the water you send is the most possible.

## The problem

The input is a [flow network](/flow-network/) $N = (G, c, s, t)$: a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, capacities $c(e) \ge 0$, and two vertices $s \ne t$. The output is a maximum [s-t flow](/s-t-flow/) $f$ and the source side $S$ of a minimum s-t [cut](/cut/).

**Assumptions.** The graph is directed; an undirected edge is given as two directed edges. Capacities are nonnegative integers for the time bound; rationals reduce to integers by scaling; for irrational capacities the method need not terminate (see Complexity). Antiparallel edges, parallel edges, self-loops and zero-capacity edges are allowed: each edge $e$ keeps its own forward residual edge $e^+$ and backward residual edge $e^-$, so two antiparallel edges give four residual edges, never one merged edge. A zero-capacity edge has no residual edge until it carries flow, which it never does. If no path leads from $s$ to $t$, the answer is the zero flow and the set of vertices that $s$ reaches.

## The algorithm

The algorithm keeps the residual capacities $c_f$ and reads the flow from them: $f(e) = c_f(e^-)$ and $c_f(e^+) = c(e) - f(e)$.

```pseudo id=main
FORD-FULKERSON(G, c, s, t)
L1  for each edge e do c_f(e⁺) ← c(e), c_f(e⁻) ← 0      ▷ the zero flow
L2  while G_f has a path P from s to t of edges x with c_f(x) > 0 do
L3      Δ ← min { c_f(x) : x in P }                     ▷ the bottleneck
L4      for each residual edge x in P do
L5          c_f(x) ← c_f(x) − Δ
L6          c_f(reverse of x) ← c_f(reverse of x) + Δ    ▷ e⁺ and e⁻ are reverses
L7  S ← the set of vertices reachable from s in G_f
L8  return f with f(e) = c_f(e⁻) for each e, and S
```

Line L2 may use any graph search; this page and its code use [depth-first search](/depth-first-search/) over the out-arcs of each vertex in input order, which is the textbook form. Lines L5 and L6 move $\Delta$ units from a residual edge to its reverse. For a forward edge $e^+$ this raises $f(e)$ by $\Delta$; for a backward edge $e^-$ it lowers $f(e)$ by $\Delta$, which cancels flow that an earlier path sent the wrong way. Line L7 is one more search, and line L8 reads the flow off the backward capacities.

## Example

The network is the running example of the area: $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10. Each vertex tries its out-arcs in input order; the backward arc of an edge $(u, v)$ sits in the list of $v$ at the position where the edge was read. The searches of line L2 find:

| round | augmenting path (residual edges) | $\Delta$ | value |
|---|---|---|---|
| 1 | $s\,a$, $a\,b$, $b\,t$ | 4 | 4 |
| 2 | $s\,a$, $a\,c$, $c\,d$, $d\,b$, $b\,t$ | 2 | 6 |
| 3 | $s\,a$, $a\,d$, $d\,b$, $b\,t$ | 4 | 10 |
| 4 | $s\,c$, $c\,a$ (backward edge of $a c$), $a\,d$, $d\,t$ | 2 | 12 |
| 5 | $s\,c$, $c\,d$, $d\,t$ | 7 | 19 |

In round 4 the search reaches $c$, and the edge $a c$ carries 2 units from round 2, so its backward edge $(c, a)$ has residual capacity 2. Using it moves those 2 units off $a c$: the flow that went $a \to c \to d$ now goes $s \to c \to d$, and $a$ can send 2 more units to $d$ instead. After round 5 the flow is $f(s, a) = 10$, $f(s, c) = 9$, $f(a, b) = 4$, $f(a, c) = 0$, $f(a, d) = 6$, $f(c, d) = 9$, $f(d, b) = 6$, $f(b, t) = 10$, $f(d, t) = 9$. From $s$ the residual graph reaches only $c$ (by $s c$, residual 1); from $c$ the edge $c d$ is full and $a c$ is empty. So $S = \{s, c\}$, and the cut capacity is $c(s, a) + c(c, d) = 10 + 9 = 19$, equal to the value.

## Correctness

**Theorem.** If FORD-FULKERSON terminates, it returns a maximum s-t flow $f$ and the source side $S$ of a minimum s-t cut, with $|f| = c(S, V \setminus S)$. With integer capacities it terminates after at most $F$ rounds, and the flow is integral.

The invariant of the loop of line L2 is: *the values $f(e) = c_f(e^-)$ form an s-t flow, $c_f(e^+) + c_f(e^-) = c(e)$ for each $e$, and with integer capacities all $c_f$ are integers*. Line L1 makes it true, and one round keeps it true by the augmentation lemma of [augmenting path](/augmenting-path-flow/), while the value grows by $\Delta > 0$. When the loop stops, $t \notin S$; every edge from $S$ to $V \setminus S$ is full and every edge back is empty, so the value equals the cut capacity, and by weak duality both are optimal. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/) with integer capacities that fit in a word; each addition and comparison is $O(1)$.

- **One round.** The search of line L2 visits each vertex and arc at most once: $O(n + m)$. Lines L3 to L6 take $O(n)$, since a simple path has at most $n - 1$ edges.
- **Number of rounds, integer capacities.** Each $\Delta$ is a positive integer, so each round raises the value by at least 1, and the value never exceeds $F$. So there are at most $F$ rounds, and the time is $O((n + m) F)$. With $F \le \sum_{e \text{ out of } s} c(e) \le m U$, where $U$ is the largest capacity, this is $O(m^2 U)$ when every vertex has an edge. This bound is pseudo-polynomial: it grows with the value of the numbers, not with their length.
- **The bound is reached.** In the network $s a$, $s b$, $a t$, $b t$ of capacity $X$ and $a b$ of capacity 1, the paths $s\,a\,b\,t$ and $s\,b\,a\,t$ (through the backward edge of $a b$) each have bottleneck 1. A search that alternates between them takes $2X$ rounds, while two rounds suffice.
- **Rational capacities.** Multiply all capacities by the common denominator $D$; the rounds are the same, so there are at most $D \cdot F$ of them.
- **Irrational capacities.** Ford and Fulkerson gave a network with irrational capacities on which a bad choice of paths never ends, and the values converge to a number below the maximum. Zwick (1995) found the smallest such networks. With real capacities, use a rule with a strongly polynomial bound, such as [Edmonds-Karp](/edmonds-karp/), which needs $O(nm)$ rounds whatever the capacities are.
- **Space.** Two residual capacities per edge, the adjacency lists and the search arrays: $\Theta(n + m)$ extra words.

## Properties

- **Integral.** With integer capacities every $\Delta$ and every flow value is an integer, so the result is an integral maximum flow. This proves the [integrality theorem](/flow-integrality-theorem/).
- **Certificate.** The set $S$ is a minimum cut of the same capacity as the flow, so the answer is easy to check in $O(n + m)$.
- **Any start.** The loop works from any feasible flow, not only from zero. This allows warm starts after a capacity increase.
- **Monotone value.** The value grows in each round, but the flow on a single edge can go down, through a backward edge.
- **Not strongly polynomial.** The number of rounds depends on the capacities.

## Variants and improvements

- **[Edmonds-Karp](/edmonds-karp/).** Pick a shortest augmenting path by [breadth-first search](/breadth-first-search/). At most $nm/2$ rounds, so $O(nm^2)$ time for any real capacities.
- **[Fattest augmenting path](/fattest-augmenting-path/).** Pick the path with the largest bottleneck. $O(m \log F)$ rounds with integer capacities.
- **[Capacity scaling](/capacity-scaling/).** Use only residual edges of capacity at least $\Delta$, and halve $\Delta$. $O(m \log U)$ rounds, $O(m^2 \log U)$ time.
- **[Dinic's algorithm](/dinic/).** Push a [blocking flow](/blocking-flow/) along all shortest paths at once. $O(n^2 m)$ time.
- **[Push-relabel](/push-relabel/).** A different method that works with [preflows](/preflow/) instead of paths.
- **Bipartite matching.** On a unit-capacity network built from a bipartite graph, $F \le n$ and Ford-Fulkerson takes $O(nm)$ time. This is the augmenting path algorithm for [bipartite matching](/bipartite-matching/).

## When to use it

Use the plain method when the maximum flow value is small, for example with unit capacities ([edge-disjoint paths](/edge-disjoint-paths/), bipartite matching), where $O((n + m) F)$ is fast and the code is short. For large integer capacities, use [capacity scaling](/capacity-scaling/) or [Dinic's algorithm](/dinic/). For real capacities, use a rule with a strongly polynomial bound: [Edmonds-Karp](/edmonds-karp/), Dinic or [push-relabel](/push-relabel/).

## Pitfalls

- **No backward edges.** If line L6 is left out, a search can only follow edges that are not full, and the method can stop with a flow that is not maximum. In the network $s a$, $s b$, $a b$, $a t$, $b t$ with capacity 1 each, the first path $s\,a\,b\,t$ blocks both $s a$ and $b t$, and value 2 needs the backward edge $(b, a)$.
- **Merging antiparallel edges.** Storing one residual entry per ordered pair $(u, v)$ is right only if it holds $c_f(e^+)$ of the edge $(u, v)$ plus $c_f(e'^-)$ of the edge $(v, u)$. Overwriting one with the other loses capacity. Keep a separate arc pair per edge, as in line L1.
- **Searching in $G$ instead of $G_f$.** A path in $G$ through a zero-capacity or full edge is not an augmenting path. Line L2 must test $c_f(x) > 0$.
- **Recursion depth.** A recursive DFS on a long path exceeds the stack in many languages. Use an explicit stack.
- **Floating-point capacities.** Rounding can leave a residual capacity of $10^{-17}$ and make many tiny rounds, or none. Use exact numbers, or treat values below a tolerance as zero and accept an approximate answer.

## Implementations

The Python version takes the vertex count, a list of edges $(u, v, c)$ and $s, t$, and returns the value, the flow on each input edge and the sorted source side of a minimum cut. It works with integers and with `Fraction` values.

## History

L. R. Ford Jr. and D. R. Fulkerson proved the max-flow min-cut theorem in a paper published in 1956, and in 1957 they published a simple labeling algorithm that finds augmenting paths. Their book Flows in Networks (1962) collects the theory, including the example with irrational capacities. Edmonds and Karp (1972) and, independently, Dinic (1970) showed that shortest augmenting paths give a polynomial bound.

## References
