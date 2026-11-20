---
tag: BPG5QE
kind: algorithm
slug: angular-spectrum-method
name: Angular spectrum method
aliases:
- angular spectrum propagation
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: "Propagate a sampled scalar field by a distance z: take its 2D DFT, multiply by exp(2 pi i z sqrt(1/lambda^2 - f^2)), drop evanescent waves and transform back. Exact for periodic band-limited fields."
model: real-ram
complexity:
  vars: {n: "the side of an n x n sample grid, a power of two, with an FFT"}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: false, in_place: false, exact: true}
prereqs: [discrete-fourier-transform, fast-fourier-transform, wave-equation]
see_also: [digital-holography-reconstruction, transport-of-intensity-equation, twin-image-problem, phase-retrieval, convolution-theorem, multidimensional-fft, sampling-theorem, diffraction-tomography]
sources:
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, third edition, Roberts and Company, 2005
    locator: Chapter 3, the section on the angular spectrum of plane waves (propagation of the angular spectrum, evanescent waves, the transfer function of free space); Chapter 4 for the Fresnel approximation
  - paper: doi:10.1364/OE.17.019662
    title: Kyoji Matsushima and Tomoyoshi Shimobaba, Band-limited angular spectrum method for numerical simulation of free-space propagation in far and near fields, Optics Express 17(22), 2009, 19662 to 19673
    locator: the sampling problem of the transfer function at long distances and the band limit (general locator)
  - paper: doi:10.1364/AO.33.000179
    title: Ulf Schnars and Werner Juptner, Direct recording of holograms by a CCD target and numerical reconstruction, Applied Optics 33(2), 1994, 179 to 181
    locator: numerical propagation of a recorded field as the reconstruction step of digital holography (general locator)
---

The angular spectrum method computes a monochromatic scalar field at a distance $z$ from its samples in one plane. It writes the field as a sum of plane waves with the 2D [discrete Fourier transform](/discrete-fourier-transform/), moves each plane wave by its own phase factor, drops the evanescent waves, and sums the waves again. In the periodic model of the sample grid the result is exact, which this page proves; for a real aperture it is accurate when the grid is padded and the transfer function is sampled well. It is the propagation step of [digital holography reconstruction](/digital-holography-reconstruction/), of the [transport of intensity equation](/transport-of-intensity-equation/) and of many methods for [phase retrieval](/phase-retrieval/).

## In plain words

Light that leaves a plane can be split into many flat waves, each one going in a slightly different direction. A flat wave is easy to move forward: it only shifts its phase, by an amount that depends on its direction and on the distance. So the method splits the field into flat waves with a Fourier transform, turns the phase of each wave by the right amount, and adds the waves back together.

Some of the waves in the split do not travel. They change too fast across the plane for the given color of light, and they die out within a few wavelengths. The method throws them away. Everything else is moved without any loss, so moving forward and then backward by the same distance gives the start field again.

## The problem

The input is a complex field $u$ sampled on an $n_1 \times n_2$ grid with spacing $d$ in a plane $z = 0$, the wavelength $\lambda$ and a distance $z$ (positive or negative). The output is the field at the same grid points in the plane $z$. The field obeys the Helmholtz equation $\nabla^2 U + k^2 U = 0$ with $k = 2\pi/\lambda$, which is the [wave equation](/wave-equation/) for one time frequency. The time dependence is $e^{-i\omega t}$, the convention of Goodman, so a wave that travels toward $+z$ has the factor $e^{+ikz}$. With the opposite time convention the sign of the exponent in $H$ below changes.

With the continuous Fourier transform $\mathcal{F} u(f) = \int u(r) e^{-2\pi i f \cdot r}\, dr$ of this area, the exact answer for a field with no sources at $z > 0$ is

$$U(\cdot, z) = \mathcal{F}^{-1}\big[\mathcal{F} U(\cdot, 0)\, H_z\big], \qquad H_z(f_x, f_y) = \begin{cases} e^{2\pi i z \sqrt{1/\lambda^2 - f_x^2 - f_y^2}} & f_x^2 + f_y^2 < 1/\lambda^2, \\ e^{-2\pi z \sqrt{f_x^2 + f_y^2 - 1/\lambda^2}} & \text{otherwise,} \end{cases}$$

for $z \ge 0$. The method computes this on the grid and replaces the second line, the evanescent part, by $0$.

## The algorithm

DFT2 and IDFT2 are the 2D DFT and its inverse with the factor $1/(n_1 n_2)$. The index $k$ along an axis of $n$ samples stands for the signed index $\bar k = k$ if $2k < n$ and $\bar k = k - n$ otherwise. The optional band limits $b_x$ and $b_y$ are $+\infty$ for the plain method.

```pseudo id=main
ANGULAR-SPECTRUM(u, d, λ, z)          ▷ u is n1 x n2, spacing d
L1  U <- DFT2(u)
L2  for k <- 0 .. n1 - 1, l <- 0 .. n2 - 1 do
L3      fy <- k̄ / (n1 d),  fx <- l̄ / (n2 d)
L4      w <- 1/λ^2 - fx^2 - fy^2
L5      if w > 0 and |fx| <= bx and |fy| <= by then V[k][l] <- U[k][l] · exp(2πi z sqrt(w))
L6      else V[k][l] <- 0                ▷ evanescent or outside the band limit
L7  return IDFT2(V)
```

Line L3 maps each DFT index to its spatial frequency in cycles per unit length. Line L5 applies the transfer function of free space to a wave that propagates. Line L6 drops the evanescent waves, for which $w \le 0$. For $z < 0$ the same lines back-propagate the field.

**Padding.** The DFT treats the field as periodic with the periods $n_1 d$ and $n_2 d$, so light that leaves one side of the window comes back in at the other side. To approximate a field in an infinite plane, put the field in the center of a grid twice as large in each direction, filled with zeros, run the algorithm, and keep the center.

**The band limit.** At a long distance the phase of $H$ changes fast between neighboring frequency samples, and the sampled $H$ aliases. Matsushima and Shimobaba (2009) cut the spectrum where the local frequency of the phase passes the Nyquist limit. With the frequency spacing $\Delta u = 1/(n d)$ of the (padded) grid along an axis, the condition $|\partial_f \varphi|\, \Delta u \le \pi$ for the phase $\varphi(f) = 2\pi z\sqrt{1/\lambda^2 - f^2}$ gives

$$b = \frac{1}{\lambda\sqrt{(2\Delta u\, z)^2 + 1}},$$

and the [proof](proofs/correctness.md) derives it.

## Example

Take one row of $n = 8$ samples, a field that does not change along $y$, with spacing $d = 1\ \mu\text{m}$, the wavelength $\lambda = 0.5\ \mu\text{m}$, the distance $z = 10\ \mu\text{m}$, and the slit $u = [0, 0, 0, 1, 1, 0, 0, 0]$. The frequencies are $f = \bar k / 8$ per $\mu$m, and all of them are below $1/\lambda = 2$ per $\mu$m, so every wave propagates. The table gives $f_z = \sqrt{1/\lambda^2 - f^2}$ and the phase of $H$ modulo $2\pi$.

| index $k$ | $f$ (1/$\mu$m) | $f_z$ (1/$\mu$m) | $\arg H \bmod 2\pi$ | $\hat u_k$ |
|---|---|---|---|---|
| 0 | 0 | 2.00000 | 0 | 2 |
| 1 | 0.125 | 1.99609 | 6.0375 | $-1.7071 - 0.7071i$ |
| 2 | 0.25 | 1.98431 | 5.2976 | $1 + i$ |
| 3 | 0.375 | 1.96453 | 4.0545 | $-0.2929 - 0.7071i$ |
| 4 | $-0.5$ | 1.93649 | 2.2928 | 0 |
| 5 | $-0.375$ | 1.96453 | 4.0545 | $-0.2929 + 0.7071i$ |
| 6 | $-0.25$ | 1.98431 | 5.2976 | $1 - i$ |
| 7 | $-0.125$ | 1.99609 | 6.0375 | $-1.7071 + 0.7071i$ |

The output intensities $|v_j|^2$ are $[0.0025, 0.0405, 0.2465, 0.7105, 0.7105, 0.2465, 0.0405, 0.0025]$. Their sum is $2$, the energy of the input, because $|H| = 1$ on every wave. The slit has spread to its neighbors. The Fresnel (paraxial) transfer function $e^{2\pi i z/\lambda} e^{-i\pi\lambda z f^2}$ differs from $H$ in phase by $0.00024$ rad at $f = 0.125$ and by $0.063$ rad at $f = 0.5$. The error grows as $f^4$, because the next term of $\sqrt{1 - \lambda^2 f^2}$ after $1 - \lambda^2 f^2/2$ is $-\lambda^4 f^4/8$.

## Correctness

The [proof](proofs/correctness.md) works in the model that the DFT assumes. A *grid field* is a sum of the waves $c_f(z) e^{2\pi i (f_x x + f_y y)}$ over the frequencies of the grid that solves the Helmholtz equation for $z > 0$, has bounded coefficients and has no wave that travels toward $-z$. Put into the Helmholtz equation, each coefficient obeys $c_f'' + 4\pi^2 (1/\lambda^2 - |f|^2) c_f = 0$. So a propagating coefficient is $c_f(0) e^{2\pi i z\sqrt{w_f}}$ and an evanescent one decays as $e^{-2\pi z\sqrt{-w_f}}$. The DFT of the samples gives the coefficients exactly, because each grid frequency has its own DFT index. Hence the output is the exact propagating part of the field at $z$, and the dropped evanescent part is at most $e^{-2\pi z\gamma}$ times its size at $z = 0$, with $\gamma$ the smallest decay rate on the grid.

This is a theorem about the periodic model. For a field in an infinite plane, the method has two errors that the theorem does not cover: the wrap-around of the periodic DFT, which the padding reduces, and the sampling of $H$ at large $z$, which the band limit controls.

## Complexity

In the [real RAM](/real-ram/) model, line L1 and line L7 each cost one 2D DFT. With the [fast Fourier transform](/fast-fourier-transform/) and $n_1 = n_2 = n$ a power of two, that is $O(n^2 \log n)$; with direct sums it is $O(n^4)$, or $O(n^3)$ with row and column transforms done directly. Lines L2 to L6 cost $O(n^2)$, with one square root and one complex exponential per entry. The memory holds two arrays of $n^2$ complex numbers. Padding by a factor two in each direction multiplies the grid by four. The method is not iterative.

## Properties

These follow from the diagonal form of the method in the DFT basis (proved in the [proof](proofs/correctness.md)).

- **Unitary on the propagating band.** $|H| = 1$ where $w > 0$, so the method keeps the energy of every field whose DFT has no evanescent entries. In general it returns the energy of the propagating band, which is at most the input energy.
- **Group property.** Propagation by $z_1$ and then by $z_2$ equals propagation by $z_1 + z_2$.
- **Reversible on the band.** Propagation by $z$ and then by $-z$ keeps the propagating band and deletes the rest. On a grid with $d \ge \lambda/\sqrt{2}$ every grid frequency propagates, and the round trip is the identity.
- **Adjoint.** The adjoint of propagation by $z$ is propagation by $-z$. Iterative methods use this as the exact adjoint of the forward model.
- **No restriction on the distance in the model.** The method needs no paraxial approximation and works at $z$ close to $0$, where the Fresnel transform fails.

## Variants and improvements

- **Band-limited angular spectrum (Matsushima and Shimobaba 2009).** Zero the spectrum outside the band limit $b$ above. This removes the aliasing of the sampled transfer function at long distances, at the cost of a lower resolution there.
- **Fresnel transfer function.** Replace $H$ by $e^{ikz} e^{-i\pi\lambda z (f_x^2 + f_y^2)}$. It is the paraxial approximation and is accurate when $\lambda |f|$ is small for all waves with energy.
- **Fresnel transform with one FFT.** For long distances, the Fresnel integral can be written as one Fourier transform with a quadratic phase factor before and after it. The output grid spacing is then $\lambda z/(n d)$, not $d$. This form is common in digital holography.
- **Shifted and scaled angular spectrum.** Variants change the output window or its sampling, for example to propagate to a tilted or offset plane. They are outside this page.
- **Nonuniform output.** With a [nonuniform FFT](/nonuniform-fft/), the plane waves can be summed on a grid that differs from the input grid.

## When to use it

Use the angular spectrum method to propagate a coherent field over short and middle distances, where the field stays mostly inside the window: refocusing in [digital holography](/digital-holography-reconstruction/), defocus series for the [transport of intensity equation](/transport-of-intensity-equation/), the near field step of [ptychography](/ptychography/), and the simulation of diffraction. It keeps the grid spacing, which makes it the natural choice when the input and output planes must line up pixel by pixel. For the far field, a single Fourier transform (the Fraunhofer approximation) is cheaper and keeps the sampling right. For long distances in the near field, use the band limit or the Fresnel transform.

## Pitfalls

- **Wrap-around.** Without padding, light that leaves the window at one side enters at the other. The result is the field of a periodic array of copies of the object.
- **Aliasing of the transfer function.** At large $z$ the phase of $H$ varies by more than $\pi$ between frequency samples. The sampled $H$ then describes the wrong field, often with ghost copies. The band limit, or a Fresnel transform, avoids this.
- **The sign convention.** With the time dependence $e^{+i\omega t}$, used in some engineering books, the forward transfer function is $e^{-2\pi i z\sqrt{\cdot}}$. Mixing conventions propagates the field the wrong way.
- **The frequency grid.** For even $n$, the index $n/2$ stands for the frequency $-n/(2 n d)$, not $+n/(2nd)$. An off-by-one in the mapping of line L3 gives a wrong $H$ that still has modulus 1, so energy checks do not catch it.
- **Evanescent waves in back propagation.** Do not multiply by $e^{+2\pi z\sqrt{-w}}$ to undo the decay. That amplifies noise without limit, which is an ill-posed step; line L6 sets these waves to zero in both directions.
- **Scalar model.** The method propagates one scalar component. It ignores the coupling of polarization components, which matters at high numerical aperture.

## Implementations

## History

The representation of a monochromatic field by plane waves, and its propagation by the transfer function of free space, is classical in scalar diffraction theory; Goodman gives it in the chapter on the foundations of scalar diffraction theory. Schnars and Juptner (1994) recorded a hologram on a CCD and reconstructed it by numerical propagation, which made numerical propagation the core of digital holography. Matsushima and Shimobaba (2009) analyzed the sampling of the transfer function and introduced the band limit that extends the method to longer distances.

## References
