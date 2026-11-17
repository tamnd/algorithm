---
tag: TTFYST
kind: algorithm
slug: wire-deformation
name: Wires deformation
aliases:
- wire deformer
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Deform a surface by moving space curves, where each point follows the nearest point of a wire with a falloff in distance.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {N: "the number of points", w: "the number of wires", V: "the number of vertices of one wire polyline"}
  time: {per_point_per_wire: "Θ(V)", all: "Θ(N w V)"}
  space: {extra: "O(w)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
prereqs: [b-spline]
see_also: [free-form-deformation, barr-global-deformations, cage-based-deformation, shape-deformation, linear-blend-skinning, rotation-minimizing-frame, nurbs, newton-point-inversion]
sources:
  - paper: doi:10.1145/280814.280946
    title: "Karan Singh and Eugene Fiume, Wires: a geometric deformation technique, SIGGRAPH 98, 405-414, 1998"
    locator: the whole paper (the reference curve and the wire curve, the radius of influence, the scale and the falloff, and the use of several wires)
---

Wires deformation moves the points of an object with space curves.
Each wire is a pair of curves with the same parameter: the reference curve $R$, which says where the wire was when the object was bound to it, and the wire curve $W$, which the user moves.
A point near $R$ finds its closest point $R(u)$ and then follows $W$ at the same parameter: it is scaled about $R(u)$, turned with the tangent, and moved by $W(u) - R(u)$, each by an amount $F$ that falls from 1 on the curve to 0 at the radius of influence.
Karan Singh and Eugene Fiume (1998) introduced the method for modeling and animation; creases, lips and brows follow curves better than lattices.
This page uses polylines for $R$ and $W$; smooth curves such as [NURBS](/nurbs/) work in the same way with a numerical closest point.

## In plain words

Lay a piece of string on a soft surface, and draw a ring around the string to say how far its pull reaches.
Now move the string.
A point of the surface right under the string goes with it all the way.
A point a little away from the string goes part of the way, and a point outside the ring does not move at all.
To know which part of the string pulls it, each point looks for the closest place on the string in its starting position.
If the string turns, the points near it turn with it, and if you ask for it, they also spread away from the string or pull in toward it.

## The problem

The input is a point $P$ and a wire: the reference polyline $R$ and the wire polyline $W$ with the same number of vertices, the radius $r > 0$, the scale $s > 0$, and the falloff $f: [0, \infty) \to [0, 1]$ with $f(0) = 1$ and $f(x) = 0$ for $x \ge 1$.
The parameter $u = i + t$ with $0 \le t \le 1$ means the point at the fraction $t$ of segment $i$, so $R(u)$ and $W(u)$ correspond.
The output is the moved point.
The implementation uses $f(x) = (1 - x^2)^2$ for $x < 1$; it has $f'(0) = 0$ and $f'(1) = 0$, so the move is smooth at the curve and at the radius. Any falloff with the properties above can be passed in.

## The algorithm

$R'(u)$ and $W'(u)$ are the unit tangents of the segments that hold $u$.

```pseudo id=main
WIRE(P, R, W, r, s, f)
L1  u ← the parameter of the point of R closest to P
L2  F ← f(|P - R(u)| / r)
L3  if F = 0 then return P
L4  Q ← R(u) + (1 + (s - 1)F)(P - R(u))
L5  a ← R'(u) × W'(u) / |R'(u) × W'(u)|; θ ← the angle from R'(u) to W'(u)
L6  Q ← R(u) + rot(a, Fθ)(Q - R(u))
L7  return Q + F(W(u) - R(u))
```

Line L1 is a closest point search; on a polyline it projects $P$ onto each segment and keeps the nearest, and on a smooth curve it is a Newton iteration such as [Newton point inversion](/newton-point-inversion/).
Line L4 scales the offset from the curve: with $s > 1$ points spread from the wire, with $s < 1$ they gather to it, and with $s = 1$ nothing changes.
Lines L5 and L6 turn the offset by the fraction $F$ of the turn of the tangent, with Rodrigues' formula for rot; if the tangents are parallel the step does nothing.
Line L7 adds the fraction $F$ of the move of the curve point.
For several wires, the implementation computes the move $\Delta_j$ of each wire alone and returns $P + \sum_j \Delta_j|\Delta_j|^m / \sum_j |\Delta_j|^m$, so with $m = 0$ the moves are averaged and with a large $m$ the largest move wins.

## Example

Let $R$ be the straight polyline from $(0, 0, 0)$ to $(3, 0, 0)$, $W$ the same polyline moved by $(0, 1, 0)$, and $r = 1$, $s = 1$.
The point $P = (1.5, 0.5, 0)$ has the closest point $R(u) = (1.5, 0, 0)$ at the distance $0.5$, so $F = (1 - 0.25)^2 = 0.5625$.
The tangents agree, so lines L5 and L6 do nothing, and line L7 gives $(1.5, 0.5 + 0.5625, 0) = (1.5, 1.0625, 0)$.
With $s = 2$, line L4 first moves the offset $0.5$ to $0.5(1 + 0.5625) = 0.78125$, and the result is $(1.5, 1.34375, 0)$.
The point $(1.5, 1.2, 0)$ is farther than $r$ and does not move.

For the turn, let $R$ go from $(0, 0, 0)$ to $(1, 0, 0)$ and $W$ from $(0, 0, 0)$ to $(0, 1, 0)$, a turn of 90 degrees about $z$.
With a very large $r$, $F \approx 1$, and the point $(0, 0.2, 0)$ turns with the tangent to $(-0.2, 0, 0)$, while $(0, 0, 0.2)$ lies on the axis of the turn and stays.

## Correctness

The method is a construction, so correctness means that it has the properties a user expects of it.
These follow from the lines of the algorithm, and the [proof](proofs/correctness.md) gives them in full.
If $W = R$ and $s = 1$, line L4 keeps $P$, line L6 turns by 0, and line L7 adds 0, so every point stays.
A point at the distance $r$ or more has $F = 0$ and stays, by line L3.
A point on $R$ has $F = 1$ and the offset 0, so it goes to $W(u)$: the object follows the wire exactly along the curve.
The turn at line L6 keeps the length of the offset, so with $s = 1$ the distance of the moved point from $R(u) + F(W(u) - R(u))$ is the distance of $P$ from $R$.
As $|P - R(u)| \to r$, $F \to 0$, and every step tends to the identity, so the move is continuous across the boundary of the region of influence.

## Complexity

Line L1 on a polyline with $V$ vertices projects onto $V - 1$ segments, in $\Theta(V)$ time; lines L2 to L7 take $O(1)$.
So $N$ points and $w$ wires cost $\Theta(NwV)$ time.
The closest parameter $u$ depends only on $R$, so it can be computed once per point and wire and kept while $W$ moves, which makes each later frame $O(Nw)$.
A spatial grid over the segments of $R$ makes line L1 much faster for long wires.

## Properties

- **Identity at rest (proved).** $W = R$ with $s = 1$ moves no point.
- **Local (proved).** Only points within the distance $r$ of $R$ move.
- **Interpolates the wire (proved).** A point on $R$ goes to the matching point of $W$.
- **Continuous at the radius (proved).** The move tends to 0 at the boundary of the region of influence.
- **Not continuous everywhere (proved).** Where a point has two closest points on $R$, as on the inside of a tight bend, $u$ jumps, and so can the move. A polyline also has a jump in its tangent at each inner vertex, so the turn of line L6 jumps for points whose closest point is that vertex.
- **Independent of the representation.** Like [FFD](/free-form-deformation/), wires move points, so they work on meshes, surfaces and point clouds.

## Variants and improvements

- **Smooth curves.** Use spline curves such as [B-splines](/b-spline/) for $R$ and $W$, with a smooth tangent, to remove the jump of the turn at the vertices.
- **Several wires.** The blend of moves above with the exponent $m$ is one choice; other blends weight each wire by its falloff.
- **Holding a region still.** In the blend above, a wire that does not move has the weight 0 and has no effect. To keep the upper lip still while the lower lip moves, the blend must give a fixed wire weight, for example by weighting each wire by its falloff $F$.
- **Falloff and scale along the curve.** $r$, $s$ and the falloff can vary with $u$, to make a crease sharp at one end and soft at the other.
- **Frames.** The turn at line L6 uses only the change of the tangent; a full frame along the curve, such as a [rotation-minimizing frame](/rotation-minimizing-frame/), also controls the twist about the tangent.

## When to use it

Use wires when the shape change follows a curve on the object: a lip, a brow, a wrinkle, a seam, a tail.
A curve is a natural handle for an artist, and it acts only near itself, so many wires can shape one face.
For broad changes of a volume, use a lattice ([FFD](/free-form-deformation/)) or a [cage](/cage-based-deformation/); for a skeleton that bends limbs, use [linear blend skinning](/linear-blend-skinning/).

## Pitfalls

- **Medial jumps.** A point that lies about as far from two parts of $R$ as from each, inside a bend, can switch its closest point between frames and jump. Keep $r$ smaller than the radius of curvature of $R$.
- **Rebinding.** The binding must use $R$, not $W$; finding the closest point on the moved wire changes $u$ and makes the result depend on the path of the edit.
- **Opposite tangents.** A turn of 180 degrees has no defined axis; the implementation raises an error there.
- **Parameter mismatch.** $R$ and $W$ must share the parameter, so they need the same number of vertices; a wire that is resampled after binding moves points along the curve.
- **Falloff with a kink.** A falloff with $f'(1) \ne 0$, such as $1 - x$, makes a visible crease at the radius.

## Implementations

## History

Singh and Fiume presented wires at SIGGRAPH 1998 as a geometric deformation technique driven by space curves, with a radius of influence, a scale and a falloff for each wire.
Earlier space deformations, such as [Barr's](/barr-global-deformations/) closed-form maps and lattice [FFD](/free-form-deformation/), used no curve as the handle.
Wire deformers of this kind are now common in animation software.

## References
