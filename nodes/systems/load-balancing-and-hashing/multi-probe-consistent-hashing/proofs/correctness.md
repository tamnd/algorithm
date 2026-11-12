---
title: Multi-probe lookup returns the nearest node over all probes, is monotone, and has exact shares given by an integral
proves: [correctness]
status: full
---

We use the pseudocode of the page. The ring has $R$ positions. Each node $v$ has one point $p_v$, and the points are distinct. A key $x$ has the probe points $q_1, \ldots, q_k$. For a probe point $q$ and a node $v$, write $d(q, v) = (p_v - q) \bmod R$ for the clockwise distance from $q$ to the point of $v$.

**Lemma 1 (the next node is the nearest node).** For a probe point $q$, the node whose point is the first point of $P$ at or after $q$, with wraparound, is the unique node $v$ with the smallest $d(q, v)$.

*Proof.* Walk clockwise from $q$. The distance $d(q, v)$ is the number of steps until the walk reaches $p_v$. The first node point that the walk reaches has the smallest number of steps, and it is the first point of $P$ at or after $q$, or $P[0]$ if no point is at or after $q$. The points are distinct, so no other node has the same distance. $\square$

Define the rank of a pair $(i, v)$ as $(d(q_i, v), i)$, compared first by distance and then by probe number.

**Theorem 1 (the lookup).** MP-LOOKUP returns the node $v$ of the pair $(i, v)$ with the smallest rank over all probes $i$ and all nodes $v$.

*Proof.* By Lemma 1, for a fixed probe $i$ the smallest rank among the pairs $(i, \cdot)$ belongs to the node found in line L4, and line L5 computes its distance. We show this invariant: after the loop of line L2 has done probes $1$ to $i$, $\text{best}$ is the node of the smallest-rank pair among the probes $1$ to $i$, and $\text{best\_dist}$ is its distance. Before the first probe, line L1 sets $\text{best\_dist} = R$, which is larger than every distance. At probe $i$, line L6 replaces the best pair only if the new distance is strictly smaller. If the new distance is equal, the old pair has the smaller probe number and so the smaller rank. So the invariant holds after probe $i$. After probe $k$, line L8 returns the node of the smallest-rank pair. $\square$

**Theorem 2 (adding a node).** Add a node $w$ with a new point. Then each key either keeps its node or moves to $w$.

*Proof.* The probe points of a key do not depend on the nodes, and the distance $d(q_i, v)$ of an old node $v$ does not change. So the set of pairs after the change is the old set plus the pairs $(i, w)$. The smallest rank over the larger set is the old smallest rank or the rank of a new pair. In the first case the key keeps its node, by Theorem 1. In the second case its node is $w$. $\square$

**Theorem 3 (removing a node).** Remove a node $w$. Then only the keys of $w$ change their node.

*Proof.* The set of pairs after the change is the old set without the pairs $(i, w)$. If the old smallest-rank pair of a key has a node other than $w$, that pair is still in the set, and a subset has no pair of smaller rank. So the key keeps its node. $\square$

Theorems 2 and 3 are the [monotonicity property](/monotonicity-property/) for this scheme.

**Theorem 4 (exact shares).** Take a ring of length 1 with node points fixed, and let $a_v$ be the length of the arc that ends at $p_v$ and starts at the point before it. Let the $k$ probes of a key be independent and uniform on the ring. Write $G(t) = \sum_v \max(a_v - t, 0)$. Then the probability that the key goes to node $v$ is

$$s_v = k \int_0^{a_v} G(t)^{k-1}\, dt,$$

and $\sum_v s_v = 1$.

*Proof.* Take one probe. Its next node is $v$ and its distance is at most $t$ when the probe lies in the last part of length $\min(t, a_v)$ of the arc of $v$. So the pair (next node, distance) has density 1 on the set $\{(v, t) : 0 \le t < a_v\}$, and the probability that the distance is more than $t$ is $\sum_v \max(a_v - t, 0) = G(t)$. Two probes have the same distance with probability 0, so we can ignore ties. The key goes to $v$ when exactly one probe, say probe $i$, has the smallest distance $t$, its next node is $v$, and the other $k - 1$ probes have distance more than $t$. For a fixed $i$ this has probability $\int_0^{a_v} G(t)^{k-1}\, dt$, by independence. The $k$ events for $i = 1, \ldots, k$ are disjoint, so their probabilities add, which gives $s_v$.

For the sum, let $c(t)$ be the number of nodes with $a_v > t$. Then $G$ is continuous, $G'(t) = -c(t)$ except at the points $t = a_v$, $G(0) = 1$, and $G(t) = 0$ for $t \ge \max_v a_v$. The node $v$ is counted in $c(t)$ exactly for $t < a_v$, so

$$\sum_v s_v = k \int_0^{\infty} c(t)\, G(t)^{k-1}\, dt = \left[-G(t)^k\right]_0^{\infty} = 1. \quad\square$$

**Computing the shares.** Sort the arcs, $a_{(1)} \le \cdots \le a_{(n)}$. On the piece between $a_{(j-1)}$ and $a_{(j)}$, the count $c$ is $n - j + 1$ and $G$ is linear with slope $-c$, so

$$k \int_{t_0}^{t_1} G(t)^{k-1}\, dt = \frac{G(t_0)^k - G(t_1)^k}{c}.$$

The share of the node with the $j$-th smallest arc is the sum of these terms over the first $j$ pieces. This is the function `exact_shares` of the implementation, and it takes $O(n \log n)$ time.

**Two consequences.** For $k = 1$, $s_v = a_v$, which is the plain ring. Since $G(t) \le 1$, every share is at most $k a_v$, so a node with a short arc stays light for every $k$. The bound $k/(k-1)$ on the largest share, for random node points and $2 \le k \ll \sqrt{n}/\ln n$, is Theorem 1 of Appleton and O'Reilly. It holds with high probability over the node points and is not a statement about every node set. $\blacksquare$
