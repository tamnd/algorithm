---
tag: 7QR9V6
kind: algorithm
slug: motion-warping
name: Motion warping
aliases:
- motion displacement mapping
area: graphics-and-signals/character-animation
level: core
summary: Edit a captured motion by adding a smooth displacement curve that meets new keyframe constraints while keeping the high-frequency detail.
model: real-ram
complexity:
  vars: {f: the number of frames, m: the number of keys in a channel, j: the number of channels}
  time: {warp: O(j (m + f log m))}
  space: {extra: O(j (f + m))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1995
  people: [Andrew Witkin, Zoran Popović]
  note: "Witkin and Popović presented motion warping at SIGGRAPH 95. At the same conference Bruderlin and Williams presented the same displacement idea under the name motion displacement mapping."
prereqs: [keyframe-interpolation, skeletal-animation]
see_also: [motion-signal-processing, natural-cubic-spline, cubic-spline-interpolation, thomas-algorithm, motion-blending, registration-curves, footskate-cleanup, spacetime-constraints]
sources:
  - paper: doi:10.1145/218380.218422
    title: "Andrew Witkin and Zoran Popović, Motion warping, SIGGRAPH 95, 1995, 105 to 108"
    locator: "the warp of a channel by a scale curve and an offset curve through keyframes, and the time warp"
  - paper: doi:10.1145/218380.218421
    title: "Armin Bruderlin and Lance Williams, Motion signal processing, SIGGRAPH 95, 1995, 97 to 104"
    locator: the section on motion displacement mapping
  - book: isbn:9780124158429
    title: "Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012"
    locator: the material on the processing of motion capture data
---

Motion warping changes a captured motion so that it meets a few new key poses, and keeps all the small detail of the capture.
Each joint channel $\theta(t)$ becomes

$$\theta'(t) = c(t)\, \theta(g(t)) + b(t),$$

where $g$ is a time warp, $c$ is a smooth scale curve and $b$ is a smooth offset curve.
The animator sets keys $(t_k, v_k)$ where the new channel must have the value $v_k$.
With $c$ fixed, each key gives one offset $\beta_k = v_k - c(t_k)\, \theta(g(t_k))$, and $b$ is a spline through the offsets.
Because $b$ is smooth and only adds to $\theta$, the high frequency parts of the capture (the small shakes, the impact of a foot) stay as they were; only a slow change is added.
The cost is $O(m)$ for the spline of $m$ keys and $O(f \log m)$ to evaluate it on $f$ frames, for each channel.

## In plain words

You have a captured motion of a person who reaches for a cup.
Now the cup is 10 cm higher.
You do not want to animate the arm again by hand, because you would lose all the small life of the real motion.
So you say only: at this moment, the shoulder must be raised a bit more.
The method computes a smooth correction that is zero far away and grows to the needed amount at that moment.
It adds the correction to the captured motion.
The small movements of the original are still there, on top of the slow correction.

## The problem

The input is one or more channels, each a list of samples $\theta_0, \dots, \theta_{f-1}$ at the frames $0, \dots, f - 1$ (a joint angle, a root coordinate), a list of keys $(t_1, v_1), \dots, (t_m, v_m)$ with $t_1 < \dots < t_m$ for each channel, an optional scale curve $c$, and an optional time warp $g$.
The output is a new channel $\theta'$ with $\theta'(t_k) = v_k$ for every key, as smooth as the input between the keys, and equal to $c \cdot (\theta \circ g)$ when every key already holds.

The time warp maps new time to original time.
It is given by pairs $(t'_l, t_l)$ with both lists increasing: the new motion reaches original time $t_l$ at new time $t'_l$.
Between the pairs $g$ is linear, and outside them it has slope 1.
So the warp can slow down or speed up parts of a motion, for example to make a jump wait for a moving platform.

## The algorithm

```pseudo id=main
MOTION-WARP(θ, keys, c, g)                    ▷ samples, keys (tₖ, vₖ), scale, time warp
L1  src(t) ← θ(g(t))                          ▷ the original, read at the warped time
L2  βₖ ← vₖ - c(tₖ) · src(tₖ) for every key   ▷ the offset needed at each key
L3  b ← the natural cubic spline through (tₖ, βₖ), constant outside [t₁, tₘ]
L4  θ'(t) ← c(t) · src(t) + b(t)
    for every channel
L5      evaluate θ' at the new frames 0, 1, 2, ...
L6  return the new frames
```

The samples are read between frames by linear interpolation, clamped at the ends.
For rotations stored as joint angles, the method works channel by channel; for quaternion channels, the offset is a rotation and the sum is a product, an extension that the code does not cover.

Line L3 uses a [natural cubic spline](/natural-cubic-spline/): a cubic on each interval between keys, $C^2$ at the keys, with zero second derivative at the first and the last key.
Its second derivatives solve a tridiagonal system with a strictly dominant diagonal, so the [Thomas algorithm](/thomas-algorithm/) solves it in $O(m)$.
With one key, $b$ is a constant; with two, it is a line between the keys.
The original paper uses interpolating splines for $b$ and $c$; the natural spline and the constant ends are choices of the code.

## Example

Take a channel with $\theta(10) = 0.1$, $\theta(20) = 0.2$ and $\theta(30) = 0.1$, no scale, no time warp, and the keys $(10, 0.4)$, $(20, 0.7)$, $(30, 0.4)$.
Line L2 gives the offsets $\beta = (0.3, 0.5, 0.3)$.

The spline has the knot spacing $h = 10$ and one unknown second derivative $M_1$ in the middle, with $M_0 = M_2 = 0$:

$$2(h + h) M_1 = 6\left(\frac{0.3 - 0.5}{10} - \frac{0.5 - 0.3}{10}\right), \qquad 40 M_1 = -0.24, \qquad M_1 = -0.006.$$

At $t = 15$, with $A = B = 1/2$,

$$b(15) = \tfrac12 (0.3) + \tfrac12 (0.5) + \big((A^3 - A) M_0 + (B^3 - B) M_1\big) \frac{h^2}{6} = 0.4 + (-0.375)(-0.006)(16.667) = 0.4375.$$

So $\theta'(15) = \theta(15) + 0.4375$, and by symmetry $b(25) = 0.4375$.
For $t \le 10$ the offset is 0.3, and for $t \ge 30$ it is 0.3.
Whatever detail $\theta$ has between the keys, it is kept; only the smooth curve $b$ is added.

A time warp with the pairs $(0, 0)$, $(50, 40)$, $(100, 80)$ plays the first 80 frames over 100 frames; new frame 25 reads original time 20, and new frame 75 reads original time 60.

## Correctness

The proof file shows the following facts, in exact arithmetic.

- The natural spline through $m \ge 2$ keys exists and is unique, because its tridiagonal system has a strictly dominant diagonal.
- It reproduces linear data: offsets on a line give that line.
- So the warped channel meets every key, $\theta'(t_k) = v_k$ (Theorem 1).
- If every key already holds, the offset is zero and the motion is unchanged up to the scale and the time warp (Theorem 2).
- A linear change at the keys gives exactly that linear change between them (Theorem 3).
- The offset is $C^2$ between the first and the last key, so it adds no corner (Theorem 4).
- The time warp is continuous and strictly increasing and maps each pair as given (Theorem 5), so it never plays the motion backward.

That the result looks like the same actor is a visual heuristic, not a theorem.
A large offset or a strong time warp changes the dynamics: a sped up jump does not follow the same parabola in a world with the same gravity, and a raised arm can push a hand through the body.

## Complexity

For each channel, line L2 costs $O(m)$, the spline of line L3 costs $O(m)$ with the Thomas algorithm, and the evaluation of line L5 costs $O(\log m)$ per frame for the search of the interval, so $O(f \log m)$ for all frames.
For $j$ channels this is $O(j (m + f \log m))$ time and $O(j (f + m))$ space.
When the frames are evaluated in order, a moving index replaces the search and the time is $O(j (m + f))$.

## Properties

- **Exact at the keys.** Every key holds, up to rounding.
- **Local in size.** The offset depends only on the keys; between two keys it is a cubic, so far from all keys it is the end constant.
- **No change without need.** Keys that the motion already meets change nothing.
- **Detail kept.** The added curve has only the frequencies of the key spacing; the higher frequencies of the capture pass unchanged.
- **Channel by channel.** No constraint between joints is kept; for a hand or a foot at a place, use [inverse kinematics](/inverse-kinematics/) first to find the joint keys.

## Variants and improvements

- **Scale curve.** A curve $c$ through scale keys stretches the motion around zero, for example to make a gesture larger.
- **Hierarchical displacement.** Later work fits the offset with a hierarchy of B-splines, coarse first, so that keys close in time get detail and keys far apart get a smooth change.
- **Motion signal processing.** [Motion signal processing](/motion-signal-processing/) of Bruderlin and Williams edits the frequency bands of the channels; their motion displacement mapping is the same idea as motion warping, from the same conference.
- **Constraint based editing.** [Spacetime constraints](/spacetime-constraints/) and per frame [inverse kinematics](/inverse-kinematics/) solve for the change from positions of end effectors.
- **Blending.** To join two motions, warp the end of one and the start of the other to meet at a common pose, then [blend](/motion-blending/).

## When to use it

Use motion warping to fit a captured motion to a new scene with small changes: a hand that must reach a new place, a foot on a step, a jump that must last a few frames longer.
It is fast and needs only a few keys.
For large changes, or when contacts must hold over many frames, combine it with inverse kinematics and [footskate cleanup](/footskate-cleanup/), or use a method that knows about the body.

## Pitfalls

- **Keys too close.** Two keys a few frames apart with very different offsets make the spline swing far beyond both offsets between and around them.
- **Euler angles.** Warping three Euler channels of one joint independently can give an unexpected rotation, mostly near gimbal lock. Warp in a parameterization that is well behaved near the pose, or use quaternion offsets.
- **Foot contacts.** An offset on the hip or the legs moves a planted foot. Fix the contacts after the warp.
- **Time warp physics.** Slowing a fall makes it float. Keep the time warp mild in ballistic phases.
- **Ends.** Outside the key range, the code holds the end offset. Without it, a spline continued past the last key can grow without bound.

## Implementations

## History

Andrew Witkin and Zoran Popović presented motion warping at SIGGRAPH 95, with a few keyframes, a smooth warp of each channel, and a time warp, as a way to reuse captured or keyframed motion.
At the same conference, Armin Bruderlin and Lance Williams presented [motion signal processing](/motion-signal-processing/), whose motion displacement mapping is the same idea.
Later, Jehee Lee and Sung Yong Shin fitted the displacement with hierarchical B-splines and combined it with inverse kinematics.

## References
