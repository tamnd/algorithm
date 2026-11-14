---
title: The exact ray test, the exit test, and the shape diameter of a slab
proves: [correctness, termination]
status: full
---

**Setup.** The mesh has vertices with rational coordinates (every float is a rational number) and faces $(a, b, c)$ of positive area. It is closed and bounds a solid $S$, and its faces are oriented outward: near every point $x$ inside a face $g$, the points $x + \varepsilon n_g$ are outside $S$ and the points $x - \varepsilon n_g$ are inside, for all small $\varepsilon > 0$, where $n_g = (b - a) \times (c - a)$. For a face $f$, the algorithm takes the centroid $o$ of $f$, a list $D$ of rational directions $d$ with $d \cdot n_f < 0$, and for each $d$ the ray $o + t d$, $t > 0$. All arithmetic in lines L1 to L5 is on rationals, so it is exact.

**Lemma 1 (the ray-triangle test).** Let $e_1 = b - a$, $e_2 = c - a$, $s = o - a$ and $\Delta = e_1 \cdot (d \times e_2)$. If $\Delta \ne 0$, the function returns $t$ exactly when $o + t d$ lies in the closed triangle $abc$ and $t > 0$, and it returns None otherwise. If $\Delta = 0$, it returns None.

*Proof.* The point $o + t d$ equals $a + u e_1 + v e_2$ exactly when $-t d + u e_1 + v e_2 = s$. This is a $3 \times 3$ linear system in $(t, u, v)$ with the columns $-d, e_1, e_2$. Its determinant is $\det(-d, e_1, e_2) = \det(e_1, d, e_2) = e_1 \cdot (d \times e_2) = \Delta$. If $\Delta \ne 0$, [Cramer's rule](/cramers-rule/) gives the unique solution

$$u = \frac{\det(-d, s, e_2)}{\Delta} = \frac{s \cdot (d \times e_2)}{\Delta}, \qquad v = \frac{\det(-d, e_1, s)}{\Delta} = \frac{d \cdot (s \times e_1)}{\Delta}, \qquad t = \frac{\det(s, e_1, e_2)}{\Delta} = \frac{e_2 \cdot (s \times e_1)}{\Delta},$$

which are the values that the function computes, with `pv` $= d \times e_2$ and `qv` $= s \times e_1$. The point $a + u e_1 + v e_2$ is in the closed triangle exactly when $u \ge 0$, $v \ge 0$ and $u + v \le 1$. The function returns None as soon as one of these fails, and returns $t$ only when also $t > 0$. The early test $u > 1$ only rejects points that also fail $u + v \le 1$ or $v \ge 0$. All values are rational and all comparisons are exact. If $\Delta = 0$, then $d$ is parallel to the plane of the triangle, and the ray meets the plane in no point or in a whole line; the function treats both as a miss. $\square$

**Lemma 2 (the first hit).** For each ray, line L4 returns the smallest $t > 0$ such that $o + t d$ lies on a face other than $f$ (among faces not parallel to $d$), and the set of all such faces at that $t$.

*Proof.* By Lemma 1, each call returns the exact parameter of the hit or None. The loop keeps the smallest value seen and the faces that reach it, with exact comparisons, so two faces that meet the ray at the same point, as at a shared edge or vertex, are both in the set. $\square$

**Lemma 3 (the exit test keeps every ray that leaves through the inside of a face).** Let the first hit of a ray be at $x = o + t^* d$, and suppose $x$ lies inside a single face $g$ (not on its boundary) and $d$ is not parallel to $g$. Then $d \cdot n_g > 0$, so line L5 keeps the ray.

*Proof.* The face $f$ is not hit again: $d \cdot n_f \ne 0$, so the line meets the plane of $f$ only at $o$. Since $o$ lies inside $f$ and $d \cdot n_f < 0$, the points $o + \varepsilon d$ are on the side $-n_f$ of $f$ for small $\varepsilon$, so they are inside $S$ by the orientation. By Lemma 2 the open segment from $o + \varepsilon d$ to $x$ meets no face, so it does not cross the boundary of $S$, and it is connected; so all its points are inside $S$. In particular $x - \varepsilon d$ is inside $S$ for small $\varepsilon > 0$. Now $d \cdot n_g \ne 0$. If $d \cdot n_g < 0$, then $(x - \varepsilon d - x) \cdot n_g = -\varepsilon\, d \cdot n_g > 0$, so $x - \varepsilon d$ is on the side $n_g$ of $g$, which is outside $S$ by the orientation. This is a contradiction, so $d \cdot n_g > 0$. $\square$

When the first hit is on an edge or a vertex, the code keeps the ray if one of the faces there has $d \cdot n_g > 0$. That this is always the right choice is not proved. When the faces of the mesh are not consistently oriented, Lemma 3 does not apply, and the code drops the rays that reach a face from its outer side.

**Theorem 1 (termination and cost).** For one face, the algorithm stops after $|D| \cdot (F - 1)$ ray-triangle tests and $|D|$ exit tests, where $F$ is the number of faces, and lines L6 to L8 take $O(|D| \log |D|)$ time.

*Proof.* Each loop runs over a finite list, and each ray-triangle test is a fixed number of exact operations on rationals. The median needs a sort of at most $|D|$ lengths. $\square$

**Theorem 2 (the slab).** Let the mesh be the box $[-L, L]^2 \times [-h/2, h/2]$ with $h > 0$, and let $f$ be a face of the top side whose centroid $o$ satisfies $|o_x| + h \tan(\gamma/2) < L$ and $|o_y| + h \tan(\gamma/2) < L$, where $\gamma$ is the opening angle of the cone. Then every ray of $f$ is kept, and a ray at the angle $\theta$ from the inward normal $-e_z$ has the length $h / \cos\theta$. With one ray ($|D| = 1$), the SDF is $h$. For a fixed list of angles, the SDF is $h$ times a number that does not depend on $h$, on $L$, or on the position of $f$ in the region above.

*Proof.* A ray $o + t d$ with $d \cdot (-e_z) = |d| \cos\theta > 0$ reaches the plane $z = -h/2$ at $t^* = h / (|d|\cos\theta)$, at the length $t^* |d| = h / \cos\theta$, and its horizontal distance from $o$ there is $h \tan\theta \le h \tan(\gamma / 2)$. By the condition on $o$, this point lies inside the bottom side, not on its border, so it is on one or two bottom faces. Before $t^*$ the ray is strictly between the planes $z = \pm h/2$ and strictly inside the side walls, so it meets no other face. The bottom faces have $n_g$ along $-e_z$, so $d \cdot n_g > 0$, and the ray is kept (also when it hits a shared edge of two bottom faces, because both have $d \cdot n_g > 0$). With one ray, $\theta = 0$ and the length is $h$. The directions depend only on the normal direction $-e_z$, so they do not change with $h$, $L$ or $f$. The list of lengths is $h$ times the list of the $1/\cos\theta$, and the median, the standard deviation, the set kept by line L7 and the mean of line L8 all scale by $h$. $\square$

For the 25 directions of the code, at $0°$, $20°$, $40°$ and $60°$ (eight at each nonzero angle), the lengths are $h$, $1.0642h$, $1.3054h$ and $2h$. The median is $1.3054h$ and the standard deviation is $0.3989h$, so line L7 drops the eight rays at $60°$, and the SDF is $(1 + 8 \sec 20° + 8 \sec 40°)h/17 = 1.1739h$, up to the rounding of the directions to floats.

**What is not proved.** That the SDF approximates the diameter of the shape near a face, that it changes little when a shape changes its pose, and that the segmentation built on it finds meaningful parts are claims about typical shapes. They are measured, not proved here.
