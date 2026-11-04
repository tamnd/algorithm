---
title: Heapsort sorts the array and keeps its items
proves: [correctness, termination]
status: full
---

We write $p(c) = \lfloor (c-1)/2 \rfloor$ for the parent of an index $c \ge 1$. The part $A[0 \ldots m-1]$ is a *heap* when $A[p(c)] \ge A[c]$ for each $c$ with $1 \le c < m$. The *subtree* of $i$ in a heap of size $m$ is the set of indices less than $m$ that have $i$ as an ancestor, together with $i$. Each step of the algorithm is an exchange of two items, so the multiset of items of $A$ never changes. We prove only the order.

**Lemma 1 (SIFT-DOWN).** Let $0 \le i < m$. Assume that each pair $(p(c), c)$ with $c$ in the subtree of $i$ and $c \ne i$ satisfies $A[p(c)] \ge A[c]$, except the pairs whose parent is $i$. Then SIFT-DOWN$(A, i, m)$ stops after at most $\lfloor \lg m \rfloor$ steps of its loop, and after it the subtree of $i$ satisfies the heap order. It changes only items of the subtree of $i$.

*Proof.* Let $i_0$ be the value of $i$ at the call, and let $x$ be the item $A[i_0]$. We use this invariant at the test of line L5, for the current index $i$:

> **(S)** Each pair $(p(c), c)$ with $c$ in the subtree of $i_0$ and $c \ne i_0$ is in heap order, except perhaps the pairs whose parent is $i$. If $i \ne i_0$, then $A[p(i)]$ is at least each child of $i$. The item at $i$ is $x$.

*Initialization.* At the call $i = i_0$, so the first statement is the assumption, and the second statement does not apply.

*Maintenance.* Assume (S) and $2i + 1 < m$. Lines L6 and L7 set $c$ to a child of $i$ with the largest item among the children of $i$. If $A[i] \ge A[c]$, line L8 returns, and $A[i]$ is at least each child, so all pairs with parent $i$ are in order. Together with (S), the full subtree is in heap order. Otherwise $A[c] > A[i] = x$. Line L9 exchanges them. Now the item at $i$ is the old $A[c]$, which is at least the item of the other child of $i$, by the choice of $c$, and at least $x$, the new item at $c$. If $i \ne i_0$, the old $A[c]$ is at most $A[p(i)]$ by the second statement of (S), so the pair $(p(i), i)$ stays in order. The children of $c$ were at most the old $A[c]$, because $(c, \text{child})$ was in order by (S), so after line L10 sets $i \leftarrow c$, the parent of the new $i$ holds the old $A[c]$, which is at least each child of the new $i$. Only the pairs with parent $c$ can now be out of order. So (S) holds for the new $i$.

*Termination.* Each step moves $i$ to a child, so it increases the depth of $i$ by exactly 1. The depth of an index less than $m$ is at most $\lfloor \lg m \rfloor$. So the loop runs at most $\lfloor \lg m \rfloor$ times. If it stops at line L5, then $i$ has no child less than $m$, so there are no pairs with parent $i$, and (S) gives the heap order of the whole subtree. If it stops at line L8, the maintenance step showed the heap order. Each exchange is between $i$ and a child of $i$, both in the subtree of $i_0$. $\square$

**Lemma 2 (build phase).** After line L1, $A[0 \ldots n-1]$ is a heap.

*Proof.* We use the invariant: before the call for $i$, the subtree of each index $j$ with $i < j < n$ is in heap order. At the start $i = \lfloor n/2 \rfloor - 1$. Each $j \ge \lfloor n/2 \rfloor$ has $2j + 1 \ge n$, so it has no child, and its subtree $\{j\}$ is in heap order. Before the call for $i$, both children of $i$ are greater than $i$, so their subtrees are in heap order. These are all the pairs of the subtree of $i$ whose parent is not $i$, so Lemma 1 applies, and after the call the subtree of $i$ is in heap order. The call changes only the subtree of $i$, so the subtree of each $j > i$ that is not inside the subtree of $i$ is unchanged. The subtrees of the indices $j > i$ inside the subtree of $i$ are parts of a subtree in heap order, so they are in heap order too. So the invariant holds for $i - 1$. After the call for $i = 0$, the subtree of 0, which is the whole array, is in heap order. If $n \le 1$ the loop does not run, and an array of at most one item is a heap. $\square$

**Theorem.** HEAPSORT$(A)$ stops, and after it $A$ is sorted in non-decreasing order and holds the same multiset of items.

*Proof.* We use this invariant at the test of line L2, for the current value of $end$:

> **(H)** $A[0 \ldots end]$ is a heap. $A[end+1 \ldots n-1]$ is sorted in non-decreasing order. Each item of $A[0 \ldots end]$ is at most each item of $A[end+1 \ldots n-1]$.

*Initialization.* Before the first step, $end = n - 1$. By Lemma 2, $A[0 \ldots n-1]$ is a heap. The other two parts of (H) are about an empty range.

*Maintenance.* Assume (H) for $end \ge 1$. In a heap, each item is at most the item of its parent, so by induction on the depth each item is at most $A[0]$. So $A[0]$ is a largest item of $A[0 \ldots end]$. Line L3 moves it to $A[end]$. It is at least each item of $A[0 \ldots end-1]$, and by (H) at most each item of $A[end+1 \ldots n-1]$. So $A[end \ldots n-1]$ is sorted, and each item of $A[0 \ldots end-1]$ is at most each item of $A[end \ldots n-1]$. After the exchange, each pair of $A[0 \ldots end-1]$ whose parent is not 0 is still in heap order, because only the item at index 0 changed. So Lemma 1 applies to SIFT-DOWN$(A, 0, end)$, and after line L4, $A[0 \ldots end-1]$ is a heap. SIFT-DOWN changes only indices less than $end$, so the sorted part is unchanged. Then the loop sets $end \leftarrow end - 1$, and (H) holds.

*Termination.* The loop of line L2 runs $n - 1$ times, and each call of SIFT-DOWN stops by Lemma 1. After the last step $end = 0$, and (H) says that $A[1 \ldots n-1]$ is sorted and that $A[0]$ is at most each item of it. So $A[0 \ldots n-1]$ is sorted. If $n \le 1$ the loop does not run, and the array is sorted. $\blacksquare$
