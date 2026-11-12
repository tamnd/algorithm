---
tag: ACVN3F
kind: technique
slug: he-initialization
name: He initialization
aliases:
- Kaiming initialization
- MSRA initialization
- Kaiming normal initialization
area: machine-learning/neural-network-training
level: intro
summary: "Draw each weight of a ReLU layer with mean 0 and variance 2/fan_in. ReLU keeps half of the second moment, and the factor 2 puts it back, so the signal neither grows nor fades."
prereqs: [xavier-initialization, relu, variance]
see_also: [xavier-initialization, activation-function, vanishing-gradient-problem, exploding-gradient-problem, batch-normalization]
sources:
  - paper: doi:10.1109/ICCV.2015.123
    title: Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun, Delving deep into rectifiers, surpassing human-level performance on ImageNet classification, ICCV 2015, pages 1026 to 1034 (arXiv:1502.01852)
    locator: Section 2.2 (initialization of filter weights for rectifiers, the forward and the backward case, the leaky case and the comparison with Xavier initialization)
  - url: https://proceedings.mlr.press/v9/glorot10a.html
    title: Xavier Glorot and Yoshua Bengio, Understanding the difficulty of training deep feedforward neural networks, AISTATS 2010, PMLR 9
    locator: Section 4.2.1 (the variance analysis for the linear regime)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 8.4 (parameter initialization strategies)
---

He initialization (He, Zhang, Ren and Sun, 2015) draws the weights of a layer with $n_{\mathrm{in}}$ inputs that feed a [ReLU](/relu/) network independently with mean 0 and [variance](/variance/) $2/n_{\mathrm{in}}$. The factor 2 comes from one exact fact: for a pre-activation $z$ that is symmetric about 0, $\mathbb{E}[\mathrm{relu}(z)^2] = \operatorname{Var}(z)/2$. So a ReLU layer halves the second moment of the signal, and doubling the weight variance of [Xavier initialization](/xavier-initialization/) in its fan-in form puts it back. With this choice a deep ReLU network keeps the scale of its activations and of its gradients at the start of training.

## In plain words

A ReLU unit passes positive numbers and replaces negative numbers with zero. If its input is equally likely to be positive or negative, it throws away half of the signal energy. In a deep network this loss repeats at each layer, so the signal fades fast, and so does the error signal that flows back during training. He initialization makes the random starting weights a little larger, by exactly the amount that the ReLU units lose. The size depends only on how many numbers go into each unit. Then each layer gives out a signal of about the same size as the signal it got, and very deep networks can start to learn.

## When it applies

- **Architecture.** A multilayer perceptron or a convolutional network with ReLU or leaky ReLU units, $z^{(l)} = W^{(l)} h^{(l-1)}$ and $h^{(l)} = \mathrm{relu}(z^{(l)})$. For a convolution, $n_{\mathrm{in}}$ is (input channels) times (kernel area).
- **Part of the training loop.** Only the starting point $\theta_0$.
- **Activation.** A rectifier, positively homogeneous with $f(z) = z$ for $z > 0$ and $f(z) = a z$ for $z \le 0$. For tanh near 0 use [Xavier initialization](/xavier-initialization/).
- **Depth.** It matters most for deep plain networks without normalization layers. With [batch normalization](/batch-normalization/) the layer rescales its input, so the initial scale matters much less.

## The template

Notation: layer $l$ has $n_l$ units and $W^{(l)}$ is $n_l \times n_{l-1}$, with fan-in $n_{l-1}$. The biases start at 0.

```pseudo id=template
HE-INIT(n_0, ..., n_L, a, rng)                       ▷ a: negative slope, 0 for ReLU
L1  for l ← 1 to L do
L2      s² ← 2 / ((1 + a²) · n_(l−1))                 ▷ the forward condition
L3      for each entry (i, j) of W^(l) do
L4          W^(l)[i, j] ← a Gaussian draw with mean 0 and variance s²
L5      b^(l) ← 0
L6  return W^(1), ..., W^(L), b^(1), ..., b^(L)
```

The uniform form draws from $[-\sqrt{3}s, \sqrt{3}s]$, which is $[-\sqrt{6/n_{\mathrm{in}}}, \sqrt{6/n_{\mathrm{in}}}]$ for ReLU. The cost is one random draw per weight, done once.

### The factor one half

**Lemma.** Let $z$ be a random variable with $\mathbb{E}[z^2] < \infty$ that is symmetric about 0, that is, $z$ and $-z$ have the same law. Then $\mathbb{E}[\mathrm{relu}(z)^2] = \frac12 \mathbb{E}[z^2]$. For the leaky rectifier with slope $a$, $\mathbb{E}[f(z)^2] = \frac{1 + a^2}{2} \mathbb{E}[z^2]$.

*Proof.* Write $z^2 = z^2 \mathbf{1}[z > 0] + z^2 \mathbf{1}[z < 0]$, since the term at $z = 0$ is 0. By symmetry the two parts have the same expectation, so each is $\frac12 \mathbb{E}[z^2]$. Then $\mathrm{relu}(z)^2 = z^2 \mathbf{1}[z > 0]$ gives the first claim, and $f(z)^2 = z^2 \mathbf{1}[z > 0] + a^2 z^2 \mathbf{1}[z < 0]$ gives the second. $\blacksquare$

The lemma is about the second moment, not the variance, of $\mathrm{relu}(z)$: the output has a positive mean. Symmetry is needed. For $z$ with $P(z = -1) = 1/2$, $P(z = 2) = P(z = 0) = 1/4$, $\mathbb{E}[z^2] = 3/2$ but $\mathbb{E}[\mathrm{relu}(z)^2] = 1$, not $3/4$.

### The forward condition

**Assumptions.** The entries of $W^{(l)}$ are i.i.d., symmetric about 0, with variance $\sigma_l^2$, and independent of $h^{(l-1)}$. The biases are 0.

**Claim.** $\operatorname{Var}(z^{(l)}_i) = n_{l-1}\sigma_l^2 \cdot \frac12 \operatorname{Var}(z^{(l-1)}_j)$ for $l \ge 2$.

*Proof.* As in Claim 1 of [Xavier initialization](/xavier-initialization/), the cross terms vanish because $W_{ij}$ has mean 0 and is independent of the rest, so $\mathbb{E}[(z^{(l)}_i)^2] = n_{l-1}\sigma_l^2\, \mathbb{E}[(h^{(l-1)}_j)^2]$, and $\mathbb{E}[z^{(l)}_i] = 0$. Here $h^{(l-1)} = \mathrm{relu}(z^{(l-1)})$ does not have mean 0, which is why the second moment, not the variance, of $h$ appears. Next, $z^{(l-1)}_j = \sum_k W^{(l-1)}_{jk} h^{(l-2)}_k$ is symmetric: changing the signs of row $j$ of $W^{(l-1)}$ maps $z^{(l-1)}_j$ to $-z^{(l-1)}_j$ and keeps the joint law. The lemma gives $\mathbb{E}[(h^{(l-1)}_j)^2] = \frac12 \operatorname{Var}(z^{(l-1)}_j)$. $\blacksquare$

So the variance is the same at every layer exactly when $\frac12 n_{l-1}\sigma_l^2 = 1$, that is $\sigma_l^2 = 2/n_{l-1}$. Over $L$ layers the variance is multiplied by $\prod_{l=2}^{L} \frac12 n_{l-1}\sigma_l^2$, so a factor $c$ per layer gives $c^{L-1}$: with Xavier's $1/n$ on equal widths, $c = 1/2$ and the signal shrinks by $2^{L-1}$.

### The backward condition

The gradient obeys $g^{(l-1)} = \mathrm{relu}'(z^{(l-1)}) \odot (W^{(l)})^\top g^{(l)}$. The factor $\mathrm{relu}'(z)$ is 0 or 1, each with probability 1/2 when $z$ is symmetric with $P(z = 0) = 0$. If it is independent of the other factor, the same steps give $\mathbb{E}[(g^{(l-1)}_j)^2] = \frac12 n_l \sigma_l^2\, \mathbb{E}[(g^{(l)}_i)^2]$, so the backward pass is kept when $\sigma_l^2 = 2/n_l$, the fan-out form. He et al. show that either condition is enough: with the forward condition the backward factors multiply to $\prod_l n_l/n_{l-1} = n_L/n_1$, a ratio of two widths that does not grow with depth, and the same holds the other way round.

## Classic examples

**One layer.** A 3 by 3 convolution with 64 input channels has $n_{\mathrm{in}} = 576$, so $\sigma^2 = 2/576 \approx 0.003472$ and $\sigma \approx 0.05893$.

**A 20 layer ReLU network.** Take width 64, $x \sim N(0, I)$, Gaussian weights and 30 inputs, drawn with `random.Random(1)`. The first row of each pair is the mean square of $z^{(l)}$; the backward rows give the mean square of $g^{(l)}$, sent back from $g^{(20)} \sim N(0, I)$.

| layer $l$ | 1 | 5 | 10 | 15 | 20 |
|---|---|---|---|---|---|
| forward, $\sigma^2 = 2/n$ (He) | 1.89 | 1.28 | 1.47 | 1.18 | 0.95 |
| forward, $\sigma^2 = 1/n$ | 0.946 | 0.040 | 0.00144 | $3.6 \cdot 10^{-5}$ | $9.1 \cdot 10^{-7}$ |
| forward, $\sigma^2 = 4/n$ | 3.78 | 41.0 | 1500 | 38800 | 996000 |
| backward, $\sigma^2 = 2/n$ (He) | 1.06 | 1.49 | 1.12 | 1.03 | 1.02 |
| backward, $\sigma^2 = 1/n$ | $2.0 \cdot 10^{-6}$ | $4.5 \cdot 10^{-5}$ | 0.00109 | 0.0323 | 1.02 |

Layer 1 has variance near 2 under He because its input $x$ did not pass through a ReLU; He et al. note that one factor of 2 at the first layer does no harm. After that the He rows stay between 0.9 and 2, while the other scales change by a factor of about 2 per layer, $2^{19} \approx 5 \cdot 10^5$ over the network. He et al. report that a 30 layer plain ReLU network trains from their initialization and stalls from Xavier initialization.

## Variations

- **Fan-in or fan-out mode.** $2/n_{\mathrm{in}}$ keeps the forward pass, $2/n_{\mathrm{out}}$ keeps the backward pass. Libraries call these modes `fan_in` and `fan_out`.
- **Leaky ReLU and PReLU.** Use $2/((1 + a^2) n_{\mathrm{in}})$. For $a = 1$ the unit is linear and this is the fan-in form of Xavier, $1/n_{\mathrm{in}}$.
- **Uniform form.** $U[-\sqrt{6/n_{\mathrm{in}}}, \sqrt{6/n_{\mathrm{in}}}]$ has the same variance.
- **Residual networks.** A residual block adds its output to its input, so the variance grows with the number of blocks even with He weights. Common fixes set the last layer or the last normalization scale of each block to 0, or scale the branch down with depth.

## Pitfalls

- **Using Xavier for ReLU.** The Xavier variance $2/(n_{\mathrm{in}} + n_{\mathrm{out}})$ equals $1/n$ for equal widths, half of what ReLU needs, and the signal halves at each layer.
- **Non-zero biases or a shifted activation.** The lemma needs symmetry about 0. A positive bias at the start, or an activation such as the logistic sigmoid, breaks it.
- **Confusing the second moment with the variance.** $\operatorname{Var}(\mathrm{relu}(z)) = \frac12 \operatorname{Var}(z) - (\mathbb{E}[\mathrm{relu}(z)])^2$ is smaller than half. The forward recursion uses $\mathbb{E}[h^2]$.
- **The wrong fan-in for a convolution.** It is the number of input channels times the kernel area.
- **Expectation, not every draw.** The analysis holds on average over the weights; one draw of a deep and narrow network can drift by a large factor.

## Exercises

1. Let $z \sim N(0, q)$. Compute $\mathbb{E}[\mathrm{relu}(z)]$ and $\operatorname{Var}(\mathrm{relu}(z))$, and check that $\mathbb{E}[\mathrm{relu}(z)^2] = q/2$.
2. Derive the variance for a leaky ReLU with slope $a = 0.01$ and $n_{\mathrm{in}} = 512$.
3. With the forward condition $\sigma_l^2 = 2/n_{l-1}$, compute the product of the backward factors $\frac12 n_l \sigma_l^2$ for widths $n_0, \ldots, n_L$ and show that it equals $n_L/n_1$ when the product starts at $l = 2$.
4. A unit uses $f(z) = \max(z, 0) - c$ for a constant $c > 0$. Which step of the derivation fails?

## References
