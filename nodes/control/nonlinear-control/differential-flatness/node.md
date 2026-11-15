---
tag: Y45QJA
kind: definition
slug: differential-flatness
name: Differential flatness
aliases:
- flat system
- flatness
area: control/nonlinear-control
level: advanced
summary: A system is flat if m outputs and their derivatives give all states and inputs with no integration. Trajectories can then be planned in those outputs; no general test exists for m >= 2.
prereqs: [feedback-linearization, controllability]
see_also: [feedback-linearization, feedback-linearizability-conditions, quadrotor-differential-flatness, unicycle-model, trajectory-generation-problem, minimum-snap-trajectory, controllability, kinematic-bicycle-model]
sources:
  - paper: doi:10.1080/00207179508921959
    title: "M. Fliess, J. Lévine, P. Martin and P. Rouchon, Flatness and defect of non-linear systems: introductory theory and examples, International Journal of Control 61(6), 1327-1361, 1995"
    locator: the definition of a flat system and a flat output, the link with linearization by endogenous dynamic feedback, and the examples
  - paper: doi:10.1016/0167-6911(89)90031-5
    title: "B. Charlet, J. Lévine and R. Marino, On dynamic feedback linearization, Systems and Control Letters 13(2), 143-151, 1989"
    locator: a single-input system is linearizable by dynamic feedback only if it is linearizable by static feedback
  - book: isbn:9783642008382
    title: "Jean Lévine, Analysis and Control of Nonlinear Systems: A Flatness-based Approach, Springer, 2009"
    locator: the definition of flatness, the characterization of flat outputs and the trajectory planning examples
---

A system is differentially flat if there is a set of outputs, as many as the inputs, such that all states and all inputs are functions of these outputs and a finite number of their derivatives, with no integration. These outputs are called flat outputs. They can be chosen freely as functions of time, and then the states and inputs follow by algebra and differentiation. So planning a motion becomes the choice of a smooth curve for the flat outputs that meets the boundary conditions, a task that needs no differential equation to be solved. Flatness was introduced by Fliess, Lévine, Martin and Rouchon in the 1990s. It is close to [feedback linearization](/feedback-linearization/): a flat system is linearizable by a dynamic feedback of a special kind, and for one input flatness is the same as static feedback linearizability. Its main use is [trajectory generation](/trajectory-generation-problem/), for vehicles such as the [unicycle](/unicycle-model/) and the [quadrotor](/quadrotor-differential-flatness/).

## Definition

**Setting.** The system is $\dot x = f(x, u)$ with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, $f$ smooth, and $\operatorname{rank} \frac{\partial f}{\partial u} = m$. Smoothness makes $f$ locally Lipschitz, so solutions are unique for each input by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/).

The system is **(differentially) flat** if there are an integer $q$, a smooth map

$$y = h(x, u, \dot u, \dots, u^{(p)}) \in \mathbb{R}^m,$$

and smooth maps $\varphi$ and $\psi$ such that, along every trajectory of the system,

$$x = \varphi(y, \dot y, \dots, y^{(q)}), \qquad u = \psi(y, \dot y, \dots, y^{(q+1)}).$$

Then $y$ is a **flat output**. Its components are differentially independent: they satisfy no differential equation $R(y, \dot y, \dots, y^{(k)}) = 0$. So every smooth curve $t \mapsto y(t)$ is the flat output of exactly one trajectory, given by $\varphi$ and $\psi$. In most applications the definition is local: the maps exist on an open set of the variables, and singular points are excluded.

**Properties.**

- The number of flat outputs equals the number of inputs, $m$.
- A flat output is not unique. Any invertible smooth map of $y$ and its derivatives with the same properties gives another one.
- A flat system can be transformed by an endogenous dynamic feedback (a feedback with extra states that are themselves functions of $x$, $u$ and derivatives of $u$) and a change of coordinates into $m$ chains of integrators $y_i^{(k_i)} = v_i$ (Fliess et al. 1995). Conversely, every system that can be linearized this way is flat.
- For one input, $m = 1$, a system is flat if and only if it is static feedback linearizable (Charlet, Lévine and Marino 1989). Then the flat output is an output of [relative degree](/relative-degree/) $n$, and the [conditions for feedback linearizability](/feedback-linearizability-conditions/) are a complete test.
- For $m \ge 2$ there is no general test that decides flatness from $f$. Flat outputs are found by physical insight, or by tests for special classes.
- A flat system is controllable in the sense that its trajectories can join any two points where the maps $\varphi$, $\psi$ are defined: choose a curve $y(t)$ that matches the values of $y, \dot y, \dots, y^{(q)}$ given by the two points.

## Examples and non-examples

**Linear systems.** A linear system $\dot x = A x + B u$ is flat if and only if it is [controllable](/controllability/). For one input, the flat output is $y = w^T x$, with $w^T$ the last row of the inverse of $\mathcal{C} = [B, A B, \dots, A^{n-1} B]$. For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $\mathcal{C} = \begin{bmatrix} 0 & 1 \\ 1 & -3 \end{bmatrix}$ and $\mathcal{C}^{-1} = \begin{bmatrix} 3 & 1 \\ 1 & 0 \end{bmatrix}$, so $y = x_1$. Then $x_2 = \dot y$ and $u = \ddot y + 3 \dot y + 2 y$.

**The unicycle.** For $\dot p_1 = v \cos\theta$, $\dot p_2 = v \sin\theta$, $\dot\theta = \omega$ with inputs $v$ and $\omega$, the position $y = (p_1, p_2)$ is a flat output. Where $v > 0$,

$$\theta = \operatorname{atan2}(\dot p_2, \dot p_1), \qquad v = \sqrt{\dot p_1^2 + \dot p_2^2}, \qquad \omega = \frac{\dot p_1 \ddot p_2 - \dot p_2 \ddot p_1}{\dot p_1^2 + \dot p_2^2}.$$

For the planned path $p_1 = t$, $p_2 = t^2$, at $t = 1$: $\dot p = (1, 2)$ and $\ddot p = (0, 2)$, so $\theta = \operatorname{atan2}(2, 1) = 1.10715$, $v = \sqrt 5 = 2.23607$ and $\omega = 2/5 = 0.4$. At $v = 0$ the heading is not defined by the path, so a stop inside a plan is a singular point. The [differential drive](/differential-drive-model/) moves like the unicycle, with the midpoint of its wheel axle as the flat output. For the [kinematic bicycle model](/kinematic-bicycle-model/), the center of the rear axle is a flat output.

**Feedback linearizable systems.** For the pendulum $\dot x_1 = x_2$, $\dot x_2 = -a \sin x_1 - b x_2 + c u$, the angle $y = x_1$ is a flat output: $x_2 = \dot y$ and $u = (\ddot y + a \sin y + b \dot y)/c$.

**The quadrotor.** The position of the center of mass and the yaw angle form a flat output of the standard rigid body model, with four inputs. The [quadrotor flatness](/quadrotor-differential-flatness/) page gives the maps, and [minimum snap trajectories](/minimum-snap-trajectory/) plan the position as polynomials because of it.

**Non-example: a system that is not feedback linearizable.** The single-input system $\dot x_1 = x_2 + x_3^2$, $\dot x_2 = x_3$, $\dot x_3 = u$ fails the involutivity condition, so it is not static feedback linearizable. By Charlet, Lévine and Marino (1989) it is not flat, although its Jacobian linearization is controllable and so is flat.

**Non-example: an uncontrollable part.** For $\dot x_1 = -x_1$, $\dot x_2 = u$, every trajectory has $x_1(t) = x_1(0) e^{-t}$. If $x_1$ were a function of a flat output and its derivatives, these would satisfy the differential equation $\dot x_1 = -x_1$, which flatness forbids. So the system is not flat.

**Non-example: an output with internal states.** For a single-input system and an output with relative degree $r < n$, $x$ is not a function of $y$ and its derivatives alone: the $n - r$ internal states follow the [zero dynamics](/zero-dynamics/), a differential equation driven by $y$. Such an output is not flat.

## Related definitions

- [Feedback linearization](/feedback-linearization/): static linearization, the same as flatness for one input.
- [Conditions for feedback linearizability](/feedback-linearizability-conditions/): the test for one input.
- [Controllability](/controllability/): linear flatness is controllability.
- [Trajectory generation problem](/trajectory-generation-problem/): the main use of flat outputs.
- [Relative degree](/relative-degree/): a flat output of a single-input system has relative degree $n$.

## References
