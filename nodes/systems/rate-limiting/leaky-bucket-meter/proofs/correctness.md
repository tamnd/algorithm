---
title: The leaky bucket meter passes exactly the packets that keep its output inside the (r, b) arrival curve, and it is the mirror image of the token bucket
proves: [correctness]
status: full
---

**Setup.** The bucket has leak rate $r > 0$ and size $b > 0$, and it is empty at the start time $t_0$. The packets arrive at times $t_0 \le t_1 \le \cdots \le t_n$ with sizes $L_1, \ldots, L_n > 0$. For packet $j$ we write $X_j$ for the level after line L1 (before the test of line L3), and $A$ for the set of indices of the packets that pass. For $i \le j$ let $S(i, j) = \sum_{k \in A,\, i \le k < j} L_k$, the size of the passed packets from $i$ up to, but not with, $j$. A family of packets $(t_k, L_k)_{k \in K}$ *conforms to* $(r, b)$ when $\sum_{k \in K,\, i \le k \le j} L_k \le r(t_j - t_i) + b$ for all $i \le j$ in $K$. Each interval of length $\tau$ that holds packets of $K$ has a first packet $i$ and a last packet $j$ with $t_j - t_i \le \tau$, so a conforming family puts at most $r\tau + b$ units in each interval of length $\tau$.

**Lemma 1 (floors compose).** For each real $y$ and each $d \ge 0$, $\max(0, \max(0, y) - d) = \max(0, y - d)$.

*Proof.* If $y \ge 0$ the inner maximum is $y$ and both sides are equal. Else the left side is $\max(0, -d) = 0$, and the right side is $0$ because $y - d < 0$. $\square$

**Lemma 2 (closed form).** For each $j$,

$$X_j = \max\Big(0,\ \max_{i \in A,\, i < j} \big(S(i, j) - r(t_j - t_i)\big)\Big),$$

where a maximum over the empty set is $-\infty$.

*Proof.* By induction on $j$. For $j = 1$ the bucket is empty at $t_0$, so line L1 gives $X_1 = \max(0, 0 - r(t_1 - t_0)) = 0$, and the inner maximum is over the empty set. Assume the claim for $j$, and write $X_j = \max(0, M)$, where $M$ is the inner maximum. Let $Y_j$ be the level after packet $j$: $Y_j = X_j + L_j$ if $j \in A$ (line L4), else $Y_j = X_j$. Line L1 for packet $j + 1$ gives $X_{j+1} = \max(0, Y_j - d)$ with $d = r(t_{j+1} - t_j) \ge 0$.

1. If $j \notin A$, then $X_{j+1} = \max(0, \max(0, M) - d) = \max(0, M - d)$ by Lemma 1. For $i < j$, $S(i, j+1) = S(i, j)$, so subtracting $d$ turns each term $S(i, j) - r(t_j - t_i)$ of $M$ into $S(i, j+1) - r(t_{j+1} - t_i)$. This is the claim for $j + 1$.
2. If $j \in A$, then $X_{j+1} = \max(0, \max(0, M) + L_j - d) = \max(0,\ L_j - d,\ M + L_j - d)$, because adding $L_j - d$ commutes with the maximum. The term $L_j - d$ is $S(j, j+1) - r(t_{j+1} - t_j)$, the new term for $i = j$. For $i < j$ in $A$, $S(i, j+1) = S(i, j) + L_j$, so $M + L_j - d$ is the maximum of the terms $S(i, j+1) - r(t_{j+1} - t_i)$. This is the claim for $j + 1$. $\square$

The rejected packets do not appear in the formula: a rejected packet leaves no trace in the bucket.

**Theorem 1 (the output conforms).** The passed packets conform to $(r, b)$.

*Proof.* Let $i \le j$ be in $A$. Line L3 passed $j$, so $X_j + L_j \le b$. If $i = j$ this says $L_j \le b$, since $X_j \ge 0$. If $i < j$, Lemma 2 gives $X_j \ge S(i, j) - r(t_j - t_i)$, so $S(i, j) + L_j \le b + r(t_j - t_i)$. The left side is the size of the passed packets from $i$ to $j$. $\square$

**Theorem 2 (greedy).** Packet $j$ passes if and only if the passed packets before $j$, together with packet $j$, conform to $(r, b)$.

*Proof.* By Theorem 1 the passed packets before $j$ conform among themselves, so the extended family conforms exactly when the pairs that end at $j$ satisfy the bound: $L_j \le b$, and $S(i, j) + L_j \le b + r(t_j - t_i)$ for each $i \in A$ with $i < j$. By Lemma 2, $X_j + L_j \le b$ holds exactly when $0 + L_j \le b$ and each term of the inner maximum plus $L_j$ is at most $b$. These are the same inequalities, and line L3 passes $j$ exactly when $X_j + L_j \le b$. $\square$

**Corollary 1 (tightness).** If the whole input conforms to $(r, b)$, every packet passes.

*Proof.* By induction on $j$. If packets $1, \ldots, j-1$ passed, the family of Theorem 2 is the prefix $1, \ldots, j$. Its pairs are pairs of the whole input, so it conforms, and packet $j$ passes. $\square$

**Theorem 3 (mirror of the token bucket).** Run a token bucket with rate $r$ and depth $b$, full at $t_0$, on the same packets, and let $x_j$ be its tokens after its refill line. Then $X_j = b - x_j$ for each $j$, the two make the same decision on each packet, and the level after each packet is $b$ minus the tokens after it.

*Proof.* By induction on $j$. At $j = 1$, $X_1 = 0$ and $x_1 = \min(b, b + r(t_1 - t_0)) = b$. Assume $X_j = b - x_j$. The meter passes $j$ when $X_j + L_j \le b$, that is when $x_j \ge L_j$, which is the token bucket test, so the decisions agree. The values after packet $j$ are $Y_j = X_j + L_j$ and $y_j = x_j - L_j$ on a pass, and $Y_j = X_j$, $y_j = x_j$ on a reject, so $Y_j = b - y_j$ in both cases. Then $X_{j+1} = \max(0, Y_j - d) = \max(0, b - y_j - d) = b - \min(b, y_j + d) = b - x_{j+1}$, with $d = r(t_{j+1} - t_j)$. $\blacksquare$

So the meter and the token bucket are one algorithm with two names for the state: the meter counts the fluid that is in the bucket, and the token bucket counts the room that is left.
