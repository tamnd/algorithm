---
tag: 3PZQJN
kind: problem
slug: covering-integer-program
name: Covering integer program
aliases:
- covering IP
- CIP
- covering integer linear program
area: approximation/covering-and-packing
level: advanced
summary: Minimize a nonnegative objective subject to covering constraints on integer variables.
prereqs: [lp-relaxation, randomized-rounding, chernoff-bound, set-cover]
see_also: [packing-integer-program, set-cover, vertex-cover, randomized-rounding, chernoff-bound, lp-relaxation, integrality-gap, primal-dual-approximation]
sources:
  - paper: "G. Dobson, Worst-case analysis of greedy heuristics for integer programming with nonnegative data, Mathematics of Operations Research 7(4), 1982, pp. 515-531"
    title: Dobson 1982
    locator: the greedy algorithm for covering integer programs and its logarithmic ratio
  - paper: "A. Srinivasan, Improved approximation guarantees for packing and covering integer programs, SIAM Journal on Computing 29(2), 1999, pp. 648-670"
    title: Srinivasan 1999
    locator: the bounds for covering integer programs in terms of m and B
  - paper: "R. D. Carr, L. K. Fleischer, V. J. Leung and C. A. Phillips, Strengthening integrality gaps for capacitated network design and covering problems, SODA 2000, pp. 106-115"
    title: Carr, Fleischer, Leung and Phillips 2000
    locator: the knapsack cover inequalities and the primal-dual algorithms that use them
  - paper: "S. G. Kolliopoulos and N. E. Young, Approximation algorithms for covering/packing integer programs, Journal of Computer and System Sciences 71(4), 2005, pp. 495-505"
    title: Kolliopoulos and Young 2005
    locator: the covering integer programs with multiplicity constraints
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1 and Chapter 5 (set cover by rounding and by randomized rounding)
---

A covering integer program (CIP) minimizes a nonnegative linear cost over nonnegative integer vectors subject to constraints $Ax \ge b$ with nonnegative $A$ and positive $b$. It contains [set cover](/set-cover/) (a 0/1 matrix and right side 1), [vertex cover](/vertex-cover/), multicover and the minimum knapsack problem. Without upper bounds on the variables, scaling the LP solution up by a factor $O(\log m)$ and rounding it gives ratio $O(\log m)$, which matches the hardness of set cover up to a constant. With upper bounds such as $x \in \{0, 1\}^n$, the natural LP can be arbitrarily weak, and the knapsack cover inequalities of Carr, Fleischer, Leung and Phillips (2000) are needed.

## In plain words

You must meet several demands, such as amounts of nutrients in a diet or numbers of guards at several gates. Each option you can buy costs money and helps several demands by some amount. You may buy each option several times. You want to meet all demands at the least cost.

If you allow fractions of options, the best plan is easy to find, and its cost is a lower limit for the true answer. To get a whole plan, you multiply the fractions by a moderate factor and then round them at random. Each demand then fails only with a small probability, and the cost grows by about that factor. When each option may be bought only once, a plan with fractions can cheat badly, and stronger rules are needed.

## Definition

The input is a matrix $A \in \mathbb{R}_{\ge 0}^{m \times n}$, a vector $b \in \mathbb{R}_{> 0}^m$ and a vector $c \in \mathbb{R}_{\ge 0}^n$. The problem is

$$\min\ c^{\top} x \quad \text{subject to} \quad A x \ge b, \qquad x \in \mathbb{Z}_{\ge 0}^n,$$

possibly with multiplicity constraints $x \le d$; the case $d = \mathbf{1}$ is the 0/1 CIP. For integer $x$ we can replace each $a_{ij}$ by $\min(a_{ij}, b_i)$ without changing the feasible integer vectors, because $x_j \ge 1$ with $a_{ij} \ge b_i$ meets row $i$ in both cases. After this, and after dividing each row by its largest entry, $A \in [0, 1]^{m \times n}$ and $B = \min_i b_i \ge 1$. The LP relaxation allows real $x \ge 0$ (and $x \le d$); its optimum $\mathrm{LP}^*$ is at most $\mathrm{OPT}$.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ on every input. The analyses compare with the lower bound $\mathrm{OPT} \ge \mathrm{LP}^*$, for the natural LP or for the LP with knapsack cover inequalities.

## Variants

- **Set cover and multicover.** $A \in \{0, 1\}^{m \times n}$ with the columns as sets and the rows as elements; $b = \mathbf{1}$ gives [set cover](/set-cover/), and integer $b$ gives multiset multicover. With exactly two ones in each row, that is, each element in exactly two sets, it is [vertex cover](/vertex-cover/).
- **Minimum knapsack.** One row: buy items of sizes $a_j$ and costs $c_j$, each at most once, of total size at least $b$, at least cost.
- **Multiplicity constraints.** $x_j \le d_j$; the 0/1 case is the hardest for LP methods.
- **Row sparse.** Each row has at most $f$ nonzero entries; for set cover, $f$ is the largest frequency of an element.
- **The packing version.** Maximize $c^\top x$ subject to $Ax \le b$: the [packing integer program](/packing-integer-program/). The LP dual of the covering LP $\min\{c^\top x : Ax \ge b, x \ge 0\}$ is the packing LP $\max\{b^\top y : A^\top y \le c, y \ge 0\}$.

## Examples

*The natural LP fails with upper bounds.* Take one row $(B - 1)\,x_1 + B\,x_2 \ge B$ with $x \in \{0, 1\}^2$, costs $c_1 = 0$ and $c_2 = 1$, and $B \ge 2$. The item $x_1$ alone gives only $B - 1$, so each feasible 0/1 vector has $x_2 = 1$, and $\mathrm{OPT} = 1$. The LP point $x_1 = 1$, $x_2 = \frac1B$ is feasible with cost $\frac1B$. So the [integrality gap](/integrality-gap/) is at least $B$, without limit.

*Knapsack cover inequalities fix it.* For a set $S$ of items with $\sum_{j \in S} a_j < b$, the residual demand is $b_S = b - \sum_{j \in S} a_j$, and each feasible 0/1 vector satisfies

$$\sum_{j \notin S} \min(a_j, b_S)\, x_j \ \ge\ b_S.$$

Indeed, if some $j \notin S$ with $a_j \ge b_S$ has $x_j = 1$, the left side is at least $b_S$; otherwise the items outside $S$ that are chosen must give at least $b_S$ in full. In the example, $S = \{1\}$ gives $b_S = 1$ and the inequality $x_2 \ge 1$, so the strengthened LP has optimum 1.

## Known algorithms

- **Greedy.** Repeatedly buy the option with the least cost for each unit of remaining demand that it meets, counting each row only up to its residual demand. For integer data this gives ratio $H(\max_j \sum_i a_{ij})$, a harmonic number, as for [greedy set cover](/greedy-set-cover/) (Dobson 1982).
- **Scaled randomized rounding.** Solve the LP to get $x^*$, take $\lambda \ge 1$, and set $X_j = \lfloor \lambda x^*_j \rfloor + Y_j$, where $Y_j$ is 1 with probability equal to the fractional part of $\lambda x^*_j$, independently. Then $\mathbb{E}[X_j] = \lambda x^*_j$.
  *Theorem.* Let $A \in \{0, 1\}^{m \times n}$, $b \in \mathbb{Z}_{\ge 1}^m$, no upper bounds, and $\lambda = \max(2, 8 \ln(4m))$. With probability at least $\frac14$, $X$ is feasible and $c^\top X \le 2\lambda\,\mathrm{LP}^*$. So the ratio is $O(\log m)$.
  *Proof.* Fix a row $i$, and let $D = \sum_j a_{ij} \lfloor \lambda x^*_j \rfloor$, an integer. If $D \ge b_i$, the row holds. Otherwise $t = b_i - D \ge 1$ is an integer, and the row fails exactly when $R = \sum_j a_{ij} Y_j < t$. $R$ is a sum of independent 0/1 variables with mean $\mu = \lambda (A x^*)_i - D \ge \lambda b_i - D \ge \lambda t$, because $\lambda \ge 1$. So $t \le \mu / \lambda \le \mu / 2$, and the lower tail [Chernoff bound](/chernoff-bound/) gives $\Pr[R < t] \le \Pr[R \le \frac{\mu}{2}] \le e^{-\mu/8} \le e^{-\lambda t / 8} \le e^{-\lambda/8} \le \frac{1}{4m}$. By the union bound, some row fails with probability at most $\frac14$. Also $\mathbb{E}[c^\top X] = \lambda\,\mathrm{LP}^*$, so by Markov's inequality $\Pr[c^\top X > 2\lambda\,\mathrm{LP}^*] \le \frac12$. Both good events hold with probability at least $1 - \frac14 - \frac12 = \frac14$. $\square$
- **Bounds in terms of $B$.** Srinivasan (1999) gives ratio $1 + O\bigl(\max(\frac{\ln m}{B}, \sqrt{\frac{\ln m}{B}})\bigr)$ for the case without upper bounds, so the ratio tends to 1 as $B$ grows compared with $\ln m$.
- **Knapsack cover inequalities.** With them, Carr, Fleischer, Leung and Phillips (2000) give a 2-approximation for minimum knapsack and a primal-dual algorithm with ratio equal to the largest number of nonzero entries in a row. Kolliopoulos and Young (2005) give a logarithmic ratio for CIPs with multiplicity constraints.
- **Primal-dual and local ratio.** For row sparse CIPs, the [primal-dual method](/primal-dual-approximation/) and the [local ratio technique](/local-ratio-technique/) give ratio $f$, as for [set cover by frequency](/frequency-rounding-set-cover/).

## Bounds

| claim | statement | source |
|---|---|---|
| lower bound used | $\mathrm{OPT} \ge \mathrm{LP}^*$ | LP relaxation |
| rounding, no upper bounds | ratio $O(\log m)$ | proved above for 0/1 matrices; Srinivasan 1999 in general |
| greedy | ratio $H(\max_j \sum_i a_{ij})$ for integer data | Dobson 1982 |
| natural LP, 0/1 variables | integrality gap without limit | example above |
| minimum knapsack | ratio 2 with knapsack cover inequalities | Carr, Fleischer, Leung and Phillips 2000 |
| hardness | no ratio $(1 - \varepsilon) \ln m$ unless P = NP | from [set cover](/set-cover/) (Dinur and Steurer 2014) |

## Reductions

- **From set cover.** One variable for each set and the row $\sum_{S \ni u} x_S \ge 1$ for each element $u$. So the hardness of set cover applies: no polynomial-time ratio $(1 - \varepsilon) \ln m$ unless P = NP.
- **From vertex cover.** One variable for each vertex and the row $x_u + x_v \ge 1$ for each edge.
- **From minimum knapsack.** One row with 0/1 variables; the problem is NP-hard by a reduction from [subset sum](/subset-sum-problem/), and it has an FPTAS by dynamic programming over costs.
- **Duality with packing.** By [LP duality](/lp-duality/), the covering LP and the packing LP with the transposed matrix have the same optimum; primal-dual algorithms build a covering solution and a packing dual together.

## Applications

- **Diet and blending.** Buy foods so that each nutrient reaches its required amount, at least cost.
- **Facility placement with coverage demands.** Open facilities so that each client is covered a required number of times, for fault tolerance.
- **Network design.** Buy capacity on edges so that each cut carries its demand; the knapsack cover inequalities were first used for capacitated network design.
- **Staffing.** Choose shifts so that each time slot has at least its required number of workers.

## References
