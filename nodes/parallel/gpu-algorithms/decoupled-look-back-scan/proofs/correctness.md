---
title: The decoupled look-back scan is correct, cannot deadlock, and looks back at most p tiles
proves: [correctness]
status: full
---

**Setting.** The input is $A[0 \ldots n-1]$ with an associative operator $\oplus$, which need not be commutative. The array is cut into $t = \lceil n / b \rceil$ tiles of $b$ items; the last tile can be shorter. Write $T_g$ for the reduction of tile $g$ and $I_g = T_0 \oplus \cdots \oplus T_g$ for the inclusive prefix through tile $g$. Each tile $g$ has a descriptor that holds a flag in $\{X, A, P\}$ and a value. All descriptors start as $X$. The code is LOOK-BACK-SCAN-BLOCK, lines L1 to L16, run once by every thread block.

**Hypotheses.**

1. *Atomic publication.* PUBLISH writes the flag and the value of a descriptor as one indivisible store, and READ reads both as one indivisible load. (On a GPU this is the fence-free form with flag and value packed in one word, or a store of the value, a memory fence, and then a store of the flag.)
2. *Dynamic index.* Line L1 takes the tile index from a global counter with an atomic increment that starts at 0. Each block takes its index after the hardware has made it resident.
3. *Forward progress.* At most $p \ge 1$ blocks are resident at a time. A resident block that can execute an instruction is not starved forever, and a block that finishes frees its slot for a waiting block.

**Lemma 1 (descriptor values).** At all times, if descriptor $g$ holds $(A, v)$ then $v = T_g$, and if it holds $(P, v)$ then $v = I_g$. The flag of a descriptor only moves from $X$ to $A$ to $P$, or from $X$ to $P$, and the value written with a flag never changes later.

*Proof.* By hypothesis 2, the indices $0, 1, \ldots, t-1$ go to distinct blocks, so only the block of tile $g$ writes descriptor $g$. That block writes it at most twice: on line L5 with $(P, T_0)$ when $g = 0$, or on line L7 with $(A, T_g)$ and later on line L15 with $(P, \cdot)$. So the flag order holds, and the claim for $A$ holds. For $P$ we use induction on the time of the write. Line L5 writes $I_0 = T_0$. Consider the write on line L15 by tile $g \ge 1$, and assume the claim for all earlier writes. Let the loop of lines L9 to L14 read, in order, descriptors $g-1, g-2, \ldots, k$, and stop at $k$ with flag $P$. By the induction hypothesis and hypothesis 1, each read of a descriptor $j$ with $k < j < g$ returned $(A, T_j)$, and the read of $k$ returned $(P, I_k)$. Line L12 puts each new value on the left. So after the loop,
$$excl = I_k \oplus T_{k+1} \oplus \cdots \oplus T_{g-1} = T_0 \oplus \cdots \oplus T_{g-1} = I_{g-1},$$
by associativity. Line L15 writes $I_{g-1} \oplus T_g = I_g$. $\square$

**Lemma 2 (output).** Every block that finishes writes the correct inclusive scan of its tile.

*Proof.* Tile 0 has $excl$ empty and writes the scan of $A[0 \ldots b-1]$. For $g \ge 1$, the proof of Lemma 1 shows that $excl = I_{g-1}$, the reduction of all items before the tile. Line L16 writes, for each item $A[i]$ of the tile, $I_{g-1} \oplus A[gb] \oplus \cdots \oplus A[i] = A[0] \oplus \cdots \oplus A[i]$. $\square$

**Lemma 3 (no deadlock).** Under hypotheses 2 and 3 every block finishes.

*Proof.* Suppose not, and look at a time after which no more blocks finish. Let $g$ be the smallest tile index that is taken but not finished at that time. Every tile $j < g$ is finished, so it has written its $P$ descriptor before it finished. Tile $g$ waits only on line L11, and only for a descriptor $j < g$ with flag $X$. No such descriptor exists, so tile $g$ never waits, and every other step of its code is a finite amount of work. By hypothesis 3 it finishes. This is a contradiction, unless no tile is taken but unfinished. In that case all resident blocks have finished, so by hypothesis 3 new blocks become resident and take new indices, until all $t$ indices are taken and finished. $\square$

The proof uses the fact that the waiting graph points only to smaller indices that are already *taken*. Hypothesis 2 gives this. If a block used its hardware block index as its tile index, a resident block $g$ could wait for tile $g-1$ whose block is not yet resident, while all $p$ slots hold blocks that wait in the same way. The hardware does not promise to dispatch blocks in index order, so this deadlock can occur. The tests show it in the simulator.

**Lemma 4 (bounded look-back).** Tile $g$ reads at most $\min(g, p)$ descriptors in its look-back.

*Proof.* When tile $g$ took its index on line L1, every index $j < g$ was already taken, by a block that was then resident or finished. Tile $g$ itself held one of the $p$ slots, so at most $p - 1$ of the tiles $g-1, \ldots, g-p$ were held by resident blocks. If $g \ge p$, at least one of these $p$ tiles had finished, and so had published $P$. Flags never move back (Lemma 1), so the look-back stops at the latest at that tile, after at most $p$ reads. If $g < p$, it stops at tile 0 or earlier, after at most $g$ reads. $\square$

**Theorem.** Under hypotheses 1 to 3, the decoupled look-back scan terminates and writes the inclusive scan $A[0] \oplus \cdots \oplus A[i]$ at every index $i$. It reads each input item once and writes each output item once, publishes $2t - 1$ descriptors, and reads at most $p$ descriptors per tile, not counting failed polls.

*Proof.* Lemma 3 gives termination and Lemma 2 the output. Line L2 is the only read of $A$ and line L16 the only write of the output. Tile 0 publishes once and every other tile twice, which gives $2t - 1$. Lemma 4 bounds the reads. $\blacksquare$

With $b$ much larger than $p$, the descriptor traffic $O(t p) = O(np/b)$ is small next to the $2n$ item transfers. A reduce-then-scan that reads the input twice moves about $3n$ items.
