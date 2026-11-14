---
tag: G1EQN0
kind: definition
slug: gear-contact-ratio
name: Contact ratio
aliases:
- gear contact ratio
- transverse contact ratio
- profile contact ratio
area: cad/mechanism-and-assembly-design
level: core
summary: The average number of tooth pairs in contact, the length of the line of action over the base pitch, kept above about 1.2 for smooth meshing.
prereqs: [involute-gear-tooth]
see_also: [fundamental-law-of-gearing, gear-undercutting, gear-generation-by-enveloping, willis-formula]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 9.3 (p. 497, nomenclature) and Section 9.5 (p. 502, contact ratio)
  - book: isbn:9780073398204
    title: Richard G. Budynas and J. Keith Nisbett, Shigley's Mechanical Engineering Design, 10th edition, McGraw-Hill
    locator: Section 13-6, contact ratio, with m_c = q_t/p (Eq. 13-8) and the advice not to design gears with contact ratios below about 1.20; Section 13-7 for interference
  - book: isbn:9780521815178
    title: Faydor L. Litvin and Alfonso Fuentes, Gear Geometry and Applied Theory, 2nd edition, Cambridge University Press, 2004
    locator: Chapter 10, spur involute gears (general locator)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapter on spur gears, the contact ratio (general locator)
---

The contact ratio of a pair of gears is the average number of tooth pairs that are in contact at the same time. A pair of teeth touches only for part of a turn, from the moment the tip of one tooth meets the flank of the other until the tip of the other tooth leaves. For the gears to turn without a break in the drive, the next pair must start to touch before the last pair stops, so the contact ratio must be at least 1. For [involute gear teeth](/involute-gear-tooth/) it has a closed form: the length of the path of contact divided by the base pitch.

## Definition

Take two external involute gears with base radii $r_{b1}$, $r_{b2}$, tip radii $r_{a1}$, $r_{a2}$ (the radius of the outer edge of the teeth), $z_1$ and $z_2$ teeth, module $m$ and pressure angle $\varphi$, at the center distance $c$ with the operating pressure angle $\varphi'$, $\cos\varphi' = (r_{b1} + r_{b2})/c$. The line of action $\ell$ is the common internal tangent of the base circles, which touches them at $T_1$ and $T_2$. Every contact of the involute flanks is on $\ell$.

The **base pitch** is the distance between two neighbor flanks of one gear, measured along a common normal:

$$p_b = \frac{2\pi r_{b}}{z} = \pi m \cos\varphi.$$

The two gears have the same base pitch, because $r_{b1}/z_1 = r_{b2}/z_2 = \tfrac12 m\cos\varphi$.

The **length of action** $Z$ is the length of the part of $\ell$ inside both tip circles. The **contact ratio** is

$$m_c = \frac{Z}{p_b}, \qquad Z = \sqrt{r_{a1}^2 - r_{b1}^2} + \sqrt{r_{a2}^2 - r_{b2}^2} - c\sin\varphi'.$$

Shigley writes the same number as $m_c = q_t/p$, the arc of action on the pitch circle over the circular pitch. Both the arc and the pitch are $1/\cos\varphi$ times the lengths along $\ell$, so the ratios agree.

### Why the formula holds

**Claim 1 (the length of action).** Assume that the tip circle of gear 2 cuts $\ell$ between $T_1$ and $T_2$, and so does the tip circle of gear 1. Then contact starts at the point $A$ where the tip circle of the driven gear cuts $\ell$, ends at the point $B$ where the tip circle of the driving gear cuts it, and $|AB| = Z$.

*Proof.* A point of $\ell$ is on a flank of gear $i$ only if it is inside the tip circle of gear $i$, since the teeth end there, and outside the base circle, which holds on the whole segment $T_1T_2$. So the contact points form the part of $\ell$ inside both tip circles. The point of $\ell$ at the distance $d$ from $T_i$ along $\ell$ is at the radius $\sqrt{r_{bi}^2 + d^2}$ from $O_i$, because $O_iT_i$ is square to $\ell$. So the tip circle of gear $i$ cuts $\ell$ at the distance $a_i = \sqrt{r_{ai}^2 - r_{bi}^2}$ from $T_i$. Measure positions along $\ell$ from $T_1$. The tip of gear 1 is at $a_1$, and the tip of gear 2 is at $|T_1T_2| - a_2$. The segment $T_1T_2$ has the length $c\sin\varphi'$, because $T_1T_2 = T_1P + PT_2 = (O_1P + O_2P)\sin\varphi'$, where $P$ is the pitch point. So $Z = a_1 - (c\sin\varphi' - a_2) = a_1 + a_2 - c\sin\varphi'$. $\blacksquare$

**Claim 2 (neighbor flanks are $p_b$ apart on $\ell$).** The flanks of two neighbor teeth of gear $i$ cross $\ell$ at points $p_b$ apart.

*Proof.* Each flank is the involute of the base circle, with its start turned by $2\pi/z_i$ from the last. On $\ell$, which is tangent to the base circle at $T_i$, the involute that starts at the base circle point at the angle $\gamma$ behind $T_i$ crosses at the distance $r_{bi}\gamma$ from $T_i$, which is the length of string unwound. Two flanks whose starts differ by $2\pi/z_i$ cross at distances that differ by $2\pi r_{bi}/z_i = p_b$. $\blacksquare$

**Claim 3 ($m_c$ is the average number of pairs in contact).** If $m_c = k + f$ with an integer $k \ge 0$ and $0 \le f < 1$, then at each moment $k$ or $k + 1$ pairs are in contact, and the share of time with $k + 1$ pairs is $f$. The average number of pairs is $m_c$.

*Proof.* The contact points move along $\ell$ at the same speed $r_{b1}\omega_1$, because the string of base circle 1 unwinds at that rate. By Claim 2 they are spaced $p_b$ apart. So over a time in which they move by $p_b$, the pattern repeats. A pair is in contact while its point is in the segment $AB$ of length $Z = (k + f)p_b$. A segment of length $(k + f)p_b$ holds $k + 1$ points of a grid of spacing $p_b$ for a share $f$ of the shifts of the grid, and $k$ points for the rest. The average is $k(1 - f) + (k + 1)f = k + f$. $\blacksquare$

So the drive is never broken if and only if $m_c \ge 1$.

### Rule of thumb, not a theorem

Shigley advises that gears should not be designed with contact ratios below about $1.20$, because errors of mounting can lower the contact ratio further and then increase impact and noise. This is a rule of thumb. The theorem gives only $m_c \ge 1$ for an unbroken drive of perfect gears. The margin above 1 covers errors of shape, center distance and deflection under load, and how much margin is needed depends on the accuracy of the gears.

## Examples and non-examples

**A standard pair.** Take $m = 4$ mm, $\varphi = 20°$, $z_1 = 20$, $z_2 = 30$, standard teeth with the addendum (the height above the pitch circle) of $1\,m$, at $c = 100$ mm. Then $r_{b1} = 37.588$, $r_{b2} = 56.382$, $r_{a1} = 44$ and $r_{a2} = 64$ mm, so

$$Z = 22.873 + 30.284 - 100\sin 20° = 22.873 + 30.284 - 34.202 = 18.955 \text{ mm},$$

and $p_b = 4\pi\cos 20° = 11.809$ mm, so $m_c = 1.605$. Two pairs are in contact for $60.5\%$ of the time and one pair for $39.5\%$. The two shares sum to $1$, and $2(0.605) + 1(0.395) = 1.605$.

**The center distance moved.** At $c = 101$ mm the same gears have $\varphi' = 21.505°$ and $c\sin\varphi' = 37.024$ mm, so $Z = 16.133$ mm and $m_c = 1.366$. The speed ratio stays the same, as the involute page proves, but the contact ratio drops.

**Other cases with the addendum $1\,m$.**

| pair | $\varphi$ | $m_c$ |
| --- | --- | --- |
| $z = 20$ and $30$ | $25°$ | $1.442$ |
| $z = 40$ and $80$ | $20°$ | $1.770$ |
| $z = 13$ and $13$ | $20°$ | $1.442$ |
| $z = 20$ and a rack | $20°$ | $1.769$ |

A larger pressure angle gives shorter contact, and more teeth give longer contact. For a rack, the tip line of the rack cuts $\ell$ at the distance $m/\sin\varphi$ from $P$, which replaces $a_2 - r_2\sin\varphi$ in the formula.

**Non-example: interference.** For $z_1 = z_2 = 12$ at $20°$, the formula gives $1.420$, but the number is wrong. Here $a_1 = a_2 = 16.595$ mm is more than $c\sin\varphi = 16.417$ mm, so each tip circle cuts $\ell$ beyond the far tangent point, outside the segment $T_1T_2$. The tips then touch the other gear below its base circle, where it has no involute, and the hypothesis of Claim 1 fails. This is interference, the subject of [gear undercutting](/gear-undercutting/). With $13$ teeth each, $a_i = 17.409 < 17.785$ mm and the pair is free of it, which is the value $13$ that Shigley gives for a pair of equal full-depth $20°$ gears. The pair $z = 20$ and $30$ at $14.5°$ also fails the check, with $a_2 = 26.864 > 25.038$ mm.

## Related definitions

- [Involute gear tooth](/involute-gear-tooth/): the profile, the line of action and the base pitch.
- [Fundamental law of gearing](/fundamental-law-of-gearing/): the constant ratio of each pair. The contact ratio adds the condition that some pair is always in contact.
- [Gear undercutting](/gear-undercutting/): what happens when the tips reach past the tangent points, and the limit on the number of teeth.
- Face contact ratio: helical gears add a second ratio, the face width times $\tan$ of the helix angle over the circular pitch, because the contact also moves across the face. The total contact ratio is the sum.

## References
