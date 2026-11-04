---
title: Floyd's method builds a max-heap from the keys of the input
proves: [correctness, termination]
status: full
---

Write $T(i)$ for the set of indices in the subtree of node $i$ in the complete binary tree on $\{1, \ldots, n\}$: $i$, its children $2i$ and $2i + 1$ when they are at most $n$, their children, and so on. Say that $T(i)$ *is a heap* when $A[\lfloor j/2 \rfloor] \ge A[j]$ for each $j \in T(i)$ with $j \ne i$. Each index in $T(i)$ other than $i$ is larger than $i$, because a child has a larger index than its parent.

**Lemma (MAX-HEAPIFY).** Let $1 \le i \le n$, and assume that $T(2i)$ and $T(2i+1)$ are heaps (when they exist). Then MAX-HEAPIFY$(A, n, i)$ stops, it permutes the keys of the cells of $T(i)$ and changes no other cell, and afterwards $T(i)$ is a heap.

*Proof.* Let $i_0$ be the first value of $i$. We show that this statement is a loop invariant of line L3, for the current value of $i$:

> **(D)** $i \in T(i_0)$; each edge $(\lfloor j/2 \rfloor, j)$ with $j \in T(i_0) \setminus \{i_0\}$ and $\lfloor j/2 \rfloor \ne i$ holds; and if $i \ne i_0$, then $A[\lfloor i/2 \rfloor] \ge A[c]$ for each child $c$ of $i$ with $c \le n$.

*Initialization.* $i = i_0$. The edges inside $T(i_0)$ that do not start at $i_0$ are the edges inside $T(2i_0)$ and $T(2i_0+1)$, and these hold because the two subtrees are heaps. The last part is empty.

*Maintenance.* Lines L4 to L6 set $m$ to an index of a largest key among $A[i]$, $A[l]$ (if $l \le n$) and $A[r]$ (if $r \le n$): after line L5, $A[m] = \max(A[i], A[l])$, and after line L6, $A[m]$ is also at least $A[r]$. If $m = i$, then each edge out of $i$ holds, so with (D) each edge inside $T(i_0)$ holds, and line L7 returns with $T(i_0)$ a heap. Else $m$ is a child of $i$, $y = A[m] > A[i] = x$, and $y \ge A[s]$ for the other child $s$ of $i$, if it exists. Line L8 swaps $x$ and $y$. Then:

- the edge $(i, m)$ holds, because $y > x$;
- the edge $(i, s)$ holds, because $y \ge A[s]$;
- if $i \ne i_0$, the edge $(\lfloor i/2 \rfloor, i)$ holds, because the last part of (D) gave $A[\lfloor i/2 \rfloor] \ge A[m] = y$;
- for each child $c$ of $m$, the edge $(m, c)$ held before the swap, because (D) excluded only the edges out of $i$, so $y \ge A[c]$, and $y$ is now at $i = \lfloor m/2 \rfloor$.

The edges out of $m$ may now fail, and (D) for the new value $i = m$ excludes exactly them. The last point gives the last part of (D) for $m$. Also $m \in T(i_0)$. So line L9 keeps (D).

*Termination.* Each iteration that does not return replaces $i$ by a child, so the depth of $i$ below $i_0$ grows by exactly 1. The depth is at most the height of $i_0$, so there are at most that many swaps, and then line L7 returns, since a leaf gives $m = i$. Each change is a swap of two cells of $T(i_0)$. $\square$

**Theorem.** BUILD-MAX-HEAP$(A, n)$ stops, and afterwards $A[1 \ldots n]$ is a permutation of its input and satisfies $A[\lfloor j/2 \rfloor] \ge A[j]$ for each $2 \le j \le n$.

*Proof.* We show this invariant of the loop of line L1:

> **(B)** before the iteration for $i$, the subtree $T(j)$ is a heap for each $j$ with $i < j \le n$.

*Initialization.* The first value is $i = \lfloor n/2 \rfloor$. Each $j > \lfloor n/2 \rfloor$ has $2j > n$, so it has no child, and $T(j) = \{j\}$ is a heap. If $n \le 1$ the loop does not run, and the array is a heap.

*Maintenance.* Let $i \ge 1$. The children $2i$ and $2i + 1$ are larger than $i$, so by (B) their subtrees are heaps. The lemma applies: after line L2, $T(i)$ is a heap, and only cells of $T(i)$ changed. Take $j$ with $i - 1 < j \le n$. If $j = i$, $T(j)$ is a heap. If $j \in T(i)$, then $T(j) \subseteq T(i)$, and a subset of a heap of this form is a heap, because its edges are edges of $T(i)$. Else $T(j)$ and $T(i)$ are disjoint: $j$ is not an ancestor of $i$, because an ancestor of $i$ has an index smaller than $i$. So no cell of $T(j)$ changed, and $T(j)$ is still a heap. This is (B) for $i - 1$.

*Termination.* The loop runs $\lfloor n/2 \rfloor$ times, and each call stops by the lemma. After the iteration for $i = 1$, (B) with $i = 0$ says that $T(1) = \{1, \ldots, n\}$ is a heap. Each change is a swap, so $A$ is a permutation of its input. $\blacksquare$
