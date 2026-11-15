---
tag: 1PY7EN
kind: algorithm
slug: hybrid-mpc
name: Hybrid MPC
aliases:
- hybrid model predictive control
- mixed-integer MPC
area: control/discrete-event-and-hybrid-systems
level: research
summary: MPC for piecewise affine or mixed logical dynamical models, where each step is a mixed-integer quadratic or linear program.
model: real-ram
complexity:
  vars: {s: the number of modes, N: the horizon, m: the input dimension, n: the state dimension, c: the cost of one convex QP in N m variables}
  time: {worst: O(s^N (N^3 n m^2 + c))}
  space: {extra: O(N^2 m (n + m))}
properties: {deterministic: true, exact: true, online: true}
history:
  year: 1999
  people: [Alberto Bemporad, Manfred Morari]
  note: "Bemporad and Morari introduced mixed logical dynamical models in 1999 and showed that predictive control of these models is a mixed-integer quadratic or linear program at each sampling instant."
prereqs: [mixed-logical-dynamical-system, linear-mpc, mixed-integer-programming]
see_also: [mixed-logical-dynamical-system, piecewise-affine-system, model-predictive-control, explicit-mpc, mpc-stability-theorem, big-m-formulation, quadratic-programming, hybrid-automata]
sources:
  - paper: doi:10.1016/S0005-1098(98)00178-2
    title: "A. Bemporad and M. Morari, Control of systems integrating logic, dynamics, and constraints, Automatica 35(3), 1999, pages 407 to 427"
    locator: the MLD form, the predictive control law as a mixed-integer quadratic program, and its stability with a terminal equality constraint
  - book: isbn:978-1-107-01688-0
    title: "F. Borrelli, A. Bemporad and M. Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017"
    locator: "Chapter 16, Models of Hybrid Systems, and Chapter 17, Optimal Control of Hybrid Systems"
  - paper: doi:10.1109/TAC.2006.883059
    title: "M. Lazar, W. P. M. H. Heemels, S. Weiland and A. Bemporad, Stabilizing model predictive control of hybrid systems, IEEE Transactions on Automatic Control 51(11), 2006, pages 1813 to 1818"
    locator: terminal cost and terminal set conditions for the stability of hybrid MPC of PWA systems
  - paper: doi:10.1109/TCST.2004.824309
    title: "F. D. Torrisi and A. Bemporad, HYSDEL: a tool for generating computational hybrid models for analysis and synthesis problems, IEEE Transactions on Control Systems Technology 12(2), 2004, pages 235 to 249"
    locator: the modeling language that compiles a hybrid description into MLD form
  - paper: doi:10.1016/S0005-1098(01)00059-0
    title: "W. P. M. H. Heemels, B. De Schutter and A. Bemporad, Equivalence of hybrid dynamical models, Automatica 37(7), 2001, pages 1085 to 1091"
    locator: the equivalence of MLD, PWA and other hybrid model classes
---

Hybrid MPC is [model predictive control](/model-predictive-control/) for a plant whose model has both real states and discrete modes: a [piecewise affine system](/piecewise-affine-system/) or a [mixed logical dynamical system](/mixed-logical-dynamical-system/). At each sampling instant it measures the state, finds the input sequence and the mode sequence over a horizon of $N$ steps that minimize a cost under constraints, and applies the first input. With a quadratic cost the problem at each instant is a mixed-integer quadratic program (MIQP), and with a 1-norm or infinity-norm cost it is a mixed-integer linear program. Bemporad and Morari (1999) gave this formulation. For a fixed mode sequence the problem is a convex QP, as in [linear MPC](/linear-mpc/). The mode choice makes it nonconvex, and the worst case grows exponentially with $N$. The code on this page solves the problem exactly by enumeration of the $s^N$ mode sequences, which is the simplest correct method for small $s$ and $N$.

## In plain words

Some machines change their behavior when the state crosses a line: a valve opens, a contact closes, a gear shifts. Plan the next few moves of such a machine as a normal predictive controller does, but also plan which behavior it will have at each move. For one fixed list of behaviors, the best moves are easy to find, because the problem is smooth and bowl-shaped. So try every list of behaviors. Drop the lists that the machine cannot follow from where it is. Solve the easy problem for each list that is left, and keep the cheapest. Apply only the first move, measure again, and repeat. The number of lists grows very fast with the length of the plan, so real solvers prune the lists with branch and bound.

## The problem

The plant is a PWA system with modes $i = 1, \ldots, s$: $x^+ = A_i x + B_i u + f_i$ when $x$ is in the closed polyhedral cell $\mathcal{C}_i = \{x : H_i x \le h_i\}$. The cells cover the state set and meet only on their boundaries. At each sampling instant, with the measured state $x_0$, solve

$$\min_{U, \sigma} \; \sum_{k=0}^{N-1} \left(x_k^T Q x_k + u_k^T R u_k\right) + x_N^T P x_N$$

over the inputs $U = (u_0, \ldots, u_{N-1})$ and the mode sequence $\sigma = (\sigma_0, \ldots, \sigma_{N-1})$, subject to $x_{k+1} = A_{\sigma_k} x_k + B_{\sigma_k} u_k + f_{\sigma_k}$, $x_k \in \mathcal{C}_{\sigma_k}$, $u_{\min} \le u_k \le u_{\max}$ and $x_{\min} \le x_{k+1} \le x_{\max}$ for $k = 0, \ldots, N - 1$, with $Q, P \succeq 0$ and $R \succ 0$. Apply $u_0$. The MLD form writes the same problem with binary variables $\delta$ for the modes and [big-M](/big-m-formulation/) inequalities; Heemels, De Schutter and Bemporad (2001) showed that the two model classes are equivalent under mild conditions, see [mixed logical dynamical system](/mixed-logical-dynamical-system/).

## The algorithm

```pseudo id=main
HYBRID-MPC-STEP(modes, x0, N, Q, R, P, bounds)
L1  best ← None
L2  for each mode sequence sigma in {1, ..., s}^N do
L3      if x0 is not in cell(sigma_0) then continue
L4      write x_k = d_k + Gamma_k U for k = 0, ..., N under sigma
L5      solve the QP in U: cost (1/2) U^T H U + phi^T U, input bounds, state bounds, x_k in cell(sigma_k) for k = 1, ..., N - 1
L6      if the QP is feasible and its cost < cost(best) then best ← (U, sigma, cost)
L7  return best

CLOSED-LOOP(modes, x, steps)
    repeat steps times
        (U, sigma, J) ← HYBRID-MPC-STEP(modes, x, ...)
L8      u ← the first m entries of U
L9      x ← the true PWA step from x with input u
```

Line L4 is the condensing of linear MPC with a different $(A, B, f)$ at each step: $d_{k+1} = A_{\sigma_k} d_k + f_{\sigma_k}$ and $\Gamma_{k+1} = A_{\sigma_k} \Gamma_k + B_{\sigma_k} E_k$, where $E_k$ picks $u_k$ out of $U$. Substituting gives $\mathcal{H} = 2(\sum_k \Gamma_k^T W_k \Gamma_k + I_N \otimes R)$, which is positive definite. Line L5 uses the dual active set method of Goldfarb and Idnani: it starts at the unconstrained minimum, adds the most violated constraint, and drops an active constraint when its multiplier would become negative. It also reports an empty feasible set. A production solver replaces lines L2 to L6 by branch and bound on the binary variables of the MLD form (see [mixed-integer programming](/mixed-integer-programming/)). Each node of the tree solves a QP in which some $\delta$ are fixed and the others are relaxed to $[0, 1]$, and its value bounds every leaf below it. The code also contains this big-M MLD form of a PWA system, and the tests check that it accepts exactly the mode of each state.

## Example

Take two modes that rotate the state by $\pm \pi/3$ and stretch it by $\rho = 1.2$: $x^+ = \rho R(\pi/3) x + b u$ if $x_1 \ge 0$ (mode 1) and $x^+ = \rho R(-\pi/3) x + b u$ if $x_1 \le 0$ (mode 2), with $R(\theta)$ the rotation matrix and with $b = (0, 1)^T$. The open loop is unstable: from $(1, 1)$ with $u = 0$, $\|x\|_2 > 10$ after 15 steps. Use $N = 3$, $Q = P = I$, $R = 0.1$, $|u| \le 1$ and $|x_i| \le 10$, and start at $x_0 = (1, 0)$.

Line L2 visits $2^3 = 8$ sequences. The 4 sequences that start in mode 2 fail at line L3, because $x_1 = 1 > 0$. For mode 1 first, $x_1 = (0.6, 1.0392 + u_0)$ has the first entry $0.6 > 0$ for every input, so it is not in the cell of mode 2, and the sequences $(1, 2, 1)$ and $(1, 2, 2)$ give infeasible QPs at line L5. Two QPs are left, each with 3 variables, 6 input bounds, 12 state bounds and 2 cell rows.

| sequence | $U$ | cost | note |
|---|---|---|---|
| (1, 1, 1) | (-0.8270, -0.6812, -0.1698) | 1.5474 | states (1, 0), (0.6, 0.2122), (0.1395, 0.0697), (0.0113, 0.0170) |
| (1, 1, 2) | (-0.6928, -0.7938, -0.0205) | 1.5940 | $x_2 = (0.0, 0.0376)$ lies on the boundary of the two cells |

Line L7 returns $(1, 1, 1)$ and the controller applies $u_0 = -0.8270$. In closed loop from $(1, 1)$, the first input saturates at $-1$, and the state norm is below $10^{-4}$ after 15 steps, with all inputs and states inside their bounds. This is a measurement on this example, not a theorem: the problem has no terminal constraint.

## Correctness

For a fixed sequence $\sigma$, the states are affine in $U$, so the admissible inputs form a polyhedron and the cost is a strictly convex quadratic; line L5 gives its minimum. Every admissible pair $(U, \sigma)$ has its $\sigma$ in the loop of line L2, so the least of the QP minima is the minimum of the MIQP, and line L6 keeps it. The QP solver is the one step that the proof quotes rather than proves: Goldfarb and Idnani proved that their method stops at the optimum or detects infeasibility. The tests check the KKT conditions of its answers on random problems and compare with an enumeration of active sets. The full argument is in [the correctness proof](proofs/correctness.md). Closed-loop properties are separate theorems: Bemporad and Morari (1999) prove convergence to the equilibrium $x_e$ with the terminal constraint $x_N = x_e$ when the first problem is feasible, and Lazar et al. (2006) give conditions with a terminal cost and a terminal set for asymptotic stability in the sense of Lyapunov, as in the [MPC stability theorem](/mpc-stability-theorem/).

## Complexity

The model is the [real RAM](/real-ram/). Per sampling instant:

- **Enumeration (this code).** $s^N$ QPs. Each has $Nm$ variables, $2Nm$ input bounds, $2Nn$ state bounds and the cell rows of $x_1, \ldots, x_{N-1}$. Building $\Gamma_k$ and $\mathcal{H}$ costs $O(N^3 n m^2)$, and $c$ is the cost of the QP. The total is $O(s^N (N^3 n m^2 + c))$ time and $O(N^2 m (n + m))$ extra space.
- **Branch and bound on the MLD form.** One MIQP with $N(m + n s)$ real variables, $N s$ binary variables and the big-M rows. In the worst case it also explores $2^{Ns}$ leaves, since MIQP is [NP-hard](/np-hard/). In practice the relaxations prune most of the tree; how much depends on the model and the tightness of the big-M constants (rule of thumb, not a theorem).
- **Explicit hybrid MPC.** The optimal input is a piecewise affine function of $x_0$ on a partition that is not convex in general, computed offline by [multiparametric quadratic programming](/multiparametric-quadratic-programming/) for each mode sequence, or by dynamic programming (Borrelli, Bemporad and Morari 2017, Chapter 17). Online cost is a point location, but the number of regions can grow exponentially with $N$.

## Properties

- **Exact per instant.** Enumeration and complete branch and bound both return the global optimum of the MIQP, not a local one.
- **Online.** It solves one optimization per sampling instant, so the time to solve must fit in the sampling period.
- **Discontinuous control law.** The optimal input can jump when the optimal mode sequence changes, even for a continuous PWA system.
- **Same tuning as linear MPC.** $Q$, $R$, $P$, the horizon and the constraints have the same roles as in [linear MPC](/linear-mpc/).

## Variants and improvements

- **Linear costs.** With 1-norm or infinity-norm stage costs, each instant is a mixed-integer linear program, which mature MILP solvers handle well (Bemporad and Morari 1999).
- **Explicit hybrid MPC.** Precompute the control law offline, as in [explicit MPC](/explicit-mpc/), and store the regions; Borrelli, Bemporad and Morari (2017, Chapter 17) give the method.
- **Fewer sequences.** Restrict the mode sequences to those that the reachable sets of the PWA system allow, or fix the mode after a few steps (move blocking of the modes). This trades optimality for speed.
- **Stabilizing terminal ingredients.** Add a terminal equality constraint (Bemporad and Morari 1999) or a terminal cost and set (Lazar et al. 2006).
- **Modeling tools.** HYSDEL (Torrisi and Bemporad 2004) compiles a description with logic and real variables into MLD form.

## When to use it

Use it when the plant has real switching that a linear model cannot capture and the horizon is short enough for the solver: automotive traction and gear control, power converters, water and gas networks with valves, contact in robot locomotion (a related convex scheme is [convex MPC for legged locomotion](/convex-mpc-legged-locomotion/), which fixes the contact sequence in advance). If the mode sequence is known, fix it and use [linear MPC](/linear-mpc/) on a time-varying model. If the plant switches without control, and only robustness to the switching is needed, a [switched system](/switched-system/) analysis may be enough.

## Pitfalls

- **Boundaries of the cells (line L3).** With closed cells, a state on a shared boundary is admissible in both modes, and the optimizer may plan with a mode that the real system does not use there. Make the dynamics agree on the boundary, or make one cell open on it.
- **Exponential growth (line L2).** $s^N$ grows fast: 2 modes and $N = 20$ give about $10^6$ QPs. Enumeration is for small examples and tests only.
- **Loose big-M constants.** Big constants in the MLD form weaken the relaxations and slow branch and bound. Compute them from bounds on the states and inputs, as `pwa_to_mld` does.
- **No guarantee without terminal ingredients.** Without a terminal constraint or a terminal cost and set, the closed loop may lose feasibility or fail to converge, even if each instant is solved exactly.
- **Time limit.** A solver stopped early returns a feasible but suboptimal input; the stability arguments that assume the optimum then need a separate proof for suboptimal solutions.

## Implementations

## History

Sontag (1981) studied piecewise linear systems in discrete time. Bemporad and Morari (1999) introduced MLD models, which put logic, dynamics and constraints into mixed-integer linear inequalities, and formulated predictive control of these models as MIQP or MILP. Heemels, De Schutter and Bemporad (2001) showed that MLD, PWA and other hybrid model classes are equivalent under mild conditions, so results for one transfer to the others. Torrisi and Bemporad (2004) gave the HYSDEL language. Lazar, Heemels, Weiland and Bemporad (2006) gave stabilizing terminal conditions for PWA systems. Borrelli, Bemporad and Morari (2017) collected the theory, including explicit solutions, in a textbook.

## References
