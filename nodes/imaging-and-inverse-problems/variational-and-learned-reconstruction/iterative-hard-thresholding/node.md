---
tag: M2CY6N
kind: algorithm
slug: iterative-hard-thresholding
name: Iterative hard thresholding
aliases:
- IHT
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Recover an s-sparse vector from y = Ax + e by a gradient step on the least squares residual followed by keeping only the s largest entries, repeated.
solves: [sparse-signal-recovery]
model: real-ram
complexity:
  vars: {K: the number of iterations, m: the number of measurements, n: the length of the signal}
  time: {worst: O(K m n)}
  space: {extra: O(m + n)}
properties: {deterministic: true, iterative: true, matrix_free: true, convex: false, needs_sparsity_level: true}
history:
  year: 2008
  people: [Thomas Blumensath, Mike E. Davies]
  note: Blumensath and Davies (2008) derived the iteration as a majorization-minimization method for the l0 constrained least squares problem. Their 2009 paper proved stable recovery under a restricted isometry condition on delta_3s, and their 2010 paper added an adaptive step.
prereqs: [sparse-signal-recovery, restricted-isometry-property, least-squares-problem]
see_also: [cosamp, orthogonal-matching-pursuit, iterative-shrinkage-thresholding, approximate-message-passing, basis-pursuit, compressed-sensing, mutual-coherence, proximal-gradient-method]
sources:
  - paper: doi:10.1007/s00041-008-9035-z
    title: Thomas Blumensath and Mike E. Davies, Iterative thresholding for sparse approximations, Journal of Fourier Analysis and Applications 14(5-6), 2008
    locator: pages 629 to 654 (the iteration as a majorization-minimization method and the decrease of the residual for ||A|| < 1)
  - paper: doi:10.1016/j.acha.2009.04.002
    title: Thomas Blumensath and Mike E. Davies, Iterative hard thresholding for compressed sensing, Applied and Computational Harmonic Analysis 27(3), 2009
    locator: pages 265 to 274 (the main recovery theorem under a bound on delta_3s)
  - paper: doi:10.1109/JSTSP.2010.2042411
    title: Thomas Blumensath and Mike E. Davies, Normalized iterative hard thresholding, guaranteed stability and performance, IEEE Journal of Selected Topics in Signal Processing 4(2), 2010
    locator: pages 298 to 309
  - paper: doi:10.1137/100806278
    title: Simon Foucart, Hard thresholding pursuit, an algorithm for compressive sensing, SIAM Journal on Numerical Analysis 49(6), 2011
    locator: pages 2543 to 2563
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhauser, 2013
    locator: chapter 3 (the algorithm) and chapter 6 (its analysis under the restricted isometry property)
---

Iterative hard thresholding (IHT) recovers a vector $x \in \mathbb{R}^n$ with at most $s$ nonzero entries from $m < n$ linear measurements $y = Ax + e$. Each step takes a gradient step on $\tfrac12\|y - Ax\|^2$ and then keeps only the $s$ entries of largest magnitude: $x^{k+1} = H_s(x^k + A^T(y - Ax^k))$. It works directly on the nonconvex problem $\min \|y - Ax\|^2$ subject to $\|x\|_0 \le s$ of [sparse signal recovery](/sparse-signal-recovery/). This is the difference to [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/), which applies soft thresholding (the [proximal operator](/proximal-operator/) of the $\ell_1$ norm) and solves a convex problem with a weight $\lambda$ instead of a known $s$. It also differs from [orthogonal matching pursuit](/orthogonal-matching-pursuit/), which adds one column per step and never removes one: IHT can change the whole support in every step. If the [restricted isometry constant](/restricted-isometry-property/) satisfies $\delta_{3s} < 1/2$, the error contracts by the factor $2\delta_{3s}$ per step up to a multiple of the noise. The cost of a step is one product with $A$ and one with $A^T$, so the method suits large problems with fast operators.

## The problem

Given a real $m \times n$ matrix $A$, a vector $y \in \mathbb{R}^m$ and a sparsity level $s$, find

$$\hat x \in \arg\min_{\|z\|_0 \le s} \|y - Az\|^2.$$

This problem is NP-hard in general (see [sparse signal recovery](/sparse-signal-recovery/)). IHT is a local method for it. The guarantee is for the compressed sensing setting: $y = Ax + e$ with an $s$-sparse $x$ and a matrix with a small restricted isometry constant, where IHT returns a point within a fixed multiple of $\|e\|$ from $x$. The input is $A$ (or routines for $Az$ and $A^Tr$), $y$, $s$ and a number of steps $K$. The output is an $s$-sparse vector.

## The algorithm

$H_s(v)$ keeps the $s$ entries of $v$ of largest magnitude and sets the others to zero. Ties are broken by a fixed rule, here the lower index.

```pseudo id=main
IHT(A, y, s, μ, K)
L1  x ← 0                         ▷ any s-sparse start
L2  for k = 1 to K
L3      r ← y - A x               ▷ residual
L4      g ← Aᵀ r                  ▷ minus the gradient of ½‖y - Ax‖²
L5      x ← H_s(x + μ g)          ▷ gradient step, then keep the s largest entries
L6  return x
```

The plain method of Blumensath and Davies uses $\mu = 1$ and assumes that $A$ is scaled so that $\|A_Sz\| \approx \|z\|$ on sparse vectors. Line L5 is a projection: $H_s(v)$ is the closest $s$-sparse vector to $v$. So IHT is projected gradient descent onto the nonconvex set of $s$-sparse vectors. A practical loop also stops when the residual or the change in $x$ is small.

## Example

Take $m = 4$, $n = 8$ and $A = [I \mid H/2]$, where $H$ is the $4 \times 4$ Sylvester Hadamard matrix with rows $(1,1,1,1)$, $(1,-1,1,-1)$, $(1,1,-1,-1)$, $(1,-1,-1,1)$. The columns have unit norm. Let $x$ have $x_1 = 1$ and $x_6 = 2$, all other entries zero, so $s = 2$ and $y = e_1 + 2 \cdot \tfrac12(1, -1, 1, -1) = (2, -1, 1, -1)$.

Step 1 starts from $x^0 = 0$. Then $u = A^Ty = (2, -1, 1, -1, 0.5, 2.5, 0.5, 0.5)$, and $H_2$ keeps entries 6 and 1. So $x^1$ has $x_1 = 2$ and $x_6 = 2.5$, with the correct support. From now on the support stays fixed, and the step acts on the two entries as $z \mapsto z + (I - G)(\text{target} - z)$ with $G = \begin{pmatrix} 1 & 1/2 \\ 1/2 & 1\end{pmatrix}$. The matrix $I - G$ has eigenvalues $\pm\tfrac12$, so the error halves in each step.

| $k$ | $x^k_1$ | $x^k_6$ | $\lVert x^k - x\rVert$ |
|---|---|---|---|
| 1 | 2 | 2.5 | 1.1180 |
| 2 | 0.75 | 1.5 | 0.5590 |
| 3 | 1.25 | 2.125 | 0.2795 |
| 4 | 0.9375 | 1.875 | 0.1398 |
| 5 | 1.0625 | 2.03125 | 0.0699 |

The same matrix shows that the method can fail. With $x_1 = 2$ and $x_6 = -1$, so $y = (1.5, 0.5, -0.5, 0.5)$, the iterates from $x^0 = 0$ alternate for ever between the vector with $x_1 = 1.5$, $x_5 = 1$ and the vector with $x_1 = 1$, $x_3 = -1$. The residual norms alternate between about 1.118 and 1, so the residual also grows in every second step. The true $x$ is a fixed point of the iteration, but the run never reaches it. This matrix has coherence $1/2$ and $\|A\|^2 = 2$, so neither the recovery theorem nor the descent theorem below applies.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has two parts.

The first part is the recovery guarantee. Let $T$ be the union of the supports of $x$, $x^k$ and $x^{k+1}$, so $|T| \le 3s$. On $T$, the step is $u_T - x_T = (I - A_T^TA_T)(x^k - x)_T + A_T^Te$, and the restricted isometry property bounds $\|I - A_T^TA_T\| \le \delta_{3s}$. Since $x^{k+1}$ is the best $s$-term approximation of $u$, it is at least as close to $u_T$ as $x$ is, and the triangle inequality gives

$$\|x^{k+1} - x\| \le 2\delta_{3s}\|x^k - x\| + 2\sqrt{1 + \delta_{3s}}\,\|e\|.$$

So for $\delta_{3s} < 1/2$ the error falls geometrically to at most $2\sqrt{1 + \delta_{3s}}\,\|e\|/(1 - 2\delta_{3s})$. This simple argument gives the condition $\delta_{3s} < 1/2$. Blumensath and Davies (2009) state their theorem under $\delta_{3s} < 1/\sqrt{32}$, and Foucart (2011) proves recovery under $\delta_{3s} < 1/\sqrt{3}$; these are cited, not proved here.

The second part holds for every $y$: if $\|A\| \le 1$, the residual $\|y - Ax^k\|$ does not increase from $k = 1$ on. The proof writes the step as the exact minimization of a surrogate function that lies above $\|y - Ax\|^2$ and touches it at the current iterate. This is a statement about the residual, not about the distance to $x$.

## Complexity

Each iteration costs one product with $A$, one with $A^T$ and one selection of the $s$ largest entries. For a dense matrix this is $O(mn)$ time per step, so $K$ steps cost $O(Kmn)$. The selection costs $O(n)$ with a linear time selection algorithm or $O(n \log n)$ with a sort, which is less than the products. For a partial Fourier or Hadamard matrix the products cost $O(n \log n)$ with the FFT or the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/). The extra memory is $O(m + n)$ for $r$, $g$ and $x$. Under $\delta_{3s} < 1/2$ the number of steps to reach accuracy $\varepsilon\|x\|$ without noise is $O(\log(1/\varepsilon))$ by the contraction factor $2\delta_{3s}$.

## Properties

- Every iterate is exactly $s$-sparse (or sparser), unlike the iterates of ISTA.
- The true $x$ is a fixed point when $e = 0$, because then $A^T(y - Ax) = 0$ and $H_s(x) = x$. Other $s$-sparse fixed points and cycles can exist when the restricted isometry property fails, as the example shows.
- The guarantee is uniform: one matrix with $\delta_{3s} < 1/2$ recovers every $s$-sparse $x$, and the error bound is linear in $\|e\|$. If $x$ is not exactly sparse, the bound holds with $x$ replaced by its best $s$-term approximation and $e$ by $e + A(x - H_s(x))$.
- It is not scale invariant: multiplying $A$ by 2 changes the iterates, because the step is fixed. The theory needs $A$ to be close to an isometry on sparse vectors.
- It needs only products with $A$ and $A^T$, so it is matrix free.

## Variants and improvements

- Normalized IHT (Blumensath and Davies 2010) chooses the step $\mu_k = \|g_S\|^2/\|A_Sg_S\|^2$ on the current support $S$ and shrinks it when the support changes and the residual would grow. This removes the dependence on the scaling of $A$ and gives guarantees that do not depend on that scaling.
- Hard thresholding pursuit (Foucart 2011) uses the support chosen by line L5 and then solves least squares on it. It stops after a finite number of steps when the support repeats.
- [CoSaMP](/cosamp/) and subspace pursuit pick a larger candidate set, solve least squares on it and prune to $s$ entries. They cost more per step and have similar guarantees.
- The same projected gradient idea works for low rank matrices, with a truncated SVD in place of $H_s$, and for other structured sparsity models with a projection onto the model set.
- Accelerated forms add a momentum term as in FISTA. They are heuristics: the recovery theorems are for the plain form.

## When to use it

Use IHT when the sparsity level $s$ is known or can be bounded, when $A$ is applied through a fast transform and when memory is tight. Each step is as cheap as a step of ISTA, and the iterates are sparse. When $s$ is not known but a noise level or a weight is, $\ell_1$ methods such as [basis pursuit](/basis-pursuit/) or ISTA are easier to tune. When $s$ is small and $A$ is explicit, [orthogonal matching pursuit](/orthogonal-matching-pursuit/) needs only $s$ steps. For Gaussian matrices in the large system limit, [approximate message passing](/approximate-message-passing/) recovers more sparse vectors per measurement.

## Pitfalls

- The unit step is only safe when $A$ behaves like an isometry on sparse vectors. Random Gaussian matrices with entries of variance $1/m$ have $\|A\|^2 \approx (1 + \sqrt{n/m})^2$, and at small sizes their $\delta_{3s}$ is far above $1/2$. In a run with 20 random $32 \times 64$ Gaussian matrices and $s = 3$, the unit step recovered $x$ in 15 cases, diverged in 3 and stopped at a wrong point in 2. This is a measurement. Use the normalized step or scale $A$ so that $\|A\| < 1$ when the theory does not apply.
- With $\|A\| < 1$ the residual decreases, but the iterates can still stop at a wrong sparse point.
- The sparsity level $s$ is an input. If it is too small, the result misses entries. If it is too large, the condition on $\delta_{3s}$ is harder to meet and noise enters more entries.
- When several entries have the same magnitude, the result of $H_s$ depends on the tie rule. Fix the rule, or the runs are not reproducible.
- Do not compare IHT and ISTA at the same step without care: ISTA needs a step at most $1/\|A\|^2$ for its descent theorem, while IHT with unit step relies on the restricted isometry property instead.

## Implementations

## History

Blumensath and Davies (2008) studied iterative thresholding for the $\ell_0$ penalized and the $\ell_0$ constrained least squares problems. They derived the hard thresholding iteration as a majorization-minimization method and proved that it does not increase the cost when $\|A\| < 1$. In 2009 they proved that the method recovers sparse vectors stably under a condition on $\delta_{3s}$, with an error bound of the same form as that of [CoSaMP](/cosamp/). In 2010 they introduced the normalized form with an adaptive step. Foucart (2011) improved the condition and introduced hard thresholding pursuit, and the book of Foucart and Rauhut (2013) gives the method with its analysis.

## References
