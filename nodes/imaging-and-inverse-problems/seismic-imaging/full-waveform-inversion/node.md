---
tag: H0DMN3
kind: algorithm
slug: full-waveform-inversion
name: Full waveform inversion
aliases:
- FWI
- waveform tomography
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Estimate the subsurface velocity by minimizing the misfit between recorded and simulated full wavefields, with gradients from the adjoint-state method."
model: real-ram
complexity:
  vars: {g: "the number of grid points", s: "the number of time steps", e: "the number of shots", k: "the number of iterations"}
  time: {gradient_per_shot: "O(s g)", total: "O(k e s g)"}
  space: {stored_forward_field: "O(s g)"}
properties: {deterministic: true, nonlinear: true, local_optimization: true, exact_discrete_gradient: true, fails_by: "cycle skipping"}
history:
  year: 1984
  people: [Albert Tarantola, Patrick Lailly]
  note: Lailly (1983) and Tarantola (1984) posed seismic inversion as the least-squares fit of full waveforms and computed the gradient by correlating a forward field with a back-propagated residual field.
prereqs: [adjoint-state-method, reverse-time-migration, nonlinear-least-squares]
see_also: [adjoint-state-method, cycle-skipping, four-dimensional-variational-assimilation, reverse-time-migration, least-squares-migration, traveltime-tomography, limited-memory-bfgs, gauss-newton-algorithm]
sources:
  - paper: doi:10.1190/1.1441754
    title: Albert Tarantola, Inversion of seismic reflection data in the acoustic approximation, Geophysics 49(8), 1984, 1259 to 1266
    locator: the least-squares waveform misfit and its gradient by back-propagation of the residuals
  - paper: "Patrick Lailly, The seismic inverse problem as a sequence of before stack migrations, in Conference on Inverse Scattering: Theory and Application, SIAM, 1983"
    locator: the gradient of the waveform misfit as a prestack migration of the residuals
  - paper: doi:10.1190/1.1444597
    title: R. Gerhard Pratt, Seismic waveform inversion in the frequency domain, Part 1, Theory and verification in a physical scale model, Geophysics 64(3), 1999, 888 to 901
    locator: waveform inversion one frequency at a time with the frequency-domain wave equation
  - paper: doi:10.1190/1.1443880
    title: Carey Bunks, Fatimetou M. Saleck, S. Zaleski and Guy Chavent, Multiscale seismic waveform inversion, Geophysics 60(5), 1995, 1457 to 1473
    locator: inversion from low to high frequencies to avoid local minima
  - paper: doi:10.1190/1.3238367
    title: Jean Virieux and Stephane Operto, An overview of full-waveform inversion in exploration geophysics, Geophysics 74(6), 2009, WCC1 to WCC26
    locator: the review of the method, its gradient, its local minima and its practice
---

Full waveform inversion (FWI) estimates the velocity of the subsurface by fitting whole recorded seismograms. It simulates the data $F(m)$ for a model $m$ with the wave equation, measures the misfit $J(m) = \frac12\|F(m) - d\|^2$, and lowers it with a gradient method. The gradient comes from the [adjoint-state method](/adjoint-state-method/) at the cost of one forward and one backward simulation per shot, and it is a [reverse-time migration](/reverse-time-migration/) of the data residuals. FWI looks like [4D-Var](/four-dimensional-variational-assimilation/) of weather forecasting, which also fits a time-dependent model to observations with an adjoint. The difference is in the unknowns: 4D-Var fits the initial state of the forecast over a time window and adds a background term, while FWI fits the coefficients of the wave equation (the velocity), with a known source and zero initial state. $J$ is not convex, so FWI is a local method: it needs a starting model whose predicted events are within half a period of the recorded ones, or it fails by [cycle skipping](/cycle-skipping/) (a heuristic rule that is a theorem for one shifted sinusoid).

## In plain words

FWI guesses a model of the wave speeds in the ground, simulates the seismograms that this model would give, and compares them with the real ones, sample by sample. Then it changes the model a little in the direction that makes the difference smaller, and repeats. The direction comes from playing the differences backward in time from the receivers and comparing them with the forward simulation, which costs about two simulations. Because it uses every wiggle of the seismograms, FWI can find much finer detail than methods that use only arrival times. The catch is that the first guess must be close: if a simulated wiggle is off by more than half a wiggle, the method matches it to the wrong one.

## The problem

Given the recorded data $d$ of one or more shots, a known source $f$, and a starting model $m_0$, find
$$m^* = \arg\min_{m > 0} J(m), \qquad J(m) = \frac12\sum_{\text{shots}}\sum_n\sum_r \big(u^n_r(m) - d^n_r\big)^2,$$
where $u(m)$ solves the wave equation $m\,u_{tt} - \Delta u = f$ with $m = 1/v^2$. This is a nonlinear [inverse problem](/inverse-problem/) and a [nonlinear least-squares](/nonlinear-least-squares/) problem with a very large number of unknowns.

## The algorithm

The scheme is $u^{n+1} = 2u^n - u^{n-1} + (\Delta t^2/m)(Lu^n + f^n)$ with the second difference $L$, $u^0 = u^{-1} = 0$ and the [CFL condition](/courant-friedrichs-lewy-condition/). The gradient of the discrete $J$ comes from the adjoint state of this scheme.

```pseudo id=main
FWI-GRADIENT(m, f, receivers, d, Δt, h)     ▷ one shot; L: the second difference
L1  u^0, ..., u^N ← the forward run of the scheme with the source f; store all fields
L2  res^n_r ← u^n_r - d^n_r for every step n and receiver r;  J ← (1/2) Σ (res^n_r)²
L3  λ1 ← 0;  λ2 ← 0;  g ← 0      ▷ the adjoint field at the steps k + 1 and k + 2
L4  for k ← N down to 1 do  λ ← 2 λ1 - λ2 + (Δt² / m) L λ1
L5      λ[r] ← λ[r] + res^k_r / m[r] for every receiver r      ▷ inject the residuals
L6      g ← g - λ · (u^k - 2 u^(k-1) + u^(k-2));  λ2 ← λ1;  λ1 ← λ
L7  return J, g
```

The outer loop is gradient descent: compute $(J, g)$, take the trial step $m - a g$ with $a$ chosen so that the largest change is 5 percent of $\max m$, and halve $a$ until the model stays positive and the Armijo condition $J(m - ag) \le J(m) - 10^{-4} a\|g\|^2$ holds ([backtracking line search](/backtracking-line-search/)). Line L1 is one forward simulation with all fields stored. Line L2 forms the residuals. Lines L4 and L5 run the transposed scheme backward in time with the residuals as the source; this is the same backward run as [reverse-time migration](/reverse-time-migration/). Line L6 correlates the adjoint field with the second time difference of the forward field, which is the derivative of the scheme with respect to $m$.

## Example

**The half-period rule by hand.** In the 1D test, the source and the receiver are 550 m apart and the true velocity is 2000 m/s, so the direct wave arrives after 0.275 s. A 15 Hz wavelet has the period 0.0667 s. For a constant starting velocity $v$, the predicted arrival is $550/v$, and the half-period rule asks for $|550/v - 0.275| < 0.0333$ s, which gives $v > 1784$ m/s. The measured misfit has its barrier at about 1800 m/s and a false minimum at 1625 m/s, where the predicted pulse is about one period late; see [cycle skipping](/cycle-skipping/).

**A 1D inversion.** The test model has 60 cells of 10 m, 2000 m/s over 2400 m/s below cell 25, and a Gaussian bump of 300 m/s at cell 40. The source is at cell 2, the receivers are at cells 2 and 57, and the wavelet is a 15 Hz Ricker wavelet over 300 steps of 2 ms. From a constant 2200 m/s, 10 iterations of the descent loop lower the misfit from 2392.8 to 75.05, 3.1 percent of the start, and every iteration lowers it (measurements on this case). The adjoint gradient agrees with centered finite differences to a relative error of about $6 \times 10^{-8}$.

## Correctness

The full proof is in proofs/correctness.md.

- **Exact discrete gradient (theorem).** Line L7 returns $J$ and $\partial J/\partial m_i = -\sum_{k=1}^{N}\lambda^k_i\,(u^k - 2u^{k-1} + u^{k-2})_i$, where $\lambda^k$ solves the transposed scheme $\lambda^k = 2\lambda^{k+1} - \lambda^{k+2} + \Delta t^2 M^{-1}L\lambda^{k+1} + M^{-1}R^{\mathsf T}\mathrm{res}^k$ with $\lambda^{N+1} = \lambda^{N+2} = 0$. This is the exact gradient of the discrete misfit, with no gap between the continuous and the discrete adjoint. A loop invariant matches line L4 to this recursion.
- **The descent loop (theorem).** The loop keeps every model positive and the misfit history non-increasing, and it uses at most $30$ extra forward runs per iteration plus one at the end. For a small enough step the Armijo condition holds whenever $g \ne 0$.
- **Zero residual (theorem).** At the true model the residual is zero, so the adjoint source and the gradient are zero.

That the descent reaches the true model is not a theorem. It needs a starting model within the basin of attraction, which the half-period rule estimates (a heuristic).

## Complexity

- **Real-ram.** One gradient costs one forward and one backward simulation, $O(s g)$ each, per shot. With $e$ shots and $k$ iterations and a bounded number of line-search runs, the total is $O(k e s g)$.
- **Against finite differences.** A gradient by finite differences needs one simulation per model parameter, $O(g)$ simulations per shot, which is out of reach for $10^6$ to $10^9$ unknowns. The adjoint state needs two.
- **Memory.** Line L1 stores the forward field, $O(s g)$; checkpointing or boundary storage reduces this, as in reverse-time migration.

## Properties

- **High resolution.** The gradient uses the whole waveform, so FWI can resolve features of about half a wavelength, much finer than [traveltime tomography](/traveltime-tomography/) (a common estimate, not a theorem).
- **Local.** The misfit has many local minima. Gradient methods converge to the minimum of the basin that holds the starting model.
- **Low frequencies first.** The basin is wider at low frequencies, because the period is longer.
- **Exact gradient of the discrete problem.** Differentiating the discrete scheme, as here, gives a gradient that passes the finite-difference check to rounding; differentiating the continuous equation first and then discretizing does not.
- **Shots are independent.** The gradient is a sum over shots, so shots run in parallel.

## Variants and improvements

- **Quasi-Newton and Gauss-Newton steps.** [L-BFGS](/limited-memory-bfgs/) uses past gradients to approximate the Hessian, and the [Gauss-Newton algorithm](/gauss-newton-algorithm/) solves a linearized problem at each step, often with CG.
- **Frequency domain.** Pratt (1999) solved the Helmholtz equation for a few frequencies and inverted them from low to high.
- **Multiscale inversion.** Bunks et al. (1995) inverted low-pass filtered data first and added higher frequencies as the model improved, which widens the basin (a heuristic).
- **Other misfits.** Misfits based on cross-correlation traveltimes, envelopes, or optimal transport (Engquist and Froese 2014) are more convex with respect to time shifts (a heuristic).
- **Extended models.** Allow a model that depends on the shot or on a time lag, and penalize the extension, so that the data can be fitted far from the true model.
- **Elastic and anisotropic FWI.** Invert for several parameters with the elastic or anisotropic wave equation.

## When to use it

Use FWI when a good starting model is available, for example from [traveltime tomography](/traveltime-tomography/), and the data have low frequencies and long offsets, so that diving waves and refractions sample the deep model. It gives the highest-resolution velocity models in exploration and in global seismology. Without low frequencies or a good start, use tomography first, or a cycle-skipping-resistant misfit.

## Pitfalls

- **A poor starting model.** Starting with arrivals more than half a period off makes the inversion converge to a false model with a small misfit. Check the predicted and recorded first arrivals before line L1.
- **Inconsistent adjoints.** Using the continuous adjoint equation with a different discretization in line L4 gives a gradient that is only approximate, and the line search fails near convergence. Check the gradient against finite differences, as in the test.
- **No positivity.** A gradient step can make $m = 1/v^2$ negative, and the next simulation fails. Reject such trial steps in the line search.
- **A CFL violation during the line search.** A trial model with a higher velocity can break the CFL condition for the fixed $\Delta t$. Check $v_{\max}\Delta t/h$ for every trial model.

## Implementations

## History

Lailly (1983) and Tarantola (1984) posed the inversion of seismic waveforms as least-squares fitting and showed that the gradient is a migration of the residuals, using the adjoint-state method that Chavent had introduced for distributed parameter systems. Early tests on reflection data were limited by local minima and computing power. Pratt and coworkers in the 1990s developed frequency-domain inversion, and Bunks et al. (1995) proposed the multiscale strategy. With long-offset data, low frequencies and parallel computers, FWI became a standard tool for velocity model building in the 2000s and 2010s; Virieux and Operto (2009) reviewed it.

## References
