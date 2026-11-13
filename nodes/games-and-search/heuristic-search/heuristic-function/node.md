---
tag: 383VGH
kind: definition
slug: heuristic-function
name: Heuristic function
aliases:
- heuristic
area: games-and-search/heuristic-search
level: intro
summary: A function h(n) that estimates the cost of a cheapest path from a state n to a goal. Informed searches such as A* use it to decide which state to expand next.
prereqs: [state-space-search]
see_also: [admissible-heuristic, consistent-heuristic, heuristic-dominance, evaluation-function, a-star-search, greedy-best-first-search, relaxation-heuristic, pattern-database]
sources:
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 1 (heuristics and problem representations) and Chapter 4 (heuristics as the costs of simplified models)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5 (informed search and the heuristic function h(n)) and Section 3.6 (heuristic functions, their accuracy, relaxed problems and pattern databases)
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the estimate h of the cost from a node to a goal, and f = g + h)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 1 (heuristics and their properties) and Chapter 4 (automatically created heuristics)
---

A heuristic function $h$ gives, for each state $n$ of a [state-space search](/state-space-search/) problem, an estimate $h(n)$ of the cost of a cheapest path from $n$ to a goal. It is the knowledge about the problem that an informed search adds to the bare state space. [Greedy best-first search](/greedy-best-first-search/) expands the state of least $h$, and [A*](/a-star-search/) the state of least $f = g + h$, where $g$ is the cost so far. The heuristic depends only on the state, not on the path to it, and it should be cheap to compute. Its quality is measured by how close it is to the true cost $h^*$ and by how many states the search then expands. The two main properties that make it safe for optimal search are [admissibility](/admissible-heuristic/) and [consistency](/consistent-heuristic/).

## Definition

Let a state-space search problem have states $S$, nonnegative action costs and a set of goal states. The *perfect heuristic* $h^*(n)$ is the cost of a cheapest path from $n$ to a goal, or $\infty$ if no goal can be reached from $n$. A **heuristic function** is a function

$$ h : S \to [0, \infty], $$

computable from the state alone, with $h(t) = 0$ at each goal $t$. Its value $h(n)$ is read as an estimate of $h^*(n)$. Some authors do not require $h = 0$ at goals, but each common property of heuristics includes it.

A search uses $h$ through an *evaluation function* $f$ that orders the states in OPEN:

| search | $f(n)$ |
| --- | --- |
| [uniform-cost search](/uniform-cost-search/) | $g(n)$ |
| greedy best-first search | $h(n)$ |
| A* | $g(n) + h(n)$ |
| [weighted A*](/weighted-a-star/) | $g(n) + w\,h(n)$, $w > 1$ |

The heuristic is the part of $f$ that looks forward. The cost $g(n)$ looks back, and it depends on the path, so it is not a heuristic.

The common properties, each defined on its own page:

- **Admissible:** $h(n) \le h^*(n)$ for all $n$.
- **Consistent:** $h(n) \le c(n, n') + h(n')$ for each action, and $h = 0$ at goals.
- **Dominance:** $h_2$ [dominates](/heuristic-dominance/) $h_1$ if both are admissible and $h_2 \ge h_1$ everywhere.

**Fact (the perfect heuristic).** Let all action costs be positive and let a goal be reachable. A* with $h = h^*$ and ties broken toward larger $g$ expands exactly the states of one cheapest path, the goal not included.

*Proof.* Each state on a cheapest path from $s_0$ to a goal has $g^* + h^* = C^*$, and each state reached with $g^* + h^* > C^*$ is never removed before the goal, since a state of $f = C^*$ is always in OPEN until then. Suppose that A* has expanded the states $p_0 = s_0, p_1, \ldots, p_i$ of a cheapest path, each with $f = C^*$, and that $p_i$ is not a goal. Some successor $p'$ of $p_i$ starts the rest of a cheapest path, so it enters OPEN with $f = C^*$ and $g = g(p_i) + c > g(p_i)$. Every other entry of OPEN with $f = C^*$ came from an earlier $p_j$ and was not chosen before $p_i$, so its $g$ is at most $g(p_i)$, by the tie rule. So the next state removed is a successor of $p_i$ with $f = C^*$, and the expanded states form one path. $\square$

## Examples and non-examples

- **Manhattan distance.** In the 8-puzzle, the sum over the tiles of the rows and columns between a tile and its goal square. It is admissible and consistent.
- **Misplaced tiles.** In the 8-puzzle, the number of tiles not on their goal square. It is weaker than the Manhattan distance.
- **Straight-line distance.** For routes on a map, the distance in the plane to the goal.
- **Pattern databases.** A table of exact costs in an abstract problem that keeps only some of the tiles, built once by a search backward from the goal and then read at each state.
- **Relaxed planning heuristics.** In planning, the cost of a simpler problem in which actions do not delete facts. These are computed anew at each state and can be inconsistent.
- **Not a heuristic function: a chess evaluation.** The [evaluation function](/evaluation-function/) of a game program gives a static score of a position for one player. It does not estimate a cost to a goal, and $h = 0$ at goals has no meaning for it. The two names are close, and R&N also call the $f$ of best-first search an evaluation function, but they are different things.
- **Not a heuristic function: $g$.** The cost so far depends on the path that reached a state, so two paths to one state give two values.
- **Not a heuristic function: a rule of thumb.** In the broad sense, any rule that guides a choice, such as "try the most constrained variable first", is called a heuristic. It is not a function from states to estimates of cost.
- **The two extremes.** $h = 0$ is a heuristic function. It makes A* the same as uniform-cost search. $h = h^*$ is one too, and by the fact above A* then walks straight along a cheapest path. In the example of the page on A*, the counts of expanded states are 7 for $h = 0$, 5 for the Manhattan distance and 3 for $h^*$.

## Related definitions

- **Heuristic search.** Search that uses a heuristic function to choose what to expand. The area of this page is named for it.
- **Informedness.** A heuristic is more informed than another if it is closer to $h^*$. [Dominance](/heuristic-dominance/) is the formal version for admissible heuristics, and the [effective branching factor](/effective-branching-factor/) is a measured one.
- **Cost of the heuristic.** A better heuristic usually costs more time per state. The total time is the number of states expanded times the cost per state, so a cheap and weaker heuristic can win.
- **[Pathmax](/pathmax/).** A rule that raises $h$ during the search from the values at the neighbors, without losing admissibility.
- **[Evaluation function](/evaluation-function/).** In games, the static score of a position, as above.
- **Distance estimate.** On a graph with a metric, such as a road network, a lower bound on the distance from a node to the target. The [ALT algorithm](/alt-algorithm/) builds one from landmarks.

## References
