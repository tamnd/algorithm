---
tag: CZF1BY
kind: problem
slug: local-search-problem
name: Local search problem
aliases:
- local optimisation
- local optimization
area: techniques/search-strategies
level: core
summary: Given a neighbourhood structure and an objective, find a solution that is no worse than all its neighbours.
prereqs: [local-optimum, hill-climbing]
see_also: [pls, hill-climbing, simulated-annealing, tabu-search, two-opt, maximum-cut, kernighan-lin, tfnp]
sources:
  - paper: doi:10.1016/0022-0000(88)90046-3
    title: David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1) (1988)
    locator: pp. 79 to 100 (the class PLS, PLS reductions, the PLS-completeness of Circuit Flip and of the Kernighan-Lin neighbourhood for graph partitioning, and the result that a PLS problem is not NP-hard unless NP = co-NP)
  - paper: doi:10.1137/0220004
    title: Alejandro A. Schäffer and Mihalis Yannakakis, Simple local search problems that are hard to solve, SIAM Journal on Computing 20(1) (1991)
    locator: pp. 56 to 87 (the PLS-completeness of Max-Cut with the flip neighbourhood and of stable configurations of Hopfield networks, tight PLS reductions, and the exponential running time of the standard algorithm)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 12 (local search; Section 12.3 on Hopfield networks, Section 12.4 on Max-Cut by local search with the bound of one half)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 4, Section 4.1 (local search and optimization problems, hill climbing, simulated annealing, local beam search)
---

A local search problem gives a set of solutions, an objective to maximize or minimize, and for each solution a set of neighbours, and it asks for a *local optimum*: a solution that no neighbour improves. It is the problem that [hill climbing](/hill-climbing/) and its relatives solve. A local optimum always exists on a finite set, and the standard algorithm, "move to a better neighbour while one exists", always finds one, but it can take exponentially many steps. Johnson, Papadimitriou and Yannakakis (1988) defined the class [PLS](/pls/) of these problems, and for many natural ones, such as Max-Cut with single flips, no polynomial-time algorithm is known.

## In plain words

You stand somewhere on a hilly field in thick fog and want to stand high. You can only see the ground one step around you. A local search problem asks for a spot from which every single step goes down or stays level. Such a spot is a local top. It need not be the highest point of the field.

You can always find a local top by walking uphill until no step goes up. The question is how long the walk takes. On some fields the uphill walk winds around for a very long time, and nobody knows a shortcut that always works.

## Definition

A local search problem $\Pi$ for maximization consists of a set of instances and, for each instance $I$:

- a finite set $F(I)$ of feasible solutions;
- an objective $c_I : F(I) \to \mathbb{Z}$;
- a neighbourhood $N_I(x) \subseteq F(I)$ for each $x \in F(I)$.

**Task.** Given $I$, output a solution $x \in F(I)$ that is *locally optimal*: $c_I(y) \le c_I(x)$ for each $y \in N_I(x)$. For minimization, reverse the inequality.

A solution always exists, because a solution of the largest objective value is locally optimal. So the task is a total search problem.

**The class PLS (polynomial local search).** Johnson, Papadimitriou and Yannakakis require three polynomial-time algorithms: one that gives some initial solution in $F(I)$, one that computes $c_I(x)$, and one that, given $x$, either returns a neighbour $y$ with $c_I(y) > c_I(x)$ or reports that $x$ is locally optimal. The solutions have length polynomial in the length of $I$. PLS is the class of these problems, and it is a subclass of [TFNP](/tfnp/).

## Variants

- **Maximization or minimization.** The two are the same up to the sign of $c$.
- **Pivoting rule.** The problem asks only for some local optimum. An algorithm still chooses which better neighbour to move to: the first one found (first improvement), the best one (steepest ascent), or a random one.
- **The standard-algorithm problem.** Given also a start solution, find the local optimum that the standard algorithm with a fixed pivoting rule reaches from it. This is harder: for the tight PLS-complete problems it is PSPACE-complete (Schäffer and Yannakakis).
- **Approximate local optima.** Ask for $x$ such that no neighbour is better by more than a factor $1 + \epsilon$. These can often be found in polynomial time.
- **Continuous local search.** The solutions form a continuous domain and the moves are small steps, as in [gradient descent](/gradient-descent/).

## Examples

- **Max-Cut with the flip neighbourhood.** A solution is a split of the vertices of a weighted graph into two sides, the objective is the total weight of the edges that cross the split, and the neighbours of a split are the splits that move one vertex to the other side.
- **TSP with the 2-opt neighbourhood.** A solution is a tour, and the neighbours are the tours obtained by removing two edges and reconnecting the two paths the other way, see [2-opt](/two-opt/).
- **Graph partitioning with the Kernighan-Lin neighbourhood.** Split the vertices into two equal halves with few edges between them, with the moves of the [Kernighan-Lin](/kernighan-lin/) heuristic.
- **Satisfiability with the flip neighbourhood.** Maximize the number of satisfied clauses, where a neighbour changes one variable, as in [WalkSAT](/walksat/).
- **Pure Nash equilibria of potential games.** In a congestion game, a profile where no player gains by changing strategy is a local optimum of the potential function under single-player moves. This is a [Nash equilibrium](/nash-equilibrium/).

**A worked instance.** The graph has the vertices $a, b, c, d, e$ and the six edges $ab$, $ad$, $bd$, $be$, $ce$, $de$, each of weight 1. Start with all vertices on one side, and flip the first vertex, in the order $a$ to $e$, whose move raises the cut.

| step | moved | side of $a, b, c, d, e$ | cut |
| --- | --- | --- | --- |
| 0 | none | 0, 0, 0, 0, 0 | 0 |
| 1 | $a$ | 1, 0, 0, 0, 0 | 2 |
| 2 | $b$ | 1, 1, 0, 0, 0 | 3 |
| 3 | $c$ | 1, 1, 1, 0, 0 | 4 |

Now no single move raises the cut. Moving $a$ leaves it at 4, and moving $b$, $c$, $d$ or $e$ lowers it to 3. So the split $\{a, b, c\}$, $\{d, e\}$ is a local optimum with cut 4. It is not a global optimum: the split $\{a, e\}$, $\{b, c, d\}$ cuts every edge except $bd$, so its cut is 5, the maximum.

## Known algorithms

- **The standard algorithm**, also called iterative improvement or [hill climbing](/hill-climbing/): start from the initial solution, and move to a better neighbour while one exists. It is correct for every problem in PLS, and its number of steps is at most the number of distinct objective values. If the objective takes only polynomially many values, as in unweighted Max-Cut where the cut is between 0 and $m$, it runs in polynomial time.
- **Variants of the standard algorithm.** Steepest ascent, random improvement, and the use of larger neighbourhoods such as [3-opt](/three-opt/) or [Lin-Kernighan](/lin-kernighan/) for the TSP.
- **Methods that leave local optima.** [Simulated annealing](/simulated-annealing/), [tabu search](/tabu-search/), [random-restart hill climbing](/random-restart-hill-climbing/), [stochastic local search](/stochastic-local-search/) and [genetic algorithms](/genetic-algorithm/) aim at good solutions of the optimization problem, not only at a local optimum.

## Bounds

- **Existence and membership.** Each problem in PLS has a solution, and a claimed solution can be checked in polynomial time, with one call of the improvement algorithm. So PLS lies in TFNP (Johnson, Papadimitriou and Yannakakis).
- **Not NP-hard unless NP = co-NP.** Johnson, Papadimitriou and Yannakakis showed that if a problem in PLS is NP-hard, then NP = co-NP. So local search problems are believed to be easier than NP-hard optimization problems.
- **Polynomial-time solution is open.** No polynomial-time algorithm is known for the PLS-complete problems. Such an algorithm would solve every problem in PLS in polynomial time.
- **The standard algorithm can be exponential.** For Max-Cut with the flip neighbourhood and integer weights, Schäffer and Yannakakis gave instances and start splits from which every sequence of improving flips is exponentially long. So no pivoting rule makes the standard algorithm polynomial on this problem.
- **Quality of local optima.** For Max-Cut with non-negative weights, each flip-local optimum cuts at least half of the total weight $W$. At a local optimum, each vertex $v$ has at least half of the weight of its edges crossing the cut, or moving $v$ would raise the cut. Summing over the vertices counts each edge twice, so the cut has weight at least $W/2$ (Kleinberg and Tardos, Section 12.4). In the example above, $m/2 = 3 \le 4$.

## Reductions

A *PLS reduction* from $\Pi_1$ to $\Pi_2$ is a pair of polynomial-time maps: $f$ maps an instance $I$ of $\Pi_1$ to an instance $f(I)$ of $\Pi_2$, and $g$ maps each local optimum of $f(I)$ back to a local optimum of $I$. A problem is PLS-complete if every problem in PLS reduces to it.

- **Circuit Flip** is PLS-complete: given a Boolean circuit, find an input whose output, read as a number, is not improved by flipping one input bit (Johnson, Papadimitriou and Yannakakis).
- **Graph partitioning** with the Kernighan-Lin neighbourhood is PLS-complete (Johnson, Papadimitriou and Yannakakis).
- **Max-Cut with the flip neighbourhood**, and the stable configurations of Hopfield neural networks, are PLS-complete (Schäffer and Yannakakis). Their reductions are *tight*, so the exponential running time and the PSPACE-completeness of the standard-algorithm problem carry over from Circuit Flip.
- **Pure Nash equilibria of congestion games** are PLS-complete, by a reduction from Max-Cut with flips.

## Applications

Local search is the main practical method for large hard optimization problems: the TSP with 2-opt and Lin-Kernighan, scheduling, timetabling, VLSI placement and circuit partitioning, and satisfiability with WalkSAT. In AI it is the tool for problems where only the final state matters, such as the $n$-queens puzzle and configuration problems (Russell and Norvig, Section 4.1). In game theory, best-response dynamics in a potential game is the standard algorithm, and its running time is the question of how fast players reach an equilibrium. The theory of PLS explains why these methods find local optima fast on most inputs, yet have no known polynomial guarantee.

## References
