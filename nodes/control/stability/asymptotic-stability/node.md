---
tag: MRDCBN
kind: definition
slug: asymptotic-stability
name: Asymptotic stability
aliases:
- asymptotically stable equilibrium
area: control/stability
level: core
summary: An equilibrium is asymptotically stable if it is Lyapunov stable and every solution that starts close enough converges to it. Globally, if every solution converges.
prereqs: [lyapunov-stability]
see_also: [lyapunov-stability, exponential-stability, region-of-attraction, hurwitz-matrix, lyapunov-direct-method, lasalle-invariance-principle, converse-lyapunov-theorem, input-to-state-stability]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.1 (the definition of asymptotic stability and global asymptotic stability), Section 4.3 (linear systems), Section 4.4 (class K and class KL functions and the KL form of the definitions) and Section 4.5 (uniform asymptotic stability for time-varying systems)
  - paper: doi:10.1080/00207179208934253
    title: "A. M. Lyapunov, The general problem of the stability of motion, translated by A. T. Fuller, International Journal of Control 55(3), 531-773, 1992"
    locator: asymptotic stability of a motion, as defined and used in the first and second methods
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: Chapter 5, Dynamic Behavior
---

An equilibrium of a differential equation is asymptotically stable when it is [Lyapunov stable](/lyapunov-stability/) and every solution that starts close enough to it converges to it as time goes to infinity. It is globally asymptotically stable when every solution converges. For the linear system $\dot x = A x$ the property is the same as $A$ being a [Hurwitz matrix](/hurwitz-matrix/), and it is then also [exponential stability](/exponential-stability/). For nonlinear systems the two differ: the solutions of $\dot x = -x^3$ converge to $0$ only like $1/\sqrt{2t}$. The set of initial states whose solutions converge is the [region of attraction](/region-of-attraction/).

## Definition

**Setting.** As on [Lyapunov stability](/lyapunov-stability/): $\dot x = f(x)$ with $f : D \to \mathbb{R}^n$ locally Lipschitz on a domain $D$ that contains the origin, $f(0) = 0$, and $|\cdot|$ any norm on $\mathbb{R}^n$.

**Definition.** The equilibrium $x = 0$ is

- *attractive* if there is a $\delta > 0$ such that every solution with $|x(0)| < \delta$ exists for all $t \ge 0$ and $x(t) \to 0$ as $t \to \infty$;
- *asymptotically stable* if it is Lyapunov stable and attractive;
- *globally asymptotically stable* if it is Lyapunov stable and every solution, from every $x(0) \in \mathbb{R}^n$, converges to $0$ (here $D = \mathbb{R}^n$).

Both parts of the definition are needed. Lyapunov stability without attraction is the frictionless pendulum. Attraction without Lyapunov stability also happens; an example is below.

**The class KL form.** A function $\beta : [0, a) \times [0, \infty) \to [0, \infty)$ is of *class KL* if $\beta(\cdot, t)$ is of class K for each fixed $t$, and $\beta(r, \cdot)$ is nonincreasing with $\beta(r, t) \to 0$ as $t \to \infty$ for each fixed $r$ (Khalil 2002, Section 4.4). The origin is asymptotically stable if and only if there are a class KL function $\beta$ and a $c > 0$ such that

$$|x(t)| \le \beta(|x(0)|, t) \quad \text{for all } t \ge 0 \text{ and all } |x(0)| < c .$$

It is globally asymptotically stable if and only if this holds for all $x(0)$, with $\beta$ defined on $[0, \infty) \times [0, \infty)$. The bound $\beta(r, 0)$ is the class K bound of Lyapunov stability, and the decay in $t$ is the attraction. The bound says more than the two parts side by side: the convergence is uniform over the initial states of a ball. For autonomous systems with locally Lipschitz $f$ the two forms are equivalent (Khalil 2002, Section 4.4). Exponential stability is the special case $\beta(r, t) = k r e^{-\lambda t}$.

**Linear systems.** For $\dot x = A x$ these four statements are equivalent: the origin is asymptotically stable; it is globally asymptotically stable; it is exponentially stable; every eigenvalue of $A$ has negative real part.

Proof. If the origin is attractive, $e^{At} x_0 \to 0$ for every $x_0$ in a ball, and by linearity for every $x_0 \in \mathbb{R}^n$. If $A v = \lambda v$ with $v \ne 0$ and $\operatorname{Re} \lambda \ge 0$, the real part of $e^{\lambda t} v$ is a solution of $\dot x = A x$ (for real $\lambda$ take $v$ real), and $|e^{\lambda t}| = e^{t \operatorname{Re} \lambda} \ge 1$, so the solution from $\operatorname{Re} v$ or from $\operatorname{Im} v$ does not go to $0$. So attraction forces $\operatorname{Re} \lambda < 0$ for all eigenvalues. Conversely, if $A$ is Hurwitz, there are $k \ge 1$ and $\lambda > 0$ with $\|e^{At}\| \le k e^{-\lambda t}$ (see [Hurwitz matrix](/hurwitz-matrix/)), which is global exponential stability, and that implies the rest.

**Time-varying systems.** For $\dot x = f(t, x)$ the equilibrium is *uniformly asymptotically stable* if the bound $|x(t)| \le \beta(|x(t_0)|, t - t_0)$ holds with one class KL function for all initial times $t_0 \ge 0$ (Khalil 2002, Section 4.5). Convergence for each $t_0$ separately is weaker, and it does not survive perturbations in general. For autonomous systems the two agree.

## Examples and non-examples

- **Linear first order.** $\dot x = -a x$ with $a > 0$ has $x(t) = e^{-at} x(0)$: globally asymptotically stable, with $\beta(r, t) = r e^{-at}$.
- **Asymptotically but not exponentially stable.** $\dot x = -x^3$ has the solution
  $$x(t) = \frac{x_0}{\sqrt{1 + 2 x_0^2 t}} .$$
  So $|x(t)| \le |x_0|$, and $x(t) \to 0$ for every $x_0$: the origin is globally asymptotically stable with the class KL function $\beta(r, t) = r / \sqrt{1 + 2 r^2 t}$. For large $t$, $|x(t)| \approx 1 / \sqrt{2t}$ whatever $x_0 \ne 0$ is. No bound $k e^{-\lambda t} |x_0|$ can hold, because $e^{\lambda t} / \sqrt{2t} \to \infty$. From $x_0 = 1$, the state is $1/\sqrt{3} = 0.57735$ at $t = 1$, $1/\sqrt{21} = 0.21822$ at $t = 10$ and $1/\sqrt{201} = 0.07053$ at $t = 100$: a factor 10 in time gains only about a factor 3.
- **Local, not global.** $\dot x = -x + x^2$ has the equilibria $0$ and $1$. Its solution is
  $$x(t) = \frac{x_0 e^{-t}}{1 - x_0 + x_0 e^{-t}} .$$
  For $x_0 < 1$ the denominator stays positive and $x(t) \to 0$. For $x_0 > 1$ the solution escapes to infinity at the finite time $t = \ln(x_0 / (x_0 - 1))$, for example at $t = \ln 2 = 0.69315$ from $x_0 = 2$. The origin is asymptotically stable and not globally, and its region of attraction is the interval $(-\infty, 1)$.
- **Damped pendulum.** $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - b x_2$ with $b > 0$. The bottom equilibrium is asymptotically stable. With $b = 1$ the Jacobian there has the eigenvalues $(-1 \pm i\sqrt{3})/2$, so the [indirect method](/lyapunov-indirect-method/) applies. It is not globally asymptotically stable, because the other equilibria $(k\pi, 0)$ do not move. The proof by the energy uses the [invariance principle](/lasalle-invariance-principle/), since the energy decreases only where $x_2 \ne 0$.
- **Attractive but not Lyapunov stable (non-example).** In polar coordinates, $\dot r = r(1 - r)$ and $\dot \theta = \sin^2(\theta / 2)$. Every solution with $r(0) > 0$ converges to the equilibrium $(r, \theta) = (1, 0)$, so that equilibrium is attractive with $\delta = 1$. A solution that starts on the unit circle at a small angle $\theta_0 > 0$ goes once around the circle first, and passes the point at distance 2 from the equilibrium. So the equilibrium is not Lyapunov stable, and not asymptotically stable.
- **Linear with an eigenvalue on the axis (non-example).** $A = \operatorname{diag}(-1, 0)$: the origin is Lyapunov stable, but the solution from $(0, 1)$ stays at $(0, 1)$. Not attractive.

## Related definitions

- [Lyapunov stability](/lyapunov-stability/): the first half of the definition.
- [Exponential stability](/exponential-stability/): asymptotic stability with an exponential rate.
- [Region of attraction](/region-of-attraction/): the set of all initial states whose solutions converge to the equilibrium. It is open and invariant.
- [Hurwitz matrix](/hurwitz-matrix/): the matrix condition for $\dot x = A x$; tested by the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) on the characteristic polynomial.
- [Lyapunov's direct method](/lyapunov-direct-method/) proves asymptotic stability with a function whose derivative is negative definite. The [invariance principle](/lasalle-invariance-principle/) needs only a negative semidefinite derivative. The [converse Lyapunov theorem](/converse-lyapunov-theorem/) says that a Lyapunov function exists for every asymptotically stable equilibrium.
- *Finite-time stability*: solutions reach the equilibrium in finite time. It needs a right-hand side that is not Lipschitz at the origin, for example $\dot x = -\operatorname{sign}(x) |x|^{1/2}$.
- [Input-to-state stability](/input-to-state-stability/): the class KL bound plus a class K gain of the input.
- *Schur stability* is the discrete-time analogue for $x_{k+1} = A x_k$: every eigenvalue inside the unit disc; see [Jury stability test](/jury-stability-test/).

## References
