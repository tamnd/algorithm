---
tag: HGZT7G
kind: technique
slug: xavier-initialization
name: Xavier initialization
aliases:
- Glorot initialization
- normalized initialization
- Glorot uniform initialization
area: machine-learning/neural-network-training
level: intro
summary: "Draw each weight with mean 0 and variance 2/(fan_in + fan_out), so the signal variance stays about the same forward and backward through a tanh or linear network."
prereqs: [variance, backpropagation, linearity-of-expectation]
see_also: [he-initialization, vanishing-gradient-problem, exploding-gradient-problem, activation-function, batch-normalization, layer-normalization]
sources:
  - url: https://proceedings.mlr.press/v9/glorot10a.html
    title: Xavier Glorot and Yoshua Bengio, Understanding the difficulty of training deep feedforward neural networks, AISTATS 2010, PMLR 9, pages 249 to 256
    locator: Section 4.2.1 (equations 8 to 12 for the forward and backward conditions and their compromise, equation 15 for the old heuristic, equation 16 for the normalized initialization)
  - paper: doi:10.1109/ICCV.2015.123
    title: Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun, Delving deep into rectifiers, surpassing human-level performance on ImageNet classification, ICCV 2015
    locator: Section 2.2 (the same analysis redone for rectifiers)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 8.4 (parameter initialization strategies)
  - paper: "Yann LeCun, Léon Bottou, Genevieve B. Orr and Klaus-Robert Müller, Efficient BackProp, in Neural Networks, Tricks of the Trade, LNCS 1524, Springer, 1998"
    locator: Section 4.6 (initializing the weights with standard deviation 1/sqrt(fan_in))
---

Xavier initialization (Glorot and Bengio, 2010) sets the starting weights of a neural network layer with $n_{\mathrm{in}}$ inputs and $n_{\mathrm{out}}$ outputs to independent draws with mean 0 and [variance](/variance/) $2/(n_{\mathrm{in}} + n_{\mathrm{out}})$, often from the uniform distribution on $[-a, a]$ with $a = \sqrt{6/(n_{\mathrm{in}} + n_{\mathrm{out}})}$. The value is a compromise between two conditions: the forward pass keeps the variance of the activations when $n_{\mathrm{in}} \operatorname{Var}(W) = 1$, and [backpropagation](/backpropagation/) keeps the variance of the gradients when $n_{\mathrm{out}} \operatorname{Var}(W) = 1$. The derivation assumes a linear network, or a tanh network near the origin, where $\tanh'(0) = 1$. For ReLU networks the right value is twice the fan-in form, which is [He initialization](/he-initialization/).

## In plain words

A deep network multiplies its input by one weight matrix after another. If each multiplication makes the numbers a little larger on average, they become huge after many layers. If each one makes them a little smaller, they fade to almost nothing. The same happens to the error signal that flows back during training. Then the network learns very slowly or not at all. Xavier initialization picks the size of the random starting weights so that one layer keeps the spread of the numbers about the same, in both directions. The spread depends on how many numbers go into each unit and how many units read from it. The method takes the average of the two needs and picks the weight spread from it.

## When it applies

- **Architecture.** A multilayer perceptron with dense layers $z^{(l)} = W^{(l)} h^{(l-1)} + b^{(l)}$, $h^{(l)} = f(z^{(l)})$, or a convolutional layer, where $n_{\mathrm{in}}$ is the number of input channels times the kernel area and $n_{\mathrm{out}}$ is the number of output channels times the kernel area.
- **Part of the training loop.** Only the starting point $\theta_0$. The optimizer, the loss and the data do not change.
- **Activation.** An [activation function](/activation-function/) that is odd, with $f(0) = 0$ and $f'(0) = 1$, such as tanh, softsign or the identity. For ReLU use [He initialization](/he-initialization/). For the logistic sigmoid, which has $f(0) = 1/2$ and $f'(0) = 1/4$, the assumptions fail.
- **No normalization layer.** [Batch normalization](/batch-normalization/) and [layer normalization](/layer-normalization/) rescale the activations at each layer, so the initial scale of the weights matters much less there.

## The template

Notation: layer $l$ has $n_l$ units, so $W^{(l)}$ is $n_l \times n_{l-1}$, with $n_{\mathrm{in}} = n_{l-1}$ (the fan-in) and $n_{\mathrm{out}} = n_l$ (the fan-out). The biases start at 0.

```pseudo id=template
XAVIER-INIT(n_0, ..., n_L, rng)
L1  for l ← 1 to L do
L2      a ← sqrt(6 / (n_(l−1) + n_l))                ▷ uniform limit; variance a²/3 = 2/(n_(l−1) + n_l)
L3      for each entry (i, j) of W^(l) do
L4          W^(l)[i, j] ← a uniform draw from [−a, a]   ▷ or a Gaussian draw with variance 2/(n_(l−1) + n_l)
L5      b^(l) ← 0
L6  return W^(1), ..., W^(L), b^(1), ..., b^(L)
```

The cost is one random draw per weight, $\sum_l n_l n_{l-1}$ in all, done once before training. The memory is the parameters themselves.

### The derivation

**Assumptions.** (A1) The entries of $W^{(l)}$ are i.i.d. with mean 0 and variance $\sigma_l^2$, and independent of $h^{(l-1)}$. (A2) The entries of $h^{(l-1)}$ have the same second moment $v_{l-1} = \mathbb{E}[(h^{(l-1)}_j)^2]$. (A3) The network is in its linear regime: $f'(z) \approx 1$ and $f(z) \approx z$, as for tanh near 0. The bias is 0.

**Claim 1 (one layer forward).** Under (A1) and (A2), $\mathbb{E}[z^{(l)}_i] = 0$ and $\operatorname{Var}(z^{(l)}_i) = n_{l-1} \sigma_l^2 v_{l-1}$.

*Proof.* $z^{(l)}_i = \sum_{j=1}^{n_{l-1}} W_{ij} h_j$. Each term has mean $\mathbb{E}[W_{ij}] \mathbb{E}[h_j] = 0$ by independence, so $\mathbb{E}[z_i] = 0$ by [linearity of expectation](/linearity-of-expectation/). For $j \ne k$, $\mathbb{E}[W_{ij} h_j W_{ik} h_k] = \mathbb{E}[W_{ij}] \mathbb{E}[W_{ik} h_j h_k] = 0$, because $W_{ij}$ is independent of the rest and has mean 0. So $\mathbb{E}[z_i^2] = \sum_j \mathbb{E}[W_{ij}^2] \mathbb{E}[h_j^2] = n_{l-1} \sigma_l^2 v_{l-1}$. $\blacksquare$

**Claim 2 (one layer backward).** Let $g^{(l)} = \partial L / \partial z^{(l)}$ have entries with second moment $u_l$, independent of $W^{(l)}$. In the linear regime $g^{(l-1)} = (W^{(l)})^\top g^{(l)}$, and $\mathbb{E}[(g^{(l-1)}_j)^2] = n_l \sigma_l^2 u_l$.

The proof is the proof of Claim 1 applied to $W^\top$, which has $n_l$ terms in each sum. Over $L$ layers the factors multiply: $\prod_l n_{l-1}\sigma_l^2$ forward and $\prod_l n_l \sigma_l^2$ backward (Glorot and Bengio, equations 5 and 6). To keep every layer at the same variance, the forward pass needs $n_{l-1} \sigma_l^2 = 1$ and the backward pass needs $n_l \sigma_l^2 = 1$ (their equations 10 and 11). Both hold only when $n_{l-1} = n_l$. The compromise (equation 12) takes the harmonic mean of $1/n_{l-1}$ and $1/n_l$:

$$\sigma_l^2 = \frac{2}{n_{l-1} + n_l}.$$

A uniform law on $[-a, a]$ has variance $a^2/3$, so $a = \sqrt{6/(n_{l-1} + n_l)}$ (equation 16). With equal widths both conditions hold exactly. Then the gradient with respect to the weights, $\partial L/\partial W^{(l)} = g^{(l)} (h^{(l-1)})^\top$, also has the same variance at each layer, since $v_{l-1} u_l$ does not depend on $l$.

The earlier heuristic $W_{ij} \sim U[-1/\sqrt{n}, 1/\sqrt{n}]$ gives $n \operatorname{Var}(W) = 1/3$ (equation 15). Then the backward variance of a linear network shrinks by a factor 3 in each layer.

## Classic examples

**A dense layer.** For $n_{\mathrm{in}} = 784$ and $n_{\mathrm{out}} = 256$, $\operatorname{Var}(W) = 2/1040 = 1/520 \approx 0.001923$ and $a = \sqrt{6/1040} \approx 0.07596$.

**A deep linear network.** Take 10 layers of width 64, input $x \sim N(0, I)$, Gaussian weights and 40 inputs, drawn with `random.Random(1)`. The table gives the mean square of $z^{(l)}$ at every second layer for three weight variances.

| layer $l$ | 0 | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| Xavier, $\sigma^2 = 1/64$ | 0.993 | 1.011 | 1.173 | 1.207 | 1.192 | 1.190 |
| twice Xavier | 0.993 | 4.04 | 18.8 | 77.2 | 305 | 1218 |
| half Xavier | 0.993 | 0.253 | 0.0733 | 0.0189 | 0.0047 | 0.0012 |

With Xavier the variance stays near 1. With twice the variance it grows by about 2 per layer ($2^{10} = 1024$), and with half it shrinks by about 2 per layer. The backward pass of a Xavier network, seeded with `random.Random(2)`, keeps the mean square of the gradients between 0.89 and 1.07 over the 10 layers.

**Where the assumption breaks.** The same Xavier network with ReLU after each layer (seed 3) has mean square 1.04, 0.253, 0.0513, 0.0071, 0.0023 and 0.00024 at layers 0, 2, 4, 6, 8, 10: it loses a factor of about 2 per layer, because ReLU zeroes half of its input. [He initialization](/he-initialization/) fixes this. With tanh (seed 1), the mean square is 0.993, 0.238, 0.145, 0.094, 0.072 and 0.056: tanh shrinks large inputs, so the variance falls slowly once the units leave the linear regime. Glorot and Bengio report that the normalized initialization still trains deep tanh networks better than the old heuristic.

## Variations

- **Gaussian form.** $W_{ij} \sim N(0, 2/(n_{\mathrm{in}} + n_{\mathrm{out}}))$. Only the variance enters the derivation.
- **Fan-in only (LeCun initialization).** $\operatorname{Var}(W) = 1/n_{\mathrm{in}}$ keeps the forward pass exactly and ignores the backward pass. LeCun, Bottou, Orr and Müller recommended it for sigmoid-like units with normalized inputs.
- **Fan-out only.** $\operatorname{Var}(W) = 1/n_{\mathrm{out}}$ keeps the backward pass exactly.
- **A gain.** Libraries multiply the standard deviation by a gain that depends on the activation, for example $\sqrt 2$ for ReLU, which turns the fan-in form into [He initialization](/he-initialization/).
- **Orthogonal initialization.** Draw $W$ as a random orthogonal matrix times a scale. All singular values are equal, so a linear layer keeps the norm of every vector, not only the average.

## Pitfalls

- **The wrong activation.** The factor 2 in the numerator comes from averaging two conditions, not from the activation. It does not correct for ReLU, which needs twice the variance of the fan-in form.
- **The wrong fans for a convolution.** The fan-in is (input channels) times (kernel height) times (kernel width), not the number of input channels.
- **Uniform limit versus standard deviation.** The limit $a = \sqrt{6/(n_{\mathrm{in}} + n_{\mathrm{out}})}$ is $\sqrt 3$ times the standard deviation. Using $a$ as the standard deviation of a Gaussian triples the variance.
- **Variance in expectation only.** The argument fixes the average over the random weights. A single draw of a very deep network can still drift, since the log of the variance does a random walk whose spread grows with the depth divided by the width.
- **Biases and inputs.** The derivation assumes zero biases and centered inputs with equal variance. Standardize the inputs.

## Exercises

1. Show that a uniform law on $[-a, a]$ has variance $a^2/3$, and derive $a$ for the fan-in form $1/n_{\mathrm{in}}$.
2. For widths $n_0 = 100$, $n_1 = 400$, $n_2 = 100$ and Xavier weights, compute the forward factor $n_{l-1}\sigma_l^2$ of each layer and their product. Do the same for the backward factors.
3. Prove that if $\operatorname{Var}(W^{(l)}) = 2/(n_{l-1} + n_l)$ for all $l$ and $n_0 = n_L$, the product of the forward factors is at most 1. (Hint: each factor is $2r/(1 + r)$ with $r = n_{l-1}/n_l$; compare it with $\sqrt r$.)
4. Repeat Claim 1 for $h = \tanh(z)$ with $z \sim N(0, q)$ and show that $\mathbb{E}[h^2] < q$ for every $q > 0$.

## References
