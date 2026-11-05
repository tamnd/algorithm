---
title: Sort-and-Count returns the number of inversions and sorts the range
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. For a range $R = A[lo \ldots hi-1]$, write $\operatorname{inv}(R)$ for the number of pairs of indices $lo \le p < q < hi$ with $A[p] > A[q]$, taken at the start of the call. For two finite multisets $L$ and $M$ of items, write $\chi(L, M) = |\{(x, y) \in L \times M : x > y\}|$, counting each copy of an item separately. $\chi(L, M)$ depends only on the two multisets, not on the order in which they are stored.

**Split of the count.** Let $lo \le mid \le hi$, let $L$ be the multiset of $A[lo \ldots mid-1]$ and $M$ the multiset of $A[mid \ldots hi-1]$. Each pair $p < q$ of the range has both indices below $mid$, both indices at least $mid$, or $p < mid \le q$. The pairs of the third kind with $A[p] > A[q]$ are exactly the pairs of $L \times M$ with the first item larger. So

$$\operatorname{inv}(A[lo \ldots hi-1]) = \operatorname{inv}(A[lo \ldots mid-1]) + \operatorname{inv}(A[mid \ldots hi-1]) + \chi(L, M). \tag{1}$$

**Lemma (MERGE-AND-COUNT).** Assume that $lo \le mid \le hi$ and that $A[lo \ldots mid-1]$ and $A[mid \ldots hi-1]$ are sorted, with multisets $L$ and $M$. Then MERGE-AND-COUNT$(A, lo, mid, hi)$ returns $\chi(L, M)$, leaves $A[lo \ldots hi-1]$ sorted with the multiset $L \cup M$, and changes no other item of $A$.

*Proof.* The data movement of lines L6 to L13 is the merge of [merge sort](/merge-sort/), and the counter $c$ does not affect it. So the proof of the merge lemma on the merge sort page shows that the range ends sorted with the multiset $L \cup M$, that no other item changes, and that the write position $k$ never passes the read position $j$. It remains to show what $c$ counts. Let $m = |B| = mid - lo$, and for $j' \in [mid, hi)$ write $r_{j'}$ for the item at index $j'$ at the start of the call; these items are not changed before they are read. We use this invariant of the loop of line L8.

> **(C)** $c = \sum_{j' = mid}^{j - 1} |\{t : 0 \le t < m,\ B[t] > r_{j'}\}|$, and each item of $B[0 \ldots i-1]$ is at most each of $r_j, r_{j+1}, \ldots, r_{hi-1}$.

*Initialization.* Line L7 sets $c = 0$, $j = mid$ and $i = 0$. The sum is empty and $B[0 \ldots -1]$ is empty, so (C) holds.

*Maintenance.* Assume (C) before a step of line L8, so $i < m$ and $j < hi$.

- If $B[i] \le r_j$, line L9 places $B[i]$ and increases $i$. The right half is sorted, so $B[i] \le r_j \le r_{j+1} \le \cdots$, and the second part of (C) holds for $i + 1$. The values $c$ and $j$ do not change, so the first part still holds.
- If $B[i] > r_j$, line L10 places $r_j$, adds $m - i$ to $c$, and increases $j$. Since $B$ is sorted, $B[t] \ge B[i] > r_j$ for each $t \ge i$, so at least $m - i$ items of $B$ are larger than $r_j$. By the second part of (C), each $B[t]$ with $t < i$ is at most $r_j$. So exactly $m - i$ items of $B$ are larger than $r_j$, and the new $c$ is the sum of (C) up to $j' = j$. The second part holds for the new $j$, because $r_{j+1}, \ldots$ are a subset of the old list.

Each step increases $i + j$ by exactly 1, and $i + j \le m + hi$, so the loop stops after at most $m + (hi - mid)$ steps.

*Termination.* The loop stops when $i = m$ or $j = hi$.

- If $j = hi$, the first part of (C) is the sum over all right items, which is $\chi(L, M)$ because $B$ holds the multiset $L$. The loop of line L12 only moves items and does not change $c$.
- If $i = m$ and $j < hi$, the second part of (C) says that each item of $B$ is at most each of $r_j, \ldots, r_{hi-1}$. So these right items have no larger left item, and their terms of $\chi(L, M)$ are 0. The sum of (C) up to $j - 1$ is then $\chi(L, M)$. The loop of line L12 does not run, since $i = m$.

In both cases line L14 returns $\chi(L, M)$. $\square$

**Theorem.** SORT-AND-COUNT$(A, lo, hi)$ returns $\operatorname{inv}(A[lo \ldots hi-1])$, leaves $A[lo \ldots hi-1]$ sorted with the same multiset of items, changes no other item of $A$, and terminates.

*Proof.* By strong induction on $s = hi - lo$.

*Base.* If $s \le 1$, the range has no pair of indices, so its inversion count is 0. Line L1 returns 0 and changes nothing, and a range with at most one item is sorted.

*Step.* Let $s \ge 2$ and assume the claim for all shorter ranges. Line L2 gives $lo < mid < hi$, so the calls of lines L3 and L4 are on ranges of lengths $\lfloor s/2 \rfloor$ and $\lceil s/2 \rceil$, both less than $s$. By the induction hypothesis, line L3 returns $x = \operatorname{inv}(A[lo \ldots mid-1])$, sorts that part and changes nothing else; in particular the right half is not changed. Line L4 then returns $y = \operatorname{inv}(A[mid \ldots hi-1])$ for the original right half and sorts it, without changing the left half. Both halves keep their multisets $L$ and $M$. By the lemma, MERGE-AND-COUNT returns $\chi(L, M)$ and leaves the range sorted with multiset $L \cup M$. By (1), line L5 returns $x + y + \chi(L, M) = \operatorname{inv}(A[lo \ldots hi-1])$. Each call is on a strictly shorter range, so the recursion terminates. $\blacksquare$

**Repeated keys.** The proof never assumes distinct items. An equal pair $B[i] = r_j$ goes to line L9, and it is not counted, which matches the strict test $A[p] > A[q]$ in the definition of an inversion.
