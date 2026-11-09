---
tag: EZEF0D
kind: algorithm
slug: moea-d
name: MOEA/D
aliases:
- multi-objective evolutionary algorithm based on decomposition
- MOEA based on decomposition
area: optimization/multi-objective
level: advanced
summary: Splits a multi-objective problem into N scalar subproblems with spread weight vectors. Each child of two neighbours replaces the neighbour solutions it does not make worse.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the number of subproblems, T: the neighbourhood size, p: the number of objectives, g: the number of generations, E: the size of the external population, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(N^2 (p + log N) + g N (p T + p E + n + c))}
  space: {extra: O(N T + N n + p E)}
properties: {deterministic: false, iterative: true, population: true, elitist: true}
history:
  year: 2007
  people: [Qingfu Zhang, Hui Li]
  note: Zhang and Li published MOEA/D in the IEEE Transactions on Evolutionary Computation in 2007. Li and Zhang gave MOEA/D-DE in 2009, with a bound on the number of replacements.
prereqs: [scalarization, weighted-tchebycheff-method, genetic-algorithm, ideal-point]
see_also: [nsga-ii, nsga-iii, weighted-sum-method, normal-boundary-intersection, multi-objective-evolutionary-algorithm, spea2, pareto-local-search, achievement-scalarizing-function]
sources:
  - paper: doi:10.1109/TEVC.2007.892759
    title: Qingfu Zhang and Hui Li, MOEA/D, a multiobjective evolutionary algorithm based on decomposition, IEEE Transactions on Evolutionary Computation 11(6), 2007, 712-731
    locator: Section II, the weighted sum, Tchebycheff and boundary intersection decompositions; Section III, the general framework and the cost per generation
  - paper: doi:10.1109/TEVC.2008.925798
    title: Hui Li and Qingfu Zhang, Multiobjective optimization problems with complicated Pareto sets, MOEA/D and NSGA-II, IEEE Transactions on Evolutionary Computation 13(2), 2009, 284-302
    locator: MOEA/D-DE, the parent choice from the whole population with probability 1 - δ and the bound n_r on replacements
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II, the weighted Tchebycheff problem and its relation to Pareto optimality
---

MOEA/D, the multi-objective evolutionary algorithm based on decomposition of Zhang and Li (2007), turns a multi-objective problem into $N$ scalar subproblems, one per weight vector, by a [scalarization](/scalarization/), usually the [weighted Tchebycheff](/weighted-tchebycheff-method/) function. Each subproblem keeps one solution and has a neighbourhood of the $T$ subproblems with the nearest weight vectors. A child made from two neighbours replaces each neighbour solution that it does not make worse, and an external population keeps the non-dominated images found. It has no general guarantee to reach the [Pareto front](/pareto-front/).

## In plain words

MOEA/D fixes many trade-off directions before the run, one for each place in the population. Each place solves its own single-cost problem: how good a candidate is along that direction. Places with close directions are neighbours. Each step, a place takes two candidates from its neighbours and mixes them into a new one. The new candidate then visits the neighbours and takes over every place where it scores at least as well. Neighbours help each other because their problems are close. A separate list keeps every trade-off found so far that nothing else beats.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size (here the number of subproblems), and $y = f(x)$ is the image of $x$.

The input is a search space $X$, the map $f : X \to \mathbb{R}^p$, weight vectors $\lambda^1, \ldots, \lambda^N \ge 0$, the neighbourhood size $T$, a variation and a number $g$ of generations. Subproblem $j$ minimizes $g(x \mid \lambda^j, z) = \max_m \lambda^j_m \lvert f_m(x) - z_m \rvert$, where $z$ is the best value of each objective found so far, an estimate of the [ideal point](/ideal-point/). The output is the external population $E$, the non-dominated images of all points evaluated, and the $N$ subproblem solutions. There is no quality guarantee in general.

## The algorithm

```pseudo id=main
MOEA/D(f, λ^1..λ^N, T, g)
L1  B(i) ← the indices of the T weight vectors nearest to λ^i, for each i
L2  x^i ← a random solution for each i; z_m ← min_i f_m(x^i) for each m; E ← the non-dominated images of the x^i
L3  repeat g times
L4      for i ← 1 to N do
L5          pick k and l at random from B(i); y ← crossover and mutation of x^k and x^l
L6          z_m ← min(z_m, f_m(y)) for each m
L7          for each j ∈ B(i) do
L8              if g(y | λ^j, z) ≤ g(x^j | λ^j, z) then x^j ← y
L9          remove from E the images that f(y) dominates; add f(y) if no image in E weakly dominates it
L10 return E and x^1, …, x^N
```

The weight vectors are usually the simplex lattice: all $\lambda \ge 0$ with $\sum_m \lambda_m = 1$ and coordinates in multiples of $1/h$, which gives $N = \binom{h + p - 1}{p - 1}$. Zhang and Li also allow a repair or local improvement of $y$ after line L5, and the weighted sum or the penalty-based boundary intersection instead of the Tchebycheff function.

## Example

Let $p = 2$, $N = 5$, $T = 3$, with $\lambda^1, \ldots, \lambda^5 = (0, 1), (\tfrac14, \tfrac34), (\tfrac12, \tfrac12), (\tfrac34, \tfrac14), (1, 0)$. Then $B(3) = \{2, 3, 4\}$. The solutions have images $(1, 10), (2, 9), (5, 5), (8, 2), (10, 1)$, so $z = (1, 1)$. For $i = 3$, the child has image $f(y) = (3, 6)$, and $z$ stays $(1, 1)$.

| $j$ | $\lambda^j$ | $g$ of the old $x^j$ | $g$ of $y$ | line L8 |
|---|---|---|---|---|
| 2 | (1/4, 3/4) | $\max(1/4, 6) = 6$ | $\max(1/2, 15/4) = 15/4$ | replace |
| 3 | (1/2, 1/2) | $\max(2, 2) = 2$ | $\max(1, 5/2) = 5/2$ | keep |
| 4 | (3/4, 1/4) | $\max(21/4, 1/4) = 21/4$ | $\max(3/2, 5/4) = 3/2$ | replace |

The child does not dominate $(2, 9)$ or $(8, 2)$, but it replaces both, so subproblems 2 and 4 now hold the same solution. No image of $E$ dominates $(3, 6)$, so line L9 adds it.

## Correctness

MOEA/D has no guarantee to reach the front of a general problem; the proof covers the update rules. $z$ is always the best value of each objective seen, so $z \le f(x)$ for every evaluated $x$. Line L8 replaces only when the child is no worse for subproblem $j$ at the current $z$. If $f(y)$ weakly dominates $f(x^j)$, then each term $\lambda^j_m (f_m(y) - z_m)$ is at most the matching term for $x^j$, so the child replaces $x^j$. The external population is exactly the set of non-dominated images of all points evaluated, by the same induction as for an elitist archive. The full proof is below.

## Complexity

- **Setup, lines L1 and L2.** $O(p N^2)$ for the distances between weight vectors and $O(N^2 \log N)$ to sort them, plus $N$ evaluations.
- **One child, lines L5 to L9.** $O(n)$ for the variation, one evaluation at cost $c$, $O(p)$ for $z$, $O(p T)$ for the $T$ comparisons and $O(p E)$ for the external population.

The total is $O(N^2 (p + \log N) + g N (p T + p E + n + c))$ time and $O(N T + N n + p E)$ space. Zhang and Li give $O(p N T)$ per generation for the work outside variation, evaluation and the external population, against $O(p N^2)$ for the sort of [NSGA-II](/nsga-ii/). $E$ can grow without bound; a bounded external population changes the last term.

## Properties

- **Decomposition.** Each solution belongs to a scalar subproblem, and selection compares only scalar values.
- **Replacement is monotone at fixed $z$.** A subproblem value never grows by line L8, but it can grow when $z$ moves.
- **Dominance is respected.** A child replaces every neighbour solution that it weakly dominates.
- **Tchebycheff reaches non-convex parts.** For each Pareto-optimal point there is a weight vector for which it minimizes the Tchebycheff function with a utopian $z$, unlike the [weighted sum](/weighted-sum-method/), which reaches only the supported points.
- **Scale.** The Tchebycheff values depend on the scale of each objective; Zhang and Li normalize the objectives when their ranges differ.

## Variants and improvements

- **MOEA/D-DE.** Li and Zhang (2009) pick parents from the whole population with probability $1 - \delta$, use differential evolution, and replace at most $n_r$ neighbours per child, which limits the loss of diversity in the example.
- **Other decompositions.** The weighted sum, the penalty-based boundary intersection of Zhang and Li, or the [achievement scalarizing function](/achievement-scalarizing-function/).
- **Weight vectors.** The simplex lattice, as in [NSGA-III](/nsga-iii/) and [normal-boundary intersection](/normal-boundary-intersection/), or adaptive weights for fronts that miss part of the simplex.
- **Resource allocation.** Spend more children on subproblems whose values improved most recently.

## When to use it

Use MOEA/D when a scalarization fits the problem, when each subproblem can use a single-objective operator or local search, and when the cost per generation matters. It is also a common choice for many objectives. Zhang and Li reported comparisons with MOGLS and NSGA-II on multi-objective knapsack and continuous test problems; these are measured results on those instances, budgets and settings.

## Pitfalls

- **Copies.** One child can replace up to $T$ neighbours, as in the example, so many subproblems can hold the same solution; bound the replacements.
- **The direction of a weight.** The Tchebycheff optimum of $\lambda$ lies on the ray from $z$ along $(1/\lambda_1, \ldots, 1/\lambda_p)$, not along $\lambda$. Evenly spread weights do not give evenly spread points.
- **Zero weights.** A zero coordinate makes the subproblem ignore that objective, so its optimum can be weakly Pareto-optimal only.
- **Moving reference point.** Subproblem values are not comparable across generations when $z$ changes.
- **Unbounded external population.** On continuous problems $E$ can grow at every step; bound it or keep only the subproblem solutions.

## Implementations

## History

Decomposition into scalar subproblems is old in multi-objective optimization, in the weighted sum, the Tchebycheff method and [normal-boundary intersection](/normal-boundary-intersection/). Earlier evolutionary methods, such as the multi-objective genetic local search of Ishibuchi and Murata and of Jaszkiewicz, used random weights per step. Zhang and Li (2007) fixed one weight vector per solution and let neighbours share children. Li and Zhang (2009) gave MOEA/D-DE for complicated Pareto sets.

## References
