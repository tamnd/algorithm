---
tag: 6PA25Q
kind: technique
slug: rayleigh-ritz-method
name: Rayleigh-Ritz method
aliases:
- Ritz projection
- Rayleigh-Ritz procedure
- Galerkin projection for eigenproblems
area: numerical/eigenproblems
level: advanced
summary: Approximate eigenpairs of A from a subspace with orthonormal basis V by solving the small eigenproblem of V* A V. For Hermitian A the Ritz values are the best approximations the subspace allows.
prereqs: [rayleigh-quotient, spectral-theorem]
see_also: [lanczos-algorithm, arnoldi-iteration, subspace-iteration, courant-fischer-theorem, cauchy-interlacing-theorem, krylov-subspace, implicitly-restarted-arnoldi, symmetric-eigenproblem]
sources:
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 11, Approximations from a Subspace (the Rayleigh-Ritz procedure, its optimality and the error bounds for Ritz values and vectors)
  - book: isbn:9781611970722
    title: Yousef Saad, Numerical Methods for Large Eigenvalue Problems, revised edition, SIAM Classics in Applied Mathematics 66, 2011
    locator: Chapter 4, Section 4.3 (orthogonal projection methods, the Rayleigh-Ritz procedure and the a priori error bounds for Ritz vectors)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1.4 (Rayleigh-Ritz approximation for symmetric matrices) and Section 10.1 (Krylov subspaces and Ritz pairs)
  - book: isbn:9780898714715
    title: Zhaojun Bai, James Demmel, Jack Dongarra, Axel Ruhe and Henk van der Vorst (editors), Templates for the Solution of Algebraic Eigenvalue Problems, SIAM, 2000
    locator: Section 3.2 (projection methods, Ritz and harmonic Ritz values)
  - paper: "Walther Ritz, Über eine neue Methode zur Lösung gewisser Variationsprobleme der mathematischen Physik, Journal für die reine und angewandte Mathematik 135, 1909"
    title: Über eine neue Methode zur Lösung gewisser Variationsprobleme der mathematischen Physik
    locator: J. Reine Angew. Math. 135 (1909), pp. 1 to 61
---

The Rayleigh-Ritz method approximates some eigenpairs of a large matrix $A$ using a subspace $\mathcal S$ that is believed to contain good approximations to the wanted eigenvectors. With an orthonormal basis $V \in \mathbb C^{n \times k}$ of $\mathcal S$, it forms the small matrix $H = V^* A V$, solves $H y_i = \theta_i y_i$, and returns the Ritz values $\theta_i$ and Ritz vectors $x_i = V y_i$. The residual $A x_i - \theta_i x_i$ is orthogonal to $\mathcal S$, which is the Galerkin condition. For Hermitian $A$ the method is optimal in a precise sense: the Ritz values are the max-min values of the [Rayleigh quotient](/rayleigh-quotient/) restricted to $\mathcal S$, they interlace the eigenvalues, and $H$ minimizes $\|A V - V M\|$ over all $k \times k$ matrices $M$. Every subspace method for eigenvalues, from [subspace iteration](/subspace-iteration/) to [Lanczos](/lanczos-algorithm/), [Arnoldi](/arnoldi-iteration/) and Davidson, ends with this step.

## In plain words

Suppose a huge problem has a few answers we care about, and we have a small collection of directions that we think lie near them. Instead of solving the huge problem, we look at how the big table acts inside our small collection only. That gives a small table, which is easy to solve. Its answers, and the directions they point to back in the big space, are our approximations. If the collection really contains good directions, the approximations are good, and for symmetric tables they are the best that collection can give.

## When it applies

- A subspace $\mathcal S$ of dimension $k \ll n$ is available, built so that it nearly contains the wanted invariant subspace: a [Krylov subspace](/krylov-subspace/) $\mathcal K_k(A, b)$, the block of [subspace iteration](/subspace-iteration/), a search space expanded by corrections (Davidson, Jacobi-Davidson), or a space of trial functions in a variational problem.
- Products $A v$ for vectors $v$ are affordable, so $A V$ can be formed with $k$ products.
- The wanted eigenvalues are extreme (largest or smallest) for the standard method. Interior eigenvalues need the harmonic variant below.
- For Hermitian $A$ the guarantees are strongest; for non-Hermitian $A$ the method still works, but its Ritz values carry no interlacing or optimality guarantee.

## The template

**Notation.** $A \in \mathbb C^{n \times n}$, $\mathcal S$ a subspace of dimension $k$, $V \in \mathbb C^{n \times k}$ with $V^* V = I_k$ and range $\mathcal S$. For Hermitian $A$, $\lambda_1 \ge \dots \ge \lambda_n$ are its eigenvalues and $\theta_1 \ge \dots \ge \theta_k$ the Ritz values. $\rho(x) = x^* A x / x^* x$.

1. Orthonormalize the basis of $\mathcal S$ (Householder QR or Gram-Schmidt with reorthogonalization) to get $V$.
2. Compute $W = A V$ ($k$ matrix-vector products) and $H = V^* W$ ($2nk^2$ flops). For Hermitian $A$, symmetrize $H \leftarrow (H + H^*)/2$ to remove rounding asymmetry.
3. Solve the small dense eigenproblem $H Y = Y \Theta$ ($O(k^3)$ flops) by the [QR algorithm](/qr-algorithm/), or the symmetric solver when $A$ is Hermitian.
4. Form the Ritz vectors $X = V Y$ ($2nk^2$ flops) and the residuals $R = W Y - X \Theta$, with column norms $\|r_i\|_2$.
5. Accept the pairs with small residual norms; otherwise enlarge or improve $\mathcal S$ and repeat.

**Why it works (Hermitian $A$).**

- *Galerkin condition.* $V^*(A x_i - \theta_i x_i) = H y_i - \theta_i y_i = 0$, so $r_i \perp \mathcal S$, and $\theta_i = \rho(x_i)$.
- *Optimality.* For each $j \le k$, $\theta_j = \max_{\mathcal U \subseteq \mathcal S, \dim \mathcal U = j} \min_{x \in \mathcal U} \rho(x)$, the [Courant-Fischer](/courant-fischer-theorem/) value restricted to $\mathcal S$. Since restricting the outer maximum to subspaces of $\mathcal S$ can only lower it, $\theta_j \le \lambda_j$, and applying this to $-A$ gives $\theta_j \ge \lambda_{n-k+j}$. This is [Cauchy interlacing](/cauchy-interlacing-theorem/) for the compression $V^* A V$.
- *Best residual.* For every $M \in \mathbb C^{k \times k}$, $\|A V - V M\|_2 \ge \|A V - V H\|_2$, and the same holds in the Frobenius norm, because $A V - V M = (A V - V H) + V (H - M)$ and the two terms have orthogonal ranges ($V^*(AV - VH) = 0$).
- *Residual bounds.* There is an eigenvalue $\lambda$ of $A$ with $|\lambda - \theta_i| \le \|r_i\|_2$, and if $\theta_i$ is separated by $\delta$ from all other eigenvalues of $A$, $|\lambda - \theta_i| \le \|r_i\|_2^2 / \delta$ and $\sin\angle(x_i, v) \le \|r_i\|_2 / \delta$ for the corresponding eigenvector $v$ (Parlett Chapter 11).
- *A priori bound.* If $\epsilon = \sin\angle(v_j, \mathcal S)$ is the distance from an eigenvector to the subspace, then some Ritz vector $x$ satisfies $\sin\angle(v_j, x) \le \epsilon \sqrt{1 + \gamma^2 / \delta^2}$, where $\gamma = \|P A (I - P)\|_2$, $P = V V^*$, and $\delta$ is the distance from $\lambda_j$ to the other Ritz values (Saad 2011, Chapter 4). So a good subspace gives a good Ritz vector unless Ritz values crowd around $\lambda_j$.

## Classic examples

**A coordinate subspace.** For $A = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 4 \end{pmatrix}$, with eigenvalues $4.732051$, $3$, $1.267949$, and $\mathcal S = \operatorname{span}\{e_1, e_2\}$, $H = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$ has Ritz values $(5 \pm \sqrt 5)/2 = 3.618034$ and $1.381966$. They interlace: $3 \le 3.618034 \le 4.732051$ and $1.267949 \le 1.381966 \le 3$. The Ritz vectors are $(0.525731, 0.850651, 0)$ and $(0.850651, -0.525731, 0)$, and their residuals are $(0, 0, 0.850651)$ and $(0, 0, -0.525731)$, orthogonal to $\mathcal S$ as the Galerkin condition says. The residual bound holds: $|3.618034 - 3| = 0.618 \le 0.851$ and $|1.381966 - 1.267949| = 0.114 \le 0.526$.

**Lanczos and Arnoldi.** With $\mathcal S = \mathcal K_k(A, b)$ and the basis built by the [Arnoldi iteration](/arnoldi-iteration/), $H = V^* A V$ is the upper Hessenberg matrix $H_k$ that the iteration produces anyway, and for Hermitian $A$ it is the tridiagonal $T_k$ of the [Lanczos algorithm](/lanczos-algorithm/). The residual norm is then $|h_{k+1,k}| \, |e_k^* y_i|$, available without forming $x_i$.

**Subspace iteration.** After $j$ steps of [subspace iteration](/subspace-iteration/), a Rayleigh-Ritz step on the current block gives the eigenvalue estimates and rotates the basis toward the eigenvectors, which improves the convergence of the individual vectors.

**Ritz's variational method.** For a self-adjoint differential operator, $\mathcal S$ is spanned by trial functions, $H$ and the Gram matrix are integrals, and, read from the bottom, the interlacing says that the $j$-th smallest Ritz value is an upper bound for the $j$-th smallest eigenvalue of the operator. This is how the finite element method bounds vibration frequencies from above.

## Variations

- **Harmonic Rayleigh-Ritz.** For eigenvalues near a target $\tau$ inside the spectrum, impose $A x - \theta x \perp (A - \tau I) \mathcal S$ instead. This is Rayleigh-Ritz for $(A - \tau I)^{-1}$ on the subspace $(A - \tau I)\mathcal S$, without the inverse, and it gives harmonic Ritz values that avoid the spurious interior values of the standard method (Morgan 1991; Templates Section 3.2).
- **Refined Ritz vectors.** Keep $\theta_i$ but replace $x_i$ by the unit $x \in \mathcal S$ that minimizes $\|(A - \theta_i I) x\|_2$, a small SVD problem (Jia 1997).
- **Oblique projection.** For non-Hermitian $A$, two-sided methods take $W^* (A x - \theta x) = 0$ with a different left space, as in nonsymmetric Lanczos.
- **Generalized problems.** For $A x = \lambda B x$ with $B$ Hermitian positive definite, use a $B$-orthonormal $V$ and solve $V^* A V y = \theta y$, or with any basis solve the pencil $(V^* A V, V^* B V)$.
- **Block and restarted forms.** Thick restart and [implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/) keep selected Ritz vectors and discard the rest, which keeps $k$ bounded.

## Pitfalls

- **Spurious interior Ritz values.** For $A = \operatorname{diag}(-1, 0, 1)$ and $\mathcal S = \operatorname{span}\{(1, 0, 1)/\sqrt 2\}$, the only Ritz value is $0$, an eigenvalue of $A$, but the Ritz vector is orthogonal to the eigenvector $e_2$, and its residual norm is $1$. Always check residuals, and use harmonic Ritz values for interior eigenvalues.
- **A non-orthonormal basis.** If $V$ is not orthonormal, $V^* A V$ is the wrong matrix; either orthonormalize, or solve the pencil $(V^* A V, V^* V)$, which becomes ill conditioned as the basis degenerates. In Lanczos without reorthogonalization this loss of orthogonality produces copies of converged Ritz values.
- **Clusters.** When several Ritz values are close, individual Ritz vectors are poorly determined even if the subspace is excellent; only the invariant subspace of the cluster is accurate, by the gap term $\delta$ of the a priori bound.
- **Non-Hermitian matrices.** Ritz values need not converge monotonically, need not lie in any interval, and can be far from every eigenvalue when $A$ is far from normal; they lie in the field of values of $A$, which can be much larger than the convex hull of the spectrum.
- **Forgetting to symmetrize $H$.** Rounding makes $V^* A V$ slightly non-Hermitian; a nonsymmetric solver may then return tiny imaginary parts.

## Exercises

1. Show that $H = V^* A V$ minimizes $\|A V - V M\|_F$ over all $k \times k$ matrices $M$.
2. For Hermitian $A$, prove $\theta_1 \le \lambda_1$ and $\theta_k \ge \lambda_n$ directly from $\theta_1 = \max_{x \in \mathcal S} \rho(x)$.
3. Show that if $\mathcal S$ is an invariant subspace of $A$, the Ritz pairs are exact eigenpairs, and that every Ritz vector has a zero residual.
4. Show that for $\mathcal S = \mathcal K_n(A, b)$ of full dimension $n$, the Ritz values are the eigenvalues of $A$, and that for $\mathcal K_k(A, b)$ the Ritz values are the zeros of the degree $k$ polynomial that minimizes $\|p(A) b\|_2$ among monic polynomials.
5. Compute the harmonic Ritz value for $\tau = 0$ in the spurious example and check that it is not near $0$.

## References
