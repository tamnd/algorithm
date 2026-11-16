---
tag: T5V3Y0
kind: definition
slug: force-closure
name: Force closure
aliases:
- force-closure grasp
area: robotics/grasping-and-manipulation
level: core
summary: A grasp is in force closure when contact forces inside the friction cones can balance every external wrench on the object, given enough squeeze.
prereqs: [form-closure, friction-cone, grasp-matrix]
see_also: [force-closure-test, antipodal-grasp, grasp-wrench-space, ferrari-canny-metric, polyhedral-friction-cone, grasp-synthesis, fixture-planning, kinematic-fixture-analysis]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 12, Section 12.2.3 (Force Closure), with the edges of the friction cones as columns of a matrix F, and Section 12.2.4 (Duality of Force and Motion Freedoms)"
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4.2 (Force Closure), Definition 38.9 (frictional form closure, quoted from Murray, Li and Sastry) and Definition 38.10 (force closure with the hand); the chapter is pages 955 to 988"
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (grasp statics and force closure); the Handbook cites the rank and interior condition as their Proposition 5.2
  - paper: doi:10.1177/027836498800700301
    title: "Van-Duc Nguyen, Constructing force-closure grasps, International Journal of Robotics Research 7(3), 3-16, 1988"
    locator: the construction of planar force-closure grasps and the two-finger condition
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 5 (Rigid Body Statics), Section 5.3 (contact wrenches and wrench cones) and Section 5.8 (the force dual)
---

A grasp is in force closure when the fingers, by pressing on the object with forces that do not slip, can balance any force and moment that the world puts on the object. It is the friction version of [form closure](/form-closure/): friction lets each finger push sideways, so fewer fingers are needed, but the fingers must squeeze actively, and harder for larger loads. Two fingers can hold a box in the plane this way, and three can hold it in space. Force closure is the basic yes or no question of grasp analysis, and the [grasp wrench space](/grasp-wrench-space/) and the [Ferrari-Canny metric](/ferrari-canny-metric/) turn it into a number.

## Definition

A rigid object is held by $c$ contacts. Contact $i$ has a [contact model](/grasp-contact-models/) with force components $\lambda_i$ and a cone $FC_i$ of allowed components: a ray for a frictionless point, the [friction cone](/friction-cone/) $\lVert f_t \rVert \le \mu f_n$ for a hard finger, and the friction cone with $\lvert m_n \rvert \le \gamma f_n$ for a soft finger. Let $FC = FC_1 \times \cdots \times FC_c$ and let $G$ be the [grasp matrix](/grasp-matrix/), so the contacts apply the wrench $G\lambda$. The wrench space has dimension $d$: 3 in the plane and 6 in space.

**Force closure.** The grasp is in force closure if for every external wrench $\mathcal{F}_{ext} \in \mathbb{R}^d$ there are contact forces $\lambda \in FC$ with

$$G \lambda + \mathcal{F}_{ext} = 0.$$

In short, $G(FC) = \mathbb{R}^d$: the cone of all contact wrenches is the whole wrench space.

**The rank and interior form.** The grasp is in force closure if and only if

1. $\operatorname{rank} G = d$, and
2. some $\lambda_0$ in the interior of $FC$ has $G\lambda_0 = 0$.

Condition 2 asks for an internal force, a squeeze, that is strictly inside every cone. Proof. Assume both conditions. Given a wrench $w$, the rank condition gives some $\lambda_1$, maybe outside the cones, with $G\lambda_1 = w$. Since $\lambda_0$ is interior, $\lambda_0 + \lambda_1 / t$ is in $FC$ for $t$ large, and $FC$ is a cone, so $\lambda = t\lambda_0 + \lambda_1$ is in $FC$ with $G\lambda = w$. Conversely, $G(FC) = \mathbb{R}^d$ forces $\operatorname{rank} G = d$. Take any $x$ in the interior of $FC$, and pick $\lambda' \in FC$ with $G\lambda' = -Gx$. The sum of an interior point and a point of a convex cone is interior, so $\lambda_0 = x + \lambda'$ is interior with $G\lambda_0 = 0$. $\square$

The proof shows the price of friction: the squeeze $t$ grows with the size of the load.

**With linearized cones.** Replace each cone by a [polyhedral friction cone](/polyhedral-friction-cone/) with edges $e_{ij}$. Each edge gives a primitive wrench $w_{ij} = G_i e_{ij}$, and the contact wrenches are the nonnegative combinations of the $w_{ij}$. Force closure then means that the primitive wrenches positively span $\mathbb{R}^d$, which holds if and only if they have rank $d$ and a strictly positive combination of them is zero. The [force-closure test](/force-closure-test/) decides this with one linear program. If the pyramids lie inside the true cones, a positive answer also holds for the true cones.

**The motion view.** As for form closure, the [separating hyperplane theorem](/separating-hyperplane-theorem/) turns a failure of force closure into a twist: if $G(FC) \ne \mathbb{R}^d$, some twist $\mathcal{V} \ne 0$ has $w^T \mathcal{V} \ge 0$ for every contact wrench $w$, so no contact force can do negative work against it. With $\mu = 0$ the condition is exactly first-order form closure.

**Two definitions in the literature.** The definition above is a property of the contacts and the cones alone. Murray, Li and Sastry call it force closure. The Handbook calls it frictional form closure (its Definition 38.9), and keeps the name force closure (Definition 38.10) for a stricter property: in addition, the hand must be able to apply the needed internal forces, which it writes as $\mathcal{N}(G) \cap \mathcal{N}(J^T) = 0$ with $J$ the hand Jacobian. A page or a paper that uses the term should say which one it means. This page uses the first.

Properties that follow from the definition:

- Force closure is unchanged by a change of the reference point or of units, because these act on $G$ by an invertible matrix.
- Adding a contact, or increasing a friction coefficient, can only enlarge $G(FC)$, so it keeps force closure.
- Force closure is open: a small move of the contacts or a small change of the normals keeps it, because the rank and interior conditions are strict. First-order form closure is open in the same way.

## Examples and non-examples

**Two fingers on a box in the plane.** Fingers at $(-1, 0)$ and $(1, 0)$ press along the normals $(1, 0)$ and $(-1, 0)$, with $\mu = 0.5$. The squeeze $\lambda_0$ with both normal forces equal to 1 and no tangential force is interior to both cones, and $G\lambda_0 = 0$. The grasp matrix of this pair has rank 3. So the grasp is in force closure. This is an [antipodal grasp](/antipodal-grasp/).

**An off-axis pair.** Move the fingers to $(-1, 0.5)$ and $(1, -0.5)$, with the same normals. The line between them makes the angle $\arctan(0.5) \approx 26.57$ degrees with the normals. A squeeze along that line is inside both cones only if $\arctan \mu > 26.57$ degrees. With $\mu = 0.6$ the grasp is in force closure; the [force-closure test](/force-closure-test/) finds the positive combination $k = (1, 11, 1, 11)$ of the four cone edges. With $\mu = 0.5$ the line lies on the boundary of both cones: the squeeze exists but is not interior, some moments about the midpoint cannot be balanced, and the grasp is not in force closure. With $\mu = 1/3$ it fails by a margin.

**Two hard fingers in space.** Put the box in space, with hard fingers at $(\pm 1, 0, 0)$ and $\mu = 0.5$. Every contact force passes through a point of the $x$ axis, so it has no moment about that axis. The rank of $G$ is 5, and the grasp cannot resist a twist about the line of the fingers. It is not in force closure for any $\mu$.

**Two soft fingers in space.** Make the same two fingers soft, with $\gamma = 0.1$. Each finger can now apply a moment of up to $0.1 f_n$ about its normal, which is the $x$ axis. The rank is 6 and the squeeze is interior, so the grasp is in force closure. This is the Handbook's statement that two soft fingers suffice in space.

**Three hard fingers in space.** Fingers at $(-1, 0, 0)$ with normal $(1, 0, 0)$ and at $(1, \pm 0.5, 0)$ with normal $(-1, 0, 0)$, with $\mu = 0.5$, are in force closure. The three points are not collinear, so the moments of the forces span all three axes.

**Non-example: three frictionless contacts in the plane.** Three wrenches in $\mathbb{R}^3$ cannot positively span it; that needs at least four. With $\mu = 0$, at least 4 contacts are needed in the plane and 7 in space ([finger bounds for form closure](/finger-bounds-for-form-closure/)).

**Non-example: a part on locators.** A part that rests on the locators of a fixture, held there by gravity, resists only the loads that push it onto the locators. It is not in force closure until clamps squeeze it. [Fixture planning](/fixture-planning/) and [kinematic fixture analysis](/kinematic-fixture-analysis/) place the clamps.

## Related definitions

- [Form closure](/form-closure/): immobilization by geometry alone; first-order form closure is force closure with $\mu = 0$.
- [Force-closure test](/force-closure-test/): the linear program that decides force closure with linearized cones.
- [Antipodal grasp](/antipodal-grasp/): the two-finger condition for force closure in the plane.
- [Grasp wrench space](/grasp-wrench-space/): the set of wrenches that bounded contact forces can apply; the grasp is in force closure exactly when the origin is in its interior.
- [Ferrari-Canny metric](/ferrari-canny-metric/): how far the origin is from the boundary of that set, a measure of how much force closure the grasp has.
- [Grasp synthesis](/grasp-synthesis/): the search for contacts that give force closure.

## References
