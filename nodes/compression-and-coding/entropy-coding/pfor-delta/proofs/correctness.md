---
title: The PFOR decoder returns the coded block, and PForDelta returns the list
proves: [correctness]
status: full
---

Fix a block $v_0, \ldots, v_{m-1}$ with $0 \le v_i < 2^{32}$, let $\text{base} = \min_i v_i$ and $d_i = v_i - \text{base}$, and fix a width $0 \le b \le 32$. Let $E = (E_0 < E_1 < \cdots < E_{k-1})$ be the list after lines L3 and L4.

**Lemma 1 (the exception list).** (a) Every $i$ with $d_i \ge 2^b$ is in $E$. (b) $E_{j+1} - E_j \le 2^b$ for $0 \le j < k - 1$.

*Proof.* (a) Line L3 puts each such $i$ in $E$, and line L4 only adds positions. (b) Line L4 runs while some pair of neighbors is more than $2^b$ apart, and each insertion of $p + 2^b$ between $p$ and $q$ splits a step of length $q - p > 2^b$ into one of length exactly $2^b$ and one of length $q - p - 2^b \ge 1$. The sum of the excesses $\max(0, (q - p) - 2^b)$ over all steps drops by at least 1 at each insertion, so the loop stops, and when it stops no step is longer than $2^b$. $\square$

**Lemma 2 (the slots fit).** Every value that lines L5 and L6 put in a slot is in $[0, 2^b - 1]$.

*Proof.* For $i \notin E$, $d_i < 2^b$ by Lemma 1(a). For $j < k - 1$, $0 \le E_{j+1} - E_j - 1 \le 2^b - 1$ by Lemma 1(b). The last exception gets 0. $\square$

So line L7 writes each slot in $b$ bits without loss, and line L8 reads back $\text{code}[i]$ exactly as lines L5 and L6 set it.

**Lemma 3 (the patch loop).** At the start of round $j$ of line L10, $cur = E_j$, and $out[i] = v_i$ for every $i$ not in $\{E_j, \ldots, E_{k-1}\}$.

*Proof.* Before round 0, $cur = E_0$ by line L9. After line L8, $out[i] = \text{base} + \text{code}[i] = \text{base} + d_i = v_i$ for each $i \notin E$, by line L5. Suppose the claim holds at round $j$. The round reads $\text{code}[E_j]$, which is $E_{j+1} - E_j - 1$ when $j < k - 1$, so $nxt = E_{j+1}$. It writes $out[E_j] = \text{base} + d_{E_j} = v_{E_j}$, because line L7 wrote the exceptions in the order of $E$ and round $j$ takes exception number $j$. So the claim holds at round $j + 1$. $\square$

**Theorem.** PFOR-DECODE-BLOCK returns $v_0, \ldots, v_{m-1}$ for every width $b$, in particular for the width of line L2. A decoder of the list that decodes the blocks in order and takes prefix sums returns the input list.

*Proof.* By Lemma 3 with $j = k$, after the last round $out[i] = v_i$ for all $i$; when $k = 0$ the loop does not run and Lemma 3 holds with no exceptions. The header gives $m$, $b$, the base, $E_0$ and $k$, and the layout fixes where the slots and the exceptions start, so the decoder of the next block starts at its first byte. For the list, PForDelta coded the gaps $g_1 = x_1$ and $g_i = x_i - x_{i-1}$ in blocks; each block decodes to its gaps, and $x_i = g_1 + \cdots + g_i$. $\blacksquare$
