---
tag: T7DN88
kind: definition
slug: instant-center-of-velocity
name: Instant center of velocity
aliases:
- instantaneous center of rotation
- instant centre
area: cad/mechanism-and-assembly-design
level: intro
summary: The point about which a link turns at an instant, where its velocity is zero. A planar mechanism with n links has n(n - 1)/2 of them.
prereqs: [kinematic-pair, four-bar-linkage]
see_also: [aronhold-kennedy-theorem, vector-loop-closure, transmission-angle, slider-crank-mechanism, forward-kinematics, kinematic-chain, watt-and-stephenson-six-bar]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Sections 6.3 (p. 298, instant centers of velocity), 6.4 (p. 305, velocity analysis with instant centers) and 6.5 (p. 313, centrodes)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: Chapter 3, the sections on instantaneous centers of velocity and the Aronhold-Kennedy theorem
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 4 (pp. 75 to 92), planar kinematics, the pole of a planar velocity
  - book: "Alexander B. W. Kennedy, The Mechanics of Machinery, Macmillan, London, 1886"
    locator: the chapter on virtual centres (general locator)
---

The instant center of velocity of a body in plane motion is the point of the plane, thought of as fixed to the body, whose velocity is zero at a given instant. At that instant the body turns about it, so the velocity of every other point is perpendicular to the line from the center and proportional to the distance. For two moving bodies the same idea gives a relative center, the point where the two bodies have the same velocity. A planar mechanism with $n$ links has one such center for each pair of links, so $n(n - 1)/2$ of them.

This page defines the centers and counts them. The [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/) proves the rule that the three centers of any three links lie on one line, which is how the centers are found without solving the position equations again.

## Definition

### Plane velocity fields

Let $J$ be the rotation of the plane by $+90°$, so $J(x, y) = (-y, x)$ and $J^2 = -I$. The velocity field of a rigid body in plane motion, relative to a frame, has the form

$$v(p) = v_0 + \omega J (p - o),$$

where $o$ is a reference point, $v_0$ is the velocity of the body point at $o$, and $\omega$ is the angular velocity. The pair $(v_0, \omega)$ is the planar twist of the body.

**Instant center.** If $\omega \ne 0$, the body has exactly one point with zero velocity, the **instant center**

$$P = o + \frac{J v_0}{\omega},$$

and $v(p) = \omega J (p - P)$ for every $p$.

*Proof.* The field is affine in $p$, and its linear part $\omega J$ is invertible because $\omega \ne 0$, so $v(p) = 0$ has exactly one solution. Check that $P$ is it: $v(P) = v_0 + \omega J (J v_0/\omega) = v_0 + J^2 v_0 = 0$. Then $v(p) = v(p) - v(P) = \omega J (p - P)$. $\blacksquare$

If $\omega = 0$ and $v_0 \ne 0$, the body translates and no point has zero velocity. Its instant center is then the point at infinity in the direction $J v_0$, perpendicular to the velocity. In homogeneous coordinates the center is $(J v_0 + \omega o,\ \omega)$ in both cases, which is how the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/) page treats it.

### Relative centers in a mechanism

Number the links $1$ to $n$. The relative instant center $P_{ij}$ of links $i$ and $j$ is the instant center of the motion of $j$ seen from $i$. Equivalently, it is the point which, taken as a point of $i$ and as a point of $j$, has the same velocity in any frame. The motion of $i$ seen from $j$ is the inverse motion, with the opposite twist, so $P_{ij} = P_{ji}$. When link 1 is the ground, $P_{1j}$ is the instant center of link $j$ in the usual sense.

**Count.** A planar mechanism with $n$ links has exactly $n(n - 1)/2$ relative instant centers, counted by the pairs of links.

*Proof.* Each unordered pair $\{i, j\}$ with $i \ne j$ has one center, because the center of a motion is unique when it exists and the symmetric case $P_{ji}$ is the same point. The pair $\{i, i\}$ has no center, since a body does not move relative to itself. So the centers are counted by the 2-element subsets of $n$ links, and there are $\binom{n}{2} = n(n - 1)/2$ of them. $\blacksquare$

The count is of labels, not of points: two different pairs can have their centers at the same point of the plane, and a center can be at infinity. A four-bar has 6 centers, a slider-crank also 6, and a [Watt or Stephenson six-bar](/watt-and-stephenson-six-bar/) has 15.

### Centers that can be read from the joints

- A revolute joint between $i$ and $j$ is the center $P_{ij}$, because the pin is a point of both links.
- A prismatic joint between $i$ and $j$ gives $P_{ij}$ at infinity, perpendicular to the slide, because the relative motion is a translation along it.
- Rolling without slip at a contact point gives $P_{ij}$ at that point, since the two bodies have the same velocity there.
- Sliding contact, as between a cam and a flat follower, puts $P_{ij}$ somewhere on the common normal at the contact point. One more line is needed to fix it.

These are the primary centers. The others come from the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/).

## Examples and non-examples

**The six centers of a four-bar.** In the notation of the [four-bar linkage](/four-bar-linkage/) page, let link 1 be the ground, 2 the input, 3 the coupler and 4 the output. The joints give $P_{12} = O_2$, $P_{23} = A$, $P_{34} = B$ and $P_{14} = O_4$. By the Aronhold-Kennedy theorem, $P_{13}$ lies on the line through $P_{12}$ and $P_{23}$ and on the line through $P_{14}$ and $P_{34}$, so it is the intersection of the lines $O_2A$ and $O_4B$. In the same way $P_{24}$ is the intersection of the ground line $O_2O_4$ and the coupler line $AB$.

**The velocity ratio from $P_{24}$.** The point $P_{24}$ has the same velocity as a point of link 2 and as a point of link 4: $\omega_2 J (P_{24} - O_2) = \omega_4 J (P_{24} - O_4)$. With $P_{24} = (x_{24}, 0)$ on the ground line,

$$\frac{\omega_4}{\omega_2} = \frac{x_{24}}{x_{24} - d}.$$

If $P_{24}$ lies outside the segment $O_2O_4$, the two links turn the same way; inside, they turn opposite ways. If there are no losses, the input power $T_2\omega_2$ equals the output power $T_4\omega_4$, so the mechanical advantage is $T_4/T_2 = \omega_2/\omega_4$.

**A numerical case.** Take $a = 2$, $b = 7$, $c = 5$, $d = 6$ and $\theta_2 = 60°$ on the open branch. The [vector loop closure](/vector-loop-closure/) gives $A = (1, 1.7321)$, $B = (7.2748, 4.8348)$, $\theta_3 = 26.311°$ and $\theta_4 = 75.229°$. The line $AB$ meets the ground line at $P_{24} = (-2.5028, 0)$, so $\omega_4/\omega_2 = -2.5028/(-8.5028) = 0.2944$, and the output turns the same way as the input, at about 0.29 of its speed. The lines $O_2A$ and $O_4B$ meet at $P_{13} = (11.0436, 19.1281)$. The coupler turns about $P_{13}$, and from $v_A = a\omega_2 J e^{i\theta_2} = \omega_3 J (A - P_{13})$ one gets $\omega_3/\omega_2 = -0.0996$. Both ratios agree with the velocity solution of the loop equation to about $10^{-15}$.

**The slider-crank.** In the [slider-crank mechanism](/slider-crank-mechanism/), with 1 the ground, 2 the crank, 3 the rod and 4 the slider, $P_{12} = O_2$, $P_{23} = A$, $P_{34} = B$, and $P_{14}$ is at infinity in the direction perpendicular to the guide. Then $P_{13}$ is where the line $O_2A$ meets the vertical line through $B$, and $P_{24}$ is where the line $AB$ meets the vertical line through $O_2$, and with $P_{24} = (0, y_{24})$ the slider velocity is $\dot x = -\omega_2 y_{24}$. This agrees with the formula $\dot x = -a\omega_2\sin(\theta_2 - \theta_3)/\cos\theta_3$ of that page, since $y_{24} = a\sin(\theta_2 - \theta_3)/\cos\theta_3$.

**Non-example: the center of curvature of a path.** The instant center $P_{13}$ of the coupler is not, in general, the center of curvature of the path of a coupler point. The instant center has zero velocity but in general not zero acceleration, so it moves along a curve, the fixed centrode, while the coupler's own copy of it moves along the moving centrode. The two centrodes roll on each other without slip, a standard result given in Norton Section 6.5.

**Non-example: a point of zero acceleration.** The point of a body with zero acceleration, the acceleration pole, is a different point in general. Using the instant center as the center of acceleration is a common error.

**Non-example: spatial motion.** In space, a rigid motion with nonzero angular velocity has an instantaneous screw axis, not a point, and points on that axis can still move along it.

## Related definitions

- [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/): the three centers of three links lie on one line, which locates the secondary centers.
- [Kinematic pair](/kinematic-pair/): the joint types that give the primary centers.
- [Vector loop closure](/vector-loop-closure/): the algebraic velocity analysis that the instant centers replace with a drawing.
- [Transmission angle](/transmission-angle/): the angle at the output pin, which with the instant centers gives the mechanical advantage.
- [Forward kinematics](/forward-kinematics/): in robotics the same velocity field appears as the planar twist of a link.

### History

The fact that a plane motion is, at each instant, a rotation about one point is older than machine kinematics. In the kinematics of machines, Aronhold (1872) and Kennedy (1886) used the center of each pair of links in a systematic way, and Kennedy called them virtual centres in The Mechanics of Machinery.

## References
