---
tag: NFWQWZ
kind: definition
slug: lyapunov-stability
name: Lyapunov stability
aliases:
- stability in the sense of Lyapunov
area: control/stability
level: core
summary: An equilibrium is Lyapunov stable if solutions that start near it stay near it for all future time. It is the weakest of the Lyapunov notions and does not ask that solutions converge.
prereqs: [equilibrium-point, ode-initial-value-problem, lipschitz-condition]
see_also: [asymptotic-stability, exponential-stability, lyapunov-function, lyapunov-direct-method, hurwitz-matrix, bibo-stability, input-to-state-stability, jordan-normal-form]
sources:
  - paper: doi:10.1080/00207179208934253
    title: "A. M. Lyapunov, The general problem of the stability of motion, translated by A. T. Fuller, International Journal of Control 55(3), 531-773, 1992"
    locator: the definition of stability of a motion and the first and second methods (the Russian original is the Kharkov thesis of 1892)
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.1 (autonomous systems, the definitions of stable, unstable and asymptotically stable), Section 4.3 (linear systems) and Section 4.4 (the class K form of the definitions)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: Chapter 5, Dynamic Behavior (stability of equilibrium points)
---

Lyapunov stability is a property of an equilibrium of a differential equation: every solution that starts close enough to the equilibrium stays close to it for all future time. It does not ask the solutions to approach the equilibrium; that stronger property is [asymptotic stability](/asymptotic-stability/), and a rate for it gives [exponential stability](/exponential-stability/). The definition is about one equilibrium and one initial condition at a time, so it differs from [BIBO stability](/bibo-stability/), which is about the input-output map of a linear system, and from [input-to-state stability](/input-to-state-stability/), which adds an input. The usual way to prove it is a [Lyapunov function](/lyapunov-function/) and the [direct method](/lyapunov-direct-method/).

## Definition

**Setting.** Consider the autonomous system

$$\dot x = f(x), \qquad x(t) \in \mathbb{R}^n,$$

where $f : D \to \mathbb{R}^n$ is locally Lipschitz on a domain $D \subseteq \mathbb{R}^n$ that contains the origin (see [Lipschitz condition](/lipschitz-condition/)). By the [Picard-Lindelöf theorem](/picard-lindelof-theorem/), each initial state $x(0) = x_0 \in D$ gives a unique solution $x(t)$ on a maximal interval. The origin is an [equilibrium point](/equilibrium-point/): $f(0) = 0$. An equilibrium $x^*$ at another place is moved to the origin by the change of variables $y = x - x^*$. The norm $|\cdot|$ is any norm on $\mathbb{R}^n$. All norms on $\mathbb{R}^n$ are equivalent, so the definition does not depend on the choice.

**Definition.** The equilibrium $x = 0$ is *Lyapunov stable* (or *stable in the sense of Lyapunov*) if for each $\varepsilon > 0$ there is a $\delta = \delta(\varepsilon) > 0$ such that

$$|x(0)| < \delta \implies |x(t)| < \varepsilon \quad \text{for all } t \ge 0 .$$

It is *unstable* if it is not Lyapunov stable: there is an $\varepsilon > 0$ such that for every $\delta > 0$ some solution with $|x(0)| < \delta$ reaches $|x(t)| \ge \varepsilon$ at some time $t \ge 0$.

The definition contains an existence statement. A solution that stays in the closed ball of radius $\varepsilon$ (inside $D$) stays in a compact set, so it cannot escape in finite time, and it exists for all $t \ge 0$.

**The class K form.** A function $\alpha : [0, a) \to [0, \infty)$ is of *class K* if it is continuous, strictly increasing and $\alpha(0) = 0$ (Khalil 2002, Section 4.4). The origin is Lyapunov stable if and only if there are a class K function $\alpha$ and a $c > 0$ such that

$$|x(t)| \le \alpha(|x(0)|) \quad \text{for all } t \ge 0 \text{ and all } |x(0)| < c .$$

For the "if" part, let $\varepsilon > 0$. Because $\alpha$ is continuous with $\alpha(0) = 0$, there is a $\delta \in (0, c]$ with $\alpha(\delta) < \varepsilon$. Then $|x(0)| < \delta$ gives $|x(t)| \le \alpha(|x(0)|) < \alpha(\delta) < \varepsilon$, because $\alpha$ is strictly increasing. For the "only if" part, let $\delta^*(\varepsilon)$ be the supremum of the $\delta \le \varepsilon$ that the definition admits. It is positive and nondecreasing in $\varepsilon$, a class K function lies below it, and the inverse of that function is an $\alpha$ that works (Khalil 2002, Section 4.4).

**Linear systems.** For $\dot x = A x$ the solution is $x(t) = e^{At} x(0)$, and the origin is Lyapunov stable if and only if $\sup_{t \ge 0} \|e^{At}\| < \infty$ in an induced [matrix norm](/matrix-norms/). In terms of eigenvalues, this holds if and only if every eigenvalue $\lambda$ of $A$ has $\operatorname{Re} \lambda \le 0$, and every eigenvalue with $\operatorname{Re} \lambda = 0$ is semisimple: its Jordan blocks have size 1 (Khalil 2002, Section 4.3). The reason is the [Jordan normal form](/jordan-normal-form/): a Jordan block of size $k$ at $\lambda$ gives entries $t^j e^{\lambda t} / j!$ with $j < k$ in $e^{At}$, and these are bounded on $t \ge 0$ exactly when $\operatorname{Re} \lambda < 0$, or $\operatorname{Re} \lambda = 0$ and $k = 1$. For a linear system the property is global: if it holds near the origin, it holds for all initial states, by scaling.

**Time-varying systems.** For $\dot x = f(t, x)$ with $f(t, 0) = 0$, the definition is stated for each initial time $t_0$, with $\delta = \delta(\varepsilon, t_0)$. The equilibrium is *uniformly stable* if $\delta$ can be chosen independent of $t_0$ (Khalil 2002, Section 4.5). For autonomous systems the two notions agree, because a solution started at $t_0$ is a time shift of one started at $0$.

## Examples and non-examples

- **Harmonic oscillator.** $\dot x_1 = x_2$, $\dot x_2 = -x_1$. Solutions move on circles: $x_1^2 + x_2^2$ is constant. With the Euclidean norm, $\delta = \varepsilon$ works. The origin is Lyapunov stable, and no solution other than the equilibrium approaches it, so it is not asymptotically stable. Here $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$ has the simple eigenvalues $\pm i$, in line with the eigenvalue test.
- **Pendulum without friction.** $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1$, where $x_1$ is the angle from the bottom. The energy $E = \tfrac12 x_2^2 + 1 - \cos x_1$ is constant along solutions and has a strict local minimum at the bottom, so the bottom equilibrium is Lyapunov stable (this is the [direct method](/lyapunov-direct-method/) with $V = E$). The top equilibrium $(\pi, 0)$ is unstable.
- **Double integrator (non-example).** $\dot x_1 = x_2$, $\dot x_2 = 0$ gives $x_1(t) = x_1(0) + x_2(0) t$. For every $\delta > 0$ the initial state $(0, \delta/2)$ leaves every ball. The origin is unstable, although both eigenvalues are $0$ and so have real part $0$. The eigenvalue $0$ has one Jordan block of size 2, which the linear test rejects.
- **A solution that blows up (non-example).** $\dot x = x^2$ has $x(t) = x_0 / (1 - x_0 t)$. Every solution with $x_0 < 0$ goes to $0$, but every solution with $x_0 > 0$ escapes to infinity at $t = 1 / x_0$. The origin is unstable. Convergence from one side does not help.
- **Convergence without stability (non-example).** In polar coordinates, take $\dot r = r(1 - r)$ and $\dot \theta = \sin^2(\theta / 2)$. The point $(r, \theta) = (1, 0)$ is an equilibrium, and every solution with $r(0) > 0$ converges to it. But a solution that starts on the unit circle at a small angle $\theta_0 > 0$ goes once around the circle before it comes back, so it reaches the point $(-1, 0)$ at distance 2. The equilibrium is attractive but unstable. This is why the definition of asymptotic stability asks for Lyapunov stability as well as convergence.
- **Linearization.** If the Jacobian at $0$ has an eigenvalue with positive real part, the origin is unstable; this is the instability half of the [indirect method](/lyapunov-indirect-method/). The converse fails: $\dot x = x^3$ is unstable and $\dot x = -x^3$ is asymptotically stable, while both have the Jacobian $0$.

## Related definitions

- [Asymptotic stability](/asymptotic-stability/): Lyapunov stable, and nearby solutions converge to the equilibrium.
- [Exponential stability](/exponential-stability/): nearby solutions converge at least as fast as $k e^{-\lambda t} |x(0)|$.
- [Lyapunov function](/lyapunov-function/): a positive definite function that does not increase along solutions; its existence near the origin is sufficient for Lyapunov stability by the [direct method](/lyapunov-direct-method/). The [converse Lyapunov theorem](/converse-lyapunov-theorem/) gives the other direction under conditions.
- [Hurwitz matrix](/hurwitz-matrix/): a matrix whose eigenvalues all have negative real part; for $\dot x = A x$ this is asymptotic stability.
- [Positively invariant set](/positively-invariant-set/): a set that no solution leaves. A Lyapunov stable equilibrium has arbitrarily small positively invariant neighborhoods: for a given $\varepsilon$, the union of the forward orbits that start in the ball of radius $\delta(\varepsilon)$ is one.
- *Lagrange stability*: every solution is bounded. It is a property of the whole system, not of one equilibrium, and it neither implies nor follows from Lyapunov stability of a given equilibrium.
- *Orbital stability*: the same idea for a periodic orbit, with the distance to the orbit in place of the distance to a point; see [limit cycle](/limit-cycle/).
- [BIBO stability](/bibo-stability/) and [input-to-state stability](/input-to-state-stability/): notions for systems with an input.

## References
