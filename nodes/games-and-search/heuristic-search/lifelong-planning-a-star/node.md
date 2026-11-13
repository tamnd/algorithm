---
tag: X7W103
kind: algorithm
slug: lifelong-planning-a-star
name: Lifelong planning A*
aliases:
- "LPA*"
area: games-and-search/heuristic-search
level: research
summary: "Incremental A*: after edge costs change, it repairs the g-values of the last search and expands only the locally inconsistent vertices, so a new shortest path often costs a few expansions."
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, d: the largest number of predecessors of a vertex}
  time: {per-call: O((n + m)(d + log n))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [a-star-search, consistent-heuristic, dijkstra]
see_also: [d-star-lite, d-star, ramalingam-reps, dynamic-single-source-shortest-paths, replanning, anytime-repairing-a-star, optimal-efficiency-of-a-star]
sources:
  - paper: doi:10.1016/j.artint.2003.12.001
    title: Sven Koenig, Maxim Likhachev and David Furcy, Lifelong Planning A*, Artificial Intelligence 155(1-2) (2004)
    locator: pp. 93 to 146; Figure 3 (the pseudocode, lines 01 to 23), Section 5 (Theorems 1 to 11, among them Theorem 4 on at most two expansions, Theorem 7 on the similarity to A* and Theorems 10 and 11 on efficiency), Section 6 (the optimized version, Figure 7) and Section 8 (experiments)
  - paper: doi:10.1006/jagm.1996.0046
    title: G. Ramalingam and Thomas Reps, An incremental algorithm for a generalization of the shortest-path problem, Journal of Algorithms 21(2) (1996)
    locator: pp. 267 to 305 (DynamicSWSF-FP, the incremental algorithm with g and rhs values and local consistency that LPA* extends)
  - paper: Bernhard Nebel and Jana Koehler, Plan reuse versus plan generation, a theoretical and empirical analysis, Artificial Intelligence 76(1-2) (1995)
    title: Bernhard Nebel and Jana Koehler, Plan reuse versus plan generation, a theoretical and empirical analysis, Artificial Intelligence 76(1-2) (1995)
    locator: pp. 427 to 454 (plan reuse is not easier than plan generation in the worst case, the result that Koenig, Likhachev and Furcy cite for incremental search)
  - paper: doi:10.1109/TRO.2004.838026
    title: Sven Koenig and Maxim Likhachev, Fast replanning for navigation in unknown terrain, IEEE Transactions on Robotics 21(3) (2005)
    locator: pp. 354 to 363 (D* Lite, built on LPA*, with a summary of LPA*)
---

Lifelong planning A* (LPA*) finds a shortest path from a fixed start vertex to a fixed goal vertex again and again, while the edge costs of the graph change between the searches. Its first search does the same work as [A*](/a-star-search/). After a change, it does not start from scratch. It keeps for each vertex the estimate $g$ of its start distance from the last search and a one-step lookahead value $\mathrm{rhs}$, and it repairs only the vertices where the two values differ and that can matter for the goal. Koenig, Likhachev and Furcy introduced it, and the journal version appeared in 2004. It combines A* with the incremental shortest path algorithm DynamicSWSF-FP of [Ramalingam and Reps](/ramalingam-reps/), and [D* Lite](/d-star-lite/) is built on it.

## In plain words

You have found the best route across a town, and you remember how far each street corner is from your house. Then the radio says that one bridge is closed. Most of the corners are still as far from your house as before, so you do not need to work them out again. You look only at the corners next to the bridge. Each corner can check its own distance against its neighbours: "my distance should be the best neighbour's distance plus the street between us." If a corner fails this check, you fix it and then look at the corners after it. You start with the fixes that look most promising for the trip to the goal, as A* does, and you stop as soon as no fix can change the best route.

## The problem

The input is a finite directed graph $G = (S, E)$ with a start vertex $s_{start}$, a goal vertex $s_{goal}$, and positive edge costs $c(u, v) > 0$, where $c(u, v) = \infty$ means that the edge is blocked. A heuristic $h$ gives a finite value $h(s) \ge 0$ for each vertex. It must be [consistent](/consistent-heuristic/) for every version of the costs: $h(s_{goal}) = 0$ and $h(u) \le c(u, v) + h(v)$ for each edge. After each batch of cost changes, the output is $g^*(s_{goal})$, the cost of a shortest path from $s_{start}$ to $s_{goal}$ under the current costs, and such a path. We write $g^*(s)$ for the start distance of $s$, $\mathrm{Pred}(s)$ and $\mathrm{Succ}(s)$ for the predecessors and successors of $s$, and we compare keys, which are pairs, in lexicographic order. Each single search is a [single-pair shortest path](/single-pair-shortest-path/) problem. The sequence is a dynamic version of it, close to the [dynamic single-source shortest paths](/dynamic-single-source-shortest-paths/) problem but with one target.

The cost of a search is counted in vertex expansions, as for A*.

## The algorithm

Each vertex $s$ has two values. The value $g(s)$ is the current estimate of the start distance. The value $\mathrm{rhs}(s)$ is computed from the $g$-values of the predecessors:
$$ \mathrm{rhs}(s) = \begin{cases} 0 & \text{if } s = s_{start}, \\ \min_{s' \in \mathrm{Pred}(s)} \big(g(s') + c(s', s)\big) & \text{otherwise.} \end{cases} $$
A vertex is *locally consistent* when $g(s) = \mathrm{rhs}(s)$. When all vertices are locally consistent, $g = g^*$ everywhere. A vertex is *locally overconsistent* when $g(s) > \mathrm{rhs}(s)$, which happens when a cheaper way to it appeared, and *locally underconsistent* when $g(s) < \mathrm{rhs}(s)$, which happens when its old path became more expensive. The priority queue $U$ holds exactly the locally inconsistent vertices, with the key
$$ k(s) = \big[\min(g(s), \mathrm{rhs}(s)) + h(s);\ \min(g(s), \mathrm{rhs}(s))\big] . $$
The first component plays the role of $f = g + h$ in A*, and the second breaks ties toward smaller $g$.

```pseudo id=main
CALCULATE-KEY(s)
L1  return [min(g(s), rhs(s)) + h(s); min(g(s), rhs(s))]

INITIALIZE()
L2  U ← ∅
L3  for each s ∈ S do rhs(s) ← g(s) ← ∞
L4  rhs(s_start) ← 0
L5  U.INSERT(s_start, CALCULATE-KEY(s_start))

UPDATE-VERTEX(u)
L6  if u ≠ s_start then rhs(u) ← min over s′ ∈ Pred(u) of g(s′) + c(s′, u)
L7  if u ∈ U then U.REMOVE(u)
L8  if g(u) ≠ rhs(u) then U.INSERT(u, CALCULATE-KEY(u))

COMPUTE-SHORTEST-PATH()
L9  while U.TOPKEY() < CALCULATE-KEY(s_goal) or rhs(s_goal) ≠ g(s_goal) do
L10     u ← U.POP()
L11     if g(u) > rhs(u) then                       ▷ overconsistent
L12         g(u) ← rhs(u)
L13         for each s ∈ Succ(u) do UPDATE-VERTEX(s)
L14     else                                        ▷ underconsistent
L15         g(u) ← ∞
L16         for each s ∈ Succ(u) ∪ {u} do UPDATE-VERTEX(s)

MAIN()
L17 INITIALIZE()
L18 forever do
L19     COMPUTE-SHORTEST-PATH()
L20     wait for changes of edge costs
L21     for each directed edge (u, v) whose cost changed do
L22         c(u, v) ← the new cost
L23         UPDATE-VERTEX(v)
```

The lines follow Figure 3 of the paper, which numbers them 01 to 23. An overconsistent vertex gets its new, lower value at line L12, as in an expansion of A*. An underconsistent vertex is set to $\infty$ at line L15, so it becomes overconsistent or consistent, and its successors see that their old support is gone. After a call, a shortest path is read backward: start at $s_{goal}$ and go to a predecessor $s'$ that minimizes $g(s') + c(s', s)$, until $s_{start}$.

With $h = 0$ the algorithm is an incremental version of breadth-first search or of [Dijkstra's algorithm](/dijkstra/). It is DynamicSWSF-FP with a stop rule for one goal. The heuristic focuses the repair on vertices that can be on a shortest path, as in A*.

## Example

The graph has the edges S→A 1, S→B 2, A→C 1, B→C 2, C→G 2, B→D 3, D→G 2 and A→D 4, with start S and goal G. The heuristic is $h$ = 3, 2, 2, 2, 2, 0 for S, A, B, C, D, G, which is consistent.

**First call.** Only S is in $U$, with key [3; 0]. The call expands, in this order:

| step | expanded, key | kind | what changes |
| --- | --- | --- | --- |
| 1 | S [3; 0] | over | $g$(S) = 0; rhs(A) = 1, rhs(B) = 2 |
| 2 | A [3; 1] | over | $g$(A) = 1; rhs(C) = 2, rhs(D) = 5 |
| 3 | B [4; 2] | over | $g$(B) = 2; C and D keep their rhs |
| 4 | C [4; 2] | over | $g$(C) = 2; rhs(G) = 4 |
| 5 | G [4; 4] | over | $g$(G) = 4 |

Now G is consistent and the top key of $U$ is D [7; 5] > [4; 4], so the call stops with cost 4 and the path S-A-C-G. These are the 5 expansions of A* with ties toward smaller $g$; D has $f = 7 > 4$ and is not expanded.

**The change.** The edge A→C goes up from 1 to 5. Line L23 recomputes rhs(C) = min(1 + 5, 2 + 2) = 4. Now $g$(C) = 2 < rhs(C) = 4, so C is underconsistent, with key [4; 2].

**Second call.**

| step | expanded, key | kind | what changes |
| --- | --- | --- | --- |
| 1 | C [4; 2] | under | $g$(C) = ∞; rhs(G) = ∞; C goes back with key [6; 4] |
| 2 | G [4; 4] | under | $g$(G) = ∞; G is consistent |
| 3 | C [6; 4] | over | $g$(C) = 4; rhs(G) = 6 |
| 4 | G [6; 6] | over | $g$(G) = 6 |

The cost is 6 and the path is S-B-C-G. LPA* made 4 expansions. A* from scratch makes 5 on the new graph (S, A, B, C, G). The vertices S, A and B were not touched, because their start distances did not change. If C→G is then blocked, a third call expands G as underconsistent, D as overconsistent with key [7; 5], and G again, and returns cost 7.

**A measured experiment.** A 40 by 40 grid is 4-connected with unit costs. Each cell is blocked with probability 0.25 (the random generator `random.Random(seed)` of Python), and an edge into or out of a blocked cell has cost $\infty$. The start is the corner (0, 0), the goal is (39, 39), and $h$ is the Manhattan distance. In each of 30 rounds, 5 random cells change their state, and both LPA* and A* from scratch (ties toward smaller $g$, the goal expansion counted) compute the new path. The counts are:

| seed | first call, LPA* and A* | LPA*, 30 later calls | A*, 30 later calls | rounds where LPA* expanded more |
| --- | --- | --- | --- | --- |
| 1 | 660 and 660 | 316 | 16,436 | 0 |
| 2 | 419 and 419 | 1,432 | 11,171 | 1 |
| 3 | 796 and 796 | 400 | 20,504 | 0 |

These are measurements on these instances, not bounds. In the bad round of seed 2, LPA* expanded 418 vertices and A* only 6: a change near the start made most of the old $g$-values wrong, so much of the old search had to be undone, while the new path was easy to find from scratch.

## Correctness

The [proof](proofs/correctness.md) shows, for a consistent $h$ and positive costs, that each call of COMPUTE-SHORTEST-PATH stops and returns $g(s_{goal}) = g^*(s_{goal})$, and that the backward trace gives a shortest path. Its main steps are these.

- **Invariants.** At line L9, every rhs-value satisfies its definition, and $U$ holds exactly the locally inconsistent vertices with their current keys. UPDATE-VERTEX is called on each vertex whose rhs or consistency can change.
- **Keys do not go down.** During a call, the keys removed at line L10 form a nondecreasing sequence, and a vertex that comes back into $U$ comes back with a key larger than the key just removed. This is where consistency and $c > 0$ are used.
- **An overconsistent expansion is exact.** When line L10 removes an overconsistent $u$, $\mathrm{rhs}(u) = g^*(u)$. So each vertex is expanded at most once as overconsistent and at most once as underconsistent per call (Theorem 4 of the paper), and the call stops after at most $2n$ expansions.
- **The stop rule is enough.** When $s_{goal}$ is consistent and no key in $U$ is smaller than its key, a shortest path to $s_{goal}$ cannot pass through a vertex with a wrong $g$-value.

The paper proves more about the work. The first call expands the vertices in the same order as A* with ties toward smaller $g$ (Theorem 7). An overconsistent expansion in any call has the key $[g^*(s) + h(s); g^*(s)]$, so it happens only to vertices with $g^*(s) + h(s) \le g^*(s_{goal})$, as in A* (Theorems 6 and 8). No vertex whose $g$-value was already equal to its new start distance before the call is expanded (Theorem 10). The tests check these statements on random graphs.

## Complexity

The model is the [word RAM](/word-ram/) with $n$ vertices, $m$ edges and $d$ the largest number of predecessors of a vertex. A call does at most $2n$ expansions. An expansion of $u$ calls UPDATE-VERTEX for the successors of $u$, and once more for $u$ in the underconsistent case. Each such call takes a minimum over at most $d$ predecessors and does $O(1)$ operations on a [binary heap](/binary-heap/) that supports removal, for example an [indexed priority queue](/indexed-priority-queue/). So a call takes $O((n + m)(d + \log n))$ time in the worst case. The space is $O(n)$ for the values and the queue, besides the graph.

This worst case is no better than A* from scratch, and Koenig, Likhachev and Furcy note that incremental search cannot be more efficient than search from scratch in the worst case, citing Nebel and Koehler (1995). The gain is in the typical case. When a change touches the costs far from the start, few start distances change, and the next call expands few vertices. When a change is close to the start, or the old and new shortest path trees have little in common, LPA* can expand more vertices than A*, as the seed 2 round shows, and each expansion costs more than in A*.

In the experiments of the paper (Section 8), on 4-connected grids with 20 percent blocked cells where about 0.6 percent of the cells change before each search, LPA* did better than A* in the long run by their measures, which count vertex expansions and heap operations. The authors also report that against an A* with buckets instead of a heap, and with 1 percent or more of the edges changed before each search, LPA* was not faster than A* in one of their experiments. They conclude only that incremental heuristic search is promising.

## Properties

- **Exact.** After each call, $g(s_{goal})$ is the start distance of the goal under the current costs.
- **The first call is A*.** It expands the same vertices as A* with ties toward smaller $g$.
- **At most two expansions per vertex per call**, at most once overconsistent and at most once underconsistent.
- **Forward search.** It searches from $s_{start}$ to $s_{goal}$, with $h$ toward the goal. D* Lite reverses the direction so that the moving robot is the goal of the search.
- **Memory.** It keeps $g$ and rhs for each vertex from the earlier searches, so it needs about the same memory as A* plus the values of the earlier searches.
- **Not anytime.** Each call runs until the path is optimal. For a bounded suboptimal answer, see [anytime repairing A*](/anytime-repairing-a-star/) and its incremental form.

## Variants and improvements

- **Optimized version.** Section 6 of the paper keeps a parent pointer and updates rhs in $O(1)$ when a successor gets a lower value, recomputes the minimum over predecessors only when the parent got worse, and stops when $\mathrm{rhs}(s_{goal}) \le g(s_{goal})$ instead of requiring equality. The implementation on this page is the basic version.
- **Changes during a call.** Section 7 of the paper moves lines L21 to L23 into the loop, so that changes are seen before the call ends. Termination still holds, but the bound of two expansions per vertex does not.
- **[D* Lite](/d-star-lite/).** LPA* searching backward from the goal, with a key modifier so that the start can move. It is the usual form for robot navigation in unknown terrain, and it gives the same paths as [D*](/d-star/).
- **DynamicSWSF-FP.** The algorithm of Ramalingam and Reps without a heuristic, which repairs all vertices and not only those that matter for one goal.
- **Anytime D*.** Likhachev, Ferguson, Gordon, Stentz and Thrun (2005) combined the incremental repair with the inflated heuristic of anytime repairing A*.

## When to use it

Use LPA* when the same start and goal must be connected again and again on a graph that changes a little at a time, and the changes are mostly far from the start, for example route planning with changing traffic far from the departure, or replanning in symbolic planning when operator costs change. When the start moves, as for a robot, use D* Lite. When each change is large or close to the start, or each search is small, use A* from scratch, which has less overhead per expansion. The page [replanning](/replanning/) covers the planning problem of what to do when a plan fails during execution.

## Pitfalls

- **An inconsistent heuristic.** The proofs need $h(u) \le c(u, v) + h(v)$ for every version of the costs. When costs go down, a heuristic that was consistent can stop being so. Use a heuristic that stays below every possible cost, such as the Manhattan distance with the smallest possible edge cost.
- **Zero costs and self-loops.** The keys argument uses $c > 0$. A self-loop would make rhs(u) depend on g(u), which the algorithm does not handle.
- **Forgetting UPDATE-VERTEX after a change.** Line L23 must be run for the end vertex of every changed edge, or rhs is wrong and the result is wrong.
- **Stale heap entries.** With lazy deletion, an entry whose key is not the current key of the vertex must be skipped, both in POP and in TOPKEY, or a consistent vertex is expanded.
- **Comparing keys by the first component only.** The second component, ties toward smaller $g$, is part of the proofs of Theorem 7 and of the bound of two expansions.
- **Expecting a gain in every round.** It is measured, not guaranteed. A change near the start can make LPA* slower than A*.

## Implementations

## History

Ramalingam and Reps (1996) gave DynamicSWSF-FP, an incremental algorithm for a class of shortest path problems that keeps $g$ and rhs values and repairs the locally inconsistent vertices in the order of a priority queue. Koenig and Likhachev added a heuristic and a stop rule for one goal and called the result Lifelong Planning A*. It appeared in conference papers around 2001 and 2002, and the journal version with all the proofs is Koenig, Likhachev and Furcy (2004) in Artificial Intelligence. The name refers to lifelong learning: the search reuses what it learned in earlier searches. In 2002 Koenig and Likhachev used LPA* to build D* Lite, which is simpler than Stentz's focussed D* and moves the robot along the same paths. The paper also applied LPA* to symbolic planning, in the replanner SHERPA.

## References
