---
tag: F2PT3X
kind: concept
slug: spectral-rendering
name: Spectral rendering
aliases:
- wavelength sampling
- hero wavelength sampling
area: graphics-and-signals/ray-tracing
level: advanced
summary: Simulates light as radiance per wavelength, not as RGB triples, and converts to color only at the pixel. It handles dispersion, metamerism and spectral absorption, which RGB gets wrong.
prereqs: [color-spaces, monte-carlo-integration]
see_also: [snells-law, fresnel-equations, path-tracing, multiple-importance-sampling, stratified-sampling, importance-sampling, participating-media, gamma-correction]
sources:
  - paper: doi:10.1111/cgf.12419
    title: Alexander Wilkie, Sehera Nawaz, Marc Droske, Andrea Weidlich and Johannes Hanika, Hero wavelength spectral sampling, Computer Graphics Forum 33(4), Eurographics Symposium on Rendering 2014
    locator: the hero wavelength with equally spaced companions, the combination by multiple importance sampling, and the handling of dispersion
  - url: https://jcgt.org/published/0002/02/01/
    title: Chris Wyman, Peter-Pike Sloan and Peter Shirley, Simple analytic approximations to the CIE XYZ color matching functions, Journal of Computer Graphics Techniques 2(2), 2013
    locator: the multi-lobe piecewise Gaussian fit of the CIE 1931 functions used in the examples
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 5, Color and Radiometry (spectral representation, XYZ color and the conversion from RGB to spectra)
  - book: isbn:9780471399186
    title: Günter Wyszecki and W. S. Stiles, Color Science, Concepts and Methods, Quantitative Data and Formulae, second edition, Wiley, 1982, reprinted in the Wiley Classics Library, 2000
    locator: the CIE 1931 standard observer and the colorimetry of metamers
---

Spectral rendering simulates light as a function of wavelength. A renderer that works in RGB carries three numbers per ray and multiplies them at every bounce; a spectral renderer carries the radiance $L(\lambda)$ at one or a few wavelengths $\lambda$, applies the materials and lights at those wavelengths, and turns the result into a color only at the pixel, through the CIE color matching functions. The difference shows when the physics depends on the wavelength: a prism or a diamond splits white light by dispersion, two paints that match under daylight differ under a fluorescent lamp, and light that passes deep through colored water or glass changes its hue. In a [path tracer](/path-tracing/) the wavelength is one more dimension of the [Monte Carlo](/monte-carlo-integration/) integral, and sampling one wavelength per path gives color noise. Hero wavelength sampling (Wilkie et al. 2014) traces several wavelengths along one path and combines them by [multiple importance sampling](/multiple-importance-sampling/).

## In plain words

White light is a mix of all the colors of the rainbow. Each color is a wave of a different length. A normal renderer squeezes this mix into just three numbers, red, green and blue, as if light were made of three colors only.

That shortcut is fine most of the time, but it misses some things. Glass bends blue light a bit more than red, so a prism spreads white light into a rainbow. Two shirts can look the same in a shop and different in the sun. Light that goes through deep water loses its red first.

A spectral renderer keeps the full mix. Each ray picks one or a few wavelengths at random and follows them through the scene. At the end, the camera turns the light that it collected into a color, much as the eye does.

## The idea

**Radiance per wavelength.** At each wavelength, light transport is the same as in gray: the [rendering equation](/rendering-equation/) holds for $L(x, \omega, \lambda)$ with the BSDF, the emission and the coefficients of the media at $\lambda$, as long as no material moves light from one wavelength to another (fluorescence does). The color of a pixel is the CIE XYZ triple

$$X = \int L(\lambda)\,\bar x(\lambda)\,d\lambda, \quad Y = \int L(\lambda)\,\bar y(\lambda)\,d\lambda, \quad Z = \int L(\lambda)\,\bar z(\lambda)\,d\lambda,$$

over the visible range, about 360 to 830 nm, where $\bar x$, $\bar y$ and $\bar z$ are the color matching functions of the CIE 1931 standard observer. A display needs a further linear map to RGB and a transfer curve, which belong to [color spaces](/color-spaces/) and [gamma correction](/gamma-correction/).

**Why three numbers are not enough.** The XYZ map is linear, so the color of a sum of spectra is the sum of their colors. Rendering multiplies spectra, and a product does not commute with the projection: in general the color of $L(\lambda)\,\rho(\lambda)$ is not the product of the colors of $L$ and $\rho$. RGB rendering is exact only when one of the factors is flat or when the spectra happen to fit the three primaries. Three effects need the spectrum:

- **Dispersion.** The index of refraction depends on $\lambda$. Cauchy's formula $n(\lambda) = A + B/\lambda^2$ describes glass in the visible range. By [Snell's law](/snells-law/), each wavelength leaves a refracting surface in its own direction, and so does each [Fresnel](/fresnel-equations/) weight.
- **Metamerism.** Two different spectra with the same XYZ under one light are metamers. Under another light their colors differ. RGB rendering, which knows only their common triple, cannot tell them apart.
- **Spectral absorption.** In a medium with the absorption coefficient $\sigma_a(\lambda)$, the transmittance over a distance $d$ is $e^{-\sigma_a(\lambda) d}$, a nonlinear function of $\sigma_a$. An average of the exponentials is not the exponential of the average, so per-channel coefficients give the wrong color for long paths in [participating media](/participating-media/).

**Sampling wavelengths.** A Monte Carlo renderer draws a wavelength $\lambda$ with the density $p(\lambda)$, traces a path at $\lambda$, and adds $L(\lambda)\,\bar x(\lambda) / p(\lambda)$ and the same for $\bar y$ and $\bar z$ to the pixel. This is unbiased, but a single wavelength per path is noisy: each sample adds a pure spectral color, and the pixel converges to white only through the average. [Stratified sampling](/stratified-sampling/) of $\lambda$ over the samples of a pixel and [importance sampling](/importance-sampling/) with a density close to the sum of the color matching functions both help.

**Hero wavelength sampling.** Wilkie et al. (2014) draw one hero wavelength $\lambda_h$ uniformly on $[\lambda_{\min}, \lambda_{\max})$ and add $C - 1$ companions

$$\lambda_j = \lambda_{\min} + \big( (\lambda_h - \lambda_{\min} + j\,\Delta / C) \bmod \Delta \big), \qquad j = 1, \dots, C - 1, \quad \Delta = \lambda_{\max} - \lambda_{\min}.$$

The path is sampled at the hero wavelength and evaluated at all $C$ wavelengths, usually $C = 4$ to fill a SIMD register. The density of the path is different at each wavelength, so the $C$ estimates are combined by the balance heuristic of multiple importance sampling: the path sampled at $\lambda_h$ contributes at $\lambda_j$ with the weight $p_j / \sum_k p_k$, where $p_k$ is the density of the same path had it been sampled at $\lambda_k$. When the path does not depend on the wavelength all densities are equal and the weights are $1/C$; the $C$ wavelengths are then a rotated stratified sample of the spectrum. At a smooth dispersive interface the refracted direction is right for the hero wavelength only, the densities of the companions are zero, and the weights drop the companions from the rest of the path.

**Spectra from RGB inputs.** Textures and colors chosen by artists are RGB. A spectral renderer turns them into smooth spectra with the same color, for example by Smits' method (1999) or by the low-dimensional sigmoid polynomials of Jakob and Hanika (2019), so that a reflectance stays between 0 and 1 at every wavelength.

## Examples

**Dispersion in crown glass.** With $A = 1.5046$ and $B = 0.00420\ \mu\mathrm{m}^2$, Cauchy's formula gives for BK7 the indices $1.5309$ at 400 nm, $1.5168$ at 587.6 nm and $1.5132$ at 700 nm, and the Abbe number $(n_d - 1)/(n_F - n_C) = 64.4$; the catalog values are $n_d = 1.5168$ and about 64.2. Light that enters at $45°$ from air is refracted to $27.51°$ at 400 nm and to $27.86°$ at 700 nm, a spread of $0.35°$. A prism with an apex angle of $60°$ has the minimum deviations $39.89°$ and $38.33°$, a spread of $1.56°$ that makes a visible rainbow on a wall a meter away, about 2.7 cm wide.

**A metameric pair.** Take the flat reflectance $\rho_a(\lambda) = 0.5$, and let $\rho_b = 0.5 + \varepsilon\,m(\lambda)$, where $m$ is a wavy function made orthogonal to $\bar x$, $\bar y$ and $\bar z$ and scaled so that $\rho_b$ stays between 0.13 and 0.9. Under the equal energy light both have the normalized XYZ $(0.499, 0.500, 0.500)$, to nine digits. Under a lamp with three narrow lines at 436, 546 and 611 nm, normalized so that white has $Y = 1$, $\rho_a$ gives $(0.530, 0.500, 0.522)$ and $\rho_b$ gives $(0.434, 0.371, 0.599)$: one stays gray, the other turns dark and bluish. An RGB renderer stores the same triple for both and shows them the same under every light.

**The product error.** A green light, a Gaussian spectrum at 520 nm with a width of 30 nm, falls on a surface that reflects a Gaussian band at 600 nm with a width of 20 nm. The spectral product is a dim yellow-orange with the luminance $Y = 0.029$, on the scale where the flat spectrum of value 1 has $Y = 1$. The product of the two linear sRGB triples has $Y = 0.010$ and a negative red channel, because the green of the light lies outside the sRGB gamut. For broad spectra the error is smaller: a broad orange reflectance under a broad green light gives $Y = 0.423$ by the spectrum and $0.402$ by RGB, 5 percent low.

**Absorption.** Let half of the energy of a light be at a wavelength with $\sigma_a = 0$ and half at a wavelength with $\sigma_a = 2$ per meter, both in one RGB channel. After 1 m of the medium, the spectral transmittance is $0.5 + 0.5\,e^{-2} = 0.568$, while a channel with the average coefficient 1 gives $e^{-1} = 0.368$.

**Hero wavelengths against one wavelength.** To estimate $Y$ of a spectrum with one uniform wavelength per sample, against one hero wavelength with three companions per sample, the relative standard deviation per sample is $1.48$ against $0.124$ for the flat spectrum, $2.17$ against $0.66$ for the green Gaussian above, and $2.51$ against $0.91$ for the narrow orange band. Per sample, the variance falls by factors of 141, 11 and 8, for four times the shading work and one path.

## Where it is used

- Production renderers for film, such as Weta's Manuka, and physically based research renderers such as PBRT and Mitsuba, render spectrally, with a few wavelengths per path; Manuka was built around hero wavelength sampling.
- Prediction and lighting design need it: the color of a car paint under street lamps, of a gem, or of a material under a new LED spectrum.
- [Path tracing](/path-tracing/) of dispersive glass, thin films and soap bubbles, and of [participating media](/participating-media/) such as deep water, uses wavelength sampling.
- The colors of metals follow from their complex index of refraction per wavelength in the [Fresnel equations](/fresnel-equations/); Cook and Torrance (1982) computed metal colors in this way.

### History

Hall and Greenberg (1983) rendered with spectral samples in a testbed for realistic image synthesis, and Meyer (1988) studied which wavelengths to choose. Peercy (1993) projected spectra onto linear bases to make full spectral rendering cheaper. Monte Carlo renderers turned the wavelength into a random variable, which made dispersion simple but added color noise, until Wilkie et al. (2014) introduced hero wavelength sampling. Smits (1999) and Jakob and Hanika (2019) gave the conversions from RGB to spectra that let a spectral renderer read RGB assets.

## References
