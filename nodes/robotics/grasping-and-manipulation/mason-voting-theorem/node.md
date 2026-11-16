---
tag: 0D9KZB
kind: theorem
slug: mason-voting-theorem
name: Mason's voting theorem
aliases:
- rotation sense of a pushed object
area: robotics/grasping-and-manipulation
level: advanced
summary: The sense of rotation of a quasi-statically pushed object follows from three votes, by the two friction cone edges and the pushing direction, about the center of friction.
prereqs: [quasi-static-pushing, limit-surface, friction-cone]
see_also: [sensorless-part-orienting, goldberg-part-orienting-algorithm, instant-center-of-velocity, wrench, rigid-body-twist, manipulation-planning, fixture-planning, grasp-contact-models]
sources:
  - paper: doi:10.1177/027836498600500303
    title: Matthew T. Mason, Mechanics and planning of manipulator pushing operations, The International Journal of Robotics Research 5(3), 53-71, 1986
    locator: the whole paper (the quasi-static analysis of pushing and the voting rule for the sense of rotation)
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 7, Section 7.2 (pushing, from page 147)
  - paper: doi:10.1016/0043-1648(91)90104-3
    title: Suresh Goyal, Andy Ruina and Jim Papadopoulos, Planar sliding with dry friction. Part 1. Limit surface and moment function, Wear 143(2), 307-330, 1991
    locator: the whole paper (the limit surface and maximum dissipation, used in the proof below)
  - paper: doi:10.1109/IROS.1992.587370
    title: Kevin M. Lynch, Hitoshi Maekawa and Kazuo Tanie, Manipulation and active sensing by pushing using tactile feedback, IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 1992
    locator: the whole paper (the closed form of the pushed motion for an ellipsoidal limit surface)
---

Mason's voting theorem tells which way an object turns when a robot pushes it across a table at one point. Three lines through the contact point vote: the two edges of the friction cone at the contact and the direction in which the pusher moves. Each votes clockwise or counterclockwise by the side on which it passes the center of friction of the support, and the majority wins. The result does not need the pressure distribution under the object, which is almost never known. It is one result inside the [quasi-static pushing](/quasi-static-pushing/) model; the [limit surface](/limit-surface/) is the friction law of that model, and this page uses it only in the proof.

## Statement

**Hypotheses.**

1. A rigid object lies on a horizontal plane. It moves in the plane, quasi-statically: inertial forces are negligible, so at each instant the pusher force balances the friction of the support.
2. The support has Coulomb friction with one coefficient $\mu_s$ everywhere, and a pressure distribution $p \ge 0$ that is not concentrated on a line. The *center of friction* $O$ is the center of pressure, $\int p\, r\, dA / \int p\, dA$.
3. A pusher touches the object at one point $r_c$, where the object has the inward normal $n$. The contact has Coulomb friction with coefficient $\mu_c$, so the pusher force lies in the [friction cone](/friction-cone/) with the edges $e_l = n + \mu_c t$ and $e_r = n - \mu_c t$, where $t$ is a unit tangent.
4. The pusher moves with velocity $v_p$ with $v_p \cdot n > 0$, and the object moves.

For a direction $d$, let $M(d) = \operatorname{cross}(r_c - O, d)$, with $\operatorname{cross}(a, b) = a_x b_y - a_y b_x$. This is the moment about $O$ of a force along $d$ at $r_c$. The ray from $r_c$ along $d$ *votes counterclockwise* if $M(d) > 0$ and *clockwise* if $M(d) < 0$; it passes to the right or to the left of $O$.

**Conclusion.** Let the three rays along $e_l$, $e_r$ and $v_p$ vote, with none of them through $O$. Then:

- if $e_l$ and $e_r$ vote the same way, the object rotates that way, whatever $v_p$ is;
- if they vote differently, the object rotates the way $v_p$ votes.

In both cases the sense of rotation is the majority of the three votes. It does not depend on the pressure distribution $p$.

## In plain words

Push a book on a table with a finger, near one corner. The finger can push straight in or a bit to the side, as far as friction allows. If every push the finger can make passes on the same side of the book's balance point, the book turns that way, no matter how the finger moves. If the possible pushes pass on both sides, the way the finger moves decides. You do not need to know where the book presses hardest on the table, only the balance point of that pressure.

## Proof

The proof has two steps. The first is a lemma about the support friction that holds for every pressure distribution. Take moments about $O$, and write the twist of the object as $\xi = (\omega, v)$, with $v$ the velocity of the point at $O$, and the wrench of the pusher as $w_c = (M(f_c), f_c)$.

**Lemma (the friction moment opposes the rotation).** If the object rotates, $\omega \ne 0$, then the moment of the pusher force about the center of friction has the sign of $\omega$: $\omega\, M(f_c) > 0$.

*Proof.* Let $W$ be the set of wrenches that the support friction can balance, the convex set bounded by the limit surface. It is symmetric about the origin. A pure translation with unit velocity $-u$ gives a friction force $\mu_s N u$ with zero moment about $O$, because $\int \mu_s p\, (r - O)\, dA = 0$. So $(0, \mu_s N u) \in W$ for every unit vector $u$, and by convexity $(0, f) \in W$ whenever $\lvert f \rvert \le \mu_s N$. The force part of every wrench in $W$ has size at most $\mu_s N$, the sum of all friction forces, so $(0, f_c) \in W$. Quasi-statically, $w_c$ balances the support friction, and by the maximum dissipation property of the limit surface (Goyal, Ruina and Papadopoulos 1991) $w_c$ maximizes $\xi \cdot w$ over $W$. Comparing with $(0, f_c)$ gives $\omega M(f_c) + v \cdot f_c \ge v \cdot f_c$, so $\omega M(f_c) \ge 0$.

For strictness, suppose $\omega \ne 0$ and $M(f_c) = 0$. Then the dissipated power is $\xi \cdot w_c = v \cdot f_c \le \lvert v \rvert \mu_s N$. It also equals $\int \mu_s p\, \lvert v(r) \rvert\, dA \ge \lvert \int \mu_s p\, v(r)\, dA \rvert = \mu_s N \lvert v \rvert$, where $v(r) = v + \omega J (r - O)$ and $J$ is the turn by 90 degrees; the last step uses again that $O$ is the center of friction. So equality holds in the triangle inequality, and all the velocities $v(r)$ on the support point the same way. For a rotation this happens only on a half line from the center of rotation, which hypothesis 2 excludes. $\square$

**Step 1: the edges agree.** The force $f_c$ is a nonnegative combination of $e_l$ and $e_r$, not zero because the object moves. $M$ is linear, so if $M(e_l)$ and $M(e_r)$ have the same sign, $M(f_c)$ has that sign. The object cannot translate: a translation has $\omega = 0$, and the friction of a translation has zero moment about $O$, so $M(f_c) = 0$, which is false. So $\omega \ne 0$, and by the lemma $\omega$ has the sign of $M(f_c)$. This case holds for every pressure distribution.

**Step 2: the edges disagree.** Say $M(e_l) > 0 > M(e_r)$, so $M(t) = (M(e_l) - M(e_r)) / (2\mu_c) > 0$. The contact either sticks, or slides with $f_c$ on one edge of the cone. Mason (1986) shows for every pressure distribution that the sense of rotation is the vote of $v_p$, by an analysis of these contact modes and of the centers of rotation that each allows. We give the argument for the ellipsoidal limit surface of the quasi-static pushing page, where it is short. With moments about $O$ and $c = m_{\max} / f_{\max}$, the twist is normal to the ellipsoid: $\xi = k\,(M(f_c) / m_{\max}^2,\ f_c / f_{\max}^2)$ with $k > 0$. The velocity of the contact point is $v_c = v + \omega J (r_c - O)$, so

$$M(v_c) = \operatorname{cross}(r_c - O, v) + \omega \lvert r_c - O \rvert^2 = k\, M(f_c) \left( \frac{1}{f_{\max}^2} + \frac{\lvert r_c - O \rvert^2}{m_{\max}^2} \right).$$

So $M(v_c)$, $M(f_c)$ and $\omega$ have the same sign. Now:

- *Sticking*: $v_p = v_c$, so $\omega$ has the sign of $M(v_p)$.
- *Sliding with $f_c$ along $e_l$*: the friction on the object has the tangential part along $+t$, so the object slips along $-t$ relative to the pusher, and $v_p = v_c + s t$ with $s > 0$. Here $M(f_c) = M(e_l) > 0$, so $\omega > 0$ and $M(v_c) > 0$, and then $M(v_p) = M(v_c) + s M(t) > 0$. The vote of $v_p$ is counterclockwise, as is the rotation.
- *Sliding with $f_c$ along $e_r$*: by the same argument with the signs reversed, $\omega < 0$ and $M(v_p) < 0$.

In every mode the object turns the way $v_p$ votes. $\square$

## Consequences

- **Planning without the pressure.** A planner can choose pushes whose rotation sense is certain, using only the support region (through its center of friction) and bounds on $\mu_c$. If the center of friction is only known to lie in a region, a push whose three rays all pass the region on the same side has a certain sense.
- **Orienting parts.** A push against a fence or a jaw turns a part toward a stable edge. The voting rule tells which edge, and so it gives the push functions of [sensorless part orienting](/sensorless-part-orienting/), and of the push-grasp variant of [Goldberg's algorithm](/goldberg-part-orienting-algorithm/).
- **Robust to the model of the support.** Step 1 uses only the convexity and maximum dissipation of the support friction, so it holds for every pressure distribution and for both the exact limit surface and the ellipsoid model.

## Tightness

- **Only the sense.** The theorem fixes the sense of rotation, not its rate or the center of rotation. Both depend on the pressure distribution.
- **Ties.** If a ray passes through the center of friction, its vote is void. When the edges disagree and the push passes through $O$, the theorem says nothing; the object can translate, as when a disc is pushed at its rim along the normal.
- **The center of friction, not the center of mass.** With a uniform $\mu_s$ the center of friction is the center of pressure, and under a slow push on a flat table it is usually taken to be below the center of mass. If $\mu_s$ varies over the support, the rule needs the center of friction $\int \mu_s p\, r\, dA / \int \mu_s p\, dA$ instead, and the proof is the same.
- **Quasi-static only.** With fast pushes, inertia can turn the object the other way for a short time, and the rule does not apply.
- **One point contact.** With two contacts or an edge contact, the possible pusher forces form a larger set of wrenches, and the three-ray rule is replaced by a test on that set.

## History

Mason (1986) studied the mechanics of pushing in the quasi-static model and gave the voting rule as a way to predict the rotation of a pushed object without the support pressure, which a planner rarely knows. His book (Mason 2001) presents it with the mechanics of pushing. Goyal, Ruina and Papadopoulos (1991) then gave the general theory of the limit surface, and Lynch, Maekawa and Tanie (1992) used an ellipsoidal limit surface to get closed forms of the pushed motion.

## References
