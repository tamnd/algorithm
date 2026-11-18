---
title: Frame of reference encoding decodes every value back, and its range selection with block skipping returns exactly the matching positions
proves: [correctness]
status: full
---

We use the notation of the page. The column is a list of integers $a_0, \ldots, a_{N-1}$, cut into blocks of $B$ consecutive values; block $k$ holds the positions $kB$ to $\min(N, kB + B) - 1$ (line L1). Its header has $\mathrm{base}_k = \min$ and $\mathrm{max}_k = \max$ of its values (line L2), and $w_k$, the number of bits of $\mathrm{max}_k - \mathrm{base}_k$ (line L3), which is 0 when all values are equal.

**Lemma 1 (offsets fit).** For every position $i$ in block $k$, the offset $o_i = a_i - \mathrm{base}_k$ satisfies $0 \le o_i \le \mathrm{max}_k - \mathrm{base}_k < 2^{w_k}$.

*Proof.* The base is the minimum and $\mathrm{max}_k$ the maximum of the block, so $\mathrm{base}_k \le a_i \le \mathrm{max}_k$. A non-negative integer with $w$ bits is less than $2^w$, and 0 has 0 bits, so the bound holds with $w_k = 0$ as well. $\square$

**Lemma 2 (round trip).** GET$(i)$ returns $a_i$.

*Proof.* Line L4 writes the $w_k$ bits of $o_i$ at the bit positions $(i - kB) w_k$ to $(i - kB) w_k + w_k - 1$ of the bit array of block $k$. These ranges are disjoint for different positions of the block, and the array starts with all bits 0, so each field holds exactly the bits of its offset, which fit by Lemma 1. Line L5 finds the block $k = \lfloor i / B \rfloor$ and reads the same field, so it returns $o_i$, and line L6 returns $\mathrm{base}_k + o_i = a_i$. $\square$

GET reads one header and $w_k$ bits, so its cost does not depend on $N$ or on the other values of the block. Block $k$ uses $\lceil c_k w_k / 8 \rceil$ bytes for its offsets, where $c_k$ is its number of values.

**Theorem 1 (selection).** For bounds $lo \le hi$, each an integer or open, SELECT$(lo, hi)$ returns, in increasing order, exactly the positions $i$ with $lo \le a_i \le hi$.

*Proof.* Take one block $k$; the blocks are visited in order at line L7 and the positions inside a block in order, so the output is sorted if each block contributes exactly its matching positions. Every value of the block lies in $[\mathrm{base}_k, \mathrm{max}_k]$. There are three cases.

If $\mathrm{max}_k < lo$ or $\mathrm{base}_k > hi$ (line L8), every value of the block is below $lo$ or above $hi$, so no position matches, and skipping the block is correct.

Else, if $lo \le \mathrm{base}_k$ and $\mathrm{max}_k \le hi$ (line L9), every value is in $[lo, hi]$, so every position matches, and line L9 outputs them all without reading an offset.

Else, line L10 sets $s = \max(lo - \mathrm{base}_k, 0)$ and $e = hi - \mathrm{base}_k$, with $s = 0$ for an open $lo$ and $e = \mathrm{max}_k - \mathrm{base}_k$ for an open $hi$. Since $o_i \ge 0$ and $a_i = \mathrm{base}_k + o_i$,

$$lo \le a_i \le hi \iff lo - \mathrm{base}_k \le o_i \le hi - \mathrm{base}_k \iff s \le o_i \le e,$$

where the last step uses $o_i \ge 0$ for the lower bound and $o_i \le \mathrm{max}_k - \mathrm{base}_k$ for an open upper bound. By Lemma 2 line L11 reads $o_i$ correctly, so it outputs exactly the matching positions of the block. $\square$

A comparison with a constant is a range: $= v$ is $[v, v]$, $< v$ is $(-\infty, v - 1]$, $\le v$ is $(-\infty, v]$, $> v$ is $[v + 1, \infty)$ and $\ge v$ is $[v, \infty)$, since the values are integers. If $lo > hi$, every block falls in the first or the third case and no position is output, which is also correct.

**Theorem 2 (cost).** SELECT reads every header once and reads offsets only in the blocks of the third case, that is, the blocks whose range $[\mathrm{base}_k, \mathrm{max}_k]$ meets $[lo, hi]$ without lying inside it. If the column is sorted, at most two blocks are in the third case, so SELECT reads at most $2B$ offsets.

*Proof.* The first claim is the case analysis above. In a sorted column, $\mathrm{base}_k$ and $\mathrm{max}_k$ do not decrease with $k$, and $\mathrm{max}_k \le \mathrm{base}_{k+1}$. A block meets $[lo, hi]$ if and only if $\mathrm{max}_k \ge lo$ and $\mathrm{base}_k \le hi$. The blocks with $\mathrm{max}_k \ge lo$ are a suffix of the blocks and those with $\mathrm{base}_k \le hi$ are a prefix, so the blocks that meet $[lo, hi]$ form a run of consecutive blocks. Let $k$ be in the run but be neither its first nor its last block. Then $k - 1$ and $k + 1$ are in the run, so $\mathrm{base}_k \ge \mathrm{max}_{k-1} \ge lo$ and $\mathrm{max}_k \le \mathrm{base}_{k+1} \le hi$, and block $k$ lies inside $[lo, hi]$. So only the first and the last block of the run can be in the third case. $\square$
