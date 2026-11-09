---
tag: F3F4VF
kind: algorithm
slug: adam
name: Adam
aliases:
- Adam optimizer
- adaptive moment estimation
area: optimization/gradient-methods
level: core
summary: Combines momentum with per-coordinate adaptive scaling using bias-corrected first and second moment estimates.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the dimension, k: the number of steps, g: the cost of one stochastic gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2014
  people: [Diederik P. Kingma, Jimmy Ba]
  note: Kingma and Ba posted Adam in 2014 and published it at ICLR 2015; Reddi, Kale and Kumar (2018) showed that its convergence proof is wrong.
prereqs: [rmsprop, momentum-method, stochastic-gradient-descent, exponential-moving-average]
see_also: [amsgrad, adamw, radam, rmsprop, adagrad, momentum-method, learning-rate-schedule, stochastic-gradient-descent]
sources:
  - url: https://arxiv.org/abs/1412.6980
    title: Diederik P. Kingma and Jimmy Ba, Adam, A method for stochastic optimization, ICLR 2015
    locator: Algorithm 1 for the update and defaults, Section 2.1 for the informal step bound, Section 3 for the bias correction, Theorem 4.1 and Corollary 4.2 for the regret claim, Section 7.1 for AdaMax
  - url: https://arxiv.org/abs/1904.09237
    title: Sashank J. Reddi, Satyen Kale and Sanjiv Kumar, On the convergence of Adam and beyond, ICLR 2018
    locator: Section 3 for the error in the proof and Theorems 1 to 3 for the counterexamples, Section 4 and Theorem 4 for AMSGrad
  - url: https://arxiv.org/abs/2003.02395
    title: Alexandre Défossez, Léon Bottou, Francis Bach and Nicolas Usunier, A simple convergence proof of Adam and Adagrad, Transactions on Machine Learning Research, 2022
    locator: Section 4, the main theorems for Adam with and without momentum on smooth nonconvex problems with bounded gradients
  - url: https://arxiv.org/abs/2208.09632
    title: Yushun Zhang, Congliang Chen, Naichen Shi, Ruoyu Sun and Zhi-Quan Luo, Adam can converge without any modification on update rules, NeurIPS 2022
    locator: Section 3, convergence when β₂ is large enough relative to the number of terms n and β₁ < √β₂, and divergence for small β₂
  - url: https://arxiv.org/abs/1808.02941
    title: Xiangyi Chen, Sijia Liu, Ruoyu Sun and Mingyi Hong, On the convergence of a class of Adam-type algorithms for non-convex optimization, ICLR 2019
    locator: Section 3, sufficient conditions and the O(log T / √T) rate for AMSGrad and related methods
  - url: https://arxiv.org/abs/1811.09358
    title: Fangyu Zou, Li Shen, Zequn Jie, Weizhong Zhang and Wei Liu, A sufficient condition for convergences of Adam and RMSProp, CVPR 2019
    locator: Section 3, the condition on β₂,t → 1 and the step
  - url: https://arxiv.org/abs/2304.13972
    title: Haochuan Li, Alexander Rakhlin and Ali Jadbabaie, Convergence of Adam under relaxed assumptions, NeurIPS 2023
    locator: the main theorem, convergence under generalized smoothness without bounded gradients
  - url: https://arxiv.org/abs/1711.05101
    title: Ilya Loshchilov and Frank Hutter, Decoupled weight decay regularization, ICLR 2019
    locator: Section 2 and Algorithm 2, AdamW
---

Adam is a stochastic [gradient method](/stochastic-gradient-descent/) that keeps two [exponential moving averages](/exponential-moving-average/) for each coordinate: $m$ of the gradients, as in the [momentum method](/momentum-method/), and $v$ of their squares, as in [RMSProp](/rmsprop/). It corrects both for their start at zero and steps by $\alpha\hat{m}/(\sqrt{\hat{v}} + \epsilon)$. Kingma and Ba introduced it in 2014, and it became the default optimizer for training neural networks. Its original convergence proof is wrong: Reddi, Kale and Kumar (2018) gave a one-dimensional convex problem, within the assumptions of the claimed theorem, on which Adam's average regret does not go to zero. What is proved now is the exactness of the bias correction, a bound on each step, and convergence results that need the second-moment decay $\beta_2$ to be close to $1$ in a problem-dependent way or to grow to $1$.

## In plain words

Momentum smooths the direction of the steps by averaging recent gradients. RMSProp scales each coordinate by how large its gradients usually are, so that steep and flat directions move at similar speeds. Adam does both: it moves in the averaged direction, and it divides each coordinate by the typical size of its gradients.

Both averages start at zero, so in the first steps they are too small. Adam divides them by $1 - \beta^t$, which makes them exact averages of the gradients seen so far. Because of this the first step is exactly $\alpha$ in each coordinate when the gradient is steady, and the step size stays near $\alpha$ whatever the scale of the loss.

## The problem

The method minimizes $F(x) = \mathbb{E}f(x, \xi)$ over $\mathbb{R}^d$ from stochastic gradients, as in [stochastic optimization](/stochastic-optimization/), usually a neural network training loss. Kingma and Ba analysed it in [online convex optimization](/online-convex-optimization/), where losses $f_t$ arrive one at a time and the goal is small [regret](/regret/).

## The algorithm

```pseudo id=main
ADAM(∇f, x₁, α, β₁, β₂, ε, T)
L1  x ← x₁;  m ← 0;  v ← 0                   ▷ m, v ∈ ℝ^d
L2  for t ← 1 to T do
L3      g ← ∇fₜ(x)
L4      m ← β₁ m + (1 − β₁) g
L5      vᵢ ← β₂ vᵢ + (1 − β₂) gᵢ² for every i
L6      m̂ ← m / (1 − β₁ᵗ);  v̂ ← v / (1 − β₂ᵗ)      ▷ bias correction
L7      xᵢ ← xᵢ − αₜ m̂ᵢ / (√v̂ᵢ + ε) for every i
L8      x ← Π(x)                              ▷ projection, only in the online convex setting
L9  return x₁, …, x_{T+1}
```

The defaults are $\alpha = 10^{-3}$, $\beta_1 = 0.9$, $\beta_2 = 0.999$ and $\epsilon = 10^{-8}$. The convergence theorem of the paper uses $\alpha_t = \alpha/\sqrt{t}$ and a decreasing $\beta_{1,t}$; practice uses a constant or hand-made schedule. An equivalent form folds the corrections into the step, $\alpha_t\sqrt{1 - \beta_2^t}/(1 - \beta_1^t)$, which changes the role of $\epsilon$ slightly.

## Example

Take $F(x) = \frac{1}{2}(100x_1^2 + x_2^2)$, with condition number $100$, and $x_1 = (1, 1)$, $\alpha = 0.1$, $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 0$ and exact gradients.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $x_{t,1} = x_{t,2}$ | 1 | 0.9 | 0.80041 | 0.70159 | 0.60394 | 0.50796 | 0.41424 | 0.32342 | 0.23626 |

The first step is exactly $\alpha = 0.1$ in both coordinates, because $\hat{m}_1 = g_1$ and $\sqrt{\hat{v}_1} = |g_1|$. As in RMSProp, both coordinates follow the same path, because their gradients differ by the factor $100$ at every step and the division cancels it. The steps stay near $\alpha$ while the gradient keeps its sign; near the minimum the momentum term makes the iterates overshoot and oscillate, and a decreasing $\alpha$ is needed to settle.

## Correctness

What is proved for Adam itself (see the proof file):

- **Bias correction is exact.** $\hat{m}_t$ and $\hat{v}_t$ are weighted averages of $g_1, \dots, g_t$ and $g_1^2, \dots, g_t^2$ with weights that add up to $1$. So with a constant gradient every step is exactly $\alpha$, and with gradients of common mean $\mu$ and second moment $\nu$, $\mathbb{E}\hat{m}_t = \mu$ and $\mathbb{E}\hat{v}_t = \nu$ at every $t$.
- **Bounded steps.** If $\gamma = \beta_1^2/\beta_2 < 1$, every step is at most $\alpha_t\frac{1 - \beta_1}{1 - \beta_1^t}\sqrt{\frac{(1 - \beta_2^t)(1 - \gamma^t)}{(1 - \beta_2)(1 - \gamma)}}$, which is $\alpha_t$ at $t = 1$ and about $7.27\alpha_t$ in the limit for the defaults.

**The original proof has an error.** Kingma and Ba (2015, Theorem 4.1) claim $O(\sqrt{T})$ regret for online convex problems with bounded gradients, $\alpha_t = \alpha/\sqrt{t}$ and $\beta_1^2/\sqrt{\beta_2} < 1$. Reddi, Kale and Kumar (2018) show that this is false. On $[-1, 1]$ with losses $3x, -x, -x, 3x, -x, -x, \dots$, $\beta_1 = 0$ and $\beta_2 = 1/10$, Adam stays at $x = 1$, the worst point, and its average regret stays at $2/3$. The rare large gradient is forgotten before the next one comes, so the two small gradients in the other direction get steps almost three times larger. The proof needed the effective step $\alpha_t/\sqrt{\hat{v}_t}$ to be nonincreasing, which is true for AdaGrad but not for Adam. They also show that for every constant pair $\beta_1 < \sqrt{\beta_2}$ there is a stochastic convex problem on which Adam fails.

**What is known now.**

- [AMSGrad](/amsgrad/), which uses the running maximum of $\hat{v}$, has $O(\sqrt{T})$ regret on bounded convex domains (Reddi, Kale and Kumar 2018).
- On smooth nonconvex problems with gradients bounded by $R$, Adam with $\beta_2 = 1 - 1/N$ and $\alpha \propto 1/\sqrt{N}$ for a run of $N$ steps reaches $\mathbb{E}\lVert\nabla F\rVert^2 = O(d\ln N/\sqrt{N})$ at a random iterate; with constant $\beta_2$ and $\alpha$ the bound only gives a neighbourhood of stationary points (Défossez, Bottou, Bach and Usunier 2022).
- On finite sums with random shuffling, Adam with constant $\beta_1 < \sqrt{\beta_2}$ converges to a neighbourhood of stationary points when $\beta_2$ is close enough to $1$ for the given number of terms, and diverges on some problems when $\beta_2$ is small (Zhang, Chen, Shi, Sun and Luo 2022).
- Further sufficient conditions are in Chen, Liu, Sun and Hong (2019), Zou et al. (2019) and Li, Rakhlin and Jadbabaie (2023).

**What is only practice.** The defaults with a constant or hand-made schedule are not covered by a convergence theorem for general problems. That they work well for neural networks, with little tuning, is an empirical finding.

## Complexity

Each step costs one stochastic gradient and $O(d)$ arithmetic, with $\Theta(d)$ extra memory for $m$ and $v$, twice the memory of SGD with momentum. There is no general iteration bound for the default settings. With $\beta_2 = 1 - 1/k$ and $\alpha \propto 1/\sqrt{k}$, the result of Défossez et al. gives a random iterate with $\mathbb{E}\lVert\nabla F\rVert^2 = O(d\ln k/\sqrt{k})$ on smooth nonconvex problems with bounded gradients.

## Properties

- **Deterministic** given the gradient sequence.
- **Invariant to the scale of the loss.** With $\epsilon = 0$, multiplying the gradients of one coordinate by $c > 0$ does not change the iterates; the step size is set by $\alpha$, not by the gradient size.
- **Sign-like early steps.** With a steady gradient, each step is about $\alpha$ in size in every coordinate, as in sign descent.
- **Not a descent method** and does not converge to a point with constant $\alpha$; with noisy gradients the iterates keep moving at a scale of about $\alpha$.

## Variants and improvements

- **[AMSGrad](/amsgrad/).** Replace $\hat{v}_t$ by $\max(\hat{v}_{t-1}, \hat{v}_t)$, so the effective step never grows; this gives a correct regret bound.
- **[AdamW](/adamw/).** Apply weight decay directly to $x$ instead of adding it to the gradient, which makes the decay independent of the adaptive scaling (Loshchilov and Hutter 2019).
- **AdaMax.** Replace $\sqrt{\hat{v}}$ by an exponentially weighted infinity norm $u_t = \max(\beta_2u_{t-1}, |g_t|)$ (Kingma and Ba 2015, Section 7.1).
- **[RAdam](/radam/).** Turn the adaptive scaling on gradually, to reduce the variance of $\hat{v}$ in the first steps.
- **Nadam.** Use a Nesterov form of the momentum term.
- **Memory-saving forms.** [Adafactor](/adafactor/) stores factored second moments, and [LAMB](/lamb/) adds a per-layer trust ratio for large batches.

## When to use it

Use Adam to train neural networks, in particular transformers, recurrent networks and models with sparse or badly scaled gradients, where it reaches good training loss with little tuning. Use it with a [learning rate schedule](/learning-rate-schedule/) with warm-up and decay, and use AdamW when weight decay is wanted. For convex problems that need a guarantee, use AdaGrad, AMSGrad or SGD with a proved schedule.

## Pitfalls

- **No guarantee for the defaults.** Adam can fail to converge even on simple convex problems; if the loss stalls or oscillates, reduce $\alpha$, increase $\beta_2$ or use AMSGrad.
- **L2 penalty is not weight decay.** Adding $\lambda x$ to the gradient is rescaled by $1/\sqrt{\hat{v}}$, so heavily used weights are barely regularized; use AdamW.
- **$\epsilon$ matters.** For tiny $\hat{v}$, the step is about $\alpha\hat{m}/\epsilon$, and a large $\epsilon$ turns Adam into SGD with momentum; the right value depends on the model and the number format.
- **Citing the theorem.** Theorem 4.1 of the original paper is false as stated; cite AMSGrad or the later nonconvex results instead.
- **Instability with small $\beta_2$.** A small $\beta_2$ forgets rare large gradients quickly, which is the mechanism of the counterexample.

## Implementations

## History

Kingma and Ba posted Adam in December 2014 and published it at ICLR 2015, as a combination of the momentum method with the per-coordinate scaling of AdaGrad and RMSProp, with a bias correction for the zero start. The paper included a regret bound for online convex optimization. It quickly became the most used optimizer in deep learning. Reddi, Kale and Kumar (2018) found the error in the proof, gave counterexamples, and proposed AMSGrad. Later work explained why Adam works in practice: Défossez et al. (2022) and Zhang et al. (2022) gave convergence results with $\beta_2$ close to $1$, and Loshchilov and Hutter (2019) separated weight decay from the adaptive step in AdamW.

## References
