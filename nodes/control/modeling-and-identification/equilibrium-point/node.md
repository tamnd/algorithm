---
tag: QNHMXC
kind: definition
slug: equilibrium-point
name: Equilibrium point
aliases:
- equilibrium of a dynamical system
- rest point
area: control/modeling-and-identification
level: intro
summary: A state where the vector field is zero for a fixed input, so the constant function at that state is a solution of the state equation for all time.
prereqs: [state-space-representation]
see_also: [jacobian-linearization, lyapunov-stability, asymptotic-stability, region-of-attraction, lyapunov-indirect-method, limit-cycle, fixed-point-iteration, lipschitz-condition]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 1.1, Nonlinear Models and Nonlinear Phenomena (equilibrium points, multiple equilibria); Section 2.3, Qualitative Behavior Near Equilibrium Points
  - book: isbn:9780134412054
    title: Wilson J. Rugh, Linear System Theory, second edition, Prentice Hall, 1996
    locator: Chapter 2, State Equation Representation (linearization about a constant nominal solution)
  - paper: doi:10.1090/S0002-9939-1960-0121542-7
    title: Philip Hartman, A lemma in the theory of structural stability of differential equations, Proceedings of the American Mathematical Society 11(4), 610-620, 1960
    locator: the local topological equivalence of a flow and its linearization at a hyperbolic equilibrium
  - paper: "D. M. Grobman, Homeomorphism of systems of differential equations, Doklady Akademii Nauk SSSR 128, 880-881, 1959"
    locator: the same local equivalence, found independently
---

An equilibrium point of a dynamical system is a state at which the system can rest: for the state equation $\dot x = f(x, u)$ and a fixed constant input $u^*$, a state $x^*$ with $f(x^*, u^*) = 0$. Then the constant function $x(t) = x^*$ is a solution, and when solutions are unique, a system that starts at $x^*$ with the input $u^*$ stays at $x^*$ for all time. In discrete time the condition is $F(x^*, u^*) = x^*$, a fixed point of the update map. Stability is a property of an equilibrium, not of a system, and the [linearization about an equilibrium](/jacobian-linearization/) is the main tool to study the system near it.

## Definition

Consider a time-invariant [state-space representation](/state-space-representation/) $\dot x = f(x, u)$ with $f : \mathbb{R}^n \times \mathbb{R}^m \to \mathbb{R}^n$.

- A pair $(x^*, u^*)$ is an *equilibrium* (or *operating point*) if $f(x^*, u^*) = 0$. For a system without input, $\dot x = f(x)$, the condition is $f(x^*) = 0$.
- For $x_{k+1} = F(x_k, u_k)$, the condition is $F(x^*, u^*) = x^*$.
- For a time-varying system $\dot x = f(t, x)$, $x^*$ is an equilibrium if $f(t, x^*) = 0$ for all $t \ge t_0$.
- An equilibrium is *isolated* if some neighbourhood of $x^*$ contains no other equilibrium.

**Constant solution.** If $f(x^*, u^*) = 0$, the constant function $x(t) = x^*$ satisfies $\dot x = 0 = f(x, u^*)$, so it is a solution. If $f$ is locally Lipschitz in $x$ (see [Lipschitz condition](/lipschitz-condition/)), it is the only solution from $x^*$, by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/). So with uniqueness, "the system stays at $x^*$" is a theorem. Without it, the system may leave; see the non-examples.

**Shift to the origin.** With $z = x - x^*$ and $v = u - u^*$, the system $\dot z = f(x^* + z, u^* + v) =: \tilde f(z, v)$ has the equilibrium $(0, 0)$. The control pages place the equilibrium at 0 unless they say otherwise.

**Linear systems.** For $\dot x = A x + B u$ and a constant $u^*$, the equilibria are the solutions of $A x^* = -B u^*$. If $A$ is invertible, there is exactly one, $x^* = -A^{-1} B u^*$, and the static gain from $u^*$ to $y^* = C x^* + D u^*$ is $-C A^{-1} B + D$. If $A$ is singular, the equilibria for $u^* = 0$ form the subspace $\ker A$, and none is isolated. A linear system therefore has either one equilibrium or a whole affine subspace of them. Several isolated equilibria occur only in nonlinear systems.

**Classification near an equilibrium.** Let $J = \partial f / \partial x (x^*, u^*)$, the Jacobian matrix. The equilibrium is *hyperbolic* if no eigenvalue of $J$ has zero real part. At a hyperbolic equilibrium of a $C^1$ system, the Hartman-Grobman theorem says that the flow near $x^*$ is topologically equivalent to the flow of $\dot z = J z$ near 0 (Hartman 1960; Grobman 1959). In the plane this gives the familiar cases: a stable or unstable node (real eigenvalues of one sign), a saddle (real eigenvalues of opposite signs), and a stable or unstable focus (complex eigenvalues). At a non-hyperbolic equilibrium, the linearization does not decide the local behaviour (Khalil 2002, Section 2.3).

## Examples and non-examples

**Pendulum.** With $x = (\theta, \dot\theta)$, $\dot x_1 = x_2$, $\dot x_2 = -\frac{g}{\ell} \sin x_1 - k x_2 + c u$. For $u^* = 0$ the equilibria are $(j\pi, 0)$ for every integer $j$; physically there are two, hanging down ($\theta = 0$) and standing up ($\theta = \pi$). With $g / \ell = 1$ and $k = 0.5$:

- At $(0, 0)$, $J = \begin{bmatrix} 0 & 1 \\ -1 & -0.5 \end{bmatrix}$, with eigenvalues $-0.25 \pm 0.9682 i$: a stable focus.
- At $(\pi, 0)$, $J = \begin{bmatrix} 0 & 1 \\ 1 & -0.5 \end{bmatrix}$, with eigenvalues $0.7808$ and $-1.2808$: a saddle, so the upright position is unstable.
- Without friction ($k = 0$), the eigenvalues at $(0, 0)$ are $\pm i$. The equilibrium is not hyperbolic, and the linearization alone does not decide stability; the energy shows that it is stable but not asymptotically stable.

With a constant torque $u^* \ne 0$, the equilibria move: $\sin x_1^* = c u^* \ell / g$. For $|c u^* \ell / g| > 1$ there is no equilibrium at all, and the pendulum turns over and over.

**Logistic growth.** $\dot x = x(1 - x)$ has the equilibria $0$ and $1$. The derivative $1 - 2x$ is $1$ at 0 (unstable) and $-1$ at 1 (asymptotically stable).

**Three equilibria.** $\ddot q = q - q^3$, with $x = (q, \dot q)$, has the equilibria $(0, 0)$, $(1, 0)$ and $(-1, 0)$. The Jacobian at the origin has eigenvalues $\pm 1$ (a saddle), and at $(\pm 1, 0)$ it has eigenvalues $\pm \sqrt 2\, i$.

**Discrete fixed points.** $x_{k+1} = x_k^2$ has the fixed points $0$ and $1$. The derivative $2x$ is $0$ at 0, so solutions near 0 converge, and $2$ at 1, so solutions near 1 move away. Finding fixed points numerically is the subject of [fixed-point iteration](/fixed-point-iteration/).

**Non-example: leaving an equilibrium without uniqueness.** For $\dot x = x^{1/3}$, $f(0) = 0$, so $x^* = 0$ is an equilibrium and $x(t) = 0$ is a solution. But $x(t) = (2t/3)^{3/2}$ is also a solution from $x(0) = 0$, because $f$ is not Lipschitz at 0. So the claim that a system started at an equilibrium stays there needs uniqueness of solutions.

**Non-example: the wrong input.** For $\dot x = -x + u$, the point $x = 1$ is an equilibrium for $u^* = 1$ and not for $u = 0$. An equilibrium is a property of the pair $(x^*, u^*)$.

**Non-example: a periodic orbit.** For $\dot x_1 = x_2 + x_1(1 - x_1^2 - x_2^2)$, $\dot x_2 = -x_1 + x_2(1 - x_1^2 - x_2^2)$, the unit circle is a periodic orbit, a [limit cycle](/limit-cycle/). Its points are not equilibria, since $f \ne 0$ on it. The only equilibrium is the origin.

**Non-example: a forced system.** $\dot x = -x + \sin t$ has no equilibrium: no constant $x^*$ makes $-x^* + \sin t$ zero for all $t$. All solutions converge to the periodic solution $x(t) = \frac12(\sin t - \cos t)$.

## Related definitions

- **Lyapunov stability and asymptotic stability.** An equilibrium is stable if solutions that start close stay close, and asymptotically stable if they also converge to it. See [Lyapunov stability](/lyapunov-stability/), [asymptotic stability](/asymptotic-stability/) and [exponential stability](/exponential-stability/).
- **Region of attraction.** The set of initial states whose solutions converge to an asymptotically stable equilibrium. See [region of attraction](/region-of-attraction/).
- **Linearization.** The LTI model $\dot z = J z + G v$ with the Jacobians at $(x^*, u^*)$. See [linearization about an equilibrium](/jacobian-linearization/); the stability test it gives is [Lyapunov's indirect method](/lyapunov-indirect-method/).
- **Operating points.** In practice, the set of equilibria $\{(x^*, u^*) : f(x^*, u^*) = 0\}$ is a family parametrized by the input, typically of dimension $m$. [Gain scheduling](/gain-scheduling/) designs one linear controller per operating point.
- **Fixed point.** The discrete-time analogue, $F(x^*) = x^*$. The [Banach fixed-point theorem](/banach-fixed-point-theorem/) gives a unique fixed point for a contraction.
- **Periodic orbit and limit cycle.** A closed orbit that is not a single point. Near it the analysis uses a Poincaré map, whose fixed point is the orbit.

## References
