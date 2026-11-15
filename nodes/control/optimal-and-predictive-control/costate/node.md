---
tag: FAF6PP
kind: definition
slug: costate
name: Costate
aliases:
- adjoint state
- costate variables
area: control/optimal-and-predictive-control
level: core
summary: The multiplier of the dynamics in an optimal control problem, which runs backward in time and gives the sensitivity of the optimal cost to the state.
prereqs: [control-hamiltonian]
see_also: [pontryagin-maximum-principle, transversality-conditions, hamilton-jacobi-bellman-equation, lagrange-multiplier, kkt-conditions, indirect-method-optimal-control, gradient-descent, lqr-problem]
sources:
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 4.2.8 (the adjoint equation in the proof of the maximum principle) and Section 5.2 (the relation between the HJB equation and the maximum principle)
  - book: isbn:9780891162285
    title: Arthur E. Bryson and Yu-Chi Ho, Applied Optimal Control, Optimization, Estimation, and Control, Hemisphere, 1975 (revised printing of the 1969 edition)
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Section 5.1 (the costate equations among the necessary conditions)
---

The costate $\lambda(t) \in \mathbb{R}^n$ is the time-varying multiplier that an optimal control problem attaches to its dynamics $\dot x = f(x, u)$. It solves a linear differential equation that runs backward from a condition at the final time, and it enters the [Hamiltonian](/control-hamiltonian/) whose minimum gives the optimal input. Where the optimal cost $V(t, x)$ is smooth, the costate is its gradient along the optimal trajectory, so $\lambda_i(t)$ is the marginal cost of one more unit of $x_i$ at time $t$.

## Definition

Take the [optimal control problem](/optimal-control-problem/) with dynamics $\dot x = f(x, u)$, running cost $L$, terminal cost $K$, and the [Hamiltonian](/control-hamiltonian/) $H(x, u, \lambda, \lambda_0) = \lambda_0 L(x, u) + \lambda^T f(x, u)$, where $f$, $L$ and $K$ are $C^1$ in $x$. Let $u^*$ be an admissible input on $[t_0, t_f]$ and $x^*$ its trajectory.

A **costate** for $(x^*, u^*)$ with cost multiplier $\lambda_0 \in \{0, 1\}$ is an absolutely continuous function $\lambda : [t_0, t_f] \to \mathbb{R}^n$ that solves the **adjoint equation**

$$\dot \lambda(t) = -H_x(x^*(t), u^*(t), \lambda(t), \lambda_0)^T = -f_x(x^*(t), u^*(t))^T \lambda(t) - \lambda_0 L_x(x^*(t), u^*(t))^T$$

for almost every $t$, together with the end conditions of the problem (the [transversality conditions](/transversality-conditions/)), and with $(\lambda_0, \lambda(t)) \ne (0, 0)$. For a free final state the end condition is $\lambda(t_f) = \lambda_0 \nabla K(x^*(t_f))$. For a fixed final state there is no condition on $\lambda(t_f)$.

The adjoint equation is linear in $\lambda$, so $\lambda(t)$ is determined by its final value, and it is integrated from $t_f$ back to $t_0$. Its homogeneous part $\dot\lambda = -f_x^T \lambda$ is the adjoint of the linearized dynamics $\dot\delta = f_x \delta$: for every solution $\delta$ of the linearization,

$$\frac{d}{dt}\left( \lambda^T \delta \right) = -\lambda_0 L_x \delta.$$

**The costate as a gradient.** Suppose the value function $V(t, x)$, the optimal cost from state $x$ at time $t$, is $C^2$ near the optimal trajectory and solves the [HJB equation](/hamilton-jacobi-bellman-equation/) $-V_t = \min_{u \in U} (L + V_x f)$. Then $\lambda(t) = V_x(t, x^*(t))^T$ is a costate with $\lambda_0 = 1$. Proof: let $\varphi(t, x) = L(x, u^*(t)) + V_t(t, x) + V_x(t, x) f(x, u^*(t))$. The HJB equation gives $\varphi \ge 0$ everywhere, and $\varphi(t, x^*(t)) = 0$ because $u^*$ attains the minimum along the optimal trajectory. So $x^*(t)$ minimizes $\varphi(t, \cdot)$, and $\varphi_x(t, x^*(t)) = 0$:

$$L_x + V_{tx} + f^T V_{xx} + V_x f_x = 0 \quad \text{at } (t, x^*(t), u^*(t)).$$

Then $\frac{d}{dt} V_x(t, x^*(t))^T = V_{xt}^T + V_{xx} f = -L_x^T - f_x^T V_x^T$, which is the adjoint equation, and $V_x(t_f, x)^T = \nabla K(x)$ is the end condition.

## Examples and non-examples

**A scalar problem.** For $\dot x = u$, $J = \int_0^T u^2\, dt + x(T)^2$, $U = \mathbb{R}$, the Hamiltonian is $H = u^2 + \lambda u$, so $u = -\lambda/2$. The adjoint equation is $\dot\lambda = -H_x = 0$, so $\lambda$ is a constant, and the end condition gives $\lambda = 2 x(T)$. Then $x(T) = x_0 - \lambda T / 2 = x_0 - x(T) T$, so $x(T) = x_0/(1 + T)$, $\lambda = 2 x_0/(1 + T)$ and $u^* = -x_0/(1 + T)$. The optimal cost is $V(0, x_0) = x_0^2/(1 + T)$, and indeed $\partial V / \partial x_0 = 2 x_0/(1 + T) = \lambda(0)$. With $x_0 = 1$ and $T = 1$: $\lambda = 1$, $u^* = -1/2$ and the cost is $1/2$.

**The costate gives the gradient of the cost.** For an input $u$ that is not optimal, solve the adjoint equation with $\lambda_0 = 1$ along its own trajectory. Then the derivative of $J$ in the direction of a change $\delta u$ of the input is $\int_{t_0}^{t_f} H_u(x, u, \lambda)\, \delta u\, dt$. In the scalar example with $T = 1$, $x_0 = 1$ and constant inputs $u = c$, $\lambda = 2(1 + c)$, and $\int_0^1 H_u\, dt = 2c + 2(1 + c)$, which is the derivative of $J = c^2 + (1 + c)^2$. This is the adjoint method for gradients. Its discrete form, $\lambda_k = L_x^T + F_x^T \lambda_{k+1}$ for $x_{k+1} = F(x_k, u_k)$, is reverse-mode differentiation, and it gives the gradient used by [gradient descent](/gradient-descent/) on the inputs.

**The linear quadratic regulator.** For the [LQR problem](/lqr-problem/) with the cost $\int (x^T Q x + u^T R u)\, dt + x(T)^T Q_f x(T)$, the value function is $V = x^T P(t) x$ and the costate is $\lambda(t) = 2 P(t) x^*(t)$, where $P$ solves the Riccati differential equation with $P(T) = Q_f$.

**Non-example: a costate that is not a gradient.** Take $\dot x = u$, $U = [-1, 1]$, $x(0) = 0$, the horizon 1 and the cost $K(x(1)) = -x(1)^2$. The inputs $u = 1$ and $u = -1$ are both optimal, with cost $-1$. The value function is $V(t, x) = -(|x| + 1 - t)^2$, which is not differentiable at $x = 0$. The costate is constant with $\lambda = -2 x(1)$, so it is $-2$ along $u = 1$ and $+2$ along $u = -1$. At $(0, 0)$ there are two costates and no gradient. For $t > 0$ each costate equals $V_x$ along its own trajectory.

**Non-example: an abnormal multiplier.** Minimize $\int_0^1 u\, dt$ with $\dot x = u^2$, $x(0) = x(1) = 0$, $U = \mathbb{R}$. Only $u = 0$ is admissible. A costate exists only with $\lambda_0 = 0$ (see the [maximum principle](/pontryagin-maximum-principle/)), and any constant $\lambda > 0$ works. Here $\lambda$ does not measure a change of the cost, because the constraint alone fixes the input.

## Related definitions

- **[Lagrange multiplier](/lagrange-multiplier/).** The costate is the multiplier of the equality constraint $\dot x - f(x, u) = 0$ at each time. In discrete time, $\lambda_{k+1}$ is the multiplier of $x_{k+1} = F(x_k, u_k)$ in the [KKT conditions](/kkt-conditions/) of the finite program.
- **Momentum.** In the calculus of variations, $\lambda = -L_{\dot x}$, the negative of the momentum of mechanics ([Euler-Lagrange equation](/euler-lagrange-equation/)).
- **Transversality conditions.** The end conditions on $\lambda$ for free, fixed and constrained end points and a free final time ([transversality conditions](/transversality-conditions/)).
- **Shooting.** In an [indirect method](/indirect-method-optimal-control/), the unknown initial costate $\lambda(t_0)$ is found by Newton's method so that the end condition holds.

## References
