---
title: Double coverage is k-competitive on the line and on trees
proves: [correctness]
status: full
---

**Theorem.** Let the $k$ servers of DC and of an offline schedule $B$ start at the same points $s_1, \ldots, s_k$ of the real line. For each request sequence $\sigma$,

$$\mathrm{DC}(\sigma) \le k \cdot \mathrm{cost}_B(\sigma) + \sum_{i<j} |s_i - s_j| .$$

With $B$ an optimal schedule, $\mathrm{DC}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + \sum_{i<j} |s_i - s_j|$, so DC is $k$-competitive.

**Notation.** Write $x_1 \le \dots \le x_k$ for the DC servers and $y_1, \ldots, y_k$ for the servers of $B$. Let $M$ be the cost of a minimum perfect matching between the two multisets, with cost $|x - y|$ for a pair. Let $\Sigma = \sum_{i<j} |x_i - x_j|$. The potential is

$$\Phi = k \cdot M + \Sigma \ge 0 .$$

At the start, both multisets are equal, so $M = 0$ and $\Phi_0 = \sum_{i<j} |s_i - s_j|$.

For request $r_t$, we let $B$ move first and then DC. We show two claims.

**Claim 1.** If $B$ moves its servers by a total distance $d$, then $\Phi$ rises by at most $k d$.

*Proof.* $\Sigma$ does not change. Take the minimum matching before the move and keep the same pairs. A server of $B$ that moves by $d'$ changes the cost of its pair by at most $d'$, by the triangle inequality. So the matching after the move costs at most $M + d$, and the new minimum is at most this. $\square$

After $B$ has moved, some server $y^*$ of $B$ is at $r = r_t$.

**Swap lemma.** Let $X'$ be a set of DC servers such that for each DC server $x_j \notin X'$ there is some $x_a \in X'$ with $|r - x_j| = |r - x_a| + |x_a - x_j|$. Then some minimum matching matches $y^*$ to a server of $X'$.

*Proof.* Take a minimum matching. If $y^*$ is matched to $x_j \notin X'$, choose $x_a \in X'$ as in the statement, and let $y'$ be the partner of $x_a$. Match $y^*$ with $x_a$ and $y'$ with $x_j$ instead. The cost changes by

$$|r - x_a| + |y' - x_j| - |r - x_j| - |y' - x_a| \le |r - x_a| + |x_a - x_j| - |r - x_j| = 0,$$

where we used $|y' - x_j| \le |y' - x_a| + |x_a - x_j|$. So the new matching is also minimum. $\square$

**Claim 2.** If DC moves its servers at a cost $c$, then $\Phi$ drops by at least $c$.

*Proof.* If a DC server is already at $r$, then $c = 0$ and nothing changes. Otherwise there are three cases.

*Case 1: $r < x_1$ (line L3).* Let $\delta = x_1 - r$, so $c = \delta$. Use the swap lemma with $X' = \{x_1\}$: for each $j$, $r < x_1 \le x_j$ gives $|r - x_j| = |r - x_1| + |x_1 - x_j|$. So a minimum matching pairs $x_1$ with $y^*$. Line L3 moves $x_1$ to $r$, which lowers the cost of this pair by $\delta$ and does not change the other pairs. So $M$ drops by at least $\delta$. The server $x_1$ moves away from each of the other $k - 1$ servers, so $\Sigma$ rises by $(k-1)\delta$. In total,

$$\Delta \Phi \le -k \delta + (k-1)\delta = -\delta = -c .$$

*Case 2: $r > x_k$ (line L4).* This is the mirror image of Case 1.

*Case 3: $x_i < r < x_{i+1}$ (lines L5 to L8).* Let $\delta = \min(r - x_i, x_{i+1} - r)$, so $c = 2\delta$. Use the swap lemma with $X' = \{x_i, x_{i+1}\}$: a server $x_j$ with $j < i$ has $x_j \le x_i < r$, and a server with $j > i + 1$ has $r < x_{i+1} \le x_j$. So a minimum matching pairs $y^*$ with $x_i$ or with $x_{i+1}$. That server moves by $\delta$ toward $r$ and does not pass it, so its pair gets cheaper by $\delta$. The other one of the two moves by $\delta$, so its pair gets dearer by at most $\delta$. The other pairs do not change. So $M$ does not rise.

For $\Sigma$, the pair $x_i, x_{i+1}$ gets closer by $2\delta$. Since $\delta \le (x_{i+1} - x_i)/2$, the two servers do not cross. A server $x_j$ with $j < i$ is left of both: it gets farther from $x_i$ by $\delta$ and closer to $x_{i+1}$ by $\delta$. A server with $j > i + 1$ is the mirror image. So $\Sigma$ drops by exactly $2\delta$, and

$$\Delta \Phi \le 0 - 2\delta = -c . \qquad \square$$

**Proof of the theorem.** Let $d_t$ be the cost of $B$ and $c_t$ the cost of DC for request $r_t$. By the two claims, $c_t + \Phi_t - \Phi_{t-1} \le k d_t$. Summing over $t = 1, \ldots, m$ gives

$$\mathrm{DC}(\sigma) + \Phi_m - \Phi_0 \le k \cdot \mathrm{cost}_B(\sigma).$$

Since $\Phi_m \ge 0$ and $\Phi_0 = \sum_{i<j} |s_i - s_j|$, the bound follows. $\square$

**Trees.** Let the metric be a tree with positive edge lengths, where points may lie inside edges. Root the tree at $r$. A DC server is *active* if no other server lies on the open path from it to $r$; of several servers at one point, only one counts as active. The tree rule moves all $a \ge 1$ active servers toward $r$ at the same speed. We cut the motion into steps in which each active server moves by $\delta$, where $\delta$ is so small that no server reaches a vertex, another server, or $r$ inside the step. The set of active servers is then fixed during the step, and the cost of the step is $a \delta$. Claim 1 holds without change. For Claim 2 we show $\Delta \Phi \le -a\delta$ in each step.

- *Matching.* For a non-active server $x_j$, walk from $r$ along the path to $x_j$. The first server met is active; call it $x_a$. Then $x_a$ lies on the path, so $d(r, x_j) = d(r, x_a) + d(x_a, x_j)$. By the swap lemma (which uses only the triangle inequality), a minimum matching pairs $y^*$ with an active server. That pair gets cheaper by $\delta$, and each of the other $a - 1$ moving servers makes its pair dearer by at most $\delta$. So $\Delta M \le (a - 2)\delta$.
- *Two active servers.* Their paths to $r$ meet at a point $z$, and their distance is the sum of their distances to $z$. Both move toward $z$, so the pair gets closer by $2\delta$. This gives $-a(a-1)\delta$ in total over the $\binom{a}{2}$ pairs.
- *A non-active server $u$.* The first server on the path from $r$ to $u$ is an active server $x_a$, and it moves away from $u$ by $\delta$. Each other active server $x_b$ has a path to $r$ that meets the path from $u$ to $r$ at a point between $x_a$ and $r$; otherwise $x_a$ would lie on the path from $x_b$ to $r$, and $x_b$ would not be active. So $x_b$ moves toward $u$ by $\delta$. The servers that do not move add nothing. So the distances to $u$ change by $\delta - (a-1)\delta = -(a-2)\delta$ in total.

With $k - a$ non-active servers,

$$\Delta \Phi \le k(a-2)\delta - a(a-1)\delta - (k-a)(a-2)\delta = a(a-2)\delta - a(a-1)\delta = -a\delta .$$

This is the cost of the step, so Claim 2 holds on trees, and the same sum gives $\mathrm{DC}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + \Phi_0$. For $a = 1$ the same computation gives $-\delta$, which also matches the cost. The line is the special case of a path. $\blacksquare$
