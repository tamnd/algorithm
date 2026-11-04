---
title: Sink restores a max-heap, and heapsort with sink sorts
proves: [correctness, termination]
status: full
---

Positions run from 1 to $n$. The children of $k$ are $2k$ and $2k + 1$ when they are at most $n$. Let $T(k)$ be the set of positions of the subtree of $k$. A pair $(q, c)$ with $c$ a child of $q$ is *in order* when $\neg\,\text{less}(q, c)$, that is, the item at $q$ is not smaller than the item at $c$. The relation `less` is a strict weak order on the items, so "not smaller" is transitive.

**Lemma (SINK).** Let $k_0$ be a position such that each pair of $T(k_0)$ whose parent is not $k_0$ is in order. Then SINK$(k_0, n)$ ends after at most $\lfloor \lg(n/k_0) \rfloor + 1$ tests of line L1. At the end, each pair of $T(k_0)$ is in order, the items of $T(k_0)$ are a permutation of the old ones, and no other position changes.

*Proof.* We show this invariant at each test of line L1:

> **(I)** $k \in T(k_0)$. (S1) Each pair of $T(k_0)$ whose parent is not $k$ is in order. (S2) If $k \ne k_0$ and $q$ is the parent of $k$, the item at $q$ is not smaller than the item at any child of $k$. Only positions of $T(k_0)$ have changed, by exchanges.

*Initialization.* At the first test, $k = k_0$, (S1) is the hypothesis, and (S2) does not apply.

*Maintenance.* Assume (I) and $2k \le n$. After line L3, $j$ is a child of $k$ whose item is not smaller than the item of the other child, if any. If line L4 breaks, we treat it below. Else $\text{less}(k, j)$: write $x$ for the item at $k$ and $y$ for the item at $j$, so $x < y$. After line L5, $y$ is at $k$ and $x$ is at $j$.

1. The pair $(k, j)$ is in order, since $y > x$.
2. The pair $(k, s)$ for the other child $s$ is in order, by the choice of $j$.
3. If $k \ne k_0$, the pair $(q, k)$ with $q$ the parent of $k$ is in order, since by (S2) the item at $q$ is not smaller than $y$.
4. The pairs $(j, d)$ for the children $d$ of $j$ are the ones that (S1) for the new $k = j$ leaves out.

So (S1) holds for $j$. For (S2): before the exchange, each pair $(j, d)$ was in order by (S1), since $j \ne k$, so $y$ is not smaller than the item at $d$, and $y$ is now at the parent $k$ of $j$. Line L6 sets $k \leftarrow j$, and (I) holds again.

*Termination.* Each pass that does not break replaces $k$ by a child, so $\lfloor \lg(n/k) \rfloor$, the number of levels below $k$, drops by exactly 1, and the loop test fails when no level is left. If the test of line L1 fails, $k$ has no child and (S1) covers all pairs. If line L4 breaks, the item at $k$ is not smaller than the item at $j$, which is not smaller than the item at the other child, so the pairs from $k$ are in order, and with (S1) all pairs of $T(k_0)$ are in order. $\square$

**Lemma (DEL-MAX).** If $pq[1 \ldots n]$ is a max-heap with $n \ge 1$, DEL-MAX returns a largest item and leaves a max-heap of the other $n - 1$ items. *Proof.* The root is a largest item, because each item is joined to the root by a chain of pairs in order. After line L8, position 1 holds the old last item and the heap has $n - 1$ positions. Each pair whose parent is not 1 joins two positions that did not change, so the lemma on SINK with $k_0 = 1$ applies. $\square$

**Theorem (HEAPSORT).** HEAPSORT$(a[1 \ldots n])$ ends, and then $a$ is a permutation of its input in non-decreasing order.

*Proof.* *Construction.* We claim that after the call of line L12 for $k$, the subtree of each position $k' \ge k$ is a max-heap. Before the first call, each position $k' > \lfloor n/2 \rfloor$ has no child, so its subtree is a max-heap. At the call for $k$, the children $2k$ and $2k + 1$ are larger than $k$, so their subtrees are max-heaps, and the lemma on SINK applies. The call changes only positions of $T(k)$, so each subtree $T(k')$ with $k' > k$ is inside $T(k)$, where all pairs are now in order, or disjoint from it, where nothing changed. After the call for $k = 1$, $a[1 \ldots n]$ is a max-heap.

*Sortdown.* Let $N$ be the input size and $m$ the current heap size. We show this invariant at each test of line L13:

> **(H)** $a[1 \ldots m]$ is a max-heap, $a[m+1 \ldots N]$ is in non-decreasing order, and no item of $a[1 \ldots m]$ is larger than an item of $a[m+1 \ldots N]$.

At the first test, $m = N$ and the tail is empty, so (H) follows from the construction. In a pass with $m > 1$, line L14 moves the root, a largest item of the heap, to position $m$, and sets the heap size to $m - 1$. By (H), this item is not larger than the items of the old tail, and it is not smaller than any item that stays in the heap. So the new tail $a[m \ldots N]$ is sorted, and the order between heap and tail holds. Each pair of $a[1 \ldots m-1]$ whose parent is not 1 is unchanged, so the lemma on SINK with $k_0 = 1$ makes $a[1 \ldots m-1]$ a max-heap. Thus (H) holds with $m - 1$.

*Termination.* Each pass lowers $m$ by exactly 1, so the loop runs $N - 1$ times and stops with $m \le 1$. Then $a[1 \ldots m]$ has at most one item, which is not larger than the items of the sorted tail, so $a[1 \ldots N]$ is sorted. Exchanges keep the multiset of the items. $\blacksquare$
