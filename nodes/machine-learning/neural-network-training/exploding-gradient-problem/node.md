---
tag: 7ABN4Y
kind: concept
slug: exploding-gradient-problem
name: Exploding gradient problem
aliases:
- exploding gradients
- exploding gradient
area: machine-learning/neural-network-training
level: intro
summary: "The backpropagated gradient can grow exponentially with depth or sequence length when the Jacobians it passes through expand, as when a recurrent weight matrix has spectral radius above 1."
prereqs: [backpropagation, spectral-radius]
see_also: [vanishing-gradient-problem, gradient-clipping, backpropagation-through-time, matrix-norms, power-iteration, spectral-normalization, mixed-precision-training, he-initialization]
sources:
  - paper: "Razvan Pascanu, Tomas Mikolov and Yoshua Bengio, On the difficulty of training recurrent neural networks, Proceedings of the 30th International Conference on Machine Learning (ICML), PMLR 28(3), 2013"
    locator: pp. 1310 to 1318; Section 2.1 (the necessary condition on the largest singular value for exploding gradients), Section 2.2 (the dynamical systems view and cliffs) and Section 3.2 (norm clipping)
  - paper: doi:10.1109/72.279181
    title: "Yoshua Bengio, Patrice Simard and Paolo Frasconi, Learning long-term dependencies with gradient descent is difficult, IEEE Transactions on Neural Networks 5(2), 1994"
    locator: pp. 157 to 166 (expanding dynamics make long-term gradients grow, contracting dynamics make them vanish)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 8.2.4 (cliffs and exploding gradients), Section 10.7 (the challenge of long-term dependencies) and Section 10.11.1 (clipping gradients)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, 2nd edition, Cambridge University Press, 2013
    locator: Section 5.6 (matrix norms and the spectral radius; the limit of the norms of the powers)
---

The exploding gradient problem is the tendency of the gradient that [backpropagation](/backpropagation/) computes to grow exponentially as it moves back through many layers or time steps. The gradient is a product of one Jacobian per step. When these Jacobians expand vectors, as when a recurrent network's weight matrix $W$ has [spectral radius](/spectral-radius/) $\rho(W) > 1$ and its units are not saturated, the product grows like $\rho(W)^t$. Then one gradient step can throw the parameters far away, and training diverges or produces overflow. Pascanu, Mikolov and Bengio (2013) analysed it and proposed [gradient clipping](/gradient-clipping/) as the standard fix.

## In plain words

Backpropagation sends an error signal from the output back to the input, and each layer or time step multiplies it by a matrix. If those matrices tend to stretch the signal, the stretch compounds: a factor of 1.1 per step is a factor of about 14000 after 100 steps. The gradient then becomes huge, the update step jumps far past any good point, and the loss suddenly spikes or becomes "not a number".

The same mechanism causes the [vanishing gradient problem](/vanishing-gradient-problem/) when the matrices shrink the signal. Exploding gradients are rarer in practice but more violent: they do not slow training down, they wreck it in one step.

## The idea

**The product.** In a recurrent network $h_t = f(W h_{t-1} + U x_t + b)$, the derivative of a later state with respect to an earlier one is

$$\frac{\partial h_t}{\partial h_s} = \prod_{u = s+1}^{t} \mathrm{diag}(f'(a_u))\, W,$$

and the [backpropagation through time](/backpropagation-through-time/) gradient is a sum of terms containing these products. Deep feedforward networks have the same product with a different matrix per layer.

**The linear case and the spectral radius.** For a linear recurrence, $f(a) = a$, the product is $W^{t-s}$. By Gelfand's formula, $\lVert W^n \rVert^{1/n} \to \rho(W)$ for every matrix norm, where $\rho(W)$ is the largest absolute value of an eigenvalue. So for a start vector with a component along the leading eigenvector, $\frac1n \log \lVert W^n v \rVert \to \log \rho(W)$:

- if $\rho(W) > 1$, the long-term terms of the gradient grow exponentially;
- if $\rho(W) < 1$, they vanish in the long run.

**A necessary condition with a nonlinearity.** Let $\gamma = \sup \lvert f' \rvert$, which is 1 for tanh and $1/4$ for the sigmoid. Each factor has operator norm at most $\gamma\, \sigma_{\max}(W)$, with $\sigma_{\max}$ the largest singular value. So, as Pascanu, Mikolov and Bengio observe, the long-term terms can explode only if $\sigma_{\max}(W) > 1/\gamma$. This condition is necessary, not sufficient: saturated units have $f'$ near 0 and damp the product.

**Transient growth.** For a non-normal matrix, $\lVert W^n \rVert$ can grow for many steps even when $\rho(W) < 1$. The spectral radius fixes only the long-run rate. The largest singular value bounds the growth per step, and the gap between the two can be large.

**Cliffs.** In a nonlinear network, exploding gradients appear in narrow regions of parameter space or state space, near the boundary between two attractors of the dynamics. There the final state jumps from one attractor to the other as a parameter crosses the boundary, and the loss surface has a near vertical wall, a cliff. Outside the cliff the gradient is small; on it, the gradient is enormous, and a full gradient step overshoots by orders of magnitude.

**Random Jacobians.** For independent random $m \times m$ Jacobians with entries $N(0, s^2/m)$, the log norm grows at the exact mean rate $\lambda = \log s + \frac12(\psi(\frac m2) - \log \frac m2)$, with the digamma function $\psi$. The norm explodes when $\lambda > 0$, which needs $s$ slightly above 1: for $m = 4$, $\lambda(1.1) = -0.040$ but $\lambda(1.2) = +0.047$.

## Examples

**A linear recurrence.** $W = \begin{pmatrix} 1.1 & 1 \\ 0 & 0.5 \end{pmatrix}$ has eigenvalues 1.1 and 0.5, so $\rho(W) = 1.1$ and $\log \rho(W) = 0.0953$. The mean log growth per step of $\lVert W^n v \rVert$ for $v = (0.3, 1)$ is 0.1586 after 10 steps, 0.1016 after 100 steps and 0.0969 after 400 steps, tending to 0.0953. The similar matrix $\begin{pmatrix} 1.3 & -0.2 \\ 0.8 & 0.3 \end{pmatrix} = SWS^{-1}$ with $S = \begin{pmatrix} 1 & 2 \\ 1 & 3 \end{pmatrix}$ gives the same limit, since it has the same eigenvalues. After 100 steps, the gradient term is about $1.1^{100} \approx 13781$ times larger than after one step.

**Transient growth with $\rho < 1$.** $W = \begin{pmatrix} 0.9 & 5 \\ 0 & 0.9 \end{pmatrix}$ has $\rho(W) = 0.9$, and $W^n = \begin{pmatrix} 0.9^n & 5n\,0.9^{n-1} \\ 0 & 0.9^n \end{pmatrix}$. The Frobenius norm is 5.16 for $n = 1$, peaks at 19.38 for $n = 9$, is still 1.43 at $n = 50$, and falls to $1.5 \times 10^{-2}$ at $n = 100$ and $7.8 \times 10^{-7}$ at $n = 200$.

**A cliff.** The scalar network $h_t = \tanh(3 h_{t-1})$ has an unstable fixed point at 0 and two stable ones at $\pm 0.9949$. After $T = 20$ steps:

| $h_0$ | $h_{20}$ | $\partial h_{20} / \partial h_0$ |
|---|---|---|
| 0 | 0 | $3^{20} = 3486784401$ |
| $10^{-6}$ | 0.9949 | $1.1 \times 10^{-5}$ |
| $10^{-3}$ | 0.9949 | $3.2 \times 10^{-18}$ |
| $-10^{-3}$ | −0.9949 | $3.2 \times 10^{-18}$ |

As $h_0$ crosses 0, $h_{20}$ jumps by almost 2 over a width of about $10^{-9}$. The derivative is $3^{20}$ on the cliff and tiny everywhere else.

**Random products.** With 2000 random Jacobians (`random.Random(m)`), the measured and predicted mean log growth rates per factor are 0.6272 and 0.6281 for $m = 8$, $s = 2$; 0.2630 and 0.2703 for $m = 4$, $s = 1.5$; 0.1164 and 0.1172 for $m = 8$, $s = 1.2$.

## Where it is used

The analysis explains the remedies used in practice:

- **[Gradient clipping](/gradient-clipping/).** Rescale the gradient when its norm exceeds a threshold. On a cliff, this keeps the direction and limits the step, so the parameters do not jump away. It is the standard fix for recurrent networks and is common in transformer training.
- **Initialization.** Choose $W$ with $\rho(W)$ and $\sigma_{\max}(W)$ near 1, for example orthogonal matrices or the scaled Gaussian of [He initialization](/he-initialization/), so the products neither grow nor shrink fast at the start.
- **Constraining the weights.** [Spectral normalization](/spectral-normalization/) divides $W$ by an estimate of $\sigma_{\max}(W)$ from [power iteration](/power-iteration/), which bounds every factor by $\gamma$.
- **Shorter paths.** [Truncated BPTT](/backpropagation-through-time/) limits the number of factors; gated cells, normalization layers and residual connections keep the Jacobians near the identity.
- **Smaller or adaptive learning rates.** Adaptive methods normalize steps by running gradient magnitudes, which damps but does not remove spikes.
- **Overflow in low precision.** In [mixed precision training](/mixed-precision-training/), an exploding gradient overflows the float16 range and produces infinities; dynamic loss scaling detects them and skips the step.

## References
