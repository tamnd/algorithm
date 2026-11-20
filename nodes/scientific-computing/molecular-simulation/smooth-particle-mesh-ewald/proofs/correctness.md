---
title: SPME computes a B-spline approximation of the reciprocal Ewald energy, and its forces are the exact gradient of that energy
proves: [correctness]
status: full
---

We use Gaussian units and the line numbers of the pseudocode. The box is a cube of side $L$ and volume $V$, with $K$ grid points per side, and $u_j = K r_j / L$ are the scaled coordinates of charge $j$. The cardinal B-spline of order $n$ is $M_2(x) = 1 - |x - 1|$ on $[0, 2]$ and 0 elsewhere, and
$$M_n(x) = \frac{x}{n-1} M_{n-1}(x) + \frac{n - x}{n-1} M_{n-1}(x - 1).$$
It is a piecewise polynomial of degree $n - 1$, positive on $(0, n)$ and zero outside, with $n - 2$ continuous derivatives, $\sum_g M_n(x - g) = 1$ for all $x$, and $M_n'(x) = M_{n-1}(x) - M_{n-1}(x - 1)$. The exact reciprocal energy $E_{\text{rec}} = \frac{2\pi}{V} \sum_{m \ne 0} G(m) |S(m)|^2$ with $G(m) = e^{-k^2/4\alpha^2} / k^2$ is proved on the [Ewald summation](/ewald-summation/) page.

**Claim 1 (the spline identity is exact at the grid points).** Let $\beta(m) = \sum_{j=0}^{n-1} M_n(j) e^{-2\pi i m j / K}$ and suppose $\beta(m) \ne 0$. Then for each integer $u$,
$$e^{2\pi i m u / K} = \frac{1}{\beta(m)} \sum_g M_n(u - g) e^{2\pi i m g / K}.$$

*Proof.* Put $g = u - j$. Then $\sum_g M_n(u - g) e^{2\pi i m g / K} = e^{2\pi i m u / K} \sum_j M_n(j) e^{-2\pi i m j / K}$, and the sum over $j$ is over $0 \le j \le n - 1$ because $M_n$ vanishes at the other integers. $\square$

Between grid points the right side is a spline interpolant of $e^{2\pi i m u / K}$, and Essmann et al. (1995) show that its error is bounded by a constant times $(2|m| / K)^n$. So with $b(m) = 1/\beta(m)$ for one coordinate,
$$S(m) \approx \tilde S(m) = b(m_1) b(m_2) b(m_3) \, \overline{\mathcal{F}Q(m)}, \qquad Q(g) = \sum_j q_j \prod_a M_n(u_{ja} - g_a),$$
where $\mathcal{F}$ is the forward discrete Fourier transform, and the grid indices are reduced modulo $K$, which does not change the sum because $e^{2\pi i m g / K}$ has period $K$ in $g$. The energy depends only on $|b|^2$, so the code needs $\beta$ only up to a phase: the function `bspline_moduli` uses $\sum_{j=0}^{n-2} M_n(j+1) e^{2\pi i m j/K}$, which is $e^{-2 \pi i m/K}$ times the complex conjugate of $\beta(m)$ because $M_n(0) = 0$, so it has the same modulus. For odd $n$ and $2m = K$, $\beta(m) = 0$; the code sets $|b|^2 = 0$ there, as Essmann et al. suggest.

**Claim 2 (lines L2 to L5 compute the SPME energy).** Line L5 gives
$$\tilde E = \frac12 \sum_{m \ne 0} C(m) B(m) |\mathcal{F}Q(m)|^2, \qquad C(m) = \frac{4\pi}{V} G(m), \quad B(m) = \prod_a |b(m_a)|^2,$$
which is $\frac{2\pi}{V} \sum G(m) |\tilde S(m)|^2$.

*Proof.* Line L1 puts the weight $M_n(u - \lfloor u \rfloor + j)$ on the grid point $\lfloor u \rfloor - j$ for $j = 0, \ldots, n - 1$. These are exactly the grid points $g$ with $M_n(u - g) \ne 0$, since $u - g$ must lie in $(0, n)$. Line L2 adds the products of the three weights, times $q_j$, so the array is $Q$. Line L3 takes the conjugate of its FFT, which has the modulus of $\mathcal{F}Q$. The rest is the definition. $\square$

**Claim 3 (the energy as a convolution).** Let $\phi(g) = \sum_m C(m) B(m) \overline{\mathcal{F}Q(m)}\, e^{-2\pi i m \cdot g / K}$, the array of line L6. Then $\phi$ is real, $\phi = \Theta * Q$ for the real, even kernel $\Theta$ whose transform is $C B$, and $\tilde E = \frac12 \sum_g Q(g) \phi(g)$.

*Proof.* $C(m) B(m)$ is real and even in $m$, so $\Theta(g) = \sum_m C(m) B(m) e^{-2\pi i m \cdot g / K}$ is real and even, and the convolution theorem gives $\phi = \Theta * Q$, with no factor $1/K^3$ because of this normalisation of $\Theta$. Since $Q$ is real, $\phi$ is real. Since $\sum_g Q(g) e^{-2\pi i m \cdot g / K} = \mathcal{F}Q(m)$, $\sum_g Q(g) \phi(g) = \sum_m C B |\mathcal{F}Q(m)|^2 = 2 \tilde E$. $\square$

**Claim 4 (the forces are the exact gradient).** Lines L7 and L8 give $F_j = -\nabla_{r_j} \tilde E$, and for $n \ge 3$ the forces are continuous functions of the positions.

*Proof.* $\tilde E = \frac12 Q^{\mathsf T} \Theta Q$ is a quadratic form in $Q$ with a symmetric matrix $\Theta(g, g') = \Theta(g - g')$, so $\partial \tilde E / \partial r_{ja} = \sum_g \frac{\partial Q(g)}{\partial r_{ja}} (\Theta Q)(g) = \sum_g \frac{\partial Q(g)}{\partial r_{ja}} \phi(g)$. For the first coordinate, $\frac{\partial Q(g)}{\partial r_{j1}} = q_j \frac{K}{L} M_n'(u_{j1} - g_1) M_n(u_{j2} - g_2) M_n(u_{j3} - g_3)$, and the other two are alike. The function `bspline` computes $M_n'$ by the identity $M_n' = M_{n-1}(x) - M_{n-1}(x - 1)$, from the values of $M_{n-1}$ that the recursion has at that point. Line L7 sums these products against $\phi$ and line L8 multiplies by $-q_j K / L$. $M_n$ has a continuous first derivative for $n \ge 3$, so $\tilde E$ is $C^1$ in the positions and the forces are continuous. $\square$

So a run with SPME forces and a symplectic integrator conserves a shadow of the approximate energy $\tilde E$ plus the other Ewald parts, without a drift from the mesh (see the [shadow Hamiltonian](/shadow-hamiltonian/) page for what this means and what can break it).

**Claim 5 (the net force averages to zero but is not zero).** For a shift $t \in \mathbb{R}^3$ of all charges, let $e(t) = \tilde E(r + t)$. Then $\sum_j F_j = -\nabla e(0)$, $e$ has period $L/K$ in each direction, and the mean of $\sum_j F_j(r + t)$ over $t$ in one grid cell is 0.

*Proof.* The first part is the chain rule. Moving every $u_j$ by one grid spacing moves $Q$ by one index, which does not change $|\mathcal{F}Q|$, so $e$ is periodic. The mean of the gradient of a periodic function over one period is 0. $\square$

Translation by a fraction of a cell does change $\tilde E$, so in general $\nabla e(0) \ne 0$; the test finds a net force of $10^{-2}$ of the scale of the forces at $K = 8$, $n = 4$. The exact energy is translation invariant, so the net force has the size of the force error, as Essmann et al. (1995) state.

**Cost.** Lines L1, L2 and L7 cost $\Theta(N n^3)$, lines L3 and L6 are two 3D FFTs, $\Theta(K^3 \log K)$, and lines L4 and L5 cost $\Theta(K^3)$. With $K^3 = \Theta(N)$ at a fixed density, the total is $\Theta(N \log N)$.
