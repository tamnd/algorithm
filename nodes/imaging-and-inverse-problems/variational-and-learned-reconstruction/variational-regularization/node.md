---
tag: NDREDD
kind: technique
slug: variational-regularization
name: Variational regularization
aliases:
- energy minimization reconstruction
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: core
summary: Reconstruct by minimizing a data fidelity term plus a weighted regularization functional that encodes prior knowledge about the image.
prereqs: [inverse-problem, regularization-method, data-fidelity-term, tikhonov-regularization, convex-function]
see_also: [total-variation-denoising, total-generalized-variation, analysis-and-synthesis-sparsity, bregman-distance-convergence-rates, maximum-a-posteriori-estimation, chambolle-pock-algorithm, morozov-discrepancy-principle, bilevel-learning-of-regularizers]
sources:
  - book: isbn:9780387309316
    title: Otmar Scherzer, Markus Grasmair, Harald Grossauer, Markus Haltmeier and Frank Lenzen, Variational Methods in Imaging, Springer, 2009, Applied Mathematical Sciences 167
    locator: Chapter 3, Variational Regularization Methods for the Solution of Inverse Problems (existence, stability and convergence for convex and nonconvex regularizers)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 5, Tikhonov Regularization (the quadratic case and its convergence theory)
  - paper: doi:10.1088/0266-5611/10/6/003
    title: Robert Acar and Curtis R. Vogel, Analysis of bounded variation penalty methods for ill-posed problems, Inverse Problems 10(6), 1994
    locator: pages 1217 to 1229 (existence, uniqueness and stability for total variation penalties with a forward operator)
  - paper: doi:10.1016/0167-2789(92)90242-F
    title: Leonid I. Rudin, Stanley Osher and Emad Fatemi, Nonlinear total variation based noise removal algorithms, Physica D 60(1-4), 1992
    locator: pages 259 to 268 (the total variation model)
  - paper: doi:10.1017/S0962492918000016
    title: Martin Benning and Martin Burger, Modern regularization methods for inverse problems, Acta Numerica 27, 2018
    locator: pages 1 to 111 (survey of variational and iterative regularization with convex functionals)
  - paper: doi:10.1017/S096249291600009X
    title: Antonin Chambolle and Thomas Pock, An introduction to continuous optimization for imaging, Acta Numerica 25, 2016
    locator: pages 161 to 319 (the models and the first order solvers)
---

Variational regularization reconstructs the unknown $x$ of an [inverse problem](/inverse-problem/) $y = Ax + e$ as a minimizer of an energy $\mathcal{D}(Ax, y) + \lambda R(x)$. The [data fidelity term](/data-fidelity-term/) $\mathcal{D}$ measures the misfit to the data, the regularizer $R$ is small for the images that the model expects, and the weight $\lambda > 0$ sets the balance. [Tikhonov regularization](/tikhonov-regularization/) is the case of two quadratic terms; [total variation](/total-variation-denoising/), $\ell_1$ sparsity and [total generalized variation](/total-generalized-variation/) are the main nonquadratic cases. For convex, lower semicontinuous and coercive $R$ the minimizer exists, depends stably on the data and converges to an $R$-minimizing solution when the noise and $\lambda$ go to 0 at matched speeds, so the technique is a [regularization method](/regularization-method/) in the sense of the area.

## In plain words

A measurement of an image is never perfect, and many different images explain it equally well. Some of these images are full of noise and wild patterns. To pick a good one, write down a score with two parts. The first part says how badly a candidate image explains the measurement. The second part says how strange the candidate looks, for example how many edges it has or how rough it is. Add the two parts, with a weight on the second, and search for the image with the lowest total score. The choice of the second part is where the knowledge about the images goes. The weight decides how much to trust the measurement against that knowledge.

## When it applies

**Setting.** $X$ and $Y$ are Hilbert spaces, $A: X \to Y$ is a bounded linear operator, and the data are $y^\delta$ with $\|y^\delta - y\| \le \delta$ and $y = Ax^\dagger$ (deterministic noise). The discrete setting is $X = \mathbb{R}^n$, $Y = \mathbb{R}^m$ with an $m \times n$ matrix $A$. For Gaussian noise the energy is

$$T_\lambda(x) = \tfrac12\|Ax - y^\delta\|^2 + \lambda R(x),$$

which is the form of the variational pages of this area. Other noise laws change only the first term (see [data fidelity term](/data-fidelity-term/)). The rz pages write $\alpha$ for the same weight.

Use the technique when the problem is ill-posed and the prior knowledge is a statement about structure, not only about size: edges, sparsity in a basis or frame, piecewise smooth regions, nonnegativity. It also applies when no closed form exists, because the energy is minimized by a numerical solver.

**Hypotheses (H).** $R: X \to [0, \infty]$ is convex, lower semicontinuous and proper, and for every $c$ the set $\{x : \|Ax\|^2 + R(x) \le c\}$ is bounded. The last condition is the coercivity condition. It holds for $R(x) = \tfrac12\|x\|^2$ with any $A$, for $R = \|\cdot\|_1$ in $\mathbb{R}^n$, and for total variation on $L^2(\Omega)$ with $\Omega \subset \mathbb{R}^2$ when $A$ does not map constants to 0 (Acar and Vogel 1994).

**Theorem (existence, stability, convergence).** Under (H):

1. For every $y^\delta \in Y$ and $\lambda > 0$, $T_\lambda$ has a minimizer $x_\lambda^\delta$. It is unique if $A$ is injective or $R$ is strictly convex.
2. If $y_k \to y^\delta$ in $Y$, then every sequence of minimizers $x_k$ for the data $y_k$ has a subsequence that converges weakly to a minimizer for $y^\delta$.
3. Let $y \in A(\operatorname{dom} R)$ and choose $\lambda(\delta) \to 0$ with $\delta^2/\lambda(\delta) \to 0$. Then every sequence $x_{\lambda(\delta_k)}^{\delta_k}$ with $\delta_k \to 0$ has a subsequence that converges weakly to an $R$-minimizing solution, that is a minimizer of $R$ over $\{x : Ax = y\}$, and $R(x_{\lambda(\delta_k)}^{\delta_k}) \to R(x^\dagger)$ along it. If the $R$-minimizing solution $x^\dagger$ is unique, the whole family converges weakly to it.

*Proof.* A bounded sequence in a Hilbert space has a weakly convergent subsequence, and a convex lower semicontinuous function is weakly lower semicontinuous; $x \mapsto \tfrac12\|Ax - y\|^2$ is convex and continuous, so it is weakly lower semicontinuous too.

(1) If $T_\lambda(x) \le c$, then $R(x) \le c/\lambda$ and $\|Ax\| \le \|y^\delta\| + \sqrt{2c}$, so the sublevel sets of $T_\lambda$ are bounded by (H). Take a minimizing sequence; a subsequence converges weakly to some $\bar x$, and $T_\lambda(\bar x) \le \liminf T_\lambda(x_k) = \inf T_\lambda$. If $A$ is injective the data term is strictly convex, and a strictly convex function has at most one minimizer.

(2) Let $T_k$ be the energy with data $y_k$. For a fixed $x$ with $R(x) < \infty$, $T_k(x_k) \le T_k(x)$, which is bounded in $k$; so $(x_k)$ is bounded, and a subsequence converges weakly to some $\bar x$. Since $Ax_k - y_k \rightharpoonup A\bar x - y^\delta$, weak lower semicontinuity gives $T_\lambda(\bar x) \le \liminf T_k(x_k) \le \lim T_k(x) = T_\lambda(x)$ for every $x$.

(3) Let $x^\dagger$ be an $R$-minimizing solution; it exists by the argument of (1) applied to $R$ on the closed affine set $\{Ax = y\}$. Write $x_k$ and $\lambda_k$ for the iterates and weights. Comparing with $x^\dagger$, whose residual is at most $\delta_k$,

$$\tfrac12\|Ax_k - y^{\delta_k}\|^2 + \lambda_k R(x_k) \le \tfrac12\delta_k^2 + \lambda_k R(x^\dagger).$$

So $R(x_k) \le R(x^\dagger) + \delta_k^2/(2\lambda_k)$, which is bounded, and $\|Ax_k - y^{\delta_k}\|^2 \le \delta_k^2 + 2\lambda_k R(x^\dagger) \to 0$. By (H) the sequence is bounded; a subsequence converges weakly to some $\bar x$ with $A\bar x = y$, and $R(\bar x) \le \liminf R(x_k) \le \limsup R(x_k) \le R(x^\dagger)$. So $\bar x$ is $R$-minimizing and $R(x_k) \to R(\bar x) = R(x^\dagger)$. If $x^\dagger$ is unique, every subsequence has a further subsequence with the limit $x^\dagger$, so the whole family converges. $\blacksquare$

The theorem gives convergence without a rate. A rate needs a source condition, and for convex $R$ the natural measure of the error is the Bregman distance: under $A^*w \in \partial R(x^\dagger)$ and $\lambda \sim \delta$ the Bregman distance is $O(\delta)$ ([convergence rates in Bregman distance](/bregman-distance-convergence-rates/)). Nonconvex and Banach space versions with the weak topology replaced by a suitable one are in Scherzer et al. (2009), Chapter 3.

## The template

```pseudo id=main
VARIATIONAL(A, y, data about the noise)
L1  choose the data term D from the noise law                 ▷ hole: least squares, Kullback-Leibler, l1
L2  choose the regularizer R from the prior knowledge        ▷ hole: Tikhonov, TV, TGV, l1 of a transform
L3  choose a first λ                                          ▷ hole: the starting weight
L4  repeat
L5      x_λ ← argmin_x D(Ax, y) + λ R(x)                      ▷ hole: the solver
L6      evaluate the parameter rule at λ                      ▷ hole: discrepancy, GCV, L-curve, learned
L7      if the rule is satisfied then return x_λ
L8      update λ                                              ▷ hole: the search over λ
```

The holes are the model (L1, L2), the solver (L5) and the parameter choice (L3, L6, L8). For a quadratic model the solver is a linear system. For a convex nonsmooth model it is a first order method that uses $A$ and $A^*$ and the [proximal operator](/proximal-operator/) of each term: the [proximal gradient method](/proximal-gradient-method/) or [FISTA](/fista/) when $R$ has a cheap proximal operator, and the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/), [split Bregman](/split-bregman-method/) or [ADMM](/admm/) when $R$ acts on a linear transform of $x$. The cost of the solver is counted per iteration, as one product with $A$, one with $A^*$ and the proximal steps, and the iteration count depends on the accuracy, not on the data size alone.

## Classic examples

**Tikhonov.** $R(x) = \tfrac12\|x\|^2$ gives the normal equations $(A^*A + \lambda I)x = A^*y^\delta$, which is the Tikhonov solution of EHN with $\alpha = \lambda$. With $R(x) = \tfrac12\|Lx\|^2$ for a difference operator $L$ it is Phillips' smoothing. The minimizer is linear in the data, and edges are smeared.

**Total variation against a smoothness penalty.** Denoise $f = (0, 0, 3, 3)$ with $A = I$ and $\lambda = 1$, with $D$ the forward difference matrix ($3 \times 4$).

| regularizer $R$ | minimizer | jump at the edge |
|---|---|---|
| $\tfrac12\|Dx\|^2$ | $(3/7, 6/7, 15/7, 18/7) = (0.4286, 0.8571, 2.1429, 2.5714)$ | 1.2857 |
| $\|Dx\|_1$ (total variation) | $(0.5, 0.5, 2.5, 2.5)$ | 2 |

The quadratic penalty solves $(I + D^\top D)x = f$ and spreads the step over all four samples. Total variation keeps the flat parts flat and keeps a sharp edge, but lowers the jump from 3 to 2: each side moves toward the other by $\lambda$ divided by its length 2. This is the contrast loss of total variation, which [Bregman iteration](/bregman-iteration/) removes. Rudin, Osher and Fatemi (1992) introduced the total variation model; [total variation denoising](/total-variation-denoising/) has its theory and solver.

**Sparsity.** $R(x) = \|x\|_1$ with $A = I$ gives soft thresholding: for $y = (3, 0.5, -2)$ and $\lambda = 1$ the minimizer is $(2, 0, -1)$. The quadratic penalty $\tfrac12\|x\|^2$ gives $y/(1 + \lambda) = (1.5, 0.25, -1)$: every entry shrinks and none becomes zero. With a forward operator, $R = \|Wx\|_1$ for a wavelet transform $W$ is the basis of [compressed sensing](/compressed-sensing/) and of compressed sensing MRI; the two ways to put a transform into $R$ are compared on [analysis and synthesis sparsity](/analysis-and-synthesis-sparsity/).

**Poisson data.** For photon counts, $\mathcal{D}(Ax, y) = \sum_i [(Ax + b)_i - y_i\log(Ax + b)_i]$ with total variation and $x \ge 0$ is the standard model in emission tomography and fluorescence microscopy. The energy is convex, but the data term has no Lipschitz gradient near zero, so the solvers use its proximal operator.

**Statistical reading.** With noise $\mathcal{N}(0, \sigma^2 I)$ and a prior density proportional to $\exp(-\beta R(x))$, the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/) minimizes $\tfrac{1}{2\sigma^2}\|Ax - y\|^2 + \beta R(x)$, which is $T_\lambda$ with $\lambda = \sigma^2\beta$. For the Gaussian prior $\mathcal{N}(0, \sigma_{pr}^2 I)$, $\beta R(x) = \|x\|^2/(2\sigma_{pr}^2)$ and $\lambda R(x) = \tfrac{\sigma^2}{2\sigma_{pr}^2}\|x\|^2$, so the weight of EHN Tikhonov is $\alpha = \sigma^2/\sigma_{pr}^2$. The MAP reading is a correspondence of minimizers. It does not make total variation a good model of the prior distribution of images.

## Variations

- **Constrained forms.** Morozov: minimize $R(x)$ subject to $\|Ax - y^\delta\| \le \tau\delta$. Ivanov: minimize $\|Ax - y^\delta\|$ subject to $R(x) \le \rho$. For convex $R$ each is equivalent to the penalized form for some $\lambda$, which the constrained form chooses implicitly. The first is the [discrepancy principle](/morozov-discrepancy-principle/) built into the problem.
- **Nonlinear forward maps.** $\tfrac12\|F(x) - y^\delta\|^2 + \lambda R(x)$ with a nonlinear $F$. Existence and convergence hold when $F$ is weakly sequentially closed; the energy is not convex, so solvers find stationary points (Scherzer et al. 2009, Chapter 3).
- **Several terms.** $\sum_j \lambda_j R_j(x)$, for example total variation plus a nonnegativity constraint, or an infimal convolution of first and second order terms. [Total generalized variation](/total-generalized-variation/) is a balanced form of the latter.
- **Iterative refinement.** [Bregman iteration](/bregman-iteration/) solves the problem again with the residual added back, and replaces the choice of $\lambda$ by a stop index.
- **Learned regularizers.** $R$ is a network or has learned weights, chosen by [bilevel learning](/bilevel-learning-of-regularizers/), or the proximal step of $R$ is replaced by a denoiser in [plug-and-play priors](/plug-and-play-priors/). The theorem above then holds only if the learned $R$ meets its hypotheses.

## Pitfalls

- **Coercivity fails.** If $A$ and $R$ share a direction with no cost, a minimizer need not exist or be unique. For total variation, constants cost nothing, so $A$ must see the mean of $x$; for blind inpainting or a sampling mask that misses a region, the solution in that region is decided by $R$ alone.
- **The weight depends on the scaling.** $\lambda$ has the units of the data term over those of $R$. Doubling the image intensity doubles $\|Dx\|_1$ but quadruples the squared residual, so a weight tuned on one intensity range does not transfer. Values of $\lambda$ in papers are design choices tuned for a data set, not constants of the method.
- **Contrast loss and bias.** Every penalty with $R(0) = 0$ pulls the solution toward its zero set: total variation lowers jumps, $\ell_1$ shrinks large coefficients. Debiasing or Bregman iteration corrects this.
- **Staircasing.** Total variation turns smooth ramps in noisy data into piecewise constant steps. Total generalized variation avoids it.
- **Parameter rules.** The L-curve and GCV are heuristics; only rules that use the noise level give a convergent method in the worst case ([Bakushinskii veto](/bakushinskii-veto/)).
- **Discretization.** The anisotropic discrete total variation $\sum|\partial_1 x| + |\partial_2 x|$ favors edges along the axes. The isotropic form with the Euclidean length per pixel is closer to the continuous model.

## Exercises

1. Show that for $R(x) = \tfrac12\|x\|^2$ the minimizer is $(A^*A + \lambda I)^{-1}A^*y^\delta$, and compute its spectral filter factors.
2. Verify the two rows of the table for $f = (0, 0, 3, 3)$. For the total variation row, check the optimality condition $f - x \in D^\top \partial\|\cdot\|_1(Dx)$ with the dual vector $(0.5, 1, 0.5)$.
3. Show that the convergence part of the theorem fails if $\lambda(\delta) = \delta^2$: construct a diagonal operator with $\sigma_k = 1/k$, $R = \tfrac12\|x\|^2$ and noise along one singular vector such that $\|x_\lambda^\delta - x^\dagger\|$ does not go to 0.
4. Prove that for convex $R$ the constrained problem $\min R(x)$ subject to $\|Ax - y^\delta\| \le \tau\delta$ has a solution that also minimizes $T_\lambda$ for some $\lambda \in (0, \infty]$, if $\tau\delta < \|y^\delta - A\hat x\|$ for every minimizer $\hat x$ of $R$.
5. For $A = I$ in $\mathbb{R}$ and $R(x) = |x|$, write the minimizer of $\tfrac12(x - y)^2 + \lambda|x|$ and of the Kullback-Leibler version $x - y\log x + \lambda x$ for $y > 0$, and compare how each shrinks.

## References
