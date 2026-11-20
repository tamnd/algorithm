---
tag: Y8PCJ8
kind: algorithm
slug: reverse-time-migration
name: Reverse time migration
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Propagate the source wavefield forward and the recorded data backward in time with the full wave equation and apply the imaging condition."
solves: [seismic-migration]
model: real-ram
complexity:
  vars: {g: "the number of grid points", s: "the number of time steps"}
  time: {per_shot: "O(s g)"}
  space: {stored_source_field: "O(s g)"}
properties: {deterministic: true, linear_in_data: true, two_way: true, no_dip_limit: true, adjoint_of_born_modeling: true, needs_cfl: true}
history:
  year: 1983
  people: [Edip Baysal, Dan D. Kosloff, John W. C. Sherwood, George A. McMechan, N. Dan Whitmore]
  note: Baysal, Kosloff and Sherwood, McMechan, and Whitmore each published migration by backward time propagation of the full wave equation in 1983.
prereqs: [imaging-condition, finite-difference-method, courant-friedrichs-lewy-condition, seismic-migration]
see_also: [imaging-condition, finite-difference-method, courant-friedrichs-lewy-condition, perfectly-matched-layer, least-squares-migration, full-waveform-inversion, adjoint-state-method, kirchhoff-migration]
sources:
  - paper: doi:10.1190/1.1441434
    title: Edip Baysal, Dan D. Kosloff and John W. C. Sherwood, Reverse time migration, Geophysics 48(11), 1983, 1514 to 1524
    locator: the backward time propagation of the full wave equation with the exploding reflector imaging condition
  - paper: doi:10.1111/j.1365-2478.1983.tb01060.x
    title: George A. McMechan, Migration by extrapolation of time-dependent boundary values, Geophysical Prospecting 31(3), 1983, 413 to 420
    locator: the recorded data as a time-dependent boundary value, propagated backward in time
  - paper: doi:10.1190/1.1893867
    title: N. Dan Whitmore, Iterative depth migration by backward time propagation, SEG Technical Program Expanded Abstracts, 1983, 382 to 385
    locator: depth migration by backward time propagation
  - paper: doi:10.1190/1.1440185
    title: Jon F. Claerbout, Toward a unified theory of reflector mapping, Geophysics 36(3), 1971, 467 to 481
    locator: the imaging principle that reflectors exist where the downgoing and upgoing waves coincide in time
---

Reverse time migration (RTM) images the subsurface with the full two-way wave equation. It propagates the source wavefield forward in time, propagates the recorded data backward in time from the receivers, and applies the [imaging condition](/imaging-condition/): at every point it correlates the two fields at zero lag. RTM is not a new way to solve the [wave equation](/wave-equation/); both propagations use an ordinary [finite-difference method](/finite-difference-method/) in time and space, with its [CFL condition](/courant-friedrichs-lewy-condition/). What RTM adds is the backward run and the correlation. In the form below, the backward run is the transpose of the discrete scheme, so the image is the exact adjoint of discrete Born modeling (a theorem), the operator that [least-squares migration](/least-squares-migration/) inverts and the gradient that [full-waveform inversion](/full-waveform-inversion/) uses. Because it solves the two-way equation, RTM has no dip limit and images turning waves and steep salt flanks that one-way methods miss.

## In plain words

A shot sends a wave into the ground, and receivers at the surface record the echoes. RTM first simulates the shot wave going down, using a computer model of the wave speed, and keeps a copy of it at every time step. Then it plays the recording backward: it injects the echoes at the receivers, last sample first, and lets the simulation send them back into the ground. A reflector is at the place where the wave going down and the echo played back meet at the same moment. So at every point RTM multiplies the two fields at each time and adds up the products. The sum is large at reflectors and small elsewhere.

## The problem

Given the recorded data $d^n_r$ of one shot at the receivers $r$ and the time steps $n$, and a smooth background model $m_0 = 1/v_0^2$, compute the image of the model perturbation. The data are modeled by the constant-density acoustic equation $m\,u_{tt} - \Delta u = f$. Linearizing about $m_0$ (the Born approximation) gives the scattered field $\delta u$ that solves $m_0\,\delta u_{tt} - \Delta\delta u = -\delta m\, u_{0,tt}$, where $u_0$ is the source field. RTM computes $B^{\mathsf T} d$, the adjoint of the linear map $B : \delta m \mapsto \delta u$ at the receivers. This is [seismic migration](/seismic-migration/) with the cross-correlation imaging condition.

## The algorithm

The scheme is $u^{n+1} = 2u^n - u^{n-1} + w\,(L u^n + f^n)$ with $w = \Delta t^2/m$, the 5-point Laplacian $L$, $u^0 = u^{-1} = 0$ and $u = 0$ outside the grid. First run it with the source to get the source field $u_0$ and store its second time differences $D_2 u_0^n = (u_0^{n+1} - 2u_0^n + u_0^{n-1})/\Delta t^2$. Then run the transposed scheme backward with the data as the source.

```pseudo id=main
REVERSE-TIME-MIGRATION(d, m, D2u0, receivers, Δt, h)     ▷ D2u0[n]: stored, from the forward run
L1  N ← the number of time steps of the source field;  w ← Δt² / m
L2  λ1 ← 0;  λ2 ← 0;  image ← 0      ▷ the adjoint field at the steps n + 1 and n + 2
L3  for n ← N down to 1 do
L4      λ ← 2 λ1 + L(w · λ1) - λ2      ▷ the transposed scheme, run backward in time
L5      λ[r] ← λ[r] + d[n][r] for every receiver r      ▷ inject the data
L6      image ← image - D2u0[n - 1] · w · λ;  λ2 ← λ1;  λ1 ← λ      ▷ the imaging condition
L7  return image
```

Line L4 is the transpose of one forward step: the forward step applies $w$ after the Laplacian, so the transpose applies $w$ before it. Line L5 injects the recorded sample of every receiver, last time first. Line L6 is the imaging condition: the zero-lag correlation of the backward field with the second time derivative of the source field, summed over time. With $\mu = w\lambda$ the recursion of line L4 becomes $\mu^n = 2\mu^{n+1} - \mu^{n+2} + w L\mu^{n+1}$, which is the forward scheme run backward in time, so it is stable under the same CFL condition.

## Example

**The time step by hand.** With $h = 10$ m, $\Delta t = 2$ ms and $v = 2000$ m/s, the CFL number is $v\Delta t/h = 2000 \cdot 0.002/10 = 0.4$. The 2D bound for this scheme is $1/\sqrt{2} = 0.707$, so the scheme is stable. Doubling $\Delta t$ to 4 ms gives 0.8, which is above the bound, and the fields grow without limit.

**One scatterer.** The test uses a $32 \times 32$ grid with these values, a 20 Hz Ricker source at row 2 and column 16, receivers along row 2, 180 time steps (0.36 s), and a scatterer $\delta m = 0.2/v^2$ at row 18 and column 12. RTM of the Born data puts the largest absolute value below row 5 at exactly row 18, column 12, and the value there is positive, the sign of $\delta m$ (a measurement on this case). The rows next to the source and the receivers hold strong artifacts from the direct wave.

**Adjointness.** For random $\delta m$ and random data $r$, $\langle B\,\delta m, r\rangle$ and $\langle \delta m, B^{\mathsf T} r\rangle$ agree to a relative $10^{-10}$ in the test.

## Correctness

The full proof is in proofs/correctness.md.

- **Born is the derivative (theorem).** The discrete Born modeling is the exact derivative of the discrete forward scheme with respect to $m$, applied to $\delta m$.
- **Exact adjoint (theorem).** Write all time steps of the forward scheme as one block lower-triangular system $A u = s$. Its transpose is block upper triangular, and back substitution from the last step is exactly lines L3 to L6. A loop invariant shows that after the pass for step $n$, $\lambda1$ holds the adjoint field at step $n$. So the returned image is $B^{\mathsf T} d$ for the discrete $B$.
- **The imaging condition (corollary).** The image is $-\sum_n D_2u_0^{n-1}\, w\, \lambda^n$, a zero-lag cross-correlation of the source field (second time derivative) and the backward field, as the imaging condition says.
- **Stability.** The backward recursion is the forward scheme in $\mu = w\lambda$, so it is stable exactly when the forward scheme is, under the CFL condition $v\Delta t/h \le 1/\sqrt{2}$ in 2D.

That the adjoint image puts its peaks at the reflectors is not a theorem; it holds when the background velocity is close to the true one and the acquisition covers the target (a heuristic, supported by the test above).

## Complexity

- **Real-ram.** Each propagation costs $O(1)$ per grid point and time step, so one shot costs $O(s g)$ for the forward run, the same for the backward run, and the same for the correlation: $O(s g)$ in total.
- **Memory.** The imaging condition pairs the source field at step $n - 1$ with the backward field at step $n$, but the source field is computed forward and the backward field backward. Storing the source field costs $O(s g)$ memory, the main cost of RTM in 3D.
- **Checkpointing.** Storing the source field at $O(\sqrt{s})$ checkpoints and recomputing between them cuts the memory to $O(\sqrt{s}\, g)$ for one extra forward run; the logarithmic checkpointing schedules of [automatic differentiation](/automatic-differentiation/) cut it further.
- **Many shots.** Shots are independent, so the cost is $O(s g)$ per shot and the shots run in parallel.

## Properties

- **Two-way propagation.** RTM uses the full wave equation, so it has no dip limit, and it images with turning waves and prism waves.
- **Exact adjoint.** In this discrete form the image is the exact transpose of Born modeling, the property that [least-squares migration](/least-squares-migration/) and the [adjoint-state method](/adjoint-state-method/) need.
- **Not an inverse.** The adjoint does not undo the wavelet, the illumination or the finite aperture; amplitudes are not reflection coefficients.
- **Low-frequency artifacts.** Waves reflected from sharp contrasts in the background correlate with the source field along their whole path and give strong low-wavenumber noise, especially near the source.
- **Edge reflections.** Dirichlet edges, as in the test, reflect waves back into the grid. Production codes surround the grid with a [perfectly matched layer](/perfectly-matched-layer/) that absorbs them.

## Variants and improvements

- **Absorbing boundaries.** A [perfectly matched layer](/perfectly-matched-layer/) on all sides except the free surface removes edge reflections. The adjoint of the absorbing scheme must be used for the backward run to keep exact adjointness.
- **Higher-order stencils.** Spatial stencils of order 8 to 16 allow fewer grid points per wavelength, which reduces the cost in 3D.
- **Laplacian filtering.** Applying a Laplacian to the image, or separating the fields into up-going and down-going parts before the correlation, reduces the low-frequency artifacts.
- **Source field reconstruction.** Store only the boundary values of the source field and run it backward together with the receiver field, which cuts the memory to $O(s\sqrt{g})$ in 2D, when the scheme has no absorption.
- **Extended imaging conditions.** Correlate with a space or time lag to build gathers for velocity analysis; see [imaging condition](/imaging-condition/).
- **Elastic and anisotropic RTM.** Use the elastic or anisotropic wave equation for the two runs.

## When to use it

Use RTM for complex geology with steep dips and strong lateral velocity contrasts, such as below salt, where [Kirchhoff](/kirchhoff-migration/) and one-way methods fail. It is the most expensive standard migration. For smooth media and moderate dips, one-way methods such as [split-step Fourier migration](/split-step-fourier-migration/) cost much less. RTM is also the inner adjoint of [least-squares migration](/least-squares-migration/) and of the gradient of [full-waveform inversion](/full-waveform-inversion/).

## Pitfalls

- **A time step above the CFL bound.** Choosing $\Delta t$ with $v_{\max}\Delta t/h > 1/\sqrt{2}$ makes both runs blow up. Check the bound with the largest velocity before line L1.
- **The wrong transpose.** Applying $w$ after the Laplacian in line L4, as in the forward step, gives a field that is not the adjoint when $m$ varies, and the dot-product test fails. Apply $w$ before the Laplacian, as in line L4.
- **A time shift in the correlation.** Pairing $D_2u_0^n$ instead of $D_2u_0^{n-1}$ with $\lambda^n$ in line L6 shifts the image by one step and breaks exact adjointness.
- **Too few grid points per wavelength.** The second-order stencil has numerical dispersion; with fewer than about 10 points per shortest wavelength the waves arrive late (a common rule of thumb).

## Implementations

## History

Claerbout (1971) stated the imaging principle: reflectors are where the down-going and up-going waves coincide in time. In 1983 three groups independently proposed migration by backward time propagation of the full wave equation: Baysal, Kosloff and Sherwood; McMechan; and Whitmore. Baysal, Kosloff and Sherwood migrated stacked data with the exploding reflector model. In the same years Lailly (1983) and Tarantola (1984) showed that the cross-correlation of a forward field and a backward-propagated residual is the gradient of a least-squares misfit, which tied RTM to the [adjoint-state method](/adjoint-state-method/). Prestack RTM became a standard industry tool for subsalt imaging once computers had enough memory and speed for 3D two-way propagation.

## References
