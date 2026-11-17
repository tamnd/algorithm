---
tag: EA23M6
kind: algorithm
slug: double-reflection-method
name: Double reflection method
aliases:
- double reflection rotation minimizing frame
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Approximate a rotation minimizing frame along sampled curve points by two reflections per step, with fourth-order accuracy.
model: real-ram
complexity:
  vars: {N: "the number of steps between sample points"}
  time: {worst: "Θ(N)"}
  space: {extra: "Θ(1)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
prereqs: [rotation-minimizing-frame]
see_also: [frenet-frame, sweep-surface, discrete-elastic-rods, runge-kutta-methods, catmull-rom-spline, arc-length-table, unit-quaternion-rotation]
sources:
  - paper: doi:10.1145/1330511.1330513
    title: "Wenping Wang, Bert Jüttler, Dayue Zheng and Yang Liu, Computation of rotation minimizing frames, ACM Transactions on Graphics 27(1), Article 2, 2008"
    locator: "Section 4.1 and Table I (the algorithm), Theorem 4.3 (exact on spheres and planes), Section 4.4 (degenerate cases and symmetry), Theorems 4.4 and 4.5 (local error O(h^5) and global error O(h^4))"
  - paper: doi:10.1080/00029890.1975.11993807
    title: "Richard L. Bishop, There is more than one way to frame a curve, The American Mathematical Monthly 82(3), 246-251, 1975"
    locator: the relatively parallel frame, the continuous form of the frame that the method approximates
  - paper: doi:10.1016/0167-8396(86)90039-7
    title: "Fopke Klok, Two moving coordinate frames for sweeping along a 3D trajectory, Computer Aided Geometric Design 3(3), 217-229, 1986"
    locator: the rotation minimizing frame as the solution of a differential equation, and the projection method that the double reflection method improves
---

The double reflection method computes a [rotation minimizing frame](/rotation-minimizing-frame/) along a space curve from sample points and their unit tangents.
Each step maps the frame at one point to the frame at the next point by two reflections in planes.
The first reflection takes the point $x_i$ to $x_{i+1}$, and the second one takes the reflected tangent to the true tangent $t_{i+1}$.
Wang, Jüttler, Zheng and Liu (2008) gave the method and showed that its global error is $O(h^4)$ for a step $h$, at a much lower cost than a fourth-order Runge-Kutta integration of the defining equation.
It is the standard way to frame sweep surfaces, tubes, camera paths and rods without the twist and the flips of the [Frenet frame](/frenet-frame/).

## In plain words

To move a camera or to sweep a tube along a curved path, you need a direction "up" at each point of the path.
That up direction must stay at a right angle to the path, and it must not spin about the path for no reason.
The method finds it one step at a time.
Put a mirror halfway between two neighbouring points, so that the mirror image of the first point is the second point.
Mirror the current up direction and the current path direction in it.
The mirrored path direction is usually a little off from the true one at the new point, so a second mirror moves it onto the true one.
The second mirror moves the up direction too.
Two mirrors together give a turn, and the turn is very close to the one that the ideal frame makes.

## The problem

The input is a list of points $x_0, \dots, x_N$ on a regular space curve $x(u)$, the unit tangents $t_i$ at these points, and a unit normal vector $r_0 \perp t_0$.
The output is a list of frames $(r_i, s_i, t_i)$, each a right-handed orthonormal basis with $s_i = t_i \times r_i$.
The frames must approximate the rotation minimizing frame of the curve, the solution of $r' = -(r \cdot t')\,t$ with $r(u_0) = r_0$.
The definition of the frame and its properties are on the page [rotation minimizing frame](/rotation-minimizing-frame/).

## The algorithm

For a nonzero vector $v$ with $c = v \cdot v$, the map $a \mapsto a - \frac{2}{c}(v \cdot a)\,v$ is the reflection in the plane through the origin that is perpendicular to $v$.

```pseudo id=main
DOUBLE-REFLECTION(x₀..x_N, t₀..t_N, r₀)          ▷ returns the frames (rᵢ, sᵢ, tᵢ)
L1  for i ← 0 to N - 1 do
L2      v₁ ← xᵢ₊₁ - xᵢ; c₁ ← v₁ · v₁
L3      r_L ← rᵢ - (2/c₁)(v₁ · rᵢ) v₁
L4      t_L ← tᵢ - (2/c₁)(v₁ · tᵢ) v₁
L5      v₂ ← tᵢ₊₁ - t_L; c₂ ← v₂ · v₂
L6      rᵢ₊₁ ← r_L - (2/c₂)(v₂ · r_L) v₂
L7      sᵢ₊₁ ← tᵢ₊₁ × rᵢ₊₁
L8  return the frames (rᵢ, sᵢ, tᵢ), with s₀ = t₀ × r₀
```

Lines L2 to L4 apply the reflection $R_1$ in the plane perpendicular to the chord $v_1$.
This reflection maps the vector from any point on the perpendicular bisector plane of the chord to $x_i$ onto the vector from the same point to $x_{i+1}$.
Line L5 sets up the second reflection $R_2$, whose plane is perpendicular to $v_2 = t_{i+1} - t_L$.
Because $t_L$ and $t_{i+1}$ are unit vectors, $R_2$ maps $t_L$ exactly to $t_{i+1}$.
Line L6 applies $R_2$ to the reflected normal, and line L7 completes the frame.
The product $R_2R_1$ is a rotation that maps $t_i$ to $t_{i+1}$, so each new frame is orthonormal and right-handed.

If $c_1 = 0$, the two points are the same.
The implementation then uses $v_1 = t_i$, the limit of the chord direction, and the step becomes the smallest rotation that takes $t_i$ to $t_{i+1}$; for $t_{i+1} = t_i$ it leaves the frame unchanged.
For small steps on a smooth curve, $t_L$ is close to $-t_{i+1}$ and $c_2$ is close to 4.
A $c_2$ near 0 means that the step is too coarse, and the implementation raises an error, because the direction of $v_2$ is then not determined.
The implementation also projects $r_0$ onto the plane perpendicular to $t_0$ and normalizes it.

## Example

Take the helix $x(u) = (\cos u, \sin u, u/2)$ on one turn, $u \in [0, 2\pi]$, with the step $h = \pi/2$, so $N = 4$.
Its speed is $w = \sqrt{5}/2$, and the start frame is $r_0 = (-1, 0, 0)$, the principal normal, with $t_0 = (0, 0.89443, 0.44721)$.

- Line L2 gives $v_1 = (-1, 1, 0.78540)$ and $c_1 = 2.61685$.
- Lines L3 and L4 give $r_L = (-0.23572, -0.76428, -0.60026)$ and $t_L = (0.95204, -0.05761, -0.30051)$.
- The true tangent is $t_1 = (-0.89443, 0, 0.44721)$, so line L5 gives $v_2 = (-1.84646, 0.05761, 0.74773)$ and $c_2 = 3.97184$.
- Line L6 gives $r_1 = (-0.28929, -0.76261, -0.57857)$.

The exact rotation minimizing normal at $u = \pi/2$ is $(-0.28895, -0.76324, -0.57790)$, so the error after one quarter turn is $9.8 \cdot 10^{-4}$.
The exact frame is known in closed form for a helix: it is the Frenet frame turned about the tangent by the angle $-\int\tau\,ds$, which is $2\pi \cdot \frac{1/2}{w} = 2.810$ radians, or 161 degrees, per turn.

The largest error of $r_i$ over the turn, for $N = 4, 8, 16, 32, 64$, is shown with the projection method, which projects $r_i$ onto the normal plane at $x_{i+1}$ and normalizes it.

| $N$ | double reflection | projection |
|---|---|---|
| 4 | $3.9 \cdot 10^{-3}$ | $0.84$ |
| 8 | $2.4 \cdot 10^{-4}$ | $0.34$ |
| 16 | $1.5 \cdot 10^{-5}$ | $0.17$ |
| 32 | $9.3 \cdot 10^{-7}$ | $0.086$ |
| 64 | $5.8 \cdot 10^{-8}$ | $0.043$ |

Each halving of the step divides the error of the double reflection method by about 16, and that of the projection method by 2.

## Correctness

Each frame is orthonormal and right-handed, because $R_2R_1$ is a product of two reflections, which is a rotation, and it maps $t_i$ to $t_{i+1}$.
So the frames never drift away from orthonormality, even after many steps, which is not true of a general integrator applied to the defining equation.

On a curve that lies in a plane with the normal $n$, both $v_1$ and $v_2$ are in the plane, so $R_1$ and $R_2$ fix $n$.
The rotation $R_2R_1$ then turns the plane by the angle from $t_i$ to $t_{i+1}$, which is what the exact frame does.
On a curve on a sphere with the center $p$, $R_1$ maps $x_i - p$ to $x_{i+1} - p$, and $R_2$ fixes the new radial direction, because $t_L$ and $t_{i+1}$ are both perpendicular to it.
So the radial unit vector, which is the exact rotation minimizing normal of a curve on a sphere, is reproduced at every point.
This is Theorem 4.3 of Wang et al.

Running the method backward along the reversed points, from the last frame, returns every earlier frame exactly, because the backward step uses the reflection $R_1$ and the reflection $R_1R_2R_1$, whose product is $(R_2R_1)^{-1}$.

For a smooth curve with $u_i = u_0 + ih$, Wang et al. show that the error of one step is $\frac{K}{720}h^5 + O(h^6)$, where $K$ depends on the curvature, the torsion and their derivatives, and that the global error is $O(h^4)$ (Theorems 4.4 and 4.5).
The [proof](proofs/correctness.md) gives the exact properties in detail.

## Complexity

Each step does a fixed number of dot products, scalings and one cross product, so $N$ steps take $\Theta(N)$ time.
Wang et al. count 28 additions, 32 multiplications and 2 divisions per frame.
The method needs $\Theta(1)$ memory besides the output, since each frame depends only on the one before it.
A fourth-order Runge-Kutta integration of the defining equation reaches the same order, but it needs the second derivative of the curve and several evaluations per step.

## Properties

- **Fourth order.** The global error is $O(h^4)$ for equally spaced parameters, as the table of the example shows.
- **Exact on planes and spheres.** For curves in a plane or on a sphere, the frames equal the exact rotation minimizing frames at the sample points.
- **Orthonormal by construction.** Every frame is an exact rotation of the first one, up to roundoff, with no normalization step.
- **Symmetric.** The backward run from the last frame gives back the earlier frames.
- **Only points and tangents.** The method needs no second derivative and no curvature, so it also works on a curve that is given by samples and tangent estimates.
- **Defined where the curvature is zero.** On a straight piece, $R_1$ and $R_2$ both reverse the tangent, and the frame does not change.

## Variants and improvements

- **Closed curves.** On a closed curve, the last frame differs from the first by a rotation about the tangent by some angle $\alpha$. Adding the twist $-\alpha\,i/N$ to frame $i$ spreads the error evenly and closes the frame. The angle is a property of the curve, not an error of the method.
- **Projection method.** Projecting $r_i$ onto the plane normal to $t_{i+1}$ and normalizing it is simpler, but it is only of the first order globally, as the example shows.
- **Rotation method.** Rotating the frame by the smallest rotation that takes $t_i$ to $t_{i+1}$, about the axis $t_i \times t_{i+1}$, ignores the positions of the points. On the helix of the example its error falls only by 4 when the step is halved, from $0.12$ at $N = 8$ to $1.8 \cdot 10^{-3}$ at $N = 64$.
- **Runge-Kutta integration.** A Runge-Kutta method on $r' = -(r \cdot t')t$ gives any order, but it needs the derivatives of the tangent and a final normalization.
- **Rational frames.** For some polynomial curves, such as Pythagorean hodograph curves, a rotation minimizing frame with rational coefficients exists, and it can be computed exactly.

## When to use it

Use the double reflection method to frame sweep surfaces, tubes, ribbons, roads, roller coasters and camera paths, where the frame must follow the curve without twist.
For a polyline that is the curve itself, as in [discrete elastic rods](/discrete-elastic-rods/), the frame is moved from edge to edge by the rotation method instead, which is exact for that discrete curve.
If the frame must point a given direction, as for a camera that keeps the horizon level, a rotation minimizing frame is the wrong frame, and an up vector or a [keyframed orientation](/keyframe-interpolation/) is the better tool.

## Pitfalls

- **Large steps.** The method assumes that neighbouring tangents are close. If a step is so large that $R_1t_i$ is close to $t_{i+1}$, then $c_2$ is small and the direction of $v_2$ is badly determined. Sample more points where the curve turns quickly.
- **Bad tangents.** The method uses the given tangents as exact. Tangents from finite differences of the points lower the accuracy to that of the difference formula.
- **Uneven samples.** The fourth-order result is for equally spaced parameters. With very uneven spacing, the error constant grows.
- **The start normal.** $r_0$ must be perpendicular to $t_0$. A start vector parallel to $t_0$ has no valid projection.
- **Closed curves do not close.** Expect a twist between the last frame and the first frame on a closed curve, and correct it as in the variants.

## Implementations

## History

Bishop (1975) described the relatively parallel frame, a frame along a curve whose normal vectors do not turn about the tangent and which, unlike the Frenet frame, exists where the curvature is zero.
Klok (1986) called it the rotation minimizing frame, studied it as the solution of a differential equation for sweeping, and gave a simple projection scheme to compute it.
Other early schemes rotated the frame from one tangent to the next.
Wang, Jüttler, Zheng and Liu (2008) introduced the double reflection method, proved its exactness on spheres and planes and its fourth-order accuracy, and showed that it is faster than the earlier methods of the same accuracy.

## References
