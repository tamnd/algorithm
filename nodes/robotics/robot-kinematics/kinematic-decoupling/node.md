---
tag: H4E0Q4
kind: technique
slug: kinematic-decoupling
name: Kinematic decoupling
aliases:
- wrist partitioning
- inverse position and inverse orientation
area: robotics/robot-kinematics
level: core
summary: Solves the inverse kinematics of an arm with a spherical wrist in two parts, the wrist center position first and then the wrist angles.
prereqs: [inverse-kinematics, forward-kinematics, euler-angles]
see_also: [pieper-criterion, paden-kahan-subproblems, raghavan-roth-method, denavit-hartenberg-convention, kinematic-singularity, robot-workspace, newton-raphson-inverse-kinematics, six-r-inverse-kinematics-sixteen-solutions]
sources:
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Section 5.2, Kinematic Decoupling; Section 5.3, Inverse Position; Section 5.4, Inverse Orientation
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Section 3.7, inverse kinematics of arms with a spherical wrist
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 6, analytic inverse kinematics
  - book: "Donald L. Pieper, The kinematics of manipulators under computer control, Stanford Artificial Intelligence Project Memo AIM-72 (PhD thesis), Stanford University, 1968"
    locator: Sections 3.3.3 to 3.3.8, the closed-form solutions for arms with three intersecting axes
---

Kinematic decoupling splits the [inverse kinematics](/inverse-kinematics/) of a six-joint arm with a spherical wrist into two problems with three unknowns each.
The last three joint axes meet in one point, the wrist center, and those joints cannot move it.
So the target pose fixes the wrist center, the first three joints must put it there, and the last three joints then set the orientation.
Each part has a small number of closed-form solutions, and their products give all solutions of the arm.
[Pieper's criterion](/pieper-criterion/) proves that the split is valid, and most industrial arms are built so that it applies.

## In plain words

Your shoulder and elbow put your wrist somewhere in space.
Your wrist then turns your hand, but it does not move the wrist joint itself.
So to reach a cup with a given grip, first find where the wrist must be, which is a little behind the hand along the direction it points.
Move the shoulder and elbow to put the wrist there.
Then turn the wrist so that the hand points the right way.
Each step is a small puzzle with a few answers, and you never have to solve all six angles at once.

## When it applies

- The arm has six joints, and the axes of the last three joints meet in one point for every configuration: a spherical wrist.
- The first three joints can be any kind, but the method is useful when their position problem has a closed form.
For an elbow arm, an arm with a prismatic joint, or a general 3R arm (see the [Raghavan-Roth method](/raghavan-roth-method/)) it has one.
- The target is a full pose: a rotation $R$ and a position $p$ of the tool frame.
- The tool frame lies on the last axis at a known distance $d_6$ from the wrist center; any fixed tool offset can be removed first by a constant transform.

## The template

1. **Wrist center.**
The tool frame is $d_6$ along its own $z$ axis from the wrist center, so
$$p_c = p - d_6\,R\,e_z.$$
2. **Inverse position.**
Solve the position problem of the first three joints: find every $(\theta_1, \theta_2, \theta_3)$ with $o_c(\theta_1, \theta_2, \theta_3) = p_c$, where $o_c$ is the wrist center by [forward kinematics](/forward-kinematics/).
3. **Wrist rotation.**
For each solution, compute $R_3^0$ from the first three joints and the rotation that the wrist must make,
$$R_6^3 = (R_3^0)^T R.$$
4. **Inverse orientation.**
Solve $R_6^3 = R_4^3(\theta_4)\,R_5^4(\theta_5)\,R_6^5(\theta_6)$.
For the usual wrist this is a set of [ZYZ Euler angles](/euler-angles/), with two solutions when the middle angle is not 0 or $\pi$.
For other wrists use [Paden-Kahan](/paden-kahan-subproblems/) subproblems 2 and 1.
5. **Check and select.**
Check each joint vector by forward kinematics and against the joint limits, and pick the one closest to the current configuration.

## Classic examples

**An elbow arm with a spherical wrist.**
The Denavit-Hartenberg rows $(a_i, \alpha_i, d_i)$ are $(0, 90°, d_1)$, $(a_2, 0°, 0)$, $(0, 90°, 0)$, $(0, -90°, d_4)$, $(0, 90°, 0)$ and $(0, 0°, d_6)$.
Take $d_1 = 0.4$ m, $a_2 = 0.5$ m, $d_4 = 0.4$ m and $d_6 = 0.1$ m.
The target is the pose made by the joint vector $(0.6, 0.5, 0.3, 0.7, 0.9, -0.4)$ rad: $p = (0.698721, 0.416878, 0.360700)$ m, with the tool $z$ axis $R\,e_z = (0.997472, 0.070980, -0.003296)$.

1. The wrist center is $p_c = (0.598974, 0.409780, 0.361030)$ m.
2. Joint 1 points the arm plane at the wrist center: $\theta_1 = \operatorname{atan2}(y_c, x_c) = 0.6$ rad, or $0.6 + \pi$ with the arm reaching back.
In that plane the wrist center is at $r = \pm\sqrt{x_c^2 + y_c^2} = \pm 0.725734$ m and $s = z_c - d_1 = -0.038970$ m.
3. The upper arm $a_2$ and the forearm $d_4$ give $r^2 + s^2 = a_2^2 + d_4^2 + 2a_2d_4\sin\theta_3$, so $\sin\theta_3 = 0.295520$ and $\theta_3 = 0.3$ or $\pi - 0.3 = 2.841593$ rad, elbow up or down.
4. Then $\theta_2 = \operatorname{atan2}(s, r) - \operatorname{atan2}(-d_4\cos\theta_3,\ a_2 + d_4\sin\theta_3)$, which gives $0.5$ rad for $\theta_3 = 0.3$ and $-0.607291$ rad for $\theta_3 = 2.841593$.
5. For the wrist, $R_6^3 = R_z(\theta_4)R_y(\theta_5)R_z(\theta_6)$, so $\theta_5 = \operatorname{atan2}(\pm\sqrt{1 - r_{33}^2}, r_{33})$, $\theta_4 = \operatorname{atan2}(\pm r_{23}, \pm r_{13})$ and $\theta_6 = \operatorname{atan2}(\pm r_{32}, \mp r_{31})$.
For the first arm solution this gives $(0.7, 0.9, -0.4)$ and $(-2.441593, -0.9, 2.741593)$ rad.

| $\theta_1$ | $\theta_2$ | $\theta_3$ | $\theta_4$ | $\theta_5$ | $\theta_6$ |
|---|---|---|---|---|---|
| 0.600000 | 0.500000 | 0.300000 | 0.700000 | 0.900000 | -0.400000 |
| 0.600000 | 0.500000 | 0.300000 | -2.441593 | -0.900000 | 2.741593 |
| 0.600000 | -0.607291 | 2.841593 | 2.384747 | 0.825578 | -2.489615 |
| 0.600000 | -0.607291 | 2.841593 | -0.756846 | -0.825578 | 0.651978 |
| -2.541593 | -2.534301 | 0.300000 | -0.756846 | 0.825578 | -2.489615 |
| -2.541593 | -2.534301 | 0.300000 | 2.384747 | -0.825578 | 0.651978 |
| -2.541593 | 2.641593 | 2.841593 | -2.441593 | 0.900000 | -0.400000 |
| -2.541593 | 2.641593 | 2.841593 | 0.700000 | -0.900000 | 2.741593 |

All angles are in radians.
All 8 joint vectors reproduce the target pose to about $10^{-15}$: four arm solutions times two wrist solutions.

**A general 3R arm with a spherical wrist.**
If the first three joints have no special geometry, step 2 is the quartic of the [Raghavan-Roth method](/raghavan-roth-method/) page, with up to four arm solutions.
The [Pieper criterion](/pieper-criterion/) page shows an arm of this kind with 8 real solutions.

**Arms with a prismatic joint.**
In the Stanford arm the third joint is prismatic, and step 2 becomes even simpler: $\theta_1$ from the direction, $\theta_2$ from an angle, and $d_3$ from a distance.

## Variations

- **The first three axes meet.** If the spherical joint is at the base, apply the method to the inverse pose, which runs the chain from the hand to the base.
- **No spherical wrist.** Many collaborative arms have wrists whose axes do not meet.
The pose then does not fix a wrist center, and the arm needs other closed forms, such as sequences of [Paden-Kahan subproblems](/paden-kahan-subproblems/) with three parallel axes, or a numerical method such as [Newton-Raphson](/newton-raphson-inverse-kinematics/).
- **Seven joints.** For a redundant arm with a spherical wrist, fix one extra parameter, for example one joint angle or the angle of the elbow about the line from shoulder to wrist, and decouple the rest.
- **Position only.** If only the position of the hand matters, step 2 alone with $p_c = p$ is the whole problem.

## Pitfalls

- **Wrong offset.** The wrist center is $p - d_6 R e_z$ only if the tool lies on the last axis; a tool offset in $x$ or $y$ must be removed with the full transform first.
- **Lost branches.** Each $\operatorname{atan2}$ with a $\pm$ is a branch; dropping one loses solutions, and mixing them between steps gives wrong ones.
Check every result by forward kinematics.
- **Shoulder singularity.** If the wrist center lies on the axis of joint 1, $\theta_1$ is free and the formula $\operatorname{atan2}(y_c, x_c)$ is undefined.
- **Elbow singularity.** When $\sin\theta_3 = \pm 1$ the arm is fully stretched or folded, the two elbow solutions merge, and rounding can push $|\sin\theta_3|$ above 1; clamp it, or report that the target is out of reach.
- **Wrist singularity.** When $\theta_5 = 0$, axes 4 and 6 line up and only $\theta_4 + \theta_6$ is fixed; choose one of them, for example keep $\theta_4$ at its current value.
- **Angle wrap.** Joint limits often span more than $2\pi$; add or subtract $2\pi$ to choose the angle nearest the current one.

## Exercises

1. For the elbow arm above, show that the target $p = (0.5, 0, 0.4)$ m with the tool pointing along $+x$ has a wrist center at $(0.4, 0, 0.4)$ m, and find all solutions.
2. Show that for the usual wrist with $\alpha_4 = -90°$ and $\alpha_5 = 90°$, $R_x(-90°)R_z(\theta)R_x(90°) = R_y(\theta)$, so the wrist rotation is a ZYZ product.
3. Add a shoulder offset $d_2 \ne 0$ to the elbow arm, so that the arm plane passes at the distance $|d_2|$ from axis 1, and show that $\theta_1 = \operatorname{atan2}(y_c, x_c) - \operatorname{atan2}(d_2, \pm\sqrt{x_c^2 + y_c^2 - d_2^2})$ for one choice of the sign of $d_2$.
4. Explain why kinematic decoupling cannot be used when axes 4 and 5 meet but axis 6 does not pass through their meeting point.

## References
