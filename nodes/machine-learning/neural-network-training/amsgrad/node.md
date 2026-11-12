---
tag: VZ3Q5P
kind: algorithm
slug: amsgrad
name: AMSGrad
aliases:
- AMSGrad optimizer
area: machine-learning/neural-network-training
level: advanced
summary: A variant of Adam that divides by the running maximum of the second moment estimate, so the step never grows; this repairs Adam's failure on a simple online convex problem.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the number of parameters, k: the number of steps, g: the cost of one minibatch gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2018
  people: [Sashank J. Reddi, Satyen Kale, Sanjiv Kumar]
  note: Reddi, Kale and Kumar published the counterexample to Adam and the AMSGrad fix at ICLR 2018.
prereqs: [adam, online-convex-optimization, regret]
see_also: [adamw, radam, rmsprop, adagrad, online-gradient-descent, learning-rate-schedule]
sources:
  - url: https://arxiv.org/abs/1904.09237
    title: Sashank J. Reddi, Satyen Kale and Sanjiv Kumar, On the convergence of Adam and beyond, ICLR 2018
    locator: Section 3 (the error in the proof of Adam, Theorems 1 to 3 with the counterexamples), Section 4 (Algorithm 2, AMSGrad, and Theorem 4, its regret bound)
  - paper: doi:10.1109/ACCESS.2019.2916341
    title: Tran Thi Phuong and Le Trieu Phong, On the convergence proof of AMSGrad and a new version, IEEE Access 7, 2019
    locator: the gap in the handling of the momentum parameters in the proof of Theorem 4, and the corrected proof
  - url: https://arxiv.org/abs/1412.6980
    title: Diederik P. Kingma and Jimmy Ba, Adam, a method for stochastic optimization, ICLR 2015
    locator: Algorithm 1 and Theorem 4.1 (the regret claim that the counterexample refutes)
  - url: https://arxiv.org/abs/1808.02941
    title: Xiangyi Chen, Sijia Liu, Ruoyu Sun and Mingyi Hong, On the convergence of a class of Adam-type algorithms for non-convex optimization, ICLR 2019
    locator: Section 3, sufficient conditions and the O(log T / sqrt T) rate for AMSGrad on smooth nonconvex problems
---

AMSGrad is a variant of [Adam](/adam/) that divides each coordinate by $\sqrt{\hat{v}_t}$, where $\hat{v}_t = \max(\hat{v}_{t-1}, v_t)$ is the running maximum of the second moment estimate $v_t$. Reddi, Kale and Kumar (2018) found that Adam's convergence proof is wrong, gave a one dimensional [online convex](/online-convex-optimization/) problem on which Adam converges to the worst point, and proposed AMSGrad as the fix: with the maximum, the effective step $\alpha_t/\sqrt{\hat{v}_t}$ never grows, and the [regret](/regret/) is sublinear on convex problems. For neural network training it is a drop in replacement for Adam with one more vector of state; its guarantee is for convex losses and for stationary points of smooth nonconvex losses, not for global minima.

## In plain words

Adam divides each step by the typical size of recent gradients. If a coordinate sees one large gradient and then many small ones, Adam soon forgets the large one, its divisor shrinks, and the small gradients get large steps. When the rare large gradients carry the right information, Adam can be pushed the wrong way by the many small ones.

AMSGrad remembers the largest divisor it has seen and never lets it shrink. A step can then only get smaller over time for the same gradient. The rare large gradient keeps its weight, and the method moves the right way.

## The problem

The analysis is in [online convex optimization](/online-convex-optimization/): a convex set $F \subset \mathbb{R}^d$ with bounded diameter and convex losses $f_1, f_2, \ldots$ with bounded gradients arrive one at a time. After choosing $x_t$, the method pays $f_t(x_t)$ and sees $g_t = \nabla f_t(x_t)$. The goal is small regret $R_T = \sum_{t=1}^T f_t(x_t) - \min_{x \in F}\sum_{t=1}^T f_t(x)$, in particular $R_T/T \to 0$. In neural network training, $f_t$ is the loss of minibatch $t$ of a multilayer perceptron, a convolutional network or a transformer, $F = \mathbb{R}^d$, and AMSGrad replaces the update step of the training loop. Notation: $x$ or $\theta$ the parameters, $\alpha_t$ the step size, $\beta_1, \beta_2$ the moment constants.

## The algorithm

```pseudo id=main
AMSGRAD(f₁, f₂, …, x₁, α, β₁, β₂, T)
L1  m ← 0;  v ← 0;  v̂ ← 0                     ▷ m, v, v̂ ∈ ℝ^d
L2  for t ← 1 to T do
L3      g ← ∇fₜ(x)
L4      m ← β₁ m + (1 − β₁) g
L5      vᵢ ← β₂ vᵢ + (1 − β₂) gᵢ² for every i
L6      v̂ᵢ ← max(v̂ᵢ, vᵢ) for every i               ▷ Adam uses v̂ ← v here
L7      xᵢ ← xᵢ − αₜ mᵢ / √v̂ᵢ for every i         ▷ αₜ = α / √t in the analysis
L8      x ← the projection of x onto F in the norm weighted by √v̂
L9  return x₁, …, x_{T+1}
```

This is Algorithm 2 of the paper. It has no bias correction, and the analysis allows a decreasing $\beta_{1,t}$. The only change from Adam in the same form is line L6. When $F$ is a box, the weighted projection of line L8 is coordinatewise clipping. Practical versions add $\epsilon$ to the divisor and Adam's bias correction: PyTorch, with `amsgrad=True`, takes the maximum of the uncorrected $v$ and then divides it by $1 - \beta_2^t$.

## Example

Take the problem of Theorem 1 of the paper: $F = [-1, 1]$ and
$$f_t(x) = \begin{cases} Cx & t \bmod 3 = 1,\\ -x & \text{otherwise,}\end{cases}$$
with $C = 3$. Over a period of three steps the losses add to $(C - 2)x = x$, so the best fixed point is $x^* = -1$. Use $\beta_1 = 0$, $\beta_2 = 1/(1 + C^2) = 0.1$, $\alpha_t = 0.5/\sqrt{t}$, $\epsilon = 0$ and $x_1 = 0$.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Adam $x_t$ | 0 | −0.52705 | −0.25668 | 0.02227 | −0.23953 | −0.06907 | 0.12807 | −0.06983 | 0.06494 | 0.2259 |
| AMSGrad $x_t$ | 0 | −0.52705 | −0.40282 | −0.30139 | −0.56319 | −0.48514 | −0.41388 | −0.61178 | −0.55008 | −0.4919 |

The first step is the same: $v_1 = 0.9 \cdot 9 = 8.1$ and the step is $0.5 \cdot 3/\sqrt{8.1} = 0.52705$. Then the paths split. With $\beta_2 = 0.1$, Adam's $v$ falls back within one step: in the periodic regime it takes the values $8.2072, 1.7207, 1.0721$ in the three steps of a period, so the steps are $1.047\alpha_t$ down and $0.762\alpha_t + 0.966\alpha_t = 1.728\alpha_t$ up. The two small gradients win. AMSGrad keeps $\hat{v} = 8.2072$ for all three steps, so it steps $1.047\alpha_t$ down and $2 \times 0.349\alpha_t$ up, and the large gradient wins.

| $T$ | 300 | 3000 | 30000 |
|---|---|---|---|
| Adam, $x_{T+1}$ | 1 | 1 | 1 |
| Adam, $R_T/T$ | 0.66802 | 0.67235 | 0.66899 |
| AMSGrad, $x_{T+1}$ | −0.97983 | −0.99363 | −0.99798 |
| AMSGrad, $R_T/T$ | 0.05174 | 0.01245 | 0.00354 |

Adam sits at the worst point $x = 1$ and its average regret stays near $2(C - 2)/3 = 2/3$. AMSGrad approaches $-1$ and its average regret falls by about $\sqrt{10}$ for each factor of $10$ in $T$.

## Correctness

The proof file proves both directions on this problem, for every $C > 2$, with $\beta_1 = 0$ and $\beta_2 = 1/(1 + C^2)$:

- **Adam fails.** All $v_t \le C^2$, $v_t \ge (1 - \beta_2)C^2$ after a large gradient, and $v_t < 2$ after a small one. From period $1$ on, the two upward steps exceed the downward step by more than $0.24\,\alpha_{3k+1}\sqrt{1 + C^2}/C$. The sum of these margins diverges, so $x$ reaches $1$ and stays there at the start of every period, and $R_T/T \to 2(C-2)/3$ (Theorem 1 of the paper).
- **AMSGrad succeeds.** Since $\alpha_t$ falls and $\hat{v}_t$ does not, both upward steps of a period are at most $\alpha_{3k+1}/\sqrt{\hat{v}_{3k+1}}$, so a period moves $x$ down by at least $(C - 2)\alpha_{3k+1}/C$ until the projection stops it. So $x_t \to -1$ and $R_T/T \to 0$.
- **The key property.** For any losses, $\alpha_t/\sqrt{\hat{v}_{t,i}}$ is nonincreasing when $\alpha_t$ is. Adam's proof needed this for $\alpha_t/\sqrt{v_{t,i}}$, which is false.

The paper extends the failure: for every pair of constants $\beta_1 < \sqrt{\beta_2}$ there is an online convex problem on which Adam has average regret bounded away from $0$ (Theorem 2), and a stochastic convex problem on which it does not converge to the optimum (Theorem 3). For AMSGrad, Theorem 4 bounds the regret when $F$ has bounded diameter, the gradients are bounded, $\alpha_t = \alpha/\sqrt{t}$, $\beta_{1,t} \le \beta_1$ and $\beta_1/\sqrt{\beta_2} < 1$; with $\beta_{1,t}$ decaying, the average regret goes to $0$ at a rate of order $1/\sqrt{T}$ up to a logarithmic factor. Tran and Phong (2019) found a gap in that proof, in the handling of the varying $\beta_{1,t}$, and gave a corrected proof. On smooth nonconvex problems, Chen, Liu, Sun and Hong (2019) show that AMSGrad reaches a point with small expected gradient at rate $O(\log T/\sqrt{T})$. None of these results says that AMSGrad trains a deep network better than Adam; in practice the two often reach similar losses.

## Complexity

Each step costs one gradient and $O(d)$ arithmetic, the same as Adam plus one maximum per coordinate. The extra memory is $3d$ numbers for $m$, $v$ and $\hat{v}$, against $2d$ for Adam. Over $k$ steps the time is $O(k(g + d))$.

## Properties

- **Nonincreasing effective step.** With $\alpha_t$ nonincreasing, each coordinate's effective step $\alpha_t/\sqrt{\hat{v}_{t,i}}$ never grows, as in [AdaGrad](/adagrad/), while the moments still use exponential averages as in [RMSProp](/rmsprop/).
- **Long memory of large gradients.** One very large gradient makes $\hat{v}_i$ large for the rest of the run, which can make the steps of that coordinate very small. This is the price of the guarantee.
- **Same as Adam when $v$ grows.** If $v_{t,i}$ never decreases, line L6 changes nothing and AMSGrad takes exactly Adam's steps (in the same form, without bias correction).
- **Scale invariance.** With $\epsilon = 0$, multiplying the gradients of a coordinate by $c > 0$ multiplies $m$ by $c$ and $\sqrt{\hat{v}}$ by $c$, so the iterates do not change.

## Variants and improvements

- **AdamNC.** The paper's other fix uses an increasing $\beta_{2,t}$, for example $\beta_{2,t} = 1 - 1/t$, which makes $v$ the plain mean of the squared gradients, as in AdaGrad, and also gives a nonincreasing effective step.
- **AdamX.** Tran and Phong (2019) change the maximum so that it accounts for a decreasing $\beta_{1,t}$, which makes their corrected proof go through.
- **With decoupled decay.** AMSGrad combines with the weight decay of [AdamW](/adamw/) in the same way as Adam.
- **Other stable variants.** [RAdam](/radam/) attacks a different problem of Adam, the high variance of $v$ in the first steps, and does not use a maximum.

## When to use it

Use AMSGrad when you need Adam's per coordinate scaling with a regret guarantee on convex problems, or when Adam oscillates or diverges with a small $\beta_2$ on a problem with rare large gradients. For most neural network training, Adam or AdamW with $\beta_2$ close to $1$ and a [learning rate schedule](/learning-rate-schedule/) work as well; try AMSGrad as a switch when training is unstable.

## Pitfalls

- **Bias correction and the maximum.** Taking the maximum of the corrected $v/(1 - \beta_2^t)$ instead of the uncorrected $v$ keeps the early, inflated values for a long time. Libraries differ here.
- **A single outlier.** A huge gradient from a bad minibatch freezes the coordinate for a long time, because $\hat{v}$ never falls. [Gradient clipping](/gradient-clipping/) before the optimizer limits this.
- **The guarantee is for convex losses.** The regret bound does not say anything about the generalization or the final loss of a deep network.
- **Citing the theorem.** The original proof of Theorem 4 has a gap; cite the corrected proof of Tran and Phong (2019) together with it.

## Implementations

## History

Kingma and Ba (2015) claimed an $O(\sqrt{T})$ regret bound for Adam. Reddi, Kale and Kumar (2018) showed that the proof needs the effective step to be nonincreasing, which Adam does not ensure, gave the three step counterexample and its stochastic version, and proposed AMSGrad and AdamNC. Tran and Phong (2019) found and fixed a gap in the AMSGrad proof. Later work gave conditions under which plain Adam does converge, mostly with $\beta_2$ close to $1$; see [Adam](/adam/).

## References
