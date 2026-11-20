---
tag: E4W3EQ
kind: definition
slug: optical-transfer-function
name: Optical transfer function
aliases:
- OTF
- modulation transfer function
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: core
summary: "The Fourier transform of the point spread function, normalized to 1 at zero frequency. Its modulus scales the contrast of each sine pattern and its phase shifts the pattern."
prereqs: [point-spread-function, convolution-theorem, autocorrelation]
see_also: [abbe-diffraction-limit, rayleigh-criterion, discrete-fourier-transform, image-deblurring, wiener-filter, gibson-lanni-model, phase-diversity, sampling-theorem]
sources:
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, 3rd edition, Roberts and Company, 2005
    locator: Chapter 6, sections 6.2.1 (the amplitude transfer function), 6.3.1 to 6.3.4 (the OTF, its general properties, the OTF as the normalized autocorrelation of the pupil, and the circular pupil) and 6.4 (aberrations and the focusing error)
  - paper: doi:10.1098/rspa.1955.0158
    title: H. H. Hopkins, The frequency response of a defocused optical system, Proceedings of the Royal Society of London A 231(1184), 1955
    locator: pages 91 to 103 (the OTF of a defocused circular pupil, with its zeros and negative lobes)
  - book: isbn:9780898716184
    title: Per Christian Hansen, James G. Nagy and Dianne P. O'Leary, Deblurring Images, Matrices, Spectra, and Filtering, SIAM, 2006
    locator: the chapters on the blur model and on structured matrices (a periodic blur is diagonalized by the DFT, and its eigenvalues are the DFT of the PSF)
---

The optical transfer function (OTF) of an imaging system is the Fourier transform $H$ of its [point spread function](/point-spread-function/) $h$, scaled so that $H(0) = 1$. The PSF page describes the blur in space, as the image of one point. The OTF describes the same blur by frequency: a sine pattern of frequency $\xi$ in the object comes out as a sine pattern of the same frequency, with its contrast multiplied by $|H(\xi)|$ and its position shifted by the phase $\arg H(\xi)$. The modulus $|H|$ is called the modulation transfer function (MTF) and the phase is called the phase transfer function (PTF). By the [convolution theorem](/convolution-theorem/), blur by $h$ is multiplication by $H$, so the OTF of a chain of blurs is the product of their OTFs. For an incoherent system in scalar diffraction theory, the OTF is the normalized [autocorrelation](/autocorrelation/) of the pupil, and it is zero above the frequency $2\,\mathrm{NA}/\lambda$, which is the [Abbe diffraction limit](/abbe-diffraction-limit/).

## Definition

**Setting.** The object is an intensity $o(x) \ge 0$ on the plane, $x \in \mathbb{R}^2$. The light is incoherent, so intensities add. The system is shift invariant (isoplanatic): the image of a point at $x_0$ is the same pattern moved to $x_0$, after the magnification is scaled out. Then the image is the convolution

$$i(x) = (h \ast o)(x) = \int h(x - x')\, o(x')\, dx',$$

with a PSF $h \ge 0$ that is integrable and normalized, $\int h = 1$. The Fourier transform uses ordinary frequency, $\hat f(\xi) = \int f(x) e^{-2\pi i x \cdot \xi} dx$, with $\xi$ in cycles per unit length.

**Definition.** The optical transfer function is $H = \hat h$:

$$H(\xi) = \int h(x)\, e^{-2\pi i x \cdot \xi}\, dx.$$

The modulation transfer function is $|H(\xi)|$ and the phase transfer function is $\arg H(\xi)$. Some authors define the OTF as $\hat h / \hat h(0)$ for a PSF that is not normalized. With $\int h = 1$ the two agree.

**Properties.** Each one follows in one line from $h \ge 0$, $h$ real and $\int h = 1$.

1. $H(0) = \int h = 1$. A uniform object stays uniform with the same brightness.
2. $|H(\xi)| \le 1$ for every $\xi$. Proof: $|H(\xi)| \le \int |h(x)|\,|e^{-2\pi i x\cdot\xi}|\, dx = \int h = 1$. So no frequency gains contrast.
3. $H(-\xi) = \overline{H(\xi)}$, because $h$ is real. So the MTF is even and the PTF is odd. If $h$ is also symmetric, $h(-x) = h(x)$, then $H$ is real, and the PTF is $0$ or $\pi$.
4. Cascade: if $h = h_1 \ast h_2$ (a lens followed by a detector pixel, or a telescope followed by the air), then $H = H_1 H_2$. This is the convolution theorem.
5. Sine response: let $o(x) = 1 + m \cos(2\pi \xi_0 \cdot x + \varphi)$ with contrast $0 \le m \le 1$. Then
$$i(x) = 1 + m\,|H(\xi_0)| \cos\big(2\pi \xi_0 \cdot x + \varphi + \arg H(\xi_0)\big).$$
Proof: write the cosine as two complex exponentials. Convolution with $h$ multiplies $e^{2\pi i \xi_0\cdot x}$ by $H(\xi_0)$ and $e^{-2\pi i \xi_0\cdot x}$ by $H(-\xi_0) = \overline{H(\xi_0)}$, and the constant by $H(0) = 1$. The sum of the two terms is the cosine above. So the image contrast at $\xi_0$ is $m\,|H(\xi_0)|$, which is the reason for the name.

**The OTF from the pupil.** In scalar Fraunhofer diffraction theory, write the pupil of the system as a function $P(\eta)$ of frequency (the coherent transfer function). For an aberration-free system with numerical aperture $\mathrm{NA}$ in light of wavelength $\lambda$, $P(\eta) = 1$ for $|\eta| \le \mathrm{NA}/\lambda$ and $0$ elsewhere; aberrations multiply it by $e^{i k W(\eta)}$ with the wavefront error $W$ and $k = 2\pi/\lambda$. The amplitude PSF is the inverse Fourier transform $a = \check P$, and the intensity PSF is $|a|^2 = a\,\bar a$ scaled to unit integral. The Fourier transform of a product is the convolution of the transforms, and the transform of $\bar a$ is $\overline{P(-\eta)}$. This gives (Goodman, section 6.3.1)

$$H(\xi) = \frac{\int P(\eta + \xi/2)\, \overline{P(\eta - \xi/2)}\, d\eta}{\int |P(\eta)|^2\, d\eta}.$$

So the incoherent OTF is the autocorrelation of the pupil, divided by its value at $0$. Two shifted copies of a disk of radius $\mathrm{NA}/\lambda$ overlap only if the shift is less than $2\,\mathrm{NA}/\lambda$. So $H(\xi) = 0$ for $|\xi| \ge 2\,\mathrm{NA}/\lambda$. The coherent transfer function $P$ itself cuts off at $\mathrm{NA}/\lambda$. For the clear circular pupil the overlap area gives, with $\rho = |\xi|$ and $\rho_c = 2\,\mathrm{NA}/\lambda$,

$$H(\rho) = \frac{2}{\pi}\left(\arccos\frac{\rho}{\rho_c} - \frac{\rho}{\rho_c}\sqrt{1 - \Big(\frac{\rho}{\rho_c}\Big)^2}\,\right), \qquad 0 \le \rho \le \rho_c.$$

**Aberrations lower the MTF.** Let $P = \chi_D\, e^{ikW}$ with $\chi_D$ the indicator of the clear pupil $D$. In the formula above the numerator is an integral of $e^{ik(W(\eta + \xi/2) - W(\eta - \xi/2))}$ over the overlap of the two shifted copies of $D$. The modulus of the integral is at most the area of the overlap, which is the numerator for $W = 0$. The denominator does not depend on $W$. So $|H_W(\xi)| \le H_0(\xi)$ at every frequency: no aberration raises the MTF above that of the aberration-free system (Goodman, section 6.4).

**Discrete OTF.** On a periodic grid of $n$ samples, the PSF is stored with its center at index $0$, so that $h_j$ for $j > n/2$ holds the value at $j - n$. Then a delta PSF ($h_0 = 1$, all other $h_j = 0$) gives the identity, and the OTF is the DFT

$$H_k = \sum_{j=0}^{n-1} h_j\, e^{-2\pi i jk/n},$$

where index $k$ stands for frequency $k$ for $k < n/2$ and $k - n$ otherwise. Periodic convolution $y_i = \sum_j h_j x_{(i - j) \bmod n}$ becomes $\hat y_k = H_k \hat x_k$ under the [discrete Fourier transform](/discrete-fourier-transform/). So the periodic blur matrix is diagonalized by the DFT, and its eigenvalues are the $H_k$ (Hansen, Nagy and O'Leary). This is the operator that the deconvolution pages of this area invert. With a zero or a reflexive boundary the matrix is not circulant, and the $H_k$ are only an approximation of its spectrum.

## Examples and non-examples

**A three-point blur.** Take $n = 8$ and the PSF $(1/4, 1/2, 1/4)$ centered at index 0, that is $h_0 = 1/2$, $h_1 = h_7 = 1/4$. Then $H_k = \tfrac12 + \tfrac12 \cos(2\pi k/8) = \cos^2(\pi k/8)$. The values for $k = 0, 1, 2, 3, 4$ are $1$, $0.8536$, $0.5$, $0.1464$ and $0$. The OTF is real and nonnegative because the PSF is symmetric with a large center. At $k = 4$ the pattern $(1, -1, 1, -1, \dots)$ is blurred to $\tfrac12 - \tfrac14 - \tfrac14 = 0$ at every pixel, so this frequency is lost and no deconvolution can bring it back.

**A box blur, with contrast reversal.** Take $n = 16$ and a box of width 5, $h_j = 1/5$ for $j \in \{-2, \dots, 2\}$. Then $H_k = \tfrac15\big(1 + 2\cos(2\pi k/16) + 2\cos(4\pi k/16)\big)$, which gives $1$, $0.8524$, $0.4828$, $0.0702$, $-0.2$, $-0.2359$, $-0.0828$, $0.1133$ and $0.2$ for $k = 0, \dots, 8$. At $k = 4$ the OTF is $-1/5$: the MTF is $0.2$ and the PTF is $\pi$. A sine pattern with a period of 4 pixels comes out with a fifth of its contrast and with its bright and dark bars swapped. A defocused lens does the same thing, because its PSF is close to a uniform disk; Hopkins (1955) computed the defocused OTF of a circular pupil with its zeros and negative lobes.

**A diffraction-limited microscope.** Take $\lambda = 500$ nm and an oil objective with $\mathrm{NA} = 1.4$. The cutoff is $\rho_c = 2 \cdot 1.4 / 0.5\ \mu\mathrm{m} = 5.6$ cycles per micrometer, a period of $178.6$ nm. The circular pupil formula gives $H = 0.6850$ at $\rho_c/4$, $0.3910$ at $\rho_c/2$ and $0.1443$ at $3\rho_c/4$. A grating with a period of 200 nm has $\rho = 5$ cycles per micrometer, so $\rho/\rho_c = 0.8929$ and $H = 0.0414$: it is imaged with about 4 percent of its contrast. A grating with a period of 170 nm is above the cutoff and is imaged as a uniform field.

**A Gaussian PSF.** The model $h(x) = (2\pi\sigma^2)^{-1} e^{-|x|^2/(2\sigma^2)}$ has $H(\xi) = e^{-2\pi^2\sigma^2|\xi|^2}$. It is positive at every frequency, so it has no cutoff. It is a convenient fit to the center of an Airy pattern, not a result of diffraction, and its OTF is wrong at high frequencies.

**Non-example: a shift-variant system.** If the PSF changes across the field, as with field-dependent aberrations or with depth in a thick specimen (see the [Gibson-Lanni model](/gibson-lanni-model/)), the image is not a convolution, and there is no single OTF. One uses a local OTF in each region where the PSF is nearly constant (an isoplanatic patch).

**Non-example: coherent imaging.** With coherent light the amplitudes add, not the intensities, so the image intensity is not a linear function of the object intensity. The pupil $P$ is then the transfer function of the amplitude, and the formula $\hat i = H \hat o$ does not hold for intensities. Two coherent points in phase at the Rayleigh distance show no dip between them (see [Rayleigh criterion](/rayleigh-criterion/)).

**Non-example: the MTF alone does not fix the PSF.** The PSFs $h(x)$, $h(-x)$ and $h(x - x_0)$ all have the same MTF. Their OTFs differ only in the phase. Measurement of the MTF with sine targets therefore loses the asymmetry of a PSF with coma, and blind methods such as [phase diversity](/phase-diversity/) need extra data to find the phase.

## Related definitions

- [Point spread function](/point-spread-function/): the image of a point. The OTF is its Fourier transform, normalized to $1$ at $\xi = 0$.
- Coherent transfer function: the pupil $P$ as a function of frequency. It acts on amplitudes and cuts off at $\mathrm{NA}/\lambda$, half the incoherent cutoff.
- [Abbe diffraction limit](/abbe-diffraction-limit/): the statement that the incoherent OTF of an aberration-free system is zero for $|\xi| \ge 2\,\mathrm{NA}/\lambda$.
- [Rayleigh criterion](/rayleigh-criterion/): a convention for the smallest distance at which two points look separate. It is a statement about the PSF, not about the OTF.
- [Sampling theorem](/sampling-theorem/): an image with an OTF that is zero above $\rho_c$ is band-limited, so a pixel pitch of $1/(2\rho_c) = \lambda/(4\,\mathrm{NA})$ in the object plane samples it without aliasing.
- [Wiener filter](/wiener-filter/) and [image deblurring](/image-deblurring/): deconvolution divides by $H$ where $|H|$ is large compared with the noise and damps the frequencies where it is small or zero.

## References
