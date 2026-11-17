---
tag: 2J3336
kind: model
slug: chemical-langevin-equation
name: Chemical Langevin equation
aliases:
- CLE
area: biology/systems-biology
level: advanced
summary: 'An SDE limit of the master equation for large counts: drift S a(x) plus noise with a square-root propensity amplitude per reaction.'
history:
  year: 2000
  people: [Daniel T. Gillespie]
  note: Gillespie derived the chemical Langevin equation from the master equation in 2000, by two conditions on a time step, and in 2001 showed it as a limit of tau-leaping.
prereqs: [tau-leaping, stochastic-differential-equation]
see_also: [euler-maruyama-method, chemical-master-equation, linear-noise-approximation, langevin-dynamics, milstein-method, gillespie-algorithm, moment-closure, central-limit-theorem]
sources:
  - paper: doi:10.1063/1.481811
    title: Daniel T. Gillespie, The chemical Langevin equation, Journal of Chemical Physics 113(1), 2000, 297-306
    locator: the derivation from the two conditions on the step, the equation with one noise per reaction, and its Fokker-Planck form
  - paper: doi:10.1063/1.1378322
    title: Daniel T. Gillespie, Approximate accelerated stochastic simulation of chemically reacting systems, Journal of Chemical Physics 115(4), 2001, 1716-1733
    locator: the chemical Langevin equation as the limit of the Poisson leap when every reaction fires many times per step
  - paper: doi:10.1063/1.4885345
    title: David Schnoerr, Guido Sanguinetti and Ramon Grima, The complex chemical Langevin equation, Journal of Chemical Physics 141(2), 2014, 024103
    locator: the failure of the real equation when a propensity becomes negative, and a version in complex variables
  - paper: doi:10.1088/1751-8121/aa54d9
    title: David Schnoerr, Guido Sanguinetti and Ramon Grima, Approximation and inference methods for stochastic biochemical kinetics, a tutorial review, Journal of Physics A 50(9), 2017, 093001
    locator: the section on the chemical Langevin equation and its relation to the master equation and the system size expansion
---

The chemical Langevin equation (CLE) is a [stochastic differential equation](/stochastic-differential-equation/) that approximates the jump process of the [chemical master equation](/chemical-master-equation/) when every reaction fires many times in a time over which the propensities change little. Each reaction contributes a drift $\nu_j a_j(x)$ and a noise $\nu_j \sqrt{a_j(x)}$ driven by its own Brownian motion. The state is real, not an integer vector, and the noise has the right size: its variance per unit time matches the variance of the number of firings. Gillespie (2000) derived it from the master equation by two conditions on a time step, and it sits between the exact jump process and the deterministic rate equations. It is simulated with the [Euler-Maruyama method](/euler-maruyama-method/), and the result is close to a [tau-leaping](/tau-leaping/) run with normal draws in place of Poisson ones. The name refers to the Langevin equation of physics, but the equation here is a different one: [Langevin dynamics](/langevin-dynamics/) adds friction and thermal noise to Newton's equations for particles, while the CLE has no inertia and its noise comes from the random timing of reactions.

## The machine

**State.** $X(t) \in \mathbb{R}^n$, the amounts of $n$ species, as real numbers.

**Equation.** For a network with change vectors $\nu_j$ and propensities $a_j(x)$, $j = 1, \ldots, m$,

$$dX = \sum_{j=1}^{m} \nu_j\, a_j(X)\, dt + \sum_{j=1}^{m} \nu_j \sqrt{a_j(X)}\, dW_j ,$$

with $m$ independent standard Brownian motions $W_j$ and the Itô interpretation. The drift is $S a(X)$, the right side of the [mass action](/mass-action-kinetics/) rate equations written in counts. The diffusion matrix is $D(x) = S \operatorname{diag}(a(x)) S^{\mathsf T}$, and any noise term $B\, dW$ with $B B^{\mathsf T} = D$ gives the same law. So $n$ noises are enough, even when $m > n$.

**Propensities.** The same as for the master equation: $c$ for a source, $c x_A$, $c x_A x_B$, and $c\, x_A(x_A - 1)/2$ for $2A$ with $c = 2k/(N_A V)$. For large counts, $x_A(x_A - 1)/2$ and $x_A^2/2$ differ little.

**Derivation.** Fix $x$ at time $t$ and a step $\tau$. Under condition (i), $\tau$ is small enough that every $a_j$ stays nearly constant on $[t, t + \tau)$; then the numbers of firings are independent Poisson$(a_j(x)\tau)$, the tau-leap. Under condition (ii), $\tau$ is large enough that every $a_j(x)\tau \gg 1$; then each Poisson count is close to normal with mean and variance $a_j(x)\tau$. Together they give

$$X(t + \tau) \approx x + \sum_j \nu_j a_j(x) \tau + \sum_j \nu_j \sqrt{a_j(x)\tau}\, N_j ,$$

with independent standard normal $N_j$, which is one Euler-Maruyama step of the CLE. Both conditions can hold at once only when the counts are large.

**Fokker-Planck form.** The density $p(x, t)$ of $X$ solves

$$\frac{\partial p}{\partial t} = -\sum_i \frac{\partial}{\partial x_i}\bigl[(S a(x))_i\, p\bigr] + \frac{1}{2} \sum_{i, k} \frac{\partial^2}{\partial x_i \partial x_k}\bigl[D_{ik}(x)\, p\bigr],$$

the chemical Fokker-Planck equation, which is the master equation with the jumps expanded to second order.

## What it counts

The CLE gives sample paths and a density over real-valued amounts. It is good for the bulk of the distribution when every species that reacts has a large count: means, variances, correlations and the shape of fluctuations near a stable state. It is poor for anything that depends on single molecules: the probability of extinction, the time to reach 0, the switching rate between the states of a bistable circuit, and distributions over counts below about 10.

**Pure death, a linear case.** $X \to \emptyset$ at rate 1 per molecule gives $dX = -X\, dt + \sqrt{X}\, dW$. From $X(0) = 100$, the mean $m$ and the variance $V$ solve $\dot m = -m$ and $\dot V = -2V + m$, the same equations as for the master equation, so $X(1)$ has mean 36.787944 and variance 23.254416 exactly. Euler-Maruyama runs with step 0.01 give a mean of 36.75 and a variance of 23.42. Higher moments are not exact: the master equation gives a Binomial law, and the CLE a continuous one.

**Pure death, a failure.** From $X(0) = 5$ to $t = 3$, the exact probability that all molecules are gone is $(1 - e^{-3})^5 = 0.7746$. The CLE has no atom at 0: a path near 0 reaches 0 and then the square root of a negative propensity is not defined. With step 0.001, 58.6 percent of the paths cross 0 before $t = 3$, and what to do with them is a choice of the method, not part of the model.

**Immigration-death.** $\emptyset \to X$ at rate 10 and $X \to \emptyset$ at rate $x$ give $dX = (10 - X)\, dt + \sqrt{10 + X}\, dW$. The stationary mean and variance are 10 and 10, the same as for the exact Poisson$(10)$ law. Euler-Maruyama runs with step 0.01 give 9.95 and 9.80. For this linear drift, Euler-Maruyama with step $h$ has a stationary variance near $20/(2 - h)$ rather than 10, so the step adds its own bias.

## Relation to other models

- **The master equation.** The CLE is an approximation of the jump process. It keeps the first two conditional moments of the increments, $\mathbb{E}[dX] = S a\, dt$ and $\operatorname{Cov}[dX] = D\, dt$, and drops the higher ones.
- **Tau-leaping.** A Poisson leap with every $a_j\tau$ large is close to an Euler-Maruyama step of the CLE (Gillespie 2001).
- **The rate equations.** Dropping the noise gives $\dot x = S a(x)$. In concentrations $x/V$, the noise has size $1/\sqrt{V}$, so the rate equations are the limit as $V \to \infty$.
- **The linear noise approximation.** Linearizing the CLE around the solution of the rate equations gives an Ornstein-Uhlenbeck type process whose covariance solves a [Lyapunov equation](/lyapunov-equation/). This is the [linear noise approximation](/linear-noise-approximation/). The CLE and the LNA agree to the first order in $V^{-1/2}$ and differ at the next order.
- **Langevin equations in physics.** [Langevin dynamics](/langevin-dynamics/) is a model of particles with positions and velocities, friction and thermal noise, and its noise strength is fixed by the temperature. In the CLE the noise strength depends on the state through the propensities, and there are no velocities.
- **Moment closure.** For linear networks the moment equations of the CLE and of the master equation coincide up to order 2. For nonlinear networks they differ, and [moment closure](/moment-closure/) applied to the CLE gives other results than applied to the master equation.

## Known results in the model

- **Derivation.** Under the two conditions on the step, the master equation gives the CLE (Gillespie 2000). The conditions are heuristic: there is no error bound for a given network and count, only the scaling with $V$.
- **Exact second moments for linear networks.** If every propensity is affine in $x$ (reactions of order 0 and 1), the means and covariances of the CLE solve the same linear equations as those of the master equation, so they are exact. The higher cumulants are not.
- **Large volume.** With counts proportional to $V$, the CLE in concentrations approximates the jump process better than the rate equations do: the rate equations miss fluctuations of size $V^{-1/2}$, and the CLE captures them, with errors of a smaller order.
- **Boundaries.** Solutions can leave the region where all propensities are $\ge 0$, and then the real equation is not defined. Rules such as setting negative propensities to 0, or reflecting at 0, change the model. Schnoerr, Sanguinetti and Grima (2014) gave a version in complex variables whose moments remain well defined.
- **Rare events.** For a bistable network, the CLE gives the stable states and the shape of the fluctuations near them, but the mean switching time can be wrong by orders of magnitude, because it depends on the tails of the jump distribution, which the CLE does not keep.
- **Numerical methods.** [Euler-Maruyama](/euler-maruyama-method/) has strong order 1/2 and weak order 1 for this equation with smooth propensities away from the boundary. The noise is not commutative when several reactions change the same species, so the [Milstein method](/milstein-method/) needs Lévy areas to reach strong order 1.

## References
