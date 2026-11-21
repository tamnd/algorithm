---
tag: MKX2VP
kind: problem
slug: fredholm-integral-equation-first-kind
name: Fredholm integral equation of the first kind
aliases:
- first-kind integral equation
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "Find x from y(s) = integral of K(s,t) x(t) dt with a known kernel K. A square-integrable kernel gives a compact operator, so the inverse is unbounded and noisy data need regularization."
model: real-ram
prereqs: [inverse-problem, forward-operator, well-posed-problem]
see_also: [singular-value-expansion, picard-condition, degree-of-ill-posedness, truncated-svd, tikhonov-regularization, galerkin-method, gaussian-quadrature, image-deblurring]
sources:
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 2, Meet the Fredholm Integral Equation of the First Kind, and Chapter 3, Discretizations
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapters 1 and 2 (integral equations of the first kind as the model ill-posed problem, compact operators)
  - paper: doi:10.1145/321105.321114
    title: David L. Phillips, A technique for the numerical solution of certain integral equations of the first kind, Journal of the ACM 9(1), 1962, 84 to 97
    locator: the test equation with kernel 1 + cos(pi x / 3) and the smoothing that stabilizes its discretization
  - paper: doi:10.1007/BF02149761
    title: Per Christian Hansen, Regularization Tools, a Matlab package for analysis and solution of discrete ill-posed problems, Numerical Algorithms 6, 1994, 1 to 35
    locator: the test problems baart, deriv2, phillips and shaw
  - book: "Rainer Kress, Linear Integral Equations, Springer, 1989"
    locator: the chapters on compact operators and on ill-posed problems (general locator)
---

The Fredholm integral equation of the first kind asks for a function $x$ that satisfies $\int_a^b K(s,t)\,x(t)\,dt = y(s)$, where the kernel $K$ and the data $y$ are given. It is the standard continuous model of a linear [inverse problem](/inverse-problem/): blur, gravity surveys, spectroscopy and the inverse heat equation all have this form. Because the integral smooths, a square-integrable kernel gives a compact [forward operator](/forward-operator/), and the problem fails the stability condition of a [well-posed problem](/well-posed-problem/). This page states the problem and lists what is known; the tools to analyze it are the [singular value expansion](/singular-value-expansion/) and the [Picard condition](/picard-condition/).

## In plain words

Each measurement is a weighted average of the unknown function, and the kernel gives the weights. A blurred image is an example: each pixel is an average of nearby points of the sharp image. Averages hide fast wiggles. If you add a fast wiggle to the unknown, the averages barely change. So when the data have a little noise, many very different functions fit them equally well, and the one that fits best is usually full of wild wiggles. To get a useful answer you must prefer smooth functions, or stop the solution process early, and you must accept that the finest details cannot be recovered.

## Definition

**Input.** A kernel $K \in L^2((c,d) \times (a,b))$, which defines the operator
$$(A x)(s) = \int_a^b K(s,t)\,x(t)\,dt, \qquad A: L^2(a,b) \to L^2(c,d),$$
and data $y^\delta \in L^2(c,d)$ with $\|y^\delta - y\| \le \delta$, where $y = A x^{\mathrm{true}}$. In practice the data are often samples $y_i = (A x)(s_i) + e_i$ for $i = 1, \ldots, m$.

**Output.** An approximation of $x^\dagger = A^\dagger y$, the solution of minimum norm, that converges to $x^\dagger$ as $\delta \to 0$.

**What is known about the problem.**

- **Compactness.** A square-integrable kernel gives a Hilbert-Schmidt operator, so $A$ is compact. Its singular values satisfy $\sum_k \sigma_k^2 = \|K\|_{L^2}^2 < \infty$.
- **Instability.** If the range of $A$ has infinite dimension (that is, if $K$ is not a finite sum of products $f_j(s) g_j(t)$), the range is not closed, and $A^\dagger$ is unbounded. No solution method can be stable for all data.
- **Riemann-Lebesgue.** For each fixed square-integrable kernel, $\|A x_p\| \to 0$ for any orthonormal sequence $x_p$, for example $x_p(t) = \sqrt2 \sin(2\pi p t)$. Fast oscillations are invisible in the data.
- **Existence.** A solution exists if and only if $y$ is in the closure of the range and its singular coefficients satisfy $\sum_k |\langle u_k, y \rangle|^2/\sigma_k^2 < \infty$. This is the [Picard condition](/picard-condition/).
- **Uniqueness.** It holds exactly when the null space of $A$ is $\{0\}$. Many kernels have a null space; the minimum norm solution $x^\dagger$ then fixes the choice.

**Contrast with the second kind.** The equation of the second kind, $x(s) - \lambda \int K(s,t) x(t)\,dt = y(s)$, is well posed whenever $1/\lambda$ is not an eigenvalue of $A$ (the Fredholm alternative). The unknown appears outside the integral there, so it is not smoothed. The first kind has no such term, and that is the whole difference.

## Variants

- **Volterra equations of the first kind.** The upper limit is $s$: $\int_a^s K(s,t) x(t)\,dt = y(s)$. This is the special case $K(s,t) = 0$ for $t > s$.
- **Convolution kernels.** $K(s,t) = h(s - t)$. The problem is deconvolution, and the Fourier transform diagonalizes $A$ (see [image deblurring](/image-deblurring/)).
- **Semi-discrete data.** Only finitely many samples $y_i$ are measured. The problem is then underdetermined, and the methods of Backus and Gilbert (see [Backus-Gilbert method](/backus-gilbert-method/)) estimate local averages of $x$.
- **Two and three dimensions.** Kernels on $\Omega \subset \mathbb{R}^d$; CT, where the [Radon transform](/radon-transform/) plays the role of $A$, is a close relative with a singular kernel.
- **Constraints.** Positivity, bounds or a known support of $x$. They add information that the linear theory does not use.

## Examples

**The integration operator.** $K(s,t) = 1$ for $t \le s$ and $0$ otherwise, on $(0,1)^2$. This is a Volterra kernel, and the inverse is differentiation. The singular values are $\sigma_k = 2/((2k-1)\pi)$: $0.63662$, $0.21221$, $0.12732$, $0.09095$, $0.07074$. The check $\sum_k \sigma_k^2 = \tfrac{4}{\pi^2} \sum_k \tfrac{1}{(2k-1)^2} = \tfrac{4}{\pi^2} \cdot \tfrac{\pi^2}{8} = \tfrac12$ equals $\|K\|^2$, the area of the triangle $t \le s$. For $x(t) = \sin(2\pi p t)$, with norm $1/\sqrt2 = 0.70711$, the data are $y(s) = (1 - \cos(2\pi p s))/(2\pi p)$ with norm $\sqrt{1.5}/(2\pi p) = 0.19492/p$. With $p = 100$ the data have norm $0.0019$ while the solution has norm $0.707$.

**deriv2.** The Green's function of $-x''$ with zero boundary values: $K(s,t) = s(1 - t)$ for $s \le t$ and $t(1 - s)$ for $s > t$, on $(0,1)^2$. Up to sign, this is the kernel of the deriv2 test problem of Regularization Tools. It is symmetric with eigenfunctions $\sqrt2 \sin(k\pi t)$ and eigenvalues $1/(k\pi)^2$, so $\sigma_1 = 0.1013$, $\sigma_2 = 0.02533$ and $\sigma_{10} = 0.001013$. Recovering $x$ means taking two derivatives of $y$.

**Phillips' problem.** Phillips (1962) used $K(s,t) = \phi(s - t)$ with $\phi(u) = 1 + \cos(\pi u/3)$ for $|u| < 3$ and $\phi(u) = 0$ otherwise, on $[-6, 6]$. He showed that the plain discretization gives a useless solution and repaired it with a smoothness penalty, one of the first forms of [Tikhonov regularization](/tikhonov-regularization/).

**Shaw and Baart.** Two test problems of Regularization Tools with smooth (analytic) kernels. Their singular values decay exponentially, so they are severely ill posed: only a few components of $x$ can be recovered at any realistic noise level.

## Known algorithms

All practical methods first discretize, then regularize.

- **Discretization.** Quadrature on a grid $t_j$ with weights $w_j$ gives $A_{ij} = w_j K(s_i, t_j)$ (for example the midpoint rule or [Gaussian quadrature](/gaussian-quadrature/)). The [Galerkin method](/galerkin-method/) with orthonormal bases $\phi_j$ and $\psi_i$ gives $A_{ij} = \langle \psi_i, A \phi_j \rangle$; its singular values never exceed those of $A$ and converge to them as the bases grow. The rectangle rule for the integration operator with $n = 24$ gives $\sigma_1 = 0.64999$ against the exact $0.63662$.
- **Spectral filtering.** [Truncated SVD](/truncated-svd/) and [Tikhonov regularization](/tikhonov-regularization/) damp the small singular components; see [spectral filter factors](/spectral-filter-factors/).
- **Iterative regularization.** [Landweber iteration](/landweber-iteration/), [CGLS](/cgls/) and [LSQR](/lsqr/) with the iteration count as the parameter. They need only products with $A$ and $A^T$.
- **Parameter choice.** The [discrepancy principle](/morozov-discrepancy-principle/) when $\delta$ is known; see [regularization parameter choice](/regularization-parameter-choice/) for the other rules.

## Bounds

- **Decay of the singular values.** For a square-integrable kernel, $\sum_k \sigma_k^2 < \infty$ and the $\sigma_k$ decrease, so $k \sigma_k^2 \le \sum_{j \le k} \sigma_j^2$ forces $\sigma_k = o(k^{-1/2})$. Smoother kernels give faster decay; analytic kernels give exponential decay.
- **No uniform rate without prior knowledge.** Since $A^\dagger$ is unbounded, for any method and any $\delta > 0$ the worst-case error over all $x$ with $\|A x - y^\delta\| \le \delta$ is infinite. A rate needs a bound on $x$, usually a [source condition](/source-condition/) $x^\dagger = (A^* A)^\nu w$ with $\|w\| \le \rho$. Then the best possible worst-case error is of the order $\delta^{2\nu/(2\nu+1)} \rho^{1/(2\nu+1)}$, and TSVD with a suitable $k$ attains it (EHN chapter 3).

## Reductions

- **To a least squares problem.** Discretization gives $\min_x \|A_n x - y\|$, a [least squares problem](/least-squares-problem/) with an ill-conditioned matrix.
- **Volterra first kind to second kind.** If $K$ is differentiable and $K(s,s) \ne 0$, differentiating $\int_a^s K(s,t) x(t)\,dt = y(s)$ gives $K(s,s) x(s) + \int_a^s \partial_s K(s,t) x(t)\,dt = y'(s)$, an equation of the second kind. So the instability of such an equation is exactly that of differentiating the data.
- **Convolution to division.** For a periodic convolution kernel the DFT turns the equation into $\hat h_k \hat x_k = \hat y_k$, and the instability is the division by small $\hat h_k$.

## Applications

Gravity and magnetic surveying (the field at the surface is an integral of the density below), image deblurring, spectroscopy and the unfolding of instrument responses, the inverse heat conduction problem, the inverse Laplace transform in relaxation and NMR studies (severely ill posed), and Abel inversion in plasma diagnostics.

## References
