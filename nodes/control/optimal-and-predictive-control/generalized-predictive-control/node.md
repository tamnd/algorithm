---
tag: J9ZFD5
kind: algorithm
slug: generalized-predictive-control
name: Generalized predictive control
aliases:
- GPC
area: control/optimal-and-predictive-control
level: core
summary: An MPC on a CARIMA transfer function model that minimizes predicted output errors and input increments over a horizon.
model: real-ram
complexity:
  vars: {N: the output horizon N2, M: the control horizon Nu, a: the degree of A, b: the degree of B}
  time: {worst: "O(N (a + b))", offline: "O(N^2 (a + b) + N M^2 + M^3)"}
  space: {extra: "O(N^2 + N (a + b) + N M)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1987
  people: [D. W. Clarke, C. Mohtadi, P. S. Tuffs]
  note: "Clarke, Mohtadi and Tuffs published GPC in two papers in Automatica in 1987, the basic algorithm and its extensions and interpretations."
prereqs: [model-predictive-control, transfer-function, armax-model, normal-equations]
see_also: [dynamic-matrix-control, linear-mpc, self-tuning-regulator, adaptive-pole-placement, polynomial-long-division, least-squares-arx-identification, internal-model-principle, deadbeat-control]
sources:
  - paper: "D. W. Clarke, C. Mohtadi and P. S. Tuffs, Generalized predictive control, Part I. The basic algorithm, Automatica 23(2), 137-148, 1987"
    locator: the CARIMA model, the Diophantine predictor, the cost with the horizons N1, N2, Nu and the move weight, and the receding horizon law
  - paper: "D. W. Clarke, C. Mohtadi and P. S. Tuffs, Generalized predictive control, Part II. Extensions and interpretations, Automatica 23(2), 149-160, 1987"
    locator: the extensions of the basic algorithm and its relation to other self-tuning and predictive controllers
  - paper: doi:10.1016/S0967-0661(02)00186-7
    title: S. Joe Qin and Thomas A. Badgwell, A survey of industrial model predictive control technology, Control Engineering Practice 11(7), 733-764, 2003
    locator: the place of GPC and the adaptive control line of work in the history of MPC
---

Generalized predictive control (GPC) is a [model predictive control](/model-predictive-control/) method for a plant given as a [transfer function](/transfer-function/) in the backward shift $q^{-1}$. Its model is the CARIMA model (controlled autoregressive integrated moving average)

$$A(q^{-1})\, y(t) = B(q^{-1})\, u(t-1) + \frac{e(t)}{\Delta}, \qquad \Delta = 1 - q^{-1},$$

in which the disturbance is integrated white noise. From this model, the Diophantine identity $1 = E_j \Delta A + q^{-j} F_j$ gives the optimal $j$-step predictor of the output. GPC minimizes the squared predicted errors over the horizons $N_1$ to $N_2$ plus $\lambda$ times the squared input increments over $N_u$ moves, and applies the first increment. Without constraints the law is a fixed linear controller in RST form with integral action. Clarke, Mohtadi and Tuffs introduced it in 1987, from the line of work on self-tuning control.

## In plain words

GPC is like dynamic matrix control, but its model is a short difference equation instead of a recorded step response. The model also says how the unknown disturbance behaves: it drifts like a random walk, so the controller must act on changes of the input, which gives integral action. From the model, a polynomial division gives the best guess of each future output, as a sum of a part from the past and a part from the future input changes. The controller picks the future input changes that bring the guesses close to the setpoint, with a penalty on large changes, and applies only the first one. Because the model has few numbers, it is easy to estimate online, which makes GPC a common choice for adaptive control.

## The problem

Input: monic $A$ of degree $a$ and $B$ of degree $b$ (a dead time of $\tau$ samples is written as $\tau$ leading zeros in $B$); the horizons $1 \le N_1 \le N_2$; the control horizon $N_u$; the move weight $\lambda \ge 0$; at each sampling instant $t$, the measured output $y(t)$ and the setpoint $w$. Output: the input $u(t)$.

**The predictor.** Write $\tilde A = \Delta A$, which is monic of degree $a + 1$. For each $j$, long division of 1 by $\tilde A$ to $j$ terms gives unique $E_j$ of degree $j - 1$ and $F_j$ of degree $a$ with $1 = E_j \tilde A + q^{-j} F_j$. With $G_j = E_j B$,

$$y(t + j) = G_j\, \Delta u(t + j - 1) + F_j\, y(t) + E_j\, e(t + j).$$

The last term depends only on future noise, so $\hat y(t + j \mid t) = G_j\, \Delta u(t + j - 1) + F_j\, y(t)$ is the minimum mean square error predictor.

**The split.** The first $j$ coefficients of $G_j$ are $g_0, \dots, g_{j-1}$, the step response of $q^{-1} B / A$. So the predictions for $j = N_1, \dots, N_2$ are $\hat y = G\, \Delta U + f$ with $G_{j l} = g_{j - 1 - l}$ for $l < \min(j, N_u)$, and the free response $f_j$ collects $F_j\, y(t)$ and the terms of $G_j$ that multiply past increments.

**The move.** Minimize $\|w \mathbf{1} - G\, \Delta U - f\|^2 + \lambda \|\Delta U\|^2$ over the $N_u$ increments $\Delta U$. The minimizer is $\Delta U^* = (G^T G + \lambda I)^{-1} G^T (w \mathbf{1} - f)$.

## The algorithm

```pseudo id=main
GPC-SETUP(A, B, N1, N2, Nu, λ)                       ▷ offline
L1   Ã ← A (1 - q⁻¹)
     for j ← N1 to N2
L2       (E_j, F_j) ← long division of 1 by Ã to j terms   ▷ 1 = E_j Ã + q⁻ʲ F_j
L3       G_j ← E_j B
     G ← the matrix with G_jl = g_(j-1-l), the step response coefficients
L4   K ← first row of (Gᵀ G + λ I)⁻¹ Gᵀ
GPC-STEP(y(t), w)                                   ▷ online, at each sampling instant
L5   f_j ← F_j y(t) + Σ_(i ≥ j) G_j,i Δu(t + j - 1 - i)  for j = N1, …, N2
L6   Δu(t) ← K (w 1 - f)
L7   u(t) ← u(t - 1) + Δu(t);  store y(t) and Δu(t);  return u(t)
```

Line L2 is [polynomial long division](/polynomial-long-division/): $E_j$ is the first $j$ terms of the power series $1 / \tilde A$, and $F_j$ is what is left, shifted by $j$. Line L4 keeps only the first row, because only the first increment is applied. Line L5 needs the last $a + 1$ outputs and the last $b$ increments. The implementation also returns the equivalent RST polynomials and the closed-loop polynomial, for analysis.

## Example

The model is $A = 1 - 0.8\, q^{-1}$, $B = 0.2\, q^{-1}$, so $y(t) = 0.8\, y(t-1) + 0.2\, u(t-2)$. This is the plant of the [DMC](/dynamic-matrix-control/) example: gain 1 and one extra sample of delay. Then $\tilde A = 1 - 1.8\, q^{-1} + 0.8\, q^{-2}$.

**The Diophantine polynomials** (exact with rational arithmetic):

| $j$ | $E_j$ | $F_j$ |
|---|---|---|
| 1 | $1$ | $\frac95 - \frac45 q^{-1}$ |
| 2 | $1 + \frac95 q^{-1}$ | $\frac{61}{25} - \frac{36}{25} q^{-1}$ |

$F_j(1) = 1$ in both rows, as it must be because $\tilde A(1) = 0$. The step response coefficients are $g = (0, 0.2, 0.36, 0.488, 0.5904, \dots)$, the DMC step response.

**The gain.** With $N_1 = 1$, $N_2 = 10$, $N_u = 2$ and $\lambda = 0.1$, $G$ is the dynamic matrix of DMC with $P = 10$, $M = 2$, so $K$ is the same vector, with $\sum_j K_j = 1.8422$.

**The RST form.** The law is $R(q^{-1})\, \Delta u(t) = T\, w - S(q^{-1})\, y(t)$ with

$$R = 1 + 0.8962\, q^{-1}, \qquad S = 5.4268 - 3.5846\, q^{-1}, \qquad T = 1.8422.$$

$S(1) = 1.8422 = T$, which gives unit steady-state gain. The closed-loop polynomial is $P_c = \tilde A R + q^{-1} B S = 1 - 0.9038\, q^{-1} + 0.2723\, q^{-2}$. Its roots are $0$ and $0.4519 \pm 0.2609\, i$, of modulus $0.5218$, inside the unit circle, so the loop with the exact model is Schur.

**Setpoint and disturbance.** For a unit setpoint step from rest, the outputs are $0, 0.3684, 0.7015, 0.9021, 0.9928, 1.0202, \dots$, the same as with DMC. For a step of 0.3 added to the measured output from $t = 25$ (measurement with the implementation), the two methods differ:

| sample after the step | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| GPC | 1.3 | 1.3 | 0.9744 | 0.8952 | 0.9122 | 0.9492 | 0.9780 |
| DMC | 1.2999 | 1.2999 | 1.1894 | 1.0896 | 1.0295 | 1.0025 | 0.9946 |

GPC treats the jump as noise that enters through $1/\tilde A$, so it predicts that the output will keep rising and acts harder; for a pure output step this gives an undershoot. DMC assumes the jump stays constant, which is right for this disturbance. For a load that enters the difference equation, the CARIMA assumption is the right one. In the tests, GPC removes such a load with no offset, also when the plant is $1 - 0.85\, q^{-1}$ with $B = 0.12\, q^{-1}$ or $0.3\, q^{-1}$ instead of the model.

**Other tunings** (with the same model, $\lambda = 0$, $N_u = 1$):

| $N_1$ | $N_2$ | closed-loop pole | $T$ |
|---|---|---|---|
| 2 | 10 | 0.7101 | 1.4496 |
| 1 | 20 | 0.7664 | 1.1679 |
| 1 | 50 | 0.7896 | 1.0519 |
| 2 | 2 | 0 | 5 |

With $N_u = 1$ and a long output horizon the pole moves toward the open-loop pole 0.8. With $N_1 = N_2 = 2$, the delay plus one, all closed-loop poles are at 0: $R = 1 + 1.8\, q^{-1}$, $S = 12.2 - 7.2\, q^{-1}$, $T = 5$, which is [deadbeat control](/deadbeat-control/).

## Correctness

The proofs are in proofs/correctness.md.

1. **The Diophantine identity** has a unique solution with $\deg E_j \le j - 1$ and $\deg F_j \le a$, and $F_j(1) = 1$ (Lemma 1).
2. **The predictor** is the minimum mean square error predictor of $y(t + j)$ for the CARIMA model, and it is exact when the noise is zero after time $t$ (Lemma 2).
3. **The split** into $G\, \Delta U + f$ holds because $G_j$ agrees with $B / \tilde A$ up to order $j - 1$ (Lemma 3).
4. **The move** is the unique least squares minimizer for $\lambda > 0$, or for $\lambda = 0$ when $G$ has full column rank (Lemma 4).
5. **RST form and zero offset (theorem).** The law is $R\, \Delta u = T w - S y$ with $S(1) = T$. If the closed loop is Schur, a constant setpoint and a constant load give $y \to w$, also under model error that keeps the loop Schur. The theorem says nothing about where the closed-loop poles are; they must be checked.

## Complexity

Costs are in the [real-RAM model](/real-ram/), with $N = N_2$, $M = N_u$, $a = \deg A$ and $b = \deg B$, for one input and one output.

- **Offline.** Each long division to $j$ terms costs $O(j a)$, and $G_j = E_j B$ costs $O(j b)$, so $O(N^2 (a + b))$ for all $j$. The divisions can also be done recursively in $O(a)$ per step of $j$, which gives $O(N (a + b))$. The gain costs $O(N M^2 + M^3)$ with a [Cholesky factorization](/cholesky-decomposition/).
- **Online, per sampling instant.** The free response costs $O(a + b)$ for each $j$, so $O(N (a + b))$, and line L6 costs $O(N)$. In RST form the law costs only $O(a + b)$.
- **Space.** $O(N^2)$ for the polynomials $E_j$, which can be dropped after setup, $O(N (a + b))$ for $F_j$ and the tails of $G_j$, and $O(N M)$ for $G$.

## Properties

- **Linear time-invariant controller** without constraints, of RST form with the factor $\Delta$, so it has integral action.
- **No general stability guarantee.** Theorem 1 of the proof file does not locate the poles. Some choices of the horizons and $\lambda$ give an unstable loop; check the roots of $P_c$.
- **Handles integrating and unstable plants.** The model is a transfer function, so $A$ may have roots on or outside the unit circle, which DMC with a finite step response cannot represent.
- **Same setpoint response as DMC** when the step response of DMC is the step response of $q^{-1} B / A$ and the horizons match ($N_1 = 1$, $N_2 = P$, $N_u = M$); the disturbance responses differ, as in the table.
- **Few parameters to estimate.** The model has $a + b + 1$ numbers, which a recursive estimator can update online; with such an estimator GPC is a [self-tuning regulator](/self-tuning-regulator/).

## Variants and improvements

- **The noise polynomial or $T$ filter.** The CARIMA model can carry a noise polynomial, $C(q^{-1})\, e(t) / \Delta$, and in practice a designer filter $T$ often takes its place. It changes the predictor and the disturbance response; with an exact model it does not change the setpoint response.
- **Constrained GPC.** With input or output limits, each step is a [quadratic program](/quadratic-programming/), as in [linear MPC](/linear-mpc/).
- **Multivariable GPC.** $A$ and $B$ become polynomial matrices; the Diophantine identity is solved with matrix polynomials.
- **Setpoint preview.** A known future setpoint $w(t + j)$ replaces $w \mathbf{1}$ in line L6.
- **Stabilizing variants.** Terminal equality constraints on the predicted outputs and increments can be added to get a stability guarantee, in the spirit of the [MPC stability theorem](/mpc-stability-theorem/).

## When to use it

Use GPC for single-loop or small plants that are well described by a low-order transfer function, especially when the model is estimated online, as in adaptive control. It handles dead time by leading zeros in $B$ and integrating plants directly. For many inputs and outputs with constraints, a state-space [linear MPC](/linear-mpc/) is usually simpler to set up and analyze.

## Pitfalls

- **Rank loss with a dead time.** If $\lambda = 0$ and the horizons do not cover the dead time, $G$ loses rank. In the example, $N_1 = 1$, $N_2 = 3$, $N_u = 3$, $\lambda = 0$ gives a singular $G^T G$. Choose $N_2 \ge N_u + \tau$, or use $\lambda > 0$.
- **Instability for some tunings.** GPC does not guarantee an asymptotically stable loop. Check the roots of $P_c$ for the model, and test with model error.
- **Noise model mismatch.** The default model assumes integrated noise through $1 / A$. For output steps or measurement noise this gives an aggressive response; use the $T$ filter.
- **Deadbeat tuning.** $N_1 = N_2 = \tau + 1$, $N_u = 1$, $\lambda = 0$ gives all poles at 0 but large inputs ($T = 5$ in the example), and it is sensitive to model error.
- **Clipping the input.** Clipping $u$ after line L7 without telling the controller the applied value gives windup. Store the applied increment, or solve the constrained problem.

## Implementations

## History

Clarke, Mohtadi and Tuffs published GPC in 1987 in two papers in Automatica: the basic algorithm and the extensions and interpretations. It came from self-tuning control, where the plant model is a transfer function estimated online. It used the same receding horizon idea as the industrial methods based on step and impulse responses, such as [DMC](/dynamic-matrix-control/). Qin and Badgwell (2003) place GPC in the history of MPC next to these industrial methods.

## References
