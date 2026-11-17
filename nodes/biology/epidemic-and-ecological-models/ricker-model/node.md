---
tag: ZBTGC3
kind: model
slug: ricker-model
name: Ricker model
aliases:
- Ricker stock-recruitment model
area: biology/epidemic-and-ecological-models
level: core
summary: "The discrete population model N_(t+1) = N_t e^(r (1 - N_t / K)), used for fish stocks, which shows cycles and chaos for large r."
history:
  year: 1954
  people: [William E. Ricker]
  note: "Ricker introduced the curve R = a S e^(-b S) in 1954 for the number of recruits produced by a stock of spawning fish."
prereqs: [logistic-map]
see_also: [logistic-growth-model, leslie-matrix, fixed-point-iteration, ordinary-least-squares, poisson-distribution, lotka-volterra-competition, floyd-cycle-detection, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1139/f54-039
    title: "W. E. Ricker, Stock and recruitment, Journal of the Fisheries Research Board of Canada 11(5), 1954"
    locator: "pages 559 to 623 (the stock-recruitment curve with a maximum, and its use for fish stocks)"
  - paper: doi:10.1038/261459a0
    title: "Robert M. May, Simple mathematical models with very complicated dynamics, Nature 261(5560), 1976"
    locator: "pages 459 to 467 (the exponential form x exp(r (1 - x)) beside the logistic form)"
  - book: isbn:9780387952239
    title: "J. D. Murray, Mathematical Biology I, An Introduction, 3rd ed., Springer, 2002"
    locator: "Chapter 2 (discrete population models for a single species)"
---

The Ricker model is the discrete population model $N_{t+1} = N_t e^{r(1 - N_t / K)}$ for a species with separate generations. Below the level $K$ the population grows, and above $K$ it falls. The fall is strong: a large population produces fewer offspring than a medium one. Ricker (1954) wrote it as a stock-recruitment curve $R = a S e^{-bS}$, the number of young fish $R$ that a stock of $S$ spawners produces, for fisheries. Like the [logistic map](/logistic-map/), the model has a stable equilibrium for small $r$, then cycles of period 2, 4, 8, and chaos for large $r$. Unlike the logistic map, the population stays positive for every $r$, so the model is a valid population model for all its parameters.

## The machine

**The state.** One number $N_t > 0$, the population, or the number of spawners, in generation $t$. The scaled state is $u_t = N_t / K$.

**The parameters.** The growth rate $r > 0$, with no unit: $e^r$ is the factor of growth per generation when the population is very small. The equilibrium level $K > 0$, in the units of $N$ (individuals, or tonnes of spawners).

**The update rule.** $N_{t+1} = N_t \exp(r(1 - N_t / K))$, or $u_{t+1} = f(u_t)$ with $f(u) = u e^{r(1 - u)}$. The slope is $f'(u) = e^{r(1 - u)} (1 - r u)$. The stock-recruitment form $R = a S e^{-bS}$ is the same rule with $a = e^r$ and $b = r / K$, so $r = \ln a$ and $K = \ln a / b$.

**The assumptions.** Generations are discrete and do not overlap. The population is closed and has no age structure. The number of offspring per individual falls exponentially with the density, $e^{r} e^{-rN/K}$, so it never becomes negative. A common way to get this form: if each young individual dies when it meets an adult, and the meetings are random with a mean number proportional to $N_t$, then the chance to survive is the zero term of a [Poisson distribution](/poisson-distribution/), $e^{-cN_t}$ (heuristic). The model is deterministic.

```pseudo id=main
RICKER(r, K, N_0, T)
L1  N ← N_0
L2  for t ← 1 to T do
L3      N ← N exp(r (1 - N / K))
L4      record N_t ← N
L5  return N_1, ..., N_T
```

Each step costs one exponential and a few arithmetic operations, so $T$ generations cost $\Theta(T)$.

## What it counts

- The trajectory $N_1, \ldots, N_T$, the population or the stock in each generation.
- The long-run behaviour: the equilibrium $K$, a cycle of period $p$, or an orbit with no period.
- The multiplier of a cycle, the product of $f'(u)$ over its points. The cycle is stable when the absolute value of the multiplier is less than 1.
- The Lyapunov exponent, the mean of $\ln |f'(u_t)|$ along the orbit, which is positive for chaos.
- In fisheries, the recruits $R$ from a stock $S$, and the stock $S = 1/b$ that gives the most recruits.

## Relation to other models

- **[Logistic map](/logistic-map/).** Both maps have one hump and the same route to chaos by period doubling. The logistic map sends values above 1 to negative values for $r > 4$. The Ricker map is positive for every $r$, and its large values are followed by very small ones, not by negative ones.
- **[Logistic growth model](/logistic-growth-model/).** Suppose that the population grows by $dN/dt = r(1 - N_t / K) N$ during one generation, with the rate per individual fixed by the density $N_t$ at the start of the generation. Then $d \ln N / dt$ is constant during the generation, and the population at its end is exactly $N_t e^{r(1 - N_t / K)}$. So the Ricker model is logistic growth with a density effect that acts once per generation (theorem, by integration).
- **Beverton-Holt model.** The model $N_{t+1} = R_0 N_t / (1 + N_t / M)$ has recruitment that rises to a plateau and never falls. It has no cycles. The Ricker curve falls at high stock, which is called overcompensation, and this is the source of the cycles.
- **[Leslie matrix](/leslie-matrix/).** An age-structured linear model. If the fertilities in its first row are made to depend on the density in the Ricker form, the model has cycles and chaos as well (heuristic).
- **[Fixed-point iteration](/fixed-point-iteration/).** The trajectory is a fixed-point iteration of $f$, and the rate of approach to $K$ is $|1 - r|$ per generation.

## Known results in the model

**Positive and bounded (theorem).** If $u_0 > 0$, then $0 < u_t \le e^{r-1}/r$ for every $t \ge 1$.

*Proof.* $f(u) > 0$ for $u > 0$. The slope $e^{r(1-u)}(1 - ru)$ is zero only at $u = 1/r$, positive below and negative above, so $f$ has its maximum $f(1/r) = e^{r-1}/r$ there. $\square$

The value after the peak is $f(e^{r-1}/r)$. At $r = 3$ the peak is $e^2/3 = 2.463019$ times $K$, and the next generation is $0.030572$ times $K$. Over 199000 generations at $r = 3$ the orbit fills the range from $0.030572$ to $2.463019$ (measurement). A crash to 3 percent of $K$ is a real risk of extinction in a small population, which the deterministic model does not show (heuristic).

**The equilibrium (theorem).** The fixed point $u = 1$, that is $N = K$, has multiplier $f'(1) = 1 - r$. It is stable for $0 < r < 2$. For $0 < r < 1$ the population approaches $K$ from one side, at $r = 1$ the fixed point is superstable, and for $1 < r < 2$ the population overshoots and oscillates with decreasing size. For example, $r = 1.5$ from $u_0 = 0.2$ gives $0.664023, 1.099139, 0.947260, 1.025241, 0.987149, 1.006362$, and the error is roughly halved and changes sign in each step, since $1 - r = -0.5$. The Lyapunov exponent there is $\ln 0.5 = -0.6931$.

**The 2-cycle (theorem).** For $r > 2$ the map has a 2-cycle $1 - d, 1 + d$, where $d \in (0, 1)$ solves $\ln((1 + d)/(1 - d)) = r d$. Its multiplier is $(1 - r)^2 - r^2 d^2$.

*Proof.* Let $u_1, u_2$ be a 2-cycle. Multiply $u_2 = u_1 e^{r(1 - u_1)}$ and $u_1 = u_2 e^{r(1 - u_2)}$ to get $e^{r(2 - u_1 - u_2)} = 1$, so $u_1 + u_2 = 2$. Write $u_1 = 1 - d$ and $u_2 = 1 + d$. Then $u_2 / u_1 = e^{rd}$, which is the equation for $d$. The left side is $2d + 2d^3/3 + \ldots$, convex in $d$ with slope 2 at 0 and infinite at 1, so it meets $rd$ at some $d \in (0, 1)$ exactly when $r > 2$. The multiplier is $f'(u_1) f'(u_2) = e^{r(2 - u_1 - u_2)} (1 - r u_1)(1 - r u_2) = (1 - r + rd)(1 - r - rd) = (1 - r)^2 - r^2 d^2$. $\square$

At $r = 2.3$ the cycle is $0.407845, 1.592155$ with multiplier $-0.164925$. The population alternates between 41 percent and 159 percent of $K$. The cycle loses stability when the multiplier is $-1$, that is when $d^2 = ((r - 1)^2 + 1)/r^2$. Together with the equation for $d$ this gives $r = 2.526468$ (numerical root).

**The period-doubling cascade (measurement).** A bisection on the period of the attractor gives the next doublings near $r = 2.6563$ (period 4 to 8), $2.6846$ (8 to 16) and $2.6907$ (16 to 32), and the onset of chaos near $r = 2.692$. The ratios of the successive intervals are about $4.59$ and $4.64$. The map has one quadratic maximum, so by the known result of Feigenbaum they converge to $4.669201609$, the same constant as for the logistic map. At $r = 2.6$ the stable 4-cycle is $0.181222, 0.390846, 1.523166, 1.904765$.

**Chaos (measurement).** At $r = 3$ the orbit from $u_0 = 0.3$ has no period up to 64, and with 1000 steps of transient and 200000 steps of average its Lyapunov exponent is $0.3854$. At $r = 3.5$ it is $0.5379$, and at $r = 2.6$ it is $-0.5751$. A search on a grid of step $0.001$ finds a stable 3-cycle from about $r = 3.103$. Where a 3-cycle exists, the theorem of Li and Yorke gives points of every period.

**Fitting the curve (theorem and practice).** $\ln(R/S) = \ln a - bS$ is linear in $S$. So [ordinary least squares](/ordinary-least-squares/) of $\ln(R/S)$ on $S$ estimates $\ln a$ and $b$ from pairs of stock and recruits. If the noise is a factor $e^{\varepsilon}$ with independent normal $\varepsilon$ of constant variance, this fit is the [maximum likelihood estimate](/maximum-likelihood-estimation/) (theorem). It is the usual first fit of the Ricker curve in fisheries (known practice). The errors in the stock values bias the slope, and the observed stocks depend on past recruits, so the fit is only a first estimate (heuristic).

## References
