---
tag: ENSRSS
kind: concept
slug: candy-wrapper-artifact
name: Candy wrapper artifact
aliases:
- collapsing joint artifact
area: graphics-and-signals/character-animation
level: core
summary: The loss of volume of linear blend skinning when joints twist or bend far, because averaging rotation matrices does not give a rotation.
prereqs: [linear-blend-skinning]
see_also: [dual-quaternion-skinning, spherical-blend-skinning, optimized-centers-of-rotation-skinning, delta-mush, character-skinning, special-orthogonal-group, rotation-averaging, pose-space-deformation]
sources:
  - url: https://skinning.org/direct-methods.pdf
    title: Ladislav Kavan, Part I, Direct skinning methods and deformation primitives, in Alec Jacobson, Zhigang Deng, Ladislav Kavan and J. P. Lewis, Skinning, Real-time Shape Deformation, SIGGRAPH 2014 course
    locator: "Section 2 (linear blend skinning and the candy wrapper artifact) and Section 4 (dual quaternion blending as a fix, and its bulging artifact)"
  - paper: doi:10.1145/1409625.1409627
    title: Ladislav Kavan, Steven Collins, Jiří Žára and Carol O'Sullivan, Geometric skinning with approximate dual quaternion blending, ACM Transactions on Graphics 27(4), article 105, 2008
    locator: "Section 2.2 (linear blend skinning, equation 2, and the candy wrapper example)"
---

The candy wrapper artifact is the collapse of the skin of [linear blend skinning](/linear-blend-skinning/) at a joint that twists.
Near a forearm that turns by half a turn, the skin narrows to a thin neck, like the twisted ends of a wrapped sweet.
The cause is exact and simple: LBS averages the skinning matrices of the joints, and the average of two rotation matrices is not a rotation, but a rotation times a shrink.
The same cause makes a bent elbow lose volume on its inside, the collapsing elbow; the candy wrapper is the twist case of that collapse.

## In plain words

Think of a long sweet in a paper wrapper, and twist one end while you hold the other.
The paper in the middle narrows to a thin neck.
Simple skinning does the same thing to a twisted arm.
A point of the skin halfway between the elbow and the wrist is moved partly as the elbow says and partly as the wrist says, and the result is the midpoint of the two places.
When the wrist turns far, those two places are on opposite sides of the arm, and their midpoint is near the middle of the arm.
So the skin there falls inward.
Better skinning methods blend the turns themselves, not the places, and keep the arm round.

## The idea

LBS moves a vertex by $v' = \sum_a w_a C_a v$, so the linear part of the map is the average $\bar R = \sum_a w_a R_a$ of the rotations $R_a$ of the joints.
Take two joints that turn about the same axis $x$: joint 0 by the angle $0$ and joint 1 by $\theta$, with the weights $1 - w$ and $w$.
In the plane orthogonal to the axis,

$$\bar R = (1 - w) \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} + w \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix} = \begin{pmatrix} p & -q \\ q & p \end{pmatrix}, \quad p = 1 - w + w\cos\theta, \; q = w \sin\theta.$$

A matrix of this form is a scale by $s = (p^2 + q^2)^{1/2}$ times a rotation by $\varphi = \operatorname{atan2}(q, p)$, and

$$s^2 = 1 - 2 w (1 - w) (1 - \cos\theta).$$

This is a proved property, with these consequences:
- $s < 1$ whenever $0 < w < 1$ and $\theta$ is not a multiple of $2\pi$: a ring of the radius $r$ about the axis shrinks to the radius $s r$. So the average is not a rotation.
- At $w = 1/2$, $s = \lvert\cos(\theta/2)\rvert$ and $\varphi = \theta/2$: the ring turns by the right angle but shrinks, and at $\theta = \pi$ it collapses onto the axis.
- At $\theta = \pi$, $s = \lvert 1 - 2w \rvert$, and the ring does not turn at all for $w < 1/2$ and is turned by $\pi$ for $w > 1/2$: along the limb, where $w$ rises from 0 to 1, the skin narrows to a neck and flips there, which is the look of the wrapper.
- At $\theta = 2\pi$ the two matrices are equal, and LBS gives no twist at all; a matrix cannot tell a full turn from none.

The same algebra holds for a bend: the rotations are about an axis through the joint, and the points in the plane of the bend move closer to the joint by the factor $s$.
The determinant of the blended linear part is $s^2$ here, so where the weights are nearly constant the local volume shrinks by that factor.

The methods that fix it blend rotations as rotations: [dual quaternion skinning](/dual-quaternion-skinning/) blends unit dual quaternions and normalizes, so each vertex moves rigidly; [spherical blend skinning](/spherical-blend-skinning/) and [optimized centers of rotation](/optimized-centers-of-rotation-skinning/) blend unit quaternions about a center.
These keep the radius, but DQS and its kin can bulge at a bent joint, the opposite artifact.

## Examples

**The check value.**
With the weights $0.5$ and $0.5$, joint 0 at the identity and joint 1 turned by $\pi$ about $x$, LBS maps $(0, 1, 0)$ to $0.5 (0, 1, 0) + 0.5 (0, -1, 0) = (0, 0, 0)$.
Dual quaternion skinning with the same weights turns the vertex by $\pi/2$, to $(0, 0, 1)$, and keeps the radius 1.

**The radius against the twist.**
For a vertex at the radius 1 with the weight $w = 0.5$:

| twist $\theta$ | radius with LBS, $\lvert\cos(\theta/2)\rvert$ | radius with DQS |
|---|---|---|
| $\pi/4$ | $0.92388$ | $1$ |
| $\pi/2$ | $0.70711$ | $1$ |
| $3\pi/4$ | $0.38268$ | $1$ |
| $\pi$ | $0$ | $1$ |

**Along the limb at a half turn.**
At $\theta = \pi$ the radius is $\lvert 1 - 2w \rvert$: $1$ at $w = 0$, $0.5$ at $w = 0.25$, $0$ at $w = 0.5$, $0.5$ at $w = 0.75$ and $1$ at $w = 1$.

**The collapsing elbow.**
Put the elbow at $(1, 0, 0)$, bend joint 1 by $\pi/2$ about $z$ through it, and take the vertex $(1.5, 0.2, 0)$ with the weights $0.5$ and $0.5$, at the distance $0.53852$ from the elbow.
LBS puts it at $(1.15, 0.35, 0)$, at the distance $0.38079 = 0.53852 \cos(\pi/4)$; DQS puts it at $(1.21213, 0.49497, 0)$, at the distance $0.53852$.

## Where it is used

- **As the test of a skinning method.** The twist of two joints by $\pi$ is the standard case; this site tests it on [LBS](/linear-blend-skinning/), [DQS](/dual-quaternion-skinning/), [spherical blend skinning](/spherical-blend-skinning/) and [CoR skinning](/optimized-centers-of-rotation-skinning/).
- **In rigging practice.** Riggers add twist joints along the forearm and the thigh, each taking a part of the twist, so that LBS blends only small angles, where $s$ is close to 1.
- **As the reason for corrections.** [Pose-space deformation](/pose-space-deformation/) and other corrective shapes add back the volume that LBS loses at the joints, and [delta mush](/delta-mush/) hides part of it (it does not keep the radius in a twist, as its page measures).
- **In the theory of rotation averages.** The fix is a better average of rotations; the [rotation group](/special-orthogonal-group/) is not convex, and [rotation averaging](/rotation-averaging/) studies the means that stay in it.
- **In the [character skinning](/character-skinning/) problem**, as the reason why no linear blend of the matrices can keep the volume in every pose.

## References
