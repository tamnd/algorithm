---
tag: 0PK200
kind: theorem
slug: aronhold-kennedy-theorem
name: Aronhold-Kennedy theorem
aliases:
- Kennedy's theorem
- three centers theorem
area: cad/mechanism-and-assembly-design
level: core
summary: The three instant centers of any three bodies in plane motion lie on one line, which locates all centers of a linkage without solving equations.
prereqs: [instant-center-of-velocity]
see_also: [four-bar-linkage, slider-crank-mechanism, transmission-angle, fundamental-law-of-gearing, cam-pressure-angle, vector-loop-closure, watt-and-stephenson-six-bar]
sources:
  - paper: "Siegfried Aronhold, Grundzüge der kinematischen Geometrie, Verhandlungen des Vereins zur Beförderung des Gewerbefleißes in Preußen, 51 (1872), 129 to 155"
  - book: "Alexander B. W. Kennedy, The Mechanics of Machinery, Macmillan, London, 1886"
    locator: the chapter on virtual centres (general locator; no page number confirmed)
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 6.3 (p. 298, instant centers of velocity, Kennedy's rule) and Section 6.4 (p. 305, velocity analysis with instant centers)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: Chapter 3, the section on the Aronhold-Kennedy theorem of three centers
  - book: isbn:9780198561248
    title: Kenneth H. Hunt, Kinematic Geometry of Mechanisms, Oxford University Press, 1978
    locator: the chapters on instantaneous kinematics in the plane and in space (general locator)
---

The Aronhold-Kennedy theorem says that if three bodies move in a plane, the three [instant centers](/instant-center-of-velocity/) of their pairs lie on one line. A linkage gives some centers for free, at its pins and slides. The theorem then gives each other center as the intersection of two lines through known centers, so all the centers of a [four-bar linkage](/four-bar-linkage/) can be drawn with a ruler. Aronhold published it in 1872 and Kennedy, independently, in 1886.

This page proves the collinearity rule. The [instant center of velocity](/instant-center-of-velocity/) page defines the centers and counts them, $n(n - 1)/2$ for $n$ links.

## Statement

Let $J$ be the rotation of the plane by $+90°$. A plane rigid motion relative to a frame has the velocity field $v(p) = v_0 + \omega J p$, where $v_0$ is the velocity of the body point at the origin. Call $t = (v_0, \omega)$ its twist. Its instant center, as a point of the projective plane, is the homogeneous point

$$C(t) = (J v_0,\ \omega),$$

which is the ordinary point $J v_0/\omega$ when $\omega \ne 0$ and the point at infinity in the direction $J v_0$ when $\omega = 0$. For bodies $i$ and $j$ that move relative to each other, $P_{ij}$ is the center of the motion of $j$ relative to $i$, and $P_{ij} = P_{ji}$.

**Theorem (Aronhold 1872, Kennedy 1886).** Let $i$, $j$ and $k$ be three bodies in plane motion, each pair moving relative to each other. Then $P_{ij}$, $P_{ik}$ and $P_{jk}$ lie on one line of the projective plane. Moreover, if $\omega_j$ and $\omega_k$ are the angular velocities of $j$ and $k$ relative to $i$, and $\omega_j \ne \omega_k$, then

$$P_{jk} = \frac{\omega_k P_{ik} - \omega_j P_{ij}}{\omega_k - \omega_j},$$

where $P_{ij}$ or $P_{ik}$ is an ordinary point if its $\omega$ is not zero. If $\omega_j = \omega_k$, then $j$ translates relative to $k$, and $P_{jk}$ is the point at infinity of the line.

## In plain words

Three parts of a machine move in a flat plane. Each two of them have a point where they move together at this moment, like a shared pin. There are three such points, one for each pair. The theorem says that the three points are always on one straight line.

This is useful because some of the points are easy to see: a pin is one, and a slide puts one far away, square to the slide. If you know two points on a line, you can draw the line. If you know two lines through a missing point, the point is where they cross. So you can find all the points of a linkage with a ruler and no algebra. The ratio in the formula also tells you how fast the two parts turn against each other.

## Proof

Work in the frame of body $i$. Let $t_j = (v_j, \omega_j)$ and $t_k = (v_k, \omega_k)$ be the twists of $j$ and $k$ relative to $i$.

**Step 1, the map $C$ is linear and has no zero.** The map $t = (v_0, \omega) \mapsto (J v_0, \omega)$ is linear, and $J$ is invertible, so $C(t) = 0$ only if $t = 0$. A nonzero twist therefore gives a well defined projective point. For $\omega \ne 0$ the point $J v_0/\omega$ is the zero of the field: $v_0 + \omega J (J v_0/\omega) = v_0 + J^2 v_0 = 0$. For $\omega = 0$ the motion is a translation with velocity $v_0$, and $J v_0$ is the direction perpendicular to it. So $C(t)$ is the instant center as defined on the [instant center of velocity](/instant-center-of-velocity/) page.

**Step 2, the relative twist is the difference.** At this instant a point $p$ fixed to $j$ has the velocity $v_j + \omega_j J p$ in the frame $i$, and a point fixed to $k$ at the same place has $v_k + \omega_k J p$. The center $P_{jk}$ is the point where the two bodies have the same velocity, that is the zero of the field $(v_k - v_j) + (\omega_k - \omega_j) J p$. This field is the motion of $k$ relative to $j$ at this instant, written in the coordinates of $i$, with twist $t_k - t_j$. The motion of $j$ relative to $k$ has the opposite twist and the same center. If the field has no zero, the same argument as in step 1 puts the center at infinity. So $P_{jk} = C(t_k - t_j)$.

**Step 3, collinearity.** By linearity, $C(t_k - t_j) = C(t_k) - C(t_j)$. So the homogeneous vectors of $P_{ik}$, $P_{ij}$ and $P_{jk}$ satisfy one linear relation, and they span a subspace of $\mathbb{R}^3$ of dimension at most 2. Three points of the projective plane whose vectors span at most a 2-dimensional subspace lie on one line. If two of the three points coincide, any line through them both works.

**Step 4, the formula.** Write $C(t_j) = (\omega_j P_{ij}, \omega_j)$ when $\omega_j \ne 0$, and the same for $k$. If $\omega_j$ or $\omega_k$ is zero, the corresponding product $\omega P$ means $J v$, which is a finite vector, so the formula below still holds with that reading. Then $C(t_k - t_j) = (\omega_k P_{ik} - \omega_j P_{ij},\ \omega_k - \omega_j)$. If $\omega_k \ne \omega_j$, divide by the last coordinate to get the formula. If $\omega_k = \omega_j$, the last coordinate is zero, so $P_{jk}$ is at infinity, and since it is on the line of $P_{ij}$ and $P_{ik}$, it is the point at infinity of that line. $\blacksquare$

## Consequences

- **The centers of a four-bar.** With 1 the ground, 2 the input, 3 the coupler and 4 the output, the pins give $P_{12}$, $P_{23}$, $P_{34}$ and $P_{14}$. The theorem on the triples $\{1, 2, 3\}$ and $\{1, 3, 4\}$ puts $P_{13}$ on the lines $O_2A$ and $O_4B$, and on $\{1, 2, 4\}$ and $\{2, 3, 4\}$ puts $P_{24}$ on the lines $O_2O_4$ and $AB$. The [instant center of velocity](/instant-center-of-velocity/) page works a numerical case.
- **Velocity ratios.** The formula of the theorem, applied to the triple $\{1, 2, 4\}$ with $1$ as the reference body, gives $P_{24} = (\omega_4 O_4 - \omega_2 O_2)/(\omega_4 - \omega_2)$. With $O_2 = (0, 0)$ and $O_4 = (d, 0)$ this is $\omega_4/\omega_2 = x_{24}/(x_{24} - d)$. The three centers divide their line in the inverse ratio of the angular velocities: $P_{jk}$ is between $P_{ij}$ and $P_{ik}$ exactly when $j$ and $k$ turn in opposite directions relative to $i$. With the [transmission angle](/transmission-angle/), this gives the mechanical advantage.
- **The slider-crank.** The slide puts $P_{14}$ at infinity, perpendicular to the guide. The lines through it are the lines perpendicular to the guide, and the theorem gives $P_{13}$ on the vertical through the slider pin and $P_{24}$ on the vertical through the crank pivot, as on the [slider-crank mechanism](/slider-crank-mechanism/) page.
- **Gears and cams.** For two bodies in direct contact with fixed pivots, the center of their relative motion is on the line of the pivots and also on the common normal at the contact point, so it is the intersection of those two lines. The ratio of the angular velocities is fixed by where that point divides the line of centers. Keeping that point fixed for every position is the [fundamental law of gearing](/fundamental-law-of-gearing/). For a cam and a follower the same point gives the follower velocity, and the angle between the normal and the follower motion is the [cam pressure angle](/cam-pressure-angle/).
- **Linkages with more links.** A [Watt or Stephenson six-bar](/watt-and-stephenson-six-bar/) has 15 centers. The theorem gives the centers one by one from lines through known ones, but for some linkages with many loops no pair of lines through known centers exists for any missing center. Then one center is found from the velocity equations of the [vector loop closure](/vector-loop-closure/), and the theorem gives the rest.

## Tightness

**Collinearity is the only condition on the positions.** Let $P_{ij}$ and $P_{ik}$ be two different points and let $Q$ be any point on their line other than these two. Then there is a motion with these centers and $P_{jk} = Q$. Write $Q = P_{ij} + \lambda (P_{ik} - P_{ij})$ with $\lambda \ne 0, 1$. Let $j$ turn about $P_{ij}$ with $\omega_j = 1$ and $k$ turn about $P_{ik}$ with $\omega_k = \lambda/(\lambda - 1)$. Then $\omega_k - \omega_j = 1/(\lambda - 1)$ and the formula gives $(\omega_k P_{ik} - \omega_j P_{ij})/(\omega_k - \omega_j) = \lambda P_{ik} - (\lambda - 1) P_{ij} = Q$. The point at infinity of the line is reached with $\omega_k = \omega_j$. So no rule stronger than collinearity holds for the positions alone.

**The hypothesis that each pair moves.** If $j$ and $k$ are at rest relative to each other, $P_{jk}$ is not defined, and $P_{ij} = P_{ik}$, so the statement is empty.

**The plane.** In space a rigid motion has an instantaneous screw axis, not a center. The analogue is that the three screw axes of three bodies have a common perpendicular, because the three twists are linearly dependent in the same way. That is a statement about lines in space, not about points, and Hunt treats it with the other results of spatial instantaneous kinematics.

## History

Siegfried Aronhold gave the theorem in his 1872 paper Grundzüge der kinematischen Geometrie, in the transactions of the Prussian society for the promotion of industry. Alexander Kennedy found it independently and published it in The Mechanics of Machinery (1886), where the instant centers are called virtual centres. English texts long called it Kennedy's theorem or the theorem of three centers, and German texts the Satz von Aronhold-Kennedy. The joint name is now usual in textbooks such as that of Uicker, Pennock and Shigley.

## References
