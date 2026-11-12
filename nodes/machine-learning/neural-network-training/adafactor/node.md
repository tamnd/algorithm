---
tag: 39XP8M
kind: algorithm
slug: adafactor
name: Adafactor
aliases:
- Adafactor optimizer
- factored second moment estimation
area: machine-learning/neural-network-training
level: advanced
summary: An adaptive optimizer that stores the second moment of an n by m weight matrix as row and column sums, O(n + m) memory, with update clipping and relative step sizes.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {n: the rows of a weight matrix, m: the columns of a weight matrix, k: the number of steps, g: the cost of one minibatch gradient}
  time: {worst: O(k (g + n m))}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2018
  people: [Noam Shazeer, Mitchell Stern]
  note: Shazeer and Stern introduced factored second moments, update clipping and relative step sizes to train large transformers with little optimizer memory, at ICML 2018.
prereqs: [adam, rmsprop]
see_also: [adamw, lamb, mixed-precision-training, learning-rate-schedule, gradient-clipping, singular-value-decomposition]
sources:
  - url: https://arxiv.org/abs/1804.04235
    title: Noam Shazeer and Mitchell Stern, Adafactor, adaptive learning rates with sublinear memory cost, ICML 2018, PMLR 80
    locator: Section 3 (factored second moment estimation), Section 4 (no momentum), Section 5 (out of date second moment estimator), Section 6 (update clipping), Section 7 (increasing decay parameter), Section 8 (relative step size), Algorithms 4 and 5
  - url: https://arxiv.org/abs/1412.6980
    title: Diederik P. Kingma and Jimmy Ba, Adam, a method for stochastic optimization, ICLR 2015
    locator: Algorithm 1 (the unfactored method)
  - url: https://arxiv.org/abs/1910.10683
    title: Colin Raffel and others, Exploring the limits of transfer learning with a unified text-to-text transformer, JMLR 2020
    locator: Section 3.1 (the T5 baseline trained with Adafactor)
---

Adafactor is an adaptive optimizer in the family of [Adam](/adam/) and [RMSProp](/rmsprop/) that keeps, for each $n \times m$ weight matrix, only the row sums $R$ and the column sums $C$ of the running average of squared gradients, and divides the gradient by the rank one matrix $\hat{V} = RC/(1^\top R)$. This cuts the optimizer state of a matrix from $nm$ numbers to $n + m$. Shazeer and Stern (2018) built it to train large transformers, where Adam's two extra copies of the weights limit the model size. Three further changes make it stable without momentum: a decay constant that grows with $t$, clipping of the update by its root mean square, and a step size relative to the size of the weights.

## In plain words

Adam keeps, for every weight, an average of its squared gradients, and divides each step by its square root. For a large layer this table is as large as the layer itself.

Adafactor keeps only the sum of each row and the sum of each column of that table. From these two short lists it rebuilds an estimate of the full table: the entry in row $i$ and column $j$ is row sum $i$ times column sum $j$ divided by the total. When the table has this product form, the estimate is exact; otherwise it is the closest table of that form. To keep training stable, it also caps the size of each update and makes the step a fixed fraction of the size of the weights.

## The problem

Train a network whose parameters are mostly large matrices, for example the projection and feed-forward matrices of a transformer, with an adaptive method, when the memory for the optimizer state is the limit. A weight matrix $X \in \mathbb{R}^{n \times m}$ of a layer gets the gradient $G_t$ of the minibatch loss; Adafactor changes the update step of the training loop for that matrix. Vectors such as biases and normalization gains use the unfactored update.

| symbol | meaning |
|---|---|
| $X, G_t$ | a weight matrix and its minibatch gradient, $n \times m$ |
| $G_t^2$ | the entrywise square |
| $R_t \in \mathbb{R}^n, C_t \in \mathbb{R}^m$ | running row sums and column sums of the squared gradients |
| $\hat{\beta}_{2t}$ | the decay constant at step $t$ |
| $\rho_t$ | the relative step size |
| $\operatorname{RMS}(U)$ | $\sqrt{\text{mean of } U_{ij}^2}$ |
| $\epsilon_1, \epsilon_2, d$ | the regularizing constants and the clipping threshold |

## The algorithm

```pseudo id=main
ADAFACTOR(X, T)                                      ▷ one n × m matrix
L1  R ← 0 ∈ ℝⁿ;  C ← 0 ∈ ℝᵐ
L2  for t ← 1 to T do
L3      G ← minibatch gradient at X
L4      α ← max(ε₂, RMS(X)) · ρₜ                         ▷ relative step size
L5      R ← β̂₂ₜ R + (1 − β̂₂ₜ)(G² + ε₁ 1ₙ1ₘᵀ) 1ₘ           ▷ row sums
L6      C ← β̂₂ₜ C + (1 − β̂₂ₜ) 1ₙᵀ(G² + ε₁ 1ₙ1ₘᵀ)          ▷ column sums
L7      V̂ ← R C / (1ₙᵀ R)                                ▷ rank one, never stored in practice
L8      U ← G / √V̂                                       ▷ entrywise
L9      Û ← U / max(1, RMS(U)/d)                           ▷ update clipping
L10     X ← X − α Û
L11 return X
```

This is Algorithm 4 of the paper; the default constants are $\epsilon_1 = 10^{-30}$, $\epsilon_2 = 10^{-3}$, $d = 1$, $\rho_t = \min(10^{-2}, 1/\sqrt{t})$ and $\hat{\beta}_{2t} = 1 - t^{-0.8}$. For a vector, Algorithm 5 replaces lines L5 to L7 by the unfactored average $\hat{V} \leftarrow \hat{\beta}_{2t}\hat{V} + (1 - \hat{\beta}_{2t})(G^2 + \epsilon_1)$. An implementation computes $U_{ij} = G_{ij}\sqrt{(1^\top R)/(R_iC_j)}$ without forming $\hat{V}$. Since $\hat{\beta}_{21} = 0$, the first average is exactly $G_1^2 + \epsilon_1$ and no bias correction is needed. The default has no momentum ($\beta_1 = 0$); a first moment can be added at the cost of $nm$ more numbers.

## Example

Take the squared gradient
$$G^2 = \begin{pmatrix} 1 & 4\\ 9 & 1\end{pmatrix}, \qquad R = \begin{pmatrix} 5\\ 10\end{pmatrix}, \quad C = \begin{pmatrix} 10 & 5\end{pmatrix}, \quad 1^\top R = 15.$$
The factored estimate is
$$\hat{V} = \frac{RC}{15} = \begin{pmatrix} 10/3 & 5/3\\ 20/3 & 10/3\end{pmatrix}.$$
It is not $G^2$, but its row sums are $5, 10$ and its column sums are $10, 5$, as for $G^2$. For the gradient $G = \begin{pmatrix} 1 & -2\\ 3 & -6\end{pmatrix}$, a rank one matrix, $G^2 = \begin{pmatrix} 1 & 4\\ 9 & 36\end{pmatrix}$ gives $R = (5, 45)^\top$, $C = (10, 40)$, $1^\top R = 50$ and $\hat{V} = \begin{pmatrix} 1 & 4\\ 9 & 36\end{pmatrix}$, exactly $G^2$. On step 1, with $\hat{\beta}_{21} = 0$, the update is then $U = G/|G| = \operatorname{sign}(G)$, with $\operatorname{RMS}(U) = 1$, so no clipping, and every entry of $X$ moves by $\alpha = \max(10^{-3}, \operatorname{RMS}(X)) \cdot 10^{-2}$ against the sign of its gradient.

For memory, take a feed-forward matrix of size $1024 \times 4096$. Adam stores $2 \times 4{,}194{,}304$ numbers for its two moments. Adafactor without momentum stores $1024 + 4096 = 5120$.

## Correctness

The proof file shows that the factored estimate is the right compression:

- **Best rank one fit.** Among all matrices $rc^\top$ with positive entries, $\hat{V} = RC/(1^\top R)$ is the unique minimizer of the I-divergence $\sum V\log(V/W) - V + W$ from $V$. The function is convex after the change $r = e^a$, $c = e^b$, and $\hat{V}$ is its stationary point.
- **Row and column sums.** $\hat{V}$ has the same row and column sums as $V$.
- **Exact for rank one.** If $V = uw^\top$, then $\hat{V} = V$.
- **The running averages.** $R_t$ and $C_t$ are the row and column sums of the average that Adam with $\beta_1 = 0$ would keep, so $\hat{V}_t$ is the factored version of that average. With $\hat{\beta}_{21} = 0$ the weights of the average add to $1$, so no bias correction is needed.
- **Clipping.** $\operatorname{RMS}(\hat{U}) = \min(\operatorname{RMS}(U), d)$.

The paper gives no convergence theorem; its support is these facts and experiments with the transformer on WMT 2014 English to German translation.

## Complexity

Each step costs one gradient and $O(nm)$ arithmetic for a matrix, the same order as Adam. The optimizer state is $n + m$ numbers for a matrix and the size of the vector for a vector, against $2nm$ for Adam with momentum. Over $k$ steps the time is $O(k(g + nm))$ for one matrix.

## Properties

- **Sublinear memory.** For a matrix the state is $n + m$, so for large square matrices the optimizer memory is almost zero next to the weights.
- **Scale of the step.** The relative step size makes the step proportional to $\operatorname{RMS}(X)$, so layers with large weights take large steps; $\epsilon_2$ keeps zero-initialized weights moving.
- **Bounded updates.** Clipping bounds $\operatorname{RMS}(\hat{U})$ by $d$, which handles the case where the second moment estimate is out of date: if the gradients grow fast, $\hat{V}$ is too small, and an unclipped $U$ would be too large.
- **Approximate scaling.** When $G_t^2$ is far from rank one, single entries of $\hat{V}$ can be off by a large factor; the scaling is right for rows and columns on average.

## Variants and improvements

- **With momentum.** Adding $\beta_1 > 0$ restores Adam's first moment at the cost of $nm$ numbers; this, with a fixed decay constant, is common in practice.
- **Without factorization.** The vector form for every parameter is Adam with $\beta_1 = 0$ plus clipping and relative steps.
- **Absolute step.** Setting $\alpha_t$ to an ordinary [learning rate schedule](/learning-rate-schedule/) instead of the relative step is common in implementations.
- **Other memory savers.** [LAMB](/lamb/) changes the step per layer but keeps full moments. Storing the moments in 8 bits, or the weights in [mixed precision](/mixed-precision-training/), saves memory in a different way and combines with factorization.

## When to use it

Use Adafactor when the optimizer state of Adam does not fit in memory, for example for large transformers on accelerators with little memory. It is the optimizer of the T5 models (Raffel and others, 2020). When memory is not the limit, [AdamW](/adamw/) with a tuned learning rate is the more common and better studied choice.

## Pitfalls

- **Wrong orientation.** The factorization is per matrix. Factoring a parameter tensor of higher order requires choosing which two dimensions to keep; libraries keep the last two.
- **No momentum with a fixed $\beta_2$.** Without momentum and with $\hat{\beta}_2$ close to $1$ from the start, the paper reports unstable training. In its experiments either the increasing decay or update clipping alone makes training stable, and the default settings use both.
- **Relative step and warmup.** $\rho_t = \min(10^{-2}, 1/\sqrt{t})$ is constant for the first $10^4$ steps; combining it with an external warmup and decay without turning it off gives an unexpected schedule.
- **Small weights.** With relative steps, weights initialized at $0$ move only by $\epsilon_2\rho_t$ per step at first.

## Implementations

## History

Shazeer and Stern (2018) noticed that Adam's state for the large matrices of transformer models takes as much memory as the model. They proposed the factored estimate, the removal of momentum, update clipping, the increasing decay and relative steps, and trained transformers for translation with almost no optimizer memory. The method was used to train T5 and other large language models in Mesh TensorFlow.

## References
