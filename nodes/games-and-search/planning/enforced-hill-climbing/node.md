---
tag: K6E90E
kind: algorithm
slug: enforced-hill-climbing
name: Enforced hill climbing
aliases:
- EHC
area: games-and-search/planning
level: advanced
summary: Greedy local search that breaks heuristic plateaus with breadth-first search.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of reachable states, b: the largest number of successors of a state, k: the heuristic value of the initial state, e: the time of one heuristic evaluation}
  time: {worst: O(k n b e)}
  space: {extra: O(n)}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 2000
  people: [Joerg Hoffmann]
  note: Hoffmann introduced enforced hill climbing in 2000 as the search of the FF planner, and Hoffmann and Nebel described it with its completeness result in 2001.
prereqs: [hill-climbing, breadth-first-search, heuristic-function]
see_also: [fast-forward-planner, relaxed-plan-heuristic, hill-climbing, random-restart-hill-climbing, greedy-best-first-search, local-optimum, hsp-planner, sussman-anomaly]
sources:
  - paper: doi:10.1613/jair.855
    title: "Joerg Hoffmann and Bernhard Nebel, The FF planning system: fast plan generation through heuristic search, Journal of Artificial Intelligence Research 14 (2001)"
    locator: pp. 253 to 302; Section 5.1 and Figure 3 (the algorithm), Section 5.2 with Definition 7, Proposition 4 and Theorem 3 (dead ends and completeness), Section 6.1.2 (helpful actions inside the search), Section 8.1.1 (depth of the breadth-first searches in Logistics)
  - paper: "Joerg Hoffmann, A heuristic for domain independent planning and its use in an enforced hill-climbing algorithm, Proceedings of the 12th International Symposium on Methodologies for Intelligent Systems (ISMIS 2000), Springer"
    locator: pp. 216 to 227 (the first description of enforced hill climbing)
  - paper: doi:10.1613/jair.1747
    title: "Joerg Hoffmann, Where ignoring delete lists works: local search topology in planning benchmarks, Journal of Artificial Intelligence Research 24 (2005)"
    locator: pp. 685 to 758 (local minima, benches and the exit distance under the optimal relaxed plan heuristic; general locator)
---

Enforced hill climbing (EHC) is a local search for a goal state in a state space with a heuristic $h$. Like [hill climbing](/hill-climbing/), it moves from the current state to a state with a smaller value and never goes back. Unlike hill climbing, it does not look only at the neighbors. From the current state $s$ it runs a [breadth-first search](/breadth-first-search/) until it finds the nearest state that is a goal or has $h$ strictly below $h(s)$, and it moves there along the path that the search found. So a plateau or a small [local minimum](/local-optimum/) costs one wider search, not a restart. Hoffmann (2000) made it the search of the [Fast-Forward planner](/fast-forward-planner/), where it runs on the [relaxed plan heuristic](/relaxed-plan-heuristic/). It always returns a valid plan, it is complete on tasks with no dead ends, and it can fail on other solvable tasks, so FF falls back to a complete search.

## In plain words

Always try to get closer to the goal, by the measure of a guide that estimates the distance. If one step can make the guide's number smaller, take that step. If no single step helps, look two steps ahead, then three, in all directions, until you find some state with a smaller number. Walk there and start again.

You never walk back, so a bad choice can trap you: you can walk into a corner from which the goal cannot be reached. Then the method gives up. In practice it either finds a plan fast or fails fast, and the planner then tries a slower method that cannot get trapped.

## The problem

The input is a finite state space with an initial state $I$, a successor function that gives the pairs (action, next state) of each state, a test for goal states, and a heuristic $h$ with values in the natural numbers or $\infty$. The value $\infty$ must mean that the state is a dead end, a state from which no goal state is reachable, and every successor of such a state must also have the value $\infty$. The FF heuristic has both properties. The output is a sequence of actions from $I$ to a goal state, or failure. Failure does not prove that no plan exists.

## The algorithm

```pseudo id=main
ENFORCED-HILL-CLIMBING(I, h)
L1  s ← I ; π ← the empty plan
L2  if h(s) = ∞ then return failure
L3  while s is not a goal state do
L4      s' ← BETTER(s)
L5      if s' = failure then return failure
L6      append the actions on the path from s to s' to π ; s ← s'
L7  return π

BETTER(s)
L8  seen ← {s} ; queue ← [s]
L9  while queue is not empty do
L10     u ← remove the first state of queue
L11     for each successor t of u by an action a, with t ∉ seen, do
L12         add t to seen with the parent (u, a)
L13         if t is a goal state or h(t) < h(s) then return t
L14         if h(t) < ∞ then append t to queue
L15 return failure
```

Lines L1 to L7 are the outer loop of Figure 3 of Hoffmann and Nebel (2001). Each iteration replaces the current state by a strictly better one, and appends the path to the plan. No state is ever left again in favor of an earlier one, so the plan only grows.

BETTER is a plain breadth-first search from $s$. It tests each state when it is generated (line L13), so it returns the nearest better state in the order of generation, and the parents give the path to it. A state with $h = \infty$ is not expanded (line L14). This is safe: all states reachable from it have the value $\infty$ too, so none of them is better than $s$. Each call of BETTER uses a new seen set, so a state visited in an earlier iteration can be visited again.

Hoffmann and Nebel stop the loop when $h(s) = 0$. For the FF heuristic, $h(s) = 0$ exactly at goal states, and then the two tests are the same. The explicit goal test of lines L3 and L13 keeps the algorithm correct for any heuristic with the two properties above.

## Example

**A plateau that hill climbing cannot leave.** Hoffmann and Nebel (2001, Section 6.1.1) use six actions on the facts $A$, $B$, $P_A$ and $P_B$:

| action | pre | add | del |
|---|---|---|---|
| $op_{A1}$ | | $A$ | $B$ |
| $op_{A2}$ | $P_A$ | $A$ | |
| $op_{PA}$ | | $P_A$ | |
| $op_{B1}$ | | $B$ | $A$ |
| $op_{B2}$ | $P_B$ | $B$ | |
| $op_{PB}$ | | $P_B$ | |

The initial state is $\{B\}$ and the goal is $\{A, B\}$. The FF heuristic is 1 in $\{B\}$, and every successor that is not a goal also has the value 1. Steepest-ascent hill climbing stops at once. EHC runs a breadth-first search: at depth 1 it meets $\{A\}$, $\{B, P_A\}$ and $\{B, P_B\}$, all with the value 1, and at depth 2 it meets the goal state $\{A, B, P_A\}$ through $op_{PA}, op_{A2}$. That is the plan.

**A dead end.** A route of five actions leads from $r_0$ through $r_1, \ldots, r_4$ to the goal $g$, and each action deletes the fact it needs. A second action $\mathit{trap}$ goes from $r_0$ to $u$. From $u$, the action $a_p$ gives $p$ and $a_q$ gives $q$, and each deletes $u$, while $\mathit{finish}$ needs $p$ and $q$ and adds $g$. The relaxed plan from $\{r_0\}$ uses the trap and both of $a_p$ and $a_q$, so $h(\{r_0\}) = 4$, and $h(\{u\}) = 3$. EHC moves to $\{u\}$ at depth 1. Its two successors $\{p\}$ and $\{q\}$ have the value $\infty$, because neither $u$ nor the other fact can come back. BETTER fails, and so does EHC. [Greedy best-first search](/greedy-best-first-search/) on the same heuristic expands $\{u\}$, drops its two children, and goes on along the route to the 5-action plan. This is the fallback of FF.

**Goal ordering in the blocks world.** In the [blocks world](/blocks-world/) with $A$, $B$, $C$ on the table and the goal $\mathit{on}(A, B)$, $\mathit{on}(B, C)$, the implementation of this page returns 8 actions, and the shortest plan has 4. The values along the way are $4, 3, 2, 1, 0$, and the four breadth-first searches go to the depths 2, 4, 1 and 1. The first search stacks $A$ on $B$. The second must undo it: it unstacks $A$, puts it down, and stacks $B$ on $C$. This is the goal order trap of the [Sussman anomaly](/sussman-anomaly/), and FF has extra rules for it, added goal deletion and the goal agenda. The trace depends on the tie-breaking of the heuristic.

**Measured on small tasks.** These counts come from the implementation of this page and the FF heuristic.

| task set | runs | EHC finds a plan | plain hill climbing finds a plan |
|---|---|---|---|
| random STRIPS tasks with 4 to 8 facts, 600 seeds | 600 | 334, all the solvable tasks | 304 |
| blocks world, 3 blocks, every reachable state as start | 22 | 22, 12 of them longer than optimal | 4 |
| blocks world, 4 blocks, every reachable state as start | 125 | 125, 107 of them longer than optimal | 4 |

On the random tasks, 366 of the 400 searches stopped at depth 1, 33 at depth 2 and 1 at depth 4. Hoffmann and Nebel (2001, Section 8.1.1) report the same picture in Logistics: the better state is almost always at depth 1 or 2.

## Correctness

The proofs are in [the correctness proof](proofs/correctness/). The results are these.

1. **Soundness.** A returned plan leads from $I$ to a goal state, since each iteration appends a real path from the current state to the next one.
2. **Nearest better state.** BETTER returns a state that is a goal or better than $s$ whenever one is reachable from $s$, and the path to it is a shortest one. The proof uses the property that $\infty$ is passed on to successors, so no pruned state leads to a better one.
3. **Termination.** Each iteration lowers $h$ by at least 1, or reaches a goal, so there are at most $h(I) + 1$ iterations, and at most $h(I)$ when $h$ is positive on all non-goal states.
4. **Completeness on dead-end free tasks.** If no reachable state is a dead end, then a goal is reachable from every current state, so BETTER never fails (Hoffmann and Nebel 2001, Proposition 4).

The converse fails: tasks with dead ends can still be solved, and often are. But deciding whether a task is dead-end free is PSPACE-complete (Hoffmann and Nebel 2001, Theorem 3), so a planner cannot test it first in general.

## Complexity

One call of BETTER generates at most $n b$ states, and it evaluates $h$ once for each, so it costs $O(n b e)$ time. There are at most $k + 1$ calls, where $k = h(I)$. So the time is $O(k n b e)$ in the worst case, and the space is $O(n)$ for the seen set and the queue, plus the plan. These are proved upper bounds. The worst case is not a reason to use EHC: a plain breadth-first search from $I$ costs $O(n b)$.

The point is the typical case. When the nearest better state is at a small depth $d$, one call costs about $b^d$ evaluations, and the whole run costs about $k b^d$. Hoffmann and Nebel (2001, Section 8.1.1) state that in Logistics, with the optimal relaxed plan length as the heuristic, the better state is never more than $d + 1$ steps away, where $d$ is the largest distance between two locations. Hoffmann (2005) proves bounds of this kind for many benchmark domains.

## Properties

- **Not complete.** It can fail on a solvable task with dead ends.
- **Not optimal.** The plan can be much longer than a shortest plan, as in the blocks world example.
- **No backtracking.** A step once taken is never undone, so the memory is that of one breadth-first search.
- **Deterministic.** The order of successors and the heuristic fix the run. Randomized restarts did not help in the tests of Hoffmann and Nebel (2001, Section 5.2), because the failing tasks were full of dead ends.
- **Fails fast.** When it fails, it usually fails early, which makes a complete fallback cheap to add.

## Variants and improvements

- **Helpful actions.** FF expands, inside BETTER, only the successors by helpful actions (Hoffmann and Nebel 2001, Section 6.1.2). The search is much smaller, and the result is incomplete even on dead-end free tasks. In the plateau example above, the helpful actions only swap $A$ and $B$, and they cut out every plan. See the [Fast-Forward planner](/fast-forward-planner/).
- **Fallback to complete search.** If EHC fails, start a complete search such as [greedy best-first search](/greedy-best-first-search/) from scratch. FF does this, and so does every planner that uses EHC as a first try.
- **Goal agenda.** Split the goals into an ordered series of subsets, and run EHC on growing goal sets, each time from the state where the previous run ended. FF uses a simplified version of the agenda of Koehler (1998).
- **Other heuristics.** The algorithm needs only the two properties of $h$. It works with any heuristic, for example the additive heuristic of [HSP](/hsp-planner/), but its success depends on small plateaus, which the relaxed plan heuristic tends to give on benchmark domains.
- **Restarts.** [Random-restart hill climbing](/random-restart-hill-climbing/) attacks the same weakness of hill climbing from the other side: it starts again from new points instead of searching wider from the stuck one.

## When to use it

Use EHC as a first, fast attempt in satisficing planning, when the heuristic is well informed, when the tasks rarely have dead ends, and when plan length is a secondary concern. Always add a complete fallback. Do not use it when the plan must be optimal or when the task is full of dead ends, such as tasks with resources that run out. There, a best-first search such as [greedy best-first search](/greedy-best-first-search/) or [weighted A*](/weighted-a-star/) is the safer choice.

## Pitfalls

- **Treating failure as proof.** Failure means only that the search walked into a region with no better state. Report "no plan" only after a complete search.
- **Stopping at $h = 0$ with a heuristic that can be 0 elsewhere.** Then EHC can stop at a state that is not a goal. Test for the goal, as lines L3 and L13 do.
- **Expanding states with $h = \infty$.** It does no harm to correctness, but on tasks with many dead ends the breadth-first search then explores large dead regions.
- **Keeping one seen set across iterations.** The current state changes, and a state visited in an earlier search can be on the only path to a better state now. Use a new seen set in each call.
- **Comparing with plain hill climbing on the wrong measure.** EHC evaluates many more states per step. It wins because it does not get stuck, not because each step is cheaper.

## Implementations

## History

Hoffmann (2000) presented the FF heuristic and enforced hill climbing at ISMIS 2000. FF, with this search, took part in the planning competition at AIPS 2000 and was named a Group A distinguished performance planning system. Hoffmann and Nebel (2001) gave the full description, with the dead-end analysis, the completeness result for dead-end free tasks, and the PSPACE-completeness of deciding dead-end freeness. Hoffmann (2005) then explained why EHC works so well on the benchmarks: under the optimal relaxed plan heuristic, many benchmark domains have no local minima and only short plateaus. Later planners kept the idea of a fast incomplete search with a complete fallback, though most moved to best-first search with preferred operators.

## References
