---
tag: X68YYQ
kind: technique
slug: gear-generation-by-enveloping
name: Gear tooth generation by enveloping
aliases:
- Litvin theory of gearing
- generating method for gear teeth
- equation of meshing
area: cad/mechanism-and-assembly-design
level: advanced
summary: Computes a tooth surface as the envelope of a rack or hob cutter in relative motion by the equation of meshing, the basis of Litvin's theory of gearing.
prereqs: [involute-gear-tooth, instant-center-of-velocity]
see_also: [fundamental-law-of-gearing, gear-undercutting, gear-contact-ratio, cam-profile-synthesis, swept-volume, bisection-method, newton-raphson-method, offset-curve]
sources:
  - book: isbn:9780521815178
    title: Faydor L. Litvin and Alfonso Fuentes, Gear Geometry and Applied Theory, 2nd edition, Cambridge University Press, 2004
    locator: Chapter 1 (coordinate transformation), Chapter 2 (relative velocity), Chapter 6 (conjugated surfaces and curves, the envelope and the equation of meshing) and Chapter 10 (spur involute gears, generation by a rack cutter)
  - paper: "Faydor L. Litvin, Development of Gear Technology and Theory of Gearing, NASA Reference Publication 1406, ARL-TR-1500, 1998"
    title: Development of Gear Technology and Theory of Gearing
    locator: the history of the theory of gearing, with Olivier (1842) and Gochman (1886)
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 9.2 (p. 493, the involute) and Section 9.4 (p. 500, interference and undercutting)
  - book: isbn:9780073398204
    title: Richard G. Budynas and J. Keith Nisbett, Shigley's Mechanical Engineering Design, 10th edition, McGraw-Hill
    locator: Section 13-7, interference and the smallest pinion cut by a rack
---

Gear tooth generation by enveloping finds the shape that a cutting tool leaves on a gear blank. The tool, a rack cutter (a straight bar of teeth), a pinion cutter or a hob (a cutter in the form of a worm), moves relative to the blank in a fixed generating motion. The cut tooth is the envelope of the tool positions: the curve that touches every position of the tool edge. The points of the envelope are the solutions of one scalar equation, the equation of meshing $\mathbf n \cdot \mathbf v = 0$, which says that the tool point slides along the tool edge relative to the gear and does not cross it.

This page works in the plane, which is the transverse section of a spur gear. The gear frame turns with the gear blank, and $\psi$ is the angle of the blank. A tool point $\mathbf r_c(u)$ with unit normal $\mathbf n_c(u)$ in the tool frame is at $F(u, \psi) = R(a(\psi))\,\mathbf r_c(u) + \mathbf t(\psi)$ in the gear frame, where $R(a)$ turns a vector by the angle $a$ and $J = R(90°)$. The equation of meshing is

$$f(u, \psi) = \big(R(a)\,\mathbf n_c(u)\big) \cdot \big(a'(\psi)\,J R(a)\,\mathbf r_c(u) + \mathbf t'(\psi)\big) = 0,$$

where the second factor is $F_\psi$, the velocity of the tool point relative to the gear per unit turn of the gear.

## In plain words

Think of a gear blank as soft clay, and push a hard rack tooth through it while you turn the clay. At each moment the rack tooth scrapes away the clay that it covers. When the motion is over, the edge that is left is the tooth of the gear. Each point of that edge was touched by the rack at one moment, and at that moment the rack slid along the edge without biting into it.

The method turns this picture into an equation. For each point on the edge of the tool, you ask at which moment it moves only along its own edge, as seen from the clay. At that moment the point is on the finished tooth. A straight rack edge that rolls on a circle gives the involute, so one straight tool cuts gears with any number of teeth.

## When it applies

- The gear is cut by a generating process: a rack cutter (gear planing), a pinion cutter (gear shaping) or a hob (gear hobbing). In each one the tool and the blank turn and slide together as if they were a pair of gears in mesh. Form cutting, where a milling cutter has the shape of the tooth space, is not a generating process, and the tooth is a copy of the cutter.
- The tool edge is a smooth curve with a known normal, and the motion is smooth in $\psi$. A corner of the tool, such as the tip of a rack tooth, is a separate tool curve and has its own envelope.
- You want the tooth as a curve, with exact points, normals and the parameter of the tool point that made each point. If only an approximate shape is needed, a simulated cut that subtracts many tool positions from the blank also works, as a [swept volume](/swept-volume/), but it gives no equation and its error falls only as the square of the step.
- In space the same equation holds for a tool surface $\mathbf r_c(u, \theta)$, with one more parameter. This is how helical, bevel and worm gears are computed. This page treats the plane.

## The template

The holes are the tool curve, the generating motion, the root solver and the branch check. The block below takes a list $U$ of tool parameters and a window $[\psi_{lo}, \psi_{hi}]$ of turns of the blank, and returns the points of the cut tooth.

```pseudo id=main
ENVELOPE(r_c, n_c, a, t, U, ψ_lo, ψ_hi, K, KEEP)
L1  for each u in U                                                 ▷ hole 1: the tool r_c(u), n_c(u)
L2      f(ψ) ← (R(a(ψ)) n_c(u)) · (a′(ψ) J R(a(ψ)) r_c(u) + t′(ψ))   ▷ hole 2: the motion a, t
L3      for each of the K cells of [ψ_lo, ψ_hi] where f changes sign
L4          ψ* ← the root of f in the cell, by bisection             ▷ hole 3: the root solver
L5          p ← R(a(ψ*)) r_c(u) + t(ψ*)
L6          if KEEP(u, ψ*, p) then output (u, ψ*, p)                  ▷ hole 4: the branch check
```

**Hole 1, the tool.** A rack cutter flank through the pitch point of the rack, at the pressure angle $\varphi$ to the normal of the pitch line, is

$$\mathbf r_c(u) = u(\sin\varphi, \cos\varphi), \qquad \mathbf n_c = (\cos\varphi, -\sin\varphi).$$

Here the pitch line of the rack is the $x$ axis of the rack frame, and $u \cos\varphi$ is the height of the point above it. The straight flank reaches the height $-km$ toward the blank, where $m$ is the module and $k = 1$ for full depth teeth. The tip of the cutter, which goes $0.25m$ deeper, is a separate curve and cuts the root fillet. A pinion cutter of pitch radius $r_c$ has an involute flank with the base radius $r_c\cos\varphi$, placed so that it has the same point and normal as the rack flank at the pitch point.

**Hole 2, the motion.** Put the center of the blank at the origin of the fixed frame. A blank with $z$ teeth has the pitch radius $r = mz/2$. For a rack, the pitch line of the rack is the line $y = r$, tangent to the pitch circle at the pitch point $P = (0, r)$, and it rolls on the pitch circle without slip. So when the blank turns by $\psi$, the rack moves by $-r\psi$ along $x$. Carried into the gear frame, which turns by $-\psi$ relative to the fixed frame,

$$a(\psi) = -\psi, \qquad \mathbf t(\psi) = R(-\psi)\,(-r\psi,\ r).$$

For a pinion cutter with center $(0, r + r_c)$, the pitch circles roll on each other, so the cutter turns by $-(r/r_c)\psi$, and $a(\psi) = -(1 + r/r_c)\psi$ and $\mathbf t(\psi) = R(-\psi)(0, r + r_c)$.

**Hole 3, the root solver.** For each $u$, line L3 samples $f$ on $K$ cells and line L4 halves each cell with a sign change until it is shorter than the tolerance, as in the [bisection method](/bisection-method/). [Newton's method](/newton-raphson-method/) needs fewer steps when a good start is known, for example the root at the last $u$. For a rack the root has a closed form, derived below.

**Hole 4, the branch check.** Every root is a point of the envelope, but not every point of the envelope is on the cut tooth. The tool may remove the point at some other position. The check in line L6 tests the point against the tool at the other positions near $\psi^*$: for the rack, it computes the smallest signed distance from $p$ to the tooth of the rack, which is the region behind the flank and above the tip line, over a range of turns. A negative value means that the rack covers $p$ at some turn, so $p$ is cut away.

### Why the roots are the points of the envelope

Write $F_u$ and $F_\psi$ for the partial derivatives of $F(u, \psi)$. The vector $F_u = R(a)\,\mathbf r_c'(u)$ is tangent to the tool edge at its position $\psi$, and $\mathbf n = R(a)\,\mathbf n_c(u)$ is normal to it, so $\mathbf n \cdot F_u = 0$ and $f = \mathbf n \cdot F_\psi$.

1. *Every point of an envelope solves the equation.* Let $\Gamma(\psi) = F(u(\psi), \psi)$ be a curve that touches the tool edge at its position $\psi$ for every $\psi$ in an interval, with $u(\psi)$ differentiable. Then $\Gamma' = F_u u' + F_\psi$. Since $\Gamma$ touches the tool edge there, $\Gamma'$ is parallel to $F_u$, so $\mathbf n \cdot \Gamma' = 0$. This gives $0 = (\mathbf n \cdot F_u)\,u' + \mathbf n \cdot F_\psi = f(u(\psi), \psi)$.
2. *Every regular branch of solutions is an envelope.* Let $f(u_0, \psi_0) = 0$ with $f_u(u_0, \psi_0) \ne 0$. By the implicit function theorem there is a differentiable $u(\psi)$ near $\psi_0$ with $f(u(\psi), \psi) = 0$. Put $\Gamma(\psi) = F(u(\psi), \psi)$. Then $\mathbf n \cdot \Gamma' = (\mathbf n \cdot F_u)\,u' + f = 0$, so $\Gamma'$ is parallel to the tool edge, and $\Gamma$ touches the tool at each of its points where $\Gamma' \ne 0$.
3. *The equation is the fundamental law of gearing.* The motion of the tool relative to the gear is, at each instant with $a' \ne 0$, a turn about the instant center $I$ of the two frames, so $F_\psi = a'\,J(p - I)$ and $f = a'\,\mathbf n \cdot J(p - I)$. This is zero exactly when $p - I$ is parallel to $\mathbf n$: the normal of the tool at the contact point passes through $I$. When the pitch curves of the tool and the blank roll without slip, $I$ is their point of contact, the pitch point, by the theory of the [instant center of velocity](/instant-center-of-velocity/). So the cut gear and the tool satisfy the [fundamental law of gearing](/fundamental-law-of-gearing/): they are conjugate, and the gear meshes with any gear that the same tool would cut. $\blacksquare$

At a point where $\Gamma' = 0$ the envelope has a cusp. Litvin and Fuentes (Chapter 6) treat these singular points of the generated curve, and in gear cutting they mark the start of undercutting.

### Why a rack cuts an involute

Take the rack of holes 1 and 2. In the fixed frame the flank at the turn $\psi$ is the line through $(-r\psi, r) + u(\sin\varphi, \cos\varphi)$ with the normal $(\cos\varphi, -\sin\varphi)$. By step 3 the contact point $C$ is where the normal passes through $P = (0, r)$. The normal line through the flank point meets the line $y = r$ at $x = -r\psi + u/\sin\varphi$, so

$$\psi^* = \frac{u}{r\sin\varphi}, \qquad C = P + \frac{u\cos\varphi}{\sin\varphi}\,(-\cos\varphi,\ \sin\varphi).$$

So all contacts lie on one fixed line $\ell$ through $P$ in the direction $(-\cos\varphi, \sin\varphi)$, which is the line of action. The distance from the center $O$ to $\ell$ is $r\cos\varphi = r_b$, so $\ell$ touches the base circle of radius $r_b$ at the point $T = r_b(\sin\varphi, \cos\varphi)$, at the distance $r\sin\varphi$ from $P$. Measured from $T$, the contact is at

$$|TC| = r\sin\varphi + \frac{u\cos\varphi}{\sin\varphi} = r\sin\varphi + \psi^* r\cos\varphi = r_b(\tan\varphi + \psi^*).$$

Now look from the gear frame, which has turned by $-\psi^*$. There $\ell$ is still tangent to the base circle, at the point $R(-\psi^*)T$ with polar angle $\tfrac{\pi}{2} - \varphi - \psi^*$, and $C$ is at the distance $r_b(\tan\varphi + \psi^*)$ from it along the tangent. This is the end of a taut string that is wound on the base circle and unwound from the polar angle $\theta_0 = \tfrac{\pi}{2} - \varphi + \tan\varphi = \tfrac{\pi}{2} + \operatorname{inv}\varphi$, since the free length equals $r_b$ times the angle unwound. So $C$ traces the involute of the base circle with the roll angle $t = \tan\varphi + \psi^*$, and in polar form $\theta + \operatorname{inv}\alpha = \theta_0$ with $\cos\alpha = r_b/\rho$, as on the page on the [involute gear tooth](/involute-gear-tooth/). The base radius $r\cos\varphi$ depends only on the pitch radius and the angle of the rack, so one rack cuts correct involute gears of every size. $\blacksquare$

The argument needs $|TC| \ge 0$, that is $\psi^* \ge -\tan\varphi$, or a flank height $u\cos\varphi \ge -r\sin^2\varphi$. A lower point of the flank makes a contact past $T$, on the other branch of the envelope behind the cusp at the base circle, and hole 4 finds that the rack cuts into the involute there. The rack tip at the height $-km$ stays above this limit if and only if $km \le r\sin^2\varphi$, which is the bound $z \ge 2k/\sin^2\varphi$ of [gear undercutting](/gear-undercutting/).

### Cost

One evaluation of $f$ is a fixed number of operations. For each $u$, lines L3 and L4 take $K$ evaluations for the scan and $\log_2\!\big((\psi_{hi} - \psi_{lo})/(K\varepsilon)\big)$ for each root at the tolerance $\varepsilon$, so $|U|$ points cost $O\big(|U|(K + \log(1/\varepsilon))\big)$ evaluations, plus the branch checks. With the closed form for the rack, each point costs $O(1)$. A simulated cut with $M$ positions of the tool costs $O(|U|M)$ and has an error of order $(\Delta\psi)^2$ in the normal direction.

## Classic examples

**A rack cutting a 20 tooth gear.** Take $m = 4$ mm, $z = 20$ and $\varphi = 20°$, so $r = 40$ mm, $r_b = 37.588$ mm and $\theta_0 = 90.854°$. The table gives five points of one flank, by the height $h = u\cos\varphi$ of the rack point above the pitch line.

| $h$ (mm) | $\psi^*$ (rad) | roll $t$ | $\rho$ (mm) | $\theta$ |
| --- | --- | --- | --- | --- |
| $-4$ | $-0.311145$ | $0.052825$ | $37.640$ | $90.851°$ |
| $-2$ | $-0.155572$ | $0.208398$ | $38.395$ | $90.686°$ |
| $0$ | $0$ | $0.363970$ | $40.000$ | $90.000°$ |
| $2$ | $0.155572$ | $0.519543$ | $42.358$ | $88.540°$ |
| $4$ | $0.311145$ | $0.675115$ | $45.352$ | $86.197°$ |

Each point has $\theta + \operatorname{inv}\alpha = 90.854° = \theta_0$, so they lie on one involute. The rack tip at $h = -4$ mm cuts the lowest flank point at $\rho = 37.640$ mm, just $0.052$ mm above the base circle, and the limit height $r\sin^2\varphi = 4.679$ mm is above $km = 4$ mm, so there is no undercut. The tip circle of the gear, $\rho = 44$ mm, is reached at $h = 3.144$ mm.

**A pinion cutter cuts the same flank.** A pinion cutter with $12$ teeth of the same module has $r_c = 24$ mm. With the closed form root $\psi^* = -(r_c/r)(t_c - \tan\varphi)$, where $t_c$ is the roll angle of the cutter flank, the cutter points at $t_c = \tan\varphi \mp 0.2$ give $\psi^* = \pm 0.12$ and the gear points at $\rho = 41.758$ and $38.690$ mm, both with $\theta + \operatorname{inv}\alpha = 90.854°$. This is the conjugacy of step 3: the cutter is an involute gear, and any gear that meshes with it on the same base pitch has the same involute flank.

**Undercut of a 12 tooth gear.** With $z = 12$ and the same rack, $r = 24$ mm and $r\sin^2\varphi = 2.807$ mm, which is less than $4$ mm. The rack tip makes its root at $\psi^* = -0.5186$, behind the cusp, and the branch check finds that the rack covers this point by $0.055$ mm at a nearby turn. A simulated cut with dense positions of the rack confirms that near $\rho = 22.6$ mm the cut flank lies $3.7 \times 10^{-5}$ rad inside the involute, and that at $\rho = 23$ mm and above it agrees with the involute.

**A cam with a roller follower.** The profile of a cam with a roller follower is the envelope of the roller circle as the follower moves around the cam, in the frame of the cam. The tool is a circle and the motion is the inverted motion of the follower, and the envelope is an [offset curve](/offset-curve/) of the pitch curve. [Cam profile synthesis](/cam-profile-synthesis/) computes it this way.

## Variations

- **Profile shift.** Move the pitch line of the rack away from the center by $xm$, so that the rack translates on the line $y = r + xm$ but still moves by $r\psi$. The rolling line of the rack stays at $y = r$, so the base circle stays $r\cos\varphi$, and only the place of the involute on it changes. The tooth on the pitch circle becomes thicker by $2xm\tan\varphi$, and the undercut limit becomes $(k - x)m \le r\sin^2\varphi$.
- **Hobbing.** A hob is a worm with gashes that make cutting edges. In the transverse section of a spur gear its threads look like a rack that moves along its pitch line while the hob turns, so the cut flank is the rack envelope above. The hob cuts all teeth in one continuous motion, with no stop to index from one tooth to the next.
- **Surfaces in space.** For a tool surface $\mathbf r_c(u, \theta)$ the envelope is the set of points with $\mathbf n(u, \theta) \cdot \mathbf v(u, \theta, \psi) = 0$, one equation in three parameters, so it is a surface. Litvin and Fuentes write the motion as a product of $4 \times 4$ matrices (Chapter 1) and the relative velocity from it (Chapter 2), and they compute helical, bevel, worm and face gears in this way.
- **Kinematic form.** Step 3 replaces the equation of meshing by a geometric test: the normal of the tool at the point passes through the pitch point. This avoids derivatives of the motion and is the classical way to construct conjugate profiles by hand.
- **Simulated cutting.** Subtract the tool region at many positions from the blank, and read the boundary. This is the brute force check of the method, and the right tool when the tool has many corners and edges, as in a [swept volume](/swept-volume/) computation.

## Pitfalls

- **Extra roots.** The equation of meshing has other roots than the cut point. For a pinion cutter, the normal of a cutter point passes through the pitch point at two turns of the cutter, once for each tangent from the pitch point to the cutter base circle. For the 12 tooth cutter above at $t_c = \tan\varphi - 0.2$, a window of $[-0.3, 0.3]$ gives the true root $\psi^* = 0.12$ and a second root at $\psi = -0.2989$, whose point is not on the involute. Use a window around the expected contact, or the branch check.
- **The cusp is not material.** Past the base circle the envelope turns back on a second branch. These points solve the equation, but the tool removes them, and taking them as the tooth gives a profile that crosses itself.
- **The tool tip is a separate curve.** The flank of the rack is straight only up to the height $km$. The rounded tip below it cuts the root fillet, which is the envelope of the tip circle, a trochoid. Using the flank formula below $km$ is wrong.
- **The rolling radius fixes the number of teeth.** The rack must move by $r\psi$ with $r = mz/2$. A different rolling radius still gives an involute, but its base pitch no longer fits $z$ teeth around the gear.
- **Errors in the derivatives.** A wrong sign in $a'$ or $\mathbf t'$ moves every root and still gives a smooth curve. Check $f$ against a central difference of $F$ in $\psi$, as the tests of this page do.

## Exercises

1. Show directly from $f(u, \psi) = 0$ for the rack of hole 2 that $\psi^* = u/(r\sin\varphi)$, without the instant center.
2. Keep the module and let the number of teeth of a pinion cutter grow without bound. Show that its flank near the pitch point tends to the straight flank of the rack, and that the motion of hole 2 for the cutter tends to the motion for the rack.
3. Show that the cusp of the rack envelope is at $\rho = r_b$, and find the flank height $u\cos\varphi$ that cuts it.
4. Find the smallest profile shift $x$ that lets a rack with $k = 1$ and $\varphi = 20°$ cut $12$ teeth without undercut.
5. A tool is a circle of radius $R_f$ whose center moves on a curve $c(s)$ without turning. Write the equation of meshing and show that the envelope is the pair of offset curves at the distance $R_f$.

## References
