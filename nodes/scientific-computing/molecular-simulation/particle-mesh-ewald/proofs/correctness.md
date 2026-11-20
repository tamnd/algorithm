---
title: PME computes an interpolated reciprocal Ewald sum whose error falls with the grid and the order, and its forces sum to zero
proves: [correctness]
status: full
---

We use Gaussian units and the line numbers of the pseudocode. The box is a cube of side $L$ and volume $V$, with $K$ grid points per side. For a charge at $r_j$, write $u_j = K r_j / L$ for its scaled coordinates. The exact reciprocal energy is
$$E_{\text{rec}} = \frac{2\pi}{V} \sum_{m \ne 0} G(m) |S(m)|^2, \qquad G(m) = \frac{e^{-k^2/4\alpha^2}}{k^2}, \qquad S(m) = \sum_j q_j e^{2\pi i m \cdot u_j / K},$$
with $k = 2\pi m / L$, as proved on the [Ewald summation](/ewald-summation/) page. For one coordinate, $W(u, g)$ is the weight that piecewise Lagrange interpolation with the $2p$ points $\lfloor u \rfloor - p + 1, \ldots, \lfloor u \rfloor + p$ gives to the point $g$, and 0 for other points.

**Claim 1 (interpolation error).** For each integer $m$ and real $u$,
$$\Bigl| e^{2\pi i m u / K} - \sum_g W(u, g) e^{2\pi i m g / K} \Bigr| \le \frac{(p!)^2}{(2p)!} \Bigl(\frac{2\pi |m|}{K}\Bigr)^{2p}.$$

*Proof.* Let $\theta = 2\pi m / K$ and $f(t) = e^{i\theta t}$. The sum is the value at $u$ of the polynomial of degree less than $2p$ that interpolates $f$ at the $2p$ points $x_j$. Apply the Lagrange remainder to the real and imaginary parts, or use the Hermite integral form of the remainder for complex $f$: the error is at most $\max |f^{(2p)}| \prod_j |u - x_j| / (2p)! = |\theta|^{2p} \prod_j |u - x_j| / (2p)!$. With $w = u - \lfloor u \rfloor \in [0, 1)$, the points below or at $\lfloor u \rfloor$ are at distances $w, 1 + w, \ldots, p - 1 + w$, each at most $1, 2, \ldots, p$, and the points above are at distances $1 - w, \ldots, p - w$, each at most $1, \ldots, p$. So the product is at most $(p!)^2$. $\square$

Essmann et al. (1995) give a sharper bound of the same form. In both, the error falls with $K$ at the rate $K^{-2p}$ for each fixed $m$, and the large $|m|$ terms, where the bound is poor, carry the small factor $G(m)$.

**Claim 2 (what lines L1 to L5 compute).** Line L3 gives $\tilde S(m) = \sum_j q_j \prod_{a=1}^{3} \sum_{g_a} W(u_{ja}, g_a) e^{2\pi i m_a g_a / K}$, and line L5 gives $\tilde E = \frac{2\pi}{V} \sum G(m) |\tilde S(m)|^2$ over $m \ne 0$ with $-K/2 < m_a \le K/2$.

*Proof.* Line L2 adds $q_j W(u_{j1}, g_1) W(u_{j2}, g_2) W(u_{j3}, g_3)$ to $Q(g)$, with the indices $g_a$ reduced modulo $K$. Since $e^{2\pi i m g / K}$ has period $K$ in $g$, the reduction does not change $\sum_g Q(g) e^{2\pi i m \cdot g / K}$, which is the complex conjugate of the forward FFT of the real array $Q$. Line L4 maps each FFT index to the representative of $m$ modulo $K$ in $(-K/2, K/2]$. $\square$

By Claim 1, $\tilde S(m) \to S(m)$ for each $m$ as $K \to \infty$ or $p \to \infty$ at fixed $m / K$ small. The wave vectors with $|m_a| > K/2$ are left out, and their terms are at most $G(m) (\sum_j |q_j|)^2$, which is small when $\pi K / L \gg 2\alpha$.

**Claim 3 (the grid field).** Line L6 gives, for each grid point $g$ and direction $d$,
$$\mathcal{E}_d(g) = \frac{4\pi}{V} \sum_m k_d G(m) \operatorname{Im}\bigl(e^{2\pi i m \cdot g / K} \overline{\tilde S(m)}\bigr),$$
with the Nyquist components $2 m_d = K$ left out, and line L7 gives $F_j = q_j \sum_g W_j(g) \mathcal{E}(g)$ with $W_j(g) = \prod_a W(u_{ja}, g_a)$.

*Proof.* The forward FFT of the array $k_d G(m) \tilde S(m)$ is $\sum_m k_d G \tilde S e^{-2\pi i m \cdot g / K}$, and $\operatorname{Im}(\tilde S e^{-i\phi}) = -\operatorname{Im}(\overline{\tilde S} e^{i\phi})$. Multiplying by $-\frac{4\pi}{V}$ gives the formula. The exact reciprocal force on a charge at $r$ is $q$ times the same expression with $g$ replaced by $u = K r / L$ and $\tilde S$ by $S$ (see the Ewald page), so $\mathcal{E}$ is the reciprocal field at the grid points, and line L7 interpolates it to the charges with the weights of line L2. $\square$

The Nyquist component is left out because $m_d = K/2$ and $m_d = -K/2$ are the same index, and the field term has opposite signs for the two. Its true weight $G(m)$ is small when the grid is fine enough.

**Claim 4 (zero net force).** $\sum_j F_j = 0$ in exact arithmetic.

*Proof.* By Claim 3 and line L2, $\sum_j F_j = \sum_g \bigl(\sum_j q_j W_j(g)\bigr) \mathcal{E}(g) = \sum_g Q(g) \mathcal{E}(g)$. For direction $d$, since $Q$ is real,
$$\sum_g Q(g) \mathcal{E}_d(g) = \frac{4\pi}{V} \sum_m k_d G(m) \operatorname{Im}\Bigl(\overline{\tilde S(m)} \sum_g Q(g) e^{2\pi i m \cdot g / K}\Bigr) = \frac{4\pi}{V} \sum_m k_d G(m) \operatorname{Im} |\tilde S(m)|^2 = 0. \qquad \square$$

**What is not claimed.** The forces are not the gradient of $\tilde E$: the gradient would need the derivative of the weights, and piecewise Lagrange weights are not differentiable at the integers. So a run with PME forces does not conserve any energy exactly, even with a symplectic integrator. Essmann et al. (1995) report this: the original PME conserves momentum to machine precision but not energy. The [smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) method makes the opposite choice.

**Cost.** Lines L1, L2 and L7 cost $\Theta(N p^3)$ for $(2p)^3$ grid points per charge. Lines L3 and L6 are four 3D FFTs of $K^3$ points, $\Theta(K^3 \log K)$. Lines L4 and L5 cost $\Theta(K^3)$. With the grid spacing $L/K$ fixed as $N$ grows at a fixed density, $K^3 = \Theta(N)$, and the total is $\Theta(N \log N)$ for the reciprocal part. The real-space part with a fixed cutoff costs $\Theta(N)$ with a cell list.
