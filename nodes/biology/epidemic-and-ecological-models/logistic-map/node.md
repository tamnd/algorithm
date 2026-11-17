---
tag: DM7V7K
kind: model
slug: logistic-map
name: Logistic map
aliases:
- May logistic map
area: biology/epidemic-and-ecological-models
level: core
summary: "The population model x_(t+1) = r x_t (1 - x_t), whose fixed point gives way to cycles of period 2, 4, 8 and then to chaos as r grows, May's example."
history:
  year: 1976
  people: [Robert M. May, Mitchell J. Feigenbaum, Tien-Yien Li, James A. Yorke]
  note: "May reviewed the map as a model of populations with discrete generations in 1976 and showed its route from a stable point through cycles to chaos. Li and Yorke proved in 1975 that period 3 implies chaos, and Feigenbaum found the universal ratio of the period doublings in 1978."
prereqs: [logistic-growth-model, fixed-point-iteration]
see_also: [ricker-model, euler-method, floyd-cycle-detection, brent-cycle-detection, lyapunov-stability, floating-point-arithmetic, leslie-matrix]
sources:
  - paper: doi:10.1038/261459a0
    title: "Robert M. May, Simple mathematical models with very complicated dynamics, Nature 261(5560), 1976"
    locator: "pages 459 to 467 (the logistic difference equation as a population model, its fixed points, cycles and chaotic regime)"
  - paper: doi:10.1080/00029890.1975.11994008
    title: "Tien-Yien Li and James A. Yorke, Period three implies chaos, The American Mathematical Monthly 82(10), 1975"
    locator: "pages 985 to 992 (a map of an interval with a point of period 3 has points of every period)"
  - paper: doi:10.1007/BF01020332
    title: "Mitchell J. Feigenbaum, Quantitative universality for a class of nonlinear transformations, Journal of Statistical Physics 19(1), 1978"
    locator: "pages 25 to 52 (the universal ratio 4.669201609 of the period-doubling intervals)"
  - book: isbn:9780813349107
    title: "Steven H. Strogatz, Nonlinear Dynamics and Chaos, 2nd ed., Westview Press, 2015"
    locator: "Chapter 10 (one-dimensional maps, the logistic map, period doubling and Lyapunov exponents)"
  - book: isbn:9780387952239
    title: "J. D. Murray, Mathematical Biology I, An Introduction, 3rd ed., Springer, 2002"
    locator: "Chapter 2 (discrete population models for a single species)"
---

The logistic map is the population model $x_{t+1} = r x_t (1 - x_t)$ for a species with separate, non-overlapping generations. The value $x_t$ is the population in generation $t$ as a fraction of a maximum, and $r$ is the growth factor per generation at low density. The factor $1 - x_t$ makes the growth fall as the population grows. May (1976) used this map to show that a very simple deterministic model can have very complicated dynamics. As $r$ grows from 1 to 4, the population first settles to a fixed level, then to cycles of period 2, 4, 8 and so on, and then changes without a period, in a way that depends sensitively on the start. So erratic numbers in a field census do not prove that the environment is random. The map is also the standard first example of chaos in one dimension.

## The machine

**The state.** One number $x_t \in [0, 1]$, the population in generation $t$ divided by a scale $M$. The population is $N_t = M x_t$. The scale $M$ is the population at which the next generation is zero, not the equilibrium level.

**The parameter.** $r > 0$, with no unit: the number of offspring per individual per generation that survive to breed when the population is small. In the population model $0 < r \le 4$.

**The update rule.** $x_{t+1} = f(x_t)$ with $f(x) = r x (1 - x)$. In the units of the population, $N_{t+1} = r N_t (1 - N_t / M)$. The slope of the map is $f'(x) = r (1 - 2x)$.

**The assumptions.** Generations are discrete and do not overlap, as in many insects with one generation per year. The population is closed, with no migration. The growth per individual falls linearly with the density. The model is deterministic and has no age or space structure. For $0 \le r \le 4$ the map sends $[0, 1]$ into itself, because $x(1 - x)$ has its maximum $1/4$ at $x = 1/2$. For $r > 4$ some values go above 1, and then the next population is negative, which has no biological meaning. The [Ricker model](/ricker-model/) does not have this defect.

```pseudo id=main
LOGISTIC-MAP(r, x_0, T)
L1  x ← x_0
L2  for t ← 1 to T do
L3      x ← r x (1 - x)
L4      record x_t ← x
L5  return x_1, ..., x_T
```

Each step costs a constant number of arithmetic operations, so a trajectory of $T$ generations costs $\Theta(T)$.

## What it counts

- The trajectory $x_1, \ldots, x_T$, the population in each generation.
- The long-run behaviour of the population: extinction, a fixed level, a cycle of period $p$, or an orbit with no period.
- The multiplier of a cycle $x_1, \ldots, x_p$, the product $f'(x_1) \cdots f'(x_p)$. The cycle is stable when the absolute value of the multiplier is less than 1. When the multiplier is 0 the cycle is called superstable.
- The Lyapunov exponent $\lambda = \lim_{T \to \infty} \frac{1}{T} \sum_{t=0}^{T-1} \ln |f'(x_t)|$, the mean rate per generation at which two nearby starts separate. A negative value means a stable cycle, and a positive value means chaos.

## Relation to other models

- **[Logistic growth model](/logistic-growth-model/).** The continuous model $dN/dt = rN(1 - N/K)$ always moves monotonically to $K$. Its [Euler method](/euler-method/) step with step size $h$ is a logistic map with parameter $1 + hr$, as that page shows. So a large time step, or a long gap between generations, turns smooth growth into cycles and chaos.
- **[Ricker model](/ricker-model/).** The Ricker model $x_{t+1} = x_t e^{r(1 - x_t)}$ has the same kind of density dependence and the same route to chaos, but its population stays positive for every $r$.
- **[Leslie matrix](/leslie-matrix/).** The Leslie model adds age structure but is linear, so it can only grow or decline geometrically. Density dependence such as the factor $1 - x_t$ is what gives the logistic map its cycles.
- **[Fixed-point iteration](/fixed-point-iteration/).** The trajectory is a fixed-point iteration of $f$. Near the fixed point $x^\ast$ the error is multiplied by about $f'(x^\ast)$ in each step, so the convergence is linear for $1 < r < 3$, $r \ne 2$, and quadratic at $r = 2$.
- **Cycle detection.** A floating-point number has finitely many values, so every computed orbit is eventually periodic. [Floyd's algorithm](/floyd-cycle-detection/) or [Brent's algorithm](/brent-cycle-detection/) finds the exact period of the computed orbit. To find the period of the true attractor, compare values with a tolerance after a transient, as the code of this page does.

## Known results in the model

**Bounded populations and extinction (theorem).** For $0 \le r \le 4$, $f$ maps $[0, 1]$ into itself. For $0 < r \le 1$, $x_t \to 0$ from every start in $[0, 1]$.

*Proof.* The first claim follows from $0 \le x(1 - x) \le 1/4$. For $r \le 1$ and $x_t > 0$, $x_{t+1} \le x_t (1 - x_t) < x_t$. So the sequence decreases and is bounded below by 0. Its limit is a fixed point in $[0, 1)$, and the only one is 0, because $1 - 1/r \le 0$. $\square$

**The equilibrium (theorem).** For $r > 1$ the map has a second fixed point $x^\ast = 1 - 1/r$ in $(0, 1)$. Its multiplier is $f'(x^\ast) = 2 - r$, so it is stable for $1 < r < 3$. The fixed point 0 has multiplier $r$ and is unstable for $r > 1$. For $1 < r < 2$ the multiplier is positive and the population approaches $x^\ast$ from one side. For $2 < r < 3$ it is negative and the population overshoots and oscillates with decreasing size. For example, $r = 2.8$ gives $x^\ast = 0.642857$, and the trajectory from $x_0 = 0.2$ is $0.448, 0.692429, 0.596319, 0.674023, 0.615205, 0.662838$. It is a known result that for $1 < r \le 3$ every start in $(0, 1)$ converges to $x^\ast$.

*Proof of the multiplier.* $f'(1 - 1/r) = r(1 - 2 + 2/r) = 2 - r$. $\square$

**The 2-cycle (theorem).** For $r > 3$ the map has a cycle of period 2,

$$x_\pm = \frac{r + 1 \pm \sqrt{(r - 3)(r + 1)}}{2r},$$

with multiplier $-r^2 + 2r + 4$. The cycle is stable for $3 < r < 1 + \sqrt{6} = 3.449490$ and superstable at $r = 1 + \sqrt{5} = 3.236068$.

*Proof.* The points of period 2 solve $f(f(x)) = x$. This is a polynomial of degree 4 that has the fixed points 0 and $1 - 1/r$ as roots. Division by these two factors leaves $r^2 x^2 - r(r + 1) x + (r + 1) = 0$, whose roots are $x_\pm$. They are real and distinct exactly when $r > 3$. With $x_+ + x_- = (r + 1)/r$ and $x_+ x_- = (r + 1)/r^2$, the multiplier is $r^2 (1 - 2x_+)(1 - 2x_-) = r^2 - 2r(r + 1) + 4(r + 1) = -r^2 + 2r + 4$. It is $-1$ when $r^2 - 2r - 5 = 0$, at $r = 1 + \sqrt{6}$, and $0$ when $r^2 - 2r - 4 = 0$, at $r = 1 + \sqrt{5}$. $\square$

At $r = 3.2$ the cycle is $0.513045, 0.799455$ with multiplier $0.16$, and the trajectory from $x_0 = 0.2$ is $0.512, 0.799539, 0.512884, 0.799469, 0.513019, 0.799458$. The population alternates between a high and a low year.

**The period-doubling cascade (known result).** At $r_1 = 3$ the fixed point gives way to the 2-cycle, and at $r_2 = 1 + \sqrt{6}$ the 2-cycle gives way to a 4-cycle. The doublings continue at $r_3 = 3.544090$, $r_4 = 3.564407$, $r_5 = 3.568759$, and the values $r_k$ accumulate at $r_\infty = 3.569946$. The ratios $(r_k - r_{k-1})/(r_{k+1} - r_k)$ converge to $\delta = 4.669201609$. Feigenbaum (1978) showed that the same constant holds for a wide class of smooth maps of an interval with one quadratic maximum, so it is universal. At $r = 3.5$ the stable 4-cycle is $0.826941, 0.500884, 0.874997, 0.382820$. A bisection on the period of the attractor agrees with $r_3$, $r_4$ and $r_5$ to four decimals (measurement).

**Chaos and periodic windows (known result).** Between $r_\infty$ and 4, parameters with chaotic orbits are mixed with windows of stable cycles. The widest window has period 3 and opens at $r = 1 + \sqrt{8} = 3.828427$. At $r = 3.83$ the stable 3-cycle is $0.156149, 0.504666, 0.957417$. Li and Yorke (1975) proved that a continuous map of an interval with a point of period 3 has points of every period and an uncountable set of orbits that do not approach any cycle (theorem). With $x_0 = 0.3$, 1000 steps of transient and 200000 steps of average, the Lyapunov exponent is $-0.8725$ at $r = 3.5$, $0.3548$ at $r = 3.7$ and $-0.3697$ at $r = 3.83$ (measurement). At $r = 3.2$ it is $\ln(0.16)/2 = -0.9163$, the logarithm of the multiplier divided by the period.

**The case r = 4 (theorem).** If $x_0 = \sin^2 \theta$, then $x_t = \sin^2(2^t \theta)$.

*Proof.* $4 \sin^2 a \,(1 - \sin^2 a) = 4 \sin^2 a \cos^2 a = \sin^2 2a$. Apply this with $a = 2^t \theta$. $\square$

So at $r = 4$ the map is the doubling of an angle in disguise, and for almost every start the Lyapunov exponent is $\ln 2 = 0.693147$ (known result). The computed value with $x_0 = 0.3$ is $0.6931$ (measurement).

**Loss of digits in floating point (measurement).** At $r = 4$ an error is about doubled in each step. From $x_0 = 0.2$, the orbit in double precision differs from an orbit computed with 300 digits by more than 0.1 first at step 52, which matches the 53 bits of a double. A computed chaotic orbit is a faithful trajectory only for a few dozen steps, but its long-run statistics are still useful (heuristic).

**Parameters above 4 (theorem).** For $r > 4$ the points near $1/2$ with $f(x) > 1$ go to a negative value and then to $-\infty$. It is a known result that the set of starts that stay in $[0, 1]$ forever is a Cantor set of measure zero. In the population model this means extinction for almost every start.

## References
