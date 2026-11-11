---
title: FrodoKEM decapsulation returns the encapsulated secret when the noise is small
proves: [correctness]
status: full
---

Let $q = 2^D$, $\bar n = 8$ and $1 \le B < D$. Write $\Delta = q / 2^B$ and $h = \Delta / 2 = 2^{D - B - 1}$. All matrix entries are taken modulo $q$ unless they are said to be integers. Encode places a $B$-bit chunk $k$ at $k \Delta$, and Decode maps an entry $x \in [0, q)$ to $\lfloor (x + h) / \Delta \rfloor \bmod 2^B$.

**Lemma 1 (Decode).** If $x \equiv k \Delta + \epsilon \pmod q$ with $0 \le k < 2^B$ and an integer $\epsilon$ with $-h \le \epsilon < h$, then Decode returns $k$.

*Proof.* Let $y = k\Delta + \epsilon + h$. Then $k\Delta \le y < (k+1)\Delta$, so $\lfloor y / \Delta \rfloor = k$. The entry $x$ is $y - h$ reduced into $[0, q)$, so $x + h \equiv y \pmod q$. Since $q = 2^B \Delta$, adding or removing a multiple of $q$ changes $\lfloor \cdot / \Delta \rfloor$ by a multiple of $2^B$, and Decode reduces modulo $2^B$. So Decode returns $k \bmod 2^B = k$. $\square$

**Lemma 2 (the noise).** Let $B_{pk} = A S + E$ from line L4, and let $B' = S' A + E'$, $V = S' B_{pk} + E''$ and $C = V + \mathrm{Encode}(\mu)$ from lines L10 and L11. Then line L14 computes $M = \mathrm{Encode}(\mu) + N_e$ with
$$N_e = S' E - E' S + E''.$$

*Proof.* Pack and Unpack are inverse on values in $[0, q)$, so decapsulation reads the same $B'$ and $C$, and the secret key holds $S^\mathsf{T}$ as 16-bit signed integers, which recovers $S$. Then
$$M = S'(A S + E) + E'' + \mathrm{Encode}(\mu) - (S' A + E') S = \mathrm{Encode}(\mu) + S' E + E'' - E' S,$$
because $S'(A S) = (S' A) S$. $\square$

**Theorem.** Let $(pk, sk)$ come from lines L1 to L6 and $(ct, ss)$ from lines L7 to L13. If every entry of $N_e$, taken as an integer, lies in $[-h, h)$, then lines L14 to L19 return $ss$.

*Proof.* By Lemma 2, each entry of $M$ is $k \Delta + \epsilon$ where $k$ is the chunk of $\mu$ at that place and $\epsilon$ is the entry of $N_e$. By Lemma 1, line L15 returns $\mu' = \mu$. The secret key holds $pkh = \mathrm{SHAKE}(pk, len)$ (line L5), which is the value used in line L8, so line L16 computes $(seedSE', k') = (seedSE, k)$. Lines L9 to L11 are a deterministic function of $(pk, seedSE, \mu)$, and the secret key holds $pk$, so line L17 computes $B'' = B'$ and $C' = C$. Line L18 then returns $\mathrm{SHAKE}(ct \| k, len) = ss$. $\blacksquare$

**When the condition holds.** Each entry of $S'E$ and of $E'S$ is a sum of $n$ products of two values from $\chi$, and each entry of $E''$ is one value from $\chi$. For FrodoKEM-640, $h = 2^{12} = 4096$ and $\chi$ has $\sigma = 2.8$, so an entry of $N_e$ has standard deviation about $\sqrt{2n} \sigma^2 \approx 280$, more than 14 standard deviations below $h$. The specification computes the distribution of one entry exactly by convolution and takes a union bound over the 64 entries, which gives the failure rate stated on the page. This part is a probability statement; the theorem above is exact.
