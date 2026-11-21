---
tag: KKE2E7
kind: algorithm
slug: katsevich-algorithm
name: Katsevich algorithm
aliases:
- Katsevich helical reconstruction
area: imaging-and-inverse-problems/tomographic-reconstruction
level: research
summary: Exact helical cone-beam CT reconstruction. Differentiate the data along the source path, apply a 1D Hilbert filter along kappa-lines, and back-project over the PI-interval of each point.
solves: [tomographic-reconstruction-problem]
model: real-ram
complexity:
  vars: {V: the number of reconstructed points, K: the number of views in one PI-interval, a: the number of views, m: the number of detector rows, d: the number of detector columns}
  time: {worst: "O(a m d + V K d)"}
  space: {extra: "O(a m d)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 2002
  people: [A. Katsevich]
  note: Katsevich gave the first exact inversion formula for helical cone-beam data of the filtered back-projection type, with shift-invariant 1D filtering.
prereqs: [feldkamp-davis-kress, grangeat-formula, hilbert-transform]
see_also: [tuy-condition, fan-beam-filtered-back-projection, x-ray-transform, radon-transform, back-projection-operator, filtered-back-projection, ramp-filter, sart]
sources:
  - paper: doi:10.1137/S0036139901387186
    title: A. Katsevich, Theoretically exact filtered backprojection-type inversion algorithm for spiral CT, SIAM Journal on Applied Mathematics 62(6), 2002
    locator: pp. 2012 to 2026 (the inversion formula with filtering along kappa-lines)
  - paper: doi:10.1016/S0196-8858(03)00099-X
    title: A. Katsevich, An improved exact filtered backprojection algorithm for spiral computed tomography, Advances in Applied Mathematics 32(4), 2004
    locator: pp. 681 to 697
  - paper: doi:10.1088/0031-9155/48/23/001
    title: F. Noo, J. Pack and D. Heuscher, Exact helical reconstruction using native cone-beam geometries, Physics in Medicine and Biology 48(23), 2003
    locator: the implementation for flat and curved detectors, with the derivative at a fixed ray direction and the kappa-line rebinning
  - paper: doi:10.1137/0143035
    title: H. K. Tuy, An inversion formula for cone-beam reconstruction, SIAM Journal on Applied Mathematics 43(3), 1983
    locator: the data condition that a helix satisfies
---

Katsevich's algorithm reconstructs a 3D object exactly from cone-beam X-ray data taken while the source moves on a helix around it, as in a helical CT scanner. It is of the filtered back-projection type. First it differentiates the data along the source path at a fixed ray direction. Then it applies a 1D Hilbert filter along special lines in the detector, the kappa-lines. Then it back-projects the result, for each point, over the part of the helix between the two ends of the PI-line through the point. Unlike [Feldkamp-Davis-Kress](/feldkamp-davis-kress/), it is exact for every smooth object inside the helix, and it needs only a narrow band of detector rows. The filter is 1D and shift-invariant along each line, so the cost is close to that of FDK.

## In plain words

In a helical scanner the patient moves through the ring while the X-ray source turns, so the source draws a helix around the patient. Each shot records a 2D picture on a detector with a few rows.

Older fast methods for this scan are approximate. Katsevich found a formula of the same simple shape as filtered back-projection that is exact. For each point, it uses only the shots from the part of the helix that "sees" the point between two fixed ends, a little more than half a turn. It filters each shot along slanted lines, not along the rows, and the slant of these lines follows the helix. Then it smears each filtered shot back through the volume, as other back-projection methods do.

## The problem

The source is at $y(s) = (R\cos s, R\sin s, hs)$, a helix of radius $R$ and pitch $P = 2\pi h$, the rise per turn. Put $e_u(s) = (-\sin s, \cos s, 0)$, $e_v = (0, 0, 1)$ and $e_w(s) = (\cos s, \sin s, 0)$. A flat detector at the distance $D$ from the source is normal to $e_w(s)$. Its point $(u, v)$ is $y(s) + u\,e_u + v\,e_v - D\,e_w$. The data $g(s, u, v)$ is the integral of the attenuation $f$ along the ray from $y(s)$ through the point $(u, v)$. This is the cone-beam [X-ray transform](/x-ray-transform/). The unknown $f$ is smooth with support inside the cylinder of radius $r < R$ around the axis. The views are $s_k = s_0 + k\,\Delta s$, the columns $u_j = (j - (d-1)/2)\Delta u$ and the rows $v_r = (r - (m-1)/2)\Delta v$.

**The PI-line.** For a point $x$ inside the helix there are $s_b < s_t < s_b + 2\pi$ such that $x$ lies on the segment from $y(s_b)$ to $y(s_t)$. This segment is the PI-line of $x$, and it is unique. The PI-interval is $I_{PI}(x) = [s_b, s_t]$. A helix meets every plane through the object, so it satisfies the [Tuy condition](/tuy-condition/).

**The kappa-lines.** In the detector of the view $s$, the kappa-line with the angle $\psi \in (-\pi/2, \pi/2)$ is
$$v = v_\kappa(u, \psi) = \frac{DP}{2\pi R}\left(\psi + \frac{\psi}{\tan\psi}\,\frac{u}{D}\right).$$
It is the projection of the plane through $y(s)$, $y(s + \psi)$ and $y(s + 2\psi)$.

**The formula.** For $x$ and $s \in I_{PI}(x)$, let $(u^*, v^*)$ be the detector point of the ray through $x$ and $\psi^*$ the angle of the kappa-line through it. Let
$$g_1 = \left(\partial_s + \frac{u^2 + D^2}{D}\,\partial_u + \frac{uv}{D}\,\partial_v\right)g, \qquad g_2 = \frac{D}{\sqrt{u^2 + v^2 + D^2}}\,g_1.$$
Here $g_1$ is the derivative of the data along the source path for a fixed ray direction. Then
$$f(x) = \frac{1}{2\pi}\int_{I_{PI}(x)} \frac{1}{R - x\cdot e_w(s)}\,\mathrm{p.v.}\!\int \frac{1}{\pi(u^* - u)}\,g_2\big(s, u, v_\kappa(u, \psi^*)\big)\,du\,ds.$$
The inner integral is the [Hilbert transform](/hilbert-transform/) of $g_2$ along the kappa-line, read at $u^*$. This is the flat-detector form of Noo, Pack and Heuscher. The constant and the sign are written for the conventions here, and the code confirms them.

## The algorithm

```pseudo id=main
KATSEVICH(g, geometry, x)        ▷ g[k][r][j]: view s_k, detector point (u_j, v_r); one point x
                                ▷ for each view k: g₂ from central differences
L1      g_s ← (g[k+1][r][j] - g[k-1][r][j]) / (2Δs), and g_u, g_v in the same way
L2      g₁ ← g_s + ((u_j² + D²)/D) g_u + (u_j v_r / D) g_v
L3      g₂[k][r][j] ← D / sqrt(u_j² + v_r² + D²) · g₁
L4  (s_b, s_t) ← the PI-interval of x, by bisection
    for each view k with s_k in [s_b - Δs, s_t + Δs] do
L5      (u*, v*, depth) ← the projection of x; ψ* ← the kappa-line angle through (u*, v*), by bisection
L6      ℓ[j] ← g₂[k] at (u_j, v_κ(u_j, ψ*)), by linear interpolation in v
L7      H[j] ← Σ_l (2 / (π (j - l))) ℓ[l] over odd j - l, for the two columns j next to u*
L8      val[k] ← H interpolated at u*, divided by depth
L9  return (1/(2π)) ∫ over [s_b, s_t] of the piecewise linear interpolant of val
```

Lines L1 to L3 depend only on the data and are done once for each view that some point needs. Lines L4 to L9 are done for each point. The code computes $g_2$ for a view the first time a point needs it and keeps it. Line L7 is the band-limited discrete Hilbert kernel: $\Delta u$ times $1/(\pi(u^* - u))$ at the odd offsets, doubled because the even offsets are 0. Line L9 integrates the piecewise linear interpolant exactly, including the partial cells at the two ends of the PI-interval.

## Example

Take $R = 3$, $P = 2$ and $D = 3$, so $h = 1/\pi$ and $\frac{DP}{2\pi R} = \frac{1}{\pi}$.

**PI-interval of a point on the axis.** For $x = (0, 0, x_3)$ every chord through the axis is a diameter, so $s_t = s_b + \pi$ and $x$ is at the middle of the segment. Its height is $h(s_b + \pi/2) = x_3$, so $I_{PI}(x) = [\pi x_3 - \pi/2, \pi x_3 + \pi/2]$. For $x_3 = 0$ this is $[-1.5708, 1.5708]$, and for $x_3 = 0.5$ it is $[0, 3.1416]$. The code gives these values. A point off the axis has a different interval: for $(0.6, 0, 0)$ the code gives $[-1.3694, 1.3694]$, which is shorter than $\pi$.

**The filtering line.** Take $x = 0$ and the view $s = \pi/4$. The depth is $R - x\cdot e_w = 3$, $u^* = 0$ and $v^* = 3(0 - \pi/4 \cdot 1/\pi)/3 = -0.25$. On the column $u = 0$ the kappa-line has the height $\psi/\pi$, so $\psi^* = -\pi/4$. With $\psi/\tan\psi = (-\pi/4)/(-1) = \pi/4$, the kappa-line is
$$v = \frac{1}{\pi}\left(-\frac{\pi}{4} + \frac{\pi}{4}\cdot\frac{u}{3}\right) = -0.25 + \frac{u}{12}.$$
So at $u = 1$ the filter reads the data at $v = -0.1667$. The line rises to the right, while the rows are horizontal. Filtering along the rows, as FDK does, would mix data from other kappa-planes.

**Measurements.** The table gives the output of the code for the Gaussian blob $f(x) = e^{-10\vert x - c\vert^2}$ with $c = (0.1, 0.05, 0)$, on exact data with 64 views per turn, $m = 41$ rows with $\Delta v = 0.05$, and $d = 41$ columns with $\Delta u = 0.055$ or $d = 81$ columns with $\Delta u = 0.0275$. These are measurements, not bounds.

| point $x$ | true $f(x)$ | $d = 41$ | $d = 81$ |
|---|---|---|---|
| $(0.1, 0.05, 0)$ | 1.0000 | 0.9692 | 0.9888 |
| $(0.2, 0.05, 0)$ | 0.9048 | 0.8778 | 0.8952 |
| $(0.1, 0.05, 0.15)$ | 0.7985 | 0.7756 | 0.7912 |
| $(0, 0, 0)$ | 0.8825 | 0.8643 | 0.8751 |
| $(-0.2, 0.1, -0.1)$ | 0.3588 | 0.3566 | 0.3573 |
| $(0.6, 0, 0)$ | 0.0801 | 0.0831 | 0.0806 |

The error falls by about a factor 3 when the column step is halved. With 128 views per turn and 41 columns the values change by less than 0.001, so on this grid the column step dominates the error. The values are the same for $D = 3$ and $D = 6$ when $\Delta u$ and $\Delta v$ scale with $D$, as the formula predicts.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) is partial: it cites Katsevich's inversion theorem and proves the steps that connect it to the code. It shows that the PI-line exists, by the intermediate value theorem on the height of the chord through $x$. It derives the kappa-line formula, by checking that the line passes through the projections of $y(s + \psi)$ and $y(s + 2\psi)$. It proves that $g_1$ is the derivative at a fixed ray direction, by the chain rule. And it changes the inner integral of Katsevich's formula, an integral over a half circle of ray directions with the kernel $1/\sin\gamma$, into the Hilbert transform along the kappa-line on the flat detector, which gives the factors $1/(R - x\cdot e_w)$ and $D/\sqrt{u^2 + v^2 + D^2}$. The reason why the formula is exact is sketched there. The 3D Radon inversion writes $f$ as an integral over all planes through $x$ ([Grangeat's formula](/grangeat-formula/) gives the plane integrals from the data). Every plane through $x$ meets the PI-segment of the helix in one or three points, and Katsevich's weights for these points add to 1 for almost every plane. The proof also shows an exact locality property of the discrete algorithm: it never reads the detector rows outside a band around the kappa-lines.

## Complexity

In the real-RAM model:

- Lines L1 to L3 take $O(md)$ for each view, so $O(amd)$ in total.
- Line L4 takes a fixed number of bisection steps for each point.
- Lines L5 to L8 take $O(d)$ for each point and view: $O(d)$ to read the kappa-line and $O(d)$ for each of the two Hilbert sums. With $K$ views in a PI-interval this is $O(Kd)$ per point.
- Line L9 takes $O(K)$ per point.

The total for $V$ points is $O(amd + VKd)$, and the extra space is $O(amd)$ for $g_2$. This point-wise form is simple and fits a small test. A volume code filters each view once along a family of kappa-lines: it rebins $g_2$ to $(u, \psi)$ coordinates, filters each line with an FFT, and rebins back. That costs $O(m d \log d)$ per view, and the back-projection then costs $O(1)$ per voxel and view, as in FDK. For a cube of $N^3$ voxels with $K$ of order $N$ the back-projection dominates with $O(N^4)$.

## Properties

- **Exact** for smooth $f$ inside the helix cylinder in the continuous limit (theorem, cited). FDK is not.
- **Linear** in the data.
- **Shift-invariant 1D filter.** The filter along each kappa-line is the Hilbert kernel, which does not depend on the position. The kappa-line itself depends on the view and on the point only through $\psi^*$.
- **Local in $v$.** The algorithm reads only a band of rows around the kappa-lines, so a detector a little taller than the band is enough (proved for the discrete code, and tested).
- **Long objects.** The data for a point comes from its PI-interval, which is less than one turn. The object may extend far beyond the scanned region along the axis, and the method still works inside it.
- **Not local in $u$.** The Hilbert kernel decays like $1/u$, so every column of the kappa-line is needed. A detector cut short in $u$ gives errors.

## Variants and improvements

- **Curved detector.** Noo, Pack and Heuscher give the same steps for the cylindrical detector of clinical scanners.
- **Derivative at a fixed direction.** Computing $g_1$ by the chain rule, as here, or by a difference of rays with the same direction from two nearby source points, changes the accuracy. Katsevich's 2004 paper gives an improved form of the algorithm.
- **Approximate methods.** FDK adapted to the helix is simpler and is still used, at the cost of cone-beam errors at large cone angles.
- **Iterative methods.** [SART](/sart/) handles any orbit and noise models, at a much higher cost.

## When to use it

Use it for helical cone-beam CT when exactness matters: a large cone angle, a large pitch, or objects with fast changes along the axis, where FDK-type methods show cone-beam errors. It needs a detector that covers the band of the kappa-lines in $v$ and the whole object in $u$. For a circular orbit it does not apply, and FDK or an iterative method is the choice.

## Pitfalls

- **Filtering along the rows.** The Hilbert filter must run along the kappa-lines. Filtering the rows mixes data from different planes, and the result is no longer exact.
- **The wrong derivative.** The derivative in $s$ must be taken for a fixed ray direction, not at a fixed detector point. Without the terms in $\partial_u$ and $\partial_v$ of $g_1$ the result is wrong everywhere.
- **The wrong PI-interval.** Using $[x_3/h - \pi/2, x_3/h + \pi/2]$ for every point, as for the axis, is wrong off the axis. The interval of $(0.6, 0, 0)$ above is shorter than $\pi$.
- **Ends of the interval.** The integrand does not vanish at $s_b$ and $s_t$. A sum over the whole views in the interval, without the partial cells at the two ends, gives an error of order $\Delta s$.
- **Sign conventions.** The sign of the result depends on the orientation of $u$, of the helix and of the Hilbert kernel. Check it on a known blob, as the test does.

## Implementations

## History

Tuy showed in 1983 that exact cone-beam inversion needs every plane through the object to meet the source path, and a helix meets this condition. Grangeat gave in 1991 the link between cone-beam data and the derivative of the 3D Radon transform. Katsevich published in 2002 an exact formula of the filtered back-projection type with a 1D shift-invariant filter, and in 2004 an improved form. Noo, Pack and Heuscher wrote it in 2003 for the flat and curved detectors of real scanners.

## References
