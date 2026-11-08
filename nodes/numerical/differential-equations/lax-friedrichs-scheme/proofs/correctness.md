---
title: The Lax-Friedrichs scheme is conservative, monotone under the CFL condition, and converges with order 1 for linear advection
proves: [correctness, termination, convergence]
status: full
---

**Setting.** Cells $j = 0, \dots, m - 1$ with $x_j = j\Delta x$, periodic indices unless stated otherwise. One step with $\lambda = \Delta t/\Delta x$ is

$$U_j^{n+1} = H(U_{j-1}^n, U_{j+1}^n) := \frac{U_{j-1}^n + U_{j+1}^n}{2} - \frac{\lambda}{2}\bigl(f(U_{j+1}^n) - f(U_{j-1}^n)\bigr).$$

For $f(u) = au$ we write $\nu = a\lambda$.

**Lemma 1 (the loop).** After iteration $n$ of lines L3 to L9, $t = t_{n+1}$ and $U$ holds $U^{n+1} = H$ applied to $U^n$ with $\lambda_n = (t_{n+1} - t_n)/\Delta x$, where $t_k = k\Delta t$ for $k < N$ and $t_N = T$.

*Proof.* Induction on $n$. Line L8 computes all new values from the old ones (the list is rebuilt, not updated in place), so each $U_j^{n+1}$ uses $U^n$ only. The ghost values of line L7 are $U_{-1} = U_{m-1}$, $U_m = U_0$ in the periodic case and $U_{-1} = U_0$, $U_m = U_{m-1}$ in the transmissive case. $\square$

**Termination.** The loop runs $N = \lceil T/\Delta t \rceil$ times (up to the rounding slack), and each iteration does $m$ flux evaluations and $O(m)$ arithmetic.

**Lemma 2 (conservation).** With periodic boundary conditions, $\sum_j U_j^{n+1} = \sum_j U_j^n$.

*Proof.* $\sum_j (U_{j-1} + U_{j+1})/2 = \sum_j U_j$ and $\sum_j (f(U_{j+1}) - f(U_{j-1})) = 0$, because both sums run over all indices modulo $m$. $\square$

**Lemma 3 (monotonicity).** If $f \in C^1$ and $\lambda \max|f'(v)| \le 1$ for all $v$ between $\min_j U_j^n$ and $\max_j U_j^n$, then $H$ is nondecreasing in each argument on that range, and $\min_j U_j^n \le U_j^{n+1} \le \max_j U_j^n$.

*Proof.* $\partial H/\partial U_{j-1} = \frac12 + \frac{\lambda}{2} f'(U_{j-1}) \ge 0$ and $\partial H/\partial U_{j+1} = \frac12 - \frac{\lambda}{2} f'(U_{j+1}) \ge 0$. Since $H(c, c) = c$ for every constant $c$, monotonicity gives $H(U_{j-1}, U_{j+1}) \le H(M, M) = M$ with $M = \max_k U_k^n$, and similarly from below. $\square$

For the linear flux the lemma says that $U_j^{n+1} = \frac{1 + \nu}{2} U_{j-1}^n + \frac{1 - \nu}{2} U_{j+1}^n$ is a convex combination when $|\nu| \le 1$, so $\|U^{n+1}\|_\infty \le \|U^n\|_\infty$. By linearity the same holds for differences of two solutions: the scheme is stable in the max norm.

**Lemma 4 (local error for linear advection).** Let $f(u) = au$, $0 < |\nu| \le 1$, $u_0 \in C^2$ periodic with $M_2 = \max|u_0''|$, and $u(x, t) = u_0(x - at)$. Then the local error

$$\delta_j^{n} = u(x_j, t_{n+1}) - \Bigl(\frac{1 + \nu}{2} u(x_{j-1}, t_n) + \frac{1 - \nu}{2} u(x_{j+1}, t_n)\Bigr)$$

satisfies $|\delta_j^n| \le \frac{M_2}{2}(1 - \nu^2)\Delta x^2$.

*Proof.* Let $w(x) = u(x, t_n)$, so $u(x_j, t_{n+1}) = w(x_j - a\Delta t) = w(x_j - \nu\Delta x)$. The linear function $p$ that interpolates $w$ at $x_{j-1}$ and $x_{j+1}$ takes at $\xi = x_j - \nu\Delta x$ the value $\frac{1 + \nu}{2} w(x_{j-1}) + \frac{1 - \nu}{2} w(x_{j+1})$, because $\xi$ divides $[x_{j-1}, x_{j+1}]$ in the ratio $(1 - \nu) : (1 + \nu)$. So $\delta_j^n = w(\xi) - p(\xi)$, and $\xi \in [x_{j-1}, x_{j+1}]$ when $|\nu| \le 1$. The interpolation error formula gives $w(\xi) - p(\xi) = \frac{w''(\eta)}{2}(\xi - x_{j-1})(\xi - x_{j+1})$ for some $\eta$, and $|(\xi - x_{j-1})(\xi - x_{j+1})| = (1 - \nu)\Delta x \cdot (1 + \nu)\Delta x$. Since $w'' = u_0''(\cdot - at_n)$, $|w''| \le M_2$. $\square$

**Theorem (convergence of order 1).** Under the assumptions of Lemma 4, with $U_j^0 = u_0(x_j)$ and steps $\Delta t_n$ with Courant numbers $\nu_n = a\Delta t_n/\Delta x$, $0 < |\nu_n| \le 1$,

$$\max_j |u(x_j, t_N) - U_j^N| \le \frac{M_2}{2}\Delta x^2 \sum_{n=0}^{N-1}(1 - \nu_n^2).$$

With equal steps, $N = T/\Delta t$ and $\nu_n = \nu$, the right side is $\frac{T|a|(1 - \nu^2)}{2|\nu|} M_2 \Delta x$.

*Proof.* Let $E^n = \max_j |u(x_j, t_n) - U_j^n|$, with $E^0 = 0$. Subtracting the scheme from the definition of $\delta$,

$$u(x_j, t_{n+1}) - U_j^{n+1} = \frac{1 + \nu_n}{2}\bigl(u(x_{j-1}, t_n) - U_{j-1}^n\bigr) + \frac{1 - \nu_n}{2}\bigl(u(x_{j+1}, t_n) - U_{j+1}^n\bigr) + \delta_j^n.$$

The two weights are nonnegative with sum 1, so $E^{n+1} \le E^n + \frac{M_2}{2}(1 - \nu_n^2)\Delta x^2$ by Lemma 4. Summing over $n$ gives the claim, and $\Delta x^2 / \Delta t = |a| \Delta x/|\nu|$ gives the second form. $\blacksquare$

The bound is proved and non-asymptotic. It is zero for $|\nu| = 1$, where the scheme is the exact shift by one cell, and it grows like $1/|\nu|$ as $\nu \to 0$ at fixed $\Delta x$, as the experiments on the page show.

**Instability for $|\nu| > 1$.** The Fourier mode $U_j = e^{ij\theta}$ is multiplied by $g(\theta) = \cos\theta - i\nu\sin\theta$ in one step (substitute it into the linear form). At $\theta = \pi/2$, $|g| = |\nu| > 1$, so with periodic data containing this mode the solution grows like $|\nu|^n$ and the scheme cannot be stable; by the Lax equivalence theorem it does not converge.

**Nonlinear conservation laws (cited).** The scheme is in conservation form with a consistent numerical flux $\hat F(v, v) = f(v)$. By the Lax-Wendroff theorem (1960), if the numerical solutions converge boundedly almost everywhere as $\Delta x, \Delta t \to 0$, the limit is a weak solution. By Lemma 3 the scheme is monotone under the CFL condition, and Crandall and Majda (1980) proved that conservative monotone schemes converge to the entropy solution, with an $L^1$ error of order $\Delta x^{1/2}$ for data of bounded variation (Kuznetsov's estimate). These results are cited, not proved here.
