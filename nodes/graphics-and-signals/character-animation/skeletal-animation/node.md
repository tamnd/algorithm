---
tag: K2Q2Q7
kind: technique
slug: skeletal-animation
name: Skeletal animation
aliases:
- skeleton animation
- bone animation
area: graphics-and-signals/character-animation
level: intro
summary: Animate a character by moving the joints of a hierarchical skeleton and deriving the surface from it, rather than moving every vertex.
prereqs: [character-skeleton, bind-pose, keyframe-interpolation]
see_also: [character-skinning, linear-blend-skinning, two-bone-inverse-kinematics, forward-kinematics, spherical-linear-interpolation, motion-blending, blendshape-model, candy-wrapper-artifact]
sources:
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: the chapters on kinematic linkages and on the animation of articulated figures
  - url: https://skinning.org/direct-methods.pdf
    title: Ladislav Kavan, Part I, Direct skinning methods and deformation primitives, in Alec Jacobson, Zhigang Deng, Ladislav Kavan and J. P. Lewis, Skinning, Real-time Shape Deformation, SIGGRAPH 2014 course
    locator: Section 2 (linear blend skinning)
  - url: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
    title: The Khronos Group, glTF 2.0 Specification
    locator: "Section 3.5 (nodes, the hierarchy and the T * R * S transforms) and Section 3.7.3 (skins, inverse bind matrices, and sets of four joints and weights per vertex)"
---

Skeletal animation moves a character through a small [skeleton](/character-skeleton/) of joints, not through its mesh.
An animator, a motion capture system or a controller gives the local transforms of a few tens of joints per frame; [forward kinematics](/forward-kinematics/) turns them into world transforms; and a [skinning](/character-skinning/) method moves the thousands of vertices of the skin from those transforms.
The motion data is small, it can be reused on every mesh bound to the same skeleton, and inverse kinematics and blending work on joints, where they are simple.
It differs from [blendshapes](/blendshape-model/), which store whole meshes and mix them; faces often use both.

## In plain words

Moving every point of a character's skin by hand, frame by frame, would take forever.
So the character gets an inner skeleton, like a puppet with a frame of sticks inside.
Each point of the skin is tied to one or a few of the sticks.
The animator only moves the sticks: the hips, the knees, the elbows.
The computer then works out where every stick is, and moves each point of the skin along with the sticks it is tied to.
One walk made for the skeleton can drive any character built on the same skeleton.

## When it applies

- The character is articulated: its motion is close to rigid pieces that turn at joints, as for people, animals and robots.
- The motion comes as joint data: keyframes, motion capture, physics on rigid bodies, or a controller.
- The frame budget is tight: the per-frame work is $O(j)$ for the skeleton and $O(n k)$ for the skin, with $j$ joints, $n$ vertices and $k$ joints per vertex, and the skin step runs well on a GPU.
- It fits badly where the shape does not follow rigid parts: faces, cloth, hair, and soft tissue that jiggles. There, blendshapes, simulation, or [corrective shapes](/pose-space-deformation/) go on top.

## The template

1. **Build the skeleton.** Make the tree of joints, and store it as an array in parent order, so that every parent comes before its children.
2. **Bind the skin.** Pick the [bind pose](/bind-pose/), store the inverse bind matrices $B_i^{-1}$, and give each vertex its joints and weights, painted or computed (see [automatic rigging](/automatic-rigging/) and [bounded biharmonic weights](/bounded-biharmonic-weights/)).
3. **Author the motion.** Store a clip as keys of the local transform of each joint over time: a rotation, usually a unit quaternion, a translation for the root and maybe for other joints, and a scale if needed.
4. **Sample the pose.** At the frame time, interpolate the keys of each joint (see [keyframe interpolation](/keyframe-interpolation/)); rotations use [slerp](/spherical-linear-interpolation/) or normalized linear interpolation after the sign alignment of the quaternions.
5. **Mix and correct.** Blend several clips per joint ([motion blending](/motion-blending/)), then fix contacts with inverse kinematics, for example [two-bone IK](/two-bone-inverse-kinematics/) on each leg.
6. **Run forward kinematics.** One pass over the array computes $M_i = M_{p(i)} L_i$ with $L_i = T_i R_i S_i$.
7. **Build the palette.** Compute the skinning matrices $C_i = M_i B_i^{-1}$, one per joint.
8. **Skin the mesh.** Move each vertex with its weights and the palette, by [linear blend skinning](/linear-blend-skinning/) or [dual quaternion skinning](/dual-quaternion-skinning/), and move the normals with the inverse transpose of the blended linear part.

Steps 4 to 7 cost $O(j)$ per frame, and step 8 costs $O(n k)$.
A clip of $f$ frames stores $O(f j)$ values, against $O(f n)$ for the vertex positions of every frame.

## Classic examples

**Joints are interpolated, not vertices.**
Take the forearm of the [bind pose](/bind-pose/) page: the elbow at $(1, 0, 0)$ and the vertex $v = (1.5, 0.2, 0)$ with the weight 1 on the elbow, at the distance $0.53852$ from it.
One key has the elbow straight, the next has it bent by $\pi/2$ about $z$, where the vertex is at $(0.8, 0.5, 0)$.
Halfway, slerp gives the bend $\pi/4$, and the vertex is at $(1.21213, 0.49497, 0)$, still at the distance $0.53852$ from the elbow.
Linear interpolation of the two vertex positions gives $(1.15, 0.35, 0)$, at the distance $0.38079$: the forearm would shrink in the middle of the motion.

**A walk cycle.**
A loop of keys for the hips, the legs and the arms plays over and over, while the root moves the character forward.
Two-bone IK pins each foot to the ground during its contact, so that the feet do not slide; [footskate cleanup](/footskate-cleanup/) is the general fix for captured motion.

**GPU skinning in a game.**
The CPU or a compute pass samples the clips and runs FK for each character, then uploads the palette of $C_i$; the vertex shader blends up to four joints per vertex.
glTF stores the joints and weights of a vertex in sets of four, which matches this layout.

**Motion capture.**
Markers on an actor are fitted to a skeleton each frame, which gives joint rotations; the same data then drives any character with that skeleton, or with a mapped one (see [motion retargeting](/motion-retargeting/)).

## Variations

- **Skinning method.** LBS is the fast default; DQS removes the [candy wrapper artifact](/candy-wrapper-artifact/) of twists; [delta mush](/delta-mush/) and [implicit skinning](/implicit-skinning/) correct the result.
- **Corrective shapes.** Shapes that fade in with the pose fix the faults of skinning at elbows and shoulders ([pose-space deformation](/pose-space-deformation/)).
- **Helper joints.** Extra joints, such as twist joints in the forearm, driven by rules from the main joints, spread a twist over more of the limb.
- **Procedural and physical motion.** Inverse kinematics, look-at rules and ragdoll physics set some joints each frame in place of the clip.
- **Additive layers.** A clip stores the difference to a reference pose, and it is added on top of another clip, for example breathing on top of a walk.
- **Compression.** Clips are stored with fewer keys and fewer bits per key, because the frame count times the joint count can be large.

## Pitfalls

- **Wrong product order.** $M_i = M_{p(i)} L_i$, not $L_i M_{p(i)}$; and $L = T R S$, so the scale acts first.
- **Joint order.** One pass of FK needs the parent first; sort the joints of a file before use.
- **Euler angle keys.** Interpolating [Euler angles](/euler-angles/) gives curved, uneven paths and fails near [gimbal lock](/gimbal-lock/); interpolate quaternions.
- **Quaternion signs.** $q$ and $-q$ are the same rotation; without the sign flip, slerp takes the long way round.
- **Non-uniform scale on a parent.** With $L = T R S$, a non-uniform scale of a parent shears the rotated frames of its children; many tools keep the scale uniform or do not pass it down.
- **Missing inverse bind matrices.** Skinning with $M_i$ in place of $M_i B_i^{-1}$ moves the mesh even in the bind pose.
- **Weights.** The weights of a vertex must be nonnegative with the sum 1; after quantization, normalize them again.

## Exercises

1. A skeleton has the parent array $(-1, 0, 1, 1, 0)$. Is it in parent order, and which joints move when joint 1 turns?
   *Answer.* Yes, every parent index is smaller than its child. Joint 1 and its subtree, joints 2 and 3, move; joints 0 and 4 do not.
2. In the arm of the first example, the shoulder at the origin also turns by $\pi/2$ about $z$ while the elbow is bent by $\pi/2$. Where is the vertex $v$?
   *Answer.* $R_z(\pi/2) (0.8, 0.5, 0) = (-0.5, 0.8, 0)$, because the whole arm turns about the origin.
3. A character has 60 joints and 20000 vertices with 4 joints each. Count the matrix products of FK and the matrix-vector products of LBS per frame.
   *Answer.* 59 products for FK and 60 more for the palette, against 80000 for the skin: the skin step dominates.
4. Why does a clip made on one skeleton look wrong on a skeleton with longer legs, even with the same joint rotations?
   *Answer.* The rotations are the same, but the translations of the root and the positions of the feet scale with the legs, so the feet slide or float; this is the subject of motion retargeting.

## References
