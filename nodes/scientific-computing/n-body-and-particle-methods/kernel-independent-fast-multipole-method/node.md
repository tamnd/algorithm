---
tag: RS9RNM
kind: algorithm
slug: kernel-independent-fast-multipole-method
name: Kernel-independent fast multipole method
aliases:
- KIFMM
area: scientific-computing/n-body-and-particle-methods
level: research
summary: An FMM that replaces analytic expansions by equivalent densities on surfaces around each box, fitted by small solves, so it works for many kernels.
model: real-ram
complexity:
  vars: {N: the number of charges, P: the number of points on each circle, s: the mean number of charges in a leaf box, L: the leaf level}
  time: {best: "Θ(N P)", average: "Θ(N P^2 / s + N s + L P^3)", worst: "Θ(N^2)"}
  space: {extra: "Θ(N + N P / s + L P^2)"}
properties: {deterministic: true}
history:
  year: 2004
  people: [Lexing Ying, George Biros, Denis Zorin]
  note: Ying, Biros and Zorin published the kernel-independent adaptive FMM in 2D and 3D in the Journal of Computational Physics in 2004.
prereqs: [fast-multipole-method, multipole-to-local-translation, poisson-equation]
see_also: [black-box-fast-multipole-method, adaptive-fast-multipole-method, boundary-element-method, fast-fourier-transform, singular-value-decomposition, tikhonov-regularization, condition-number, pseudoinverse]
sources:
  - paper: doi:10.1016/j.jcp.2003.11.021
    title: "Lexing Ying, George Biros and Denis Zorin, A kernel-independent adaptive fast multipole algorithm in two and three dimensions, Journal of Computational Physics 196(2), 2004, 591-626"
    locator: the equivalent and check surfaces, the three translations as local Dirichlet problems, and the use of the SVD in 2D and the FFT in 3D for the far field translations
  - paper: doi:10.1137/0913055
    title: "Christopher R. Anderson, An implementation of the fast multipole method without multipoles, SIAM Journal on Scientific and Statistical Computing 13(4), 1992, 923-947"
    locator: the representation of the expansions by potential values on a circle or sphere through the Poisson formula
  - url: https://math.nyu.edu/~greengar/shortcourse_fmm.pdf
    title: "Rick Beatson and Leslie Greengard, A short course on fast multipole methods, in Wavelets, Multilevel Methods and Elliptic PDEs, Oxford University Press, 1997"
    locator: Section 4, the tree, the interaction list and the operation count of the FMM that the kernel-independent method keeps
---

The kernel-independent fast multipole method (KIFMM) computes sums $u_j = \sum_{i \ne j} q_i K(z_j, z_i)$ with the tree and the lists of the [fast multipole method](/fast-multipole-method/), but it never expands the kernel $K$. The far field of the charges in a box is represented by an *equivalent density*: values at $P$ points on a circle (in 3D, a sphere or a cube surface) around the box, chosen so that the potential of these points matches the potential of the real charges on a larger *check* circle. The field of all far charges inside a box is represented in the same way, by a density on a circle outside the box that matches on a check circle inside. Every translation is then a set of kernel evaluations and a small linear solve. The kernel must be the fundamental solution of an elliptic equation, for example the Laplace, modified Laplace (Yukawa), Stokes or Navier kernels. Ying, Biros and Zorin (2004) gave the method, building on the "FMM without multipoles" of Anderson (1992).

## In plain words

The plain FMM needs a formula for how the pull of a group changes with distance, and a different formula for each kind of pull. The KIFMM uses a trick that needs no formula. Put a ring of fake charges around a box. Choose their sizes so that, on a second, bigger ring, they pull exactly like the real charges. Then they pull like the real charges everywhere outside the bigger ring too, for the kinds of pull that come from a smooth physical law.

So each box keeps the sizes of its fake charges instead of a formula. Every step of the FMM becomes: compute the pull of some fake charges on a ring, then solve a small system to get new fake charges. You only need a function that gives the pull of one charge on one point.

## The problem

The input is $N$ real charges $q_i$ at points $z_i$ of the unit square, a kernel $K(x, y)$ given as a function, and a number $P$ of points on each circle. The output is an approximation of each potential

$$u_j = \sum_{i \ne j} q_i K(z_j, z_i).$$

The kernel must be the Green's function of a constant coefficient elliptic equation, so that the Dirichlet problems inside and outside a circle have unique solutions, and here it must depend on $x - y$ only, so that the matrices can be computed once per level. The examples use $K = \log|x - y|$ and $K = K_0(2 |x - y|)$, the modified Bessel function.

## The algorithm

A box of half-width $h$ and center $c$ has four circles of $P$ equally spaced points: the upward equivalent circle (radius $1.5h$) and the upward check circle (radius $2.5h$) for the far field of its own charges, and the downward check circle (radius $1.5h$) and the downward equivalent circle (radius $2.5h$) for the field of the far charges inside it. The box fits in the radius $\sqrt{2}\, h$. The matrices $A_{\text{up}} = [K(\text{upward check}_i, \text{upward equivalent}_j)]$ and $A_{\text{down}} = [K(\text{downward check}_i, \text{downward equivalent}_j)]$ are inverted once per level.

```pseudo id=main
KIFMM(q, z, K, P, L)
L1  for each leaf B: φ ← potential of the charges of B at the upward check points of B;  σ↑_B ← A_up⁻¹ φ
L2  for l ← L - 1 down to 2: for each box B at level l: φ ← potential of σ↑ of the children at the upward check points of B;  σ↑_B ← A_up⁻¹ φ
    for l ← 2 to L do
        for each box T at level l do
L3          ψ_T ← Σ potential of σ↑_C at the downward check points of T, over C in the interaction list of T
L4          if l > 2 then ψ_T ← ψ_T + potential of σ↓ of the parent at the downward check points of T
L5          σ↓_T ← A_down⁻¹ ψ_T
L6  for each leaf T and charge j in T: u_j ← potential of σ↓_T at z_j
L7  add the direct terms of all charges i ≠ j in T and its near neighbours; return u
```

Lines L1 to L7 match the steps of the [fast multipole method](/fast-multipole-method/): source to upward (P2M), upward to upward (M2M), the interaction list (M2L, called VLI in the paper), downward to downward (L2L) and downward to targets (L2P). Each translation from a fixed offset is a $P \times P$ matrix of kernel values, also computed once per level and offset: 4 child offsets for each of M2M and L2L, and the $7^2 - 3^2 = 40$ offsets of the interaction list.

The radii are chosen so that each fit is valid where it is used. The upward check circle of a box encloses the upward equivalent circles of its children. The downward check circle of a box in the interaction list is at least $4h - 1.5h = 2.5h$ from the center of the source box, so it is outside the source's upward check circle. The far charges of a box are at least $4h - \sqrt{2}\, h \approx 2.59h$ from its center, outside its downward equivalent circle.

## Example

Take $N = 400$ uniform points in the unit square with charges uniform in $[-1, 1]$ (seed 5), and leaves at level $L = 3$. The near field uses 18302 ordered pairs and there are 1272 M2L products, the same counts as for the analytic FMM on these points. Against direct summation:

| $P$ | relative error, $\log$ kernel (2-norm) | largest error, $\log$ kernel | relative error, $K_0(2r)$ kernel |
|---|---|---|---|
| 4 | $3.5 \times 10^{-2}$ | $1.2$ | |
| 8 | $2.3 \times 10^{-3}$ | $8.5 \times 10^{-2}$ | $3.3 \times 10^{-3}$ |
| 12 | $2.2 \times 10^{-4}$ | $9.1 \times 10^{-3}$ | |
| 16 | $2.0 \times 10^{-5}$ | $6.5 \times 10^{-4}$ | $2.8 \times 10^{-5}$ |
| 24 | $2.3 \times 10^{-7}$ | $7.4 \times 10^{-6}$ | $3.3 \times 10^{-7}$ |
| 32 | $3.0 \times 10^{-9}$ | $1.4 \times 10^{-7}$ | $4.3 \times 10^{-9}$ |
| 40 | $5.0 \times 10^{-11}$ | $3.0 \times 10^{-9}$ | |

These are measurements. The two kernels use the same code; only the function $K$ changes. The error falls by about a factor of 10 for every 4 more points. A density of $P$ real values holds about as much as an analytic expansion of $P / 2$ complex terms, and the analytic FMM with $p = 12$ on these points has the relative error $3.0 \times 10^{-8}$, against $2.3 \times 10^{-7}$ here with $P = 24$.

The fit matters. If the inverses are replaced by the regularized normal equations $(A^T A + \lambda I)^{-1} A^T$ with $\lambda = 10^{-13}$ times the mean of the diagonal, the errors for $P = 24$, $32$ and $40$ are $2.3 \times 10^{-7}$, $7.6 \times 10^{-8}$ and $6.0 \times 10^{-6}$: they stop falling and then grow, because $A^T A$ squares the condition number of $A$.

## Correctness

The proof file is partial. It proves three things for the $\log$ kernel. First, the tree and the lists are those of the uniform FMM, so each charge reaches each target exactly once (Lemma 1). Second, the matrix of $\log|x_i - y_j|$ between two concentric circles of $P$ equally spaced points is circulant, with the eigenvalues $\log(R_>^P - R_<^P)$ and $-\frac{P}{2} \sum_{k \equiv \pm m} \rho^k / k$; so the fits exist whenever $R_>^P - R_<^P \ne 1$, which holds for all radii below 1, and the condition number grows like $\rho^{-P/2}$ (Lemma 2). Third, a continuous density that matches the potential on the whole check circle matches it in the whole far region, by the uniqueness of the exterior and interior Dirichlet problems; so with exact fits every step is exact (Lemma 3). A bound on the error of the $P$-point fits, which alias the Fourier modes they do not resolve, is not proved there; the convergence in $P$ is measured above.

## Complexity

The model is the [real RAM](/real-ram/), with kernel evaluations counted as one operation.

- **Same structure as the FMM (theorem).** The tree and the lists are those of the uniform FMM, so the counts of the operation count of Beatson and Greengard hold with $P \times P$ matrix-vector products in place of the $p^2$ translations: $\Theta(N P)$ for L1 and L6, $\Theta((N / s) P^2)$ for L2 to L5, and $\Theta(N s)$ for L7.
- **Precomputation.** Per level: two $P \times P$ inverses, $O(P^3)$, and $48$ matrices of $P^2$ kernel values. For a kernel that is homogeneous, such as $1 / r$, the matrices are the same at every level after scaling.
- **Faster M2L.** The M2L matrices dominate. In 3D, the paper uses the FFT: on a regular grid of equivalent points, the translation is a convolution. In 2D it compresses them with the [SVD](/singular-value-decomposition/).
- **Worst case.** With a uniform tree, clustered charges make the near field $\Theta(N^2)$; the paper uses the adaptive tree with the lists of the [adaptive FMM](/adaptive-fast-multipole-method/).
- **Space.** $\Theta(N + N P / s)$ for the densities, plus the precomputed matrices.

## Properties

- **Kernel independent.** The code calls $K$ only as a function. A new kernel needs no new formulas.
- **Linear in the charges.** The output is a linear function of $q$, so the method works as a fast matrix-vector product in iterative solvers for [boundary element](/boundary-element-method/) equations.
- **Not every kernel.** The uniqueness argument needs a kernel that solves an elliptic equation. For a smooth kernel that does not, such as a Gaussian, the fits can fail; the [black-box FMM](/black-box-fast-multipole-method/) uses interpolation instead and needs only smoothness.
- **Deterministic.** The result does not depend on the order of the charges, up to rounding.

## Variants and improvements

- **Adaptive trees.** The original method works on an adaptive tree with the $U$, $V$, $W$ and $X$ lists of the [adaptive FMM](/adaptive-fast-multipole-method/); this page uses a uniform tree to keep the code short.
- **FFT acceleration.** With equivalent points on the surface of a cube in a regular grid, the M2L operator is a discrete convolution and the [fast Fourier transform](/fast-fourier-transform/) applies it in $O(P \log P)$ after a zero padded transform.
- **SVD compression.** The M2L matrices can be compressed by a truncated [singular value decomposition](/singular-value-decomposition/), as in the 2D code of the paper and in later SVD-accelerated versions.
- **Regularized fits.** When the check-to-equivalent matrices are ill conditioned, a [Tikhonov](/tikhonov-regularization/) regularized [pseudoinverse](/pseudoinverse/), computed from the SVD and not from the normal equations, limits the growth of rounding errors.
- **Black box versions.** The [black-box FMM](/black-box-fast-multipole-method/) replaces the equivalent densities by Chebyshev interpolation, which needs no uniqueness theorem.

## When to use it

Use the KIFMM when you need a fast summation for a kernel that is a Green's function but whose analytic expansions you do not have or do not want to code: Stokes and elasticity kernels, the modified Laplace kernel, or kernels of a family of equations. For the Laplace and modified Laplace kernels, Ying, Biros and Zorin report that it compares very well with the best analytic FMM codes, so it is a reasonable choice there too. For kernels that are only smooth, use the black-box FMM. For small $N$, use direct summation.

## Pitfalls

- **Radius 1 for the log kernel.** The $\log$ kernel matrix between concentric circles is singular when $R_>^P - R_<^P = 1$, and nearly singular when it is close to 1. Scale the problem so that all circles have radius well below 1, or start the tree at a level where they do.
- **Normal equations.** Forming $A^T A$ squares the condition number; in the example, the error grows from $3 \times 10^{-9}$ to $6 \times 10^{-6}$ at $P = 40$. Invert $A$ directly or use an SVD.
- **Equivalent and check radii.** A check circle that crosses a source box, or an equivalent circle that does not enclose the charges, breaks the uniqueness argument and gives large errors without a warning.
- **Kernels that are not Green's functions.** For a Gaussian kernel, matching on a circle does not determine the field outside, and the method can give poor results.
- **Too few points for the accuracy.** The error falls with $P$ at a rate set by the ratios of the radii, and the rate on this page does not carry over to other radii, other kernels or 3D. Measure against direct summation.

## Implementations

## History

Anderson (1992) represented the multipole and local expansions of the 2D and 3D Laplace kernel by potential values on circles and spheres, through the Poisson formula, an "FMM without multipoles". Ying, Biros and Zorin (2004) turned the idea into a method for general elliptic kernels: equivalent densities fitted on check surfaces by local Dirichlet problems, inside the adaptive FMM, with the SVD in 2D and the FFT in 3D for the far field translations. They tested it on the Laplace, modified Laplace, Stokes, modified Stokes, Navier and modified Navier kernels. Fong and Darve (2009) gave the black-box FMM, based on Chebyshev interpolation, which needs only a smooth kernel.

## References
