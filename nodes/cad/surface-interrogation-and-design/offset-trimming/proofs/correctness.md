---
title: The sweep finds exactly the meeting segment pairs, and for the exact offset of a closed curve one test point decides each piece
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are two parts. Part A is about the polyline that the algorithm computes, and it is exact: the sweep of line L2 reports exactly the pairs of non-adjacent segments that meet, and the cuts of lines L3 to L5 split the polyline into pieces that meet only at cut points. Part B is about the exact offset curve, and it justifies lines L7 and L8: between two consecutive self-intersections, a point of the offset is either everywhere at distance $|d|$ from the curve or everywhere closer. How well the polyline follows the exact offset is a matter of sampling and is measured, not proved, on the page.

## Part A: the polyline

Let $q_0, \dots, q_{m-1}$ be the samples of line L1 and let segment $k$ join $q_k$ and $q_{k+1}$, indices modulo $m$. Two segments are adjacent if their indices differ by $1$ modulo $m$.

**Lemma A1 (the predicate).** For segments $ab$ and $ce$ of positive length that are not contained in one line, the closed segments meet if and only if $\operatorname{orient}(a, b, c)\operatorname{orient}(a, b, e) \le 0$ and $\operatorname{orient}(c, e, a)\operatorname{orient}(c, e, b) \le 0$, where $\operatorname{orient}$ is the sign of the cross product. The implementation evaluates the signs in exact rational arithmetic on the floating point coordinates, so each sign is the true sign for the sampled points.

*Proof.* If the segments meet at a point $x$, then $x$ lies on the line $ab$ and on the segment $ce$, so $c$ and $e$ are not strictly on the same side of the line $ab$, which is the first condition, and symmetrically the second. Conversely, if $ab$ and $ce$ are not parallel, the lines meet in one point $x = a + \lambda (b - a) = c + \mu (e - c)$, and $\operatorname{orient}(c, e, a)$ and $\operatorname{orient}(c, e, b)$ are the signs of the values at $a$ and $b$ of an affine function that vanishes on the line $ce$ and is linear in $\lambda$ along $ab$. The second condition says that this function does not have the same strict sign at both ends, so $0 \le \lambda \le 1$, and the first condition gives $0 \le \mu \le 1$ in the same way. If they are parallel and on different lines, then $c$ and $e$ are strictly on the same side of the line $ab$ and the first condition fails. The rounding claim holds because every float is a rational number and Fraction arithmetic is exact. $\square$

Segments of length zero are tested as points against the other segment, and pairs that lie on one line and overlap are reported as degenerate input; these are the remaining cases.

**Lemma A2 (the sweep).** The list returned in line L2 is exactly the set of pairs of non-adjacent segments that meet.

*Proof.* Every reported pair passed the test of Lemma A1, so it meets. Conversely, let segments $i$ and $j$ meet, with $j$ before $i$ in the order of their least $x$ coordinate $\ell$. They share a point, so their $x$ ranges overlap: $\ell_i \le h_j$, where $h$ is the greatest $x$ coordinate. A segment is dropped from the active list only while some segment $k$ with $\ell_k > h_j$ is processed. All segments processed before $i$ have $\ell_k \le \ell_i \le h_j$, and so does $i$, so $j$ is still active when $i$ is processed. Their $y$ ranges overlap too, so the $y$ filter does not skip the pair, and the test of Lemma A1 reports it. $\square$

**Lemma A3 (the pieces).** Cut the closed polyline at every point where one of its segments meets a non-adjacent one, as in lines L3 to L5. If two different pieces, or two non-consecutive parts of one piece, share a point, then this point is a cut point and an end point of the pieces involved.

*Proof.* Two parts of the polyline that share a point $x$ lie on segments $i$ and $j$. If $i$ and $j$ are not adjacent, Lemma A2 reports the pair, and line L4 adds $x$ as a cut on segment $i$ and as a cut on segment $j$. So $x$ is a cut point, and the pieces end there. If $i = j$ or the segments are adjacent, then either $x$ is the common vertex, where the polyline passes once, or the two segments fold back onto each other along a line. The implementation checks every vertex for this fold exactly and rejects it as degenerate input. $\square$

## Part B: the exact offset

Let $C(t)$, $t$ in a circle $\mathbb{R}/L\mathbb{Z}$, be a closed curve of class $C^3$ that is regular and simple, and orient it counterclockwise. Let $T = C'/|C'|$, let $N$ be the left unit normal, which points into the interior, and let $\kappa$ be the signed curvature, so that $T' = |C'| \kappa N$ and $\kappa > 0$ where the curve turns left. The mean curvature $H$ of surfaces does not appear. For $d \ne 0$, the raw offset is $\gamma(t) = C(t) + d N(t)$, and

$$f(t) = \operatorname{dist}(\gamma(t), C) - |d|.$$

Since $C(t)$ is at distance $|d|$ from $\gamma(t)$, $f \le 0$ everywhere. The *trimmed offset* is $\{\gamma(t) : f(t) = 0\}$.

We use one fact that we do not prove, the local form of the Jordan curve theorem for smooth curves: $\mathbb{R}^2 \setminus C$ has two components, the interior and the exterior, and for every $t$ the points $C(t) + \varepsilon N(t)$ lie in the interior and $C(t) - \varepsilon N(t)$ in the exterior for all small $\varepsilon > 0$ (do Carmo, Section 1-7).

**Assumption (G).** There is no $t$ with $d \kappa(t) = 1$ and $\kappa'(t) = 0$. That is, $|d|$ is not the radius of curvature at a vertex of $C$ on the side of the offset. This holds for all $d$ except finitely many values when $C$ has finitely many vertices.

**Lemma B1.** Assume (G). If $t_0$ is a boundary point of the open set $\{t : f(t) < 0\}$, then $\gamma(t_0) = \gamma(s)$ for some $s \ne t_0$.

*Proof.* Since $f$ is continuous and $t_0$ is a boundary point of an open set, $f(t_0) = 0$. Let $P = \gamma(t_0)$, and let $D$ be the open disc of radius $|d|$ about $P$. Then $D$ does not meet $C$, and $C(t_0)$ lies on the boundary circle of $D$. Let

$$F(t, s) = \tfrac{1}{2} |\gamma(t) - C(s)|^2.$$

*Case 1: $P$ has a second nearest point $C(s)$, $s \ne t_0$.* Then $|P - C(s)| = |d|$ and $s$ minimizes $F(t_0, \cdot)$, so $\partial_s F = -(P - C(s)) \cdot C'(s) = 0$, and $P - C(s) = \pm d N(s)$. The open disc $D$ is connected and does not meet $C$, so it lies in one component of $\mathbb{R}^2 \setminus C$. It contains $C(t_0) + \varepsilon d N(t_0)$ and $C(s) + \varepsilon (P - C(s)) = C(s) \pm \varepsilon d N(s)$ for small $\varepsilon > 0$. By the fact above, these lie in the same component only if the sign is $+$. So $P = C(s) + d N(s) = \gamma(s)$.

*Case 2: $C(t_0)$ is the only nearest point of $P$.* At $s = t$ we have $\gamma(t) - C(t) = d N(t)$, so

$$\partial_s F(t, t) = 0, \qquad \partial_s^2 F(t, t) = |C'|^2 - d N \cdot C'' = |C'(t)|^2 \left(1 - d \kappa(t)\right).$$

If $1 - d \kappa(t_0) < 0$, then $F(t_0, s) < d^2/2$ for $s \ne t_0$ near $t_0$, so $f(t_0) < 0$, which is false. If $1 - d \kappa(t_0) = 0$, then by (G) $\kappa'(t_0) \ne 0$. In an arc length parameter, $C'' = \kappa N$ and $C''' = \kappa' N - \kappa^2 T$, so $\partial_s^3 F(t_0, t_0) = 3 C' \cdot C'' - d N \cdot C''' = -d \kappa'(t_0) \ne 0$. Then $F(t_0, \cdot) - d^2/2$ changes sign at $t_0$, so again $f(t_0) < 0$, which is false. So $1 - d \kappa(t_0) > 0$. By continuity, there is an interval $U$ around $t_0$ with $\partial_s^2 F > 0$ on $U \times U$. For $t \in U$, $F(t, \cdot)$ is strictly convex on $U$ with critical point $s = t$, so $|\gamma(t) - C(s)| \ge |d|$ for all $s \in U$.

Now take $t_k \to t_0$ with $f(t_k) < 0$, and let $C(s_k)$ be a nearest point of $\gamma(t_k)$, so $|\gamma(t_k) - C(s_k)| < |d|$. A subsequence of $s_k$ converges to some $s^*$ with $|P - C(s^*)| \le |d|$, so $C(s^*)$ is a nearest point of $P$, and $s^* = t_0$. For large $k$, both $t_k$ and $s_k$ lie in $U$, and $|\gamma(t_k) - C(s_k)| \ge |d|$, a contradiction. So Case 2 cannot occur. $\square$

**Theorem B2.** Assume (G), and assume that $\gamma$ has finitely many self-intersection parameters, that is, parameters $t$ with $\gamma(t) = \gamma(s)$ for some $s \ne t$. On each open arc $I$ between two consecutive such parameters, either $f = 0$ on all of $I$ or $f < 0$ on all of $I$. So the trimmed offset is the union of the closures of the arcs on which $f$ vanishes at one point, and one test point per arc decides it.

*Proof.* The set $\{f < 0\} \cap I$ is open in $I$. By Lemma B1, it has no boundary point inside $I$, so it is also closed in $I$. Since $I$ is connected, it is empty or all of $I$. $\square$

Lines L3 to L6 cut the sampled offset at the crossing points, which approximate the self-intersections of $\gamma$, line L7 evaluates $\gamma$ itself at the middle parameter of each piece, and line L8 keeps the piece when its distance is $|d|$ up to the tolerance. By Theorem B2 this is the right decision for the exact curve, for every piece whose cuts are close to the self-intersections of $\gamma$.
