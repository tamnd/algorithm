---
title: The lazy buddy system keeps its slack nonnegative and gives back the whole heap when all blocks are freed
proves: [correctness, termination]
status: full
---

**Setting.** The heap is $[0, 2^m)$, and *tree blocks* are as in the [buddy system](/buddy-system/): a tree block of order $k$ is $[p, p + 2^k)$ with $p$ a multiple of $2^k$, two tree blocks are disjoint or nested, and the buddy of a tree block of order $k < m$ starts at $p \oplus 2^k$. A state is the set of active blocks (with $A_k$ of order $k$), the lists LOCAL$[k]$ (with $L_k$ blocks) and the lists GLOBAL$[k]$. The state is *legal* when:

- **(T)** all active, locally free and globally free blocks are tree blocks of their stated order, and they tile $[0, 2^m)$;
- **(B)** no two globally free blocks are buddies;
- **(S)** $0 \le L_k \le A_k$ for each $k$, that is, the slack $D_k = A_k - L_k$ is at least 0.

**Lemma 1 (GLOBAL-FREE).** Let the state satisfy (T) and (B), except that one tree block $P$ of order $k$ is in no list and in no active set (it is *pending*). Then GLOBAL-FREE$(P, k)$ ends after at most $m - k$ passes, and after it (T) and (B) hold with $P$, or a block that contains it, in GLOBAL.

*Proof.* The loop keeps the invariant: the pending block is a tree block, it and the other blocks tile the heap, and (B) holds among the globally free blocks. A pass finds the buddy $Q$ of the pending block in GLOBAL$[k]$, removes it, and makes the pending block the parent, which is the union of the two and a tree block. So the invariant holds after the pass. Each pass raises $k$, so the loop ends after at most $m - k$ passes. At the end, $k = m$ and the pending block is the whole heap, or its buddy is not in GLOBAL$[k]$. In both cases no globally free block is its buddy, so line L12 keeps (B). $\square$

**Lemma 2 (each call keeps a legal state).** If the state is legal before LAZY-MALLOC or LAZY-FREE, it is legal after it.

*Proof.* The start state has GLOBAL$[m] = \{0\}$ and nothing else, which is legal.

*Malloc.* Lines L2 and L3 move one free block of order $k$ to the active set. (T) holds, (B) holds because a block left GLOBAL, and (S) holds because $A_k$ grows by 1 and $L_k$ does not grow. Line L4 removes a free block $X$ of order $j > k$ from LOCAL$[j]$ or GLOBAL$[j]$, which can only lower $L_j$, and splits it as the buddy system does: each pass replaces the kept block with its two halves and puts the upper half in GLOBAL. The new globally free blocks lie strictly inside $X$. The buddy of each one is the half that the same pass kept, which is never globally free. An old globally free block is disjoint from $X$, so its buddy is disjoint from $X$ or contains $X$, and it is not a new block. So (B) holds. (T) holds as in the buddy system, and line L5 then raises $A_k$, so (S) holds.

*Free.* Line L6 reads $D = A_k - L_k \ge 0$ and moves the block $p$ out of the active set, so now $A'_k = A_k - 1$.

- *Lazy case*, $D \ge 2$. Line L7 puts $p$ in LOCAL$[k]$. Then $L'_k = L_k + 1$, and $A'_k - L'_k = D - 2 \ge 0$. (T) holds, and (B) holds because GLOBAL did not change.
- *Reclaiming case*, $D = 1$. Line L8 frees $p$ globally. By Lemma 1, (T) and (B) hold. $L_k$ did not change, and $A'_k - L_k = 0$.
- *Accelerated case*, $D = 0$. Then $L_k = A_k \ge 1$, because $p$ was active, so line L9 can remove a block $q$ from LOCAL$[k]$. Then $A'_k - L'_k = (A_k - 1) - (L_k - 1) = 0$. The first call of GLOBAL-FREE keeps (T) and (B) with $q$ as a block that is in no list, which counts as in use for (B); it is pending for the second call, so by Lemma 1 again (T) and (B) hold at the end.

GLOBAL-FREE changes only GLOBAL lists, so it does not change any $A_j$ or $L_j$, and (S) holds for every class. $\square$

**Lemma 3 (termination and cost).** LAZY-MALLOC runs at most $m$ split passes, and LAZY-FREE runs at most $2m$ merge passes.

*Proof.* Line L4 splits from an order at most $m$ down to $k \ge 0$. LAZY-FREE calls GLOBAL-FREE at most twice, and each call does at most $m$ passes by Lemma 1. $\square$

**Lemma 4 (canonical form without local blocks).** If the state is legal and all LOCAL lists are empty, then the globally free blocks are exactly the maximal tree blocks that meet no active block.

*Proof.* With no local blocks, (T) and (B) are the legal state of the eager buddy system, with the globally free blocks as its free blocks. Lemma 3 of the [buddy system proof](/buddy-system/) uses only (T) and (B), so it applies. $\square$

**Theorem.** Run any sequence of calls from the start state. Then:

1. the state is legal after each call, and each call ends;
2. a class never has more locally free blocks than active blocks;
3. when no block is active, LOCAL is empty for every class, GLOBAL$[m] = \{0\}$, and the other GLOBAL lists are empty;
4. with the flush of the page's code, LAZY-MALLOC$(n)$ fails exactly when an eager buddy system with the same active blocks would fail.

*Proof.* (1) is Lemmas 2 and 3 by induction on the number of calls. (2) is (S). (3): $A_k = 0$ for each $k$, so (S) gives $L_k = 0$. By Lemma 4, the globally free blocks are the maximal empty tree blocks, and with no active block the only one is the root. (4): if line L2, L3 or L4 finds a free block of order at least $k$, that block is a tree block that meets no active block, so the eager system, whose free blocks are the maximal empty tree blocks, has a free block of order at least $k$ too. If they find none, the flush frees every local block with GLOBAL-FREE, which keeps the state legal by Lemma 1 and leaves all LOCAL lists empty. By Lemma 4 the free blocks are then exactly those of the eager system, so the second try fails exactly when the eager system fails. $\blacksquare$
