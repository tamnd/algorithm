---
title: WFQ finishes each packet within one maximum packet time of GPS
proves: [correctness]
status: full
---

We use the pseudocode of the page. GPS is the fluid model of [generalized processor sharing](/generalized-processor-sharing/) on the same arrivals: at each time, each flow $i$ that has bits in GPS is served at rate $\varphi_i r / \Phi_{GPS}(t)$, where $\Phi_{GPS}(t)$ is the sum of the weights of those flows, and each flow is served in FIFO order. Write $L_p$, $a_p$, $S_p$ and $F_p$ for the size, arrival time and tags of packet $p$, $d_p$ for its GPS finish time and $\hat d_p$ for its WFQ finish time. Let $L_{max} = \max_p L_p$.

**Lemma 1 (the virtual time tracks GPS).** At all times, the set of flows with $F_{last}[i] > V$ is the set of flows with bits in GPS, $\Phi = \Phi_{GPS}$, and each such flow $i$ has exactly $\varphi_i (F_{last}[i] - V)$ bits left in GPS.

*Proof.* By induction over the events in time order: the arrivals, and the points of line L5 at which $V$ reaches a last tag. At the start, no flow has bits and none has $F_{last} > V$. Between events the sets do not change. By lines L5 and L6, $V$ grows at rate $r / \Phi$, so each flow in the set loses $\varphi_i\, dV = \varphi_i r / \Phi \cdot dt$ bits in GPS while its count $\varphi_i(F_{last}[i] - V)$ falls by the same amount. At a point of line L5, $V = m$, and the flows with $F_{last} = m$ have 0 bits left, so they leave GPS exactly when line L5 removes their weights from $\Phi$. At an arrival of $L_p$ bits of flow $i$, line L2 gives $S_p = \max(F_{last}[i], V)$. If flow $i$ had bits, $S_p = F_{last}[i]$, and its bits left grow from $\varphi_i(F_{last}[i] - V)$ to $\varphi_i(F_p - V)$, an increase of $\varphi_i \cdot L_p / \varphi_i = L_p$. If it had no bits, $S_p = V$, its bits left become $L_p = \varphi_i(F_p - V)$, and line L3 adds $\varphi_i$ to $\Phi$. In both cases the invariant holds after the event. $\square$

**Corollary 2 (the tags are the GPS finish points).** Packet $p$ is served in GPS while $V$ runs from $S_p$ to $F_p$, and $d_p$ is the first time at which $V(t) = F_p$. Hence $F_p < F_q$ implies $d_p \le d_q$.

*Proof.* By Lemma 1, after the arrival of $p$ the bits of flow $i$ that belong to $p$ or to earlier packets are $\varphi_i(F_p - V)$ as long as this is positive, since later packets add to $F_{last}$ and to the bits left by the same amount. GPS serves flow $i$ in FIFO order, so $p$ is in service while this amount falls from $L_p$ to 0, that is, while $V$ runs from $F_p - L_p/\varphi_i = S_p$ to $F_p$. The flow keeps bits until $V$ reaches $F_p$, and $V$ strictly increases while some flow has bits, so $d_p$ is the first time with $V = F_p$. Since $V$ never decreases, a smaller tag is reached no later. $\square$

**Lemma 3 (same busy periods).** WFQ and GPS are both work conserving, so they have the same unfinished work at all times and the same busy periods.

*Proof.* In both systems the work grows by $L_p$ at each arrival and falls at rate $r$ while positive. $\square$

**Theorem 4 (Parekh and Gallager).** For every packet $p$, $\hat d_p \le d_p + L_{max}/r$.

*Proof.* Fix a busy period, the same in both systems by Lemma 3, and let it start at time 0. Let $p_1, p_2, \dots$ be its packets in the order in which WFQ sends them, so $\hat d_{p_k} = \sum_{i \le k} L_{p_i} / r$. Fix $k$ and let $j$ be the largest index below $k$ with $d_{p_j} > d_{p_k}$.

If there is no such $j$, then GPS finishes all of $p_1, \dots, p_k$ by $d_{p_k}$. They arrive at time 0 or later, and GPS serves at most $r$ bits per unit of time, so $\sum_{i \le k} L_{p_i} \le r\, d_{p_k}$, which is $\hat d_{p_k} \le d_{p_k}$.

Otherwise, let $s = \hat d_{p_j} - L_{p_j}/r$, the time at which WFQ started $p_j$. For $j < i \le k$ we have $d_{p_i} \le d_{p_k} < d_{p_j}$, so by Corollary 2, $F_{p_i} < F_{p_j}$. Line L8 chose $p_j$ at time $s$ as the queued packet with the least tag, so none of $p_{j+1}, \dots, p_k$ was queued at $s$: they all arrive after $s$. GPS serves all of them within $(s, d_{p_k}]$, at most $r(d_{p_k} - s)$ bits, so $\sum_{i=j+1}^{k} L_{p_i} \le r(d_{p_k} - s)$. WFQ sends $p_j, \dots, p_k$ back to back from $s$, so

$$\hat d_{p_k} = s + \frac{L_{p_j}}{r} + \sum_{i=j+1}^{k} \frac{L_{p_i}}{r} \le d_{p_k} + \frac{L_{p_j}}{r} \le d_{p_k} + \frac{L_{max}}{r}. \qquad \blacksquare$$

**Corollary 5 (delay bound).** If flow $i$ conforms to a token bucket of depth $\sigma_i$ and rate $\rho_i \le g_i = \varphi_i r / \sum_j \varphi_j$, then every packet of flow $i$ leaves WFQ within $\sigma_i / g_i + L_{max}/r$ of its arrival.

*Proof.* Under GPS the flow is served at rate at least $g_i$ whenever it is backlogged. Let $\tau$ be the start of the GPS backlogged period of flow $i$ that contains the arrival time $a$ of the packet. The bits of flow $i$ that arrive in $[\tau, a]$, including the packet, are at most $\sigma_i + \rho_i (a - \tau)$, and GPS has served them all once $g_i(t - \tau) \ge \sigma_i + \rho_i(a - \tau)$, which holds for $t = a + \sigma_i / g_i$ since $\rho_i \le g_i$. So $d_p \le a + \sigma_i/g_i$. Apply Theorem 4. $\square$

**Theorem 6 (cost).** Over $n$ arrivals, the loop of line L5 makes at most $n$ passes.

*Proof.* Each pass removes at least one flow from the set of flows with bits in GPS, and a flow enters that set only at line L3, at most once per arrival. $\square$
