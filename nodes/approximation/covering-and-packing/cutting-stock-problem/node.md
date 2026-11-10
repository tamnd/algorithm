---
tag: DQYG44
kind: problem
slug: cutting-stock-problem
name: Cutting stock problem
aliases:
- one-dimensional cutting stock
- cutting stock
- Gilmore-Gomory model
area: approximation/covering-and-packing
level: advanced
summary: Cut stock rolls to meet demands for piece lengths with minimum waste or rolls.
prereqs: [bin-packing, linear-programming-problem, lp-duality, unbounded-knapsack]
see_also: [bin-packing, column-generation, configuration-lp, karmarkar-karp-bin-packing, unbounded-knapsack, rod-cutting-problem, first-fit-decreasing, bin-packing-lower-bound]
sources:
  - paper: doi:10.1287/opre.9.6.849
    title: "P. C. Gilmore and R. E. Gomory, A linear programming approach to the cutting-stock problem, Operations Research 9(6), 1961"
    locator: pp. 849-859, the pattern formulation and the knapsack pricing step
  - paper: "P. C. Gilmore and R. E. Gomory, A linear programming approach to the cutting stock problem, Part II, Operations Research 11(6), 1963, pp. 863-888"
    title: Gilmore and Gomory 1963
    locator: computational experience and the use of the knapsack solution
  - paper: "L. V. Kantorovich, Mathematical methods of organizing and planning production, Management Science 6(4), 1960, pp. 366-422 (translation of the 1939 text)"
    title: Kantorovich 1939
    locator: the early formulation of cutting problems as linear programs
  - paper: "M. X. Goemans and T. Rothvoss, Polynomiality for bin packing with a constant number of item types, SODA 2014"
    title: Goemans and Rothvoss 2014
    locator: the main theorem (polynomial time for a fixed number of piece types)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 4 (the configuration LP for bin packing and its solution)
---

The cutting stock problem asks how to cut stock rolls of one fixed length into pieces of given lengths, so that the demand for each piece length is met and the number of rolls is as small as possible. It is [bin packing](/bin-packing/) with *high multiplicity*: the input lists each piece length once, with a demand, instead of listing each piece. Its linear programming relaxation over cutting patterns, solved by [column generation](/column-generation/) with a knapsack problem as the pricing step, was introduced by Gilmore and Gomory (1961) and is one of the first large-scale uses of linear programming in industry. The same relaxation is the [configuration LP](/configuration-lp/) of bin packing.

## In plain words

A paper mill makes big rolls of paper, all of the same width. Customers want narrower rolls of several widths, each in some quantity. The mill cuts each big roll across its width into narrower pieces, and the leftover strip is waste. The question is how to cut, so that every order is filled and the number of big rolls is as small as possible.

A way to cut one big roll is called a pattern. There are a huge number of patterns, but a good plan uses only a few of them, each many times. The classic method starts with a few patterns, finds the best mix of them, and then asks: is there a new pattern that would make the plan cheaper? Finding that pattern is a small packing puzzle of its own.

## Definition

The input is a stock length $W > 0$ and $m$ piece types; type $i$ has length $w_i$ with $0 < w_i \le W$ and demand $d_i \in \mathbb{Z}_{\ge 1}$. A *pattern* is a vector $a \in \mathbb{Z}_{\ge 0}^m$ with $\sum_i a_i w_i \le W$: it cuts $a_i$ pieces of type $i$ from one roll. Let $\mathcal{P}$ be the set of patterns. The problem is the integer program

$$\min \sum_{a \in \mathcal{P}} x_a \quad \text{subject to} \quad \sum_{a \in \mathcal{P}} a_i\, x_a \ge d_i \ \ (i = 1, \ldots, m), \qquad x_a \in \mathbb{Z}_{\ge 0},$$

where $x_a$ is the number of rolls cut with pattern $a$. Extra pieces may be thrown away, so "$\ge$" is the same as "$=$" up to removing pieces from patterns. We write $\mathrm{OPT}$ for the optimum and $\mathrm{LP}^*$ for the optimum of the linear relaxation with $x_a \ge 0$ real.

With all $d_i = 1$, this is bin packing with capacity $W$. The input size is about $m \log(W + \max_i d_i)$, so the number of pieces $\sum_i d_i$ can be exponential in the input size.

*Ratio convention.* This is a minimization problem. The bounds below are absolute or additive, and they compare with the lower bounds $\mathrm{OPT} \ge \lceil \mathrm{LP}^* \rceil \ge \lceil \sum_i d_i w_i / W \rceil$.

## Variants

- **Minimum waste.** Minimize the total trim loss $\sum_a x_a (W - \sum_i a_i w_i)$. With exact demands this is the same as minimizing the number of rolls.
- **Multiple stock lengths.** Rolls of several lengths, each with a cost; the problem is variable sized bin packing.
- **Two-stage and two-dimensional cutting.** Sheets are cut in two directions, often by guillotine cuts; see [strip packing](/strip-packing/) and [rectangle packing](/rectangle-packing/).
- **Bounded patterns.** Each pattern may have at most a given number of pieces, because a cutting machine has a limited number of knives.
- **Single piece, value maximization.** Cutting one rod into pieces of given values is the [rod cutting problem](/rod-cutting-problem/), which is an [unbounded knapsack](/unbounded-knapsack/) problem.

## Examples

Take $W = 10$ and three types: length 6 with demand 2, length 4 with demand 3, length 3 with demand 4. The total length is $12 + 12 + 12 = 36$, so at least $\lceil 3.6 \rceil = 4$ rolls are needed.

| pattern $(a_6, a_4, a_3)$ | pieces | waste |
|---|---|---|
| $(1, 1, 0)$ | 6, 4 | 0 |
| $(1, 0, 1)$ | 6, 3 | 1 |
| $(0, 1, 2)$ | 4, 3, 3 | 0 |
| $(0, 0, 3)$ | 3, 3, 3 | 1 |
| $(0, 2, 0)$ | 4, 4 | 2 |

The plan $2 \times (1, 1, 0)$, $1 \times (0, 1, 2)$, $1 \times (0, 0, 2)$ uses 4 rolls, so $\mathrm{OPT} = 4$. The linear relaxation has $\mathrm{LP}^* = \frac{11}{3}$, which is larger than the length bound $3.6$; here $\lceil \mathrm{LP}^* \rceil = \mathrm{OPT}$.

*One step of column generation.* Start with the patterns $(1, 0, 0)$, $(0, 2, 0)$, $(0, 0, 3)$. The restricted LP has the solution $x = (2, \frac32, \frac43)$ with value $\frac{29}{6}$ and the dual prices $y = (1, \frac12, \frac13)$. The pricing problem is $\max\, y \cdot a$ over patterns $a$, a knapsack problem with capacity 10. Its best solution is $(1, 1, 0)$ with value $\frac32 > 1$, so this pattern has negative reduced cost $1 - \frac32$, and it enters the LP.

## Known algorithms

- **Gilmore and Gomory column generation.** Solve the LP relaxation with only some patterns. Take the dual prices $y_i$. Solve the [unbounded knapsack](/unbounded-knapsack/) problem $\max \{ y \cdot a : \sum_i a_i w_i \le W,\ a \in \mathbb{Z}_{\ge 0}^m \}$. If its value is more than 1, add the pattern and repeat; otherwise the LP is optimal, by [LP duality](/lp-duality/). The knapsack step is NP-hard in general but takes $O(mW)$ time by dynamic programming. Then round the LP solution: round each $x_a$ down and pack the remaining pieces with a heuristic such as [first fit decreasing](/first-fit-decreasing/).
- **Rounding a basic solution.** A basic optimal solution has at most $m$ nonzero entries. Rounding each up gives at most $\mathrm{LP}^* + m$ rolls.
- **Karmarkar and Karp.** Solve the LP approximately with the [ellipsoid method](/ellipsoid-method/) and use geometric grouping, for at most $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$ rolls; see [Karmarkar and Karp](/karmarkar-karp-bin-packing/). Hoberg and Rothvoss (2017) improved this to $\mathrm{OPT} + O(\log \mathrm{OPT})$.
- **Branch and price.** For exact solutions, combine column generation with branch and bound. In practice the gap $\mathrm{OPT} - \lceil \mathrm{LP}^* \rceil$ is almost always 0 or 1, so the LP bound prunes well.
- **Few types.** Goemans and Rothvoss (2014) solve the problem exactly in polynomial time when the number $m$ of types is a constant, with a running time of $(\log \Delta)^{2^{O(m)}}$, where $\Delta$ bounds the numbers in the input.

## Bounds

| claim | statement | source |
|---|---|---|
| LP bound | $\mathrm{OPT} \ge \lceil \mathrm{LP}^* \rceil \ge \lceil \sum_i d_i w_i / W \rceil$ | [bin packing lower bounds](/bin-packing-lower-bound/) |
| basic rounding | $\mathrm{OPT} \le \lceil \mathrm{LP}^* \rceil + m$ | rounding a basic solution |
| additive | $\mathrm{OPT} + O(\log \mathrm{OPT})$ rolls in polynomial time | Hoberg and Rothvoss 2017 |
| hardness | NP-hard even with $m$ part of the input and all $d_i = 1$, strongly NP-hard | [bin packing hardness](/bin-packing-np-hardness/) |
| conjecture | $\mathrm{OPT} \le \lceil \mathrm{LP}^* \rceil + 1$ on every instance (the modified integer round-up conjecture) | open |

## Reductions

- **Bin packing is a special case.** Set all demands to 1. So all hardness results for [bin packing](/bin-packing/) apply, including strong NP-hardness and the absolute $\frac32$ bound.
- **Cutting stock reduces to bin packing.** Write out $d_i$ copies of each type. This gives a bin packing list of length $\sum_i d_i$, which can be exponential in the input size, so the reduction is only pseudo-polynomial.
- **The pricing step is a knapsack problem.** Each column generation step solves an [unbounded knapsack](/unbounded-knapsack/) problem; the separation problem for the dual of the configuration LP is exactly this knapsack problem, so an exact or approximate knapsack solver gives an exact or approximate LP solution.

## Applications

- **Paper, film, steel and textile mills.** Cutting master rolls or coils into customer widths; this was the first industrial use of the Gilmore and Gomory method.
- **Lumber and pipe.** Cutting standard lengths of wood, pipe or cable into required pieces.
- **Scheduling and allocation.** Packing jobs of a few distinct durations into machine shifts, and assigning advertisements of a few lengths to fixed breaks.
- **A model for bin packing algorithms.** The pattern LP is the [configuration LP](/configuration-lp/) used by the best approximation algorithms for bin packing.

## References
