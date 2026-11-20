---
tag: 6HJ81K
kind: algorithm
slug: coarse-projective-integration
name: Coarse projective integration
aliases:
- equation-free method
area: scientific-computing/multiscale-methods
level: advanced
summary: Runs short bursts of a fine simulator, estimates the time derivative of coarse variables, and takes a large projective step with no coarse equation.
model: real-ram
complexity:
  vars: {n: the number of outer steps, k: the number of healing steps per outer step, s: the cost of one micro step, d: the size of the fine state}
  time: {worst: "Θ(n (k + 1) s)"}
  space: {extra: "Θ(d)"}
properties: {deterministic: true, equation_free: true, explicit: true, first_order: true}
history:
  year: 2003
  people: [C. William Gear, Ioannis G. Kevrekidis]
  note: Gear and Kevrekidis introduced projective integration for stiff systems with a gap in the spectrum in 2003, and with coauthors made it the coarse time stepper of the equation-free framework in the same year.
prereqs: [euler-method, stiff-ode-problem, multiscale-modeling]
see_also: [stability-region, a-stability, parareal-algorithm, heterogeneous-multiscale-method, model-order-reduction, newton-method-for-systems, mori-zwanzig-formalism, kinetic-monte-carlo]
sources:
  - paper: doi:10.1137/S1064827501388157
    title: C. William Gear and Ioannis G. Kevrekidis, Projective methods for stiff differential equations, problems with gaps in their eigenvalue spectrum, SIAM Journal on Scientific Computing 24(4), 2003, 1091-1106
    locator: projective forward Euler, its amplification polynomial and the shape of its stability region for stiff systems with a gap in the spectrum
  - paper: doi:10.4310/CMS.2003.v1.n4.a5
    title: Ioannis G. Kevrekidis, C. William Gear, James M. Hyman, Panagiotis G. Kevrekidis, Olof Runborg and Constantinos Theodoropoulos, Equation-free, coarse-grained multiscale computation, enabling microscopic simulators to perform system-level analysis, Communications in Mathematical Sciences 1(4), 2003, 715-762
    locator: the coarse time stepper built from lifting, short micro simulation and restriction, and its use for coarse projective integration
---

Coarse projective integration advances the coarse variables of a fine simulator, such as a molecular dynamics, kinetic Monte Carlo or lattice Boltzmann code, over long times without a closed equation for them. Each outer step builds a fine state from the coarse state, runs the fine simulator for a short burst, estimates the time derivative of the coarse variables from the end of the burst, and extrapolates them over a much longer interval. The fine simulator is used as a black box and only for a fraction of the time interval. The method works when the coarse variables evolve slowly and all other variables relax quickly to values set by them, which is a gap in the spectrum of time scales. It is the time stepper of the equation-free method of Kevrekidis, Gear and coauthors.

## In plain words

Suppose a detailed simulation is correct but too slow to run for the whole time of interest, and only a few averages of it matter. The averages change slowly. Coarse projective integration runs the detailed simulation for a short time, looks at how fast the averages change at the end, and jumps ahead along that trend for a long time. Then it builds a new detailed state that matches the averages and repeats. The first part of each burst is wasted on purpose: the new state is not quite right, and the quick details need time to settle before the trend can be read.

## The problem

Given a fine simulator $\Phi_{\delta t}$ that advances a fine state $u$ by a micro step $\delta t$, a restriction $\mathcal{R}$ that maps a fine state to coarse variables $X$, a lifting $\mathcal{L}$ that maps coarse variables to a fine state with $\mathcal{R}\mathcal{L} X = X$, a start value $X_0$ and a final time, approximate the coarse variables $X(t) = \mathcal{R} u(t)$ of the fine evolution with far fewer micro steps than the whole interval needs. The method assumes that after a short time the coarse variables evolve by a closed equation $X' = F(X)$, which is not known.

## The algorithm

```pseudo id=main
CPI(X, lift, micro step Φ of length δt, restrict, k, M, n)
L1  for outer step = 1 .. n do
L2      u ← lift(X)
L3      run k + 1 micro steps u ← Φ(u), and record X_k and X_{k+1}, the restrictions after steps k and k + 1
L4      s ← (X_{k+1} - X_k) / δt                        ▷ estimate of the coarse time derivative
L5      X ← X_{k+1} + M δt s                            ▷ projective step
L6  return X
```

The first $k$ micro steps of line L3 heal the lift: they let the fine variables that the lift did not set correctly relax to the slow manifold. Line L4 is a finite difference estimate of $F(X)$ on the slow manifold, and line L5 is a forward Euler step with it. An outer step advances the time by $(M + k + 1)\delta t$ and costs $k + 1$ micro steps, so the saving is the factor $(M + k + 1)/(k + 1)$. For a stochastic simulator, line L3 runs an ensemble, and the restriction averages over it. The derivative of line L4 is then estimated by a least squares fit over the last few micro steps.

When the fine simulator is an ODE solver for $y' = f(y)$ and the lift and the restriction are the identity, the method is projective forward Euler. On $y' = \lambda y$ with $\zeta = 1 + \delta t\, \lambda$, one outer step multiplies $y$ by the amplification polynomial

$$\sigma(\zeta) = \big((M + 1)\zeta - M\big)\zeta^k.$$

## Example

Take $y' = A y$ with $A = R \operatorname{diag}(-1, -1000) R^T$, where $R$ is the rotation by $0.3$ radians, $y_0 = (1, 1)$ and $\delta t = 5 \times 10^{-4}$. Forward Euler is stable only for $\delta t \le 0.002$. The fast Euler factor is $\zeta = 1 - 0.5 = 0.5$, and the slow factor is $0.9995$.

- **Stability needs enough healing steps.** With $M = 100$, an outer step covers $109\,\delta t = 0.0545$ for $k = 8$. The fast factor is $\sigma(0.5) = (50.5 - 100)/256 = -0.193$, and the slow factor is $0.94571$ against the exact $e^{-0.0545} = 0.94696$. After 10 outer steps, $y = (0.6838, 0.2115)$ and the exact solution is $(0.6929, 0.2143)$, which is an error of $0.0095$. With $k = 4$, $\sigma(0.5) = -49.5/16 = -3.09$, and 10 outer steps give $(-15662, 50633)$.
- **First order.** With $k = 8$ and outer steps $49\,\delta t$, $98\,\delta t$ and $196\,\delta t$ ($M = 40$, $89$, $187$), the errors at $T = 0.98$ are $0.0040$, $0.0097$ and $0.0216$. Plain forward Euler with 1960 steps has error $1.2 \times 10^{-4}$; projective Euler with $M = 40$ uses 360 micro steps.
- **Coarse variables and lifting.** Take $x' = -y$, $y' = 1000 (x - y)$, with the coarse variable $x$. The variable $y$ relaxes quickly to near $x$, and $x$ then decays at the slow rate $-1.001$. With the lift $(X, X)$, $k = 8$ and $M = 40$, the coarse error at $T = 0.98$ is $0.0032$. With the poor lift $(X, 0)$ and outer steps of $49\,\delta t$, the error is $0.625$, $0.111$, $0.033$ and $0.013$ for $k = 0$, $2$, $4$ and $8$. Without healing, $x$ does not move at all, because the first micro step sees $y = 0$.

## Correctness

The [proof](proofs/correctness.md) treats projective forward Euler on a linear system with real negative eigenvalues. One outer step is $\sigma(I + \delta t A)$, so each eigenvector component evolves by itself. A fast component with $|1 + \delta t \lambda| \le \rho$ is not amplified if $\rho^k \le 1/(2M + 1)$: the projection can multiply it by at most $2M + 1$, and the $k$ healing steps damp it by $\rho^k$. For a slow component, $|\sigma(1 + z) - e^{m z}| \le m^2 z^2 / 2$ with $m = M + k + 1$, so after $n$ outer steps up to time $T$ the error is at most $T H \lambda^2 / 2$ times the size of the component, with $H = m\,\delta t$: the method is first order in the outer step. The stability region in the $\zeta$ plane is the union of a region near $\zeta = 1$ of size about $1/M$ and a region near $\zeta = 0$, which makes the method suited to a gap in the spectrum and not to a continuous spread of time scales.

For a general fine simulator, the argument holds on the slow manifold. The proof page explains why the lifting error adds a term at every outer step, which the example shows as the remaining error $0.013$ of the poor lift.

## Complexity

In the [real RAM](/real-ram/) model, each outer step runs $k + 1$ micro steps of cost $s$, plus a lift and two restrictions, which cost $\Theta(d)$ for a fine state of size $d$ when they are simple. So $n$ outer steps cost $\Theta(n (k + 1) s)$, against $\Theta(n (M + k + 1) s)$ for running the fine simulator over the same time. The extra space is $\Theta(d)$ for the current fine state. A stochastic simulator multiplies the cost by the ensemble size that the derivative estimate needs.

## Properties

- **Equation free.** The coarse equation $X' = F(X)$ is never written down. It is evaluated through the fine simulator.
- **Explicit.** Each outer step uses only forward runs of the fine simulator, so any existing code can be wrapped without changes.
- **First order.** Projective forward Euler is first order in the outer step. Higher order outer integrators use several projective derivative estimates.
- **Split stability region.** The method is stable for modes near $\zeta = 0$ and near $\zeta = 1$ and unstable between them.

## Variants and improvements

- **Higher order outer integrators.** Projective Runge-Kutta and Adams methods use derivative estimates from several bursts.
- **Telescopic projective integration.** Nest projective steps inside projective steps to treat several gaps in the spectrum.
- **Patch dynamics and the gap-tooth scheme.** Run the fine simulator only in small patches of space as well as for short bursts of time, and interpolate the coarse fields between them.
- **Coarse fixed points and bifurcations.** Use the coarse time stepper of lines L2 and L3 with Newton-Krylov methods or [Newton's method for systems](/newton-method-for-systems/) to find coarse steady states and their stability, without a coarse equation.
- **Constrained runs for lifting.** Choose the unset fine variables by running the fine simulator with the coarse variables held fixed, so that the lift starts near the slow manifold.

## When to use it

Use coarse projective integration when a trusted fine simulator exists, the quantities of interest are a few coarse variables, and there is a clear separation between their slow evolution and the fast relaxation of everything else, but no closed coarse equation is known. Typical cases are kinetic Monte Carlo or molecular dynamics of a reaction, agent-based models and lattice Boltzmann codes. For an ODE whose equations are known, a stiff implicit solver is usually better. If there is no gap in the time scales, the derivative estimate of line L4 is not a function of the coarse state alone and the method does not apply.

## Pitfalls

- **Too few healing steps.** If $\rho^k$ is larger than about $1/(2M + 1)$, the fast modes are amplified at every outer step and the solution blows up, as in the example with $k = 4$.
- **A poor lift.** The lifting error returns at every outer step. Healing reduces it but does not remove the drift of the slow variables during the healing, so the error grows with the number of outer steps.
- **Noise in the derivative.** For a stochastic simulator, the noise of $X_{k+1} - X_k$ is divided by $\delta t$ and multiplied by $M \delta t$, so the projective step amplifies it by $M$. The ensemble must be large or the derivative must be fitted over many micro steps.
- **Wrong coarse variables.** If the chosen coarse variables do not close, there is no slow manifold parametrized by them, and the derivative depends on the hidden variables.
- **Oscillatory fast modes.** Fast modes with large imaginary parts may lie outside the region near $\zeta = 0$ even after healing, if the micro step does not damp them.

## Implementations

## History

Gear and Kevrekidis introduced projective integration in 2003 as an explicit method for stiff systems whose eigenvalues have a gap, and analyzed the stability region of projective forward Euler. In the same year Kevrekidis, Gear, Hyman, Kevrekidis, Runborg and Theodoropoulos described the equation-free framework, in which the coarse time stepper built from lifting, a short fine simulation and restriction is used for projective integration, coarse fixed point computation and bifurcation analysis. Later work added telescopic and higher order projective methods, patch dynamics in space and analysis for stochastic simulators.

## References
