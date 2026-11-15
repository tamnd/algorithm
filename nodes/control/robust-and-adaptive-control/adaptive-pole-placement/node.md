---
tag: G5MEWV
kind: algorithm
slug: adaptive-pole-placement
name: Adaptive pole placement
aliases:
- indirect adaptive pole placement
area: control/robust-and-adaptive-control
level: advanced
summary: A self-tuning controller that solves a polynomial pole placement equation for the current plant estimate at each step.
model: real-ram
complexity:
  vars: {N: the number of samples, n: the order of the plant model}
  time: {worst: O(N n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 1979
  people: [Peter E. Wellstead, D. Prager, P. Zanker, Karl Johan Åström, Björn Wittenmark]
  note: "Wellstead, Prager and Zanker (1979) and Åström and Wittenmark (1980) proposed self-tuning regulators that place the closed loop poles, which removed the restriction of minimum variance control to minimum phase plants."
prereqs: [self-tuning-regulator, pole-placement-problem, sylvester-matrix, rls-algorithm, certainty-equivalence]
see_also: [extended-euclidean-algorithm, resultant, pole-placement-theorem, two-degree-of-freedom-control, parameter-projection, persistent-excitation, internal-model-principle, model-reference-adaptive-control]
sources:
  - book: isbn:9780486462783
    title: "Karl Johan Åström and Björn Wittenmark, Adaptive Control, second edition, Addison-Wesley 1995 (Dover reprint 2008)"
    locator: "Chapter 3, Deterministic self-tuning regulators: the pole placement design with the Diophantine equation and the indirect self-tuning regulator"
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Chapter 7, Adaptive pole placement control: the indirect schemes and Section 7.6 (the stabilizability problem and its solution by projection)"
  - paper: "P. E. Wellstead, D. Prager and P. Zanker, Pole assignment self-tuning regulator, Proceedings of the IEE 126(8), 1979"
    locator: "pages 781 to 787"
---

Adaptive pole placement is an indirect [self-tuning regulator](/self-tuning-regulator/): at every sample it updates a plant model $\hat A(q)$, $\hat B(q)$ by recursive least squares, solves the polynomial [pole placement](/pole-placement-problem/) equation $\hat A R + \hat B S = A_c A_o$ for the controller polynomials $R$ and $S$, and applies the controller $R u = T u_c - S y$. The equation is a linear system with a [Sylvester matrix](/sylvester-matrix/), which has a unique solution exactly when $\hat A$ and $\hat B$ are coprime. Unlike the minimum variance self-tuner it does not cancel the plant zeros, so it works for plants with zeros outside the unit circle. Its weak point is the estimate itself: when $\hat A$ and $\hat B$ are close to a common factor, the design is ill conditioned, and the scheme needs a fix such as [parameter projection](/parameter-projection/).

## In plain words

The controller has two parts that run at every sample. The first part keeps a model of the plant and corrects it from the newest measurement. The second part asks: if this model were the true plant, which controller would give the closed loop the response that I want? It answers by solving a small set of linear equations. Then it applies that controller for one sample, and the cycle repeats. The wanted response is fixed by the designer as a set of pole positions. Trouble comes when the model, by chance, looks like a plant that no controller can fix, because a pole and a zero of the model almost cancel. The design then gives huge gains, so a practical version keeps the model away from such points.

## The problem

The plant is $A(q) y_t = B(q) u_t + e_t$, with the forward shift operator $q$, $A = q^n + a_1 q^{n-1} + \dots + a_n$ monic and $B = b_0 q^{n-1} + \dots + b_{n-1}$, so the delay is one sample. The coefficients are unknown, $A$ and $B$ are coprime, and the sign and a lower bound $b_{\min} > 0$ of $b_0$ are known. The designer chooses the closed loop polynomial $A_c$ of degree $n$ and an observer polynomial $A_o$ of degree $n - 1$, both with all zeros inside the unit circle. The aim is a controller

$$R(q) u_t = T(q) u_{c,t} - S(q) y_t$$

that gives the closed loop $y = \frac{B T}{A R + B S} u_c$ the characteristic polynomial $A_c A_o$ and the static gain 1. With $R$ monic of degree $n - 1$ and $S$ of degree $n - 1$, this is the Diophantine equation

$$A R + B S = A_c A_o,$$

and $T = t_0 A_o$ with $t_0 = A_c(1)/B(1)$, so that $y = t_0 B/A_c\,u_c$: the observer polynomial cancels, and the zeros of $B$ stay in the response. This is a [two-degree-of-freedom](/two-degree-of-freedom-control/) design.

## The algorithm

```pseudo id=main
ADAPTIVE-POLE-PLACEMENT(A_c, A_o, θ₀, p₀, b_min, N)
L1  θ̂ ← θ₀; P ← p₀ I; R, S, T ← the design for θ₀
L2  for t ← 0 to N - 1 do
L3      measure y_t; φ ← (-y_{t-1}, …, -y_{t-n}, u_{t-1}, …, u_{t-n})
L4      update θ̂ and P by one RLS step with (φ, y_t)
L5      if b̂₀ < b_min then b̂₀ ← b_min           ▷ projection
L6      Â ← (1, â₁, …, â_n); B̂ ← (b̂₀, …, b̂_{n-1})
L7      if |det Syl(Â, B̂)| > tol and |B̂(1)| > tol then
            solve Â R + B̂ S = A_c A_o; T ← (A_c(1)/B̂(1)) A_o
L8      u_t ← from R u = T u_c - S y               ▷ certainty equivalence
L9  return θ̂
```

Line L7 writes $R = q^{n-1} + r_1 q^{n-2} + \dots + r_{n-1}$ and $S = s_0 q^{n-1} + \dots + s_{n-1}$ and compares the coefficients of $q^{2n-2}, \dots, q^0$. This gives $2n - 1$ linear equations in the $2n - 1$ unknowns, with a matrix whose columns are shifted copies of the coefficients of $\hat A$ and $\hat B$. Its determinant is, up to sign, the [resultant](/resultant/) of $\hat A$ and $\hat B$. If the test in line L7 fails, the controller of the last sample is kept. Line L8 divides the controller equation by $q^{n-1}$ to get $u_t$ from past values.

## Example

Take $A = q^2 - 1.5q + 0.7$ (poles $0.75 \pm 0.37j$, inside the unit circle but lightly damped) and $B = q + 0.5$. The designer chooses $A_c = (q - 0.5)^2 = q^2 - q + 0.25$ and $A_o = q$.

**The design for the true plant.** With $R = q + r_1$ and $S = s_0 q + s_1$, the coefficients of $q^2$, $q^1$ and $q^0$ in $A R + B S = q^3 - q^2 + 0.25 q$ give

$$r_1 + s_0 = 0.5, \quad -1.5 r_1 + 0.5 s_0 + s_1 = -0.45, \quad 0.7 r_1 + 0.5 s_1 = 0.$$

The determinant of this system is $17/10$, and the exact solution is $r_1 = 7/34$, $s_0 = 5/17$, $s_1 = -49/170$. Then $t_0 = A_c(1)/B(1) = 0.25/1.5 = 1/6$ and $T = q/6$. The closed loop is $y = \frac{(q + 0.5)/6}{(q - 0.5)^2} u_c$, and its step response starts $0, 0.1667, 0.4167, 0.6250, 0.7708, 0.8646, \dots$ toward 1.

**The adaptive loop.** The estimate starts at $\hat A = q^2$, $\hat B = q + 0.1$, with $p_0 = 100$ and $b_{\min} = 0.1$. The command is a square wave of amplitude 1 that switches every 25 samples, and there is no noise. These are measurements.

| sample $t$ | $\hat a_1$ | $\hat a_2$ | $\hat b_0$ | $\hat b_1$ |
|---|---|---|---|---|
| 2 | -0.6685 | 0.0000 | 1.2168 | 0.7685 |
| 5 | -1.1671 | 0.2679 | 0.9284 | 0.9871 |
| 10 | -1.4846 | 0.6851 | 0.9876 | 0.5140 |
| 199 | -1.4965 | 0.6967 | 1.0008 | 0.5010 |
| true | -1.5 | 0.7 | 1 | 0.5 |

The first outputs are $0, 0.227, 0.909, 1.702, 1.696, 0.991, 0.295, \dots$, an overshoot of 70 percent while the model is wrong. From sample 50 on, the output differs from the response of the true design by at most $0.012$. The start $\hat B = q$ would fail: $\hat A = q^2$ and $\hat B = q$ share the factor $q$, the design does not exist, the input stays zero, and the estimator never gets data.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) proves the design step. For coprime $A$ and $B$ the Sylvester matrix is invertible (its determinant is the resultant), so line L7 has exactly one solution with $\deg R = \deg S = n - 1$, and the closed loop with the true plant has the characteristic polynomial $A_c A_o$ and the transfer function $t_0 B/A_c$ (theorem). The adaptive loop is a different matter. With the certainty equivalence design and a projection that keeps the estimates in a convex set where $\hat A$ and $\hat B$ stay uniformly coprime, the closed loop signals are bounded and the tracking error goes to zero (a theorem that Ioannou and Sun, Chapter 7, prove for the continuous-time form). Without such a set, no general guarantee is known for the plain scheme: the estimate can pass near a common factor, where the gains of the design become unbounded.

## Complexity

In the real-RAM model, one RLS step with $d = 2n$ parameters costs $O(n^2)$ operations. Building the Sylvester matrix costs $O(n^2)$, and its determinant and the solution of the Diophantine equation by Gaussian elimination cost $O(n^3)$. So $N$ samples cost $O(N n^3)$, and the memory is $O(n^2)$ for $P$ and the matrix. For the small $n$ of practice (2 to 4), the cost per sample is a few hundred operations.

## Properties

- **Non-minimum phase plants.** The design does not cancel $B$, so zeros outside the unit circle are allowed. The zeros of $B$ appear in the closed loop response.
- **Stabilizability problem.** The design needs $\hat A$ and $\hat B$ coprime. Least squares does not ensure this, and near a common factor the gains in $R$ and $S$ are large. This is the main difficulty of all indirect adaptive schemes (Ioannou and Sun, Section 7.6).
- **Static gain one.** With $T = t_0 A_o$ the static gain from $u_c$ to $y$ is 1 for the estimate; with an estimation error it is not exactly 1. Integral action in $R$, by the [internal model principle](/internal-model-principle/), gives zero static error for every model error.
- **Excitation.** Parameter convergence needs a command that is persistently exciting of order $2n$. A square wave is rich enough; a constant command is not.
- **Separation.** The estimator and the design are independent modules, so other designs (linear quadratic, model predictive) can be put in line L7.

## Variants and improvements

- **Projection on a coprime set.** Keep $\hat\theta$ in a convex set where the resultant of $\hat A$ and $\hat B$ is bounded away from zero ([parameter projection](/parameter-projection/)). This gives a proof of bounded signals but needs prior knowledge to build the set.
- **Integral action.** Choose $R = (q - 1) R'$ and solve the Diophantine equation with the extra factor. This removes static errors from load disturbances and model errors.
- **Robust estimation.** Normalization, dead zones and forgetting make the estimator tolerant of unmodeled dynamics and noise.
- **Continuous time.** The same design works with polynomials in $s$ and a continuous estimator; Ioannou and Sun treat this form.
- **Direct pole placement.** For minimum phase plants, the design can be parameterized by the controller coefficients and estimated directly, as in the [minimum variance self-tuner](/self-tuning-regulator/).

## When to use it

Use adaptive pole placement for a sampled plant of low, known order with slowly varying parameters and possibly non-minimum phase zeros, when the wanted closed loop response is given as pole positions. Add integral action and a guard against near common factors. For a minimum phase plant and a noise regulation goal, the minimum variance [self-tuning regulator](/self-tuning-regulator/) is simpler. For a plant whose full state is measured, [model reference adaptive control](/model-reference-adaptive-control/) has a cleaner stability proof.

## Pitfalls

- **Common factors in the start estimate.** A start such as $\hat A = q^2$, $\hat B = q$ has no design; the example shows that the loop then never starts learning.
- **Wrong order.** If the model order is too high, $\hat A$ and $\hat B$ get a common factor at convergence, and the design is singular.
- **Bursting.** With little excitation, the estimate drifts toward a near common factor, the loop gets large gains and bursts, and the burst brings new data. Keep a small dither or stop the update when the excitation is low.
- **Polynomial conventions.** The page writes polynomials in $q$ with the highest power first. Many books use $q^{-1}$; the coefficient lists then read in the opposite order.
- **Sampling period.** A small sampling period $h$ makes the poles cluster near 1 and the Sylvester matrix ill conditioned.

## Implementations

## History

The self-tuning regulator of Åström and Wittenmark (1973) used minimum variance control, which needs a minimum phase plant. Wellstead, Prager and Zanker (1979) replaced it by a pole assignment design, and Åström and Wittenmark (1980) gave a pole and zero placement version. The difficulty that the estimates can lose coprimeness, the stabilizability problem, was studied in the 1980s and 1990s; Ioannou and Sun (Chapter 7) give the projection solution and other fixes.

## References
