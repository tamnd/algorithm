---
title: Block nested-loop join returns the join as a multiset and does M + ceil(M/(B - 2)) N reads
proves: [correctness, termination, io.worst]
status: full
---

We use the line numbers of the pseudocode. Let $R$ be stored as pages $P_1, \ldots, P_M$ and $S$ as pages $Q_1, \ldots, Q_N$, and let $c = B - 2 \ge 1$. We treat each stored tuple as a distinct occurrence. The join $R \bowtie S$ on $r.a = s.b$ is the multiset with one copy of $r \cdot s$ for each pair of occurrences $(r, s)$ with $r.a = s.b$.

**Lemma 1 (blocks).** Line L2 visits the blocks $K_j = \{P_{(j-1)c + 1}, \ldots, P_{\min(jc, M)}\}$ for $j = 1, \ldots, \lceil M/c \rceil$. Each page of $R$, and so each occurrence of $R$, lies in exactly one block.

*Proof.* The blocks are consecutive ranges of $c$ page indices, the last one possibly shorter, starting at $1$ and ending at $M$. Consecutive ranges with these ends partition $\{1, \ldots, M\}$. $\square$

**Lemma 2 (the table).** After line L4 for block $K_j$, for each value $v$, the tuples of $H$ with attribute $a$ equal to $v$ are exactly the occurrences of $K_j$ with $r.a = v$, each one once.

*Proof.* Line L4 inserts each occurrence of the block once, keyed by $r.a$, and keeps all tuples with the same key in its bucket. A lookup of $v$ returns the tuples of the bucket of $v$ whose key equals $v$. $\square$

**Theorem 1 (correctness).** BLOCK-NESTED-LOOP-JOIN returns a list whose multiset of elements is $R \bowtie S$.

*Proof.* Fix a pair of occurrences $(r, s)$. By Lemma 1, $r$ is in exactly one block $K_j$. In the iteration for $K_j$, lines L5 and L7 meet $s$ exactly once, because the pages of $S$ partition its occurrences. By Lemma 2, line L8 at that moment appends $r \cdot s$ exactly once if $r.a = s.b$ and not at all otherwise. In the iteration for another block $K_{j'}$, $r$ is not in $H$, so line L8 does not append $r \cdot s$. Each element that line L8 appends comes from some pair $(r, s)$ with $r$ in the current block, so there are no other elements. Hence the number of copies of each tuple $t$ in $out$ is the number of matching pairs $(r, s)$ with $r \cdot s = t$. All loops are finite, so the algorithm stops. For a general condition $\theta$, the same argument holds with Lemma 2 replaced by a direct test of each $r$ of the block. $\blacksquare$

**Theorem 2 (I/O count).** The algorithm does exactly $M + \lceil M/(B-2) \rceil N$ page reads and writes no page other than the output.

*Proof.* Reads happen only at lines L3 and L6. By Lemma 1, line L3 reads each page of $R$ once, which is $M$ reads. Line L2 runs $\lceil M/c \rceil$ times, and line L6 reads each of the $N$ pages of $S$ once in each run, which is $\lceil M/c \rceil N$ reads. Memory holds the $c$ pages of the block, one page of $S$ and one output page, so $c + 2 = B$ frames suffice and nothing else is written. $\blacksquare$
