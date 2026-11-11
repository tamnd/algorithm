---
title: A UOV signature verifies, because the public map is the central map after a change of variables and the signer solves the central map exactly
proves: [correctness]
status: full
---

We use the notation of the page. $q$ is odd, $n = v + o$, $m = o$, and the first $v$ coordinates are vinegar. Each central matrix is symmetric of the form

$$F_k = \begin{pmatrix} A_k & B_k \\ B_k^T & 0 \end{pmatrix}, \qquad A_k \in \mathbb{F}_q^{v \times v},\ B_k \in \mathbb{F}_q^{v \times o},$$

with $f_k(x) = x^T F_k x$, and $P_k = S^T F_k S$ with $S$ invertible.

**Lemma 1 (public map).** For every $s \in \mathbb{F}_q^n$, $s^T P_k s = f_k(Ss)$.

*Proof.* $s^T S^T F_k S s = (Ss)^T F_k (Ss)$. $\square$

**Lemma 2 (linear in the oil variables).** Write $x = (x_v, x_o)$. Then $f_k(x) = x_v^T A_k x_v + 2 x_v^T B_k x_o$.

*Proof.* Expand $x^T F_k x = x_v^T A_k x_v + x_v^T B_k x_o + x_o^T B_k^T x_v + x_o^T 0\, x_o$. The two middle terms are the same scalar, since a $1 \times 1$ matrix equals its transpose. $\square$

**Theorem (correctness).** If SIGN returns $(s, \mathrm{salt})$ for a message $M$, then VERIFY$(pk, M, (s, \mathrm{salt}))$ accepts.

*Proof.* Let $t = H(M \,\|\, \mathrm{salt})$ from line L5 and $x_v$ the vinegar values of the last pass through line L6. By Lemma 2, line L7 builds the system $L x_o = c$ with rows $L_k = 2 x_v^T B_k$ and $c_k = t_k - x_v^T A_k x_v$, and its solutions are exactly the $x_o$ with $f_k(x_v, x_o) = t_k$ for all $k$. SIGN passes line L8 only when $L$ is invertible, so line L9 gives $x$ with $f_k(x) = t_k$ for all $k$. Line L10 returns $s = S^{-1} x$, and by Lemma 1 $s^T P_k s = f_k(x) = t_k$. VERIFY recomputes the same $t$ from $M$ and the salt and checks these $m$ equations in line L11. $\blacksquare$

**Termination.** Each pass through lines L6 to L8 succeeds when the $m \times m$ matrix $L$ is invertible. For a uniform matrix this has probability $\prod_{i=1}^{m}(1 - q^{-i}) > 1 - 1/(q - 1)$. The matrix $L$ is not exactly uniform, so this is a heuristic, but over random keys the expected number of passes is close to $1/(1 - 1/(q-1))$, and the tests confirm that signing is fast.

**Lemma 3 (the oil space).** Let $O = S^{-1}\{(0, x_o)\}$. Then $s^T P_k s' = 0$ for all $s, s' \in O$, so the public map vanishes on $O$. Conversely, any subspace $O^*$ of dimension $m$ on which all $P_k$ vanish lets anyone sign: for $y$ random and $s = y + u$ with $u \in O^*$, $s^T P_k s = y^T P_k y + 2 y^T P_k u$, which is linear in $u$.

*Proof.* For $s = S^{-1}(0, a)$ and $s' = S^{-1}(0, b)$, $s^T P_k s' = (0, a) F_k (0, b)^T = a^T \cdot 0 \cdot b = 0$. For the second part, $u^T P_k u = 0$ and $P_k$ is symmetric. $\square$

**Lemma 4 (Kipnis-Shamir).** Let $v = o$, and let $W_1 = \sum_k c_k P_k$ and $W_2 = \sum_k d_k P_k$ with $W_1$ invertible. Then $M = W_1^{-1} W_2$ maps $O$ into $O$, and the characteristic polynomial of $M$ is $g^2$, where $g$ is the characteristic polynomial of $M$ on $O$. Hence every eigenvector of $M$ whose eigenspace has dimension 1 lies in $O$.

*Proof.* $W_i = S^T G_i S$ with $G_1 = \sum c_k F_k$ and $G_2 = \sum d_k F_k$, which have the same block shape, with blocks $A, B$ and $A', B'$. $G_1$ is invertible, so $B$ is a square invertible matrix, and a direct check gives

$$G_1^{-1} = \begin{pmatrix} 0 & B^{-T} \\ B^{-1} & -B^{-1} A B^{-T} \end{pmatrix}, \qquad G_1^{-1} G_2 = \begin{pmatrix} B^{-T} B'^T & 0 \\ \ast & B^{-1} B' \end{pmatrix}.$$

The zero block means that $G_1^{-1} G_2$ maps $\{(0, x_o)\}$ into itself, and $M = S^{-1} G_1^{-1} G_2 S$ maps $O$ into $O$. The block triangular form gives the characteristic polynomial as the product of those of $B^{-1} B'$ (the action on $O$) and $B^{-T} B'^T = (B' B^{-1})^T$. The matrix $B' B^{-1}$ is similar to $B^{-1} B'$, so both factors equal $g$. If $\lambda$ is a root of $g$, then $M$ restricted to $O$ has an eigenvector for $\lambda$ inside $O$; if the eigenspace of $\lambda$ for $M$ has dimension 1, it is spanned by that vector. $\square$

The attack in the code adds a vector only if all $P_k$ still vanish on the span, a check that uses only the public key. So whatever space it returns has dimension $m$ and makes all $P_k$ vanish, and by Lemma 3 it lets the attacker sign, even if it were not $O$ itself. Lemma 4 explains why enough vectors appear when $v = o$; the tests also check that the returned space is $O$.
