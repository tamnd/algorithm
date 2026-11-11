---
title: CMAC verifies its own tags, its subkeys are field multiples, and its last-block encoding is injective
proves: [correctness]
status: full
---

Fix a block cipher $E_K$ with block length $n \in \{64, 128\}$ and the field $\mathrm{GF}(2^n) = \mathrm{GF}(2)[x]/(P(x))$ with $P(x) = x^{128} + x^7 + x^2 + x + 1$ for $n = 128$ and $P(x) = x^{64} + x^4 + x^3 + x + 1$ for $n = 64$. An $n$-bit string $a_{n-1} \cdots a_1 a_0$ (leftmost bit first) stands for the polynomial $\sum_i a_i x^i$. $R_n$ is the string of the coefficients of $P(x) - x^n$, which is $0^{120}10000111$ for $n = 128$.

**Lemma 1 (doubling is multiplication by $x$).** For every $n$-bit string $X$, $\mathrm{dbl}(X) = x \cdot X$ in $\mathrm{GF}(2^n)$.

*Proof.* Let $X = \sum_{i=0}^{n-1} a_i x^i$. Then $x \cdot X = \sum_{i=0}^{n-1} a_i x^{i+1} = a_{n-1} x^n + \sum_{i=1}^{n-1} a_{i-1} x^i$. The sum is the string $X \ll 1$ (the shift moves $a_{i-1}$ to position $i$ and drops $a_{n-1}$). Modulo $P(x)$ we have $x^n = P(x) - x^n$ over $\mathrm{GF}(2)$, which is the polynomial of $R_n$. So $x \cdot X = (X \ll 1) \oplus a_{n-1} R_n$, and $a_{n-1} = \mathrm{MSB}_1(X)$. This is the rule of lines L2 and L3. $\square$

**Lemma 2 (the subkeys).** $K_1 = x \cdot L$ and $K_2 = x^2 \cdot L$. The map $\mathrm{dbl}$ is a bijection, and $K_1 \ne K_2$, $K_1 \ne 0^n$ and $K_2 \ne 0^n$ unless $L = 0^n$.

*Proof.* The first sentence follows from Lemma 1 applied twice. Since $P$ is irreducible, $\mathrm{GF}(2^n)$ is a field, and $x \ne 0$ in it, so multiplication by $x$ is a bijection with inverse multiplication by $x^{-1}$. If $L \ne 0$, then $K_1 = xL \ne 0$ and $K_2 = x^2 L \ne 0$, because a field has no zero divisors. Also $K_1 \oplus K_2 = (x + x^2) L = x(1 + x) L$, and $x \ne 0$, $1 + x \ne 0$ (as $n \ge 2$), so $K_1 \oplus K_2 \ne 0$. $\square$

**Lemma 3 (verification accepts honest tags).** For every key, message and tag length $1 \le t \le n$, VERIFY$(K, M, \mathrm{CMAC}(K, M, t))$ accepts.

*Proof.* All steps of CMAC are deterministic functions of $K$, $M$ and $t$. Line L12 recomputes CMAC with $t = |T|$, which is the length of the given tag, and so obtains the same string, and a comparison of equal strings that reads every byte returns true. $\square$

For a message $M$, line L4 gives $m = \max(1, \lceil |M|/n \rceil)$ blocks, and the last part $M_m^*$ has length $|M| - (m-1)n$, which is in $\{1, \ldots, n\}$ if $M$ is not empty and is $0$ if $M$ is empty. For a string $B$ with $|B| < n$, let $\mathrm{pad}(B) = B \,\|\, 1 \,\|\, 0^{n - 1 - |B|}$. Call $M$ full if $|M_m^*| = n$ and padded otherwise.

**Lemma 4 (the padding is injective).** If $|B|, |B'| < n$ and $\mathrm{pad}(B) = \mathrm{pad}(B')$, then $B = B'$.

*Proof.* In $\mathrm{pad}(B)$ the last 1 bit is at position $|B| + 1$ from the left, because all bits after it are 0. So $|B|$ is determined by $\mathrm{pad}(B)$, and $B$ is its first $|B|$ bits. $\square$

**Theorem (the encoding).** Let $\mathrm{enc}(M) = (M_1, \ldots, M_{m-1}, M_m)$ be the block sequence of lines L5 and L6, so that CMAC is the CBC-MAC of $\mathrm{enc}(M)$ cut to $t$ bits.

1. If $M$ and $M'$ are both full or both padded and $\mathrm{enc}(M) = \mathrm{enc}(M')$, then $M = M'$.
2. If $M$ is full and $M'$ is padded, with the same number of blocks, then the last encoded blocks are equal only if $M_m^* \oplus \mathrm{pad}(M'^*_m) = K_1 \oplus K_2 = (x^2 + x) L$.

*Proof.* Equal sequences have equal lengths, so $m = m'$ and $M_i = M'_i$ for $i < m$. In part 1, if both are full, then $M_m^* \oplus K_1 = M'^*_m \oplus K_1$ gives $M_m^* = M'^*_m$. If both are padded, then $\mathrm{pad}(M_m^*) \oplus K_2 = \mathrm{pad}(M'^*_m) \oplus K_2$ gives $\mathrm{pad}(M_m^*) = \mathrm{pad}(M'^*_m)$, and Lemma 4 gives $M_m^* = M'^*_m$. In both cases $M = M'$. In part 2, $M_m^* \oplus K_1 = \mathrm{pad}(M'^*_m) \oplus K_2$ is the same as $M_m^* \oplus \mathrm{pad}(M'^*_m) = K_1 \oplus K_2$, and Lemma 2 gives the value $(x^2 + x)L$. $\blacksquare$

**Remark.** Part 2 is why two distinct subkeys are needed. With $K_1 = K_2$, the full message $\mathrm{pad}(B)$ and the padded message $B$ would have the same encoding and the same tag, for every key. With distinct subkeys the condition depends on the secret $L$, and in the security proof of Iwata and Kurosawa it holds with small probability. The trace of RFC 4493, Example 3, on the main page is an instance of the padded case, and Lemma 1 explains why $K_2$ there is $K_1$ shifted and XORed with `87`: the leftmost bit of $K_1$ = `fbee…` is 1.
