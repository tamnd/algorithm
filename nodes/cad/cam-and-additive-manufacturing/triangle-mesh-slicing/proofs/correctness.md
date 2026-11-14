---
title: The bucket and sweep slicer returns closed loops with the solid on their left
proves: [correctness, termination]
status: full
---

**Claim.** Let $(V, T)$ be a closed, oriented, edge-manifold triangle mesh: each edge $\{a, b\}$ belongs to exactly two triangles, one of them has $b$ right after $a$ in its cyclic order and the other has $a$ right after $b$. Let $Z_1 < \dots < Z_k$, and let all coordinates be exact numbers. Then SLICE$(V, T, Z)$ stops, and for each $j$:

1. every triangle $t$ with $z_{\min}(t) < Z_j \le z_{\max}(t)$ gives exactly one segment, and no other triangle gives one;
2. LINK partitions these segments into closed loops, where each segment ends at the start of the next one;
3. the horizontal part of the outward normal of each triangle points to the right of its segment, or the segment has length zero.

Here a vertex counts as above the plane $z = Z_j$ when $z_v \ge Z_j$ and below when $z_v < Z_j$.

**Step 1 (the active list).** Fix a triangle $t$ and let $j_0$ be the bucket of line L4, so $j_0 - 1$ is the number of planes with $Z_i \le z_{\min}(t)$. Since the heights increase, $Z_j > z_{\min}(t)$ holds exactly for $j \ge j_0$. The triangle enters $A$ at step $j_0$ (line L7) and stays until the first step $j$ with $z_{\max}(t) < Z_j$ (line L8). It never comes back, because $z_{\max}(t) < Z_j$ implies $z_{\max}(t) < Z_{j'}$ for all $j' > j$. So after line L8 of step $j$, $t \in A$ if and only if $j \ge j_0$ and $Z_j \le z_{\max}(t)$, that is, if and only if $z_{\min}(t) < Z_j \le z_{\max}(t)$. If $j_0 = k + 1$, the triangle is in the bucket $B[k+1]$, which the loop never reads, and indeed it crosses no plane.

**Step 2 (one segment per active triangle).** Let $t = (a, b, c)$ be active at step $j$. The vertex of height $z_{\min}(t)$ is below and the vertex of height $z_{\max}(t)$ is above, so both labels occur. Go around the cycle $a \to b \to c \to a$. The label changes an even number of times, at least once, and at most three times, so exactly twice: once from above to below (the edge $e_{\text{out}}$) and once from below to above (the edge $e_{\text{in}}$). So CROSS is well defined, and on each of these two edges the heights of the ends differ, so the crossing point is defined. A triangle that is not active has all three labels equal and gives no segment. This proves part 1.

**Step 3 (the successor map).** Let $E_j$ be the set of edges with one end above and one end below. For every edge $e \in E_j$, both triangles of $e$ are active, since each has a vertex above and a vertex below. The two triangles traverse $e$ in opposite directions, so $e$ goes from above to below in exactly one of them and from below to above in the other. So $e$ is $e_{\text{out}}$ of exactly one segment and $e_{\text{in}}$ of exactly one segment. Line L12 therefore never writes a key twice, and the keys of $S$ are exactly $E_j$. Define $\sigma(e) = e_{\text{in}}$ of the segment filed under $e$. Each $e' \in E_j$ is $e_{\text{in}}$ of exactly one segment, so $\sigma$ is a bijection of the finite set $E_j$, a [permutation](/permutation/).

The end point of the segment filed under $e$ is the crossing point of the edge $\sigma(e)$, and the segment filed under $\sigma(e)$ starts at the crossing point of the same edge. The crossing point of an edge depends only on the edge and the plane: the formula of line L11 applied from either end gives the same exact point, because $a + (b - a)\lambda = b + (a - b)(1 - \lambda)$ with $\lambda = (z - z_a)/(z_b - z_a)$ and $1 - \lambda = (z - z_b)/(z_a - z_b)$. So each segment ends where its successor starts.

**Step 4 (LINK).** Each pass of the repeat loop of lines L18 to L20 starts at a key $e_0$ and visits $e_0, \sigma(e_0), \sigma^2(e_0), \dots$, deleting each key it reads. A permutation of a finite set is a union of disjoint cycles, so the sequence returns to $e_0$ after the length $\ell$ of the cycle of $e_0$, and the keys $\sigma(e_0), \dots, \sigma^{\ell-1}(e_0)$ are different from $e_0$ and from each other. They are all still in $S$: a key leaves $S$ only when it is read, and the keys read in earlier passes belong to other cycles. So line L19 never reads a missing key, the pass stops with $e = e_0$, and it has deleted exactly one cycle. Each pass deletes at least one key, so the outer loop stops after at most $|E_j|$ passes, and the passes write out every cycle once. By Step 3 consecutive points of a pass are the start and end of one segment, and the last segment ends at the first point. This proves part 2.

**Step 5 (orientation).** Let $t$ be active, with the outward normal $n = (b - a) \times (c - a)$ for its cyclic order $(a, b, c)$. A cyclic shift does not change $n$, so let $a$ be the vertex that is alone on its side. Write $p$ and $q$ for the start and the end of the segment, $d = q - p$, and $h = Z_j$.

*Case 1: $a$ is below and $b$, $c$ are above.* Then $a \to b$ goes from below to above, so $q = a + s(b - a)$, and $c \to a$ goes from above to below, so $p = a + r(c - a)$, with $s, r \in (0, 1]$. Then $(q - a) \times (p - a) = s r\, n$. Also $(q - a) \times (p - a) = (q - p + p - a) \times (p - a) = d \times w$ with $w = p - a$. Here $d_z = 0$ because $p$ and $q$ lie in the plane, and $w_z = h - z_a > 0$. With $d = (d_x, d_y, 0)$,
$$d \times w = (d_y w_z,\; -d_x w_z,\; d_x w_y - d_y w_x).$$
So $(n_x, n_y) = \frac{w_z}{s r}\,(d_y, -d_x)$, a positive multiple of $d$ turned clockwise by a right angle.

*Case 2: $a$ is above and $b$, $c$ are below.* Then $p = a + s(b - a)$ on the edge $a \to b$, and $q = a + r(c - a)$ on the edge $c \to a$, with $s, r \in [0, 1)$. If $z_a = h$, then $s = r = 0$, $p = q = a$, and the segment has length zero. Otherwise $s, r > 0$ and $(p - a) \times (q - a) = s r\, n$. Now $(p - a) \times (q - a) = w \times (q - p) = -d \times w$ with $w = p - a$ and $w_z = h - z_a < 0$. So $(n_x, n_y) = \frac{-w_z}{s r}\,(d_y, -d_x)$, again a positive multiple of $d$ turned clockwise.

In both cases the outward direction lies to the right of $d$, so the inside of the solid lies to the left. This proves part 3.

**Remark (area).** Parts 2 and 3 say that the loops of plane $j$ are the boundary of the cross-section at height $Z_j - \varepsilon$, traversed with the region on the left. By Green's theorem the sum of their shoelace areas is then the area of that cross-section. This step uses Green's theorem and is not proved here. The tests check the identity exactly on a cube, a tetrahedron and a square frame with a hole, and they check the inside and outside of random sample points against a vertical ray count in the mesh.

**Termination.** The loops of lines L2 and L6 are over finite lists, line L8 and line L10 scan the finite list $A$, and Step 4 shows that LINK stops. $\blacksquare$
