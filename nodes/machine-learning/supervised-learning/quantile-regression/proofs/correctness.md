---
title: The simplex method on the quantile linear program returns a regression quantile, and some optimum interpolates d points
proves: [correctness, termination]
status: full
---

Let $X \in \mathbb{R}^{n \times d}$ have rows $x_i^\top$, let $y \in \mathbb{R}^n$ and $0 \le \tau \le 1$. Write $Q(w) = \sum_i \rho_\tau(y_i - x_i^\top w)$ with $\rho_\tau(r) = \tau \max(r, 0) + (1 - \tau)\max(-r, 0)$. The linear program (LP) is

$$\min \; c^\top z = \tau \mathbf{1}^\top u + (1-\tau)\mathbf{1}^\top v \quad \text{s.t.} \quad X w^+ - X w^- + u - v = y,\; z = (w^+, w^-, u, v) \ge 0 .$$

**Lemma 1 (the LP is the problem).** The optimal value of the LP equals $\min_w Q(w)$, and if $z$ is optimal for the LP, then $w = w^+ - w^-$ minimizes $Q$.

*Proof.* Take a feasible $z$ and let $w = w^+ - w^-$ and $r = y - Xw$. Then $u - v = r$ with $u, v \ge 0$. So $u_i \ge r_i$ and $u_i \ge 0$, which gives $u_i \ge \max(r_i, 0)$, and in the same way $v_i = u_i - r_i \ge \max(-r_i, 0)$. Since $\tau \ge 0$ and $1 - \tau \ge 0$, $c^\top z \ge Q(w)$. Conversely, for each $w$, the point with $w^+ = \max(w, 0)$, $w^- = \max(-w, 0)$, $u = \max(r, 0)$ and $v = \max(-r, 0)$ is feasible and has $c^\top z = Q(w)$. So the two infima are equal. The LP is feasible and its objective is $\ge 0$, so it has an optimal solution (a feasible LP that is bounded below attains its minimum). If $z$ is optimal, then $Q(w^+ - w^-) \le c^\top z = \min_w Q$, so $w^+ - w^-$ is a minimizer. $\square$

**Lemma 2 (the start).** After line L2, the basic columns form the identity matrix and the right side is $\ge 0$, so the start is a basic feasible solution.

*Proof.* In row $i$ the column of $u_i$ is $e_i$ and the column of $v_i$ is $-e_i$. If $y_i \ge 0$, the basic column $u_i$ is $e_i$ and the right side is $y_i \ge 0$. If $y_i < 0$, line L2 negates row $i$, so the column of $v_i$ becomes $e_i$ in that row and stays 0 in the others, and the right side becomes $-y_i > 0$. Negating a row does not change the feasible set. $\square$

**Lemma 3 (each step).** Assume that the tableau is a basic feasible solution with basis $B$, so $T = [B^{-1}A \mid B^{-1}b]$ with $B^{-1}b \ge 0$, and line L4 computes $\bar c_j = c_j - c_B^\top B^{-1} a_j$.

(a) If $\bar c \ge 0$, the current point is optimal. For each feasible $z$, $Az = b$ gives $z_B = B^{-1}b - B^{-1}A_N z_N$, so $c^\top z = c_B^\top B^{-1}b + \bar c^\top z \ge c_B^\top B^{-1} b$, because $z \ge 0$ and $\bar c \ge 0$ (the basic reduced costs are 0). The right side is the current cost.

(b) If $\bar c_e < 0$, then the set $R$ of line L7 is not empty. Otherwise the column $T[\cdot][e] \le 0$, and the points $z(t)$ with $z_e = t$, $z_B = B^{-1}b - t\,T[\cdot][e]$ and the other nonbasic variables 0 are feasible for each $t \ge 0$, with cost $c_B^\top B^{-1} b + t\,\bar c_e \to -\infty$. That is impossible, since the cost is $\ge 0$ on the feasible set.

(c) The ratio test of line L8 keeps the right side $\ge 0$ after the pivot of line L9, so the new tableau is again a basic feasible solution, and the cost does not increase. This is the standard step of the simplex method.

**Termination.** Line L6 chooses the smallest entering index, and line L8 breaks ties by the smallest basis index. This is Bland's rule, and Bland (1977) proved that the simplex method with this rule never repeats a basis. There are finitely many bases, so the loop of line L3 stops. By (a), it stops at an optimal basic feasible solution, and by Lemma 1, line L11 returns a minimizer of $Q$.

**Theorem (interpolation, Koenker and Bassett 1978).** Assume that $X$ has rank $d$. Then some minimizer $w^\star$ of $Q$ has a set $Z = \{i : y_i = x_i^\top w^\star\}$ such that the rows $\{x_i : i \in Z\}$ span $\mathbb{R}^d$. In particular, $w^\star$ fits $d$ points with linearly independent rows exactly.

*Proof.* Let $w$ be any minimizer, which exists by Lemma 1, and let $Z(w)$ be its set of zero residuals. Let $s = \operatorname{rank}\{x_i : i \in Z(w)\}$. If $s = d$ we are done. Else there is $\delta \ne 0$ with $x_i^\top \delta = 0$ for all $i \in Z(w)$. Since $X$ has rank $d$, $X\delta \ne 0$, so some index $j$ has $a_j = x_j^\top \delta \ne 0$, and $j \notin Z(w)$.

For $t \in \mathbb{R}$ consider $w(t) = w + t\delta$. The residuals in $Z(w)$ stay 0. A residual $r_i(t) = r_i - t a_i$ with $i \notin Z(w)$ is nonzero at $t = 0$. Let $t_0 = \min\{|r_i / a_i| : i \notin Z(w), a_i \ne 0\} > 0$. For $|t| < t_0$ no residual changes its sign, so $Q(w(t))$ is an affine function $Q(w) + g\,t$ on the open interval $(-t_0, t_0)$. Since $w$ is a minimizer, $Q(w(t)) \ge Q(w)$ for $t$ of both signs, so $g = 0$. By continuity, $Q(w(t)) = Q(w)$ also at the end point $t^\star = r_j / a_j$ where $|r_j/a_j| = t_0$. So $w' = w(t^\star)$ is a minimizer, $Z(w') \supseteq Z(w) \cup \{j\}$, and $x_j \notin \operatorname{span}\{x_i : i \in Z(w)\}$, because $x_j^\top \delta \ne 0$ while $\delta$ is orthogonal to that span. So the rank $s$ grows by at least one. After at most $d$ moves, $s = d$. $\blacksquare$

**Corollary (the residual counts).** Assume that the first column of $X$ is all ones. Let $w$ be a minimizer, and let $N^-$, $N^0$ and $N^+$ be the numbers of negative, zero and positive residuals. Then $N^- \le n\tau \le N^- + N^0$.

*Proof.* Move the intercept: $w(t) = w + t e_1$, so each residual becomes $r_i - t$. The right derivative of $Q(w(t))$ at $t = 0$ is $-\tau N^+ + (1 - \tau)(N^- + N^0)$, and it is $\ge 0$ because $w$ is a minimizer. With $N^+ = n - N^- - N^0$ this is $N^- + N^0 \ge n\tau$. The left derivative gives, in the same way, $-\tau(N^+ + N^0) + (1 - \tau)N^- \le 0$, which is $N^- \le n\tau$. $\blacksquare$
