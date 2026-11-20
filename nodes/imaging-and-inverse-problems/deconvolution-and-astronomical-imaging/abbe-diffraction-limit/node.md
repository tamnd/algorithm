---
tag: GYMS6K
kind: theorem
slug: abbe-diffraction-limit
name: Abbe diffraction limit
aliases:
- diffraction limit
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: intro
summary: "In scalar diffraction theory the incoherent OTF of a lens of numerical aperture NA is zero above 2 NA/lambda, so periods finer than lambda/(2 NA) image as a uniform field."
prereqs: [optical-transfer-function, point-spread-function, convolution-theorem]
see_also: [rayleigh-criterion, sampling-theorem, structured-illumination-microscopy, single-molecule-localization, localization-precision-formula, super-resolution, image-deblurring, autocorrelation]
sources:
  - paper: doi:10.1007/BF02956173
    title: Ernst Abbe, Beitrage zur Theorie des Mikroskops und der mikroskopischen Wahrnehmung, Archiv fur mikroskopische Anatomie 9(1), 1873
    locator: pages 413 to 468 (the image as the result of the diffraction orders that the objective collects, and the smallest resolvable period)
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, 3rd edition, Roberts and Company, 2005
    locator: sections 6.2.1 (the amplitude transfer function and its cutoff), 6.3.1 to 6.3.4 (the OTF as the autocorrelation of the pupil and its cutoff) and 6.6 (resolution beyond the classical diffraction limit)
  - paper: doi:10.1073/pnas.0406877102
    title: Mats G. L. Gustafsson, Nonlinear structured-illumination microscopy, wide-field fluorescence imaging with theoretically unlimited resolution, Proceedings of the National Academy of Sciences 102(37), 2005
    locator: pages 13081 to 13086
  - paper: doi:10.1126/science.1127344
    title: Eric Betzig, George H. Patterson, Rachid Sougrat, O. Wolf Lindwasser, Scott Olenych, Juan S. Bonifacino, Michael W. Davidson, Jennifer Lippincott-Schwartz and Harald F. Hess, Imaging intracellular fluorescent proteins at nanometer resolution, Science 313(5793), 2006
    locator: pages 1642 to 1645
---

The Abbe diffraction limit says that a lens cannot transfer spatial frequencies above a cutoff fixed by its numerical aperture $\mathrm{NA}$ and the wavelength $\lambda$. Here it is stated as a theorem about the [optical transfer function](/optical-transfer-function/): in scalar diffraction theory, with incoherent light, the OTF is zero for frequencies at or above $2\,\mathrm{NA}/\lambda$. So a grating with a period below $\lambda/(2\,\mathrm{NA})$ is imaged as a uniform field, whatever the aberrations are. The limit is a cutoff frequency. It is not a rule for when two points look separate; that is the [Rayleigh criterion](/rayleigh-criterion/), a convention with the larger distance $0.61\,\lambda/\mathrm{NA}$. For $\lambda = 500$ nm and $\mathrm{NA} = 1.4$ the Abbe period is $500/2.8 = 178.6$ nm. The theorem holds only under its hypotheses. Methods that break them, such as saturated [structured illumination](/structured-illumination-microscopy/) and [single-molecule localization](/single-molecule-localization/), resolve detail far below $\lambda/(2\,\mathrm{NA})$.

## Statement

**Model.** Light of one wavelength $\lambda$ (in vacuum) comes from a planar object and is imaged by a system that is shift invariant over the field. Scalar diffraction theory in the Fraunhofer form holds: the amplitude transfer function of the system is a pupil function $P(\eta)$ of the spatial frequency $\eta \in \mathbb{R}^2$ in the object plane, square integrable and not zero. The objective accepts the plane waves that leave the object at angles $\theta$ with $n \sin\theta \le \mathrm{NA}$, where $n$ is the refractive index of the object space. A plane wave component of frequency $\eta$ leaves at the angle with $n \sin\theta = \lambda |\eta|$. So

$$P(\eta) = 0 \quad \text{for } |\eta| > \mathrm{NA}/\lambda .$$

Inside the disk $P$ can be any function: aberrations $P = |P|\, e^{ikW}$ are allowed. The light is incoherent, so the image intensity is $i = h \ast o$ with the intensity PSF $h = |\check P|^2 / \int |P|^2$, and the OTF is $H = \hat h$.

**Theorem.** Under this model:

1. $H(\xi) = 0$ for every $\xi$ with $|\xi| \ge 2\,\mathrm{NA}/\lambda$.
2. For every object intensity $o$ whose spectrum exists as a tempered distribution, the image spectrum $\hat i = H \hat o$ is zero on $|\xi| \ge 2\,\mathrm{NA}/\lambda$. Two objects whose spectra agree on the open disk $|\xi| < 2\,\mathrm{NA}/\lambda$ give the same image.
3. In particular the grating $o(x) = 1 + m\cos(2\pi x_1/d + \varphi)$ with period $d \le \lambda/(2\,\mathrm{NA})$ gives the uniform image $i \equiv 1$.

For coherent illumination by one plane wave at normal incidence, the image amplitude is the object amplitude filtered by $P$, so the amplitude spectrum is zero for $|\xi| > \mathrm{NA}/\lambda$, and a grating with a period below $\lambda/\mathrm{NA}$ gives a uniform image.

## In plain words

Fine detail in an object bends light to wide angles. A lens catches light only inside a cone, whose width is set by its numerical aperture. Detail that sends its light outside the cone leaves no trace in the image. With ordinary light that comes from all points at random, the finest stripe pattern that can show up has a stripe period of about half the wavelength divided by the numerical aperture. A good oil objective with green light reaches about 180 nanometers. Stripes finer than that do not look blurred; they vanish, and the image is a flat gray. No lens design and no computer can bring them back from that one image, because the image holds no information about them. Tricks that beat the limit change the rules: they switch the molecules on and off, or they use light patterns and a nonlinear response.

## Proof

Write $r = \mathrm{NA}/\lambda$ and $a = \check P$, the inverse Fourier transform of the pupil, so that the amplitude PSF is $a$.

*Step 1: the PSF is integrable.* $P$ is square integrable, so $a$ is too, and by Plancherel $\int |a|^2 = \int |P|^2 > 0$. So $h = |a|^2 / \int |P|^2$ is integrable, nonnegative, with $\int h = 1$, and $H = \hat h$ is a continuous function with $H(0) = 1$.

*Step 2: the OTF is the autocorrelation of the pupil.* $h$ is the product of $a$ and $\bar a$, up to the constant. The Fourier transform of $a$ is $P$, and the Fourier transform of $\bar a$ is $\eta \mapsto \overline{P(-\eta)}$. The transform of a product of two square integrable functions is the convolution of their transforms. So

$$H(\xi) = \frac{1}{\int |P|^2} \int P(\eta)\, \overline{P(\eta - \xi)}\, d\eta .$$

*Step 3: the support.* Let $|\xi| > 2r$. If $|\eta| \le r$, then $|\eta - \xi| \ge |\xi| - |\eta| > 2r - r = r$, so $P(\eta - \xi) = 0$. If $|\eta| > r$, then $P(\eta) = 0$. So the integrand is zero for every $\eta$, and $H(\xi) = 0$. For $|\xi| = 2r$ the two disks $|\eta| \le r$ and $|\eta - \xi| \le r$ meet only at the point $\eta = \xi/2$, a set of measure zero, so again $H(\xi) = 0$. This proves part 1.

*Step 4: the image.* The image is $i = h \ast o$ with $h$ integrable. By the convolution theorem, $\hat i = H \hat o$, which is zero where $H$ is zero. Two objects whose spectra agree on the open disk give image spectra that agree on the open disk and are both zero outside it, so the images are equal. This proves part 2.

*Step 5: the grating.* The grating has the spectrum $\delta(\xi) + \tfrac{m}{2}\big(e^{i\varphi}\delta(\xi - \xi_0) + e^{-i\varphi}\delta(\xi + \xi_0)\big)$ with $\xi_0 = (1/d, 0)$. For $d \le \lambda/(2\,\mathrm{NA})$ we have $|\xi_0| \ge 2r$, so $H(\pm\xi_0) = 0$ by part 1, and $\hat i = H(0)\,\delta = \delta$. So $i \equiv 1$. This proves part 3.

*Coherent case.* With normal incidence the image amplitude has the spectrum $P \hat u$, where $u$ is the object amplitude. It is zero for $|\xi| > r$ because $P$ is. The grating at a period $d < 1/r$ keeps only the zero order, so the amplitude, and with it the intensity, is uniform. $\blacksquare$

## Consequences

- **Sampling.** The image is band-limited to $|\xi| < 2\,\mathrm{NA}/\lambda$. By the [sampling theorem](/sampling-theorem/), a pixel pitch of $\lambda/(4\,\mathrm{NA})$ in the object plane, $89.3$ nm for $\lambda = 500$ nm and $\mathrm{NA} = 1.4$, samples it without aliasing. A coarser pitch folds frequencies near the cutoff onto lower ones.
- **Deconvolution has a hard ceiling.** Deconvolution divides by the OTF where it is large compared with the noise. Above the cutoff $H = 0$, and by part 2 the data do not depend on the object there. So no linear deconvolution and no method without prior knowledge can restore those frequencies. With prior knowledge the picture changes: the spectrum of an object of bounded support is an analytic function, so in exact arithmetic it is fixed by its values inside the disk, and methods that extrapolate the spectrum exist (Goodman, section 6.6). The extrapolation is badly ill-posed, and with noise it gains little.
- **Abbe's coherent setting.** Abbe studied a microscope with a condenser. With an illumination cone of numerical aperture $\mathrm{NA}_c$, a plane wave at an oblique angle shifts the spectrum of the object, and the smallest period that sends two orders into the objective is $\lambda/(\mathrm{NA} + \mathrm{NA}_c)$. With a full condenser, $\mathrm{NA}_c = \mathrm{NA}$, this is $\lambda/(2\,\mathrm{NA})$ again, the same number as the incoherent cutoff.
- **The Rayleigh distance is a different number.** $\lambda/(2\,\mathrm{NA}) = 0.5\,\lambda/\mathrm{NA}$ is a period that the system cannot transfer at all. The Rayleigh distance $0.61\,\lambda/\mathrm{NA}$ and the Sparrow distance $0.47\,\lambda/\mathrm{NA}$ are conventions about when two points look like two (see [Rayleigh criterion](/rayleigh-criterion/)). A grating with a period of $0.51\,\lambda/\mathrm{NA}$ passes the system, but with very little contrast.
- **Methods that pass the limit.** Each of these breaks a hypothesis of the theorem, so the theorem does not apply to them. Linear [structured illumination](/structured-illumination-microscopy/) makes the illumination a pattern, so the image is no longer $h \ast o$ for one shift-invariant $h$; it moves frequencies of the object into the passband and reaches about twice the cutoff. Saturated structured illumination uses the nonlinear response of the dye, and Gustafsson (2005) showed that it has no limit in theory. [Single-molecule localization](/single-molecule-localization/) (Betzig et al. 2006) uses the prior that only a few emitters are on in each frame, and finds each one with a precision set by the photon count (see [localization precision formula](/localization-precision-formula/)), not by the cutoff. Near-field methods detect the evanescent waves, which the Fraunhofer model leaves out.

## Tightness

The cutoff cannot be lowered for the aberration-free circular pupil. With $P = 1$ on the disk $|\eta| \le r$, the integral in Step 2 is the area of the overlap of two disks of radius $r$ with centers $|\xi|$ apart. This area is positive for every $|\xi| < 2r$, and it gives

$$H(\rho) = \frac{2}{\pi}\left(\arccos\frac{\rho}{2r} - \frac{\rho}{2r}\sqrt{1 - \Big(\frac{\rho}{2r}\Big)^2}\,\right) > 0, \qquad 0 \le \rho < 2r .$$

So every grating with a period above $\lambda/(2\,\mathrm{NA})$ is imaged with some contrast, though the contrast goes to zero at the cutoff: $H = 0.0414$ at $\rho/2r = 0.8929$, which is a period of 200 nm for $\lambda = 500$ nm and $\mathrm{NA} = 1.4$.

The hypotheses cannot be dropped. With aberrations, the OTF still vanishes above the cutoff, but it can also vanish below it: a defocused system has zeros of the OTF inside the passband, so part 1 gives a frequency band that is always lost, not one that is always kept. The cutoff depends only on the support of $P$: an annular pupil of the same outer radius has the same cutoff. Without the incoherent model (coherent light) the cutoff for amplitudes is halved, and without the shift invariant model (structured or scanned illumination with a nonlinear response) there is no cutoff in the sense of part 2.

## History

Ernst Abbe (1873) explained image formation in the microscope by diffraction: the object, lit by the condenser, splits the light into diffraction orders, and the image shows a periodic detail only if the objective collects at least two of them. This gives the smallest resolvable period $\lambda/(\mathrm{NA} + \mathrm{NA}_c)$ and, with a full condenser, $\lambda/(2\,\mathrm{NA})$. The formula $d = \lambda/(2\,n\sin\alpha)$ is now known as the Abbe limit. The statement as the cutoff of a transfer function came with the Fourier analysis of optical systems in the twentieth century, which Goodman presents in chapter 6. Gustafsson (2005) and Betzig et al. (2006) are two of the methods that showed in practice that the limit binds only linear, shift-invariant, single-image systems.

## References
