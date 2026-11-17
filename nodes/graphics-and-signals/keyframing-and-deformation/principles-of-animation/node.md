---
tag: ZNV1VX
kind: concept
slug: principles-of-animation
name: Principles of traditional animation
aliases:
- twelve principles of animation
- squash and stretch
area: graphics-and-signals/keyframing-and-deformation
level: intro
summary: The rules of hand-drawn animation, such as squash and stretch, anticipation, timing and slow in and slow out, carried over to computer animation.
see_also: [keyframe-interpolation, ease-in-ease-out, arc-length-table, kochanek-bartels-spline, spacetime-constraints, motion-signal-processing, motion-warping, skeletal-animation]
sources:
  - book: isbn:9780896592322
    title: "Frank Thomas and Ollie Johnston, Disney Animation: The Illusion of Life, Abbeville Press, 1981"
    locator: "Chapter 3, The Principles of Animation, which starts on page 47"
  - paper: doi:10.1145/37401.37407
    title: "John Lasseter, Principles of traditional animation applied to 3D computer animation, SIGGRAPH 87, Computer Graphics 21(4), 35-44, 1987"
    locator: the whole paper (each principle, its meaning in hand-drawn animation, and its use with 3D keyframe tools)
---

The principles of traditional animation are twelve rules of the craft that the animators of the Walt Disney studio worked out in the 1930s to make drawn characters look alive, heavy and clear.
Frank Thomas and Ollie Johnston, two of those animators, wrote them down in their book *The Illusion of Life* (1981).
John Lasseter (1987) explained what they mean for 3D computer animation, where a program makes the in-between frames from the key poses.
Several of the principles became features of animation software: slow in and slow out became [ease curves](/ease-in-ease-out/), arcs became spline paths, and squash and stretch became a scale that keeps the volume.
The others are about acting, design and composition, and no algorithm replaces them.

## In plain words

A drawing that moves from one place to another at an even speed looks like a machine.
Real things speed up and slow down, bend when they hit something, and move a little the other way before a big action.
The animators at Disney noticed these effects and turned them into rules for drawing.
A ball squashes when it lands and stretches when it falls fast.
A person bends the knees before a jump.
A tail keeps swinging after the dog stops.
Most motions follow curves, not straight lines.
The number of frames for an action tells the viewer how heavy and how fast something is.
Computer animation programs make the frames between key poses for you.
The rules tell you how to set the key poses and the timing so that the result looks alive.

## The idea

The twelve principles, in the order of Thomas and Johnston, are these.

1. **Squash and stretch.** A soft object flattens on impact and lengthens when it moves fast, but its volume stays the same, so that it looks solid and not like rubber that grows and shrinks.
2. **Anticipation.** A small move in the opposite direction prepares the viewer for the main action, like the wind-up before a throw.
3. **Staging.** Each pose and each shot shows one idea clearly, with a readable silhouette and a camera that points the eye to it.
4. **Straight ahead action and pose to pose.** Straight ahead animation draws frame after frame in order. Pose to pose animation first draws the key poses and then fills in the frames between them, which is the method of keyframe software.
5. **Follow through and overlapping action.** Loose parts, such as hair, clothes and tails, keep moving after the body stops, and the parts of a body do not start and stop at the same time.
6. **Slow in and slow out.** More frames go near the extreme poses and fewer in the middle, so the motion eases out of one pose and into the next.
7. **Arcs.** Most natural motions, such as a swinging arm or a turning head, follow curved paths.
8. **Secondary action.** A smaller action supports the main one, such as a gesture of the hands or a change of expression during a walk.
9. **Timing.** The number of frames for an action sets its speed, and with it the weight, the size and the mood that the viewer sees.
10. **Exaggeration.** A motion is pushed further than reality to make its idea read clearly, without losing its believability.
11. **Solid drawing.** The forms have weight, depth and balance in three dimensions.
12. **Appeal.** A character has a design and a personality that the audience wants to watch, whether it is a hero or a villain.

The principles are not laws of physics and they are not an algorithm.
They describe how viewers read weight, intent and life from motion, and a good animator breaks them on purpose.
In computer animation, some of them map to tools.
Pose to pose is [keyframe interpolation](/keyframe-interpolation/).
Slow in and slow out is the shape of the curve that maps time to the interpolation parameter, or to the distance along a path through an [arc length table](/arc-length-table/).
Arcs come from spline paths and from rotating joints instead of moving points in straight lines.
Squash and stretch is a scale along the direction of motion, with the opposite scale across it.
Follow through and overlapping action come from offsets of the keys of different parts, or from simulation of the loose parts.
Anticipation, staging, exaggeration and appeal are choices of the animator, which the software only makes easier to edit.

## Examples

**A bouncing ball.** This is the first exercise of most animation courses, and it shows timing, slow in and slow out, arcs and squash and stretch at once.
Under gravity, a ball that falls from rest covers distances in the ratio $1 : 3 : 5 : 7 : \dots$ in equal frames, because the distance fallen after $k$ frames is proportional to $k^2$.
So the drawings are close together near the top of the bounce and far apart near the floor, which is slow in and slow out produced by physics.
A drop of 1 metre takes $\sqrt{2/9.81} = 0.452$ seconds, about 11 frames at 24 frames per second, so a full bounce of that height takes about 22 frames.
The path between two contacts is a parabola, an arc.
At the contact the ball squashes, and just before and after it the ball stretches along the motion.

**Volume in squash and stretch.** If the ball is stretched by the factor $\lambda$ along its motion and scaled by $\mu$ in the two other directions, its volume stays the same when $\lambda\mu^2 = 1$.
A stretch by $\lambda = 1.5$ then needs $\mu = 1/\sqrt{1.5} = 0.816$ across the motion.
In a 2D drawing, area is kept with $\mu = 1/\lambda$.

**Anticipation in a jump.** Before a character jumps, it crouches, which moves its centre of mass down, the opposite way of the jump.
Without the crouch, the jump looks as if an outside force lifted the character.

**Linear interpolation breaks two principles.** Linear interpolation between two keys moves at a constant speed with a sudden start and stop, so it has no slow in and slow out, and between three keys it gives straight pieces with a corner, so it has no arcs.
A [Kochanek-Bartels spline](/kochanek-bartels-spline/) with an ease curve on each key fixes both.

**Overlapping action of a tail.** If the keys of each joint of a tail are the keys of the joint before it, delayed by one or two frames, the tail waves behind the body.

## Where it is used

- **Keyframe animation software.** Graph editors, tangent types of key curves and the ease controls of [keyframe interpolation](/keyframe-interpolation/) and [ease-in-ease-out](/ease-in-ease-out/) implement slow in and slow out, arcs and timing.
- **Character rigs.** Rigs for [skeletal animation](/skeletal-animation/) include squash and stretch controls that scale a bone and its skin along its length and keep the volume.
- **Physics-based animation.** In [spacetime constraints](/spacetime-constraints/), anticipation, follow through and squash and stretch come out of an optimization of a physical motion, without being keyed.
- **Motion editing.** [Motion signal processing](/motion-signal-processing/) exaggerates a captured motion by amplifying some of its frequency bands, and [motion warping](/motion-warping/) changes the timing and the poses of a captured motion.
- **Teaching and critique.** Animation courses and reviews of animation use the principles as a common vocabulary.
- **User interfaces.** Animated transitions of user interfaces use easing, anticipation and follow through to make changes of the screen easy to follow.

## References
