---
tag: KN8M9F
kind: algorithm
slug: implicit-skinning
name: Implicit skinning
aliases:
- implicit surface skinning
area: graphics-and-signals/character-animation
level: research
summary: Corrects linear or dual quaternion skinning by moving each vertex back to its rest value of a field built from one implicit surface per bone, which gives skin contact and bulges at joints.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", j: "the number of joints", k: "the largest number of joints per vertex", i: "the number of projection steps per vertex"}
  time: {frame: "O(j + n (k + i j))"}
  space: {extra: "O(n + j)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [linear-blend-skinning, dual-quaternion-skinning, radial-basis-function-interpolation]
see_also: [signed-distance-function, newton-raphson-method, delta-mush, optimized-centers-of-rotation-skinning, candy-wrapper-artifact, pose-space-deformation, character-skinning]
sources:
  - paper: doi:10.1145/2461912.2461960
    title: "Rodolphe Vaillant, Loïc Barthe, Gaël Guennebaud, Marie-Paule Cani, Damien Rohmer, Brian Wyvill, Olivier Gourmel and Mathias Paulin, Implicit skinning, real-time skin deformation with contact modeling, ACM Transactions on Graphics 32(4), article 125, 2013 (SIGGRAPH 2013)"
    locator: "the fields of the bones (HRBF and compact support), the composition operators, and the projection of the vertices with the gradient stop and the relaxation"
---

Implicit skinning is a correction step that runs after a geometric skinning method such as [linear blend skinning](/linear-blend-skinning/) or [dual quaternion skinning](/dual-quaternion-skinning/).
In a precomputation it builds, for each bone, an implicit surface that fits the part of the mesh around the bone, and it composes these fields into one field $f$ of the whole character.
Each vertex stores its value $f(v_i) = \mathrm{iso}_i$ in the rest pose.
In each frame the fields move rigidly with their bones, the mesh is skinned as usual, and each vertex then walks along the gradient of $f$ until it is back at its own value:

$$v \leftarrow v + \sigma\,(\mathrm{iso}_i - f(v))\,\frac{\nabla f(v)}{\lvert \nabla f(v) \rvert^2}.$$

A vertex stops when the gradient turns sharply between two steps, which happens where the field of one bone meets that of another.
So the skin on the inside of a bent elbow does not pass into itself, it forms a contact crease, and the outside keeps its shape.
Vaillant and co-authors fit the field of each bone with Hermite [radial basis functions](/radial-basis-function-interpolation/), and compose them with operators that can make a bulge where two parts press together.
The code on this page is a 2D toy of the method; it says so in its header.

## In plain words

Plain skinning moves the skin with the bones, but where a limb bends, the skin on the inside sinks into the limb and passes through itself.
Implicit skinning first builds a smooth invisible shape around each bone, like a sausage that fits the flesh of that bone.
Each point of the skin remembers how deep it sat in these shapes before the animation.
When the bones move, the shapes move with them.
After the usual skinning, each point is pushed in or out until it sits at its old depth again.
Where the inner sides of a bent elbow meet, the points stop, and the skin forms a fold instead of passing through itself.

## The problem

The input is the rest mesh, the skinning weights, the rest transforms of the bones, and in each frame the skinning transforms $C_j$ of the pose (see [bind pose](/bind-pose/)).
The output is the deformed mesh, with no self-intersection near the joints and with the shape of the rest pose kept where the parts do not touch.
This is the [character skinning](/character-skinning/) problem with a correction for contact.

## The algorithm

The field of bone $j$ is a function $f_j$ with values in $[0, 1]$ that is $0.5$ on the surface of its part of the mesh, larger inside and 0 far away; in the paper it is an HRBF fit, changed to a compact support.
In the pose, the field of the bone is $f_j(C_j^{-1} x)$, and the union of the bones is the maximum $f = \max_j f_j(C_j^{-1} x)$ in the simplest composition.

```pseudo id=main
IMPLICIT-SKINNING(V, W, bones, C)
L1  iso_i ← f(v_i) for each rest vertex                  ▷ precomputation
L2  v_i ← Σ_j w_ij C_j v_i for each vertex               ▷ geometric skinning, here LBS
L3  for each vertex i
L4      PROJECT(v_i, iso_i):
L5          g_prev ← none
L6          repeat at most K times
L7              f, g ← the field and its gradient at v_i, with the bones in the pose
L8              if |f - iso_i| ≤ tol: stop
L9              if g_prev ≠ none and angle(g, g_prev) > α_max: stop    ▷ contact
L10             v_i ← v_i + σ (iso_i - f) g / |g|²; g_prev ← g
L11 repeat R times: move each vertex along the surface toward a smooth spacing, then PROJECT it again
L12 return V
```

Line L10 is a damped Newton step for the scalar equation $f(v) = \mathrm{iso}_i$ along the gradient (see [Newton's method](/newton-raphson-method/)).
Line L9 is the contact rule: where the vertex crosses into the region of another bone, the gradient of the union changes direction, and the vertex stops there.
Line L11 is the relaxation: the projection moves each vertex on its own, so neighbors can bunch up; a tangential move toward a better spacing, followed by a new projection, evens them out.
The paper also applies a Laplacian smoothing in this step.

The toy of the code is in the plane.
The field of a bone with the rest radius $r$ is $t(d / 2r)$, with $d$ the distance to the segment of the bone and $t(u) = 1 - 3u^2 + 2u^3$ for $u < 1$ and 0 beyond, so it is $0.5$ at the distance $r$.
The mesh is a closed polygon, and the relaxation moves each vertex along the chord of its two neighbors to the point with its rest parameter on that chord.
The step $\sigma = 0.35$, the angle $\alpha_{\max} = 55°$, the cap of $0.05$ on the step length and the two rounds of relaxation are tuning values of the toy.

## Example

Take the toy arm: two bones from $(0, 0)$ to $(1, 0)$ and from $(1, 0)$ to $(2, 0)$ with the radius $0.25$, the outline of a stadium with 80 vertices, and the weight of bone 1 rising smoothly over $0.8 \le x \le 1.2$.
Bend bone 1 about the elbow $(1, 0)$.

| bend | nearest skin point to a bone, LBS | nearest skin point to a bone, implicit | vertices stopped at contact |
|---|---|---|---|
| $60°$ | $0.189$ | $0.238$ | 4 |
| $100°$ | $0.084$ | $0.161$ | 8 |
| $130°$ | $0.0001$ | $0.056$ | 10 |

The rest skin is at the distance $0.25$ from the bones.
All the vertices that converged are back at the field value $0.5$ within $10^{-9}$, so they are at least $0.25$ from both bones; the stopped vertices lie within $0.05$ of the line where the two fields are equal, on the inside of the elbow.
These values come from the code of this page and are measurements of the toy.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md); they are proved properties of the method in exact arithmetic, not of the HRBF fit.
- In the bind pose every vertex is at its iso value, the relaxation target is the vertex itself, and the mesh does not move.
- Under a common rigid motion of all the bones, the skinned mesh and the fields move together, so the vertices again do not move relative to the bones.
- Each step of line L10 changes $f$ by $\sigma(\mathrm{iso}_i - f) + O(\lvert \text{step} \rvert^2)$ to first order, so for a small enough $\sigma$ and a smooth field the error $\lvert f - \mathrm{iso}_i \rvert$ shrinks by about the factor $1 - \sigma$ per step.
- In the toy, a converged vertex with $\mathrm{iso}_i = 0.5$ has the distance at least $r$ from every bone, because the union is the maximum.
- For one bone in the toy, the projection moves the vertex on the line from its nearest point on the bone, to the distance where the field has the value $\mathrm{iso}_i$.

## Complexity

The geometric skinning costs $O(j + n k)$.
A projection step evaluates the field; in the toy this costs $O(j)$ for all the bones, and in practice only the few bones near a vertex count, because the fields have a compact support.
With $i$ steps per vertex, the frame costs $O(j + n (k + i j))$.
The fit of the fields is a precomputation; the paper reports real-time rates for whole characters (a measurement of the paper).

## Properties

- It keeps the rest shape where the parts of the mesh do not touch, and makes a contact crease where they do; LBS and DQS make neither.
- It is a correction: it needs a good geometric skinning as the start, because the projection only moves vertices along the gradient, a short way.
- The iso value of each vertex is stored, so the rest details of the mesh survive, unlike a projection onto one level of the field.
- The result depends on tuning values: the step, the angle of the contact stop, and the number of relaxation rounds (heuristics).
- It is not exact: the projection is iterative and stops after a fixed number of steps or at contact.

## Variants and improvements

- **Composition operators.** Instead of the union by maximum, the paper composes the fields of neighbor bones with gradient-based operators, which can give a bulge where two parts press together.
- **Tracking.** A later paper of the same group tracks the iso level over time to handle large and fast motions more robustly.
- **Delta mush.** [Delta mush](/delta-mush/) also corrects a geometric skinning, by smoothing and stored details, with no fields and no contact.
- **Centers of rotation.** [CoR skinning](/optimized-centers-of-rotation-skinning/) removes the collapse at joints with a better blend instead of a correction, but it does not model contact.
- **Distance fields.** In the simplest case the field is a function of a [signed distance](/signed-distance-function/) to each bone, as in the toy.

## When to use it

Use it when the skin of a character must fold at the joints without passing through itself, as at the inside of an elbow or a knee, and a per-vertex iteration each frame is acceptable.
For a fast game character with no visible contact, LBS or DQS with corrective shapes is cheaper.

## Pitfalls

- **Large motions.** If the geometric skinning moves a vertex too far, the projection can reach the wrong part of the field or leave the support, where the gradient is zero; the toy stops such a vertex.
- **Flat fields near the bone.** Deep inside the field the gradient is small and a Newton step can be very long; cap the step, as the toy does.
- **The contact angle.** Too small an angle stops vertices that are not in contact, and too large an angle lets the skin pass through itself.
- **Thin parts.** The field of a bone must fit its part of the mesh well; for fingers and other thin parts the fit is hard.
- **Relaxation drift.** Without a target from the rest mesh, the relaxation moves vertices even in the bind pose; keep the rest pose a fixed point.

## Implementations

## History

Rodolphe Vaillant, Loïc Barthe, Gaël Guennebaud, Marie-Paule Cani, Damien Rohmer, Brian Wyvill, Olivier Gourmel and Mathias Paulin presented implicit skinning at SIGGRAPH 2013.
It joined the line of work on implicit surfaces in modeling, with composition operators of fields, and the line of work on skinning methods that correct LBS and DQS.

## References
