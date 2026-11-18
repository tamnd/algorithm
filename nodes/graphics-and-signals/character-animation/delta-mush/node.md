---
tag: 118N6H
kind: algorithm
slug: delta-mush
name: Delta mush
aliases:
- direct delta mush
area: graphics-and-signals/character-animation
level: advanced
summary: Smooths the skinned mesh and adds back the rest detail, stored as offsets in frames of the smoothed rest mesh. It hides the faults of rough skinning weights.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", f: "the number of triangles", j: "the number of joints", k: "the largest number of joints per vertex", K: "the number of smoothing steps"}
  time: {precompute: "O(K (n + f))", frame: "O(j + n k + K (n + f))"}
  space: {extra: "O(n + f)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [linear-blend-skinning, laplacian-smoothing]
see_also: [dual-quaternion-skinning, implicit-skinning, taubin-smoothing, cotangent-laplacian, laplacian-surface-editing, jacobi-method, candy-wrapper-artifact, character-skinning]
sources:
  - paper: doi:10.1145/2633374.2633376
    title: "Joe Mancewicz, Matt L. Derksen, Hans Rijpkema and Cyrus A. Wilson, Delta mush, smoothing deformations while preserving detail, Proceedings of the Fourth Symposium on Digital Production (DigiPro '14), pages 7-11, 2014"
    locator: "the smoothing of the rest mesh and the skinned mesh, the deltas in local frames, and the examples"
---

Delta mush is a correction step that runs after a skinning method such as [linear blend skinning](/linear-blend-skinning/).
It smooths the skinned mesh until the faults of the skinning are gone, and then adds back the detail that the smoothing removed.
That detail comes from the rest pose: the rest mesh is smoothed in the same way once, and the difference between each rest vertex and its smoothed position is the delta of the vertex.
The delta is stored in a frame of the smoothed rest surface at the vertex, so it turns with the surface when the mesh moves:

$$u'_i = \tilde u_i + G_i\, \delta_i, \qquad \delta_i = F_i^{\mathsf T} (v_i - \tilde v_i),$$

where $\tilde v$ and $\tilde u$ are the smoothed rest and skinned meshes, and $F_i$ and $G_i$ are their orthonormal frames at vertex $i$.
Joe Mancewicz, Matt Derksen, Hans Rijpkema and Cyrus Wilson described it in 2014.
It needs no extra data from an artist, so rough weights, even weights of only 0 and 1, give a smooth result.

## In plain words

Skinning with rough weights gives a mesh with dents and sharp folds at the joints.
If you blur that mesh, the dents go away, but so do the small shapes of the model, such as wrinkles and muscles.
Delta mush blurs the model once in its rest pose and records, for each point, how far the point sits from its blurred place.
It records this offset in a small frame that sits on the blurred surface, so the offset turns when the surface turns.
In each frame of the animation, it skins the mesh, blurs it the same way, and puts each recorded offset back.
The small shapes come back, and the dents of the skinning stay blurred away.

## The problem

The input is the rest mesh $V$ with its triangles, the skinning weights, and in each frame the skinning transforms of the pose (see [bind pose](/bind-pose/)).
The output is the deformed mesh.
The goal is a smooth deformation near the joints that keeps the detail of the rest mesh, with weights that need little painting.
This is the [character skinning](/character-skinning/) problem with a correction step.

## The algorithm

The smoothing is $K$ steps of uniform [Laplacian smoothing](/laplacian-smoothing/) with the step $\lambda$, done for all vertices at once, as in the [Jacobi method](/jacobi-method/): each vertex moves the fraction $\lambda$ of the way to the mean of its neighbors.
The frame of a vertex has the normal $n_i$, the normalized sum of the cross products of the triangles around it; the tangent $t_i$, the edge to a fixed neighbor with its part along $n_i$ removed, normalized; and $b_i = n_i \times t_i$.

```pseudo id=main
DELTA-MUSH(V, triangles, W, C)
L1  Ṽ ← SMOOTH(V)                                        ▷ precomputation, once
L2  for each vertex i: F_i ← FRAME(Ṽ, i); δ_i ← F_iᵀ (v_i - ṽ_i)
L3  U ← the skinned mesh, here u_i = Σ_j w_ij C_j v_i      ▷ each frame
L4  Ũ ← SMOOTH(U)
L5  for each vertex i: G_i ← FRAME(Ũ, i)
L6      u'_i ← ũ_i + G_i δ_i
L7  return U'

SMOOTH(X)
L8  repeat K times: x_i ← x_i + λ (mean of x_k over the neighbors k of i - x_i), for all i at once

FRAME(X, i)
L9  n ← normalized Σ of the face cross products at i; t ← normalized (e - (e·n) n) for the edge e to the first neighbor; return (t, n × t, n)
```

Lines L1 and L2 depend only on the rest mesh, so they run once.
Line L6 is the only use of the deltas: the frame $G_i$ of the smoothed pose carries the rest detail to its place in the pose.
Any skinning can give $U$ in line L3; the code of this page takes LBS by default and also accepts a given deformed mesh.
The tuning values of the code are $\lambda = 0.5$ and $K = 10$.

## Example

Take an open tube of radius $0.5$ along the $y$ axis from $y = 0$ to $y = 2$, with 12 vertices around and 13 rings.
Joint 0 is at the origin and joint 1 at $(0, 1, 0)$, and the weight of joint 1 rises smoothly over $0.6 \le y \le 1.4$.
The table gives the mean distance of the middle ring, at $y = 1$, from the joint $(0, 1, 0)$; in the rest pose it is $0.5$.

| pose of joint 1 | LBS | delta mush on LBS |
|---|---|---|
| twist by $\pi/2$ about $y$ | $0.354$ | $0.332$ |
| twist by $\pi$ about $y$ | $0.000$ | $0.289$ |
| bend by $\pi/2$ about $z$ through the joint | $0.430$ | $0.467$ |

In the bend, delta mush keeps more of the radius than LBS.
In the twist by $\pi$, LBS puts the whole middle ring on the axis, and delta mush keeps the tube open.
In the twist by $\pi/2$, it is a little worse than LBS: it does not cure the [candy wrapper artifact](/candy-wrapper-artifact/).
Even when the input twists each ring rigidly, so that every ring keeps the radius $0.5$, the output middle ring has the radius $0.380$, and the output moves up to $0.12$ from the input.

With rigid weights, 0 below $y = 1$ and 1 above, and a bend by $\pi/3$, LBS tears the tube between the rings at $y = 1$ and $y = 1.1667$, whose rest gap is $0.1667$.
The worst change of that gap is $0.483$ with LBS and $0.150$ with delta mush.
These values come from the code of this page and are measurements, not proved properties.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md); they are proved properties in exact arithmetic.
- SMOOTH is the linear map $(I - \lambda L)^K$ with the random-walk Laplacian $L = I - D^{-1} A$; each row of $I - \lambda L$ sums to 1.
- The frames are orthonormal and right-handed wherever the normal sum is not zero and the tangent edge is not along the normal.
- In the bind pose the output is the rest mesh exactly, because $F_i F_i^{\mathsf T} = I$; the same holds for any skinning that returns the rest mesh.
- If all the joints move by one rigid motion $G$, the output is $G V$: the smoothing commutes with affine maps, and the frames turn with the mesh.

These do not say that the output is close to a "true" deformation; how well the method hides the faults of the skinning is a measurement, as in the example.

## Complexity

One smoothing step visits each vertex and its neighbors, which costs $O(n + f)$ on a triangle mesh, so SMOOTH costs $O(K (n + f))$.
The frames cost $O(n + f)$.
The precomputation costs $O(K (n + f))$, and each frame costs $O(j + n k)$ for LBS plus $O(K (n + f))$ for the correction.
The extra space is $O(n + f)$ for the neighbor lists, the deltas and the work arrays.
The cost grows with $K$, so a large $K$ for a wide blur makes delta mush much slower than LBS.

## Properties

- It is a correction step: any skinning can come before it, and the bind pose and common rigid motions pass through unchanged (proved).
- It keeps the detail of the rest mesh in the local frames, so wrinkles and other small shapes move with the surface.
- It hides rough weights: with weights of only 0 and 1 the joint still bends smoothly (a measurement on the example).
- It does not keep volume in twists: on the tube it is no better than LBS at $\pi/2$ (a measurement).
- It is global within the reach of the smoothing: a vertex depends on the skinned positions of all vertices within about $K$ edges.
- $\lambda$, $K$ and the choice of the tangent edge are tuning values.

## Variants and improvements

- **Masks.** Production tools let the artist scale the correction per vertex, so that some regions follow the skinning directly.
- **Other smoothing.** [Taubin smoothing](/taubin-smoothing/) shrinks the mesh less per step, and a [cotangent Laplacian](/cotangent-laplacian/) depends less on the triangulation than the uniform one.
- **Direct delta mush.** Binh Huy Le and J. P. Lewis (2019) rewrote the method as a direct skinning with precomputed data per vertex and joint, which avoids the smoothing at run time; it is a different method and has its own trade-offs.
- **Better input.** Since delta mush corrects any skinning, [dual quaternion skinning](/dual-quaternion-skinning/) can give $U$ in line L3, but the example shows that a good input alone does not keep the twist radius.
- **Other corrections.** [Implicit skinning](/implicit-skinning/) corrects the skinning with fields of the bones and models contact; [Laplacian surface editing](/laplacian-surface-editing/) also stores detail as differential coordinates.

## When to use it

Use it when the weights are rough or the rig is in early work, and smooth joints with the rest detail kept matter more than the cost per frame.
For twist-heavy joints, add a twist bone or another fix, since delta mush does not keep the radius in a twist.

## Pitfalls

- **Shrinking.** The smoothing shrinks the mesh, and the deltas restore the rest shape only where the deformation is close to rigid; with large $K$ the results can drift.
- **Degenerate frames.** A vertex whose normal sum is near zero, or whose tangent edge is near the normal, has an unstable frame, and its delta can jump.
- **Boundaries.** On an open boundary the uniform smoothing pulls vertices inward along the surface; the deltas restore this in the rest pose, but a pose that stretches the boundary changes it.
- **Topology.** The neighbor lists and the frames depend on the mesh connectivity, so the rest mesh and the skinned mesh must have the same triangles and the same vertex order.
- **Cost.** A wide blur needs a large $K$, and the cost per frame grows with it.

## Implementations

## History

Joe Mancewicz, Matt Derksen, Hans Rijpkema and Cyrus Wilson of Rhythm and Hues presented delta mush at DigiPro 2014.
Commercial animation tools soon added it as a deformer.
In 2019 Binh Huy Le and J. P. Lewis turned it into direct delta mush, a direct skinning method with precomputed data.

## References
