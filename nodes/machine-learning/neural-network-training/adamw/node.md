---
tag: P87340
kind: algorithm
slug: adamw
name: AdamW
aliases:
- decoupled weight decay Adam
- Adam with decoupled weight decay
area: machine-learning/neural-network-training
level: core
summary: Adam with weight decay applied to the weights directly, scaled by the schedule, instead of an L2 term added to the gradient before the adaptive scaling.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the number of parameters, k: the number of steps, g: the cost of one minibatch gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2017
  people: [Ilya Loshchilov, Frank Hutter]
  note: Loshchilov and Hutter posted the paper on arXiv in November 2017 and published it at ICLR 2019.
prereqs: [adam, weight-decay, stochastic-gradient-descent]
see_also: [learning-rate-schedule, amsgrad, radam, lamb, adafactor, regularization, momentum-method, batch-normalization]
sources:
  - url: https://arxiv.org/abs/1711.05101
    title: Ilya Loshchilov and Frank Hutter, Decoupled weight decay regularization, ICLR 2019
    locator: Section 2 (Equation 1, Propositions 1 to 3), Algorithm 1 (SGDW) and Algorithm 2 (AdamW), and the appendix on normalized weight decay
  - url: https://arxiv.org/abs/1412.6980
    title: Diederik P. Kingma and Jimmy Ba, Adam, a method for stochastic optimization, ICLR 2015
    locator: Algorithm 1 (the Adam update and its default parameters)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 7.1.1 (L2 parameter regularization as weight decay) and Section 8.5.3 (Adam)
  - url: https://pytorch.org/docs/stable/generated/torch.optim.AdamW.html
    title: PyTorch documentation, torch.optim.AdamW
    locator: the algorithm box (the weight is multiplied by 1 minus the learning rate times the decay before the Adam step) and the default weight_decay of 0.01
---

AdamW is [Adam](/adam/) with decoupled [weight decay](/weight-decay/): at each step it shrinks the weights by $\eta_t\lambda\theta$, where $\eta_t$ is the [schedule](/learning-rate-schedule/) multiplier, instead of adding the gradient $\lambda\theta$ of an L2 penalty to the minibatch gradient before Adam's per coordinate scaling. Loshchilov and Hutter (2019) showed that the two forms are the same for plain [SGD](/stochastic-gradient-descent/), up to the rescaling $\lambda = \alpha\lambda'$, but not for Adam: there the L2 term is divided by $\sqrt{\hat{v}}$, so weights with large gradients are barely regularized. AdamW is now the default optimizer for training transformers. Like Adam it has no general convergence guarantee for deep networks; what is proved is the exact relation between the two forms of decay.

## In plain words

Weight decay pulls every weight a little toward zero at each step, so that the network prefers small weights. With plain gradient descent, there are two ways to do this that give the same result: add a penalty for large weights to the loss, or shrink the weights after each step.

Adam does not take plain steps. It divides each coordinate of the gradient by the typical size of that coordinate's past gradients. If the penalty goes into the gradient, it is divided too. A weight that gets large gradients then feels almost no pull, and a weight that gets no gradient is pulled hard. AdamW keeps the shrink outside of Adam, so every weight shrinks by the same fraction.

## The problem

The setting is the training of a neural network of any architecture by minibatch gradients, with the regularized goal of minimizing the [empirical risk](/empirical-risk-minimization/) $L(\theta)$ while keeping the weights small. AdamW changes only the update step of the training loop. Notation: $\theta \in \mathbb{R}^d$ the parameters, $g_t$ the minibatch gradient of the data loss (without any penalty), $\alpha$ the base step size, $\eta_t$ the schedule multiplier, $\lambda$ the decoupled decay factor, $\lambda'$ an L2 coefficient, $\beta_1, \beta_2, \epsilon$ the Adam constants. In the L2 form the method minimizes $L(\theta) + \frac{\lambda'}{2}\lVert\theta\rVert^2$; AdamW does not minimize a fixed penalized objective, because its decay acts on the weights after the adaptive step.

## The algorithm

```pseudo id=main
ADAMW(∇L, θ, α, β₁, β₂, ε, λ, T)
L1  m ← 0;  v ← 0                                  ▷ m, v ∈ ℝ^d
L2  for t ← 1 to T do
L3      g ← ∇L_B(θ)                                ▷ data loss only, no λθ term
L4      m ← β₁ m + (1 − β₁) g
L5      vᵢ ← β₂ vᵢ + (1 − β₂) gᵢ² for every i
L6      m̂ ← m / (1 − β₁ᵗ);  v̂ ← v / (1 − β₂ᵗ)
L7      ηₜ ← the schedule multiplier of step t
L8      θᵢ ← θᵢ − ηₜ (α m̂ᵢ / (√v̂ᵢ + ε) + λ θᵢ) for every i
L9  return θ
```

This is Algorithm 2 of the paper. The L2 form, "Adam with weight decay" in older libraries, instead sets $g \leftarrow \nabla L_B(\theta) + \lambda'\theta$ in line L3 and drops $\lambda\theta_i$ from line L8. Lines L4 to L6 are Adam's moment estimates; see the [Adam](/adam/) page for their derivation and the bias correction.

The paper's defaults for the Adam part are those of Adam. The decay $\lambda$ is a tuned hyperparameter. The paper also suggests a normalized decay, $\lambda = \lambda_{\text{norm}}\sqrt{b/(BT)}$ for batch size $b$, $B$ training points and $T$ epochs, so that the best value depends less on the length of the run.

Libraries write the decay with the learning rate inside: PyTorch multiplies the weights by $1 - \gamma_t\lambda_{\text{pt}}$, where $\gamma_t$ is the current learning rate, before the Adam step. This is line L8 with $\alpha\lambda_{\text{pt}}$ in place of $\lambda$, so a change of the learning rate there also changes the decay.

## Example

Take two weights, $\theta_0 = (1, 1)$, and a data gradient that is $(1, 0)$ at every step: the first weight is in use, the second gets no gradient. Use $\alpha = 0.01$, $\eta_t = 1$, $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$. Compare AdamW with $\lambda = 0.001$ against Adam with the L2 coefficient $\lambda' = 0.1$, the coefficient that gives the same SGD run since $\alpha\lambda' = 0.001$.

| step | AdamW $\theta_1$ | AdamW $\theta_2$ | Adam L2 $\theta_1$ | Adam L2 $\theta_2$ |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 0.989 | 0.999 | 0.99 | 0.99 |
| 2 | 0.978011 | 0.998001 | 0.98 | 0.980003 |
| 3 | 0.967033 | 0.997003 | 0.970001 | 0.97001 |
| 5 | 0.94511 | 0.99501 | 0.950004 | 0.950046 |
| 100 | | 0.904792 | | 0.224446 |

In the first step, Adam with L2 sees the gradient $(1.1, 0.1)$ and normalizes each coordinate to a step of $\alpha = 0.01$. The penalty adds nothing to the step of the busy weight, and it moves the idle weight ten times faster than the intended $0.001$ per step. AdamW moves the busy weight by $\alpha$ plus the decay $0.001$, and shrinks the idle weight by the factor $0.999$ per step, so $\theta_2 = 0.999^{100} = 0.904792$ after 100 steps. Under L2 the idle weight is at $0.2244$ after 100 steps: the steps get smaller only as $\lambda'\theta_2$ falls below the size that $\hat{v}$ remembers.

## Correctness

AdamW is a heuristic for nonconvex training; there is no theorem that it reaches a minimizer of a neural network loss. The claims of the method are statements about the update rule, proved in the proof file below.

- **SGD (Proposition 1 of the paper).** Plain SGD with step $\alpha$ and L2 coefficient $\lambda'$ takes the same steps as SGD with decoupled decay $\lambda = \alpha\lambda'$: $\theta - \alpha(g + \lambda'\theta) = \theta - \alpha g - \lambda\theta$.
- **SGD with momentum.** The two forms differ, because the L2 term enters the momentum buffer and is applied again in later steps. With $\theta_0 = (1, 2)$, $g = (\frac12, -1)$, $\alpha = \frac1{10}$, $\beta = \frac9{10}$, $\lambda' = \frac1{10}$, $\lambda = \frac1{100}$, the two runs agree after one step and differ after two.
- **Adam (Proposition 2 of the paper).** No L2 coefficient gives AdamW: on the two starts $(1, 1)$ and $(2, 2)$ with gradient $(1, 0)$, the idle coordinate forces $\lambda = \alpha\lambda'/(\lambda' + \epsilon)$ and $\lambda = \alpha\lambda'/(2\lambda' + \epsilon)$, which have no common solution with $\lambda > 0$.
- **Idle weights.** A coordinate with zero data gradient decays exactly as $\theta_{t,i} = \theta_{0,i}\prod_{s \le t}(1 - \eta_s\lambda)$.

## Complexity

Each step costs one minibatch gradient and $O(d)$ arithmetic; the decay adds $d$ multiplications. The extra memory is $\Theta(d)$ for $m$ and $v$, the same as Adam and twice that of SGD with momentum. Over $k$ steps the time is $O(k(g + d))$, where $g$ is the cost of one gradient. There is no general bound on the number of steps for deep networks.

## Properties

- **Equal relative decay.** Every weight with $\theta_i \ne 0$ shrinks by the same fraction $\eta_t\lambda$ per step, whatever its gradient history.
- **Decay follows the schedule.** Because line L8 multiplies the decay by $\eta_t$, the decay falls with the learning rate. Without this, a large decay late in training would pull the weights toward zero after the steps have become small.
- **Separate hyperparameters.** The paper reports that, with decoupled decay, the best $\lambda$ depends less on $\alpha$, so the two can be tuned more independently. This is an observation on their image classification experiments, not a theorem.
- **Not scale invariant in the decay.** Adam's step is invariant to rescaling the loss; the decay term is not, so multiplying the loss by $c$ changes the balance between data fit and decay.

## Variants and improvements

- **SGDW.** Decoupled decay with SGD and momentum, Algorithm 1 of the paper. Without momentum it equals the L2 form; with momentum it differs slightly.
- **AdamWR.** AdamW with cosine annealing and warm restarts (see [learning rate schedule](/learning-rate-schedule/)).
- **Decay on a subset.** In practice biases and the gains of [batch normalization](/batch-normalization/) and [layer normalization](/layer-normalization/) are often excluded from the decay.
- **Other decoupled optimizers.** [LAMB](/lamb/) adds $\lambda\theta$ to the Adam ratio before its layer wise normalization, and [Adafactor](/adafactor/) and [AMSGrad](/amsgrad/) can take decoupled decay in the same way as line L8.

## When to use it

Use AdamW instead of Adam with an L2 term whenever weight decay is wanted with an adaptive optimizer, in particular for transformers and other models trained with Adam. With plain SGD, decoupled decay and L2 are the same up to $\lambda = \alpha\lambda'$, so the choice is only a matter of how the hyperparameter is written.

## Pitfalls

- **The same name for two methods.** In older code, "Adam with weight decay" often meant the L2 form. Check whether the decay goes into the gradient or onto the weights.
- **Units of $\lambda$.** In the paper the decay is multiplied by $\eta_t$ only; in PyTorch it is multiplied by the full learning rate. A value of $\lambda$ copied from one convention to the other is off by the factor $\alpha$.
- **Decay with normalization layers.** For weights that feed a batch or layer normalization, the loss does not change when the weights are scaled, so the decay then changes the effective step size rather than the function. It still matters, but not as a penalty on the function.
- **Accumulated and clipped gradients.** The decay is applied once per optimizer step, not per micro batch of [gradient accumulation](/gradient-accumulation/), and [gradient clipping](/gradient-clipping/) acts on $g$ without the decay.

## Implementations

## History

Loshchilov and Hutter posted "Decoupled weight decay regularization" in November 2017 and published it at ICLR 2019. They took the definition of weight decay as $\theta_{t+1} = (1 - \lambda)\theta_t - \alpha\nabla f_t(\theta_t)$ from Hanson and Pratt (1988), proved that it equals L2 regularization for SGD and not for adaptive methods, and attributed part of the gap in generalization between Adam and SGD with momentum on image classification to this difference. Deep learning libraries then added AdamW as a separate optimizer.

## References
