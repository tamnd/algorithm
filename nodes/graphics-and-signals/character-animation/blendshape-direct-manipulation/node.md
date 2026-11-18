---
tag: RFBXKQ
kind: algorithm
slug: blendshape-direct-manipulation
name: Direct manipulation of blendshapes
aliases:
- blendshape direct manipulation
area: graphics-and-signals/character-animation
level: advanced
summary: Solve for blendshape weights that move dragged vertices to target positions, regularized toward the current weights to keep edits predictable.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {n: "the number of vertices", k: "the number of targets", m: "the number of pinned and dragged vertices"}
  time: {setup: "O(m k^2 + k^3)", drag: "O(m k)", sweep: "O(k^2)"}
  space: {extra: "O(m k + k^2)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
prereqs: [blendshape-model, least-squares-problem]
see_also: [quadratic-programming, kkt-conditions, lagrange-multiplier, projected-gradient-descent, example-based-facial-rigging, facial-action-coding-system, inverse-kinematics, deformation-transfer]
sources:
  - paper: doi:10.1109/MCG.2010.41
    title: "J. P. Lewis and Ken Anjyo, Direct manipulation blendshapes, IEEE Computer Graphics and Applications 30(4), 2010, 42-50"
    locator: "equation 1 (the hard constraint form), equation 2 (the regularized energy with alpha = 0.1), equation 3 (the weight decay mu = 0.001), equation 4 (the solution as w = X m + k) and the bounded quadratic program"
  - paper: doi:10.2312/egst.20141042
    title: "J. P. Lewis, Ken Anjyo, Taehyun Rhee, Mengjie Zhang, Fred Pighin and Zhigang Deng, Practice and theory of blendshape facial models, Eurographics 2014 State of the Art Reports, 199-218"
    locator: the sections on direct manipulation and on solving for weights (general locator)
---

Direct manipulation of blendshapes lets an animator edit a [blendshape](/blendshape-model/) face by dragging points of the mesh instead of moving sliders.
The animator picks a vertex and drags it to a goal, and may pin other vertices so that they stay where they are.
The method finds the weights that bring the picked vertices as close as possible to their goals while they stay close to the current weights.
This is a small regularized [least squares problem](/least-squares-problem/), and it has a closed-form solution, or a box-constrained [quadratic program](/quadratic-programming/) if the weights must stay in $[0, 1]$.
Lewis and Anjyo (2010) gave the method and showed that the regularization term is what makes the edits predictable.

## In plain words

A face rig has many sliders, often dozens or more.
To get a shape, an animator must know which sliders move which part of the face.
Here the animator grabs the face itself, for example the corner of the mouth, and pulls it.
The system then asks: which small change of the sliders moves this point to where the mouse is?
Many slider changes can do it, because the targets overlap.
So the system takes the one that changes the sliders the least from their current values.
That choice keeps the rest of the face calm while the animator drags.
The animator can pin points that must not move, and the system treats them as goals that do not move.

## The problem

The rig is the delta form $v = b_0 + D w$, with the neutral $b_0 \in \mathbb{R}^{3n}$, the delta matrix $D \in \mathbb{R}^{3n \times k}$ and the weights $w \in \mathbb{R}^k$.
The input is the current weights $w_0$, and a set of $m$ picked vertices with goals $p_i$, both pinned and dragged.
Let $S \in \mathbb{R}^{3m \times k}$ be the rows of $D$ at the picked vertices, and let $\mathbf{m} \in \mathbb{R}^{3m}$ be the goals minus the neutral at those vertices, $p_i - b_{0,i}$.
The output is the weights

$$w^\ast = \arg\min_w\; E(w), \qquad E(w) = \lVert S w - \mathbf{m} \rVert^2 + \alpha \lVert w - w_0 \rVert^2 + \mu \lVert w \rVert^2,$$

optionally subject to $0 \le w \le t$ (usually $t = 1$).
The constants $\alpha > 0$ and $\mu \ge 0$ are tuning.
The paper uses $\alpha = 0.1$ and $\mu = 0.001$, for meshes and weights in the units of its own rigs.

## The algorithm

```pseudo id=main
DRAG(D, b₀, goals, w₀, α, μ, bounded)
L1  for each picked vertex i with goal pᵢ: append its 3 rows of D to S, and pᵢ - b₀,ᵢ to m
L2  A ← SᵀS + (α + μ) I
L3  c ← Sᵀm + α w₀
L4  if not bounded: return solve(A, c)               ▷ the free minimizer
L5  w ← clamp(w₀, 0, t)
L6  repeat
L7      for j ← 1 to k: wⱼ ← clamp((cⱼ - Σ_{l≠j} A_jl w_l) / A_jj, 0, t)
L8  until no weight changed by more than tol
L9  return w
```

Lines L2 and L3 come from the gradient $\nabla E = 2(S^T S + (\alpha + \mu) I) w - 2(S^T \mathbf{m} + \alpha w_0)$.
Line L4 solves $A w = c$, which is equation 4 of the paper in the form $w = X \mathbf{m} + \kappa$ with $X = A^{-1} S^T$ and $\kappa = \alpha A^{-1} w_0$.
While the user drags one vertex, the picked set does not change, so $X$ and $\kappa$ are computed once and each mouse move costs one matrix-vector product.
Lines L5 to L8 are projected Gauss-Seidel: each step minimizes $\tfrac12 w^T A w - c^T w$ exactly in one coordinate over the interval $[0, t]$.
The paper solves the bounded problem with a general QP solver; any correct solver gives the same minimizer, because it is unique.

## Example

Take one vertex at $b_0 = (0, 0, 0)$ and two targets with the deltas $d_1 = (1, 0, 0)$ and $d_2 = (1, 1, 0)$ at that vertex.
The current weights are $w_0 = (0, 0)$, $\alpha = 0.1$ and $\mu = 0$.

Drag the vertex to $(1, 0.5, 0)$.
Then $S^T S = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}$, $A = \begin{pmatrix} 1.1 & 1 \\ 1 & 2.1 \end{pmatrix}$ and $c = (1, 1.5)$, with $\det A = 1.31$.

| quantity | value |
|---|---|
| free weights $w^\ast$ | $(0.6, 0.65) / 1.31 = (0.45802, 0.49618)$ |
| vertex $b_0 + D w^\ast$ | $(0.95420, 0.49618, 0)$ |
| weights as $\alpha \to 0$ | $(0.5, 0.5)$, which reaches the goal |

The regularization pulls the weights a little toward $w_0 = 0$, so the vertex stops short of the goal.
This is intended: the user keeps dragging, and the next solve starts from the new $w_0$.

Now drag the vertex to $(2, 1.5, 0)$, so $c = (2, 3.5)$.
The free solution is $(0.7, 1.85) / 1.31 = (0.53435, 1.41221)$, and $w_2$ is above 1.
With the bound $0 \le w \le 1$, $w_2$ sits on its bound and $w_1 = (c_1 - A_{12} \cdot 1) / A_{11} = 1 / 1.1 = 0.90909$.
The gradient of the energy in $w_2$ there is $2 (1 \cdot 0.90909 + 2.1 - 3.5) < 0$, so the energy would decrease if $w_2$ could grow, which the KKT conditions allow at an upper bound.
The vertex goes to $(1.90909, 1, 0)$.
The tests check these values.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md); they hold in exact arithmetic.
- **A unique minimizer.** If $\alpha + \mu > 0$, the Hessian $2A$ is symmetric positive definite, so $E$ is strictly convex and has exactly one minimizer over $\mathbb{R}^k$ and exactly one over the box. This is a proved property.
- **The free solution.** $\nabla E(w) = 0$ if and only if $A w = c$, so line L4 returns the free minimizer.
- **The bounded solution.** A point of the box is the minimizer if and only if it meets the [KKT conditions](/kkt-conditions/): for each $j$, $(A w - c)_j = 0$ if $0 < w_j < t$, $\ge 0$ if $w_j = 0$, and $\le 0$ if $w_j = t$.
- **Projected Gauss-Seidel.** Each step of line L7 does not increase the energy, and lowers it by at least $\tfrac12 A_{jj} \delta^2$ when $w_j$ changes by $\delta$. The iterates converge to the minimizer of the box problem. This is also a proved property.

The tests check the free solution against a numerical gradient and random perturbations, and the bounded solution against a brute force that tries every split of the weights into free, at 0 and at 1.

## Complexity

The cost is in the real RAM model, with $m$ picked vertices and $k$ targets.
Lines L1 to L3 cost $O(m k^2)$, and the solve of line L4 costs $O(k^3)$.
During a drag of one vertex with a fixed picked set, a new goal changes only $\mathbf{m}$, so the new weights cost $O(m k)$ with the precomputed $X$.
One sweep of lines L6 to L8 costs $O(k^2)$.
The number of sweeps depends on the conditioning of $A$ and is not bounded here; on the 15 random problems of the brute force test (4 targets, tolerance $10^{-13}$) it is at most 22, which is a measurement of those tests only.
The extra space is $O(m k + k^2)$.
Building the mesh from the new weights costs $O(n k)$, as for any [blendshape model](/blendshape-model/).

## Properties

- Deterministic, with a unique answer when $\alpha + \mu > 0$.
- Interactive: one small dense solve per edit, independent of the mesh size $n$ except through the final evaluation.
- With $\alpha = \mu = 0$ the problem is underdetermined when $3m < k$, and the plain least squares solution is not unique; the regularization fixes that.
- Pins and drags are the same kind of constraint. A pinned vertex is a goal at its current position.
- The constraints are soft. A goal is met exactly only in the limit $\alpha, \mu \to 0$ and only if it is reachable.

## Variants and improvements

- **Hard constraints.** Equation 1 of the paper keeps $S w = \mathbf{m}$ exactly and minimizes $\lVert w - w_0 \rVert^2$ with a [Lagrange multiplier](/lagrange-multiplier/). The soft form is preferred because a drag can ask for an unreachable point, and then the hard form has no solution.
- **Weight decay.** The term $\mu \lVert w \rVert^2$ pulls weights toward 0 and keeps them from growing over a long edit session.
- **Bounds.** The bounded form is a convex QP with a box. [Projected gradient descent](/projected-gradient-descent/), active set methods and projected Gauss-Seidel all solve it.
- **Sparse weights.** An $\ell_1$ term instead of $\lVert w - w_0 \rVert^2$ prefers edits that move few sliders. That is a variant from later work, not from this paper.
- **Fitting to captured markers.** The same energy with many goals from motion capture markers fits weights to a performance, and the $\alpha$ term then gives temporal smoothness. [Example-based facial rigging](/example-based-facial-rigging/) solves weights in a similar bounded way inside a larger fit.

## When to use it

Use direct manipulation as an editing mode next to the sliders of a face rig.
It works best for fine edits near the current pose, where the linear model and the small regularization give the change the user expects.
For large changes, or for posing from a blank face, sliders or a pose library are often faster, because many weight vectors reach one dragged point.

## Pitfalls

- **Too small an $\alpha$.** The targets overlap, so $S^T S$ is badly conditioned. With a tiny $\alpha$, small mouse moves give large weight changes of opposite sign. Raise $\alpha$, or add the bounds.
- **No bounds.** The free solution can leave $[0, 1]$, as the example shows, and a rig that clamps weights at evaluation time then shows a different face from the one the solver found. Solve with the bounds if the rig has them.
- **The linear term of the QP.** For this energy the QP is $\min \tfrac12 w^T (2A) w + q^T w$ with $q = -2(S^T \mathbf{m} + \alpha w_0)$. Check the sign and the factors when you copy the QP from a paper.
- **Vertices that no target moves.** Their rows in $S$ are zero, so a drag there has no effect. Tell the user, or pick from vertices with nonzero rows only.
- **Units.** $\alpha$ compares squared distances with squared weights, so its useful value depends on the scale of the mesh. A value tuned on one rig does not carry over to another.

## Implementations

## History

Lewis and Anjyo (2010) gave the form of this page: the soft goals, the regularization toward the current weights, an argument for why that term makes edits predictable, and the bounded QP.
Their paper also discusses earlier drag interfaces for faces; this page does not list them, because their details were not checked here.
Lewis and others (2014) place the method among the ways to solve for blendshape weights in their survey.

## References
