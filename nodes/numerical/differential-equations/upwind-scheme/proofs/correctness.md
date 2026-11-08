---
title: The upwind scheme is stable for |ν| ≤ 1 and converges at first order in the max norm
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We solve $u_t + a u_x = 0$ on the periodic interval $[0, 1)$ with $m$ cells of width $\Delta x = 1/m$ and time steps $\Delta t$, and write $\nu = a\Delta t/\Delta x$ for the Courant number. We treat $a \ge 0$; the case $a < 0$ is the mirror image under $x \mapsto -x$. The grid values are $U_j^n$, and the norm is $\|U\|_\infty = \max_j |U_j|$. The exact solution is $u(x, t) = u_0(x - at)$.

**Termination.** Line L1 returns a finite $N \ge 0$ and the loop of line L3 runs $N$ times; each pass does $\Theta(m)$ arithmetic. Line L4 sets the last time to $T$ exactly, so the final step has length $T - t_{N-1} \in (0, \Delta t]$ (up to the slack $\delta$) and its Courant number lies in $(0, \nu]$. For $T = 0$, $N = 0$ and the input is returned unchanged.

**Lemma 1 (convex combination).** For $0 \le \nu \le 1$, line L7 reads $U_j^{n+1} = (1 - \nu) U_j^n + \nu U_{j-1}^n$, a convex combination. Hence:
1. $\min_j U_j^n \le U_j^{n+1} \le \max_j U_j^n$ (discrete maximum principle), and in particular $\|U^{n+1}\|_\infty \le \|U^n\|_\infty$;
2. the scheme is monotone: $U \le V$ componentwise implies $U^{n+1} \le V^{n+1}$;
3. $\sum_j U_j^{n+1} = \sum_j U_j^n$ (periodic), so the scheme is conservative;
4. $TV(U^{n+1}) \le TV(U^n)$ with $TV(U) = \sum_j |U_{j+1} - U_j|$.

*Proof.* Parts 1 to 3 are immediate from nonnegative weights summing to 1. For part 4, $U_{j+1}^{n+1} - U_j^{n+1} = (1 - \nu)(U_{j+1}^n - U_j^n) + \nu(U_j^n - U_{j-1}^n)$; take absolute values, use the triangle inequality and sum over $j$ with periodic indices. $\square$

**Lemma 2 (local truncation error).** Let $u_0 \in C^2$ be periodic and $M = \max |u_0''|$. Define the local truncation error
$$\tau_j^n = \frac{u(x_j, t_{n+1}) - u(x_j, t_n)}{\Delta t} + a\,\frac{u(x_j, t_n) - u(x_{j-1}, t_n)}{\Delta x}.$$
Then $|\tau_j^n| \le \frac{|a|}{2}(\Delta x + |a|\Delta t) M$.

*Proof.* By Taylor's theorem with the Lagrange remainder, $u(x_j, t_{n+1}) = u + \Delta t\,u_t + \frac{\Delta t^2}{2} u_{tt}(\xi)$ and $u(x_{j-1}, t_n) = u - \Delta x\,u_x + \frac{\Delta x^2}{2} u_{xx}(\eta)$. Since $u_t + a u_x = 0$, the first-order terms cancel, leaving $\tau = \frac{\Delta t}{2} u_{tt}(\xi) - \frac{a\Delta x}{2} u_{xx}(\eta)$. As $u_{tt} = a^2 u_{xx}$ and $|u_{xx}| \le M$ everywhere, the bound follows. $\square$

A finer expansion gives $\tau = \frac{a\Delta x}{2}(\nu - 1) u_{xx} + O(\Delta x^2)$, so the scheme is a second-order approximation of the modified equation $u_t + a u_x = \frac{a\Delta x}{2}(1 - \nu) u_{xx}$. This explains the smearing of fronts and the exactness at $\nu = 1$.

**Theorem (convergence, proved).** Let $u_0 \in C^2$ be periodic, $a \ge 0$ and $0 \le \nu \le 1$. Then the grid error $e_j^n = u(x_j, t_n) - U_j^n$ with $e^0 = 0$ satisfies
$$\|e^n\|_\infty \le t_n \frac{a}{2}(\Delta x + a\Delta t) M \le t_n \frac{a\Delta x}{2}(1 + \nu) M.$$

*Proof.* The exact values satisfy the scheme up to $\Delta t\,\tau$: $u(x_j, t_{n+1}) = (1 - \nu) u(x_j, t_n) + \nu u(x_{j-1}, t_n) + \Delta t\,\tau_j^n$. Subtract line L7: $e_j^{n+1} = (1 - \nu)e_j^n + \nu e_{j-1}^n + \Delta t\,\tau_j^n$. By Lemma 1, $\|e^{n+1}\|_\infty \le \|e^n\|_\infty + \Delta t \max|\tau|$, and induction with Lemma 2 gives the claim. A shortened last step has a smaller Courant number in $[0, \nu]$ and a smaller $\Delta t$, so the same bound holds. $\square$

**Theorem (instability for |ν| > 1, proved).** If $\nu > 1$, the mode $U_j^0 = (-1)^j$ (with $m$ even) is multiplied by $1 - 2\nu$ per step, and $|1 - 2\nu| > 1$. So no bound $\|U^n\|_\infty \le K\|U^0\|_\infty$ with $K$ independent of $n$ holds, and the method is not stable.

*Proof.* With $U_j = (-1)^j$, $U_{j-1} = -U_j$, so line L7 gives $U_j^{n+1} = (1 - \nu)U_j - \nu U_j = (1 - 2\nu)U_j$. $\square$

In Fourier form, the mode $e^{ij\theta}$ is multiplied by $g(\theta) = 1 - \nu(1 - e^{-i\theta})$, and
$$|g(\theta)|^2 = 1 - 2\nu(1 - \nu)(1 - \cos\theta),$$
which is at most 1 for all $\theta$ exactly when $0 \le \nu \le 1$. This is the [von Neumann](/von-neumann-stability-analysis/) form of the same statement, in the $\ell^2$ norm. It agrees with the [CFL condition](/courant-friedrichs-lewy-condition/): the numerical domain of dependence of $U_j^{n}$ is $[x_j - n\Delta x, x_j]$, and it contains the characteristic foot $x_j - a t_n$ exactly when $\nu \le 1$.

**Nonlinear conservation laws.** For $u_t + f(u)_x = 0$ with $f$ nondecreasing, the conservative upwind scheme is $U_j^{n+1} = H(U_{j-1}, U_j) = U_j - \lambda(f(U_j) - f(U_{j-1}))$ with $\lambda = \Delta t/\Delta x$. If $\lambda \max f' \le 1$ on the range of the data, then $\partial H/\partial U_j = 1 - \lambda f'(U_j) \ge 0$ and $\partial H/\partial U_{j-1} = \lambda f'(U_{j-1}) \ge 0$, so the scheme is monotone, and by the same argument as Lemma 1 it is TVD and satisfies the maximum principle. Monotone conservative consistent schemes converge to the entropy solution (Crandall and Majda, 1980); conservative schemes that converge give weak solutions with the right shock speeds (the Lax-Wendroff theorem). We cite both as known results (LeVeque 2002, Chapter 12). For $f'$ that changes sign, the Roe flux of the implementation is not monotone and can keep an entropy-violating expansion shock, as the tests show.
