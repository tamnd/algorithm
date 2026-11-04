---
title: The pairwise network sorts each input
proves: [correctness]
status: full
---

The calls of PAIRWISE-SORT make the same comparators on each input, so they form a network of standard comparators, and the output is a permutation of the input. By the [zero-one principle](/zero-one-principle/) it is enough to show that the output is sorted for each input of zeros and ones.

Fix a call PAIRWISE-SORT$(A, lo, m, r)$ with $L = m / r \ge 2$ items in its subsequence, and let $k = L / 2$ be the number of pairs. Write $a_i$ for the item on the wire $lo + 2ir$ and $b_i$ for the item on the wire $lo + (2i + 1) r$, for $0 \le i < k$. The subsequence of the call is $a_0, b_0, a_1, b_1, \ldots, a_{k-1}, b_{k-1}$. Each comparator of the call has both wires in this subsequence.

**Definition.** For integers $0 \le \beta \le \alpha \le k$, the subsequence is in *pair form* $(\alpha, \beta)$ when $a_i = 0$ if and only if $i < \alpha$, and $b_i = 0$ if and only if $i < \beta$. Its *amplitude* is $\mu = \alpha - \beta$. In pair form the subsequence is $0^{2\beta} (0\,1)^{\mu} 1^{2(k - \alpha)}$. So it is sorted if and only if $\mu \le 1$.

**Lemma 1 (one round).** Let $g \ge 1$ with $g < k$, and let the subsequence be in pair form $(\alpha, \beta)$ with $\mu = \alpha - \beta \le 2g$. Apply the comparators $[b_i : a_{i+g}]$ for $0 \le i \le k - g - 1$ (line L8). Then the subsequence is in pair form with amplitude at most $g$.

*Proof.* The comparators have disjoint wires: the $b_i$ are different and the $a_{i+g}$ are different, and no wire is both a $b$ and an $a$. So each comparator sees the items of the input of the round. The comparator on $b_i$ and $a_{i+g}$ exchanges them if and only if $b_i = 1$ and $a_{i+g} = 0$, that is, if and only if $i \ge \beta$ and $i + g < \alpha$.

If $\mu \le g$, then $i \ge \beta$ gives $i + g \ge \beta + g \ge \alpha$, so no comparator exchanges, and the amplitude stays $\mu \le g$.

If $g < \mu \le 2g$, the exchanges happen exactly for $\beta \le i < \alpha - g$. These values of $i$ satisfy $i \le k - g - 1$, so all of them are in the round. After the round, $b_i = 0$ for $i < \alpha - g$ and $b_i = 1$ for $i \ge \alpha - g$; and $a_j = 0$ for $j < \beta + g$ and $a_j = 1$ for $j \ge \beta + g$, because the items $a_j$ with $\beta + g \le j < \alpha$ became 1. Let $\alpha' = \beta + g$ and $\beta' = \alpha - g$. Then $\beta' \le \alpha'$ because $\mu \le 2g$, and $\alpha' \le \alpha \le k$. So the subsequence is in pair form $(\alpha', \beta')$ with amplitude $\alpha' - \beta' = 2g - \mu < g$. $\square$

**Lemma 2 (steps 1 and 2).** Suppose that the calls of lines L3 and L4 sort their subsequences. Then after line L4 the subsequence is in pair form with amplitude at most $k$.

*Proof.* After line L2, $a_i \le b_i$ for each $i$, so the second items hold at least as many ones as the first items. Line L3 sorts the items $a_0, \ldots, a_{k-1}$, which are the subsequence of stride $2r$ from $lo$, and line L4 sorts $b_0, \ldots, b_{k-1}$, the subsequence of stride $2r$ from $lo + r$. These two calls have disjoint wires and do not change the number of ones of each row. Let $\alpha$ be the number of zeros of the first row and $\beta$ that of the second row. Then $\beta \le \alpha$, and since both rows are sorted, the subsequence is in pair form $(\alpha, \beta)$. Its amplitude is at most $\alpha \le k$. $\square$

**Theorem.** For each $lo$, and for powers of 2 $m$ and $r$, PAIRWISE-SORT$(A, lo, m, r)$ sorts its subsequence for each 0-1 content and changes no other entry of $A$. So by the zero-one principle, PAIRWISE-SORT$(A, 0, n, 1)$ sorts each array of $n = 2^k$ items.

*Proof.* By induction on $L = m / r$. If $L \le 1$, line L1 returns. Let $L \ge 2$. The calls of lines L3 and L4 have $L / 2$ items each, so by the induction hypothesis they sort their subsequences. By Lemma 2, after line L4 the subsequence is in pair form with amplitude $\mu \le k$.

If $k = 1$, then $g = 0$ in line L6, the loop of line L7 does not run, and $\mu \le 1$, so the subsequence is sorted.

If $k \ge 2$, the loop runs with $g = k/2, k/4, \ldots, 1$. Before the round with the value $g$, the amplitude is at most $2g$: for the first round, $\mu \le k = 2g$; for each later round, Lemma 1 applied to the round before, with the value $2g$, gives an amplitude of at most $2g$. Each $g$ satisfies $1 \le g < k$. So by Lemma 1, after the last round, with $g = 1$, the subsequence is in pair form with amplitude at most 1, and it is sorted. Each comparator of the call has both wires in the subsequence, so no other entry changes. $\blacksquare$
