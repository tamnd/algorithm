---
tag: N8CBT7
kind: definition
slug: local-optimum
name: Local optimum
aliases:
- local maximum
- local minimum
- locally optimal solution
area: optimization/metaheuristics
level: intro
summary: A solution no neighbor improves, though a better solution may exist elsewhere.
prereqs: [neighborhood-structure, combinatorial-optimization-problem]
see_also: [local-search, hill-climbing, neighborhood-structure, fitness-landscape, local-search-problem, pls, maximum-cut, global-optimization]
sources:
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover, 1998
    locator: Chapter 19, Local Search (neighborhoods, local optima, exact neighborhoods)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 12.4, Maximum-Cut Approximation via Local Search (a local optimum of the flip neighborhood cuts at least half of the total weight)
  - paper: doi:10.1016/0022-0000(88)90046-3
    title: David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1), 1988
    locator: pp. 79 to 100 (the class PLS of problems of finding a local optimum)
  - paper: doi:10.1137/0220004
    title: Alejandro A. Schäffer and Mihalis Yannakakis, Simple local search problems that are hard to solve, SIAM Journal on Computing 20(1), 1991
    locator: pp. 56 to 87 (PLS-completeness of local Max-Cut with the flip neighborhood)
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Chapter 5, Search Space Structure and SLS Performance, from p. 203 (local minima, plateaus, basins)
---

A local optimum is a solution that no solution in its [neighborhood](/neighborhood-structure/) improves. For minimization it is a local minimum: every neighbor has an equal or larger objective value. A local optimum need not be a global optimum, a best solution overall, and whether a solution is a local optimum depends on the neighborhood, not only on the objective. A [local search](/local-search/) that only accepts improving moves stops at a local optimum, which is why escaping local optima is the main task of a [metaheuristic](/metaheuristic/). Finding some local optimum can itself be hard: for Max-Cut with single-vertex flips, it is complete for the class [PLS](/pls/).

## Definition

Let $S$ be a finite set of solutions, $f : S \to \mathbb{R}$ an objective to minimize, and $N : S \to 2^S$ a neighborhood, with $N(x)$ the set of neighbors of $x$.

- $x \in S$ is a **local minimum** with respect to $N$ if $f(x) \le f(y)$ for every $y \in N(x)$. It is a **strict** local minimum if $f(x) < f(y)$ for every $y \in N(x)$.
- $x^*$ is a **global minimum** if $f(x^*) \le f(y)$ for every $y \in S$.
- A **local maximum** and a **global maximum** are defined in the same way with the inequalities reversed. A **local optimum** is a local minimum or a local maximum, as fits the problem.

Three facts follow at once.

1. Every global minimum is a local minimum for every neighborhood.
2. If $N_1(x) \subseteq N_2(x)$ for all $x$, then every local minimum for $N_2$ is a local minimum for $N_1$. A larger neighborhood has the same or fewer local minima.
3. Every finite $S$ has a local minimum, since a global minimum exists.

A neighborhood is **exact** if every local minimum is a global minimum (Papadimitriou and Steiglitz). For the [minimum spanning tree](/minimum-spanning-tree/) problem, the neighborhood "add one edge and remove one edge of the cycle it closes" is exact. For an NP-hard problem, an exact neighborhood with a polynomial-time test for local optimality would give a polynomial-time test for global optimality, so such neighborhoods are not expected. Exact neighborhoods for such problems exist, for example the neighborhood in which every solution is a neighbor, but they are too large to search.

## Examples and non-examples

**A local but not global minimum.** On the 9-city instance of the [iterated local search](/iterated-local-search/) page, the 2-opt neighborhood has exactly four local minima, of lengths 69, 70, 71 and 72, counting each cycle once. Only the tour of length 69 is a global minimum. A 2-opt descent from the tour $0, 1, \ldots, 8$ stops at the one of length 72.

**The neighborhood decides.** On the Max-Cut example of the [variable neighborhood search](/variable-neighborhood-search/) page, with $f$ the weight of the uncut edges, the single-flip neighborhood has local minima of values 6, 8 and 11 (up to taking the complement of the cut). The assignment 11100010, of value 11, is a local minimum for single flips, but its double-flip neighbor 11000011 is better. With single and double flips together, only the local minima of values 6 and 8 remain, as fact 2 allows.

**Many local minima.** On the weighted MAX-SAT example of the [path relinking](/path-relinking/) page, 9 of the 64 assignments are local minima for single flips, and only 1 is global. On the set cover example of the [GRASP](/grasp/) page, the drop and swap moves have three local minima, of costs 23, 24 and 27.

**Random objectives.** Let $f$ give independent values, all distinct with probability 1, from one continuous distribution to the $2^n$ bit strings of length $n$, with single flips as the neighborhood. A bit string and its $n$ neighbors form $n + 1$ points, and each of them is equally likely to have the least value, so a given string is a local minimum with probability $1/(n + 1)$. The expected number of local minima is $2^n / (n + 1)$.

**A local optimum with a guarantee.** For Max-Cut on a graph with nonnegative edge weights of total $W$, take the neighborhood that moves one vertex to the other side. If no move increases the cut, then at each vertex $v$ the cut edges weigh at least as much as the uncut edges. Adding over all vertices counts each cut edge twice on the left and each uncut edge twice on the right, so the cut weighs at least $W/2$. So every local maximum is within a factor 2 of the global maximum (Kleinberg and Tardos).

**Non-examples.** A solution with one strictly better neighbor is not a local minimum, even if all its other neighbors are worse. A point on a plateau, where some neighbors have the same value, is a local minimum but not a strict one; a search that stops there may stop on the flat part of a slope that goes down further away.

## Related definitions

- **[Neighborhood structure](/neighborhood-structure/).** The relation that a local optimum is defined by.
- **Basin of attraction.** The set of starting points from which a given descent ends at a given local minimum. On the MAX-SAT example of the path relinking page, 18 of the 64 starts lead a best-improvement single-flip descent with ties to the lowest position to the global minimum. See [fitness landscape](/fitness-landscape/).
- **Plateau.** A connected set of solutions with the same value; a plateau of local minima is a set where no member has a better neighbor.
- **[Local search problem](/local-search-problem/) and [PLS](/pls/).** The task of finding some local optimum, given $S$, $f$ and $N$ by polynomial-time algorithms, defines the class PLS of Johnson, Papadimitriou and Yannakakis. Schäffer and Yannakakis proved that local Max-Cut with the flip neighborhood is PLS-complete, and that a descent can need exponentially many improving steps on some instances from some starts.
- **Global optimum.** See [global optimization](/global-optimization/).

## References
