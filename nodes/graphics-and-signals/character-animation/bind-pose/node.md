---
tag: 3RBDTZ
kind: definition
slug: bind-pose
name: Bind pose
aliases:
- rest pose
area: graphics-and-signals/character-animation
level: intro
summary: The pose of the skeleton in which the skin was attached. The inverses of its joint world transforms map the rest mesh into the frame of each joint.
prereqs: [character-skeleton]
see_also: [linear-blend-skinning, dual-quaternion-skinning, character-skinning, skeletal-animation, forward-kinematics, automatic-rigging, homogeneous-transformation-matrix]
sources:
  - url: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
    title: The Khronos Group, glTF 2.0 Specification
    locator: "Section 3.7.3 (skins, the joints and the inverseBindMatrices accessor, the per-vertex matrix as a weighted linear sum of the joint matrices, and the rule that the transform of the skinned mesh node is ignored)"
  - url: https://skinning.org/direct-methods.pdf
    title: Ladislav Kavan, Part I, Direct skinning methods and deformation primitives, in Alec Jacobson, Zhigang Deng, Ladislav Kavan and J. P. Lewis, Skinning, Real-time Shape Deformation, SIGGRAPH 2014 course
    locator: Section 2 (linear blend skinning)
---

The bind pose is the pose of a [character skeleton](/character-skeleton/) in which the skin mesh was attached to it.
The mesh as it was modeled, the **rest mesh**, sits around the skeleton in this pose.
Skinning needs to know where each vertex was relative to each joint at that moment, and the inverse of the world transform of each joint in the bind pose gives exactly that.
Every skinning method of this sub-area, for example [linear blend skinning](/linear-blend-skinning/), starts from these matrices.

## Definition

Let a skeleton with $j$ joints have the world transforms $M_0, \ldots, M_{j-1}$ in its current pose (see [character skeleton](/character-skeleton/) for $M_i = M_{p(i)} L_i$).
The **bind pose** is one fixed pose of the skeleton, chosen when the mesh is attached; its world transforms are $B_0, \ldots, B_{j-1}$.
The **inverse bind matrix** of joint $i$ is $B_i^{-1}$.
It maps a point of the rest mesh, given in model coordinates, to the coordinates of the frame of joint $i$ in the bind pose.

The **skinning matrix** of joint $i$ in the current pose is

$$C_i = M_i\, B_i^{-1}.$$

It maps a rest vertex to the place it would have if it moved rigidly with joint $i$ from the bind pose to the current pose.
Linear blend skinning is $v' = \sum_i w_i\, C_i\, v$ with $w_i \ge 0$ and $\sum_i w_i = 1$.

**Property (proved).**
In the bind pose $M_i = B_i$ for every joint, so $C_i = I$, and any skinning that blends the $C_i$ with weights of sum 1 returns the rest mesh: $\sum_i w_i\, I\, v = v$.
This is the first test of every skinning code on this site.

The inverse bind matrices do not change during the animation, so they are computed once, or stored in the file; glTF stores them in the `inverseBindMatrices` accessor of a skin, in the order of its `joints` array.

### Notation

- $B_i$ is the world transform of joint $i$ in the bind pose, and $M_i$ is its world transform in the current pose.
- Normals move with the inverse transpose of the linear part of the blended matrix, normalized again.
- Points are column vectors, and the world frame is right-handed with $y$ up.

## Examples and non-examples

**One vertex on a forearm.**
Take the shoulder at the origin and the elbow at $(1, 0, 0)$ in the bind pose, with no rotation, so $B_0 = I$ and $B_1 = T(1, 0, 0)$.
The rest vertex $v = (1.5, 0.2, 0)$ has the coordinates $B_1^{-1} v = (0.5, 0.2, 0)$ in the frame of the elbow.
Now bend the elbow by $\pi/2$ about $z$, with the shoulder fixed: $M_1 = T(1, 0, 0)\, R_z(\pi/2)$.
Then $C_1 v = M_1 (0.5, 0.2, 0) = (1, 0, 0) + (-0.2, 0.5, 0) = (0.8, 0.5, 0)$: the vertex keeps its place relative to the elbow.
With the weights $0.5$ on the shoulder and $0.5$ on the elbow, linear blend skinning gives $0.5\, v + 0.5\, C_1 v = (1.15, 0.35, 0)$.

**T-pose and A-pose.**
Characters are often modeled and bound with the arms straight out (a T-pose) or angled down (an A-pose), so that the skin of the armpits and the shoulders is open and easy to weight.

**Non-example: the world transform alone.**
Using $M_1$ in place of $C_1$ applies the offset of the elbow twice: $M_1 v = (0.8, 1.5, 0)$, not $(0.8, 0.5, 0)$.
Even in the bind pose $M_1 v = (2.5, 0.2, 0) \ne v$, so the mesh moves with no animation at all.

**Non-example: a rest pose that is not the bind pose.**
Some tools keep a separate "rest pose" of the skeleton, for example a neutral pose for editing, that differs from the pose in which the mesh was bound.
If the code takes the world transforms of that pose as $B_i$, the skinning matrices are not $I$ when the skeleton is in its true bind pose, and the mesh is deformed before any animation.
The alias "rest pose" of this page is right only when the two poses agree.

**Non-example: a mesh with its own transform.**
In glTF the transform of the node that holds the skinned mesh is ignored, and only the joint transforms move the vertices; applying it as well moves the mesh twice.

## Related definitions

- [Character skeleton](/character-skeleton/): the tree of joints, the local transforms and the world transforms $M_i$.
- [Linear blend skinning](/linear-blend-skinning/) and [dual quaternion skinning](/dual-quaternion-skinning/): they blend the skinning matrices $C_i$, as matrices or as dual quaternions.
- [Character skinning](/character-skinning/): the problem that the bind pose sets up.
- [Forward kinematics](/forward-kinematics/): computes $M_i$ and $B_i$ from the poses; the robotics pages use z up.
- [Automatic rigging](/automatic-rigging/): fits a skeleton into a rest mesh and computes weights, which fixes the bind pose.

### History

The bind pose came with the joint-based skinning of the late 1980s and the 1990s, where each vertex moves with the change of its joints from the attachment pose.
Exchange formats such as glTF store the inverse bind matrices with the skin, so that a viewer does not need the bind pose itself.

## References
