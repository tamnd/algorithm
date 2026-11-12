---
tag: CAQ103
kind: algorithm
slug: kronecker-factored-approximate-curvature
name: Kronecker-factored approximate curvature
aliases:
- K-FAC
- KFAC optimizer
area: machine-learning/neural-network-training
level: research
summary: A natural gradient method for neural networks that approximates each layer's Fisher block by a Kronecker product of two small matrices, so the block inverse costs two small inverses.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {L: the number of layers, d: the largest layer width, b: the minibatch size, k: the number of steps}
  time: {worst: O(k L (b d^2 + d^3))}
  space: {extra: Θ(L d^2)}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2015
  people: [James Martens, Roger Grosse]
  note: Martens and Grosse introduced K-FAC for multilayer perceptrons at ICML 2015; later work extended it to convolutional and recurrent layers.
prereqs: [natural-gradient-descent, fisher-information-matrix, kronecker-product, backpropagation]
see_also: [adam, matrix-inversion, cholesky-decomposition, quasi-newton-method, limited-memory-bfgs, sharpness-aware-minimization, softmax-regression, cross-entropy-loss]
sources:
  - url: https://arxiv.org/abs/1503.05671
    title: James Martens and Roger Grosse, Optimizing neural networks with Kronecker-factored approximate curvature, ICML 2015
    locator: Section 3 (the Kronecker factored approximation of a Fisher block), Section 4.2 (block diagonal inverse), Section 4.3 (block tridiagonal inverse), Section 5 (estimating the factors with sampled targets), Section 6.3 (factored Tikhonov damping), Section 6.4 (rescaling by the exact Fisher), Section 6.5 (adjusting lambda), Section 7 (momentum)
  - url: https://arxiv.org/abs/1602.01407
    title: Roger Grosse and James Martens, A Kronecker-factored approximate Fisher matrix for convolution layers, ICML 2016
    locator: the extension to convolution layers (KFC)
  - url: https://arxiv.org/abs/1412.1193
    title: James Martens, New insights and perspectives on the natural gradient method, JMLR 2020
    locator: the relation of the Fisher to the generalized Gauss-Newton matrix, and the empirical Fisher
---

Kronecker-factored approximate curvature (K-FAC) is an approximate [natural gradient](/natural-gradient-descent/) method for neural networks. For each layer with weight matrix $W$, input $\bar{a}$ and backpropagated output gradient $g$, it approximates the layer's block of the [Fisher information matrix](/fisher-information-matrix/), $\mathbb{E}[\bar{a}\bar{a}^\top \otimes gg^\top]$, by the [Kronecker product](/kronecker-product/) $\bar{A} \otimes G$ of $\bar{A} = \mathbb{E}[\bar{a}\bar{a}^\top]$ and $G = \mathbb{E}[gg^\top]$. Because $(\bar{A} \otimes G)^{-1} = \bar{A}^{-1} \otimes G^{-1}$, the preconditioned gradient is $G^{-1}\nabla_W h\,\bar{A}^{-1}$: two inverses of the size of the layer's input and output, instead of one of the size of its weight count. Martens and Grosse (2015) added factored damping, a step length from the exact quadratic model and an adaptive damping rule, and found that K-FAC makes much more progress per step than SGD with momentum on deep autoencoders. It replaces the update step of the training loop and adds a pass that collects the factors.

## In plain words

Plain gradient descent takes the same step size in every direction, even though some directions of the weights change the network's predictions a lot and others hardly at all. Natural gradient fixes this by dividing by a matrix that measures how much the predictions change, the Fisher matrix. For a real network that matrix is far too large to store or invert.

K-FAC handles one layer at a time and makes one simplifying guess: that the inputs to a layer and the error signals at its output are roughly unrelated. Then the layer's huge matrix splits into two small ones, one for the inputs and one for the outputs. Inverting two small matrices is cheap, so the method can take curvature into account at a moderate cost.

## The problem

Train a feedforward network, here a multilayer perceptron with layers $s_l = W_l\bar{a}_{l-1}$, $a_l = \phi(s_l)$, and a probabilistic output $p(y \mid x, \theta)$ such as a softmax with [cross entropy loss](/cross-entropy-loss/). The objective is $h(\theta) = \mathbb{E}[-\log p(y \mid x, \theta)] + \tfrac{\eta}{2}\lVert\theta\rVert^2$. The natural gradient step is $-F^{-1}\nabla h$ with $F = \mathbb{E}_{x}\mathbb{E}_{y \sim p(\cdot \mid x)}[\nabla\log p\,\nabla\log p^\top]$, the Fisher matrix of the model's own predictive distribution. With $n$ parameters, storing $F$ costs $n^2$ and inverting it $n^3$, impossible for $n$ in the millions.

| symbol | meaning |
|---|---|
| $\bar{a}_{l-1}$ | the input of layer $l$ with a $1$ appended, size $d_{l-1} + 1$ |
| $g_l$ | $\partial\log p(y \mid x)/\partial s_l$ for a sampled $y$, size $d_l$ |
| $\bar{A}_{l-1}, G_l$ | running estimates of $\mathbb{E}[\bar{a}\bar{a}^\top]$ and $\mathbb{E}[gg^\top]$ |
| $\lambda$, $\eta$ | the adaptive damping and the $\ell_2$ coefficient |
| $\pi_l$ | the split of the damping between the two factors |
| $\operatorname{vec}$ | stacking of columns, so $\operatorname{vec}(g\bar{a}^\top) = \bar{a} \otimes g$ |

## The algorithm

```pseudo id=main
K-FAC(θ, data, T, λ, η, T₁)
L1  Ā, G ← none
L2  for k ← 1 to T do
L3      draw a minibatch S
L4      ∇h ← minibatch gradient of h at θ, by backpropagation
L5      for each layer l: Āₗ₋₁, Gₗ ← batch means of ā āᵀ and g gᵀ, g backpropagated from y ~ p(·|x)
L6      update the running averages with weight ε = min(1 − 1/k, 0.95)
L7      Δₗ ← −(Gₗ + (γ/πₗ) I)⁻¹ ∇_{Wₗ} h (Āₗ₋₁ + πₗ γ I)⁻¹  for each l, γ = √(λ + η)
L8      α ← −∇hᵀΔ / (Δᵀ F Δ + (λ + η) ‖Δ‖²)              ▷ F Δ by a forward pass, exact Fisher
L9      θ ← θ + α Δ
L10     every T₁ steps: ρ ← (h(θ_new) − h(θ_old)) / M(αΔ); if ρ > 3/4 then λ ← ω₁ λ; if ρ < 1/4 then λ ← λ / ω₁
L11 return θ
```

Line L5 samples the targets from the model's own distribution, as Section 5 of the paper requires; using the training labels would give the empirical Fisher, a different matrix. Line L7 is the block diagonal version (Section 4.2) with the factored Tikhonov damping of Section 6.3, $\pi_l = \sqrt{(\operatorname{tr}\bar{A}_{l-1}/(d_{l-1} + 1))/(\operatorname{tr}G_l/d_l)}$. Line L8 rescales the proposal by the exact quadratic model (Section 6.4), and line L10 is the Levenberg-Marquardt rule of Section 6.5 with $\omega_1 = (19/20)^{T_1}$, $T_1 = 5$; $M$ there is the quadratic model without $\lambda$. The paper also adds momentum by choosing the step lengths of $\Delta$ and the previous step together (Section 7), adapts the factor damping $\gamma$ separately from $\lambda$, recomputes the inverses only every few steps, and offers a block tridiagonal inverse (Section 4.3). The implementation here ties $\gamma = \sqrt{\lambda + \eta}$ and has no momentum.

## Example

Take one layer with input factor and output factor
$$\bar{A} = \begin{pmatrix} 2 & 1\\ 1 & 1\end{pmatrix},\quad G = \begin{pmatrix} 2 & 0\\ 0 & 4\end{pmatrix},\quad \nabla_W h = \begin{pmatrix} 1 & 3\\ 2 & -2\end{pmatrix}.$$
Then $\bar{A}^{-1} = \begin{pmatrix} 1 & -1\\ -1 & 2\end{pmatrix}$, $G^{-1}\nabla_W h = \begin{pmatrix} 0.5 & 1.5\\ 0.5 & -0.5\end{pmatrix}$ and
$$G^{-1}\nabla_W h\,\bar{A}^{-1} = \begin{pmatrix} -1 & 2.5\\ 1 & -1.5\end{pmatrix}.$$
By the identity $(\bar{A} \otimes G)\operatorname{vec}(X) = \operatorname{vec}(GX\bar{A}^\top)$, this is exactly the solution of the $4 \times 4$ system $(\bar{A} \otimes G)\operatorname{vec}(X) = \operatorname{vec}(\nabla_W h)$, found with two $2 \times 2$ inverses. For a layer with $1000$ inputs and $1000$ outputs, the Fisher block has $10^{12}$ entries, while the two factors have $2 \times 10^6$.

On a small run, a tanh network with layers $2, 6, 2$ trained on $80$ points labeled by the sign of $x_1x_2$, with minibatches of $40$, the training loss starts at $0.952$. After $60$ steps, K-FAC with $\lambda = 1$ reaches $0.142$; SGD with the best of the learning rates $0.3$, $1$ and $3$ reaches $0.308$.

## Correctness

The proof file proves the facts the method rests on:

- **Kronecker identities.** $\operatorname{vec}(uv^\top) = v \otimes u$, $(A \otimes G)\operatorname{vec}(X) = \operatorname{vec}(GXA^\top)$, and $(A \otimes G)^{-1} = A^{-1} \otimes G^{-1}$.
- **The form of a Fisher block.** For one input, the layer's Fisher block is exactly $\bar{a}\bar{a}^\top \otimes \mathbb{E}_y[gg^\top]$. Over many inputs, K-FAC replaces the mean of the Kronecker products by the Kronecker product of the means, which is exact when $\bar{a}\bar{a}^\top$ and $gg^\top$ are uncorrelated and an approximation otherwise. For the softmax output, $\mathbb{E}_{y \sim p}[gg^\top] = \operatorname{diag}(p) - pp^\top$.
- **The damped step.** The damped factors are positive definite, line L7 solves the Kronecker system exactly, and the result is a descent direction.
- **The damping split.** $\pi_l$ minimizes the trace of the extra term $\gamma(\pi I \otimes G + \pi^{-1}\bar{A} \otimes I)$ that factored damping adds to $\bar{A} \otimes G + \gamma^2I$.
- **The step length.** Line L8 minimizes the damped quadratic model along $\Delta$, and the predicted decrease is $\tfrac12\alpha\nabla h^\top\Delta < 0$.

The paper does not prove convergence of K-FAC; the quality of the approximation $\mathbb{E}[\bar{a}\bar{a}^\top \otimes gg^\top] \approx \bar{A} \otimes G$ is measured in its experiments.

## Complexity

For a layer with $d_a$ inputs and $d_o$ outputs, collecting the factors over a minibatch of $b$ costs $O(b(d_a^2 + d_o^2))$, and inverting them $O(d_a^3 + d_o^3)$, against $O(d_a^3d_o^3)$ for the exact block. Applying the preconditioner costs two matrix products, $O(d_ad_o(d_a + d_o))$. The extra state is the two factors and their inverses, $O(d_a^2 + d_o^2)$ per layer. The extra forward pass for $F\Delta$ costs about one gradient. Martens and Grosse report that, with the inverses refreshed every few steps, a step costs only several times as much as an SGD step.

## Properties

- **Invariance.** K-FAC is invariant to some reparametrizations of the network, for example affine transformations of each layer's input and output, which SGD is not; this is part of why it needs little tuning across architectures.
- **Approximate natural gradient.** With exact factors and no damping, the block diagonal version computes the natural gradient for the Kronecker-factored Fisher, not the exact one.
- **Random targets.** The factors depend on targets sampled from the model, so the method is randomized even with a fixed data order.
- **Damping is essential.** Without damping, small eigenvalues of the factors give huge steps; the adaptive $\lambda$ and $\gamma$ keep the step inside the region where the quadratic model is trusted.

## Variants and improvements

- **Block tridiagonal.** Section 4.3 models the interactions between adjacent layers and inverts a block tridiagonal approximation, at a higher cost.
- **Convolution layers.** Grosse and Martens (2016) extend the factorization to convolutions by treating spatial positions as extra samples (KFC).
- **Distributed and large scale.** Later work computes the factors and their inverses on separate workers and updates the inverses rarely, which makes K-FAC competitive in wall clock time for large batch training.
- **Related preconditioners.** Shampoo keeps one preconditioner per tensor dimension and uses matrix roots instead of inverses; [Adam](/adam/) keeps only a diagonal. [Quasi-Newton methods](/quasi-newton-method/) such as [L-BFGS](/limited-memory-bfgs/) approximate the Hessian from gradient differences and work poorly with noisy minibatch gradients.

## When to use it

Use K-FAC when steps are expensive relative to computation, for example with large batches where the number of steps is the bottleneck, or on problems with strong curvature such as deep autoencoders, where first order methods progress slowly. For standard image and language training with well tuned Adam or SGD and a [learning rate schedule](/learning-rate-schedule/), the gain often does not pay for the extra code and memory.

## Pitfalls

- **Empirical Fisher.** Using the training labels instead of sampled targets in line L5 gives a different matrix with weaker theory; the paper samples from the model.
- **Stale inverses.** Recomputing the inverses rarely saves time, but with a fast changing network the stale preconditioner can give poor steps; the running averages and the damping must be tuned together.
- **Numerical inversion.** The factors are often nearly singular; use a [Cholesky decomposition](/cholesky-decomposition/) or an eigendecomposition of the damped factors, not an explicit inverse of the undamped ones.
- **Layer types.** The derivation is for fully connected layers; convolutions, normalization layers, embeddings and attention need their own factorization.

## Implementations

## History

Amari's natural gradient (1998) was too expensive for neural networks. Hessian-free optimization (Martens 2010) used curvature through matrix vector products. Martens and Grosse (2015) proposed the Kronecker-factored approximation and showed fast progress on deep autoencoders. Grosse and Martens (2016) extended it to convolution layers, and later work applied it to recurrent networks, reinforcement learning (ACKTR) and large batch distributed training.

## References
