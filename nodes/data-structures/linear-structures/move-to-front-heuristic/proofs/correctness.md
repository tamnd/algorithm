---
title: MTF-ACCESS returns the position of the item and moves it to the front
proves: [correctness, termination]
status: full
---

**Statement.** Let $L$ be a singly linked list of $n \ge 1$ nodes with distinct keys $y_1, y_2, \ldots, y_n$ in this order, and let $x = y_p$ for some $p$ with $1 \le p \le n$. Then MTF-ACCESS$(L, x)$ stops, returns $p$, and after the call $L$ holds the keys $y_p, y_1, \ldots, y_{p-1}, y_{p+1}, \ldots, y_n$ in this order. No node is created or freed.

**Setup.** Write $N_1, \ldots, N_n$ for the nodes in list order at the start, so $N_t.key = y_t$, $N_t.next = N_{t+1}$ for $t < n$, $N_n.next = nil$, and $L.head = N_1$. Lines L1 to L3 do not write any pointer field, so these facts hold during the loop.

**Invariant of line L2.** Each time line L2 tests its condition:

> **(S)** $1 \le i \le p$, $cur = N_i$, $prev = N_{i-1}$ when $i \ge 2$ and $prev = nil$ when $i = 1$, and $y_t \ne x$ for each $t$ with $1 \le t < i$.

*Initialization.* Line L1 sets $i = 1$, $cur = L.head = N_1$ and $prev = nil$. The last part of (S) is about an empty range of $t$. Since $p \ge 1$, (S) holds.

*Maintenance.* Assume (S) and that the test succeeds, so $cur.key = y_i \ne x$. Since the keys are distinct and $y_p = x$, we have $i \ne p$, so $i < p \le n$ and $N_i.next = N_{i+1}$ exists. Line L3 sets $prev = N_i$, $cur = N_{i+1}$ and increases $i$ by 1. With the new value of $i$, $1 \le i \le p$, $cur = N_i$, $prev = N_{i-1}$, and $y_t \ne x$ for all $t < i$, because this was known for $t$ below the old $i$ and was just shown for the old $i$. So (S) holds again.

*Termination.* The quantity $p - i$ is a nonnegative integer by (S), and each run of line L3 lowers it by exactly 1. So the loop runs at most $p - 1$ times. When it stops, $cur.key = x$, so $y_i = x$ and, the keys being distinct, $i = p$. Then $cur = N_p$, and $prev = N_{p-1}$ or $nil$ when $p = 1$.

**The move.** If $p = 1$, then $prev = nil$, lines L5 to L7 do not run, and $L$ is unchanged, which is the claimed order $y_1, \ldots, y_n$. If $p \ge 2$, then $prev = N_{p-1}$ and:

1. Line L5 sets $N_{p-1}.next = N_p.next$, which is $N_{p+1}$, or $nil$ when $p = n$. Now the chain from $L.head = N_1$ is $N_1, \ldots, N_{p-1}, N_{p+1}, \ldots, N_n$, and $N_p$ is outside it.
2. Line L6 sets $N_p.next = L.head = N_1$. The chain from $N_p$ is $N_p, N_1, \ldots, N_{p-1}, N_{p+1}, \ldots, N_n$. Line L6 reads $L.head$ before line L7 changes it.
3. Line L7 sets $L.head = N_p$.

So $L$ holds $y_p, y_1, \ldots, y_{p-1}, y_{p+1}, \ldots, y_n$, the chain ends in $nil$ after $N_n$ or $N_{n-1}$ (no cycle, since each node appears once), and the nodes are the same $n$ nodes. Line L8 returns $i = p$. $\blacksquare$
