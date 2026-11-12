---
title: Roberts' method returns exactly the visible parts of each edge
proves: [correctness]
status: full
---

**Setting.** Each body $B$ is a convex polyhedron $\{x : f_k(x) \le 0 \text{ for all faces } k\}$ with $f_k(x) = a_k \cdot x - b_k$ and outward normals $a_k$, and its interior is $\{x : f_k(x) < 0 \text{ for all } k\}$. The viewer is the homogeneous point $e$, outside every body. For a point $p$, the line of sight is $L(p) = \{p + \alpha e : \alpha > 0\}$ in homogeneous form. For an eye point ($e_w = 1$) the homogeneous point $(p + \alpha e_{xyz}, 1 + \alpha)$ is the point $q_\alpha = (p + \alpha e_{xyz})/(1 + \alpha)$, and $\alpha$ from $0$ to $\infty$ moves $q_\alpha$ from $p$ to the eye. For a direction ($e_w = 0$) it is the point $p + \alpha e_{xyz}$. A point $p$ is hidden if some point of $L(p)$ is in the interior of some body.

**Lemma 1 (linearity).** For every face $k$ and every $\alpha \ge 0$, the sign of $f_k$ at the point of $L(p)$ with parameter $\alpha$ is the sign of $f_k(p) + \alpha f_k(e)$, where $f_k(x, w) = a_k \cdot x - b_k w$.

*Proof.* The homogeneous form is linear, so $f_k(p + \alpha e_{xyz}, 1 + \alpha e_w) = f_k(p, 1) + \alpha f_k(e)$. The Cartesian point is this homogeneous point divided by its last coordinate $1 + \alpha e_w > 0$, and $f_k$ of the Cartesian point is the homogeneous value divided by that positive number. $\square$

**Lemma 2 (self-hiding).** Let $p$ be a point in the relative interior of an edge of $B$ with faces $k_1$ and $k_2$. Then $L(p)$ meets the interior of $B$ if and only if $f_{k_1}(e) < 0$ and $f_{k_2}(e) < 0$.

*Proof.* At $p$, $f_{k_1}(p) = f_{k_2}(p) = 0$ and $f_k(p) < 0$ for every other face, because $p$ lies inside the edge. If both $f_{k_1}(e)$ and $f_{k_2}(e)$ are negative, then by Lemma 1 for small $\alpha > 0$ all values are negative: the two face values are $\alpha f_{k_i}(e) < 0$, and the others stay negative by continuity. So $L(p)$ meets the interior. Conversely, suppose $f_{k_1}(e) \ge 0$. Then $f_{k_1}(p) + \alpha f_{k_1}(e) = \alpha f_{k_1}(e) \ge 0$ for every $\alpha > 0$, so by Lemma 1 no point of $L(p)$ satisfies $f_{k_1} < 0$, and none is in the interior. $\square$

So line L4 removes exactly the edges whose points are hidden by their own body. For an edge with at least one face toward the viewer, its own body hides none of its inner points, and for its endpoints the same holds by the argument of the converse part, because the converse uses only $f_{k_1}(p) = 0$.

**Lemma 3 (hiding by another body).** Fix an edge $p(t) = p_0 + t (p_1 - p_0)$, $t \in [0, 1]$, and a body $B_j$. Let $U = \{(t, \alpha) : 0 \le t \le 1,\ \alpha > 0,\ g_k(t, \alpha) < 0 \text{ for all } k\}$ with $g_k(t, \alpha) = f_k(p_0) + t f_k(p_1 - p_0) + \alpha f_k(e)$. Then $p(t)$ is hidden by $B_j$ if and only if $(t, \alpha) \in U$ for some $\alpha$.

*Proof.* By Lemma 1 with $p = p(t)$, and because $f_k(p(t)) = f_k(p_0) + t f_k(p_1 - p_0)$ by linearity (with $w = 0$ for the difference $p_1 - p_0$), the point of $L(p(t))$ with parameter $\alpha$ is in the interior of $B_j$ exactly when all $g_k(t, \alpha) < 0$. $\square$

**Lemma 4 (the bound on $\alpha$).** Let $k$ be a face of $B_j$ with $f_k(e) > 0$; one exists because $e$ is outside $B_j$ (for $e_w = 1$, the eye violates some inequality; for $e_w = 0$, a bounded body has a face whose normal has a positive component along the direction $e_{xyz}$). If $\alpha > \alpha_{\max} = \max(-f_k(p_0), -f_k(p_1)) / f_k(e)$, then $g_k(t, \alpha) > 0$ for all $t \in [0, 1]$.

*Proof.* $g_k(t, \alpha)$ is linear in $t$, so for $t \in [0, 1]$ it is at least $\min(f_k(p_0), f_k(p_1)) + \alpha f_k(e)$, which is positive when $\alpha > \alpha_{\max}$. $\square$

So $U$ lies in the rectangle $R = [0, 1] \times [0, \alpha_{\max}]$ of line L7, and the polygon $Q$ of lines L8 and L9 is $Q = R \cap \{g_k \le 0 \text{ for all } k\}$, a convex polygon.

**Lemma 5.** Let $C = \{(t, \alpha) : 0 < t < 1,\ \alpha > 0,\ g_k(t, \alpha) < 0 \text{ for all } k\}$, the part of $U$ with $0 < t < 1$. If $Q$ has zero area, then $C$ is empty. If $Q$ has positive area, then the projection of $C$ on the $t$ axis is the open interval $(t_{\min}, t_{\max})$, where $t_{\min}$ and $t_{\max}$ are the least and greatest $t$ of $Q$.

*Proof.* By Lemma 4, every point of $C$ has $\alpha < \alpha_{\max}$, because at $\alpha \ge \alpha_{\max}$ the value $g_k$ of the chosen face is at least 0. So $C$ is the intersection of the open half-planes $t > 0$, $t < 1$, $\alpha > 0$, $\alpha < \alpha_{\max}$ and $g_k < 0$, and $Q$ is the intersection of the same half-planes, closed. For finitely many half-planes, if the open intersection is not empty, then the closed intersection is its closure, and the open intersection is the interior of the closed one. So if $C$ is not empty, $Q$ is the closure of a nonempty open set and has positive area; this proves the first claim. If $Q$ has positive area, its interior is not empty. A point of $Q$ on the boundary line of one of the half-planes is a boundary point of $Q$, because $Q$ lies on one side of that line. So an interior point of $Q$ satisfies all the strict inequalities, and $C$ is not empty. Then $C$ is the interior of $Q$. The projection of the interior of a convex polygon of positive area on the $t$ axis is the open interval between its least and its greatest $t$. $\square$

**Theorem.** For each edge, the output of line L11 is the set of visible points of the edge, up to the finitely many endpoints of the intervals.

*Proof.* If both faces of the edge face away, Lemma 2 shows that the whole edge is hidden by its own body, and line L4 outputs nothing. Otherwise its own body hides no point of it (Lemma 2 and the remark after it). By Lemma 3 and Lemma 5, for $t \in (0, 1)$ the point $p(t)$ is hidden by $B_j$ exactly when $t$ lies in the open interval that line L10 adds to $H$ for $B_j$, or nothing if $Q$ has zero area. A point is visible exactly when no body hides it, so the visible points with $0 < t < 1$ are those outside every interval of $H$, which is what line L11 returns. The only points where the output and the visible set can differ are the endpoints of the intervals and $t = 0, 1$, where the output is closed. $\square$

**Running time.** Line L2 evaluates each face once. For an edge and a body with $f_j$ faces, each clip by a half-plane keeps a convex polygon and adds at most one corner, so $Q$ has at most $4 + f_j$ corners and the $f_j$ clips cost $O(f_j (4 + f_j)) = O(f_j^2)$. Summed over the bodies this is at most $O(f n)$ for one edge, and line L11 sorts at most $m$ intervals. Over at most $n$ edges the time is $O(n^2 (f + \log n))$. $\square$
