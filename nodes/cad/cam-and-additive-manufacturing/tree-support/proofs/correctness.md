---
title: Greedy cone merging gives a support forest of allowed struts, never longer than vertical pillars
proves: [correctness, termination]
status: full
---

**Claim.** Let $P$ be a finite set of $n$ points with rational coordinates and $z > 0$, and let $k > 0$ be rational. Then TREE-SUPPORT$(P, k)$ stops, and its output $E$ has these properties:

1. every strut $(a, b) \in E$ is allowed: $a_z > b_z$ and $\|a_{xy} - b_{xy}\| \le k\,(a_z - b_z)$;
2. every node has at most one strut below it, and the path of struts down from each point of $P$ ends at a node with $z = 0$;
3. the total length of $E$ is at most $\sum_{p \in P} p_z$.

**Notation.** For rational $x \ge 0$ let $\lceil\sqrt{x}\rceil_*$ be the rational upper bound that the code uses, so $\lceil\sqrt{x}\rceil_* \ge \sqrt{x}$. Line L18 uses $|m - p|_{xy}$ in this rounded form. Let $\Phi$ be the length of the struts in $E$ plus $\sum_{a \in A} a_z$.

**Step 1 (MERGE returns an allowed point).** Let $p_z \ge q_z$ and let $D = \|p_{xy} - q_{xy}\|$.

*Case L15:* $D \le k\,(p_z - q_z)$ (the code tests the squares, which is the same because both sides are non-negative). Then $m = q$. If $D > 0$ then $p_z - q_z \ge D/k > 0$. If $D = 0$ and $p_z = q_z$, then $p = q$, which cannot happen for two active points, because two active points never coincide (Step 3). If $D = 0$ and $p_z > q_z$, the strut is vertical. So the strut $(p, q)$ is allowed.

*Case L16 to L18:* $D > k\,(p_z - q_z) \ge 0$. Line L18 gives $m_z \le p_z - \lceil\sqrt{h_p}\rceil_*/k$ with $h_p = \|m_{xy} - p_{xy}\|^2$. So $k\,(p_z - m_z) \ge \lceil\sqrt{h_p}\rceil_* \ge \sqrt{h_p} = \|m_{xy} - p_{xy}\|$, and the same holds for $q$. It remains to show $m_z < q_z$ (and so $m_z < p_z$). If $m_{xy} \ne q_{xy}$, then $\lceil\sqrt{h_q}\rceil_* \ge \sqrt{h_q} > 0$ and $m_z \le q_z - \sqrt{h_q}/k < q_z$. If $m_{xy} = q_{xy}$, then $h_p = D^2$ and $m_z \le p_z - D/k < p_z - (p_z - q_z) = q_z$. In both cases the struts $(p, m)$ and $(q, m)$ are allowed.

**Step 2 (the saving test is exact).** In case L15 the code tests $|p - q|^2 < p_z^2$, which is $|p - q| < p_z$ because $p_z > 0$. Otherwise it tests $\sqrt{A} + \sqrt{B} < C$ with $A = |p - m|^2$, $B = |q - m|^2$ and $C = p_z + q_z - m_z$, by: $C > 0$, $d = C^2 - A - B > 0$ and $4AB < d^2$. If $\sqrt{A} + \sqrt{B} < C$, then $C > 0$, and squaring gives $A + B + 2\sqrt{AB} < C^2$, so $d > 2\sqrt{AB} \ge 0$ and $d^2 > 4AB$. Conversely, if $C > 0$, $d > 0$ and $4AB < d^2$, then $2\sqrt{AB} < d$, so $(\sqrt{A} + \sqrt{B})^2 < C^2$, and since both sides are non-negative, $\sqrt{A} + \sqrt{B} < C$. So line L19 accepts exactly the merges with $m_z > 0$ that lower $\Phi$.

**Step 3 (invariants of the loop).** Before each pass of line L3 these hold:

(a) every node in $A$ has $z > 0$ and has no strut below it, and every node not in $A$ that is an input point or a merge point has exactly one strut below it;

(b) for every node $x$, the path of struts down from $x$ ends at a node of $A$;

(c) $\Phi \le \sum_{p \in P} p_z$;

(d) no two nodes of $A$ are equal points.

At the start $A = P$ (a set, so (d) holds), $E$ is empty, and $\Phi = \sum p_z$, so all four hold. Consider a pass that does not skip at line L5, with the event $(m, p, q)$. Both $p$ and $q$ are in $A$, and the event was created by MERGE with "saves" true, so $m_z > 0$. If $m = q$ (line L7), $p$ leaves $A$ and gets the strut $(p, q)$, and $q$ stays in $A$ (lines L6 and L9 remove and add it again). If $m \ne q$ (line L8), $p$ and $q$ leave $A$ with one strut each, and $m$ is in $A$ afterwards with no strut below it: either it is a new node, or it is a node of $A$ equal to $m$, which line L8 reuses and which has no strut below it by (a). So (a) holds, and (d) holds because a point equal to a node of $A$ is never added as a new node. A path from any node that used to end at $p$ or $q$ now continues by one strut to $m$, which is in $A$, so (b) holds. By Step 2, $\Phi$ goes down in both cases: by $p_z - |p - q|$ in the first case and by $p_z + q_z - m_z - |p - m| - |q - m|$ in the second. (If $m$ is a reused node, its height was already in the sum, so the change is $|p - m| + |q - m| - p_z - q_z$, which is smaller than $-m_z < 0$.) So (c) holds. Skipped passes change nothing.

**Step 4 (termination).** Each pass that does not skip makes $|A|$ smaller by one, so at most $n - 1$ passes merge. Each of them inserts at most $|A| \le n$ events, and line L2 inserts at most $\binom{n}{2}$. Every pass extracts one event. So the loop stops after at most $\binom{n}{2} + n(n - 1)$ passes.

**Step 5 (the end).** Line L12 adds one vertical strut from each node of $A$ to a new node with $z = 0$. By (a) each node of $A$ has $z > 0$, so these struts are allowed, and every node now has at most one strut below it. By (b), the path from each input point ends at a node of $A$ and then reaches $z = 0$. The trunks add exactly $\sum_{a \in A} a_z$ to the length and empty $A$, so the final length equals the final value of $\Phi$, which is at most $\sum_{p \in P} p_z$ by (c). Together with Step 1 this proves parts 1, 2 and 3. $\blacksquare$
