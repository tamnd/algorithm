---
tag: GSR20V
kind: algorithm
slug: sharpness-aware-minimization
name: Sharpness-aware minimization
aliases:
- SAM
- SAM optimizer
area: machine-learning/neural-network-training
level: research
summary: Trains on the worst loss in a small ball around the weights; each step takes a gradient at w + rho g/||g||, so it costs two gradients and favors flat minima.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the number of parameters, k: the number of steps, g: the cost of one minibatch gradient}
  time: {worst: O(k (2 g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2021
  people: [Pierre Foret, Ariel Kleiner, Hossein Mobahi, Behnam Neyshabur]
  note: Foret, Kleiner, Mobahi and Neyshabur introduced SAM with a PAC-Bayes motivation and improved image classification results, at ICLR 2021.
prereqs: [stochastic-gradient-descent, generalization-error]
see_also: [overfitting, regularization, kronecker-factored-approximate-curvature, adamw, learning-rate-schedule, margin-generalization-bound, eigenvalue, power-iteration]
sources:
  - url: https://arxiv.org/abs/2010.01412
    title: Pierre Foret, Ariel Kleiner, Hossein Mobahi and Behnam Neyshabur, Sharpness-aware minimization for efficiently improving generalization, ICLR 2021
    locator: Section 2 (Theorem 1, Eq. 2 for the perturbation, Eq. 3 for the gradient approximation, Algorithm 1), Section 3 (experiments), Section 4.1 (m-sharpness), Section 4.2 (Hessian spectra), Appendix A.1 (proof of Theorem 1)
  - url: https://arxiv.org/abs/1609.04836
    title: Nitish Shirish Keskar, Dheevatsa Mudigere, Jorge Nocedal, Mikhail Smelyanskiy and Ping Tak Peter Tang, On large-batch training for deep learning, generalization gap and sharp minima, ICLR 2017
    locator: the sharpness measure over a small box and the link between large batches, sharp minima and worse test error
  - url: https://arxiv.org/abs/2102.11600
    title: Jungmin Kwon, Jeongseop Kim, Hyunseo Park and In Kwon Choi, ASAM, adaptive sharpness-aware minimization for scale-invariant learning of deep neural networks, ICML 2021
    locator: the scale-invariant neighborhood (adaptive sharpness)
---

Sharpness-aware minimization (SAM) trains a network on the worst loss in a small ball around the current weights, $\max_{\lVert\epsilon\rVert \le \rho} L(w + \epsilon)$, instead of the loss at the weights. Foret, Kleiner, Mobahi and Neyshabur (2021) approximate the inner maximum by one gradient step: with $g = \nabla L(w)$, the worst perturbation is about $\hat{\epsilon} = \rho g/\lVert g\rVert$, and SAM updates the weights with the gradient taken at $w + \hat{\epsilon}$. Each step costs two forward and backward passes. The motivation is a PAC-Bayes bound in which the worst loss over the ball, and so the sharpness of the minimum, controls the [generalization error](/generalization-error/). SAM wraps any base optimizer, SGD with momentum or [AdamW](/adamw/); it changes the gradient that the update step uses.

## In plain words

Two sets of weights can have the same training loss, but one sits in a narrow valley and the other in a wide one. In the narrow valley, a small change of the weights makes the loss jump; such solutions tend to do worse on new data.

SAM asks, at each step, which small change of the weights would hurt the most. The gradient already points that way, so SAM moves a short fixed distance uphill, computes the gradient there, and then uses that gradient to update the original weights. The network is pushed toward places where even the worst nearby weights have low loss, which are the wide valleys.

## The problem

Given a training loss $L_S(w)$ of a network, for example a Wide ResNet or PyramidNet on CIFAR, a ResNet on ImageNet, or a vision transformer, find weights that have low loss and generalize well. SAM solves
$$\min_w\ L_S^{\text{SAM}}(w) + \lambda\lVert w\rVert_2^2, \qquad L_S^{\text{SAM}}(w) = \max_{\lVert\epsilon\rVert_p \le \rho} L_S(w + \epsilon),$$
where $\rho$ is the size of the neighborhood and $p = 2$ in practice. The sharpness is $L_S^{\text{SAM}}(w) - L_S(w)$.

| symbol | meaning |
|---|---|
| $w$ | the weights |
| $L_S, L_{\mathcal{B}}$ | the training loss and the loss of a minibatch $\mathcal{B}$ |
| $\rho$ | the radius of the neighborhood, default $0.05$ |
| $\hat{\epsilon}(w)$ | the approximate worst perturbation |
| $\eta$ | the learning rate of the base optimizer |

## The algorithm

```pseudo id=main
SAM(w, η, ρ, μ, T)
L1  v ← 0
L2  for t ← 1 to T do
L3      g ← ∇L_B(w) for a minibatch B                 ▷ first forward and backward pass
L4      ε̂ ← ρ g / ‖g‖₂                                ▷ ε̂ ← 0 when g = 0
L5      g_SAM ← ∇L_B(w + ε̂), on the same minibatch     ▷ second pass
L6      v ← μ v + g_SAM                                ▷ base optimizer, here SGD with momentum
L7      w ← w − η v
L8  return w
```

This is Algorithm 1 of the paper with SGD with momentum as the base optimizer. For a general $p$, line L4 uses $\hat{\epsilon} = \rho\operatorname{sign}(g)\lvert g\rvert^{q-1}/(\lVert g\rVert_q^q)^{1/p}$ with $1/p + 1/q = 1$ (Eq. 2); the paper finds $p = 2$ best. The weights are only perturbed for line L5; the update in line L7 starts from $w$. The full gradient of $L_S(w + \hat{\epsilon}(w))$ has a second term with the Hessian, which the paper drops (Eq. 3).

## Example

Take the quadratic $L(w) = \tfrac12w^\top Hw + b^\top w$ with
$$H = \begin{pmatrix} 2 & 1\\ 1 & 3\end{pmatrix},\quad b = \begin{pmatrix} -1\\ 2\end{pmatrix},\quad w = \begin{pmatrix} 2\\ 0\end{pmatrix},\quad \rho = 0.05.$$
The gradient is $g = Hw + b = (3, 4)$, with $\lVert g\rVert = 5$, so $\hat{\epsilon} = 0.05 \cdot (3, 4)/5 = (0.03, 0.04)$. The gradient at $w + \hat{\epsilon} = (2.03, 0.04)$ is
$$g^{\text{SAM}} = H(w + \hat{\epsilon}) + b = (3.1,\ 4.15) = g + \rho\,Hg/\lVert g\rVert,$$
since $Hg = (10, 15)$. SAM adds to the gradient a term along $Hg$, which is larger in directions of high curvature.

At a minimum $w^*$ of a quadratic with Hessian $H$, the sharpness is $\tfrac12\rho^2\lambda_{\max}(H)$. Two minima with equal loss and curvatures $30$ and $1$ have, with $\rho = 0.05$, SAM losses higher by $0.0375$ and $0.00125$: SAM prefers the flat one.

## Correctness

The proof file shows what the two gradient evaluations compute:

- **The perturbation.** $\hat{\epsilon}$ is the exact maximizer of the first order Taylor expansion $L(w) + g^\top\epsilon$ over $\lVert\epsilon\rVert_p \le \rho$, by Hölder's inequality; it has norm $\rho$ and gives $g^\top\hat{\epsilon} = \rho\lVert g\rVert_q$.
- **Second order error.** If $\nabla L$ is $\beta$-Lipschitz, $0 \le L^{\text{SAM}}(w) - L(w + \hat{\epsilon}) \le \beta\rho^2$.
- **The gradient.** $\nabla L(w + \hat{\epsilon})$ is the gradient of $L(w + \hat{\epsilon}(w))$ without the term $D\hat{\epsilon}(w)^\top\nabla L(w + \hat{\epsilon})$, which involves the Hessian. On a quadratic it is exactly $g + \rho Hg/\lVert g\rVert$.
- **Sharpness of a minimum.** At a minimum of a convex quadratic, $L^{\text{SAM}} - L = \tfrac12\rho^2\lambda_{\max}(H)$.

Theorem 1 of the paper bounds the population loss: with high probability, $L_{\mathcal{D}}(w) \le \max_{\lVert\epsilon\rVert_2 \le \rho} L_S(w + \epsilon) + h(\lVert w\rVert_2^2/\rho^2)$ for an increasing function $h$. The formal version in Appendix A.1 adds the assumption that the population loss does not decrease under Gaussian perturbations of the weights. The bound motivates SAM; it is not a convergence result.

## Complexity

Each step costs two gradient evaluations on the same minibatch plus $O(d)$ arithmetic, so a SAM epoch takes about twice the time of an epoch of the base optimizer. The extra memory is one vector of size $d$ to store $w$ or $\hat{\epsilon}$ while the second gradient is computed. In data parallel training each worker computes $\hat{\epsilon}$ from its own part of the batch, which is the m-sharpness variant with $m$ equal to the per worker batch size.

## Properties

- **Wrapper.** SAM changes only the gradient; momentum, weight decay and the learning rate schedule of the base optimizer stay the same.
- **Fixed points.** Where $g = 0$, $\hat{\epsilon} = 0$ and the SAM gradient is $0$, so every stationary point of $L$ is a fixed point of exact SAM; the preference for flat minima acts during training, through the extra term $\rho Hg/\lVert g\rVert$.
- **Lower Hessian spectrum.** Section 4.2 of the paper reports that SAM reaches minima with a smaller top Hessian eigenvalue and a smaller ratio of the largest to the fifth largest eigenvalue than SGD, measured on a Wide ResNet on CIFAR-10.
- **Not scale invariant.** For networks with normalization, scaling the weights of a layer does not change the function, but it changes the ball $\lVert\epsilon\rVert \le \rho$; adaptive variants fix this.
- **Label noise.** The paper reports that SAM is robust to noisy labels, close to methods built for that purpose.

## Variants and improvements

- **m-sharpness.** Compute $\hat{\epsilon}$ separately on small parts of size $m$ of the batch and average the gradients. Section 4.1 of the paper finds that smaller $m$ generalizes better.
- **Adaptive SAM (ASAM).** Kwon and others (2021) scale the ball by the size of each weight, $\lVert T_w^{-1}\epsilon\rVert \le \rho$, so that the sharpness does not change when a layer is rescaled.
- **Cheaper SAM.** Variants compute the perturbation only every few steps or on a part of the batch to reduce the factor of two in cost.
- **Other $p$.** With $p = \infty$, $\hat{\epsilon} = \rho\operatorname{sign}(g)$, as in the fast gradient sign method for adversarial examples, but in weight space.

## When to use it

Use SAM when generalization matters more than training time and the base optimizer is already tuned: image classification with residual networks and vision transformers, fine tuning, and training with noisy labels. It is not useful when the training budget is fixed in passes over the data and the doubled cost per step would mean half as many steps; compare at equal compute. Tune $\rho$, for example in $\{0.01, 0.02, 0.05, 0.1, 0.2, 0.5\}$.

## Pitfalls

- **Batch normalization statistics.** The second pass at $w + \hat{\epsilon}$ should not update the running means and variances of [batch normalization](/batch-normalization/), or it must be done so that the statistics stay consistent.
- **Different minibatch.** Lines L3 and L5 must use the same minibatch; with a new minibatch, $\hat{\epsilon}$ no longer points to the worst direction for the loss being differentiated.
- **Gradient clipping and mixed precision.** Clip or unscale the gradient that the update uses, $g_{\text{SAM}}$, and compute $\hat{\epsilon}$ from the unscaled $g$.
- **Equal compute comparisons.** SAM with $T$ steps costs as much as the base optimizer with $2T$ steps; claims of improvement should compare at equal cost.

## Implementations

## History

The link between flat minima and generalization goes back to Hochreiter and Schmidhuber (1997). Keskar and others (2017) argued that large batch training finds sharp minima that generalize worse. Foret, Kleiner, Mobahi and Neyshabur (2020, ICLR 2021) turned the worst loss in a neighborhood into a training objective with a cheap first order approximation and reported improved results on CIFAR, ImageNet and fine tuning tasks. Later work studied why the method works and proposed adaptive and cheaper variants.

## References
