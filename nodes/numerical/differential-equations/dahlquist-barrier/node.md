---
tag: PG6EGE
kind: theorem
slug: dahlquist-barrier
name: Dahlquist's second barrier
aliases:
- Dahlquist order barrier
- second Dahlquist barrier
- Dahlquist's A-stability barrier
area: numerical/differential-equations
level: advanced
summary: No A-stable linear multistep method has order greater than two. Among A-stable methods of order two, the trapezoidal rule has the smallest error constant, -1/12.
prereqs: [a-stability, zero-stability]
see_also: [linear-multistep-methods, backward-differentiation-formulas, adams-moulton-methods, dahlquist-equivalence-theorem, stability-region, stiff-ode-problem, gauss-legendre-runge-kutta, crank-nicolson-method]
sources:
  - paper: doi:10.1007/BF01963532
    title: "G. Dahlquist, A special stability problem for linear multistep methods, BIT 3 (1963) 27-43"
    locator: the definition of A-stability, the bound p ≤ 2 for A-stable linear multistep methods, and the optimality of the trapezoidal rule
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section V.1 (stability of multistep methods, A-stability and the second Dahlquist barrier, with proof)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section III.2 (order of multistep methods and the error constant) and Section III.3 (stability and the first Dahlquist barrier)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 4 (stiff equations, A-stability of multistep methods and the Dahlquist barrier)
  - paper: "G. Wanner, E. Hairer and S. P. Nørsett, Order stars and stability theorems, BIT 18 (1978) 475-489"
    locator: order stars and a second proof of the barrier, with its extension to multistep methods with higher derivatives
  - paper: "G. Dahlquist, Convergence and stability in the numerical integration of ordinary differential equations, Mathematica Scandinavica 4 (1956) 33-53"
    locator: the first barrier on the order of zero-stable methods
---

## Statement

**Setting.** A [linear multistep method](/linear-multistep-methods/) with $k$ steps is $\sum_{j=0}^k\alpha_jy_{n+j} = h\sum_{j=0}^k\beta_jf(t_{n+j}, y_{n+j})$, with characteristic polynomials $\rho(\zeta) = \sum\alpha_j\zeta^j$ and $\sigma(\zeta) = \sum\beta_j\zeta^j$, $\alpha_k \ne 0$. We assume that $\rho$ and $\sigma$ have no common factor. The method has order $p \ge 1$ if
$$\rho(e^h) - h\sigma(e^h) = C_{p+1}h^{p+1} + O(h^{p+2}), \qquad C_{p+1} \ne 0.$$
Then $\rho(1) = 0$ and $\sigma(1) = \rho'(1)$. The **error constant** is $C = C_{p+1}/\sigma(1)$, which does not change when $\rho$ and $\sigma$ are multiplied by the same number. On the test equation $y' = \lambda y$ with $z = h\lambda$, the stability polynomial is $\pi(\zeta; z) = \rho(\zeta) - z\sigma(\zeta)$. The method is [A-stable](/a-stability/) if for every $z$ with $\operatorname{Re}z \le 0$ all roots of $\pi(\cdot\,; z)$ satisfy $|\zeta| \le 1$, and the roots with $|\zeta| = 1$ are simple.

**Theorem (Dahlquist 1963).**

1. An A-stable linear multistep method has order $p \le 2$.
2. An A-stable linear multistep method of order 2 has error constant $C \le -\tfrac1{12}$. The trapezoidal rule $y_{n+1} = y_n + \tfrac h2(f_n + f_{n+1})$ is A-stable and has $C = -\tfrac1{12}$.

## In plain words

Stiff problems need methods that stay stable for every step size when the solution decays. Among linear multistep methods, which reuse past values of the solution and of $f$, this property costs accuracy. However many past values a method uses, if it is stable on the whole left half plane, its error per step can shrink at most like $h^3$, so the method is at most second order. Among those second order methods, the trapezoidal rule has the smallest error. To get higher order together with this kind of stability, you must leave the class of linear multistep methods, or accept stability on a smaller region.

## Proof

**Lemma 1.** Let the method be A-stable. Then:

- (i) the roots of $\rho$ on the unit circle are simple, and $\sigma(1) \ne 0$;
- (ii) for $|\zeta| > 1$, $\sigma(\zeta) \ne 0$ and $\operatorname{Re}\big(\rho(\zeta)/\sigma(\zeta)\big) > 0$.

*Proof.* (i) $z = 0$ is in the closed left half plane, and $\pi(\cdot\,; 0) = \rho$. Since $\rho(1) = 0$ is a simple root, $\sigma(1) = \rho'(1) \ne 0$.

(ii) Suppose $\sigma(\zeta_1) = 0$ with $|\zeta_1| > 1$. Then $\rho(\zeta_1) \ne 0$, since $\rho$ and $\sigma$ have no common factor. Take a small circle $\Gamma$ around $\zeta_1$ that lies in $|\zeta| > 1$ and has no zero of $\sigma$ on it. Let $m = \min_\Gamma|\sigma| > 0$ and $M = \max_\Gamma|\rho|$. For real $z < -M/m$, $|z\sigma| > |\rho|$ on $\Gamma$. By Rouché's theorem, $\pi(\cdot\,; z) = -(z\sigma - \rho)$ has as many zeros inside $\Gamma$ as $\sigma$, so at least one. That zero has modulus greater than 1, which contradicts A-stability. So $\sigma(\zeta) \ne 0$ for $|\zeta| > 1$. Now let $|\zeta| > 1$ and $z = \rho(\zeta)/\sigma(\zeta)$. Then $\pi(\zeta; z) = 0$ with $|\zeta| > 1$, so A-stability forces $\operatorname{Re}z > 0$. $\square$

**Change of variable.** Put $w = (\zeta - 1)/(\zeta + 1)$, so $\zeta = (1 + w)/(1 - w)$. Since $|1 + w| > |1 - w|$ exactly when $\operatorname{Re}w > 0$, this maps $|\zeta| > 1$ onto the open right half plane $H$. The circle $|\zeta| = 1$ minus $\zeta = -1$ goes to the imaginary axis, $\zeta = 1$ to $w = 0$, and $\zeta = -1$ to $w = \infty$. Let $r(w) = \rho(\zeta)/\sigma(\zeta)$, a rational function of $w$. By Lemma 1, $r$ has no poles in $H$ and $\operatorname{Re}r > 0$ there, so $1/r$ is analytic in $H$ with $\operatorname{Re}(1/r) = \operatorname{Re}r/|r|^2 > 0$.

**Lemma 2 (expansion at $w = 0$).** Let $p \ge 2$, and let $C^\star = C$ if $p = 2$ and $C^\star = 0$ if $p \ge 3$. Then
$$\phi(w) := \frac1{r(w)} - \frac1{2w} = -\Big(\frac16 + 2C^\star\Big)w + O(w^2).$$

*Proof.* Near $\zeta = 1$ put $h = \log\zeta$, which is analytic. Dividing the order relation by $\sigma(e^h) = \sigma(1) + O(h)$ gives $r = h + C^\star h^3 + O(h^4)$. In the new variable, $h = \log(1 + w) - \log(1 - w) = 2w + \tfrac23w^3 + O(w^5)$, so $h^3 = 8w^3 + O(w^5)$ and
$$r(w) = 2w\Big(1 + \big(\tfrac13 + 4C^\star\big)w^2 + O(w^3)\Big).$$
Inverting, $1/r = \frac1{2w}\big(1 - (\tfrac13 + 4C^\star)w^2 + O(w^3)\big)$. $\square$

**Lemma 3.** If the method is A-stable and $p \ge 1$, then $\operatorname{Re}\phi(w) \ge 0$ for all $w \in H$.

*Proof.* The function $\phi$ is rational. In $H$ it is analytic. Its possible poles on the boundary of $H$ are:

- $w = 0$: here $1/r$ has a simple pole with residue $\tfrac12$, because $r(w) = 2w + O(w^2)$, so $\phi$ is analytic at 0;
- points $w_k = iy_k \ne 0$ that come from roots $\zeta_k \ne \pm1$ of $\rho$ on the unit circle;
- $w = \infty$, if $\rho(-1) = 0$.

At $w_k$, the root $\zeta_k$ is simple by Lemma 1(i), $\sigma(\zeta_k) \ne 0$ since there is no common factor, and the change of variable is conformal. So $1/r$ has a simple pole at $w_k$ with some residue $c_k$. On a small half circle $w = w_k + \delta e^{i\theta}$, $|\theta| < \pi/2$, we have $1/r = c_k\delta^{-1}e^{-i\theta} + O(1)$. Since $\operatorname{Re}(1/r) > 0$ in $H$, letting $\delta \to 0$ gives $\operatorname{Re}(c_ke^{-i\theta}) \ge 0$ for all $|\theta| < \pi/2$. This forces $c_k > 0$. In the same way, if $\rho(-1) = 0$, then $1/r = c_\infty w + O(1)$ near $\infty$ with $c_\infty > 0$. Let
$$P(w) = \sum_k\frac{c_k}{w - iy_k} + c_\infty w$$
(with $c_\infty = 0$ if $\rho(-1) \ne 0$). Then $\operatorname{Re}P(w) = \operatorname{Re}w\,\big(\sum_kc_k/|w - iy_k|^2 + c_\infty\big) \ge 0$ in $H$, and $\operatorname{Re}P = 0$ on the imaginary axis away from the $w_k$.

The function $\psi = \phi - P$ has no poles in $\overline H$, and it has a finite limit at $\infty$. So $\operatorname{Re}\psi$ is harmonic in $H$ and continuous on $\overline H \cup \{\infty\}$. On the imaginary axis, at points $iy$ with $y \ne 0$ that are not poles, $\operatorname{Re}(1/(2iy)) = 0$ and $\operatorname{Re}P(iy) = 0$. So $\operatorname{Re}\psi(iy) = \operatorname{Re}(1/r(iy)) \ge 0$, as a limit of positive values. By continuity, $\operatorname{Re}\psi \ge 0$ on the whole boundary, including $0$, the $w_k$ and $\infty$. By the minimum principle for harmonic functions (apply it on the disk $|\zeta| > 1$ seen from $\infty$, or after a Möbius map to the unit disk), $\operatorname{Re}\psi \ge 0$ in $H$. Hence $\operatorname{Re}\phi = \operatorname{Re}\psi + \operatorname{Re}P \ge 0$ in $H$. $\square$

**Proof of the theorem.** Suppose the method is A-stable of order $p \ge 2$. For small real $\varepsilon > 0$, Lemma 2 gives $\operatorname{Re}\phi(\varepsilon) = -(\tfrac16 + 2C^\star)\varepsilon + O(\varepsilon^2)$, and Lemma 3 says this is $\ge 0$. So $\tfrac16 + 2C^\star \le 0$, that is $C^\star \le -\tfrac1{12}$. If $p \ge 3$, then $C^\star = 0$, which is impossible. So $p \le 2$, and for $p = 2$, $C \le -\tfrac1{12}$.

For the trapezoidal rule, $\rho(\zeta) = \zeta - 1$ and $\sigma(\zeta) = (\zeta + 1)/2$. Expanding, $e^h - 1 - \tfrac h2(e^h + 1) = -\tfrac1{12}h^3 + O(h^4)$ and $\sigma(1) = 1$, so $C = -\tfrac1{12}$. The only root of $\pi(\zeta; z)$ is $\zeta = (1 + z/2)/(1 - z/2)$, and $|\zeta| \le 1$ exactly when $\operatorname{Re}z \le 0$. So the rule is A-stable. In the variable $w$, $r(w) = 2w$ and $\phi \equiv 0$, so the bound is attained with equality. $\square$

## Consequences

- **Error constants of A-stable methods.** Computed exactly with `Fraction`: the trapezoidal rule has $C = -\tfrac1{12}$. [BDF2](/backward-differentiation-formulas/), $\tfrac32y_{n+2} - 2y_{n+1} + \tfrac12y_n = hf_{n+2}$, is A-stable with $C = -\tfrac13$. For BDF2, Lemma 2 gives $\phi(w) = \tfrac12w + O(w^2)$, which agrees with Lemma 3. The $\theta$-method $y_{n+1} = y_n + h(\theta f_{n+1} + (1 - \theta)f_n)$ is A-stable for $\theta \ge \tfrac12$, but has order 1 unless $\theta = \tfrac12$.
- **Higher order Adams-Moulton methods are not A-stable.** The two-step [Adams-Moulton method](/adams-moulton-methods/) has order 3, so by the theorem it cannot be A-stable. Indeed its real stability interval is $[-6, 0]$. At $z = -7$ the roots of $\pi$ have moduli $0.1386$ and $1.0747$. At $z = -5.9$ the largest modulus is $0.9916$, and at $z = -6.1$ it is $1.0082$ (computed).
- **A practical test.** By Lemma 1(ii) and continuity, an A-stable method has $\operatorname{Re}\big(\rho(e^{i\theta})/\sigma(e^{i\theta})\big) \ge 0$ for all $\theta$: the boundary locus of the [stability region](/stability-region/) never enters the open left half plane. This necessary condition is the usual first check. For BDF2, $\rho(\zeta)/\sigma(\zeta) = \tfrac32 - 2\zeta^{-1} + \tfrac12\zeta^{-2}$, and its real part on the circle is $\tfrac32 - 2\cos\theta + \tfrac12\cos2\theta = (1 - \cos\theta)^2 \ge 0$.
- **How stiff solvers live with the barrier.** BDF codes use BDF3 to BDF5, which are only A($\alpha$)-stable, with $\alpha$ below $90°$. Implicit Runge-Kutta methods are not linear multistep methods and are not bound by the theorem: the [Gauss methods](/gauss-legendre-runge-kutta/) are A-stable of order $2s$, and the [Radau IIA methods](/radau-iia-methods/) are A-stable and [L-stable](/l-stability/) of order $2s - 1$. In PDE time stepping the trapezoidal rule appears as the [Crank-Nicolson method](/crank-nicolson-method/).

## Tightness

- **Order 2 is attained**, by the trapezoidal rule and by BDF2. So the bound $p \le 2$ cannot be improved.
- **The constant $-\tfrac1{12}$ is attained** by the trapezoidal rule. This page proves only the bound, not that the trapezoidal rule is the only method that attains it.
- **A($\alpha$)-stability escapes the barrier.** BDF3 has order 3 and is A($\alpha$)-stable with $\alpha$ close to $86°$. Stability on a sector that is smaller than the half plane does not force $p \le 2$.
- **Linear multistep methods only.** Methods with several stages, such as Runge-Kutta methods, or with higher derivatives, are not covered. For multistep methods that use derivatives of higher order, Daniel and Moore conjectured a similar barrier. Wanner, Hairer and Nørsett (1978) proved it with order stars.

## History

Dahlquist (1956) proved the first barrier: a zero-stable $k$-step method has order at most $k + 1$ for odd $k$ and $k + 2$ for even $k$, and at most $k$ if it is explicit. In 1963, in a short paper in BIT, he introduced the notion of A-stability for stiff problems and proved the theorem above with an argument from complex function theory. The proof on this page is an argument of that kind, with positive real parts on a half plane. Wanner, Hairer and Nørsett (1978) gave a geometric proof with order stars, which also covers the multistep methods with higher derivatives of the Daniel-Moore conjecture. The result is called the second Dahlquist barrier to separate it from the first.

## References
