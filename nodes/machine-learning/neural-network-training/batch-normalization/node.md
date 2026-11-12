---
tag: 3YR4QN
kind: technique
slug: batch-normalization
name: Batch normalization
aliases:
- batchnorm
- BatchNorm layer
- batch norm
area: machine-learning/neural-network-training
level: core
summary: "Normalize each feature of a layer with the mean and variance of the current mini-batch, then apply a learned scale and shift. Inference uses running averages of the statistics."
prereqs: [backpropagation, stochastic-gradient-descent, variance]
see_also: [layer-normalization, weight-normalization, spectral-normalization, he-initialization, xavier-initialization, dropout, weight-decay, whitening]
sources:
  - url: https://proceedings.mlr.press/v37/ioffe15.html
    title: Sergey Ioffe and Christian Szegedy, Batch normalization, accelerating deep network training by reducing internal covariate shift, ICML 2015, PMLR 37, pages 448 to 456 (arXiv:1502.03167)
    locator: Section 3 and Algorithm 1 (the transform and its backward pass), Section 3.1 and Algorithm 2 (training and inference), Section 3.2 (convolutional networks), Section 3.3 (higher learning rates and the scale invariance)
  - paper: "Shibani Santurkar, Dimitris Tsipras, Andrew Ilyas and Aleksander Madry, How does batch normalization help optimization?, NeurIPS 2018 (arXiv:1805.11604)"
    locator: Section 2 (batch normalization and internal covariate shift), Section 3 (the smoothing effect on the loss landscape)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 8.7.1 (batch normalization)
  - paper: "Sergey Ioffe, Batch renormalization, towards reducing minibatch dependence in batch-normalized models, NIPS 2017 (arXiv:1702.03275)"
    locator: the small batch problem and the correction terms r and d
---

Batch normalization (Ioffe and Szegedy, 2015) is a layer that normalizes each feature of its input with the mean and the variance of that feature over the current mini-batch, and then applies a learned scale $\gamma$ and shift $\beta$. At inference it uses fixed running averages of the statistics instead, so each example is processed alone. The layer lets deep networks train with larger learning rates and makes them much less sensitive to the scale of the [initial weights](/he-initialization/). The original paper explains this by a reduction of "internal covariate shift"; later work disputes that explanation and points to a smoother loss landscape instead (Santurkar, Tsipras, Ilyas and Madry, 2018).

## In plain words

Inside a network, each unit produces one number per example. During training these numbers can drift to very large or very small values, and then the next layer learns badly. Batch normalization takes the numbers that one unit produces for a small group of examples, subtracts their average and divides by their spread. Now the numbers have average zero and spread one. Two learned numbers per unit then stretch and move them, so the network can still choose any average and spread it needs. At test time there is no group of examples, so the layer uses averages that it saved during training.

## When it applies

- **Architecture.** Multilayer perceptrons and, above all, convolutional networks. The layer usually sits between a linear or convolutional layer and the nonlinearity: $h = f(\mathrm{BN}(W u))$. The bias of $W u$ is dropped, because $\beta$ takes its role.
- **Part of the training loop.** It changes the model function (a new layer with its own forward and backward pass) and couples the examples of one mini-batch. It does not change the optimizer.
- **Batch size.** It needs mini-batches large enough for stable statistics; with a few examples per batch, use [layer normalization](/layer-normalization/) or a group variant.
- **Not for** recurrent networks over time steps or for transformers, where the statistics would mix positions and sequence lengths. [Layer normalization](/layer-normalization/) is the usual choice there.

## The template

Notation: a mini-batch $B$ of $m$ examples; the layer input $x \in \mathbb{R}^{m \times d}$, with $d$ features; $\epsilon > 0$ a small constant, often $10^{-5}$; $\gamma, \beta \in \mathbb{R}^d$ learned. For a convolutional layer, each channel is one feature and its statistics run over the $m$ examples and all spatial positions.

```pseudo id=template
BN-TRAIN(x[1..m, 1..d], γ, β, ε, μ_run, v_run, a)   ▷ a: the momentum of the running averages
L1  for j ← 1 to d do
L2      μ_j ← (1/m) Σ_i x[i, j]
L3      σ²_j ← (1/m) Σ_i (x[i, j] − μ_j)²              ▷ biased variance in the forward pass
L4      for i ← 1 to m do
L5          x̂[i, j] ← (x[i, j] − μ_j) / sqrt(σ²_j + ε)
L6          y[i, j] ← γ_j x̂[i, j] + β_j
L7      μ_run_j ← (1 − a) μ_run_j + a μ_j
L8      v_run_j ← (1 − a) v_run_j + a · m/(m − 1) · σ²_j  ▷ unbiased estimate for inference
L9  return y, and keep x̂ and σ² for the backward pass

BN-INFER(x, γ, β, ε, μ_run, v_run)
L10 return γ (x − μ_run) / sqrt(v_run + ε) + β      ▷ a fixed affine map of each example
```

Ioffe and Szegedy (Algorithm 2) set the inference statistics to the mean of the batch means and $m/(m-1)$ times the mean of the batch variances over many training batches. Lines L7 and L8 are the exponential moving average that libraries use instead. At inference the layer is $y = a \odot x + c$ with $a_j = \gamma_j/\sqrt{v_j + \epsilon}$ and $c_j = \beta_j - a_j \mu_j$, so it can be folded into the weights of the previous linear layer.

**Cost.** The forward and the backward pass each take $\Theta(m d)$ arithmetic operations per layer, less than the $\Theta(m d\, d_{\mathrm{in}})$ of the matrix product before it. The layer adds $2d$ parameters and $2d$ running statistics, and keeps $\hat x$ ($m d$ numbers) for the backward pass.

### The output statistics

**Claim 1.** In training mode, for each feature $j$, $\frac1m \sum_i \hat x_{ij} = 0$ and $\frac1m \sum_i \hat x_{ij}^2 = \sigma_j^2/(\sigma_j^2 + \epsilon)$. So $y_{\cdot j}$ has mean $\beta_j$ and variance $\gamma_j^2 \sigma_j^2/(\sigma_j^2 + \epsilon)$.

*Proof.* $\sum_i (x_{ij} - \mu_j) = 0$ by the definition of $\mu_j$, and $\sum_i (x_{ij} - \mu_j)^2 = m\sigma_j^2$ by the definition of $\sigma_j^2$. Divide by $\sqrt{\sigma_j^2 + \epsilon}$ and by its square. The affine map $y = \gamma \hat x + \beta$ moves the mean to $\beta$ and multiplies the variance by $\gamma^2$. $\blacksquare$

The variance is 1 up to the factor $\sigma^2/(\sigma^2 + \epsilon)$, which is $1 - O(\epsilon/\sigma^2)$.

**Claim 2 (scale invariance).** With $\epsilon = 0$, $\mathrm{BN}(a x + b) = \mathrm{BN}(x)$ for all $a > 0$ and $b \in \mathbb{R}$, applied per feature. In particular $\mathrm{BN}((aW)u) = \mathrm{BN}(Wu)$, and the gradient with respect to $aW$ is $1/a$ times the gradient with respect to $W$ (Ioffe and Szegedy, Section 3.3).

*Proof.* The mean of $a x + b$ is $a\mu + b$ and its standard deviation is $a\sigma$, so $\hat x$ does not change. The output is constant along the ray $\{aW : a > 0\}$, so the chain rule gives the gradient claim. $\blacksquare$

So a layer whose weights grow gets smaller gradients, which damps the growth, and the scale of the initialization matters little.

### The backward pass

Fix one feature and drop the index $j$. Let $s = \sqrt{\sigma^2 + \epsilon}$ and $\delta_i = \partial L/\partial y_i$ for the loss $L$.

**Claim 3.**
$$\frac{\partial L}{\partial \beta} = \sum_{i=1}^{m} \delta_i, \qquad \frac{\partial L}{\partial \gamma} = \sum_{i=1}^{m} \delta_i \hat x_i, \qquad \frac{\partial L}{\partial x_k} = \frac{\gamma}{m s}\Big(m\,\delta_k - \sum_{i} \delta_i - \hat x_k \sum_i \delta_i \hat x_i\Big).$$

*Proof.* The first two follow from $y_i = \gamma \hat x_i + \beta$. For the third, $\partial \mu/\partial x_k = 1/m$. Next, $\sigma^2 = \frac1m \sum_i (x_i - \mu)^2$ gives $\partial \sigma^2/\partial x_k = \frac2m (x_k - \mu) - \frac{2}{m^2} \sum_i (x_i - \mu)$, and the second term is 0 because $\sum_i (x_i - \mu) = 0$. So $\partial s/\partial x_k = \frac{1}{2s} \cdot \frac2m (x_k - \mu) = \hat x_k/m$. Then

$$\frac{\partial \hat x_i}{\partial x_k} = \frac{\mathbf{1}[i = k] - 1/m}{s} - \frac{x_i - \mu}{s^2} \cdot \frac{\hat x_k}{m} = \frac1s\Big(\mathbf{1}[i = k] - \frac1m - \frac{\hat x_i \hat x_k}{m}\Big).$$

With $\partial L/\partial \hat x_i = \gamma \delta_i$, the chain rule $\partial L/\partial x_k = \sum_i \gamma \delta_i\, \partial \hat x_i/\partial x_k$ gives the formula. $\blacksquare$

The formula shows that the input gradient sums to 0 over the batch, and with $\epsilon = 0$ it is also orthogonal to $\hat x$: the layer removes the parts of the gradient that would only shift or scale the feature. It also shows that the gradient of each example depends on the whole batch.

## Classic examples

**A worked batch.** Take $m = 4$, $d = 2$, $\gamma = 1$, $\beta = 0$, $\epsilon = 10^{-5}$, and the batch with rows $(1, 0)$, $(2, 4)$, $(3, 4)$, $(6, 8)$. Feature 1 has $\mu = 3$ and $\sigma^2 = (4 + 1 + 0 + 9)/4 = 3.5$, so $\hat x = (-1.069, -0.5345, 0, 1.6036)$. Feature 2 has $\mu = 4$ and $\sigma^2 = 8$, so $\hat x = (-1.4142, 0, 0, 1.4142)$. The per feature variances of $\hat x$ are 0.9999971 and 0.9999988, the factor of Claim 1. For the upstream gradient $\delta = (1, 0, 0, 0)$ on feature 1, $\partial L/\partial \gamma = \hat x_1 = -1.069$, $\partial L/\partial \beta = 1$, and Claim 3 gives $\partial L/\partial x = (0.2482, -0.2100, -0.1336, 0.0954)$, which sums to 0. A change of example 3, whose own $\delta$ is 0, still changes the loss, through $\mu$ and $\sigma^2$.

**Why "internal covariate shift" is disputed.** Ioffe and Szegedy argued that the layer helps because it stops the input distribution of each layer from moving while the earlier layers train. Santurkar et al. (2018) added random noise with a changing mean and variance after each batch normalization layer, so the distributions moved more than without the layer, and the networks still trained about as fast as with plain batch normalization. They also found that batch normalization does not always reduce a measure of the shift. Their explanation is that the layer makes the loss and its gradient change more slowly with the parameters (a smaller Lipschitz constant and a smaller smoothness constant along the training path), which allows larger steps. They prove bounds of this kind for the effect of one batch normalization layer, under their assumptions. No general theorem says that batch normalization speeds up training of a deep network.

**A regularizing side effect.** Each example sees statistics computed with other random examples, which adds noise to its activations. Ioffe and Szegedy report that with batch normalization [dropout](/dropout/) can often be removed.

## Variations

- **[Layer normalization](/layer-normalization/)** takes the statistics over the features of one example, so it does not depend on the batch and is the same at training and test time.
- **Group and instance normalization** take the statistics over groups of channels, or over one channel, of one example.
- **Batch renormalization** (Ioffe, 2017) corrects the batch statistics toward the running averages with two clipped factors $r$ and $d$, which reduces the gap between training and inference for small or non-i.i.d. batches.
- **Ghost batch normalization** computes the statistics on small virtual batches inside a large one.
- **Synchronized batch normalization** computes the statistics over the batches of all devices in data parallel training.
- **[Weight normalization](/weight-normalization/)** gets part of the effect, the scale invariance, from a reparameterization of the weights, with no batch statistics.

## Pitfalls

- **Forgetting the mode switch.** In training mode the output depends on the batch. An evaluation run in training mode gives different and noisy results, and it also changes the running averages.
- **Small batches.** With $m = 1$ every $\hat x$ is 0. With a few examples the statistics are noisy and the inference statistics do not match them.
- **Batches that are not i.i.d.** If a batch holds examples of one class, or the two halves of a pair in contrastive learning, the statistics leak information between examples.
- **Biased versus unbiased variance.** The forward pass uses $1/m$; the inference statistics in Algorithm 2 use $m/(m-1)$. Mixing them up gives a small, systematic shift at test time.
- **Fine-tuning.** The running statistics were set on the old data. On new data either recompute them or freeze them on purpose.
- **[Weight decay](/weight-decay/) on scale-invariant weights.** By Claim 2 the decay does not change the function; it shrinks $\|W\|$ and so raises the effective learning rate.

## Exercises

1. Derive $\partial L/\partial x_k$ for $\epsilon = 0$ in vector form, $\nabla_x L = \frac{\gamma}{s}\,(I - \frac1m \mathbf{1}\mathbf{1}^\top - \frac1m \hat x \hat x^\top)\,\delta$, and show that the matrix is the orthogonal projection onto the complement of $\mathbf{1}$ and $\hat x$.
2. Show that with $\epsilon > 0$ the input gradient still sums to 0 but is no longer orthogonal to $\hat x$, and compute $\sum_k \hat x_k\, \partial L/\partial x_k$.
3. Fold the inference transform of a batch normalization layer into a preceding layer $z = Wu + b$: give the new $W'$ and $b'$.
4. A convolutional feature map has shape (batch $m$, channels $c$, height $p$, width $q$). How many numbers enter each mean, and how many parameters does the layer have?

## References
