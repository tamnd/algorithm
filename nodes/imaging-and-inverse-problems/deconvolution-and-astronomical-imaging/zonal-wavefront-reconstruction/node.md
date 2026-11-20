---
tag: 4DD2FS
kind: algorithm
slug: zonal-wavefront-reconstruction
name: Zonal wavefront reconstruction
aliases:
- Shack-Hartmann wavefront reconstruction
- Southwell reconstruction
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Recover a wavefront on a grid of phase points from measured slopes by least squares. The normal equations are a discrete Poisson equation; piston, and waffle for Fried, are lost."
solves: [least-squares-problem]
model: real-ram
complexity:
  vars: {n: the number of phase points along one side of the grid, K: the number of conjugate gradient iterations}
  time: {worst: Θ(K n^2), average: Θ(K n^2), best: Θ(K n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, iterative: true, linear: true, minimum_norm: true, exact_for_consistent_slopes: true}
history:
  year: 1977
  people: [David L. Fried, Richard H. Hudgin, W. H. Southwell]
  note: Fried and Hudgin published least squares reconstructors for two slope sensor geometries in the same 1977 issue of JOSA. Southwell (1980) compared zonal and modal estimates and gave the geometry with slopes at the phase points.
prereqs: [least-squares-problem, poisson-equation, conjugate-gradient-method]
see_also: [least-squares-phase-unwrapping, phase-unwrapping, phase-diversity, normal-equations, multigrid-method, fast-dct, gauss-seidel-method, pseudoinverse]
sources:
  - paper: doi:10.1364/JOSA.67.000370
    title: David L. Fried, Least-square fitting a wave-front distortion estimate to an array of phase-difference measurements, Journal of the Optical Society of America 67(3), 1977
    locator: pages 370 to 375
  - paper: doi:10.1364/JOSA.67.000375
    title: Richard H. Hudgin, Wave-front reconstruction for compensated imaging, Journal of the Optical Society of America 67(3), 1977
    locator: pages 375 to 378
  - paper: doi:10.1364/JOSA.70.000998
    title: W. H. Southwell, Wave-front estimation from wave-front slope measurements, Journal of the Optical Society of America 70(8), 1980
    locator: pages 998 to 1006 (zonal and modal estimates, the three sampling geometries and the noise propagation)
---

Zonal wavefront reconstruction recovers the phase of an optical wavefront at the points of a grid from measurements of its slopes. A Shack-Hartmann sensor, for example, puts an array of small lenses in the beam; each lens forms a spot, and the shift of the spot is proportional to the mean slope of the wavefront over that lens. "Zonal" means that the unknowns are the phase values at the grid points, one per zone, as opposed to a modal method, which fits the coefficients of a few smooth modes such as Zernike polynomials. The slopes are differences of phase values, so the data are $s = G\varphi + e$ with a sparse difference matrix $G$, and the method solves the [least squares problem](/least-squares-problem/) $\min_\varphi \lVert G\varphi - s\rVert^2$. Its [normal equations](/normal-equations/) are a discrete [Poisson equation](/poisson-equation/) with Neumann boundary data. Two things are never seen by the sensor: the mean phase (piston), and in the Fried geometry also the checkerboard "waffle" mode. The method returns the minimum norm solution, which sets these to zero. The same least squares problem, with wrapped phase differences as data, is [least squares phase unwrapping](/least-squares-phase-unwrapping/).

## In plain words

Think of a hilly field that you cannot see. You can only stand at points of a grid and measure how steep the ground is toward the east and toward the north. Each measurement tells you the height difference between two neighbor points, with some error. From all these differences you want the heights. With no errors, you could walk from one corner and add up the differences, and every path would agree. With errors, paths disagree. Least squares picks the heights whose differences match all the measurements as well as possible in total. The absolute height of the field is never measured, only differences, so the answer is fixed only up to a constant; you set the mean height to zero. In one sensor layout there is one more blind pattern, a checkerboard of up and down, which gives zero in every measurement.

## The problem

The phase $\varphi$ lives on an $n \times n$ grid of points with spacing $h$; $\varphi_{i,j}$ has row $i$ (the $y$ index) and column $j$ (the $x$ index). The data are slopes times $h$, so they have the units of phase. Three geometries are in use:

- **Hudgin.** Each measurement is the difference of two neighbor points: $d^x_{i,j} = \varphi_{i,j+1} - \varphi_{i,j}$ and $d^y_{i,j} = \varphi_{i+1,j} - \varphi_{i,j}$. There are $2n(n-1)$ measurements.
- **Fried.** The sensor sits at the center of each square of four phase points, the usual layout for a Shack-Hartmann sensor in front of a deformable mirror. The $x$ slope is the mean of the two $x$ differences of the square: $d^x_{i,j} = \tfrac12(\varphi_{i,j+1} + \varphi_{i+1,j+1} - \varphi_{i,j} - \varphi_{i+1,j})$, and the same for $y$. There are $2(n-1)^2$ measurements.
- **Southwell.** The slopes $s^x, s^y$ are measured at the phase points. The model is that the mean of two neighbor slopes times $h$ is the phase difference: $\varphi_{i,j+1} - \varphi_{i,j} = \tfrac h2 (s^x_{i,j} + s^x_{i,j+1})$. This is the Hudgin matrix with averaged data.

In each case $s = G\varphi + e$ with a known sparse matrix $G$ and noise $e$, white with variance $\sigma^2$ per measurement in the usual analysis. The output is the minimum norm least squares solution $\varphi^\dagger = G^\dagger s$ (see [pseudoinverse](/pseudoinverse/)).

## The algorithm

The normal equations $G^T G \varphi = G^T s$ have a symmetric positive semidefinite matrix, and the right side is in its range. [Conjugate gradients](/conjugate-gradient-method/) from $\varphi = 0$ solve them without forming the matrix; each step applies $G$ and $G^T$ once.

```pseudo id=main
ZONAL-LS(s, G, K, tol)            ▷ s = slopes times h; G = Hudgin or Fried differences
L1  b ← G^T s                        ▷ minus a discrete divergence of the slopes
L2  phi ← 0;  r ← b;  p ← r
L3  repeat at most K times, while ||r|| > tol · ||b||
L4      q ← G^T (G p)                    ▷ a discrete Laplacian applied to p
L5      a ← <r, r> / <p, q>
L6      phi ← phi + a · p
L7      r' ← r - a · q
L8      p ← r' + (<r', r'> / <r, r>) · p;  r ← r'
L9  phi ← phi minus its projection on the null space of G   ▷ piston; for Fried also waffle
L10 return phi
```

For Southwell data, first form the Hudgin data $d^x_{i,j} = \tfrac h2(s^x_{i,j} + s^x_{i,j+1})$ and $d^y_{i,j} = \tfrac h2(s^y_{i,j} + s^y_{i+1,j})$, then run the Hudgin version. Line L9 removes rounding drift; in exact arithmetic every iterate is already orthogonal to the null space.

For the Hudgin geometry, $G$ is the forward difference and $G^T$ is minus the backward difference divergence, so $G^T G$ is the 5-point Laplacian with Neumann boundary: a row has the number of neighbors of the point on the diagonal (4 inside, 3 on an edge, 2 at a corner) and $-1$ for each neighbor.

## Example

**One loop.** Take the $2 \times 2$ Hudgin grid with four measurements around one square: $d^x_{0,0} = 1$ (top edge) and $0$ on the other three edges. The four differences around the loop should add to zero (the curl of a gradient is zero), but they add to $1$. Least squares spreads this misfit equally over the four edges: the fitted differences are $3/4$ on the top edge, $1/4$ on the bottom edge and $1/4$ and $-1/4$ on the left and right edges, and each fitted value differs from its datum by $1/4$, so the residual norm squared is $4 \cdot (1/4)^2 = 1/4$. The minimum norm solution is

$$\varphi = \begin{pmatrix} -3/8 & 3/8 \\ -1/8 & 1/8 \end{pmatrix},$$

with mean zero. The test runs the code in exact rational arithmetic and gets this matrix; CG stops after two steps, because $G^T G$ has two distinct nonzero eigenvalues here (2 and 4).

**The waffle.** On a $3 \times 3$ Fried grid, add the checkerboard $w_{i,j} = (-1)^{i+j}$ to any phase. In each square the two $x$ differences are $w_{i,j+1} - w_{i,j} = -2w_{i,j}$ and $w_{i+1,j+1} - w_{i+1,j} = 2w_{i,j}$, so their mean is zero, and the same for $y$. The sensor does not see $w$. A deformable mirror driven by a Fried reconstructor can build up waffle over time, since nothing measures it.

**CG on a random phase.** A measurement on one seed: an $8 \times 8$ Hudgin grid with a random Gaussian phase and exact data. The relative error of the CG iterate is 0.58 after 1 step, 0.36 after 4, 0.18 after 8, 0.0052 after 16 and $3 \times 10^{-14}$ after 32 steps.

**Noise.** With white noise of variance $\sigma^2$ on each Hudgin difference, the mean square error of the reconstructed phase per point is $(\sigma^2/n^2)\sum 1/\lambda$, summed over the nonzero eigenvalues $\lambda_{p,q} = 4\sin^2(\pi p/2n) + 4\sin^2(\pi q/2n)$ of the Neumann Laplacian. Computed from this formula:

| $n$ | 4 | 8 | 16 | 32 | 64 | 128 |
|---|---|---|---|---|---|---|
| error variance per point $/\sigma^2$ | 0.493 | 0.632 | 0.755 | 0.872 | 0.985 | 1.097 |
| condition number of $G^T G$ on the range | 11.7 | 50.5 | 206.2 | 828.7 | 3318.8 | 13279.0 |

The noise grows only like $\ln n$, by about $0.11$ each time $n$ doubles. Fried (1977) and Hudgin (1977) both studied this noise propagation; its slow growth is the reason why zonal reconstruction works for large sensors. The condition number grows like $n^2$, so plain iterations need many steps on a large grid.

## Correctness

The full proof is in `proofs/correctness.md`. The main facts:

1. **Normal equations.** $\varphi$ minimizes $\lVert G\varphi - s\rVert^2$ if and only if $G^TG\varphi = G^Ts$. For Hudgin, $G^TG$ is the Neumann 5-point Laplacian, so the problem is a discrete Poisson equation.
2. **Null space.** For Hudgin (and Southwell), the null space of $G$ is the constants (piston), because the grid graph is connected. For Fried with $n \ge 2$, it is spanned by the piston and the waffle $(-1)^{i+j}$, and nothing else.
3. **CG gives the minimum norm solution.** The right side $G^Ts$ is orthogonal to the null space, and every CG iterate from $0$ stays in the range of $G^TG$. So CG converges to the unique least squares solution in that range, which is $G^\dagger s$, in at most as many steps as $G^TG$ has distinct nonzero eigenvalues (exact arithmetic).
4. **Exact data.** If $s = G\varphi^\ast$, the output is $\varphi^\ast$ minus its projection on the null space: the true phase up to piston (and waffle for Fried).
5. **Southwell is exact for quadratics.** If $\varphi$ is a polynomial of degree at most 2 in $x$ and $y$ and the slopes are exact, then $\tfrac h2(s^x_{i,j} + s^x_{i,j+1})$ equals the phase difference exactly (the trapezoid rule is exact for a linear integrand), so Southwell recovers defocus, astigmatism and tilt up to piston.

## Complexity

In the real-RAM model, one application of $G$ or $G^T$ costs $\Theta(n^2)$, so one CG step costs $\Theta(n^2)$ and $K$ steps cost $\Theta(Kn^2)$, with $\Theta(n^2)$ extra space. The condition number of $G^TG$ on its range grows like $n^2$ (table above), so CG needs $K = O(n \log(1/\varepsilon))$ steps for a relative error $\varepsilon$, which gives $O(n^3 \log(1/\varepsilon))$ in total. Other solvers of the same system:

- Dense Gaussian elimination on the $n^2 \times n^2$ matrix: $\Theta(n^6)$. An adaptive optics system with a fixed geometry precomputes the reconstructor matrix $G^\dagger$ once and then applies it to each slope frame by a matrix-vector product, $\Theta(n^4)$ per frame.
- For Hudgin and Southwell the matrix is the Neumann Laplacian, which the 2D DCT diagonalizes ([fast DCT](/fast-dct/)), so a direct solve costs $\Theta(n^2 \log n)$. Freischlad and Koliopoulos (1986) used Fourier transforms in this way. The same trick solves [least squares phase unwrapping](/least-squares-phase-unwrapping/).
- [Multigrid](/multigrid-method/) solves the Poisson system to a fixed accuracy in $\Theta(n^2)$.
- [Gauss-Seidel](/gauss-seidel-method/) and Jacobi sweeps, used in early hardware reconstructors, need $O(n^2)$ sweeps.

## Properties

- Linear in the data: the output is $G^\dagger s$.
- Minimum norm: piston (and waffle for Fried) is set to zero. Any other choice is a constant (or a waffle) added to the result.
- The residual $G\varphi - s$ is the part of the data that is not a gradient. On a grid it is a sum of loop (curl) components; for a smooth wavefront in a weak turbulence it is noise, but at a branch point of the phase (strong scintillation) the true field has curl, and least squares cannot represent it.
- Noise propagation is low: the error variance per point grows like $\ln n$.

## Variants and improvements

- **Weighted least squares.** Weight each slope by the inverse of its noise variance, for example by the spot photon count. The matrix is then a weighted Laplacian, and CG still applies.
- **Modal reconstruction.** Fit the coefficients of a few Zernike or Karhunen-Loeve modes instead of the phase at every point. This is a small dense least squares problem; it filters noise but cannot represent detail finer than the modes.
- **Minimum variance (MAP) reconstruction.** Add a prior covariance of the phase, for example the Kolmogorov statistics of turbulence, which turns the problem into a regularized one, like [Tikhonov regularization](/tikhonov-regularization/), and removes the null space.
- **Branch point reconstruction.** For strong turbulence, add a reconstruction of the rotational part of the field, as in phase unwrapping with residues (see [phase unwrapping](/phase-unwrapping/)).
- **Curvature sensing.** A curvature sensor measures the Laplacian of the phase directly, with the slopes at the edge as Neumann data; the same Poisson solver applies.

## When to use it

Use zonal least squares to turn Shack-Hartmann, shearing interferometer or pyramid sensor slopes into a phase map, in adaptive optics and in optical testing. It is the default when the wavefront may have structure at the scale of the sensor grid. Use the Fried geometry when the sensor and the actuators are laid out with sensors at the centers of the actuator squares, and filter or penalize the waffle mode. Use a modal fit when only low order aberrations matter and the noise is high. To estimate the aberration from images instead of slopes, use [phase diversity](/phase-diversity/).

## Pitfalls

- The sensor never sees piston, so the absolute phase is unknown. Do not compare two reconstructions without removing the mean.
- In the Fried geometry the waffle mode is invisible. A closed loop that integrates the reconstructor output can let it grow; remove it as in line L9 or penalize it.
- Mixing up the geometries gives a wrong reconstructor. Fried slopes fed to a Hudgin matrix give an error of the same size as the signal.
- The slopes must be multiplied by the spacing $h$ (and by the factor from spot shift to slope) before they are phase differences.
- A grid with holes, such as a circular pupil with a central obstruction, must use only the measurements inside the pupil. The null space can grow if the pupil splits into parts that no measurement connects, and then each part has its own piston.
- Stopping CG with a loose tolerance leaves the low spatial frequencies, which converge last, partly fitted.

## Implementations

## History

D. L. Fried (1977) and R. H. Hudgin (1977) published least squares reconstructors from phase difference measurements in the same issue of the Journal of the Optical Society of America, for compensated imaging through the atmosphere. Fried used the geometry that now carries his name, and Hudgin used differences between neighbor points; both studied how the measurement noise propagates into the phase. W. H. Southwell (1980) compared zonal and modal estimation and introduced the geometry with slopes at the phase points. Later work added Fourier solvers, sparse and multigrid methods for very large adaptive optics systems, and minimum variance reconstructors.

## References
