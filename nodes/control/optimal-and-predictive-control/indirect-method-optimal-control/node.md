---
tag: NBHETY
kind: technique
slug: indirect-method-optimal-control
name: Indirect method for optimal control
aliases:
- optimize then discretize
area: control/optimal-and-predictive-control
level: core
summary: Solves an optimal control problem by applying the maximum principle first and then solving the boundary value problem for state and costate, usually by shooting with Newton's method.
prereqs: [pontryagin-maximum-principle, transversality-conditions, shooting-method]
see_also: [optimal-control-problem, costate, control-hamiltonian, newton-method-for-systems, homotopy-continuation, collocation-method, trajectory-optimization, singular-arc]
sources:
  - book: isbn:9780387954523
    title: Josef Stoer and Roland Bulirsch, Introduction to Numerical Analysis, third edition, Springer, 2002
    locator: Section 7.3 (boundary value problems, simple shooting and multiple shooting)
  - paper: doi:10.1007/BF02071065
    title: Oskar von Stryk and Roland Bulirsch, Direct and indirect methods for trajectory optimization, Annals of Operations Research 37, 357-373, 1992
  - paper: doi:10.2514/2.4231
    title: John T. Betts, Survey of numerical methods for trajectory optimization, Journal of Guidance, Control, and Dynamics 21(2), 193-207, 1998
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Chapter 6 (numerical determination of optimal trajectories)
  - paper: "Roland Bulirsch, Die Mehrzielmethode zur numerischen Lösung von nichtlinearen Randwertproblemen und Aufgaben der optimalen Steuerung, report of the Carl-Cranz-Gesellschaft, 1971"
  - paper: doi:10.1007/s10957-012-0050-5
    title: Emmanuel Trélat, Optimal control and applications to aerospace, some results and challenges, Journal of Optimization Theory and Applications 154(3), 713-758, 2012
---

The indirect method solves an [optimal control problem](/optimal-control-problem/) in two stages. First it applies the [maximum principle](/pontryagin-maximum-principle/): the input that minimizes the [Hamiltonian](/control-hamiltonian/) is written as a function of the state and the [costate](/costate/), and this gives a system of $2n$ differential equations with $n$ conditions at the start and $n$ conditions at the end. Then it solves this two-point boundary value problem numerically. The most common solver is [shooting](/shooting-method/): guess the initial costate, integrate forward, measure the error in the end conditions, and correct the guess with [Newton's method](/newton-method-for-systems/). The name means that the method finds the optimum indirectly, through the necessary conditions, and not by comparing costs. It is also called "optimize then discretize", in contrast to direct methods, which discretize the problem first.

## In plain words

The maximum principle gives a rule that tells the best input at each moment, if you know the current state and a second quantity, the costate, which measures how much a small change in the state is worth. The state is known at the start. The costate is not known at the start, but there is a condition that it must meet at the end. So you guess its start value, run the system forward with the rule, and look at the end. If the end condition fails, you change the guess and run again, and Newton's method tells you how to change it. When the end condition holds, the run gives an input that satisfies the necessary conditions for an optimum. The answer is very accurate, but a good first guess is necessary, and long runs of unstable systems make the method fail.

## When it applies

- The problem is smooth, and the minimum condition gives the input as an explicit and smooth function $u^*(x, \lambda)$. The usual case is a Hamiltonian that is strictly convex in $u$, for example a cost with a term $u^T R u$, $R > 0$.
- The problem is normal ($\lambda_0 = 1$). Abnormal extremals exist (see the [maximum principle](/pontryagin-maximum-principle/)), and the method does not find them unless they are set up separately.
- The structure of the solution is known: which arcs are bang, which are [singular](/singular-arc/), and where state constraints are active. With the structure known, the switching and junction times become extra unknowns.
- A good first guess for the costate is available, for example from a direct method, from a simpler problem, or from a continuation in a parameter.
- High accuracy is needed. A converged solution satisfies the necessary conditions to the accuracy of the integrator, and it gives the costate, which is the sensitivity of the optimal cost to the state.
- The method is a poor choice when the structure of the solution is unknown, when the horizon is long and the dynamics are unstable (single shooting loses all accuracy, see Pitfalls), and when only a rough answer is needed quickly. Direct methods, as in [trajectory optimization](/trajectory-optimization/) and [nonlinear MPC](/nonlinear-mpc/), are more robust in those cases.

## The template

**The boundary value problem.** Take the problem: minimize $\varphi(x(T)) + \int_0^T L(x, u)\, dt$ subject to $\dot x = f(x, u)$, $x(0) = x_0$. With $H = L + \lambda^T f$ and $u^*(x, \lambda) = \arg\min_u H(x, u, \lambda)$, the maximum principle gives the canonical equations

$$\dot x = H_\lambda(x, u^*, \lambda) = f(x, u^*), \qquad \dot\lambda = -H_x(x, u^*, \lambda),$$

with $x(0) = x_0$ and $n$ end conditions from the [transversality conditions](/transversality-conditions/). Some cases:

| end condition | residual $R$ |
|---|---|
| free end, fixed $T$ | $\lambda(T) - \varphi_x(x(T))$ |
| fixed end $x(T) = x_T$ | $x(T) - x_T$ |
| free final time, added to one of the above | $H(T) + \varphi_t$, with $T$ as an extra unknown |

**Single shooting.** The unknowns are $s = \lambda(0) \in \mathbb{R}^n$, with $T$ added if the final time is free. Each $s$ defines an initial value problem, and the residual $R(s)$ is a function of $s$. Shooting solves $R(s) = 0$:

```pseudo id=main
INDIRECT-SHOOTING(canon, x0, R, s, T, N, tol)   ▷ s is the guess for λ(0), with T last if T is free
L1  repeat
L2      (x(T), λ(T)) ← RK4 with N steps on z' = canon(t, z) from z(0) = (x0, s)
L3      r ← R(x(T), λ(T), T)
L4      if ‖r‖ ≤ tol then return s
L5      J ← forward-difference Jacobian of r with respect to s
L6      solve J d = r and set s ← s - d
```

Line L2 uses the classical [Runge-Kutta method](/runge-kutta-methods/) with a fixed step. Line L5 costs one more integration for each unknown. After convergence, one more integration gives the state, the costate and the input $u^*(x(t), \lambda(t))$, and a quadrature state $\dot c = L(x, u^*)$ gives the cost.

**Why it works.** If $f$, $L$ and $u^*$ are $C^2$, the end point $(x(T), \lambda(T))$ is a $C^2$ function of $s$, so $R$ is $C^2$. The maximum principle says that a normal optimal solution gives a root of $R$. Near a root where the Jacobian is nonsingular, Newton's method converges quadratically, and a forward difference with step $h$ changes this only by an error of order $h$ in $J$. A root is only an extremal: it satisfies the necessary conditions, and second-order conditions or a comparison of costs must confirm that it is a minimum.

**Checks.** For a problem without explicit time dependence, $H$ is constant along an extremal, so its variation along the computed trajectory measures the integration error. A small perturbation $u^* + \varepsilon \phi$ of the input must change the cost only by $O(\varepsilon^2)$, and for a minimum it must not lower it.

## Classic examples

**A scalar problem solved by hand.** Minimize $\int_0^1 u^2\, dt + x(1)^2$ with $\dot x = u$, $x(0) = 1$, the example of the [optimal control problem](/optimal-control-problem/) page. Here $H = u^2 + \lambda u$, $u^* = -\lambda/2$, $\dot\lambda = 0$ and the residual is $\lambda(1) - 2x(1)$. With $\lambda(0) = s$, $x(1) = 1 - s/2$ and $R(s) = s - 2(1 - s/2) = 2s - 2$. This is linear, so one Newton step from any guess gives $s = 1$, $u = -1/2$, $x(1) = 1/2$ and the cost $1/4 + 1/4 = 1/2$. For a general horizon $T$ and start $x_0$, $R(s) = (1 + T)s - 2x_0$ and $\lambda(0) = 2x_0/(1 + T)$. The tests check this for random $x_0$ and $T$.

**Linear quadratic problems and the Riccati equation.** For $\dot x = A x + B u$ with the cost $\int_0^T (x^T Q x + u^T R u)\, dt$ and a free end, $u^* = -\tfrac12 R^{-1} B^T \lambda$, and the canonical equations are linear:

$$\begin{pmatrix} \dot x \\ \dot\lambda \end{pmatrix} = \begin{pmatrix} A & -\tfrac12 B R^{-1} B^T \\ -2Q & -A^T \end{pmatrix} \begin{pmatrix} x \\ \lambda \end{pmatrix}, \qquad \lambda(T) = 0.$$

So $R(s)$ is affine and Newton converges in one step. The solution is $\lambda(0) = 2 P(0) x_0$, where $P$ solves the Riccati differential equation $-\dot P = A^T P + P A + Q - P B R^{-1} B^T P$, $P(T) = 0$, of the [LQR problem](/lqr-problem/). For the double integrator ($\dot x_1 = x_2$, $\dot x_2 = u$) with $Q = I$, $R = 1$ and $T = 3$, $P(0) \approx \begin{pmatrix} 1.69441 & 0.96749 \\ 0.96749 & 1.69441 \end{pmatrix}$, and for $x_0 = (1, -0.5)$ shooting gives $\lambda(0) = (2.42133, 0.24058) = 2 P(0) x_0$. The tests compare shooting with a separate RK4 integration of the Riccati equation, and they agree to $10^{-8}$. As $T \to \infty$, $P(0)$ tends to $\begin{pmatrix} \sqrt3 & 1 \\ 1 & \sqrt3 \end{pmatrix}$, the solution of the [continuous algebraic Riccati equation](/continuous-algebraic-riccati-equation/).

**A nonlinear problem.** Minimize $\int_0^2 (x^2 + u^2)\, dt$ with $\dot x = \sin x + u$, $x(0) = 1$ and a free end. Then $H = x^2 + u^2 + \lambda(\sin x + u)$, $u^* = -\lambda/2$, and

$$\dot x = \sin x - \lambda/2, \qquad \dot\lambda = -2x - \lambda \cos x, \qquad \lambda(2) = 0.$$

From the guess $s = 0$ with $N = 400$ steps, Newton needs 8 steps and gives $\lambda(0) \approx 4.15956$, so $u(0) \approx -2.080$. Along the solution $H = x^2 - \lambda^2/4 + \lambda \sin x$ stays at 0.174668 to within $10^{-10}$, $x(2) \approx 0.41793$, and the cost is about 2.21587. The tests add a random smooth perturbation $\varepsilon\phi(t)$ to the input: the cost rises for $\varepsilon = \pm 0.1$, $0.3$ and $0.03$, and its derivative at $\varepsilon = 0$ is below $10^{-4}$.

**A free final time.** Minimize $\int_0^T (1 + u^2)\, dt$ with $\dot x = u$, $x(0) = 1$, $x(T) = 0$ and $T$ free, the example of the [transversality conditions](/transversality-conditions/) page. Here $\lambda$ is constant, $u^* = -\lambda/2$ and $H = 1 - \lambda^2/4$. The unknowns are $(\lambda(0), T)$ and the residual is $(x(T), H(T)) = (1 - \lambda T/2, 1 - \lambda^2/4)$. From the guess $(1.5, 0.7)$ Newton needs 4 steps to reach $(2, 1)$: $u = -1$ and $T = 1$.

**A bang-bang problem with a known structure.** Steer the double integrator from $(1, 0)$ to the origin in minimum time with $|u| \le 1$ (see [time-optimal control](/time-optimal-control/)). With $H = 1 + \lambda_1 x_2 + \lambda_2 u$, $\lambda_1$ is constant, $\lambda_2(t) = \lambda_2(0) - \lambda_1 t$ and $u = -\operatorname{sgn}\lambda_2$. Here $u^*$ is not smooth, so it is better to fix the structure (one switch, from $-1$ to $+1$) and use the switch time $t_1$ and $T$ as unknowns, with the conditions $x(T) = 0$. They give $t_1 = 1$ and $T = 2$. The costate follows from $\lambda_2(t_1) = 0$ and $H(0) = 1 - |\lambda_2(0)| = 0$: $\lambda(0) = (1, 1)$.

## Variations

- **Multiple shooting** (Bulirsch 1971). Split $[0, T]$ into $m$ intervals, take the state and the costate at each node as unknowns, and add continuity conditions at the nodes. The system is larger but sparse, and each integration covers only $T/m$, so the growth that ruins single shooting (see Pitfalls) falls from about $e^{\mu T}$ to $e^{\mu T/m}$. Stoer and Bulirsch (Section 7.3) describe it, and it is the standard indirect solver for hard trajectory problems.
- **Exact Jacobians.** Integrate the variational equations $\dot\Phi = (\partial\, \mathrm{canon}/\partial z)\Phi$ next to $z$, or use [automatic differentiation](/automatic-differentiation/), in place of the forward differences of line L5. This removes the error of order $h$ and costs about the same.
- **Damped Newton.** Take $s \leftarrow s - \alpha d$ with $\alpha \le 1$ chosen so that $\|R\|$ decreases. This widens the region of convergence, but it does not make it global.
- **Continuation.** Solve an easy problem first, for example with a large weight on $u^2$, a short horizon, or a smoothed version of a bang-bang problem, and then change the parameter in small steps. Each solution is the guess for the next one. This is [homotopy continuation](/homotopy-continuation/) applied to $R(s; \theta) = 0$. Trélat (2012) describes its use for aerospace problems.
- **Collocation of the boundary value problem.** Solve the canonical equations with a [collocation method](/collocation-method/) for boundary value problems in place of shooting. Collocation does not integrate across the whole interval, so it does not suffer from the growth problem.
- **Gradient methods in function space.** Integrate the state forward with the current input, the costate backward from its end condition, and change the input in the direction $-H_u$ (Kirk, Chapter 6). This is [gradient descent](/gradient-descent/) on the cost. It needs no guess of the costate and converges from far away, but slowly. It is often used to get a guess for shooting.
- **Direct and indirect methods together.** A direct method gives a rough solution and estimates of the costate from the multipliers of the discretized problem. Shooting then refines this to high accuracy (von Stryk and Bulirsch 1992).

## Pitfalls

- **Growth of the sensitivity.** The canonical equations are a [Hamiltonian system](/hamiltonian-systems/), so the eigenvalues of their linearization come in pairs $\pm\mu$, and some solutions grow like $e^{|\mu| T}$. For $\dot x = x + u$ with the cost $\int (x^2 + u^2)\, dt$, the canonical matrix $M = \begin{pmatrix} 1 & -1/2 \\ -2 & -1 \end{pmatrix}$ has $M^2 = 2I$, and $\partial\lambda(T)/\partial\lambda(0) = \cosh(\sqrt2 T) - \sinh(\sqrt2 T)/\sqrt2$. This is 0.81 at $T = 1$, 172 at $T = 5$, $2.0 \cdot 10^5$ at $T = 10$ and $2.8 \cdot 10^{11}$ at $T = 20$. The problem is linear, and the code needs 2 Newton steps at $T = 1$ and $T = 5$ (the second only removes the error of the forward differences). At $T = 10$ it needs 5, because the forward-difference Jacobian loses digits. It still gives $\lambda(0) = 4.8284271247$, which agrees with the infinite-horizon value $2(1 + \sqrt2)$ to $2 \cdot 10^{-11}$. At $T = 20$ a change of $s$ in its last bit changes $\lambda(20)$ by about $10^{-3}$, so the residual cannot be made small and single shooting fails. The tests check both cases. Use multiple shooting or collocation for long horizons.
- **The first guess.** The costate has no direct physical meaning, so it is hard to guess, and the region in which Newton converges can be small. In the free-time example, the guess $(\lambda(0), T) = (-1, 0.7)$ sends Newton toward the other root $\lambda = -2$ of $H = 0$, which needs $T = -1$, and the integration fails when $T$ becomes negative.
- **An unknown structure.** If the true solution has a bang arc, a singular arc or an active state constraint that the formulation does not include, there is no root, or there is a root of the wrong problem. A switch inside a fixed integration step also lowers the order of RK4. Find the structure with a direct method first, and then use switch times as unknowns.
- **Abnormal and singular cases.** The template assumes $\lambda_0 = 1$ and a smooth $u^*(x, \lambda)$. On a [singular arc](/singular-arc/) the minimum condition does not give $u$, and the arc needs its own conditions.
- **Necessary is not sufficient.** A root of $R$ can be a maximum, a saddle or a local minimum that is not global. Compare the cost with other candidates, test perturbations, or check second-order conditions.
- **The scaling of the costate.** The costate can be many orders of magnitude larger or smaller than the state. Scale the variables so that the Newton system is well conditioned and the stopping test means the same in every component.

## Exercises

1. For $\dot x = u$ with the cost $\int_0^T u^2\, dt + x(T)^2$, show that $R(s) = (1 + T)s - 2x_0$ and that Newton converges in one step from any guess.
2. For the LQ problem, show that the canonical equations are linear, so that $R$ is affine in $s$, and that $\lambda(t) = 2P(t)x(t)$ satisfies them if $P$ solves the Riccati differential equation with $P(T) = 0$.
3. For $\dot x = x + u$ with the cost $\int_0^T (x^2 + u^2)\, dt$ and a free end, show that $M^2 = 2I$, $e^{MT} = \cosh(\sqrt2 T) I + \sinh(\sqrt2 T) M/\sqrt2$, and $\lambda(0) = \sqrt2 \tanh(\sqrt2 T) x_0 / (1 - \tanh(\sqrt2 T)/\sqrt2)$. Show that this tends to $2(1 + \sqrt2)x_0$ as $T \to \infty$. (For $T = 1$ and $x_0 = 1$ it is 3.37900.)
4. In the free-time example, find both roots of $H = 0$ and show that only $\lambda = 2$ gives $T > 0$.
5. For the time-optimal double integrator from $(1, 0)$, check that $\lambda(0) = (1, 1)$, $t_1 = 1$ and $T = 2$ satisfy $x(T) = 0$, $\lambda_2(t_1) = 0$ and $H \equiv 0$.
6. Explain why multiple shooting with $m$ equal intervals reduces the growth factor of the previous Pitfall from about $e^{\sqrt2 T}$ to $e^{\sqrt2 T/m}$, and estimate the $m$ needed for $T = 20$ if each interval may have a growth of at most $10^3$. (Answer: $\sqrt2 \cdot 20/m \le \ln 10^3$ gives $m \ge 5$.)

## References
