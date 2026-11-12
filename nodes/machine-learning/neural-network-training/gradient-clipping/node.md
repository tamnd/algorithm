---
tag: YBTGFW
kind: technique
slug: gradient-clipping
name: Gradient clipping
aliases:
- norm clipping
- value clipping
- gradient norm clipping
area: machine-learning/neural-network-training
level: core
summary: "Rescale the gradient when its norm exceeds a threshold c, g ← g·min(1, c/‖g‖), so a step keeps its direction but has bounded length; clipping each entry instead changes the direction."
prereqs: [exploding-gradient-problem, stochastic-gradient-descent]
see_also: [backpropagation-through-time, adam, momentum-method, projected-gradient-descent, mixed-precision-training, gradient-accumulation, lipschitz-condition, matrix-norms]
sources:
  - paper: "Razvan Pascanu, Tomas Mikolov and Yoshua Bengio, On the difficulty of training recurrent neural networks, Proceedings of the 30th International Conference on Machine Learning (ICML), PMLR 28(3), 2013"
    locator: pp. 1310 to 1318; Section 3.2 (scaling down the gradients) and Algorithm 1 (norm clipping)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 10.11.1 (clipping gradients; clipping by norm and clipping each element) and Section 8.2.4 (cliffs)
  - paper: doi:10.1145/2976749.2978318
    title: "Martín Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar and Li Zhang, Deep learning with differential privacy, Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security (CCS), 2016"
    locator: pp. 308 to 318; Section 3.1 and Algorithm 1 (per-example norm clipping and Gaussian noise)
  - paper: "Jingzhao Zhang, Tianxing He, Suvrit Sra and Ali Jadbabaie, Why gradient clipping accelerates training: a theoretical justification for adaptivity, ICLR 2020, arXiv:1905.11881"
    locator: Section 3 (the relaxed smoothness condition) and Section 4 (convergence of clipped gradient descent)
  - paper: "Andrew Brock, Soham De, Samuel L. Smith and Karen Simonyan, High-performance large-scale image recognition without normalization, ICML 2021, arXiv:2102.06171"
    locator: Section 4 (adaptive gradient clipping by the ratio of gradient norm to weight norm)
---

Gradient clipping limits the size of a gradient step. Clipping by norm, proposed for recurrent networks by Pascanu, Mikolov and Bengio (2013), computes the norm $\nu = \lVert g \rVert$ of the whole gradient and, if $\nu$ is larger than a threshold $c$, scales the gradient down to norm $c$:

$$g \leftarrow g \cdot \min\left(1, \frac{c}{\lVert g \rVert}\right).$$

The direction stays the same and only the length changes. Clipping by value instead clamps each entry to $[-c, c]$. That bounds every entry, but in general it turns the vector to a different direction. Both are cheap safeguards against the [exploding gradient problem](/exploding-gradient-problem/), where one huge gradient throws the parameters far away.

## In plain words

Gradient descent takes a step of length $\eta \lVert g \rVert$. Most of the time that is fine. But on a cliff of the loss surface, the gradient can be $10^9$ times larger than usual for one step, and the step then lands somewhere useless. Clipping puts a cap on the step length: if the gradient is longer than $c$, shrink it to length $c$ and keep pointing the same way. Short gradients pass through without change.

Clipping each entry separately is simpler, but it is a different operation. A gradient $(10, 0.1)$ that points almost along the first axis becomes $(1, 0.1)$ with $c = 1$, which points ten times more to the side.

## When it applies

- Training recurrent networks with [backpropagation through time](/backpropagation-through-time/), where products of many Jacobians can make the gradient explode on a few batches.
- Training deep networks and transformers, where rare loss spikes would otherwise undo much progress; a fixed threshold on the global norm is a common default.
- Any [stochastic gradient descent](/stochastic-gradient-descent/) setting with heavy-tailed gradient noise, where single minibatches give very large gradients.
- Private training, where each example's gradient must have bounded norm so that noise of a known scale hides it (DP-SGD, below).

It is not a cure for vanishing gradients, and it does nothing when the gradient is already short. It also does not fix a learning rate that is too large everywhere; then nearly every step is clipped and the method becomes normalized gradient descent with step $\eta c$.

## The template

The gradient is a list of tensors $g_1, \dots, g_K$, one per parameter tensor. Clipping by global norm treats them as one long vector.

```pseudo id=main
CLIP-BY-GLOBAL-NORM(g_1..g_K, c)          ▷ c > 0 is the threshold
L1  ν ← sqrt(Σ_k ‖g_k‖²)                   ▷ the norm of all entries together
L2  if ν > c then
L3      for k ← 1 to K do g_k ← g_k · (c / ν)
L4  return (g_1..g_K, ν)                   ▷ ν is useful to log
```

The caller then takes the step $\theta \leftarrow \theta - \eta g$ with the clipped gradient, or passes it to an optimizer such as [momentum](/momentum-method/) or [Adam](/adam/).

**Why the norm is exact.** After line 3 every entry is multiplied by the same positive factor $s = c/\nu$. So the new vector is $s g$, which has the same direction as $g$, and its norm is $s \nu = c$. If $\nu \le c$ nothing changes. So the output norm is $\min(\nu, c)$, up to one rounding error per entry in floating point.

**Clipping by value**, for contrast, is $g_i \leftarrow \max(-c, \min(c, g_i))$ for each entry $i$. Each entry of the result has absolute value at most $c$, but the norm can be as large as $c\sqrt{n}$ for $n$ entries, and the direction changes whenever some entries are clamped and others are not. The clipped vector is still a descent direction: each product $g_i \cdot \mathrm{clip}(g_i)$ is at least 0, so its inner product with $g$ is positive when $g \ne 0$.

## Classic examples

**A worked example.** Let $g = (3, 4)$, so $\lVert g \rVert = 5$, and let $c = 1$.

| method | result | norm | angle to the first axis |
|---|---|---|---|
| no clipping | $(3, 4)$ | 5 | 53.13° |
| clip by norm | $(0.6, 0.8)$ | 1 | 53.13° |
| clip by value | $(1, 1)$ | 1.414 | 45° |

Norm clipping keeps the angle and gives norm exactly $c$. Value clipping gives a norm above $c$ and turns the vector by 8.13°. For $g = (10, 0.1)$ the turn is larger: the angle goes from 0.573° to 5.711°.

**A cliff in a recurrent network.** The scalar recurrence $h_t = \tanh(3 h_{t-1})$ started at $h_0 = 0$ has $\partial h_{20} / \partial h_0 = 3^{20} = 3486784401$, while a start $10^{-3}$ away gives a derivative of about $10^{-18}$ (see the [exploding gradient problem](/exploding-gradient-problem/)). With learning rate $\eta = 0.1$, a plain step on the cliff moves the parameter by $3.5 \times 10^{8}$. With norm clipping at $c = 1$, it moves by 0.1. This is the picture Pascanu, Mikolov and Bengio give: the cliff gradient points the right way, but its size is meaningless.

**Global norm against per-tensor norm.** Let the gradient have two tensors, $g_1 = (30, 40)$ and $g_2 = (0.3, 0.4)$, and let $c = 1$. The global norm is $\sqrt{2500.25} = 50.0025$, and global clipping gives $(0.59997, 0.79996)$ and $(0.0060, 0.0080)$. The ratio of the two tensor norms stays 100 to 1. Clipping each tensor to norm 1 separately gives $(0.6, 0.8)$ and $(0.3, 0.4)$: the ratio becomes 2 to 1, and the full vector turns by about 26°.

## Variations

- **Clip by value.** Clamp each entry to $[-c, c]$, as above. Pascanu, Mikolov and Bengio note that Mikolov had used a heuristic of this kind for language models before their norm version.
- **Per-tensor or per-layer norm clipping.** Clip each $g_k$ to norm $c$ separately. It is easy to compute locally but changes the relative step sizes of the layers.
- **Adaptive thresholds.** Pascanu, Mikolov and Bengio suggest setting $c$ from the average norm seen over many updates. Others track a running percentile of the norms and clip relative to it.
- **Adaptive gradient clipping.** Brock et al. (2021) clip the gradient of each unit when the ratio of its norm to the norm of the unit's weights exceeds $\lambda$. This lets very deep networks train without batch normalization.
- **Per-example clipping in DP-SGD.** Abadi et al. (2016) clip the gradient of each training example to norm $C$, sum, and add Gaussian noise with standard deviation $\sigma C$. The clipping bounds how much one example can change the update, which is what the privacy analysis needs.
- **Skipping the step.** If $\nu$ is infinite or not a number, scaling cannot repair the gradient. Implementations skip the update, and Goodfellow, Bengio and Courville mention a random step of fixed size as an alternative.

**Theory.** Zhang et al. (2020) study functions whose Hessian norm grows with the gradient norm, $\lVert \nabla^2 f \rVert \le L_0 + L_1 \lVert \nabla f \rVert$, a weaker condition than a global [Lipschitz](/lipschitz-condition/) bound on the gradient. Under it, clipped gradient descent can converge much faster than gradient descent with a fixed step, because the step becomes small exactly where the curvature is large.

## Pitfalls

- **Clip at the right point.** With [gradient accumulation](/gradient-accumulation/), clip the accumulated gradient, not each micro-batch. With loss scaling in [mixed precision training](/mixed-precision-training/), unscale the gradient before clipping, or the threshold applies to the scaled values.
- **The global norm is global.** In data or model parallel training each worker holds only part of the gradient. The squares of the local norms must be summed across all workers before line 2, or each worker clips with a different factor and the direction changes.
- **Overflow in the norm.** The sum of squares can overflow even when every entry is finite. Scale by the largest absolute entry first, or accumulate in higher precision.
- **The threshold changes the optimizer.** If $c$ is far below the typical gradient norm, every step is clipped and the effective learning rate is $\eta c / \lVert g \rVert$, not $\eta$. Log $\nu$ and the fraction of clipped steps.
- **Clipping hides problems.** Frequent clipping can be a sign of a bug, a learning rate that is too high, or bad initialization. Clipping keeps training alive but does not explain the spikes.
- **Clipping is not a projection of the parameters.** It bounds the step, not the parameters. To keep $\theta$ in a set, use [projected gradient descent](/projected-gradient-descent/) instead.

## Exercises

1. Show that clipping by global norm returns a vector of norm exactly $\min(\lVert g \rVert, c)$ in exact arithmetic, and that it is a positive multiple of $g$.
2. For $g \in \mathbb{R}^n$, find the largest possible norm of the value-clipped vector, and give a $g$ that reaches it.
3. Show that the value-clipped vector $\tilde g$ satisfies $\tilde g \cdot g > 0$ for every $g \ne 0$, so it is a descent direction, but that the angle between $\tilde g$ and $g$ can be close to 90° in high dimension.
4. Let $\nu_1$ and $\nu_2$ be the norms of two gradient tensors. Compute the ratio of their norms after global clipping and after per-tensor clipping with the same $c$.
5. Take $f(\theta) = \theta^4$ and gradient descent with step $\eta = 0.1$ from $\theta_0 = 10$. Show that the plain iteration diverges and that the clipped iteration with $c = 1$ converges.

## References
