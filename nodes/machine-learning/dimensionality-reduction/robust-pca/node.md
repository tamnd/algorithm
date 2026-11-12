---
tag: 4W6RMP
kind: algorithm
slug: robust-pca
name: Robust PCA
aliases:
- principal component pursuit
- low-rank plus sparse decomposition
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Split a data matrix into a low-rank part and a sparse part of gross errors by minimizing the nuclear norm plus lambda times the l1 norm, solved with an augmented Lagrangian method."
model: real-ram
complexity:
  vars: {m: the number of rows n_1, n: the number of columns n_2, T: the number of iterations}
  time: {worst: "O(T m n min(m, n))", per_step: "O(m n min(m, n))"}
  space: {extra: "O(m n)"}
properties: {deterministic: true, exact: false, iterative: true, online: false, recursive: false}
history:
  year: 2011
  people: [Emmanuel J. Candès, Xiaodong Li, Yi Ma, John Wright]
  note: "Candès, Li, Ma and Wright proved that principal component pursuit recovers a low-rank matrix from sparse gross errors. Chandrasekaran et al. gave related deterministic conditions. Lin, Chen and Ma gave the augmented Lagrangian solver."
prereqs: [principal-component-analysis, singular-value-decomposition, augmented-lagrangian-method]
see_also: [admm, proximal-operator, compressed-sensing, lasso-regression, sparse-pca, reconstruction-error, factor-analysis, semidefinite-programming]
sources:
  - paper: doi:10.1145/1970392.1970395
    title: Emmanuel J. Candès, Xiaodong Li, Yi Ma and John Wright, Robust principal component analysis?, Journal of the ACM 58(3), Article 11, 2011
    locator: Section 1.3 (principal component pursuit), the incoherence conditions (1.2) and (1.3), Theorem 1.1 (exact recovery with lambda = 1/sqrt(n_(1)) for rank up to a constant times n_(2) / (mu log^2 n_(1)) and a random support of size up to a constant times n_1 n_2), Section 4 (experiments, including video background and face images) and Section 5 (the ALM algorithm)
  - paper: "Zhouchen Lin, Minming Chen and Yi Ma, The augmented Lagrange multiplier method for exact recovery of corrupted low-rank matrices, arXiv:1009.5055, 2010"
    title: Lin, Chen and Ma 2010
    locator: "Section 2.3, equation (10) (J(Y) = max(||Y||_2, ||Y||_inf / lambda)), Section 3.1, Algorithm 5 (inexact ALM) and Theorems 2 and 3 (convergence when the sum of 1/mu_k diverges), and Section 4 (mu_0 = 1.25/||D||_2, rho = 1.6, tolerance 1e-7)"
  - paper: doi:10.1137/090761793
    title: Venkat Chandrasekaran, Sujay Sanghavi, Pablo A. Parrilo and Alan S. Willsky, Rank-sparsity incoherence for matrix decomposition, SIAM Journal on Optimization 21(2), 572-596, 2011
    locator: deterministic conditions for the unique recovery of a low-rank plus sparse decomposition by the same convex program
  - paper: doi:10.1137/080738970
    title: Jian-Feng Cai, Emmanuel J. Candès and Zuowei Shen, A singular value thresholding algorithm for matrix completion, SIAM Journal on Optimization 20(4), 1956-1982, 2010
    locator: Theorem 2.1, singular value thresholding is the proximal operator of the nuclear norm
---

Robust PCA splits a data matrix $M$ into a low-rank matrix $L$ and a sparse matrix $S$, so that $M = L + S$. The low-rank part is the structure that ordinary [PCA](/principal-component-analysis/) looks for, and the sparse part holds a few entries with gross errors of any size, which would ruin ordinary PCA. Candès, Li, Ma and Wright (2011) showed that the convex program called principal component pursuit (PCP), $\min \|L\|_* + \lambda \|S\|_1$ subject to $L + S = M$ with $\lambda = 1/\sqrt{\max(n_1, n_2)}$, recovers $L$ and $S$ exactly under broad conditions. This page solves PCP with the inexact augmented Lagrange multiplier method of Lin, Chen and Ma (2010), which alternates singular value thresholding for $L$, soft thresholding for $S$, and a multiplier update.

## In plain words

PCA fits the data with a few directions, using least squares. One very wrong value, such as a broken pixel or a typing error, can pull these directions far away, because least squares pays a lot for a large error.

Robust PCA assumes the data are a clean low-rank table plus a few corrupted cells. The corrupted cells can have any value, but there are few of them, and their positions are unknown. The method looks for the "simplest" split: the low-rank part should have small singular values in total, and the error part should have small entries in total. Both measures are convex, so a computer can find the best split reliably. In a video from a fixed camera, the low-rank part is the background, and the sparse part is the moving people.

## The problem

**Input.** An $n_1 \times n_2$ matrix $M$ and a weight $\lambda > 0$, by default $\lambda = 1/\sqrt{\max(n_1, n_2)}$.

**Output.** Matrices $L$ and $S$ that solve principal component pursuit,

$$\min_{L, S}\; \|L\|_* + \lambda \|S\|_1 \quad \text{subject to} \quad L + S = M,$$

where the nuclear norm $\|L\|_*$ is the sum of the singular values of $L$, and $\|S\|_1 = \sum_{ij}|S_{ij}|$. The nuclear norm is the convex surrogate for the rank, and the $\ell_1$ norm the convex surrogate for the number of nonzero entries, as in [compressed sensing](/compressed-sensing/). The principal directions of the data are then the singular vectors of $L$.

## The algorithm

The [augmented Lagrangian](/augmented-lagrangian-method/) is $\mathcal{L}(L, S, Y, \mu) = \|L\|_* + \lambda\|S\|_1 + \langle Y, M - L - S\rangle + \frac{\mu}{2}\|M - L - S\|_F^2$. The inexact method minimizes it once in $L$, once in $S$, and then updates the multiplier $Y$. Both minimizations have closed forms, the [proximal operators](/proximal-operator/) of the two norms:

- $\operatorname{svt}_\tau(W) = U \operatorname{diag}(\max(\sigma - \tau, 0)) V^T$ for the SVD $W = U \operatorname{diag}(\sigma) V^T$, singular value thresholding;
- $\operatorname{shrink}_\tau(W)_{ij} = \operatorname{sign}(W_{ij}) \max(|W_{ij}| - \tau, 0)$, soft thresholding.

```pseudo id=main
ROBUST-PCA(M, λ, ρ, tol)                       ▷ inexact ALM, Lin, Chen and Ma, Algorithm 5
L1  Y ← M / max(‖M‖₂, ‖M‖∞ / λ);  S ← 0;  μ ← 1.25 / ‖M‖₂
L2  repeat
L3      L ← svt_{1/μ}(M − S + Y/μ)
L4      S ← shrink_{λ/μ}(M − L + Y/μ)
L5      Z ← M − L − S;  Y ← Y + μ Z
L6      μ ← min(ρ μ, μ̄)
L7  until ‖Z‖_F ≤ tol ‖M‖_F
L8  return L, S
```

The start $Y_0 = M / J(M)$ with $J(M) = \max(\|M\|_2, \lambda^{-1}\|M\|_\infty)$ is the scaling of the dual problem (Lin, Chen and Ma, equation (10)). The implementation uses $\rho = 1.2$, the cap $\bar\mu = 10^7 \mu_0$ and $\mathrm{tol} = 10^{-7}$, and computes the SVD in L3 with the one-sided Jacobi method of Hestenes. This is also the alternating direction method of multipliers ([ADMM](/admm/)) for PCP, with an increasing penalty.

## Example

**The thresholding steps.** Soft thresholding with $\tau = 1$ maps the entries $(3, -0.5, -2)$ to $(2, 0, -1)$: small entries become 0, and large entries move toward 0 by $\tau$. Singular value thresholding does the same to the singular values, so it lowers the rank: a matrix with singular values $(5, 2, 0.5)$ and $\tau = 1$ becomes a matrix of rank 2 with singular values $(4, 1, 0)$.

**A planted instance.** Take $L_0 = U V^T$ with $20 \times 2$ Gaussian factors $U$ and $V$ (seed 0), so $L_0$ is $20 \times 20$ with rank 2, singular values $28.672$ and $13.818$, and entries at most $5.46$ in size. Corrupt 20 random entries (5%) by adding $\pm 10$. The matrix $M = L_0 + S_0$ has full rank, with the singular values $31.54, 21.65, 21.47, 16.46, \ldots$, so its spectrum no longer shows the rank. Here $\lambda = 1/\sqrt{20} = 0.2236$.

| iteration | rank of $L$ | nonzeros of $S$ | $\|M - L - S\|_F / \|M\|_F$ |
|---|---|---|---|
| 1 | 3 | 21 | 0.378 |
| 2 | 2 | 24 | 0.157 |
| 5 | 2 | 26 | 0.0150 |
| 10 | 2 | 25 | 0.00125 |
| 15 | 2 | 20 | 1.04e-4 |
| 20 | 2 | 20 | 6.77e-6 |
| 29 | 2 | 20 | 3.17e-8 |

The method stops after 29 iterations. The relative errors are $\|L - L_0\|_F / \|L_0\|_F = 7.5 \cdot 10^{-8}$ and $\|S - S_0\|_F / \|S_0\|_F = 3.7 \cdot 10^{-8}$, and the support of $S$ is exactly the 20 corrupted cells. For comparison, the best rank-2 approximation of $M$ by the plain SVD has the relative error $0.84$: ordinary PCA is far off on the same data.

## Correctness

There are two separate questions: does the algorithm solve PCP, and does PCP give the true split?

**The algorithm solves PCP.** The proofs file shows that L3 and L4 minimize the augmented Lagrangian exactly in $L$ and in $S$ (by the proximal formulas above). After each iteration, $Y \in \lambda\, \partial\|S\|_1$ holds exactly: every entry of $Y$ is in $[-\lambda, \lambda]$, and equals $\lambda \operatorname{sign}(S_{ij})$ where $S_{ij} \ne 0$. A matrix close to $Y$ is in $\partial\|L\|_*$. A pair $(L, S)$ with $L + S = M$ and one $Y$ in both subdifferentials is optimal, so every limit of the iteration with bounded $\mu$ is optimal. Lin, Chen and Ma (Theorem 2) prove that the iteration converges when $\mu_k$ is nondecreasing and $\sum_k 1/\mu_k = \infty$, which holds with the cap $\bar\mu$. Their Theorem 3 shows that the condition is needed.

**PCP finds the true split.** Write $n_{(1)} = \max(n_1, n_2)$ and $n_{(2)} = \min(n_1, n_2)$. Let $L_0 = U \Sigma V^T$ have rank $r$ and satisfy the incoherence conditions with a parameter $\mu$:

$$\max_i \|U^T e_i\|^2 \le \frac{\mu r}{n_1}, \quad \max_i \|V^T e_i\|^2 \le \frac{\mu r}{n_2}, \quad \|U V^T\|_\infty \le \sqrt{\frac{\mu r}{n_1 n_2}},$$

so its singular vectors are spread out and $L_0$ is not itself sparse. Let the support of $S_0$ be uniformly random with $m$ entries; the values on the support can be arbitrary. Theorem 1.1 of Candès et al. states that there are constants $\rho_r, \rho_s > 0$ such that if $r \le \rho_r\, n_{(2)}\, \mu^{-1} (\log n_{(1)})^{-2}$ and $m \le \rho_s n_1 n_2$, then PCP with $\lambda = 1/\sqrt{n_{(1)}}$ returns exactly $(L_0, S_0)$, with probability at least $1 - c\, n_{(1)}^{-10}$. So a rank almost linear in the dimension and a constant fraction of corrupted entries can be handled, with no tuning of $\lambda$. Chandrasekaran et al. (2011) give deterministic conditions in terms of rank-sparsity incoherence.

## Complexity

In the real RAM, each iteration costs one SVD of an $n_1 \times n_2$ matrix in L3, $O(n_1 n_2 \min(n_1, n_2))$ for a dense method, plus $O(n_1 n_2)$ for L4 and L5. In practice $T$ is a few tens of iterations; in the example $T = 29$. So the total is $O(T n_1 n_2 \min(n_1, n_2))$ time and $O(n_1 n_2)$ memory. Only the singular values above $1/\mu$ are needed in L3, and the rank of $L$ stays small, so large-scale codes compute a partial SVD (Lanczos, or [randomized](/randomized-pca/)) and predict the number of singular values to compute; this gives about $O(T n_1 n_2 r)$.

## Properties

- **Convex.** PCP has no bad local minima; every method that solves it finds the same optimum value.
- **Deterministic.** The method has no random choices.
- **Exact recovery.** Under the conditions above the planted split is the unique solution, without knowing the rank or the support.
- **Parameter-free in theory.** The default $\lambda = 1/\sqrt{n_{(1)}}$ works for the whole range of the theorem.
- **Not online.** Each iteration needs the whole matrix and an SVD.

## Variants and improvements

- **Exact ALM** (Algorithm 4 of Lin, Chen and Ma) minimizes the augmented Lagrangian fully in $(L, S)$ before each multiplier update, with a faster proven rate but more SVDs.
- **Accelerated proximal gradient** and the earlier iterative thresholding solve a penalized version; the inexact ALM was reported as several times faster.
- **Stable PCP** (Zhou et al. 2010) allows dense small noise: $\|M - L - S\|_F \le \delta$.
- **Missing entries.** PCP with observations only on a set $\Omega$ handles corruption and matrix completion together.
- **Outlier pursuit** replaces $\|S\|_1$ by the sum of the column norms, for data where whole points (columns) are corrupted.
- **Nonconvex methods** fix the rank and alternate projections or a gradient method on a factorization $L = A B^T$, which is faster for large matrices, at the cost of a known rank and local analysis.
- **Robust covariance estimators** such as the minimum covariance determinant handle outlying points instead of outlying entries.

## When to use it

Use robust PCA when a few entries of the data are grossly wrong and their positions are unknown: background subtraction in video from a fixed camera, removal of shadows and specular highlights from face images, sensor faults, and corrupted rankings or measurements. The low-rank part must be incoherent (spread over many entries), and the errors must be sparse and spread out. When the noise is small and dense everywhere, ordinary PCA or [probabilistic PCA](/probabilistic-pca/) is better; when whole points are outliers, use outlier pursuit or a robust covariance.

## Pitfalls

- **Too fast growth of $\mu$.** With $\mu_{k+1} = \rho\mu_k$ and no cap, $\sum 1/\mu_k$ is finite and the limit can be feasible but not optimal (Theorem 3 of Lin, Chen and Ma). On the example, $\rho = 1.6$ and $\rho = 1.5$ stop with $\|L - L_0\|_F/\|L_0\|_F$ about $5 \cdot 10^{-3}$ and $9 \cdot 10^{-4}$ and $\|Y\|_2 \approx 1.08$, a sign that $Y$ is not a dual certificate; $\rho = 1.2$ reaches $10^{-7}$. Check $\|Y\|_2 \approx 1$ at the end.
- **The stopping test checks only feasibility.** $\|M - L - S\|_F$ small does not prove optimality; the dual condition $\|Y\|_2 \le 1$ is the other half.
- **Coherent low-rank part.** If $L_0$ is itself sparse, for example a single nonzero row, it cannot be told apart from $S_0$, and no method can recover it.
- **Errors in a pattern.** The theorem needs a random support. Errors that fill whole columns or a block can look low-rank and are absorbed into $L$.
- **Scaling of $\lambda$.** The value $1/\sqrt{n_{(1)}}$ assumes comparable scales of rows and columns. With very different units, standardize first or tune $\lambda$.
- **Cost.** A full SVD per iteration is the main cost; for large matrices use a partial SVD.

## Implementations

## History

Robust versions of PCA go back to the 1970s and 1980s, with robust covariance estimators, M-estimators and projection pursuit, which handle outlying points. The low-rank plus sparse model with arbitrary entrywise corruption, and its convex relaxation, appeared in 2009 in two independent lines of work: Wright, Ganesh, Rao, Peng and Ma, and Candès, Li, Ma and Wright on one side, and Chandrasekaran, Sanghavi, Parrilo and Willsky on the other. Candès et al. named the program principal component pursuit and proved exact recovery with the universal $\lambda = 1/\sqrt{n_{(1)}}$, published in the Journal of the ACM in 2011. Lin, Chen and Ma (2009, arXiv 2010) gave the exact and inexact ALM methods, which made PCP practical; this is the solver used in the experiments of Candès et al.

## References
