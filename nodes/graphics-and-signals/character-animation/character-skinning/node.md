---
tag: RJPPJ9
kind: problem
slug: character-skinning
name: Character skinning
aliases:
- mesh skinning
area: graphics-and-signals/character-animation
level: intro
summary: Deform the surface mesh of a character from the transforms of its skeleton joints, smoothly and without artifacts at the joints.
prereqs: [character-skeleton, bind-pose]
see_also: [linear-blend-skinning, dual-quaternion-skinning, spherical-blend-skinning, optimized-centers-of-rotation-skinning, implicit-skinning, delta-mush, candy-wrapper-artifact, skeletal-animation]
sources:
  - url: https://skinning.org/direct-methods.pdf
    title: Ladislav Kavan, Part I, Direct skinning methods and deformation primitives, in Alec Jacobson, Zhigang Deng, Ladislav Kavan and J. P. Lewis, Skinning, Real-time Shape Deformation, SIGGRAPH 2014 course
    locator: "Section 2 (linear blend skinning and the candy wrapper artifact) and Section 4 (dual quaternion blending and the bulging artifact)"
  - paper: doi:10.1145/1409625.1409627
    title: Ladislav Kavan, Steven Collins, Jiří Žára and Carol O'Sullivan, Geometric skinning with approximate dual quaternion blending, ACM Transactions on Graphics 27(4), article 105, 2008
    locator: "Section 2 (previous skinning methods) and Section 2.2 (linear blend skinning)"
  - url: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
    title: The Khronos Group, glTF 2.0 Specification
    locator: "Section 3.7.3 (skins, inverse bind matrices, and sets of four joints and weights per vertex)"
---

Character skinning is the problem of moving the skin mesh of a character with its [skeleton](/character-skeleton/).
The skeleton gives a rigid transform per joint in each frame, and the skin must follow it: rigid where a part of the body is rigid, smooth across the joints, with no loss of volume and no folds where none belong.
There is no single correct answer, because a real limb is not a function of its joints alone; methods are judged by the properties they prove, by their artifacts and by their cost per frame.
It is a special case of [shape deformation](/shape-deformation/), where the handles are the joints of a skeleton; the methods for it are on the algorithm pages listed below.

## In plain words

A character has a skin made of many small triangles and an inner skeleton made of a few joints.
When the joints move, every point of the skin must move too, in a way that looks right.
Points in the middle of the upper arm should move with the upper arm.
Points near the elbow should move partly with the upper arm and partly with the forearm, so that the skin bends smoothly.
The hard part is to bend and twist the skin without making it thin, flat or crumpled at the joints, and to do it many times per second for many characters.

## Definition

**Input.**
- The rest mesh: $n$ vertices $v_1, \ldots, v_n$ with their normals and $f$ triangles, in the [bind pose](/bind-pose/).
- The skeleton with $j$ joints, the world transforms $B_0, \ldots, B_{j-1}$ of the bind pose and, in each frame, the world transforms $M_0, \ldots, M_{j-1}$ of the pose; together they give the skinning matrices $C_a = M_a B_a^{-1}$.
- The weights: for each vertex $i$ at most $k$ pairs $(a, w_{ia})$ with $w_{ia} \ge 0$ and $\sum_a w_{ia} = 1$.

**Output.** The deformed positions $v'_1, \ldots, v'_n$ and normals of the frame.

**Requirements.** A method should meet these; the first three are exact properties that a page can prove.
1. In the bind pose, where every $C_a = I$, the output is the rest mesh.
2. A vertex with one joint of weight 1 moves rigidly with that joint: $v' = C_a v$.
3. If every joint moves by the same rigid motion $G$, the mesh moves by $G$.
4. The output depends smoothly on the pose and on the weights.
5. The volume near a joint is kept in a bend and a twist (no [candy wrapper artifact](/candy-wrapper-artifact/), no collapsing elbow), and there is no bulge where none belongs.
6. Optionally: the skin does not pass through itself, and it bulges where parts press together.

**Cost model.** The real-RAM model; the cost per frame is given in $n$, $j$ and $k$, apart from a precomputation that runs once for the rest mesh.
The weights are given here; finding them is a separate problem (see Variants).

## Variants

- **Rigging.** Find the skeleton and the weights for a rest mesh; see [automatic rigging](/automatic-rigging/) and [bounded biharmonic weights](/bounded-biharmonic-weights/).
- **Skinning decomposition.** The inverse problem: given example meshes, find the weights and the joint transforms that best reproduce them (see [skinning decomposition](/skinning-decomposition/)).
- **Example-based skinning.** Given sculpted meshes at some poses, interpolate corrections over the pose space (see [pose-space deformation](/pose-space-deformation/)).
- **Skinning with contact.** Add requirement 6, as [implicit skinning](/implicit-skinning/) does.
- **Skinning with scale.** Allow scale in the joint transforms, as for stretchy cartoon limbs; this rules out methods that blend only rigid transforms.

## Examples

**The twist.**
Take two joints with the weights $0.5$ and $0.5$, where joint 0 stays at the identity and joint 1 turns by $\pi$ about the $x$ axis.
The vertex $(0, 1, 0)$ should turn by $\pi/2$, to $(0, 0, 1)$, since it lies halfway in weight.
Linear blend skinning gives $0.5 (0, 1, 0) + 0.5 (0, -1, 0) = (0, 0, 0)$: the vertex falls onto the axis.
Dual quaternion skinning gives $(0, 0, 1)$ and keeps the radius 1.

**The bend.**
Take the elbow at $(1, 0, 0)$, joint 0 at the identity and joint 1 bent by $\pi/2$ about the $z$ axis through the elbow, and the vertex $(1.5, 0.2, 0)$ with the weights $0.5$ and $0.5$; it is at the distance $0.53852$ from the elbow.
LBS gives $(1.15, 0.35, 0)$, at the distance $0.38079$ from the elbow.
DQS gives $(1.21213, 0.49497, 0)$, a turn by $\pi/4$ about the elbow, at the distance $0.53852$.

## Known algorithms

| method | per frame | precomputation | main property and limit |
|---|---|---|---|
| [linear blend skinning](/linear-blend-skinning/) | $O(j + n k)$ | none | requirements 1 to 4; loses volume in twists and bends |
| [dual quaternion skinning](/dual-quaternion-skinning/) | $O(j + n k)$ | none | each vertex moves rigidly when the blended real part is not zero; bulges in bends, does not blend scale |
| [spherical blend skinning](/spherical-blend-skinning/) | $O(j + n k)$ plus one center per set of joints | none | rigid per vertex, about a least squares center of rotation |
| [optimized centers of rotation](/optimized-centers-of-rotation-skinning/) | $O(j + n k)$ | a center per vertex from the similarity of the weights | rigid rotation about the center; the paper reports less bulge than DQS |
| [implicit skinning](/implicit-skinning/) | $O(j + n (k + i j))$ for $i$ projection steps | a field per bone | a correction with contact and bulges; iterative |
| [delta mush](/delta-mush/) | $O(j + n k + K (n + f))$ for $K$ smoothing steps | the deltas of the rest mesh | a correction that hides rough weights; does not keep the radius in a twist |
| [pose-space deformation](/pose-space-deformation/) | the correction of the examples near the pose | sculpted examples | adds artist-made shapes on top of a skinning |

The first four are direct methods: each vertex is a function of its own weights, its rest position and the palette.
The last three use the mesh or extra data.

## Bounds

- **Lower bound.** Every output vertex depends on its weights, so a method that reads them needs $\Omega(n k)$ time per frame in the worst case, and the palette needs $\Omega(j)$. LBS and DQS meet this bound.
- **No linear blend is rigid.** A weighted average of rotation matrices is not a rotation in general, so no method that blends the matrices $C_a$ linearly meets requirement 5 for every pose; see [candy wrapper artifact](/candy-wrapper-artifact/) for the proof.
- **Direct methods cannot model contact.** In a direct method, two vertices with the same rest position and the same weights move together in every pose, whatever the rest of the mesh does; so the inner side of a bend cannot stop at the other side, and requirement 6 needs a method that looks at the mesh.

## Reductions

- **LBS is a matrix product.** Stack the top three rows of the matrices $C_a$ side by side into a $3 \times 4j$ matrix $C$, and let $A$ be the $4j \times n$ matrix whose column $i$ has the block $w_{ia} (v_i, 1)$ at the rows of joint $a$. Then the deformed vertices are the columns of $C A$. This is the form that skinning decomposition fits.
- **Skinning as shape deformation.** A skinning method is a deformation with $j$ rigid handles and fixed weights per vertex, so the methods of [shape deformation](/shape-deformation/) with handles apply, at a higher cost.
- **Skinning of one limb from two joints.** The two-joint twist and bend above are the test cases of every method; a method that fails them fails on characters.

## Applications

- Real-time characters in games and VR, skinned on the GPU from a palette of joint matrices; glTF stores up to four joints and weights per vertex in each set of attributes.
- Film characters, where a fast skinning gives the base and corrections, simulation and sculpted shapes go on top.
- Bodies for cloth and hair simulation, which need the skinned mesh as a collision surface.
- [Skeletal animation](/skeletal-animation/) in general: retargeted motion capture and crowds reuse one skinned mesh for many motions.

## References
