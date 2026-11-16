---
tag: 74MX2A
kind: theorem
slug: stuelpnagel-theorem
name: Stuelpnagel's theorem
aliases:
- no global three-parameter rotation representation
area: robotics/rigid-body-motion
level: advanced
summary: No map from three numbers onto SO(3) is both one-to-one and nonsingular everywhere, so every three-parameter chart of rotations has a singular or a repeated point.
prereqs: [special-orthogonal-group, gimbal-lock]
see_also: [euler-angles, roll-pitch-yaw-angles, cayley-rotation-parameters, unit-quaternion-rotation, axis-angle-representation, so3-logarithm-map, configuration-space, error-state-kalman-filter]
sources:
  - paper: doi:10.1137/1006093
    title: John Stuelpnagel, On the parametrization of the three-dimensional rotation group, SIAM Review 6(4), 422-430, 1964
    locator: Section 3 (the topological argument by the invariance of domain), Section 4 (five- and six-dimensional parametrizations), Section 5 (quaternions) and Section 6 (three-dimensional parametrizations)
---

Stuelpnagel's theorem says that the rotations of space cannot be described by three numbers without a bad point.
Every map from an open set of $\mathbb{R}^3$ onto the [special orthogonal group](/special-orthogonal-group/) SO(3) either takes some rotation twice or has a point where its derivative loses rank.
[Euler angles](/euler-angles/) and [roll-pitch-yaw angles](/roll-pitch-yaw-angles/) fail by [gimbal lock](/gimbal-lock/), the exponential coordinates fail at the angle $2\pi$, and the [Cayley parameters](/cayley-rotation-parameters/) miss the half turns.
The cause is topological: SO(3) is a compact three-dimensional space, and no compact three-dimensional space fits one-to-one into $\mathbb{R}^3$.
This is the reason why orientation estimators and planners keep a [unit quaternion](/unit-quaternion-rotation/) or a rotation matrix, and use three numbers only for small errors.

## Statement

**Theorem.**

(a) There is no continuous one-to-one map $g : SO(3) \to \mathbb{R}^3$.

(b) Let $U \subseteq \mathbb{R}^3$ be open and let $f : U \to SO(3)$ be continuously differentiable and onto.
Then $f$ is not one-to-one, or its derivative has rank less than 3 at some point of $U$.

In the words of attitude dynamics: a parametrization of all rotations by three numbers cannot be both global (onto and one-to-one) and nonsingular (with a derivative of full rank everywhere).
With four numbers, unit quaternions give a nonsingular map that is two-to-one, and with five numbers a one-to-one nonsingular map exists.

## In plain words

You cannot give every orientation of a body its own three numbers in a smooth way.
Any scheme with three numbers, however clever, has a weak spot.
Either some orientation gets two or more sets of numbers, or near some orientation a tiny turn of the body changes the numbers by a large amount, or some orientation gets no numbers at all.
The weak spot can be moved by a change of the scheme, but it cannot be removed.
The reason is the shape of the set of all orientations.
It closes on itself in every direction, like the surface of a ball but one dimension higher, while three plain numbers spread out without end.
A closed shape cannot be laid flat into an open space without a tear or an overlap.
So a fourth number, as in a quaternion, is the price of a scheme with no weak spot.

## Proof

We use three facts about SO(3).

1. SO(3) is compact. Its entries satisfy $|r_{ij}| \le 1$, because the columns are unit vectors, and it is the set of zeros of the continuous maps $R \mapsto R^{\mathsf T}R - I$ and $R \mapsto \det R - 1$, so it is closed and bounded in $\mathbb{R}^9$.
2. SO(3) is a three-dimensional manifold. Fix $R_0$. The map $\phi_{R_0}(w) = R_0\, e^{[w]}$ on the open ball $B = \{ w : |w| < \pi \}$ is one-to-one onto the open set $V = \{ R : \operatorname{tr}(R_0^{\mathsf T}R) > -1 \}$, and its inverse $R \mapsto \log(R_0^{\mathsf T}R)$ is continuous on $V$, by [Rodrigues' formula](/rodrigues-rotation-formula/) and the [logarithm map](/so3-logarithm-map/). So every point of SO(3) has an open neighbourhood homeomorphic to an open ball of $\mathbb{R}^3$.
3. Invariance of domain (Brouwer). A continuous one-to-one map from an open set of $\mathbb{R}^n$ into $\mathbb{R}^n$ has an open image.

*Proof of (a).*
Suppose $g : SO(3) \to \mathbb{R}^3$ is continuous and one-to-one, and let $K = g(SO(3))$.
By fact 1, $K$ is compact, so it is closed and bounded in $\mathbb{R}^3$.
Take a point $y = g(R_0)$ of $K$.
The map $g \circ \phi_{R_0} : B \to \mathbb{R}^3$ is continuous and one-to-one, so by fact 3 its image is an open set of $\mathbb{R}^3$.
This image contains $y$ and lies in $K$.
So every point of $K$ has an open neighbourhood inside $K$, and $K$ is open.
$K$ is not empty, and it is both open and closed in the connected space $\mathbb{R}^3$, so $K = \mathbb{R}^3$.
But $K$ is bounded and $\mathbb{R}^3$ is not, which is a contradiction. $\square$

*Proof of (b).*
Suppose $f$ is onto, one-to-one, and has a derivative of rank 3 at every point.
By the inverse function theorem, every point of $U$ has a neighbourhood on which $f$ has a continuous inverse, so $f$ maps open sets to open sets.
Since $f$ is a bijection, its inverse $f^{-1} : SO(3) \to U$ exists, and it is continuous because $f$ is open.
Then $f^{-1}$ is a continuous one-to-one map from SO(3) into $\mathbb{R}^3$, which (a) forbids. $\square$

### A check by hand

The exponential coordinates $f(w) = e^{[w]}$ show each way of failing.
The derivative of $f$ at $w$, written as an angular velocity in the body frame, has the determinant $2(1 - \cos\theta)/\theta^2$ with $\theta = |w|$.
At $\theta = 1$ this is $0.9194$, at $\theta = \pi$ it is $4/\pi^2 = 0.4053$, and at $\theta = 2\pi$ it is $0$; a numerical derivative of $e^{[w]}$ at $w = (2\pi, 0, 0)$ has rank 1.

- On the open ball $|w| < \pi$, $f$ is one-to-one and nonsingular, but not onto: it misses the half turns.
- On the closed ball $|w| \le \pi$, $f$ is onto, but not one-to-one: $w = (\pi, 0, 0)$ and $w = (-\pi, 0, 0)$ both give $\operatorname{diag}(1, -1, -1)$. Every pair of opposite points of the boundary sphere gives one rotation, and gluing these pairs turns the ball into SO(3).
- On the ball $|w| < 2\pi$, $f$ is onto and nonsingular, but not one-to-one: the rotation by $\theta \in (0, \pi]$ about $\hat\omega$ comes from both $\theta\hat\omega$ and $-(2\pi - \theta)\hat\omega$, so only the identity is hit once.

The Cayley parameters $c = \tan\frac\theta2\,\hat\omega$ are one-to-one and nonsingular on all of $\mathbb{R}^3$, and they fail by not being onto.
Along the axis $x$, $c = (t, 0, 0)$ gives the angle $2\arctan t$: $90°$ for $t = 1$, $168.58°$ for $t = 10$, and $178.85°$ for $t = 100$; the half turn needs $t = \infty$.

## Consequences

- **Every three-angle chart has gimbal lock.** For [Euler angles](/euler-angles/) on a domain that reaches every rotation, the theorem forces a point of lower rank or a repeated rotation; the ZYZ chart has both, at $\beta = 0$ and $\beta = \pi$. A change of the axis order only moves the [gimbal lock](/gimbal-lock/).
- **Four numbers suffice for a nonsingular description.** The map from the unit sphere $S^3$ of quaternions to SO(3) is nonsingular and onto, and it is two-to-one, so it does not contradict part (b). Its domain is not an open set of $\mathbb{R}^3$.
- **Estimators use a global state and a local error.** The [error-state Kalman filter](/error-state-kalman-filter/) and filters on Lie groups store the attitude as a quaternion or a matrix and use a three-vector only for the small error, where the exponential coordinates are one-to-one and nonsingular.
- **Configuration spaces with rotations are not Euclidean.** A [configuration space](/configuration-space/) that contains SO(3) cannot be given one chart of $\mathbb{R}^3$, so planners need several charts, or a representation in more dimensions with a constraint.

## Tightness

- **Three numbers suffice locally.** Each point of SO(3) has a neighbourhood with a one-to-one nonsingular chart, for example $w \mapsto R_0 e^{[w]}$ on $|w| < \pi$. So the theorem is about a single chart for all rotations, not about small regions.
- **Four numbers, two-to-one.** Unit quaternions give a nonsingular map from $S^3$ onto SO(3) with exactly two points, $q$ and $-q$, over each rotation. No continuous map from $S^3$ onto SO(3) is one-to-one, because such a map would be a homeomorphism, and $S^3$ is simply connected while SO(3) is not.
- **Five numbers, one-to-one.** Stuelpnagel gave a one-to-one nonsingular parametrization of SO(3) by five numbers. Four do not suffice for this, because the real projective space of dimension 3, which is SO(3), does not embed in $\mathbb{R}^4$ (Hopf, 1940).
- **Six and nine numbers.** Two columns of $R$, six numbers with three constraints, give a one-to-one parametrization with a simple form, since the third column is their cross product. The nine entries of $R$ are the trivial one.

## History

John Stuelpnagel published the theorem in SIAM Review in 1964, in a survey of the parametrizations of the rotation group used for the attitude of spacecraft.
His Section 3 gives the argument above, based on Brouwer's invariance of domain, and his Section 6 checks it on roll, pitch and yaw, on the exponential coordinates and on the Cayley form.
He also cites the result of Heinz Hopf from 1940 that the real projective space of dimension 3 has no embedding in $\mathbb{R}^4$, which sets the five-number bound.

## References
