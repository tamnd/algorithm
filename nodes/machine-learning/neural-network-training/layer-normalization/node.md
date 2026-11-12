---
tag: 0KRVGN
kind: technique
slug: layer-normalization
name: Layer normalization
aliases:
- LayerNorm
- layer norm
area: machine-learning/neural-network-training
level: core
summary: "Normalize the features of one example with their own mean and variance, then apply a learned scale and shift. It needs no batch statistics, so training and inference agree."
prereqs: [batch-normalization, backpropagation]
see_also: [batch-normalization, weight-normalization, spectral-normalization, backpropagation-through-time, he-initialization, gradient-clipping]
sources:
  - url: https://arxiv.org/abs/1607.06450
    title: Jimmy Lei Ba, Jamie Ryan Kiros and Geoffrey E. Hinton, Layer normalization, arXiv:1607.06450, 2016
    locator: Section 3 (the layer statistics), Section 3.1 (layer-normalized recurrent networks), Section 5.1 and Table 1 (invariance under weight and data transformations)
  - url: https://arxiv.org/abs/1910.07467
    title: Biao Zhang and Rico Sennrich, Root mean square layer normalization, NeurIPS 2019
    locator: the definition of RMSNorm, its invariance analysis and partial RMSNorm
  - url: https://arxiv.org/abs/2002.04745
    title: Ruibin Xiong, Yunchang Yang, Di He, Kai Zheng, Shuxin Zheng, Chen Xing, Huishuai Zhang, Yanyan Lan, Liwei Wang and Tie-Yan Liu, On layer normalization in the transformer architecture, ICML 2020
    locator: the Post-LN and Pre-LN placements and the learning rate warm-up
  - url: https://proceedings.mlr.press/v37/ioffe15.html
    title: Sergey Ioffe and Christian Szegedy, Batch normalization, ICML 2015, PMLR 37
    locator: Algorithm 1 (the per feature transform that layer normalization transposes)
---

Layer normalization (Ba, Kiros and Hinton, 2016) normalizes the vector of $H$ summed inputs of one layer, for one example, with the mean and the standard deviation of those $H$ numbers, and then applies a learned gain $\gamma$ and bias $\beta$ per feature. It is [batch normalization](/batch-normalization/) with the statistics taken across the features of one example instead of across the examples of a batch. So it does not depend on the batch size, computes the same function at training and test time, and applies to each time step of a recurrent network. It is the normalization layer of transformers. RMSNorm (Zhang and Sennrich, 2019) is a variant that divides by the root mean square and skips the centering.

## In plain words

A layer of a network turns one example into a list of numbers, one per unit. Layer normalization looks at this one list. It subtracts the average of the list from each number and divides by the spread of the list. Then each number is stretched and moved by two learned values for its unit. Because the method uses only the numbers of the example itself, it gives the same result whether the example comes alone or with many others, and during training or during use. If the whole list gets twice as large, or gets a constant added to it, the output does not change.

## When it applies

- **Architecture.** Transformers (before or after each attention and feed-forward block), recurrent networks (at each time step, with statistics per step), and multilayer perceptrons. It is less common in convolutional networks, where the channels of one example have different roles.
- **Part of the training loop.** It changes the model function: one new layer with its own forward and backward pass. It does not couple the examples of a batch, and it has no running statistics.
- **Batch size.** Any, including 1 and online learning.
- **Sequences.** Inputs of different lengths need no special case, unlike batch normalization over time.

## The template

Notation: the input of the layer for one example is $a \in \mathbb{R}^H$ (often $a = W h + b$); $\gamma, \beta \in \mathbb{R}^H$ are learned; $\epsilon > 0$ is small.

```pseudo id=template
LAYER-NORM(a[1..H], γ, β, ε)
L1  μ ← (1/H) Σ_i a_i
L2  σ² ← (1/H) Σ_i (a_i − μ)²
L3  for i ← 1 to H do
L4      â_i ← (a_i − μ) / sqrt(σ² + ε)
L5      y_i ← γ_i â_i + β_i
L6  return y

RMS-NORM(a[1..H], γ, ε)
L7  r ← sqrt((1/H) Σ_i a_i² + ε)
L8  return (γ_i a_i / r for i = 1 .. H)
```

**Cost.** $\Theta(H)$ arithmetic operations per example for the forward pass and for the backward pass, $2H$ parameters ($H$ for RMSNorm), and no state between examples. RMSNorm saves the mean and one subtraction per feature.

### Invariance

**Claim 1.** With $\epsilon = 0$ and $\sigma > 0$, $\mathrm{LN}(c\, a + t \mathbf{1}) = \mathrm{LN}(a)$ for every $c > 0$ and $t \in \mathbb{R}$, and $\mathrm{LN}(-a) = 2\beta - \mathrm{LN}(a)$.

*Proof.* The mean of $c a + t\mathbf{1}$ is $c\mu + t$ and its standard deviation is $|c|\sigma$. So the centered and scaled vector is $c(a - \mu\mathbf{1})/(|c|\sigma)$, which is $\hat a$ for $c > 0$ and $-\hat a$ for $c < 0$. Then $y = \gamma \odot \hat a + \beta$ gives both claims. $\blacksquare$

Two consequences follow for $a = W h$ (Ba et al., Table 1). Scaling all of $W$ by $c > 0$ does not change the output: this is invariance to weight matrix rescaling. Adding the same vector $\delta$ to every row of $W$ adds $(\delta \cdot h)\mathbf{1}$ to $a$, a shift that the layer removes: this is invariance to re-centering of the weight matrix. Scaling a single input $h$ by $c > 0$ also leaves the output unchanged, which batch normalization does not give. With $\epsilon > 0$ the invariance is approximate, and it fails when $\sigma^2$ is not large compared with $\epsilon$.

**Claim 2.** RMSNorm with $\epsilon = 0$ satisfies $\mathrm{RMS}(c\, a) = \mathrm{RMS}(a)$ for $c > 0$, but in general not $\mathrm{RMS}(a + t\mathbf{1}) = \mathrm{RMS}(a)$.

*Proof.* The root mean square of $c a$ is $|c|$ times that of $a$. For the second part, $a = (1, 2, 3, 6)$ gives $\mathrm{RMS}(a) = (0.2828, 0.5657, 0.8485, 1.6971)$ with $\gamma = \mathbf{1}$, and $a + \mathbf{1}$ gives $(0.4529, 0.6794, 0.9058, 1.5852)$. $\blacksquare$

### The backward pass

Let $\delta = \partial L/\partial y$, $g = \gamma \odot \delta$ and $s = \sqrt{\sigma^2 + \epsilon}$. The same steps as in the proof for [batch normalization](/batch-normalization/), with the sum over the features instead of over the batch, give

$$\frac{\partial L}{\partial a_k} = \frac{1}{H s}\Big(H g_k - \sum_i g_i - \hat a_k \sum_i g_i \hat a_i\Big), \qquad \frac{\partial L}{\partial \gamma_k} = \delta_k \hat a_k, \qquad \frac{\partial L}{\partial \beta_k} = \delta_k.$$

The only change is that $\gamma$ now differs across the summed index, so it moves inside the sums as $g$. For RMSNorm, $\partial r/\partial a_k = a_k/(H r)$, which gives

$$\frac{\partial L}{\partial a_k} = \frac{g_k}{r} - \frac{a_k}{H r^3} \sum_i g_i a_i, \qquad \frac{\partial L}{\partial \gamma_k} = \frac{\delta_k a_k}{r}.$$

## Classic examples

**One example.** For $a = (1, 2, 3, 6)$ with $\gamma = \mathbf{1}$, $\beta = \mathbf{0}$ and $\epsilon = 10^{-5}$: $\mu = 3$, $\sigma^2 = 3.5$, and $\mathrm{LN}(a) = (-1.069, -0.5345, 0, 1.6036)$. The input $10a + 5 = (15, 25, 35, 65)$ gives the same output to 4 decimals. The input $10^{-3} a$ gives $(-0.5443, -0.2722, 0, 0.8165)$, because $\sigma^2 = 3.5 \cdot 10^{-6}$ is now smaller than $\epsilon$. Compare the [batch normalization](/batch-normalization/) example: there the same four numbers were the values of one feature over four examples, and the output was the same, but here they are four features of one example.

**Recurrent networks.** Ba et al. apply the layer to the summed inputs $W_{hh} h_{t-1} + W_{xh} x_t$ at each time step $t$, with one shared $\gamma$ and $\beta$ over time. Batch normalization would need separate statistics for each time step and has none for steps longer than the training sequences.

**Transformers.** Each sublayer is wrapped as $x + \mathrm{Sublayer}(\mathrm{LN}(x))$ (Pre-LN) or $\mathrm{LN}(x + \mathrm{Sublayer}(x))$ (Post-LN). Xiong et al. (2020) show that at initialization the Post-LN form has large gradients near the output, which is why it needs a learning rate warm-up (see [learning rate schedules](/learning-rate-schedule/)); the Pre-LN form trains without it in their experiments.

## Variations

- **RMSNorm** drops the mean and $\beta$. Zhang and Sennrich argue that the re-scaling invariance, not the re-centering, carries most of the benefit, and report the same quality at a lower cost on their tasks. Many large language models use it.
- **Partial RMSNorm** estimates the root mean square from the first $p$ percent of the features.
- **Group normalization and instance normalization** sit between layer and batch normalization: the statistics run over a group of channels, or over one channel, and over the spatial positions of one example.
- **No gain or bias.** Some models drop $\beta$, or both $\gamma$ and $\beta$, from some layers.

## Pitfalls

- **Normalizing over the wrong axis.** In a transformer the axis is the model dimension of one token, not the sequence. Normalizing over the tokens mixes positions and leaks information from the future in a causal model.
- **Small $\epsilon$ in low precision.** In 16-bit floats, $\sigma^2 + \epsilon$ can round to 0 or overflow when squared; compute the statistics in 32 bits.
- **Expecting batch normalization's regularization.** The statistics are not noisy across batches, so the layer gives no such noise.
- **Weight decay on scale-invariant weights.** By Claim 1 the function does not change when $W$ is scaled, so [weight decay](/weight-decay/) on $W$ only changes the effective learning rate. Decay on $\gamma$ does change the function.
- **Features with different roles.** When the $H$ features have very different typical scales, as the channels of a convolutional layer, one mean and one variance for all of them can suppress some features.

## Exercises

1. Derive the backward formula of layer normalization from the one for batch normalization, and say exactly where $\gamma$ enters.
2. Show that the vector $\hat a$ of a layer normalization with $\epsilon = 0$ lies on the sphere of radius $\sqrt H$ in the hyperplane $\sum_i \hat a_i = 0$.
3. Show that RMSNorm with $\epsilon = 0$ equals layer normalization without $\beta$ whenever the input has mean 0.
4. Give an input $a$ and a weight change for which layer normalization is invariant and batch normalization is not, and the other way round.

## References
