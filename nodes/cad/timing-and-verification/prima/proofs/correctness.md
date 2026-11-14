---
title: PRIMA spans the block Krylov subspace, matches q block moments (2q when G and C are symmetric), gives the full model at full order, and keeps passivity and stability
proves: [the basis spans the block Krylov subspace, matching of q block moments, matching of 2q block moments in the symmetric case, exactness at full order, passivity of the reduced model, poles in the closed left half-plane, running time]
status: full
---

**Setting.** A linear circuit in modified nodal form is
$$ (G + sC) \, x(s) = B \, u(s), \qquad y(s) = L^T x(s), \qquad H(s) = L^T (G + sC)^{-1} B, $$
with real $G, C$ of order $n$, $G$ invertible, $B$ of size $n \times p$ and $L$ of size $n \times r$. Write $A = -G^{-1} C$ and $R = G^{-1} B$. The block moments are the coefficients of $H(s) = \sum_k M_k s^k$ at $s = 0$, $M_k = L^T A^k R$ (Neumann series of $(I - sA)^{-1}$, as for [AWE](/asymptotic-waveform-evaluation/)). The block Krylov subspace of order $q$ is
$$ \mathcal K_q = \operatorname{span}\{ R, AR, \ldots, A^{q-1} R \}, $$
the span of all columns of these $q$ blocks. PRIMA returns the columns $X = [X_0, \ldots, X_{q-1}]$ and the reduced matrices $\hat G = X^T G X$, $\hat C = X^T C X$, $\hat B = X^T B$ and $\hat L = X^T L$, with $\hat H(s) = \hat L^T (\hat G + s \hat C)^{-1} \hat B$ and reduced moments $\hat M_k = \hat L^T \hat A^k \hat R$, where $\hat A = -\hat G^{-1} \hat C$ and $\hat R = \hat G^{-1} \hat B$. The proofs are in exact arithmetic.

**Theorem 1 (the basis).** The columns of $X$ are orthonormal, and $\operatorname{span}(X) = \mathcal K_q$. More precisely, $\operatorname{span}(X_0, \ldots, X_k) = \mathcal K_{k+1}$ for each $k < q$.

*Proof.* By induction on $k$. Line L2 makes $X_0$ an orthonormal basis of the columns of $R$, so the claim holds for $k = 0$. Suppose $\operatorname{span}(X_0, \ldots, X_{k-1}) = \mathcal K_k$. Line L4 sets $V = A X_{k-1}$. Since the columns of $X_{k-1}$ lie in $\mathcal K_k$, those of $V$ lie in $A \mathcal K_k \subseteq \mathcal K_{k+1}$. Conversely, $\mathcal K_{k+1} = \mathcal K_k + \operatorname{span}(A^k R)$. Since $A^{k-1} R \in \mathcal K_k = \operatorname{span}(X_0, \ldots, X_{k-1})$, the columns of $A^k R$ lie in the span of $A X_0, \ldots, A X_{k-1}$. For $j < k - 1$, the induction hypothesis gives $A X_j \subseteq A \mathcal K_{j+1} \subseteq \mathcal K_{j+2} \subseteq \mathcal K_k$. So $A^k R$ lies in $\mathcal K_k + \operatorname{span}(V)$, and $\mathcal K_{k+1} = \mathcal K_k + \operatorname{span}(V)$. Lines L5 and L6 subtract from $V$ its projection on $\mathcal K_k$ and take an orthonormal basis of the rest, dropping the columns that are dependent (deflation). This changes neither $\mathcal K_k + \operatorname{span}(V)$ nor the orthonormality of the whole set. If a whole block is dropped, then $\mathcal K_{k+1} = \mathcal K_k$, the subspace is invariant under $A$, all later $\mathcal K_j$ are equal to it, and the loop can stop. $\square$

**Theorem 2 (q block moments).** If $\hat G$ is invertible, then $X \hat A^k \hat R = A^k R$ and $\hat M_k = M_k$ for $k = 0, \ldots, q - 1$. The same holds for every $X$ of full column rank with $\mathcal K_q \subseteq \operatorname{span}(X)$; orthonormality is not needed.

*Proof.* We show $X \hat A^k \hat R = A^k R$ by induction. For $k = 0$: $R \in \mathcal K_q$, so $R = X Z$ for some $Z$. Then $\hat G Z = X^T G X Z = X^T G R = X^T B = \hat B$, so $Z = \hat R$ and $X \hat R = R$. For $1 \le k \le q - 1$, let $W = \hat A^{k-1} \hat R$, so $X W = A^{k-1} R$ by the induction hypothesis. Since $A^k R \in \mathcal K_q$, $A X W = A^k R = X U$ for some $U$. Multiply $G X U = G A X W = -C X W$ by $X^T$: $\hat G U = -\hat C W$, so $U = \hat A W = \hat A^k \hat R$. Hence $X \hat A^k \hat R = X U = A^k R$. Finally $\hat M_k = \hat L^T \hat A^k \hat R = L^T X \hat A^k \hat R = L^T A^k R = M_k$. $\square$

The hypothesis that $\hat G$ is invertible is needed. When $G + G^T$ is positive definite, $\hat G + \hat G^T$ is positive definite too and $\hat G$ is invertible. When $G + G^T$ is only semidefinite, as in the modified nodal form of an RLC circuit, $\hat G$ can be singular although $G$ is not. Example: node voltages $v_0, v_1, v_2$ and inductor currents $i_0, i_1$ of a ladder with a conductance 1 at node 0 only, capacitors 1 at all nodes and inductors 1 between nodes 0, 1 and 1, 2, with one port at node 0. Then $R$ is $(1, 1, 1, 0, 0)$ (at DC the inductors are shorts), $AR = (-3, -3, -3, 2, 1)$, and $q = 2$ gives $X_0 = (1, 1, 1, 0, 0)/\sqrt 3$, $X_1 = (0, 0, 0, 2, 1)/\sqrt 5$ and $\hat G = \operatorname{diag}(1/3, 0)$. Here $X_1^T G X_1 = 0$ because $G$ has a zero block for the currents, and the off-diagonal entries are 0 because each column of the incidence block sums to 0.

**Theorem 3 (2q block moments in the symmetric case).** If $G$ and $C$ are symmetric, $L = B$ and $\hat G$ is invertible, then $\hat M_k = M_k$ for $k = 0, \ldots, 2q - 1$.

*Proof.* Since $G$ is symmetric, $B^T = R^T G$, and $A^T G = -C G^{-1} G = -C = G A$. By induction, $(A^i)^T G = G A^i$. So for $i, j \ge 0$,
$$ M_{i+j} = R^T G A^i A^j R = (A^i R)^T G (A^j R), \qquad M_{i+j+1} = (A^i R)^T G A (A^j R) = -(A^i R)^T C (A^j R). $$
The reduced matrices $\hat G$ and $\hat C$ are symmetric and $\hat L = \hat B$, so the same identities hold for $\hat M$ with $\hat A$ and $\hat R$. Let $i, j \le q - 1$. By Theorem 2, $A^i R = X \hat A^i \hat R$ and $A^j R = X \hat A^j \hat R$, so
$$ M_{i+j} = (\hat A^i \hat R)^T X^T G X (\hat A^j \hat R) = \hat M_{i+j}, \qquad M_{i+j+1} = -(\hat A^i \hat R)^T X^T C X (\hat A^j \hat R) = \hat M_{i+j+1}. $$
The values $i + j$ and $i + j + 1$ with $i, j \le q - 1$ cover $0, \ldots, 2q - 1$. $\square$

For one port ($p = 1$) with $G$, $C$ symmetric and $L = B$, the reduced model is a rational function with numerator degree at most $q - 1$ and denominator degree at most $q$ that matches $2q$ moments. So it is the Padé approximation of AWE, which is unique when its Hankel matrix is invertible. For an RC circuit with $G$ positive definite this Padé model is therefore stable, by Theorem 6.

**Theorem 4 (full order).** If $X$ has $n$ columns, then $\hat H = H$.

*Proof.* Then $X$ is an orthogonal $n \times n$ matrix, and $\hat G + s \hat C = X^T (G + sC) X$, so $(\hat G + s \hat C)^{-1} = X^T (G + sC)^{-1} X$ wherever either side exists, and $\hat L^T (\hat G + s\hat C)^{-1} \hat B = L^T X X^T (G + sC)^{-1} X X^T B = H(s)$. $\square$

**Theorem 5 (passivity).** Suppose $G + G^T$ is positive semidefinite, $C$ is symmetric positive semidefinite and $L = B$. Then $\hat G + \hat G^T$ and $\hat C$ have the same properties and $\hat L = \hat B$. For every $s$ with $\operatorname{Re} s > 0$ at which $\hat G + s \hat C$ is invertible, the Hermitian part $\tfrac12 (\hat H(s) + \hat H(s)^H)$ is positive semidefinite, and $\hat H(\bar s) = \overline{\hat H(s)}$.

*Proof.* $z^T (\hat G + \hat G^T) z = (Xz)^T (G + G^T)(Xz) \ge 0$, $\hat C^T = \hat C$ and $z^T \hat C z = (Xz)^T C (Xz) \ge 0$, and $\hat L = X^T B = \hat B$. Now fix $s$ and a complex vector $w$, and let $\xi = (\hat G + s \hat C)^{-1} \hat B w$. Then $w^H \hat H(s) w = (\hat B w)^H \xi = ((\hat G + s\hat C) \xi)^H \xi = \xi^H (\hat G^T + \bar s \hat C) \xi$, using that the matrices are real. The real part of this is
$$ \tfrac12 \xi^H (\hat G + \hat G^T) \xi + \operatorname{Re}(s) \, \xi^H \hat C \xi \ge 0, $$
since $\xi^H M \xi = \operatorname{Re}(\xi)^T M \operatorname{Re}(\xi) + \operatorname{Im}(\xi)^T M \operatorname{Im}(\xi)$ for a real symmetric $M$. The real part of $w^H \hat H w$ is $\tfrac12 w^H (\hat H + \hat H^H) w$. The last claim holds because all matrices are real. $\square$

This is the positive-real condition of a passive multiport, here on the set where $\hat H$ is defined. The same computation with $X = I$ shows that the original circuit has the property, so the theorem says that the congruence transform keeps it.

**Theorem 6 (poles).** Under the hypotheses of Theorem 5, if $\hat G$ is invertible, every pole of $\hat H$, that is every $\lambda$ with $\det(\hat G + \lambda \hat C) = 0$, has $\operatorname{Re} \lambda \le 0$. If moreover $G + G^T$ is positive definite, then $\operatorname{Re} \lambda < 0$. If $G$ and $C$ are symmetric and $G$ is positive definite, the poles are real and negative.

*Proof.* Let $(\hat G + \lambda \hat C) z = 0$ with $z \ne 0$. Then $z^H \hat G z + \lambda z^H \hat C z = 0$, and the real part gives $\tfrac12 z^H (\hat G + \hat G^T) z + \operatorname{Re}(\lambda) \, z^H \hat C z = 0$. If $z^H \hat C z = 0$, then $\hat C z = 0$ because $\hat C$ is positive semidefinite, so $\hat G z = 0$, which is impossible for invertible $\hat G$. So $z^H \hat C z > 0$ and $\operatorname{Re} \lambda = -\tfrac12 z^H (\hat G + \hat G^T) z / z^H \hat C z \le 0$. If $G + G^T$ is positive definite, so is $\hat G + \hat G^T$ (as $X$ has full column rank), and the inequality is strict. In the symmetric case, $\lambda = -z^H \hat G z / z^H \hat C z$ is a ratio of real numbers, negative when $\hat G$ is positive definite. $\square$

**Theorem 7 (running time).** With dense matrices and $k \le qp$ columns in $X$, PRIMA takes $\Theta(n^3)$ for the LU factorization of $G$, $\Theta(k n^2)$ for the solves and the products with $C$ in lines L1 and L4, $\Theta(k^2 n)$ for the Gram-Schmidt steps of lines L2, L5 and L6, and $\Theta(k n^2 + k^2 n)$ for line L8. It uses $\Theta(n^2 + k n)$ extra space.

*Proof.* Each of the $k$ columns is produced by one product with $C$ and two triangular solves, $\Theta(n^2)$, and is orthogonalized twice against at most $k$ earlier columns, $\Theta(k n)$ each. Line L8 forms $G X$ and $C X$ in $\Theta(k n^2)$ and the $k^2$ inner products in $\Theta(k^2 n)$. The LU factors take $\Theta(n^2)$ space and $X$ takes $\Theta(kn)$. $\square$

$\blacksquare$
