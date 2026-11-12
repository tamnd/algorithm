---
title: Fair queueing finishes each packet within one maximum packet time of bit-by-bit round robin
proves: [correctness]
status: full
---

We use the pseudocode of the page. The *ideal* is the fluid limit of bit-by-bit round robin: at each time, every flow that still has bits in the ideal is served at rate $r / N(t)$, where $N(t)$ is the number of such flows, and the bits of one flow are served in FIFO order. Both the ideal and FQ see the same arrivals. Write $L_p$ for the size of packet $p$, $a_p$ for its arrival time, $F_p$ for its finish number, $d_p$ for its finish time in the ideal and $\hat d_p$ for its finish time under FQ. Let $L_{max} = \max_p L_p$.

**Lemma 1 (the round number counts bits per flow).** Let $R(t)$ be the round number that lines L5 to L7 compute. A flow has bits in the ideal at time $t$ exactly when $F_{last} > R(t)$, and packet $p$ is served in the ideal while $R$ runs from $F_p - L_p$ to $F_p$. In particular $d_p$ is the first time at which $R(t) = F_p$.

*Proof.* Lines L5 and L6 make $R$ continuous and piecewise linear, with slope $r / N_{active}$ while $N_{active} > 0$ and slope 0 otherwise, where $N_{active}$ counts the flows with $F_{last} > R$. We prove the claims by induction over the events (arrivals and the points of line L5 where a flow becomes inactive), in time order.

Assume that at some time the set of active flows equals the set of flows with bits in the ideal, and that each such flow $i$ has exactly $F_{last}[i] - R$ bits left in the ideal. Until the next event, both sets stay the same, and each of these flows is served at rate $r/N$ in the ideal while $R$ grows at rate $r/N$. So the number of bits left falls exactly as fast as $R$ grows, and the invariant holds. At a point of line L5, $R$ reaches $F_{last}[i]$ for some flows; exactly then those flows have no bits left in the ideal, and line L5 makes them inactive. At an arrival of a packet of $L_p$ bits of flow $i$: if $i$ is active, it has $F_{last}[i] - R$ bits left, and line L2 gives $F_p = F_{last}[i] + L_p$, so it now has $F_p - R$ bits left. If $i$ is not active, it has no bits left, and $F_p = R + L_p$, so again it has $F_p - R$ bits left. Line L3 makes it active. At the start, no flow is active and none has bits. So the invariant holds at all times.

Now fix a packet $p$ of flow $i$. Just after its arrival, flow $i$ has $F_p - R$ bits left in the ideal, and the last $L_p$ of them belong to $p$. A later packet of flow $i$ adds its size both to $F_{last}[i]$ and to the bits left, so at any later time the bits left that belong to $p$ or to earlier packets of flow $i$ are $F_p - R$, as long as this is positive. The ideal serves a flow in FIFO order, so it serves $p$ while this amount falls from $L_p$ to 0, that is, while $R$ runs from $F_p - L_p$ to $F_p$. The flow stays active until $R$ reaches $F_p$, and while some flow is active, $R$ strictly increases. So $d_p$ is the first time at which $R(t) = F_p$. $\square$

**Corollary 2 (order).** If $F_p < F_q$ then $d_p \le d_q$. Equivalently, $d_p > d_q$ implies $F_p > F_q$.

*Proof.* $R$ is nondecreasing, so the first time it reaches $F_p$ is not after the first time it reaches $F_q > F_p$. $\square$

**Lemma 3 (same busy periods).** FQ and the ideal are both work conserving and have the same arrivals, so at every time they have the same amount of unfinished work, and they have the same busy periods.

*Proof.* In both systems the unfinished work grows by $L_p$ at each arrival and falls at rate $r$ whenever it is positive. Two functions that satisfy the same equation from the same start are equal. $\square$

**Theorem 4 (one packet of lag).** For every packet $p$, $\hat d_p \le d_p + L_{max}/r$.

*Proof.* Fix a busy period, which by Lemma 3 is the same in both systems, and shift time so that it starts at 0. Let $p_1, p_2, \dots$ be the packets of the busy period in the order in which FQ sends them. FQ does not idle in the busy period, so $\hat d_{p_k} = \sum_{i \le k} L_{p_i} / r$. Fix $k$, and let $j$ be the largest index below $k$ with $d_{p_j} > d_{p_k}$.

*Case 1: there is no such $j$.* Then $d_{p_i} \le d_{p_k}$ for all $i \le k$. All these packets arrive at time 0 or later, and the ideal sends at most $r$ bits per unit of time, so it finishes $p_1, \dots, p_k$ by time $d_{p_k}$ only if $\sum_{i \le k} L_{p_i} \le r\, d_{p_k}$. Hence $\hat d_{p_k} \le d_{p_k}$.

*Case 2: $j$ exists.* Let $s = \hat d_{p_j} - L_{p_j}/r$ be the time at which FQ started $p_j$. For each $i$ with $j < i \le k$ we have $d_{p_i} \le d_{p_k} < d_{p_j}$ (for $i < k$ by the choice of $j$), so $F_{p_i} < F_{p_j}$ by Corollary 2. Line L8 picked $p_j$ at time $s$, the queued packet with the least finish number, so $p_i$ was not yet queued: $a_{p_i} > s$. So the packets $p_{j+1}, \dots, p_k$ all arrive after $s$ and all finish in the ideal by $d_{p_k}$. The ideal sends at most $r(d_{p_k} - s)$ bits in $[s, d_{p_k}]$, hence

$$\sum_{i=j+1}^{k} L_{p_i} \le r\,(d_{p_k} - s).$$

FQ sends $p_j, p_{j+1}, \dots, p_k$ back to back from time $s$, so

$$\hat d_{p_k} = s + \frac{L_{p_j}}{r} + \sum_{i=j+1}^{k} \frac{L_{p_i}}{r} \le s + \frac{L_{p_j}}{r} + d_{p_k} - s \le d_{p_k} + \frac{L_{max}}{r}.$$

In both cases the bound holds. $\blacksquare$

This is the argument of Parekh and Gallager for packet-by-packet GPS, specialised to equal weights.

**Corollary 5 (isolation).** Suppose a flow $i$ sends a packet of $L$ bits that finds flow $i$ idle in the ideal, and that at most $N$ flows are active in the ideal while it is served. Then FQ finishes it within $N L / r + L_{max}/r$ of its arrival, whatever the other flows send.

*Proof.* In the ideal, flow $i$ is served at rate at least $r/N$, so $d_p \le a_p + NL/r$. Apply Theorem 4. $\square$

In the isolation example of the page, $N = 2$ and $L = 100$, which gives the bound $200 + 1500$.

**Theorem 6 (cost).** Over a run with $n$ packets, the loop of line L5 makes at most $n$ passes in total.

*Proof.* Each pass makes at least one flow inactive. A flow becomes active only at line L3, at most once per arrival. So the number of times a flow becomes inactive is at most $n$. $\square$
