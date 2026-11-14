---
tag: P217W3
kind: concept
slug: three-two-one-locating-principle
name: 3-2-1 locating principle
aliases:
- 3-2-1 principle
- six-point locating
area: cad/manufacturing-process-planning
level: intro
summary: Locates a prismatic part by three points on a primary datum face, two on a secondary and one on a tertiary, which removes all six degrees of freedom.
prereqs: [rigid-body-twist, rank]
see_also: [kinematic-fixture-analysis, fixture-planning, modular-fixture-design, form-closure, wrench, setup-planning, tolerance-stack-up, degrees-of-freedom-analysis]
sources:
  - paper: doi:10.1109/JRA.1985.1087007
    title: Haruhiko Asada and Andre B. By, Kinematic analysis of workpart fixturing for flexible assembly with automatically reconfigurable fixtures, IEEE Journal of Robotics and Automation 1(2), 1985, 86 to 94
    locator: the locator Jacobian of frictionless point contacts, deterministic positioning as full rank of the Jacobian, and the accessibility and detachability conditions
  - book: isbn:978-1-4018-1107-5
    title: Edward G. Hoffman, Jig and Fixture Design, fifth edition, Delmar Learning, 2004
    locator: the chapter on locating principles, the three-two-one (six-point) method and the twelve directions of movement
---

The 3-2-1 locating principle places a prismatic part in a fixture with six fixed point locators: three touch a primary datum face, two touch a secondary face and one touches a tertiary face. If the three primary points are not on one line and the two secondary points are not one above the other, the six contacts fix the part to first order, so its position is repeatable from part to part. The principle locates the part. It does not hold it: six frictionless contacts can never stop every motion, and a clamp must push the part onto the locators. This page proves both facts with the locator Jacobian of Asada and By (1985) and works one box with numbers.

## In plain words

A box resting on a table can still slide and turn. Put three pins under it, two pins against one side and one pin against the end, and push the box onto all six pins. Now there is only one place where the box can be, so every box in a batch ends up in the same place, and the machine cuts each one in the same spot. The three bottom pins stop it from dropping and tipping. The two side pins stop it from sliding sideways and turning flat on the table. The end pin stops the last slide. The pins only push, they cannot pull. So the box can always be lifted off, and a clamp must press it onto the pins. The pins must also be spread out. Pins that are close together let a small error in one pin turn the whole part.

## The idea

**Model.** The part is rigid. Each locator $i$ is a frictionless point contact at a point $p_i$ on the part surface, with unit normal $n_i$ that points from the locator into the part. A small motion of the part is a [twist](/rigid-body-twist/) $\xi = (\delta, \omega)$: a body point $p$ moves to $p + \delta + \omega \times p$, to first order. The gap at contact $i$ then changes by
$$ n_i \cdot (\delta + \omega \times p_i) = n_i \cdot \delta + (p_i \times n_i) \cdot \omega = J_i \, \xi, \qquad J_i = \big[\, n_i^{\mathsf T} \;\; (p_i \times n_i)^{\mathsf T} \,\big]. $$
The rows $J_i$ form the locator Jacobian $J$. Row $i$ is also the [wrench](/wrench/) that a unit push of locator $i$ applies to the part. A locator cannot pull, so a motion is allowed when $J\xi \ge 0$ (no gap closes into the locator), and the part is held in place to first order when $J\xi = 0$ forces $\xi = 0$. By rank and nullity this is $\operatorname{rank} J = 6$ (Asada and By 1985). The [kinematic fixture analysis](/kinematic-fixture-analysis/) page treats the general test. This page applies it to the 3-2-1 layout.

**The layout.** Take the corner of the part as the origin and the three datum faces as the planes $z = 0$ (primary), $y = 0$ (secondary) and $x = 0$ (tertiary), with the part in $x, y, z \ge 0$. The locators are:

| locator | point | normal | row of $J$, columns $(\delta_x, \delta_y, \delta_z, \omega_x, \omega_y, \omega_z)$ |
| --- | --- | --- | --- |
| primary $i = 1, 2, 3$ | $(x_i, y_i, 0)$ | $(0, 0, 1)$ | $(0, 0, 1, \; y_i, \; -x_i, \; 0)$ |
| secondary $j = 1, 2$ | $(a_j, 0, z_j)$ | $(0, 1, 0)$ | $(0, 1, 0, \; -z_j, \; 0, \; a_j)$ |
| tertiary | $(0, b, c)$ | $(1, 0, 0)$ | $(1, 0, 0, \; 0, \; c, \; -b)$ |

**Claim.** $\operatorname{rank} J = 6$ if and only if the primary points $(x_i, y_i)$ are not collinear and $a_1 \ne a_2$. Then $|\det J| = 2 A \, |a_2 - a_1|$, where $A$ is the area of the primary triangle.

*Proof.* Suppose $J\xi = 0$. The primary rows say that the affine function $f(x, y) = \delta_z + y\,\omega_x - x\,\omega_y$ is zero at the three primary points. An affine function of the plane that vanishes at three non-collinear points is zero, so $\delta_z = \omega_x = \omega_y = 0$. The secondary rows then read $\delta_y + a_j \omega_z = 0$ for $j = 1, 2$. Subtracting gives $(a_2 - a_1)\,\omega_z = 0$, so $\omega_z = 0$ and $\delta_y = 0$. The tertiary row then reads $\delta_x = 0$. So $\xi = 0$ and the rank is 6. For the converse and the determinant, order the columns as $(\delta_z, \omega_x, \omega_y \mid \delta_y, \omega_z \mid \delta_x)$. The primary rows have zeros outside the first block, and the secondary rows have zeros in the last block, so $J$ is block triangular and $\det J$ is, up to sign, the product of the three diagonal blocks: the $3 \times 3$ determinant of the rows $(1, y_i, -x_i)$, which is $\pm 2A$; the $2 \times 2$ determinant of the rows $(1, a_j)$, which is $a_2 - a_1$; and $1$. If the primary points are collinear ($A = 0$) or $a_1 = a_2$, the determinant is 0 and the rank is less than 6. $\square$

**Why six and not fewer.** $\operatorname{rank} J$ is at most the number of rows. With five locators, some nonzero twist has $J\xi = 0$, and the part can move without opening or closing any contact. With six locators in the layout above, each one is needed: removing a row leaves rank 5. So 3-2-1 removes exactly the six degrees of freedom of a rigid body, one per locator. Shop texts count twelve directions of movement (both senses along and about each axis) and say that the six locators block nine of them and the clamps block the other three (Hoffman). The count of twelve is the one-sided form of the same fact: a locator stops motion toward it, not away from it.

**Locating is not holding.** If $J$ is invertible, take any vector $e$ with all entries positive and let $\xi = J^{-1} e$. Then $J\xi = e > 0$: the twist opens all six gaps at once, so the part lifts off every locator. So no six frictionless contacts can immobilize a part, whatever their layout. In the language of grasping, the six locators never give [form closure](/form-closure/), and at least one more contact is needed (the [fixture planning](/fixture-planning/) page proves the lower bound of seven). The extra contacts are the clamps. In the frictionless model a single clamp on a face of a box is not enough. With seven contacts and $J$ invertible, the wrench $w_7$ of the clamp must satisfy $w_7 = -\sum_{i=1}^{6} \lambda_i J_i$ with all $\lambda_i > 0$, so its force part is $-(\lambda_6, \lambda_4 + \lambda_5, \lambda_1 + \lambda_2 + \lambda_3)$, which has three nonzero components. A contact inside a face of a box has a normal along one axis, so it cannot supply this force. Real fixtures use one clamp per datum, or one clamp and friction ([force closure](/force-closure/)).

**Error amplification.** If the second secondary locator is too high by $\Delta$ (it stands out of the plane $y = 0$ by $\Delta$), the part rests at the twist with $\delta_y + a_1 \omega_z = 0$ and $\delta_y + a_2 \omega_z = \Delta$, so it turns by $\omega_z = \Delta / (a_2 - a_1)$. The same holds for the primary triangle: the tilt caused by a height error is inversely proportional to the spacing of the points. This is why the rule of thumb puts the locators as far apart as the datum face allows, and why $|\det J|$ is a measure of the quality of a layout.

## Examples

**A box, worked.** A block of $100 \times 60 \times 40$ mm with locators at:

| locator | point (mm) | row of $J$ |
| --- | --- | --- |
| 1 primary | $(20, 10, 0)$ | $(0, 0, 1, 10, -20, 0)$ |
| 2 primary | $(80, 10, 0)$ | $(0, 0, 1, 10, -80, 0)$ |
| 3 primary | $(50, 50, 0)$ | $(0, 0, 1, 50, -50, 0)$ |
| 4 secondary | $(20, 0, 20)$ | $(0, 1, 0, -20, 0, 20)$ |
| 5 secondary | $(80, 0, 20)$ | $(0, 1, 0, -20, 0, 80)$ |
| 6 tertiary | $(0, 30, 20)$ | $(1, 0, 0, 0, 20, -30)$ |

The primary triangle has area $A = \tfrac12 \cdot 60 \cdot 40 = 1200$ mm$^2$ and $a_2 - a_1 = 60$ mm, so $|\det J| = 2 \cdot 1200 \cdot 60 = 144000$, and Gaussian elimination in exact rational arithmetic gives the same value and rank 6. The twist $J^{-1}(1, 1, 1, 1, 1, 1)^{\mathsf T}$ is $(1, 1, 1, 0, 0, 0)$, a translation away from the corner, which opens all six gaps. A secondary locator that stands out by $\Delta = 0.01$ mm turns the part by $0.01 / 60 \approx 1.7 \times 10^{-4}$ rad.

**Clamps for the box.** Add three frictionless clamps at the centers of the three opposite faces: $(100, 30, 20)$ pushing in $-x$, $(50, 60, 20)$ pushing in $-y$ and $(50, 30, 40)$ pushing in $-z$. The nine wrenches then positively span $\mathbb{R}^6$ (each of $\pm e_1, \dots, \pm e_6$ is a nonnegative combination of six of them, checked with exact arithmetic over all 84 choices of six), so the fixture has form closure. The six locators with only the top clamp do not, as the argument above predicts.

**Collinear primary points.** Move locator 3 to $(50, 10, 0)$. Now the three primary points lie on the line $y = 10$ and the rank drops to 5. The null twist is $\xi = (0, 20, -10, 1, 0, 0)$: a rotation about the line $y = 10$, $z = 20$ parallel to the $x$ axis. Each contact point moves along its face, so no gap changes to first order and the part can rock about this line.

**Stacked secondary points.** Move locator 5 to $(20, 0, 30)$, straight above locator 4. Then $a_1 = a_2$ and the rank is 5. The null twist is $\xi = (30, -20, 0, 0, 0, 1)$, a rotation about the vertical line through $(20, 30)$. This line meets the line $x = 20$ of the two secondary points and the line $y = 30$ along which the tertiary locator pushes, so all three side contacts slide along their faces and no gap changes to first order.

## Where it is used

- [Fixture planning](/fixture-planning/) uses 3-2-1 as the default layout for prismatic parts, then adds clamps and checks stability under the cutting forces.
- [Kinematic fixture analysis](/kinematic-fixture-analysis/) is the general rank test, for any surfaces and any number of locators. The claim above is its special case for three orthogonal planes.
- [Modular fixture design](/modular-fixture-design/) is the planar version of the same idea with locators on a lattice: three locators and a clamp give four contacts, the minimum for form closure in the plane.
- [Setup planning](/setup-planning/) chooses the datum faces of each setup, and the three datum faces of the 3-2-1 layout are the reference for the dimensions cut in that setup.
- [Tolerance stack-up](/tolerance-stack-up/) needs the datum reference frame that the three faces define, and error amplification above is the first-order sensitivity to locator errors.
