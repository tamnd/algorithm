---
tag: 3M9YWE
kind: algorithm
slug: example-based-facial-rigging
name: Example-based facial rigging
aliases:
- example-based blendshape generation
area: graphics-and-signals/character-animation
level: research
summary: Generate a personalized blendshape rig from a few example expressions of an actor by optimizing the targets with a generic rig as prior.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {n: "the number of targets", m: "the number of examples", T: "the number of triangles", V: "the number of vertices", I: "the number of alternations", K: "the number of coordinate descent sweeps per weight step"}
  time: {total: "O(I (T n (n + m) + n^3 + m n^2 K) + V^3 + n V^2)"}
  space: {extra: "O(T (n + m) + V^2 + n V)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [blendshape-model, deformation-transfer]
see_also: [facial-action-coding-system, blendshape-direct-manipulation, deformation-gradient, least-squares-problem, coordinate-descent, poisson-equation, laplacian-surface-editing, pose-space-deformation]
sources:
  - paper: doi:10.1145/1778765.1778769
    title: "Hao Li, Thibaut Weise and Mark Pauly, Example-based facial rigging, ACM Transactions on Graphics 29(4), SIGGRAPH 2010, article 32"
    locator: "the optimization of the actor targets in deformation gradients with the generic rig as a prior, the alternation with the blend weights of the examples, and the reconstruction of the vertex positions"
---

Example-based facial rigging builds a [blendshape](/blendshape-model/) rig for one actor from a generic rig and a few scans of the actor's face.
A good face rig has dozens of targets, such as "jaw open" or "left smile", and modeling them by hand for each actor takes days.
A scan of the actor making an expression is easy to get, but a scan is a mix of many targets at once, not a single target.
Li, Weise and Pauly (2010) start from the [deformation transfer](/deformation-transfer/) of a generic rig onto the actor's neutral face, and then change the targets so that suitable blends of them reproduce the scans, while each target stays close to its generic counterpart.

## In plain words

A generic face rig knows what "open the jaw" or "smile" does to a face, but not how this actor does it.
You have a few scans of the actor making faces, and a rough guess of how much of each target is in each scan.
First, copy each generic target onto the actor with deformation transfer.
Then improve two things in turn.
Change the targets so that the blends with the current weights look like the scans, but do not let a target drift far from what the generic one does.
Then change the weights so that the blends of the new targets fit the scans better, with every weight between 0 and 1.
Repeat a few times.
The work is done on how each triangle stretches and turns, and at the end one linear solve turns that back into vertex positions.

## The problem

The input is:
- a generic rig with the neutral face $A_0$ and the targets $A_1, \ldots, A_n$;
- the neutral face $B_0$ of the actor;
- $m$ example expressions $S_1, \ldots, S_m$ of the actor;
- a first guess $\alpha^0_j \in [0, 1]^n$ of the blend weights of each example.

All meshes share one triangulation, which the method needs, for example after a template is fitted to each scan.
The output is the actor targets $B_1, \ldots, B_n$ and the weights $\alpha_j$ of the examples.

For a triangle $t$, the [deformation gradient](/deformation-gradient/) of a mesh $X$ relative to $B_0$ is the matrix $F_t(X)$ that maps the edges of the triangle in $B_0$ to its edges in $X$.
Let $D_{i,t} = F_t(B_i) - I$ be the unknowns, $R_{j,t} = F_t(S_j) - I$ the examples, and $H_{i,t} = G_{i,t} - I$ the prior, where $G_{i,t}$ is the gradient of the generic target $A_i$ relative to $A_0$.
The method minimizes
$$E(D, \alpha) = \sum_j \sum_t \Big\lVert \sum_i \alpha_{ij} D_{i,t} - R_{j,t} \Big\rVert_F^2 + \beta \sum_i \sum_t \lVert D_{i,t} - H_{i,t} \rVert_F^2$$
subject to $0 \le \alpha_{ij} \le 1$.
The first term is the fit to the examples, and the second is the prior from the generic rig.
With $D = H$, each target changes its triangles like the generic target, which is deformation transfer for meshes with one triangulation.

The code in `impl/python` works on 2D triangle meshes and uses this energy only.
The paper works on 3D face meshes, and its energy has more detail than this one, for example in how the prior is weighted; this page keeps the structure of the method.

## The algorithm

```pseudo id=main
EXAMPLE-BASED-RIG(A₀ … Aₙ, B₀, S₁ … Sₘ, α⁰, β)
L1  H_i ← gradients of A_i relative to A₀, minus I;  D ← H
L2  R_j ← gradients of S_j relative to B₀, minus I;  α ← α⁰
L3  repeat a fixed number of times:
L4      D ← argmin_D E(D, α)                     (one linear solve)
L5      α_j ← argmin over [0, 1]ⁿ of E(D, α), for each j
L6      record E(D, α)
L7  B_i ← the mesh whose gradients fit I + D_i in least squares, with one vertex fixed
L8  return B₁ … Bₙ and α
```

Line L4 separates into one small problem per entry of the 2 by 2 (or 3 by 3) matrices.
For an entry $p$ of triangle $t$, the vector $z = (D_{1}[p], \ldots, D_{n}[p])$ solves
$$(A^\top A + \beta I) z = A^\top (R_1[p], \ldots, R_m[p]) + \beta (H_1[p], \ldots, H_n[p]),$$
where $A$ is the $m$ by $n$ matrix of the weights.
The matrix $A^\top A + \beta I$ is the same for every entry, so the code solves it once with all entries as right hand sides.

Line L5 is a [least squares problem](/least-squares-problem/) with bounds, one per example, with the Gram matrix of the targets.
The code solves it by cyclic [coordinate descent](/coordinate-descent/): it sets each weight to its exact minimizer, clipped to $[0, 1]$, until no weight moves.

Line L7 is the Poisson step of deformation transfer: the vertex positions of $B_i$ minimize $\sum_t \lVert F_t(B_i) - (I + D_{i,t}) \rVert_F^2$, which is a sparse [Poisson](/poisson-equation/) type system whose matrix depends only on $B_0$.

## Example

The tests use a strip of six vertices and four triangles.
The generic rig has a target "open", which stretches the top row up by 50 percent, and a target "smile", which shears the right side.
The actor has a different neutral face and true targets that differ from the transferred generic ones.
There are three examples, made with the true weights $(1, 0)$, $(0, 1)$ and $(0.6, 0.5)$, and the first guesses are $(0.9, 0.1)$, $(0.1, 0.8)$ and $(0.5, 0.5)$.

With $\beta = 0.1$ and 30 alternations, $E$ falls from $1.523$ at the start to $0.175$ after the first step and to $0.077$ at the end.
The largest vertex error of the targets is:

| target | deformation transfer | example-based rig |
|---|---|---|
| open | 0.286 | 0.026 |
| smile | 0.347 | 0.032 |

The weights become $(1, 0.021)$, $(0, 1)$ and $(0.625, 0.534)$, close to the true ones.

Two check values.
For one target, one example and one entry, line L4 gives $z = (\alpha r + \beta h) / (\alpha^2 + \beta)$; with $\alpha = 0.5$ and $\beta = 0.25$, this is $z = r + h / 2$.
For one target, line L5 gives the weight $\operatorname{clip}(d^\top r / d^\top d, 0, 1)$; with $d = (1, 0, 0, 0)$, the entries $r_1 = 2$, $0.3$ and $-0.4$ give the weights 1, 0.3 and 0.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
- **Line L4 is exact.** For $\beta > 0$, $A^\top A + \beta I$ is positive definite, so the step is the unique minimizer of $E$ in $D$ for the fixed weights.
- **Line L5 does not increase $E$, and converges to the minimizer.** Each coordinate update is an exact minimization of a convex function of one variable on $[0, 1]$, and coordinate descent on a convex quadratic with box constraints reaches the minimizer. The tests compare it with a brute force search over all faces of the box.
- **$E$ never increases.** Both steps minimize $E$ in one block of variables, so the sequence of values is nonincreasing, and it converges, because $E \ge 0$.
- **The generic rig is a fixed point.** If the actor is the generic face and the examples are exact blends of the generic targets with the given weights, then $E = 0$ at the start, and the method returns the generic targets and the given weights.
- **Line L7 is exact for exact gradients.** If the gradients come from a mesh, the least squares solution is that mesh, up to the fixed vertex.

The method finds a local minimum of a nonconvex problem in $(D, \alpha)$, and the result depends on the first guess of the weights.

## Complexity

The costs are in the real RAM model.
One step of line L4 costs $O(T n m)$ to form the right hand sides, $O(n^3)$ to factor the matrix and $O(T n^2)$ to solve for all entries.
One step of line L5 costs $O(T n^2)$ for the Gram matrix, $O(T n m)$ for the right hand sides and $O(m n^2 K)$ for $K$ sweeps of coordinate descent.
Line L7 factors one matrix of size $V$ once and solves for the $n$ targets.
The code uses dense matrices, which gives $O(V^3 + n V^2)$ for line L7; with a sparse factorization, as in practice, this is much less.

## Properties

- Personal: the targets follow the actor's examples, not only the generic rig.
- Semantic: each target keeps the meaning of its generic counterpart, so the rig works with the same controls and the same animation data.
- Few examples: the prior fills in what the examples do not show, so a few scans are enough.
- Bounded weights: the weights of the examples stay in $[0, 1]$, as in a blendshape rig.
- Local: the method is an alternating minimization, so it finds a local minimum.

## Variants and improvements

- **Without the prior.** With $\beta = 0$, the targets fit the examples only, and with fewer examples than targets the problem has many solutions. The prior is what makes few examples enough.
- **More examples.** With many examples, the fit term dominates and the targets approach the true targets of the actor.
- **Weighted prior.** Weight the prior per triangle, so that a target may change more in some regions than in others.
- **Online adaptation.** Later work on real-time face tracking adapts the rig to the user during tracking instead of in a separate step.

## When to use it

Use example-based facial rigging when you have a good generic face rig and must make a rig for a new actor or character with the same targets, from a few scans or sculpts.
If the new face is a different character with no examples at all, [deformation transfer](/deformation-transfer/) alone gives a first rig.
If you must edit an existing rig to hit a pose, [blendshape direct manipulation](/blendshape-direct-manipulation/) solves for the weights instead.

## Pitfalls

- **Correspondence.** All meshes must share one triangulation. The scans must be fitted with a template first, and errors in that fit go into the targets.
- **Bad first guesses.** The weights of each example start from a guess, and the method finds a local minimum near it. A guess that names the wrong targets gives wrong targets.
- **The value of $\beta$.** A large $\beta$ keeps the generic targets and ignores the examples; a small one overfits the examples, and with few examples the targets can become strange where no example constrains them. On the toy face of the example, $\beta = 0.01$ gives a larger error on the open target than $\beta = 0.1$, 0.055 against 0.026.
- **Scale ambiguity.** Without the prior, a target scaled by $c$ with its weights divided by $c$ fits the same examples. The prior fixes the scale.
- **Rigid motion.** The examples must be aligned with the neutral face, because a head motion in a scan changes every gradient.

## Implementations

## History

Blendshape rigs for faces were modeled by hand for a long time, often with the [Facial Action Coding System](/facial-action-coding-system/) as a guide for the targets.
Sumner and Popović (2004) gave deformation transfer, which copies the targets of one face onto another, but the copies show how the source face moves, not how the new face moves.
Li, Weise and Pauly (2010) added examples of the actor and optimized the targets in the space of deformation gradients, with the transferred generic rig as the prior.
Later work on real-time face tracking adapted the rig to the user during tracking.

## References
