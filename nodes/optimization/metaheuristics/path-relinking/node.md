---
tag: EFCZD2
kind: algorithm
slug: path-relinking
name: Path relinking
area: optimization/metaheuristics
level: advanced
summary: Explore paths between elite solutions to find better intermediate solutions.
model: word-ram
complexity:
  vars: {h: the Hamming distance between the two solutions, e: the time to evaluate f once, n: the length of a solution}
  time: {worst: O(h^2 e + n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [local-search, local-optimum, neighborhood-structure, hamming-distance]
see_also: [grasp, scatter-search, tabu-search, intensification-and-diversification, max-sat, iterated-local-search, genetic-algorithm, crossover]
sources:
  - paper: "Fred Glover, Tabu search and adaptive memory programming, advances, applications and challenges, in R. S. Barr, R. V. Helgason and J. L. Kennington (editors), Interfaces in Computer Science and Operations Research, Kluwer, 1997"
    locator: pp. 1 to 75 (path relinking as a way to combine elite solutions)
  - book: isbn:9780792381877
    title: Fred Glover and Manuel Laguna, Tabu Search, Kluwer Academic Publishers, 1997
    locator: the chapters on intensification and on scatter search and path relinking
  - paper: "Fred Glover, Manuel Laguna and Rafael Martí, Fundamentals of scatter search and path relinking, Control and Cybernetics 29(3), 2000"
    locator: pp. 653 to 684 (initiating and guiding solutions, the moves along the path, the link to scatter search)
  - paper: "Manuel Laguna and Rafael Martí, GRASP and path relinking for 2-layer straight line crossing minimization, INFORMS Journal on Computing 11(1), 1999"
    locator: pp. 44 to 52 (path relinking as an intensification step of GRASP)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 6, Greedy Randomized Adaptive Search Procedures, Advances and Extensions, by Mauricio G. C. Resende and Celso C. Ribeiro, from p. 169 (GRASP with path relinking, forward, backward and mixed relinking)
---

Path relinking is a [metaheuristic](/metaheuristic/) step that takes two good solutions and walks from one to the other, one move at a time, looking for a better solution on the way. The walk starts at the *initiating* solution and each move makes the current solution more like the *guiding* solution. The moves are chosen greedily: of the moves that bring in one more attribute of the guiding solution, take the one that gives the best objective. Glover proposed path relinking in the 1990s as part of the [tabu search](/tabu-search/) and [scatter search](/scatter-search/) framework. It is now often used inside [GRASP](/grasp/) to combine new local optima with a pool of elite solutions. On bit strings, the walk takes exactly as many moves as the [Hamming distance](/hamming-distance/) between the two solutions. Path relinking has no guarantee of finding an optimum.

## In plain words

Two good solutions often share most of their parts, and a better solution is often somewhere between them. Path relinking walks from the first to the second. At each step it copies one more part from the second solution into the current one, and it picks the part whose copy helps most, or hurts least. After a few steps the current solution is the second solution. The best solution seen on the way is the result.

The walk must move every time, even if every move makes things worse. This is the point: a plain descent stops at the first solution, but the walk is forced across the hill between the two.

## The problem

The page shows path relinking on bit strings. The input is a cost $f : \{0, 1\}^n \to \mathbb{R}$ to minimize, an initiating solution $x^s$ and a guiding solution $x^t$. In the example $f$ is the total weight of the clauses that are not satisfied in a weighted [MAX-SAT](/max-sat/) instance. The output is the best point on a path of one-bit moves from $x^s$ to $x^t$. In a full method, $x^s$ and $x^t$ are local optima from an elite pool, and the output goes on to a local search.

## The algorithm

```pseudo id=main
PATH-RELINKING(xs, xt, f)
L1  x ← xs;  b ← xs
L2  Δ ← { i : x_i ≠ xt_i }
L3  while Δ is not empty do
L4      i ← the position in Δ whose flip gives the least f, ties to the lowest
L5      flip x_i;  Δ ← Δ \ {i}
L6      if f(x) < f(b) then b ← x
L7  return b
```

Line L2 lists the positions where the two solutions differ. Each pass of the loop flips one of them, so $x$ gets one bit closer to $x^t$. Line L4 is the greedy choice: it looks only at the moves toward $x^t$ and takes the best one, even if it raises the cost. Line L6 keeps the best point seen. The loop ends when $x = x^t$.

## Example

Take the weighted MAX-SAT instance with 6 variables and these 12 clauses.

| clause | literals | weight |
|---|---|---|
| $C_1$ | $x_6 \lor x_2 \lor x_5$ | 3 |
| $C_2$ | $x_1 \lor \bar{x}_5$ | 7 |
| $C_3$ | $x_4 \lor \bar{x}_2$ | 5 |
| $C_4$ | $\bar{x}_1 \lor \bar{x}_3$ | 6 |
| $C_5$ | $x_3 \lor \bar{x}_6$ | 4 |
| $C_6$ | $\bar{x}_6 \lor x_3 \lor \bar{x}_4$ | 6 |
| $C_7$ | $\bar{x}_6 \lor \bar{x}_4 \lor x_2$ | 9 |
| $C_8$ | $\bar{x}_2 \lor \bar{x}_6 \lor \bar{x}_3$ | 3 |
| $C_9$ | $x_5 \lor \bar{x}_3 \lor x_4$ | 4 |
| $C_{10}$ | $x_2 \lor x_3$ | 8 |
| $C_{11}$ | $x_6 \lor \bar{x}_4 \lor x_5$ | 4 |
| $C_{12}$ | $\bar{x}_2 \lor \bar{x}_4$ | 1 |

Write an assignment as the bits $x_1 \ldots x_6$. By enumeration of the 64 assignments, the least cost is 1, at 110110 only, which leaves $C_{12}$ unsatisfied. The one-flip neighborhood has 9 local minima. Two of them are $x^s = 010100$ of cost 5 ($C_{11}$ and $C_{12}$ unsatisfied) and $x^t = 101110$ of cost 6 ($C_4$ unsatisfied). They differ in $x_1$, $x_2$, $x_3$ and $x_5$, so the Hamming distance is 4.

| step | $x$ | $f(x)$ | cost after flipping each position in $\Delta$ | flip |
|---|---|---|---|---|
| 0 | 010100 | 5 | $x_1$: 5, $x_2$: 15, $x_3$: 5, $x_5$: 8 | $x_1$ |
| 1 | 110100 | 5 | $x_2$: 15, $x_3$: 11, $x_5$: 1 | $x_5$ |
| 2 | 110110 | 1 | $x_2$: 8, $x_3$: 7 | $x_3$ |
| 3 | 111110 | 7 | $x_2$: 6 | $x_2$ |
| 4 | 101110 | 6 | | |

In step 0, $x_1$ and $x_3$ tie at 5, and the tie goes to $x_1$. The move to 110100 does not lower the cost, so a descent would not make it, but path relinking must move. The next move reaches 110110, the optimum. Steps 2 and 3 raise the cost and end at $x^t$, as they must. The result is $b = 110110$ with cost 1.

The direction matters. From $x^t = 101110$ to $x^s = 010100$ the greedy path is 101110 (6), 001110 (7), 001100 (7), 011100 (5), 010100 (5), and its best point 011100 of cost 5 leads by one-flip descent to 011101 of cost 4, not to the optimum.

Over all 72 ordered pairs of distinct one-flip local minima of this instance, 21 greedy paths pass through the optimum, and 24 reach it when a one-flip descent is run from the best point of the path. These are exact counts for this one instance.

## Correctness

Path relinking has no optimality guarantee, so "correct" means the following. Each pass flips a bit where $x$ still differs from $x^t$, so the set of differing positions loses one element per pass. So the loop makes exactly $h$ passes, where $h$ is the Hamming distance of $x^s$ and $x^t$, the points on the path are distinct, and the last point is $x^t$. The path is a shortest path between the two solutions in the one-flip neighborhood. The result is a point of the path with the least cost, so its cost is at most $\min(f(x^s), f(x^t))$. The [full proof](proofs/correctness.md) gives all steps.

The result is only the best point on one of the $h!$ shortest paths, and it need not be a local minimum.

## Complexity

The loop makes $h$ passes, and pass $k$ evaluates $h - k + 1$ candidate moves, so there are $h (h + 1) / 2$ evaluations of $f$ in all. With $e$ the time of one evaluation and $O(n)$ to copy the start and compute $\Delta$, the time is $O(h^2 e + n)$. For MAX-SAT, a code that keeps for each variable the change in cost of its flip can update these changes after each flip in time proportional to the clauses of the flipped variable, which makes $e$ much smaller than a full evaluation. The extra space is $O(n)$ for $x$, $b$ and $\Delta$.

## Properties

- **Deterministic.** With a fixed tie rule, the path is a function of $x^s$, $x^t$ and $f$.
- **A shortest path.** The walk never moves away from the guiding solution, so it takes exactly $h$ moves.
- **Forced moves.** Each move is the best move toward $x^t$, not the best move overall, and it is made even if it raises the cost. This lets the walk cross the region between two local minima.
- **Combines, does not mix at random.** Like [crossover](/crossover/) in a [genetic algorithm](/genetic-algorithm/), path relinking builds solutions that take some parts from each parent. Unlike uniform crossover, it chooses the parts by the objective and it looks at every point on the path.
- **Intensification.** Path relinking searches the region between good solutions, so it is an [intensification](/intensification-and-diversification/) step.

## Variants and improvements

- **Forward, backward and mixed.** Forward relinking starts at the worse solution, backward relinking starts at the better one, and mixed relinking moves the two ends toward each other. The example shows that the two directions can give different results.
- **Truncated relinking.** Stop after some fraction of the path. Good points are often near one end.
- **Local search on the path.** Run a local search from the best point, or from several points of the path. In the example this adds 3 pairs that reach the optimum.
- **Elite pools.** In GRASP with path relinking, each new local minimum is relinked with a solution from a small pool of elite solutions, and the pool is updated with good results that are not too close to the solutions already in it. Resende and Ribeiro describe these schemes in the handbook chapter.
- **Other neighborhoods.** For permutations, a move can place one element at the position it has in the guiding solution, and $\Delta$ is the set of elements whose positions differ.

## When to use it

Use path relinking when good solutions share much of their structure, so that a better solution is likely to lie between two good ones, and when a method already makes a pool of good solutions, such as GRASP, tabu search or [iterated local search](/iterated-local-search/). It adds memory to a method like GRASP whose iterations are otherwise independent. It is of little use when the two solutions are very close, since the path is short, or very far apart, since the path then passes through many poor points.

## Pitfalls

- **Relinking near copies.** If $x^s$ and $x^t$ differ in one or two positions, the path has nothing new to offer. Codes keep pairs apart by a minimum distance.
- **Counting the ends.** The best point can be $x^s$ or $x^t$ itself. Report it as such and do not count the run as a new find.
- **Treating the result as a local optimum.** The best point on a path is often not one. Follow with a local search.
- **Full evaluations at each step.** Evaluating $f$ from scratch for each candidate costs $O(h^2)$ full evaluations per path. Incremental evaluation of moves is usually needed for large instances.

## Implementations

## History

Glover proposed path relinking in the 1990s, as a generalization of the way scatter search combines solutions, and described it within his work on tabu search and adaptive memory programming. Glover, Laguna and Martí gave a joint account of scatter search and path relinking in 2000. Laguna and Martí combined it with GRASP in 1999, and GRASP with path relinking is now a standard form of GRASP, described in the chapter by Resende and Ribeiro in the Handbook of Metaheuristics.

## References
