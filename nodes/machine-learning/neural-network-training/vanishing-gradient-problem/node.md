---
tag: M6EW97
kind: concept
slug: vanishing-gradient-problem
name: Vanishing gradient problem
aliases:
- vanishing gradients
- vanishing gradient
area: machine-learning/neural-network-training
level: intro
summary: "The backpropagated gradient is a product of one Jacobian per layer or time step, so it can shrink exponentially with depth, and early layers or long-range dependencies stop learning."
prereqs: [backpropagation, activation-function]
see_also: [exploding-gradient-problem, backpropagation-through-time, relu, he-initialization, xavier-initialization, batch-normalization, layer-normalization, matrix-norms]
sources:
  - paper: "Sepp Hochreiter, Untersuchungen zu dynamischen neuronalen Netzen, diploma thesis, Institut für Informatik, Technische Universität München, 1991"
    locator: the analysis of the exponential decay of backpropagated error signals in recurrent networks
  - paper: doi:10.1109/72.279181
    title: "Yoshua Bengio, Patrice Simard and Paolo Frasconi, Learning long-term dependencies with gradient descent is difficult, IEEE Transactions on Neural Networks 5(2), 1994"
    locator: pp. 157 to 166 (robust latching of information forces the gradient of long-term terms to vanish)
  - paper: doi:10.1162/neco.1997.9.8.1735
    title: "Sepp Hochreiter and Jürgen Schmidhuber, Long short-term memory, Neural Computation 9(8), 1997"
    locator: pp. 1735 to 1780; Section 3 (the decay of the error flow) and Section 4 (the constant error carousel)
  - paper: "Razvan Pascanu, Tomas Mikolov and Yoshua Bengio, On the difficulty of training recurrent neural networks, Proceedings of the 30th International Conference on Machine Learning (ICML), PMLR 28(3), 2013"
    locator: pp. 1310 to 1318; Section 2.1 (a sufficient condition on the largest singular value for vanishing gradients)
  - paper: doi:10.1109/CVPR.2016.90
    title: "Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun, Deep residual learning for image recognition, CVPR 2016"
    locator: pp. 770 to 778; Section 3 (residual learning with identity shortcuts)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 8.2.5 (long-term dependencies), Section 10.7 (the challenge of long-term dependencies) and Section 10.10 (the LSTM)
---

The vanishing gradient problem is the tendency of the gradient that [backpropagation](/backpropagation/) computes to shrink exponentially as it moves back through many layers, or through many time steps of a recurrent network. The gradient for an early layer is a product of one Jacobian per later layer. If these factors are smaller than 1 in norm, as they are for saturated sigmoid units whose derivative is at most $1/4$, the product goes to zero, and the early layers or the long-range dependencies hardly learn. Hochreiter (1991) and Bengio, Simard and Frasconi (1994) analysed it; LSTM cells and residual connections are the main remedies.

## In plain words

During training, each layer finds out how to change by receiving an error signal from the layer above it. On the way down, every layer multiplies the signal by its weights and by the slope of its activation. If each layer shrinks the signal a little, say by half, then after 20 layers the signal is a millionth of its size. The top layers learn normally, but the bottom layers receive almost nothing and stay near their random start.

A recurrent network has the same problem in time: the signal that links an output to an input many steps earlier passes through one multiplication per step, so the network cannot learn that the early input matters.

## The idea

**A product of Jacobians.** In a feedforward network with $z_l = W_l a_{l-1} + b_l$ and $a_l = f(z_l)$, the backpropagation recursion gives

$$\frac{\partial \ell}{\partial a_k} = J_{k+1}^\top J_{k+2}^\top \cdots J_L^\top \frac{\partial \ell}{\partial a_L}, \qquad J_l = \frac{\partial a_l}{\partial a_{l-1}} = \mathrm{diag}(f'(z_l))\, W_l.$$

In a recurrent network $h_t = f(W h_{t-1} + U x_t + b)$, the term of the gradient that links the loss at step $t$ to the state at step $s < t$ contains $\prod_{u=s+1}^{t} \mathrm{diag}(f'(a_u))\, W$; see [backpropagation through time](/backpropagation-through-time/). The same weight matrix $W$ appears in every factor.

**A bound.** Let $\gamma = \sup \lvert f' \rvert$ and let $\sigma_{\max}(W_l)$ be the largest singular value, the operator 2-norm of [matrix norms](/matrix-norms/). Since $\lVert \mathrm{diag}(d) \rVert_2 = \max_i \lvert d_i \rvert$ and norms are submultiplicative,

$$\Big\lVert \frac{\partial \ell}{\partial a_k} \Big\rVert \le \prod_{l = k+1}^{L} \gamma\, \sigma_{\max}(W_l)\; \Big\lVert \frac{\partial \ell}{\partial a_L} \Big\rVert.$$

So if $\gamma\, \sigma_{\max}(W_l) \le \eta < 1$ for every layer, the gradient at layer $k$ is at most $\eta^{L-k}$ times the gradient at the top: exponential decay. For a recurrent network this is the sufficient condition of Pascanu, Mikolov and Bengio (2013): if $\sigma_{\max}(W) < 1/\gamma$, the long-term terms vanish. The logistic sigmoid has $\gamma = \frac14$, attained only at 0, and tanh has $\gamma = 1$.

**Why it is hard to avoid in recurrent networks.** Bengio, Simard and Frasconi (1994) showed a dilemma. For a recurrent network to store a bit of information robustly against noise, its dynamics must be contracting near the stored state, which means that the Jacobians there have norm below 1. But then the gradient of the long-term terms vanishes, and gradient descent cannot learn to store the information in the first place. Either the storage is fragile, or the gradient vanishes.

**Random Jacobians.** For a typical size, let the factors $J_l$ be independent random $m \times m$ matrices with entries $N(0, s^2/m)$. Then $\lVert J v \rVert^2 / \lVert v \rVert^2$ is $s^2/m$ times a chi-square variable with $m$ degrees of freedom, independent of $v$, so $\log \lVert J_L \cdots J_1 v \rVert$ is a sum of independent terms, and by the law of large numbers

$$\frac{1}{L} \log \frac{\lVert J_L \cdots J_1 v \rVert}{\lVert v \rVert} \to \lambda = \log s + \tfrac12 \big( \psi(\tfrac m2) - \log \tfrac m2 \big),$$

where $\psi$ is the digamma function, from $\mathbb{E} \log \chi^2_m = \psi(m/2) + \log 2$. Since $\psi(x) < \log x$, $\lambda < \log s$. With $s = 1$, the mean square norm is preserved, $\mathbb{E} \lVert Jv \rVert^2 = \lVert v \rVert^2$, but the typical norm still decays, by Jensen's inequality. The decay rate is about $1/(2m)$ per layer, so it matters for narrow layers and for very deep stacks.

## Examples

**A chain of sigmoids.** For the scalar chain $h_i = \sigma(w h_{i-1} + c)$ the derivative $dh_n / dh_0$ is a product of $n$ factors $w \sigma'(\cdot)$, each at most $\lvert w \rvert / 4$ in absolute value. With $w = 1$, $c = 0$, $h_0 = 0$:

| $n$ | $dh_n / dh_0$ | bound $4^{-n}$ |
|---|---|---|
| 1 | 0.25 | 0.25 |
| 5 | $6.76 \times 10^{-4}$ | $9.77 \times 10^{-4}$ |
| 10 | $3.88 \times 10^{-7}$ | $9.54 \times 10^{-7}$ |
| 20 | $1.27 \times 10^{-13}$ | $9.09 \times 10^{-13}$ |

The bound is reached only when every unit sits at $\sigma'(0) = 1/4$ and $\lvert w \rvert = 4$: the chain $h_i = \sigma(4 h_{i-1} - 2)$ with $h_0 = \tfrac12$ has every factor exactly 1. Larger weights usually move units away from 0, into the flat tails of $\sigma$, where the factors are small. They do not rule out growth: the chain $h_i = \sigma(8 h_{i-1} - 4)$ with $h_0 = \tfrac12$ has every factor equal to 2. Such chains need finely tuned weights and biases.

**Random products.** Pushing a unit vector back through 2000 random Jacobians with $s = 1$ (`random.Random(m)`), the mean log growth per factor is:

| width $m$ | predicted $\lambda$ | measured | norm factor after 50 layers, $e^{50 \lambda}$ | scale $s$ with $\lambda = 0$ |
|---|---|---|---|---|
| 4 | −0.1352 | −0.1425 | 0.0012 | 1.1447 |
| 8 | −0.0651 | −0.0660 | 0.0386 | 1.0673 |
| 16 | −0.0319 | −0.0255 | 0.2029 | 1.0324 |
| 64 | −0.0079 | | 0.6753 | 1.0079 |

With $s = 0.5$ and $m = 8$, the predicted rate is $\log 0.5 - 0.0651 = -0.7582$ and the measured rate is $-0.7591$: the norm falls by a factor of about 2.1 per layer.

**A recurrent network.** In the scalar network of the [backpropagation through time](/backpropagation-through-time/) example, with $W = 0.5$ and $\tanh$, the factor $\partial h_3 / \partial h_0 = \prod_{t=1}^{3} 0.5 (1 - h_t^2) = 0.0441$. The factor for the input at step 1 is $\partial h_3 / \partial x_1 = (1 - h_1^2) \prod_{t=2}^{3} 0.5 (1 - h_t^2) = 0.0882$, twice as large, because $x_1$ enters with $U = 1$ and not with $W = 0.5$. After 20 steps the factor for $x_1$ is less than $10^{-6}$.

## Where it is used

The problem shaped most of the design of modern networks. The remedies:

- **LSTM** (Hochreiter and Schmidhuber 1997). The cell state is updated additively, $c_t = f_t \odot c_{t-1} + i_t \odot g_t$, so along the direct path $\partial c_t / \partial c_{t-1} = \mathrm{diag}(f_t)$. In the original LSTM this factor was exactly the identity, the constant error carousel; with the forget gate added later, the network learns to keep $f_t$ near 1 where it must remember. GRU cells use the same idea.
- **Residual connections** (He, Zhang, Ren and Sun 2016). A block computes $a_l = a_{l-1} + F_l(a_{l-1})$, so its Jacobian is $I + \partial F_l / \partial a_{l-1}$. The gradient has an identity path through all layers, and networks with hundreds of layers train.
- **ReLU and its relatives.** [ReLU](/relu/) has derivative exactly 1 for active units, so it does not shrink the signal there, unlike the sigmoid.
- **Initialization.** [Xavier initialization](/xavier-initialization/) and [He initialization](/he-initialization/) choose the weight variance so that the mean square of the signal is about preserved. Xavier initialization is a compromise between the forward and the backward pass, exact for both only when the fan-in equals the fan-out and the units are near linear; He initialization preserves it in one direction through ReLU units; as the random product example shows, this keeps the decay rate near $1/(2m)$ per layer instead of a constant.
- **Normalization.** [Batch normalization](/batch-normalization/) and [layer normalization](/layer-normalization/) keep pre-activations away from the saturated regions.
- **Other remedies.** Layer-wise pretraining (historically), skip connections in time, attention, which links distant steps in one step, and second order methods. [Gradient clipping](/gradient-clipping/) treats the opposite problem, the [exploding gradient problem](/exploding-gradient-problem/), and does nothing for vanishing gradients.

## References
