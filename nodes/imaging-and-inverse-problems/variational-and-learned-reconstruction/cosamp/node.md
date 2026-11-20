---
tag: E7NF54
kind: algorithm
slug: cosamp
name: CoSaMP
aliases:
- compressive sampling matching pursuit
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: A greedy sparse recovery method that adds 2s candidate columns by correlation with the residual, solves least squares on the merged support and prunes back to s entries.
solves: [sparse-signal-recovery]
model: real-ram
complexity:
  vars: {K: the number of iterations, m: the number of measurements, n: the length of the signal, s: the sparsity level}
  time: {worst: O(K (m n + m s^2))}
  space: {extra: O(m s + n)}
properties: {deterministic: true, iterative: true, greedy: true, needs_sparsity_level: true}
history:
  year: 2008
  people: [Deanna Needell, Joel A. Tropp]
  note: Needell and Tropp posted CoSaMP in 2008 and published it in 2009 with a uniform error bound under delta_4s <= 0.1. Dai and Milenkovic proposed the closely related subspace pursuit at the same time.
prereqs: [iterative-hard-thresholding, orthogonal-matching-pursuit, restricted-isometry-property, least-squares-problem]
see_also: [sparse-signal-recovery, compressed-sensing, basis-pursuit, iterative-shrinkage-thresholding, approximate-message-passing, qr-decomposition, mutual-coherence]
sources:
  - paper: doi:10.1016/j.acha.2008.07.002
    title: Deanna Needell and Joel A. Tropp, CoSaMP, iterative signal recovery from incomplete and inaccurate samples, Applied and Computational Harmonic Analysis 26(3), 2009
    locator: pages 301 to 321 (the algorithm, the iteration invariant under delta_4s <= 0.1 and the cost analysis)
  - paper: doi:10.1109/TIT.2009.2016006
    title: Wei Dai and Olgica Milenkovic, Subspace pursuit for compressive sensing signal reconstruction, IEEE Transactions on Information Theory 55(5), 2009
    locator: pages 2230 to 2249
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhauser, 2013
    locator: chapter 3 (the algorithm) and chapter 6 (its analysis under the restricted isometry property)
---

CoSaMP (compressive sampling matching pursuit) recovers a vector $x \in \mathbb{R}^n$ with at most $s$ nonzero entries from $y = Ax + e$ with $m < n$ measurements. Each iteration correlates the residual with the columns of $A$, adds the $2s$ best matching columns to the current support, solves a least squares problem on the merged set of at most $3s$ columns and keeps the $s$ largest entries of the solution. Like [orthogonal matching pursuit](/orthogonal-matching-pursuit/), it uses correlations and least squares, but OMP adds one column per step and never removes one, while CoSaMP adds many columns at once and can remove wrong ones. Like [iterative hard thresholding](/iterative-hard-thresholding/), it keeps an $s$-sparse iterate and has a uniform guarantee under the [restricted isometry property](/restricted-isometry-property/), but it replaces the gradient step by an exact least squares fit, so it often needs only a few iterations. Unlike [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/) and [basis pursuit](/basis-pursuit/), it needs the sparsity level $s$ and no weight $\lambda$. Needell and Tropp proved that under $\delta_{4s} \le 0.1$ each iteration halves the error up to a fixed multiple of the noise.

## The problem

Given a real $m \times n$ matrix $A$, a vector $y \in \mathbb{R}^m$ and a sparsity level $s$ with $3s \le m$, find an $s$-sparse $\hat x$ with small error $\|\hat x - x\|$, where $y = Ax + e$ and $x$ is $s$-sparse or close to an $s$-sparse vector. This is a form of [sparse signal recovery](/sparse-signal-recovery/). The output is an $s$-sparse vector.

## The algorithm

$H_s(v)$ keeps the $s$ entries of $v$ of largest magnitude. $A_T$ holds the columns of $A$ in the set $T$.

```pseudo id=main
CoSaMP(A, y, s, K)
L1  a ← 0
L2  for k = 1 to K
L3      p ← Aᵀ (y - A a)                    ▷ proxy: correlations with the residual
L4      Ω ← indices of the 2s largest |pᵢ|  ▷ identify
L5      T ← Ω ∪ supp(a)                     ▷ merge, |T| ≤ 3s
L6      b_T ← argmin ‖y - A_T z‖, b ← 0 off T ▷ least squares on T
L7      a ← H_s(b)                          ▷ prune to s entries
L8      stop if the residual ‖y - A a‖ is small or stops changing
L9  return a
```

Line L4 takes $2s$ columns, not $s$, because the error $x - a$ has up to $2s$ nonzero entries: $s$ from $x$ and $s$ from the current $a$. Line L5 keeps the old support, so a correct entry found earlier is not lost before the least squares step can weigh it. Line L6 is the only expensive step. Needell and Tropp solve it approximately with a few steps of conjugate gradients or LSQR, and the analysis allows this. The implementation here uses the pseudoinverse from a thin SVD of $A_T$, which also handles the case of dependent columns.

## Example

Take $m = 4$, $n = 8$ and $A = [I \mid H/2]$, where $H$ is the $4 \times 4$ Sylvester Hadamard matrix with rows $(1,1,1,1)$, $(1,-1,1,-1)$, $(1,1,-1,-1)$, $(1,-1,-1,1)$. Let $x_1 = 1$, $x_6 = 2$ and all other entries zero, so $s = 2$ and $y = (2, -1, 1, -1)$, with $\|y\| = \sqrt 7 \approx 2.6458$. This is the first example of the [iterative hard thresholding](/iterative-hard-thresholding/) page.

Iteration 1 starts from $a = 0$. The proxy is $p = A^Ty = (2, -1, 1, -1, 0.5, 2.5, 0.5, 0.5)$. The $2s = 4$ largest entries are entry 6 (2.5), entry 1 (2) and two of the entries 2, 3, 4 (all of magnitude 1); the implementation takes 2 and 3 by the lower index rule. So $T = \{1, 2, 3, 6\}$. These four columns are independent and contain the true support, so the least squares fit is exact: $b_1 = 1$, $b_6 = 2$, and $b_2 = b_3 = 0$. Pruning keeps entries 1 and 6, and $a = x$ with residual 0. Any choice among the tied entries gives the same result.

On the same data, iterative hard thresholding finds the right support in its first step but then only halves the error per step, because it takes a gradient step instead of the least squares fit. In a run on 20 random $32 \times 64$ Gaussian matrices with entries of variance $1/m$, CoSaMP recovered every $s$-sparse test vector for $s = 2, 3, 4, 5$, in 1 to 3 iterations. This is a measurement.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). With $\delta = \delta_{4s} < 1$, $d = x - a$ and $c = \delta/(1 - \delta)$, one iteration satisfies four bounds:

1. Identification: the part of $d$ missed by $\Omega$ is small, $\|d_{\Omega^c}\| \le \frac{2\delta}{1 - \delta}\|d\| + \frac{2\sqrt{1 + \delta}}{1 - \delta}\|e\|$. The proof compares $p$ on the support of $d$ and on $\Omega$, and uses that $A_U^TA_V$ has norm at most $\delta$ for disjoint sets $U$, $V$.
2. Merge: $\|x_{T^c}\| \le \|d_{\Omega^c}\|$, because $a$ vanishes off $T$.
3. Least squares: $\|x - b\| \le \sqrt{1 + c^2}\,\|x_{T^c}\| + \|e\|/\sqrt{1 - \delta}$.
4. Prune: $\|x - H_s(b)\| \le 2\|x - b\|$, because $H_s(b)$ is the best $s$-sparse approximation of $b$.

Together, $\|x - a'\| \le \rho\|x - a\| + \tau\|e\|$ with $\rho = 4\delta\sqrt{1 + c^2}/(1 - \delta)$. At $\delta = 0.1$ this is $\rho \approx 0.447$ and $\tau \approx 6.80$, so the error falls geometrically to about $12.3\|e\|$. The factor is below 1 for $\delta$ up to about 0.195. Needell and Tropp state the invariant $\|x - a^{k+1}\| \le 0.5\|x - a^k\| + 10\nu$ under $\delta_{4s} \le 0.1$, with the unrecoverable energy $\nu$, which also covers signals that are only close to sparse.

## Complexity

One iteration costs a product with $A$ and one with $A^T$, which is $O(mn)$ for a dense matrix, a selection of the $2s$ largest entries in $O(n)$, and a least squares problem with $m$ rows and at most $3s$ columns. A direct solve by [QR decomposition](/qr-decomposition/) or an SVD costs $O(ms^2)$. So $K$ iterations cost $O(K(mn + ms^2))$, and the extra memory is $O(ms + n)$ for $A_T$ and the vectors. With a fast operator and an iterative least squares solver, an iteration costs a fixed number of products with $A$ and $A^T$. Under $\delta_{4s} \le 0.1$, reaching error $\varepsilon\|x\|$ plus the noise term takes $O(\log(1/\varepsilon))$ iterations by the contraction factor.

## Properties

- The guarantee is uniform: one matrix with small $\delta_{4s}$ works for every $s$-sparse $x$, and the error is linear in the noise and in the tail of $x$.
- In the noiseless case, once the true support lies inside $T$, the least squares step gives $x$ exactly. So on easy instances CoSaMP stops after a finite number of iterations, unlike [iterative hard thresholding](/iterative-hard-thresholding/) and ISTA.
- The iterate is always $s$-sparse. Entries can enter and leave the support in every iteration.
- It is not scale sensitive in the way IHT is: if $A$ is multiplied by a constant $c \ne 0$, every iterate is divided by $c$ and the residuals stay the same, because the selections in lines L4 and L7 depend only on the order of magnitudes and line L6 is an exact fit.
- The condition $\delta_{4s} \le 0.1$ is stronger than the conditions known for $\ell_1$ minimization, such as $\delta_{2s} < 1/\sqrt 2$ for [basis pursuit](/basis-pursuit/).

## Variants and improvements

- Subspace pursuit (Dai and Milenkovic 2009) adds only $s$ candidates, solves least squares on the $2s$ columns, prunes to $s$ and then solves least squares again on the final support. It has a guarantee of the same kind.
- Hard thresholding pursuit (Foucart 2011) takes the support of a gradient step, as in IHT, and then solves least squares on it. It sits between IHT and CoSaMP.
- A final debiasing step, a least squares solve on the returned support, improves the result when the loop stops early.
- The same steps work for other structured sparsity models (block sparsity, tree sparsity in wavelets) if lines L4 and L7 are replaced by the best approximation in the model.
- Foucart reports better restricted isometry conditions for CoSaMP than $\delta_{4s} \le 0.1$ with a refined analysis; see the book of Foucart and Rauhut.

## When to use it

Use CoSaMP when the sparsity level is known, the matrix satisfies a restricted isometry property with room to spare (random Gaussian, Bernoulli or partial Fourier matrices with enough rows), and a solution with the exact sparsity is wanted. It usually needs fewer iterations than [iterative hard thresholding](/iterative-hard-thresholding/), at the cost of a least squares problem per iteration. When $s$ is not known, $\ell_1$ methods such as [basis pursuit](/basis-pursuit/) are easier to set up. When $s$ is very small, [orthogonal matching pursuit](/orthogonal-matching-pursuit/) is simpler and needs exactly $s$ steps.

## Pitfalls

- The merged set has up to $3s$ columns, and the least squares problem needs $3s \le m$ and independent columns. With a coherent matrix or too large an $s$, $A_T$ can be rank deficient. Use a pseudoinverse or a QR solver with column pivoting, not the normal equations.
- The sparsity level is an input. If the true signal has more than $s$ large entries, the result is the best fit with $s$ entries, not the signal.
- The iteration is not monotone in the residual in general. Keep the best iterate seen, or stop when the residual stops decreasing.
- On a coherent matrix the identification step can miss a true column again and again. The theorem needs a small $\delta_{4s}$; a small coherence alone is not enough for large $s$.
- Ties in the selection of lines L4 and L7 make runs depend on the tie rule. Fix it.

## Implementations

## History

Greedy pursuits with one column per step go back to matching pursuit (Mallat and Zhang 1993) and [orthogonal matching pursuit](/orthogonal-matching-pursuit/). Needell and Tropp posted CoSaMP in 2008 and published it in 2009. It was one of the first greedy methods with a uniform guarantee as strong as that of $\ell_1$ minimization up to constants: optimal error bounds for noisy and approximately sparse signals under a restricted isometry condition, and a cost bound. Dai and Milenkovic proposed subspace pursuit independently at the same time. Later work by Foucart and others improved the restricted isometry constants for CoSaMP, IHT and related methods.

## References
