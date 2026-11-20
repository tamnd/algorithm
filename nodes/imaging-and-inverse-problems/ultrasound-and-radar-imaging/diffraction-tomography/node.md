---
tag: X0C2PM
kind: technique
slug: diffraction-tomography
name: Diffraction tomography
aliases:
- Fourier diffraction theorem
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Under the Born approximation the scattered field of each plane wave gives the object Fourier transform on an arc, which a Fourier method can invert."
history:
  year: 1969
  people: [Emil Wolf]
  note: "Wolf (1969) showed that, under the first Born approximation, holographic data of the scattered field give the three-dimensional Fourier transform of a weakly scattering object on a sphere. Mueller, Kaveh and Wade (1979) applied the idea to ultrasound, and Devaney (1982) gave the filtered backpropagation algorithm."
prereqs: [fourier-slice-theorem, wave-equation]
see_also: [photoacoustic-tomography, filtered-back-projection, direct-fourier-reconstruction, nonuniform-fft, angular-spectrum-method, tomographic-reconstruction-problem, digital-holography-reconstruction, phase-retrieval]
sources:
  - paper: doi:10.1016/0030-4018(69)90052-2
    title: "Emil Wolf, Three-dimensional structure determination of semi-transparent objects from holographic data, Optics Communications 1(4), 1969, 153"
    locator: "the Fourier transform of the object on a sphere from the scattered field, under the first Born approximation (general locator)"
  - paper: doi:10.1109/PROC.1979.11284
    title: "R. K. Mueller, M. Kaveh and G. Wade, Reconstructive tomography and applications to ultrasonics, Proceedings of the IEEE 67(4), 1979, 567"
    locator: "diffraction tomography for ultrasound (general locator)"
  - paper: doi:10.1177/016173468200400404
    title: "A. J. Devaney, A filtered backpropagation algorithm for diffraction tomography, Ultrasonic Imaging 4(4), 1982, 336"
    locator: "the filtered backpropagation algorithm (general locator)"
  - paper: doi:10.1109/TASSP.1983.1164196
    title: "S. X. Pan and A. C. Kak, A computational study of reconstruction algorithms for diffraction tomography: interpolation versus filtered backpropagation, IEEE Transactions on Acoustics, Speech, and Signal Processing 31(5), 1983, 1262"
    locator: "comparison of Fourier interpolation and filtered backpropagation (general locator)"
  - paper: doi:10.1109/TMTT.1984.1132783
    title: "Malcolm Slaney, Avinash C. Kak and Lawrence E. Larsen, Limitations of imaging with first-order diffraction tomography, IEEE Transactions on Microwave Theory and Techniques 32(8), 1984, 860"
    locator: "the limits of the Born and Rytov approximations (general locator)"
  - book: isbn:9780898714944
    title: "A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001"
    locator: "Chapter 6 (tomographic imaging with diffracting sources)"
---

Diffraction tomography reconstructs a weakly scattering object from the waves it scatters when plane waves from many directions pass through it. It is the version of computed tomography for wavelengths that are not small compared with the details of the object, as in ultrasound, microwaves and optical microscopy. There the waves bend around the object, and straight rays are a poor model. Under the first Born approximation the scattered field is linear in the object. The Fourier transform of the field measured on a line behind the object gives the Fourier transform of the object on a circular arc through the origin (Wolf 1969; Kak and Slaney, Chapter 6). In 3D the arc is a cap of a sphere. As the direction of the incident wave turns, the arcs fill a disk, and the object follows by interpolation onto a grid and an inverse FFT, or by the filtered backpropagation of Devaney (1982). When the wavelength goes to zero, the arcs become straight lines and the method becomes the [Fourier slice theorem](/fourier-slice-theorem/) of straight ray tomography.

## In plain words

In X-ray CT the rays go straight through the body, and each view gives one straight line through the centre of the Fourier transform of the image. Sound and microwaves do not go straight: they bend and spread around the details.

If the object changes the wave only a little, the part of the wave that it scatters is a sum of small waves from every point of the object. Measure that part along a line behind the object and take its Fourier transform. Each frequency of the measurement tells you one frequency of the object, but these frequencies lie on a circle and not on a line. Turn the source around the object, collect all the circles, and put them together to rebuild the object.

## When it applies

- **Coherent waves of one frequency** with a known wavenumber $k_0 = 2\pi / \lambda$ in the background medium. Broadband data are processed one frequency at a time.
- **Weak scattering.** The first Born approximation needs a small total phase shift through the object. The Rytov approximation allows larger objects with small changes of the refractive index (Slaney, Kak and Larsen 1984 study both limits).
- **Measured amplitude and phase** of the field on a line (2D) or a plane (3D) behind the object, for many directions of incidence.
- **Known incident field.** The scattered field is the total field minus the field without the object.

Under these conditions, the theorem below links the data to the object.

### The key theorem

**Model.** In 2D, the field $u$ solves $(\nabla^2 + k_0^2)\, u = -o(r)\, u$ with the object function $o(r) = k_0^2 (n(r)^2 - 1)$, where $n$ is the refractive index relative to the background. The incident field is the plane wave $u_0 = e^{i k_0 y}$, and the scattered field is $u_s = u - u_0$.

**Born approximation.** Replace $u$ by $u_0$ on the right. Then $u_s(r) = \int g(r - r')\, o(r')\, u_0(r')\, dr'$ with the Green's function $g(r) = \frac{i}{4} H_0^{(1)}(k_0 |r|)$ of the Helmholtz equation.

**Theorem.** Let $O(K) = \int o(r)\, e^{-i K \cdot r}\, dr$ and let $U_s(\alpha) = \int u_s(x, l)\, e^{-i \alpha x}\, dx$ be the Fourier transform of the scattered field on the line $y = l$, beyond the object. For $|\alpha| < k_0$ and $\gamma = \sqrt{k_0^2 - \alpha^2}$,

$$U_s(\alpha) = \frac{i}{2\gamma}\, e^{i \gamma l}\, O(\alpha,\, \gamma - k_0).$$

The points $(\alpha, \gamma - k_0)$ lie on the circle of radius $k_0$ centred at $(0, -k_0)$: an arc that passes through the origin.

*Proof.* The plane wave expansion of the Green's function is $g(x, y) = \frac{i}{4\pi} \int \frac{1}{\gamma}\, e^{i(\alpha x + \gamma |y|)}\, d\alpha$, with $\gamma$ imaginary and of positive imaginary part for $|\alpha| > k_0$. Insert it into the Born formula with $y = l > y'$:

$$u_s(x, l) = \frac{i}{4\pi} \int \frac{1}{\gamma}\, e^{i \alpha x + i \gamma l} \int o(x', y')\, e^{-i(\alpha x' + (\gamma - k_0) y')}\, dx'\, dy'\, d\alpha = \frac{1}{2\pi} \int \frac{i}{2\gamma}\, e^{i \gamma l}\, O(\alpha, \gamma - k_0)\, e^{i \alpha x}\, d\alpha.$$

The right side is an inverse Fourier transform in $x$, which gives the formula. $\square$

The Fourier sign here is $e^{-i K \cdot r}$ with the angular frequency $K = 2\pi \xi$, the convention $e^{-2\pi i x \cdot \xi}$ of the encyclopedia. For $|\alpha| > k_0$ the factor $e^{i\gamma l}$ decays: those components are evanescent and do not reach the detectors.

## The template

```pseudo id=main
DIFFRACTION-TOMOGRAPHY(u for each view φ, k0, l)
L1  for each direction φ of the incident wave
L2      u_s ← u - u_0                         ▷ Born; Rytov: u_0 ln(u / u_0)
L3      U_s(α) ← FFT of u_s along the detector line
L4      for each α with |α| < k0
L5          γ ← sqrt(k0² - α²)
L6          K ← α t(φ) + (γ - k0) s(φ)        ▷ s: direction of the wave, t: the detector line
L7          O(K) ← (2γ / i) e^(-i γ l) U_s(α)
L8  put the values on the arcs onto a Cartesian grid   ▷ hole: interpolation or filtered backpropagation
L9  o ← inverse 2D FFT of O
L10 return n ← sqrt(1 + o / k0²)
```

Lines L4 to L7 apply the theorem to one view, rotated so that the wave travels along $s(\varphi)$. Line L8 is the hard part. The samples lie on arcs, densely near the origin and sparsely far from it. Interpolation onto a grid is fast but its errors spread over the whole image (Pan and Kak 1983). Filtered backpropagation (Devaney 1982) instead filters each view and propagates it back into the object along the field of the wave, the analogue of [filtered back-projection](/filtered-back-projection/). A [nonuniform FFT](/nonuniform-fft/) is a modern way to do line L8.

## Classic examples

**Coverage of the Fourier plane.** For transmission data from all directions $\varphi$ in $[0, 2\pi)$, the arcs fill the disk $|K| \le \sqrt{2}\, k_0$. A detector line on the same side as the source records reflection data, which lie on the other half of each circle and reach $|K| = 2 k_0$. Ultrasound at 5 MHz in water ($c = 1540$ m/s) has $\lambda = 0.308$ mm and $k_0 = 20.4$ rad/mm, so transmission data reach $|K| = 28.8$ rad/mm.

**A point scatterer.** For $o(r) = \sigma \delta(r)$, $O(K) = \sigma$ for all $K$, and the theorem gives $U_s(\alpha) = \frac{i \sigma}{2 \gamma} e^{i \gamma l}$, the plane wave expansion of the cylindrical wave $\sigma g(x, l)$. The data of every view are the same up to rotation, and the reconstruction is the point blurred by the disk of coverage.

**The limit of short waves.** As $k_0 \to \infty$ with $\alpha$ fixed, $\gamma - k_0 \to 0$, and the arc becomes the straight line $K = \alpha\, t(\varphi)$ through the origin. This is the Fourier slice theorem of X-ray CT, and filtered backpropagation becomes filtered back-projection.

**Ultrasound computed tomography.** Ring and cylindrical arrays around the breast record transmission data at many frequencies. Diffraction tomography gives the speed of sound and attenuation at a higher resolution than straight ray methods.

**Optical diffraction tomography.** Holographic microscopes measure the field of a cell for many directions of illumination and reconstruct its 3D refractive index on spherical caps, as in Wolf's original setting.

## Variations

- **Rytov approximation.** Use the complex phase $u_0 \ln(u / u_0)$ in place of $u - u_0$. It allows objects much larger than the wavelength if the index changes slowly.
- **Three dimensions.** The arcs become spherical caps of radius $k_0$, and the data come from holograms on a plane.
- **Filtered backpropagation** (Devaney 1982) instead of Fourier interpolation.
- **Broadband data.** Several frequencies give arcs of several radii and fill the Fourier plane with fewer views.
- **Distorted Born iterations and full waveform inversion** drop the weak scattering assumption by solving the nonlinear problem iteratively.
- **Limited angle and reflection geometries,** where the coverage of the Fourier plane has gaps that a prior must fill.

## Pitfalls

- **Strong scattering.** The Born approximation fails when the phase shift through the object is more than a fraction of a turn. The reconstruction then shrinks or rings, and refining the data does not help.
- **Phase errors.** The method needs the phase of the field. A drift of the source phase between views, or an error in $l$, rotates the data on each arc. Measure or calibrate the incident field.
- **Evanescent components.** The factor $1/\gamma$ grows near $|\alpha| = k_0$, and noise there is amplified. Use a window that goes to zero at the edge of the arc.
- **Uneven sampling.** The arcs cross near the origin, where the samples are dense, and spread apart at large $|K|$. Simple nearest neighbour interpolation onto a grid gives strong artefacts. Use a density weight and a good interpolator.
- **Wrong background.** $k_0$ and the incident field must be those of the background medium, such as water at the right temperature.

## Exercises

1. Show that the points $(\alpha, \sqrt{k_0^2 - \alpha^2} - k_0)$ lie on the circle of radius $k_0$ centred at $(0, -k_0)$, and find where the arc ends for $|\alpha| \to k_0$.
2. Show that the arcs of transmission data from all directions fill exactly the disk $|K| \le \sqrt{2}\, k_0$.
3. Expand $\gamma - k_0$ for $|\alpha| \ll k_0$ and show how far the arc is from the straight slice of X-ray CT at the frequency $\alpha$.
4. For a cylinder of radius $a$ with a constant index $n$, estimate the phase shift of the wave through its centre, and find the largest $a$ for a phase shift of $\pi/2$ at 5 MHz with $n = 1.02$.
5. Why does a source and detector pair on the same side of the object give information at higher spatial frequencies than transmission data?

## References
