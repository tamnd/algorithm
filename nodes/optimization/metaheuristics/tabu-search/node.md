---
tag: 4KBPCC
kind: algorithm
slug: tabu-search
name: Tabu search
aliases:
- tabu
- TS
area: optimization/metaheuristics
level: core
summary: Local search that forbids recently visited moves via a memory list to escape local optima.
model: word-ram
complexity:
  vars: {K: the number of iterations, d: the size of the largest neighborhood, e: the time to evaluate f once, t: the tabu tenure, s: the size of one solution}
  time: {worst: O(K d (e + t))}
  space: {extra: O(s + t)}
properties: {deterministic: true, recursive: false}
prereqs: [local-search, hill-climbing, neighborhood-structure]
see_also: [tabu-list, aspiration-criterion, intensification-and-diversification, simulated-annealing, guided-local-search, path-relinking, knapsack-problem, metaheuristic]
sources:
  - paper: doi:10.1016/0305-0548(86)90048-1
    title: Fred Glover, Future paths for integer programming and links to artificial intelligence, Computers and Operations Research 13(5), 1986
    locator: pp. 533 to 549 (the first description of tabu search, and the term meta-heuristic)
  - paper: doi:10.1287/ijoc.1.3.190
    title: Fred Glover, Tabu Search, Part I, ORSA Journal on Computing 1(3), 1989
    locator: pp. 190 to 206 (short-term memory, tabu restrictions, aspiration criteria)
  - paper: doi:10.1287/ijoc.2.1.4
    title: Fred Glover, Tabu Search, Part II, ORSA Journal on Computing 2(1), 1990
    locator: pp. 4 to 32 (long-term memory, intensification and diversification)
  - book: isbn:9780792381877
    title: Fred Glover and Manuel Laguna, Tabu Search, Kluwer Academic Publishers, 1997
    locator: the whole book (the standard reference on the method and its memory structures)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 2, Tabu Search, by Michel Gendreau and Jean-Yves Potvin, from p. 37
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.2, 'Simple' SLS Methods, from p. 71 (tabu search with a recency memory and aspiration)
  - paper: "Roberto Battiti and Giampietro Tecchiolli, The reactive tabu search, ORSA Journal on Computing 6(2), 1994"
    locator: the whole paper (the tenure adapts to repetitions of solutions)
  - paper: "Éric Taillard, Robust taboo search for the quadratic assignment problem, Parallel Computing 17, 1991"
    locator: the whole paper (a random tenure drawn from an interval)
---

Tabu search is a [local search](/local-search/) that keeps moving after it reaches a [local optimum](/local-optimum/). At each step it moves to the best neighbor it is allowed to take, even when that neighbor is worse than the current solution. To stop the search from stepping straight back, it keeps a short memory, the [tabu list](/tabu-list/), of the moves it made recently, and it forbids moves that would undo them. An [aspiration criterion](/aspiration-criterion/) lifts the ban when a forbidden move leads to a solution better than any seen so far. Fred Glover proposed the method in 1986. It is one of the most used [metaheuristics](/metaheuristic/) for scheduling, routing and assignment problems, and it has no general guarantee of reaching a global optimum.

## In plain words

Think of a walker in a hilly field at night who wants the lowest point. A plain downhill walker stops in the first hollow. A tabu walker always takes the lowest step it can see, so in a hollow it climbs out by the least steep way. To keep from sliding straight back, it remembers its last few steps and does not undo them for a while.

The memory is short on purpose. It blocks the obvious way back, but it soon forgets, so the walker is not shut out of good places for ever. There is one exception to the ban: a forbidden step is allowed when it leads lower than any place the walker has been. The walker always remembers the lowest place it has seen, and it reports that place at the end.

## The problem

The input is a finite set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, and a [neighborhood](/neighborhood-structure/) given as a list of moves: each solution $x$ has moves $(a, y)$, where $y \in N(x)$ is the neighbor that the move reaches and $a$ is an *attribute* of the move, the thing that the tabu list stores. For flip moves on bit strings the attribute is the index of the flipped bit; for a swap of two cities in a tour it can be the pair of cities. The other inputs are a start $x_0$, a tenure $t \ge 0$ (the length of the tabu list) and a number of iterations $K$. The output is the best solution visited. The aim is a global minimum, but the method cannot prove that it found one.

## The algorithm

```pseudo id=main
TABU-SEARCH(x0, f, N, t, K)
L1  x ← x0, b ← x0, T ← empty list
L2  for k ← 1 to K do
L3      m ← none
L4      for each move (a, y) of x, with y in N(x) do
L5          if a ∈ T and f(y) ≥ f(b) then skip this move      ▷ tabu and not aspirated
L6          if m = none or f(y) < f(m) then m ← (a, y)
L7      if m = none then leave the loop
L8      (a, x) ← m                                          ▷ move, even if f gets worse
L9      append a to T; if |T| > t then remove the oldest entry of T
L10     if f(x) < f(b) then b ← x
L11 return b
```

Lines L4 to L6 scan all moves of the current solution and keep the best *admissible* one. A move is admissible if its attribute is not in the tabu list, or if it reaches a value below the best one seen so far (line L5, *aspiration by objective*). Line L8 makes the move even when $f(x)$ gets worse; this is what takes the search out of a local minimum. Line L9 keeps the attributes of the last $t$ moves, in the order of the moves. Line L10 keeps the best solution, because the current solution often gets worse.

## Example

Take a 0-1 [knapsack](/knapsack-problem/) with six items, numbered 0 to 5, and capacity $C = 15$.

| item | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| value | 9 | 9 | 12 | 7 | 2 | 8 |
| weight | 4 | 3 | 5 | 4 | 3 | 4 |

A solution is a bit string $x$, with $x_i = 1$ if item $i$ is in the knapsack. We minimize $f(x) = -(\text{total value})$, so a lower $f$ is a higher value. A move flips one bit, its attribute is the item index, and a move that breaks the capacity is not a move. Start from the empty knapsack with tenure $t = 3$ and $K = 10$. The table shows the value, so the best is the largest.

| step | move | $x$ after | weight | value | tabu list $T$ | best value |
|---|---|---|---|---|---|---|
| 1 | add 2 | 001000 | 5 | 12 | 2 | 12 |
| 2 | add 0 | 101000 | 9 | 21 | 2, 0 | 21 |
| 3 | add 1 | 111000 | 12 | 30 | 2, 0, 1 | 30 |
| 4 | add 4 | 111010 | 15 | 32 | 0, 1, 4 | 32 |
| 5 | remove 2 | 110010 | 10 | 20 | 1, 4, 2 | 32 |
| 6 | add 5 | 110011 | 14 | 28 | 4, 2, 5 | 32 |
| 7 | remove 0 | 010011 | 10 | 19 | 2, 5, 0 | 32 |
| 8 | add 3 | 010111 | 14 | 26 | 5, 0, 3 | 32 |
| 9 | remove 4 | 010101 | 11 | 24 | 0, 3, 4 | 32 |
| 10 | add 0 | 110101 | 15 | 33 | 3, 4, 0 | 33 |

Steps 1 to 4 are plain descent. After step 4 the knapsack is full, every move removes an item, and 111010 is a local minimum: [hill climbing](/hill-climbing/) stops here with value 32. Tabu search goes on. At step 5 the moves on items 0, 1 and 4 are tabu, so the only admissible move removes item 2, and the value falls to 20. In steps 6 to 9 the search changes the contents of the knapsack. At step 10, adding item 0 is tabu, because item 0 was removed at step 7, but it gives value 33, more than the best value 32, so the aspiration criterion allows it. The result 110101 has value 33, which is the optimum of this instance, found by enumeration of all 64 subsets.

## Correctness

Tabu search has no optimality guarantee, so "correct" means the following. The search stops after at most $K$ moves. The returned $b$ is the best solution among the visited ones, so $f(b)$ never gets worse and $f(b) \le f(x_0)$. The tabu list holds exactly the attributes of the last $\min(k, t)$ moves after $k$ moves. Each move is the best admissible move, and a tabu move is made only when it gives a new best value. If every move keeps a solution feasible, every visited solution is feasible.

One more result holds for aspiration by objective. As long as the current solution is the best so far and it has an improving neighbor, every improving neighbor is admissible, so the search makes the same move as best-improvement hill climbing. So tabu search starts with the full descent of hill climbing, and it never returns a worse solution than that descent. The [full proof](proofs/correctness.md) gives all steps.

## Complexity

Each iteration scans the $d$ moves of the current solution, evaluates $f$ on each in time $e$, and tests the attribute against the list in time $O(t)$. So the time is $O(K d (e + t))$. Two common changes make this smaller:

- **Tabu test in $O(1)$.** Store for each attribute the last iteration at which it may still be tabu. A move is tabu if that iteration is not yet past. Then the time is $O(K d e)$.
- **Incremental evaluation.** For many problems the change $f(y) - f(x)$ of one move costs $O(1)$, not a full evaluation. For the knapsack flip it is $\pm v_i$. Then $e = O(1)$ and an iteration costs $O(d)$.

The extra space is the current and the best solution and the list, $O(s + t)$. The number of iterations $K$ is a parameter: no bound on $K$ is known that guarantees a global optimum for the general method.

## Properties

- **Deterministic.** With a fixed neighbor order and tie rule, the search is a function of the start and the parameters. Randomness, if any, comes from added rules such as a random tenure.
- **Memory based.** The tabu list is short-term memory. Long-term memory, such as counts of how often each attribute was used, drives [intensification and diversification](/intensification-and-diversification/).
- **Aggressive.** It evaluates the whole neighborhood at each step, so one step costs as much as one pass of best-improvement hill climbing.
- **No convergence guarantee in general.** The search can cycle. In the example with $t = 0$, the search goes from 111010 to 111000 and back, again and again. A tenure $t \ge 1$ blocks cycles of length 2 but not longer ones.
- **Tenure matters, and not in one direction.** On the example, $t = 1$ and $t = 2$ end with value 32, $t = 3$ finds 33, and with $t = 4$ the four items in the full knapsack 111010 are all tabu after step 4, no move is admissible, and the search stops at line L7 with value 32.

## Variants and improvements

- **Attributes.** The list can store moves, solutions or attributes of solutions. Storing full solutions forbids exact revisits but costs memory, so most codes store attributes and accept that a tabu attribute can forbid solutions that were never visited. The [tabu list](/tabu-list/) page covers the choices.
- **Aspiration criteria.** Aspiration by objective is the most common; others allow a tabu move when no admissible move exists, or when it improves the best value in a region. See [aspiration criterion](/aspiration-criterion/).
- **Reactive tabu search.** Battiti and Tecchiolli change the tenure during the search: it grows when solutions repeat and shrinks when they do not. The Handbook of Metaheuristics has a chapter on reactive search.
- **Robust tabu search.** Taillard drew the tenure at random from an interval, for the [quadratic assignment problem](/quadratic-assignment-problem/).
- **Candidate lists.** For large neighborhoods, scan only a subset of the moves at each step.
- **Long-term memory.** Frequency memory penalizes attributes that occur often (diversification), and restarts from elite solutions return to good regions (intensification). [Path relinking](/path-relinking/) grew out of this part of the method.

## When to use it

Use tabu search when a good neighborhood exists, the moves are cheap to evaluate incrementally, and you can afford to scan the whole neighborhood at each step. It has strong records on scheduling, [vehicle routing](/vehicle-routing-problem/), [graph coloring](/graph-coloring/) and quadratic assignment. It needs no random numbers and no cooling schedule, so runs are easy to repeat.

To show the effect of the tenure, we ran the code below on 200 random knapsack instances with 12 items (values 5 to 40, weights 3 to 20, capacity half of the total weight, drawn in this order from Python `random.Random(2026)`), from the empty knapsack with $K = 100$, one run per instance since the method is deterministic. Best-improvement hill climbing reached the optimum on 73 instances. Tabu search reached it on 75 with $t = 0$, 130 with $t = 1$, 157 with $t = 3$ and 146 with $t = 5$. This is one small test, not a general ranking. Prefer [simulated annealing](/simulated-annealing/) when a full scan of the neighborhood is too expensive and random sampled moves are cheap.

## Pitfalls

- **Forgetting the best solution.** The current solution gets worse on purpose. Line L10 must keep the best one, and the result is $b$, not $x$.
- **Tabu on the wrong thing.** If the list stores the attribute of the new solution where it should store the attribute that blocks the reverse move, the reverse move stays allowed and the search cycles.
- **No aspiration.** Without it, a tabu attribute can block the best solution in the neighborhood. In the example, step 10 needs aspiration.
- **A list that is too long.** With $t$ close to the number of attributes, almost every move is tabu, and the search can stop with no admissible move (line L7).
- **Comparing against $f(x)$ instead of $f(b)$ in line L5.** Aspiration by objective compares with the best value seen, not with the current value. Comparing with $f(x)$ allows almost every tabu move and the list stops working.

## Implementations

## History

Glover introduced tabu search in his 1986 paper on integer programming and artificial intelligence, the same paper in which he used the word "meta-heuristic". His two-part paper "Tabu Search" (1989 and 1990) set out short-term memory and aspiration criteria in Part I, and long-term memory, intensification and diversification in Part II. Glover and Laguna's book (1997) is the standard reference. The chapter by Gendreau and Potvin in the Handbook of Metaheuristics surveys the method and its uses.

## References
