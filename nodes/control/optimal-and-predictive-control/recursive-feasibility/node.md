---
tag: ATXJ8G
kind: definition
slug: recursive-feasibility
name: Recursive feasibility
aliases:
- persistent feasibility
area: control/optimal-and-predictive-control
level: advanced
summary: An MPC scheme is recursively feasible if feasibility of its problem at one time implies feasibility at the next.
prereqs: [model-predictive-control, control-invariant-set]
see_also: [mpc-stability-theorem, linear-mpc, positively-invariant-set, maximal-positively-invariant-set, tube-mpc, min-max-mpc, reference-governor, explicit-mpc]
sources:
  - paper: doi:10.1016/S0005-1098(99)00214-9
    title: D. Q. Mayne, J. B. Rawlings, C. V. Rao and P. O. M. Scokaert, Constrained model predictive control, stability and optimality, Automatica 36(6), 789-814, 2000
    locator: the terminal set conditions and the feasibility of the shifted control sequence at the next sampling instant
  - paper: doi:10.1109/9.751369
    title: P. O. M. Scokaert, D. Q. Mayne and J. B. Rawlings, Suboptimal model predictive control (feasibility implies stability), IEEE Transactions on Automatic Control 44(3), 648-654, 1999
    locator: the use of the shifted feasible sequence as a warm start, and stability without optimality
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: Chapter 2, regulation, the feasible set of the MPC problem and its invariance under the MPC law
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapter on receding horizon control, with the feasibility and stability of constrained linear MPC
---

Recursive feasibility is the property of a [model predictive control](/model-predictive-control/) scheme that the optimization problem, once feasible, stays feasible at every later sampling instant. MPC solves a constrained problem from the current state at each instant. If the problem has no solution, the controller has no input to apply. Feasibility at the start is not enough: a plan that meets the limits for $N$ steps can lead the state to a point from which no plan meets them. Recursive feasibility rules this out for the nominal model. The usual way to get it is a [control invariant](/control-invariant-set/) terminal set. It is also the first half of the proof of the [MPC stability theorem](/mpc-stability-theorem/).

## Definition

Consider the MPC problem $\mathbb{P}_N(x)$ for the model $x_{k+1} = f(x_k, u_k)$, with the constraints $(x_i, u_i) \in \mathbb{Z}$ for $i < N$ and the terminal constraint $x_N \in \mathbb{X}_f$. Let $\mathcal{X}_N$ be its feasible set, the set of states $x$ for which $\mathbb{P}_N(x)$ has a feasible input sequence, and let $\kappa_N(x)$ be the MPC law.

The MPC scheme is **recursively feasible** if

$$x \in \mathcal{X}_N \implies f(x, \kappa_N(x)) \in \mathcal{X}_N.$$

In other words, $\mathcal{X}_N$ is a [positively invariant set](/positively-invariant-set/) of the closed loop $x_{k+1} = f(x_k, \kappa_N(x_k))$. Then a state that is feasible at time 0 stays feasible, and the constraints hold, for all time.

Two variants are common.

- **Strong recursive feasibility.** The implication holds for every feasible first input, not only for the optimal one: $f(x, u_0) \in \mathcal{X}_N$ for every feasible sequence $(u_0, \dots, u_{N-1})$. Then the property does not depend on the cost or on the accuracy of the solver.
- **Robust recursive feasibility.** For $x_{k+1} = f(x_k, u_k, w_k)$ with $w_k \in \mathbb{W}$, the implication holds for every disturbance: $f(x, \kappa_N(x), w) \in \mathcal{X}_N$ for all $w \in \mathbb{W}$.

**The standard sufficient condition (theorem).** Suppose $\mathbb{X}_f$ is control invariant with a local law $\kappa_f$: for each $x \in \mathbb{X}_f$, $(x, \kappa_f(x)) \in \mathbb{Z}$ and $f(x, \kappa_f(x)) \in \mathbb{X}_f$. Then the scheme is strongly recursively feasible. Proof: let $(u_0, \dots, u_{N-1})$ be feasible from $x$, with states $x_0 = x, x_1, \dots, x_N \in \mathbb{X}_f$. From $x_1 = f(x, u_0)$ the shifted sequence $(u_1, \dots, u_{N-1}, \kappa_f(x_N))$ is feasible: the first $N - 1$ steps are the old ones, the step from $x_N$ meets $\mathbb{Z}$, and it ends in $\mathbb{X}_f$. So $x_1 \in \mathcal{X}_N$. The same argument shows that $\mathcal{X}_N$ is control invariant and that $\mathcal{X}_{N} \subseteq \mathcal{X}_{N+1}$.

## Examples and non-examples

The examples use the scalar plant $x_{k+1} = 2 x_k + u_k$ with $|u| \le 1$, $|x| \le 5$, the stage cost $x^2 + u^2$ and $N = 1$. Its largest control invariant set is $[-1, 1]$ (see [control invariant set](/control-invariant-set/)).

- **Non-example: no terminal constraint.** With $\mathbb{X}_f = [-5, 5]$ and the terminal cost 0, the feasible set is $\mathcal{X}_1 = \{x : |x| \le 5,\ \exists |u| \le 1,\ |2x + u| \le 5\} = [-3, 3]$. The optimal input minimizes $u^2$ alone, so it is $u = 0$ whenever $|2x| \le 5$. From $x = 2$ this gives $x_1 = 4 \notin \mathcal{X}_1$: the problem at the next instant has no solution. No other input would help for long, because $2$ lies outside $[-1, 1]$: every admissible sequence from it leaves $[-5, 5]$ within 3 steps.
- **Example: a control invariant terminal set.** With $\mathbb{X}_f = [-1, 1]$, the feasible set is $\mathcal{X}_1 = \{x : \exists |u| \le 1,\ |2x + u| \le 1\} = [-1, 1]$, and every feasible input keeps the next state in it. The scheme is strongly recursively feasible, as the theorem says.
- **Example: linear MPC with the maximal positively invariant terminal set.** On the [linear MPC](/linear-mpc/) page the terminal set is the [maximal positively invariant set](/maximal-positively-invariant-set/) of the LQR closed loop inside the limits. It is control invariant with $\kappa_f(x) = -K x$, so the scheme is recursively feasible.
- **Non-example: a disturbance.** For $x_{k+1} = 2 x_k + u_k + w_k$ with $|w_k| \le 0.5$, the terminal set $[-1, 1]$ no longer works: from $x = 1$, the best input $u = -1$ gives $x_1 = 1 + w$, which can be $1.5$. The set $[-0.5, 0.5]$ is robust control invariant: from $|x| \le 0.5$ the input $u = -2x$ is admissible and gives $x_1 = w$. Robust schemes such as [tube MPC](/tube-mpc/) and [min-max MPC](/min-max-mpc/) build on such sets.
- **Soft constraints.** If the state constraints are replaced by penalties, the problem is feasible for every state. This gives recursive feasibility in a trivial way, at the price of possible constraint violations.

## Related definitions

- **Control invariant set** and **positively invariant set**: recursive feasibility says that $\mathcal{X}_N$ is positively invariant for the closed loop, and the standard condition makes it control invariant. See [control invariant set](/control-invariant-set/).
- **Feasible set.** $\mathcal{X}_N$ is the $N$-step controllable set to $\mathbb{X}_f$ inside the constraints. It is the domain of the MPC law.
- **Asymptotic stability of MPC.** Recursive feasibility makes the MPC law defined along the whole closed-loop trajectory; with a terminal cost that is a local control Lyapunov function, the optimal cost then decreases and the origin is asymptotically stable. See the [MPC stability theorem](/mpc-stability-theorem/).
- **Feasibility implies stability.** Scokaert, Mayne and Rawlings (1999) showed that an MPC that applies any feasible sequence with enough cost decrease, such as the shifted sequence of the proof above, is still stabilizing. So recursive feasibility also gives a warm start for the solver.
- **Constraint admissibility of a reference.** A [reference governor](/reference-governor/) keeps an existing loop recursively feasible by changing its setpoint, using a positively invariant set of the closed loop.

## References
