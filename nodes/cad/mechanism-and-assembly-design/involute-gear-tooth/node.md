---
tag: ZTP1JX
kind: definition
slug: involute-gear-tooth
name: Involute gear tooth profile
aliases:
- involute tooth profile
- involute of a circle
- involute function
area: cad/mechanism-and-assembly-design
level: intro
summary: A tooth flank shaped as the involute of the base circle, which obeys the law of gearing and keeps the speed ratio when the center distance changes.
prereqs: [fundamental-law-of-gearing]
see_also: [gear-contact-ratio, gear-undercutting, gear-generation-by-enveloping, cam-pressure-angle, frenet-frame, arc-length-parametrization]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 9.2 (p. 492, with the involute tooth form on p. 493, the pressure angle on p. 495, changing center distance on p. 495 and backlash on p. 497) and Section 9.3 (p. 497, gear tooth nomenclature)
  - book: isbn:9780073398204
    title: Richard G. Budynas and J. Keith Nisbett, Shigley's Mechanical Engineering Design, 10th edition, McGraw-Hill
    locator: Section 13-4, involute properties
  - book: isbn:9780521815178
    title: Faydor L. Litvin and Alfonso Fuentes, Gear Geometry and Applied Theory, 2nd edition, Cambridge University Press, 2004
    locator: Chapter 4 (planar curves) and Chapter 10 (spur involute gears)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on spur gears, the involute properties and the involutometry (general locator)
---

The involute gear tooth has flanks that are involutes of a circle, the base circle. The involute is the curve traced by the end of a taut string as it is unwound from a fixed circle. Almost all gears for power transmission use this shape. It meets the [fundamental law of gearing](/fundamental-law-of-gearing/), and it has a property that no other common tooth form has: two involute gears keep exactly the same speed ratio when the distance between their shafts changes. So small errors of mounting, wear of the bearings and heat do not spoil the motion. They change only the play between the teeth and the angle of the push.

## Definition

**The involute of a circle.** Let the base circle have the center $O$ and the radius $r_b$. The involute that starts at $(r_b, 0)$ is

$$I(t) = r_b\,(\cos t + t\sin t,\ \sin t - t\cos t), \qquad t \ge 0.$$

The parameter $t$ is the roll angle. The string leaves the circle at the tangent point $T(t) = r_b(\cos t, \sin t)$, and the free part of the string, from $T(t)$ to $I(t)$, has the length $r_b t$, which is the arc of the circle that has been unwound. So $I(t) = T(t) + r_b t\,(\sin t, -\cos t)$, where $(\sin t, -\cos t)$ is the unit tangent of the circle at $T(t)$.

**The involute tooth.** An involute gear has a base circle of radius $r_b$ and $z$ teeth. Each tooth has two flanks, which are mirror images of each other, and each flank is a copy of the involute above, turned about $O$. The pitch circle of the gear has the radius $r = mz/2$, where the module $m$ is the pitch circle diameter per tooth. The pressure angle $\varphi$ is fixed by $r_b = r\cos\varphi$. The usual standard value is $\varphi = 20°$. The involute exists only outside the base circle, so the part of the tooth below the base circle has another shape, the fillet.

**The involute function.** The function

$$\operatorname{inv}\alpha = \tan\alpha - \alpha$$

gives the polar angle of the involute at the radius $r_b/\cos\alpha$.

### Properties

**Claim 1 (the normal is tangent to the base circle).** The tangent of $I$ at $t > 0$ is along $(\cos t, \sin t)$, and the normal line of $I$ at $I(t)$ is the tangent line of the base circle at $T(t)$. The radius of curvature of $I$ at $t$ is $r_b t$, with the center of curvature at $T(t)$.

*Proof.* Differentiate: $I'(t) = r_b(-\sin t + \sin t + t\cos t,\ \cos t - \cos t + t\sin t) = r_b t(\cos t, \sin t)$. The vector $I(t) - T(t) = r_b t(\sin t, -\cos t)$ is square to $I'(t)$, so the normal line at $I(t)$ passes through $T(t)$ and has the direction $(\sin t, -\cos t)$, which is the tangent direction of the circle at $T(t)$. The speed is $|I'| = r_b t$ and the tangent angle is $t$, which turns at the unit rate, so the curvature is $1/(r_b t)$. The normal toward the center of curvature points from $I(t)$ to $T(t)$, at the distance $r_b t$. $\blacksquare$

**Claim 2 (polar form).** At the roll angle $t$, the involute is at the radius $r_b\sqrt{1 + t^2}$ and at the polar angle $t - \arctan t$. Put $t = \tan\alpha$. Then the radius is $r_b/\cos\alpha$ and the polar angle is $\operatorname{inv}\alpha$, and $\alpha$ is the angle between the normal at that point and the tangent of the circle of that radius about $O$.

*Proof.* $|I(t)|^2 = r_b^2\bigl((\cos t + t\sin t)^2 + (\sin t - t\cos t)^2\bigr) = r_b^2(1 + t^2)$. In the right triangle $O\,T(t)\,I(t)$ the leg $OT$ is $r_b$, the leg $TI$ is $r_b t$, and the angle at $O$ is $\arctan t = \alpha$. The point $T(t)$ is at the polar angle $t$, and $I(t)$ lags it by the angle at $O$, so its polar angle is $t - \alpha = \tan\alpha - \alpha$. The radius $OI$ is square to the circle about $O$ through $I$, and the normal $TI$ makes the angle $90° - \alpha$ with $OI$, so it makes the angle $\alpha$ with the tangent of that circle. $\blacksquare$

At the pitch radius, $\alpha = \varphi$. So the pressure angle of an involute gear is the angle between the line of action and the common tangent of the pitch circles, and it is the same at every point of the mesh.

**Claim 3 (tooth thickness).** If a tooth has the thickness $s$ along the pitch circle of radius $r$, then at the radius $r_\alpha = r_b/\cos\alpha$ its thickness along the circle of that radius is

$$s_\alpha = 2 r_\alpha\left(\frac{s}{2r} + \operatorname{inv}\varphi - \operatorname{inv}\alpha\right).$$

*Proof.* Measure polar angles from the center line of the tooth. The flank is at the half angle $s/(2r)$ at the pitch radius. By Claim 2 it moves toward the center line by the polar angle $\operatorname{inv}\alpha - \operatorname{inv}\varphi$ between the pitch radius and the radius $r_\alpha$. The half angle at $r_\alpha$ is $s/(2r) + \operatorname{inv}\varphi - \operatorname{inv}\alpha$, and the arc is $r_\alpha$ times twice this. $\blacksquare$

### Insensitivity to the center distance

**Theorem.** Let two involute gears with base radii $r_{b1}$ and $r_{b2}$ turn about $O_1$ and $O_2$, at a center distance $c > r_{b1} + r_{b2}$, with their flanks in contact. Then the contact moves along a fixed line, a common internal tangent of the two base circles, and the speed ratio is

$$\left|\frac{\omega_2}{\omega_1}\right| = \frac{r_{b1}}{r_{b2}},$$

which does not depend on $c$. The operating pressure angle $\varphi'$ and the operating pitch radii $r_1'$, $r_2'$ satisfy

$$\cos\varphi' = \frac{r_{b1} + r_{b2}}{c}, \qquad r_i' = \frac{r_{bi}}{\cos\varphi'}.$$

*Proof.* At the contact point $K$ the two flanks have a common normal. By Claim 1, the normal of flank 1 at $K$ is tangent to base circle 1, and the normal of flank 2 at $K$ is tangent to base circle 2. So the common normal is a line tangent to both base circles. The flanks of external gears face each other between the centers, so the line separates the two centers, and it is one of the two internal common tangents. The choice of the tangent is fixed by which flanks drive, so the line is the same for every position. Call it $\ell$ and let it touch the base circles at $T_1$ and $T_2$. It crosses the line of centers at a point $P$, and the right triangles $O_1T_1P$ and $O_2T_2P$ are similar, with the equal angles at $P$. So $O_1P/O_2P = r_{b1}/r_{b2}$, and $P$ is a fixed point that divides $O_1O_2$ in the ratio $r_{b1} : r_{b2}$. By the fundamental law of gearing, the speed ratio is $O_1P/O_2P = r_{b1}/r_{b2}$.

The same ratio follows from the string. As gear 1 turns by $d\theta_1$, its involute moves along $\ell$ by $r_{b1}\,d\theta_1$, because the string unwinds from the base circle by that length. Gear 2 must move its flank along $\ell$ by the same length, so $r_{b1}\,d\theta_1 = r_{b2}\,d\theta_2$.

For the pressure angle, $\ell$ makes the angle $\varphi'$ with the line square to $O_1O_2$. Then $O_1T_1 = O_1P\cos\varphi'$ and $O_2T_2 = O_2P\cos\varphi'$, so $r_{b1} + r_{b2} = (O_1P + O_2P)\cos\varphi' = c\cos\varphi'$, and the operating pitch radii are $r_i' = O_iP = r_{bi}/\cos\varphi'$. $\blacksquare$

## Examples and non-examples

**A pair at the standard distance.** Take $m = 4$ mm, $\varphi = 20°$, $z_1 = 20$ and $z_2 = 30$. The pitch radii are $40$ and $60$ mm, so the standard center distance is $c = 100$ mm, and the base radii are $r_{b1} = 40\cos 20° = 37.588$ mm and $r_{b2} = 56.382$ mm. The base pitch, the distance between two flanks along the line of action, is $\pi m\cos\varphi = 11.809$ mm. The involute of gear 1 reaches the pitch circle at the roll angle $t = \tan 20° = 0.36397$, at the polar angle $\operatorname{inv} 20° = 0.014904$ rad, and its radius of curvature there is $r_{b1} t = 13.681$ mm.

**The center distance moved.** The same gears mounted at other center distances:

| $c$ (mm) | $\varphi'$ | $r_1'$ (mm) | $r_2'$ (mm) | $\lvert\omega_2/\omega_1\rvert$ |
| --- | --- | --- | --- | --- |
| 100 | $20.000°$ | 40.0 | 60.0 | $2/3$ |
| 101 | $21.505°$ | 40.4 | 60.6 | $2/3$ |
| 102 | $22.888°$ | 40.8 | 61.2 | $2/3$ |

The ratio stays $2/3$. The operating pressure angle grows, and the teeth have play: at $c = 101$ mm, with standard teeth of thickness $\pi m/2$ on the pitch circle, Claim 3 gives a backlash of $0.762$ mm along the operating pitch circle, close to the estimate $2\,\Delta c\tan\varphi = 0.728$ mm.

**The tooth tip.** With the standard addendum of $1\,m$ (the height of the tooth above the pitch circle), gear 1 has the tip radius $44$ mm. There $\cos\alpha = 37.588/44$, so $\alpha = 31.32°$, and Claim 3 gives the tip thickness $2.780$ mm, against $6.283$ mm on the pitch circle. The two flanks would meet in a point at the radius $46.15$ mm.

**Non-example: cycloidal teeth.** Teeth made of epicycloids and hypocycloids are also conjugate, and clocks use them. But their pitch point is fixed only at the design center distance, so a change of $c$ changes the speed ratio during the mesh.

**Non-example: the flank below the base circle.** The involute does not exist inside the base circle. The fillet there is not conjugate to the mating flank, so contact there breaks the law. On gears with few teeth, the cutting tool removes part of the involute near the base circle, which is [gear undercutting](/gear-undercutting/).

## Related definitions

- [Fundamental law of gearing](/fundamental-law-of-gearing/): the condition that the involute meets, with a pitch point that is fixed for every center distance.
- [Contact ratio](/gear-contact-ratio/): the length of the part of the line $\ell$ where the teeth touch, divided by the base pitch.
- [Gear undercutting](/gear-undercutting/): the limit on the number of teeth that comes from the start of the involute at the base circle.
- [Gear generation by enveloping](/gear-generation-by-enveloping/): a rack with straight flanks, rolled on the pitch circle, cuts the involute as its envelope.
- [Cam pressure angle](/cam-pressure-angle/): the angle with the same name for a cam, which changes with the position.

## References
