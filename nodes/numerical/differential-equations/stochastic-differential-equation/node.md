---
tag: S1JFXA
kind: problem
slug: stochastic-differential-equation
name: Stochastic differential equations
aliases:
- SDEs
- SDE initial value problem
- Itô stochastic differential equation
area: numerical/differential-equations
level: advanced
summary: "Find the random process X with dX = a(t, X) dt + b(t, X) dW, X(t_0) = X_0, where W is Brownian motion. Numerical methods are judged by strong (pathwise) or weak (in distribution) error."
model: real-ram
prereqs: [ode-initial-value-problem, picard-lindelof-theorem, monte-carlo-integration]
see_also: [euler-maruyama-method, milstein-method, heat-equation, box-muller-transform, markov-chain, stiff-ode-problem, random-walk-metropolis]
sources:
  - book: isbn:9783540540625
    title: Peter E. Kloeden and Eckhard Platen, Numerical Solution of Stochastic Differential Equations, Springer, 1992
    locator: Chapter 3 (Itô calculus), Chapter 4 (existence and uniqueness, Stratonovich SDEs, explicitly solvable SDEs), Chapter 9 (strong and weak convergence criteria), Chapter 10 (strong Taylor schemes, Euler and Milstein), Chapter 14 (weak Taylor schemes)
  - paper: doi:10.1137/S0036144500378302
    title: Desmond J. Higham, An algorithmic introduction to numerical simulation of stochastic differential equations, SIAM Review 43 (2001) 525-546
    locator: Sections 4 to 7 (Euler-Maruyama, strong and weak convergence experiments, Milstein, linear mean-square stability)
  - book: isbn:9783540047582
    title: Bernt Øksendal, Stochastic Differential Equations, An Introduction with Applications, sixth edition, Springer, 2003
    locator: Chapter 3 (the Itô integral), Chapter 4 (the Itô formula), Section 5.2 (existence and uniqueness of strong solutions), Chapter 8 (Kolmogorov equations and the Feynman-Kac formula)
  - paper: "Michael B. Giles, Multilevel Monte Carlo path simulation, Operations Research 56 (2008) 607-617"
    locator: complexity of weak approximation, multilevel estimator; doi:10.1287/opre.1070.0496
  - paper: "J. M. C. Clark and R. J. Cameron, The maximum rate of convergence of discrete approximations for stochastic differential equations, in Stochastic Differential Systems, Lecture Notes in Control and Information Sciences 25, Springer, 1980, 162-171"
    locator: methods that use only Brownian increments have strong order at most 1/2 in general
---

A stochastic differential equation (SDE) is an initial value problem driven by noise. In Itô form it reads $dX = a(t, X)\,dt + b(t, X)\,dW$, $X(t_0) = X_0$, where $X(t) \in \mathbb{R}^d$, $a$ is the drift, $b$ is the $d \times m$ diffusion matrix and $W$ is an $m$-dimensional Wiener process (Brownian motion). The solution is a random process. Numerical methods produce approximations $X_n \approx X(t_n)$ on a grid with step $\Delta t$, and there are two different questions: how close each simulated path is to the true path driven by the same noise (strong error), and how close the distribution, or the expected value of some function of the solution, is (weak error). SDEs model finance, molecular dynamics, chemical kinetics with small numbers of molecules, filtering and neural networks with noise.

## In plain words

An ordinary differential equation says exactly how a quantity changes. Many real systems also receive random kicks, like a stock price or a particle hit by molecules. An SDE adds a random term to the equation: in each small time interval the change is a predictable part plus a random part whose typical size is the square root of the time interval.

Because of that square root, the usual rules of calculus change, and simple methods become less accurate than for ordinary equations. To simulate, you draw random numbers for the kicks and step forward many times. You can then ask either whether one simulated path follows the true path for the same kicks, or whether averages over many simulated paths give the right averages. The second question is easier and is what most applications need.

## Definition

**Brownian motion.** $W(t)$, $t \ge 0$, has $W(0) = 0$, independent increments, $W(t) - W(s) \sim \mathcal N(0, (t - s) I_m)$ for $s < t$, and continuous paths. Paths are nowhere differentiable, and $\sum (\Delta W)^2 \to t$ over refining partitions of $[0, t]$, which is the source of the extra terms in Itô calculus.

**Itô SDE.** A process $X$ adapted to the filtration of $W$ solves the SDE on $[t_0, T]$ if, almost surely,

$$X(t) = X_0 + \int_{t_0}^t a(s, X(s))\,ds + \int_{t_0}^t b(s, X(s))\,dW(s) \quad \text{for all } t \in [t_0, T],$$

where the second integral is the Itô integral (left-point Riemann sums, a limit in mean square). The Stratonovich form $dX = \tilde a\,dt + b \circ dW$ uses midpoint sums; for $d = m = 1$ it is equivalent to the Itô SDE with drift $a = \tilde a + \frac12 b\,\partial_x b$.

**Existence and uniqueness (proved, Øksendal Section 5.2; Kloeden-Platen Chapter 4).** If $a$ and $b$ are measurable, globally Lipschitz in $x$ with constant $L$ uniformly in $t$, satisfy the linear growth bound $|a(t, x)| + |b(t, x)| \le K(1 + |x|)$, and $E|X_0|^2 < \infty$ with $X_0$ independent of $W$, then there is a pathwise unique continuous solution with $E\sup_{t \le T}|X(t)|^2 < \infty$. The proof is a [Picard iteration](/picard-lindelof-theorem/) in the space of square integrable processes, with the Itô isometry in place of the integral bound.

**Itô formula.** For $g \in C^{1,2}$ and $d = m = 1$, $dg(t, X) = \big(g_t + a g_x + \frac12 b^2 g_{xx}\big)dt + b g_x\,dW$. The term $\frac12 b^2 g_{xx}$ has no counterpart in ordinary calculus.

**The computational tasks.** Given a grid $t_n = t_0 + n\Delta t$ and Brownian increments $\Delta W_n$, a method computes $X_n$. Its **strong order** is $\gamma$ if $E|X(T) - X_N| \le C\Delta t^{\gamma}$, and its **weak order** is $\beta$ if $|E\,g(X(T)) - E\,g(X_N)| \le C\Delta t^{\beta}$ for all smooth $g$ with polynomial growth. In practice the expectation is estimated by the mean over $M$ independent paths, which adds a statistical error of order $M^{-1/2}$.

## Variants

- **Additive noise** ($b$ independent of $X$) and **commutative noise** (the columns $b_j$ satisfy $b_j'b_k = b_k'b_j$): higher strong order is possible with increments only.
- **Stratonovich SDEs**, natural when the noise is a limit of smooth noise and for geometric problems; they obey the ordinary chain rule.
- **Stiff SDEs** with a stiff drift, treated by drift-implicit methods.
- **SDEs with non-Lipschitz coefficients**, such as superlinear drift ($a = -x^3$) or square root diffusion (the CIR model $b = \sigma\sqrt x$), where standard theory and plain methods may fail.
- **Jump-diffusions** (driven by Poisson processes), **stochastic delay equations**, **backward SDEs**, and **stochastic PDEs** such as the stochastic heat equation.

## Examples

**Geometric Brownian motion.** $dX = \lambda X\,dt + \mu X\,dW$ has the exact solution $X(t) = X_0\exp\big((\lambda - \frac12\mu^2)t + \mu W(t)\big)$ by the Itô formula applied to $\ln X$, and $E X(t) = X_0 e^{\lambda t}$. With $\lambda = 2$, $\mu = 1$, $X_0 = 1$, $T = 1$ (the test of Higham 2001), 1000 paths, Brownian paths sampled at $2^{-9}$ and steps $\Delta t = 2^{-9}, \dots, 2^{-5}$, the mean absolute errors at $T$ were (observed):

| $\Delta t$ | $2^{-9}$ | $2^{-8}$ | $2^{-7}$ | $2^{-6}$ | $2^{-5}$ | fitted slope |
|---|---|---|---|---|---|---|
| [Euler-Maruyama](/euler-maruyama-method/) | 0.185 | 0.252 | 0.369 | 0.523 | 0.738 | 0.50 |
| [Milstein](/milstein-method/) | 0.031 | 0.062 | 0.124 | 0.245 | 0.476 | 0.99 |

Strong orders $\frac12$ and 1, as the theory predicts. For the weak error with $g(x) = x$, Euler-Maruyama gives $E X_N = (1 + \lambda\Delta t)^N$ exactly, so the weak error $|e^2 - (1 + 2\Delta t)^{1/\Delta t}|$ is $3.389$, $2.327$, $1.429$, $0.806$, $0.430$ for $\Delta t = 2^{-1}, \dots, 2^{-5}$, falling by about 2 per halving (weak order 1). A Monte Carlo estimate with 50000 paths gave $3.382$, $2.303$, $1.441$, $0.801$, $0.427$, within the statistical error.

**Ornstein-Uhlenbeck process.** $dX = -\theta X\,dt + \sigma\,dW$ has the Gaussian solution $X(t) = e^{-\theta t}X_0 + \sigma\int_0^t e^{-\theta(t - s)}dW(s)$ with variance $\frac{\sigma^2}{2\theta}(1 - e^{-2\theta t})$, which can be sampled exactly at grid points. It models velocities in Langevin dynamics and mean-reverting interest rates.

**Mean-square stability.** The zero solution of $dX = \lambda X\,dt + \mu X\,dW$ is mean-square stable, $E X(t)^2 \to 0$, if and only if $2\lambda + \mu^2 < 0$. Euler-Maruyama gives $E X_{n+1}^2 = \big((1 + \Delta t\lambda)^2 + \Delta t\mu^2\big)E X_n^2$. For $\lambda = -3$, $\mu = \sqrt3$ the factor is $7$ for $\Delta t = 1$, $\frac74$ for $\Delta t = \frac12$ and $\frac{13}{16}$ for $\Delta t = \frac14$, so only the last step size reproduces the decay (Higham 2001, Section 7). The exact condition is $\Delta t < -(2\lambda + \mu^2)/\lambda^2 = \frac13$.

## Known algorithms

- **[Euler-Maruyama](/euler-maruyama-method/)**: $X_{n+1} = X_n + a(t_n, X_n)\Delta t + b(t_n, X_n)\Delta W_n$. Strong order $\frac12$, weak order 1, under Lipschitz and smoothness conditions.
- **[Milstein](/milstein-method/)**: adds $\frac12 b b'\big((\Delta W_n)^2 - \Delta t\big)$ in the scalar case. Strong order 1; with several noise sources it needs Lévy areas unless the noise is commutative.
- **Stochastic Runge-Kutta methods** (for example Rößler's) avoid derivatives of $b$ and reach strong order 1 or weak order 2.
- **Weak schemes with simplified noise** replace $\Delta W_n$ by $\pm\sqrt{\Delta t}$ with probability $\frac12$; weak order is kept.
- **Drift-implicit and tamed schemes** for stiff or superlinear drifts; tamed Euler divides the drift increment by $1 + \Delta t|a|$.
- **[Monte Carlo](/monte-carlo-integration/) and multilevel Monte Carlo** (Giles 2008) estimate $E\,g(X(T))$ by combining paths on several grids with coupled noise.
- **Exact simulation** for linear SDEs (geometric Brownian motion, Ornstein-Uhlenbeck) and for some scalar SDEs (Beskos and Roberts).

## Bounds

- **Strong order barrier (proved, Clark and Cameron 1980).** A method that uses only the Brownian increments $\Delta W_n$ on a uniform grid has strong order at most $\frac12$ in general for multidimensional noise without commutativity; higher order needs iterated integrals (Lévy areas).
- **Monte Carlo cost.** With a method of weak order $\beta$, root mean square error $\varepsilon$ requires $M \sim \varepsilon^{-2}$ paths and $\Delta t \sim \varepsilon^{1/\beta}$, so the cost is $O(\varepsilon^{-2 - 1/\beta})$; for Euler-Maruyama $O(\varepsilon^{-3})$. Multilevel Monte Carlo reduces this to $O(\varepsilon^{-2}(\log\varepsilon)^2)$ with Euler-Maruyama and to $O(\varepsilon^{-2})$ with Milstein in one dimension (Giles 2008).
- **Failure of explicit Euler for superlinear coefficients (proved, Hutzenthaler, Jentzen and Kloeden 2011).** For $dX = -X^3dt + dW$, the moments $E|X_N|^p$ of Euler-Maruyama diverge as $\Delta t \to 0$, even though the exact moments are bounded.

## Reductions

- **To a PDE (Feynman-Kac).** $u(t, x) = E\big[g(X(T)) \mid X(t) = x\big]$ solves the backward Kolmogorov equation $u_t + a u_x + \frac12 b^2 u_{xx} = 0$, $u(T, x) = g(x)$. For $a = 0$, $b = 1$ this is the backward [heat equation](/heat-equation/). Weak approximation of the SDE is therefore a Monte Carlo method for this PDE, useful in high dimensions.
- **To the Fokker-Planck equation.** The density $p(t, x)$ of $X(t)$ solves $p_t = -(ap)_x + \frac12(b^2 p)_{xx}$.
- **To an ODE.** With $b = 0$ the SDE is an [ODE initial value problem](/ode-initial-value-problem/), and Euler-Maruyama becomes the Euler method.
- **Itô to Stratonovich and back**, by the drift correction $\frac12 b\,\partial_x b$; the Lamperti transform $Y = \int^X du/b(u)$ turns a scalar SDE into one with additive noise.

## Applications

- **Finance.** Asset prices (Black-Scholes uses geometric Brownian motion), interest rates and option pricing by Monte Carlo.
- **Molecular dynamics.** Langevin dynamics, thermostats and sampling of Boltzmann distributions.
- **Biology and chemistry.** The chemical Langevin equation for reaction networks with moderate molecule counts; population genetics.
- **Machine learning.** Stochastic gradient Langevin dynamics, and score-based diffusion models that generate images by integrating a reverse-time SDE.
- **Filtering and control.** Kalman-Bucy filters and stochastic optimal control.

## References
