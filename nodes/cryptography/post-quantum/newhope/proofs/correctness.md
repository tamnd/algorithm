---
title: NewHope decapsulation returns the encapsulated key when the noise is small
proves: [correctness]
status: full
---

Let $n = 512$, $q = 12289$, $h = \lfloor q/2 \rfloor = 6144$ and $R_q = \mathbb{Z}_q[x]/(x^n + 1)$. For $a \in \mathbb{Z}_q$ let $\bar a$ be its representative in $(-q/2, q/2)$.

**The NTT as a ring map.** Let $\phi$ be the inverse NTT of line L12 (bit-reverse, butterflies, scaling), from vectors in $\mathbb{Z}_q^n$ to $R_q$, and let $\pi$ be the bit reversal of indices. The reference transform satisfies $\phi(\mathrm{NTT}(p)) = p^\pi$ (the vector $p$ read in bit-reversed order) and $\phi(\hat x \circ \hat y) = \phi(\hat x)\,\phi(\hat y)$, the product in $R_q$; the tests check both. So $\phi$ is a ring isomorphism from $(\mathbb{Z}_q^n, +, \circ)$ onto $R_q$. Write $A = \phi(\hat a)$, $S = s^\pi$, $E = e^\pi$, $S' = s'^\pi$ and $E' = e'^\pi$.

**Lemma 1 (the noise).** Let $c = (\hat u, \mathrm{Compress}(v'))$ come from lines L6 to L10 with the public key of lines L1 to L5, and let $c_v = \mathrm{Decompress}(\mathrm{Compress}(v')) - v'$. Then the value $w = \phi(\hat s \circ \hat u) - \mathrm{Decompress}(\mathrm{Compress}(v'))$ of line L12 satisfies
$$w = -(\mathrm{Encode}(\mu) + n_e), \qquad n_e = E S' - S E' + e'' + c_v.$$

*Proof.* By line L4, $\phi(\hat b) = A S + E$. By line L8, $\phi(\hat u) = A S' + E'$. By line L9, $v' = \phi(\hat b)\,S' + e'' + \mathrm{Encode}(\mu) = (A S + E) S' + e'' + \mathrm{Encode}(\mu)$. The packing of $\hat u$ and $\hat s$ with 14 bits per coefficient is lossless, so line L12 sees the same $\hat u$ and $\hat s$, and $\phi(\hat s \circ \hat u) = S (A S' + E')$. Subtract, and use $S A S' = A S S'$ in the commutative ring $R_q$. $\square$

**Lemma 2 (Decode).** Let $m \in \{0, 1\}$ and let $x_1, x_2 \in \mathbb{Z}_q$ with $x_j \equiv -(m h + \nu_j)$ for integers $\nu_j$ with $|\nu_1| + |\nu_2| < h - 2$. Write $t = |x_1 - h| + |x_2 - h|$, with $x_j$ taken in $[0, q)$. Then $t < h$ if $m = 1$ and $t \ge h$ if $m = 0$, so Decode returns $m$.

*Proof.* Case $m = 0$. Then $x_j \equiv -\nu_j$. If $\nu_j \le 0$, $x_j = |\nu_j|$ and $|x_j - h| = h - |\nu_j|$. If $\nu_j > 0$, $x_j = q - \nu_j$ and $|x_j - h| = q - h - \nu_j = h + 1 - |\nu_j|$. In both cases $|x_j - h| \ge h - |\nu_j|$, so $t \ge 2h - (|\nu_1| + |\nu_2|) > h$.

Case $m = 1$. Then $x_j \equiv -h - \nu_j \equiv h + 1 - \nu_j$, because $q = 2h + 1$. Since $|\nu_j| < h - 2$, the integer $h + 1 - \nu_j$ lies in $(3, q - 2)$, so $x_j = h + 1 - \nu_j$ and $|x_j - h| = |1 - \nu_j| \le 1 + |\nu_j|$. So $t \le 2 + |\nu_1| + |\nu_2| < h$. $\square$

**Theorem.** Let $(pk, sk)$ come from line L13 and $(c, ss)$ from lines L14 to L16 with the key $K$. If $|\bar n_{e,i}| + |\bar n_{e,i+256}| < h - 2 = 6142$ for every $i < 256$, then line L17 returns $ss$.

*Proof.* Encode puts bit $i$ of $K$ as $m_i h$ in coefficients $i$ and $i + 256$. By Lemma 1, coefficient $i + 256 j$ of $w$ is $-(m_i h + n_{e, i+256j})$, so Lemma 2 with $\nu_j = \bar n_{e, i + 256 j}$ shows that Decode returns $m_i$ for every $i$. So line L12 returns $K$, and line L17 returns $\mathrm{SHAKE256}(K, 32) = ss$. $\blacksquare$

**When the condition holds.** The coefficients of $s, e, s', e', e''$ come from $\psi_8$, with values in $[-8, 8]$ and variance 4. A coefficient of $E S'$ or $S E'$ is a sum of 512 products, with variance $512 \cdot 16 = 8192$, so standard deviation about 91, and the compression error is at most about $q/16 \approx 768$. The sum of two coefficients of $n_e$ is therefore far below 6142 except with very small probability; the specification computes the failure rate exactly. This part is a probability statement; the theorem above is exact.
