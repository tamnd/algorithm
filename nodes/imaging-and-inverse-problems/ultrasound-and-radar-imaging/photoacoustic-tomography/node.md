---
tag: 7F3QQT
kind: problem
slug: photoacoustic-tomography
name: Photoacoustic tomography
aliases:
- optoacoustic tomography
- thermoacoustic tomography
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: Recover the initial pressure that a laser pulse makes in tissue from the acoustic waves recorded on a surface around it.
model: real-ram
prereqs: [wave-equation, radon-transform]
see_also: [universal-back-projection, tomographic-reconstruction-problem, delay-and-sum-beamforming, diffraction-tomography, filtered-back-projection, beamforming, pulse-echo-imaging, perfectly-matched-layer]
sources:
  - paper: doi:10.1017/S0956792508007353
    title: "Peter Kuchment and Leonid Kunyansky, Mathematics of thermoacoustic tomography, European Journal of Applied Mathematics 19(2), 2008, 191"
    locator: "the model with zero initial velocity, the spherical mean transform, uniqueness, stability, inversion formulas and limited data (general locator)"
  - paper: doi:10.1063/1.2195024
    title: "Minghua Xu and Lihong V. Wang, Photoacoustic imaging in biomedicine, Review of Scientific Instruments 77, 2006, 041101"
    locator: "the physics of photoacoustic generation and a review of reconstruction methods (general locator)"
  - paper: doi:10.1103/PhysRevE.71.016706
    title: "Minghua Xu and Lihong V. Wang, Universal back-projection algorithm for photoacoustic computed tomography, Physical Review E 71, 2005, 016706"
    locator: "a back-projection formula exact for spherical, cylindrical and planar surfaces (general locator)"
  - paper: doi:10.1137/S0036141002417814
    title: "David Finch, Sarah K. Patch and Rakesh, Determining a function from its mean values over a family of spheres, SIAM Journal on Mathematical Analysis 35(5), 2004, 1213"
    locator: "uniqueness and exact inversion formulas for spherical means centred on a sphere in odd dimensions (general locator)"
  - paper: doi:10.1137/070682137
    title: "David Finch, Markus Haltmeier and Rakesh, Inversion of spherical means and the wave equation in even dimensions, SIAM Journal on Applied Mathematics 68(2), 2007, 392"
    locator: "exact inversion formulas in even dimensions (general locator)"
  - paper: doi:10.1088/0266-5611/23/1/021
    title: "Leonid A. Kunyansky, Explicit inversion formulae for the spherical mean Radon transform, Inverse Problems 23(1), 2007, 373"
    locator: "explicit inversion formulas for the sphere (general locator)"
  - paper: doi:10.1088/0266-5611/24/5/055006
    title: "Yulia Hristova, Peter Kuchment and Linh Nguyen, Reconstruction and time reversal in thermoacoustic tomography in acoustically homogeneous and inhomogeneous media, Inverse Problems 24(5), 2008, 055006"
    locator: "time reversal reconstruction for constant and variable speed of sound (general locator)"
---

Photoacoustic tomography (PAT) is the problem of recovering the initial pressure $p_0(x)$ that a short pulse of light creates in tissue, from the sound waves that this pressure sends to detectors outside the tissue. Light absorbed in a few nanoseconds heats the tissue a little and makes it expand, so $p_0$ is proportional to the absorbed energy, which shows blood vessels and other strong absorbers with optical contrast at ultrasound resolution. When the pulse is a microwave pulse, the same problem is called thermoacoustic tomography. Mathematically, the data are the values on a surface of the solution of the [wave equation](/wave-equation/) with initial value $p_0$ and zero initial velocity, or equivalently the means of $p_0$ over spheres centred on that surface (Kuchment and Kunyansky 2008). With a closed surface and a constant speed of sound the problem has a unique and stable solution and exact formulas such as [universal back-projection](/universal-back-projection/). With a partial surface, a variable speed of sound or attenuation it becomes harder.

## In plain words

Flash a very short pulse of light into tissue. The parts that absorb more light, such as blood, warm up a little more and expand, and each of them becomes a small source of sound. Microphones around the tissue record the sound.

The problem is to work back from the recordings to the map of the sources. Sound from a source at distance $r$ reaches a microphone after the time $r/c$. So each moment of a recording is the sum of all sources on a sphere around the microphone. With microphones all around, these sums over spheres pin down every source. This is like a CT scan, with spheres in place of straight lines.

## Definition

**Model.** The initial pressure $p_0$ is smooth with compact support in a region $\Omega$. The speed of sound $c$ is known, usually taken constant ($c = 1540$ m/s is the usual soft tissue convention). The pressure solves

$$p_{tt} = c^2 \Delta p \quad \text{in } \mathbb{R}^d \times (0, \infty), \qquad p(x, 0) = p_0(x), \qquad p_t(x, 0) = 0.$$

The zero initial velocity comes from the short pulse: the tissue is heated before it has time to move.

**Data.** $g(z, t) = p(z, t)$ for $z$ on a detection surface $S$ outside $\Omega$ and $0 \le t \le T$.

**Task.** Find $p_0$ from $g$.

**Spherical means.** In three dimensions, $p(z, t) = \partial_t \big(t\, M p_0(z, ct)\big)$, where $M p_0(z, \rho)$ is the mean of $p_0$ over the sphere of radius $\rho$ about $z$. So the data determine, and are determined by, the spherical means of $p_0$ centred on $S$, the spherical mean Radon transform.

## Variants

- **Closed surface or partial surface.** A sphere, a cylinder or a plane around the object, or only part of one (limited view).
- **Dimension.** 3D with point detectors, or 2D with line detectors that integrate the pressure along a line, or a 2D slice with focused detectors. In even dimensions the wave has a tail, and the inversion formulas differ.
- **Variable speed of sound.** $c(x)$ known but not constant, as in breast imaging.
- **Attenuation and finite detector bandwidth.** The data are filtered versions of $g$.
- **Quantitative PAT.** The next step: recover the optical absorption from $p_0$, which is the absorption times the light fluence times a conversion factor.
- **Thermoacoustic tomography.** The same problem with microwave or radio frequency heating.

## Examples

**A uniform ball.** Let $p_0 = 1$ in a ball of radius $a$ and 0 outside, in 3D. At the distance $r > a$ from its centre, the pressure is

$$p(r, t) = \frac{r - ct}{2r} \quad \text{for } |r - ct| < a, \qquad 0 \text{ otherwise}.$$

With $a = 1$ mm, $r = 10$ mm and $c = 1.54$ mm/µs, the detector sees an N-shaped pulse that falls linearly from $+0.05$ to $-0.05$ between $t = 5.84$ µs and $t = 7.14$ µs. The amplitude falls as $1/r$, the duration $2a/c$ gives the size of the ball, and the arrival time $r/c$ gives its distance. The sharp edges of the N come from the sharp edge of the ball.

**A Gaussian ball.** For $p_0 = \exp(-|x|^2/(2 s^2))$, the pressure at distance $r$ is $\big((r - ct) g(r - ct) + (r + ct) g(r + ct)\big)/(2r)$ with $g(u) = e^{-u^2/(2s^2)}$, a smooth N. The page on universal back-projection uses it to check that the reconstruction is exact.

**Limited view.** With detectors on only the upper half of a sphere, the edges of an object whose normals do not point toward any detector are blurred in every reconstruction. In the test of the universal back-projection page, the value at the centre of a Gaussian ball becomes 0.577 instead of 1.

## Known algorithms

| Method | Geometry | Exact | Cost |
|---|---|---|---|
| [Universal back-projection](/universal-back-projection/) (Xu and Wang 2005) | sphere, cylinder, plane in 3D | yes in 3D | $O(V D)$ |
| Inversion formulas of Finch, Patch and Rakesh (2004) | sphere, odd dimensions | yes | $O(V D)$ |
| Formulas of Finch, Haltmeier and Rakesh (2007) | sphere, even dimensions | yes | more than $O(V D)$, with an integral over time |
| Formulas of Kunyansky (2007) | sphere | yes | $O(V D)$ |
| Fourier methods | plane | yes, for full data | $O(n^3 \log n)$ with the FFT and interpolation |
| Time reversal (Hristova, Kuchment and Nguyen 2008) | any closed surface, variable $c$ | yes in 3D with constant $c$; approximate otherwise | a wave solver |
| [Delay and sum](/delay-and-sum-beamforming/) | any | no | $O(V D)$ |
| Model based iterative methods | any, with noise and filters | no closed form | iterative |

Here $V$ is the number of image points and $D$ the number of detectors; for $n^3$ voxels and $n^2$ detectors, $O(V D) = O(n^5)$.

## Bounds

- **Uniqueness** (theorem). For a closed surface around the support and a constant speed, the data determine $p_0$ (Finch, Patch and Rakesh 2004; Kuchment and Kunyansky 2008 survey this and the more general cases).
- **Stability** (theorem, surveyed by Kuchment and Kunyansky 2008). With a closed surface the inversion is about as stable as the inversion of the [Radon transform](/radon-transform/). With limited view, the parts of the boundaries of objects that are not seen at a normal direction from some detector cannot be recovered stably.
- **Record length.** In 3D with a constant speed, the pressure inside a sphere of radius $R$ is zero after $2R/c$ (Huygens' principle), so a record of that length holds all the information. In 2D the wave has a tail, and every finite record cuts it.
- **Cost.** Reading the data takes $\Omega(D T)$ for $T$ time samples per detector.

## Reductions

**To the spherical mean transform.** In 3D, $p = \partial_t (t\, M p_0(\cdot, ct))$, and the map from $t M p_0$ to $p$ is invertible by integration in time, because $t M p_0$ is zero at $t = 0$. So PAT with point detectors is the inversion of the spherical mean transform with centres on $S$.

**To the Radon transform.** When the detectors are far from the object compared with its size, the spheres through the object are almost planes, and the spherical means become plane integrals: PAT tends to the inversion of the 3D [Radon transform](/radon-transform/). Back-projection along spheres is then the analogue of [filtered back-projection](/filtered-back-projection/).

**To a boundary value problem.** Time reversal solves the wave equation backward from $t = T$ with zero data inside and the measured $g$ as boundary values on $S$. In 3D with a constant speed and $T \ge 2R/c$ this gives $p_0$ exactly.

**Compared with diffraction tomography.** In [diffraction tomography](/diffraction-tomography/) a known incident wave scatters from the object. In PAT the object itself is the source. Both are inverse problems for the wave equation, but PAT is linear without any approximation, while diffraction tomography is linear only under the Born or Rytov approximation.

## Applications

- **Preclinical imaging** of small animals: the vascular system, tumours and the brain.
- **Breast imaging** with hemispherical or ring arrays of detectors.
- **Photoacoustic microscopy** of blood vessels and of the oxygen saturation of blood, which needs several wavelengths of light.
- **Thermoacoustic imaging** with microwave heating, with the contrast of the electrical conductivity.
- **Hybrid ultrasound systems** that use the same array for pulse echo images and for photoacoustic images.

## References
