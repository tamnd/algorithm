---
tag: 5R0MXZ
kind: algorithm
slug: unconditionally-stable-maccormack
name: Unconditionally stable MacCormack method
aliases:
- semi-Lagrangian MacCormack
area: graphics-and-signals/fluid-animation
level: advanced
summary: "Advect forward, trace the result back, and add half the round trip error to the forward result. Second order for smooth fields; a limiter keeps each value in its stencil range."
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {g: "the number of grid samples of the field"}
  time: {step: "Θ(g)", limiter: "Θ(g)"}
  space: {extra: "Θ(g)"}
properties: {deterministic: true, exact: false, unconditionally_stable: true, conservative: false}
history:
  year: 2008
  people: [Andrew Selle, Ronald Fedkiw, ByungMoon Kim, Yingjie Liu, Jarek Rossignac]
  note: Selle and colleagues derived a two-step form of BFECC with semi-Lagrangian steps and a limiter that keeps it stable for any time step.
prereqs: [stable-fluids, bfecc, method-of-characteristics, bilinear-interpolation]
see_also: [maccormack-method, bfecc, stable-fluids, level-set-method, runge-kutta-methods, courant-friedrichs-lewy-condition, vorticity-confinement, fluid-implicit-particle]
sources:
  - paper: doi:10.1007/s10915-007-9166-4
    title: "Andrew Selle, Ronald Fedkiw, ByungMoon Kim, Yingjie Liu and Jarek Rossignac, An unconditionally stable MacCormack method, Journal of Scientific Computing 35(2-3), 350-371, 2008"
    locator: "the two-step method, its relation to BFECC and to Runge-Kutta on an ordinary differential equation, the limiter, and the convergence tables"
  - paper: doi:10.1016/s0021-9991(03)00276-6
    title: "Todd F. Dupont and Yingjie Liu, Back and forth error compensation and correction methods for removing errors induced by uneven gradients of the level set function, Journal of Computational Physics 190(1), 311-324, 2003"
    locator: the BFECC step that the method simplifies
  - book: isbn:9781482232837
    title: "Robert Bridson, Fluid Simulation for Computer Graphics, second edition, CRC Press, 2015"
    locator: the chapter Advection Algorithms
---

The unconditionally stable MacCormack method of Selle, Fedkiw, Kim, Liu and Rossignac (2008) is a sharper advection step for grid fluids. It does one [semi-Lagrangian](/method-of-characteristics/) step forward and one back, and uses half of the round trip error to correct the forward result. That makes it second order for smooth fields, at the cost of two plain steps, one fewer than [BFECC](/bfecc/). A limiter falls back to the plain step wherever the corrected value leaves the range of the old values that the plain step used. With the limiter, the step stays bounded for any time step and any velocity. The name refers to the predictor-corrector structure. The method is not the 1969 [MacCormack method](/maccormack-method/) for compressible flow, which is explicit and has a CFL limit.

## In plain words

Moving smoke one step with the plain method blurs it a little. This method measures that blur and takes it back.

It moves the smoke forward one step, which gives a blurred result. Then it moves that result back one step with the same method. If nothing were lost, this would give back the start. In fact it gives a picture that was blurred twice. Half of the difference from the start is about one blur, so the method adds that half to the forward result.

The correction can push a value past the old range near a sharp edge. There the method simply keeps the plain forward value, which never leaves that range.

## The problem

Given a field $q$ on a grid, a velocity field $\mathbf u$ and a time step $\Delta t$, find the field at the next step for the advection equation $\partial q / \partial t + \mathbf u \cdot \nabla q = 0$. The plain semi-Lagrangian step of [stable fluids](/stable-fluids/) is stable for any $\Delta t$ but first order, and it smears small features. The goal is a second order step that keeps that stability and costs only a small multiple of the plain step.

## The algorithm

Let $A$ be the plain semi-Lagrangian step and $A^R$ the same step with $-\Delta t$.

```pseudo id=main
MACCORMACK(q, u, dt)
L1  q_hat <- A(q)                                   ▷ predictor: the plain forward step
L2  q_check <- A^R(q_hat)                           ▷ trace the predictor back to the start time
L3  q_new <- q_hat + (q - q_check) / 2              ▷ corrector: add half the round trip error
L4  for each sample: [lo, hi] <- range of the values of q that L1 mixed at its foot
L5  where q_new is outside [lo, hi]: q_new <- q_hat (revert), or clamp it to [lo, hi]
```

**Why it works.** If the plain step has the error $e$, then $\hat q \approx q_{\text{exact}} + e$, and the round trip $\check q \approx q + 2e$. So $\frac12 (q - \check q) \approx -e$, and line L3 removes the error of the forward step. For $y' = \lambda y$ with forward Euler as the plain step, line L3 gives exactly $(1 + \lambda h + \frac12 \lambda^2 h^2) y$, the second order Taylor step.

**The relation to BFECC.** BFECC uses the same error estimate, but it corrects the start and then does a third plain step. MacCormack corrects the end directly, which saves one step. Selle and colleagues report that both are second order on smooth problems, and the analysis on the proof page agrees.

**The limiter (L4, L5).** The plain value at a point is a weighted mean of the four (in 3D, eight) old values around the foot of its backtrace, so it lies in their range. The corrected value may not. There are two choices: clamp to the range, or revert to the plain value. Selle and colleagues revert, and this page does the same by default. In the tests of this page the two give similar results.

**On a MAC grid.** Advect $u$, $v$ and each scalar with their own sample points, and take all backtraces in the velocity field from the start of the step.

## Example

**One step by hand.** A row of 7 cells with $\Delta x = 1$ m, $u = 0.5$ m/s and $\Delta t = 1$ s, so the CFL number is $0.5$. The plain step is $(A q)_a = \frac12 q_a + \frac12 q_{a - 1}$, and the reverse step is $\frac12 q_a + \frac12 q_{a+1}$. Start with a spike at cell 3:

| cell | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $q$ | 0 | 0 | 1 | 0 | 0 |
| $\hat q$ (L1) | 0 | 0 | 0.5 | 0.5 | 0 |
| $\check q$ (L2) | 0 | 0.25 | 0.5 | 0.25 | 0 |
| $q^{\text{new}}$ (L3) | 0 | -0.125 | 0.75 | 0.375 | 0 |
| after revert (L5) | 0 | 0 | 0.75 | 0.375 | 0 |

The exact spike would sit at the position $3.5$. The plain step splits it into $0.5$ and $0.5$. MacCormack keeps more height but is not symmetric: it moves the mass less than the exact half cell, and it dips to $-0.125$ at cell 2. The plain step at cell 2 mixes two zeros, so the limiter reverts that value to 0. The sum is 1 before the limiter and 1.125 after it.

**Measured on a smooth bump.** A bump of radius 0.3 m moves for 0.25 s with the velocity $(1, 0.5)$ m/s on a square of 1 m, at the CFL number $4/3$ in $x$:

| method | 16 by 16 | 32 by 32 | observed order |
|---|---|---|---|
| plain semi-Lagrangian | 0.197 | 0.106 | 0.89 |
| MacCormack | 0.158 | 0.0492 | 1.68 |
| MacCormack with revert | 0.158 | 0.0503 | 1.65 |

On the same test, BFECC has the error 0.00684 at 32 cells. The proof page explains the gap: the error constant of MacCormack has a term that does not shrink when the step grows. At 32 cells, the MacCormack error is 0.0486 with 12 steps and 0.0492 with 6 steps.

**Rotation and a sharp edge, measured.** A bump of radius 0.2 m turns a quarter turn on a 32 by 32 grid in 16 steps. The largest error is 0.157 without the limiter, 0.188 with revert and 0.160 with clamp, against 0.375 for the plain step. A square of height 1 moved for five steps reaches 1.31 and -0.25 without the limiter, and it stays in $[0, 1]$ with either limiter.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Constants.** A constant field stays exactly the same.
2. **Stability.** On a periodic grid with a constant velocity, the step without the limiter multiplies each Fourier mode by $G = A + \frac12 (1 - |A|^2)$, where $A$ is the factor of the plain step. For every CFL number, $|G| \le 1$.
3. **Order.** Under the same conditions, $G$ differs from the exact factor by $O(\theta^3)$, so the error after a fixed time is $O(\Delta x^2)$ at a fixed CFL number. The constant is $\alpha + \beta / c$, where $\alpha$ and $\beta$ depend only on the fractional part of the CFL number $c$.
4. **Limiter.** With "revert" or "clamp", each new value lies in the range of the old values at the foot of its backtrace. So the field stays between its old minimum and maximum, for any velocity and any $\Delta t$.

The tests check the symbol against the code to $10^{-13}$, the measured order, the error at two step sizes, the exact result at a whole number of cells per step, the rotation, and the range of the limited values.

## Complexity

Let $g$ be the number of samples. Each plain step costs $\Theta(g)$, so lines L1 to L3 cost about twice the plain step. The limiter needs the stencil range at the foot of each forward backtrace. An implementation can record it during line L1; the code here recomputes the backtraces. The extra space is $\Theta(g)$ for $\hat q$, $\check q$ and the ranges.

## Properties

- **Second order for smooth fields** under a constant velocity, with two plain steps per step.
- **Bounded at any step size** with the limiter, for any velocity field.
- **Not conservative.** The sum of the field is not kept, and the limiter changes it more.
- **Not symmetric.** The correction is applied to the forward result, so a spike moves unevenly, as in the example above.
- **Generic.** It wraps any advection step that has a reverse, without looking inside it.

## Variants and improvements

- **BFECC.** [BFECC](/bfecc/) corrects the start instead and does a third plain step. In the bump test of this page it is about 7 times more accurate, at 1.5 times the cost.
- **Clamp or revert.** The two limiters of the paper. Reverting keeps the plain value and can lose more detail near smooth extrema; clamping keeps more of the correction.
- **Higher order interpolation.** A cubic sample in place of the bilinear one reduces the error of each plain step, and the correction then works on a smaller error.
- **Velocity advection.** Applied to the velocity, the method keeps more of the small swirls than the plain step. A [vorticity confinement](/vorticity-confinement/) force may then be weaker or not needed.

## When to use it

Use it as the default advection in a grid smoke or fire solver when the plain step smears too much. It adds one plain step per field and a limiter, and it keeps the large steps that make semi-Lagrangian solvers attractive. Use BFECC instead if the extra plain step is affordable and the field is smooth.

For liquid surfaces, use it on the level set together with a limiter, or use particles such as the [particle level set](/particle-level-set/) or [FLIP](/fluid-implicit-particle/) for thin features.

## Pitfalls

- **Confusing it with the 1969 MacCormack method.** That scheme is an explicit finite difference predictor-corrector for compressible flow. It has a CFL limit, and this method has none.
- **No limiter.** The step creates new extrema at sharp edges. Smoke density goes negative, and a velocity field can gain energy.
- **The wrong range.** The limiter must use the values of $q$ that the forward step mixed, not those of $\hat q$ or a global range.
- **The reverse step.** Use the same velocity field with $-\Delta t$. A reverse step with an updated velocity breaks the cancellation.
- **Boundaries.** Near walls and inflow borders the clamped samples are not symmetric, and the order drops.
- **Stable is not accurate.** The error constant does not shrink with a larger step, so a large step is not a cheap way to reach a given accuracy.

## Implementations

## History

The back and forth idea came from Dupont and Liu (2003), who used it for level sets as BFECC. Kim, Liu, Llamas and Rossignac then used BFECC with semi-Lagrangian steps in fluid animation. In 2008, Selle, Fedkiw, Kim, Liu and Rossignac observed that the error estimate of BFECC can correct the forward result directly. This removes one of the three steps and gives a scheme with the predictor-corrector form of MacCormack's method. They added the limiter that keeps it bounded for any step and showed second order convergence in their tests.

## References
