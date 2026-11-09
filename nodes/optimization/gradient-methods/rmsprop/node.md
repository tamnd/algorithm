---
tag: DDRZ14
kind: algorithm
slug: rmsprop
name: RMSProp
aliases:
- root mean square propagation
area: optimization/gradient-methods
level: core
summary: Adagrad with an exponentially decaying average of squared gradients, so the step size does not vanish.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the dimension, k: the number of steps, g: the cost of one stochastic gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2012
  people: [Geoffrey Hinton, Tijmen Tieleman]
  note: Tieleman and Hinton presented RMSProp in lecture 6.5 of the 2012 Coursera course Neural Networks for Machine Learning; it was never published as a paper.
prereqs: [adagrad, stochastic-gradient-descent, exponential-moving-average]
see_also: [adagrad, adam, adadelta, amsgrad, rprop, stochastic-gradient-descent, learning-rate-schedule, online-convex-optimization]
sources:
  - paper: "Tijmen Tieleman and Geoffrey Hinton, Lecture 6.5, rmsprop, Divide the gradient by a running average of its recent magnitude, Coursera course Neural Networks for Machine Learning, 2012"
    locator: the lecture slides, the update with the moving average of squared gradients and its motivation as a minibatch version of Rprop
  - url: https://arxiv.org/abs/1904.09237
    title: Sashank J. Reddi, Satyen Kale and Sanjiv Kumar, On the convergence of Adam and beyond, ICLR 2018
    locator: Section 3, Theorem 1 for the online counterexample with β₁ = 0 and β₂ = 1/(1 + C²), Theorem 3 for the stochastic counterexample for any constant β₁ < √β₂
  - url: https://arxiv.org/abs/1706.05507
    title: Mahesh Chandra Mukkamala and Matthias Hein, Variants of RMSProp and Adagrad with logarithmic regret bounds, ICML 2017
    locator: Section 4, SC-RMSProp with β_t = 1 − γ/t and its O(log T) regret for strongly convex losses
  - url: https://arxiv.org/abs/1811.09358
    title: Fangyu Zou, Li Shen, Zequn Jie, Weizhong Zhang and Wei Liu, A sufficient condition for convergences of Adam and RMSProp, CVPR 2019
    locator: Section 3, the sufficient condition on β_t and the step, and the O(log T / √T) rate
  - url: https://arxiv.org/abs/1807.06766
    title: Soham De, Anirbit Mukherjee and Enayat Ullah, Convergence guarantees for RMSProp and ADAM in non-convex optimization and an empirical comparison to Nesterov acceleration, 2018
    locator: Section 3, deterministic RMSProp on smooth functions
  - paper: "Naichen Shi, Dawei Li, Mingyi Hong and Ruoyu Sun, RMSprop converges with proper hyper-parameter, ICLR 2021"
    locator: the main theorem, random shuffling on finite sums with β close enough to 1
  - url: https://arxiv.org/abs/2208.09632
    title: Yushun Zhang, Congliang Chen, Naichen Shi, Ruoyu Sun and Zhi-Quan Luo, Adam can converge without any modification on update rules, NeurIPS 2022
    locator: Section 3, convergence for β₂ large enough relative to the number of terms n, with RMSProp as the case β₁ = 0
  - url: https://arxiv.org/abs/1308.0850
    title: Alex Graves, Generating sequences with recurrent neural networks, 2013
    locator: Section 4, the centred RMSProp variant with momentum used to train the networks
---

RMSProp is a per-coordinate adaptive [gradient method](/stochastic-gradient-descent/). It divides each gradient coordinate by the root of an [exponential moving average](/exponential-moving-average/) of the squares of past gradients in that coordinate, $v \leftarrow \beta v + (1 - \beta)g^2$, $x \leftarrow x - \eta g/(\sqrt{v} + \epsilon)$. It is [AdaGrad](/adagrad/) with the growing sum replaced by an average that forgets, so the steps do not shrink to zero during long runs. Tieleman and Hinton proposed it in a 2012 lecture for training neural networks. Its proved results are narrow: the steps are bounded, and one schedule with $\beta_t \to 1$ is exactly AdaGrad. With a constant $\beta$, Reddi, Kale and Kumar (2018) show that it can fail to converge even on a one-dimensional convex problem.

## In plain words

Each coordinate keeps a running estimate of how large its gradients usually are, the root mean square. The step in that coordinate is the gradient divided by this estimate, so it is about $\eta$ in size, whatever the scale of the gradients. A steep direction and a flat direction then move at the same speed.

AdaGrad does the same with the sum of all past squares, so its steps keep shrinking. RMSProp uses an average over roughly the last $1/(1 - \beta)$ steps, so it keeps moving and adjusts when the gradient scale changes, which matters for long nonconvex training runs.

## The problem

The method minimizes $F(x) = \mathbb{E}f(x, \xi)$ over $\mathbb{R}^d$ from stochastic gradients, as in [stochastic optimization](/stochastic-optimization/), or plays the online game of [online convex optimization](/online-convex-optimization/), where losses $f_t$ arrive one at a time. In the online setting the iterate is clipped to a box $\prod_i[l_i, h_i]$ after each step.

## The algorithm

```pseudo id=main
RMSPROP(∇f, x₁, η, β, ε, T)
L1  x ← x₁;  v ← 0 ∈ ℝ^d
L2  for t ← 1 to T do
L3      g ← ∇fₜ(x)                          ▷ stochastic gradient or loss gradient of round t
L4      vᵢ ← β vᵢ + (1 − β) gᵢ² for every i
L5      xᵢ ← xᵢ − η gᵢ / (√vᵢ + ε) for every i with vᵢ > 0
L6      xᵢ ← min(max(xᵢ, lᵢ), hᵢ)            ▷ only in the online setting with a box
L7  return x₁, …, x_{T+1}
```

The usual values are $\beta = 0.9$ or $0.99$, $\epsilon$ between $10^{-8}$ and $10^{-6}$, and $\eta$ around $10^{-3}$. Both $\eta$ and $\beta$ may change with $t$; the theory uses $\eta_t = \alpha/\sqrt{t}$ and sometimes $\beta_t \to 1$. Some libraries put $\epsilon$ inside the root, $\sqrt{v_i + \epsilon}$, which changes small steps a little.

## Example

Take $F(x) = \frac{1}{2}(100x_1^2 + x_2^2)$, with condition number $100$, and $x_1 = (1, 1)$, $\eta = 0.1$, $\beta = 0.9$, $\epsilon = 0$ and exact gradients $(100x_1, x_2)$.

| $t$ | $x_t$ (both coordinates) | $\sqrt{v_1}$ after the step | $\sqrt{v_2}$ after the step |
|---|---|---|---|
| 1 | 1 | 31.6228 | 0.31623 |
| 2 | 0.68377 | 36.9803 | 0.36980 |
| 3 | 0.49887 | 38.4664 | 0.38466 |
| 4 | 0.36918 | 38.3144 | 0.38314 |
| 5 | 0.27282 | 37.3581 | 0.37358 |
| 6 | 0.1998 | 35.9997 | 0.36000 |
| 7 | 0.1443 | | |

Both coordinates take exactly the same path, because the gradient in coordinate 1 is $100$ times the gradient in coordinate 2 at every step and the division by $\sqrt{v}$ cancels that factor. Gradient descent with a fixed step would need $\eta < 2/100$ to stay stable in coordinate 1 and would then move slowly in coordinate 2. The first step is $\eta/\sqrt{1 - \beta} = 0.316$, not $\eta$, because $v$ starts at $0$; this is the start-up bias that [Adam](/adam/) corrects.

## Correctness

What is proved for RMSProp itself:

- **Bounded steps.** Since $v_{t,i} \ge (1 - \beta)g_{t,i}^2$, every step satisfies $|x_{t+1,i} - x_{t,i}| \le \eta/\sqrt{1 - \beta}$, for every gradient sequence.
- **Scale invariance.** With $\epsilon = 0$, multiplying the gradients of one coordinate by $c > 0$ does not change the iterates.
- **Start-up bias.** With a constant gradient, $v_t = (1 - \beta^t)g^2$, so the step is $\eta/\sqrt{1 - \beta^t}$ instead of $\eta$.
- **AdaGrad as a special case.** With $\beta_t = 1 - 1/t$ and $\eta_t = \eta/\sqrt{t}$, $v_t$ is the mean of the past squared gradients and RMSProp is exactly AdaGrad, so it has AdaGrad's regret bound $(D_\infty^2/(2\eta) + \eta)\sum_i\lVert g_{1:T,i}\rVert_2$ on a box.
- **Failure with a constant decay.** On $[-1, 1]$ with losses $Cx, -x, -x, Cx, \dots$, $\beta = 1/(1 + C^2)$ and $\eta_t = \alpha/\sqrt{t}$, RMSProp stays at $x = 1$, the worst point, and its average regret stays at least $2(C - 2)/3$. The rare large gradient $C$ is forgotten before the next one comes, so the two small gradients in the other direction get large steps. Reddi, Kale and Kumar (2018) prove this and show that for every constant $\beta$ there is a stochastic convex problem on which the method fails.

What is proved only under extra assumptions: convergence to stationary points on smooth nonconvex problems when $\beta_t \to 1$ at a suitable rate (Zou et al. 2019), when $\beta$ is close enough to $1$ for the given finite sum (Shi et al. 2021; Zhang et al. 2022), or for deterministic gradients (De, Mukherjee and Ullah 2018). The common use, with a constant $\beta$ such as $0.9$ and a hand-made step schedule on neural networks, works well in practice but is not covered by a theorem.

## Complexity

Each step costs one stochastic gradient and $O(d)$ arithmetic, with $\Theta(d)$ extra memory for $v$. There is no iteration bound for the method with a constant $\beta$ on general convex problems, because of the counterexample above. With the schedule $\beta_t = 1 - 1/t$, $\eta_t = \eta/\sqrt{t}$, the AdaGrad bound applies: on a box of side $D$ with gradient coordinates at most $G$, the averaged point has expected gap at most $\sqrt{2}DdG/\sqrt{k}$.

## Properties

- **Deterministic** given the gradient sequence; with sampled gradients, the randomness comes only from the oracle.
- **Steps of size about $\eta$.** In steady state the step in each coordinate is about $\eta$ times the gradient divided by its root mean square, so its size does not depend on the scale of the loss.
- **Forgetting.** The average covers about $1/(1 - \beta)$ recent steps, so the method reacts to changes in gradient scale, unlike AdaGrad.
- **Not a descent method.** With noisy gradients and a constant step, the iterates keep moving at a size of about $\eta$ and do not converge to a point; a decaying [learning rate schedule](/learning-rate-schedule/) is needed for that.

## Variants and improvements

- **RMSProp with momentum.** Apply [momentum](/momentum-method/) to the scaled step $g/\sqrt{v}$. With bias correction and the momentum applied to $g$ instead, this becomes [Adam](/adam/).
- **Centred RMSProp.** Also keep an average $m$ of $g$ and divide by $\sqrt{v - m^2}$, an estimate of the standard deviation instead of the root mean square (Graves 2013).
- **[AMSGrad](/amsgrad/).** Use $\hat{v}_t = \max(\hat{v}_{t-1}, v_t)$, so the step never increases; this fixes the counterexample and has a regret bound.
- **SC-RMSProp.** Use $\beta_t = 1 - \gamma/t$ and $\eta_t = \alpha/t$ for strongly convex losses, with $O(\log T)$ regret (Mukkamala and Hein 2017).
- **[Adadelta](/adadelta/).** Replace $\eta$ by a moving root mean square of past steps, to fix the units of the update.
- **[Rprop](/rprop/).** The full-batch method that RMSProp was designed to imitate with minibatches: it uses only the sign of the gradient.

## When to use it

Use RMSProp to train neural networks, in particular recurrent networks and reinforcement learning agents, where gradient scales differ across parameters and change over time. It is also a simpler choice than Adam when momentum is not wanted. For convex problems with a required guarantee, use AdaGrad, AMSGrad or SGD with a proved schedule instead.

## Pitfalls

- **No guarantee with a constant decay.** The method can fail to converge on simple convex problems; a small $\beta$ makes this more likely because rare large gradients are forgotten quickly.
- **Large first steps.** Because $v$ starts at $0$, the first steps are up to $\eta/\sqrt{1 - \beta}$, which is $10\eta$ for $\beta = 0.99$. A warm-up schedule or bias correction helps.
- **The $\epsilon$ term.** Where $v$ is tiny, the step is about $\eta g/\epsilon$, which can be large; libraries differ in where they put $\epsilon$.
- **No convergence to a point.** With a constant $\eta$, the iterates keep moving at a scale of about $\eta$; reduce $\eta$ over time.

## Implementations

## History

Tieleman and Hinton described RMSProp in lecture 6.5 of the Coursera course Neural Networks for Machine Learning in 2012, as a minibatch version of [Rprop](/rprop/) that divides by a running root mean square. It was never published as a paper, and it is usually cited by the lecture slides. Graves (2013) used a centred variant with momentum for recurrent networks, and it became a standard optimizer for deep learning and deep reinforcement learning. Reddi, Kale and Kumar (2018) showed that it can fail to converge, and later work gave conditions under which it does converge.

## References
