---
tag: PYFE77
kind: theorem
slug: lyapunov-direct-method
name: Lyapunov's direct method
aliases:
- Lyapunov's second method
- Lyapunov stability theorem
area: control/stability
level: core
summary: If a positive definite V has a derivative along solutions that is at most 0, the equilibrium is Lyapunov stable; if it is negative definite, asymptotically stable; global needs V radially unbounded.
prereqs: [lyapunov-function, asymptotic-stability]
see_also: [lyapunov-function, lasalle-invariance-principle, lyapunov-indirect-method, lyapunov-theorem-for-linear-systems, converse-lyapunov-theorem, region-of-attraction, control-lyapunov-function, barbalat-lemma]
sources:
  - paper: doi:10.1080/00207179208934253
    title: "A. M. Lyapunov, The general problem of the stability of motion, translated by A. T. Fuller, International Journal of Control 55(3), 531-773, 1992"
    locator: the second method and its theorems on stability, asymptotic stability and instability (the Russian original was published at Kharkov in 1892)
  - paper: "E. A. Barbashin and N. N. Krasovskii, On global stability of motion, Doklady Akademii Nauk SSSR 86(3), 453-456, 1952 (in Russian)"
    locator: the global theorem with a radially unbounded function
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.1 (the theorems for autonomous systems, the proof by level sets, global asymptotic stability, the instability theorem of Chetaev) and Section 4.5 (time-varying systems); the counterexample without radial unboundedness is in Chapter 4
---

Lyapunov's direct method proves that an equilibrium of a differential equation is stable without solving the equation. One looks for a [Lyapunov function](/lyapunov-function/) $V$: zero at the equilibrium, positive elsewhere, and with a derivative along the solutions that is never positive. Then the equilibrium is [Lyapunov stable](/lyapunov-stability/). If the derivative is negative away from the equilibrium, it is [asymptotically stable](/asymptotic-stability/), and if in addition $V$ grows to infinity in every direction, it is globally asymptotically stable. The last condition cannot be dropped; a counterexample is below. The method is sufficient only: a function that fails proves nothing. Its companion, [Lyapunov's indirect method](/lyapunov-indirect-method/), decides stability from the linearization.

## Statement

**Setting.** $\dot x = f(x)$, where $f : D \to \mathbb{R}^n$ is locally Lipschitz on a domain $D \subseteq \mathbb{R}^n$ that contains the origin, and $f(0) = 0$ (see [Lipschitz condition](/lipschitz-condition/) and [Picard-Lindelöf theorem](/picard-lindelof-theorem/)). For a continuously differentiable $V : D \to \mathbb{R}$, $\dot V(x) = \nabla V(x) \cdot f(x)$. The norm $|\cdot|$ is any norm on $\mathbb{R}^n$.

**Theorem 1 (Lyapunov).** Let $V : D \to \mathbb{R}$ be continuously differentiable with $V(0) = 0$ and $V(x) > 0$ for $x \in D \setminus \{0\}$.

(a) If $\dot V(x) \le 0$ for all $x \in D$, the origin is Lyapunov stable.

(b) If $\dot V(x) < 0$ for all $x \in D \setminus \{0\}$, the origin is asymptotically stable.

**Theorem 2 (Barbashin and Krasovskii).** Let $D = \mathbb{R}^n$, and let $V : \mathbb{R}^n \to \mathbb{R}$ be continuously differentiable with $V(0) = 0$, $V(x) > 0$ for $x \ne 0$, $\dot V(x) < 0$ for $x \ne 0$, and $V(x) \to \infty$ as $|x| \to \infty$ (radially unbounded). Then the origin is globally asymptotically stable.

## In plain words

Think of a bowl with the equilibrium at the bottom, and of a ball that moves on the inside of the bowl. If the ball can never climb, a ball that starts low stays low, so it stays near the bottom. That is stability. If the ball always loses height while it is away from the bottom, it cannot stop at any height above the bottom, so it slides all the way down. That is convergence. For a ball that starts anywhere, one more thing is needed: the walls of the bowl must rise without limit. If the walls flatten out at some height, a ball that starts high can roll away to infinity while it keeps losing height. The bowl is the function, and the ball is the solution. Nobody needs to compute the motion; it is enough to check how the height changes at each point.

## Proof

**Part (a).** Let $\varepsilon > 0$. Choose $r \in (0, \varepsilon]$ such that the closed ball $\bar B_r = \{|x| \le r\}$ lies in $D$. The sphere $\{|x| = r\}$ is compact and $V > 0$ on it, so $a = \min_{|x| = r} V(x) > 0$. Take $\beta \in (0, a)$ and

$$\Omega_\beta = \{x \in \bar B_r : V(x) \le \beta\} .$$

No point of $\Omega_\beta$ lies on the sphere, because $V \ge a > \beta$ there. Let $x(0) \in \Omega_\beta$. As long as the solution stays in $\bar B_r$, $\frac{d}{dt} V(x(t)) = \dot V(x(t)) \le 0$, so $V(x(t)) \le V(x(0)) \le \beta$. To leave $\bar B_r$ the solution would have to cross the sphere, where $V > \beta$; so it never leaves, and it stays in $\Omega_\beta$. The set $\Omega_\beta$ is closed and bounded, so the solution cannot escape in finite time, and it exists for all $t \ge 0$. Finally, $V$ is continuous with $V(0) = 0$, so there is a $\delta > 0$ with $V(x) < \beta$ for $|x| < \delta$. Then $B_\delta \subseteq \Omega_\beta \subseteq \bar B_r$, and $|x(0)| < \delta$ gives $|x(t)| \le r \le \varepsilon$ for all $t \ge 0$. (Using $r$ slightly less than $\varepsilon$ gives the strict inequality of the definition.)

**Part (b).** Stability holds by part (a). Keep $r$, $\beta$ and $\delta$ from part (a), and let $|x(0)| < \delta$. The function $t \mapsto V(x(t))$ is nonincreasing and bounded below by $0$, so it has a limit $c \ge 0$. Suppose $c > 0$. By continuity of $V$ at $0$ there is $d \in (0, r)$ with $V(x) < c$ for $|x| < d$. Since $V(x(t)) \ge c$ for all $t$, the solution stays in the compact annulus $K = \{d \le |x| \le r\}$. On $K$ the continuous function $\dot V$ is negative, so it has a maximum $-\gamma < 0$. Then

$$V(x(t)) = V(x(0)) + \int_0^t \dot V(x(s))\, ds \le V(x(0)) - \gamma t ,$$

which is negative for large $t$, a contradiction. So $V(x(t)) \to 0$. Now suppose $x(t)$ does not go to $0$: there are $\eta \in (0, r)$ and times $t_k \to \infty$ with $|x(t_k)| \ge \eta$. Then $V(x(t_k)) \ge \min_{\eta \le |x| \le r} V(x) > 0$ for all $k$, which contradicts $V(x(t)) \to 0$. So $x(t) \to 0$, and the origin is asymptotically stable.

**Theorem 2.** Stability holds by part (a). Let $x(0) \in \mathbb{R}^n$ and $c = V(x(0))$. Because $V$ is radially unbounded, there is an $R$ with $V(x) > c$ for $|x| > R$. So the set $\Omega = \{x : V(x) \le c\}$ is closed and bounded, and it is positively invariant because $V(x(t))$ does not increase. The solution exists for all $t \ge 0$ and stays in $\Omega$. Repeat the argument of part (b) with the compact set $\Omega$ in place of $\bar B_r$: $V(x(t))$ has a limit $c' \ge 0$; if $c' > 0$ the solution stays in the compact set $\{x \in \Omega : V(x) \ge c'\}$, which does not contain $0$, where $\dot V \le -\gamma < 0$, a contradiction; so $V(x(t)) \to 0$ and $x(t) \to 0$. $\blacksquare$

The proof is the one of Khalil (2002, Section 4.1). It uses only the continuity of $V$ and $\dot V$ and the existence and uniqueness of solutions.

## Consequences

**Examples with numbers.**

- $\dot x = -x^3$ with $V = x^2/2$: $\dot V = -x^4 < 0$ for $x \ne 0$, and $V$ is radially unbounded, so the origin is globally asymptotically stable. The linearization is $\dot x = 0$, about which the [indirect method](/lyapunov-indirect-method/) says nothing.
- $\dot x_1 = -x_1^3 + x_2$, $\dot x_2 = -x_1 - x_2^3$ with $V = x_1^2 + x_2^2$:
  $$\dot V = 2 x_1 (-x_1^3 + x_2) + 2 x_2 (-x_1 - x_2^3) = -2 x_1^4 - 2 x_2^4 ,$$
  which is negative for $x \ne 0$. By Theorem 2 the origin is globally asymptotically stable. The Jacobian at $0$ is $\begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, with eigenvalues $\pm i$, so the linearization does not decide.
- Damped pendulum $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - b x_2$, $b > 0$, with the energy $V = \tfrac12 x_2^2 + 1 - \cos x_1$: $\dot V = -b x_2^2 \le 0$. Part (a) gives Lyapunov stability. Part (b) does not apply, because $\dot V = 0$ on the line $x_2 = 0$. The [invariance principle](/lasalle-invariance-principle/) closes the gap and gives asymptotic stability.
- Linear systems: for $\dot x = A x$ and $V = x^T P x$ with $A^T P + P A = -Q$, $P > 0$, $Q > 0$, the function is radially unbounded and $\dot V = -x^T Q x$, so Theorem 2 applies. For the check matrix $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $Q = I$, $P = \begin{bmatrix} 5/4 & 1/4 \\ 1/4 & 1/4 \end{bmatrix}$. See [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/).

**Estimates of the region of attraction.** The proof shows more than the theorem says. In part (b), every set $\Omega_\beta$ with $\beta < \min_{|x| = r} V$ lies in the [region of attraction](/region-of-attraction/). More generally, if a bounded component of $\{V \le c\}$ that contains the origin lies in the set where $\dot V < 0$ (except at $0$), it is an inner estimate. This is the basis of [region of attraction estimation](/region-of-attraction-estimation/).

**Instability.** A theorem of Chetaev gives the other direction: if there is a continuously differentiable $V$ with $V(0) = 0$, with points $x$ arbitrarily close to $0$ where $V(x) > 0$, and with $\dot V > 0$ on the set $\{x \in B_r : V(x) > 0\}$, then the origin is unstable (Khalil 2002, Section 4.1). The [indirect method](/lyapunov-indirect-method/) page uses it.

**Time-varying systems.** For $\dot x = f(t, x)$ the theorem holds with uniform notions when $V(t, x)$ is bounded between two positive definite functions of $x$ alone, $W_1(x) \le V(t, x) \le W_2(x)$, and $\dot V = \partial V / \partial t + \nabla_x V \cdot f(t, x) \le -W_3(x)$ (Khalil 2002, Section 4.5). The upper bound $W_2$ is what makes the result uniform in the initial time. When only $\dot V \le 0$ is known, [Barbalat's lemma](/barbalat-lemma/) often replaces the invariance principle.

**What the method does not say.** A $V$ that fails the conditions proves nothing: for $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, the function $|x|^2$ has $\dot V > 0$ at some points, although the origin is globally exponentially stable. The [converse Lyapunov theorem](/converse-lyapunov-theorem/) says that for an asymptotically stable equilibrium a strict Lyapunov function always exists, so the method loses no generality in principle; the difficulty is to find one. For [control Lyapunov functions](/control-lyapunov-function/) the same idea becomes a design method.

## Tightness

**Semidefinite derivative does not give convergence.** For the harmonic oscillator $\dot x_1 = x_2$, $\dot x_2 = -x_1$ and $V = x_1^2 + x_2^2$, $\dot V = 0$. Part (a) applies, and the origin is Lyapunov stable but not asymptotically stable, since every solution stays on its circle. So part (b) needs the strict inequality, or an extra argument such as the invariance principle.

**Radial unboundedness cannot be dropped.** Let $u = 1 + x_1^2$ and

$$\dot x_1 = -\frac{6 x_1}{u^2} + 2 x_2, \qquad \dot x_2 = -\frac{2 (x_1 + x_2)}{u^2}, \qquad V(x) = \frac{x_1^2}{u} + x_2^2 .$$

Then $\partial V / \partial x_1 = 2 x_1 / u^2$ and

$$\dot V = \frac{2 x_1}{u^2}\left(-\frac{6 x_1}{u^2} + 2 x_2\right) + 2 x_2 \left(-\frac{2 (x_1 + x_2)}{u^2}\right) = -\frac{12 x_1^2}{u^4} - \frac{4 x_2^2}{u^2} ,$$

which is negative for $x \ne 0$. So Theorem 1(b) holds: the origin is asymptotically stable. But $V < 1 + x_2^2$, so $V$ is not radially unbounded, and the origin is not globally asymptotically stable. To see this, take the region $G = \{x_1 > \sqrt 2,\ x_2 > 2 / (x_1 - \sqrt 2)\}$, bounded by a branch of a hyperbola. On the boundary curve $x_2 = 2/w$ with $w = x_1 - \sqrt 2 > 0$, let $h(x) = x_2 - 2/(x_1 - \sqrt 2)$. A direct computation gives

$$w^3 u^2\, \dot h = 6 w^4 + 30 \sqrt 2\, w^3 + 96 w^2 + 84 \sqrt 2\, w + 72 > 0 .$$

So $h$ increases on the curve, and no solution can leave $G$ through it. A solution that starts in $G$, for example from $(2, 5)$, keeps $x_1 > \sqrt 2 = 1.41421$ for all time and never converges to the origin. This system is the standard counterexample (Khalil 2002, Chapter 4).

**The conditions are on all of $D$.** Theorem 1 needs $\dot V \le 0$ on a whole neighborhood of the origin. A sign condition only on a curve or a sequence of points that approaches the origin does not suffice.

## History

Lyapunov developed the method in his doctoral thesis, The general problem of the stability of motion, published at Kharkov in 1892, as the "second method", next to the first method of series expansions. A French translation appeared in 1907, and Fuller's English translation in 1992. Chetaev added the instability theorem in the 1930s. Barbashin and Krasovskii (1952) gave the global theorem with a radially unbounded function and the version with a semidefinite derivative that LaSalle (1960) extended to the [invariance principle](/lasalle-invariance-principle/). Massera, Kurzweil and others proved converse theorems in the 1950s, which showed that the method is in principle complete for asymptotic stability.

## References
