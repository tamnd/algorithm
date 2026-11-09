---
tag: MHMX5D
kind: algorithm
slug: momentum-method
name: Momentum method
aliases:
- Momentum
- Nesterov momentum
- Polyak momentum
- heavy ball method
- heavy-ball method
area: optimization/gradient-methods
level: core
summary: "Polyak's heavy ball: x_(k+1) = x_k - α∇f(x_k) + β(x_k - x_(k-1)). On quadratics with tuned α, β the error falls like ((√κ-1)/(√κ+1))^k, the optimal rate."
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, D: "L_f R^2 (the smoothness constant times the squared distance from x_0 to x*)", ε: the target accuracy, κ: the condition number L_f/μ}
  time: {worst: O(k n)}
  space: {extra: O(n)}
  gradients: {quadratic: O(√κ log(1/ε)), convex_average: O(D/ε), step: "1"}
properties: {deterministic: true, iterative: true, descent_method: false, first_order: true}
history:
  year: 1964
  people: [Boris T. Polyak]
  note: Polyak introduced the heavy ball method in 1964 and proved its accelerated local rate. Momentum became standard in neural network training after the 1986 back-propagation paper of Rumelhart, Hinton and Williams.
prereqs: [gradient-descent, strong-convexity, convergence-rate]
see_also: [nesterov-accelerated-gradient, gradient-descent, linear-convergence-strongly-convex, first-order-lower-bound, condition-number-of-an-optimization-problem, conjugate-gradient-method, chebyshev-iteration, stochastic-gradient-descent]
sources:
  - paper: doi:10.1016/0041-5553(64)90137-5
    title: Boris T. Polyak, Some methods of speeding up the convergence of iteration methods, USSR Computational Mathematics and Mathematical Physics 4(5), 1964
    locator: pages 1 to 17 (the heavy ball method, its optimal parameters and its local rate)
  - book: isbn:9780911575149
    title: Boris T. Polyak, Introduction to Optimization, Optimization Software, 1987
    locator: Chapter 3, Section 3.2 (the heavy ball method)
  - paper: doi:10.1137/15M1009597
    title: Laurent Lessard, Benjamin Recht and Andrew Packard, Analysis and design of optimization algorithms via integral quadratic constraints, SIAM Journal on Optimization 26(1), 2016
    locator: pages 57 to 95 (the one-dimensional strongly convex function on which the heavy ball method with Polyak's parameters does not converge)
  - paper: doi:10.1109/ECC.2015.7330562
    title: Euhanna Ghadimi, Hamid Reza Feyzmahdavian and Mikael Johansson, Global convergence of the heavy-ball method for convex optimization, European Control Conference, 2015
    locator: pages 310 to 315 (the O(1/k) rate of the averaged iterate for convex smooth functions and a linear rate for strongly convex functions)
  - paper: doi:10.1038/323533a0
    title: David E. Rumelhart, Geoffrey E. Hinton and Ronald J. Williams, Learning representations by back-propagating errors, Nature 323, 1986
    locator: pages 533 to 536 (the momentum term in the weight update)
  - paper: doi:10.23915/distill.00006
    title: Gabriel Goh, Why momentum really works, Distill, 2017
    locator: the analysis of momentum on quadratics through the eigenvalues of the two-step iteration
---

The momentum method, or heavy ball method, adds to each [gradient descent](/gradient-descent/) step a fixed fraction $\beta$ of the previous step: $x_{k+1} = x_k - \alpha\nabla f(x_k) + \beta(x_k - x_{k-1})$. On a quadratic whose Hessian has eigenvalues in $[\mu, L_f]$, the tuned values $\alpha = 4/(\sqrt{L_f} + \sqrt{\mu})^2$ and $\beta = \left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^2$ make the error fall like $\left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^k$, so the number of steps grows like $\sqrt\kappa$ in place of $\kappa$, which matches the [first-order lower bound](/first-order-lower-bound/). The same tuned values can fail on non-quadratic strongly convex functions, where the iterates may cycle. With smaller steps the method converges on every smooth convex function, and in stochastic form it is the default optimizer for training neural networks.

## In plain words

Picture a heavy ball rolling down a valley. Plain gradient descent is a ball with no mass: at each moment it moves only in the direction of the slope where it stands, so in a long narrow valley it bounces from wall to wall and moves slowly along the floor.

A heavy ball keeps part of its speed from one moment to the next. The pushes across the valley change sign at each step and mostly cancel, while the pushes along the valley floor point the same way each time and add up. So the ball builds speed in the useful direction and damps the zigzag.

The two settings are the size of the push from the slope and how much speed is kept. The right choice depends on how steep and how flat the valley is.

## The problem

The input is the gradient $\nabla f$ of a differentiable $f : \mathbb{R}^n \to \mathbb{R}$, a start $x_0$, a step $\alpha > 0$, a momentum $\beta \in [0, 1)$ and a number of iterations $K$ (or a tolerance on $\|\nabla f\|$). The output is the last iterate. The guarantees below need $f$ to be $L_f$-[smooth](/smoothness/), and convex or quadratic. All arithmetic is in floating point; the tests compare with a relative tolerance of $10^{-9}$.

## The algorithm

```pseudo id=main
HEAVY-BALL(∇f, x₀, α, β, K)
L1  x_prev ← x₀;  x ← x₀                         ▷ so the first step is a gradient step
L2  for k ← 0 to K − 1 do
L3      g ← ∇f(x)
L4      x_next ← x − α g + β (x − x_prev)
L5      (x_prev, x) ← (x, x_next)
L6  return x
```

Line L4 is the whole method: a gradient step from $x$ plus the momentum term $\beta(x_k - x_{k-1})$. With $v_k = x_k - x_{k-1}$ it reads $v_{k+1} = \beta v_k - \alpha\nabla f(x_k)$, $x_{k+1} = x_k + v_{k+1}$, $v_0 = 0$: the velocity is an exponentially weighted sum of past gradients. With $\beta = 0$ it is gradient descent. For a quadratic with known $\mu$ and $L_f$, take

$$\alpha = \frac{4}{(\sqrt{L_f} + \sqrt\mu)^2}, \qquad \beta = \rho^2, \qquad \rho = \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}, \qquad \kappa = \frac{L_f}{\mu}.$$

## Example

Take $f(x) = \frac12(x_1^2 + 10x_2^2)$, so $\mu = 1$, $L_f = 10$, $\kappa = 10$, and start at $x_0 = (10, 1)$. The tuned values are $\alpha = 4/(\sqrt{10} + 1)^2 = 0.2309$ and $\beta = 0.2699$, with $\rho = 0.5195$.

| $k$ | $x_k$ | $f(x_k)$ |
|---|---|---|
| 0 | $(10, 1)$ | $55$ |
| 1 | $(7.6911, -1.3089)$ | $38.14$ |
| 2 | $(5.2923, 1.0900)$ | $19.94$ |
| 3 | $(3.4230, -0.7793)$ | $8.89$ |
| 4 | $(2.1282, 0.5155)$ | $3.59$ |

The second coordinate still changes sign, but its size shrinks faster than under gradient descent, and the first coordinate moves faster because the momentum adds up along it. The gradient norm falls below $10^{-6}$ after $31$ steps, against $83$ for gradient descent with step $2/(\mu + L_f)$ and $153$ with step $1/L_f$. For $\kappa = 1000$ ($f = \frac12(x_1^2 + 1000x_2^2)$, same start) the counts are $435$ for the heavy ball, $10362$ and $16111$ for the two gradient steps: the ratio grows like $\sqrt\kappa$.

## Correctness

The proofs are in the correctness proof of this page. Write $R = \|x_0 - x^*\|$.

1. **Quadratics with the tuned values.** Let $f(x) = \frac12(x - x^*)^\top A(x - x^*) + f^*$ with the eigenvalues of $A$ in $[\mu, L_f]$, $\mu > 0$, and take the tuned $\alpha$ and $\beta$. Then for every $k \ge 0$,

$$\|x_k - x^*\| \le \left(1 + (1 + \rho)k\right)\rho^kR, \qquad \rho = \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}.$$

*Reason:* in each eigendirection the error obeys $e_{k+1} = (1 + \beta - \alpha\lambda)e_k - \beta e_{k-1}$. The tuned values make $|1 + \beta - \alpha\lambda| \le 2\rho$ for every $\lambda \in [\mu, L_f]$, so both roots of $z^2 - (1 + \beta - \alpha\lambda)z + \beta$ have modulus $\rho$, and the solution is $\rho^k$ times a combination of Chebyshev polynomials bounded by $1 + (1 + \rho)k$.

2. **Convex functions, averaged iterate.** Let $f$ be convex and $L_f$-smooth with a minimizer $x^*$, $\beta \in [0, 1)$ and $0 < \alpha \le (1 - \beta)/L_f$. Then for $\bar{x}_T = \frac{1}{T + 1}\sum_{k=0}^Tx_k$,

$$f(\bar{x}_T) - f^* \le \frac{1}{T + 1}\left(\frac{(1 - \beta)R^2}{2\alpha} + \frac{\beta}{1 - \beta}(f(x_0) - f^*)\right),$$

and the same bound holds for $\min_{k \le T}f(x_k) - f^*$ (Ghadimi, Feyzmahdavian and Johansson, 2015). *Reason:* the points $z_k = x_k + \frac{\beta}{1 - \beta}(x_k - x_{k-1})$ satisfy $z_{k+1} = z_k - \frac{\alpha}{1 - \beta}\nabla f(x_k)$, and the gradient descent argument applies to them.

3. **No global acceleration with the tuned values.** Claim 1 is about quadratics. Lessard, Recht and Packard (2016) give a one-dimensional function with $\mu = 1$ and $L_f = 25$ on which the heavy ball method with the tuned values $\alpha = 1/9$, $\beta = 4/9$ does not converge from some starts (see Pitfalls). Polyak (1964) proved that for a twice continuously differentiable $f$ whose Hessian at $x^*$ has eigenvalues in $[\mu, L_f]$, the method with the tuned values converges locally with a rate close to $\rho$.

## Complexity

Each iteration costs one gradient and $O(n)$ arithmetic, and the method stores two vectors, $x$ and $x_{\text{prev}}$, so the extra space is $O(n)$.

**Quadratics.** By claim 1, the error is at most $\varepsilon R$ once $(1 + 2k)\rho^k \le \varepsilon$. Since $\ln(1/\rho) \ge 2/\sqrt\kappa$, this needs $O(\sqrt\kappa\log(1/\varepsilon))$ iterations, against $O(\kappa\log(1/\varepsilon))$ for gradient descent. This matches the lower bound for first-order methods on quadratics up to a constant factor.

**Convex functions.** By claim 2 with $\alpha = (1 - \beta)/L_f$ and a fixed $\beta$, the averaged iterate reaches accuracy $\varepsilon$ after $O(L_fR^2/\varepsilon)$ iterations, the same order as gradient descent; the guarantee shows no acceleration.

| setting | iterations to accuracy $\varepsilon$ |
|---|---|
| quadratic, tuned $\alpha, \beta$ | $O(\sqrt\kappa\log(1/\varepsilon))$ |
| convex $L_f$-smooth, $\alpha \le (1 - \beta)/L_f$ | $O(L_fR^2/\varepsilon)$ |
| strongly convex, tuned $\alpha, \beta$ | may not converge |

## Properties

- **Not a descent method.** The values $f(x_k)$ need not decrease, even on quadratics: the ball can roll up the other side of the valley.
- **Two-step recurrence.** The new point depends on the last two points, so the state is $(x_k, x_{k-1})$ and the error obeys a linear recurrence of order two on quadratics.
- **Optimal on quadratics.** The tuned values give the same asymptotic factor $\rho$ as the [Chebyshev iteration](/chebyshev-iteration/) and the [conjugate gradient method](/conjugate-gradient-method/) on quadratics, and both of these are known to be optimal there.
- **Sensitive to the spectrum bounds.** If the true smallest eigenvalue is below the $\mu$ used for tuning, the components along it still converge but more slowly than $\rho^k$. If the true largest eigenvalue is far above the $L_f$ used for tuning, the components along it can grow.

## Variants and improvements

- **[Nesterov's accelerated gradient](/nesterov-accelerated-gradient/)** evaluates the gradient at the extrapolated point $x_k + \beta(x_k - x_{k-1})$ in place of $x_k$. This small change gives a proven accelerated rate for every smooth convex or strongly convex function, which the heavy ball method lacks.
- **Stochastic momentum.** In [stochastic gradient descent](/stochastic-gradient-descent/) for neural networks, the velocity form with a stochastic gradient and $\beta \approx 0.9$ is the standard optimizer. [Adam](/adam/) combines a momentum average of gradients with per-coordinate scaling.
- **Conservative parameters.** With $\alpha \le (1 - \beta)/L_f$ the method converges on every smooth convex function (claim 2), and Ghadimi, Feyzmahdavian and Johansson also prove a linear rate for strongly convex functions under a step condition.
- **Restart.** Resetting $x_{\text{prev}} \leftarrow x$ when $f$ increases removes the overshoot and is a common safeguard.

## When to use it

Use the heavy ball method with tuned values on quadratic problems, or on problems that are nearly quadratic near the solution, when $\mu$ and $L_f$ are known well, for example as a cheap alternative to the conjugate gradient method that needs no inner products. In stochastic training, momentum is the default because it averages noise and speeds progress along flat directions. For general smooth convex problems with a guarantee, use [Nesterov's method](/nesterov-accelerated-gradient/) in place of the heavy ball.

## Pitfalls

- **Tuned values on a non-quadratic function.** Lessard, Recht and Packard define $f$ on $\mathbb{R}$ by $\nabla f(x) = 25x$ for $x < 1$, $x + 24$ for $1 \le x < 2$ and $25x - 24$ for $x \ge 2$, which is $1$-strongly convex and $25$-smooth with $f^* = 0$ at $0$. With $\alpha = 1/9$, $\beta = 4/9$ and $x_0 = 3.3$, the iterates of the implementation end in a cycle through about $2.1159$, $-1.8024$ and $0.6465$ and never converge. From $x_0 = 0.5$, inside the quadratic piece, they converge.
- **Wrong spectrum bounds.** Claim 1 needs every eigenvalue of $A$ in $[\mu, L_f]$. A $\mu$ that is too large slows the flat directions, and an $L_f$ that is much too small makes the steep directions grow. When in doubt, overestimate $L_f$ and underestimate $\mu$.
- **Assuming monotone decrease.** Do not use a decrease of $f$ as a stopping test or a line search criterion on the heavy ball iterates without a restart rule.
- **Confusing the two momenta.** "Nesterov momentum" in deep learning libraries is the variant that evaluates the gradient at the look-ahead point; it is a different method with a different theory.

## Implementations

The Python module has the method in position form with an optional gradient tolerance, the velocity form, and the tuned parameters for a quadratic.

## History

Boris Polyak introduced the heavy ball method in 1964, with the tuned parameters and a proof of the accelerated local rate, as one of several ways to speed up gradient iterations; the name comes from the equation of a heavy ball moving with friction in a potential field. Rumelhart, Hinton and Williams used a momentum term in back-propagation in 1986, and it has been standard in neural network training since then. Lessard, Recht and Packard showed in 2016 that the tuned method can fail to converge on strongly convex functions that are not quadratic, and Ghadimi, Feyzmahdavian and Johansson gave global guarantees for smaller steps in 2015.

## References
