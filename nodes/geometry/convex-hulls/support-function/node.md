---
tag: 5W8GV1
kind: definition
slug: support-function
name: Support function
aliases:
- support function of a convex body
- support mapping
area: geometry/convex-hulls
level: advanced
summary: For a direction u, the maximum of the dot product of u with points of the set.
prereqs: [supporting-hyperplane, convex-set, dot-product]
see_also: [extreme-point, minkowski-sum, gjk-algorithm, convex-conjugate, rotating-calipers, polygon-width, hausdorff-distance, convex-hull-trick]
sources:
  - book: isbn:9781107601017
    title: Rolf Schneider, Convex Bodies, The Brunn-Minkowski Theory, second edition, Cambridge University Press, 2014
    locator: Section 1.7, The support function (properties, Minkowski addition, and the recovery of a closed convex set), and Section 1.8 for the Hausdorff metric
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 13, Support Functions
  - paper: doi:10.1109/56.2083
    title: Elmer G. Gilbert, Daniel W. Johnson and S. Sathiya Keerthi, A fast procedure for computing the distance between complex objects in three-dimensional space, IEEE Journal of Robotics and Automation 4(2), 1988
    locator: the whole paper (the support mapping of a convex set and of a Minkowski difference)
---

The support function of a set $K \subseteq \mathbb{R}^d$ maps each direction $u$ to $h_K(u) = \sup_{x \in K} \langle u, x \rangle$, the largest projection of $K$ on $u$. The hyperplane $\langle u, x \rangle = h_K(u)$ is the [supporting hyperplane](/supporting-hyperplane/) of $K$ with outer normal $u$, and a closed convex set is the intersection of all the half-spaces $\langle u, x \rangle \le h_K(u)$. The support function turns Minkowski sums into sums of functions, gives the width and the diameter of a set, and is the only access to the shape that the [GJK algorithm](/gjk-algorithm/) needs.

## Definition

Let $K \subseteq \mathbb{R}^d$ be nonempty. The **support function** of $K$ is

$$h_K : \mathbb{R}^d \to \mathbb{R} \cup \{+\infty\}, \qquad h_K(u) = \sup_{x \in K} \langle u, x \rangle.$$

If $K$ is compact, $h_K$ is finite and the supremum is a maximum. A **support mapping** $s_K$ picks for each $u$ a point $s_K(u) \in K$ with $\langle u, s_K(u) \rangle = h_K(u)$. For a finite set $P$, $h_P(u) = \max_{p \in P} \langle u, p \rangle$, which takes $O(n)$ time to evaluate, or $O(\log h)$ time by binary search over the $h$ vertices of a [convex polygon](/convex-polygon/) given in order.

**Properties.** For nonempty $K, L \subseteq \mathbb{R}^d$, all $u, v \in \mathbb{R}^d$ and all $\lambda \ge 0$:

1. **Positive homogeneity:** $h_K(\lambda u) = \lambda h_K(u)$ (with $0 \cdot \infty = 0$).
2. **Subadditivity:** $h_K(u + v) \le h_K(u) + h_K(v)$. With item 1, $h_K$ is convex.
3. **Hull invariance:** $h_K = h_{\operatorname{conv} K} = h_{\overline{\operatorname{conv}} K}$.
4. **Minkowski sum:** $h_{K + L} = h_K + h_L$ and $h_{\lambda K} = \lambda h_K$, where $K + L = \{x + y : x \in K, y \in L\}$.
5. **Reflection and union:** $h_{-K}(u) = h_K(-u)$ and $h_{K \cup L} = \max(h_K, h_L)$.
6. **Recovery:** if $K$ is closed and convex, then $K = \bigcap_{u} \{x : \langle u, x \rangle \le h_K(u)\}$.
7. **Order:** if $K$ and $L$ are closed and convex, then $K \subseteq L$ if and only if $h_K \le h_L$.

*Proofs.* Item 1: $\sup \langle \lambda u, x \rangle = \lambda \sup \langle u, x \rangle$. Item 2: $\langle u + v, x \rangle = \langle u, x \rangle + \langle v, x \rangle \le h_K(u) + h_K(v)$ for each $x \in K$. Item 3: a linear function is at most $h_K(u)$ on $K$, so on each convex combination of points of $K$, and by continuity on the closure. Item 4: $\langle u, x + y \rangle = \langle u, x \rangle + \langle u, y \rangle$, and the two suprema are taken over independent choices of $x$ and $y$. Item 5 is direct. Item 6: $K$ lies in each half-space. If $y \notin K$, the nearest point $z \in K$ to $y$ satisfies $\langle y - z, x - z \rangle \le 0$ for $x \in K$ (the projection inequality proved on the page [supporting hyperplane](/supporting-hyperplane/)). With $u = y - z \ne 0$ this gives $h_K(u) \le \langle u, z \rangle < \langle u, z \rangle + |u|^2 = \langle u, y \rangle$, so $y$ is outside the half-space for $u$. Item 7: if $K \subseteq L$ the suprema compare. If $h_K \le h_L$, each half-space of item 6 for $L$ contains $K$, so $K \subseteq L$. $\square$

Conversely, every positively homogeneous, subadditive and finite function on $\mathbb{R}^d$ is the support function of exactly one nonempty compact convex set (Schneider, Theorem 1.7.1). In the language of convex analysis, $h_K$ is the [convex conjugate](/convex-conjugate/) of the indicator function of $K$.

**Derived measures.** For a compact set $K$ and a unit vector $u$:

- The **width** in direction $u$ is $w_K(u) = h_K(u) + h_K(-u)$, the distance between the two supporting hyperplanes with normals $u$ and $-u$. The width of $K$ is $\min_u w_K(u)$; see [polygon width](/polygon-width/).
- The **diameter** is $\max_u w_K(u)$, because $\max_u \bigl(h_K(u) + h_K(-u)\bigr) = \max_u \max_{x, y \in K} \langle u, x - y \rangle = \max_{x, y \in K} |x - y|$. See [polygon diameter](/polygon-diameter/).
- For compact convex $K$ and $L$, the [Hausdorff distance](/hausdorff-distance/) is $\max_{|u| = 1} |h_K(u) - h_L(u)|$ (Schneider, Section 1.8).

## Examples and non-examples

- **Unit disk.** $h(u) = |u|$, attained at $u / |u|$.
- **Square** $[-1, 1]^2$: $h(u) = |u_1| + |u_2|$, attained at the corner $(\operatorname{sign} u_1, \operatorname{sign} u_2)$.
- **Segment** $[a, b]$: $h(u) = \max(\langle u, a \rangle, \langle u, b \rangle)$.
- **A pentagon.** For the polygon with vertices $(0,0)$, $(5,0)$, $(7,3)$, $(3,6)$, $(0,4)$: $h(1, 0) = 7$, $h(-1, 0) = 0$, $h(0, 1) = 6$, $h(0, -1) = 0$, $h(1, 1) = 10$ and $h(-1, -1) = 0$. So the horizontal width is $7$, the vertical width is $6$, and the width in direction $(1,1)/\sqrt{2}$ is $10/\sqrt{2} \approx 7.07$.
- **A Minkowski sum.** For the square $S$ with corners $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$ and the segment $T$ from $(0,0)$ to $(3,1)$, $h_S(1, -2) = 2$ and $h_T(1, -2) = 1$, and the sum $S + T$ has $h_{S+T}(1, -2) = 3$. Item 4 holds for all 1000 seeded random integer directions in $[-9, 9]^2$ when $S + T$ is computed point by point.
- **Upper envelope of lines.** For the lines $y = a_i x + b_i$ with $(a_i, b_i) \in P = \{(1, 3), (-2, 1), (0, 0), (3, -4)\}$, the value $\max_i (a_i x + b_i)$ equals $h_P(x, 1)$. At $x = -2, 0, 1, 5$ it is $5, 3, 4, 11$. The maximum is always attained at a vertex of the [upper hull](/upper-and-lower-hull/) of $P$, and $(0, 0)$, which lies below that hull, never attains it. This is the idea behind the [convex hull trick](/convex-hull-trick/).
- **Non-example: unbounded sets.** For the half-plane $\{y \le 0\}$, $h(u) = +\infty$ unless $u = (0, t)$ with $t \ge 0$, where $h(u) = 0$. The support function exists but is not finite.
- **Non-example: not determined by a non-convex set.** The set $\{(1,0), (-1,0)\}$ and the segment between those points have the same support function, so $h_K$ determines only the closed convex hull of $K$.

## Related definitions

- [Supporting hyperplane](/supporting-hyperplane/): the hyperplane $\langle u, x \rangle = h_K(u)$.
- [Extreme point](/extreme-point/): a unique maximizer of $\langle u, \cdot \rangle$ is an exposed point.
- [Minkowski sum](/minkowski-sum/) and [Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/): the operation that support functions add.
- [GJK algorithm](/gjk-algorithm/) and [convex collision detection](/convex-collision-detection/): they access a convex shape only through a support mapping, with $s_{K - L}(u) = s_K(u) - s_L(-u)$.
- [Rotating calipers](/rotating-calipers/), [polygon width](/polygon-width/) and [polygon diameter](/polygon-diameter/): they scan $h_K(u) + h_K(-u)$ over the critical directions of a polygon.
- [Convex conjugate](/convex-conjugate/): the general duality behind the definition.

## References
