---
title: The Fibonacci buddy system keeps a legal state, finds each buddy with two bits, and has canonical free lists
proves: [correctness, termination]
status: full
---

**Setting.** Let $S_0 = 1$, $S_1 = 2$ and $S_k = S_{k-1} + S_{k-2}$ for $k \ge 2$. The heap is $[0, S_m)$. The *split tree* has the root $(0, m)$. A node $(a, k)$ stands for the interval $[a, a + S_k)$. A node $(a, k)$ with $k \ge 2$ has the left child $(a, k - 1)$ and the right child $(a + S_{k-1}, k - 2)$, and these two children are *buddies*. Nodes of order 0 and 1 are leaves. Each node also has two bits: the root has $(LR, IN) = (0, 0)$, and a node with bits $(x, y)$ gives its left child $(0, x)$ and its right child $(1, y)$.

**Fact 1 (laminar family).** The two children of a node tile its interval, so by induction on the depth, the intervals of two nodes are either disjoint or nested, and a node is inside another only if it is a descendant. A child is strictly shorter than its parent, so different nodes have different intervals or, at the same address, different orders. So a node is fixed by its pair $(a, k)$. The root is the only node of order $m$, because every other node is a descendant and has a smaller order.

**Fact 2 (the buddy rule).** Let $(a, k)$ be a node other than the root. If it is a left child, the parent is $(a, k + 1)$ and the buddy is $(a + S_k, k - 1)$. If it is a right child, the parent $(p, j)$ has $a = p + S_{j-1}$ and $k = j - 2$, so the parent is $(a - S_{k+1}, k + 2)$ and the buddy is $(a - S_{k+1}, k + 1)$. By the bit rule, a node that is not the root has $LR = 0$ exactly when it is a left child. So line L12 computes the buddy of a non-root node from its address, its order and its LR bit.

**Fact 3 (merge restores the bits).** If a parent has bits $(x, y)$, its children have bits $(0, x)$ and $(1, y)$, so the IN bit of the left child is $x$ and the IN bit of the right child is $y$. So line L16 gives the merged block the bits $(x, y)$ of the parent.

A state is the family $F_k$ = AVAIL$[k]$ of free blocks of each order, the family $A$ of allocated blocks, and the order and bits stored with each block. The state is *legal* when:

- **(T)** all blocks of $F$ and $A$ are nodes of the split tree, and their intervals tile $[0, S_m)$ with no gap and no overlap;
- **(L)** each block carries the order and the bits of its node;
- **(B)** no two blocks of $F$ are buddies of each other.

**Lemma 1 (each call keeps a legal state).** If the state is legal before FIB-MALLOC or FIB-FREE, it is legal after it.

*Proof.* The start state holds only the root with bits $(0, 0)$, which is legal.

*Malloc.* If line L3 returns FAIL, nothing changes. Otherwise line L4 removes a free node $C = (a, j)$ with $j \ge k$. The loop of lines L5 to L8 keeps this invariant: $C$ is a node with its bits, $j \ge k$, and the blocks of $F$, the blocks of $A$ and $C$ tile the heap. A pass runs only when $j \ge 2$, so $C$ has two children, and lines L6 to L8 give them the bits of the tree by the bit rule. The children tile $C$. If $j - 2 \ge k$, the right child becomes $C$, and the left child goes to $F$. Otherwise $j - 1 \ge k$ by the loop test, and the left child becomes $C$. In both cases $j \ge k$ stays true. So (T) and (L) hold when line L9 puts $C$ in $A$.

For (B), take a block $X$ that a pass puts in $F$. Its buddy is the node that the same pass keeps as $C$. That node is never a block of $F$: it is either allocated at line L9 or split by a later pass. Two new free blocks are not buddies of each other, because the buddy of each one is a kept node. Now take an old free block $Y$. It is disjoint from the removed node, because of (T). By Fact 1 the buddy of $Y$ is disjoint from the removed node or contains it, so the buddy of $Y$ is not one of the new blocks, which are strictly inside the removed node. Line L4 removes a block, which cannot break (B).

*Free.* Line L10 reads the block $P = (a, j)$ and its bits, and the block leaves $A$. The loop of lines L11 to L16 keeps the invariant: $P$ is a node with its bits, the blocks of $F$, the blocks of $A$ and $P$ tile the heap, and (B) holds for $F$. In a pass, $j < m$, so $P$ is not the root (Fact 1), and line L12 finds the buddy node $(b, i)$ by Fact 2. Line L13 checks if $b$ is in AVAIL$[i]$. Because a node is fixed by its address and its order (Fact 1), this is true exactly when the buddy node itself is a free block. Then line L14 removes it, and line L16 makes $P$ the parent, whose interval is the union of the two buddies, with the bits of the parent by Fact 3. So the invariant holds after the pass. The loop ends when $j = m$, so $P$ is the root and has no buddy, or when the buddy of $P$ is not a free block. Then no block of $F$ is the buddy of $P$, and line L17 adds $P$ to $F$ with (B) intact. $\square$

**Lemma 2 (termination).** Each call ends after at most $m$ passes of its loop.

*Proof.* Each pass of the malloc loop lowers $j$ by 1 or 2 and needs $j \ge 2$. Each pass of the free loop replaces $P$ with its parent, whose order is larger by 1 or 2, and the order of a node is at most $m$. $\square$

**Lemma 3 (no hidden free buddies).** In a legal state, let $Y$ be a node that is not a free block, and assume that $Y$ is covered by free blocks that lie strictly inside $Y$. Then two of these free blocks are buddies.

*Proof.* By strong induction on the order of $Y$. A node of order 0 or 1 has no node strictly inside it, so it cannot be covered in this way, and the claim holds trivially. Let $Y$ have order at least 2, with children $Y_1$ and $Y_2$. Every node strictly inside $Y$ is inside $Y_1$ or inside $Y_2$ (Fact 1), so each child is covered by the free blocks inside it. If both children are free blocks, they are free buddies. Otherwise one child $Y_i$ is not a free block, and it is covered by free blocks strictly inside it, so the induction gives two free buddies inside $Y_i$. $\square$

**Lemma 4 (canonical form).** Call a node *empty* when it meets no block of $A$, and *maximal* when it is empty and it is the root or its parent is not empty. In a legal state, the free blocks are exactly the maximal nodes.

*Proof.* (a) *Each free block is maximal.* A free block $X$ is empty by (T). Assume that $X$ is not the root and that its parent is empty. Then its buddy $Y$ is empty, so by (T) it is covered by free blocks. A free block that meets $Y$ is inside $Y$: otherwise, by Fact 1, it contains $Y$, so it contains the parent, so it meets $X$, which (T) forbids. If $Y$ is a free block, then $X$ and $Y$ are free buddies. If not, Lemma 3 gives two free buddies inside $Y$. Both cases contradict (B).

(b) *Each maximal node is free.* Let $X$ be maximal. By (T), $X$ is covered by free blocks, and each of them is inside $X$ or contains $X$. A free block that contains $X$ strictly contains the parent of $X$, which is not empty, against (T). So all of them are inside $X$. If one of them is strictly inside $X$, then by (a) it is maximal, so its parent is not empty; but its parent is inside $X$, which is empty. So $X$ itself is a free block. $\square$

**Theorem.** Run any sequence of calls from the start state. Then:

1. the state is legal after each call, and each call ends;
2. after each call, the free lists are the maximal nodes of the current set $A$, so they depend only on $A$;
3. FIB-MALLOC$(n)$ returns FAIL exactly when $S_m < n$ or no node of order at least $k$ is empty, where $k$ is the least order with $S_k \ge n$;
4. a returned block has at least $n$ words and does not meet any other allocated block;
5. when $A$ becomes empty, AVAIL$[m]$ holds only the root and the other lists are empty.

*Proof.* (1) follows from Lemmas 1 and 2 by induction on the number of calls. (2) is Lemma 4. (3): if a node of order at least $k$ is empty, then its largest empty ancestor is maximal, so by (2) it is a free block of order at least $k$, and line L2 finds it. Conversely, a free block is an empty node, so if no node of order at least $k$ is empty, line L3 returns FAIL. (4) follows from the loop invariant $j \ge k$, so $S_j \ge S_k \ge n$, and from the tiling in (T). (5): when $A$ is empty, the root is empty, so it is the only maximal node, and by (2) it is the only free block. $\blacksquare$
