---
tag: X6FC7X
kind: algorithm
slug: pareto-local-search
name: Pareto local search
aliases:
- PLS
- multi-objective local search
- Pareto local search algorithm
area: optimization/multi-objective
level: advanced
summary: Local search on an archive of non-dominated solutions. It visits each member once and adds every neighbour that no member weakly dominates, until all members are visited.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {V: the number of solutions visited, D: the number of neighbours of one solution, M: the largest archive size, p: the number of objectives, n: the length of a solution, c: the cost of one evaluation of f}
  time: {worst: O(V D (c + n + p M))}
  space: {extra: O(M (n + p))}
properties: {deterministic: true, iterative: true, population: false, elitist: true}
history:
  year: 2004
  people: [Luís Paquete, Marco Chiarandini, Thomas Stützle, Eric Angel, Evripidis Bampis, Laurent Gourvès]
  note: Paquete, Chiarandini and Stützle, and independently Angel, Bampis and Gourvès, published Pareto local search for the biobjective traveling salesman problem in the same 2004 volume.
prereqs: [local-search, pareto-dominance, pareto-front]
see_also: [hill-climbing, iterated-local-search, multi-objective-simulated-annealing, paes, moea-d, multi-objective-knapsack, traveling-salesman-problem, hypervolume-indicator]
sources:
  - paper: doi:10.1007/978-3-642-17144-4_7
    title: Luís Paquete, Marco Chiarandini and Thomas Stützle, Pareto local optimum sets in the biobjective traveling salesman problem, an experimental study, in X. Gandibleux, M. Sevaux, K. Sörensen and V. T'kindt (eds.), Metaheuristics for Multiobjective Optimisation, Lecture Notes in Economics and Mathematical Systems 535, Springer, 2004, 177-199
    locator: the definition of a Pareto local optimum set and the Pareto local search algorithm with 2-opt and 3-opt neighbourhoods
  - paper: doi:10.1007/s10479-007-0230-0
    title: Luís Paquete, Tommaso Schiavinotto and Thomas Stützle, On local optima in multiobjective combinatorial optimization problems, Annals of Operations Research 156(1), 2007, 83-97
    locator: the local optimality notions, the Pareto local search and its termination in a Pareto local optimum set
  - paper: doi:10.1016/S0377-2217(96)00116-6
    title: Matthias Ehrgott and Kathrin Klamroth, Connectedness of efficient solutions in multiple criteria combinatorial optimization, European Journal of Operational Research 97(1), 1997, 159-166
    locator: the efficient graph and examples where the efficient set is not connected
  - paper: doi:10.1007/s10732-009-9103-9
    title: Thibaut Lust and Jacques Teghem, Two-phase Pareto local search for the biobjective traveling salesman problem, Journal of Heuristics 16(3), 2010, 475-510
    locator: the two-phase method, weighted sum solutions as the start of Pareto local search
---

Pareto local search (PLS) is [local search](/local-search/) for several objectives, given by Paquete, Chiarandini and Stützle in 2004. It keeps an archive of solutions whose images do not dominate each other, visits each member once, and adds every neighbour whose image no member weakly dominates. It stops when every member has been visited. On a finite space it always stops, and the result is a Pareto local optimum set: no neighbour of a member dominates a member. It is the whole [Pareto front](/pareto-front/) only under extra hypotheses, for example a complete neighbourhood or a connected efficient set.

## In plain words

The search keeps a list of the best trade-offs found so far, where nothing on the list beats anything else on it. It takes a solution from the list that it has not explored yet and tries every small change of it. A changed solution goes on the list if nothing on the list is at least as good in every cost. When it goes on, it pushes out the solutions that it beats. The search marks the explored solution and takes the next one. It stops when it has explored every solution on the list. There is no temperature and no randomness: only improving trade-offs are kept.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size (PLS has no population; its archive plays that role), and $y = f(x)$ is the image of $x$.

The input is a finite search space $X$, a neighbour set $\mathcal{N}(x)$ for each $x$, the map $f : X \to \mathbb{R}^p$ and a start solution $x_0$. The output is a set $A$ of solutions with mutually non-dominated images such that every neighbour of a member has an image that some member weakly dominates. This is an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem.

## The algorithm

```pseudo id=main
PLS(x_0, f, 𝒩)
L1  A ← {x_0}, with x_0 marked unvisited
L2  while A has an unvisited member do
L3      x ← the oldest unvisited member of A
L4      for each x' ∈ 𝒩(x) do
L5          if some member of A weakly dominates f(x') then skip x'
L6          remove from A the members that f(x') dominates; add x' unvisited
L7      mark x visited
L8  return A
```

Line L6 can remove $x$ itself, when a neighbour dominates it; the visit still ends normally. The order of line L3 does not change the stopping rule; the implementation takes the oldest unvisited member, so a run is deterministic. Some descriptions accept a neighbour that no member dominates, which can keep several solutions with the same image. The test of line L5 with weak dominance rejects a second solution with the same image, which keeps the archive at one solution per image.

## Example

The solutions are 3-bit vectors $x$, and the neighbours of $x$ are the three vectors that differ from $x$ in one bit. With $a = (4, 1, 3)$ and $b = (2, 5, 3)$, $f(x) = (\sum_i a_i (1 - x_i), \sum_i b_i x_i)$: the value of the items left out and the weight of the items taken. The start is $x_0 = 010$ with image $(7, 5)$.

| visit | $x$ | $f(x)$ | neighbours and their fate | archive images after the visit |
|---|---|---|---|---|
| 1 | 010 | (7, 5) | 110 (3, 7) added; 000 (8, 0) added; 011 (4, 8) weakly dominated by (3, 7) | (7, 5), (3, 7), (8, 0) |
| 2 | 110 | (3, 7) | 010 (7, 5) in A; 100 (4, 2) added, removes (7, 5); 111 (0, 10) added | (3, 7), (8, 0), (4, 2), (0, 10) |
| 3 | 000 | (8, 0) | 100 in A; 010 (7, 5) and 001 (5, 3) weakly dominated by (4, 2) | unchanged |
| 4 | 100 | (4, 2) | 000 and 110 in A; 101 (1, 5) added, removes (3, 7) | (8, 0), (4, 2), (0, 10), (1, 5) |
| 5 | 111 | (0, 10) | 011 (4, 8) and 110 (3, 7) weakly dominated by (1, 5); 101 in A | unchanged |
| 6 | 101 | (1, 5) | 001 (5, 3) weakly dominated by (4, 2); 111 and 100 in A | unchanged |

All members are visited after 6 passes. The archive images $(8, 0), (4, 2), (1, 5), (0, 10)$ are the whole front of the 8 images; the start $010$ left the archive in visit 2. On the path $a - b - c$ with $f(a) = (1, 1)$, $f(b) = (2, 2)$ and $f(c) = (0, 0)$, the search from $a$ rejects $b$ and stops with $\{a\}$, far from the front $\{(0, 0)\}$.

## Correctness

Line L5 adds only images that no member weakly dominates, and line L6 removes the members they dominate, so the archive stays mutually non-dominated with one solution per image. Once an image is weakly dominated by a member, it stays so, because a member leaves only for a dominator. So each image enters at most once, the loop runs at most $\lvert f(X) \rvert$ times, and the search stops. At the end every member was visited, so every neighbour of every member is weakly dominated by a member; hence no neighbour dominates a member, which makes $A$ a Pareto local optimum set. With a complete neighbourhood the archive is the whole front. If the start is efficient, efficient solutions have distinct images and they form a connected subgraph of the neighbour graph, the archive is the whole efficient set. The full proof is below.

## Complexity

- **One visit, lines L3 to L7.** Finding the oldest unvisited member costs $O(M)$. Each of the $D$ neighbours costs $O(n)$ to build, $c$ to evaluate and $O(p M)$ for lines L5 and L6.
- **Number of visits.** $V$ is at most the number of distinct images in $f(X)$, by the termination proof.

The total is $O(V D (c + n + p M))$ time and $O(M (n + p))$ space. These are exact counts for this implementation, but $V$ and $M$ can be exponential in $n$: with $a_i = b_i = 2^i$ in the example model, $f_1(x) + f_2(x) = \sum_i 2^i$ is the same for all $x$, so no image dominates another, and all $2^n$ images are distinct and Pareto-optimal. On such an instance PLS with the one-bit neighbourhood keeps all $2^n$ solutions.

## Properties

- **Stops on finite spaces.** At most $\lvert f(X) \rvert$ visits; no randomness and no parameters other than the neighbourhood.
- **Archive equals the front of the points seen.** At all times the archive images are the non-dominated images among all evaluated points.
- **Pareto local optimum set at the end.** No neighbour of a member dominates a member, which is the multi-objective analogue of a local optimum of [hill climbing](/hill-climbing/).
- **Whole front under hypotheses.** With a complete neighbourhood, or with an efficient start, distinct efficient images and a connected efficient set, the result is exact. Neither hypothesis holds in general.
- **Order independence of the end test.** The order of line L3 changes the run and can change the final set, but not the property above.

## Variants and improvements

- **Biobjective local search with dynasearch.** Angel, Bampis and Gourvès (2004) explore the neighbourhoods of all archive members at once in each round.
- **Two-phase PLS.** Lust and Teghem (2010) start PLS from the supported solutions found by a [weighted sum](/weighted-sum-method/) method, so the start is already near the front.
- **Bounded archive.** Keep at most a fixed number of members by a grid or crowding rule, as in [PAES](/paes/); the result then is no longer a Pareto local optimum set in general.
- **Iterated and restarted PLS.** Perturb archive members and run PLS again, in the manner of [iterated local search](/iterated-local-search/), to leave Pareto local optimum sets.
- **Anytime PLS.** Dubois-Lacoste, López-Ibáñez and Stützle (2012) studied the order of line L3 and the acceptance rule to improve the archive early in the run.

## When to use it

Use PLS on combinatorial problems with a good single-objective neighbourhood, such as 2-opt for the [traveling salesman problem](/traveling-salesman-problem/) or flips for the [multi-objective knapsack](/multi-objective-knapsack/), when the front is not too large. It is also a final step after a method that finds good start solutions. Paquete, Chiarandini and Stützle reported that PLS with 3-opt on the biobjective traveling salesman problem was competitive with the metaheuristics they compared; that is a measured result on their instances and settings.

## Pitfalls

- **Exponential archives.** The front, and the archive, can have $2^n$ members, as in the complexity section; the run time grows with it.
- **Dominated start.** A start far from the front can stop in a poor Pareto local optimum set, as in the path example.
- **Equal images.** With weak dominance in line L5, a second efficient solution with the same image is dropped, so its neighbours are not explored; Theorem 5 of the proof needs distinct images for this reason.
- **Non-connected efficient sets.** Ehrgott and Klamroth (1997) gave problems whose efficient sets are not connected under natural neighbourhoods; PLS from one efficient start cannot then reach all of them.
- **Removed current solution.** Line L6 can remove the member being visited; the loop must not use the removed entry after the visit.

## Implementations

## History

Local search with a set of non-dominated solutions as its state appears in several earlier multi-objective metaheuristics. Paquete, Chiarandini and Stützle (2004) gave the plain Pareto local search and the notion of a Pareto local optimum set, and Angel, Bampis and Gourvès gave a related method in the same volume. Paquete, Schiavinotto and Stützle (2007) studied the local optimality notions in detail. Lust and Teghem (2010) made PLS the second phase of a two-phase method, and later work studied anytime and parallel forms.

## References
