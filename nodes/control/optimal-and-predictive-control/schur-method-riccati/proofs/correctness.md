---
title: The ordered Schur form of the Hamiltonian matrix gives the stabilizing solution of the CARE
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T$ and $R = R^T > 0$. Put $G = B R^{-1} B^T$, so $G = G^T \ge 0$, and

$$H = \begin{bmatrix} A & -G \\ -Q & -A^T \end{bmatrix}, \qquad J = \begin{bmatrix} 0 & I \\ -I & 0 \end{bmatrix}.$$

A stabilizing solution of the CARE $A^T P + P A - P G P + Q = 0$ is a solution $P$ for which $A - G P$ is Hurwitz. The algorithm computes a unitary $Z$ and an upper triangular $T$ with $Z^* H Z = T$, moves the eigenvalues with negative real part to the first $n$ places of the diagonal, splits the first $n$ columns of $Z$ as $\begin{bmatrix} U_1 \\ U_2 \end{bmatrix}$, and returns $P = U_2 U_1^{-1}$ and $K = R^{-1} B^T P$. It stops with an error if a diagonal entry of $T$ lies on the imaginary axis, if the number of entries with negative real part is not $n$, or if $U_1$ is singular.

The lemmas below are in exact arithmetic. The last section says what changes in floating point.

## Lemma 1: the rotations are unitary similarities

Every step of the algorithm (the reduction to Hessenberg form, each QR step and each swap) replaces $T$ by $G T G^*$ and $Z$ by $Z G^*$, where $G$ is the identity except for a $2 \times 2$ block $\begin{bmatrix} c & s \\ -\bar s & c \end{bmatrix}$ in rows and columns $i$, $i + 1$, with $c \ge 0$ real and $c^2 + |s|^2 = 1$. So the invariant $H = Z T Z^*$ with $Z^* Z = I$ holds after every step.

*Proof.* The block satisfies $\begin{bmatrix} c & s \\ -\bar s & c \end{bmatrix} \begin{bmatrix} c & -s \\ \bar s & c \end{bmatrix} = \begin{bmatrix} c^2 + |s|^2 & 0 \\ 0 & |s|^2 + c^2 \end{bmatrix} = I$, so $G$ is unitary. If $H = Z T Z^*$, then $H = (Z G^*) (G T G^*) (Z G^*)^*$. In a QR step the shift $\mu$ is subtracted from the diagonal entries of the active window $[l, h]$ and added back after the rotations. Each rotation of the step acts on two rows and two columns whose indices lie in the window. If $D$ is the diagonal matrix with ones on the window and zeros elsewhere, then $G D G^* = D$ for such a rotation, so $G (T - \mu D) G^* + \mu D = G T G^*$, and subtracting and adding $\mu$ on the window gives the similarity of the whole matrix. The code stores an entry that a rotation makes zero as an exact 0, and deflation sets a subdiagonal entry below a rounding level to 0. Both change $T$ by at most a rounding error, which the section on floating point covers; with exact zeros they change nothing. $\square$

When the algorithm leaves the QR iteration, $T$ is upper triangular, so $T = Z^* H Z$ is a complex Schur form of $H$ and its diagonal holds the eigenvalues of $H$ with their algebraic multiplicities.

## Lemma 2: one swap exchanges two diagonal entries

Let $T$ be upper triangular with $t_1 = T_{kk} \ne t_2 = T_{k+1,k+1}$ and $x = T_{k,k+1}$. Let $G$ be the rotation with $G \begin{bmatrix} x \\ t_2 - t_1 \end{bmatrix} = \begin{bmatrix} r \\ 0 \end{bmatrix}$, $r \ne 0$, acting on rows and columns $k$ and $k + 1$. Then $G T G^*$ is upper triangular, with $t_2$ in place $k$ and $t_1$ in place $k + 1$.

*Proof.* Let $T_2 = \begin{bmatrix} t_1 & x \\ 0 & t_2 \end{bmatrix}$ and $v = \begin{bmatrix} x \\ t_2 - t_1 \end{bmatrix}$. Then $T_2 v = \begin{bmatrix} t_1 x + x (t_2 - t_1) \\ t_2 (t_2 - t_1) \end{bmatrix} = t_2 v$. From $G v = r e_1$ we get $G^* e_1 = v / r$, so $G T_2 G^* e_1 = G T_2 v / r = t_2 G v / r = t_2 e_1$. The first column of the block $G T_2 G^*$ is $(t_2, 0)$, and its trace is $t_1 + t_2$, so its second diagonal entry is $t_1$. The rotation acts on rows $k$, $k + 1$ and columns $k$, $k + 1$ only. Rows $k$ and $k + 1$ are zero in the columns before $k$, and columns $k$ and $k + 1$ are zero in the rows after $k + 1$, so no other entry below the diagonal changes. $\square$

By Lemmas 1 and 2, the reordering ends with $H Z = Z T$, $T$ upper triangular, and the entries with negative real part in places $1, \dots, n$, provided there are exactly $n$ of them, which the algorithm checks. Write $T_{11}$ for the leading $n \times n$ block of $T$ and $U = \begin{bmatrix} U_1 \\ U_2 \end{bmatrix}$ for the first $n$ columns of $Z$. Because $T$ is upper triangular, the first $n$ columns of $H Z = Z T$ give

$$H U = U T_{11}, \qquad U^* U = I, \tag{1}$$

and every eigenvalue of $T_{11}$ has negative real part. So the columns of $U$ span an $n$-dimensional invariant subspace $\mathcal{V}$ of $H$, the stable invariant subspace. It is the sum of the generalized eigenspaces of the eigenvalues with negative real part, so it does not depend on the choices made by the QR iteration.

## Lemma 3: an invertible U1 gives a stabilizing solution

If $U_1$ is invertible, then $P = U_2 U_1^{-1}$ solves the CARE and $A - G P = U_1 T_{11} U_1^{-1}$, so $A - G P$ is Hurwitz.

*Proof.* The two block rows of (1) are $A U_1 - G U_2 = U_1 T_{11}$ and $-Q U_1 - A^T U_2 = U_2 T_{11}$. Multiply both on the right by $U_1^{-1}$. The first gives $A - G P = U_1 T_{11} U_1^{-1}$. The second gives $-Q - A^T P = P U_1 T_{11} U_1^{-1} = P (A - G P)$, which is $A^T P + P A - P G P + Q = 0$. $\square$

## Lemma 4: P is real and symmetric

If $U_1$ is invertible, then $P = U_2 U_1^{-1}$ is real and $P = P^T$.

*Proof.* Symmetric: the matrix $J H = \begin{bmatrix} -Q & -A^T \\ -A & G \end{bmatrix}$ is real and symmetric, so $(J H)^* = J H$. Since $J^* = -J$, this reads $-H^* J = J H$, that is, $H^* J = -J H$. Let $W = U^* J U = U_1^* U_2 - U_2^* U_1$. Then, by (1), $T_{11}^* W = T_{11}^* U^* J U = (H U)^* J U = U^* H^* J U = -U^* J H U = -W T_{11}$. Hence $W T_{11} + T_{11}^* W = 0$. The eigenvalues of $T_{11}$ and of $-T_{11}^*$ are in the open left and the open right half plane, so they are disjoint, and this Sylvester equation has the unique solution $W = 0$. So $U_1^* U_2 = U_2^* U_1$, and

$$P^* = U_1^{-*} U_2^* = U_1^{-*} (U_2^* U_1) U_1^{-1} = U_1^{-*} (U_1^* U_2) U_1^{-1} = P.$$

Real: $H$ is real, so complex conjugation maps an invariant subspace of $H$ to an invariant subspace of $H$ and maps the eigenvalues to their conjugates, which have the same real part. So $\bar{\mathcal{V}} = \mathcal{V}$. Then $\bar U = U M$ for an invertible $n \times n$ matrix $M$, and $\bar P = \bar U_2 \bar U_1^{-1} = U_2 M M^{-1} U_1^{-1} = P$. A real Hermitian matrix is real symmetric. $\square$

The same computation shows that $P$ does not depend on the basis: any other basis of $\mathcal{V}$ is $U M$ with $M$ invertible, and gives the same $U_2 U_1^{-1}$.

## Lemma 5: the checks fail only when no stabilizing solution exists

If the CARE has a stabilizing solution $P_+$, then $H$ has no eigenvalue on the imaginary axis, it has exactly $n$ eigenvalues with negative real part, and $U_1$ is invertible.

*Proof.* Since $P_+$ solves the CARE, $H \begin{bmatrix} I \\ P_+ \end{bmatrix} = \begin{bmatrix} A - G P_+ \\ -Q - A^T P_+ \end{bmatrix} = \begin{bmatrix} I \\ P_+ \end{bmatrix} (A - G P_+)$, and with $E = \begin{bmatrix} I & 0 \\ P_+ & I \end{bmatrix}$ a short computation gives

$$E^{-1} H E = \begin{bmatrix} A - G P_+ & -G \\ 0 & -(A - G P_+)^T \end{bmatrix}.$$

So the eigenvalues of $H$ are those of $A - G P_+$, all in the open left half plane, and those of $-(A - G P_+)^T$, all in the open right half plane. This gives the first two claims. The columns of $\begin{bmatrix} I \\ P_+ \end{bmatrix}$ span an invariant subspace of dimension $n$ whose eigenvalues all have negative real part, so it is contained in $\mathcal{V}$, and both have dimension $n$, so it equals $\mathcal{V}$. Hence $U = \begin{bmatrix} I \\ P_+ \end{bmatrix} M$ for an invertible $M$, and $U_1 = M$ is invertible. $\square$

## Theorem

If the algorithm returns, then $P$ is the real symmetric stabilizing solution of the CARE and $A - B K = A - G P$ is Hurwitz. It is the only stabilizing solution. The algorithm stops with an error exactly when the CARE has no stabilizing solution, or, in floating point, when the data is within the tolerances of such a case.

*Proof.* Lemmas 3 and 4 give the first sentence, since $B K = B R^{-1} B^T P = G P$. If $P'$ is another stabilizing solution, then by Lemma 5 the columns of $\begin{bmatrix} I \\ P' \end{bmatrix}$ span $\mathcal{V}$ too, so $\begin{bmatrix} I \\ P' \end{bmatrix} = \begin{bmatrix} I \\ P \end{bmatrix} M$, which forces $M = I$ and $P' = P$. If no stabilizing solution exists, then by Lemma 3 the matrix $U_1$ cannot be invertible, or there is no $n$-dimensional stable subspace; either way a check fails. If a stabilizing solution exists, Lemma 5 shows that no check fails. $\blacksquare$

The QR iteration is not proved to converge here. The implementation counts the QR steps since the last deflation, uses an exceptional shift after every 10 steps without a deflation, and raises an error after 30. So it always terminates, and when it returns, Lemmas 1 to 5 apply.

## The discrete-time variant

For the DARE $P = A^T P A - A^T P B (R + B^T P B)^{-1} B^T P A + Q$ with $A$ invertible, the code uses

$$S = \begin{bmatrix} A + G A^{-T} Q & -G A^{-T} \\ -A^{-T} Q & A^{-T} \end{bmatrix} = N^{-1} L, \qquad L = \begin{bmatrix} A & 0 \\ -Q & I \end{bmatrix}, \quad N = \begin{bmatrix} I & G \\ 0 & A^T \end{bmatrix},$$

and selects the eigenvalues with $|\lambda| < 1$. Lemmas 1 and 2 do not depend on $H$, so (1) holds with $S$ in place of $H$, and $|\lambda| < 1$ for every eigenvalue of $T_{11}$. If $U_1$ is invertible, multiply $L U = N U T_{11}$ on the right by $U_1^{-1}$ and put $\Lambda = U_1 T_{11} U_1^{-1}$. The two block rows are $A = (I + G P) \Lambda$ and $-Q + P = A^T P \Lambda$. Since $A$ is invertible, so is $I + G P$, and $\Lambda = (I + G P)^{-1} A$. By Sylvester's determinant identity, $\det(I + B R^{-1} B^T P) = \det(I + R^{-1} B^T P B)$, so $R + B^T P B$ is invertible. Multiplying out shows $(I + G P)(A - B (R + B^T P B)^{-1} B^T P A) = A$, so $\Lambda = A - B K$ with $K = (R + B^T P B)^{-1} B^T P A$, and the second row becomes the DARE. The closed loop $\Lambda$ is similar to $T_{11}$, so it is Schur.

For the symmetry, $S$ is symplectic: $S^T J S = J$, which follows from $G = G^T$ and $Q = Q^T$ by multiplying out the blocks. With $W = U^* J U$ and $S U = U T_{11}$ this gives $T_{11}^* W T_{11} = U^* S^* J S U = W$, so $W = (T_{11}^*)^k W T_{11}^k$ for every $k$, and $W = 0$ because $T_{11}^k \to 0$. The rest of Lemma 4 is the same, and Lemma 5 uses $E^{-1} S E$, which is block upper triangular with diagonal blocks $A - B K$ and $(A - B K)^{-T}$ when $P$ is a stabilizing solution of the DARE.

## Floating point

In floating point, Lemma 1 holds with a small error: the computed $T$ and $Z$ satisfy $Z T Z^* = H + E$, with $Z$ unitary up to rounding and $\|E\|$ a small multiple of the unit roundoff times $\|H\|$, because the algorithm uses only Givens rotations (Golub and Van Loan, Chapter 7). The computed basis $U$ is then an exact stable basis of a nearby matrix. The error in $P$ is controlled by this backward error and by the conditioning of $U_1$ and of the stable subspace. This is why the code refuses a $U_1$ with smallest singular value below $10^{-10}$ and an eigenvalue whose real part is within $10^{-8} \|H\|_F$ of 0. The imaginary part of the computed $P$ and its departure from symmetry are rounding errors; the code drops the first and averages $P$ with $P^T$ for the second.
