---
tag: 7JEBVX
kind: concept
slug: dantzig-pivot-rule
name: Dantzig's pivot rule
aliases:
- largest coefficient rule
- most negative reduced cost rule
- textbook pivot rule
area: optimization/linear-programming
level: core
summary: Enter the nonbasic variable with the most favorable reduced cost.
prereqs: [simplex-method, reduced-cost, pivot-operation]
see_also: [bland-rule, steepest-edge-pivot-rule, klee-minty-cube, lp-degeneracy, ratio-test, simplex-termination, smoothed-simplex-analysis, revised-simplex-method]
sources:
  - paper: "George B. Dantzig, Maximization of a linear function of variables subject to linear inequalities, in T. C. Koopmans (ed.), Activity Analysis of Production and Allocation, Cowles Commission Monograph 13, Wiley, 1951"
    locator: Chapter XXI, the simplex method with the choice of the largest coefficient
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.2, Development of the simplex method (pivoting rules) and Section 3.7, Computational efficiency of the simplex method
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 3, Pitfalls and how to avoid them (the largest coefficient rule and cycling) and Chapter 4, How fast is the simplex method (the Klee-Minty examples)
  - paper: "Victor Klee and George J. Minty, How good is the simplex algorithm?, in O. Shisha (ed.), Inequalities III, Academic Press, 1972"
    locator: pages 159 to 175, the exponential example for this rule
  - paper: doi:10.1002/nav.3800020406
    title: E. M. L. Beale, Cycling in the dual simplex algorithm, Naval Research Logistics Quarterly 2(4), 1955
    locator: pages 269 to 275, the cycling example
  - paper: doi:10.1016/0012-365X(73)90171-4
    title: Robert G. Jeroslow, The simplex algorithm with the pivot rule of maximizing criterion improvement, Discrete Mathematics 4(4), 1973
    locator: pages 367 to 377, exponential examples for the largest improvement rule
---

Dantzig's pivot rule chooses, in each iteration of the [simplex method](/simplex-method/), the entering variable with the most negative [reduced cost](/reduced-cost/) (for a minimization). It is the rule of Dantzig's first account of the method in 1951 and the rule of most textbooks. It is cheap and often good in practice, but it depends on the scaling of the variables, it can cycle on [degenerate](/lp-degeneracy/) programs, and on the [Klee-Minty cube](/klee-minty-cube/) it takes $2^n - 1$ pivots.

## In plain words

At a corner of the feasible region, each variable outside the basis gives one edge to walk along, and its reduced cost says how fast the objective improves per unit of that variable. Dantzig's rule takes the edge with the fastest rate. It looks only at the rate, not at how far the walk can go, and the rate depends on the unit in which the variable is measured.

Most of the time this greedy choice works well. But one can build regions where it walks through every corner of a squashed cube before it reaches the best one, and degenerate corners where it goes round a loop of bases for ever.

## The idea

**The rule.** The program is minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$, with a feasible basis $B$ and reduced costs $r_j = c_j - c_B^\top B^{-1} A_j$. If $r \ge 0$, the basis is optimal. Otherwise enter
$$q \in \arg\min_j r_j,$$
with ties broken by the smallest index $j$ in most codes. The leaving variable comes from the [ratio test](/ratio-test/).

**What the reduced cost measures.** Increasing $x_q$ by $\theta$ along its edge changes the objective by $\theta r_q$. So $r_q$ is the improvement per unit of $x_q$. The total improvement of the pivot is $\theta^* r_q$, where $\theta^*$ is the step length of the ratio test. The rule that maximizes $|\theta^* r_q|$ is the *largest improvement rule*. It needs a ratio test for every candidate, and Jeroslow (1973) showed that it also takes exponentially many pivots on some programs.

**Scaling.** Replace $x_j$ by $x_j = s\, x'_j$ with $s > 0$. The column becomes $s A_j$, the cost $s c_j$, and the reduced cost $s\, r_j$. So the rule can choose a different column after a change of units, while the program and its optimal points stay the same. The [steepest-edge rule](/steepest-edge-pivot-rule/) divides $r_j$ by the length of the edge direction to remove most of this effect.

**Termination.** With degenerate pivots the rule can return to a basis it has seen before, and then it cycles for ever. In exact arithmetic, a tie rule such as [Bland's rule](/bland-rule/) or the lexicographic ratio test is needed for a guarantee; see [simplex termination](/simplex-termination/). In floating point, cycling is rare, and codes use small perturbations of $b$ instead.

**Cost of one choice.** With all reduced costs at hand, the choice costs $O(n)$. In the [revised simplex method](/revised-simplex-method/), computing all $r_j$ costs one solve with $B^\top$ and one product with each nonbasic column. *Partial pricing* scans only a part of the columns and takes the most negative there, which saves time on programs with many columns.

## Examples

**The effect of units.** Minimize $-3x_1 - 2x_2$ subject to $x_1 + 2x_2 \le 4$, $3x_1 + x_2 \le 6$, $x \ge 0$. At the slack basis, $r = (-3, -2)$, so the rule enters $x_1$. Now measure $x_2$ in tenths: $x_2 = 10 x_2'$. The program is the same, but the column of $x_2'$ is $(20, 10)$ with cost $-20$, so $r = (-3, -20)$, and the rule enters $x_2'$. The steepest-edge rule compares $r_j^2 / (1 + \|B^{-1}A_j\|^2)$, which is $9/11$ for $x_1$ against $4/6$ for $x_2$, and $9/11$ against $400/501$ for $x_2'$, so it enters $x_1$ both times.

**The Klee-Minty cube.** Minimize $-\sum_{j=1}^{n} 10^{n-j} x_j$ subject to $2\sum_{j<i} 10^{i-j} x_j + x_i \le 100^{i-1}$ for $i = 1, \ldots, n$ and $x \ge 0$, starting from the slack basis. Dantzig's rule visits all $2^n$ vertices:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Dantzig's rule | 1 | 3 | 7 | 15 | 31 | 63 | 127 | 255 | 511 | 1023 |
| steepest edge | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

For $n = 3$ the path is $(0,0,0)$, $(1,0,0)$, $(1,80,0)$, $(0,100,0)$, $(0,100,8000)$, $(1,80,8200)$, $(1,0,9800)$, $(0,0,10000)$. The [Klee-Minty page](/klee-minty-cube/) has the proof of the count.

**Cycling.** On Beale's program in seven variables (minimize $-\frac34 x_4 + 20x_5 - \frac12 x_6 + 6x_7$ subject to $x_1 + \frac14 x_4 - 8x_5 - x_6 + 9x_7 = 0$, $x_2 + \frac12 x_4 - 12x_5 - \frac12 x_6 + 3x_7 = 0$, $x_3 + x_6 = 1$, $x \ge 0$), Dantzig's rule with the smallest-index tie rule in the ratio test enters $x_4, x_5, x_6, x_7, x_1, x_2$ in turn, all with step $0$, and is back at the start basis $\{x_1, x_2, x_3\}$ after six pivots. The optimum is $-5/4$ at $x = (\frac34, 0, 0, 1, 0, 1, 0)$, which [Bland's rule](/bland-rule/) reaches in six pivots.

## Where it is used

- **Textbooks and teaching codes.** It is the default rule in most first courses and in many small implementations.
- **Large codes, with changes.** Production solvers prefer [steepest edge](/steepest-edge-pivot-rule/) or its approximation Devex for the primal and dual simplex, and fall back to partial pricing with Dantzig's choice when pricing all columns is too costly, for example in [column generation](/column-generation/), where the most negative reduced cost is exactly what the pricing problem returns.
- **Theory.** It is the rule of the first exponential lower bound, the [Klee-Minty cube](/klee-minty-cube/), and the start of the search for a polynomial pivot rule, which is still open and is tied to the [Hirsch conjecture](/hirsch-conjecture/).

## References
