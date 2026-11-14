---
tag: 3F65BA
kind: model
slug: small-displacement-torsor
name: Small displacement torsor
aliases:
- SDT model
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Bourdet and Clement's model of the small deviation of a feature from its nominal place as a screw of three rotations and three translations, linear in analysis.
prereqs: [rigid-body-transformation, geometric-dimensioning-and-tolerancing]
see_also: [rigid-body-twist, rodrigues-rotation-formula, skew-symmetric-matrix-of-a-vector, requicha-tolerance-zone-theory, tolerance-map, jacobian-torsor-model, least-squares-reference-feature, minimum-zone-flatness]
sources:
  - paper: "Pierre Bourdet, Luc Mathieu, Claire Lartigue and Alex Ballu, The concept of the small displacement torsor in metrology, in Advanced Mathematical Tools in Metrology II, Series on Advances in Mathematics for Applied Sciences 40, World Scientific, 1996, 110 to 122"
    locator: the whole chapter (the torsor of a small displacement, its use for the deviation of a substitute feature, and the components left free by the invariance of a feature)
  - paper: doi:10.1016/S0007-8506(07)61687-4
    title: Pierre Bourdet and André Clément, A study of optimal-criteria identification based on the small-displacement screw model, CIRP Annals 37(1), 503 to 506, 1988
    locator: the whole paper (the linearized deviation of measured points under a small displacement screw, and the fitting of a feature under several criteria with it)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, the exponential coordinates of a rotation, Rodrigues' formula and twists
  - url: https://arxiv.org/abs/1106.6148
    title: Denis Teissandier, Vincent Delos and Yves Couétard, Operations on polytopes, application to tolerance analysis, arXiv 1106.6148, 2011 (a paper of the 6th CIRP Seminar on Computer Aided Tolerancing, 1999)
    locator: the whole paper (geometric and contact specifications as polytopes of torsors, combined by Minkowski sums and intersections)
  - paper: doi:10.1016/j.cad.2014.02.014
    title: Hua Chen, Sun Jin, Zhimin Li and Xinmin Lai, A comprehensive study of three dimensional tolerance analysis methods, Computer-Aided Design 53, 1 to 13, 2014
    locator: the parts on the small displacement torsor and on its use in the other 3D tolerance analysis methods
---

The small displacement torsor (SDT) describes how far a feature of a real part lies from its nominal place by one small rigid motion: three small rotations and three small translations. Bourdet and Clément developed it for coordinate metrology, and Bourdet, Mathieu, Lartigue and Ballu gave the standard account in 1996. The real surface is first replaced by an ideal *substitute feature* of the nominal shape, a plane, cylinder or sphere fitted to the measured points. The SDT is the rigid motion that takes the nominal feature to the substitute, kept to first order. To first order a rigid motion moves each point $M$ by $D(M) = D(O) + \omega \times \vec{OM}$, which is linear in the six numbers. Constraints from tolerance zones become linear inequalities, and deviations along a chain of parts add. The price is the first-order (small-angle) approximation, which this page bounds, and the loss of form error, which the substitute feature removes. [Requicha's zones](/requicha-tolerance-zone-theory/) keep form and need no approximation; [Tolerance-Maps](/tolerance-map/) and the [Jacobian-torsor model](/jacobian-torsor-model/) build on the torsor.

## The machine

The "machine" of a variation model is its representation of a part and its assumptions about the deviations.

**The representation.** Write $[\omega]$ for the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of a vector $\omega$, so that $[\omega] p = \omega \times p$. A *twist* is the velocity field of a rigid body: a pair of vectors $(\omega, v_O)$ such that the velocity of any point $M$ is $v_O + \omega \times \vec{OM}$. A *torsor* is the French name for any field of vectors of this form, given by its two *reduction elements* at one point; a twist is a torsor, and so is a field of moments of a force system. The SDT of a feature at a point $O$ is the pair

$$ \mathcal{T} = \{\omega, \; D(O)\}_O, \qquad \omega = (\alpha, \beta, \gamma), \quad D(O) = (u, v, w), $$

and the point $M$ of the feature moves by $D(M) = D(O) + \omega \times \vec{OM}$. The vector $\omega$ holds three small rotation angles in radians about the axes of the frame, and $D(O)$ is the small translation of $O$. The same six numbers describe a whole part (the *deviation torsor* of the part), the deviation of a feature on a part, or the free play between two features in contact (the *gap torsor*).

A feature does not fix all six numbers. A motion that maps the nominal feature onto itself is invisible, so the components along such motions are undetermined. A plane $z = 0$ is unchanged by rotation about $z$ and translation along $x$ and $y$, so its torsor keeps only $(\alpha, \beta, w)$. A cylinder along $z$ keeps $(\alpha, \beta, u, v)$, and a sphere keeps the translation of its centre. A tolerance zone then becomes a set of allowed values of the determined components.

**Assumptions.** The model takes these as given.

- Each feature is replaced by an ideal substitute feature, so form error is not part of the torsor. The fit that makes the substitute is a separate step, such as a [least squares reference feature](/least-squares-reference-feature/) or a minimum zone fit.
- The rotations are small, $\theta = |\omega| \ll 1$ rad, and the model keeps only the first-order part of the rigid motion. This is a first-order (small-angle) approximation; the error bound is the first result below.
- The deviation of a size, such as the radius of a cylinder, is not a rigid motion. It is carried as an extra parameter when it is needed.
- Deviations of features in a chain add, which holds to first order only.

## What it counts

A variation model counts no cost. This section says which variations the model can express.

- **Location and orientation of ideal features.** Position, orientation, runout and profile tolerances of planes, cylinders, spheres and cones become linear constraints on the determined components of each torsor. A flat face in a zone gives the inequality of the plane example below.
- **Free play in joints.** A gap torsor between two parts in contact holds the small motions that the clearance allows. The contact conditions are linear constraints on it.
- **Measured deviations.** The torsor of a substitute feature is what a coordinate measuring machine reports as the position and orientation error of the feature.
- **What it cannot express.** Form error inside a feature, such as a wavy face, is lost when the substitute replaces the surface. Large rotations are outside the model, because the small-angle error grows with $\theta^2$. Size enters only as an added parameter, and the model alone holds no statistics; it describes one part, and a distribution needs a [Monte Carlo](/monte-carlo-tolerance-analysis/) or statistical layer.

## Relation to other models

- **[Requicha's tolerance zone theory](/requicha-tolerance-zone-theory/).** Requicha's zones test the whole surface exactly. The SDT keeps only the rigid deviation of a fitted ideal feature, to first order. The set of torsors whose moved feature lies in a Requicha zone is the zone written in torsor coordinates.
- **[Tolerance-Map](/tolerance-map/).** A T-Map is the set of all small displacements of a feature that its tolerances allow, drawn in a space of the determined components. In torsor terms it is the domain of the SDT of that feature.
- **[Jacobian-torsor model](/jacobian-torsor-model/).** It carries the torsor of each feature, with interval bounds on its components, to a functional requirement through a Jacobian matrix of the assembly. The transport law below is the step that moves a torsor from one point to another.
- **Polytopes of torsors.** Teissandier, Delos and Couétard write each specification as a polytope of torsors and combine them by [Minkowski sums](/minkowski-sum/) and intersections. This uses the linearity of the SDT.
- **Robotics.** The torsor of a small displacement is the twist of a rigid motion times a small time. The transport law is the first-order form of the [adjoint map](/adjoint-map-se3/), and the existence of an axis is the small form of [Chasles' theorem](/chasles-theorem/) on [screw motions](/screw-motion/).
- **[Direct linearization](/direct-linearization-method/).** DLM linearizes vector loops of dimensions in a plane or in space. The SDT linearizes rigid motions of features, so it carries the GD&T tolerances of 3D features that DLM handles less directly.

## Known results in the model

The results below are proved here. The fitting results are from Bourdet and Clément and are cited. There are no standard benchmarks for tolerance models, and no measured results are claimed.

**The SDT is the first-order part of a rigid motion.** Let a rigid motion be $p \mapsto R p + u$, with $R$ the rotation by angle $\theta$ about the unit axis $\omega / \theta$, so $\omega$ is its rotation vector. Then for every point $p$

$$ R p + u - p = u + \omega \times p + E(p), \qquad |E(p)| = |p_\perp| \sqrt{(\theta - \sin \theta)^2 + (1 - \cos \theta)^2} \le \frac{\theta^2}{2} |p_\perp|, $$

where $p_\perp$ is the part of $p$ at right angles to $\omega$. In matrix form $R = I + [\omega] + O(\theta^2)$.

*Proof.* [Rodrigues' formula](/rodrigues-rotation-formula/) gives $R = I + \frac{\sin \theta}{\theta} [\omega] + \frac{1 - \cos \theta}{\theta^2} [\omega]^2$. Write $p = p_\parallel + p_\perp$ with $p_\parallel$ along $\omega$. Then $\omega \times p = \omega \times p_\perp$, which has length $\theta |p_\perp|$, and $[\omega]^2 p = \omega \times (\omega \times p_\perp) = -\theta^2 p_\perp$. So

$$ E(p) = R p - p - \omega \times p = \Big(\frac{\sin \theta}{\theta} - 1\Big)\, \omega \times p_\perp - (1 - \cos \theta)\, p_\perp. $$

The vectors $\omega \times p_\perp$ and $p_\perp$ are at right angles, with lengths $\theta |p_\perp|$ and $|p_\perp|$, so $|E(p)|^2 = |p_\perp|^2 \big((\sin \theta - \theta)^2 + (1 - \cos \theta)^2\big)$. This is $|p_\perp|^2 |e^{i\theta} - 1 - i\theta|^2$, and

$$ |e^{i\theta} - 1 - i\theta| = \Big|\int_0^\theta i\,(e^{is} - 1)\, ds\Big| \le \int_0^\theta |e^{is} - 1|\, ds \le \int_0^\theta s\, ds = \frac{\theta^2}{2}, $$

because $|e^{is} - 1| = 2 |\sin(s/2)| \le s$. $\square$

Any other set of three small angles, such as Euler or Cardan angles, gives the same first-order part, because their rotation matrices differ from $R$ by $O(\theta^2)$. The six numbers of an SDT therefore have one meaning only to first order.

*Numbers.* For $\theta = 0.001$ rad and a point 100 mm from the axis the error is at most $0.5 \cdot 10^{-6} \cdot 100 = 5 \cdot 10^{-5}$ mm, small against a tolerance of 0.01 mm. For $\theta = 0.01$ rad it is up to 0.005 mm, half of that tolerance, and the first-order model is then too coarse for it.

**Transport.** If $D(M) = D(O) + \omega \times \vec{OM}$ for all $M$, then for any two points $A$ and $B$, $D(B) = D(A) + \omega \times \vec{AB}$, with the same $\omega$. *Proof.* Subtract the two equations for $A$ and $B$ and use $\vec{OB} - \vec{OA} = \vec{AB}$. $\square$ So a torsor is fixed by $\omega$ and the translation at one point, and moving the reference point is a linear map.

**The scalar invariant and the axis.** $\omega \cdot D(M)$ is the same at every point, because $\omega \cdot (\omega \times \vec{OM}) = 0$. If $\omega \ne 0$, the points where $D(M)$ is parallel to $\omega$ form a line parallel to $\omega$, the axis of the torsor. *Proof.* $D(M) = D(O) + \omega \times \vec{OM}$ is parallel to $\omega$ exactly when its part at right angles to $\omega$ is zero. That part is $D(O)_\perp + \omega \times \vec{OM}$, and the map $x \mapsto \omega \times x$ is a bijection of the plane at right angles to $\omega$, so there is one solution $\vec{OM}_\perp$, plus any multiple of $\omega$. $\square$ A small displacement is thus a small screw: a rotation $\theta$ about this axis with a slide $(\omega \cdot D)/\theta$ along it.

**Deviations add to first order.** Let $R_1, R_2$ have rotation vectors $\omega_1, \omega_2$ of size at most $\theta$. Then $R_2 R_1 = I + [\omega_1] + [\omega_2] + O(\theta^2)$, and the composed motion has, to first order, the torsor $\mathcal{T}_1 + \mathcal{T}_2$ once both are taken at the same point. *Proof.* Multiply $(I + [\omega_2] + O(\theta^2))(I + [\omega_1] + O(\theta^2))$; the product $[\omega_2][\omega_1]$ is $O(\theta^2)$. The translations add in the same way after transport. $\square$ The exact composition does not commute: $R_1 R_2 - R_2 R_1 = [\omega_1][\omega_2] - [\omega_2][\omega_1] + O(\theta^3) = [\omega_1 \times \omega_2] + O(\theta^3)$, by the identity $[a][b] - [b][a] = [a \times b]$. This is the second-order error that summing torsors along an assembly ignores.

**A plane face in a zone.** Let the nominal face be the rectangle $|x| \le a$, $|y| \le b$ in the plane $z = 0$, with $O$ at its centre, and let the zone be the slab $|z| \le t/2$. A point $(x, y, 0)$ moves along $z$ by $w + \alpha y - \beta x$, the $z$ part of $D(O) + \omega \times (x, y, 0)$. The face stays in the zone, to first order, if and only if

$$ |w| + b |\alpha| + a |\beta| \le t/2. $$

*Proof.* The normal displacement is an affine function of $(x, y)$, so its largest and smallest values on the rectangle are at the corners. They are $w + b|\alpha| + a|\beta|$ and $w - b|\alpha| - a|\beta|$. Both lie in $[-t/2, t/2]$ exactly when the inequality holds. $\square$ The allowed set in $(w, \alpha, \beta)$ is an octahedron, a [convex polytope](/convex-polytope/) with vertices $(\pm t/2, 0, 0)$, $(0, \pm t/(2b), 0)$ and $(0, 0, \pm t/(2a))$. For a 40 by 20 face ($a = 20$, $b = 10$) and $t = 0.1$ mm, the largest tilt about $x$ is 0.005 rad and about $y$ is 0.0025 rad. For a round face the same argument gives a double cone, the [Tolerance-Map](/tolerance-map/) of Davidson, Mujezinovic and Shah.

**Fitting by linear algebra (Bourdet and Clément).** Let a measured point $q_i$ lie near the nominal point $p_i$ of a feature with unit normal $n_i$, and let $e_i = n_i \cdot (q_i - p_i)$ be its measured deviation. After a small displacement $\mathcal{T}$ of the ideal feature, the residual is, to first order,

$$ r_i = e_i - n_i \cdot D(O) - (\vec{O p_i} \times n_i) \cdot \omega, $$

by the identity $n \cdot (\omega \times x) = (x \times n) \cdot \omega$. The residual is linear in the six components. Least squares fitting is then a linear least squares problem in the determined components. Fitting the thinnest zone, the minimum zone criterion, is a [linear program](/linear-programming-problem/): minimize $h$ subject to $-h \le r_i \le h$. Bourdet and Clément treat these criteria and the tangent criteria in the same framework; the linear forms hold only within the first-order model, and exact minimum zone results need the nonlinear problem, as on [minimum zone flatness](/minimum-zone-flatness/).

## References
