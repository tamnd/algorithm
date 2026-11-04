---
title: Randomized quickselect returns the item of rank k, stops, and makes at most 4n expected comparisons
proves: [correctness, termination, complexity]
status: full
---

Let $A_0$ be the input array, $n = |A_0| \ge 1$ and $0 \le k < n$. Write $\mathrm{sel}(X, j)$ for the item at index $j$ of a sorted copy of the multiset $X$. The goal is $\mathrm{sel}(A_0, k)$. For a range we write $A[a..b)$ for $A[a], \ldots, A[b - 1]$, and $X \le Y$ for two sets of items means $x \le y$ for all $x \in X$ and $y \in Y$.

**Lemma 1 (PARTITION3).** Let $lo < hi$ and let $p$ be an item of $A[lo..hi)$. PARTITION3 permutes $A[lo..hi)$, leaves the rest of $A$ alone, makes exactly $hi - lo$ three-way comparisons, and returns $lt, gt$ with $lo \le lt < gt \le hi$ such that $A[lo..lt) < p$, $A[lt..gt) = p$ and $A[gt..hi) > p$.

*Proof.* Each step of lines L11 to L13 only swaps items of $A[lo..hi)$, so the multiset of the range is kept and the rest of $A$ is not touched. We show that the following holds at line L10: $lo \le lt \le i \le gt \le hi$, $A[lo..lt) < p$, $A[lt..i) = p$ and $A[gt..hi) > p$. At line L9 the three ranges are empty. In line L11, $A[i] < p$. If $lt < i$, the swap moves the item $A[lt] = p$ to index $i$ and the smaller item to index $lt$; if $lt = i$, nothing moves. Then both $lt$ and $i$ grow by one, and the three facts hold. In line L12, $A[i] > p$; after $gt$ drops by one, the swap puts this item at index $gt$, and the item from the old index $gt - 1$ comes to $i$, still unexamined. In line L13, $A[i] = p$, and $i$ grows by one. Each pass compares one item with $p$ once, and $gt - i$ drops by exactly one, so the loop runs $hi - lo$ times and stops with $i = gt$. Then the three ranges cover $A[lo..hi)$. The pivot $p$ is in the range and is equal to itself, so it lies in $A[lt..gt)$, and $lt < gt$. $\square$

**Invariant 2.** At the start of each pass of the loop L2 to L8:

1. $A$ is a permutation of $A_0$;
2. $A[0..lo) \le A[lo..hi) \le A[hi..n)$;
3. $lo \le k < hi$.

*Proof.* After line L1, (1) and (3) hold since $0 \le k < n$, and (2) holds with two empty sets. Assume the invariant at the start of a pass that does not return. By Lemma 1 and (1), $A$ stays a permutation of $A_0$. By (2), each item left of $lo$ is at most each item of $A[lo..hi)$, and PARTITION3 only permutes this range, so the inequalities of (2) still hold for the old $lo$ and $hi$. If line L6 sets $hi \leftarrow lt$, then $A[lt..hi_{\mathrm{old}})$ holds items $\ge p$ and $A[lo..lt)$ holds items $< p$, so $A[lo..lt) \le A[lt..n)$, and (2) holds with the new $hi$. Also $lo \le k < lt$ by the test. If line L7 sets $lo \leftarrow gt$, then $A[lo_{\mathrm{old}}..gt) \le p < A[gt..hi)$, so (2) holds with the new $lo$, and $gt \le k < hi$. $\square$

**Lemma 3.** If (1) and (2) hold and $lo \le j < hi$, then $\mathrm{sel}(A_0, j) = \mathrm{sel}(A[lo..hi), j - lo)$.

*Proof.* By (2), the sorted copy of $A$ is the sorted copy of $A[0..lo)$, then that of $A[lo..hi)$, then that of $A[hi..n)$. Its first part has $lo$ items. By (1) it is also the sorted copy of $A_0$. So index $j$ of it is index $j - lo$ of the sorted copy of $A[lo..hi)$. $\square$

**Theorem 4 (correctness).** If the algorithm returns, it returns $\mathrm{sel}(A_0, k)$.

*Proof.* It returns at line L8 with $lt \le k < gt$, where Invariant 2 held at the start of the pass and Lemma 1 holds for the partition. Since the partition only permuted $A[lo..hi)$, (1) and (2) still hold. The sorted copy of $A[lo..hi)$ is the sorted copy of $A[lo..lt)$, then the $gt - lt$ copies of $p$, then the sorted copy of $A[gt..hi)$. Since $lt - lo \le k - lo < gt - lo$, its item at index $k - lo$ is $p$. By Lemma 3 this is $\mathrm{sel}(A_0, k)$, and $A[k] = p$ by Lemma 1. $\square$

**Theorem 5 (termination).** For every input and every sequence of random choices, the algorithm returns after at most $n$ passes and at most $n(n + 1)/2$ three-way comparisons.

*Proof.* Let $m = hi - lo$, which is at least 1 by (3). By Lemma 1, $lt < gt$. A pass that does not return replaces the range by $A[lo..lt)$ or by $A[gt..hi)$, each of which misses the non-empty $A[lt..gt)$, so $m$ drops by at least 1. So there are at most $n$ passes, and the ranges have sizes at most $n, n - 1, \ldots, 1$. A pass on a range of size $m$ makes $m$ comparisons, which gives the second bound. $\square$

**Theorem 6 (expected comparisons).** Let $C(A_0, k)$ be the number of three-way comparisons. Then $\mathbb{E}[C(A_0, k)] \le 4n$ for every input $A_0$ of size $n$ and every $k$, where the expectation is over the random indices of line L3.

*Proof.* We show by strong induction on $m \ge 1$: for every array range of size $m$ that satisfies Invariant 2 at the start of a pass, the expected number of comparisons from this pass to the end is at most $4m$. Given the range, the later passes depend only on the contents of the range and on fresh random choices.

Fix the range $A[lo..hi)$ with $m$ items. Order its items by value, with ties broken by their index in the range before the pass, and let $r \in \{0, \ldots, m - 1\}$ be the position of the chosen pivot item in this order. Line L3 picks the index uniformly, so $r$ is uniform. The items in $A[lo..lt)$ are smaller than $p$, so they come before the pivot in this order, and there are at most $r$ of them. In the same way, $A[gt..hi)$ has at most $m - 1 - r$ items. So the next range, if any, has a size $m' \le \max(r, m - 1 - r) < m$. This pass makes $m$ comparisons. By the induction hypothesis, the expected cost after this pass, given $r$, is at most $4\max(r, m - 1 - r)$, and it is 0 when the pass returns. So

$$ \mathbb{E}[\text{cost}] \le m + \frac{1}{m} \sum_{r = 0}^{m - 1} 4 \max(r, m - 1 - r) \le m + \frac{8}{m} \sum_{j = \lfloor m/2 \rfloor}^{m - 1} j, $$

since each value $j = \max(r, m - 1 - r)$ is at least $\lfloor m/2 \rfloor$ and is taken by at most two values of $r$. For $m = 2t$ the last sum is $t(3t - 1)/2 = 3m^2/8 - m/4$, and for $m = 2t + 1$ it is $3t(t + 1)/2 = 3(m^2 - 1)/8$. In both cases it is at most $3m^2/8$. So the expected cost is at most $m + 3m = 4m$. For $m = 1$ the pass makes 1 comparison and returns, which is at most 4. The claim for $m = n$ and the first pass is the theorem. $\square$

Theorems 4, 5 and 6 together show that randomized quickselect is a Las Vegas algorithm for the selection problem with at most $4n$ expected and $n(n + 1)/2$ worst-case three-way comparisons, and $O(1)$ extra space, since it stores only $lo$, $hi$, $i$, $p$, $lt$ and $gt$. $\blacksquare$
