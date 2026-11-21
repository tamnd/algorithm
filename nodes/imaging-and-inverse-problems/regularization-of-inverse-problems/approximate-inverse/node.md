---
tag: 7S6RR0
kind: algorithm
slug: approximate-inverse
name: Approximate inverse
aliases:
- mollifier method
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: Compute mollified values of the solution as inner products of the data with reconstruction kernels that are precomputed from the adjoint equation.
solves: [fredholm-integral-equation-first-kind]
model: real-ram
complexity:
  vars: {m: "the number of data values", n: "the number of unknowns", r: "the number of reconstruction points", s: "the number of data sets"}
  time: {precompute: "O(m^2 n + r m n + m^3 + r m^2)", per_data_set: "O(r m)", total: "O(m^2 n + r m n + m^3 + r m^2 + s r m)"}
  space: {extra: "O(m^2 + r m)"}
properties: {deterministic: true, iterative: false, linear_in_data: true, kernels_precomputed: true, regularization_parameter: "the mollifier width gamma", rate_example: "O(delta^(4/7)) for integration with a hat mollifier and a C2 solution"}
history:
  year: 1990
  people: [A. K. Louis, P. Maass]
  note: Louis and Maass introduced the mollifier method for linear operator equations of the first kind, and Louis developed it into the approximate inverse in 1996.
prereqs: [regularization-method, fredholm-integral-equation-first-kind]
see_also: [backus-gilbert-method, filtered-back-projection, radon-transform, lambda-tomography, resolution-matrix, point-spread-function, tikhonov-regularization, truncated-svd]
sources:
  - paper: "A. K. Louis and P. Maass, A mollifier method for linear operator equations of the first kind, Inverse Problems 6(3), 1990, 427 to 440"
    locator: the mollifier method and its convergence (general locator)
  - paper: "A. K. Louis, Approximate inverse for linear and some nonlinear problems, Inverse Problems 12(2), 1996, 175 to 190"
    locator: the approximate inverse, invariance properties of the kernels, and applications to tomography (general locator)
  - book: "T. Schuster, The Method of Approximate Inverse: Theory and Applications, Lecture Notes in Mathematics 1906, Springer, Berlin, 2007"
    locator: the theory of the method and its use in tomography (general locator)
---

The approximate inverse computes smoothed values of the solution of $A x = y$ directly from the data. Pick a mollifier $e_p$: a smooth bump with integral 1 and width $\gamma$, centered at the point $p$. The mollified solution $x_\gamma(p) = \langle x, e_p\rangle$ is a local average of $x$ near $p$, and it tends to $x(p)$ as $\gamma \to 0$. If the reconstruction kernel $\psi_p$ solves the adjoint equation $A^* \psi_p = e_p$, then
$$\langle y, \psi_p\rangle = \langle A x, \psi_p\rangle = \langle x, A^* \psi_p\rangle = \langle x, e_p\rangle = x_\gamma(p).$$
So one inner product of the data with $\psi_p$ gives the mollified value at $p$. The kernels depend only on $A$ and on the mollifiers, so they are computed once, stored, and used for every data set. The width $\gamma$ is the regularization parameter. A wider mollifier gives a kernel with a smaller norm, so less noise amplification, but a larger smoothing error. For [filtered back-projection](/filtered-back-projection/), the convolution filter is an approximate inverse kernel of the [Radon transform](/radon-transform/).

## In plain words

You cannot recover the exact value of the solution at a point from noisy data of an ill-posed problem. But you can recover a local average of the solution near that point. Decide first which average you want: its center and its width. Then solve one equation, which does not involve the data, for a weight vector that turns the data into exactly that average. After that, each reconstruction is only a weighted sum of the data. A narrow average shows more detail but lets more noise through. A wide average is stable but blurred.

## The problem

Given a bounded linear operator $A: X \to Y$ between Hilbert spaces (a real $m \times n$ matrix in the code), one or more data sets $y^\delta$ with $\|y^\delta - A x\| \le \delta$, and mollifiers $e_1, \dots, e_r \in X$ (in the code, rows of weights with $h \sum_i e_i = 1$ on a grid of step $h$), compute approximations of the mollified values $\langle x, e_i\rangle$, $i = 1, \dots, r$.

## The algorithm

```pseudo id=main
APPROXIMATE-INVERSE(A, e₁…eᵣ, data sets Y, β)       ▷ β ≥ 0
L1  compute the kernels once, independent of the data:
L2      bᵢ ← A eᵢ                    for i = 1, …, r
L3      solve (A Aᵀ + β I) ψᵢ = bᵢ   for i = 1, …, r
L4      Ψ ← (ψ₁, …, ψᵣ)
L5  for each data set y in Y do
L6      x̂ᵢ ← ⟨y, ψᵢ⟩                for i = 1, …, r
```

Line L1 starts the precomputation; it uses only $A$, the mollifiers and $\beta$. In the discrete setting the adjoint equation $A^\top \psi = e$ can have no exact solution, so lines L2 and L3 compute the minimizer of $\|A^\top \psi - e\|^2 + \beta\|\psi\|^2$, which is $\psi = (A A^\top + \beta I)^{-1} A e$. With $\beta = 0$ and $A$ square and nonsingular this is $\psi = A^{-\top} e$, the exact solution of the adjoint equation. Line L3 factors one $m \times m$ matrix and solves for all $r$ right-hand sides together. Line L4 stores the kernels. Lines L5 and L6 are the whole reconstruction: $r$ inner products per data set.

When $A$ commutes with a group of shifts or rotations (convolution, the Radon transform), a shifted mollifier has the shifted kernel, so only one kernel has to be computed (Louis 1996). The code tests this for a circulant blur.

## Example

**A small discrete case.** Let $A$ be the $10 \times 10$ matrix of cumulative sums $(A x)_i = h\sum_{j \le i} x_j$ with $h = 0.1$, the discrete form of $(A x)(s) = \int_0^s x(t)\,dt$. Take the mollifier weights $e = (0, 0, 0, \tfrac18, \tfrac38, \tfrac38, \tfrac18, 0, 0, 0)$, a hat of half width $0.2$ centered at $p = 0.5$, with sum 1. The adjoint equation $A^\top \psi = e$ reads $h \sum_{i \ge j} \psi_i = e_j$, so $\psi_j = (e_j - e_{j+1})/h$:
$$\psi = (0, 0, -1.25, -2.5, 0, 2.5, 1.25, 0, 0, 0).$$
The kernel is a scaled difference of the mollifier, so $\langle y, \psi\rangle$ is a smoothed second difference of the data: numerical differentiation, which is what inverting integration means. For $x_j = \sin(\pi t_j)$ at the cell centers $t_j = (j - 0.5)h$, the estimate is $\langle A x, \psi\rangle = 0.96352$. This is exactly the average $\tfrac18 x_4 + \tfrac38 x_5 + \tfrac38 x_6 + \tfrac18 x_7 = \tfrac14(0.89101) + \tfrac34(0.98769)$, not the point value $x(0.5) = 1$.

**The width as the regularization parameter.** In the continuous case, with the hat $e_p(t) = \gamma^{-1}\max(0, 1 - |t - p|/\gamma)$, the kernel is $\psi_p = -e_p'$, which is $1/\gamma^2$ on $(p, p + \gamma)$ and $-1/\gamma^2$ on $(p - \gamma, p)$. So
$$x_\gamma(p) = \frac{1}{\gamma^2}\Big(\int_p^{p+\gamma} y - \int_{p-\gamma}^{p} y\Big), \qquad \|\psi_p\| = \sqrt2\,\gamma^{-3/2}.$$
Two errors compete. The smoothing error for $x(t) = \sin(\pi t)$ at $p = 1/2$ is about $|x''(p)|\gamma^2/12 = \pi^2\gamma^2/12$. The noise error is at most $\delta\|\psi_p\| = \sqrt 2\,\delta\gamma^{-3/2}$. The code computes the integrals on a grid with $N = 4000$; the smoothing error is measured, and the noise bound is the worst case. For $\delta = 10^{-3}$:

| $\gamma$ | smoothing error | noise bound $\sqrt2\,\delta\gamma^{-3/2}$ | sum |
|---|---|---|---|
| 0.05 | 0.00205 | 0.1265 | 0.1285 |
| 0.1 | 0.00820 | 0.0447 | 0.0529 |
| 0.139 | 0.0158 | 0.0273 | 0.0431 |
| 0.2 | 0.0325 | 0.0158 | 0.0483 |
| 0.3 | 0.0719 | 0.0086 | 0.0805 |

Balancing $\gamma^2$ against $\delta\gamma^{-3/2}$ gives $\gamma \sim \delta^{2/7}$ and a total error of order $\delta^{4/7}$. With $\gamma = \delta^{2/7}$ the sums are $0.160$, $0.0431$, $0.0116$ and $0.0031$ for $\delta = 10^{-2}, 10^{-3}, 10^{-4}, 10^{-5}$. Each step divides the error by about $3.72$, and $10^{4/7} = 3.73$. A random noise vector of norm $\delta$ does much less harm than the worst case: for $\delta = 10^{-3}$ and $\gamma = 0.139$, the Gaussian noise of the test (seed 64) changed the estimate by only $6.4 \cdot 10^{-5}$.

## Correctness

The proofs are in proofs/correctness.md, in exact arithmetic.

- **Exact recovery of mollified values (theorem).** If $A^\top \psi = e$, then $\langle A x, \psi\rangle = \langle x, e\rangle$ for every $x$. With $\beta = 0$ and $A$ square and nonsingular, lines L2 and L3 give such a $\psi$, so line L6 returns the mollified values of $x$ from exact data.
- **The kernel minimizes the adjoint residual (theorem).** For $\beta > 0$, line L3 gives the unique minimizer of $\|A^\top \psi - e\|^2 + \beta\|\psi\|^2$. For $\beta = 0$ and $A A^\top$ invertible, it gives the unique minimizer of $\|A^\top \psi - e\|$.
- **Noise bound (theorem).** $|\langle y^\delta, \psi\rangle - \langle y, \psi\rangle| \le \delta\|\psi\|$, with equality for the worst noise.
- **Invariance (theorem).** If $S$ is orthogonal and commutes with $A$, then the kernel of $S e$ is $S\psi$.
- **Termination.** The algorithm has no loop with a data-dependent length.

The convergence of $x_\gamma(p)$ to $x(p)$ as $\delta \to 0$ with a suitable $\gamma(\delta)$ follows from these bounds and the smoothing error of the mollifier, as in the example. General convergence results under conditions on $A$ and the mollifier are in Louis and Maass (1990) and Schuster (2007).

## Complexity

- **Precomputation.** Forming $A A^\top$ costs $O(m^2 n)$, the right-hand sides $A e_i$ cost $O(r m n)$, and the solve costs $O(m^3 + r m^2)$.
- **Per data set.** $r$ inner products of length $m$, so $O(r m)$. This is the point of the method: in imaging with many data sets of the same geometry, each reconstruction is as cheap as one matrix-vector product.
- **With invariance.** If the kernels are shifts of one kernel, line L6 is a convolution, which the FFT computes in $O(m \log m)$ (see the [convolution theorem](/convolution-theorem/)), and only one kernel is stored.
- **Space.** $O(m^2 + r m)$, or $O(m)$ with invariance and a matrix-free solver.

## Properties

- **Linear in the data.** The reconstruction is $\hat x = \Psi^\top y$ for a fixed matrix $\Psi$.
- **Known resolution.** Exact data give exactly the chosen averages, so the averaging kernels (the rows of the [resolution matrix](/resolution-matrix/)) are the mollifiers themselves, chosen in advance. Compare the [Backus-Gilbert method](/backus-gilbert-method/), which computes the best averaging kernel instead.
- **Data independent cost.** All the expensive work is done before any data are measured.
- **Regularization by the width.** $\gamma$ plays the role of $\alpha$ in Tikhonov regularization. With $\beta > 0$ there is a second parameter, needed when the adjoint equation is not solvable.

## Variants and improvements

- **Invariant kernels.** For the Radon transform with rotation and translation invariant mollifiers, one kernel gives filtered back-projection with a filter determined by the mollifier (Louis 1996).
- **Lambda tomography.** Choosing a mollifier that also applies a differential operator gives local reconstructions of edges (see [lambda tomography](/lambda-tomography/)).
- **Kernels by singular value expansion.** If the singular system of $A$ is known, $\psi = \sum_j \sigma_j^{-1} \langle e, v_j\rangle u_j$, truncated or filtered.
- **Nonlinear problems and Banach spaces.** Louis (1996) and Schuster (2007) describe extensions, including the use of approximate inverse kernels inside iterations.

## When to use it

Use the approximate inverse when the same operator is applied to many data sets, so that a costly precomputation pays off, as in tomography with a fixed scanner geometry. It is also a good choice when you want to say in advance which local averages you reconstruct, for example to report a known resolution. If $A$ changes from one problem to the next, or you need only one reconstruction, a [Tikhonov](/tikhonov-regularization/) or [truncated SVD](/truncated-svd/) solution is simpler. If you want the averaging kernel with the best trade-off between width and noise at each point, use the [Backus-Gilbert method](/backus-gilbert-method/).

## Pitfalls

- **No exact solution of the adjoint equation.** If $e$ is not in the range of $A^\top$, then $\langle y, \psi\rangle$ is not exactly the mollified value; the error is $\langle x, A^\top \psi - e\rangle$. Check the residual $\|A^\top \psi - e\|$ after line L3.
- **$\beta = 0$ with a rank deficient $A$.** Then $A A^\top$ is singular and line L3 fails. Use a small $\beta > 0$.
- **A mollifier too narrow.** $\|\psi\|$ grows fast as $\gamma \to 0$ (like $\gamma^{-3/2}$ for integration), so noise dominates. Pick $\gamma$ from the noise level, not from the grid size.
- **Mollifier near the boundary.** In the example the closed form needs $\gamma \le p$ and $p + \gamma \le 1$. Near the edge of the domain the mollifier must be cut and renormalized, and the kernel changes.
- **Discrete and continuous inner products.** The code uses plain sums. If the mollifier is normalized so that $h \sum_i e_i = 1$, then $\langle x, e\rangle$ is $1/h$ times the average, as in the tests.

## Implementations

## History

A. K. Louis and P. Maass introduced the mollifier method for linear equations of the first kind in 1990. Louis developed it into the approximate inverse in 1996, with the invariance properties that make it efficient in tomography and with an interpretation of filtered back-projection as an approximate inverse. T. Schuster wrote a book on the theory and its applications (2007). The idea of reconstructing chosen local averages is close to the Backus-Gilbert method from geophysics (1967 to 1970), which instead optimizes the averaging kernel.

## References
