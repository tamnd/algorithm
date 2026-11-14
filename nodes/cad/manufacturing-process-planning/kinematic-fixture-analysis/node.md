---
tag: E79S9A
kind: technique
slug: kinematic-fixture-analysis
name: Kinematic fixture analysis
aliases:
- Asada-By fixture analysis
area: cad/manufacturing-process-planning
level: advanced
summary: Asada and By's test that point locators fix a part deterministically, by the rank of a matrix of locator normals and positions, and allow loading and unloading.
prereqs: [three-two-one-locating-principle, rigid-body-twist, rank]
see_also: [fixture-planning, modular-fixture-design, form-closure, force-closure, wrench, infinitesimal-rigidity, farkas-lemma, grasp-wrench-space]
sources:
  - paper: doi:10.1109/JRA.1985.1087007
    title: Haruhiko Asada and Andre B. By, Kinematic analysis of workpart fixturing for flexible assembly with automatically reconfigurable fixtures, IEEE Journal of Robotics and Automation 1(2), 1985, 86 to 94
    locator: the locator Jacobian of frictionless point contacts, deterministic positioning as rank 6, and the accessibility and detachability conditions for loading and unloading
  - book: isbn:978-0-471-98232-6
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986 (paperback 1998)
    locator: Chapter 7 (Farkas' lemma and its variants) and Chapter 8 (the structure of polyhedra, faces and extreme rays of cones)
  - paper: doi:10.1177/027836499000900102
    title: Xanthippi Markenscoff, Luqun Ni and Christos H. Papadimitriou, The geometry of grasping, International Journal of Robotics Research 9(1), 1990, 61 to 74
    locator: frictionless form closure needs and, for almost all parts, can be had with 4 contacts in the plane and 7 in space
---

Kinematic fixture analysis decides from the locator layout alone whether a fixture positions a part in one well-defined place. Asada and By (1985) wrote the first-order gap change at each frictionless point locator as a row of a matrix, the locator Jacobian, and showed that the part is positioned deterministically if and only if this matrix has rank 6. The same matrix answers a second question with a sign test instead of a rank test: can the part be loaded and unloaded, that is, is there a small motion that moves it away from the locators without pushing into any of them? This page gives the template, proves both tests, and shows an exact implementation in rational arithmetic.

## In plain words

Each locator is a pin that touches the part at one point. If you move the part a tiny bit, each pin sees a small gap open or close. Write down, for each pin, how its gap changes for each of the six ways the part can move: three slides and three turns. That gives a table with one row per pin and six columns. If some motion leaves every gap unchanged, the part can drift along that motion and its position is not fixed. This happens exactly when the rows do not fill all six directions, which is a rank test. A second question is whether the part can be put in and taken out. That needs a motion that opens some gaps and closes none. Pins can only push, so this is a test about signs, not about rank.

## When it applies

- The part is rigid and the locators are point contacts with no friction. Friction and part deformation are outside the model.
- Motions are small. The test is first order: it uses the tangent plane at each contact, not the curvature of the part or of the locator. A rank 6 result is a sufficient condition for a fixed position. A rank deficient result means the part is free to first order, and a second-order analysis can still find that curvature holds it.
- The question is about the layout, before forces: is the position unique, which locators are needed, can the part be loaded. Holding the part against cutting forces is a later step of [fixture planning](/fixture-planning/).

## The template

A contact is a point $p_i$ on the part surface and a normal $n_i$ from the locator into the part. A small motion is a [twist](/rigid-body-twist/) $\xi = (\delta, \omega) \in \mathbb{R}^6$ that moves a body point $p$ to $p + \delta + \omega \times p$. The gap at contact $i$ changes by $n_i \cdot \delta + (p_i \times n_i) \cdot \omega$, so the row $J_i = [\, n_i^{\mathsf T} \;\; (p_i \times n_i)^{\mathsf T} \,]$ is the gradient of gap $i$. It is also the [wrench](/wrench/) of a unit push of locator $i$ on the part.

```pseudo id=main
KINEMATIC-FIXTURE-ANALYSIS((p_1, n_1), …, (p_m, n_m))
L1  for i ← 1 to m do J_i ← (n_i, p_i × n_i)                ▷ hole: the contact model
L2  r ← rank of J, by elimination in exact arithmetic
L3  if r < 6 then report NOT DETERMINISTIC and a basis of {ξ : Jξ = 0}
L4  for each set T of r − 1 linearly independent rows of J do   ▷ hole: the cone test
L5      choose ξ with J_T ξ = 0 and Jξ ≠ 0
L6      if Jξ ≥ 0 then return DETACHABLE along ξ
L7      if Jξ ≤ 0 then return DETACHABLE along −ξ
L8  return NOT DETACHABLE                                    ▷ with r = 6 this is form closure
```

Line L1 has a hole for the contact model: a point on a plane, a point on a sphere and a point in a hole all give one row each, with the normal at the contact. A cylindrical pin in a hole is often modeled as two rows, one per direction across the axis. Lines L4 to L7 have a hole for the cone test: the exact enumeration shown here, or a [linear program](/linear-programming-problem/).

**Theorem 1 (determinism, Asada and By).** No nonzero twist leaves every gap unchanged to first order if and only if $\operatorname{rank} J = 6$. *Proof.* The twists that leave every gap unchanged to first order are the solutions of $J\xi = 0$. By rank and nullity, this space has dimension $6 - \operatorname{rank} J$, so it is $\{0\}$ exactly when the rank is 6. $\square$ When the rank is less than 6, line L3 returns the null twists: each is a motion along which every contact slides on its face.

**Detachability.** A twist $\xi$ is *detaching* if $J\xi \ge 0$ and $J\xi \ne 0$: no gap closes and at least one opens. Asada and By call the conditions for loading and unloading accessibility and detachability. With rank 6 and no detaching twist, every motion closes some gap, so the contacts alone stop all small motions: this is first-order [form closure](/form-closure/).

**Theorem 2 (the cone test is exact).** A detaching twist exists if and only if lines L4 to L7 find one. *Proof.* The "if" part holds because L6 and L7 return a twist that they have checked. For "only if", let $r = \operatorname{rank} J$, let $V$ be the row space of $J$, and let $D = \{\xi \in V : J\xi \ge 0\}$. A twist and its projection on $V$ give the same $J\xi$, because the difference lies in $V^\perp$, the null space of $J$. So if a detaching twist exists, $D$ contains a nonzero vector. $D$ is a polyhedral cone, and it is pointed: if $\xi$ and $-\xi$ are both in $D$, then $J\xi = 0$, so $\xi \in V \cap V^\perp = \{0\}$. A nonzero pointed polyhedral cone in the $r$-dimensional space $V$ has an extreme ray, and on an extreme ray $r - 1$ linearly independent constraints $J_i \xi \ge 0$ hold with equality (Schrijver, Chapter 8). Let $T$ be these rows and $\xi^\ast$ a twist on the ray. The solutions of $J_T \xi = 0$ form the null space of $J$ plus one more dimension, so the vectors $J\xi$ for these solutions form a single line through 0. The twist $\xi$ of L5 and $\xi^\ast$ give two nonzero points of this line, so $J\xi$ is a nonzero multiple of $J\xi^\ast \ge 0$, and L6 or L7 returns. $\square$

A second view of the same test is Stiemke's theorem, a variant of the [Farkas lemma](/farkas-lemma/): there is no detaching twist if and only if some $\lambda$ with all entries strictly positive has $J^{\mathsf T} \lambda = 0$. The easy half takes one line: if such a $\lambda$ exists and $J\xi \ge 0$, then $0 = \lambda^{\mathsf T} J \xi$ is a sum of nonnegative terms with positive weights, so $J\xi = 0$. The other half is in Schrijver, Chapter 7. In the language of wrenches, the locator wrenches positively span their own span. With rank 6 they positively span $\mathbb{R}^6$, which is the usual statement of form closure.

**Six locators never hold.** If $m = 6$ and $\operatorname{rank} J = 6$, then $\xi = J^{-1}(1, \dots, 1)^{\mathsf T}$ is detaching. So a deterministic fixture with six locators can always be loaded and unloaded, and it never has form closure. At least seven contacts are needed in space and four in the plane, with equality for almost all parts (Markenscoff, Ni and Papadimitriou 1990). The [fixture planning](/fixture-planning/) page proves the lower bound.

**Locator errors.** For six locators with rank 6, if locator $i$ is off by a small $\varepsilon_i$ along its normal, the part comes to rest at the twist $\xi = J^{-1} \varepsilon$. The norm of $J^{-1}$ measures how much the layout amplifies locator errors, and a well-spread layout keeps it small.

**Cost.** Line L1 takes $O(m)$ time and L2 takes $O(m)$ row operations on rows of length 6, so the rank test is linear in the number of contacts. The exact cone test of L4 to L7 tries up to $\binom{m}{r-1}$ sets, which is fine for the 6 to 12 contacts of a real fixture. A linear program decides the same question in polynomial time for large $m$.

**Implementation.** The code works in `Fraction` arithmetic, so a rank or a sign is never wrong because of rounding. The tests compare the rank with the largest nonzero minor found by Laplace expansion. They move the part by exact finite rigid motions, with rational rotations from the Cayley transform, and check that each gap changes by $t J_i \xi$ up to $O(t^2)$, that each reported null twist changes no gap to first order, and that no twist in $\{-1, 0, 1\}^6$ is a null twist when the rank is 6. They compare the cone test with a brute-force positive span test over all bases of rows, by Carathéodory's theorem.

## Classic examples

- **The [3-2-1 locating principle](/three-two-one-locating-principle/).** Three locators on the plane $z = 0$, two on $y = 0$ and one on $x = 0$. The rank is 6 if and only if the first three are not collinear and the next two are not one above the other, and $|\det J| = 2A\,|a_2 - a_1|$. For the block on that page, $J^{-1}(1, \dots, 1)^{\mathsf T} = (1, 1, 1, 0, 0, 0)$, a translation away from the corner that unloads the part.
- **A cylinder in a V-block.** A shaft of radius 1 along the $x$ axis lies in a V-block with two contacts at $x = 0$ and two at $x = 4$, at the points $(x, \pm\tfrac35, -\tfrac45)$ with normals toward the axis, and an end stop at $(0, \tfrac15, 0)$ with normal $(1, 0, 0)$. The rank is 5 and the null twist is $(0, 0, 0, 1, 0, 0)$, a turn about the axis. This is not a bad choice of points: for a contact on the cylinder the normal meets the axis, and for a contact on a flat end the normal is parallel to the axis, so the column of $\omega_x$ is zero for every such contact. A sixth locator on a milled flat at $(2, \tfrac12, \tfrac45)$ with normal $(0, 0, -1)$ gives rank 6.
- **[Modular fixture design](/modular-fixture-design/).** In the plane a twist has three entries $(\delta_x, \delta_y, \omega)$ and the rows are $(n_x, n_y, p_x n_y - p_y n_x)$. The Brost and Goldberg algorithm keeps a placement of three locators and a clamp only if the four rows have rank 3 and positively span $\mathbb{R}^3$, which is the planar form closure test of this page.
- **[Infinitesimal rigidity](/infinitesimal-rigidity/)** of a bar framework is the same idea for a different body: the rows of the rigidity matrix are the gradients of the bar lengths, and the framework is rigid to first order if the rank is as large as possible.

## Variations

- **Clamps and forces.** The clamps add rows with the same form. With friction, each contact gives a cone of forces instead of one direction, and the question becomes [force closure](/force-closure/): can the contact forces resist every external wrench? A [grasp wrench space](/grasp-wrench-space/) measures how well.
- **Quality of a layout.** Among layouts with rank 6, planners prefer a small error amplification, for example a large smallest singular value of $J$ or a large $\det(J^{\mathsf T} J)$. These are criteria for search over candidate locator positions, not part of the test.
- **Second order.** When the rank is less than 6, the curvatures of the part and of the locators at the contacts decide whether the part is still held. A part with concave curvature at a contact can be immobilized by fewer contacts than the first-order count (Rimon and Burdick 1998, cited on [fixture planning](/fixture-planning/)).
- **Bilateral contacts.** A pin in a tight hole constrains motion in both senses. Its rows enter the rank test as usual, and in the cone test each such row is added with both signs.

## Pitfalls

- **A full rank is not a hold.** Rank 6 says the position is unique. It says nothing about whether the part stays there: with six locators it never does without a clamp.
- **Inward normals.** The sign of $n_i$ does not change the rank, but it flips the cone test. Use one convention for all rows: here $n_i$ points from the locator into the part.
- **Floating point rank.** Locator layouts are often exactly degenerate, for example three locators at equal heights on one line. A rank found with a floating point tolerance can report 6 for a layout that is singular. Exact arithmetic, or a tolerance tied to the size of the part, avoids this.
- **Surfaces of revolution.** Contacts on a cylinder, a cone or a sphere cannot stop a turn about the axis, whatever their number, as the V-block shows. A flat, a keyway or a pin in a hole must take the last degree of freedom.
- **Points on edges and vertices.** The model needs a tangent plane at each contact. At an edge or a vertex the normal is not defined, and a locator there must be modeled as two or three rows, or moved.

## Exercises

1. Show that for the planar model the rows $(n_x, n_y, p_x n_y - p_y n_x)$ of three contacts have rank less than 3 if the three normal lines meet in one point or are all parallel. (Hint: the meeting point is the center of a turn that moves each contact along its tangent.)
2. Three locators on $z = 0$ at $(0, 0, 0)$, $(2, 0, 0)$, $(0, 2, 0)$, two on $y = 0$ at $(0, 0, 1)$ and $(2, 0, 1)$, and one on $x = 0$ at $(0, 1, 1)$. Compute $|\det J|$ with the formula of the 3-2-1 page. (Answer: $2 \cdot 2 \cdot 2 = 8$.)
3. A part is held by eight contacts whose rows come in four pairs $J_i$ and $-J_i$. Show that it has no detaching twist, and say when it is deterministic.

## References
