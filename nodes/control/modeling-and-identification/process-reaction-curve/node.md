---
tag: QACT9Z
kind: algorithm
slug: process-reaction-curve
name: Process reaction curve method
aliases:
- FOPDT model fitting
- step response model fitting
area: control/modeling-and-identification
level: intro
summary: Fits a first-order plus dead time model to the open-loop step response from its gain, its delay and its time constant.
solves: [system-identification]
model: real-ram
complexity:
  vars: {n: the number of samples}
  time: {worst: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: false, recursive: false, exact: false}
history:
  year: 1942
  people: [John G. Ziegler, Nathaniel B. Nichols]
  note: "Ziegler and Nichols read a delay and a slope off the recorded reaction curve of a process and gave PID settings in terms of them; Cohen and Coon in 1953 based their tuning formulas on the same first-order plus dead time model."
prereqs: [laplace-transform, time-delay-system, system-identification]
see_also: [ziegler-nichols-tuning, pid-controller, internal-model-control, smith-predictor, relay-autotuning, pade-approximation, transfer-function, empirical-transfer-function-estimate]
sources:
  - paper: "John G. Ziegler and Nathaniel B. Nichols, Optimum settings for automatic controllers, Transactions of the ASME 64, 759-768, 1942"
    locator: the reaction curve method, the apparent dead time and the reaction rate read from the tangent at the steepest point, and the controller settings derived from them
  - paper: "G. H. Cohen and G. A. Coon, Theoretical consideration of retarded control, Transactions of the ASME 75, 827-834, 1953"
    locator: controller settings for a first-order process with dead time identified from the reaction curve
  - book: isbn:9781556179426
    title: "Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006"
    locator: "the chapter on process models (step response methods, the tangent and area methods, and first-order plus dead time models)"
  - paper: doi:10.1016/S0959-1524(02)00062-8
    title: "Sigurd Skogestad, Simple analytic rules for model reduction and PID controller tuning, Journal of Process Control 13(4), 291-309, 2003"
    locator: the first-order plus dead time model and the SIMC tuning rules
---

The process reaction curve method fits the first-order plus dead time (FOPDT) model

$$G(s) = \frac{K\, e^{-L s}}{T s + 1}$$

to the recorded response of a process to one step of its input, taken in open loop. The gain $K$ is the final change of the output divided by the size of the step. The dead time $L$ and the time constant $T$ come from the shape of the curve: either from the tangent at its steepest point, the classical reading of Ziegler and Nichols in 1942, or from the two times at which the normalized output reaches 28.3 and 63.2 percent of its final change. The work is one pass over the $n$ samples, $O(n)$. The two-point formulas return $L$ and $T$ exactly for a true FOPDT response, and for any other S-shaped response they return an approximation. The three numbers $K$, $L$ and $T$ are the input of many rules of thumb for tuning [PID controllers](/pid-controller/).

## In plain words

Put the process in a steady state, change its input by one fixed step, and record how the output moves until it settles again. Many processes answer in the same way: for a while nothing happens, then the output rises along an S-shaped curve and levels off. Three numbers describe that curve well enough to tune a controller. The gain says how far the output moved for each unit of input. The dead time says how long the process waited before it began to move. The time constant says how long the rise took. You can read them with a ruler from a printed curve, or compute them from the samples in one pass.

## The problem

**Input.** Sample times $t_0 < t_1 < \cdots < t_{n-1}$, the output samples $y_0, \ldots, y_{n-1}$, and the step size $\Delta u \ne 0$. The step is applied at $t_0$, the process is at rest at $y_0$ before it, and the output has settled at $y_{n-1} \ne y_0$.

**Output.** $K$, $L$ and $T$ of the FOPDT model, with $L$ measured from $t_0$. Its unit step response is 0 for $t < L$ and $K\big(1 - e^{-(t - L)/T}\big)$ for $t \ge L$.

## The algorithm

```pseudo id=main
FOPDT-FIT(t, y, Δu, ⟨method⟩)
L1  K ← (y_(n-1) - y_0) / Δu
L2  z_i ← (y_i - y_0) / (y_(n-1) - y_0) for every i
L3  if ⟨method⟩ = two-point then
L4      t28, t63 ← the first times, after t_0, at which z reaches 1 - e^(-1/3) and 1 - e^(-1), by linear interpolation between samples
L5      T ← 1.5 · (t63 - t28)
L6      L ← t63 - T
L7  else: (s, tm, zm) ← the slope and the midpoint of the steepest chord (z_(i+1) - z_i) / (t_(i+1) - t_i)
L8      L ← tm - zm / s
L9      T ← 1 / s
L10 return (K, L, T)
```

Line L2 scales the curve so that it goes from 0 to 1; the levels of L4 are then $1 - e^{-1/3} \approx 0.2835$ and $1 - e^{-1} \approx 0.6321$. For an FOPDT curve these levels are reached at $L + T/3$ and $L + T$, so their distance is $2T/3$, which gives L5 and L6. Lines L7 to L9 are the tangent method on sampled data: the steepest chord stands for the tangent at the inflection point, and the line through the chord midpoint with slope $s$ crosses $z = 0$ at $L$ and $z = 1$ at $L + 1/s$.

## Example

Take the process $1/(s+1)^3$, three equal first-order lags in series, a unit step and samples every $0.5$ s. Its step response is $y(t) = 1 - e^{-t}(1 + t + t^2/2)$, so $K = 1$ and $z = y$.

| $t$ | $0.5$ | $1.0$ | $1.5$ | $2.0$ | $2.5$ | $3.0$ | $3.5$ |
|---|---|---|---|---|---|---|---|
| $y(t)$ | $0.0144$ | $0.0803$ | $0.1912$ | $0.3233$ | $0.4562$ | $0.5768$ | $0.6792$ |
| slope of the chord ending at $t$ | $0.0288$ | $0.1318$ | $0.2217$ | $0.2643$ | $0.2657$ | $0.2412$ | $0.2047$ |

**Two-point.** L4 interpolates $t_{28} = 1.8492$ between $1.5$ and $2.0$, and $t_{63} = 3.2702$ between $3.0$ and $3.5$. L5 gives $T = 1.5 \cdot 1.4210 = 2.1315$ and L6 gives $L = 3.2702 - 2.1315 = 1.1387$.

**Tangent.** The steepest chord is the one from $2.0$ to $2.5$, with $s = 0.2657$ and midpoint $(2.25, 0.3898)$. L8 gives $L = 2.25 - 0.3898/0.2657 = 0.7832$ and L9 gives $T = 3.7633$.

**Fine sampling (computation).** The exact curve has its inflection point at $t = 2$ with slope $2e^{-2}$, so the true tangent gives $L = (9 - e^2)/2 = 0.8055$ and $T = e^2/2 = 3.6945$, and the exact crossing times give $L = 1.1496$ and $T = 2.1087$. With samples every $0.01$ s the algorithm returned $(0.80546, 3.69456)$ and $(1.14959, 2.10867)$.

The two models are different approximations of the same curve. At $\omega = 0.5$ rad/s the true gain is $0.7155$ and the true phase $-1.3909$ rad; the tangent model gives $0.4761$ and $-1.4774$, the two-point model $0.6882$ and $-1.3866$ (computation). The tangent model has the larger time constant and the smaller delay, so it underestimates the gain at middle frequencies.

## Correctness

**Claim.** Suppose the samples come from an FOPDT response, $y_i = y_0 + K \Delta u \big(1 - e^{-(t_i - t_0 - L)/T}\big)$ for $t_i \ge t_0 + L$ and $y_i = y_0$ before, except that the last sample holds the settled value $y_0 + K \Delta u$, and that the record is long enough (made precise in the proof). Then L1 returns $K$ exactly. If the crossing times of L4 are read from the continuous curve, the two-point method returns $L$ and $T$ exactly; with linear interpolation and sample spacing $h \le T/3$, each crossing time is off by at most $h^2 e^{h/T}/(8T)$. If $t_0 + L$ is a sample time and the spacing near it is $h$, the tangent method returns $L$ exactly and $T$ as $h/(1 - e^{-h/T}) = T + h/2 + O(h^2)$.

**Key invariant.** After L2, $z(t) = 1 - e^{-(t - t_0 - L)/T}$ for $t \ge t_0 + L$. This is concave, so the chords to the right of $t_0 + L$ get flatter, and the steepest chord is the first one after the dead time.

The two-point formula follows from $z(L + T/3) = 1 - e^{-1/3}$ and $z(L + T) = 1 - e^{-1}$. The tangent result follows because the line through the first chord after the dead time meets $z = 0$ exactly at its left end. The full proof is below.

## Complexity

Line L1 is $O(1)$, line L2 is $O(n)$, the two scans of L4 and the scan of L7 are $O(n)$ each, and the rest is $O(1)$. The total is $O(n)$ arithmetic operations in the [real RAM](/real-ram/), plus two evaluations of $e^x$ for the levels, with $O(n)$ extra space for the normalized curve; computing $z_i$ on the fly lowers this to $O(1)$.

## Properties

- **Exact for FOPDT data (theorem).** As stated in the claim, for the two-point method with exact crossings and for the tangent method with the dead time on the sample grid.
- **Not exact for other curves.** A process of higher order has no exact FOPDT model, and the two methods give different models, as in the example. The two-point model matches the curve at two points by design; the tangent model matches the steepest slope.
- **Noise sensitivity (measurement).** With Gaussian noise of standard deviation $0.01$ added to the $0.01$ s samples of the example, the tangent method gave $L = 8.55$ and $T = 0.19$, because the steepest chord between two noisy samples is set by the noise. The two-point method gave $L = 1.034$ and $T = 2.170$.
- **Gain error from an unsettled record.** If the record stops at time $t_e$ before the output has settled, L1 returns $K\big(1 - e^{-(t_e - t_0 - L)/T}\big)$ for FOPDT data, and the levels of L4 shift with it.
- **Open loop only.** The method needs the process to be BIBO stable and to settle; an integrating or unstable process has no final value.

## Variants and improvements

- **Other pairs of levels.** Several published two-point rules use other pairs of levels, such as 35.3 and 85.3 percent; any two levels $z_1, z_2$ give $T = (t_2 - t_1)/\ln\big((1 - z_1)/(1 - z_2)\big)$.
- **Area method.** Compute the area between the final value and the curve, which equals $K (L + T)$ for an FOPDT model, and a second area to separate $L$ from $T$. Integrals average the noise, so this is much less sensitive than the tangent method.
- **Least squares fit.** Fit $K$, $L$ and $T$ to all samples by nonlinear least squares, an [output error](/output-error-model/) fit with a step input and a delay.
- **Second-order plus dead time.** Fit two time constants and a delay when the curve is clearly more sluggish than one lag.
- **Integrating processes.** Fit $K e^{-L s}/s$ from the slope of the final ramp and its intercept with the time axis.
- **Closed-loop alternatives.** The [relay autotuning](/relay-autotuning/) test identifies one point of the frequency response with the loop closed.

## When to use it

Use it to get a first model of a stable, well-damped process that can be run in open loop for one step test, as for many temperature, level and flow loops in the process industry, and to tune a PID controller from that model. Prefer the two-point or area method to the tangent method on measured data. Use a parametric fit or a frequency method when the process oscillates, when the dead time must be known accurately, or when the model will be used for more than tuning.

The tuning rules that start from $K$, $L$ and $T$ are not part of the fit; they are rules of thumb.

- **Ziegler and Nichols.** For a PID controller, $K_p = 1.2\, T/(K L)$, $T_i = 2L$ and $T_d = 0.5 L$ (Ziegler and Nichols 1942); see [Ziegler-Nichols tuning](/ziegler-nichols-tuning/). On the tangent model of the example this gives $K_p = 5.5041$, $T_i = 1.6109$ and $T_d = 0.4027$; on the two-point model, $K_p = 2.2011$, $T_i = 2.2992$ and $T_d = 0.5748$. The rule aims at a quarter amplitude decay, which is often too aggressive.
- **Cohen and Coon.** Settings derived for the same model, with more attention to processes where $L$ is large compared with $T$ (Cohen and Coon 1953).
- **SIMC.** For a PI controller with a desired closed-loop time constant $\tau_c$, $K_p = T/\big(K (\tau_c + L)\big)$ and $T_i = \min\big(T, 4(\tau_c + L)\big)$, with $\tau_c = L$ as a default (Skogestad 2003). The [internal model control](/internal-model-control/) view gives rules of the same kind.

## Pitfalls

- **Normalizing by an unsettled value.** Stopping the record early makes $y_{n-1}$ in L1 and L2 too small, so $K$ is too small and every level of L4 is reached too early. Record until the output has settled, and use the settled value in L1 and L2.
- **The tangent on raw noisy samples.** The steepest chord of L7 on noisy data is a noise spike. Filter the samples or fit a smooth curve before L7, or use the two-point lines L4 to L6.
- **Measuring $L$ from the wrong origin.** L4 and L8 must measure time from the moment $t_0$ of the step. Measuring it from the start of the record adds the idle time before the step to $L$.
- **A step that is too small or too large.** A small step drowns in noise and a large one drives the process out of its linear range. Choose $\Delta u$ in L1 so that the output change is several times the noise level, and check that a step of the opposite sign gives a similar $K$.
- **Disturbances during the test.** A load change during the recording is read as part of the response. Repeat the test, and in L1 and L2 use only records where the output starts from a steady value.

## Implementations

## History

Ziegler and Nichols in 1942 proposed to record the reaction curve of a process after a step of the controller output, to draw the tangent at its steepest point, and to read from it an apparent dead time and a reaction rate; their controller settings were given in terms of these two numbers. Cohen and Coon in 1953 derived settings from the first-order plus dead time model that the curve suggests. Two-point readings based on fixed percentages of the final change, and area methods, came later to make the reading less dependent on drawing a tangent. Skogestad's rules of 2003 are a modern set of tuning formulas built on the same three numbers.

## References
