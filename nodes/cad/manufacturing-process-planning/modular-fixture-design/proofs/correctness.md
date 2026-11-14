---
title: MODULAR-FIXTURES returns each normalized fixture exactly one time
proves: [correctness]
status: full
---

We use the definitions of the page. $P$ is a simple polygon with edges $e_1, \ldots, e_n$ in counterclockwise order. Edge $e_k$ has the outward normal $m_k$ and lies on the line $m_k \cdot x = h_k$. A pose $g$ is a rotation $R$ by an angle $\theta$, with $c = \cos\theta$ and $s = \sin\theta$, and a translation $t$. A fixture is a tuple $(g, q_1, q_2, q_3, e_1, e_2, e_3, v, d)$ with conditions 1 to 4 of the page. It is *normalized* when $q_1 = (0, 0)$.

**Lemma 1 (translation).** If $F$ is a fixture and $z \in \mathbb{Z}^2$, then $F$ moved by $z$ (each $q_k$, $v$ and the translation of $g$ shifted by $z$) is a fixture. So the set of all fixtures is the set of normalized fixtures and their integer translations.

*Proof.* A shift by $z$ maps lattice points to lattice points and keeps the conditions "inside an edge", "outside the part", the first hit of an axis ray, and distances. The wrench of a contact at $p + z$ with normal $\nu$ is $(\nu, (p + z) \times \nu)$, and $(p + z) \times \nu = p \times \nu - z_y \nu_x + z_x \nu_y$. So each new wrench is $T$ times the old one, with the same invertible matrix

$$T = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ -z_y & z_x & 1 \end{pmatrix}$$

for every contact. Hence the four wrenches positively span $\mathbb{R}^3$ before the shift if and only if they do after it. A fixture with $q_1 = z$ moved by $-z$ is normalized. $\square$

**Lemma 2 (line L2).** The sites of a normalized fixture are among the pairs of line L2.

*Proof.* Each $q_k$ is a point of $g(P)$, and $g$ is an isometry, so $\lvert q_i - q_j \rvert \le D$, the diameter of $P$. By the order $q_1 < q_2 < q_3$ and $q_1 = (0,0)$, the points $q_2$ and $q_3$ come after the origin in lexicographic order. The implementation lists all lattice points $(x, y)$ with $0 \le x \le \lfloor D \rfloor + 1$, $\lvert y \rvert \le \lfloor D \rfloor + 1$, $(x, y) > (0, 0)$ and $x^2 + y^2 \le D^2$. These are all lattice points after the origin within distance $D$. It then keeps each pair $q_2 < q_3$ with $\lvert q_3 - q_2 \rvert^2 \le D^2$. $\square$

**Lemma 3 (the pose equation).** Fix the sites $q_k$ and the edges $e_k$, and let $C_1 = m_2 \times m_3$, $C_2 = m_3 \times m_1$ and $C_3 = m_1 \times m_2$. Assume that not all $C_k$ are zero. A pose puts each $q_k$ on the line of $g(e_k)$ if and only if $A c + B s + C_0 = 0$ and $t$ is the unique solution of the three equations below, with $A$, $B$ and $C_0$ as on the page.

*Proof.* The point $q_k$ is on the line of $g(e_k)$ if and only if $g^{-1}(q_k) = R^{\mathsf T}(q_k - t)$ is on the line of $e_k$, that is $m_k \cdot R^{\mathsf T}(q_k - t) = h_k$, or

$$(R m_k) \cdot t = (R m_k) \cdot q_k - h_k, \qquad k = 1, 2, 3.$$

This is a system $M t = b$ with $M$ of size $3 \times 2$. A cofactor $C_k$ is a $2 \times 2$ minor of $M$ up to sign, since $(R m_i) \times (R m_j) = m_i \times m_j$ for a rotation. Some $C_k \ne 0$, so $M$ has rank 2, the solution $t$ is unique if it exists, and it exists if and only if the $3 \times 3$ matrix $[M \mid b]$ is singular. The expansion of its determinant along the column $b$ is $\sum_k C_k b_k$. Next, $R^{\mathsf T} q = (c q_x + s q_y, -s q_x + c q_y)$, so

$$(R m) \cdot q = m \cdot R^{\mathsf T} q = c\,(m \cdot q) + s\,(m_x q_y - m_y q_x) = c\,(m \cdot q) + s\,(m \times q).$$

So $\sum_k C_k b_k = A c + B s + C_0$. $\square$

**Lemma 4 (line L4 is complete).** If a fixture uses the sites $q_k$ and the edges $e_k$, its pose is one of the poses of line L4.

*Proof.* Let $w_1, w_2, w_3$ be the locator wrenches and $w_4$ the clamp wrench. We first show that $w_1, w_2, w_3$ are linearly independent. Set $\lambda_i = (-1)^i \det(w_j : j \ne i)$, with the index $i$ from 0 to 3. For each coordinate $j$, $\sum_i \lambda_i (w_i)_j$ is the expansion along the first column of the $4 \times 4$ matrix with rows $((w_i)_j, w_i)$. This matrix has two equal columns, so the sum is 0, and $\sum_i \lambda_i w_i = 0$. If $w_1, w_2, w_3$ are dependent, then $\lambda_4 = \pm\det(w_1, w_2, w_3) = 0$. Then either the four wrenches have rank less than 3, or their null space is spanned by $\lambda$, which has a zero entry. In both cases no strictly positive combination of them is zero, so by the positive span lemma (the vectors positively span $\mathbb{R}^3$ if and only if they span it and a strictly positive combination is zero) there is no form closure. This contradicts condition 4.

Now the two cases that line L4 drops:

- *All three normals parallel.* Then the forces of $w_1, w_2, w_3$ are all multiples of one vector $\nu$, so the three wrenches lie in the plane spanned by $(\nu, 0)$ and $(0, 0, 1)$, and they are dependent.
- *$r^2 = A^2 + B^2 = 0$.* Then the pose equation is $C_0 = 0$. If $C_0 \ne 0$, no pose exists. If $C_0 = 0$, every angle $\theta$ has a pose $g_\theta$ by Lemma 3, and $g_\theta$ depends smoothly on $\theta$. Along this family each $q_k$ stays on the line of $g_\theta(e_k)$. In the moving part frame, the curve $\theta \mapsto g_\theta^{-1}(q_k)$ stays on the line of $e_k$, so the first-order change of the gap at each locator is zero. The derivative of the family at the pose of the fixture is a twist $\xi$ with $\omega = 1$, so $\xi \ne 0$, and $w_k \cdot \xi = 0$ for $k = 1, 2, 3$. A nonzero vector is orthogonal to the three wrenches, so they are dependent.

So in a fixture, not all $C_k$ are zero and $r^2 > 0$. The pose satisfies $A c + B s + C_0 = 0$ and $c^2 + s^2 = 1$. The line meets the circle only if its distance $\lvert C_0 \rvert / r$ from the origin is at most 1, that is $\Delta = r^2 - C_0^2 \ge 0$. Substitution shows that the two points of the page satisfy both equations: $A c + B s = (-A^2 C_0 - B^2 C_0)/r^2 = -C_0$ and $c^2 + s^2 = r^2 (C_0^2 + \Delta) / r^4 = 1$. A line meets a circle in at most two points, so these are all the solutions, and one solution when $\Delta = 0$. By Lemma 3 the translation is the unique solution of the system, which Cramer's rule gives from two rows with $m_i \times m_j \ne 0$. $\square$

**Lemma 5 (exact signs).** Each number that lines L5 to L8 test is in the field $K = \mathbb{Q}(\sqrt{\Delta})$, and its sign is computed exactly.

*Proof.* The inputs are rational, and $c$, $s$ and $t$ are in $K$, so all coordinates of $g(P)$ are in $K$, and so are all sums, products and quotients of them. If $\Delta$ is the square of a rational, $K = \mathbb{Q}$. Otherwise $\sqrt{\Delta}$ is irrational and $a + b\sqrt{\Delta}$ is zero only if $a = b = 0$. If $a$ and $b$ have the same sign, or one is zero, the sign is clear. If they have opposite signs, the sign is that of the term with the larger absolute value, and $a^2 \ne b^2 \Delta$ because $\sqrt{\Delta}$ is irrational. $\square$

**Lemma 6 (line L5).** A pose passes line L5 if and only if each $q_k$ is in the relative interior of $g(e_k)$.

*Proof.* By Lemma 3, $q_k$ is on the line of $g(e_k) = [a, b]$. Write $\delta = b - a$ and $\mu = (q_k - a) \cdot \delta$. The point is strictly between $a$ and $b$ if and only if $0 < \mu < \delta \cdot \delta$. Line L5 tests these two signs exactly (Lemma 5). $\square$

**Lemma 7 (lines L6 and L7).** For a pose that passes line L5, lines L6 and L7 keep exactly the pairs $(v, d)$ of condition 2 and 3.

*Proof.* If $(v, d)$ satisfies conditions 2 and 3, then $v = u - \sigma d$ with $\sigma \le \rho$ and $u \in g(P)$. So $v$ is in the bounding box of $g(P)$ grown by $\rho$. The implementation scans the integer points from $\lfloor \min x - \rho \rfloor - 1$ or less to $\lceil \max x + \rho \rceil + 1$ or more, and the same for $y$, which covers the box with a margin of one unit against rounding of the float bounds. The float filter drops $(v, d)$ only if the segment from $v$ to $v + \rho d$ is more than $10^{-7}$ from every edge in floating point. For a real hit the true distance is 0, and the rounding error of the float distance for coordinates of moderate size is far below $10^{-7}$, so a real hit is never dropped. The test "$v$ strictly outside $g(P)$" is the crossing number test with exact signs, after an exact test for a point on the boundary. The first hit is the minimum of $s > 0$ over the crossings of the ray with the edges, computed exactly. A crossing at an end of an edge, two crossings at the same $s$, or an edge on the line of the ray mark the hit as a vertex, and line L7 skips it. Line L7 then checks $s \le \rho$ and $u \notin \{q_1, q_2, q_3\}$ with exact signs. $\square$

**Lemma 8 (line L8).** Line L8 accepts the four wrenches if and only if they positively span $\mathbb{R}^3$.

*Proof.* The proof of Lemma 4 gives $\sum_i \lambda_i w_i = 0$. If the rank is 3, some $3 \times 3$ minor is not zero, so $\lambda \ne 0$, and the null space of the map $\mu \mapsto \sum_i \mu_i w_i$ has dimension $4 - 3 = 1$, so it is spanned by $\lambda$. Then a strictly positive null vector exists if and only if all $\lambda_i$ are nonzero with one sign. If the rank is less than 3, all $\lambda_i$ are zero, line L8 rejects, and the wrenches do not span $\mathbb{R}^3$. By the positive span lemma, line L8 is right in both cases. The signs are exact by Lemma 5. $\square$

**Theorem.** MODULAR-FIXTURES$(P, \rho)$ outputs each normalized fixture exactly one time, and outputs nothing else.

*Proof.* *Soundness.* An output has $q_1 = (0,0)$ and sites in order by line L2. Lemmas 3 and 6 give condition 1, Lemma 7 gives conditions 2 and 3, and Lemma 8 gives condition 4.

*Completeness.* Take a normalized fixture. By Lemma 2, line L2 tries its sites. Line L3 tries all $n^3$ triples, so it tries its edges. By Lemma 4, line L4 produces its pose. By Lemma 6 the pose passes line L5. By Lemma 7, lines L6 and L7 produce its clamp pair $(v, d)$ with its $u$ and $e$. By Lemma 8, line L8 outputs it.

*Uniqueness.* Two outputs from different iterations differ in the sites, in the pose, or in $(v, d)$. The edges cannot be the only difference: the relative interiors of the edges of a simple polygon are disjoint, so a pose and a site $q_k$ fix the edge that contains $q_k$ in its interior. Two poses of line L4 for the same sites and edges are different points of the circle. So each fixture is output at most one time. $\blacksquare$

**Termination.** The loops of lines L2, L3, L4 and L6 are over finite sets: a finite set of lattice points, $n^3$ triples, at most two poses, and a finite box of holes with four directions.
