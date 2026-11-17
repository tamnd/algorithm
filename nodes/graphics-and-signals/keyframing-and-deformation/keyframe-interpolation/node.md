---
tag: MQDV76
kind: problem
slug: keyframe-interpolation
name: Keyframe interpolation
aliases:
- in-betweening
- tweening
area: graphics-and-signals/keyframing-and-deformation
level: intro
summary: Given the values of animation parameters at key times, compute a value for every frame in between, so that the motion passes through the keys and is smooth.
model: real-ram
prereqs: [hermite-spline, catmull-rom-spline]
see_also: [ease-in-ease-out, arc-length-table, squad, kochanek-bartels-spline, spherical-linear-interpolation, euler-angles, skeletal-animation, principles-of-animation]
sources:
  - paper: doi:10.1145/360349.360357
    title: N. Burtnyk and M. Wein, Interactive skeleton techniques for enhancing motion dynamics in key frame animation, Communications of the ACM 19(10), 564-569, 1976
    locator: the whole paper (key frames as drawings on skeletons, and the interpolation of the skeletons)
  - paper: doi:10.1145/800031.808575
    title: Doris H. U. Kochanek and Richard H. Bartels, Interpolating splines with local tension, continuity, and bias control, Computer Graphics (Proceedings of SIGGRAPH 1984) 18(3), 33-41, 1984
    locator: the whole paper (cubic interpolating splines for key frame animation, with three shape parameters per key)
  - paper: doi:10.1145/325165.325242
    title: Ken Shoemake, Animating rotation with quaternion curves, Computer Graphics (Proceedings of SIGGRAPH 1985) 19(3), 245-254, 1985
    locator: the whole paper (the interpolation of orientation keys with quaternions, and the failure of Euler angle interpolation)
  - paper: doi:10.1145/325334.325243
    title: Scott N. Steketee and Norman I. Badler, Parametric keyframe interpolation incorporating kinetic adjustment and phrasing control, Computer Graphics (Proceedings of SIGGRAPH 1985) 19(3), 255-262, 1985
    locator: the whole paper (separate splines for the values of the keys and for their timing)
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: "Chapter 3 (interpolating values: curves, speed control and orientations) and Chapter 4, Section 4.1 (key-frame systems)"
---

Keyframe interpolation is the problem at the center of key frame animation.
An animator sets the values of the parameters of a scene, such as a joint angle, a position or an orientation, at a few key times.
The computer must then fill in the values at every frame between the keys.
The result must pass through the keys, it must be smooth enough to look natural, and it must not add motion that the animator did not ask for.
In traditional animation, assistants drew these frames by hand, and the word in-betweening comes from that work.

## In plain words

An animator tells the computer where things are at a few moments, for example where a ball is at the start, at the top of its bounce and at the end.
The computer must decide where the ball is at all the moments in between.
The simplest answer joins the keys with straight lines, but then the ball changes speed with a jerk at each key.
Smoother answers use curves that bend through the keys.
Turns of a body need their own methods, because angles wrap around and the order of turns matters.
A good method also lets the animator say how fast the motion goes, apart from where it goes.

## Definition

The input is a sequence of keys $(t_0, v_0), (t_1, v_1), \dots, (t_{n-1}, v_{n-1})$ with $t_0 < t_1 < \dots < t_{n-1}$.
Each value $v_i$ is a point of a space $M$: the real line for one channel, $\mathbb{R}^3$ for a position, or the rotation group SO(3), with unit quaternions as coordinates, for an orientation.
Some systems also take a tangent or a shape parameter at each key.

The output is a function $v : [t_0, t_{n-1}] \to M$ with $v(t_i) = v_i$ for each key, evaluated at the frame times $t_0 + k/f$ for a frame rate $f$.
The usual quality goals are:

- **Continuity.** $v$ is $C^0$, $C^1$ or $C^2$ in $t$. $C^1$ means no jump in the velocity, $C^2$ no jump in the acceleration.
- **Local control.** A change of one key changes $v$ only near that key.
- **No overshoot.** Between two equal keys, the value stays at the key value, if the animator asks for this.
- **Independence of coordinates.** For positions and rotations, the result does not depend on the choice of the world frame.

The cost model is the real RAM.
The cost has two parts: a build step once per set of keys, and an evaluation per frame and per channel.

## Variants

- **Interpolating or approximating.** An interpolating curve passes through every key. An approximating curve, such as a [B-spline](/b-spline/), only follows the keys as control points, and it is smoother for the same degree.
- **Step keys.** The value holds until the next key. Animators use this to block out the poses of a shot before they ask for in-betweens.
- **Keys with tangents.** The animator sets a tangent or a handle at each key, as in the [Hermite spline](/hermite-spline/) and in the curve editors of animation software.
- **Rotations.** The values lie on SO(3), or on the unit sphere of quaternions, and the methods use the group structure instead of coordinates.
- **Path and timing apart.** The keys fix a path in space, and a separate curve fixes the distance along the path as a function of time. This needs an [arc length table](/arc-length-table/) or an [arc length parametrization](/arc-length-parametrization/), and an [ease curve](/ease-in-ease-out/).
- **Shapes and images.** Each key is a whole shape or image, and the problem becomes morphing, as in [Beier-Neely morphing](/beier-neely-morphing/) and [as-rigid-as-possible shape interpolation](/as-rigid-as-possible-shape-interpolation/).

## Examples

Take one channel with the keys $(0, 0)$, $(1, 1)$, $(2, 1)$ and $(3, 0)$, and evaluate at $t = 1.5$.

- Linear interpolation gives $1$, the value of the two keys around $t = 1.5$.
- The [Catmull-Rom spline](/catmull-rom-spline/) sets the tangent at key 1 to $(v_2 - v_0)/2 = 0.5$ and at key 2 to $(v_3 - v_1)/2 = -0.5$. The cubic Hermite basis at $s = 0.5$ is $h_{00} = 0.5$, $h_{10} = 0.125$, $h_{01} = 0.5$ and $h_{11} = -0.125$, so the value is $0.5 + 0.0625 + 0.5 + 0.0625 = 1.125$.

The smooth curve rises above both keys, so the object floats up between two equal keys.
This overshoot is the reason for the tension parameter of the [Kochanek-Bartels spline](/kochanek-bartels-spline/): with tension 1 the tangents are 0 and the value at $t = 1.5$ is 1.

Interpolating Euler angles per channel fails on rotations.
Take a yaw angle with the keys 170 degrees and $-170$ degrees, which differ by 20 degrees.
The midpoint per channel is 0 degrees, so the body turns 170 degrees back and then 170 degrees forward, through 340 degrees in all.
[Slerp](/spherical-linear-interpolation/) of the two quaternions gives 180 degrees, halfway along the short turn of 20 degrees.
With three angles the per-channel curve also depends on the order of the axes, and near [gimbal lock](/gimbal-lock/) a small change of the keys swings the angles wildly.

## Known algorithms

For one channel or for positions:

- **Linear interpolation.** $C^0$, local, no overshoot. The velocity jumps at each key.
- **Cubic Hermite interpolation** with given tangents ([Hermite spline](/hermite-spline/), [cubic Hermite spline](/cubic-hermite-spline/)). $C^1$ and local.
- **[Catmull-Rom spline](/catmull-rom-spline/).** A Hermite spline whose tangents come from the neighbour keys. $C^1$, local, and it can overshoot.
- **[Kochanek-Bartels spline](/kochanek-bartels-spline/).** Catmull-Rom with tension, continuity and bias per key (Kochanek and Bartels 1984).
- **[Natural cubic spline](/natural-cubic-spline/).** $C^2$ and interpolating, but each value depends on all the keys.
- **[B-spline](/b-spline/).** $C^2$ and local for cubics, but it does not pass through the keys.

For orientations:

- **[Spherical linear interpolation](/spherical-linear-interpolation/)** per segment (Shoemake 1985). Constant angular speed in each segment, with a jump of the angular velocity at the keys.
- **[Squad](/squad/).** Three nested slerps per segment, $C^1$ and interpolating.
- **[Cumulative B-spline quaternion curve](/cumulative-b-spline-quaternion-curve/).** $C^2$ on the unit sphere, approximating.

For timing:

- **[Ease-in and ease-out](/ease-in-ease-out/)** curves and the [time scaling](/time-scaling/) of robotics change the speed along a fixed path.
- **[Arc length tables](/arc-length-table/)** give the curve parameter for a wanted distance along the path.
- Steketee and Badler (1985) proposed a second spline for the timing of the keys, apart from the spline of their values.

## Bounds

- **Evaluation.** For a local cubic scheme, one value costs $O(1)$ per channel after the segment is known. Finding the segment of a time costs $O(\log n)$ by [binary search](/binary-search/), or $O(1)$ amortized when the frames come in time order.
- **Build.** Catmull-Rom and Kochanek-Bartels tangents cost $O(n)$. The natural cubic spline needs one tridiagonal solve, also $O(n)$.
- **Smoothness against locality.** A $C^2$ cubic spline that interpolates the keys is fixed by the keys and two end conditions, so a change of one key moves every segment. For uniform keys the effect decays by about the factor $2 - \sqrt3 \approx 0.268$ per key. Local cubic interpolants, such as Catmull-Rom, are only $C^1$.
- **Rotations.** A single slerp segment is the shortest path between two orientations. A smooth curve through three or more keys that are not on one great circle must leave these arcs.

## Reductions

- Positions and other vector values reduce to one scalar problem per coordinate, because the linear schemes act on each coordinate apart and commute with affine maps.
- Orientations do not reduce in this way. Interpolating quaternion components and then normalizing gives a curve on the sphere, but its speed and its shape depend on the scheme. The methods of the rotation list work on the sphere directly.
- Timing control reduces to the composition $v(s(t))$ of a path $v$ with a monotone reparametrization $s$, so the shape of the path and its timing are separate problems.

## Applications

- The joint angles and the root motion of a character in [skeletal animation](/skeletal-animation/), and the inputs of [motion blending](/motion-blending/).
- Camera paths and camera orientations.
- Light, color and material parameters that change over a shot.
- Shape keys and morph targets, where each key is a mesh.

Burtnyk and Wein (1976) used skeletons to control the in-betweens of key drawings, in an early interactive system for computer-aided key frame animation.
The [principles of traditional animation](/principles-of-animation/), such as slow in and slow out and arcs, describe what a good in-between looks like.

## References
