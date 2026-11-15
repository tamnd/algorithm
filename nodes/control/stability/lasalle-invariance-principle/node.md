---
tag: RQJJVC
kind: theorem
slug: lasalle-invariance-principle
name: LaSalle's invariance principle
aliases:
- LaSalle's theorem
- Krasovskii-LaSalle principle
area: control/stability
level: core
summary: If V' <= 0 on a compact positively invariant set, every solution that starts there converges to the largest invariant set in {V' = 0}. V need not be positive definite.
prereqs: [lyapunov-direct-method]
see_also: [lyapunov-direct-method, lyapunov-function, positively-invariant-set, barbalat-lemma, asymptotic-stability, region-of-attraction, limit-cycle, poincare-bendixson-theorem]
sources:
  - paper: doi:10.1109/TCT.1960.1086720
    title: J. P. LaSalle, Some extensions of Liapunov's second method, IRE Transactions on Circuit Theory 7(4), 520-527, 1960
    locator: the invariance principle for autonomous systems with a function whose derivative is only negative semidefinite
  - paper: "E. A. Barbashin and N. N. Krasovskii, On global stability of motion, Doklady Akademii Nauk SSSR 86(3), 453-456, 1952 (in Russian)"
    locator: asymptotic stability when no solution other than the equilibrium stays in the set where the derivative vanishes
  - book: "N. N. Krasovskii, Stability of Motion, Stanford University Press, 1963 (translation of the Russian edition of 1959)"
    locator: the theorems on asymptotic stability with a semidefinite derivative
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.2, The Invariance Principle (positive limit sets, the theorem and its corollaries), and Chapter 8 (invariance-like theorems for time-varying systems with Barbalat's lemma)
---

LaSalle's invariance principle extends [Lyapunov's direct method](/lyapunov-direct-method/) to functions whose derivative along the solutions is only nonpositive, not negative. It says that a solution that stays in a compact set where $\dot V \le 0$ must approach the largest set of whole solutions that keep $\dot V = 0$. Often that largest set is the equilibrium alone, and then the principle proves [asymptotic stability](/asymptotic-stability/) with a function, such as the physical energy, that the direct method cannot use. The function $V$ does not need to be positive definite, so the principle also proves convergence to sets that are not points, such as a [limit cycle](/limit-cycle/). It holds for autonomous systems; for time-varying systems one uses [Barbalat's lemma](/barbalat-lemma/).

## Statement

**Setting.** $\dot x = f(x)$, with $f : D \to \mathbb{R}^n$ locally Lipschitz on a domain $D \subseteq \mathbb{R}^n$. For a continuously differentiable $V : D \to \mathbb{R}$, $\dot V(x) = \nabla V(x) \cdot f(x)$. A set $M$ is *invariant* if every solution that starts in $M$ stays in $M$ for all $t \in \mathbb{R}$, forward and backward. It is [positively invariant](/positively-invariant-set/) if this holds for $t \ge 0$. A solution *approaches* $M$ if $\operatorname{dist}(x(t), M) \to 0$ as $t \to \infty$.

**Theorem (LaSalle).** Let $\Omega \subset D$ be compact and positively invariant. Let $V : D \to \mathbb{R}$ be continuously differentiable with $\dot V(x) \le 0$ for all $x \in \Omega$. Let

$$E = \{x \in \Omega : \dot V(x) = 0\} ,$$

and let $M$ be the largest invariant set contained in $E$. Then every solution that starts in $\Omega$ approaches $M$ as $t \to \infty$.

**Corollary (Barbashin and Krasovskii).** Let $f(0) = 0$, and let $V : D \to \mathbb{R}$ be continuously differentiable and positive definite on $D$, with $\dot V \le 0$ on $D$. Let $S = \{x \in D : \dot V(x) = 0\}$. If no solution other than $x(t) \equiv 0$ stays in $S$ for all $t \ge 0$, the origin is asymptotically stable. If in addition $D = \mathbb{R}^n$ and $V$ is radially unbounded, the origin is globally asymptotically stable.

## In plain words

Suppose a quantity never increases along the motion of a system, and the motion stays inside a closed and bounded region. The quantity cannot fall forever, so it settles at some value. Once it has settled, the motion can only be in places where the quantity does not change. But a motion cannot sit in such places unless it can move there for all time while the quantity stays fixed. So one asks: which whole motions keep the quantity fixed? Every motion ends up close to those. Often the only such motion is the rest point, and then every motion goes to the rest point. The quantity does not need to have a minimum at the rest point; it only needs to stop falling in few places.

## Proof

**Positive limit sets.** For a solution $x(t)$ defined for all $t \ge 0$, a point $p$ is a *positive limit point* if $x(t_k) \to p$ for some sequence $t_k \to \infty$. The set $L^+$ of all such points is the positive limit set (the omega-limit set).

*Lemma.* If a solution stays in a compact set $\Omega \subset D$ for all $t \ge 0$, then $L^+$ is nonempty, compact and invariant, and $x(t)$ approaches $L^+$ (Khalil 2002, Section 4.2).

*Proof of the lemma.* The sequence $x(k)$, $k = 1, 2, \dots$, lies in the compact set $\Omega$, so it has a convergent subsequence, and $L^+$ is nonempty. $L^+$ lies in $\Omega$, so it is bounded. It is closed: if $p_j \in L^+$ and $p_j \to p$, choose $t_j > j$ with $|x(t_j) - p_j| < 1/j$; then $x(t_j) \to p$. For invariance, let $p \in L^+$ with $x(t_k) \to p$, and let $\phi(s, p)$ be the solution through $p$. For a fixed $s$, the points $x(t_k + s)$ are defined for large $k$ and lie in $\Omega$, and by continuous dependence on initial conditions $x(t_k + s) = \phi(s, x(t_k)) \to \phi(s, p)$ while $\phi(s, p)$ exists. So $\phi(s, p) \in L^+ \subset \Omega$, and since $\Omega$ is compact, $\phi(\cdot, p)$ exists for all $s \in \mathbb{R}$ and stays in $L^+$. Finally, if $x(t)$ does not approach $L^+$, there are $\varepsilon > 0$ and $t_k \to \infty$ with $\operatorname{dist}(x(t_k), L^+) \ge \varepsilon$. A subsequence of $x(t_k)$ converges, to a point of $L^+$ by definition, which is a contradiction.

**The theorem.** Let $x(0) \in \Omega$. Since $\Omega$ is positively invariant and compact, the solution exists for all $t \ge 0$ and stays in $\Omega$. Since $\dot V \le 0$ on $\Omega$, $t \mapsto V(x(t))$ is nonincreasing, and since $V$ is continuous on the compact $\Omega$, it is bounded below. So $V(x(t)) \to a$ for some number $a$. For $p \in L^+$ with $x(t_k) \to p$, continuity gives $V(p) = a$. So $V = a$ on $L^+$. Since $L^+$ is invariant, a solution that starts in $L^+$ stays in $L^+$, so $V$ is constant along it, and $\dot V = 0$ on $L^+$. Hence $L^+ \subseteq E$. Since $L^+$ is invariant and $M$ is the largest invariant subset of $E$, $L^+ \subseteq M$. By the lemma, $x(t)$ approaches $L^+$, and so it approaches $M$. $\blacksquare$

**The corollary.** By part (a) of the direct method the origin is Lyapunov stable, and the proof there gives a compact positively invariant set $\Omega_\beta = \{x \in \bar B_r : V(x) \le \beta\}$ that contains a ball around $0$. Apply the theorem on $\Omega_\beta$. Let $M$ be the largest invariant set in $E = \Omega_\beta \cap S$. A solution in $M$ stays in $S$ for all $t \ge 0$, so by hypothesis it is $x \equiv 0$, and $M = \{0\}$. So every solution from $\Omega_\beta$ converges to $0$. In the global case, for any $x(0)$ the set $\{x : V(x) \le V(x(0))\}$ is compact and positively invariant because $V$ is radially unbounded, and the same argument applies. $\blacksquare$

## Consequences

**Damped pendulum.** $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - b x_2$ with $b > 0$, and the energy $V = \tfrac12 x_2^2 + 1 - \cos x_1$. Then $\dot V = -b x_2^2$, so $S = \{x_2 = 0\}$. Take $D = \{|x_1| < \pi\} \times \mathbb{R}$. A solution that stays in $S$ has $x_2 \equiv 0$, so $\dot x_2 = -\sin x_1 \equiv 0$, which forces $x_1 \equiv 0$ in $D$. By the corollary the bottom equilibrium is asymptotically stable. Moreover, for $c < 2$ the component $\Omega_c$ of $\{V \le c\}$ around the origin lies in $D$, and it is compact and positively invariant, so every solution from $\Omega_c$ converges to $0$. That gives an estimate of the [region of attraction](/region-of-attraction/). The direct method alone gives only Lyapunov stability here, because $\dot V$ is not negative definite.

**A global example.** $\dot x_1 = x_2$, $\dot x_2 = -x_1 - x_1^3 - x_2$, a spring with a hardening term and linear damping. With $V = \tfrac12 x_1^2 + \tfrac14 x_1^4 + \tfrac12 x_2^2$, which is radially unbounded,

$$\dot V = (x_1 + x_1^3) x_2 + x_2 (-x_1 - x_1^3 - x_2) = -x_2^2 .$$

On $x_2 \equiv 0$, $\dot x_2 = -x_1 - x_1^3 = 0$ forces $x_1 = 0$. So the origin is globally asymptotically stable.

**Convergence to a limit cycle.** For

$$\dot x_1 = -x_2 + x_1 (1 - x_1^2 - x_2^2), \qquad \dot x_2 = x_1 + x_2 (1 - x_1^2 - x_2^2) ,$$

the radius $r = |x|$ satisfies $\dot r = r (1 - r^2)$. Take $V = (1 - |x|^2)^2$, which is not positive definite about any point. Then $\dot V = -4 r^2 (1 - r^2)^2 \le 0$. The annulus $\Omega = \{1/2 \le r \le 2\}$ is compact and positively invariant, since $\dot r > 0$ for $r < 1$ and $\dot r < 0$ for $r > 1$. In $\Omega$, $E$ is the unit circle, which is itself invariant. So $M$ is the unit circle, and every solution from the annulus approaches it. The direct method cannot state this, because its conclusions are about equilibria. In the plane the [Poincaré-Bendixson theorem](/poincare-bendixson-theorem/) gives related results.

**Adaptive control and estimation.** Many adaptive laws give a function $V$ of the tracking error and the parameter error with $\dot V = -e^2 \le 0$. The error converges, but the parameters need not; the invariance principle (for autonomous loops) or Barbalat's lemma (for time-varying ones) proves the first part, and a condition of persistent excitation is needed for the second.
## Tightness

**Compactness cannot be dropped.** On $\mathbb{R}$, take $\dot x = e^{-x}$ and $V(x) = e^{-x}$. Then $\dot V = -e^{-x} e^{-x} = -e^{-2x} < 0$ everywhere, so $E$ and $M$ are empty. The solution $x(t) = \ln(e^{x_0} + t)$ exists for all $t \ge 0$ and goes to infinity; it does not approach $M$, since nothing can approach the empty set. The theorem does not apply because no compact set is positively invariant here. In applications, the compact set usually comes from a sublevel set of a positive definite or radially unbounded $V$, or from a separate proof that the solution is bounded.

**The largest invariant set matters, not $E$.** In the pendulum example $E$ is the whole segment $\{x_2 = 0\}$ in $\Omega_c$, but the solutions converge to the single point $0$. The conclusion with $E$ in place of $M$ is true but weaker. Computing $M$ is the real work of an application: one asks which solutions keep $\dot V \equiv 0$.

**Time-varying systems.** The theorem fails for $\dot x = f(t, x)$, because the positive limit set of a solution of a time-varying system need not be invariant. Example: $\dot x = -x / (1 + t)^2$ and $V = x^2$. Then $\dot V = -2 x^2 / (1 + t)^2 \le 0$, and $\dot V = 0$ only at $x = 0$. But

$$x(t) = x_0 \exp\left(-\int_0^t \frac{ds}{(1 + s)^2}\right) = x_0 \exp\left(-\frac{t}{1 + t}\right) \to x_0 / e ,$$

which is not $0$ for $x_0 \ne 0$. For time-varying systems the substitute is Barbalat's lemma: if $\dot V \le -W(x) \le 0$ and $\dot V$ is uniformly continuous in $t$ along the solution, then $W(x(t)) \to 0$ (Khalil 2002, Chapter 8). In the example the uniform continuity holds, but $\dot V \le -W(x)$ fails for every positive definite $W$ that does not depend on $t$.

**Only nonpositive on $\Omega$.** The sign condition $\dot V \le 0$ is needed only on $\Omega$, not on all of $D$, but $\Omega$ must be positively invariant. Positive invariance is not implied by the sign of $\dot V$ when $\Omega$ is not a sublevel set of $V$, and it must then be proved separately.

## History

Barbashin and Krasovskii (1952) proved asymptotic stability, local and global, from a positive definite function whose derivative is only negative semidefinite, under the condition that no solution other than the equilibrium stays in the set where the derivative vanishes. Krasovskii's book of 1959 (English translation 1963) developed these results further. LaSalle (1960) stated the general principle with positive limit sets, without the condition that $V$ be positive definite, and he and Lefschetz made it widely known in the book Stability by Liapunov's Direct Method (1961). The name Krasovskii-LaSalle principle records both lines of work.

## References
