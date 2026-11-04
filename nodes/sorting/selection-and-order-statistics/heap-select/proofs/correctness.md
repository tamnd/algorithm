---
title: Heap-based selection returns the k smallest items in sorted order
proves: [correctness, termination]
status: full
---

Let the input be $a_0, \ldots, a_{n-1}$, let $m = \min(k, n)$, and let $a_{(1)} \le \cdots \le a_{(n)}$ be the input in sorted order. The claim is: HEAP-SELECT$(a, k)$ stops and returns the list $a_{(1)}, \ldots, a_{(m)}$.

A list $H[0 \ldots s-1]$ is a **max-heap** when $H[\lfloor (c-1)/2 \rfloor] \ge H[c]$ for each $1 \le c < s$, that is, each item is at least each of its children. A max-heap of size $s \ge 1$ has its largest item at index 0, since each index is joined to 0 by a chain of parents along which the items do not decrease.

**Lemma 1 (SIFT-DOWN).** Let $0 \le i < s$, and assume that the parent condition holds for each $c$ in the subtrees of the children of $i$, that is, these two subtrees are max-heaps. Then SIFT-DOWN$(H, i, s)$ stops, permutes $H[0 \ldots s-1]$ by swaps inside the subtree of $i$, and after it the subtree of $i$ is a max-heap.

*Proof.* By induction on the height of $i$ in the tree. If $i$ has no child, line L13 returns and the subtree is the single item $H[i]$. Else line L14 picks $c$ as a child of $i$ with the larger item, so $H[c]$ is the largest item of the two children, and by the heap order of the child subtrees it is the largest item of both subtrees. If $H[i] \ge H[c]$, line L15 returns, and $H[i]$ is at least each item below it, so the subtree is a max-heap. Else line L16 swaps $H[i]$ and $H[c]$. Now $H[i]$ is the largest item of the subtree, at least both children; the other child's subtree did not change; and the subtree of $c$ has the max-heap order below its children, so the loop continues at $c$, which has a smaller height. By the induction hypothesis the subtree of $c$ is a max-heap at the end, and its items are the same as before as a multiset, so each of them is at most the new $H[i]$. Each pass moves $i$ down one level, so the loop stops. $\square$

**Lemma 2 (build).** After line L2, $H[0 \ldots m-1]$ is a max-heap and holds $a_0, \ldots, a_{m-1}$.

*Proof.* The indices $i \ge \lfloor m/2 \rfloor$ have no child. Line L2 visits $i = \lfloor m/2 \rfloor - 1, \ldots, 0$. Before the visit of $i$, the subtrees of its children are max-heaps: their roots have larger indices than $i$, so they were visited before, or they are leaves, and later visits of larger indices do not touch them again. By Lemma 1, after the visit the subtree of $i$ is a max-heap. After the visit of $0$ the whole heap is a max-heap. Only swaps are made, so the items are those of line L1. $\square$

**Invariant of the loop of line L3.** Write $P_j = a_0, \ldots, a_{j-1}$ for the prefix of the first $j$ items read. At each test of line L3, when $j$ items have been read:

> **(S)** $H[0 \ldots m-1]$ is a max-heap, and the multiset of its items equals the multiset of the $m$ smallest entries of a sorted order of $P_j$.

1. *Initialization.* If $k = 0$, $m = 0$ and the heap is empty; if $n \le k$, $m = n$ and there is no later item. In the main case $j = m = k$, and by Lemma 2 the heap holds all of $P_k$, which are its $k$ smallest entries.
2. *Maintenance.* Let $x = a_j$ be the next item, and let $y = H[0]$, the largest candidate. Let $s_1 \le \cdots \le s_j$ be $P_j$ sorted, so $H$ holds $s_1, \ldots, s_m$ and $y = s_m$.
   - If $x \ge y$, line L4 does nothing. A sorted order of $P_{j+1}$ is $s_1, \ldots, s_m$ followed by the other items and $x$ in sorted order, since all of these are at least $s_m$. Its first $m$ entries are the items of $H$, so (S) holds.
   - If $x < y$, lines L5 and L6 replace $y$ by $x$. A sorted order of $P_{j+1}$ is obtained by inserting $x$ into $s_1, \ldots, s_j$ at a place before $s_m$. Its first $m$ entries are $x$ and $s_1, \ldots, s_{m-1}$, which is the new multiset of $H$. The children of the root had max-heap subtrees before, and they did not change, so by Lemma 1 the heap is a max-heap after line L6.
3. *Termination of the loop.* Each pass reads one item, and there are $n - m$ of them.

At the end of the loop $j = n$, so by (S) the heap holds $a_{(1)}, \ldots, a_{(m)}$ as a multiset.

**The sort phase.** At each test of line L7 with index $j$, $H[0 \ldots j]$ is a max-heap and $H[j+1 \ldots m-1]$ holds the $m - 1 - j$ largest items of the heap in increasing order, each at least each item of $H[0 \ldots j]$. At the start $j = m - 1$ and the second part is empty. Line L8 moves the largest item $H[0]$ of the first part to index $j$, which keeps the order of the second part, and line L9 restores the heap order of $H[0 \ldots j-1]$ by Lemma 1, since the subtrees of the children of the root did not change. The loop runs $m - 1$ times, and at the end $H[0]$ is the smallest item and $H[1 \ldots m-1]$ is increasing. So $H = a_{(1)}, \ldots, a_{(m)}$ in this order, which line L10 returns. $\blacksquare$
