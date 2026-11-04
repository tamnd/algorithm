---
title: The RRR bit vector is correct and its offsets fit in lg C(n, m) + n/b + 1 bits
proves: [correctness, space]
status: full
---

Write $C(j, c) = \binom{j}{c}$, with $C(j, c) = 0$ for $c > j$. A block is a word $x$ of $b$ bits; its class is $c = $ the number of 1s of $x$, and if its 1s are at $p_1 < \cdots < p_c$, its offset is $o(x) = \sum_{i=1}^{c} C(p_i, i)$. Lines L1 to L4 compute exactly this sum: when the loop meets the $i$-th 1, at $j = p_i$, the counter $c$ has just become $i$.

**Lemma 1 (range).** For a block of class $c$, $0 \le o(x) < C(b, c)$. More precisely, if all 1s are below position $h$, then $o(x) < C(h, c)$.

*Proof.* By induction on $c$. For $c = 0$, $o = 0 < 1 = C(h, 0)$. For $c \ge 1$, $p_c \le h - 1$, and the first $c - 1$ ones lie below $p_c$, so by induction their sum is less than $C(p_c, c-1)$, that is at most $C(p_c, c-1) - 1$. Then $o(x) \le C(p_c, c-1) - 1 + C(p_c, c) = C(p_c + 1, c) - 1 \le C(h, c) - 1$ by Pascal's rule and the monotonicity of $C(\cdot, c)$. $\square$

**Lemma 2 (decode).** For each block $x$ of class $c$, DECODE$(c, o(x)) = x$.

*Proof.* DECODE scans $j$ from $b - 1$ down. Let the invariant be: before step $j$, the bits above $j$ of the output are those of $x$, the remaining counter $c'$ is the number of 1s of $x$ at positions $\le j$, and the remaining value $o'$ is $\sum_{i=1}^{c'} C(p_i, i)$ for those 1s. It holds at $j = b - 1$. At step $j$, if $x$ has a 1 at $j$, then $j = p_{c'}$ and $o' \ge C(j, c')$, so line L7 sets the bit and lines L8 restore the invariant. If $x$ has no 1 at $j$, then all of the $c'$ ones are below $j$, and Lemma 1 with $h = j$ gives $o' < C(j, c')$, or $c' = 0$; so line L7 does not set the bit. After $j = 0$ the output equals $x$. $\square$

By Lemmas 1 and 2, ENCODE maps the $C(b, c)$ blocks of class $c$ injectively into $\{0, \ldots, C(b,c) - 1\}$, so it is a bijection, and each offset fits in $L[c] = \lceil \lg C(b, c) \rceil$ bits.

**The pointers.** BUILD appends the offsets of blocks $0, 1, \ldots$ to the stream in order, with lengths $L[K[t]]$. So the offset of block $t$ starts at $\sum_{t' < t} L[K[t']]$, which is $P[q] + PB[t]$ by the definitions of the samples, with $q = \lfloor t/k \rfloor$. In the same way $R[q] + RB[t] = \sum_{t' < t} K[t'] = \text{rank}_1(t b)$. Hence line L14 (and L11, L18) rebuilds block $t$ exactly, by Lemma 2.

**Access and rank.** Position $i$ is bit $i \bmod b$ of block $t = \lfloor i/b \rfloor$, so line L11 is correct. For rank, $\text{rank}_1(i) = \text{rank}_1(t b) + $ the number of 1s of block $t$ at positions below $i \bmod b$. If $i \bmod b = 0$ the second term is 0, which is line L13; otherwise it is the POPCOUNT of line L15.

**Select.** Let $j \le m$. The number of 1s before superblock $q$, $R[q]$, is nondecreasing in $q$ and $R[0] = 0 < j$, so the last $q$ with $R[q] < j$ exists, and the $j$-th 1 is not in a later superblock, because those start with at least $j$ ones before them. In the same way, the binary search of line L17 finds the block $t$ of superblock $q$ that holds the $j$-th 1: the last block with $\text{rank}_1(tb) < j$. The $j$-th 1 of $B$ is then the $(j - \text{rank}_1(tb))$-th 1 of block $t$, which line L19 returns. For $\text{select}_0$ the same argument holds with the counts of 0s, $t b - \text{rank}_1(t b)$; the bits of the last block word above $b'$ are not part of $B$ and lie after the last real 0, so they are never reached when $j \le n - m$.

**Space of the offsets.** Let $b_t$ be the length of block $t$: $b$ for each block but the last, and $b' = n - (\lceil n/b \rceil - 1) b$ for the last. Let $c_t$ be the class of block $t$, and let $L_t = \lceil \lg C(b_t, c_t) \rceil$ be the length of its offset, which suffices by Lemma 1 with $h = b_t$. Cutting a vector into its blocks is a bijection between the bit vectors of length $n$ and the tuples of blocks of lengths $(b_t)$. It maps the vectors whose blocks have the classes $(c_t)$ onto the tuples whose block $t$ has class $c_t$, and there are $\prod_t C(b_t, c_t)$ of these. Each such vector has $\sum_t c_t = m$ ones, so it is one of the $C(n, m)$ vectors with $m$ ones, and $\prod_t C(b_t, c_t) \le C(n, m)$. Hence

$$\sum_t L_t \le \sum_t \left(\lg C(b_t, c_t) + 1\right) \le \lg C(n, m) + \lceil n / b \rceil \le \lg C(n, m) + \frac{n}{b} + 1.$$

$\blacksquare$
