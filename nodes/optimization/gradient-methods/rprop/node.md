---
tag: TRX7X7
kind: algorithm
slug: rprop
name: Rprop
aliases:
- resilient propagation
- resilient backpropagation
area: optimization/gradient-methods
level: advanced
summary: Per-coordinate step sizes adapted from gradient sign changes, ignoring gradient magnitude.
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {d: the dimension, k: the number of iterations, g: the cost of one gradient}
  time: {worst: O(k (g + d))}
  space: {extra: Θ(d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1993
  people: [Martin Riedmiller, Heinrich Braun]
  note: Riedmiller and Braun (1993) introduced Rprop for full-batch training of neural networks; Igel and Hüsken (2000) gave the simpler iRprop⁻ form used in most libraries.
prereqs: [gradient, gradient-descent, backpropagation]
see_also: [rmsprop, adam, adagrad, gradient-descent, backpropagation, bisection-method, coordinate-descent, step-size-selection]
sources:
  - paper: doi:10.1109/ICNN.1993.298623
    title: Martin Riedmiller and Heinrich Braun, A direct adaptive method for faster backpropagation learning, The RPROP algorithm, IEEE International Conference on Neural Networks, 1993
    locator: Section 3 for the update rules with weight backtracking and the values η⁺ = 1.2, η⁻ = 0.5, Δ₀ = 0.1, Δ_max = 50, Section 4 for the benchmark results
  - paper: "Christian Igel and Michael Hüsken, Improving the Rprop learning algorithm, Proceedings of the Second International ICSC Symposium on Neural Computation (NC 2000), ICSC Academic Press, 2000"
    locator: the variants Rprop⁻, Rprop⁺, iRprop⁻ and iRprop⁺
  - paper: "Christian Igel and Michael Hüsken, Empirical evaluation of the improved Rprop learning algorithms, Neurocomputing 50, 2003, pages 105 to 123"
    locator: the comparison of the four variants on benchmark problems
  - paper: "Aristoklis D. Anastasiadis, George D. Magoulas and Michael N. Vrahatis, New globally convergent training scheme based on the resilient propagation algorithm, Neurocomputing 64, 2005, pages 253 to 270"
    locator: the GRprop variant and its global convergence theorem
  - paper: "Tijmen Tieleman and Geoffrey Hinton, Lecture 6.5, rmsprop, Divide the gradient by a running average of its recent magnitude, Coursera course Neural Networks for Machine Learning, 2012"
    locator: the explanation of why Rprop fails with minibatches and RMSProp as the minibatch version
  - url: https://arxiv.org/abs/1802.04434
    title: Jeremy Bernstein, Yu-Xiang Wang, Kamyar Azizzadenesheli and Anima Anandkumar, signSGD, Compressed optimisation for non-convex problems, ICML 2018
    locator: Section 3, convergence of stochastic sign descent with large batches
---

Rprop (resilient propagation) is a full-batch gradient method that uses only the signs of the partial derivatives. Each coordinate has its own step size. The step size grows by a factor $\eta^+ = 1.2$ while the partial derivative keeps its sign, and shrinks by $\eta^- = 0.5$ when the sign flips, which means the last step jumped over a minimum in that coordinate. The size of the gradient is never used. Riedmiller and Braun introduced it in 1993 to train neural networks, where gradient sizes differ by orders of magnitude between layers. What is proved is that only signs matter, that the steps stay in their bounds, and, on this page, linear convergence on separable functions. On general functions and with minibatches there is no guarantee, and its good results are from practice.

## In plain words

Imagine walking downhill in fog along one direction. You only feel which way the ground slopes, not how steep it is. While the slope keeps pointing the same way, you take bigger and bigger steps. When it suddenly points back, you know you walked past the lowest point, so you take a smaller step back.

Rprop does this for every coordinate on its own. Because it ignores the steepness, a very flat direction and a very steep direction are handled at the same speed, and nobody has to choose a learning rate.

## The problem

Rprop minimizes a differentiable function $f$ on $\mathbb{R}^d$ with exact (full-batch) gradients, as in [unconstrained smooth minimization](/unconstrained-smooth-minimization/). In its original use, $f$ is the training error of a neural network over the whole data set, with gradients from [backpropagation](/backpropagation/).

## The algorithm

```pseudo id=main
RPROP(∇f, x₁, T, Δ₀, η⁺, η⁻, Δ_min, Δ_max)
L1  x ← x₁;  Δᵢ ← Δ₀ and pᵢ ← 0 for every i       ▷ p is the stored gradient
L2  for t ← 1 to T do
L3      g ← ∇f(x)
        for every i do
L4          if gᵢ pᵢ > 0 then Δᵢ ← min(η⁺ Δᵢ, Δ_max)
L5          else if gᵢ pᵢ < 0 then Δᵢ ← max(η⁻ Δᵢ, Δ_min);  gᵢ ← 0
L6          xᵢ ← xᵢ − sign(gᵢ) Δᵢ
L7      p ← g
L8  return x₁, …, x_{T+1}
```

This is the iRprop⁻ form of Igel and Hüsken (2000), which is what most libraries implement. After a sign flip the coordinate does not move, and setting $g_i$ to $0$ makes the next iteration keep the step size. The defaults are $\Delta_0 = 0.1$, $\eta^+ = 1.2$, $\eta^- = 0.5$, $\Delta_{\min} = 10^{-6}$ and $\Delta_{\max} = 50$. The original rule of Riedmiller and Braun also undoes the previous move after a sign flip (weight backtracking).

## Example

Take $f(x) = (x - 1)^2$ in one dimension, $x_1 = 0$, the default factors and $\Delta_{\min} = 0$.

| $t$ | $x_t$ | $\lvert x_t - 1\rvert$ | what happens |
|---|---|---|---|
| 1 | 0 | 1 | move by 0.1 |
| 2 | 0.1 | 0.9 | same sign, step 0.12 |
| 3 | 0.22 | 0.78 | step 0.144 |
| 4 | 0.364 | 0.636 | step 0.1728 |
| 5 | 0.5368 | 0.4632 | step 0.20736 |
| 6 | 0.74416 | 0.25584 | step 0.24883 |
| 7 | 0.99299 | 0.00701 | step 0.29860, crosses 1 |
| 8 | 1.29159 | 0.29159 | sign flip, step becomes 0.14930, no move |
| 9 | 1.29159 | 0.29159 | move by 0.14930 |
| 10 | 1.14229 | 0.14229 | same sign, step 0.17916, crosses 1 |
| 11 | 0.96313 | 0.03687 | sign flip, step 0.08958, no move |
| 12 | 0.96313 | 0.03687 | move by 0.08958, crosses 1 |
| 13 | 1.05271 | 0.05271 | sign flip, step 0.04479, no move |
| 14 | 1.05271 | 0.05271 | move by 0.04479 |
| 15 | 1.00792 | 0.00792 | |

The steps grow geometrically until the minimum is passed at $t = 7$. After that the method brackets the minimum with steps that shrink by at least $0.6$ every two or three iterations, much like the [bisection method](/bisection-method/). The error is not monotone: at $t = 7$ the method is very close to $1$ but still takes a large step.

## Correctness

What is proved (see the proof file):

- **Only signs matter.** If each partial derivative is multiplied by any positive factor, even a different one at every iteration, the iterates do not change. So Rprop is invariant to the scale of the loss and to the size of each partial derivative.
- **Steps in range.** Every step size stays in $[\Delta_{\min}, \Delta_{\max}]$, and every move in a coordinate is $0$ or the current step size.
- **Linear convergence on separable functions.** Let $f(x) = \sum_ih_i(x_i)$ where each $h_i'$ is negative left of $z_i$ and positive right of it (convexity is not needed). With $\Delta_{\min} = 0$, $\eta^-\eta^+ < 1$ and $\eta^-(1 + \eta^+) \ge 1$, each sign flip is followed by at most two moves before the next crossing, and the last move shrinks by at least $\eta^-\eta^+$ per crossing. Hence $|x_{t,i} - z_i| \le s_1(\eta^-\eta^+)^{\lfloor(t - t_1)/3\rfloor}$ after the first flip $t_1$, where $s_1$ is the move that caused it. For the defaults this is a factor $0.6$ every three iterations, whatever the curvature of $h_i$.

What is not proved: on nonseparable functions a sign flip in one coordinate need not mean that the minimum was crossed, and the sources here give no convergence theorem for the original rules. Anastasiadis, Magoulas and Vrahatis (2005) changed the rules to get a globally convergent variant. The speed of Rprop on neural network training is an empirical result (Riedmiller and Braun 1993; Igel and Hüsken 2003).

## Complexity

Each iteration costs one full gradient and $O(d)$ arithmetic, with $\Theta(d)$ extra memory for the step sizes and the stored gradient. On separable functions, after the first sign flip, reaching error $\varepsilon$ in a coordinate takes at most $3\lceil\ln(s_1/\varepsilon)/\ln(1/(\eta^-\eta^+))\rceil$ more iterations, about $5.9\ln(s_1/\varepsilon)$ for the defaults. Before the first flip, the steps grow geometrically, so a distance $D$ is covered in $O(\ln(\Delta_{\max}/\Delta_0) + D/\Delta_{\max})$ iterations.

## Properties

- **Deterministic** and full batch.
- **Scale-free in the gradient.** Only signs are used, so very small or very large gradients, as in deep or saturated networks, do not slow it down.
- **Not invariant to rotations.** The adaptation is per coordinate, so the behaviour depends on the coordinate system, unlike gradient descent with a line search.
- **Few settings.** The defaults work for many problems; only $\Delta_0$ and $\Delta_{\max}$ sometimes need changes.

## Variants and improvements

- **Rprop⁺ and Rprop⁻.** With and without weight backtracking, the undoing of the last move after a sign flip.
- **iRprop⁺.** Backtrack only if the error increased (Igel and Hüsken 2000).
- **GRprop.** A globally convergent variant with an extra step-size condition (Anastasiadis, Magoulas and Vrahatis 2005).
- **[RMSProp](/rmsprop/).** Divides by a running root mean square of the gradient, which keeps Rprop's insensitivity to scale but averages over minibatches, so it works with stochastic gradients.
- **Sign descent and signSGD.** Use $x \leftarrow x - \eta\operatorname{sign}(g)$ with a fixed or decreasing step; with large batches this has convergence guarantees on smooth nonconvex problems (Bernstein et al. 2018).

## When to use it

Use Rprop for full-batch training of small and medium neural networks and for other smooth problems where exact gradients are cheap and their sizes vary a lot across coordinates. It is a good default when no learning rate tuning is wanted. Do not use it with minibatches: noisy signs flip at random and the steps collapse; use RMSProp or Adam instead.

## Pitfalls

- **Minibatches.** The sign of a sum of gradients is not the sum of signs, so averaging Rprop steps over minibatches does not give the full-batch step, and the method stalls.
- **$\Delta_{\min} > 0$.** The iterates cannot settle closer than about $\Delta_{\min}$ to a minimizer.
- **Coordinate dependence.** On functions with long diagonal valleys, the per-coordinate signs flip often and progress can be slow.
- **Variant confusion.** Libraries differ in backtracking and in what happens after a sign flip; results with the same name can differ.

## Implementations

## History

Riedmiller and Braun (1993) proposed Rprop to fix the slow and erratic learning of backpropagation with a fixed learning rate, after earlier adaptive schemes such as delta-bar-delta and Quickprop. It was among the fastest full-batch methods for neural networks in the 1990s and is still in common libraries. Igel and Hüsken (2000, 2003) introduced and compared the iRprop variants. When training moved to minibatches, Tieleman and Hinton (2012) derived RMSProp from Rprop's idea of dividing by the gradient size.

## References
