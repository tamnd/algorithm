---
tag: YG7MJ1
kind: algorithm
slug: fringe-search
name: Fringe search
area: games-and-search/heuristic-search
level: advanced
summary: IDA* without the restarts. It keeps the frontier in a linked list and the g of each seen state in a table, and each pass with a higher threshold goes on from the frontier of the last one.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of states that the search sees, b: the largest number of successors of a state, t: the number of passes}
  time: {consistent: O(t n + n b)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2005
  people: [Yngvi Björnsson, Markus Enzenberger, Robert C. Holte, Jonathan Schaeffer]
  note: The four authors presented fringe search at the 2005 IEEE Symposium on Computational Intelligence and Games, as a replacement for A* in path finding on game maps.
prereqs: [iterative-deepening-a-star, a-star-search]
see_also: [memory-bounded-heuristic-search, recursive-best-first-search, doubly-linked-list, hash-table, open-list, consistent-heuristic, jump-point-search, partial-expansion-a-star]
sources:
  - paper: Yngvi Björnsson, Markus Enzenberger, Robert C. Holte and Jonathan Schaeffer, Fringe search, beating A* at pathfinding on game maps, Proceedings of the 2005 IEEE Symposium on Computational Intelligence and Games (CIG-05)
    locator: pp. 125 to 132 (the now and later lists, the cache of g values, the comparison with IDA* and A*, and the experiments on game maps)
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (IDA*, the method whose restarts fringe search removes)
---

Fringe search is [IDA*](/iterative-deepening-a-star/) that keeps its frontier. Like IDA*, it works in passes with a threshold on $f = g + h$: a pass expands the states with $f$ at most the threshold, and the next pass uses the least $f$ above it. IDA* starts each iteration again from the root and forgets every state it saw. Fringe search keeps the states at the edge of the last pass, the *fringe*, in a [doubly linked list](/doubly-linked-list/), and the cost $g$ and parent of each state it has seen in a [hash table](/hash-table/). So the next pass goes on from the fringe and does not expand the inner states again, and the table detects duplicates as in [A*](/a-star-search/). It uses no priority queue. The order of expansion is the order of IDA*, depth first within a threshold, not the order of A*. With an [admissible heuristic](/admissible-heuristic/), it returns a cheapest path. Björnsson, Enzenberger, Holte and Schaeffer gave it in 2005 for path finding in games.

## In plain words

Think of a search that goes out in rings, with a limit on how far it may look. In each round, it goes over a list of places at the edge of what it knows. A place that is within the limit is opened: its neighbors go into the list right after it, and it leaves the list. A place that is too far stays in the list for the next round.

When the round ends, the limit goes up to the closest place that was too far, and a new round goes over the same list again.

A notebook keeps the best known way to each place. If a place is reached by a longer way than before, it is ignored. So the search never starts again from the beginning, and it never needs to keep the list sorted.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(m, c)$ of a next state and the positive cost of the action to it, a goal test IS-GOAL, and an admissible heuristic $h$. The output is a cheapest path from $s_0$ to a goal state, or *failure* when no goal can be reached. The proof of failure needs a finite graph.

## The algorithm

```pseudo id=main
FRINGE-SEARCH(s0, SUCCESSORS, IS-GOAL, h)
L1  FRINGE ← the list (s0)
L2  CACHE[s0] ← (g = 0, parent = none); flim ← h(s0)
L3  while FRINGE is not empty do
L4      fmin ← ∞
L5      for each state n of FRINGE, from left to right, with the states put in during the pass do
L6          if f(n) = g(n) + h(n) > flim then fmin ← min(fmin, f(n)) and go on to the next state
L7          if IS-GOAL(n) then return the path to n by the parents in CACHE
L8          for each pair (m, c) of SUCCESSORS(n), from the last to the first do
L9              if m is in CACHE and g(n) + c ≥ g(m) then skip m
L10             if m is in FRINGE then take m out of FRINGE
L11             put m into FRINGE just after n
L12             CACHE[m] ← (g = g(n) + c, parent = n)
L13         take n out of FRINGE
L14     flim ← fmin
L15 return failure
```

The paper describes two lists, *now* and *later*. The states before the current position of the pass form the later list: they are above the threshold and wait for the next pass. The states after it form the now list. One linked list with a moving position holds both. Line L11 puts the children of $n$ just after it, so the pass visits them next, as a depth-first search would. Line L8 takes the successors from the last to the first so that they end up in their own order.

Line L9 is the duplicate test of A*. A state is put in the list again only when the search finds a cheaper path to it. Expanded states stay in CACHE, so CACHE also plays the part of the closed list.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the goal G, and $h$ the Manhattan distance to G, with the values 6, 4, 4, 2, 2, 6, 7, 0 on S, A, B, C, D, E, F, G. The neighbors are taken in alphabetical order. $C^* = 7$.

| pass, flim | visit | $g$, $f$ | action | FRINGE after |
| --- | --- | --- | --- | --- |
| 1, 6 | S | 0, 6 | expand | A B F |
| | A | 2, 6 | expand; S is not cheaper | C D B F |
| | C | 6, 8 | keep, fmin 8 | C D B F |
| | D | 5, 7 | keep, fmin 7 | C D B F |
| | B | 3, 7 | keep | C D B F |
| | F | 1, 8 | keep | C D B F |
| 2, 7 | C | 6, 8 | keep | C D B F |
| | D | 5, 7 | expand; G gets $g = 8$ | C G B F |
| | G | 8, 8 | keep | C G B F |
| | B | 3, 7 | expand; C moves after B with $g = 5$, E gets $g = 5$ | G C E F |
| | C | 5, 7 | expand; G moves after C with $g = 7$ | G E F |
| | G | 7, 7 | goal | |

Fringe search returns S-B-C-G of cost 7 after 12 visits and 5 expansions, S, A, D, B, C, one each. The second pass did not expand S and A again, as IDA* does.

**Not the order of A\*.** On the small directed graph S→B 4, S→C 1, B→A 1, B→G 3 and C→A 1, with $h$ equal to 6, 0, 2, 0, 0 on S, A, B, C, G, the heuristic is admissible but not consistent, since $h(S) = 6 > 1 + h(C)$. The first pass has the threshold 6. It expands S, then B, which is first in the list, then its child A with $g = 5$, and only then C, which gives A the smaller $g = 2$, so A is expanded again. The second pass returns S-B-G of cost 7. Fringe search expands S, B, A, C, A, with one expansion of A again. A*, which takes the state of least $f$ each time, expands S, C, A, B and never expands A twice.

**The 8-puzzle.** The script draws 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$. The heuristic is the Manhattan distance, which is consistent. Over the 20 instances, fringe search made 4,946 expansions and 9,477 visits, A* made 3,411 expansions, and IDA* made 8,229. No state was expanded twice. Fringe search expands more states than A* here, because in the last pass it expands the states with $f = C^*$ in depth-first order until it meets a goal. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for positive costs and an admissible $h$:

- **Real paths.** The parents in CACHE lead from each seen state back to $s_0$ along a path of cost at most its $g$.
- **A good state in the list.** Until a goal is returned, the list holds a state on a cheapest path to a goal with its least $g$, so its $f$ is at most $C^*$.
- **Thresholds.** Each pass that does not return raises the threshold, and the new threshold is at most $C^*$. So the goal that line L7 returns has $g \le C^*$, and the path costs $C^*$.
- **Termination.** On a finite graph, the search ends, and it returns failure only when no goal can be reached.
- **Consistent heuristics.** With a [consistent heuristic](/consistent-heuristic/), all states expanded in one pass have $f$ equal to its threshold, and no state is expanded twice.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ and each operation of the hash table counted as $O(1)$.

**Space.** The list and CACHE hold at most the $n$ states seen, so the space is $O(n)$, the same order as A*. Fringe search is memory bounded only in the sense that it uses no priority queue and no copies of states per path. Its saving over IDA* is time, not space.

**Time.** Each list operation is $O(1)$, so an expansion costs $O(b)$, with no $\log$ factor for a heap. Each pass visits each state in the list once. With a consistent heuristic, each state is expanded at most once, so with $t$ passes the time is $O(t\,n + n\,b)$. When $f$ takes few distinct values, as on grids with unit costs, $t$ is small and the passes cost about as much as the expansions. With many distinct values, $t$ can be close to $n$, and the visits of the states that wait in the list dominate, as the many iterations do for IDA*. With an inconsistent heuristic, a state can be expanded once per cheaper path to it, as in A* with reopening.

## Properties

- **Optimal** with an admissible heuristic, and **complete** on finite graphs.
- **Duplicate detection** by the table of $g$ values, unlike IDA*.
- **No priority queue**: the list is not sorted, and each operation on it is $O(1)$.
- **Order of IDA***: depth first within a threshold, so with an inconsistent heuristic it can expand a state again where A* would not.
- **Space $O(n)$**, like A*.
- **Deterministic and not recursive.**

## Variants and improvements

- **Buckets.** A [bucket queue](/bucket-queue/) keyed by $f$ also avoids a heap when $f$ takes few values. Fringe search goes further and keeps no order in a pass at all.
- **[IDA*](/iterative-deepening-a-star/).** Drop the list and the table, and the method is IDA*: linear space, but each iteration starts again from the root.

## When to use it

Use fringe search where you would use A* with a consistent heuristic and $f$ takes few distinct values, as on grid maps with small integer costs. There it avoids the cost of a heap and of keeping the open list sorted. The authors found it faster than an optimized A* on game maps. When memory is the limit, it does not help, since it stores every state it sees: use IDA* or [RBFS](/recursive-best-first-search/). When $f$ takes many distinct values, the passes become many and short, and A* with a heap is better.

## Pitfalls

- **Testing the goal when it is generated.** A goal can first be reached by a path that is not the cheapest, as G is with $g = 8$ in the example. Test it at line L7, when it is visited within the threshold.
- **Forgetting to take a state out of the list before putting it in again.** When a cheaper $g$ is found for a state that is still in the list, line L10 must move it, or it is visited twice with different values.
- **Storing $f$ in the list.** The $f$ of a state changes when its $g$ changes. Compute it from CACHE at each visit, as line L6 does.
- **A threshold that rises by less than one value.** Line L14 must use the least $f$ that was above the threshold, as IDA* does, or the pass expands nothing new.
- **Expecting the order of A\*.** With an inconsistent heuristic, fringe search can expand a state more than once, as in the example.

## Implementations

## History

Björnsson, Enzenberger, Holte and Schaeffer presented fringe search at the 2005 IEEE Symposium on Computational Intelligence and Games. They started from IDA*, noted that its iterations repeat the work of the earlier ones and that it does not detect duplicates, and kept the frontier and a table of seen states between iterations. The result lies between IDA* and A*, with the threshold order of the first and the memory of the second. On the grid maps of commercial games, it was faster than an optimized A* in their experiments.

## References
