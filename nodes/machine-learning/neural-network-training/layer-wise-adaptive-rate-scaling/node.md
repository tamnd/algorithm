---
tag: ZN48H9
kind: technique
slug: layer-wise-adaptive-rate-scaling
name: Layer-wise adaptive rate scaling
aliases:
- LARS
- LARS optimizer
area: machine-learning/neural-network-training
level: advanced
summary: Gives each layer the learning rate eta times its weight norm over its gradient norm, so every layer changes by the same fraction per step; used for large batch SGD.
prereqs: [stochastic-gradient-descent, momentum-method]
see_also: [lamb, learning-rate-schedule, gradient-accumulation, data-parallelism, batch-normalization, weight-decay, adamw]
sources:
  - url: https://arxiv.org/abs/1708.03888
    title: Yang You, Igor Gitman and Boris Ginsburg, Large batch training of convolutional networks, arXiv 2017
    locator: Section 4 (Eq. 5 and Eq. 6, the local learning rate with the trust coefficient eta), Algorithm 1 (SGD with momentum and LARS, polynomial decay of power 2), Table 2 (ratios of weight norm to gradient norm in AlexNet with batch normalization)
  - url: https://arxiv.org/abs/1904.00962
    title: Yang You, Jing Li, Sashank Reddi, Jonathan Hseu, Sanjiv Kumar, Srinadh Bhojanapalli, Xiaodan Song, James Demmel, Kurt Keutzer and Cho-Jui Hsieh, Large batch optimization for deep learning, training BERT in 76 minutes, ICLR 2020
    locator: Algorithm 1 (LARS with the scaling function phi), Section 3 (the general layerwise strategy) and Theorem 2 (convergence of LARS)
  - url: https://arxiv.org/abs/1706.02677
    title: Priya Goyal and others, Accurate, large minibatch SGD, training ImageNet in 1 hour, arXiv 2017
    locator: Section 2.1 and 2.2 (the linear scaling rule and warmup, the baseline LARS improves on)
---

Layer-wise adaptive rate scaling (LARS) gives each layer $l$ of a network its own learning rate, proportional to $\lVert w^l\rVert/\lVert\nabla L(w^l)\rVert$, the ratio of the norm of its weights to the norm of its gradient. You, Gitman and Ginsburg (2017) observed that in large batch training of convolutional networks this ratio differs by orders of magnitude between layers, so one global learning rate is too large for some layers and too small for others. With LARS, every layer moves by the same fraction $\eta$ of its weight norm per step (times the global rate), which let them train AlexNet with batch normalization and ResNet-50 on ImageNet with batches of 32K. It changes the update step of [SGD with momentum](/momentum-method/); the per layer trust ratio is also the core of [LAMB](/lamb/).

## In plain words

In a deep network some layers have large weights and small gradients, and others have small weights and large gradients. One learning rate for all of them changes some layers by a tiny fraction and others by more than their own size. That second case makes training diverge, so the learning rate must stay small, which is a problem when large batches call for a large learning rate.

LARS measures, for each layer, the size of its weights and the size of its gradient, and scales that layer's step so that the change is a fixed small fraction of the layer's size. The gradient only gives the direction. All layers then learn at a similar relative speed.

## When it applies

- **Large batch training.** Data parallel training with a batch of thousands to tens of thousands of examples, where the [linear scaling rule](/learning-rate-schedule/) asks for a learning rate that makes some layers diverge even with warmup.
- **Layers with very different ratios.** Convolutional networks, in particular with [batch normalization](/batch-normalization/), where the output of a layer does not depend on the scale of its weights, so only the relative change matters.
- **SGD with momentum as the base method.** For Adam-type methods the same idea gives [LAMB](/lamb/).

It does not help at small batch sizes, where a single tuned learning rate already works, and it was found to work poorly for attention models such as BERT, which motivated LAMB.

## The template

For each layer $l$ with weights $w^l$ and gradient $g^l$, the local learning rate (Eq. 6 of the paper) is
$$\lambda^l = \eta\,\frac{\lVert w^l\rVert}{\lVert g^l\rVert + \beta\lVert w^l\rVert},$$
where $\eta < 1$ is the trust coefficient, for example $0.001$, and $\beta$ is the [weight decay](/weight-decay/) coefficient. With $\beta = 0$ this is Eq. 5, $\lambda^l = \eta\lVert w^l\rVert/\lVert g^l\rVert$.

```pseudo id=main
LARS(w, γ₀, μ, β, η, T)                ▷ w = (w¹, …, wᴸ), one vector per layer
L1  v ← 0                                       ▷ one momentum vector per layer
L2  for t ← 0 to T − 1 do
L3      g ← minibatch gradient at w
L4      γₜ ← γ₀ (1 − t/T)²                       ▷ global rate, polynomial decay
L5      for each layer l do
L6          λˡ ← η ‖wˡ‖ / (‖gˡ‖ + β ‖wˡ‖)          ▷ local rate, the trust ratio
L7          vˡ ← μ vˡ + γₜ λˡ (gˡ + β wˡ)
L8          wˡ ← wˡ − vˡ
L9  return w
```

This is Algorithm 1 of the paper. Without momentum ($\mu = 0$) and with $\beta = 0$, the step of layer $l$ is $\gamma_t\eta\lVert w^l\rVert\, g^l/\lVert g^l\rVert$, so its norm is exactly $\gamma_t\eta\lVert w^l\rVert$: the step changes every layer by the same fraction $\gamma_t\eta$, for any gradient. With $\beta > 0$ the triangle inequality gives $\lVert g^l + \beta w^l\rVert \le \lVert g^l\rVert + \beta\lVert w^l\rVert$, so the step norm is at most $\gamma_t\eta\lVert w^l\rVert$, with equality when $g^l$ is a nonnegative multiple of $w^l$. With momentum the fraction holds for the increments added to $v$, not for each step. The step does not depend on the scale of $g^l$: multiplying a layer's gradient by $c > 0$ leaves the iterates the same when $\beta = 0$.

The LAMB paper writes LARS with the momentum inside the normalization: $m^l \leftarrow \beta_1 m^l + (1 - \beta_1)(g^l + \lambda w^l)$ and $w^l \leftarrow w^l - \eta_t\,\phi(\lVert w^l\rVert)\, m^l/\lVert m^l\rVert$, where $\phi(z) = \min(\max(z, \gamma_l), \gamma_u)$ bounds the weight norm. In this form every step has norm exactly $\eta_t\phi(\lVert w^l\rVert)$.

## Classic examples

**Two layers by hand.** Let $\gamma = 1$, $\eta = 0.001$, $\beta = 0$, no momentum. Layer 1 has $w^1 = (3, 4)$, $\lVert w^1\rVert = 5$, and $g^1 = (0, 0.01)$, so $\lambda^1 = 0.001 \cdot 5/0.01 = 0.5$ and the step is $(0, 0.005)$, norm $0.005 = 0.001 \cdot 5$. Layer 2 has $w^2 = (0.3, 0.4)$, $\lVert w^2\rVert = 0.5$, and $g^2 = (6, 8)$, $\lVert g^2\rVert = 10$, so $\lambda^2 = 0.00005$ and the step is $(0.0003, 0.0004)$, norm $0.0005 = 0.001 \cdot 0.5$. Both layers change by $0.1\%$. Plain SGD with learning rate $0.1$ would change layer 1 by $0.001/5 = 0.02\%$ and layer 2 by $1/0.5 = 200\%$.

**AlexNet with batch normalization.** Table 2 of the paper lists ratios $\lVert w\rVert/\lVert\nabla L(w)\rVert$ from $5.76$ for the first convolution weights to $1345$ for the first fully connected weights: more than two orders of magnitude between layers of the same network.

**ImageNet with batches of 32K.** With LARS, warmup and polynomial decay, the paper trains AlexNet with batch normalization and ResNet-50 with batches up to 32K at a small loss of accuracy against small batch training. Plain SGD with the linear scaling rule and warmup (Goyal and others, 2017) loses much more accuracy at that size.

## Variations

- **Clipped trust ratio.** Some implementations clip $\lambda^l/\eta$ or use $\phi$ to bound the weight norm, as in the LAMB paper, so that layers with tiny or huge weights do not get extreme rates.
- **Excluded parameters.** Biases and batch normalization gains and shifts are often excluded from both the weight decay and the trust ratio, and use the global rate.
- **Zero weight norm.** Implementations set the trust ratio to $1$ when $\lVert w^l\rVert = 0$ or $\lVert g^l\rVert = 0$; otherwise a layer that starts at zero would never move.
- **Adam base.** Using Adam's normalized direction in place of the gradient, with the same trust ratio, gives [LAMB](/lamb/).
- **Convergence.** Theorem 2 of the LAMB paper shows that LARS reaches a stationary point of a smooth nonconvex loss at a rate that depends on the average of the per layer smoothness constants, instead of their maximum.

## Pitfalls

- **Coefficient name clash.** The paper's $\beta$ is weight decay and $\eta$ the trust coefficient, while momentum is $m$; in the LAMB paper $\beta_1$ is momentum and $\lambda$ is weight decay. Check which constant a library means.
- **Global rate still matters.** LARS fixes the ratio between layers, not the overall size; the global rate $\gamma_t$ still needs warmup and decay, and the paper's ImageNet runs use both.
- **Bad fit for attention models.** LARS performs poorly on BERT pretraining according to the LAMB paper; use LAMB there.
- **Small batches.** At ordinary batch sizes LARS adds a hyperparameter and gives little benefit.

## Exercises

1. Show that with $\beta = 0$ and no momentum the LARS step of a layer has norm $\gamma_t\eta\lVert w^l\rVert$, and that with $\beta > 0$ it is at most that. When is it equal?
2. Show that with $\beta = 0$ the LARS iterates do not change when the gradient of one layer is multiplied by a positive constant at every step, with or without momentum.
3. A layer followed by batch normalization computes the same function for $w$ and $cw$, $c > 0$. Show that its gradient at $cw$ is $1/c$ times its gradient at $w$, and explain why plain SGD then effectively changes the learning rate of that layer as $\lVert w\rVert$ grows, while LARS does not.
4. In the LAMB paper form, with $\phi(z) = \min(\max(z, \gamma_l), \gamma_u)$, give the step norm for $\lVert w\rVert < \gamma_l$, $\gamma_l \le \lVert w\rVert \le \gamma_u$ and $\lVert w\rVert > \gamma_u$.

## References
