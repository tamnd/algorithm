---
tag: EMM7B9
kind: concept
slug: grasp-quality-measures
name: Grasp quality measures
aliases:
- grasp metrics
area: robotics/grasping-and-manipulation
level: core
summary: "Numbers that rank grasps: singular values of the grasp matrix, the size of the grasp wrench space, the geometry of the contacts, or the posture of the hand."
prereqs: [grasp-matrix, grasp-wrench-space]
see_also: [ferrari-canny-metric, grasp-wrench-space, grasp-matrix, grasp-synthesis, yoshikawa-manipulability-measure, manipulability-ellipsoid, condition-number, singular-value-decomposition]
sources:
  - paper: doi:10.1007/s10514-014-9402-3
    title: "Máximo A. Roa and Raúl Suárez, Grasp quality measures: review and performance, Autonomous Robots 38(1), 65-88, 2015"
    locator: the classification of quality measures by what they depend on, and the comparison of their behavior
  - paper: "Zexiang Li and S. Shankar Sastry, Task-oriented optimal grasping by multifingered robot hands, IEEE Journal of Robotics and Automation 4(1), 32-44, 1988"
    locator: the measures from the singular values of the grasp matrix, the volume of its ellipsoid, and the task ellipsoid
  - paper: doi:10.1109/ROBOT.1992.219918
    title: "Carlo Ferrari and John Canny, Planning optimal grasps, Proceedings of the IEEE International Conference on Robotics and Automation, vol. 3, 2290-2295, 1992"
    locator: the largest ball in the wrench space as a measure, with the sum or the largest of the finger forces bounded
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4.1 (Form Closure), the value of the linear program test as a measure, its dependence on units and its lack of monotonicity; the chapter is pages 955 to 988"
---

A grasp quality measure is a number that says how good a grasp is, so that a planner can compare candidate grasps and pick the best. Yes or no properties such as [force closure](/force-closure/) do not rank grasps: thousands of candidates may all be closed. A measure adds a scale. There are many measures, because "good" has many meanings: resisting the worst disturbance, resisting a known load, needing little squeeze, or leaving the hand far from its joint limits.

## In plain words

When you pick up a cup, some ways of holding it feel safer than others. A grasp score tries to put that feeling into a number. Some scores ask how hard the fingers must push to hold against the worst bump from any direction. Some ask how evenly the grip resists pushes in different directions. Some look only at where the fingers touch, for example how far apart they are, or whether they surround the center of the object. Others look at the hand, for example whether the fingers are near the ends of their range. No single score is right for every job. Scores also depend on choices such as the unit of length, so they compare grasps fairly only when all grasps use the same choices.

## The idea

Roa and Suárez (2015) group the measures by what they depend on.

**Measures on the grasp matrix.** The [grasp matrix](/grasp-matrix/) $G$ maps contact forces to the object wrench. Its [singular values](/singular-value-decomposition/) $\sigma_1 \ge \cdots \ge \sigma_d$ describe how well the contacts transmit forces in different directions of the wrench space. Li and Sastry (1988) proposed three measures:

- the smallest singular value $\sigma_d$, which measures the weakest direction: if $\operatorname{rank} G = d$, every wrench of size at most $\sigma_d$ is $G\lambda$ for some contact force vector $\lambda$ of size at most 1;
- the volume of the image of the unit ball, proportional to $\sigma_1 \cdots \sigma_d = \sqrt{\det(G G^T)}$;
- a task-oriented measure, which compares the ellipsoid of $G$ with an ellipsoid of the wrenches that the task needs.

The ratio $\sigma_d / \sigma_1$, the inverse of the [condition number](/condition-number/), is a measure of isotropy. These measures are smooth functions of the contact positions, so gradient methods can improve a grasp. They ignore the friction cones: they treat the contact forces as free vectors.

**Measures on the grasp wrench space.** The [grasp wrench space](/grasp-wrench-space/) $W$ is the set of wrenches that the fingers can apply with bounded forces, respecting the friction cones. The [Ferrari-Canny metric](/ferrari-canny-metric/) $\varepsilon$ is the radius of the largest ball about the origin inside $W$. The volume of $W$ is another measure. A task-based measure scales $W$ until it contains the set of wrenches that the task will apply, and scores the grasp by that scale. These measures see the friction cones, and $\varepsilon > 0$ exactly when the grasp is in force closure. They are not smooth in the contact positions, and they are costly in six dimensions.

**Measures on the contact geometry.** In the plane, simple measures use the polygon of the contact points: its area, its smallest angle, and the distance from its centroid to the center of mass of the object. A large, regular polygon around the center of mass resists moments well. These measures are cheap and need no wrench model.

**Measures on the hand.** Some measures score the configuration of the hand rather than the contacts: the distance of each joint from its limits, or the manipulability of the hand in the sense of the [Yoshikawa measure](/yoshikawa-manipulability-measure/) and the [manipulability ellipsoid](/manipulability-ellipsoid/). A grasp with perfect contacts is useless if the hand cannot reach it or cannot apply the forces.

**What every measure must fix.** A wrench mixes forces (newtons) with moments (newton meters), so any norm on wrenches needs a length $\rho$ that converts moments into forces, and a reference point. The Handbook notes the dependence on units for the value of its linear program test of form closure, and the same holds for $\sigma_d$, for $\varepsilon$, and for the volumes. Grasps compare fairly only under the same choices. Combined scores, weighted sums of several measures, add more choices: the weights.

**Measured, not proved.** A measure is a model. That a grasp with a higher score holds better in practice is a claim about the world, tested by experiments; the measures differ in how well they predict success, and Roa and Suárez compare their behavior.

## Examples

**Singular values of a two-finger grasp.** Two hard fingers hold a planar box at $(\pm L, 0)$. The grasp matrix has $G G^T = \operatorname{diag}(2L^2, 2, 2)$, so its singular values are $\sqrt{2} L$, $\sqrt{2}$ and $\sqrt{2}$. For $L = 1$ the grasp is isotropic: $\sigma_d / \sigma_1 = 1$. For a box of half-width 0.1 m measured in meters, $\sigma_d = 0.1414$ and the isotropy index is 0.1; in centimeters, with $L = 10$, $\sigma_d = \sqrt{2}$ and the index is again 0.1, but now the weak direction is a force direction, not the moment. The physical grasp is the same in both cases.

**The Ferrari-Canny metric and friction.** The same grasp with $L = 1$ and $\mu = 0.25$, $0.5$ and $1$ has $\varepsilon_1 = 0.1741$, $0.3333$ and $0.5774$. The singular values of $G$ do not change with $\mu$, but the Ferrari-Canny metric does, because it sees the cones.

**Volume against the worst direction.** A grasp whose wrench space is long and thin has a large volume and a small inscribed ball. A volume measure prefers it; the Ferrari-Canny metric does not. The two measures can rank the same pair of grasps in opposite order.

**Monotonicity.** Adding a contact cannot decrease $\varepsilon$, because the wrench space grows. The Handbook shows that the value of its linear program test of form closure can decrease when a contact is added, so that value is a poor measure for comparing grasps with different numbers of contacts.

## Where it is used

- **Grasp planning.** A [grasp synthesis](/grasp-synthesis/) method generates candidate contacts and keeps the one with the best score. Analytic planners optimize a measure directly; sampling planners score many candidates.
- **Training data for learned grasping.** Learned grasp detectors are often trained on labels from an analytic score, such as the Ferrari-Canny metric computed over perturbed contacts.
- **Fixture design.** A fixture is a grasp by fixed locators and clamps, and fixture planners rank layouts by the same kinds of measures.
- **In-hand and cooperative manipulation.** Measures on the grasp matrix and the hand guide regrasping in [in-hand manipulation](/in-hand-manipulation/) and the load sharing in [cooperative manipulation](/cooperative-manipulation/).

## References
