---
tag: 1X10R6
kind: definition
slug: supporting-hyperplane
name: Supporting hyperplane
aliases:
- supporting line
- supporting line of a convex polygon
- tangent line of a convex polygon
area: geometry/convex-hulls
level: intro
summary: A hyperplane touching a convex set while leaving the whole set on one side.
prereqs: [convex-set, dot-product]
see_also: [support-function, extreme-point, facet, supporting-hyperplane-theorem, separating-hyperplane-theorem, rotating-calipers, chan-algorithm, dynamic-convex-hull]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.5.2, Supporting hyperplanes (definition and the supporting hyperplane theorem)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 11, Separation Theorems (supporting hyperplanes to a convex set)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, the supporting lines of a convex polygon from an external point and their search in logarithmic time
---

A supporting hyperplane of a set $C \subseteq \mathbb{R}^d$ is a hyperplane that meets $C$ and has all of $C$ in one of its two closed half-spaces. In the plane it is a supporting line: a line that touches a [convex polygon](/convex-polygon/) at a vertex or along an edge and does not cut through it. Supporting hyperplanes define the faces of a polytope, the [support function](/support-function/), and the tangent searches inside many hull algorithms.

## Definition

A **hyperplane** in $\mathbb{R}^d$ is a set $H(a, \beta) = \{x : \langle a, x \rangle = \beta\}$ with $a \in \mathbb{R}^d \setminus \{0\}$ and $\beta \in \mathbb{R}$. Its closed half-spaces are $H^-(a, \beta) = \{x : \langle a, x \rangle \le \beta\}$ and $H^+(a, \beta) = \{x : \langle a, x \rangle \ge \beta\}$.

Let $C \subseteq \mathbb{R}^d$ be nonempty and closed. The hyperplane $H = H(a, \beta)$ **supports** $C$ if

$$C \subseteq H^-(a, \beta) \quad \text{and} \quad C \cap H \ne \emptyset.$$

It supports $C$ **at** each point $x_0 \in C \cap H$, and $a$ is then an **outer normal** of $C$ at $x_0$. The two conditions say that $\beta = \max_{x \in C} \langle a, x \rangle$, so for each $a \ne 0$ there is at most one supporting hyperplane with outer normal $a$, and there is exactly one when the maximum is attained, for example when $C$ is compact. A supporting hyperplane is **proper** if $C \not\subseteq H$. For a set that is not closed, the usual convention replaces $C \cap H \ne \emptyset$ with $\overline{C} \cap H \ne \emptyset$.

**Theorem (supporting hyperplane theorem).** If $C \subseteq \mathbb{R}^d$ is closed and convex and $x_0$ is a boundary point of $C$, then some hyperplane supports $C$ at $x_0$.

*Proof.* For $y \notin C$ let $\pi(y)$ be the point of $C$ nearest to $y$. It exists because $C$ is closed, and for each $x \in C$ it satisfies $\langle y - \pi(y), x - \pi(y) \rangle \le 0$: the point $\pi(y) + t(x - \pi(y))$ is in $C$ for $t \in (0, 1]$, so $|y - \pi(y)|^2 \le |y - \pi(y) - t(x - \pi(y))|^2$, which gives $2t \langle y - \pi(y), x - \pi(y) \rangle \le t^2 |x - \pi(y)|^2$; divide by $t$ and let $t \to 0$. Since $x_0$ is a boundary point, there are points $y_k \notin C$ with $y_k \to x_0$. Let $a_k = (y_k - \pi(y_k)) / |y_k - \pi(y_k)|$. Then $|\pi(y_k) - x_0| \le |\pi(y_k) - y_k| + |y_k - x_0| \le 2|y_k - x_0|$, because $x_0 \in C$ is not nearer to $y_k$ than $\pi(y_k)$. So $\pi(y_k) \to x_0$. The unit vectors $a_k$ have a convergent subsequence with a unit limit $a$. Passing to the limit in $\langle a_k, x - \pi(y_k) \rangle \le 0$ gives $\langle a, x \rangle \le \langle a, x_0 \rangle$ for all $x \in C$, so $H(a, \langle a, x_0 \rangle)$ supports $C$ at $x_0$. $\square$

The page [supporting hyperplane theorem](/supporting-hyperplane-theorem/) treats the general form for convex sets that are not closed.

**Faces.** The intersection of a convex set with a supporting hyperplane is a *face*. For a polytope these exposed faces are the vertices, the edges and so on up to the [facets](/facet/). A point is an exposed point when a supporting hyperplane meets $C$ only there; every exposed point is an [extreme point](/extreme-point/).

**Supporting lines of a convex polygon.** Let $v_0, \ldots, v_{h-1}$ be the vertices of a strictly convex polygon in counterclockwise order, with indices modulo $h$ and $h \ge 3$.

- The line through $v_i$ and $v_j$ supports the polygon if and only if $j = i \pm 1$, that is, the segment is an edge.
- A line through $v_i$ supports the polygon at $v_i$ alone if and only if $v_{i-1}$ and $v_{i+1}$ lie strictly on the same side of it. The outer normals at $v_i$ form the cone between the outer normals of the edges $v_{i-1} v_i$ and $v_i v_{i+1}$.
- From a point $q$ outside the polygon there are exactly two supporting lines through $q$. The line $q v_i$ is one of them if and only if $\mathrm{orient}(q, v_i, v_{i-1})$ and $\mathrm{orient}(q, v_i, v_{i+1})$ are not of opposite strict signs. Here orient is the [orientation test](/orientation-test/). The two tangent vertices split the polygon into a near chain and a far chain, and each tangent vertex can be found by binary search in $O(\log h)$ time.

## Examples and non-examples

- **A square.** For $C = [0, 2]^2$ the line $x + y = 4$ supports $C$ at the corner $(2, 2)$ only, with outer normal $(1, 1)$. The line $x = 2$ supports $C$ along the whole right side. The line $x + y = 3$ is not supporting: it has $(2, 2)$ on one side and $(0, 0)$ on the other.
- **A pentagon.** For the polygon $(0,0)$, $(5,0)$, $(7,3)$, $(3,6)$, $(0,4)$, the supporting line with outer normal $(1, 1)$ is $x + y = 10$, which touches $(7, 3)$. With outer normal $(-1, 2)$ it is $-x + 2y = 9$, which touches $(3, 6)$.
- **Tangents from a point.** For the rectangle $(0,0)$, $(4,0)$, $(4,3)$, $(0,3)$ and $q = (6, 5)$, the pairs $\bigl(\mathrm{orient}(q, v, v_{\text{prev}}), \mathrm{orient}(q, v, v_{\text{next}})\bigr)$ for the four vertices are $(-18, 20)$, $(-20, -6)$, $(6, -8)$ and $(8, 18)$. Only $(4, 0)$ and $(0, 3)$ have both neighbors on one side, so the tangents from $q$ are the lines $q(4,0)$ and $q(0,3)$.
- **A disk.** At each boundary point of a closed disk the tangent line is the only supporting line.
- **Non-example: a line through an inner point.** A line through an interior point of $C$ has points of $C$ on both sides.
- **Non-example: no contact.** The line $x = 3$ has $[0, 2]^2$ on one side but does not meet it. It is a separating line, not a supporting one.
- **Non-example: unattained supremum.** For the closed set $C = \{(x, y) : y \ge e^x\}$ and $a = (0, -1)$, $\sup_{x \in C} \langle a, x \rangle = 0$ is not attained, and no supporting line has outer normal $a$.

## Related definitions

- [Support function](/support-function/): the value $\beta = h_C(a)$ of the supporting hyperplane with outer normal $a$.
- [Extreme point](/extreme-point/) and [facet](/facet/): the faces cut out by supporting hyperplanes.
- [Supporting hyperplane theorem](/supporting-hyperplane-theorem/) and [separating hyperplane theorem](/separating-hyperplane-theorem/): the existence results of convex analysis.
- [Rotating calipers](/rotating-calipers/): a pair of parallel supporting lines turned around a convex polygon.
- [Chan's algorithm](/chan-algorithm/), [dynamic convex hull](/dynamic-convex-hull/) and [divide-and-conquer hull](/divide-and-conquer-convex-hull/): they find tangents and common tangents (bridges) of convex polygons.

## References
