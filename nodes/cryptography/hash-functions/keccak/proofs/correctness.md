---
title: Keccak-f[1600] is a permutation and the Keccak sponge pads injectively
proves: [correctness]
status: full
---

We prove the facts that the page uses: each of the five step mappings is a bijection of the 1600-bit state, so Keccak-f[1600] is a permutation; the byte padding of lines L8 to L10 is injective; and lines L11 to L17 compute the sponge of FIPS 202 Algorithm 8. That the code is the standard function is checked by the XKCP and NIST test values, not proved. Nothing here proves that Keccak is secure; that rests on the sponge bound and on cryptanalysis.

**Lemma 1 ($\rho$, $\pi$ and $\iota$).** $\rho$, $\pi$ and $\iota$ are bijections of the state.

*Proof.* $\rho$ rotates each lane by a fixed amount, and rotation right by the same amount undoes it. $\pi$ sets $A'[x, y] = A[\sigma(x, y)]$ with $\sigma(x, y) = (x + 3y, x) \bmod 5$. The matrix $\begin{pmatrix} 1 & 3 \\ 1 & 0 \end{pmatrix}$ has determinant $-3$, which is not 0 modulo the prime 5, so $\sigma$ is a bijection of $\mathbb{Z}_5^2$ and $\pi$ only moves lanes. $\iota$ XORs a constant into lane $(0, 0)$, and XOR with the same constant undoes it. $\square$

**Lemma 2 ($\chi$).** $\chi$ is a bijection of the state.

*Proof.* $\chi$ acts on each row $(A[0, y], \ldots, A[4, y])$ and on each bit position $z$ separately: the output bit $(x, y, z)$ depends only on the bits $(x, y, z)$, $(x + 1, y, z)$ and $(x + 2, y, z)$. So $\chi$ is the same map $f$ of $\{0,1\}^5$ applied to $320$ disjoint 5-bit rows, with $f(a)_x = a_x \oplus (\neg a_{x+1} \wedge a_{x+2})$. A check of all 32 inputs shows that the 32 outputs of $f$ are distinct, so $f$ is a bijection, and so is $\chi$. $\square$

The check uses that 5 is odd: on rows of even length, the map $a_x \oplus (\neg a_{x+1} \wedge a_{x+2})$ is not a bijection, which is one reason for the $5 \times 5$ shape.

**Lemma 3 ($\theta$).** $\theta$ is a bijection of the state.

*Proof.* $\theta$ is linear over GF(2). Let $C[x] = \bigoplus_y A[x, y]$ be the column parities of $A$, and let $L(C)[x] = C[x] \oplus C[x-1] \oplus \mathrm{rot}(C[x+1], 1)$, a linear map on 320 bits. With $D[x] = C[x - 1] \oplus \mathrm{rot}(C[x + 1], 1)$, $\theta$ adds $D[x]$ to each of the 5 lanes of column $x$. So the parities of $A' = \theta(A)$ are $C'[x] = C[x] \oplus D[x]$, because $D[x]$ is added an odd number of times; that is, $C' = L(C)$. Gaussian elimination over GF(2) on the $320 \times 320$ matrix of $L$ gives rank 320, so $L$ is invertible. Now from $A'$ compute $C'$, then $C = L^{-1}(C')$, then $D$ from $C$, then $A = A' \oplus D$ lane by lane. This inverts $\theta$. $\square$

**Corollary.** KECCAK-F (lines L1 to L7) is a composition of $24 \times 5$ bijections, so it is a permutation of $\{0,1\}^{1600}$.

**Lemma 4 (padding).** Fix a byte $d$ with $d \ne 0$ and $d < \texttt{80}$, as for $d = \texttt{01}$, $\texttt{06}$ and $\texttt{1F}$. Lines L8 to L10 map $M$ to a string $P$ whose length is a positive multiple of $r$, and $P$ determines $M$.

*Proof.* After line L8, $|P| = |M| + 1$, and line L9 adds the least number of zero bytes that makes $|P|$ a multiple of $r$, so $|P| \ge 1$ is a multiple of $r$. Line L10 sets bit 7 of the last byte. To recover $M$ from $P$, clear bit 7 of the last byte. This gives back $M \| d \| 0^j$, because the last byte before line L10 was either a zero byte or $d$, and in both cases its bit 7 was 0. Then remove the trailing zero bytes. Because $d \ne 0$, the last remaining byte is $d$, and the bytes before it are $M$. $\square$

In bits, with the order of FIPS 202 Appendix B.1, $P$ is $M \| s \| 1 0^k 1$ where $s$ is the domain suffix (empty, 01 or 1111), which is $M \| s$ followed by pad10*1 of Algorithm 9.

**Lemma 5 (the sponge).** Lines L11 to L17 return the first $\ell$ bytes of $\mathrm{SPONGE}[\text{Keccak-f}[1600], \text{pad10*1}, 8r](M \| s, 8\ell)$.

*Proof.* Algorithm 8 sets $S = 0^{1600}$ and, for each block $P_i$ of $r$ bytes, sets $S \leftarrow f(S \oplus (P_i \| 0^{c}))$. Lines L11 to L13 do the same, since the byte order of the state matches Section 3.1. Algorithm 8 then sets $Z$ to the empty string and repeats: append $\mathrm{Trunc}_r(S)$ to $Z$; if $|Z| \ge \ell$ return $\mathrm{Trunc}_\ell(Z)$; else $S \leftarrow f(S)$. Lines L14 to L17 are these three steps. $\square$

By Lemmas 4 and 5, KECCAK[$c$] with $d = \texttt{01}$ is the function Keccak[$c$] of FIPS 202 Section 5.2, with $d = \texttt{06}$ it is SHA3 with $c = 2 \cdot 8\ell$, and with $d = \texttt{1F}$ it is SHAKE. The number of calls of KECCAK-F is $|P|/r = \lfloor n/r \rfloor + 1$ in the absorbing loop and $\lceil \ell/r \rceil - 1$ when squeezing.
