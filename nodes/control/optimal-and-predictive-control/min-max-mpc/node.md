---
tag: SE9461
kind: algorithm
slug: min-max-mpc
name: Min-max MPC
aliases:
- min-max model predictive control
area: control/optimal-and-predictive-control
level: advanced
summary: Minimizes the worst case cost over all disturbance sequences in a bounded set, by open-loop or feedback min-max optimization.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, V: the number of vertices of the disturbance set, N: the horizon, L: "the number of variables and rows of the LP, of order V^N (n + m + q) for q rows of the constraints", I: the number of simplex pivots}
  time: {worst: "O(I L^2)"}
  space: {extra: "O(L^2)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1987
  people: [Pedro J. Campo, Manfred Morari]
  note: "Campo and Morari (1987) posed MPC as a minimization of the worst case cost over a set of models and solved the 1-norm and infinity-norm cases by linear programming. Scokaert and Mayne (1998) gave the feedback form on a tree of disturbance vertices."
prereqs: [linear-mpc, linear-programming-problem, simplex-method, positively-invariant-set]
see_also: [tube-mpc, stochastic-mpc, recursive-feasibility, control-invariant-set, explicit-mpc, model-uncertainty, h-infinity-control-problem, mpc-stability-theorem]
sources:
  - paper: doi:10.1109/ACC.1987.4172491
    title: Pedro J. Campo and Manfred Morari, Robust model predictive control, Proceedings of the American Control Conference, 1021-1026, 1987
    locator: the worst case formulation of MPC and its solution by linear programming for 1-norm and infinity-norm costs
  - paper: doi:10.1109/9.704989
    title: Pierre O. M. Scokaert and David Q. Mayne, Min-max feedback model predictive control for constrained linear systems, IEEE Transactions on Automatic Control 43(8), 1136-1142, 1998
    locator: the feedback min-max problem with one control per vertex sequence, and its feasibility and stability properties
  - paper: doi:10.1016/S0005-1098(99)00214-9
    title: David Q. Mayne, James B. Rawlings, Christopher V. Rao and Pierre O. M. Scokaert, Constrained model predictive control, stability and optimality, Automatica 36(6), 789-814, 2000
    locator: the section on robust MPC, with open-loop and feedback min-max formulations
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: the chapter on robust MPC
---

Min-max MPC is a form of [model predictive control](/model-predictive-control/) for a plant with a bounded disturbance. At each sample it solves a game: the controller picks the inputs, the disturbance picks the worst sequence in its set, and the controller minimizes that worst case cost subject to the constraints for every possible disturbance. In the open-loop form the inputs are a fixed sequence. In the feedback form each future input may depend on the disturbances seen so far, which is less conservative and can be feasible where the open-loop form is not. For a linear plant, a polytope of disturbances and 1-norm costs, the feedback problem is one linear program over a tree with one branch per vertex of the disturbance set, and it is exact for the whole polytope. Only the first input is applied, and the problem is solved again at the next sample.

## In plain words

Plan the next few moves as if an opponent controls the disturbance and always does the most harmful thing. Pick the plan whose worst outcome is the best, and make sure that every limit holds whatever the opponent does. A good plan says what to do after each move of the opponent, not one fixed list of moves, because you will see the disturbance before you act again. For a linear plant it is enough to plan against the corners of the disturbance set, since anything in between is a mix of corners. The price is size: the plan has a branch for every corner at every step, so the number of branches grows very fast with the horizon.

## The problem

Input: matrices $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, the vertices $w^1, \dots, w^V$ of the disturbance set $W$, a horizon $N$, weights $Q$, $R$, $P$, bounds $\bar x$, $\bar u$, a terminal set $X_f = \{x : F x \le f\}$, and the current state $x_0$.

The plant is $x_{k+1} = A x_k + B u_k + w_k$ with $w_k \in W$. The cost of one trajectory is

$$J = \sum_{k=0}^{N-1} \left(\|Q x_k\|_1 + \|R u_k\|_1\right) + \|P x_N\|_1.$$

Output: an input $u_0$ that is the first input of an optimal policy for

$$J^*(x_0) = \min_{\pi} \ \max_{w_0, \dots, w_{N-1} \in W} J \quad \text{subject to } |x_k| \le \bar x, \ |u_k| \le \bar u, \ x_N \in X_f \text{ for every disturbance sequence},$$

where the policy $\pi$ chooses $u_k$ as a function of $w_0, \dots, w_{k-1}$ (feedback form) or as a constant (open-loop form). If no policy meets the constraints, report that the problem is infeasible.

## The algorithm

```pseudo id=main
MIN-MAX-MPC(A, B, x₀, N, w¹..wⱽ, Q, R, P, x̄, ū, F, f)
L1   nodes ← all sequences s of vertex indices with |s| ≤ N            ▷ the scenario tree
L2   variables: x_s for each node, u_s for each inner node (feedback) or one u per depth (open loop)
L3   for each node s and vertex i: x_{s i} = A x_s + B u_s + wⁱ
L4   |x_s| ≤ x̄ at each node, |u_s| ≤ ū at each inner node, F x_ℓ ≤ f at each leaf ℓ
L5   t ≥ (cost along the path to ℓ) for each leaf ℓ, with each |·| as an epigraph variable
L6   solve the LP: minimize t subject to L3 to L5
L7   return t and u_() at the root
L8   at each sample: measure x, set x₀ ← x, run L1 to L7, apply u_()
```

Line L5 writes each absolute value $|a^T z|$ as a variable $s \ge 0$ with $s \ge a^T z$ and $s \ge -a^T z$, and bounds $t$ from below by the sum of these variables along each path. At the optimum each $s$ equals its absolute value, and $t$ equals the largest path cost. The code solves the LP with a two-phase [simplex method](/simplex-method/) and Bland's rule, in exact rational arithmetic when the data are rational.

The feedback form has a separate control at each inner node, so the input at depth $k$ can differ between branches that saw different disturbances. The open-loop form forces all nodes of one depth to share one control.

## Example

Take the scalar plant $x_{k+1} = 1.2\, x_k + u_k + w_k$ with $|w_k| \le 0.2$, so the vertices are $\pm 0.2$. The weights are $Q = 1$, $R = 0.1$, $P = 3$, the input bound is $|u| \le 1$, and the terminal set is $|x_N| \le 0.5$. The plant alone is unstable.

**From $x_0 = 0$ with $N = 2$.** In the feedback form, $u_0 = 0$, so $x_1 = \pm 0.2$. On the branch $x_1 = 0.2$ the second input is $u_1 = -0.24$, which cancels $1.2\, x_1$ and leaves $x_2 = \pm 0.2$; the other branch is the mirror image. The worst path cost is $0 + 0 + 0.2 + 0.024 + 3 \cdot 0.2 = 0.824 = 103/125$. In the open-loop form, $u_1$ must be the same on both branches, the best choice is $u_1 = 0$, and the worst final state is $1.2 \cdot 0.2 + 0.2 = 0.44$, so the value is $0.2 + 3 \cdot 0.44 = 1.52$. Feedback cuts the worst case cost by almost half.

| $x_0$, $N$ | feedback value | open-loop value | first input |
|---|---|---|---|
| $0$, $N = 1$ | $3/5$ | $3/5$ | $0$ |
| $0.5$, $N = 1$ | $29/25$ | $29/25$ | $-0.6$ |
| $0$, $N = 2$ | $103/125$ | $38/25$ | $0$ |
| $0.5$, $N = 2$ | $173/125$ | $52/25$ | $-0.6$ |
| $0$, $N = 3$ | $131/125$ | infeasible | $0$ |

**Where open loop fails.** With a fixed input sequence, the spread of $x_3$ caused by the disturbances is $\pm 0.2\,(1.44 + 1.2 + 1) = \pm 0.728$, which does not fit in $|x_3| \le 0.5$. So the open-loop problem with $N = 3$ is infeasible from every state. The feedback problem is feasible exactly for $|x_0| \le 13/12$, $113/72$ and $853/432$ for $N = 1, 2, 3$: each extra step adds the states that one input of size at most 1 can bring into the previous region despite the disturbance.

**In closed loop** with $N = 2$ from $x_0 = 1$ and $w = 0$, the inputs are $-1$ and $-0.24$, and the state goes $1, 0.2, 0$ and stays at 0. With random disturbances in $[-0.2, 0.2]$ every problem stays feasible, as Theorem 2 of the proof says, because the terminal set is robustly invariant under $u = -1.2\, x$: then $x^+ = w$, and $|u| \le 0.6$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Any admissible feedback policy, restricted to the vertex sequences, is a feasible point of the LP with a cost no larger than its worst case, so the LP value is at most the min-max value. Conversely, given an LP solution, write each disturbance as a convex combination of the vertices and mix the controls of the tree with the products of these weights. This policy is causal, and its trajectory under any disturbance sequence in the polytope is a convex combination of the leaf trajectories. The constraints are convex and the cost is convex, so the policy meets all constraints and its cost is at most the largest leaf cost. Hence the LP value equals the min-max value over the whole polytope, not only over the vertices. If the terminal set is robustly invariant under a local feedback inside the constraints, the shifted tree with that feedback appended is feasible at the next sample, so the receding horizon loop stays feasible.

## Complexity

The tree has $(V^{N+1} - 1)/(V - 1)$ nodes for $V \ge 2$, so the LP has $L$ of order $V^N (n + m + q)$ variables and rows, where $q$ is the number of constraint rows per node. The dense simplex tableau has $O(L^2)$ entries, and each pivot costs $O(L^2)$, so the time is $O(I L^2)$ for $I$ pivots. The simplex method can need exponentially many pivots in the worst case; an interior point method solves the LP in time polynomial in $L$. The size is exponential in the horizon in any case, which limits exact feedback min-max MPC to short horizons and few vertices. The open-loop form has only $N m$ input variables, but its constraints still range over all $V^N$ vertex sequences.

## Properties

- **Exact for the polytope.** The worst case over the vertex sequences equals the worst case over all sequences in the polytope, for both forms, because the plant is linear and the cost and constraints are convex.
- **Feedback is never worse.** The feedback value is at most the open-loop value, and its feasible region contains the open-loop one, often strictly.
- **Recursive feasibility** of the feedback form, when the terminal set is robustly positively invariant under a local law that meets the constraints. The open-loop form has no such guarantee.
- **Guaranteed constraints** for every disturbance in the set, as long as the model and the set are right.
- **Conservative cost.** The controller plans for the worst case. Under typical disturbances, the performance can be worse than that of a nominal or [stochastic MPC](/stochastic-mpc/).

## Variants and improvements

- **Infinity-norm costs.** Replace the sum by a maximum; the problem is still an LP. Quadratic costs give a QP for the open-loop form, and a convex problem over the tree for the feedback form.
- **Explicit solution.** With 1-norm or infinity-norm costs, the first input is a piecewise affine function of $x_0$, and it can be computed offline as in [explicit MPC](/explicit-mpc/).
- **Affine disturbance feedback.** Restrict the policy to inputs affine in the past disturbances. The problem is then convex with size polynomial in $N$, at the price of some conservatism.
- **[Tube MPC](/tube-mpc/).** Fix the feedback to $u = v + K (x - z)$ with a nominal state $z$, and plan only $v$ with tightened constraints. The size does not grow with the number of vertices.
- **Model uncertainty.** If $A$ and $B$ lie in a polytope instead of an additive disturbance, the tree branches over the vertex models. Kothare, Balakrishnan and Morari (1996) gave an LMI form with a state feedback law for this case.

## When to use it

Use min-max MPC when the disturbance is bounded but has no useful probability law, the constraints are hard, and the system is small with a short horizon. The feedback form is the reference solution for robust linear MPC: other methods are often judged by how close they come to its value and feasible region. For larger systems or longer horizons, use [tube MPC](/tube-mpc/) or affine disturbance feedback. If the disturbance has a known distribution and small violations are acceptable, use [stochastic MPC](/stochastic-mpc/). If a small disturbance only needs to be rejected near a setpoint, [offset-free MPC](/offset-free-mpc/) is simpler.

## Pitfalls

- **Open loop in place of feedback.** The open-loop form plans as if no new information will come. It is very conservative for unstable plants and can be infeasible for every state, as in the example.
- **Exponential size.** The tree has $V^N$ leaves. A box disturbance in $\mathbb{R}^d$ has $2^d$ vertices, so the tree grows like $2^{d N}$.
- **Wrong disturbance set.** The guarantees hold only for disturbances in $W$. A set that is too small gives false confidence, and one that is too large gives a small feasible region.
- **No terminal set.** Without a robustly invariant terminal set the loop can become infeasible after a few steps, even if the first problem is feasible.
- **Sampled vertices.** Planning against a few sampled disturbance sequences instead of all vertex sequences is not the min-max problem and gives no guarantee.

## Implementations

## History

Campo and Morari (1987) brought the worst case cost into MPC and showed that the 1-norm and infinity-norm problems are linear programs. Open-loop min-max MPC was soon found to be conservative, and Scokaert and Mayne (1998) proposed the feedback form, which optimizes one control for each vertex sequence and has feasibility and stability guarantees. The survey of Mayne, Rawlings, Rao and Scokaert (2000) placed min-max MPC in the general theory of MPC stability. Later work reduced the cost of robust MPC with explicit solutions, affine disturbance feedback, and tubes.

## References
