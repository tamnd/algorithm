---
title: Deficit round robin is fair in bytes over every interval and costs O(1) per packet
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $M$ be the largest packet size. A *turn* of flow $i$ starts when line L5 adds $Q_i$ to $DC_i$, and ends at line L8 or line L10. A *point* is a moment between two calls of DEQUEUE, or between the steps of one call. The ActiveList keeps its flows in a cyclic order: line L10 moves the head to the tail, and line L2 adds new flows at the tail.

**Lemma 1 (the counter).** While flow $i$ is in the ActiveList, $DC_i \ge 0$. Outside its turns, $DC_i < M$. During its turn, $DC_i < Q_i + M$.

*Proof.* Line L2 sets $DC_i = 0$ when $i$ joins the list. Line L7 subtracts the size of a packet only when line L6 found it at most $DC_i$, so $DC_i$ stays at least 0. A turn of a flow that stays in the list ends at line L10, where the head packet did not fit: $DC_i < \text{size} \le M$. So outside its turns $DC_i < M$, which also holds at 0 before the first turn. A turn starts from a value below $M$ and adds $Q_i$, and line L7 only lowers it, so $DC_i < Q_i + M$ during the turn. $\square$

**Lemma 2 (bytes and turns).** Let $n_i(t)$ be the number of turns of flow $i$ started since it last joined the list, up to point $t$. Then the bytes $s_i(t_1, t_2)$ that flow $i$ sends between two points $t_1 \le t_2$ at which it is in the list, and with no exit from the list in between, satisfy

$$s_i(t_1, t_2) = Q_i\,(n_i(t_2) - n_i(t_1)) - DC_i(t_2) + DC_i(t_1).$$

*Proof.* Between joins, $DC_i$ changes only by $+Q_i$ at line L5 and by $-\text{size}$ at line L7. $\square$

**Theorem 3 (fairness over any interval).** Let flows $i$ and $j$ both stay in the ActiveList between two points $t_1 \le t_2$. Then

$$\left| \frac{s_i(t_1, t_2)}{Q_i} - \frac{s_j(t_1, t_2)}{Q_j} \right| < 1 + \frac{M}{Q_i} + \frac{M}{Q_j}.$$

*Proof.* Let $t_0 \le t_1$ be the last point at which $i$ or $j$ joined the list. From $t_0$ to $t_2$ both are in the list. Their cyclic order does not change, since line L10 only rotates the list and line L8 removes flows other than $i$ and $j$. So their turns alternate: between two turns of $i$ there is exactly one turn of $j$, and the other way round. Let $k(t) = n_i(t) - n_j(t)$. Each turn of $i$ adds 1 to $k$ and each turn of $j$ subtracts 1, and they alternate, so there is an integer $c$ with $k(t) \in \{c, c+1\}$ for all points $t \in [t_0, t_2]$, where $k = c + 1$ just after a turn of $i$ starts and $k = c$ just after a turn of $j$ starts. Let

$$D(t) = k(t) - \frac{DC_i(t)}{Q_i} + \frac{DC_j(t)}{Q_j}.$$

By Lemma 2, $s_i(t_1, t_2)/Q_i - s_j(t_1, t_2)/Q_j = D(t_2) - D(t_1)$. We show that $c - M/Q_i < D(t) < c + 1 + M/Q_j$ for every point $t$ in $[t_0, t_2]$, which proves the claim. At most one of the two flows is in its turn at $t$.

- *Flow $i$ is in its turn.* Then $k = c + 1$. By Lemma 1, $0 \le DC_i < Q_i + M$ and $0 \le DC_j < M$. So $D > c + 1 - 1 - M/Q_i = c - M/Q_i$ and $D < c + 1 + M/Q_j$.
- *Flow $j$ is in its turn.* Then $k = c$, $0 \le DC_i < M$ and $0 \le DC_j < Q_j + M$. So $D > c - M/Q_i$ and $D < c + 1 + M/Q_j$.
- *Neither is in its turn.* Then $k \in \{c, c + 1\}$, $0 \le DC_i < M$ and $0 \le DC_j < M$. So $D > c - M/Q_i$ and $D < c + 1 + M/Q_j$.

In each case the bound holds. $\blacksquare$

With equal quanta $Q_i = Q_j = Q$, multiply by $Q$: $|s_i - s_j| < Q + 2M$. This is the fairness measure $2\,Max + Q$ of Shreedhar and Varghese.

**Corollary 4 (long-run shares).** If flow $i$ stays in the list for $K$ turns, it sends between $K Q_i - M$ and $K Q_i$ bytes plus what it sends in a turn in progress. Hence flows that stay backlogged get bytes in the ratio of their quanta, with an error that does not grow with time.

*Proof.* Apply Lemma 2 from the join to the end of the $K$-th turn: $s_i = K Q_i - DC_i$ with $0 \le DC_i < M$ by Lemma 1, unless the flow left at the end of that turn, in which case $DC_i$ was reset after its last packet and $s_i \le K Q_i$. $\square$

**Theorem 5 (cost).** If $Q_i \ge M$ for every flow, every turn sends at least one packet, and $n$ packets cost $O(n)$ time.

*Proof.* At the start of a turn of flow $i$, $DC_i \ge Q_i \ge M$ after line L5, by Lemma 1. Flow $i$ is in the list, so its queue is not empty, and its head packet has size at most $M \le DC_i$. So line L6 succeeds at least once in the turn. Hence the number of turns is at most the number of packets sent. Each pass of the loop at lines L3 to L10 either sends a packet or ends a turn, and costs $O(1)$, so the total work is $O(n)$. $\square$

**Lemma 6 (each packet is sent once, in FIFO order per flow).** Line L7 removes the head of a queue and line L9 returns it. Packets leave a queue only there, and only from the head. $\square$
