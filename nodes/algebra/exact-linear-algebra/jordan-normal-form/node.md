---
tag: A91GSV
kind: problem
slug: jordan-normal-form
name: Jordan normal form
aliases:
- Jordan canonical form
- Jordan form
- Jordan decomposition of a matrix
area: algebra/exact-linear-algebra
level: advanced
summary: Find a similarity transformation that puts a matrix into block-diagonal Jordan blocks.
prereqs: [characteristic-polynomial, eigenvalue, rank-computation]
see_also: [rational-canonical-form, matrix-minimal-polynomial, characteristic-polynomial-computation, cayley-hamilton-theorem, eigenvalue, rank-computation, nullspace, smith-normal-form]
sources:
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition
    locator: Chapter 7, Section 7.3, The Jordan form; Section 7.4, Computation of invariant factors
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition
    locator: Chapter 3, Section 3.1, The Jordan canonical form theorem (with the rank formula for the number of blocks of each size)
  - paper: "Mark Giesbrecht, Nearly optimal algorithms for canonical matrix forms, SIAM Journal on Computing 24(5), 1995"
    locator: pp. 948 to 969 (Las Vegas algorithms for the Frobenius and Jordan forms and their transforms with about n^ω field operations, given the factorization of the characteristic polynomial)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: the chapters on the Frobenius form (deterministic computation of the Frobenius form, from which the Jordan form follows by factoring the invariant factors)
  - paper: "Gene H. Golub and James H. Wilkinson, Ill-conditioned eigensystems and the computation of the Jordan canonical form, SIAM Review 18(4), 1976"
    locator: pp. 578 to 619 (why the Jordan form cannot be computed reliably in floating point)
  - book: "Camille Jordan, Traite des substitutions et des equations algebriques, Gauthier-Villars, Paris, 1870"
    locator: the canonical form of a linear substitution (the form now named after Jordan)
---

The Jordan normal form of a square matrix $A$ over an algebraically closed field is a block diagonal matrix $J = P^{-1} A P$ made of Jordan blocks, each an eigenvalue $\lambda$ on the diagonal with ones just above it. It is unique up to the order of the blocks, so two matrices are similar exactly when they have the same Jordan form. The problem is to find $J$, and often also the transformation $P$, exactly. The eigenvalues come from the [characteristic polynomial](/characteristic-polynomial/), and the sizes of the blocks come from the ranks of the powers $(A - \lambda I)^k$. The hard parts are elsewhere: the eigenvalues may need an extension field, and in floating point the form is not continuous in the entries, so it is a problem for exact arithmetic.

Notation: $K$ is a field and $\bar K$ an algebraic closure, $A$ is an $n \times n$ matrix over $K$, and $J_k(\lambda)$ is the $k \times k$ Jordan block with $\lambda$ on the diagonal, $1$ on the superdiagonal and $0$ elsewhere. $r_k(\lambda) = \operatorname{rank}(A - \lambda I)^k$, with $r_0(\lambda) = n$. $\omega$ is the exponent of matrix multiplication. Costs are counted in operations of the field in which the eigenvalues lie.

## In plain words

A square table of numbers acts on vectors, and most of its action can be split into simple pieces. Each piece either stretches some directions by a fixed factor, or stretches them and also shifts each direction a little into the next one, like a chain. The Jordan form lists these pieces: one block per chain, with the stretch factor on the diagonal and ones next to it for the shifts. Two tables describe the same action in different coordinates exactly when they have the same list of pieces. The task is to find that list, and the change of coordinates, without rounding errors.

## Definition

**Input:** an $n \times n$ matrix $A$ over a field $K$, for example $\mathbb{Q}$ or a finite field.

**Output:** the list of Jordan blocks, as pairs $(\lambda, k)$ of an eigenvalue $\lambda \in \bar K$ and a size $k \ge 1$, with $\sum k = n$, such that $A = P J P^{-1}$ with $J = J_{k_1}(\lambda_1) \oplus \cdots \oplus J_{k_s}(\lambda_s)$, for some invertible $P$ over $\bar K$. Often $P$ is also required. Eigenvalues that are not in $K$ are given as roots of irreducible factors of $\chi_A$ over $K$, that is as elements of a finite extension of $K$.

**Theorem (Jordan).** If $\chi_A$ splits into linear factors over $K$, then $A = PJP^{-1}$ for a Jordan matrix $J$ and an invertible $P$ over $K$, and $J$ is unique up to the order of the blocks. For each eigenvalue $\lambda$, the number of blocks $J_k(\lambda)$ of size at least $k$ is

$$
r_{k-1}(\lambda) - r_k(\lambda),
$$

so the number of blocks of size exactly $k$ is $r_{k-1}(\lambda) - 2r_k(\lambda) + r_{k+1}(\lambda)$.

*Why the rank formula holds.* Ranks do not change under similarity, so compute them on $J$. For a block $J_k(\mu)$ with $\mu \ne \lambda$, $J_k(\mu) - \lambda I$ is invertible and all its powers have rank $k$. For a block $J_k(\lambda)$, $N = J_k(\lambda) - \lambda I$ is the shift matrix, and $N^j$ has rank $\max(k - j, 0)$. So $r_{j-1}(\lambda) - r_j(\lambda)$ counts one for each block $J_k(\lambda)$ with $k \ge j$, and nothing for the others. Existence is proved with the primary decomposition and cyclic subspaces (Hoffman and Kunze, Section 7.3). $\square$

Three numbers per eigenvalue follow: the *algebraic multiplicity* (the exponent of $x - \lambda$ in $\chi_A$) is the total size of its blocks, the *geometric multiplicity* $n - r_1(\lambda)$ is the number of its blocks, and the exponent of $x - \lambda$ in the [minimal polynomial](/matrix-minimal-polynomial/) is the size of its largest block. $A$ is diagonalizable exactly when all blocks have size $1$.

Karl Weierstrass introduced elementary divisors in 1868 to classify pencils of bilinear forms, which gives the Jordan form over $\mathbb{C}$ in another language. Camille Jordan published the canonical form in 1870, in his treatise on substitutions, for linear substitutions over finite fields. Fast exact algorithms came with the Frobenius form, through the work of Giesbrecht and of Storjohann in the 1990s.

## Variants

- **Only the Jordan structure.** Output the eigenvalues and the block sizes but not $P$. This is the similarity invariant, and it is equivalent to the list of *elementary divisors* $(x - \lambda)^k$.
- **With the transformation.** Output $P$ as well, whose columns are Jordan chains $v, (A - \lambda I)v, \dots$ of generalized eigenvectors. This is harder, and the entries of $P$ can be much larger than those of $A$.
- **Without leaving $K$.** When $\chi_A$ does not split over $K$, the *primary rational form* (generalized Jordan form) uses blocks built from companion matrices of powers $p(x)^e$ of irreducible factors $p$ of $\chi_A$; it has entries in $K$ and carries the same information. The [rational canonical form](/rational-canonical-form/) (Frobenius form) groups the elementary divisors into invariant factors.
- **Nilpotent matrices.** If $A^n = 0$, the only eigenvalue is $0$ and the form is a partition of $n$, read from the ranks of $A, A^2, \dots$.
- **Numerical Jordan form.** In floating point, a tiny perturbation of a matrix with a block of size $k \ge 2$ splits the block into $k$ distinct eigenvalues, so the question is replaced by staircase or Schur forms with a tolerance (Golub and Wilkinson 1976). This is a different problem.

## Examples

- $\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix} = J_2(0)$ is already in Jordan form. It is not diagonalizable: its only eigenvalue is $0$ with geometric multiplicity $1$ and algebraic multiplicity $2$.
- The integer matrix

  $$
  A = \begin{pmatrix} 1 & 2 & -2 & 1 \\ 0 & 2 & 0 & 0 \\ -1 & 1 & 1 & 1 \\ -3 & 4 & -4 & 5 \end{pmatrix}
  $$

  has $\chi_A(x) = x^4 - 9x^3 + 30x^2 - 44x + 24 = (x - 2)^3 (x - 3)$. For $\lambda = 2$, the ranks of $(A - 2I)^k$ for $k = 1, 2, 3$ are $2, 1, 1$. So there are $4 - 2 = 2$ blocks for the eigenvalue $2$, of which $2 - 1 = 1$ has size at least $2$ and $1 - 1 = 0$ have size at least $3$. For $\lambda = 3$, $\operatorname{rank}(A - 3I) = 3$, one block. Hence $J = J_2(2) \oplus J_1(2) \oplus J_1(3)$, and the minimal polynomial is $(x - 2)^2 (x - 3)$. The matrix was built as $PJP^{-1}$ with $P$ having rows $(1, 1, 0, 0)$, $(0, 1, 1, 0)$, $(0, 0, 1, 1)$, $(1, 0, 0, 2)$, and a script checked the ranks and the polynomials.
- $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$ has $\chi_M = (x - 3)(x^2 - 6x + 6)$, with three distinct eigenvalues $3$ and $3 \pm \sqrt 3$. Its Jordan form is diagonal, over $\mathbb{Q}(\sqrt 3)$ but not over $\mathbb{Q}$.
- The rotation $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ has no Jordan form over $\mathbb{R}$, since $\chi = x^2 + 1$ has no real root. Over $\mathbb{C}$ it is $J_1(i) \oplus J_1(-i)$.
- Over $\mathbb{F}_2$, $\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix} = J_2(1)$ is its own Jordan form, while the matrix with rows $(1, 1)$, $(1, 0)$ has $\chi = x^2 + x + 1$, irreducible over $\mathbb{F}_2$. Its Jordan form is diagonal over $\mathbb{F}_4$, with the two roots of $x^2 + x + 1$.

## Known algorithms

| Method | Cost | Notes |
| --- | --- | --- |
| Factor $\chi_A$, then the ranks $r_k(\lambda)$ | $O(n^3)$ per rank, at most $n$ ranks in all, so $O(n^4)$, or $O(n^{\omega+1})$ | arithmetic in the field of each eigenvalue; gives the structure only |
| Jordan chains from kernels of $(A - \lambda I)^k$ | $O(n^4)$ | gives $P$; chains must be chosen to fit together |
| Frobenius form, then factoring the invariant factors | $O(n^\omega)$ Las Vegas (Giesbrecht 1995), plus the factorization | stays in $K$ until the factorization |
| Storjohann's deterministic Frobenius form | about $n^\omega$ up to logarithmic factors | then the same factorization step |
| Modular methods over $\mathbb{Q}$ | Frobenius form modulo primes, lifted or combined | the structure of $A \bmod p$ equals that of $A$ for all but finitely many primes |

The steps outside linear algebra are the factorization of $\chi_A$ (or of the invariant factors) over $K$, which runs in polynomial time over $\mathbb{Q}$ by lattice reduction and in randomized polynomial time over finite fields, and arithmetic in the extension fields generated by the eigenvalues. A Jordan structure algorithm needs the ranks only for the distinct eigenvalues, and only up to the size of the largest block, which is usually small. For a matrix with integer entries, the number of distinct eigenvalues and their multiplicities can be read from the squarefree factorization of $\chi_A$ and the Frobenius form without computing any root.

## Bounds

- **Cost of the structure.** Given the factorization of $\chi_A$, the Jordan structure costs $O(n^\omega)$ field operations up to logarithmic factors, by the Frobenius form. It is at least as hard as the [rank](/rank-computation/) of a matrix, of any matrix: for an $m \times n$ matrix $C$, the block matrix $A = \begin{pmatrix} 0 & C \\ 0 & 0 \end{pmatrix}$ has $A^2 = 0$, and its number of Jordan blocks of size $2$ is $\operatorname{rank} A = \operatorname{rank} C$.
- **Discontinuity.** The form is not a continuous function of the entries. $\begin{pmatrix} 0 & 1 \\ \varepsilon & 0 \end{pmatrix}$ has the eigenvalues $\pm\sqrt\varepsilon$ and a diagonal Jordan form for every $\varepsilon \ne 0$, but $J_2(0)$ for $\varepsilon = 0$. So no algorithm with rounded arithmetic can compute it reliably; the eigenvalues of a block of size $k$ move by about $\varepsilon^{1/k}$.
- **Size of the transform.** Even over $\mathbb{Q}$ with all eigenvalues rational, $P$ can have entries much larger than those of $A$, because the chain vectors solve linear systems with $(A - \lambda I)^k$, and their size is bounded through [Cramer's rule](/cramers-rule/) and the [Hadamard bound](/hadamard-bound/) of those powers.

## Reductions

- **Similarity testing.** $A$ and $B$ are similar over $\bar K$ iff they have the same Jordan structure. Over $K$ itself, similarity is decided by the Frobenius forms, which avoids extension fields; the two answers agree, because similarity over $\bar K$ implies similarity over $K$.
- **From the Smith form of $xI - A$.** The invariant factors of the polynomial matrix $xI - A$ over $K[x]$, from its [Smith normal form](/smith-normal-form/), factor into the elementary divisors $(x - \lambda)^k$, which are the Jordan blocks.
- **Minimal and characteristic polynomials.** $\chi_A = \prod (x - \lambda_i)^{k_i}$ over all blocks, and $\mu_A = \prod_\lambda (x - \lambda)^{\max k}$. So the Jordan form gives both, and the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) is visible block by block.
- **Eigenvectors.** The kernel of $A - \lambda I$, a [nullspace](/nullspace/) computation, has one vector per block, the first vector of each chain.

## Applications

- **Functions of matrices.** $f(J_k(\lambda))$ is the upper triangular Toeplitz matrix with entries $f(\lambda), f'(\lambda), f''(\lambda)/2!, \dots$ on its diagonals, so powers $A^t$, the exponential $e^{tA}$ and other functions have closed forms. The solutions of $x' = Ax$ and of linear recurrences are polynomials times exponentials, with degrees given by the block sizes.
- **Classification.** The Jordan form describes all linear maps up to change of basis, and the similarity classes of nilpotent matrices are the partitions of $n$.
- **Stability of discrete systems.** $A^t \to 0$ iff all eigenvalues have absolute value less than $1$, and $A^t$ stays bounded iff in addition the eigenvalues of absolute value $1$ have only blocks of size $1$.
- **Computer algebra.** Exact Jordan forms of matrices with rational or symbolic entries are standard functions of computer algebra systems, which compute them through the characteristic polynomial, its factorization and rank computations, or through the Frobenius form.

## References
