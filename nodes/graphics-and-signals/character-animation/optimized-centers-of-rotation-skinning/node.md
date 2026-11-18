---
tag: 3BKQB9
kind: algorithm
slug: optimized-centers-of-rotation-skinning
name: Optimized centers of rotation skinning
aliases:
- CoR skinning
area: graphics-and-signals/character-animation
level: research
summary: Precomputes a center of rotation per vertex as a mean of the rest surface weighted by weight similarity, then turns the vertex about it by blended quaternions and moves it by blended translations.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", j: "the number of joints", k: "the largest number of joints per vertex", m: "the number of triangles of the refined mesh"}
  time: {precompute: "O(n m k^2)", frame: "O(j + n k)"}
  space: {extra: "O(n + m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [linear-blend-skinning, spherical-blend-skinning, unit-quaternion-rotation]
see_also: [dual-quaternion-skinning, candy-wrapper-artifact, delta-mush, implicit-skinning, bounded-biharmonic-weights, skinning-decomposition, character-skinning]
sources:
  - paper: doi:10.1145/2897824.2925959
    title: "Binh Huy Le and Jessica K. Hodgins, Real-time skeletal skinning with optimized centers of rotation, ACM Transactions on Graphics 35(4), article 37, 2016 (SIGGRAPH 2016)"
    locator: "the similarity of skinning weights, the center of rotation integral, the subdivision of the rest mesh and the run-time blend"
---

Skinning with optimized centers of rotation (CoR skinning) is a skinning method of Le and Hodgins (2016) that sits between [linear blend skinning](/linear-blend-skinning/) and [dual quaternion skinning](/dual-quaternion-skinning/).
In a precomputation it gives each vertex $i$ a center of rotation $p_i$: the mean of the rest surface, where each part counts by how similar its skinning weights are to the weights $w_i$ of the vertex.
In each frame the vertex turns about $p_i$ by the normalized blend of the joint quaternions, and $p_i$ itself moves by linear blend skinning:

$$v_i' = R_i\,(v_i - p_i) + \sum_j w_{ij}\, C_j\, p_i .$$

The rotation part has no candy wrapper collapse, and the center sits inside the limb near the joint, so a bent elbow neither collapses as with LBS nor bulges as with DQS.
The run-time cost is close to that of DQS, and the result depends only on the weights and the rest mesh, so it fits an existing rig.

## In plain words

Each point of the skin needs a pivot to turn about.
Bones that move the same point turn in different ways, so there is no single obvious pivot.
This method picks the pivot of each point once, before the animation starts.
It looks at all the parts of the skin that the same bones move in the same proportions, and takes their average position.
For a point on an elbow, those parts form a ring around the arm at the elbow, so the pivot falls in the middle of the arm.
During the animation each point turns about its pivot by the average turn of its bones, so the arm keeps its thickness when it bends or twists.

## The problem

The input is the rest mesh with the vertices $v_i$, the normals $n_i$ and the triangles, the weights $w_{ij} \ge 0$ with $\sum_j w_{ij} = 1$, and in each frame the rigid skinning transforms $C_j = M_j B_j^{-1}$ (see [bind pose](/bind-pose/)), with the rotation $R_j$, the translation $t_j$ and the unit quaternion $q_j$.
The output is the deformed mesh of each frame.
This is the [character skinning](/character-skinning/) problem with rigid joint transforms and fixed weights.

## The algorithm

The similarity of two weight vectors is

$$s(w_p, w_v) = \sum_{j < k} w_{pj}\, w_{pk}\, w_{vj}\, w_{vk}\, \exp\!\left(-\frac{(w_{pj} w_{vk} - w_{pk} w_{vj})^2}{\sigma^2}\right).$$

A term is large when both vectors use the joints $j$ and $k$ in the same ratio; the factor $w_{pj} w_{pk} w_{vj} w_{vk}$ makes it zero unless both vectors use both joints.
The center of vertex $i$ is the integral $p_i = \int s(w_i, w(x))\, x\, dA / \int s(w_i, w(x))\, dA$ over the rest surface, with $w(x)$ the interpolated weights.
The method subdivides the rest mesh until the weights change little across each triangle, and then sums over the triangles $t$ with the area $a_t$, the centroid $c_t$ and the mean weight vector $\bar w_t$.

```pseudo id=main
COR-SKINNING
▷ precomputation, once for the rest mesh
L1  refine the triangles; for each triangle t: a_t ← area, c_t ← centroid, w̄_t ← mean of its vertex weights
L2  for each vertex i
L3      num ← 0; den ← 0
L4      for each triangle t: s ← s(w_i, w̄_t) a_t; num ← num + s c_t; den ← den + s
L5      p_i ← num / den if den > 0, else v_i
▷ each frame
L6  for each vertex i
L7      R ← the rotation of normalize(Σ_j s_j w_ij q_j)    ▷ s_j = ±1, aligned to the joint of the largest weight
L8      t ← Σ_j w_ij C_j p_i - R p_i
L9      v'_i ← R v_i + t
L10     n'_i ← R n_i
L11 return V', N'
```

Line L5 handles a vertex whose weights share no pair of joints with any triangle, such as a vertex with one joint: with $p_i = v_i$, lines L8 and L9 give the linear blend $\sum_j w_{ij} C_j v_i$, which is the rigid motion of the joint.
Line L7 is the same quaternion blend as in [spherical blend skinning](/spherical-blend-skinning/); line L8 makes the translation the linear blend of the images of the center, so the center moves exactly as in LBS.
The width $\sigma$ of the similarity and the refinement bound are tuning values; the code uses $\sigma = 0.1$ and refines until the weight vectors of the two ends of every edge differ by at most $0.1$ in length.

## Example

Take an open tube of radius $0.5$ along $y$ from 0 to 2, with 8 vertices per ring and 9 rings, two joints at $y = 0$ and $y = 1$, and the weight of joint 1 rising smoothly from 0 at $y = 0.5$ to 1 at $y = 1.5$.
The rings are symmetric about the $y$ axis, so every center of a vertex with two joints lies on the axis: the vertices at $y = 0.75$, $1$ and $1.25$ get the centers $(0, 0.736, 0)$, $(0, 1, 0)$ and $(0, 1.264, 0)$.

| pose | vertex | CoR | LBS |
|---|---|---|---|
| twist by $\pi$ about $y$ | $(0.5, 1, 0)$ | $(0, 1, -0.5)$ | $(0, 1, 0)$ |
| bend by $\pi/2$ about $z$ through $(0, 1, 0)$ | $(0.5, 1, 0)$ | $(0.35355, 1.35355, 0)$ | $(0.25, 1.25, 0)$ |
| same bend | $(-0.5, 1, 0)$ | $(-0.35355, 0.64645, 0)$ | $(-0.25, 0.75, 0)$ |

In the twist, LBS pulls the middle ring onto the axis, and CoR keeps the radius $0.5$.
In the bend, the middle ring keeps the distance $0.5$ from the elbow with CoR and drops to $0.35355$ with LBS.
These values come from the code of this page, so they are measurements of this mesh and these weights.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md); they are proved properties of the formulas in exact arithmetic.
- The similarity is symmetric, nonnegative, and zero unless both weight vectors use at least two common joints.
- Each center is a convex combination of triangle centroids, so it lies in the convex hull of the rest mesh; the centers move with the rest mesh under a rigid motion.
- In the bind pose the mesh stays where it is; under a common rigid motion $C_j = G$ the mesh moves by $G$.
- A vertex with one joint moves by the transform of that joint.
- Each vertex moves by a rotation and a translation, so its normal stays a unit vector, and the center $p_i$ moves as in LBS.
- If the center of a vertex is a fixed point of all its joint transforms, the vertex keeps its distance to the center; this is why the twisted and the bent tube keep their radius.

## Complexity

The precomputation compares each vertex with each triangle of the refined mesh, which costs $O(n m k^2)$ time with $k^2$ joint pairs per similarity; the code of this page uses this plain double loop, and a production tool needs a faster evaluation of the sum.
Each frame costs $O(j)$ for the quaternions of the joints and $O(k)$ per vertex, so $O(j + n k)$, the same order as LBS and DQS.
The extra space is one center per vertex and the refined mesh during the precomputation, $O(n + m)$.

## Properties

- Rigid per vertex at run time: no candy wrapper collapse under twist (a proved property for centers on the twist axis, and a measurement for the tube above).
- Less bulge than DQS and less collapse than LBS in bends; Le and Hodgins show this on character models (a measurement).
- The center depends only on the rest mesh and the weights, so changing the animation needs no new precomputation; changing the weights does.
- The similarity, $\sigma$ and the refinement are heuristic choices.
- A vertex far from all others with similar weights can get a center that is far from the joint, because the mean is over the whole surface.

## Variants and improvements

- **Spherical blend skinning.** [SBS](/spherical-blend-skinning/) uses the same formula, but finds the center in each frame by least squares per set of joints, from the pose instead of the rest surface.
- **Dual quaternion skinning.** [DQS](/dual-quaternion-skinning/) has no explicit center; for a bend it turns the vertices about a point that can lie outside the limb, which gives the bulge that CoR removes.
- **Delta mush.** [Delta mush](/delta-mush/) also fixes the artifacts of LBS, by smoothing and stored details instead of a better blend.
- **Better weights.** The method keeps the weights of the rig; [bounded biharmonic weights](/bounded-biharmonic-weights/) or [skinning decomposition](/skinning-decomposition/) can provide them.

## When to use it

Use it as a drop-in replacement of LBS or DQS in a real-time engine when twists collapse and bends bulge, and the weights are fixed.
Use DQS if no precomputation is possible, for example when the weights change at run time.

## Pitfalls

- **Coarse meshes.** Without the refinement, the sum over triangles is a poor stand-in for the integral where the weights change fast, and the centers jump between neighbor vertices.
- **One joint per vertex.** Such a vertex has no similar triangles; give it its own position as the center, or any point, since the result is then the rigid motion of the joint anyway.
- **The sign of the quaternions.** Align the signs to a pivot before the blend, or the blend can turn the long way.
- **Scale in the rig.** The rotation blend assumes rigid joint transforms; with scale in $C_j$, the quaternions of line L7 are not defined, and the scale must be handled separately.
- **Weights not normalized.** The weights of each vertex must sum to 1, or the center does not move as in LBS.

## Implementations

## History

Binh Huy Le and Jessica K. Hodgins presented the method at SIGGRAPH 2016.
It takes the idea of a center of rotation from the spherical blend skinning of Kavan and Žára (2005), and moves the computation of the center from each frame to a precomputation over the rest surface.

## References
