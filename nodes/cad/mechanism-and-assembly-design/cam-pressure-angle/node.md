---
tag: WQKE8D
kind: definition
slug: cam-pressure-angle
name: Pressure angle of a cam
aliases:
- cam pressure angle
- pressure angle of a translating roller follower
area: cad/mechanism-and-assembly-design
level: intro
summary: The angle between the follower motion and the common normal at contact, kept below about 30 degrees, which sets the base circle size of a cam.
prereqs: [cam-follower-motion-laws]
see_also: [cam-profile-synthesis, transmission-angle, aronhold-kennedy-theorem, instant-center-of-velocity, involute-gear-tooth, fundamental-law-of-gearing]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 8.6 (p. 460, sizing the cam, with the pressure angle of translating roller followers on p. 461, choosing a prime circle radius on p. 464 and the overturning moment of flat-faced followers on p. 465)
  - book: isbn:9780831133672
    title: Robert L. Norton, Cam Design and Manufacturing Handbook, 2nd edition, Industrial Press, 2009
    locator: the chapter on cam size and pressure angle, with the guideline of about 30 degrees for translating and 35 degrees for oscillating roller followers (general locator)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on cam design, the sections on the pressure angle and the size of the cam (general locator)
---

The pressure angle of a cam is the angle, at the point of contact, between the common normal of the cam and the follower and the direction in which the follower moves. A cam is a shaped plate on a turning shaft, and the follower is the part that rides on its edge. Without friction the cam can push the follower only along the common normal. The part of the push along the motion does the work, and the part across the motion only presses the follower into its guide. So a small pressure angle means a good force path, and a large one means a large side load and, at worst, a follower that jams in its guide. The angle changes as the cam turns, and its peak decides how large the cam must be.

## Definition

Take a disk cam that turns about the origin $O$, and a translating roller follower: a slide that moves along a fixed line and carries a roller of radius $R_f$. The line of motion is at the offset $\varepsilon$ from $O$. The base circle is the smallest circle about $O$ that touches the cam, with the radius $R_b$. The prime circle, with the radius $R_p = R_b + R_f$, is the circle through the roller center when the lift is zero. The lift is $s(\theta)$ at the cam angle $\theta$, and $s' = ds/d\theta$.

Put the fixed frame with $O$ at the origin and the follower moving along the line $x = \varepsilon$ in the direction $+y$, and let the cam turn counterclockwise. The roller center is at $(\varepsilon, d_0 + s)$ with $d_0 = \sqrt{R_p^2 - \varepsilon^2}$. The **pressure angle** $\varphi$ is the signed angle from the direction of motion $(0, 1)$ to the common normal at the contact. It satisfies

$$\tan\varphi = \frac{s' - \varepsilon}{s + \sqrt{R_p^2 - \varepsilon^2}}.$$

For a radial follower, $\varepsilon = 0$ and $\tan\varphi = s'/(R_p + s)$. In a dwell $s' = 0$, so $\varphi = 0$ for a radial follower and $\tan\varphi = -\varepsilon/(d_0 + s)$ for an offset one. Many texts quote only $|\varphi|$. The sign of a helpful offset depends on the direction in which the cam turns: with the conventions here a positive $\varepsilon$ lowers $\varphi$ on the rise, and for a cam that turns clockwise the sign flips.

### The formula

**Claim.** With the conventions above, the common normal at the contact passes through the roller center $(\varepsilon, d_0 + s)$ and through the point $(s', 0)$ on the line through $O$ square to the motion. So $\tan\varphi = (s' - \varepsilon)/(d_0 + s)$.

*Proof by instant centers.* Call the ground 1, the cam 2 and the follower 3. The center $P_{12}$ is the cam pivot $O$. The follower slides on the ground, so $P_{13}$ is the point at infinity in the direction square to the slide, that is along the $x$ axis. By the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/), $P_{23}$ is on the line through $P_{12}$ and $P_{13}$, which is the $x$ axis. The cam and the follower touch with no gap and no overlap, so their relative velocity at the contact has no part along the common normal, and $P_{23}$ is also on that normal. A roller is a circle, so the normal passes through its center. At $P_{23} = (x_I, 0)$ the cam and the follower have the same velocity. The cam point there has the velocity $\omega J(x_I, 0) = (0, \omega x_I)$, where $J$ is the rotation by $90°$. The follower point has the velocity $(0, \omega s')$, because the follower translates with $ds/dt = \omega s'$. So $x_I = s'$. The normal runs from $(s', 0)$ to $(\varepsilon, d_0 + s)$, so it rises by $d_0 + s$ and moves sideways by $\varepsilon - s'$, and the angle it makes with the $y$ axis has the tangent $(s' - \varepsilon)/(d_0 + s)$. $\blacksquare$

*Second proof by inversion.* In the frame of the cam, the roller center traces the pitch curve $C(\theta) = R(-\theta)(\varepsilon, d_0 + s)$, whose derivative is $R(-\theta)(d_0 + s, s' - \varepsilon)$, as on the [cam profile synthesis](/cam-profile-synthesis/) page. Turned back to the fixed frame, the tangent at the contact is $(d_0 + s, s' - \varepsilon)$, and the normal is square to it. The angle of the tangent from the $x$ axis equals the angle of the normal from the $y$ axis, which gives the same formula. $\square$

The first proof shows the geometry: the follower velocity per unit cam speed, $s'$, is the distance from $O$ to the point where the normal crosses the line square to the motion. A large $s'$ pushes that point far out and tilts the normal.

### Forces

Let the cam push with the force $F$ along the normal and ignore friction. The follower gets $F\cos\varphi$ along its motion and $F\sin\varphi$ across it. The cross part is carried by the guide. The ratio of side load to useful load is $\tan\varphi$, which is $0.577$ at $30°$ and $1$ at $45°$. The side load causes friction in the guide that grows with it, and if the friction force reaches the useful force the follower jams.

### A rule of thumb, not a theorem

Norton recommends keeping $|\varphi|$ below about $30°$ for translating roller followers and below about $35°$ for oscillating roller followers. These are guidelines from practice. The real limit depends on the friction and the length of the guide, on the overhang of the roller from the guide and on the spring force. No proof shows that a cam with a peak of $31°$ fails or that one with $29°$ works.

## Examples and non-examples

**Sizing a cam.** Take a radial roller follower and a rise of $L = 20$ mm over $\beta = 90°$. The peak of $\varphi$ over the rise comes near the middle of the rise, where $s'$ is largest, and it falls as $R_p$ grows. The smallest prime circle that keeps $\varphi \le 30°$ is:

| law | peak $s'$ (mm/rad) | $R_p$ for a $30°$ peak | peak $\varphi$ at $R_p = 50$ mm |
| --- | --- | --- | --- |
| simple harmonic | $20.00$ | 26.06 mm | $18.68°$ |
| 3-4-5 polynomial | $23.87$ | 32.40 mm | $21.94°$ |
| cycloidal | $25.46$ | 35.02 mm | $23.23°$ |

The order follows the peak velocity coefficient $C_v$ of the laws on the [cam follower motion laws](/cam-follower-motion-laws/) page, $\pi/2$, $1.875$ and $2$. A smoother law needs a larger cam for the same pressure angle.

**A point checked by hand.** For the cycloidal rise with $R_p = 50$ mm and $\varepsilon = 0$, at the middle of the rise $s = 10$ mm and $s' = 2L/\beta = 80/\pi = 25.46$ mm per radian. So $\tan\varphi = 25.46/60$ and $\varphi = 23.00°$. The peak $23.23°$ is a little earlier, at $x = 0.466$ of the rise, where $s$ is smaller.

**An offset.** With $\varepsilon = 5$ mm, the same cycloidal rise has the peak $19.07°$, but a cycloidal return over $90°$ has the peak $-27.34°$, against $\pm 23.23°$ with no offset. An offset trades the angle of one stroke against the other. It helps when the rise carries the load and the return is driven only by the spring.

**The force on the guide.** At $\varphi = 23°$, a normal force of $500$ N gives $460.3$ N along the motion and $195.4$ N on the guide.

**Non-example: a flat-faced follower.** If the face is square to the line of motion, the normal at the contact is always along the motion, so $\varphi = 0$ at every angle. The cost moves elsewhere: the contact moves along the face by $s'$, so the force has the lever arm $s'$ about the axis and gives an overturning moment on the follower stem. Norton treats this moment in place of the pressure angle.

**Non-example: the angle at a gear tooth.** The pressure angle of a gear is the angle between the line of action and the common tangent of the pitch circles. For an [involute gear tooth](/involute-gear-tooth/) it is a constant of the gear pair, set by the tool, and it does not vary with the position. The cam pressure angle varies with every degree of cam turn.

## Related definitions

- [Cam follower motion laws](/cam-follower-motion-laws/): the laws that give $s'$, and so the peak of the pressure angle.
- [Cam profile synthesis](/cam-profile-synthesis/): computes the pressure angle at each angle along with the profile, and the radius of curvature, the other check on the size of the cam.
- [Transmission angle](/transmission-angle/): the same measure for a [four-bar linkage](/four-bar-linkage/). The pressure angle at the output pin is $|90° - \mu|$.
- [Instant center of velocity](/instant-center-of-velocity/) and the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/): the tools of the first proof.
- [Fundamental law of gearing](/fundamental-law-of-gearing/): the same instant center on the line of centers, used for gear teeth.

## References
