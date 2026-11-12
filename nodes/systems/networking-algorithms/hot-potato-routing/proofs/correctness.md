---
title: The multi-source Dijkstra gives each router its nearest egress with the lowest-id tie-break, and forwarding toward the chosen egresses is consistent
proves: [correctness, time.worst]
status: full
---

**Setting.** $G = (V, E)$ is the interior graph of one AS, with link costs $w(u, v) > 0$ and $n$ routers, $m$ links. $X \subseteq V$ is the set of egress routers whose BGP routes for a prefix tie in all steps of the decision process before the interior-cost step. Egress routers have distinct ids, ordered. For $v \in V$ define

$$L(v) = \min_{e \in X} \bigl(\delta(v, e), e\bigr),$$

the least pair in lexicographic order: least interior distance, and among those the least id. This is what the interior-cost step and the BGP Identifier step of RFC 4271, Section 9.1.2.2, select when every egress has one route and the ids are the router ids.

**Claim 1 (the algorithm computes $L$).** Add a new vertex $s$ with an arc of weight $(0, e)$ to each $e \in X$, and give each link the weight $(w(u, v), 0)$. Let weights be pairs added component by component, except that the second component of a path is the id on its first arc; formally, use the set $\mathbb{R}_{\ge 0} \times (X \cup \{\top\})$ with $(a, x) \oplus (b, \top) = (a + b, x)$ and order it lexicographically. The weight of a path $s, e, \dots, v$ is then $(\text{its interior cost}, e)$, and the least weight of a path from $s$ to $v$ is $L(v)$. Lines L1 to L8 are [Dijkstra's algorithm](/dijkstra/) from $s$ in this setting, with the arcs out of $s$ applied at once in line L2.

Dijkstra's correctness proof uses only three facts about weights: they are totally ordered, every weight is at least the zero weight, and adding a nonnegative weight to a path does not make it smaller and preserves order, that is, $a \le b$ implies $a \oplus c \le b \oplus c$. All three hold here: lexicographic order is total, and adding $(c, \top)$ with $c \ge 0$ adds $c$ to the first component and keeps the second, which preserves the lexicographic order and does not decrease it. Hence the label of each router when it leaves the queue is $L(v)$, and $\mathrm{next}[v]$ is the predecessor of $v$ on a path of that weight.

**Claim 2 (consistent forwarding).** Let $v \notin X$ with $L(v) = (d, e)$ and $u = \mathrm{next}[v]$. Then $L(u) = (d - w(v, u), e)$, by line L7: $v$ got its final label from $u$. Thus $u$ chooses the same egress $e$, and its distance is smaller by $w(v, u) > 0$. By induction, the walk $v, \mathrm{next}[v], \mathrm{next}[\mathrm{next}[v]], \dots$ visits routers that all choose $e$, with strictly falling distances, so it has no repeated router and ends at $e$ with total cost $d = \delta(v, e)$.

The same holds for routers that forward by their own IGP tables toward their own chosen egress, without the shared $\mathrm{next}$ array. Let $v$ choose $e$, and let $u$ be any neighbour on a shortest path from $v$ to $e$, so $\delta(u, e) = \delta(v, e) - w(v, u)$. For any other egress $e'$, the triangle inequality gives $\delta(u, e') \ge \delta(v, e') - w(v, u) \ge \delta(v, e) - w(v, u) = \delta(u, e)$. If equality holds throughout, then $\delta(v, e') = \delta(v, e)$, so $e < e'$ because $v$ chose $e$. In every case $(\delta(u, e), e) < (\delta(u, e'), e')$, so $u$ also chooses $e$. So in plain hop-by-hop forwarding, a packet never switches to another egress on its way.

**Time.** Each router is removed from the queue once and each link is relaxed at most twice. With a [binary heap](/binary-heap/) with lazy deletion, each operation takes $O(\log n)$ time, and there are $O(n + m)$ of them, so the time is $O((n + m) \log n)$, and the labels take $O(n)$ space. $\blacksquare$
