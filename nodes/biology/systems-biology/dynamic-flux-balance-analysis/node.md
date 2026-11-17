---
tag: 4C9MZV
kind: algorithm
slug: dynamic-flux-balance-analysis
name: Dynamic flux balance analysis
aliases:
- dFBA
area: biology/systems-biology
level: advanced
summary: Couple FBA at each time step with ODEs for biomass and external metabolites, so that uptake bounds change as the medium is used up.
model: real-ram
complexity:
  vars: {N: the number of time steps, K: the number of medium species, m: the number of reactions, T: the time of one FBA linear program}
  time: {worst: O(N (T + K m))}
  space: {extra: O(N K + T)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2002
  people: [Radhakrishnan Mahadevan, Jeremy S. Edwards, Francis J. Doyle III]
  note: Mahadevan, Edwards and Doyle named the static and the dynamic optimization approaches and used them for the diauxic growth of Escherichia coli on glucose and acetate. Varma and Palsson had already predicted batch culture time courses with one LP per time step in 1994.
prereqs: [flux-balance-analysis, euler-method]
see_also: [ode-initial-value-problem, runge-kutta-methods, stiff-ode-problem, michaelis-menten-kinetics, parametric-linear-programming, minimization-of-metabolic-adjustment, flux-variability-analysis, constraint-based-metabolic-modeling]
sources:
  - paper: doi:10.1016/S0006-3495(02)73903-9
    title: Radhakrishnan Mahadevan, Jeremy S. Edwards and Francis J. Doyle III, Dynamic flux balance analysis of diauxic growth in Escherichia coli, Biophysical Journal 83(3), 2002, 1331-1340
    locator: the static optimization approach (one LP per time step) and the dynamic optimization approach (one NLP over the whole time course)
  - paper: doi:10.1128/aem.60.10.3724-3731.1994
    title: Amit Varma and Bernhard O. Palsson, Stoichiometric flux balance models quantitatively predict growth and metabolic by-product secretion in wild-type Escherichia coli W3110, Applied and Environmental Microbiology 60(10), 1994, 3724-3731
    locator: the time profiles of batch cultures computed from one LP per time interval
  - paper: doi:10.1002/bit.24748
    title: Kai Höffner, Stuart M. Harwood and Paul I. Barton, A reliable simulator for dynamic flux balance analysis, Biotechnology and Bioengineering 110(3), 2013, 792-802
    locator: dFBA as an ODE with an embedded LP, solved with lexicographic optimization and event detection when the optimal basis changes
---

Dynamic flux balance analysis (dFBA) extends [flux balance analysis](/flux-balance-analysis/) from one steady state to a time course in a batch or fed-batch culture. Inside the cell, fluxes are assumed to be at a quasi steady state and optimal for growth. Outside the cell, the biomass and the concentrations of the medium species change slowly, by ordinary differential equations whose rates are the exchange fluxes times the biomass. In the static optimization approach of Mahadevan, Edwards and Doyle (2002), each time step solves one FBA problem with uptake bounds set by the current medium, for example by Michaelis-Menten kinetics, and then moves the biomass and the medium forward by one step of an ODE method. The method predicts growth curves, substrate depletion and by-product secretion, including switches between metabolic modes.

## In plain words

FBA describes a cell at one moment. In a flask, the food runs out and waste piles up, so the best way to grow changes over time. dFBA cuts time into short steps.

At the start of each step, look at how much food is left. Less food means the cell can take it in more slowly, so the speed limit on the food door goes down. Solve FBA with that limit to get the growth rate and the rates of food use and waste output. Then move the clock forward: the cells grow a little, the food goes down a little, and the waste goes up a little. Repeat until the food is gone. The result is a curve over time for the cells, the food and the waste.

## The problem

**Input.**

- A network with matrix $S$, flux bounds $lb, ub$ and the biomass reaction $b$, as for FBA.
- Medium species $k = 1, \ldots, K$ with initial concentrations $z_k(0)$ (mmol/L), and the initial biomass $X(0)$ (gDW/L).
- A matrix $E$ that maps the fluxes to the medium: $(E v)_k$ is the rate of change of $z_k$ per gram of biomass.
- For each uptake reaction $j$ of species $k$, a rate law for its upper bound, here the Michaelis-Menten form $v^{\max}_j z_k / (K_j + z_k)$.
- A step $\Delta t$ and a number of steps $N$.

**Output.** The time course of $X$ and $z$, and the flux vector at each step, approximating the solution of

$$\frac{dX}{dt} = \mu(z) X, \qquad \frac{dz}{dt} = (E v(z)) X,$$

where $v(z)$ is an FBA optimum for the bounds set by $z$, and $\mu(z) = v_b(z)$ is its growth rate.

## The algorithm

```pseudo id=main
DFBA-SOA(S, lb, ub, b, E, uptakes, X0, z0, Δt, N)
L1  t ← 0; X ← X0; z ← z0
L2  for i ← 1 to N:
L3      for each uptake j of species k: ub_j ← min(vmax_j z_k / (K_j + z_k), z_k / (X Δt))
L4      v ← FBA(S, lb, ub, b)
L5      if the LP is infeasible then record the state and stop
L6      z ← z + Δt (E v) X; X ← X + Δt v_b X
L7      t ← t + Δt
L8  return the recorded time course
```

Line L3 sets the uptake bounds from the current medium. The second term in the minimum keeps the step from using more substrate than is left, so the concentration cannot become negative. Line L4 is one exact LP. Line L6 is one explicit [Euler step](/euler-method/). The code also has the variant of Varma and Palsson, which holds $v$ fixed over the step and integrates exactly: $X$ is multiplied by $e^{\mu \Delta t}$, and $z_k$ changes by $(E v)_k X (e^{\mu \Delta t} - 1)/\mu$.

## Example

The overflow network has four internal metabolites, a substrate $A$, oxygen $O$, an energy carrier $E$ and a by-product $P$, and six reactions:

| reaction | equation | bound |
|---|---|---|
| EX_A | $\emptyset \to A$ | Monod uptake, $v^{\max} = 10$, $K = 1$ |
| EX_O | $\emptyset \to O$ | at most 1 |
| RESP | $A + O \to 2E$ | |
| FERM | $A \to E + P$ | |
| EX_P | $P \to \emptyset$ | secreted into the medium |
| BIO | $5A + 5E \to \emptyset$ | growth rate |

For an uptake $u$, respiration gives $\frac{2}{15}$ units of growth per unit of $A$ and fermentation gives $\frac{1}{10}$, but respiration is limited by oxygen. So the FBA optimum has a closed form. If $u \le 3$, all substrate is respired and $\mu = \frac{2u}{15}$. If $u > 3$, oxygen is at its bound, the rest is fermented, and $\mu = \frac{u + 1}{10}$ with the secretion $\frac{u - 3}{2}$ of $P$. This is overflow metabolism: at high uptake the cell secretes a by-product even with oxygen present.

Start with $X = 0.05$, a substrate $s = 10$ and no $P$, and take $\Delta t = 0.01$ h:

| $t$ | $X$ | $s$ | $p$ | mode |
|---|---|---|---|---|
| 0 | 0.05 | 10 | 0 | overflow, $\mu \approx 1.009$ |
| 1 | 0.1361 | 9.2247 | 0.2593 | overflow |
| 2 | 0.3655 | 7.1623 | 0.9432 | overflow |
| 3 | 0.9160 | 2.2617 | 2.4868 | overflow |
| 3.34 | 1.1359 | 0.4131 | 2.8856 | respiration only from here |
| 4 | 1.1909 | 0.0002 | 2.8856 | substrate used up |

While $s$ is high, the uptake is above 3 and the cells secrete $P$. When $s$ falls below $\frac{3}{7}$, the uptake drops below 3 and the cells switch to respiration only, so $p$ stops rising. A reference solution of the same ODE by RK4 with step $10^{-3}$ gives $X = 1.1915$ and $p = 2.8775$ at $t = 4$. The Euler errors for $\Delta t = 0.04, 0.02, 0.01$ are about 0.035, 0.017 and 0.0087, so the error halves when the step halves, as expected for a first-order method.

The tests check the code against a hand Euler run of the closed-form ODE, the switch from overflow to respiration, this first-order convergence, the conservation of $X + \frac{2}{15} s$ when oxygen is not limiting, the exact exponential solution when the uptake is constant, and that the medium never becomes negative with a large step.

## Correctness

Each step solves the FBA problem for the current bounds exactly, so the growth rate and the fluxes are an exact FBA optimum for those bounds. The update is the explicit Euler step of the ODE with the flux vector of the step, or, in the variant, the exact solution of the ODE with the flux vector held constant over the step. With the cap in line L3, the uptake in one step is at most what is in the medium, so the substrate concentration stays non-negative when the uptake reaction is its only consumer. When the growth yield is constant, the Euler update keeps the biomass plus the yield times the substrate exactly constant. If the map from the medium to the FBA optimum is Lipschitz, the Euler method converges with error of order $\Delta t$; this is the standard theorem for the Euler method, and it holds for the overflow network away from depletion. The full proof is below.

## Complexity

- **Per step.** One LP in time $T$ and an update in $O(K m)$ for $E v$. The total time is $O(N (T + K m))$ for $N$ steps. This is a count of operations.
- **Warm starts.** The bounds change a little from step to step, so the optimal basis often stays the same. A solver that starts from the last basis needs few or no pivots per step. Höffner, Harwood and Barton (2013) go further and integrate the ODE with a fixed basis until an event shows that the basis is no longer optimal; this gives an exact piecewise solution with adaptive steps.
- **Step size.** The Euler error is of order $\Delta t$, so halving the error doubles the number of LPs. An adaptive ODE method with the LP inside the right side is usual for large models.
- **Space.** $O(N K)$ for the time course, plus the space of one LP.

## Properties

- **Not exact.** The time course is an approximation of the ODE with error of order $\Delta t$ for the Euler update. Each LP inside it is exact.
- **Quasi steady state.** The method assumes that intracellular metabolism is much faster than the change of the medium, the same assumption as in the [quasi-steady-state approximation](/quasi-steady-state-approximation/).
- **Non-unique fluxes.** When the FBA optimum is not unique, the solver picks one optimal vertex, and the secretion fluxes (not the growth rate) can jump between steps. The ODE is then not well defined by FBA alone. Höffner and co-authors fix this with a lexicographic order of secondary objectives.
- **Mode switches.** Changes of the optimal basis show up as switches of metabolic mode, such as the switch from overflow to respiration in the example, or from glucose to acetate in diauxic growth.
- **Infeasible steps.** If a lower bound, such as a maintenance flux, cannot be met with the medium left, the LP is infeasible and the static approach stops. Models usually relax such bounds or let the biomass decay.

## Variants and improvements

- **Static optimization approach (SOA).** The method of this page: one LP per time step (Mahadevan, Edwards and Doyle 2002, following Varma and Palsson 1994).
- **Dynamic optimization approach (DOA).** Optimize over the whole time course at once, for example the final biomass, as one nonlinear program after a discretization in time. It allows rate limits on how fast fluxes change, at a much higher cost.
- **Direct approach with an ODE solver.** Put the LP inside the right side of an adaptive ODE solver, with event detection when the optimal basis changes (Höffner, Harwood and Barton 2013).
- **Community dFBA.** Several species share one medium, each with its own FBA problem per step. This models cross-feeding and competition.
- **Spatial dFBA.** One dFBA model per grid cell, coupled by diffusion of the medium species, models colonies and biofilms.

## When to use it

Use dFBA when the medium changes during the experiment, as in batch and fed-batch cultures, and you want growth curves, substrate use and by-product profiles from a genome-scale model without a full kinetic model. It needs uptake kinetics for the limiting substrates and a growth objective. For one steady condition, plain FBA is enough. For fast transients inside the cell, such as the response to a pulse of substrate in seconds, a kinetic model is needed, since dFBA assumes that the cell is always at its optimum.

## Pitfalls

- **Negative concentrations.** Without the cap $z_k / (X \Delta t)$ on the uptake, a large step can use more substrate than is left.
- **Jumps from alternate optima.** Secretion fluxes can change at random between steps if the FBA optimum is not unique. Fix them with a secondary objective, or report the growth rate only.
- **Stiffness.** Near depletion, the uptake changes fast compared with the step. A fixed step that is too large gives oscillations; an adaptive step or event detection avoids them.
- **Units.** Fluxes are per gram of biomass per hour, and $X$ is in grams per liter, so $(E v) X$ is in mmol per liter per hour. Mixing time units between the uptake law and the step is a common error.
- **Infeasibility at the end.** A maintenance requirement that the medium can no longer support makes the LP infeasible. Decide in advance what the model does then.

## Implementations

## History

Varma and Palsson (1994) predicted the time profiles of E. coli batch cultures, including by-product secretion, from an FBA model solved at successive time intervals with the medium updated between them. Mahadevan, Edwards and Doyle (2002) named this the static optimization approach, contrasted it with a dynamic optimization over the whole time course, and applied both to diauxic growth of E. coli on glucose and acetate. Höffner, Harwood and Barton (2013) gave a simulator that treats dFBA as an ODE with an embedded LP and handles changes of the optimal basis and alternate optima with events and lexicographic optimization.

## References
