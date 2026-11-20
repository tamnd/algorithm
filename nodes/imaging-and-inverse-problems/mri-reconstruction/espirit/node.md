---
tag: CN1ST0
kind: algorithm
slug: espirit
name: ESPIRiT
aliases:
- eigenvector-based SPIRiT
area: imaging-and-inverse-problems/mri-reconstruction
level: research
summary: "Estimates coil sensitivity maps from calibration k-space: the null space of the calibration matrix defines a small matrix at each pixel, and its eigenvector with eigenvalue 1 is the map."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", c: "the number of coils", K: "the number of kernel positions per coil", a: "the side of the square ACS block"}
  time: {worst: "O(a^2 c^2 K^2 + c^3 K^3 + n^2 c^2 K^2)"}
  space: {extra: "O(a^2 c K + c^2 K^2 + c n^2)"}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2014
  people: [Martin Uecker, Peng Lai, Mark J. Murphy, Patrick Virtue, Michael Elad, John M. Pauly, Shreyas S. Vasanawala, Michael Lustig]
  note: Uecker and colleagues showed that the SPIRiT consistency condition defines coil maps as eigenvectors, which joins the k-space and the image space views of parallel imaging.
prereqs: [spirit, singular-value-decomposition]
see_also: [sense, coil-sensitivity-map, grappa, cg-sense, power-iteration, jacobi-eigenvalue-algorithm, principal-component-analysis, root-sum-of-squares-coil-combination]
sources:
  - paper: doi:10.1002/mrm.24751
    title: Martin Uecker, Peng Lai, Mark J. Murphy, Patrick Virtue, Michael Elad, John M. Pauly, Shreyas S. Vasanawala and Michael Lustig, ESPIRiT, an eigenvalue approach to autocalibrating parallel MRI, where SENSE meets GRAPPA, Magnetic Resonance in Medicine 71(3), 2014, 990 to 1001
    locator: the calibration matrix and its null space, the pointwise eigenvalue problem with eigenvalue 1, the thresholds, and the multiple sets of maps (general locator; section and equation numbers not confirmed)
  - paper: doi:10.1002/mrm.22428
    title: Michael Lustig and John M. Pauly, SPIRiT, iterative self-consistent parallel imaging reconstruction from arbitrary k-space, Magnetic Resonance in Medicine 64(2), 2010, 457 to 471
    locator: the calibration consistency condition that ESPIRiT turns into an eigenvalue problem (general locator)
  - paper: doi:10.1002/(SICI)1522-2594(200005)43:5<682::AID-MRM10>3.0.CO;2-G
    title: David O. Walsh, Arthur F. Gmitro and Michael W. Marcellin, Adaptive reconstruction of phased array MR imagery, Magnetic Resonance in Medicine 43(5), 2000, 682 to 690
    locator: the earlier map estimate from the dominant eigenvector of the local signal correlation matrix (general locator)
---

ESPIRiT estimates the [coil sensitivity maps](/coil-sensitivity-map/) of a multi-coil MR scan from a small fully sampled calibration region at the center of k-space. It puts all patches of the calibration k-space of all coils into a matrix and splits the patch space into a signal space and a null space with the [singular value decomposition](/singular-value-decomposition/). The null space turns, pixel by pixel, into a small $c \times c$ matrix, and the coil map at that pixel is the eigenvector with eigenvalue 1. The maps then go into [SENSE](/sense/) or [CG-SENSE](/cg-sense/). Uecker and colleagues published the method in 2014. When the maps have a finite k-space support and the calibration is rich enough, the method returns the normalized maps exactly (a theorem).

## In plain words

The calibration region tells us which combinations of neighboring k-space samples of all coils always give zero. Each such rule, moved to the image domain, says that at each pixel the coil values are perpendicular to a certain vector. Collect all these vectors at a pixel: the coil profile must be perpendicular to all of them. ESPIRiT builds a small matrix at each pixel that keeps exactly what is perpendicular to them, and reads off the coil profile as the direction that the matrix does not change. Where there is no signal, no direction survives, and the map is set to zero.

## The problem

The input is the multi-coil k-space $x_b$, $b = 1, \ldots, c$, on an $n \times n$ grid, of which only the central $a \times a$ block (the ACS block) is used. The kernel size $k_r \times k_c$, with $K = k_r k_c$, the signal threshold $t_s$ and the eigenvalue threshold $t_e$ are choices; the code uses $3 \times 3$, $t_s = 10^{-3}$ and $t_e = 0.9$ by default. The output is a map $m_b(p)$ for every coil and pixel, with $\sum_b |m_b(p)|^2 = 1$ and $m_0(p)$ real and positive where the map is kept, and the top eigenvalue at each pixel. The maps match the true maps $s_b(p)$ up to a scalar factor at each pixel, which goes into the image.

## The algorithm

```pseudo id=main
ESPIRIT(x, ACS, k_r, k_c, t_s, t_e)
L1  A <- one row per k_r x k_c patch of the ACS block, entry (b, d) = x_b(kappa + d);
        V <- right singular vectors of A with sigma > t_s sigma_1
L2  N_v <- the number of kept vectors
L3  for each pixel p do
L4      a_l(p)[b] <- sum over d of conj(v_l(b, d)) exp(2 pi i d . p / n), for l = 1, ..., N_v
L5      G(p) <- (1/K) sum over l of a_l(p) a_l(p)^H
L6      (lambda_1, u) <- largest eigenvalue of G(p) and its unit eigenvector
L7      if lambda_1 >= t_e then m(p) <- u / (u_0 / |u_0|) else m(p) <- 0
L8  return m and lambda_1 at every pixel
```

Line L1 takes the singular vectors from the Hermitian eigenproblem of $A^H A$, a matrix of size $c K$; the code uses the complex [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/). Line L4 is the inverse DFT of the kernel $\bar v_l$ of each coil, taken at one pixel. Line L5 sums over the kept vectors; by Lemma 2 of the proof this is the identity minus the same sum over the discarded vectors, so the null space decides the result. Line L7 fixes the free phase of the eigenvector and masks pixels with a small top eigenvalue.

## Example

Four coils, $3 \times 3$ kernel, no noise. The band maps have only the image frequencies 0 and 1 on each axis; the ring maps are smooth Gaussian profiles, see [coil sensitivity map](/coil-sensitivity-map/). The map error is the Euclidean norm of the difference between the normalized true map and the estimate at a pixel (measurements with the code of this page).

| grid | maps and object | ACS | $t_s$ | result |
|---|---|---|---|---|
| $16 \times 16$ | band, Shepp-Logan | 10 | $10^{-3}$ | 16 of 36 vectors kept, gap above $10^4$; eigenvalue 1 and map error below $10^{-9}$ at every pixel |
| $32 \times 32$ | band, Shepp-Logan | 12 | $10^{-3}$ | 16 large singular values, then a gap of several orders of magnitude to the rest |
| $16 \times 16$ | ring, disk of radius 0.75 | 10 | 0.02 | inside: eigenvalue at least 0.9989, map error at most 0.035, mean 0.010; outside: eigenvalue mean 0.929, least 0.626 |
| $32 \times 32$ | ring, disk of radius 0.75 | 12 | 0.02 | map error at most 0.053 inside |
| $16 \times 16$ | ring, disk of radius 0.75 | 10 | $10^{-3}$ | 32 of 36 vectors kept, so too few null vectors remain |

The band maps meet the model of the theorem, and the result is exact up to rounding. The ring maps do not: the singular values decay without a clear gap, and the threshold $t_s$ decides how many vectors count as signal. With $t_e = 0.99$, many pixels outside the disk are masked, while all pixels inside are kept. A [SENSE](/sense/) reconstruction at $R = 2$ with the band ESPIRiT maps reproduces the coil images to $10^{-9}$ (measurement, the test of this page). The tests run on $16 \times 16$ grids to keep the run time short.

## Correctness

A vector $v$ with $A v = 0$ for all patches of the whole k-space gives, in the image domain, $a_v(p)^H f(p) = 0$ at every pixel. The sum of $a_v(p) a_v(p)^H$ over all singular vectors is $K I$, so $G(p)$ is the identity minus a positive semidefinite part built from the null space, and its eigenvalues lie in $[0, 1]$. If the maps are trigonometric polynomials with a fixed finite set of frequencies and the calibration data contain enough independent object patterns, the null space of the calibration matrix is the null space of the whole k-space, and then $G(p) s(p) = s(p)$ at every pixel. If the eigenvalue 1 is simple, line L7 returns $s(p)/\lVert s(p)\rVert$ with the phase of coil 0 removed. The [proof](proofs/correctness.md) gives the details. These are theorems for maps with a finite k-space support; for real coils the quality of the maps is a measurement.

## Complexity

In the [real RAM](/real-ram/): line L1 forms $A^H A$ from about $a^2$ patches in $O(a^2 c^2 K^2)$ and solves the eigenproblem of size $c K$ in $O(c^3 K^3)$ per Jacobi sweep, with a number of sweeps that is small in practice (a heuristic). At each of the $n^2$ pixels, line L4 costs $O(N_v c K)$, line L5 costs $O(N_v c^2)$ and line L6 costs $O(c^3)$ per sweep. With $N_v \le c K$, the total is $O(a^2 c^2 K^2 + c^3 K^3 + n^2 c^2 K^2)$. Practical codes compute line L4 for all pixels with FFTs, $O(N_v c\, n^2 \log n)$, and use [power iteration](/power-iteration/) for the top eigenvector. The memory holds the patches, the Gram matrix and the maps.

## Properties

- **Eigenvalues in $[0, 1]$.** For any data and any threshold, $0 \preceq G(p) \preceq I$ (theorem).
- **Exact for band-limited maps.** Under the model and the rich calibration assumption, the true map is an eigenvector with eigenvalue 1 at every pixel (theorem). With a simple eigenvalue, the method returns it normalized (theorem).
- **Maps up to a pixelwise factor.** The maps have unit norm across coils at each pixel. The missing factor $\lVert s(p) \rVert$ and the phase go into the image, so the coil images are unchanged (theorem, corollary of the proof).
- **Built-in mask.** Outside the object, the top eigenvalue drops below 1, and the threshold $t_e$ masks those pixels (measurement for the ring maps). This mask also suppresses the noise outside the object in a SENSE reconstruction.
- **Same calibration as GRAPPA and SPIRiT.** ESPIRiT needs only the ACS block that [GRAPPA](/grappa/) and [SPIRiT](/spirit/) use, no extra reference scan.

## Variants and improvements

- **Several sets of maps.** If the eigenvalue 1 is not simple, for example when the object is larger than the field of view, Uecker et al. (2014) keep two or more eigenvectors as separate sets of maps, and the SENSE model uses one image per set.
- **Soft weighting.** Instead of the hard mask of line L7, the maps can be weighted by a function of the eigenvalue.
- **Fast versions.** Practical codes compute $G(p)$ with FFTs of the zero-padded kernels, on a coarse grid with interpolation, and find the top eigenvector by [power iteration](/power-iteration/).
- **Walsh maps.** Walsh, Gmitro and Marcellin (2000) take the top eigenvector of the local correlation matrix of the coil images. This needs fully sampled low resolution images and gives no theorem of exactness.
- **SENSE with ESPIRiT maps.** The maps feed [SENSE](/sense/), [CG-SENSE](/cg-sense/), or a reconstruction with a sparsity prior.

## When to use it

Use ESPIRiT to get coil maps from the same calibration data that k-space methods use, when a separate reference scan is not available or not reliable. The maps then allow image domain reconstructions with priors that need an image, not coil images. Use several sets of maps when the field of view is tight. If a body coil reference scan is available and the coil setup does not move, ratio maps are simpler. For a quick combination of fully sampled data, the [root sum of squares](/root-sum-of-squares-coil-combination/) needs no maps at all.

## Pitfalls

- **Wrong signal threshold.** If $t_s$ is too small, line L1 keeps vectors that carry only noise or model error, and the null space is too small to fix the maps (the last row of the example). If $t_s$ is too large, true signal vectors count as null, and the eigenvalue drops inside the object.
- **Missing conjugate.** Line L4 needs $\bar v$, as the proof shows. Without it the matrix $G(p)$ belongs to the mirrored kernel, and the maps are wrong.
- **Phase of the eigenvector.** An eigenvector has a free phase at each pixel. Without the fix of line L7 the maps have random phase jumps, which do no harm in SENSE in exact arithmetic but break smoothness and any phase-based method.
- **Too small a calibration block.** With few patches, $A$ has fewer rows than columns, and the null space contains vectors that are not null for the whole k-space.
- **Masking the object.** A high $t_e$ can mask pixels with weak signal inside the object, which then come out as zero in SENSE.

## Implementations

## History

Walsh, Gmitro and Marcellin estimated maps from local eigenvectors of coil correlation matrices in 2000. Lustig and Pauly introduced the SPIRiT consistency condition in 2010. Uecker, Lai, Murphy, Virtue, Elad, Pauly, Vasanawala and Lustig showed in 2014 that this condition defines the coil maps as eigenvectors with eigenvalue 1 of a pixelwise operator, which links the k-space methods of the [GRAPPA](/grappa/) family with the image space methods of the [SENSE](/sense/) family.

## References
