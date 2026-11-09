---
tag: 93DZCW
kind: concept
slug: fitness-landscape
name: Fitness landscape
aliases:
- search landscape
area: optimization/metaheuristics
level: advanced
summary: The map of solution quality over the search space and its neighborhood relation.
prereqs: [neighborhood-structure, local-optimum, local-search]
see_also: [local-optimum, neighborhood-structure, stochastic-local-search, fitness-function, multimodal-optimization, no-free-lunch-theorem, hamming-distance, max-sat]
sources:
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Chapter 5, Search Space Structure and SLS Performance, from p. 203; Section 5.3, fitness-distance analysis, from p. 220; Section 5.4, ruggedness, from p. 226, with NK landscapes from p. 231; Section 5.5, plateaus, from p. 235; Section 5.6, barriers and basins, from p. 243
  - paper: "Sewall Wright, The roles of mutation, inbreeding, crossbreeding and selection in evolution, Proceedings of the Sixth International Congress of Genetics 1, 1932"
    locator: pp. 356 to 366 (the surface of adaptive values over the space of genotypes)
  - paper: "Edward D. Weinberger, Correlated and uncorrelated fitness landscapes and how to tell the difference, Biological Cybernetics 63, 1990"
    locator: pp. 325 to 336 (the autocorrelation of a random walk and the correlation length)
  - paper: "Terry Jones and Stephanie Forrest, Fitness distance correlation as a measure of problem difficulty for genetic algorithms, Proceedings of the Sixth International Conference on Genetic Algorithms, 1995"
    locator: pp. 184 to 192 (the fitness-distance correlation coefficient)
  - paper: "Kenneth D. Boese, Andrew B. Kahng and Sudhakar Muddu, A new adaptive multi-start technique for combinatorial global optimizations, Operations Research Letters 16(2), 1994"
    locator: pp. 101 to 113 (local optima of the TSP lie close to each other and to the optimum, the big valley)
---

A fitness landscape is a set of solutions together with a [neighborhood structure](/neighborhood-structure/) and an objective, seen as a surface: the solutions are places, the neighborhood says which places are next to each other, and the objective gives the height of each place. A [local search](/local-search/) is a walk on this surface. The shape of the landscape, such as the number of [local optima](/local-optimum/), the size of their basins, the flat regions and the correlation between nearby heights, explains much of why a search method works well or badly on a problem. The same problem has different landscapes for different neighborhoods. Measures of the landscape describe instances; they do not prove how long a method will take.

## In plain words

Think of all the solutions as places on a map, with good solutions low and bad solutions high. Two places are next to each other if one small change turns one solution into the other. A search walks from place to place.

If the map is one smooth bowl, walking downhill finds the bottom. If it has many small pits, a downhill walk stops in the first pit. If it is flat in large parts, the walk has no sense of direction. If the good pits are close together, it pays to search near good solutions; if they are spread out, it pays to jump far.

## The idea

A landscape is a triple $(S, N, f)$: a finite set of solutions $S$, a neighborhood $N$, and an objective $f$, here to be minimized. Its main features are these.

- **Local minima** and their number. A landscape with one local minimum is easy for descent; one where a random point is a local minimum with high probability is hard.
- **Basins of attraction.** The basin of a local minimum is the set of starting points from which a given descent ends there. Its size is the chance that a uniform random start ends there.
- **Plateaus.** Connected sets of solutions with equal values. They are common in satisfiability, where the objective counts unsatisfied clauses and takes few values.
- **Barriers.** The least height that a walk must climb to go from one local minimum to another. High barriers trap methods that accept only small worsening moves.
- **Ruggedness.** How fast the value changes along a walk. Weinberger measured it by the autocorrelation $r(s)$ of the values $f(x_t)$ and $f(x_{t+s})$ along a long random walk, and the *correlation length* $\ell = -1 / \ln |r(1)|$. A value of $r(1)$ near 1 means a smooth landscape; near 0, a rugged one.
- **Fitness-distance correlation (FDC).** Jones and Forrest's correlation coefficient between $f(x)$ and the distance from $x$ to the nearest global optimum, over a sample of solutions, often local optima. For minimization, a value near 1 means that better solutions tend to be closer to the optimum, so a search near good solutions is likely to pay. A value near 0 or below means the landscape gives little guidance, or misleads.

For many problems the local optima of good neighborhoods lie close to each other and to the global optimum. Boese, Kahng and Muddu called this structure a *big valley* for the TSP. It is an observation on instances, not a theorem, and it is the reason for methods that search near good solutions, such as [iterated local search](/iterated-local-search/) and [path relinking](/path-relinking/).

## Examples

**Two extremes on bit strings.** Take bit strings of length $n$ with single flips.

- *A smooth landscape.* Let $f(x)$ be the number of ones, to be minimized. The only local minimum is $0 \cdots 0$, the value of $x$ equals its [Hamming distance](/hamming-distance/) to the optimum, so the FDC is exactly 1, and the random walk autocorrelation is exactly $r(1) = 1 - 2/n$: for a uniform $x$ and one random flip, the covariance of $f(x)$ and $f(y)$ is $n/4 - 1/2$ and the variance is $n/4$.
- *A rugged landscape.* Let $f$ give independent values from one continuous distribution to the $2^n$ strings. Then $r(1) = 0$, and each string is a local minimum with probability $1/(n + 1)$, so there are $2^n / (n + 1)$ local minima on average.

**A weighted MAX-SAT instance.** Take the 6-variable, 12-clause instance of the [path relinking](/path-relinking/) page, with $f$ the weight of the unsatisfied clauses, single flips, and the unique optimum 110110 of cost 1. Over all 64 assignments:

- the values range from 1 to 34, with mean 11.375;
- the random walk autocorrelation is $r(1) \approx 0.41$, so $\ell \approx 1.1$;
- the FDC over all assignments is about $0.11$, and over the 9 local minima about $0.36$.

The local minima and the basins of the best-improvement descent with ties to the lowest position are:

| local minimum | 110110 | 011101 | 001001 | 110000 | 101010 | 101110 | 010000 | 101011 | 010100 |
|---|---|---|---|---|---|---|---|---|---|
| cost | 1 | 4 | 4 | 5 | 6 | 6 | 5 | 6 | 5 |
| distance to optimum | 0 | 4 | 6 | 2 | 3 | 2 | 3 | 4 | 2 |
| basin size | 18 | 11 | 9 | 6 | 5 | 5 | 4 | 4 | 2 |

The optimum has the largest basin, so a random restart descent reaches it with probability $18/64$ per start. But the local minimum 001001, which is the complement of the optimum and as far from it as possible, has the second best cost. This part of the landscape misleads a search that looks near good solutions.

**The TSP.** On the 9-city instance of the iterated local search page, the 2-opt landscape has four local minima, of lengths 69, 70, 71 and 72.

## Where it is used

Landscape analysis is used to explain and compare the behavior of [stochastic local search](/stochastic-local-search/) methods and to choose among neighborhoods: Hoos and Stützle devote a chapter to it, with case studies on SAT and the TSP. Ruggedness and FDC help decide between methods that stay near good solutions and methods that make large jumps, the balance of [intensification and diversification](/intensification-and-diversification/). NK landscapes, with a tunable amount of interaction between bits, serve as test problems with controlled ruggedness. In biology, where Wright introduced the picture in 1932, the landscape maps genotypes to fitness and mutations define the neighbors. By the [no free lunch theorem](/no-free-lunch-theorem/), a search method can do better than another only on some classes of problems, and landscape measures are one way to describe such classes. They are statistics of instances, not proofs of performance.

## References
