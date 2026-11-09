---
tag: 5EJH5P
kind: technique
slug: local-search
name: Local search
aliases:
- iterative improvement
- neighborhood search
- neighbourhood search
area: optimization/metaheuristics
level: intro
summary: Repeatedly move to a better neighboring solution until none exists.
prereqs: [combinatorial-optimization-problem, neighborhood-structure]
see_also: [hill-climbing, local-optimum, neighborhood-structure, two-opt, local-search-problem, pls, metaheuristic, stochastic-local-search]
sources:
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover, 1998
    locator: Chapter 19, Local Search (the general scheme, neighborhoods, exactness, the TSP and k-opt)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Chapter 12, Local Search, and Section 12.4, Maximum-Cut Approximation via Local Search
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.1, Iterative Improvement, pp. 61 to 70 (first and best improvement, incremental evaluation, neighborhood pruning)
  - paper: doi:10.1016/0022-0000(88)90046-3
    title: David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1), 1988
    locator: pp. 79 to 100 (the class PLS)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Section 4.1, Local Search and Optimization Problems
---

Local search is the technique of improving one solution by small changes. It starts from some solution, looks at its neighbors under a [neighborhood structure](/neighborhood-structure/), moves to a better neighbor, and repeats until no neighbor is better. The result is a [local optimum](/local-optimum/). Local search is the base of [2-opt](/two-opt/) for the [traveling salesman problem](/traveling-salesman-problem/), [Kernighan-Lin](/kernighan-lin/) for graph partitioning, [GSAT](/gsat/) for satisfiability and of most [metaheuristics](/metaheuristic/). On a finite set of solutions it always stops, but the number of steps can be exponential, and the local optimum it finds can be far from the global one.

## In plain words

Start with any answer. Look at all the answers that differ from it by one small change. If one of them is better, take it and look again. If none is better, stop.

This is how you might arrange furniture: move one piece at a time, and keep a move only if the room looks better. You will end with a room where no single move helps. That room may still be worse than one you could get by moving two pieces at once.

## When it applies

Local search needs three things:

- a set of solutions, all of which are valid answers, or a way to measure how far an answer is from valid;
- an objective that can be evaluated for each solution, ideally with a fast way to compute the change caused by one move;
- a neighborhood: a small change that turns a solution into another solution.

It is most useful when the problem is [NP-hard](/np-hard/) and an exact method is too slow, when a good solution in little time is enough, and when good solutions tend to be near other good solutions. It also works as the improvement step inside other methods, such as [GRASP](/grasp/), [iterated local search](/iterated-local-search/), [memetic algorithms](/memetic-algorithm/) and [scatter search](/scatter-search/).

## The template

```pseudo id=main
LOCAL-SEARCH(x0, f, N)
L1  x ← x0
L2  loop
L3      Y ← { y ∈ N(x) : f(y) < f(x) }
L4      if Y is empty then return x
L5      x ← an element of Y chosen by the pivoting rule
```

The template minimizes $f$. The *pivoting rule* of line L5 decides which improving neighbor to take. **Best improvement** scans all of $N(x)$ and takes a neighbor with the least $f$; this is [hill climbing](/hill-climbing/) in its steepest form. **First improvement** scans $N(x)$ in some order and takes the first improving neighbor it finds, so a step is cheaper but the search may take more steps.

Three facts hold for every finite set of solutions.

1. **It stops.** Each move strictly lowers $f$, so no solution is visited twice, and the number of moves is less than $|S|$.
2. **The result is a local minimum.** Line L4 returns $x$ only when no neighbor is better.
3. **The number of moves can be exponential.** Johnson, Papadimitriou and Yannakakis defined the class [PLS](/pls/) of problems of finding some local optimum, and for complete problems in it, such as local Max-Cut with single-vertex flips, there are instances and starts from which the standard descent needs exponentially many moves.

With integer objective values, the number of moves is at most $f(x_0) - \min f$, so it is pseudo-polynomial.

## Classic examples

- **[2-opt](/two-opt/) for the TSP.** The neighborhood removes two edges and reconnects the tour; it has $n(n-3)/2$ neighbors, and each change of length is computed in $O(1)$ time. On the 9-city instance of the [iterated local search](/iterated-local-search/) page, from 1000 random tours drawn with seed 9 (Python `random.Random(9)`), best improvement reached the optimum 69 in 449 runs, with 4.0 moves and 136 tour evaluations on average; first improvement, scanning in a fixed order, reached it in 420 runs, with 7.2 moves and 110 evaluations on average. These numbers are for this one instance and say nothing general about the two rules.
- **Max-Cut with single flips.** Move one vertex to the other side while this increases the cut. Every local maximum cuts at least half of the total weight. Kleinberg and Tardos show that a variant which accepts only flips of large enough gain runs in polynomial time and keeps nearly the same guarantee. See [maximum cut](/maximum-cut/).
- **Graph partitioning.** [Kernighan-Lin](/kernighan-lin/) and [Fiduccia-Mattheyses](/fiduccia-mattheyses/) improve a balanced partition by sequences of vertex swaps or moves.
- **Satisfiability.** [GSAT](/gsat/) flips the variable that most increases the number of satisfied clauses; [WalkSAT](/walksat/) adds random moves. For constraint problems such as $n$ queens, the [min-conflicts](/min-conflicts/) heuristic moves one variable to a value with the fewest conflicts.
- **Linear programming.** The simplex method is a local search over the vertices of the feasible region, and for linear programs its neighborhood is exact: a vertex with no better adjacent vertex is optimal.

## Variations

- **Pivoting rules.** Best improvement, first improvement, or a random improving neighbor.
- **Sideways moves.** Allow moves to neighbors of equal value, with a limit, to cross plateaus.
- **Restarts.** Run the search from many starts and keep the best result: [random-restart hill climbing](/random-restart-hill-climbing/), or [GRASP](/grasp/) with greedy randomized starts.
- **Accepting worse moves.** [Simulated annealing](/simulated-annealing/), [late acceptance hill climbing](/late-acceptance-hill-climbing/), [threshold accepting](/threshold-accepting/) and [tabu search](/tabu-search/) sometimes move to a worse neighbor, so they do not stop at the first local optimum.
- **Changing the neighborhood or the objective.** [Variable neighborhood search](/variable-neighborhood-search/) switches neighborhoods; [guided local search](/guided-local-search/) adds penalties to the objective.
- **Perturb and descend.** [Iterated local search](/iterated-local-search/) kicks a local optimum and descends again.
- **Large neighborhoods.** [Large neighborhood search](/large-neighborhood-search/) destroys and repairs a large part of the solution in each move.

## Pitfalls

- **Stopping at the first local optimum and calling it good.** It is good only relative to its neighbors. Report how it compares to a bound, to other runs or to the optimum on small instances.
- **Recomputing the objective from scratch.** A full evaluation of every neighbor makes each step slow. Compute the change caused by each move instead.
- **A neighborhood that cannot reach good solutions.** If some solutions are not reachable from the start by moves, no amount of search finds them. Check that the neighborhood graph is connected, or use restarts.
- **Moves that break feasibility.** Either keep only feasible neighbors, or add a penalty for infeasibility to the objective and make sure the final answer is feasible.
- **Plateaus.** With many equal values, strict improvement stops early. Allow some sideways moves or break ties with a secondary score.

## Exercises

1. Prove that with the single-flip neighborhood for Max-Cut with nonnegative weights, every local maximum cuts at least half of the total weight. Hint: at each vertex, compare the cut and uncut edges, then add over all vertices.
2. Show that the 2-opt neighborhood of a tour of $n \ge 4$ cities has exactly $n(n-3)/2$ distinct neighbors.
3. Give a function on bit strings of length 3 with a local minimum for single flips that is not a local minimum for single and double flips together.
4. Suppose the objective takes integer values between 0 and $M$. Prove that local search stops after at most $M$ moves from any start, whatever the pivoting rule.
5. Show that for the minimum spanning tree problem, the neighborhood "add one edge, remove one edge of the cycle it closes" is exact.

## References
