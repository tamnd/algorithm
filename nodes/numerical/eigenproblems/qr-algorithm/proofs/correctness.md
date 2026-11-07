---
title: The Hessenberg QR algorithm terminates and returns a Schur form of a nearby matrix
proves: [correctness, termination]
status: full
---

Notation of the page. Indices are 1-based. The steps of lines L8 and L9 are analysed in exact arithmetic; the rounding errors of a computed rotation are of order $u$ relative to the rows and columns it touches, and their accumulation into a backward error $O(u) \|A\|$ is the classical analysis of Wilkinson (1965, Chapter 3 and Chapter 8) and GVL Section 5.1 and Section 7.5, which we do not repeat. What we prove is that the structure is kept, that the deflations perturb $A$ by a bounded amount, that the loop terminates, that a CONVERGED result is a Schur form, and why the shifts give fast local convergence.

**Lemma 1 (one step keeps Hessenberg form).** Let $W$ be an unreduced upper Hessenberg $m \times m$ matrix and $\mu$ a scalar. Let $G_1, \dots, G_{m-1}$ be the rotations of line L8, where $G_i$ acts in the plane $(i, i+1)$ and is chosen so that $G_{m-1}^* \cdots G_1^* (W - \mu I) = R$ is upper triangular. Then $R G_1 \cdots G_{m-1} + \mu I$ is upper Hessenberg, and it equals $G^* W G$ with $G = G_1 \cdots G_{m-1}$ unitary.

*Proof.* Induction on the left rotations: before $G_i^*$ is applied, rows $1..i-1$ are already triangular and the only nonzero entry below the diagonal in column $i$ is the original $w_{i+1,i}$ (rows $i$ and $i+1$ have zeros in columns $< i$, by the previous rotation and by the Hessenberg form). So $G_i^*$ can zero it, which is how it is chosen, and it does not touch columns $< i$. After all left rotations, $R$ is upper triangular. For the right rotations, multiplying a matrix whose column $i+1$ has nonzeros only in rows $\le i + 1$ by $G_i$ on the right mixes columns $i$ and $i+1$, so it creates a nonzero only in position $(i+1, i)$. Applying $G_1, \dots, G_{m-1}$ in order fills exactly the first subdiagonal, so $R G$ is Hessenberg. Finally $R G + \mu I = G^*(W - \mu I) G + \mu I = G^* W G$. $\square$

Lemma 1 also shows that restricting the left rotations to columns $i..n$ and the right rotations to rows $1..i+1$ (line L9 uses $1..i+2$, which only adds zeros) computes the full products exactly.

**Lemma 2 (the invariant).** At every execution of line L3, $Q$ is unitary, $H$ is upper Hessenberg, $h_{lo', lo'-1} = 0$ for every row $lo'$ at which an entry was set to zero, $h_{i+1,i} = 0$ for all $i \ge hi$, and

$$Q H Q^* = A + E, \qquad \|E\|_2 \le \sum_t |\eta_t|,$$

where $\eta_t$ are the values that line L4 replaced by zero.

*Proof.* After line L1, $Q H Q^* = A$ with $E = 0$ (Hessenberg reduction is a unitary similarity). Line L4 replaces $H$ by $H - \eta \, e_l e_{l-1}^T$, which changes $Q H Q^*$ by $-\eta \, Q e_l e_{l-1}^T Q^*$, a matrix of 2-norm $|\eta|$; this adds a term to $E$ and keeps the Hessenberg form. A step of lines L8 and L9 acts on rows and columns $lo..hi$ only, by the unitary $\tilde G = \operatorname{diag}(I_{lo-1}, G, I_{n-hi})$. Because $h_{lo,lo-1} = 0$ and $h_{hi+1,hi} = 0$, $H$ is block upper triangular with the window as its middle diagonal block, so $\tilde G^* H \tilde G$ is block upper triangular with the same outer diagonal blocks, its middle block is $G^* W G$, which is Hessenberg by Lemma 1, and the zero blocks below the diagonal stay zero. Replacing $Q$ by $Q \tilde G$ keeps $Q H Q^*$ and the unitarity of $Q$. The zero entries $h_{l,l-1}$ outside the current window lie in a row or a column the step does not touch. $\square$

**Lemma 3 (the size of the deflation perturbation).** Each zeroed value satisfies $|\eta| \le u(|h_{l-1,l-1}| + |h_{l,l}|) \le \sqrt 2 \, u \, \|H\|_F$, at most $n - 1$ values are nonzero, and so $\|E\|_2 \le \sqrt 2 (n - 1) u \, (\|A\|_F + \|E\|_F)$, which gives $\|E\|_2 = O(n u) \|A\|_F$ when $n u$ is small. If both diagonal entries are zero, the implementation uses the threshold $u \|H_1\|_F$, where $H_1$ is the Hessenberg matrix of line L1, and the same bound holds.

*Proof.* The first inequality is the test of line L4, and $|x| + |y| \le \sqrt 2 (|x|^2 + |y|^2)^{1/2}$. By Lemma 2, an entry $h_{l,l-1}$ that has been set to zero is never changed again, so each of the $n - 1$ subdiagonal positions contributes at most once a nonzero $\eta$. Since $H$ is unitarily similar to $A + E$, $\|H\|_F = \|A + E\|_F \le \|A\|_F + \|E\|_F$. $\square$

**Theorem 4 (termination).** For every input, the loop of line L3 ends after at most $n (\mathrm{maxit} + 1)$ passes.

*Proof.* Each pass through the loop body either executes line L5, which lowers $hi$ by one and resets $its$ to 0, or reaches line L6, which raises $its$ by one and returns once $its > \mathrm{maxit}$. So the pair $(hi, -its)$ decreases in the lexicographic order at each pass, $hi$ takes at most $n$ values, and for each value of $hi$ at most $\mathrm{maxit} + 1$ passes raise $its$. $\square$

**Theorem 5 (a CONVERGED result is a Schur form).** If line L10 returns, then $T = H$ is upper triangular, $Q$ is unitary, and $Q T Q^* = A + E$ with $E$ as in Lemmas 2 and 3. In particular the diagonal entries of $T$ are the eigenvalues of $A + E$.

*Proof.* Line L10 is reached with $hi = 1$. The value of $hi$ only decreases at line L5, when $lo = hi$, and that happens only when line L4 has found $l = hi$, that is, set $h_{hi, hi-1} = 0$. So every subdiagonal entry $h_{i, i-1}$ for $i = 2, \dots, n$ has been set to zero, and by Lemma 2 it has stayed zero. A Hessenberg matrix with zero subdiagonal is upper triangular. $\square$

**Proposition 6 (unshifted QR is subspace iteration).** With $\mu = 0$ at every step and no deflation, let $A_0 = H$, $A_{k-1} = Q_k R_k$ and $A_k = R_k Q_k$. Put $\hat Q_k = Q_1 \cdots Q_k$ and $\hat R_k = R_k \cdots R_1$. Then $A_k = \hat Q_k^* A_0 \hat Q_k$ and $A_0^k = \hat Q_k \hat R_k$. With shifts $\mu_1, \dots, \mu_k$, the same argument gives $\prod_{i=1}^k (A_0 - \mu_i I) = \hat Q_k \hat R_k$.

*Proof.* $A_k = R_k Q_k = Q_k^* A_{k-1} Q_k$, which gives the first claim by induction. For the second, $A_0^k = A_0 \cdot A_0^{k-1} = A_0 \hat Q_{k-1} \hat R_{k-1} = \hat Q_{k-1} A_{k-1} \hat R_{k-1} = \hat Q_{k-1} Q_k R_k \hat R_{k-1} = \hat Q_k \hat R_k$, using the first claim in the form $A_0 \hat Q_{k-1} = \hat Q_{k-1} A_{k-1}$. The shifted case is the same computation with $A_0 - \mu_k I$ in place of $A_0$ at step $k$. $\square$

So the first $j$ columns of $\hat Q_k$ are an orthonormal basis of $A_0^k$ applied to $\operatorname{span}\{e_1, \dots, e_j\}$, which is [subspace iteration](/subspace-iteration/). If $|\lambda_j| > |\lambda_{j+1}|$ and the start subspace is not deficient, the subspace converges to the invariant subspace of the $j$ largest eigenvalues at the rate $|\lambda_{j+1}/\lambda_j|$ (GVL Section 7.3), and the block $(A_k)_{j+1:n, 1:j}$, which is the single entry $h_{j+1,j}$ for a Hessenberg matrix, goes to zero at that rate.

**Proposition 7 (shifted QR is inverse iteration on the last column).** If $H - \mu I = Q R$ is nonsingular, then $(H - \mu I)^{-*} e_n = Q e_n / \bar r_{nn}$.

*Proof.* $(H - \mu I)^{-*} = (Q R)^{-*} = Q R^{-*}$, and $R^{-*}$ is lower triangular with last diagonal entry $1 / \bar r_{nn}$, so $R^{-*} e_n = e_n / \bar r_{nn}$. $\square$

The new last row of $H$ is $e_n^* Q^* H Q$, and its diagonal entry $q_n^* H q_n$ is the Rayleigh quotient of $q_n$. With the Rayleigh shift $\mu = h_{nn}$ the step is therefore one step of [Rayleigh quotient iteration](/rayleigh-quotient-iteration/) for $H^*$ from $e_n$, which explains the quadratic and, for Hermitian $H$, cubic local rates.

**Proposition 8 (the exact $2 \times 2$ step).** Let $H = \begin{pmatrix} a & b \\ \epsilon & d \end{pmatrix}$ with $\epsilon \ne 0$ and $\mu = d$. Then one step gives $|h'_{21}| = |\epsilon|^2 |b| / (|a - d|^2 + |\epsilon|^2)$.

*Proof.* Let $\alpha = a - d$ and $r = (|\alpha|^2 + |\epsilon|^2)^{1/2} > 0$. The rotation of line L8 has $c = |\alpha| / r$ and $s = \phi \bar\epsilon / r$ with $|\phi| = 1$ (for $\alpha = 0$, $c = 0$ and $|s| = 1$). Its second row $(-\bar s, c)$ applied to the columns of $H - d I = \begin{pmatrix} \alpha & b \\ \epsilon & 0 \end{pmatrix}$ gives the second row of $R$ as $(0, -\bar s b)$. Applying the right rotation of line L9, the new $(2, 1)$ entry is $\bar s \cdot (-\bar s b) = -\bar s^2 b$, of modulus $|s|^2 |b| = |\epsilon|^2 |b| / r^2$. Adding $\mu$ back changes only the diagonal. $\square$

So if $a \ne d$ the next subdiagonal entry is $O(|\epsilon|^2)$, and if $|b| = |\epsilon|$, as for a Hermitian $H$, it is $O(|\epsilon|^3)$. For a larger Hessenberg matrix, GVL Section 7.5.3 derives the same quadratic behaviour of $h_{n,n-1}$ with the Rayleigh shift, under the assumption that the trailing entries have settled.

**Remark (no global theorem).** Propositions 6 to 8 are local statements. The cyclic permutation matrix is a fixed point of the step with $\mu = 0$, the Rayleigh shift and the Wilkinson shift, so no global convergence theorem holds for these shifts on general matrices; exceptional shifts break this example but are not known to give a provable bound. For symmetric tridiagonal matrices with the Wilkinson shift, Wilkinson (1968) proved convergence for every input. $\blacksquare$
