---
tag: CVGADP
kind: technique
slug: economic-mpc
name: Economic MPC
aliases:
- economic model predictive control
area: control/optimal-and-predictive-control
level: research
summary: MPC whose cost is a general economic objective, not a distance to a setpoint, with stability shown by dissipativity.
prereqs: [model-predictive-control, mpc-stability-theorem, dissipativity, lyapunov-function]
see_also: [nonlinear-mpc, linear-mpc, stochastic-mpc, recursive-feasibility, lagrangian-duality, kkt-conditions, optimal-control-problem, input-to-state-stability]
sources:
  - paper: "Moritz Diehl, Rishi Amrit and James B. Rawlings, A Lyapunov function for economic optimizing model predictive control, IEEE Transactions on Automatic Control 56, 703-707, 2011"
    locator: the rotated cost and the Lyapunov function for economic MPC with a terminal equality constraint under strong duality of the steady state problem
  - paper: "David Angeli, Rishi Amrit and James B. Rawlings, On average performance and stability of economic model predictive control, IEEE Transactions on Automatic Control 57(7), 1615-1626, 2012"
    locator: the bound on the closed loop average cost, and asymptotic stability under strict dissipativity
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: the section on economic MPC, with dissipativity and the rotated cost
---

Economic MPC is [model predictive control](/model-predictive-control/) whose stage cost $\ell(x, u)$ is a direct economic measure, such as energy use, raw material cost or lost product, and not a weighted distance to a setpoint. Standard MPC first computes the best steady state and then tracks it with a positive definite cost. Economic MPC optimizes the economic cost along the whole transient, which can earn more on the way. The price is that the usual stability proof breaks: the economic cost is not zero at the steady state and not positive elsewhere, so the optimal value is not a Lyapunov function. The fix is strict [dissipativity](/dissipativity/). If a storage function exists, the cost rotated by it is positive definite, the rotated problem has the same solutions, and the rotated optimal value is a Lyapunov function. Without dissipativity, economic MPC still keeps the average cost no worse than the best steady state, but the closed loop may never settle.

## In plain words

Ordinary predictive control is told where to go and is paid for staying close. Economic predictive control is told what costs money and is left to find the best way to run. Often the best long-run choice is still to settle at one operating point, and then the controller finds it on its own and saves money on the way there. But it does not always settle. Sometimes cycling between two points is cheaper than any single point, and then the controller cycles. To prove that it settles, one shows that the cost, after adding a fixed correction that depends on the state, rewards closeness to the best point. That correction does not change which plan is best, so the controller behaves like an ordinary one with a hidden target.

## When it applies

- A plant $x^+ = f(x, u)$ with constraints $(x, u) \in \mathbb{Z}$, and a stage cost $\ell(x, u)$ that measures money, energy or another real quantity.
- The best steady state $(x_s, u_s)$, the solution of $\min \ell(x, u)$ subject to $x = f(x, u)$ and $(x, u) \in \mathbb{Z}$, exists, with value $\ell_s = \ell(x_s, u_s)$.
- For stability at $x_s$: the system is strictly dissipative with respect to the supply rate $\ell(x, u) - \ell_s$. That is, there is a storage function $\lambda$ and a positive definite function $\rho$ with
$$\lambda(f(x, u)) - \lambda(x) \le \ell(x, u) - \ell_s - \rho(|x - x_s|) \quad \text{for all } (x, u) \in \mathbb{Z}.$$
- For the average cost bound alone, no dissipativity is needed.

For a linear plant with a strictly convex cost, a linear storage $\lambda(x) = \lambda^T x$ from the multiplier of the steady state problem works when that problem has strong duality, as shown by Diehl, Amrit and Rawlings (2011).

## The template

1. **Steady state.** Solve the steady state problem for $(x_s, u_s)$ and $\ell_s$, and keep its multiplier $\lambda$ of the constraint $x = f(x, u)$.
2. **Problem.** At the measured $x$, solve
$$V_N(x) = \min_{u_0, \dots, u_{N-1}} \sum_{k=0}^{N-1} \ell(x_k, u_k) \quad \text{s.t.} \quad x_0 = x, \ x_{k+1} = f(x_k, u_k), \ (x_k, u_k) \in \mathbb{Z}, \ x_N = x_s.$$
A terminal region with a terminal cost $V_f$ and a local controller $\kappa_f$ can replace $x_N = x_s$, with the condition $V_f(f(x, \kappa_f(x))) \le V_f(x) - \ell(x, \kappa_f(x)) + \ell_s$.
3. **Apply and repeat.** Apply $u_0$ and solve again at the next sample.
4. **Check dissipativity** to know whether the loop settles at $x_s$. Form the rotated cost
$$L(x, u) = \ell(x, u) - \ell_s + \lambda(x) - \lambda(f(x, u)),$$
and check that $L(x, u) \ge \rho(|x - x_s|)$.

**Why it works.**

*Average cost.* Let $u^*$ solve the problem at $x$. The shifted sequence with $u_s$ appended is feasible at $x^+ = f(x, u^*_0)$, because $x^*_N = x_s$ and $u_s$ keeps it there. Its cost is $V_N(x) - \ell(x, u^*_0) + \ell_s$. So
$$V_N(x^+) \le V_N(x) - \ell(x, u_0) + \ell_s.$$
Summing over $T$ samples gives $\sum_{t<T} (\ell(x_t, u_t) - \ell_s) \le V_N(x_0) - V_N(x_T)$. If $V_N$ is bounded below on the feasible set, for example because $\mathbb{Z}$ is compact, the average cost of the closed loop is at most $\ell_s$ in the limit. This holds with or without dissipativity (Angeli, Amrit and Rawlings 2012).

*Stability.* Sum the rotated cost along any feasible sequence. The storage terms telescope:
$$\sum_{k=0}^{N-1} L(x_k, u_k) = \sum_{k=0}^{N-1} \ell(x_k, u_k) - N \ell_s + \lambda(x_0) - \lambda(x_N).$$
With $x_N = x_s$ fixed, the right side is the economic cost plus a term that depends only on $x_0$. So the rotated problem and the economic problem have the same minimizers, and the controller is the same. The rotated stage cost is positive definite around $x_s$, and the rotated problem is a standard MPC problem with a terminal equality constraint. By the [MPC stability theorem](/mpc-stability-theorem/), its optimal value $\tilde V_N(x) = V_N(x) - N \ell_s + \lambda(x) - \lambda(x_s)$ is a Lyapunov function, and $x_s$ is asymptotically stable for the closed loop.

**What is not proved here.** For nonlinear plants, finding a storage function is in general hard, and there is no general recipe. Without a terminal constraint, stability needs a turnpike property and holds only near $x_s$ for long horizons. Strict dissipativity is close to necessary: Müller, Angeli and Allgöwer showed that it is needed for optimal steady state operation under a controllability condition. These results are cited and not proved here.

## Classic examples

**A dissipative scalar plant.** Take $x^+ = 0.5 x + u$ and $\ell(x, u) = x^2 + (u - 1)^2$. The cost wants $x = 0$ and $u = 1$, which is not a steady state. Steady states satisfy $u = 0.5 x$, and $\min x^2 + (0.5 x - 1)^2$ gives $x_s = 0.4$, $u_s = 0.2$ and $\ell_s = 0.8$. The multiplier is $\lambda = -1.6$, and with $\lambda(x) = -1.6 x$,
$$L(x, u) = x^2 + (u - 1)^2 - 0.8 - 1.6 x + 1.6 (0.5 x + u) = (x - 0.4)^2 + (u - 0.2)^2.$$
So the plant is strictly dissipative, and economic MPC with $x_N = x_s$ is exactly tracking MPC with the cost $(x - 0.4)^2 + (u - 0.2)^2$. With $N = 3$ from $x_0 = 2$, the first plan is $u = (-87/385, \ 37/385, \ 61/385)$, and the closed loop goes through $x = 2, 0.7740, 0.4874, 0.4204, 0.4048, 0.4011$ toward $0.4$. With $N = 5$ the states differ from these by less than $0.002$. The economic and the rotated problem give exactly the same inputs at every sample.

**A plant that prefers to cycle.** Take $x^+ = u$, $\ell(x, u) = x u$ and $|u| \le 1$. Steady states have $u = x$ and cost $x^2$, so the best steady state is $x_s = 0$ with $\ell_s = 0$. But the cycle $1, -1, 1, \dots$ with $u = -x$ costs $-1$ at every step. With $x_N = 0$ and $N = 4$, the plan from $x_0 = 1$ is $u = (-1, 1, -1, 0)$, with cost $-3$. The closed loop applies only $-1$ and plans again, so it alternates between $1$ and $-1$ for ever with average cost $-1 < \ell_s$. Even from $x_0 = 0$ the first input is $\pm 1$, with plan cost $-2$: the controller leaves the best steady state. The terminal constraint is met by every plan but never reached, and the average bound holds, but $x_s$ is not stable. No storage function exists, since along the cycle the dissipation inequality would sum to $0 \le -2$.

**Process control.** In chemical plants, the economic cost is the price of feed and energy minus the value of product. Economic MPC can exploit cheap periods of energy or move the plant to a better operating point faster than a two-layer scheme of steady state optimization and tracking control.

## Variations

- **Terminal region and cost.** Replace $x_N = x_s$ by a terminal set and cost, which enlarges the feasible set.
- **No terminal ingredients.** Use a long horizon and rely on the turnpike property, under which optimal open loop trajectories stay near $x_s$ for most of the horizon.
- **Periodic operation.** If a periodic orbit is optimal, replace the steady state by that orbit, with a periodic terminal constraint and dissipativity with respect to the orbit.
- **Average constraints.** Constrain the average of some quantity over time, such as emissions, instead of each value.
- **Regularized economic MPC.** Add a small tracking term to the economic cost so that the rotated cost becomes positive definite, at a small loss of economic performance.
- **Uncertainty.** Combine with [stochastic MPC](/stochastic-mpc/) for expected economic costs.

## Pitfalls

- **Assuming that it settles.** Without strict dissipativity the loop can cycle or wander, as in the second example. Check the storage function before relying on convergence.
- **A wrong steady state.** The terminal constraint uses $x_s$. If it is not the best steady state, the average bound refers to the wrong value.
- **Nonconvex costs.** Economic costs are often linear or nonconvex in the inputs, which can make the problem harder and the inputs jump between bounds.
- **Short horizons without terminal constraints.** With a short horizon, the controller can greedily use up resources at the end of the horizon, and the closed loop can be worse than steady operation.
- **Model error.** Economic optimization pushes the plant toward its constraints, where model errors matter most. Add back off from the constraints.

## Exercises

1. Find the best steady state of $x^+ = 0.5 x + u$ with $\ell = x^2 + (u - 1)^2$. (Answer: $u = 0.5 x$, and $\frac{d}{dx}(x^2 + (0.5 x - 1)^2) = 2.5 x - 1 = 0$ gives $x_s = 0.4$, $u_s = 0.2$ and $\ell_s = 0.8$.)
2. In exercise 1, verify that $\lambda(x) = -1.6 x$ makes the rotated cost $(x - 0.4)^2 + (u - 0.2)^2$. (Answer: $\ell - 0.8 - 1.6 x + 0.8 x + 1.6 u = x^2 - 0.8 x + u^2 - 0.4 u + 0.2$, which is the given square sum.)
3. Show that the plant $x^+ = u$ with $\ell = x u$ and $|u| \le 1$ is not dissipative with respect to $\ell - \ell_s$ at $x_s = 0$. (Answer: the inequality for $(x, u) = (1, -1)$ and $(-1, 1)$ gives $\lambda(-1) - \lambda(1) \le -1$ and $\lambda(1) - \lambda(-1) \le -1$, whose sum is $0 \le -2$.)
4. Show that with $x_N = x_s$, the economic and the rotated problems have the same minimizers. (Answer: the sums differ by $N \ell_s - \lambda(x_0) + \lambda(x_s)$, which does not depend on the inputs.)
5. Derive the average cost bound from $V_N(x^+) \le V_N(x) - \ell(x, u) + \ell_s$. (Answer: sum over $T$ samples, divide by $T$, and use that $V_N$ is bounded on the feasible set, so $(V_N(x_0) - V_N(x_T))/T \to 0$.)

## References
