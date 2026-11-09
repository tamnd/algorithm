---
tag: R1B2TS
kind: algorithm
slug: natural-gradient-descent
name: Natural gradient descent
aliases:
- natural gradient
- natural gradient method
- Fisher-preconditioned gradient descent
area: optimization/gradient-methods
level: research
summary: Gradient descent preconditioned by the inverse Fisher information matrix, invariant to parameterization.
solves: [maximum-likelihood-estimation]
model: real-ram
complexity:
  vars: {n: the number of parameters, k: the number of iterations, g: the cost of one gradient of the loss, c: the cost of forming the Fisher matrix, β: the Lipschitz constant of the gradient of the loss, λ: the smallest eigenvalue bound of the damped Fisher matrix, Λ: the largest eigenvalue bound of the damped Fisher matrix, δ: "the initial gap L(θ_0) - inf L", ε: "the target squared gradient norm"}
  time: {worst: O(k (g + c + n^3))}
  space: {extra: Θ(n^2)}
  steps: {worst: "⌈2 β Λ δ / (λ ε)⌉"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1998
  people: [Shun-ichi Amari]
  note: Amari (1998) proposed the natural gradient, the steepest descent direction in the Fisher-Rao metric, and showed its efficiency for online learning.
prereqs: [fisher-information-matrix, gradient-descent, maximum-likelihood-estimation]
see_also: [kronecker-factored-approximate-curvature, natural-policy-gradient, newton-raphson-method, mirror-descent, logistic-regression, exponential-family-distribution, adam, bregman-divergence]
sources:
  - paper: doi:10.1162/089976698300017746
    title: Shun-ichi Amari, Natural gradient works efficiently in learning, Neural Computation 10(2), 1998
    locator: pages 251 to 276, the natural gradient as steepest descent in a Riemannian metric, and its Fisher efficiency in online learning
  - paper: "James Martens, New insights and perspectives on the natural gradient method, Journal of Machine Learning Research 21(146), 2020, pages 1 to 76"
    locator: the natural gradient as a second-order method, its relation to the generalized Gauss-Newton matrix, damping, and the empirical Fisher
  - url: https://arxiv.org/abs/1503.05671
    title: James Martens and Roger Grosse, Optimizing neural networks with Kronecker-factored approximate curvature, ICML 2015
    locator: Sections 3 and 6, the Kronecker-factored approximation of the Fisher and its damping
  - url: https://arxiv.org/abs/1905.12558
    title: Frederik Kunstner, Lukas Balles and Philipp Hennig, Limitations of the empirical Fisher approximation for natural gradient descent, NeurIPS 2019
    locator: Section 3, failure cases of the empirical Fisher as a preconditioner
  - paper: "Sham Kakade, A natural policy gradient, Advances in Neural Information Processing Systems 14, 2001"
    locator: the natural gradient of the expected return with the Fisher information of the policy
---

Natural gradient descent multiplies the [gradient](/gradient/) of a loss by the inverse of the [Fisher information matrix](/fisher-information-matrix/) $F(\theta)$ before it takes a step: $\theta_{k+1} = \theta_k - \eta F(\theta_k)^{-1}\nabla L(\theta_k)$. The Fisher matrix measures how fast the model's distribution changes with $\theta$, so the step is the steepest descent direction when distance is measured between distributions, not between parameter vectors. The result does not depend on how the model is parameterized, exactly for linear changes and to first order for nonlinear ones. Amari (1998) introduced it; for exponential families it reduces to [Newton's method](/newton-raphson-method/) in the natural parameter.

## In plain words

A model can be described by many sets of numbers. A probability can be given as the probability itself, or as its log-odds. Plain gradient descent gives different steps for the two descriptions, because a change of 0.01 means different things in each.

Natural gradient descent measures each step by how much it changes the predictions of the model, not by how much it changes the numbers. Then the description does not matter. Steps in directions where the model is very sensitive become small, and steps in directions where the model hardly changes become large.

## The problem

Minimize a loss $L(\theta)$ over $\theta \in \mathbb{R}^n$ where $L$ is the mean negative log-likelihood of a probabilistic model $p(y \mid x;\theta)$ on data, as in [maximum likelihood estimation](/maximum-likelihood-estimation/), or another loss on the outputs of such a model. The method needs the gradient and the Fisher information

$$F(\theta) = \mathbb{E}_{x}\,\mathbb{E}_{y \sim p(\cdot \mid x;\theta)}\big[\nabla_\theta\log p(y \mid x;\theta)\,\nabla_\theta\log p(y \mid x;\theta)^\top\big],$$

or an approximation of it. Notation: $\eta$ is the step size, $\lambda \ge 0$ is a damping constant, $\ell$ is the Lipschitz constant of $\nabla L$, and $mI \preceq F + \lambda I \preceq MI$.

## The algorithm

```pseudo id=main
NATURAL-GRADIENT(∇L, F, θ₀, η, λ, K)
L1  θ ← θ₀
L2  for k ← 0 to K − 1 do
L3      g ← ∇L(θ)
L4      G ← F(θ) + λI                  ▷ the Fisher matrix, with damping
L5      solve G d = g                  ▷ the natural gradient d = G⁻¹ g
L6      θ ← θ − η d
L7  return θ
```

For $\lambda = 0$, the step $-d$ is a positive multiple of the solution of $\min_v\{\langle g, v\rangle\ \text{subject to}\ \frac{1}{2}v^\top F v \le r\}$. Since $\frac{1}{2}d^\top F(\theta)d$ is the second-order term of $\operatorname{KL}(p_\theta\,\Vert\,p_{\theta + d})$, the natural gradient is the steepest descent direction in a small KL ball. For $n$ parameters, line L5 costs $O(n^3)$ and $F$ needs $O(n^2)$ memory, so large models use approximations such as [K-FAC](/kronecker-factored-approximate-curvature/) or conjugate gradient with Fisher-vector products.

## Example

Estimate the mean $q$ of Bernoulli data with sample mean $\bar{y} = 0.8$, in the parameter $q$ itself. The loss is $L(q) = -\bar{y}\log q - (1 - \bar{y})\log(1 - q)$, with $L'(q) = (q - \bar{y})/(q(1 - q))$ and $F(q) = 1/(q(1 - q))$. The natural gradient is $F^{-1}L' = q - \bar{y}$, so the step is $q_{k+1} = q_k - \eta(q_k - \bar{y})$, and the error is exactly $(1 - \eta)^k(q_0 - \bar{y})$. From $q_0 = 0.1$:

| $k$ | natural gradient, $\eta = 0.5$ | gradient descent, step $0.05$ |
|---|---|---|
| 0 | 0.1 | 0.1 |
| 1 | 0.45 | 0.48889 |
| 2 | 0.625 | 0.55114 |
| 3 | 0.7125 | 0.60144 |
| 4 | 0.75625 | 0.64286 |
| 5 | 0.77813 | 0.67708 |

With $\eta = 1$ the natural gradient reaches the maximum likelihood estimate $0.8$ in one step. Plain gradient descent takes a large first step, because $L'$ is large near $q = 0$, and then slows down. In the log-odds parameter $\theta = \log(q/(1 - q))$, the natural gradient direction is $(q - \bar{y})/(q(1 - q))$, which is the same direction mapped through $d\theta/dq = 1/(q(1 - q))$.

## Correctness

Natural gradient descent is a preconditioned gradient method, so its correctness rests on three facts, all proved below.

- **Invariance.** Under a linear change of parameter $\theta = B\xi + c$, the Fisher matrix transforms as $B^\top FB$ and the gradient as $B^\top\nabla L$. So the step in $\xi$ maps exactly to the step in $\theta$. Under a nonlinear change, the direction maps through the Jacobian, so the continuous flow is invariant and a finite step changes at second order.
- **Descent.** If $L$ has an $\ell$-Lipschitz gradient and $mI \preceq F + \lambda I \preceq MI$, the step $\eta = m/\ell$ decreases $L$ by at least $\frac{m}{2\ell}g^\top(F + \lambda I)^{-1}g$, and $\min_{k<K}\lVert\nabla L(\theta_k)\rVert^2 \le 2\ell M(L(\theta_0) - \inf L)/(mK)$.
- **Exponential families.** In the mean parameter $\mu$ of an [exponential family](/exponential-family-distribution/), the natural gradient of the negative log-likelihood is $\mu - \bar{T}$, so the error contracts by exactly $1 - \eta$ per step. In the natural parameter, the Fisher matrix equals the Hessian, and the method with $\eta = 1$ is Newton's method, called Fisher scoring.

## Complexity

One step costs a gradient, the Fisher matrix and a linear solve: $O(n^3)$ time with $\Theta(n^2)$ memory for an explicit $F$. For a model with $N$ data points and a scalar output per point, forming $F$ costs $O(Nn^2)$. The descent guarantee gives $\lceil 2\ell M\delta/(m\varepsilon)\rceil$ steps for $\min\lVert\nabla L\rVert^2 \le \varepsilon$, with $\delta = L(\theta_0) - \inf L$. This general bound is not better than that of gradient descent. The gains come from the special structure: exact contraction in mean parameters, Newton's local quadratic rate for exponential families in natural parameters, and the asymptotic efficiency of the online version (Amari 1998).

## Properties

- **Parameterization invariant.** Exactly for linear changes, and to first order for nonlinear ones. Damping $\lambda I$ breaks the exact invariance.
- **A second-order method.** For log-likelihood losses, $F$ is the expected Hessian. For models whose outputs are natural parameters, it is the generalized Gauss-Newton matrix, which is positive semidefinite even where the Hessian is not.
- **Fisher efficient online.** Amari (1998) showed that online natural gradient with the step $1/k$ is asymptotically as efficient as the maximum likelihood estimate.
- **Deterministic** in the batch form above.

## Variants and improvements

- **Damping and trust regions.** Add $\lambda I$ and adapt $\lambda$ with a trust region rule, as in Levenberg-Marquardt.
- **K-FAC.** Approximate each layer's block of $F$ by a Kronecker product of two small matrices, so the inverse is cheap (Martens and Grosse 2015).
- **Hessian-free natural gradient.** Solve line L5 by conjugate gradient with Fisher-vector products, which cost about two gradients.
- **Natural policy gradient.** Use the Fisher information of a policy to precondition the policy gradient in reinforcement learning (Kakade 2001). [Natural policy gradient](/natural-policy-gradient/) and trust region policy optimization build on it.
- **Diagonal approximations.** Keep only the diagonal of $F$. With the empirical Fisher, this is close to the second-moment estimate of [Adam](/adam/), but the analogy is loose.

## When to use it

Use the exact natural gradient for small probabilistic models, generalized linear models (where it is Fisher scoring) and models with a strong dependence on the parameterization, such as mixtures and variational families. For neural networks, use an approximation such as K-FAC when a cheap enough curvature estimate exists. For very large models, first-order adaptive methods are cheaper per step.

## Pitfalls

- **Empirical Fisher.** The outer product of the gradients at the observed labels is not the Fisher information. Away from a good fit it can give poor steps (Kunstner, Balles and Hennig 2019).
- **Singular Fisher.** Redundant parameters or saturated outputs make $F$ singular. Always add damping.
- **Step size.** Invariance does not choose $\eta$. Too large a step can leave the domain, for example $q \notin (0, 1)$, in a nonlinear parameterization.
- **Cost.** An explicit $F$ with $n = 10^6$ parameters needs $10^{12}$ entries; use structure or matrix-free solves.

## Implementations

## History

Amari (1998) introduced the natural gradient as the steepest descent direction in the Riemannian metric given by the Fisher information, building on the information geometry of statistical models, and proved its efficiency for online learning. Kakade (2001) applied it to policy gradients. Martens and Grosse (2015) made it practical for neural networks with Kronecker-factored approximations, and Martens (2020) related it to second-order methods and the generalized Gauss-Newton matrix.

## References
