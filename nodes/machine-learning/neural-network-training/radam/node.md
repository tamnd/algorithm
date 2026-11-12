---
tag: KMW02T
kind: algorithm
slug: radam
name: RAdam
aliases:
- rectified Adam
- RAdam optimizer
area: machine-learning/neural-network-training
level: advanced
summary: Adam with a rectification term that removes the high variance of the adaptive step in early training, and plain momentum steps while that variance is not finite.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the number of parameters, k: the number of steps, g: the cost of one minibatch gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2020
  people: [Liyuan Liu, Haoming Jiang, Pengcheng He, Weizhu Chen, Xiaodong Liu, Jianfeng Gao, Jiawei Han]
  note: Liu and others explained learning rate warmup for Adam as variance reduction and replaced it with a rectification term, at ICLR 2020.
prereqs: [adam, momentum-method]
see_also: [learning-rate-schedule, adamw, amsgrad, lamb, stochastic-gradient-descent, exponential-moving-average]
sources:
  - url: https://arxiv.org/abs/1908.03265
    title: Liyuan Liu, Haoming Jiang, Pengcheng He, Weizhu Chen, Xiaodong Liu, Jianfeng Gao and Jiawei Han, On the variance of the adaptive learning rate and beyond, ICLR 2020
    locator: Section 3 (warmup as variance reduction, Theorem 1), Section 4.1 (estimation of rho), Section 4.2 (Eq. 5 and the rectification term), Algorithm 2, Appendix C (downgrading to SGDM)
  - url: https://github.com/LiyuanLucasLiu/RAdam
    title: Liyuan Liu, RAdam, the official implementation
    locator: radam.py, the test N_sma >= 5 for the rectified branch
  - url: https://arxiv.org/abs/1910.04209
    title: Jerry Ma and Denis Yarats, On the adequacy of untuned warmup for adaptive optimization, AAAI 2021
    locator: the comparison of RAdam with Adam under a fixed linear warmup over about 2/(1 - beta2) steps
  - url: https://arxiv.org/abs/1412.6980
    title: Diederik P. Kingma and Jimmy Ba, Adam, a method for stochastic optimization, ICLR 2015
    locator: Algorithm 1 (the base method)
---

RAdam (rectified Adam) is a variant of [Adam](/adam/) that multiplies the adaptive step by a rectification term $r_t \le 1$, and takes plain [momentum](/momentum-method/) steps while the second moment estimate rests on too few gradients. Liu and others (2020) observed that Adam needs a learning rate warmup on transformers and other networks because, in the first steps, $\hat{v}_t$ averages only a few squared gradients, so $1/\sqrt{\hat{v}_t}$ has a very large variance. They measure the number of gradients behind $\hat{v}_t$ by a length $\rho_t$ and scale the step so that its variance stays at the level of the limit. RAdam changes only the update step of the training loop; it does not remove the need for a decaying [learning rate schedule](/learning-rate-schedule/).

## In plain words

Adam divides each step by an average of recent squared gradients. At the start, that average comes from only one or two gradients, so it can be very small by chance, and then the step is very large. People fix this with warmup: they start with a tiny learning rate and raise it over thousands of steps.

RAdam computes how many gradients the average really rests on. While that number is four or less, it does not divide at all and takes ordinary momentum steps. After that, it shrinks the Adam step by a factor that is small at first and grows to one as the average rests on more gradients. This acts like a warmup that comes from the formula, not from a tuned number of steps.

## The problem

Minimize a training loss $L(\theta) = \mathbb{E}[\ell(\theta; \text{minibatch})]$ over the parameters $\theta \in \mathbb{R}^d$ of a network, for example an LSTM language model, a ResNet or a transformer, from minibatch gradients $g_t$. The goal is Adam's per coordinate scaling without its unstable first steps and without a tuned warmup length.

| symbol | meaning |
|---|---|
| $\alpha_t$ | step size |
| $\beta_1, \beta_2$ | decay constants of the first and second moments |
| $m_t, v_t$ | exponential averages of $g$ and $g^2$; $\hat{m}_t = m_t/(1 - \beta_1^t)$ |
| $\rho_\infty, \rho_t$ | the length of the simple moving average that matches the exponential average, in the limit and at step $t$ |
| $r_t$ | the rectification term |

## The algorithm

```pseudo id=main
RADAM(θ, α, β₁, β₂, T)
L1  m ← 0;  v ← 0                               ▷ m, v ∈ ℝ^d
L2  ρ∞ ← 2/(1 − β₂) − 1
L3  for t ← 1 to T do
L4      g ← minibatch gradient at θ
L5      v ← β₂ v + (1 − β₂) g²                    ▷ coordinatewise
L6      m ← β₁ m + (1 − β₁) g
L7      m̂ ← m / (1 − β₁ᵗ)
L8      ρₜ ← ρ∞ − 2t β₂ᵗ / (1 − β₂ᵗ)
L9      if ρₜ > 4 then                            ▷ the variance is finite
L10         lₜ ← √(1 − β₂ᵗ) / √v                  ▷ the adaptive learning rate, coordinatewise
L11         rₜ ← √((ρₜ − 4)(ρₜ − 2)ρ∞ / ((ρ∞ − 4)(ρ∞ − 2)ρₜ))
L12         θ ← θ − αₜ rₜ m̂ lₜ
L13     else θ ← θ − αₜ m̂                         ▷ momentum SGD
L14 return θ
```

This is Algorithm 2 of the paper, with the threshold $\rho_t > 4$. The official code and PyTorch use $\rho_t \ge 5$ (`N_sma >= 5`, `rho_t > 5`), which moves the first rectified step one step later for the usual $\beta_2$. Implementations add $\epsilon$ to $\sqrt{v}$ in line L10. Without the rectification, lines L10 and L12 are Adam's update with $\epsilon = 0$.

The length $\rho_t$ comes from a matching rule. The bias-corrected average $\hat{v}_t$ gives weight $(1 - \beta_2)\beta_2^{t-i}/(1 - \beta_2^t)$ to $g_i^2$. A simple moving average of the last $f$ values has its center of mass at $t - (f - 1)/2$. Setting the two centers of mass equal gives $f = \rho_t$ of line L8, and $t \to \infty$ gives $\rho_\infty$. The rectification $r_t$ is the square root of the ratio of the approximate variances of $1/\sqrt{\hat{v}}$ at length $\rho_\infty$ and at length $\rho_t$.

## Example

Take $\beta_1 = 0.9$, $\beta_2 = 0.999$, so $\rho_\infty = 1999$.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 10 | 100 | 1000 | 10000 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\rho_t$ | 1 | 1.9995 | 2.99867 | 3.9975 | 4.996 | 5.99416 | 9.98349 | 98.33294 | 835.96738 | 1998.09649 |
| $r_t$ | | | | | 0.01731 | 0.02582 | 0.049 | 0.21534 | 0.64533 | 0.99977 |

Steps 1 to 4 are momentum steps $\theta \leftarrow \theta - \alpha\hat{m}_t$. From step 5 on, the step is Adam's step times $r_t$: about $1.7\%$ of it at step 5, $22\%$ at step 100, $65\%$ at step 1000, and almost all of it after 10000 steps. For a gradient that is the same $g$ at every step, Adam moves each coordinate by exactly $\alpha$ per step from the first step; RAdam moves it by $\alpha|g|$ in steps 1 to 4 and by $\alpha r_t$ after that. The growth of $r_t$ looks like a warmup over a few thousand steps whose length follows from $\beta_2$.

The variance claim can be checked by simulation. For standard normal gradients and $\beta_2 = 0.999$, the sample variance of $\sqrt{(1 - \beta_2^t)/v_t}$ at $t = 10$ is about $0.076$, about 300 times its limit $0.00025$; after multiplication by $r_{10}^2$ it is $0.00018$, the same order as the limit.

## Correctness

The proof file shows four facts about the quantities in the algorithm:

- **The closed form.** Matching the center of mass of the bias-corrected exponential weights with a simple moving average of length $f$ gives exactly $f = \rho_\infty - 2t\beta_2^t/(1 - \beta_2^t)$.
- **Bounds.** $\rho_1 = 1$, $\rho_t$ increases strictly to $\rho_\infty$, and $\rho_t \le t$. So the first four steps always take the momentum branch, and if $\beta_2 \le 3/5$, then $\rho_\infty \le 4$ and RAdam is momentum SGD at every step.
- **The rectification term.** For $\rho_t > 4$, $0 < r_t < 1$, and $r_t$ increases to $1$, so RAdam becomes Adam after a long run.
- **Constant variance.** Under the paper's model ($1/\hat{v}_t$ scaled inverse chi squared with $\rho_t$ degrees of freedom, Eq. 5), the variance of $1/\sqrt{\hat{v}_t}$ is about $\rho_t/(2(\rho_t - 2)(\rho_t - 4)\sigma^2)$, and the rectified rate $r_t/\sqrt{\hat{v}_t}$ has the variance of the limit at every step. For $\rho_t \le 4$ the model's variance is not finite, which is why the algorithm does not divide there.

Theorem 1 of the paper shows that the variance of $1/\sqrt{\hat{v}}$ decreases as the number of degrees of freedom grows. The paper gives no regret or convergence theorem for RAdam as an optimizer; its support is the variance analysis and experiments on language modeling, image classification and machine translation.

## Complexity

Each step costs one minibatch gradient and $O(d)$ arithmetic, as in Adam; $\rho_t$ and $r_t$ are scalars, $O(1)$ per step. The state is $m$ and $v$, $2d$ numbers. Over $k$ steps the time is $O(k(g + d))$.

## Properties

- **A built in warmup.** $r_t$ grows from about $0.017$ to $1$ over a number of steps of order $1/(1 - \beta_2)$, which removes the need to tune a warmup length.
- **Scale of the early steps.** The momentum branch is not scale invariant: its step is $\alpha_t\hat{m}_t$, proportional to the gradient, while the adaptive step is about $\alpha_t$ per coordinate. With large gradients the first four steps can be large.
- **Same limit as Adam.** As $t \to \infty$, $r_t \to 1$ and RAdam takes Adam's steps.
- **No extra state.** The rectification depends only on $t$ and $\beta_2$, not on the data.

## Variants and improvements

- **Threshold 5.** The official code and the libraries use $\rho_t \ge 5$; some versions also skip the update entirely, instead of taking a momentum step, while $\rho_t$ is small.
- **With decoupled weight decay.** RAdam combines with the decay of [AdamW](/adamw/); the decay is applied to $\theta$ directly in both branches.
- **Lookahead and Ranger.** RAdam is often wrapped by the Lookahead method (Zhang and others, 2019), which averages fast and slow weights.
- **Untuned warmup.** Ma and Yarats (2021) find that Adam with a linear warmup over about $2/(1 - \beta_2)$ steps performs about the same as RAdam; this warmup is a [learning rate schedule](/learning-rate-schedule/) with no tuned length.

## When to use it

Use RAdam where Adam or AdamW needs a warmup to train stably, for example transformers and other deep networks trained with a large learning rate, and you do not want to tune the warmup length. If a warmup schedule is already tuned, RAdam gives little extra. It does not replace a decay of the learning rate later in training.

## Pitfalls

- **Threshold mismatch.** The paper uses $\rho_t > 4$ and the code $\rho_t \ge 5$. Results can differ in the first steps; state which one you use.
- **Large first steps.** The momentum branch uses the raw gradient scale. With a learning rate tuned for Adam and gradients of size much larger than $1$, the first steps can be too large. [Gradient clipping](/gradient-clipping/) helps.
- **Small $\beta_2$.** With $\beta_2 \le 0.6$ RAdam never uses the adaptive branch.
- **Not a convergence fix.** RAdam does not address the counterexample of [AMSGrad](/amsgrad/); as $r_t \to 1$ it behaves as Adam.

## Implementations

## History

Learning rate warmup for Adam became common with transformers (Vaswani and others, 2017). Liu, Jiang, He, Chen, Liu, Gao and Han (2019, ICLR 2020) showed that Adam without warmup moves to bad regions in the first updates, related this to the variance of the adaptive learning rate when few gradients are seen, and proposed RAdam. Ma and Yarats (2019, AAAI 2021) argued that RAdam is close to Adam with a simple fixed warmup.

## References
