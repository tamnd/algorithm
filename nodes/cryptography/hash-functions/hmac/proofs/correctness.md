---
title: HMAC verification is exact, HMAC equals NMAC with derived keys, and equal padded keys give equal functions
proves: [correctness]
status: full
---

We use the notation of the page. $H$ has block size $B$ bytes and output length $L \le B$ bytes. For a byte string $x$, $|x|$ is its length in bytes.

**Lemma 1 (verification).** VERIFY$(H, K, m, T)$ returns true if and only if $1 \le |T| \le L$ and $T$ equals the first $|T|$ bytes of $\mathrm{HMAC}(H, K, m)$.

*Proof.* The code returns false when $|T| = 0$ or $|T| > L$. Otherwise line L5 sets $T'$ to the first $|T|$ bytes of the tag. Line L6 sets $d = \bigvee_i (T'[i] \oplus T[i])$. A byte $T'[i] \oplus T[i]$ is zero if and only if $T'[i] = T[i]$, and an OR of bytes is zero if and only if each of them is zero. So $d = 0$ if and only if $T' = T$, and line L7 returns exactly this. $\square$

**Lemma 2 (key handling).** Let $K_1, K_2$ be two keys. If $K'_1 = K'_2$ after lines L1 and L2, then $\mathrm{HMAC}(K_1, m) = \mathrm{HMAC}(K_2, m)$ for every $m$. In particular: (a) if $|K| + j \le B$, then $K$ and $K \| 0^j$ give the same function; (b) if $|K| > B$, then $K$ and $H(K)$ give the same function.

*Proof.* Lines L3 and L4 depend on $K$ only through $K'$, which gives the first statement. For (a), both keys have at most $B$ bytes, so line L1 does nothing, and line L2 pads both with zero bytes to the same string of $B$ bytes. For (b), line L1 replaces $K$ by $H(K)$, which has $L \le B$ bytes; the key $H(K)$ itself has $L \le B$ bytes, so line L1 leaves it, and line L2 gives the same $K'$ for both. $\square$

**Lemma 3 (HMAC is NMAC).** Let $H$ be a Merkle-Damgård hash: $H(x) = f^{*}(\mathrm{IV}, x \| p(|x|))$, where $p(\ell)$ is the padding for an input of $\ell$ bytes, $x \| p(|x|)$ has a length that is a multiple of $B$, and $f^{*}(k, y_1 \cdots y_r) = f(\ldots f(f(k, y_1), y_2) \ldots, y_r)$ iterates the compression function $f$ over the blocks $y_i$ of $B$ bytes. Define, for a chaining value $k$ and a string $x$,
$$F_k(x) = f^{*}(k, x \| p(B + |x|)).$$
Let $k_2 = f(\mathrm{IV}, K' \oplus \mathrm{ipad})$ and $k_1 = f(\mathrm{IV}, K' \oplus \mathrm{opad})$. Then $\mathrm{HMAC}(K, m) = F_{k_1}(F_{k_2}(m))$.

*Proof.* Let $X = K' \oplus \mathrm{ipad}$, a string of exactly $B$ bytes. The input of line L3 is $X \| m$, of length $B + |m|$, so
$$H(X \| m) = f^{*}(\mathrm{IV}, X \| m \| p(B + |m|)).$$
Because $|X| = B$, the first block of $X \| m \| p(B + |m|)$ is $X$, and the other blocks are the blocks of $m \| p(B + |m|)$; this string has a length that is a multiple of $B$ because the whole string has one and $|X| = B$. By the definition of $f^{*}$, iterating over a first block $X$ and then over the rest is the same as iterating over the rest from the chaining value $f(\mathrm{IV}, X)$. So
$$h = H(X \| m) = f^{*}(f(\mathrm{IV}, X), m \| p(B + |m|)) = F_{k_2}(m).$$
The same argument with $Y = K' \oplus \mathrm{opad}$ and the input $Y \| h$ of line L4 gives $H(Y \| h) = F_{k_1}(h)$. Together, $\mathrm{HMAC}(K, m) = F_{k_1}(F_{k_2}(m))$. $\square$

**Remarks.** Lemma 3 is the reason why results on NMAC transfer to HMAC: the HMAC keys are $k_1$ and $k_2$, computed from one key with $f$ keyed through its message input. The extra assumption in Bellare (2006) is that these two derived values look like two independent uniform chaining values. The padding $p(B + |x|)$ in $F_k$ is a fixed function of $|x|$, so $F$ is a keyed iterated hash in the sense of the NMAC analysis. Lemma 3 needs the Merkle-Damgård structure; for a sponge such as SHA-3 the first block does not give a chaining value of $c$ bits that stands for a key, and HMAC-SHA-3 is analysed differently.
