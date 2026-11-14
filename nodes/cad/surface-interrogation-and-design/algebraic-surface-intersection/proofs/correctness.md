---
title: The subdivision of the substituted polynomial loses no piece of the intersection, pairs the boundary points of each monotone box correctly, and stops near every regular point
proves: [correctness]
status: full
---

Let $r$ be a polynomial patch of bidegree $(m, n)$ on $\Omega = [0, 1]^2$ and let $f$ be a polynomial of degree $k$. Then $g = f \circ r$ is a polynomial of bidegree at most $(km, kn)$, and line L1 writes it in tensor product Bernstein form,

$$g(u, v) = \sum_{i = 0}^{M} \sum_{j = 0}^{N} G_{ij} \, B_{i, M}(u) \, B_{j, N}(v), \qquad M = km, \; N = kn,$$

exactly, with rational coefficients. On a box $Q = [u_0, u_0 + h] \times [v_0, v_0 + h]$ the coefficients $G^Q_{ij}$ are those of $g$ in the local coordinates $s = (u - u_0)/h$, $t = (v - v_0)/h$. Line L7 obtains them by de Casteljau halving, which replaces each list of coefficients by averages of its entries, so every coefficient on $Q$ is a convex combination of the coefficients on $\Omega$. Write $Z = \{x \in \Omega : g(x) = 0\}$.

**Claim 1 (the convex hull bound).** For every $x \in Q$, $\min_{ij} G^Q_{ij} \le g(x) \le \max_{ij} G^Q_{ij}$. So a box excluded by line L4 holds no point of $Z$.

*Proof.* The Bernstein polynomials are nonnegative on $[0, 1]$ and sum to $1$, since $\sum_i B_{i, M}(s) = (s + (1 - s))^M = 1$. So the products $B_{i, M}(s) B_{j, N}(t)$ are nonnegative and sum to $1$, and $g(x)$ is a convex combination of the $G^Q_{ij}$. If all of them are positive, so is $g$ on $Q$, and the same for negative. $\square$

**Claim 2 (the monotone test).** The differences $G^Q_{i, j+1} - G^Q_{ij}$, which line L5 tests, are $\frac{h}{N}$ times the Bernstein coefficients of degree $(M, N - 1)$ of $g_v$ on $Q$. So if they all have one strict sign, $g_v$ has that sign on all of $Q$. The same holds for $u$.

*Proof.* Differentiating $B_{j, N}(t)$ gives $N (B_{j - 1, N - 1}(t) - B_{j, N - 1}(t))$, and collecting terms gives $\partial_t \sum_{ij} G^Q_{ij} B_{i, M} B_{j, N} = N \sum_{i, j} (G^Q_{i, j+1} - G^Q_{ij}) B_{i, M} B_{j, N - 1}$. Since $\partial_t = h \, \partial_v$, the first statement follows, and Claim 1 applied to $g_v$ gives the second. $\square$

**Claim 3 (the arcs of a monotone box).** Let $g_v$ have a strict sign on $Q$, and assume that every root of $g$ on the bottom and top edges of $Q$ is simple and that no point of $Z$ is a corner of $Q$ at which $Z$ does not enter $Q$. Sort the points of $Z$ on the boundary of $Q$ by $u$, as line L6 does, into $p_1, p_2, \dots, p_{2q}$. Then $Z \cap Q$ consists of exactly $q$ disjoint arcs, the $\ell$th from $p_{2\ell - 1}$ to $p_{2\ell}$, and each is the graph $v = \varphi(u)$ of a continuous function over the interval between the $u$ values of its ends. The same holds with $u$ and $v$ exchanged.

*Proof.* Let $Q = [u_0, u_1] \times [v_0, v_1]$ and say $g_v > 0$. For each $u$ the function $v \mapsto g(u, v)$ is strictly increasing, so it has at most one zero in $[v_0, v_1]$, and it has one exactly when $g(u, v_0) \le 0 \le g(u, v_1)$. Let $U$ be the set of such $u$ and $\varphi(u)$ the zero. By the implicit function theorem, which applies because $g_v \ne 0$, $\varphi$ is continuous on $U$, and $Z \cap Q$ is the graph of $\varphi$ over $U$.

The set $U$ is defined by two polynomial inequalities, so it is a finite union of disjoint closed intervals $[a_1, b_1], \dots, [a_q, b_q]$ with $a_1 \le b_1 < a_2 \le \dots$. Over each interval the graph is an arc, and its two ends are its points at $u = a_\ell$ and $u = b_\ell$. An end at $u = a_\ell > u_0$ is a point where $g(u, v_0)$ or $g(u, v_1)$ changes sign, so it is a root on the bottom or top edge, and conversely a simple root on the bottom or top edge is such a change of sign, so it is an end. An end at $u = u_0$ is the zero of $g$ on the left edge, and the same at $u_1$. The assumption on the corners excludes $a_\ell = b_\ell$, which would be an isolated point of $Z \cap Q$ at a corner. So the boundary points of $Z$ on $Q$ are exactly the $2q$ ends, their $u$ values are $a_1 < b_1 < a_2 < b_2 < \dots$, and two ends never share a $u$ value, because a line $u = \text{const}$ meets $Z \cap Q$ at most once. Sorting by $u$ and pairing neighbors gives the arcs. $\square$

The tracing of line L6 computes, for $u$ values between the ends of an arc, the zero $\varphi(u)$ by bisection on the monotone function $v \mapsto g(u, v)$. So every vertex of the output lies on $Z$ to the bisection tolerance, and since $Q$ is convex, every edge of the polyline lies in $Q$, as does the arc it replaces. The distance between them is at most the diagonal of $Q$, which is all that is proved about it.

**Claim 4 (nothing is lost).** Every point of $Z$ lies in a box excluded by no test, that is, in a monotone box handled by line L6 or in a box of line L8. Under the assumptions of Claim 3 on every monotone box, the arcs of line L6 together with the boxes of line L8 cover $Z$, and line L9 chains the arcs into the components of $Z$ outside the boxes of line L8.

*Proof.* The leaves of the subdivision cover $\Omega$. A leaf is excluded only by line L4, which holds no point of $Z$ by Claim 1. In a monotone leaf, Claim 3 gives all of $Z$ there as arcs. A point where two leaves meet that is on $Z$ is the end of an arc in each leaf that $Z$ enters, so the arcs that share an end are consecutive pieces of one component, and line L9 joins them. A closed component of $Z$ is cut by the leaves into arcs whose ends join in a cycle, so it is returned as a closed curve, however small it is. $\square$

**Claim 5 (termination near regular points).** Let $L_u$ and $L_v$ be the largest absolute values of the Bernstein coefficients of $g_u$ and $g_v$ on $\Omega$, and put $K_0 = 2 (L_u + L_v)$. Define $K_u$ and $K_v$ the same way from the second derivatives. If a box of side $h$ is split, then at every point $x$ of it,

$$|g(x)| \le K_0 h, \qquad |g_u(x)| \le K_u h, \qquad |g_v(x)| \le K_v h.$$

Hence, if $Z$ has no singular point in $\Omega$, that is, no point where $g = g_u = g_v = 0$, the number $\mu = \min_{x \in \Omega} \max(|g| / K_0, |g_u| / K_u, |g_v| / K_v)$ is positive, and no box of side less than $\mu$ is split, except for a box rejected at line L6 by the assumptions of Claim 3.

*Proof.* On $Q$, by Claim 2, $|G^Q_{i+1, j} - G^Q_{ij}| = \frac{h}{M} |c_{ij}|$, where $c_{ij}$ is a coefficient of $g_u$ on $Q$, a convex combination of the coefficients on $\Omega$, so $|c_{ij}| \le L_u$. The same holds in $v$. Walking from $G^Q_{00}$ to $G^Q_{ij}$ in at most $M$ steps in $i$ and $N$ steps in $j$ gives $|G^Q_{ij} - G^Q_{00}| \le h (L_u + L_v)$. Since $G^Q_{00} = g(u_0, v_0)$ and $|g_u| \le L_u$, $|g_v| \le L_v$ on $\Omega$ by Claim 1, $|g(x) - g(u_0, v_0)| \le h (L_u + L_v)$ for $x \in Q$. So every coefficient is within $K_0 h$ of $g(x)$. If $g(x) > K_0 h$, all coefficients are positive and line L4 excludes $Q$, and the same for $g(x) < -K_0 h$. The same argument for $g_u$ and $g_v$ shows that if $|g_v(x)| > K_v h$ or $|g_u(x)| > K_u h$, line L5 finds a strict sign. A box that is split therefore has all three bounds at every point. If $h < \mu$, some point of the box has one of the three ratios above $h$, a contradiction. The minimum is attained because $\Omega$ is compact, and it is $0$ exactly at a singular point of $Z$. $\square$

So, with no singular point and no tangency of $Z$ to the lines $u = i / 2^d$ and $v = j / 2^d$, the depth of the subdivision is at most $\lceil \log_2 (1 / \mu) \rceil$, and boxes reach line L8 only around singular points or such tangencies. At a singular point every box that contains it is split, so with a depth limit $d$ line L8 returns the boxes of side $2^{-d}$ that contain it, which isolates it. $\blacksquare$
