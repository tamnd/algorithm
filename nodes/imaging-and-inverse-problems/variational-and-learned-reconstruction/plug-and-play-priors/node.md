---
tag: S92WZQ
kind: technique
slug: plug-and-play-priors
name: Plug-and-play priors
aliases:
- PnP reconstruction
- plug-and-play ADMM
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: "Replace the proximal step of the prior in ADMM or a proximal gradient method by a generic image denoiser, such as a trained network."
prereqs: [admm, proximal-operator, image-denoising]
see_also: [regularization-by-denoising, proximal-gradient-method, haar-wavelet-transform, non-local-means, total-variation-denoising, variational-regularization, diffusion-posterior-sampling, learned-primal-dual]
sources:
  - paper: doi:10.1109/GlobalSIP.2013.6737048
    title: "Singanallur V. Venkatakrishnan, Charles A. Bouman and Brendt Wohlberg, Plug-and-play priors for model based reconstruction, IEEE Global Conference on Signal and Information Processing (GlobalSIP), 2013"
    locator: pages 945 to 948 (the ADMM split and the replacement of the prior step by a denoiser)
  - paper: doi:10.1109/TCI.2016.2599778
    title: "Suhas Sreehari, Singanallur V. Venkatakrishnan, Brendt Wohlberg, Gregery T. Buzzard, Lawrence F. Drummy, Jeffrey P. Simmons and Charles A. Bouman, Plug-and-play priors for bright field electron tomography and sparse interpolation, IEEE Transactions on Computational Imaging 2(4), 2016"
    locator: "pages 408 to 423 (conditions under which a denoiser is a proximal map, and the symmetrized non-local means denoiser)"
  - paper: doi:10.1109/TCI.2016.2629286
    title: "Stanley H. Chan, Xiran Wang and Omar A. Elgendy, Plug-and-play ADMM for image restoration, fixed-point convergence and applications, IEEE Transactions on Computational Imaging 3(1), 2017"
    locator: pages 84 to 98 (bounded denoisers and fixed point convergence with a growing penalty)
  - url: https://proceedings.mlr.press/v97/ryu19a.html
    title: "Ernest K. Ryu, Jialin Liu, Sicheng Wang, Xiaohan Chen, Zhangyang Wang and Wotao Yin, Plug-and-play methods provably converge with properly trained denoisers, Proceedings of the 36th International Conference on Machine Learning, PMLR 97, 2019"
    locator: "pages 5546 to 5557 (Assumption A on the residual of the denoiser, Theorem 1 for PnP-FBS, Theorem 2 and Corollary 3 for PnP-DRS and PnP-ADMM)"
  - paper: doi:10.1561/2200000016
    title: "Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato and Jonathan Eckstein, Distributed optimization and statistical learning via the alternating direction method of multipliers, Foundations and Trends in Machine Learning 3(1), 2011"
    locator: Section 3 (the scaled form of ADMM and its convergence)
---

Plug-and-play (PnP) priors reconstruct the unknown $x$ of an inverse problem $y = Ax + e$ with a splitting method, such as [ADMM](/admm/) or the [proximal gradient method](/proximal-gradient-method/), in which the [proximal step](/proximal-operator/) of the regularizer is replaced by a call to an image denoiser. Venkatakrishnan, Bouman and Wohlberg (2013) noticed that this step has the form of a denoising problem, so any good denoiser, such as BM3D, [non-local means](/non-local-means/) or a trained network, can stand in for it. The data term keeps the physics, and the denoiser supplies the prior. If the denoiser is the proximal map of a convex function, PnP is the original method and converges. For other denoisers there is in general no objective that PnP minimizes; convergence holds only under extra conditions on the denoiser.

## In plain words

Many reconstruction methods take turns between two jobs. One job makes the image agree with the measured data. The other job cleans the image, so that it looks like a real image and not like noise. In the classical methods, the cleaning job comes from a formula for what a good image is.

Plug-and-play keeps the turn taking but hands the cleaning job to an existing noise remover. This can be a very good one, for example a network trained to remove noise from photos. You do not need to write down what a good image is; the noise remover already knows it in its own way. The cost is that you lose the guarantee that the method solves a clear problem, unless the noise remover has special properties.

## When it applies

**Setting.** $x \in \mathbb{R}^n$, $A \in \mathbb{R}^{m \times n}$, and the objective $f(x) + \lambda R(x)$ with $f(x) = \tfrac12\|Ax - y\|^2$. Split $x = v$. ADMM in scaled form with penalty $\rho > 0$ is

$$x \leftarrow \operatorname{prox}_{f/\rho}(v - u),\qquad v \leftarrow \operatorname{prox}_{(\lambda/\rho)R}(x + u),\qquad u \leftarrow u + x - v,$$

where $\operatorname{prox}_{g}(z) = \arg\min_v g(v) + \tfrac12\|v - z\|^2$. The $v$ step is a denoising problem: find $v$ close to the noisy image $x + u$ with a small $R(v)$, at the noise variance $\lambda/\rho$. PnP replaces it by $v \leftarrow D(x + u)$ for a given denoiser $D$.

Use the technique when the forward model is known and its proximal step (a linear solve for least squares) is cheap, when a good denoiser for the image class exists, and when no explicit prior is convenient. The theory below says when the result is the minimizer of an objective.

**Fact 1 (a proximal denoiser gives ADMM).** If $D = \operatorname{prox}_{\theta R}$ for a proper closed convex $R$, then PnP-ADMM with penalty $\rho$ is ADMM for $f(x) + \rho\theta R(x)$. So, when this problem has a minimizer, the iterates converge to one (Boyd et al. 2011, Section 3). The weight of the prior is $\rho\theta$: with a fixed denoiser, $\rho$ acts as the regularization parameter. This is a theorem; it is the definition of the step. Soft thresholding in an orthonormal basis $H$, $D(z) = H^T\operatorname{soft}(Hz, \theta)$, is the proximal map of $\theta\|Hx\|_1$.

**Fact 2 (when a denoiser is a proximal map).** Let $D : \mathbb{R}^n \to \mathbb{R}^n$ be continuously differentiable, with a Jacobian that is symmetric and has its eigenvalues in $[0, 1]$ at every point. Then $D$ is the proximal map of some proper closed convex function, so Fact 1 applies (Sreehari et al. 2016, from a theorem of Moreau). For a linear denoiser $D(z) = Wz$, this means $W$ is symmetric with eigenvalues in $[0, 1]$. If they lie in $(0, 1]$, then $W = \operatorname{prox}_g$ for $g(x) = \tfrac12x^T(W^{-1} - I)x$, and PnP-ADMM solves $(A^TA + \rho(W^{-1} - I))x = A^Ty$. Most practical denoisers, such as BM3D, non-local means with its usual normalization, and trained networks, do not have a symmetric Jacobian. Sreehari et al. built a symmetric form of non-local means to meet the condition.

**Fact 3 (contractive residual).** Ryu et al. (2019) assume that the residual $D - I$ is $\varepsilon$-Lipschitz: $\|(D - I)(x) - (D - I)(x')\| \le \varepsilon\|x - x'\|$. If $f$ is $\mu$-strongly convex and $\varepsilon < 1$, PnP-ADMM with the step $\alpha = 1/\rho$ of the $f$ step converges to a unique fixed point when $\varepsilon/((1 + \varepsilon - 2\varepsilon^2)\mu) < \alpha$ (their Corollary 3); the forward-backward form converges when $\max\{|1 - \alpha\mu|, |1 - \alpha L|\}(1 + \varepsilon) < 1$ for an $L$-smooth $f$ (their Theorem 1). Strong convexity of $f$ needs $A$ to have full column rank, which fails for most inverse problems. The fixed point need not minimize any objective. Ryu et al. train networks with a spectral norm control to meet the assumption; whether a trained network meets it is a measurement.

**Fact 4 (bounded denoisers).** Chan, Wang and Elgendy (2017) prove fixed point convergence for bounded denoisers, whose change $\|D(z) - z\|$ is controlled by the noise level, when $\rho$ grows by a fixed rule during the iterations. The growing $\rho$ forces the steps to shrink, so the limit depends on the schedule.

## The template

```pseudo id=main
PNP-ADMM(prox_f, D, v_0, K)
L1  v ← v_0,  u ← 0
L2  for k = 1 to K
L3      x ← prox_{f/ρ}(v - u)            ▷ data step: (A^T A + ρI) x = A^T y + ρ(v - u)
L4      v ← D(x + u)                     ▷ hole: the denoiser, a given function
L5      u ← u + x - v                    ▷ dual update
L6  return x, v, u
```

The holes are the denoiser (L4), the penalty $\rho$ and the number of steps. Line L3 calls $A$ and $A^T$; for least squares it is a linear solve, done once by a factorization for a small dense $A$ or by conjugate gradients for a large one. Each step calls the denoiser once, so the cost is $K$ times one data step plus one denoiser call. Other splittings give other PnP methods: the forward-backward form $x \leftarrow D(x - \gamma A^T(Ax - y))$ (PnP-ISTA or PnP-FBS), half-quadratic splitting, and primal-dual forms.

The denoiser is a given function: the code takes $D$ and the data step as arguments and runs lines L1 to L6 around them. The tests build $D$ by hand, as soft thresholding in the orthonormal Haar basis or as a fixed symmetric matrix, so that the answer is known; no network is trained. They check that the Haar denoiser satisfies the optimality condition of its proximal problem, the hand example below, that PnP with the Haar denoiser reaches the lasso minimizer found by an independent ISTA solver to $10^{-7}$ on a seeded deblurring problem, and Fact 2 for a symmetric linear denoiser.

## Classic examples

**A proximal denoiser, by hand.** Take $A = I$ (pure denoising), $y = (3, 1)$, $\rho = 1$ and the Haar denoiser in $\mathbb{R}^2$, $D(z) = H^T\operatorname{soft}(Hz, 1)$ with $H = \tfrac{1}{\sqrt2}\begin{pmatrix}1 & 1\\ 1 & -1\end{pmatrix}$. By Fact 1, PnP minimizes $\tfrac12\|x - y\|^2 + \|Hx\|_1$, whose solution is $H^T\operatorname{soft}(Hy, 1)$. Here $Hy = (2\sqrt2, \sqrt2)$, the soft threshold gives $(2\sqrt2 - 1, \sqrt2 - 1)$, and so $x^\star = (3 - \sqrt2, 1) = (1.585786, 1)$. From $v = u = 0$, line L3 is $x = (y + v - u)/2$:

| step $k$ | $x$ | $v$ | $u$ |
|---|---|---|---|
| 1 | (1.5, 0.5) | (0.292893, 0.292893) | (1.207107, 0.207107) |
| 2 | (1.042893, 0.542893) | (0.835786, 0.75) | (1.414214, 0) |
| 3 | (1.210786, 0.875) | (1.210786, 0.875) | (1.414214, 0) |
| 4 | (1.398286, 0.9375) | (1.398286, 0.9375) | (1.414214, 0) |
| 10 | (1.582857, 0.999023) | (1.582857, 0.999023) | (1.414214, 0) |

From step 2 on, $u$ is fixed at $(\sqrt2, 0)$, which is $H^T$ times the subgradient $(1, 1)$ of $\|Hx\|_1$ at the solution, and the error halves at each step.

**A symmetric smoother.** A linear smoother $W$ that is symmetric with eigenvalues in $(0, 1]$ gives the quadratic regularizer $\tfrac{\rho}{2}x^T(W^{-1} - I)x$ (Fact 2). A periodic blur with a sampled Gaussian kernel that sums to 1 is such a $W$, since it is symmetric and its eigenvalues, the DFT of the kernel, lie in $(0, 1]$; a non-local means matrix with rows normalized to sum to 1 is not symmetric.

**Strong denoisers.** With BM3D or a trained network such as DnCNN as $D$, PnP gives high quality results in deblurring, super-resolution, tomography and MRI. These results are measurements on test images, and the methods have no convergence guarantee unless the denoiser meets Fact 3 or Fact 4. In practice the number of steps and $\rho$ are tuned, often with a fixed small $K$.

## Variations

- **PnP-ISTA and PnP-FISTA.** Replace the proximal step of [ISTA](/iterative-shrinkage-thresholding/) or [FISTA](/fista/) by $D$. Only $A$ and $A^T$ are needed, with no linear solve.
- **Half-quadratic splitting.** Alternate the data step and the denoiser with a growing penalty and no dual variable; Zhang et al. (2017) used this with a set of trained CNN denoisers at decreasing noise levels.
- **Consensus equilibrium.** Buzzard et al. (2018) describe the PnP fixed point as a balance of forces between the data step and the denoiser, without an objective.
- **Regularization by denoising.** [RED](/regularization-by-denoising/) builds an explicit regularizer from $D$ and uses the residual $x - D(x)$ as a gradient.
- **Learned splitting.** Unroll a fixed number of PnP steps and train the denoiser end to end; this is [algorithm unrolling](/algorithm-unrolling/), as in [learned primal-dual](/learned-primal-dual/).
- **Score-based priors.** A denoiser at many noise levels is a score model, and [diffusion posterior sampling](/diffusion-posterior-sampling/) samples instead of iterating to a fixed point.

## Pitfalls

- **No objective.** Without Fact 1 or Fact 2, the limit is a fixed point, not a minimizer. Its quality cannot be checked by an objective value, and different splittings ($\rho$, ADMM or ISTA) give different fixed points.
- **The noise level of the denoiser.** The $v$ step denoises at noise variance $\lambda/\rho$. A denoiser trained for one noise level must match it, and changing $\rho$ changes the effective weight of the prior.
- **Divergence.** With an expansive denoiser, PnP can oscillate or diverge. Stop on a fixed number of steps or check $\|x - v\|$, and do not read a stable image as a converged one.
- **Strong convexity is rare.** The contraction results need a strongly convex data term, so they do not apply to underdetermined problems such as compressed sensing MRI without changes.
- **Hidden bias.** A denoiser trained on one image class pushes every reconstruction toward that class.

## Exercises

1. Show that $D(z) = H^T\operatorname{soft}(Hz, \theta)$ is the proximal map of $\theta\|Hx\|_1$ when $H$ is orthonormal. Why does this fail for a frame that is not orthonormal?
2. Verify the first two rows of the table. Then prove that from step 2 on the error $x_k - x^\star$ halves at each step.
3. Let $W$ be symmetric with eigenvalues in $(0, 1]$. Show that $\operatorname{prox}_g = W$ for $g(x) = \tfrac12x^T(W^{-1} - I)x$, and derive the linear system that PnP-ADMM solves.
4. Take $W = \begin{pmatrix}0 & 1\\ 0 & 1\end{pmatrix}$, which copies the second entry into the first. Is it the proximal map of a convex function? Run PnP-ADMM with $A = I$ and $y = (1, 0)$ for $\rho = 1$ and $\rho = 2$, and compare the fixed points.
5. For $f(x) = \tfrac12\|x - y\|^2$ ($\mu = L = 1$) and a denoiser with $\varepsilon = 0.2$, find the range of $\alpha$ for which the forward-backward bound of Ryu et al. gives a contraction.

## References
