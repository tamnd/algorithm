---
tag: N0B0GB
kind: problem
slug: matrix-completion
name: Low-rank matrix completion
aliases:
- matrix completion
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Recover a low-rank matrix from a small random subset of its entries, the model problem behind rating prediction.
prereqs: [singular-value-decomposition, rating-matrix]
see_also: [exact-matrix-completion-theorem, semidefinite-programming, convex-relaxation, compressed-sensing, restricted-isometry-property, alternating-least-squares, matrix-factorization-recommendation, probabilistic-matrix-factorization]
sources:
  - paper: doi:10.1007/s10208-009-9045-5
    title: Emmanuel J. Candès and Benjamin Recht, Exact matrix completion via convex optimization, Foundations of Computational Mathematics 9(6), 717-772, 2009
    locator: Abstract and Section 1 (the problem, the nuclear norm program, the assumptions A0 and A1, and the first bounds, of order n^(5/4) r log n for most matrices and n^(6/5) r log n when r <= n^(1/5))
  - url: https://www.jmlr.org/papers/volume12/recht11a/recht11a.pdf
    title: Benjamin Recht, A simpler approach to matrix completion, Journal of Machine Learning Research 12, 3413-3430, 2011
    locator: Section 1 (the problem, lowest rank completion is NP-hard, the nuclear norm as a semidefinite program) and Theorem 2 (the bound of order r (n1 + n2) log^2 n2)
  - paper: doi:10.1109/TIT.2010.2044061
    title: Emmanuel J. Candès and Terence Tao, The power of convex relaxation, near-optimal matrix completion, IEEE Transactions on Information Theory 56(5), 2053-2080, 2010
    locator: Section 1.1 (applications), Theorem 1.7 and Equation 1.21 (the lower bound of order mu0 n r log n for any method, in the Bernoulli model)
  - paper: doi:10.1137/110820361
    title: Nicolas Gillis and François Glineur, Low-rank matrix approximation with weights or missing data is NP-hard, SIAM Journal on Matrix Analysis and Applications 32(4), 1149-1165, 2011
    locator: Abstract and main result (the approximation problem with missing data is NP-hard, already for rank one)
---

Low-rank matrix completion asks for the missing entries of a matrix when only some entries are known and the whole matrix is known, or assumed, to have low rank. A table of ratings with one row per user and one column per item is the standard example: most entries are missing, and the hope is that a few hidden factors explain the ratings, so that the table is close to low rank. Without a rank bound the problem has no answer, since any values fit the missing entries. With a rank bound and an arbitrary pattern of known entries it is [NP-hard](/np-hard/). With random known entries and a spread-out matrix, the [exact matrix completion theorem](/exact-matrix-completion-theorem/) says that a convex program recovers the matrix exactly from about $r (n_1 + n_2) \log^2 n_2$ entries.

## In plain words

You have a big table with most cells empty. You believe the table is simple: every row is a mix of a few basic rows. Fill in the empty cells so that the table stays that simple. If the cells you see are scattered at random, and the table does not hide its content in a few rows or columns, a small fraction of the cells is enough to fill in the rest exactly. For real rating data the table is only close to simple and the cells you see are not random, so the filled-in values are estimates, and how good they are is measured, not proved.

## Definition

**Input.** Dimensions $n_1 \le n_2$, a set $\Omega \subseteq \{1, \dots, n_1\} \times \{1, \dots, n_2\}$ of $m$ observed positions, and the values $M_{ij}$ for $(i, j) \in \Omega$ of an unknown matrix $M$.

**Exact version.** Given a rank bound $r$, find a matrix $X$ of rank at most $r$ with $X_{ij} = M_{ij}$ for all $(i, j) \in \Omega$, or the matrix of least rank with that property:

$$\text{minimize } \operatorname{rank}(X) \quad \text{subject to } X_{ij} = M_{ij}, \ (i, j) \in \Omega .$$

The recovery question is whether the answer is unique and equal to $M$.

**Noisy version.** The observed values are $M_{ij} + \varepsilon_{ij}$. Find $X$ of rank at most $r$ that minimizes $\sum_{(i,j) \in \Omega} (X_{ij} - M_{ij} - \varepsilon_{ij})^2$, or a penalized form of it.

**Sampling model.** Most results assume that $\Omega$ is a uniformly random set of $m$ positions, or that each position is observed independently with probability $p = m / (n_1 n_2)$ (the Bernoulli model). Candès and Tao (2010, Section 1) note that results for one model carry over to the other with minor changes.

**Incoherence.** Write $M = U \Sigma V^*$ for its [singular value decomposition](/singular-value-decomposition/). The coherence of the column space is $\mu(U) = (n_1 / r) \max_i \lVert P_U e_i \rVert^2$, between 1 and $n_1 / r$, and the same for the row space (Recht 2011, Definition 1). Recovery from random entries needs low coherence, because a matrix such as $e_1 e_1^*$ is zero almost everywhere and cannot be found unless its one nonzero entry is observed.

## Variants

- **Noisy completion.** The observations have noise, and the aim is a small error rather than exact recovery.
- **Weighted low-rank approximation.** Each entry has a weight and the aim is a rank-$r$ matrix that minimizes the weighted squared error. Missing entries are entries of weight 0. This is the problem that Gillis and Glineur (2011) show NP-hard.
- **Completion from general linear measurements.** The known values are $\langle A_k, M \rangle$ for given matrices $A_k$, not single entries. Entries are the case $A_k = e_i e_j^*$. Gross (2011) treats measurements in any orthonormal basis of matrices.
- **One-class completion.** Only positive entries are observed, as with clicks and purchases, and the missing entries are a mix of unknown and negative. See [implicit feedback](/implicit-feedback/).
- **Completion with side information.** Features of the rows and columns are also known; [factorization machines](/factorization-machine/) are one model for this.

## Examples

A $2 \times 2$ matrix of rank 1 with entries $M_{11} = 2$, $M_{12} = 4$, $M_{21} = 3$ known and $M_{22}$ missing. Rank 1 means the rows are proportional. The first row is $(2, 4)$, so the second row is $(3, 6)$ and $M_{22} = 6$. Here three entries fix the fourth, and the rank bound is what makes the answer unique.

Remove instead $M_{12}$ and $M_{22}$, so that the whole second column is missing. Then $(2, t)$ and $(3, 1.5 t)$ have rank 1 for every $t$, and no method can recover the column. This is why random sampling needs about $n \log n$ entries at least: with fewer, some row or column is likely to have no observed entry at all (Candès and Tao 2010 call this a coupon collector effect).

## Known algorithms

- **Nuclear norm minimization.** Replace the rank by the nuclear norm $\lVert X \rVert_* = \sum_k \sigma_k(X)$, its [convex relaxation](/convex-relaxation/) (the best convex lower bound of the rank on matrices with all singular values at most 1, Recht 2011, Section 1), and solve the resulting [semidefinite program](/semidefinite-programming/) (Recht 2011, Section 1). Under incoherence and uniform sampling this recovers $M$ exactly with high probability; see the [exact matrix completion theorem](/exact-matrix-completion-theorem/). General [interior-point methods](/interior-point-method/) are too slow for large matrices, so first-order methods such as singular value thresholding and soft-impute, which apply a shrinkage step to the singular values, are used instead.
- **Factored nonconvex methods.** Write $X = W H^\top$ with $W$ of size $n_1 \times r$ and $H$ of size $n_2 \times r$, and minimize the squared error on $\Omega$ plus a penalty, by [alternating least squares](/alternating-least-squares/) or by [stochastic gradient descent](/stochastic-gradient-descent/). This is [matrix factorization for recommendation](/matrix-factorization-recommendation/), and [probabilistic matrix factorization](/probabilistic-matrix-factorization/) gives it a Bayesian reading. The objective is not convex, so these methods may stop at a local minimum.
- **Spectral methods.** Take the top $r$ singular vectors of the rescaled matrix of observed entries, with zeros elsewhere, and refine them. Keshavan, Montanari and Oh (2010) analyze an algorithm of this kind.

## Bounds

- **Upper bound for nuclear norm minimization.** Recht (2011, Theorem 2): under coherence bounds $\mu_0$ and $\mu_1$, $m \ge 32 \max\{\mu_1^2, \mu_0\} r (n_1 + n_2) \beta \log^2(2 n_2)$ uniformly random entries suffice for exact recovery with probability at least $1 - 6 \log(n_2) (n_1 + n_2)^{2 - 2\beta} - n_2^{2 - 2\beta^{1/2}}$. Earlier bounds were of order $n^{5/4} r \log n$, or $n^{6/5} r \log n$ when $r \le n^{1/5}$, for most matrices (Candès and Recht 2009) and $\mu^2 n r \log^6 n$ under a stronger incoherence condition (Candès and Tao 2010, Theorem 1.2).
- **Lower bound for any method.** Candès and Tao (2010, Theorem 1.7 and Equation 1.21): in the Bernoulli model, recovering every rank-$r$ matrix of coherence $\mu_0$ with probability at least $1 - \delta$ needs about $\mu_0 n r \log(n / (2\delta))$ entries. So when the coherences are bounded by constants, the upper bound is tight up to a constant and one factor of $\log n$.
- **Counting.** A rank-$r$ matrix of size $n \times n$ has $r (2n - r)$ degrees of freedom, so fewer entries than that cannot determine it.
- **Hardness.** With an arbitrary pattern of known entries, finding the lowest rank completion is NP-hard (Recht 2011, Section 1), and low-rank approximation with missing data is NP-hard already for rank one (Gillis and Glineur 2011). The positive results above depend on the random sampling.

## Reductions

- **Rank minimization to a semidefinite program.** The nuclear norm bound $\lVert X \rVert_* \le t$ holds exactly when there are symmetric $A$ and $B$ with $\operatorname{tr} A + \operatorname{tr} B \le 2t$ and $\begin{pmatrix} A & X \\ X^\top & B \end{pmatrix} \succeq 0$. So nuclear norm minimization under linear constraints is a semidefinite program.
- **From compressed sensing.** A diagonal matrix has rank equal to its number of nonzero diagonal entries and nuclear norm equal to the $\ell_1$ norm of its diagonal. So rank minimization contains sparse recovery, and nuclear norm minimization contains [basis pursuit](/basis-pursuit/). The analogy guides the theory of [compressed sensing](/compressed-sensing/) for matrices, but entry sampling does not have the [restricted isometry property](/restricted-isometry-property/), and incoherence takes its place.

## Applications

- **Rating prediction.** The [rating matrix](/rating-matrix/) of a recommender is treated as a noisy, partly observed low-rank matrix, and its completion gives predicted ratings. This is the reading behind [collaborative filtering](/collaborative-filtering/) by matrix factorization. Rating data are not missing at random, since users choose what to rate, so the recovery theorems describe an ideal case; the quality of predicted ratings is measured on held-out data, never proved.
- **Other areas.** Candès and Tao (2010, Section 1.1) list structure from motion in computer vision, system identification in control, multi-class learning, sensor positions from partial distances, and covariance estimation from partial correlations. Recht (2011, Section 1) adds dimensionality reduction and embedding problems, and his proof comes from quantum state tomography (Gross et al. 2010).

## References
