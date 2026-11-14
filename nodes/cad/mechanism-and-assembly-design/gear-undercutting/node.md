---
tag: 2EWHB0
kind: concept
slug: gear-undercutting
name: Gear undercutting and interference
aliases:
- involute interference
- minimum number of teeth
area: cad/mechanism-and-assembly-design
level: core
summary: Teeth are cut away at the root when the mating addendum passes the interference point, which sets a minimum tooth count for a pressure angle.
prereqs: [involute-gear-tooth]
see_also: [gear-generation-by-enveloping, gear-contact-ratio, fundamental-law-of-gearing]
sources:
  - book: isbn:9780073398204
    title: Richard G. Budynas and J. Keith Nisbett, Shigley's Mechanical Engineering Design, 10th edition, McGraw-Hill
    locator: Section 13-7, interference, with the smallest pinion for a 1 to 1 pair (Eq. 13-10) and the smallest pinion that runs with a rack (Eq. 13-13), 18 teeth at 20 degrees
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 9.4 (p. 500), interference and undercutting, with unequal-addendum (profile shifted) teeth
  - book: isbn:9780521815178
    title: Faydor L. Litvin and Alfonso Fuentes, Gear Geometry and Applied Theory, 2nd edition, Cambridge University Press, 2004
    locator: Chapter 10, spur involute gears, generation by a rack cutter and avoidance of undercutting (general locator)
---

Interference is contact between the tip of one gear tooth and the part of the mating tooth below its base circle, where the tooth has no involute. The [involute gear tooth](/involute-gear-tooth/) page shows that every involute contact lies on the line of action between the two points $T_1$ and $T_2$ where it touches the base circles. These two points are the interference points. A tip that reaches past one of them meets a flank that is not conjugate, and the gears jam or the speed ratio jumps. Undercutting is the same event during manufacture: when a generating cutter reaches past the interference point of the gear it cuts, it removes the root of the tooth, including a part of the involute.

## In plain words

The working face of an involute tooth starts at a circle near the bottom of the tooth. Below that circle the tooth has a different shape. If a tooth of the mating gear is too long, its tip reaches that lower part, and the two gears push on each other in the wrong way.

When the gear is cut, the cutter acts like a mating gear. If the cutter tooth is too long for the gear, it digs into the bottom of the gear teeth and makes them thin at the root, where they need the most strength. Small gears have the problem first, because their base circle is close to the pitch circle. So each tooth system has a smallest number of teeth that can be cut with no undercut. For the usual 20 degree teeth this number is 18.

## The idea

**The setting.** Let a rack cutter cut a gear with $z$ teeth, module $m$ and pressure angle $\varphi$, so that the pitch radius is $r = mz/2$ and the base radius is $r_b = r\cos\varphi$. The straight flank of the cutter reaches the depth $km$ below its pitch line, toward the gear, where $k$ is the addendum coefficient: $k = 1$ for full depth teeth and $k = 0.8$ for stub teeth. As on the page on [gear generation by enveloping](/gear-generation-by-enveloping/), the pitch line of the rack rolls on the pitch circle, the pitch point is $P$, and the line of action $\ell$ through $P$ touches the base circle at $T$ with $|PT| = r\sin\varphi$.

**Theorem.** The straight flank of the rack cuts away part of the involute if $km > r\sin^2\varphi$. The flank makes all of its contacts on the segment $PT$ if and only if $km \le r\sin^2\varphi$, that is

$$z \ge \frac{2k}{\sin^2\varphi}.$$

*Proof.* Use the fixed frame with $O$ at the origin and $P = (0, r)$, and measure the depth below the pitch line $y = r$. The rack only translates, so each point of the flank keeps its depth. The point $T = r_b(\sin\varphi, \cos\varphi)$ has the height $r\cos^2\varphi$, which is the depth $r - r\cos^2\varphi = r\sin^2\varphi$.

*Contacts.* The flank touches the gear where its normal passes through $P$, by the [fundamental law of gearing](/fundamental-law-of-gearing/), so the contact point lies on $\ell$ and on the flank, at the depth of the flank point that makes it. The depth along $\ell$ grows from $0$ at $P$ to $r\sin^2\varphi$ at $T$. So a flank point at a depth $h \le r\sin^2\varphi$ makes its contact on $PT$, and a point at a depth $h > r\sin^2\varphi$ makes it past $T$. Contacts past $T$ exist exactly when $km > r\sin^2\varphi$.

*Cut.* Let $km > r\sin^2\varphi$, and let $S$ be the start of a flank involute on the base circle. Take the turn $\psi^*$ at which $S$ is at $T$. The rack tooth is the set of points behind the flank line and above the tip line. Let $d(\psi)$ be the signed distance from the turned point $q(\psi) = R(\psi - \psi^*)T$ to the flank line, negative behind it. The flank line moves by $-r\psi$ along $x$ and has the normal $\mathbf n = (\cos\varphi, -\sin\varphi)$, so $d(\psi) = \mathbf n \cdot q(\psi) + r\psi\cos\varphi + c$ for a constant $c$. Differentiate with $q' = Jq$, where $J$ turns a vector by $90°$:

$$d' = \mathbf n \cdot Jq + r\cos\varphi, \qquad d'' = \mathbf n \cdot J^2 q = -\mathbf n \cdot q, \qquad d''' = -\mathbf n \cdot Jq.$$

At $\psi^*$, $q = T$, so $\mathbf n \cdot T = 0$ and $\mathbf n \cdot JT = -r_b$. This gives $d' = 0$, $d'' = 0$ and $d''' = r_b > 0$, and $d(\psi^*) = 0$ since the flank passes through $T$ at the contact. So $d(\psi) < 0$ for $\psi$ a little less than $\psi^*$: the point $S$ is behind the flank. At those turns $S$ is near $T$, at a depth near $r\sin^2\varphi < km$, so it is above the tip line too, and the rack tooth covers $S$. By continuity it also covers the involute points near $S$. $\blacksquare$

With $km \le r\sin^2\varphi$, all contacts of the straight flank are on $PT$, and the flank generates the involute down to the depth $km$. The rounded tip of the cutter, below that depth, cuts the root fillet. That the cutter then removes no part of the involute at any turn is a global claim that this page does not prove. The enveloping page measures it by simulated cutting, with the cutter tooth modeled as the flank and a tip line at the depth $km$.

**Profile shift.** Move the cutter away from the gear center by $xm$, so that its pitch line is at $y = r + xm$ and its flank ends at the depth $(k - x)m$ below the rolling line. The base circle does not change, and the proof gives the condition $(k - x)m \le r\sin^2\varphi$:

$$x \ge k - \frac{z}{2}\sin^2\varphi.$$

The shifted gear has teeth that are thicker at the root and thinner at the tip. Norton calls these unequal-addendum teeth.

**Two gears.** For a pair of gears the condition is the same picture with the mating gear in place of the rack: the tip circle of each gear must cut $\ell$ on the segment $T_1T_2$. With the notation of the [contact ratio](/gear-contact-ratio/) page, gear 2 does not interfere with gear 1 if $\sqrt{r_{a2}^2 - r_{b2}^2} \le c\sin\varphi$. A rack is the worst case, because its tip line reaches deeper along $\ell$ than the tip circle of any gear with the same addendum.

## Examples

**The full depth 20° system.** With $k = 1$ and $\varphi = 20°$, $\sin^2 20° = 0.11698$, so

$$z \ge \frac{2}{0.11698} = 17.097,$$

and the smallest gear that a standard rack cuts without undercut has $18$ teeth, as in Shigley (Eq. 13-13). For $m = 4$ mm:

| $z$ | $r\sin^2\varphi$ (mm) | $km$ (mm) | result |
| --- | --- | --- | --- |
| 12 | 2.807 | 4 | undercut |
| 17 | 3.977 | 4 | slight undercut |
| 18 | 4.211 | 4 | no undercut |
| 20 | 4.679 | 4 | no undercut |

With $17$ teeth, $\tfrac{17}{2}\sin^2 20° = 0.9943$, just below $k = 1$. At $m = 4$ mm the flank reaches $0.023$ mm deeper than $T$, so the undercut is very small, and some tables accept it and give $17$. For $z = 12$ the simulated cut on the enveloping page removes the involute near the base circle: the tip point of the rack is covered by $0.055$ mm, and at the radius $22.6$ mm the cut flank lies $3.7 \times 10^{-5}$ rad inside the involute. These two numbers are measured, not derived.

**Other systems.** The bound $2k/\sin^2\varphi$ for other pressure angles and stub teeth:

| $\varphi$ | $k = 1$ | $k = 0.8$ |
| --- | --- | --- |
| $14.5°$ | $31.9$, so $32$ | $25.5$, so $26$ |
| $20°$ | $17.1$, so $18$ | $13.7$, so $14$ |
| $25°$ | $11.2$, so $12$ | $8.96$, so $9$ |

A larger pressure angle allows fewer teeth, at the cost of a shorter contact.

**Profile shift for 12 teeth.** At $20°$ with $k = 1$, $x \ge 1 - 6 \times 0.11698 = 0.298$. A shift of $0.3m = 1.2$ mm for $m = 4$ mm removes the undercut. For $17$ teeth the needed shift is only $0.0057$.

**Equal gears.** Two equal full depth $20°$ gears need $13$ teeth each. With $12$ teeth and $m = 4$ mm, $\sqrt{r_a^2 - r_b^2} = 16.595$ mm is more than $c\sin\varphi = 16.417$ mm, so the pair interferes. With $13$ teeth, $17.409 < 17.785$ mm and it does not. Shigley (Eq. 13-10) gives the same $13$. A gear that meshes with a 13 tooth pinion still needs $18$ teeth or a profile shift if it is cut by a rack.

**Non-example.** A pair that interferes when cut to standard size can run free of interference if the addendum is cut short, or if the pinion is shifted. Interference depends on the tip circles and the center distance, and undercutting depends on the cutter. A pinion cut with a shift of $x = 0.3$ has no undercut but has a different tip circle, so its contact ratio must be checked again.

## Where it is used

- Gear design: the smallest pinion for a given pressure angle, the choice between a larger pressure angle, stub teeth and profile shift, and the check of every pair against its interference points.
- Gear cutting: the setting of the hob or rack cutter, whose radial offset is the profile shift.
- Gear software: the check that the tip circle of each gear cuts the line of action inside $T_1T_2$, which is also the hypothesis of the [contact ratio](/gear-contact-ratio/) formula.

## References
