---
title: Bogosort is correct when it stops, and it stops with probability 1
proves: [correctness, termination]
status: full
---

**Lemma 1 (IS-SORTED).** IS-SORTED$(A)$ returns true if and only if $A[i-1] \le A[i]$ for each $i$ with $1 \le i \le n-1$, which is the case exactly when $A$ is in non-decreasing order.

*Proof.* The loop of line L3 tests the pairs $(i-1, i)$ for $i = 1, 2, \ldots$ in order. If some pair has $A[i-1] > A[i]$, line L4 returns false at the first such pair. If no pair has it, the loop ends and line L5 returns true. A sequence is non-decreasing exactly when each pair of neighbours is in order, because $\le$ is transitive. $\square$

**Lemma 2 (SHUFFLE).** After SHUFFLE$(A)$, $A$ holds the same multiset of items, and if the random integers of line L7 are uniform and independent, each of the $n!$ arrangements of the positions has probability $1/n!$.

*Proof.* Each step of line L8 is an exchange, so the multiset does not change. For the distribution, the loop makes $n - 1$ choices, the choice for $i$ among $i + 1$ values, so there are $n \cdot (n-1) \cdots 2 = n!$ equally likely sequences of choices. Each sequence gives a different arrangement: the choice for $i = n-1$ fixes which item ends at position $n-1$, which is never touched again, and by induction the later choices fix the remaining positions. So the $n!$ sequences give the $n!$ arrangements, one each. This is the proof of CLRS, Section 5.3. $\square$

**Theorem.** (a) If BOGOSORT$(A)$ returns, $A$ holds the input items in non-decreasing order. (b) BOGOSORT returns with probability 1, and on $n$ distinct keys that are not sorted, the number $N$ of shuffles satisfies $\Pr[N > k] = (1 - 1/n!)^k$ and $\mathbb{E}[N] = n!$.

*Proof.* (a) The loop of line L1 exits only when IS-SORTED$(A)$ returns true, so by Lemma 1 the array is in non-decreasing order at that time. By Lemma 2 and because IS-SORTED does not change $A$, it holds the input multiset.

(b) Let the input have the key values with multiplicities $m_1, \ldots, m_r$. Of the $n!$ arrangements of the positions, exactly $m_1! \cdots m_r!$ give a non-decreasing array, so by Lemma 2 each shuffle gives a sorted array with probability $p = m_1! \cdots m_r! / n! \ge 1/n!$. The shuffles use fresh random integers, so the events "shuffle $t$ gives a sorted array" are independent, each with probability $p$. If the input is not sorted, the run makes more than $k$ shuffles exactly when the first $k$ shuffles all give unsorted arrays, so $\Pr[N > k] = (1 - p)^k$. This tends to 0 as $k$ grows, so $\Pr[N = \infty] = 0$, and the run stops with probability 1. Then
$$\mathbb{E}[N] = \sum_{k \ge 0} \Pr[N > k] = \sum_{k \ge 0} (1-p)^k = \frac{1}{p}.$$
For distinct keys, $p = 1/n!$ and $\mathbb{E}[N] = n!$. If the input is sorted, $N = 0$. $\blacksquare$
