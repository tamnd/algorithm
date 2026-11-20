---
tag: A44WD4
kind: algorithm
slug: nudging
name: Nudging
aliases:
- Newtonian relaxation
area: scientific-computing/data-assimilation
level: intro
summary: "Adds a term G (y^o - H x) to the model equations that pulls the state toward the observations with a time scale 1/g; the simplest continuous data assimilation."
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, p: the number of observed quantities, m: the number of time steps, c: the cost of one evaluation of the model tendency, z: the number of nonzero entries of H and G}
  time: {worst: "Θ(m (c + n + p + z))"}
  space: {extra: "Θ(n + p + z)"}
properties: {deterministic: true, continuous_in_time: true, gain: fixed and tuned, optimal: "no, the gain is not derived from error statistics", synchronizes: "for full exact observations and a large enough gain"}
history:
  year: 1976
  people: [John E. Hoke, Richard A. Anthes]
  note: Hoke and Anthes used Newtonian relaxation toward observed fields in 1976 to initialize numerical weather prediction models.
prereqs: [data-assimilation-problem, observation-operator, classical-runge-kutta-4]
see_also: [luenberger-observer, state-observer, kalman-filter, optimal-interpolation, three-dimensional-variational-assimilation, lorenz-96-model, observing-system-simulation-experiment, ensemble-kalman-filter]
sources:
  - paper: doi:10.1175/1520-0493(1976)104<1551:TIONMB>2.0.CO;2
    title: J. E. Hoke and R. A. Anthes, The initialization of numerical models by a dynamic-initialization technique, Monthly Weather Review 104 (1976) 1551-1556
    locator: the relaxation term added to the model equations
  - paper: doi:10.1007/s00332-013-9189-y
    title: A. Azouani, E. Olson and E. S. Titi, Continuous data assimilation using general interpolant observables, Journal of Nonlinear Science 24(2) (2014) 277-304
    locator: exponential convergence of nudging with interpolated coarse observations for the 2D Navier-Stokes equations
  - book: isbn:9781611974539
    title: M. Asch, M. Bocquet and M. Nodet, Data Assimilation, Methods, Algorithms, and Applications, SIAM, 2016
    locator: Chapter 4 (nudging methods)
  - book: isbn:9783319203249
    title: K. Law, A. Stuart and K. Zygalakis, Data Assimilation, A Mathematical Introduction, Springer, 2015
    locator: Section 4.4.3 (the synchronization filter)
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Chapter 5 (data assimilation)
---

Nudging, also called Newtonian relaxation, assimilates observations by adding a relaxation term to the equations of the model, $\dot x = f(x) + G\,(y^o(t) - Hx)$, and integrating the result in time. The term pulls each observed quantity toward its observed value with the rate set by the gain $G$, and the model dynamics carry the information to the unobserved parts of the state. The gain is a tuned constant, not a quantity derived from error statistics, so nudging is cheap, easy to add to any model and continuous in time, but it is not an optimal estimator. With a constant gain the nudged model is a [Luenberger observer](/luenberger-observer/) for the model, and with full exact observations and a large enough gain the nudged state converges to the truth even for a chaotic model.

## In plain words

Take a weather model and run it forward. At the same time, look at the measurements. Wherever the model has a value that is measured, push the model a little toward the measurement at every time step. The push is stronger when the model is farther from the measurement, like a spring. The model then moves the corrected values to the places that are not measured, through its own physics. If the spring is too weak, the model drifts away on its own. If it is too strong for poor or sparse measurements, the model copies the noise or is pulled into a state that its physics do not like. The strength of the spring is chosen by trial, not by a formula.

## The problem

**Input.** A model tendency $f : \mathbb R^n \to \mathbb R^n$, an initial state $x_0$, a linear [observation operator](/observation-operator/) $H$ ($p \times n$), observations $y^o(t) \in \mathbb R^p$ given at every time, usually by interpolation in time between observation times, a gain $G$ ($n \times p$), a time step $dt$ and a number of steps $m$. Here $n$ is the state dimension and $p$ the number of observed quantities. The common choice is $G = gH^\top$, which relaxes each observed quantity with the rate $g$ and the time scale $1/g$.

**Output.** An approximation $x_k \approx x(t_k)$, $t_k = k\,dt$, of the solution of

$$\dot x = f(x) + G\big(y^o(t) - Hx\big), \qquad x(0) = x_0.$$

## The algorithm

```pseudo id=main
NUDGE(f, x_0, H, G, y^o, dt, m)
L1  x <- x_0
L2  for k <- 0 to m - 1 do
L3      q(t, z) := f(z) + G (y^o(t) - H z)              ▷ model plus relaxation
L4      x_{k+1} <- RK4 step of dz/dt = q(t, z) from t_k to t_{k+1}
L5  return x_0, x_1, ..., x_m
```

Line L3 is the only change to the model. Line L4 is one step of the [classical Runge-Kutta method](/classical-runge-kutta-4/), which evaluates $q$ at $t_k$, twice at $t_k + dt/2$ and at $t_{k+1}$, so $y^o$ must be available between observation times. The reference code interpolates it linearly in time. The step must also be stable for the relaxation: for $G = gI$ this needs about $g\,dt < 2.78$, the limit of RK4 on the negative real axis. With $G = 0$ the algorithm is the free model run.

## Example

**Scalar check.** For $\dot x = -ax + g(y - x)$ with constants, the solution is $x_e + (x_0 - x_e)e^{-(a+g)t}$ with $x_e = gy/(a + g)$. With $a = 0.7$, $g = 2.5$, $y = 3$ and $x_0 = -1$, the state relaxes to $x_e = 2.344$, not to $y = 3$: the model and the observation compromise.

**Lorenz-96 with full exact observations.** A truth run of the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$ and $F = 8$, RK4 with $dt = 0.01$, is observed at every variable without error. The nudged run starts from the truth plus Gaussian noise of standard deviation 3 (seed 1), with $H = I$ and $G = gI$. The table gives the root mean square error over the 40 variables (measurements).

| $g$ | $t = 0$ | $t = 5$ | $t = 10$ | $t = 20$ |
|---|---|---|---|---|
| 0 (free run) | 2.49 | 5.50 | 4.80 | 4.49 |
| 0.5 | 2.49 | 2.19 | 4.15 | 3.38 |
| 1 | 2.49 | 1.35 | 2.37 | 2.39 |
| 1.5 | 2.49 | 1.05 | 0.34 | 1.64 |
| 2 | 2.49 | 0.11 | 0.006 | 0.003 |
| 3 | 2.49 | 0.003 | 0.001 | 0.002 |
| 5 | 2.49 | 0.0009 | 0.0009 | 0.001 |

For $g \le 1.5$ the error stays of the order of the spread of the attractor. For $g \ge 2$ the nudged run locks onto the truth. The remaining error of about $10^{-3}$ comes from the linear interpolation of the truth in time at the half steps of RK4. The largest growth rate of small errors on this attractor is about 1.7, which is close to the measured threshold (measurement, see the Lorenz-96 page). The sufficient condition of Corollary 5 in the proof, $g > 4\max_j|x^t_j| - 1 \approx 54$, is far from sharp.

**Noisy observations.** The same truth is observed every $0.05$ time units with Gaussian errors of standard deviation $\sigma_o = 1$, and the observations are interpolated linearly in time. The mean root mean square error between $t = 10$ and $t = 30$ is 3.93 for $g = 0.5$, 2.44 for $g = 1$, 0.71 for $g = 2$, 0.40 for $g = 5$ and 0.46 for $g = 10$ (measurements). A moderate gain averages the noise over a time of about $1/g$; a large gain follows the noise more closely.

**Half the variables observed.** With only the even variables observed and $G = gH^\top$, the error after $t = 30$ was 2.7 for $g = 2$, 0.3 for $g = 5$, 0.003 for $g = 10$ and 0.6 for $g = 20$ (measurements). Here a gain that is too large is worse than a moderate one.

## Correctness

The [proof](proofs/correctness.md) shows that the loop stops after $m$ Runge-Kutta steps of the nudged equation, and three facts about that equation. For a linear scalar model it relaxes to the weighted mean $gy/(a + g)$ with the rate $a + g$. If the model satisfies the one-sided bound $e^\top(f(x^t + e) - f(x^t)) \le \ell|e|^2$ along the truth, and the observations are full and exact with $G = gI$, then $|e(t)| \le e^{(\ell - g)t}|e(0)|$ (a theorem). For Lorenz-96 the bound holds with $\ell = 4\max_j|x^t_j| - 1$, because the advection term conserves energy. With partial observations, convergence needs more: Azouani, Olson and Titi (2014) prove it for the 2D Navier-Stokes equations when the observations resolve the flow finely enough and the gain is large enough, but not too large for that resolution.

## Complexity

Each step evaluates the tendency four times, at the cost $c$ each, and forms $G(y^o - Hz)$ four times in $\Theta(n + p + z)$ time with sparse $H$ and $G$ ($z$ nonzero entries). So $m$ steps cost $\Theta(m(c + n + p + z))$, which for a local $H$ is a small fraction more than the free model run. The extra memory is the current state and the observations needed for the current step. This is much less than for any method that stores or evolves a covariance matrix.

## Properties

- **Not optimal.** The gain does not come from $B$ and $R$, so the result is not the minimum variance estimate. With noisy observations the error does not go to zero; it settles at a level set by the gain, the noise and the model.
- **Continuous in time.** The state is corrected at every step, so there are no jumps in the forecast at analysis times, and the run is smooth enough to drive other models.
- **Balance.** A gentle relaxation lets the model adjust the unobserved fields to the observed ones, which is why it was first used to initialize models (Hoke and Anthes 1976).
- **Observer form.** For a constant $G$ the nudged model is a [Luenberger observer](/luenberger-observer/) of the model. The [Kalman filter](/kalman-filter/) gives the gain that minimizes the error variance for linear Gaussian models.
- **Synchronization.** For full exact observations, convergence of the nudged run to the truth is synchronization of two copies of the model through a coupling, which needs a coupling strength above a threshold set by the instability of the model.

## Variants and improvements

- **Observation nudging and analysis nudging.** Relax toward individual observations, with weights that fall off with distance and time from each observation, or toward gridded analyses. Regional models use both.
- **Spectral nudging.** Relax only the large scales of the model toward a global analysis, and leave the small scales free. Regional climate runs use this.
- **Back and forth nudging.** Run the nudged model forward and then backward in time with the opposite sign of relaxation, several times, to improve the initial state (Asch, Bocquet and Nodet 2016, Chapter 4).
- **Interpolant observables.** Replace $Hx$ by an interpolant of the coarse observations, as in Azouani, Olson and Titi (2014), which gives proofs of convergence for dissipative partial differential equations.
- **Statistical gains.** Take $G$ from optimal interpolation weights, or from a Kalman gain computed once, to give more weight to good observations.

## When to use it

Use nudging when a cheap continuous assimilation is needed for a model with no tangent linear or adjoint code, for example to keep a regional or climate model close to a reanalysis, to spin up a model, or to prepare initial conditions with balanced fields. Use it also as a baseline in an [observing system simulation experiment](/observing-system-simulation-experiment/). For the best estimate from noisy observations, use [optimal interpolation](/optimal-interpolation/), [3D-Var](/three-dimensional-variational-assimilation/) or an [ensemble Kalman filter](/ensemble-kalman-filter/).

## Pitfalls

- **Gain too large for the time step (line L4).** RK4 is unstable for the relaxation term when $g\,dt$ is larger than about $2.78$, and the run blows up. Reduce $dt$ or treat the relaxation implicitly.
- **Sign of the relaxation (line L3).** Writing $Hz - y^o$ in place of $y^o - Hz$ pushes the model away from the observations, and the error grows like $e^{gt}$. A test with $f = 0$ and a constant observation shows it at once.
- **Observations only at the observation times (line L3).** If $y^o(t)$ is used only at the exact observation times and the term is set to zero between them, the effective gain depends on the time step. Interpolate the observations in time, or spread each one over a time window.
- **Gain too large for partial or noisy data.** A strong relaxation of a few observed quantities forces the model into states that its dynamics do not support, and it copies the noise. In the half observed example above, $g = 20$ was worse than $g = 10$. Tune the gain by experiment.
- **Treating the output as an error estimate.** Nudging gives no analysis error variance. Measure the error against independent observations or in a twin experiment.

## Implementations

## History

Hoke and Anthes in 1976 used Newtonian relaxation for dynamic initialization, adding a relaxation term to the equations of a numerical weather prediction model so that the model adjusts gradually to the observed fields. The method then spread to continuous assimilation in regional models and to nudged climate runs. Its mathematical analysis as continuous data assimilation came later: Azouani, Olson and Titi gave in 2014 a proof of convergence for the 2D Navier-Stokes equations with general interpolant observables, and Law, Stuart and Zygalakis (2015) analyze the closely related synchronization filter.

## References
