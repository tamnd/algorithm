---
tag: 32ZCJ0
kind: problem
slug: fixture-planning
name: Fixture planning
aliases:
- fixture design
- fixture layout design
area: cad/manufacturing-process-planning
level: core
summary: Choose locators and clamps that hold a part in a known position, determinate and stable under cutting forces, without blocking the operations.
prereqs: [three-two-one-locating-principle, kinematic-fixture-analysis, form-closure]
see_also: [modular-fixture-design, setup-planning, force-closure, wrench, accessibility-cone, computer-aided-process-planning, linear-programming-problem, caratheodory-theorem]
sources:
  - paper: doi:10.1109/JRA.1985.1087007
    title: Haruhiko Asada and Andre B. By, Kinematic analysis of workpart fixturing for flexible assembly with automatically reconfigurable fixtures, IEEE Journal of Robotics and Automation 1(2), 1985, 86 to 94
    locator: deterministic positioning as rank 6 of the locator Jacobian, and the accessibility and detachability conditions
  - paper: doi:10.1177/027836499000900102
    title: Xanthippi Markenscoff, Luqun Ni and Christos H. Papadimitriou, The geometry of grasping, International Journal of Robotics Research 9(1), 1990, 61 to 74
    locator: four frictionless contacts suffice to immobilize a planar part and seven a part in space, except for parts with rotational symmetry such as a disk or a body of revolution
  - paper: doi:10.1109/70.481749
    title: Randy C. Brost and Kenneth Y. Goldberg, A complete algorithm for designing planar fixtures using modular components, IEEE Transactions on Robotics and Automation 12(1), 1996, 31 to 46
    locator: the planar fixture with three locators and a clamp on a lattice, and the complete enumeration of all such fixtures
  - paper: doi:10.1177/027836499601500608
    title: Yan Zhuang and Ken Goldberg, On the existence of solutions in modular fixturing, International Journal of Robotics Research 15(6), 1996, 646 to 656
    locator: convex polygons of any width that admit no fixture with three locators and a clamp, and the fixture with four clamps as an alternative
  - paper: doi:10.1109/70.720346
    title: Elon Rimon and Joel W. Burdick, Mobility of bodies in contact, part I, a 2nd-order mobility index for multiple-finger grasps, IEEE Transactions on Robotics and Automation 14(5), 1998, 696 to 708
    locator: second-order (curvature) immobilization, with fewer contacts than the first-order count
  - paper: doi:10.1115/1.2831031
    title: Wayne Cai, S. Jack Hu and Jingxia Yuan, Deformable sheet metal fixturing, principles, algorithms, and simulations, Journal of Manufacturing Science and Engineering 118(3), 1996, 318 to 324
    locator: the N-2-1 locating principle for compliant sheet metal parts and the choice of the N primary locators that minimizes deformation
---

Fixture planning chooses the locators and clamps that hold a part during machining, inspection, welding or assembly. The fixture must put the part in one known position, keep it there under the cutting forces, let the tools reach the features of the setup, and let the part be loaded and unloaded. It differs from [setup planning](/setup-planning/) in scope: setup planning decides which features are made in which orientation of the part, and fixture planning decides how the part is held in one of those setups. This page states the problem, proves the minimum number of contacts that can hold a part without friction, and lists what is known about solving it.

## In plain words

A part on a milling machine must not move. A fixture does this with two kinds of elements. Locators are fixed stops that the part rests against, so each part sits in the same place. Clamps press the part onto the locators. A good fixture puts the part in exactly one place, holds it firmly when the cutter pushes on it, stays out of the way of the cutter, and lets a worker or a robot put the part in and take it out. A rule of thumb for boxes is three stops under the part, two on one side and one at the end, and then clamps. Without friction, a part in the plane needs at least four contacts to be held, and a part in space needs at least seven. There is no single standard formal version of the task.

## Definition

There is no standard formal statement of fixture planning. The following version uses the rigid body, point contact model of [kinematic fixture analysis](/kinematic-fixture-analysis/), which most of the cited work uses.

**Input.**
- A rigid part $P$ with its boundary surface, and a set $S \subseteq \partial P$ of surface patches where elements may touch it (datum faces, faces not to be machined).
- The operations of the setup, with the volumes $V_1, \dots, V_q$ that the tools and holders sweep, and a set $\mathcal{W}$ of external wrenches: the cutting forces and moments, and gravity.
- A library of elements: locators that are fixed, clamps that apply a force of at most $F_{\max}$ along their normal, and optional friction with coefficient $\mu$ at each contact.

**Design variables.** A set of locator contacts $(p_i, n_i)$, $i = 1, \dots, \ell$, and clamp contacts $(p_j, n_j)$, $j = \ell + 1, \dots, m$, with $p_i \in S$ and $n_i$ the inner normal of $P$ at $p_i$. Let $w_i = (n_i, p_i \times n_i) \in \mathbb{R}^6$ be the [wrench](/wrench/) of a unit push at contact $i$, and $J$ the matrix of the locator rows.

**Constraints.**
1. *Determinism.* $\operatorname{rank} J = 6$, so the locators fix the position to first order (Asada and By 1985).
2. *Restraint.* For each $w \in \mathcal{W}$ there are contact forces $f_i \ge 0$, with $f_j \le F_{\max}$ for the clamps, such that $\sum_i f_i w_i + w = 0$ (frictionless), or the same with each $f_i$ in its friction cone ([force closure](/force-closure/)).
3. *Access.* The elements do not meet the swept volumes $V_1, \dots, V_q$ or each other.
4. *Loading.* There is a motion that brings the part onto the locators and takes it off without collision, for example a detaching twist with all clamps open.

**Objective.** One of: the fewest elements; the smallest error amplification $\|J^{-1}\|$ of locator errors into part position; the smallest clamp forces needed for the worst $w \in \mathcal{W}$; or the smallest deformation of the part. Real planners combine several.

**The planar version.** The part is a polygon, twists and wrenches have three entries $(x, y, \text{moment})$, and the rank condition is $\operatorname{rank} J = 3$. The modular version restricts the contacts to locators and clamps at the holes of a lattice plate.

## Variants

- **Form closure.** No friction and no bound on the clamp forces: the contact wrenches must positively span $\mathbb{R}^6$ (or $\mathbb{R}^3$ in the plane), so they resist every external wrench. This is [form closure](/form-closure/), a property of the geometry alone.
- **Force closure.** With friction, each contact can push inside a cone, and fewer contacts can resist all wrenches. Machining fixtures often rely on friction under the clamps.
- **Modular fixtures.** Elements sit at the holes of a lattice plate. [Modular fixture design](/modular-fixture-design/) enumerates all planar fixtures with three locators and a clamp, and decides if one exists.
- **Dedicated fixtures and the 3-2-1 layout.** For a prismatic part, the [3-2-1 locating principle](/three-two-one-locating-principle/) fixes the six locators, and the planner adds clamps opposite the datum faces.
- **Compliant parts.** A thin sheet sags between locators, so the rigid body model fails. The N-2-1 principle uses $N > 3$ locators on the primary datum and chooses them to minimize deformation, computed by finite elements (Cai, Hu and Yuan 1996).
- **Feasibility only.** Decide if any fixture exists in a given library. For modular fixtures with three locators and a clamp, some polygons have none (Zhuang and Goldberg 1996).

## Examples

**A pinwheel in the plane.** A square $[0, 2]^2$ with four frictionless contacts: $(0, \tfrac32)$ pushing in $+x$, $(2, \tfrac12)$ pushing in $-x$, $(\tfrac32, 0)$ pushing in $+y$ and $(\tfrac12, 2)$ pushing in $-y$. The planar wrench of a contact is $(n_x, n_y, p_x n_y - p_y n_x)$, so the rows are
$$ (1, 0, -\tfrac32), \quad (-1, 0, \tfrac12), \quad (0, 1, \tfrac32), \quad (0, -1, -\tfrac12). $$
They have rank 3, and their sum is $0$: the combination with all weights 1 is strictly positive. By the lemma below, the four wrenches positively span $\mathbb{R}^3$, so the square has form closure with four contacts, the minimum.

**The symmetric layout fails.** Move each contact to the middle of its side: $(0, 1)$, $(2, 1)$, $(1, 0)$, $(1, 2)$. The rows are $(1, 0, -1)$, $(-1, 0, 1)$, $(0, 1, 1)$, $(0, -1, -1)$, with rank 2. The twist $(\delta_x, \delta_y, \omega) = (1, -1, 1)$, a turn about the center $(1, 1)$, changes no gap, since each contact moves along its side. The square can turn.

**A box in space.** For the $100 \times 60 \times 40$ mm block of the [3-2-1 page](/three-two-one-locating-principle/), the six locators have rank 6, the six locators and one clamp on the top face do not have form closure, and the six locators with one clamp at the center of each opposite face do. These are computed in exact arithmetic on that page.

## Known algorithms

- [Kinematic fixture analysis](/kinematic-fixture-analysis/) tests a given layout: rank 6 for determinism, a sign test for loading and form closure. It is a test, not a design method, and planners call it inside a search over candidate layouts.
- [Modular fixture design](/modular-fixture-design/), the algorithm of Brost and Goldberg (1996), is complete for its model: a polygon, three locators and a translating clamp on a lattice, frictionless point contacts. It returns every fixture of the model, ranked by a quality measure.
- The [3-2-1 locating principle](/three-two-one-locating-principle/) is a layout rule for prismatic parts. It gives determinism, not restraint.
- Restraint for a fixed layout and a finite set $\mathcal{W}$ is a [linear program](/linear-programming-problem/) in the contact forces, one per wrench.
- General 3D fixture design with access and deformation is solved by heuristic search over candidate contact points, by rule-based systems and by optimization with finite element models. These methods carry no optimality guarantee. There are no standard benchmarks for fixture planning, so published results are case studies.

## Bounds

**Lemma (positive span).** Vectors $w_1, \dots, w_m$ positively span $\mathbb{R}^d$ (every vector is a nonnegative combination of them) if and only if they span $\mathbb{R}^d$ and $\sum_i \lambda_i w_i = 0$ for some $\lambda$ with all $\lambda_i > 0$. *Proof.* If they positively span, they span. Also $-\sum_i w_i = \sum_i \mu_i w_i$ for some $\mu \ge 0$, so $\sum_i (1 + \mu_i) w_i = 0$ with all weights at least 1. Conversely, take any $x = \sum_i c_i w_i$, with coefficients of any sign. For $t$ large enough, $x = \sum_i (c_i + t \lambda_i) w_i$ has all weights nonnegative. $\square$

**Theorem (lower bound on contacts).** Frictionless point contacts that give form closure number at least $d + 1$: at least 4 for a part in the plane ($d = 3$) and at least 7 in space ($d = 6$). *Proof.* Suppose $m \le d$ wrenches positively span $\mathbb{R}^d$. They span $\mathbb{R}^d$, so $m = d$ and they form a basis. Then $-w_1 = \sum_i c_i w_i$ with $c \ge 0$. In the basis, the coordinates of $-w_1$ are $(-1, 0, \dots, 0)$, and they are unique, so $c_1 = -1 < 0$, a contradiction. $\square$

The same argument shows that six locators alone never hold a part, whatever the layout: their wrenches are at most six. The bound is tight for almost all parts. Markenscoff, Ni and Papadimitriou (1990) prove that four frictionless contacts suffice in the plane and seven in space for every part except those with rotational symmetry, where no number of frictionless contacts on the curved surface stops the turn about the axis. The counting bound itself is older: Reuleaux defined form closure in the 19th century, and the seven-contact bound in space is attributed to Somoff (1900) and Lakshminarayana (1978) in the grasping literature. These are first-order results. With the curvature of the part and the contacts taken into account, fewer contacts can immobilize a part: Rimon and Burdick (1998) define a second-order mobility index for this case, and their theory allows four suitably curved contacts to immobilize a generic part in space.

**Existence.** For modular fixtures with three locators and a clamp, Zhuang and Goldberg (1996) give convex polygons with no such fixture, so the feasibility version can have the answer "no" for reasons of the lattice alone.

**Hardness.** No hardness result for the general fixture planning problem is known in the cited sources. The difficulty in practice is the size of the design space, the access constraints and the deformation model, not a proved lower bound.

## Reductions

- **Form closure to a linear program.** By the lemma, a layout has form closure if and only if $\operatorname{rank} W = d$ and the system $W^{\mathsf T} \lambda = 0$, $\lambda_i \ge 1$ is feasible, where $W$ has the contact wrenches as rows. The second condition is a linear feasibility problem, solvable in polynomial time. In the plane with four contacts, $\lambda$ is unique up to scale and is given by the signed $3 \times 3$ minors, so the test is four determinants.
- **Restraint to a linear program.** For a finite set $\mathcal{W}$, the clamp forces that resist all of $\mathcal{W}$ with the smallest maximum force are one linear program with variables $f_i^{(w)}$ for each $w \in \mathcal{W}$.
## Applications

- Machining: every setup of a [process plan](/computer-aided-process-planning/) needs a fixture, and the datum faces of the fixture are the reference for the dimensions cut in that setup.
- Inspection: a coordinate measuring machine measures a part in a fixture, and locator errors enter the measurement as the twist $J^{-1}\varepsilon$.
- Welding and assembly of sheet metal: N-2-1 fixtures hold compliant panels so that the joined parts keep their shape.
- Robot grasping solves the same problem with fingers instead of locators and clamps, and uses the same closure tests.
