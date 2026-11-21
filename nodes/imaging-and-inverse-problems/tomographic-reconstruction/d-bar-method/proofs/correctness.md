---
title: What the D-bar code computes, and why its fixed-point loop converges
proves: [correctness]
status: full
---

We use the notation of the page. $\Omega$ is the unit disk, $z = x_1 + i x_2$, and $\gamma$ is a conductivity with $\gamma = 1$ near $\partial\Omega$. $\Lambda_\gamma$ is the Dirichlet-to-Neumann map, $e_z(k) = \exp(i(kz + \overline{kz}))$, and for $k \in \mathbb{C}$
$$\mathbf{t}^{\exp}(k) = \int_{\partial\Omega} e^{i \bar k \bar z} (\Lambda_\gamma - \Lambda_1) e^{i k z} \, ds(z).$$
The truncated D-bar equation with cutoff $R$ is
$$\mu(z, k) = 1 + \frac{1}{4\pi^2} \int_{|k'| \le R} \frac{\mathbf{t}(k')\, e_{-z}(k')\, \overline{\mu(z, k')}}{(k - k')\, \overline{k'}} \, dA(k'), \tag{1}$$
and the output is $\gamma_R(z) = \operatorname{Re} \mu(z, 0)^2$.

Three facts are cited and not proved here. (a) Nachman 1996: for $\gamma$ with two derivatives in $L^p$, $p > 1$, the exact scattering transform $\mathbf{t}$ (with the special solutions $\psi$ in place of $e^{ikz}$) has no exceptional points, equation (1) with $R = \infty$ and $\mathbf{t}$ has a unique solution with $\mu(z, \cdot) - 1$ vanishing at infinity, and $\gamma(z) = \mu(z, 0)^2$. (b) Knudsen, Lassas, Mueller and Siltanen 2009: cutting $\mathbf{t}$ at a radius $R$ chosen from the noise level gives a regularization strategy. (c) The function $1/(\pi k)$ is a fundamental solution of $\bar\partial_k = \frac12(\partial_{k_1} + i \partial_{k_2})$, so $u(k) = \frac{1}{\pi}\int F(k')/(k - k')\, dA(k')$ solves $\bar\partial u = F$ for a continuous $F$ of compact support; this is how (1) comes from the D-bar equation $\bar\partial_k \mu = \frac{1}{4\pi \bar k} \mathbf{t}(k) e_{-z}(k) \overline{\mu}$. The code uses $\mathbf{t}^{\exp}$, not $\mathbf{t}$, so (a) does not apply to its output; the page treats that gap as a heuristic with measurements.

**Theorem 1 (the scattering transform of a radial conductivity).** Let $\gamma$ be radial, so that $\Lambda_\gamma e^{i n \varphi} = \lambda_{|n|} e^{i n \varphi}$ on $\partial\Omega$ with $\lambda_0 = 0$ and $\lambda_n$ real. Then
$$\mathbf{t}^{\exp}(k) = 2\pi \sum_{n \ge 1} (-1)^n \frac{|k|^{2n}}{(n!)^2} (\lambda_n - n),$$
a real function of $|k|$, provided the sum converges absolutely (it does when $|\lambda_n - n| \le C n$, which holds for the conductivities of the page).

*Proof.* On $\partial\Omega$, $z = e^{i\varphi}$, and $e^{ikz} = \sum_{m \ge 0} \frac{(ik)^m}{m!} e^{i m \varphi}$, a series that converges uniformly with all derivatives. $\Lambda_1 e^{i m \varphi} = |m| e^{i m \varphi}$, so
$$(\Lambda_\gamma - \Lambda_1) e^{ikz} = \sum_{m \ge 1} \frac{(ik)^m}{m!} (\lambda_m - m) e^{i m \varphi}.$$
Also $e^{i \bar k \bar z} = \sum_{n \ge 0} \frac{(i \bar k)^n}{n!} e^{-i n \varphi}$. Multiply the two series and integrate over $\varphi \in [0, 2\pi)$ with $ds = d\varphi$. Only the products with $n = m$ survive, each with the factor $2\pi$:
$$\mathbf{t}^{\exp}(k) = 2\pi \sum_{m \ge 1} \frac{(ik)^m (i \bar k)^m}{(m!)^2} (\lambda_m - m) = 2\pi \sum_{m \ge 1} \frac{(-1)^m |k|^{2m}}{(m!)^2} (\lambda_m - m).$$
The exchange of sum and integral is allowed because both series converge absolutely and uniformly in $\varphi$. Each term is real and depends on $|k|$ only. $\square$

For $\gamma = 1$ every $\lambda_n - n$ is 0, so $\mathbf{t}^{\exp} = 0$, equation (1) gives $\mu = 1$, and the output is exactly 1. The code computes the sum with the terms $|k|^{2n}/(n!)^2$ built by the recursion $\tau_n = \tau_{n-1} |k|^2 / n^2$.

**Theorem 2 (the center value for a radial real transform).** Let $\mathbf{t}$ be real, radial ($\mathbf{t}(k) = t(|k|)$), continuous on $[0, R]$, with $|t(s)| \le C s^2$ near 0. Let
$$m(r) = \exp\Big(-\frac{1}{2\pi}\int_{\min(r, R)}^{R} \frac{t(s)}{s}\, ds\Big), \qquad r \ge 0.$$
Then $\mu(0, k) = m(|k|)$ solves (1) at $z = 0$, and the output of the method at the center is
$$\gamma_R(0) = m(0)^2 = \exp\Big(-\frac{1}{\pi}\int_0^R \frac{t(s)}{s}\, ds\Big).$$
If the solution of (1) is unique (for example under the condition of Theorem 3), this is the value the method returns.

*Proof.* The integral defining $m$ is finite because $t(s)/s = O(s)$ near 0. At $z = 0$, $e_{-z} = 1$. Put $\mu(0, k') = m(s)$ with $s = |k'|$, a real function, so $\overline{\mu} = m$. With $1/\overline{k'} = k'/s^2$, the right side of (1) is
$$1 + \frac{1}{4\pi^2} \int_0^R \frac{t(s)\, m(s)}{s^2} \, s \, ds \int_0^{2\pi} \frac{k'}{k - k'} \, d\theta, \qquad k' = s e^{i\theta}.$$
For the inner integral write $\frac{k'}{k - k'} = -1 + \frac{k}{k - k'}$. If $s < |k|$, then $\frac{1}{k - k'} = \frac{1}{k}\sum_{j \ge 0} (k'/k)^j$ and the mean over $\theta$ is $1/k$, so the mean of $k'/(k - k')$ is 0. If $s > |k|$, then $\frac{1}{k - k'} = -\frac{1}{k'}\sum_{j \ge 0} (k/k')^j$, every term has mean 0, and the mean of $k'/(k - k')$ is $-1$. (The circle $s = |k|$ has measure 0.) So the right side is
$$1 - \frac{1}{2\pi} \int_{\min(|k|, R)}^{R} \frac{t(s)\, m(s)}{s} \, ds.$$
On $[0, R]$, $m'(s) = m(s) t(s)/(2\pi s)$ and $m(R) = 1$, so the integral is $2\pi \int_{\min(|k|,R)}^{R} m'(s)\, ds = 2\pi\,(1 - m(\min(|k|, R)))$, and for $|k| > R$ it is 0 with $m(|k|) = 1$. In both cases the right side equals $m(|k|)$. So $\mu(0, \cdot) = m(|\cdot|)$ solves (1), and $\operatorname{Re} \mu(0, 0)^2 = m(0)^2$. $\square$

By Theorem 1, $\mathbf{t}^{\exp}$ of a radial conductivity satisfies the hypotheses, with $t(s) \approx -2\pi s^2 (\lambda_1 - 1)$ near 0. The function `gamma0_reference` evaluates the formula by Simpson's rule; it is the reference against which the tests check the grid solver at $z = 0$.

**Theorem 3 (the discrete fixed-point loop).** Let $k_1, \dots, k_N$ be the grid points, and let $w_l = \frac{h^2}{4\pi^2} \mathbf{t}(k_l) e_{-z}(k_l) / \overline{k_l}$ for $k_l \ne 0$ and $w_l = 0$ for $k_l = 0$ (lines L2 and L4). Define the map $T$ on $\mathbb{C}^N$ by
$$T(v)_j = 1 + \sum_{l \ne j} \frac{w_l\, \overline{v_l}}{k_j - k_l}$$
(line L7), and let $q = \max_j \sum_{l \ne j} |w_l| / |k_j - k_l|$. If $q < 1$, then $T$ has exactly one fixed point $v^*$, the iterates $v^{(0)} = (1, \dots, 1)$, $v^{(i+1)} = T(v^{(i)})$ satisfy $\|v^{(i)} - v^*\|_\infty \le q^i \|v^{(0)} - v^*\|_\infty$, and when the loop stops at line L8 with $\|v^{(i+1)} - v^{(i)}\|_\infty < \varepsilon$, the returned vector $v = v^{(i+1)}$ has residual $\|T(v) - v\|_\infty < q \varepsilon$ and error $\|v - v^*\|_\infty < q \varepsilon / (1 - q)$.

*Proof.* $T$ is not complex-linear because of the conjugate, but $T(u) - T(v)$ has entries $\sum_{l \ne j} w_l \overline{(u_l - v_l)}/(k_j - k_l)$, whose modulus is at most $\sum_{l \ne j} |w_l| |u_l - v_l| / |k_j - k_l| \le q \|u - v\|_\infty$. So $T$ is a contraction of the complete metric space $(\mathbb{C}^N, \|\cdot\|_\infty)$, and the [Banach fixed-point theorem](/banach-fixed-point-theorem/) gives the unique fixed point and the rate $\|v^{(i)} - v^*\| = \|T(v^{(i-1)}) - T(v^*)\| \le q \|v^{(i-1)} - v^*\|$. For the stopping test, $\|T(v^{(i+1)}) - v^{(i+1)}\| = \|T(v^{(i+1)}) - T(v^{(i)})\| \le q \|v^{(i+1)} - v^{(i)}\| < q\varepsilon$, and $\|v - v^*\| \le \|v - T(v)\| + \|T(v) - T(v^*)\| \le q\varepsilon + q \|v - v^*\|$ gives the error bound. $\square$

The same argument works for the continuous equation (1) in the sup norm on $|k| \le R$, with
$$q_{\text{cont}} = \frac{1}{4\pi^2} \sup_k \int_{|k'| \le R} \frac{|\mathbf{t}(k')|}{|k - k'|\,|k'|}\, dA(k') \le \frac{R}{2\pi} \sup_{0 < |k'| \le R} \frac{|\mathbf{t}(k')|}{|k'|},$$
because among sets of area $\pi R^2$ the integral of the decreasing function $1/|k - k'|$ is largest on the disk of radius $R$ centered at $k$, where it is $2\pi R$. So (1) has a unique bounded solution whenever $R \sup |\mathbf{t}(k')|/|k'| < 2\pi$. This is a sufficient condition only. The code does not check $q$; if the loop does not settle in the given number of iterations it raises an error instead of returning a value. In the smooth example of the page, $q = 0.085$ at $z = 0$ with $R = 3$ and $h = 0.3$ (a measurement of this run).

**What the code returns.** Put together: line L2 computes $\mathbf{t}^{\exp}$ exactly up to the truncation of the series at the number of given eigenvalues (Theorem 1). Lines L5 to L8 compute the unique solution of the discrete equation to the stated tolerance when $q < 1$ (Theorem 3). The discrete equation is the midpoint rule for (1) with the singular cell left out; for a continuous integrand the left-out cell contributes $O(h)$, and the test of the Cauchy transform of $e^{-|k|^2}$ shows this first-order error. At $z = 0$ with a radial conductivity, the result converges to the closed form of Theorem 2 as $h \to 0$. That $\gamma_R$ is close to $\gamma$ is not a theorem for $\mathbf{t}^{\exp}$: it rests on facts (a) and (b) for the exact $\mathbf{t}$ and on the measurements on the page.
