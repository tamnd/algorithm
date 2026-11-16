---
tag: ZVVMQX
kind: algorithm
slug: inverse-compositional-alignment
name: Inverse compositional image alignment
aliases:
- Baker-Matthews alignment
- inverse compositional Lucas-Kanade
area: computer-vision/visual-tracking
level: advanced
summary: Align a template to an image by Gauss-Newton steps that warp the template, so the Hessian is computed once, and compose the inverse of each step into the warp.
solves: [image-registration]
model: real-ram
complexity:
  vars: {m: the number of template pixels, n: "the number of warp parameters (6 for an affine warp)", N: the number of iterations}
  time: {worst: Θ(n^2 m + N (n m + n^3)), average: Θ(n^2 m + N (n m + n^3)), best: Θ(n^2 m + n^3)}
  space: {extra: Θ(n m + n^2)}
properties: {deterministic: true, exact: false, local: true, iterative: true}
history:
  year: 2001
  people: [Simon Baker, Iain Matthews]
  note: Baker and Matthews presented the inverse compositional algorithm in 2001 and placed it with the additive and compositional forms in one framework in 2004.
prereqs: [lucas-kanade-method, gauss-newton-algorithm]
see_also: [kanade-lucas-tomasi-tracker, direct-image-alignment, image-warping, homography, nonlinear-least-squares, levenberg-marquardt, photometric-error, template-matching]
sources:
  - paper: doi:10.1023/B:VISI.0000011205.11775.fd
    title: Simon Baker and Iain Matthews, Lucas-Kanade 20 years on, a unifying framework, International Journal of Computer Vision 56(3), 2004, 221 to 255
    locator: Section 2 (the forwards additive algorithm and its cost), Section 3.1 (the forwards compositional algorithm and the group requirement) and Section 3.2 (the inverse compositional algorithm, its first-order equivalence with the forwards compositional one, and its cost)
  - paper: "Simon Baker and Iain Matthews, Equivalence and efficiency of image alignment algorithms, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2001"
    locator: the whole paper (the first statement of the inverse compositional algorithm and of its equivalence to the forwards additive algorithm)
  - paper: "Bruce D. Lucas and Takeo Kanade, An iterative image registration technique with an application to stereo vision, Proceedings of the 7th International Joint Conference on Artificial Intelligence (IJCAI), Vancouver, 1981, volume 2, pages 674 to 679"
    locator: the whole paper (the forwards additive iteration that this algorithm reorganizes)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 9, Motion estimation (the sections on incremental refinement and parametric motion)
---

Inverse compositional alignment finds the parameters $p$ of a warp $W(x; p)$ that make the image $I$, warped back, match a template $T$: it minimizes $\sum_x (I(W(x; p)) - T(x))^2$ over the template pixels, as the [Lucas-Kanade method](/lucas-kanade-method/) does. The difference is the roles of the two images in each [Gauss-Newton](/gauss-newton-algorithm/) step. The step finds a small warp of the template, $\Delta p$, so that $T(W(x; \Delta p))$ matches the current $I(W(x; p))$, and then composes the inverse of that small warp into $p$. Because the linearization is always at the template and at $\Delta p = 0$, the steepest descent images and the $n \times n$ Hessian do not change between iterations: they are computed once, and each iteration costs only one warp of the image and $\Theta(n m)$ more operations. Baker and Matthews showed that, to first order, the step gives the same update as the classic additive and compositional steps. The method needs warps that form a group, such as translations, affine maps and [homographies](/homography/).

## In plain words

You have a small picture, the template, and a large picture that contains a moved and distorted copy of it. You want the stretch and shift that lines them up. The usual way makes a guess, warps the large picture by the guess, compares it with the template, and computes a correction from the slopes of the large picture at the warped places. Those slopes change at every guess, so the costly part of the work is redone. The inverse compositional way asks the opposite question: how should the template move to look like the warped picture? The slopes of the template never change, so the hard part is done once, before the loop. The answer is then undone on the guess: if the template should move a little to the right, the guess moves a little to the left. Near the answer, both ways make the same step.

## The problem

The input is a template $T$ given on a set $\Omega$ of $m$ pixels, an image $I$, a warp family $W(x; p)$ with $n$ parameters, a start $p_0$, an iteration limit $k$ and a tolerance $\tau$. Points use the convention of the vision pages: pixel $(u, v)$ is $I[v][u]$, with its center at the point $(u, v)$. Off-grid values come from [bilinear interpolation](/bilinear-interpolation/). The output is the $p$ that minimizes

$$
E(p) = \sum_{x \in \Omega} \big( I(W(x; p)) - T(x) \big)^2 ,
$$

a [nonlinear least-squares](/nonlinear-least-squares/) problem. The warps must form a group: $W(x; 0) = x$, the composition of two warps of the family is a warp of the family, and each warp has an inverse in the family. The code on this page uses the affine warp in the parameterization of Baker and Matthews,

$$
W(x; p) = \begin{pmatrix} (1 + p_1) u + p_3 v + p_5 \\ p_2 u + (1 + p_4) v + p_6 \end{pmatrix}, \qquad A(p) = \begin{pmatrix} 1 + p_1 & p_3 & p_5 \\ p_2 & 1 + p_4 & p_6 \\ 0 & 0 & 1 \end{pmatrix},
$$

where $A(p)$ is the same warp in [homogeneous coordinates](/homogeneous-coordinates/). Composition of warps is the product of the matrices.

## The algorithm

```pseudo id=main
IC-ALIGN(T, Ω, I, p, k, τ)
L1   for each x in Ω do compute ∇T(x)                       ▷ central differences of T
L2   for each x in Ω do compute ∂W/∂p at (x; 0)              ▷ a 2 × n matrix
L3   for each x in Ω do S(x) ← ∇T(x)ᵀ ∂W/∂p(x; 0)           ▷ steepest descent image, 1 × n
L4   H ← Σ_{x ∈ Ω} S(x)ᵀ S(x)                                ▷ n × n, fixed from now on
L5   repeat up to k times
L6       for each x in Ω do e(x) ← I(W(x; p)) - T(x)
L7       g ← Σ_{x ∈ Ω} S(x)ᵀ e(x)
L8       Δp ← H⁻¹ g
L9       W(·; p) ← W(·; p) ∘ W(·; Δp)⁻¹                     ▷ A(p) ← A(p) A(Δp)⁻¹
L10      if |Δp| < τ then return p
L11  return p
```

Lines L1 to L4 are the precomputation. Lines L6 to L10 are the loop, and only line L6 reads the image. For the affine warp, $\partial W / \partial p$ at $x = (u, v)$ is

$$
\frac{\partial W}{\partial p} = \begin{pmatrix} u & 0 & v & 0 & 1 & 0 \\ 0 & u & 0 & v & 0 & 1 \end{pmatrix},
$$

so $S(x) = (T_u u,\ T_v u,\ T_u v,\ T_v v,\ T_u,\ T_v)$, with $(T_u, T_v) = \nabla T(x)$. Line L8 solves a $6 \times 6$ system. For a translation, $W(x; p) = x + p$, line L9 is $p \leftarrow p - \Delta p$, and the algorithm is the tracking step of the [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/).

**The forwards additive algorithm, for comparison.** Lucas and Kanade linearize $I(W(x; p + \Delta p))$ at the current $p$. Each step needs $\nabla I$ at the warped points $W(x; p)$, new steepest descent images and a new Hessian, then sets $p \leftarrow p + \Delta p$. That is $\Theta(n^2 m)$ per iteration instead of $\Theta(n m)$.

## Example

**One dimension by hand.** Let $T(x) = x^2$ on the pixels $x = 1, 2, 3$, and let the image be $I(y) = (y - 0.5)^2$, so the true warp is the translation $p^* = 0.5$: $I(x + 0.5) = T(x)$. The central differences of $T$ are $(4 - 0)/2 = 2$, $(9 - 1)/2 = 4$ and $(16 - 4)/2 = 6$, so $S = (2, 4, 6)$ and $H = 4 + 16 + 36 = 56$, once. From $p = 0$:

| Step | $e(1), e(2), e(3)$ | $g$ | $\Delta p$ | new $p = p - \Delta p$ | $p^* - p$ |
|---|---|---|---|---|---|
| 1 | $-0.75, -1.75, -2.75$ | $-25$ | $-25/56$ | $0.446429$ | $0.0536$ |
| 2 | $-0.1043, -0.2114, -0.3186$ | $-2.9656$ | $-0.052956$ | $0.499385$ | $6.1 \cdot 10^{-4}$ |
| 3 | $-0.00123, -0.00246, -0.00369$ | $-0.034434$ | $-0.000615$ | $0.49999992$ | $8.1 \cdot 10^{-8}$ |
| 4 | | | | $0.5$ to 15 digits | $1.4 \cdot 10^{-15}$ |

The error is squared at each step, up to a factor of about 0.21: the residual at the answer is zero, and the central difference of a quadratic is its exact derivative.

**An affine warp.** The template is a $40 \times 40$ texture of 12 Gaussian blobs (seeded, widths 2.5 to 4.5 pixels), and $\Omega$ is the $21 \times 21$ block $10 \le u, v \le 30$, so $m = 441$ and $n = 6$. The image is the texture warped so that $I(W(x; p^*)) = T(x)$ with $p^* = (0.05, -0.03, 0.02, -0.04, 1.5, -1)$. From $p = 0$, the cost goes 643132, 101084, 1623.6, 122.7, 120.06 and then stays at 120.11 after 9 steps. The result $p = (0.0501, -0.0294, 0.0219, -0.0397, 1.4492, -1.0169)$ moves every point of $\Omega$ to within 0.031 pixel of its true place. The cost cannot reach zero, because the image is sampled and the template gradient is a central difference, so the last steps move the cost by about 0.05 in either direction. The forwards additive algorithm on the same data ends within 0.0004 pixel of the inverse compositional result, with a new Hessian at every step.

**A whole-pixel shift.** With $I(u, v) = T(u - 3, v + 2)$, every sample $I(W(x; p^*))$ falls on a pixel, so the cost at $p^* = (0, 0, 0, 0, 3, -2)$ is exactly zero. The cost goes from $4.75 \cdot 10^5$ to $3.5 \cdot 10^{-17}$ in 10 steps, and all six parameters are within $10^{-8}$ of $p^*$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts.

- **The step solves the linearized problem.** Line L8 minimizes $\sum_x (T(x) + S(x) \Delta p - I(W(x; p)))^2$, the first-order form of $\sum_x (T(W(x; \Delta p)) - I(W(x; p)))^2$. If the steepest descent images are linearly independent as functions on $\Omega$, $H$ is positive definite and the step is unique.
- **The update stays in the family.** Line L9 is the matrix product $A(p) A(\Delta p)^{-1}$, which is affine with last row $(0, 0, 1)$; so the update is exact and the result has a parameter vector.
- **An exact alignment is a fixed point.** If $I(W(x; p^*)) = T(x)$ for all $x \in \Omega$, then $e = 0$, $\Delta p = 0$ and $p^*$ does not change.
- **Local convergence.** If $T$ is continuously differentiable and $I(W(y; p^*)) = T(y)$ on an open set around the template, then the warp error after one step is $o$ of the error before it, so from every start close enough to $p^*$ the iteration converges to $p^*$, faster than any fixed linear rate. The proof writes the current warp as $W(\cdot; p^*) \circ W(\cdot; \delta)$ and shows that the step $\Delta p$ equals $\delta$ to first order.

Baker and Matthews prove, also to first order, that the inverse compositional and forwards compositional updates are the same warp, and that both agree with the forwards additive update. This equivalence is a first-order statement. It does not say that the iterations follow the same path, and it gives no global convergence: a start far from $p^*$ can converge to another local minimum.

## Complexity

- **Precomputation.** Lines L1 to L3 cost $\Theta(n m)$. Line L4 forms $\Theta(n^2)$ sums of $m$ terms, $\Theta(n^2 m)$.
- **One iteration.** Line L6 is $m$ warps and bilinear samples, $\Theta(n m)$ for a warp with $n$ parameters. Line L7 is $\Theta(n m)$, line L8 is $\Theta(n^3)$ by elimination (or $\Theta(n^2)$ with a factorization of $H$ stored once), and line L9 is $O(1)$ for a $3 \times 3$ matrix.
- **Total.** $\Theta(n^2 m + N(n m + n^3))$ for $N$ iterations, in the [real RAM](/real-ram/). The forwards additive algorithm costs $\Theta(N(n^2 m + n^3))$. With $n = 6$ and $m = 441$, the per-iteration sums drop from about $36 \cdot 441$ products to about $6 \cdot 441$.
- **Space.** $\Theta(n m)$ for the steepest descent images and $\Theta(n^2)$ for $H$.

## Properties

- **Fixed Hessian.** The Gauss-Newton matrix is evaluated once, at the template. This is the source of the speed, and it also means the step uses the template gradient, not the image gradient at the current warp.
- **Same first-order step.** Near the solution, the update matches the forwards additive and forwards compositional updates.
- **Group warps only.** The algorithm needs the inverse of $W(\cdot; \Delta p)$ and a composition that stays in the family.
- **No step control.** The plain algorithm accepts every step. Near the noise floor the cost can rise slightly, as in the affine example; far from the solution it can diverge.
- **Deterministic and local.** The result depends only on the start and the pixels near the warped template.

## Variants and improvements

- **Other warp groups.** Translations, similarities, affine maps and homographies (8 parameters, with $A(p)$ a general $3 \times 3$ matrix) all form groups.
- **Robust and weighted errors.** Reweight $e(x)$ to reduce the effect of outliers. A weight that changes per iteration makes $H$ change too, so the saving is partly lost unless the weights are approximated by fixed ones.
- **Linear appearance change.** Add a linear model of brightness change (for example, gain and bias, or a few basis images). Projecting the error out of the appearance subspace keeps a fixed Hessian.
- **Levenberg-Marquardt.** Add a damping term to $H$ and test the cost before accepting a step, as in [Levenberg-Marquardt](/levenberg-marquardt/).
- **Coarse to fine.** Run the algorithm on an [image pyramid](/image-pyramid/) to widen the range of convergence.
- **Direct visual odometry.** The same structure, a fixed Jacobian at a reference frame and composed updates of a camera pose, appears in [direct image alignment](/direct-image-alignment/) with a [photometric error](/photometric-error/).

## When to use it

Use it to align or track a fixed template (a planar patch, a face model, a reference image) through many images or frames, where the template does not change but the image does. The precomputation is paid once and each frame costs only a few image warps. Use the forwards additive form when the template changes at every frame, when the warp family is not a group, or when each step needs a different weight per pixel.

## Pitfalls

- **Additive update of a compositional step.** Adding $-\Delta p$ to $p$ is right for a translation only. For an affine warp, the update must be the matrix product of line L9; the additive form gives a wrong warp off the identity.
- **Order of composition.** The update is $W(\cdot; p) \circ W(\cdot; \Delta p)^{-1}$, applied first to the template coordinates. Composing in the other order gives the right answer only for commuting warps such as translations.
- **Template gradient on the border.** Central differences need one pixel around $\Omega$. Take the gradient from the full template image, or shrink $\Omega$.
- **Region coordinates.** The parameters $p_1$ to $p_4$ multiply the coordinates, so a template far from the origin couples the linear part with the translation and conditions $H$ badly. Put the origin of the template coordinates at its center, or scale them.
- **Large motion.** The start must be inside the range of the linearization, about the size of the smallest structures in the template; use a pyramid or a coarse search first.
- **Noise and the floor.** With noise or sampling error, the cost has a floor, and a test on the change of the cost may never stop the loop. Test the size of $\Delta p$, with a limit on the number of iterations.

## Implementations

## History

Lucas and Kanade (1981) introduced the forwards additive iteration for image registration. Baker and Matthews presented the inverse compositional algorithm at CVPR 2001 and, in their 2004 paper, put it with the forwards additive, forwards compositional and inverse additive forms in one framework, with proofs of their first-order equivalence, their costs per iteration and an experimental comparison. They noted that the inverse compositional form is the efficient one that works for any warp group.

## References
