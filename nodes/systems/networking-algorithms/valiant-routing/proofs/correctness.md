---
title: Valiant's two-phase routing delivers every packet of a permutation on the hypercube within 14n steps with probability at least 1 - 2^(-5n+1)
proves: [correctness]
status: full
---

**Model.** The network is the hypercube with $N = 2^n$ nodes, written as bit strings $x_1 x_2 \ldots x_n$, and a directed edge in each direction between nodes that differ in one bit. Time runs in synchronous steps. In each step each directed edge carries at most one packet. A packet that wants an edge waits in a queue at that edge. The queue policy can be anything that is *non-idling*: if the queue of an edge is not empty at a step, the edge carries a packet in that step. FIFO is one such policy. Queues have no size limit.

**Routes.** The bit-fixing route from $u$ to $t$ visits the nodes $P_k = t_1 \ldots t_k\, u_{k+1} \ldots u_n$ for $k = 0, \ldots, n$, and between $P_{k-1}$ and $P_k$ it crosses the edge of dimension $k$ out of $P_{k-1}$ when $u_k \ne t_k$ (otherwise $P_{k-1} = P_k$ and no edge is used). The route has at most $n$ edges, used in increasing order of dimension.

**Phases.** Packet $p$ starts at node $p$ and has destination $d_p$, where $d$ is a permutation. It picks $r_p$ uniformly at random and independently. In phase 1 every packet follows the bit-fixing route from $p$ to $r_p$. Phase 2 starts at step $7n$ (or when every packet has reached $r_p$, if that is earlier and the system knows it), and every packet follows the bit-fixing route from $r_p$ to $d_p$.

**Lemma 1 (routes meet in one segment).** If the bit-fixing routes of two packets share an edge of dimension $i$ and an edge of dimension $j > i$, they also share every edge between them on the two routes. So once two routes separate, they do not meet again.

*Proof.* Let the packets go from $u$ to $t$ and from $u'$ to $t'$. Sharing the edge of dimension $i$ means they are at the same node $P_{i-1}$, so $t_1 \ldots t_{i-1} = t'_1 \ldots t'_{i-1}$ and $u_i \ldots u_n = u'_i \ldots u'_n$. Sharing the edge of dimension $j$ means $t_1 \ldots t_{j-1} = t'_1 \ldots t'_{j-1}$ and $u_j \ldots u_n = u'_j \ldots u'_n$. For each $k$ with $i \le k \le j - 1$, the node $P_k = t_1 \ldots t_k\, u_{k+1} \ldots u_n$ is then the same for both packets, because $t_1 \ldots t_k$ is a prefix of $t_1 \ldots t_{j-1}$ and $u_{k+1} \ldots u_n$ is a suffix of $u_i \ldots u_n$. Equal nodes $P_{k-1}$ and $P_k$ give the same edge, or no edge for both. $\square$

**Lemma 2 (delay lemma).** Fix one phase and a packet $p$ whose route is $e_1, \ldots, e_k$. Let $S$ be the set of other packets whose routes share at least one edge with the route of $p$. Then $p$ arrives by step $k + |S|$.

*Proof.* Number the steps $1, 2, \ldots$ from the start of the phase. Say that a packet has *lag* $\ell$ at step $t$ if at the start of step $t$ it is in the queue of edge $e_j$ of the route of $p$ (it may cross $e_j$ in that step) and $t - j = \ell$. A packet that crosses $e_j$ at step $t$ and is then in the queue of $e_{j+1}$ at step $t+1$ keeps its lag, and a packet that stays in a queue for a step without crossing gains 1. Packet $p$ has lag 0 at step 1, and its lag when it crosses $e_k$ is its delay $\delta$, which is its arrival step minus $k$. Its lag takes every value $0, 1, \ldots, \delta$.

Fix $\ell$ with $0 \le \ell < \delta$. Some packet has lag $\ell$ at some step, so there is a last step $t'$ at which some packet has lag $\ell$; say that packet waits at $e_j$, with $t' - j = \ell$. The queue of $e_j$ is not empty at step $t'$, so by the non-idling rule some packet $q$ crosses $e_j$ at step $t'$, and $q$ also has lag $t' - j = \ell$. If $q$ then waits for $e_{j+1}$ at step $t'+1$, it has lag $\ell$ at step $t' + 1$, against the choice of $t'$. So $q$ leaves the route of $p$ after $e_j$. This $q$ is not $p$: packet $p$ leaves its route only after $e_k$, and then with lag $\delta \ne \ell$. So $q \in S$, and $q$ leaves the route of $p$ with lag $\ell$.

By Lemma 1, each packet of $S$ uses one contiguous segment of the route of $p$, so it leaves the route once, with one lag. Different values of $\ell$ therefore give different packets of $S$, and $\delta \le |S|$. $\square$

**Lemma 3 (expected load).** In phase 1, for any fixed edge $e$, the expected number of packets whose route uses $e$ is $1/2$. The same holds in phase 2.

*Proof.* Let $e$ be the edge of dimension $i$ out of node $w$. In phase 1, the route of the packet from $u$ to $t$ uses $e$ exactly when $P_{i-1} = w$ and $t_i \ne u_i$, that is, when $t_1 \ldots t_{i-1} = w_1 \ldots w_{i-1}$, $u_i \ldots u_n = w_i \ldots w_n$ and $t_i \ne w_i$. Exactly $2^{i-1}$ start nodes $u$ have $u_i \ldots u_n = w_i \ldots w_n$, one packet each. For each of them, the random $t = r_u$ has the required first $i$ bits with probability $2^{-i}$. The expected count is $2^{i-1} \cdot 2^{-i} = 1/2$.

In phase 2, the packet goes from $u = r_p$ to $t = d_p$, and the same condition applies. The destinations form a permutation, so exactly $2^{n-i}$ packets have $t_1 \ldots t_{i-1} = w_1 \ldots w_{i-1}$ and $t_i \ne w_i$. For each of them, the random $r_p$ has $r_i \ldots r_n = w_i \ldots w_n$ with probability $2^{-(n-i+1)}$. The expected count is $2^{n-i} \cdot 2^{-(n-i+1)} = 1/2$. $\square$

**Lemma 4 (one phase).** In each phase, with probability at least $1 - 2^{-5n}$, every packet finishes the phase within $7n$ steps of its start.

*Proof.* Fix a packet $p$ and condition on $r_p$, which fixes the route of $p$, of at most $n$ edges. For each other packet $q$, let $H_q = 1$ if the route of $q$ shares an edge with the route of $p$. In either phase, $H_q$ depends only on $r_q$, so the $H_q$ are independent given $r_p$. Since $H_q \le$ the number of edges of $p$'s route that $q$ uses, Lemma 3 (applied to the other packets, whose choices do not depend on $r_p$) gives

$$\mu = \mathbb{E}\Big[\sum_{q \ne p} H_q\Big] \le \sum_{e \in \text{route}(p)} \mathbb{E}[\text{number of packets using } e] \le \frac n2.$$

By the [Chernoff bound](/chernoff-bound/) for a sum of independent 0-1 variables, $\Pr[X \ge R] \le 2^{-R}$ for every $R \ge 6\mu_H$, where $\mu_H \ge \mu$ is any upper bound on the mean. With $\mu_H = n/2$ and $R = 6n \ge 3n$, $\Pr[|S| \ge 6n] \le 2^{-6n}$. By Lemma 2, outside this event $p$ finishes within $n + 6n = 7n$ steps. A [union bound](/union-bound/) over the $2^n$ packets gives failure probability at most $2^n \cdot 2^{-6n} = 2^{-5n}$. $\square$

**Theorem.** With probability at least $1 - 2^{-5n+1}$, every packet reaches its destination within $14n$ steps.

*Proof.* By Lemma 4 for phase 1, with probability at least $1 - 2^{-5n}$ all packets reach their intermediate nodes by step $7n$, so phase 2 starts with every packet in place and no packet of phase 1 left in a queue. Lemma 2 needs nothing about the start positions, and Lemma 3 holds for phase 2 for any permutation $d$, so Lemma 4 applies to phase 2 as a fresh routing problem started at step $7n$. With probability at least $1 - 2^{-5n}$ it ends by step $14n$. A union bound over the two phases gives the claim. Since $2^{-5n+1} \le 2^{-n} = 1/N$ for $n \ge 1$, all packets arrive within $14 \log_2 N$ steps with probability at least $1 - 1/N$. $\blacksquare$

**Remark (what the proof does not cover).** If phase 2 starts for each packet as soon as it reaches $r_p$ (the pipelined form), packets of the two phases share queues and Lemma 2 does not apply as stated. The pipelined form is faster in the simulations of the page, and other analyses cover it, but this proof does not.
