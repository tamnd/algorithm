---
title: QUADTREE-MESH stops with a balanced tree and a triangulation of the root square whose triangles all have aspect ratio at most 4
proves: [correctness, termination]
status: full
---

**Claim.** Let $X$ be a set of $n \ge 2$ distinct points with rational coordinates. Then QUADTREE-MESH$(X)$, with C3 over the 5 by 5 block, stops. At the end the quadtree is balanced, and every leaf that holds a point holds exactly one and is surrounded by eight leaves of its own size. The output is a triangulation of the root square $R$ that has every point of $X$ as a vertex, and every triangle $abc$ has aspect ratio $A(abc) \le 4$. So every angle is at least $\arcsin(1/4) \approx 14.4775°$.

**What is not claimed.** The size bound of Bern, Eppstein and Gilbert (Theorem 1 and Corollary 1 of their paper) is cited, not proved here.

**Notation.** For a triangle, $A(abc) = \ell_{\max} / h$, where $\ell_{\max}$ is the longest side and $h$ the altitude onto it. Since $h = 2\,\mathrm{area}/\ell_{\max}$, we have $A = \ell_{\max}^2 / (2\,\mathrm{area})$. If $\theta$ is the smallest angle and $b$ a side next to it other than the longest, then $h = b \sin\theta \le \ell_{\max} \sin\theta$, so $A \ge 1/\sin\theta$. Thus $A \le 4$ gives $\sin\theta \ge 1/4$. A box is *internal* if it has been split. The *block* of radius $r$ of a box $b$ of level $k$ is the set of level $k$ boxes whose column and row differ from those of $b$ by at most $r$.

**Step 1: the loop stops.** Let $\delta$ be the smallest distance between two points of $X$. Every split in the run is of one of these kinds: a crowded box (L5, first part), a neighbor of a crowded box or a coarser box split to create it (L5, second part), a coarser box that covers a missing neighbor (L7), or an unbalanced leaf (L9). Suppose some box is split, and let $s$ be the smallest side of a box that is ever split. Look at the first split, in time order, of a box of side $s$.

- If it was crowded by C3, a box of side $s$ in its block was already internal, so an earlier split of a box of side $s$ exists. Contradiction.
- If it was split in the second part of L5, the crowded box was split just before it, and that box has side at most $s$. By the choice of $s$ it has side $s$, and it was split earlier. Contradiction.
- If it was split in L7, it covers a missing neighbor of a leaf of side $t$ that holds a point, so $s \ge 2t$, and that leaf exists because its parent, of side $2t \le s$, was split before. Again an earlier split of a box of side at most $s$ exists. Contradiction.
- If it was split in L9, one of its sides has two corners inside, so a box of side $s/2$ was split earlier. Contradiction with the choice of $s$.

So the first split of side $s$ was by C1 or C2. With C1 the box holds two points, so its diagonal is at least $\delta$ and $s \ge \delta/\sqrt2$. With C2 the box holds a point whose nearest neighbor is closer than $2\sqrt2\,s$, so $s > \delta / (2\sqrt2)$. Every split box therefore has side more than $\delta / (2\sqrt2)$. The root holds finitely many boxes of that size or larger, and each is split at most once. Each round of the loop splits at least one box, so the loop stops.

**Step 2: the state at the end.** The loop stops only when no leaf is crowded, no leaf with a point lacks a neighbor of its size, and no leaf is unbalanced. So the tree is balanced. Let $b$ be a leaf of side $\ell$ that holds a point $x$. C1 fails, so $x$ is the only point in $b$. C2 fails, so every other point is at distance at least $2\sqrt2\,\ell$ from $x$. L6 fails, so all eight extended neighbors of $b$ exist, and C3 fails, so no box of the 5 by 5 block is internal. In particular the eight extended neighbors are leaves. They lie in the root. The root has side $4L$ and its boundary is at distance at least $1.5L$ from $X$, so a box that holds a point and touches the boundary has side at least $1.5L$, which means side $2L$ or $4L$. Such a box is crowded by C1 or C2, because any two points are at most $\sqrt2 L < 2\sqrt2 \cdot 2L$ apart. So a final leaf with a point does not touch the boundary, and its eight neighbors, which are boxes of the same grid, lie inside the root.

**Step 3: the moves.** Let $x$ lie in leaf $b$ of side $\ell$ and let $y$ be its chosen corner. Since $y$ is a nearest corner, $x$ lies in the closed quarter of $b$ at $y$, so $|x - y| \le \ell/\sqrt2$. The four boxes with corner $y$ are $b$ and three of its extended neighbors, all leaves of side $\ell$.

(a) Two points never move the same corner. If $x$ and $x'$ both chose $y$, then $x'$ lies in one of these four boxes, of side $\ell$, so $|x - x'| \le \sqrt2\,\ell < 2\sqrt2\,\ell$. This contradicts Step 2.

(b) No box has two moved corners. Let a box $q$ of side $\ell$ have moved corners $y$ and $y'$, moved by $x$ and $x'$. The leaves of $x$ and $x'$ both touch $q$, so they are extended neighbors of $q$ and all have side $\ell$. If $y$ and $y'$ are adjacent corners, $|x - x'| \le \ell/\sqrt2 + \ell + \ell/\sqrt2 = (1 + \sqrt2)\ell < 2\sqrt2\,\ell$. If they are opposite corners, $|x - x'| \le 2\sqrt2\,\ell$, and Step 2 forces equality. Equality needs $|x - y| = \ell/\sqrt2$, so $x$ is the center of its box, and $x, y, y', x'$ lie on one diagonal line. At the center all four corners tie, and the tie rule picks the lower left corner, so $y$ is the lower left corner of the box of $x$. The points lie on one line in the order $x, y, y', x'$, and $y'$ is the corner of $q$ opposite to $y$, so $q$ lies below and to the left of $y$, and $y$ is the upper right corner of $q$. The same argument with $x'$ in place of $x$ shows that $y'$ is the upper right corner of $q$ as well. So $y = y'$, a contradiction.

(c) A box with a moved corner has no split side. Let $q$ have the moved corner $y$ of $x$, where $x$ lies in $b$. The box $q$ lies in the 3 by 3 block of $b$, so each box across a side of $q$, at the level of $q$, lies in the 5 by 5 block of $b$. By Step 2 none of them is internal. A side of a leaf has a corner inside it only if the box of the same level across that side is internal. So the sides of $q$ hold no corner inside.

By (a), (b) and (c), every leaf with a moved corner is a quadrilateral with exactly one moved corner and no other boundary vertex, which is the case L14 handles.

**Step 4: the unmoved boxes.** By balance, the vertices on a side of an unmoved leaf of side $\ell$ are its two corners and, if the box across is internal, the midpoint. The fan from the center $c$ gives two kinds of triangles. A triangle $c$, corner, corner has a right angle at $c$ and legs $\ell/\sqrt2$. A triangle $c$, corner, midpoint has a right angle at the midpoint and legs $\ell/2$. Both are right isosceles, with $A = \ell_{\max}^2/(2\,\mathrm{area}) = 2$.

**Step 5: the moved boxes.** Scale, rotate and reflect so that the box $q$ is $[0,1]^2$ and its moved corner is the origin. These maps do not change $A$. The other corners are $p = (1,0)$, $r = (1,1)$ and $u = (0,1)$. By Step 3, $x$ lies in the quarter at the origin of a box with corner $0$, so $x = (x_1, x_2) \in [-\tfrac12, \tfrac12]^2$. L14 takes, among the diagonals whose two triangles are both counterclockwise, the one with the smaller largest $A$. So it suffices to show one valid diagonal with both triangles at most 4.

*Case 1: $x_1 \ge 0$ and $x_2 \ge 0$.* Take the diagonal $xr$, with triangles $xpr$ and $xru$. Twice the area of $xpr$ is $\mathrm{ORIENT2D}(x, p, r) = 1 - x_1 \ge \tfrac12 > 0$. Put $t = 1 - x_1 \in [\tfrac12, 1]$. The squared sides are $|pr|^2 = 1$, $|xp|^2 = t^2 + x_2^2 \le t^2 + \tfrac14$ and $|xr|^2 = t^2 + (1 - x_2)^2 \le t^2 + 1$. So
$$A(xpr) \le \frac{t^2 + 1}{t} = t + \frac1t \le \frac52,$$
because $t + 1/t$ is at most $5/2$ on $[\tfrac12, 1]$. The triangle $xru$ is the mirror case with $x_1$ and $x_2$ swapped, so $A(xru) \le 5/2$ too.

*Case 2: $x_1 < 0$ or $x_2 < 0$.* Take the diagonal $pu$, with triangles $xpu$ and $pru$. The triangle $pru$ is right isosceles, $A = 2$. Twice the area of $xpu$ is $\mathrm{ORIENT2D}(x, p, u) = 1 - x_1 - x_2$. Let $\sigma = x_1 + x_2$. One coordinate is negative and the other is at most $\tfrac12$, so $\sigma < \tfrac12$ and $1 - \sigma > \tfrac12 > 0$. The squared sides are $|pu|^2 = 2$, $|xp|^2 = (1 - x_1)^2 + x_2^2$ and $|xu|^2 = x_1^2 + (1 - x_2)^2$. First, $2 < 4(1 - \sigma)$ because $\sigma < \tfrac12$. Second,
$$|xp|^2 - 4(1 - \sigma) = (x_1 + 1)^2 + (x_2 + 2)^2 - 8.$$
On the region of Case 2 this is negative. The function grows with $x_1$ and with $x_2$ on $[-\tfrac12, \tfrac12]^2$, so on the part with $x_2 < 0$ it is below its value at $(\tfrac12, 0)$, which is $\tfrac94 + 4 - 8 < 0$, and on the part with $x_1 < 0$ it is below its value at $(0, \tfrac12)$, which is $1 + \tfrac{25}{4} - 8 < 0$. By symmetry the same holds for $|xu|^2$. So $\ell_{\max}^2 < 4 (1 - \sigma)$ and $A(xpu) < 4$.

In both cases a valid diagonal with $A \le 4$ exists, so the triangles of L14 have $A \le 4$.

**Step 6: the triangles tile the root.** All triangles are counterclockwise: the fans by construction, and the moved boxes because L14 accepts only counterclockwise pairs, and Step 5 shows that one exists. Now look at the directed edges.

- Inside a leaf, the fan edges $c v$ and the diagonal of L14 are used once in each direction.
- Two leaves of the same size that share a side see the same vertices on it: the same corners, moved or not, since both boxes have the corner and a moved corner is moved for all four boxes at it, and no midpoint, since a midpoint would need an internal box across, and both are leaves. So the edge is used once in each direction.
- A leaf of side $2\ell$ and two leaves of side $\ell$ that share its side: the big leaf has the midpoint $m$, because the box across is internal, and its edges are $a m$ and $m b$. The small leaves have the sides $m a$ and $b m$ with no midpoint. The point $m$ and the corners $a$ and $b$ are not moved, because a moved corner has four leaves of one size around it.
- Edges on the boundary of the root are used once, with the root on their left.

Let $w(z)$ be the number of triangles that contain a point $z$ that lies on no edge. When $z$ crosses an inner edge, it leaves the triangle on one side and enters the triangle on the other side, because the edge is used once in each direction, so $w$ does not change. When $z$ crosses the boundary of $R$ from outside, $w$ grows by one. Far from $R$, $w = 0$. So $w = 0$ outside $R$ and $w = 1$ inside. The triangles have disjoint interiors and cover $R$, and since no vertex lies inside an edge used in the other direction, they meet face to face. Every point of $X$ is a moved corner, so it is a vertex.

Together, Steps 1 to 6 prove the claim. The test file checks Steps 2, 5 and 6 directly: balance by brute force over all pairs of leaves, $A \le 4$ in exact arithmetic, and the tiling by orientation, edge twins and total area. $\blacksquare$
