---
tag: D5V4KY
kind: technique
slug: perfectly-matched-layer
name: Perfectly matched layer
aliases:
- PML
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: An absorbing layer at the domain boundary built by complex coordinate stretching, so outgoing waves enter it without reflection and decay.
model: floating-point-model
prereqs: [wave-equation, finite-difference-method, boundary-conditions]
see_also: [yee-fdtd-scheme, finite-element-method, discontinuous-galerkin-method, crank-nicolson-method, heat-equation, upwind-scheme, summation-by-parts-operators, von-neumann-stability-analysis]
sources:
  - paper: doi:10.1006/jcph.1994.1159
    title: Jean-Pierre Berenger, A perfectly matched layer for the absorption of electromagnetic waves, Journal of Computational Physics 114(2) (1994) 185-200
    locator: the split-field layer for Maxwell's equations, the matching condition on the electric and magnetic conductivities, the proof of zero reflection at all angles and frequencies
  - book: isbn:9781580538329
    title: Allen Taflove and Susan C. Hagness, Computational Electrodynamics, The Finite-Difference Time-Domain Method, 3rd edition, Artech House, 2005
    locator: Chapter 7 (perfectly matched layer absorbing boundary conditions, polynomial grading, the reflection estimate, CPML)
  - paper: arXiv:2108.05348
    title: Steven G. Johnson, Notes on perfectly matched layers (PMLs)
    locator: PML as complex coordinate stretching, the decay of propagating waves, why the discrete layer reflects and the need for gradual turn-on
---

A perfectly matched layer (PML) is an artificial absorbing layer around a computational domain for wave equations in open space. Inside the layer the coordinate normal to the boundary is continued into the complex plane: $\partial_x$ is replaced by $\frac{1}{1 + i\sigma(x)/\omega}\partial_x$, with $\sigma = 0$ in the interior and $\sigma > 0$ in the layer. A wave $e^{i(kx - \omega t)}$ becomes $e^{i(kx - \omega t)}e^{-(k/\omega)\int\sigma\,dx}$ in the layer, so it decays, and because the stretched equations agree with the original ones where $\sigma = 0$, the interface has zero reflection for every angle and every frequency. This holds for the continuous equations only. On a grid the layer reflects a little, and the reflection is kept small by turning $\sigma$ on gradually, often as $\sigma_{\max}(d/D)^m$ with depth $d$, layer depth $D$ and $m$ from 2 to 4. Berenger (1994) introduced the layer for Maxwell's equations and the [Yee scheme](/yee-fdtd-scheme/). Chew and Weedon (1994) gave the interpretation as stretched coordinates, which carries the PML to acoustics, elasticity and other wave equations.

## In plain words

A computer can only hold a finite piece of space. When a wave reaches the edge of that piece, a simple boundary sends it back, and the echo spoils the result. A perfectly matched layer is a thin border around the domain where waves are slowly damped. The damping is made in a special way: the border looks exactly like empty space to a wave that enters it, so the wave goes in without an echo, whatever its direction and frequency. Inside the border the wave dies out before it reaches the outer wall. On a computer the match is not quite perfect, so the damping must start softly and grow with depth.

## When it applies

- Wave problems in an unbounded region, truncated to a finite domain: electromagnetics, acoustics, elastic waves, water waves, and the Schrödinger equation.
- Time-domain schemes such as the [Yee scheme](/yee-fdtd-scheme/) and frequency-domain solvers such as [finite elements](/finite-element-method/) for the Helmholtz equation.
- Outgoing waves at all angles, where first-order absorbing conditions fail at grazing incidence.
- Problems where a few cells of extra domain at each side are cheap compared with the cost of an echo.

It does not apply to waves that do not propagate outward with a positive group velocity in the normal direction. Some anisotropic and elastic media have backward waves, and there the standard PML grows instead of decaying.

## The template

For the one-dimensional wave equation in the first-order form $E_t = H_x$, $H_t = E_x$ (units with $c = 1$), the stretching gives $E_t + \sigma E = H_x$ and $H_t + \sigma H = E_x$, with the same $\sigma$ in both equations. The reference code adds this layer to the one-dimensional Yee scheme with $E$ at $x_i$ and $H$ at $x_{i+1/2}$:

```pseudo id=main
PML-STEP(E, H, σ, Δx, Δt)
L1  σ_max ← -(m + 1) c ln R / (2D)                         ▷ once, from the target reflection R
L2  σ(x) ← σ_max (d(x)/D)^m in the layer, 0 inside         ▷ once, at the E and H points
L3  for each i do H_(i+1/2) ← ((1 - σΔt/2) H_(i+1/2) + (Δt/Δx)(E_(i+1) - E_i)) / (1 + σΔt/2)
L4  for each interior i do E_i ← ((1 - σΔt/2) E_i + (Δt/Δx)(H_(i+1/2) - H_(i-1/2))) / (1 + σΔt/2)
L5  E ← 0 at the two ends                                  ▷ a wall behind the layer
```

**Walk-through.** L1 picks the peak conductivity from the reflection that the continuous layer would have. For $\sigma = \sigma_{\max}(d/D)^m$ a wave at angle $\theta$ to the normal crosses the layer, is reflected by the wall and comes back, so its amplitude is multiplied by

$$R(\theta) = \exp\Big(-\frac{2\cos\theta}{c}\int_0^D\sigma\,dd\Big) = \exp\Big(-\frac{2\cos\theta\,\sigma_{\max}D}{c\,(m + 1)}\Big).$$

L2 grades the conductivity. L3 and L4 are the Yee updates with the damping term averaged between the old and the new time level, which keeps the scheme second order and stable for any $\sigma \ge 0$. In the interior $\sigma = 0$ and they are the plain Yee scheme. L5 closes the domain with a wall, because any wave that reaches it has already lost the factor $\sqrt{R}$.

**Why the continuous layer is perfect.** Let $\tilde x = x + \frac{i}{\omega}\int_0^x\sigma$. At the frequency $\omega$ the layer equations are the free equations in the variable $\tilde x$, because $\partial_{\tilde x} = \frac{1}{1 + i\sigma/\omega}\partial_x$. So the outgoing solution $e^{i(k\tilde x - \omega t)}$ of the free equations solves the layer equations, and it equals the incident wave for $x \le 0$, where $\tilde x = x$. No reflected wave is needed to satisfy the interface conditions. The same argument works in several dimensions for each coordinate that is stretched, so the interface does not reflect at any angle. The factor $|e^{ik\tilde x}| = e^{-(k\cos\theta/\omega)\int\sigma}$ gives the decay, and $k/\omega = 1/c$ makes it independent of the frequency.

## Classic examples

- [Yee scheme](/yee-fdtd-scheme/): the original use. Berenger split each field component into two parts with separate conductivities; the convolutional PML (CPML) of Roden and Gedney (2000) does the same with one auxiliary variable per derivative and is the standard in FDTD codes.
- [Wave equation](/wave-equation/) and acoustics: the stretched form of the pressure and velocity equations, as in the reference code, and second-order forms with auxiliary fields for seismic modelling.
- [Finite element method](/finite-element-method/) for the Helmholtz equation: in the frequency domain the PML is only a change of the coefficients, $\partial_x \to \partial_x/(1 + i\sigma/\omega)$, with no extra unknowns.
- [Discontinuous Galerkin method](/discontinuous-galerkin-method/): DG solvers for Maxwell's equations and acoustics add the PML auxiliary equations as extra source terms in the layer elements.
- The Schrödinger equation with a [Crank-Nicolson](/crank-nicolson-method/) scheme: a complex stretching absorbs outgoing wave packets in quantum scattering and ionization problems.

**One wave by hand.** Take the design $R = 10^{-6}$, a layer of $D = 20$ cells with $\Delta x = 1$, $c = 1$ and $m = 2$. L1 gives $\sigma_{\max} = 3\ln(10^6)/40 = 1.036$. At normal incidence $\int_0^D\sigma = \sigma_{\max}D/3 = 6.91$, so one pass through the layer multiplies the amplitude by $e^{-6.91} = 10^{-3}$, and the way back by another $10^{-3}$. At $\theta = 60°$, $\cos\theta = \tfrac12$ and the same layer gives only $R = 10^{-3}$. At grazing incidence the layer gives no damping at all, which is why the domain should be large enough that the important waves meet the layer at moderate angles.

**Reflection (measurement).** A Gaussian pulse $E = e^{-((x - x_0)/6)^2}$, $H = -E$, moving right in an interior of 200 cells with $\Delta t = \Delta x/2$, enters a layer of $N$ cells designed for $R = 10^{-6}$. The table shows the largest $|E|$ in the interior after the reflected part has come back, measured against the same scheme on a domain so long that no wave reaches its ends. With no layer, a wall gives 0.988.

| layer cells $N$ | $m = 0$ (step) | $m = 1$ | $m = 2$ | $m = 3$ |
|---|---|---|---|---|
| 5 | 3.09e-1 | 3.77e-2 | 5.01e-4 | 2.95e-4 |
| 10 | 1.66e-1 | 8.84e-3 | 5.46e-5 | 2.26e-5 |
| 20 | 8.49e-2 | 2.18e-3 | 6.77e-6 | 1.41e-6 |
| 40 | 4.25e-2 | 5.38e-4 | 9.84e-7 | 1.03e-6 |

The design value $10^{-6}$ is the same in every cell of the table, but the discrete layer reaches it only when it is thick and smooth. A step in $\sigma$ reflects about $\sigma_{\max}\Delta x/4$, and the reflection falls only as $1/N$. A linear profile gives $1/N^2$. With $m = 2$ or $3$ and 20 to 40 cells, the reflection is at the design level. With $N = 20$ and $m = 3$, the designs $R = 10^{-2}$ and $10^{-4}$ give the measured $9.8\cdot 10^{-3}$ and $1.1\cdot 10^{-4}$, and the design $10^{-8}$ gives $1.9\cdot 10^{-6}$, which is the floor of the discretization. A layer with loss only in $E$ (no matching loss in $H$) reflects 0.28 of the pulse, where the matched layer reflects $6.7\cdot 10^{-6}$.

## Variations

- **Split-field PML.** Berenger's form: each field is split into the parts that are differentiated in $x$ and in $y$, each with its own conductivity. It is not a strongly well-posed system, which can matter for some schemes.
- **Uniaxial PML (UPML).** An anisotropic artificial material with tensors $\varepsilon$ and $\mu$ that has the same effect without splitting, and is a physical (though artificial) medium.
- **Complex frequency shifted PML and CPML.** The stretching $1 + \sigma/(\alpha - i\omega)$ with a small $\alpha > 0$ damps evanescent and low-frequency waves better and removes the late-time growth of the standard layer. The convolutional form implements it with a recursive update.
- **Real stretching.** A term $\kappa(x) > 1$ in the stretching $\kappa + i\sigma/\omega$ speeds up the decay of evanescent waves, which a pure imaginary stretching does not damp.
- **Sponge layers and absorbing boundary conditions.** A simple damping term without matching, or a local condition such as the first-order Engquist-Majda condition. They are cheaper but reflect much more, especially at grazing angles.

## Pitfalls

- **A sudden jump in $\sigma$.** The continuous layer does not reflect, but the discrete one does, by an amount that grows with $\sigma\Delta x$. Grade $\sigma$ smoothly and use at least 8 to 10 cells.
- **Too large $\sigma_{\max}$.** A small design $R$ with a thin layer makes $\sigma$ change fast, and the discrete reflection then grows. The measured reflection, not the design value, is what counts.
- **Unmatched loss.** In electromagnetics the magnetic conductivity must satisfy $\sigma^*/\mu = \sigma/\varepsilon$. In other systems every equation that contains the stretched derivative needs the same stretching.
- **Grazing and evanescent waves.** The damping is proportional to $\cos\theta$, and evanescent waves are not damped by an imaginary stretching. Keep sources away from the layer, or add a real stretching $\kappa$ and a frequency shift $\alpha$.
- **Backward waves.** In some anisotropic or elastic media the phase and group velocities point in opposite directions, and the standard PML becomes unstable. These media need modified layers.
- **The layer in the wrong place.** The PML must surround the domain on every side where waves leave. Corners need the stretching in both directions at once.

## Exercises

1. Insert $E = e^{i(k\tilde x - \omega t)}$, $H = -E$ with $\tilde x = x + \frac i\omega\int_0^x\sigma$ into $E_t + \sigma E = H_x$ and $H_t + \sigma H = E_x$, and show that it is a solution for $c = 1$. Show that $|E|$ decays as $e^{-\int_0^x\sigma}$.
2. Show that L3 and L4 are second-order accurate for the layer equations, and that with $\sigma\ge 0$ the discrete energy of the Yee scheme does not increase.
3. For a layer with a constant $\sigma$ that starts with a jump at $x = 0$, compute the reflection coefficient of the discrete scheme for a wave with $k\Delta x \to 0$, and show that it is of order $\sigma\Delta x$.

## References
