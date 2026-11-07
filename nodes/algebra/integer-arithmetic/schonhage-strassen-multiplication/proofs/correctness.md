---
title: SSA-MULMOD returns the product modulo 2^n + 1
proves: [correctness, termination]
status: full
---

Fix $n$ and residues $0 \le A, B \le 2^n$. Write $R_m = \mathbb{Z}/(2^m + 1)$. In $R_m$, $2^m = -1$ and $2^{2m} = 1$, and since $2^m + 1$ is odd, 2 is a unit.

**Base cases.** If $A = 2^n$ then $A \equiv -1$ and $AB \equiv -B$, and symmetrically for $B$; line L1 returns these. If $n$ is small, the product is computed directly and reduced, which is correct. From now on $0 \le A, B < 2^n$.

**Lemma 1 (negacyclic convolution).** Let $K = 2^k$ divide $n$, $M = n/K$, and $A = \sum_{j<K} a_j 2^{jM}$, $B = \sum_{j<K} b_j 2^{jM}$ with $0 \le a_j, b_j < 2^M$. Define

$$c_j = \sum_{i + l = j} a_ib_l - \sum_{i + l = j + K} a_ib_l \qquad (0 \le j < K) .$$

Then $AB \equiv \sum_{j<K} c_j 2^{jM} \pmod{2^n + 1}$, and $-(K - 1 - j)2^{2M} < c_j < (j + 1)2^{2M}$ when $c_j$ has a nonzero term, and $c_j = 0$ otherwise.

*Proof.* $AB = \sum_{i, l < K} a_ib_l 2^{(i + l)M}$. A term with $i + l = j + K$ has $2^{(j + K)M} = 2^{jM} 2^n \equiv -2^{jM}$. The first sum has $j + 1$ terms, each less than $2^{2M}$, and the second has $K - 1 - j$ terms. $\square$

**Lemma 2 (roots of unity).** Let $K \mid n'$, $\theta = 2^{n'/K}$ and $\omega = \theta^2$ in $R_{n'}$. Then $\theta^K = -1$, $\omega^{K/2} = -1$, and for $0 < s < K$, $\sum_{j<K} \omega^{sj} = 0$.

*Proof.* $\theta^K = 2^{n'} = -1$, and $\omega^{K/2} = \theta^K$. For $0 < s < K$ write $s = 2^e u$ with $u$ odd and $e < k$. Then $\omega^{s K/2^{e+1}} = (\omega^{K/2})^{u} = (-1)^u = -1$. Split the indices $j < K$ into pairs $j$ and $j + K/2^{e+1}$ within each block of length $K/2^e$; the two terms of a pair are $\omega^{sj}$ and $\omega^{sj} \cdot (-1)$, so each pair sums to 0. $\square$

Lemma 2 is all the [convolution theorem](/convolution-theorem/) needs: for sequences $x, y$ of length $K$ over $R_{n'}$ and $\mathrm{DFT}_\omega(x)_s = \sum_j x_j \omega^{sj}$,

$$\mathrm{DFT}_{\omega^{-1}}\big(\mathrm{DFT}_\omega(x) \cdot \mathrm{DFT}_\omega(y)\big)_j = K \sum_{i + l \equiv j \ (\mathrm{mod}\ K)} x_iy_l ,$$

because expanding the left side gives $\sum_{i,l} x_iy_l \sum_s \omega^{s(i + l - j)}$, and the inner sum is $K$ if $i + l \equiv j$ and 0 otherwise by Lemma 2. The radix-2 recursion of `_fft` computes $\mathrm{DFT}_\omega$ by the usual split into even and odd indices, which is valid in any commutative ring with $\omega^{K/2} = -1$.

**Lemma 3 (weights).** With $x_i = \theta^i a_i$ and $y_l = \theta^l b_l$, $\sum_{i + l \equiv j \ (\mathrm{mod}\ K)} x_iy_l = \theta^j c_j$ in $R_{n'}$.

*Proof.* A pair with $i + l = j$ contributes $\theta^j a_ib_l$, and a pair with $i + l = j + K$ contributes $\theta^{j + K} a_ib_l = -\theta^j a_ib_l$, since $\theta^K = -1$. $\square$

**Lemma 4 (recovery).** If $n' \ge 2M + k + 1$, line L9 turns the residue of $c_j$ in $R_{n'}$ into the integer $c_j$.

*Proof.* By Lemmas 2 and 3 and the induction hypothesis on line L6 (below), line L7 gives $K\theta^j c_j$ in $R_{n'}$, and line L8 multiplies by the inverse of $K\theta^j = 2^{k + jn'/K}$, which is $2^{2n' - k - jn'/K}$ since $2^{2n'} = 1$; so it gives $r_j = c_j \bmod (2^{n'} + 1)$ in $[0, 2^{n'}]$. By Lemma 1, $c_j$ lies in the open interval $(-(K - 1 - j)2^{2M}, (j + 1)2^{2M})$ or is 0, whose length $K 2^{2M} \le 2^{n' - 1}$ is less than the modulus. If $c_j \ge 0$, then $r_j = c_j < (j + 1)2^{2M}$ and line L9 keeps it. If $c_j < 0$, then $r_j = c_j + 2^{n'} + 1 > 2^{n'} + 1 - K2^{2M} \ge 2^{n' - 1} \ge K 2^{2M} \ge (j + 1)2^{2M}$, and line L9 subtracts the modulus, giving $c_j$. $\square$

**Theorem.** SSA-MULMOD returns $AB \bmod (2^n + 1)$, and terminates.

*Proof.* By strong induction on $n$. The base cases were treated above. Otherwise, the recursive calls of line L6 are on residues in $R_{n'}$ with $n' < n$ (the implementation takes the base case whenever its choice gives $n' \ge n$), so by the induction hypothesis they return $\hat a_j \hat b_j$ in $R_{n'}$. By Lemma 4 the values after line L9 are the integers $c_j$, and by Lemma 1 line L10 returns $\sum_j c_j 2^{jM} \bmod (2^n + 1) = AB \bmod (2^n + 1)$. Since each call either is a base case or recurses on a strictly smaller $n'$, the recursion terminates. $\blacksquare$

**Remark (depth).** With $K$ about $\sqrt{n}$, $n' \le 2n/K + k + 1 + K$ is $O(\sqrt{n})$, so the bit length of the size halves at each level, up to a constant, and the depth of the recursion is $\log_2 \log_2 n + O(1)$.
