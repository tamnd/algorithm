---
title: The network simplex method with strongly feasible trees is correct and finite
proves: [correctness, termination]
status: full
---

**Setting.** $G = (V, E)$ is directed with finite capacities $u \ge 0$, costs $c$ of any sign, and supplies $b$ with $\sum_v b(v) = 0$. The extended network $G^+$ adds a root $r$ and one artificial edge per vertex, of cost $M$ and unlimited capacity, as in line L1. Edges of capacity 0 are fixed at 0 and ignored below. $C = \max_e |c(e)|$, and $M = (C + 1)(n + 1)$, so $2M > (n - 1) C$.

A *tree solution* is a spanning tree $T$ of $G^+$ and a feasible flow $x$ of $G^+$ in which every non-tree edge is empty or full. For a direction of travel along an edge, the *residual* is $u(e) - x(e)$ when walking from tail to head, and $x(e)$ when walking from head to tail. $T$ is *strongly feasible* if, for every vertex $v$, every edge of the tree path from $v$ to $r$, walked toward $r$, has positive residual. Potentials $\pi$ and reduced costs $c^{\pi}$ are as on the page; tree edges have $c^{\pi} = 0$.

**Lemma 1 (start).** The first tree is a strongly feasible tree solution.

*Proof.* The artificial flows meet every supply: $v \to r$ carries $b(v) \ge 0$ out of $v$, and $r \to v$ carries $-b(v)$ into $v$, and $r$ is balanced since $\sum b = 0$. Real edges are empty, which is a bound. A tree path from $v$ to $r$ is one artificial edge. If it is $v \to r$, walking toward $r$ follows the edge, whose capacity is unlimited. If it is $r \to v$, walking toward $r$ goes against it, with residual $-b(v) > 0$. $\square$

**Lemma 2 (cost change).** For any feasible flows $x$, $y$ of $G^+$ and any potentials $\pi$, $c(y) - c(x) = \sum_e c^{\pi}(e)(y(e) - x(e))$.

*Proof.* $\sum_e (\pi(\mathrm{tail}\,e) - \pi(\mathrm{head}\,e))(y(e) - x(e)) = \sum_v \pi(v)\,(\text{net outflow of } y - x \text{ at } v) = 0$, because $y - x$ has net outflow 0 at every vertex. $\square$

**Lemma 3 (a pivot).** Let $e$ be eligible, and let $W$ be its cycle, oriented as at line L5. Pushing $\delta$ units around $W$ keeps feasibility, keeps every non-tree edge at a bound after the exchange of line L8, and changes the cost by $-\delta\,|c^{\pi}(e)|$.

*Proof.* $\delta$ is the least residual along $W$ in its orientation, so no bound is crossed, and a push around a cycle keeps every net outflow. The edge $f$ has residual $\delta$, so after the push it is at a bound and may leave the tree; $T - f + e$ is a spanning tree because $f$ lies on the unique cycle of $T + e$. The entering edge has positive residual in its orientation, at least $u(e) > 0$, and $\delta$ is finite because $e$ has finite capacity. By Lemma 2 with the old potentials, only $e$ has a nonzero reduced cost on $W$, and it changes by $\delta$ in the direction that lowers the cost by $\delta\,|c^{\pi}(e)|$. $\square$

**Lemma 4 (strong feasibility is kept).** If $T$ is strongly feasible and $f$ is chosen as at line L6, then $T' = T - f + e$ is strongly feasible.

*Proof.* Let $w$ be the apex. Walk $W$ in its orientation from $w$; $f$ splits the walk into the part before $f$ and the part after $f$. Removing $f$ and adding $e$, the vertices of $W$ after $f$ reach $w$ in $T'$ by continuing along the orientation, and the vertices before $f$ reach $w$ by going back against it. Vertices off $W$ keep their path to $W$ or to $r$, and the path from $w$ to $r$ is unchanged; its edges have positive residual toward $r$ by strong feasibility of $T$, and the push did not touch them.

*After $f$.* Every edge of $W$ after $f$ is not blocking, by the choice of $f$ as the last blocking edge, so its residual in the orientation was larger than $\delta$, and after the push it is still positive.

*Before $f$.* Walking against the orientation, the residual of each edge rose by $\delta$. If $\delta > 0$, it is positive. If $\delta = 0$, we show that $f$ is on the path from $w$ to the start $a$ of $e$; then the edges before $f$ lie on that path, and walking against the orientation there goes up the tree toward $w$, where $T$ had positive residuals, which the push of 0 units did not change. The walk after $e$ goes from the end of $e$ up the tree to $w$, so those edges have positive residual by strong feasibility, and they are not blocking. The entering edge has residual $u(e) > 0$. So every blocking edge, and $f$ in particular, lies on the path from $w$ down to $a$.

So every vertex has a path to $r$ in $T'$ with positive residuals toward $r$. $\square$

**Lemma 5 (potentials rise in a degenerate pivot).** If $\delta = 0$, the new potentials $\pi'$ agree with $\pi$ outside the subtree $X$ that $f$ cut off from $r$, and $\pi'(v) = \pi(v) + |c^{\pi}(e)|$ for $v \in X$.

*Proof.* By Lemma 4, $f$ is on the path from $w$ down to $a$, so $X$ is the part below $f$, and it contains $a$ and not the other end of $e$. Tree edges inside $X$ and outside $X$ are unchanged, so $\pi'$ differs from $\pi$ by a constant $\Delta$ on $X$ and agrees with it outside, with $\pi'(r) = 0$. The new tree edge $e$ needs reduced cost 0. If $e = (a, b)$ was empty, $c(e) + \pi(a) + \Delta - \pi(b) = 0$ gives $\Delta = -c^{\pi}(e) > 0$. If $e = (b, a)$ was full, $c(e) + \pi(b) - \pi(a) - \Delta = 0$ gives $\Delta = c^{\pi}(e) > 0$. $\square$

**Theorem.** The method stops. At the end, if an artificial edge carries flow, $G$ has no feasible flow; otherwise the flow on the real edges is a minimum-cost feasible flow of $G$.

*Proof.* *Termination.* A tree solution is determined by $T$ and by which non-tree edges are full, so there are finitely many. By Lemma 3 a pivot with $\delta > 0$ lowers the cost, and by Lemma 5 a pivot with $\delta = 0$ keeps the cost and raises $\sum_v \pi(v)$, which depends only on $T$. So the pair (cost, $-\sum_v \pi(v)$) decreases strictly in the lexicographic order at every pivot, no tree solution repeats, and the loop ends.

*Optimality in $G^+$.* At the end no edge is eligible: tree edges have $c^{\pi} = 0$, empty edges $c^{\pi} \ge 0$, full edges $c^{\pi} \le 0$. For any feasible $y$ of $G^+$, each term of Lemma 2 is $\ge 0$: where $x(e) = 0$, $y(e) - x(e) \ge 0$ and $c^{\pi}(e) \ge 0$; where $x(e) = u(e)$, $y(e) - x(e) \le 0$ and $c^{\pi}(e) \le 0$. So $x$ is optimal in $G^+$.

*Artificial flow.* If $x$ uses no artificial edge, its restriction is a feasible flow of $G$, and it is optimal in $G$ since every flow of $G$ is a flow of $G^+$ of the same cost. Suppose instead $x$ uses an artificial edge but $G$ has a feasible flow $z$, extended by 0 on artificial edges. Then $d = x - z$ has net outflow 0 everywhere, and it splits into simple cycles $C_i$ with weights $\lambda_i > 0$, each conformal to $d$: it walks forward only where $d > 0$ and backward only where $d < 0$. Some cycle uses an artificial edge, since $d$ is positive there. A simple cycle through $r$ uses exactly two artificial edges, both forward because $d \ge 0$ on them, and at most $n - 1$ real edges, so its cost is at least $2M - (n - 1) C > 0$. Subtracting $\lambda_i C_i$ from $x$ for all such cycles gives a flow $y$ that lies between $x$ and $z$ on every edge, hence is feasible in $G^+$, and $c(y) < c(x)$. This contradicts the optimality of $x$. So artificial flow at the end means that $G$ has no feasible flow. $\blacksquare$
