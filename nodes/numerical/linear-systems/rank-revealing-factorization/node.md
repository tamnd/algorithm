---
tag: EKG9A3
kind: concept
slug: rank-revealing-factorization
name: Rank-revealing factorization
aliases:
- rank-revealing QR
- RRQR
- QR with column pivoting
- rank-revealing LU
area: numerical/linear-systems
level: advanced
summary: A factorization that exposes the numerical rank of a matrix through its diagonal.
prereqs: [qr-decomposition, singular-value-decomposition]
see_also: [pseudoinverse, least-squares-problem, householder-reflections, tikhonov-regularization, condition-number, complete-pivoting, lup-decomposition, matrix-norms]
sources:
  - paper: doi:10.1007/BF01436084
    title: Peter Businger and Gene H. Golub, Linear least squares solutions by Householder transformations, Numerische Mathematik 7, 1965
    locator: Householder QR with column pivoting by largest remaining column norm
  - paper: doi:10.1016/0024-3795(87)90103-0
    title: Tony F. Chan, Rank revealing QR factorizations, Linear Algebra and its Applications 88/89, 1987
    locator: the definition of a rank-revealing QR factorization and an algorithm based on estimates of the smallest singular vectors
  - paper: doi:10.1090/S0025-5718-1992-1106970-4
    title: Yoo Pyo Hong and Ching-Tsuan Pan, Rank-revealing QR factorizations and the singular value decomposition, Mathematics of Computation 58, 1992
    locator: existence of a column permutation with bounds polynomial in k and n
  - paper: doi:10.1137/0917055
    title: Ming Gu and Stanley C. Eisenstat, Efficient algorithms for computing a strong rank-revealing QR factorization, SIAM Journal on Scientific Computing 17(4), 1996
    locator: strong rank-revealing QR, the bound on the entries of R11^-1 R12, and an algorithm that costs little more than QR with column pivoting
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.4, Other Orthogonal Factorizations (QR with column pivoting, its use for rank determination, and the UTV factorizations); Section 5.5, The Rank-Deficient Least Squares Problem
---

A rank-revealing factorization of $A \in \mathbb{R}^{m \times n}$ writes $A \Pi = Q R$ (or $A = U T V^T$, or $P A \Pi = L U$) so that a gap in the singular values of $A$ shows up as a gap in the triangular factor: for the right $k$,
$$R = \begin{pmatrix} R_{11} & R_{12} \\ 0 & R_{22} \end{pmatrix}, \qquad \sigma_{\min}(R_{11}) \ge \frac{\sigma_k(A)}{p(k, n)}, \qquad \|R_{22}\|_2 \le p(k, n)\,\sigma_{k+1}(A),$$
with $R_{11}$ of order $k$ and $p(k, n)$ a modest function. It gives the numerical rank, a well-conditioned basis of the range, and least squares solutions of rank-deficient problems, at the cost of a QR factorization rather than an SVD.

## In plain words

In exact arithmetic the rank of a matrix is a count, but after rounding nearly every matrix has full rank, and the question becomes how many directions are really there and how many are just noise. The singular value decomposition answers this exactly but costs a lot. A rank-revealing factorization reorders the columns so that the important ones come first, then triangularizes. If the reordering is good, the part of the triangle that belongs to the leftover columns is tiny, about as small as the noise, and the important part is safely far from singular.

## The idea

**Notation.** $A \in \mathbb{R}^{m \times n}$, $m \ge n$, singular values $\sigma_1 \ge \cdots \ge \sigma_n \ge 0$, $\Pi$ a permutation, $u = 2^{-53}$. The *numerical rank* for a tolerance $\tau$ is the number of singular values above $\tau$, for instance $\tau = \max(m,n)\,u\,\|A\|_2$ or a tolerance set by the uncertainty in the data.

**What any QR gives.** For every permutation, by interlacing of singular values of submatrices,
$$\sigma_i(R_{11}) \le \sigma_i(A), \qquad \sigma_j(R_{22}) \ge \sigma_{k+j}(A).$$
So $R_{11}$ can only be worse conditioned than the leading part of $A$, and $R_{22}$ can only be larger than the tail. The factorization is rank revealing when both inequalities hold within the factor $p(k, n)$, and then the numerical rank can be read off. A *strong* rank-revealing QR also asks $|(R_{11}^{-1} R_{12})_{ij}| \le f$ for a constant $f \ge 1$, which makes the null space basis $\Pi \begin{pmatrix} -R_{11}^{-1}R_{12} \\ I \end{pmatrix}$ well conditioned.

**QR with column pivoting (Businger and Golub, 1965).** At step $j$, move the remaining column of largest norm (in the part not yet triangularized) to position $j$, then apply a Householder reflection. This makes $|r_{11}| \ge |r_{22}| \ge \cdots$ and $r_{jj}^2 \ge \sum_{i = j}^{l} r_{il}^2$ for $l > j$. It costs $4 m n k - 2k^2(m + n) + 4k^3/3$ flops for $k$ steps, like unpivoted Householder QR, plus the norm downdates. It reveals the rank in almost every case met in practice, but there is no polynomial guarantee: on the Kahan matrix below it fails by an exponential factor. Its worst-case bounds relating $|r_{kk}|$ to $\sigma_k(A)$ grow exponentially with $k$.

**Guaranteed versions.**
- *Existence.* Hong and Pan (1992) proved that a permutation exists with $p(k, n) = \sqrt{k(n - k) + \min(k, n - k)}$.
- *Strong RRQR.* Gu and Eisenstat (1996) find, by column swaps that each increase $|\det R_{11}|$ by a factor above $f$, a factorization with $p(k, n) = \sqrt{1 + f^2 k(n - k)}$ and $|R_{11}^{-1} R_{12}| \le f$ entrywise, in $O(m n k)$ flops for fixed $f > 1$.
- *Chan's algorithm (1987)* repairs a column-pivoted QR by estimating a small singular vector of $R_{11}$ and permuting its largest component to the end.
- *UTV.* $A = U \begin{pmatrix} T_{11} & T_{12} \\ 0 & T_{22} \end{pmatrix} V^T$ with orthogonal $U, V$ (Stewart's URV and ULV) can be updated cheaply when rows are added, which suits signal processing.
- *Rank-revealing LU.* $P A \Pi = L U$ with similar bounds on $U_{22}$, cheaper for sparse matrices; complete pivoting is a heuristic RRLU.

**Floating point.** Householder QR with column pivoting is backward stable: the computed factors are exact for $(A + E)\Pi$ with $\|E\|_2 \le c(m, n)\,u\,\|A\|_2$. So the computed $\hat{R}_{22}$ is within $c\,u\,\|A\|_2$ of the exact factor of a nearby matrix, and singular values above that level are revealed reliably (proved through the backward error and Weyl's inequality); below it, no factorization can distinguish them from zero.

## Examples

**A nearly dependent column.** Let $A$ have columns $a_1 = e_1$, $a_2 = e_2$ and $a_3 = e_1 + e_2 + 10^{-10} e_3$. Column pivoting takes $a_3$ first (norm $\sqrt2$), then $a_2$, and computes
$$R = \begin{pmatrix} 1.414 & 0.707 & 0.707 \\ 0 & 0.707 & -0.707 \\ 0 & 0 & 10^{-10} \end{pmatrix}, \qquad \Pi = (3, 2, 1).$$
$R_{22} = 10^{-10}$ shows numerical rank $2$ for any tolerance above $10^{-10}$, and $R_{11}$ is well conditioned.

**The Kahan matrix.** For $s^2 + c^2 = 1$, $K_n = \mathrm{diag}(1, s, \ldots, s^{n-1})\,T$ with $T$ unit upper triangular and every entry above the diagonal equal to $-c$. All its columns have norm $1$, and after scaling column $j$ by $1 - 10^{-9} j$ to break ties, column pivoting does no interchange, so $R = K_n$ and its smallest diagonal entry is $s^{n-1}$. Computed with inverse iteration on the triangular factor, the smallest singular value is much smaller:

| $n$ | $c$ | $|r_{nn}| = s^{n-1}$ | $\sigma_n$ |
|---|---|---|---|
| 30 | 0.2 | 0.553 | $5.4 \times 10^{-3}$ |
| 50 | 0.2 | 0.368 | $9.3 \times 10^{-5}$ |
| 90 | 0.285 | 0.0231 | $8.8 \times 10^{-12}$ |

At $n = 90$ the diagonal suggests full rank with a smallest pivot of $0.02$, while $K_n$ is within $10^{-11}$ of a singular matrix. A strong RRQR swaps the last column forward and reveals it.

**The SVD as the ideal.** $A = U \Sigma V^T$ is rank revealing with $p = 1$; its cost, about $4 m n^2 + 8 n^3$ flops for $\Sigma$ and $V$ with Golub-Kahan-Reinsch, is several times that of QR with column pivoting.

**Non-example.** Unpivoted QR of $A = (e_1 \;\; e_1 \;\; e_2) \in \mathbb{R}^{3 \times 3}$, which has rank $2$, gives $R = \begin{pmatrix} 1 & 1 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$. The zero pivot sits in the middle, so for $k = 2$ the block $R_{11}$ is singular and $R_{22} = (1)$ is not small: the factor shows that something is singular but not the rank split. Column pivoting moves the dependent column to the end and gives $R_{22} = 0$.

## Where it is used

- **Rank-deficient least squares.** With numerical rank $k$, a basic solution solves $R_{11} y = (Q^T b)_{1:k}$; a complete orthogonal decomposition gives the minimum-norm solution $A^+ b$ of the [pseudoinverse](/pseudoinverse/) page (Golub and Van Loan, Section 5.5).
- **Subset selection.** The first $k$ columns of $A \Pi$ are a well-conditioned set of $k$ columns of $A$, used to choose regressors, sensors or interpolation points.
- **Low-rank approximation.** $Q_{:,1:k}(R_{11} \; R_{12})\Pi^T$ approximates $A$ within $\|R_{22}\|_2$; randomized and interpolative decompositions start with a QR with column pivoting of a sketch.
- **Null spaces and regularization.** The trailing columns give a null space basis; truncating at the gap is a regularization comparable to the truncated SVD and to [Tikhonov regularization](/tikhonov-regularization/).
- **Signal processing and control.** Updatable URV and ULV factorizations track the dimension of a signal subspace as data arrive.

## References
