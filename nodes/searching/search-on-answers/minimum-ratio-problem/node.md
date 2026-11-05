---
tag: FMH9CD
kind: problem
slug: minimum-ratio-problem
name: Minimum ratio problem
aliases:
- fractional combinatorial optimization
- ratio optimization
- minimum ratio cycle problem
area: searching/search-on-answers
level: advanced
summary: Minimize the ratio of two linear costs, such as cost over time, over a combinatorial set of solutions.
prereqs: [fractional-programming, optimization-to-decision-reduction, negative-cycle-detection]
see_also: [fractional-programming, dinkelbach-algorithm, parametric-search, minimum-mean-cycle-problem, karp-minimum-mean-cycle, maximum-density-segment, minimum-spanning-tree, bellman-ford]
sources:
  - paper: doi:10.1287/moor.4.4.414
    title: "Nimrod Megiddo, Combinatorial optimization with rational objective functions, Mathematics of Operations Research 4(4) (1979), 414-424"
    note: the minimum ratio cycle and the minimum ratio spanning tree in strongly polynomial time
  - paper: doi:10.1109/SFCS.1992.267785
    title: "Tomasz Radzik, Newton's method for fractional combinatorial optimization, Proceedings of the 33rd IEEE Symposium on Foundations of Computer Science (1992), 659-669"
    note: a strongly polynomial bound on the number of Newton (Dinkelbach) iterations
  - paper: doi:10.1287/mnsc.13.7.492
    title: "Werner Dinkelbach, On nonlinear fractional programming, Management Science 13(7) (1967), 492-498"
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Prentice Hall, 1993
    locator: Chapter 5, Shortest Paths, Label-Correcting Algorithms (the minimum cost-to-time ratio cycle problem)
---

The minimum ratio problem asks, over a family $X$ of combinatorial structures such as the cycles, spanning trees or paths of a graph, for the structure that minimizes the ratio $c(x)/t(x)$ of two additive weights, for example cost over time. It is [fractional programming](/fractional-programming/) over a finite set with linear numerator and denominator. Its parametric form "is $\min_x (c(x) - \lambda t(x)) \le 0$?" is the ordinary problem with the edge weights $c_e - \lambda t_e$, so a [binary search](/binary-search-on-real-numbers/) on $\lambda$, [Dinkelbach's algorithm](/dinkelbach-algorithm/) or [parametric search](/parametric-search/) solves it whenever the linear problem is solvable for weights of any sign. Megiddo showed in 1979 that parametric search makes the minimum ratio cycle and the minimum ratio spanning tree strongly polynomial.

## In plain words

A ship sails between ports. Each trip earns or costs some money and takes some days. The captain wants a round trip that is best per day, not best in total: a long voyage with a large profit can be worse than a short one with a medium profit.

Ratios are awkward, so turn the question around. Guess a value per day, say 100. Charge each trip 100 for each day it takes, and ask whether some round trip still makes a profit. If one does, a better value than 100 is possible; if none does, 100 is the best or better than the best. Each guess is an ordinary question about the trips, with no ratio, and the guesses can be narrowed until the best value is found.

## Definition

**Input.** A ground set $E$ (the edges of a graph), weights $c_e \in \mathbb{R}$ and $t_e \ge 0$ for $e \in E$, and a family $X$ of subsets of $E$, given implicitly (all directed cycles, all spanning trees, all $s$-$t$ paths), with $t(x) = \sum_{e \in x} t_e > 0$ for every $x \in X$.

**Output.** An $x \in X$ that minimizes

$$\frac{c(x)}{t(x)} = \frac{\sum_{e \in x} c_e}{\sum_{e \in x} t_e},$$

and the optimal ratio $\lambda^*$.

**The parametric problem.** For a real $\lambda$, let $F(\lambda) = \min_{x \in X} \big(c(x) - \lambda t(x)\big)$, the ordinary problem with weights $w_e = c_e - \lambda t_e$. By Dinkelbach's lemma on the page [fractional programming](/fractional-programming/), $F(\lambda) \le 0$ exactly when $\lambda \ge \lambda^*$, and $F(\lambda^*) = 0$. So the decision "is $\lambda^* \le \lambda$?" is one call of the ordinary problem, and it is a [monotone predicate](/monotone-predicate/) in $\lambda$.

**The condition on the ordinary problem.** The weights $c_e - \lambda t_e$ can be negative even when all $c_e$ are positive. The method works only if the ordinary problem can be solved, or at least the sign of $F(\lambda)$ decided, for weights of any sign.

## Variants

- **Minimum ratio cycle (tramp steamer problem).** $X$ is the set of directed cycles. The decision "$F(\lambda) < 0$?" asks for a cycle that is negative under $c - \lambda t$, which [negative-cycle detection](/negative-cycle-detection/) answers in $O(nm)$ time. Maximizing profit per time is the same with $c$ negated.
- **Minimum mean cycle.** The case $t_e = 1$, where the ratio is the average weight per edge. [Karp's algorithm](/karp-minimum-mean-cycle/) solves the [minimum mean cycle problem](/minimum-mean-cycle-problem/) directly in $O(nm)$ time.
- **Minimum ratio spanning tree.** $X$ is the set of spanning trees. The decision is one [minimum spanning tree](/minimum-spanning-tree/) computation with weights $c_e - \lambda t_e$, which works for weights of any sign.
- **Maximum density.** The densest subgraph maximizes $|E(S)|/|S|$ over vertex sets $S$, with a minimum cut as the decision; the [maximum density segment](/maximum-density-segment/) maximizes a sum over a length on a sequence.
- **Minimum ratio path.** For $s$-$t$ paths the parametric weights can create negative cycles, and the shortest simple path with negative cycles is NP-hard. Megiddo's paper claimed a polynomial algorithm for this case; a later note by Ahuja, Batra and Gupta pointed out that the claim is wrong. The ratio path problem is easy when the parametric weights never create a negative cycle, for example on acyclic graphs.
- **Ratio versions of other problems.** Assignment, matching and knapsack constraints with a ratio objective, each with its own decision algorithm.

## Examples

**A minimum ratio cycle.** Take the directed graph on vertices $1, 2, 3$ with arcs $(1 \to 2)$ of cost $4$ and time $1$, $(2 \to 1)$ of cost $2$ and time $1$, $(2 \to 3)$ of cost $1$ and time $2$, and $(3 \to 1)$ of cost $3$ and time $1$. The two cycles are $1 \to 2 \to 1$, with ratio $6/2 = 3$, and $1 \to 2 \to 3 \to 1$, with ratio $8/4 = 2$. So $\lambda^* = 2$.

| $\lambda$ | weights of $1\to2$, $2\to1$, $2\to3$, $3\to1$ | cycle 121 | cycle 1231 | $F(\lambda)$ |
|---|---|---|---|---|
| 2.5 | 1.5, −0.5, −4, 0.5 | 1 | −2 | −2 < 0 |
| 1.5 | 2.5, 0.5, −2, 1.5 | 3 | 2 | 2 > 0 |
| 2 | 2, 0, −3, 1 | 2 | 0 | 0 |

At $\lambda = 2.5$ a negative cycle exists, so $\lambda^* < 2.5$. At $\lambda = 1.5$ none does, so $\lambda^* > 1.5$. At $\lambda = 2$ the smallest cycle weight is exactly $0$, attained by the optimal cycle.

**A minimum ratio spanning tree.** On a triangle with edges $a, b, e$ of (cost, time) $(3, 1)$, $(4, 4)$ and $(2, 1)$, the three spanning trees have ratios $(3 + 4)/5 = 1.4$, $(3 + 2)/2 = 2.5$ and $(4 + 2)/5 = 1.2$. At $\lambda = 1.2$ the weights are $1.8, -0.8, 0.8$, and the minimum spanning tree $\{b, e\}$ has weight $0$, which confirms $\lambda^* = 1.2$.

## Known algorithms

- **Binary search on $\lambda$.** With integer data, $\lambda^*$ is a fraction $p/q$ with $1 \le q \le T = \sum_e t_e$, and two such fractions differ by at least $1/T^2$. A search on an interval of length $L$ that stops at width below $1/T^2$, followed by one more call of the ordinary problem, finds $\lambda^*$ exactly with $O(\log(L T^2))$ calls. With $C = \sum_e |c_e|$, $L \le 2C$, so this is polynomial in the input size but not strongly polynomial.
- **Dinkelbach's algorithm.** Start with any feasible $x_0$, set $\lambda_{k} = c(x_k)/t(x_k)$, and let $x_{k+1}$ minimize $c - \lambda_k t$; stop when $F(\lambda_k) = 0$. It is Newton's method on $F$. Radzik proved that the number of iterations is strongly polynomial for linear ratio problems over any family of subsets; see [Dinkelbach's algorithm](/dinkelbach-algorithm/).
- **Parametric search.** Megiddo ran a minimum spanning tree algorithm, or a shortest-path algorithm for the cycle test, at the unknown $\lambda^*$, and resolved each comparison of two weights $c_e - \lambda t_e$ by one call of the decision. This gives strongly polynomial algorithms for the minimum ratio cycle and the minimum ratio spanning tree. With a parallel decision algorithm the number of calls drops further; see [parametric search](/parametric-search/).
- **Direct methods.** For the minimum mean cycle, Karp's dynamic program over walk lengths takes $O(nm)$ time. For the densest subgraph, a minimum cut per guess, or one parametric maximum flow, solves the problem.

## Bounds

- **Polynomial reduction.** If the ordinary problem with weights of any sign takes time $T_0$, the ratio problem takes $O(T_0 \log(CT))$ by the binary search above, for integer data.
- **Strongly polynomial.** For cycles and spanning trees, parametric search gives a number of operations bounded by a polynomial in $n$ and $m$ alone; Radzik's bound gives the same for Dinkelbach's method over any family for which the linear problem is strongly polynomial.
- **Hardness.** If the ordinary problem with weights of any sign is NP-hard, so is the ratio problem, since the decision at $\lambda$ is that problem. This is why the ratio path problem is hard in general.

## Reductions

- **To the parametric linear problem.** One call per value of $\lambda$, as above; this is the [optimization-to-decision reduction](/optimization-to-decision-reduction/) with the decision rewritten without a ratio.
- **From the linear problem.** The minimum of $c(x)$ over $X$ is the ratio problem with $t_e$ chosen so that $t(x)$ is the same for all $x$, for example $t_e = 1$ on spanning trees, where every tree has $n - 1$ edges.
- **Minimum mean cycle as a special case.** $t_e = 1$ for all $e$.

## Applications

- **Tramp steamer routing.** A ship chooses a cyclic route that maximizes profit per day.
- **Cyclic scheduling and timing.** The throughput of a cyclic process, the period of a synchronous circuit and the iteration bound of a data-flow program are maximum cycle ratios of a graph whose arcs carry delays and tokens.
- **Network design.** A spanning tree with the best ratio of benefit to cost, or of reliability to cost.
- **Graph mining.** The densest subgraph, a ratio of edges to vertices, finds dense communities.

## References
