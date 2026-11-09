---
title: The wedge method returns the correct location for every query point
proves: [correctness]
status: full
---

**Setting.** $v_0, \ldots, v_{n-1}$ is a convex polygon in counterclockwise order with at least three vertices not on one line, $c$ a point of its open interior, and $\theta(r)$ the counterclockwise angle of $r - c$ from the direction of $v_0 - c$, in $[0, 2\pi)$. Indices are modulo $n$.

**Lemma 1.** If $c$ is in the open interior of the convex polygon and the vertices are in counterclockwise order, then $0 = \theta(v_0) < \theta(v_1) < \cdots < \theta(v_{n-1}) < 2\pi$, and the wedges partition the plane minus $c$.

*Proof.* For each $i$, $c$ lies strictly to the left of the line through $v_i$ and $v_{i+1}$, since the polygon is on the closed left side of each edge line and $c$ is not on the boundary. So $\mathrm{orient}(c, v_i, v_{i+1}) > 0$, and the counterclockwise turn $\alpha_i$ from $v_i - c$ to $v_{i+1} - c$ is in $(0, \pi)$. The boundary of the polygon is a closed curve that winds once counterclockwise around the interior point $c$, so $\alpha_0 + \cdots + \alpha_{n-1} = 2\pi$. Then $\theta(v_i) = \alpha_0 + \cdots + \alpha_{i-1}$ is strictly increasing and below $2\pi$ for $i \le n - 1$. The half-open intervals $[\theta(v_i), \theta(v_{i+1}))$, with $\theta(v_n) = 2\pi$, partition $[0, 2\pi)$, so the wedges partition the plane minus $c$. $\blacksquare$

**Theorem.** CONVEX-LOCATE returns the answer defined in the problem statement for every query point $q$.

*Proof.* If $q = c$, then $q$ is interior and line L1 is right. Otherwise, Lemma 1 makes $i \mapsto \theta(v_i)$ increasing, so line L5 keeps the invariant $\theta(v_{lo}) \le \theta(q) < \theta(v_{hi})$, and the loop ends with $q$ in wedge $i = \mathrm{lo}$. The closed wedge $i$ meets the polygon in the triangle $T = c\, v_i\, v_{i+1}$: the polygon is the union of the triangles $c\, v_j\, v_{j+1}$, which lie in the wedges $j$. In $T$, the side $v_i v_{i+1}$ is the only side on the boundary of the polygon. If $o > 0$, then $q$ is strictly on the side of $c$ and in the wedge, so in the interior of $T$ or on the open ray from $c$ to $v_i$ before $v_i$, which is interior to the polygon. If $o < 0$, then $q$ is beyond the edge line, outside the polygon, which lies on the closed left side of that line. If $o = 0$, then $q$ is on the edge line and in the wedge; the line meets the half-open wedge in the segment from $v_i$ included to $v_{i+1}$ excluded, so $q$ is $v_i$ or in the relative interior of the edge. Line L9 tells the two apart. $\blacksquare$

**Remark (the comparison of line L5).** For $w \ne 0$, let half$(w) = 0$ if $u \times w > 0$, or $u \times w = 0$ and $u \cdot w > 0$, and half$(w) = 1$ otherwise, where $u = v_0 - c$. Then half$(w) = 0$ exactly when the angle of $w$ from $u$ is in $[0, \pi)$. Two vectors in the same half have angles less than $\pi$ apart, so the angle of $a$ is at most the angle of $b$ exactly when $a \times b \ge 0$, with equality only for the same direction. So line L5 computes $\theta(v_{mid}) \le \theta(q)$ exactly.
