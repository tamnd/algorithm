---
tag: TKPRJX
kind: algorithm
slug: schur-method-riccati
name: Schur method for Riccati equations
aliases:
- Laub's Schur method
area: control/optimal-and-predictive-control
level: advanced
summary: Solves the algebraic Riccati equation from an ordered real Schur form of the Hamiltonian matrix, whose first n Schur vectors span its stable subspace.
solves: [continuous-algebraic-riccati-equation, discrete-algebraic-riccati-equation]
model: floating-point-model
complexity:
  vars: {n: the number of states, c: the largest number of QR steps spent on one eigenvalue}
  time: {typical: "O(n^3)", worst: "O(c n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, recursive: false, iterative: true}
history:
  year: 1979
  people: [Alan J. Laub]
  note: "Laub (1979) proposed to compute the stabilizing solution from an ordered real Schur form of the Hamiltonian matrix, in place of its eigenvectors."
prereqs: [continuous-algebraic-riccati-equation, hamiltonian-matrix, schur-decomposition, qr-algorithm]
see_also: [stabilizing-riccati-solution-theorem, kleinman-iteration, infinite-horizon-lqr, givens-rotations, wilkinson-shift, hessenberg-reduction, qz-algorithm, backward-error-analysis]
sources:
  - paper: doi:10.1109/TAC.1979.1102178
    title: Alan J. Laub, A Schur method for solving algebraic Riccati equations, IEEE Transactions on Automatic Control 24(6), 913-921, 1979
    locator: the method, the ordered real Schur form of the Hamiltonian matrix and the discrete-time version
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Chapter 7, on the QR iteration, the Schur form and the reordering of eigenvalues
  - paper: doi:10.1016/0024-3795(81)90086-0
    title: Chris Paige and Charles Van Loan, A Schur decomposition for Hamiltonian matrices, Linear Algebra and its Applications 41, 11-32, 1981
    locator: the Hamiltonian Schur form and its relation to the Riccati equation
  - book: isbn:9780198537953
    title: Peter Lancaster and Leiba Rodman, Algebraic Riccati Equations, Clarendon Press, Oxford, 1995
    locator: the description of solutions by invariant subspaces of the Hamiltonian matrix
  - book: isbn:9781611972085
    title: Dario A. Bini, Bruno Iannazzo and Beatrice Meini, Numerical Solution of Algebraic Riccati Equations, SIAM, 2012
    locator: the chapter on Schur methods and the comparison with Newton and doubling methods
---

The Schur method solves the [continuous algebraic Riccati equation](/continuous-algebraic-riccati-equation/) (CARE) $A^T P + P A - P B R^{-1} B^T P + Q = 0$ for its stabilizing solution. It forms the $2n \times 2n$ [Hamiltonian matrix](/hamiltonian-matrix/) $H$, computes a [Schur decomposition](/schur-decomposition/) $Z^* H Z = T$ with a unitary $Z$, and reorders it so that the $n$ eigenvalues with negative real part come first. The first $n$ columns of $Z$ then span the stable invariant subspace of $H$, and if they are split as $\begin{bmatrix} U_1 \\ U_2 \end{bmatrix}$, the solution is $P = U_2 U_1^{-1}$. Laub (1979) introduced the method with the real Schur form, which has $2 \times 2$ blocks for complex pairs. The implementation on this page uses the complex Schur form, which has only $1 \times 1$ blocks. A variant with a symplectic matrix solves the [discrete algebraic Riccati equation](/discrete-algebraic-riccati-equation/) (DARE). The method differs from [Kleinman iteration](/kleinman-iteration/), which is Newton's method on the equation and needs a stabilizing start, and from the Riccati recursion of [infinite-horizon LQR](/infinite-horizon-lqr/), which converges only linearly.

## In plain words

The Riccati equation is quadratic in a matrix, so it cannot be solved by one linear solve. The trick is to double the size. The matrix $H$ of size $2n$ holds the data of the equation, and every solution of the equation is a "flat slice" of $2n$-space that $H$ maps into itself. The slice we want is the one on which $H$ shrinks things: the span of the eigenvectors of the eigenvalues with negative real part. Eigenvectors can be badly conditioned, so the method does not compute them. It computes Schur vectors instead. These are orthonormal, and the first $k$ of them span the same space as the first $k$ eigenvectors in the Schur order. After the stable eigenvalues are moved to the front, the first $n$ Schur vectors give the slice, and one linear solve turns the slice into the matrix $P$.

## The problem

Input: real matrices $A$ ($n \times n$), $B$ ($n \times m$), $Q = Q^T$ ($n \times n$) and $R = R^T > 0$ ($m \times m$). Put $G = B R^{-1} B^T$ and

$$H = \begin{bmatrix} A & -G \\ -Q & -A^T \end{bmatrix}.$$

Output: the real symmetric $P$ with $A^T P + P A - P G P + Q = 0$ and $A - G P$ Hurwitz, and the gain $K = R^{-1} B^T P$, or an error if no such $P$ exists. By the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/), such a $P$ exists when $(A, B)$ is [stabilizable](/stabilizability/) and $H$ has no eigenvalue on the imaginary axis, for example when $Q \ge 0$ and $(Q^{1/2}, A)$ is [detectable](/detectability/).

## The algorithm

```pseudo id=main
SCHUR-METHOD-RICCATI(A, B, Q, R)
L1  H ← [[A, -G], [-Q, -A^T]]  with  G = B R^(-1) B^T
L2  (T, Z) ← complex Schur form of H        ▷ Z^* H Z = T, Z unitary, T upper triangular
L3  if some |Re T_ii| ≤ tol ‖H‖ then error  ▷ eigenvalue on or near the imaginary axis
L4  swap adjacent diagonal entries of T, updating Z, until Re T_ii < 0 exactly for i ≤ n; error if the count is not n
L5  U_1 ← rows 1..n of the first n columns of Z;  U_2 ← rows n+1..2n of them
L6  solve U_1^T X = U_2^T                    ▷ error if U_1 is singular or nearly so
L7  P ← real part of X^T
L8  return P, K = R^(-1) B^T P
```

Line L1 forms $H$ with one solve $R^{-1} B^T$; $R^{-1}$ itself is not formed. Line L2 is the [QR algorithm](/qr-algorithm/). The implementation reduces $H$ to upper Hessenberg form with [Givens rotations](/givens-rotations/) (see [Hessenberg reduction](/hessenberg-reduction/)) and then runs the explicit shifted QR iteration with the [Wilkinson shift](/wilkinson-shift/) and [deflation](/deflation/). After every 10 steps without a deflation it uses an exceptional shift, and after 30 it stops with an error. Every rotation is applied to $T$ from both sides and to $Z$ from the right, so $H = Z T Z^*$ holds at all times.

Line L3 rejects an eigenvalue whose real part is below $10^{-8} \|H\|_F$ in absolute value. Such an eigenvalue cannot be put on the correct side of the axis with confidence, and in exact arithmetic an eigenvalue on the axis means that no stabilizing solution exists.

Line L4 moves each stable diagonal entry to the front by swaps of neighbours. One swap of $t_1 = T_{kk}$ and $t_2 = T_{k+1,k+1}$ uses the rotation that maps the vector $(T_{k,k+1}, t_2 - t_1)$ to a multiple of $e_1$. That vector is the eigenvector of the $2 \times 2$ block for $t_2$, so the rotated block has $t_2$ first and $t_1$ second.

Lines L5 to L7 compute $P = U_2 U_1^{-1}$. Since $(U_2 U_1^{-1})^T = U_1^{-T} U_2^T$, line L6 is a single solve with $n$ right sides and no inverse. Before the solve, the code estimates the smallest singular value of $U_1$ and stops if it is below $10^{-10}$; a singular $U_1$ means that the stable subspace is not the graph of a matrix, and then no stabilizing solution exists. In exact arithmetic $X^T$ is real and symmetric, so line L7 only removes rounding errors. The code also replaces $P$ by $(P + P^T)/2$.

## Example

Scalar case: $a = b = q = r = 1$. Then $H = \begin{bmatrix} 1 & -1 \\ -1 & -1 \end{bmatrix}$ with $\det(s I - H) = s^2 - 2$, so the eigenvalues are $\pm \sqrt 2$. The eigenvector for $-\sqrt 2$ solves $(1 + \sqrt 2) v_1 - v_2 = 0$, so $v = (1, 1 + \sqrt 2)$ up to a factor, and $p = v_2 / v_1 = 1 + \sqrt 2 \approx 2.414214$. Check: $2 p - p^2 + 1 = 2 + 2\sqrt 2 - (3 + 2 \sqrt 2) + 1 = 0$, and $a - b^2 p / r = -\sqrt 2 < 0$. In the implementation, one QR step with the Wilkinson shift gives $T = \operatorname{diag}(\sqrt 2, -\sqrt 2)$ up to the off-diagonal entry, one swap puts $-\sqrt 2$ first, and the first column of $Z$ is a unit multiple of $(\sin(\pi/8), \cos(\pi/8))$, whose ratio $\cot(\pi/8)$ is $1 + \sqrt 2$.

Double integrator: $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$, $R = 1$. Here $\det(s I - H) = s^4 - s^2 + 1$, so $s^2 = e^{\pm i \pi / 3}$ and the eigenvalues are $\pm \sqrt 3 / 2 \pm i / 2$. The state of the run, with six decimals:

| Step | Line | State |
|---|---|---|
| 1 | L1 | $H = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & -1 \\ -1 & 0 & 0 & 0 \\ 0 & -1 & -1 & 0 \end{bmatrix}$ |
| 2 | L2 | diagonal of $T$: $0.866025 + 0.5 i$, $0.866025 - 0.5 i$, $-0.866025 + 0.5 i$, $-0.866025 - 0.5 i$ |
| 3 | L3 | smallest $\lvert \operatorname{Re} T_{ii} \rvert$ is $0.866025$, far from 0 |
| 4 | L4 | 4 swaps; diagonal of $T$: $-0.866025 + 0.5 i$, $-0.866025 - 0.5 i$, $0.866025 + 0.5 i$, $0.866025 - 0.5 i$; count 2 |
| 5 | L5 | $U_1$ is a complex $2 \times 2$ matrix with smallest singular value $0.343724$ |
| 6 | L6 | $X^T$ has imaginary parts below $1.1 \times 10^{-15}$ and asymmetry below $1.4 \times 10^{-15}$ |
| 7 | L7 | $P = \begin{bmatrix} 1.732051 & 1 \\ 1 & 1.732051 \end{bmatrix}$, that is $\begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}$ |
| 8 | L8 | $K = \begin{bmatrix} 1 & 1.732051 \end{bmatrix}$; $A - B K$ has eigenvalues $-0.866025 \pm 0.5 i$ |

The closed loop eigenvalues are exactly the stable eigenvalues of $H$, as the theory says. The CARE residual of the computed $P$ is $1.3 \times 10^{-15}$ in the largest entry.

## Correctness

The full proof is in proofs/correctness.md. Every step is a unitary similarity, so after line L4 we have $H U = U T_{11}$, where $U = \begin{bmatrix} U_1 \\ U_2 \end{bmatrix}$ has orthonormal columns and $T_{11}$ is the leading $n \times n$ block of $T$, with all eigenvalues in the open left half plane. This is the key invariant. If $U_1$ is invertible, multiply the two block rows of $H U = U T_{11}$ by $U_1^{-1}$ on the right. The first gives $A - G P = U_1 T_{11} U_1^{-1}$, so $A - G P$ is Hurwitz. The second gives $-Q - A^T P = P (A - G P)$, which is the CARE. The matrix $W = U_1^* U_2 - U_2^* U_1$ solves $W T_{11} + T_{11}^* W = 0$, a Sylvester equation with the unique solution $W = 0$, so $P$ is Hermitian; it is real because the stable subspace of a real matrix is closed under conjugation. Conversely, if a stabilizing solution $P_+$ exists, the columns of $\begin{bmatrix} I \\ P_+ \end{bmatrix}$ span the same subspace, so $U_1$ is invertible and no check fails. The QR iteration has a step limit, so the algorithm always stops.

The tests check the Schur form on random matrices (unitary $Z$, $Z T Z^* = M$, eigenvalues equal to the roots of the characteristic polynomial), check the CARE solution on 250 random problems against the stable roots of $\det(s I - H)$ and on 250 against Newton's method with Kronecker-form Lyapunov solves, check the DARE variant on 100 problems against a long Riccati recursion, and check that the method raises an error on problems with no stabilizing solution.

## Complexity

In the [floating point model](/floating-point-model/), with $N = 2n$:

- Line L1 costs $O(n^2 m + m^3)$, or $O(n^3)$ when $m \le n$.
- The Hessenberg reduction in line L2 uses about $N^2/2$ rotations, each applied to two rows and two columns of length $N$, so $O(N^3) = O(n^3)$.
- One QR step on a window of size $w$ uses $w - 1$ rotations on full rows and columns, $O(N w) = O(n^2)$. Each of the $N$ deflations takes at most $c$ steps, so the iteration costs $O(c n^3)$. In practice the Wilkinson shift gives deflation after a few steps per eigenvalue, so $c$ is a small constant and the cost is $O(n^3)$.
- Line L4 needs at most $n^2$ swaps, since each of the $n$ stable entries passes at most $n$ unstable ones, and a swap costs $O(N)$. So $O(n^3)$.
- Lines L5 to L8 cost $O(n^3)$, including the singular value estimate of $U_1$.

The extra space is $O(n^2)$ for $H$, $T$ and $Z$.

## Properties

- **Direct up to the eigenvalue iteration.** There is no iteration on $P$. All the iteration is inside the QR algorithm, whose convergence is fast and well understood in practice, although not proved for every matrix.
- **Unitary transformations.** All the work on $H$ is done with rotations, so the computed $T$ and $Z$ are an exact Schur form of a nearby matrix $H + E$ with $\|E\|$ a small multiple of the unit roundoff times $\|H\|$ ([backward error analysis](/backward-error-analysis/)). The error in $P$ then depends on how well conditioned $U_1$ and the stable subspace are.
- **No structure.** The rotations do not preserve the Hamiltonian structure, so $H + E$ is not Hamiltonian in general, and the computed eigenvalues are not exactly symmetric about the imaginary axis. This is why the check of line L3 has a tolerance.
- **Other solutions.** Lemma 3 of the proof does not use stability. Moving any $n$ eigenvalues to the front in line L4 gives a solution of the CARE whenever $U_1$ is invertible, though not always a real symmetric one. Selecting the eigenvalues with positive real part gives the anti-stabilizing solution, for the double integrator $\begin{bmatrix} -\sqrt 3 & 1 \\ 1 & -\sqrt 3 \end{bmatrix}$.
- **Closed loop for free.** The diagonal of $T_{11}$ holds the eigenvalues of $A - B K$.

## Variants and improvements

- **Real Schur form.** Laub's original method works in real arithmetic. The real Schur form has $2 \times 2$ blocks for complex pairs, computed by the [Francis double shift QR](/francis-double-shift-qr/), and the reordering must swap blocks of size 1 and 2. It does half the arithmetic of the complex form on real data, and the Schur vectors are real, so $P$ is real without a final real part.
- **Discrete time.** For the DARE, replace $H$ by the symplectic matrix $S = \begin{bmatrix} A + G A^{-T} Q & -G A^{-T} \\ -A^{-T} Q & A^{-T} \end{bmatrix}$ and select the eigenvalues inside the unit circle. The implementation has this as `dare_schur`. It needs $A$ invertible.
- **Generalized Schur form.** Without inverting $A$ (discrete time) or $R$ (both cases), work with a matrix pencil and compute an ordered generalized Schur form with the [QZ algorithm](/qz-algorithm/). This handles a singular or badly conditioned $A$ or $R$; Van Dooren (1981) gave a method of this kind. See the [generalized eigenvalue problem](/generalized-eigenvalue-problem/).
- **Structure preserving methods.** Paige and Van Loan (1981) studied a Hamiltonian Schur form, computed with transformations that are both unitary and symplectic. Methods that keep the structure give eigenvalues that are exactly symmetric about the axis.
- **Balancing.** Scaling $H$ or the data before the computation, as in [matrix balancing](/matrix-balancing/), can reduce the error when the entries of $A$, $Q$ and $G$ have very different sizes.
- **Newton refinement.** One or two steps of [Kleinman iteration](/kleinman-iteration/) started from the Schur solution often reduce the residual to the rounding level, since the Schur solution is stabilizing and close.

## When to use it

Use it for dense problems of small and medium size, when no stabilizing gain is known in advance. It needs no starting point, it is the standard direct method, and it gives the closed loop eigenvalues as a by-product. [Kleinman iteration](/kleinman-iteration/) needs a stabilizing start, but converges quadratically and is good for refining a solution or for tracking a slowly changing problem. The Riccati recursion of [infinite-horizon LQR](/infinite-horizon-lqr/) is simple but converges only linearly, and slowly when the closed loop is close to the stability boundary. For large sparse problems with a low rank $Q$, dense $O(n^3)$ methods are too expensive, and low rank Newton or Krylov methods are used instead.

## Pitfalls

- **Wrong half of the spectrum.** If line L4 selects the eigenvalues with positive real part, the result is the anti-stabilizing solution, and $A - B K$ is unstable. Line L4 must select $\operatorname{Re} T_{ii} < 0$ (or $\lvert T_{ii} \rvert < 1$ in discrete time).
- **Forming the inverse.** Computing $U_1^{-1}$ and then $U_2 U_1^{-1}$ costs more and is less accurate than the solve of line L6. Check the conditioning of $U_1$ before line L6: a nearly singular $U_1$ gives a huge and meaningless $P$, not an error.
- **No check on the axis.** Without line L3, an eigenvalue close to the axis can fall on the wrong side by rounding, and the count in line L4 is then $n \pm 1$, or the subspace is the wrong one. Line L3 must reject such cases, and the user should then check stabilizability and detectability.
- **Complex output.** With the complex Schur form, line L7 must take the real part. Returning $X^T$ as it is gives complex entries of size $10^{-16}$, and code that expects a real matrix can fail.
- **Eigenvectors instead of Schur vectors.** Computing $n$ eigenvectors of $H$ in line L2 fails when $H$ has a multiple eigenvalue without a full set of eigenvectors, and is inaccurate when eigenvalues are close. Schur vectors always exist and are orthonormal.

## Implementations

## History

Earlier methods computed the stable invariant subspace of $H$ from its eigenvectors, which fails or loses accuracy when eigenvalues are multiple or close. Laub (1979) replaced the eigenvectors by Schur vectors from the ordered real Schur form, computed with the QR algorithm and a reordering of the diagonal blocks, and gave the discrete-time version with a symplectic matrix. The method became the standard way to solve the CARE and the DARE for dense problems. Paige and Van Loan (1981) studied the Hamiltonian Schur form, which started the work on structure preserving methods, and the extended pencil methods of Van Dooren removed the need to invert $R$ or $A$.

## References
