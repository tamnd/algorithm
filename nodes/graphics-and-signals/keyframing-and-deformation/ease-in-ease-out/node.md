---
tag: M1V8Y9
kind: technique
slug: ease-in-ease-out
name: Ease-in and ease-out
aliases:
- easing curves
- slow in and slow out
area: graphics-and-signals/keyframing-and-deformation
level: intro
summary: Reparametrize time with a monotone curve, such as a sine or a cubic, so that a motion starts from rest, speeds up, and slows down into rest at the next key.
model: real-ram
complexity:
  vars: {k: "the number of frames evaluated"}
  time: {worst: "Θ(k)"}
  space: {extra: "Θ(1)"}
prereqs: [keyframe-interpolation]
see_also: [arc-length-table, arc-length-parametrization, time-scaling, hermite-spline, principles-of-animation, kochanek-bartels-spline, spherical-linear-interpolation]
sources:
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: "Chapter 3, Section 3.2 (controlling the motion of a point along a curve: the sine ease curve, the sine curve with a constant speed part, and constant acceleration)"
  - paper: doi:10.1145/325334.325243
    title: Scott N. Steketee and Norman I. Badler, Parametric keyframe interpolation incorporating kinetic adjustment and phrasing control, Computer Graphics (Proceedings of SIGGRAPH 1985) 19(3), 255-262, 1985
    locator: the whole paper (a separate spline for the timing of the keys)
  - book: isbn:9780896592322
    title: Frank Thomas and Ollie Johnston, Disney Animation, The Illusion of Life, Abbeville Press, New York, 1981
    locator: Chapter 3, The Principles of Animation (slow in and slow out)
---

Ease-in and ease-out shapes the timing of a motion.
A path or an interpolation goes from a start value to an end value as a parameter $s$ goes from 0 to 1.
Instead of $s = t$, the technique uses $s = e(t)$ for a monotone curve $e$ with $e(0) = 0$, $e(1) = 1$ and $e'(0) = e'(1) = 0$.
The motion then starts from rest, speeds up, and comes to rest at the end.
This is the principle of slow in and slow out of traditional animation in a computable form.

## In plain words

A real object does not jump from standing still to full speed.
It speeds up at the start and slows down at the end.
If you move an object between two keys at a steady pace, it starts and stops with a jolt.
An ease curve fixes this.
It takes the clock time and returns how far along the path the object should be.
Near the start and the end, the curve is flat, so the object moves slowly there.
In the middle, the curve is steep, so the object moves faster to make up the time.
The path stays the same; only the timing changes.

## When it applies

- A value moves between two keys, and it should be at rest at both keys: a camera move that starts and stops, a door that opens, a fade.
- A path is given, and the motion along it should start and stop smoothly. Then $e(t)$ is the fraction of the arc length, and an [arc length table](/arc-length-table/) turns it into the curve parameter.
- A [keyframe interpolation](/keyframe-interpolation/) through many keys is too uniform in speed, and the animator wants to accent some keys with a hold.

It does not apply when the motion must keep its speed through a key, as in a cycle or a moving hold, because an ease curve forces the speed to 0 at each end.

## The template

1. Normalize the time of the segment: $t = (T - T_a)/(T_b - T_a)$ for a clock time $T$ between the keys at $T_a$ and $T_b$.
2. Choose an ease curve $e$ and compute $s = e(t)$.
3. If $s$ is the fraction of the distance along a path of length $L$, find the curve parameter $u$ with arc length $sL$ from an [arc length table](/arc-length-table/). Otherwise use $s$ directly as the interpolation parameter.
4. Evaluate the path or the interpolation at that parameter.

The three common curves are these.

```pseudo id=template
EASE(t)                                          ▷ t is the normalized time
L1  t ← min(max(t, 0), 1)
L2  sine: return (sin(πt - π/2) + 1) / 2
L3  cubic: return 3t² - 2t³
L4  constant acceleration with ramps [0, t₁] and [t₂, 1]: v₀ ← 2 / (1 + t₂ - t₁)
L5  if t < t₁ then return v₀ t² / (2t₁)
L6  if t ≤ t₂ then return v₀ t₁ / 2 + v₀ (t - t₁)
L7  d ← t - t₂; return v₀ t₁ / 2 + v₀ (t₂ - t₁) + v₀ d (1 - d / (2(1 - t₂)))
```

Line L2 is half a period of a sine, shifted to run from 0 to 1. Its speed is $\frac\pi2 \sin(\pi t)$, with the peak $\pi/2 \approx 1.571$ at $t = \frac12$.
Line L3 is the cubic Hermite segment with zero tangents, often called smoothstep. Its speed is $6t(1 - t)$, with the peak $1.5$.
Lines L4 to L7 are the constant acceleration profile: the speed grows linearly from 0 to $v_0$ on $[0, t_1]$, stays at $v_0$, and falls linearly to 0 on $[t_2, 1]$. The area under the speed is $v_0(1 + t_2 - t_1)/2$, and the choice of $v_0$ in line L4 makes it 1.

Each curve is monotone, maps $[0, 1]$ onto $[0, 1]$, and has zero slope at both ends.
For the sine and the cubic this follows from $\sin(\pi t) \ge 0$ and $6t(1 - t) \ge 0$ on $[0, 1]$.
For the constant acceleration profile the speed is a trapezoid that is not negative and has area 1.
These are proved properties of the formulas.
Which curve looks right is a matter of taste.

## Classic examples

- **Move between two keys.** With $a = (0, 2)$, $b = (4, 6)$ and the cubic, the point at $t = 0.25$ is $a + 0.15625\,(b - a) = (0.625, 2.625)$. Without easing it would be $(1, 3)$.
- **Values at $t = 0.25$.** The sine curve gives $0.14645$, the cubic $0.15625$, and the constant acceleration curve with $t_1 = 0.2$, $t_2 = 0.8$ gives $0.1875$. All three give $0.5$ at $t = 0.5$, by symmetry.
- **The constant acceleration check.** With $t_1 = 0.2$ and $t_2 = 0.8$, $v_0 = 1.25$, the acceleration is $v_0/t_1 = 6.25$, and the distance at $t = 0.2$ is $0.125$.
- **A move along a path.** A camera dolly along a [Catmull-Rom](/catmull-rom-spline/) path of length 10 at the time $t = 0.25$ with the cubic goes to the arc length $1.5625$. The arc length table gives the curve parameter, and the path gives the position.
- **Rotations.** The same curve times a [slerp](/spherical-linear-interpolation/): $\operatorname{slerp}(q_a, q_b, e(t))$ turns about a fixed axis, from rest to rest.

## Variations

- **Ease-in only or ease-out only.** Use the first half of a curve, scaled to $[0, 1]$, for example $e(t) = 1 - \cos(\pi t/2)$ for ease-in. The speed is 0 at one end only.
- **Sine with a constant speed part.** Parent (2012) joins two quarter periods of a sine with a straight middle part, so the curve has a phase of constant speed, as in lines L4 to L7.
- **Higher order.** The quintic $6t^5 - 15t^4 + 10t^3$ also has zero acceleration at both ends, so the acceleration has no jump when the motion starts. The [time scaling](/time-scaling/) of robotics uses the same cubic and quintic polynomials.
- **Many keys.** An animator edits the timing curve of a whole shot as a spline of time against distance, and the speed may stay above 0 at the inner keys. Steketee and Badler (1985) used a second spline for this timing.
- **Tension at the keys.** The tension of the [Kochanek-Bartels spline](/kochanek-bartels-spline/) slows the motion near a key without a separate timing curve, but it also changes the path.
- **Overshoot curves.** Interface toolkits add curves that pass beyond 1 and come back, or bounce. These are not monotone, so they are not easing in the sense of this page.

## Pitfalls

- **Easing the curve parameter instead of the distance.** If the path parameter $u$ does not grow with arc length, $e(t)$ applied to $u$ gives a speed that also depends on the spacing of the control points. Use an arc length table first.
- **A higher peak speed.** The motion takes the same time, so it must move faster in the middle: $1.571$ times the mean speed for the sine, $1.5$ for the cubic, and $v_0$ for the constant acceleration curve. A short ramp needs a large acceleration.
- **Stops at every key.** Easing each segment of a many-key motion makes the object stop at each key. This is the right result only for holds.
- **A jump in the acceleration.** The sine and the cubic start with a nonzero acceleration, $\pi^2/2$ and 6. For physical devices, use the quintic or a jerk-limited profile.
- **Times outside $[0, 1]$.** Clamp $t$, as in line L1, or the cubic returns values outside $[0, 1]$.

## Exercises

1. Show that the sine curve and the cubic differ by at most $0.0101$ on $[0, 1]$. (Hint: the difference is $0.0098$ at $t = 0.25$, and its maximum is near $t = 0.279$ and $t = 0.721$.)
2. Find $v_0$ and the distance at $t = t_1$ of the constant acceleration curve with $t_1 = 0.1$ and $t_2 = 0.7$. (Answer: $v_0 = 2/1.6 = 1.25$ and $0.0625$.)
3. Show that a cubic $e$ with $e(0) = 0$, $e(1) = 1$ and $e'(0) = e'(1) = 0$ is unique, and that it is $3t^2 - 2t^3$.
4. Compose the cubic with itself, $e(e(t))$. Is the result still an ease curve? What is its peak speed?

## References
