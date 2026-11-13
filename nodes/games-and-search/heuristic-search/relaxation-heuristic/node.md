---
tag: 2WVNT9
kind: concept
slug: relaxation-heuristic
name: Relaxation heuristic
aliases:
- relaxed-problem heuristic
area: games-and-search/heuristic-search
level: core
summary: A heuristic whose value is the exact cost of a relaxed problem, made by dropping constraints on the actions. It is admissible and consistent, and useful only when the relaxed problem is easy.
prereqs: [heuristic-function, admissible-heuristic, consistent-heuristic]
see_also: [heuristic-dominance, pattern-database, a-star-search, sliding-tile-puzzle, delete-relaxation, h-max-heuristic, lp-relaxation, held-karp-bound]
sources:
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 4 (heuristics viewed as information provided by simplified models, the derivation of the 8-puzzle heuristics by deleting constraints)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.6.2 (generating heuristics from relaxed problems, the 8-puzzle rule and its three relaxations)
  - paper: doi:10.1016/0020-0255(84)90009-4
    title: Marco Valtorta, A result on the computational complexity of heuristic estimates for the A* algorithm, Information Sciences 34(1) (1984)
    locator: pp. 47 to 59 (A* with a heuristic computed by blind search in a relaxed space that keeps the states expands every state that blind search expands)
  - paper: Robert C. Holte, M. B. Perez, Robert M. Zimmer and Alan J. MacDonald, Hierarchical A*, searching abstraction hierarchies efficiently, Proceedings of AAAI-96 (1996)
    title: Hierarchical A*, searching abstraction hierarchies efficiently
    locator: pp. 530 to 535 (Valtorta's barrier for embeddings, and homomorphic abstractions with caching that beat blind search)
  - paper: John Gaschnig, Performance measurement and analysis of certain search algorithms, PhD thesis, Carnegie-Mellon University, report CMU-CS-79-124 (1979)
    title: Performance measurement and analysis of certain search algorithms
    locator: the thesis as a whole (the 8-puzzle experiments with A* and the heuristic in which a tile may move into the blank from any square)
  - paper: doi:10.1007/BF00993063
    title: Armand E. Prieditis, Machine discovery of effective admissible heuristics, Machine Learning 12 (1993)
    locator: pp. 117 to 141 (the Absolver II system, which finds admissible heuristics by transforming the problem with relaxations and abstractions)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 4 (automatically created heuristics, abstraction transformations, embeddings and homomorphisms, and Valtorta's theorem)
---

A relaxation heuristic estimates the cost from a state to a goal as the exact cost of an optimal solution of a *relaxed problem*, a copy of the problem in which some constraints on the actions are dropped. Each solution of the real problem is still a solution of the relaxed one, at no larger cost, so the estimate never exceeds the true cost: the heuristic is [admissible](/admissible-heuristic/), and it is also [consistent](/consistent-heuristic/). Pearl (1984) described heuristics in general as information from such simplified models, and the two classic [heuristic functions](/heuristic-function/) of the [sliding tile puzzles](/sliding-tile-puzzle/), the misplaced tiles and the Manhattan distance, are relaxations. A relaxation helps only when its problem is much easier than the real one: Valtorta (1984) showed that a relaxed problem solved by blind search inside [A*](/a-star-search/) costs at least as much work as blind search of the real problem.

## In plain words

To guess how hard a task is, pretend that some rule does not exist and solve the easier task exactly. In a sliding puzzle, a tile can only slide into the empty square next to it. Pretend that tiles can pass through each other, and each tile needs only as many steps as it is far from its home: add them up. Pretend that a tile can jump to its home in one step, and the answer is the number of tiles that are not home.

The easier task never needs more steps than the real one, because every real solution also solves the easy task. So the guess is never too high, which is what a shortest path search needs. The trick works only if the easy task is fast to solve. If it is as hard as the real one, you gain nothing.

## The idea

### Definition

A problem $P$ has a set of states $S$, actions $s \to t$ with costs $c(s, t) \ge 0$, and a set of goal states $T \subseteq S$. Write $h^*_P(s)$ for the cost of a cheapest path from $s$ to $T$, and $\infty$ when there is none. A *relaxation* of $P$ is a problem $P'$ with states $S'$, costs $c'$, goals $T'$, and a map $\varphi : S \to S'$ such that

1. for each action $s \to t$ of $P$, the relaxed problem has a path from $\varphi(s)$ to $\varphi(t)$ of cost at most $c(s, t)$, and
2. $\varphi(T) \subseteq T'$.

The relaxation heuristic is $h(s) = h^*_{P'}(\varphi(s))$. In the common case $\varphi$ is the identity and $P'$ has all the actions of $P$ and more, because some preconditions are gone. Edelkamp and Schroedl (Chapter 4) call this an *embedding*. When $\varphi$ merges states, $P'$ is an *abstraction*, and a table of its costs is a [pattern database](/pattern-database/).

### Why the estimate is admissible and consistent

**Fact.** A relaxation heuristic is consistent, and $h(t) = 0$ for each goal $t$. So it is admissible.

*Proof.* Let $s \to t$ be an action of $P$. A cheapest relaxed path from $\varphi(t)$ to $T'$, after a relaxed path from $\varphi(s)$ to $\varphi(t)$ of cost at most $c(s, t)$, is a relaxed path from $\varphi(s)$ to $T'$. So $h(s) \le c(s, t) + h(t)$, also when $h(t) = \infty$. For a goal $t$, $\varphi(t) \in T'$, so $h(t) = 0$. A consistent heuristic with value $0$ at the goals is admissible, by the induction along a cheapest path that the page [consistent heuristic](/consistent-heuristic/) gives. $\square$

The proof uses only the [triangle inequality](/triangle-inequality/) of distances in $P'$, so the result holds for each relaxation whose cost is computed exactly. If a program computes the relaxed cost only approximately, as planners do with the [delete relaxation](/delete-relaxation/), an approximation from above can lose admissibility, and an approximation from below can lose consistency.

### More relaxed means less informed

If $P''$ relaxes $P'$ with the identity map, each relaxed path of $P'$ is a path of $P''$, so $h'' \le h'$ at every state. The less relaxed problem gives the [dominant](/heuristic-dominance/) heuristic, and A* with it expands no more states, up to ties at the optimal cost. The cost of a lookup goes the other way: the less relaxed problem is harder to solve, and with no relaxation at all the heuristic is $h^*$ and computing it solves the problem.

### Decomposition

A relaxed problem is cheap to solve when it falls apart into independent parts. Suppose the state is a tuple $(x_1, \ldots, x_k)$, each relaxed action changes one part $x_i$, and its precondition and cost depend only on $x_i$. Then the actions of one part never help or block another, so a cheapest relaxed solution is a cheapest solution for each part, in any order, and the relaxed cost is the sum $\sum_i d_i(x_i)$ of the costs of the parts. The Manhattan distance is this sum with one part per tile. A sum of heuristics for parts that are not independent can overestimate. The page [admissible heuristic](/admissible-heuristic/) gives such a case, and additive pattern databases give the condition under which a sum stays admissible.

### The cost of solving the relaxed problem

A relaxation is a good heuristic only if its cost has a closed form or a fast algorithm. Valtorta (1984) proved a limit for embeddings: if A* computes $h(s)$ for each state it meets by a blind search of the relaxed space, then A* must expand every state that a blind search of the real space expands, and it does the relaxed searches on top. So the total work is never less than that of blind search. Holte, Perez, Zimmer and MacDonald (1996) got past this limit with abstractions that merge many states into one and with caches of the abstract distances, and their Hierarchical A* beat blind search on all the spaces they studied.

## Examples

### Three relaxations of the 8-puzzle

Write the move rule as a precondition, as Pearl (Chapter 4) and Russell and Norvig (Section 3.6.2) do: *a tile can move from square A to square B if A is next to B and B is blank.* The goal is $(1, 2, 3, 4, 5, 6, 7, 8, \text{blank})$, row by row. Dropping one condition or both gives three relaxed problems, each with an exact cost that is easy to compute.

| condition dropped | relaxed move | exact relaxed cost |
| --- | --- | --- |
| both | a tile goes to any square, occupied or not | the number of misplaced tiles $h_{\text{mis}}$ |
| B is blank | a tile goes to a next square, occupied or not | the Manhattan distance $h_{\text{man}}$, a sum over the tiles |
| A is next to B | a tile jumps into the blank from any square | Gaschnig's heuristic $h_{\text{gas}}$, given below |

The first two relaxed problems decompose into one part per tile. The third does not, since all moves use the one blank.

**Gaschnig's heuristic.** In the third relaxation a move swaps the blank with any tile, so a solution sorts the board by swaps that involve the blank. Map each square to the goal square of its content. This is a [permutation](/permutation/) of the 9 squares, and it splits into cycles, as the page [permutation cycle decomposition](/permutation-cycle-decomposition/) describes. Let $m$ be the number of squares on cycles of length at least 2, let $k$ be the number of those cycles that do not hold the blank, and let $b = 1$ if the blank is not on its goal square and $b = 0$ otherwise. Then

$$h_{\text{gas}} = m + k - b .$$

Each cycle of length $L \ge 2$ that holds the blank costs $L - 1$ swaps, and each other cycle of length $L \ge 2$ costs $L + 1$. To prove the formula, look at one swap of the blank with a tile $x$. If $x$ is on the blank's cycle, the swap splits that cycle in two. When $x$ is the tile that belongs on the blank's square, $x$ goes home, and the formula drops by exactly 1. Each other split makes a new cycle of length at least 2 without the blank, and the formula goes up by 1. If $x$ is on another cycle of length $L \ge 2$, the swap merges the two cycles into one cycle that holds the blank, and the formula drops by exactly 1. If $x$ is already home, the merge puts it on the blank's cycle, and the formula goes up by 1. So no swap lowers the formula by more than 1, and the formula is $0$ only at the goal, which proves the lower bound. The rule "if the blank is not home, swap it with the tile that belongs on its square, else swap it with any misplaced tile" lowers the formula by 1 at each swap, so the bound is reached.

**Two boards.** Neither the Manhattan distance nor Gaschnig's heuristic dominates the other.

| board, row by row | $h_{\text{mis}}$ | $h_{\text{man}}$ | $h_{\text{gas}}$ | $h^*$ |
| --- | --- | --- | --- | --- |
| 1 2 3 / 5 4 6 / 8 7 blank | 4 | 4 | 6 | 14 |
| 5 1 3 / 4 blank 2 / 7 8 6 | 4 | 6 | 4 | 12 |

On the first board the tiles 4 and 5 are swapped, and so are 7 and 8. Each swapped pair is a cycle of length 2 without the blank, so $h_{\text{gas}} = 3 + 3$. The Manhattan distance gives only 1 per tile. On the second board the blank's cycle holds 5 squares, so $h_{\text{gas}} = 4$, but the tiles 2, 5 and 6 are far from home.

**Over all 181,440 solvable boards.** A [breadth-first search](/breadth-first-search/) from the goal gives $h^*$ at every board. The mean values are $h_{\text{mis}} = 7.11$, $h_{\text{gas}} = 8.05$, $h_{\text{man}} = 14.00$, $\max(h_{\text{man}}, h_{\text{gas}}) = 14.003$ and $h^* = 21.97$. Gaschnig's heuristic is larger than the Manhattan distance on 304 boards, smaller on 177,591 and equal on 3,545. On 100 boards drawn with a fixed seed, A* with ties toward larger $g$ expands on average 90,107 states with $h = 0$, 10,987 with $h_{\text{mis}}$, 6,822 with $h_{\text{gas}}$, 730 with $h_{\text{man}}$ and 722 with the maximum of the last two. The maximum is admissible and consistent because each part is.

### Grid maps

On a 4-connected grid with unit costs, delete all obstacles: the relaxed cost from $(x, y)$ to $(x_g, y_g)$ is the Manhattan distance $|x - x_g| + |y - y_g|$. On an 8-connected grid with costs 1 and $\sqrt 2$, the relaxed cost is the octile distance $\max(\Delta x, \Delta y) + (\sqrt 2 - 1)\min(\Delta x, \Delta y)$. Whether the real grid allows a diagonal move past a blocked corner does not matter here, since the relaxed grid has no obstacles. The straight-line [Euclidean distance](/euclidean-distance/) relaxes further: it also drops the grid and lets the agent move at any angle, so it is never larger than the octile distance, and it is the natural heuristic of [Theta*](/theta-star/).

### A tour and a tree

For the [traveling salesman problem](/traveling-salesman-problem/), drop the condition that the edges chosen form a cycle and keep only that they connect all cities. The relaxed optimum is a [minimum spanning tree](/minimum-spanning-tree/). Deleting one edge of an optimal tour leaves a spanning tree, so the tree costs no more than the tour. The 1-tree of the [Held-Karp bound](/held-karp-bound/) and the [LP relaxation](/lp-relaxation/) of an integer program are relaxations of the same kind, used as lower bounds in exact optimization.

### Dropping delete effects in planning

In classical planning an action has preconditions, facts it adds and facts it deletes. The [delete relaxation](/delete-relaxation/) ignores the deletes. Its exact cost $h^+$ is admissible by the fact above, but computing it is NP-hard, so planners use approximations of it such as the [h-max](/h-max-heuristic/) and [h-add](/h-add-heuristic/) heuristics. These pages give the details.

## Where it is used

- **Heuristics for puzzles.** The misplaced tiles and the Manhattan distance for the sliding tile puzzles, and as building blocks of stronger heuristics: the maximum of several relaxations, and [pattern databases](/pattern-database/), which take the abstraction route.
- **Path finding on maps and grids.** The Manhattan, octile and Euclidean distances are the standard heuristics of [A*](/a-star-search/), [jump point search](/jump-point-search/) and the incremental searches such as [D* Lite](/d-star-lite/), where the free-space assumption about unknown cells is itself a relaxation of the true map.
- **Domain-independent planning.** The [HSP planner](/hsp-planner/) and its successors compute heuristics from the delete relaxation, and the [relaxed plan heuristic](/relaxed-plan-heuristic/) extracts a plan of the relaxed problem.
- **Automatic discovery of heuristics.** Prieditis (1993) built Absolver II, a program that applies relaxations and abstractions to a description of a problem and keeps the transformed problems that are cheap to solve. It found many known heuristics and the first known effective admissible heuristic for Rubik's Cube.
- **Bounds in exact optimization.** Branch and bound methods for the traveling salesman problem and for integer programs prune with relaxations such as the spanning tree, the LP relaxation and [Lagrangian relaxation](/lagrangian-relaxation/).

## References
