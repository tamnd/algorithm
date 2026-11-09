---
tag: 0JTKYZ
kind: algorithm
slug: guided-local-search
name: Guided local search
aliases:
- GLS
area: optimization/metaheuristics
level: advanced
summary: Local search that penalizes features of local optima to push the search out of them.
model: word-ram
complexity:
  vars: {K: the number of iterations, H: the time of one run of the local search, m: the number of features of one solution, s: the size of one solution, F: the number of features in all}
  time: {worst: O((K + 1) H + K m)}
  space: {extra: O(s + F)}
properties: {deterministic: true, recursive: false}
prereqs: [local-search, hill-climbing, local-optimum, neighborhood-structure]
see_also: [tabu-search, tabu-list, iterated-local-search, two-opt, traveling-salesman-problem, fitness-landscape, intensification-and-diversification, walksat]
sources:
  - paper: doi:10.1016/S0377-2217(98)00099-X
    title: Christos Voudouris and Edward Tsang, Guided local search and its application to the traveling salesman problem, European Journal of Operational Research 113(2), 1999
    locator: pp. 469 to 499 (features, costs, penalties, utilities, the augmented objective, the parameter a, fast local search)
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.2, 'Simple' SLS Methods, from p. 71 (dynamic local search and guided local search), and Section 6.4, Dynamic Local Search Algorithms for SAT, from p. 284
---

Guided local search (GLS) is a [local search](/local-search/) that changes the objective it descends when it gets stuck. Each solution has *features*, such as the edges of a tour, and each feature has a cost. When the search reaches a [local minimum](/local-optimum/), GLS adds a penalty to the features of that solution that are most costly and least penalized so far. The local search then minimizes the original objective plus the penalties, so the local minimum it was stuck in no longer looks good, and the search moves on. Voudouris and Tsang developed the method in the 1990s and applied it to the [traveling salesman problem](/traveling-salesman-problem/). GLS is deterministic for a deterministic local search, and it has no guarantee of reaching a global optimum.

## In plain words

A walker reaches the bottom of a hollow and cannot go lower. Guided local search fills that hollow with some sand, so the bottom is now higher, and the walker can walk out to a nearby lower spot.

It does not fill the whole hollow at random. It looks at what makes the current solution bad, for example the longest road in a tour, and it marks that road. A marked road counts as longer from now on. A road that has been marked many times is marked less eagerly, so the marks spread over many bad roads. The walker always remembers the best tour it saw by the true lengths, without the marks.

## The problem

The input is a finite set $S$ of solutions, an objective $g : S \to \mathbb{R}$ to minimize, a set of features, with $F(x)$ the features present in solution $x$ and a cost $c_e \ge 0$ for each feature $e$, a local search procedure for a [neighborhood](/neighborhood-structure/) $N$, a start $x_0$, a parameter $a > 0$ and a number of iterations $K$. For the TSP, the features are the edges, $c_e$ is the length of edge $e$, and $F(x)$ is the set of $n$ edges of tour $x$. The output is the best solution found by $g$. The aim is a global minimum, which GLS cannot prove it has found.

## The algorithm

```pseudo id=main
GUIDED-LOCAL-SEARCH(x0, g, F, c, LOCAL-SEARCH, a, K)
L1  p_e ← 0 for every feature e;  x ← LOCAL-SEARCH(x0, g);  b ← x
L2  λ ← a · g(x) / |F(x)|
L3  for k ← 1 to K do
L4      u_e ← c_e / (1 + p_e) for every feature e in F(x)        ▷ utility
L5      p_e ← p_e + 1 for every e in F(x) with the largest u_e
L6      x ← LOCAL-SEARCH(x, h), where h(y) = g(y) + λ · Σ_{e ∈ F(y)} p_e
L7      if g(x) < g(b) then b ← x
L8  return b
```

Line L1 runs a plain descent on $g$. Line L2 sets the weight $\lambda$ of the penalties on the scale of the objective: $g(x)/|F(x)|$ is the average cost of one feature of the first local minimum. Line L4 computes the *utility* of penalizing each feature of the current local minimum: high for a costly feature, lower for a feature already penalized often. Line L5 adds one penalty point to the features of largest utility. Line L6 descends on the *augmented objective* $h$. Line L7 keeps the best solution by the true objective $g$.

## Example

Take the nine cities of the [iterated local search](/iterated-local-search/) page, at $(17,2)$, $(11,19)$, $(19,9)$, $(2,16)$, $(11,12)$, $(13,0)$, $(1,3)$, $(14,20)$ and $(7,11)$, numbered 0 to 8, with distances rounded to the nearest integer. The local search is best-improvement [2-opt](/two-opt/), and $a = 1/5$. Line L1 descends from the tour $0, 1, \ldots, 8$ to the 2-opt local minimum 0 2 4 8 7 1 3 6 5 of length 72, with edges of lengths

| edge | 0-2 | 2-4 | 4-8 | 8-7 | 7-1 | 1-3 | 3-6 | 6-5 | 5-0 |
|---|---|---|---|---|---|---|---|---|---|
| length | 7 | 9 | 4 | 11 | 3 | 9 | 13 | 12 | 4 |

so $\lambda = (1/5) \cdot 72 / 9 = 1.6$. The run goes as follows.

| $k$ | utilities of the top features | penalized | new $x$ | $g(x)$ | $h(x)$ |
|---|---|---|---|---|---|
| 1 | 3-6: 13, 6-5: 12, 8-7: 11 | 3-6 | 0 2 4 8 7 1 3 6 5 | 72 | 73.6 |
| 2 | 6-5: 12, 8-7: 11, 2-4: 9 | 6-5 | 0 2 4 8 7 1 3 6 5 | 72 | 75.2 |
| 3 | 8-7: 11, 2-4: 9, 1-3: 9 | 8-7 | 0 2 7 1 4 8 3 6 5 | 69 | 72.2 |

In iteration 1 the longest edge 3-6 gets a penalty, but no 2-opt move pays for it, and the descent stays. In iteration 2 the utility of 3-6 has dropped to $13/2$, so 6-5 is penalized. In iteration 3 the edge 8-7 is penalized; now 2-opt moves that remove 8-7 become better under $h$, and the descent reaches the tour 0 2 7 1 4 8 3 6 5 of length 69, which is the optimum by enumeration. This tour still uses the penalized edges 3-6 and 6-5, so $h = 69 + 1.6 \cdot 2 = 72.2$.

## Correctness

GLS has no optimality guarantee, so "correct" means the following. Each descent stops, since the penalties do not change during a descent. The result is the best solution by $g$ among the local minima found. Penalties never decrease, and each iteration adds one point to exactly the features of largest utility.

One result explains why the penalties work. If all costs are positive and $\lambda > 0$, GLS cannot stay at the same solution for ever: while it stays, every feature of that solution is penalized again and again, the penalties of the solution's own features grow without bound, and a neighbor that drops one of these features becomes better under $h$. This does not prevent cycles among several solutions, and it says nothing about global optimality. The [full proof](proofs/correctness.md) gives all steps.

## Complexity

The time is $O((K + 1) H + K m)$, where $H$ bounds one run of the local search and $m$ is the number of features of one solution: lines L4 and L5 cost $O(m)$. For the TSP with edge features, $m = n$, and the change of $h$ for a 2-opt move needs the penalties of the four edges involved, so it costs $O(1)$ like the change of $g$. The extra space is $O(s + F)$: the solutions and one penalty per feature, which for the TSP is a table of $n^2$ counters, or a hash table of the penalized edges only.

## Properties

- **Deterministic.** With a deterministic local search, GLS is a function of the start and $a$.
- **The objective changes, not the move rule.** The local search is the same plain descent. GLS only changes what it descends.
- **Memory over features.** Penalties are a long-term memory of which features appeared in local minima, weighted by their cost. Compare the [tabu list](/tabu-list/), a short-term memory that forbids moves.
- **Self-limiting.** The utility $c_e / (1 + p_e)$ falls each time $e$ is penalized, so penalties spread over several costly features.
- **One main parameter.** The weight $a$; $\lambda$ follows from it.

## Variants and improvements

- **Fast local search.** Voudouris and Tsang pair GLS with a local search that keeps an activation bit for each sub-neighborhood and scans only the active ones; after a penalty, only the parts of the solution near the penalized features are made active.
- **Dynamic local search.** Hoos and Stützle group GLS with other methods that change the weights of an evaluation function during the search, such as clause weighting for SAT, where each unsatisfied clause gets more weight at a local minimum. [WalkSAT](/walksat/) itself uses random noise, not weights.
- **Penalties on top of other searches.** The penalty scheme does not depend on the descent, so it can be placed on top of any local search that accepts a changed objective, such as 2-opt, 3-opt or a flip search.

## When to use it

Use GLS when a solution has natural costly features, as edges in a tour, assignments in a scheduling problem or violated constraints in a constraint problem, and a fast local search already exists. It adds little code to a descent and keeps it deterministic. On the 10-city instance of the [late acceptance](/late-acceptance-hill-climbing/) page (optimum 231), GLS with 2-opt and $a = 1/5$ from the tour $0, 1, \ldots, 9$ reached the optimum within 20 iterations; this one case shows only that the code works.

## Pitfalls

- **Reporting by $h$.** The augmented objective is a tool. Compare and report solutions by $g$, as in line L7.
- **A weight on the wrong scale.** If $\lambda$ is much larger than the costs, one penalty dominates $g$ and the descent wanders; if it is tiny, many iterations pass before a penalty has any effect. Setting $\lambda$ from $g(x)/|F(x)|$ ties it to the scale of the instance.
- **Penalizing all features.** Penalizing every feature of the local minimum raises $h$ evenly, and the relative order of nearby solutions hardly changes. The utility rule penalizes only the worst ones.
- **Missing the best solution inside a descent.** Line L7 checks only the end of each descent. A descent on $h$ can pass through a solution with a lower $g$; a careful code checks $g$ at each move.

## Implementations

## History

Voudouris and Tsang developed guided local search from GENET, a neural network method for constraint satisfaction by Tsang and coworkers, and published the method with its application to the TSP in 1999. Hoos and Stützle treat it as an instance of dynamic local search.

## References
