---
tag: K86DXS
kind: technique
slug: regularization-by-denoising
name: Regularization by denoising
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: Define the regularizer (1/2) x^T (x - D(x)) from an image denoiser D; its gradient is x - D(x) only if D is locally homogeneous with a symmetric Jacobian.
prereqs: [plug-and-play-priors, image-denoising, gradient-descent]
see_also: [variational-regularization, fixed-point-iteration, admm, non-local-means, total-variation-denoising, image-deblurring, deep-image-prior, diffusion-posterior-sampling]
sources:
  - paper: doi:10.1137/16M1102884
    title: "Yaniv Romano, Michael Elad and Peyman Milanfar, The little engine that could, regularization by denoising (RED), SIAM Journal on Imaging Sciences 10(4), 2017"
    locator: "pages 1804 to 1844 (the regularizer, the gradient under local homogeneity and a symmetric Jacobian, and the steepest descent, ADMM and fixed point solvers)"
  - paper: doi:10.1109/TCI.2018.2880326
    title: "Edward T. Reehorst and Philip Schniter, Regularization by denoising, clarifications and new interpretations, IEEE Transactions on Computational Imaging 5(1), 2019"
    locator: "pages 52 to 67 (the general gradient of the RED regularizer, the lack of Jacobian symmetry in practical denoisers, and the score matching reading of the RED algorithms)"
---

Regularization by denoising (RED) turns an image denoiser $D$ into an explicit regularizer for an inverse problem $y = Ax + e$:

$$R(x) = \tfrac12x^T\big(x - D(x)\big),\qquad \min_x\ \tfrac12\|Ax - y\|^2 + \lambda R(x).$$

The regularizer is small when $x$ is close to its denoised version or nearly orthogonal to the residual. Romano, Elad and Milanfar (2017) showed that, if $D$ is locally homogeneous and has a symmetric Jacobian, the gradient of $R$ is the denoising residual $x - D(x)$. Then gradient and fixed point methods need only one call to $D$ per step and no derivative of $D$. Reehorst and Schniter (2019) showed that common denoisers do not have a symmetric Jacobian. For them, $x - D(x)$ is not the gradient of $R$, nor of any function, and the RED algorithms do not minimize the RED objective. They still converge in many tests to a fixed point, whose meaning is the balance of the data gradient and the residual.

## In plain words

A noise remover takes an image and returns a cleaner one. The difference between the two is what the noise remover thinks is noise. RED uses that difference as a penalty: a candidate image is good if the noise remover would barely change it.

The reconstruction then takes small steps. Each step pulls the image toward agreement with the measured data and pushes it in the direction in which the noise remover would move it. Under two technical conditions on the noise remover, this is plain gradient descent on a clear score, so the method is easy to analyze. Most real noise removers break one of the conditions, and then the steps still settle down but no longer lower a score.

## When it applies

**Setting.** $x \in \mathbb{R}^n$, a forward matrix $A$, data $y$, a weight $\lambda > 0$, and a denoiser $D : \mathbb{R}^n \to \mathbb{R}^n$ that is differentiable with Jacobian $J_D(x)$.

**Fact 1 (the general gradient).** By the product rule,

$$\nabla R(x) = x - \tfrac12D(x) - \tfrac12J_D(x)^Tx.$$

This always holds. It needs the Jacobian of $D$, which is costly for a network.

**Fact 2 (Romano et al.).** Suppose $D$ is locally homogeneous, $D((1 + \epsilon)x) = (1 + \epsilon)D(x)$ for all small $\epsilon$, and $J_D(x)$ is symmetric. Differentiating the first condition in $\epsilon$ gives $J_D(x)x = D(x)$, and with the second, $J_D(x)^Tx = D(x)$. So Fact 1 becomes

$$\nabla R(x) = x - D(x).$$

If, in addition, the spectral radius of $J_D(x)$ is at most 1, Romano et al. show that $R$ is convex, so the RED objective is convex and every stationary point is a minimizer. A linear denoiser $D(x) = Wx$ is homogeneous, and the two facts give $\nabla R(x) = x - \tfrac12(W + W^T)x$; this is $x - Wx$ exactly when $W$ is symmetric.

**Fact 3 (Reehorst and Schniter).** If $J_D$ is not symmetric, the vector field $x - D(x)$ is not the gradient of any function, since a gradient field has a symmetric Jacobian. So no objective, $R$ or other, has the RED steps as gradient steps. The common denoisers they tested, including BM3D, non-local means and trained CNNs, do not have symmetric Jacobians. They give another reading, through score matching. For the MMSE denoiser at noise level $\sigma$, Tweedie's formula gives $D(x) - x = \sigma^2\nabla\log p_\sigma(x)$, where $p_\sigma$ is the prior smoothed by the noise. Then $x - D(x)$ is the gradient of $-\sigma^2\log p_\sigma$, not of $R$, and a RED fixed point is a stationary point of the MAP problem with the smoothed prior. A trained denoiser approximates this case.

Use RED when a good denoiser is at hand, when you want an explicit objective to monitor (with a linear symmetric or a carefully built denoiser), or when you want a method that uses the denoiser without its derivatives and accept a fixed point without a variational meaning.

## The template

```pseudo id=main
RED-GRADIENT(A, y, D, λ, μ, x_0, K)
L1  x ← x_0
L2  for k = 1 to K
L3      d ← D(x)                                ▷ hole: the denoiser, a given function
L4      g ← A^T(Ax - y) + λ(x - d)              ▷ the gradient, if Fact 2 holds
L5      x ← x - μ g
L6  return x
```

The holes are the denoiser, the weight $\lambda$, the step $\mu$ and $K$. Each step calls $A$, $A^T$ and $D$ once. Under Fact 2, a fixed step $\mu < 2/L$ is safe when $L$ is a Lipschitz constant of the full gradient; for a linear symmetric $W$, $L = \|A^TA + \lambda(I - W)\|$. Romano et al. also give two other solvers. The fixed point iteration solves $(A^TA + \lambda I)x_{k+1} = A^Ty + \lambda D(x_k)$, which sets the gradient of line L4 to zero with $D$ frozen at the old point. The ADMM form splits $x = v$ and updates $v$ by a few fixed point steps of $\lambda(v - D(v)) + \rho(v - x - u) = 0$. All three have the same fixed points: $A^T(Ax - y) + \lambda(x - D(x)) = 0$.

The denoiser is a given function: the code takes $D$ as an argument and runs lines L1 to L6 around it, and also gives the fixed point variant. The tests build $D$ by hand, as a fixed symmetric matrix, a fixed nonsymmetric matrix, or $\tanh(Bx)$ with a seeded matrix $B$; no network is trained. They check the hand example below, that with a symmetric $W$ the residual equals the finite difference gradient of $R$ and RED reaches the solution of $(A^TA + \lambda(I - W))x = A^Ty$, that with a nonsymmetric $W$ RED stops at a point that is not the minimizer, and Fact 1 for the nonlinear $\tanh$ denoiser.

## Classic examples

**A symmetric smoother.** Take $A = I$, $y = (1, 0)$, $\lambda = 1$ and the averaging denoiser $W = \begin{pmatrix}1/2 & 1/2\\ 1/2 & 1/2\end{pmatrix}$, which is symmetric with eigenvalues 1 and 0. Then $R(x) = \tfrac14(x_1 - x_2)^2$ and the minimizer solves $(2I - W)x = y$, so $x^\star = (0.75, 0.25)$. Gradient steps with $\mu = 0.5$ from $x_0 = 0$ give $(0.5, 0)$, $(0.625, 0.125)$, $(0.6875, 0.1875)$, $(0.71875, 0.21875)$, and the error halves at each step.

**A nonsymmetric denoiser.** Keep $A$, $y$ and $\lambda$, and let $W = \begin{pmatrix}0 & 1\\ 0 & 1\end{pmatrix}$, which replaces the first entry by the second. It is linear, so homogeneous, and its eigenvalues are 0 and 1, but $W$ is not symmetric. RED (both the gradient and the fixed point forms) stops at the solution of $(2I - W)x = y$, which is $(0.5, 0)$, with the objective value $0.25$. The RED objective has the gradient $(2I - \tfrac12(W + W^T))x - y$, so its minimizer is $(4/7, 2/7) = (0.5714, 0.2857)$, with the lower value $3/14 = 0.2143$. The RED iteration converges, but not to the minimizer of the RED objective.

**Practical denoisers.** Romano et al. used trained and classical denoisers in RED for deblurring and super-resolution of standard test images and compared the results with other methods, PnP among them. These comparisons are measurements on those images. By Fact 3, their convergence argument does not apply to those denoisers.

## Variations

- **Fixed point and ADMM solvers.** As in the template. The fixed point form needs a linear solve per step, and the ADMM form reuses a fast solver for the data term.
- **Accelerated RED.** Momentum and vector extrapolation of the fixed point iteration reduce the number of denoiser calls.
- **Score-based reading.** Reehorst and Schniter interpret $D(x) - x$ as a scaled score, which links RED to [diffusion posterior sampling](/diffusion-posterior-sampling/), where the denoiser is a score network at many noise levels.
- **Plug-and-play.** [PnP](/plug-and-play-priors/) uses $D$ as a proximal step instead of a gradient. With a denoiser that is a proximal map, PnP has an objective; with a symmetric, homogeneous denoiser, RED has one. The two conditions are different.
- **Gradient step denoisers.** Train the denoiser as $D = I - \nabla g$ for a network $g$; then $x - D(x)$ is a gradient by construction and RED-type methods minimize an explicit objective.

## Pitfalls

- **Assuming the gradient.** Using $x - D(x)$ as $\nabla R$ for a denoiser with a nonsymmetric Jacobian gives a method without an objective, as the second example shows. Do not report the RED objective value as a measure of progress then.
- **Step size.** Without Fact 2 there is no Lipschitz bound to set $\mu$. Use the fixed point form or check that $\|x_{k+1} - x_k\|$ goes down.
- **Weight and noise level.** The weight $\lambda$ and the noise level for which $D$ is set interact. Tune them together.
- **Cost of the true gradient.** Fact 1 needs $J_D^Tx$, one backpropagation through a network per step. It is exact but costs about as much again as the denoiser call.

## Exercises

1. Prove Fact 1, and derive Fact 2 from it.
2. For $W$ symmetric with eigenvalues in $[0, 1]$, show that $R(x) = \tfrac12x^T(I - W)x$ is convex, and find the minimizer of the RED objective with $A = I$.
3. Verify both examples. In the second, check that the RED fixed point satisfies $(2I - W)x = y$ and that the objective has a smaller value at $(4/7, 2/7)$.
4. Show that the soft threshold $D(x) = \operatorname{soft}(x, \theta)$ is not locally homogeneous. Compute $\nabla R$ by Fact 1 at a point where no entry equals $\pm\theta$, and compare it with $x - D(x)$.
5. Show that a smooth vector field $F$ on $\mathbb{R}^n$ is a gradient field only if its Jacobian is symmetric. Apply this to $F(x) = x - Wx$.

## References
