---
title: The 2D expanding polytope algorithm brackets the penetration depth and terminates on polygons
proves: [correctness, termination]
status: full
---

Let $A$ and $B$ be convex polygons and $M = A - B = \{a - b : a \in A, b \in B\}$, a convex polygon. The support function of $M$ is $h_M(u) = \max_{x \in M} u \cdot x = h_A(u) + h_B(-u)$, and a support point of $M$ in the direction $u$ is $s_A(u) - s_B(-u)$. Use exact arithmetic. The penetration depth is $\delta = \min \{ |t| : (A + t) \cap B \text{ has no interior point} \}$. Since $(A + t) \cap B \neq \emptyset$ exactly when $-t \in M$, $\delta$ is the distance from the origin to the boundary of $M$ when the origin is in $M$.

**Lemma 1 (the depth is the smallest support value).** If $0 \in M$, then $\delta = \min_{|u| = 1} h_M(u)$, and $A$ moved by $-h_M(u)\,u$ touches $B$ without overlap.

*Proof.* Let $z$ be a point of $\partial M$ closest to the origin, so $|z| = \delta$. There is a supporting line of $M$ at $z$ with a unit normal $u$, so $h_M(u) = u \cdot z \le |z| = \delta$. Conversely, the open disc of radius $\delta$ about the origin is inside $M$, so for each unit $u$ the point $\delta u$ is in the closure of $M$ and $h_M(u) \ge \delta$. For the second claim, $(A - s u) - B = M - s u$, and with $s = h_M(u)$ every point $x$ of it has $u \cdot x \le 0$, with equality on a face. So the origin is on the boundary of $M - s u$. $\square$

**The start.** The GJK stage returns a triangle $T_0$ with three properties. Its vertices are support points of $M$ for nonzero directions. It is counterclockwise and not degenerate. It contains the origin. The last two are the exit tests of the GJK stage: the code returns the triangle only when the cross product is not zero (it reorders it to counterclockwise), and when the origin is on the inner side of the two new edges, and on the inner side of the old edge, because the new vertex and the origin are on the same side of the old edge with respect to the search direction. The termination of the GJK stage is a property of GJK and is not proved here. The code also stops it after a fixed number of rounds.

**Invariant.** Let $P$ be the polygon of EPA at the start of a round. Then:

1. $P$ is a convex polygon in counterclockwise order, possibly with collinear vertices, and no two of its vertices are equal;
2. each vertex $v$ of $P$ is a support point of $M$ for a nonzero direction $d_v$;
3. $0 \in P \subseteq M$.

*Proof.* The start triangle has the three properties. Suppose $P$ has them, line L4 picks the edge $pq$ with the outward unit normal $n$ and the distance $r = n \cdot p$, and line L5 gets the support point $t$ with $n \cdot t > r + \varepsilon \ge r$. Line L7 puts $t$ between $p$ and $q$. Property 2 holds for $t$ with $d_t = n$, and $t \in M$, so $P' \subseteq M$ by the convexity of $M$, and $0 \in P \subseteq P'$. It remains to show that $P'$ is convex.

The point $t$ is strictly beyond the line of $pq$, so the turn $p \to t \to q$ is to the left, and $t$ differs from all vertices of $P$, which are on the inner side of that line. Let $o$ be the vertex before $p$, with the edge normal $n'$. Suppose $t$ is strictly beyond the line of $op$ too. The direction $d_p$ is in the normal cone of $P$ at $p$, because $p$ maximizes $d_p \cdot x$ over $M \supseteq P$. So $d_p = \alpha n' + \beta n$ with $\alpha, \beta \ge 0$, not both zero. Then $d_p \cdot (t - p) = \alpha\, n' \cdot (t - p) + \beta\, n \cdot (t - p) > 0$, which contradicts that $p$ is a support point in the direction $d_p$. So $t$ is on the inner side of the line of $op$ or on it, and the turn $o \to p \to t$ is to the left or straight. The same argument at $q$ shows that the turn $t \to q \to r$ is to the left or straight. All other turns are unchanged. So $P'$ is convex. $\square$

**Lemma 2 (the bracket).** In each round, $r \le \delta$. When line L6 stops the loop, $r \le \delta \le r + \varepsilon$.

*Proof.* The origin is in the convex polygon $P$, so its distance to $\partial P$ is the smallest distance to the line of an edge, which is $r$. Because $P \subseteq M$, a disc about the origin that is inside $P$ is also inside $M$, so $r \le \delta$. At the stop, the support point $t$ in the direction $n$ has $h_M(n) = n \cdot t \le r + \varepsilon$, and by Lemma 1, $\delta \le h_M(n) \le r + \varepsilon$. $\square$

**Lemma 3 (the witness).** At the stop, the returned points $p_A$ and $p_B$ are in $A$ and $B$, and $p_A - p_B = r\,n$. If $\varepsilon = 0$, then moving $A$ by $r$ along the returned normal $-n$ makes $A$ and $B$ touch without overlap.

*Proof.* Each vertex of $P$ is stored as a triple $(w, a, b)$ with $w = a - b$, $a \in A$ and $b \in B$. The foot of the perpendicular from the origin to the line of $pq$ is $r\,n$. It lies on the segment $pq$: otherwise the segment from the origin to it would leave $P$ through another edge, and that edge would have a smaller distance than $r$. So $\lambda \in [0, 1]$, the clamp does nothing, and $r\,n = (1 - \lambda) w_p + \lambda w_q = p_A - p_B$ with $p_A = (1 - \lambda) a_p + \lambda a_q \in A$ and $p_B = (1 - \lambda) b_p + \lambda b_q \in B$ by convexity. With $\varepsilon = 0$, Lemma 2 gives $h_M(n) = r = \delta$, and Lemma 1 gives the touching. $\square$

**Theorem (termination on polygons).** If $A$ and $B$ are polygons with $n$ and $m$ vertices and the support functions return vertices, EPA stops after at most $nm$ rounds, for every $\varepsilon \ge 0$.

*Proof.* Every support point of $M$ that the code can return is a difference $a - b$ of a vertex of $A$ and a vertex of $B$, so there are at most $nm$ of them. Each round that does not stop inserts a point that is not yet a vertex of $P$ (by the invariant), and no vertex is ever removed. So there are fewer than $nm$ insertions, and the round after the last insertion stops. $\blacksquare$

**Remarks.** For curved shapes, such as discs, the set of support points is infinite, and the termination needs $\varepsilon > 0$. This proof does not cover that case. The implementation bounds the number of rounds and raises an error. In floating point, the signs in the invariant can be wrong for nearly parallel edges, and then the polygon can lose its convexity. This is the reason for the tolerance in practice, not only for curved shapes.
