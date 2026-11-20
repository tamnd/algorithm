---
tag: VXHK1N
kind: algorithm
slug: spirit
name: SPIRiT
aliases:
- iterative self-consistent parallel imaging
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: "Finds the missing multi-coil k-space samples for any sampling pattern by asking that every sample agree with a calibrated kernel over its neighbors, solved by CGLS with the acquired samples kept."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: "the side of the n x n k-space", c: "the number of coils", q: "the number of kernel positions per coil", a: "the number of calibration rows", K: "the number of iterations"}
  time: {worst: "O(a n c^2 q^2 + c^4 q^3 + K c^2 q n^2)"}
  space: {extra: "O(c^2 q^2 + a n c q + c n^2)"}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2010
  people: [Michael Lustig, John M. Pauly]
  note: Lustig and Pauly turned the GRAPPA kernel into a consistency condition on the whole k-space, which works for any sampling pattern and combines with sparsity priors.
prereqs: [grappa, conjugate-gradient-method]
see_also: [espirit, cg-sense, sense, cgls, compressed-sensing-mri, loraks, least-squares-problem, k-space-trajectory]
sources:
  - paper: doi:10.1002/mrm.22428
    title: Michael Lustig and John M. Pauly, SPIRiT, iterative self-consistent parallel imaging reconstruction from arbitrary k-space, Magnetic Resonance in Medicine 64(2), 2010, 457 to 471
    locator: the calibration consistency equation x = G x, the data consistency constraint, and the conjugate gradient solution (general locator; section and equation numbers not confirmed)
  - paper: doi:10.1002/mrm.10171
    title: Mark A. Griswold, Peter M. Jakob, Robin M. Heidemann, Mathias Nittka, Vladimir Jellus, Jianmin Wang, Berthold Kiefer and Axel Haase, Generalized autocalibrating partially parallel acquisitions (GRAPPA), Magnetic Resonance in Medicine 47(6), 2002, 1202 to 1210
    locator: the k-space kernel fitted on autocalibration data that SPIRiT generalizes (general locator)
  - paper: doi:10.6028/jres.049.044
    title: Magnus R. Hestenes and Eduard Stiefel, Methods of conjugate gradients for solving linear systems, Journal of Research of the National Bureau of Standards 49(6), 1952, 409 to 436
    locator: the conjugate gradient method on the normal equations of a least squares problem, the form now called CGLS (general locator)
  - paper: doi:10.1109/TMI.2012.2188039
    title: Mark Murphy, Marcus Alley, James Demmel, Kurt Keutzer, Shreyas Vasanawala and Michael Lustig, Fast l1-SPIRiT compressed sensing parallel imaging MRI, scalable parallel implementation and clinically feasible runtime, IEEE Transactions on Medical Imaging 31(6), 2012, 1250 to 1262
    locator: the combination of SPIRiT with a sparsity term and a fast parallel implementation (general locator)
---

SPIRiT (iterative self-consistent parallel imaging reconstruction) fills the missing k-space samples of a multi-coil MR scan for any sampling pattern. Like [GRAPPA](/grappa/), it fits a kernel on a fully sampled calibration region. Unlike GRAPPA, the kernel predicts each sample of each coil from all its neighbors in all coils, acquired or not. SPIRiT then asks for a full k-space that agrees with the kernel everywhere and with the data on the acquired samples, and solves this [least squares problem](/least-squares-problem/) with [CGLS](/cgls/). Lustig and Pauly published it in 2010. The consistency residual decreases at every step (a theorem), and the result is exact when the kernel is consistent with the true k-space and the missing samples are determined.

## In plain words

In the middle of k-space every sample is known, so we can learn how each sample follows from its neighbors in all coils. That rule should hold everywhere. Where samples are missing, we look for the values that make the rule hold as well as possible, while the measured samples stay as they are. GRAPPA uses the rule once, with only measured neighbors. SPIRiT uses it everywhere at once and solves for all missing values together, so it does not care which samples are missing.

## The problem

The input is the multi-coil k-space $y$ on the acquired samples of an $n \times n$ grid, the sampling mask, which can be any pattern, and a block of $a$ fully sampled calibration rows at the center. The kernel size $k_r \times k_c$ and the regularization of the fit are choices. The output is the full k-space $x$ of every coil, with $x = y$ on the acquired samples, that minimizes $\lVert (G - I) x \rVert^2$, where $G$ is the calibrated kernel operator. The model is $y_k = M F_u(s_k x)$, but the maps are not inputs.

## The algorithm

$P$ selects the missing samples, and $P^{\mathsf T}$ puts values on them. The unknowns $z$ are the missing values.

```pseudo id=main
SPIRIT(y, mask, ACS, kernel shape, iters)
L1  G <- fit of each sample from its k_r x k_c neighbors in all coils, without itself, on the ACS rows
L2  x0 <- y on the acquired samples, 0 elsewhere
L3  B z = (G - I) P^T z;  B^H w = P (G^H - I) w
L4  r <- -(G - I) x0; z <- 0; s <- B^H r; p <- s
L5  for t = 1, ..., iters do
L6      q <- B p
L7      alpha <- ||s||^2 / ||q||^2
L8      z <- z + alpha p; r <- r - alpha q
L9      s_new <- B^H r; p <- s_new + (||s_new||^2 / ||s||^2) p; s <- s_new
L10 return x0 + P^T z
```

Line L1 solves one small regularized least squares problem per target coil: the sources are all patch entries of all coils except the target sample itself. Line L3 defines the operator on the missing samples; it applies the kernel as a sum of shifted copies of the coil arrays. Lines L4 to L9 are CGLS for $\min_z \lVert B z - r \rVert^2$, which is $\lVert (G - I)(x_0 + P^{\mathsf T} z) \rVert^2$. The acquired samples never change. Each iteration applies $G$ once and $G^H$ once.

## Example

Four coils, a modified Shepp-Logan phantom, no noise, a $3 \times 3$ kernel. The table gives the relative error of the full k-space against the truth (measurement with the code of this page). The band maps have only the image frequencies 0 and 1 on each axis; the ring maps are smooth Gaussian profiles, see [coil sensitivity map](/coil-sensitivity-map/).

| grid | maps | sampling | calibration rows | iterations | SPIRiT error | zero filled |
|---|---|---|---|---|---|---|
| $32 \times 32$ | band | every 2nd row | 8 | 40 | $8.7 \times 10^{-9}$ | 0.464 |
| $32 \times 32$ | ring | every 2nd row | 8 | 40 | 0.080 | 0.466 |
| $32 \times 32$ | band | every 3rd row | 10 | 40 | 0.358 | |
| $16 \times 16$ | band | every 2nd row | 8 | 20 | $4.8 \times 10^{-9}$ | |
| $16 \times 16$ | ring | calibration rows, then each other sample with probability 0.5 | 8 | 25 | 0.148 | 0.370 |

The first row is exact up to rounding, as part 3 of the theorem says. In the third row the consistency residual fell to $4 \times 10^{-7}$ while the error stayed at 0.358: the kernel is consistent with the truth, but other k-spaces fit as well, so the missing samples are not determined. The tests of this page run on $16 \times 16$ grids to keep the run time short.

## Correctness

CGLS is the conjugate gradient method on the normal equations $B^H B z = B^H r_0$. Its iterates minimize the residual over a growing Krylov subspace, so the consistency residual $\lVert (G - I) x \rVert$ does not increase, and the method reaches a minimizer after at most as many steps as there are missing samples. If the true k-space $k$ satisfies $G k = k$, it is a minimizer with residual 0, and it is the only one when no nonzero k-space that is zero on the acquired samples satisfies $G v = v$. A kernel with $G k = k$ exists, and the fit finds it, under the band-limited map model of the [GRAPPA](/grappa/) proof. The [proof](proofs/correctness.md) gives the details. These are theorems in exact arithmetic.

## Complexity

In the [real RAM](/real-ram/), with $q = k_r k_c$: line L1 forms one Gram matrix of size $c q$ from about $a n$ patches, $O(a n c^2 q^2)$, and solves $c$ systems of size $c q - 1$, $O(c^4 q^3)$. One application of $G$ or $G^H$ costs $O(c^2 q n^2)$, so each iteration costs $O(c^2 q n^2)$, and $K$ iterations cost $O(K c^2 q n^2)$. Applying the kernel in the image domain, as a pixelwise $c \times c$ matrix after FFTs, costs $O(c^2 n^2 + c n^2 \log n)$ per application instead. The memory holds the Gram matrix, the patches and a few k-space arrays, $O(c^2 q^2 + a n c q + c n^2)$. The number of iterations depends on the conditioning of $B$; the bound of at most one step per missing sample holds only in exact arithmetic.

## Properties

- **Monotone consistency residual.** $\lVert (G - I) x_t \rVert$ does not increase (theorem). The test of this page checks it at every step. The error against the truth is not proved monotone.
- **Exact under consistency and uniqueness.** If $G k = k$ and the missing samples are determined, the method returns $k$ (theorem). The test checks it for band maps at $R = 2$ with junk in the missing samples, which are never read.
- **Any sampling.** The kernel uses all neighbors, so the same kernel works for uniform, random, variable density and, with gridding, non-Cartesian patterns.
- **Coil images out.** Like GRAPPA, the method returns one k-space per coil, and a coil combination follows.
- **Linear.** For a fixed kernel and a fixed number of iterations, the output is linear in the data.

## Variants and improvements

- **Data weighting.** Lustig and Pauly (2010) also give a form where the data term $\lVert M x - y \rVert^2$ is weighted against the consistency term, for noisy data.
- **L1-SPIRiT.** Adding a sparsity term, as in [compressed sensing MRI](/compressed-sensing-mri/), regularizes the solution; Murphy et al. (2012) made it fast enough for clinical use.
- **Non-Cartesian SPIRiT.** With a gridding operator in the data term, the consistency is imposed on a Cartesian grid while the data are on a trajectory.
- **ESPIRiT.** [ESPIRiT](/espirit/) shows that the consistency condition $G x = x$ is the same as a set of coil maps, which turns SPIRiT into a SENSE-type problem with maps from the calibration data.
- **Low-rank methods.** Structured low-rank methods such as [LORAKS](/loraks/) impose the null space of the calibration matrix directly, without a fitted kernel.
- **Image space methods.** [CG-SENSE](/cg-sense/) solves the same kind of least squares problem with explicit maps.

## When to use it

Use SPIRiT when the sampling is not uniform, for example random or variable density patterns for compressed sensing, or when the coil maps are hard to estimate, and when a fully sampled calibration region is available. It is a natural base for combination with sparsity. For uniform Cartesian undersampling, [GRAPPA](/grappa/) is faster and gives a similar result. When good maps are available or can be computed with [ESPIRiT](/espirit/), a SENSE-type reconstruction has fewer unknowns.

## Pitfalls

- **Including the target in the kernel.** If line L1 lets a sample predict itself, the fit returns the identity, and $G - I = 0$: every k-space is consistent.
- **Too few calibration rows.** As for GRAPPA, an underdetermined fit in line L1 gives a kernel that fits the calibration region and fails elsewhere.
- **Non-unique solution.** If $B$ has a null space, the consistency residual goes to zero while the error stays large (the third row of the example). More samples or a prior, such as sparsity, fix it.
- **Overwriting the data.** The unknowns are only the missing samples (line L3). Letting CGLS change the acquired samples loses the data constraint.
- **Wrong adjoint.** Line L3 needs the exact adjoint of $G$, with the shift $-d$ and the conjugated weights. A wrong adjoint breaks the monotone residual.
- **Running long on noisy data.** With noise, the late iterations fit noise into the missing samples; stop early or add a data weight or a prior.

## Implementations

## History

Griswold and colleagues published [GRAPPA](/grappa/) in 2002, with a kernel over the acquired neighbors only. Lustig and Pauly published SPIRiT in 2010: a kernel over all neighbors, a consistency equation on the whole k-space, and an iterative solution that works for any sampling, with sparsity priors as an option. Murphy and colleagues made L1-SPIRiT fast in 2012, and Uecker and colleagues explained the consistency condition through coil maps with [ESPIRiT](/espirit/) in 2014.

## References
