---
title: BFECC is second order and stable under constant velocity, and the limiter gives a maximum principle
proves: [correctness]
status: full
---

We use the line numbers of the page. $A$ is one semi-Lagrangian step with time step $\Delta t$ (the helper's RK2 backtrace and bilinear sample), and $A^R$ is the same step with $-\Delta t$, which traces forward. The BFECC step is

$$\hat q = A q, \qquad \check q = A^R \hat q, \qquad \bar q = q + \tfrac12 (q - \check q), \qquad q^{\text{new}} = A \bar q.$$

All statements are in exact arithmetic.

**Lemma 1 (constants).** If $q$ is constant, the BFECC step returns the same constant, with or without the limiter.

*Proof.* Each value of $A q$ is a convex combination of values of $q$, so $A$ and $A^R$ keep a constant $\kappa$. Then $\hat q = \check q = \kappa$, $\bar q = \kappa + \frac12(\kappa - \kappa) = \kappa$ and $A \bar q = \kappa$. The stencil range at every point is $[\kappa, \kappa]$, so the limiter changes nothing. $\square$

**Setting for the next results.** Take a periodic grid of spacing $\Delta x$ in 1D and a constant velocity $u > 0$. Let $c = u \Delta t / \Delta x = m + \varphi$ with an integer $m \ge 0$ and $\varphi \in [0, 1)$. The RK2 backtrace is exact for a constant velocity, so the foot of sample $a$ is at $a - c$ in cell units, between samples $a - m - 1$ and $a - m$. So

$$(A q)_a = (1 - \varphi)\, q_{a - m} + \varphi\, q_{a - m - 1}, \qquad (A^R q)_a = (1 - \varphi)\, q_{a + m} + \varphi\, q_{a + m + 1}.$$

A Fourier mode $q_a = e^{\mathrm i \theta a}$, $\theta \in [-\pi, \pi]$, is multiplied by $A(\theta) = e^{-\mathrm i m \theta} \left(1 - \varphi + \varphi e^{-\mathrm i \theta}\right)$ under $A$, and by $\overline{A(\theta)}$ under $A^R$. The test file checks on a grid of 40 cells that the interior values of one BFECC step of $\cos(\theta a)$ equal the real part of the symbol below to $10^{-13}$, for $c \in \{0.3, 1.5, 2.7\}$ and three values of $\theta$. On a non-periodic grid, these results hold at the samples whose three backtraces stay inside the grid.

**Lemma 2 (the symbol).** One BFECC step multiplies the mode by

$$G(\theta) = A \left(1 + \tfrac12 (1 - |A|^2)\right) = A\, \frac{3 - |A|^2}{2}, \qquad |A|^2 = 1 - 2 \varphi (1 - \varphi)(1 - \cos \theta).$$

*Proof.* $\hat q = A q$ and $\check q = \bar A A q = |A|^2 q$ for the mode. Then $\bar q = (1 + \frac12 (1 - |A|^2)) q$, and the last step multiplies by $A$. For the modulus, $|1 - \varphi + \varphi e^{-\mathrm i \theta}|^2 = (1 - \varphi)^2 + \varphi^2 + 2 \varphi (1 - \varphi) \cos \theta$, which is the formula. $\square$

**Theorem 1 (stability for any $\Delta t$, without the limiter).** For every $c \ge 0$ and every $\theta$, $|A| \le |G| \le 1$. So on the periodic grid the BFECC step does not increase the $\ell^2$ norm, at any CFL number.

*Proof.* Let $s = |A| \in [0, 1]$. Then $|G| = f(s)$ with $f(s) = s (3 - s^2)/2$. $f'(s) = \frac32 (1 - s^2) \ge 0$, so $f$ increases on $[0, 1]$ from $f(0) = 0$ to $f(1) = 1$, so $f(s) \le 1$. Also $f(s) - s = \frac12 s (1 - s^2) \ge 0$. By Parseval, a step that multiplies each mode by a factor of modulus at most 1 does not increase the $\ell^2$ norm. $\square$

So BFECC damps every mode less than plain semi-Lagrangian advection, and never amplifies one. It is not stable in the maximum norm: the test file moves a square of height 1 for five steps and gets values from $-0.124$ to $1.240$.

**Theorem 2 (second order).** For a fixed $\varphi$,

$$G(\theta) = e^{-\mathrm i c \theta} \exp\left(\mathrm i\, \frac{\varphi (1 - \varphi)(1 - 2\varphi)}{6}\, \theta^3 + O(\theta^4)\right),$$

while plain semi-Lagrangian advection has $A(\theta) = e^{-\mathrm i c \theta} \exp\left(-\frac{\varphi(1 - \varphi)}{2} \theta^2 + O(\theta^3)\right)$. Let $q(x) = \sum_k \hat q_k e^{\mathrm i k x}$ be a periodic trigonometric polynomial (a finite sum), and let $\Delta x$ be small enough that $|k \Delta x| \le \pi$ for each of its modes. At a fixed CFL number $c$, the error of BFECC after the time $T$ is $O(\Delta x^2)$, and the error of plain semi-Lagrangian advection is $O(\Delta x)$ when $\varphi \ne 0$.

*Proof.* Write $1 - \varphi + \varphi e^{-\mathrm i \theta} = 1 + z$ with $z = \varphi (e^{-\mathrm i \theta} - 1) = \varphi(-\mathrm i \theta - \frac12 \theta^2 + \frac{\mathrm i}{6} \theta^3 + O(\theta^4))$. Then $z^2 = \varphi^2 (-\theta^2 + \mathrm i \theta^3) + O(\theta^4)$ and $z^3 = \mathrm i \varphi^3 \theta^3 + O(\theta^4)$, so

$$\log(1 + z) = z - \tfrac12 z^2 + \tfrac13 z^3 + O(\theta^4) = -\mathrm i \varphi \theta - \tfrac12 \varphi (1 - \varphi) \theta^2 + \tfrac{\mathrm i}{6} \varphi (1 - \varphi)(1 - 2 \varphi) \theta^3 + O(\theta^4).$$

With $e^{-\mathrm i m \theta} e^{-\mathrm i \varphi \theta} = e^{-\mathrm i c \theta}$ this gives the form of $A$. By Lemma 2, $\frac{3 - |A|^2}{2} = 1 + \varphi (1 - \varphi)(1 - \cos \theta) = \exp\left(\frac12 \varphi (1 - \varphi) \theta^2 + O(\theta^4)\right)$. The product cancels the $\theta^2$ term and gives the form of $G$.

The function $h(\theta) = (G(\theta) e^{\mathrm i c \theta} - 1) / \theta^3$ is continuous on $[-\pi, \pi]$ (the numerator is smooth and vanishes to third order at 0), so $|G(\theta) - e^{-\mathrm i c \theta}| \le C |\theta|^3$ for a constant $C$ that depends on $\varphi$. On the grid, the mode $e^{\mathrm i k x}$ is $e^{\mathrm i \theta a}$ with $\theta = k \Delta x$. Since $|G| \le 1$ and $|e^{-\mathrm i c \theta}| = 1$, $|G^N - e^{-\mathrm i N c \theta}| \le N |G - e^{-\mathrm i c \theta}|$ by the telescoping sum $G^N - E^N = \sum_{j} G^{j} (G - E) E^{N - 1 - j}$. After $N = T u / (c \Delta x)$ steps, the error of each sample is at most

$$\sum_k |\hat q_k| \, N C |k \Delta x|^3 = \frac{T u C}{c} \Delta x^2 \sum_k |k|^3 |\hat q_k|,$$

which is $O(\Delta x^2)$. A smooth periodic function is close to such a polynomial, and its coefficients decay fast enough for the same bound. For plain semi-Lagrangian advection, the $\theta^2$ term does not cancel, the same argument gives $O(\Delta x)$, and the [stable fluids](/stable-fluids/) proof gives a direct bound. $\square$

The error constant has the factor $1 - 2\varphi$, so for $\varphi = \frac12$ the $\theta^3$ term vanishes and the error is smaller still. For $\varphi = 0$ both methods are exact. In 2D with a constant velocity, the bilinear sample is the product of two 1D samples, so $A = A_x A_y$ and $A^R = \overline{A}$. Lemma 2 and Theorem 1 hold with the same proof, since they use only $|A| \le 1$ and $A^R = \bar A$. In Theorem 2, $1 - |A|^2 = \varphi_x(1 - \varphi_x)\theta_x^2 + \varphi_y (1 - \varphi_y) \theta_y^2 + O(|\theta|^4)$ cancels the real second order part of $\log A$ in the same way, so the step is second order in 2D too. The test file moves a smooth bump of radius 0.3 with the velocity $(1, 0.5)$ m/s for 0.25 s at $c_x = 4/3$. Between 16 and 32 cells, the observed order is 2.41 for BFECC and 0.89 for plain semi-Lagrangian advection, and the errors at 32 cells are $0.00684$ and $0.1062$.

**Theorem 3 (the limiter, line L5).** Let $[\ell_a, h_a]$ be the range of the four values of $q$ that the plain step $A$ mixes at sample $a$. With the "clamp" or the "revert" limiter, every new value lies in $[\ell_a, h_a]$. So $\min q \le q^{\text{new}} \le \max q$, for any velocity and any $\Delta t$.

*Proof.* With "clamp", a value outside $[\ell_a, h_a]$ is replaced by the nearest end of the interval. With "revert", it is replaced by $\hat q_a = (A q)_a$, which is a convex combination of those four values (Lemma 1 of the stable fluids proof), so it lies in $[\ell_a, h_a]$. A value inside the interval stays. $\square$

The limiter is not linear, so Theorems 1 and 2 do not apply where it acts. It acts at discontinuities and also at smooth maxima, where the second order value overshoots the stencil. The test file measures the order on the smooth bump as 2.15 with "clamp" and 1.72 with "revert". At a discontinuity the order drops below the smooth order for all of these methods.
