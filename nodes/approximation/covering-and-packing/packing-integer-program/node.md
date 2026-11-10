---
tag: EJJYG1
kind: problem
slug: packing-integer-program
name: Packing integer program
aliases:
- packing IP
- PIP
- packing integer linear program
area: approximation/covering-and-packing
level: advanced
summary: Maximize a nonnegative objective subject to packing constraints on integer variables.
prereqs: [lp-relaxation, randomized-rounding, chernoff-bound, approximation-ratio]
see_also: [covering-integer-program, set-packing, knapsack-problem, randomized-rounding, chernoff-bound, independent-set, lp-relaxation, integrality-gap]
sources:
  - paper: "P. Raghavan and C. D. Thompson, Randomized rounding: a technique for provably good algorithms and algorithmic proofs, Combinatorica 7(4), 1987, pp. 365-374"
    title: Raghavan and Thompson 1987
    locator: the randomized rounding method and its analysis by Chernoff bounds
  - paper: "P. Raghavan, Probabilistic construction of deterministic algorithms: approximating packing integer programs, Journal of Computer and System Sciences 37(2), 1988, pp. 130-143"
    title: Raghavan 1988
    locator: the bounds for packing integer programs and their derandomization by pessimistic estimators
  - paper: "A. Srinivasan, Improved approximation guarantees for packing and covering integer programs, SIAM Journal on Computing 29(2), 1999, pp. 648-670"
    title: Srinivasan 1999
    locator: the improved bounds for packing integer programs in terms of B and the column structure
  - paper: "N. Bansal, N. Korula, V. Nagarajan and A. Srinivasan, Solving packing integer programs via randomized rounding with alterations, Theory of Computing 8, 2012, pp. 533-565"
    title: Bansal, Korula, Nagarajan and Srinivasan 2012
    locator: the O(k) approximation for k-column-sparse packing integer programs
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 5 (randomized rounding and Chernoff bounds)
---

A packing integer program (PIP) maximizes a nonnegative linear objective over integer vectors subject to constraints $Ax \le b$ with nonnegative $A$ and positive $b$. It contains the [knapsack problem](/knapsack-problem/) (one constraint), [independent set](/independent-set/) and [set packing](/set-packing/) (0/1 constraints with right side 1), and matching. The standard method solves the [LP relaxation](/lp-relaxation/), scales the fractional solution down, and rounds it by [randomized rounding](/randomized-rounding/); the [Chernoff bound](/chernoff-bound/) controls each constraint. The ratio that this gives depends on the number $m$ of constraints and on the least right side $B$: it is $O(m^{1/B})$, and it tends to 1 when $B$ is large compared with $\log m$.

## In plain words

You can choose some items, and each item brings a profit. Each item also uses some amount of several shared resources, such as money, space or time, and each resource has a limit. You want the most profit without passing any limit.

A good first step is to allow fractions of items. That problem is easy to solve, and it gives an upper limit on the best profit. Then you take each item with a probability equal to its fraction, made a little smaller. Each limit is then broken only with a very small probability. If the limits are large compared with the use of one item, you lose almost nothing; if the limits are small, you can lose a lot, and this loss cannot be avoided in general.

## Definition

The input is a matrix $A \in \mathbb{R}_{\ge 0}^{m \times n}$, a vector $b \in \mathbb{R}_{> 0}^m$ and a vector $c \in \mathbb{R}_{\ge 0}^n$. The problem is

$$\max\ c^{\top} x \quad \text{subject to} \quad A x \le b, \qquad x \in \{0, 1\}^n.$$

The version with $x \in \mathbb{Z}_{\ge 0}^n$, possibly with upper bounds $x_j \le d_j$, reduces to this one by copies of variables. After scaling each row, we can assume $A \in [0, 1]^{m \times n}$, so that one item uses at most the full limit, and we write $B = \min_i b_i \ge 1$. The LP relaxation replaces $x \in \{0,1\}^n$ by $x \in [0, 1]^n$; its optimum $\mathrm{LP}^*$ is at least $\mathrm{OPT}$.

*Ratio convention.* This is a maximization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \ge \mathrm{OPT} / \rho$ on every input. The analyses below compare with the upper bound $\mathrm{OPT} \le \mathrm{LP}^*$.

## Variants

- **0/1 matrices.** $A \in \{0, 1\}^{m \times n}$ and $b = \mathbf{1}$: this is [set packing](/set-packing/), with the items as sets and the rows as elements; with two ones in each row, it is [independent set](/independent-set/).
- **Few constraints.** With $m = 1$ it is the [knapsack problem](/knapsack-problem/), which has an FPTAS. With a constant $m$ it is the multidimensional knapsack problem, which has a PTAS (Frieze and Clarke 1984) but no FPTAS for $m \ge 2$ unless P = NP.
- **Column sparse.** Each column has at most $k$ nonzero entries; each item uses at most $k$ resources. This includes $k$-set packing and matching in hypergraphs of rank $k$.
- **Graph structure.** The rows are the vertices of a graph and the columns its edges: [b-matching](/b-matching/) and [maximum weight matching](/maximum-weight-matching/). Paths with edge capacities give [edge-disjoint paths](/edge-disjoint-paths/) and unsplittable flow.
- **Several knapsacks.** One item may go into one of several knapsacks: the [multiple knapsack problem](/multiple-knapsack-problem/).
- **The covering version.** Minimize $c^\top x$ subject to $Ax \ge b$: the [covering integer program](/covering-integer-program/).

## Examples

*An integrality gap.* For [independent set](/independent-set/) in the complete graph $K_n$, the PIP has one variable for each vertex and the constraint $x_u + x_v \le 1$ for each edge. The point $x = (\frac12, \ldots, \frac12)$ is feasible, so $\mathrm{LP}^* \ge \frac n2$, but $\mathrm{OPT} = 1$. Here $B = 1$, and the [integrality gap](/integrality-gap/) is at least $\frac n2$. With $n = 3$ the PIP is

$$\max\ x_1 + x_2 + x_3 \quad \text{s.t.} \quad x_1 + x_2 \le 1,\ x_2 + x_3 \le 1,\ x_1 + x_3 \le 1,$$

with $\mathrm{LP}^* = \frac32$ at $(\frac12, \frac12, \frac12)$ and $\mathrm{OPT} = 1$.

*Large right sides.* If each row has $b_i = 100$ and all entries in $[0, 1]$, then rounding $(1 - \varepsilon)x^*$ with a moderate $\varepsilon$ breaks a fixed row only with a tiny probability, and the result keeps almost all of $\mathrm{LP}^*$.

## Known algorithms

- **Randomized rounding (Raghavan and Thompson 1987).** Solve the LP to get $x^*$. Fix $\alpha \in (0, 1]$, and set $X_j = 1$ with probability $\alpha x^*_j$, independently. Then $\mathbb{E}[c^\top X] = \alpha\,\mathrm{LP}^*$ and $\mathbb{E}[(AX)_i] \le \alpha b_i$.
  *Theorem.* Let $A \in [0,1]^{m \times n}$, $b_i \ge B \ge 1$, $c \in [0, 1]^n$, $\alpha = 1 / \bigl(e\,(4m)^{1/B}\bigr)$, and $\alpha\,\mathrm{LP}^* \ge 12$. Then with probability at least $\frac12$, $X$ is feasible and $c^\top X \ge \frac{\alpha}{2}\,\mathrm{LP}^*$. So $\mathrm{OPT} \le \mathrm{LP}^* \le 2e\,(4m)^{1/B}\,\mathrm{ALG}$.
  *Proof.* Fix a row $i$ and let $Y = (AX)_i$, a sum of independent variables in $[0, 1]$ with $\mathbb{E}[Y] \le \mu = \alpha b_i$. The Chernoff bound with $1 + \delta = 1/\alpha$ gives $\Pr[Y \ge b_i] \le \bigl(e^{\delta} / (1+\delta)^{1+\delta}\bigr)^{\mu} = e^{b_i (1 - \alpha)}\,\alpha^{b_i} \le (e\alpha)^{b_i} \le (e\alpha)^B = \frac{1}{4m}$, since $e\alpha < 1$. By the union bound, some row is broken with probability at most $\frac14$. The objective $Z = c^\top X$ is a sum of independent variables in $[0, 1]$ with mean $\alpha\,\mathrm{LP}^* \ge 12$, so the lower tail bound gives $\Pr[Z < \frac{\alpha}{2}\,\mathrm{LP}^*] \le e^{-\alpha\,\mathrm{LP}^*/8} \le e^{-3/2} < \frac14$. $\square$
- **Large $B$.** If $B \ge C \ln(m) / \varepsilon^2$ for a suitable constant $C$, the same rounding with $\alpha = 1 - \varepsilon$ gives value at least $(1 - O(\varepsilon))\,\mathrm{LP}^*$ with constant probability, by the Chernoff bound in its form for small $\delta$.
- **Derandomization.** Raghavan (1988) replaced the random choices by pessimistic estimators, a form of the [method of conditional expectations](/method-of-conditional-expectations/), so the bounds hold for a deterministic algorithm.
- **Better dependence on the matrix.** Srinivasan (1999) used the column structure and positive correlation to improve the bounds, for example for 0/1 matrices to about $m^{1/(B+1)}$.
- **Column sparse PIPs.** If each column has at most $k$ nonzero entries, randomized rounding with alterations gives ratio $O(k)$ (Bansal, Korula, Nagarajan and Srinivasan 2012).
- **Exact methods.** Branch and bound with the LP bound, and dynamic programming over the right sides when $m$ is small and the numbers are integers of moderate size.

## Bounds

| claim | statement | source |
|---|---|---|
| upper bound used | $\mathrm{OPT} \le \mathrm{LP}^*$ | LP relaxation |
| rounding, general $B$ | ratio $O(m^{1/B})$ | proved above; Raghavan 1988 |
| rounding, large $B$ | ratio $1 + O(\varepsilon)$ when $B = \Omega(\log(m) / \varepsilon^2)$ | Raghavan 1988 |
| integrality gap, $B = 1$ | at least $\frac n2$ | complete graph, above |
| hardness, $B = 1$ | no ratio $n^{1 - \varepsilon}$ and no ratio $m^{1/2 - \varepsilon}$, unless P = NP | from independent set and set packing |
| one constraint | FPTAS | [knapsack](/knapsack-problem/) |

## Reductions

- **From independent set.** A graph with $n$ vertices and $m$ edges gives a PIP with one variable for each vertex and the constraint $x_u + x_v \le 1$ for each edge; the feasible 0/1 vectors are the independent sets. Since independent set has no polynomial-time ratio $n^{1 - \varepsilon}$ unless P = NP (Håstad 1999, Zuckerman 2007), neither has PIP with $B = 1$. In terms of the number of rows, this gives no ratio $m^{1/2 - \varepsilon}$, because $m < n^2$.
- **From set packing.** A family of sets over a universe gives a PIP with one variable for each set and the constraint $\sum_{S \ni u} x_S \le 1$ for each element $u$; see [set packing](/set-packing/).
- **From knapsack.** One row: $\max c^\top x$ subject to $a^\top x \le b$.
- **To LP.** Dropping integrality gives a [linear program](/linear-programming-problem/) with the same constraints, solved in polynomial time; this is the base of all the rounding methods.

## Applications

- **Capital budgeting.** Select projects with profits, subject to budget limits in several years.
- **Routing.** Choose paths for requests in a network with edge capacities, to route the most requests: unsplittable flow and [edge-disjoint paths](/edge-disjoint-paths/).
- **Combinatorial auctions.** Choose winning bids, each for a bundle of items, so that no item is sold more than its supply.
- **Scheduling and allocation.** Admission control, where jobs with resource needs are accepted on machines with resource limits.

## References
