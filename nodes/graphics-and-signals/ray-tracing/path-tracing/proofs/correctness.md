---
title: Unbiasedness of path tracing
proves: [correctness]
status: full
---

**Setting.** Write $h(x, \omega)$ for the first hit of the ray from $x$ in the direction $\omega$, and define the transport operator on functions $g(x, \omega_o) \ge 0$ by

$$(K g)(x, \omega_o) = \int_{H^2(x)} f(x, \omega_i, \omega_o)\, g(h(x, \omega_i), -\omega_i) \cos\theta_i \, d\omega_i,$$

with $g = 0$ for a ray that hits nothing. The rendering equation is $L = L_e + K L$. Assume $f \ge 0$ and $L_e \ge 0$.

**Claim.** Let $x_0 = h(o, d)$ and $\omega_0 = -d$. Assume that (a) $p(\omega) > 0$ at every vertex wherever $f \cos\theta > 0$, and (b) $q > 0$ wherever $f \cos\theta / p$ is positive for some sampled direction. Then the value $F$ that PATH-TRACE returns has

$$E[F] = \sum_{k = 0}^{\infty} (K^k L_e)(x_0, \omega_0).$$

If the series converges, for example when $K$ has norm at most $\rho_{\max} < 1$ in the supremum norm, its sum is the unique bounded solution $L$ of the rendering equation, so $E[F] = L(x_0, \omega_0)$. With a depth limit of $B$ bounces and no roulette, $E[F] = \sum_{k = 0}^{B} (K^k L_e)(x_0, \omega_0)$.

**The terms of the estimator.** Let $x_k$ be the $k$-th vertex, $\omega_k$ the direction toward the previous vertex (so $\omega_0 = -d$), $A_k$ the event that the path reaches vertex $k$, and $\beta_k$ the throughput at line L4 of vertex $k$. Then $\beta_0 = 1$, and when vertex $k + 1$ exists,

$$\beta_{k+1} = \beta_k \, \frac{f(x_k, \omega'_k, \omega_k) \cos\theta'_k}{p(\omega'_k)\, q_k}, \qquad A_{k+1} = A_k \cap \{u_k < q_k\} \cap \{h(x_k, \omega'_k) \text{ exists}\},$$

where $\omega'_k$ is the direction sampled at line L5 and $x_{k+1} = h(x_k, \omega'_k)$, $\omega_{k+1} = -\omega'_k$. The returned value is $F = \sum_{k \ge 0} \mathbf{1}[A_k]\, \beta_k\, L_e(x_k, \omega_k)$.

**Lemma.** For every $m \ge 0$ and every measurable $g \ge 0$, $E[\mathbf{1}[A_m]\, \beta_m\, g(x_m, \omega_m)] = (K^m g)(x_0, \omega_0)$.

*Proof by induction on $m$.* For $m = 0$, $A_0$ holds, $\beta_0 = 1$, and both sides are $g(x_0, \omega_0)$. Assume the lemma for $m$ and all $g$. Condition on the history up to vertex $m$, which fixes $A_m$, $\beta_m$, $x_m$, $\omega_m$ and $q_m$. On $A_m$, the new direction $\omega'$ has the density $p$, and $u_m$ is uniform on $[0, 1)$ and independent of $\omega'$, so

$$E\big[\mathbf{1}[A_{m+1}]\, \beta_{m+1}\, g(x_{m+1}, \omega_{m+1}) \,\big|\, \text{history}\big] = \mathbf{1}[A_m]\, \beta_m \int \frac{f \cos\theta'}{p(\omega')\, q_m}\, q_m\, g(h(x_m, \omega'), -\omega')\, p(\omega')\, d\omega'.$$

The factor $q_m$ is the probability of $u_m < q_m$. When $q_m = 0$, condition (b) says that the integrand is $0$ where $p > 0$, and the left side is $0$ as well, so the equation holds with both sides $0$. Otherwise $q_m$ and $p$ cancel, and by condition (a) the integral over $\{p > 0\}$ equals the integral over all directions where $f \cos\theta' > 0$, so the right side is $\mathbf{1}[A_m]\, \beta_m\, (K g)(x_m, \omega_m)$. Taking the expected value and using the hypothesis for $m$ with the function $K g \ge 0$ gives $(K^m K g)(x_0, \omega_0) = (K^{m+1} g)(x_0, \omega_0)$. $\square$

**Sum over the vertices.** Each term of $F$ is not negative, so by monotone convergence

$$E[F] = \sum_{k \ge 0} E\big[\mathbf{1}[A_k]\, \beta_k\, L_e(x_k, \omega_k)\big] = \sum_{k \ge 0} (K^k L_e)(x_0, \omega_0),$$

by the lemma with $g = L_e$. This holds also when the sum is infinite.

**The sum is the solution.** If $\|K\| \le \rho_{\max} < 1$ in the supremum norm, which holds when every directional albedo $\int f \cos\theta_i\, d\omega_i$ is at most $\rho_{\max}$, then $\|K^k L_e\| \le \rho_{\max}^k \|L_e\|$, the [Neumann series](/neumann-series/) converges, and its sum $S$ has $S = L_e + K S$. Any bounded solution $L$ has $L - S = K (L - S)$, so $\|L - S\| \le \rho_{\max} \|L - S\|$ and $L = S$.

**The depth limit.** With a limit of $B$ bounces, the path returns at vertex $B$ after line L4, and $q = 1$ before. The terms with $k > B$ are $0$, so the same steps give $E[F] = \sum_{k \le B} (K^k L_e)(x_0, \omega_0)$. All terms are not negative, so this is at most $L$, and less than $L$ when some term with $k > B$ is positive.

**Termination.** If after some depth $q \le q_{\max} < 1$ at every vertex, the probability that a path reaches $k$ more vertices is at most $q_{\max}^k$, so a path stops with probability 1 and its number of vertices has a finite mean.

**RENDER.** A camera direction $\omega$ with density $p_j(\omega) > 0$ wherever $W_j(\omega) > 0$ gives $E[W_j(\omega)\, F(c, \omega) / p_j(\omega)] = \int W_j(\omega)\, L(h(c, \omega), -\omega)\, d\omega = I_j$, by the claim conditioned on $\omega$. The $N$ estimates of a pixel are independent with this mean, so their average is unbiased. If one estimate has a finite variance $\sigma^2$, the average has the variance $\sigma^2 / N$, and the sample variance divided by $N$ is an unbiased estimate of it.
