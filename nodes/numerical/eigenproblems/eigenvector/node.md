---
tag: 2SE68A
kind: concept
slug: eigenvector
name: Eigenvector
aliases:
- characteristic vector
- proper vector
- right eigenvector
area: numerical/eigenproblems
level: intro
summary: A nonzero vector v that A maps to a scalar multiple of itself, A v = λ v. Only its direction is determined, and its sensitivity depends on the gap between λ and the other eigenvalues.
prereqs: [eigenvalue]
see_also: [eigenvalue-problem, diagonalization, inverse-iteration, rayleigh-quotient, davis-kahan-theorem, eigenvalue-condition-number, residual, eigenvector-centrality]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Chapter 1, Sections 1.1 and 1.3 (independence of eigenvectors for distinct eigenvalues), and 1.4 (left and right eigenvectors)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Sections 7.1 (properties) and 7.2 (perturbation theory, sensitivity of eigenvectors and invariant subspaces)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, Classics in Applied Mathematics 20, SIAM, 1998
    locator: Chapter 4 (residual bounds) and Chapter 11 (the sin θ bound for eigenvectors)
---

An eigenvector of a square matrix $A \in \mathbb{C}^{n \times n}$ is a nonzero vector $v \in \mathbb{C}^n$ with $A v = \lambda v$ for some scalar $\lambda$, the [eigenvalue](/eigenvalue/) that it belongs to. Only the line through $v$ is determined: each nonzero multiple $c v$ is again an eigenvector, so a program must fix a scaling before it compares eigenvectors. A left eigenvector is a nonzero $w$ with $w^* A = \lambda w^*$. How well an eigenvector can be computed depends on the distance from $\lambda$ to the rest of the spectrum, not only on the [condition of the eigenvalue](/eigenvalue-condition-number/).

## In plain words

Most vectors change direction when a matrix acts on them. An eigenvector is a vector whose direction the matrix keeps: the result lies on the same line, only longer, shorter or reversed. The amount of the stretch is the eigenvalue.

Because only the line matters, an eigenvector has no fixed length or sign. Two programs can return vectors that point in opposite directions, or that differ by a complex factor, and both are right. When two stretch amounts are almost equal, a tiny change in the matrix can turn their directions by a large angle, even though the stretch amounts barely move. So directions are harder to compute than stretch amounts when eigenvalues are close.

## The idea

**Definitions.** For an eigenvalue $\lambda$ of $A$, the *eigenspace* is $\operatorname{null}(A - \lambda I)$, a subspace of dimension equal to the geometric multiplicity of $\lambda$. Its nonzero vectors are the (right) eigenvectors for $\lambda$. A *left eigenvector* is a nonzero $w$ with $w^* A = \lambda w^*$, that is, a right eigenvector of $A^*$ for $\bar\lambda$. A subspace $\mathcal{S}$ with $A \mathcal{S} \subseteq \mathcal{S}$ is an *invariant subspace*; the span of any set of eigenvectors is one. Numerical codes often compute invariant subspaces, through the [Schur decomposition](/schur-decomposition/) $A = Q T Q^*$, rather than eigenvectors: the first $k$ columns of $Q$ span an invariant subspace for every $k$.

**Distinct eigenvalues give independent eigenvectors.** Let $A v_i = \mu_i v_i$ for $i = 1, \dots, k$ with $\mu_1, \dots, \mu_k$ pairwise distinct and each $v_i \neq 0$. Then $v_1, \dots, v_k$ are linearly independent. *Proof.* Suppose not, and take a dependence $\sum_{i \in S} c_i v_i = 0$ with all $c_i \neq 0$ and $|S|$ as small as possible; $|S| \ge 2$ since each $v_i \ne 0$. Pick $j \in S$. Apply $A - \mu_j I$: $\sum_{i \in S, i \neq j} c_i (\mu_i - \mu_j) v_i = 0$. Every coefficient is nonzero, so this is a shorter dependence, a contradiction. $\square$ Hence a matrix with $n$ distinct eigenvalues has a basis of eigenvectors and is [diagonalizable](/diagonalization/).

**Left and right eigenvectors are biorthogonal.** If $A v = \lambda v$, $w^* A = \mu w^*$ and $\lambda \neq \mu$, then $w^* v = 0$. *Proof.* $\mu \, w^* v = w^* A v = \lambda \, w^* v$, so $(\mu - \lambda) w^* v = 0$. $\square$ For a simple eigenvalue, the left and right eigenvectors $w$ and $v$ satisfy $w^* v \neq 0$, and the number $\|w\|_2 \|v\|_2 / |w^* v|$ is its [condition number](/eigenvalue-condition-number/).

**Hermitian matrices have orthogonal eigenvectors.** If $A = A^*$, then left and right eigenvectors coincide, so the result above gives $v_i^* v_j = 0$ for eigenvectors of distinct eigenvalues. With an orthonormal basis inside each eigenspace, this gives the [spectral theorem](/spectral-theorem/) $A = V \Lambda V^*$ with $V$ unitary. More generally, $A$ has an orthonormal basis of eigenvectors if and only if $A$ is normal, $A^* A = A A^*$.

**Defective matrices.** When the geometric multiplicity of some eigenvalue is below its algebraic multiplicity, there are fewer than $n$ independent eigenvectors. The missing directions are filled by *generalized eigenvectors*, vectors $x$ with $(A - \lambda I)^k x = 0$ for some $k \ge 2$; they form the chains of the [Jordan normal form](/jordan-normal-form/).

**Residual and backward error.** For a unit vector $x$ and a number $\theta$, the residual is $r = A x - \theta x$. The pair $(\theta, x)$ is an exact eigenpair of $A + E$ with $E = -r x^*$, and $\|E\|_2 = \|r\|_2$. No smaller $E$ works: if $(A + E) x = \theta x$, then $E x = -r$, so $\|E\|_2 \ge \|r\|_2$. So the [residual](/residual/) norm of a unit vector is its normwise backward error, and a residual of size $u \|A\|_2$ means the pair is exact for a matrix that rounding alone could produce ($u$ is the unit roundoff). For a given $x \neq 0$ the residual is smallest when $\theta$ is the [Rayleigh quotient](/rayleigh-quotient/) $\rho(x) = x^* A x / x^* x$.

**Sensitivity and the gap.** For a Hermitian $A$, let $(\theta, x)$ be a unit approximate eigenpair with residual $r$, and let $\delta$ be the distance from $\theta$ to the eigenvalues of $A$ other than $\lambda$. If $\delta > 0$, the angle between $x$ and the eigenvector $v$ of $\lambda$ satisfies $\sin \angle(x, v) \le \|r\|_2 / \delta$. This is the one-vector case of the [Davis-Kahan theorem](/davis-kahan-theorem/). The bound depends on the gap: a small residual guarantees an accurate eigenvector only when $\lambda$ is well separated. For a nonsymmetric matrix the bound also involves the departure from normality (Golub and Van Loan, Section 7.2).

## Examples

**A 2 by 2 matrix.** $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$ has eigenvalues 5 and 2. The right eigenvectors are $v_5 = (1, 1)^T$ and $v_2 = (1, -2)^T$. The left eigenvectors are $w_5 = (2, 1)^T$, since $(2, 1) A = (10, 5)$, and $w_2 = (1, -1)^T$, since $(1, -1) A = (2, -2)$. Biorthogonality holds: $w_5^T v_2 = 2 - 2 = 0$ and $w_2^T v_5 = 1 - 1 = 0$. The right eigenvectors are not orthogonal, $v_5^T v_2 = -1$, because $A$ is not normal.

**A symmetric matrix.** $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ has eigenvalues 3 and 1 with the orthonormal eigenvectors $(1, 1)^T/\sqrt{2}$ and $(1, -1)^T/\sqrt{2}$. The vectors $-(1, 1)^T/\sqrt2$ and $i(1, 1)^T/\sqrt2$ are equally valid unit eigenvectors for 3.

**Complex eigenvectors of a real matrix.** The rotation $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ has the eigenvector $(1, -i)^T$ for $i$: the matrix maps it to $(i, 1)^T = i (1, -i)^T$. The conjugate vector $(1, i)^T$ belongs to $-i$. A real matrix has no real eigenvector for a nonreal eigenvalue.

**A defective matrix.** For $J = \begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}$, the only eigenvectors are the multiples of $e_1$. The vector $e_2$ is a generalized eigenvector: $(J - 2I) e_2 = e_1$ and $(J - 2I)^2 e_2 = 0$.

**Close eigenvalues turn eigenvectors.** $A = \operatorname{diag}(1, 1 + \delta)$ with $\delta = 10^{-8}$ has the eigenvectors $e_1$ and $e_2$. Add $10^{-8}$ to both off-diagonal entries. For a real symmetric $2 \times 2$ matrix $\begin{pmatrix} a & b \\ b & c \end{pmatrix}$, the eigenvectors make the angle $\theta$ with the axes where $\tan 2\theta = 2b/(a - c)$. Here $|\tan 2\theta| = 2$, so the eigenvectors turn by $\theta = \tfrac12 \arctan 2 \approx 0.5536$ radians, about 31.7 degrees. The eigenvalues move by less than $10^{-8}$ (Weyl). The gap $\delta$ is as small as the perturbation, so the sin θ bound allows a turn of this size.

## Where it is used

- **Ranking.** PageRank and [eigenvector centrality](/eigenvector-centrality/) score the nodes of a graph by the entries of a dominant eigenvector, which [power iteration](/power-iteration/) computes.
- **Modes.** The vibration modes of a structure and the stationary states of a quantum system are eigenvectors. The stationary distribution of a Markov chain is a left eigenvector for the eigenvalue 1.
- **Principal components and clustering.** The principal directions of data are eigenvectors of the covariance matrix. Spectral clustering splits a graph by the signs of the eigenvector of the second smallest eigenvalue of its [Laplacian](/laplacian-matrix/).
- **Solving linear recurrences and ODEs.** With a basis of eigenvectors, $x_{k+1} = A x_k$ decouples into $n$ scalar recurrences, one for each coordinate in the eigenvector basis.
- **Algorithms.** [Inverse iteration](/inverse-iteration/) computes an eigenvector from a known eigenvalue; [deflation](/deflation/) uses a known eigenvector to remove its eigenvalue.

## References
