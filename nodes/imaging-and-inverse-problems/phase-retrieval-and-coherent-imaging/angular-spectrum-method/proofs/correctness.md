---
title: The angular spectrum method is exact for periodic band-limited fields
proves: [correctness]
status: full
---

The setting is that of the algorithm. The grid has $n_1 \times n_2$ samples with spacing $d$, so the periods are $L_1 = n_1 d$ along $y$ and $L_2 = n_2 d$ along $x$. The DFT index $k$ along an axis of $n$ samples stands for the signed index $\bar k$, with $\bar k = k$ if $2k < n$ and $\bar k = k - n$ otherwise, and for the frequency $\bar k / (n d)$. Let $\Lambda$ be the set of frequency pairs $f = (f_x, f_y) = (\bar l / L_2, \bar k / L_1)$ for $0 \le k < n_1$ and $0 \le l < n_2$. The wavelength is $\lambda > 0$, and the time dependence is $e^{-i\omega t}$, so a wave $e^{2\pi i (f \cdot r + f_z z)}$ with $f_z > 0$ travels toward $+z$.

**The model.** A field $U(x, y, z)$ on $z \ge 0$ is a *grid field* if it has the form

$$U(x, y, z) = \sum_{f \in \Lambda} c_f(z)\, e^{2\pi i (f_x x + f_y y)} \tag{1}$$

with twice differentiable $c_f$, if it solves the Helmholtz equation $\nabla^2 U + (2\pi/\lambda)^2 U = 0$ for $z > 0$, if each $c_f$ is bounded on $z \ge 0$, and if no wave of (1) travels toward $-z$. The last condition says that no source lies at $z > 0$.

**Lemma 1 (the coefficients).** For a grid field, put $w_f = 1/\lambda^2 - |f|^2$. If $w_f > 0$, then $c_f(z) = c_f(0)\, e^{2\pi i z \sqrt{w_f}}$. If $w_f < 0$, then $c_f(z) = c_f(0)\, e^{-2\pi z \sqrt{-w_f}}$. If $w_f = 0$, then $c_f(z) = c_f(0)$.

*Proof.* The functions $e^{2\pi i f \cdot r}$ for $f \in \Lambda$ are orthogonal on one period. Put (1) into the Helmholtz equation and take the inner product with $e^{2\pi i f \cdot r}$. Each Laplacian in $x$ and $y$ gives the factor $-4\pi^2 |f|^2$, so

$$c_f''(z) + 4\pi^2 w_f\, c_f(z) = 0.$$

For $w_f > 0$ the solutions are $A e^{2\pi i z\sqrt{w_f}} + B e^{-2\pi i z\sqrt{w_f}}$. The second term is a wave that travels toward $-z$, so $B = 0$ and $A = c_f(0)$. For $w_f < 0$ the solutions are $A e^{-2\pi z\sqrt{-w_f}} + B e^{2\pi z\sqrt{-w_f}}$, and the bound on $c_f$ forces $B = 0$. For $w_f = 0$ the solutions are $A + B z$, and the bound forces $B = 0$. $\square$

**Lemma 2 (sampling).** Let $u_{ij} = U(j d, i d, 0)$ for a grid field $U$. Then the 2D DFT of $u$ is $\hat u_{kl} = n_1 n_2\, c_f(0)$, where $f$ is the frequency pair of the index $(k, l)$.

*Proof.* At the samples, $e^{2\pi i (f_x j d + f_y i d)} = e^{2\pi i (\bar l j / n_2 + \bar k i / n_1)} = e^{2\pi i (l j / n_2 + k i / n_1)}$, because $\bar l - l$ is a multiple of $n_2$ and $\bar k - k$ is a multiple of $n_1$. So $u$ is the inverse DFT of the array $n_1 n_2\, c_f(0)$, and the map from $\Lambda$ to the index pairs is a bijection. The DFT inverts the inverse DFT. $\square$

**Theorem.** Let $U$ be a grid field, let $u$ hold its samples at $z = 0$, and let $v$ be the output of ANGULAR-SPECTRUM$(u, d, \lambda, z)$ for $z \ge 0$ without the band limit. Write $U = U_p + U_e$, where $U_p$ holds the terms of (1) with $w_f > 0$ and $U_e$ the rest. Then

$$v_{ij} = U_p(j d, i d, z) \quad \text{for all } i, j,$$

and the dropped part is small: $\|U_e(\cdot, z)\|_{\mathrm{grid}} \le e^{-2\pi z \gamma} \|U_e(\cdot, 0)\|_{\mathrm{grid}}$, where $\|\cdot\|_{\mathrm{grid}}$ is the Euclidean norm of the samples and $\gamma = \min\{\sqrt{-w_f} : f \in \Lambda, w_f < 0\}$, provided that no $f \in \Lambda$ has $w_f = 0$.

*Proof.* By Lemma 2, line L1 gives $\hat u_{kl} = n_1 n_2 c_f(0)$. Line L4 computes $w_f$. Lines L5 and L6 form $V_{kl} = n_1 n_2 c_f(0) e^{2\pi i z\sqrt{w_f}}$ if $w_f > 0$ and $V_{kl} = 0$ otherwise. By Lemma 1, $V_{kl} = n_1 n_2 c_f(z)$ for $w_f > 0$. Line L7 takes the inverse DFT, and by the computation in the proof of Lemma 2 it returns the samples of $\sum_{w_f > 0} c_f(z) e^{2\pi i f \cdot r}$, which is $U_p$ at $z$.

For the bound, the samples of $U_e(\cdot, z)$ have the DFT $n_1 n_2 c_f(z)$ for $w_f < 0$ and $0$ elsewhere (no $w_f = 0$ by hypothesis). By Lemma 1, $|c_f(z)| = |c_f(0)| e^{-2\pi z\sqrt{-w_f}} \le |c_f(0)| e^{-2\pi z \gamma}$. By the [Parseval theorem](/parseval-theorem/) for the DFT, the grid norm squared is $(n_1 n_2)^{-1}$ times the sum of the squared DFT magnitudes, so the bound on each term gives the bound on the norm. $\square$

**Corollary (properties of the propagator).** Let $P_z$ be the map $u \mapsto v$ of the algorithm without the band limit, and let $B$ be the projector that keeps the DFT entries with $w_f > 0$ and sets the rest to zero, so that $B = P_0$. Then for all real $z$, $z_1$ and $z_2$:

1. $P_{z_1} P_{z_2} = P_{z_1 + z_2}$.
2. $P_{-z} P_z = B$, and $P_{-z} P_z = I$ if every $f \in \Lambda$ has $w_f > 0$.
3. $\|P_z u\| = \|B u\| \le \|u\|$, with equality if $u$ has no DFT entry with $w_f \le 0$.
4. $P_z^* = P_{-z}$, so back propagation is the adjoint of propagation.

*Proof.* In the DFT basis, $P_z$ is the diagonal map with entries $h_f(z) = e^{2\pi i z\sqrt{w_f}}$ for $w_f > 0$ and $0$ otherwise. Item 1 follows from $h_f(z_1) h_f(z_2) = h_f(z_1 + z_2)$ for $w_f > 0$ and $0 \cdot 0 = 0$ otherwise. Item 2 is item 1 with $z_1 = -z$ and $z_2 = z$, since $h_f(0) = 1$ for $w_f > 0$. Item 3 follows from $|h_f(z)| = 1$ for $w_f > 0$ and the Parseval theorem. For item 4, the unnormalized DFT is $\sqrt{n_1 n_2}$ times a unitary map $Q$, so $P_z = Q^* D_z Q$ with the diagonal $D_z$, and $P_z^* = Q^* \overline{D_z} Q$. Since $\overline{h_f(z)} = h_f(-z)$, this is $P_{-z}$. $\square$

**Lemma 3 (the band limit).** Let $\Delta u = 1/(n d)$ be the frequency spacing along one axis, and consider the phase $\varphi(f) = 2\pi z\sqrt{1/\lambda^2 - f^2}$ along that axis for $z > 0$ and $0 \le f < 1/\lambda$. The sampled transfer function meets the Nyquist condition $|\varphi'(f)|\, \Delta u \le \pi$ exactly for

$$f \le f_{\lim} = \frac{1}{\lambda \sqrt{(2 \Delta u\, z)^2 + 1}}.$$

*Proof.* $|\varphi'(f)| = 2\pi z f / \sqrt{1/\lambda^2 - f^2}$, which increases with $f$. The condition $2\pi z f \Delta u \le \pi \sqrt{1/\lambda^2 - f^2}$ is, after squaring both nonnegative sides, $4 z^2 \Delta u^2 f^2 \le 1/\lambda^2 - f^2$, that is $f^2 (4 z^2 \Delta u^2 + 1) \le 1/\lambda^2$. Take the square root. $\square$

Lemma 3 is a statement about the sampling of $H$, which matters for the aperiodic problem with a padded grid. In the periodic model of the theorem the method is exact without any band limit.
