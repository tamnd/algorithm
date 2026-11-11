---
title: NTRUEncrypt decrypts correctly when no coefficient wraps, and NTRU-HPS never fails
proves: [correctness]
status: full
---

Let $R = \mathbb{Z}[x]/(x^N - 1)$. For an element $a$ of $R$ or of $R/qR$, $\|a\|_\infty$ is the largest absolute value of a coefficient, taken for the centered representative. For $u, v \in R$ with $\|u\|_\infty \le 1$, each coefficient of the cyclic product $u v$ is $\sum_j u_{i-j} v_j$, so
$$\|u v\|_\infty \le \|v\|_1, \tag{1}$$
where $\|v\|_1$ is the sum of the absolute values of the coefficients of $v$.

## Part 1: the 1998 scheme (lines L1 to L8)

**Lemma 1.** Let $(h, (f, f_p))$ come from lines L1 to L4 and $e$ from lines L5 and L6. Then $f e \equiv p r g + f m \pmod q$.

*Proof.* By line L3, $h \equiv p f_q g$, and by line L2, $f f_q \equiv 1 \pmod q$. So $f e \equiv f (r p f_q g + m) = p r g (f f_q) + f m \equiv p r g + f m \pmod q$, because $R$ is commutative. $\square$

**Theorem 1.** If every coefficient of the integer polynomial $A = p r g + f m \in R$ lies in $(-q/2, q/2]$, and $m$ has coefficients in $(-p/2, p/2]$, then line L8 returns $m$.

*Proof.* By Lemma 1, $f e \bmod q$ and $A$ agree modulo $q$. Each residue class modulo $q$ has exactly one representative in $(-q/2, q/2]$, and $A$ is that representative coefficient by coefficient, so line L7 sets $a = A$ in $R$. Modulo $p$, $A \equiv f m$ because $p r g \equiv 0$. Then $f_p a \equiv f_p f m \equiv m \pmod p$, by line L2. The centered representative of $m$ modulo $p$ is $m$ itself, so line L8 returns $m$. $\blacksquare$

**A sufficient condition.** With $r \in \mathcal{L}(d_r, d_r)$, $g \in \mathcal{L}(d_g, d_g)$, $f \in \mathcal{L}(d_f, d_f - 1)$ and $m$ ternary, (1) gives $\|p r g\|_\infty \le p \cdot 2 d_g$ and $\|f m\|_\infty \le 2 d_f - 1$. So if $q > 2 (2 p d_g + 2 d_f - 1)$, decryption never fails. For $N = 11$, $p = 3$, $d_f = 4$, $d_g = 3$ this bound is $25$, so $q = 256$ is enough. The 1998 parameters are smaller than this worst-case bound: there decryption fails with a small probability, and Theorem 1 is the exact condition.

## Part 2: the round 3 KEM NTRU-HPS (lines L9 to L17)

Let $q = 2^k$, $\Phi_1 = x - 1$, $\Phi_N = 1 + x + \dots + x^{N-1}$, with $N$ prime and $\Phi_N$ irreducible modulo 2 and modulo 3. Let $T$ be the set of polynomials of degree at most $N - 2$ with coefficients in $\{-1, 0, 1\}$ (the samplers set the coefficient of $x^{N-1}$ to 0), and let $T_w \subset T$ be those with exactly $w/2$ coefficients 1 and $w/2$ coefficients $-1$, where $w = q/8 - 2$. Lines L9 and L12 take $f, r \in T$ and $g, m \in T_w$.

**Lemma 2 (unique representatives).** The map from $T$ to $\mathbb{Z}_3[x]/(\Phi_N)$, and the map from polynomials of degree at most $N - 2$ with coefficients in $(-q/2, q/2]$ to $\mathbb{Z}_q[x]/(\Phi_N)$, are bijections.

*Proof.* $\Phi_N$ is monic of degree $N - 1$, so every class has exactly one representative of degree at most $N - 2$, with coefficients in any fixed set of residues. $\square$

**Lemma 3 (the inverses exist).** If $f \ne 0$ and $g \ne 0$, then $f$ is invertible modulo $(3, \Phi_N)$ and $3 g f$ is invertible modulo $(q, \Phi_N)$.

*Proof.* $\mathbb{F}_3[x]/(\Phi_N)$ and $\mathbb{F}_2[x]/(\Phi_N)$ are fields. A nonzero element of $T$ is nonzero in both, by Lemma 2 with the residues $\{-1, 0, 1\}$ and since a ternary polynomial is $0$ modulo 2 only if it is $0$. So $f$ is invertible modulo 3, and $3 g f \equiv g f$ is invertible modulo 2. An element that is invertible modulo 2 is invertible modulo $2^k$, by the Newton lift $b \leftarrow b (2 - a b)$. $\square$

**Lemma 4 (the key equation).** Line L10 gives $h f \equiv 3 g \pmod{(q, x^N - 1)}$.

*Proof.* Modulo $(q, \Phi_N)$, $h = (3g)^2 (3 g f)^{-1} = 3 g f^{-1}$, so $h f \equiv 3g$. Modulo $(q, \Phi_1)$, that is at $x = 1$: $g(1) = 0$ because $g \in T_w$ has as many coefficients 1 as $-1$, and $h(1) = 0$ because $h$ is computed as $(3 g)^2$ times an element, so both sides are $0$. The resultant of $\Phi_1$ and $\Phi_N$ is $\Phi_N(1) = N$, which is odd, so it is a unit modulo $q = 2^k$, and by the Chinese remainder theorem $\mathbb{Z}_q[x]/(x^N - 1) \cong \mathbb{Z}_q[x]/(\Phi_1) \times \mathbb{Z}_q[x]/(\Phi_N)$. Both components agree, so the congruence holds modulo $x^N - 1$. $\square$

The packing of $h$ and $c$ drops the coefficient of $x^{N-1}$ and restores it from $a(1) = 0$. This is lossless because $h(1) = 0$ by Lemma 4 and $c(1) = r(1) h(1) + m(1) = 0$.

**Lemma 5 (no wrap).** For $c = r h + m \bmod q$ from line L13, $c f \equiv 3 r g + m f \pmod{(q, x^N - 1)}$, and every coefficient of $3 r g + m f$ is at most $q/2 - 8$ in absolute value.

*Proof.* The congruence follows from Lemma 4. By (1) with $\|r\|_\infty \le 1$ and $\|g\|_1 = w$, $\|3 r g\|_\infty \le 3 w$; with $\|f\|_\infty \le 1$ and $\|m\|_1 = w$, $\|m f\|_\infty \le w$. So the bound is $4 w = q/2 - 8$. $\square$

**Theorem 2.** Let $f, g \ne 0$. For every key pair from lines L9 to L11 and every $(c, K)$ from lines L12 to L14, line L17 returns $K$.

*Proof.* By Lemma 5 and the argument of Theorem 1, the centered value $a$ of line L15 equals $3 r g + m f$ over the integers. Modulo 3 it is $m f$, and multiplying by $f_3 = f^{-1} \bmod (3, \Phi_N)$ (Lemma 3) gives $m \bmod (3, \Phi_N)$. Line L15 reduces modulo $\Phi_N$ to a representative of degree at most $N - 2$ with coefficients in $\{-1, 0, 1\}$; since $m \in T$, Lemma 2 gives $m' = m$, which has fixed type.

In line L16, $c - m' = c - m \equiv r h \pmod q$. Modulo $\Phi_N$, $h h_q = (3 g f^{-1}) (f (3g)^{-1}) = 1$, so $(c - m') h_q \equiv r \pmod{(q, \Phi_N)}$. Since $r \in T$ has centered coefficients in $\{-1, 0, 1\}$ and degree at most $N - 2$, Lemma 2 gives $r' = r$, which is ternary. Both checks of line L17 pass, and it returns $\mathrm{SHA3\text{-}256}(r \| m)$ on the same packed trits as line L14, that is $K$. $\blacksquare$

**Remarks.** The bound $q/2 - 8 < q/2$ holds for every input, so NTRU-HPS has no decryption failures at all; this is what makes its CCA reduction tight. The condition $f, g \ne 0$ fails only if the sampler outputs the zero polynomial, which for $g \in T_w$ is impossible and for $f$ has negligible probability. Since decapsulation recovers $r$ and $m$ exactly, the checks of line L17 accept exactly the ciphertexts that line L13 can produce, so no re-encryption is needed.
