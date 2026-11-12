---
tag: 3WZDG5
kind: technique
slug: gradient-checking
name: Gradient checking
aliases:
- numerical gradient check
- finite-difference gradient check
area: machine-learning/neural-network-training
level: intro
summary: "Test an analytic gradient by comparing each entry with a central difference (f(t + h e_i) - f(t - h e_i)) / 2h, using a relative error."
prereqs: [finite-differences, gradient]
see_also: [backpropagation, automatic-differentiation, machine-epsilon, catastrophic-cancellation, relu, richardson-extrapolation]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, 2nd edition, Springer, 2006
    locator: Section 8.1 (finite-difference derivative approximations; the step sqrt(u) for forward and u^(1/3) for central differences)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 11.5 (debugging strategies, including comparing back-propagated derivatives with numerical derivatives)
  - book: isbn:9780898716597
    title: Andreas Griewank and Andrea Walther, Evaluating Derivatives, 2nd edition, SIAM, 2008
    locator: Chapter 1 (the comparison of algorithmic differentiation with divided differences)
---

Gradient checking tests the code that computes a gradient, such as a new layer's [backpropagation](/backpropagation/) rule, by comparing it entry by entry with a [finite difference](/finite-differences/) estimate. The standard choice is the central difference $n_i = (f(\theta + h e_i) - f(\theta - h e_i)) / 2h$, whose truncation error is $O(h^2)$, with $h$ near $\varepsilon^{1/3}$, and the relative error $|g_i - n_i| / \max(|g_i|, |n_i|)$. It costs two evaluations of $f$ per parameter, so it is a test on small cases, not a way to train.

## In plain words

The derivative of $f$ is the slope: how much $f$ changes for a small change of one input. You can measure it directly. Move one parameter a little up, then a little down, evaluate $f$ both times, and divide the change by the distance. This is slow but hard to get wrong.

The gradient code is fast but easy to get wrong: a missing factor or a transposed matrix still gives numbers of the right shape. So you run both on a few small random inputs and check that they agree. If they do not, the gradient code has a bug, or the test hit one of the cases where the slow method is itself wrong.

## When it applies

Use it when you write a gradient by hand: a new layer, a custom loss, a backward rule for a new primitive in an [automatic differentiation](/automatic-differentiation/) system, or the adjoint of a simulation. The function must be smooth near the test point: twice differentiable for forward differences and three times for central differences. You need $f$ in floating point with good relative accuracy, and a parameter vector small enough that $2P$ evaluations are affordable; for a large model, check a random subset of the coordinates or a few random directions.

**Error analysis.** Let $f$ have bounded derivatives near $\theta$. By Taylor's theorem, for each coordinate $i$,

$$\frac{f(\theta + h e_i) - f(\theta)}{h} = \partial_i f(\theta) + \frac{h}{2} \partial_i^2 f(\xi), \qquad \frac{f(\theta + h e_i) - f(\theta - h e_i)}{2h} = \partial_i f(\theta) + \frac{h^2}{6} \partial_i^3 f(\eta),$$

for some $\xi, \eta$ within $h$ of $\theta$. In the central difference the even terms of the two Taylor series cancel. So the forward difference has truncation error $O(h)$ and the central difference $O(h^2)$.

Floating point adds a rounding error. If each value of $f$ has a relative error up to $\varepsilon$, the [machine epsilon](/machine-epsilon/), the difference in the numerator has an absolute error up to about $2\varepsilon |f|$, and dividing by $h$ makes it $O(\varepsilon |f| / h)$. This is [catastrophic cancellation](/catastrophic-cancellation/): the error grows as $h$ shrinks. Balancing the two terms gives the best step:

- forward: $\frac{h}{2} M_2 + \frac{2 \varepsilon |f|}{h}$ is smallest at $h \approx \sqrt{\varepsilon}$, with error about $\sqrt{\varepsilon} \approx 1.5 \times 10^{-8}$ in double precision;
- central: $\frac{h^2}{6} M_3 + \frac{\varepsilon |f|}{h}$ is smallest at $h \approx \varepsilon^{1/3} \approx 6 \times 10^{-6}$, with error about $\varepsilon^{2/3} \approx 4 \times 10^{-11}$,

where $M_k$ bounds $|\partial_i^k f|$ and the constants assume that $|f|$ and $M_k$ are of order 1. For a parameter of large size, scale the step to $h \max(1, |\theta_i|)$.

## The template

```pseudo id=main
GRADIENT-CHECK(f, g, θ, h, τ)                 ▷ g = the analytic gradient at θ
L1  for i ← 1 to P do
L2      θ⁺ ← θ + h e_i;  θ⁻ ← θ − h e_i
L3      n_i ← (f(θ⁺) − f(θ⁻)) / (2h)
L4      r_i ← |g_i − n_i| / max(|g_i|, |n_i|, tiny)
L5  return (max_i r_i ≤ τ, r)
```

The relative error in line L4 is scale free, so one tolerance $\tau$ works for gradients of any size, and the small constant tiny avoids $0/0$ when both values are zero. A vector form is $\lVert g - n \rVert / (\lVert g \rVert + \lVert n \rVert)$. In double precision with central differences, values near $10^{-8}$ or smaller mean that the gradient is right; values above $10^{-3}$ almost always mean a bug or a kink. Use double precision for the check even when the model trains in lower precision: in single precision, $\varepsilon^{2/3}$ is only about $2.4 \times 10^{-5}$.

## Classic examples

**Orders of the error.** For $f(x) = e^x \sin x$ at $x = 0.7$, the derivative is $(\cos x + \sin x) e^x = 2.837498$. The absolute error of the two differences:

| $h$ | forward | central |
|---|---|---|
| $10^{-1}$ | $1.5 \times 10^{-1}$ | $8.0 \times 10^{-4}$ |
| $10^{-2}$ | $1.5 \times 10^{-2}$ | $8.1 \times 10^{-6}$ |
| $10^{-3}$ | $1.5 \times 10^{-3}$ | $8.1 \times 10^{-8}$ |
| $10^{-4}$ | $1.5 \times 10^{-4}$ | $8.1 \times 10^{-10}$ |
| $\varepsilon^{1/3} \approx 6.06 \times 10^{-6}$ | $9.3 \times 10^{-6}$ | $5.7 \times 10^{-12}$ |
| $\sqrt{\varepsilon} \approx 1.49 \times 10^{-8}$ | $3.1 \times 10^{-8}$ | $8.9 \times 10^{-9}$ |
| $10^{-10}$ | $1.5 \times 10^{-6}$ | $3.6 \times 10^{-7}$ |
| $10^{-12}$ | $7.3 \times 10^{-5}$ | $7.3 \times 10^{-5}$ |

The forward error falls by 10 for each factor 10 in $h$, and the central error by 100, as the Taylor analysis says. The forward values match $\frac{h}{2} |f''(x)| = 1.540 h$ and the central values $\frac{h^2}{6} |f'''(x)| = 0.0810 h^2$. Below the best step, rounding takes over and both errors grow again. In the rows that rounding dominates, from $h = \varepsilon^{1/3}$ for the central difference and from $h = \sqrt{\varepsilon}$ for the forward one, the digits depend on the platform's floating point library, and another machine can give other values. Only the bound $O(\varepsilon |f| / h)$ on the rounding part carries over.

**A bug found.** For $f(\theta) = \log \sum_i \exp((A\theta)_i)$ with a random $4 \times 4$ matrix $A$, the gradient is $A^\top \mathrm{softmax}(A\theta)$. The correct code gives relative errors below $10^{-7}$ at random points. Code that forgets to normalize the softmax gives errors above $10^{-3}$, and the check fails at every point.

**A false alarm at a kink.** For $\mathrm{ReLU}(\theta) = \max(\theta, 0)$ at $\theta = 10^{-7}$ with $h = 10^{-5}$, the analytic derivative is 1, but the central difference is $(10^{-5} + 10^{-7} - 0) / (2 \cdot 10^{-5}) = 0.505$, a relative error of 0.495. The gradient is right; the difference crossed the kink at 0. At $\theta = 10^{-3}$ the same check passes with error below $10^{-9}$. In a network, a check fails like this when any pre-activation of a [ReLU](/relu/) unit, a max pool or a hinge loss lies within $h$ of its kink.

## Variations

- **Forward differences.** One extra evaluation per coordinate instead of two, with $h \approx \sqrt{\varepsilon}$ and error about $10^{-8}$. Only useful when $f$ is very costly.
- **Random directions.** Check $g^\top v$ against $(f(\theta + h v) - f(\theta - h v)) / 2h$ for a few random unit vectors $v$. This costs two evaluations per direction instead of per parameter and finds most bugs, but an error in a direction orthogonal to all chosen $v$ goes unseen.
- **Complex step.** For an $f$ that is real analytic and written with complex arithmetic, $\partial_i f(\theta) \approx \mathrm{Im}\, f(\theta + i h e_i) / h$ has no subtraction, so $h$ can be as small as $10^{-20}$ and the result is accurate to full precision. It does not work through $|\cdot|$, $\max$ or code that is not complex safe.
- **[Richardson extrapolation](/richardson-extrapolation/).** Combine central differences with steps $h$ and $h/2$ to cancel the $h^2$ term: $(4 n(h/2) - n(h)) / 3$ has error $O(h^4)$.
- **Checking a Jacobian or a backward rule.** For a primitive with vector output, compare $u^\top J v$ from the forward and the backward rule with the finite difference of $u^\top f$ in direction $v$, for random $u$ and $v$.

## Pitfalls

- **Kinks.** ReLU, max, absolute values and hinge losses give false alarms when a kink lies within $h$ of the test point. Use few data points, check that no pre-activation is within $h$ of a kink, or use smooth activations for the check.
- **Randomness.** Dropout, data augmentation or sampling inside $f$ makes $f(\theta + h e_i)$ and $f(\theta - h e_i)$ use different noise. Fix the seed, or turn the randomness off.
- **Steps that are too small.** $h = 10^{-12}$ gives an error of about $10^{-4}$, not a better estimate. Keep $h$ near $\varepsilon^{1/3}$ for central differences.
- **Single precision.** A check in float32 cannot reach errors much below $10^{-4}$, and correct code then looks wrong. Run the check in float64.
- **Regularization and batch terms.** Check the full loss, including weight decay and batch statistics, and make $f$ and $g$ use exactly the same batch.
- **Tiny gradients.** When both $g_i$ and $n_i$ are near zero, the relative error is dominated by noise. Look at the absolute error for these entries too.
- **Only at the start.** A check at the random initial point can miss a bug that appears only in other regimes, for example saturated units. Check at a few points, including points after some training.

## Exercises

1. Derive the truncation error $\frac{h^2}{6} f'''(\eta)$ of the central difference from the Taylor expansions of $f(x \pm h)$.
2. With a rounding error up to $\varepsilon |f|$ in each evaluation, show that the total error bound of the central difference is smallest for $h = (3 \varepsilon |f| / M_3)^{1/3}$.
3. Explain why the central difference of $\max(x, 0)$ at $x = \delta$ with $0 < \delta < h$ equals $(h + \delta) / 2h$.
4. Show that $(4 n(h/2) - n(h)) / 3$ cancels the $h^2$ term of the central difference $n(h)$.

## References
