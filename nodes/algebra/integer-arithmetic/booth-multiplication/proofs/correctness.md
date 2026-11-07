---
title: Booth's recoding and the sequential algorithm compute the signed product
proves: [correctness, termination]
status: full
---

Let $y$ be an $n$-bit two's complement integer with bits $y_{n-1}, \ldots, y_0$ and $y_{-1} = 0$, so $y = -y_{n-1}2^{n-1} + \sum_{i=0}^{n-2} y_i 2^i$. Let $D_i = y_{i-1} - y_i \in \{-1, 0, 1\}$.

**Termination.** BOOTH runs exactly $n$ steps and BOOTH-4 exactly $\lceil n/2 \rceil$ digits.

**Lemma 1 (radix-2 recoding).** $\sum_{i=0}^{n-1} D_i 2^i = y$.

*Proof.* $\sum_{i=0}^{n-1} y_{i-1} 2^i = \sum_{i=0}^{n-2} y_i 2^{i+1}$, so the sum is $\sum_{i=0}^{n-2} y_i (2^{i+1} - 2^i) - y_{n-1}2^{n-1} = \sum_{i=0}^{n-2} y_i 2^i - y_{n-1} 2^{n-1} = y$. $\square$

**Lemma 2 (radix-4 recoding).** For even $n$ and $q_j = y_{2j-1} + y_{2j} - 2y_{2j+1}$, $\sum_{j=0}^{n/2-1} q_j 4^j = y$, and $q_j \in \{-2, \ldots, 2\}$.

*Proof.* $q_j 4^j = D_{2j} 2^{2j} + D_{2j+1} 2^{2j+1}$, since $D_{2j} + 2D_{2j+1} = y_{2j-1} - y_{2j} + 2y_{2j} - 2y_{2j+1} = q_j$. Summing over $j$ gives Lemma 1. The bound is clear from $y_{2j-1} + y_{2j} \in [0, 2]$. For odd $n$, sign extension by one bit keeps the value of $y$, and the claim applies to $n + 1$ bits. $\square$

So line L8 returns $\sum_j q_j x 4^j = xy$, which proves BOOTH-4.

**The sequential algorithm.** Read the $2n + 1$ bits of $(A, Q, q_{-1})$ with $A$ in two's complement of $n + 1$ bits. Write $\operatorname{val}(A)$ for the signed value of $A$. Before step $k + 1$ ($0 \le k \le n$), let $Q$ hold the bits $y_{n-1}, \ldots, y_k$ in its low $n - k$ positions and the $k$ low bits of a partial product in its top $k$ positions, and $q_{-1} = y_{k-1}$. We prove the invariant

$$P_k := \operatorname{val}(A) \cdot 2^k + (\text{top } k \text{ bits of } Q) = x \sum_{i=0}^{k-1} D_i 2^i ,$$

and $A$ never overflows.

*Base.* For $k = 0$, $A = 0$, $Q = y$, $q_{-1} = 0 = y_{-1}$, and both sides are 0.

*Step.* At step $k + 1$, $q_0 = y_k$ and $q_{-1} = y_{k-1}$, so lines L3 and L4 add $D_k x$ to $A$. By the invariant, $|P_k| \le |x| (2^k - 1)$, and the top $k$ bits of $Q$ form a number $T \in [0, 2^k)$, so $\operatorname{val}(A) = (P_k - T)/2^k$ satisfies $-|x| - 1 < \operatorname{val}(A) < |x|$, that is $-2^{n-1} \le \operatorname{val}(A) \le 2^{n-1} - 1$ since $|x| \le 2^{n-1}$. With $|D_k x| \le 2^{n-1}$, $-2^n \le \operatorname{val}(A) + D_k x \le 2^n - 1$, which is the range of $n + 1$ bits; so no overflow occurs. Line L5 is an arithmetic shift of $A$ by one bit with the low bit of $A$ moved into the top of $Q$; with $A' = \lfloor (\operatorname{val}(A) + D_k x)/2 \rfloor$ and $b$ the bit moved, $\operatorname{val}(A) + D_k x = 2A' + b$. Then

$$P_{k+1} = A' 2^{k+1} + b\, 2^k + (\text{top } k \text{ bits}) = (\operatorname{val}(A) + D_k x) 2^k + (\text{top } k \text{ bits}) = P_k + D_k x 2^k ,$$

which is the invariant for $k + 1$. Line L5 also moves $y_k$ into $q_{-1}$ and exposes $y_{k+1}$ in $q_0$.

*End.* After $n$ steps, $P_n = \operatorname{val}(A) 2^n + Q = x \sum_{i<n} D_i 2^i = xy$ by Lemma 1. Since $|xy| \le 2^{2n-2} < 2^{2n-1}$, the low $2n$ bits of $(A, Q)$, read in two's complement, are $xy$, which line L6 returns. $\blacksquare$
