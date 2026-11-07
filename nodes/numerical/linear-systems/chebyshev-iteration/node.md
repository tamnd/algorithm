---
tag: 3W6N6C
kind: algorithm
slug: chebyshev-iteration
name: Chebyshev iteration
aliases:
- Chebyshev semi-iterative method
- Chebyshev acceleration
- Chebyshev polynomial iteration
area: numerical/linear-systems
level: advanced
summary: Accelerated stationary iteration using Chebyshev polynomials and eigenvalue bounds.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", κ: "the ratio lmax / lmin of the eigenvalue bounds", ε: "the factor by which the error must drop"}
  time: {worst: "O(z √κ ln(2/ε))"}
  space: {extra: Θ(n)}
  matvecs: {worst: "⌈(√κ / 2) ln(2/ε)⌉"}
  flops: {per_step: "2 z + 7 n + O(1)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true, parallel: true}
prereqs: [richardson-iteration, spectral-radius, krylov-subspace, orthogonal-polynomials]
see_also: [conjugate-gradient-method, richardson-iteration, jacobi-method, successive-over-relaxation, multigrid-method, gershgorin-circle-theorem, preconditioning, krylov-subspace]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 6.11.1, Real Chebyshev Polynomials (Theorem 6.25 on the min-max property); Section 12.3.2, Chebyshev Acceleration (Algorithm 12.1)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.2.8, The Chebyshev Semi-Iterative Method
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Section 3.1, the Chebyshev bound for CG; Section 2.1 and Chapter 1 on polynomial methods
  - paper: doi:10.1007/BF01386223
    title: Gene H. Golub and Richard S. Varga, Chebyshev semi-iterative methods, successive overrelaxation iterative methods, and second order Richardson iterative methods, Numerische Mathematik 3, 1961
    locator: Part I, pp. 147 to 156 (the three-term recurrence and its optimality)
  - paper: doi:10.1016/S0167-8191(01)00139-9
    title: Martin H. Gutknecht and Stefan Röllin, The Chebyshev iteration revisited, Parallel Computing 28(2), 2002
    locator: pp. 263 to 283 (rounding errors, the residual gap and the stable three-term forms)
  - paper: doi:10.1007/BF01396379
    title: Thomas A. Manteuffel, The Tchebychev iteration for nonsymmetric linear systems, Numerische Mathematik 28, 1977
    locator: pp. 307 to 327 (ellipses in the complex plane and adaptive parameter estimation)
  - book: "Richard S. Varga, Matrix Iterative Analysis, second edition, Springer, 2000"
    locator: Chapter 5, Semi-Iterative Methods
---

Chebyshev iteration solves $A x = b$ when the eigenvalues of $A$ are known to lie in an interval $[\lambda_{\min}, \lambda_{\max}]$ with $0 < \lambda_{\min}$. It chooses the iterate $x_k$ whose error is $e_k = p_k(A) e_0$ for the polynomial $p_k$ of degree $k$ with $p_k(0) = 1$ that is smallest in maximum norm on the interval: a shifted and scaled Chebyshev polynomial. A three-term recurrence computes $x_k$ with one matvec per step and no inner products. For symmetric $A$ the error then drops like $2 \left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^k$ with $\kappa = \lambda_{\max}/\lambda_{\min}$, the same rate as the [conjugate gradient method](/conjugate-gradient-method/)'s worst case, and the square root of $\kappa$ is a large gain over [Richardson](/richardson-iteration/) or [Jacobi](/jacobi-method/) iteration, which need about $\kappa$ steps. The price is that the bounds must be supplied, and an underestimated $\lambda_{\max}$ makes the iteration diverge.

## In plain words

A simple iteration takes the same step every time and so has to be cautious, because a step that is good for one part of the error is too big for another. Chebyshev iteration plans a sequence of different steps in advance, some big and some small, so that together they reduce every part of the error by about the same amount. The plan uses a special family of polynomials that wiggle as little as possible over a range.

It needs to know the range of the matrix's eigenvalues. It never compares vectors with each other, which makes it fast on parallel machines.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A \in \mathbb{R}^{n \times n}$, $x_k$ the iterate, $e_k = x - x_k$, $r_k = b - A x_k$, $u = 2^{-53}$, $\rho(\cdot)$ the [spectral radius](/spectral-radius/). The inputs $0 < \lambda_{\min} \le \lambda_{\max}$ bound the spectrum; $\theta = (\lambda_{\max} + \lambda_{\min})/2$ is the center, $\delta = (\lambda_{\max} - \lambda_{\min})/2$ the half width, $\sigma_1 = \theta/\delta$, $\kappa = \lambda_{\max}/\lambda_{\min}$, and $T_k$ is the Chebyshev polynomial $T_k(\cos t) = \cos(k t)$, with $T_0 = 1$, $T_1(s) = s$ and $T_{k+1}(s) = 2 s T_k(s) - T_{k-1}(s)$.

Given $A$ (through matvecs), $b$, $x_0$, the bounds and a tolerance, return $x_k$ with $\|r_k\|_2 \le \mathrm{tol} \cdot \|b\|_2$, or NOT-CONVERGED, or DIVERGED.

## The algorithm

The target polynomial is
$$p_k(\lambda) = \frac{T_k\left(\frac{\theta - \lambda}{\delta}\right)}{T_k(\sigma_1)}, \qquad \max_{\lambda \in [\lambda_{\min}, \lambda_{\max}]} |p_k(\lambda)| = \frac{1}{T_k(\sigma_1)}.$$
The three-term recurrence for $T_k$ gives a recurrence for the corrections $d_k = x_{k+1} - x_k$ (Saad, Algorithm 12.1):

```pseudo id=main
Chebyshev(A, b, x, λmin, λmax, tol, kmax)      ▷ needs 0 < λmin ≤ λmax
L1  θ ← (λmax + λmin)/2;  δ ← (λmax − λmin)/2;  σ₁ ← θ/δ;  ρ ← 1/σ₁
L2  r ← b − A x;  d ← r / θ
L3  for k ← 0 to kmax do
L4      if ‖r‖₂ ≤ tol · ‖b‖₂ then return (x, k, CONVERGED)
L5      w ← A d
L6      x ← x + d
L7      r ← r − w
L8      ρ_new ← 1 / (2σ₁ − ρ)
L9      d ← ρ_new ρ d + (2ρ_new / δ) r;  ρ ← ρ_new
```

If $\delta = 0$ (a single eigenvalue), the code takes Richardson steps $d = r/\theta$. The norm in L4 is the only inner product, and it may be evaluated only every few steps; the implementation also stops with DIVERGED if $\|r\|$ grows by a factor of $10^6$.

## Example

$A = \begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$, $b = (1, 1)$, $x = (1, 1)$, with the exact bounds $\lambda_{\min} = 1$, $\lambda_{\max} = 3$: $\theta = 2$, $\delta = 1$, $\sigma_1 = 2$, $\rho_0 = 1/2$. From $x_0 = 0$:

- $r_0 = (1, 1)$, $d_0 = (1/2, 1/2)$, $x_1 = (1/2, 1/2)$, $r_1 = (1/2, 1/2)$.
- $\rho_1 = 1/(4 - 1/2) = 2/7$, $d_1 = \frac{2}{7} \cdot \frac{1}{2} d_0 + \frac{4}{7} r_1 = (5/14, 5/14)$, $x_2 = (6/7, 6/7)$.

Here $b$ is the eigenvector for $\lambda = 1$, so $e_k = p_k(1) e_0 = e_0 / T_k(2)$. The errors $1, 1/2, 1/7, 1/26, 1/97$ are $1/T_k(2)$ for $k = 0, \dots, 4$, and $T_k(2) = \frac{1}{2}((2 + \sqrt 3)^k + (2 - \sqrt 3)^k)$, so the rate is $q = 1/(2 + \sqrt 3) = (\sqrt 3 - 1)/(\sqrt 3 + 1) \approx 0.268$, as the theory predicts for $\kappa = 3$. The test file reproduces these numbers in rational arithmetic.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Polynomial form** (exact arithmetic, any $A$). $e_k = p_k(A) e_0$ and $r_k = p_k(A) r_0$ with $p_k$ as above, and $x_k \in x_0 + \mathcal K_k(A, r_0)$, the [Krylov subspace](/krylov-subspace/).
2. **Optimality** (Chebyshev). Among polynomials of degree $\le k$ with $p(0) = 1$, $p_k$ has the least maximum on $[\lambda_{\min}, \lambda_{\max}]$, namely $1/T_k(\sigma_1)$ (Saad, Theorem 6.25).
3. **Error bound.** If $A$ is symmetric (or normal) with spectrum in $[\lambda_{\min}, \lambda_{\max}]$, then
$$\|e_k\|_2 \le \frac{\|e_0\|_2}{T_k(\sigma_1)} \le 2 q^k \|e_0\|_2, \qquad q = \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1},$$
and the same for $r_k$ and in the $A$-norm. So $k \ge \ln(2/\varepsilon)/\ln(1/q)$ steps, and in particular $k = \lceil (\sqrt\kappa/2) \ln(2/\varepsilon) \rceil$, give a reduction by $\varepsilon$. If $A = X \Lambda X^{-1}$ is diagonalizable with real spectrum in the interval, multiply by $\kappa_2(X)$.
4. **Termination** of the code after at most $\mathrm{kmax} + 1$ passes.

The bound is sharp for the worst $e_0$, and on the 1D Laplacian with $n = 60$ ($\kappa \approx 1507$) the test observes 365 steps for $\varepsilon = 10^{-8}$ against the bound 371. CG, which adapts to the actual spectrum, never needs more steps than this and usually needs fewer.

**Floating point.** The three-term recurrence is a stable way to evaluate the polynomial: the computed iterates have errors that stay bounded by a modest multiple of $u$ times $\max_j \|x_j\|$ and $\|A\| \|d_j\|$ summed over the steps, and the true residual can be kept near the updated one by computing $r$ from $b - A x$ occasionally (Gutknecht and Röllin 2002; their analysis gives worst-case bounds, observed behavior is better). Wrong bounds matter more than rounding: if some eigenvalue $\lambda > \lambda_{\max}$, then $|p_k(\lambda)|$ grows like $\left(\frac{|\theta - \lambda| + \sqrt{(\theta - \lambda)^2 - \delta^2}}{\delta}\right)^k / T_k(\sigma_1)$, which exceeds 1 once $\lambda > 2\theta$ and then diverges geometrically. The test with $\lambda_{\max} = 2$ for the 1D Laplacian (true value near 4) shows this.

## Complexity

Proof in [proofs/complexity.md](proofs/complexity.md). One matvec ($2 z$ flops) and three vector updates per step: L6 and L7 cost $n$ each and L9 $3 n$; the stopping norm adds $2 n$ when evaluated. So $2 z + 7 n + O(1)$ flops per step, $\Theta(n)$ extra storage ($x$, $r$, $d$, $w$), and $O(z \sqrt\kappa \ln(2/\varepsilon))$ time for a reduction by $\varepsilon$.

The method has no inner products in the loop. On distributed memory machines inner products are global reductions whose latency dominates sparse Krylov methods, so Chebyshev iteration can beat CG in time though it takes more steps. With few nonzeros per row the step is limited by memory traffic: it streams $A$ and about five vectors per step, the same as one CG step.

## Properties

- **Polynomial method, nonadaptive**: the iterates depend on $b$, $x_0$ and the two bounds only, not on inner products.
- **Optimal over the interval**, not over the actual spectrum: CG is never slower in the $A$-norm (for SPD $A$), and much faster when the spectrum clusters.
- **Linear and fixed**: $x_k$ is a fixed linear function of $b$ for fixed $k$ and $x_0 = 0$, so a fixed number of steps is a symmetric linear operator when $A$ is symmetric. That makes it usable as a [preconditioner](/preconditioning/) inside CG and as a smoother in [multigrid](/multigrid-method/), where it targets the interval $[\lambda_{\max}/\alpha, \lambda_{\max}]$ of high frequencies.
- **Needs a definite spectrum**: for an interval containing 0 there is no polynomial with $p(0) = 1$ that is small on it; the implementation rejects $\lambda_{\min} \le 0$.

## Variants and improvements

- **Chebyshev acceleration of a stationary method**: apply the recurrence to $x = G x + c$ with the eigenvalues of $G$ in $[\alpha, \beta]$, $\beta < 1$; for Jacobi this is the Chebyshev semi-iterative method of Golub and Varga (1961). For SSOR it gives a $\sqrt{}$ speedup on top of SSOR's.
- **Nonsymmetric matrices**: Manteuffel (1977) uses ellipses in the complex plane containing the spectrum, with adaptive estimates of the ellipse.
- **Adaptive bounds**: estimate $\lambda_{\max}$ by a few [Lanczos](/lanczos-algorithm/) or CG steps, or by [Gershgorin](/gershgorin-circle-theorem/) discs, and $\lambda_{\min}$ by inverse iteration, then restart.
- **Second order Richardson** (Frankel 1950) is the stationary limit with the asymptotic parameters, simpler but slower at the start.
- **Polynomial preconditioning**: a fixed degree Chebyshev polynomial as $M^{-1}$ for CG or GMRES.

## When to use it

Use it when good eigenvalue bounds are available cheaply (from the physics, Gershgorin, or a few Lanczos steps), when inner products are expensive (large parallel machines, GPUs), or when a fixed linear operator is required (multigrid smoothers, preconditioners for CG). Otherwise CG is simpler and adapts to the spectrum without bounds.

## Pitfalls

- **Underestimated $\lambda_{\max}$** gives divergence; overestimate it a little (Gershgorin is safe for symmetric $A$).
- **Wrong $\lambda_{\min}$.** If the bound is above the true smallest eigenvalue $\lambda > 0$, that component still decays, since $T_k(s(\lambda)) < T_k(\sigma_1)$, but slowly, and it ends up dominating the error; underestimating $\lambda_{\min}$ slows all components through a larger $\sqrt\kappa$ (the test with $\lambda_{\min}/10$ observes more steps).
- **Singular or indefinite A**: no valid interval exists. With a singular $A$ and a positive $\lambda_{\min}$, the null space component of the error never changes and an inconsistent $b$ never converges; the code returns NOT-CONVERGED.
- **The $\delta = 0$ case** must be handled separately (division by zero in $\sigma_1$).
- **Residual drift** in long runs: recompute $r = b - A x$ every few hundred steps.

## Implementations

## History

Chebyshev polynomials were introduced by Chebyshev (1854) for best uniform approximation. Flanders and Shortley (1950) used them to accelerate iterations for eigenvalue and boundary value problems, and Lanczos (1952) and Stiefel (1958) studied polynomial iterations. Golub and Varga (1961) gave the three-term Chebyshev semi-iterative method and related it to SOR and second order Richardson. Manteuffel (1977) extended the method to nonsymmetric matrices with ellipses, and Gutknecht and Röllin (2002) analyzed its rounding errors. It remains in use as a smoother in algebraic multigrid and as a communication-avoiding solver.

## References
