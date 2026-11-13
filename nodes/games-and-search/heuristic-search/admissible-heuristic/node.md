---
tag: C55SMV
kind: definition
slug: admissible-heuristic
name: Admissible heuristic
aliases:
- admissibility
- optimistic heuristic
area: games-and-search/heuristic-search
level: intro
summary: A heuristic that never overestimates the cost of a cheapest path from a state to a goal. With it, A* returns an optimal solution.
prereqs: [heuristic-function]
see_also: [consistent-heuristic, heuristic-dominance, a-star-optimality, relaxation-heuristic, pattern-database, weighted-a-star, completeness-and-optimality-of-search, sliding-tile-puzzle]
sources:
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (admissible algorithms, and the theorem that A* is admissible when h is a lower bound on the cost to a goal)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5.2 (admissible heuristics and the cost optimality of A*), Section 3.6 (the heuristics h1 and h2 of the 8-puzzle) and Section 3.6.2 (heuristics from relaxed problems)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (admissibility of A*) and Chapter 4 (heuristics as the costs of simplified models)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 2 (admissible heuristics and A*) and Chapter 4 (heuristics from abstractions and pattern databases)
---

A [heuristic function](/heuristic-function/) $h$ is *admissible* if it never overestimates: for each state $n$, $h(n)$ is at most the cost $h^*(n)$ of a cheapest path from $n$ to a goal. An admissible heuristic is optimistic, since each state looks at least as close to a goal as it is. This is the condition under which [A*](/a-star-search/) returns a cheapest solution, as Hart, Nilsson and Raphael proved in 1968. The function $h = 0$ is admissible and gives no information, and $h^*$ is admissible and gives all of it. Good heuristics lie between, as large as possible while still below $h^*$. The usual way to get one is to solve a simpler problem exactly: a [relaxed problem](/relaxation-heuristic/) or an abstraction such as a [pattern database](/pattern-database/).

## Definition

Let a state space have nonnegative action costs and a set of goal states, and let $h^*(n)$ be the cost of a cheapest path from $n$ to a goal, with $h^*(n) = \infty$ when no goal can be reached from $n$. A function $h$ from states to $[0, \infty]$ is **admissible** if

$$ h(n) \le h^*(n) \quad \text{for each state } n. $$

So $h(t) = 0$ at each goal $t$, and $h$ may take any value, $\infty$ included, at a dead end, a state from which no goal can be reached.

The word has a second, older use for algorithms: a search algorithm is admissible if it returns an optimal solution whenever one exists, see [completeness and optimality of search](/completeness-and-optimality-of-search/). The two meet in the theorem of [A* optimality](/a-star-optimality/): A* with an admissible heuristic is an admissible algorithm, under the usual conditions on the state space.

**Fact 1 (ways to build admissible heuristics).**

1. If $h$ is admissible and $0 \le h' \le h$, then $h'$ is admissible.
2. If $h_1, \ldots, h_k$ are admissible, so is $\max(h_1, \ldots, h_k)$.
3. If a problem $P'$ has the same states, at least the actions of $P$ with at most the same costs, and at least the goals of $P$, then the optimal cost $h^*_{P'}$ in $P'$ is admissible for $P$.
4. If $\phi$ maps the states of $P$ to the states of an abstract problem, each action $n \to n'$ of $P$ maps to an action $\phi(n) \to \phi(n')$ of no larger cost or to $\phi(n) = \phi(n')$, and each goal maps to an abstract goal, then $h(n) = h^*_{\text{abs}}(\phi(n))$ is admissible.

*Proof.* Items 1 and 2 follow from $h_i \le h^*$ for each $i$. For item 3, a cheapest path from $n$ to a goal in $P$ is a path to a goal in $P'$ of at most the same cost, so the cheapest path of $P'$ costs at most $h^*(n)$. For item 4, the image of a cheapest path of $P$ is an abstract path, with the steps where $\phi(n) = \phi(n')$ left out, from $\phi(n)$ to an abstract goal, and its cost is at most $h^*(n)$. $\square$

Item 3 is the source of relaxed problems, which drop preconditions of actions, and item 4 is the source of pattern databases.

## Examples and non-examples

The examples use the 8-puzzle with unit costs, the goal with the blank in the top left corner and the tiles 1 to 8 in order, and the start state of Russell and Norvig with rows 7 2 4, 5 _ 6 and 8 3 1.

- **Misplaced tiles.** $h_1$ counts the tiles that are not on their goal square, the blank not included. Each such tile must move at least once, and each move moves one tile, so $h_1 \le h^*$. For the start state, $h_1 = 8$, because every tile is out of place.
- **Manhattan distance.** $h_2$ adds, over the tiles, the number of rows plus columns between the square of a tile and its goal square. A move takes one tile one square, so it lowers the sum by at most 1, and $h_2 \le h^*$. For the start state the eight tiles 7, 2, 4, 5, 6, 8, 3, 1 contribute 3, 1, 2, 2, 2, 3, 3, 2, so $h_2 = 18$. The true cost, from a [breadth-first search](/breadth-first-search/) of all 181,440 states that can reach the goal, is $h^* = 26$. Both heuristics are admissible, and $h_2$ is closer.
- **Relaxations behind them.** If a tile may move to any square, the cost of the relaxed problem is $h_1$. If a tile may move to any next square, occupied or not, it is $h_2$. Both are cases of item 3 of Fact 1.
- **Straight-line distance.** On a road map, no road between two places is shorter than the straight line, so the straight-line distance to the goal is admissible.
- **A sum that overestimates.** $h_1 + h_2$ is not admissible. The state that is one move from the goal, with tile 1 and the blank swapped, has $h_1 = 1$ and $h_2 = 1$ but $h^* = 1$, so the sum 2 is too large. The maximum of $h_1$ and $h_2$ is admissible, by Fact 1. Sums are admissible only when the parts count disjoint sets of moves, as in additive pattern databases.
- **The wrong metric for the moves.** On a grid with diagonal moves of cost $\sqrt{2}$, the Manhattan distance is not admissible: one diagonal step lowers it by 2 at cost $\sqrt{2} < 2$. The octile distance, $\sqrt{2}\min(\Delta x, \Delta y) + |\Delta x - \Delta y|$, is the cost of a cheapest path on the empty grid, and it is admissible.
- **A heuristic scaled up.** $w h$ with $w > 1$ is usually not admissible. [Weighted A*](/weighted-a-star/) uses it on purpose and returns a path that costs at most $w C^*$, so it is called $w$-admissible.
- **A dead end.** If no goal can be reached from $n$, then $h^*(n) = \infty$ and each value of $h(n)$ is admissible. A heuristic that detects dead ends and returns $\infty$ prunes them at no risk.

## Related definitions

- **[Consistent heuristic](/consistent-heuristic/).** The stronger condition $h(n) \le c(n, n') + h(n')$ for each action, with $h = 0$ at goals. Each consistent heuristic is admissible. An admissible heuristic that is not consistent can make A* reopen states, and A* without reopening can then return a path that is too expensive.
- **[Heuristic dominance](/heuristic-dominance/).** For two admissible heuristics, $h_2$ dominates $h_1$ if $h_2 \ge h_1$ everywhere. Then each state that A* must expand with $h_2$ it must also expand with $h_1$, so up to ties $h_2$ is never worse. The Manhattan distance dominates the misplaced tiles, since a misplaced tile is at least one square from its goal.
- **Optimistic and pessimistic bounds.** An admissible $h$ is a lower bound on the cost to go. An upper bound, from any known solution, is used by branch and bound and by bounded searches to prune.
- **$\epsilon$-admissibility.** A search is $\epsilon$-admissible if it returns a solution of cost at most $(1 + \epsilon) C^*$. Weighted A* with $w = 1 + \epsilon$ is one, with an admissible $h$.
- **[Evaluation function](/evaluation-function/).** In game playing, a static evaluation scores a position for one player. It is not an estimate of a cost to go, and admissibility has no meaning for it.

## References
