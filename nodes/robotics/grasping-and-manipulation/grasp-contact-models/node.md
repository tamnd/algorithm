---
tag: 5F8B07
kind: model
slug: grasp-contact-models
name: Grasp contact models
aliases:
- point contact with friction
- soft finger contact
- frictionless point contact
area: robotics/grasping-and-manipulation
level: intro
summary: "The three standard models of what a finger contact can transmit to a grasped body: a frictionless point (normal force), a hard finger (friction cone) and a soft finger (friction cone and torsion)."
prereqs: [friction-cone]
see_also: [grasp-matrix, polyhedral-friction-cone, force-closure, form-closure, limit-surface, rigid-contact-complementarity, montana-contact-kinematics, contact-wrench-cone]
sources:
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.1 (Models and Definitions), the contact models PwoF, HF and SF and their sizes in Table 38.2; the chapter is pages 955 to 988"
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (contact models, wrench bases and friction cones of the frictionless, frictional and soft finger contacts)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 12, Section 12.1 (contact kinematics, including Section 12.1.2 on rolling, sliding and breaking contacts) and Section 12.2.1 (Friction)
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 5 (Rigid Body Statics), Section 5.3 (contact wrenches and wrench cones)
  - paper: "J. Kenneth Salisbury, Kinematic and Force Analysis of Articulated Hands, PhD thesis, Stanford University, 1982"
    locator: the classification of contact types by the wrenches that each one transmits
  - paper: "Robert D. Howe and Mark R. Cutkosky, Practical force-motion models for sliding manipulation, International Journal of Robotics Research 15(6), 557-572, 1996"
    locator: the coupled limits of friction force and friction moment for a contact patch
---

A grasp contact model says which forces and moments one finger can apply to a grasped body through one contact, and which relative motions the contact blocks. Grasp analysis uses three standard models: the frictionless point, which pushes only along the normal; the hard finger, which also pushes sideways inside a [friction cone](/friction-cone/); and the soft finger, which adds a limited twist about the normal. Each model is a linear map from a few contact force components to a wrench, together with a convex cone of allowed components. The [grasp matrix](/grasp-matrix/), the tests for [form closure](/form-closure/) and [force closure](/force-closure/), and the grasp quality scores are all built from these models.

## The machine

**Bodies and frames.** A rigid object is held by $c$ contacts with rigid fingers. Contact $i$ is at the point $p_i$ of the object surface. Its contact frame $\{C_i\}$ has the origin at $p_i$, the $z$ axis along the unit normal $n_i$ that points into the object, and the $x$ and $y$ axes in the tangent plane. The rotation of $\{C_i\}$ in the object frame $\{b\}$ is $R_i$. A wrench is written moment first, $\mathcal{F} = (m, f)$.

**Contact force components.** Contact $i$ transmits a vector $\lambda_i \in \mathbb{R}^{m_i}$ of force components in $\{C_i\}$. A wrench basis $B_i$ (a $6 \times m_i$ matrix) maps them to the wrench at the contact frame, $\mathcal{F}_{C_i} = B_i \lambda_i$. The adjoint transpose $\mathrm{Ad}^T$ of the contact pose maps that wrench to the object frame, so the contact applies $G_i \lambda_i$ to the object, with $G_i = \mathrm{Ad}_{T_{C_i b}}^T B_i$. The [grasp matrix](/grasp-matrix/) is $G = [G_1 \cdots G_c]$.

**The three models.**

| Model | $m_i$ (space, plane) | Wrench basis $B_i$ (moment rows first) | Allowed components $\lambda_i$ | Relative motion blocked |
|---|---|---|---|---|
| Frictionless point (PwoF) | 1, 1 | $(0, 0, 0, 0, 0, 1)^T$ | $f_z \ge 0$ | velocity along the normal |
| Hard finger (HF) | 3, 2 | $\begin{pmatrix} 0_{3 \times 3} \\ I_3 \end{pmatrix}$ | $\sqrt{f_x^2 + f_y^2} \le \mu f_z$ | the three velocities of the contact point |
| Soft finger (SF) | 4, not used | $\begin{pmatrix} 0_{3 \times 3} & e_3 \\ I_3 & 0 \end{pmatrix}$ | $\sqrt{f_x^2 + f_y^2} \le \mu f_z$ and $\lvert m_z \rvert \le \gamma f_z$ | the three velocities and the spin about the normal |

Here $e_3 = (0, 0, 1)^T$, $\mu$ is the dimensionless coefficient of static friction, and $\gamma$ is the torsional friction coefficient, with the unit of a length (meters, because $m_z$ is in newton meters and $f_z$ in newtons). The Handbook writes the sizes as $n_\lambda = 1, 3, 4$ in space and $1, 2$ in the plane.

**Standing assumptions.** The object and the fingers are rigid. Each contact is a point, or for the soft finger a patch small enough to be treated as a point that can also resist twist. Friction obeys Coulomb's law with one coefficient. The analysis is quasi-static: inertial forces are neglected or put into the external wrench. The contact neither breaks nor slides while the model is used; the contact force stays inside its cone. Contacts cannot pull.

**The motion side.** The model is dual to a set of constraints on the relative twist. With the object twist $\mathcal{V}$ (in $\{b\}$) and a fixed finger, the components of the object velocity at the contact that the contact transmits are $G_i^T \mathcal{V}$. A hard finger requires all three translational components to be zero when the contact sticks; a frictionless point constrains only the normal component, and only as an inequality $n_i^T \dot{p} \ge 0$ when the contact may break. The power of the contact force is $\lambda_i^T G_i^T \mathcal{V}$, the same number computed on the force side or on the motion side.

## What it counts

For each contact, the model gives the set of wrenches that the contact can apply to the object, the cone $\{G_i \lambda_i : \lambda_i \in FC_i\}$, and the components of relative motion that the contact blocks. For a whole grasp it gives:

- the number $m = \sum_i m_i$ of contact force components, which is the number of columns of the grasp matrix;
- the set of total contact wrenches $\{G\lambda : \lambda_i \in FC_i\}$, whose interior decides [force closure](/force-closure/);
- for a given external wrench $\mathcal{F}_{ext}$, the set of contact forces $\lambda$ with $G\lambda = -\mathcal{F}_{ext}$ and each $\lambda_i$ in its cone; the model predicts that the grasp holds without slip if this set is not empty;
- the internal forces, the contact forces in the null space of $G$, which squeeze the object without moving it.

**A worked size count.** A three-finger grasp in space has $m = 3$ with frictionless points, $m = 9$ with hard fingers and $m = 12$ with soft fingers. The wrench space has dimension 6, so the grasp matrix is $6 \times 3$, $6 \times 9$ or $6 \times 12$. With hard fingers the null space has dimension at least $9 - 6 = 3$: the three squeezes along the sides of the triangle of contacts.

**A worked torsion limit.** A soft finger with $\gamma = 0.005$ m that presses with $f_z = 10$ N resists a twist about its normal of up to $\gamma f_z = 0.05$ N m, and with $\mu = 0.5$ a tangential force of up to $5$ N. These two limits are separate in the model of the table; Howe and Cutkosky (1996) show that a real patch couples them, so that a patch that already slides sideways resists less twist.

## Relation to other models

- **[Friction cone](/friction-cone/).** The hard finger is exactly the friction cone placed in the contact frame. The soft finger adds the torsion interval.
- **[Polyhedral friction cone](/polyhedral-friction-cone/).** Linear programs replace the cone of each model by a pyramid. For a soft finger each edge is used twice, with the moments $\pm\gamma$ about the normal.
- **[Limit surface](/limit-surface/).** For a contact patch that slides, the friction force and friction moment are coupled through a convex limit surface. The soft finger model with separate limits is a box-shaped simplification of it.
- **[Rigid contact complementarity](/rigid-contact-complementarity/).** Adds the dynamics, the sliding case and the breaking of contact. The grasp contact models are its sticking case.
- **[Contact wrench cone](/contact-wrench-cone/).** A flat foot or a flat finger with finite area transmits the wrenches of a whole patch. Its cone is the sum of the hard finger cones at the corners of the patch.
- **[Montana contact kinematics](/montana-contact-kinematics/).** Describes how the contact point moves on both surfaces when the bodies roll, which these static models do not.
- **Compliant contact.** Models with springs at the contact allow a contact force that depends on a small penetration, which removes the static indeterminacy of rigid models but adds stiffness parameters.

## Known results in the model

- **Frictionless points.** A body can be immobilized only if the contact wrenches positively span the wrench space, which needs at least 4 contacts in the plane and 7 in space. For bodies that are not a disc or a surface of revolution, 4 and 7 suffice ([finger bounds for form closure](/finger-bounds-for-form-closure/)).
- **Hard fingers.** In the plane, 3 hard fingers suffice for force closure of a body with a piecewise smooth boundary, and in space 4 suffice (Markenscoff, Ni and Papadimitriou 1990). In the plane two hard fingers can give force closure: this is the [antipodal grasp](/antipodal-grasp/) condition of Nguyen (1988).
- **Two hard fingers in space.** They never give force closure, because no force through the two contact points has a moment about the line that joins them.
- **Two soft fingers in space.** They can give force closure: the torsion about the normals resists the moment about the line of the contacts. The Handbook states that two soft fingers or three hard fingers that are not collinear suffice in space.
- **Decision procedure.** With pyramids in place of cones, force closure under any of the three models is decided by a linear program, the [force-closure test](/force-closure-test/).
- **Frictionless points and form closure.** With $\mu = 0$, force closure under the frictionless model is the same as first-order [form closure](/form-closure/).

## References
