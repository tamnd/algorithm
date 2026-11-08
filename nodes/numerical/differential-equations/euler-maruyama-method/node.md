---
tag: YNYFA8
kind: algorithm
slug: euler-maruyama-method
name: Euler-Maruyama method
aliases:
- stochastic Euler method
- Euler scheme for SDEs
- Maruyama scheme
area: numerical/differential-equations
level: advanced
summary: "Euler's method for dX = a dt + b dW: X_(n+1) = X_n + a h + b ΔW_n with ΔW_n ~ N(0, h). Strong order 1/2 (order 1 for additive noise) and weak order 1 under Lipschitz coefficients."
solves: [stochastic-differential-equation]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", d: "the dimension of X", m: "the dimension of the Brownian motion W", C: "the cost of one evaluation of a and b"}
  time: {worst: "Θ(N (C + d m))"}
  space: {extra: "Θ(d m)"}
  evaluations: {worst: "N"}
properties: {deterministic: false, implicit: false, one_step: true, strong_order: "1/2", weak_order: "1", order: "1/2"}
history:
  year: 1955
  people: [Gisiro Maruyama]
  note: Maruyama (1955) studied the Euler approximation of Itô equations driven by Brownian motion and proved its mean-square convergence; it became the base scheme of the stochastic Taylor expansion theory of Kloeden and Platen.
prereqs: [stochastic-differential-equation, euler-method]
see_also: [milstein-method, euler-method, monte-carlo-integration, box-muller-transform, stiff-ode-problem, backward-euler-method, global-error, gronwall-inequality]
sources:
  - book: isbn:9783540540625
    title: Peter E. Kloeden and Eckhard Platen, Numerical Solution of Stochastic Differential Equations, Springer, 1992
    locator: Section 9.1 (the Euler approximation), Section 10.2 (strong convergence of the Euler scheme, order 1/2), Section 14.1 (the weak Euler scheme, order 1), Section 4.5 (existence and uniqueness of strong solutions)
  - paper: doi:10.1137/S0036144500378302
    title: Desmond J. Higham, An algorithmic introduction to numerical simulation of stochastic differential equations, SIAM Review 43(3) (2001) 525-546
    locator: the Euler-Maruyama method, strong and weak convergence experiments on geometric Brownian motion, mean-square stability
  - paper: doi:10.1007/BF02846028
    title: Gisiro Maruyama, Continuous Markov processes and stochastic equations, Rendiconti del Circolo Matematico di Palermo 4 (1955) 48-90
    locator: the Euler-type approximation of stochastic equations and its convergence
  - paper: doi:10.1137/S0036142901389530
    title: Desmond J. Higham, Xuerong Mao and Andrew M. Stuart, Strong convergence of Euler-type methods for nonlinear stochastic differential equations, SIAM Journal on Numerical Analysis 40(3) (2002) 1041-1063
    locator: strong convergence under local Lipschitz conditions with moment bounds
---

The Euler-Maruyama method approximates the solution of an Itô [stochastic differential equation](/stochastic-differential-equation/) $dX = a(t, X)\,dt + b(t, X)\,dW$ by the step $X_{n+1} = X_n + a(t_n, X_n)\,h + b(t_n, X_n)\,\Delta W_n$, where $\Delta W_n = W(t_{n+1}) - W(t_n)$ is a Brownian increment, a normal random vector with mean 0 and covariance $hI$. It is [Euler's method](/euler-method/) with a random kick added per step. Each step costs one evaluation of $a$ and $b$ and $m$ normal samples. Under global Lipschitz conditions the mean error along a path is $O(h^{1/2})$ (strong order 1/2) and the error of expectations is $O(h)$ (weak order 1). It is the base scheme of stochastic simulation in finance, physics and biology, usually inside a [Monte Carlo](/monte-carlo-integration/) loop.

## In plain words

Some quantities change partly by a rule and partly by chance, like a stock price or a particle jostled by molecules. To simulate one possible history, the method takes small time steps. In each step it moves the quantity by the rule, as an ordinary simulation would, and then adds a random push whose typical size grows like the square root of the step length. Running it many times with different random pushes gives many possible histories, and averaging them estimates expected values. The method is simple and cheap per step, but not very accurate for a single history: to halve the error of one path you need four times as many steps. For averages it does better: halving the step roughly halves the error.

## The problem

Given drift $a : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$, diffusion $b : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^{d \times m}$, an $m$-dimensional Brownian motion $W$ and an initial value $X_0$ independent of $W$ with $E\|X_0\|^2 < \infty$, approximate the strong solution $X(t)$ of $X(t) = X_0 + \int_{t_0}^{t}a(s, X(s))\,ds + \int_{t_0}^{t}b(s, X(s))\,dW(s)$ (Itô integral) at $t = T$: either the random value $X(T)$ on a given Brownian path (strong approximation), or expectations $E\,g(X(T))$ (weak approximation). The grid is $t_n = t_0 + nh$, with the last step shortened to end at $T$.

## The algorithm

```pseudo id=main
EULER-MARUYAMA(a, b, t0, X0, T, h)
L1  N ← ⌈(T − t0)/h − δ⌉                       ▷ δ: relative slack 10^-9 against rounding
L2  t ← t0, X ← X0
L3  for n ← 0 to N − 1 do
L4      t_next ← T if n = N − 1 else t0 + (n + 1) h
L5      Δt ← t_next − t
L6      ΔW ← a sample of N(0, Δt I_m), independent of all earlier samples
L7      X ← X + a(t, X) Δt + b(t, X) ΔW
L8      t ← t_next
L9  return (t, X)
```

Line L6 draws the Brownian increment with variance equal to the actual step length, which matters for the last, shortened step. To follow a given Brownian path (for strong error tests, or to compare step sizes on one path), the increments are taken from that path instead: the increment over a coarse step is the sum of the fine increments it contains. Line L7 evaluates $a$ and $b$ at the left end of the step, which is what makes the limit an Itô and not a Stratonovich integral.

## Example

**One path by hand.** Geometric Brownian motion $dX = 2X\,dt + X\,dW$, $X(0) = 1$, $T = 1$, $h = \tfrac14$, with increments $\Delta W = 0.3, -0.2, 0.1, 0.25$. Each step multiplies $X$ by $1 + 2h + \Delta W_n = 1.5 + \Delta W_n$:

| $n$ | $t_n$ | $\Delta W_{n-1}$ | factor | $X_n$ |
|---|---|---|---|---|
| 0 | 0 | | | 1 |
| 1 | 0.25 | 0.3 | 1.8 | 1.8 |
| 2 | 0.5 | $-0.2$ | 1.3 | 2.34 |
| 3 | 0.75 | 0.1 | 1.6 | 3.744 |
| 4 | 1 | 0.25 | 1.75 | 6.552 |

The exact solution is $X(t) = \exp\big((\mu - \tfrac12\sigma^2)t + \sigma W(t)\big)$ with $\mu = 2$, $\sigma = 1$. If the path passes through $W(1) = 0.45$, $X(1) = e^{1.95} = 7.0287$. (The exact value depends only on $W(1)$; the numerical value depends on all four increments.)

**Strong error.** With 1000 Brownian paths (seed 100), each sampled on a fine grid of $2^9$ steps and summed to coarser grids, the mean of $|X_N - X(1)|$ is:

| $h$ | 1/4 | 1/8 | 1/16 | 1/32 | 1/64 |
|---|---|---|---|---|---|
| $E\,|X_N - X(1)|$ | 2.435 | 1.673 | 1.107 | 0.738 | 0.523 |

The least-squares slope of $\log$ error against $\log h$ is 0.56, close to the strong order $\tfrac12$ (an observed value, with Monte Carlo noise).

**Weak error, exactly.** For this equation $E[X_N] = (1 + 2h)^N$ exactly, because each factor $1 + 2h + \Delta W_n$ has mean $1 + 2h$ and the factors are independent. Against $E[X(1)] = e^2 = 7.3891$, the weak errors are $2.327, 1.429, 0.806, 0.430, 0.223$ for $h = \tfrac14, \ldots, \tfrac1{64}$: ratios near 2, weak order 1.

## Correctness

The loop computes the Euler-Maruyama approximation on the grid, with independent increments $\Delta W_n \sim N(0, (t_{n+1} - t_n)I_m)$ (induction on $n$). Two convergence statements hold.

**Strong convergence (proved in the proof file).** Let $a$ and $b$ be globally Lipschitz in $(t, x)$ with constant $K$, and $E\|X_0\|^2 < \infty$. Then there is $C$, independent of $h$, with

$$\max_{n}\big(E\|X(t_n) - X_n\|^2\big)^{1/2} \le C\,h^{1/2}.$$

The proof writes the scheme as a continuous process driven by the same Brownian motion, bounds the difference of drift and diffusion integrals by the Itô isometry, uses $E\|X(s) - X(t_n)\|^2 = O(s - t_n)$, and closes with the [Gronwall inequality](/gronwall-inequality/).

**Strong order 1 for additive noise.** If $b$ does not depend on $X$, the method coincides with the [Milstein method](/milstein-method/), whose correction term $\tfrac12 b\,b'(\Delta W^2 - h)$ vanishes, and it has strong order 1 when $a$ is smooth (Kloeden and Platen 1992, Section 10.3). This is cited, not proved here; the tests observe it.

**Weak order 1 (cited).** If $a, b$ are smooth with bounded derivatives and $g$ is smooth with polynomial growth, then $|E\,g(X(T)) - E\,g(X_N)| = O(h)$ (Kloeden and Platen 1992, Section 14.1).

## Complexity

Line L7 runs $N = \lceil (T - t_0)/h\rceil$ times. Each run makes one evaluation each of $a$ and $b$ (cost $C$), draws $m$ normal samples, and does $O(dm)$ arithmetic. So the time is $\Theta(N(C + dm))$ and the extra space $\Theta(dm)$ in the [real RAM](/real-ram/) model with a unit-cost normal sampler (for example by the [Box-Muller transform](/box-muller-transform/)).

To reach a strong error $\varepsilon$ at fixed $T$ needs $N = \Theta(\varepsilon^{-2})$ steps. To estimate $E\,g(X(T))$ with root mean square error $\varepsilon$ by plain Monte Carlo needs bias $O(h) \le \varepsilon$ and $M = \Theta(\varepsilon^{-2})$ samples, so $\Theta(\varepsilon^{-3})$ steps in total; multilevel Monte Carlo reduces this to $O(\varepsilon^{-2}(\log\varepsilon)^2)$ by combining several step sizes on coupled paths (Giles 2008).

## Properties

- **Strong order 1/2, weak order 1** under Lipschitz conditions; strong order 1 for additive noise.
- **Explicit.** One evaluation of $a$ and $b$ per step, no equation to solve.
- **Itô consistent.** Evaluating $b$ at the left end gives the Itô solution. Evaluating it at the midpoint or averaging the ends converges to the Stratonovich solution instead.
- **Mean-square stability.** On $dX = \lambda X\,dt + \mu X\,dW$ with real $\lambda, \mu$, the exact solution has $E X(t)^2 \to 0$ iff $2\lambda + \mu^2 < 0$, and the method has $E X_{n+1}^2 = \big((1 + h\lambda)^2 + h\mu^2\big)E X_n^2$, so it is mean-square stable iff $(1 + h\lambda)^2 + h\mu^2 < 1$. For $\lambda = -3$, $\mu = \sqrt3$ this means $h < \tfrac13$ (Higham 2001).
- **Reduces to Euler's method** when $b = 0$.

## Variants and improvements

- **[Milstein method](/milstein-method/).** Adds $\tfrac12 b\,\partial_x b\,(\Delta W^2 - h)$ for scalar noise and reaches strong order 1. For several noise sources it needs iterated Itô integrals (Lévy areas) unless the noise is commutative.
- **Drift-implicit (stochastic theta) methods.** Evaluate $a$ at the new point, as in [backward Euler](/backward-euler-method/), for stiff drift; mean-square stable for larger steps.
- **Tamed and truncated Euler schemes.** For drifts that grow faster than linearly, divide the drift increment by $1 + h\|a(X_n)\|$ to keep moments bounded.
- **Weak schemes with simple increments.** For weak order 1 the normal increments can be replaced by $\pm\sqrt h$ with probability $\tfrac12$ each.
- **Multilevel Monte Carlo** (Giles 2008) couples Euler-Maruyama paths at several step sizes.

## When to use it

Use it as the default for Monte Carlo estimates of expectations when the weak order 1 is enough, for prototypes, and whenever the coefficients are not smooth enough for higher-order schemes. For pathwise accuracy with multiplicative noise use the Milstein method or higher-order strong schemes; for stiff drift use a drift-implicit variant.

## Pitfalls

- **Wrong increment scaling.** Drawing $\Delta W$ with variance 1 or with standard deviation $h$ instead of $\sqrt h$ gives a scheme that converges to the wrong equation or to a deterministic one. The last, shortened step needs variance equal to its own length.
- **Comparing step sizes on different paths.** A strong error estimate needs the same Brownian path on all grids; sum the fine increments, do not draw new ones.
- **Superlinear coefficients.** For drifts such as $-X^3$ the moments of the explicit scheme can diverge as $h \to 0$ even though the exact solution is well behaved (Hutzenthaler, Jentzen and Kloeden 2011); use tamed or implicit variants.
- **Stratonovich models.** If the model is written in Stratonovich form, convert the drift ($a + \tfrac12 b\,\partial_x b$ in the scalar case) before applying the scheme.
- **Confusing strong and weak error.** A small Monte Carlo error bar on $E\,g(X_N)$ says nothing about the bias $O(h)$.

## Implementations

## History

Gisiro Maruyama introduced the approximation in 1955, in a paper on continuous Markov processes and stochastic equations, and proved that it converges in mean square to the solution of the Itô equation. The systematic theory of strong and weak orders, based on stochastic Taylor expansions, is due to Platen, Milstein, Talay and others in the 1970s and 1980s, and was collected by Kloeden and Platen in 1992. Higham's 2001 article made the method and its convergence experiments the standard starting point for teaching.

## References
