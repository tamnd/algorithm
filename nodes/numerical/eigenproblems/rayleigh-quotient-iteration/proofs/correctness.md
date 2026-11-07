---
title: Rayleigh quotient iteration has a small backward error, monotone residuals and local cubic convergence for Hermitian matrices
proves: [correctness, termination]
status: full
---

Exact arithmetic, except in Lemma 1, which holds for every pair the method returns. Notation of the page: $x_k$ is the unit vector after $k$ executions of line L8 ($x_0$ from line L1), $\rho_k = x_k^* A x_k$, $r_k = A x_k - \rho_k x_k$, and $y_k$ is the solution computed in line L7 from $x_k$, so $x_{k+1} = y_k / \|y_k\|_2$. We assume that $A - \rho_k I$ is nonsingular whenever line L7 is executed; the zero pivot rule of line L7 is a floating-point device and is not needed for the statements below.

**Lemma 1 (backward error).** If line L5 returns $(\rho, x)$, then $(A - r x^*) x = \rho x$ with $\|r x^*\|_2 = \|r\|_2 \le \mathrm{tol} \, \|A\|_F$. If $A$ is Hermitian, then also $(A + E) x = \rho x$ for the Hermitian $E = -(r x^* + x r^*)$ with $\|E\|_2 = \|r\|_2$, and some eigenvalue $\lambda$ of $A$ satisfies $|\lambda - \rho| \le \|r\|_2$.

*Proof.* $(A - r x^*) x = A x - r = \rho x$ because $x^* x = 1$, and the rank-one matrix $r x^*$ has 2-norm $\|r\|_2 \|x\|_2$. If $A$ is Hermitian, $\rho$ is real and $x^* r = x^* A x - \rho = 0$. Then $(A + E) x = A x - r - x (r^* x) = \rho x$. If $r = 0$ the claim is trivial; otherwise $E$ acts on the orthonormal pair $x, r / \|r\|$ by the matrix $-\|r\| \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ and is zero on their orthogonal complement, so $\|E\|_2 = \|r\|_2$. By Weyl's inequality the eigenvalues of $A$ and of $A + E$, both sorted, differ by at most $\|E\|_2$, and $\rho$ is one of the eigenvalues of $A + E$. $\square$

**Lemma 2 (one step of inverse iteration).** Let $A$ be Hermitian with orthonormal eigenvectors $v_i$, fix $j$, and let $\sigma$ be real and not an eigenvalue. Let $x$ be a unit vector with $v_j^* x \ne 0$ and $\theta = \angle(x, v_j)$, and let $\theta' = \angle\bigl((A - \sigma I)^{-1} x, v_j\bigr)$. Then

$$\tan\theta' \le \tan\theta \, \frac{|\lambda_j - \sigma|}{\min_{i \ne j} |\lambda_i - \sigma|}.$$

*Proof.* Write $x = \sum_i c_i v_i$. Then $(A - \sigma I)^{-1} x = \sum_i c_i (\lambda_i - \sigma)^{-1} v_i$, and

$$\tan\theta' = \frac{\bigl(\sum_{i \ne j} |c_i|^2 |\lambda_i - \sigma|^{-2}\bigr)^{1/2}}{|c_j| \, |\lambda_j - \sigma|^{-1}} \le \frac{|\lambda_j - \sigma|}{\min_{i \ne j}|\lambda_i - \sigma|} \cdot \frac{\bigl(\sum_{i \ne j} |c_i|^2\bigr)^{1/2}}{|c_j|}.$$

The last factor is $\tan\theta$. $\square$

**Lemma 3 (the Rayleigh quotient error).** For Hermitian $A$ and a unit $x$ with $\theta = \angle(x, v_j)$, $|\rho(x) - \lambda_j| \le \delta \sin^2\theta$ and $\|A x - \rho(x) x\|_2 \le \delta \sin\theta$, where $\delta = \lambda_{\max} - \lambda_{\min}$.

*Proof.* Write $x = \phi \cos\theta \, v_j + \sin\theta \, w$ with $|\phi| = 1$ and a unit $w \perp v_j$. Since $A v_j = \lambda_j v_j$ and $w \perp v_j$, the cross terms $v_j^* A w = \lambda_j v_j^* w$ vanish, so $\rho(x) = \cos^2\theta \, \lambda_j + \sin^2\theta \, \rho(w)$ and $\rho(x) - \lambda_j = \sin^2\theta \, (\rho(w) - \lambda_j)$. Both $\rho(w)$ and $\lambda_j$ lie in $[\lambda_{\min}, \lambda_{\max}]$, which gives the first bound. For the second, $\rho(x)$ minimizes $\|A x - \mu x\|_2$ over $\mu$, so $\|A x - \rho(x) x\| \le \|(A - \lambda_j I) x\| = \sin\theta \, \|(A - \lambda_j I) w\| \le \delta \sin\theta$, because $w$ lies in the span of the $v_i$ with $i \ne j$ and $|\lambda_i - \lambda_j| \le \delta$. $\square$

**Theorem 1 (local cubic convergence).** Let $A$ be Hermitian, let $\lambda_j$ be a simple eigenvalue with $\mathrm{gap}_j = \min_{i \ne j} |\lambda_i - \lambda_j| > 0$, let $c = 2 \delta / \mathrm{gap}_j$, and suppose $c \tan^2\theta_0 < 1$, where $\theta_0 = \angle(x_0, v_j)$. Then for every $k$ at which the method has not stopped,

$$\tan\theta_{k+1} \le c \tan^3\theta_k \quad\text{and}\quad \tan\theta_{k+1} \le \tan\theta_k,$$

so $\theta_k \to 0$, and the order of convergence is at least 3.

*Proof.* We show by induction that $c \tan^2\theta_k \le c \tan^2\theta_0 < 1$. This holds for $k = 0$. Assume it for $k$. Then $\delta \sin^2\theta_k \le \delta \tan^2\theta_k < \mathrm{gap}_j / 2$, so by Lemma 3 $|\rho_k - \lambda_j| < \mathrm{gap}_j / 2$, and for $i \ne j$

$$|\lambda_i - \rho_k| \ge |\lambda_i - \lambda_j| - |\lambda_j - \rho_k| \ge \mathrm{gap}_j - \delta \sin^2\theta_k > \mathrm{gap}_j / 2 .$$

If $\rho_k = \lambda_j$, then $\rho(w) = \lambda_j$ in the notation of Lemma 3; the method then either has $r_k = 0$ and stops, or meets a singular system, which we excluded. Otherwise Lemma 2 with $\sigma = \rho_k$ applies (note $v_j^* x_k \ne 0$ because $\tan\theta_k < \infty$), and with Lemma 3

$$\tan\theta_{k+1} \le \tan\theta_k \cdot \frac{\delta \sin^2\theta_k}{\mathrm{gap}_j / 2} \le c \tan^3\theta_k .$$

Since $c \tan^2\theta_k < 1$, this is at most $\tan\theta_k$, and the induction hypothesis passes to $k + 1$. Finally $\tan\theta_{k} \le (c \tan^2\theta_0)^{(3^k - 1)/2} \tan\theta_0$ by induction from $\tan\theta_{k+1} \le (c \tan^2\theta_k) \tan\theta_k$, which tends to $0$. $\square$

**Theorem 2 (monotone residuals).** Let $A$ be Hermitian. For every start and every $k$ at which line L7 is executed, $\|r_{k+1}\|_2 \le \|r_k\|_2$.

*Proof.* Let $y = y_k$, so $(A - \rho_k I) y = x_k$ and $(A - \rho_k I) x_{k+1} = x_k / \|y\|_2$. Since $\rho_{k+1}$ minimizes $\|A x_{k+1} - \mu x_{k+1}\|$ over $\mu$,

$$\|r_{k+1}\|_2 \le \|(A - \rho_k I) x_{k+1}\|_2 = \frac{1}{\|y\|_2}.$$

On the other hand, since $A - \rho_k I$ is Hermitian, $x_{k+1}^* (A - \rho_k I) x_k = \bigl((A - \rho_k I) x_{k+1}\bigr)^* x_k = x_k^* x_k / \|y\|_2 = 1/\|y\|_2$. By the Cauchy-Schwarz inequality, $1/\|y\|_2 \le \|x_{k+1}\|_2 \, \|(A - \rho_k I) x_k\|_2 = \|r_k\|_2$. $\square$

**Theorem 3 (termination).** Under the hypotheses of Theorem 1 and for every $\mathrm{tol} > 0$, line L5 returns CONVERGED after finitely many steps if $\mathrm{maxit}$ is large enough.

*Proof.* By Lemma 3 and Theorem 1, $\|r_k\|_2 \le \delta \sin\theta_k \le \delta \tan\theta_k \to 0$. If $A \ne 0$, then $\mathrm{tol} \, \|A\|_F > 0$ and the test of line L5 passes for some finite $k$. If $A = 0$, then $r_0 = 0$ and the test passes at $k = 0$. $\square$

**Remark (the rate is sharp, and it degrades without symmetry).** For $A = \operatorname{diag}(\lambda_1, \lambda_2)$ and $x_k = (\cos\theta, \sin\theta)^T$, $\rho_k - \lambda_1 = (\lambda_2 - \lambda_1) \sin^2\theta$, $\lambda_2 - \rho_k = (\lambda_2 - \lambda_1) \cos^2\theta$, and $(A - \rho_k I)^{-1} x_k$ is a multiple of $(-\cos\theta / \sin^2\theta, \ \sin\theta / \cos^2\theta)^T$, so $\tan\theta_{k+1} = -\tan^3\theta_k$: equality, with constant 1, as the table of the page shows. For a nonnormal $A$ the identity $\rho(x) - \lambda_j = \sin^2\theta \, (\rho(w) - \lambda_j)$ fails, because the cross term $v_j^* A w$ need not vanish; then $|\rho_k - \lambda_j| = O(\sin\theta_k)$ only, and Lemma 2 (in its diagonalizable form) gives order 2. $\blacksquare$
