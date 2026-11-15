---
tag: 9JA2MM
kind: theorem
slug: pontryagin-maximum-principle
name: Pontryagin maximum principle
aliases:
- Pontryagin's minimum principle
- PMP
area: control/optimal-and-predictive-control
level: core
summary: An optimal control minimizes the Hamiltonian at each time, along state and costate trajectories that satisfy the canonical equations. It is a necessary condition, not a sufficient one.
prereqs: [control-hamiltonian, costate, euler-lagrange-equation]
see_also: [transversality-conditions, hamilton-jacobi-bellman-equation, bang-bang-control, singular-arc, indirect-method-optimal-control, time-optimal-control, lqr-problem, kkt-conditions]
sources:
  - paper: "L. S. Pontryagin, V. G. Boltyanskii, R. V. Gamkrelidze and E. F. Mishchenko, The Mathematical Theory of Optimal Processes, translated by K. N. Trirogoff, edited by L. W. Neustadt, Interscience, 1962 (Russian edition 1961)"
    locator: Chapter 1 (the statement of the maximum principle) and Chapter 2 (its proof)
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 4.1 (statement), Section 4.2 (proof, with the temporal and spatial perturbations, the terminal cone, the adjoint equation, the properties of the Hamiltonian and the transversality condition) and Section 4.3 (discussion)
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Section 5.3 (Pontryagin's minimum principle and state inequality constraints)
  - url: https://math.berkeley.edu/~evans/control.course.pdf
    title: Lawrence C. Evans, An Introduction to Mathematical Optimal Control Theory, lecture notes, University of California, Berkeley
    locator: Chapter 4 (the Pontryagin maximum principle) and the appendix (proofs of the maximum principle)
---

The Pontryagin maximum principle (PMP) is the main necessary condition for optimality in an [optimal control problem](/optimal-control-problem/). If an input $u^*$ is optimal, then there is a [costate](/costate/) $\lambda(t)$ such that at almost every time $u^*(t)$ minimizes the [Hamiltonian](/control-hamiltonian/) $H = \lambda_0 L(x, u) + \lambda^T f(x, u)$ over all allowed inputs, while $x$ and $\lambda$ follow the canonical equations with end conditions. It extends the [Euler-Lagrange equation](/euler-lagrange-equation/) to inputs that take values in a closed or even a discrete set, where setting a derivative to zero does not work. It gives necessary conditions only.

**Sign convention.** Pontryagin, Boltyanskii, Gamkrelidze and Mishchenko (1962) state the result as a maximum principle: they use the function $\psi^T f + \psi_0 L$ with a constant $\psi_0 \le 0$, and the optimal input maximizes it. With $\psi = -\lambda$ and $\psi_0 = -\lambda_0$ their function is $-H$, so maximizing it is minimizing $H$. Liberzon (2012) uses the same maximum form. This page and the other pages of this area use the minimum form with $H$ and $\lambda_0 \in \{0, 1\}$, as Kirk (1970) does.

## Statement

**Problem.** Minimize $J(u) = \int_{t_0}^{t_f} L(x, u)\, dt + K(x(t_f))$ subject to $\dot x = f(x, u)$, $x(t_0) = x_0$, $u(t) \in U$ and $x(t_f) \in S$, with $t_f$ fixed or free. Here $U \subseteq \mathbb{R}^m$ is any set. The functions $f : \mathbb{R}^n \times U \to \mathbb{R}^n$ and $L$ are continuous, and their derivatives $f_x$ and $L_x$ exist and are continuous on $\mathbb{R}^n \times U$. $K$ is $C^1$. The target is $S = \mathbb{R}^n$, or a point, or $S = \{x : \psi(x) = 0\}$ for a $C^1$ map $\psi : \mathbb{R}^n \to \mathbb{R}^k$ whose Jacobian has rank $k$ on $S$. Admissible inputs are piecewise continuous. The [Lipschitz condition](/lipschitz-condition/) that follows from $f_x$ being continuous gives unique trajectories by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/).

**Theorem.** Let $u^*$ be an optimal input on $[t_0, t_f^*]$ with trajectory $x^*$. Then there are a number $\lambda_0 \in \{0, 1\}$ and a continuous, piecewise $C^1$ function $\lambda : [t_0, t_f^*] \to \mathbb{R}^n$ with $(\lambda_0, \lambda(t)) \ne (0, 0)$ for all $t$, such that:

1. **Canonical equations.** $\dot x^* = H_\lambda^T = f(x^*, u^*)$ and $\dot\lambda = -H_x^T$, evaluated at $(x^*(t), u^*(t), \lambda(t), \lambda_0)$.
2. **Minimum condition.** At every $t$ where $u^*$ is continuous,
$$H(x^*(t), u^*(t), \lambda(t), \lambda_0) = \min_{v \in U} H(x^*(t), v, \lambda(t), \lambda_0).$$
3. **Constant Hamiltonian.** $t \mapsto H(x^*(t), u^*(t), \lambda(t), \lambda_0)$ is constant. If $t_f$ is free, the constant is 0.
4. **Transversality.** $\lambda(t_f^*) - \lambda_0 \nabla K(x^*(t_f^*))$ is orthogonal to the tangent space of $S$ at $x^*(t_f^*)$. For $S = \mathbb{R}^n$ this means $\lambda(t_f^*) = \lambda_0 \nabla K(x^*(t_f^*))$, and for a fixed end point it says nothing ([transversality conditions](/transversality-conditions/)).

The case $\lambda_0 = 1$ is **normal**, and $\lambda_0 = 0$ is **abnormal**. In the abnormal case the cost does not enter the conditions at all: the conditions then describe inputs that are extreme for the constraints alone, whatever the cost. For a free end point ($S = \mathbb{R}^n$), item 4 gives $\lambda(t_f) = \lambda_0 \nabla K$, so $\lambda_0 = 0$ would force $\lambda(t_f) = 0$ and then, by the linear adjoint equation, $\lambda \equiv 0$, which is excluded. So problems with a free end point are always normal.

A pair $(x^*, u^*)$ with such multipliers is an **extremal**. Time-varying data $f(t, x, u)$ and $L(t, x, u)$ are handled by adding the state $t$; then item 3 changes to $\frac{d}{dt} H = H_t$ along the extremal.

## In plain words

Attach to each state variable a price that changes with time, the costate. Then the best input does something simple at each moment: among all allowed inputs, it picks the one that makes the current cost plus the priced rate of change of the state as small as possible. The prices themselves move backward in time by a fixed rule, starting from what the final state is worth. This turns a search over whole input functions into a pointwise choice plus a boundary value problem. The rule is necessary, not sufficient: an input that passes it may still be poor, and the rule says nothing when no best input exists. In rare cases the price of the cost itself is zero, and then the rule only reflects the constraints.

## Proof

We prove the theorem in full for a fixed final time and a free end point, $S = \mathbb{R}^n$, where $\lambda_0 = 1$. Then we prove item 3 and sketch the general case.

**Setup.** Let $\lambda$ solve $\dot\lambda = -H_x(x^*, u^*, \lambda, 1)^T$ with $\lambda(t_f) = \nabla K(x^*(t_f))$. This is a linear equation with piecewise continuous coefficients, so $\lambda$ exists and is unique on $[t_0, t_f]$.

**Needle variation.** Fix a time $\tau \in (t_0, t_f]$ where $u^*$ is continuous, a value $v \in U$, and a small $\varepsilon > 0$. Let $u_\varepsilon = v$ on $(\tau - \varepsilon, \tau]$ and $u_\varepsilon = u^*$ elsewhere. This input is admissible. Let $x_\varepsilon$ be its trajectory. Up to $\tau - \varepsilon$ it equals $x^*$. On the short interval,

$$x_\varepsilon(\tau) - x^*(\tau) = \int_{\tau - \varepsilon}^{\tau} \left( f(x_\varepsilon, v) - f(x^*, u^*) \right) dt = \varepsilon\, \Delta f + o(\varepsilon),$$

with $\Delta f = f(x^*(\tau), v) - f(x^*(\tau), u^*(\tau))$, because $x_\varepsilon - x^* = O(\varepsilon)$ on the interval and $f$ and $u^*$ are continuous there. After $\tau$ both trajectories use the same input, and by differentiable dependence on initial values, $x_\varepsilon(t) = x^*(t) + \varepsilon\, \delta(t) + o(\varepsilon)$ uniformly on $[\tau, t_f]$, where $\delta$ solves the linearized equation $\dot\delta = f_x(x^*, u^*)\, \delta$ with $\delta(\tau) = \Delta f$.

**Change of the cost.** In the same way,

$$J(u_\varepsilon) - J(u^*) = \varepsilon \left( \Delta L + \int_\tau^{t_f} L_x \delta\, dt + \nabla K^T \delta(t_f) \right) + o(\varepsilon),$$

with $\Delta L = L(x^*(\tau), v) - L(x^*(\tau), u^*(\tau))$ and $\nabla K$ at $x^*(t_f)$.

**The adjoint removes the integral.** Since $H_x = L_x + \lambda^T f_x$,

$$\frac{d}{dt}\left( \lambda^T \delta \right) = -H_x \delta + \lambda^T f_x \delta = -L_x \delta.$$

Integrating from $\tau$ to $t_f$ gives $\int_\tau^{t_f} L_x \delta\, dt = \lambda(\tau)^T \delta(\tau) - \lambda(t_f)^T \delta(t_f)$, and $\lambda(t_f)^T \delta(t_f) = \nabla K^T \delta(t_f)$. So the bracket above is $\Delta L + \lambda(\tau)^T \Delta f$, and

$$J(u_\varepsilon) - J(u^*) = \varepsilon \left( H(x^*(\tau), v, \lambda(\tau), 1) - H(x^*(\tau), u^*(\tau), \lambda(\tau), 1) \right) + o(\varepsilon).$$

Optimality gives $J(u_\varepsilon) \ge J(u^*)$. Divide by $\varepsilon$ and let $\varepsilon \to 0$: $H(x^*(\tau), v, \lambda(\tau), 1) \ge H(x^*(\tau), u^*(\tau), \lambda(\tau), 1)$. This holds for every $v \in U$, which is item 2. Items 1 and 4 hold by the choice of $\lambda$.

**Item 3, for compact $U$.** Let $m(t) = \min_{v \in U} H(x^*(t), v, \lambda(t))$. For a fixed $v$, the function $g_v(t) = H(x^*(t), v, \lambda(t))$ has the derivative

$$g_v'(t) = H_x(x^*, v, \lambda)\, f(x^*, u^*(t)) - f(x^*, v)^T H_x(x^*, u^*(t), \lambda)^T$$

at every $t$ where $u^*$ is continuous, and this derivative is bounded uniformly in $v \in U$. So $m$, a minimum of uniformly Lipschitz functions, is Lipschitz, and it is differentiable almost everywhere. Take such a $t$ where $u^*$ is also continuous, and let $w = u^*(t)$. Then $g_w(s) - m(s) \ge 0$ for all $s$, with equality at $s = t$ by item 2. So $s = t$ is a minimum, and $m'(t) = g_w'(t)$. Put $v = w$ in the formula: the two terms cancel, and $m'(t) = 0$. A Lipschitz function with derivative 0 almost everywhere is constant. By item 2, $m(t)$ is the Hamiltonian along the extremal.

**Free final time.** Still with a free end point, let $t_f^*$ be optimal. Stopping at $t_f^* - \varepsilon$ changes the cost by $-\varepsilon (L + \nabla K^T f) + o(\varepsilon) = -\varepsilon H(t_f^*) + o(\varepsilon)$, where $\lambda(t_f^*) = \nabla K$ was used. Running on to $t_f^* + \varepsilon$ with the input held at $u^*(t_f^*)$ changes it by $+\varepsilon H(t_f^*) + o(\varepsilon)$. Both changes are at least 0, so $H(t_f^*) = 0$, and by item 3, $H \equiv 0$.

**The general case, a sketch.** With a terminal constraint, the needle variations cannot all be compared with $u^*$ directly, because they move the end point off $S$. The proof first converts the cost to Mayer form with the extra state $x_{n+1}$, $\dot x_{n+1} = L$ ([optimal control problem](/optimal-control-problem/), Reductions). Each needle variation, and each change of the final time, moves the augmented end point by a vector to first order. These vectors, and their nonnegative combinations from several needles at different times, form a convex cone, the terminal cone. Optimality implies that the direction of a lower cost, $-e_{n+1}$, does not point into the interior of the cone, after the tangent space of $S$ is taken into account. A separating hyperplane then gives a nonzero normal vector $(\lambda_0, \lambda(t_f))$ with $\lambda_0 \ge 0$, and one scales it so that $\lambda_0 \in \{0, 1\}$. The case $\lambda_0 = 0$ is the case where the hyperplane is vertical, that is, where the cone fails to reach some direction of the end constraint, whatever the cost. The adjoint equation carries the normal back in time, and the separation gives items 2 to 4. The hard step is the topological argument that the end point map of the needle variations covers a neighborhood in the cone; Pontryagin et al. (1962, Chapter 2) and Liberzon (2012, Section 4.2) give it in full.

## Consequences

**A worked example.** For $\dot x = u$, $J = \int_0^1 u^2\, dt + x(1)^2$, $x(0) = 1$, $U = \mathbb{R}$, the end point is free, so $\lambda_0 = 1$. $H = u^2 + \lambda u$ gives $u = -\lambda/2$, the adjoint equation gives a constant $\lambda$, and item 4 gives $\lambda = 2 x(1)$. Then $x(1) = 1 - x(1)$, so $x(1) = 1/2$, $\lambda = 1$, $u^* = -1/2$ and $J = 1/2$. The Hamiltonian is $H = 1/4 - 1/2 = -1/4$ at all times, constant as item 3 says.

**An abnormal example.** Minimize $\int_0^1 u\, dt$ subject to $\dot x = u^2$, $x(0) = x(1) = 0$, $U = \mathbb{R}$. Since $\dot x \ge 0$, the end condition forces $\int_0^1 u^2 dt = 0$, so $u = 0$ is the only admissible input, and it is optimal. The Hamiltonian is $H = \lambda_0 u + \lambda u^2$, and $\lambda$ is constant. If $\lambda_0 = 1$, then $H$ has a minimum over $u \in \mathbb{R}$ only if $\lambda > 0$, and the minimum is at $u = -1/(2\lambda) \ne 0$. So $u^* = 0$ satisfies the theorem only with $\lambda_0 = 0$ and $\lambda > 0$. The conditions here say nothing about the cost.

- **Euler-Lagrange.** With $f(x, u) = u$ and $U = \mathbb{R}^n$, the minimum condition gives $\lambda = -L_u$, and the adjoint equation becomes the [Euler-Lagrange equation](/euler-lagrange-equation/). The minimum condition also gives the Weierstrass condition, which is stronger than the Legendre condition.
- **LQR.** For linear dynamics and quadratic cost, the extremals solve a linear two-point boundary value problem, and $\lambda = 2 P(t) x$ with the Riccati solution $P$ ([LQR problem](/lqr-problem/)). Because this problem is convex, the extremal is optimal.
- **Bang-bang and singular controls.** If $H$ is affine in $u$ and $U$ is a box, the minimum is at a vertex of $U$ wherever the switching function is nonzero. This gives the [bang-bang principle](/bang-bang-control/) for [time-optimal control](/time-optimal-control/). Where the switching function vanishes on an interval, the minimum condition does not decide $u$, and higher-order conditions are needed ([singular arc](/singular-arc/)).
- **Computation.** The theorem turns the problem into a boundary value problem for $(x, \lambda)$ in $2n$ unknowns, which the [indirect method](/indirect-method-optimal-control/) solves by shooting.
- **Sufficiency under convexity.** For a fixed final time and a fixed or free end point, if $\lambda_0 = 1$, $K$ is convex and $(x, u) \mapsto H(x, u, \lambda(t), 1)$ is convex for each $t$ with $U$ convex, then every extremal is optimal (the Mangasarian condition).
- **Link to dynamic programming.** Where the value function is $C^2$, $\lambda(t) = V_x(t, x^*(t))^T$ ([costate](/costate/), [HJB equation](/hamilton-jacobi-bellman-equation/)).

## Tightness

**Necessary, not sufficient.** Take $\dot x = u$, $J = \int_0^T (u^2 - x^2)\, dt$, $x(0) = x(T) = 0$, $U = \mathbb{R}$, with $T > \pi$. The input $u = 0$ with $\lambda = 0$ and $\lambda_0 = 1$ satisfies all four items: $H = u^2 - x^2 + \lambda u$ is minimized at $u = -\lambda/2 = 0$, and $\dot\lambda = 2 x = 0$. But $x = c \sin(\pi t / T)$ gives $J = c^2 \frac{T}{2}(\pi^2/T^2 - 1) < 0$, and $J \to -\infty$ as $c \to \infty$. So the extremal is not optimal, and no optimal input exists.

**The theorem assumes an optimal input.** For $\dot x = u$, $U = \{-1, 1\}$, $x(0) = 0$ and $J = \int_0^1 x^2\, dt$, the infimum 0 is not attained ([optimal control problem](/optimal-control-problem/), Examples). The principle then gives no information. Existence must come from a separate theorem, such as Filippov's.

**$\lambda_0$ cannot be fixed to 1.** The abnormal example above shows that the normal form can miss the optimal input.

**The minimum condition cannot be replaced by $H_u = 0$.** With a bounded $U$ the minimum is often on the boundary, as in time-optimal problems, where $H_u = 0$ has no solution.

**Discrete time is different.** For $x_{k+1} = F(x_k, u_k)$ the KKT conditions give $H_u = 0$, but the pointwise minimum of $H_k = L + \lambda_{k+1}^T F$ over $U$ can fail. Example: $x_1 = x_0 + u_0$, $x_0 = 0$, $U = [-1, 1]$, cost $-u_0^2 + 2 x_1^2$. The cost is $u_0^2$, so $u_0 = 0$ is optimal, with $\lambda_1 = 4 x_1 = 0$. But $H_0 = -u^2 + \lambda_1 u = -u^2$ is minimized at $u = \pm 1$, not at 0. A discrete maximum principle needs convexity of the set of possible $(L, F)$ values.

## History

Pontryagin, Boltyanskii and Gamkrelidze announced the maximum principle in 1956. Boltyanskii gave the first general proof, and the four authors published the book in Russian in 1961 and in English in 1962. The work came from problems of the time-optimal control of aircraft and from the classical calculus of variations, whose Weierstrass condition it extends to closed input sets. At the same time, Bellman developed [dynamic programming](/hamilton-jacobi-bellman-equation/) in the United States. Liberzon (2012, Chapter 4) gives a modern proof that follows the original.

## References
