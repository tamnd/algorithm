---
tag: 0RQ6RW
kind: algorithm
slug: a-star-bend-sequencing
name: A* bend sequence search
aliases:
- Gupta bend planner
area: cad/manufacturing-process-planning
level: advanced
summary: Gupta, Bourne, Kim and Krishnan's planner that searches bend orders with A*, with costs from tool changes and handling and collision checks from geometry.
solves: [bend-sequence-planning]
model: real-ram
complexity:
  vars: {n: number of bends, k: number of tools}
  time: {worst: "O(2^n n k^2 (n + log k))"}
  space: {extra: "O(2^n n k^2)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1998
  people: [Satyandra K. Gupta, David A. Bourne, K. H. Kim, S. S. Krishnan]
  note: Gupta, Bourne, Kim and Krishnan used A* over partial bend sequences in a planner for a robotic press brake. They chose heuristics that can overestimate, for speed, so their plans are near optimal. The admissible heuristic on this page makes the search exact.
prereqs: [bend-sequence-planning, a-star-search]
see_also: [consistent-heuristic, admissible-heuristic, uniform-cost-search, weighted-a-star, collision-detection, flat-pattern-development, springback-compensation, computer-aided-process-planning]
sources:
  - paper: doi:10.1016/s0278-6125(98)80002-2
    title: S. K. Gupta, D. A. Bourne, K. H. Kim and S. S. Krishnan, Automated process planning for sheet metal bending operations, Journal of Manufacturing Systems 17(5), 1998, 338 to 360
    locator: the central operation planner that runs A* over partial bend sequences, the tooling, grasping and moving planners that give the costs and the feasibility tests, and the heuristics that can overestimate, chosen for speed
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2), 1968, 100 to 107
    locator: the A* algorithm, the optimality of its result with an admissible heuristic, and the consistency condition under which no state is expanded twice
  - paper: doi:10.1016/s0007-8506(07)62155-6
    title: M. Shpitalni and D. Saddan, Automatic determination of bending sequence in sheet metal products, CIRP Annals 43(1), 1994, 23 to 26
    locator: the bend sequence and the tools stated as one graph search, an earlier form of the search on this page
  - paper: doi:10.1115/1.2826245
    title: B. Radin, M. Shpitalni and I. Hartman, Two-stage algorithm for determination of the bending sequence in sheet metal products, Journal of Mechanical Design 119(2), 1997, 259 to 266
    locator: a fast search for a feasible sequence, then a search for a cheaper one within a time limit, the main alternative to A*
  - paper: doi:10.1016/0924-0136(94)90169-4
    title: L. J. de Vin, J. de Vries, A. H. Streppel, E. J. W. Klaassen and H. J. J. Kals, The generation of bending sequences in a CAPP system for sheet-metal components, Journal of Materials Processing Technology 41(3), 1994, 331 to 339
    locator: bend sequences from a search with collision and tolerance tests and handling rules
---

A* bend sequence search plans the order of the bends of a sheet metal part on a press brake, and the tool of each bend, with [A* search](/a-star-search/). A state is the set of bends already made, with the sign of the last bend and the last tool. The shape of the part depends only on the set of bends made, so a collision test of the next bend needs only this set. A step costs a turn of the part when the sign of the bend changes, and a tool change when the tool changes. Gupta, Bourne, Kim and Krishnan (1998) built a planner of this kind for a robotic press brake, with heuristics that can overestimate. This page gives a heuristic that is consistent, so the search returns a cheapest plan, and proves it. This page differs from [bend sequence planning](/bend-sequence-planning/): that page states the problem and its costs, and this page is one exact search method for it.

## In plain words

Bend the part in your head one bend at a time. After each bend, note which bends are done, the last tool and which way up the part was. That note is a state. From a state, try every bend left with every tool that fits it. If the part hits the punch or the die, drop that move. Else the move costs a tool change, a turn of the part, both or nothing.

A* always takes the open state with the least cost so far plus a guess of the cost to come. If some bend left needs the part the other way up, at least one more turn is needed. If the last tool does not fit some bend left, at least one more tool change is needed. The guess never says too much, so the first finished plan that A* takes is a cheapest one.

## The problem

**Input.** A planar profile of $n + 1$ flanges with integer lengths $l_0, \dots, l_n$. Bend $b$, for $1 \le b \le n$, joins flanges $b - 1$ and $b$, and turns the profile by 90 degrees to the left ($s_b = +1$) or to the right ($s_b = -1$) as you walk from flange $0$ to flange $n$. A list of $k$ tools, each a triple $(w, D, m)$: punch width, die width and smallest flange. Two weights $\textit{flip} \ge 0$ and $\textit{change} \ge 0$.

**Shape after a set of bends.** A bend is either not done, and the profile is straight there, or done fully. So the shape after a set $S$ of bends does not depend on their order.

**Collision rule.** This is a toy rule, the model of the code. Put the part in the frame of bend $b$: the bend at the origin, flange $b$ along $+x$ and flange $b - 1$ along $+y$, with the profile mirrored if $s_b = -1$, which is the part turned over. Draw the profile with the bends of $S \cup \{b\}$ done. Tool $(w, D, m)$ can make bend $b$ if both flanges next to $b$ have length at least $m$ (the fit), and no point of the profile is in the open punch region $\{x > 0, y > 0, \lvert x - y \rvert < w\}$ or in the open die region $\{x + y < 0, \lvert x - y \rvert < D\}$. The punch is a blade of half width $w / \sqrt 2$ along the bisector inside the bend, and the die is a block along the bisector outside it. The rule tests the part at the end of the stroke, not during it.

**Cost.** A plan is an order of all bends with a tool for each, where each bend can be made after the bends before it. It costs $\textit{flip}$ for each pair of consecutive bends with different signs, and $\textit{change}$ for each pair with different tools.

**Output.** A plan of least cost, or "none" if no plan exists.

## The algorithm

A state is $u = (S, \sigma, \tau)$: the set $S$ of bends done, the sign $\sigma$ of the last bend ($0$ at the start) and the last tool $\tau$ (none at the start). Let $R = B \setminus S$ be the bends left. A tool *fits* a bend when both flanges next to it are at least its smallest flange; this ignores collisions. The heuristic is $h(u) = 0$ if $R = \emptyset$, and otherwise

$$h(u) = \textit{flip} \cdot \varphi(u) + \textit{change} \cdot \psi(u),$$

where $\varphi(u) = 1$ if $\sigma = 0$ and $R$ holds bends of both signs, or $\sigma \ne 0$ and some bend of $R$ has a sign other than $\sigma$; and $\psi(u) = 1$ if $\tau$ is none and no one tool fits all bends of $R$, or $\tau$ is a tool that does not fit some bend of $R$. Otherwise $\varphi(u) = 0$ and $\psi(u) = 0$.

```pseudo id=main
A*-BENDS(l, s, T, flip, change)
L1  start ← (∅, 0, none); g[start] ← 0; put start in the queue with key h(start)
L2  while the queue is not empty
L3      take u = (S, σ, τ) of least key from the queue; if u is closed, skip it, else close it
L4      if S = B then return the plan along the parent links to u, with cost g[u]
L5      for each bend b ∉ S and each tool t that fits b
L6          if bend b with tool t after the bends of S collides then skip (b, t)
L7          v ← (S ∪ {b}, s_b, t); c ← flip · [σ ∉ {0, s_b}] + change · [τ ∉ {none, t}]
L8          if g[v] is not set or g[u] + c < g[v] then g[v] ← g[u] + c; parent[v] ← u; put v in the queue with key g[v] + h(v)
L9  return none
```

**Line L3.** The queue keeps old copies of a state when line L8 finds a cheaper path. A copy that comes out after the state is closed is skipped. There is no reopening of closed states, which is correct because $h$ is consistent (see [A* search](/a-star-search/)).

**Line L6.** The collision test depends on $S$, $b$ and $t$, and not on $\sigma$ or $\tau$. The code caches it by $(S, b, t)$, so each test runs one time, however many states share the set $S$.

**Exact test.** All points of the profile are integer. A point of a segment is $p + \lambda (q - p)$ with $0 \le \lambda \le 1$, and each open half plane $a x + c y < k$ of a region keeps an open interval of $\lambda$. The code cuts the interval with each half plane in rational arithmetic and asks if what is left is empty. A segment that only touches the boundary of the punch region does not collide, and the test sees that exactly.

## Example

The lipped channel of [bend sequence planning](/bend-sequence-planning/): $l = (1, 4, 6, 4, 1)$, all four signs $+1$, so lip, wall, base, wall, lip. The tools are STANDARD $= (3, 2, 1)$ and GOOSENECK $= (1, 4, 2)$, with $\textit{flip} = 2$ and $\textit{change} = 1$. GOOSENECK does not fit the lip bends $b_1$ and $b_4$, since a lip of 1 is shorter than its smallest flange of 2.

**The collision tests.** A lip bend after the wall next to it collides: after $b_2$, the base stands up at the end of the wall and enters the punch region when $b_1$ is made. The second wall bend needs GOOSENECK. For $b_3$ after $\{b_1, b_2, b_4\}$, the profile in the frame of $b_3$ is the wall from $(0, 0)$ to $(4, 0)$ and its lip to $(4, 1)$, then the base from $(0, 0)$ to $(0, 6)$, the other wall to $(4, 6)$ and its lip to $(4, 5)$. With STANDARD, $w = 3$, and the point $(4, 5)$ has $\lvert x - y \rvert = 1 < 3$, a collision. With GOOSENECK, $w = 1$, the lip at $x = 4$, $5 \le y \le 6$ has $\lvert x - y \rvert \ge 1$, so it only touches the boundary, and the wall at $y = 6$, $x \le 4$ has $\lvert x - y \rvert \ge 2$. No collision.

**The search.** At the start, all signs are equal and STANDARD fits all bends, so $h = 0$. Every state with last tool STANDARD also has $h = 0$. A state with last tool GOOSENECK and a lip left has $h = 1$.

| states taken at line L3 | key | count |
|---|---|---|
| the start; $\{1\}, \{2\}, \{3\}, \{4\}$; $\{1,2\}, \{1,3\}, \{1,4\}, \{2,4\}, \{3,4\}$; $\{1,2,4\}, \{1,3,4\}$, all with STANDARD | 0 | 12 |
| $\{2\}$, $\{3\}$, $\{1,2,4\}$, $\{1,3,4\}$ with GOOSENECK, then $\{1,2,3,4\}$ with GOOSENECK | 1 | 5 |

The state $\{1,2,3,4\}$ with GOOSENECK passes line L4 with cost 1. The plan is $b_1, b_2, b_4$ with STANDARD and $b_3$ with GOOSENECK: one tool change, no turn. A* takes 17 states from the queue, and [uniform cost search](/uniform-cost-search/), which is the same code with $h = 0$, takes 24. A check of all $4! = 24$ orders finds 6 feasible orders, the ones with $b_1$ before $b_2$ and $b_4$ before $b_3$, each with one tool change at best, so the least cost is 1.

## Correctness

**Theorem.** A*-BENDS returns a plan of least cost if a plan exists, and none otherwise.

The proof has three parts. First, plans are exactly the paths from the start to a state with $S = B$ in the graph of lines L5 to L7, with the same cost, because the shape and the collision test depend only on $S$ and the step cost depends only on $\sigma$, $\tau$, $b$ and $t$. Second, $h$ is consistent: for each move from $u$ to $v$ with cost $c$, $h(u) \le c + h(v)$. Take $\varphi$. If $\varphi(u) = 1$ and the move turns the part, it pays $\textit{flip}$. If it does not turn the part, some bend of the other sign is still left in $v$, so $\varphi(v) = 1$. At the start, the bends left have both signs, so after the first bend some bend of the other sign is left. The same holds for $\psi$, because a move uses a tool that fits its bend. With $h = 0$ at the goals, consistency gives admissibility. Third, A* with a consistent heuristic and no reopening returns a cheapest path to a goal set, or reports that none is reachable, as on the [A* search](/a-star-search/) page. The exact clipping makes line L6 the collision rule of the page, with no error from rounding. The full proof is below.

## Complexity

The states are the start and the triples $(S, s_b, t)$ with $S$ a set of bends, so there are at most $1 + 2^n \cdot 2k$ of them. Each is closed at most one time.

- **Lines L5 to L8.** A closed state tries at most $n k$ moves. Each computes $h$ in $O(n)$ and puts at most one entry in the queue. So there are $O(2^n n k^2)$ entries, and each queue operation costs $O(\log(2^n n k^2)) = O(n + \log k)$.
- **Line L6.** With the cache, there are at most $2^n n k$ collision tests. Each clips $n + 1$ segments against two regions of at most 4 half planes, in $O(n)$.

The total time is $O(2^n n k^2 (n + \log k))$, and the extra space is $O(2^n n k^2)$ for the queue, with $O(2^n n k)$ for the cache. The numbers in the clipping are fractions with numerators and denominators at most the total length of the profile, so each operation takes constant time on the real RAM. The search is exponential in $n$, but over sets, not orders: for $n = 7$ there are $2^7 = 128$ sets against $7! = 5040$ orders. A good $h$ cuts the number of states taken from the queue, as in the example, but not the worst case.

## Properties

- **Exact.** The plan has least cost, because $h$ is consistent, and the collision test is exact.
- **Complete.** If no plan exists, the search ends with none after it closes each reachable state.
- **Deterministic.** Ties in the queue go to the state put in first, so the same input gives the same plan.
- **Lower bound only from tools and signs.** The heuristic is at most $\textit{flip} + \textit{change}$. It ignores collisions, which is what keeps it admissible, and also what keeps it weak on parts where the geometry forces several tool changes.

## Variants and improvements

- **Heuristics that overestimate.** Gupta, Bourne, Kim and Krishnan (1998) estimate the cost to go from their tooling and grasping planners. For example, the regrip estimate is the number of groups of bends that one grip can reach, minus one, times the cost of a regrip. Such estimates can be too high, so A* is faster but its plan is only near optimal. [Weighted A*](/weighted-a-star/) is a controlled form of this: with key $g + w h$ and a consistent $h$, the cost is at most $w$ times the least cost.
- **Regrips and grasps.** For a robot, add the grip to the state, and charge a regrip when the next bend cannot be made with the current grip. The heuristic then adds a lower bound on the regrips left.
- **Two stages.** Radin, Shpitalni and Hartman (1997) first find any feasible order with a fast search, then improve its cost within a time limit. This gives an answer fast on large parts, without a guarantee.
- **Graph search over sets.** Shpitalni and Saddan (1994) state the bend order and the tools as one graph search. The search on this page is one form of it, with A* as the method.
- **Swept collisions and real tools.** A real planner checks the motion of the part during the stroke against the true punch, die and machine shapes, in 3D, with [collision detection](/collision-detection/). The search stays the same; only line L6 changes. A good cache at line L6 matters more then, since each test is costly.

## When to use it

Use it when a part has few enough bends that the $2^n$ sets of bends fit in memory, and you want a plan of least cost, or a proof that no plan exists for the given tools. The search grows as $2^n$, so for parts with many more bends, use an estimate that can overestimate, or the two-stage search, and accept a plan that may not be optimal. Use it with a collision test that matches the machine. The toy rule on this page shows the method, not a press brake. The lengths of the flanges should come from the [flat pattern](/flat-pattern-development/) and the formed shape, with [springback compensation](/springback-compensation/), so that the profile that line L6 tests is the profile that the brake makes.

## Pitfalls

- **Cache key at line L6.** The collision test depends on the set $S$, the bend $b$ and the tool $t$. A cache keyed by $S$ alone, or by $(S, b)$, gives the result of one tool to another. In the example, $b_3$ after $\{b_1, b_2, b_4\}$ collides with STANDARD but not with GOOSENECK. A key that adds $\sigma$ and $\tau$ is correct but wastes tests.
- **Old copies at line L3.** Without the check that a state is closed, an old copy of a state with a higher key is expanded again. The plan stays correct, but the work grows. If instead the code marks a state closed when line L8 puts it in the queue, a cheaper path found later is lost, and the plan can cost too much.
- **Goal test at line L8.** Test for $S = B$ when a state leaves the queue at line L4, not when line L8 puts it in. The first full state put in the queue need not be the cheapest one.
- **A heuristic that sees collisions.** It is tempting to add a tool change to $h$ when the last tool "will collide later". A collision depends on the bends made before, so such a guess can be too high, and with no reopening at line L3 the plan can then cost too much.
- **Rounding at line L6.** In the example, the lip of the last wall touches the boundary of the GOOSENECK punch region at $(4, 5)$. A floating point test with a tolerance can call this a collision, and then the search reports that no plan exists.

## Implementations

## History

A* comes from Hart, Nilsson and Raphael (1968). For bend sequences, de Vin and others (1994) and Shpitalni and Saddan (1994) stated the choice of bend order and tools as a search over partial sequences, with collision tests from the geometry. Radin, Shpitalni and Hartman (1997) gave a two-stage method. Gupta, Bourne, Kim and Krishnan (1998) built a planner for a robotic press brake, in which a central operation planner runs A* over partial bend sequences and calls planners for tools, grasps and robot motion for costs and feasibility. They chose estimates that can be too high, on purpose, for speed, and reported near optimal plans. The consistent heuristic on this page is weaker but makes the search exact.

## References
