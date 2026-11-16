---
title: The centroid step never increases the coverage cost, and the robots approach the set of centroidal Voronoi configurations
proves: [correctness]
status: full
---

Let $Q \subset \mathbb{R}^2$ be a convex polygon with nonempty interior, and let $\phi \ge 0$ be an integrable density on $Q$; the implementation uses $\phi = 1$. For distinct points $P = (p_1, \dots, p_r)$ in $Q$ and a partition $W = (W_1, \dots, W_r)$ of $Q$ into measurable sets, let

$$H(P, W) = \sum_{i=1}^{r} \int_{W_i} \lVert q - p_i \rVert^2 \phi(q)\, dq, \qquad H(P) = H(P, V(P)),$$

where $V(P)$ is the Voronoi partition, $V_i = \{ q \in Q : \lVert q - p_i \rVert \le \lVert q - p_j \rVert \text{ for all } j \}$. For a set $W_i$ with mass $M_i = \int_{W_i} \phi > 0$ the centroid is $C_i = \frac{1}{M_i} \int_{W_i} q \phi(q)\, dq$. Line numbers refer to the pseudocode on the [distributed Lloyd coverage algorithm](/cortes-coverage-algorithm/) page. One step is $p_i' = p_i + k (C_i - p_i)$ with $C_i$ the centroid of $V_i$ and a gain $0 < k < 2$; the page uses $0 < k \le 1$.

**Lemma 1 (the cell is computed exactly).** Lines L3 to L5 return $V_i$.

*Proof.* $\lVert q - p_i \rVert \le \lVert q - p_j \rVert$ is equivalent, after squaring and cancelling $\lVert q \rVert^2$, to $(p_j - p_i) \cdot q \le \frac12 (\lVert p_j \rVert^2 - \lVert p_i \rVert^2)$, a closed half-plane. So $V_i$ is $Q$ intersected with $r - 1$ half-planes. Clipping a convex polygon with a half-plane gives the convex polygon of their intersection, and the order of the clips does not matter. $\square$

**Lemma 2 (parallel axis identity).** For a set $W_i$ with mass $M_i > 0$ and centroid $C_i$, and any point $p$,

$$\int_{W_i} \lVert q - p \rVert^2 \phi(q)\, dq = \int_{W_i} \lVert q - C_i \rVert^2 \phi(q)\, dq + M_i \lVert p - C_i \rVert^2.$$

*Proof.* Write $q - p = (q - C_i) + (C_i - p)$ and expand the square. The cross term is $2 (C_i - p) \cdot \int_{W_i} (q - C_i) \phi(q)\, dq = 2 (C_i - p) \cdot (M_i C_i - M_i C_i) = 0$. $\square$

The implementation uses this identity with $p = 0$ to compute the cost of a cell from its area, its centroid and its polar moment $\int \lVert q \rVert^2 dq$, which the shoelace formulas give exactly.

**Lemma 3 (the best partition for fixed points).** For fixed $P$ and every partition $W$, $H(P, V(P)) \le H(P, W)$.

*Proof.* For each $q \in Q$, the term of $H(P, W)$ at $q$ is $\lVert q - p_i \rVert^2 \phi(q)$ for the $i$ with $q \in W_i$, and the Voronoi partition takes the smallest of these values. The boundaries of the cells have measure zero, so ties do not matter. Integrate over $Q$. $\square$

**Lemma 4 (the best points for a fixed partition).** For a fixed partition $W$ with all $M_i > 0$, $H(P, W) = \sum_i J_i + \sum_i M_i \lVert p_i - C_i \rVert^2$, where $J_i = \int_{W_i} \lVert q - C_i \rVert^2 \phi$ does not depend on $P$. So $H(\cdot, W)$ is smallest exactly when $p_i = C_i$ for all $i$.

*Proof.* Apply Lemma 2 to each cell and add. $\square$

**Lemma 5 (robots stay in $Q$ and stay distinct).** If $\phi = 1$, the points $p_i'$ lie in $Q$, and for $0 < k \le 1$ they are distinct.

*Proof.* $C_i$ is the centroid of the convex set $V_i \subseteq Q$, so $C_i \in V_i$, and $p_i \in V_i$. For $0 < k \le 1$ the point $p_i'$ is a convex combination of the two, so it is in $V_i \subseteq Q$. The centroid of a convex polygon with nonempty interior is an interior point of it, and $V_i$ has nonempty interior because $p_i$ is strictly nearer to itself than to any other robot. A point of the half-open segment from a point of a convex set to an interior point of it is an interior point, so $p_i'$ is in the interior of $V_i$. The interiors of two Voronoi cells do not meet, so $p_i' \ne p_j'$. $\square$

**Theorem 1 (sufficient decrease).** Let $\phi = 1$ and $0 < k \le 1$. Then

$$H(P') \le H(P) - k (2 - k) \sum_{i=1}^{r} M_i \lVert p_i - C_i \rVert^2,$$

with $M_i$ and $C_i$ taken for the cells of $P$. In particular $H(P') \le H(P)$, with equality only when every robot is at the centroid of its cell.

*Proof.* Let $W = V(P)$. By Lemma 5 the new points are distinct and in $Q$. By Lemma 3, $H(P') = H(P', V(P')) \le H(P', W)$. By Lemma 4, $H(P', W) = \sum_i J_i + \sum_i M_i \lVert p_i' - C_i \rVert^2$, and $p_i' - C_i = (1 - k)(p_i - C_i)$. Also $H(P) = H(P, W) = \sum_i J_i + \sum_i M_i \lVert p_i - C_i \rVert^2$. Subtract and use $1 - (1 - k)^2 = k (2 - k)$. Every $M_i > 0$, so the decrease is zero only when $p_i = C_i$ for all $i$. $\square$

**Theorem 2 (the centroid gap goes to zero).** Let $\phi = 1$, $0 < k \le 1$, and let $P(0), P(1), \dots$ be the steps of the algorithm. Then $\sum_{t \ge 0} \sum_i M_i(t) \lVert p_i(t) - C_i(t) \rVert^2 \le H(P(0)) / (k (2 - k))$, so $\sum_i M_i(t) \lVert p_i(t) - C_i(t) \rVert^2 \to 0$.

*Proof.* Add the inequality of Theorem 1 for $t = 0, \dots, T - 1$. The sum telescopes to $H(P(0)) - H(P(T))$, which is at most $H(P(0))$ because $H \ge 0$. A series of nonnegative terms with bounded partial sums has terms that go to zero. $\blacksquare$

**What is not proved here.** Theorem 2 bounds the gap weighted by the masses. To conclude that every limit point of the robots is a centroidal Voronoi configuration one needs that no cell mass goes to zero and that the centroids depend continuously on the points; this is the convergence result of Cortés, Martínez, Karatas and Bullo (2004), proved there with the LaSalle invariance principle for the continuous flow $\dot p_i = -k (p_i - C_i)$ and for the discrete step. The formula $\partial H / \partial p_i = 2 M_i (p_i - C_i)$ for the gradient of $H(P)$, which shows that the centroid step is a step against the gradient, is also from that paper and from Du, Faber and Gunzburger (1999); it is not proved here. The theorems give no rate, and the limit can be a saddle of $H$ and not the global minimum.
