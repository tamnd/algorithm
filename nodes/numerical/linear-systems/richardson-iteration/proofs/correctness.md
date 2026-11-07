---
title: Richardson iteration multiplies the residual by a polynomial in A, and converges for symmetric positive definite A exactly when 0 < omega < 2 / lambda_max
proves: [correctness, termination]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$ be nonsingular, $A x = b$, and let $x_k$, $r_k = b - A x_k$ and $e_k = x_k - x$ be the iterate, residual and error after $k$ updates, with parameters $\omega_0, \omega_1, \ldots$ (all equal to $\omega$ in the stationary case).

**Termination.** The loop at line L3 runs at most `maxiter` + 1 times, so the algorithm stops. It reports convergence only when the test at line L4 holds, and then $\|r_k\|_2 \le \mathrm{tol}\,\|b\|_2$.

**Lemma 1 (residual polynomial).** $e_{k+1} = (I - \omega_k A) e_k$ and $r_{k+1} = (I - \omega_k A) r_k$. Hence $r_k = p_k(A) r_0$ and $e_k = p_k(A) e_0$ with
$$p_k(t) = \prod_{j=0}^{k-1}(1 - \omega_j t), \qquad p_k(0) = 1,$$
and $x_k \in x_0 + \mathcal{K}_k(A, r_0)$, the [Krylov subspace](/krylov-subspace/) $\mathrm{span}\{r_0, A r_0, \ldots, A^{k-1} r_0\}$.

*Proof.* Line L5 gives $x_{k+1} = x_k + \omega_k r_k$ and $r_k = A(x - x_k) = -A e_k$, so $e_{k+1} = e_k - \omega_k A e_k$. Multiplying by $-A$, which commutes with $I - \omega_k A$, gives the residual recurrence. Induction gives the products. Finally $x_k - x_0 = \sum_{j<k} \omega_j r_j = \sum_{j<k} \omega_j p_j(A) r_0$, a polynomial of degree at most $k-1$ in $A$ applied to $r_0$. $\square$

**Lemma 2 (stationary convergence).** With constant $\omega$, $x_k \to x$ for every $x_0$ if and only if $|1 - \omega\lambda| < 1$ for every eigenvalue $\lambda$ of $A$, that is, every eigenvalue lies in the open disc of center and radius $1/\omega$. If $A$ is symmetric positive definite with extreme eigenvalues $\lambda_{\min}$ and $\lambda_{\max}$, this holds if and only if $0 < \omega < 2/\lambda_{\max}$.

*Proof.* $e_k = G^k e_0$ with $G = I - \omega A$, whose eigenvalues are $1 - \omega\lambda$. By the [spectral radius](/spectral-radius/) facts, $G^k e_0 \to 0$ for all $e_0$ if and only if $\rho(G) < 1$. For real positive $\lambda$, $|1 - \omega\lambda| < 1$ means $0 < \omega\lambda < 2$; this holds for all eigenvalues exactly when $0 < \omega < 2/\lambda_{\max}$. $\square$

**Lemma 3 (rate for SPD $A$).** If $A$ is symmetric positive definite, then $\|r_k\|_2 \le \rho^k \|r_0\|_2$ and $\|e_k\|_2 \le \rho^k\|e_0\|_2$ with $\rho = \max_\lambda |1 - \omega\lambda| = \max(|1 - \omega\lambda_{\min}|, |1 - \omega\lambda_{\max}|)$. The minimum of $\rho$ over $\omega$ is attained at $\omega^* = 2/(\lambda_{\min} + \lambda_{\max})$ and equals $(\kappa - 1)/(\kappa + 1)$ with $\kappa = \kappa_2(A) = \lambda_{\max}/\lambda_{\min}$.

*Proof.* $G$ is symmetric, so $\|G\|_2 = \rho(G)$ and $\|G^k\|_2 \le \rho(G)^k$. The function $\omega \mapsto \max(|1 - \omega\lambda_{\min}|, |1 - \omega\lambda_{\max}|)$ is the maximum of a decreasing and an increasing function on the relevant range, so it is smallest where $1 - \omega\lambda_{\min} = \omega\lambda_{\max} - 1$, which is $\omega^*$, with value $(\lambda_{\max} - \lambda_{\min})/(\lambda_{\max} + \lambda_{\min})$. $\square$

**Lemma 4 (Chebyshev parameters).** Let $A$ be symmetric with eigenvalues in $[\alpha, \beta]$, $0 < \alpha < \beta$, and let $\omega_j = 1/\tau_j$ for the roots $\tau_j = \frac{\beta + \alpha}{2} + \frac{\beta - \alpha}{2}\cos\frac{(2j+1)\pi}{2m}$, $j = 0, \ldots, m-1$. Then after $m$ steps, $\|r_m\|_2 \le \|r_0\|_2 / T_m\big(\frac{\beta + \alpha}{\beta - \alpha}\big)$, where $T_m$ is the Chebyshev polynomial, and repeating the cycle $c$ times gives the bound to the power $c$.

*Proof.* $p_m(t) = \prod_j (1 - t/\tau_j)$ has degree $m$, roots $\tau_j$ and $p_m(0) = 1$, so $p_m(t) = T_m\big(\frac{\beta + \alpha - 2t}{\beta - \alpha}\big)/T_m\big(\frac{\beta + \alpha}{\beta - \alpha}\big)$, because the right side has the same roots, the same degree and the same value at $0$. On $[\alpha, \beta]$ the argument of the numerator lies in $[-1, 1]$, where $|T_m| \le 1$. Since $A$ is symmetric, $\|p_m(A)\|_2 = \max_\lambda |p_m(\lambda)| \le 1/T_m\big(\frac{\beta + \alpha}{\beta - \alpha}\big)$. After $c$ cycles $r = p_m(A)^c r_0$. $\square$

**Lemma 5 (finite termination in exact arithmetic).** If $A$ is diagonalizable with distinct nonzero eigenvalues $\lambda_1, \ldots, \lambda_s$ and $\omega_j = 1/\lambda_{j+1}$ for $j < s$, then $r_s = 0$.

*Proof.* $p_s(A) = \prod_j (I - A/\lambda_j)$ maps every eigenvector to $0$, and the eigenvectors span $\mathbb{R}^n$. $\square$

**Conclusion.** The algorithm stops; when it reports convergence, $\|e_k\|_2/\|x\|_2 \le \kappa_2(A)\,\mathrm{tol}$. For symmetric positive definite $A$ and constant $0 < \omega < 2/\lambda_{\max}$ the iterates converge to $x$ in exact arithmetic for every $x_0$, at the rate of Lemma 3; for $\omega \ge 2/\lambda_{\max}$ or $\omega \le 0$ they do not converge for every $x_0$. $\blacksquare$

**About floating point.** In floating point the computed residual of the iterates settles near a small multiple of $u\,\|A\|\,\|x\|$, which the tests observe; Lemma 5 does not survive rounding, and Lemma 4 holds up to rounding only for small $m$ in the natural order of the parameters.
