---
tag: 88JWRJ
kind: technique
slug: weight-normalization
name: Weight normalization
aliases:
- WeightNorm
- weight norm reparameterization
area: machine-learning/neural-network-training
level: advanced
summary: "Write each weight vector as w = g v/||v||, a learned length g times a learned direction, and train g and v. The gradient in v is orthogonal to v."
prereqs: [backpropagation, gradient-descent, batch-normalization]
see_also: [batch-normalization, layer-normalization, spectral-normalization, weight-decay, stochastic-gradient-descent]
sources:
  - url: https://arxiv.org/abs/1602.07868
    title: Tim Salimans and Diederik P. Kingma, Weight normalization, a simple reparameterization to accelerate training of deep neural networks, NIPS 2016
    locator: Section 2 (the reparameterization), Section 2.1 (the gradients, the projection form and the growth of the norm of v), Section 3 (data-dependent initialization), Section 4 (mean-only batch normalization)
  - url: https://proceedings.mlr.press/v37/ioffe15.html
    title: Sergey Ioffe and Christian Szegedy, Batch normalization, ICML 2015, PMLR 37
    locator: Section 3.3 (the scale invariance that weight normalization reproduces without batch statistics)
  - url: https://arxiv.org/abs/1706.05350
    title: Twan van Laarhoven, L2 regularization versus batch and weight normalization, arXiv:1706.05350, 2017
    locator: the effect of an L2 penalty on scale-invariant weights (the effective learning rate)
---

Weight normalization (Salimans and Kingma, 2016) rewrites each weight vector $w$ of a neuron as $w = g\, v/\|v\|$, with a scalar $g$ and a vector $v$ of the same size as $w$, and trains $g$ and $v$ instead of $w$. The length of $w$ is then $|g|$, independent of $v$, and its direction is the direction of $v$. The gradient with respect to $v$ is the gradient with respect to $w$, projected onto the complement of $w$ and scaled by $g/\|v\|$; in particular it is orthogonal to $v$, so plain [gradient descent](/gradient-descent/) never shrinks $\|v\|$. The method gives part of the effect of [batch normalization](/batch-normalization/) without batch statistics, at the cost of one norm per neuron.

## In plain words

A weight vector says two things: which direction the neuron looks in, and how strongly it reacts. Weight normalization stores these two things apart. One number holds the strength. A second vector holds the direction, and only its direction is used, never its length. Training then changes the strength and the direction separately. The direction vector gets updates that are always at a right angle to it, so it can only grow longer, which makes later updates of the direction smaller. The method needs only the weights, not the other examples of a batch, so it works the same in training and in use.

## When it applies

- **Architecture.** Dense and convolutional layers of multilayer perceptrons, convolutional networks, recurrent networks, and networks for generative models or reinforcement learning, where the noise of batch statistics hurts. For a convolution, $w$ is the kernel of one output channel.
- **Part of the training loop.** The parameterization of the model, and so the gradients that the optimizer sees. The function computed by the network is unchanged: any $w$ can be written as $g v/\|v\|$.
- **Batch size.** Any. Nothing depends on the other examples.
- **When batch normalization is a poor fit:** small batches, recurrent networks, online learning, or noise-sensitive training.

## The template

Notation: a neuron computes $y = \phi(w \cdot x + b)$ with $w, x \in \mathbb{R}^k$. Weight normalization stores $v \in \mathbb{R}^k$ and $g \in \mathbb{R}$, and a [backpropagation](/backpropagation/) pass first gives $\nabla_w L$ for the current $w$.

```pseudo id=template
WN-STEP(v, g, b, batch, η)
L1  w ← g · v / ||v||                                  ▷ forward: build the weight
L2  compute the loss L on the batch with w and b, and ∇_w L, ∂L/∂b by backpropagation
L3  ∂L/∂g ← (∇_w L · v) / ||v||
L4  ∇_v L ← (g / ||v||) ∇_w L − (g · ∂L/∂g / ||v||²) v
L5  v ← v − η ∇_v L;  g ← g − η ∂L/∂g;  b ← b − η ∂L/∂b   ▷ or any other optimizer
```

**Cost.** For a layer with $k$ inputs and $n$ outputs, lines L1, L3 and L4 take $\Theta(k n)$ arithmetic operations per step, the cost of one pass over the weights. This does not grow with the batch size, while the layer itself costs $\Theta(m k n)$ on a batch of $m$ examples. The memory is one extra scalar $g$ per neuron. An equivalent form computes $t = v \cdot x$ first and scales by $g/\|v\|$ after the matrix product.

### The gradients

**Claim 1.** For a loss $L(w)$ with $w = g v/\|v\|$ and $v \ne 0$,

$$\frac{\partial L}{\partial g} = \frac{\nabla_w L \cdot v}{\|v\|}, \qquad \nabla_v L = \frac{g}{\|v\|} \nabla_w L - \frac{g\, \partial L/\partial g}{\|v\|^2}\, v = \frac{g}{\|v\|} M_w \nabla_w L, \qquad M_w = I - \frac{w w^\top}{\|w\|^2}.$$

*Proof.* $\partial w/\partial g = v/\|v\|$ gives the first formula. For $v$, $\partial (v_i/\|v\|)/\partial v_j = \delta_{ij}/\|v\| - v_i v_j/\|v\|^3$, so $\partial w_i/\partial v_j = \frac{g}{\|v\|}(\delta_{ij} - v_i v_j/\|v\|^2)$. The chain rule gives $\nabla_v L = \frac{g}{\|v\|}\big(\nabla_w L - \frac{(\nabla_w L \cdot v)}{\|v\|^2} v\big)$, which is the second form after substituting $\partial L/\partial g$. Since $w$ is parallel to $v$ (for $g \ne 0$), $v v^\top/\|v\|^2 = w w^\top/\|w\|^2$, which gives the third. $\blacksquare$

**Claim 2 (orthogonality).** $v \cdot \nabla_v L = 0$.

*Proof.* From the second form, $v \cdot \nabla_v L = \frac{g}{\|v\|}(v \cdot \nabla_w L) - \frac{g\, \partial L/\partial g}{\|v\|^2}\|v\|^2 = g\, \partial L/\partial g - g\, \partial L/\partial g = 0$. $\blacksquare$

The reason is that $L$ does not change along the ray $\{c v : c > 0\}$, so its gradient has no component along $v$.

**Claim 3 (the norm of v grows).** A gradient step $v' = v - \eta \nabla_v L$ gives $\|v'\|^2 = \|v\|^2 + \eta^2 \|\nabla_v L\|^2 \ge \|v\|^2$.

*Proof.* Expand $\|v - \eta \nabla_v L\|^2$ and use Claim 2 to drop the cross term. $\blacksquare$

The step on the direction of $w$ has size about $\eta |g| \|\nabla_v L\|/\|v\|$, and $\nabla_v L$ itself carries a factor $1/\|v\|$. So a large gradient makes $\|v\|$ grow, which shrinks the next steps on the direction: Salimans and Kingma call this a built-in stabilization of the effective learning rate (Section 2.1).

### Data-dependent initialization

Salimans and Kingma (Section 3) draw $v$ from a Gaussian with a small standard deviation, such as 0.05, and pass one batch through the layer. With $t = v \cdot x/\|v\|$ and its mean $\mu[t]$ and standard deviation $\sigma[t]$ over the batch, they set $g = 1/\sigma[t]$ and $b = -\mu[t]/\sigma[t]$. Then the pre-activations $g t + b$ have mean 0 and variance 1 on that batch, as with batch normalization at the first step, and the layers are initialized in order from the input.

## Classic examples

**A hand-sized step.** Take $v = (3, 4)$, $g = 2$, so $\|v\| = 5$ and $w = (1.2, 1.6)$. Let $\nabla_w L = (1, 0)$. Then $\partial L/\partial g = 3/5$ and

$$\nabla_v L = \tfrac25 (1, 0) - \tfrac{2 \cdot 3/5}{25}(3, 4) = \big(\tfrac{32}{125}, -\tfrac{24}{125}\big) = (0.256, -0.192).$$

The dot product with $v$ is $0.768 - 0.768 = 0$. A step with $\eta = 1$ gives $v' = (2.744, 4.192)$, with $\|v'\|^2 = 25 + 0.1024 = 25.1024$.

**A logistic unit.** Forty points in $\mathbb{R}^3$ drawn with `random.Random(4)`, labelled by the sign of $(1.5, -2, 0.5) \cdot x$ plus Gaussian noise of standard deviation 0.3, are fit by a weight-normalized logistic unit with $v$ drawn with `random.Random(5)`, the data-dependent initialization and gradient descent with $\eta = 0.5$. The mean logistic loss is 0.771 at the start, 0.360 after 10 steps, 0.237 after 50, 0.187 after 100 and 0.124 after 300.

## Variations

- **Mean-only batch normalization** (Salimans and Kingma, Section 4) adds the subtraction of the batch mean of the pre-activations, without the division by the standard deviation, to weight normalization.
- **Weight standardization** subtracts the mean of $v$ and divides by its standard deviation, usually with a group normalization of the activations.
- **[Spectral normalization](/spectral-normalization/)** divides a whole matrix by its largest singular value instead of each row by its norm.
- **Fixed scale.** Keep $g$ fixed, so that only directions are learned; this is a constraint to the sphere instead of a reparameterization.

## Pitfalls

- **$v$ near 0.** The formulas divide by $\|v\|$. Do not initialize $v$ at 0, and do not apply a weight decay that drives $v$ to 0.
- **[Weight decay](/weight-decay/) on $v$ is not a penalty on $w$.** The function does not depend on $\|v\|$, so decay on $v$ only works against the growth of Claim 3 and changes the effective learning rate (van Laarhoven, 2017). A penalty on the size of $w$ must act on $g$.
- **Claim 3 holds for plain gradient steps.** With momentum or Adam the update is not the current gradient, so it need not be orthogonal to $v$, and $\|v\|$ can shrink.
- **No normalization of the activations.** Unlike batch normalization, the pre-activations of a deep network can still drift during training; the data-dependent initialization fixes them only at the start.
- **Mixing up the per-neuron norm.** The norm is over the inputs of one output neuron (one row of the weight matrix), not over the whole matrix.

## Exercises

1. Derive $\nabla_v L$ for a loss that depends on $v$ only through $u = v/\|v\|$, and show that it is orthogonal to $v$ whatever the loss.
2. Show that the Hessian of $L$ with respect to $v$, at a point with $g = \|v\|$, is $M_w H M_w$ plus a term that vanishes when $\nabla_w L = 0$, where $H$ is the Hessian with respect to $w$.
3. After $T$ gradient steps from $v_0$, show that $\|v_T\|^2 = \|v_0\|^2 + \eta^2 \sum_{t < T} \|\nabla_v L(v_t)\|^2$.
4. Show that the data-dependent initialization gives pre-activations with mean 0 and variance 1 on the batch it uses.

## References
