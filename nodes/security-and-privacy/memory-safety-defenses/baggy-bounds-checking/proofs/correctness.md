---
title: Baggy bounds checking refuses exactly the accesses outside the padded block
proves: [correctness, invariant]
status: full
---

**Setting.** The memory has $2^b$ bytes and slots of 16 bytes. The mark bit is a bit $M > 2^b + 8$, a power of two, so every address $a$ used below has $0 \le a < M$ and $a$ with the mark is $a + M$. Slot 0 is reserved, so every allocation has base $B \ge 16$. The program runs ALLOC, ADD, LOAD, STORE and FREE of the main block, and every pointer it uses is a result of ALLOC or ADD.

**Lemma 1 (the table).** After each operation, for every live allocation with base $B$ and padded size $P = 2^e$: $16 \le P$, $B$ is a multiple of $P$, the blocks of live allocations are disjoint, and $T[s] = e$ for every slot $s$ of $[B, B + P)$.

*Proof.* Line L1 gives $e \ge 4$. The buddy allocator in line L2 gives aligned blocks that are disjoint from all blocks in use. Line L3 writes $e$ to every slot of the new block, and these slots belong to no other live allocation. Line L17 writes the default only to the slots of the freed block. No other line writes $T$. $\square$

For a live allocation $(B, e)$ with $P = 2^e$, define the pointer that baggy bounds must hold at offset $o$:

$$f(o) = \begin{cases} B + o & \text{if } 0 \le o < P, \\ (B + o) + M & \text{if } -8 \le o < 0 \text{ or } P \le o < P + 8, \\ \text{none} & \text{otherwise.} \end{cases}$$

**Lemma 2 (arithmetic).** Let the allocation $(B, e)$ be live and let $p = f(o) \ne$ none. Then ADD$(p, k)$ returns $f(o + k)$ if it is not none, and reports a bounds error otherwise.

*Proof.* First we show that lines L6 and L7 give $r = B + o$ and an address $ref$ in $[B, B + P)$.

- If $0 \le o < P$, $p$ has no mark, and line L7 sets $r = ref = B + o$.
- If $P \le o < P + 8$, write $o = P + j$ with $0 \le j < 8$. Since $B$ and $P$ are multiples of 16, $r = B + P + j$ has $r \bmod 16 = j < 8$, the low half, so $ref = r - 8 = B + P - 8 + j$. As $P \ge 16$, this is in $[B + P - 8, B + P) \subseteq [B, B + P)$.
- If $-8 \le o < 0$, write $o = -8 + j$ with $0 \le j < 8$. Then $r \bmod 16 = 8 + j \ge 8$, the high half, so $ref = r + 8 = B + j \in [B, B + 8) \subseteq [B, B + P)$.

The mark is removed correctly because $r < M$. By Lemma 1, line L8 reads $T[ref \gg 4] = e$. Line L9 sets $q = B + o + k$.

Line L10 tests $(ref \oplus q) \gg e = 0$, that is, $\lfloor ref / P \rfloor = \lfloor q / P \rfloor$ for $q \ge 0$. As $B$ is a multiple of $P$ and $ref \in [B, B + P)$, $\lfloor ref / P \rfloor = B / P$, so the test holds exactly when $B \le q < B + P$, that is, $0 \le o + k < P$. Then ADD returns $q = f(o + k)$.

Otherwise line L11 computes $base = B$, again because $ref \in [B, B + P)$ and $B$ is aligned. Line L12 returns $q + M = f(o + k)$ exactly when $-8 \le o + k < P + 8$, and line L13 reports an error in the remaining case, where $f(o + k)$ is none. For $q < 0$ we have $o + k < -B \le -16$, so $f(o + k)$ is none, and both tests fail because of the condition $q \ge 0$. $\square$

**Lemma 3 (invariant).** While allocation $(B, e)$ is live, every pointer derived from it at offset $o$ equals $f(o)$.

*Proof.* By induction on the derivation. ALLOC returns $B = f(0)$ in line L5. ADD keeps the claim by Lemma 2, and a step whose result would be none reports an error and gives no pointer. $\square$

**Theorem.** Let $p$ be derived from a live allocation $(B, e)$ at offset $o$, and let $w \ge 1$. CHECK$(p, w)$ passes exactly when $0 \le o$ and $o + w \le P$, that is, when the $w$ bytes lie in the padded block $[B, B + P)$.

*Proof.* By Lemma 3, $p = f(o)$. If $o < 0$ or $o \ge P$, $p$ is marked and line L14 faults; in both cases the bytes do not lie in the block. Otherwise $p = B + o$ with $0 \le o < P$, line L14 passes, and line L15 reads $T[p \gg 4] = e$ by Lemma 1. As in Lemma 2, $(p \oplus (p + w - 1)) \gg e = 0$ holds exactly when $p + w - 1 < B + P$, that is, $o + w \le P$. $\blacksquare$

**What is not claimed.** The theorem is about the padded block, so an access to bytes $[B + n, B + P)$ of the padding passes. It says nothing about a pointer whose allocation was freed: then line L17 has reset the table and the checks use the default or a new allocation.

**Termination.** Every operation runs a bounded number of lines, plus a loop over the $2^e / 16$ slots of one block and a buddy split or merge of at most $b$ steps.
