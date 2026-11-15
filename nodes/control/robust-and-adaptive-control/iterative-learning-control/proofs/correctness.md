---
title: The ILC error obeys a fixed linear recursion over the trials, and its convergence is set by the spectral radius and the norm of I - PL
proves: [correctness]
status: full
---

Notation is that of the page. Trial $j$ starts at $x(0) = x_0$, the input $u_j \in \mathbb{R}^N$ holds $u(0), \dots, u(N-1)$, and the output $y_j \in \mathbb{R}^N$ holds $y(1), \dots, y(N)$.

**Claim 1 (lifted model).** $y_j = Pu_j + d$, where $P_{ik} = CA^{i-k}B$ for $i \ge k$, $P_{ik} = 0$ for $i < k$ (indices from 0), and $d_i = CA^{i+1}x_0$.

*Proof.* By induction on $k$, $x(k) = A^kx_0 + \sum_{m=0}^{k-1}A^{k-1-m}Bu(m)$. So $y(i+1) = Cx(i+1) = CA^{i+1}x_0 + \sum_{m=0}^{i}CA^{i-m}Bu(m)$, which is row $i$ of $Pu_j + d$. $\square$

The function `run_trial` computes the recursion and `lifted_matrix` builds $P$; the tests check $y_j = Pu_j + d$ exactly in Fraction arithmetic.

**Claim 2 (error recursion).** With $Q = I$, $e_{j+1} = (I - PL)e_j$, so $e_j = (I - PL)^je_0$.

*Proof.* Line L5 gives $u_{j+1} = u_j + Le_j$. By Claim 1, $e_{j+1} = y_d - Pu_{j+1} - d = (y_d - Pu_j - d) - PLe_j = e_j - PLe_j$. $\square$

**Claim 3 (asymptotic convergence).** $e_j \to 0$ for every $e_0$ if and only if $\rho(I - PL) < 1$. For $L = \gamma I$, $\rho(I - \gamma P) = |1 - \gamma CB|$.

*Proof.* For a square matrix $M$, $M^j \to 0$ if and only if $\rho(M) < 1$ (by the Jordan form: a Jordan block of the eigenvalue $\lambda$ has entries $\binom{j}{m}\lambda^{j-m}$, which go to zero if and only if $|\lambda| < 1$). Since $e_0 = y_d - Pu_0 - d$ can be any vector (choose $y_d$), $e_j = M^je_0 \to 0$ for every $e_0$ if and only if $M^j \to 0$. For $L = \gamma I$, $I - \gamma P$ is lower triangular with every diagonal entry $1 - \gamma CB$, and the eigenvalues of a triangular matrix are its diagonal entries. $\square$

In particular, if $\gamma CB = 1$ then $I - \gamma P$ is strictly lower triangular, so $(I - \gamma P)^N = 0$ and $e_N = 0$ for every $e_0$. The tests check this exactly for $a = 9/10$, $N = 30$. If $|1 - \gamma CB| > 1$, the first entry of $e_j$ is $(1 - \gamma CB)^je_0(0)$ and grows; the tests check the factor $-3/2$ for $\gamma = 5/2$.

**Claim 4 (monotonic convergence).** If $\|I - PL\|_2 = q < 1$, then $\|e_{j+1}\|_2 \le q\|e_j\|_2$ for every $j$. For $L = \gamma I$ and $A$ with all eigenvalues inside the unit circle, $\|I - \gamma P\|_2 \le \max_\omega|1 - \gamma\bar P(e^{\mathrm{i}\omega})|$ with $\bar P(z) = \sum_{k\ge 0}CA^kBz^{-k}$.

*Proof.* The first part follows from Claim 2 and the definition of the induced norm. For the second, let $c_k = [k = 0] - \gamma CA^kB$, so $I - \gamma P$ is the $N$ by $N$ lower triangular Toeplitz matrix $T_N$ with entries $c_{i-k}$, and $\sum_k|c_k| < \infty$ because $\rho(A) < 1$. For $v \in \mathbb{R}^N$, extend $v$ by zeros to a sequence on $\mathbb{Z}$; then $T_Nv$ is the restriction to $\{0, \dots, N-1\}$ of the convolution $c * v$. By Parseval, $\|c * v\|_2^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi}|\hat c(\omega)|^2|\hat v(\omega)|^2\,d\omega \le \max_\omega|\hat c(\omega)|^2\,\|v\|_2^2$, where $\hat c(\omega) = \sum_kc_ke^{-\mathrm{i}k\omega} = 1 - \gamma\bar P(e^{\mathrm{i}\omega})$. A restriction does not increase the norm, so $\|T_Nv\|_2 \le \max_\omega|\hat c(\omega)|\,\|v\|_2$. $\square$

For the example $\bar P(z) = 1/(1 - az^{-1})$, which is real at $\omega = 0$ and $\omega = \pi$ with the values $1/(1 - a)$ and $1/(1 + a)$. For $a = 1/2$ and $\gamma = 1/2$, $1 - \gamma\bar P$ ranges over a circle through $0$ and $2/3$, so the maximum is $2/3$ and the decay is monotonic. For $a = 0.9$ and $\gamma = 1$ the value at $\omega = 0$ is $1 - 10 = -9$, and the bound gives nothing; the example shows the growth.

**Claim 5 (norm-optimal law).** If $P$ is invertible and $w > 0$, then $L = (P^TP + wI)^{-1}P^T$ gives $I - PL = w(PP^T + wI)^{-1}$ and $\|I - PL\|_2 = w/(\sigma_{\min}^2 + w) < 1$, where $\sigma_{\min}$ is the smallest singular value of $P$. So the decay is monotonic for every invertible $P$.

*Proof.* $P^T(PP^T + wI) = (P^TP + wI)P^T$, so $(P^TP + wI)^{-1}P^T = P^T(PP^T + wI)^{-1}$. Then $PL = PP^T(PP^T + wI)^{-1}$ and $I - PL = (PP^T + wI - PP^T)(PP^T + wI)^{-1} = w(PP^T + wI)^{-1}$. This matrix is symmetric with the eigenvalues $w/(\sigma_i^2 + w)$; the largest is at $\sigma_{\min}$. $P$ is lower triangular with diagonal $CB \ne 0$, so it is invertible and $\sigma_{\min} > 0$. $\square$

The law minimizes $\|e_j - P\delta\|_2^2 + w\|\delta\|_2^2$ over the change $\delta = u_{j+1} - u_j$: the gradient $-2P^T(e_j - P\delta) + 2w\delta$ vanishes at $\delta = (P^TP + wI)^{-1}P^Te_j = Le_j$, and the cost is strictly convex.

**Plant inversion.** $L = P^{-1}$ gives $I - PL = 0$, so $e_1 = 0$ for every $e_0$; the tests check this exactly. If the true plant is $(I + \Delta)\hat P$ and $L = \hat P^{-1}$, then $I - PL = -\Delta$, and Claim 4 gives monotonic decay when $\|\Delta\|_2 < 1$.
