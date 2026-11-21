---
tag: 4RF9RF
kind: algorithm
slug: asd-pocs
name: Adaptive steepest descent POCS
aliases:
- ASD-POCS
area: imaging-and-inverse-problems/tomographic-reconstruction
level: research
summary: Reconstruct sparse-view CT by alternating projections onto the data and positivity constraints with steepest descent steps on total variation.
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", a: "the number of projection angles", d: "the number of detector bins", g: "the number of TV steps per iteration", K: "the number of iterations"}
  time: {per_iteration: "O(a d n + g n^2)", total: "O(K (a d n + g n^2))"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, iterative: true, heuristic: true, convergence_proof: none, linear_in_data: false}
history:
  year: 2008
  people: [Emil Y. Sidky, Xiaochuan Pan]
  note: Sidky and Pan made the step lengths of the earlier TV-POCS method adaptive, to reach a small total variation under a data tolerance in few-view cone-beam CT.
prereqs: [kaczmarz-method, total-variation-denoising, convex-feasibility-problem]
see_also: [sparse-view-ct-reconstruction, sart, sirt, chambolle-pock-algorithm, compressed-sensing, projected-gradient-descent, total-generalized-variation, limited-angle-tomography]
sources:
  - paper: doi:10.1088/0031-9155/53/17/021
    title: Emil Y. Sidky and Xiaochuan Pan, Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization, Physics in Medicine and Biology 53(17), 2008
    locator: the ASD-POCS algorithm, its adaptive step rules and its use in few-view cone-beam CT (general locator)
  - paper: "E. Y. Sidky, C.-M. Kao and X. Pan, Accurate image reconstruction from few-views and limited-angle data in divergent-beam CT, Journal of X-Ray Science and Technology 14(2), 2006, 119 to 139"
    locator: the earlier TV-POCS method with fixed steps (general locator)
  - paper: doi:10.1088/0031-9155/57/10/3065
    title: Emil Y. Sidky, Jakob H. Jorgensen and Xiaochuan Pan, Convex optimization problem prototyping for image reconstruction in computed tomography with the Chambolle-Pock algorithm, Physics in Medicine and Biology 57(10), 2012
    locator: solving the same constrained TV problem with a primal-dual method that has a convergence proof (general locator)
  - paper: doi:10.1109/TIT.2005.862083
    title: Emmanuel J. Candes, Justin Romberg and Terence Tao, Robust uncertainty principles, exact signal reconstruction from highly incomplete frequency information, IEEE Transactions on Information Theory 52(2), 2006
    locator: exact recovery of piecewise constant images from few Fourier samples by TV minimization (general locator)
---

ASD-POCS reconstructs a CT image from few projection angles by looking for an image with a small total variation that fits the data within a tolerance and has no negative values. It alternates two kinds of steps. A data step is one sweep of [ART](/kaczmarz-method/) over all rays followed by clipping at zero, as in the method of projections onto convex sets (POCS). A TV step is a short run of normalized steepest descent steps on the total variation. The name means adaptive steepest descent POCS: the length of the TV steps adapts to the size of the change made by the data steps, so that the TV steps do not undo the data fit. The target is the constrained problem
$$\min_x \operatorname{TV}(x) \quad\text{subject to}\quad \|A x - y\| \le \varepsilon,\ x \ge 0.$$
ASD-POCS is a heuristic. It has no convergence proof, and its result depends on five tuning parameters. Its value is that it works well in practice on piecewise constant objects with few views, where [SART](/sart/), [SIRT](/sirt/) and [filtered back-projection](/filtered-back-projection/) give streaks.

## In plain words

With few projection angles, many images fit the data, and the plain algebraic methods pick one with streaks. Most real objects are made of regions of nearly constant value. Such images have a small total variation: the sum over all pixels of the local jump in value. So among the images that fit the data, pick one with small total variation.

ASD-POCS does this by turns. It pulls the image toward the data with one ART sweep and sets negative values to zero. Then it pushes the image toward smaller total variation with a few steepest descent steps. If the push is stronger than the pull, the image drifts away from the data. So after each round, ASD-POCS compares the two, and if the push was larger, it makes the next push smaller. The ART steps also get smaller over time, so that both settle down together.

## The problem

Given a nonnegative $m \times N$ system matrix $A$ for an $n \times n$ image ($N = n^2$), data $y \in \mathbb{R}^m$ with $m$ often much smaller than $N$, and a tolerance $\varepsilon \ge 0$, find an image $x \ge 0$ with $\|A x - y\| \le \varepsilon$ and a small value of
$$\operatorname{TV}_\eta(x) = \sum_{i,j} \sqrt{(x_{i+1,j} - x_{i,j})^2 + (x_{i,j+1} - x_{i,j})^2 + \eta^2},$$
with forward differences that are 0 at the last row and the last column, and a small $\eta > 0$ that makes the function differentiable. The constrained problem is convex. ASD-POCS does not solve it exactly; it looks for a point that is close to feasible and has a small TV value. See [sparse-view CT reconstruction](/sparse-view-ct-reconstruction/) for the problem and other methods.

## The algorithm

```pseudo id=main
ASD-POCS(A, y, ε, K; β, β_red, g, α, α_red, r_max)
L1  x ← 0; dtvg ← undefined
L2  for k ← 1 to K do
L3      x0 ← x; for each ray i: x ← x + β a_i (y_i - ⟨a_i, x⟩) / ‖a_i‖²     ▷ one ART sweep
L4      x ← max(x, 0); x_res ← x                                        ▷ positivity
L5      dd ← ‖A x - y‖; dp ← ‖x - x0‖; if k = 1 then dtvg ← α dp
L6      x1 ← x; repeat g times: v ← ∇TV(x); x ← x - dtvg v / ‖v‖           ▷ TV steps
L7      dg ← ‖x - x1‖; if dg > r_max dp and dd > ε then dtvg ← α_red dtvg
L8      β ← β_red β
L9  return x_res
```

Line L3 projects the image in turn onto the hyperplane of each ray, relaxed by $\beta$. Line L4 projects onto the nonnegative orthant. Line L5 measures the data misfit $dd$ and the change $dp$ made by the data steps, and the first change fixes the scale of the TV step length. Line L6 takes $g$ steps of length $dtvg$ along the normalized negative TV gradient, so each step moves the image by exactly $dtvg$. Line L7 is the adaptive rule: if the TV steps moved the image more than $r_{\max}$ times as far as the data steps did, and the data are not yet fit, shorten the TV steps. Line L8 shrinks the ART relaxation. The code returns the image after the data steps of the last iteration, whose misfit $dd$ was measured. The defaults of the code are $\beta = 1$, $\beta_{\text{red}} = 0.995$, $g = 20$, $\alpha = 0.2$, $\alpha_{\text{red}} = 0.95$ and $r_{\max} = 0.95$.

## Example

The worked case of the tests: a $16 \times 16$ phantom of three ellipses with the values 0, 0.5, 1 and 1.5 (its TV is 49.3), 6 angles in $[0, \pi)$ with 23 bins each, so 138 rays for 256 pixels, the pixel-driven matrix of the shared helper, exact data, and $\varepsilon = 10^{-3}\|y\| = 0.0077$. All numbers are measurements of this setup. The relative error $\|x - x_{\text{true}}\| / \|x_{\text{true}}\|$ after $k$ iterations:

| method | $k = 50$ | $k = 200$ | $k = 400$ | $k = 1000$ |
|---|---|---|---|---|
| ART with positivity ($g = 0$) | 0.087 | 0.068 | 0.068 | 0.067 |
| ASD-POCS, defaults | 0.185 | 0.071 | 0.045 | 0.039 |
| ASD-POCS, $g = 10$, $\alpha = 0.05$ | 0.124 | 0.050 | 0.037 | |

ART alone converges to an image that fits the data but keeps the error of the null space of $A$. ASD-POCS starts slower, because the early TV steps pull away from the data, and then goes past ART. The TV of the result is 48.3 with the defaults after 1000 iterations, against 51.3 for ART. The final misfit is 0.015 with the defaults, above $\varepsilon$, because the ART relaxation $\beta$ has decayed to $0.995^{1000} \approx 0.007$ and the data steps are weak. The second parameter set reaches a smaller error sooner. Both facts show that the parameters matter.

A small exact case: without TV steps ($g = 0$) and with $\beta_{\text{red}} = 1$, the method is ART with positivity. On the $2 \times 2$ image $(1, 2, 3, 5)$ with the rays of the two rows, the two columns and the two diagonals, the first ART step on row 0 sets $x_0 = x_1 = 3/2$, the step on row 1 sets $x_2 = x_3 = 4$, and 200 sweeps reach the true image to $10^{-9}$.

## Correctness

There is no convergence theorem for ASD-POCS. What can be said:

- **The data steps (theorem).** Without lines L6 and L7, and with $0 < \beta < 2$ fixed, line L3 is the [Kaczmarz method](/kaczmarz-method/) and line L4 a projection onto a convex set. For consistent data with a nonnegative solution, this cyclic projection scheme converges to a point of the intersection of the hyperplanes and the orthant (the theory of [convex feasibility](/convex-feasibility-problem/) by successive projections). The test with $g = 0$ checks this on a small system.
- **The TV steps (theorem).** $\operatorname{TV}_\eta$ is convex and differentiable for $\eta > 0$, and the code computes its exact gradient (a test compares it with finite differences). A short enough step along the negative gradient lowers TV. Line L6 uses a fixed length per step, not a line search, so a single step can raise TV.
- **The combination (heuristic).** The adaptive rule of line L7 keeps the TV steps from growing larger than the data steps while the misfit is above $\varepsilon$. Sidky and Pan argued that near a solution of the constrained problem, the TV gradient and the gradient of the data constraint point in opposite directions, and they used the cosine of their angle as a check. This is a necessary condition for optimality, not a proof that the iterates reach it.

So the output is an image that fits the data roughly and has a smaller TV than the ART image; neither the misfit bound $\varepsilon$ nor TV optimality is guaranteed. Methods with a proof for the same constrained problem exist: the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/) solves it with known convergence, as Sidky, Jorgensen and Pan showed in 2012. The file [proofs/correctness.md](proofs/correctness.md) proves the two theorem parts above.

## Complexity

In the real-RAM model, with $a$ angles of $d$ bins, an $n \times n$ image and a ray-driven matrix with $O(n)$ nonzero entries per ray:

- Line L3 reads each nonzero entry twice per ray, $O(a d n)$ time.
- Lines L4, L5 and L7 take $O(n^2)$ time, plus $O(a d n)$ for the product $A x$ in line L5.
- Line L6 computes $g$ TV gradients, each in $O(n^2)$ time.

So one iteration costs $O(a d n + g n^2)$ time and $O(a d + n^2)$ extra space, and $K$ iterations cost $O(K (a d n + g n^2))$. With few views, $a d$ is small, and the TV steps can dominate. The number of iterations needed is not bounded by any theorem; published uses run hundreds to thousands of iterations.

## Properties

- **Heuristic.** No convergence proof, and no guarantee that the result is feasible or TV-minimal.
- **Five parameters.** $\beta_{\text{red}}$, $g$, $\alpha$, $\alpha_{\text{red}}$ and $r_{\max}$, plus $\varepsilon$. In the example, two parameter sets differ in error by a factor of 1.4 to 1.5 at a fixed iteration count (a measurement).
- **Matrix free.** It needs only the action of single rows of $A$ and the TV gradient, so it works with any projector, including cone-beam projectors that compute rows on the fly.
- **Nonlinear in the data.** The clipping and the normalized TV steps make the output a nonlinear function of $y$, unlike SIRT.
- **Strong prior.** It favors piecewise constant images. Smooth gradients in the object turn into flat regions with steps, the staircase effect of TV.

## Variants and improvements

- **TV-POCS.** The earlier method of Sidky, Kao and Pan (2006) used the same two kinds of steps with fixed step lengths.
- **SART or SIRT data steps.** Line L3 can be any data step: a [SART](/sart/) sweep, a SIRT iteration, or ordered subsets. The method is often run on GPUs with SART.
- **Other priors.** Replace TV with [total generalized variation](/total-generalized-variation/) to reduce the staircase effect, or with a weighted TV that penalizes some directions less.
- **Primal-dual methods.** The [Chambolle-Pock algorithm](/chambolle-pock-algorithm/) and [ADMM](/admm/) solve the same constrained TV problem, or its penalized form, with a convergence proof and fewer parameters.
- **Learned methods.** Unrolled networks such as [learned primal-dual](/learned-primal-dual/) learn the steps from training data.

## When to use it

Use ASD-POCS for sparse-view or [limited-angle](/limited-angle-tomography/) CT of objects that are close to piecewise constant, when a simple code built on an existing ART or SART loop is wanted. Use a primal-dual method when convergence to the solution of the convex problem matters, for example to compare priors or to study the number of views needed. Do not use it for objects with fine texture or smooth gradients, where TV erases detail, and do not use it when many views are available: there [filtered back-projection](/filtered-back-projection/) or [SIRT](/sirt/) are cheaper and the prior adds little.

## Pitfalls

- **Treating it as a solver.** The output is not the solution of the constrained TV problem. Check the misfit and the TV value; do not report them as optimal.
- **The tolerance $\varepsilon$.** With noisy data, $\varepsilon$ must be close to the noise norm. A smaller value overfits noise, and a larger value over-smooths. With exact data, a tiny $\varepsilon$ only means that the rule of line L7 keeps shrinking the TV steps.
- **Decay of $\beta$.** With $\beta_{\text{red}} < 1$, the data steps vanish over time. After many iterations the misfit stops falling, as in the example.
- **No stopping rule from theory.** Nothing tells when the iterates are good enough. Record the misfit $dd$ and the TV value over the iterations, and stop when both have leveled off.
- **The smoothing $\eta$.** With $\eta = 0$ the gradient is not defined at flat regions. Use a small $\eta > 0$, or a subgradient with care.

## Implementations

The Python code takes the sparse rows of $A$ as (column, weight) pairs, for example from the shared helper `imgkit.parallel_beam_matrix`, and an image as a row-major vector. It has the TV function and its exact gradient, the residual norm, and the main loop with the six parameters. The tests check two TV values, the gradient against central differences, the reduction to ART with positivity for $g = 0$ (with the first ART steps by hand), the sparse-view phantom of the example against ART, and positivity with noisy data.

## History

Rudin, Osher and Fatemi introduced total variation as an image prior for denoising in 1992. In 2006, Candes, Romberg and Tao showed that a piecewise constant image can be recovered exactly from few Fourier samples by TV minimization, which started [compressed sensing](/compressed-sensing/) and suggested that CT could use far fewer views. In the same year, Sidky, Kao and Pan proposed TV-POCS for few-view and limited-angle fan-beam and cone-beam CT. In 2008 Sidky and Pan published ASD-POCS, with adaptive step lengths, for circular cone-beam CT. It became a standard reference method for sparse-view CT. In 2012 Sidky, Jorgensen and Pan showed how to solve the same convex problems with the Chambolle-Pock algorithm, which has a convergence proof.

## References
