---
tag: 7F3P2X
kind: problem
slug: seismic-migration
name: Seismic migration
aliases:
- migration imaging
- seismic imaging
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "Move recorded reflections to the true subsurface position of their reflectors, which collapses diffractions and corrects dipping events."
model: real-ram
prereqs: [inverse-problem, wave-equation, seismic-reflection-model]
see_also: [exploding-reflector-model, imaging-condition, kirchhoff-migration, phase-shift-migration, reverse-time-migration, least-squares-migration, full-waveform-inversion, common-midpoint-stacking]
sources:
  - paper: doi:10.1190/1.1440185
    title: Jon F. Claerbout, Toward a unified theory of reflector mapping, Geophysics 36(3), 1971, 467 to 481
    locator: the imaging principle and migration by downward continuation of the wave equation
  - paper: doi:10.1190/1.1440828
    title: William A. Schneider, Integral formulation for migration in two and three dimensions, Geophysics 43(1), 1978, 49 to 76
    locator: migration as a Kirchhoff integral over the recorded data
  - paper: doi:10.1190/1.1440899
    title: Jeno Gazdag, Wave equation migration with the phase-shift method, Geophysics 43(7), 1978, 1342 to 1351
    locator: migration by phase shift in the frequency-wavenumber domain
  - paper: doi:10.1190/1.1441434
    title: Edip Baysal, Dan D. Kosloff and John W. C. Sherwood, Reverse time migration, Geophysics 48(11), 1983, 1514 to 1524
    locator: migration by backward time propagation of the full wave equation
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001
    locator: Chapter 4 (migration), the principles of migration, the dip and diffraction relations, and the families of methods
---

Seismic migration is the problem of turning recorded seismic reflections into a picture of the reflectors in the subsurface. A reflection is recorded at the receiver position and at a traveltime, not at the place of the reflector. Dipping reflectors appear too shallow, too gentle and moved downdip, and every sharp point or edge appears as a diffraction curve. Given the data and a velocity model, migration moves each reflection back to its true position: it collapses diffractions to points and puts dipping events at their true dip. In wave terms, migration is the adjoint of linearized (Born) modeling, not its inverse (a theorem), and most migration algorithms differ only in how they approximate the [wave equation](/wave-equation/). Migration assumes a known velocity; finding the velocity is a separate problem, solved for example by [full-waveform inversion](/full-waveform-inversion/).

## In plain words

A seismic survey sends sound into the ground and records the echoes at the surface. An echo tells how long the sound took, but not from which direction it came. So a raw record puts every echo straight below the receiver, which is wrong for tilted layers, and a small rock edge looks like a long curved arch. Migration fixes this. Using the speed of sound in the rocks, it works out where each echo could have come from and moves it there. The arches shrink back to points, and tilted layers move to their true place and slope. The result is a picture of the layers in the ground.

## Definition

**Input.** Recorded data $d(t, x_s, x_r)$ for sources $x_s$ and receivers $x_r$ at the surface, or a zero-offset section $d(t, x)$ with the source and the receiver at the same point. A velocity model $v(x, z)$, usually smooth.

**Output.** An image $m(x, z)$ whose large values lie on the reflectors.

**Linear model.** Write the data as $d = L\,\delta m$, where $L$ is Born modeling in the background velocity: each point of the reflectivity $\delta m$ scatters the source wave, and the scattered waves are recorded. Migration computes $m = L^{\mathsf T}d$, the adjoint of $L$, through the [imaging condition](/imaging-condition/): a reflector is where the down-going source wave and the up-going recorded wave coincide in time.

**Zero offset.** For a zero-offset section, the [exploding reflector model](/exploding-reflector-model/) replaces the two-way problem by a one-way problem in the half velocity $v/2$: migration is downward continuation of the data to every depth, followed by the field at time zero.

## Variants

- **Time and depth migration.** Time migration assumes a velocity that changes slowly and outputs the image in vertical time; depth migration uses the full velocity model and outputs depth.
- **Poststack and prestack.** Poststack migration images a stacked zero-offset section; prestack migration images each shot or offset before stacking, which needs more computing but handles strong lateral velocity changes.
- **2D and 3D.** Out-of-plane reflections need 3D migration.
- **Adjoint and inverse.** Migration computes $L^{\mathsf T}d$; [least-squares migration](/least-squares-migration/) solves $\min\|L\,\delta m - d\|$ and corrects amplitudes.
- **Image gathers.** Keep the image as a function of offset, angle or lag, for velocity analysis and amplitude studies.

## Examples

**A dipping reflector (theorem for constant velocity).** A plane reflector with the dip $\alpha$ appears on a zero-offset section, with time scaled to depth by $z = vt/2$, as a line with the slope $\sin\alpha$, because the normal-incidence distance from the surface point $x$ to the reflector is $x\sin\alpha$. So $\tan\alpha_{\text{section}} = \sin\alpha_{\text{true}}$. A reflector at 30 degrees appears at $\arctan 0.5 = 26.6$ degrees, and even a vertical reflector appears at only 45 degrees. Migration steepens the event and moves it updip.

**A diffraction (theorem for constant velocity).** A point scatterer at $(x_0, z_0)$ appears on a zero-offset section along the hyperbola $t = (2/v)\sqrt{z_0^2 + (x - x_0)^2}$. With $v = 2000$ m/s and $z_0 = 300$ m, the apex is at 0.3 s, and the trace 400 m away records the scatterer at 0.5 s. Migration collapses the hyperbola to the point.

**A flat layer.** A horizontal reflector at depth $z_0$ in constant velocity appears at $t = 2z_0/v$ on every trace. Migration only converts time to depth.

## Known algorithms

| Method | Velocity | Approach | Cost (2D zero offset) | Status |
|---|---|---|---|---|
| [Kirchhoff migration](/kirchhoff-migration/) | any, with traveltimes | weighted sums along diffraction curves | $O(n_z n_x a)$, aperture $a$ | high-frequency approximation |
| [Phase-shift migration](/phase-shift-migration/) | $v(z)$ | downward continuation by phase shift per frequency | $O(n_z n_t n_x)$ | exact for $v(z)$ |
| [Stolt migration](/stolt-migration/) | constant | change of variables $\omega \to k_z$ in the FK domain | $O(n_t n_x\log(n_t n_x))$ | exact up to interpolation |
| [Split-step Fourier migration](/split-step-fourier-migration/) | $v(x, z)$, moderate contrast | phase shift plus a space-domain correction | $O(n_z n_t n_x\log n_x)$ | exact for $v(z)$; angle error otherwise |
| [Finite-difference migration](/finite-difference-migration/) | $v(x, z)$ | implicit one-way paraxial equation | $O(n_z n_t n_x)$ | about 15 degrees |
| [Reverse-time migration](/reverse-time-migration/) | $v(x, z)$ | full two-way wave equation and imaging condition | $O(s g)$ per shot | exact adjoint of discrete Born |
| [Least-squares migration](/least-squares-migration/) | as its adjoint | conjugate gradients on Born modeling | $k$ times two migrations | converges to the least-squares image |

The velocity model itself comes from tomography or from [full-waveform inversion](/full-waveform-inversion/), whose gradient is computed with the [adjoint-state method](/adjoint-state-method/) and which fails by [cycle skipping](/cycle-skipping/) when the start is poor.

## Bounds

- **Bandwidth (theorem for constant velocity and zero offset).** In the exploding reflector model the data at the frequency $\omega$ map to image wavenumbers with $k_x^2 + k_z^2 = (2\omega/v)^2$. So the image contains only wavenumbers up to $2\omega_{\max}/v$, and finer detail cannot be recovered.
- **Aperture (heuristic).** A reflector with the dip $\alpha$ is imaged only if the recording line extends far enough for its normal rays to reach the surface; steep dips need wide apertures.
- **Input cost.** Every algorithm must read the data, $\Omega(n_t n_x)$ for a zero-offset section. The FK method of Stolt is within a log factor of this.
- **Velocity error.** Migration with a wrong velocity overmigrates (too high) or undermigrates (too low) diffractions into smiles or frowns; no algorithm removes the error of a wrong model.

## Reductions

- **To a one-way problem.** For zero-offset data, the [exploding reflector model](/exploding-reflector-model/) reduces migration to downward continuation in the half velocity.
- **To an adjoint.** Migration equals $L^{\mathsf T}d$ for Born modeling $L$; in the time domain, $L^{\mathsf T}$ is computed by back-propagation and the [imaging condition](/imaging-condition/).
- **To linear least squares.** Inverting $L$ is a linear least-squares problem, solved by [CGLS](/cgls/) in [least-squares migration](/least-squares-migration/).
- **From nonlinear inversion.** The gradient of the waveform misfit in [full-waveform inversion](/full-waveform-inversion/) is a migration of the residuals, so migration is the first step of nonlinear inversion.

## Applications

- **Exploration seismology.** Imaging of oil, gas and mineral reservoirs, and of structures for carbon storage.
- **Crustal and global seismology.** Imaging of faults, subduction zones and discontinuities in the mantle.
- **Ground-penetrating radar.** The same algorithms migrate radar sections with the radar wave speed.
- **Ultrasonic testing and medical ultrasound.** The [synthetic aperture focusing technique](/saft/) and [delay-and-sum beamforming](/delay-and-sum-beamforming/) are Kirchhoff migrations with other weights.
- **Synthetic aperture radar.** The [omega-k algorithm](/omega-k-algorithm/) is Stolt migration for radar.

## References
