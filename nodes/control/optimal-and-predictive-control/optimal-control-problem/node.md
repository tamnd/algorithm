---
tag: 65XJN8
kind: problem
slug: optimal-control-problem
name: Optimal control problem
aliases:
- Bolza problem
- dynamic optimization problem
area: control/optimal-and-predictive-control
level: core
summary: Find the input over a horizon that minimizes a cost of the state and input, subject to the dynamics and to constraints.
prereqs: [state-space-representation, ode-initial-value-problem, lipschitz-condition]
see_also: [pontryagin-maximum-principle, hamilton-jacobi-bellman-equation, euler-lagrange-equation, lqr-problem, time-optimal-control, indirect-method-optimal-control, model-predictive-control, bellman-equation]
sources:
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 3.3 (the formulation of the optimal control problem and the forms of the cost) and Section 4.5 (existence of optimal controls)
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Chapter 1 (the statement of the problem and the performance measures)
  - book: isbn:9780891162285
    title: Arthur E. Bryson and Yu-Chi Ho, Applied Optimal Control, Optimization, Estimation, and Control, Hemisphere, 1975 (revised printing of the 1969 edition)
  - paper: doi:10.2514/2.4231
    title: John T. Betts, Survey of numerical methods for trajectory optimization, Journal of Guidance, Control, and Dynamics 21(2), 193-207, 1998
---

An optimal control problem asks for an input signal $u(t)$ on a time interval that makes a cost as small as possible. The state $x(t)$ must follow a differential equation $\dot x = f(x, u)$ from a given start, the input must stay in an allowed set, and the end of the motion may be fixed or free. The cost adds a running cost, integrated along the motion, and a terminal cost on the final state. This is the problem behind the [Pontryagin maximum principle](/pontryagin-maximum-principle/), the [Hamilton-Jacobi-Bellman equation](/hamilton-jacobi-bellman-equation/), the [LQR problem](/lqr-problem/) and [model predictive control](/model-predictive-control/).

## In plain words

You steer a system, for example a car, a rocket or a chemical reactor, for some time. At each moment you choose a setting of the controls. The settings change the motion, and the motion is fixed by physics once you choose the settings. Each choice of settings over time has a price: fuel used, time taken, distance from a target, or a mix of these. The task is to find the plan of settings with the lowest total price. The plan must obey the limits of the controls, and the system may have to end at a given place. The answer is a whole function of time, not one number, so the problem is much larger than an ordinary minimization.

## Definition

**Data.** A time interval $[t_0, t_f]$, with $t_0$ fixed and $t_f$ fixed or free. A state space $\mathbb{R}^n$ and an input set $U \subseteq \mathbb{R}^m$. A vector field $f : \mathbb{R}^n \times U \to \mathbb{R}^n$, continuous, and $C^1$ in $x$, so that each piecewise continuous input gives a unique solution on a short interval (the [Lipschitz condition](/lipschitz-condition/) and the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)). A running cost $L : \mathbb{R}^n \times U \to \mathbb{R}$ and a terminal cost $K : \mathbb{R}^n \to \mathbb{R}$, both continuous and $C^1$ in $x$. An initial state $x_0$, and a target set $S \subseteq \mathbb{R}^n$ for the final state. Time-varying data $f(t, x, u)$ and $L(t, x, u)$ are also allowed.

**Admissible inputs.** An input is admissible if it is a piecewise continuous (in the general theory, measurable and bounded) function $u : [t_0, t_f] \to U$ such that the solution of

$$\dot x(t) = f(x(t), u(t)), \qquad x(t_0) = x_0$$

exists on the whole interval and ends in the target, $x(t_f) \in S$.

**The question.** Among all admissible inputs, find one that minimizes the cost

$$J(u) = \int_{t_0}^{t_f} L(x(t), u(t))\, dt + K(x(t_f)),$$

and find the minimum value. A cost with both terms is the **Bolza form**. With $K = 0$ it is the **Lagrange form**, and with $L = 0$ it is the **Mayer form**. The three forms are equivalent; the Reductions section gives the conversions.

**Output.** An optimal input $u^*$, its trajectory $x^*$ and the value $J(u^*)$. A local answer is also of interest: an input that is optimal against nearby inputs. The [maximum principle](/pontryagin-maximum-principle/) gives necessary conditions for such an input. The [HJB equation](/hamilton-jacobi-bellman-equation/) describes the optimal cost from every start, the value function $V(t, x)$.

## Variants

- **Fixed or free final time.** With $t_f$ free, the final time is one more unknown. The [time-optimal control](/time-optimal-control/) problem is the case $L = 1$, $K = 0$, so the cost is $t_f - t_0$.
- **Fixed, free or constrained final state.** $S = \{x_1\}$ fixes the end point, $S = \mathbb{R}^n$ leaves it free, and a smooth surface $S = \{x : \psi(x) = 0\}$ constrains it. Each case gives its own boundary condition on the [costate](/costate/), the [transversality conditions](/transversality-conditions/).
- **Input constraints.** $U = \mathbb{R}^m$ is the unconstrained case. A box such as $U = [-1, 1]^m$ leads to [bang-bang](/bang-bang-control/) and [singular](/singular-arc/) controls.
- **State constraints.** A path constraint $g(x(t)) \le 0$ at all times. The necessary conditions then contain a measure as a multiplier and are harder to use.
- **Infinite horizon.** $t_f = \infty$ with no terminal cost. The cost may be infinite for some inputs, and the transversality condition at infinity needs care.
- **Discrete time.** $x_{k+1} = f(x_k, u_k)$ and the cost $\sum_{k=0}^{N-1} L(x_k, u_k) + K(x_N)$ for a horizon of $N$ steps. This is a finite-dimensional nonlinear program and the form that [model predictive control](/model-predictive-control/) solves at each sampling instant.
- **Stochastic problems.** Noise in the dynamics turns the problem into a [Markov decision process](/markov-decision-process/) in discrete time, or a controlled diffusion in continuous time.

## Examples

**A scalar problem with a free end.** Let $\dot x = u$, $x(0) = 1$, $t_f = 1$, $U = \mathbb{R}$ and

$$J(u) = \int_0^1 u(t)^2\, dt + x(1)^2.$$

Try constant inputs $u(t) = c$. Then $x(1) = 1 + c$ and $J = c^2 + (1 + c)^2$, which is smallest at $c = -1/2$ with $J = 1/4 + 1/4 = 1/2$. The input $u = 0$ costs $J = 1$, and the input $u = -1$, which brings the state exactly to 0, also costs $J = 1$. A constant input is in fact optimal here: for a given end value $x(1)$, the Cauchy-Schwarz inequality gives $\int_0^1 u^2 \ge (\int_0^1 u)^2 = (x(1) - 1)^2$, with equality only for a constant $u$. So the minimum is $1/2$ at $u^* = -1/2$. The pages on the [costate](/costate/) and the [HJB equation](/hamilton-jacobi-bellman-equation/) find the same answer by their own methods.

**A problem with no optimal input.** Let $\dot x = u$, $x(0) = 0$, $t_f = 1$, $U = \{-1, 1\}$ and $J(u) = \int_0^1 x^2\, dt$. An input that switches between $+1$ and $-1$ every $1/k$ seconds keeps $|x| \le 1/k$, so $J \le 1/k^2$, and the infimum of $J$ is 0. But $J = 0$ needs $x = 0$ on the whole interval, so $u = \dot x = 0$, which is not in $U$. No admissible input reaches the infimum. If $U$ is replaced by its convex hull $[-1, 1]$, the input $u = 0$ is optimal. This is why existence theorems ask for convex sets of velocities.

**The linear quadratic regulator.** With $f(x, u) = A x + B u$, $L = x^T Q x + u^T R u$ and $K = x^T Q_f x$, the problem is the [LQR problem](/lqr-problem/), and its answer is a linear feedback $u = -R^{-1} B^T P(t) x$ from a Riccati equation.

## Known algorithms

- **Indirect methods** apply the maximum principle first. This gives a two-point boundary value problem for the state and the costate, solved by shooting or multiple shooting with Newton's method ([indirect method](/indirect-method-optimal-control/)).
- **Direct methods** discretize the input, or the input and the state, and solve the resulting finite nonlinear program by sequential quadratic programming or an interior point method. Direct single shooting, direct multiple shooting and collocation are the main forms (Betts 1998).
- **Dynamic programming** solves the [HJB equation](/hamilton-jacobi-bellman-equation/) on a grid, or its discrete form, the [Bellman equation](/bellman-equation/), by [value iteration](/value-iteration/). It gives a global answer and a feedback, but the grid grows exponentially with the state dimension $n$.
- **Special structure.** The LQ problem reduces to a Riccati equation ([finite-horizon LQR](/finite-horizon-lqr/)). Linear time-optimal problems reduce to the search for a switching function ([bang-bang principle](/bang-bang-control/)). Convex discrete-time problems with linear dynamics are [convex optimization problems](/convex-optimization-problem/).

## Bounds

The problem in continuous time has infinitely many unknowns, so there is no general operation count. What is known:

- **Existence.** Filippov's theorem gives an optimal input when $U$ is compact, the set of velocities $\{f(x, u) : u \in U\}$ (with the running cost added as one more coordinate) is convex for every $x$, all trajectories stay bounded, and some admissible input exists (Liberzon, Section 4.5). The second example above shows that convexity cannot be dropped.
- **Necessary conditions** hold under the smoothness stated in the Definition: the [maximum principle](/pontryagin-maximum-principle/). They are not sufficient in general.
- **Sufficient conditions** come from a $C^1$ solution of the HJB equation (a verification theorem) or from convexity: for a fixed final time and a fixed or free final state, if $f$ is affine in $(x, u)$, $U$ is convex and $L$ and $K$ are convex, every input that satisfies the maximum principle in the normal form is optimal.
- **Hardness after discretization.** The discrete-time problem with general $f$ and $L$ contains every nonconvex nonlinear program, for example nonconvex [quadratic programming](/quadratic-programming/), which is [NP-hard](/np-hard/). So no polynomial-time method for the global minimum is known in general. The LQ case costs $O(n^3)$ operations per step of the Riccati recursion, in the real-ram model.

## Reductions

**Lagrange to Mayer.** Add a state $x_{n+1}$ with $\dot x_{n+1} = L(x, u)$ and $x_{n+1}(t_0) = 0$. Then $\int_{t_0}^{t_f} L\, dt = x_{n+1}(t_f)$, and the cost becomes a terminal cost of the augmented state. A Bolza cost becomes $x_{n+1}(t_f) + K(x(t_f))$, also in Mayer form.

**Mayer to Lagrange.** If $K$ is $C^1$, then along every trajectory

$$K(x(t_f)) = K(x_0) + \int_{t_0}^{t_f} \nabla K(x(t))^T f(x(t), u(t))\, dt.$$

The first term is a constant, so minimizing $K(x(t_f))$ is the same as minimizing the integral of $\tilde L(x, u) = \nabla K(x)^T f(x, u)$. With the two conversions, the Bolza, Lagrange and Mayer forms are equivalent. In the scalar example above, the Mayer form uses the states $(x, z)$ with $\dot z = u^2$, $z(0) = 0$, and the cost $z(1) + x(1)^2$.

**Time-varying to time-invariant.** Add the state $x_0 = t$ with $\dot x_0 = 1$. Then $f(t, x, u)$ becomes a function of the augmented state.

**Free final time to fixed final time.** Write $t = t_0 + \tau s$ with $s \in [0, 1]$ and treat $\tau = t_f - t_0$ as one more state with $\dot \tau = 0$. The dynamics become $dx/ds = \tau f(x, u)$, on a fixed interval.

**Calculus of variations.** With $U = \mathbb{R}^n$ and $f(x, u) = u$, the input is the derivative of the state, and the problem is the basic problem of the calculus of variations, minimize $\int L(x, \dot x)\, dt$. Its first-order condition is the [Euler-Lagrange equation](/euler-lagrange-equation/).

**Discrete time to nonlinear programming.** With the inputs $u_0, \dots, u_{N-1}$ as unknowns, the discrete-time problem is a nonlinear program with $N m$ variables. The [KKT conditions](/kkt-conditions/) of that program, with the multipliers of the dynamics as a discrete costate, are the discrete maximum principle for an unconstrained input.

## Applications

- Trajectories for aircraft, rockets and spacecraft, which motivated much of the theory in the 1950s and 1960s.
- Robot motion planning, with costs of time, energy or smoothness.
- Chemical processes, for example the temperature profile of a batch reactor.
- Economics, where optimal growth models are infinite-horizon problems.
- Feedback design through receding horizons: [model predictive control](/model-predictive-control/) solves a discrete-time optimal control problem at every sampling instant.

## References
