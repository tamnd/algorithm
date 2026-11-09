---
title: BUILD computes the Yao graph, which for eight cones is a 4.27-spanner containing every Euclidean minimum spanning tree
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a set of $n$ distinct points in the plane. For $k \in \{4, 8\}$ let $\theta = 2\pi/k$, and for $j = 0, \ldots, k-1$ let the cone $C_j$ be the set of nonzero vectors whose angle with the positive $x$-axis lies in $[j\theta, (j+1)\theta)$. The cones are disjoint and cover every nonzero vector. The Yao graph $Y_k$ joins each $p_i$ to a nearest point $p_j$ among those with $p_j - p_i \in C_c$, for each cone $C_c$ that contains at least one such point.

**Lemma 1 (the cone function).** For $(dx, dy) \ne (0, 0)$, `octant(dx, dy)` returns the $j$ with $(dx, dy) \in C_j$ for $k = 8$, and `cone` returns $\lfloor j/2 \rfloor$ for $k = 4$, which is the quadrant.

*Proof.* Let $\varphi \in [0, 2\pi)$ be the angle of $(dx, dy)$. The first test holds exactly when $\varphi \in [\pi, 2\pi)$, that is, $dy < 0$, or $dy = 0$ and $dx < 0$. In that case the vector is negated, which subtracts $\pi$ from the angle, and $4$ is added to the answer; cones $C_{j+4}$ are the negations of $C_j$. So it remains to treat $\varphi \in [0, \pi)$, where $dy > 0$, or $dy = 0$ and $dx > 0$. Then $\varphi < \pi/4$ exactly when $dx > 0$ and $dy < dx$; $\varphi \in [\pi/4, \pi/2)$ exactly when $dx > 0$ and $dy \ge dx$; $\varphi \in [\pi/2, 3\pi/4)$ exactly when $dx \le 0$ and $-dx < dy$; and the remaining case, $dx \le 0$ and $dy \le -dx$, is $\varphi \in [3\pi/4, \pi)$. These are the four tests of the function in order. For $k = 4$, the quadrant $[c\pi/2, (c+1)\pi/2)$ is the union of the octants $2c$ and $2c + 1$. $\square$

**Lemma 2 (BUILD is correct).** After BUILD, for each $i$ and each cone $c$, $best[c]$ is the smallest index $j$ among the points nearest to $p_i$ in cone $c$ of $p_i$ (or none if the cone is empty), and $adj$ holds exactly the undirected Yao edges.

*Proof.* Fix $i$. Line L2 empties $best$. Lines L3 to L5 scan $j$ in increasing order; by Lemma 1, line L4 finds the cone of $p_j - p_i$, and line L5 replaces $best[c]$ only by a strictly closer point. By induction on the scan, after each step $best[c]$ is the smallest index of a nearest point among those scanned in cone $c$. Line L6 adds the edge $\{i, best[c]\}$ for every nonempty cone, at both ends. Lines L7 and L8 only read $adj$. $\square$

**Termination.** The two loops of lines L1 and L3 have $n$ iterations each, and every line costs $O(1)$ plus $O(k)$ for lines L2 and L6, so BUILD takes $O(n^2 + kn)$ time.

**Lemma 3 (a step toward $q$).** Let $p, q, r$ be distinct points with $\|r - p\| \le \|q - p\|$, and let the angle $\alpha$ between $r - p$ and $q - p$ satisfy $\alpha < \theta < \pi/3$. Then $\|q - r\| \le \|q - p\| - (1 - 2 \sin(\theta/2)) \|r - p\|$, and in particular $\|q - r\| < \|q - p\|$.

*Proof.* Let $r'$ be the point on the segment $pq$ with $\|r' - p\| = \|r - p\|$. The triangle $p r r'$ is isosceles with apex angle $\alpha$ at $p$, so $\|r - r'\| = 2 \|r - p\| \sin(\alpha/2) \le 2 \|r - p\| \sin(\theta/2)$. Also $\|q - r'\| = \|q - p\| - \|r - p\|$. By the triangle inequality, $\|q - r\| \le \|q - r'\| + \|r' - r\| \le \|q - p\| - (1 - 2\sin(\theta/2)) \|r - p\|$. Since $\theta < \pi/3$, $1 - 2\sin(\theta/2) > 0$, and $\|r - p\| > 0$, which gives the strict inequality. $\square$

**Lemma 4 (stretch for $k = 8$).** Let $t = 1/(1 - 2\sin(\pi/8)) \approx 4.262$. For all $p, q \in P$, the shortest path from $p$ to $q$ in $Y_8$ has length at most $t \|p - q\|$.

*Proof.* By induction over the pairs in order of increasing distance (ties in any order). For a pair $p \ne q$, let $C$ be the cone of $p$ containing $q - p$ and $r$ the point chosen in $C$ by BUILD. Then $\|r - p\| \le \|q - p\|$, and both $r - p$ and $q - p$ lie in the half-open cone $C$ of angle $\theta = \pi/4 < \pi/3$, so the angle between them is less than $\theta$. If $r = q$, the edge $pq$ is a path of length $\|p - q\|$. Otherwise Lemma 3 gives $\|q - r\| < \|q - p\|$, so by induction there is a path from $r$ to $q$ of length at most $t \|q - r\|$, and the path that starts with the edge $pr$ has length at most
$$\|r - p\| + t \left(\|q - p\| - (1 - 2\sin(\pi/8)) \|r - p\|\right) = t \|q - p\|,$$
because $t (1 - 2 \sin(\pi/8)) = 1$. $\square$

**Lemma 5 (minimum spanning trees for $k = 8$).** Every Euclidean minimum spanning tree of $P$ is a subgraph of $Y_8$.

*Proof.* Let $pq$ be an edge of a minimum spanning tree $T$ and suppose it is not in $Y_8$. Let $r \ne q$ be the point chosen in the cone of $p$ containing $q$, so $\|r - p\| \le \|q - p\|$, and the angle at $p$ is less than $\pi/4$. By Lemma 3, $\|q - r\| < \|q - p\|$. So $pq$ is strictly the longest edge of the cycle $p, r, q$ in the complete graph. Removing $pq$ from $T$ splits it into two parts, and one of the edges $pr$ or $rq$ joins them, since $r$ lies in one part; that edge is strictly shorter than $pq$, so exchanging it gives a lighter spanning tree, a contradiction. $\square$

**Conclusion.** By Lemmas 1 and 2, BUILD stores exactly the Yao graph with the stated tie rule, and it terminates in $O(n^2)$ time. For eight cones, Lemma 4 shows it is a $t$-spanner with $t = 1/(1 - 2\sin(\pi/8))$, and Lemma 5 shows that it contains every Euclidean minimum spanning tree, so in particular it is connected. $\blacksquare$
