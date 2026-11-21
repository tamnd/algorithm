---
tag: 7MNYCN
kind: algorithm
slug: feldkamp-davis-kress
name: Feldkamp-Davis-Kress algorithm
aliases:
- FDK
- Feldkamp algorithm
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Approximate cone-beam CT reconstruction for a circular source orbit. Weight each projection, ramp-filter it row by row, and back-project it in 3D with the inverse squared depth.
solves: [tomographic-reconstruction-problem]
model: real-ram
complexity:
  vars: {a: the number of source positions, m: the number of detector rows, d: the number of detector columns, n: the side of each n x n slice, s: the number of output slices}
  time: {worst: "O(a m d log d + a s n^2)"}
  space: {extra: "O(a m d + s n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 1984
  people: [L. A. Feldkamp, L. C. Davis, J. W. Kress]
  note: Feldkamp, Davis and Kress gave a practical cone-beam algorithm for a circular orbit that extends fan-beam filtered back-projection to 3D.
prereqs: [fan-beam-filtered-back-projection, x-ray-transform, ramp-filter]
see_also: [tuy-condition, grangeat-formula, katsevich-algorithm, fan-to-parallel-rebinning, back-projection-operator, filtered-back-projection, sart, beer-lambert-law]
sources:
  - paper: doi:10.1364/JOSAA.1.000612
    title: L. A. Feldkamp, L. C. Davis and J. W. Kress, Practical cone-beam algorithm, Journal of the Optical Society of America A 1(6), 1984
    locator: the whole paper, which starts at p. 612
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.6 (three-dimensional reconstructions)
  - paper: doi:10.1137/0143035
    title: H. K. Tuy, An inversion formula for cone-beam reconstruction, SIAM Journal on Applied Mathematics 43(3), 1983
    locator: the data condition for exact cone-beam inversion, which the circular orbit does not satisfy
---

The Feldkamp-Davis-Kress (FDK) algorithm reconstructs a 3D object from cone-beam X-ray projections taken while a point source moves on a circle. It is [fan-beam filtered back-projection](/fan-beam-filtered-back-projection/) with a flat detector, applied to each detector row as if the row were a tilted fan, followed by a back-projection in 3D. Each projection gets a cosine weight, each detector row is filtered with the [ramp filter](/ramp-filter/), and each voxel adds the filtered value of the ray through it, divided by the square of its depth. With $a$ source positions, an $m \times d$ detector and $s$ slices of $n \times n$ voxels it takes $O(a m d \log d + a s n^2)$ time with an FFT. The result is exact in the plane of the orbit and for objects that do not change along the axis. Elsewhere it is an approximation, which is good for small cone angles.

## In plain words

A cone-beam scanner has a small X-ray source and a flat detector panel that turn around the object together. Each shot records a whole 2D picture, so one turn gives data for many slices at once.

FDK treats each row of the panel as if it were a normal fan of rays. It weights each reading by how much its ray is tilted, sharpens each row with the same filter as in 2D, and then smears each picture back through the volume along the rays to the source. Points near the source get less weight. The method is fast and simple, and it is the standard method for a circular scan. But the rays of one row are tilted out of the slice, so slices far from the plane of the orbit come out with errors.

## The problem

The source at the angle $\beta$ is at $S(\beta) = D\,\omega^\perp(\beta)$, on a circle of radius $D$ in the plane $x_3 = 0$, with $\omega(\beta) = (\cos\beta, \sin\beta, 0)$ and $\omega^\perp(\beta) = (-\sin\beta, \cos\beta, 0)$. A virtual flat detector passes through the axis of rotation, normal to $\omega^\perp(\beta)$. Its point $(t, z)$ is $t\,\omega(\beta) + z\,e_3$. The data $g(\beta, t, z)$ is the integral of the attenuation $f$ along the ray from $S(\beta)$ through the point $(t, z)$, which is a value of the cone-beam [X-ray transform](/x-ray-transform/). A real detector farther away gives the same data after a scaling of $t$ and $z$. The scanner gets the line integrals from the intensities by the [Beer-Lambert law](/beer-lambert-law/). The unknown $f$ is zero outside a ball of radius $r < D$.

The detector samples $t_j = (j - (d-1)/2)\tau$ for $j = 0, \ldots, d-1$ and $z_r = (r - (m-1)/2)\zeta$ for $r = 0, \ldots, m-1$, and the scan takes $\beta_k = 2\pi k/a$. The output is a set of slices at the heights $x_3$. Each slice is an $n \times n$ image on $[-1, 1]^2$, with the pixel $(i, j)$ at $x_1 = -1 + (2j+1)/n$ and $x_2 = 1 - (2i+1)/n$.

For a point $x$, put $U = (D - x\cdot\omega^\perp)/D$, the depth of $x$ along the central ray divided by $D$. The ray from $S(\beta)$ through $x$ hits the detector at $t' = x\cdot\omega/U$ and $z' = x_3/U$. The algorithm evaluates the FDK formula
$$f_{\mathrm{FDK}}(x) = \int_0^{2\pi} \frac{1}{U^2}\int \frac{h(t' - u)}{2}\,\frac{D\,g(\beta, u, z')}{\sqrt{D^2 + u^2 + z'^2}}\,du\,d\beta,$$
where $h$ is the ramp filter, the filter with the frequency response $|\sigma|$ in ordinary frequency.

## The algorithm

```pseudo id=main
FDK(g, D, τ, ζ, n, heights)     ▷ g[k][r][j]: source angle β_k = 2πk/a, detector point (t_j, z_r)
L1  a, m, d ← the sizes of g
L2  h[l] ← (1/2) · RAMLAK(l, τ) for l = -(d-1) .. d-1     ▷ 1/(4τ²) at 0, 0 for even l, -1/(l²π²τ²) for odd l
L3  for k ← 0 to a - 1 and each row r do
L4      p[j] ← D / sqrt(D² + t_j² + z_r²) · g[k][r][j] for each j
L5      q_k[r][j] ← τ Σ_l h[j - l] p[l] for each j    ▷ direct sum, or an FFT with zero padding
L6  for each height x₃, each pixel (x₁, x₂) and each k do
L7      U ← (D - x·ω⊥(β_k)) / D;  t' ← x·ω(β_k) / U;  z' ← x₃ / U
L8      f(x) ← f(x) + BILINEAR(q_k, z'/ζ + (m-1)/2, t'/τ + (d-1)/2) / U²
L9  return (2π/a) · f
```

Line L2 is the band-limited ramp (Ram-Lak) kernel times $\frac{1}{2}$. The $\frac{1}{2}$ is there because a full scan measures each line in the mid-plane twice. Line L4 is the cosine weight: the factor $D/\sqrt{D^2 + t^2 + z^2}$ is the cosine of the angle between the ray and the central ray. Line L5 filters each detector row alone, as an aperiodic [discrete convolution](/discrete-convolution/). Line L7 projects the voxel onto the detector, and line L8 reads the filtered projection there by bilinear interpolation, with 0 outside the detector, and divides by $U^2$. Line L9 multiplies by the angle step.

## Example

Take $D = 3$. The weight of line L4 at the detector point $(t, z) = (0.5, 0.4)$ is $3/\sqrt{9 + 0.25 + 0.16} = 3/\sqrt{9.41} = 0.9780$.

**An object that does not change in $z$.** Let $f$ be 1 inside the infinite cylinder $x_1^2 + x_2^2 < 0.16$. The central ray $t = 0$ in the row $z = 0$ crosses it along a chord of length $0.8$. In the row $z = 1$ the central ray is tilted, and its path through the cylinder is longer by the factor $\sqrt{10}/3$, so $g = 0.8 \cdot \sqrt{10}/3 = 0.8433$. The weight there is $3/\sqrt{10} = 0.9487$, and $0.9487 \cdot 0.8433 = 0.8$. So after line L4 the two rows agree. The same holds for every ray, so the weighted rows are equal and every slice of the output is the same as the mid-plane slice. This is Theorem 2 of the proof.

**The back-projection of one voxel.** Take $x = (0.5, 0, 0.4)$.

| source angle | $x\cdot\omega$ | $x\cdot\omega^\perp$ | $U$ | $t'$ | $z'$ | $1/U^2$ |
|---|---|---|---|---|---|---|
| $\beta = 0$ | 0.5 | 0 | 1 | 0.5 | 0.4 | 1 |
| $\beta = \pi/2$ | 0 | -0.5 | 7/6 | 0 | 0.3429 | 0.7347 |

At $\beta = \pi/2$ the source is at $(-3, 0, 0)$, and the voxel is farther from it than the axis is. So the ray through the voxel hits the detector lower, at $z' = 0.4 \cdot 6/7$, and the voxel gets a smaller weight.

**Measurements.** The table gives the results of the code on exact cone-beam data with $D = 3$, $a = 32$, $d = 41$ columns with $\tau = 0.075$, $m = 13$ rows with $\zeta = 1/6$, and $n = 16$. These are measurements of this setup, not bounds.

| object | result |
|---|---|
| Gaussian $e^{-8\vert x - c\vert^2}$, $c = (0.2, -0.1, 0)$, largest error in the slice $x_3 = 0$ | 0.0167 |
| same Gaussian, largest error in the slice $x_3 = 0.25$ | 0.0136 |
| cylinder of radius 0.4 around $(0.2, -0.1)$, pixel $(7, 9)$ at the distance 0.16 from the axis of the cylinder, slices $x_3 = 0$ and $x_3 = 0.6$ | 1.0002 and 1.0002 |

To see the error of the formula itself, take the blob $e^{-8((x_1 - 0.5)^2 + (x_2 - 0.5)^2) - 40(x_3 - h)^2}$, which is thin in $x_3$, and read the output at its center $(0.5, 0.5, h)$, where the true value is 1. The detector has the height $\pm 1.2$.

| height $h$ | $a = 32$, $m = 41$, $d = 61$ | $a = 64$, $m = 81$, $d = 121$ |
|---|---|---|
| 0 | 0.9935 | 0.9988 |
| 0.25 | 0.9503 | 0.9752 |
| 0.5 | 0.9090 | 0.9264 |

In the mid-plane the error becomes small as the sampling becomes finer, as Theorem 1 predicts. At the height 0.5 it is 9 percent and then 7 percent, so most of it does not come from the sampling. This is the cone-beam error of FDK (measurement).

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that the ray from the source through the point $(t', z')$ passes through $x$, and then proves two exactness results. **Theorem 1:** in the mid-plane $x_3 = 0$ the formula only reads the row $z = 0$, whose rays lie in that plane, and it is then the 2D flat-detector fan-beam formula, which is exact. **Theorem 2:** if $f$ does not depend on $x_3$, a tilted ray crosses the object along a path that is longer by the factor $\sqrt{D^2 + t^2 + z^2}/\sqrt{D^2 + t^2}$, and the cosine weight cancels this factor. So the weighted rows are equal, and every slice is reconstructed as the mid-plane. Both results also hold for the discrete algorithm in a form that the tests check exactly. For a general $f$ and $x_3 \ne 0$ the measurement above shows an error that does not come from the sampling. A heuristic reason is that the rays used for one voxel do not lie in one plane. A deeper reason is that the circular orbit fails the [Tuy condition](/tuy-condition/): a plane $x_3 = c$ with $c \ne 0$ that cuts the object does not meet the orbit.

## Complexity

In the real-RAM model:

- Lines L3 to L5 take $O(d^2)$ for each row of each projection with the direct sum, or $O(d \log d)$ with an FFT of length at least $2d - 1$. That is $O(a m d^2)$ or $O(a m d \log d)$ in total.
- Lines L6 to L8 take $O(1)$ for each source and voxel, so $O(a s n^2)$ for $s$ slices.

The total is $O(a m d \log d + a s n^2)$ with an FFT, and the code uses the direct sum. For a cube of $N^3$ voxels with $a, m, d$ all of order $N$ the back-projection costs $O(N^4)$, which dominates. The extra space is $O(a m d)$ for the filtered projections and $O(s n^2)$ for the volume. A code can also filter and back-project one projection at a time and keep only $O(m d)$ of the filtered data.

## Properties

- **Linear.** The output is a linear function of the data, as the code tests.
- **Exact in the mid-plane.** In the plane of the orbit it is the 2D fan-beam method (theorem).
- **Exact for objects that do not change along the axis** (theorem). The detector must be tall enough to see the voxel.
- **Approximate elsewhere.** The error grows with the distance from the mid-plane and is largest for objects with fast changes along the axis (measurement above).
- **Row-wise filtering.** The filter runs along the detector rows, which are parallel to the plane of the orbit. It does not mix the rows, so the filtered data of one projection is available at once.

## Variants and improvements

- **Short scan.** Parker's weights from [fan-beam filtered back-projection](/fan-beam-filtered-back-projection/) reduce the scan to $\pi$ plus the fan angle. They make the mid-plane exact again, and off the mid-plane the result is still an approximation.
- **Curved detector.** For a cylindrical detector, use the equiangular fan kernel in each row with the matching weights.
- **Exact methods.** A circle does not give enough data for exact inversion. [Grangeat's formula](/grangeat-formula/) relates cone-beam data to derivatives of the 3D Radon transform, and a helical orbit with [Katsevich's algorithm](/katsevich-algorithm/) is exact.
- **Iterative methods.** [SART](/sart/) and [SIRT](/sirt/) handle cone beams with any orbit and reduce the cone-beam error at a much higher cost.

## When to use it

Use FDK for cone-beam CT with a circular orbit and a moderate cone angle. It is fast, it is easy to run on a GPU, and its error is small near the mid-plane. If the cone angle is large or the object changes fast along the axis far from the mid-plane, use a helical scan with an exact method, or an iterative method.

## Pitfalls

- **Missing cosine weight.** Without the factor $D/\sqrt{D^2 + t^2 + z^2}$, rows far from the center are too bright, and Theorem 2 fails.
- **The wrong depth weight.** The weight is $1/U^2$ with the depth along the central ray, not one over the squared distance from the source to the voxel. With a flat detector these differ off the central ray.
- **Short detector.** If $z' = x_3/U$ falls outside the detector, the code reads 0 and the voxel is too dark. Voxels near the source side need the tallest detector.
- **Real and virtual detector.** If the detector is at the distance $D_d$ from the source and not at the axis, scale $t$ and $z$ by $D/D_d$ before the algorithm.
- **Filtering along the wrong direction.** Filtering the columns, or the whole 2D projection, is not FDK and does not reduce to the fan-beam formula in the mid-plane.

## Implementations

## History

The early CT scanners measured one slice at a time. Feldkamp, Davis and Kress published in 1984 a practical algorithm for the data of a 2D detector and a circular orbit. They extended the fan-beam method by row-wise filtering of weighted projections and a 3D back-projection. Their algorithm reduces to the fan-beam method in the mid-plane and is the standard method for circular cone-beam CT. Tuy showed in 1983 which orbits give enough data for exact inversion, and a circle is not one of them. This is why exact methods for cone beams use other orbits, such as a helix.

## References
