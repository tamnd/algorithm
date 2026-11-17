---
title: FVA returns the exact range of each flux over the near-optimal flux set
proves: [correctness]
status: full
---

Fix an $n \times m$ matrix $S$, bounds $lb \le ub$ (entries may be infinite), an objective $c \in \mathbb{Q}^m$ and a fraction $f \in [0, 1] \cap \mathbb{Q}$. Write $P = \{v : S v = 0, \; lb \le v \le ub\}$. Assume that the FBA problem $\max_P c^{\mathsf T} v$ has a finite optimum $z$; otherwise the code raises an error at line L1 and returns nothing. Let $t = z - (1 - f) |z|$ and

$$P_f = \{v \in P : c^{\mathsf T} v \ge t\} .$$

For each reaction $j$, the claim is that the code returns $(lo_j, hi_j)$ with $lo_j = \min_{P_f} v_j$ and $hi_j = \max_{P_f} v_j$, where None stands for $-\infty$ or $+\infty$ when the minimum or the maximum does not exist, and that every value strictly between $lo_j$ and $hi_j$ (and each finite end) is the flux $v_j$ of some $v \in P_f$.

**Lemma 1 (the LP solver).** For a rational LP $\min$ or $\max$ of $c^{\mathsf T} x$ subject to $A_{eq} x = b_{eq}$, $A_{le} x \le b_{le}$ and $lb \le x \le ub$, solve_lp returns "infeasible" if the feasible set is empty, "unbounded" if the objective has no finite optimum on a non-empty feasible set, and otherwise an optimal $x$ and its value.

*Proof.* solve_lp makes the same change of variables as lines L1 to L4 of FBA (lower bound offset, reflection for an upper bound only, a split for a free variable, a slack row for each pair of finite bounds), and adds one slack $s_i \ge 0$ for each row of $A_{le}$, which turns $a_i^{\mathsf T} x \le b_i$ into $a_i^{\mathsf T} x + s_i = b_i$. A maximization is the minimization of $-c^{\mathsf T} x$. By Lemma 1 of the correctness proof of flux balance analysis, extended by the slack rows in the same way as the bound rows, the feasible set of the new standard form LP maps onto the feasible set of the original LP, and the objectives differ by a constant and a sign. Lemmas 2 to 4 of that proof show that simplex_standard returns the right status and an optimum of the standard form. The status and the optimum carry over as in the theorem there. $\square$

**Lemma 2 (the set is not empty).** $t \le z$, and the FBA optimum $v^*$ of line L1 is in $P_f$. So no LP of lines L4 and L5 is infeasible.

*Proof.* $1 - f \ge 0$ and $|z| \ge 0$, so $t = z - (1 - f)|z| \le z = c^{\mathsf T} v^*$, and $v^* \in P$. $\square$

**Lemma 3 (the ranges).** For each $j$, line L4 returns $\min_{P_f} v_j$ if it exists, and None otherwise. Line L5 returns $\max_{P_f} v_j$ if it exists, and None otherwise.

*Proof.* Line L4 calls solve_lp with the objective $e_j$, the rows $S v = 0$, the single row $-c^{\mathsf T} v \le -t$ (that is, $c^{\mathsf T} v \ge t$) and the bounds $lb, ub$. Its feasible set is exactly $P_f$. By Lemma 2 it is not empty, so by Lemma 1 the status is "optimal" with the value $\min_{P_f} v_j$, or "unbounded" when $v_j$ has no lower bound on $P_f$. Line L6 stores the value or None. A linear function bounded below on a non-empty polyhedron attains its minimum there (a standard fact of linear programming, which also follows from the simplex method of Lemma 1, which stops at an optimal basis whenever the LP is bounded). So "the minimum does not exist" and "unbounded" are the same case. Line L5 is the same with maximize. $\square$

**Lemma 4 (every value in the range is attained).** If $lo_j \le x \le hi_j$, with finite $x$, then some $v \in P_f$ has $v_j = x$.

*Proof.* $P_f$ is an intersection of half spaces and hyperplanes, so it is convex. If both ends are finite, take $v^{lo}, v^{hi} \in P_f$ with $v^{lo}_j = lo_j$ and $v^{hi}_j = hi_j$ (they exist by Lemma 3), and a point $\lambda v^{lo} + (1 - \lambda) v^{hi}$ on the segment between them with the flux $x$. If an end is infinite, take a point of $P_f$ with $v_j$ beyond $x$ on that side, which exists because $v_j$ is unbounded there, and the same segment argument applies. $\square$

**Theorem.** For $0 \le f \le 1$, fva returns the optimum $z$ and, for each reaction $j$ in the list, the exact interval $\{v_j : v \in P_f\}$, with None for an infinite end. For $f = 1$, $t = z$, and $P_1$ is the set of optimal flux vectors of the FBA problem, so the ranges are the ranges of the fluxes over all FBA optima.

*Proof.* Lemmas 2 to 4. For $f = 1$, $t = z$, and $v \in P$ with $c^{\mathsf T} v \ge z$ means $c^{\mathsf T} v = z$, since $z$ is the maximum. $\square$

**Remark (the threshold for a negative optimum).** The code uses $|z|$ in $t$. If $z \ge 0$, then $t = f z$, the usual "at least the fraction $f$ of the optimum". If $z < 0$, then $t = z - (1 - f)(-z) = (2 - f) z \le z$, which still loosens the constraint as $f$ decreases. The form $t = f z$ would instead make the constraint stricter than the optimum when $z < 0$ and $f < 1$, and then $P_f$ would be empty. Lemma 2 needs only $t \le z$, which holds for both signs of $z$.

**Remark (blocked reactions).** blocked_reactions calls fva with $c = 0$. Then $z = 0$ whenever $P$ is not empty, $t = 0$, and $P_f = P$. A reaction is reported as blocked exactly when its range over $P$ is $[0, 0]$, that is, when $v_j = 0$ for every steady state that obeys the bounds.
