---
tag: NDHC1V
kind: algorithm
slug: hill-climbing
name: Hill climbing
aliases:
- greedy local search
- steepest ascent
- steepest descent
- iterative improvement
- first-improvement local search
area: optimization/metaheuristics
level: intro
summary: Move to the best improving neighbor until no neighbor is better.
solves: [local-search-problem]
model: word-ram
complexity:
  vars: {k: the number of moves, N: the size of the largest neighborhood, T: the time to evaluate f once, s: the size of one solution}
  time: {worst: O(k N T), best: O(N T)}
  space: {extra: O(s)}
properties: {deterministic: true, recursive: false}
prereqs: [local-search, neighborhood-structure, local-optimum]
see_also: [random-restart-hill-climbing, late-acceptance-hill-climbing, tabu-search, simulated-annealing, iterated-local-search, pls, two-opt, maximum-cut]
sources:
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.1, Iterative Improvement (Revisited), pp. 61 to 70 (best and first improvement, neighborhood evaluation)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 4, Section 4.1 (hill climbing, its variants, and why it gets stuck)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 12, Section 12.4 (Max-Cut by single flips; every local optimum cuts at least half the weight)
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover edition
    locator: Chapter 19, Local Search (neighborhoods, exact neighborhoods, the general local search algorithm)
  - paper: doi:10.1137/0220004
    title: Alejandro A. Schäffer and Mihalis Yannakakis, Simple local search problems that are hard to solve, SIAM Journal on Computing 20(1), 1991
    locator: pp. 56 to 87 (Max-Cut with flips is PLS-complete; exponentially long improving paths)
  - paper: "Matthias Englert, Heiko Röglin and Berthold Vöcking, Worst case and probabilistic analysis of the 2-Opt algorithm for the TSP, Algorithmica 68(1), 2014"
    locator: pp. 190 to 264 (exponential worst case of 2-opt in the Euclidean plane; polynomial smoothed bounds)
  - paper: doi:10.1016/0022-0000(88)90046-3
    title: David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1), 1988
    locator: pp. 79 to 100 (the class PLS)
  - paper: doi:10.1287/opre.6.6.791
    title: G. A. Croes, A method for solving traveling-salesman problems, Operations Research 6(6), 1958
    locator: pp. 791 to 812 (tour improvement by reversing a segment)
  - paper: "Shen Lin, Computer solutions of the traveling salesman problem, Bell System Technical Journal 44(10), 1965"
    locator: pp. 2245 to 2269 (3-opt local search)
---

Hill climbing is the simplest [local search](/local-search/) algorithm: start at a solution, move to a better [neighbor](/neighborhood-structure/) while one exists, and stop at a solution that no neighbor improves. That solution is a [local optimum](/local-optimum/), which is the answer to the [local search problem](/local-search-problem/), but it need not be the best solution overall. Each move strictly improves the objective, so the method always stops on a finite set, but the number of moves can be exponential. Most [metaheuristics](/metaheuristic/) on this site run hill climbing as their inner step and add a rule to leave its local optima.

## In plain words

You stand on a hilly field in thick fog and want to reach low ground. You can only feel the ground one step around you. So you test each step you could take, and you take the step that goes down the most. Then you test again. When no step goes down, you stop.

You are then at the bottom of a hollow. It may be the lowest point of the field, or only a small dip high on a hill. From where you stand you cannot tell the difference. The method is fast and easy to write, and it is the base of many better methods, which add some way to climb out of a small dip.

## The problem

The input is a set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, a [neighborhood](/neighborhood-structure/) $N(x) \subseteq S$ for each $x \in S$, listed in a fixed order, and a start $x_0 \in S$. The output is a local minimum: a solution $x$ with $f(y) \ge f(x)$ for each $y \in N(x)$. To maximize an objective $g$, minimize $f = -g$; "hill climbing" and "steepest ascent" are the names for that direction. This is the [local search problem](/local-search-problem/). We write $f^* = \min_{x \in S} f(x)$ for the global optimum, which the algorithm does not promise to find.

## The algorithm

```pseudo id=main
HILL-CLIMBING(x0, f, N, rule)          ▷ rule is best or first
L1  x ← x0
L2  loop
L3      y* ← none, f* ← f(x)
L4      for each y in N(x), in a fixed order do
L5          if f(y) < f* then
L6              y* ← y, f* ← f(y)
L7              if rule = first then leave the loop of line L4
L8      if y* = none then return x          ▷ no neighbor is better
L9      x ← y*
```

Line L3 sets the bar that a neighbor must pass: the value of the current solution. The loop of line L4 looks at the neighbors. With the rule *best* (steepest descent, also called best improvement), it looks at all of them and keeps the best one; on a tie it keeps the first one, because line L5 uses a strict test. With the rule *first* (first improvement), it takes the first neighbor that is strictly better and stops looking. If no neighbor passes the bar, line L8 returns $x$. Otherwise line L9 moves.

## Example

Take Max-Cut on six vertices $0, \ldots, 5$ with the ten weighted edges $01{:}3$, $02{:}1$, $03{:}2$, $12{:}2$, $14{:}4$, $23{:}3$, $25{:}1$, $34{:}1$, $35{:}2$, $45{:}3$, so the total weight is $W = 22$. A solution is a string $x \in \{0,1\}^6$ that puts vertex $i$ on side $x_i$. To minimize, let $f(x)$ be the *uncut* weight, the total weight of the edges with both ends on one side; then the cut is $W - f(x)$. The neighborhood flips one vertex, in the order $0$ to $5$. Run the rule *best* from $x_0 = 000000$.

| step | $x$ | $f(x)$ | $f$ after flipping vertex 0, 1, 2, 3, 4, 5 | move |
|---|---|---|---|---|
| 0 | 000000 | 22 | 16, 13, 15, 14, 14, 16 | flip 1 |
| 1 | 010000 | 13 | 13, 22, 10, 5, 13, 7 | flip 3 |
| 2 | 010100 | 5 | 9, 14, 8, 13, 7, 3 | flip 5 |
| 3 | 010101 | 3 | 7, 12, 8, 7, 11, 5 | stop |

The run stops after 3 moves at $x = 010101$ with $f = 3$, a cut of 19. A check of all 64 strings shows that 3 is the global minimum, so here hill climbing finds the optimum. The rule *first* from the same start takes 7 moves, through the values 22, 16, 13, 12, 10, 8, 5, 3, and ends at the same string.

From another start it fails. From $x_0 = 001100$ the best flip is vertex 4, which gives $x = 001110$ with $f = 7$. The six flips of $001110$ give 7, 10, 8, 7, 13, 13, none below 7, so the run stops at a local minimum that is not global. Of the 64 start strings, 44 lead the rule *best* to a global minimum with $f = 3$, 12 to a local minimum with $f = 6$ and 8 to one with $f = 7$.

## Correctness

The claim is that hill climbing stops, and that it returns a solution $x \in S$ with $f(y) \ge f(x)$ for each $y \in N(x)$, provided $f$ takes finitely many values on the solutions reachable from $x_0$. The key fact is an invariant of the loop of line L4: $y^*$ is none and no neighbor seen so far is better than $x$, or $y^*$ is a neighbor with $f(y^*) = f^* < f(x)$ and no neighbor seen so far is below $f^*$. So each move strictly lowers $f$, which proves termination, and a return at line L8 happens only after the loop has seen every neighbor, which proves local optimality. The [full proof](proofs/correctness.md) gives the details. The proof says nothing about $f(x) - f^*$: there is no guarantee of global optimality.

## Complexity

One pass of line L2 evaluates $f$ at most $N$ times, where $N$ is the size of the largest neighborhood. With $k$ moves there are $k + 1$ passes, so the time is $O(k N T)$, where $T$ is the time to evaluate $f$ once. In practice $T$ is often replaced by the time of a *delta evaluation*, the change of $f$ caused by a move: for the flip neighborhood of Max-Cut this is the weight of the edges at one vertex, and for [2-opt](/two-opt/) it is four distances. The best case is a start at a local minimum: one pass, $O(N T)$ time.

The number of moves $k$ is the hard part.

- **Upper bound.** Each move strictly lowers $f$, so $k$ is less than the number of distinct values of $f$. With integer values, $k \le f(x_0) - f^*$. For unweighted Max-Cut, $f$ is between 0 and the number of edges, so $k$ is at most the number of edges.
- **Exponential lower bound, artificial objective.** On $\{0,1\}^n$ with the flip neighborhood, there is an objective and a start from which every rule makes $2^{n/2+1} - 2$ moves: the objective decreases along an induced path of the cube (a "snake"), so the only improving neighbor is always the next vertex of the path. The [proof](proofs/complexity.md) builds the path.
- **Exponential lower bound, natural problems.** Schäffer and Yannakakis (1991) gave weighted Max-Cut instances and start cuts from which every sequence of improving flips is exponentially long. Englert, Röglin and Vöcking (2014) gave Euclidean instances of the [traveling salesman problem](/traveling-salesman-problem/) on which 2-opt can make exponentially many moves.
- **Complexity class.** Finding a local optimum of Max-Cut with flips is [PLS](/pls/)-complete (Schäffer and Yannakakis). So a polynomial-time method for it, by hill climbing or by any other means, would give one for every problem in PLS. None is known.

The extra space is one solution $x$, one candidate $y^*$ and the loop state, so $O(s)$ for a solution of size $s$.

## Properties

- **Deterministic.** For a fixed order of the neighbors and a fixed rule, the run is a function of $x_0$. Randomized variants pick a random improving neighbor or a random order.
- **Monotone.** The value $f(x)$ strictly decreases at each move. This is what makes the method stop, and also what traps it.
- **Anytime.** The current solution is always feasible, and it is the best one seen so far. The run can stop at any moment with a usable answer.
- **Local guarantee only.** The output is a local minimum of $N$. Whether it is global depends on the instance, the start and the neighborhood. A neighborhood is *exact* when every local minimum is global; for example the edge-exchange neighborhood of [minimum spanning trees](/minimum-spanning-tree/) is exact (Papadimitriou and Steiglitz, Chapter 19).
- **Quality bounds for some problems.** For Max-Cut with non-negative weights and the flip neighborhood, every local optimum cuts at least half the total weight (Kleinberg and Tardos, Section 12.4). In the example, every local minimum has $f \le 7 \le W/2 = 11$.

## Variants and improvements

- **First improvement versus best improvement.** First improvement makes cheaper steps and often more of them; best improvement makes fewer, more expensive steps. Hoos and Stützle (Section 2.1) discuss when each pays off. Neither dominates.
- **Random improvement.** Move to a random improving neighbor. With a random order of the neighbors, first improvement is of this kind.
- **Sideways moves.** Accept a neighbor of equal value to cross a plateau. Then the strict decrease is lost, and the run needs a bound on the number of such moves to stop.
- **Larger neighborhoods.** A larger neighborhood has fewer local minima but costs more per pass: [2-opt](/two-opt/) versus [3-opt](/three-opt/) and [Lin-Kernighan](/lin-kernighan/) for the TSP, single flips versus the swaps of [Kernighan-Lin](/kernighan-lin/) for graph partitioning. [Large neighborhood search](/large-neighborhood-search/) uses neighborhoods of exponential size searched by an exact method.
- **Restarts and escapes.** [Random-restart hill climbing](/random-restart-hill-climbing/) runs it from many starts. [Iterated local search](/iterated-local-search/), [variable neighborhood search](/variable-neighborhood-search/), [tabu search](/tabu-search/), [guided local search](/guided-local-search/), [late acceptance hill climbing](/late-acceptance-hill-climbing/) and [simulated annealing](/simulated-annealing/) add rules that leave local minima.
- **Continuous version.** On $\mathbb{R}^n$ with a differentiable $f$, the analogue is [gradient descent](/gradient-descent/), with infinitely many neighbors and a step size.

## When to use it

Use hill climbing as the inner step of a metaheuristic, as a fast way to polish a solution from a [greedy](/greedy-algorithm/) construction, or alone when the neighborhood is exact or local optima are known to be good enough. Do not use it alone when you need the optimum of a hard problem: it stops at the first local minimum. For a small instance, exhaustive search or an exact method such as [dynamic programming](/held-karp-algorithm/) for the TSP gives the optimum with a proof.

## Pitfalls

- **A non-strict test.** If line L5 uses $f(y) \le f^*$, then a neighbor of equal value is a move, and two solutions of equal value can swap forever. Keep the strict test $f(y) < f^*$ of line L5, or count the sideways moves and stop after a limit.
- **Stopping the scan early with the rule best.** If line L7 leaves the loop for the rule *best*, the move is not to a best neighbor. Leave the loop only for the rule *first*.
- **Comparing with the old value.** Line L3 must reset $f^*$ to $f(x)$ of the current solution at each pass. If $f^*$ keeps the value of the previous pass, a neighbor no better than $x$ can be taken.
- **Recomputing $f$ from scratch.** A full evaluation of each neighbor costs $T$ each. Use delta evaluation of the move, and check it against a full evaluation in the tests.
- **Calling a local minimum the optimum.** Report the result as a local minimum of the stated neighborhood unless something else proves it is global.

## Implementations

## History

Local improvement by exchanges is old. Croes (1958) improved tours of the traveling salesman problem by the moves now called 2-opt, and Lin (1965) used 3-opt moves. Papadimitriou and Steiglitz (1982, Chapter 19) gave the general form of the local search algorithm and the notion of an exact neighborhood. The name hill climbing comes from artificial intelligence, where the search usually maximizes (Russell and Norvig, Section 4.1). Johnson, Papadimitriou and Yannakakis (1988) defined the class PLS to study how long the search for a local optimum takes, and Schäffer and Yannakakis (1991) proved the exponential lower bounds for Max-Cut.

## References
