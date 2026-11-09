---
tag: 32WWG5
kind: technique
slug: large-neighborhood-search
name: Large neighborhood search
aliases:
- LNS
- destroy and repair
- ruin and recreate
area: optimization/combinatorial-optimization
level: advanced
summary: Local search whose moves destroy and exactly repair a large part of the solution.
prereqs: [local-search, neighborhood-structure, local-optimum, metaheuristic]
see_also: [local-search, vehicle-routing-problem, relaxation-induced-neighborhood-search, local-branching, constraint-programming, iterated-local-search, simulated-annealing, lin-kernighan]
sources:
  - paper: "Paul Shaw, Using constraint programming and local search methods to solve vehicle routing problems, in Principles and Practice of Constraint Programming (CP 98), Lecture Notes in Computer Science 1520, Springer, 1998, 417 to 431"
    locator: the destroy and repair scheme with related removal and repair by constraint programming
  - paper: doi:10.1287/trsc.1050.0135
    title: Stefan Ropke and David Pisinger, An adaptive large neighborhood search heuristic for the pickup and delivery problem with time windows, Transportation Science 40(4), 455 to 472, 2006
    locator: adaptive weights for several destroy and repair methods, and the simulated annealing acceptance
  - paper: "David Pisinger and Stefan Ropke, Large neighborhood search, in Handbook of Metaheuristics, second edition, Springer, 2010, Chapter 13"
    locator: the survey of the method, its variants and its applications
  - paper: doi:10.1016/S0166-218X(01)00338-9
    title: Ravindra K. Ahuja, Özlem Ergun, James B. Orlin and Abraham P. Punnen, A survey of very large-scale neighborhood search techniques, Discrete Applied Mathematics 123, 75 to 102, 2002
    locator: neighborhoods of exponential size searched by network flows, dynamic programming and ejection chains
  - paper: doi:10.1007/s10107-004-0518-7
    title: Emilie Danna, Edward Rothberg and Claude Le Pape, Exploring relaxation induced neighborhoods to improve MIP solutions, Mathematical Programming 102(1), 71 to 90, 2005
    locator: the RINS neighborhood, which fixes the variables where the incumbent and the LP solution agree
---

Large neighborhood search (LNS) is a [local search](/local-search/) technique in which each move *destroys* a large part of the current solution, for example by removing a group of related customers from the routes, and then *repairs* it into a new complete solution with a strong method: an exact solver such as [constraint programming](/constraint-programming/) or a MIP solver, or a good constructive heuristic. The neighborhood of a solution is the set of all solutions that the repair can reach, which is usually exponentially large, so the search is never examined element by element. Paul Shaw introduced the method in 1998 for [vehicle routing](/vehicle-routing-problem/), and Ropke and Pisinger (2006) made it adaptive (ALNS) with several destroy and repair methods chosen by their past success. LNS is a heuristic: it has no general bound on solution quality or on the number of steps. For some problems, local optima of large exchange neighborhoods have proved approximation ratios.

## In plain words

You have a good plan, but small changes no longer improve it. Instead of changing one thing at a time, tear out a sizable piece of the plan, such as all the stops in one part of town. Then rebuild that piece as well as you can while keeping the rest fixed. If the new plan is better, keep it.

Repeat with a different piece each time. Each rebuild looks at a huge number of possible changes at once, so the method escapes traps that small steps cannot leave. The size of the piece matters: too small and nothing changes, too large and the rebuild becomes slow or poor.

## When it applies

- **A strong repair method exists for partial solutions.** The problem stays hard, but fixing most of the solution makes the rest small enough for an exact solver, or structured enough for a good heuristic. Constraint programming, MIP solvers, dynamic programming and insertion heuristics are typical.
- **Tightly constrained problems.** In problems with time windows, capacities or precedence rules, small moves are often infeasible, while a repair method can rebuild a feasible solution around the constraints. This is why LNS is strong for [vehicle routing](/vehicle-routing-problem/) and scheduling.
- **A meaningful "part" of a solution.** Related elements can be removed together: customers that are close or have similar time windows, jobs on one machine, or variables in one block of a model.
- **Not the best choice** when cheap small moves are already very effective and can be evaluated in constant time, as with [2-opt](/two-opt/) and [Lin-Kernighan](/lin-kernighan/) for the plain TSP, unless LNS is used on top of them.

## The template

```pseudo id=main
LARGE-NEIGHBORHOOD-SEARCH(x0)
L1  x ← x0;  best ← x0
L2  repeat until a time or iteration limit
L3      choose a destroy method d and a repair method r      ▷ fixed, random or adaptive
L4      y ← d(x)                    ▷ remove or free a part of x, for example q related elements
L5      x' ← r(y)                   ▷ rebuild a complete feasible solution, exactly or heuristically
L6      if accept(x', x) then x ← x'            ▷ only improvements, or a simulated annealing rule
L7      if cost(x') < cost(best) then best ← x'
L8      update the scores of d and r            ▷ only in adaptive LNS
L9  return best
```

The *neighborhood* of $x$ is the set of all solutions $r(d(x))$ over the possible destroy choices. If the repair is exact, the move finds the best solution that agrees with $x$ outside the destroyed part. With $q$ elements destroyed out of $n$, there are $\binom{n}{q}$ possible parts, and each part leaves a subproblem with many completions, so the neighborhood is much larger than the polynomial neighborhoods of classical local search.

**Measured example.** For the Euclidean [traveling salesman problem](/traveling-salesman-problem/) with 40 cities placed uniformly in the unit square, 30 instances from seed 2026, an LNS run started from the [nearest neighbor](/nearest-neighbor-heuristic/) tour. Each move removed a random city together with its 5 nearest neighbors (6 cities in all), reinserted them by regret-2 [cheapest insertion](/cheapest-insertion/), and kept the result only if shorter. After 600 moves, its tours averaged 0.974 times the length of a [2-opt](/two-opt/) local optimum from the same start (range 0.899 to 1.028), and were shorter in 24 of the 30 instances. Applying 2-opt to the LNS tour gave a mean ratio of 0.966, shorter in 28 of 30. These numbers are measured on this one setting, not proved, and they depend on the destroy size, the repair method and the time spent.

## Classic examples

- **[Vehicle routing](/vehicle-routing-problem/).** Shaw (1998) removed related customers and reinserted them with constraint programming and limited discrepancy search. Ropke and Pisinger (2006) used several removal heuristics (random, worst cost, related) and insertion heuristics (greedy, regret) with adaptive weights, and found many new best solutions for pickup and delivery problems with time windows. Routes from [Clarke-Wright savings](/clarke-wright-savings/) are a common start.
- **[RINS](/relaxation-induced-neighborhood-search/) in MIP solvers.** Fix the integer variables where the incumbent and the LP solution agree, and solve the remaining sub-MIP. The MIP solver is the repair method.
- **[Local branching](/local-branching/).** Add the constraint that at most $k$ binary variables differ from the incumbent, and solve the resulting MIP. This is an LNS whose neighborhood is a Hamming ball, searched exactly.
- **[Job shop scheduling](/job-shop-scheduling/).** Free the order of the operations in a time window or on a few machines, and reoptimize it with constraint programming, keeping the rest of the schedule fixed.
- **Very large-scale neighborhoods.** Ejection chains and variable-depth moves, as in [Lin-Kernighan](/lin-kernighan/), cyclic exchanges among routes or clusters, found by negative cycle search, and dynasearch, which applies sets of independent swaps found by dynamic programming. Ahuja, Ergun, Orlin and Punnen (2002) surveyed these neighborhoods of exponential size that are searched in polynomial time.

## Variations

- **Adaptive LNS (ALNS).** Keep several destroy and repair methods, and choose them at random with weights that grow when a method finds improvements.
- **Acceptance rules.** Accept only improvements, use a [simulated annealing](/simulated-annealing/) rule as in ALNS, or use record-to-record travel or threshold acceptance.
- **Destroy size schedules.** Start with small parts and grow $q$ when the search stagnates, in the spirit of [variable neighborhood search](/variable-neighborhood-search/).
- **Ruin and recreate.** The same scheme, introduced independently by Schrimpf, Schneider, Stamm-Wilbrandt and Dueck (2000).
- **Relation to other methods.** [Iterated local search](/iterated-local-search/) perturbs a solution and then improves it by local search; LNS replaces both steps by one destroy and repair. Population methods such as [genetic algorithms](/genetic-algorithm/) can use LNS as their improvement step.
- **Proved ratios for exchange neighborhoods.** For some problems, local optima of neighborhoods that change up to $p$ elements at once have approximation guarantees. For example, local search for the [$k$-median problem](/k-median-problem/) with $p$ simultaneous swaps reaches a ratio of $3 + 2/p$ (Arya and others, 2004), and similar results hold for [set packing](/set-packing/). These bounds are for local optima, not for the time needed to reach them, which can be exponential ([PLS](/pls/)).

## Pitfalls

- **Wrong destroy size.** If $q$ is too small, the repair often rebuilds the same solution. If it is too large, the repair is slow, and a heuristic repair approaches a random restart.
- **Unrelated removal.** Removing random elements that do not interact often leaves the repair no real choice, since each element goes back where it was. Related removal, by distance, time or shared resources, gives more useful moves.
- **Weak repair.** The quality of LNS is mostly the quality of its repair. A repair that only inserts greedily can be weaker than a good small-move local search with the same time.
- **Exact repair without limits.** An exact repair on a subproblem that is still large can take as long as the full problem. Use time or node limits, and treat the result as a heuristic repair.
- **Stagnation with greedy acceptance.** Accepting only improvements makes the search stop at a local optimum of the large neighborhood. Use a randomized acceptance rule or restarts.
- **Reporting.** Results depend on the seed, the time limit and the instance set. Report measured results as measured, with the settings and the number of runs.

## References
