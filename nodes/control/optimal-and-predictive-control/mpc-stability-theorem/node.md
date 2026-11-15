---
tag: 3P4RVR
kind: theorem
slug: mpc-stability-theorem
name: Stability of MPC with terminal ingredients
aliases:
- terminal cost and terminal set theorem
area: control/optimal-and-predictive-control
level: advanced
summary: "Nominal MPC is recursively feasible and asymptotically stable if a local controller keeps the terminal set invariant within the constraints and the terminal cost falls by the stage cost under it."
history:
  year: 2000
  people: [D. Q. Mayne, J. B. Rawlings, C. V. Rao, P. O. M. Scokaert]
  note: "Mayne, Rawlings, Rao and Scokaert (2000) stated the terminal set and terminal cost conditions that cover the earlier stability results, among them the terminal equality constraint of Keerthi and Gilbert (1988)."
prereqs: [model-predictive-control, recursive-feasibility, control-lyapunov-function, asymptotic-stability]
see_also: [linear-mpc, maximal-positively-invariant-set, control-invariant-set, infinite-horizon-lqr, discrete-algebraic-riccati-equation, lyapunov-direct-method, nonlinear-mpc, tube-mpc]
sources:
  - paper: doi:10.1016/S0005-1098(99)00214-9
    title: D. Q. Mayne, J. B. Rawlings, C. V. Rao and P. O. M. Scokaert, Constrained model predictive control, stability and optimality, Automatica 36(6), 789-814, 2000
    locator: the stability conditions on the terminal set, the local controller and the terminal cost, and the decrease of the value function
  - paper: doi:10.1007/BF00938540
    title: S. S. Keerthi and E. G. Gilbert, Optimal infinite-horizon feedback laws for a general class of constrained discrete-time systems, stability and moving-horizon approximations, Journal of Optimization Theory and Applications 57(2), 265-293, 1988
    locator: the stability of moving horizon control with the terminal equality constraint for constrained nonlinear discrete-time systems
  - paper: doi:10.1109/9.751369
    title: P. O. M. Scokaert, D. Q. Mayne and J. B. Rawlings, Suboptimal model predictive control (feasibility implies stability), IEEE Transactions on Automatic Control 44(3), 648-654, 1999
    locator: the stability of MPC that applies a feasible, not optimal, sequence with a sufficient decrease of the cost
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: Chapter 2, regulation, the basic stability assumptions and the asymptotic stability of the origin for the MPC closed loop
---

The MPC stability theorem gives conditions on the terminal ingredients of a [model predictive control](/model-predictive-control/) problem, the terminal set and the terminal cost, under which the closed loop is safe and convergent. If the terminal set is invariant under a local controller that meets the constraints, and the terminal cost decreases along that controller by at least the stage cost, then the MPC problem stays feasible and the optimal cost is a Lyapunov function, so the origin is asymptotically stable with the whole feasible set as its region of attraction. The theorem is for the nominal case: the model is exact and there is no disturbance. Keerthi and Gilbert (1988) proved stability with the terminal equality constraint $x_N = 0$; Mayne, Rawlings, Rao and Scokaert (2000) stated the general conditions in this form.

## Statement

Consider $x_{k+1} = f(x_k, u_k)$ with the constraints $(x, u) \in \mathbb{Z}$, the stage cost $\ell$, the horizon $N \ge 1$, the terminal cost $V_f$ and the terminal set $\mathbb{X}_f$. The MPC problem is

$$V_N(x) = \min_{u_0, \dots, u_{N-1}} \sum_{i=0}^{N-1} \ell(x_i, u_i) + V_f(x_N) \quad \text{s.t.} \quad x_0 = x,\ x_{i+1} = f(x_i, u_i),\ (x_i, u_i) \in \mathbb{Z},\ x_N \in \mathbb{X}_f.$$

Let $\mathcal{X}_N$ be its feasible set and $\kappa_N(x) = u_0^*(x)$ the MPC law. Assume:

1. **Basic.** $f$, $\ell$ and $V_f$ are continuous, $f(0, 0) = 0$, $\ell(0, 0) = 0$, $V_f(0) = 0$, $\ell \ge 0$ and $V_f \ge 0$; $\mathbb{Z}$ and $\mathbb{X}_f$ are closed, the input part of $\mathbb{Z}$ is bounded, and $0 \in \mathbb{X}_f$. So the minimum exists for each $x \in \mathcal{X}_N$.
2. **Terminal set.** There is a local law $\kappa_f$ with $(x, \kappa_f(x)) \in \mathbb{Z}$ and $f(x, \kappa_f(x)) \in \mathbb{X}_f$ for all $x \in \mathbb{X}_f$. So $\mathbb{X}_f$ is a [control invariant set](/control-invariant-set/) inside the constraints.
3. **Terminal cost.** For all $x \in \mathbb{X}_f$,

$$V_f(f(x, \kappa_f(x))) - V_f(x) \le -\ell(x, \kappa_f(x)).$$

So $V_f$ is a local [control Lyapunov function](/control-lyapunov-function/) on $\mathbb{X}_f$ with decrease at least $\ell$.

4. **Bounds.** There are class $\mathcal{K}_\infty$ functions $\alpha_1, \alpha_2$ with $\ell(x, u) \ge \alpha_1(|x|)$ for all $(x, u) \in \mathbb{Z}$ and $V_N(x) \le \alpha_2(|x|)$ for all $x \in \mathcal{X}_N$.

Then, for the nominal closed loop $x_{k+1} = f(x_k, \kappa_N(x_k))$:

- **(a) Recursive feasibility.** $x \in \mathcal{X}_N$ implies $f(x, \kappa_N(x)) \in \mathcal{X}_N$.
- **(b) Decrease.** $V_N(f(x, \kappa_N(x))) \le V_N(x) - \ell(x, \kappa_N(x))$ for all $x \in \mathcal{X}_N$.
- **(c) Stability.** The origin is asymptotically stable with the region of attraction $\mathcal{X}_N$. If moreover $\alpha_1(r) = c_1 r^a$ and $\alpha_2(r) = c_2 r^a$, it is exponentially stable on $\mathcal{X}_N$.

The upper bound in assumption 4 holds, for example, when $V_f(x) \le \alpha_f(|x|)$ on $\mathbb{X}_f$ and $\mathcal{X}_N$ is bounded; for linear MPC with a quadratic cost, a bounded feasible set and 0 in the interior of $\mathbb{X}_f$, it holds with $\alpha_2(r) = c_2 r^2$.

## In plain words

At the end of each plan, the state must be in a safe zone where a simple known controller can take over, keep the state in the zone and meet all limits. The end cost must be at least what that simple controller would still pay. Under these two rules, yesterday's plan, cut at the front and extended at the end by the simple controller, is a valid plan for today. Its cost is lower than yesterday's best cost by at least the cost of the step just taken. Today's best plan is at least as good, so the best cost falls at every step by an amount that is positive away from the target. A quantity that always falls and is zero only at the target works like an energy, and the state goes to the target.

## Proof

Fix $x \in \mathcal{X}_N$ with the optimal inputs $u_0^*, \dots, u_{N-1}^*$ and states $x_0^* = x, x_1^*, \dots, x_N^* \in \mathbb{X}_f$. Let $x^+ = f(x, u_0^*) = x_1^*$.

**(a)** Take the shifted sequence $\tilde u = (u_1^*, \dots, u_{N-1}^*, \kappa_f(x_N^*))$ from $x^+$. Its states are $x_1^*, \dots, x_N^*$ and then $f(x_N^*, \kappa_f(x_N^*))$. The first $N - 1$ steps meet $\mathbb{Z}$ because the old plan did. By assumption 2 the last step meets $\mathbb{Z}$ and ends in $\mathbb{X}_f$. So $\tilde u$ is feasible and $x^+ \in \mathcal{X}_N$.

**(b)** The cost of $\tilde u$ is

$$J(x^+, \tilde u) = V_N(x) - \ell(x, u_0^*) + \Big[\ell(x_N^*, \kappa_f(x_N^*)) + V_f\big(f(x_N^*, \kappa_f(x_N^*))\big) - V_f(x_N^*)\Big].$$

The stage costs of steps $1$ to $N-1$ are shared; the first stage cost is removed; the old terminal cost is replaced by one more stage cost and a new terminal cost. By assumption 3 the bracket is at most 0. Since $V_N(x^+)$ is the minimum, $V_N(x^+) \le J(x^+, \tilde u) \le V_N(x) - \ell(x, \kappa_N(x))$.

**(c)** By assumption 4, $\alpha_1(|x|) \le \ell(x, \kappa_N(x)) \le V_N(x) \le \alpha_2(|x|)$ on $\mathcal{X}_N$, where the middle inequality holds because all terms of $V_N$ are nonnegative by assumption 1. With (b), $V_N(x^+) - V_N(x) \le -\alpha_1(|x|)$. So $V_N$ is a Lyapunov function on the positively invariant set $\mathcal{X}_N$, and the discrete-time [Lyapunov theorem](/lyapunov-direct-method/) gives asymptotic stability with this region of attraction. Directly: summing (b) along the trajectory gives $\sum_{k \ge 0} \alpha_1(|x_k|) \le V_N(x_0) < \infty$, so $x_k \to 0$; and $\alpha_1(|x_k|) \le V_N(x_k) \le V_N(x_0) \le \alpha_2(|x_0|)$ gives Lyapunov stability. In the power case, $V_N(x^+) \le (1 - c_1/c_2) V_N(x)$, which gives exponential decay. $\square$

## Consequences

- **Linear MPC is stabilizing (theorem).** For $f(x, u) = A x + B u$, $\ell = x^T Q x + u^T R u$ with $Q, R > 0$, take $V_f(x) = x^T P x$ with $P$ from the [discrete algebraic Riccati equation](/discrete-algebraic-riccati-equation/), $\kappa_f(x) = -K x$ the [LQR](/infinite-horizon-lqr/) gain, and $\mathbb{X}_f$ the [maximal positively invariant set](/maximal-positively-invariant-set/) of $A - B K$ inside the state limits and $-K x \in \mathbb{U}$. Then assumption 3 holds with equality, $V_f(x^+) - V_f(x) = -x^T (Q + K^T R K) x$, and the [linear MPC](/linear-mpc/) closed loop is exponentially stable on $\mathcal{X}_N$. In the example of that page the optimal cost from $(-5, 3)$ falls as $48.94, 14.03, 2.706, 0.2906, 0.0205$.
- **Terminal equality constraint.** $\mathbb{X}_f = \{0\}$, $V_f = 0$ and $\kappa_f = 0$ meet assumptions 2 and 3 because $f(0, 0) = 0$. This is the setting of Keerthi and Gilbert (1988). The feasible set is then the set of states that can reach 0 in $N$ steps, which is often small, and the solver must meet an equality exactly.
- **Performance bound.** Summing (b) gives $\sum_{k \ge 0} \ell(x_k, \kappa_N(x_k)) \le V_N(x_0)$: the infinite-horizon cost of the closed loop is at most the predicted cost. Also $V_N \ge V_\infty$, the optimal infinite-horizon cost, because $V_f$ is an upper bound on the cost to go under $\kappa_f$.
- **Larger horizons help.** Under assumption 2, $\mathcal{X}_N \subseteq \mathcal{X}_{N+1}$, and under assumption 3, $V_{N+1} \le V_N$ on $\mathcal{X}_N$. A longer horizon gives a larger region of attraction and a cost closer to $V_\infty$.
- **Suboptimal MPC.** The proof uses only the cost of the shifted sequence. So any feasible sequence whose cost is at most that of the shifted one gives the same decrease; Scokaert, Mayne and Rawlings (1999) built suboptimal MPC on this idea, and it also gives a warm start for the solver.
- **Nonlinear MPC.** For a nonlinear $f$ whose linearization at 0 is stabilizable, a common choice is the LQR of the linearization as $\kappa_f$, a quadratic $V_f$ with a slightly larger weight, and a small sublevel set of $V_f$ as $\mathbb{X}_f$; see [nonlinear MPC](/nonlinear-mpc/).

## Tightness

- **Without the terminal cost the conclusion can fail.** For $x_{k+1} = 2 x_k + u_k$ with $\ell = x^2 + u^2$, no constraints, $N = 1$ and $V_f = 0$, the MPC law is $u = 0$, and the closed loop $x_{k+1} = 2 x_k$ is not Schur. Assumption 3 fails: no $\kappa_f$ makes $0 - 0 \le -\ell$ with $\ell > 0$.
- **A Lyapunov function is not enough as terminal cost.** In the same plant, take $\kappa_f(x) = -1.5\, x$, so the local loop is $x_{k+1} = 0.5\, x_k$, and $V_f(x) = \varepsilon x^2$ with $\mathbb{X}_f = \mathbb{R}$. $V_f$ decreases along $\kappa_f$ for every $\varepsilon > 0$. The MPC with $N = 1$ minimizes $x^2 + u^2 + \varepsilon (2x + u)^2$, which gives $u = -2 \varepsilon x / (1 + \varepsilon)$ and the closed loop $x_{k+1} = \frac{2}{1 + \varepsilon} x_k$. For $\varepsilon \le 1$ the origin is not asymptotically stable. Assumption 3 asks $\varepsilon (0.25 - 1) \le -(1 + 2.25)$, that is $\varepsilon \ge 13/3$, and then the closed loop factor is at most $0.375$.
- **The conditions are sufficient, not necessary.** MPC without terminal ingredients is often asymptotically stable when the horizon is long enough, as the example of the [model predictive control](/model-predictive-control/) page shows for $N = 3$. That needs a different argument.
- **Nominal only.** The theorem assumes an exact model and no disturbance. With a disturbance, the feasible set need not be invariant, and the decrease can fail. Robust versions use robust invariant sets and tightened constraints, as in [tube MPC](/tube-mpc/) and [min-max MPC](/min-max-mpc/).
- **Optimality is not needed, feasibility is.** If the solver returns a plan that is worse than the shifted plan, the decrease (b) can fail. The suboptimal version keeps the decrease by comparing with the shifted plan.

## History

Keerthi and Gilbert (1988) proved that moving horizon control of constrained nonlinear discrete-time systems with the terminal equality constraint $x_N = 0$ is stabilizing, and that it approximates the infinite-horizon law. Scokaert, Mayne and Rawlings (1999) showed that feasibility with enough cost decrease is sufficient, without optimality. The survey of Mayne, Rawlings, Rao and Scokaert (2000) stated the conditions on the terminal set, the local controller and the terminal cost in the form of this page, and showed that they cover the earlier results. The book of Rawlings, Mayne and Diehl presents the theorem with the bounds of assumption 4.

## References
