---
title: The Chang-Lawler SET algorithm reports exactly the approximate matches
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, $k \ge 0$, and $\mathrm{ed}$ is the Levenshtein distance with unit costs. A **match** is a substring $A = T[h \ldots j)$ with $\mathrm{ed}(P, A) \le k$, and the claim is that CHANG-LAWLER-SET returns the sorted set of the end positions $j$ of all matches. We use the correctness of [Sellers' algorithm](/sellers-algorithm/): SELLERS($P$, $X$, $k$) returns the end positions of the matches in a string $X$.

## Alignments

An **alignment** of $P$ and $A$ is a set of pairs $(i, u)$, with $i$ a position of $P$ and $u$ a position of $A$, in which no position occurs twice and $i < i'$ if and only if $u < u'$ for any two pairs $(i, u)$ and $(i', u')$. Its cost is the number of unpaired positions of $P$ and of $A$ plus the number of pairs $(i, u)$ with $P[i] \ne A[u]$. The least cost of an alignment is $\mathrm{ed}(P, A)$: an edit script gives an alignment of no larger cost by pairing each surviving symbol with its final position, and an alignment gives a script with one operation per unit of cost. The [proof of the edit distance hardness theorem](/edit-distance-hardness/) gives this argument in full (its Lemma 1).

The following fact follows from the order condition. If $(i, u)$ and $(i', u')$ are pairs with $u < u'$, then every position of $P$ strictly between $i$ and $i'$ is unpaired or paired with a position of $A$ strictly between $u$ and $u'$.

## Lemma 1: few whole pieces

If $\mathrm{ed}(P, A) \le k$, then there are no $k + 1$ pairwise disjoint nonempty intervals $Q_0, \ldots, Q_k$ of positions of $A$ such that no $A[Q_r]$ is a substring of $P$.

*Proof.* Suppose that such intervals exist. Fix an alignment of $P$ and $A$ of cost $\mathrm{ed}(P, A) \le k$. We give, for each $r$, a unit of cost that belongs to $Q_r$, such that the $k + 1$ units are distinct. This shows a cost of at least $k + 1$, a contradiction.

Let $Q_r = [x, y)$. Suppose first that every $u \in Q_r$ is paired, with partner $\pi(u)$ and $P[\pi(u)] = A[u]$, and that $\pi(u + 1) = \pi(u) + 1$ for $x \le u < y - 1$. Then $A[x \ldots y) = P[\pi(x) \ldots \pi(x) + y - x)$, a substring of $P$, which is false. So one of the following holds, and we choose the unit as stated.

- Some $u \in Q_r$ is unpaired, or paired with an unequal symbol. The unit is the unpaired symbol $A[u]$, or the unequal pair of $u$.
- All $u \in Q_r$ are paired with equal symbols, and $\pi(u + 1) \ne \pi(u) + 1$ for some $u$ with $x \le u < y - 1$. By the order condition, $\pi(u + 1) > \pi(u)$, so $\pi(u + 1) \ge \pi(u) + 2$, and the position $i = \pi(u) + 1$ of $P$ lies strictly between the partners of $u$ and $u + 1$. A partner of $i$ would lie strictly between $u$ and $u + 1$, so $i$ is unpaired. The unit is the unpaired symbol $P[i]$.

Units of the first kind involve a position of $A$ in $Q_r$, so units of the first kind for different $r$ are distinct, because the intervals are disjoint. A unit of the first kind is a symbol of $A$ or a pair, and a unit of the second kind is a symbol of $P$, so they are distinct. Two units of the second kind, for $r \ne s$, come from consecutive positions $u, u + 1 \in Q_r$ and $v, v + 1 \in Q_s$ with $u \ne v$. Say $u < v$; then $u + 1 \le v$, so $\pi(u + 1) \le \pi(v)$, and the unit of $Q_r$ is below $\pi(u + 1)$ while the unit of $Q_s$ is above $\pi(v)$. So all $k + 1$ units are distinct. $\square$

## Lemma 2: the pieces of a dead block

If line L5 calls block $t$ dead, then the intervals $[p_r, p_{r+1})$ for $r = 0, \ldots, k$ are disjoint, lie inside the block $[tb, (t+1)b)$, and $T[p_r \ldots p_{r+1})$ is not a substring of $P$ for each $r$.

*Proof.* A dead block is one where line L4 makes all $k + 1$ jumps, with $p_r < (t+1)b$ before each jump, and ends with $p_{k+1} \le (t+1)b$. The jumps increase $p$ by at least 1, so $tb = p_0 < p_1 < \cdots < p_{k+1} \le (t+1)b$, and the intervals are disjoint, nonempty and inside the block. For each $r$, $p_r + ms(p_r) = p_{r+1} - 1 < (t+1)b \le n$, so the symbol $T[p_r + ms(p_r)]$ exists, and by the maximality of $ms(p_r)$ the string $T[p_r \ldots p_r + ms(p_r)] = T[p_r \ldots p_{r+1})$ is not a substring of $P$. $\square$

## Lemma 3: every match covers a live block

Let $m - k \ge 2$ and $b = \lfloor (m - k)/2 \rfloor$. Every match $A = T[h \ldots j)$ contains a block $[tb, (t+1)b)$ with $0 \le t < \lfloor n/b \rfloor$, and every block that $A$ contains is live.

*Proof.* Each operation changes the length by at most 1, so $|A| \ge m - k \ge 2b$. Let $t = \lceil h / b \rceil$. Then $h \le tb < h + b$, so $(t+1)b < h + 2b \le j \le n$. So $A$ contains the block $[tb, (t+1)b)$, and $(t+1)b \le n$ gives $t < \lfloor n / b \rfloor$. If a block contained in $A$ were dead, Lemma 2 would give $k + 1$ disjoint substrings of $A$ that are not substrings of $P$, against Lemma 1 applied to $A$ with its positions shifted by $h$. $\square$

## The theorem

*Line L1.* If $m - k < 2$, the algorithm returns SELLERS($P$, $T$, $k$), which is correct.

*Soundness.* Let $m - k \ge 2$. Each window $[lo, hi)$ of line L8 satisfies $0 \le lo \le hi \le n$, and an end position $j'$ reported by SELLERS($P$, $T[lo \ldots hi)$, $k$) is the end of a match $T[lo + h' \ldots lo + j')$ of $T$. So every returned value $lo + j'$ is the end of a match.

*Completeness.* Let $A = T[h \ldots j)$ be a match. By Lemma 3 it contains a live block $t$. Since $|A| \le m + k$, $h \ge j - m - k \ge (t+1)b - m - k$ and $j \le h + m + k \le tb + m + k$, and $0 \le h \le j \le n$. So $A$ lies inside the window $W = [\max(0, (t+1)b - m - k), \min(n, tb + m + k))$ of line L6. The left and right ends of these windows do not decrease as $t$ grows, so line L7 merges each window into an interval that contains it, and the final windows contain every window of a live block. Let $[lo, hi)$ be the final window that contains $W$. Then $T[h \ldots j)$ is the substring $[h - lo, j - lo)$ of $T[lo \ldots hi)$, so SELLERS reports $j - lo$, and the algorithm returns $j$.

Line L9 sorts the end positions and removes repeats, so the output is the sorted set of the ends of all matches. $\blacksquare$
