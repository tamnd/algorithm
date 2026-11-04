---
title: The external queue returns items in FIFO order and makes at most 2n/B block transfers
proves: [correctness, complexity]
status: full
---

We use the pseudocode of the page with block size $B \ge 1$. The state is the head $H$, the disk blocks $D_1, \ldots, D_k$ and the tail $T$. Let $\sigma = H \cdot D_1 \cdots D_k \cdot T$.

**Invariant.** At the start and after each operation: (I1) $\sigma$ is the abstract queue, from the front to the back; (I2) each $D_j$ has exactly $B$ items; (I3) $|H| \le B$ and $|T| < B$.

*Base.* For the empty queue all three parts are empty, so the invariant holds.

*Enqueue.* Line L1 appends $x$ to $T$ and so to $\sigma$, which is now the old queue followed by $x$. Now $|T| \le B$. If $|T| = B$, lines L3 and L4 append $T$ as a block $D_{k+1}$ and empty $T$. This does not change $\sigma$, the new block has $B$ items, and $|T| = 0$. Otherwise $|T| < B$ already. $H$ does not change.

*Dequeue.* If $H$ is not empty, only line L10 runs: it removes the first item of $H$, which is the first item of $\sigma$. If $H$ is empty and $k \ge 1$, line L7 makes $H = D_1$ and removes $D_1$ from the disk part, so $\sigma$ does not change and $|H| = B$. If $H$ is empty and $k = 0$, then $\sigma = T$. If $T$ is empty the queue is empty, and line L8 reports the error. Otherwise line L9 moves $T$ into $H$, which does not change $\sigma$, and gives $|H| < B$ and $|T| = 0$. In both cases $H$ is now not empty, and line L10 removes and returns the first item of $\sigma$, the front of the queue. (I2) holds because no block was written, and (I3) holds because $H$ has at most $B$ items and only shrinks in line L10.

By induction the invariant holds after every operation, and each dequeue returns the oldest item that is still in the queue. $\square$

**Theorem (I/O bound).** Starting from the empty queue, a sequence with $e$ enqueues and any number of dequeues, $n$ operations in all, makes at most $\lfloor e/B \rfloor$ writes and at most as many reads, so at most $2\lfloor n/B \rfloor$ block transfers.

*Proof.* Writes. Follow one item $x$. It enters $T$ in its enqueue (line L1). It leaves $T$ only through line L3, into a disk block, or through line L9, into $H$. From a disk block it goes only to $H$ (line L7), and from $H$ only out of the queue (line L10). So $x$ is in at most one written block. Each write contains exactly $B$ items, all different, so the number of writes $w$ satisfies $wB \le e$, and $w \le \lfloor e/B \rfloor$.

Reads. Each read in line L7 removes one block from the disk part, and blocks enter the disk part only by writes. So the number of reads is at most $w$.

Hence the transfers number at most $2w \le 2\lfloor e/B \rfloor \le 2\lfloor n/B \rfloor$. $\blacksquare$
