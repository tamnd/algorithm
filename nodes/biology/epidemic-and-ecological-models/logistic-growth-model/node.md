---
tag: SN0SST
kind: model
slug: logistic-growth-model
name: Logistic growth model
aliases:
- Verhulst equation
- logistic equation
area: biology/epidemic-and-ecological-models
level: intro
summary: Population growth dN/dt = r N (1 - N/K), exponential at first and levelling off at the carrying capacity K.
history:
  year: 1838
  people: [Pierre-François Verhulst]
  note: Verhulst proposed the equation in 1838 as a law of population growth with a ceiling, and later named its solution the logistic curve.
prereqs: [ode-initial-value-problem, classical-runge-kutta-4]
see_also: [logistic-map, ricker-model, lotka-volterra-competition, levins-metapopulation-model, fisher-kpp-equation, birth-death-process, euler-method, logistic-regression]
sources:
  - paper: "Pierre-François Verhulst, Notice sur la loi que la population suit dans son accroissement, Correspondance mathématique et physique 10, 1838, pages 113 to 121"
    title: Verhulst 1838
    locator: the equation with a growth rate that falls as the population grows, and its solution
  - book: isbn:9780387952239
    title: James D. Murray, Mathematical Biology I, An Introduction, third edition, Springer, 2002
    locator: Chapter 1, Continuous Population Models for Single Species (section 1.1 on growth models and section 1.3 on delay models), and Chapter 2 for the discrete models
---

The logistic growth model is the differential equation $\frac{dN}{dt} = r N \left(1 - \frac{N}{K}\right)$ for the size $N(t)$ of one population, with an intrinsic growth rate $r$ and a carrying capacity $K$. Verhulst proposed it in 1838. A small population grows almost exponentially, the growth slows down as $N$ comes near $K$, and every positive solution tends to $K$ without oscillation. It is the single-species part of the [Lotka-Volterra competition model](/lotka-volterra-competition/), the [Levins metapopulation model](/levins-metapopulation-model/) and the [Fisher-KPP equation](/fisher-kpp-equation/).

## The machine

**The state.** $N(t) \ge 0$ is the size of the population at time $t$: a number of individuals, a biomass or a density. The model treats it as a real number.

**The parameters.**

- $r > 0$ is the intrinsic growth rate, in units of 1 per time. It is the per capita birth rate minus the per capita death rate when the population is very small.
- $K > 0$ is the carrying capacity, in the unit of $N$. It is the size at which births and deaths balance.

**The equation.**

$$\frac{dN}{dt} = r N \left(1 - \frac{N}{K}\right), \qquad N(0) = N_0 \ge 0.$$

The per capita growth rate $\frac{1}{N}\frac{dN}{dt} = r(1 - N/K)$ falls linearly in $N$. It is $r$ at $N = 0$, zero at $N = K$ and negative above $K$. One way to get this form: let the per capita birth rate be $b_0 - b_1 N$ and the per capita death rate be $d_0 + d_1 N$, with $b_0 > d_0$ and $b_1 + d_1 > 0$. Then $r = b_0 - d_0$ and $K = (b_0 - d_0)/(b_1 + d_1)$.

**The assumptions.** The population is closed (no migration). All individuals are the same, so there is no age, stage or sex structure. Crowding acts at once, with no delay, and it lowers the per capita rate linearly. The environment is constant. The population is large, so a deterministic equation for a real-valued size is a good description and chance births and deaths average out.

**A numerical solution.** The model has a closed form (below), so a numerical method is only needed for variants of it. The implementation uses the [classical Runge-Kutta method](/classical-runge-kutta-4/) with a fixed step $dt$ and checks it against the closed form.

```pseudo id=main
LOGISTIC-RK4(N0, r, K, dt, steps)          ▷ f(N) = r N (1 - N/K)
L1  N ← N0
L2  repeat steps times
L3      k1 ← f(N)
L4      k2 ← f(N + dt k1 / 2)
L5      k3 ← f(N + dt k2 / 2)
L6      k4 ← f(N + dt k3)
L7      N ← N + dt (k1 + 2 k2 + 2 k3 + k4) / 6
L8  return N
```

Each step costs four evaluations of $f$, so a run to time $T$ costs $O(T/dt)$ arithmetic operations. With $r = 1$ per day, $K = 100$ and $N_0 = 10$, the error at $t = 5$ days is $7.27 \times 10^{-6}$ for $dt = 0.1$ and $4.50 \times 10^{-7}$ for $dt = 0.05$. The ratio is $16.2$, close to $2^4$, as a fourth order method gives.

## What it counts

- The size $N(t)$ at each time, and the time to reach a given size.
- The equilibria $0$ and $K$, and how fast a population returns to $K$ after a small change.
- The time of fastest growth (the inflection point of the S-shaped curve) and the largest growth rate $rK/4$.
- With a constant harvest $H$ per unit of time, the largest harvest that the population can sustain.

**An example.** Take $r = 1$ per day, $K = 100$ and $N_0 = 10$. The closed form gives these sizes:

| $t$ (days) | 0 | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|
| $N(t)$ | 10 | 23.20 | 45.09 | 69.06 | 94.28 | 99.96 |

The growth is fastest at $t^* = \ln 9 \approx 2.197$ days, when $N = 50$, and the rate is then $rK/4 = 25$ per day. In the first day the size grows by a factor 2.32, a little less than the factor $e \approx 2.72$ of exponential growth at rate $r$.

## Relation to other models

- **Exponential growth.** As $K \to \infty$ the equation becomes $dN/dt = rN$, with the solution $N_0 e^{rt}$. The logistic solution stays close to it while $N \ll K$.
- **The [logistic map](/logistic-map/) and the [Ricker model](/ricker-model/).** These are discrete-time models with the same idea of a growth rate that falls with density. They behave in a different way: for large growth rates they oscillate and can become chaotic. The continuous model cannot oscillate, because a solution of a one-dimensional autonomous equation is monotone.
- **The exact time step is a Beverton-Holt map.** Sampling the solution at times $0, h, 2h, \ldots$ gives $N_{j+1} = \lambda N_j / (1 + (\lambda - 1) N_j / K)$ with $\lambda = e^{rh}$ (see the results below). This map is monotone and converges to $K$ for each step $h$.
- **The [Euler method](/euler-method/) gives a logistic map.** One forward Euler step of size $h$ is $N \mapsto N + hrN(1 - N/K)$. This is not the exact time step, and for large $h$ it is a different dynamical system.
- **A stochastic version.** A [birth-death process](/birth-death-process/) with per capita rates $b_0 - b_1 N$ and $d_0 + d_1 N$ has the logistic equation as its large-population limit. If the birth rate is zero above some size, the chain has finitely many states and $0$ can be reached from each state, so it dies out with probability 1. The time to extinction can be very long, and the logistic equation describes the long phase before it. The [Gillespie algorithm](/gillespie-algorithm/) simulates this chain exactly.
- **Models with more than one species or with space.** The [Lotka-Volterra competition model](/lotka-volterra-competition/) couples two logistic equations. The [Levins metapopulation model](/levins-metapopulation-model/) is a logistic equation for the fraction of occupied patches. The [Fisher-KPP equation](/fisher-kpp-equation/) adds diffusion in space.
- **The logistic function in statistics.** The solution is a shifted and scaled logistic function $1/(1 + e^{-x})$, the same function that [logistic regression](/logistic-regression/) uses. The two uses share the curve and nothing else.

## Known results in the model

**Closed form.** For each $N_0 \ge 0$ and $t \ge 0$,

$$N(t) = \frac{K N_0}{N_0 + (K - N_0)\, e^{-rt}}.$$

*Proof.* For $N_0 = 0$ the solution is $N \equiv 0$, and the formula gives 0. For $N_0 > 0$, the solution stays positive, because $N \equiv 0$ is a solution and solutions of this smooth equation cannot cross. Put $y = 1/N$. Then $y' = -N'/N^2 = -\frac{r}{N}(1 - N/K) = -ry + r/K$. This linear equation has the solution $y(t) = 1/K + (1/N_0 - 1/K) e^{-rt}$. Take the inverse and multiply the numerator and the denominator by $K N_0$. $\square$

**Monotone convergence to $K$.** If $0 < N_0 < K$, then $N(t)$ increases to $K$. If $N_0 > K$, it decreases to $K$. If $N_0 = K$, it stays at $K$. The approach is never an oscillation.

*Proof.* In the closed form, the term $(K - N_0) e^{-rt}$ has the sign of $K - N_0$, and its absolute value decreases to 0. So the denominator moves monotonically to $N_0$, and $N(t)$ moves monotonically to $K N_0 / N_0 = K$. $\square$

**Stability of the equilibria.** Write $f(N) = rN(1 - N/K)$. Then $f'(0) = r > 0$, so $0$ is unstable, and $f'(K) = -r < 0$, so $K$ is stable. Near $K$, a small deviation decays like $e^{-rt}$, so the return time is $1/r$. This is [Jacobian linearization](/jacobian-linearization/) in one dimension.

**Time to reach a size.** For $0 < N_0 < K$ and $N_0 < N < K$, solving the closed form for $t$ gives

$$t(N) = \frac{1}{r} \ln \frac{N (K - N_0)}{N_0 (K - N)}.$$

In the example, the population reaches 80 after $\ln 36 \approx 3.58$ days. The time tends to infinity as $N \to K$: the population never reaches $K$ in finite time.

**The inflection point.** $f(N)$ is a parabola in $N$ with its maximum $rK/4$ at $N = K/2$. If $N_0 < K/2$, the curve $N(t)$ is convex until it reaches $K/2$ and concave after, so its inflection is at $t^* = \frac{1}{r}\ln\frac{K - N_0}{N_0}$, the value of $t(K/2)$. If $N_0 \ge K/2$, there is no inflection point after time 0.

**The exact time-$h$ map.** For each $h > 0$, $N(t + h) = \frac{\lambda N(t)}{1 + (\lambda - 1) N(t)/K}$ with $\lambda = e^{rh}$.

*Proof.* The equation is autonomous, so $N(t + h)$ is the closed form with the start value $N(t)$ and the time $h$: $\frac{K N}{N + (K - N) e^{-rh}}$. Multiply the numerator and the denominator by $e^{rh}/K$. This gives $\frac{\lambda N}{\lambda N/K + 1 - N/K} = \frac{\lambda N}{1 + (\lambda - 1)N/K}$. $\square$

**The Euler map is a logistic map.** Let $\mu = 1 + hr$. The substitution $x = \frac{hrN}{\mu K}$ turns the Euler step $N \mapsto N + hrN(1 - N/K)$ into $x \mapsto \mu x (1 - x)$.

*Proof.* The Euler step is $N' = \mu N - hrN^2/K$. Then $x' = \frac{hr N'}{\mu K} = \frac{hrN}{K} - \frac{(hr)^2 N^2}{\mu K^2}$. Since $\frac{hrN}{K} = \mu x$, this is $\mu x - \frac{(\mu x)^2}{\mu} = \mu x (1 - x)$. $\square$

So the Euler iteration converges to $K$ only for $hr < 2$, because the fixed point $K$ has multiplier $1 - hr$. With $r = 1$, $K = 100$ and $h = 2.2$, the iteration settles on the 2-cycle $116.28, 74.63$. With $h = 2.7$ it does not settle at all. These are artefacts of a step that is too large, not properties of the model; the [logistic map](/logistic-map/) page gives the bifurcation values.

**Harvesting.** With a constant harvest $H \ge 0$, the equation $\frac{dN}{dt} = rN(1 - N/K) - H$ has an equilibrium if and only if $H \le rK/4$.

*Proof.* An equilibrium solves $\frac{r}{K} N^2 - rN + H = 0$. Its discriminant is $r^2 - 4rH/K$, which is non-negative if and only if $H \le rK/4$. $\square$

For $H < rK/4$ there are two equilibria; the larger one is stable and the smaller one is a threshold below which the population collapses. With $r = 1$, $K = 100$ and $H = 16$ they are $80$ and $20$. At $H = rK/4$ the two meet at $K/2$, and for a larger $H$ every solution reaches 0 in finite time. The value $rK/4$ is the maximum sustainable yield of this model. It is a result inside the model: a harvest close to it leaves the population near a fold, where a small error in $r$ or $K$ removes the equilibrium.

**A delay changes the behaviour.** If crowding acts with a delay $T$, as in $\frac{dN}{dt} = rN(t)\left(1 - \frac{N(t - T)}{K}\right)$, the equilibrium $K$ loses stability when $rT > \pi/2$ and the population oscillates (Murray, chapter 1). Monotone convergence is a property of the equation without delay.

## References
