---
tag: BP8WJH
kind: definition
slug: relu
name: ReLU
aliases:
- rectified linear unit
- rectifier
area: machine-learning/neural-network-training
level: intro
summary: "The activation function relu(x) = max(0, x): derivative 1 for x > 0 and 0 for x < 0, with f'(0) = 0 by convention; networks built from it are piecewise linear."
prereqs: [activation-function]
see_also: [he-initialization, vanishing-gradient-problem, backpropagation, gradient-checking, piecewise-linear-interpolation, subgradient, dropout, batch-normalization]
sources:
  - paper: "Vinod Nair and Geoffrey E. Hinton, Rectified linear units improve restricted Boltzmann machines, Proceedings of the 27th International Conference on Machine Learning (ICML), 2010"
    locator: pp. 807 to 814; Section 2 (noisy rectified linear units as many tied binary units, and the approximation max(0, x))
  - paper: "Xavier Glorot, Antoine Bordes and Yoshua Bengio, Deep sparse rectifier neural networks, Proceedings of the 14th International Conference on Artificial Intelligence and Statistics (AISTATS), PMLR 15, 2011"
    locator: pp. 315 to 323; Section 3 (rectifier units, sparsity, and training deep networks without pretraining)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 6.3.1 (rectified linear units and their generalizations) and Section 6.3 (the derivative at 0)
  - paper: "Guido Montúfar, Razvan Pascanu, Kyunghyun Cho and Yoshua Bengio, On the number of linear regions of deep neural networks, Advances in Neural Information Processing Systems 27 (NIPS 2014), arXiv:1402.1869"
    locator: Section 2 and Section 3 (piecewise linear networks; deep rectifier networks have exponentially many linear regions in depth)
  - paper: doi:10.1109/ICCV.2015.123
    title: "Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun, Delving deep into rectifiers: surpassing human-level performance on ImageNet classification, ICCV 2015"
    locator: pp. 1026 to 1034; Section 2.1 (parametric ReLU) and Section 2.2 (initialization of rectifier networks)
---

The rectified linear unit, ReLU, is the [activation function](/activation-function/) $\mathrm{relu}(x) = \max(0, x)$. It passes positive inputs unchanged and maps negative inputs to 0. Its derivative is 1 for $x > 0$ and 0 for $x < 0$; at $x = 0$ it is not differentiable, and software uses a fixed value, almost always 0. Because it does not saturate for positive inputs and costs one comparison, it is the default hidden activation of deep feedforward and convolutional networks.

## Definition

The function $\mathrm{relu} : \mathbb{R} \to \mathbb{R}$ is

$$\mathrm{relu}(x) = \max(0, x) = \begin{cases} x & x > 0, \\ 0 & x \le 0. \end{cases}$$

Applied to a vector, it acts on each coordinate. A ReLU unit computes $\mathrm{relu}(w^\top a + b)$ from its inputs $a$.

**The derivative and the convention at 0.** For $x \ne 0$, $\mathrm{relu}'(x) = \mathbf{1}[x > 0]$. At $x = 0$ the left derivative is 0 and the right derivative is 1, so the derivative does not exist. The function is convex, and its [subdifferential](/subgradient/) at 0 is the interval $[0, 1]$. A [backpropagation](/backpropagation/) program needs one number, so it fixes $\mathrm{relu}'(0) = s$ for some $s \in [0, 1]$, almost always $s = 0$. The set where this matters has measure zero, but the inputs of a unit can be exactly 0, for example after another ReLU or with zero initial biases. Then the program returns the derivative of the program with that convention, which need not be a subgradient of the loss: $\mathrm{relu}(x) - \mathrm{relu}(-x) = x$ has derivative 1, but the program with $s = 0$ returns 0 at $x = 0$.

**Basic properties.**

- Positive homogeneity: $\mathrm{relu}(cx) = c\, \mathrm{relu}(x)$ for $c \ge 0$. So a network without biases satisfies $F(cx) = cF(x)$, and scaling one layer's weights up by $c > 0$ and the next layer's down by $c$ leaves the function unchanged.
- Identities: $x = \mathrm{relu}(x) - \mathrm{relu}(-x)$, $\lvert x \rvert = \mathrm{relu}(x) + \mathrm{relu}(-x)$, and $\max(a, b) = a + \mathrm{relu}(b - a)$.
- Sparsity: for inputs symmetric around 0, about half of the units output exactly 0.
- No saturation for $x > 0$: the derivative is exactly 1, so active units pass the gradient unchanged, unlike the sigmoid with $\sigma' \le 1/4$.

**Dying ReLU.** A unit is dead on a data set when $w^\top a + b < 0$ for every example. Then its output and its derivative are 0 on every example, so the gradient of its incoming weights and bias is 0, and gradient descent never changes them again: the unit stays dead. A large learning rate step that makes $b$ very negative is a common cause. Dead units waste capacity; a network can lose a large fraction of its units this way.

**Piecewise linear networks.** A network whose activations are ReLU, leaky ReLU or max is a composition of affine maps and these functions, so it is a continuous piecewise linear function. Each pattern of active and inactive units defines a region of the input space on which the network is one affine map. The number of these linear regions measures the expressive power of the network:

- One hidden layer of $n$ ReLU units on $\mathbb{R}^{d}$ has at most $\sum_{j=0}^{d} \binom{n}{j}$ regions, the maximum number of regions of an arrangement of $n$ hyperplanes. On $\mathbb{R}$ this is $n + 1$ pieces.
- Depth multiplies regions. Montúfar, Pascanu, Cho and Bengio (2014) showed that deep rectifier networks can have a number of regions exponential in the depth, far more than shallow networks with the same number of units.

## Examples and non-examples

**Example: the worked values.** $\mathrm{relu}(-1.5) = 0$, $\mathrm{relu}(2.5) = 2.5$; with the convention $s = 0$, $\mathrm{relu}'(-1.5) = 0$, $\mathrm{relu}'(2.5) = 1$ and $\mathrm{relu}'(0) = 0$.

**Example: the tent map and exponential regions.** On $[0, 1]$, the tent map $t(x) = 2\,\mathrm{relu}(x) - 4\,\mathrm{relu}(x - \tfrac12)$ equals $2x$ on $[0, \tfrac12]$ and $2 - 2x$ on $[\tfrac12, 1]$. It uses two ReLU units. Its $L$-fold composition $t \circ \cdots \circ t$ is a sawtooth with $2^L$ linear pieces, computed by a network of depth $L$ with $2L$ units. A network with one hidden layer on $\mathbb{R}$ has at most $n + 1$ pieces with $n$ units, so it needs at least $2^L - 1$ units for the same function.

**Example: a dead unit.** A unit with weights $w = (1, 1)$ and bias $b = -3$ on inputs in $[0, 1]^2$ has $w^\top x + b \le -1 < 0$ everywhere. Its output and its gradient are 0 for every input, so gradient descent never revives it.

**Example: a kink in gradient checking.** At $x = 10^{-7}$, the central difference of ReLU with step $h = 10^{-5}$ is $0.505$, while the derivative is 1. This false alarm of [gradient checking](/gradient-checking/) comes from the kink at 0, not from a bug.

**Non-example: softplus.** $\log(1 + e^x)$ is a smooth approximation of ReLU with derivative $\sigma(x)$, but it is not ReLU: it is positive everywhere and never gives exact zeros.

**Non-example: the step function.** $\mathbf{1}[x > 0]$ is the derivative of ReLU, not ReLU. Its own derivative is 0 almost everywhere, so a network of step units cannot be trained by gradients.

## Related definitions

- **Leaky ReLU**: $\max(\alpha x, x)$ with a small fixed $\alpha$ such as 0.01. Its gradient for $x < 0$ is $\alpha$, not 0, so units cannot die.
- **Parametric ReLU (PReLU)**: leaky ReLU with $\alpha$ learned for each channel (He, Zhang, Ren and Sun 2015).
- **ReLU6**: $\min(\max(0, x), 6)$, bounded for low precision arithmetic.
- **ELU, GELU, SiLU and softplus**: smooth relatives, described on the [activation function](/activation-function/) page.
- **Maxout**: the maximum of several affine functions of the input; ReLU is maxout with the pieces $0$ and $x$.
- **He initialization**: the weight scale $\mathrm{Var}(w) = 2 / n_{\text{in}}$ that keeps the activation variance constant in ReLU networks; see [He initialization](/he-initialization/).
- **History.** Nair and Hinton (2010) used rectified linear units in restricted Boltzmann machines. Glorot, Bordes and Bengio (2011) showed that deep networks of rectifiers train well without unsupervised pretraining and produce sparse representations.

## References
