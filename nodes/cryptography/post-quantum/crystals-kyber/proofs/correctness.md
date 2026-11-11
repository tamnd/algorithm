---
title: ML-KEM decapsulation returns the encapsulated key when the noise is small
proves: [correctness]
status: full
---

Work in $R_q = \mathbb{Z}_q[X]/(X^{256}+1)$ with $q = 3329$. For $a \in \mathbb{Z}_q$ let $\|a\|$ be the distance from $a$ to 0 on the circle, that is $\min(a \bmod q, q - (a \bmod q))$, and for a polynomial let $\|f\|_\infty$ be the largest $\|f_i\|$. The NTT is a ring isomorphism from $R_q$ onto a product of 128 rings $\mathbb{Z}_q[X]/(X^2 - \zeta_i)$, and $\circ$ is the product there, so $\mathrm{NTT}^{-1}(\hat a \circ \hat b) = a b$ for all $a, b \in R_q$. All the identities below are therefore identities in $R_q$.

**Lemma 1 (rounding).** For $d < 12$ and $x \in \mathbb{Z}_q$, $\|\mathrm{Decompress}_d(\mathrm{Compress}_d(x)) - x\| \le \lceil q / 2^{d+1} \rfloor$. For $d = 1$: if $\|w - \lceil q/2 \rfloor \cdot \beta\| < \lceil q/4 \rfloor$ for a bit $\beta$, then $\mathrm{Compress}_1(w) = \beta$.

*Proof.* Let $y = \lceil 2^d x / q \rfloor$, so $|2^d x/q - y| \le 1/2$, hence $|x - q y / 2^d| \le q/2^{d+1}$. Decompress returns $x' = \lceil q y' / 2^d \rfloor$ with $y' = y \bmod 2^d$. If $y = 2^d$ then $y' = 0$ and $q y / 2^d = q \equiv 0$, so in both cases $x'$ is within $1/2$ of a real number congruent to $q y / 2^d$ modulo $q$. So $\|x' - x\| \le q / 2^{d+1} + 1/2$. The left side is an integer, so it is at most $\lfloor q/2^{d+1} + 1/2 \rfloor = \lceil q/2^{d+1} \rfloor$. For $d = 1$, Compress$_1(w) = \lceil 2w/q \rfloor \bmod 2$ is 1 exactly when $w$ is in $(q/4, 3q/4)$, the half of the circle around $q/2$. If $\|w\| < \lceil q/4 \rfloor = 832$, then $w \le 831 < q/4$ or $w \ge q - 831 > 3q/4$, so the result is 0. If $\|w - 1665\| < 832$, then $834 \le w \le 2496$, inside $(832.25, 2496.75)$, so the result is 1. $\square$

**Lemma 2 (the noise of K-PKE).** Let $(ek, dk_{PKE})$ come from lines L1 to L5 with secret $\mathbf{s}$, error $\mathbf{e}$ and $\mathbf{t} = A \mathbf{s} + \mathbf{e}$, and let $c$ come from lines L6 to L10 on the message $m$ with randomness $r$. Then line L12 computes $w = \mu + n_e$ with
$$n_e = \mathbf{e}^\mathsf{T}\mathbf{y} + e_2 + c_v - \mathbf{s}^\mathsf{T}\mathbf{e}_1 - \mathbf{s}^\mathsf{T}\mathbf{c}_u,$$
where $\mathbf{c}_u = \mathbf{u}' - \mathbf{u}$ and $c_v = v' - v$ are the compression errors.

*Proof.* Line L6 rebuilds the same $\hat A$ as line L2, because both read SampleNTT on the same seed $\rho$ with the same indices. ByteEncode$_{12}$ and ByteDecode$_{12}$ are inverse on $\mathbb{Z}_q$, so line L6 also recovers $\hat{t}$ and line L12 recovers $\hat{s}$. By lines L8 and L9, $\mathbf{u} = A^\mathsf{T}\mathbf{y} + \mathbf{e}_1$ and $v = \mathbf{t}^\mathsf{T}\mathbf{y} + e_2 + \mu$. ByteDecode inverts ByteEncode on values below $2^d$, so line L11 gives $\mathbf{u}' = \mathbf{u} + \mathbf{c}_u$ and $v' = v + c_v$. Then
$$w = v' - \mathbf{s}^\mathsf{T}\mathbf{u}' = (A\mathbf{s} + \mathbf{e})^\mathsf{T}\mathbf{y} + e_2 + \mu + c_v - \mathbf{s}^\mathsf{T}A^\mathsf{T}\mathbf{y} - \mathbf{s}^\mathsf{T}\mathbf{e}_1 - \mathbf{s}^\mathsf{T}\mathbf{c}_u,$$
and $(A\mathbf{s})^\mathsf{T}\mathbf{y} = \mathbf{s}^\mathsf{T}A^\mathsf{T}\mathbf{y}$ because $R_q$ is commutative. $\square$

**Lemma 3 (K-PKE decrypts).** If $\|n_e\|_\infty < \lceil q/4 \rfloor$, then line L13 returns $m$.

*Proof.* Line L9 sets the coefficient $\mu_i = \mathrm{Decompress}_1(m_i) = \lceil q/2 \rfloor \cdot m_i$ for each message bit $m_i$. By Lemma 2, $w_i = \mu_i + (n_e)_i$ with $\|(n_e)_i\| < \lceil q/4 \rfloor$, so Lemma 1 gives $\mathrm{Compress}_1(w_i) = m_i$. ByteEncode$_1$ then packs the 256 bits back into the 32 bytes of $m$. $\square$

**Theorem (ML-KEM).** Let $(ek, dk)$ come from line L22 and $(K, c)$ from line L23. If the noise of Lemma 2 for this encryption satisfies $\|n_e\|_\infty < \lceil q/4 \rfloor$, then line L24 returns $K$.

*Proof.* The key passes the checks: $ek$ was made by ByteEncode$_{12}$ of reduced values, so the modulus check of line L23 holds, and $dk$ holds $H(ek)$ in the place that line L24 checks. Line L16 sets $(K, r) = G(m \| H(ek))$ and line L17 sets $c = \text{K-PKE.Encrypt}(ek, m, r)$. Line L18 splits $dk$ into the parts written by line L15, so $h = H(ek)$. By Lemma 3, line L19 gets $m' = m$, so $(K', r') = G(m \| H(ek)) = (K, r)$. Line L20 runs K-PKE.Encrypt on the same $(ek, m, r)$; it is a deterministic function of its inputs, so $c' = c$. Line L21 keeps $K' = K$. $\blacksquare$

**The failure rate.** The theorem is exact; the only probabilistic part is the event $\|n_e\|_\infty \ge \lceil q/4 \rfloor$ over the key and the coins. All terms of $n_e$ have small coefficients (at most $\eta_1$ or $\eta_2$ for the samples and $\lceil q / 2^{d+1} \rfloor$ for the compression errors), so each coefficient of $n_e$ is a sum of a few thousand small terms. The Kyber papers compute the exact distribution of one coefficient by convolution and take a union bound over the 256 coefficients, which gives the rates of FIPS 203, about $2^{-139}$ for ML-KEM-512 and less for the larger sets.
