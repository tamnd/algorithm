---
tag: JP94MG
kind: technique
slug: coherent-diffraction-imaging
name: Coherent diffraction imaging
aliases:
- CDI
- lensless imaging
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: Image a small isolated object by recording its far field diffraction intensity with coherent X-rays and recovering the phase by iteration.
prereqs: [phase-retrieval, oversampling-in-phase-retrieval, hybrid-input-output, discrete-fourier-transform]
see_also: [shrinkwrap, difference-map, raar, error-reduction-algorithm, ptychography, phase-retrieval-ambiguities, single-particle-reconstruction, crystallographic-phase-problem]
sources:
  - paper: doi:10.1107/S0365110X52002276
    title: D. Sayre, Some implications of a theorem due to Shannon, Acta Crystallographica 5(6), 1952, 843
    locator: the remark that sampling the diffraction pattern between the Bragg peaks would give more information (general locator)
  - paper: doi:10.1364/JOSAA.15.001662
    title: Jianwei Miao, David Sayre and H. N. Chapman, Phase retrieval from the magnitude of the Fourier transforms of nonperiodic objects, Journal of the Optical Society of America A 15(6), 1998, 1662 to 1669
    locator: the oversampling ratio and its role in iterative reconstruction (general locator)
  - paper: doi:10.1038/22498
    title: Jianwei Miao, Pambos Charalambous, Janos Kirz and David Sayre, Extending the methodology of X-ray crystallography to allow imaging of micrometre-sized non-crystalline specimens, Nature 400(6742), 1999, 342 to 344
    locator: the first image of a non-crystalline object from an oversampled X-ray diffraction pattern (general locator)
  - paper: doi:10.1364/AO.21.002758
    title: J. R. Fienup, Phase retrieval algorithms, a comparison, Applied Optics 21(15), 1982, 2758 to 2769
    locator: the error-reduction and hybrid input-output algorithms (general locator)
  - paper: doi:10.1103/PhysRevB.68.140101
    title: S. Marchesini, H. He, H. N. Chapman, S. P. Hau-Riege, A. Noy, M. R. Howells, U. Weierstall and J. C. H. Spence, X-ray image reconstruction from a diffraction pattern alone, Physical Review B 68(14), 2003, 140101
    locator: the shrinkwrap update of the support (general locator)
  - paper: doi:10.1038/nphoton.2010.240
    title: Henry N. Chapman and Keith A. Nugent, Coherent lensless X-ray imaging, Nature Photonics 4(12), 2010, 833 to 839
    locator: review of the methods and their applications (general locator)
---

Coherent diffraction imaging (CDI) forms an image of a small isolated object without an objective lens. A coherent beam, usually of X-rays or electrons, lights the object. A detector in the far field records the intensity of the diffraction pattern, which is the squared modulus of the Fourier transform of the exit wave. The phase of the pattern is lost, and a computer recovers it by [phase retrieval](/phase-retrieval/) with the constraint that the object is zero outside a finite region, its support. The resolution is then limited by the largest angle at which the pattern can be measured, not by the quality of a lens. This matters most for X-rays, for which good lenses are hard to make.

## In plain words

To see very small things, you need very short waves, such as X-rays. But it is hard to make a lens for X-rays. CDI leaves out the lens. It shines a clean, even beam on a tiny object and puts a camera far behind it. The camera records a pattern of bright and dark speckles made by the scattered waves.

The pattern holds only the brightness of each wave, not its timing, so it cannot be turned back into a picture directly. The missing part is found by computer. The program knows that the object is small and sits alone in empty space. It guesses the missing part, makes a picture, clears everything outside the small region, goes back to the pattern and repeats. After many rounds the picture settles on the object.

## When it applies

- **An isolated object.** The exit wave is zero, or known, outside a region $S$ that is much smaller than the field that the detector sampling allows. This is the support constraint.
- **Coherent illumination.** The beam is spatially coherent across the whole object and has a narrow bandwidth, so that the waves from all parts of the object interfere. With partial coherence the speckles lose contrast, and the simple model $I = |\mathcal{F}\psi|^2$ fails.
- **The far field.** The detector is in the Fraunhofer region, or a known lens or a curved beam maps the pattern to a Fourier transform. Then the measured intensity is $I(q) = |\Psi(q)|^2$, where $\Psi$ is the Fourier transform of the exit wave $\psi$ and $q$ is the scattering vector.
- **Oversampling.** The detector samples the pattern at least twice as finely in each direction as the inverse of the object width. Then the inverse transform of the intensity, the [autocorrelation](/autocorrelation/) of $\psi$, is not aliased, because the autocorrelation is twice as wide as the object. This is a theorem of sampling (see [oversampling](/oversampling-in-phase-retrieval/)). Sayre (1952) pointed out that the intensity between the Bragg peaks of a crystal holds this extra information, which a crystal cannot give.
- **A thin object, or the projection approximation.** The exit wave is the product of the beam and a transmission function of the object. For thick objects, the data are a slice of the three-dimensional Fourier transform on the Ewald sphere.

## The template

1. **Record.** Measure the pattern with several exposures to cover its large dynamic range. A beam stop blocks the direct beam and leaves a hole in the data near $q = 0$.
2. **Prepare the data.** Subtract the background, merge the exposures, find the center of the pattern and take the square root of the intensity to get the modulus $|\Psi|$. Mark the pixels that are missing (the beam stop, gaps between detector modules, saturated pixels).
3. **Start the support.** Take the inverse Fourier transform of the intensity. It is the autocorrelation, and its support contains every difference of two points of the object support. A threshold of the autocorrelation gives a loose first support.
4. **Iterate.** Run an iterative projection method such as [hybrid input-output](/hybrid-input-output/), the [difference map](/difference-map/) or [RAAR](/raar/). In Fourier space, replace the modulus by the measured one at the measured pixels and keep the current value at the missing pixels. In real space, apply the support and, where it holds, a constraint such as a real and positive density. Update the support every few iterations with [shrinkwrap](/shrinkwrap/).
5. **Refine.** End with a number of [error reduction](/error-reduction-algorithm/) steps, which do not increase the error (a theorem of Fienup 1982), to settle near a fixed point.
6. **Check.** Repeat from many random starts. Align the results for the trivial [ambiguities](/phase-retrieval-ambiguities/): a constant phase, a shift and the conjugate reflection (the twin). Average them, and use their agreement at each spatial frequency as a measure of the resolution.

A two-dimensional pattern of an object with a known support usually determines the object up to the trivial ambiguities, while in one dimension it does not. The statement for two and more dimensions holds for almost all objects, in a sense that is made precise by [Bruck and Sodin](/bruck-sodin-uniqueness/) and its successors. A given experiment can still fall in the exceptions or be too noisy, so uniqueness is a guide, not a guarantee.

## Classic examples

- **The first X-ray image.** Miao and coworkers (1999) recorded an oversampled X-ray pattern of a small non-periodic test pattern and recovered its image with iterative phase retrieval. This showed that the methods of optical phase retrieval work with X-ray data.
- **Shrinkwrap on X-ray data.** Marchesini and coworkers (2003) reconstructed an X-ray test object from the diffraction pattern alone, with no separate knowledge of the support, by updating the support during the iteration.
- **Strain in nanocrystals.** In the Bragg geometry, the pattern around one Bragg peak of a small crystal gives the shape of the crystal and a phase that measures the displacement of the lattice. CDI in this geometry maps strain inside single nanocrystals.
- **Single particles with X-ray free electron lasers.** A short and intense pulse can record a pattern before the particle is destroyed. Many patterns of identical particles in random orientations are oriented and merged in three dimensions, as in [single particle reconstruction](/single-particle-reconstruction/), and then phased.
- **Optical demonstrations.** With a laser and a small transparent mask, the whole chain fits on a table and is a common test bed for new algorithms.

## Variations

- **[Ptychography](/ptychography/).** Scan a confined beam across an extended object and record a pattern at each position. The overlap of the illuminated areas replaces the support constraint and also recovers the beam.
- **Fresnel CDI.** Light the object with a curved beam of known phase. The data then carry information that breaks the twin ambiguity and helps convergence.
- **Holographic CDI.** Place a small reference object next to the sample. The autocorrelation then contains a direct image of the sample, as in holography, which can start or replace the iteration.
- **Tomographic CDI.** Record patterns for many rotations of the object and reconstruct its three-dimensional density.
- **Bragg CDI.** As in the strain example above, the pattern is taken around a Bragg peak instead of around the direct beam.

## Pitfalls

- **Missing center.** The beam stop removes the lowest frequencies. If the hole is larger than the speckle size, some slowly varying images fit the data and the support equally well, and the iteration cannot fix them. Keep the hole small, or fill it with a separate low resolution measurement.
- **A support that is wrong.** A support that is too tight cuts off parts of the object; one that is too loose weakens the constraint so that the iteration may not converge. Shrinkwrap thresholds need tuning.
- **Partial coherence.** It lowers the contrast of the speckles, and the algorithm then tries to explain the blurred data with a wrong object. Measure the coherence or include it in the model.
- **Stagnation with the twin.** The iteration can stall in a mix of the object and its conjugate reflection. Restarts and a support that is not centrally symmetric help.
- **Noise at high angles.** The intensity falls quickly with the angle, so the outer speckles carry few photons. The resolution is limited by the dose, not only by the size of the detector.
- **An object that is not isolated.** Anything else in the beam, such as a substrate or dust, breaks the support constraint.

## Exercises

1. Show that the inverse Fourier transform of $|\Psi|^2$ is the autocorrelation of $\psi$, and that its support is the set of differences of points in the support of $\psi$.
2. An object is 1 micrometre wide and the wavelength is 1 nanometre. At a distance of 1 metre, how large may the detector pixels be so that the pattern is oversampled by 2 in each direction?
3. Show that a shift of the object, a constant phase factor and the conjugate reflection $\overline{\psi(-x)}$ give the same intensity.
4. Explain why a support that is centrally symmetric cannot tell the object from its twin, and why a support that is not symmetric can.
5. Suppose that a beam stop removes all frequencies with $|q| < q_0$. Describe the images that fit the data and a support, and explain why their number grows with $q_0$.
6. Compare CDI with [ptychography](/ptychography/): list what each needs to know before the iteration starts.

## References
