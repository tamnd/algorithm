---
title: The best of the 2^|P| direction LPs is an optimal L1 controlled adjustment
proves: [correctness]
status: full
---

The input is a table $a \in \mathbb{R}^n$ with $M a = 0$, bounds $lb \le a \le ub$, weights $w \ge 0$, and a set $P$ of sensitive cells with levels $LPL_p, UPL_p \ge 0$. Lines L1 to L8 are those of the page. An *adjustment* is a vector $y \in \mathbb{R}^n$. It is *feasible* if $M y = 0$ and $lb \le a + y \le ub$, and it *protects* $P$ if, for each $p \in P$, $y_p \ge UPL_p$ or $y_p \le -LPL_p$. The problem is to find a feasible adjustment that protects $P$ and has the least cost $c(y) = \sum_i w_i |y_i|$.

For a direction vector $d \in \{\text{down}, \text{up}\}^P$, let $Y_d$ be the set of feasible adjustments with $y_p \ge UPL_p$ for each $p$ with $d_p = \text{up}$ and $y_p \le -LPL_p$ for each $p$ with $d_p = \text{down}$. Let $L_d$ be the linear program of lines L3 to L5: minimize $\sum_i w_i (z^+_i + z^-_i)$ subject to $M (z^+ - z^-) = 0$, $0 \le z^+ \le ub - a$, $0 \le z^- \le a - lb$, and, for each $p \in P$, $z^+_p \ge UPL_p$ and $z^-_p = 0$ if $d_p = \text{up}$, or $z^-_p \ge LPL_p$ and $z^+_p = 0$ if $d_p = \text{down}$.

**Lemma 1 (from the LP to a table).** If $(z^+, z^-)$ is feasible for $L_d$, then $y = z^+ - z^-$ is in $Y_d$ and $c(y) \le \sum_i w_i (z^+_i + z^-_i)$.

*Proof.* $M y = 0$ by the first constraint. For each cell, $a_i + y_i \le a_i + z^+_i \le ub_i$ and $a_i + y_i \ge a_i - z^-_i \ge lb_i$, so $y$ is feasible. If $d_p = \text{up}$, then $z^-_p = 0$ and $y_p = z^+_p \ge UPL_p$. If $d_p = \text{down}$, then $z^+_p = 0$ and $y_p = -z^-_p \le -LPL_p$. So $y \in Y_d$. Finally $|y_i| = |z^+_i - z^-_i| \le z^+_i + z^-_i$, and $w_i \ge 0$. $\square$

**Lemma 2 (from a table to the LP).** If $y \in Y_d$, then $z^+ = \max(y, 0)$ and $z^- = \max(-y, 0)$, taken entry by entry, are feasible for $L_d$ with value $c(y)$.

*Proof.* $z^+ - z^- = y$, so $M (z^+ - z^-) = 0$. If $y_i \ge 0$, then $z^+_i = y_i \le ub_i - a_i$ and $z^-_i = 0 \le a_i - lb_i$, because $a + y \le ub$ and $lb \le a$. The case $y_i < 0$ is the same with the roles exchanged. If $d_p = \text{up}$, then $y_p \ge UPL_p \ge 0$, so $z^+_p = y_p \ge UPL_p$ and $z^-_p = 0$. If $d_p = \text{down}$, then $y_p \le -LPL_p \le 0$, so $z^-_p = -y_p \ge LPL_p$ and $z^+_p = 0$. The value is $\sum_i w_i (z^+_i + z^-_i) = \sum_i w_i |y_i| = c(y)$. $\square$

**Theorem 1 (one direction).** $L_d$ is feasible if and only if $Y_d$ is not empty. Then its optimal value equals $\min \{ c(y) : y \in Y_d \}$, and if $(z^+, z^-)$ is optimal for $L_d$, the adjustment $z^+ - z^-$ reaches this minimum.

*Proof.* Feasibility goes both ways by Lemmas 1 and 2. The program has a finite optimum because it is feasible and its objective is at least 0. Let $v$ be the optimal value and $(z^+, z^-)$ an optimal solution, and let $y^* = z^+ - z^-$. By Lemma 1, $y^* \in Y_d$ and $c(y^*) \le v$. For each $y \in Y_d$, Lemma 2 gives a feasible point of value $c(y)$, so $v \le c(y)$. With $y = y^*$ this gives $v \le c(y^*) \le v$, and for every $y \in Y_d$ it gives $c(y^*) = v \le c(y)$. $\square$

**Theorem 2 (the algorithm).** If line L7 returns infeasible, no feasible adjustment protects $P$. Otherwise line L8 returns $x = a + y$ where $y$ is feasible, protects $P$, and has the least cost among all such adjustments.

*Proof.* An adjustment protects $P$ if and only if it lies in $Y_d$ for some $d$: choose $d_p = \text{up}$ when $y_p \ge UPL_p$ and $d_p = \text{down}$ otherwise. So the set of feasible protecting adjustments is the union of the $2^{|P|}$ sets $Y_d$. Line L2 visits every $d$. By Theorem 1, the LP of line L5 is infeasible exactly when $Y_d$ is empty. If it is infeasible for every $d$, the union is empty and line L7 is correct. Otherwise, line L6 keeps a solution of the least value over the feasible $d$, and by Theorem 1 that value is $\min_d \min_{y \in Y_d} c(y)$, the least cost over the union. The kept adjustment is in its $Y_d$, so it is feasible and protects $P$. $\square$

**Theorem 3 (the LP solver).** The implementation solves each $L_d$ by a primal simplex method with bounds on the variables. After the substitution $z \leftarrow z - \ell$ for the lower bounds $\ell$ of line L4, every variable lies in $[0, u_j]$ with $u_j$ possibly infinite. Phase 1 adds one artificial variable per row, starts from the basis of the artificials, and minimizes their sum. If the minimum is positive, the system has no solution. Otherwise phase 2 sets the upper bound of each artificial to 0 and minimizes the objective of $L_d$ from the final basis of phase 1.

*Proof sketch.* Phase 1 starts from a feasible basis: the rows are multiplied by $-1$ where needed so that the right side is at least 0, and then the artificials equal the right side. Each pivot keeps all variables within their bounds, because the ratio test takes the least step at which a basic variable or the entering variable reaches a bound. When no nonbasic variable has a reduced cost of the right sign, the basis is optimal by the usual optimality test for bounded variables. With Bland's rule, the entering variable is the first eligible one, and on a tie in the ratio test the leaving variable has the least index, so no basis repeats, and both phases end after finitely many pivots. This is Bland's theorem, extended to bounds on the variables in the standard way. A step in which the entering variable moves to its other bound changes no basis. A variable at its lower bound enters only if its range is positive, so such a step strictly lowers the objective and cannot be part of a cycle. The sum of the artificials is 0 after phase 1 if and only if the system has a solution. In phase 2 their upper bound is 0, so every point of phase 2 is a solution of the original system. The objective of $L_d$ is bounded below by the shifted constant, because $w \ge 0$, so phase 2 cannot report an unbounded program. $\blacksquare$

**Remark.** With exact rational arithmetic the implementation follows the proof exactly. With floating-point arithmetic and a tolerance, the result is an approximation, and the test file compares it with a brute force on small tables.
