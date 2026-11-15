---
tag: 3FNPFS
kind: definition
slug: state-space-representation
name: State-space representation
aliases:
- state equations
- state-variable model
area: control/modeling-and-identification
level: intro
summary: A model of a dynamical system as first-order differential or difference equations in a state vector, with an input and an output map.
prereqs: [ode-initial-value-problem]
see_also: [state-space-model, linear-time-invariant-system, transfer-function-matrix, realization-problem, minimal-realization, controllable-canonical-form, equilibrium-point, similarity-transformation]
sources:
  - paper: "R. E. Kalman, On the general theory of control systems, Proceedings of the First International Congress of the IFAC, Moscow 1960, Butterworths, London, 1961, vol. 1, 481-492"
    locator: the state of a dynamical system, and controllability and observability as properties of the state equations
  - book: isbn:9780134412054
    title: Wilson J. Rugh, Linear System Theory, second edition, Prentice Hall, 1996
    locator: Chapter 2, State Equation Representation (examples, linearization and state variable changes)
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Chapter 2 (mathematical descriptions of systems) and Chapter 4 (equivalent state equations and realizations)
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 1.1, Nonlinear Models and Nonlinear Phenomena (state equations, existence and uniqueness, and the pendulum)
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: the chapters on system modeling and on linear systems
---

A state-space representation models a dynamical system by first-order equations in a vector of state variables: a differential equation $\dot x = f(x, u)$, or a difference equation $x_{k+1} = F(x_k, u_k)$, for the state, and an output map $y = h(x, u)$. The state is the smallest summary of the past that, together with the future input, fixes the future behaviour. In the linear time-invariant case the model is $\dot x = A x + B u$, $y = C x + D u$, and it describes the same input-output behaviour as a proper rational [transfer function matrix](/transfer-function-matrix/), but it also shows the internal variables. This page is the deterministic control model; the [state-space model](/state-space-model/) page covers the probabilistic model with noise used in filtering, and the [linear time-invariant system](/linear-time-invariant-system/) page covers the input-output view by convolution.

## Definition

A *state-space representation* in continuous time consists of

- a state space $\mathbb{R}^n$, an input space $\mathbb{R}^m$ and an output space $\mathbb{R}^p$, with $n$ the *order*;
- a state equation $\dot x(t) = f(t, x(t), u(t))$;
- an output equation $y(t) = h(t, x(t), u(t))$.

In discrete time the state equation is $x_{k+1} = F(k, x_k, u_k)$ and the output equation is $y_k = H(k, x_k, u_k)$. When $f$ and $h$ do not depend on $t$, the representation is *time-invariant*.

**Standing assumptions.** In continuous time, $f$ is continuous, and locally Lipschitz in $x$ uniformly in $t$ and $u$ on compact sets (see [Lipschitz condition](/lipschitz-condition/)). Inputs are piecewise continuous. Then for each initial state $x(t_0) = x_0$ and each input there is exactly one solution on some interval $[t_0, t_0 + \delta)$, by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/) applied to $g(t, x) = f(t, x, u(t))$ between the jumps of $u$. A nonlinear solution can escape to infinity in finite time; a linear one cannot. In discrete time no assumption is needed for existence.

**The state property.** The vector $x(t_0)$ and the input on $[t_0, t]$ determine $x(t)$ and $y(t)$. No other information on the past is needed. This is what makes $x$ a state, and it is the reason the equations are of first order.

**The linear case.** The linear time-invariant representation is

$$\dot x = A x + B u, \qquad y = C x + D u, \qquad A \in \mathbb{R}^{n \times n},\ B \in \mathbb{R}^{n \times m},\ C \in \mathbb{R}^{p \times n},\ D \in \mathbb{R}^{p \times m},$$

or $x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$ in discrete time. If the matrices depend on time, it is a [linear time-varying system](/linear-time-varying-system/). The solution is given by the [variation of constants formula](/variation-of-constants-formula/). With $x(0) = 0$, the Laplace transform gives $Y(s) = G(s) U(s)$ with

$$G(s) = C (sI - A)^{-1} B + D,$$

a proper rational matrix. Conversely, every proper rational $G(s)$ has such a representation; finding one is the [realization problem](/realization-problem/).

**Coordinates are not unique.** For any invertible $T$, the substitution $x = T z$ gives the representation

$$\dot z = T^{-1} A T z + T^{-1} B u, \qquad y = C T z + D u,$$

with the same transfer matrix, since $C T (sI - T^{-1} A T)^{-1} T^{-1} B = C (sI - A)^{-1} B$. This is a [similarity transformation](/similarity-transformation/). So a representation is unique only up to such a change of coordinates, and even that only among *minimal* representations, the ones of the smallest order. Two minimal representations of the same $G$ are always related by a unique $T$ ([minimal realization](/minimal-realization/)). Representations of larger order also exist; they have parts that the input cannot reach or that the output cannot see.

## Examples and non-examples

**Mass, spring and damper.** A mass $m$ on a spring of stiffness $k$ with a damper $c$, pushed by a force $u$, obeys $m \ddot q + c \dot q + k q = u$. With the state $x = (q, \dot q)$ and the output $y = q$,

$$A = \begin{bmatrix} 0 & 1 \\ -k/m & -c/m \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 1/m \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad D = 0.$$

For $m = 1$, $c = 3$, $k = 2$, $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, its eigenvalues are $-1$ and $-2$, and $G(s) = 1/(s^2 + 3s + 2)$. Any $n$-th order linear differential equation becomes a state model in the same way, with the output and its first $n - 1$ derivatives as the state; this gives a companion matrix, as in the [controllable canonical form](/controllable-canonical-form/).

**The same system in other coordinates.** The eigenvectors of $A$ above are $(1, -1)$ and $(1, -2)$. With $T = \begin{bmatrix} 1 & 1 \\ -1 & -2 \end{bmatrix}$ and $x = T z$, $T^{-1} = \begin{bmatrix} 2 & 1 \\ -1 & -1 \end{bmatrix}$, and the new matrices are

$$T^{-1} A T = \begin{bmatrix} -1 & 0 \\ 0 & -2 \end{bmatrix}, \quad T^{-1} B = \begin{bmatrix} 1 \\ -1 \end{bmatrix}, \quad C T = \begin{bmatrix} 1 & 1 \end{bmatrix}.$$

This modal form gives $G(s) = \frac{1}{s + 1} - \frac{1}{s + 2}$, which is again $1/(s^2 + 3s + 2)$. The two state vectors have different physical meaning (position and velocity, against two modal amplitudes), but the input-output behaviour is the same.

**A non-minimal representation.** Add a third state $\dot z_3 = -5 z_3 + u$ that does not enter the output. The order is 3, the transfer function is the same, and the extra state is unobservable. This is still a valid state-space representation, but not a minimal one.

**A nonlinear example: the pendulum.** A pendulum of length $\ell$ and mass $m$ with friction coefficient $b$ and torque $u$ obeys $m \ell^2 \ddot\theta = -m g \ell \sin\theta - b \dot\theta + u$. With $x = (\theta, \dot\theta)$,

$$\dot x_1 = x_2, \qquad \dot x_2 = -\frac{g}{\ell} \sin x_1 - \frac{b}{m \ell^2} x_2 + \frac{1}{m \ell^2} u.$$

The right side is smooth, so it is locally Lipschitz. It is a [control-affine system](/control-affine-system/), with [equilibrium points](/equilibrium-point/) at $\theta = 0$ and $\theta = \pi$ for $u = 0$. Its [linearization about an equilibrium](/jacobian-linearization/) is an LTI state model.

**A discrete example.** A sampled plant from [zero-order hold discretization](/zero-order-hold-discretization/) is a discrete state model: the double integrator with period $h$ gives $x_{k+1} = \begin{bmatrix} 1 & h \\ 0 & 1 \end{bmatrix} x_k + \begin{bmatrix} h^2/2 \\ h \end{bmatrix} u_k$.

**Non-example: a pure delay.** The system $y(t) = u(t - \tau)$ with $\tau > 0$ has no finite-dimensional state-space representation. Its state at time $t$ is the whole input segment on $[t - \tau, t]$, a function, not a vector. Its transfer function $e^{-s\tau}$ is not rational. See [time-delay system](/time-delay-system/).

**Non-example: an ideal differentiator.** The system $y = \dot u$ has the transfer function $s$, which is not proper. It has no representation of the form above, because $y = Cx + Du$ cannot contain $\dot u$.

**Non-example: a wrong choice of state.** For $\ddot q = u$, the position $q$ alone is not a state: two motions with the same $q(t_0)$ and different velocities have different futures under the same input. The pair $(q, \dot q)$ is a state.

## Related definitions

- **Transfer function matrix.** The input-output description $G(s) = C(sI - A)^{-1} B + D$. It hides the parts of the state that are not controllable or not observable. See [transfer function matrix](/transfer-function-matrix/).
- **Realization and minimal realization.** A realization of $G$ is a state model with that transfer matrix. A minimal one has the least order; it is controllable and observable, and it is unique up to $x = Tz$. See [realization problem](/realization-problem/) and [minimal realization](/minimal-realization/).
- **Canonical forms.** Special coordinates in which the matrices have a fixed pattern, such as the [controllable canonical form](/controllable-canonical-form/) and the [observable canonical form](/observable-canonical-form/).
- **Controllability and observability.** Properties of $(A, B)$ and $(C, A)$ that say whether the input can steer every state and whether the output reveals every state. See [controllability](/controllability/) and [observability](/observability/).
- **Equilibrium point and linearization.** A constant solution of the state equation, and the linear state model that approximates the nonlinear one near it. See [equilibrium point](/equilibrium-point/) and [linearization about an equilibrium](/jacobian-linearization/).
- **Control-affine system.** The nonlinear class $\dot x = f(x) + g(x) u$. See [control-affine system](/control-affine-system/).
- **Descriptor systems.** The form $E \dot x = A x + B u$ with a singular $E$. It includes algebraic constraints and can represent some improper transfer functions. It is not a state-space representation in the sense of this page unless $E$ is invertible.
- **State-space model (statistics).** The model $x_t = f(x_{t-1}) + w_t$, $y_t = g(x_t) + v_t$ with random noise, used for filtering and smoothing. See [state-space model](/state-space-model/) and the [Kalman filter](/kalman-filter/).

Kalman (1960) made the state the central object of control theory, with controllability and observability defined on the state equations.

## References
