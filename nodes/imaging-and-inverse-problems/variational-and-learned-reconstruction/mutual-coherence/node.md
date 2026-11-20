---
tag: 1VF7YK
kind: definition
slug: mutual-coherence
name: Mutual coherence
aliases:
- coherence of a dictionary
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: core
summary: The largest absolute normalized inner product between two distinct columns of a sensing matrix, which bounds the sparsity that recovery can guarantee.
prereqs: [sparse-signal-recovery]
see_also: [restricted-isometry-property, null-space-property, welch-bound, gershgorin-circle-theorem, basis-pursuit, orthogonal-matching-pursuit, k-svd, compressed-sensing]
sources:
  - paper: doi:10.1109/18.959265
    title: David L. Donoho and Xiaoming Huo, Uncertainty principles and ideal atomic decomposition, IEEE Transactions on Information Theory 47(7), 2001
    locator: pages 2845 to 2862 (the pair of orthonormal bases, the uncertainty principle and exact recovery by l1 minimization)
  - paper: doi:10.1073/pnas.0437847100
    title: David L. Donoho and Michael Elad, Optimally sparse representation in general (nonorthogonal) dictionaries via l1 minimization, Proceedings of the National Academy of Sciences 100(5), 2003
    locator: pages 2197 to 2202 (the spark, the bound of the spark by the coherence, and recovery for s < (1 + 1/mu)/2)
  - paper: doi:10.1109/TIT.2004.834793
    title: Joel A. Tropp, Greed is good, algorithmic results for sparse approximation, IEEE Transactions on Information Theory 50(10), 2004
    locator: pages 2231 to 2242 (the exact recovery condition, and recovery by OMP and basis pursuit for s < (1 + 1/mu)/2)
  - paper: doi:10.1109/TIT.1974.1055219
    title: Lloyd R. Welch, Lower bounds on the maximum cross correlation of signals, IEEE Transactions on Information Theory 20(3), 1974
    locator: pages 397 to 399
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhauser, 2013
    locator: the chapter on coherence
---

The mutual coherence of a matrix is the largest absolute inner product between two of its distinct normalized columns. It is the simplest number that measures how well a matrix can separate sparse vectors: when no two columns are close, a sparse combination of columns determines its coefficients. It is cheap to compute, in contrast with the [restricted isometry constants](/restricted-isometry-property/) and the [null space property](/null-space-property/), which look at all sets of $s$ columns and are NP-hard to compute. The price is that the guarantees it gives are weaker: they apply only for sparsity of order $\sqrt m$, while restricted isometry gives sparsity of order $m$ up to a logarithm. Coherence is also the standard measure of quality for a learned dictionary, for example one from [K-SVD](/k-svd/).

## Definition

Let $A \in \mathbb{C}^{m \times n}$ have nonzero columns $a_1, \dots, a_n$. The mutual coherence of $A$ is

$$\mu(A) = \max_{i \ne j}\frac{|\langle a_i, a_j\rangle|}{\|a_i\|\,\|a_j\|}.$$

It does not change when a column is scaled by a nonzero number, so one can assume that the columns have norm 1, and then $\mu$ is the largest absolute entry off the diagonal of the Gram matrix $A^HA$. Always $0 \le \mu \le 1$. $\mu = 0$ means that the columns are orthogonal, which needs $n \le m$, and $\mu = 1$ means that two columns are parallel.

The direct computation takes $O(mn^2)$ time:

```pseudo id=main
COHERENCE(A)
L1  for j = 1 to n: c_j ← a_j / ‖a_j‖
L2  μ ← 0
L3  for i = 1 to n - 1
L4      for j = i + 1 to n
L5          μ ← max(μ, |⟨c_i, c_j⟩|)
L6  return μ
```

**Lower bound (Welch 1974).** For $n > m$ unit vectors in $\mathbb{C}^m$,

$$\mu \ge \sqrt{\frac{n - m}{m(n - 1)}}.$$

*Proof.* Let $G$ be the $n \times n$ Gram matrix. It has trace $n$ and rank at most $m$, so by the Cauchy-Schwarz inequality on its at most $m$ nonzero eigenvalues, $\|G\|_F^2 = \sum\lambda_i^2 \ge (\sum\lambda_i)^2/m = n^2/m$. The diagonal gives $n$ and each of the $n(n - 1)$ entries off the diagonal is at most $\mu^2$ in squared absolute value, so $n^2/m \le n + n(n - 1)\mu^2$. Solve for $\mu^2$. $\square$

Equality holds exactly for equiangular tight frames, where all $|\langle a_i, a_j\rangle|$ are equal and $AA^H = (n/m)I$. For $n = 2m$ the bound is about $1/\sqrt{2m}$. See the [Welch bound](/welch-bound/) page for the bound on sequences.

**What coherence guarantees.** Let the columns have norm 1 and let $\mu > 0$.

1. Every set of $s$ columns with $(s - 1)\mu < 1$ is linearly independent, and the restricted isometry constant satisfies $\delta_s \le (s - 1)\mu$. The Gram matrix of $s$ columns has diagonal 1 and off-diagonal entries of absolute value at most $\mu$, so by the [Gershgorin circle theorem](/gershgorin-circle-theorem/) its eigenvalues are in $[1 - (s - 1)\mu, 1 + (s - 1)\mu]$. For $s = 2$ this is an equality: $\delta_2 = \mu$.
2. The spark of $A$, the least number of linearly dependent columns, satisfies $\operatorname{spark}(A) \ge 1 + 1/\mu$. This follows from item 1.
3. If $Ax = y$ and $x$ has $s$ nonzero entries with $s < \tfrac12(1 + 1/\mu)$, then $x$ is the unique sparsest solution of $Az = y$ (Donoho and Elad 2003), and both [basis pursuit](/basis-pursuit/) and [orthogonal matching pursuit](/orthogonal-matching-pursuit/) find it (Donoho and Huo 2001 for a pair of orthonormal bases, Donoho and Elad 2003 and Gribonval and Nielsen 2003 for basis pursuit with more general dictionaries, Tropp 2004 for OMP and basis pursuit). With noise, the same condition with a stricter constant gives stable recovery.

The Welch bound makes $1/\mu$ at most about $\sqrt m$ when $n$ is a multiple of $m$, so item 3 never gives more than about $\sqrt m/2$ nonzeros. This limit is called the square root bottleneck. It is a limit of the coherence argument, not of the matrices: a random $m \times n$ Gaussian matrix has $\mu$ of order $\sqrt{\log n/m}$, so coherence gives $s$ of order $\sqrt{m/\log n}$, while the same matrix has the restricted isometry property for $s$ of order $m/\log(n/s)$.

## Examples and non-examples

**Identity and Hadamard.** In $\mathbb{R}^4$ let $A = [\,I \mid \tfrac12H\,]$ with the Sylvester Hadamard matrix

$$H = \begin{pmatrix}1 & 1 & 1 & 1\\ 1 & -1 & 1 & -1\\ 1 & 1 & -1 & -1\\ 1 & -1 & -1 & 1\end{pmatrix}.$$

The columns have norm 1. Two identity columns are orthogonal, and so are two Hadamard columns. An identity column $e_i$ and a Hadamard column meet with inner product $\pm\tfrac12$. So $\mu = \tfrac12$. The Welch bound for 8 vectors in $\mathbb{R}^4$ is $\sqrt{4/28} \approx 0.378$, so this matrix is not optimal. The coherence bound gives $\operatorname{spark} \ge 3$ and uniqueness for $s < 1.5$, that is $s = 1$. The true spark is 4: the first two Hadamard columns add up to $(1, 0, 1, 0) = e_1 + e_3$. For every power of two $m$ the matrix $[\,I \mid H/\sqrt m\,]$ has $\mu = 1/\sqrt m$, and the analogous pair of identity and unitary DFT has the same coherence; these are the pairs of bases of Donoho and Huo. The [compressed sensing](/compressed-sensing/) page uses the same construction.

**Regular simplex.** Three unit vectors in the plane at 120 degrees have $\mu = |\cos 120°| = \tfrac12$, which equals the Welch bound $\sqrt{1/4}$. More generally, the $m + 1$ vertices of a regular simplex centered at the origin in $\mathbb{R}^m$ give $\mu = 1/m$, which also equals the Welch bound. They form an equiangular tight frame.

**Repeated column.** A matrix with two parallel columns has $\mu = 1$, and the bounds above say nothing. Indeed $e_1$ and $e_2$ times the same column give the same measurement.

**Non-example of a good bound.** Coherence is a worst case over pairs. A matrix can have one bad pair of columns and still recover most sparse vectors; and a matrix with small coherence can still fail for some sets of $s$ columns with $s > \tfrac12(1 + 1/\mu)$, as the identity and Hadamard example shows at $s = 2$: the vectors $\tfrac12(h_1 + h_2)$ and $e_1 + e_3$ are two different 2-sparse solutions of the same measurement.

**Measurement.** For 20 random Gaussian matrices of size $64 \times 128$ (seeds 0 to 19 of Python's `random.Random`), the measured coherence was between 0.43 and 0.56, with mean 0.47. The Welch bound for this size is 0.089. So for these matrices the coherence bound guarantees recovery only for $s = 1$, while the asymptotic [Donoho-Tanner phase transition](/donoho-tanner-phase-transition/) for basis pursuit at $m/n = 1/2$ lies at about $0.386m$, that is near 25 nonzeros, for typical sparse vectors.

## Related definitions

- **Restricted isometry property.** The constant $\delta_s$ bounds the eigenvalues of all $s \times s$ Gram submatrices, not just the entries. $\delta_2 = \mu$ for unit columns, and $\delta_s \le (s - 1)\mu$.
- **Null space property.** The exact condition for basis pursuit to recover every $s$-sparse vector. Coherence below $1/(2s - 1)$ implies it. See [null space property](/null-space-property/).
- **Spark.** The least number of dependent columns. Every $s$-sparse vector is the unique sparsest solution if and only if $\operatorname{spark}(A) > 2s$. The spark is NP-hard to compute in general, and $1 + 1/\mu$ is a cheap lower bound.
- **Babel function or cumulative coherence.** $\mu_1(s) = \max_{|\Lambda| = s}\max_{j \notin \Lambda}\sum_{i \in \Lambda}|\langle a_i, a_j\rangle|$ (Tropp 2004). It is at most $s\mu$, and conditions in terms of it are sharper when a few pairs are much worse than the rest.
- **Coherence between two bases.** For orthonormal bases $\Phi$ and $\Psi$ of $\mathbb{C}^m$, $\max_{i,j}|\langle\phi_i, \psi_j\rangle|$ is the coherence of $[\,\Phi \mid \Psi\,]$. In compressed sensing the scaled version $\sqrt m\max|\langle\phi_i, \psi_j\rangle|$, between 1 and $\sqrt m$, sets how many random samples in $\Phi$ are needed to recover a signal sparse in $\Psi$.

## References
