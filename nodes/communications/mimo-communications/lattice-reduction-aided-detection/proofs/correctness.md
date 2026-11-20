---
title: LR-aided detection is exact without noise, and LR-SIC is correct inside a noise radius within 2^((n-1)/2) of the lattice ML radius
proves: [correctness]
status: full
---

Notation. $H_r \in \mathbb{R}^{m \times n}$ is the real channel with linearly independent columns $h_1, \ldots, h_n$, and $\Lambda = \{H_r z : z \in \mathbb{Z}^n\}$ is the lattice they generate. For a basis $b_1, \ldots, b_n$, the Gram-Schmidt vectors are $b^*_1 = b_1$ and $b^*_k = b_k - \sum_{j < k} \mu_{kj} b^*_j$ with $\mu_{kj} = \langle b_k, b^*_j \rangle / \|b^*_j\|^2$. The vectors $b^*_k$ are orthogonal, and $b_k = b^*_k + \sum_{j < k} \mu_{kj} b^*_j$.

**Lemma 1 (the real model and the shift).** $\|y - H x\|^2 = \|y_r - H_r x_r\|^2$, and with $x_r = (2 z - (q - 1) \mathbf 1) / s$ and $y' = (s\, y_r + (q - 1) H_r \mathbf 1) / 2$, the model $y = H x + w$ becomes $y' = H_r z + w'$ with $w' = \frac{s}{2} w_r$.

*Proof.* For complex $a = H x$, $\mathrm{Re}(H x) = \mathrm{Re} H\, \mathrm{Re} x - \mathrm{Im} H\, \mathrm{Im} x$ and $\mathrm{Im}(H x) = \mathrm{Im} H\, \mathrm{Re} x + \mathrm{Re} H\, \mathrm{Im} x$, which is $H_r x_r$ for QAM; for PAM, $\mathrm{Im} x = 0$ and the second block column drops out. A complex vector and its stacked real and imaginary parts have the same squared norm. For the shift, $y_r = H_r x_r + w_r = H_r (2 z - (q - 1) \mathbf 1) / s + w_r$. Multiply by $s / 2$ and add $(q - 1) H_r \mathbf 1 / 2$. $\square$

**Lemma 2 (unimodular change of basis).** If $T \in \mathbb{Z}^{n \times n}$ with $|\det T| = 1$, then $T^{-1} \in \mathbb{Z}^{n \times n}$, the columns of $B = H_r T$ generate $\Lambda$, and $u \mapsto T u$ is a bijection of $\mathbb{Z}^n$.

*Proof.* $T^{-1} = \mathrm{adj}(T) / \det T$, and the adjugate of an integer matrix is an integer matrix. So $T$ and $T^{-1}$ both map $\mathbb{Z}^n$ into $\mathbb{Z}^n$, and $B \mathbb{Z}^n = H_r T \mathbb{Z}^n = H_r \mathbb{Z}^n$. $\square$

**Theorem 3 (LLL).** For $1/4 < \delta < 1$, the LLL loop terminates. At the end, $B = H_r T$ with $T$ an integer matrix with $|\det T| = 1$, $|\mu_{kj}| \le 1/2$ for $j < k$, and $\|b^*_k\|^2 \ge (\delta - \mu_{k,k-1}^2) \|b^*_{k-1}\|^2$ for $k \ge 2$.

*Proof.* Invariant. The loop changes the basis only by $b_k \leftarrow b_k - c\, b_j$ with an integer $c$ and $j < k$, or by a swap of $b_{k-1}$ and $b_k$, and it applies the same operation to the columns of $T$. Both operations multiply $T$ on the right by an integer matrix of determinant $\pm 1$, so $B = H_r T$, $T$ is an integer matrix and $|\det T| = 1$ at all times, starting from $T = I$.

Size reduction. $b_k \leftarrow b_k - c\, b_j$ with $j < k$ does not change any $b^*_i$, because $b_j$ lies in the span of $b^*_1, \ldots, b^*_j$. It changes $\mu_{kl}$ to $\mu_{kl} - c \mu_{jl}$ for $l \le j$ (with $\mu_{jj} = 1$) and leaves $\mu_{kl}$ for $l > j$ unchanged. The loop runs $j = k - 1$ down to 1 and chooses $c = \lfloor \mu_{kj} + 1/2 \rfloor$, so after step $j$, $|\mu_{kj}| \le 1/2$, and later steps (with smaller $j$) do not change it.

Termination. Let $d_i = \prod_{l \le i} \|b^*_l\|^2$, the squared volume of the sublattice spanned by $b_1, \ldots, b_i$, and let $P = \prod_{i = 1}^{n - 1} d_i$. Size reduction does not change $P$. A swap at position $k$ changes only $d_{k-1}$, which is multiplied by $\|b'^*_{k-1}\|^2 / \|b^*_{k-1}\|^2$, where $b'^*_{k-1} = b^*_k + \mu_{k,k-1} b^*_{k-1}$ is the new Gram-Schmidt vector. So $\|b'^*_{k-1}\|^2 = \|b^*_k\|^2 + \mu_{k,k-1}^2 \|b^*_{k-1}\|^2 < \delta \|b^*_{k-1}\|^2$ when the Lovász condition fails, and $P$ is multiplied by less than $\delta$. Each $d_i$ is the squared determinant of an $i$-dimensional sublattice of $\Lambda$. By the definition of the Hermite constant $\gamma_i$, the sublattice has a nonzero vector of squared length at most $\gamma_i d_i^{1/i}$, and that vector is in $\Lambda$, so $d_i \ge (\lambda_1^2 / \gamma_i)^i > 0$, with $\lambda_1$ the length of a shortest nonzero vector of $\Lambda$. So $P$ has a positive lower bound that does not depend on the basis, and the number of swaps is at most $\log_{1/\delta}(P_0 / P_{\min})$, with $P_0$ the initial value. Between two swaps, $k$ grows by one at each step, so the loop ends.

Reduced prefix. At the start of each iteration with current position $k$ (1-based), the vectors $b_1, \ldots, b_{k-1}$ are size-reduced and satisfy the Lovász condition among themselves. This holds for $k = 2$. An iteration size-reduces $b_k$, which changes no other vector and no $b^*_i$. If the test passes, $b_1, \ldots, b_k$ are reduced and $k$ grows by one. If it fails, the swap changes only positions $k - 1$ and $k$, and $k$ becomes $\max(k - 1, 2)$, so the prefix up to the new $k - 1$ is unchanged. The loop ends with $k = n + 1$, so the whole basis is reduced. $\square$

**Theorem 4 (exact without noise).** If $w = 0$, the detector returns $x$, with or without reduction, for both ZF and SIC.

*Proof.* By Lemma 1, $y' = H_r z$ with $z \in \{0, \ldots, q - 1\}^n$. Let $u^\ast = T^{-1} z$, an integer vector by Lemma 2, so $y' = B u^\ast$. ZF: $B^+ y' = (B^T B)^{-1} B^T B u^\ast = u^\ast$, which rounding does not change. SIC: Lemma 5 below with $w' = 0$. Then $T u^\ast = z$, which lies in the box, so clipping does not change it, and line L8 maps $z$ to the points of $x$. $\square$

**Lemma 5 (SIC, the nearest plane step).** Let $y' = B u^\ast + w'$ with $u^\ast \in \mathbb{Z}^n$ and $\|w'\| < \frac12 \min_i \|b^*_i\|$. Then line L5 returns $u = u^\ast$.

*Proof.* By downward induction on $i$. Assume $u_l = u^\ast_l$ for all $l > i$. Then the residual before step $i$ is $r = \sum_{l \le i} u^\ast_l b_l + w'$. For $l < i$, $b_l$ lies in the span of $b^*_1, \ldots, b^*_{i-1}$, which is orthogonal to $b^*_i$, and $\langle b_i, b^*_i \rangle = \|b^*_i\|^2$. So

$$\frac{\langle r, b^*_i \rangle}{\|b^*_i\|^2} = u^\ast_i + \frac{\langle w', b^*_i \rangle}{\|b^*_i\|^2}, \qquad \Big| \frac{\langle w', b^*_i \rangle}{\|b^*_i\|^2} \Big| \le \frac{\|w'\|}{\|b^*_i\|} < \frac12$$

by the Cauchy-Schwarz inequality. So rounding gives $u_i = u^\ast_i$. $\square$

**Theorem 6 (the noise radius of LR-SIC).** After LLL with $\delta = 3/4$, $\min_i \|b^*_i\|^2 \ge 2^{-(n-1)} \lambda_1^2$. So if $\|w'\| < 2^{-(n-1)/2} \lambda_1 / 2$, LR-SIC returns the transmitted $x$.

*Proof.* Size reduction gives $\mu_{k,k-1}^2 \le 1/4$, so the Lovász condition gives $\|b^*_k\|^2 \ge (3/4 - 1/4) \|b^*_{k-1}\|^2 = \frac12 \|b^*_{k-1}\|^2$. By induction, $\|b^*_i\|^2 \ge 2^{-(i-1)} \|b^*_1\|^2 = 2^{-(i-1)} \|b_1\|^2 \ge 2^{-(n-1)} \lambda_1^2$, since $b_1$ is a nonzero vector of $\Lambda$. Under the assumption on $w'$, Lemma 5 gives $u = u^\ast = T^{-1} z$, so line L6 gives $z$, which is in the box, and the argument of Theorem 4 ends the proof. $\square$

For comparison, the nearest point of $\Lambda$ to $y'$ is $H_r z$ whenever $\|w'\| < \lambda_1 / 2$, because any other lattice point $v$ has $\|y' - v\| \ge \|v - H_r z\| - \|w'\| \ge \lambda_1 - \|w'\| > \|w'\|$. So the guarantee of Theorem 6 is smaller by the factor $2^{(n-1)/2}$, which depends only on $n$. Without reduction, $\min_i \|h^*_i\|$ has no lower bound in terms of $\lambda_1$. For example, the basis $h_1 = (N, 1)$, $h_2 = (1, 0)$ with an integer $N$ generates $\mathbb{Z}^2$, so $\lambda_1 = 1$, but $\|h^*_2\| = 1 / \sqrt{N^2 + 1}$, which goes to zero as $N$ grows. So plain SIC in this basis can fail at noise levels that LR-SIC always handles.

**Lemma 7 (ZF in the reduced basis).** If every entry of $B^+ w'$ lies in $[-1/2, 1/2)$, LR-ZF returns the transmitted $x$.

*Proof.* $B^+ y' = (B^T B)^{-1} B^T (B u^\ast + w') = u^\ast + B^+ w'$, and $\lfloor v + 1/2 \rfloor = u^\ast_i$ exactly when $v - u^\ast_i \in [-1/2, 1/2)$. So $u = u^\ast$, $T u = z$, clipping does not change $z$, and line L8 returns $x$. $\square$

**Lemma 8 (the MMSE form).** With $\tilde H = \begin{pmatrix} H_r \\ \sigma I \end{pmatrix}$ and $\tilde y = \begin{pmatrix} y' \\ \sigma c \mathbf 1 \end{pmatrix}$, $c = (q - 1)/2$, the metric $\|\tilde y - \tilde H z\|^2$ equals $\|y' - H_r z\|^2 + \sigma^2 \|z - c \mathbf 1\|^2$, and $\tilde H$ has linearly independent columns for every $\sigma > 0$.

*Proof.* The squared norm of a stacked vector is the sum of the squared norms of its blocks. If $\tilde H v = 0$, the lower block gives $\sigma v = 0$. $\square$

With $\sigma^2 = \frac{3 s^2 N_0}{2 (q^2 - 1)}$, the noise variance of $w'$ in one dimension, $s^2 N_0 / 8$, divided by the variance $(q^2 - 1)/12$ of a uniform $z_i$, this is the regularized metric of the MMSE detector in the integer coordinates. For unit-energy $M$-QAM, $s^2 = 2(q^2 - 1)/3$ gives $\sigma^2 = N_0$, and for $M$-PAM, $s^2 = (q^2 - 1)/3$ gives $\sigma^2 = N_0 / 2$ (closed forms). Theorems 3 to 6 apply to $\tilde H$ and $\tilde y$ unchanged, with the lattice generated by $\tilde H$.
