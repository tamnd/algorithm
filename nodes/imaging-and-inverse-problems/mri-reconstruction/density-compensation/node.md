---
tag: 4CW95Q
kind: algorithm
slug: density-compensation
name: Density compensation
aliases:
- Pipe-Menon density compensation
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: "Weights for non-Cartesian k-space samples, found by the Pipe-Menon fixed point iteration w <- w / (C w), so that the weighted samples convolved with the gridding kernel give a flat density."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {m: the number of k-space samples, q: the largest number of samples within the kernel radius of one sample, K: the number of iterations}
  time: {worst: O(m^2 + K m q)}
  space: {extra: O(m q)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1999
  people: [James G. Pipe, Padmanabhan Menon]
  note: Pipe and Menon explained why gridding needs density weights and found them by a fixed point iteration that uses only the gridding kernel and the sample positions.
prereqs: [k-space-trajectory, nonuniform-fft]
see_also: [conjugate-phase-reconstruction, nonuniform-discrete-fourier-transform, voronoi-diagram, propeller-mri, k-space, cg-sense, fixed-point-iteration, convolution-theorem]
sources:
  - paper: doi:10.1002/(SICI)1522-2594(199901)41:1<179::AID-MRM25>3.0.CO;2-V
    title: James G. Pipe and Padmanabhan Menon, Sampling density compensation in MRI, rationale and an iterative numerical solution, Magnetic Resonance in Medicine 41(1), 1999, 179 to 186
    locator: the rationale for density weights in gridding and the iteration W <- W / (W convolved with C) (general locator; equation numbers not confirmed)
  - paper: doi:10.1109/42.97598
    title: John I. Jackson, Craig H. Meyer, Dwight G. Nishimura and Albert Macovski, Selection of a convolution function for Fourier inversion using gridding, IEEE Transactions on Medical Imaging 10(3), 1991, 473 to 478
    locator: gridding with a Kaiser-Bessel kernel and the role of the density weights (general locator)
  - paper: doi:10.1109/42.774166
    title: Volker Rasche, Roland Proksa, Ralph Sinkus, Peter Bornert and Holger Eggers, Resampling of data between arbitrary grids using convolution interpolation, IEEE Transactions on Medical Imaging 18(5), 1999, 385 to 392
    locator: resampling between arbitrary grids by convolution interpolation and its density compensation (general locator)
  - paper: doi:10.1002/mrm.1910380117
    title: Richard D. Hoge, Remi K. S. Kwan and G. Bruce Pike, Density compensation functions for spiral MRI, Magnetic Resonance in Medicine 38(1), 1997, 117 to 128
    locator: analytic density compensation for spiral trajectories (general locator)
  - book: isbn:9780120928613
    title: Matt A. Bernstein, Kevin F. King and Xiaohong Joe Zhou, Handbook of MRI Pulse Sequences, Elsevier Academic Press, 2004
    locator: Section 13.2, Gridding Reconstruction
---

Density compensation gives each sample of a non-Cartesian [k-space trajectory](/k-space-trajectory/) a weight that corrects for how densely the trajectory samples k-space near it. A radial trajectory, for example, samples the center far more densely than the edge. Without weights, gridding and the adjoint [nonuniform FFT](/nonuniform-fft/) give an image that is blurred by this extra weight at low frequencies. This page treats the iterative method of Pipe and Menon (1999). It needs only the sample positions and the gridding kernel $C$, and it looks for weights $w > 0$ with $\sum_j C(|k_i - k_j|)\, w_j = 1$ at every sample $k_i$. It starts from $w = 1$ and repeats $w_i \leftarrow w_i / (C w)_i$. Analytic weights such as the radial ramp exist only for simple trajectories; this method works for any trajectory.

## In plain words

A non-Cartesian scan takes its measurements at points that are close together in some places and far apart in others. When the computer adds up the measurements to make a picture, the crowded places count too much. Each measurement needs a weight: small where the points are crowded and large where they are sparse.

The method finds the weights by trial. It starts with equal weights. It then measures how much total weight sits near each point, using the same smoothing shape that the picture step uses. Where that total is too large, the weight of the point goes down; where it is too small, the weight goes up. After a few rounds the total weight near every point is nearly the same.

## The problem

The input is a set of $m$ sample positions $k_1, \ldots, k_m$ in $\mathbb{R}^d$, in units of the Cartesian grid spacing $\Delta k = 1/\mathrm{FOV}$, and a gridding kernel $C(r) \ge 0$ with $C(0) > 0$ and $C(r) = 0$ for $r \ge W/2$. A common kernel is the Kaiser-Bessel function $C(r) = I_0(\beta \sqrt{1 - (2r/W)^2}) / I_0(\beta)$, recommended for gridding by Jackson and colleagues (1991), with the width $W$ and the shape parameter $\beta$. The output is a vector of weights $w > 0$ such that the weighted sample distribution $\sum_j w_j \delta(k - k_j)$, convolved with $C$, is close to 1 at every sample. In matrix form, with $C_{ij} = C(|k_i - k_j|)$, the aim is $C w = \mathbf{1}$.

## The algorithm

```pseudo id=main
PIPE-MENON(k_1..k_m, C, W, K)
L1  for each i: N(i) <- {(j, C_ij) : |k_i - k_j| < W/2 and C_ij > 0}
L2  w_i <- 1 for each i
L3  repeat K times
L4      d_i <- sum over (j, c) in N(i) of c w_j for each i     ▷ d = C w
L5      w_i <- w_i / d_i for each i
L6  return w
```

Line L1 finds the neighbours of each sample. The code of this page does it by brute force in $O(m^2)$; a cell grid or a k-d tree finds them faster. Line L4 is the convolution of the weighted samples with the kernel, evaluated at the samples. Line L5 divides each weight by that density. A sample that sees too much weight around it gets a smaller weight, and a sample that sees too little gets a larger one. The weights are used in gridding: the sample $s_j$ is multiplied by $w_j$ before it is spread onto the grid with $C$.

## Example

Take a radial trajectory with 16 spokes through the center at angles $\pi s / 16$, each with 16 samples at the radii $\pm 0.5, \pm 1.5, \ldots, \pm 7.5$, so $m = 256$. The kernel is Kaiser-Bessel with $W = 3$ and $\beta = 6$, whose integral over the plane is 2.1497. The residual $\max_i |(C w)_i - 1|$ after $K$ iterations was as follows.

| $K$ | 0 | 1 | 2 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|---|
| residual | 19.4 | 0.151 | 0.0508 | 0.00396 | $1.1 \times 10^{-4}$ | $4.6 \times 10^{-7}$ | $3.2 \times 10^{-14}$ |

With $K = 0$ the weights are all 1, and the most crowded sample, near the center, sees a kernel sum of 20.4 where 1 is wanted. After 50 iterations the weights on one spoke, which are the same on every spoke by symmetry, compare with the ramp $w(r) = 2\pi r \Delta r / (32 \cdot 2.1497) = 0.0913\, r$ as follows. The ramp is the area of the ring around radius $r$ shared among the 32 half spokes, divided by the kernel integral.

| radius $r$ | 0.5 | 1.5 | 2.5 | 3.5 | 4.5 | 5.5 | 6.5 | 7.5 |
|---|---|---|---|---|---|---|---|---|
| weight | 0.039 | 0.140 | 0.230 | 0.321 | 0.404 | 0.520 | 0.565 | 0.823 |
| ramp | 0.046 | 0.137 | 0.228 | 0.320 | 0.411 | 0.502 | 0.594 | 0.685 |

In the inner part the weights follow the ramp within a few percent. At the outer edge they are larger, because the outermost samples have no neighbours beyond them, and they oscillate a little near the edge.

## Correctness

The [proof](proofs/correctness.md) shows these facts for every input.

- Every iterate is positive and well defined, because $d_i \ge C(0) w_i > 0$; after the first step every weight is at most $1/C(0)$.
- A positive vector is a fixed point of line L5 if and only if $C w = \mathbf{1}$. So a positive limit, if one exists, is a solution.
- If the kernel is multiplied by $c > 0$, every iterate after the first is divided by $c$.
- Samples at the same position keep equal weights.

The key invariant is $w > 0$. The page does not claim that the iteration converges. Pipe and Menon did not prove convergence, and the system $C w = \mathbf{1}$ need not have a positive solution (see Pitfalls). In the tests, the iterates matched the direct solution of $C w = \mathbf{1}$ when it was positive.

## Complexity

The brute force search of line L1 costs $O(m^2)$ distance computations. With a cell grid of cell size $W/2$ it costs $O(m q)$ on average for evenly spread samples. Each iteration of lines L4 and L5 costs $O(m q)$, where $q$ is the largest neighbour count, so $K$ iterations cost $O(K m q)$. The neighbour lists take $O(m q)$ memory. A gridding implementation can also compute $C w$ by spreading onto an oversampled grid and interpolating back, which costs $O(m W^d + G)$ per iteration for a grid of $G$ points.

## Properties

- **Positive weights.** Every iterate is positive (theorem). This is not true of a direct solve of $C w = \mathbf{1}$, which can give negative weights.
- **Kernel dependent.** The weights depend on the kernel and its width, and they carry its scale (theorem). Weights made for one kernel are not right for another.
- **Fast first steps.** On the radial example the residual fell by a factor of about 130 in the first iteration and below $10^{-3}$ in 10 (measurement).
- **No convergence guarantee.** On random points in the plane with the Kaiser-Bessel kernel, the residual stopped falling near 0.038, because no positive solution exists (measurement).
- **Any trajectory.** It needs only positions, so it works for radial, spiral, [PROPELLER](/propeller-mri/) and random trajectories.

## Variants and improvements

- **Analytic weights.** For radial sampling the ramp $|k|$; for spirals the Jacobian of the trajectory, as in Hoge, Kwan and Pike (1997). These need no iteration, but they are wrong where the trajectory deviates from the model, for example at the center of a radial scan.
- **Voronoi weights.** The area of the [Voronoi](/voronoi-diagram/) cell of each sample, a common geometric choice. Rasche and colleagues (1999) treat density compensation for convolution interpolation on arbitrary grids. The cells at the edge of the sampled region need a bound.
- **Grid-based evaluation.** Line L4 can be done with the gridding operator itself, by spreading the weights onto a grid with $C$ and reading the grid back at the samples. This is how the method is often run on large data.
- **Weighted variant for PROPELLER.** Pipe used a version that also multiplies the weights by a quality factor per blade in [PROPELLER](/propeller-mri/).
- **Least squares in place of weights.** An iterative solver such as the [conjugate gradient method](/conjugate-gradient-method/), as in [CG-SENSE](/cg-sense/), solves the least squares problem directly; density weights then serve only as a preconditioner.

## When to use it

Use density compensation for gridding or for the adjoint nonuniform FFT on any non-Cartesian trajectory, and as a preconditioner for iterative solvers. Compute the weights once per trajectory and kernel, then reuse them for every scan with that trajectory. Use the iterative method when no analytic formula fits the trajectory, or when the trajectory deviates from its design. For [conjugate phase reconstruction](/conjugate-phase-reconstruction/) the same weights serve as $w_j$.

## Pitfalls

- **Kernel that differs from the gridding kernel.** If line L4 uses a kernel that is not the one used in gridding, or with a different scale, the weights are wrong by the ratio of the two (Theorem 3 of the proof).
- **Oscillating weights for a narrow kernel.** With the points $0, 1, 2, 2.5, 3, 4, 5$ on a line and the triangle kernel of width 3, the weights after one pass of line L5 are $[0.75, 0.6, 0.429, 0.429, 0.429, 0.6, 0.75]$, which look right. The limit, the solution of $C w = \mathbf{1}$, is $[0.783, 0.652, 0.261, 0.652, 0.261, 0.652, 0.783]$: the extra point at 2.5 gets a large weight and its neighbours small ones. A kernel width close to the gap between samples gives such patterns.
- **Slow or no convergence.** With the points $0, 1, 2, 2.5, 3, 3.5, 4, 5, 6$ and the triangle kernel of width 2, the exact solution has zero weights and the iterates approach it slowly, like $1/t$. When $C w = \mathbf{1}$ has no positive solution, line L3 should stop after a fixed number of iterations.
- **Neighbour search with a radius too small.** If line L1 uses a radius below $W/2$, some kernel terms are lost and $d$ is too small.
- **Edge of k-space.** Samples at the edge have neighbours only on one side, so their weights grow. Some implementations limit the weights at the edge.

## Implementations

## History

Jackson, Meyer, Nishimura and Macovski (1991) studied the choice of the gridding kernel and recommended the Kaiser-Bessel function. Hoge, Kwan and Pike (1997) compared density compensation functions for spirals. Pipe and Menon (1999) explained why the weights should make the weighted samples, convolved with the kernel, flat, and gave the fixed point iteration. In the same year Rasche and colleagues treated resampling between arbitrary grids by convolution. Later work replaced density weights in many uses by iterative least squares with the [nonuniform FFT](/nonuniform-fft/).

## References
