---
tag: 6Q14YT
kind: concept
slug: speckle
name: Speckle in coherent imaging
aliases:
- coherent speckle
- fully developed speckle
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "The granular pattern from the interference of echoes of many unresolved scatterers in coherent imaging. When fully developed, the amplitude is Rayleigh distributed and the intensity is exponential."
prereqs: [pulse-echo-imaging, central-limit-theorem]
see_also: [image-noise, speckle-interferometry, synthetic-aperture-radar, b-mode-image-formation, coherence-factor, van-cittert-zernike-theorem, median-filter, non-local-means]
sources:
  - book: isbn:9780974707792
    title: "Joseph W. Goodman, Speckle Phenomena in Optics: Theory and Applications, Roberts and Company, 2007"
    locator: "Chapter 2, Random Phasor Sums; Chapter 3, First-Order Statistical Properties"
  - paper: doi:10.1109/T-SU.1978.30978
    title: "Christoph B. Burckhardt, Speckle in ultrasound B-mode scans, IEEE Transactions on Sonics and Ultrasonics 25(1), 1978, 1 to 6"
    locator: "speckle in ultrasound images as an interference effect and its first-order statistics (general locator)"
  - paper: doi:10.1109/T-SU.1983.31404
    title: "Robert F. Wagner, Stephen W. Smith, John M. Sandrik and Hector Lopez, Statistics of speckle in ultrasound B-scans, IEEE Transactions on Sonics and Ultrasonics 30(3), 1983, 156 to 163"
    locator: "the signal-to-noise ratio 1.91 of the Rayleigh amplitude, the second-order statistics and the speckle size (general locator)"
---

Speckle is the granular pattern that appears in every coherent imaging system when many scatterers lie inside one resolution cell. Each scatterer adds an echo with its own amplitude and phase, and the detected value is the modulus of the sum: a random phasor sum. Where the phases happen to agree, the pixel is bright; where they cancel, it is dark. So speckle is not noise added by the detector, but a deterministic interference pattern of the unknown fine structure of the object, which looks random because that structure is. The same effect occurs in medical ultrasound, in [synthetic aperture radar](/synthetic-aperture-radar/), and in optics, with laser light and with starlight through turbulence; [speckle interferometry](/speckle-interferometry/) uses the speckle of short astronomical exposures to recover detail at the diffraction limit. The page on [image noise](/image-noise/) treats speckle as one noise model among others, a multiplicative one; this page explains where it comes from. When the number of scatterers per cell is large and their phases are uniform, the speckle is fully developed: the amplitude has a Rayleigh distribution and the intensity an exponential one, with a ratio of mean to standard deviation of $1.91$ for the amplitude and $1$ for the intensity.

## In plain words

Shine a laser on a wall, or send ultrasound into tissue, and look at the image up close. It is full of small bright and dark spots, even where the wall or the tissue looks the same everywhere. Each spot is made by many tiny reflectors that are too close together to see one by one. Their echoes meet at the detector with random timing. Sometimes they add up, sometimes they cancel. The spots do not show the reflectors themselves; they show how their echoes happen to mix. Move the probe a little and the pattern changes. Averaging several different looks makes it smoother.

## The idea

**The random phasor sum.** Model the complex value of one pixel as

$$A = \frac{1}{\sqrt N} \sum_{k=1}^{N} a_k e^{i \varphi_k},$$

with independent terms, phases $\varphi_k$ uniform on $[0, 2\pi)$ and independent of the amplitudes $a_k$, and $\mathbb{E}[a_k^2] = 2\sigma^2$. The terms have mean $0$, and the real and imaginary parts are uncorrelated with equal variance $\sigma^2$. By the [central limit theorem](/central-limit-theorem/), as $N$ grows, $A$ tends to a circular complex Gaussian variable (Goodman 2007, Chapter 2).

**First-order statistics** (theorems for the limit model). For a circular complex Gaussian $A$ with $\mathbb{E}|A|^2 = 2\sigma^2$:

- the amplitude $|A|$ has the Rayleigh density $\frac{u}{\sigma^2} e^{-u^2/(2\sigma^2)}$ for $u \ge 0$, with mean $\sigma\sqrt{\pi/2}$ and standard deviation $\sigma\sqrt{(4 - \pi)/2}$;
- the intensity $I = |A|^2$ has the exponential density $\frac{1}{\langle I\rangle} e^{-I/\langle I\rangle}$, with standard deviation equal to its mean $\langle I\rangle = 2\sigma^2$;
- so the amplitude signal-to-noise ratio, mean over standard deviation, is $\sqrt{\pi/(4 - \pi)} = 1.9131$, and the intensity ratio is $1$, whatever the mean level;
- the probability that the intensity exceeds $k$ times its mean is $e^{-k}$.

The amplitude ratio $1.91$ is the value that Wagner et al. (1983) give for fully developed ultrasound speckle. These statements are theorems only for the random phasor model in the limit. Real tissue can have few scatterers per cell, a regular structure, or a strong reflector, and then the statistics differ.

**Speckle is multiplicative.** If the local mean reflectivity of a region is $\mu$, the intensity is $\mu$ times an exponential variable of mean $1$. A filter for additive noise does not fit this model; this is why speckle reduction often works on the log of the image, or with filters built for this ratio.

**Grain size** (heuristic). The speckle pattern has a correlation length set by the [point-spread function](/point-spread-function/) of the system, not by the scatterers: about the pulse length along depth and about $\lambda F$ across the beam for the f-number $F$. Wagner et al. (1983) derive the second-order statistics for ultrasound. The [van Cittert-Zernike theorem](/van-cittert-zernike-theorem/) gives the matching coherence of the echoes across the receive aperture.

**Partially developed speckle.** With few scatterers per cell, or with one strong reflector added to the random sum (the Rician case), the amplitude ratio rises above $1.91$. With unresolved but regularly spaced scatterers, the phases are not uniform and the model fails.

## Examples

All numbers are from a Monte Carlo simulation with a fixed seed, 20000 trials and unit-amplitude phasors scaled so that $\mathbb{E}|A|^2 = 1$. They are measurements, and they match the theory within the expected error.

| case | amplitude mean over standard deviation | theory |
|---|---|---|
| $N = 50$ phasors | 1.9217 | 1.9131 (Rayleigh) |
| $N = 3$ phasors | 2.202 | above 1.91 |
| $N = 50$ plus a constant phasor of amplitude 2 | 3.150 | above 1.91 (Rician) |

For $N = 50$ the intensity ratio is $1.0068$, against $1$. With $\mathbb{E}|A|^2 = 1$, the Rayleigh mean is $\sqrt{\pi}/2 = 0.8862$ and the standard deviation $\sqrt{1 - \pi/4} = 0.4633$.

**Averaging looks.** The mean of $L$ independent exponential intensities has the ratio $\sqrt L$. For $L = 4$ the simulation gives $2.03$, against $2$. This is the principle of compounding in ultrasound and of multilook processing in radar: average images with different angles, frequencies or sub-apertures, whose speckle is independent, at the cost of resolution or time.

**Bright spots.** In fully developed speckle, $e^{-3} = 4.98$ percent of the pixels have more than three times the mean intensity. A single bright spot in speckle is therefore not evidence of a target.

**The coherence factor of speckle.** Under the triangular coherence that the van Cittert-Zernike theorem gives at the focus, the [coherence factor](/coherence-factor/) of speckle is near $2/3$, between $1$ for a point target and $1/M$ for noise.

## Where it is used

- **Ultrasound imaging.** The texture of tissue in a [B-mode image](/b-mode-image-formation/) is speckle. It limits the detection of low-contrast lesions, and its statistics are used to characterize tissue and to track motion (speckle tracking).
- **Speckle reduction.** Spatial and frequency compounding, [median filters](/median-filter/), [non-local means](/non-local-means/) and other filters on the log image lower its variance; adaptive beamformers change it too.
- **Synthetic aperture radar.** SAR images show the same statistics; multilook processing averages independent looks, and the speckle model is the basis of SAR filters and change detection.
- **Optics.** Laser speckle limits coherent imaging and is also used to measure the motion and deformation of surfaces. In astronomy, turbulence turns a star into a speckle pattern, and [speckle interferometry](/speckle-interferometry/) averages the power spectra of many short exposures to recover the diffraction-limited spectrum.
- **Image noise models.** [Image noise](/image-noise/) lists speckle as the multiplicative model next to Gaussian and Poisson noise.

## References
