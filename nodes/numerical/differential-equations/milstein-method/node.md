---
tag: C27YYP
kind: algorithm
slug: milstein-method
name: Milstein method
aliases:
- Milstein scheme
- Mil'shtein method
area: numerical/differential-equations
level: advanced
summary: "For dX = a dt + b dW, step X + a h + b dW + (1/2) b b' (dW^2 - h). The correction term raises the strong order from 1/2 (Euler-Maruyama) to 1; weak order stays 1."
solves: [stochastic-differential-equation]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", d: "the dimension of X", C: "the cost of evaluating a, b and b' once", M: "the number of sample paths"}
  time: {worst: "Θ(M N (C + d))"}
  space: {extra: "Θ(d)"}
  evaluations: {worst: "3 M N"}
properties: {deterministic: false, implicit: false, one_step: true, strong_order: "1", weak_order: "1", needs_derivative_of_b: true}
history:
  year: 1974
  people: [Grigori N. Milstein]
  note: Milstein derived the scheme in 1974 from a stochastic Taylor expansion, as the first scheme of strong order 1 for Ito equations.
prereqs: [euler-maruyama-method, stochastic-differential-equation, order-of-accuracy]
see_also: [euler-method, local-truncation-error, global-error, monte-carlo-integration, taylor-series-method, runge-kutta-methods, stiff-ode-problem, gronwall-inequality]
sources:
  - book: isbn:9783540540625
    title: Peter E. Kloeden and Eckhard Platen, Numerical Solution of Stochastic Differential Equations, Springer, 1992
    locator: Chapter 5 (stochastic Taylor expansions), Section 10.3 (the Milstein scheme and its strong order 1 under commutative noise), Section 11.1 (derivative-free strong schemes) and Chapter 14 (weak schemes)
  - paper: doi:10.1137/S0036144500378302
    title: Desmond J. Higham, An algorithmic introduction to numerical simulation of stochastic differential equations, SIAM Review 43 (2001) 525-546
  - paper: "G. N. Mil'shtein, Approximate integration of stochastic differential equations, Theory of Probability and its Applications 19 (1974) 557-562"
  - paper: "G. N. Milstein, Numerical Integration of Stochastic Differential Equations, Kluwer, 1995 (translation of the 1988 Russian edition)"
    locator: Chapter 1 (the fundamental theorem on mean-square order of convergence)
---

The Milstein method approximates solutions of an Itô [stochastic differential equation](/stochastic-differential-equation/) $dX = a(t, X)\,dt + b(t, X)\,dW$, $X(t_0) = x_0$, driven by a Brownian motion $W$. On a grid $t_n$ with steps $h_n$ and Brownian increments $\Delta W_n = W(t_{n+1}) - W(t_n) \sim N(0, h_n)$ it takes

$$X_{n+1} = X_n + a(t_n, X_n)h_n + b(t_n, X_n)\Delta W_n + \tfrac12 b(t_n, X_n)\,b'(t_n, X_n)\bigl(\Delta W_n^2 - h_n\bigr),$$

with $b' = \partial b/\partial x$. The last term is what distinguishes it from the [Euler-Maruyama method](/euler-maruyama-method/). It comes from the double Itô integral $\int\int dW\,dW = \frac12(\Delta W^2 - h)$ in the stochastic Taylor expansion, and it raises the strong order, the rate at which individual paths converge, from $\frac12$ to $1$. The weak order, the rate for expectations, is 1 for both. For additive noise ($b' = 0$) the two methods coincide.

## In plain words

Some quantities change partly by a known trend and partly by random kicks, such as a stock price or a particle in a fluid. A simulation steps forward in small time steps, adding the trend and a random kick drawn for each step.

The simplest way of doing this ignores that the size of the kick itself changes when the quantity changes within the step. When the kicks are proportional to the current value, as for stock prices, this neglect makes each computed path wander away from the true path quickly as the step shrinks only slowly. The Milstein method adds one small correction for this effect. With it, halving the step halves the error of each path, instead of reducing it by less than a third.

## The problem

Given drift $a$ and diffusion $b$ (scalar, or diagonal noise for vectors), an initial value $x_0$, $T \ge t_0$, a step $h > 0$, and either Brownian increments or a seeded random generator, compute $X_N$ at $t_N = T$. Strong error is measured as $\mathbb{E}|X(T) - X_N|$ (or its mean-square version), weak error as $|\mathbb{E}\,g(X(T)) - \mathbb{E}\,g(X_N)|$. The cost is counted in evaluations of $a$, $b$, $b'$ and normal random numbers, times the number of steps and of sample paths.

## The algorithm

```pseudo id=main
MILSTEIN(a, b, b', x0, t0, T, h, source of ΔW)
L1  N ← ⌈(T − t0)/h − δ⌉                       ▷ δ: relative slack against rounding
L2  t ← t0, X ← x0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else t0 + (n + 1)h;  h_n ← t_next − t
L5      ΔW ← given increment, or √h_n · N(0, 1) per component
L6      A ← a(t, X),  B ← b(t, X)
L7      D ← b'(t, X)                             ▷ ∂b_i/∂x_i for diagonal noise
L8      X ← X + A h_n + B ΔW + ½ B D (ΔW² − h_n)  ▷ componentwise
L9      t ← t_next
L10 return X
```

The last step is shortened so that the grid ends at $T$, and its increment has variance $h_n$. Taking the increments from a given list lets one sample path be computed on several grids: summing groups of fine increments gives the increments of the same Brownian path on a coarser grid, which is how strong errors are measured.

## Example

**Three steps by hand.** $dX = \frac12 X\,dt + \frac12 X\,dW$, $X_0 = 1$, $h = \frac1{10}$, increments $\Delta W = (0.2, -0.1, 0.3)$. The exact solution is $X(t) = \exp(\frac38 t + \frac12 W(t))$. The first step is $1 + 0.05 + 0.1 + \frac18(0.04 - 0.1) = 1.1425$, exactly $\frac{457}{400}$.

| $t$ | 0.1 | 0.2 | 0.3 |
|---|---|---|---|
| Milstein | 1.142500 | 1.129647 | 1.354164 |
| Euler-Maruyama | 1.150000 | 1.150000 | 1.380000 |
| exact | 1.147402 | 1.133148 | 1.366838 |

On a single path with large steps either method may be closer; the orders are statements about averages over paths.

**Strong order.** $dX = 1.5X\,dt + X\,dW$ on $[0, 1]$, $X_0 = 1$, 1000 paths with seed 2024, each built from $2^9$ fine increments and coarsened. Mean of $|X(1) - X_N|$:

| $h$ | 1/4 | 1/8 | 1/16 | 1/32 | 1/64 | 1/128 |
|---|---|---|---|---|---|---|
| Euler-Maruyama | 1.243 | 0.921 | 0.615 | 0.424 | 0.317 | 0.215 |
| Milstein | 1.188 | 0.699 | 0.381 | 0.197 | 0.101 | 0.051 |
| derivative-free (Platen) | 1.467 | 0.884 | 0.477 | 0.242 | 0.123 | 0.061 |

The observed orders for Milstein are $0.77, 0.87, 0.95, 0.96, 0.98$, approaching 1; Euler-Maruyama stays near $0.5$. With 300 paths and five seeds, least squares slopes were $0.91$ to $0.97$ for Milstein and $0.50$ to $0.52$ for Euler-Maruyama. These are observed values with Monte Carlo error.

**Stiff drift.** For $dX = -50X\,dt + 0.5X\,dW$ the deterministic factor of a step is $1 - 50h$. With $h = 0.1$ it is $-4$ and the computed paths explode ($|X_N| > 10^6$ at $T = 2$); with $h = 0.01$ they decay below $10^{-10}$, like the true solution. The method is explicit, and its mean-square stability region is bounded.

## Correctness

Assume $a$, $b$ and $bb'$ are globally Lipschitz in $x$ with linear growth, $b \in C^2$, the coefficients are smooth enough in $t$, and the noise is scalar or diagonal (commutative). Then there is $C$ independent of $h$ with

$$\bigl(\mathbb{E}\,|X(T) - X_N|^2\bigr)^{1/2} \le C h.$$

The proof combines two facts. The Milstein step is the Itô-Taylor expansion of $X$ over one step truncated after the terms with $h$, $\Delta W$ and $I_{(1,1)} = \int_{t_n}^{t_{n+1}}\int_{t_n}^{s} dW\,dW = \frac12(\Delta W_n^2 - h_n)$, so the local error $\delta_n$ has $|\mathbb{E}[\delta_n \mid \mathcal{F}_{t_n}]| = O(h^2)$ and $\mathbb{E}|\delta_n|^2 = O(h^3)$. And Milstein's fundamental theorem says that local errors with mean $O(h^{p_1})$ and mean square $O(h^{2p_2})$, $p_2 \ge \frac12$, $p_1 \ge p_2 + \frac12$, give global mean-square order $p_2 - \frac12$. The correctness file proves the identity for $I_{(1,1)}$, the fundamental theorem by a discrete [Gronwall](/gronwall-inequality/) argument, and the local error bounds for linear equations such as the one in the example; the local bounds for general coefficients are cited (Kloeden and Platen, Section 10.3 and Chapter 5).

For Euler-Maruyama the term $bb'I_{(1,1)}$ is part of the local error, with $\mathbb{E}|bb'I_{(1,1)}|^2 = \frac12(bb')^2h^2$, so $p_2 = 1$ and the strong order is only $\frac12$ unless $bb' = 0$.

## Complexity

Each step evaluates $a$, $b$ and $b'$ once and draws $d$ normal numbers: $\Theta(C + d)$ per step, $\Theta(N(C + d))$ per path and $\Theta(MN(C + d))$ for $M$ paths in the [real RAM](/real-ram/) model, with $3MN$ coefficient evaluations. Extra space $\Theta(d)$ per path. To reach a strong error $\varepsilon$, Milstein needs $N = \Theta(\varepsilon^{-1})$ steps against $\Theta(\varepsilon^{-2})$ for Euler-Maruyama (asymptotic). For expectations the Monte Carlo error $\Theta(M^{-1/2})$ usually dominates; the strong order then matters mainly through multilevel Monte Carlo, where it reduces the variance of level differences.

## Properties

- **Strong order 1, weak order 1** under the conditions above.
- **Exact for the double integral.** Only $\Delta W$ is needed in the scalar and commutative cases; for general multi-dimensional noise the scheme needs the Lévy areas $\int\int (dW_j\,dW_k - dW_k\,dW_j)$, which cannot be computed from the increments alone.
- **Coincides with Euler-Maruyama for additive noise**, where both have strong order 1.
- **Depends on the interpretation.** For a Stratonovich equation the correction is $\frac12bb'\Delta W^2$, without the $-h$.
- **Explicit**, so stiff drifts limit the step; implicit-drift (drift-implicit Milstein) versions fix this for the drift part.
- **Positivity.** Not preserved in general. For $a = \mu x$, $b = \sigma x$ the Milstein factor $1 + \mu h + \sigma\Delta W + \frac12\sigma^2(\Delta W^2 - h)$ is a quadratic in $\Delta W$ with minimum $\frac12 + \mu h - \frac12\sigma^2h$, so it keeps $X_n > 0$ for every increment when $(\sigma^2 - 2\mu)h < 1$; Euler-Maruyama's factor $1 + \mu h + \sigma\Delta W$ is negative for large negative $\Delta W$.

## Variants and improvements

- **Derivative-free (Runge-Kutta) Milstein.** Platen's scheme replaces $bb'$ by $(b(\Upsilon) - b(X_n))/\sqrt{h}$ with the support value $\Upsilon = X_n + ah + b\sqrt h$; same strong order 1 (Kloeden and Platen, Section 11.1). The table above includes it.
- **Drift-implicit Milstein.** Evaluate the drift at $X_{n+1}$ for stiff drifts.
- **General noise.** With $m$ Brownian motions, add $\sum_{j,k}L^jb_k\,I_{(j,k)}$; under commutativity $L^jb_k = L^kb_j$ the iterated integrals reduce to products of increments.
- **Higher strong orders.** Itô-Taylor and stochastic Runge-Kutta schemes of strong order 1.5 need further multiple integrals such as $\int\int dW\,ds$.
- **Multilevel Monte Carlo.** Giles showed that the strong order 1 of Milstein makes the variance of level corrections decay like $h^2$, which reduces the cost of an expectation to $O(\varepsilon^{-2})$.
- **Tamed and truncated Milstein.** For superlinearly growing coefficients, where explicit schemes can diverge in moments.

## When to use it

Use Milstein when individual paths must be accurate, as in pathwise simulation, filtering, or multilevel Monte Carlo, and the noise is scalar or commutative so that no Lévy areas are needed. If only expectations are wanted and the Monte Carlo error dominates, Euler-Maruyama is cheaper and has the same weak order. If $b'$ is unavailable, use the derivative-free variant.

## Pitfalls

- **Itô or Stratonovich.** Using the Itô correction for a Stratonovich equation, or the reverse, gives a consistent scheme for the wrong equation.
- **Different paths on different grids.** Strong errors are measured on the same Brownian path; drawing new increments on each grid measures something else and shows no convergence.
- **Non-commutative noise.** Dropping the Lévy areas reduces the strong order to $\frac12$ again.
- **Stiffness and large noise.** Explicit steps can blow up; check the mean-square stability condition or use a drift-implicit version.
- **The last step.** If $T$ is not on the grid, the last increment must have variance $h_N$, not $h$.

## Implementations

## History

Milstein published the scheme in 1974, in "Approximate integration of stochastic differential equations", deriving it from an expansion of the solution in iterated Itô integrals, and later proved the fundamental theorem relating local and global mean-square orders. Wagner and Platen (1978) developed the stochastic Taylor expansion systematically, and Kloeden and Platen's book of 1992 made the Milstein scheme a standard reference method. Higham's 2001 SIAM Review article popularised the numerical study of its strong order with short programs, the experiment repeated above.

## References
