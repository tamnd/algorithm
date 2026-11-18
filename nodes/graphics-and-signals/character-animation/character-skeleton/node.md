---
tag: 2RYEBQ
kind: definition
slug: character-skeleton
name: Character skeleton
aliases:
- joint hierarchy
- bone hierarchy
area: graphics-and-signals/character-animation
level: intro
summary: A tree of joints, each with a transform relative to its parent, whose world transforms are found by multiplying down the tree.
prereqs: [rooted-tree, homogeneous-transformation-matrix]
see_also: [forward-kinematics, bind-pose, skeletal-animation, character-skinning, linear-blend-skinning, two-bone-inverse-kinematics, topological-sort, euler-angles]
sources:
  - url: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
    title: The Khronos Group, glTF 2.0 Specification
    locator: "Section 3.4 (the right-handed frame with y up), Section 3.5.2 (the node hierarchy as disjoint strict trees), Section 3.5.3 (the T * R * S order of a local transform) and Section 3.7.3 (skins and their joints)"
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 4, Forward Kinematics (the product of the transforms along a chain, in the z-up frames of robotics)
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: the chapter on kinematic linkages (hierarchical models and forward kinematics)
---

A character skeleton is the hierarchy of joints that drives a character in [skeletal animation](/skeletal-animation/).
Each joint has a transform relative to its parent, and the world transform of a joint is the product of the transforms on the path from the root to it.
The skeleton is not drawn; it moves the skin through a [skinning](/character-skinning/) method.
It is the same tree as a kinematic chain of a robot in [forward kinematics](/forward-kinematics/), but animation tools store a full transform per joint, with scale, where robotics uses joint angles and fixed link parameters, and the robotics pages use z up.

## Definition

A **character skeleton** with $j$ joints is a rooted tree on the joints $0, \ldots, j - 1$, given by a parent array $p$, together with a **local transform** $L_i$ for each joint $i$.
The root $r$ has $p(r) = -1$; every other joint has a parent $p(i)$.
The skeleton is stored in **parent order** when $p(i) < i$ for every joint $i$ that is not the root, so the root is joint 0.

The local transform is a $4 \times 4$ [homogeneous matrix](/homogeneous-transformation-matrix/) $L_i = T_i R_i S_i$ that acts on column vectors: first the scale $S_i$, then the rotation $R_i$, then the translation $T_i$.
It maps the coordinates of the frame of joint $i$ to those of the frame of its parent.
The **world transform** of joint $i$ is

$$M_i = M_{p(i)}\, L_i, \qquad M_r = L_r,$$

where a model transform of the whole character can be put in front of $M_r$.
The **pose** of the skeleton is the list of its local transforms; animation changes the pose, and the tree stays the same.

In parent order, one pass over $i = 0, 1, \ldots, j - 1$ computes every $M_i$, because $M_{p(i)}$ is ready when joint $i$ comes.
This pass is forward kinematics; it does $j - 1$ matrix products, so it costs $O(j)$ time and $O(j)$ space, with no recursion.

### Notation

- A **bone** is the segment from a joint to one of its children; its length is the length of the translation of the child, when the parent has no scale. Many tools say "bone" for the joint itself.
- The world position of joint $i$ is $M_i (0, 0, 0, 1)^{\mathsf T}$, the origin of its frame.
- A **chain** is a path in the tree, for example shoulder, elbow, wrist.
- The world frame is right-handed with the $y$ axis up.

## Examples and non-examples

**A planar arm.**
Take three joints in parent order: the shoulder 0 at the origin, the elbow 1 with the local translation $(1, 0, 0)$, and the wrist 2 with the local translation $(1, 0, 0)$.
With the rotations $R_0 = R_z(\pi/2)$, $R_1 = R_z(\pi/2)$ and $R_2 = I$, and no scale:
- $M_0 = R_z(\pi/2)$, so the shoulder stays at the origin;
- $M_1 = R_z(\pi/2)\, T(1, 0, 0)\, R_z(\pi/2)$, so the elbow is at $R_z(\pi/2) (1, 0, 0) = (0, 1, 0)$;
- $M_2 = M_1\, T(1, 0, 0)$, so the wrist is at $M_1 (1, 0, 0) = R_z(\pi/2) ((1, 0, 0) + R_z(\pi/2) (1, 0, 0)) = R_z(\pi/2) (1, 1, 0) = (-1, 1, 0)$.

The rotation of the shoulder moves the elbow and the wrist, and the rotation of the elbow moves only the wrist: each joint carries its subtree.

**A humanoid.**
A typical game or film character has its root at the hips, a spine chain to the head, and chains for the arms, the legs and the fingers.
The hips carry the motion of the whole body through the world, so moving the root moves every joint.

**Not in parent order.**
The parent array $p = (-1, 2, 0)$ is a tree, but joint 1 comes before its parent 2, so one pass in index order would use $M_2$ before it is computed.
A [topological sort](/topological-sort/) of the tree, for example a breadth-first order from the root, renumbers it into parent order.
File formats may list the joints in any order; glTF requires only that the node hierarchy is a set of disjoint strict trees, so a loader sorts the joints first.

**Not a skeleton.**
Two hands that hold one stick make a closed loop: the stick has two parents.
A skeleton has no loops, so the loop is a constraint that [inverse kinematics](/inverse-kinematics/) must solve each frame, not part of the hierarchy.

**Not a world transform.**
The product in the wrong order, $L_i M_{p(i)}$, applies the transform of the parent inside the frame of the child.
For the arm above it puts the elbow at $(1, 0, 0)$ and the wrist at $(2, 0, 0)$, in place of $(0, 1, 0)$ and $(-1, 1, 0)$: the rotations no longer carry the subtrees.

## Related definitions

- [Bind pose](/bind-pose/): the pose in which the skin was attached; its world transforms $B_i$ give the inverse bind matrices $B_i^{-1}$ that skinning needs.
- [Forward kinematics](/forward-kinematics/): the map from the pose to the world transforms; for a robot it is written with joint angles, often in the [Denavit-Hartenberg convention](/denavit-hartenberg-convention/).
- [Inverse kinematics](/inverse-kinematics/): the inverse problem, from a target position to a pose; [two-bone IK](/two-bone-inverse-kinematics/) solves one limb in closed form.
- [Euler angles](/euler-angles/): one way to give $R_i$; animation tools use several rotate orders, and [unit quaternions](/unit-quaternion-rotation/) are the usual stored form.
- [Rooted tree](/rooted-tree/): the graph structure under the skeleton.
- [Skinning](/character-skinning/): the problem of moving the mesh with the world transforms of the joints.

### History

Hierarchical models with transforms relative to a parent come from computer graphics of the 1970s and from the kinematics of robot arms.
Character tools added the joint with a full local transform, scale included, and the bind pose for skinning.

## References
