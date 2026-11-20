---
tag: VE2JDY
kind: technique
slug: bilevel-learning-of-regularizers
name: Bilevel learning of regularizers
aliases:
- bilevel parameter learning
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: "Learn the parameters of a variational regularizer by minimizing the error of its reconstructions on training data, a bilevel optimization problem."
prereqs: [tikhonov-regularization, variational-regularization, gradient-descent]
see_also: [algorithm-unrolling, adjoint-state-method, automatic-differentiation, cross-validation, stein-unbiased-risk-estimate, linear-gaussian-inverse-problem, total-variation-denoising, morozov-discrepancy-principle]
sources:
  - paper: doi:10.1088/0266-5611/19/3/309
    title: "Eldad Haber and Luis Tenorio, Learning regularization functionals, a supervised training approach, Inverse Problems 19(3), 2003"
    locator: pages 611 to 626 (learning the regularization functional from training models by minimizing the reconstruction error)
  - paper: doi:10.1137/120882706
    title: "Karl Kunisch and Thomas Pock, A bilevel optimization approach for parameter learning in variational models, SIAM Journal on Imaging Sciences 6(2), 2013"
    locator: "pages 938 to 983 (the bilevel problem for learning the weights of variational denoising models, and its solution by gradient methods)"
  - paper: doi:10.3934/ipi.2013.7.1183
    title: "Juan Carlos De los Reyes and Carola-Bibiane Schönlieb, Image denoising, learning the noise model via nonsmooth PDE-constrained optimization, Inverse Problems and Imaging 7(4), 2013"
    locator: pages 1183 to 1214 (learning the weights of the data terms for mixed noise by a bilevel problem)
  - paper: doi:10.1017/S0962492919000059
    title: "Simon Arridge, Peter Maass, Ozan Öktem and Carola-Bibiane Schönlieb, Solving inverse problems using data-driven models, Acta Numerica 28, 2019"
    locator: the section on learning the regularizer by bilevel optimization
---

Bilevel learning chooses the parameters $\theta$ of a variational reconstruction method from training pairs $(x_i, y_i)$, with $y_i = Ax_i + e_i$. The lower level is the reconstruction itself, and the upper level scores it against the true images:

$$\min_\theta\ L(\theta) = \frac1N\sum_{i=1}^N\big\|x_\theta(y_i) - x_i\big\|^2, \qquad x_\theta(y) = \arg\min_x\ E(x; \theta, y) = \|Ax - y\|^2 + R_\theta(x).$$

The parameters can be one regularization weight, weights of several penalties, filters inside the regularizer, or weights of the data terms. Haber and Tenorio (2003) set this up for inverse problems, and Kunisch and Pock (2013) and De los Reyes and Schönlieb (2013) developed it for variational image models. The gradient of $L$ comes from the implicit function theorem and one adjoint solve per pair.

## In plain words

A variational method has knobs, such as how strongly to smooth. Normally a person sets them by hand or by a rule that uses only the measured data. Bilevel learning sets them from examples where the true image is known. For each candidate setting, it runs the reconstruction on the examples and measures how far the results are from the true images. Then it changes the setting in the direction that makes this error smaller. The inner reconstruction is an optimization problem, and the outer search is another one, which is why it is called bilevel.

## When it applies

**Setting.** The lower-level energy $E(x; \theta, y)$ is twice differentiable in $x$ and differentiable in $\theta$, and has a unique minimizer $x_\theta(y)$ with an invertible Hessian $H = \nabla_x^2E(x_\theta; \theta, y)$. The training pairs come from the same source as the data to be reconstructed.

**Fact 1 (the gradient, by the implicit function theorem).** The minimizer satisfies $\nabla_xE(x_\theta; \theta, y) = 0$. Differentiating in $\theta$ gives

$$H\,\frac{\partial x_\theta}{\partial\theta} = -\,\partial_\theta\nabla_xE(x_\theta; \theta, y).$$

So for the upper loss $\ell(x) = \|x - x_i\|^2$, solve the adjoint system $Hp = \nabla\ell(x_\theta) = 2(x_\theta - x_i)$, and then

$$\nabla_\theta\ell\big(x_\theta(y_i)\big) = -\big(\partial_\theta\nabla_xE\big)^Tp.$$

This is a theorem under the conditions above. Each pair needs one lower-level solve and one linear solve with $H$, whatever the number of parameters.

**Fact 2 (Tikhonov).** For $E = \|Ax - y\|^2 + \alpha\|x\|^2$, the minimizer solves $(A^TA + \alpha I)x_\alpha = A^Ty$, and Fact 1 gives

$$\frac{dx_\alpha}{d\alpha} = -(A^TA + \alpha I)^{-1}x_\alpha.$$

Both levels are then exact, which makes Tikhonov the test case.

**Fact 3 (what is learned).** In the scalar model $x \sim N(0, \sigma_x^2)$, $y = x + e$ with $e \sim N(0, \sigma^2)$, the expected upper loss of $x_\alpha = y/(1 + \alpha)$ is

$$\mathbb{E}(x_\alpha - x)^2 = \frac{\alpha^2\sigma_x^2 + \sigma^2}{(1 + \alpha)^2},$$

which is smallest at $\alpha = \sigma^2/\sigma_x^2$, with the value $\sigma^2\sigma_x^2/(\sigma_x^2 + \sigma^2)$, the posterior variance. So with many pairs, bilevel learning recovers the weight of the Bayes estimator for a [linear Gaussian problem](/linear-gaussian-inverse-problem/). With few pairs, it fits those pairs.

Use bilevel learning when there are training pairs and the regularizer has few, meaningful parameters, so that the learned method stays a variational method that can be analyzed. If the regularizer is nonsmooth, such as total variation, smooth it first or use a nonsmooth analysis; Kunisch and Pock and De los Reyes and Schönlieb treat such cases.

## The template

```pseudo id=main
BILEVEL-LEARN(pairs (x_i, y_i), LOWER, α_0, η, K)
L1  α ← α_0
L2  for k = 1 to K
L3      g ← 0
L4      for each pair (x_i, y_i), i = 1 to N
L5          x ← LOWER(α, y_i)                         ▷ hole: the lower-level solver, a given function
L6          g ← g + (2/N) ⟨dx/dα, x - x_i⟩            ▷ adjoint solve, Fact 1
L7      α ← max(α - η g, 0)                           ▷ projected gradient step
L8  return α
```

The holes are the lower-level energy and its solver, the parameters, the upper loss and the outer optimizer. The template learns one weight $\alpha \geq 0$ by projected gradient descent; for many parameters, $\alpha$ becomes a vector and the outer optimizer is often a quasi-Newton method. Each outer step costs $N$ lower-level solves and $N$ adjoint solves. If the lower level is solved only approximately, the gradient is approximate too, and the outer method needs a solve accuracy that grows as it converges.

The lower-level solver and the product $\langle dx/d\alpha, v\rangle$ are given functions: the code takes them as arguments and runs lines L1 to L8 around them. The tests build them by hand, for Tikhonov in closed form by Fact 2 or as $y/(1 + \alpha)$ for a scalar problem, and draw the training pairs from fixed seeds; no network is trained. They check the hand example below, that the projection keeps $\alpha$ at 0 when the data asks for less than no smoothing, the adjoint gradient against finite differences, that the learned weight matches a grid search on a seeded problem, and Fact 3 on 2000 seeded pairs.

## Classic examples

**One pair by hand.** Let $A = 1$, $x_1 = 1$ and $y_1 = 1.2$. Then $x_\alpha = 1.2/(1 + \alpha)$ and $L(\alpha) = (x_\alpha - 1)^2$. At $\alpha = 1$: $x_\alpha = 0.6$, $L = 0.16$, $dx/d\alpha = -0.6/2 = -0.3$ by Fact 2, and $dL/d\alpha = 2(-0.4)(-0.3) = 0.24$. The minimizer is $\alpha = 0.2$, where $x_\alpha = 1$ and $L = 0$; projected gradient descent with $\eta = 0.5$ reaches it from $\alpha = 1$. With $y_1 = 0.8$ instead, every $\alpha \geq 0$ shrinks the estimate further from 1, so the learned weight is $\alpha = 0$, with $L = 0.04$.

**Many scalar pairs.** Draw 2000 pairs with $\sigma_x = 1$ and $\sigma = 0.5$ (seed 6). Fact 3 predicts $\alpha = 0.25$ and a loss of 0.2 for infinitely many pairs. The learned weight is 0.2677, which equals the exact minimizer $\sum y_i^2/\sum x_iy_i - 1$ for this sample. The difference from 0.25 is sampling error, a measurement for this seed.

**A seeded matrix problem.** A Gaussian $5 \times 4$ matrix, four training pairs and noise of standard deviation 0.5 (seed 5). Projected gradient descent from $\alpha = 1$ with $\eta = 0.5$ lowers the loss from 0.340 to 0.255 and stops at $\alpha = 0.36527$, which matches a grid search with spacing $10^{-3}$.

**Image models.** Kunisch and Pock learn the weights of filter-based regularizers for denoising, and De los Reyes and Schönlieb learn the weights of the data terms for mixed noise. Their results on test images are measurements.

## Variations

- **Many parameters.** Learn filters and penalty functions inside the regularizer, as in Kunisch and Pock. Fact 1 still needs only one adjoint solve per pair.
- **Unrolled lower level.** Replace the exact minimizer by $K$ steps of a solver and backpropagate through them. This is [algorithm unrolling](/algorithm-unrolling/), and the learned parameters may then depend on $K$.
- **Learning the data term.** Learn the weights of several noise models, as De los Reyes and Schönlieb do.
- **Without true images.** Replace the upper loss by an unbiased estimate of the error, such as the [Stein unbiased risk estimate](/stein-unbiased-risk-estimate/), or by [cross-validation](/cross-validation/) on the data.

## Pitfalls

- **Nonsmooth lower levels.** With total variation or an $\ell_1$ penalty, $x_\theta$ is not differentiable everywhere and Fact 1 does not apply as written. Smooth the penalty, or use a nonsmooth calculus.
- **Inexact lower-level solves.** An inaccurate $x_\theta$ gives an inaccurate gradient. Check the gradient against finite differences on a small case.
- **Nonconvex upper level.** $L(\theta)$ is not convex in general, so the outer method can stop at a local minimizer.
- **Overfitting.** With few pairs and many parameters, the learned method fits the training images. Keep test pairs apart.
- **Positivity.** Weights such as $\alpha$ must stay nonnegative. Project, or learn $\log\alpha$ instead.

## Exercises

1. Derive Fact 1 from the implicit function theorem, and Fact 2 from Fact 1.
2. Verify the hand example, and show that $\alpha = y_1/x_1 - 1$ is the minimizer when $y_1 > x_1 > 0$.
3. Prove Fact 3 and compare the minimum with the posterior variance of $x$ given $y$.
4. For the lower level $\|Ax - y\|^2 + \alpha\|Dx\|^2$ with a matrix $D$, find $dx_\alpha/d\alpha$ and write the adjoint gradient.
5. For a vector of weights $\alpha_j$ on the penalties $\|D_jx\|^2$, show that one adjoint solve per pair gives the gradient in all $\alpha_j$.

## References
