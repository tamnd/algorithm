---
tag: 7N4K94
kind: algorithm
slug: backpropagation
name: Backpropagation
aliases:
- backprop
- error backpropagation
area: machine-learning/neural-network-training
level: intro
summary: "Compute the gradient of a network's loss for all weights in one backward sweep, by the delta recursion delta_l = (W_(l+1)^T delta_(l+1)) * f'(z_l)."
model: real-ram
complexity:
  vars: {P: "the number of weights, the sum of d_l d_(l-1) over the layers", N: "the number of units in the layers 1 to L"}
  time: {worst: Θ(P), best: Θ(P)}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1986
  people: [David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams]
  note: "Rumelhart, Hinton and Williams showed in Nature in 1986 that backpropagation learns useful hidden representations. Linnainmaa (1970) and Werbos (1974) had the method earlier."
prereqs: [automatic-differentiation, activation-function, gradient]
see_also: [backpropagation-through-time, gradient-checking, computational-graph, vanishing-gradient-problem, stochastic-gradient-descent, perceptron, gradient-checkpointing, relu]
sources:
  - paper: doi:10.1038/323533a0
    title: "David E. Rumelhart, Geoffrey E. Hinton and Ronald J. Williams, Learning representations by back-propagating errors, Nature 323, 1986"
    locator: pp. 533 to 536 (the generalized delta rule for layered networks and the hidden units it learns)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 6.5 (6.5.4 back-propagation in a fully connected MLP, 6.5.6 general back-propagation, 6.5.7 the MLP example) and Section 6.6 (historical notes)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 5.3 (error backpropagation; 5.3.1 the delta recursion, 5.3.3 efficiency)
  - paper: doi:10.1007/BF01931367
    title: "Seppo Linnainmaa, Taylor expansion of the accumulated rounding error, BIT 16(2), 1976"
    locator: pp. 146 to 160 (reverse accumulation of derivatives, from his 1970 master's thesis at the University of Helsinki)
  - paper: "Paul J. Werbos, Beyond Regression: New Tools for Prediction and Analysis in the Behavioral Sciences, PhD thesis, Harvard University, 1974"
    locator: the use of reverse derivative accumulation to fit layered models
  - paper: doi:10.1016/j.neunet.2014.09.003
    title: "Jürgen Schmidhuber, Deep learning in neural networks: an overview, Neural Networks 61, 2015"
    locator: pp. 85 to 117; the section on the development of backpropagation (history from the 1960s to 1986)
---

Backpropagation computes the [gradient](/gradient/) of the loss of a multilayer perceptron with respect to all its weights and biases. It runs the network forward and stores each layer's pre-activation $z_l$ and activation $a_l$. Then it runs one backward sweep that carries the error signal $\delta_l = \partial \ell / \partial z_l$ from the output layer to the first layer, by the recursion $\delta_l = (W_{l+1}^\top \delta_{l+1}) \odot f_l'(z_l)$. It is reverse mode [automatic differentiation](/automatic-differentiation/) on the [computational graph](/computational-graph/) of a layered network, and it costs about two forward passes, whatever the number of weights.

## In plain words

A network makes a guess, and the loss says how wrong the guess is. To improve the network, you need to know, for every weight, which way to move it and how much the loss reacts. Testing each weight one at a time would cost one run of the network per weight.

Backpropagation gets all of these numbers in one pass from the back. It first computes how the loss reacts to each output unit. A unit in the layer before the output affects the loss only through the units it feeds, so its share is a weighted sum of their shares, scaled by the slope of its own activation. The method repeats this, layer by layer, to the input. The share of a weight is then the share of the unit it feeds times the value that flows through it.

## The problem

The architecture is a multilayer perceptron with $L \ge 1$ layers and widths $d_0 = d, d_1, \ldots, d_L$. Layer $l$ has a weight matrix $W_l \in \mathbb{R}^{d_l \times d_{l-1}}$, a bias $b_l \in \mathbb{R}^{d_l}$ and an elementwise [activation function](/activation-function/) $f_l$:

$$a_0 = x, \qquad z_l = W_l a_{l-1} + b_l, \qquad a_l = f_l(z_l), \qquad l = 1, \ldots, L.$$

The parameters are $\theta = (W_1, b_1, \ldots, W_L, b_L)$, and $\ell(a_L, y)$ is the loss on one example $(x, y)$. The output is $\partial \ell / \partial W_l$ and $\partial \ell / \partial b_l$ for every $l$, at the current $\theta$. The empirical risk $L(\theta)$ is the mean of $\ell$ over the $n$ training examples, so its gradient is the mean of the per-example gradients. Backpropagation is the gradient step of the training loop; the update itself is done by [gradient descent](/gradient-descent/), [stochastic gradient descent](/stochastic-gradient-descent/) or another optimizer.

## The algorithm

$\odot$ is the elementwise product, and $f_l'(z_l)$ is the vector of the derivatives $f_l'((z_l)_i)$.

```pseudo id=main
BACKPROP(W_1..W_L, b_1..b_L, x, y)          ▷ the gradient of ℓ(a_L, y)
L1  a_0 ← x
L2  for l ← 1 to L do                       ▷ forward pass; keep every z_l and a_l
L3      z_l ← W_l a_{l−1} + b_l
L4      a_l ← f_l(z_l)
L5  δ_L ← ∇_a ℓ(a_L, y) ⊙ f_L'(z_L)          ▷ δ_l = ∂ℓ/∂z_l
L6  for l ← L down to 1 do                  ▷ backward pass
L7      G_l ← δ_l a_{l−1}ᵀ;  g_l ← δ_l       ▷ ∂ℓ/∂W_l and ∂ℓ/∂b_l
L8      if l > 1 then δ_{l−1} ← (W_lᵀ δ_l) ⊙ f_{l−1}'(z_{l−1})
L9  return (G_1, g_1, ..., G_L, g_L)
```

The forward pass (lines L1 to L4) is the normal evaluation of the network, except that it keeps every $z_l$ and $a_l$. Line L5 starts the backward pass at the output. For the squared loss $\ell = \frac12 \lVert a_L - y \rVert^2$ with an identity output, $\delta_L = a_L - y$. For a softmax output with the [cross-entropy loss](/cross-entropy-loss/), the product of the two derivatives also simplifies to $\delta_L = a_L - y$, with $y$ one-hot. Line L7 reads the gradient of layer $l$ from its error signal and its input. Line L8 sends the error signal one layer back: through the transpose of the same weights, then through the slope of the activation. With the indices shifted by one, this is the recursion $\delta_l = (W_{l+1}^\top \delta_{l+1}) \odot f_l'(z_l)$.

## Example

A network with $d_0 = 2$, one hidden layer of two [ReLU](/relu/) units, and one identity output, with $\ell = \frac12 (a_2 - y)^2$:

$$W_1 = \begin{pmatrix} 0.5 & -1 \\ 1 & 0.5 \end{pmatrix}, \quad b_1 = \begin{pmatrix} 0 \\ 0.5 \end{pmatrix}, \quad W_2 = \begin{pmatrix} 1 & -2 \end{pmatrix}, \quad b_2 = 0.5, \quad x = \begin{pmatrix} 1 \\ 2 \end{pmatrix}, \quad y = 1.$$

| step | line | value |
|---|---|---|
| forward, layer 1 | L3, L4 | $z_1 = (-1.5, 2.5)$, $a_1 = (0, 2.5)$ |
| forward, layer 2 | L3, L4 | $z_2 = 0 - 5 + 0.5 = -4.5$, $a_2 = -4.5$, $\ell = \frac12 \cdot 5.5^2 = 15.125$ |
| output error | L5 | $\delta_2 = a_2 - y = -5.5$ |
| layer 2 gradient | L7 | $G_2 = \delta_2 a_1^\top = (0, -13.75)$, $g_2 = -5.5$ |
| send back | L8 | $W_2^\top \delta_2 = (-5.5, 11)$, $f_1'(z_1) = (0, 1)$, $\delta_1 = (0, 11)$ |
| layer 1 gradient | L7 | $G_1 = \delta_1 x^\top = \begin{pmatrix} 0 & 0 \\ 11 & 22 \end{pmatrix}$, $g_1 = (0, 11)$ |

The first hidden unit has $z = -1.5 < 0$, so its slope is 0 and the gradient of its incoming weights is 0 on this example. Each of the 8 gradient entries agrees with a central difference of $\ell$ with step $10^{-6}$.

A run of training: the XOR data $\{(0,0) \mapsto 0, (0,1) \mapsto 1, (1,0) \mapsto 1, (1,1) \mapsto 0\}$, a 2-4-1 network with $\tanh$ hidden units and an identity output, weights uniform in $[-2/\sqrt{d_{l-1}}, 2/\sqrt{d_{l-1}}]$ from `random.Random(0)`, biases 0, full batch gradient descent with $\eta = 0.2$ on the mean squared loss. The mean loss is 0.3774 at the start, 0.0545 after 100 steps, 0.0061 after 200 steps, $1.4 \times 10^{-7}$ after 500 steps and below $10^{-10}$ after 1000 steps. This is one observed run, not a guarantee: training a network has no general convergence proof, and other seeds or step sizes can stop at a worse point.

## Correctness

Assume that $\ell$ is differentiable at $a_L$ and each $f_l$ is differentiable at each coordinate of $z_l$. The invariant of the backward loop is: at the start of round $l$, $\delta = \partial \ell / \partial z_l$. It holds for $l = L$ by the chain rule through the elementwise $f_L$ (line L5). If it holds for $l$, then, because $z_{l-1}$ affects the loss only through $a_{l-1}$ and then $z_l = W_l a_{l-1} + b_l$, the chain rule gives $\partial \ell / \partial z_{l-1} = (W_l^\top \delta_l) \odot f_{l-1}'(z_{l-1})$, which is line L8. Since $(z_l)_i$ depends on $(W_l)_{ij}$ with coefficient $(a_{l-1})_j$ and on $(b_l)_i$ with coefficient 1, line L7 gives the exact partial derivatives. The full proof is in the proof file below.

At a kink of an activation, such as ReLU at 0, the algorithm returns the derivative of the program with the chosen value of $f'$ there. This is not always a gradient or a subgradient of the loss.

## Complexity

Count multiply-adds on a [real RAM](/real-ram/). Let $P = \sum_{l=1}^{L} d_l d_{l-1}$ be the number of weights and $N = \sum_{l=1}^{L} d_l$ the number of units. Assume that $f_l$, $f_l'$ and $\nabla_a \ell$ cost $O(1)$ per unit.

- **Forward pass.** Line L3 costs $d_l d_{l-1}$ multiply-adds, and line L4 costs $O(d_l)$. In total $P + O(N)$.
- **Backward pass.** Line L7 costs $d_l d_{l-1}$ multiplications for $G_l$. Line L8 costs $d_l d_{l-1}$ multiply-adds for $W_l^\top \delta_l$, for $l \ge 2$ only. In total at most $2P + O(N)$.
- **Total.** At most $3P + O(N)$ operations per example, $\Theta(P)$ in the best and the worst case, since each unit has at least one incoming weight, so $N \le P$. A minibatch of $B$ examples costs $\Theta(BP)$. The backward pass costs about twice the forward pass, which is the cheap gradient principle of reverse mode for this program.
- **Memory.** The forward pass keeps $z_l$ and $a_l$ for every layer: $\Theta(N + d_0)$ numbers per example, or $\Theta(B N)$ for a batch, beyond the $\Theta(P)$ for the weights and the gradient. For wide batches and deep networks this term dominates. [Gradient checkpointing](/gradient-checkpointing/) reduces it to about $\sqrt{L}$ layers at the cost of one more forward pass.

Computing the gradient with [finite differences](/finite-differences/) instead costs $P + 1$ or $2P$ forward passes, $\Theta(P^2)$ operations.

## Properties

- **Exact up to rounding.** The result is the exact gradient of the computed function, not an estimate, at points where all activations are differentiable.
- **Local.** Each unit needs only its own $z$, the error signals of the units it feeds and the weights between them. This is why the same rule fits any layered or acyclic architecture.
- **Reuse of the weights.** The backward pass multiplies by $W_l^\top$, the same matrices as the forward pass. Biological plausibility arguments against backpropagation start from this weight transport.
- **Products of Jacobians.** $\delta_1$ is a product of $L - 1$ factors $\mathrm{diag}(f'_l(z_l)) W_{l+1}^\top$ applied to $\delta_L$. Its size can shrink or grow exponentially in $L$: the [vanishing gradient problem](/vanishing-gradient-problem/) and the [exploding gradient problem](/exploding-gradient-problem/).

## Variants and improvements

- **Matrix form for a batch.** Put the $B$ examples in the columns of $A_{l-1}$, $Z_l$ and $\Delta_l$. Then $\partial L / \partial W_l = \frac{1}{B} \Delta_l A_{l-1}^\top$ and $\Delta_{l-1} = (W_l^\top \Delta_l) \odot f'_{l-1}(Z_{l-1})$, a sequence of matrix products that hardware runs fast.
- **General graphs.** For convolutional, residual and attention layers, each layer type gives its own vector Jacobian product, and the sweep runs over the [computational graph](/computational-graph/) in reverse topological order.
- **Recurrent networks.** [Backpropagation through time](/backpropagation-through-time/) unfolds the network over the sequence and runs the same sweep.
- **Lower memory.** [Gradient checkpointing](/gradient-checkpointing/) and reversible layers recompute activations instead of storing them.
- **Second order information.** A forward pass over the backward pass gives Hessian vector products (Pearlmutter 1994), as described on the [automatic differentiation](/automatic-differentiation/) page.

## When to use it

Use backpropagation whenever you train a differentiable network with a gradient method: it gives the exact gradient for a constant number of passes. Use [gradient checking](/gradient-checking/) with central differences to test a new layer, not to train. Methods that avoid backpropagation, such as evolution strategies or forward mode with random directions, need many passes per useful gradient and are used only when the model is not differentiable or the backward pass is not available.

## Pitfalls

- **Forgetting the activation slope.** Line L8 must multiply by $f'_{l-1}(z_{l-1})$. Writing $\delta_{l-1} \leftarrow W_l^\top \delta_l$ gives the gradient of a linear network.
- **The slope at the wrong point.** $f'$ must be evaluated at $z_{l-1}$, the pre-activation. For $\tanh$ and the sigmoid it is cheaper to write it with the output, $1 - a^2$ and $a(1 - a)$; mixing the two forms, such as $1 - z^2$, is a common bug.
- **Order of updates.** Line L8 must use $W_l$ before the optimizer changes it. Updating $W_l$ inside the backward loop sends the error back through the new weights.
- **Shapes of the outer product.** $G_l = \delta_l a_{l-1}^\top$ has the shape of $W_l$; $a_{l-1} \delta_l^\top$ is its transpose and fails only when the layer is square.
- **Summing instead of averaging.** The gradient of the mean loss over a batch divides by $B$. A sum changes the effective learning rate with the batch size.
- **Numerical overflow at the output.** Compute softmax with cross-entropy as one primitive with the log-sum-exp form and $\delta_L = a_L - y$; separate primitives can overflow or divide by zero.

## Implementations

## History

Seppo Linnainmaa described the reverse accumulation of derivatives of a program in his 1970 master's thesis at the University of Helsinki, published in BIT in 1976, as a tool for rounding error analysis. Paul Werbos proposed in his 1974 Harvard thesis to train layered models with the same reverse computation. Rumelhart, Hinton and Williams, in their 1986 Nature paper, showed that the method trains networks with hidden units, and that these units learn useful features; this paper made backpropagation the standard training method. Schmidhuber's 2015 survey and Griewank's 2012 article trace the earlier work in control theory and automatic differentiation.

## References
