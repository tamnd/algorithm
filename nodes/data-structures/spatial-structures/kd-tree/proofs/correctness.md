---
title: The k-d tree operations keep the order invariant and answer range and nearest queries exactly
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode on the page. For an axis $a$, the order $<_a$ compares the superkeys $(p_a, p_{a+1}, \ldots, p_{a-1})$ lexicographically. It is a total order on $\mathbb{R}^k$, and $p <_a q$ implies $p_a \le q_a$. Write $S(t)$ for the multiset of points in the subtree of $t$.

**Invariant.** (A) A node at depth $d$ has axis $d \bmod k$. (K) At each node $t$ with axis $a$, each $p \in S(t.left)$ has $p <_a t.point$, and each $p \in S(t.right)$ has $p \ge_a t.point$.

**Lemma 1 (region).** Let (K) hold. For each node $u$, define $R(\text{root}) = \mathbb{R}^k$, $R(t.left) = R(t) \cap \{x : x_a \le t.point_a\}$ and $R(t.right) = R(t) \cap \{x : x_a \ge t.point_a\}$, where $a = t.axis$. Then $S(u) \subseteq R(u)$.

*Proof.* By induction on depth. The root is clear. A point $p$ of $S(t.left)$ is in $S(t) \subseteq R(t)$ and has $p <_a t.point$, so $p_a \le t.point_a$; the right side is the same with $\ge$. $\square$

**BUILD.** By induction on $|P|$, BUILD$(P, d)$ returns a tree on exactly the multiset $P$ in which (A) and (K) hold with depths counted from $d$. For $P = \emptyset$, line L1 returns the empty tree. Otherwise line L3 picks $m \in P$. The set of line L5 holds the points $p <_a m$, and the multiset of line L6 holds the points $p \ge_a m$ with one copy of $m$ removed; together with $m$ these are exactly $P$, and both are smaller than $P$, so the induction applies and the recursion stops. The node gets axis $d \bmod k$ and its children get depth $d + 1$, so (A) holds. Each point of the left subtree is $<_a m$ and each point of the right subtree is $\ge_a m$, so (K) holds at the new node, and below it by induction.

**INSERT.** Each pass of the loop of lines L14 to L16 moves $t$ one level down, so the loop stops after at most $h$ passes. The new node is a child of the last $t$, with axis one more than the axis of $t$ modulo $k$, so (A) holds. At each node $u$ on the path, the loop went left exactly when $p <_{u.axis} u.point$, so the new point is on the side of $u$ that (K) asks for. Nodes off the path do not change.

**FIND-MIN.** FIND-MIN$(u, a)$ returns a node whose point is least in $<_a$ over $S(u)$. By induction on the size: the candidates are $u$ and the minima of the subtrees it visits. The only subtree it skips is $u.right$ when $u.axis = a$, and then by (K) each point there is $\ge_a u.point$, so $u.point$ is at least as small. It stops since each call goes to a smaller subtree.

**DELETE.** If line L23 finds no node, nothing changes. Suppose the search reaches a node $t_0$ with point $p$. Each pass of lines L24 and L25 replaces $t.point$ by the point of a node $m$ strictly below $t$, and then works on $m$; line L26 removes a leaf. The depth of $t$ grows at each pass, so the loop stops after at most $h$ passes, and the multiset of points loses exactly one copy of $p$: the point of $t_0$ is overwritten, each copied point leaves its old node at the next pass, and the last node is removed. (A) holds, since no node changes depth except in line L25, treated below.

We show (K) holds after each pass, at every node. Fix a pass at node $t$ with axis $a$, and let $m$ be the node that FIND-MIN returns, with point $\mu$.

- *Line L24.* $\mu$ is least in $<_a$ over $S(t.right)$, so every other point that stays in the right subtree is $\ge_a \mu$. Each point of the left subtree is $<_a$ the old point of $t$, which is $\le_a \mu$ since $\mu$ came from the right subtree, so it is $<_a \mu$. So (K) holds at $t$. For an ancestor $u$ of $t$, $\mu$ moved from $S(t)$ to $t$, which are on the same side of $u$, so the constraint of $u$ on $\mu$ is unchanged. The node $m$ still holds $\mu$ for now, and the next pass treats it.
- *Line L25.* Here $t.right$ is empty. $\mu$ is least in $<_a$ over $S(t.left)$, so every point that stays in that subtree is $\ge_a \mu$. The subtree moves to the right side of $t$, at the same depth, so (A) holds, and (K) at $t$ asks exactly for $\ge_a \mu$. Inside the moved subtree nothing changed. Ancestors are as in line L24.
- *Line L26.* Removing a leaf keeps (K) everywhere.

During the passes the point $\mu$ is held by two nodes, $t$ and $m$; the next pass overwrites the point of $m$, so at the end each point is held once and (K) holds at every node.

**RANGE-SEARCH.** Let $B = \prod_i [\ell_i, h_i]$. Every point reported is in $B$ by line L9, and each node is visited at most once, since the calls follow the tree, so no point is reported twice from one node. Suppose $p \in B$ is the point of a node $v$, and let $t$ be an ancestor of $v$ with axis $a$. If $v$ is in the left subtree of $t$, then by Lemma 1 $p_a \le t.point_a$, and $\ell_a \le p_a$, so the test of line L11 holds; if it is in the right subtree, $t.point_a \le p_a \le h_a$, and the test of line L12 holds. So the search reaches $v$, and line L9 reports $p$. The search visits at most $n$ nodes and stops.

**NEAREST.** Let $q$ be the query and $d^*$ the value of the global bound. We show that at the end $best$ is a point of the tree at the least distance from $q$. The value $d^*$ only goes down and is always the distance from $q$ to $best$. Suppose a point $p^\circ$ at the least distance $\rho$ is never compared in line L18. Then some call skipped a subtree that holds it: line L22 at a node $t$ with axis $a$ decided not to search $far$, with $|\delta| \ge d^*$. The subtree $far$ is on the other side of $x_a = t.point_a$ from $q$, or on that plane, so by Lemma 1, $|q_a - p^\circ_a| \ge |\delta|$, and $\rho = \operatorname{dist}(q, p^\circ) \ge |\delta| \ge d^*$. Since $d^*$ is the distance of a point of the tree, $d^* \ge \rho$, so $d^* = \rho$, and $best$ is already a nearest point. If no skip hides $p^\circ$, line L18 compares it and $d^* \le \rho$ afterward. In both cases the final $best$ is at distance $\rho$. The calls follow the tree, so they stop. $\blacksquare$
