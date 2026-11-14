---
tag: M4KDD2
kind: theorem
slug: fundamental-law-of-gearing
name: Fundamental law of gearing
aliases:
- law of conjugate action
- Camus theorem of gearing
area: cad/mechanism-and-assembly-design
level: intro
summary: Two gear teeth keep a constant speed ratio exactly when the common normal at their contact always passes through a fixed pitch point on the line of centers.
prereqs: [instant-center-of-velocity, aronhold-kennedy-theorem]
see_also: [involute-gear-tooth, gear-contact-ratio, gear-generation-by-enveloping, gear-undercutting, willis-formula, cam-pressure-angle]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 9.1 (p. 491, rolling cylinders) and Section 9.2 (p. 492, the fundamental law of gearing, with the involute tooth form on p. 493 and changing center distance on p. 495)
  - book: isbn:9780073398204
    title: Richard G. Budynas and J. Keith Nisbett, Shigley's Mechanical Engineering Design, 10th edition, McGraw-Hill
    locator: Section 13-3, conjugate action
  - book: isbn:9780521815178
    title: Faydor L. Litvin and Alfonso Fuentes, Gear Geometry and Applied Theory, 2nd edition, Cambridge University Press, 2004
    locator: Chapter 3 (centrodes, axodes and operating pitch surfaces) and Chapter 6 (conjugated surfaces and curves)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on spur gears, the fundamental law of toothed gearing (general locator)
  - book: "Robert Willis, Principles of Mechanism, John W. Parker, London, 1841"
    locator: the chapters on the communication of motion by rolling contact and by sliding contact of teeth (general locator)
  - paper: "Faydor L. Litvin, Development of Gear Technology and Theory of Gearing, NASA Reference Publication 1406, ARL-TR-1500, 1998"
    locator: the history of the theory of gearing and the biographies of its founders (general locator)
---

The fundamental law of gearing says when two toothed wheels turn at a constant ratio of speeds. Each gear turns about a fixed center, and the line through the two centers is the line of centers. The teeth push on each other at a contact point, and the common normal is the line through that point square to both tooth surfaces. The law says that the speed ratio at an instant is fixed by where the common normal crosses the line of centers, and so the ratio stays constant exactly when that crossing point, the pitch point, does not move. Tooth shapes that meet this condition are called conjugate. The law is the reason gear teeth have special shapes: a tooth of arbitrary shape gives a speed that wobbles as each tooth passes, and that causes vibration and noise.

## Statement

Let body 1 turn about the fixed point $O_1$ with the angular velocity $\omega_1$, and body 2 about the fixed point $O_2$ with $\omega_2$, in one plane. Put $O_1$ at the origin and $O_2 = (c, 0)$ with $c > 0$, so the line of centers is the $x$ axis and $c$ is the center distance. Assume that a smooth curve on body 1 and a smooth curve on body 2 touch at the point $K$, and stay in contact, with the common unit normal $n$ at $K$. Assume that $n$ is not along the line of centers, and let the normal line through $K$ cross the line of centers at $P = (p, 0)$.

**Theorem.** If $p \ne c$, the angular velocities satisfy

$$\frac{\omega_2}{\omega_1} = \frac{p}{p - c} = -\frac{\overline{O_1P}}{\overline{PO_2}},$$

where $\overline{O_1P} = p$ and $\overline{PO_2} = c - p$ are signed lengths along the line of centers. The point $P$ is the instant center of the motion of body 2 relative to body 1. So the ratio $\omega_2/\omega_1$ is constant through the mesh if and only if $P$ is a fixed point of the line of centers.

When $P$ is fixed, it is the pitch point. The pitch circles are the circles about $O_1$ and $O_2$ through $P$, with the radii $r_1 = |p|$ and $r_2 = |c - p|$, and they roll on each other without slipping. For external gears $P$ lies between the centers, the gears turn in opposite directions, and $|\omega_2/\omega_1| = r_1/r_2$.

## In plain words

Two gears push on each other through the teeth that touch. At the point of touch, draw the line that is square to both tooth faces. Where this line cuts the line between the two shafts, the two gears move at the same speed, as if they were two smooth wheels rolling on each other at that point. If the crossing point stays in the same place while the teeth slide past each other, the speed ratio stays the same, and the gears turn smoothly. If the crossing point moves, the speed ratio changes all the time. Good tooth shapes keep the crossing point still.

## Proof

**Step 1, the contact condition.** Let $J$ be the rotation by $+90°$, so $J(a, b) = (-b, a)$. The point of body 1 at $K$ has the velocity $v_1 = \omega_1 J(K - O_1)$, and the point of body 2 at $K$ has $v_2 = \omega_2 J(K - O_2)$. The bodies are rigid and stay in contact, so they neither separate nor overlap along the normal, and the two velocities have the same normal part:

$$n \cdot v_1 = n \cdot v_2.$$

They may differ along the tangent, which is the sliding of the teeth.

**Step 2, moments about the centers.** For any vector $a$, $n \cdot Ja = -n_x a_y + n_y a_x = a \times n$, where $a \times b = a_x b_y - a_y b_x$. So the condition reads

$$\omega_1 (K - O_1) \times n = \omega_2 (K - O_2) \times n.$$

The point $P$ is on the normal line through $K$, so $K - P$ is a multiple of $n$, and $(K - P) \times n = 0$. Hence $(K - O_i) \times n = (P - O_i) \times n$ for $i = 1, 2$. With $u = (1, 0)$, $P - O_1 = p\,u$ and $P - O_2 = (p - c)\,u$, so

$$\omega_1\, p\, (u \times n) = \omega_2\, (p - c)\, (u \times n).$$

**Step 3, the ratio.** The normal is not along the line of centers, so $u \times n \ne 0$, and $\omega_1 p = \omega_2 (p - c)$. With $p \ne c$ this gives $\omega_2/\omega_1 = p/(p - c)$.

**Step 4, $P$ is the relative instant center.** At $P$ the two bodies have the velocities $\omega_1 J(P - O_1) = \omega_1 p\, Ju$ and $\omega_2 J(P - O_2) = \omega_2 (p - c)\, Ju$, which are equal by Step 3. So $P$ is the point where the two bodies move together, the instant center $P_{12}$ of their relative motion. This agrees with the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/): with the ground as the third body, $P_{12}$ is on the line through the centers $O_1$ and $O_2$.

**Step 5, constant ratio if and only if $P$ is fixed.** If $P$ is fixed, $p$ is constant, and so is $p/(p - c)$. Conversely, let $R = \omega_2/\omega_1$. From $\omega_1 p = \omega_2(p - c)$ we get $p(R - 1) = Rc$. If $R = 1$ this forces $c = 0$, which is excluded, so $R \ne 1$ and $p = Rc/(R - 1)$. This is a function of $R$ alone, so a constant $R$ gives a constant $p$.

**Step 6, the pitch circles roll.** When $P$ is fixed, the circles about $O_1$ and $O_2$ through $P$ touch at $P$. By Step 4 their points at $P$ have the same velocity at each instant, so they roll on each other with no slip. If $0 < p < c$, then $p/(p - c) < 0$, so the gears turn in opposite directions with $|\omega_2/\omega_1| = p/(c - p) = r_1/r_2$. $\blacksquare$

## Consequences

- **Teeth and pitch.** Equal teeth must be spaced equally on the two pitch circles, so the number of teeth is proportional to the pitch radius. With $z_1$ and $z_2$ teeth, $|\omega_2/\omega_1| = r_1/r_2 = z_1/z_2$. For the module $m$, the pitch radius is $r = mz/2$. Gears with $m = 4$ mm, $z_1 = 20$ and $z_2 = 30$ have $r_1 = 40$ mm, $r_2 = 60$ mm, $c = 100$ mm and $\omega_2/\omega_1 = -2/3$.
- **The sliding speed.** The motion of body 2 relative to body 1 is, at each instant, a rotation about $P$ with the rate $\omega_2 - \omega_1$. So the sliding speed of the teeth at $K$ is $|\omega_2 - \omega_1|\,|KP|$. It is zero only when the contact is at the pitch point. For external gears $\omega_1$ and $\omega_2$ have opposite signs, so the rate is $|\omega_1| + |\omega_2|$. In the example, at $\omega_1 = 100$ rad/s and $|KP| = 5$ mm, the sliding speed is $(100 + 66.7) \cdot 5 = 833$ mm/s.
- **The involute.** The normal of an involute of a circle is tangent to that circle. Two involutes on base circles about $O_1$ and $O_2$ therefore have, as their common normal, a common internal tangent of the two base circles. This line is fixed, so it crosses the line of centers at a fixed point, and the ratio is the ratio of the base radii for any center distance. The [involute gear tooth](/involute-gear-tooth/) page proves this in full.
- **Conjugate profiles exist for any tooth.** For a given profile on gear 1, the relative velocity at $K$ is $(\omega_2 - \omega_1) J(K - P)$, so the condition $n \cdot (v_2 - v_1) = 0$ is the same as $K - P$ parallel to $n$. Solving this equation of meshing at each position of gear 1 gives the conjugate profile on gear 2. [Gear generation by enveloping](/gear-generation-by-enveloping/) does this, and Litvin and Fuentes treat it in Chapter 6.
- **Internal gears and racks.** For an internal gear $P$ lies outside the segment $O_1O_2$, and the gears turn in the same direction. For a rack, $O_2$ goes to infinity, the pitch circle of the rack becomes the pitch line, and the rack moves at the speed $\omega_1 r_1$.
- **Variable ratios.** If $P$ moves, the ratio changes. Non-circular gears use this on purpose: their pitch curves are the centrodes of the relative motion. A cam and its follower are the same pair of bodies with a moving $P$, and the same point gives the follower speed on the [cam pressure angle](/cam-pressure-angle/) page.

## Tightness

**The ratio is set only by $P$.** The proof uses no other property of the profiles. So any two profiles whose common normals all pass through the same fixed point are conjugate, and the involute and the cycloidal tooth forms are two of many. Litvin and Fuentes treat cycloidal gearing in Chapter 13.

**A tooth that is not conjugate.** Let gear 2 carry a thin pin, taken as a point $Q$ at the distance $40$ mm from $O_2$, and let gear 1 push it with a straight flank through $O_1$, with $c = 100$ mm. The contact is at $Q$, so the flank is the line $O_1Q$, and the normal is the line through $Q$ square to $O_1Q$. It crosses the axis where $pQ_x = |Q|^2$. With the pin at the angle $\psi$ from the line of centers, $Q = (100 + 40\cos\psi, 40\sin\psi)$. At $\psi = 180°$, $Q = (60, 0)$, $p = 60$ and $\omega_2/\omega_1 = 60/(60 - 100) = -1.5$. At $\psi = 150°$, $Q = (65.36, 20)$, $p = 4672.0/65.36 = 71.48$ and $\omega_2/\omega_1 = 71.48/(71.48 - 100) = -2.51$. The pitch point moves, and the ratio changes by two thirds within $30°$ of pin travel.

**The normal along the line of centers.** If $n$ is along the line of centers, then $u \times n = 0$ and Step 3 gives no information. The contact force then passes through both centers, so it gives no torque, and the contact does not fix the ratio at that instant. Conjugate teeth avoid this position.

**Corners.** The law needs a common normal. At a sharp tip corner of a tooth there is no unique normal, and the contact of a corner with a flank does not keep the ratio. This happens when the teeth interfere, which is the subject of [gear undercutting](/gear-undercutting/).

**Kinematics only.** The law says nothing about how long a pair of teeth stays in contact. A constant ratio through the whole turn also needs the next pair to touch before the last pair leaves, which is the condition on the [contact ratio](/gear-contact-ratio/). Real gears also deflect under load and have errors of shape, so their ratio varies a little even with conjugate teeth. This variation is the transmission error.

## History

Textbooks credit the French mathematician Charles-Étienne-Louis Camus with the first statement of the condition, in a memoir of 1733, and Leonhard Euler with the study of involute teeth in the middle of the eighteenth century. Historians of gearing do not fully agree on how complete the statement of Camus was. Robert Willis gave the theory of rolling contact and of tooth profiles in his Principles of Mechanism (1841), and his name stays attached to the analysis of gear trains through the [Willis formula](/willis-formula/). Litvin's NASA report of 1998 surveys the history and the people who built the theory of gearing.

## References
