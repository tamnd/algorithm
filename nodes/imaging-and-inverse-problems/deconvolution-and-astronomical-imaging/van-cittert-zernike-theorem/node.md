---
tag: EMC7GV
kind: theorem
slug: van-cittert-zernike-theorem
name: Van Cittert-Zernike theorem
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: core
summary: "The spatial coherence of light from an incoherent source in the far field is the Fourier transform of the source intensity, the base of interferometric imaging."
history:
  year: 1934
  people: [Pieter Hendrik van Cittert, Frits Zernike]
  note: "Van Cittert (1934) found the correlation of the light at two points lit by an incoherent source; Zernike (1938) defined the degree of coherence and gave the result its usual form."
prereqs: [discrete-fourier-transform, cross-correlation]
see_also: [aperture-synthesis, dirty-image, w-projection, speckle-interferometry, optical-transfer-function, wiener-khinchin-theorem, sampling-theorem, coherent-diffraction-imaging]
sources:
  - paper: doi:10.1016/S0031-8914(34)90026-4
    title: "P. H. van Cittert, Die wahrscheinliche Schwingungsverteilung in einer von einer Lichtquelle direkt oder mittels einer Linse beleuchteten Ebene, Physica 1, 1934"
    locator: "pp. 201 to 210 (the correlation of the light at two points of a plane lit by an incoherent source)"
  - paper: doi:10.1016/S0031-8914(38)80203-2
    title: "F. Zernike, The concept of degree of coherence and its application to optical problems, Physica 5(8), 1938"
    locator: "pp. 785 to 795 (the degree of coherence and its computation from the intensity of the source)"
  - book: isbn:9783319444314
    title: "A. Richard Thompson, James M. Moran and George W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, third edition, Springer, 2017"
    locator: "Chapter 15, Section 15.1, pp. 767 to 776 (the theorem, the mutual coherence of an incoherent source and the assumptions of the derivation); Chapters 2 and 3, pp. 59 to 108 (the response of an interferometer and the Fourier relation between visibility and intensity)"
  - book: isbn:9780521642224
    title: "Max Born and Emil Wolf, Principles of Optics, seventh edition, Cambridge University Press, 1999"
    locator: "the chapter on interference and diffraction with partially coherent light (the Van Cittert-Zernike theorem and its use in stellar interferometry)"
  - book: isbn:9781119009450
    title: "Joseph W. Goodman, Statistical Optics, second edition, Wiley, 2015"
    locator: "the chapter on the coherence of optical waves (the propagation of mutual coherence and the Van Cittert-Zernike theorem)"
---

The Van Cittert-Zernike theorem says that the correlation of the fields at two points, lit by a far source whose parts radiate independently, depends only on the vector between the points, and that it is the Fourier transform of the brightness of the source. In radio astronomy this correlation is the visibility that a pair of antennas measures, so each pair measures one Fourier coefficient of the sky. [Aperture synthesis](/aperture-synthesis/) is the technique that collects many of these coefficients and inverts them; the [dirty image](/dirty-image/) is what the inversion gives when the coefficients are incomplete; [w-projection](/w-projection/) handles the term of the theorem that is not a 2D Fourier transform.

## Statement

**Setting.** Lengths are in units of the wavelength $\lambda$. A direction on the sky is a unit vector $s$, and $s_0$ is a fixed direction, the phase center. The coordinates are chosen so that $s_0 = (0, 0, 1)$ and $s = (l, m, \nu)$ with $\nu = \sqrt{1 - l^2 - m^2}$ on the half of the sky toward $s_0$. Two antennas or two points of an aperture are at $r_1$ and $r_2$, and the baseline is $b = r_1 - r_2 = (u, v, w)$, with $w$ along $s_0$. The visibility is the correlation of the fields with the delay to $s_0$ compensated:

$$V(b) = e^{2\pi i\, b \cdot s_0}\; \mathbb E\big[E(r_1)\, \overline{E(r_2)}\big].$$

**Hypotheses.**

1. *Far field.* Every part of the source is so far away that its field over the array is a plane wave. The field is $E(r) = \int a(s)\, e^{-2\pi i\, s \cdot r}\, d\Omega(s)$, where $a(s)$ is the random complex amplitude of the light from direction $s$.
2. *Quasi-monochromatic light.* The bandwidth is so small that the formula above holds with one wavelength.
3. *Spatial incoherence.* Light from different directions is uncorrelated: $\mathbb E[a(s)\, \overline{a(s')}] = I(s)\, \delta(s - s')$, where $I \ge 0$ is the brightness of the sky. For a finite set of point sources with amplitudes $a_k$, this means $\mathbb E[a_j \overline{a_k}] = I_k$ if $j = k$ and 0 otherwise.
4. *Free propagation.* Nothing between the source and the array scatters the light, and $I = 0$ on the half of the sky away from $s_0$.

**Theorem.** Under hypotheses 1 to 4,

$$V(u, v, w) = \iint_{l^2 + m^2 < 1} \frac{I(l, m)}{\sqrt{1 - l^2 - m^2}}\; e^{-2\pi i \left(u l + v m + w \left(\sqrt{1 - l^2 - m^2} - 1\right)\right)}\, dl\, dm .$$

For point sources of flux $I_k$ at $(l_k, m_k)$ the integral is the sum $\sum_k I_k\, e^{-2\pi i (u l_k + v m_k + w (\nu_k - 1))}$.

**Corollary (the 2D Fourier form).** Let $I'(l, m) = I(l, m) / \sqrt{1 - l^2 - m^2}$, let $S' = \iint I'$, and let $\widehat{I'}(u, v)$ be its 2D Fourier transform $\iint I'(l, m)\, e^{-2\pi i (u l + v m)}\, dl\, dm$. If $w = 0$, then $V(u, v, 0) = \widehat{I'}(u, v)$ exactly. If $I'$ is zero outside the field $l^2 + m^2 \le \rho^2$, then

$$\big|V(u, v, w) - \widehat{I'}(u, v)\big| \le 2\pi |w| \left(1 - \sqrt{1 - \rho^2}\right) S' \approx \pi |w| \rho^2 S' .$$

So for a small field the visibility is the 2D Fourier transform of the sky, as the brief form of the theorem says.

## In plain words

Two antennas listen to the same patch of sky, and the receiver multiplies their signals and averages the product. If every part of the sky shines on its own, without any fixed relation to the other parts, the cross terms between different parts average to zero. Only each part with itself is left. Each part then adds a small wave whose phase depends on its direction and on the separation of the antennas. The sum of these waves over the sky is one Fourier coefficient of the picture of the sky. A pair of antennas far apart sees fine detail, and a pair close together sees coarse structure. Many pairs, at many separations and directions, give many coefficients, and from them a computer can make an image. This is the idea behind radio telescopes made of many dishes.

## Proof

Take first a finite set of point sources with amplitudes $a_k$ from directions $s_k$, so that $E(r) = \sum_k a_k\, e^{-2\pi i\, s_k \cdot r}$ by hypothesis 1. Then

$$E(r_1)\, \overline{E(r_2)} = \sum_j \sum_k a_j\, \overline{a_k}\; e^{-2\pi i (s_j \cdot r_1 - s_k \cdot r_2)} .$$

Take the expectation. By hypothesis 3, the terms with $j \ne k$ have expectation 0, and the terms with $j = k$ have expectation $I_k$. So

$$\mathbb E\big[E(r_1)\, \overline{E(r_2)}\big] = \sum_k I_k\, e^{-2\pi i\, s_k \cdot (r_1 - r_2)} = \sum_k I_k\, e^{-2\pi i\, b \cdot s_k} ,$$

which depends on $r_1$ and $r_2$ only through $b$. Multiply by $e^{2\pi i\, b \cdot s_0}$: $V(b) = \sum_k I_k\, e^{-2\pi i\, b \cdot (s_k - s_0)}$. In the coordinates of the setting, $b \cdot (s_k - s_0) = u l_k + v m_k + w (\nu_k - 1)$, which is the point-source form of the theorem.

For a brightness density the same steps hold with integrals. Write $E(r_1)\overline{E(r_2)}$ as a double integral over $s$ and $s'$, take the expectation inside, and use $\mathbb E[a(s)\overline{a(s')}] = I(s)\, \delta(s - s')$ to do the integral over $s'$. This gives $V(b) = \int I(s)\, e^{-2\pi i\, b \cdot (s - s_0)}\, d\Omega(s)$, over the half of the sky toward $s_0$ by hypothesis 4. On that half, the map $(l, m) \mapsto (l, m, \sqrt{1 - l^2 - m^2})$ covers the sphere, and the element of solid angle is $d\Omega = dl\, dm / \sqrt{1 - l^2 - m^2}$. This gives the formula of the theorem.

For the corollary, $w = 0$ removes the last term of the exponent. For $w \ne 0$, use $|e^{-ix} - 1| \le |x|$ for real $x$:

$$\big|V(u, v, w) - \widehat{I'}(u, v)\big| \le \iint I'(l, m)\, \big|e^{-2\pi i w (\nu - 1)} - 1\big|\, dl\, dm \le 2\pi |w| \iint I'(l, m)\, (1 - \nu)\, dl\, dm .$$

On the field, $1 - \nu \le 1 - \sqrt{1 - \rho^2}$, which gives the bound. Finally $1 - \sqrt{1 - x} = x / (1 + \sqrt{1 - x}) \approx x/2$ for small $x$. $\square$

A check by simulation: two incoherent point sources of flux 1 at $l = 0$ and 0.5 at $l = 0.001$, each with a random phase, uniform on $[0, 2\pi)$, in each of 20000 draws (seed 1). At $b = (250, 0, 0)$ the average of $E(r_1)\overline{E(r_2)}$ was $0.996 - 0.496 i$. The theorem gives $1 + 0.5\, e^{-2\pi i \cdot 0.25} = 1 - 0.5 i$.

## Consequences

- **One baseline, one Fourier coefficient.** With $w$ negligible, a pair of antennas at baseline $(u, v)$ measures $\widehat{I'}(u, v)$. A baseline of length $|b|$ wavelengths responds to structure on angular scales of about $1/|b|$ radians. This is the base of [aperture synthesis](/aperture-synthesis/).
- **Hermitian symmetry.** $I$ is real, so $V(-b) = \overline{V(b)}$. Each baseline gives two samples of the Fourier plane, at $b$ and at $-b$.
- **The total flux is at the origin.** $V(0) = S'$, but two antennas cannot be at the same place, so an interferometer does not measure $V$ near $b = 0$. Smooth emission on large scales is lost unless a single dish adds the short spacings.
- **The modulus gives the size.** The visibility of two point sources is $1 + F e^{-2\pi i u l_0}$ for fluxes 1 and $F$ at separation $l_0$. With $F = 0.5$ and $l_0 = 0.001$ radian, $|V|$ is 1.5 at $u = 0$, 1.118 at $u = 250$ (with phase $-0.4636$), 0.5 at $u = 500$ and 1.5 again at $u = 1000$. The period $1/l_0$ in $u$ gives the separation, and the depth of the dip gives the flux ratio. A stellar interferometer that measures only $|V|$ uses this to measure the size of a star.
- **The image is an inverse problem.** Finitely many baselines give finitely many samples. Their inverse Fourier transform is the [dirty image](/dirty-image/), the sky convolved with the dirty beam, and CLEAN and the other deconvolution methods start from it.
- **The w term.** For a field of radius $\rho$, the phase $2\pi w (\nu - 1)$ is about $\pi w \rho^2$. At $w = 1000$ it is $-0.3142$ radian at $l = 0.01$, $-7.859$ at $l = 0.05$ and $-31.49$ at $l = 0.1$. The first is small, and the last is many turns. Wide fields need [w-projection](/w-projection/) or a related method.

## Tightness

Each hypothesis is needed, and each fails in practice in a known way.

- **Coherent sources.** Take two point sources with the same amplitude $a$, so the light from them is fully correlated. Then $\mathbb E[|E(r)|^2] = 2\, \mathbb E|a|^2\, (1 + \cos 2\pi (s_1 - s_2) \cdot r)$, which changes with the position $r$. The correlation at two points is not a function of $b$ alone, and the theorem fails. The cross terms that hypothesis 3 removes are exactly these. Thompson, Moran and Swenson discuss the response to a coherent source in Section 15.2.
- **Near field.** For a source at a finite distance, the waves are not plane over the array, and the correlation gets an extra phase that depends on the two points. The far-field form needs the distance to be large compared with the square of the array size in wavelengths.
- **Wide bandwidth.** The formula holds at one wavelength. Over a band, $V$ is the average of the formula over the wavelengths, and point sources far from $s_0$ are smeared in the radial direction. The usual remedy is to split the band into narrow channels.
- **Wide fields and non-coplanar baselines.** The bound of the corollary is sharp for small fields: for a point source at the edge of the field and $\pi |w| \rho^2$ small, the error is about $\pi |w| \rho^2 S'$. When it is not small, $V$ is not a 2D Fourier transform.
- **Scattering.** Turbulence in the ionosphere, the troposphere or the interstellar medium adds random phases that differ between antennas. For optical telescopes the atmosphere does the same, which is why [speckle interferometry](/speckle-interferometry/) works with short exposures.
- **The antenna pattern.** Real antennas are not isotropic. The measured visibility is the transform of $A(s)\, I(s)$, where $A$ is the primary beam of the antennas. This changes the sky that is measured, not the theorem.

## History

Van Cittert (1934) computed the correlation of the light at two points lit by an incoherent source, and Zernike (1938) defined the degree of coherence and gave the result its usual form. The theorem came from optics. Thompson, Moran and Swenson note that it was not widely known among radio astronomers until the textbook of Born and Wolf appeared in 1959. Ryle and Hewish (1960) described the synthesis of a large radio telescope from a few small ones, which rests on this relation, and it remains the model behind every radio interferometer and every optical long-baseline interferometer.

## References
