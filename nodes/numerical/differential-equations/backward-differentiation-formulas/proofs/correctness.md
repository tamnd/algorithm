---
title: Order, zero-stability and A-stability of the backward differentiation formulas
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$, $y \in \mathbb{R}^d$ with a norm $\|\cdot\|$, uniform grid $t_n = t_0 + nh$, $\nabla v_{n+1} = v_{n+1} - v_n$. The $k$-step BDF is $\sum_{j=1}^k\frac1j\nabla^jy_{n+1} = hf(t_{n+1}, y_{n+1})$.

## Lemma 1 (the formula differentiates the interpolant)

Let $P$ be the polynomial of degree at most $k$ with $P(t_{n+1-i}) = v_{n+1-i}$ for $i = 0, \dots, k$. Then $hP'(t_{n+1}) = \sum_{j=1}^k\frac1j\nabla^jv_{n+1}$.

*Proof.* Newton's backward difference form gives $P(t_{n+1} + sh) = \sum_{j=0}^k\binom{s + j - 1}{j}\nabla^jv_{n+1}$, where $\binom{s+j-1}{j} = s(s+1)\cdots(s+j-1)/j!$. For $j \ge 1$ the derivative of this product at $s = 0$ is $(j - 1)!/j! = 1/j$, since only the term in which the factor $s$ is differentiated survives. So $\frac{d}{ds}P(t_{n+1} + sh)|_{s=0} = hP'(t_{n+1}) = \sum_{j \ge 1}\frac1j\nabla^jv_{n+1}$. $\square$

In particular the coefficient of $v_{n+1}$ is $\alpha_0 = \sum_{j=1}^k 1/j$, because $\nabla^jv_{n+1}$ contains $v_{n+1}$ with coefficient 1.

## Lemma 2 (local truncation error)

Let $y \in C^{k+1}$, $M_{k+1} = \max\|y^{(k+1)}\|$, and $\tau_{n+1} = \sum_j\frac1j\nabla^jy(t_{n+1}) - hy'(t_{n+1})$. Then $\|\tau_{n+1}\| \le \frac{1}{k+1}M_{k+1}h^{k+1}$, and for $d = 1$, $\tau_{n+1} = -\frac{1}{k+1}h^{k+1}y^{(k+1)}(\xi)$ for some $\xi \in (t_{n+1-k}, t_{n+1})$.

*Proof.* Let $P$ interpolate $y$ at $t_{n+1}, \dots, t_{n+1-k}$. By Lemma 1, $\tau_{n+1} = h(P'(t_{n+1}) - y'(t_{n+1}))$. Write the interpolation error as $y(t) - P(t) = w(t)\,g(t)$ with $w(t) = \prod_{i=0}^k(t - t_{n+1-i})$ and $g(t) = y[t_{n+1-k}, \dots, t_{n+1}, t]$, a $C^1$ function by the Hermite-Genocchi formula. Since $w(t_{n+1}) = 0$, $(y - P)'(t_{n+1}) = w'(t_{n+1})g(t_{n+1})$, and $w'(t_{n+1}) = \prod_{i=1}^k(ih) = k!h^k$. The confluent divided difference $g(t_{n+1})$ is an average of $y^{(k+1)}/(k+1)!$ over a simplex, so $\|g(t_{n+1})\| \le M_{k+1}/(k+1)!$, and for $d = 1$ it equals $y^{(k+1)}(\xi)/(k+1)!$. Hence $\tau_{n+1} = -h\cdot k!h^k g(t_{n+1})$, which gives both claims. $\square$

So BDF$k$ is [consistent](/consistency/) of order exactly $k$ with error constant $-1/(k+1)$. The tests check, with exact fractions, that $C_0 = \dots = C_k = 0$ and $C_{k+1} = -1/(k+1)$ for $k = 1, \dots, 7$.

## Zero-stability

$\rho(\zeta) = \sum_{i=0}^k\alpha_i\zeta^{k-i}$, and $\rho(1) = 0$ because each $\nabla^j$ annihilates constants. The remaining $k - 1$ roots are not available in closed form for $k \ge 3$; for $k = 2$, $\rho(\zeta) = \tfrac32\zeta^2 - 2\zeta + \tfrac12 = \tfrac12(\zeta - 1)(3\zeta - 1)$, with the spurious root $1/3$. The tests compute all roots for $k = 2, \dots, 7$ (Durand-Kerner iteration) and find the largest spurious modulus $0.3333, 0.4264, 0.5609, 0.7087, 0.8634$ for $k \le 6$ and $1.0222$ for $k = 7$. This is a numerical verification, not a proof; the statement that BDF$k$ is zero-stable exactly for $k \le 6$ is a theorem (Hairer, Nørsett and Wanner, Section III.3, and Cryer 1972 for all $k \ge 7$), which we cite. For $k \le 6$, Dahlquist's equivalence theorem then gives convergence of order $k$ for Lipschitz $f$ and accurate starting values. In the implementation the starting values come from the Gauss method of order 6, whose local errors are $O(h^7)$, so they do not limit the order.

## Theorem (BDF2 is A-stable)

For every $z$ with $\operatorname{Re}z \le 0$, all roots of $\pi(\zeta; z) = \rho(\zeta) - z\zeta^2$ satisfy $|\zeta| \le 1$, and roots of modulus 1 are simple.

*Proof.* A root $\zeta = e^{i\theta}$ on the unit circle occurs exactly when $z = z(\theta) = \rho(e^{i\theta})/e^{2i\theta} = (1 - e^{-i\theta}) + \tfrac12(1 - e^{-i\theta})^2$. Its real part is
$$\operatorname{Re}z(\theta) = (1 - \cos\theta) + \tfrac12(1 - 2\cos\theta + \cos 2\theta) = (1 - \cos\theta) + (\cos^2\theta - \cos\theta) = (1 - \cos\theta)^2 \ge 0,$$
with equality only for $\theta = 0$, that is $z = 0$. So for $\operatorname{Re}z < 0$ no root lies on the unit circle. The open half-plane is connected and the roots depend continuously on $z$ (the leading coefficient $\tfrac32 - z$ does not vanish there), so the number of roots outside the closed unit disc is constant on it. For real $z \to -\infty$, the roots of $\pi(\zeta; z)/(-z) = \zeta^2 - \rho(\zeta)/z$ tend to the double root 0 of $\zeta^2$, so that number is 0. On the imaginary axis, $z \ne 0$ gives no root on the circle, and by continuity from the left no root outside; at $z = 0$ the roots are $1$ and $1/3$, and 1 is simple. $\square$

For $k \ge 3$ the boundary locus enters the left half-plane (for $k = 3$ it passes through $-\tfrac1{12} + \tfrac{3\sqrt3}{4}i$, see [A-stability](/a-stability/)), so BDF$k$ is not A-stable; this is also forced by the second Dahlquist barrier. The A($\alpha$) angles are computed in the tests as $\min|\arg(-z(\theta))|$ over the points of the locus with $\operatorname{Re}z(\theta) < 0$.

## Stiff decay

The roots of $\rho(\zeta) - z\zeta^k$, divided by $-z$, are the roots of $\zeta^k - \rho(\zeta)/z$, which tend to the $k$-fold root 0 of $\zeta^k$ as $|z| \to \infty$. Hence for $y' = \lambda y$ with $|h\lambda|$ large the numerical solution is multiplied in each step by factors close to 0, whatever the starting values: very stiff components are damped at once.

## Linear invariants

If $c^Tf(t, y) = 0$ for all $(t, y)$, then $c^T$ applied to the BDF relation gives $\sum_i\alpha_ic^Ty_{n+1-i} = 0$, a zero-stable recurrence with constant solutions only when started at a constant: since $c^Ty_0 = \dots = c^Ty_{k-1}$ (the Gauss starting steps preserve linear invariants too, as $c^Ty_{n+1} = c^Ty_n + h\sum b_ic^Tk_i$), and $\sum_i\alpha_i = 0$, the recurrence gives $c^Ty_{n+1} = -\sum_{i \ge 1}(\alpha_i/\alpha_0)c^Ty_{n+1-i} = c^Ty_n$. So $c^Ty_n$ is constant up to rounding and the Newton tolerance, as the Robertson test shows.
