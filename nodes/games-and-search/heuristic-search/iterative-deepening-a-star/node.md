---
tag: 1ND9FV
kind: algorithm
slug: iterative-deepening-a-star
name: Iterative-deepening A*
aliases:
- IDA*
area: games-and-search/heuristic-search
level: core
summary: Runs depth-first searches that cut off each path once f = g + h passes a threshold, and raises the threshold to the least cut-off f each time. It is optimal and needs memory linear in the depth.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of nodes of the search tree with f at most C*, b: the largest number of successors of a state, d: the largest number of actions on a path that the search follows}
  time: {worst: O(n^2), geometric: O(n)}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
history:
  year: 1985
  people: [Richard E. Korf]
  note: Korf introduced IDA* in 1985 and used it to find the first optimal solutions of random instances of the 15-puzzle.
prereqs: [iterative-deepening-search, a-star-search, admissible-heuristic]
see_also: [recursive-best-first-search, fringe-search, memory-bounded-heuristic-search, simplified-memory-bounded-a-star, depth-first-branch-and-bound, pattern-database, sliding-tile-puzzle, partial-expansion-a-star]
sources:
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (iterative deepening, IDA* with thresholds on f, its optimality with an admissible heuristic, and the 15-puzzle experiments)
  - paper: doi:10.1016/0004-3702(91)90100-X
    title: U. K. Sarkar, P. P. Chakrabarti, S. Ghose and S. C. De Sarkar, Reducing reexpansions in iterative-deepening search by controlling cutoff bounds, Artificial Intelligence 50(2) (1991)
    locator: pp. 207 to 221 (IDA*_CR, which raises the threshold by more than the least cut-off f)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition
    locator: Section 3.5.5 (iterative-deepening A* as a memory-bounded search)
---

Iterative-deepening A* (IDA*) finds a cheapest path with the memory of a [depth-first search](/depth-first-search/). It combines [iterative deepening](/iterative-deepening-search/) with the evaluation $f = g + h$ of [A*](/a-star-search/). Each iteration is a depth-first search that cuts off a path as soon as $f$ exceeds a threshold $T$. The first threshold is $h(s_0)$, and each new threshold is the least $f$ that the iteration before cut off. With an [admissible heuristic](/admissible-heuristic/), the threshold never passes the optimal cost $C^*$, so the first goal found costs $C^*$. IDA* stores only the current path, so its memory is linear in the depth, and it has no queue and no closed list. The price is that each iteration repeats the work of the ones before, and the search does not notice that two paths lead to the same state. Korf introduced it in 1985.

## In plain words

You look for the shortest way out of a maze, but you cannot write anything down. So you set yourself a budget: "I will only try routes whose length so far plus my guess of what is left is at most 6." You walk every such route, turning back each time the budget is used up. You note the smallest amount by which you went over.

If you did not get out, you raise the budget to exactly that amount and start again from the entrance. Your guess never says more than the real distance, so the first time you get out, there was no shorter way.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(m, c)$ of a next state and the cost of the action to it, with each cost at least some $\epsilon > 0$, a goal test IS-GOAL, and an admissible heuristic $h$. The output is a cheapest path from $s_0$ to a goal state, or *failure* when no goal can be reached on a finite graph.

## The algorithm

```pseudo id=main
IDA-STAR(s0, SUCCESSORS, IS-GOAL, h)
L1  T ← h(s0)
L2  loop
L3      PATH ← [ s0 ]
L4      r ← DFS(s0, 0, T); if r = FOUND then return PATH
L5      if r = ∞ then return failure
L6      T ← r

DFS(n, g, T)                                  ▷ returns FOUND or the least f above T that was cut off
L7  f ← g + h(n)
L8  if f > T then return f
L9  if IS-GOAL(n) then return FOUND
L10 next ← ∞
L11 for each (m, c) in SUCCESSORS(n) with m not on PATH do
L12     push m on PATH
L13     r ← DFS(m, g + c, T)
L14     if r = FOUND then return FOUND
L15     next ← min(next, r)
L16     pop m from PATH; when the loop ends, return next
```

Line L8 is the cut-off and line L15 collects the least $f$ that was cut off below $n$. Line L11 skips a successor that is already on the current path, which removes cycles at a cost of $O(1)$ per check with a hash set next to PATH. The goal test comes after the cut-off test, so a goal is accepted only when its $f = g$ is at most $T$.

The implementation does the same with an explicit stack of successor iterators, so deep paths do not hit the recursion limit of Python. It tests $f$ and the goal when it generates a successor, which is the same as doing it at the start of the call on that successor, and it tests the start for a goal once before the first iteration.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the goal G, and $h$ the Manhattan distance to G, with the values 6, 4, 4, 2, 2, 6, 7, 0 on S, A, B, C, D, E, F, G. The neighbors are tried in alphabetical order. $C^* = 7$.

**Iteration 1, $T = 6$.** S has $f = 6$. Its successors A ($f = 2 + 4 = 6$), B ($3 + 4 = 7$) and F ($1 + 7 = 8$) give one path within the threshold, to A. From A, C has $f = 6 + 2 = 8$ and D has $f = 5 + 2 = 7$, and S is on the path. Nothing else fits, so the iteration ends with the least cut-off value $\min(7, 8, 8, 7) = 7$. It expanded S and A.

**Iteration 2, $T = 7$.** From S, A ($f = 6$), then D below A ($f = 7$), whose successor G has $f = 8 + 0 = 8 > 7$ and is cut off. Back at S, B ($f = 7$), then C below B with $g = 5$ and $f = 7$, then G below C with $g = 7$ and $f = 7$: a goal within the threshold. IDA* returns S-B-C-G of cost 7.

| iteration | $T$ | expanded | least cut-off $f$ |
| --- | --- | --- | --- |
| 1 | 6 | S, A | 7 |
| 2 | 7 | S, A, D, B, C | (goal found) |

IDA* expanded 7 states and generated 17 successors in all. A* on the same graph expands S, A, D, B, C, the same 5 states as the last iteration, and keeps all of them in memory.

**A bad case.** On a chain $0 \to 1 \to \cdots \to N$ with unit costs and $h = 0$, each iteration raises $T$ by 1 and reaches one more state. The thresholds are $0, 1, \ldots, N$, and the total number of expansions is $N(N+1)/2 + N$, quadratic in the $N$ expansions of A*. This happens whenever each new threshold admits only a few new nodes, for example with many distinct real-valued costs.

**The 8-puzzle.** The script draws 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$, with $d$ from 14 to 24. The heuristic is the Manhattan distance, and the successors are tried in the order up, down, left, right of the blank.

| method | expansions, all 20 instances |
| --- | --- |
| A* | 3,411 |
| IDA*, all iterations (the start counted once per iteration) | 8,229 |
| IDA*, last iterations only | 3,452 |

IDA* ran 78 iterations in all. Since each move changes the Manhattan distance by exactly 1, $f$ changes by 0 or 2 along a path, so each threshold is 2 above the one before. The earlier iterations cost about 1.4 times the last ones here, which is the geometric growth that makes IDA* efficient. The last iterations alone cost about as much as A* here, but IDA* stores only one path at a time, and its cost per node is lower because it has no heap and no table of states. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for costs at least $\epsilon > 0$, finitely many successors per state, and an admissible $h$:

- **Each iteration ends.** A path with $f \le T$ has at most $T / \epsilon$ actions, so the depth-first search explores a finite tree.
- **The thresholds rise and stay at most $C^*$.** If $T < C^*$, the iteration finds no goal, and it cuts off some state of an optimal path with $f \le C^*$. So the next threshold is above $T$ and at most $C^*$.
- **Optimality.** The thresholds take finitely many values up to $C^*$, so some iteration finds a goal. The goal it finds has cost $g = f \le T \le C^*$.
- **Failure.** On a finite graph with no reachable goal, the number of simple paths is finite, the thresholds run out, and line L5 returns failure.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$. Let $n$ be the number of nodes of the search tree, the tree of simple paths from $s_0$, with $f \le C^*$.

**Time.** The last iteration expands at most the $n$ nodes with $f \le C^*$, and each earlier iteration at most as many. If each new threshold admits a fixed fraction more nodes, as in a tree where the number of nodes with $f \le T$ grows geometrically with $T$, the earlier iterations together cost a constant times the last one, and IDA* takes $O(n)$ expansions. Korf showed this for trees with a constant branching factor. In the worst case each iteration adds one node, as on the chain above, and IDA* takes $O(n^2)$ expansions. Each expansion costs $O(b)$.

**Compared with A*.** The tree of paths can be much larger than the graph of states, because IDA* does not detect duplicates other than on the current path. On a grid, the number of paths to a cell grows exponentially with the distance, while the number of cells grows only quadratically. IDA* is then far slower than A*. On a puzzle like the 15-puzzle, with few short cycles and a huge state space, the tree is not much larger than the graph and IDA* is the method of choice.

**Space.** PATH holds at most $d + 1$ states, and the recursion or the explicit stack holds $O(d)$ frames. With the successor lists in memory, that is $O(b\,d)$. IDA* needs no queue, no table of $g$ values and no closed list.

## Properties

- **Optimal** with an admissible heuristic and costs bounded away from 0.
- **Complete** on finite graphs, and on infinite graphs with a reachable goal.
- **Linear space** in the depth of the search.
- **No duplicate detection** beyond the current path, unless it is combined with a [transposition table](/transposition-table/).
- **Low overhead per node**: no heap and no hashing of the whole state set.
- **Deterministic and recursive.**

## Variants and improvements

- **Larger threshold steps.** IDA*_CR (Sarkar and others 1991) raises the threshold so that the next iteration is expected to admit a set number of new nodes, which avoids the quadratic case. Then the first goal found is no longer surely optimal, so the search goes on until it has seen all nodes with $f$ below the cost of the goal found, as in a [depth-first branch and bound](/depth-first-branch-and-bound/).
- **Better heuristics.** Most of the success of IDA* comes from strong heuristics such as [pattern databases](/pattern-database/), with which it found optimal solutions of the 15-puzzle and the [Rubik's cube](/rubiks-cube-problem/).
- **Memory for speed.** A transposition table caches states and their $g$, which cuts duplicates. [Fringe search](/fringe-search/) keeps the frontier of the last iteration so that the next one need not restart from $s_0$.
- **Best-first order in linear space.** [Recursive best-first search](/recursive-best-first-search/) expands nodes in best-first order even with a heuristic that is not consistent, with the same memory.
- **Fewer successors.** Move pruning and [partial expansion](/partial-expansion-a-star/) cut the number of successors generated per node.

## When to use it

Use IDA* when A* runs out of memory, the action costs take few distinct values, and the graph has few short cycles: sliding-tile puzzles, the Rubik's cube and similar permutation puzzles are the classic cases. Do not use it on grids and road maps, where many paths lead to each state: there A* or a memory-bounded best-first method such as [SMA*](/simplified-memory-bounded-a-star/) is much faster.

## Pitfalls

- **Many distinct costs.** With real-valued costs, each threshold can admit only one new node, and the run time becomes quadratic. Raise the threshold by larger steps, as IDA*_CR does.
- **Graphs with many duplicates.** Without a transposition table, IDA* explores each path to a state separately. At least skip the successor that undoes the last action.
- **Testing the goal before the cut-off.** If line L9 comes before line L8, IDA* can return a goal with $f > T$, which is not surely optimal.
- **Inadmissible heuristics.** The first goal found then need not be optimal.
- **Deep recursion.** In a language with a small stack, use an explicit stack, as the implementation does.
- **A zero-cost cycle.** The cut-off on $f$ does not bound the depth when costs can be 0, and the check against the current path is then needed for termination.

## Implementations

## History

Korf introduced depth-first iterative deepening and IDA* in 1985. He showed that iterative deepening is asymptotically optimal in time and space among brute-force tree searches, that IDA* returns optimal paths with an admissible heuristic, and that its time is of the same order as that of A* on trees whose size grows geometrically. With the Manhattan distance, IDA* found optimal solutions to random instances of the 15-puzzle, which A* could not do in the memory of the time. Sarkar, Chakrabarti, Ghose and De Sarkar (1991) addressed the quadratic case with IDA*_CR. Korf's later work combined IDA* with pattern databases for the Rubik's cube (1997), and IDA* became the standard optimal solver for permutation puzzles. In 1993 Korf gave recursive best-first search, which keeps the linear space and gets best-first order.

## References
