---
title: The token bucket passes exactly the packets that keep its output inside the (r, b) arrival curve
proves: [correctness]
status: full
---

**Setup.** The bucket has rate $r > 0$ and depth $b > 0$, and it is full at the start time $t_0$. The packets arrive at times $t_0 \le t_1 \le t_2 \le \cdots \le t_n$ with sizes $L_1, \ldots, L_n > 0$. For packet $j$ we write $x_j$ for the tokens after line L1 (before the test of line L3), and $A$ for the set of indices of the packets that pass. For $i \le j$ we write $S(i, j) = \sum_{k \in A,\, i \le k < j} L_k$, the size of the passed packets from $i$ up to, but not with, $j$. A sequence of packets $(t_k, L_k)_{k \in K}$ *conforms to* $(r, b)$ when $\sum_{k \in K,\, i \le k \le j} L_k \le r (t_j - t_i) + b$ for all $i \le j$ in $K$.

**Remark (closed intervals suffice).** Let $I$ be any interval of the time line, open, closed or half-open, of length $\tau$. If $I$ holds packets of $K$, let $i$ be the first and $j$ the last of them. Then $t_j - t_i \le \tau$, so a conforming $K$ puts at most $r (t_j - t_i) + b \le r \tau + b$ units in $I$. So the pairwise test is the same as the statement "at most $r\tau + b$ units in each interval of length $\tau$".

**Lemma 1 (caps compose).** For each real $y$ and each $d \ge 0$, $\min(b, \min(b, y) + d) = \min(b, y + d)$.

*Proof.* If $y \le b$, the inner minimum is $y$ and both sides are equal. Else the inner minimum is $b$, the left side is $\min(b, b + d) = b$, and the right side is $b$ because $y + d > b$. $\square$

**Lemma 2 (closed form).** For each $j$,

$$x_j = \min\Big(b,\ \min_{i \in A,\, i < j} \big(b + r (t_j - t_i) - S(i, j)\big)\Big).$$

*Proof.* By induction on $j$. For $j = 1$ the bucket is full at $t_0$ and line L1 gives $x_1 = \min(b, b + r(t_1 - t_0)) = b$, and the inner minimum is over an empty set. Assume the claim for $j$. Let $y_j$ be the tokens after packet $j$: $y_j = x_j - L_j$ if $j \in A$ (line L4), else $y_j = x_j$. Line L1 for packet $j + 1$ gives $x_{j+1} = \min(b, y_j + r (t_{j+1} - t_j))$, with $y_j \le b$.

Write $d = r (t_{j+1} - t_j) \ge 0$, and let $M$ be the inner minimum of the claim for $x_j$ (it is $+\infty$ when it is over an empty set), so that $x_j = \min(b, M)$.

1. If $j \notin A$, then $x_{j+1} = \min(b, \min(b, M) + d) = \min(b, M + d)$ by Lemma 1. Here $S(i, j+1) = S(i, j)$ for each $i < j$, so adding $d$ turns each term $b + r(t_j - t_i) - S(i, j)$ of $M$ into $b + r(t_{j+1} - t_i) - S(i, j+1)$. This is the claim for $j + 1$.
2. If $j \in A$, then $x_{j+1} = \min(b, \min(b, M) - L_j + d) = \min(b,\ b - L_j + d,\ M - L_j + d)$. Here $S(i, j+1) = S(i, j) + L_j$ for each $i < j$ in $A$, and $S(j, j+1) = L_j$. So $b - L_j + d = b + r(t_{j+1} - t_j) - S(j, j+1)$ is the new term for $i = j$, and $M - L_j + d$ is the minimum of the terms $b + r(t_{j+1} - t_i) - S(i, j+1)$ for $i < j$. This is the claim for $j + 1$. $\square$

The rejected packets do not appear in the formula. So the tokens depend only on the passed packets: a rejected packet leaves no trace.

**Theorem 1 (the output conforms).** The passed packets conform to $(r, b)$.

*Proof.* Let $i \le j$ be in $A$. If $i = j$, line L3 passed $j$ with $L_j \le x_j \le b$. If $i < j$, Lemma 2 gives $x_j \le b + r(t_j - t_i) - S(i, j)$, because a minimum is at most each of its terms. Line L3 passed $j$, so $L_j \le x_j$. Together, $S(i, j) + L_j \le b + r(t_j - t_i)$, and the left side is the size of the passed packets from $i$ to $j$. $\square$

**Theorem 2 (greedy).** Packet $j$ passes if and only if the passed packets before $j$, together with packet $j$, conform to $(r, b)$.

*Proof.* By Theorem 1, the passed packets before $j$ conform among themselves. So the extended set conforms exactly when the new pairs, the ones that end at $j$, satisfy the bound: $L_j \le b$, and $S(i, j) + L_j \le b + r(t_j - t_i)$ for each $i \in A$ with $i < j$. By Lemma 2, $x_j \ge L_j$ holds exactly when each term of the minimum is at least $L_j$, and these are the same inequalities. Line L3 passes $j$ exactly when $x_j \ge L_j$. $\square$

**Corollary (tightness).** If the whole input conforms to $(r, b)$, the bucket passes every packet.

*Proof.* By induction on $j$. Assume that packets $1, \ldots, j-1$ passed. Then the passed packets before $j$ with packet $j$ are the prefix $1, \ldots, j$, and a prefix of a conforming sequence conforms, because its pairs are pairs of the whole sequence. By Theorem 2, packet $j$ passes. $\blacksquare$

So the token bucket is the tightest filter for the arrival curve $r t + b$: no packet that it passes breaks the curve, and no packet of a conforming input is lost.
