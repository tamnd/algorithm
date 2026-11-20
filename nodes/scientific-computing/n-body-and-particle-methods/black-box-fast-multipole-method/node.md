---
tag: T616YW
kind: algorithm
slug: black-box-fast-multipole-method
name: Black-box fast multipole method
aliases:
- bbFMM
- Chebyshev fast multipole method
area: scientific-computing/n-body-and-particle-methods
level: research
summary: An FMM for any smooth kernel that interpolates the kernel at Chebyshev nodes and compresses the multipole-to-local operators by singular value decomposition.
model: real-ram
complexity:
  vars: {N: the number of charges, n: the number of Chebyshev nodes in each coordinate, s: the mean number of charges in a leaf box, L: the leaf level}
  time: {best: "Θ(N n^2)", average: "Θ(N n^2 + N n^4 / s + N s + L n^4)", worst: "Θ(N^2)"}
  space: {extra: "Θ(N + N n^2 / s + L n^4)"}
properties: {deterministic: true}
history:
  year: 2009
  people: [William Fong, Eric Darve]
  note: Fong and Darve published the black-box FMM, based on Chebyshev interpolation and SVD compression, in the Journal of Computational Physics in 2009.
prereqs: [fast-multipole-method, chebyshev-interpolation, multipole-to-local-translation]
see_also: [kernel-independent-fast-multipole-method, chebyshev-polynomials, chebyshev-nodes, singular-value-decomposition, adaptive-fast-multipole-method, lagrange-interpolation, boundary-element-method, gaussian-process]
sources:
  - paper: doi:10.1016/j.jcp.2009.08.031
    title: "William Fong and Eric Darve, The black-box fast multipole method, Journal of Computational Physics 228(23), 2009, 8712-8725"
    locator: the sections on Chebyshev interpolation, the black-box FMM with Chebyshev interpolation, and the fast convolution by SVD compression
  - book: isbn:9781611972399
    title: "Lloyd N. Trefethen, Approximation Theory and Approximation Practice, SIAM, 2013"
    locator: Chapter 8, Theorems 8.1 and 8.2, the decay of the Chebyshev coefficients and the accuracy of Chebyshev approximations of analytic functions
  - url: https://math.nyu.edu/~greengar/shortcourse_fmm.pdf
    title: "Rick Beatson and Leslie Greengard, A short course on fast multipole methods, in Wavelets, Multilevel Methods and Elliptic PDEs, Oxford University Press, 1997"
    locator: Section 4, the tree, the interaction list and the operation count of the FMM that the black-box method keeps
---

The black-box fast multipole method (bbFMM) computes sums $u_j = \sum_{i \ne j} q_i K(z_j, z_i)$ with the tree and the lists of the [fast multipole method](/fast-multipole-method/), for any kernel $K$ that is smooth away from $x = y$ and that the code can only evaluate. For two well separated boxes, it replaces $K$ by its [Chebyshev interpolant](/chebyshev-interpolation/) in all coordinates of both points. The multipole expansion of a box becomes a set of weights at the [Chebyshev nodes](/chebyshev-nodes/) of the box, the local expansion becomes a set of values at the same nodes, and the multipole-to-local operator becomes a matrix of kernel values between two sets of nodes. Fong and Darve (2009) gave the method and compressed these matrices with the [singular value decomposition](/singular-value-decomposition/), so that the far field uses close to the smallest number of coefficients for a given accuracy.

## In plain words

The plain FMM needs a formula for how the pull of a group of charges changes with distance. The black-box FMM only asks for a function that gives the pull of one charge on one point.

For two boxes that are far apart, the pull changes smoothly across each box. A smooth function is well described by its values on a small grid of special points, packed more closely near the edges. So each box spreads its charges onto its grid points, the pull is computed only from grid points to grid points, and each target reads its value back from the grid of its own box. Passing values between a box and its children is exact, because a parent's smooth shape is also smooth inside each child.

More grid points give more digits. Near boxes are still added one pair at a time.

## The problem

The input is $N$ charges $q_i$ at points $z_i$ of the unit square, a kernel $K(x, y)$ given as a function, and a number $n$ of nodes in each coordinate. The output is an approximation of each potential

$$u_j = \sum_{i \ne j} q_i K(z_j, z_i).$$

The kernel must be smooth when $x$ and $y$ lie in two well separated boxes; it does not have to solve any equation. Here it must also depend on $x - y$ only, so that the matrices can be computed once per level. The examples use $\log|x - y|$, $1 / |x - y|$ and the inverse multiquadric $(|x - y|^2 + 0.01)^{-1/2}$.

## The algorithm

Let $\bar x_m = \cos((2m - 1)\pi / (2n))$, $m = 1, \ldots, n$, be the Chebyshev nodes on $[-1, 1]$, and

$$S_n(\bar x_m, t) = \frac{1}{n} + \frac{2}{n} \sum_{k=1}^{n-1} T_k(\bar x_m) T_k(t),$$

which is the Lagrange polynomial of the node $\bar x_m$. Map each box $B$ to $[-1, 1]^2$ and write $S_B(m, x) = S_n(\bar x_{m_1}, \xi_1) S_n(\bar x_{m_2}, \xi_2)$ for the $n^2$ tensor nodes $\bar x^B_m$ of $B$, where $\xi$ is the mapped point. For a target box $T$ and a source box $C$ in its interaction list,

$$K(x, y) \approx \sum_m \sum_{m'} S_T(m, x) \, K(\bar x^T_m, \bar x^C_{m'}) \, S_C(m', y).$$

```pseudo id=main
BBFMM(q, z, K, n, L)
L1  for each leaf C: W_C(m') ← Σ_{i in C} q_i S_C(m', z_i)
L2  for l ← L - 1 down to 2: for each box B at level l: W_B(m) ← Σ over the children C of Σ_{m'} S_B(m, x̄^C_{m'}) W_C(m')
    for l ← 2 to L do
        for each box T at level l do
L3          g_T(m) ← Σ_{C in the interaction list of T} Σ_{m'} K(x̄^T_m, x̄^C_{m'}) W_C(m')
L4          if l < L then for each child D of T: g_D(k) ← g_D(k) + Σ_m g_T(m) S_T(m, x̄^D_k)
L5  for each leaf T and charge j in T: u_j ← Σ_m g_T(m) S_T(m, z_j)
L6  add the direct terms of all charges i ≠ j in T and its near neighbours
L7  return u
```

Lines L1 to L5 are the P2M, M2M, M2L, L2L and L2P steps of the FMM. Line L1 anterpolates the charges onto the nodes and line L5 interpolates the values back. The shifts of lines L2 and L4 use the $n \times n$ matrices $S_n(\bar x_m, (\bar x_{m'} \pm 1)/2)$ of the parent basis at the child nodes, once for each coordinate, so they cost $O(n^3)$ per box. Line L3 uses one $n^2 \times n^2$ matrix of kernel values for each of the $7^2 - 3^2 = 40$ offsets of the interaction list, computed once per level.

Fong and Darve also compress line L3. They stack the M2L matrices of a level and take a truncated SVD, so that each translation becomes a product with a small $r \times r$ matrix, with $r$ set by the tolerance. The code on this page applies the full matrices.

## Example

Take $N = 400$ uniform points in the unit square with charges uniform in $[-1, 1]$ (seed 5), and leaves at level $L = 3$. The near field uses 18302 ordered pairs and there are 1272 M2L products, the same counts as for the analytic FMM on these points. Against direct summation, the relative errors in the 2-norm are:

| $n$ | values per box | $\log$ kernel | largest error, $\log$ | $1/r$ kernel | inverse multiquadric |
|---|---|---|---|---|---|
| 2 | 4 | $8.7 \times 10^{-3}$ | $4.4 \times 10^{-1}$ | $6.1 \times 10^{-3}$ | $1.0 \times 10^{-2}$ |
| 3 | 9 | $1.0 \times 10^{-3}$ | $3.5 \times 10^{-2}$ | $9.7 \times 10^{-4}$ | $1.5 \times 10^{-3}$ |
| 4 | 16 | $9.5 \times 10^{-5}$ | $4.7 \times 10^{-3}$ | $1.2 \times 10^{-4}$ | $1.4 \times 10^{-4}$ |
| 6 | 36 | $2.2 \times 10^{-6}$ | $8.8 \times 10^{-5}$ | $3.5 \times 10^{-6}$ | $3.2 \times 10^{-6}$ |
| 8 | 64 | $5.8 \times 10^{-8}$ | $2.6 \times 10^{-6}$ | $9.7 \times 10^{-8}$ | $7.8 \times 10^{-8}$ |
| 10 | 100 | $1.5 \times 10^{-9}$ | $8.8 \times 10^{-8}$ | $2.6 \times 10^{-9}$ | $2.0 \times 10^{-9}$ |

These are measurements. The three kernels use the same code; only the function $K$ changes. From $n = 4$ on, the error falls by a factor of about 6 for each extra node, nearly the same for the three kernels: the rate depends mostly on how far the singularity at $x = y$ is from the pairs of boxes, and the three kernels have it at the same place.

The price is the number of values. With $n = 8$ a box holds 64 values for the relative error $5.8 \times 10^{-8}$. On the same points, the analytic FMM with $p = 12$ complex terms (24 real values) has $3.0 \times 10^{-8}$, and the [kernel-independent FMM](/kernel-independent-fast-multipole-method/) with 24 points on each circle has $2.3 \times 10^{-7}$. A tensor grid of $n^2$ nodes holds more numbers than the far field needs, and the SVD compression of Fong and Darve removes this excess.

## Correctness

The proof file proves two things. First, the shifts of lines L2 and L4 are exact: a parent basis polynomial $S_B(m, \cdot)$ has degree $n - 1$ in each coordinate, also inside each child, and interpolation at $n$ nodes reproduces such polynomials (Lemmas 1 and 2). So the output is exactly the direct sum in which, for every pair of a target box and a box in its interaction list, $K$ is replaced by its tensor Chebyshev interpolant in four variables (Lemma 3). The error is then at most $\sum_i |q_i|$ times the largest interpolation error over these pairs.

Second, this interpolation error tends to 0. Each 1D interpolation step has the error at most $1 + \Lambda_n$ times the best polynomial error, where $\Lambda_n = O(\log n)$ is the Lebesgue constant of the Chebyshev nodes, and four steps give at most $4 (1 + \Lambda_n)^4$ times it. For the three kernels above, the singular points in each scaled coordinate lie outside the Bernstein ellipse with $\rho = 2 + \sqrt{5}$, because the boxes of an interaction list are one box width apart. Then the best error is $O(\rho^{-n})$ by the bound on the Chebyshev coefficients of an analytic function. This is a bound on the rate; the measured rate above is faster.

## Complexity

The model is the [real RAM](/real-ram/), with kernel evaluations counted as one operation.

- **Same structure as the FMM (theorem).** The tree and the lists are those of the uniform FMM. Lines L1 and L5 cost $\Theta(n^2)$ per charge, $\Theta(N n^2)$ in total. Lines L2 and L4 cost $O(n^3)$ per box. Line L3 costs $n^4$ per pair, at most 27 pairs per box, so $\Theta((N / s) n^4)$. Line L6 costs $\Theta(N s)$.
- **Precomputation.** $40$ matrices of $n^4$ kernel values per level, $\Theta(L n^4)$. For a homogeneous kernel such as $1 / r$, the matrices of one level give all the others after scaling.
- **With SVD compression.** With rank $r$, the M2L products cost $O(r^2)$ each, plus $O(n^2 r)$ per box to enter and leave the compressed basis. In 3D, with $n^3$ nodes per box and 189 boxes in the interaction list, this is the step that makes the method practical.
- **Worst case.** With a uniform tree, clustered charges make the near field $\Theta(N^2)$; an adaptive tree with the lists of the [adaptive FMM](/adaptive-fast-multipole-method/) avoids this.
- **Space.** $\Theta(N + N n^2 / s)$ for the weights and values, plus $\Theta(L n^4)$ for the matrices.

## Properties

- **Only kernel values.** The code calls $K$ only as a function, and only at nodes and at near pairs. The kernel need not solve an equation, unlike for the kernel-independent FMM.
- **Exact shifts.** The M2M and L2L steps add no error. All the error comes from the interpolation in the M2L step.
- **Linear in the charges.** The output is a linear function of $q$, so the method is a fast matrix-vector product for iterative solvers of [boundary element](/boundary-element-method/) and integral equations, and for kernel matrices of [Gaussian processes](/gaussian-process/).
- **Uniform accuracy across levels for the log kernel.** Scaling a box changes $\log|x - y|$ only by a constant, which interpolation reproduces, so every level has the same relative accuracy.
- **Deterministic.** The result does not depend on the order of the charges, up to rounding.

## Variants and improvements

- **SVD compression.** Fong and Darve compress the M2L operators of each level by a truncated SVD of the stacked matrices, which also gives the multipole and local bases of the smallest size for a given tolerance in the 2-norm.
- **Adaptive trees.** The same expansions work on an adaptive tree with the $U$, $V$, $W$ and $X$ lists of the [adaptive FMM](/adaptive-fast-multipole-method/); the W and X lists need the conversion between charges and node values.
- **Other interpolation nodes.** Equispaced nodes make the M2L matrices Toeplitz, so the [FFT](/fast-fourier-transform/) applies them fast, at the cost of a larger Lebesgue constant and worse stability than Chebyshev nodes.
- **Oscillatory kernels.** For the Helmholtz kernel at high frequency, $n$ must grow with the size of a box in wavelengths, and directional variants of the interpolation are used.
- **Higher dimensions.** In 3D the box holds $n^3$ nodes and the M2L matrices have $n^6$ entries, so compression is needed for any practical $n$.

## When to use it

Use the bbFMM when the kernel is smooth away from the diagonal but has no convenient expansions: kernels given by a formula that is long to expand, kernels that come from a table or another computation, covariance functions, or anisotropic kernels. It is a good choice when you need to change the kernel often. For the Laplace kernel in 2D, the analytic FMM needs fewer coefficients for the same accuracy. For Green's functions of elliptic equations, the kernel-independent FMM is the other black-box choice. For small $N$, use [direct summation](/direct-n-body-summation/).

## Pitfalls

- **Points outside the box.** The basis $S_n$ is a polynomial, and it grows fast outside $[-1, 1]$. A charge assigned to the wrong box, for example by a rounding error at the edge of the square, is extrapolated and can give a large error. Clamp the mapped coordinates to $[-1, 1]$.
- **Kernels that are not smooth enough.** A kernel with a singularity or a fast change at a distance comparable to a box, such as a narrow Gaussian or a kernel with a softening length close to the box size, needs many more nodes. Choose the levels so that the boxes are large or small compared with that length.
- **Cost without compression.** The M2L step costs $n^4$ per pair in 2D and $n^6$ in 3D. Without the SVD step, the method is slower than the analytic FMM for the same accuracy.
- **Matrices per level.** For a kernel that is not homogeneous, the M2L matrices differ between levels and must be computed for each level.
- **Too few nodes for the accuracy.** The rate of convergence on this page depends on the separation of the interaction list and on the kernel. Measure against direct summation on a small problem.

## Implementations

## History

Interpolation of smooth kernels on hierarchical boxes was used before 2009 in several fast summation methods. Fong and Darve (2009) gave the black-box FMM: tensor Chebyshev interpolation of the kernel inside the FMM tree, with exact shifts between levels and a compression of the M2L operators by singular value decompositions. Their aim was a method for kernels that are known only numerically, or that are known analytically but are complicated, with a small precomputation time even for large systems. The [kernel-independent FMM](/kernel-independent-fast-multipole-method/) of Ying, Biros and Zorin (2004) is the other main FMM that needs no analytic expansions; it needs a kernel that is the Green's function of an elliptic equation.

## References
