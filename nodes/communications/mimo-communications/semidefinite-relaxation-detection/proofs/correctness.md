---
title: Correctness of semidefinite relaxation detection
proves: [correctness]
status: full
---

This proof refers to the lines of the pseudocode `main` on the page. The real-valued model is $\|y - H x\|^2 = \|y_r - G b\|^2$ for $x = a b$ and $b \in \{-1, +1\}^N$, where $G$ has $m$ rows and $N$ columns. For BPSK, $y_r$ and $G$ hold the real and the imaginary parts of $y$ and $H$ in two blocks of rows, and $a = 1$. For 4-QAM, $G = a \begin{pmatrix} \Re H & -\Im H \\ \Im H & \Re H \end{pmatrix}$ with $a = 1/\sqrt 2$, and $b$ holds the real signs and then the imaginary signs. In both cases the identity holds because $|z|^2 = (\Re z)^2 + (\Im z)^2$ for every entry of $y - H x$. So the ML vectors of the two problems are the same (a closed form). Let $M^\star = \min_b \|y_r - G b\|^2$ be the ML metric.

## Theorem 1 (homogeneous form)

Let $Q$ be the matrix of line L2. For $v = (b, t)$ with $t \in \{-1, +1\}$, $v^T Q v = \|y_r - G (t b)\|^2$.

Proof. Expand: $v^T Q v = b^T G^T G b - 2 t\, b^T G^T y_r + t^2 y_r^T y_r$. Since $t^2 = 1$, this equals $(t b)^T G^T G (t b) - 2 (t b)^T G^T y_r + y_r^T y_r = \|y_r - G (t b)\|^2$. $\square$

So $\min_{v \in \{-1, +1\}^{N+1}} v^T Q v = M^\star$. An optimal $v$ gives the ML vector $t b$, and the vector with $t = 1$ has metric $v^T Q v$ for $v = (b, 1)$, which is the function `metric` of the implementation.

## Theorem 2 (the relaxation is a lower bound)

Let $P^\star = \min \{ \mathrm{tr}(Q X) : X \succeq 0, X_{ii} = 1 \}$. Then $P^\star \le M^\star$.

Proof. For every $v \in \{-1, +1\}^{N+1}$, the matrix $X = v v^T$ is positive semidefinite and has $X_{ii} = v_i^2 = 1$, and $\mathrm{tr}(Q v v^T) = v^T Q v$. So the feasible set of the SDR contains every point of the ML problem in Theorem 1, and the minimum over the larger set is not larger. $\square$

The feasible set is compact (all entries satisfy $|X_{ij}| \le 1$, because every $2 \times 2$ principal minor is nonnegative), so the minimum exists.

## Theorem 3 (the bound of line L6 is valid for any unit vectors)

Let $u_0, \dots, u_N$ be any vectors, let $\lambda_i = \sum_j Q_{ij}\, u_i \cdot u_j$ (line L5), and let $e$ be the smallest eigenvalue of $Q - \mathrm{Diag}(\lambda)$. Then $\sum_i \lambda_i + (N + 1) e \le P^\star \le M^\star$.

Proof. Put $\mu = \lambda + e \mathbf 1$. Then $Q - \mathrm{Diag}(\mu) = (Q - \mathrm{Diag}(\lambda)) - e I \succeq 0$, because its eigenvalues are those of $Q - \mathrm{Diag}(\lambda)$ minus their minimum. Let $X$ be feasible for the SDR. The trace of the product of two positive semidefinite matrices is nonnegative (write $X = C C^T$; then $\mathrm{tr}(A X) = \mathrm{tr}(C^T A C) \ge 0$ for $A \succeq 0$). So

$$\mathrm{tr}(Q X) = \mathrm{tr}((Q - \mathrm{Diag}(\mu)) X) + \sum_i \mu_i X_{ii} \ge \sum_i \mu_i = \sum_i \lambda_i + (N + 1) e.$$

This holds for every feasible $X$, so also for the minimum $P^\star$. Theorem 2 gives the second inequality. $\square$

This is weak duality for the dual program $\max \sum_i \mu_i$ subject to $Q - \mathrm{Diag}(\mu) \succeq 0$. The proof uses no property of the vectors $u_i$, so the bound holds whether the solver of lines L3 and L4 converged or not. In floating point the bound is correct up to the rounding error of the Jacobi method, which the tests allow for with a tolerance of $10^{-9}$.

## Theorem 4 (certificate)

Let $\hat b$ be the vector that the algorithm returns, with metric $\hat M = \|y_r - G \hat b\|^2$, and let $\ell$ be the bound of line L6. Then $\hat M - M^\star \le \hat M - \ell$. In particular, if $\hat M = \ell$, then $\hat b$ is an ML vector.

Proof. Theorem 3 gives $\ell \le M^\star$, so $\hat M - M^\star \le \hat M - \ell$. If $\hat M = \ell$, then $\hat M \le M^\star$, and $\hat M \ge M^\star$ by the definition of $M^\star$, so $\hat M = M^\star$. $\square$

The returned vector is always a feasible point: lines L7 and L8 make a sign vector, and line L8 multiplies it by the sign of $t$, so by Theorem 1 the metric that the algorithm compares is the true metric of that vector. Line L9 maps each $a b_i$ (or each pair of real and imaginary parts) to the constellation point that it equals. So the output is a valid symbol vector in all cases, and an ML vector whenever the certificate holds.

## Theorem 5 (each step of the mixing method does not increase the objective)

Let $f(U) = \sum_{i,j} Q_{ij}\, u_i \cdot u_j$ with all $\|u_i\| = 1$. Fix all vectors but $u_i$, and let $g = \sum_{j \ne i} Q_{ij} u_j$. If $g \ne 0$, then $u_i = -g / \|g\|$ minimizes $f$ over the unit vectors $u_i$, and line L4 does not increase $f$.

Proof. Since $Q$ is symmetric, the terms of $f$ that contain $u_i$ are $Q_{ii} \|u_i\|^2 + 2 u_i \cdot g = Q_{ii} + 2 u_i \cdot g$. By the Cauchy-Schwarz inequality, $u_i \cdot g \ge -\|u_i\| \|g\| = -\|g\|$, with equality for $u_i = -g / \|g\|$. So this choice is a minimizer over the unit sphere, and the value after the update is at most the value before. If $g = 0$, $f$ does not depend on $u_i$, and the implementation leaves $u_i$ unchanged. $\square$

So the values $f$ after each sweep form a nonincreasing sequence that is bounded below by $P^\star$ (every $U$ with unit rows gives a feasible $X = U U^T$), and so it converges. The proof does not show that the limit is $P^\star$; Theorem 3 is what makes the bound valid without that.

## Theorem 6 (exact without noise)

Let $w = 0$, so $y_r = G b^\star$ for the transmitted $b^\star$, and let $G$ have full column rank $N$. Let $v^\star = (b^\star, 1)$. Then $X^\star = v^\star v^{\star T}$ is the unique optimal solution of the SDR, $P^\star = M^\star = 0$, and the rounding of lines L7 and L8 applied to any factor $U$ with $U U^T = X^\star$ returns $b^\star$.

Proof. By Theorem 1 with $t = 1$, $v^T Q v = \|G b^\star - G b\|^2$ for $v = (b, 1)$, and for a general $v = (z, s) \in \mathbb{R}^{N+1}$ the same expansion gives $v^T Q v = \|G (s b^\star - z)\|^2 \ge 0$. So $Q \succeq 0$, and $\mathrm{tr}(Q X) \ge 0$ for every feasible $X$ (as in the proof of Theorem 3). $X^\star$ is feasible with $\mathrm{tr}(Q X^\star) = v^{\star T} Q v^\star = 0$, so it is optimal and $P^\star = 0$. Also $M^\star = 0$, attained by $b^\star$.

Uniqueness. The null space of $Q$ is the set of $v = (z, s)$ with $G (s b^\star - z) = 0$, which by the full column rank is $z = s b^\star$, the line spanned by $v^\star$. Let $X$ be optimal. Then $\mathrm{tr}(Q X) = 0$ with $X = C C^T$ gives $\sum_k c_k^T Q c_k = 0$ over the columns $c_k$ of $C$, and each term is nonnegative, so $Q c_k = 0$ for each $k$. So each column is a multiple of $v^\star$, and $X = \alpha v^\star v^{\star T}$ for some $\alpha \ge 0$. The diagonal condition gives $\alpha = 1$.

Rounding. $U U^T = X^\star$ means $u_i \cdot u_j = v^\star_i v^\star_j$. In particular $u_i \cdot u_N = b^\star_i$ for $i < N$, and since $\|u_i\| = \|u_N\| = 1$, this gives $u_i = b^\star_i u_N$. Line L7 returns $\mathrm{sign}(u_i \cdot u_N) = b^\star_i$. In line L8, $\mathrm{sign}(u_N \cdot r) \cdot \mathrm{sign}(u_i \cdot r) = \mathrm{sign}(u_N \cdot r)^2 b^\star_i = b^\star_i$ whenever $u_N \cdot r \ne 0$, which has probability one. $\square$

The solver of lines L3 and L4 reaches $X^\star$ only up to its stopping tolerance, so the implementation gets $b^\star$ when its vectors are close enough to $X^\star$ that every sign is right. The test with seed 1906 checks this on noiseless instances (a measurement), and Theorem 4 then certifies the result whenever the bound is within rounding of 0.

## Theorem 7 (rank of the low-rank factor)

The rank $k = \min(N + 1, \lceil \sqrt{2 (N + 1)} \rceil + 1)$ used by the implementation is large enough to hold some optimal solution of the SDR.

Proof. The SDR has $N + 1$ linear equality constraints. By the theorem of Barvinok and Pataki, a feasible and bounded SDP in standard form with $p$ linear constraints has an optimal solution of rank $r$ with $r (r + 1) / 2 \le p$. Here $p = N + 1$, and $r (r + 1) / 2 \le p$ gives $r < \sqrt{2 p} \le k$ (or $r \le N + 1 = k$ in the other case of the minimum). So an optimal $X$ factors as $U U^T$ with $U$ of $k$ columns. $\square$

The theorem says only that the low-rank set contains an optimum. It does not say that the mixing method finds it; that is why the bound of Theorem 3 does not rely on it.

## Summary

Theorem 1 shows that line L2 encodes ML detection exactly. Theorems 2 and 3 show that line L6 gives a lower bound on the ML metric for any output of the solver. Theorem 4 turns that bound into a proof of optimality whenever the rounded metric reaches it. Theorem 5 shows that the solver is monotone. Theorem 6 shows that without noise the relaxation is tight and its unique solution rounds to the transmitted vector. In general the relaxation need not be tight, as the example on the page shows, and the result is then an approximation without a guarantee of optimality.
