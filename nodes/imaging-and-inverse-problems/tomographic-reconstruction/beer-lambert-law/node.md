---
tag: J72ZYM
kind: theorem
slug: beer-lambert-law
name: Beer-Lambert law
aliases:
- Beer's law
area: imaging-and-inverse-problems/tomographic-reconstruction
level: intro
summary: The intensity of a ray through matter falls as the exponential of minus the line integral of the attenuation, which makes CT data line integrals after a log.
model: real-ram
prereqs: []
see_also: [radon-transform, x-ray-transform, sinogram, beam-hardening, attenuated-radon-transform, participating-media, precomputed-atmospheric-scattering, poisson-distribution]
sources:
  - book: "P. Bouguer, Essai d'optique sur la gradation de la lumière, Paris, 1729"
    title: P. Bouguer, Essai d'optique sur la gradation de la lumière, 1729
    locator: whole book (equal thicknesses of a uniform medium take away equal fractions of the light)
  - book: "J. H. Lambert, Photometria sive de mensura et gradibus luminis, colorum et umbrae, Augsburg, 1760"
    title: J. H. Lambert, Photometria, 1760
    locator: whole book (the exponential law of absorption in mathematical form)
  - paper: doi:10.1002/andp.18521620505
    title: A. Beer, Bestimmung der Absorption des rothen Lichts in farbigen Flüssigkeiten, Annalen der Physik 162(5), 1852
    locator: pp. 78 to 88 (the absorption of a solution depends on the product of concentration and thickness)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 4, Section 4.1 (the attenuation of monochromatic X-rays and the line integral after a log, and the polychromatic case)
---

The Beer-Lambert law is the law of exponential attenuation of light along a path through an absorbing medium. Each short piece of the path removes a fixed fraction of the light that reaches it, and this fraction is proportional to the length of the piece and to the local attenuation coefficient $\mu$. So the transmitted fraction is $e^{-\int \mu\,ds}$. In chemistry, $\mu$ is proportional to the concentration of a dye, and the log of the transmitted fraction measures the concentration. In computer graphics, the same factor is the transmittance of [participating media](/participating-media/) such as fog or air ([precomputed atmospheric scattering](/precomputed-atmospheric-scattering/)). In X-ray computed tomography, the log of the measured fraction is the line integral of $\mu$ along the ray, and these line integrals are the [Radon transform](/radon-transform/) of the attenuation map. The law is a model: it holds for a monochromatic beam in which each photon is either absorbed or passes straight on. It fails when the beam has many energies or when scattered photons reach the detector.

## Statement

**Theorem.** Let $\mu : [0, L] \to [0, \infty)$ be integrable, and let $I_0 > 0$. The equation
$$\frac{dI}{ds}(s) = -\mu(s)\,I(s), \qquad I(0) = I_0,$$
has exactly one absolutely continuous solution $I$ on $[0, L]$ that satisfies it at almost every $s$, and
$$I(s) = I_0\exp\left(-\int_0^s \mu(t)\,dt\right).$$
In particular the fraction that leaves the path is $I(L)/I_0 = e^{-p}$ with $p = \int_0^L \mu(t)\,dt$, and $p = -\ln(I(L)/I_0)$.

For a ray along a line $\ell$ through an object with attenuation map $\mu(x)$, the theorem gives $-\ln(I/I_0) = \int_\ell \mu$, the [X-ray transform](/x-ray-transform/) of $\mu$ on $\ell$. In the plane this is $\mathcal{R}\mu(\theta, s)$.

**Example.** A ray passes through 2 cm of a tissue with $\mu = 0.5\ \mathrm{cm}^{-1}$ and then through 3 cm of a tissue with $\mu = 0.2\ \mathrm{cm}^{-1}$. The line integral is $p = 0.5\cdot 2 + 0.2\cdot 3 = 1.6$, and $I/I_0 = e^{-1.6} = 0.20190$. The order of the two layers does not change the result.

## In plain words

Light that goes through a tinted glass loses part of itself. A second, equal glass loses the same share of what is left, not the same amount. So the light falls by a fixed factor for each layer, and the total factor for a stack is the product of the factors of the layers. A log turns this product into a sum. The sum adds, over the path, how strongly each place absorbs. A CT scanner measures how much of the beam gets through, takes the log, and so gets this sum for each ray. The rule assumes that each photon is absorbed or goes straight through. A beam with many energies, or photons that bounce into the detector, break it.

## Proof

Put $M(s) = \int_0^s \mu(t)\,dt$. Since $\mu$ is integrable, $M$ is absolutely continuous on $[0, L]$ with $M' = \mu$ almost everywhere, and so is $e^{\pm M}$, by the chain rule for absolutely continuous functions composed with a smooth function.

Existence: $I(s) = I_0 e^{-M(s)}$ is absolutely continuous, $I(0) = I_0$, and $I'(s) = -\mu(s)\,I_0 e^{-M(s)} = -\mu(s)\,I(s)$ at almost every $s$.

Uniqueness: let $I$ be any absolutely continuous solution, and put $J(s) = I(s)\,e^{M(s)}$. A product of absolutely continuous functions on a compact interval is absolutely continuous, and at almost every $s$
$$J'(s) = \big(I'(s) + \mu(s)\,I(s)\big)\,e^{M(s)} = 0.$$
An absolutely continuous function with derivative 0 almost everywhere is constant, so $J(s) = J(0) = I_0$, and $I(s) = I_0 e^{-M(s)}$. $\square$

The equation itself is the physical assumption. Over a short piece $ds$, a photon at $s$ is absorbed with probability $\mu(s)\,ds$, independently of what happened before. The expected number of photons then satisfies $I(s + ds) = I(s)\,(1 - \mu(s)\,ds)$, which is the equation in the limit.

## Consequences

- **Products of layers.** For a path through layers with constant $\mu_i$ and lengths $\ell_i$, the transmitted fraction is $\prod_i e^{-\mu_i\ell_i} = e^{-\sum_i \mu_i\ell_i}$. [Ray marching](/ray-marching/) in volume rendering computes transmittance by this product, one step at a time.
- **CT data are linear in the object.** The log data $-\ln(I/I_0)$ are linear in $\mu$, so the [sinogram](/sinogram/) is the Radon transform of $\mu$ and linear methods such as [filtered back-projection](/filtered-back-projection/) apply. Without the log, the data are not linear in $\mu$.
- **Half-value layer.** In a uniform medium the intensity halves over the length $\ln 2/\mu$. For $\mu = 0.5\ \mathrm{cm}^{-1}$ this is 1.386 cm; for $\mu = 0.2\ \mathrm{cm}^{-1}$ it is 3.466 cm.
- **Noise.** A detector counts photons. If the source sends $N_0$ photons along a ray, the count is close to a [Poisson](/poisson-distribution/) variable with mean $N_0 e^{-p}$. By the delta method, the estimate $-\ln(N/N_0)$ has a standard deviation of about $1/\sqrt{N_0 e^{-p}}$. For $N_0 = 10^4$ and $p = 1.6$ the mean count is 2019 and the standard deviation of the estimate is about 0.022. Rays with large $p$ give few counts and noisy data, and a count of 0 has no log.
- **Emission and attenuation.** In emission tomography the source is inside the body, and each emitted photon is attenuated along its path out. The data are then the [attenuated Radon transform](/attenuated-radon-transform/) of the source.

## Tightness

- **Many energies.** A real X-ray tube emits a spectrum, and $\mu$ depends on the energy. With spectral weights $w_E \ge 0$ that sum to 1, the detector gives $I/I_0 = \sum_E w_E e^{-p_E}$, where $p_E$ is the line integral at energy $E$. Since $\exp$ is convex, Jensen's inequality gives $-\ln(I/I_0) \le \sum_E w_E\,p_E$. The log data grow more slowly than the thickness. For two equal energy weights with $\mu = 0.5$ and $0.2\ \mathrm{cm}^{-1}$, a uniform slab of thickness $L$ gives $-\ln(I/I_0)/L = 0.339, 0.298, 0.264\ \mathrm{cm}^{-1}$ at $L = 1, 5, 10$ cm, while the mean of $\mu$ is 0.35. This is [beam hardening](/beam-hardening/): the low energies are absorbed first and the beam gets harder along the path. It causes cupping and streaks in CT images.
- **Scatter.** The equation counts a scattered photon as removed. If scattered photons still reach the detector, the measured $I$ is too large and $-\ln(I/I_0)$ is too small. In a fog or in the air, scattering into the path adds light, and the radiative transfer equation replaces the law ([participating media](/participating-media/)).
- **Large concentrations.** In chemistry the law that absorbance is proportional to concentration fails at large concentrations, where the molecules interact and the absorption coefficient changes. The theorem then still holds for the actual $\mu$, but $\mu$ is no longer proportional to the concentration.
- **Waves.** The law treats light as rays. When the features of the medium are not large compared with the wavelength, diffraction moves energy off the ray, and the straight-line model fails.

## History

Bouguer stated in 1729 that equal thicknesses of a uniform medium take away equal fractions of the light. Lambert gave the law a mathematical form in his Photometria of 1760. Beer showed in 1852 that the absorption of red light in colored solutions depends on the product of concentration and thickness, which made the law a tool of chemical analysis. In tomography, the law is the reason that the measured data, after a log, are line integrals. Cormack in 1963 and Hounsfield in 1973 used it in this way.

## References
