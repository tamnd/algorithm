---
tag: 065TYG
kind: algorithm
slug: gradient-temporal-difference
name: Gradient temporal-difference learning
aliases:
- GTD
- GTD2
- TDC
- TD with gradient correction
area: machine-learning/reinforcement-learning
level: advanced
summary: "Linear TD methods that do stochastic gradient descent on the projected Bellman error, with a second weight vector. GTD2 and TDC converge off-policy, where plain TD can diverge."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {N: the number of samples, d: the number of features}
  time: {worst: "O(N d)"}
  space: {extra: "O(d)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2009
  people: [Richard S. Sutton, Hamid Reza Maei, Csaba Szepesvari]
  note: "Sutton, Szepesvari and Maei gave the first GTD method in 2008. GTD2 and TDC followed in 2009 and were proved to converge off-policy with linear features."
prereqs: [value-function-approximation, importance-sampling-off-policy, deadly-triad]
see_also: [temporal-difference-learning, least-squares-td, stochastic-approximation, off-policy-evaluation, retrace, stochastic-gradient-descent]
sources:
  - paper: doi:10.1145/1553374.1553501
    title: Richard S. Sutton, Hamid Reza Maei, Doina Precup, Shalabh Bhatnagar, David Silver, Csaba Szepesvari and Eric Wiewiora, Fast gradient-descent methods for temporal-difference learning with linear function approximation, ICML 2009, pages 993 to 1000
    locator: the MSPBE objective, GTD2 (equations 8 and 9), TDC (equation 10), Theorems 1 and 2
  - paper: "Richard S. Sutton, Csaba Szepesvari and Hamid Reza Maei, A convergent O(n) algorithm for off-policy temporal-difference learning with linear function approximation, Advances in Neural Information Processing Systems 21, 2008"
    locator: the first GTD algorithm and its convergence proof
  - paper: doi:10.1016/B978-1-55860-377-6.50013-X
    title: Leemon Baird, Residual algorithms, Reinforcement learning with function approximation, Machine Learning Proceedings 1995, pages 30 to 37
    locator: the star counterexample on which off-policy linear TD diverges
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 11.2 (Baird's counterexample), Section 11.7 (gradient-TD methods, off-policy GTD2 and TDC)
  - book: isbn:9780521515924
    title: Vivek S. Borkar, Stochastic Approximation, A Dynamical Systems Viewpoint, Cambridge University Press, 2008
    locator: Chapter 6 (two time scale stochastic approximation)
---

Gradient temporal-difference (GTD) methods are linear TD methods that are true stochastic gradient methods. They minimize the mean squared projected Bellman error, $\mathrm{MSPBE}(\theta) = \lVert\Pi(T\Phi\theta - \Phi\theta)\rVert_D^2$, whose minimum is the TD fixed point of [value function approximation](/value-function-approximation/). The gradient contains a product of two expectations, so the methods keep a second weight vector $w$ that estimates one of them. The two main methods are GTD2 and TDC (TD with gradient correction) of Sutton et al. (2009). Both cost $O(d)$ per step, like ordinary [temporal difference learning](/temporal-difference-learning/), and both converge with off-policy data, where semi-gradient TD can diverge. This removes one cause of the [deadly triad](/deadly-triad/).

## In plain words

Ordinary TD learning with features adjusts its weights in a direction that is not the downhill direction of any fixed error measure. When the data come from the policy being evaluated, this still works. When the data come from a different policy, the weights can grow without limit.

Gradient TD fixes this by choosing an error measure and going downhill on it. The measure asks: after the TD correction is projected back onto what the features can express, how large is it? Computing the downhill direction needs an average that one sample cannot give. So the method keeps a second, faster-learning set of weights that estimates that average, and uses it to steer the main weights. The cost per step stays small.

## The problem

Evaluate a target policy $\pi$ with linear features $\hat{v}(s) = \phi(s)^\top\theta$, from samples taken under a behavior policy $\mu$ that may differ from $\pi$. This is [policy evaluation](/policy-evaluation/), off-policy and with function approximation. A sample is $(x, \rho, r, x')$: the features $x = \phi(s)$ of a state drawn from a distribution $d$, the [importance sampling ratio](/importance-sampling-off-policy/) $\rho = \pi(a \mid s)/\mu(a \mid s)$ of the action taken, the reward, and the features $x'$ of the next state. With

$$A = \mathbb{E}[\rho\,x(x - \gamma x')^\top], \qquad b = \mathbb{E}[\rho\,r\,x], \qquad C = \mathbb{E}[x x^\top],$$

the objective is

$$\mathrm{MSPBE}(\theta) = (b - A\theta)^\top C^{-1}(b - A\theta),$$

and its minimum $0$ is attained at the TD fixed point $\theta^* = A^{-1}b$ when $A$ and $C$ are invertible.

## The algorithm

```pseudo id=main
GRADIENT-TD(sample, θ₀, γ, α, β, N, variant)
L1  θ ← θ₀;  w ← 0
L2  for k ← 0 to N − 1 do
L3      (x, ρ, r, x′) ← sample()                     ▷ features, ratio π/μ, reward, next features
L4      δ ← r + γ x′ᵀθ − xᵀθ                          ▷ the TD error
L5      if variant = TDC then θ ← θ + αₖ ρ (δ x − γ x′ (xᵀw))
L6      else θ ← θ + αₖ ρ (x − γ x′)(xᵀw)            ▷ GTD2
L7      w ← w + βₖ ρ (δ − xᵀw) x                      ▷ both use the old θ and w
L8  return θ
```

**Where the updates come from.** The gradient of the objective is

$$-\tfrac{1}{2}\nabla\mathrm{MSPBE}(\theta) = \mathbb{E}[\rho(x - \gamma x')x^\top]\;C^{-1}\;\mathbb{E}[\rho\delta x].$$

A single sample cannot estimate a product of two expectations without bias. So line L7 runs a least mean squares regression of $\rho\delta$ on $x$, whose solution is $w^*(\theta) = C^{-1}\mathbb{E}[\rho\delta x]$. With $w$ in place of $w^*$, sampling the first factor gives the GTD2 update of line L6. Since $\mathbb{E}[\rho(x - \gamma x')x^\top] = C - \gamma\mathbb{E}[\rho x' x^\top]$, the gradient is also $\mathbb{E}[\rho\delta x] - \gamma\mathbb{E}[\rho x' x^\top]w^*$. Sampling this form gives the TDC update of line L5: the ordinary off-policy TD update $\rho\delta x$ plus a correction term that is $0$ when $w = 0$.

**Two time scales.** TDC is analyzed with $\alpha_k/\beta_k \to 0$: $w$ moves faster and tracks $w^*(\theta)$, and $\theta$ sees it as converged. Both sequences must meet the [Robbins-Monro conditions](/robbins-monro-conditions/). GTD2 is analyzed with $\beta_k = \eta\alpha_k$ for a constant $\eta > 0$, one time scale.

## Example

Baird's counterexample (Baird 1995; Sutton and Barto 2018, Section 11.2) has 7 states and 8 weights. The six upper states have values $2\theta_i + \theta_8$ for $i = 1, \ldots, 6$, and the lower state has value $\theta_7 + 2\theta_8$. From every state, the dashed action goes to one of the six upper states with equal probability, and the solid action goes to the lower state. The behavior policy takes dashed with probability $6/7$ and solid with probability $1/7$, so the next state is uniform and states are sampled uniformly. The target policy always takes solid, so $\rho = 7$ for solid and $\rho = 0$ for dashed. All rewards are $0$ and $\gamma = 0.99$, so the true values are all $0$, and $\theta = 0$ represents them exactly. The start is $\theta_0 = (1, 1, 1, 1, 1, 1, 10, 1)$.

Semi-gradient off-policy TD uses $\theta \leftarrow \theta + \alpha\rho\delta x$ with $\alpha = 0.01$. TDC uses $\alpha = 0.005$ and $\beta = 0.05$. Both runs use seed 0. The table gives $\lVert\theta\rVert$ and, for TDC, the root mean square Bellman error over the 7 states.

| steps | semi-gradient TD, $\lVert\theta\rVert$ | TDC, $\lVert\theta\rVert$ | TDC, RMS Bellman error | TDC, values of the 7 states |
|---|---|---|---|---|
| 0 | 10.34 | 10.34 | 8.221 | 3, 3, 3, 3, 3, 3, 12 |
| 100 | 12.19 | 9.926 | 6.361 | 3.83, 3.72, 2.64, 2.64, 5.76, 2.64, 10.42 |
| 1000 | 390.7 | 8.761 | 0.0539 | 1.95, 1.90, 1.88, 1.90, 2.04, 1.91, 1.93 |
| 10000 | $8.9 \times 10^{11}$ | 8.761 | 0.0074 | 1.93 for each upper state, 1.95 |

Semi-gradient TD diverges: its expected update $\theta \leftarrow \theta + \alpha(b - A\theta)$ also diverges, because the off-policy $A$ has an eigenvalue with negative real part. TDC stays bounded and drives the Bellman error toward $0$. The values approach a vector that is almost constant, near $1.93$. A constant $c$ has Bellman error only $(1 - \gamma)c$, so the remaining drift to $0$ is slow. GTD2 with the same steps gives nearly the same numbers. In this example $C$ is singular, because 8 weights describe 7 states, but the updates stay in the span of the feature vectors, where the analysis holds.

## Correctness

The objective equals $\lVert\Pi(T\Phi\theta - \Phi\theta)\rVert_D^2$, so its zero is the TD fixed point. When $w$ equals $w^*(\theta)$, the mean of each $\theta$ update is $-\frac{\alpha}{2}\nabla\mathrm{MSPBE}(\theta)$, and the only rest point of the mean dynamics is $(\theta^*, 0)$. For GTD2 with $\beta = \eta\alpha$, the linear mean ODE has a matrix whose eigenvalues solve $\lambda^2 + \eta c\lambda + \eta a = 0$ with $a, c > 0$, so they all have negative real part. For TDC on two time scales the slow ODE is $\dot{\theta} = A^\top C^{-1}(b - A\theta)$, whose matrix is negative definite. In both cases this holds for every invertible $A$, on-policy or not. The theorems of [stochastic approximation](/stochastic-approximation/) then give convergence with probability one (Sutton et al. 2009, Theorems 1 and 2). The proofs of the mean dynamics are below.

## Complexity

- **Time.** Each step costs $O(d)$: three inner products and three vector updates. $N$ samples take $O(Nd)$ time.
- **Memory.** Two vectors of length $d$, against one for linear TD and a $d \times d$ matrix for [least-squares TD](/least-squares-td/).
- **Speed of convergence.** The rate depends on the conditioning of $A^\top C^{-1}A$ and on the ratio $\beta/\alpha$. Sutton et al. (2009) report that on their test problems, including a Computer Go task with about a million features, GTD2 and TDC learned about as fast as conventional TD, and much faster than the first GTD.

## Properties

- **Off-policy convergence.** Both methods converge with linear features for any behavior distribution $d$, given invertible $A$ and $C$ and suitable steps.
- **True gradient.** Unlike semi-gradient TD, the expected update of $\theta$ is the gradient of a fixed objective, once $w$ has converged.
- **Same fixed point as TD.** When TD converges, GTD2 and TDC converge to the same point.
- **Two parameters.** Both $\alpha$ and $\beta$ must be tuned, and the results can be sensitive to their ratio.

## Variants and improvements

- **GTD.** The first method (Sutton, Szepesvari and Maei 2008) minimizes the norm of the expected TD update, $\lVert b - A\theta\rVert^2$, and is slower than GTD2 and TDC.
- **GTD($\lambda$) and GQ($\lambda$).** Versions with eligibility traces, and for action values (Maei and Sutton 2010).
- **Greedy-GQ.** A control method that uses a TDC-style correction for a greedy target policy.
- **Emphatic TD.** A different route to stable off-policy TD: reweight the updates by an emphasis so that the expected update matrix becomes positive definite.
- **Proximal and saddle point forms.** The MSPBE can be written as a convex-concave saddle point problem in $(\theta, w)$, which gives finite sample bounds for GTD2-like methods.

## When to use it

Use TDC or GTD2 for off-policy prediction with linear features, when semi-gradient TD may diverge and you need $O(d)$ cost per step. If $O(d^2)$ per step is affordable, off-policy [least-squares TD](/least-squares-td/) solves the same equations without step sizes. On-policy, plain linear TD is simpler and usually as good.

## Pitfalls

- **Swapping the time scales.** In TDC, $w$ must adapt faster than $\theta$. With $\beta \le \alpha$ the method can oscillate or converge slowly.
- **High variance from large ratios.** The ratios $\rho$ enter every update. When $\pi$ and $\mu$ differ much, the variance is large; see [importance sampling for off-policy learning](/importance-sampling-off-policy/).
- **The fixed point may still be poor.** GTD methods converge to the TD fixed point under $d$, and off-policy that point can be far from the true values. Stability does not mean accuracy.
- **Nonlinear features.** The guarantees are for linear features. Nonlinear versions need an extra Hessian term.

## Implementations

## History

Baird (1995) gave the counterexample on which off-policy linear TD diverges, and proposed residual gradient methods, which are stable but converge to a different solution. Sutton, Szepesvari and Maei (2008) introduced the first gradient TD method with $O(d)$ cost. Sutton, Maei, Precup, Bhatnagar, Silver, Szepesvari and Wiewiora (2009) introduced the MSPBE objective with GTD2 and TDC, and proved their convergence with the two time scale theory of Borkar. Maei's thesis (2011) extended the family to traces, control and nonlinear features.

## References
