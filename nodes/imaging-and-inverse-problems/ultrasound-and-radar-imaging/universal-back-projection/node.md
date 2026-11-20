---
tag: 4TK0K9
kind: algorithm
slug: universal-back-projection
name: Universal back-projection
aliases:
- Xu-Wang back-projection
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Reconstruct photoacoustic images by back-projecting b = 2p - 2t dp/dt, which combines the pressure and its time derivative, with solid angle weights. Exact for a sphere, cylinder or plane in 3D."
solves: [photoacoustic-tomography]
model: real-ram
complexity:
  vars: {D: the number of detectors, T: the number of time samples per detector, V: the number of image points}
  time: {worst: O(D T + V D)}
  space: {extra: O(D T)}
properties: {deterministic: true, recursive: false, exact: true, linear_in_data: true}
history:
  year: 2005
  people: [Minghua Xu, Lihong V. Wang]
  note: "Xu and Wang (2005) derived one back-projection formula for the sphere, the infinite cylinder and the infinite plane. Finch, Patch and Rakesh (2004) had proved exact inversion formulas for the sphere in odd dimensions."
prereqs: [photoacoustic-tomography, wave-equation, back-projection-operator]
see_also: [filtered-back-projection, delay-and-sum-beamforming, radon-transform, fourier-slice-theorem, gauss-legendre-quadrature, total-focusing-method, diffraction-tomography, beamforming]
sources:
  - paper: doi:10.1103/PhysRevE.71.016706
    title: "Minghua Xu and Lihong V. Wang, Universal back-projection algorithm for photoacoustic computed tomography, Physical Review E 71, 2005, 016706"
    locator: "the back-projection term b = 2p - 2t dp/dt, the solid angle weights, and exactness for spherical, cylindrical and planar surfaces (general locator)"
  - paper: doi:10.1137/S0036141002417814
    title: "David Finch, Sarah K. Patch and Rakesh, Determining a function from its mean values over a family of spheres, SIAM Journal on Mathematical Analysis 35(5), 2004, 1213"
    locator: "exact inversion formulas for spherical means centred on a sphere in odd dimensions (general locator)"
  - paper: doi:10.1137/070682137
    title: "David Finch, Markus Haltmeier and Rakesh, Inversion of spherical means and the wave equation in even dimensions, SIAM Journal on Applied Mathematics 68(2), 2007, 392"
    locator: "exact inversion formulas for the sphere in even dimensions, including 2D (general locator)"
  - paper: doi:10.1088/0266-5611/23/1/021
    title: "Leonid A. Kunyansky, Explicit inversion formulae for the spherical mean Radon transform, Inverse Problems 23(1), 2007, 373"
    locator: "inversion formulas for the sphere in divergence form (general locator)"
  - paper: doi:10.1017/S0956792508007353
    title: "Peter Kuchment and Leonid Kunyansky, Mathematics of thermoacoustic tomography, European Journal of Applied Mathematics 19(2), 2008, 191"
    locator: "survey of the model with zero initial velocity, uniqueness, inversion formulas and limited data (general locator)"
  - paper: doi:10.1063/1.2195024
    title: "Minghua Xu and Lihong V. Wang, Photoacoustic imaging in biomedicine, Review of Scientific Instruments 77, 2006, 041101"
    locator: "review of photoacoustic reconstruction methods including back-projection (general locator)"
---

Universal back-projection reconstructs the initial pressure $p_0$ of [photoacoustic tomography](/photoacoustic-tomography/) from the pressure $p(r_0, t)$ that point detectors record on a surface around the object. Each detector signal is turned into the back-projection term $b = 2p - 2t\, \partial p / \partial t$, which combines the pressure and its time derivative. Each image point then sums $b$ at the time of flight from every detector, weighted by the solid angle under which the point sees that detector element. Xu and Wang (2005) showed that this one formula is exact in three dimensions for a sphere, an infinite cylinder and an infinite plane, hence the name "universal". The cost is that of a [back-projection](/back-projection-operator/): $O(V D)$ for $V$ image points and $D$ detectors, with no filter in the Fourier domain. In two dimensions the same formula is only approximate. Exact formulas for even dimensions have a different form (Finch, Haltmeier and Rakesh 2007).

## In plain words

A short laser pulse heats the tissue a little, and every absorbing spot becomes a small source of sound. Detectors around the tissue record the sound for a short time.

To find the strength of the source at one point, look at each detector at the moment the sound from that point arrived there. Take twice the signal minus twice the time multiplied by the slope of the signal. Add these numbers over all the detectors, weighted by how large each detector looks from the point, and divide by the full solid angle. On a closed sphere, the parts that come from other points cancel exactly, and only the source at that point is left.

## The problem

**Model.** The initial pressure $p_0$ has compact support inside the detection surface. The pressure $p(x, t)$ solves the [wave equation](/wave-equation/) $p_{tt} = c^2 \Delta p$ with $p(x, 0) = p_0(x)$ and zero initial velocity $p_t(x, 0) = 0$. The speed $c$ is known and constant; the code uses $c = 1.54$ mm/µs, the usual soft tissue convention of 1540 m/s.

**Input.** Samples $p(r_0, t_k)$, $t_k = k\, \Delta t$, at $D$ point detectors on a surface $S$. Each detector has the position $r_0$, the unit normal $n_0$ that points toward the object, and the area $dS_0$ of its surface element. The record must last until the sound from the far side has passed, $2R/c$ for a sphere of radius $R$.

**Output.** $p_0(r)$ at $V$ image points inside $S$.

**Formula.** With the solid angle element $d\Omega_0 = dS_0\, n_0 \cdot (r - r_0) / |r - r_0|^3$ and the solid angle $\Omega_0$ of the whole surface seen from $r$ ($4\pi$ for a sphere or a cylinder, $2\pi$ for a plane),

$$p_0(r) = \frac{1}{\Omega_0} \int_S b\Big(r_0, \frac{|r - r_0|}{c}\Big)\, d\Omega_0, \qquad b(r_0, t) = 2p(r_0, t) - 2t\, \frac{\partial p(r_0, t)}{\partial t}.$$

## The algorithm

```pseudo id=main
UBP(p, detectors, Δt, c, points)
L1  for each detector d: compute b_d from p_d
L2      b_d(t_k) ← 2 p_d(t_k) - 2 t_k (p_d(t_{k+1}) - p_d(t_{k-1})) / (2Δt)
L3  for each image point r
L4      for each detector d with position r0, normal n0 and area a
L5          dΩ ← a n0·(r - r0) / |r - r0|^3
L6          sum ← sum + dΩ · b_d(|r - r0| / c)       ▷ linear interpolation in t
L7          Ω ← Ω + dΩ
L8      p0(r) ← sum / Ω                            ▷ or sum / Ω0
L9  return p0
```

Line L2 uses the central difference inside the record and one sided differences at its two ends, where the signal is zero. Line L6 reads $b_d$ at the time of flight and interpolates linearly between samples; outside the record it uses zero. Line L8 divides by the sum of the solid angle elements. For a point inside a closed surface that sum is $4\pi$ up to the quadrature error, so the result is the same, and the division corrects part of the quadrature error. For a partial surface the choice matters (see Pitfalls).

The code places the detectors on a sphere at the nodes of a [Gauss-Legendre rule](/gauss-legendre-quadrature/) in $\cos\theta$ times a uniform rule in the azimuth, and uses the weights of that product rule as the areas.

## Example

**A ball at the centre, by hand.** Let $p_0(x) = \exp(-|x|^2 / (2 s^2))$ with $s = 0.8$ mm, a sphere of radius $R = 10$ mm and $c = 1.54$ mm/µs. The wave of a radial initial pressure has a closed form, and at a detector at distance $R$ it is

$$p(R, t) = \frac{(R - ct)\, g(R - ct) + (R + ct)\, g(R + ct)}{2R}, \qquad g(u) = e^{-u^2 / (2s^2)}.$$

For the image point at the centre, every detector is at the distance $R$, so line L6 reads every signal at $t = R/c = 6.494$ µs. There $p = 1.9 \times 10^{-136}$, practically zero, and $\partial p / \partial t = -c/(2R) = -0.077$ per µs. So $b = 0 - 2 \cdot 6.494 \cdot (-0.077) = 1.000$ at every detector. The solid angle elements sum to $4\pi$, and line L8 gives $p_0(0) = 1$, the true value. All the information comes from the derivative term, because the pressure itself is zero at that time.

**A ball away from the centre.** Move the centre of the ball to $(2, -1, 1.5)$ mm and use 800 detectors (20 rings by 40 azimuths). With the exact $b$ from the closed form, the reconstruction at the centre of the ball, at $(2.5, -1, 1.5)$ and at $(3, 0, 1)$ matches the true values 1, 0.8226 and 0.1724 to $10^{-15}$. With sampled data and central differences at $\Delta t = 0.02$ µs, the value at the centre of the ball is 0.9989, and at $\Delta t = 0.04$ µs it is 0.9956: the error falls by 4 when the step is halved. Dropping the term $2p$ and keeping only $-2t\, \partial p / \partial t$ changes the value at $(2.5, -1, 1.5)$ by 0.004.

## Correctness

The proof in proofs/correctness.md covers the sphere in three dimensions. Exactness for the cylinder and the plane is stated by Xu and Wang (2005) and is not proved there.

1. **Divergence form** (theorem). With $q = p/t$, $b = -2t^2\, \partial_t q$, and $b\, d\Omega_0 = 2\, n \cdot \nabla_r [q(r_0, |r - r_0|/c)]\, dS_0$ with the outward normal $n$. So the formula is $\frac{1}{2\pi} \operatorname{div}_r \int_S n\, q\, dS_0$, the form of the formulas of Kunyansky (2007).
2. **Frequency form of the data** (theorem). The sine and cosine transforms of the signal at $r_0$ are integrals of $p_0$ against $\cos(k|y - r_0|)/|y - r_0|$ and $\sin(k|y - r_0|)/|y - r_0|$.
3. **The sphere identity** (theorem). After integration over the sphere, the expansion of these kernels in spherical Bessel functions leaves the Wronskian $j_l y_l' - j_l' y_l = 1/(kR)^2$ in every term. The kernel becomes $\sin(k|r - y|)/|r - y|$, and the integral over $k$ is the Fourier inversion formula, so the formula returns $p_0(r)$.
4. **Sampling** (theorem). The central difference and the linear interpolation each add an error of order $\Delta t^2$ to $b$, so the sampled algorithm converges as $\Delta t^2$. The quadrature over the sphere adds a further error that is spectrally small for smooth signals (measurement: $10^{-15}$ with 800 detectors for the ball).

## Complexity

In the real-RAM model, line L2 costs $O(1)$ per sample, $O(D T)$ in total. Lines L4 to L7 cost $O(1)$ per point and detector, $O(V D)$ in total. The array of $b$ needs $O(D T)$ space. For a volume of $V = n^3$ voxels and $D = n^2$ detectors this is $O(n^5)$, the cost of a back-projection. Fast methods based on the [nonuniform FFT](/nonuniform-fft/) or on series expansions for special geometries reduce it.

## Properties

- **Exact on the sphere in 3D** (theorem), for smooth $p_0$ with support inside the sphere. Exact for the infinite cylinder and plane (theorem of Xu and Wang 2005, not proved here).
- **Approximate in 2D** (stated in the literature, not proved here). In 2D the wave has a tail, and the exact formulas of Finch, Haltmeier and Rakesh (2007) involve an integral over all later times.
- **No Fourier filter.** The only filtering is the time derivative in $b$, a local operation. This is what makes the method fast and simple to implement on any detector layout.
- **Linear in the data.** The map from the data to the image is linear.
- **Both terms matter** (measurement). Far from the detectors ($c t \gg$ the wavelength) the term $-2t\, \partial p / \partial t$ dominates and the term $2p$ is a small correction. In the example the term $2p$ changes the value by 0.004.
- **Convergence in $\Delta t^2$** (theorem and measurement).

## Variants and improvements

- **Far field form.** Dropping $2p$ gives $b \approx -2t\, \partial p / \partial t$, the form of many earlier back-projection methods, valid when the detector is many wavelengths from the source.
- **Other exact formulas for the sphere.** Finch, Patch and Rakesh (2004) proved exact formulas in odd dimensions, and Kunyansky (2007) found a family of formulas in divergence form. Item 1 of the correctness section shows that universal back-projection on the sphere can be written in that form.
- **Even dimensions.** For line detectors, which integrate the pressure along a line and reduce the problem to 2D, use the formulas of Finch, Haltmeier and Rakesh (2007) instead of the 2D form of this method.
- **Time reversal.** Solve the wave equation backward in time with the measured data as boundary values. It works for any closed surface and for a variable speed of sound, at the cost of a full wave solver.
- **Iterative and model based methods** handle limited view, a variable speed of sound, the detector size and the bandwidth of the detector.
- **Weighting for partial surfaces.** Dividing by the sum of the solid angles that the detectors actually cover, as in line L8, partly corrects for missing parts of the surface.

## When to use it

Use it when the detectors surround the object well on a sphere, a long cylinder or a large plane, the speed of sound is close to constant, and a fast direct method is needed, for example as the first image of an iterative method. Do not use it as an exact method in 2D, with a strongly varying speed of sound, or with a small aperture. Use time reversal or an iterative method there.

## Pitfalls

- **Limited view.** With detectors on the upper half of the sphere only, the reconstruction of the ball at its centre is 0.577 instead of 1 when divided by $4\pi$. Divided by the sum of the solid angle elements it is 1.000 at the centre, but 0.812 instead of 0.823 and 0.149 instead of 0.172 at the other two points: the shape is wrong (measurement).
- **Normal direction.** $n_0$ must point toward the object. The wrong sign changes the sign of the image.
- **Too short a record.** The signal from the far side of a sphere arrives at $2R/c$. A shorter record cuts the back-projection for points near the far side.
- **Noisy derivative.** The time derivative amplifies high frequency noise. Filter the data in time, with the band of the detector, before line L2.
- **Wrong time origin.** $t$ in $b$ is the time since the laser pulse. A delay in the trigger changes both the time of flight and the factor $t$ in $b$.
- **Using the 3D formula in 2D.** It gives artefacts and wrong values that do not go away when the sampling is refined.

## Implementations

The Python code places the detectors on a sphere, simulates the pressure of a Gaussian ball from its closed form, computes $b$ by central differences, and back-projects with linear interpolation. It needs no shared helper. The tests check the Gauss-Legendre rule, the solid angles of the sphere, that the closed form solves the wave equation with zero initial velocity, exact reconstruction with the exact $b$, the hand example at the centre, the need for both terms of $b$, the linearity, the $\Delta t^2$ convergence with sampled data, and the limited view of a half sphere.

## History

Finch, Patch and Rakesh (2004) proved exact inversion formulas for spherical means centred on a sphere in odd dimensions, which covers photoacoustic data on a sphere in 3D. Xu and Wang (2005) derived the universal back-projection formula from the Green's function of the wave equation and showed that it is exact for the sphere, the cylinder and the plane. Kunyansky (2007) gave a family of explicit formulas for the sphere, and Finch, Haltmeier and Rakesh (2007) gave exact formulas for even dimensions. The survey of Kuchment and Kunyansky (2008) and the review of Xu and Wang (2006) put the method among the other reconstruction methods.

## References
