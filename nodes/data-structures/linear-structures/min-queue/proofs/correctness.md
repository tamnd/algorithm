---
title: The two-stack queue with minimum is a FIFO queue and returns its least item
proves: [correctness, amortized]
status: full
---

**Setting.** The structure has two [stacks with minimum](/min-stack/), $In$ and $Out$. We use only their laws: PUSH adds an item at the top, POP removes and returns the top item, and MIN returns the least item of a non-empty stack. Write $In = \langle a_1, \ldots, a_p \rangle$ and $Out = \langle b_1, \ldots, b_r \rangle$, each from the bottom to the top.

**Invariant (Q).** The queue, from the front to the back, is

$$\langle b_r, b_{r-1}, \ldots, b_1, a_1, a_2, \ldots, a_p \rangle.$$

So the front is the top of $Out$ when $Out$ is not empty, and the back is the top of $In$.

At the start both stacks are empty and the queue is empty, so (Q) holds.

**ENQUEUE$(Q, x)$.** Line L1 pushes $x$ on $In$, so $a_{p+1} = x$. By (Q) the queue becomes $\langle b_r, \ldots, b_1, a_1, \ldots, a_p, x \rangle$, which is the old queue with $x$ at the back.

**DEQUEUE$(Q)$, the queue not empty.**

*Case $r \ge 1$.* Line L2 skips the transfer. Line L5 pops $b_r$ from $Out$ and returns it. By (Q) $b_r$ is the front item, and the rest $\langle b_{r-1}, \ldots, b_1, a_1, \ldots, a_p \rangle$ is the old queue without its front.

*Case $r = 0$.* Then $p \ge 1$, because the queue is not empty. The loop of lines L3 and L4 keeps this loop invariant at its test: for some $0 \le t \le p$, $In = \langle a_1, \ldots, a_{p-t} \rangle$ and $Out = \langle a_p, a_{p-1}, \ldots, a_{p-t+1} \rangle$ from the bottom to the top. It holds for $t = 0$. One iteration pops $a_{p-t}$ from $In$ and pushes it on $Out$, which gives the invariant for $t + 1$. The value $t$ grows by exactly 1 in each iteration, and the loop stops when $In$ is empty, at $t = p$. Then $Out = \langle a_p, \ldots, a_1 \rangle$ with $a_1$ at the top, and $In$ is empty. In the notation of (Q), $r = p$ and $b_j = a_{p+1-j}$, so the queue read by (Q) is $\langle a_1, \ldots, a_p \rangle$, which is unchanged. Line L5 then pops $a_1$, the front item, as in the first case.

**MIN$(Q)$, the queue not empty.** The set of items of the queue is the union of the items of $In$ and of $Out$, by (Q). If $In$ is empty, line L6 returns the least item of $Out$, which is the least item of the queue. If $Out$ is empty, line L7 returns the least item of $In$. Otherwise line L8 returns the smaller of the two minima, which is the least item of the union. Nothing changes.

**Amortized cost.** Count one unit for each PUSH and each POP on $In$ or $Out$; each costs $O(1)$ on a stack with minimum. Let $\Phi = 2p$, twice the size of $In$. Then $\Phi \ge 0$ and $\Phi = 0$ at the start.

- ENQUEUE costs 1 and raises $\Phi$ by 2: amortized cost 3.
- DEQUEUE without a transfer costs 1 and does not change $\Phi$: amortized cost 1.
- DEQUEUE with a transfer of $p$ items costs $2p + 1$, and $\Phi$ drops from $2p$ to 0: amortized cost 1.
- MIN costs at most two MIN calls on stacks, and does not change $\Phi$: amortized cost $O(1)$.

The sum of the potential differences telescopes, so for any sequence of $m$ operations from the start, the total cost is at most the sum of the amortized costs minus the final potential, which is at most $3m$ stack operations. $\blacksquare$
