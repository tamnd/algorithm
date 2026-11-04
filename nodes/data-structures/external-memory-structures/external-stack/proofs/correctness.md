---
title: The external stack returns the right items and makes at most n/B block transfers
proves: [correctness, complexity]
status: full
---

We use the pseudocode of the page with block size $B \ge 1$. The state is the list of disk blocks $D[0], \ldots, D[k-1]$ and the buffer $buf$. Let $\sigma = D[0] \cdot D[1] \cdots D[k-1] \cdot buf$ be their concatenation.

**Invariant.** At the start and after each operation: (I1) $\sigma$ is the abstract stack, from the bottom to the top; (I2) each $D[j]$ has exactly $B$ items; (I3) $|buf| \le 2B$.

*Base.* The empty stack has $k = 0$ and $buf$ empty, so $\sigma$ is empty and (I2) and (I3) hold.

*Push.* If $|buf| = 2B$, lines L2 and L3 append the first $B$ items of $buf$ to the disk part as a new block and remove them from $buf$. The concatenation $\sigma$ does not change, the new block has $B$ items, and $|buf| = B$. Line L4 appends $x$ to $buf$, so $\sigma$ becomes the old stack followed by $x$, which is the new stack. Before line L4, $|buf| \le 2B - 1$: either it was below $2B$, or it is now $B \le 2B - 1$. So $|buf| \le 2B$ after it.

*Pop.* If the abstract stack is empty, $\sigma$ is empty, so $buf$ is empty and $k = 0$, and line L6 reports the error. Otherwise, if $buf$ is empty, then $k > 0$, and line L7 moves the last block into $buf$, which does not change $\sigma$ and gives $|buf| = B \ge 1$. Line L8 removes the last item of $buf$, which is the last item of $\sigma$, the top of the stack. (I1) holds, and (I2) and (I3) hold because no block was written and $buf$ only became smaller or equal to $B$.

So by induction the invariant holds after every operation, and each pop returns the top of the stack. $\square$

**Theorem (I/O bound).** Starting from the empty stack, any sequence of $n$ pushes and pops makes at most $\lfloor n/B \rfloor$ block transfers.

*Proof.* Each operation makes at most one transfer: a push writes only if $|buf| = 2B$, and a pop reads only if $buf$ is empty, and these are not both true in one operation. Let the transfers happen in the operations $o_1 < o_2 < \cdots < o_t$ of the sequence, numbered from 1.

The first transfer is a write, since a read needs $k > 0$, and $k$ grows only by writes. A write needs $|buf| = 2B$, and each operation before it is a push or a pop without transfer, which changes $|buf|$ by one, starting from 0. So at least $2B$ operations come before it, and $o_1 \ge 2B + 1$.

After the transfer in $o_j$, and before the change of line L4 or L8, $|buf| = B$. So at the end of $o_j$, $|buf|$ is $B + 1$ after a write or $B - 1$ after a read. The transfer in $o_{j+1}$ needs $|buf| = 2B$ or $|buf| = 0$ at the start of $o_{j+1}$. The operations $o_j + 1, \ldots, o_{j+1} - 1$ make no transfer, so each changes $|buf|$ by exactly one. From $B + 1$ or $B - 1$ to $2B$ or 0 needs at least $B - 1$ such steps, so $o_{j+1} - o_j \ge B$.

Hence $o_t \ge 2B + 1 + (t - 1)B > tB$, and since $o_t \le n$, $t < n/B$ when $t \ge 1$. So $t \le \lfloor n/B \rfloor$. $\blacksquare$
