---
title: The shoelace sum is twice the signed area
proves: [correctness]
status: full
---

**Notation.** For points $p = (x_p, y_p)$ and $q = (x_q, y_q)$ write $p \times q = x_p y_q - x_q y_p$. This form is antisymmetric: $p \times q = -(q \times p)$, and $p \times p = 0$. For a closed polygon $P$ with vertex list $v_0, \ldots, v_{n-1}$ (indices mod $n$) write $S(P) = \sum_{i=0}^{n-1} v_i \times v_{i+1}$. Lines L2 to L5 compute $s = S(P)$, and line L6 returns $S(P)/2$. For $n < 3$ line L1 returns 0, which equals $S(P)/2$: for $n = 1$ the only term is $v_0 \times v_0 = 0$, and for $n = 2$ the terms are $v_0 \times v_1 + v_1 \times v_0 = 0$. So it remains to show what $S(P)$ is.

A simple polygon is *counterclockwise* when its interior lies to the left of each directed edge $v_i v_{i+1}$, near each point of the edge. For a simple polygon the interior lies on the same side of every edge (this follows from the [Jordan curve theorem](/jordan-curve-theorem/) for polygons), so a simple polygon is counterclockwise or clockwise, and reversing the list changes one into the other.

## Part 1: simple polygons

**Claim 1.** If $P$ is a simple counterclockwise polygon with $n \ge 3$ vertices, then $S(P) = 2 \operatorname{area}(P)$. If it is clockwise, $S(P) = -2 \operatorname{area}(P)$.

**Lemma 1 (translation).** For any point $c$, $\sum_i (v_i - c) \times (v_{i+1} - c) = S(P)$.

*Proof.* Expand by bilinearity: $(v_i - c) \times (v_{i+1} - c) = v_i \times v_{i+1} - v_i \times c - c \times v_{i+1} + c \times c$. The last term is 0. Also $- c \times v_{i+1} = v_{i+1} \times c$, so the two middle terms are $v_{i+1} \times c - v_i \times c$. Summed over the cycle $i = 0, \ldots, n-1$ they telescope to 0. $\square$

**Lemma 2 (triangle).** For a triangle $abc$, $S(abc) = \mathrm{orient}(a, b, c)$, and $|\mathrm{orient}(a, b, c)| = 2 \operatorname{area}(abc)$. The sign is positive exactly when $abc$ is counterclockwise.

*Proof.* By Lemma 1 with $c' = a$: $S(abc) = 0 \times (b - a) + (b - a) \times (c - a) + (c - a) \times 0 = (b - a) \times (c - a) = \mathrm{orient}(a, b, c)$. Let $u = b - a$ and $v = c - a$, with $u \ne 0$, and let $\theta$ be the angle from $u$ to $v$. Then $u \times v = |u|\,|v| \sin\theta$. The height of the triangle over the base $ab$ is the distance from $c$ to the line $ab$, which is $|v|\,|\sin\theta|$. So $2 \operatorname{area} = |u| \cdot |v|\,|\sin\theta| = |u \times v|$. The point $c$ is to the left of the directed line $ab$ exactly when $0 < \theta < \pi$, that is, when $u \times v > 0$; and the interior of the triangle is to the left of $ab$ exactly when $c$ is. $\square$

**Lemma 3 (splitting).** Let $v_i v_j$ be a diagonal of $P$, with $i < j$, and let $P_1 = (v_i, v_{i+1}, \ldots, v_j)$ and $P_2 = (v_j, v_{j+1}, \ldots, v_{n-1}, v_0, \ldots, v_i)$. Then $S(P) = S(P_1) + S(P_2)$.

*Proof.* The edges of $P_1$ are the edges $v_k v_{k+1}$ of $P$ for $i \le k < j$, and the closing edge $v_j v_i$. The edges of $P_2$ are the other edges of $P$, and the closing edge $v_i v_j$. So $S(P_1) + S(P_2) = S(P) + v_j \times v_i + v_i \times v_j = S(P)$ by antisymmetry. $\square$

*Proof of Claim 1.* By strong induction on $n$. For $n = 3$, $P$ is a triangle, and Lemma 2 gives the claim.

Let $n \ge 4$. Every simple polygon with at least four vertices has a diagonal; this follows from the [two ears theorem](/two-ears-theorem/), and O'Rourke proves it directly (Computational Geometry in C, Section 1.2). Take a diagonal $v_i v_j$. Its relative interior lies in the interior of $P$, so it cuts $P$ into the two simple polygons $P_1$ and $P_2$ of Lemma 3, with disjoint interiors and with $P = P_1 \cup P_2$. Each has between 3 and $n - 1$ vertices, since $v_i$ and $v_j$ are not neighbors. The diagonal has zero area, so $\operatorname{area}(P) = \operatorname{area}(P_1) + \operatorname{area}(P_2)$.

Both pieces are counterclockwise when $P$ is. Take an edge $e$ of $P$ that is an edge of $P_1$, and a point $x$ in the relative interior of $e$. A small disk around $x$ does not meet the diagonal, so its intersection with the interior of $P$ lies in the interior of $P_1$. That intersection is to the left of $e$, so the interior of $P_1$ is to the left of $e$. The interior of a simple polygon is on the same side of all its edges, so it is also to the left of the closing edge $v_j v_i$. The same argument works for $P_2$.

By the induction hypothesis $S(P_1) = 2 \operatorname{area}(P_1)$ and $S(P_2) = 2 \operatorname{area}(P_2)$, and by Lemma 3, $S(P) = 2 \operatorname{area}(P)$.

For a clockwise $P$, the reversed list $P'$ is counterclockwise, and each term of $S(P')$ is $v_{i+1} \times v_i = -(v_i \times v_{i+1})$. So $S(P) = -S(P') = -2 \operatorname{area}(P)$. $\blacksquare$

## Part 2: any closed polygon

**Winding number by a vertical ray.** Let $X$ be the finite set of the $x$-coordinates of the vertices. For an edge $e_i = v_i v_{i+1}$ with $x_i \ne x_{i+1}$, let $I_i$ be the open interval between $x_i$ and $x_{i+1}$, let $y_i(x)$ be the height of $e_i$ above $x \in I_i$, and let $\sigma_i = +1$ if $x_{i+1} > x_i$ and $\sigma_i = -1$ otherwise. For $q = (x, y)$ with $x \notin X$ and $q$ not on $P$, set

$$w(q) = \sum_{i \,:\, x \in I_i,\ y_i(x) < y} \sigma_i,$$

the signed number of edges that cross the downward vertical ray from $q$. This is the [winding number](/winding-number-algorithm/) of $P$ around $q$; for a counterclockwise unit square and a point inside, only the bottom edge, which goes to the right, crosses the ray, and $w = 1$.

**Claim 2.** $S(P) = 2 \iint w(q)\, dq$, where the integral is over the plane minus the measure-zero set of points on $P$ or with $x \in X$.

*Proof.* Expand: $(x_i - x_{i+1})(y_i + y_{i+1}) = x_i y_i + x_i y_{i+1} - x_{i+1} y_i - x_{i+1} y_{i+1}$. So

$$v_i \times v_{i+1} = (x_i - x_{i+1})(y_i + y_{i+1}) + x_{i+1} y_{i+1} - x_i y_i.$$

The last two terms telescope to 0 around the cycle, so $S(P) = \sum_i (x_i - x_{i+1})(y_i + y_{i+1})$. A vertical edge adds 0. For an edge with $x_i \ne x_{i+1}$, the trapezoid rule is exact for the linear function $y_i(x)$, so $\frac{1}{2}(x_{i+1} - x_i)(y_i + y_{i+1}) = \sigma_i \int_{I_i} y_i(x)\, dx$. Hence

$$\frac{S(P)}{2} = -\sum_i \sigma_i \int_{I_i} y_i(x)\, dx = -\int \Big( \sum_{i \,:\, x \in I_i} \sigma_i\, y_i(x) \Big)\, dx.$$

Fix $x \notin X$. First, $\sum_{i : x \in I_i} \sigma_i = 0$. The vertex $v_0$ has $x_0 \ne x$, and the sign of $x_k - x$ changes along the cycle exactly at the edges with $x \in I_i$. An edge with $\sigma_i = +1$ changes it from negative to positive, and an edge with $\sigma_i = -1$ from positive to negative. The changes alternate and the cycle returns to the sign of $x_0 - x$, so there are as many of each kind.

Now let $Y_0$ be below and $Y_1$ above all the heights $y_i(x)$. For $y < Y_0$ no edge is below $q$, so $w = 0$. For $y > Y_1$ every crossing edge is below $q$, so $w = \sum \sigma_i = 0$. Each crossing edge contributes $\sigma_i$ to $w(x, y)$ for $y$ in $(y_i(x), Y_1)$, so

$$\int_{Y_0}^{Y_1} w(x, y)\, dy = \sum_{i \,:\, x \in I_i} \sigma_i \,(Y_1 - y_i(x)) = -\sum_{i \,:\, x \in I_i} \sigma_i\, y_i(x).$$

Integrating over $x$ gives $\iint w = -\int \sum_i \sigma_i y_i(x)\, dx = S(P)/2$. $\blacksquare$

For a simple polygon, $w = \pm 1$ inside and $w = 0$ outside, so Claim 2 gives Claim 1 again; Part 1 does not need that fact.
