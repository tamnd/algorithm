---
title: The P3M split is exact, the short-range sum finds every close pair, and the mesh force conserves total momentum
proves: [correctness]
status: partial
---

We use exact arithmetic. The charges are in the periodic unit square, the mesh has $M \times M$ points $x_g = g / M$ with $M$ even, $h = 1 / M$, and $r_c < \frac12$. The exact force on charge $i$ is $F_i = \sum_j \sum_{n \in \mathbb{Z}^2}' q_i q_j \frac{x_i - x_j + n}{|x_i - x_j + n|^2}$, where the prime omits $j = i$, $n = 0$; it is the force of the potential $-q_i q_j \log r$ over all images, defined as the limit of the Ewald sums.

**Lemma 1 (the split).** For every $r > 0$, $\frac{1}{r} = \frac{e^{-\alpha^2 r^2}}{r} + \frac{1 - e^{-\alpha^2 r^2}}{r}$, and the second term is the field, at distance $r$, of a unit charge spread with the density $\frac{\alpha^2}{\pi} e^{-\alpha^2 |x|^2}$. In the periodic square, the potential of these Gaussian clouds has the Fourier coefficients $\frac{2\pi}{k^2} e^{-k^2 / (4\alpha^2)} S(k)$, $k \in 2\pi \mathbb{Z}^2 \setminus \{0\}$, with $S(k) = \sum_j q_j e^{-i k \cdot x_j}$.

*Proof.* The identity is algebra. The density has total charge $\int_0^\infty \frac{\alpha^2}{\pi} e^{-\alpha^2 \rho^2} 2\pi\rho \, d\rho = 1$, and the charge inside the radius $r$ is $1 - e^{-\alpha^2 r^2}$. In 2D, Gauss's law for the potential $-\log r$ gives the radial field (charge inside) $/ r$. The potential solves $-\nabla^2 \phi = 2\pi \rho$, and the Fourier transform of the density is $e^{-k^2 / (4\alpha^2)}$; dividing by $k^2$ gives the coefficients. The mode $k = 0$ adds a constant to the potential and no force. $\square$

So $F_i = F_i^{\text{short}} + F_i^{\text{long}}$, where $F_i^{\text{short}}$ is the sum of $q_i q_j e^{-\alpha^2 r^2} (x_i - x_j + n) / r^2$ over all images, which converges absolutely, and $F_i^{\text{long}} = q_i \sum_{k \ne 0} \frac{2\pi}{k^2} e^{-k^2/(4\alpha^2)} \, k \, \mathrm{Im}\big(S(k) e^{i k \cdot x_i}\big)$, which converges absolutely too. This is the Ewald sum that the reference function computes.

**Lemma 2 (the short-range sum).** Line L6 adds the short-range term of every ordered pair $(i, j)$, $i \ne j$, whose minimum image distance is below $r_c$, exactly once, and of no other pair. The omitted short-range force on charge $i$ is at most $\sum_{j} |q_i q_j| \, e^{-\alpha^2 r_c^2} / r_c$ times a factor that tends to 1, and in particular it is $O(e^{-\alpha^2 r_c^2})$.

*Proof.* The chaining mesh has $n_c = \lfloor 1 / r_c \rfloor$ cells per side, of side $1 / n_c \ge r_c$. If $n_c \ge 3$, two charges closer than $r_c$ in the minimum image lie in the same or in adjacent cells (modulo the period), and the 9 offsets visit each adjacent cell once, because $n_c \ge 3$ makes them distinct. If $n_c \le 2$, all pairs of cells are visited once. Since $r_c < \frac12$, an image closer than $r_c$ is the minimum image, and it is unique. The test $r^2 < r_c^2$ then keeps exactly the pairs claimed. For the omitted part, every omitted image is at distance at least $r_c$, and the sum of $e^{-\alpha^2 r^2} / r$ over the images of a pair at distances $r \ge r_c$ is $e^{-\alpha^2 r_c^2} / r_c$ times a factor bounded by a sum of Gaussian tails over the lattice, which tends to 1 as $\alpha r_c$ grows. $\square$

**Lemma 3 (total momentum).** For any influence function with $G(-k) = G(k)$ real, if the same weights $W$ are used for the assignment (line L1) and for the interpolation (line L5), and the derivative is set to 0 at the Nyquist index, then the mesh forces satisfy $\sum_i F_i^{\text{mesh}} = 0$. In particular, a single charge feels no mesh force from itself.

*Proof.* Let $Q_g = \sum_i q_i W(x_i - x_g)$ be the mesh charge, $\hat\rho(k) = \sum_g Q_g e^{-i k \cdot x_g}$, and $E_g = \sum_k (-i \tilde k) G(k) \hat\rho(k) e^{i k \cdot x_g}$, where $\tilde k$ is $k$ with the Nyquist components set to 0. Then

$$\sum_i F_i^{\text{mesh}} = \sum_i q_i \sum_g W(x_i - x_g) E_g = \sum_g Q_g E_g = \sum_k (-i \tilde k) G(k) \hat\rho(k) \overline{\hat\rho(k)},$$

because $Q_g$ is real, so $\sum_g Q_g e^{i k \cdot x_g} = \overline{\hat\rho(k)}$. The map $k \mapsto -k$ on the FFT indices fixes exactly the indices whose components are 0 or Nyquist, where $\tilde k$ has the corresponding component 0, and it pairs the other indices. Along each pair, $G$ and $|\hat\rho|^2$ are equal and $\tilde k$ changes sign, so the terms cancel, and every fixed index contributes a zero vector component. $\square$

The short-range forces satisfy Newton's third law pair by pair, so the total P3M force is zero, as the test checks to rounding.

**What is not proved here.** The mesh force is an approximation of $F_i^{\text{long}}$ with an error from the charge assignment and from aliasing. Hockney and Eastwood derive the optimal influence function

$$G(k) = \frac{\sum_m \hat U^2(k_m) \, (k \cdot k_m) \, \hat\phi(k_m)}{|k|^2 \big(\sum_m \hat U^2(k_m)\big)^2}, \qquad k_m = k + \frac{2\pi m}{h},$$

with $\hat\phi(k) = \frac{2\pi}{k^2} e^{-k^2/(4\alpha^2)}$ and the assignment function $\hat U(k) = \prod_c \mathrm{sinc}(k_c h / 2)^P$ ($P = 2$ for CIC, $P = 3$ for TSC), as the minimizer of the mean square force error, averaged over the positions of the charges, for this assignment and ik differentiation. We do not prove this, nor a rate of convergence of the mesh force as $h \to 0$; the code sums the aliases with $|m_c| \le 2$, and the errors against the Ewald sum are measured on the page.
