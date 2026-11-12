---
title: The free-list operations keep the list consistent and in its order
proves: [correctness]
status: full
---

Write the list as a sequence $L = (b_0, \ldots, b_{k-1})$ of distinct free blocks. The representation is *consistent* with $L$ when $head = b_0$ and $tail = b_{k-1}$ (both NIL if $k = 0$), $NEXT(b_i) = b_{i+1}$ and $PREV(b_i) = b_{i-1}$, where $b_{-1} = b_k = $ NIL. The *order* condition is: for addr, $b_0 < b_1 < \cdots < b_{k-1}$; for lifo and fifo there is no condition on addresses, only the position rules below.

The link words of a free block $a$ are $a + 1$ and $a + 2$. Since a free block has at least $MIN = 4$ words and blocks do not overlap, the link words of different free blocks are different words, and they are not header or footer words. So a write to the links of one block changes no other block's links or tags.

**Lemma 1 (BETWEEN).** If the representation is consistent with $L$, $a$ is a free block not in $L$, and $p, q$ are adjacent in $L$ (that is, $q$ follows $p$, with $p = $ NIL meaning the front and $q = $ NIL meaning the back), then after lines L1 to L3 the representation is consistent with $L$ with $a$ inserted between $p$ and $q$.

*Proof.* Line L1 sets the links of $a$ to $q$ and $p$. Line L2 sets $NEXT(p) = a$, or $head = a$ when $a$ is the new front. Line L3 sets $PREV(q) = a$, or $tail = a$ when $a$ is the new back. No other link changes, and these are exactly the links that differ between the old and the new sequence. $\square$

**Lemma 2 (LINK).** LINK($a$) inserts $a$ at the front for lifo, at the back for fifo, and before the first block of higher address for addr. In each case the order condition still holds.

*Proof.* For lifo, line L4 calls BETWEEN with $p = $ NIL and $q = head$, the front. For fifo, line L5 uses $p = tail$ and $q = $ NIL, the back. For addr, lines L6 and L7 walk from the head while the block $q$ has a lower address than $a$, so $q$ is the first block of higher address, or NIL. Line L8 inserts $a$ before $q$, after $PREV(q)$ or after the tail. All blocks before $a$ are lower and all blocks after it are higher, so the list stays sorted. $\square$

**Lemma 3 (UNLINK).** If the representation is consistent with $L$ and $a = b_i$, lines L9 to L11 make it consistent with $L$ without $b_i$.

*Proof.* Line L9 reads $p = b_{i-1}$ and $q = b_{i+1}$. Line L10 sets $NEXT(p) = q$, or $head = q$ if $i = 0$. Line L11 sets $PREV(q) = p$, or $tail = p$ if $i = k - 1$. These are the only links that differ between the two sequences. Removing an element keeps a sorted list sorted. $\square$

**Lemma 4 (REPLACE).** If $old = b_i$ and $new$ is a free block that is not in $L$, lines L12 and L13 make the representation consistent with $L$ where $b_i$ is replaced by $new$. If $new$ lies inside $old$'s words, as the remainder of a split does, the addr order still holds.

*Proof.* Line L12 reads the neighbours $b_{i-1}$ and $b_{i+1}$ of $old$. These stay adjacent in the list without $old$, and BETWEEN puts $new$ between them by Lemma 1; the links of $old$ are not used again. For a split, $old < new < old + SIZE(old)$, and no other free block starts in that range, so $b_{i-1} < new < b_{i+1}$. $\square$

**Theorem.** In the heap of the page, after any sequence of malloc and free calls, the free list is consistent with a sequence that holds each free block exactly once, and that sequence satisfies the order condition of the chosen order.

*Proof.* By induction on the calls. At the start the only block is free and LINK puts it on the empty list. A malloc either replaces the chosen block by its remainder (Lemma 4) or unlinks it (Lemma 3), and the chosen block is the one that becomes used. A free unlinks each free neighbour that is merged (Lemma 3), and then links the merged block (Lemma 2); the merged block is the only new free block, and the absorbed neighbours are no longer blocks. In each case the list holds exactly the free blocks afterwards, and its order condition holds. $\square$
