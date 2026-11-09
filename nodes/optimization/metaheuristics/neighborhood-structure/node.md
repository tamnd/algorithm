---
tag: GGMMQB
kind: concept
slug: neighborhood-structure
name: Neighborhood structure
aliases:
- move operator
- neighborhood
area: optimization/metaheuristics
level: intro
summary: The rule that defines which solutions are adjacent to a given solution.
prereqs: [combinatorial-optimization-problem]
see_also: [local-search, local-optimum, fitness-landscape, two-opt, kernighan-lin, large-neighborhood-search, variable-neighborhood-search, hamming-distance]
sources:
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover, 1998
    locator: Chapter 19, Local Search (neighborhoods, the 2-opt and k-opt neighborhoods of the TSP, exact neighborhoods)
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 1.5, Stochastic Local Search, from p. 37 (the neighborhood relation and the neighborhood graph), and Section 2.1, Iterative Improvement, pp. 61 to 70 (neighborhood size, incremental evaluation)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 3, Variable Neighborhood Search, from p. 57, and Chapter 4, Large Neighborhood Search, from p. 99
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Chapter 12, Local Search (neighbor relations, the flip neighborhood for Max-Cut)
---

A neighborhood structure is the rule that gives each solution of an optimization problem a set of nearby solutions, its neighbors. Usually the rule is a *move*, a small change such as flipping one bit, swapping two elements or reversing a segment of a tour, and the neighbors of $x$ are the solutions one move away. The neighborhood is the main problem-specific choice in [local search](/local-search/): together with the objective it decides which solutions are [local optima](/local-optimum/), how long one step takes, and how far the search can see. A larger neighborhood has fewer local optima but costs more to search.

## In plain words

To improve a solution step by step, you must say what one step is. For a list of yes or no choices, one step can be to change one choice. For a route through cities, one step can be to cut the route in two places and reconnect it the other way. The solutions you can reach in one step are the neighbors.

A small step is cheap to try, but a search with small steps gets stuck easily, because every nearby solution may be worse. A large step sees more, but each try costs more.

## The idea

Let $S$ be a finite set of solutions. A neighborhood is a function $N : S \to 2^S$, and $N(x)$ is the set of neighbors of $x$. Usually $x \notin N(x)$, and the relation is symmetric: $y \in N(x)$ exactly when $x \in N(y)$. The **neighborhood graph** has the solutions as vertices and an edge from $x$ to each $y \in N(x)$.

Four properties of a neighborhood matter most.

- **Size.** The number $|N(x)|$ is the work of one full scan, for example one step of best-improvement [hill climbing](/hill-climbing/).
- **Evaluation cost.** Most good neighborhoods allow *incremental evaluation*: the change $f(y) - f(x)$ is computed from the move alone, much faster than $f(y)$ from scratch. For a 2-opt move that removes edges $(a, b)$ and $(c, d)$ of a tour and adds $(a, c)$ and $(b, d)$, the change is $d(a, c) + d(b, d) - d(a, b) - d(c, d)$, in $O(1)$ time, while a full tour length takes $O(n)$.
- **Connectivity.** If the neighborhood graph is strongly connected, every solution, the optimum included, can be reached from every start. Random walks and [stochastic local search](/stochastic-local-search/) methods need this to have any chance of reaching the optimum from every start.
- **Strength.** If $N_1(x) \subseteq N_2(x)$ for all $x$, every local minimum of $N_2$ is a local minimum of $N_1$, so the larger neighborhood has the same or fewer local minima. A neighborhood is **exact** if its only local minima are global minima.

These properties pull against each other. The neighborhood "every solution is a neighbor" is exact, but one scan is a full enumeration. The art is to find a neighborhood that is small or fast to search and still has few poor local optima.

A neighborhood together with the objective defines the [fitness landscape](/fitness-landscape/) on which a local search moves.

## Examples

The table gives the exact number of distinct neighbors for common moves. Here $n$ is the number of bits, cities, elements or vertices.

| solutions | move | $\lvert N(x) \rvert$ | for $n = 9$ |
|---|---|---|---|
| bit strings of length $n$ | flip one bit | $n$ | 9 |
| bit strings of length $n$ | flip two bits | $n(n-1)/2$ | 36 |
| tours of $n$ cities | [2-opt](/two-opt/): remove two non-adjacent edges, reconnect | $n(n-3)/2$ for $n \ge 4$ | 27 |
| sequences of $n$ elements | swap two elements | $n(n-1)/2$ | 36 |
| sequences of $n$ elements | move one element to another position | $(n-1)^2$ | 64 |

The 2-opt count holds because an $n$-city tour has $n$ edges, of which $n(n-1)/2 - n = n(n-3)/2$ pairs are not adjacent, each such pair can be reconnected in only one other way to give a tour, and different pairs give different tours, since the two removed edges are the edges of $x$ that are not in the new tour. The count $(n-1)^2$ for the insertion move is smaller than the $n(n-1)$ ways to pick an element and a new position because moving an element one place forward gives the same sequence as moving its right neighbor one place back, and there are $n - 1$ such pairs: $n(n-1) - (n-1) = (n-1)^2$.

Other common neighborhoods:

- **Max-Cut.** Move one vertex to the other side: $n$ neighbors. Every local maximum of this neighborhood cuts at least half of the total edge weight; see [maximum cut](/maximum-cut/).
- **Graph partitioning.** Swap one vertex of each side, as in [Kernighan-Lin](/kernighan-lin/), with $|A| \cdot |B|$ neighbors, or move single vertices under a balance limit, as in [Fiduccia-Mattheyses](/fiduccia-mattheyses/).
- **0-1 knapsack.** Flip one item, and keep only the feasible results; or drop one item and add another.
- **Set cover.** Drop one chosen set, or swap one chosen set for one other set, keeping a cover, as in the [GRASP](/grasp/) page.
- **TSP, larger moves.** [3-opt](/three-opt/) has $\Theta(n^3)$ neighbors, [Or-opt](/or-opt/) moves a segment of up to three cities, and [Lin-Kernighan](/lin-kernighan/) builds a variable number of edge exchanges one at a time, so it searches part of a very large neighborhood.
- **Large neighborhoods.** [Large neighborhood search](/large-neighborhood-search/) destroys part of a solution and repairs it with a heuristic or an exact method; its neighborhood can be exponential in size and is never listed in full.

## Where it is used

Every [local search](/local-search/) method and every trajectory [metaheuristic](/metaheuristic/) is built on one or more neighborhoods. [Variable neighborhood search](/variable-neighborhood-search/) changes the neighborhood on purpose: it uses nested neighborhoods to shake and a sequence of neighborhoods to descend. [Tabu search](/tabu-search/) restricts a neighborhood with a [tabu list](/tabu-list/). [Iterated local search](/iterated-local-search/) uses a perturbation, such as the double-bridge move for tours, that is outside the neighborhood of its local search so that the descent does not undo it at once. In complexity theory, a neighborhood that is searchable in polynomial time defines a [local search problem](/local-search-problem/) in the class [PLS](/pls/).

## References
