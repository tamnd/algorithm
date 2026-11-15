---
tag: RFCEGD
kind: model
slug: control-affine-system
name: Control-affine nonlinear system
aliases:
- affine nonlinear system
- input-affine system
area: control/modeling-and-identification
level: core
summary: A nonlinear system whose state derivative is a drift vector field plus input vector fields weighted by the inputs, x' = f(x) + g(x)u.
prereqs: [state-space-representation, jacobian-linearization]
see_also: [lie-bracket, lie-derivative, relative-degree, feedback-linearization, lie-algebra-rank-condition, brockett-condition, control-lyapunov-function, port-hamiltonian-system]
sources:
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: the chapters on local decompositions and controllability of input-affine systems, and on feedback linearization, relative degree and zero dynamics
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, Deterministic Finite Dimensional Systems, second edition, Springer, 1998
    locator: the chapters on nonlinear controllability (Lie algebra rank condition) and on feedback stabilization (control Lyapunov functions and the universal formula)
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: the chapter on feedback linearization (input-output linearization, relative degree and full-state linearization)
---

A control-affine nonlinear system is a state model in which the input enters linearly, though the state does not:

$$\dot x = f(x) + \sum_{i=1}^{m} g_i(x)\, u_i = f(x) + g(x)\, u, \qquad y = h(x).$$

The vector field $f$ is the *drift*, what the system does with zero input, and the $g_i$ are the *input vector fields*, the directions in which the inputs push. Most models of mechanical, electrical and chemical systems with forces, torques, voltages or flows as inputs have this form. It is the standard class of nonlinear control theory, because the tools based on [Lie derivatives](/lie-derivative/) and [Lie brackets](/lie-bracket/) need the input to enter linearly. The linear model $\dot x = A x + B u$ of the [state-space representation](/state-space-representation/) page is the case $f(x) = A x$, $g(x) = B$.

## The machine

**Equations.** The state is $x \in D \subseteq \mathbb{R}^n$, an open set; the input is $u \in \mathbb{R}^m$ (or a subset $U$, for bounded inputs), and the output is $y \in \mathbb{R}^p$. The model is $\dot x = f(x) + g(x) u$, $y = h(x)$, where $g(x) = [g_1(x) \cdots g_m(x)]$ is an $n \times m$ matrix.

**Standing assumptions.** $f$, the $g_i$ and $h$ are smooth ($C^\infty$) on $D$. Smoothness is more than existence needs; it is assumed so that Lie derivatives and brackets of any order exist. Inputs are piecewise continuous. Since the right side is locally Lipschitz in $x$, there is a unique solution from each initial state, on some interval (see [Lipschitz condition](/lipschitz-condition/)). Unlike a linear system, it can escape in finite time: $\dot x = x^2 + u$ with $u = 0$ and $x(0) = 1$ gives $x(t) = 1 / (1 - t)$, which is infinite at $t = 1$.

**Examples.**

- *Pendulum with a torque.* $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - 0.5 x_2 + u$ (normalized). Here $f(x) = (x_2, -\sin x_1 - 0.5 x_2)$ and $g = (0, 1)$, a constant input field.
- *Mechanical systems.* $M(q) \ddot q + C(q, \dot q) \dot q + G(q) = \tau$, with a positive definite inertia matrix $M(q)$. With $x = (q, \dot q)$, $f(x) = (\dot q, -M(q)^{-1}(C(q, \dot q) \dot q + G(q)))$ and $g(x) = \begin{bmatrix} 0 \\ M(q)^{-1} \end{bmatrix}$. This is the form used by [computed torque control](/computed-torque-control/).
- *A wheeled robot.* The [unicycle model](/unicycle-model/) $\dot p_1 = v \cos\phi$, $\dot p_2 = v \sin\phi$, $\dot\phi = \omega$ has $f = 0$, $g_1 = (\cos\phi, \sin\phi, 0)$ and $g_2 = (0, 0, 1)$. A system with $f = 0$ is called *driftless*.
- *Bilinear systems.* $\dot x = A x + \sum_i u_i N_i x$, with $g_i(x) = N_i x$. Examples are a heat exchanger with the flow rate as input, and population models where the input scales a rate.

**Non-examples.** $\dot x = -x + \sin u$, or a ship whose steering force is a nonlinear function of the rudder angle, are not affine in $u$. A model $\dot x = F(x, u)$ can be made affine by a *dynamic extension*: take $u$ as a new state with $\dot u = v$, and $v$ as the new input. Then $\dot x = F(x, u)$, $\dot u = v$ is affine in $v$. The price is a larger state, and the controller must then produce the rate of the original input.

## What it counts

The model gives the state and output trajectories for each initial state and input. The objects the theory works with are derivatives along the vector fields.

**Lie derivatives.** For a function $h$, $L_f h = \frac{\partial h}{\partial x} f$ is its rate of change along $f$, and similarly $L_{g_i} h$. Along a solution,

$$\dot y = L_f h(x) + L_g h(x)\, u,$$

again affine in $u$. If $L_g h = 0$, differentiate again, and so on. The *relative degree* is the number $r$ of derivatives needed before the input appears, with $L_g L_f^{r-1} h(x) \ne 0$ (see [relative degree](/relative-degree/)). For the pendulum with $y = x_1$, $\dot y = x_2$ and $\ddot y = -\sin x_1 - 0.5 x_2 + u$, so $r = 2$.

**Lie brackets.** $[f, g] = (Dg) f - (Df) g$ measures the motion that results from moving along $f$ and $g$ in turn and then back. Brackets give directions of motion that no input field gives directly. For the unicycle, $[g_1, g_2] = (\sin\phi, -\cos\phi, 0)$, a sideways motion.

**Linearization.** At an equilibrium $(x^*, u^*)$ with $f(x^*) + g(x^*) u^* = 0$, the [linearization about an equilibrium](/jacobian-linearization/) is

$$A = \frac{\partial f}{\partial x}(x^*) + \sum_{i} u_i^* \frac{\partial g_i}{\partial x}(x^*), \qquad B = g(x^*).$$

## Relation to other models

- **Linear time-invariant.** $f(x) = A x$, $g(x) = B$, $h(x) = C x$. Lie derivatives reduce to products such as $C A^k B$, the Markov parameters, and the Lie algebra rank condition reduces to the Kalman rank condition of [controllability](/controllability/).
- **General nonlinear systems.** $\dot x = F(x, u)$ contains the affine class. Dynamic extension (above) maps the general class into the affine one.
- **Driftless systems.** $f = 0$. They model kinematic constraints such as rolling without slipping. Every state is an equilibrium for $u = 0$.
- **Mechanical and port-Hamiltonian systems.** A [port-Hamiltonian system](/port-hamiltonian-system/) $\dot x = (J(x) - R(x)) \nabla H(x) + g(x) u$, $y = g(x)^T \nabla H(x)$ is control-affine with an energy structure, and satisfies $\dot H \le y^T u$.
- **Linearization.** At each equilibrium the model has an LTI linearization (above); along a trajectory it has a [linear time-varying](/linear-time-varying-system/) one.

## Known results in the model

- **Accessibility (theorem).** If the vectors of the Lie algebra generated by $f, g_1, \dots, g_m$ span $\mathbb{R}^n$ at $x_0$, the set of states reachable from $x_0$ has a nonempty interior. For driftless systems, the same rank condition at every point of a connected $D$ implies that every state can be steered to every other state (the Chow-Rashevskii theorem). See [Lie algebra rank condition](/lie-algebra-rank-condition/). For the unicycle, $g_1$, $g_2$ and $[g_1, g_2]$ have determinant

  $$\det \begin{bmatrix} \cos\phi & 0 & \sin\phi \\ \sin\phi & 0 & -\cos\phi \\ 0 & 1 & 0 \end{bmatrix} = 1,$$

  so the robot can reach every pose, although its linearization at rest is not controllable.
- **Obstruction to smooth stabilization (theorem).** If a continuous feedback $u = k(x)$ makes $x^* = 0$ asymptotically stable, the map $(x, u) \mapsto f(x) + g(x) u$ is onto a neighbourhood of 0 ([Brockett condition](/brockett-condition/)). For the unicycle near the origin, a velocity $(0, \varepsilon, 0)$ needs $v \sin\phi = \varepsilon$ with $\cos\phi = 0$, which is impossible with $\phi$ near 0. So the unicycle is controllable but has no continuous static stabilizing feedback.
- **Input-output linearization (theorem).** If the relative degree is $r$ near $x_0$, the feedback

  $$u = \frac{v - L_f^r h(x)}{L_g L_f^{r-1} h(x)}$$

  gives $y^{(r)} = v$, an integrator chain. The rest of the state, $n - r$ dimensions, evolves by the [zero dynamics](/zero-dynamics/), which must be stable for the closed loop to be stable (Isidori 1995). For the pendulum with $y = x_1$, $u = \sin x_1 + 0.5 x_2 + v$ gives $\ddot y = v$, and $r = n = 2$, so there are no zero dynamics. See [input-output linearization](/input-output-linearization/).
- **Full-state feedback linearization (theorem).** A single-input system is exactly linearizable by a state transformation and feedback near $x_0$ if and only if the vectors $g, \mathrm{ad}_f g, \dots, \mathrm{ad}_f^{n-1} g$ are linearly independent at $x_0$ and the set $\{g, \dots, \mathrm{ad}_f^{n-2} g\}$ is involutive near $x_0$, where $\mathrm{ad}_f g = [f, g]$ (Isidori 1995). See [feedback linearization](/feedback-linearization/) and [feedback linearizability conditions](/feedback-linearizability-conditions/).
- **Control Lyapunov functions (theorem).** A smooth positive definite $V$ is a [control Lyapunov function](/control-lyapunov-function/) if $L_g V(x) = 0$ implies $L_f V(x) < 0$ for $x \ne 0$. Because the input enters linearly, the condition "some $u$ makes $\dot V < 0$" is the explicit test above, and Sontag's formula

  $$u = -\frac{a + \sqrt{a^2 + \|b\|^4}}{\|b\|^2}\, b^T \quad (b \ne 0), \qquad u = 0 \quad (b = 0),$$

  with $a = L_f V$ and $b = L_g V$, gives a feedback that is smooth away from the origin and makes it asymptotically stable (see [Sontag's universal formula](/sontag-universal-formula/)). For $\dot x = x + u$ and $V = x^2 / 2$, $a = x^2$, $b = x$, and the formula gives $u = -(1 + \sqrt 2) x$, so the closed loop is $\dot x = -\sqrt 2\, x$. With input bounds, the same linearity in $u$ makes the pointwise choice of $u$ a quadratic program, as in [control barrier functions](/control-barrier-function/) (rule of thumb: this is why most online safety filters assume an affine model).

## References
