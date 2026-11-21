---
tag: KFR7FZ
kind: algorithm
slug: sirt
name: Simultaneous iterative reconstruction technique
aliases:
- SIRT
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Update all pixels at once by the back projection of all ray residuals, scaled by the row and column sums of the system matrix. It is a weighted Landweber iteration.
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", a: "the number of projection angles", d: "the number of detector bins", K: "the number of iterations"}
  time: {per_iteration: "O(a d n)", total: "O(K a d n)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true, linear_in_data: true, order_independent: true, discrepancy_stop: "O(delta^(-2 / (2 nu + 1)))"}
history:
  year: 1972
  people: [Peter Gilbert]
  note: Gilbert proposed to correct all pixels at once from all ray sums, as a smoother alternative to the ray-by-ray corrections of ART.
prereqs: [landweber-iteration, kaczmarz-method, sparse-matrix]
see_also: [sart, siddon-algorithm, joseph-projector, distance-driven-projector, semi-convergence, morozov-discrepancy-principle, richardson-iteration, projected-gradient-descent]
sources:
  - paper: "P. Gilbert, Iterative methods for the three-dimensional reconstruction of an object from projections, Journal of Theoretical Biology 36(1), 1972, 105 to 117"
    locator: the simultaneous correction of all pixels from all ray sums (general locator)
  - paper: doi:10.1109/TIP.2003.815295
    title: Ming Jiang and Ge Wang, Convergence of the simultaneous algebraic reconstruction technique (SART), IEEE Transactions on Image Processing 12(8), 2003
    locator: pp. 957 to 961 (convergence of the simultaneous form x + lambda V A^T W (y - A x) for nonnegative A to a weighted least squares solution from any start)
  - paper: "A. van der Sluis and H. A. van der Vorst, SIRT- and CG-type methods for the iterative solution of sparse linear least-squares problems, Linear Algebra and its Applications 130, 1990, 257 to 302"
    locator: SIRT as a scaled Landweber iteration and its weighted least squares limit (general locator)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 7, algebraic reconstruction algorithms (ART, SIRT and SART)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 6 (Landweber iteration, its stopping by the discrepancy principle and its rates)
---

SIRT reconstructs an image from the data $y$ of the discrete model $y = A x + e$ of tomography, where $x \in \mathbb{R}^N$ holds the $N = n^2$ pixel values, $y \in \mathbb{R}^m$ holds the $m$ ray sums, and $A$ is a sparse $m \times N$ matrix with nonnegative entries $a_{ij}$, the weight of pixel $j$ in ray $i$. Each iteration computes the residuals of all rays, divides each by the sum of its row, back-projects them, divides each pixel by the sum of its column, and adds the result: $x \leftarrow x + \lambda C A^T R (y - A x)$ with $R = \operatorname{diag}(1/r_i)$ and $C = \operatorname{diag}(1/c_j)$. It is the [Landweber iteration](/landweber-iteration/) for the scaled system $R^{1/2} A C^{1/2}$, which has norm exactly 1. So it converges for $0 < \lambda < 2$ to a weighted least squares solution, and with noisy data it needs a stopping rule. It differs from [ART](/kaczmarz-method/), which corrects the image after each single ray, and from [SART](/sart/), which corrects it after the rays of one view.

## In plain words

Each ray gives one equation: the weighted sum of the pixel values along the ray must equal the measured value. SIRT starts from an image, often all zeros, and computes what each ray would measure. The difference to the measurement is the error of that ray. Divide each error by the total weight of its ray, so that a long ray does not count more than a short one, and spread it back over the pixels of the ray.

Now each pixel holds the sum of the corrections that its rays want. Divide this sum by the total weight of the pixel, so that the pixel takes the average correction. Add this average, times a factor $\lambda$, and repeat. Every pixel listens to all rays at once, so the image changes smoothly and the order of the rays does not matter.

## The problem

Given a nonnegative $m \times N$ matrix $A$ and data $y \in \mathbb{R}^m$, find $x$ that fits $A x \approx y$. Write $r_i = \sum_j a_{ij}$ for the row sums and $c_j = \sum_i a_{ij}$ for the column sums, and assume all are positive (a ray that misses the image, or a pixel that no ray meets, is removed first; the code gives it the weight 0). The weighted norm of a residual is $\|v\|_R^2 = \sum_i v_i^2 / r_i$. With exact consistent data, the target is a solution of $A x = y$. With inconsistent data, SIRT solves the weighted least squares problem
$$\min_x \|y - A x\|_R^2,$$
and among its solutions it picks the one closest to the start $x_0$ in the norm $\|v\|_{C^{-1}}^2 = \sum_j c_j v_j^2$. In tomography the data are noisy and the matrix is ill-conditioned, so this limit is not the goal: the useful result is an early iterate.

## The algorithm

```pseudo id=main
SIRT(A, y, λ, K, x0)                     ▷ 0 < λ < 2; δ is the noise level if known
L1  r_i ← Σ_j a_ij, c_j ← Σ_i a_ij; R ← diag(1/r_i), C ← diag(1/c_j)
L2  x ← x0
L3  for k ← 1 to K do
L4      e ← y - A x;  if δ is known and ‖e‖ ≤ τ δ then return x
L5      e_i ← e_i / r_i for each ray i
L6      g ← A^T e                         ▷ the back projection of the scaled residuals
L7      x_j ← x_j + λ g_j / c_j for each pixel j
L8      (optional) x_j ← max(x_j, 0)
L9  return x
```

Line L4 is one forward projection and line L6 one back projection, so the cost of an iteration is that of two passes over the nonzero entries of $A$. Any projector gives the matrix: [Siddon's algorithm](/siddon-algorithm/), [Joseph's projector](/joseph-projector/) or the [distance-driven projector](/distance-driven-projector/). The method needs $A^T$ in line L6, not an approximate back projector. Line L4 also tests the [discrepancy principle](/morozov-discrepancy-principle/) with a fixed $\tau > 1$. Line L8 keeps the image nonnegative. With it, the method is a projected iteration and the linear analysis below no longer applies, but it still converges (see Correctness).

## Example

Take a $2 \times 2$ image $x = (x_0, x_1, x_2, x_3)$ in row-major order, the true values $(1, 2, 3, 4)$, and five rays with weights 0 or 1: the two rows, the two columns, and the diagonal through $x_0$ and $x_3$.

| ray | pixels | $y_i$ | $r_i$ |
|---|---|---|---|
| row 0 | $x_0, x_1$ | 3 | 2 |
| row 1 | $x_2, x_3$ | 7 | 2 |
| column 0 | $x_0, x_2$ | 4 | 2 |
| column 1 | $x_1, x_3$ | 6 | 2 |
| diagonal | $x_0, x_3$ | 5 | 2 |

The column sums are $c = (3, 2, 2, 3)$, because $x_0$ and $x_3$ lie on three rays and the others on two. Start from $x = 0$ with $\lambda = 1$. Line L5 gives $e / r = (3/2, 7/2, 2, 3, 5/2)$. Line L6 gives $g_0 = 3/2 + 2 + 5/2 = 6$, $g_1 = 3/2 + 3 = 9/2$, $g_2 = 7/2 + 2 = 11/2$ and $g_3 = 7/2 + 3 + 5/2 = 9$. Line L7 divides by $c$:

| iteration | $x_0$ | $x_1$ | $x_2$ | $x_3$ | $\|y - A x\|_R^2$ |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | $135/2$ |
| 1 | 2 | $9/4$ | $11/4$ | 3 | $17/8$ |
| 2 | $5/3$ | $17/8$ | $23/8$ | $10/3$ | $265/288$ |
| 3 | $13/9$ | $33/16$ | $47/16$ | $32/9$ | $4177/10368$ |

The weighted residual falls at each step, as the theory says. The five rays determine the image, so the iterates converge to $(1, 2, 3, 4)$; after 400 steps the error is below $10^{-9}$ for $\lambda = 0.5$, $1$ and $1.9$. The scaled matrix $B = R^{1/2} A C^{1/2}$ has the singular values $1$, $1/\sqrt{2}$, $1/\sqrt{3}$ and $1/\sqrt{6}$, so the error of the slowest component shrinks by the factor $1 - 1/6 = 5/6$ per step for $\lambda = 1$. The test file checks all values of the table with `fractions.Fraction`.

A larger case: a disk of radius 0.6 on a $16 \times 16$ grid, 12 angles in $[0, \pi)$, 23 bins, and the pixel-driven matrix of the shared helper. With exact data, the relative error $\|x_k - x\|/\|x\|$ is $0.63$ after 1 step, $0.24$ after 10, $0.12$ after 100 and $0.094$ after 400. With Gaussian noise of standard deviation $2$ percent of the largest ray sum (seed 5), the error is smallest, $0.181$, at $k = 101$, and it grows to $0.207$ at $k = 400$: this is [semi-convergence](/semi-convergence/). The discrepancy principle with $\tau = 1.01$ stops at $k = 24$ with the error $0.204$. These numbers are measurements of this setup, not properties of the method.

## Correctness

Put $B = R^{1/2} A C^{1/2}$, $b = R^{1/2} y$ and $x = C^{1/2} z$. Then line L7 reads $z \leftarrow z + \lambda B^T (b - B z)$, the Landweber iteration for $B$ with the step $\omega = \lambda$. Two facts make the theory of Landweber apply:

- $\|B\|_2 = 1$. By the Cauchy-Schwarz inequality, $\big(\sum_j a_{ij} c_j^{-1/2} z_j\big)^2 \le r_i \sum_j a_{ij} c_j^{-1} z_j^2$, and summing over $i$ with the weights $1/r_i$ gives $\|B z\|^2 \le \sum_j z_j^2 = \|z\|^2$. The vector $z = (\sqrt{c_j})$ gives $B z = (\sqrt{r_i})$, and $\sum_i r_i = \sum_j c_j$, so the bound is attained.
- So $0 < \lambda < 2 = 2/\|B\|^2$ is the Landweber condition. With $B = \sum_k \sigma_k u_k v_k^T$, the iterate from $z_0 = 0$ is $z_k = \sum_k [1 - (1 - \lambda\sigma_k^2)^k] (u_k^T b / \sigma_k) v_k$: the spectral filter factors of Landweber.

Each factor $1 - \lambda\sigma^2$ lies in $(-1, 1)$ for $0 < \sigma \le 1$, so $z_k$ converges to $B^\dagger b$ plus the part of $z_0$ in the null space of $B$. In the variable $x$ this is the weighted least squares solution of the problem section, closest to $x_0$ in the $C^{-1}$ norm. The weighted residual $\|y - A x_k\|_R = \|b - B z_k\|$ does not increase, because $b - B z_{k+1} = (I - \lambda B B^T)(b - B z_k)$ and the eigenvalues of $I - \lambda B B^T$ lie in $(-1, 1]$. For $\lambda > 2$ the factor $|1 - \lambda| > 1$ on the top singular value, and from $x_0 = 0$ the iteration diverges whenever $\sum_i y_i \ne 0$, because the top singular vector is $(\sqrt{r_i})$ up to scaling. With line L8, the step is a projected gradient step for $\frac{1}{2}\|b - B z\|^2$ over $z \ge 0$, because $C$ is diagonal and positive, so $x \ge 0$ if and only if $z \ge 0$, and the projection onto the orthant is the clipping. A projected gradient step with a step size below $2/\|B\|^2$ converges to a minimizer on the orthant when one exists ([projected gradient descent](/projected-gradient-descent/)). The full proofs are in [proofs/correctness.md](proofs/correctness.md).

Jiang and Wang (2003) proved the convergence of this simultaneous update for nonnegative $A$ from any start, under the name SART; see [SART](/sart/) for the form that works one view at a time.

## Complexity

In the real-RAM model, with $a$ angles of $d$ bins each, so $m = a d$ rays, and an $n \times n$ image:

- Line L1 takes one pass over the nonzero entries of $A$. A ray-driven projector has $O(n)$ entries per ray, so $\operatorname{nnz}(A) = O(a d n)$.
- Lines L4 and L6 are one forward and one back projection, $O(a d n)$ each. Lines L5 and L7 take $O(a d)$ and $O(n^2)$.

So one iteration costs $O(a d n + n^2)$ time, which is $O(a d n)$ since $a d \ge n^2 \ge n$ in any scan that can determine the image. It needs $O(a d + n^2)$ extra space, and $K$ iterations cost $O(K a d n)$. With a matrix-free projector, count one application of $A$ and one of $A^T$ per iteration. The number of iterations is the regularization parameter. With noise level $\delta$, the discrepancy principle and the source condition of Landweber for $B$ in the EHN form $z^\dagger = (B^T B)^\nu w$, the stopping index is $O(\delta^{-2/(2\nu+1)})$ (EHN chapter 6). A measured iteration count, such as the $k = 24$ above, is not a bound.

## Properties

- **Order independent.** All rays act at once, so the result does not depend on the order of the rays, and the iteration is fully parallel over rays and over pixels. ART and SART depend on the order.
- **Weighted Landweber.** SIRT is Landweber on $B$; the theory of the [Landweber iteration](/landweber-iteration/) (filter factors, infinite qualification, order optimal rates with the discrepancy principle) carries over, in the weighted norms.
- **Slow.** Each iteration damps the component of singular value $\sigma$ by $1 - \lambda\sigma^2$. The small singular values of a tomography matrix need many iterations. ART and SART reach the same image quality in fewer passes through the data, at the price of sequential work.
- **Smooth iterates and semi-convergence.** The early iterates hold only the components with large $\sigma$, which are smooth images. With noise the error first falls and then rises. Stopping early is the regularization.
- **Linear in the data.** Without line L8, $x_k$ is a fixed linear function of $y$ and $x_0$, so its noise can be analyzed exactly. With line L8 it is not linear.

## Variants and improvements

- **Cimmino's method (1938)** projects onto all hyperplanes $\langle a_i, x\rangle = y_i$ and averages: $x \leftarrow x + \lambda \sum_i w_i \frac{y_i - \langle a_i, x\rangle}{\|a_i\|^2} a_i$. It is the same scheme with $\|a_i\|^2$ in place of $r_i$ and no column scaling.
- **Plain Landweber** uses $R = C = I$ and needs $\lambda < 2/\|A\|^2$, which requires an estimate of the norm, for example by [power iteration](/power-iteration/). The scaling of SIRT gives the bound $\|B\| = 1$ for free.
- **SART** applies the same update with the rays of one view at a time. One pass through all views is then a sequence of $a$ small SIRT steps, and it converges much faster in practice. The ordered subsets form takes a group of views at a time.
- **Krylov methods.** [CGLS](/cgls/) applied to $B$ minimizes the same weighted residual over a Krylov subspace. It usually needs far fewer iterations than SIRT for the same residual, but its iterates depend on the data in a nonlinear way.
- **Box constraints.** Line L8 can clip to any box $[0, u]$; the projected iteration still converges, by the same argument.

## When to use it

Use SIRT for tomography when the data are noisy or the angles are few, when a smooth and stable result matters more than speed, and when the forward and back projections run in parallel, for example on a GPU. Its iterates are linear in the data and do not depend on the ray order, which makes it easy to analyze. Use [SART](/sart/) or [ART](/kaczmarz-method/) when fast convergence per pass matters more than parallel work. For complete data with many angles, [filtered back-projection](/filtered-back-projection/) is far cheaper. For few angles of a piecewise constant object, add a total variation step, as in [ASD-POCS](/asd-pocs/).

## Pitfalls

- **Zero rows or columns.** A ray that misses the image has $r_i = 0$, and a pixel outside all rays has $c_j = 0$. Division by zero follows unless they are removed or given the weight 0.
- **An unmatched back projector.** If line L6 uses a back projector that is not $A^T$, the iteration is not Landweber for any matrix, $\|B\| \le 1$ no longer follows, and the method can diverge or converge to a wrong point.
- **No stopping rule.** With noisy data the iterates converge to the weighted least squares solution, which is dominated by noise. Run to convergence only with exact data. Stop by the discrepancy principle if the noise level is known; other rules are heuristics.
- **$\lambda \ge 2$.** The bound is sharp, because $\|B\| = 1$ exactly. $\lambda = 2$ gives a component that does not decay, and $\lambda > 2$ diverges.
- **Confusing the norms.** The limit minimizes the $R$-weighted residual, not the plain residual, and it is closest to $x_0$ in the $C^{-1}$ norm. A test against a plain least squares solution fails.
- **Expecting monotone error.** Only the weighted residual is monotone. The error against the true image is not monotone with noise.

## Implementations

The Python code takes the system matrix as sparse rows of (column, weight) pairs, as built by the shared helper `imgkit.parallel_beam_matrix` or by any projector page, and works with float or `fractions.Fraction` data. The tests check the worked example exactly, the convergence to the solution of a consistent system, $\|B\| = 1$, the limit against the weighted normal equations and against the minimum $C^{-1}$ norm solution, the filter factors against an SVD of $B$, the monotone weighted residual, the divergence for $\lambda > 2$, and a disk phantom with the discrepancy stop.

## History

Peter Gilbert proposed SIRT in 1972 in the Journal of Theoretical Biology, two years after Gordon, Bender and Herman published ART in the same journal. ART corrects the image after each ray and gave noisy, streaky images; Gilbert corrected every pixel from all ray sums at once, which gave smoother results. The averaging of projections onto all hyperplanes is older: Cimmino published it for linear systems in 1938. Van der Sluis and van der Vorst analyzed SIRT in 1990 as a scaled Landweber iteration for a weighted least squares problem. Andersen and Kak introduced SART in 1984, and Jiang and Wang proved the convergence of the simultaneous update in 2003.

## References
