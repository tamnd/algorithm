---
tag: D5NFP2
kind: technique
slug: fourier-ptychography
name: Fourier ptychography
aliases:
- Fourier ptychographic microscopy
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: research
summary: Light a sample from many angles with a low aperture lens and stitch the images in Fourier space by phase retrieval into a wide field high resolution image.
prereqs: [ptychography, optical-transfer-function, abbe-diffraction-limit, phase-retrieval]
see_also: [epie, structured-illumination-microscopy, aperture-synthesis, super-resolution, point-spread-function, gerchberg-saxton-algorithm, phase-diversity, transport-of-intensity-equation]
sources:
  - paper: doi:10.1038/nphoton.2013.187
    title: Guoan Zheng, Roarke Horstmeyer and Changhuei Yang, Wide-field, high-resolution Fourier ptychographic microscopy, Nature Photonics 7(9), 2013, 739 to 745
    locator: the LED array setup, the forward model with shifted pupils and the iterative recovery (general locator)
  - paper: doi:10.1364/OE.22.004960
    title: Xiaoze Ou, Guoan Zheng and Changhuei Yang, Embedded pupil function recovery for Fourier ptychographic microscopy, Optics Express 22(5), 2014, 4960 to 4972
    locator: the joint recovery of the pupil function with the sample spectrum (general locator)
  - paper: doi:10.1063/1.1823034
    title: J. M. Rodenburg and H. M. L. Faulkner, A phase retrieval algorithm for shifting illumination, Applied Physics Letters 85(20), 2004, 4795 to 4797
    locator: the real space ptychographic update that Fourier ptychography applies in the Fourier plane (general locator)
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, third edition, Roberts and Company, 2005
    locator: the coherent transfer function of an imaging system and the effect of tilted illumination (general locator)
---

Fourier ptychography is a computational microscopy method that gives an image with both a wide field of view and a high resolution, together with its phase. A microscope with a low numerical aperture (NA) objective, which sees a wide field but resolves little, takes a series of intensity images. For each image the sample is lit by a plane wave from a different angle, usually by one LED of an array under the sample. A tilt of the light shifts the spectrum of the sample, so each image holds a different disc of the spectrum. The discs overlap, and a [phase retrieval](/phase-retrieval/) iteration stitches them into one large spectrum. It is [ptychography](/ptychography/) with the roles of real space and Fourier space exchanged. Zheng, Horstmeyer and Yang introduced it in 2013.

## In plain words

A cheap microscope lens with a wide view sees a large area, but it lets in only the light that leaves the sample at small angles, so it misses the fine detail. Fourier ptychography lights the sample from many directions, one after another. Light that comes in at a slant tips the fine detail of the sample into the lens, so each slant shows the lens a different set of details. Each photo is still blurry and has only brightness. But the sets of details overlap from one photo to the next, and a computer finds the one sample that explains all the photos. The result is sharper than any one photo, keeps the wide view, and also shows how much each part of the sample delays the light.

## When it applies

- **A thin sample.** The sample acts as a transmission function $o(r)$. A plane wave with transverse spatial frequency $k_j$ then gives the exit wave $o(r)\, e^{2\pi i k_j \cdot r}$, whose spectrum is $O(k - k_j)$, the spectrum of the sample shifted by $k_j$. For thick samples this shift model fails, because the scattering depends on the angle in a more complex way.
- **A coherent imaging model.** With the coherent transfer function, or pupil, $P(k)$ of the objective, which is zero outside the disc $|k| \le \mathrm{NA}/\lambda$, the camera records
$$I_j(r) = \big| \mathcal{F}^{-1}\{ P(k)\, O(k - k_j) \} \big|^2 .$$
Each LED must be small and far enough to be spatially coherent over the area that is processed, and its light must have a narrow band.
- **Known angles.** The positions of the LEDs relative to the sample are known, or are calibrated or refined.
- **Overlap in Fourier space.** Neighboring discs $\{k : |k - k_j| \le \mathrm{NA}/\lambda\}$ overlap by a large fraction (a heuristic requirement, as in real space ptychography).
- **Dark field images.** Angles with $|k_j| > \mathrm{NA}/\lambda$ give dark field images, which carry the high frequencies and are weak. The camera needs a high dynamic range or longer exposures for them.

The largest frequency that can be recovered is $(\mathrm{NA}_{\text{obj}} + \mathrm{NA}_{\text{ill}})/\lambda$, where $\mathrm{NA}_{\text{ill}}$ is the sine of the largest illumination angle. The sum $\mathrm{NA}_{\text{obj}} + \mathrm{NA}_{\text{ill}}$ is called the synthetic NA. It can exceed the NA of the objective by a large factor and can even exceed 1, but in air it is at most 2, because each term is at most 1 (a theorem of the model).

## The template

1. **Calibrate.** Measure the LED positions and compute $k_j$ for each LED, for each region of the field. Divide the field into small patches in which the angle of each LED is nearly constant.
2. **Record.** Take one image per LED, with exposures that suit the bright field and the dark field images.
3. **Start.** Use the bright field image under normal light, up-sampled to the final grid, as the first estimate of $|o|$ with a flat phase. Its spectrum is the first estimate of $O$ on a large Fourier grid.
4. **Iterate over the LEDs.** For LED $j$:
    - cut the disc of the current spectrum around $-k_j$ and multiply it by the pupil, $\Psi_j(k) = P(k)\, O(k - k_j)$;
    - transform to the image plane, $\psi_j = \mathcal{F}^{-1}\Psi_j$, on the coarse grid of the camera;
    - replace the modulus by the measured one, $\psi_j' = \sqrt{I_j}\, \psi_j / |\psi_j|$;
    - transform back to $\Psi_j'$, and update the spectrum in the disc by the difference $\Psi_j' - \Psi_j$, weighted by $\overline{P}/\max|P|^2$ as in [ePIE](/epie/);
    - if the pupil is also unknown, update it with the conjugate of the spectrum, as in the probe step of ePIE (Ou, Zheng and Yang 2014).
5. **Repeat** the sweep over all LEDs until the data error stops falling, often in tens of sweeps.
6. **Output** $o = \mathcal{F}^{-1} O$: an amplitude and a phase image with the synthetic resolution.

The update is the real space ptychographic update of Rodenburg and Faulkner (2004) applied in the Fourier plane, with the pupil in place of the probe and the shift $k_j$ in place of the position $r_j$. Like other methods based on the modulus constraint, it has no general convergence guarantee. The method is accurate in practice when the overlap is large and the model holds (a measurement reported by Zheng and coworkers).

## Classic examples

- **The first system.** Zheng, Horstmeyer and Yang (2013) added an LED array to a standard microscope with a low NA objective, recorded images under single LEDs, and reconstructed images with a resolution far beyond that of the objective over its full field of view. The result has a space-bandwidth product much larger than the camera alone gives.
- **Pupil recovery.** Ou, Zheng and Yang (2014) recovered the aberrations of the objective together with the sample. A low cost lens with large aberrations can then still give a sharp result.
- **Quantitative phase of cells and tissue.** The recovered phase gives the optical thickness of unstained samples, as in the [transport of intensity equation](/transport-of-intensity-equation/), but with a resolution set by the synthetic NA.

## Variations

- **Multiplexed illumination.** Several LEDs are switched on together, and the model sums the intensities of their images. This cuts the number of images and the time.
- **Thick samples.** A multislice model or a diffraction tomography model replaces the thin sample model, and the data then give a three-dimensional map.
- **Gradient and second order methods.** The fit can be written as a loss over all images and minimized with gradient methods, with a noise model that fits the photon statistics.
- **Angle refinement.** The illumination angles are refined during the reconstruction, which corrects errors in the position of the LED array.
- **Relation to other methods.** [Structured illumination microscopy](/structured-illumination-microscopy/) also moves high frequencies into the pass band of the lens, but with incoherent fluorescence. [Aperture synthesis](/aperture-synthesis/) in radio astronomy also combines discs of the spectrum, but measures their phase directly by interferometry.

## Pitfalls

- **Wrong angles.** An error in the LED position shifts the disc in Fourier space and blurs the result. Calibrate the array and refine the angles.
- **Patches that are too large.** Across a wide field the angle of each LED changes, so one shift for the whole image is wrong. Process small patches with their own angles and blend them.
- **Weak dark field data.** The high frequencies come from the weakest images. Noise and stray light there limit the real resolution. Use longer exposures for these LEDs and a noise model in the fit.
- **Partial coherence and the LED spectrum.** A broad LED band or a large LED blurs the data. Use a narrow band filter and LEDs that are small compared with their distance.
- **The thin sample model.** For thick samples the result can look sharp but be wrong. Check against a known sample of similar thickness.
- **Phase wrapping.** The recovered phase is wrapped. Use [phase unwrapping](/phase-unwrapping/) for a quantitative thickness map.

## Exercises

1. Show that the spectrum of $o(r)\, e^{2\pi i k_j \cdot r}$ is $O(k - k_j)$, and draw the part of the spectrum of the sample that the pupil passes for this light.
2. For an objective of NA 0.1 and illumination angles up to a sine of 0.4, compute the synthetic NA and the smallest resolved period at a wavelength of 0.5 micrometre.
3. Two neighboring LEDs give discs that overlap by a fraction $f$ of their area. Find the distance between the centers in terms of the pupil radius for $f = 0.6$.
4. Show that a sample $o$ and the sample $c\, o$ with $|c| = 1$ give the same images. Then show that a pupil $P$ and an object spectrum $O$ give the same images as $cP$ and $O/c$ for any nonzero $c$.
5. Compare the update of step 4 with the ePIE object update, and name each quantity that plays the role of the probe, the object and the position.
6. Explain why the images under bright field light alone cannot give a resolution better than $2\,\mathrm{NA}_{\text{obj}}/\lambda$ in frequency.

## References
