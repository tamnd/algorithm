---
tag: M2Z5AG
kind: algorithm
slug: bundle-method
name: Bundle method
aliases:
- proximal bundle method
- level bundle method
area: optimization/convex-optimization
level: research
summary: Minimize nonsmooth convex functions using a bundle of past subgradients.
model: real-ram
complexity:
  vars: {k: the number of iterations, n: the dimension, s: the cost of one oracle call}
  time: {worst: O(k (s + n))}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1975
  people: [Claude Lemaréchal, Philip Wolfe, Krzysztof Kiwiel]
  note: Lemaréchal and Wolfe proposed the first bundle methods in 1975 as descent methods for nonsmooth functions. Kiwiel introduced the aggregate subgradient in 1983 and 1985, which allows a bundle of fixed size, and the proximal form became standard in the 1990s.
prereqs: [cutting-plane-method, proximal-point-method, subgradient]
see_also: [cutting-plane-method, proximal-point-method, proximal-operator, lagrangian-relaxation, dual-decomposition, mirror-descent, ellipsoid-method, quadratic-programming]
sources:
  - paper: doi:10.1007/BFb0120700
    title: Claude Lemaréchal, An extension of Davidon methods to non differentiable problems, Mathematical Programming Study 3, 1975
    locator: pages 95 to 109
  - paper: doi:10.1007/BFb0120703
    title: Philip Wolfe, A method of conjugate subgradients for minimizing nondifferentiable functions, Mathematical Programming Study 3, 1975
    locator: pages 145 to 173
  - paper: doi:10.1007/BFb0074500
    title: Krzysztof C. Kiwiel, Methods of Descent for Nondifferentiable Optimization, Lecture Notes in Mathematics 1133, Springer, 1985
    locator: Chapter 2 (aggregate subgradient methods for unconstrained convex minimization)
  - paper: doi:10.1023/A:1004689609425
    title: Krzysztof C. Kiwiel, Efficiency of proximal bundle methods, Journal of Optimization Theory and Applications 104(3), 2000
    locator: pages 589 to 603 (an O(1/eps^3) bound on the number of iterations of the proximal bundle method)
  - paper: doi:10.1007/BF01585555
    title: Claude Lemaréchal, Arkadi Nemirovski and Yurii Nesterov, New variants of bundle methods, Mathematical Programming 69, 1995
    locator: pages 111 to 147 (the level method and its O(1/eps^2) bound)
  - paper: doi:10.1007/s10107-014-0809-6
    title: Welington de Oliveira, Claudia Sagastizábal and Claude Lemaréchal, Convex proximal bundle methods in depth, a unified analysis for inexact oracles, Mathematical Programming 148, 2014
    locator: pages 241 to 277
  - book: isbn:9783540568520
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Convex Analysis and Minimization Algorithms II, Springer, 1993
    locator: Chapter XV (primal forms of bundle methods)
---

A bundle method minimizes a nonsmooth convex function $f$ that is known only through an oracle returning $f(x)$ and one [subgradient](/subgradient/). Like the [cutting-plane method](/cutting-plane-method/), it builds a piecewise linear model of $f$ from the cuts $f(x_i) + g_i^\top(y - x_i)$. Unlike that method, it does not jump to the minimum of the model. It keeps a stability center $c$, the best point so far, and takes as its next trial point the minimizer of the model plus $\tfrac{1}{2t}\|y - c\|^2$, which is a [proximal point step](/proximal-point-method/) on the model. If the trial point lowers $f$ enough, the center moves there (a serious step). If not, the new cut is added to the model, and the next trial point is better (a null step). With an aggregate cut, two cuts are enough, so the subproblem has a closed form and each iteration costs one oracle call and $O(n)$ work. The method stops with a computed certificate of near-optimality.

## In plain words

The cutting-plane method trusts its model everywhere and jumps to the lowest point of the model, which can be very far away and bad. The bundle method trusts its model only near the best point found so far. It looks for a point that is low on the model but not too far from the best point. Then it checks the real function there. If the real value is clearly better, it moves its base to the new point. If not, it keeps its base, learns a new cut from the failed try, and tries again closer to home. Each failed try teaches the model something, so failed tries cannot go on for long. The method also keeps one summary cut that sums up all the old cuts, so its memory stays small.

## The problem

Minimize a convex $f: \mathbb{R}^n \to \mathbb{R}$ that has a minimizer $x^*$. The function is known only through an oracle that returns $f(x)$ and a subgradient $g \in \partial f(x)$ for each query $x$. For the iteration bound we assume that every returned subgradient has $\|g\| \le G$. The input is the oracle, a start $x_0$, a prox parameter $t > 0$, a descent fraction $\kappa \in (0, 1)$ and a tolerance $\varepsilon$. The output is a center $c$ with $f(c) - f(z) \le \varepsilon + \sqrt{\varepsilon/t}\,\|z - c\|$ for every $z$.

## The algorithm

A cut is a pair $(h, g)$ that stands for the affine function $h + g^\top(y - c)$, so $h$ is its value at the center. Write $\phi(h, g) = h - \tfrac t2\|g\|^2$.

```pseudo id=main
PROXIMAL-BUNDLE(oracle, x, t, κ, ε)
L1  (f(x), g) ← oracle(x);  c ← x;  bundle ← {(f(x), g)}
L2  repeat
L3      λ ← the maximizer over [0, 1] of φ(λa + (1 − λ)b), for the cuts a, b in the bundle (λ = 1 if one cut)
L4      (h_a, g_a) ← λa + (1 − λ)b                                ▷ the aggregate cut
L5      y ← c − t g_a;   v ← f(c) − h_a + t‖g_a‖²                 ▷ trial point and predicted decrease
L6      if v ≤ ε then return c
L7      (f(y), g_y) ← oracle(y)
L8      if f(c) − f(y) ≥ κ v then
L9          c ← y;  bundle ← {(f(y), g_y)}                         ▷ serious step
L10     else                                                      ▷ null step
L11         bundle ← {(h_a, g_a), (f(y) + g_yᵀ(c − y), g_y)}
L12 return c
```

Lines L3 to L5 solve the proximal subproblem $\min_y \max(\text{cuts})(y) + \tfrac{1}{2t}\|y - c\|^2$ through its dual. For two cuts $a = (h_1, g_1)$ and $b = (h_2, g_2)$ the dual is a concave quadratic in $\lambda$, and its maximizer is

$$\lambda = \operatorname{clip}_{[0,1]}\Big(\frac{(h_1 - h_2)/t - (g_1 - g_2)^\top g_2}{\|g_1 - g_2\|^2}\Big),$$

with $\lambda = 1$ if $h_1 \ge h_2$ and $\lambda = 0$ otherwise when $g_1 = g_2$. The trial point is $y = c - tg_a$, and the model value there is $h_a - t\|g_a\|^2$, so $v$ is the decrease that the model predicts. The aggregate cut is a convex combination of cuts, so it lies below $f$, and it carries all the information that line L3 used. Replacing all old cuts by it is what keeps the bundle at two cuts.

## Example

Minimize $f(x) = \max(-x, 2x - 3)$ over $\mathbb{R}$, with $x_0 = 4$, $t = 1$ and $\kappa = \tfrac12$. The answer is $x^* = 1$ with $f^* = -1$. At a point where both pieces are equal, the oracle returns the slope $-1$. In exact arithmetic:

| iteration | center $c$ | $f(c)$ | $\lambda$ | $(h_a, g_a)$ | $y$ | $v$ | $f(y)$ | step |
|---|---|---|---|---|---|---|---|---|
| 0 | 4 | 5 | 1 | (5, 2) | 2 | 4 | 1 | serious |
| 1 | 2 | 1 | 1 | (1, 2) | 0 | 4 | 0 | null |
| 2 | 2 | 1 | 2/3 | (0, 1) | 1 | 2 | -1 | serious |
| 3 | 1 | -1 | 1 | (-1, -1) | 2 | 1 | 1 | null |
| 4 | 1 | -1 | 2/3 | (-1, 0) | | 0 | | stop |

In iteration 1, the trial point $0$ lowers $f$ by $1$, less than $\kappa v = 2$, so it is a null step. Its cut $-x$, written at the center $2$, is $(-2, -1)$. The best mix of $(1, 2)$ and $(-2, -1)$ has $\lambda = \tfrac23$, which puts the trial point at the kink $x = 1$. In iteration 4 the aggregate has slope $0$ and no error, so $v = 0$ proves that $c = 1$ is optimal.

## Correctness

Every cut and every aggregate is a convex combination of subgradient cuts, so it lies below $f$. For the aggregate this gives $f(z) \ge f(c) - e + g_a^\top(z - c)$ for all $z$, where $e = f(c) - h_a \ge 0$, and the predicted decrease is $v = e + t\|g_a\|^2$. When $v \le \varepsilon$, both $e$ and $t\|g_a\|^2$ are at most $\varepsilon$, which is the certificate. For termination: each serious step lowers $f(c)$ by more than $\kappa\varepsilon$, so there are finitely many. At a null step the new cut is far above the old model at $y$, by more than $(1 - \kappa)v$, so the dual value of the next subproblem rises by a fixed amount, and $1/W$ grows by at least $(1 - \kappa)^2/(8tG^2)$ per null step, where $W = e + \tfrac t2\|g_a\|^2$ is between $v/2$ and $v$. The full proof is below.

## Complexity

**Iterations.** Under the assumptions of the problem statement, for $\varepsilon > 0$, the method stops after at most

$$\Big(\Big\lfloor\frac{f(x_0) - f^*}{\kappa\varepsilon}\Big\rfloor + 1\Big)\Big(\Big\lceil\frac{16tG^2}{(1 - \kappa)^2\varepsilon}\Big\rceil + 1\Big)$$

iterations, with $f(c) - f^* \le \varepsilon + \sqrt{\varepsilon/t}\,\|x^* - c\|$ at the stop. This is $O(1/\varepsilon^2)$ iterations for a fixed $t$. For the gap $f(c) - f^*$ itself, Kiwiel (2000) proved a bound of $O(1/\varepsilon^3)$ iterations for the proximal bundle method, and the level method of Lemaréchal, Nemirovski and Nesterov (1995) needs $O(G^2D^2/\varepsilon^2)$ iterations on a set of diameter $D$, which is optimal for nonsmooth convex functions. In practice bundle methods with larger bundles converge much faster than these bounds.

**One iteration.** One oracle call and $O(n)$ arithmetic for the two-cut bundle. With a bundle of $p$ cuts, line L3 becomes a quadratic program over the simplex in $p$ variables, and its data is the $p \times p$ Gram matrix of the subgradients, at $O(pn)$ per new cut to update. The space is $O(n)$ for two cuts and $O(pn)$ for $p$ cuts.

## Properties

- **Certificate at each step.** The pair $(e, g_a)$ shows that $g_a$ is an $e$-subgradient at $c$, which bounds $f(c) - f(z)$ for every $z$.
- **Descent.** The center values $f(c)$ never increase, unlike the query points of the cutting-plane method or the subgradient method.
- **Bounded memory.** The aggregate cut lets the method keep any number of cuts from two upward and still converge.
- **Nonsmooth.** Only the oracle is used. No smoothness and no step-size sequence are needed.
- **Sensitive to $t$.** The prox parameter controls the trade-off between trusting the model and staying near the center.

## Variants and improvements

- **Larger bundles.** Keep the last $p$ cuts plus the aggregate. The subproblem is then a small quadratic program, and the model is much better.
- **Adaptive $t$.** Increase $t$ after serious steps with a good agreement between $f$ and the model, and decrease it after many null steps.
- **Level bundle methods.** Project the center onto the level set $\{y : m(y) \le \ell\}$ of the model for a target level $\ell$ between the lower and the upper bound.
- **Inexact oracles.** In [Lagrangian relaxation](/lagrangian-relaxation/) and [dual decomposition](/dual-decomposition/), the oracle solves a subproblem, often only approximately. Bundle methods can handle errors of known size (de Oliveira, Sagastizábal and Lemaréchal, 2014).
- **Second-order bundle methods.** Replace $\tfrac{1}{2t}\|y - c\|^2$ by a quasi-Newton metric, as in the VU-algorithm and variable metric bundle methods.

## When to use it

Use a bundle method to minimize a nonsmooth convex function whose oracle is expensive, for example the dual function of a [Lagrangian relaxation](/lagrangian-relaxation/) in large integer programs, unit commitment and network design, or an eigenvalue function in [semidefinite](/semidefinite-programming/) problems. It needs far fewer oracle calls than the subgradient method, gives a certificate, and does not need a step-size rule. If the function is smooth, gradient methods are simpler. If the dimension is small and the oracle is cheap, the [cutting-plane method](/cutting-plane-method/) or the [ellipsoid method](/ellipsoid-method/) also works.

## Pitfalls

- **Wrong cut values after a serious step.** Cuts are stored relative to the center. When the center moves, either restart the bundle, as above, or shift every stored value $h$ by $g^\top(c_{\text{new}} - c_{\text{old}})$.
- **Too small $\kappa$ or too large $t$.** The method stays correct, but it makes serious steps that gain little or many null steps far from the center.
- **Stopping on the step length.** A short step $\|y - c\|$ alone is not a certificate. Stop on $v$, which also includes the error $e$.
- **Unbounded below.** If $f$ has no minimizer, serious steps go on forever and $\|g_a\|$ need not become small. Bound the variables if needed.

## Implementations

## History

Lemaréchal (1975) and Wolfe (1975) proposed the first bundle methods, as extensions of conjugate gradient and quasi-Newton ideas to nonsmooth functions. Kiwiel (1983 and 1985) introduced the aggregate subgradient, which allows a bundle of fixed size with full convergence theory. In the late 1980s and the 1990s, Kiwiel, Lemaréchal, Schramm and Zowe, and others developed the proximal and trust-region forms. Lemaréchal, Nemirovski and Nesterov (1995) gave the level method with an optimal complexity bound, and Kiwiel (2000) bounded the number of iterations of the proximal bundle method. Bundle methods became a standard tool for Lagrangian relaxation in large-scale integer programming.

## References
