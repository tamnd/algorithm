---
tag: ZTRF0D
kind: theorem
slug: hoffman-wielandt-theorem
name: Hoffman-Wielandt theorem
aliases:
- Hoffman-Wielandt inequality
- Wielandt-Hoffman theorem
area: numerical/eigenproblems
level: research
summary: For normal A and B there is a pairing of their eigenvalues whose sum of squared differences is at most the squared Frobenius norm of A - B; for Hermitian matrices the sorted pairing works.
prereqs: [spectral-theorem, matrix-norms, birkhoff-von-neumann-decomposition]
see_also: [weyls-inequality, bauer-fike-theorem, davis-kahan-theorem, symmetric-eigenproblem, singular-value-decomposition, assignment-problem, courant-fischer-theorem, eigenvalue-condition-number]
sources:
  - paper: doi:10.1215/S0012-7094-53-02004-3
    title: A. J. Hoffman and H. W. Wielandt, The variation of the spectrum of a normal matrix, Duke Mathematical Journal 20, 1953
    locator: pp. 37 to 39 (the theorem and the doubly stochastic matrix proof)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 6.3, Eigenvalue perturbation theorems (the Hoffman-Wielandt theorem and its Hermitian form)
  - book: isbn:9780387948461
    title: Rajendra Bhatia, Matrix Analysis, Graduate Texts in Mathematics 169, Springer, 1997
    locator: Chapter VI, Spectral Variation of Normal Matrices (the Hoffman-Wielandt inequality, and the failure of the analogous spectral norm bound)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1.2, Eigenvalue Sensitivity (the Wielandt-Hoffman theorem for symmetric matrices)
  - book: isbn:9780126702309
    title: G. W. Stewart and Ji-guang Sun, Matrix Perturbation Theory, Academic Press, 1990
    locator: Chapter IV, Section 3 (the Hoffman-Wielandt theorem and its extensions)
  - paper: "G. Birkhoff, Tres observaciones sobre el algebra lineal, Universidad Nacional de Tucumán Revista Serie A 5, 1946, pp. 147 to 151"
    title: G. Birkhoff, Tres observaciones sobre el algebra lineal
    locator: the extreme points of the doubly stochastic matrices are the permutation matrices
---

The Hoffman-Wielandt theorem bounds the change in the whole spectrum of a normal matrix in the Frobenius norm. If $A$ and $B$ are normal with eigenvalues $\alpha_1, \dots, \alpha_n$ and $\beta_1, \dots, \beta_n$, then for some permutation $\pi$, $\sum_i |\alpha_i - \beta_{\pi(i)}|^2 \le \|A - B\|_F^2$. For Hermitian matrices with both spectra sorted in decreasing order, $\pi$ can be the identity. [Weyl's inequality](/weyls-inequality/) bounds each eigenvalue change by $\|E\|_2$; this theorem bounds all of them together, in the root-mean-square sense, which is often much sharper when the perturbation is spread out. The proof is a short argument with doubly stochastic matrices and the Birkhoff-von Neumann theorem.

## Statement

**Notation.** $\|M\|_F = (\sum_{ij} |m_{ij}|^2)^{1/2}$. A matrix is normal if $M M^* = M^* M$, which by the [spectral theorem](/spectral-theorem/) means $M = U \operatorname{diag}(\mu_i) U^*$ with $U$ unitary. For Hermitian $M$, $\lambda_1(M) \ge \dots \ge \lambda_n(M)$.

1. **Normal matrices.** Let $A, B \in \mathbb{C}^{n \times n}$ be normal, with eigenvalues $\alpha_1, \dots, \alpha_n$ and $\beta_1, \dots, \beta_n$ listed with multiplicity in any order. There is a permutation $\pi$ of $\{1, \dots, n\}$ with
$$\sum_{i=1}^{n} |\alpha_i - \beta_{\pi(i)}|^2 \le \|A - B\|_F^2 .$$
2. **Hermitian matrices.** If $A$ and $B$ are Hermitian, then
$$\sum_{i=1}^{n} (\lambda_i(A) - \lambda_i(B))^2 \le \|A - B\|_F^2 ,$$
and the sorted pairing minimizes $\sum_i (\lambda_i(A) - \lambda_{\pi(i)}(B))^2$ over all permutations.
3. **Two-sided form.** For Hermitian $A$ and $B$, also $\sum_i (\lambda_i(A) - \lambda_{n+1-i}(B))^2 \ge \|A - B\|_F^2$.

No hypothesis on the size of $A - B$ is needed. The normality of both matrices is essential; see Tightness.

## In plain words

Change a symmetric matrix a little, and each of its eigenvalues moves. One classical result says that no eigenvalue moves more than the largest stretch of the change. This theorem looks at the total instead: square the movements of all eigenvalues, add them up, and the sum is at most the sum of squares of all entries of the change.

So if a change is spread thinly over many directions, the eigenvalues as a group barely move, even though the largest stretch alone would allow much more. For matrices with complex eigenvalues the same holds, as long as both matrices are of the well-behaved kind called normal and the eigenvalues are matched up in the best way.

## Proof

**Step 1 (reduction to a doubly stochastic matrix).** Write $A = U D_\alpha U^*$ and $B = V D_\beta V^*$ with $U$, $V$ unitary and $D_\alpha = \operatorname{diag}(\alpha_i)$, $D_\beta = \operatorname{diag}(\beta_j)$. Put $W = U^* V$, which is unitary. The Frobenius norm is unitarily invariant, so
$$\|A - B\|_F^2 = \|U^* (A - B) V\|_F^2 = \|D_\alpha W - W D_\beta\|_F^2 = \sum_{i, j} |w_{ij}|^2 \, |\alpha_i - \beta_j|^2,$$
since the $(i, j)$ entry of $D_\alpha W - W D_\beta$ is $(\alpha_i - \beta_j) w_{ij}$. The matrix $P = (|w_{ij}|^2)$ is doubly stochastic: its entries are nonnegative, and every row and every column of the unitary $W$ has unit length, so its row sums and column sums are 1.

**Step 2 (minimum at a permutation).** Let $c_{ij} = |\alpha_i - \beta_j|^2$ and $\phi(P) = \sum_{ij} p_{ij} c_{ij}$, a linear function. By the Birkhoff-von Neumann theorem ([Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/)), every doubly stochastic $P$ is a convex combination $\sum_k t_k \Pi_k$ of permutation matrices, $t_k \ge 0$, $\sum_k t_k = 1$. Then $\phi(P) = \sum_k t_k \phi(\Pi_k) \ge \min_k \phi(\Pi_k)$. If $\Pi_k$ is the matrix of the permutation $\pi$, $\phi(\Pi_k) = \sum_i |\alpha_i - \beta_{\pi(i)}|^2$. Combining with Step 1 gives item 1.

**Step 3 (sorted pairing for real spectra).** For real $\alpha$, $\beta$, $\sum_i (\alpha_i - \beta_{\pi(i)})^2 = \sum_i \alpha_i^2 + \sum_i \beta_i^2 - 2 \sum_i \alpha_i \beta_{\pi(i)}$. By the rearrangement inequality, $\sum_i \alpha_i \beta_{\pi(i)}$ is largest when both sequences are sorted in the same order and smallest when they are sorted in opposite orders. (If $\alpha_i > \alpha_j$ and $\beta_{\pi(i)} < \beta_{\pi(j)}$, swapping the two values increases the sum by $(\alpha_i - \alpha_j)(\beta_{\pi(j)} - \beta_{\pi(i)}) > 0$; finitely many swaps sort the sequence.) So with $\alpha_i = \lambda_i(A)$ and $\beta_i = \lambda_i(B)$ in decreasing order, the identity pairing minimizes the sum, and item 1 gives item 2.

**Step 4 (two-sided form).** In Step 2 the same convexity argument gives $\phi(P) \le \max_k \phi(\Pi_k)$, and by Step 3 the maximum over permutations of $\sum_i (\alpha_i - \beta_{\pi(i)})^2$ is attained by the reversed pairing. $\square$

## Consequences

- **Root-mean-square stability of Hermitian spectra.** With $E = A - B$, $\big(\frac{1}{n} \sum_i (\lambda_i(A) - \lambda_i(B))^2\big)^{1/2} \le \|E\|_F / \sqrt{n}$. Since $\|E\|_F \le \sqrt{n} \|E\|_2$, this is never worse on average than the Weyl bound. When $E$ has rank $r$, $\|E\|_F \le \sqrt{r} \|E\|_2$, and the root-mean-square error is at most $\sqrt{r/n}\, \|E\|_2$, much less than Weyl's bound for every eigenvalue at once.
- **Singular values (Mirsky).** Applied to the Hermitian matrices $\begin{pmatrix} 0 & A \\ A^* & 0 \end{pmatrix}$, whose eigenvalues are $\pm \sigma_i(A)$, it gives $\sum_i (\sigma_i(A) - \sigma_i(B))^2 \le \|A - B\|_F^2$ for any $m \times n$ matrices, the bound behind the Frobenius part of the Eckart-Young theorem for the [singular value decomposition](/singular-value-decomposition/).
- **Backward error of eigensolvers.** A backward stable symmetric eigensolver computes the exact eigenvalues of $A + E$ with $\|E\|_F \le c(n) u \|A\|_F$. The theorem then bounds the whole vector of eigenvalue errors in the 2-norm by $c(n) u \|A\|_F$; see the [symmetric eigenproblem](/symmetric-eigenproblem/).
- **Matching spectra is an assignment problem.** For normal matrices the best $\pi$ minimizes $\sum_i |\alpha_i - \beta_{\pi(i)}|^2$, an instance of the [assignment problem](/assignment-problem/), solvable in $O(n^3)$ time by the Hungarian algorithm. For real spectra, sorting suffices.
- **Comparison with Bauer-Fike.** The [Bauer-Fike theorem](/bauer-fike-theorem/) needs only one matrix to be normal but locates each eigenvalue of $B$ near some eigenvalue of $A$, without a matching. Hoffman-Wielandt needs both normal and gives a matching.

## Tightness

- **Equality for commuting matrices.** If $A$ and $B$ are normal and commute, they are simultaneously unitarily diagonalizable, $W$ is a permutation matrix up to phases, and equality holds for that pairing. For example, $A = \operatorname{tridiag}(1, 2, 1)$ of order 3 and $B = 2I$: the eigenvalues of $A$ are $2 + \sqrt 2$, $2$, $2 - \sqrt 2$, so $\sum_i (\lambda_i(A) - 2)^2 = 4 = \|A - B\|_F^2$.
- **Equality without commuting.** $A = \operatorname{diag}(1, -1)$ and the rotation $B = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$, with eigenvalues $\pm i$, do not commute. Both pairings give $|1 - i|^2 + |-1 + i|^2 = 4$ and $|1 + i|^2 + |-1 - i|^2 = 4$, and $\|A - B\|_F^2 = 4$.
- **Normality is necessary.** For $A = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ and $B = \begin{pmatrix} 0 & 1 \\ \varepsilon & 0 \end{pmatrix}$, the eigenvalues are $0, 0$ and $\pm \sqrt{\varepsilon}$, so every pairing gives $2\varepsilon$, while $\|A - B\|_F^2 = \varepsilon^2$. For $\varepsilon = 0.01$ the left side is 200 times the right side, and the ratio $2/\varepsilon$ is unbounded. The perturbation of a Jordan block moves eigenvalues by $\varepsilon^{1/2}$, as on the [eigenvalue condition number](/eigenvalue-condition-number/) page.
- **One normal matrix is not enough with constant 1.** If only $A$ is normal, the inequality can fail with constant 1; Sun (1996) proved it with the factor $n$ in place of 1 on the right side, $\min_\pi \sum_i |\alpha_i - \beta_{\pi(i)}|^2 \le n \|A - B\|_F^2$.
- **The spectral norm analogue fails.** The bound $\min_\pi \max_i |\alpha_i - \beta_{\pi(i)}| \le \|A - B\|_2$ holds for Hermitian matrices (Weyl), but for normal matrices in general it needs a constant larger than 1 (Bhatia, Chapter VI).

## History

Alan Hoffman and Helmut Wielandt published the theorem in 1953, in a two-page note in the Duke Mathematical Journal, with the doubly stochastic matrix argument used above. The proof brings in Birkhoff's 1946 theorem on doubly stochastic matrices, a tool from combinatorial optimization, the field in which Hoffman was then working at the National Bureau of Standards. Mirsky's 1960 paper on symmetric gauge functions extended the Hermitian form to all unitarily invariant norms, and Ji-guang Sun and others studied the case where only one matrix is normal in the 1990s.

## References
