---
tag: V8X117
kind: algorithm
slug: adadelta
name: Adadelta
area: optimization/gradient-methods
level: advanced
summary: RMSProp-style method that removes the need for a global learning rate.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the dimension, k: the number of steps, g: the cost of one stochastic gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2012
  people: [Matthew D. Zeiler]
  note: Zeiler (2012) proposed Adadelta to remove the global learning rate of AdaGrad and to give the update the units of the parameters.
prereqs: [rmsprop, adagrad, stochastic-gradient-descent, exponential-moving-average]
see_also: [rmsprop, adagrad, adam, rprop, stochastic-gradient-descent, learning-rate-schedule, natural-gradient-descent, stochastic-optimization]
sources:
  - url: https://arxiv.org/abs/1212.5701
    title: Matthew D. Zeiler, ADADELTA, An adaptive learning rate method, 2012
    locator: Section 3 and Algorithm 1 for the update, Sections 3.1 and 3.2 for the moving window and the units argument, Section 4 for the MNIST and speech experiments with ρ = 0.95 and ε = 10⁻⁶
  - paper: "John Duchi, Elad Hazan and Yoram Singer, Adaptive subgradient methods for online learning and stochastic optimization, Journal of Machine Learning Research 12, 2011, pages 2121 to 2159"
    locator: Section 1.3, the AdaGrad update that Adadelta modifies
  - paper: "Sue Becker and Yann LeCun, Improving the convergence of back-propagation learning with second order methods, Proceedings of the 1988 Connectionist Models Summer School, pages 29 to 37"
    locator: the diagonal Hessian approximation that Zeiler uses to motivate the units correction
  - url: https://arxiv.org/abs/1206.1106
    title: Tom Schaul, Sixin Zhang and Yann LeCun, No more pesky learning rates, ICML 2013
    locator: Sections 2 and 3, per-parameter learning rates from local curvature and variance estimates
  - url: https://arxiv.org/abs/1705.07795
    title: Francesco Orabona and Tatiana Tommasi, Training deep networks without learning rates through coin betting, NeurIPS 2017
    locator: Section 3, a learning-rate-free method with a regret guarantee
  - url: https://arxiv.org/abs/2301.07733
    title: Aaron Defazio and Konstantin Mishchenko, Learning-rate-free learning by D-adaptation, ICML 2023
    locator: Section 2, a learning-rate-free method with convergence rates for convex Lipschitz functions
---

Adadelta is a per-coordinate adaptive [gradient method](/stochastic-gradient-descent/) that tries to remove the learning rate. Like [RMSProp](/rmsprop/), it divides the gradient by a running root mean square of past gradients. Unlike RMSProp, it multiplies by a running root mean square of past steps instead of a fixed learning rate, $\Delta x_t = -\frac{\mathrm{RMS}[\Delta x]_{t-1}}{\mathrm{RMS}[g]_t}g_t$. Zeiler proposed it in 2012 so that the update has the units of the parameters, as in Newton's method. What is proved is structural: the method needs its constant $\epsilon$ to move at all, its steps are bounded by the recent steps, and with correctly scaled constants it is invariant to rescaling each coordinate. No convergence rate is proved; its use rests on experiments.

## In plain words

Gradient methods need a step size, and a good one depends on the units of the problem. If you measure a parameter in millimetres instead of metres, the right step changes by a factor of a million, but plain gradient descent does not know that.

Adadelta keeps two running averages for each coordinate: how large the gradients have been, and how large its own steps have been. It then takes a step whose size is the typical recent step, in the direction and with the relative size of the current gradient. The first steps are set by a small constant $\epsilon$; after that the method grows or shrinks its steps from its own history.

## The problem

The method minimizes $F(x) = \mathbb{E}f(x, \xi)$ over $\mathbb{R}^d$ from stochastic gradients, as in [stochastic optimization](/stochastic-optimization/), usually the training loss of a neural network.

## The algorithm

```pseudo id=main
ADADELTA(∇f, x₁, ρ, ε, T)
L1  x ← x₁;  b ← 0;  a ← 0                  ▷ b = E[g²], a = E[Δx²], both in ℝ^d
L2  for t ← 1 to T do
L3      g ← ∇fₜ(x)
L4      bᵢ ← ρ bᵢ + (1 − ρ) gᵢ² for every i
L5      Δᵢ ← −(√(aᵢ + ε) / √(bᵢ + ε)) gᵢ for every i
L6      aᵢ ← ρ aᵢ + (1 − ρ) Δᵢ² for every i
L7      x ← x + Δ
L8  return x₁, …, x_{T+1}
```

Zeiler uses $\rho = 0.95$ and $\epsilon = 10^{-6}$. Line L5 uses $a$ from the previous step, because the current step is not known yet. Many libraries multiply line L5 by a learning rate $\lambda$, with default $1$ in PyTorch, which brings back the parameter that the method was meant to remove. The proofs use two constants, $\epsilon_x$ in the numerator and $\epsilon_g$ in the denominator, because they have different units.

## Example

Take the linear function $f(x) = 2x$ in one dimension, $x_1 = 0$, $\rho = 0.9$ and $\epsilon = 0.01$.

| $t$ | $\Delta_t$ | $x_{t+1}$ | $\sqrt{b_t + \epsilon}$ | $\sqrt{a_t + \epsilon}$ |
|---|---|---|---|---|
| 1 | −0.31235 | −0.31235 | 0.64031 | 0.14056 |
| 2 | −0.32036 | −0.63271 | 0.87750 | 0.17042 |
| 3 | −0.32587 | −0.95858 | 1.04594 | 0.19431 |
| 4 | −0.33015 | −1.28873 | 1.17712 | 0.21420 |
| 5 | −0.33371 | −1.62244 | 1.28376 | 0.23115 |
| 6 | −0.33679 | −1.95923 | 1.37267 | 0.24583 |
| 7 | −0.33953 | −2.29876 | 1.44804 | 0.25868 |
| 8 | −0.34202 | −2.64078 | 1.51266 | 0.27004 |

The first step is $\sqrt{\epsilon}\,g/\sqrt{(1 - \rho)g^2 + \epsilon} = 0.1 \cdot 2/0.64031$. After that the steps grow slowly, because each step is a little larger than the root mean square of the earlier ones. The step is $0.458$ at $t = 100$ and $0.694$ at $t = 399$, and it tends to $|g| = 2$: on a long slope Adadelta becomes gradient descent with step $1$.

## Correctness

What is proved (see the proof file):

- **$\epsilon$ is needed.** With $\epsilon = 0$ in the numerator, $a$ stays $0$ and the method never moves.
- **First step.** $\Delta_1 = -\sqrt{\epsilon}\,g_1/\sqrt{(1 - \rho)g_1^2 + \epsilon}$, about $\sqrt{\epsilon/(1 - \rho)}$ in size, so the early steps are set by $\epsilon$.
- **Bounded steps.** $|\Delta_t| \le \sqrt{(a_{t-1} + \epsilon)/(1 - \rho)}$, so each step is at most about $1/\sqrt{1 - \rho}$ times the recent root mean square step.
- **Units.** If the loss is multiplied by $c$ and coordinate $i$ is rescaled by $s_i$, and the two $\epsilon$ constants are rescaled with the units they carry, the iterates are exactly the rescaled iterates. Gradient descent, RMSProp and Adam do not have this property. With one shared $\epsilon$, as in the paper, it holds only approximately.
- **Constant slope.** With a constant gradient $c$ and one shared $\epsilon$, the step tends to $|c|$; with $\epsilon_g = 0$, the step grows at least like $\sqrt{\epsilon(1 + (1 - \rho)(t - 1))}$.

What is not proved: there is no convergence guarantee or rate for Adadelta in the convex or nonconvex stochastic settings in the paper or in the sources here. The constant-slope result shows that its effective step is not tied to any schedule, so the analyses of [AdaGrad](/adagrad/) and [AMSGrad](/amsgrad/) do not carry over. The claim that it needs no tuning is supported by experiments on MNIST and speech recognition in Zeiler's paper, not by a theorem.

## Complexity

Each step costs one stochastic gradient and $O(d)$ arithmetic, with $\Theta(d)$ extra memory for the two averages, twice the memory of RMSProp. No bound on the number of steps is known.

## Properties

- **Deterministic** given the gradient sequence.
- **No global learning rate** in the original form; $\rho$ and $\epsilon$ remain, and $\epsilon$ acts as the initial learning rate.
- **Invariant to diagonal rescaling** when the two constants are scaled with their units, which is the diagonal form of the invariance of Newton's method.
- **Self-adjusting step.** The step size follows the recent steps, so it can grow on long slopes and shrink near a minimum without a schedule.

## Variants and improvements

- **Adadelta with a learning rate.** Library versions multiply the step by $\lambda$, often $1$; this allows a schedule but removes the main selling point.
- **[RMSProp](/rmsprop/).** Uses a fixed $\eta$ in place of $\mathrm{RMS}[\Delta x]$.
- **[Adam](/adam/).** Adds momentum and bias correction to RMSProp, and became the more common choice.
- **Learning-rate-free methods with proofs.** Coin-betting methods (Orabona and Tommasi 2017) and D-Adaptation (Defazio and Mishchenko 2023) remove the learning rate with convergence guarantees for convex problems.
- **Curvature-based rates.** Schaul, Zhang and LeCun (2013) set per-parameter rates from estimates of curvature and gradient variance.

## When to use it

Use Adadelta when you want an adaptive method with few settings and the problem has parameters on very different scales, for example in older neural network code and some speech and vision models. In current practice Adam is more common, and for problems that need a guarantee, AdaGrad or a learning-rate-free method with a proof is a safer choice.

## Pitfalls

- **Slow start.** The first steps have size about $\sqrt{\epsilon/(1 - \rho)}$, which is $0.0045$ for the defaults; if the parameters need to move far, the method needs many steps to grow its step size.
- **$\epsilon$ is a learning rate.** Changing $\epsilon$ changes the path a lot, not only the numerical safety.
- **Library learning rates.** Some libraries use a learning rate default other than $1$ for Adadelta, which can make it extremely slow; check the default.
- **No convergence to a point.** The step does not decay by itself; with noisy gradients the iterates keep moving.

## Implementations

## History

Zeiler (2012) proposed Adadelta as a fix for two problems of AdaGrad: the steps that shrink forever and the global learning rate that must be tuned. He motivated the ratio $\mathrm{RMS}[\Delta x]/\mathrm{RMS}[g]$ by the units of Newton's method and by the diagonal Hessian approximation of Becker and LeCun (1988). The method was widely used in early deep learning libraries before Adam became the standard choice.

## References
