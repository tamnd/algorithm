---
tag: GC32TY
kind: theorem
slug: popov-criterion
name: Popov criterion
aliases:
- Popov stability criterion
area: control/stability
level: advanced
summary: A Lur'e system with a time-invariant sector nonlinearity is absolutely stable if a line in the Popov plot bounds the frequency response.
prereqs: [lure-problem, circle-criterion, kalman-yakubovich-popov-lemma]
see_also: [circle-criterion, lure-problem, kalman-yakubovich-popov-lemma, passivity-theorem, describing-function, nyquist-plot, linear-matrix-inequality, lyapunov-function]
sources:
  - paper: "V. M. Popov, Absolute stability of nonlinear systems of automatic control, Automation and Remote Control 22(8), 857-875, 1961 (translation of Avtomatika i Telemekhanika 22(8), 1961)"
    title: V. M. Popov, Absolute stability of nonlinear systems of automatic control, 1961
    locator: the frequency condition with the multiplier 1 + j omega q for a time-invariant nonlinearity
  - paper: doi:10.1073/pnas.49.2.201
    title: Rudolf E. Kalman, Lyapunov functions for the problem of Lur'e in automatic control, Proceedings of the National Academy of Sciences 49(2), 201-205, 1963
    locator: the Popov condition gives a Lyapunov function of the Lur'e form, a quadratic form plus an integral of the nonlinearity
  - paper: "V. A. Yakubovich, The solution of certain matrix inequalities in automatic control theory, Soviet Mathematics Doklady 3, 620-623, 1962"
    title: V. A. Yakubovich, The solution of certain matrix inequalities in automatic control theory, 1962
    locator: the first proof that the Popov frequency condition gives a Lyapunov function of the Lur'e form
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 7.1 (absolute stability and the Popov criterion)
---

The Popov criterion is a test for the [Lur'e problem](/lure-problem/) when the nonlinearity does not depend on time. It multiplies the frequency response $G(j\omega)$ of the linear part by $1 + j\omega\eta$ for a free number $\eta \ge 0$, and asks that the real part of the product stays above $-1/k$, where $[0, k]$ is the sector. In a picture, the Popov plot of $\operatorname{Re} G(j\omega)$ against $\omega \operatorname{Im} G(j\omega)$ must lie to the right of a line through $-1/k$ with slope $1/\eta$. With $\eta = 0$ it is case 2 of the [circle criterion](/circle-criterion/); the extra freedom of the slope often certifies a much larger sector. The price is that the nonlinearity must be time-invariant, because the Lyapunov function contains the integral of the nonlinearity. V. M. Popov published the test in 1961, and Yakubovich and Kalman gave its Lyapunov proof through the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/).

## Statement

**Setting.** $\dot x = Ax + Bu$, $y = Cx$, $u = -\psi(y)$, with scalar $u$ and $y$ and $G(s) = C(sI - A)^{-1}B$. The matrix $A$ is [Hurwitz](/hurwitz-matrix/), $(A, B)$ is controllable and $(A, C)$ is observable. The nonlinearity $\psi : \mathbb{R} \to \mathbb{R}$ is time-invariant, locally Lipschitz, and in the sector $[0, k]$ with $0 < k < \infty$:

$$0 \ \le\ y\, \psi(y) \ \le\ k y^2 \qquad \text{for all } y.$$

**Theorem (Popov 1961).** Suppose there is $\eta \ge 0$ such that $-1/\eta$ is not an eigenvalue of $A$, and

$$M(s) = 1 + k(1 + \eta s) G(s)$$

is strictly positive real. Then the origin is globally asymptotically stable for every such $\psi$. The frequency form of the condition is

$$\frac{1}{k} + \operatorname{Re}\big[(1 + j\omega\eta) G(j\omega)\big] > 0 \quad \text{for all } \omega \in \mathbb{R}, \qquad 1 + \eta k CB > 0.$$

The second inequality is the value $M(\infty)$, and it holds by itself when $CB = 0$, that is, when $G$ has relative degree at least 2.

## In plain words

A linear system is in a loop with a device whose gain is unknown but fixed in time, and stays between zero and an upper value. The circle criterion asks that the frequency response curve stays to the right of a vertical line set by the upper value. The Popov criterion lets that line tilt. It plots the curve in a slightly changed way, with the vertical part scaled by the frequency, and then any straight line through the same point on the axis may be used. If one tilt works, the loop settles to rest from every start for every such device. The tilt is allowed only because the device does not change with time; for a device that changes, the test can give a wrong answer.

## Proof

**Realization of $M$.** From $sG(s) = CB + CA(sI - A)^{-1}B$,

$$M(s) = (1 + \eta k CB) + k(C + \eta CA)(sI - A)^{-1}B.$$

So $M$ has the realization $(A, B, C_M, D_M)$ with $C_M = k(C + \eta CA)$ and $D_M = 1 + \eta k CB$. It is minimal: $(A, B)$ is controllable, and if $C_M v = 0$ for an eigenvector $Av = \lambda v$, then $k(1 + \eta\lambda)Cv = 0$; since $1 + \eta\lambda \ne 0$, this gives $Cv = 0$, which the observability of $(A, C)$ excludes. This is where $-1/\eta$ must not be an eigenvalue.

**KYP.** By the strict form of the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) (Khalil 2002, Section 6.3), there are $P = P^T > 0$, a matrix $L$, a column $W$ and $\varepsilon > 0$ with

$$PA + A^T P = -L^T L - \varepsilon P, \qquad PB = C_M^T - L^T W, \qquad W^T W = 2 D_M.$$

**Lyapunov function.** Take

$$V(x) = x^T P x + 2\eta k \int_0^{Cx} \psi(\sigma)\, d\sigma.$$

The sector gives $\sigma\psi(\sigma) \ge 0$, so the integral is nonnegative, and $V(x) \ge \lambda_{\min}(P)|x|^2$. So $V$ is positive definite and radially unbounded. Because $\psi$ does not depend on $t$, the derivative of the integral term along solutions is $2\eta k \psi(y)\dot y$, with $\dot y = CAx - CB\psi$. Write $\psi$ for $\psi(y)$. Using $B^T P x = C_M x - W^T L x = k y + \eta k CAx - W^T L x$,

$$\dot V = -\varepsilon x^T P x - |Lx|^2 - 2\psi(ky + \eta k CAx - W^T L x) + 2\eta k\psi(CAx - CB\psi).$$

The terms with $CAx$ cancel, so

$$\dot V = -\varepsilon x^T P x - |Lx|^2 + 2\psi W^T L x - 2k y\psi - 2\eta k CB \psi^2.$$

The sector gives $\psi(\psi - ky) \le 0$, so $-2ky\psi \le -2\psi^2$. Then, with $W^T W = 2(1 + \eta k CB)$,

$$\dot V \ \le\ -\varepsilon x^T P x - |Lx|^2 + 2\psi W^T L x - \psi^2 W^T W = -\varepsilon x^T P x - |Lx - W\psi|^2 \ \le\ -\varepsilon x^T P x.$$

So $\dot V$ is negative definite, and the origin is globally asymptotically stable by the Lyapunov theorem for radially unbounded $V$. Since also $\int_0^y \psi \le k y^2/2$, $V$ is bounded by a quadratic, and the bound is in fact exponential.

**Frequency form.** $M$ has its poles at eigenvalues of the Hurwitz matrix $A$, and $M(\infty) = D_M$. So $M$ is strictly positive real when $\operatorname{Re} M(j\omega) > 0$ for all $\omega$ and $D_M > 0$. Dividing $\operatorname{Re} M(j\omega) > 0$ by $k$ gives the stated inequality.

## Consequences

**The Popov plot.** Let $X(\omega) = \operatorname{Re} G(j\omega)$ and $Y(\omega) = \omega \operatorname{Im} G(j\omega)$. Since $\operatorname{Re}[(1 + j\omega\eta)G] = X - \eta Y$, the condition is $X - \eta Y > -1/k$: the curve $(X(\omega), Y(\omega))$ lies strictly to the right of the line $X - \eta Y = -1/k$, which passes through $(-1/k, 0)$ with slope $1/\eta$. Rule of thumb: draw the Popov plot, and tilt a line through the real axis until it touches the plot from the left; the point where the best line meets the axis gives the largest certified $k$.

**Circle criterion as a special case.** With $\eta = 0$, the condition is $\operatorname{Re} G(j\omega) > -1/k$, which is case 2 of the [circle criterion](/circle-criterion/). So for time-invariant $\psi$ the Popov criterion certifies every sector $[0, k]$ that the circle criterion certifies, and often more.

**Other sectors.** For a sector $[k_1, k_2]$ with $A - k_1 BC$ Hurwitz, the loop transformation $\psi_T = \psi - k_1 y$ and $G_T = G/(1 + k_1 G)$ gives the sector $[0, k_2 - k_1]$. For the sector $[0, \infty)$, the condition becomes that $(1 + \eta s)G(s)$ is strictly positive real (Khalil 2002, Section 7.1).

**Why time-invariance.** For $\psi(t, y)$, the derivative of $\int_0^{y} \psi(t, \sigma)\, d\sigma$ has the extra term $\int_0^{y} \partial_t \psi(t, \sigma)\, d\sigma$, which has no sign. So the proof fails, and the tightness example below shows that the result fails too.

**LMI form.** $C_M$ and $D_M$ are affine in $\eta$, so the KYP condition is one [linear matrix inequality](/linear-matrix-inequality/) in $P$ and $\eta$ together, with $n(n + 1)/2 + 1$ unknowns. A search over $\eta$ is not needed.

**Worked example.** Take $G(s) = 1/(s + 1)^3$, with the realization $A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -1 & -3 & -3 \end{bmatrix}$, $B = [0, 0, 1]^T$, $C = [1, 0, 0]$. Here $CB = 0$, and the only eigenvalue of $A$ is $-1$, so $\eta \ne 1$. With $t = \omega^2$, $G(j\omega) = (1 - j\omega)^3/(1 + t)^3$, so $\operatorname{Re} G = (1 - 3t)/(1 + t)^3$, $\omega\operatorname{Im} G = (t^2 - 3t)/(1 + t)^3$, and

$$f_\eta(t) = \operatorname{Re}\big[(1 + j\omega\eta)G(j\omega)\big] = \frac{1 - 3t + \eta(3t - t^2)}{(1 + t)^3}.$$

- With $\eta = 0$, the minimum of $f_0$ is $-1/4$ at $t = 1$, so $k < 4$, the circle criterion bound.
- With $\eta = 0.9$, the minimum of $f_{0.9}$ is $-0.12578$ at $t = 2.6943$, that is, $\omega = 1.6414$. So the test holds for every $k < 1/0.12578 = 7.9505$. For example, $k = 7$ gives $1/7 = 0.14286 > 0.12578$.
- At $\eta = 1$, $(1 + s)G(s) = 1/(s + 1)^2$ and $f_1(t) = (1 - t)/(1 + t)^2$, with the minimum $-1/8$ at $t = 3$. This value of $\eta$ is excluded, but $\min_t f_\eta$ depends continuously on $\eta$, so $\eta$ close to $1$ certifies every $k < 8$.
- No $\eta$ certifies $k = 8$: at $t = 3$, $f_\eta(3) = (1 - 9 + 0)/64 = -1/8$ for every $\eta$, because $G(j\sqrt 3) = -1/8$ is real. The point $(-1/8, 0)$ is on the Popov plot, and every Popov line through $(-1/k, 0)$ with $k \ge 8$ has it on the wrong side.

The constant gains give the Hurwitz sector $(-1, 8)$, and $\psi = 8y$ gives closed loop poles at $\pm j\sqrt 3$. So for this $G$ the Popov criterion certifies the sectors $[0, k]$ up to the Hurwitz limit, while the circle criterion stops at $4$.

## Tightness

**Time-varying nonlinearities.** Take $\ddot y + 0.2\dot y + \psi = 0$, that is, $G(s) = 1/(s^2 + 0.2s)$, with $\psi$ in the sector $[1, 9]$. After the loop transformation, $\psi_T = \psi - y$ is in $[0, 8]$ and $G_T(s) = 1/(s^2 + 0.2s + 1)$, which has the eigenvalues $-0.1 \pm 0.99499j$ and relative degree 2. With $\eta = 5$,

$$\operatorname{Re}\big[(1 + 5j\omega)G_T(j\omega)\big] = \frac{(1 - t) + 0.2 \cdot 5t}{(1 - t)^2 + 0.04t} = \frac{1}{(1 - t)^2 + 0.04t} > 0,$$

so the Popov test holds for every finite $k$, and every time-invariant $\psi$ in $[1, 9]$ gives a globally asymptotically stable loop. But the time-varying gain that is $1$ while $|y|$ grows and $9$ while $|y|$ shrinks multiplies $|\dot y|$ at each zero of $y$ by $2.45299$ (see the [Lur'e problem](/lure-problem/)). So the theorem is false for time-varying $\psi$, and the hypothesis of time-invariance cannot be dropped.

**The strict inequality.** In the worked example, the Popov test certifies every $k < 8$ but not $k = 8$, and the sector $[0, 8]$ contains $\psi = 8y$, which gives the closed loop poles $\pm j\sqrt 3$. So the strict inequality cannot be relaxed to a non-strict one.

**Only sufficient.** The Popov test is not necessary for absolute stability. Multipliers with more freedom than $1 + j\omega\eta$, such as the Zames-Falb multipliers for slope-restricted nonlinearities, certify sectors that the Popov test does not.

## History

Popov (1961) proved the criterion by a frequency domain argument, without a Lyapunov function, in a paper that answered the problem posed by Lur'e and Postnikov in 1944. The Lur'e school had used Lyapunov functions of the form "quadratic form plus integral of the nonlinearity", and Yakubovich (1962) and Kalman (1963) proved that the Popov condition gives exactly such a function. That proof is the origin of the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/). Khalil (2002, Section 7.1) gives a textbook version of the theorem and its proof.

## References
