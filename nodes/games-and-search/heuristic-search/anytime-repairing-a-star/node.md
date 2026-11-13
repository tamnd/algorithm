---
tag: PYDPRD
kind: algorithm
slug: anytime-repairing-a-star
name: Anytime repairing A*
aliases:
- ARA*
area: games-and-search/heuristic-search
level: advanced
summary: Runs weighted A* with a falling weight and reuses each search in the next one. After each search it reports a path with a proved bound on its cost, and the last path is optimal.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of states reachable from the start, m: the number of actions among them, k: the number of weights in the schedule}
  time: {worst: O(k m log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2003
  people: [Maxim Likhachev, Geoff Gordon, Sebastian Thrun]
  note: ARA* was presented at NIPS 2003 for path planning of robots with a time limit.
prereqs: [weighted-a-star, consistent-heuristic]
see_also: [a-star-search, greedy-best-first-search, d-star-lite, lifelong-planning-a-star, beam-stack-search, open-list]
sources:
  - paper: Maxim Likhachev, Geoff Gordon and Sebastian Thrun, ARA*, Anytime A* with provable bounds on sub-optimality, Advances in Neural Information Processing Systems 16 (NIPS 2003)
    locator: pp. 767 to 774 (the procedures ImprovePath and Main, the INCONS list, the bound min(eps, g(goal) / min over OPEN and INCONS of g + h), and the theorems that each state is expanded at most once per search and that the bound holds)
  - paper: doi:10.1016/0004-3702(70)90007-X
    title: Ira Pohl, Heuristic search viewed as path finding in a graph, Artificial Intelligence 1(3-4) (1970)
    locator: pp. 193 to 204 (the weighted evaluation function on which ARA* is built)
---

Anytime repairing A* (ARA*) finds a path quickly and then improves it while time allows. It runs [weighted A*](/weighted-a-star/) with a large weight $\varepsilon$, reports the path, lowers $\varepsilon$, and searches again. The new search does not start from scratch: it keeps the values $g$ of the old one and reexamines only the states whose $g$ became lower after they were expanded, which it keeps in a list INCONS. With a [consistent heuristic](/consistent-heuristic/), each search expands each state at most once, and each reported path comes with a bound $\varepsilon'$ such that its cost is at most $\varepsilon' C^*$. The bound is often far below the weight. When the weight reaches 1, the path is optimal. Likhachev, Gordon and Thrun introduced it in 2003.

## In plain words

A robot must move now, but it can think while it moves. First it plans fast and roughly, by trusting its guess of the distance to the goal a lot. That gives a path, and a promise: the path is at most, say, three times as long as the best one. Then it trusts the guess a little less and plans again.

The second plan does not start over. Most of the first plan is still right, so the robot only fixes the places where it now knows a shorter way. Each plan is at least as good as the one before, and the promise gets tighter. If time runs out, the robot uses the last plan. If time does not run out, the last plan is the best one.

## The problem

The input is a [state-space search](/state-space-search/) problem with one goal state: a start $s_0$, a goal $s_g$, a function SUCCESSORS that gives the finite list of pairs $(n', c)$ of a next state and the positive cost of the action to it, a consistent heuristic $h$ with $h(s_g) = 0$, and a schedule of weights $\varepsilon_1 > \varepsilon_2 > \cdots > \varepsilon_k = 1$. The output is a sequence of paths from $s_0$ to $s_g$, each with a bound $\varepsilon' \ge 1$ such that its cost is at most $\varepsilon' C^*$, or *failure* when no path exists. The user can stop the search after any path.

## The algorithm

```pseudo id=main
ARA-STAR(s0, sg, SUCCESSORS, h, ε1 > ε2 > … > εk = 1)
L1  g[s0] ← 0, g[sg] ← ∞, parent[s0] ← nil, ε ← ε1
L2  OPEN ← { s0 }, CLOSED ← ∅, INCONS ← ∅
L3  IMPROVE-PATH()
L4  if g[sg] = ∞ then return failure
L5  ε′ ← BOUND(), publish PATH(parent, sg) with the bound ε′
L6  while ε′ > 1 do
L7      ε ← the next weight of the schedule
L8      move the states of INCONS into OPEN
L9      recompute the keys of OPEN, CLOSED ← ∅
L10     IMPROVE-PATH()
L11     ε′ ← BOUND(), publish PATH(parent, sg) with the bound ε′

IMPROVE-PATH()
L12 while fvalue(sg) > the least fvalue in OPEN do
L13     s ← the state of OPEN with least fvalue; remove it, add it to CLOSED
L14     for each (s′, c) in SUCCESSORS(s) do
L15         if s′ has no g or g[s] + c < g[s′] then
L16             g[s′] ← g[s] + c, parent[s′] ← s
L17             if s′ ∉ CLOSED then put s′ in OPEN with key fvalue(s′)
L18             else add s′ to INCONS
```

Here fvalue$(s) = g[s] + \varepsilon\,h(s)$ with the current weight, and
$$\mathrm{BOUND}() = \min\Bigl(\varepsilon,\ \frac{g[s_g]}{\min_{s \in \mathrm{OPEN} \cup \mathrm{INCONS}} \bigl(g[s] + h(s)\bigr)}\Bigr).$$
The denominator is a lower bound on $C^*$, so the ratio is a bound on the quality of the current path that does not depend on the weight. It is at least 1, because the goal never leaves OPEN once it has a finite $g$. The implementation takes the larger of this value and 1 as a guard, and breaks ties in fvalue toward larger $g$.

Three details make this ARA* and not a plain sequence of weighted A* runs. Inside one call of IMPROVE-PATH, a state in CLOSED is never put back in OPEN: line L18 sets it aside in INCONS. Between calls, line L9 clears CLOSED, so a state can be expanded again in the next call, but only if it is in OPEN, that is, only if its $g$ dropped. And the stop test of line L12 is not "the goal is removed" but "the goal has the least key", which saves the expansions of states with keys equal to that of the goal.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the goal G, and $h$ the Manhattan distance to G, with the values 6, 4, 4, 2, 2, 6, 7, 0 on S, A, B, C, D, E, F, G. It is consistent, and $C^* = 7$. The schedule is $3, 2, 3/2, 1$.

With $\varepsilon = 3$, the call expands S (key 18), then A (key 14), then D (key 11). D gives G the value $g = 8$ and the key 8, which is the least key in OPEN, so the call stops. OPEN holds B, C, F and G with $g + h$ = 7, 8, 8, 8, so BOUND $= \min(3, 8/7) = 8/7$. The first path S-A-D-G costs 8, and the search already knows that it is within $8/7$ of the optimum.

With $\varepsilon = 2$ and then $3/2$, the keys of B, C, F, G become 11, 10, 15, 8 and then 9, 9, 23/2, 8. G still has the least key, so both calls expand nothing and report the same path and bound. With $\varepsilon = 1$ the keys are 7, 8, 8, 8. The call expands B, which lowers $g$ of C from 6 to 5, and then C, which lowers $g$ of G to 7. Now G has the least key 7, and BOUND $= 7/7 = 1$.

| weight | expansions | cost | bound $\varepsilon'$ |
| --- | --- | --- | --- |
| 3 | 3 (S, A, D) | 8 | 8/7 |
| 2 | 0 | 8 | 8/7 |
| 3/2 | 0 | 8 | 8/7 |
| 1 | 2 (B, C) | 7 | 1 |

ARA* made 5 expansions in all, the same as one A* search. Four separate weighted A* runs would make 3, 3, 3 and 5.

**A larger grid.** The script draws grids from `random.Random(4)` with the generator of the tests: a 40 by 40 grid, each cell a wall with probability 0.3, and a cost from 1 to 5 to enter each free cell, chosen uniformly. It keeps the first grid where $(39, 39)$ can be reached from $(0, 0)$. That grid has 1,100 free cells, and Dijkstra's algorithm gives $C^* = 218$. The heuristic is the Manhattan distance, which is consistent because each step costs at least 1. The schedule is $5, 3, 2, 3/2, 5/4, 1$.

| weight | bound $\varepsilon'$ | cost | expansions of ARA* | weighted A* from scratch: expansions, cost |
| --- | --- | --- | --- | --- |
| 5 | 244/85 ≈ 2.87 | 244 | 152 | 152, 244 |
| 3 | 13/5 = 2.6 | 221 | 178 | 282, 223 |
| 2 | 109/76 ≈ 1.43 | 218 | 815 | 839, 218 |
| 3/2 | 109/99 ≈ 1.10 | 218 | 259 | 1,004, 218 |
| 5/4 | 109/104 ≈ 1.05 | 218 | 26 | 1,030, 218 |
| 1 | 1 | 218 | 10 | 1,040, 218 |

The path was optimal after the third call, but the bound needed three more calls to prove it. ARA* made 1,440 expansions over the six calls, against 4,347 for six runs from scratch. Over 130 smaller grids from `random.Random(17)` with the same schedule, ARA* made 2,473 expansions in all, against 9,207 from scratch. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for a consistent $h$ with $h(s_g) = 0$ and positive costs:

- **One expansion per call.** Each call of IMPROVE-PATH expands each state at most once, so each call ends.
- **The weight bound.** In a call with weight $\varepsilon$, each expanded state $s$ has $g[s] \le \varepsilon\,g^*(s)$, and at the end of the call $g[s_g] \le \varepsilon\,C^*$. The proof extends the argument for weighted A* without reopening to states that are kept from earlier calls.
- **The reported bound.** At the end of a call, the least $g + h$ over OPEN and INCONS is at most $C^*$. So $g[s_g] \le \varepsilon' C^*$, and the path of parent pointers costs at most $g[s_g]$.
- **Monotone values and optimality.** $g[s_g]$ never goes up, so the published values do not increase. The last call has $\varepsilon = 1$ or stops early with $\varepsilon' = 1$, and its path is optimal.
- **Failure.** The first call leaves $g[s_g] = \infty$ only when the goal cannot be reached.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS and $h$ counted as $O(1)$, $n$ the number of states reachable from $s_0$, $m$ the number of actions among them and $k$ the number of weights.

**One call.** Each state is expanded at most once, so lines L14 to L18 run at most $m$ times and the heap gets at most $m + n$ entries. With a [binary heap](/binary-heap/) and lazy deletion, a call takes $O(m \log n)$ time. Line L9 rebuilds the heap in $O(n)$.

**All calls.** The worst case is $O(k\,m \log n)$, the same as $k$ runs of weighted A* from scratch. The gain is in the typical case: a later call expands only the states whose $g$ dropped and the states that their changes reach, as the two tables show. There is no theorem that bounds this gain.

**Space.** The tables $g$ and parent, OPEN, CLOSED and INCONS take $O(n + m)$ words with lazy deletion. ARA* keeps all of them between calls, so its memory is that of one A* search.

## Properties

- **Anytime.** It can be stopped after any call, and it has a valid path with a proved bound from the end of the first call on.
- **Bounded suboptimal at each step**, with the bound $\varepsilon' \le \varepsilon$, and optimal at the end.
- **Monotone.** The published values $g[s_g]$ never increase, and each published path costs at most its value.
- **Needs a consistent heuristic** for the bound without reopening inside a call.
- **Not in place.** It stores all generated states, like A*.
- **Deterministic**, with the tie rule of the code.

## Variants and improvements

- **Weights chosen at run time.** The schedule need not be fixed in advance. A program can lower $\varepsilon$ by a larger step when a call was cheap, or set the next weight just below the last bound $\varepsilon'$, since a weight above $\varepsilon'$ cannot itself lower the bound. Such a call can still lower it through the ratio of $g[s_g]$ to the least $g + h$ over OPEN and INCONS: with the edges s→x 30, x→t 6 and s→t 45 and $h$ = 36, 6, 0, the call with weight $5/2$ reports $\varepsilon' = 5/4$, and the next one with weight 2 expands x and proves $\varepsilon' = 1$.
- **Anytime weighted A*.** Hansen and Zhou (2007) keep the weight fixed, go on with the same search after the first path, and prune states whose $g + h$ is not below the cost of the best path. It also ends with an optimal path.
- **Anytime dynamic A*.** Likhachev and others combined ARA* with [D* Lite](/d-star-lite/), so that the search also repairs itself when action costs change, as for a robot that sees new obstacles.
- **[Beam-stack search](/beam-stack-search/).** Another anytime method that ends with an optimal path, with memory bounded by a beam width instead of the size of the graph.

## When to use it

Use ARA* when you have a time limit that you do not know in advance, a consistent heuristic, and enough memory for an A* search: path planning for a robot or a game character that must act soon is the typical case. If the time limit is known and short, weighted A* with one good weight is simpler. If memory is the limit, ARA* does not help, since it keeps everything that A* keeps.

## Pitfalls

- **Taking the weight as the bound.** The bound $\varepsilon'$ is often much lower than $\varepsilon$, as in the example, where it is $8/7$ at $\varepsilon = 3$. Publish $\varepsilon'$, not $\varepsilon$.
- **Putting a closed state back in OPEN within a call.** It makes the search correct but slower, and it breaks the claim of one expansion per call. Use INCONS, line L18.
- **Forgetting INCONS between calls.** If line L8 is dropped, the next call does not see the states whose $g$ dropped, and its bound can be false.
- **Not recomputing the keys.** The keys of OPEN depend on $\varepsilon$, so line L9 must rebuild the heap after each change of weight.
- **An inconsistent heuristic.** Then the bound of a call can fail without reopening. Use a consistent $h$ or reopen within the call, as weighted A* does.
- **Several goals.** The pseudocode has one goal state. For a goal test, add a virtual goal with an action of cost 0 from each goal state.

## Implementations

## History

Likhachev, Gordon and Thrun presented ARA* at NIPS 2003, with experiments on robot arm planning and outdoor path planning under time limits. The paper gave the INCONS list, the proof that each search expands each state at most once with a consistent heuristic, and the bound that uses the least $g + h$ over OPEN and INCONS. It built on weighted A* (Pohl 1970) and on earlier anytime searches that ran weighted A* many times from scratch. Anytime weighted A* by Hansen and Zhou (2007) and the anytime form of D* Lite by Likhachev and others followed the same goal of good paths soon and better paths later.

## References
