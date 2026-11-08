---
title: The Lax-Wendroff method is conservative, L2 stable under the CFL condition, and converges with order 2 for linear advection
proves: [correctness, termination, convergence]
status: full
---

**Setting.** Cells $j = 0, \dots, m - 1$ with $x_j = j\Delta x$, periodic indices unless stated otherwise, domain length $\ell = m\Delta x$. One step with $\lambda = \Delta t/\Delta x$ is

$$V_{j+1/2} = \frac{U_j + U_{j+1}}{2} - \frac{\lambda}{2}\bigl(f(U_{j+1}) - f(U_j)\bigr), \qquad U_j^{\text{new}} = U_j - \lambda\bigl(f(V_{j+1/2}) - f(V_{j-1/2})\bigr).$$

For $f(u) = au$ we write $\nu = a\lambda$. The discrete $L^2$ norm is $\|v\|_2 = (\Delta x \sum_j v_j^2)^{1/2}$.

**Lemma 1 (the loop).** After iteration $n$ of lines L3 to L11, $t = t_{n+1}$ and $U$ holds the result of one step applied to $U^n$ with $\lambda_n = (t_{n+1} - t_n)/\Delta x$, where $t_k = k\Delta t$ for $k < N$ and $t_N = T$.

*Proof.* Induction on $n$. Lines L6 to L9 compute the face values from the old $U$ only, and line L10 builds the new list from them, so no value of $U^{n+1}$ is used before the step is complete. The ghost values of line L7 are $U_m = U_0$ in the periodic case and $U_m = U_{m-1}$ in the transmissive case; in the transmissive case the flux through the left boundary face is $f(U_0)$. $\square$

**Termination.** The loop runs $N = \lceil T/\Delta t \rceil$ times (up to the rounding slack), each iteration doing $2m$ flux evaluations and $O(m)$ arithmetic; $T = 0$ gives $N = 0$ and returns $U^0$.

**Lemma 2 (conservation).** With periodic boundary conditions, $\sum_j U_j^{n+1} = \sum_j U_j^n$.

*Proof.* $\sum_j \bigl(f(V_{j+1/2}) - f(V_{j-1/2})\bigr) = 0$ because the sum telescopes over all indices modulo $m$. $\square$

**Lemma 3 (the linear one-step form).** For $f(u) = au$,

$$U_j^{n+1} = \frac{\nu(1 + \nu)}{2} U_{j-1}^n + (1 - \nu^2) U_j^n - \frac{\nu(1 - \nu)}{2} U_{j+1}^n.$$

*Proof.* $aV_{j+1/2} = \frac{a}{2}(U_j + U_{j+1}) - \frac{a\nu}{2}(U_{j+1} - U_j)$. Then

$$\lambda a (V_{j+1/2} - V_{j-1/2}) = \frac{\nu}{2}(U_{j+1} - U_{j-1}) - \frac{\nu^2}{2}(U_{j+1} - 2U_j + U_{j-1}),$$

and $U_j$ minus this is the stated combination. $\square$

**Lemma 4 (local error for linear advection).** Let $f(u) = au$, $|\nu| \le 1$, $u_0 \in C^3$ periodic with $M_3 = \max|u_0'''|$ and $u(x, t) = u_0(x - at)$. With $w = u(\cdot, t_n)$, the local error

$$\delta_j^n = u(x_j, t_{n+1}) - \Bigl(\frac{\nu(1 + \nu)}{2} w(x_{j-1}) + (1 - \nu^2) w(x_j) - \frac{\nu(1 - \nu)}{2} w(x_{j+1})\Bigr)$$

satisfies $|\delta_j^n| \le \frac{M_3}{6}|\nu|(1 - \nu^2)\Delta x^3$.

*Proof.* $u(x_j, t_{n+1}) = w(\xi)$ with $\xi = x_j - \nu\Delta x \in [x_{j-1}, x_{j+1}]$. Let $p$ be the quadratic that interpolates $w$ at $x_{j-1}, x_j, x_{j+1}$. Its Lagrange basis polynomials at $\xi = x_j + s\Delta x$, $s = -\nu$, are $\frac{s(s - 1)}{2}$, $1 - s^2$ and $\frac{s(s + 1)}{2}$, which equal $\frac{\nu(1 + \nu)}{2}$, $1 - \nu^2$ and $-\frac{\nu(1 - \nu)}{2}$. So $\delta_j^n = w(\xi) - p(\xi)$, and the interpolation error formula gives

$$w(\xi) - p(\xi) = \frac{w'''(\eta)}{6}(\xi - x_{j-1})(\xi - x_j)(\xi - x_{j+1})$$

for some $\eta$. The product has absolute value $(1 - \nu)\Delta x \cdot |\nu|\Delta x \cdot (1 + \nu)\Delta x$, and $|w'''| \le M_3$ since $w$ is a shift of $u_0$. $\square$

**Lemma 5 ($L^2$ stability).** For $f(u) = au$ and $|\nu| \le 1$, periodic, $\|U^{n+1}\|_2 \le \|U^n\|_2$. For $|\nu| > 1$ there are data for which $\|U^n\|_2$ grows geometrically.

*Proof.* Write $U^n$ in the discrete Fourier basis, $U_j = \sum_k \hat U_k e^{ij\theta_k}$ with $\theta_k = 2\pi k/m$. By Lemma 3 each mode is multiplied by

$$g(\theta) = \frac{\nu(1 + \nu)}{2}e^{-i\theta} + (1 - \nu^2) - \frac{\nu(1 - \nu)}{2}e^{i\theta} = 1 - \nu^2(1 - \cos\theta) - i\nu\sin\theta.$$

With $c = 1 - \cos\theta \in [0, 2]$ and $\sin^2\theta = c(2 - c)$,

$$|g|^2 = (1 - \nu^2 c)^2 + \nu^2 c(2 - c) = 1 - \nu^2(1 - \nu^2)c^2.$$

So $|g| \le 1$ for all $\theta$ iff $\nu^2 \le 1$. By the discrete Parseval identity $\|U\|_2^2 = \ell \sum_k |\hat U_k|^2$, hence $\|U^{n+1}\|_2 \le \max_k|g(\theta_k)|\,\|U^n\|_2 \le \|U^n\|_2$. If $|\nu| > 1$ and $m$ is even, the mode $\theta = \pi$ has $|g| = |1 - 2\nu^2| = 2\nu^2 - 1 > 1$ and grows like $(2\nu^2 - 1)^n$. $\square$

**Theorem (convergence of order 2).** Under the assumptions of Lemma 4, with $U_j^0 = u_0(x_j)$ and steps with Courant numbers $\nu_n$, $0 < |\nu_n| \le 1$,

$$\|u(\cdot, t_N) - U^N\|_2 \le \frac{M_3}{6}\sqrt{\ell}\,\Delta x^3 \sum_{n=0}^{N-1}|\nu_n|(1 - \nu_n^2).$$

With equal steps, $N|\nu| = T|a|/\Delta x$, and the right side is $\frac{T|a|(1 - \nu^2)}{6} M_3 \sqrt{\ell}\, \Delta x^2$.

*Proof.* Let $e^n_j = u(x_j, t_n) - U_j^n$, $e^0 = 0$, and let $S_n$ be the linear one-step map of Lemma 3 with $\nu_n$. By the definition of $\delta$, $e^{n+1} = S_n e^n + \delta^n$. Lemma 5 gives $\|S_n e^n\|_2 \le \|e^n\|_2$, and Lemma 4 gives $\|\delta^n\|_2 \le \sqrt{m\Delta x}\,\max_j|\delta_j^n| \le \sqrt{\ell}\,\frac{M_3}{6}|\nu_n|(1 - \nu_n^2)\Delta x^3$. Summing $\|e^{n+1}\|_2 \le \|e^n\|_2 + \|\delta^n\|_2$ over $n$ gives the claim. $\blacksquare$

The bound is proved and non-asymptotic. It vanishes at $|\nu| = 1$, where the scheme is the exact shift by one cell. It is a bound in $L^2$. In the max norm the scheme is not a contraction: for $0 < |\nu| < 1$ one weight is negative and the absolute values of the weights sum to $1 + |\nu|(1 - |\nu|) > 1$. A max-norm bound follows only with an extra factor from $\|v\|_\infty \le \|v\|_2/\sqrt{\Delta x}$, or from smoothness arguments not given here. The observed max-norm ratios of $4.00$ on the page are measurements.

**Nonlinear conservation laws (cited).** The scheme is in conservation form with numerical flux $\hat F(U_j, U_{j+1}) = f(V_{j+1/2})$, which is consistent: $\hat F(v, v) = f(v)$. By the Lax-Wendroff theorem (1960; LeVeque FV, Section 12.10), if the numerical solutions converge boundedly almost everywhere as $\Delta x, \Delta t \to 0$, the limit is a weak solution. The scheme is not monotone, so the convergence to the entropy solution is not guaranteed; this is cited, not proved here.
