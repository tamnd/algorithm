---
tag: 5MH4MT
kind: problem
slug: sparse-signal-recovery
name: Sparse signal recovery
aliases:
- sparse reconstruction
area: graphics-and-signals/signal-processing
level: advanced
summary: Recover a sparse vector from fewer linear measurements than unknowns. NP-hard in general; easy for good matrices.
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns, s: the number of nonzero entries}
  time: {worst: O(n^s m s^2)}
prereqs: [least-squares-problem, np-hard]
see_also: [basis-pursuit, orthogonal-matching-pursuit, iterative-shrinkage-thresholding, compressed-sensing, restricted-isometry-property, lasso-regression, exact-cover-by-3-sets, sparse-fourier-transform]
sources:
  - paper: doi:10.1137/S0097539792240406
    title: B. K. Natarajan, Sparse approximate solutions to linear systems, SIAM Journal on Computing 24(2), 1995
    locator: pages 227 to 234 (the problem of the sparsest x with a small residual is NP-hard, and a bound for the greedy method)
  - paper: doi:10.1073/pnas.0437847100
    title: David L. Donoho and Michael Elad, Optimally sparse representation in general (nonorthogonal) dictionaries via l1 minimization, Proceedings of the National Academy of Sciences 100(5), 2003
    locator: pages 2197 to 2202 (the spark, uniqueness when the sparsity is below half the spark, and the coherence bound)
  - paper: doi:10.1109/TIT.2005.858979
    title: Emmanuel J. Candès and Terence Tao, Decoding by linear programming, IEEE Transactions on Information Theory 51(12), 2005
    locator: pages 4203 to 4215 (recovery of a sparse error vector by linear programming, and the restricted isometry constants)
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhäuser, 2013
    locator: Chapter 2 (sparse solutions, the minimal number of measurements and NP-hardness), Chapter 3 (basic algorithms) and Chapter 10 (Gelfand widths and lower bounds)
---

Sparse signal recovery is the problem of finding a vector $x \in \mathbb R^n$ with at most $s$ nonzero entries from $m < n$ linear measurements $y = Ax$, or from measurements with noise. Without the sparsity, the system has infinitely many solutions; with it, the solution is unique as soon as every $2s$ columns of $A$ are linearly independent. Finding the sparsest solution is NP-hard for a general matrix $A$, but for matrices with incoherent columns or the [restricted isometry property](/restricted-isometry-property/), fast methods such as [basis pursuit](/basis-pursuit/) and [orthogonal matching pursuit](/orthogonal-matching-pursuit/) find it exactly. This page is about the problem; the plan of measuring with random matrices so that the problem becomes easy is [compressed sensing](/compressed-sensing/).

## In plain words

You want to know many numbers, but you can only measure a few mixtures of them. In general that is hopeless: too many different answers fit the same measurements. But suppose you know that almost all of the numbers are zero, and only a few are not. Then there may be just one answer that fits and has so few nonzero numbers.

The difficulty is to find it. Trying every possible group of nonzero places takes far too long when the list is long, and no fast method works for every way of mixing. For good mixings, which random ones usually are, fast methods find the answer exactly. Many signals and images are nearly of this kind once you write them in a good basis, which is why the problem matters in practice.

## Definition

**Instance.** A matrix $A \in \mathbb R^{m \times n}$ with $m < n$, a vector $y \in \mathbb R^m$, and a sparsity level $s$. The support of $x$ is $\operatorname{supp}(x) = \{j : x_j \ne 0\}$, and $\|x\|_0 = |\operatorname{supp}(x)|$ counts its nonzero entries. A vector is $s$-sparse if $\|x\|_0 \le s$.

**Noiseless problem.**

$$(P_0) \qquad \text{minimize } \|x\|_0 \quad \text{subject to } Ax = y.$$

The decision version asks whether some $x$ with $Ax = y$ and $\|x\|_0 \le s$ exists.

**Noisy problem.** For $y = Ax_0 + e$ with $\|e\|_2 \le \varepsilon$, minimize $\|x\|_0$ subject to $\|Ax - y\|_2 \le \varepsilon$. A method is *stable* if it returns $\hat x$ with $\|\hat x - x_0\|_2 \le C \varepsilon$ for every $s$-sparse $x_0$, with $C$ not depending on $x_0$.

**Spark.** $\operatorname{spark}(A)$ is the least number of columns of $A$ that are linearly dependent.

**Uniqueness theorem.** Every $s$-sparse $x_0$ is the unique $s$-sparse solution of $Ax = Ax_0$ if and only if $\operatorname{spark}(A) > 2s$.

*Proof.* If $x_0$ and $x_1 \ne x_0$ are both $s$-sparse with $Ax_0 = Ax_1$, then $z = x_0 - x_1 \ne 0$ is $2s$-sparse and $Az = 0$, so the columns on $\operatorname{supp}(z)$ are dependent and $\operatorname{spark}(A) \le 2s$. Conversely, if some $2s$ or fewer columns are dependent, there is $z \ne 0$ with $\|z\|_0 \le 2s$ and $Az = 0$. Split $\operatorname{supp}(z)$ into two parts of at most $s$ indices each, and let $u$ be $z$ on the first part and $v = u - z$, which is $-z$ on the second. Then $u \ne v$, both are $s$-sparse, and $Au = Av$. $\square$

So under $\operatorname{spark}(A) > 2s$, the $s$-sparse solution, if one exists, is also the unique solution of $(P_0)$.

## Variants

- **Sparse in a basis.** The signal is $f = \Psi c$ with $c$ sparse, for example in a wavelet basis, and the measurements are $y = \Phi f$. This is the problem with $A = \Phi \Psi$.
- **Compressible signals.** The vector is not exactly sparse but its sorted entries decay. The target is then an error bound in terms of $\sigma_s(x)_1 = \min_{\|z\|_0 \le s} \|x - z\|_1$, the error of the best $s$-term approximation.
- **Sparsity-constrained least squares.** Minimize $\|Ax - y\|_2$ subject to $\|x\|_0 \le s$. Natarajan's NP-hardness result is stated for this form.
- **Penalized form.** Minimize $\tfrac12\|Ax - y\|_2^2 + \lambda \|x\|_0$, and its convex relaxation with $\|x\|_1$, the [lasso](/lasso-regression/).
- **Support recovery.** Return only $\operatorname{supp}(x_0)$. Once the support is known, the values follow by [least squares](/least-squares-problem/) on those columns.
- **Structured sparsity.** Nonzero entries come in blocks, in a tree (as for wavelet coefficients), or must be nonnegative.
- **Low rank.** The matrix analogue: recover a low-rank matrix from linear measurements. [Robust PCA](/robust-pca/) splits a matrix into a low-rank and a sparse part.
- **Fourier measurements.** If $A$ is the full discrete Fourier matrix and $x$ has few large frequencies, the [sparse Fourier transform](/sparse-fourier-transform/) finds them in time sublinear in $n$.

## Examples

**Unique and not unique.** Let

$$A = \begin{pmatrix} 1 & 1 & -1 & -1 \\ 1 & -1 & 1 & -1 \\ 1 & -1 & -1 & 1 \end{pmatrix},$$

whose columns point to the corners of a regular tetrahedron. Any three columns are independent, and the four columns sum to $0$, so $\operatorname{spark}(A) = 4$. For $s = 1$, $\operatorname{spark}(A) > 2$, and $y = (1, 1, 1)$ has the unique $1$-sparse solution $x = (1, 0, 0, 0)$. For $s = 2$ uniqueness fails: $y = (2, 0, 0)$ is $A(1, 1, 0, 0)$ and also $A(0, 0, -1, -1)$.

**Exact cover.** Take the ground set $\{1, \ldots, 6\}$ and the sets $\{1, 2, 3\}$, $\{3, 4, 5\}$, $\{4, 5, 6\}$. Let column $j$ of $A \in \{0, 1\}^{6 \times 3}$ be the indicator of set $j$ and let $y = (1, 1, 1, 1, 1, 1)$. Then $x = (1, 0, 1)$ is a $2$-sparse solution, and it corresponds to the exact cover by the first and third sets. The reduction below shows that this works in general.

**A natural instance.** A piecewise constant signal of length $n = 2^J$ with $k$ jumps has at most $kJ + 1$ nonzero Haar coefficients (see the [Haar wavelet](/haar-wavelet/)). So it is sparse in the Haar basis, and the variant with $A = \Phi\Psi$ applies.

## Known algorithms

| method | idea | guarantee for exact recovery | cost |
|---|---|---|---|
| search over supports | least squares on every set of $s$ columns | exact whenever $\operatorname{spark}(A) > 2s$ | $\binom ns$ small least squares problems |
| [basis pursuit](/basis-pursuit/) | minimize $\|x\|_1$ subject to $Ax = y$, a linear program | under the null space property, for example when $\delta_{2s} < \sqrt 2 - 1$ or $\mu < 1/(2s - 1)$ | polynomial, by the simplex or interior-point method |
| [orthogonal matching pursuit](/orthogonal-matching-pursuit/) | add the column most correlated with the residual, then refit | when $\mu < 1/(2s - 1)$, or under the exact recovery condition | $s$ steps, each $O(mn)$ plus a least squares update |
| [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/) | proximal gradient steps on the lasso objective | converges to the lasso solution, which is close to $x_0$ under the restricted isometry property and a suitable $\lambda$ | $O(mn)$ per iteration |
| iterative hard thresholding, CoSaMP | gradient step, then keep the $s$ largest entries | stable under a bound on $\delta_{3s}$ or $\delta_{4s}$ | $O(mn)$ per iteration |

Here $\mu$ is the largest absolute inner product of two distinct normalized columns, the mutual coherence, and $\delta_k$ is the restricted isometry constant of order $k$. The guarantees in the table are sufficient conditions, and neither of basis pursuit and OMP dominates the other: there are matrices and vectors where each one succeeds and the other fails.

## Bounds

- **NP-hardness.** The decision version is NP-complete, by the reduction from exact cover below, and the sparsity-constrained least squares form is NP-hard (Natarajan 1995). So no polynomial algorithm solves every instance unless P = NP. The fast methods above work for restricted classes of $A$.
- **Measurements needed.** If $m < 2s$, every $2s$ columns are dependent, so some two $s$-sparse vectors have the same measurements. So $m \ge 2s$ is necessary for uniqueness. It is also enough: with distinct numbers $t_1, \ldots, t_n$ and $A_{ij} = t_j^{\,i}$ for $0 \le i < 2s$, every $2s$ columns form a nonsingular Vandermonde matrix. Such matrices are very badly conditioned, so recovery from them is not stable.
- **Stable recovery.** A method that is stable for compressible vectors needs $m \ge c\, s \log(en/s)$ measurements for a constant $c$, by a bound on the Gelfand widths of the $\ell_1$ ball (Foucart and Rauhut 2013, Chapter 10). Random Gaussian matrices with $m = O(s \log(n/s))$ achieve this with high probability, through the [restricted isometry property](/restricted-isometry-property/).
- **Exhaustive search.** Testing all supports of size $s$ costs $\binom ns$ least squares solves, which is at most $n^s$ and so polynomial only for a fixed $s$.

## Reductions

**From exact cover by 3-sets.** An instance of [exact cover by 3-sets](/exact-cover-by-3-sets/) has a ground set of size $3q$ and a family of $n$ subsets of size $3$. Let column $j$ of the $3q \times n$ matrix $A$ be the indicator vector of subset $j$, let $y$ be the all-ones vector, and let $s = q$.

*If there is an exact cover*, put $x_j = 1$ on its $q$ sets and $0$ elsewhere. Each element is in exactly one chosen set, so $Ax = y$ and $\|x\|_0 = q$.

*If $Ax = y$ with $\|x\|_0 \le q$*, then each of the $3q$ rows of $y$ is nonzero, so each element lies in some set of $\operatorname{supp}(x)$. The at most $q$ sets of size $3$ cover $3q$ elements, so there are exactly $q$ of them and they are pairwise disjoint. Then each row of $Ax = y$ has exactly one term, $x_j = 1$, and the sets form an exact cover.

The construction takes polynomial time, so the decision version of $(P_0)$ is NP-hard. It is in NP, since a support and the solution of a linear system on it form a certificate, checked by exact rational arithmetic.

**To linear programming.** Replacing $\|x\|_0$ by $\|x\|_1$ gives basis pursuit, which is a [linear program](/linear-programming-problem/). This is a [convex relaxation](/convex-relaxation/), not an equivalence: the two problems have the same solution exactly when $A$ has the null space property of order $s$.

**To the lasso.** The noisy problem relaxed in the same way, with a penalty in place of the constraint, is the lasso, which [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/) solves.

## Applications

- **Medical imaging.** Magnetic resonance scanners measure Fourier coefficients of an image. Images are sparse in a wavelet basis, so fewer measurements and a shorter scan are enough.
- **Error correction.** Candès and Tao (2005) decode a real codeword $y = Bf + e$ with a sparse error $e$ by applying a matrix that kills $B$, which leaves a sparse recovery problem for $e$.
- **Denoising and inverse problems.** [Signal reconstruction](/signal-reconstruction/), [image deblurring](/image-deblurring/) and [super-resolution](/super-resolution/) use sparsity in a wavelet or gradient domain as the prior.
- **Statistics.** Variable selection in regression with more features than samples is support recovery.
- **Sensing hardware.** Single-pixel cameras, radar and spectrum sensing measure random mixtures on purpose, the plan of [compressed sensing](/compressed-sensing/).

## References
