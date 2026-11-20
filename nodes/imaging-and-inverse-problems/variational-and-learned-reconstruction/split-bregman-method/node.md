---
tag: 4TK5JZ
kind: algorithm
slug: split-bregman-method
name: Split Bregman method
aliases:
- Goldstein-Osher split Bregman
- split Bregman iteration
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Solve L1 and total variation problems by moving the regularizer onto a new variable d = Φx, then alternate a linear solve, a shrinkage and a Bregman update.
solves: [image-denoising, image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of unknowns, m: the number of data values, q: the number of rows of Φ, K: the number of iterations}
  time: {worst: O(n^3 + K (n^2 + (m + q) n))}
  space: {extra: O(n^2 + q)}
properties: {deterministic: true, exact: false, iterative: true, converges_for_every_mu: true, equivalent_to_admm: true}
history:
  year: 2009
  people: [Tom Goldstein, Stanley Osher]
  note: Goldstein and Osher (2009) combined Bregman iteration with a splitting of the l1 term. Esser (2009) and Setzer (2009) showed that the method is ADMM, which gave a convergence proof for every penalty.
prereqs: [bregman-iteration, admm, proximal-operator, total-variation-denoising]
see_also: [augmented-lagrangian-method, chambolle-pock-algorithm, total-generalized-variation, compressed-sensing-mri, lasso-regression, iterative-shrinkage-thresholding, cholesky-decomposition, fast-fourier-transform]
sources:
  - paper: doi:10.1137/080725891
    title: Tom Goldstein and Stanley Osher, The split Bregman method for L1-regularized problems, SIAM Journal on Imaging Sciences 2(2), 2009
    locator: pages 323 to 343
  - paper: doi:10.1007/978-3-642-02256-2_39
    title: Simon Setzer, Split Bregman algorithm, Douglas-Rachford splitting and frame shrinkage, Scale Space and Variational Methods in Computer Vision (SSVM 2009), LNCS 5567
    locator: pages 464 to 476
  - paper: doi:10.1137/040605412
    title: Stanley Osher, Martin Burger, Donald Goldfarb, Jinjun Xu and Wotao Yin, An iterative regularization method for total variation-based image restoration, Multiscale Modeling and Simulation 4(2), 2005
    locator: pages 460 to 489
  - paper: doi:10.1561/2200000016
    title: Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato and Jonathan Eckstein, Distributed optimization and statistical learning via the alternating direction method of multipliers, Foundations and Trends in Machine Learning 3(1), 2011
    locator: pages 1 to 122
---

The split Bregman method solves problems of the form $\min_x \tfrac12\|Ax - y\|^2 + \lambda\|\Phi x\|_1$, where $\Phi$ is a linear map such as the image gradient. This covers [total variation denoising](/total-variation-denoising/), total variation deblurring and the [LASSO](/lasso-regression/). The $\ell_1$ term is hard because it is not smooth and $\Phi$ couples the unknowns. The method adds a new variable $d$ with the constraint $d = \Phi x$, so that the coupling and the nonsmooth part are in different variables. It then applies [Bregman iteration](/bregman-iteration/) to the constraint, with one alternating sweep per step: a linear solve for $x$, a [soft thresholding](/proximal-operator/) for $d$, and an update of the Bregman variable $b$. The method is the same as [ADMM](/admm/) with penalty $\mu$ and scaled multiplier $b$, so it converges for every $\mu > 0$, and $\mu b$ converges to a dual solution.

## In plain words

Some image problems ask for an image that matches the measurements and has few edges. The two wishes pull in different directions, and the "few edges" part has sharp corners that break normal solvers. The method gives the edges their own variable. Now there are two easy jobs. The first job finds an image that matches the measurements and is close to the current edge map: this is a linear system, which is easy. The second job cleans the edge map by setting small edges to zero: this is one simple rule per pixel. A third variable keeps a record of how much the edge map and the image still disagree, and it pushes them together a little more at each round. After enough rounds they agree, and the image is the solution of the original problem.

## The problem

The input is a matrix $A \in \mathbb{R}^{m \times n}$, data $y \in \mathbb{R}^m$, a matrix $\Phi \in \mathbb{R}^{q \times n}$, a weight $\lambda > 0$ and a penalty $\mu > 0$. The goal is a minimizer of

$$F(x) = \tfrac12\|Ax - y\|^2 + \lambda N(\Phi x),$$

where $N$ is the $\ell_1$ norm (anisotropic total variation when $\Phi$ is the gradient) or the sum of the Euclidean norms of pairs $\big((\Phi x)_i, (\Phi x)_{i+g}\big)$ (isotropic total variation, with the horizontal and vertical differences of one pixel in one pair). We require that $A$ and $\Phi$ have no common null vector, so that $M = A^\top A + \mu\Phi^\top\Phi$ is positive definite and $F$ has a minimizer. For denoising $A = I$ and this holds for any $\Phi$. The weight $\lambda$ is a design choice of the model; the penalty $\mu$ is a parameter of the solver and does not change the solution.

## The algorithm

The split problem is $\min_{x, d} \tfrac12\|Ax - y\|^2 + \lambda N(d)$ subject to $d = \Phi x$. Bregman iteration on the constraint, with the quadratic penalty $\tfrac\mu2\|d - \Phi x - b\|^2$, and one Gauss-Seidel sweep over $x$ and $d$ in place of the exact joint solve, gives:

```pseudo id=main
SplitBregman(A, y, Φ, λ, μ, K)
L1  factor M = AᵀA + μΦᵀΦ by Cholesky; d ← 0; b ← 0
L2  for k = 0 to K - 1
L3      x ← M⁻¹ (Aᵀy + μΦᵀ(d - b))          ▷ argmin ½‖Ax - y‖² + μ/2‖Φx - d + b‖²
L4      d ← shrink(Φx + b, λ/μ)             ▷ argmin λN(d) + μ/2‖d - Φx - b‖²
L5      b ← b + Φx - d                       ▷ Bregman update, add back the misfit
L6  return x
```

For the $\ell_1$ norm, $\operatorname{shrink}(v, t)_i = \operatorname{sign}(v_i)\max(|v_i| - t, 0)$. For the isotropic norm, each pair $w$ of $v$ is replaced by $w \max(\|w\| - t, 0)/\|w\|$. Both are the [proximal operator](/proximal-operator/) of $tN$. Line L3 is the only coupled step. Here it uses a [Cholesky factor](/cholesky-decomposition/) computed once. For deconvolution with periodic boundaries, $M$ is diagonalized by the [fast Fourier transform](/fast-fourier-transform/), and for large problems a few [conjugate gradient](/conjugate-gradient-method/) or Gauss-Seidel steps are enough.

Line L5 is the Bregman step of the constraint $d = \Phi x$: the misfit $\Phi x - d$ is added back, in the same way as Bregman iteration adds back the data residual. If lines L3 and L4 were repeated until $(x, d)$ minimizes the joint problem, the method would be exact Bregman iteration, which is the [augmented Lagrangian method](/augmented-lagrangian-method/) for the split problem. One sweep is enough, and that is the point of the method.

## Example

Take total variation denoising of the signal $f = (0, 0, 3, 3)$: $A = I$, $\Phi = D$ the forward difference matrix with 3 rows, $\lambda = 1$ and $\mu = 1$. Then $M = I + D^\top D$ is tridiagonal with diagonal $(2, 3, 3, 2)$ and off diagonal $-1$.

Step 1: with $d = b = 0$, line L3 solves $Mx = f$, which gives $x = (3/7, 6/7, 15/7, 18/7)$. Then $Dx = (3/7, 9/7, 3/7)$, and shrinkage by $\lambda/\mu = 1$ gives $d = (0, 2/7, 0)$. Line L5 gives $b = Dx - d = (3/7, 1, 3/7)$.

| $k$ | $x^k$ | $d^k$ | $b^k$ | $F(x^k)$ |
|---|---|---|---|---|
| 1 | $(0.4286, 0.8571, 2.1429, 2.5714)$ | $(0, 0.2857, 0)$ | $(0.4286, 1, 0.4286)$ | 3.0612 |
| 2 | $(0.7143, 1, 2, 2.2857)$ | $(0, 1, 0)$ | $(0.7143, 1, 0.7143)$ | 3.0816 |
| 3 | $(0.7347, 0.7551, 2.2449, 2.2653)$ | $(0, 1.4898, 0)$ | $(0.7347, 1, 0.7347)$ | 2.6406 |
| 5 | $(0.6064, 0.5394, 2.4606, 2.3936)$ | $(0, 1.9213, 0)$ | $(0.6064, 1, 0.6064)$ | 2.7140 |
| 10 | $(0.4997, 0.4968, 2.5032, 2.5003)$ | $(0, 2.0064, 0)$ | $(0.4997, 1, 0.4997)$ | 2.5088 |
| 20 | $(0.5, 0.5, 2.5, 2.5)$ | $(0, 2, 0)$ | $(0.5, 1, 0.5)$ | 2.5000 |

The limit $x = (0.5, 0.5, 2.5, 2.5)$ is the exact total variation solution: each half moves toward the other by $\lambda$ divided by its length 2, and $F = \tfrac12 \cdot 4 \cdot 0.25 + 2 = 2.5$. The edge variable $d$ has the single jump 2 at the right place from step 2 on; only its size still changes. The limit $\mu b = (0.5, 1, 0.5)$ is the dual solution: it satisfies $x - f + D^\top(\mu b) = 0$, its entries are at most $\lambda = 1$ in size, and it equals $\lambda$ where $Dx$ is not zero. The table also shows that $F(x^k)$ is not monotone (it rises at steps 2 and 5), so it is not a useful stop test.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The steps:

- Equivalence with ADMM. With $f(x) = \tfrac12\|Ax - y\|^2$, $g(d) = \lambda N(d)$ and the constraint $\Phi x - d = 0$, lines L3 to L5 are the three steps of scaled ADMM with penalty $\rho = \mu$ and scaled multiplier $u = b$. This is a theorem (Esser 2009, Setzer 2009).
- Optimality of each step: with $v^k = \mu b^k$, line L3 gives $A^\top(Ax^{k+1} - y) + \Phi^\top(v^{k+1} + \mu(d^{k+1} - d^k)) = 0$, and line L4 gives $v^{k+1} \in \partial g(d^{k+1})$.
- A saddle point exists. Since $A$ and $\Phi$ have no common null vector, $F$ is coercive and has a minimizer $x^*$, and the [subdifferential](/subdifferential/) chain rule gives $v^*$ with $A^\top(Ax^* - y) + \Phi^\top v^* = 0$ and $v^* \in \partial g(\Phi x^*)$.
- Lyapunov function: $V_k = \tfrac1\mu\|v^k - v^*\|^2 + \mu\|d^k - d^*\|^2$ satisfies $V_{k+1} \le V_k - \mu\|\Phi x^{k+1} - d^{k+1}\|^2 - \mu\|d^{k+1} - d^k\|^2$ for $k \ge 1$. This follows from the monotonicity of $\nabla f$ and $\partial g$ only.
- Convergence: the iterates are bounded and the two residuals go to 0, so every cluster point satisfies the optimality conditions. Using $V$ with that cluster point gives convergence of the whole sequence: $x^k \to \bar x$, a minimizer of $F$, and $\mu b^k \to \bar v$, a dual solution. This holds for every $\mu > 0$.

## Complexity

With dense matrices, line L1 costs $O(n^3)$ once. Each step then costs $O(n^2)$ for the two triangular solves, $O((m + q)n)$ for the products with $A^\top$, $\Phi$ and $\Phi^\top$ (only $A^\top y$ is needed, and it is computed once), and $O(q)$ for the shrinkage. So $K$ steps cost $O(n^3 + K(n^2 + (m + q)n))$ time and $O(n^2 + q)$ extra memory for the factor and $d$, $b$. For an image with $N$ pixels, $\Phi$ the gradient and $A$ a convolution, all products cost $O(N)$ and line L3 costs $O(N \log N)$ with the FFT, so each step is $O(N \log N)$.

The rate is that of ADMM: the smallest squared constraint residual among the first $K$ steps is at most $V_0/(\mu K)$, and the averaged iterates of $(x, d)$ have an objective error and a constraint residual of order $1/K$ (see the [ADMM](/admm/) page). These are theorems. In the example above, 20 steps give 4 correct digits; that is a measurement on one small problem, and the count depends on $\mu$.

## Properties

- The penalty $\mu$ does not change the limit, only the speed. A large $\mu$ enforces $d = \Phi x$ fast but shrinks by the small amount $\lambda/\mu$, so the edge set settles slowly. A small $\mu$ does the opposite. This trade-off is a heuristic, not a theorem.
- Line L3 is a linear system with the same matrix at every step. This is the main practical gain over methods that need a new system per step.
- Line L4 sets entries of $d$ exactly to zero, so the edge map is sparse at every step, while $x$ is only close to piecewise constant.
- At a limit, $\mu b$ is a dual certificate; a stop test can use the two residuals $\|\Phi x^{k} - d^k\|$ and $\mu\|\Phi^\top(d^{k} - d^{k-1})\|$, as for ADMM.
- The objective $F(x^k)$ is not monotone.
- The iteration is deterministic and uses no step size, unlike [Chambolle-Pock](/chambolle-pock-algorithm/), whose steps must satisfy $\tau\sigma\|K\|^2 < 1$.

## Variants and improvements

- Several inner sweeps: Goldstein and Osher allow $N$ sweeps of lines L3 and L4 before line L5. Many sweeps approach the augmented Lagrangian method, one sweep is ADMM. One sweep is usually the fastest.
- Inexact line L3: one Gauss-Seidel sweep for $x$, as in the original paper for denoising, or a few conjugate gradient steps. The method still works in practice; the convergence proof above needs an exact solve or summable errors.
- More splittings: for problems with several terms, for example a total variation term and a nonnegativity constraint, each term gets its own variable and Bregman variable. This is ADMM with several blocks stacked into one $d$.
- Frames and wavelets: $\Phi$ can be a tight frame. Setzer (2009) related the method to Douglas-Rachford splitting on the dual problem and studied frame shrinkage.
- [Total generalized variation](/total-generalized-variation/) and other higher order models fit the same template with a larger $\Phi$.
- Adaptive penalty: changing $\mu$ during the run needs a new factor of $M$ and a rescaling $b \leftarrow b\,\mu_{\text{old}}/\mu_{\text{new}}$, so that $\mu b$ stays the same.

## When to use it

Use it when the regularizer is an $\ell_1$ norm of a linear map and the system $(A^\top A + \mu\Phi^\top\Phi)x = r$ is cheap to solve, for example deconvolution with the FFT, or [compressed sensing MRI](/compressed-sensing-mri/) with Fourier sampling, where both matrices are diagonal in the Fourier basis. If that system is expensive, a method that uses only products with $A$, $A^\top$, $\Phi$ and $\Phi^\top$ is better: [Chambolle-Pock](/chambolle-pock-algorithm/), or [iterative shrinkage thresholding](/iterative-shrinkage-thresholding/) when $\Phi = I$.

## Pitfalls

- A common null vector of $A$ and $\Phi$ makes $M$ singular. With $\Phi$ the gradient, constants are in the null space of $\Phi$, so $A$ must not map constants to 0. The implementation raises an error in that case.
- The shrinkage threshold is $\lambda/\mu$, not $\lambda$. Mixing the two gives the solution of a problem with a different weight.
- Line L5 must use the new $x$ and $d$ of the same step. With an old value it is not the Bregman update, and the proof does not apply.
- Changing $\mu$ without rescaling $b$ breaks the method, because the true multiplier is $\mu b$.
- The isotropic shrinkage must act on the pair of differences of one pixel together. Shrinking each component on its own gives anisotropic total variation, which favors edges along the axes.
- Do not judge convergence by $F(x^k)$, which can rise; use the residuals.

## Implementations

## History

Osher, Burger, Goldfarb, Xu and Yin (2005) introduced Bregman iteration for total variation imaging, and Yin, Osher, Goldfarb and Darbon (2008) applied it to $\ell_1$ problems. In 2009 Tom Goldstein and Stanley Osher proposed to split the $\ell_1$ term off with a new variable and to apply the Bregman update to the constraint. They gave fast results for total variation denoising and compressed sensing MRI. In the same year Ernie Esser (UCLA CAM report 09-31) and Simon Setzer showed that the method with one sweep is the alternating direction method of multipliers, which Glowinski and Marroco and Gabay and Mercier had studied in the 1970s, and that it is Douglas-Rachford splitting on the dual. This gave convergence for every $\mu > 0$ and placed the method in the wider family of operator splitting methods.

## References
