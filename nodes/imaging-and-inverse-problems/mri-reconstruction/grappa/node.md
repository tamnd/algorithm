---
tag: KY1RH2
kind: algorithm
slug: grappa
name: GRAPPA
aliases:
- generalized autocalibrating partially parallel acquisitions
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: "Fills the skipped k-space lines of each coil with a small shift-invariant kernel over the acquired neighbors of all coils, fitted by least squares on a fully sampled center block. Needs no coil maps."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: "the side of the n x n k-space", c: "the number of coils", R: "the reduction factor", a: "the number of ACS rows", k: "the number of source positions per coil in the kernel"}
  time: {worst: "O(R a n c^2 k^2 + R c^3 k^3 + c^2 k n^2 + c n^2 log n)"}
  space: {extra: "O(c^2 k^2 + a n c k + c n^2)"}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2002
  people: [Mark A. Griswold, Peter M. Jakob, Robin M. Heidemann, Mathias Nittka, Vladimir Jellus, Jianmin Wang, Berthold Kiefer, Axel Haase]
  note: Griswold and colleagues fitted a separate k-space kernel for each coil from autocalibration lines and combined the coil images afterwards, which made the method robust where SMASH-type methods failed.
prereqs: [k-space, least-squares-problem]
see_also: [spirit, sense, slice-grappa, espirit, g-factor, root-sum-of-squares-coil-combination, coil-sensitivity-map, linear-prediction]
sources:
  - paper: doi:10.1002/mrm.10171
    title: Mark A. Griswold, Peter M. Jakob, Robin M. Heidemann, Mathias Nittka, Vladimir Jellus, Jianmin Wang, Berthold Kiefer and Axel Haase, Generalized autocalibrating partially parallel acquisitions (GRAPPA), Magnetic Resonance in Medicine 47(6), 2002, 1202 to 1210
    locator: the kernel that predicts each coil from the acquired neighbors of all coils, the fit on the autocalibration lines, and the combination of the coil images (general locator; section numbers not confirmed)
  - paper: doi:10.1002/mrm.1910380414
    title: Daniel K. Sodickson and Warren J. Manning, Simultaneous acquisition of spatial harmonics (SMASH), fast imaging with radiofrequency coil arrays, Magnetic Resonance in Medicine 38(4), 1997, 591 to 603
    locator: the synthesis of shifted k-space lines from linear combinations of coil signals (general locator)
  - paper: doi:10.1002/mrm.22066
    title: Felix A. Breuer, Stephan A. R. Kannengiesser, Martin Blaimer, Nicole Seiberlich, Peter M. Jakob and Mark A. Griswold, General formulation for quantitative g-factor calculation in GRAPPA reconstructions, Magnetic Resonance in Medicine 62(3), 2009, 739 to 746
    locator: the image domain form of the GRAPPA kernel and its g-factor (general locator)
  - paper: doi:10.1002/mrm.22428
    title: Michael Lustig and John M. Pauly, SPIRiT, iterative self-consistent parallel imaging reconstruction from arbitrary k-space, Magnetic Resonance in Medicine 64(2), 2010, 457 to 471
    locator: GRAPPA as one step of a k-space consistency condition, and its generalization to any sampling (general locator)
---

GRAPPA (generalized autocalibrating partially parallel acquisitions) reconstructs multi-coil MR data from a Cartesian scan that skips phase encoding lines. It works in [k-space](/k-space/) and needs no [coil sensitivity maps](/coil-sensitivity-map/). A small kernel predicts each missing sample of each coil as a linear combination of the acquired samples of all coils near it. The weights come from a [least squares](/least-squares-problem/) fit on a fully sampled block at the center of k-space, the autocalibration signal (ACS). Each coil image is then an inverse FFT, and the coil images are combined, for example by [root sum of squares](/root-sum-of-squares-coil-combination/). Griswold and colleagues published it in 2002. It is exact when the k-space of the maps has a small support that the kernel spans (a theorem on this page); for real coils it is an approximation.

## In plain words

Each coil sees the body through its own smooth window. In k-space, a smooth window makes each sample a blend of a few neighboring samples of the true object. So the samples of all coils near a missing point already know a lot about that point. GRAPPA learns the recipe, "take this much of coil 1 above, that much of coil 3 below", from the middle of k-space, where nothing is missing. Because the windows are the same everywhere, the same recipe works on every missing line.

## The problem

The input is the k-space of $c$ coils on an $n \times n$ grid, with the rows $\kappa \equiv 0 \pmod R$ acquired and a block of $a$ consecutive ACS rows at the center also acquired. The other rows are missing. The kernel shape is a choice: the code uses source rows $\kappa - \delta + Rt$ for $t$ in a block of $n_b$ values and the columns $l - w, \ldots, l + w$, where $\delta = \kappa \bmod R$. The output is the full k-space of every coil. The model is $y_k = M F_u (s_k x)$, but the maps $s_k$ are not inputs.

## The algorithm

```pseudo id=main
GRAPPA(y, R, ACS, kernel shape)
L1  for delta = 1, ..., R - 1 do      ▷ one kernel per row offset
L2      collect, over the ACS rows kappa whose sources lie in the ACS block and all columns l,
            the source vector u(kappa, l) = (y_b(kappa + o))_{b, o in O_delta} and the targets (y_a(kappa, l))_a
L3      W_delta <- least squares solution of U W = Y (small Tikhonov term)
L4  for each missing row kappa do
L5      delta <- kappa mod R
L6      for each column l do
L7          u <- (y_b(kappa + o))_{b, o in O_delta}    ▷ acquired samples only
L8          y_a(kappa, l) <- sum_s u_s W_delta[s][a] for every coil a
L9  return y
```

Line L2 builds the calibration matrix: one row per target position, one column per source (coil and offset). Line L3 solves the normal equations with a small multiple of the trace on the diagonal, which keeps the system solvable when it is nearly singular. Line L7 reads only rows $\equiv 0 \pmod R$, which the scan acquired. Line L8 fills all coils at once. The acquired rows, the ACS rows among them, are kept. The kernel size, the number of ACS rows and the regularization are design choices and are tuned in practice (Griswold et al. 2002).

## Example

The table shows the relative k-space error over all coils and samples, which by Parseval equals the relative error of the coil images, for a $32 \times 32$ modified Shepp-Logan phantom and four coils, without noise (measurement with the code of this page, regularization $10^{-10}$). The band maps have only the image frequencies 0 and 1 on each axis; the ring maps are smooth Gaussian profiles, see [coil sensitivity map](/coil-sensitivity-map/). "Zero filled" is the error with the missing rows set to 0.

| maps | $R$ | ACS rows | kernel ($n_b \times (2w+1)$) | GRAPPA error | zero filled |
|---|---|---|---|---|---|
| band | 2 | 12 | $2 \times 3$ | $1.1 \times 10^{-9}$ | 0.400 |
| band | 2 | 8 | $2 \times 3$ | $1.5 \times 10^{-9}$ | 0.464 |
| band | 4 | 16 | $2 \times 3$ | 0.272 | 0.451 |
| band | 4 | 16 | $4 \times 5$ | 1.00 | 0.451 |
| ring | 2 | 12 | $2 \times 3$ | 0.013 | 0.395 |
| ring | 2 | 8 | $2 \times 3$ | 0.023 | 0.466 |
| ring | 4 | 16 | $2 \times 3$ | 0.137 | 0.437 |
| ring | 4 | 16 | $4 \times 5$ | 0.115 | 0.437 |

For the band maps at $R = 2$ the kernel spans the target, and the error is at the rounding level, as the theorem says. At $R = 4$ the kernel does not span it, and the error is large. The large $4 \times 5$ kernel on the band maps shows the danger of a fit with more unknowns than the calibration data support: the calibration matrix is nearly singular, and the weights that fit the ACS block fail elsewhere.

## Correctness

Assume the coil k-space is the object k-space convolved with a kernel of finite support $H$, which holds when the maps are trigonometric polynomials. Then each source and each target is a linear function of the object samples in a small window around the target. If the targets lie in the span of the sources, an exact kernel exists. If the calibration data contain enough independent object patterns, every solution of the fit is that exact kernel on the level of the object samples, so it is exact at every missing position. The [proof](proofs/correctness.md) gives the details. This is a theorem about maps with a finite k-space support; real maps are smooth but not band-limited, and the error for them is a measurement.

## Complexity

In the [real RAM](/real-ram/), with $m = c k$ sources per kernel: for each of the $R - 1$ offsets, line L2 collects up to $a n$ calibration rows, forming the normal equations costs $O(a n m^2)$, and solving them costs $O(m^3)$. Lines L4 to L8 compute $c$ outputs from $m$ sources for each of the fewer than $n^2$ missing samples, $O(c m n^2)$. The coil images need $c$ inverse FFTs, $O(c n^2 \log n)$. The total is $O(R a n c^2 k^2 + R c^3 k^3 + c^2 k n^2 + c n^2 \log n)$. The memory holds the normal equations, $O(c^2 k^2)$, the calibration rows, $O(a n c k)$, and the k-space, $O(c n^2)$. The method is not iterative.

## Properties

- **Exact for band-limited maps.** Under the span and calibration assumptions, the output is the full k-space (theorem).
- **No maps.** The method needs no map estimate, so it does not fail where a map estimate is poor, for example at the edge of the object or when the field of view is tight.
- **Linear.** For fixed weights, the output is a linear function of the data, so its noise is described by a [g-factor](/g-factor/) (Breuer et al. 2009).
- **Coil images, not one image.** The output is one image per coil; the final image needs a coil combination, which adds its own noise properties.
- **Cartesian.** The kernel assumes the same pattern of neighbors at every missing sample. Irregular patterns need one kernel per pattern, or [SPIRiT](/spirit/).

## Variants and improvements

- **SPIRiT.** [SPIRiT](/spirit/) uses a kernel over all neighbors, acquired or not, and asks that the whole k-space be consistent with it. It works for any sampling and reduces to a GRAPPA-like step for uniform patterns. GRAPPA computes the missing samples in one pass; SPIRiT solves for them iteratively.
- **Slice-GRAPPA.** [Slice-GRAPPA](/slice-grappa/) uses one kernel per slice to separate simultaneously excited slices.
- **Image domain GRAPPA.** The kernel is a convolution, so it can be applied as a pixelwise multiplication of the coil images, which is faster for large kernels and gives the g-factor map.
- **SENSE.** [SENSE](/sense/) uses explicit maps instead of a kernel. With good maps it gives the optimal noise for the model; [ESPIRiT](/espirit/) links the two views.
- **Regularized fits.** Larger Tikhonov terms in line L3 lower the noise of the kernel at the cost of residual aliasing; the weight is tuned.

## When to use it

Use GRAPPA for Cartesian scans with uniform undersampling and a fully sampled center, when coil maps are not available or not reliable, for example with a tight field of view, motion between a map scan and the main scan, or a body region with fast changing maps. Keep $R$ well below the number of coils, and collect enough ACS rows for the kernel: the ACS block must hold many more independent rows than the kernel has weights. For non-Cartesian or random patterns use [SPIRiT](/spirit/) or [CG-SENSE](/cg-sense/).

## Pitfalls

- **Too few ACS rows.** If line L2 collects fewer independent patterns than the kernel has weights, the fit of line L3 is underdetermined, and the kernel can fit the ACS block and fail elsewhere (the $4 \times 5$ row of the table).
- **Kernel too small.** If the sources of line L7 do not span the target, the error stays large however good the calibration is (the $R = 4$ rows of the table).
- **No regularization.** With $\lambda = 0$ the normal equations of line L3 can be singular for clean synthetic data and badly conditioned for real data.
- **Wrong row offset.** Line L5 must pick the kernel by $\kappa \bmod R$; using one kernel for all offsets mixes up the neighbor patterns.
- **Combining badly.** A root sum of squares of the output coil images carries the noise bias and the coil shading of [RSS](/root-sum-of-squares-coil-combination/).
- **Motion in the ACS.** If the ACS block comes from a separate scan, motion or contrast changes between the scans make the kernel wrong.

## Implementations

## History

Sodickson and Manning showed in 1997 with SMASH that combinations of coil signals can synthesize shifted k-space lines. Jakob, Griswold, Heidemann and colleagues then added autocalibration lines in AUTO-SMASH and VD-AUTO-SMASH. Griswold, Jakob, Heidemann, Nittka, Jellus, Wang, Kiefer and Haase published GRAPPA in 2002: a kernel over several neighboring lines for each coil, fitted on the ACS lines, and a coil combination at the end. Lustig and Pauly generalized it to any sampling with [SPIRiT](/spirit/) in 2010, and Setsompop and colleagues used the same idea for simultaneous multi-slice imaging with [slice-GRAPPA](/slice-grappa/) in 2012.

## References
