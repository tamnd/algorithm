---
tag: ZW1MPP
kind: definition
slug: ferrari-canny-metric
name: Ferrari-Canny metric
aliases:
- epsilon quality metric
- largest minimum resisted wrench
area: robotics/grasping-and-manipulation
level: advanced
summary: The radius of the largest ball about the origin inside the grasp wrench space, the size of wrench that the grasp resists in every direction per unit of finger force.
prereqs: [grasp-wrench-space, support-function]
see_also: [grasp-wrench-space, grasp-quality-measures, force-closure, force-closure-test, support-function, quickhull, minkowski-sum, grasp-synthesis]
sources:
  - paper: doi:10.1109/ROBOT.1992.219918
    title: "Carlo Ferrari and John Canny, Planning optimal grasps, Proceedings of the IEEE International Conference on Robotics and Automation, vol. 3, 2290-2295, 1992"
    locator: the two quality criteria, the largest ball in the wrench space with the sum of the finger forces bounded and with the largest finger force bounded
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4.1 (Form Closure), the paragraph on monotonicity, and Section 38.5 (Examples), where the metric is compared with the LP1 metric; the chapter is pages 955 to 988. Its reference list gives the year of Ferrari and Canny as 1986; the paper is from 1992"
  - paper: doi:10.1007/s10514-014-9402-3
    title: "Máximo A. Roa and Raúl Suárez, Grasp quality measures: review and performance, Autonomous Robots 38(1), 65-88, 2015"
    locator: the metric among the measures based on the grasp wrench space, and its dependence on the torque scale
  - paper: doi:10.1007/BF02187843
    title: "David G. Kirkpatrick, Bhubaneswar Mishra and Chee-Keng Yap, Quantitative Steinitz's theorems with applications to multifingered grasping, Discrete and Computational Geometry 7(3), 295-318, 1992"
    locator: quantitative versions of the theorem of Steinitz for a ball about the origin inside a convex hull, applied to the choice of finger positions
---

The Ferrari-Canny metric scores a grasp by its weakest direction. Take the [grasp wrench space](/grasp-wrench-space/), the set of wrenches that the fingers can apply with a unit budget of force, and find the largest ball centered at the origin that fits inside it. Its radius $\varepsilon$ is the metric. Every wrench of size at most $\varepsilon$, in any direction, can be resisted with the unit budget, and some wrench of size slightly above $\varepsilon$ cannot. A grasp that is not in [force closure](/force-closure/) has $\varepsilon = 0$. Ferrari and Canny proposed it in 1992 to choose the best contacts for a grasp, and it is widely used in grasp planning.

## Definition

A grasp has the primitive wrenches $w_{ij}$, contact $i$ and cone edge $j$, with normal components 1, and the grasp wrench space $W$, either $W_{L_1}$ (total normal force at most 1) or $W_{L_\infty}$ (each normal force at most 1). Wrenches are compared with the Euclidean norm on $\mathbb{R}^d$, after a choice of reference point and of a length $\rho$ that converts moments into force units.

**Ferrari-Canny metric.** The metric is the radius of the largest closed ball centered at the origin that lies in $W$:

$$\varepsilon(W) = \max\{\, r \ge 0 : B(0, r) \subseteq W \,\}.$$

The $L_1$ version $\varepsilon_1$ uses $W_{L_1}$, the $L_\infty$ version $\varepsilon_\infty$ uses $W_{L_\infty}$.

**As a support function.** For a closed convex set $W$ containing the origin, the ball of radius $r$ lies in $W$ exactly when the [support function](/support-function/) $h_W(u) = \max_{w \in W} u^T w$ is at least $r$ in every unit direction $u$. So

$$\varepsilon(W) = \max\Big(0,\ \min_{\lVert u \rVert = 1} h_W(u)\Big), \qquad h_{W_{L_1}}(u) = \max\big(0, \max_{i,j} u^T w_{ij}\big).$$

For a polytope written as $W = \{x : a_f^T x \le b_f\}$ with unit facet normals $a_f$, the minimum is attained at a facet normal, and $\varepsilon = \min_f b_f$, the distance from the origin to the nearest facet.

**What the number means.** Let $\mathcal{F}$ be an external wrench with $\lVert \mathcal{F} \rVert \le \varepsilon$. Then $-\mathcal{F}$ is in the ball, so it is in $W$, and the fingers can apply it with a unit budget, which balances $\mathcal{F}$. By scaling, a wrench of size $s$ needs a budget of at most $s / \varepsilon$. So $1 / \varepsilon$ is the largest force that the fingers may need per unit of disturbance, over all directions.

Properties that follow from the definition:

- $\varepsilon > 0$ exactly when the grasp is in force closure, because the origin is then interior to $W$.
- $\varepsilon_1 \le \varepsilon_\infty \le c\, \varepsilon_1$ for $c$ contacts, from $W_{L_1} \subseteq W_{L_\infty} \subseteq c\, W_{L_1}$.
- Adding a contact enlarges $W$, so $\varepsilon$ cannot decrease. The Handbook notes this monotonicity and contrasts it with the LP measure of its form closure test, which can drop when a contact is added.
- With inner pyramids in place of the friction cones, $W$ shrinks, so the computed $\varepsilon$ is a lower bound for the metric of the exact cones.
- $\varepsilon$ depends on the length $\rho$ and on the reference point, as the review of Roa and Suárez (2015) discusses; the Handbook makes the same remark about the value of its linear program test. A common choice is the center of mass as the reference point and a length of the size of the object as $\rho$, but no choice is canonical.

## Examples and non-examples

**Two fingers on a box.** Fingers at $(-1, 0)$ and $(1, 0)$ on a planar box, with inward normals along $x$, moments taken about the center and divided by a length $\rho$. The values below come from the facets of the exact polytopes.

| $\mu$ | $\rho$ | $\varepsilon_1$ | $\varepsilon_\infty$ |
|---|---|---|---|
| 0.25 | 1 | 0.1741 | 0.3333 |
| 0.5 | 0.5 | 0.4082 | 0.6667 |
| 0.5 | 1 | 0.3333 | 0.5774 |
| 0.5 | 2 | 0.2182 | 0.4082 |
| 1.0 | 1 | 0.5774 | 0.8165 |

More friction gives a larger ball. A larger $\rho$ makes the same physical moments smaller numbers, flattens the polytope in the moment direction, and makes $\varepsilon$ smaller. For $\mu = 0.5$ the $L_1$ polytope is a tetrahedron whose faces are at the distance $s / \sqrt{4 + 5 s^2}$ with $s = 1/\rho$; this gives the three values $0.4082$, $0.3333$ and $0.2182$.

**The same grasp about another point.** Take the moments of the box grasp with $\mu = 0.5$ and $\rho = 1$ about a point $0.5$ below the line of the fingers. The contacts are then at $(\pm 1, 0.5)$ in the new frame, and the metric drops to $\varepsilon_1 = 0.2887$ and $\varepsilon_\infty = 0.4851$. The grasp is the same; the number is not.

**Three fingers on a disc.** Three fingers at 120 degrees on a unit disc press toward the center. The normal forces have no moment about the center, so moments come only from friction. With $\mu = 0.25$, $\varepsilon_1 = 0.25$ and $\varepsilon_\infty = 0.6748$; with $\mu = 0.5$, $\varepsilon_1 = 0.5$ and $\varepsilon_\infty = 0.9983$.

**A frictionless square.** The four contacts on the square of the [form closure](/form-closure/) page give a tetrahedron in $\mathbb{R}^3$ with $\varepsilon_1 = 0.2665$ and $\varepsilon_\infty = 0.5895$.

**Non-example: the pinwheel.** The pinwheel contacts on the same square are not in form closure, and $\varepsilon = 0$. A positive number would be a bug in the code.

**Non-example: the volume.** The volume of $W$ is another measure. A long thin polytope can have a large volume and a tiny inscribed ball, so a grasp that is weak in one direction can still score well by volume. The Ferrari-Canny metric does not have this defect, but it ignores every direction except the worst one.

## Related definitions

- [Grasp wrench space](/grasp-wrench-space/): the polytope whose inscribed ball the metric measures.
- [Grasp quality measures](/grasp-quality-measures/): the family of scores; this one is the most used of those based on the wrench space.
- [Force closure](/force-closure/): the qualitative property that $\varepsilon > 0$ detects.
- [Support function](/support-function/): the metric is the minimum of the support function over unit directions.
- [Quickhull](/quickhull/): computes the facets of $W_{L_1}$, from which $\varepsilon_1$ is the smallest facet offset. In $\mathbb{R}^6$ the number of facets can be large, and many planners instead sample directions $u$; the minimum of $h_W(u)$ over the sample is an upper bound on $\varepsilon$.
- [Grasp synthesis](/grasp-synthesis/): planners search for contacts that maximize $\varepsilon$.

## References
