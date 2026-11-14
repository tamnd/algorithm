---
tag: NWXR8C
kind: model
slug: peaucellier-lipkin-linkage
name: Peaucellier-Lipkin linkage
aliases:
- Peaucellier inversor
- Peaucellier cell
area: cad/mechanism-and-assembly-design
level: core
summary: An eight-link mechanism whose cell inverts points in a circle, so a crank point on a circle through the center maps to an exact straight line, the first exact planar straight-line linkage.
prereqs: [four-bar-linkage, grubler-formula]
see_also: [kempe-universality-theorem, path-generation, coupler-curve, slider-crank-mechanism, watt-and-stephenson-six-bar, roberts-chebyshev-theorem, degrees-of-freedom-analysis, kinematic-synthesis]
sources:
  - paper: "A. Peaucellier, Note sur une question de géométrie de compas, Nouvelles Annales de Mathématiques, 2e série, 12 (1873), 71 to 78"
    locator: the proof that the cell inverts points and draws a straight line; the problem was first posed by Peaucellier in Nouvelles Annales de Mathématiques, 2e série, 3 (1864), 414 to 415
  - paper: "L. Lipkine, Dispositif articulé pour la transformation rigoureuse du mouvement circulaire en mouvement rectiligne, Bulletin de l'Académie Impériale des Sciences de St.-Pétersbourg, 16 (1871), 57 to 60"
    locator: the independent discovery of the same cell
  - book: "A. B. Kempe, How to Draw a Straight Line: A Lecture on Linkages, Macmillan, London, 1877"
    locator: the Peaucellier cell, Hart's inversor and the straight-line linkages built from them (general locator)
  - book: isbn:9780691131184
    title: John Bryant and Chris Sangwin, How Round Is Your Circle? Where Engineering and Mathematics Meet, Princeton University Press, 2008
    locator: Chapter 2, How to Draw a Straight Line (Peaucellier's linkage, Hart's inversor and the Sarrus linkage; general locator, page numbers not confirmed)
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Chapter 3, the section on straight-line mechanisms, approximate and exact (section number not confirmed for this edition), with the Grübler count of Chapter 2
---

The Peaucellier-Lipkin linkage is a planar mechanism of eight links and revolute joints only that moves a point along an exact straight line. Its heart is the Peaucellier cell, a rhombus of four equal links with two longer links joining opposite corners to a fixed pivot. The cell keeps two of its corners inverse to each other in a circle about the pivot, and inversion turns a circle through the pivot into a straight line. So a crank that moves one corner on such a circle makes the opposite corner move on a line, with no slide.

No [four-bar linkage](/four-bar-linkage/) can do this: the straight-line four-bars of Watt and Chebyshev follow a line only approximately, because a [coupler curve](/coupler-curve/) of degree 6 is not a line. The [slider-crank mechanism](/slider-crank-mechanism/) gives a line through a prismatic joint, which is a guide rather than a linkage. This page gives the geometry of the cell, the proof, the working range of the crank and the configurations in which the cell stops working.

## The machine

### The mechanism

**Inversion.** Inversion in the circle with center $O$ and radius $k$ maps a point $P \ne O$ to the point $Q$ on the ray from $O$ through $P$ with

$$|OP| \cdot |OQ| = k^2.$$

In complex numbers with $O = 0$ it is $Q = k^2 P / |P|^2$. It exchanges the inside and the outside of the circle, it fixes the circle itself, and it is its own inverse.

**The cell.** Two links of length $L$ join the fixed pivot $O$ to the corners $A$ and $B$. Four links of length $s < L$ join $A$ and $B$ to the corners $P$ and $Q$: $AP$, $PB$, $BQ$ and $QA$. So $A P B Q$ is a rhombus with side $s$. The cell has 7 links (the ground and six bars) and 8 joints counted with multiplicity: a joint where three links meet counts as two. There are such triple joints at $O$, $A$ and $B$. The [Grübler formula](/grubler-formula/) gives

$$M = 3(7 - 1) - 2 \cdot 8 = 2,$$

so $P$ can be moved freely in a region of the plane, and $Q$ follows it.

**The straight-line linkage.** A crank of length $\rho$ turns about a second fixed pivot $C$, with $|OC| = \rho$, and its end is pinned to $P$. Now there are 8 links and 10 joints (the joint at $P$ now joins three links), and

$$M = 3(8 - 1) - 2 \cdot 10 = 1.$$

$P$ moves on the circle about $C$ through $O$, and $Q$ moves on a straight line perpendicular to $OC$ at distance $(L^2 - s^2)/(2\rho)$ from $O$.

**Theorem (Peaucellier 1864, 1873; Lipkin 1871).** In every configuration of the cell with $A \ne B$ and $P \ne Q$, or with $A \ne B$ and $P = Q$ at the midpoint of $AB$, the points $O$, $P$, $Q$ lie on one ray from $O$ and

$$|OP| \cdot |OQ| = L^2 - s^2.$$

So $Q$ is the inverse of $P$ in the circle about $O$ of radius $k = \sqrt{L^2 - s^2}$. If $P$ moves on a circle through $O$ with center $C$ and radius $\rho = |OC|$, then $Q$ moves on the line perpendicular to $OC$ at distance $k^2 / (2\rho)$ from $O$.

*Proof.* Since $A \ne B$, the points equidistant from $A$ and $B$ form a line $\ell$, the perpendicular bisector of $AB$, which meets $AB$ at its midpoint $M$. The points $O$, $P$ and $Q$ are each at equal distances from $A$ and $B$ ($L$, $s$ and $s$), so all three lie on $\ell$. By Pythagoras in the right triangles $OMA$, $PMA$ and $QMA$,

$$|OM|^2 = L^2 - |AM|^2, \qquad |PM|^2 = s^2 - |AM|^2 = |QM|^2.$$

So $P$ and $Q$ are the two points of $\ell$ at distance $\sqrt{s^2 - |AM|^2}$ from $M$, which are distinct when $P \ne Q$ and both equal to $M$ when $P = Q = M$. Either way $M$ is the midpoint of $PQ$. Put a coordinate $t$ on $\ell$ with $M$ at $0$ and $O$ at $-u$, $u = |OM| > 0$ (since $|AM| \le s < L$), and put $P$ at $p$ and $Q$ at $-p$. Then

$$|OP| \cdot |OQ| = |u + p| \cdot |u - p| = u^2 - p^2 = (L^2 - |AM|^2) - (s^2 - |AM|^2) = L^2 - s^2.$$

Here $|u \pm p| = u \pm p$ because $p^2 = s^2 - |AM|^2 < L^2 - |AM|^2 = u^2$. The same inequality shows that $P$ and $Q$ lie on the same side of $O$, on one ray. This proves the first part.

For the line, take $O = 0$ and $C = \rho$ on the real axis, and write the crank point as $P = \rho(1 + e^{i\tau})$ with $\tau \ne \pi$. Then $|P|^2 = 2\rho^2(1 + \cos\tau)$ and $\operatorname{Re} P = \rho(1 + \cos\tau)$, so

$$Q = \frac{k^2 P}{|P|^2} = \frac{k^2}{2\rho}\left(1 + i \, \frac{\sin\tau}{1 + \cos\tau}\right) = \frac{k^2}{2\rho}\left(1 + i \tan\frac{\tau}{2}\right).$$

The real part of $Q$ is the constant $k^2/(2\rho)$, so $Q$ lies on the vertical line at that distance from $O$, which is perpendicular to $OC$. $\blacksquare$

A step of the model is one crank angle $\tau$, and the model gives $P$, the corners $A$ and $B$ as the intersections of the circle about $O$ of radius $L$ with the circle about $P$ of radius $s$, and $Q = A + B - P$.

## What it counts

A mechanism model counts no cost. This section gives the parameters, the configuration space and what the linkage can draw.

### Parameters and configuration space

The cell has two lengths, $L$ and $s$, and only $k^2 = L^2 - s^2$ enters the inversion. The crank adds $\rho$ and the place of $C$. With $|OC| = \rho$ the output is a line, and the line is fixed by $k^2/(2\rho)$.

**Where $P$ can go.** $|OP| = u - p$ or $u + p$ in the notation of the proof. As the cell moves, $|OP|$ ranges over $[L - s, L + s]$, the annulus where the circles of radius $L$ about $O$ and of radius $s$ about $P$ meet. For each $P$ strictly inside the annulus there are two cells, mirror images with $A$ and $B$ exchanged.

**Configurations where the cell fails.** The proof needs $A \ne B$, and the cell has two kinds of special configurations:

1. *$A = B$*, when $|OP| = L - s$ or $|OP| = L + s$. The two long links lie on top of each other and the rhombus folds flat. Then the circles of radius $s$ about $A$ and $B$ coincide, and $P$ and $Q$ can move independently on one circle. From such a configuration the linkage can leave the rhombus branch, and $Q$ is no longer the inverse of $P$.
2. *$P = Q$*, when $|OP| = k$ and the rhombus is flat with $|AB| = 2s$. Here the two intersection points of the circles about $A$ and $B$ merge. The cell can go on as a rhombus, with $P$ and $Q$ exchanging the inside and the outside of the circle of inversion, or it can go on with $P$ and $Q$ moving together as one point, which is not an inversion.

A working design keeps $|OP|$ strictly between $L - s$ and $k$ (or strictly between $k$ and $L + s$) over the whole stroke. These two kinds of degenerate configurations are the same difficulty that the [Kempe universality theorem](/kempe-universality-theorem/) has with its parallelograms and contraparallelograms.

**Range of the crank.** With $P = \rho(1 + e^{i\tau})$, $|OP| = 2\rho\cos(\tau/2)$ for $|\tau| < \pi$. If $L - s < 2\rho < k$, then $|OP| < k$ for all $\tau$, and the working range is $2\rho\cos(\tau/2) > L - s$, that is

$$|\tau| < 2 \arccos\frac{L - s}{2\rho}.$$

Over this range $Q$ moves along the line through the open segment of half-length $\frac{k^2}{2\rho}\tan\left(\arccos\frac{L - s}{2\rho}\right)$ about the foot of the perpendicular from $O$.

**Example.** Take $L = 5$, $s = 2$ and $\rho = 2$, with $O = (0, 0)$ and $C = (2, 0)$. Then $k^2 = 21$, $k \approx 4.583$, and $L - s = 3 < 2\rho = 4 < k$. The line is $x = 21/4 = 5.25$, and $Q = 5.25\,(1, \tan(\tau/2))$.

| crank angle $\tau$ | $P$ | $\lvert OP \rvert$ | $Q$ | $\lvert OP \rvert \cdot \lvert OQ \rvert$ |
| --- | --- | --- | --- | --- |
| $0°$ | $(4, 0)$ | $4$ | $(5.25, 0)$ | $21$ |
| $53.13°$ | $(3.2, 1.6)$ | $3.578$ | $(5.25, 2.625)$ | $21$ |
| $\pm 82.82°$ | the ends of the range | $3 = L - s$ | $(5.25, \pm 4.630)$ | $21$ |

For $P = (3.2, 1.6)$ the corners are $A = (3.4920, 3.5786)$ and $B = (4.9580, 0.6464)$, and $A + B - P = (5.25, 2.625)$. The stroke of $Q$ is the open segment of length $2 \cdot 5.25 \cdot \sqrt 7/3 \approx 9.260$, and the crank turns through less than $\pm 82.82°$ to avoid the fold $A = B$. A simulation that stepped $\tau$ in 40000 parts, found $A$ and $B$ from the circles and set $Q = A + B - P$, kept $Q$ on $x = 5.25$ to within $1.5 \cdot 10^{-14}$.

### What it can do

- **An exact straight line**, with revolute joints only, as proved above.
- **Exact circles of any radius.** If $|OC| \ne \rho$, the crank circle does not pass through $O$, and its inverse is again a circle, since inversion maps circles not through $O$ to circles not through $O$. When $|OC|$ is close to $\rho$, the image circle is very large, so a small linkage draws an arc of a circle whose center is far outside the machine.
- **Inversion of any curve.** Without the crank the cell has two degrees of freedom, and moving $P$ along any curve in the working annulus makes $Q$ trace its inverse.

## Relation to other models

- **Four-bar straight-line linkages.** The linkages of Watt, Roberts and Chebyshev and Hoeken's linkage are four-bars whose [coupler curves](/coupler-curve/) have a nearly straight stretch. They use four links instead of eight but are only approximate. Their cognates are given by the [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/).
- **Slider-crank.** The [slider-crank mechanism](/slider-crank-mechanism/) moves a point on an exact line with a prismatic joint. A sliding guide wears and is harder to make true than a pin joint, which is why an exact line from pins alone mattered to engineers of the steam era.
- **Hart's inversor.** Hart's cell does the same inversion with four bars in an antiparallelogram (a crossed quadrilateral with opposite sides equal), so a straight-line mechanism with a crank needs six links instead of eight. Kempe's lecture and Bryant and Sangwin describe it.
- **Sarrus linkage.** Sarrus described in 1853 a spatial linkage of hinged plates that moves a plate along an exact straight line. It is spatial, so the Peaucellier-Lipkin linkage is the first exact planar one.
- **Six-bars.** The [Watt and Stephenson six-bars](/watt-and-stephenson-six-bar/) have one degree of freedom with six links. The Peaucellier linkage has eight links and ten joints, still with mobility 1.
- **Universality.** By the [Kempe universality theorem](/kempe-universality-theorem/), any bounded piece of a plane algebraic curve is drawn by some linkage. The line is the case of degree 1, and the Peaucellier linkage is a small explicit solution.

## Known results in the model

- **Inversion.** $|OP| \cdot |OQ| = L^2 - s^2$ with $O$, $P$, $Q$ on one ray, for every configuration with $A \ne B$ on the rhombus branch (proved above).
- **Straight line.** With $|OC| = \rho$, $Q = \frac{k^2}{2\rho}(1 + i\tan(\tau/2))$, a line perpendicular to $OC$ at distance $k^2/(2\rho)$ from $O$ (proved above).
- **Mobility.** $M = 2$ for the cell with its ground and $M = 1$ with the crank, by the Grübler count. The count holds away from the special configurations $A = B$ and $P = Q$.
- **Working range.** $L - s < |OP| < k$ (or $k < |OP| < L + s$), which for the crank through $O$ gives $|\tau| < 2\arccos((L - s)/(2\rho))$ when $L - s < 2\rho < k$.
- **Speed along the line.** $\frac{d}{d\tau} \operatorname{Im} Q = \frac{k^2}{4\rho}\sec^2\frac{\tau}{2}$, so a crank at constant speed moves $Q$ slowest at the foot of the perpendicular and faster towards the ends.

## References
