---
title: Weak heapsort sorts the array
proves: [correctness]
status: full
---

**Notation.** For a node $s$ of the tree on the indices $0, 1, \ldots$, let $T(s)$ be the set of indices in the subtree of $s$. The children of $s$ are $2s$ and $2s + 1$ whatever the bit $r[s]$, so $T(s)$ does not depend on the bits; only the names "left" and "right" do, and those of $s$ depend only on $r[s]$. The bit $r[0]$ is never flipped, because 0 is never the second argument of JOIN; so node 1 is the right child of the root. For a heap of size $m$ we only look at the indices below $m$. We use this property of a node $s \ge 1$:

> **R(s)**: $A[d(s)] \ge A[k]$ for each $k \in T(s)$.

If R(c) holds for the right child $c$ of $s$, then $d(c) = s$ and $A[s]$ is at least each item of the right subtree of $s$. If R(1) holds, $A[0]$ is at least each item of the heap.

**Lemma (a join step).** Let $j \ge 1$ and $d = d(j)$, and suppose R(s) holds for each proper descendant $s$ of $j$. After JOIN$(d, j)$, R(s) holds for $j$ and for each proper descendant of $j$. Moreover, for each node $s$ outside $T(j)$, if R(s) held before, it still holds.

*Proof.* Let $u$ and $v$ be the items at $d$ and $j$ before the join. Let $c$ be the right child of $j$ and $z$ the left child (either may be missing). Then $d(c) = j$, so R(c) gives $v \ge$ each item of $T(c)$. And $z$ is a left child, so the climb from $z$ goes through $j$, and $d(z) = d(j) = d$; so R(z) gives $u \ge$ each item of $T(z)$.

*No swap*, so $u \ge v$. Nothing changes. Now $u \ge v$, $u \ge T(z)$ and $u \ge v \ge T(c)$, so R(j) holds. The other statements did not change.

*Swap*, so $u < v$. Now $A[d] = v$, $A[j] = u$, and $r[j]$ is flipped, so $z$ is the right child and $c$ the left child of $j$. R(j): $A[d] = v$ is at least $u$, at least $T(c)$, and at least $u \ge T(z)$. For a proper descendant $s$ of $j$, the climb from $s$ to $d(s)$ changes only if it passes through $c$ or $z$ as a child of $j$:

- If $s$ is on the left spine of $c$, then before the join $d(s) = j$; now $c$ is a left child, the climb goes on through $j$, and $d(s) = d$, with $A[d] = v \ge T(c) \supseteq T(s)$.
- If $s$ is on the left spine of $z$, then before the join $d(s) = d$; now $z$ is a right child, so $d(s) = j$, with $A[j] = u \ge T(z) \supseteq T(s)$.
- Otherwise $d(s)$ is a proper descendant of $j$, its item did not change, and $T(s)$ does not contain $d$ or $j$. So R(s) still holds.

For a node $s$ outside $T(j)$: if $s$ is not an ancestor of $j$, then $T(s)$ contains neither $j$ nor $d$ (as $d$ is an ancestor of $j$, or $T(s)$ would contain $j$) and $d(s)$ is neither, except perhaps $d(s) = d$, where the item only grew. If $s$ is an ancestor of $j$, then $d(s)$ is not $j$; if $T(s)$ contains $d$ the two changed items stay in $T(s)$, and its set of items is the same; if $T(s)$ does not contain $d$, then $s$ is strictly between $d$ and $j$, so $d(s) = d$, whose item grew, and the item at $j$ fell. In each case R(s) still holds. $\square$

**The build.** We claim that after the step of line L3 for $j$, R(s) holds for each $s \ge j$. For $j = n - 1$ before the step, there are no nodes above $n - 1$. Each proper descendant of $j$ has a larger index, so the lemma applies, and it gives R for $j$ and for all its descendants, and keeps R for the other nodes $s > j$. After $j = 1$, R holds for all nodes, so $A[0..n-1]$ is a weak heap.

**The sort.** Suppose that before line L5, R holds for each node of the heap $A[0 \ldots m]$. Then $A[0]$ is its largest item, and line L5 puts it at index $m$; the heap is now $A[0 \ldots m-1]$. Removing index $m$ only shrinks the sets $T(s)$. The item at 0 changed, so R(s) may fail only for the nodes with $d(s) = 0$, which are the nodes $1 = s_1, s_2, \ldots, s_t$ of the left spine of node 1 below $m$, the nodes found by line L6. Lines L7 and L8 join $s_t, s_{t-1}, \ldots, s_1$ with the root in this order. When $s_i$ is joined, its proper descendants are $T(s_{i+1})$, where R holds by the lemma for the earlier step, and the nodes of its right subtree, whose distinguished ancestors are not 0, so R held for them all along. The lemma applies, and after $s_1$, R holds for all nodes of $A[0 \ldots m-1]$.

**Theorem.** WEAK-HEAPSORT$(A)$ sorts $A$ and keeps its items.

*Proof.* All changes are swaps, so the multiset of items is kept. By the build and by induction over the steps of line L4, each step puts the largest item of $A[0 \ldots m]$ at index $m$, and the later steps work only inside $A[0 \ldots m-1]$. So $A[m] \ge A[k]$ for each $k < m$, for $m \ge 2$. Before line L9, R(1) holds for the heap $A[0 \ldots 1]$, so $A[0] \ge A[1]$, and the swap orders them. So the array is sorted. $\blacksquare$
