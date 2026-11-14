---
tag: SRBZV4
kind: model
slug: hopkins-imaging-model
name: Hopkins imaging model
aliases:
- transmission cross coefficient model
- TCC model
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Hopkins' model of partially coherent imaging that gives the aerial image as a bilinear form of the mask spectrum with the transmission cross coefficients.
prereqs: [discrete-fourier-transform, convolution]
see_also: [optical-proximity-correction, sum-of-coherent-systems, inverse-lithography-technology, spectral-theorem, positive-definite-matrix, fast-fourier-transform]
sources:
  - paper: doi:10.1098/rspa.1953.0071
    title: H. H. Hopkins, On the diffraction theory of optical images, Proceedings of the Royal Society of London A 217(1130), 408 to 432, 1953
    locator: the image of an object under partially coherent illumination written with a transmission factor that depends only on the illumination and the lens, so that it is computed once for all objects; this factor is the later transmission cross coefficient
  - paper: "Nicolas Bailey Cobb, Fast Optical and Process Proximity Correction Algorithms for Integrated Circuit Manufacturing, PhD thesis, Department of Electrical Engineering and Computer Sciences, University of California at Berkeley, 1998"
    locator: the Hopkins model of a projection printer with Koehler illumination as the starting point of fast aerial image computation, and its decomposition into a sum of coherent systems
---

The Hopkins imaging model computes the light intensity that a projection lens forms from a photomask under partially coherent illumination, the *aerial image*. It writes the image as a quadratic form in the spectrum of the mask, whose kernel, the *transmission cross coefficient* or TCC, depends only on the source and the lens. So the kernel is computed once for a scanner setting and reused for every mask, which is why the model underlies [optical proximity correction](/optical-proximity-correction/), the [sum of coherent systems](/sum-of-coherent-systems/) and [inverse lithography](/inverse-lithography-technology/). Hopkins gave the model in 1953. This page states its assumptions, derives the TCC form from them, and proves the properties that the fast methods rely on.

## The machine

The model has four parts, with spatial frequencies in the plane of the mask written as $f$ (cycles per unit length, a vector in two dimensions).

- **Source.** An extended source, imaged into the pupil of the condenser (Koehler illumination). Each source point $s$ sends a plane wave $e^{2\pi i s \cdot x}$ onto the mask. The points are mutually incoherent, and point $s$ has intensity $J(s) \ge 0$.
- **Mask.** A thin mask with complex transmission $m(x)$, periodic with period $P$ in each direction, as in simulation with periodic boundaries. Its Fourier coefficients are $M(f)$ for $f$ on the lattice $\frac{1}{P}\mathbb{Z}^2$.
- **Lens.** A shift-invariant projection system with pupil function $H(f)$: it multiplies the spectrum of the field by $H$. For an ideal lens of numerical aperture $\mathrm{NA}$ at wavelength $\lambda$, $H$ is $1$ on the disk $|f| \le \mathrm{NA}/\lambda$ and $0$ outside; defocus and aberrations multiply it by a phase. Magnification is set to $1$.
- **Detector.** The output is the intensity $I(x)$ in the image plane, before any resist model.

**Assumptions.** (A1) The mask is thin: the field just after it is $m(x)$ times the incident wave (the Kirchhoff approximation). (A2) The lens acts linearly and shift-invariantly on the scalar field, so it is the pupil filter $H$. (A3) Intensities from different source points add, weighted by $J$. These are the assumptions of scalar imaging; they ignore polarization, the vector nature of light at high $\mathrm{NA}$, and the thickness of the mask.

**Derivation of the TCC form.** Under (A1), the field after the mask lit from $s$ is $m(x) e^{2\pi i s \cdot x}$, whose Fourier coefficient at $f$ is $M(f - s)$. Under (A2), the image field is

$$ E_s(x) = \sum_{f} H(f) M(f - s) e^{2\pi i f \cdot x} = e^{2\pi i s \cdot x} \sum_{f'} H(f' + s) M(f') e^{2\pi i f' \cdot x}, $$

with $f = f' + s$. The sum is finite, because $H$ vanishes outside a bounded disk. Then $|E_s(x)|^2$ is a finite double sum, the factor $e^{2\pi i s \cdot x}$ cancels in it, and under (A3)

$$ I(x) = \int J(s)\, |E_s(x)|^2\, ds = \sum_{f'} \sum_{f''} T(f', f'')\, M(f')\, \overline{M(f'')}\, e^{2\pi i (f' - f'') \cdot x}, $$

$$ T(f', f'') = \int J(s)\, H(f' + s)\, \overline{H(f'' + s)}\, ds. $$

The exchange of the integral with the double sum is valid because, for a bounded $J$ supported on a bounded set, only finitely many terms are nonzero. $T$ is the transmission cross coefficient. It does not depend on the mask.

The direct method that integrates $|E_s|^2$ over the source, one source point at a time, is called Abbe's method. It gives the same image; the two differ only in the order of summation.

## What it counts

The model returns the aerial image intensity $I(x)$ at each point of the image plane, for a given mask, source and pupil. The resist is a separate model, often a threshold on $I$, perhaps after a blur; the printed contour is a level set of the result.

The costs are as follows. Suppose $N$ lattice frequencies lie in the band where $T$ can be nonzero. Then $T$ is an $N \times N$ matrix, computed once. One image needs the $N^2$ products $T(f', f'') M(f') \overline{M(f'')}$, collected by the difference $f' - f''$ into the image spectrum, then an inverse transform. The image spectrum lies in a band of twice the radius. In two dimensions, $N$ grows with the square of the period $P$, so $T$ has a number of entries that grows with $P^4$. This is the cost that the [sum of coherent systems](/sum-of-coherent-systems/) removes. Abbe's method costs one transform per source point instead.

## Relation to other models

- **Coherent imaging.** For a point source, $J = \delta(s - s_0)$, the kernel is $T(f', f'') = H(f' + s_0)\overline{H(f'' + s_0)}$, of rank one, and $I = |E_{s_0}|^2$. The image is the squared modulus of a [convolution](/convolution/) of the mask with the lens impulse response.
- **Incoherent imaging.** If $J$ is constant on a region that contains every $s$ where $H(f' + s)\overline{H(f'' + s)} \ne 0$, then $T(f', f'') = c \int H(u)\overline{H(u + f'' - f')}\, du$ depends only on $f' - f''$, and the image is linear in $|m|^2$: it is $|m|^2$ filtered by the autocorrelation of the pupil, the optical transfer function.
- **Partial coherence.** Between the two, with a source of radius $\sigma \mathrm{NA}/\lambda$ for a fill factor $0 < \sigma < 1$, the image is neither linear in $m$ nor in $|m|^2$. In particular the image of two masks added is not the sum of their images.
- **Sum of coherent systems.** The eigendecomposition of $T$ writes the image as a weighted sum of coherent images. See [sum of coherent systems](/sum-of-coherent-systems/) for the expansion and its truncation error.
- **Beyond the model.** Vector imaging at high $\mathrm{NA}$, thick masks where diffraction depends on the angle of incidence, and stacks of films on the wafer all break the assumptions (A1) to (A3). Thick-mask effects are often added by changing the mask spectrum for each source region, which keeps a TCC-like form only approximately.

## Known results in the model

**Hermitian and positive semidefinite.** For any finite set of frequencies, the matrix $T$ is Hermitian and positive semidefinite, so every image is real and nonnegative.

*Proof.* $T(f'', f') = \int J(s) H(f'' + s)\overline{H(f' + s)}\, ds = \overline{T(f', f'')}$, since $J$ is real. For any coefficients $c$,

$$ \sum_{f', f''} \overline{c_{f'}}\, T(f', f'')\, c_{f''} = \int J(s) \Big| \sum_{f} \overline{c_f}\, H(f + s) \Big|^2 ds \ge 0, $$

because $J \ge 0$. The image is the quadratic form with $c_f = \overline{M(f)} e^{-2\pi i f \cdot x}$, so it is real and at least $0$. $\square$

By the [spectral theorem](/spectral-theorem/), $T$ then has an orthonormal basis of eigenvectors with real eigenvalues $\lambda_1 \ge \lambda_2 \ge \dots \ge 0$. This is the fact the [sum of coherent systems](/sum-of-coherent-systems/) is built on.

**Band limit.** If the source lies in the disk $|s| \le \sigma \mathrm{NA}/\lambda$ and the pupil in the disk $|f| \le \mathrm{NA}/\lambda$, then $T(f', f'') = 0$ unless $|f'|, |f''| \le (1 + \sigma)\mathrm{NA}/\lambda$, and the image spectrum lies in $|g| \le 2(1 + \sigma)\mathrm{NA}/\lambda$.

*Proof.* $T(f', f'') \ne 0$ needs some $s$ with $J(s) > 0$ and $H(f' + s) \ne 0$, so $|f'| \le |f' + s| + |s| \le (1 + \sigma)\mathrm{NA}/\lambda$, and the same for $f''$. The image frequency is $f' - f''$. $\square$

**Smallest printable pitch.** Take one dimension, a mask that is periodic with pitch $p$, a source on $[-\sigma \mathrm{NA}/\lambda, \sigma \mathrm{NA}/\lambda]$ with $0 \le \sigma \le 1$, and the pupil $[-\mathrm{NA}/\lambda, \mathrm{NA}/\lambda]$. If $p < \lambda / ((1 + \sigma)\mathrm{NA})$, the image is constant.

*Proof.* The mask frequencies are $k/p$. For $k \ne 0$ and a source point $s$, $|k/p + s| \ge 1/p - |s| > (1 + \sigma)\mathrm{NA}/\lambda - \sigma \mathrm{NA}/\lambda = \mathrm{NA}/\lambda$, so $H(k/p + s) = 0$. Hence $T(f', f'') = 0$ unless $f' = f'' = 0$, and $I(x) = T(0, 0) |M(0)|^2$ for all $x$. $\square$

At $\lambda = 193$ nm and $\mathrm{NA} = 1.35$, the limit is $143$ nm for coherent light ($\sigma = 0$) and $75.2$ nm for $\sigma = 0.9$. Off-axis light lets one diffraction order and the zero order pass together at a pitch where on-axis light passes only the zero order.

**Example.** Work in units where $\mathrm{NA}/\lambda = 1$. Let the source be uniform on $[-\frac{1}{2}, \frac{1}{2}]$ with $J = 1$ there, the pupil $1$ on $[-1, 1]$, and the mask equal lines and spaces of pitch $p$ with $1/p = 1.2$, so $m = 1$ on $[-p/4, p/4]$ and $0$ on the rest of the period. Its coefficients are $M(0) = \frac{1}{2}$, $M(\pm\frac{1}{p}) = \frac{1}{\pi}$, $M(\pm\frac{2}{p}) = 0$, and the higher orders are cut off. The TCC entries are lengths of intervals: $T(0, 0) = 1$; $T(\pm 1.2, \pm 1.2) = 0.3$ (the source points in $[-\frac{1}{2}, -0.2]$ pass the order $+1.2$); $T(0, \pm 1.2) = 0.3$; and $T(1.2, -1.2) = 0$, since no source point passes both first orders. So

$$ I(x) = \frac{1}{4} + \frac{0.6}{\pi^2} + \frac{0.6}{\pi} \cos\frac{2\pi x}{p} \approx 0.3108 + 0.1910 \cos\frac{2\pi x}{p}, $$

between $0.1198$ and $0.5018$, a contrast of $0.61$. A direct Abbe integration over $20000$ source points agrees to $10^{-12}$. With coherent light ($\sigma = 0$) the same mask gives the constant $\frac{1}{4}$, since $1/p > 1$.

**Normalization.** A clear mask, $m \equiv 1$, has only $M(0) = 1$, so its image is $T(0, 0) = \int J(s) |H(s)|^2 ds$, the total source power that passes the pupil. Images are usually divided by this value.

## References
