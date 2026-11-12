---
title: Correctness of the Plücker ray-triangle test
proves: [correctness]
status: full
---

**Claim.** In exact arithmetic, PLUCKER-RAY-TRIANGLE returns $(t, w_a, w_b, w_c)$ with $o + t\,d = w_a a + w_b b + w_c c$, $w_a + w_b + w_c = 1$, all weights $\ge 0$ and $t_{\min} < t < t_{\max}$, if such a point exists and the ray is not parallel to the plane of a non-degenerate triangle; otherwise it returns MISS.

**Step 1: the side value is a triple product.** For the ray line $R = (d, o \times d)$ and the edge line $L = (q - p, p \times q)$,

$$\mathrm{side}(R, L) = d \cdot (p \times q) + (q - p) \cdot (o \times d).$$

Write $p = o + p'$ and $q = o + q'$. Then $p \times q = o \times q' + p' \times o + p' \times q'$ (the term $o \times o$ vanishes), and $q - p = q' - p'$. So

$$\mathrm{side} = d \cdot (o \times q') + d \cdot (p' \times o) + d \cdot (p' \times q') + q' \cdot (o \times d) - p' \cdot (o \times d).$$

By the cyclic rule $x \cdot (y \times z) = y \cdot (z \times x)$, $d \cdot (o \times q') = q' \cdot (d \times o) = -q' \cdot (o \times d)$ and $d \cdot (p' \times o) = p' \cdot (o \times d)$. Four terms cancel, and $\mathrm{side}(R, L) = d \cdot (p' \times q') = \det[d, p - o, q - o]$.

**Step 2: the signs decide the line.** Let $\pi$ be the projection along $d$ onto a plane orthogonal to $d$, and let $X = \pi(o)$, the image of the whole ray line. For points $p, q$, the value $\det[d, p - o, q - o]$ is $|d|$ times twice the signed area of the 2D triangle $X\,\pi(p)\,\pi(q)$, oriented by $d$, because the component of $p - o$ along $d$ does not change the determinant. So $s_{ab}$, $s_{bc}$, $s_{ca}$ are $2|d|$ times the signed areas of $X \pi(a) \pi(b)$, $X \pi(b) \pi(c)$, $X \pi(c) \pi(a)$. Their sum is $2|d|$ times the signed area of $\pi(a)\pi(b)\pi(c)$, and also equals $d \cdot ((a - o) \times (b - o) + (b - o) \times (c - o) + (c - o) \times (a - o)) = d \cdot ((b - a) \times (c - a)) = d \cdot n$.

If $d \cdot n = 0$, the ray is parallel to the plane (or the triangle is degenerate), the projected triangle has zero area, and the problem returns MISS; line L4 returns MISS. Otherwise the projected triangle is non-degenerate. A 2D point lies in a closed non-degenerate triangle if and only if the three signed areas it forms with the directed edges are all $\ge 0$ or all $\le 0$. The ray line meets the closed triangle if and only if $X$ lies in the projected closed triangle, since $\pi$ maps the line to $X$ and the triangle onto its projection bijectively. So line L3 returns MISS exactly when the line misses the triangle.

**Step 3: the hit point.** If the line meets the plane, it meets it in exactly one point $o + t\,d$ with $n \cdot (o + t\,d - a) = 0$, that is $t = n \cdot (a - o) / (n \cdot d)$, and $n \cdot d = \mathrm{total}$ by step 2. This is line L5. By step 2 this point is in the closed triangle. Its barycentric weights are kept by the affine map $\pi$ restricted to the plane, which is a bijection onto the projection plane. The weight of $a$ in the projected triangle is the area of $X \pi(b) \pi(c)$ over the area of $\pi(a)\pi(b)\pi(c)$, which is $s_{bc} / \mathrm{total}$; likewise $w_b = s_{ca} / \mathrm{total}$ and $w_c = s_{ab} / \mathrm{total}$, as at line L7. They sum to 1, and they are $\ge 0$ since the three values have the sign of their sum or are zero.

**Step 4: the interval.** Line L6 returns MISS exactly when $t$ is outside $(t_{\min}, t_{\max})$. Since the hit point of the line is unique, no other point of the ray can be a valid answer.

Together, the algorithm returns the hit when it exists and MISS otherwise. $\blacksquare$

**Remark on floating point.** The edge from $q$ to $p$ has the coordinates $(p - q, q \times p)$. Each coordinate is computed as the negation of the corresponding coordinate of $(q - p, p \times q)$, exactly, because $\mathrm{fl}(x - y) = -\mathrm{fl}(y - x)$ and the cross product swaps the same two rounded products. The side value is a sum of products with one factor negated, so it is the exact negation as well. Hence the two triangles of a shared edge always compute opposite edge values. This gives watertightness along edges; it gives nothing at vertices, where the signs of several independently rounded values must agree.
