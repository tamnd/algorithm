---
tag: 83P5FW
kind: technique
slug: motion-blending
name: Motion blending
aliases:
- motion interpolation
area: graphics-and-signals/character-animation
level: core
summary: "Combine two or more motion clips by time-aligning them, aligning their root frames, and interpolating the joint rotations frame by frame with weights."
prereqs: [spherical-linear-interpolation, skeletal-animation]
see_also: [registration-curves, verbs-and-adverbs, motion-graph, motion-matching, unit-quaternion-rotation, squad, footskate-cleanup, dynamic-time-warping]
sources:
  - paper: doi:10.1145/325165.325242
    title: "Ken Shoemake, Animating rotation with quaternion curves, SIGGRAPH 85 (Computer Graphics 19(3)), 1985, 245 to 254"
    locator: spherical linear interpolation of unit quaternions
  - paper: doi:10.2312/SCA03/214-224
    title: "Lucas Kovar and Michael Gleicher, Flexible automatic motion blending with registration curves, ACM SIGGRAPH/Eurographics Symposium on Computer Animation, 2003, 214 to 224"
    locator: "the failures of a direct frame by frame blend, and the timewarp, coordinate alignment and constraint matching that fix them"
  - paper: doi:10.1109/38.708559
    title: "Charles Rose, Michael F. Cohen and Bobby Bodenheimer, Verbs and adverbs, multidimensional motion interpolation, IEEE Computer Graphics and Applications 18(5), 1998, 32 to 40"
    locator: blending of many time aligned examples with weights from a parameter space
  - book: isbn:9780124158429
    title: "Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012"
    locator: the material on motion capture data and its processing
---

Motion blending makes a new motion from two or more clips of the same kind of action, for example a slow walk and a fast walk, or a walk that turns left and one that turns right.
Each clip gets a weight, the weights sum to 1, and every frame of the result is a weighted mix of matching frames of the inputs.
The mix is made in three steps: match the timing of the clips, align their positions and headings on the ground, and interpolate each joint rotation with [slerp](/spherical-linear-interpolation/) or a normalized quaternion mean.
Without the first two steps the result looks wrong even when every input is good: legs cross, feet slide, and the character drifts sideways.
Blending is the common base of [registration curves](/registration-curves/), [verbs and adverbs](/verbs-and-adverbs/), the transitions of a [motion graph](/motion-graph/), and the cross fades of [motion matching](/motion-matching/).

## In plain words

Think of two films of a person walking, one slow and one fast.
You want a walk at a speed in between.
You cannot mix frame 10 of one film with frame 10 of the other, because at that time one person has the left foot forward and the other the right foot.
First you stretch the films so that the steps happen at the same moments.
Then you turn and move one film so that both people face the same way and stand at the same place.
Only then do you mix each joint, half of one bend and half of the other.
The weights say how much of each film you take.

## When it applies

The technique applies when the clips show the same action with the same structure: the same skeleton, the same contacts in the same order, and poses that are close at matching times.
A walk and a run blend well, because both have the same alternation of left and right steps.
A walk and a jump do not, because no time warp makes their contacts match.

The input is $m$ clips with $j$ joints each, the joint rotations as unit quaternions (Hamilton convention, scalar first), the root position and heading per frame, and weights $w_1, \dots, w_m \ge 0$ with $\sum_k w_k = 1$.
The output is one clip on the same skeleton.
The result of the joint interpolation is a property of the rotation math; whether the blend looks good is a visual judgment, and the weights are a control of the user.

## The template

1. **Time alignment.** Map every clip to a common normalized time $u \in [0, 1]$ in which the key events (foot strikes) happen at the same $u$. For cyclic clips with one cycle each, $u = t / T_k$ for the cycle length $T_k$ of clip $k$. For general clips, use a [registration curve](/registration-curves/) time warp, built by [dynamic time warping](/dynamic-time-warping/) of the frame distances. The blended clip has the length $\sum_k w_k T_k$, so a frame at blended time $t$ reads every clip at its own time $u T_k$.
2. **Root alignment.** Express each clip relative to a common ground frame: remove the start position and the start heading of each root, or align each clip to the first one with the best rotation about the vertical axis and the best translation in the ground plane. Blend the root velocity and the turning rate rather than the absolute root position, and integrate them again.
3. **Sign alignment.** A unit quaternion $q$ and $-q$ give the same rotation. For each joint, flip the sign of the inputs so that each has a nonnegative dot product with the first input. Otherwise the interpolation can take the long way around.
4. **Joint interpolation.** For two clips, the joint rotation is $\text{slerp}(q_1, q_2, w_2)$, where $\text{slerp}(q_1, q_2, t) = \frac{\sin((1 - t)\Omega)}{\sin\Omega} q_1 + \frac{\sin(t\Omega)}{\sin\Omega} q_2$ with $\cos\Omega = q_1 \cdot q_2$. For more clips, take the normalized weighted sum $\sum_k w_k q_k / |\sum_k w_k q_k|$ after the sign alignment, or apply slerp one clip at a time.
5. **Constraints.** Mark the foot plants of the inputs, carry them through the time warp, and fix the planted feet in the result with [footskate cleanup](/footskate-cleanup/) or [inverse kinematics](/inverse-kinematics/).

The cost per blended frame is $O(m j)$: one interpolation per joint and clip, plus the root.
Building the time warp of step 1 is the expensive part when it uses dynamic time warping, $O(f_1 f_2)$ distance evaluations for two clips of $f_1$ and $f_2$ frames.

## Classic examples

**A joint rotation.**
Blend the identity $q_1 = (1, 0, 0, 0)$ and $q_2 = (0.70711, 0, 0, 0.70711)$, a rotation by $\pi/2$ about $z$, with $w_2 = 0.5$.
Then $\cos\Omega = 0.70711$, $\Omega = \pi/4$, and slerp gives $(0.92388, 0, 0, 0.38268)$, a rotation by $\pi/4$.
The normalized sum $(q_1 + q_2)/|q_1 + q_2|$ gives the same quaternion at this weight.
At $w_2 = 0.25$, slerp gives $(0.98079, 0, 0, 0.19509)$, a rotation by $\pi/8 = 0.392699$, while the normalized sum gives a rotation by $0.376959$.
So the normalized sum does not move at a constant rate; for blending, where the weight is not a time, this is often acceptable.

**The sign.**
Take $q_2' = -q_2 = (-0.70711, 0, 0, -0.70711)$, the same rotation as $q_2$.
Without the sign step, $q_1 \cdot q_2' < 0$, and slerp goes through $(0.38268, 0, 0, -0.92388)$ at $w_2 = 0.5$, a rotation by $-3\pi/4$ instead of $\pi/4$.
After the flip, the result is again a rotation by $\pi/4$.

**Two walk cycles.**
A slow walk has a cycle of 45 frames and a fast walk a cycle of 30 frames at 30 frames per second.
With $w = 0.5$ the blended cycle has $0.5 \cdot 45 + 0.5 \cdot 30 = 37.5$ frames.
Blended frame 15 is at $u = 15 / 37.5 = 0.4$, so it reads frame 18 of the slow walk and frame 12 of the fast walk.
Reading frame 15 of both instead would mix the slow walk at $u = 0.33$ with the fast walk at $u = 0.5$, where the fast walk already has the other foot forward.

## Variations

- **Multiway blends.** [Verbs and adverbs](/verbs-and-adverbs/) computes the weights from a point in a parameter space (speed, turn, mood) by radial basis functions plus a linear term, and blends many examples.
- **Registration curves.** [Registration curves](/registration-curves/) build the time warp, the alignment and the constraint matches automatically, and handle clips with different timing in different parts.
- **Transitions.** A transition from one clip to another is a blend whose weight goes from 1 to 0 over a short window, with a smooth curve such as $2s^3 - 3s^2 + 1$; this is how a [motion graph](/motion-graph/) joins clips.
- **Inertialization.** Game engines often replace a cross fade by an offset that starts at the difference of the two poses and decays to zero, so that only the new clip is evaluated. This is an engineering choice; it is not covered by a source here.
- **Additive layers.** A clip of differences to a reference pose (a lean, a breath) is added on top of a base motion instead of mixed with it.

## Pitfalls

- **No time alignment.** Mixing frames at the same clock time blends different phases of the step, and the feet slide or cross.
- **Euler angles.** Mixing [Euler angles](/euler-angles/) channel by channel can give poses that are in neither input, and fails near gimbal lock. Interpolate quaternions.
- **Absolute root positions.** Two walks that start at different places or go in different directions blend to a root that moves between the two paths, slower than the legs step, so the feet slide. Blend in a common ground frame, and blend velocities, not positions.
- **Lost contacts.** A blend of two planted feet at different places is a foot between them that moves while it should be still. Fix contacts after the blend.
- **Dissimilar clips.** If the poses at matching times are far apart, the blend can pass through poses that are not valid, such as a leg through the floor. No weight fixes this; choose clips that are close.
- **The name.** "Motion interpolation" also names the method of [verbs and adverbs](/verbs-and-adverbs/), which interpolates over a parameter space, not only between two clips.

## Exercises

1. Show that the normalized sum of $q$ and $q$ is $q$ for every weight, and that after the sign step a two clip blend does not change when the second input is replaced by its negative. *Answer:* $(w_1 q + w_2 q)/|q| = q$ because $w_1 + w_2 = 1$ and $|q| = 1$; the sign step turns $-q_2$ back into $q_2$, because $q_1 \cdot (-q_2) < 0$ exactly when $q_1 \cdot q_2 > 0$.
2. Two clips have cycles of 24 and 40 frames. For $w = 0.25$ on the first clip, give the blended cycle length and the source times of blended frame 9. *Answer:* $0.25 \cdot 24 + 0.75 \cdot 40 = 36$ frames; $u = 9/36 = 0.25$, so the sources are frame 6 of the first clip and frame 10 of the second.
3. Two walks at the speed $v$ go to the north and to the east from the same point. Give the root speed of a half and half blend of their absolute root positions, and say how to fix the blend. *Answer:* the root moves along the diagonal at $v/\sqrt 2 \approx 0.71 v$ while the legs step for $v$, so the feet slide; blend the local forward velocities (both $v$) and the turn rates (both 0), and integrate them along the blended heading.
4. Compute the angle of the normalized sum of the identity and a rotation by $\pi/2$ about $z$ at $w_2 = 0.25$. *Answer:* the sum is $(0.75 + 0.25 \cdot 0.70711, 0, 0, 0.25 \cdot 0.70711) = (0.92678, 0, 0, 0.17678)$, and the angle is $2 \operatorname{atan2}(0.17678, 0.92678) = 0.376959$, less than the slerp angle $\pi/8 = 0.392699$.

## References
