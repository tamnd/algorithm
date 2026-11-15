---
tag: ZNT0ZQ
kind: algorithm
slug: tube-mpc
name: Tube MPC
aliases:
- tube-based MPC
area: control/optimal-and-predictive-control
level: research
summary: Plans a nominal trajectory with tightened constraints and adds an ancillary feedback that keeps the true state in a tube around it despite bounded disturbances.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, N: the horizon, L: "the number of variables and rows of the online LP, of order N (n + m + q) + r for q constraint rows per step and r facet rows of the error set", I: the number of simplex pivots}
  time: {worst: "O(I L^2)"}
  space: {extra: "O(L^2)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 2005
  people: [David Q. Mayne, María M. Seron, Saša V. Raković]
  note: "Mayne, Seron and Raković (2005) gave tube MPC with the first nominal state as a decision variable and proved robust exponential stability of the error set. In the same year Raković, Kerrigan, Kouramas and Mayne gave the outer bounds of the minimal robust positively invariant set that the method uses."
prereqs: [linear-mpc, minkowski-sum, support-function, positively-invariant-set]
see_also: [min-max-mpc, stochastic-mpc, recursive-feasibility, zonotope-reachability, maximal-positively-invariant-set, control-invariant-set, reference-governor, input-to-state-stability]
sources:
  - paper: doi:10.1016/j.automatica.2004.08.019
    title: David Q. Mayne, María M. Seron and Saša V. Raković, Robust model predictive control of constrained linear systems with bounded disturbances, Automatica 41(2), 219-224, 2005
    locator: the tube controller with the initial nominal state as a decision variable, recursive feasibility, and robust stability of the error set
  - paper: "Saša V. Raković, Eric C. Kerrigan, Konstantinos I. Kouramas and David Q. Mayne, Invariant approximations of the minimal robust positively invariant set, IEEE Transactions on Automatic Control 50(3), 406-410, 2005"
    locator: the outer bound of the minimal robust positively invariant set from A_K^s W inside alpha W
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: the chapter on robust MPC, tube-based MPC for linear systems
---

Tube MPC is a robust form of [model predictive control](/model-predictive-control/) for a linear plant with a bounded additive disturbance. It splits the input into two parts: a nominal input $v$ from an MPC problem for the plant without disturbance, and an ancillary feedback $K (x - z)$ on the error between the true state $x$ and the nominal state $z$. With $A + B K$ Schur, the error stays in a fixed robust positively invariant set $Z$, so the true state stays in a tube $z_k \oplus Z$ around the nominal trajectory. The nominal problem uses constraints tightened by $Z$, so every state in the tube meets the true constraints. The online problem has the size of a nominal MPC problem, it does not grow with the number of disturbance vertices, and the closed loop stays feasible and converges to $Z$.

## In plain words

Plan the path as if there were no disturbance, but keep a safety distance from every limit. Then follow the plan with a simple correction: when the real state drifts from the plan, push it back in proportion to the drift. Because the disturbance is bounded and the correction is fixed, the drift never leaves a known region around the plan, which you can work out once, ahead of time. So the safety distance is that region's size, and the real state never crosses a limit. Each step only solves the small plan without disturbance, which is fast. The cost is a more cautious plan, because the safety distance is always kept.

## The problem

Input: matrices $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$, a gain $K$ with $A_K = A + B K$ Schur, a disturbance set $W$ (a zonotope that contains 0 in its interior), state and input constraints $X$ and $U$ (polyhedra), a horizon $N$, weights $Q$ and $R$, and the current state $x$.

The plant is $x_{k+1} = A x_k + B u_k + w_k$ with $w_k \in W$.

Output: an input $u \in U$ such that, when the same rule is applied at every sample, $x_k \in X$ and $u_k \in U$ for every disturbance sequence in $W$, the problem stays feasible, and $x_k$ tends to the error set $Z$.

## The algorithm

```pseudo id=main
TUBE-MPC(A, B, K, W, X, U, N, Q, R, x₀)
L1   find s, α with A_Kˢ W ⊆ α W;  Z ← (1 - α)⁻¹ (W ⊕ A_K W ⊕ ... ⊕ A_Kˢ⁻¹ W)     ▷ offline
L2   X̄ ← X ⊖ Z,  Ū ← U ⊖ K Z   (each row bound b becomes b - h_Z(a))           ▷ offline
L3   for k = 0, 1, 2, ... do  measure x
L4       rows: x - z₀ ∈ Z,  z_{j+1} = A z_j + B v_j,  z_j ∈ X̄,  v_j ∈ Ū,  z_N = 0
L5       solve the LP: minimize Σ_{j<N} (‖Q z_j‖₁ + ‖R v_j‖₁) over z₀, v₀, ..., v_{N-1}
L6       apply u = v₀ + K (x - z₀)
```

Line L1 follows Raković, Kerrigan, Kouramas and Mayne (2005). The [Minkowski sum](/minkowski-sum/) of zonotopes is the list of all their generators, so $Z$ is a zonotope too. The test $A_K^s W \subseteq \alpha W$ compares [support functions](/support-function/) on the facet normals of $W$. A smaller $\alpha$ gives a tighter $Z$ and needs a larger $s$.

Line L2 subtracts the support function of $Z$ (or of $K Z$) from each row bound. For a zonotope, $h_Z(a) = \sum_j |a^T g_j|$ over its generators.

Line L4 makes the first nominal state $z_0$ a free variable that only has to be within $Z$ of the measured state. The rows of $Z$ come from its facets: in $\mathbb{R}^n$, each facet normal is orthogonal to $n - 1$ generators. The terminal constraint $z_N = 0$ is the simplest choice; a larger terminal set that is positively invariant for the nominal loop works as well. With 1-norm costs the problem is an LP; with quadratic costs it is a QP of the same size.

## Example

Take the double integrator with sample time 1, $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} 0.5 \\ 1 \end{bmatrix}$, with $|w_1| \le 0.1$ and $|w_2| \le 0.1$. The constraints are $|x_1| \le 5$, $|x_2| \le 1$ and $|u| \le 1$. Choose the deadbeat gain $K = [-1, \ -1.5]$, so that

$$A_K = \begin{bmatrix} 0.5 & 0.25 \\ -1 & -0.5 \end{bmatrix}, \quad A_K^2 = 0.$$

**The error set.** Since $A_K^2 W = \{0\}$, line L1 stops at $s = 2$ with $\alpha = 0$, and $Z = W \oplus A_K W$ is exactly the minimal invariant set. It has the four generators $(0.1, 0)$, $(0, 0.1)$, $(0.05, -0.1)$ and $(0.025, -0.05)$, so $|e_1| \le 0.175$, $|e_2| \le 0.25$ and $|K e| \le 0.4$ on $Z$. The tightened constraints are $|z_1| \le 4.825$, $|z_2| \le 0.75$ and $|v| \le 0.6$.

**One problem.** With $Q = I$, $R = 1$, $N = 6$ and $x = (-3, 0)$, the LP value is $51/4$, and the first nominal state is $z_0 = (-2.925, 0.15)$, not $x$ itself. The nominal input is $v_0 = 0.6$ and the applied input is $u = 0.6 + K (x - z_0) = 0.6 + 0.075 + 0.225 = 0.9$. With $N = 4$ the problem is infeasible from this state: with $|v| \le 0.6$ and $|z_2| \le 0.75$, the nominal state cannot reach the origin in 4 steps.

**Closed loop.** With no disturbance, the values are $12.75$, $8.625$, $5.0625$, $2.375$, $0.3125$, and then 0: the state reaches the origin at $k = 5$. With the constant disturbance $w = (0.1, 0.1)$, $z_0$ becomes 0 at $k = 4$ and the state settles at $(0.175, -0.05)$, a point of $Z$. Under random vertex disturbances the state and the input stay within their limits at every step, and the state enters $Z$ and stays there.

**A gain that is not deadbeat.** With $K = [-0.5, \ -1]$ the set $Z$ is not finitely determined, and the choice of $\alpha$ trades the size of $Z$ against the number of generators:

| $\alpha_{\max}$ | $s$ | $\alpha$ | max $\lvert e_1 \rvert$ | max $\lvert e_2 \rvert$ | max $\lvert K e \rvert$ |
|---|---|---|---|---|---|
| 0.5 | 3 | 0.344 | 0.448 | 0.324 | 0.329 |
| 0.1 | 5 | 0.065 | 0.343 | 0.275 | 0.269 |
| 0.01 | 8 | 0.0084 | 0.336 | 0.268 | 0.258 |

This gain is softer than the deadbeat one: it needs less input margin, but the tube is wider in the position.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The error $e = x - z$ follows $e^+ = A_K e + w$, whatever the nominal input is. The set of Raković and coauthors satisfies $A_K Z \oplus W \subseteq Z$, because $A_K^s W \subseteq \alpha W$ lets the last term of the sum be absorbed into the scale factor. So once $x - z_0 \in Z$, the error stays in $Z$. A nominal state in $X \ominus Z$ then gives a true state in $X$, and the same holds for the input. At the next sample, the old plan shifted by one step, with $v = 0$ appended, is feasible: its first state $z_1$ is within $Z$ of the new measured state, and $z_N = 0$ stays at 0. So the problem stays feasible, and its value drops by at least the first stage cost. The sum of the stage costs is therefore finite, the first nominal state tends to 0, and the true state approaches $Z$.

## Complexity

The online LP has $n + N m$ decision variables, $N$ times the epigraph variables of the cost, and of order $N q + r$ rows, where $q$ is the number of constraint rows per step and $r$ the number of facet rows of $Z$. Its size $L$ is linear in the horizon, and the dense simplex method costs $O(L^2)$ per pivot. The disturbance set enters only through $Z$, computed once offline: $Z$ has $s$ times as many generators as $W$, and in $\mathbb{R}^n$ the number of facet rows can grow like the number of $(n-1)$-subsets of generators. This is the main gain over [min-max MPC](/min-max-mpc/), whose LP grows like $V^N$ for $V$ vertices of $W$.

## Properties

- **Robust constraint satisfaction** for every disturbance sequence in $W$.
- **Recursive feasibility,** by the shifted nominal plan.
- **Convergence to the error set.** The value is a Lyapunov function for the nominal state, and the true state approaches $Z$. Mayne, Seron and Raković (2005) show robust exponential stability of $Z$ for the quadratic cost version.
- **Small online problem,** the size of a nominal MPC problem, which grows linearly with the horizon.
- **Conservative,** since the full tube $Z$ is reserved at every step of the horizon, even where the actual error is small. The feasible region is smaller than that of feedback [min-max MPC](/min-max-mpc/).
- **The choice of $K$ matters.** A fast $K$ gives a small $Z$ in the state but a large $K Z$, which eats the input range.

## Variants and improvements

- **Fixed initial state.** Setting $z_0 = x$ is simpler, but then the shifted plan is not feasible in general, and the stability argument needs more care.
- **Constraint tightening along the horizon.** Tighten step $j$ only by $\bigoplus_{i<j} A_K^i W$, which grows with $j$. This is less conservative early in the horizon.
- **Homothetic and elastic tubes.** Let the tube be $z_k \oplus \beta_k Z$ with scales $\beta_k$ as decision variables, so the tube shrinks where the disturbance allows.
- **Output feedback.** Add an observer and a second tube for the estimation error.
- **Nonlinear plants.** Use a nonlinear ancillary controller that tracks the nominal trajectory, and bound the tube by an incremental Lyapunov function.
- **Stochastic tubes.** Replace the robust tightening by a probabilistic one, as in [stochastic MPC](/stochastic-mpc/).

## When to use it

Use tube MPC for a linear plant with a bounded disturbance and hard constraints, when [min-max MPC](/min-max-mpc/) is too large to solve online. It is a good default for robust linear MPC: the online problem is a standard QP or LP, and the offline work is a set computation. If the disturbance is large compared to the constraints, the tightened sets can be empty; then a less conservative method or a different $K$ is needed. If constraint violations with small probability are acceptable, [stochastic MPC](/stochastic-mpc/) uses the constraint range better.

## Pitfalls

- **Empty tightened sets.** If $Z$ is larger than $X$ in some direction, or $K Z$ larger than $U$, the method has no feasible point at all. Check the tightened bounds first, and change $K$ if they are negative.
- **Too large an $\alpha$.** The bound $Z$ is $(1 - \alpha)^{-1}$ times a partial sum, so a crude $\alpha$ wastes constraint range.
- **Wrong disturbance set.** The guarantees hold only for $w \in W$. In practice $W$ should include model errors, which are often larger than the measured noise.
- **Numerical facets.** In higher dimensions, the number of facet rows of a zonotope grows fast. Remove redundant rows, or use a box or a polytope that contains $Z$.
- **Applying $v$ alone.** The applied input must include the ancillary term $K (x - z_0)$. Without it, the error is not bounded by $Z$.

## Implementations

## History

Earlier robust MPC schemes already combined a fixed linear feedback with constraint tightening along the horizon. Mayne, Seron and Raković (2005) made the first nominal state a decision variable, which gives a clean proof of recursive feasibility and robust exponential stability of the error set. In the same year Raković, Kerrigan, Kouramas and Mayne (2005) showed how to compute outer bounds of the minimal robust positively invariant set to any accuracy. Later work extended tubes to output feedback, nonlinear plants, homothetic and elastic tubes, and stochastic tubes, and the book of Rawlings, Mayne and Diehl presents tube MPC as a standard method of robust MPC.

## References
