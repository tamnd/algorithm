---
title: Correctness of filtered back-projection
proves: [correctness]
status: full
---

We use the conventions of the page. $\omega(\theta) = (\cos\theta, \sin\theta)$ and $\omega^\perp(\theta) = (-\sin\theta, \cos\theta)$. The Radon transform is $\mathcal{R}f(\theta, s) = \int_{\mathbb{R}} f(s\,\omega + t\,\omega^\perp)\,dt$ for $\theta \in [0, \pi)$ and $s \in \mathbb{R}$. The Fourier transform uses ordinary frequency, $\mathcal{F}f(\xi) = \int f(x) e^{-2\pi i x \cdot \xi}\,dx$. For a fixed angle we write $p_\theta(s) = \mathcal{R}f(\theta, s)$ and $P_\theta(\sigma) = \int p_\theta(s) e^{-2\pi i s \sigma}\,ds$.

The proof has four parts. Part 1 is the continuous inversion formula that the algorithm discretizes. Part 2 shows that the Ram-Lak kernel of line L2 samples the ramp filter cut off at the Nyquist frequency of the detector. Part 3 shows that, for band-limited projections, the discrete sum of line L6 gives the exact samples of the filtered projection. Part 4 shows that the FFT of lines L3 to L6 computes that sum exactly. The last section names the two approximations that remain, in lines L7 and L8.

**Lemma 1 (Fourier slice).** Let $f \in L^1(\mathbb{R}^2)$. Then for each $\theta$, $p_\theta \in L^1(\mathbb{R})$ and $P_\theta(\sigma) = \mathcal{F}f(\sigma\,\omega(\theta))$ for all $\sigma \in \mathbb{R}$.

*Proof.* The map $(s, t) \mapsto s\,\omega + t\,\omega^\perp$ is a rotation, so its Jacobian is 1, and $s = x \cdot \omega$ at the point $x = s\,\omega + t\,\omega^\perp$. By Fubini, $\int |p_\theta(s)|\,ds \le \int\int |f(s\,\omega + t\,\omega^\perp)|\,dt\,ds = \|f\|_1$, and
$$P_\theta(\sigma) = \int\int f(s\,\omega + t\,\omega^\perp)\, e^{-2\pi i s\sigma}\,dt\,ds = \int_{\mathbb{R}^2} f(x)\, e^{-2\pi i (x\cdot\omega)\sigma}\,dx = \mathcal{F}f(\sigma\,\omega). \qquad \square$$

**Theorem 1 (filtered back-projection formula).** Let $f \in L^1(\mathbb{R}^2)$ be continuous, with $\mathcal{F}f \in L^1(\mathbb{R}^2)$. Put $q_\theta(s) = \int_{\mathbb{R}} |\sigma|\, P_\theta(\sigma)\, e^{2\pi i s\sigma}\,d\sigma$. Then for every $x \in \mathbb{R}^2$
$$f(x) = \int_0^\pi q_\theta(x \cdot \omega(\theta))\,d\theta.$$

*Proof.* Because $\mathcal{F}f \in L^1$ and $f$ is continuous, the Fourier inversion formula holds at every point: $f(x) = \int_{\mathbb{R}^2} \mathcal{F}f(\xi) e^{2\pi i x\cdot\xi}\,d\xi$. Write $\xi = \sigma\,\omega(\theta)$ with $\theta \in [0, \pi)$ and $\sigma \in \mathbb{R}$. This map covers $\mathbb{R}^2$ once, except for the null set $\xi = 0$, and $d\xi = |\sigma|\,d\sigma\,d\theta$. So
$$f(x) = \int_0^\pi \int_{\mathbb{R}} \mathcal{F}f(\sigma\,\omega)\, |\sigma|\, e^{2\pi i \sigma (x\cdot\omega)}\,d\sigma\,d\theta.$$
The double integral converges absolutely, because its absolute value integrates to $\|\mathcal{F}f\|_1$. So by Fubini the inner integral exists for almost every $\theta$. By Lemma 1, $\mathcal{F}f(\sigma\,\omega) = P_\theta(\sigma)$, and the inner integral is $q_\theta(x\cdot\omega)$. $\square$

The filter $|\sigma|$ is the ramp. Its inverse transform $h$ is not a function, so $q_\theta = h * p_\theta$ holds only in the sense of distributions. The algorithm replaces $|\sigma|$ with a band-limited ramp.

**Lemma 2 (Ram-Lak kernel).** Let $\tau > 0$, $B = 1/(2\tau)$, and $h_B(s) = \int_{-B}^{B} |\nu|\, e^{2\pi i s\nu}\,d\nu$. Then $h_B(0) = 1/(4\tau^2)$, $h_B(m\tau) = 0$ for even $m \ne 0$, and $h_B(m\tau) = -1/(m^2\pi^2\tau^2)$ for odd $m$.

*Proof.* $|\nu|$ is even, so $h_B(s) = 2\int_0^B \nu \cos(2\pi s\nu)\,d\nu$. At $s = 0$ this is $B^2 = 1/(4\tau^2)$. For $s = m\tau$ with $m \ne 0$, put $c = 2\pi m\tau$. Integration by parts gives
$$\int_0^B \nu\cos(c\nu)\,d\nu = \frac{B \sin(cB)}{c} + \frac{\cos(cB) - 1}{c^2}.$$
Here $cB = \pi m$, so $\sin(cB) = 0$ and $\cos(cB) = (-1)^m$. Hence $h_B(m\tau) = 2((-1)^m - 1)/(4\pi^2 m^2\tau^2)$. This is 0 for even $m$ and $-1/(\pi^2 m^2\tau^2)$ for odd $m$. $\square$

Line L2 with the Ram-Lak choice stores exactly these values for $|m| \le d - 1$.

**Lemma 3 (exact discrete filtering).** Let $p \in L^1(\mathbb{R})$ be continuous, with $P(\nu) = 0$ for $|\nu| \ge B = 1/(2\tau)$, and with $\sum_k |p(k\tau)| < \infty$. Then for every integer $j$
$$(h_B * p)(j\tau) := \int_{-B}^{B} |\nu|\, P(\nu)\, e^{2\pi i j\tau\nu}\,d\nu = \tau \sum_{k \in \mathbb{Z}} h_B((j - k)\tau)\, p(k\tau).$$

*Proof.* The function $\nu \mapsto P(\nu)$ on $[-B, B]$ extends to a function of period $2B = 1/\tau$. Its Fourier coefficients are $\tau\int_{-B}^{B} P(\nu) e^{2\pi i k\tau\nu}\,d\nu = \tau\,p(k\tau)$, by the inversion formula for the band-limited $p$. The coefficients are absolutely summable, so the Fourier series converges uniformly to the continuous periodic extension: $P(\nu) = \tau\sum_k p(k\tau)\,e^{-2\pi i k\tau\nu}$ for $|\nu| \le B$. Put this into the left side. The sum converges uniformly and $|\nu|$ is bounded on $[-B, B]$, so the sum and the integral commute:
$$\int_{-B}^{B} |\nu|\, P(\nu)\, e^{2\pi i j\tau\nu}\,d\nu = \tau\sum_k p(k\tau) \int_{-B}^{B} |\nu|\, e^{2\pi i (j-k)\tau\nu}\,d\nu = \tau\sum_k p(k\tau)\, h_B((j-k)\tau). \qquad \square$$

If also $p(k\tau) = 0$ for $k < 0$ and $k \ge d$, the sum has only the terms $0 \le k \le d - 1$. Then $j - k$ lies in $\{-(d-1), \ldots, d-1\}$ for $0 \le j \le d - 1$, which is the range that line L2 stores. The sinogram index $j$ is the detector position $s_j = (j - (d-1)/2)\tau$. A shift of the origin by $(d-1)\tau/2$ changes neither side, because both sides are convolutions.

**Lemma 4 (zero padding).** Let $L \ge 2d - 1$. Let $u_k = p_k$ for $0 \le k \le d - 1$ and $u_k = 0$ for $d \le k \le L - 1$. Let $w_{m \bmod L} = h_m$ for $|m| \le d - 1$ and $w_r = 0$ at the other indices $r$. Let $y = \mathrm{IDFT}_L(\mathrm{DFT}_L(u) \cdot \mathrm{DFT}_L(w))$. Then $y_j = \sum_{k=0}^{d-1} h_{j-k}\, p_k$ for $0 \le j \le d - 1$.

*Proof.* First, $w$ is well defined. Two values $m \ne m'$ in $\{-(d-1), \ldots, d-1\}$ differ by at most $2d - 2 < L$, so $m \bmod L \ne m' \bmod L$. By the [convolution theorem](/convolution-theorem/) for the DFT, $y_j = \sum_{k=0}^{L-1} u_k\, w_{(j-k) \bmod L} = \sum_{k=0}^{d-1} p_k\, w_{(j-k) \bmod L}$. For $0 \le j, k \le d - 1$ we have $|j - k| \le d - 1$, so $w_{(j-k) \bmod L} = h_{j-k}$. $\square$

Lines L3 and L4 build $L$ and $\mathrm{DFT}_L(w)$. Line L6 builds $u$, applies the product and multiplies by $\tau$. The data and the kernel are real, so $y$ is real, and taking the real part removes only rounding errors. With Lemmas 2, 3 and 4, line L6 gives $q_k[j] = (h_B * p_{\theta_k})(s_j)$ exactly, for each projection that is band-limited to $|\nu| < 1/(2\tau)$ and zero outside the detector. If $L < 2d - 1$, two kernel samples fall on one index, and the result is a circular convolution with wrong values near both ends.

**Back projection (lines L7 to L9).** Line L8 makes two approximations of Theorem 1, with $q_\theta$ replaced by $h_B * p_\theta$.

1. *The angle integral.* By the symmetry $\mathcal{R}f(\theta + \pi, -s) = \mathcal{R}f(\theta, s)$ and because $h_B$ is even, $q_{\theta+\pi}(-s) = q_\theta(s)$. So $\theta \mapsto q_\theta(x\cdot\omega(\theta))$ has period $\pi$. The sum $(\pi/a)\sum_{k=0}^{a-1}$ at $\theta_k = k\pi/a$ is the trapezoidal rule for one full period. For a periodic integrand that is $r$ times continuously differentiable its error is $O(a^{-r})$.
2. *The detector position.* $x\cdot\omega(\theta_k)$ is not a bin center in general. The fractional index $u = x\cdot\omega/\tau + (d-1)/2$ satisfies $s_u = x\cdot\omega$, and LININTERP returns the linear interpolant of the samples $q_k[\lfloor u\rfloor]$ and $q_k[\lfloor u\rfloor + 1]$. Linear interpolation is exact for linear functions, and its error is at most $\tau^2 \max|q_\theta''| / 8$. Outside the detector it returns 0, which is the value of $q_\theta$ there only in the limit of a wide detector.

**Summary.** For a continuous $f$ with $\mathcal{F}f \in L^1$, whose projections are band-limited to $|\nu| < 1/(2\tau)$ and vanish outside the detector, lines L1 to L6 compute the exact samples of the filtered projections. Line L8 then evaluates Theorem 1 with the trapezoidal rule in $\theta$ and linear interpolation in $s$. So the only errors on such data are the quadrature error in $\theta$ and the interpolation error in $s$, and both go to 0 as $a$ grows and $\tau$ shrinks. A function with compact support is never exactly band-limited, so on real data the band limit is an approximation and the error has an aliasing part as well.

**The Shepp-Logan kernel.** Line L2 may use $h(m\tau) = -2/(\pi^2\tau^2(4m^2 - 1))$ instead. These are the samples of the inverse transform of $|\nu|\,\mathrm{sinc}(\nu\tau)$ on $[-B, B]$, with $\mathrm{sinc}(z) = \sin(\pi z)/(\pi z)$. To see this, write the inverse transform at $s = m\tau$ as $2\int_0^B \nu\,\mathrm{sinc}(\nu\tau)\cos(2\pi m\tau\nu)\,d\nu$ and put $u = \pi\tau\nu$:
$$\frac{2}{\pi^2\tau^2}\int_0^{\pi/2} \sin u \cos(2mu)\,du = \frac{1}{\pi^2\tau^2}\left(\frac{1}{1+2m} + \frac{1}{1-2m}\right) = \frac{-2}{\pi^2\tau^2(4m^2 - 1)},$$
because $\cos((1 \pm 2m)\pi/2) = 0$ for each integer $m$. So Lemmas 3 and 4 hold with this window in place of the plain ramp, and the result is $f$ blurred by the 2D filter with this window.
