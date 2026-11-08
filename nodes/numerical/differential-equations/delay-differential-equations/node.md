---
tag: MJVX3X
kind: problem
slug: delay-differential-equations
name: Delay differential equations
aliases:
- DDEs
- time-delay equations
- retarded functional differential equations
- differential equations with time lag
area: numerical/differential-equations
level: advanced
summary: "Find y on [t_0, T] with y'(t) = f(t, y(t), y(t - τ)) and y = φ on [t_0 - τ, t_0]. The state is a function segment, not a point, and derivative jumps propagate along the delays."
prereqs: [ode-initial-value-problem, picard-lindelof-theorem, dense-output]
see_also: [delay-differential-solver, dense-output, hermite-interpolation, bogacki-shampine-method, radau-iia-methods, stiff-ode-problem, dahlquist-test-equation, differential-algebraic-equations]
sources:
  - book: isbn:9780198506546
    title: Alfredo Bellen and Marino Zennaro, Numerical Methods for Delay Differential Equations, Oxford University Press, 2003
    locator: Chapter 2 (existence, uniqueness, propagation of discontinuities, the method of steps), Chapters 4 to 6 (continuous Runge-Kutta methods for DDEs, convergence and order), Chapter 10 (stability of the test equation with delay)
  - book: isbn:9780387940762
    title: Jack K. Hale and Sjoerd M. Verduyn Lunel, Introduction to Functional Differential Equations, Springer, 1993
    locator: Chapter 2 (existence, uniqueness and continuous dependence for retarded equations), Chapter 1 and Chapter 5 (linear equations, the characteristic equation)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.17 (delay differential equations; the method of steps, discontinuities, numerical methods based on dense output)
  - paper: doi:10.1016/S0168-9274(00)00055-6
    title: L. F. Shampine and S. Thompson, Solving DDEs in MATLAB, Applied Numerical Mathematics 37 (2001) 441-458
    locator: the dde23 code, an explicit 3(2) Runge-Kutta pair with cubic Hermite interpolation and discontinuity tracking for constant delays
---

A delay differential equation (DDE) is a differential equation in which the rate of change at time $t$ depends on the solution at earlier times $t - \tau$. To solve it one needs not an initial value but an initial function, the history on a whole interval. The solution is usually less smooth than for an [ODE](/ode-initial-value-problem/): a jump in a derivative at the start reappears at $t_0 + \tau$, $t_0 + 2\tau, \ldots$ one order higher each time. Numerical solvers must therefore evaluate the solution between grid points ([dense output](/dense-output/)) and locate these discontinuities to keep their order.

## In plain words

In an ordinary differential equation, the present state alone decides how the system changes next. Many real systems react to the past instead: a population whose birth rate depends on how many adults there were a generation ago, a thermostat that reads a sensor with a lag, a blood cell count controlled by a signal sent days earlier. To predict such a system you need to know its whole recent history, not just its value now. Delays can make a stable system oscillate, and long delays can make it unstable. They also leave marks: a sudden change at the start produces small kinks that repeat after each delay period. A computer method must remember past values, look them up between its own steps, and watch for these kinks.

## Definition

**Notation.** $y(t) \in \mathbb{R}^d$; constant delays $\tau_1, \ldots, \tau_m > 0$ with $\tau = \max_i\tau_i$; history function $\varphi : [t_0 - \tau, t_0] \to \mathbb{R}^d$.

**Problem (retarded DDE with constant delays).** Given $f : [t_0, T] \times \mathbb{R}^d \times (\mathbb{R}^d)^m \to \mathbb{R}^d$ and $\varphi$, find $y : [t_0 - \tau, T] \to \mathbb{R}^d$, continuous, with $y = \varphi$ on $[t_0 - \tau, t_0]$ and

$$y'(t) = f\big(t, y(t), y(t - \tau_1), \ldots, y(t - \tau_m)\big), \qquad t_0 < t \le T.$$

The derivative is the right derivative at $t_0$; in general $y'(t_0^+) = f(t_0, \varphi(t_0), \ldots) \ne \varphi'(t_0^-)$.

**Well-posedness (proved).** If $f$ is continuous and Lipschitz in its $y$ arguments and $\varphi$ is continuous, the problem has a unique solution on $[t_0, T]$, and it depends continuously on $\varphi$ in the max-norm (Hale and Verduyn Lunel 1993, Chapter 2). For constant delays this also follows from the method of steps below: on each interval $[t_0 + k\tau_{\min}, t_0 + (k+1)\tau_{\min}]$ the delayed terms are known functions, and the problem is an ODE covered by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/).

**Propagation of discontinuities (proved).** For constant delays, smooth $f$ and smooth $\varphi$, the points where $y$ may fail to be smooth lie in the set $\{t_0 + \sum_i k_i\tau_i : k_i \ge 0\}$. If $y'$ jumps at $t_0$, then for a single delay $y^{(k+1)}$ may jump at $t_0 + k\tau$ while $y, \ldots, y^{(k)}$ are continuous there: the solution gains one derivative per delay interval (Bellen and Zennaro 2003, Chapter 2).

**The state space.** The state at time $t$ is the segment $y_t(\theta) = y(t + \theta)$, $\theta \in [-\tau, 0]$, an element of $C([-\tau, 0], \mathbb{R}^d)$. A DDE is an evolution equation on this infinite-dimensional space, which is why a linear scalar DDE has infinitely many characteristic roots.

## Variants

- **Time-dependent delays** $\tau(t)$ and **state-dependent delays** $\tau(t, y(t))$. The discontinuity points must then be found by solving $t - \tau(t, y(t)) = \xi$ for earlier discontinuity points $\xi$, and well-posedness needs more care.
- **Vanishing delays**, with $\tau(t) \to 0$, such as the pantograph equation $y'(t) = ay(t) + by(qt)$, $0 < q < 1$. The method of steps does not apply near the point where the delay vanishes.
- **Neutral DDEs**, where $y'(t)$ also depends on $y'(t - \tau)$. Discontinuities do not smooth out: a jump in $y'$ at $t_0$ repeats at every $t_0 + k\tau$ as a jump in $y'$.
- **Distributed delays**, $y'(t) = f\big(t, y(t), \int_{-\tau}^{0}K(\theta)y(t + \theta)\,d\theta\big)$, which are integro-differential equations.
- **Stiff DDEs**, which need implicit methods as for [stiff ODEs](/stiff-ode-problem/), and **delay differential-algebraic equations**, combining delays with [algebraic constraints](/differential-algebraic-equations/).

## Examples

**The method of steps, by hand.** $y'(t) = -y(t - 1)$ with $\varphi(t) = 1$ for $t \le 0$. On $[0, 1]$ the delayed term is $\varphi = 1$, so $y = 1 - t$. On $[1, 2]$ it is $1 - (t - 1)$, so $y = -(t - 1) + \tfrac12(t - 1)^2$. On $[2, 3]$, $y = -\tfrac12 + \tfrac12(t - 2)^2 - \tfrac16(t - 2)^3$. In exact arithmetic $y(1) = 0$, $y(2) = -\tfrac12$, $y(3) = -\tfrac16$, $y(4) = \tfrac{5}{24}$. The derivative jumps at $t = 0$ from $\varphi' = 0$ to $y'(0^+) = -1$; at $t = 1$, $y'$ is continuous but $y''$ jumps from 0 to 1; at $t = 2$, $y''$ is continuous and $y'''$ jumps. The solution is a piecewise polynomial whose degree grows by one per interval.

**Delay-induced instability.** For $y'(t) = -b\,y(t - 1)$, $b > 0$, the characteristic equation is $\lambda + be^{-\lambda} = 0$. The zero solution is asymptotically stable iff $b < \pi/2$ (a case of Hayes' 1950 criterion); at $b = \pi/2$ the roots $\lambda = \pm i\pi/2$ cross the imaginary axis. The exact piecewise polynomial solution with $\varphi = 1$, computed with rational arithmetic up to $t = 40$, confirms this: $|y|$ over $[35, 40]$ stays below $1.5 \cdot 10^{-5}$ for $b = 1$, below $0.32$ for $b = 1.5$, near $0.9$ and slowly decreasing for $b = 1.57$, near $0.99$ and slowly increasing for $b = 1.58$, and above $1.1$ and growing for $b = 1.6$. The same equation without delay, $y' = -by$, is stable for every $b > 0$.

**Population models.** Hutchinson's delayed logistic equation $N'(t) = rN(t)\big(1 - N(t - \tau)/K\big)$ has a stable equilibrium $N = K$ for $r\tau < \pi/2$ and a stable periodic orbit beyond it. The Mackey-Glass equation $x'(t) = \beta x(t - \tau)/(1 + x(t - \tau)^n) - \gamma x(t)$, a model of blood cell production, has chaotic solutions for large delays.

**Non-example.** $y'(t) = f(t, y(t), y(t + 1))$ is an advanced equation: the rate depends on the future. It is not an initial value problem, and the method of steps does not apply.

## Known algorithms

- **Method of steps.** For constant delays $\tau \ge \tau_{\min} > 0$, solve the ODE on $[t_0 + k\tau_{\min}, t_0 + (k+1)\tau_{\min}]$ with the delayed terms taken from the already computed solution. With an ODE code this needs the solution at off-grid past times.
- **Continuous Runge-Kutta methods and discontinuity tracking.** A one-step method with [dense output](/dense-output/) supplies $y(t - \tau)$ at any past time. Including the discontinuity points as grid points keeps the order of the underlying method. This is the [delay differential solver](/delay-differential-solver/) of this site, and the design of dde23 (the [Bogacki-Shampine](/bogacki-shampine-method/) pair with cubic [Hermite interpolation](/hermite-interpolation/)).
- **Implicit methods for stiff DDEs.** Collocation methods such as [Radau IIA](/radau-iia-methods/) with their continuous extension; the code RADAR5 by Guglielmi and Hairer is of this type.
- **Linear multistep methods with interpolation**, and for state-dependent delays, codes that control the residual of the continuous approximation instead of the local error.

## Bounds

- **Order with and without tracking (proved for constant delays).** A continuous Runge-Kutta method of discrete order $p$ and uniform dense output order $q$ gives global order $\min(p, q + 1)$ when every discontinuity point up to order $p$ is a grid point (Bellen and Zennaro 2003, Chapters 4 to 6). Without tracking, a step that straddles a jump in $y^{(j)}$ has a local error $O(h^{j+1})$; this limits the observed order in the first few delay intervals.
- **Cost.** For constant delays and explicit methods, the cost is that of the ODE solver plus the interpolation of the stored past, $O(1)$ extra evaluations of the interpolant per delayed term and stage, and memory for the solution over the last $\tau$ time units.
- **Linear stability.** For $y'(t) = ay(t) + by(t - \tau)$ with real $a, b$: if $|b| < -a$, the zero solution is asymptotically stable for every delay $\tau \ge 0$ (delay-independent stability); if $b < -|a|$, it is stable for small $\tau$ and unstable beyond a critical delay; if $a + b > 0$, it is unstable for every $\tau$ (Hale and Verduyn Lunel 1993, Chapter 5). A numerical method is called P-stable or GP-stable when it reproduces the delay-independent region (Bellen and Zennaro 2003, Chapter 10).

## Reductions

- **To a sequence of ODEs** (method of steps), for constant or bounded-below delays.
- **To an ODE in infinite dimensions** on $C([-\tau, 0], \mathbb{R}^d)$, and by discretizing the history segment to a large ODE system: a [method of lines](/method-of-lines/) for the transport equation $u_t = u_\theta$ that the segment satisfies.
- **Linear chain trick.** A distributed delay with a gamma kernel $K(\theta) \propto |\theta|^{m-1}e^{a\theta}$ is equivalent to a chain of $m$ extra linear ODEs, which removes the delay exactly.

## Applications

Population dynamics and epidemiology (maturation and incubation periods), physiology (Mackey-Glass, glucose-insulin and respiratory control), control theory (feedback with transport or communication lag), laser dynamics with optical feedback, traffic models with driver reaction time, and neural networks with transmission delays.

## References
