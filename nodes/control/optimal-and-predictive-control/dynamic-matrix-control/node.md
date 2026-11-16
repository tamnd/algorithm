---
tag: 078WY3
kind: algorithm
slug: dynamic-matrix-control
name: Dynamic matrix control
aliases:
- DMC
area: control/optimal-and-predictive-control
level: core
summary: An early industrial MPC that predicts the output from a step response model and solves a least squares problem for the input moves.
model: real-ram
complexity:
  vars: {P: the prediction horizon, M: the number of future moves, L: the length of the step response model}
  time: {worst: "O(P L)", offline: "O(P M^2 + M^3)"}
  space: {extra: "O(P M + L)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1980
  people: [C. R. Cutler, B. L. Ramaker]
  note: "Cutler and Ramaker presented dynamic matrix control in 1980; García and Morshedi added constraints with a quadratic program in 1986 (QDMC)."
prereqs: [model-predictive-control, linear-time-invariant-system, normal-equations]
see_also: [generalized-predictive-control, linear-mpc, offset-free-mpc, internal-model-control, ridge-regression, smith-predictor, process-reaction-curve, steady-state-error]
sources:
  - paper: "C. R. Cutler and B. L. Ramaker, Dynamic matrix control: a computer control algorithm, Proceedings of the Joint Automatic Control Conference, San Francisco, 1980, paper WP5-B"
    locator: the step response model, the dynamic matrix, and the least squares move calculation
  - paper: doi:10.1016/0005-1098(78)90001-8
    title: J. Richalet, A. Rault, J. L. Testud and J. Papon, Model predictive heuristic control, applications to industrial processes, Automatica 14(5), 413-428, 1978
    locator: the earlier predictive scheme with an impulse response model
  - paper: doi:10.1080/00986448608911397
    title: Carlos E. García and A. M. Morshedi, Quadratic programming solution of dynamic matrix control (QDMC), Chemical Engineering Communications 46(1-3), 73-87, 1986
    locator: the constrained form of DMC as a quadratic program
  - paper: doi:10.1016/S0967-0661(02)00186-7
    title: S. Joe Qin and Thomas A. Badgwell, A survey of industrial model predictive control technology, Control Engineering Practice 11(7), 733-764, 2003
    locator: the history of DMC, IDCOM and QDMC in industry
---

Dynamic matrix control (DMC) is one of the first [model predictive control](/model-predictive-control/) methods that spread in industry. Its model is the measured step response of the plant: $s_i$ is the output $i$ samples after a unit step of the input. With this model, the future outputs are a linear function of the future input moves $\Delta u(k) = u(k) - u(k-1)$, and the matrix of that function is the dynamic matrix $S$ that gives the method its name. At each sampling instant DMC takes the difference between the measured and the model output as a constant output disturbance, predicts the outputs over $P$ samples, chooses $M$ moves by regularized least squares, and applies the first move. Without constraints the result is a fixed linear controller with integral action.

## In plain words

Step the input of the plant once and record how the output moves. That record is the whole model. Now, at each tick, ask: if I make no more changes, where will the output go? Shift the recorded responses of all past input changes forward in time and add them up. The model is never perfect, so the controller also adds the present gap between the measured output and the model output, and assumes that gap stays the same. Then it picks a few future input changes so that the predicted output comes close to the setpoint, with a penalty on large changes. This is a least squares problem. Only the first change is applied, and the whole process is done again at the next tick.

## The problem

Input: a step response model $s_1, \dots, s_L$ of a single input, single output plant whose step response settles by sample $L$ (so $s_i = s_L$ for $i > L$); a prediction horizon $P < L$; a number of moves $M \le P$; a move weight $\lambda \ge 0$; at each sampling instant $k$, the measured output $y(k)$ and the setpoint $r$. Output: the input $u(k)$.

**The model.** By superposition, a plant with this step response has the output

$$\hat y(k) = \sum_{j \ge 1} s_j\, \Delta u(k - j),$$

with $s_j = s_L$ for $j > L$. A move made $j$ samples ago contributes $s_j$ times its size.

**The prediction.** With the disturbance estimate $d(k) = y(k) - \hat y(k)$ held constant, the predicted outputs are

$$\hat y(k + i) = f_i + \sum_{j = 1}^{M} S_{ij}\, \Delta u(k + j - 1), \qquad f_i = \sum_{j \ge 1} s_{i + j}\, \Delta u(k - j) + d(k),$$

for $i = 1, \dots, P$. The free response $f_i$ is the effect of the past moves; the $P \times M$ dynamic matrix $S_{ij} = s_{i - j + 1}$ for $i \ge j$ (and 0 above the diagonal) is the effect of the future moves.

**The move.** DMC minimizes $\|r \mathbf{1} - f - S\, \Delta U\|^2 + \lambda \|\Delta U\|^2$ over $\Delta U = (\Delta u(k), \dots, \Delta u(k + M - 1))$. This is a [ridge regression](/ridge-regression/), and its [normal equations](/normal-equations/) give

$$\Delta U^* = (S^T S + \lambda I)^{-1} S^T (r \mathbf{1} - f).$$

## The algorithm

```pseudo id=main
DMC-SETUP(s, P, M, λ)                               ▷ offline
L1   S ← the P × M matrix with S_ij = s_(i-j+1) for i ≥ j, 0 otherwise
L2   K ← first row of (Sᵀ S + λ I)⁻¹ Sᵀ
DMC-STEP(y, r)                                     ▷ online, at each sampling instant
L3   compute the free response f of the past moves:
L4       d ← y - Σ_(j ≥ 1) s_j Δu(k - j)            ▷ model mismatch, held constant
L5       f_i ← Σ_(j ≥ 1) s_(i+j) Δu(k - j) + d  for i = 1, …, P
L6   Δu(k) ← K (r 1 - f)                           ▷ first move of the least squares plan
L7   store Δu(k) in the move history;  u(k) ← u(k - 1) + Δu(k);  return u(k)
```

Lines L1 and L2 run once. Line L2 needs only the first row $K$, because only the first move is applied. Lines L4 and L5 use the last $L$ moves one by one and the sum of all older moves, which all have the same weight $s_L$. Line L6 is one inner product of length $P$. The implementation stores all $M$ rows of the gain for the tests, and keeps the history in a list of the last $L$ moves.

## Example

The plant is $y(k+1) = 0.8\, y(k) + 0.2\, u(k-1)$, a first order lag with gain 1 and one extra sample of delay. Its step response is $s_i = 1 - 0.8^{i-1}$:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $s_i$ | 0 | 0.2 | 0.36 | 0.488 | 0.5904 | 0.6723 |

The tuning is $L = 30$, $P = 10$, $M = 2$, $\lambda = 0.1$. Lines L1 and L2 give

$$K = (0,\ 0.6807,\ 0.4973,\ 0.3505,\ 0.2331,\ 0.1392,\ 0.0641,\ 0.0040,\ -0.0441,\ -0.0826), \qquad \textstyle\sum_i K_i = 1.8422.$$

The first entry is 0 because $s_1 = 0$: the input cannot move the next output, so the first row of $S$ is zero.

**A setpoint step.** From rest with $r = 1$, the free response is $f = 0$ and the first move is $\sum_i K_i = 1.8422$. The closed loop (measurement with the implementation):

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $u(k)$ | 1.8422 | 2.0335 | 1.7048 | 1.3556 | 1.1295 | 1.0202 | 0.9830 | 0.9791 |
| $y(k+1)$ | 0 | 0.3684 | 0.7015 | 0.9021 | 0.9928 | 1.0202 | 1.0202 | 1.0127 |

The output overshoots by about 2 percent and settles at 1.

**An output disturbance.** A step of 0.3 is added to the measured output from $k = 25$. Because of the delay, the outputs at $k = 25$ and $k = 26$ are both 1.2999. Then the output returns: 1.1894, 1.0896, 1.0295, 1.0025, 0.9946, and it converges to 1 with no offset. The tests repeat this with a step of 0.5 and with plant gains 0.7 and 1.3 against the model gain 1, and the output still converges to the setpoint.

**Tuning.** $\sum_i K_i$ is the first move after a unit setpoint step from rest, so it measures how hard the controller acts. With $M = 1$ and $\lambda = 0$ it is 1.4496; with $P = 15$, $M = 3$ and $\lambda = 1$ it is 0.7596. In the tests, a larger $\lambda$ gives a smaller first move for $\lambda = 0, 0.1, 1, 10$.

## Correctness

The proofs are in proofs/correctness.md.

1. **The prediction is exact for a step response plant.** If the plant output is $\hat y(k) + d$ with a constant $d$, then $\hat y(k + i)$ of the formula above equals the true future output for any future moves (superposition, Lemma 1).
2. **The move is the least squares optimum.** For $\lambda > 0$, or $\lambda = 0$ with $S$ of full column rank, the cost is strictly convex and $\Delta U^*$ is its unique minimizer (Lemma 2). With a dead time of $\tau$ samples, full rank holds when $P \ge M + \tau$ and $s_{\tau + 1} \ne 0$.
3. **Unconstrained DMC is linear and time invariant.** $K$ is fixed and $f$ is linear in $y(k)$ and the past moves, so $\Delta u(k)$ is a fixed linear function of $r$, $y(k)$ and the past moves (Lemma 3).
4. **Zero offset (theorem).** If $r$ and the disturbance are constant from some time on, the closed loop with a linear plant is asymptotically stable, and $\sum_i K_i \ne 0$, then $y(k) \to r$. The plant may differ from the model: the mismatch goes into $d(k)$. In the limit $\Delta u = 0 = (\sum_i K_i)(r - y_\infty)$.

## Complexity

Costs are in the [real-RAM model](/real-ram/), with $P$ the prediction horizon, $M$ the number of moves and $L$ the model length, for one input and one output.

- **Offline.** $S^T S$ costs $O(P M^2)$, a [Cholesky factorization](/cholesky-decomposition/) of $S^T S + \lambda I$ costs $O(M^3)$, and the first row of the gain needs one more solve and a product with $S^T$, $O(M^2 + P M)$. Total $O(P M^2 + M^3)$. The implementation solves one system per column of the gain with [Gaussian elimination](/gaussian-elimination/), $O(P M^3)$, which is the same for the small $M$ of practice.
- **Online, per sampling instant.** The free response costs $O(L)$ for each of the $P$ horizons, so $O(P L)$. With a shift register of the free response, updated by one column of the step response per sample, this drops to $O(P)$. Line L6 costs $O(P)$.
- **Space.** $O(P M)$ for $S$ and the gain, and $O(L)$ for the move history.
- **Multivariable plants.** With $m$ inputs and $p$ outputs, $S$ has $P p$ rows and $M m$ columns, and the costs grow accordingly: $O(P p M^2 m^2 + M^3 m^3)$ offline.

## Properties

- **Linear time-invariant controller** when there are no constraints. Its stability with the plant depends on $P$, $M$ and $\lambda$ and must be checked. DMC itself gives no stability guarantee.
- **Integral action.** The constant output disturbance model removes steady-state error for constant setpoints and disturbances, as long as the loop converges (theorem above).
- **Only for plants with a settling step response.** A finite step response model needs an asymptotically stable plant, with all poles strictly inside the unit circle (Schur). Integrating and unstable plants need another model.
- **Same as GPC for setpoint changes.** For a plant with an exact step model and no disturbance, and the GPC horizons $N_1 = 1$, $N_2 = P$, $N_u = M$, the predictions of DMC and of [GPC](/generalized-predictive-control/) agree, so the gains and the setpoint response are equal. They differ in the disturbance model.

## Variants and improvements

- **QDMC** (García and Morshedi 1986): input, move and output limits are added, and each step solves a [quadratic program](/quadratic-programming/) instead of a least squares problem. This is DMC as a special case of [linear MPC](/linear-mpc/) with a step response model.
- **Multivariable DMC.** Each input and output pair has its own step response, and $S$ becomes a block matrix with one block per pair.
- **Output weights and move weights** per output and per input, and a reference trajectory instead of a constant setpoint (the code accepts a list $r_1, \dots, r_P$).
- **Model predictive heuristic control** (Richalet et al. 1978) uses an impulse response model instead of a step response model.
- **GPC** uses a transfer function model and a different disturbance model; see [generalized predictive control](/generalized-predictive-control/).
- **State-space disturbance models.** [Offset-free MPC](/offset-free-mpc/) generalizes the constant output disturbance of DMC to state-space models with input or state disturbances.

## When to use it

Use DMC for plants that are open-loop asymptotically stable and easy to test with a step, when a model from first principles is not available. It is common in process control, where the plants are slow and the step tests are routine. For plants with integrators or unstable modes, or for strong disturbance rejection, use a state-space form such as [linear MPC](/linear-mpc/) with an [offset-free](/offset-free-mpc/) disturbance model. If there are limits on the inputs, use the QP form.

## Pitfalls

- **Model too short.** If $L$ is shorter than the settling time, the truncation $s_i = s_L$ is wrong and the predictions drift. The implementation rejects $P \ge L$.
- **Slow rejection of input disturbances.** The model assumes a constant output disturbance. A disturbance that enters at the input passes through the plant dynamics. Rule of thumb: DMC removes it slowly, at about the speed of the open-loop plant; when this matters, use a disturbance model that matches the real disturbance.
- **Clipping the move.** Clipping $u$ at a limit after line L6 gives a feasible input but not the optimal one, and the move history then differs from the applied input unless it stores the clipped move. Store the applied move, or use QDMC. See [integrator windup](/integrator-windup/).
- **$\lambda = 0$ with $M$ close to $P$** makes the first move very large and the loop sensitive to model error.
- **No stability check.** Some choices of $P$, $M$ and $\lambda$ give an unstable loop. Check the closed-loop poles with the model, and test with model error.

## Implementations

## History

Richalet, Rault, Testud and Papon (1978) described model predictive heuristic control, with an impulse response model, and its use on industrial processes. Cutler and Ramaker, engineers at Shell Oil, presented dynamic matrix control in 1980 at the Joint Automatic Control Conference. García and Morshedi (1986) wrote the constrained version as a quadratic program, QDMC. Qin and Badgwell (2003) describe how these methods became the base of industrial MPC products.

## References
