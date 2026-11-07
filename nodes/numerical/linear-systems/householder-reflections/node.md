---
tag: WRPYB6
kind: technique
slug: householder-reflections
name: Householder reflections
aliases:
- Householder transformation
- Householder reflector
- elementary reflector
area: numerical/linear-systems
level: advanced
summary: Orthogonal reflections that zero all entries below a pivot in one step, the basis of stable QR.
prereqs: [matrix-norms, backward-error-analysis, floating-point-model]
see_also: [qr-decomposition, givens-rotations, gram-schmidt-process, least-squares-problem, singular-value-decomposition, qr-algorithm, backward-error-analysis, condition-number]
sources:
  - paper: doi:10.1145/320941.320947
    title: Alston S. Householder, Unitary triangularization of a nonsymmetric matrix, Journal of the ACM 5(4), 1958
    locator: pp. 339 to 342 (the reflector I - 2 w w^T and triangularization by n - 1 reflections)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.1, Householder and Givens transformations (Algorithm 5.1.1, the Householder vector; Sections 5.1.4 to 5.1.7, applying, factored form, WY representation); Section 5.2.2, Householder QR
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 19, QR Factorization (Section 19.3, Householder transformations; the lemmas on computed reflectors and Theorem 19.4, backward error of Householder QR)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 10, Householder Triangularization; Lecture 16, Stability of Householder Triangularization (Theorem 16.1)
  - paper: doi:10.1137/0910005
    title: Robert Schreiber and Charles Van Loan, A storage-efficient WY representation for products of Householder transformations, SIAM Journal on Scientific and Statistical Computing 10(1), 1989
    locator: pp. 53 to 57 (the compact form I - Y T Y^T)
  - paper: doi:10.1137/0908009
    title: Christian Bischof and Charles Van Loan, The WY representation for products of Householder matrices, SIAM Journal on Scientific and Statistical Computing 8(1), 1987
    locator: pp. s2 to s13 (blocking Householder products for level 3 BLAS)
---

A Householder reflection is the matrix $P = I - \beta v v^T$ with $\beta = 2/(v^T v)$. It reflects every vector across the hyperplane orthogonal to $v$, so it is symmetric, orthogonal and its own inverse. For any nonzero $x \in \mathbb{R}^m$ there is a $v$ with $P x = \mp\|x\|_2 e_1$: one reflection zeros all entries of a column below the pivot. A product of $n$ such reflections reduces an $m \times n$ matrix to upper triangular form, which is Householder QR, at $2 m n^2 - 2n^3/3$ flops. Because each step is an exactly orthogonal map perturbed by rounding of order $u$, the result is backward stable with no growth factor, unlike [Gaussian elimination](/gaussian-elimination/), and the computed $Q$ is orthogonal to working precision, unlike [Gram-Schmidt](/gram-schmidt-process/).

## In plain words

A mirror placed at the right angle can send any arrow onto a chosen axis while keeping its length. A Householder reflection is such a mirror in many dimensions. To clear the entries under the diagonal in one column, choose the mirror that sends that column onto the first axis, and apply the same mirror to the other columns. Mirrors never stretch anything, so rounding errors do not grow from step to step. Repeating this column by column turns a matrix into a triangle, which is how most software computes a QR factorization.

## When it applies

The technique applies whenever a computation needs an orthogonal transformation that maps a given vector to a multiple of a coordinate vector, or more generally to any vector of the same 2-norm, and applies that transformation to other data. It is the tool of choice when a whole subcolumn must be zeroed at once and the matrix is dense. For zeroing single entries in sparse or structured matrices, [Givens rotations](/givens-rotations/) are cheaper.

**Notation.** $A \in \mathbb{R}^{m \times n}$ with $m \ge n$, $x \in \mathbb{R}^m$, $e_1$ the first unit vector, $P = I - \beta v v^T$ the reflector. The unit roundoff is $u = 2^{-53}$ in binary64, $\gamma_k = k u/(1 - k u)$, and $\tilde\gamma_k = c k u/(1 - c k u)$ with a small integer constant $c$, as in Higham. $\kappa_2(A) = \sigma_{\max}/\sigma_{\min}$ is the [condition number](/condition-number/).

**Facts used below (proved).** If $v \ne 0$ and $\beta = 2/(v^T v)$, then $P^T = P$ and $P^2 = I - 2\beta v v^T + \beta^2 v (v^T v) v^T = I$, so $P$ is orthogonal. If $\|x\|_2 = \|y\|_2$ and $x \ne y$, then $v = x - y$ gives $P x = y$, since $v^T x = \tfrac12 v^T v$ when the norms agree.

## The template

```pseudo id=main
HOUSE(x)                                            ▷ x ∈ ℝ^m; returns v, β with (I − β v vᵀ) x = α e₁
L1  σ ← x₂² + ... + x_m²                             ▷ hole: scaled norm to avoid overflow
L2  if σ = 0 then return v = e₁, β = 0, α = x₁       ▷ x is already a multiple of e₁
L3  μ ← sqrt(x₁² + σ)
L4  α ← −sign(x₁) · μ                                ▷ sign chosen so that v₁ = x₁ − α has no cancellation
L5  v ← x; v₁ ← x₁ − α
L6  β ← 2 / (v₁² + σ)
L7  return v, β, α
APPLY(v, β, B)                                      ▷ B ← (I − β v vᵀ) B, never forming P
L8  w ← β · (Bᵀ v)
L9  B ← B − v wᵀ
```

The holes are how the norm is computed and how $v$ is normalized. LAPACK's `dlarfg` scales $x$ to avoid overflow and underflow in $\sigma$, normalizes $v_1 = 1$ so that $v$ can be stored below the diagonal in place of the zeros it creates, and returns $\tau = \beta v_1^2$. Golub and Van Loan (Algorithm 5.1.1) use $v_1 = -\sigma/(x_1 + \mu)$ when $x_1 > 0$, which allows $P x = +\mu e_1$ without cancellation.

**Why the sign matters.** If $\alpha$ had the same sign as $x_1$ and $x$ were close to a multiple of $e_1$, then $v_1 = x_1 - \alpha$ would be the difference of two nearly equal numbers, and the relative error of $\hat v_1$ could be as large as $u \|x\|_2 / |v_1|$, without bound. With $\alpha = -\operatorname{sign}(x_1)\mu$, $|v_1| = |x_1| + \mu \ge \mu$, and every entry of $\hat v$ has a relative error of a few $u$. The lemma in Higham, Section 19.3, gives $\hat v = v + \Delta v$ with $|\Delta v| \le \tilde\gamma_m |v|$ and $\hat\beta = \beta(1 + \theta)$, $|\theta| \le \tilde\gamma_m$.

**Cost.** HOUSE costs about $3m$ flops and one square root. APPLY to an $m \times n$ block costs $4 m n$ flops: $2mn$ for $B^T v$ and $2mn$ for the rank one update. Forming $P$ and multiplying would cost $2 m^2 n$, so it is never done.

**Error of one application (proved).** For the computed $\hat v$, $\hat\beta$ and any $b$, $\mathrm{fl}(\hat P b) = (P + \Delta P) b$ with $P$ the exact reflector of $x$ and $\|\Delta P\|_F \le \tilde\gamma_m$ (Higham, Section 19.3). Since $P$ is orthogonal, this is a normwise relative backward error of order $m u$, independent of the size of the entries.

## Classic examples

**One vector.** For $x = (3, 4)^T$, $\mu = 5$, $\alpha = -5$, $v = (8, 4)^T$, $v^T v = 80$, $\beta = 1/40$. Then $v^T x = 40$ and $P x = x - \beta (v^T x) v = (3, 4) - (8, 4) = (-5, 0)$.

**Householder QR.** For $k = 1, \ldots, n$, compute HOUSE of $A_{k:m, k}$ and APPLY it to $A_{k:m, k:n}$. For

$$A = \begin{pmatrix} 1 & 1 \\ 2 & 0 \\ 2 & 1 \end{pmatrix},$$

the first column has $\mu = 3$, $\alpha = -3$, $v = (4, 2, 2)^T$, $\beta = 1/12$. The second column has $v^T a_2 = 6$, so it becomes $(1, 0, 1) - \tfrac12 (4, 2, 2) = (-1, -1, 0)$. The subcolumn $(-1, 0)$ already has a zero below the pivot, so $\sigma = 0$ and the second reflector is $I$. The result is $R = \begin{pmatrix} -3 & -1 \\ 0 & -1 \end{pmatrix}$, and indeed $R^T R = \begin{pmatrix} 9 & 3 \\ 3 & 2 \end{pmatrix} = A^T A$. The step $k$ applies to an $(m - k + 1) \times (n - k + 1)$ block, so the total is $\sum_k 4(m - k + 1)(n - k + 1) \approx 2 m n^2 - 2 n^3/3$ flops (Golub and Van Loan, Section 5.2.2; Trefethen and Bau, Lecture 10). This is $4n^3/3$ for a square matrix, twice the cost of LU.

**Backward stability of QR (proved).** Let $\hat R$ be the computed factor. There is an exactly orthogonal $Q$ with $A + \Delta A = Q \hat R$ and $\|\Delta a_j\|_2 \le \tilde\gamma_{mn} \|a_j\|_2$ for each column $j$ (Higham, Theorem 19.4; Trefethen and Bau, Theorem 16.1, in normwise form). The hypothesis is only that $m n u$ is small enough for $\tilde\gamma_{mn}$ to be defined; no condition on $A$ and no growth factor appears. The computed explicit $\hat Q$ satisfies $\|\hat Q^T \hat Q - I\| = O(m n u)$ regardless of $\kappa_2(A)$. By contrast, classical Gram-Schmidt loses orthogonality like $\kappa_2(A)^2 u$ and modified Gram-Schmidt like $\kappa_2(A) u$ (both observed and, for MGS, proved by Björck).

**Least squares.** To minimize $\|b - A x\|_2$, apply the reflectors to $b$ as they are computed and solve $R x = (Q^T b)_{1:n}$ by [back substitution](/back-substitution/). The computed $\hat x$ is the exact solution of a nearby problem $\min \|(b + \Delta b) - (A + \Delta A) x\|_2$ with columnwise relative perturbations of order $m n u$ (Higham, Theorem 20.3). See [least squares problem](/least-squares-problem/).

**Reduction to Hessenberg, tridiagonal and bidiagonal form.** Reflectors applied from both sides, $P A P$, preserve eigenvalues. Zeroing below the subdiagonal gives Hessenberg form in $10 n^3/3$ flops, tridiagonal form for symmetric $A$ in $4 n^3/3$ flops, and alternating left and right reflectors give bidiagonal form in $4 m n^2 - 4 n^3/3$ flops. These are the first phases of the [QR algorithm](/qr-algorithm/) and of the [SVD](/singular-value-decomposition/) (Golub and Van Loan, Sections 7.4.3, 8.3.1 and 5.4.8).

## Variations

- **Blocked (WY) form.** A product of $r$ reflectors can be written $I - W Y^T$ (Bischof and Van Loan 1987) or, in the compact form, $I - V T V^T$ with $V$ the $m \times r$ matrix of Householder vectors and $T$ an $r \times r$ upper triangular matrix (Schreiber and Van Loan 1989). Applying it costs matrix-matrix products, so a blocked QR does most of its flops in level 3 BLAS. On modern hardware this matters more than the flop count, since unblocked APPLY is limited by memory bandwidth: it touches each entry of $B$ twice for 4 flops.
- **Column pivoting.** Before step $k$, swap the column with the largest remaining norm to the front. The diagonal of $R$ then decreases, which reveals numerical rank (see [rank-revealing factorization](/rank-revealing-factorization/)).
- **Complex reflectors.** For $x \in \mathbb{C}^m$, LAPACK uses $H = I - \tau v v^*$ with complex $\tau$, which is unitary but not Hermitian, so that $H^* x = \alpha e_1$ with real $\alpha$.
- **Tall skinny QR (TSQR).** For $m \gg n$, factor row blocks independently and combine the $R$ factors in a reduction tree. Each combination is a Householder QR of stacked triangles. This reduces communication to $O(\log p)$ messages on $p$ processors with the same backward stability.
- **Reflecting onto any vector.** With $v = x - y$ for $\|y\|_2 = \|x\|_2$, $P x = y$. Used, for example, in updating problems and in proving that the orthogonal group is generated by reflections.

## Pitfalls

- **Wrong sign.** Using $\alpha = +\operatorname{sign}(x_1)\|x\|$ without the Golub-Van Loan formula gives cancellation in $v_1$. For $x = (1, 10^{-9})^T$ the cancelling choice gives $v_1 = 1 - \sqrt{1 + 10^{-18}}$, which rounds to $0$ in binary64. Then $\beta = 2 \cdot 10^{18}$ and $P x = (1, -10^{-9})^T$ instead of $(1, 0)^T$: the entry that should vanish keeps its size, a backward error of $10^{-9}$, far above $u$.
- **Overflow in the norm.** Computing $\sum x_i^2$ directly overflows when an entry exceeds about $10^{154}$ and underflows below $10^{-154}$. Scale by $\max |x_i|$ or use a careful 2-norm, as `dnrm2` does.
- **Forming $P$.** Building the $m \times m$ matrix costs $O(m^2)$ storage and turns $O(m n)$ work into $O(m^2 n)$. Keep $v$ and $\beta$.
- **Forming $Q$ when only $Q^T b$ is needed.** For least squares, apply the reflectors to $b$. If $Q$ is needed, accumulate it backward, starting from the last reflector, to exploit the zeros: this costs $4(m^2 n - m n^2 + n^3/3)$ flops for the full $m \times m$ $Q$ (Golub and Van Loan, Section 5.1.6).
- **Expecting a positive diagonal.** The sign rule makes $r_{kk} = -\operatorname{sign}(x_1)\mu$, so $R$ may have negative diagonal entries. Multiply rows of $R$ and columns of $Q$ by $-1$ if a positive diagonal is wanted; the factorization is unique only up to these signs.
- **Destroying sparsity.** A reflector mixes all rows of the active block, so on a sparse matrix it fills in whole rows. Use Givens rotations or a sparse QR with a column ordering.

## Exercises

1. Show that $P = I - \beta v v^T$ has eigenvalue $-1$ with eigenvector $v$ and eigenvalue $1$ with multiplicity $m - 1$, so $\det P = -1$.
2. Show that if $\|x\|_2 = \|y\|_2$ and $x \ne y$, the reflector with $v = x - y$ maps $x$ to $y$.
3. Derive the Golub-Van Loan formula $v_1 = -\sigma/(x_1 + \mu)$ for $x_1 > 0$ from $x_1 - \mu = (x_1^2 - \mu^2)/(x_1 + \mu)$.
4. Count the flops of Householder QR exactly and show that the leading term is $2 m n^2 - 2 n^3/3$.
5. Show that $(I - \beta_1 v_1 v_1^T)(I - \beta_2 v_2 v_2^T) = I - V T V^T$ with $V = [v_1, v_2]$ and $T = \begin{pmatrix} \beta_1 & -\beta_1 \beta_2 v_1^T v_2 \\ 0 & \beta_2 \end{pmatrix}$.
6. Compute the QR factorization of the $5 \times 3$ [Hilbert](/hilbert-matrix/) section in binary64 by Householder reflections and by classical Gram-Schmidt, and compare $\|\hat Q^T \hat Q - I\|_2$.

## References
