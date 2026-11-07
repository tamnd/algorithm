---
title: The product form of BiCGSTAB and its finite termination
proves: [correctness, termination]
status: full
---

Exact arithmetic. Notation of the page. BiCG with shadow $\hat r_0$ produces residuals $r_k^B = \varphi_k(A) r_0$ and directions $p_k^B = \pi_k(A) r_0$, with $\varphi_0 = \pi_0 = 1$ and
$$\varphi_{k+1}(t) = \varphi_k(t) - \alpha_k t \pi_k(t), \qquad \pi_{k+1}(t) = \varphi_{k+1}(t) + \beta_k \pi_k(t),$$
$\alpha_k = \rho_k^B / \sigma_k^B$, $\beta_k = \rho_{k+1}^B / \rho_k^B$, where $\rho_k^B = \tilde r_k^T r_k^B$ and $\sigma_k^B = \tilde p_k^T A p_k^B$, with $\tilde r_k = \varphi_k(A^T) \hat r_0$ and $\tilde p_k = \pi_k(A^T) \hat r_0$. Let $\psi_0 = 1$ and $\psi_{k+1}(t) = (1 - \omega_{k+1} t) \psi_k(t)$. All polynomials in $A$ commute.

**Lemma 1 (invariant).** $r = b - A x$ holds after L1 and after each L9.

*Proof.* If $r = b - A x$ and $s = r - \alpha A p$, then $b - A(x + \alpha p + \omega s) = s - \omega A s = s - \omega t$, which is the new $r$. The same computation with $\omega = 0$ covers the return in L6. $\square$

**Lemma 2 (bilinear identities).** Let $\varphi_k$ have leading coefficient $c_k$ (coefficient of $t^k$), and $\psi_k$ leading coefficient $d_k = (-1)^k \omega_1 \cdots \omega_k$. Then
$$\rho_k^B = \frac{c_k}{d_k} \, \hat r_0^T \psi_k(A) \varphi_k(A) r_0, \qquad \sigma_k^B = \frac{c_k}{d_k} \, \hat r_0^T A \psi_k(A) \pi_k(A) r_0.$$

*Proof.* $\rho_k^B = \hat r_0^T \varphi_k(A) \varphi_k(A) r_0$. By BiCG biorthogonality, $\varphi_k(A) r_0 = r_k^B$ is orthogonal to $\mathcal K_k(A^T, \hat r_0)$, so in $\hat r_0^T q(A) r_k^B$ only the $t^k$ coefficient of $q$ matters, for any $q$ of degree $\le k$. Applied to $q = \varphi_k$ and $q = \psi_k$, $\hat r_0^T \varphi_k(A) r_k^B = (c_k / d_k) \hat r_0^T \psi_k(A) r_k^B$. For $\sigma^B$: $\tilde p_k^T A p_k^B = \hat r_0^T \pi_k(A) A \pi_k(A) r_0$, and $A p_k^B$ is $A$-biconjugate: $\hat r_0^T q(A) A \pi_k(A) r_0 = 0$ for $\deg q < k$ (since $\tilde p_j^T A p_k^B = 0$ for $j < k$ and the $\tilde p_j$ span $\mathcal K_k(A^T, \hat r_0)$). The leading coefficient of $\pi_k$ equals $c_k$ (because $\pi_k = \varphi_k + \beta_{k-1}\pi_{k-1}$ with $\deg \pi_{k-1} < k$), so the same argument applies with $\pi_k$ replaced by $\psi_k$. $\square$

**Theorem 1 (product form).** If no breakdown occurs before step $k$, then at the start of pass $k$ of L3 the vectors are $r = \psi_k(A) \varphi_k(A) r_0$, $p = \psi_k(A) \pi_k(A) r_0$, $\rho = \hat r_0^T r$, and the $\alpha$ computed in L4 equals the BiCG value $\alpha_k$; in L5, $s = \psi_k(A) \varphi_{k+1}(A) r_0$; and $\beta$ in L10 equals $\beta_k$.

*Proof.* Induction on $k$. At $k = 0$: $r = p = r_0$, $\psi_0 = \varphi_0 = \pi_0 = 1$. Assume the claim at the start of pass $k$. In L4, $\sigma = \hat r_0^T A \psi_k(A) \pi_k(A) r_0$, so by Lemma 2, $\rho / \sigma = \rho_k^B / \sigma_k^B = \alpha_k$ (the factors $c_k/d_k$ cancel). Then $s = \psi_k(A) (\varphi_k(A) - \alpha_k A \pi_k(A)) r_0 = \psi_k(A) \varphi_{k+1}(A) r_0$. In L9, $r = (I - \omega_{k+1} A) s = \psi_{k+1}(A) \varphi_{k+1}(A) r_0$. In L10, $\rho_{\text{new}} = \hat r_0^T \psi_{k+1}(A) \varphi_{k+1}(A) r_0 = (d_{k+1}/c_{k+1}) \rho_{k+1}^B$ and $\rho = (d_k / c_k) \rho_k^B$, and $c_{k+1} = -\alpha_k c_k$ (leading coefficient of $\varphi_{k+1}$) and $d_{k+1} = -\omega_{k+1} d_k$. Hence
$$\frac{\rho_{\text{new}}}{\rho} \cdot \frac{\alpha_k}{\omega_{k+1}} = \frac{\rho_{k+1}^B}{\rho_k^B} \cdot \frac{d_{k+1} c_k}{d_k c_{k+1}} \cdot \frac{\alpha_k}{\omega_{k+1}} = \beta_k \cdot \frac{\omega_{k+1}}{\alpha_k} \cdot \frac{\alpha_k}{\omega_{k+1}} = \beta_k.$$
Finally, in L11, $p = r + \beta_k (p - \omega_{k+1} v) = \psi_{k+1}(A) \varphi_{k+1}(A) r_0 + \beta_k (I - \omega_{k+1} A) \psi_k(A) \pi_k(A) r_0 = \psi_{k+1}(A) (\varphi_{k+1}(A) + \beta_k \pi_k(A)) r_0 = \psi_{k+1}(A) \pi_{k+1}(A) r_0$. $\square$

**Lemma 3 (local optimality).** $\omega = t^T s / t^T t$ minimizes $f(\omega) = \|s - \omega t\|_2^2$, and $\|r_{k+1}\|_2^2 = \|s\|_2^2 - (t^T s)^2 / t^T t \le \|s\|_2^2$.

*Proof.* $f$ is a quadratic in $\omega$ with $f'(\omega) = 2(\omega t^T t - t^T s)$, zero at the stated $\omega$ ($t \ne 0$ since $s \ne 0$ and $A$ is nonsingular); substitute. $\square$

**Theorem 2 (termination).** If no breakdown occurs, BiCGSTAB returns CONVERGED with $A x = b$ after at most $n$ passes when $\mathrm{tol} = 0$; in every case the code returns after at most $\mathrm{kmax} + 1$ passes.

*Proof.* BiCG without breakdown reaches $\varphi_d(A) r_0 = 0$ for some $d \le n$ (finite termination of BiCG). The BiCG scalars used by BiCGSTAB up to step $d$ are the same (Theorem 1), so at pass $d - 1$, $s = \psi_{d-1}(A) \varphi_d(A) r_0 = 0$, the test in L6 succeeds, and $x$ is updated so that $b - A x = s = 0$ (Lemma 1). If the residual vanishes earlier, the L3 test returns earlier. Each pass either returns or completes, and the loop has $\mathrm{kmax} + 1$ passes. $\blacksquare$
