---
title: BUILD stores in each cell the least depth of the points seen through that pixel, BACK-PROJECT inverts the projection, and the grid normal is exact on planes
proves: [correctness]
status: full
---

Fix the image size $W \times H$ and the intrinsic parameters $f_x, f_y > 0$, $c_x, c_y$. For a point $X = (X_1, X_2, X_3)$ with $X_3 > 0$ the projection is $\pi(X) = (f_x X_1 / X_3 + c_x,\ f_y X_2 / X_3 + c_y)$. The pixel $(u, v)$ owns the half-open square $S(u, v) = [u - \tfrac12, u + \tfrac12) \times [v - \tfrac12, v + \tfrac12)$ of the image plane. For a pixel let $A(u, v)$ be the set of input points with $X_3 > 0$ and $\pi(X) \in S(u, v)$.

**Lemma 1 (the pixel of a point).** Line L4 gives $(u, v)$ exactly when $\pi(X) \in S(u, v)$.

*Proof.* For a real $x$ and an integer $u$, $\lfloor x + \tfrac12 \rfloor = u$ holds exactly when $u \le x + \tfrac12 < u + 1$, that is, when $u - \tfrac12 \le x < u + \tfrac12$. Apply this to both coordinates. $\square$

**Theorem 1 (BUILD).** After BUILD, the cell $(u, v)$ holds $\min \{ X_3 : X \in A(u, v) \}$ if $A(u, v)$ is not empty, and is empty otherwise.

*Proof.* Every cell starts empty at line L1. Line L3 drops the points with $X_3 \le 0$, and line L5 drops the points whose pixel is outside the grid; by Lemma 1, such a point is in no set $A(u, v)$ of the grid. Every other point is in exactly one set $A(u, v)$, the one of the pixel of line L4, and it is compared only with that cell.

We show by induction over the loop of line L2 that after the first $t$ points each cell holds the minimum depth of the points of $A(u, v)$ among the first $t$, or is empty if there are none. This is true for $t = 0$. Point $t + 1$ changes at most the cell $(u, v)$ of line L4. If the cell was empty, line L7 stores $X_3$, the minimum of a set of one depth. If it held $z$, line L6 replaces $z$ by $X_3$ exactly when $X_3 < z$, so the cell holds $\min(z, X_3)$. Other cells keep their sets and their values. At $t = n$ this is the claim. $\square$

**Theorem 2 (BACK-PROJECT).** Let the cell $(u, v)$ hold the depth $z > 0$, and let $X = z\,(a, b, 1)$ with $a = (u - c_x)/f_x$ and $b = (v - c_y)/f_y$, as at line L10. Then $X_3 = z$, $\pi(X) = (u, v)$, and $\|X\| = z\sqrt{1 + a^2 + b^2}$. Of all the points with depth $z$ whose projection is in $S(u, v)$, $X$ is the one on the ray through the pixel center.

*Proof.* $X_3 = z$ by construction, and $f_x X_1 / X_3 + c_x = f_x a + c_x = u$, and in the same way the second coordinate is $v$. The norm is $z \|(a, b, 1)\|$. A point of depth $z$ is fixed by its projection, because $X_1 = z (x - c_x)/f_x$ and $X_2 = z (y - c_y)/f_y$; the projection $(u, v)$ gives $X$. $\square$

So a cloud whose points project exactly onto pixel centers, one point per pixel, is rebuilt exactly by BUILD and BACK-PROJECT. For other points the round trip moves each kept point along its depth plane to the ray of its pixel center, by at most $\tfrac12 z / f_x$ in $X_1$ and $\tfrac12 z / f_y$ in $X_2$.

**Theorem 3 (NEIGHBORS).** Lines L11 to L14 return the pixels $(u \pm 1, v)$ and $(u, v \pm 1)$ that are in the grid, hold a depth $z'$, and satisfy $|z' - z| \le \tau$.

*Proof.* Line L11 lists the four offsets, line L12 removes those outside the grid, and line L13 tests the remaining two conditions. $\square$

**Theorem 4 (normals on a plane).** Suppose the valid cells around $(u, v)$ used at line L15 all back-project to points of one plane $\{X : m \cdot X = d\}$ with $\|m\| = 1$, and that the two differences $\Delta_u, \Delta_v$ of line L15 are not parallel. Then lines L16 to L18 return $m$ or $-m$, and the sign is the one with $n \cdot X \le 0$ at the back-projected point $X$ of $(u, v)$, the side of the plane that faces the camera.

*Proof.* Each difference is $X' - X''$ with $m \cdot X' = m \cdot X'' = d$, so $m \cdot \Delta_u = m \cdot \Delta_v = 0$. The cross product of two vectors that are both orthogonal to $m$ and not parallel is a nonzero multiple of $m$, so after the division by its length at line L17 it is $\pm m$. Line L18 flips it when $n \cdot X > 0$, so the result has $n \cdot X \le 0$. The camera center is the origin, and $n \cdot (0 - X) \ge 0$ says that $n$ points from $X$ toward the camera side. $\square$

On a curved surface the same lines give the normal of the plane through the back-projected neighbors, which tends to the surface normal as the pixel spacing on the surface goes to zero. All loops are over finite ranges, so every operation terminates. $\blacksquare$
