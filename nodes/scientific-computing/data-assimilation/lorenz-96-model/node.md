---
tag: BQWSGH
kind: model
slug: lorenz-96-model
name: Lorenz-96 model
aliases:
- Lorenz 1996 model
area: scientific-computing/data-assimilation
level: core
summary: "A cyclic chaotic system dx_j/dt = (x_{j+1} - x_{j-2}) x_{j-1} - x_j + F, the standard test bed for data assimilation methods."
prereqs: [ode-initial-value-problem, classical-runge-kutta-4]
see_also: [observing-system-simulation-experiment, data-assimilation-problem, ensemble-kalman-filter, nudging, adjoint-model, four-dimensional-variational-assimilation, covariance-localization, particle-filter]
sources:
  - book: doi:10.1017/CBO9780511617652.004
    title: E. N. Lorenz, Predictability, a problem partly solved, in T. Palmer and R. Hagedorn (eds), Predictability of Weather and Climate, Cambridge University Press, 2006, pp. 40-58 (first in the Proceedings of the ECMWF Seminar on Predictability, 1996)
    locator: the model with one and with two scales of variables
  - paper: doi:10.1175/1520-0469(1998)055<0399:OSFSWO>2.0.CO;2
    title: E. N. Lorenz and K. A. Emanuel, Optimal sites for supplementary weather observations, simulation with a small model, Journal of the Atmospheric Sciences 55(3) (1998) 399-414
    locator: the model with 40 variables and F = 8 as a test of observing strategies
  - book: isbn:9783319203249
    title: K. Law, A. Stuart and K. Zygalakis, Data Assimilation, A Mathematical Introduction, Springer, 2015
    locator: Section 2.2 (the Lorenz '96 example, its absorbing ball and global attractor)
---

The Lorenz-96 model is a system of $n$ ordinary differential equations on a circle of variables, $\dot x_j = (x_{j+1} - x_{j-2})x_{j-1} - x_j + F$, that Edward Lorenz introduced in 1996 as a small stand-in for one latitude circle of the atmosphere. It has a quadratic advection term that conserves energy, linear damping and constant forcing, the same three ingredients as the equations of the atmosphere. For $n = 40$ and $F = 8$ it is chaotic, with small errors doubling in about 0.42 time units, and the state is cheap to integrate, so it is the standard test bed for [data assimilation](/data-assimilation-problem/) methods: a new filter or smoother is usually first shown in an [observing system simulation experiment](/observing-system-simulation-experiment/) with this model.

## The machine

**State and memory.** The state is a vector $x = (x_0, \ldots, x_{n-1}) \in \mathbb R^n$ with cyclic indices, $x_{-1} = x_{n-1}$, $x_{-2} = x_{n-2}$ and $x_n = x_0$. The memory is the $n$ numbers of the state. Here $n$ is the number of variables and $F$ is the forcing.

**Dynamics.** The state evolves by

$$\frac{dx_j}{dt} = \underbrace{(x_{j+1} - x_{j-2})\,x_{j-1}}_{\text{advection } N(x)_j} \; - \; \underbrace{x_j}_{\text{damping}} \; + \; F, \qquad j = 0, \ldots, n - 1.$$

**A step.** One evaluation of the tendency costs $\Theta(n)$ arithmetic operations. Codes advance the state with the [classical Runge-Kutta method](/classical-runge-kutta-4/), four evaluations per step, usually with $dt = 0.01$ or $dt = 0.05$. Lorenz scaled time so that one unit is about 5 days, which makes $dt = 0.05$ about 6 hours, the usual time between analyses at a weather center.

**Standard settings.** $n = 40$ and $F = 8$, with observations of some or all variables every $0.05$ time units and observation errors of standard deviation 1. Lorenz's first paper used $n = 36$. The two-scale version couples each $x_j$ to $J$ fast variables $y_{j,k}$ with their own Lorenz-96 type dynamics, and serves as a test of model error and parameterization.

## What it counts

An experiment with the model counts the error of an estimate against the known truth run: the root mean square error over the $n$ variables, averaged over time after a spin-up, and compared with the observation error. It also counts the cost of the method in model integrations, for example the ensemble size, because one integration costs almost nothing and the real cost is the number of them. The model itself is described by measured quantities: the leading Lyapunov exponent $\lambda_1$, the error doubling time $\ln 2/\lambda_1$, and the mean and the spread of the variables on the attractor.

## Relation to other models

- **The atmosphere.** The variables stand for a quantity, such as vorticity, at $n$ equally spaced points of a latitude circle. The model has no conservation laws of a real fluid apart from the energy of the advection term, no vertical structure and no balance, so methods that rely on balance, such as a [background error covariance](/background-error-covariance/) built from balance operators, cannot be tested on it.
- **Lorenz 1963.** The three-variable convection model of 1963 is also chaotic, but it has no spatial structure, so localization and the behavior of methods in many dimensions cannot be tested on it.
- **State-space model.** With RK4 steps and linear observations plus noise, the model is a nonlinear [state-space model](/state-space-model/) with a deterministic transition.
- **Spatially extended chaos.** The number of unstable directions grows with $n$ (an observation from computed Lyapunov spectra, not a theorem), so ensembles smaller than the number of unstable directions, as in real weather prediction, can be studied by taking $n$ large.

## Known results in the model

**Theorem 1 (the advection conserves energy).** $x^\top N(x) = \sum_j x_j(x_{j+1} - x_{j-2})x_{j-1} = 0$ for every $x$.

*Proof.* The sum is $\sum_j x_{j+1}x_jx_{j-1} - \sum_j x_jx_{j-1}x_{j-2}$. Shift the index of the second sum by one: it becomes $\sum_j x_{j+1}x_jx_{j-1}$, the first sum. $\square$

**Theorem 2 (absorbing ball).** Every solution satisfies $|x(t)|^2 \le e^{-t}|x(0)|^2 + nF^2(1 - e^{-t})$, so $\limsup_{t\to\infty} |x(t)| \le \sqrt n\,F$. For $n = 40$ and $F = 8$ the radius is $50.6$.

*Proof.* By Theorem 1, $\tfrac12 \tfrac{d}{dt}|x|^2 = -|x|^2 + F\sum_j x_j \le -|x|^2 + F\sqrt n\,|x| \le -\tfrac12|x|^2 + \tfrac12 nF^2$, by the Cauchy-Schwarz inequality and $ab \le \tfrac12 a^2 + \tfrac12 b^2$. So $\tfrac{d}{dt}|x|^2 \le -|x|^2 + nF^2$, and the bound follows from the Gronwall inequality. $\square$

So all solutions exist for all time and enter a bounded ball, and the long-time behavior lives on a global attractor (Law, Stuart and Zygalakis 2015, Section 2.2).

**Theorem 3 (the steady state and its instability).** $x_j = F$ for all $j$ is a steady state. Its linearization has the eigenvalues $\lambda_m = F(e^{i\theta_m} - e^{-2i\theta_m}) - 1$, $\theta_m = 2\pi m/n$, $m = 0, \ldots, n - 1$, with $\mathrm{Re}\,\lambda_m = F(\cos\theta_m - \cos 2\theta_m) - 1 \le \tfrac98 F - 1$. The steady state is linearly stable for $F < 8/9$ for every $n$. For $n = 40$ the largest real part is at $m = 8$, about $1.118F - 1$, so the steady state is unstable for $F > 0.894$.

*Proof.* At $x = F$ the factor $x_{j+1} - x_{j-2}$ is zero, so the linearization is $\dot\delta_j = F(\delta_{j+1} - \delta_{j-2}) - \delta_j$. This is a circulant system, so the Fourier modes $\delta_j = e^{ij\theta_m}$ are eigenvectors with the eigenvalues $\lambda_m$. With $c = \cos\theta$, $\cos\theta - \cos 2\theta = -2c^2 + c + 1$, whose maximum over $c$ is $9/8$ at $c = 1/4$. For $n = 40$ the angle closest to $\arccos(1/4)$ is $\theta_8$, with $\cos\theta_8 = 0.309$ and the value $1.118$. $\square$

The imaginary part $F(\sin\theta + \sin 2\theta)$ is positive for the unstable modes, so their phase moves toward decreasing $j$: the patterns of the model are waves of about 8 crests on the circle of 40 points that travel in one direction.

**Theorem 4 (small forcing gives a stable equilibrium).** If $|F| < 1/4$, every solution converges to the steady state $x_j = F$ exponentially, at the rate at least $1 - 4|F|$.

*Proof.* Let $e = x - F\mathbf 1$. As on the [nudging](/nudging/) page (Lemma 4 of its proof, with the constant solution $F\mathbf 1$ as the reference), $e^\top \dot e \le (4|F| - 1)|e|^2$, because the cubic term vanishes by Theorem 1 and the cross terms are at most $4|F|\,|e|^2$. So $|e(t)| \le e^{(4|F| - 1)t}|e(0)|$. $\square$

**Measurements for $n = 40$, $F = 8$.** With RK4, the leading Lyapunov exponent computed by the method of Benettin with the tangent linear model, a spin-up of 20 time units and an average over 200 units (seed 1), is $\lambda_1 = 1.69$ for $dt = 0.05$ and $1.66$ for $dt = 0.01$. The error doubling time is therefore about 0.42 time units, about 2.1 days in Lorenz's scaling. On the attractor the variables have a mean of about $2.35$ and a standard deviation of about $3.64$, so an observation error of 1 is a little over a quarter of the climatological spread. These are measurements of one run, not theorems.

**Use in data assimilation.** Nudging with full exact observations locks onto the truth for a gain $g \ge 2$ in a test on the [nudging](/nudging/) page (a measurement). [Ensemble Kalman filters](/ensemble-kalman-filter/) with [localization](/covariance-localization/) and [inflation](/covariance-inflation/) are commonly reported to reach errors well below the observation error with a few tens of members, while standard [particle filters](/particle-filter/) need a number of particles that grows very fast with the number of observed variables, which is the problem of [weight collapse](/particle-filter-weight-collapse/). Lorenz and Emanuel (1998) used the model to study where to place extra observations.

## References
