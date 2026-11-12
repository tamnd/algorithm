---
title: The buddy system keeps a legal state, and its free lists are the maximal free tree blocks
proves: [correctness, termination]
status: full
---

**Setting.** The heap is $[0, 2^m)$. A *tree block* of order $k$ is $[a, a + 2^k)$ with $0 \le k \le m$ and $a$ a multiple of $2^k$. Two tree blocks are either disjoint or one contains the other: if $[a, a + 2^k)$ and $[b, b + 2^j)$ meet and $j \le k$, then $b$ lies in $[a, a + 2^k)$, and because $2^j$ divides $2^k$ the whole block $[b, b + 2^j)$ lies in it too. Each tree block of order $k < m$ has a parent of order $k + 1$ and a buddy, the other half of the parent. By the lemma on the page, the buddy of $[a, a+2^k)$ starts at $a \oplus 2^k$.

A state is the family $F_k$ = AVAIL$[k]$ of free blocks of each order and the family $A$ of allocated blocks with their orders. The state is *legal* when:

- **(T)** all blocks of $F$ and $A$ are tree blocks, and they tile $[0, 2^m)$ with no gap and no overlap;
- **(B)** no two blocks of $F$ are buddies of each other.

**Lemma 1 (each call keeps a legal state).** If the state is legal before BUDDY-MALLOC or BUDDY-FREE, it is legal after it.

*Proof.* At the start, $F_m = \{0\}$ and all else is empty, which is legal.

*Malloc.* If line L3 returns FAIL, nothing changes. Otherwise line L4 removes a free block $[L, L + 2^j)$. The loop of lines L5 to L7 keeps this invariant: the blocks of $F$, the blocks of $A$ and the block $[L, L + 2^j)$ tile the heap, and they are tree blocks. A pass replaces $[L, L+2^j)$ with its two halves $[L, L + 2^{j-1})$ and $[L + 2^{j-1}, L + 2^j)$, both tree blocks, and puts the upper half in $F_{j-1}$. So (T) holds when the loop ends with $j = k$, and line L8 puts $[L, L + 2^k)$ in $A$. For (B): a free block $X$ that line L7 adds is the buddy of the block that is kept, which is not free. If $X$ were the buddy of another free block $Y$, then $Y$ would be the kept block, a contradiction. The blocks of $F$ before the call were disjoint from $[L, L + 2^j)$ and were not buddies of each other; a buddy of such a block is either disjoint from $[L, L + 2^j)$ or contains it, so it is not one of the new blocks, which are strictly inside $[L, L + 2^j)$. Line L4 removes a block, which cannot break (B).

*Free.* Line L9 removes $[L, L + 2^k)$ from $A$. The loop of lines L10 to L14 keeps the invariant: the blocks of $F$, the blocks of $A$ and the *pending* block $[L, L + 2^k)$ tile the heap, all are tree blocks, and no two blocks of $F$ are buddies. In a pass, line L12 finds that the buddy $P$ is in $F_k$. Line L13 removes it, and line L14 makes the pending block the parent, the union of the two halves, which is a tree block. So the invariant holds after the pass. The loop ends when $k = m$ or the buddy is not in $F_k$. Line L15 adds the pending block to $F_k$. If $k = m$, the pending block is the whole heap and has no buddy. Otherwise its buddy is not in $F_k$, and no other block is its buddy. So (B) holds. $\square$

**Lemma 2 (termination).** BUDDY-MALLOC runs at most $m$ passes of the loop of line L5, and BUDDY-FREE runs at most $m$ passes of the loop of line L10.

*Proof.* Each pass of line L5 lowers $j$ by 1, from $j \le m$ down to $k \ge 0$. Each pass of line L10 raises $k$ by 1, and the loop stops at $k = m$. $\square$

**Lemma 3 (canonical form).** In a legal state, the free blocks are exactly the maximal tree blocks that meet no allocated block. A tree block $X$ is *empty* when it meets no block of $A$, and *maximal* when it is empty and $X$ is the root or its parent is not empty.

*Proof.* (a) *Each free block is maximal.* A free block $X$ meets no allocated block by (T), so it is empty. Assume that $X$ is not the root and that its parent is empty. Then the buddy $Y$ of $X$ is empty. By (T), $Y$ is covered by free blocks. Each free block that meets $Y$ lies inside $Y$: a tree block that meets $Y$ and is not inside $Y$ contains $Y$, so it contains the parent, so it meets $X$, which (T) forbids. Among the free blocks inside $Y$, take one, $Z$, of the smallest order. If $Z = Y$, then $X$ and $Y$ are free buddies, against (B). If $Z \ne Y$, the buddy $Z'$ of $Z$ lies inside $Y$, and by the same argument $Z'$ is covered by free blocks inside $Z'$. These have an order at most the order of $Z$, and by the choice of $Z$ the order is equal, so $Z'$ itself is free. Then $Z$ and $Z'$ are free buddies, against (B). So the parent is not empty, and $X$ is maximal.

(b) *Each maximal block is free.* Let $X$ be maximal. By (T), $X$ is covered by free blocks, and as in (a) each of them is inside $X$ or contains $X$. A free block that contains $X$ strictly contains the parent of $X$, which is not empty, so it meets an allocated block, against (T). So all of them are inside $X$. If one of them is not $X$, it lies strictly inside $X$ and is free; by (a) it is maximal, so its parent is not empty. But its parent lies inside $X$, which is empty. This is a contradiction, so $X$ itself is free. $\square$

**Theorem.** Run any sequence of calls from the start state. Then: (1) the state is legal after each call; (2) after each call, the free lists equal the family of maximal empty tree blocks of the current set $A$; (3) BUDDY-MALLOC$(n)$ returns FAIL only if no tree block of order $\lceil \lg n \rceil$ is empty; (4) a returned block has $2^{\lceil \lg n \rceil} \ge n$ words, starts at a multiple of this size, and does not meet any other allocated block; (5) when $A$ becomes empty, AVAIL$[m] = \{0\}$ and the other lists are empty.

*Proof.* (1) follows from Lemma 1 by induction on the number of calls, and Lemma 2 shows that each call ends. (2) is Lemma 3. (3): if a tree block $X$ of order $k$ is empty, then the largest empty tree block that contains $X$ is maximal (the chain of ancestors of $X$ is finite and emptiness passes from a block to its children), so by (2) it is a free block of order at least $k$, and line L2 finds a $j$. (4) follows from line L1, the alignment in (T) and the tiling in (T). (5): when $A$ is empty, the root is empty, so it is the only maximal empty block, and by (2) it is the only free block. $\blacksquare$
