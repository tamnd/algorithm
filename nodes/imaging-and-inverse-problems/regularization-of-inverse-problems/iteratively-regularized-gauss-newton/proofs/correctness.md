---
title: Correctness of the iteratively regularized Gauss-Newton method
proves: [correctness, termination]
status: full
---

Exact arithmetic. $X$ and $Y$ are real Hilbert spaces ($\mathbb{R}^n$ and $\mathbb{R}^m$ in the code), $F: X \to Y$ is differentiable with derivative $F'(x)$, a bounded linear operator, and $J^*$ is the adjoint of $J$. The inputs are $y^\delta \in Y$, $x_0 \in X$, $\alpha_0 > 0$, $0 < q < 1$, an integer $K \ge 1$, $\delta \ge 0$ and $\tau > 1$. In the pass of the loop with counter $k$, the current iterate is $x_k$ and the current weight is $\alpha_k = \alpha_0 q^k$ (line L1 sets $\alpha_0$ and line L7 multiplies by $q$ once per pass). Lines L4 to L6 compute $x_{k+1} = x_k + h_k$ with
$$(J_k^* J_k + \alpha_k I)\, h_k = J_k^*(y^\delta - F(x_k)) + \alpha_k (x_0 - x_k), \qquad J_k = F'(x_k). \tag{1}$$

**Lemma 1 (the system of line L5 is uniquely solvable).** For every bounded linear $J$ and every $\alpha > 0$, the operator $J^* J + \alpha I$ is self-adjoint, satisfies $\langle (J^* J + \alpha I) h, h\rangle \ge \alpha \|h\|^2$, and is invertible with $\|(J^* J + \alpha I)^{-1}\| \le 1/\alpha$.

*Proof.* Self-adjointness is clear. For every $h$, $\langle (J^* J + \alpha I) h, h\rangle = \|J h\|^2 + \alpha\|h\|^2 \ge \alpha\|h\|^2$. By the Cauchy-Schwarz inequality, $\|(J^* J + \alpha I) h\| \ge \alpha \|h\|$, so the operator is injective with closed range. Its range is dense, because a vector orthogonal to the range is in the kernel of the (self-adjoint) operator, which is $\{0\}$. So the operator is bijective, and the bound on the inverse follows from $\|(J^* J + \alpha I) h\| \ge \alpha\|h\|$. In $\mathbb{R}^n$ the matrix is symmetric positive definite, so Gaussian elimination solves it. $\square$

**Theorem 1 (each step minimizes the linearized Tikhonov functional).** Let $\alpha_k > 0$, $r_k = y^\delta - F(x_k)$ and
$$\Phi_k(z) = \|r_k - J_k (z - x_k)\|^2 + \alpha_k \|z - x_0\|^2 .$$
Then $x_{k+1} = x_k + h_k$ from (1) is the unique minimizer of $\Phi_k$ over $X$.

*Proof.* Write $z = x_k + h$. Then $\Phi_k(x_k + h) = \|r_k - J_k h\|^2 + \alpha_k\|h - (x_0 - x_k)\|^2$. Expanding at $h_k$ in the direction $g$,
$$\Phi_k(x_k + h_k + g) = \Phi_k(x_k + h_k) - 2\big\langle J_k^* r_k + \alpha_k (x_0 - x_k) - (J_k^* J_k + \alpha_k I) h_k,\ g\big\rangle + \|J_k g\|^2 + \alpha_k\|g\|^2 .$$
By (1) the inner product is zero, so $\Phi_k(x_k + h_k + g) = \Phi_k(x_k + h_k) + \|J_k g\|^2 + \alpha_k \|g\|^2$, which is larger than $\Phi_k(x_k + h_k)$ for every $g \ne 0$. By Lemma 1, (1) has exactly one solution $h_k$, so the minimizer exists and is unique. $\square$

**Theorem 2 (linear case: Tikhonov centered at $x_0$).** Let $F(x) = A x$ with $A$ bounded and linear. Then for every $k$ for which line L6 runs,
$$x_{k+1} = x_0 + (A^* A + \alpha_k I)^{-1} A^*(y^\delta - A x_0),$$
the minimizer of $\|A z - y^\delta\|^2 + \alpha_k\|z - x_0\|^2$. In particular $x_{k+1}$ does not depend on $x_k$.

*Proof.* Here $J_k = A$ and $r_k = y^\delta - A x_k$. Adding $(A^* A + \alpha_k I) x_k$ to both sides of (1) gives
$$(A^* A + \alpha_k I)\, x_{k+1} = A^* y^\delta - A^* A x_k + \alpha_k x_0 - \alpha_k x_k + A^* A x_k + \alpha_k x_k = A^* y^\delta + \alpha_k x_0 .$$
The vector $w = x_0 + (A^* A + \alpha_k I)^{-1} A^*(y^\delta - A x_0)$ satisfies $(A^* A + \alpha_k I) w = A^* A x_0 + \alpha_k x_0 + A^* y^\delta - A^* A x_0 = A^* y^\delta + \alpha_k x_0$. By Lemma 1 the solution is unique, so $x_{k+1} = w$. By Theorem 1 with $J_k = A$, $\Phi_k(z) = \|y^\delta - A z\|^2 + \alpha_k\|z - x_0\|^2$, and $x_{k+1}$ is its minimizer. $\square$

**Theorem 3 (termination).** (a) The algorithm stops after at most $K$ passes of the loop, at line L3 or at line L8. It returns $(x_k, k)$ with $k \le K$, and if it returns at line L3, then $\|y^\delta - F(x_k)\| \le \tau\delta$.

(b) Let $F(x) = A x$, $y = A x^\dagger$, $\|y^\delta - y\| \le \delta$ with $\delta > 0$, and $\tau > 1$. Then there is an index $k_*$, which does not depend on $K$, such that the test of line L3 passes at some $k \le k_*$. So for $K > k_*$ the algorithm returns at line L3.

*Proof.* (a) Each pass either returns at line L3 or increases $k$ by one. The loop has at most $K$ passes, and line L8 returns after the last. Every pass is well defined by Lemma 1, because $\alpha_k = \alpha_0 q^k > 0$. A return at line L3 happens only when its test holds.

(b) Let $z = y^\delta - A x_0$ and $R_\alpha = \alpha (A A^* + \alpha I)^{-1}$. From the identity $A (A^* A + \alpha I)^{-1} A^* = A A^* (A A^* + \alpha I)^{-1} = I - R_\alpha$ (both sides agree after multiplication by $A A^* + \alpha I$, which is invertible by Lemma 1 applied to $A^*$) and Theorem 2,
$$y^\delta - A x_{k+1} = z - A (A^* A + \alpha_k I)^{-1} A^* z = R_{\alpha_k} z .$$
Let $E$ be the spectral measure of the self-adjoint operator $A A^* \ge 0$ and $P$ the orthogonal projection onto $\mathcal N(A^*) = \mathcal N(A A^*)$. Then
$$\|R_\alpha z\|^2 = \int_{[0, \|A\|^2]} \Big(\frac{\alpha}{\lambda + \alpha}\Big)^2 d\langle E_\lambda z, z\rangle .$$
The integrand is at most 1 and tends to $0$ for $\lambda > 0$ and to $1$ at $\lambda = 0$ as $\alpha \to 0$. By dominated convergence, $\|R_\alpha z\| \to \|P z\|$ as $\alpha \to 0$. (For a matrix, write $z$ in the eigenvectors of $A A^\top$ and take the limit in each term.) Now $y = A x^\dagger$ and $A x_0$ lie in the range of $A$, which is orthogonal to $\mathcal N(A^*)$, so $P z = P (y^\delta - y)$ and $\|P z\| \le \|y^\delta - y\| \le \delta < \tau\delta$. Since $\alpha_k = \alpha_0 q^k \to 0$, there is a $k_0$ with $\|R_{\alpha_k} z\| \le \tau \delta$ for all $k \ge k_0$, and $k_0$ depends only on $A$, $z$, $\alpha_0$, $q$, $\tau$ and $\delta$. Then $\|y^\delta - A x_{k_0 + 1}\| \le \tau\delta$, so the test of line L3 holds at $k = k_0 + 1$ at the latest, and $k_* = k_0 + 1$ works. $\square$

**Remark (nonlinear case).** For nonlinear $F$, part (b) needs conditions on $F$ near $x^\dagger$, for example a tangential cone condition or a range invariance condition for $F'$, and an initial guess $x_0$ close enough to $x^\dagger$. Under such conditions, Blaschke, Neubauer and Scherzer (1997) proved that the discrepancy principle stops after finitely many steps and that the iterates converge to $x^\dagger$ as $\delta \to 0$. These results are not proved here.
