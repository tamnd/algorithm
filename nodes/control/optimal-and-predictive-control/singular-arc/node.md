---
tag: A56AAV
kind: concept
slug: singular-arc
name: Singular arc
aliases:
- singular control
area: control/optimal-and-predictive-control
level: advanced
summary: An interval where the switching function (the coefficient of an input that enters H linearly) is zero, so the minimum condition does not fix the input and higher-order conditions are needed.
prereqs: [pontryagin-maximum-principle, bang-bang-control]
see_also: [control-hamiltonian, time-optimal-control, control-affine-system, costate, indirect-method-optimal-control, chattering, euler-lagrange-equation]
sources:
  - paper: "Henry J. Kelley, A second variation test for singular extremals, AIAA Journal 2(8), 1380-1382, 1964"
  - paper: doi:10.1080/00207216308937555
    title: A. T. Fuller, Study of an optimum non-linear control system, Journal of Electronics and Control 15(1), 63-71, 1963
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 4.4.3 (singular controls and Lie brackets) and Section 4.4.4 (Fuller's problem)
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Section 5.6 (singular intervals in optimal control problems)
  - paper: doi:10.1016/0005-1098(91)90105-B
    title: Panagiotis Tsiotras and Henry J. Kelley, Drag-law effects in the Goddard problem, Automatica 27(3), 481-490, 1991
---

A singular arc is a piece of an optimal trajectory on which the [maximum principle](/pontryagin-maximum-principle/) does not decide the input. This happens when the input enters the [Hamiltonian](/control-hamiltonian/) linearly and its coefficient, the switching function, stays at zero for a whole interval: then every allowed input minimizes the Hamiltonian. The input on the arc must come from differentiating the switching function in time, and its optimality is tested by the generalized Legendre-Clebsch condition of Kelley.

## In plain words

In many problems the best input is found by a sign: if a certain quantity is positive, push fully one way, and if it is negative, push fully the other way. Usually the quantity crosses zero only at single moments, which are the switches. Sometimes it stays exactly at zero for a while. Then the sign rule gives no advice, and the best input is often somewhere in the middle, not at a limit. To find it, you use the fact that the quantity stays at zero, so its rates of change are zero too. A rocket that climbs at a carefully reduced thrust, so that the air drag does not waste fuel, follows such a stretch.

## The idea

**Setting.** Take the [optimal control problem](/optimal-control-problem/) with a scalar input that enters affinely: $\dot x = f(x) + g(x) u$, $L = L_0(x) + c(x) u$, and $U = [u_{\min}, u_{\max}]$ (see [control-affine system](/control-affine-system/)). The Hamiltonian is

$$H = \lambda_0 L_0(x) + \lambda^T f(x) + \sigma(x, \lambda)\, u, \qquad \sigma = \lambda_0 c(x) + \lambda^T g(x).$$

The minimum condition gives $u = u_{\min}$ where $\sigma > 0$ and $u = u_{\max}$ where $\sigma < 0$. A zero of $\sigma$ at an isolated time is a switch. An interval on which $\sigma(x^*(t), \lambda(t)) \equiv 0$ is a **singular arc**, and there the minimum condition holds for every $u \in U$.

**Finding the input.** On a singular arc all time derivatives of $\sigma$ vanish. Differentiate along the canonical equations. The input $u$ first appears explicitly in an even derivative, $d^{2q}\sigma / dt^{2q}$ (for a scalar input it cannot first appear in an odd one), and the number $q$ is the **order** of the arc. Setting that derivative to zero and solving for $u$ gives the singular input as a function of $(x, \lambda)$. For $L = \lambda_0 \cdot 1$ (minimum time, so $c = 0$) the derivatives are Lie brackets: $\dot\sigma = \lambda^T [f, g]$ and $\ddot\sigma = \lambda^T [f, [f, g]] + u\, \lambda^T [g, [f, g]]$, with $[f, g] = g_x f - f_x g$. If $\lambda^T [g, [f, g]] \ne 0$ the arc has order 1, and

$$u_{\text{sing}} = -\frac{\lambda^T [f, [f, g]]}{\lambda^T [g, [f, g]]}.$$

**Testing it.** The classical Legendre-Clebsch condition $H_{uu} \ge 0$ is empty here, because $H_{uu} = 0$. The **generalized Legendre-Clebsch condition** (Kelley 1964 for $q = 1$, extended to higher orders in later work) is the necessary condition

$$(-1)^q \frac{\partial}{\partial u} \left[ \frac{d^{2q}}{dt^{2q}} H_u \right] \ge 0$$

along a minimizing singular arc, in the minimum form of this area. A singular arc that fails it cannot be part of a minimizer. The condition is necessary, not sufficient.

**Junctions.** An optimal trajectory can join a bang arc to a singular arc. For arcs of order 1, the input usually jumps from the bound to the singular value at the junction. For the order-2 arc of Fuller's problem below, no junction with finitely many switches is optimal: the input switches infinitely often in a finite time before it reaches the arc. This is **chattering** in the sense of Fuller. It is a property of the optimal input, and it is different from the [chattering](/chattering/) of [sliding mode control](/sliding-mode-control/), which comes from fast switching of a feedback.

## Examples

**A first-order arc.** Minimize $\int_0^2 x^2\, dt$ with $\dot x = u$, $|u| \le 1$, $x(0) = 1$, free end. Here $H = x^2 + \lambda u$, $\sigma = \lambda$, $\dot\lambda = -2x$, $\lambda(2) = 0$. The optimal input is $u = -1$ on $[0, 1]$, which brings $x$ to 0, and then $u = 0$ on $[1, 2]$, a value inside $U$. The cost is $\int_0^1 (1 - t)^2 dt = 1/3$. Check with the maximum principle: on $[1, 2]$, $x = 0$, so $\lambda$ is constant and equal to $\lambda(2) = 0$, and the arc is singular. On $[0, 1)$, $\lambda(t) = \int_t^1 2(1 - s)\, ds = (1 - t)^2 > 0$, so $u = -1$, as used. On the arc, $\sigma = \lambda$, $\dot\sigma = -2x$ and $\ddot\sigma = -2u$, so $u$ appears in the second derivative, $q = 1$, and $u_{\text{sing}} = 0$. The test gives $(-1)^1 \cdot \partial(-2u)/\partial u = 2 \ge 0$, so it passes. If instead we maximize $\int x^2\, dt$ (minimize $-\int x^2\, dt$), the same computation gives $\ddot\sigma = 2u$ and the value $-2 < 0$. So the arc $x = 0$ is not part of a maximizer, as expected.

**Fuller's problem: an order-2 arc and chattering.** Minimize $\int_0^\infty x_1^2\, dt$ with $\dot x_1 = x_2$, $\dot x_2 = u$, $|u| \le 1$. With $H = x_1^2 + \lambda_1 x_2 + \lambda_2 u$: $\dot\lambda_1 = -2 x_1$ and $\dot\lambda_2 = -\lambda_1$. Then $\sigma = \lambda_2$, $\dot\sigma = -\lambda_1$, $\ddot\sigma = 2 x_1$, $\sigma^{(3)} = 2 x_2$ and $\sigma^{(4)} = 2u$. The input appears in the fourth derivative, so $q = 2$, the singular arc is the origin with $u = 0$, and the test gives $(-1)^2 \cdot 2 = 2 \ge 0$. Fuller (1963) showed that from every other start, the optimal input is bang-bang with infinitely many switches, whose times accumulate at a finite time when the state reaches the origin. The intervals between switches shrink by a constant factor. Liberzon (2012, Section 4.4.4) gives the analysis.

**The Goddard rocket.** A rocket climbs vertically against gravity and air drag, and the thrust can be set between 0 and a maximum. The task is to reach the greatest altitude with a given amount of fuel. Full thrust wastes fuel on drag at high speed, and zero thrust wastes the fuel not yet burned. For the classical drag models the optimal program is full thrust, then a singular arc with an intermediate thrust that keeps the speed at the value that balances the drag loss, and then a coast with zero thrust (Tsiotras and Kelley 1991). The thrust on the singular arc comes from the second derivative of the switching function, as above.

## Where it is used

- **Trajectory optimization for rockets and aircraft**, where thrust programs and climb paths often contain singular arcs. Problems of this kind motivated Kelley's condition.
- **Indirect methods.** An [indirect method](/indirect-method-optimal-control/) must know the order of the arcs (bang, singular, bang) in advance, and it adds the conditions $\sigma = \dot\sigma = 0$ at the entry of a singular arc to the boundary value problem.
- **Direct methods.** After discretization a singular arc shows up as an input that oscillates from one grid point to the next, because the cost hardly depends on it. A small regularization, such as a penalty $\varepsilon \int u^2 dt$, is a common fix, at the cost of a slightly different problem.
- **Linear quadratic problems with a singular weight.** If the input weight $R$ is only positive semidefinite, the LQ problem has singular arcs; the [LQR problem](/lqr-problem/) assumes $R > 0$ to exclude them.
- **The calculus of variations.** A Lagrangian that is linear in $y'$ has $L_{y'y'} = 0$, which is the singular case of the [Euler-Lagrange equation](/euler-lagrange-equation/).

## References
