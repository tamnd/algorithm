---
tag: CHE5ZR
kind: algorithm
slug: dual-ascent
name: Dual ascent
aliases:
- Uzawa's method
- dual gradient ascent
- dual gradient method
area: optimization/convex-optimization
level: advanced
summary: Maximize the dual function by gradient or subgradient steps on the multipliers.
solves: [quadratic-programming]
model: real-ram
complexity:
  vars: {k: the number of iterations, m: the number of constraints, n: the number of variables, s: the cost of one minimization of the Lagrangian}
  time: {worst: O(k (s + m n))}
  space: {extra: O(m + n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1958
  people: [Kenneth Arrow, Leonid Hurwicz, Hirofumi Uzawa]
  note: Arrow, Hurwicz and Uzawa studied gradient methods on the Lagrangian in 1958, and the dual gradient step is often called Uzawa's method. Everett showed in 1963 how to use Lagrange multipliers to allocate resources.
prereqs: [lagrangian-duality, gradient-descent, strong-convexity]
see_also: [augmented-lagrangian-method, dual-decomposition, admm, projected-gradient-descent, lagrangian-relaxation, network-utility-maximization, subgradient, kkt-conditions]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Chapter 5 (the Lagrange dual function, weak and strong duality, Section 5.2.3 on the Slater condition for affine constraints)
  - paper: doi:10.1561/2200000016
    title: Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato and Jonathan Eckstein, Distributed optimization and statistical learning via the alternating direction method of multipliers, Foundations and Trends in Machine Learning 3(1), 2011
    locator: Section 2.1 (dual ascent), Section 2.2 (dual decomposition)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 12 (dual-based proximal gradient methods, with the rate of the primal sequence)
  - paper: doi:10.1007/s10107-004-0552-5
    title: Yurii Nesterov, Smooth minimization of non-smooth functions, Mathematical Programming 103, 2005
    locator: pages 127 to 152 (the dual of a strongly convex problem has a Lipschitz gradient with constant the squared operator norm over the convexity parameter)
  - paper: doi:10.1287/opre.11.3.399
    title: Hugh Everett III, Generalized Lagrange multiplier method for solving problems of optimum allocation of resources, Operations Research 11(3), 1963
    locator: pages 399 to 417
---

Dual ascent solves a constrained convex problem $\min f(x)$ subject to $Ax = b$ (or $Ax \le b$) by working on the Lagrange multipliers $y$. At each step it minimizes the [Lagrangian](/lagrangian-function/) $f(x) + y^\top(Ax - b)$ over $x$ with no constraints, measures the constraint violation $Ax - b$, and moves $y$ a step in that direction. The violation is the gradient of the dual function $d(y)$, so the method is gradient ascent on the dual. If $f$ is $\mu$-strongly convex, the dual gradient is Lipschitz with constant $\|A\|^2/\mu$, and with the step $\alpha = \mu/\|A\|^2$ the dual gap after $k$ steps is at most $\|A\|^2\|y_0 - y^*\|^2/(2\mu k)$. The main use is [dual decomposition](/dual-decomposition/): when $f$ is a sum of terms in separate variables, the minimization of the Lagrangian splits into small independent problems.

## In plain words

A planner has to share a fixed amount of a resource among many users. She does not tell each user what to take. She sets a price, each user picks what is best for them at that price, and she adds up the demand. If the total demand is more than the supply, she raises the price. If it is less, she lowers it. She changes the price in proportion to the excess. When the price is right, demand meets supply, and each user's choice is part of the best overall plan. Each round needs only the total demand, so the users can decide on their own. The method needs each user to have one clear best choice at each price. Otherwise the demand jumps when the price changes a little, and the price does not settle.

## The problem

Minimize $f(x)$ subject to $a_i^\top x = b_i$ for $i \notin I$ and $a_i^\top x \le b_i$ for $i \in I$, where $A \in \mathbb{R}^{m \times n}$ has rows $a_i^\top$. The assumptions are:

- $f: \mathbb{R}^n \to \mathbb{R}$ is $\mu$-[strongly convex](/strong-convexity/) with a known $\mu > 0$;
- the problem is feasible;
- there is a way to compute $x(y) = \operatorname{argmin}_x f(x) + y^\top(Ax - b)$ for each $y$.

The multipliers live in $Y = \{y : y_i \ge 0 \text{ for } i \in I\}$, and the dual function is $d(y) = \min_x f(x) + y^\top(Ax - b)$. Under these assumptions the problem has a unique solution $x^*$, strong duality holds, and a dual solution $y^* \in Y$ exists. The input is a solver for $x(y)$, $A$, $b$, $I$, a start $y_0 \in Y$, a step $\alpha$ and a tolerance $\varepsilon$.

## The algorithm

```pseudo id=main
DUAL-ASCENT(f, A, b, I, y, α, ε)
L1  repeat
L2      x ← argmin_x f(x) + yᵀ(Ax − b)
L3      g ← Ax − b                          ▷ the gradient of d at y
L4      y⁺ ← y + α g;  y⁺ᵢ ← max(0, y⁺ᵢ) for each i ∈ I
L5      if ‖y⁺ − y‖ ≤ α ε then return x, y
L6      y ← y⁺
```

Line L4 is a projected gradient step on the dual. Equality rows move freely. Inequality rows move and are then cut at zero, because a multiplier for $a_i^\top x \le b_i$ must not be negative. The pair $(x, y)$ that the method returns satisfies $d(y) = f(x) + y^\top(Ax - b)$, so the dual value, which is a lower bound on the optimum, is known at each step.

A safe step is $\alpha = \mu/\|A\|_F^2$, where $\|A\|_F^2$ is the sum of the squares of the entries of $A$. It is at most $\mu/\|A\|^2$, because the spectral norm is at most the Frobenius norm.

For a quadratic $f(x) = \tfrac12 x^\top Qx + c^\top x$ with $Q$ positive definite, line L2 is the linear system $Qx = -c - A^\top y$, and $\mu$ is the smallest eigenvalue of $Q$ or any positive lower bound on it.

## Example

Minimize $\tfrac12 x_1^2 + x_2^2$ subject to $x_1 + x_2 = 3$. The answer is $x^* = (2, 1)$ with $f^* = 3$ and $y^* = -2$. Here $\mu = 1$ and $\|A\|_F^2 = 2$, so $\alpha = \tfrac12$. Line L2 gives $x(y) = (-y, -y/2)$, line L3 gives $g = -\tfrac32 y - 3$, and line L4 gives $y^+ + 2 = (y + 2)/4$. From $y_0 = 0$, in exact arithmetic:

| $k$ | $y_k$ | $x_k$ | $g_k$ | $f(x_k)$ | $d(y_k)$ |
|---|---|---|---|---|---|
| 0 | 0 | (0, 0) | -3 | 0 | 0 |
| 1 | -3/2 | (3/2, 3/4) | -3/4 | 27/16 | 45/16 |
| 2 | -15/8 | (15/8, 15/16) | -3/16 | 675/256 | 765/256 |
| 3 | -63/32 | (63/32, 63/64) | -3/64 | 11907/4096 | 12285/4096 |
| $k$ | $-2 + 2 \cdot 4^{-k}$ | $(1 - 4^{-k})(2, 1)$ | $-3 \cdot 4^{-k}$ | $3(1 - 4^{-k})^2$ | $3(1 - 16^{-k})$ |

The primal points are infeasible, $x_1 + x_2 < 3$, and $f(x_k) < f^*$, so $f(x_k)$ alone says little. The dual values rise to $f^* = 3$ and are lower bounds at each step. The proved bound is $d^* - d(y_k) \le 4/k$. The true gap $3 \cdot 16^{-k}$ falls much faster, because here the dual is a strongly concave quadratic.

## Correctness

Because $f$ is strongly convex, $x(y)$ is unique and $d$ is differentiable with gradient $Ax(y) - b$. The minimizer moves at most $\|A\|/\mu$ times as far as $y$ does, so this gradient is Lipschitz with constant $\Lambda = \|A\|^2/\mu$. Dual ascent is then projected gradient ascent on a concave function with a $\Lambda$-Lipschitz gradient, with a step $\alpha \le 1/\Lambda$. The standard analysis of that method gives the dual rate: each step does not lower $d$ and does not move $y$ away from $y^*$. A second fact turns the dual gap into a primal error: $\tfrac{\mu}{2}\|x_k - x^*\|^2 \le d^* - d(y_k)$. The full proof is below.

## Complexity

**Iterations.** Under the assumptions of the problem statement, with $0 < \alpha \le \mu/\|A\|^2$ and $y_0 \in Y$, for each $k \ge 1$:

$$d^* - d(y_k) \le \frac{\|y_0 - y^*\|^2}{2\alpha k}, \qquad \|x_k - x^*\|^2 \le \frac{2\,(d^* - d(y_k))}{\mu} \le \frac{\|y_0 - y^*\|^2}{\alpha\mu k}.$$

With $\alpha = \mu/\|A\|^2$, a dual gap of $\varepsilon$ takes at most $\|A\|^2\|y_0 - y^*\|^2/(2\mu\varepsilon)$ steps, and the primal error falls like $1/\sqrt{k}$. If there are only equality rows, $A$ has full row rank and $f$ has an $L$-Lipschitz gradient, then $d$ is strongly concave with parameter $\sigma_{\min}(A)^2/L$, and the rate becomes linear. [Nesterov's acceleration](/nesterov-accelerated-gradient/) on the dual improves the sublinear rate to $O(1/k^2)$.

**One iteration.** One minimization of the Lagrangian in line L2, plus $O(mn)$ for $Ax$ and the update. For a quadratic $f$, one solve with $Q$, which is $O(n^2)$ after one $O(n^3)$ factorization. If $f = \sum_j f_j(x_j)$ is separable, line L2 splits into one small problem per block, and these can run in parallel.

## Properties

- **A lower bound at each step.** $d(y_k) = f(x_k) + y_k^\top(Ax_k - b) \le f^*$.
- **Monotone.** With $\alpha \le 1/\Lambda$, $d(y_k)$ does not decrease and $\|y_k - y^*\|$ does not increase.
- **Infeasible primal points.** The iterates $x_k$ do not satisfy the constraints until the limit, so $f(x_k)$ can be below $f^*$.
- **Separable.** The constraints enter line L2 only through the linear term $A^\top y$, so a separable $f$ gives a separable subproblem.
- **Needs strong convexity.** Without it, $x(y)$ can be non-unique or missing, and $d$ is not differentiable.

## Variants and improvements

- **Dual subgradient method.** If $f$ is only convex, $Ax(y) - b$ is still a [subgradient](/subgradient/) of $-d$ for any minimizer $x(y)$. With bounded subgradients and suitable step sizes, the best dual value seen so far converges at the rate $O(1/\sqrt{k})$. This is the method of [Lagrangian relaxation](/lagrangian-relaxation/) in integer programming.
- **[Augmented Lagrangian method](/augmented-lagrangian-method/).** Add $\tfrac\rho2\|Ax - b\|^2$ to the Lagrangian and use the step $\rho$. Then strong convexity is not needed, but separability is lost.
- **[ADMM](/admm/).** Keeps the robustness of the augmented Lagrangian and gets back the splitting for two blocks.
- **Accelerated dual ascent.** A Nesterov step on $d$ gives $d^* - d(y_k) = O(\Lambda\|y_0 - y^*\|^2/k^2)$.
- **Primal averaging.** For the subgradient version, under suitable step rules the running averages of the $x_k$ approach the primal solutions even when the $x_k$ themselves do not.

## When to use it

Use dual ascent when $f$ is strongly convex and separable and the coupling constraints are few: for example resource sharing, [network utility maximization](/network-utility-maximization/) and rate control, where the prices $y$ are sent to the users and the users solve their own small problems. It is easy to distribute. Do not use it for problems with a linear or otherwise non-strictly-convex objective. For those, use the [augmented Lagrangian method](/augmented-lagrangian-method/) or [ADMM](/admm/). For high accuracy on a single machine, a Newton-type method such as an [interior-point method](/interior-point-method/) is usually much faster.

## Pitfalls

- **Too large a step.** With $\alpha > 2/\Lambda$ the method can diverge, even on a quadratic dual. Using $\|A\|_F$ in place of the spectral norm is safe, but it can make the step much smaller than needed.
- **Unbounded subproblems.** For a linear objective $c^\top x$, the Lagrangian $c^\top x + y^\top(Ax - b)$ is unbounded below unless $c + A^\top y = 0$. Then line L2 has no answer for almost every $y$.
- **Wrong sign of the projection.** For a constraint $a_i^\top x \le b_i$, the multiplier must stay at or above zero. For $a_i^\top x \ge b_i$, write it as $-a_i^\top x \le -b_i$ first.
- **Stopping on $f(x_k)$.** The primal value can be below $f^*$ because $x_k$ is not feasible. Stop on the size of the violation and on the gap $f(x_k) - d(y_k) = -y_k^\top(Ax_k - b)$, and if a feasible point is needed, repair $x_k$.

## Implementations

## History

Arrow, Hurwicz and Uzawa (1958) studied gradient methods that move the primal and dual variables of a Lagrangian, and the version that minimizes over $x$ and takes a gradient step in $y$ is often called Uzawa's method. Everett (1963) showed that Lagrange multipliers solve resource allocation problems: for each price, the minimizer of the Lagrangian is optimal for the amount of resource it uses. Dantzig and Wolfe (1960) and Benders (1962) built decomposition methods on the same duality, and Held and Karp (1970 and 1971) used subgradient steps on a Lagrangian dual to get bounds for the traveling salesman problem. Since the 1990s, dual ascent has been the model for pricing in communication networks and for distributed optimization.

## References
