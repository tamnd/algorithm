---
tag: KTPH6E
kind: algorithm
slug: fista
name: FISTA
aliases:
- accelerated proximal gradient
- fast iterative shrinkage-thresholding algorithm
- accelerated proximal gradient method
area: optimization/gradient-methods
level: advanced
summary: Accelerated proximal gradient method with an O(1/k^2) rate for composite convex objectives.
solves: [composite-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, g: "the cost of one gradient of f plus one prox of h", ε: "the target accuracy F(x_k) - F* ≤ ε", R: "the distance from x_0 to a minimizer", β: "the smoothness constant L_f of f (the step is 1/L_f)"}
  time: {worst: O(k (g + n))}
  space: {extra: Θ(n)}
  steps: {worst: "⌈(2 β R^2 / ε)^(1/2)⌉"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [Amir Beck, Marc Teboulle, Yurii Nesterov]
  note: Beck and Teboulle (2009) added Nesterov's 1983 momentum to the proximal gradient method and proved the O(1/k^2) rate.
prereqs: [proximal-gradient-method, nesterov-accelerated-gradient]
see_also: [composite-minimization, first-order-lower-bound, momentum-method, lasso-regression, proximal-operator, projected-gradient-descent, convergence-rate]
sources:
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009
    locator: Section 4, Theorem 4.4 (the O(1/k^2) rate of FISTA with a constant step or with backtracking)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 10, Section 10.7 (the fast proximal gradient method, FISTA, and its analysis)
  - paper: "Yurii Nesterov, A method of solving a convex programming problem with convergence rate O(1/k^2), Soviet Mathematics Doklady 27(2), 1983, pages 372 to 376"
    locator: the accelerated gradient method for smooth convex functions
  - paper: doi:10.1007/s10957-015-0746-4
    title: Antonin Chambolle and Charles Dossal, On the convergence of the iterates of the fast iterative shrinkage/thresholding algorithm, Journal of Optimization Theory and Applications 166(3), 2015
    locator: pages 968 to 982, convergence of the iterates for t_k = (k + a - 1)/a with a > 2
  - paper: doi:10.1007/s10208-013-9150-3
    title: Brendan O'Donoghue and Emmanuel Candès, Adaptive restart for accelerated gradient schemes, Foundations of Computational Mathematics 15(3), 2015
    locator: pages 715 to 732, the function and gradient restart tests
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 5.1 (sum of a smooth and a simple non-smooth term, FISTA)
---

FISTA (fast iterative shrinkage-thresholding algorithm) is the [proximal gradient method](/proximal-gradient-method/) with a momentum step in the style of [Nesterov's accelerated gradient](/nesterov-accelerated-gradient/). It minimizes $F = f + h$, with $f$ convex and $L_f$-smooth and $h$ convex with a cheap [proximal operator](/proximal-operator/). With the step $1/L_f$ it reaches $F(x_k) - F^* \le 2L_f\lVert x_0 - x^*\rVert^2/(k+1)^2$, which matches the [first-order lower bound](/first-order-lower-bound/) up to a constant. The cost of each iteration is the same as for the plain method: one gradient and one prox.

## In plain words

The plain proximal gradient method takes each step from the point where the last step ended. FISTA takes each step from a point a little further along the direction of the last move, as a ball that rolls downhill keeps some speed. The extra push grows over time by a fixed rule.

This simple change makes the method much faster on hard problems. To halve the error, the plain method may need twice as many steps, while FISTA needs only about 1.4 times as many. The price is that the objective no longer goes down at every step: the method can overshoot and come back.

## The problem

The input is a [composite minimization](/composite-minimization/) problem: minimize $F(x) = f(x) + h(x)$ over $\mathbb{R}^n$, where $f$ is convex and differentiable with an $L_f$-Lipschitz gradient ([smoothness](/smoothness/)), and $h$ is proper, closed and convex, with an oracle for $\operatorname{prox}_{th}$. A minimizer $x^*$ exists. Notation: $F^* = F(x^*)$, $R = \lVert x_0 - x^*\rVert$, $L$ is the constant used in the step (any $L \ge L_f$), $n$ is the number of variables, and $\varepsilon$ is the target accuracy for $F(x_k) - F^*$.

## The algorithm

```pseudo id=main
FISTA(∇f, prox_h, x₀, L, K)                  ▷ L ≥ L_f
L1  y ← x₀, x_prev ← x₀, τ ← 1               ▷ y₁ = x₀, t₁ = 1
L2  for k ← 1 to K do
L3      x_k ← prox_{h/L}(y − ∇f(y)/L)         ▷ one proximal gradient step from y
L4      τ' ← (1 + √(1 + 4τ²)) / 2
L5      y ← x_k + ((τ − 1)/τ') (x_k − x_prev) ▷ momentum
L6      x_prev ← x_k, τ ← τ'
L7  return x_K
```

Line L3 is the step of the proximal gradient method, taken at the extrapolated point $y$ instead of at $x_{k-1}$. The momentum weight $(t_k - 1)/t_{k+1}$ starts at $0$, and it is close to $1 - 3/k$ for large $k$. The sequence $t_k$ satisfies $t_{k+1}^2 - t_{k+1} = t_k^2$ and $t_k \ge (k+1)/2$. A common simpler choice is $t_k = (k+1)/2$, which gives the weight $(k-1)/(k+2)$ and the same rate.

## Example

Take the lasso of the proximal gradient page: $A = \begin{pmatrix} 2 & 0 \\ 1 & 1\end{pmatrix}$, $b = (2, 0.5)$, $\lambda = 1$, $L = 6$, $x_0 = (0, 0)$. The solution is $x^* = (0.7, 0)$ with $F^* = 0.9$, and $R^2 = 0.49$.

| $k$ | $x_k$ | $t_k$ | $F(x_k) - F^*$ | bound $2LR^2/(k+1)^2$ |
|---|---|---|---|---|
| 1 | (0.58333, 0) | 1 | 3.40e-2 | 1.47 |
| 2 | (0.68056, 0) | 1.618 | 9.45e-4 | 0.653 |
| 3 | (0.70132, 0) | 2.194 | 4.39e-6 | 0.3675 |
| 4 | (0.70172, 0) | 2.750 | 7.42e-6 | 0.2352 |
| 5 | (0.70032, 0) | 3.295 | 2.60e-7 | 0.1633 |

The first two steps equal those of the plain method, because the first momentum weight is $0$. At $k = 3$ the momentum carries the first entry past $0.7$, and at $k = 4$ the gap goes up, from $4.39 \cdot 10^{-6}$ to $7.42 \cdot 10^{-6}$. This is the overshoot that the bound allows. On this easy problem the plain method is as fast, because the problem is strongly convex once the zero entry is fixed. The gain of FISTA shows on badly conditioned problems: on $f(x) = 50x_1^2 + \frac{1}{2}x_2^2$ with $L = 100$ from $(1, 1)$, plain gradient descent still has $f(x_{40}) = 0.5 \cdot 0.99^{80} \approx 0.22$, while FISTA has $f(x_{37}) < 10^{-4}$.

## Correctness

The proof uses an energy $E_k = t_k^2(F(x_k) - F^*) + \frac{L}{2}\lVert u_k\rVert^2$ with $u_k = t_k x_k - (t_k - 1)x_{k-1} - x^*$. Two instances of the one-step inequality of the proximal gradient method, at the point $y_{k+1}$ and compared with $x_k$ and with $x^*$, combine with weights $t_{k+1} - 1$ and $1$. The identity $t_{k+1}^2 - t_{k+1} = t_k^2$ is exactly what makes the result telescope to $E_{k+1} \le E_k$. Then $t_k^2(F(x_k) - F^*) \le E_1 \le \frac{L}{2}R^2$, and $t_k \ge (k+1)/2$ gives the rate. The full proof is below.

## Complexity

Each iteration costs one gradient of $f$, one prox of $h$ and $O(n)$ vector work, the same as the plain method. The memory is $\Theta(n)$: the method keeps $x_k$, $x_{k-1}$ and $y$.

- **Rate.** $F(x_k) - F^* \le 2L_f R^2/(k+1)^2$ with $L = L_f$. So $\lceil \sqrt{2L_f R^2/\varepsilon}\,\rceil$ iterations give accuracy $\varepsilon$. This is a sublinear rate, $O(1/k^2)$, against $O(1/k)$ for the plain method.
- **Optimality.** For $h = 0$ and $k \le (n-1)/2$, every method whose iterates lie in the span of past gradients has a function $f$ with $f(x_k) - f^* \ge 3L_fR^2/(32(k+1)^2)$ ([first-order lower bound](/first-order-lower-bound/)). The two bounds differ by a constant factor.
- **Strongly convex $f$.** The plain FISTA rate stays $O(1/k^2)$. The version with the constant momentum weight $(\sqrt{\kappa} - 1)/(\sqrt{\kappa} + 1)$, which needs $\mu$, contracts by $1 - 1/\sqrt{\kappa}$ in each step, against $1 - 1/\kappa$ for the plain method.

## Properties

- **Not monotone.** $F(x_k)$ can go up, as in the example. Only the energy $E_k$ decreases.
- **Same oracle as ISTA.** No extra gradient or prox per step.
- **Iterates.** The proof bounds function values only. With the sequence $t_k = (k + a - 1)/a$ for $a > 2$, the iterates converge to a minimizer (Chambolle and Dossal 2015).
- **Deterministic.** The method has no random choice.

## Variants and improvements

- **Backtracking.** If $L_f$ is unknown, find $L$ at each step by backtracking, with $L$ never decreasing. The rate becomes $2\eta L_f R^2/(k+1)^2$ for the increase factor $\eta$ (Beck and Teboulle 2009, Theorem 4.4).
- **MFISTA.** A monotone version keeps the better of the new prox point and the old iterate. It has the same rate.
- **Restart.** Reset $t_k$ to $1$ when $F$ goes up, or when the momentum points uphill (O'Donoghue and Candès 2015). In practice this recovers a linear rate on strongly convex problems without knowing $\mu$.
- **Constant momentum for strongly convex $f$.** Use the weight $(\sqrt{\kappa} - 1)/(\sqrt{\kappa} + 1)$ when $\mu$ is known.
- **Projected version.** With $h$ the indicator of a convex set, FISTA is accelerated [projected gradient descent](/projected-gradient-descent/).

## When to use it

Use FISTA for the same problems as the proximal gradient method (lasso, sparse logistic regression, total variation denoising through a dual, nonnegative least squares), when you want many fewer iterations for the same cost per iteration. If you need $F$ to decrease at each step, use MFISTA or a restart. If $f$ is strongly convex and $\kappa$ is known, use the constant-momentum version, or add restarts.

## Pitfalls

- **Momentum from the wrong points.** Line L5 extrapolates from the two last prox points $x_k$ and $x_{k-1}$, not from $y$.
- **Step too long.** As for the plain method, the step must be at most $1/L_f$. With a longer step the energy argument fails and the method can diverge.
- **Stopping when $F$ goes up.** A rise of $F$ is normal and does not mean divergence.
- **Expecting a linear rate.** Without restarts or knowledge of $\mu$, the guarantee stays $O(1/k^2)$ even on strongly convex problems.

## Implementations

## History

Nesterov (1983) introduced the accelerated gradient method for smooth convex functions with the sequence $t_k$ used here. Beck and Teboulle (2009) extended it to the composite problem $f + h$ with a prox step, named it FISTA, and proved the $O(1/k^2)$ rate. Nesterov (2013) gave another accelerated method for composite functions. Chambolle and Dossal (2015) proved that the iterates converge for a slightly modified momentum sequence.

## References
