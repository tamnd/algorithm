---
tag: CJHJQ5
kind: algorithm
slug: lamb
name: LAMB optimizer
aliases:
- layer-wise adaptive moments optimizer for batch training
- LAMB
area: machine-learning/neural-network-training
level: advanced
summary: Adam's normalized direction with decoupled weight decay, rescaled per layer so that each layer moves by the learning rate times its weight norm; built for very large batches.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the number of parameters, h: the number of layers, k: the number of steps, g: the cost of one minibatch gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2020
  people: [Yang You, Jing Li, Sashank Reddi, Jonathan Hseu, Sanjiv Kumar, Srinadh Bhojanapalli, Xiaodan Song, James Demmel, Kurt Keutzer, Cho-Jui Hsieh]
  note: You and others combined Adam with the layerwise trust ratio of LARS and pretrained BERT with batches of 32K and 64K, at ICLR 2020.
prereqs: [adam, layer-wise-adaptive-rate-scaling]
see_also: [adamw, adafactor, learning-rate-schedule, gradient-accumulation, data-parallelism, layer-normalization, radam]
sources:
  - url: https://arxiv.org/abs/1904.00962
    title: Yang You, Jing Li, Sashank Reddi, Jonathan Hseu, Sanjiv Kumar, Srinadh Bhojanapalli, Xiaodan Song, James Demmel, Kurt Keutzer and Cho-Jui Hsieh, Large batch optimization for deep learning, training BERT in 76 minutes, ICLR 2020
    locator: Section 3 (the general strategy and phi), Section 3.2 (Algorithm 2 and Theorem 3), Section 4.1 (BERT training, Table 1), Appendix E (removing the bias correction), Appendix H (default hyperparameters)
  - url: https://arxiv.org/abs/1708.03888
    title: Yang You, Igor Gitman and Boris Ginsburg, Large batch training of convolutional networks, arXiv 2017
    locator: Section 4 (the layerwise trust ratio of LARS)
  - url: https://arxiv.org/abs/1711.05101
    title: Ilya Loshchilov and Frank Hutter, Decoupled weight decay regularization, ICLR 2019
    locator: Algorithm 2 (AdamW, the decoupled decay that LAMB adds to the direction)
---

LAMB is an optimizer for training with very large batches. For each layer it takes [Adam](/adam/)'s normalized direction $r = \hat{m}/(\sqrt{\hat{v}} + \epsilon)$, adds the decoupled weight decay $\lambda x$ of [AdamW](/adamw/), and rescales the result so that the step of the layer has norm $\eta_t\,\phi(\lVert x\rVert)$: the learning rate times the weight norm, clipped by a function $\phi$. This is the trust ratio of [LARS](/layer-wise-adaptive-rate-scaling/) applied on top of Adam. You and others (2020) used it to pretrain BERT with batches of 32K, and with a mixed schedule of 64K and 32K in 76 minutes on 1024 TPUv3 chips, where LARS diverges and AdamW loses accuracy. It changes the update step of the training loop; the gradients are ordinary data parallel minibatch gradients.

## In plain words

When the batch is very large, people raise the learning rate to make fewer steps count more. A large learning rate can be too large for some layers and still too small for others, because layers differ in the size of their weights and gradients.

LAMB first computes the Adam step for each weight. Then, for each layer, it throws away the length of that step and keeps only its direction. It sets the length to the learning rate times the size of the layer's weights. Every layer then changes by the same small fraction per step, and one learning rate works for all of them.

## The problem

Minimize the training loss of a deep network, for example BERT, a transformer encoder, or a ResNet, with minibatch gradients from batches so large that the number of steps is small. The parameters are split into $h$ layers $x^{(1)}, \ldots, x^{(h)}$ (in practice each weight matrix, bias or normalization vector is its own "layer"). The goal is a method that keeps the accuracy of small batch training at batch sizes in the tens of thousands, with one learning rate schedule for all layers.

| symbol | meaning |
|---|---|
| $x_t^{(i)}$ | the weights of layer $i$ at step $t$ |
| $\eta_t$ | the learning rate at step $t$ |
| $\beta_1, \beta_2, \epsilon$ | Adam's constants |
| $\lambda$ | the decoupled weight decay coefficient |
| $\phi$ | the scaling function, $\phi(z) = \min(\max(z, \gamma_l), \gamma_u)$, or the identity |

## The algorithm

```pseudo id=main
LAMB(x₁, η, β₁, β₂, ε, λ, φ, T)
L1  m ← 0;  v ← 0
L2  for t ← 1 to T do
L3      g ← minibatch gradient at xₜ
L4      for each layer i do
L5          m⁽ⁱ⁾ ← β₁ m⁽ⁱ⁾ + (1 − β₁) g⁽ⁱ⁾
L6          v⁽ⁱ⁾ ← β₂ v⁽ⁱ⁾ + (1 − β₂) (g⁽ⁱ⁾)²
L7          r ← (m⁽ⁱ⁾/(1 − β₁ᵗ)) / (√(v⁽ⁱ⁾/(1 − β₂ᵗ)) + ε)       ▷ Adam's direction
L8          u ← r + λ x⁽ⁱ⁾                                      ▷ decoupled decay
L9          q ← φ(‖x⁽ⁱ⁾‖) / ‖u‖                                  ▷ trust ratio
L10         x⁽ⁱ⁾ ← x⁽ⁱ⁾ − ηₜ q u
L11 return x
```

This is Algorithm 2 of the paper. Appendix E reports that dropping the bias correction in line L7 does not hurt accuracy. The defaults are $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-6}$ and $\lambda = 0.01$, with a linear decay $\eta_t = \eta_0(1 - t/T)$ after a warmup. When $\lVert x^{(i)}\rVert = 0$ or $\lVert u\rVert = 0$, implementations set $q = 1$, and they often exclude biases and normalization parameters from the trust ratio and the decay.

## Example

One layer with $x = (3, 4)$ and gradient $g = (0.5, -2)$ at step 1, with $\epsilon = 0$, $\lambda = 0.01$, $\eta_1 = 0.01$ and $\phi$ the identity. After bias correction $\hat{m} = g$ and $\hat{v} = g^2$, so $r = \operatorname{sign}(g) = (1, -1)$ and $u = r + 0.01x = (1.03, -0.96)$, with $\lVert u\rVert = \sqrt{1.9825} = 1.40801$. The trust ratio is $q = \lVert x\rVert/\lVert u\rVert = 5/1.40801 = 3.55111$, so the step is $\eta_1 q u = (0.036576, -0.034091)$ and
$$x_2 = (2.963424,\ 4.034091).$$
The step has norm $0.05 = \eta_1\lVert x\rVert$: the layer changed by $1\%$. Adam with the same learning rate would move by $0.01$ per coordinate, a norm of $0.0141$, whatever the size of $x$; for a layer with $\lVert x\rVert = 0.01$ that is a change of $141\%$, and LAMB would still change it by $1\%$.

On BERT, the paper's Table 1 reports an F1 score of 91.475 on SQuAD v1.1 for LAMB with batch 32K in 15,625 steps, about 101 minutes, against 90.395 for the baseline trained for about 3 days on 16 TPUv3 chips; the mixed 64K and 32K run took 8,599 steps and 76.19 minutes with F1 90.584.

## Correctness

The proof file shows the properties that define LAMB:

- **Step norm.** For every layer with $u \ne 0$, the step has norm exactly $\eta_t\,\phi(\lVert x^{(i)}\rVert)$. With $\phi$ the identity, every layer changes by the relative amount $\eta_t$, for any gradients.
- **Weight scale.** For a layer followed by normalization, where the loss satisfies $\ell(cx) = \ell(x)$, starting from $cx$ gives the trajectory scaled by $c$ (with $\epsilon = 0$ and $\lambda = 0$). Adam's trajectory would not scale, so its relative change depends on the weight scale.
- **Gradient scale.** As in Adam, multiplying the gradients of a coordinate by a constant changes nothing when $\epsilon = 0$.

Theorem 3 of the paper gives convergence to a stationary point of a smooth nonconvex loss with $\beta_1 = 0$, $\lambda = 0$ and batch size equal to the number of steps; for $\beta_2 = 0$ the bound depends on the average $L_{\text{avg}}$ of the per layer smoothness constants, not on their maximum.

## Complexity

Each step costs one gradient and $O(d)$ arithmetic: Adam's update plus two norms per layer, $O(d)$ in total. The state is $m$ and $v$, $2d$ numbers, as for Adam. In data parallel training the norms are computed after the gradients are reduced, so they add no communication. Over $k$ steps the time is $O(k(g + d))$.

## Properties

- **Layerwise relative step.** The step norm of each layer is set by its weight norm, not by the gradient; the gradient sets only the direction.
- **Large learning rates.** Because no layer can move more than the fraction $\eta_t$ of its size, the learning rate can be raised with the batch size; the paper scales it with the square root of the batch size, with warmup.
- **Same memory as Adam.** No extra state beyond $m$ and $v$.
- **Steps can grow.** The trust ratio can be larger than $1$, so a layer can take a larger step than Adam would, when its weights are large relative to $\lVert u\rVert$.

## Variants and improvements

- **LARS.** The same trust ratio on SGD with momentum; it works for ResNet-50 but performs poorly for BERT according to the paper.
- **Without bias correction.** Appendix E drops the corrections of line L7 without loss of accuracy.
- **NVLAMB.** NVIDIA's implementation first divides the full gradient by its global norm before the moments, which helps with mixed precision.
- **Other layerwise methods.** LAMB keeps Adam's full moments; [Adafactor](/adafactor/) reduces their memory instead, and the two ideas are independent.

## When to use it

Use LAMB when you train with batches of many thousands of examples, for example BERT-style pretraining on many accelerators, and AdamW loses accuracy at that batch size. Use [gradient accumulation](/gradient-accumulation/) to reach such batches on fewer devices. At ordinary batch sizes AdamW is simpler and works as well.

## Pitfalls

- **Zero-initialized layers.** With $\phi$ the identity and the paper's formula, a layer with $x = 0$ never moves; implementations use ratio $1$ there.
- **Which parameters form a layer.** Biases, normalization gains and embeddings behave differently; applying the trust ratio to tiny vectors can make their steps erratic. Many implementations exclude them.
- **Warmup is still needed.** The paper uses a learning rate warmup and, for the mixed batch run, a second warmup when the batch size changes.
- **Large $\epsilon$.** With $\epsilon = 10^{-6}$ and tiny second moments, the direction is no longer the sign-like Adam direction; this matters most in mixed precision.

## Implementations

## History

You, Gitman and Ginsburg (2017) proposed the layerwise trust ratio for SGD with momentum (LARS) to train ImageNet models with batches of 32K. LARS did not work well for attention models. You and others (2019, ICLR 2020) applied the trust ratio to Adam's direction with decoupled weight decay, gave convergence results that depend on the average smoothness of the layers, and reduced BERT pretraining from about 3 days to 76 minutes on a TPUv3 pod.

## References
