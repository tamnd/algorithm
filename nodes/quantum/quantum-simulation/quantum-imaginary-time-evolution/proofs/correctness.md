---
title: The imaginary-time flow converges to the ground state at rate e^(-2 tau gap), and QITE with the whole register as domain follows the normalized product of the e^(-dtau h_m) to within O(e^(2 lambda tau) tau dtau)
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = \sum_{m=1}^Mh_m$ on $n$ qubits with $h_m = c_mP_m$, real $c_m$ and Pauli strings $P_m$; $\lambda = \sum_m|c_m|$ and $N = 2^n$. All states are unit vectors. For unit vectors $x, y$ let $\theta(x, y) = \arccos\mathrm{Re}\langle x|y\rangle \in [0, \pi]$, the angle between them as vectors of the real space $\mathbb{R}^{2N}$. It is the geodesic distance on the unit sphere, so it satisfies the triangle inequality, every unitary preserves it, and $\|x - y\| = 2\sin(\theta/2)$ gives $\|x - y\| \le \theta(x, y) \le \tfrac\pi2\|x - y\|$.

## Part 1: the exact flow

Let $|v_i\rangle$ be an orthonormal eigenbasis of $H$ with eigenvalues $\mu_i$, let $E_0 = \min_i\mu_i$, let $\Delta > 0$ be the distance from $E_0$ to the next distinct eigenvalue, and write $|\psi_0\rangle = \sum_ia_i|v_i\rangle$ with $w_i = |a_i|^2$. Let $w_0 = \sum_{i:\mu_i = E_0}w_i$ be the ground space weight, and $|\psi(\tau)\rangle = e^{-\tau H}|\psi_0\rangle/\|e^{-\tau H}|\psi_0\rangle\|$.

**Claim 1.** If $w_0 > 0$, the weight of $|\psi(\tau)\rangle$ outside the ground space is at most $((1 - w_0)/w_0)e^{-2\tau\Delta}$, and $E(\tau) - E_0 \le (E_{\max} - E_0)((1 - w_0)/w_0)e^{-2\tau\Delta}$.

*Proof.* $e^{-\tau H}|\psi_0\rangle = \sum_ia_ie^{-\tau\mu_i}|v_i\rangle$, so the weight on $|v_i\rangle$ after normalization is $w_ie^{-2\tau\mu_i}/Z$ with $Z = \sum_iw_ie^{-2\tau\mu_i} \ge w_0e^{-2\tau E_0}$. Every $i$ outside the ground space has $\mu_i \ge E_0 + \Delta$, so the weight outside is at most $(1 - w_0)e^{-2\tau(E_0 + \Delta)}/(w_0e^{-2\tau E_0})$. For the energy, $E(\tau) - E_0 = \sum_i(\mu_i - E_0)w_ie^{-2\tau\mu_i}/Z$, and only terms outside the ground space contribute, each with $\mu_i - E_0 \le E_{\max} - E_0$. If $w_0 = 0$ the flow stays in the span of the excited eigenvectors and never reaches the ground space. $\square$

So the infidelity with a ground state of a nondegenerate $H$ falls as $e^{-2\tau\Delta}$, and $\tau = \Delta^{-1}\cdot\tfrac12\ln((1 - w_0)/(w_0\epsilon))$ suffices for infidelity $\epsilon$.

**Claim 2.** $dE/d\tau = -2(\langle H^2\rangle - \langle H\rangle^2) \le 0$, with the expectations in $|\psi(\tau)\rangle$.

*Proof.* $E(\tau) = f/g$ with $f = \langle\psi_0|He^{-2\tau H}|\psi_0\rangle$ and $g = \langle\psi_0|e^{-2\tau H}|\psi_0\rangle$. Then $f' = -2\langle\psi_0|H^2e^{-2\tau H}|\psi_0\rangle$ and $g' = -2f$, so $E' = f'/g - fg'/g^2 = -2\langle H^2\rangle + 2\langle H\rangle^2$, since $\langle X\rangle = \langle\psi_0|Xe^{-2\tau H}|\psi_0\rangle/g$ for $X$ commuting with $H$. A variance is nonnegative. $\square$

## Part 2: one QITE substep with the whole register as domain

Fix a substep for the term $h = cP$ and the current state $|\psi\rangle$. Let $\phi' = e^{-\Delta\tau h}|\psi\rangle/\sqrt c'$ with $c' = \langle\psi|e^{-2\Delta\tau h}|\psi\rangle$ (line L4; we write $c'$ to keep $c$ for the coefficient), and $\delta = (\phi' - \psi)/\Delta\tau$ (line L5). The strings $\sigma_I$ are all $N^2 - 1$ Pauli strings other than the identity.

**Claim 3 (the least-squares problem).** For real $a$, $\|\delta + i\sum_Ia_I\sigma_I\psi\|^2$ is minimized exactly by the solutions of $\mathrm{Re}(S)a = b$ with $S_{IJ} = \langle\psi|\sigma_I\sigma_J|\psi\rangle$ and $b_I = \mathrm{Im}\langle\delta|\sigma_I|\psi\rangle$ (line L6).

*Proof.* Expand: $\|\delta\|^2 + \sum_{I,J}a_Ia_J\langle\sigma_I\psi|\sigma_J\psi\rangle + 2\mathrm{Re}\sum_Ia_I\,i\langle\delta|\sigma_I\psi\rangle$. The double sum is real for real $a$ and equals $\sum a_Ia_J\mathrm{Re}S_{IJ}$, a positive semidefinite quadratic form, and $\mathrm{Re}(i z) = -\mathrm{Im}z$. So the function is $\|\delta\|^2 + a^{\mathsf T}\mathrm{Re}(S)a - 2b^{\mathsf T}a$, a convex quadratic, whose minimizers are the solutions of the normal equations $\mathrm{Re}(S)a = b$. $\square$

**Claim 4 (reachable directions).** The set $\{-iA\psi : A$ Hermitian and traceless$\}$ is the set of all $v$ with $\mathrm{Re}\langle\psi|v\rangle = 0$, and for each such $v$ there is such an $A$ with $\|A\|_F \le 5\|v\|$.

*Proof.* If $A$ is Hermitian, $\langle\psi|{-iA}|\psi\rangle = -i\langle A\rangle$ is purely imaginary, so the condition is necessary. Conversely let $\mathrm{Re}\langle\psi|v\rangle = 0$, so $\langle\psi|v\rangle = it$ with real $t$ and $|t| \le \|v\|$. Let $A_1 = i(|v\rangle\langle\psi| - |\psi\rangle\langle v|)$ and $A_2 = t|\psi\rangle\langle\psi|$, both Hermitian. Then $-iA_1\psi = v - \langle v|\psi\rangle\psi = v + it\psi$ and $-iA_2\psi = -it\psi$, so $-i(A_1 + A_2)\psi = v$. The trace of $A_1 + A_2$ is $i(it - (-it)) + t = -t$. With $B = |\psi\rangle\langle\psi| - I/N$, which is traceless and has $B\psi = (1 - 1/N)\psi$, let $A = A_1 + A_2 + (t/N)I - (t/(N - 1))B$. It is traceless, and $-iA\psi = v - i(t/N)\psi + i(t/(N - 1))(1 - 1/N)\psi = v$. In the Frobenius norm, $\|A_1\|_F \le 2\|v\|$, $\|A_2\|_F = |t|$, $\|(t/N)I\|_F = |t|/\sqrt N$ and $\|B\|_F \le 1$, so $\|A\|_F \le 2\|v\| + |t|(1 + 1/\sqrt N + 1/(N - 1)) \le 5\|v\|$ for $N \ge 2$. $\square$

A traceless Hermitian $A$ is exactly $\sum_Ia_I\sigma_I$ with real $a_I$, and $\|A\|_F^2 = N\sum_Ia_I^2$. So, with $v = \delta - \mathrm{Re}\langle\psi|\delta\rangle\psi$: the residual of Claim 3 is at least the component of $\delta$ along $\psi$ in the real sense, which is $\mathrm{Re}\langle\psi|\delta\rangle\psi$, and it is reached exactly by Claim 4. Every minimizer satisfies $-iA\psi = v$, because the real-linear map $a \mapsto -i\sum a_I\sigma_I\psi$ has the real orthogonal complement of $\psi$ as its image and $v$ is the projection of $\delta$ onto it. The minimum-norm minimizer (line L7) has $\|a\| \le$ the norm of the coefficients of the $A$ of Claim 4, so $\|A\| \le \|A\|_F \le 5\|v\| \le 5\|\delta\|$.

**Claim 5 (one substep).** $\|\delta\| \le |c|$, and $\|e^{-i\Delta\tau A}\psi - \phi'\| \le 13c^2\Delta\tau^2$.

*Proof.* The curve $\phi_s = e^{-sh}\psi/\|e^{-sh}\psi\|$, $s \in [0, \Delta\tau]$, joins $\psi$ to $\phi'$ on the unit sphere, and $d\phi_s/ds = -(h - \langle h\rangle_s)\phi_s$, whose norm is the standard deviation of $h$ in $\phi_s$, at most $|c|$ since $h$ has eigenvalues $\pm c$. So $\|\phi' - \psi\| \le |c|\Delta\tau$ and $\|\delta\| \le |c|$. Next, $e^{-i\Delta\tau A}\psi = \psi - i\Delta\tau A\psi + R$ with $\|R\| \le (\Delta\tau\|A\|)^2/2$, because $|e^{-ix} - 1 + ix| \le x^2/2$ for real $x$ and $A$ is Hermitian. With $-iA\psi = v = \delta - \mathrm{Re}\langle\psi|\delta\rangle\psi$ and $\phi' = \psi + \Delta\tau\delta$,
$$e^{-i\Delta\tau A}\psi - \phi' = -\Delta\tau\,\mathrm{Re}\langle\psi|\delta\rangle\,\psi + R.$$
Since $\psi$ and $\phi'$ are unit vectors, $\Delta\tau\,\mathrm{Re}\langle\psi|\delta\rangle = \mathrm{Re}\langle\psi|\phi'\rangle - 1 = -\|\phi' - \psi\|^2/2$, of size at most $c^2\Delta\tau^2/2$. With $\|A\| \le 5|c|$, $\|R\| \le 25c^2\Delta\tau^2/2$. The sum is at most $13c^2\Delta\tau^2$. $\square$

## Part 3: many substeps

Let $\mathcal{N}_m(x) = e^{-\Delta\tau h_m}x/\|e^{-\Delta\tau h_m}x\|$ on unit vectors, and let $y_0 = x_0 = \psi_0$. The target sequence applies $\mathcal{N}_1, \ldots, \mathcal{N}_M$ in turn, $T$ times; QITE applies to $x_k$ the unitary $U_k$ computed from $x_k$.

**Claim 6.** $\theta(\mathcal{N}_m(x), \mathcal{N}_m(y)) \le e^{2\Delta\tau|c_m|}\,\theta(x, y)$ for unit vectors $x, y$.

*Proof.* Let $G = e^{-\Delta\tau h_m}$, with $\|G\| = e^{\Delta\tau|c_m|}$ and $\|Gz\| \ge e^{-\Delta\tau|c_m|}$ for unit $z$. Take the geodesic $z(s)$ from $x$ to $y$ of length $\theta(x, y)$. The derivative of $\mathcal{N}_m$ at $z$ in the direction $\dot z$ is $(G\dot z)/\|Gz\|$ minus its real component along $\mathcal{N}_m(z)$, so its norm is at most $\|G\|\|\dot z\|/\|Gz\| \le e^{2\Delta\tau|c_m|}\|\dot z\|$. The image curve joins $\mathcal{N}_m(x)$ to $\mathcal{N}_m(y)$ on the sphere and has length at most $e^{2\Delta\tau|c_m|}\theta(x, y)$, and the geodesic distance is at most the length of any joining curve on the sphere. $\square$

Number the substeps $k = 1, \ldots, K = TM$, with term $m(k)$. By the triangle inequality, Claim 5 (with $\theta \le \tfrac\pi2\|\cdot\|$) and Claim 6,
$$\theta(x_k, y_k) \le \theta(U_kx_{k-1}, \mathcal{N}_{m(k)}(x_{k-1})) + \theta(\mathcal{N}_{m(k)}(x_{k-1}), \mathcal{N}_{m(k)}(y_{k-1})) \le \tfrac\pi2\cdot13c_{m(k)}^2\Delta\tau^2 + e^{2\Delta\tau|c_{m(k)}|}\theta(x_{k-1}, y_{k-1}).$$
Unrolling, and bounding each product of the factors $e^{2\Delta\tau|c_m|}$ by their product over all $K$ substeps, $e^{2\lambda T\Delta\tau} = e^{2\lambda\tau}$ with $\tau = T\Delta\tau$,
$$\theta(x_K, y_K) \le e^{2\lambda\tau}\cdot\frac{13\pi}{2}\Delta\tau^2\cdot T\sum_mc_m^2 \le 21\,e^{2\lambda\tau}\,\tau\,\Delta\tau\sum_mc_m^2.$$
At fixed $\tau$ this goes to 0 as $\Delta\tau \to 0$. $\blacksquare$

**What is not proved here.** The bound is for the whole register as the domain; for smaller domains Claim 4 fails and the residual can be of order 1, as the example of the page shows for $r = 0$. The distance from the target product $(\prod_m e^{-\Delta\tau h_m})^T\psi_0$, normalized, to the exact $e^{-\tau H}\psi_0$, normalized, goes to 0 as $\Delta\tau \to 0$ at fixed $\tau$ by the Lie product formula for the matrix exponential; the rate is first order in $\Delta\tau$, with constants that depend on the commutators of the terms and on $\|e^{-\tau H}\psi_0\|^{-1}$.
