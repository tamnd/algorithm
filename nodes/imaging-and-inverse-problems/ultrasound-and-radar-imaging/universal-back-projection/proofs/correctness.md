---
title: On a sphere of detectors in 3D, universal back-projection is a divergence of a surface integral whose frequency kernel reduces, by the Wronskian of spherical Bessel functions, to the Fourier inversion formula
proves: [correctness]
status: full
---

This file proves that the continuous formula of lines L1 to L8 is exact for a sphere of detectors in three dimensions, and bounds the error of the time sampling. Exactness for the infinite cylinder and the infinite plane is stated by Xu and Wang (2005) and is not proved here. The two-dimensional analogue is not exact.

**Setting.** $B = \{x \in \mathbb{R}^3 : |x| < R\}$, $S = \partial B$, and $n(z) = z / R$ is the outward normal at $z \in S$. The initial pressure $p_0$ is smooth with compact support $K \subset B$. The pressure $p(x, t)$ solves $p_{tt} = c^2 \Delta p$ with $p(\cdot, 0) = p_0$ and $p_t(\cdot, 0) = 0$. By Poisson's (Kirchhoff's) formula,

$$p(x, t) = \partial_t \big(t\, M(x, ct)\big), \qquad M(x, \rho) = \frac{1}{4\pi} \int_{S^2} p_0(x + \rho \omega)\, d\omega.$$

The algorithm computes, for $x \in B$,

$$U(x) = \frac{1}{4\pi} \int_S b\big(z, |x - z|/c\big)\, d\Omega_x(z), \qquad b = 2p - 2t\, \partial_t p, \qquad d\Omega_x(z) = \frac{n_{\text{in}}(z) \cdot (x - z)}{|x - z|^3}\, dS(z),$$

with the inward normal $n_{\text{in}} = -n$ (line L5 is $d\Omega$, line L6 the product with $b$, line L8 the division by $\Omega_0 = 4\pi$). We use the Fourier transform $\hat f(\xi) = \int f(y) e^{-2\pi i y \cdot \xi}\, dy$.

**Lemma 0 (the speed can be taken as 1).** Put $\tilde p(z, \rho) = \partial_\rho(\rho M(z, \rho))$. Then $p(z, t) = \tilde p(z, ct)$, and $b(z, |x - z|/c) = \tilde b(z, |x - z|)$ with $\tilde b(z, \rho) = 2\tilde p - 2\rho\, \partial_\rho \tilde p$.

*Proof.* $\partial_t (t M(z, ct)) = M + ct\, M_\rho = \partial_\rho(\rho M)$ at $\rho = ct$, and $t\, \partial_t = \rho\, \partial_\rho$ under $\rho = ct$. $\square$

From now on $c = 1$ and we drop the tildes.

**Lemma 1 (support of the data).** For $z \in S$, $t \mapsto p(z, t)$ is smooth and vanishes outside an interval $[\delta, 2R]$ with $\delta = \operatorname{dist}(S, K) > 0$. The same holds for $F(z, t) = t\, M(z, t)$, uniformly in $z \in S$ together with all derivatives.

*Proof.* $F(z, t) = \frac{t}{4\pi} \int_{S^2} p_0(z + t\omega)\, d\omega$ is smooth in $(z, t)$, and the sphere of radius $t$ about $z$ meets $K$ only if $\delta \le t \le 2R$. $p = \partial_t F$. Uniformity follows from the compactness of $S \times [0, 2R]$. $\square$

**Lemma 2 (divergence form).** Let $q(z, \rho) = p(z, \rho)/\rho$. Then

$$U(x) = \frac{1}{2\pi} \int_S n(z) \cdot \nabla_x \big[ q(z, |x - z|) \big]\, dS(z).$$

*Proof.* $b = 2p - 2\rho\, p_\rho = -2\rho^2\, \partial_\rho (p/\rho)$. With $d = |x - z|$ and $\nabla_x d = (x - z)/d$,

$$b(z, d)\, \frac{n_{\text{in}} \cdot (x - z)}{d^3} = -2\, \partial_\rho q(z, d)\; n_{\text{in}} \cdot \frac{x - z}{d} = -2\, n_{\text{in}} \cdot \nabla_x [q(z, |x - z|)] = 2\, n \cdot \nabla_x [q(z, |x - z|)].$$

Integrate over $S$ and divide by $4\pi$. $\square$

**Lemma 3 (frequency form of the data).** For $k > 0$ and $z \in S$ put $P_c(z, k) = \int_0^\infty p(z, t) \cos kt\, dt$ and $P_s(z, k) = \int_0^\infty p(z, t) \sin kt\, dt$. Then, with $a_y(z) = \cos(k|z - y|)/|z - y|$ and $s_y(z) = \sin(k|z - y|)/|z - y|$,

$$P_c(z, k) = \frac{k}{4\pi} \int_B p_0(y)\, s_y(z)\, dy, \qquad P_s(z, k) = -\frac{k}{4\pi} \int_B p_0(y)\, a_y(z)\, dy,$$

and for $d > 0$

$$q(z, d) = \frac{1}{\pi} \int_0^\infty \Big[ \frac{\sin kd}{d} P_s(z, k) + \frac{\cos kd}{d} P_c(z, k) \Big]\, dk.$$

The functions $P_c$ and $P_s$ decay faster than any power of $k$, uniformly in $z$.

*Proof.* $p = \partial_t F$ and $F(z, \cdot)$ has compact support in $(0, \infty)$ by Lemma 1, so integration by parts gives $P_c = k \int_0^\infty F \sin kt\, dt$ and $P_s = -k \int_0^\infty F \cos kt\, dt$. In polar coordinates about $z$, $dy = t^2\, dt\, d\omega$, so $\int_0^\infty F(z, t) \sin kt\, dt = \frac{1}{4\pi} \int p_0(y)\, \frac{\sin(k|y - z|)}{|y - z|}\, dy$, and the same with the cosine. The function $a_y(z)$ is bounded there because $|y - z| \ge \delta$ on $K$. The Fourier sine and cosine inversion formulas for the function $p(z, \cdot)$, which is smooth with compact support in $(0, \infty)$, give $p(z, d) = \frac{2}{\pi} \int_0^\infty \sin(kd) P_s\, dk = \frac{2}{\pi} \int_0^\infty \cos(kd) P_c\, dk$ for $d > 0$. Take the mean of the two and divide by $d$. Repeated integration by parts gives the decay. $\square$

**Lemma 4 (the sphere identity).** For $x, y \in B$ and $k > 0$,

$$\int_S \big( s_y\, \partial_\nu a_x - a_y\, \partial_\nu s_x \big)\, dS = -4\pi\, \frac{\sin(k|x - y|)}{|x - y|},$$

where $\partial_\nu$ is the derivative in $z$ along $n(z)$.

*Proof.* We use three classical facts about the spherical Bessel functions $j_l$, $y_l$ and the Legendre polynomials $P_l$. (i) For $|x| < |z|$, $\frac{e^{ik|z - x|}}{|z - x|} = ik \sum_l (2l + 1) j_l(k|x|) h_l(k|z|) P_l(\hat x \cdot \hat z)$ with $h_l = j_l + i y_l$, and $\frac{\sin(k|z - x|)}{k|z - x|} = \sum_l (2l + 1) j_l(k|x|) j_l(k|z|) P_l(\hat x \cdot \hat z)$, with absolute and uniform convergence, also after one derivative in $|z|$, on compact subsets of $|x| < |z|$. (ii) $\int_S P_l(\hat x \cdot \hat z) P_m(\hat y \cdot \hat z)\, dS(z) = \delta_{lm} \frac{4\pi R^2}{2l + 1} P_l(\hat x \cdot \hat y)$. (iii) $j_l(u) y_l'(u) - j_l'(u) y_l(u) = 1/u^2$.

By (i), on $S$: $a_x = -k \sum (2l + 1) j_l(k|x|) y_l(kR) P_l(\hat x \cdot \hat z)$ and $s_x = k \sum (2l + 1) j_l(k|x|) j_l(kR) P_l(\hat x \cdot \hat z)$. Since $\partial_\nu = \partial / \partial |z|$, $\partial_\nu a_x = -k^2 \sum (2l + 1) j_l(k|x|) y_l'(kR) P_l$ and $\partial_\nu s_x = k^2 \sum (2l + 1) j_l(k|x|) j_l'(kR) P_l$. Multiply the series, integrate term by term with (ii), and write $\Pi_l = j_l(k|x|) j_l(k|y|) P_l(\hat x \cdot \hat y)$:

$$\int_S s_y\, \partial_\nu a_x\, dS = -4\pi R^2 k^3 \sum (2l + 1)\, j_l(kR) y_l'(kR)\, \Pi_l, \qquad \int_S a_y\, \partial_\nu s_x\, dS = -4\pi R^2 k^3 \sum (2l + 1)\, y_l(kR) j_l'(kR)\, \Pi_l.$$

Their difference is $-4\pi R^2 k^3 \sum (2l + 1) \big[j_l y_l' - j_l' y_l\big](kR)\, \Pi_l = -4\pi k \sum (2l + 1) \Pi_l$ by (iii), and by the second series of (i) with $z$ replaced by $y$ this is $-4\pi k \cdot \frac{\sin(k|x - y|)}{k|x - y|}$. $\square$

The identity uses the sphere twice: the normal derivative is the radial derivative, and the Wronskian (iii) is the same number $1/(kR)^2$ at every point of $S$. On a general surface no such cancellation takes place.

**Theorem 1 (exactness on the sphere).** For every $x \in B$, $U(x) = p_0(x)$.

*Proof.* Fix $x \in B$. In Lemma 2, insert the formula for $q$ from Lemma 3 and use $\nabla_x f(|x - z|) = -\nabla_z f(|x - z|)$, so that $n \cdot \nabla_x$ becomes $-\partial_\nu$:

$$U(x) = -\frac{1}{2\pi^2} \int_0^\infty \int_S \big[ \partial_\nu s_x\, P_s + \partial_\nu a_x\, P_c \big]\, dS\, dk.$$

The derivative under the $k$ integral is allowed, and the order of the integrals may be changed, because $|\partial_\nu s_x|$ and $|\partial_\nu a_x|$ are $O(k + 1)$ uniformly for $z \in S$ and $x$ near a fixed point of $B$, while $P_c$ and $P_s$ decay fast (Lemma 3). Insert $P_c$ and $P_s$ from Lemma 3 and use Fubini again ($p_0$ is bounded with compact support):

$$U(x) = -\frac{1}{2\pi^2} \int_0^\infty \frac{k}{4\pi} \int_B p_0(y) \int_S \big( s_y\, \partial_\nu a_x - a_y\, \partial_\nu s_x \big)\, dS\, dy\, dk = \frac{1}{2\pi^2} \int_0^\infty k \int_B p_0(y) \frac{\sin(k|x - y|)}{|x - y|}\, dy\, dk$$

by Lemma 4. Finally, by Fourier inversion and polar coordinates $\xi = \sigma \omega$,

$$p_0(x) = \int \hat p_0(\xi) e^{2\pi i x \cdot \xi}\, d\xi = \int_0^\infty \sigma^2 \int_B p_0(y) \int_{S^2} e^{2\pi i \sigma \omega \cdot (x - y)}\, d\omega\, dy\, d\sigma = \int_0^\infty \sigma^2 \int_B p_0(y)\, \frac{4\pi \sin(2\pi\sigma|x - y|)}{2\pi\sigma|x - y|}\, dy\, d\sigma,$$

and with $k = 2\pi\sigma$ the last expression is $\frac{1}{2\pi^2} \int_0^\infty k \int_B p_0(y) \frac{\sin(k|x - y|)}{|x - y|}\, dy\, dk$. $\square$

**Corollary (the solid angle).** For $x \in B$, $\int_S d\Omega_x = 4\pi$. So dividing by the sum of the solid angle elements (the default of line L8) or by $4\pi$ gives the same continuous formula.

*Proof.* $\partial_\nu \frac{1}{|z - x|} = \frac{n \cdot (x - z)}{|x - z|^3}$, so $d\Omega_x = -\partial_\nu \frac{1}{|z - x|}\, dS$. Gauss's law gives $\int_S \partial_\nu \frac{1}{|z - x|}\, dS = -4\pi$ for $x$ inside $S$. $\square$

**Theorem 2 (the sampled algorithm).** Let the data be sampled at $t_k = k\, \Delta t$ on a record that covers $[0, 2R/c]$ with at least one more sample, let $b_k$ be computed by line L1, and let $b$ be evaluated by linear interpolation. If $p(z, \cdot)$ has three bounded derivatives, then for every $t$ in the record, the value used for $b(z, t)$ has the error at most $\Delta t^2 \big( \tfrac{1}{3}\, t_{\max} \max|\partial_t^3 p| + \tfrac{1}{8} \max|\partial_t^2 b| \big)$ plus the rounding. With exact $b$, the only other error is the quadrature over $S$.

*Proof.* By Lemma 1, $p(z, \cdot)$ is zero near both ends of the record, so the one sided differences at the ends are exact. Inside, by Taylor's theorem, $\frac{p(t + \Delta t) - p(t - \Delta t)}{2\Delta t} - p'(t)$ is at most $\frac{\Delta t^2}{6} \max|p'''|$, so $|b_k - b(t_k)| \le 2 t_k \frac{\Delta t^2}{6} \max|p'''| \le \frac{1}{3} t_{\max} \Delta t^2 \max|p'''|$. Linear interpolation of a function with a bounded second derivative has the error at most $\frac{\Delta t^2}{8} \max|b''|$, and the interpolated value of the perturbed samples differs from the interpolated value of the exact ones by at most the largest perturbation. Line L6 is a weighted sum with $\sum |d\Omega| / \Omega_0$ bounded, so the error of $U$ is $O(\Delta t^2)$. $\square$

In the test the error at the centre of a Gaussian ball falls from $4.4 \times 10^{-3}$ to $1.1 \times 10^{-3}$ when $\Delta t$ is halved from 0.04 to 0.02 µs, the factor 4 that Theorem 2 predicts (measurement). The quadrature over $S$ (Gauss-Legendre in $\cos\theta$ times the uniform rule in $\varphi$, 800 detectors) reproduces the ball to $10^{-15}$ when $b$ is exact (measurement).

**Theorem 3 (cost).** With $D$ detectors, $T$ samples per detector and $V$ image points, the algorithm takes $O(D T + V D)$ time and $O(D T)$ space in the real-RAM model.

*Proof.* Line L1 costs $O(1)$ per sample. For each of the $V$ points, lines L4 to L7 cost $O(1)$ per detector: one distance, one solid angle element and one interpolation. The array $b$ has $D T$ entries. $\square$
