---
title: Segregated fits fails only when no free block is large enough, picks a block of the least fitting class, and keeps free blocks maximal
proves: [correctness, termination]
status: full
---

**Setting.** The heap is $[0, h)$. A state is a family of blocks, each an interval $[a, a + s)$ with $s \ge 1$ and a free bit, and the lists LIST$[0..k-1]$, with $k = \lfloor \lg h \rfloor + 1$. Write $\text{cls}(s) = \lfloor \lg s \rfloor$, so $2^{\text{cls}(s)} \le s < 2^{\text{cls}(s) + 1}$. The state is *legal* when:

- **(T)** the blocks tile $[0, h)$ with no gap and no overlap;
- **(C)** no two free blocks are neighbours, that is, no free block ends where another free block starts;
- **(L)** each free block is in LIST$[\text{cls}(s)]$ for its size $s$, each list entry is a free block, and no block is in two lists.

**Lemma 1 (the search).** In a legal state, let $n \ge 1$ and $i = \lfloor \lg n \rfloor$. Lines L1 to L4 return FAIL exactly when no free block has at least $n$ words. Otherwise they find a free block $b$ with $\text{size}(b) \ge n$, and $\text{cls}(\text{size}(b))$ is the least class that holds a free block of at least $n$ words.

*Proof.* A free block with $s \ge n$ words has $\text{cls}(s) \ge \text{cls}(n) = i$, because $\lfloor \lg \cdot \rfloor$ does not decrease. Let $c^*$ be the least class that holds a free block of at least $n$ words, if one exists.

If $c^* = i$, line L2 scans LIST$[i]$ and, by (L), finds a free block of class $i$ with at least $n$ words. Its class is $i = c^*$.

If $c^* > i$, or no fitting block exists, then no block of LIST$[i]$ fits, and line L2 finds nothing. Line L3 takes the least $j > i$ with LIST$[j]$ not empty. Every block of class $j > i$ has at least $2^j \ge 2^{i+1} > n$ words, because $n < 2^{i+1}$. So every non-empty class above $i$ holds a fitting block, and the least such class is $c^*$. Thus line L3 finds $j = c^*$ when $c^*$ exists, and line L4 returns a block of class $c^*$ with at least $n$ words. When no fitting block exists, every class above $i$ is empty, because each of its blocks would fit, and line L3 returns FAIL. $\square$

**Lemma 2 (malloc keeps a legal state).** If the state is legal and SEG-MALLOC$(n)$ returns $b$, the state after it is legal, and $[b, b + n)$ is an allocated block that meets no other allocated block.

*Proof.* Line L5 removes $b$ from its list. If $\text{size}(b) > n$, line L6 replaces the block with $[b, b + n)$, allocated, and the rest $R = [b + n, b + \text{size}(b))$, free, in the list of its class. The two parts tile the old block, so (T) holds. For (C), the only new free block is $R$. Its left neighbour is the allocated block $[b, b + n)$. Its right neighbour, if any, was the right neighbour of the free block $b$, which by (C) was not free. So $R$ has no free neighbour. Removing the free block $b$ from the free set cannot break (C). (L) holds because $b$ left its list and $R$ joined the list of its class. Since $b$ was free and the blocks tile the heap, $[b, b + n)$ meets no other allocated block. $\square$

**Lemma 3 (free keeps a legal state).** If the state is legal and $p$ is an allocated block, the state after SEG-FREE$(p)$ is legal.

*Proof.* Line L8 marks $p$ free. Now $p$ may have free neighbours, but the other free blocks still have no free neighbour other than $p$. Line L9 merges the right neighbour $q$ into $p$ if $q$ is free: $q$ leaves its list, and the union of the two intervals is one interval, so (T) holds. Line L10 does the same with the left neighbour. After these lines, the merged block $M$ has no free neighbour. Its right neighbour is the right neighbour of $q$, or of $p$ if $q$ was not free; in the first case it is not free by (C) for $q$, and in the second case it is the block that line L9 checked. The same holds on the left. No other pair of free blocks changed. So (C) holds. Line L11 puts $M$ in the list of its class, and the blocks that merged left their lists at lines L9 and L10, so (L) holds. $\square$

**Lemma 4 (termination and cost).** Line L2 looks at most at the length of LIST$[i]$ blocks, line L3 at most at $k$ list heads, and SEG-FREE does a constant number of steps besides the list operations.

*Proof.* Direct from the lines. $\square$

**Theorem.** Run any sequence of calls from the state with one free block $[0, h)$. Then:

1. the state is legal after each call, and each call ends;
2. SEG-MALLOC$(n)$ returns FAIL exactly when no free block has at least $n$ words;
3. a returned block has exactly $n$ words, does not meet any other allocated block, and was cut from a free block of the least class that holds a fitting block;
4. the total size of the free blocks and the allocated blocks is $h$;
5. when no block is allocated, the only free block is $[0, h)$.

*Proof.* The start state is legal: one free block in LIST$[k - 1]$, because $\lfloor \lg h \rfloor = k - 1$. (1) follows from Lemmas 2, 3 and 4 by induction on the number of calls, with the FAIL case changing nothing. (2) and (3) are Lemmas 1 and 2. (4) is (T). (5): with no allocated block, all blocks are free, and by (C) no two of them are neighbours. Blocks that tile $[0, h)$ and are pairwise not neighbours can only be one block. $\blacksquare$
