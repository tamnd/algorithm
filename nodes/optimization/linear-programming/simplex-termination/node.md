---
tag: Y1TH32
kind: theorem
slug: simplex-termination
name: Simplex termination
aliases:
- finiteness of the simplex method
- Bland's anticycling theorem
area: optimization/linear-programming
level: advanced
summary: Result that simplex either terminates or cycles, and that a suitable pivot rule such as Bland's rule prevents cycling.
prereqs: [simplex-method, pivot-operation, ratio-test, reduced-cost]
see_also: [bland-rule, lp-degeneracy, ratio-test, dantzig-pivot-rule, fundamental-theorem-of-lp, strong-duality, klee-minty-cube, two-phase-simplex-method]
sources:
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pages 103 to 107, the least-index rule and the proof that it does not cycle
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.2, Development of the simplex method (termination without degeneracy) and Section 3.4, Anticycling (lexicography and Bland's rule)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 3, Pitfalls and how to avoid them (cycling, the perturbation method, the smallest subscript rule and the proof of its finiteness)
  - paper: doi:10.2140/pjm.1955.5.183
    title: George B. Dantzig, Alex Orden and Philip Wolfe, The generalized simplex method for minimizing a linear form under linear inequality restraints, Pacific Journal of Mathematics 5(2), 1955
    locator: pages 183 to 195, the lexicographic rule
  - paper: doi:10.1002/nav.3800020406
    title: E. M. L. Beale, Cycling in the dual simplex algorithm, Naval Research Logistics Quarterly 2(4), 1955
    locator: pages 269 to 275, the cycling example
---

The simplex termination theorem says when the [simplex method](/simplex-method/) is sure to stop. Without degenerate pivots, every pivot rule stops after at most $\binom{n}{m}$ pivots. With degenerate pivots a rule can return to an earlier basis and cycle for ever, but with [Bland's rule](/bland-rule/) or the lexicographic [ratio test](/ratio-test/) no basis repeats, so the method always stops. At the stop it has an optimal basis or a certificate that the program is unbounded, which gives a constructive proof of the [fundamental theorem of linear programming](/fundamental-theorem-of-lp/).

## Statement

Let $A \in \mathbb{R}^{m \times n}$ have rank $m$, and consider the program minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$. Run the simplex method from a feasible basis. In each iteration, if all [reduced costs](/reduced-cost/) $r_j = c_j - c_B^\top B^{-1}A_j$ are nonnegative, stop with OPTIMAL. Otherwise choose $q$ with $r_q < 0$ and let $d = B^{-1}A_q$. If $d \le 0$, stop with UNBOUNDED. Otherwise pivot on a row $p$ chosen by the minimum ratio test.

**Theorem.**

1. *(Correct stops.)* If the method stops with OPTIMAL, the basic solution is optimal. If it stops with UNBOUNDED, the objective is unbounded below on the feasible set.
2. *(Nondegenerate programs.)* If every basic feasible solution of the program is nondegenerate, the method stops after at most $\binom{n}{m} - 1$ pivots for every choice of $q$ with $r_q < 0$.
3. *(Bland's rule.)* If $q$ is the smallest index with $r_q < 0$, and $p$ is a row of the ratio test whose basic variable has the smallest index among the tied rows, then no basis repeats, and the method stops after at most $\binom{n}{m} - 1$ pivots.
4. *(Lexicographic rule.)* If the start basis has every row of $[\,x_B \mid B^{-1}\,]$ lexicographically positive, and $p$ is the row with the lexicographically least $\frac{1}{d_p}[\,x_{B(p)} \mid (B^{-1})_{p}\,]$ among the rows with $d_p > 0$, then no basis repeats, for every choice of $q$ with $r_q < 0$.

## In plain words

Each step of the simplex method moves from one corner description, a basis, to the next. There are only finitely many bases. So the method can run for ever only if it comes back to a basis it has already seen.

If each step strictly lowers the cost, it can never come back, since the cost of a basis is fixed. Steps that do not move are the only danger; they happen at crowded corners, and with an unlucky rule the method can go round a loop of such steps without end.

The theorem says that two simple tie rules close this gap. One always picks the candidate with the smallest number. The other compares candidates by a fixed list of tie-breakers. With either rule the method cannot loop, so it always ends, and when it ends its answer is right.

## Proof

**Part 1.** For every feasible $x$, $Ax = b$ gives $x_B = B^{-1}b - B^{-1}A_N x_N$, so
$$c^\top x = c_B^\top B^{-1} b + \sum_{j \notin B} r_j x_j.$$
If $r \ge 0$, then $c^\top x \ge c_B^\top B^{-1}b$, the value of the basic solution, which is therefore optimal. If $r_q < 0$ and $d \le 0$, the points $x(\theta)$ with $x_q = \theta$, $x_B = B^{-1}b - \theta d$ and the other nonbasic variables $0$ are feasible for all $\theta \ge 0$, and their value is $c_B^\top B^{-1}b + \theta r_q \to -\infty$.

**Part 2.** A pivot with step $\theta^* = \min_{d_i > 0} x_{B(i)}/d_i$ changes the value by $\theta^* r_q$. If the basic solution is nondegenerate, $\theta^* > 0$, so the value strictly decreases. The value is a function of the basis, so no basis appears twice. There are at most $\binom{n}{m}$ bases, so at most $\binom{n}{m}$ bases are visited and at most $\binom{n}{m} - 1$ pivots are made.

**Part 3.** The bound follows as in Part 2 once no basis repeats, so assume, to get a contradiction, that the bases $B^0, B^1, \ldots, B^k = B^0$ form a cycle under Bland's rule.

*All pivots in the cycle are degenerate.* The value never increases along the cycle and comes back to its start value, so every pivot has $\theta^* r_q = 0$, so $\theta^* = 0$. Then the basic solution $x$ is the same point for all bases of the cycle.

*The fickle variables.* Call $x_j$ fickle if it is basic in some $B^i$ and nonbasic in another. Each fickle variable is nonbasic at some basis of the cycle, so $x_j = 0$. Let $t$ be the largest fickle index. Since the cycle is closed, $x_t$ leaves at some pivot and enters at another. Let $B$ be a basis of the cycle at which $x_t$ leaves, let $x_s$ be the variable that enters there, and let $B'$ be a basis of the cycle at which $x_t$ enters. Then $s$ is fickle and $s \ne t$, so $s < t$.

*At $B'$.* Bland's rule chose $t$, so $r'_t < 0$ and $r'_j \ge 0$ for all $j < t$, where $r'$ are the reduced costs at $B'$.

*At $B$.* Let $d = B^{-1}A_s$ and let $\delta \in \mathbb{R}^n$ be the edge direction of $x_s$: $\delta_s = 1$, $\delta_{B(i)} = -d_i$, and $\delta_j = 0$ for the other $j$. Then $A\delta = 0$ and $c^\top \delta = r_s < 0$. The reduced costs at $B'$ are $r' = c - A^\top y'$ with $y' = (B')^{-\top} c_{B'}$, so
$$\sum_j r'_j \delta_j = c^\top \delta - y'^\top A \delta = r_s < 0.$$
So there is an index $j$ with $r'_j \delta_j < 0$.

*That index.* First, $j \ne t$: $x_t$ is the basic variable of the pivot row $p$ at $B$, so $\delta_t = -d_p < 0$, and $r'_t < 0$, so $r'_t \delta_t > 0$. Next, $r'_j \ne 0$ means that $j$ is nonbasic at $B'$, and $\delta_j \ne 0$ means that $j = s$ or $j$ is basic at $B$. In both cases $j$ is fickle ($s$ is fickle, and a variable basic at $B$ and nonbasic at $B'$ is fickle). So $j < t$, and then $r'_j \ge 0$, so $r'_j > 0$ and $\delta_j < 0$. As $\delta_s = 1$, $j \ne s$, so $j = B(i)$ for a row $i$ with $d_i = -\delta_j > 0$.

*The contradiction.* Row $i$ has $d_i > 0$ and $x_{B(i)} = x_j = 0$, because $j$ is fickle. So its ratio is $0 = \theta^*$, and row $i$ was tied with row $p$ in the ratio test at $B$. Since $j < t$, Bland's rule would have chosen $x_j$ to leave, not $x_t$. So there is no cycle.

**Part 4.** Write $u_i = [\,x_{B(i)} \mid (B^{-1})_i\,]$ for row $i$ of the extended tableau, and $u_0 = [\,-c_B^\top B^{-1}b \mid -c_B^\top B^{-1}\,]$ for its cost row. These are the rows of the tableau of the program with $m$ extra columns $I$ of cost $0$, so a pivot on $(p, q)$ updates them as tableau rows: $u'_p = u_p / d_p$, $u'_i = u_i - d_i u_p / d_p$ for $i \ne p$, and $u'_0 = u_0 - r_q u_p / d_p$.

*The choice is unique.* If $u_i/d_i = u_k/d_k$ for rows $i \ne k$, then rows $i$ and $k$ of $B^{-1}$ are proportional, which is impossible for a nonsingular matrix.

*The rows stay lexicographically positive.* $u'_p = u_p/d_p$ is positive since $d_p > 0$. For $i \ne p$ with $d_i \le 0$, $u'_i = u_i + |d_i|\, u_p/d_p$ is a sum of a positive vector and a nonnegative multiple of a positive vector. For $i \ne p$ with $d_i > 0$, the rule gives $u_p/d_p <_{\text{lex}} u_i/d_i$ strictly, so $u'_i = d_i (u_i/d_i - u_p/d_p)$ is positive.

*The cost row strictly increases.* $u'_0 - u_0 = (-r_q/d_p)\, u_p$ is a positive multiple of a lexicographically positive vector. So $u_0$ strictly increases in the lexicographic order at each pivot. Since $u_0$ is a function of the basis, no basis repeats. $\blacksquare$

## Consequences

- **The fundamental theorem.** Run [phase one](/two-phase-simplex-method/) and then phase two with Bland's rule. The method stops, so every program in standard form is infeasible, unbounded, or has an optimal basic feasible solution. This is the [fundamental theorem of LP](/fundamental-theorem-of-lp/).
- **Strong duality.** At an OPTIMAL stop, $y = B^{-\top}c_B$ satisfies $A^\top y \le c$ (since $r \ge 0$) and $b^\top y = c_B^\top B^{-1}b$. So the simplex method with an anticycling rule proves [strong duality](/strong-duality/) and gives an optimal dual solution.
- **Exact solvers.** In rational arithmetic, cycling is a real danger, and these rules are the standard guard. A common scheme uses a fast rule and switches to Bland's rule after a long run of degenerate pivots.
- **Other methods.** The same least-index argument proves that the [dual simplex method](/dual-simplex-method/) with the dual least-index rule stops, and that the perturbation of $b$ by $(\varepsilon, \ldots, \varepsilon^m)$ is the lexicographic rule in disguise.

## Tightness

- **A rule is needed.** On Beale's program, minimize $-\frac34 x_4 + 20x_5 - \frac12 x_6 + 6x_7$ subject to $x_1 + \frac14 x_4 - 8x_5 - x_6 + 9x_7 = 0$, $x_2 + \frac12 x_4 - 12x_5 - \frac12 x_6 + 3x_7 = 0$, $x_3 + x_6 = 1$, $x \ge 0$, [Dantzig's rule](/dantzig-pivot-rule/), with the smallest index on ties in the ratio test, makes these six pivots of step $0$ and returns to the start:

| pivot | enters | leaves | new basis |
|---|---|---|---|
| 1 | $x_4$ | $x_1$ | $\{x_2, x_3, x_4\}$ |
| 2 | $x_5$ | $x_2$ | $\{x_3, x_4, x_5\}$ |
| 3 | $x_6$ | $x_4$ | $\{x_3, x_5, x_6\}$ |
| 4 | $x_7$ | $x_5$ | $\{x_3, x_6, x_7\}$ |
| 5 | $x_1$ | $x_6$ | $\{x_1, x_3, x_7\}$ |
| 6 | $x_2$ | $x_7$ | $\{x_1, x_2, x_3\}$ |

In the terms of the proof, the fickle variables are $x_1, x_2, x_4, x_5, x_6, x_7$, so $t = 7$, and $x_7$ enters at the basis $B' = \{x_3, x_5, x_6\}$. There $r'_1 = -2 < 0$ and $r'_7 = -3$: Dantzig's rule takes $x_7$ where Bland's rule takes $x_1$. With Bland's rule, the method leaves the degenerate vertex at the fifth pivot and reaches the optimum $-5/4$ at $x = (\frac34, 0, 0, 1, 0, 1, 0)$ after six pivots.

- **Finite is not fast.** The bound $\binom{n}{m} - 1$ is exponential, and it is the right order for some rules: on the [Klee-Minty cube](/klee-minty-cube/) with $n$ variables and $n$ slacks, Dantzig's rule makes $2^n - 1$ nondegenerate pivots, and Avis and Chvátal (1978) gave programs on which Bland's rule also makes exponentially many pivots. No pivot rule is known that is polynomial on all programs.
- **Both parts of Bland's rule matter.** The argument uses the least index both for the entering variable (at $B'$) and for the leaving variable (at $B$). Beale's example shows that the smallest-index tie rule in the ratio test alone does not prevent cycling.

## History

Hoffman gave the first example of cycling in 1953, and Beale (1955) gave the smaller example above. Charnes (1952) proposed the perturbation of the right-hand side, and Dantzig, Orden and Wolfe (1955) the lexicographic rule, which is its exact form. In practice cycling was so rare that codes ignored it for decades. Bland (1977) found the least-index rule and its short proof while he studied pivoting in oriented matroids, where only the signs of the entries count.

## References
