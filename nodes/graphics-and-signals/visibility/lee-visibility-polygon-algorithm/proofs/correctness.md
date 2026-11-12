---
title: The corrected scan returns the visibility polygon and runs in linear time
proves: [correctness]
status: sketch
---

This is a proof sketch. It gives the invariant, the reason why each state keeps it, and the full time bound. The complete case analysis, including the degenerate cases where $z$ is collinear with two vertices, is in the paper of Joe and Simpson (1987).

**Setting.** $P$ is a simple polygon with counterclockwise boundary $\partial P$, and $z$ is a point strictly inside $P$. For the sketch we assume general position: $z$ is not on the line through two vertices of $P$. A point $q \in \partial P$ is visible if the segment $zq$ lies in $P$. For each direction $\theta$ the ray from $z$ in direction $\theta$ leaves $P$, because $P$ is bounded; the first point of $\partial P$ on it is the only visible point of $\partial P$ in that direction. So $\partial V(z)$ is the curve of first hits, and it is traced once when $\theta$ goes once around.

**The angle with winding.** Walk along $\partial P$ from $v_0$ and let $\alpha(q)$ be the angle of $q - z$ measured from the direction of $v_0 - z$, made continuous along the walk (the angle is not reduced modulo $2\pi$). So $\alpha(v_0) = 0$ at the start, and $\alpha = 2\pi$ when the walk returns to $v_0$, because $z$ is inside $P$ and the boundary winds once around it.

**Lemma 1.** The start point $v_0$ is visible, and a visible point $q$ satisfies $0 \le \alpha(q) < 2\pi$, or $q = v_0$ at the end of the walk.

*Proof.* $v_0$ is the first point of $\partial P$ on the ray up from $z$, so $z v_0$ lies in $P$. Let $q$ be visible with $q \ne v_0$. The segments $z v_0$ and $z q$ lie in $P$ and meet $\partial P$ only at their far ends (in general position). The chain of $\partial P$ from $v_0$ to $q$, with these two segments, is a closed curve through $z$ that does not cross itself. The chain does not meet the open segment $z q$, so its angle cannot pass the direction of $q$ at a point nearer to $z$ than $q$; and it does not meet the open segment $z v_0$. A chain that starts at angle 0 and first reaches the direction of $q$ at $q$ itself has $\alpha(q) \in (0, 2\pi)$ unless it went once around $z$ outside the segment $z v_0$; in that case the rest of the boundary, from $q$ back to $v_0$, would have to cross the closed curve, which is not possible for a simple boundary. $\square$

So only the part of the boundary with $0 \le \alpha < 2\pi$ can be visible. Lee's 1983 rules compare angles only locally, and they do not detect that $\alpha$ has passed $2\pi$. Lines L32 and L33 detect exactly this: the top edge of the stack crosses the ray $z v_0$ from right to left, which is the step where $\alpha$ passes $2\pi$.

**The invariant.** Let $C_i$ be the chain $v_0 v_1 \dots v_i$. Let $V_i$ be the set of first hits of rays from $z$ with directions in $[0, 2\pi)$ when $C_i$ is the only obstacle, and only the points of $C_i$ with $0 \le \alpha < 2\pi$ count. At the start of a step in state LEFT or RIGHT:

1. the stack $s_0, \dots, s_t$ lists the vertices of $V_i$ in increasing angle, with $s_0 = v_0$ and $s_t = v_i$;
2. two consecutive stack points are joined either by a piece of an edge of $C_i$ or by a window, a segment on one ray from $z$ that joins a visible vertex to the point behind it where its ray hits $C_i$ again.

At the start of a step in a scan state, part 1 holds for the chain up to the last visible point, and the chain after it lies in a region closed off by a window: the ray from $z$ through $s_t$ beyond $s_t$ (SCANA), the segment $s_t v_0$ (SCANB), or the segment $s_t w$ (SCANC and SCAND).

**Lemma 2.** Each state keeps the invariant.

*Proof sketch.*
- *LEFT, line L8.* The edge $v_i v_{i+1}$ turns counterclockwise around $z$, so each of its points has a larger angle than $s_t = v_i$. All earlier stack points have smaller angles, so the edge hides none of them and is itself the first hit in its directions among $C_{i+1}$. Pushing $v_{i+1}$ keeps parts 1 and 2.
- *LEFT, line L9.* The edge turns clockwise around $z$ and to the right of the line from $s_{t-1}$ through $v_i$. Then the edge goes behind the chain that ends at $v_i$: its points have angles at most $\alpha(v_i)$ and lie farther from $z$ than the stack points in those directions. The boundary can come into view again only by crossing the ray from $z$ through $s_t$ beyond $s_t$. This is the region of SCANA.
- *LEFT, line L10.* The edge turns clockwise and to the left of that line, so it comes toward $z$ in front of the stack. The points of the stack that it hides are those at the top whose angle is above $\alpha(v_{i+1})$ and which lie behind the edge. This is RIGHT.
- *RIGHT, lines L12 to L18.* The stack is in angular order, so the points hidden by the edge $v_{i-1} v_i$ are a top part of the stack. Line L12 pops them. It stops either where the ray from $z$ through $v_i$ passes between two stack points, so the new window ends at the point $u$ where this ray meets the stack segment (lines L15 to L18), or where the edge crosses a window of the stack, so the boundary goes behind that window (line L13, then SCAND). In lines L16 and L17 the turn at $v_i$ decides whether the boundary goes on in view (LEFT) or away from $z$ behind the new window (SCANC).
- *Scan states, lines L20 to L31.* While the boundary is behind a window, its points are not first hits, because the window and the chain before it block their rays. The boundary is a closed curve without crossings, so it can come back into view only by crossing the window. The first edge that crosses it gives the next visible point $u$, which is pushed (or, for SCANC, the scan continues in RIGHT from it).
- *Line L32.* If the top edge crosses the ray from $z$ through $v_0$ from right to left, its end has $\alpha \ge 2\pi$. By Lemma 1 the boundary after it cannot be visible until it comes back through the window from the crossing point $y$ to $v_0$, which is what SCANB waits for. $\square$

**Theorem.** The algorithm returns $V(z)$.

*Proof.* When the scan reaches $v_m = v_0$, the chain $C_m$ is all of $\partial P$. By Lemma 1 the points of $\partial P$ with $\alpha \ge 2\pi$ are not visible, so $V_m$ is the set of first hits of all rays from $z$ against $\partial P$, which is $\partial V(z)$. By the invariant the stack lists its vertices in angular order, which for a star-shaped polygon with $z$ in its kernel is the counterclockwise order. $\square$

**Theorem.** The algorithm runs in $\Theta(n)$ time and uses $O(n)$ extra space.

*Proof.* Each step either ends the loop, advances $i$, or (in RIGHT) pops at least one point and then advances $i$ or enters SCAND. A scan examines each edge from index $i$ to $k$ once and then sets $i \leftarrow k + 1$. So the work outside the pops is $O(1)$ per value of $i$, and $i \le m \le n + 1$. Each step pushes at most two points (L16 pushes $v_i$ and $v_{i+1}$ after replacing a point; L21 and L31 push $u$ and $v_{k+1}$). A popped point is not pushed again, so the number of pops is at most the number of pushes, at most $2m + 2$. Each test is a constant number of orientation tests or one segment intersection. So the time is $O(n)$. It is also $\Omega(n)$, because each vertex must be read. The stack never holds more points than were pushed, so the space is $O(n)$. $\square$
