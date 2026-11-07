---
tag: 47MH9H
kind: concept
slug: eigenvalue
name: Eigenvalue
aliases:
- characteristic value
- proper value
- characteristic root
- latent root
area: numerical/eigenproblems
level: intro
summary: A scalar λ for which A − λI is singular, so that A v = λ v for some nonzero vector v. The n eigenvalues of an n by n matrix are the roots of its characteristic polynomial.
prereqs: [characteristic-polynomial, determinant]
see_also: [eigenvector, eigenvalue-problem, diagonalization, gershgorin-circle-theorem, eigenvalue-condition-number, spectral-radius, jordan-normal-form, schur-decomposition]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Chapter 1, Sections 1.1 (eigenvalues and eigenvectors) and 1.2 (the characteristic polynomial and algebraic multiplicity)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.1, Properties and Decompositions
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 24 (Eigenvalue Problems) and Lecture 25 (Overview of Eigenvalue Algorithms, why eigenvalue algorithms must be iterative)
---

An eigenvalue of a square matrix $A \in \mathbb{C}^{n \times n}$ is a scalar $\lambda \in \mathbb{C}$ for which $A - \lambda I$ is singular, so that $A v = \lambda v$ for some nonzero vector $v$, an [eigenvector](/eigenvector/). The eigenvalues are the roots of the [characteristic polynomial](/characteristic-polynomial/) $p_A(t) = \det(tI - A)$, so an $n \times n$ matrix has exactly $n$ eigenvalues when they are counted with multiplicity. Their set is the spectrum $\Lambda(A)$. Numerical methods find eigenvalues without the characteristic polynomial, because its roots are much more sensitive to rounding than the eigenvalues themselves.

## In plain words

A matrix acts on vectors: it turns and stretches them. For most vectors the result points in a new direction. A few special directions are only stretched, shrunk or flipped, and keep their line. The stretch factor along such a direction is an eigenvalue. A factor of two means that the matrix doubles each vector on that line. A factor of minus one means that it flips them. A factor of zero means that it crushes them to nothing, so the matrix cannot be undone.

The eigenvalues tell you what the matrix does when you apply it again and again. If every factor is smaller than one in size, repeated products shrink to zero. If one factor is larger than one, they blow up along its direction. This is why eigenvalues decide the stability of systems that evolve step by step.

## The idea

**Definition.** Let $A \in \mathbb{C}^{n \times n}$. A number $\lambda \in \mathbb{C}$ is an eigenvalue of $A$ if there is a $v \in \mathbb{C}^n$, $v \neq 0$, with $A v = \lambda v$. The following are equivalent for $\lambda \in \mathbb{C}$: (a) $\lambda$ is an eigenvalue; (b) $A - \lambda I$ has a nonzero null vector; (c) $A - \lambda I$ is singular; (d) $\det(\lambda I - A) = 0$. The step from (c) to (d) is the fact that a matrix is singular if and only if its [determinant](/determinant/) is zero.

**Counting.** The characteristic polynomial $p_A(t) = \det(tI - A)$ is monic of degree $n$, so over $\mathbb{C}$ it factors as $p_A(t) = \prod_{i=1}^{n} (t - \lambda_i)$. The list $\lambda_1, \dots, \lambda_n$ is the spectrum with multiplicity. The *algebraic multiplicity* of $\mu$ is the number of $i$ with $\lambda_i = \mu$. The *geometric multiplicity* of $\mu$ is $\dim \operatorname{null}(A - \mu I)$, the number of independent eigenvectors for $\mu$.

**Geometric multiplicity is at most algebraic multiplicity.** Let $g$ be the geometric multiplicity of $\mu$ and let $v_1, \dots, v_g$ be a basis of $\operatorname{null}(A - \mu I)$. Extend it to a basis of $\mathbb{C}^n$ and let $S$ have these vectors as columns. Then $S^{-1} A S = \begin{pmatrix} \mu I_g & B \\ 0 & C \end{pmatrix}$, because the first $g$ columns of $AS$ are $\mu v_1, \dots, \mu v_g$. Similar matrices have the same characteristic polynomial ($\det(tI - S^{-1}AS) = \det(S^{-1}(tI - A)S) = \det(tI - A)$), and the block triangular form gives $p_A(t) = (t - \mu)^g \det(tI - C)$. So $(t - \mu)^g$ divides $p_A$, and the algebraic multiplicity is at least $g$. A matrix where the two multiplicities differ for some eigenvalue is *defective*; it has no basis of eigenvectors and no [diagonalization](/diagonalization/).

**Trace and determinant.** $\sum_i \lambda_i = \operatorname{tr} A$ and $\prod_i \lambda_i = \det A$. *Proof.* At $t = 0$, $p_A(0) = \det(-A) = (-1)^n \det A$, and the product form gives $\prod (-\lambda_i) = (-1)^n \prod \lambda_i$. For the coefficient of $t^{n-1}$, expand $\det(tI - A)$ by the Leibniz formula. A permutation other than the identity moves at least two indices, so its term has at most $n - 2$ diagonal factors and degree at most $n - 2$ in $t$. So the coefficient of $t^{n-1}$ comes only from $\prod_i (t - a_{ii})$, and it is $-\operatorname{tr} A$. In the product form it is $-\sum \lambda_i$. $\square$ These two identities are cheap checks on any computed spectrum.

**Facts used on every page of this area.** Each follows from the definition in one or two lines.

- Similar matrices $S^{-1} A S$ and $A$ have the same eigenvalues with the same multiplicities (shown above). Every algorithm in this area applies [similarity transformations](/similarity-transformation/) until the eigenvalues can be read off.
- The eigenvalues of a triangular matrix are its diagonal entries, since $\det(tI - T) = \prod (t - t_{ii})$. The [Schur decomposition](/schur-decomposition/) $A = Q T Q^*$ with $Q$ unitary and $T$ upper triangular exists for every square matrix, so the eigenvalues are always the diagonal of some unitarily similar triangular matrix.
- If $A v = \lambda v$, then $A^k v = \lambda^k v$, $(A - \sigma I) v = (\lambda - \sigma) v$, and, when $A$ is nonsingular, $A^{-1} v = \lambda^{-1} v$. More generally $q(A)$ has eigenvalues $q(\lambda_i)$ for each polynomial $q$. Shifts and inverses are the base of [inverse iteration](/inverse-iteration/) and of the shifted QR algorithm.
- A real matrix has a real characteristic polynomial, so its nonreal eigenvalues come in conjugate pairs $\lambda, \bar\lambda$.
- A Hermitian matrix ($A = A^*$) has real eigenvalues: from $A v = \lambda v$, $\lambda \, v^* v = v^* A v = (A v)^* v = \bar\lambda \, v^* v$, and $v^* v > 0$.
- For each induced matrix norm, $|\lambda| \le \|A\|$: take norms in $A v = \lambda v$. So the [spectral radius](/spectral-radius/) $\max_i |\lambda_i|$ is at most $\|A\|$. The [Gershgorin circle theorem](/gershgorin-circle-theorem/) gives finer regions from the entries.

**Ordering.** The pages of this area order the eigenvalues as follows. For a general matrix, $|\lambda_1| \ge |\lambda_2| \ge \dots \ge |\lambda_n|$; for power-type methods the ratio $|\lambda_2 / \lambda_1|$ governs convergence. For a Hermitian or real symmetric matrix, the eigenvalues are real and $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$.

**Why eigenvalue algorithms iterate.** Each monic polynomial $t^n + c_{n-1} t^{n-1} + \dots + c_0$ is the characteristic polynomial of its companion matrix. So a finite formula in radicals for the eigenvalues of every $5 \times 5$ matrix would give one for the roots of every quintic, which the [Abel-Ruffini theorem](/abel-ruffini-theorem/) rules out. Hence every general eigenvalue algorithm for $n \ge 5$ is iterative, and it stops when the error is below the rounding level (Trefethen and Bau, Lecture 25). The reverse direction is used in practice: polynomial root finders such as MATLAB's `roots` compute the eigenvalues of the companion matrix.

**Why not through the characteristic polynomial.** Computing the coefficients of $p_A$ and then their roots is a poor method in floating point. The roots of a polynomial can be very sensitive to its coefficients even when the eigenvalues are well conditioned functions of the entries of $A$. Wilkinson's example is $\prod_{k=1}^{20} (t - k)$: a change of $2^{-23}$ in the coefficient of $t^{19}$ moves several roots into the complex plane. The diagonal matrix $\operatorname{diag}(1, \dots, 20)$ has the same characteristic polynomial, yet for each perturbation $E$, each eigenvalue of $\operatorname{diag}(1, \dots, 20) + E$ lies within $\|E\|_2$ of one of the numbers $1, \dots, 20$, by the [Bauer-Fike theorem](/bauer-fike-theorem/) for a normal matrix.

## Examples

**A 2 by 2 matrix.** $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$ has $p_A(t) = t^2 - 7t + 10 = (t - 5)(t - 2)$. The eigenvalues are 5 and 2, with eigenvectors $(1, 1)^T$ and $(1, -2)^T$: $A (1, -2)^T = (2, -4)^T$. The checks hold: $5 + 2 = 7 = \operatorname{tr} A$ and $5 \cdot 2 = 10 = \det A$.

**A rotation.** $A = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ turns the plane by a quarter turn, so no real direction keeps its line. Here $p_A(t) = t^2 + 1$ and the eigenvalues are the conjugate pair $\pm i$. The two have equal modulus, which is the case where [power iteration](/power-iteration/) does not converge.

**A defective matrix.** The Jordan block $J = \begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}$ has the eigenvalue 2 with algebraic multiplicity 2 and geometric multiplicity 1: $\operatorname{null}(J - 2I)$ is spanned by $e_1$ alone. Change the $(2,1)$ entry from 0 to $\varepsilon > 0$: then $p(t) = (t - 2)^2 - \varepsilon$ and the eigenvalues are $2 \pm \sqrt{\varepsilon}$. For $\varepsilon = 10^{-10}$ they move by $10^{-5}$, a hundred thousand times the change in the entry. Defective eigenvalues are the extreme case of the [eigenvalue condition number](/eigenvalue-condition-number/); see the [Jordan normal form](/jordan-normal-form/).

**A matrix with a known spectrum.** The tridiagonal Toeplitz matrix of order $n$ with 2 on the diagonal and $-1$ on the two next diagonals has eigenvalues $2 - 2\cos(k\pi/(n+1))$ for $k = 1, \dots, n$, with eigenvectors $(\sin(jk\pi/(n+1)))_{j=1}^n$. For $n = 4$ they are about $0.381966$, $1.381966$, $2.618034$ and $3.618034$, and they add up to $8 = \operatorname{tr} A$. This matrix is the second difference operator, and it is a standard test case for the algorithms of this area.

**Zero and the identity.** The zero matrix has the single eigenvalue 0 with both multiplicities $n$; every nonzero vector is an eigenvector. A matrix is singular if and only if 0 is one of its eigenvalues.

## Where it is used

- **Stability of dynamical systems.** The solutions of $x' = A x$ decay to zero for every start if and only if every eigenvalue has negative real part. The iteration $x_{k+1} = A x_k$ decays if and only if the spectral radius is below 1. The convergence of [stationary iterative methods](/matrix-splitting/) for linear systems is a statement about a spectral radius.
- **Vibration and quantum mechanics.** The natural frequencies of a structure are square roots of eigenvalues of a [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $K x = \lambda M x$. The energy levels of a quantum system are the eigenvalues of its Hamiltonian.
- **Data analysis.** Principal component analysis uses the largest eigenvalues of a covariance matrix, which are the squares of the largest [singular values](/singular-value-decomposition/) of the centered data matrix.
- **Graphs and Markov chains.** The eigenvalues of the [Laplacian matrix](/laplacian-matrix/) measure how well a graph is connected. The stationary distribution of a Markov chain is an eigenvector for the eigenvalue 1, and the second eigenvalue sets the speed of mixing.
- **Condition and norms.** The 2-norm of $A$ is the square root of the largest eigenvalue of $A^* A$, and the 2-norm [condition number](/condition-number/) uses the largest and the smallest of these.

## References
