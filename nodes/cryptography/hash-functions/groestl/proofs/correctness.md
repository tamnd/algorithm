---
title: A collision of Grøstl gives a collision of the compression function or of the output transformation
proves: [correctness]
status: full
---

We use the notation of the page: $f(h, m) = P(h \oplus m) \oplus Q(m) \oplus h$, $\Omega(x) = \mathrm{trunc}_n(P(x) \oplus x)$, and the padding of Section 3.6.

**Lemma 1 (the rounds are permutations).** Each of AddRoundConstant, SubBytes, ShiftBytes and MixBytes is a bijection of the state, so $P$ and $Q$ are permutations.

*Proof.* XOR with a constant is its own inverse. The AES S-box is a bijection of bytes. ShiftBytes moves bytes within rows, and the shifts of each row are a rotation. The matrix $B = \mathrm{circ}(02, 02, 03, 04, 05, 03, 05, 07)$ is invertible over $\mathrm{GF}(2^8)$: the designers chose it as an MDS matrix, and MDS matrices are invertible because every square submatrix, including the whole matrix, is nonsingular. A composition of bijections is a bijection. $\square$

**Lemma 2 (padding is suffix-free and injective).** For messages $M \ne M'$, the padded strings differ, and if they have the same number of blocks then their last blocks hold the same block count.

*Proof.* The padded string is $M \| 1 \| 0^w \| \langle t \rangle_{64}$ with $t$ the number of blocks. The number of blocks $t$ and $w = (-N - 65) \bmod \ell$ fix $N$: from $t \ell = N + 1 + w + 64$ and $0 \le w < \ell$, $N$ is the unique value in its range with that $t$ and that remainder, and $M$ is read off as the first $N$ bits, ended by the last 1 before the zero run. So $M$ is recovered from the padded string, which proves injectivity. $\square$

**Theorem 1 (collision reduction).** If $M \ne M'$ and Grøstl-$n$$(M) =$ Grøstl-$n$$(M')$, then from the two computations one finds either two different inputs $x \ne x'$ with $\Omega(x) = \Omega(x')$, or two different inputs $(h, m) \ne (h', m')$ with $f(h, m) = f(h', m')$.

*Proof.* Let $h_t$ and $h'_{t'}$ be the final chaining values. If $h_t \ne h'_{t'}$, they are a collision of $\Omega$. Otherwise $h_t = h'_{t'}$. If $t \ne t'$, the last blocks differ in the block count, so $(h_{t-1}, m_t) \ne (h'_{t'-1}, m'_{t'})$ is a collision of $f$. If $t = t'$, walk back from $i = t$: at each step the outputs $h_i = h'_i$ are equal; if the inputs $(h_{i-1}, m_i)$ and $(h'_{i-1}, m'_i)$ differ, we have a collision of $f$, and else $h_{i-1} = h'_{i-1}$ and $m_i = m'_i$ and we go on. If all inputs are equal down to $i = 1$, all blocks are equal and Lemma 2 gives $M = M'$, a contradiction. $\square$

**Remark on the bounds.** The reduction is tight: it makes no extra queries and loses no probability. The cost of the two targets is what differs. A collision of $\Omega$ is a collision of an $n$-bit truncation of $x \mapsto P(x) \oplus x$, which costs about $2^{n/2}$ generically; this is the claimed collision level. A collision of $f$ costs at least about $2^{\ell/4} \ge 2^{n/2}$ queries when $P$ and $Q$ are ideal (Fouque, Stern and Zimmer). So the wide pipe $\ell \ge 2n$ is what lets the weaker bound of $f$, the square root of the generic $2^{\ell/2}$, still match the output. Preimages work the same way with $2^{\ell/2} \ge 2^n$.

**Theorem 2 (the code is Grøstl).** The code agrees with the official known-answer tests for Grøstl-256 and Grøstl-512 and with the official intermediate values for `abc`, which test $P$, $Q$, the padding, the IV and $\Omega$ for both state sizes. $\blacksquare$
