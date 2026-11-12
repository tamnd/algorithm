---
title: GPSR uses a local planar subgraph, never loops forever, and delivers when its face changes are exits
proves: [correctness]
status: partial
---

**Setting.** The nodes are points in the plane in general position: no three on a line, no four on a circle, and all distances distinct. Nodes $u$ and $v$ are neighbors in the unit disk graph $U$ when $|uv| \le r$. The *Gabriel graph* $GG$ keeps the edge $uv$ of $U$ unless some node $w$ has $|uw|^2 + |vw|^2 < |uv|^2$, that is, lies inside the circle with diameter $uv$. The *relative neighborhood graph* $RNG$ keeps $uv$ unless some $w$ has $\max(|uw|, |vw|) < |uv|$.

**Theorem 1 (local, planar, connected).**

1. Each node can decide which of its edges are in $GG$ and in $RNG$ from the positions of its neighbors alone.
2. $RNG \subseteq GG \subseteq U$.
3. $GG$, hence $RNG$, is planar: no two of its edges cross.
4. Every minimum spanning tree of each component of $U$ lies in $RNG$. So $RNG$ and $GG$ have the same components as $U$.

*Proof.* (1) A witness $w$ for either test has $|uw| < |uv| \le r$, so $w$ is a neighbor of $u$ (and of $v$). Node $u$ only needs the positions of its neighbors, and $u$ and $v$ reach the same decision.

(2) If $|uw|^2 + |vw|^2 < |uv|^2$, then both $|uw|$ and $|vw|$ are less than $|uv|$, so a Gabriel witness is also an $RNG$ witness, and every edge removed from $GG$ is removed from $RNG$.

(3) Suppose the edges $uv$ and $wx$ of $GG$ cross. Their endpoints are the corners of a convex quadrilateral $u, w, v, x$ whose diagonals are $uv$ and $wx$. Its four angles add up to $2\pi$, so one of them is at least $\pi/2$, and by general position greater than $\pi/2$. If it is the angle at $w$ or $x$, say $\angle u w v > \pi/2$, then $w$ lies inside the circle with diameter $uv$, so $|uw|^2 + |vw|^2 < |uv|^2$, and $w$ removes $uv$ from $GG$. If it is the angle at $u$ or $v$, the same argument removes $wx$. Either way one of the edges is not in $GG$.

(4) Let $T$ be a minimum spanning tree of a component of $U$, with edge $uv \in T$, and suppose a node $w$ has $\max(|uw|, |vw|) < |uv|$. Then $uw$ and $vw$ are edges of $U$. Removing $uv$ splits $T$ into two parts; $w$ lies in one of them, so one of $uw$ and $vw$ joins the two parts again. Replacing $uv$ by it gives a spanning tree of smaller weight, a contradiction. So $T \subseteq RNG \subseteq GG$, and since $GG \subseteq U$ the components are the same. $\square$

**Theorem 2 (termination).** Every packet is delivered or dropped after finitely many hops.

*Proof.* A greedy hop moves the packet to a node strictly closer to $D$, so a run of greedy hops visits each node at most once. A perimeter phase starts at a node $L_p$ and ends when the packet reaches a node closer to $D$ than $L_p$. A new perimeter phase can only start at a node reached in greedy mode, which is closer to $D$ than the previous $L_p$, so the values $|L_p D|$ of successive phases strictly decrease, and there are at most $n$ phases.

Inside one phase, the point $L_f$ moves along the segment $L_p D$, and each face change moves it to a crossing point of an edge with that segment strictly closer to $D$. There are finitely many edges, so finitely many face changes. Between two face changes the packet follows the right-hand rule on one face. The rule is a permutation of the directed edges (each directed edge into $x$ determines the next directed edge out of $x$), so the walk is periodic and comes back to its first edge $e_0$ after finitely many hops; the second arrival at $e_0$ drops the packet. So each phase is finite. $\square$

**Theorem 3 (delivery under exit changes).** Assume the planar subgraph is connected, and that every face change happens at an *exit*: an edge $x \to z$ that the segment $L_p D$ crosses from the face being walked to the other side, which in the right-hand convention means that $D$ is to the left of $x \to z$. Then GPSR delivers every packet.

*Proof.* With the right-hand rule as stated (the next edge counterclockwise from the edge of arrival), the face being walked lies to the right of every directed edge the packet takes, and after a face change at $x \to z$ the new face is the one to the left of $x \to z$.

We show that throughout a perimeter phase, the points of the segment $L_p D$ just beyond $L_f$, toward $D$, lie in the face being walked. At the start, $L_f = L_p$, and the first edge is the first one counterclockwise from the ray toward $D$; so the ray toward $D$ lies in the angle between that edge and the edge before it, which is a corner of the face being walked. After a face change at an exit $x \to z$ crossing the segment at $p$, the segment passes from the right of $x \to z$ to its left at $p$, so the points just beyond $p$ are in the face to the left, which is the new face, and $L_f = p$.

Now suppose the packet is dropped. Then the walk went once around the whole boundary of the current face $F$ with no face change. Let $q$ be a point of the segment just beyond $L_f$, in $F$. The node $D$ is not in the interior of $F$, since faces contain no nodes. So the segment from $q$ to $D$ meets the boundary of $F$ at some point $p'$ with $|p' D| < |L_f D|$. By general position $p'$ is not a node other than $D$. If $p' = D$, then $D$ is on the boundary of $F$, the walk reaches $D$, and the packet is delivered, not dropped. Otherwise $p'$ is an interior point of a boundary edge of $F$, crossed by the segment from inside $F$ to outside, that is, an exit closer to $D$ than $L_f$. The walk takes this edge, in the direction that has $F$ on its right, and the face change test fires there. This contradicts the assumption that no face change happened. So no packet is dropped, and by Theorem 2 every packet is delivered. $\square$

**What is not proved here.** GPSR as published changes faces at the first edge whose crossing with $L_p D$ is closer to $D$ than $L_f$, without checking the side. If the walk meets a crossing where the segment *enters* the current face before it meets the exit, the face change goes to the wrong side, and the argument above does not apply. Frey and Stojmenovic (2006) studied such failures of face routing variants and how to avoid them; we have not checked their analysis against this exact rule. The tests run the published rule on random unit disk graphs (12 random graphs with 60 nodes, both planar subgraphs, every connected pair from a quarter of the sources) and every packet was delivered, which is evidence, not proof.
