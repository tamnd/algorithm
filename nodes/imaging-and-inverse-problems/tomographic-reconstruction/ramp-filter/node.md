---
tag: JE1G1B
kind: definition
slug: ramp-filter
name: Ramp filter
aliases:
- Ram-Lak filter
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: The filter with frequency response |sigma| that undoes the 1/r blur of back-projection, often multiplied by a window to limit noise.
model: real-ram
prereqs: [back-projection-operator, fourier-slice-theorem]
see_also: [filtered-back-projection, back-projection-operator, radon-inversion-formula, hilbert-transform, window-functions, point-spread-function, lambda-tomography, fan-beam-filtered-back-projection]
sources:
  - paper: doi:10.1073/pnas.68.9.2236
    title: G. N. Ramachandran and A. V. Lakshminarayanan, Three-dimensional reconstruction from radiographs and electron micrographs, application of convolutions instead of Fourier transforms, Proceedings of the National Academy of Sciences 68(9), 1971
    locator: pp. 2236 to 2240 (the sampled band-limited ramp kernel)
  - paper: doi:10.1109/TNS.1974.6499235
    title: L. A. Shepp and B. F. Logan, The Fourier reconstruction of a head section, IEEE Transactions on Nuclear Science 21(3), 1974
    locator: pp. 21 to 43 (the smoother kernel with the sinc window)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.3.2 (the filter |w| in the filtered back-projection formula) and Section 3.3.3 (the sampled kernel and the zero padding)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section V.1 (filters for filtered backprojection)
---

The ramp filter is the 1D filter with the frequency response $|\sigma|$. It acts on each projection of a CT [sinogram](/sinogram/) along the detector variable $s$. The [back-projection operator](/back-projection-operator/) alone gives the object blurred by the kernel $1/r$, whose 2D Fourier transform is $1/|\xi|$. The ramp multiplies each projection by $|\sigma|$ in frequency, and by the [Fourier slice theorem](/fourier-slice-theorem/) this cancels the blur exactly. Back projection of the filtered projections is [filtered back-projection](/filtered-back-projection/). In practice the ramp is cut off at the Nyquist frequency of the detector and often multiplied by a window, because it amplifies high-frequency noise.

## Definition

The Fourier transform uses ordinary frequency, $\mathcal{F}_1 g(\sigma) = \int g(s)\,e^{-2\pi i s\sigma}\,ds$. The **ramp filter** is the operator $\Lambda$ on functions of one variable with
$$\mathcal{F}_1(\Lambda g)(\sigma) = |\sigma|\,\mathcal{F}_1 g(\sigma).$$
For a smooth $g$ that decays fast, $\Lambda g = \frac{1}{2\pi} H g'$, where $H$ is the [Hilbert transform](/hilbert-transform/): the derivative has the multiplier $2\pi i\sigma$ and $H$ has $-i\,\mathrm{sgn}\,\sigma$. As a convolution, $\Lambda$ has the kernel $-1/(2\pi^2 s^2)$, taken as a finite-part distribution. It is not an integrable function, and $\Lambda$ is not a convolution with an ordinary kernel.

**Band-limited ramp.** Let the detector spacing be $\tau$, with the Nyquist frequency $b = 1/(2\tau)$. The band-limited ramp is $|\sigma|$ for $|\sigma| \le b$ and 0 outside. Its kernel is
$$h(s) = \int_{-b}^{b} |\sigma|\,e^{2\pi i s\sigma}\,d\sigma = b^2\big(2\,\mathrm{sinc}(2bs) - \mathrm{sinc}^2(bs)\big), \qquad \mathrm{sinc}(x) = \frac{\sin \pi x}{\pi x}.$$
At the samples $s = m\tau$ this gives
$$h(0) = \frac{1}{4\tau^2}, \qquad h(m\tau) = 0 \text{ for even } m \ne 0, \qquad h(m\tau) = -\frac{1}{\pi^2 m^2\tau^2} \text{ for odd } m.$$
The discrete filter is $q[n] = \tau\sum_m h(m\tau)\,p[n - m]$. Its frequency response $\tau\sum_m h(m\tau)\,e^{-2\pi i m\nu\tau}$ is exactly $|\nu|$ on $|\nu| \le b$, because $h$ is band-limited to $b$ and the samples are at the Nyquist rate. This kernel is due to Ramachandran and Lakshminarayanan (1971).

**Windowed ramps.** A window $W(\nu)$ with $W(0) = 1$ gives the response $|\nu|\,W(\nu)$. The Shepp-Logan kernel uses $W(\nu) = \mathrm{sinc}(\nu\tau)$. Its samples are
$$h_{SL}(m\tau) = -\frac{2}{\pi^2\tau^2(4m^2 - 1)},$$
and its response is $|\nu|\,\mathrm{sinc}(\nu\tau)$ on $|\nu| \le b$. Other common choices are the cosine, Hann and Hamming [windows](/window-functions/). A window lowers the gain at high frequency. This reduces the noise and the ringing near edges, and it also lowers the resolution.

**Why the ramp.** With $\theta \in [0, \pi)$, the inverse 2D Fourier transform in polar coordinates with a signed radius $\sigma$ has the area element $|\sigma|\,d\sigma\,d\theta$. The factor $|\sigma|$ is the ramp. Without it, back projection gives $\mathcal{R}^\#\mathcal{R}f = f * \frac{1}{|x|}$, and with it, $\mathcal{R}^\#(\Lambda\,\mathcal{R}f) = f$ ([Radon inversion formula](/radon-inversion-formula/)).

## Examples and non-examples

**Kernel values.** For $\tau = 1/4$, the band limit is $b = 2$. The two kernels at $m = 0, 1, 2, 3$ are:

| $m$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| band-limited ramp $h(m\tau)$ | 4 | -1.6211 | 0 | -0.1801 |
| Shepp-Logan $h_{SL}(m\tau)$ | 3.2423 | -1.0808 | -0.2162 | -0.0926 |

Both kernels have one positive center value and negative side values that fall off like $1/m^2$. The responses at $\nu = 0.5, 1, 2$ are:

| $\nu$ | 0.5 | 1 | 2 |
|---|---|---|---|
| band-limited ramp | 0.5 | 1 | 2 |
| Shepp-Logan | 0.4872 | 0.9003 | 1.2732 |

At the Nyquist frequency the Shepp-Logan response is $2\,\mathrm{sinc}(1/2) = 4/\pi$, which is 64 percent of the ramp.

**The Gaussian.** The projections of $f(x) = e^{-\pi|x|^2}$ are $g(s) = e^{-\pi s^2}$ at each angle, with $\mathcal{F}_1 g(\sigma) = e^{-\pi\sigma^2}$. Then $\Lambda g(0) = \int |\sigma|\,e^{-\pi\sigma^2}\,d\sigma = 1/\pi$. The back projection over $[0, \pi)$ at the origin gives $\pi\cdot 1/\pi = 1 = f(0)$. Without the ramp the back projection gives $\pi$.

**A truncated kernel.** The infinite sampled kernel sums to zero: $\tau\sum_m h(m\tau) = \frac{1}{4\tau} - \frac{2}{\pi^2\tau}\sum_{m \text{ odd}, m > 0}\frac{1}{m^2} = 0$, since the odd sum is $\pi^2/8$. A kernel cut off at $|m| \le M$ has the response $\frac{2}{\pi^2\tau}\sum_{m \text{ odd}, m > M} m^{-2} > 0$ at $\nu = 0$, about $1/(\pi^2\tau M)$. This small DC term is correct for a finite detector. A ramp sampled directly on the DFT grid sets this term to 0 and gives a constant offset in the image. So the kernel is sampled in space, zero-padded to at least $2d - 1$ points against circular wrap, and then transformed (Kak and Slaney, Section 3.3.3).

**Noise.** For white noise of variance $v$ per detector sample, the filtered value has variance $v\,\tau\int_{-b}^{b}\sigma^2\,d\sigma = \frac{2}{3}\,v\,\tau\,b^3 = \frac{v}{12\tau^2}$. Halving the detector spacing makes the noise variance 4 times larger, which is the price of the higher resolution.

**Non-example: the derivative.** The derivative $d/ds$ has the multiplier $2\pi i\sigma$. Its magnitude is a ramp, but it is odd and has a phase of $\pm 90$ degrees, so back projection after the derivative alone does not give $f$. The ramp is $\frac{1}{2\pi}H\,d/ds$; the Hilbert transform fixes the phase. [Lambda tomography](/lambda-tomography/) uses a second derivative, which is local, and so recovers only the edges.

**Non-example: a 2D filter on the projections.** The ramp acts in 1D along $s$, for each angle separately. The 2D ramp $|\xi|$ instead acts on the image after back projection, and $\mathcal{F}^{-1}(|\xi|\,\mathcal{F}(\mathcal{R}^\#\mathcal{R}f)) = f$ as well. This order is valid, but the blurred image $\mathcal{R}^\#\mathcal{R}f$ does not vanish outside the object, and a finite grid then cuts off its tail.

## Related definitions

- [Back-projection operator](/back-projection-operator/): the adjoint of the Radon transform, whose $1/r$ blur the ramp undoes.
- [Hilbert transform](/hilbert-transform/): with a derivative, it gives the ramp, $\Lambda = \frac{1}{2\pi}H\,d/ds$.
- [Window functions](/window-functions/): the factors that taper the ramp at high frequency.
- [Point spread function](/point-spread-function/): the response to a point; for back projection alone it is $1/r$.
- [Filtered back-projection](/filtered-back-projection/): the algorithm that applies the ramp to each projection and then back-projects.
- [Fan-beam filtered back-projection](/fan-beam-filtered-back-projection/): the same filter with a weight for divergent rays.

## References
