---
title: Correctness of the Backus-Gilbert method
proves: [correctness, termination]
status: full
---

Exact arithmetic. Every integral is the same quadrature rule $\int f = \sum_k w_k f(t_k)$ with weights $w_k > 0$, as in the code; the statements also hold for exact integrals. $G_1, \dots, G_m$ are the data kernels, $c_i = \int G_i$, $C$ is a symmetric positive semidefinite $m \times m$ matrix, $\mu \ge 0$, and for a point $p$
$$S(p)_{ij} = 12 \int (t - p)^2 G_i(t) G_j(t)\,dt, \qquad W = S(p) + \mu C .$$
For weights $a \in \mathbb{R}^m$ the averaging kernel is $K_p = \sum_i a_i G_i$. Lines L4 and L5 compute $z = W^{-1} c$ and $a = z / (c^\top z)$.

**Lemma 1 (spread identity).** For every $a$, $a^\top S(p)\, a = 12 \int (t - p)^2 K_p(t)^2\,dt \ge 0$. So $S(p)$ is symmetric positive semidefinite, and $W$ is too.

*Proof.* $\sum_{i,j} a_i a_j \int 12 (t - p)^2 G_i G_j = \int 12 (t - p)^2 \big(\sum_i a_i G_i\big)^2$, by linearity of the quadrature. The integrand is nonnegative and the weights are positive. $W$ is a sum of positive semidefinite matrices with $\mu \ge 0$. $\square$

$W$ is positive definite, for example, if $\mu > 0$ and $C$ is positive definite, or if the vectors $\big((t_k - p) G_i(t_k)\big)_k$, $i = 1, \dots, m$, are linearly independent. We assume this and $c \ne 0$ below.

**Theorem 1 (optimal weights).** If $W$ is positive definite and $c \ne 0$, then $c^\top z > 0$, the vector $a$ of line L5 satisfies $c^\top a = 1$, and it is the unique minimizer of $a^\top W a$ over $\{a : c^\top a = 1\}$. The minimum value is $1/(c^\top W^{-1} c)$.

*Proof.* $W^{-1}$ is positive definite, so $c^\top z = c^\top W^{-1} c > 0$, and $c^\top a = c^\top z / c^\top z = 1$. Let $b = a + g$ with $c^\top g = 0$. Then
$$b^\top W b = a^\top W a + 2 a^\top W g + g^\top W g .$$
Since $W a = c / (c^\top z)$, $a^\top W g = c^\top g / (c^\top z) = 0$. So $b^\top W b = a^\top W a + g^\top W g > a^\top W a$ for $g \ne 0$. Finally $a^\top W a = z^\top W z / (c^\top z)^2 = c^\top z/(c^\top z)^2 = 1/(c^\top W^{-1} c)$. $\square$

**Theorem 2 (unit area and exact averages).** For the weights of Theorem 1, $\int K_p = 1$. If $d_i = \int G_i\, x$ for a function $x$, then line L6 gives $\hat x(p) = \int K_p\, x$. In particular, if $x$ is the constant $\kappa$, then $\hat x(p) = \kappa$.

*Proof.* $\int K_p = \sum_i a_i \int G_i = c^\top a = 1$. Next, $a^\top d = \sum_i a_i \int G_i\, x = \int \big(\sum_i a_i G_i\big) x = \int K_p\, x$. For $x = \kappa$ this is $\kappa \int K_p = \kappa$. $\square$

**Corollary (noise).** If $d = d^0 + n$ with $d^0_i = \int G_i x$, $E\,n = 0$ and $\mathrm{Cov}(n) = C$, then $E\,\hat x(p) = \int K_p\, x$ and $\mathrm{Var}\,\hat x(p) = a^\top C a$.

*Proof.* $\hat x(p) = a^\top d^0 + a^\top n$. Apply Theorem 2 to the first term. The second term has mean $a^\top E n = 0$ and variance $a^\top C a$. $\square$

**Theorem 3 (monotone trade-off).** Let $0 \le \mu_1 < \mu_2$, let $W_1 = S + \mu_1 C$ and $W_2 = S + \mu_2 C$ be positive definite, and let $a_1$ and $a_2$ be the weights of Theorem 1 for $\mu_1$ and $\mu_2$. With $s_k = a_k^\top S a_k$ and $v_k = a_k^\top C a_k$, we have $s_1 \le s_2$ and $v_1 \ge v_2$.

*Proof.* Both $a_1$ and $a_2$ satisfy the constraint. Since $a_1$ minimizes the objective for $\mu_1$ and $a_2$ minimizes it for $\mu_2$,
$$s_1 + \mu_1 v_1 \le s_2 + \mu_1 v_2, \qquad s_2 + \mu_2 v_2 \le s_1 + \mu_2 v_1 .$$
Adding the two inequalities gives $\mu_1 v_1 + \mu_2 v_2 \le \mu_1 v_2 + \mu_2 v_1$, that is $(\mu_2 - \mu_1)(v_2 - v_1) \le 0$, so $v_2 \le v_1$. Then the first inequality gives $s_1 - s_2 \le \mu_1 (v_2 - v_1) \le 0$, so $s_1 \le s_2$. $\square$

**Theorem 4 (termination).** If $W$ is positive definite and $c \ne 0$ for every point $p$ in $P$, the algorithm performs, for each of the finitely many points, one spread matrix, one linear solve and one inner product, and then returns at line L7.

*Proof.* The only loop is over the finite set $P$ (line L1). Each pass is well defined: the solve at line L4 succeeds because $W$ is invertible, and the division at line L5 is by $c^\top z > 0$ (Theorem 1). $\square$
