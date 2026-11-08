---
title: Shooting with a convergent integrator finds a nearby root and an accurate profile
proves: [correctness, termination, convergence]
status: full
---

**Setting.** The problem is $y'' = g(x, y, y')$ on $[a, b]$ with $y(a) = \alpha$, $y(b) = \beta$. Write $u = (y, y') \in \mathbb{R}^2$ and $u' = F(x, u) = (u_2, g(x, u_1, u_2))$. We use the max norm on $\mathbb{R}^2$. We assume that $g$ is $C^4$ and that $F$ is Lipschitz in $u$ with constant $L$ on $[a, b] \times \mathbb{R}^2$. Then for every slope $s$ the initial value problem $u(a) = (\alpha, s)$ has a unique solution $u(x; s)$ on $[a, b]$ (the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)), and $u$ is $C^1$ in $s$. The shooting function is $\Phi(s) = y(b; s) - \beta$. The method replaces $u(b; s)$ by the result $u_h(b; s)$ of $n$ steps of RK4 with $h = (b - a)/n$, and $\Phi$ by $\Phi_h(s) = y_h(b; s) - \beta$.

**Termination.** The loop of line L2 runs at most `max_iter` times. Each pass solves one initial value problem with $n \ge 1$ steps, which is a finite computation. So the procedure stops, either by returning at line L4 or L6 or by reporting failure after the loop. A division by zero at line L5 is reported as an error, since then $\Phi_h'(s) = 0$ and the Newton step is not defined.

**Lemma 1 (the derivative is exact for the discrete map).** Line L3 integrates the system for $(y, y')$ together with the variational system for $w = \partial y / \partial s$, namely $w'' = g_y w + g_{y'} w'$ with $w(a) = 0$, $w'(a) = 1$, using the same RK4 steps. The value $w_h(b)$ it returns equals $\Phi_h'(s)$ exactly.

*Proof.* One RK4 step is a composition of evaluations of $F$ and linear combinations. Differentiate every stage equation $K_i = F(x + c_i h, U + h \sum_j a_{ij} K_j)$ with respect to $s$. The derivatives $\partial K_i / \partial s$ satisfy $\partial K_i / \partial s = F_u(x + c_i h, U_i)(\partial U / \partial s + h \sum_j a_{ij}\, \partial K_j / \partial s)$, which are exactly the stage equations of RK4 applied to the linearized system $W' = F_u(x, u) W$, with the stage values $U_i$ of the main system. The augmented integration of line L3 computes these same quantities. By induction over the $n$ steps, $W_h(b) = \partial u_h(b; s) / \partial s$, and its first component is $\Phi_h'(s)$. $\square$

So line L5 is a true Newton step for $\Phi_h$, and the classical local theorem for Newton's method applies: if $\Phi_h(s_h) = 0$, $\Phi_h'(s_h) \ne 0$ and $\Phi_h$ is $C^2$ near $s_h$, then for $s_0$ close enough to $s_h$ the iterates converge to $s_h$ quadratically (see [Newton-Raphson method](/newton-raphson-method/)). If $g$ is affine in $(y, y')$, then $u_h(b; s)$ is affine in $s$, $\Phi_h$ is an affine function, and one Newton step from any $s_0$ lands on its root up to rounding.

**Theorem (convergence of the computed slope and profile).** Let $s^*$ be a simple root: $\Phi(s^*) = 0$ and $\Phi'(s^*) \ne 0$. Then there are $\delta > 0$, $h_0 > 0$ and $C' > 0$ such that for every $h \le h_0$ the discrete function $\Phi_h$ has a root $s_h$ with $|s_h - s^*| \le \delta$, every such root satisfies $|s_h - s^*| \le C' h^4$, and $\max_k \|u_h(x_k; s_h) - u(x_k; s^*)\| \le C'' h^4$ on the grid.

*Proof.* Since $\Phi'$ is continuous, choose $\delta > 0$ with $|\Phi'(s)| \ge m > 0$ for all $s \in I = [s^* - \delta, s^* + \delta]$. The solutions $u(\cdot; s)$, $s \in I$, form a compact family, so their derivatives up to order 5 are bounded uniformly on $I \times [a, b]$, and the RK4 convergence theorem (HNW I, Section II.3, and the page on [Runge-Kutta methods](/runge-kutta-methods/)) gives one constant $C$ with
$$\|u_h(x_k; s) - u(x_k; s)\| \le C h^4 \qquad \text{for all } s \in I \text{ and all grid points } x_k.$$
In particular $|\Phi_h(s) - \Phi(s)| \le C h^4$ on $I$.

*Existence.* By the mean value theorem, $|\Phi(s^* \pm \delta)| \ge m\delta$ and the two values have opposite signs. Take $h_0$ with $C h_0^4 < m\delta$. Then $\Phi_h(s^* + \delta)$ and $\Phi_h(s^* - \delta)$ also have opposite signs. The RK4 map is continuous in $s$, so $\Phi_h$ is continuous, and the intermediate value theorem gives a root $s_h \in I$.

*Accuracy of the slope.* For any root $s_h \in I$, $m|s_h - s^*| \le |\Phi(s_h) - \Phi(s^*)| = |\Phi(s_h)| = |\Phi(s_h) - \Phi_h(s_h)| \le C h^4$. So $|s_h - s^*| \le C h^4 / m$.

*Accuracy of the profile.* Split the error at a grid point $x_k$:
$$\|u_h(x_k; s_h) - u(x_k; s^*)\| \le \|u_h(x_k; s_h) - u(x_k; s_h)\| + \|u(x_k; s_h) - u(x_k; s^*)\|.$$
The first term is at most $C h^4$. The two exact solutions start at $(\alpha, s_h)$ and $(\alpha, s^*)$, so by the [Gronwall inequality](/gronwall-inequality/) the second term is at most $e^{L(x_k - a)} |s_h - s^*|$. Together the error is at most $(C + e^{L(b - a)} C/m) h^4$. $\square$

**What the proof does not cover.** The theorem is about exact arithmetic. In floating point the computed $u_h(b; s)$ carries a rounding error of size about $\varepsilon \max_x \|u\|$ times the growth of perturbations, which the Gronwall bound only controls by $e^{L(b - a)}$. For $y'' = \lambda^2 y$ the growth of a change in the slope is $\sinh(\lambda(b - a))/\lambda$, so single shooting loses about $\lambda (b - a) / \ln 10$ decimal digits. Multiple shooting with $K$ equal segments replaces this factor by $\sinh(\lambda (b - a)/K)/\lambda$ per segment. The matching conditions form a nonlinear system whose Newton matrix is the block bidiagonal matrix built from the segment Jacobians, which are exact for the discrete maps by Lemma 1, so the same local quadratic convergence holds when that matrix is nonsingular at the root (Stoer and Bulirsch, Section 7.3.5; Ascher, Mattheij and Russell, Section 4.3). We state this last point as a known result and check it numerically in the tests.
