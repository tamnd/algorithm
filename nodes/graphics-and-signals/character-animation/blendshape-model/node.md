---
tag: ENWK12
kind: model
slug: blendshape-model
name: Blendshape model
aliases:
- blend shapes
- morph targets
area: graphics-and-signals/character-animation
level: intro
summary: A face or body as the neutral mesh plus a weighted sum of sculpted target offsets, animated by the weights.
prereqs: []
see_also: [facial-action-coding-system, blendshape-direct-manipulation, example-based-facial-rigging, deformation-transfer, pose-space-deformation, linear-blend-skinning, principal-component-analysis, least-squares-problem]
sources:
  - paper: doi:10.2312/egst.20141042
    title: "J. P. Lewis, Ken Anjyo, Taehyun Rhee, Mengjie Zhang, Fred Pighin and Zhigang Deng, Practice and theory of blendshape facial models, Eurographics 2014 State of the Art Reports, 199-218"
    locator: the sections on the whole-face and delta formulations, on the interference between targets and on corrective combination shapes (general locator)
  - paper: doi:10.1109/MCG.2010.41
    title: "J. P. Lewis and Ken Anjyo, Direct manipulation blendshapes, IEEE Computer Graphics and Applications 30(4), 2010, 42-50"
    locator: "the sidebar on the blendshape model (the delta form f = B w + f0)"
  - paper: doi:10.1145/800193.569955
    title: "Frederic I. Parke, Computer generated animation of faces, Proceedings of the ACM Annual Conference, 1972, volume 1, starting at page 451"
    locator: the interpolation between key face shapes (general locator)
---

A blendshape model describes a face, or another deformable part of a character, as one neutral mesh $b_0$ and $K$ sculpted target meshes $b_1, \ldots, b_K$ with the same vertices in the same order.
An animator, a solver or a performance capture system sets one weight $w_k$ per target, and the model gives the mesh

$$v = b_0 + \sum_{k=1}^{K} w_k\,(b_k - b_0).$$

This is the delta form: each target acts through its offset $d_k = b_k - b_0$ from the neutral.
In most face rigs each weight is bounded to $[0, 1]$, so that $w_k = 1$ gives the full sculpted shape and $w_k = 0$ removes it.
The bound is a convention of the rig and of the solvers that fit weights, not a part of the model, and the formula is defined for any real weights.
The model is linear, cheap and fully under the control of the artist, and it is the main face model in film and games.

## The machine

**Quantities.**
The mesh has $n$ vertices, so a shape is a vector in $\mathbb{R}^{3n}$.
The neutral $b_0 \in \mathbb{R}^{3n}$ and the delta matrix $B = [d_1, \ldots, d_K] \in \mathbb{R}^{3n \times K}$ are the parameters of the model.
They are sculpted by hand, scanned from an actor, or computed by [deformation transfer](/deformation-transfer/) or [example-based facial rigging](/example-based-facial-rigging/).
The weight vector $w \in \mathbb{R}^K$ is the state, and it changes at each frame.
The output is

$$v = b_0 + B w.$$

**Targets.**
A target is usually local and has a meaning: one side of a smile, a raised inner brow, an open jaw.
Many rigs name the targets after the action units of the [facial action coding system](/facial-action-coding-system/), so that a target set covers the visible movements of a face.
The deltas are not orthogonal.
Two targets can move the same vertex, and then their offsets add.

**Evaluation.**
The deltas are computed once and stored sparsely, because most targets move only a small part of the mesh.

```pseudo id=main
BLEND(b₀, b₁ … b_K, w)
L1  for each target k: dₖ ← bₖ - b₀, kept only at the vertices it moves   ▷ once per rig
L2  v ← b₀
L3  for each target k with wₖ ≠ 0 do
L4      for each vertex i in dₖ: vᵢ ← vᵢ + wₖ dₖ,ᵢ
L5  return v
```

**The whole-face form.**
An older form writes the shape as a weighted sum of whole meshes, $v = \sum_{k=0}^{K} w_k b_k$ with $\sum_{k=0}^{K} w_k = 1$.
With $w_0 = 1 - \sum_{k \ge 1} w_k$ it is the same mesh as the delta form.
The two forms differ in what a weight means to the artist.
In the whole-face form a target is a full expression, and raising one weight must lower the others.
In the delta form the targets are independent offsets, and a weight of zero always means "this target is off".

**Corrective shapes.**
When two targets look wrong together, a rig adds a combination shape $d_{ij}$ with the weight $w_i w_j$.
Such a term makes the model a polynomial in $w$ and no longer linear.
The plain model of this page has no such terms.

## What it counts

The model has a cost per frame and a cost in memory.
- **Time per frame.** Line L4 runs once per nonzero entry of the active deltas. With $m$ stored vertex offsets over all targets the cost is $O(n + m)$, and $O(n K)$ for dense deltas. This is the cost in the real RAM model.
- **Memory.** The deltas take $O(m)$ vectors, and $O(n K)$ dense.
- **GPU.** A vertex shader or a compute pass adds the active deltas. Engines often limit the number of active targets per draw call, because each one costs bandwidth for its offsets. That limit is a choice of the engine.

The model does not count physical quantities.
It is a geometric model: no mass, no muscle force and no volume is part of it.
A blendshape face looks right only for the shapes that the artist sculpted and for the weight combinations that the artist checked.

## Relation to other models

- **Linear blend skinning.** [Linear blend skinning](/linear-blend-skinning/) is linear in the joint transforms and moves vertices by rotations, so it suits limbs. A blendshape model is linear in the weights and moves vertices by fixed offsets, so a target cannot rotate a region. Rigs often use both: the jaw and the eyes by skinning, the soft tissue by blendshapes.
- **Pose space deformation.** [Pose space deformation](/pose-space-deformation/) drives corrective offsets by the pose of the skeleton through radial basis functions. Its offsets are blendshape deltas whose weights are computed, not keyed.
- **PCA models.** A [principal component analysis](/principal-component-analysis/) of scanned faces also gives a model $v = \bar v + U w$, with orthonormal columns in $U$. The basis is optimal in the least squares sense for the data, but its directions have no meaning for an animator. Blendshape deltas have a meaning and are not orthogonal.
- **FACS.** The [facial action coding system](/facial-action-coding-system/) is a description of facial movements, not a model of a mesh. It is a common guide for which targets to sculpt.

## Known results in the model

All of these are proved properties of the formula, in exact arithmetic, unless marked as a measurement.
- **Affine in the weights.** $v(w)$ is an affine map of $w$. The reachable shapes are the affine subspace $b_0 + \operatorname{span}(d_1, \ldots, d_K)$. With the bound $w \in [0, 1]^K$ they are the zonotope $b_0 + B [0, 1]^K$, the image of the unit cube by a linear map.
- **The two forms agree.** The delta form with weights $w$ equals the whole-face form with weights $(1 - \sum_k w_k, w_1, \ldots, w_K)$. The test file checks this identity with exact rational arithmetic.
- **Endpoints.** $w = 0$ gives $b_0$, and $w = e_k$ gives $b_k$.
- **Interference.** The offsets of two targets that move the same vertex add. In the example below, a smile and an open jaw both move the corner of the mouth, and the combination is not the shape of either target. This is the reason for corrective shapes, and it is also the reason why solving for weights is harder than it looks: because the deltas are not orthogonal, the best value of one weight depends on the others.
- **Fitting weights.** For a given mesh $s$, the best weights in the least squares sense solve $\min_w \lVert B w - (s - b_0) \rVert^2$, a [least squares problem](/least-squares-problem/). The solution is unique if and only if the deltas are linearly independent. With the bound $0 \le w \le 1$ the problem is a convex [quadratic program](/quadratic-programming/). [Direct manipulation of blendshapes](/blendshape-direct-manipulation/) adds a term that keeps the weights near their current values, which also makes the solution unique.
- **Practice.** Film face rigs often have many targets, from tens up to hundreds, as the 2014 survey of Lewis and others reports. This is a report on practice, not a result of the model.

**Example.**
Take one vertex, the corner of the mouth, at $b_0 = (1, 0, 0)$.
The smile target moves it to $b_1 = (1.2, 0.3, 0)$, and the open jaw target moves it to $b_2 = (1, -0.5, 0)$.
So $d_1 = (0.2, 0.3, 0)$ and $d_2 = (0, -0.5, 0)$.

| weights $(w_1, w_2)$ | vertex $v$ |
|---|---|
| $(0, 0)$ | $(1, 0, 0)$ |
| $(1, 0)$ | $(1.2, 0.3, 0)$ |
| $(1, 1)$ | $(1.2, -0.2, 0)$ |
| $(0.5, 0.5)$ | $(1.1, -0.1, 0)$ |

With both weights at 1 the corner moves out and down, which neither target shows.
An artist who wants a different corner for "smile with open jaw" sculpts a corrective shape for that pair.
The tests in `impl/python` check these values exactly.

The history of the model starts with Parke (1972), who animated a face by interpolation between key shapes of a polygon mesh.
The delta form with independent targets became the standard in production, and Lewis and others (2014) survey its practice and theory.

## References
