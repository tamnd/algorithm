---
title: Niederreiter decryption recovers the message, because a Goppa syndrome of weight t has one preimage and constant weight encoding is a bijection
proves: [correctness]
status: full
---

We use the notation of the page. $g$ is irreducible of degree $t$ over $\mathbb{F}_{2^m}$, $L = (\alpha_1, \ldots, \alpha_n)$ are distinct, and column $i$ of $H$ holds the $mt$ bits of the $t$ coefficients of $(x - \alpha_i)^{-1} \bmod g$. For $y \in \mathbb{F}_2^n$ let $S_y(x) = \sum_i y_i (x - \alpha_i)^{-1} \bmod g$.

**Lemma 1 (the syndrome is the syndrome polynomial).** For every $y$, the bits of $Hy^T$ are the bits of the coefficients of $S_y$, in the same layout as a column of $H$.

*Proof.* Addition in $\mathbb{F}_{2^m}$ is bitwise XOR of the coefficient bits, so the bit for coefficient $d$ and bit $b$ of $S_y$ is the XOR over $i$ with $y_i = 1$ of the same bit of $(x - \alpha_i)^{-1} \bmod g$. That is row $(d, b)$ of $H$ times $y^T$. $\square$

**Lemma 2 (unique preimage).** For each $s$ there is at most one $e$ with $\mathrm{wt}(e) \le t$ and $He^T = s$. If such an $e$ exists, Patterson's algorithm on $s$ returns it.

*Proof.* If $He_1^T = He_2^T$ with both weights at most $t$, then $H(e_1 + e_2)^T = 0$, so $e_1 + e_2$ is in $\Gamma(L, g)$ and has weight at most $2t$. Lemma 2 of the McEliece proof says that every nonzero codeword has weight at least $2t + 1$, so $e_1 = e_2$. By Lemma 1, the polynomial that the decoder reads from $s$ is $S_e$. Lemmas 3 and 4 of the McEliece proof show that, from $S_e$ with $\mathrm{wt}(e) \le t$, lines P2 to P6 compute a nonzero constant multiple of the error locator $\sigma_e = \prod_{e_i = 1}(x - \alpha_i)$. Its roots are exactly the $\alpha_i$ with $e_i = 1$, and the $\alpha_i$ are distinct, so line P7 returns $e$. $\square$

**Lemma 3 (constant weight encoding).** For $0 \le x < \binom{n}{t}$ there are unique integers $n > c_1 > \cdots > c_t \ge 0$ with $x = \sum_{j=1}^{t} \binom{c_j}{t - j + 1}$, CW-ENCODE finds them, and CW-DECODE inverts it.

*Proof.* Induction on $t$. For $t = 1$, $c_1 = x$. For $t > 1$, let $c_1$ be the largest $c$ with $\binom{c}{t} \le x$; it exists and $c_1 < n$ because $\binom{t-1}{t} = 0 \le x < \binom{n}{t}$. Then $x' = x - \binom{c_1}{t}$ satisfies $0 \le x' < \binom{c_1 + 1}{t} - \binom{c_1}{t} = \binom{c_1}{t-1}$, so by induction $x'$ has a unique form with $c_1 > c_2 > \cdots$. Uniqueness of $c_1$: for any valid form, $\sum_{j \ge 2} \binom{c_j}{t-j+1} \le \sum_{j \ge 2} \binom{c_1 - j + 1}{t - j + 1} = \binom{c_1}{t-1} - 1$, which is the identity $\sum_{i=0}^{t-2}\binom{c_1 - t + 1 + i}{i + 1} = \binom{c_1}{t-1} - 1$ by Pascal's rule; so $\binom{c_1}{t} \le x < \binom{c_1 + 1}{t}$, which fixes $c_1$. The map $x \mapsto \{c_1, \ldots, c_t\}$ is therefore injective from a set of size $\binom{n}{t}$ into the $t$-subsets of $\{0, \ldots, n-1\}$, which also has size $\binom{n}{t}$, so it is a bijection, and CW-DECODE, which evaluates the sum, is its inverse. $\square$

**Theorem (correctness of decryption).** For every $x$ with $0 \le x < \binom{n}{t}$, DECRYPT(sk, ENCRYPT(pk, $x$)) returns $x$.

*Proof.* By Lemma 3, line L5 gives $e$ with $\mathrm{wt}(e) = t$. Line L6 gives $s = MHPe^T$. Line L7 gives $s_1 = M^{-1}s = H e_1^T$ with $e_1^T = Pe^T$, and $\mathrm{wt}(e_1) = t$ because $P$ permutes positions. By Lemma 2, line L8 returns $e_1$. Line L9 gives $P^{-1}e_1^T = e^T$, and by Lemma 3 line L10 returns $x$. $\blacksquare$

**Remark.** The implementation also rejects any decoder output whose weight is not $t$. Lemma 2 shows that this check never fires on an honest ciphertext.
