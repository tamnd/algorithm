---
tag: 1BB6ZV
kind: algorithm
slug: pose-space-deformation
name: Pose space deformation
aliases:
- pose-space deformation
area: graphics-and-signals/character-animation
level: advanced
summary: Add sculpted corrective offsets to the skinned mesh, interpolated over the space of poses by radial basis functions.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", j: "the number of joints", k: "the largest number of joints per vertex", m: "the number of example poses"}
  time: {training: "O(m^3 + m^2 n + m n k)", frame: "O(m j + j + n (m + k))"}
  space: {extra: "O(m n + m^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [linear-blend-skinning, radial-basis-function-interpolation]
see_also: [blendshape-model, verbs-and-adverbs, dual-quaternion-skinning, candy-wrapper-artifact, gaussian-process, bounded-biharmonic-weights, skinning-decomposition, delta-mush]
sources:
  - paper: doi:10.1145/344779.344862
    title: "J. P. Lewis, Matt Cordner and Nickson Fong, Pose space deformation: a unified approach to shape interpolation and skeleton-driven deformation, SIGGRAPH 2000, 165-172"
    locator: the sections on scattered interpolation over the pose space with Gaussian radial basis functions, and on applying the correction in the rest frame before skeleton subspace deformation (general locator)
  - url: https://skinning.org/direct-methods.pdf
    title: Ladislav Kavan, Part I, Direct skinning methods and deformation primitives, in Alec Jacobson, Zhigang Deng, Ladislav Kavan and J. P. Lewis, Skinning, Real-time Shape Deformation, SIGGRAPH 2014 course
    locator: the discussion of the artifacts of linear blend skinning that example-based corrections fix (general locator)
---

Pose space deformation (PSD) fixes the shapes that [linear blend skinning](/linear-blend-skinning/) gets wrong, such as a collapsing elbow or a flat biceps.
An artist poses the skeleton, sculpts the mesh as it should look in that pose, and stores the result as an example.
PSD turns each sculpt into a corrective offset in the rest frame of the mesh, and at any new pose it computes the offset by [radial basis function interpolation](/radial-basis-function-interpolation/) over the pose space.
The corrected rest mesh then goes through the skinning as usual.
Lewis, Cordner and Fong (2000) introduced the method, and it is the base of most corrective shape systems in production rigs.

## In plain words

Skinning gives a good shape for most poses, but not for all of them.
For the poses where it fails, an artist fixes the mesh by hand: these are the examples.
Now the character moves to a pose that is between the examples.
PSD asks how close the new pose is to each example, and mixes the fixes by that closeness.
Near an example, its fix counts the most; far from all examples, no fix applies and the plain skinning shows.
The fixes are stored as if the character were in its rest pose, and they are added before the skinning.
So a fix made with the arm bent still sits on the right part of the arm when the arm also turns.

## The problem

The input is a skinned mesh: rest vertices $v_i$, skinning weights, and the bind transforms of $j$ joints, as for [linear blend skinning](/linear-blend-skinning/).
A pose is a vector $p \in \mathbb{R}^d$ of joint parameters, for example joint angles.
The artist gives $m$ example poses $p_1, \ldots, p_m$ and for each a sculpted mesh $s_{e,i}$ in the posed space.
The output is a function that maps any pose $p$ to a mesh that equals the sculpt at every example pose, equals the plain skinning where no example is near, and varies smoothly in between.

Let $A_i(p) = \sum_j w_{ij} M_j(p) B_j^{-1}$ be the blended skinning matrix of vertex $i$, so that plain skinning gives $A_i(p) v_i$.
The kernel is the Gaussian $\varphi(r) = \exp(-r^2 / (2\sigma^2))$.
The width $\sigma$ is tuning: it sets how far the influence of an example reaches in pose space.

## The algorithm

```pseudo id=main
PSD-TRAIN(v, A, p₁ … p_m, s₁ … s_m, σ)
L1  for each example e and vertex i: d_e,i ← A_i(p_e)⁻¹ s_e,i - vᵢ   ▷ the correction in the rest frame
L2  Φ_ef ← φ(‖p_e - p_f‖) for all pairs of examples
L3  solve Φ C = D                                    ▷ one coefficient per example, vertex and coordinate
PSD-DEFORM(p)
L4  for each example e: r_e ← φ(‖p - p_e‖)
L5  for each vertex i do
L6      uᵢ ← vᵢ + Σ_e r_e C_e,i                      ▷ the corrected rest vertex
L7      v′ᵢ ← A_i(p) uᵢ                              ▷ plain skinning of the corrected vertex
L8  return v′
```

Line L1 inverts the skinning of each sculpted vertex.
The sculpt tells where the vertex must be in the posed space, and $A_i(p_e)^{-1}$ maps that point back to the rest frame, where the correction is a fixed offset.
Lines L2 and L3 are RBF interpolation: one dense $m \times m$ matrix for all vertices, with $2n$ right-hand sides in 2D (or $3n$ in 3D).
Lines L4 to L7 run every frame.

The code in `impl/python` does this for a planar chain of two joints with LBS in homogeneous $3 \times 3$ form.
The paper uses skeleton subspace deformation, its name for LBS, as the base layer; any skinning that is invertible per vertex works the same way.

## Example

Take one joint angle $\theta$ and one vertex, and track only the size $c$ of its correction along the normal.
The examples are $\theta_1 = 0$ with $c = 0$ (the rest pose needs no fix) and $\theta_2 = \pi / 2$ with $c = 0.1$ (a bulge at the bent elbow), with $\sigma = 0.5$.

Then $\varphi_{12} = \exp(-(\pi/2)^2 / 0.5) = 0.0071919$, and $\Phi C = (0, 0.1)$ gives $C_1 = -0.1\,\varphi_{12} / (1 - \varphi_{12}^2) = -0.00071923$ and $C_2 = 0.1 / (1 - \varphi_{12}^2) = 0.10000517$.

| $\theta$ | correction |
|---|---|
| $0$ | $0$ |
| $\pi/8$ | $0.005702$ |
| $\pi/4$ | $0.028913$ |
| $3\pi/8$ | $0.073419$ |
| $\pi/2$ | $0.1$ |
| $3\pi/4$ | $0.029123$ |
| $\pi$ | $0.000719$ |

The correction is exact at both examples and falls off on both sides of $\pi/2$.
At $\pi/4$, halfway, it is $0.1\, r / (1 + \varphi_{12}) = 0.028913$ with $r = \exp(-(\pi/4)^2/0.5) = 0.29121$, much less than the half of 0.1 that linear interpolation would give.
That is a property of the Gaussian with this $\sigma$, and a wider $\sigma$ gives a value closer to 0.05.
The tests in `impl/python` check these numbers and the full 2D case.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
They hold in exact arithmetic, for distinct example poses and invertible blended matrices $A_i(p_e)$.
- **The system has one solution.** The Gaussian kernel is strictly positive definite on $\mathbb{R}^d$, so $\Phi$ is symmetric positive definite for distinct poses. This is a proved property of the Gaussian (a theorem of Bochner type, see [radial basis function interpolation](/radial-basis-function-interpolation/)).
- **Examples are reproduced.** At $p = p_e$, the interpolant gives $d_{e,i}$, so line L7 gives $A_i(p_e)(v_i + d_{e,i}) = s_{e,i}$, the sculpt.
- **No sculpt, no change.** If every sculpt equals plain skinning, every $d_{e,i} = 0$, so $C = 0$ and PSD equals plain skinning at every pose.
- **Far poses.** The correction is bounded by $\sum_e |C_{e,i}|\, \varphi(\operatorname{dist}(p, \{p_e\}))$, which tends to 0 as $p$ moves away from all examples.
- **Corrections move with the bones.** Because the offset is added before skinning, a rigid motion of the whole skeleton moves the corrected shape rigidly. An offset added after skinning, in world space, does not.

The tests check all of these, the last one by turning the root joint of the chain.

## Complexity

The costs are in the real RAM model.
Line L1 costs $O(m n k)$ to build and invert the blended matrices.
Line L2 costs $O(m^2 d)$, and line L3 costs $O(m^3)$ to factor $\Phi$ plus $O(m^2 n)$ for the right-hand sides.
Per frame, line L4 costs $O(m d)$, lines L5 and L6 cost $O(n m)$, and line L7 costs $O(j + n k)$ as for LBS.
The extra space is $O(m n)$ for the coefficients and $O(m^2)$ for $\Phi$.
In practice $m$ is small for each region (a few examples per joint), and the corrections are sparse in $i$, so a rig stores them like [blendshape](/blendshape-model/) deltas.

## Properties

- Interpolating: every example pose gives its sculpt exactly.
- Local in pose space with a Gaussian kernel; the reach is set by $\sigma$.
- Linear in the sculpts: the result depends linearly on the corrections $d$.
- Not local on the mesh unless the sculpts are: every example can move every vertex.
- Works with any base skinning that is invertible per vertex, for example LBS or [dual quaternion skinning](/dual-quaternion-skinning/).
- The pose space is the space of joint parameters, so the distance depends on the parameterization. Angles that wrap at $2\pi$ need care.

## Variants and improvements

- **Other kernels.** Lewis and others use Gaussians; thin-plate splines and other radial functions with a polynomial term also work, and they extrapolate instead of falling to 0. The choice changes the result between and outside the examples.
- **Per joint pose spaces.** A correction near the elbow should depend on the elbow angle only. Using a small pose vector per region keeps $d$ and $m$ small and stops unrelated joints from changing the correction.
- **Weighted PSD.** Later work weights the interpolation per vertex by the skinning weights, so that each vertex reacts to the joints that move it. That is a variant, not part of the original paper.
- **Probabilistic interpolation.** The RBF interpolant with a Gaussian kernel is the mean of a [Gaussian process](/gaussian-process/) with that covariance and no noise; adding a noise term gives a smoother fit that no longer reproduces the examples exactly.
- **Related interpolation of motions.** [Verbs and adverbs](/verbs-and-adverbs/) interpolates whole motions over a space of style parameters with radial basis functions, in the same way.
- **Corrective shapes from data.** Instead of sculpting, the examples can come from scans or simulation, and [skinning decomposition](/skinning-decomposition/) can give the base layer.

## When to use it

Use PSD when the skinning of a character is good in most poses and needs sculpted fixes in a few, for example at the elbows, knees, shoulders and hips.
It is the right tool when the artist wants exact control over a shape in given poses.
If the problem is the volume loss of LBS at twisted joints, try [dual quaternion skinning](/dual-quaternion-skinning/) first, and use PSD for the shapes that remain wrong.

## Pitfalls

- **Correcting in world space.** Adding the interpolated offsets after skinning breaks as soon as the limb also turns, because the offset does not turn with it. Invert the skinning as in line L1, and add the offset before skinning.
- **Singular blended matrices.** $A_i(p_e)$ can be close to singular at a strongly twisted LBS joint, and then line L1 amplifies small sculpting noise. Avoid examples at the collapse pose, or use a rigid base skinning there.
- **Close examples.** Two examples with nearly equal poses make $\Phi$ ill conditioned, and the coefficients large and of opposite sign. Merge them, or use a wider or a regularized kernel.
- **$\sigma$ too small or too large.** Too small, and the corrections appear only very near the examples and the mesh pops in between. Too large, and $\Phi$ becomes ill conditioned and the examples influence each other far away. Tune $\sigma$ per region, and in the units of the pose vector.
- **No rest example.** Without an example at the rest pose with zero correction, the corrections of the other examples leak into the rest pose. Add the rest pose as an example.

## Implementations

## History

Before PSD, production rigs mixed two separate ideas: shape interpolation between sculpted keys, driven by hand or by simple joint-angle rules, and skeleton-driven skinning.
Lewis, Cordner and Fong (2000) joined them: they treated the sculpts as samples of a function on the pose space, interpolated them by radial basis functions, and applied the result in the rest frame before skinning.
Their paper also pointed out why the correction must be applied before skinning and not after it.

## References
