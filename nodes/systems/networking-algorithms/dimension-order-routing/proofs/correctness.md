---
title: Dimension-order routing takes shortest paths on meshes and hypercubes and cannot deadlock there; on a torus it needs a second virtual channel
proves: [correctness]
status: full
---

We use the pseudocode of the page on a $k$-ary $n$-dimensional mesh: the nodes are the vectors $(x_0, \ldots, x_{n-1})$ with $0 \le x_d < k$, and there is a channel in each direction between nodes that differ by 1 in one coordinate. The hypercube is the case $k = 2$.

**Lemma 1 (delivery on a shortest path).** From any node $u$ to any node $t$, the route makes exactly $\sum_d |u_d - t_d|$ hops, and this is the distance from $u$ to $t$.

*Proof.* Let $d$ be the first dimension with $u_d \ne t_d$. Lines L1 to L4 return the link of dimension $d$ that moves $u_d$ one step toward $t_d$. It exists: if $u_d < t_d$ then $u_d + 1 \le t_d \le k - 1$, and if $u_d > t_d$ then $u_d - 1 \ge t_d \ge 0$, so the move stays in the mesh. The move lowers $\Phi = \sum_d |u_d - t_d|$ by exactly 1, so after $\Phi(u)$ hops $\Phi = 0$, the current node is $t$, and line L5 delivers the packet. Any path changes one coordinate by 1 per hop, so every path from $u$ to $t$ has at least $\Phi(u)$ hops. $\square$

**Lemma 2 (an increasing channel numbering).** Give the channel that leaves node $x$ along dimension $d$ the number

$$\nu = 2kd + \begin{cases} x_d & \text{in the + direction,} \\ k + (k - 1 - x_d) & \text{in the − direction.} \end{cases}$$

Then the numbers of the channels on every route strictly increase.

*Proof.* Inside one dimension $d$ the route moves in one direction only, by Lemma 1 (each hop moves toward $t_d$). In the + direction $x_d$ grows by 1 per hop, so $\nu$ grows; in the − direction $x_d$ falls by 1 per hop, so $k + (k - 1 - x_d)$ grows. All numbers of dimension $d$ lie in $[2kd, 2kd + 2k - 1]$, and the route visits the dimensions in increasing order, so a later dimension has larger numbers. $\square$

So the channel dependency graph, which has an edge $c \to c'$ when some route uses $c'$ right after $c$, has no cycle: along each edge the number grows.

**Theorem (no deadlock, after Dally and Seitz 1987).** Assume that each channel has a buffer of finite size, that a packet may hold several consecutive channels of its route (as in wormhole routing) but only in route order, that a packet waits only for the next channel of its route, and that a packet that reaches its destination is removed in finite time. If the channels have a numbering that strictly increases along every route, then no set of packets can be deadlocked.

*Proof.* Assume a nonempty set $P$ of packets is deadlocked: no packet in $P$ ever moves again, and each packet $p \in P$ waits for its next channel $w(p)$, which is full of packets of $P$. (A packet at its destination is removed, so it is not in $P$.) Let $h(p)$ be the channel that holds the head of $p$. Since $p$ holds channels in route order, the head is in the channel of largest number that $p$ holds, and $\nu(w(p)) > \nu(h(p))$, because $w(p)$ comes after $h(p)$ on the route.

Start with any $p_0 \in P$. The channel $w(p_0)$ holds some packet $p_1 \in P$, so $\nu(h(p_1)) \ge \nu(w(p_0))$, and then $\nu(w(p_1)) > \nu(h(p_1)) \ge \nu(w(p_0))$. Repeating gives packets $p_0, p_1, p_2, \ldots$ in $P$ with $\nu(w(p_0)) < \nu(w(p_1)) < \cdots$. All these numbers are distinct, so the packets are distinct, which is impossible in the finite set $P$. $\blacksquare$

By Lemma 2 the theorem applies to dimension-order routing on every mesh and hypercube. (Dally and Seitz also prove the converse for deterministic routing functions: a cycle in the dependency graph allows a deadlock. We do not use it.)

**Torus without virtual channels.** On a ring of $k \ge 4$ nodes with minimal routing and ties sent in the + direction, the route from $x$ to $x + 2$ uses the + channels out of $x$ and $x + 1$ (since $2 \le k/2$). So for every $x$ there is a dependency from the + channel out of $x$ to the + channel out of $x + 1$, and these $k$ dependencies form a cycle. With full buffers, $k$ packets, each holding the channel out of $x$ and waiting for the channel out of $x+1$, are deadlocked. For $k = 3$ every minimal route inside a ring has one hop, so there are no dependencies inside a ring. Numbering every channel of dimension $d$ by $d$ then gives a numbering that strictly increases along every route, because consecutive hops of a route are in strictly increasing dimensions, and the theorem applies.

**Torus with a dateline.** Give each channel two virtual channels, VC 0 and VC 1, and let a packet use VC 0 when it enters a dimension and VC 1 after it has crossed the wrap-around channel of that ring (from $k-1$ to 0 in the + direction, from 0 to $k-1$ in the − direction). Number the + channels of dimension $d$ out of coordinate $x$ as $4kd + x$ on VC 0 and $4kd + k + x$ on VC 1, and the − channels as $4kd + 2k + (k - 1 - x)$ on VC 0 and $4kd + 3k + (k - 1 - x)$ on VC 1. A minimal route in one ring has fewer than $k$ hops, so it crosses the wrap channel at most once. Before the wrap the numbers grow on VC 0, the wrap channel itself is on VC 0 with the largest VC 0 number of its direction, and after the wrap the numbers start again on VC 1, above all VC 0 numbers of that direction, and grow. Different dimensions have disjoint ranges in increasing order. So the numbers strictly increase along every route, and the theorem gives freedom from deadlock. The tests check the cycle for $k = 4, 5, 6$ and the acyclic graph with a dateline for $k = 4, \ldots, 7$ in two dimensions.
