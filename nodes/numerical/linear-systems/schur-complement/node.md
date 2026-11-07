---
tag: 8SABPS
kind: concept
slug: schur-complement
name: Schur complement
aliases:
- Schur complement method
- block elimination
- substructuring
area: numerical/linear-systems
level: core
summary: The matrix D - C A^-1 B that appears when eliminating a block of a block matrix.
prereqs: [gaussian-elimination, determinant]
see_also: [lu-decomposition, cholesky-decomposition, woodbury-identity, domain-decomposition, multifrontal-method, nested-dissection, positive-definite-matrix, growth-factor]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 0.8.5, Schur complements and determinantal formulae; Section 0.7.3, the inverse of a partitioned matrix
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 13, Block LU Factorization (block LU, the Schur complement and the stability of block elimination); Chapter 9, the active submatrix of Gaussian elimination as a Schur complement
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Chapter 14, Domain Decomposition Methods (the Schur complement system for the interface unknowns and its preconditioning)
  - paper: doi:10.1017/S0962492904000212
    title: Michele Benzi, Gene H. Golub and Jörg Liesen, Numerical solution of saddle point problems, Acta Numerica 14, 2005
    locator: the Schur complement reduction of saddle point systems and Schur complement preconditioners
---

For a block matrix $M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$ with $A$ square and nonsingular, the *Schur complement of $A$ in $M$* is $M/A = S = D - C A^{-1} B$. It is what is left of the lower right block after the first block of unknowns has been eliminated. Every step of Gaussian elimination computes one, the determinant and the inverse of $M$ factor through it, and it is the reduced system solved by substructuring, by the multifrontal method and by Schur complement preconditioners.

## In plain words

Split the unknowns of a system into two groups. Use the first group of equations to write the first group of unknowns in terms of the second, and put that into the remaining equations. What you get is a smaller system in the second group alone, and its matrix is the Schur complement. Solve it, then go back and recover the first group. Gaussian elimination does this one unknown at a time. Doing it with large groups lets you split a big problem into pieces that only talk to each other through a small interface.

## The idea

**Notation.** $A \in \mathbb{R}^{p \times p}$, $B \in \mathbb{R}^{p \times q}$, $C \in \mathbb{R}^{q \times p}$, $D \in \mathbb{R}^{q \times q}$, and $S = D - C A^{-1} B \in \mathbb{R}^{q \times q}$. The general notation of this area is on the page [linear system solving](/linear-system-solving/).

**Block elimination.** The system $\begin{pmatrix} A & B \\ C & D \end{pmatrix}\begin{pmatrix} x_1 \\ x_2 \end{pmatrix} = \begin{pmatrix} b_1 \\ b_2 \end{pmatrix}$ gives $x_1 = A^{-1}(b_1 - B x_2)$ from the first block row, and then

$$S\, x_2 = b_2 - C A^{-1} b_1.$$

In matrix form this is the block LDU factorization

$$M = \begin{pmatrix} I & 0 \\ C A^{-1} & I \end{pmatrix}\begin{pmatrix} A & 0 \\ 0 & S \end{pmatrix}\begin{pmatrix} I & A^{-1} B \\ 0 & I \end{pmatrix},$$

which can be checked by multiplying out. Three consequences follow at once.

- **Determinant.** $\det M = \det A \cdot \det S$.
- **Invertibility and inverse.** $M$ is nonsingular if and only if $S$ is, and then
$$M^{-1} = \begin{pmatrix} A^{-1} + A^{-1} B S^{-1} C A^{-1} & -A^{-1} B S^{-1} \\ -S^{-1} C A^{-1} & S^{-1} \end{pmatrix}.$$
In particular the lower right block of $M^{-1}$ is $S^{-1}$. Comparing this with the inverse computed from the Schur complement of $D$ (when $D$ is nonsingular) gives the [Woodbury identity](/woodbury-identity/).
- **Inertia.** If $M$ is symmetric ($C = B^T$), the factorization is a congruence, so by Sylvester's law of inertia $M$ has as many positive, negative and zero eigenvalues as $A$ and $S$ together (Haynsworth's inertia formula). Hence $M$ is [positive definite](/positive-definite-matrix/) if and only if $A$ and $S$ both are.

**Gaussian elimination computes Schur complements.** After $k$ steps of Gaussian elimination without pivoting, the active $(n-k) \times (n-k)$ submatrix is exactly the Schur complement of the leading $k \times k$ block $A_{11}$ of $A$. So the pivots are $u_{kk} = \det A_{1:k,1:k}/\det A_{1:k-1,1:k-1}$, and the [growth factor](/growth-factor/) measures how large these Schur complements become. Classes closed under Schur complements are the classes on which elimination without pivoting is safe: symmetric positive definite matrices (and $\|S\|_2 \le \|D\|_2$, $\lambda_{\min}(S) \ge \lambda_{\min}(M)$), matrices diagonally dominant by columns, M-matrices and totally nonnegative matrices.

**Quotient formula.** If $A$ is a leading block of $E$, which is a leading block of $M$, then $M/E = (M/A)/(E/A)$ (Crabtree and Haynsworth, 1969). This is why eliminating unknowns in groups gives the same result as eliminating them one at a time.

**In floating point.** Block LU computes $S$ by solving with a factorization of $A$ and a matrix product; Higham (Chapter 13) shows that block LU without pivoting inside the blocks is stable for matrices that are block diagonally dominant or symmetric positive definite, but can be unstable in general even when point LU with partial pivoting is fine. Forming $S$ explicitly also loses sparsity: $S$ is usually dense even when $A$, $B$, $C$, $D$ are sparse.

## Examples

**A $3 \times 3$ matrix.** Take

$$M = \begin{pmatrix} 2 & 1 & 1 \\ 1 & 2 & 0 \\ 1 & 0 & 3 \end{pmatrix}, \quad A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}, \quad B = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad C = B^T, \quad D = (3).$$

$A^{-1} = \tfrac13 \begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$, so $C A^{-1} B = 2/3$ and $S = 3 - 2/3 = 7/3$. Then $\det M = \det A \cdot S = 3 \cdot \tfrac73 = 7$, which agrees with direct expansion, and $(M^{-1})_{33} = 3/7$. Since $A$ is positive definite and $S > 0$, $M$ is positive definite. Eliminating $x_1$ and then $x_2$ by Gaussian elimination gives pivots $2$, $3/2$ and $7/3$; the last pivot is $S$.

**The $2 \times 2$ case.** For $M = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ with $a \ne 0$, $S = d - c b/a$, and $\det M = a S = a d - b c$. With $a = \varepsilon$ tiny and $b = c = d = 1$, $S = 1 - 1/\varepsilon$ is huge: a large Schur complement is exactly the growth that [partial pivoting](/partial-pivoting/) avoids.

**Substructuring.** Number the unknowns of a discretized PDE so that the interior unknowns of two subdomains come first and the interface unknowns last. Then $A = \operatorname{diag}(A_1, A_2)$ is block diagonal, and $S = D - C_1 A_1^{-1} B_1 - C_2 A_2^{-1} B_2$ couples only the interface. Each subdomain contributes its own term, computed independently; this is the starting point of [domain decomposition](/domain-decomposition/) and of [nested dissection](/nested-dissection/).

**Gaussian conditioning.** If $(X, Y)$ is jointly Gaussian with covariance $\begin{pmatrix} \Sigma_{XX} & \Sigma_{XY} \\ \Sigma_{YX} & \Sigma_{YY} \end{pmatrix}$, the conditional covariance of $Y$ given $X$ is the Schur complement $\Sigma_{YY} - \Sigma_{YX}\Sigma_{XX}^{-1}\Sigma_{XY}$.

## Where it is used

- **Direct solvers.** Block LU, the [multifrontal method](/multifrontal-method/) (each frontal matrix is partially factored and its Schur complement, the update matrix, is passed to the parent), and supernodal Cholesky all work with Schur complements.
- **Domain decomposition.** Iterative substructuring solves the interface system $S x_\Gamma = g$ by a Krylov method, applying $S$ through subdomain solves without forming it (Saad, Chapter 14).
- **Saddle point systems.** For $\begin{pmatrix} A & B^T \\ B & 0 \end{pmatrix}$, the Schur complement $-B A^{-1} B^T$ gives the pressure equation in fluid flow, and an approximation of it gives block preconditioners (Benzi, Golub and Liesen, 2005).
- **Updating formulas.** The [Sherman-Morrison formula](/sherman-morrison-formula/) and the [Woodbury identity](/woodbury-identity/) are two ways of writing the inverse of the same bordered matrix.
- **Proofs.** Induction on the order through the Schur complement proves the existence of Cholesky and LU factorizations, determinant identities, and the interlacing of eigenvalues of bordered matrices.

## References
