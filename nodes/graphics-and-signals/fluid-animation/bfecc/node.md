---
tag: Z26PRS
kind: algorithm
slug: bfecc
name: Back and forth error compensation and correction
aliases:
- BFECC
area: graphics-and-signals/fluid-animation
level: advanced
summary: Advect forward and back, take half the difference from the start as the error, and advect the corrected field. It is second order for smooth fields and needs a limiter at sharp edges.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {g: "the number of grid samples of the field"}
  time: {step: "Θ(g)", limiter: "Θ(g)"}
  space: {extra: "Θ(g)"}
properties: {deterministic: true, exact: false, unconditionally_stable: true, conservative: false}
history:
  year: 2003
  people: [Todd F. Dupont, Yingjie Liu]
  note: Dupont and Liu proposed BFECC to repair level set functions, and Kim, Liu, Llamas and Rossignac used it with semi-Lagrangian steps for fluids in animation.
prereqs: [stable-fluids, method-of-characteristics, bilinear-interpolation, mac-grid]
see_also: [unconditionally-stable-maccormack, maccormack-method, level-set-method, particle-level-set, vorticity-confinement, fluid-implicit-particle, courant-friedrichs-lewy-condition, weno-scheme]
sources:
  - paper: doi:10.1016/s0021-9991(03)00276-6
    title: "Todd F. Dupont and Yingjie Liu, Back and forth error compensation and correction methods for removing errors induced by uneven gradients of the level set function, Journal of Computational Physics 190(1), 311-324, 2003"
    locator: the BFECC step for the level set function
  - paper: doi:10.1109/tvcg.2007.3
    title: "Byungmoon Kim, Yingjie Liu, Ignacio Llamas and Jarek Rossignac, Advections with significantly reduced dissipation and diffusion, IEEE Transactions on Visualization and Computer Graphics 13(1), 135-144, 2007"
    locator: BFECC with semi-Lagrangian steps for the advection in fluid simulation
  - paper: doi:10.1007/s10915-007-9166-4
    title: "Andrew Selle, Ronald Fedkiw, ByungMoon Kim, Yingjie Liu and Jarek Rossignac, An unconditionally stable MacCormack method, Journal of Scientific Computing 35(2-3), 350-371, 2008"
    locator: "the description of BFECC with three advections, the limiter, and the convergence tables"
  - paper: doi:10.1090/s0025-5718-06-01898-9
    title: "Todd F. Dupont and Yingjie Liu, Back and forth error compensation and correction methods for semi-Lagrangian schemes with application to level set interface computations, Mathematics of Computation 76(258), 647-668, 2007"
    locator: the analysis of BFECC for semi-Lagrangian schemes
---

Back and forth error compensation and correction (BFECC) makes a first order advection step second order. It moves the field forward one step, moves the result back, and compares it with the start. If the step had no error, the round trip would return the start. Half of the difference is an estimate of the error of one step, so BFECC adds it to the start and moves the corrected field forward. With [semi-Lagrangian](/method-of-characteristics/) steps, as in [stable fluids](/stable-fluids/), the result is second order for smooth fields, damps much less, and still has no step limit under a constant velocity. It can overshoot at sharp edges, so it is used with a limiter.

## In plain words

Moving a picture of smoke one step with the plain method blurs it a little. BFECC measures that blur.

It moves the picture one step forward and then one step back with the same method. A perfect method would give back the start. The real method gives a picture that has been blurred twice, once each way. So the difference between the start and the round trip is about two blurs, and half of it is one blur.

BFECC adds that half to the start, which sharpens it in advance, and then moves the sharpened picture forward. The blur of this last move cancels most of the sharpening.

Near a hard edge the sharpening can push values past the old range. A limiter catches those values.

## The problem

Given a field $q$ on a grid (smoke density, temperature, a level set or a velocity component), a velocity field $\mathbf u$ and a time step $\Delta t$, find the field at the next step for the advection equation $\partial q / \partial t + \mathbf u \cdot \nabla q = 0$. Plain semi-Lagrangian advection is stable for any $\Delta t$ but first order, and its numerical diffusion smears small features. The goal is a step that keeps them, at a cost that is a small multiple of the plain step.

## The algorithm

Let $A$ be the plain semi-Lagrangian step: trace back from each sample point and interpolate the old field there. Let $A^R$ be the same step with $-\Delta t$, which traces forward.

```pseudo id=main
BFECC(q, u, dt)
L1  q_hat <- A(q)                                  ▷ forward, the plain step
L2  q_check <- A^R(q_hat)                          ▷ back to the start time
L3  q_bar <- q + (q - q_check) / 2                 ▷ subtract half the round trip error
L4  q_new <- A(q_bar)                              ▷ forward again
L5  limiter: where q_new leaves the range of the old values at the foot, clamp it (or use q_hat)
```

**Why half.** If one step has the error $e$, so that $A q \approx q_{\text{exact}} + e$, then the round trip has about $2e$: $A^R A q \approx q + 2e$. Line L3 gives $\bar q = q - e$. Line L4 adds the error $e$ of one more step, so $A \bar q \approx q_{\text{exact}}$. The proof page makes this exact for a constant velocity: the second order term of the error cancels.

**The velocity.** All three steps use the same velocity field, the one at the start of the step. To advect the velocity itself on a [MAC grid](/mac-grid/), apply BFECC to $u$ and to $v$ with their own sample points.

**The limiter (L5).** The corrected value at a point should lie between the values that the plain step mixes at the same point. The "clamp" limiter clamps it into that range. The "revert" limiter uses the plain value $\hat q$ there instead. Selle and colleagues describe both for the [MacCormack variant](/unconditionally-stable-maccormack/), and they apply to BFECC in the same way.

## Example

**One step by hand.** A row of 7 cells with $\Delta x = 1$ m, a constant velocity $u = 0.5$ m/s and $\Delta t = 1$ s, so the CFL number is $0.5$. The plain step gives $(A q)_a = \frac12 q_a + \frac12 q_{a-1}$, and the reverse step gives $\frac12 q_a + \frac12 q_{a+1}$. Start with a spike at cell 3:

| cell | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $q$ | 0 | 0 | 1 | 0 | 0 | 0 |
| $\hat q = A q$ (L1) | 0 | 0 | 0.5 | 0.5 | 0 | 0 |
| $\check q = A^R \hat q$ (L2) | 0 | 0.25 | 0.5 | 0.25 | 0 | 0 |
| $\bar q$ (L3) | 0 | -0.125 | 1.25 | -0.125 | 0 | 0 |
| $q^{\text{new}} = A \bar q$ (L4) | 0 | -0.0625 | 0.5625 | 0.5625 | -0.0625 | 0 |
| with the limiter (L5) | 0 | 0 | 0.5625 | 0.5625 | 0 | 0 |

The exact solution moves the spike to the position $3.5$. The plain step splits it into two halves. BFECC keeps more height at the peak, $0.5625$, but it dips below 0 next to it. At cell 2 the plain step mixes cells 1 and 2, both 0, so the limiter sets the value to 0. The sum is 1 before the limiter and 1.125 after it, so the limited step does not keep the total.

**Order, measured.** A smooth bump of radius 0.3 m moves for 0.25 s with the velocity $(1, 0.5)$ m/s on a square of 1 m, at the CFL number $4/3$ in $x$. The largest errors are:

| method | 16 by 16 | 32 by 32 | observed order |
|---|---|---|---|
| plain semi-Lagrangian | 0.197 | 0.106 | 0.89 |
| BFECC | 0.0364 | 0.00684 | 2.41 |
| BFECC with clamp | 0.0680 | 0.0153 | 2.15 |
| BFECC with revert | 0.120 | 0.0364 | 1.72 |

At 32 cells BFECC is 15 times more accurate than the plain step. The limiters act near the top of the bump, where the corrected value overshoots the stencil, and lose some of the gain.

**Rotation, measured.** A bump of radius 0.2 m turns a quarter turn about the center of a 32 by 32 grid in 16 steps, at a CFL number of about $1.5$ at the edge of the grid. The largest error is $0.375$ for the plain step, whose peak falls from 1 to $0.60$, against $0.059$ for BFECC and $0.076$ for BFECC with clamp.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Constants.** A constant field stays exactly the same, with or without the limiter.
2. **Stability.** On a periodic grid with a constant velocity, BFECC multiplies each Fourier mode by $G = A (3 - |A|^2)/2$, where $A$ is the factor of the plain step. For every CFL number, $|A| \le |G| \le 1$. So BFECC damps less than the plain step and never amplifies a mode.
3. **Order.** Under the same conditions, the second order term of the error cancels, and the error after a fixed time is $O(\Delta x^2)$ at a fixed CFL number. The plain step is $O(\Delta x)$. The same holds in 2D.
4. **Limiter.** With "clamp" or "revert", each new value lies in the range of the old values at the foot of its backtrace, so the new field stays between the old minimum and maximum.

Without the limiter there is no maximum principle: a square of height 1 reaches $1.24$ and $-0.12$ after five steps. Where the limiter acts, the step is no longer linear and the order drops.

The tests check that the code matches the symbol $G$ to $10^{-13}$ in the interior of a 1D grid, the measured orders, the rotation, the range of the limited values, and that a constant velocity field advects itself exactly.

## Complexity

Let $g$ be the number of samples of the field. Each plain step costs $\Theta(g)$: one backtrace and one bilinear sample per point. BFECC does three plain steps and one sweep for line L3, so it costs about three times the plain step. The limiter needs the range of the stencil at the foot of each forward backtrace; the code here recomputes the backtraces, which adds one more pass, and an implementation can store the feet of line L1 instead. The extra space is $\Theta(g)$ for the fields $\hat q$, $\check q$ and $\bar q$.

## Properties

- **Second order for smooth fields** under a constant velocity, in space and time at a fixed CFL number.
- **No step limit** in the linear analysis, and a maximum principle with the limiter, for any velocity.
- **Less dissipation.** In the bump test above, the error at 32 cells drops from $0.106$ to $0.0068$.
- **Not conservative.** Neither the plain step nor BFECC keeps the sum of the field, and the limiter can change it more.
- **Not monotone without the limiter.** New extrema appear next to sharp edges.
- **Generic.** BFECC wraps any advection step $A$ for which a reverse step exists. It does not need to know how $A$ works.

## Variants and improvements

- **MacCormack.** The [unconditionally stable MacCormack method](/unconditionally-stable-maccormack/) of Selle and colleagues reuses the error estimate of line L3 to correct $\hat q$ directly. It needs two plain steps instead of three and has the same order. It is not the 1969 [MacCormack method](/maccormack-method/) for compressible flow.
- **Level sets.** Dupont and Liu first used BFECC to advect a [level set](/level-set-method/) function, where it reduces the errors caused by uneven gradients. Their later paper analyzes BFECC for semi-Lagrangian schemes.
- **Fluids.** Kim and colleagues used BFECC with semi-Lagrangian steps for the advection in fluid simulation. Applied to the velocity, it keeps more swirl, so a weaker [vorticity confinement](/vorticity-confinement/) force may be enough.
- **Other limiters.** A limiter may clamp to the stencil range, revert to the plain step, or blend the two by a smooth weight.
- **Higher order interpolation.** A cubic or [WENO](/weno-scheme/) sample in place of the bilinear one also reduces the error. It can be combined with BFECC.

## When to use it

Use BFECC when plain semi-Lagrangian advection smears smoke, fire or a level set too much, and a finer grid is too expensive. It drops into an existing solver: it calls the plain step three times and needs no new data structure. Use it with a limiter for fields with sharp edges, such as smoke density or a liquid level set.

If the cost of three plain steps matters, use the MacCormack variant. For liquids with thin sheets and splashes, particles such as [FLIP](/fluid-implicit-particle/) or the [particle level set](/particle-level-set/) keep more detail than any grid advection.

## Pitfalls

- **No limiter.** The corrected field overshoots near edges. Smoke density can go negative, and a velocity can gain energy.
- **The wrong reverse step.** $A^R$ must trace forward with the same velocity field, that is, use $-\Delta t$. Using a different field breaks the cancellation.
- **Boundaries.** The analysis holds where all three backtraces stay inside the domain. Near walls and inflow borders the clamped samples are not symmetric, and the step loses its order there.
- **The range of the limiter.** Take the range from the values of $q$ that the first forward step mixes at the same point, not from $\bar q$ or from a fixed global range.
- **Order is not everything.** A second order step can still be wrong at a large CFL number. The error constant grows with the fractional part of the CFL number. Stable is not accurate.

## Implementations

## History

Todd Dupont and Yingjie Liu introduced BFECC in 2003 to repair level set functions whose gradients become uneven during advection. They analyzed it for semi-Lagrangian schemes in a later paper. Byungmoon Kim, Yingjie Liu, Ignacio Llamas and Jarek Rossignac used BFECC with semi-Lagrangian steps for the advection in fluid simulation, in a paper published in 2007. In 2008, Andrew Selle, Ronald Fedkiw, ByungMoon Kim, Yingjie Liu and Jarek Rossignac derived the cheaper MacCormack variant and described its limiters.

## References
