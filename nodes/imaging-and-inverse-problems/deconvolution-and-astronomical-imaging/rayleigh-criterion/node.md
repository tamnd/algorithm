---
tag: 39DRNN
kind: definition
slug: rayleigh-criterion
name: Rayleigh criterion
aliases:
- Rayleigh resolution limit
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: intro
summary: "A convention that calls two equal incoherent points just resolved when the peak of one Airy pattern falls on the first zero of the other, a distance of 0.61 lambda/NA."
prereqs: [point-spread-function, optical-transfer-function]
see_also: [abbe-diffraction-limit, localization-precision-formula, single-molecule-localization, super-resolution, sampling-theorem, image-deblurring, hogbom-clean, speckle-interferometry]
sources:
  - paper: doi:10.1080/14786447908639684
    title: Lord Rayleigh, Investigations in optics, with special reference to the spectroscope, Philosophical Magazine, Series 5, 8(49), 1879
    locator: pages 261 to 274 (the rule that two lines are just resolved when the maximum of one falls on the first minimum of the other)
  - paper: doi:10.1086/142271
    title: C. M. Sparrow, On spectroscopic resolving power, The Astrophysical Journal 44, 1916
    locator: the article from page 76 (the separation at which the dip between two lines just disappears)
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, 3rd edition, Roberts and Company, 2005
    locator: section 4.4.2 (the Fraunhofer pattern of a circular aperture) and section 6.5.2 (two-point resolution)
---

The Rayleigh criterion is a convention for the smallest distance at which an optical system shows two points of light as two. It says that two incoherent point sources of equal brightness are *just resolved* when the center of the Airy pattern of one falls on the first dark ring of the other. For a diffraction-limited system with a circular pupil this distance is $0.6098\,\lambda/\mathrm{NA}$, written $0.61\,\lambda/\mathrm{NA}$, in the object plane of a microscope, and $1.22\,\lambda/D$ in angle for a telescope of aperture diameter $D$. It is a statement about the [point spread function](/point-spread-function/), not a theorem: at the Rayleigh distance the sum of the two patterns has a dip of 26.5 percent at the midpoint, and an observer who expects two points sees two. The [Abbe diffraction limit](/abbe-diffraction-limit/) is a different statement, a frequency cutoff of the [optical transfer function](/optical-transfer-function/) that is proved in the scalar model. Points closer than the Rayleigh distance can still be told apart and located when the PSF is known and the photon count is high; see the [localization precision formula](/localization-precision-formula/).

## Definition

**The Airy pattern.** Take an aberration-free system with a clear circular pupil, numerical aperture $\mathrm{NA}$ and wavelength $\lambda$, in scalar Fraunhofer theory (Goodman, section 4.4.2). The intensity PSF, scaled to $1$ at its center, is

$$I(v) = \left(\frac{2 J_1(v)}{v}\right)^2, \qquad v = \frac{2\pi\,\mathrm{NA}\, r}{\lambda},$$

where $r$ is the distance from the image of the point, measured in the object plane, and $J_1$ is the Bessel function of the first kind of order one. $I$ has its maximum $1$ at $v = 0$, and its first zero at the first positive zero of $J_1$, $v_1 = 3.83171$. For a telescope with an aperture of diameter $D$, replace $\mathrm{NA}\, r$ by $(D/2)\sin\theta$ for the angle $\theta$ from the axis.

**Definition.** Two incoherent point sources of equal brightness, imaged by this system, are *resolved in the sense of Rayleigh* if their distance is at least

$$d_R = \frac{v_1}{2\pi}\,\frac{\lambda}{\mathrm{NA}} = 0.6098\,\frac{\lambda}{\mathrm{NA}},$$

the distance at which the maximum of one pattern lies on the first zero of the other. In angle, $\sin\theta_R = 1.2197\,\lambda/D$, and $\theta_R \approx 1.22\,\lambda/D$ for small angles.

**What the image looks like at $d_R$.** Incoherent intensities add. Put the sources at $v = \pm v_1/2$ on a line. At each source the sum is $I(0) + I(v_1) = 1 + 0 = 1$. At the midpoint it is $2\,I(v_1/2) = 2\,I(1.91585) = 0.7350$. So the profile along the line has two peaks with a dip of $1 - 0.7350 = 26.5$ percent between them. The maxima of the sum are at the two sources, because each pattern has zero slope at its own center and at its first zero. The check fits in a few lines of Python:

```python
from math import factorial, pi

def j1(x):
    return sum((-1) ** k * (x / 2) ** (2 * k + 1) / (factorial(k) * factorial(k + 1)) for k in range(40))

def airy(v):
    return 1.0 if v == 0 else (2 * j1(v) / v) ** 2

lo, hi = 3.0, 4.5                      # bisection for the first zero of J1
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if j1(mid) > 0 else (lo, mid)
z = (lo + hi) / 2
print(round(z, 5), round(z / (2 * pi), 4))   # 3.83171 0.6098
print(round(2 * airy(z / 2), 4))             # 0.735
print(round(0.61 * 500 / 1.4, 1))            # 217.9
```

**The criterion is a convention.** Rayleigh chose the first zero because it is easy to compute and because the dip it gives is easy to see. No step of the definition is a limit on what can be measured. Other conventions answer the same question with other numbers, listed below.

## Examples and non-examples

**A microscope.** With $\lambda = 500$ nm and an oil objective with $\mathrm{NA} = 1.4$, the Rayleigh distance is $0.61 \cdot 500 / 1.4 = 217.9$ nm ($217.8$ nm with the factor $0.6098$). The Abbe period for the same system is $178.6$ nm.

**A telescope.** The Hubble Space Telescope has a mirror of diameter $D = 2.4$ m. At $\lambda = 500$ nm, $\theta_R = 1.2197 \cdot 500 \cdot 10^{-9} / 2.4 = 2.54 \cdot 10^{-7}$ rad, which is $0.052$ arcseconds. On the ground the air blurs stars to about one arcsecond, so the criterion of the aperture does not apply; that is the problem that [speckle interferometry](/speckle-interferometry/) and adaptive optics address.

**Rayleigh's own case, two slits.** For a spectroscope with a rectangular aperture the pattern of one spectral line is $\mathrm{sinc}^2$, $I(u) = (\sin \pi u / \pi u)^2$, with its first zero at $u = 1$. At a distance of $1$ the midpoint of the sum is $2\, I(1/2) = 2 \cdot (2/\pi)^2 = 8/\pi^2 = 0.8106$. So the same rule gives a dip of only 19 percent for lines, against 26.5 percent for the Airy pattern. The rule fixes a geometry, not a contrast.

**Other conventions.**
- Sparrow (1916): the smallest distance at which the sum still has a dip, that is, where its second derivative at the midpoint is zero. For the Airy pattern this is $v = 2.9756$, a distance of $0.4736\,\lambda/\mathrm{NA}$.
- Full width at half maximum of the Airy pattern: $I(v) = 1/2$ at $v = 1.6163$, so the FWHM is $0.5145\,\lambda/\mathrm{NA}$.
- The Abbe period $\lambda/(2\,\mathrm{NA}) = 0.5\,\lambda/\mathrm{NA}$ is not a two-point rule but the cutoff of the OTF.
All four numbers lie between $0.47$ and $0.61$ times $\lambda/\mathrm{NA}$. They answer different questions, and none of them is a measured property of a real system.

**Non-example: coherent sources.** If the two points are coherent and in phase, the amplitudes add: the amplitude PSF is $2J_1(v)/v$, and the midpoint intensity is $(2 \cdot 0.6062)^2 = 1.4701$ against $1$ at the sources. There is no dip, so two coherent points in phase at the Rayleigh distance look like one. If they are in antiphase, the midpoint is dark and they look separate at any distance. The criterion assumes incoherent light.

**Non-example: unequal sources and noise.** A faint star next to a bright one has no visible dip at $d_R$, and in a noisy image a 26.5 percent dip may not be visible. In the other direction, with a known PSF and a high photon count, a fit of a two-point model can separate and locate two points well inside $d_R$; the error of the fit grows as the distance shrinks, and the [localization precision formula](/localization-precision-formula/) gives it for one point. So the Rayleigh distance is a rule of thumb for direct viewing, not a bound on estimation.

**Non-example: aberrations.** With aberrations the PSF is not an Airy pattern, the first zero moves or disappears, and the definition does not apply as written. One then uses the FWHM or the Sparrow rule on the measured PSF.

## Related definitions

- [Abbe diffraction limit](/abbe-diffraction-limit/): the cutoff $2\,\mathrm{NA}/\lambda$ of the incoherent OTF, a theorem in the scalar model.
- [Optical transfer function](/optical-transfer-function/): the Fourier transform of the PSF. The dip at $d_R$ comes from the OTF near the cutoff.
- [Point spread function](/point-spread-function/): the Airy pattern is the PSF of the clear circular pupil.
- [Localization precision formula](/localization-precision-formula/) and [single-molecule localization](/single-molecule-localization/): how well one point can be located, which is not limited by $d_R$.
- [Super-resolution](/super-resolution/): methods that recover detail below the diffraction scale from several images or from prior knowledge.

## References
