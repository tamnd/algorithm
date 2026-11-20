---
tag: XAXWJY
kind: technique
slug: ptychography
name: Ptychography
aliases:
- scanning coherent diffraction imaging
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: Record diffraction patterns as a probe scans an object with overlapping positions, which gives redundant data to recover object and probe.
prereqs: [phase-retrieval, coherent-diffraction-imaging, discrete-fourier-transform]
see_also: [epie, difference-map, fourier-ptychography, maximum-likelihood-estimation, stochastic-gradient-descent, phase-retrieval-ambiguities, angular-spectrum-method, phase-diversity]
sources:
  - paper: doi:10.1107/S0567739469001045
    title: W. Hoppe, Beugung im inhomogenen Primarstrahlwellenfeld. I. Prinzip einer Phasenmessung von Elektronenbeugungsinterferenzen, Acta Crystallographica A 25(4), 1969, 495 to 501
    locator: the principle of phase measurement with an inhomogeneous illumination (general locator)
  - paper: doi:10.1063/1.1823034
    title: J. M. Rodenburg and H. M. L. Faulkner, A phase retrieval algorithm for shifting illumination, Applied Physics Letters 85(20), 2004, 4795 to 4797
    locator: the iterative reconstruction from patterns at overlapping positions with a known probe (general locator)
  - paper: doi:10.1126/science.1158573
    title: Pierre Thibault, Martin Dierolf, Andreas Menzel, Oliver Bunk, Christian David and Franz Pfeiffer, High-resolution scanning X-ray diffraction microscopy, Science 321(5887), 2008, 379 to 382
    locator: the joint reconstruction of object and probe with the difference map (general locator)
  - paper: doi:10.1016/j.ultramic.2008.12.011
    title: Pierre Thibault, Martin Dierolf, Oliver Bunk, Andreas Menzel and Franz Pfeiffer, Probe retrieval in ptychographic coherent diffractive imaging, Ultramicroscopy 109(4), 2009, 338 to 343
    locator: probe retrieval and the artifacts of scans on a regular grid (general locator)
  - paper: doi:10.1016/j.ultramic.2009.05.012
    title: Andrew M. Maiden and John M. Rodenburg, An improved ptychographical phase retrieval algorithm for diffractive imaging, Ultramicroscopy 109(10), 2009, 1256 to 1262
    locator: the extended ptychographical iterative engine (general locator)
---

Ptychography is a form of [coherent diffraction imaging](/coherent-diffraction-imaging/) for objects of any size. A confined coherent beam, the probe, lights a small area of the object, and a detector records the far field diffraction intensity. The object or the probe is then moved, and the next pattern is recorded at a position whose lit area overlaps the last one. Each part of the object appears in several patterns, so the data hold many more numbers than the unknowns. This redundancy lets a computer recover the complex transmission of the object and, in most cases, the probe as well. The recovery is a [phase retrieval](/phase-retrieval/) problem that needs no support constraint and no lens of high quality.

## In plain words

Imagine looking at a large painting through a small round hole that moves across it. At each place you cannot see the painting itself, only a blurred pattern of light that passed through the hole. One pattern is not enough to work out what is in the hole. But the hole moves in small steps, so every spot of the painting is seen through the hole several times, from slightly different places. Each pattern must agree with its neighbors where they share the same spot. These shared parts tie the patterns together, and a computer can find the one painting, and even the shape of the light in the hole, that explains all the patterns at once.

## When it applies

- **The thin object model.** At position $j$ the exit wave is the product $\psi_j(r) = P(r - r_j)\, O(r)$ of the probe $P$ and the object transmission $O$, and the detector records $I_j(q) = |\mathcal{F}\psi_j(q)|^2$. For a thick object the product is replaced by a multislice model.
- **A stable probe.** The probe does not change during the scan, or changes in a way that is modeled.
- **Known positions.** The positions $r_j$ are known to a fraction of the resolution, or can be refined in the reconstruction.
- **Overlap.** Neighboring lit areas overlap by a large fraction. A common rule is an overlap of more than half the probe diameter (a heuristic).
- **Coherence.** The probe is coherent over its own area, or its partial coherence is modeled as a mix of a few coherent modes.
- **Sampling.** Each pattern is sampled finely enough to hold the field of the probe area. The detector pixel size and the distance fix the size of the reconstructed window.

## The template

1. **Design the scan.** Choose the probe size, the step and the pattern of positions. Avoid a perfectly regular grid: Thibault and coworkers (2009) showed that a regular raster lets a periodic error be shared between the object and the probe. Spiral or jittered scans avoid it.
2. **Record.** Collect one pattern per position, with the same exposure and the same detector geometry.
3. **Prepare the data.** Subtract the background, take the square root to get the moduli, and mark missing pixels.
4. **Start.** Set the object to a constant, and set the probe to a model of the optics, such as the focus of a lens or an aperture.
5. **Iterate.** Use an algorithm that updates the object and the probe from the patterns. [ePIE](/epie/) updates them one position at a time, in a random order. The [difference map](/difference-map/) treats all positions at once and was the first method to retrieve the probe (Thibault and coworkers 2008). A [maximum likelihood](/maximum-likelihood-estimation/) refinement with a model of the photon noise often follows.
6. **Refine the positions** if their error is comparable to the resolution.
7. **Remove the ambiguities.** The data do not change if the object is multiplied by a constant $c$ and the probe divided by $c$, or if a linear phase ramp moves between them. Fix the scale and the phase in a region of known value, and remove the ramp.

The data at position $j$ fix the modulus of a Fourier transform, which is a nonconvex constraint, so no algorithm of this kind has a general guarantee of convergence. The success of ptychography is a measurement: it works in practice for a wide range of samples, and the overlap is the main reason.

## Classic examples

- **The idea in electron diffraction.** Hoppe (1969) proposed to light a crystal with a confined, inhomogeneous beam, so that neighboring diffraction orders overlap and interfere, which gives access to their relative phase. The name ptychography comes from the Greek word for fold.
- **The iterative engine.** Rodenburg and Faulkner (2004) gave an iterative algorithm for many overlapping positions with a known probe. This turned ptychography into a practical method for extended objects.
- **Scanning X-ray diffraction microscopy.** Thibault and coworkers (2008) recovered both the object and the probe from X-ray data, with high resolution and with a probe that did not need to be known in advance.
- **Electron ptychography.** With a fast pixel detector in a scanning transmission electron microscope, the same method gives phase images of atoms, with resolution beyond that of the probe forming lens.
- **Ptychographic tomography.** Scans at many rotation angles give projections of the phase, which are then combined by tomography into a three-dimensional map of the electron density.

## Variations

- **[Fourier ptychography](/fourier-ptychography/).** The roles of real and Fourier space are exchanged: the object is lit from many angles, and a lens with a small aperture records images instead of diffraction patterns.
- **Mixed states.** The probe is written as an incoherent sum of a few coherent modes. This models partial coherence and vibrations.
- **Multislice ptychography.** The object is a stack of thin slices with free propagation between them, which models thick samples and gives depth information.
- **Near field ptychography.** The detector is in the Fresnel region, and the propagation is done with the [angular spectrum method](/angular-spectrum-method/). A diffuser in the beam gives the needed diversity with few positions.
- **Gradient methods.** The fit to the data can be written as a loss and minimized with automatic differentiation and [stochastic gradient](/stochastic-gradient-descent/) steps over the positions. ePIE is close to such a method with a special step size.

## Pitfalls

- **Raster grid artifacts.** On a regular grid, a periodic pattern can move between the object and the probe without changing the data. Use a scan that is not periodic.
- **Too little overlap.** The redundancy falls and the iteration can fail to converge, in particular when the probe is also unknown.
- **Position errors.** Errors in the positions blur the result and add false structure. Refine the positions or measure them with an interferometer.
- **Probe drift.** A probe that changes during the scan cannot be fitted by one function. Use several probe modes or split the scan.
- **Phase wrapping.** The recovered phase of a strong object is wrapped into $(-\pi, \pi]$. Use [phase unwrapping](/phase-unwrapping/) before a quantitative use.
- **Scale and ramp.** Compare reconstructions only after removing the constant factor and the phase ramp that the data cannot fix.

## Exercises

1. Show that $(cO, P/c)$ for a nonzero complex $c$ gives the same data as $(O, P)$.
2. Put a linear phase ramp $e^{2\pi i a \cdot r}$ on the object and the opposite ramp $e^{-2\pi i a \cdot r}$ on the probe. Show that each exit wave changes only by a constant phase factor, so the data do not change.
3. Count the measured numbers and the unknowns for $J$ positions, patterns of $m \times m$ pixels and an object of $M \times M$ pixels, and find the ratio for a step of a quarter of the probe width.
4. On a regular grid with step $s$, construct a periodic function $f$ with period $s$ such that $(Of, P/f)$ gives the same data as $(O, P)$ at all positions.
5. Explain why ptychography needs no support constraint, while single shot CDI does.
6. Compare the update of ePIE with one step of stochastic gradient descent on $\sum_j \lVert |\mathcal{F}(P_j O)| - \sqrt{I_j}\rVert^2$.

## References
