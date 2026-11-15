---
tag: SE57GX
kind: definition
slug: transversality-conditions
name: Transversality conditions
aliases:
- transversality condition
area: control/optimal-and-predictive-control
level: advanced
summary: The boundary conditions on the costate and the Hamiltonian at the end of the horizon when the final state or time is free.
prereqs: [pontryagin-maximum-principle]
see_also: [costate, control-hamiltonian, euler-lagrange-equation, indirect-method-optimal-control, time-optimal-control, optimal-control-problem, lagrange-multiplier]
sources:
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 2.3.5 (variable-endpoint problems in the calculus of variations) and Section 4.2.10 (the transversality condition in the proof of the maximum principle)
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Section 5.1 (the boundary conditions for the cases of fixed and free final time and final state)
  - book: isbn:9780891162285
    title: Arthur E. Bryson and Yu-Chi Ho, Applied Optimal Control, Optimization, Estimation, and Control, Hemisphere, 1975 (revised printing of the 1969 edition)
---

The transversality conditions are the boundary conditions that the [maximum principle](/pontryagin-maximum-principle/) adds at the end of the horizon for each part of the end data that is not fixed. A free final state gives a condition on the final [costate](/costate/), and a free final time gives a condition on the final value of the [Hamiltonian](/control-hamiltonian/). They supply exactly as many equations as there are free quantities, so the boundary value problem for the state and the costate has as many conditions as unknowns.

## Definition

Take the [optimal control problem](/optimal-control-problem/) with dynamics $\dot x = f(t, x, u)$, $x(t_0) = x_0$, running cost $L(t, x, u)$, terminal cost $K(t_f, x(t_f))$ with $K$ of class $C^1$, and a target

$$S = \{x \in \mathbb{R}^n : \psi(x) = 0\},$$

where $\psi : \mathbb{R}^n \to \mathbb{R}^k$ is $C^1$ and its Jacobian $\psi_x$ has rank $k$ on $S$. The case $k = 0$ is a free end point, and $\psi(x) = x - x_1$ ($k = n$) is a fixed end point. Let $H = \lambda_0 L + \lambda^T f$ with $\lambda_0 \in \{0, 1\}$, and let $(x^*, u^*, \lambda, \lambda_0)$ be an extremal on $[t_0, t_f]$.

**Transversality condition for the final state.** There is a vector $\nu \in \mathbb{R}^k$ with

$$\lambda(t_f) = \lambda_0 \nabla_x K(t_f, x^*(t_f)) + \psi_x(x^*(t_f))^T \nu.$$

Equivalently, $\lambda(t_f) - \lambda_0 \nabla_x K$ is orthogonal to the tangent space $\{d : \psi_x d = 0\}$ of $S$ at $x^*(t_f)$. This gives $n - k$ equations, one for each free direction of the end point.

**Transversality condition for the final time.** If $t_f$ is free,

$$H(t_f, x^*(t_f), u^*(t_f), \lambda(t_f), \lambda_0) = -\lambda_0 \frac{\partial K}{\partial t}(t_f, x^*(t_f)).$$

For a time-invariant problem, with $f$, $L$ and $K$ independent of $t$, this is $H(t_f) = 0$, and because $H$ is then constant along the extremal, $H \equiv 0$.

**Special cases.**

| End data | Condition at $t_f$ |
|---|---|
| final state free | $\lambda(t_f) = \lambda_0 \nabla_x K(x^*(t_f))$ |
| final state fixed | none on $\lambda(t_f)$; the $n$ conditions are $x(t_f) = x_1$ |
| some components $x_i(t_f)$ fixed, the rest free | $\lambda_j(t_f) = \lambda_0 \partial K / \partial x_j$ for each free component $j$ |
| final time free, time-invariant data | $H(t_f) = 0$ |

**At the initial time.** If the initial state is only required to lie in a set $S_0 = \{x : \psi_0(x) = 0\}$ and the cost contains a term $K_0(x(t_0))$, then $\lambda(t_0) + \lambda_0 \nabla K_0(x^*(t_0))$ is orthogonal to the tangent space of $S_0$. The sign differs from the final condition because a larger initial state enters the remaining cost with the opposite sign of a larger final state.

**Why these conditions.** The costate is the sensitivity of the cost to the state ([costate](/costate/)). At the final time the remaining cost is $K$, so along every free direction $d$ of the end point the costate must agree with the gradient of $K$; otherwise a small move of the end point along $d$ would lower the cost. Along the directions normal to $S$ the end point cannot move, and the multiplier $\nu$ absorbs the difference, as a [Lagrange multiplier](/lagrange-multiplier/) does. In the same way, stopping a little earlier or later changes the cost at the rate $H + \partial K / \partial t$, which must vanish. The proof for the free end point and the free final time is on the page of the [maximum principle](/pontryagin-maximum-principle/).

## Examples and non-examples

**Free end point.** For $\dot x = u$, $J = \int_0^1 u^2\, dt + x(1)^2$, $x(0) = 1$: the condition is $\lambda(1) = 2 x(1)$. With the constant costate $\lambda = 2 x(1)$ and $u = -\lambda/2$, this gives $x(1) = 1/2$, $\lambda = 1$ and the optimal cost $1/2$.

**End point on a line.** In $\mathbb{R}^2$, minimize $\int_0^1 |u|^2 dt$ with $\dot x = u$, $x(0) = (0, 0)$ and $x(1)$ on the line $x_1 + x_2 = 1$. Here $\psi(x) = x_1 + x_2 - 1$, $\psi_x = (1, 1)$, and $K = 0$. The costate is constant, $u = -\lambda/2$, and the condition is $\lambda = \nu (1, 1)$, so the motion is normal to the line. Then $x(1) = -\lambda/2 = -(\nu/2)(1, 1)$ lies on the line for $\nu = -1$, so $x(1) = (1/2, 1/2)$, $u = (1/2, 1/2)$ and the cost is $1/2$. This is the closest point of the line to the origin, as it should be.

**Free final time.** Minimize $\int_0^{t_f} (1 + u^2)\, dt$ with $\dot x = u$, $x(0) = 1$, $x(t_f) = 0$ and $t_f$ free. Here $H = 1 + u^2 + \lambda u$ and $\lambda$ is constant, so $u = -\lambda/2$ and $H = 1 - \lambda^2/4$. The condition $H = 0$ gives $\lambda = \pm 2$. To move from 1 to 0 the input must be negative, so $\lambda = 2$, $u = -1$, $t_f = 1$ and the cost is 2. A direct check: a constant speed $s$ takes the time $1/s$ and costs $(1 + s^2)/s$, which is smallest at $s = 1$ with the value 2.

**The same problem with a terminal cost in time.** Write the cost as $\int_0^{t_f} u^2\, dt + K(t_f)$ with $K(t) = t$. Now $H = u^2 + \lambda u = -\lambda^2/4$, and the condition is $H(t_f) = -\partial K / \partial t = -1$. Again $\lambda = 2$, $u = -1$ and $t_f = 1$.

**Non-example: forgetting the time term.** In the last example, the condition $H(t_f) = 0$ would give $\lambda = 0$ and $u = 0$, and the state would never reach 0. The rule $H(t_f) = 0$ holds only when $K$ does not depend on $t$.

**Non-example: a condition on a fixed end point.** For $\dot x = u$, $J = \int_0^1 u^2\, dt$, $x(0) = 0$, $x(1) = 1$, the optimal input is $u = 1$ and the costate is $\lambda = -2$. Writing $\lambda(1) = \nabla K = 0$ would be wrong: a fixed end point puts no condition on $\lambda(1)$, and the end condition $x(1) = 1$ replaces it.

**Non-example: an infinite horizon.** For $t_f = \infty$, the condition $\lambda(t) \to 0$ as $t \to \infty$ looks natural, but it is not necessary in general. Halkin (1974) gave an example of an optimal input whose costate does not tend to 0. Infinite-horizon problems need extra hypotheses for any condition at infinity.

## Related definitions

- **Natural boundary condition.** In the calculus of variations, a free end value $y(b)$ gives $L_{y'} = 0$ at $b$ ([Euler-Lagrange equation](/euler-lagrange-equation/)). With $\lambda = -L_{y'}$ this is the free end point case with $K = 0$.
- **Normality.** With a free end point the condition $\lambda(t_f) = \lambda_0 \nabla K$ excludes $\lambda_0 = 0$, so every such problem is normal ([maximum principle](/pontryagin-maximum-principle/)).
- **Shooting.** In the [indirect method](/indirect-method-optimal-control/), the transversality conditions are the residual equations that Newton's method drives to zero.
- **Time-optimal control.** For the [time-optimal problem](/time-optimal-control/) with $L = 1$, the free final time gives $\lambda_0 + \lambda(t_f)^T f(x^*(t_f), u^*(t_f)) = 0$.

## References
