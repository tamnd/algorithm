---
tag: QVWVAX
kind: theorem
slug: chasles-theorem
name: Chasles' theorem
aliases:
- Mozzi-Chasles theorem
area: robotics/rigid-body-motion
level: core
summary: Every rigid body motion is a screw motion, a rotation about a line followed by a translation along the same line.
prereqs: [screw-motion, euler-rotation-theorem, special-euclidean-group]
see_also: [se3-exponential-map, rigid-body-twist, wrench, dual-quaternion, instant-center-of-velocity, small-displacement-torsor, slippage-analysis, kinematic-fixture-analysis]
sources:
  - paper: "Michel Chasles, Note sur les propriétés générales du système de deux corps semblables entr'eux, et placés d'une manière quelconque dans l'espace; et sur le déplacement fini, ou infiniment petit, d'un corps solide libre, Bulletin des Sciences Mathématiques, Astronomiques, Physiques et Chimiques (Férussac) 14, 321 to 326, 1830"
    locator: the whole note (the finite and the infinitely small displacement of a free rigid body)
  - book: "Giulio Mozzi, Discorso matematico sopra il rotamento momentaneo dei corpi, Stamperia di Donato Campo, Napoli, 1763"
    title: Giulio Mozzi, Discorso matematico sopra il rotamento momentaneo dei corpi, 1763
    locator: the whole book (the instantaneous motion of a rigid body as a rotation about an axis and a sliding along it)
  - paper: "Marco Ceccarelli, Screw axis defined by Giulio Mozzi in 1763 and early studies on helicoidal motion, Mechanism and Machine Theory 35(6), 761 to 770, 2000"
    locator: the whole paper (the history of the theorem and the work of Mozzi)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 3.3 (screws, a geometric description of twists, Theorem 2.11, Chasles)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.3.3 (exponential coordinates of rigid-body motions and the Chasles-Mozzi theorem) and the notes of Chapter 3
---

Chasles' theorem says that every rigid motion of space is a [screw motion](/screw-motion/): a rotation about some line together with a translation along the same line.
So the six numbers of a pose in the [special Euclidean group](/special-euclidean-group/) SE(3) can always be read as a line in space (four numbers), an angle and a slide along the line.
The theorem extends [Euler's rotation theorem](/euler-rotation-theorem/), which covers the motions that keep a point fixed, to all motions.
Its infinitesimal form, due to Mozzi, says that every [twist](/rigid-body-twist/) is a turning speed about a line plus a sliding speed along it.

## Statement

**Theorem.** Let $T = (R, p) \in SE(3)$ act by $x \mapsto Rx + p$.

1. If $R \ne I$, let $\hat s$ and $\theta \in (0, \pi]$ be an axis and the angle of $R$ from Euler's theorem. Put $d = \hat s \cdot p$. There is exactly one point $q$ with $q \cdot \hat s = 0$ and $(I - R)q = p - d\,\hat s$, and then $Tx = R(x - q) + q + d\,\hat s$ for all $x$. So $T$ is the screw motion about the line $L = \{q + t\hat s\}$ with magnitude $\theta$ and pitch $h = d/\theta$. The line $L$ is the only line that $T$ maps onto itself by a slide along it, and the points of $L$ are exactly the points that $T$ moves the least, by $|d|$.
2. If $R = I$ and $p \ne 0$, $T$ is a translation, the screw motion with infinite pitch along $\hat s = p/|p|$ with magnitude $|p|$. Every line parallel to $p$ is an axis.
3. If $T = I$, every screw with magnitude 0 gives $T$.

**Infinitesimal form (Mozzi).** Let $\mathcal{V} = (\omega, v)$ be a twist with $\omega \ne 0$. Then the velocity field $\dot x = \omega \times x + v$ is the turning speed $|\omega|$ about the line through $q = \omega \times v/|\omega|^2$ with direction $\omega$, plus the sliding speed $\omega \cdot v/|\omega|$ along it.

## In plain words

Take a solid object and move it from one place to another in any way, with any turns.
Then there is always one line in space with a special property.
You can get the object from the start to the end with a single twist about this line, like a nut that turns on a bolt.
The twist turns the object about the line and slides it along the line at the same time.
If the object did not turn at all, it only slid, and the line can be any line in the direction of the slide.
The points on the special line move less than all other points of the object.

## Proof

**Case 1, $R \ne I$.**
By [Euler's theorem](/euler-rotation-theorem/), $R$ is the rotation by some $\theta \in (0, \pi]$ about a unit vector $\hat s$, with $R\hat s = \hat s$.
Let $P$ be the plane of vectors orthogonal to $\hat s$.
Split $p = d\,\hat s + p_\perp$ with $d = \hat s \cdot p$ and $p_\perp \in P$.

The map $I - R$ sends $P$ into $P$, because $R$ does.
On $P$, $R$ is the planar rotation by $\theta$, and the determinant of $I - R$ on $P$ is $(1 - \cos\theta)^2 + \sin^2\theta = 2(1 - \cos\theta) > 0$ for $\theta \in (0, \pi]$.
So $I - R$ is a bijection of $P$, and there is exactly one $q \in P$ with $(I - R)q = p_\perp$.

For every $x$,

$$R(x - q) + q + d\,\hat s = Rx + (I - R)q + d\,\hat s = Rx + p_\perp + d\,\hat s = Rx + p = Tx .$$

So $T$ is the screw motion about $L = \{q + t\hat s\}$ with angle $\theta$ and slide $d = h\theta$.

**The axis is unique, and it holds the points that move least.**
For every $x$, $Tx - x = (R - I)(x - q) + d\,\hat s$.
The first term is orthogonal to $\hat s$, because $\hat s^{\mathsf T}(R - I) = (R^{\mathsf T}\hat s - \hat s)^{\mathsf T} = 0$, since $R^{\mathsf T}\hat s = \hat s$.
So

$$|Tx - x|^2 = |(R - I)(x - q)|^2 + d^2 \ge d^2 ,$$

with equality exactly when $(R - I)(x - q) = 0$.
The kernel of $R - I$ is the line of $\hat s$ (Step 4 of Euler's theorem), so equality holds exactly for $x \in L$.
If $T$ maps a line onto itself, then $R$ maps the direction of the line to itself, so this direction is $\pm\hat s$, and every point of the line moves along $\hat s$.
Then the first term is 0 at each point of the line, and the line is $L$.

**Case 2, $R = I$.**
Then $Tx = x + p$, which is the translation of the definition with $\hat s = p/|p|$ and magnitude $|p|$.
Every line parallel to $p$ slides onto itself, so no line is preferred.

**Case 3** is clear.

**Infinitesimal form.**
Split $v = v_\parallel + v_\perp$ along $\hat\omega = \omega/|\omega|$.
For $q = \omega \times v/|\omega|^2$, the identity $a \times (b \times c) = b(a \cdot c) - c(a \cdot b)$ gives $\omega \times q = (\omega(\omega \cdot v) - v|\omega|^2)/|\omega|^2 = v_\parallel - v$, so $-\omega \times q = v_\perp$.
Then $\omega \times x + v = \omega \times (x - q) + v_\parallel$, which is the turn about the line through $q$ plus the slide $v_\parallel = (\omega \cdot v/|\omega|)\,\hat\omega$. $\square$

The matrix logarithm of SE(3) in the [exponential map of SE(3)](/se3-exponential-map/) computes $(S, \theta)$ from $T$ and is a constructive proof of the same theorem, as Lynch and Park remark.

### A check by hand

Let $R = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$ and $p = (1, 0, 0)$.

- Euler's theorem gives $\hat s = (1, 1, 1)/\sqrt3$ and $\theta = 2\pi/3$.
- The slide is $d = \hat s \cdot p = 1/\sqrt3 \approx 0.57735$, and $p_\perp = (1, 0, 0) - \tfrac13(1, 1, 1) = (\tfrac23, -\tfrac13, -\tfrac13)$.
- Try $q = (\tfrac13, 0, -\tfrac13)$. It is orthogonal to $\hat s$. $Rq = (-\tfrac13, \tfrac13, 0)$, so $(I - R)q = (\tfrac23, -\tfrac13, -\tfrac13) = p_\perp$. This is the axis point.
- The pitch is $h = d/\theta = (1/\sqrt3)/(2\pi/3) \approx 0.27566$ m/rad.
- Check: $Tq = Rq + p = (\tfrac23, \tfrac13, 0) = q + \tfrac13(1, 1, 1) = q + d\,\hat s$. The axis point slides along the axis by $d$.
- The origin moves by $|p| = 1 > d$, as the minimum property says.

A smaller case: $R = R_z(\pi/2)$ and $p = (1, 1, 2)$ give the vertical axis through $(0, 1, 0)$, $d = 2$ and $h = 2/(\pi/2) = 4/\pi \approx 1.2732$ m/rad.

## Consequences

- **Exponential coordinates.** Every $T \in SE(3)$ is $e^{[S]\theta}$ for a screw axis $S$ and a $\theta \ge 0$. So the exponential map of SE(3) is onto, and $(S, \theta)$ are coordinates on all of SE(3).
- **Interpolation along a screw.** The curve $t \mapsto e^{[S]t\theta}$ for $t \in [0, 1]$ moves a body from $I$ to $T$ along one screw at a constant twist. This is the screw linear interpolation of [dual quaternions](/dual-quaternion/).
- **Minimum displacement.** The slide $|d| = |\hat s \cdot p|$ is the smallest distance that any point of the body moves. It does not depend on the frame.
- **Instantaneous screw axis.** By the infinitesimal form, every [twist](/rigid-body-twist/) with $\omega \ne 0$ is a screw axis times a speed. In the plane this reduces to the [instant center of velocity](/instant-center-of-velocity/).
- **Wrenches.** The same algebra with force in place of angular velocity gives Poinsot's theorem: every system of forces on a rigid body is a force along a line plus a moment about the same line, a [wrench](/wrench/) with a pitch.

## Tightness

- **Reflections are excluded.** For $\det R = -1$, such as $x \mapsto \operatorname{diag}(1, 1, -1)x + (1, 0, 0)$, the map is a reflection followed by a slide in the mirror plane (a glide reflection), which no screw motion gives.
- **No rotation, no unique axis.** For $R = I$ and $p \ne 0$, every line parallel to $p$ is an axis. This is the limit of infinite pitch.
- **The pitch depends on the chosen angle.** The line $L$, the rotation and the slide $d$ depend only on $T$. The pitch $h = d/\theta$ uses $\theta \in (0, \pi]$, and the angles $\theta + 2\pi k$ give the same $T$ with other pitches. At $\theta = \pi$, the axis directions $\hat s$ and $-\hat s$ both work, with $d$ and $h$ of opposite signs, so a half turn plus a slide is both a right-handed and a left-handed screw.
- **The plane.** In SE(2) there is no direction along the axis to slide, so every planar motion is a rotation about one point or a translation. A planar motion with a slide is not possible.
- **Numerics.** As $\theta \to 0$, $I - R$ on $P$ has the small determinant $2(1 - \cos\theta)$, and the axis point $q$ moves to infinity. Small rotations with a large translation have an axis far away.

## History

Giulio Mozzi described the instantaneous motion of a rigid body as a turning about an axis and a sliding along it in a book printed in Naples in 1763, as Ceccarelli (2000) shows.
Michel Chasles stated the theorem for finite and for infinitely small displacements of a free solid in a short note in the Bulletin of Férussac, volume 14, in 1830.
Robert Ball built the theory of screws on it in his Treatise on the Theory of Screws (1900), and the robotics books of Murray, Li and Sastry (1994) and of Lynch and Park (2017) give it as the screw interpretation of the exponential coordinates.

## References
