---
title: Lloyd's algorithm is well defined and never increases the energy
proves: [correctness]
status: full
---

**Claim.** Let $B = [x_0, x_1] \times [y_0, y_1]$ with $x_0 < x_1$ and $y_0 < y_1$, with the uniform density, and let $z_1, \ldots, z_n$ be distinct points of $B$, $n \ge 1$. Let $V_i$ be the Voronoi cell of $z_i$ clipped to $B$, $m_i$ its area, $z_i^*$ its centroid, and

$$\mathcal{E}(z) = \sum_{i=1}^{n} \int_{V_i} |x - z_i|^2 \, dx.$$

Then (a) every $V_i$ is a convex polygon with $m_i > 0$; (b) the points $z_1^*, \ldots, z_n^*$ are distinct and lie in the interior of $B$; (c) $\mathcal{E}(z^*) \le \mathcal{E}(z) - \sum_i m_i |z_i - z_i^*|^2$, so the energy never increases, and it stays the same only when $z^* = z$; (d) $z$ is a fixed point of one step exactly when $z$ gives a centroidal Voronoi tessellation of $B$. So every step of LLOYD is well defined, the iterates stay distinct points of $B$, and the energies form a non-increasing sequence. The code computes each step exactly.

**Notation.** For a set $W \subseteq B$ of positive area $m$, its centroid is $c(W) = \frac{1}{m}\int_W x \, dx$. For a point $z$ and a partition $W_1, \ldots, W_n$ of $B$ into sets that overlap only on boundaries of zero area, $E(z; W) = \sum_i \int_{W_i} |x - z_i|^2 \, dx$.

**Lemma 1 (cells).** $V_i = B \cap \bigcap_{j \ne i} H_{ij}$ with $H_{ij} = \{x : 2 (z_j - z_i) \cdot x \le |z_j|^2 - |z_i|^2\}$, and $V_i$ is a convex polygon of positive area. The cells cover $B$, and two cells meet only on a segment.

*Proof.* $|x - z_i|^2 \le |x - z_j|^2$ expands to $2 (z_j - z_i) \cdot x \le |z_j|^2 - |z_i|^2$, a closed half-plane, as $z_j \ne z_i$. So $V_i$ is the intersection of $B$ with finitely many closed half-planes, a convex polygon. Let $r > 0$ be half the smallest distance from $z_i$ to another site. The disc of radius $r$ around $z_i$ is in every $H_{ij}$. Let $D'$ be a closed disc in the interior of $B$. For $0 < t \le 1$ the disc $z_i + t (D' - z_i)$ is in $B$, because $B$ is convex and holds $z_i$ and $D'$; for small $t$ it is also within distance $r$ of $z_i$, so it is in $V_i$. It has positive area, so $m_i > 0$. Every point of $B$ has a nearest site, so the cells cover $B$. The interiors of $V_i$ and $V_j$ lie in the open half-planes $|x - z_i| < |x - z_j|$ and $|x - z_j| < |x - z_i|$, which are disjoint, so the cells meet only on the bisector. $\square$

**Lemma 2 (centroid).** The centroid of a convex polygon $W$ of positive area lies in its interior.

*Proof.* Suppose $c = c(W)$ is not in the interior. Since $W$ is convex and closed, there is a unit vector $u$ with $u \cdot x \le u \cdot c$ for all $x \in W$ (a supporting line at a boundary point, or a separating line if $c \notin W$). Then $\int_W u \cdot (c - x) \, dx = 0$ by the definition of $c$, while the integrand is $\ge 0$ and is $> 0$ on the interior of $W$, which has positive area. This is a contradiction. $\square$

**Lemma 3 (parallel axis).** For a set $W$ of area $m > 0$ with centroid $c$ and any point $z$, $\int_W |x - z|^2 dx = \int_W |x - c|^2 dx + m |z - c|^2$.

*Proof.* Write $x - z = (x - c) + (c - z)$ and expand: the cross term is $2 (c - z) \cdot \int_W (x - c) \, dx = 0$. $\square$

**Lemma 4 (nearest site).** For fixed points $z$ and any partition $W$ as above, $E(z; V) \le E(z; W)$, where $V$ is the Voronoi partition of $z$.

*Proof.* Each point $x$ of $W_i$ pays $|x - z_i|^2 \ge \min_j |x - z_j|^2$, and in $V$ it pays the minimum; the boundaries have zero area. $\square$

**Proof of the claim.** (a) is Lemma 1. (b) By Lemma 2 each $z_i^*$ is in the interior of $V_i$, which lies in the interior of $B$; the interiors of different cells are disjoint by Lemma 1, so the $z_i^*$ are distinct. (c) $\mathcal{E}(z) = E(z; V)$, where $V$ is the Voronoi partition of $z$. By Lemma 3 applied to each cell, $E(z; V) = E(z^*; V) + \sum_i m_i |z_i - z_i^*|^2$. By Lemma 4 for the points $z^*$, $\mathcal{E}(z^*) = E(z^*; V^*) \le E(z^*; V)$, where $V^*$ is the Voronoi partition of $z^*$. Together these give (c). If $\mathcal{E}(z^*) = \mathcal{E}(z)$, then $\sum_i m_i |z_i - z_i^*|^2 = 0$ and all $m_i > 0$, so $z^* = z$. (d) $z$ is a fixed point exactly when $z_i = z_i^*$ for all $i$, which is the definition of a centroidal Voronoi tessellation.

*Exact computation.* The code builds $V_i$ by clipping $B$ with the half-planes $H_{ij}$ of Lemma 1, in rational arithmetic, so it gets $V_i$ exactly. For a counterclockwise polygon with vertices $p_0, \ldots, p_{k-1}$, split it into the signed triangles $(0, p_t, p_{t+1})$, indices mod $k$; the triangle has signed area $\frac{1}{2} p_t \times p_{t+1}$ and centroid $(p_t + p_{t+1})/3$, and the signed areas add up to the area of the polygon for every polygon, by the shoelace formula. So $\int_W x \, dx = \frac{1}{6} \sum_t (p_t + p_{t+1}) (p_t \times p_{t+1})$, which is the formula of the code, and the centroid is this divided by the area. So the code computes $z^*$ exactly. $\blacksquare$

*What is not proved here.* By (c) the energies converge and $\sum_k \sum_i m_i^{(k)} |z_i^{(k)} - z_i^{(k+1)}|^2 \le \mathcal{E}(z^{(0)})$. Whether the sites themselves converge, and how fast, is a separate question. Du, Faber and Gunzburger discuss the convergence of the iteration; global convergence in one dimension for log-concave densities, with a linear rate, is in the work of Du, Emelianenko and Ju. These results are cited on the page and not proved here.
