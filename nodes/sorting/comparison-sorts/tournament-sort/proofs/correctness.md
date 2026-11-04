---
title: Tournament sort outputs the items in stable sorted order
proves: [correctness]
status: full
---

We order the indices $0, \ldots, n-1$ by the strict order $i \prec j$ when $A[i] < A[j]$, or when neither $A[i] < A[j]$ nor $A[j] < A[i]$ and $i < j$. This is a total order on the indices, and listing the items in $\prec$ order is the stable sorted order.

For a node $v$ of the tree, let $L(v)$ be the set of indices that are still in the leaves of the subtree of $v$. We write $\min L(v)$ for its least element in $\prec$, or empty if $L(v)$ is empty.

**Lemma 1 (WINNER).** If $T[2v] = \min L(2v)$ and $T[2v + 1] = \min L(2v + 1)$, then WINNER$(T[2v], T[2v + 1]) = \min L(v)$.

*Proof.* $L(v)$ is the union of $L(2v)$ and $L(2v + 1)$, so its least element is the less of the two minima, or the one that exists. If one slot is empty, WINNER returns the other. If both are full, with $i$ from the left subtree and $j$ from the right, then $i < j$ as indices, because the leaves of the left subtree hold smaller indices. WINNER returns $j$ only if $A[j] < A[i]$, which is exactly $j \prec i$ in this case. $\square$

**Invariant (I).** For each internal node $v$, $T[v] = \min L(v)$; each leaf holds its index or is empty.

*After line L2.* The leaves are right by line L1. Line L2 visits the internal nodes from $m - 1$ down to 1, so both children of $v$ are done before $v$. By Lemma 1, each $T[v]$ is right.

*After lines L5 to L7.* Emptying leaf $m + w$ changes $L(v)$ only for the ancestors of that leaf. Line L7 recomputes them from the parent of the leaf up to the root, so each one is recomputed after its children, which are right: the child on the path was just recomputed, and the other child has an unchanged subtree. By Lemma 1, (I) holds again.

**Theorem.** After TOURNAMENT-SORT$(A)$, the array $A$ holds the input items in stable sorted order.

*Proof.* By (I), at step $t$ of line L3 the root holds $\min L(1)$, the $\prec$-least index of the items not yet output. So $B[t]$ is the item with the $(t+1)$-th index in $\prec$ order. After $n$ steps, $B$ lists all items in $\prec$ order, which is the stable sorted order, and line L8 copies it into $A$. $\blacksquare$

**Termination and count.** Each step empties one leaf, so the tree is empty after $n$ steps. The loop of line L6 runs $\lg m$ times per step. Line L2 makes a comparison at a node only when both children are full; each comparison removes one index from the set of candidates for the root, so line L2 makes exactly $n - 1$ comparisons when $n \ge 1$.
