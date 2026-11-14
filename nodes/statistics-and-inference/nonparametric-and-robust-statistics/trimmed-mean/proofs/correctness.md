---
title: TRIMMED-MEAN returns the mean of the middle order statistics
proves: [correctness]
status: full
---

Let $x_{(1)} \le \cdots \le x_{(n)}$ be the sorted sample and $g = \lfloor \alpha n \rfloor$ with $n - 2g \ge 1$. For a list $B$, write $\operatorname{sort}(B)$ for its values in non-decreasing order, and $\{\!\{B\}\!\}$ for its multiset. The arithmetic is exact.

**Lemma 1 (three-way partition).** Let the loop of SELECT start a round on $A[lo \ldots hi]$ with pivot value $p$. When the inner loop stops, the range is a permutation of its old content, and with the final indices $lt \le gt$,
$$A[lo \ldots lt-1] < p, \qquad A[lt \ldots gt] = p, \qquad A[gt+1 \ldots hi] > p,$$
and $lt \le gt$ (the part equal to $p$ is not empty).

*Proof.* The loop keeps the invariant: $A[lo \ldots lt-1] < p$, $A[lt \ldots i-1] = p$, $A[gt+1 \ldots hi] > p$, and $A[i \ldots gt]$ is not yet seen. At the start $lt = i = lo$ and $gt = hi$, and all three parts are empty. Each step looks at $A[i]$. If $A[i] < p$, the swap with $A[lt]$ moves an item equal to $p$ (or $A[i]$ itself when $lt = i$) to position $i$, and both indices grow. If $A[i] > p$, the swap puts it at $gt$, and $gt$ shrinks. Otherwise $i$ grows. Each step changes the range only by a swap, and shrinks the unseen part by one. The loop ends when $i = gt + 1$, so the unseen part is empty. The pivot $p$ is a value of the range, so the middle part holds at least that item. $\square$

**Lemma 2 (SELECT).** After SELECT$(A, lo, hi, k)$ with $lo \le k \le hi$, the range $A[lo \ldots hi]$ is a permutation of its old content, the rest of $A$ is unchanged, and
$$A[lo \ldots k-1] \le A[k] \le A[k+1 \ldots hi].$$

*Proof.* Invariant of the outer loop: the current window $[lo', hi']$ contains $k$, every item left of the window (inside the original range) is at most every item in the window, and every item right of the window is at least every item in the window. It holds at the start. After a round with $k < lt$, the new window $[lo', lt - 1]$ contains $k$; the items in $A[lt \ldots hi']$ are at least $p$, and so at least every item of the new window (all $< p$). The case $k > gt$ is symmetric. The window shrinks by at least one item per round (Lemma 1, the middle part is not empty), so the loop ends. It ends when the window has one item, or when $lt \le k \le gt$. In the second case $A[k] = p$, all items of $A[lo' \ldots k-1]$ are at most $p$, and all of $A[k+1 \ldots hi']$ are at least $p$. With the invariant this gives the claim. Only swaps inside the range change $A$. $\square$

**Lemma 3 (split).** Let $B = A[lo \ldots hi]$ satisfy $A[lo \ldots k-1] \le A[k] \le A[k+1 \ldots hi]$, and let $j = k - lo$. Then $\{\!\{A[lo \ldots k-1]\}\!\}$ is the multiset of the first $j$ entries of $\operatorname{sort}(B)$, $A[k]$ is entry $j$ (from 0), and $\{\!\{A[k+1 \ldots hi]\}\!\}$ is the multiset of the rest.

*Proof.* Sort the left part and the right part separately. The list $\operatorname{sort}(A[lo \ldots k-1]),\ A[k],\ \operatorname{sort}(A[k+1 \ldots hi])$ is non-decreasing, because every item on the left is at most $A[k]$ and every item on the right is at least $A[k]$. It has the multiset of $B$. A multiset has exactly one non-decreasing list, so this list is $\operatorname{sort}(B)$. Read off the parts. $\square$

**Theorem.** TRIMMED-MEAN returns $\frac{1}{n-2g}\sum_{i=g+1}^{n-g} x_{(i)}$.

*Proof.* Line L1 makes $A$ a copy of $x$, so $\operatorname{sort}(A) = (x_{(1)}, \ldots, x_{(n)})$. By Lemmas 2 and 3, after line L3,
$$\{\!\{A[0 \ldots g-1]\}\!\} = \{\!\{x_{(1)}, \ldots, x_{(g)}\}\!\}, \qquad \{\!\{A[g \ldots n-1]\}\!\} = \{\!\{x_{(g+1)}, \ldots, x_{(n)}\}\!\}.$$
Line L4 changes only $A[g \ldots n-1]$. Its sorted content is $(x_{(g+1)}, \ldots, x_{(n)})$, and the position $n - g - 1$ is at offset $j = n - 2g - 1$ in it. By Lemmas 2 and 3, afterwards
$$\{\!\{A[g \ldots n-g-2]\}\!\} = \{\!\{x_{(g+1)}, \ldots, x_{(n-g-1)}\}\!\}, \qquad A[n-g-1] = x_{(n-g)}.$$
So $\{\!\{A[g \ldots n-g-1]\}\!\} = \{\!\{x_{(g+1)}, \ldots, x_{(n-g)}\}\!\}$. A sum does not depend on the order of its terms, so line L5 computes $s = \sum_{i=g+1}^{n-g} x_{(i)}$, and line L6 divides by the count $n - 2g \ge 1$, which line L2 checks. $\square$

**Expected cost.** Each round of SELECT costs at most $hi' - lo' + 1$ comparisons. With a uniform random pivot, the window keeps at most $3/4$ of its items with probability at least $1/2$: this holds when the pivot rank lies in the middle half. So the expected number of rounds before the window size drops below $(3/4)^j m$ is at most 2 per level $j$, and the expected total is at most $\sum_j 2 (3/4)^j m = 8m$ comparisons for a range of $m$ items. The two calls cost at most $8n + 8(n - g)$ in expectation, and lines L1, L5 and L6 cost $O(n)$. In the worst case each round removes one item, which gives $O(m^2)$.
