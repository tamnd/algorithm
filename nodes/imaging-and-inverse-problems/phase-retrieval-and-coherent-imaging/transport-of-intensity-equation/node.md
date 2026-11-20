---
tag: 5EFCMW
kind: technique
slug: transport-of-intensity-equation
name: Transport of intensity equation
aliases:
- TIE phase retrieval
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: Recover phase from the derivative of intensity along the optical axis by solving the Poisson-type equation that links the two.
prereqs: [phase-retrieval, poisson-equation, angular-spectrum-method, fast-fourier-transform]
see_also: [gerchberg-saxton-algorithm, phase-diversity, digital-holography-reconstruction, phase-unwrapping, spectral-methods, multigrid-method, coherent-diffraction-imaging, least-squares-phase-unwrapping]
sources:
  - paper: doi:10.1364/JOSA.73.001434
    title: Michael Reed Teague, Deterministic phase retrieval, a Green's function solution, Journal of the Optical Society of America 73(11), 1983, 1434 to 1441
    locator: the transport of intensity equation, the substitution of an auxiliary potential and the solution with Green's functions (general locator)
  - paper: doi:10.1103/PhysRevLett.80.2586
    title: David Paganin and Keith A. Nugent, Noninterferometric phase imaging with partially coherent light, Physical Review Letters 80(12), 1998, 2586 to 2589
    locator: the solution of the equation with fast Fourier transforms and its use with partially coherent light (general locator)
  - paper: doi:10.1046/j.1365-2818.2002.01010.x
    title: David Paganin, Sheridan C. Mayo, Timur E. Gureyev, Peter R. Miller and Stephen W. Wilkins, Simultaneous phase and amplitude extraction from a single defocused image of a homogeneous object, Journal of Microscopy 206(1), 2002, 33 to 40
    locator: the single image method for a homogeneous object (general locator)
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, third edition, Roberts and Company, 2005
    locator: the angular spectrum and the Fresnel approximation (general locator)
---

The transport of intensity equation (TIE) links the change of the intensity of a paraxial beam along the optical axis to the phase in a plane across the beam. If you record two or three images at small known distances around focus, the difference of the images gives the derivative of the intensity, and the phase follows from a [Poisson equation](/poisson-equation/). The method is a non-iterative solution of [phase retrieval](/phase-retrieval/) from intensities in several planes. It needs no reference wave, no iteration and only a standard microscope with a focus drive, and it also works with partially coherent light. It is used in optical microscopy, electron microscopy and X-ray imaging.

## In plain words

Light that passes through a clear object, such as a living cell, is bent a little but hardly dimmed. In focus the cell is almost invisible, because a camera sees only brightness. Move the camera a short distance and the bent light starts to collect in some places and spread out in others. A part of the cell that acts like a weak lens makes a bright spot on one side of focus and a dark spot on the other.

So you take one image a little before focus and one a little after. Their difference shows where the light is gathering and where it is leaving. From this pattern you can work back to the shape of the delay that the object put on the light, which is the phase. The work back is a standard equation that a computer solves quickly.

## When it applies

- **A paraxial beam.** The light travels mostly along one axis, and the field changes slowly across the beam on the scale of the wavelength. Under the paraxial wave equation the intensity $I$ and the phase $\phi$ in a plane obey
$$-k \frac{\partial I}{\partial z} = \nabla \cdot (I \nabla \phi), \qquad k = \frac{2\pi}{\lambda},$$
where $\nabla$ acts across the beam (a theorem; the [proof](proofs/correctness.md) derives it).
- **Images at known defocus.** You can record the intensity in two or three planes at known distances $\pm\Delta z$ around the plane of interest, with the same alignment and magnification.
- **A positive intensity** in the field of view, because the method divides by $I$. Dark regions, such as opaque parts of the object or zeros of a speckle field, break it.
- **A smooth phase.** The equation holds for the phase without the wrapping into $(-\pi, \pi]$, and the result is the continuous phase. Phase jumps and vortices, which carry a phase singularity at a zero of the intensity, are outside its scope.
- **Partial coherence.** Paganin and Nugent's analysis shows that the equation keeps a meaning for partially coherent light, where the phase is replaced by a quantity defined through the energy flux.

## The template

Teague (1983) wrote the flux $I \nabla\phi$ as the gradient of an auxiliary function $\psi$. Then the equation splits into two Poisson equations:
$$\nabla^2 \psi = -k \frac{\partial I}{\partial z}, \qquad \nabla^2 \phi = \nabla \cdot \Big(\frac{\nabla\psi}{I}\Big).$$
On a periodic grid each Poisson equation is solved with one forward and one inverse [FFT](/fast-fourier-transform/): divide the coefficient at frequency $f \ne 0$ by $-4\pi^2|f|^2$ and set the mean to zero. This is the approach of Paganin and Nugent (1998).

```pseudo id=main
TIE-PHASE(I_-, I_0, I_+, Δz, λ)
L1  D ← (I_+ - I_-) / (2 Δz)                    ▷ central difference for dI/dz
L2  ψ ← SOLVE-POISSON(-k D)                     ▷ FFT, divide by -4π²|f|², mean 0
L3  g ← ∇ψ                                      ▷ spectral gradient
L4  g ← g / I_0                                 ▷ point by point
L5  return SOLVE-POISSON(∇ · g)                 ▷ φ up to a constant
```

Each step costs a fixed number of FFTs, so a phase image of $n \times n$ pixels costs $O(n^2 \log n)$ (with $n$ a power of two). For a uniform intensity $I_0$ the lines collapse to one solve, $\nabla^2\phi = -(k/I_0)\, \partial_z I$.

The method returns $\phi$ up to a constant when the flux $I\nabla\phi$ is a gradient, which always holds for a uniform intensity (a theorem, in the proof). If $I$ varies, the flux can have a part without divergence, which the data do not see and the method sets to zero.

## Classic examples

- **A pure phase object.** The test file builds a $32 \times 32$ grid with pixel size 1 and wavelength $0.5$ in the same length unit, a uniform amplitude and a phase made of four Gaussian bumps of width 3 pixels and up to 1 radian. The defocused images come from exact [angular spectrum](/angular-spectrum-method/) propagation. The relative error of the recovered phase, after the means are removed, is as follows (measurement). The noisy column adds Gaussian noise with standard deviation $10^{-3}$ of the mean intensity to each image.

| $\Delta z$ | 1 | 4 | 16 | 32 | 64 |
|---|---|---|---|---|---|
| no noise | 3e-4 | 2e-4 | 4.6e-3 | 0.019 | 0.068 |
| noise $10^{-3}$ | 0.087 | 0.022 | 0.0073 | 0.019 | 0.068 |

Without noise the error grows with the step, because the central difference has an error of order $\Delta z^2$. With noise the error falls as the step grows at first, because the noise in $D$ is divided by $\Delta z$, and the best step here is near 16.

- **An absorbing object.** The same phase with an amplitude that varies by up to about 30 percent. With $\Delta z = 4$, the full two-step method gives a relative error of 0.0094, and the one-step formula for a uniform intensity, with the mean intensity in place of $I_0$, gives 0.113 (measurement). The remaining error of the full method is the part of the flux that is not a gradient.
- **Bright field microscopy of cells.** A focus series of an unstained cell gives a quantitative phase map, that is, the optical thickness, without a special phase contrast optic.
- **X-ray and electron imaging.** Propagation-based phase contrast with X-rays and the focus series of transmission electron microscopes use the same equation. For a homogeneous object of one material, Paganin and coworkers (2002) found the phase and the amplitude from a single defocused image.

## Variations

- **Higher order differences.** More planes, used in a higher order finite difference or a fit along $z$, reduce the bias of order $\Delta z^2$ and average the noise.
- **Other solvers.** The Poisson equations can also be solved with [finite differences](/finite-difference-method/), [multigrid](/multigrid-method/) or [spectral methods](/spectral-methods/) with other boundary conditions, for example with a mirror extension of the images, which avoids the jumps that periodic wrapping causes at the image edge.
- **Regularized inversion.** Adding a small constant to $4\pi^2|f|^2$ in the denominator damps the noise at the lowest frequencies, at the cost of a bias in the slow parts of the phase. This is a heuristic trade, and it helps only when the phase has little content at the lowest frequencies.
- **One image of a homogeneous object.** If the ratio of phase shift to absorption of the material is known, one defocused image is enough (Paganin and coworkers 2002).
- **Iterative refinement.** The TIE phase is a good start for an iterative method such as [Gerchberg-Saxton](/gerchberg-saxton-algorithm/) on the same focus series, which can then fit the data at larger defocus where the equation is no longer accurate.

## Pitfalls

- **The wrong step.** A small $\Delta z$ amplifies the noise, and a large one adds bias and breaks the linear model. Measure the noise and try several steps.
- **Low frequency noise.** The inverse Laplacian multiplies the noise at frequency $f$ by $1/|f|^2$. The result often shows slow, cloudy errors in the phase even when the images look clean.
- **Edges of the field.** The FFT solver assumes that the images repeat periodically. Light that enters or leaves the field of view between the planes, or a phase that does not match at opposite edges, adds errors near the border.
- **Zeros of the intensity.** Division by $I$ fails where the intensity is near zero. Use a small floor or exclude these regions, and do not expect correct phase there.
- **Uniform-intensity formula on an absorbing object.** The one-step formula is exact only for a uniform intensity. In the test above it gave an error ten times larger than the full method.
- **Misalignment between planes.** A lateral shift or a change of magnification between the images looks like a phase gradient. Register the images first.
- **Missing flux part.** If the flux has a part without divergence, no TIE solver can see it. This matters for objects with strong absorption next to strong phase gradients.

## Exercises

1. From the paraxial equation $\partial_z A = \frac{i}{2k}\nabla^2 A$, derive the transport of intensity equation for $A = \sqrt{I} e^{i\phi}$.
2. For a uniform intensity $I_0$ and a phase $\phi = a \cos(2\pi x/p)$, compute $\partial_z I$ at the focal plane, and say where the intensity grows after focus.
3. Show that the FFT solver returns the mean-zero solution of $\nabla^2 u = g - \bar g$ for a band-limited $g$, and explain why the mean of the phase is lost.
4. Show that the noise added to the phase by independent noise in the two images falls as $1/\Delta z$, and that its spectrum grows as $1/|f|^4$ at low frequency.
5. Give an intensity $I$ and a phase $\phi$ on a torus for which $I\nabla\phi$ has a part without divergence, and check that the two-step method does not return $\phi$.
6. A focus series is taken with a lateral drift of one pixel between the two images. Estimate the false phase gradient that this adds.

## References
