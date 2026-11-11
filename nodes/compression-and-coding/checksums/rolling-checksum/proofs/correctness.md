---
title: The roll equals a recompute, the delta rebuilds the new file, and the Rabin window rolls exactly
proves: [correctness]
status: full
---

Let $M = 2^{16}$. For a window $X_k, \ldots, X_l$ of length $L = l - k + 1$, let $a(k, l) = \sum_{i=k}^{l} X_i \bmod M$ and $b(k, l) = \sum_{i=k}^{l} (l - i + 1) X_i \bmod M$.

**Lemma 1 (the roll).** $a(k+1, l+1) = (a(k, l) - X_k + X_{l+1}) \bmod M$ and $b(k+1, l+1) = (b(k, l) - L X_k + a(k+1, l+1)) \bmod M$.

*Proof.* The first identity holds for the plain sums, since the new window loses $X_k$ and gains $X_{l+1}$, and reduction mod $M$ commutes with addition. For the second, work with the plain sums $A' = \sum_{i=k+1}^{l+1} X_i$ and $B = \sum_{i=k}^{l} (l - i + 1) X_i$. Then
$$\sum_{i=k+1}^{l+1} (l + 1 - i + 1) X_i = \sum_{i=k+1}^{l} (l - i + 1) X_i + \sum_{i=k+1}^{l+1} X_i = (B - L X_k) + A',$$
because in $B$ the byte $X_k$ has weight $l - k + 1 = L$, each byte $X_i$ with $k < i \le l$ gains weight 1, and $X_{l+1}$ enters with weight 1. Reducing mod $M$ gives the claim. $\square$

So, by induction over the steps, lines L9 and L10 keep $(a, b) = (a(k, k+S-1), b(k, k+S-1))$ for the current $k$, and line L6 sets it from the definition after a jump.

**Lemma 2 (the invariant of DELTA).** At each test of line L3, the instructions emitted so far, followed by the pending literal bytes, rebuild exactly $\mathit{new}[0 .. k-1]$, provided that no two different blocks with equal strong hashes were compared. If $k + S \le n$, then $(a, b)$ is the weak checksum of $\mathit{new}[k .. k+S-1]$.

*Proof.* At the first test, $k = 0$, nothing is emitted, and line L2 computes the weak checksum of the first window. Suppose the invariant holds at a test with $k + S \le n$.

If line L4 finds a block $j$ with the same weak value and the same strong hash, then by the proviso $\mathit{new}[k .. k+S-1]$ equals old block $j$. Line L5 emits the pending literal bytes, which rebuild up to $k - 1$, then COPY $j$, which rebuilds $\mathit{new}[k .. k+S-1]$, and sets $k$ to $k + S$. Line L6 recomputes the weak checksum if a full window is left.

Otherwise, line L8 appends $\mathit{new}[k]$ to the pending bytes, which then rebuild up to $k$. If $k + S < n$, Lemma 1 with $L = S$ shows that lines L9 and L10 give the weak checksum of the window at $k + 1$. Line L11 increments $k$. In both cases the invariant holds at the next test. $\square$

**Theorem 1 (the delta rebuilds the new file).** If no strong hash collision occurs between a window of the new file and a different block of the old file, PATCH applied to the old file and the output of DELTA returns the new file.

*Proof.* Each step of the loop increases $k$ by 1 or by $S \ge 1$, so the loop ends, with $k + S > n$ and $k \le n$. By Lemma 2 the output so far rebuilds $\mathit{new}[0 .. k-1]$. Line L12 adds $\mathit{new}[k .. n-1]$ as literal bytes and emits them. PATCH copies each COPY $j$ as the $S$ bytes of old block $j$, which by the signature are full blocks of the old file, and copies each literal as it is. So it returns $\mathit{new}[0 .. n-1]$. $\square$

**Theorem 2 (the Rabin window).** Let $P$ have degree $d \ge 9$ over GF(2), and let the fingerprint of a byte string $W$ of $w$ bytes be $F(W) = W(x) \bmod P(x)$, where $W(x)$ reads the bytes as the bits of one big-endian integer. If the window holds $W = (o, W_2)$ with first byte $o$, and the byte $y$ enters, then
$$F(W_2, y) = \big(F(W)\, x^8 + y - o\, x^{8w}\big) \bmod P,$$
and the code computes this value with the two tables $\mathit{shift}[t] = t\, x^{d} \bmod P$ and $\mathit{drop}[o] = o\, x^{8w} \bmod P$.

*Proof.* As polynomials, $W(x) = o\, x^{8(w-1)} + W_2(x)$ and $(W_2, y)(x) = W_2(x)\, x^8 + y$. So $(W_2, y)(x) = W(x)\, x^8 + y - o\, x^{8w}$, and reduction mod $P$ is a ring map, so $W(x)$ can be replaced by $F(W)$. In GF(2), subtraction is XOR. The code splits $F = F(W)$, of degree below $d$, into its top 8 coefficients $t$ (degrees $d - 8$ to $d - 1$) and the rest $\ell$, so $F x^8 = \ell\, x^8 + t\, x^{d}$, where $\ell x^8$ has degree below $d$ and needs no reduction, and $t x^d \bmod P = \mathit{shift}[t]$. The byte $y$ has degree below $8 \le d$. So $\ell x^8 \oplus \mathit{shift}[t] \oplus y \oplus \mathit{drop}[o]$ has degree below $d$ and is congruent to the right side, hence equal to it. Before the window is full, the buffer holds zero bytes, $o = 0$ and $\mathit{drop}[0] = 0$, and the leading zero bytes do not change $W(x)$. $\square$

**Lemma 3 (chunk bounds).** CDC returns chunks whose concatenation is the input, every chunk has at most $\mathit{max\_size}$ bytes, and every chunk but the last has at least $\mathit{min\_size}$ bytes.

*Proof.* A chunk is closed at byte $i$ only when its length is at least $\mathit{min\_size}$ and the fingerprint test holds, or when its length reaches $\mathit{max\_size}$, and the next chunk starts at $i + 1$. The last chunk is the rest of the input. So the chunks partition the input in order, and the bounds hold. $\square$

**Cost.** By Lemma 1, a roll takes a fixed number of operations. In DELTA, a step without a weak hit costs $O(1)$, a weak hit costs $O(S)$ for the strong hash, and each COPY costs $O(S)$ for line L6. COPY steps cover disjoint parts of the new file, so they cost $O(n)$ in total, and the at most $n$ other steps cost $O(1)$ each plus $O(S)$ per false weak hit. So the time is $O(n)$ plus $O(S)$ per false weak hit, and $O(nS)$ in the worst case. The table has one entry per full old block. $\blacksquare$
