---
title: Stooge sort sorts the range and keeps its items
proves: [correctness]
status: full
---

Each change to the array is the swap of line L1, inside the range of the call. So each call keeps the multiset of the items of its range and changes no item outside it. To speak of "the $k$ largest items" when there are equal keys, we fix a strict total order on the items: compare by key, and on a tie by the index that the item had at the start of the call. An array is sorted by key when it is sorted in this order, so it is enough to prove that the call sorts the range in this order.

**Theorem.** For each range $A[lo \ldots hi]$ with $m = hi - lo + 1 \ge 1$, STOOGE-SORT$(A, lo, hi)$ sorts the range.

*Proof.* By strong induction on $m$.

*Base.* If $m = 1$, the range is sorted, and line L1 compares the item with itself and does nothing. If $m = 2$, line L1 swaps the two items when they are out of order, and line L2 stops. So the range is sorted.

*Step.* Let $m \ge 3$, and assume the claim for all ranges with fewer than $m$ items. Line L1 changes the multiset of no part, so we ignore it. Let $k = \lfloor m/3 \rfloor \ge 1$. Then $3k \le m$, so $m - k \ge 2k$, and $m - k < m$. The three calls of lines L4, L5 and L6 are on ranges of $m - k$ items, so by the hypothesis each one sorts its range.

Let $L$ be the set of the $k$ largest items of the range. Before line L4, let $j$ be the number of items of $L$ in the first part $P = A[lo \ldots hi - k]$; the other $k - j$ items of $L$ are in $A[hi - k + 1 \ldots hi]$, which line L4 does not change. After line L4, $P$ is sorted, so its $j$ largest items are in its last $j$ positions, $A[hi - k - j + 1 \ldots hi - k]$. Each item of $L$ is larger than each item not in $L$, so these $j$ items are exactly the items of $L$ in $P$. Since $j \le k$ and $|P| = m - k \ge 2k$, the first of these positions is $hi - k - j + 1 \ge hi - 2k + 1 \ge lo + k$, because $hi - lo + 1 = m \ge 3k$. So after line L4, all $k$ items of $L$ are in $Q = A[lo + k \ldots hi]$.

Line L5 sorts $Q$. Its $k$ largest items are the items of $L$, so after line L5 they are in the last $k$ positions $A[hi - k + 1 \ldots hi]$, in sorted order. The other $m - k$ items, none of them in $L$, are in $A[lo \ldots hi - k]$.

Line L6 sorts $A[lo \ldots hi - k]$ and does not change $A[hi - k + 1 \ldots hi]$. Now $A[lo \ldots hi - k]$ is sorted, $A[hi - k + 1 \ldots hi]$ is sorted, and each item of the first part is not in $L$, so it is less than each item of the second part. So the range is sorted. $\blacksquare$

**Termination.** Each call on $m \ge 3$ items makes three calls on $m - \lfloor m/3 \rfloor < m$ items, and a call on at most two items makes no call. So the recursion stops.

**Why the rounding matters.** The step used $m - k \ge 2k$. With $k = \lceil m/3 \rceil$ this fails for $m = 4$: then $k = 2$ and $m - k = 2 < 4$. On $[0, 2, 1, 3]$ the calls sort $A[0 \ldots 1]$, $A[2 \ldots 3]$ and $A[0 \ldots 1]$, which change nothing, and the output is not sorted.
