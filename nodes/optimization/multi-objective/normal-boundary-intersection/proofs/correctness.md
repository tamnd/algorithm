---
title: What normal boundary intersection guarantees, for two objectives and for more
proves: [correctness]
status: full
---

All objectives are minimized. The problem is $\min F(x) = (f_1(x), \ldots, f_p(x))$ over $x \in X$, and $y = F(x)$ is the image of $x$. A point $y \in F[X]$ is nondominated if no $y' \in F[X]$ has $y' \le y$ and $y' \ne y$, where $\le$ is taken in each coordinate. The set of nondominated points is $Y_N$. We write $\mathcal{P} = F[X] + \mathbb{R}^p_+$, and $e = (1, \ldots, 1)$.

The method computes anchors $x_1^*, \ldots, x_p^*$, the ideal point $F^*$ with $F^*_i = f_i(x_i^*)$, the pay-off matrix $\Phi$ whose column $j$ is $F(x_j^*) - F^*$, and the quasi-normal $\hat n = -\Phi e$. For a weight vector $\beta \ge 0$ with $e^\top \beta = 1$, the base point is $q(\beta) = F^* + \Phi \beta$, and the subproblem is

$$\mathrm{NBI}(\beta): \quad \max\ t \quad \text{subject to} \quad F(x) = q(\beta) + t \hat n, \quad x \in X.$$

Its output is $y = F(x)$ for an optimal $(x, t)$.

**Lemma 1 (anchors are Pareto optimal).** Let $F^*_i = \min_{x \in X} f_i(x)$, and let $x_i^*$ minimize $\sum_{j \ne i} f_j$ over $\{x \in X : f_i(x) = F^*_i\}$. Then $F(x_i^*) \in Y_N$.

*Proof.* Suppose $x \in X$ has $F(x) \le F(x_i^*)$ and $F(x) \ne F(x_i^*)$. Then $f_i(x) \le F^*_i$, so $f_i(x) = F^*_i$, and $x$ is feasible for the second step. Its value $\sum_{j \ne i} f_j(x)$ is less than that of $x_i^*$, because $F(x)$ is no larger in each coordinate and smaller in some coordinate, which cannot be $i$. This contradicts the choice of $x_i^*$. $\square$

The implementation uses this two-step rule for the anchors.

**Lemma 2 (the subproblems are well posed for linear programs).** Let $F(x) = C x$ and $X = \{x : A x \geqq b\}$, with $X$ nonempty and each objective bounded below on $X$. If $\Phi \ne 0$, then for each $\beta$ the linear program $\mathrm{NBI}(\beta)$ has an optimal solution with $0 \le t \le 1$.

*Proof.* The point $x = \sum_j \beta_j x_j^*$ is in $X$, because $X$ is convex, and $C x = \sum_j \beta_j C x_j^* = F^* + \Phi \beta$. So $(x, 0)$ is feasible. The entries of $\Phi$ are nonnegative, because $F^*$ is the ideal point, and $\Phi \ne 0$, so some row $k$ has $(\Phi e)_k > 0$. Every feasible $(x, t)$ has $(C x)_k \ge F^*_k$, that is, $(\Phi \beta)_k - t (\Phi e)_k \ge 0$. Since $0 \le \beta_j \le 1$, $(\Phi \beta)_k \le (\Phi e)_k$, so $t \le 1$. A feasible linear program whose objective is bounded has an optimal solution, and its value is at least the value $0$ of the feasible point above. $\square$

If $\Phi = 0$, all anchors have the image $F^*$, which is then the only nondominated point, and the implementation returns it.

**Lemma 3 (invariance under scaling).** Let $D$ be a diagonal matrix with positive diagonal and $c \in \mathbb{R}^p$, and let $G(x) = D F(x) + c$. Use the same anchors for $G$, which is allowed because they are also Pareto optimal minimizers for $G$. Then for every $\beta$, $(x, t)$ is feasible for $\mathrm{NBI}(\beta)$ with $F$ exactly when it is feasible for $\mathrm{NBI}(\beta)$ with $G$. So the two problems give the same $x$ and $t$, and the output for $G$ is $D y + c$.

*Proof.* For $G$, the ideal point is $D F^* + c$, the pay-off matrix is $D \Phi$, and the quasi-normal is $-D \Phi e = D \hat n$. The constraint $G(x) = D F^* + c + D \Phi \beta + t D \hat n$ is $D (F(x) - F^* - \Phi \beta - t \hat n) = 0$, which is the constraint for $F$, because $D$ is invertible. $\square$

So, unlike the [weighted sum method](/weighted-sum-method/), the spread of the base points does not depend on the units of the objectives.

**Theorem 4 (two objectives).** Let $p = 2$. Assume that $\mathcal{P}$ is closed and convex, that $F^*$ exists, and that the anchors are chosen as in Lemma 1. This holds for every linear program with $X$ nonempty and both objectives bounded below. Then for every $\beta$, the output of $\mathrm{NBI}(\beta)$ is in $Y_N$, and it is the only point where the line $\{q(\beta) + t \hat n : t \in \mathbb{R}\}$ meets $Y_N$.

*Proof.* Translate so that $F^* = 0$. Let $y^1 = F(x_1^*) = (0, b)$ and $y^2 = F(x_2^*) = (a, 0)$, so $\Phi = \begin{pmatrix} 0 & a \\ b & 0 \end{pmatrix}$ with $a, b \ge 0$. If $a = 0$, then $x_2^*$ also minimizes $f_1$, so the second step for $x_1^*$ gives $b = f_2(x_1^*) \le f_2(x_2^*) = 0$, and $b = 0$. In the same way $b = 0$ gives $a = 0$. The case $a = b = 0$ is the case $\Phi = 0$, so assume $a, b > 0$. Then $\hat n = -(a, b)$, and the line is $r(t) = (a (\beta_2 - t),\ b (\beta_1 - t))$.

*The lower boundary.* For $s \ge 0$ let $\psi(s) = \min\{y_2 : y \in \mathcal{P},\ y_1 = s\}$. The set is not empty, since $y^1 + (s, 0) \in \mathcal{P}$, its $y_2$ values are at least $F^*_2 = 0$, and the minimum exists since $\mathcal{P}$ is closed. The function $\psi$ is convex because $\mathcal{P}$ is convex, it is nonincreasing because $\mathcal{P} + \mathbb{R}^2_+ = \mathcal{P}$, and it is continuous on $(0, \infty)$, like every finite convex function on an open interval. Also $\mathcal{P} = \{y : y_1 \ge 0,\ y_2 \ge \psi(y_1)\}$, since $y_1 \ge F^*_1 = 0$ on $\mathcal{P}$.

- $\psi(0) = b$: a point $y \in \mathcal{P}$ with $y_1 = 0$ has $y \ge F(x)$ with $f_1(x) \le 0$, so $f_1(x) = 0$, and $y_2 \ge f_2(x) \ge b$ by the choice of $x_1^*$.
- $\psi(s) > 0$ for $0 \le s < a$: a point $y \in \mathcal{P}$ with $y = (s, 0)$ would give $x$ with $f_2(x) = 0$ and $f_1(x) \le s < a$, against the choice of $x_2^*$. And $\psi(a) = 0$, since $y^2 \in \mathcal{P}$.
- $\psi$ is strictly decreasing on $[0, a]$: if it were constant on some interval $[s_1, s_2]$ with $s_2 < a$, its slopes after $s_1$ would be at least $0$ by convexity and at most $0$ since it is nonincreasing, so $\psi(a) = \psi(s_1) > 0$, a contradiction.

*Points of the graph are nondominated.* Let $0 \le s \le a$ and $y \in \mathcal{P}$ with $y \le (s, \psi(s))$. Then $y_1 \le s$ and $\psi(s) \ge y_2 \ge \psi(y_1) \ge \psi(s)$, so $\psi(y_1) = \psi(s)$, and $y_1 = s$ by strict decrease. So no point of $\mathcal{P}$ dominates $(s, \psi(s))$. Such a point is in $F[X]$: it is $F(x) + d$ with $d \ge 0$, and $F(x) \in \mathcal{P}$ is no larger, so $d = 0$. Hence it is in $Y_N$.

*The farthest point of the line in $\mathcal{P}$.* The base point $q(\beta) = r(0)$ is a convex combination of $y^1$ and $y^2$, so it is in $\mathcal{P}$. A point $r(t) \in \mathcal{P}$ has $r_1(t) \ge 0$, so $t \le \beta_2$. Let $\hat t = \max\{t : r(t) \in \mathcal{P}\}$, which exists because $\mathcal{P}$ is closed, and $0 \le \hat t \le \beta_2$.

- If $\hat t = \beta_2$, then $r_1 = 0$ and $r_2 = b (\beta_1 - \beta_2) \ge \psi(0) = b$, so $\beta_2 = 0$, $\hat t = 0$, and $r(\hat t) = y^1 = (0, \psi(0))$.
- If $\hat t < \beta_2$, then $s = r_1(\hat t) \in (0, a]$. If $r_2(\hat t) > \psi(s)$, then by continuity of $\psi$ at $s$, $r(\hat t + \varepsilon)$ still has $r_1 > 0$ and $r_2 > \psi(r_1)$ for a small $\varepsilon > 0$, so it is in $\mathcal{P}$, against the choice of $\hat t$. So $r(\hat t) = (s, \psi(s))$.

In both cases $r(\hat t)$ is a point of the graph over $[0, a]$, so $r(\hat t) \in Y_N \subseteq F[X]$.

*The subproblem finds it.* Since $F[X] \subseteq \mathcal{P}$, every feasible $t$ of $\mathrm{NBI}(\beta)$ has $t \le \hat t$. And $t = \hat t$ is feasible, since $r(\hat t) \in F[X]$. So the optimal value is $\hat t$, and the output is $r(\hat t) \in Y_N$.

*Uniqueness.* Both coordinates of $r(t)$ strictly decrease in $t$. Two different points of $Y_N$ cannot be ordered in both coordinates, so the line meets $Y_N$ at most once. $\blacksquare$

**Proposition 5 (three objectives: a dominated output).** Let $F(x) = x$ and let $X \subset \mathbb{R}^3$ be the tetrahedron

$$X = \{x : x_1 + x_2 \ge 2,\ x_1 + x_3 \ge 2,\ x_2 + x_3 \ge 2,\ x_1 + x_2 + x_3 \le 4\},$$

with the vertices $(0, 2, 2)$, $(2, 0, 2)$, $(2, 2, 0)$ and $(1, 1, 1)$. For $\beta = (\tfrac12, \tfrac12, 0)$, the output of $\mathrm{NBI}(\beta)$ is $(1, 1, 2)$, which $(1, 1, 1) \in X$ dominates.

*Proof.* Each $f_i = x_i$ has a unique minimizer over $X$, the vertex with $x_i = 0$, so the anchors are $(0, 2, 2)$, $(2, 0, 2)$ and $(2, 2, 0)$, $F^* = 0$, and $\Phi$ has the anchors as columns. So $\hat n = -(4, 4, 4)$ and $q(\beta) = (1, 1, 2)$. The point $r(t) = (1 - 4t,\ 1 - 4t,\ 2 - 4t)$ satisfies $x_1 + x_2 \ge 2$ only when $t \le 0$. So the optimal $t$ is $0$ and the output is $(1, 1, 2)$, which is in $X$ and is dominated by $(1, 1, 1)$. $\blacksquare$

The same holds for $(1, 2, 1)$ and $(2, 1, 1)$ by symmetry. So for $p \ge 3$ the output need not be Pareto optimal, and a separate check is needed, for example the linear program of Ecker and Kouada for a linear problem. The point $(1, 1, 1)$ is nondominated; it is the output for $\beta = (\tfrac13, \tfrac13, \tfrac13)$, where $r(t) = (\tfrac43 - 4 t) e$ meets $X$ last at $t = \tfrac1{12}$.

**Lemma 6 (the relaxed subproblem gives weakly nondominated points).** Replace the equation by an inequality: maximize $t$ subject to $F(x) \le q(\beta) + t \hat n$ and $x \in X$, that is, $r(t) = q(\beta) + t \hat n \in \mathcal{P}$. If the maximum $\hat t$ is attained, then no $y' \in F[X]$ has $y'_i < r_i(\hat t)$ for every $i$.

*Proof.* If such a $y'$ existed, then $r(\hat t + \varepsilon) = r(\hat t) + \varepsilon \hat n \ge y'$ for all small enough $\varepsilon > 0$, because the gap $r(\hat t) - y'$ is positive in each coordinate. So $r(\hat t + \varepsilon) \in y' + \mathbb{R}^p_+ \subseteq \mathcal{P}$, against the maximality of $\hat t$. $\square$

This is a Pascoletti and Serafini scalarization, with the reference point $q(\beta)$ and the direction $\hat n$. It does not repair Proposition 5: there the relaxed problem also gives $\hat t = 0$ and the point $(1, 1, 2)$, which is weakly nondominated but dominated.
