---
title: Particle strength exchange conserves the total circulation exactly, keeps the maximum principle under the step limit, and is a consistent approximation of the Laplacian
proves: [correctness]
status: full
---

We use the pseudocode of the page in exact arithmetic. For a pair $p < q$ in the pair list, line L2 sets $w_{pq} = (\nu / \varepsilon^2)\, \eta_\varepsilon(x_p - x_q) \ge 0$, and we put $w_{qp} = w_{pq}$ and $w_{pq} = 0$ for pairs not in the list. After line L4,

$$r_p = \sum_q V_q\, w_{pq}\, (\omega_q - \omega_p), \tag{R}$$

since the pair $(p, q)$ with $p < q$ adds $V_q w_{pq} (\omega_q - \omega_p)$ to $r_p$, and the pair $(q, p)$ with $q < p$ subtracts $V_q w_{qp} (\omega_p - \omega_q)$, which is the same term.

**Claim 1 (exact conservation).** Line L5 leaves $C = \sum_p V_p \omega_p$ unchanged.

*Proof.* The change is $h \sum_p V_p r_p$. Each pair $p < q$ contributes $V_p (V_q d) + V_q (-V_p d) = 0$ to this sum, with $d = w_{pq}(\omega_q - \omega_p)$. $\square$

The proof uses only the symmetry $w_{pq} = w_{qp}$ and the form of line L4, so it holds for any positions, volumes, kernel and step. In floating point the pair contributions $V_p V_q d$ and $-V_q V_p d$ are equal and opposite, so $C$ changes only by the rounding of the sums.

**Claim 2 (maximum principle).** Let $D_p = \sum_q V_q w_{pq}$. If $h D_p \le 1$ for every $p$, then after line L5, $\min_q \omega_q^{old} \le \omega_p^{new} \le \max_q \omega_q^{old}$ for every $p$.

*Proof.* By (R),
$$\omega_p^{new} = \omega_p + h r_p = (1 - h D_p)\, \omega_p + \sum_q h V_q w_{pq}\, \omega_q.$$
The coefficients $1 - h D_p$ and $h V_q w_{pq}$ are nonnegative and add up to $1 - h D_p + h D_p = 1$. So $\omega_p^{new}$ is a convex combination of old values. $\square$

In particular a nonnegative field stays nonnegative, and the step is stable in the maximum norm: the map $\omega \mapsto \omega^{new}$ has norm 1 in $\ell^\infty$.

**Claim 3 (consistency).** Let $\eta$ be radial and integrable, with $\int |x|^3 \eta(x)\, dx < \infty$ and $\int x_i x_j \eta(x)\, dx = 2\delta_{ij}$, and let $\omega$ have bounded third derivatives. Then
$$\Delta_\varepsilon \omega(x) = \frac{1}{\varepsilon^2} \int (\omega(y) - \omega(x))\, \eta_\varepsilon(y - x)\, dy = \Delta \omega(x) + O(\varepsilon),$$
and $O(\varepsilon^2)$ if $\omega$ has bounded fourth derivatives and $\int |x|^4 \eta < \infty$. For a quadratic $\omega$ the operator is exact.

*Proof.* Substitute $y = x + \varepsilon z$, so $\eta_\varepsilon(y - x)\, dy = \eta(z)\, dz$. By Taylor's theorem, $\omega(x + \varepsilon z) - \omega(x) = \varepsilon\, z \cdot \nabla \omega + \frac{\varepsilon^2}{2} z^T H z + R$, with $H$ the Hessian of $\omega$ at $x$ and $|R| \le C \varepsilon^3 |z|^3$. A radial kernel has $\int z\, \eta = 0$, so the first term integrates to 0. The second gives $\frac{\varepsilon^2}{2} \sum_{i,j} H_{ij} \cdot 2\delta_{ij} = \varepsilon^2 \Delta\omega$. Dividing by $\varepsilon^2$ leaves $\Delta \omega$ plus a remainder of size $C \varepsilon \int |z|^3 \eta$. With fourth derivatives, the cubic term of the Taylor series integrates to 0 by symmetry, and the remainder is $O(\varepsilon^2)$. For a quadratic $\omega$ the Taylor series stops after the second term, so $R = 0$. $\square$

For $\eta = (4/\pi) e^{-|z|^2}$, $\int z_1^2 \eta = (4/\pi)(\sqrt\pi / 2)\sqrt\pi = 2$ and $\int z_1 z_2 \eta = 0$, so the kernel of the page satisfies the hypotheses.

**Claim 4 (the operator on Gaussians).** Let $g_s(x) = e^{-|x|^2/s} / (\pi s)$. Then $\Delta_\varepsilon g_s = (4 / \varepsilon^2)(g_{s + \varepsilon^2} - g_s)$.

*Proof.* $\eta_\varepsilon = 4 g_{\varepsilon^2}$ and $\int \eta = 4$, so $\Delta_\varepsilon g_s = \varepsilon^{-2}(4\, g_{\varepsilon^2} * g_s - 4 g_s)$. $g_s$ is the density of a 2D normal law with variance $s/2$ in each coordinate, and the convolution of two such densities is the density of the sum of independent variables, $g_{s + \varepsilon^2}$. $\square$

Since $g_s$ with $s = 4\nu t$ solves the heat equation, $\partial_s g_s = \Delta g_s / 4$, and Claim 4 shows that $\Delta_\varepsilon g_s$ is a forward difference in $s$ with step $\varepsilon^2$: its error against $\Delta g_s$ is $O(\varepsilon^2)$. It also shows that one Euler step of $h = \varepsilon^2 / (4\nu)$ with the exact integral maps $g_s$ to $g_{s + \varepsilon^2}$ exactly, which is the cancellation named under Pitfalls on the page. $\blacksquare$
