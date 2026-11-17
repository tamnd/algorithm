---
tag: Q8TJ4W
kind: algorithm
slug: tau-leaping
name: Tau-leaping
aliases:
- explicit tau-leaping
area: biology/systems-biology
level: advanced
summary: Approximate stochastic simulation that fires a Poisson number of each reaction in a step tau over which propensities change little.
model: real-ram
complexity:
  vars: {n: the number of species, m: the number of reactions, L: the number of leaps in the run, epsilon: the error control parameter}
  time: {expected: O(L m n)}
  space: {extra: Θ(n + m)}
properties: {deterministic: false, randomized: true, exact: false, recursive: false}
history:
  year: 2001
  people: [Daniel T. Gillespie, Yang Cao, Linda R. Petzold]
  note: Gillespie proposed tau-leaping in 2001. Cao, Gillespie and Petzold added critical reactions against negative counts in 2005 and the step size rule used here in 2006.
prereqs: [gillespie-algorithm, poisson-distribution]
see_also: [chemical-langevin-equation, euler-maruyama-method, next-reaction-method, chemical-master-equation, stiff-ode-problem, multilevel-monte-carlo, binomial-distribution, stochastic-sir-model]
sources:
  - paper: doi:10.1063/1.1378322
    title: Daniel T. Gillespie, Approximate accelerated stochastic simulation of chemically reacting systems, Journal of Chemical Physics 115(4), 2001, 1716-1733
    locator: the leap condition, the Poisson leap, and its limits as the chemical Langevin equation and the rate equations
  - paper: doi:10.1063/1.1992473
    title: Yang Cao, Daniel T. Gillespie and Linda R. Petzold, Avoiding negative populations in explicit Poisson tau-leaping, Journal of Chemical Physics 123(5), 2005, 054104
    locator: the critical reactions, which are fired at most once per leap
  - paper: doi:10.1063/1.2159468
    title: Yang Cao, Daniel T. Gillespie and Linda R. Petzold, Efficient step size selection for the tau-leaping simulation method, Journal of Chemical Physics 124(4), 2006, 044109
    locator: Section II C and eqs. 27 and 33 (the factors g_i and the step size), and Section IV (the full procedure, with the switch to exact steps)
  - paper: doi:10.1063/1.1627296
    title: Muruhan Rathinam, Linda R. Petzold, Yang Cao and Daniel T. Gillespie, Stiffness in stochastic chemically reacting systems, the implicit tau-leaping method, Journal of Chemical Physics 119(24), 2003, 12784-12794
    locator: the implicit leap for systems with fast reactions that reach equilibrium
---

Tau-leaping is an approximate method for the jump process of the [chemical master equation](/chemical-master-equation/). The exact methods, such as the [Gillespie algorithm](/gillespie-algorithm/), fire one reaction per step, so their cost is the number of reaction events, which is huge when the counts are large. Tau-leaping takes a step of length $\tau$ and fires every reaction $j$ a random number of times, drawn from a [Poisson](/poisson-distribution/) law with mean $a_j(x)\tau$, with the propensities frozen at the start of the step. This is exact if the propensities do not change in the step, and it is a good approximation if $\tau$ is small enough that they change little: the *leap condition*. The method of Cao, Gillespie and Petzold (2006) chooses $\tau$ from a parameter $\epsilon$ to meet that condition, fires the reactions that are about to use up a reactant at most once per step, and falls back to exact steps when a leap would be too short to be worth it. It is the stochastic analogue of the explicit Euler method, with the same problems for stiff systems.

## In plain words

The exact method moves one reaction at a time. With a million molecules that is a huge number of tiny moves.

Tau-leaping takes a bigger jump in time instead. It asks: over the next short while, about how many times will each reaction happen? If the counts barely change in that while, each reaction keeps about the same speed, and the number of times it happens is a known kind of random count. So draw those counts, apply them all at once, and jump the clock forward.

The catch is the word "barely". Jump too far and the speeds you used are out of date, so the answer drifts from the truth, and a jump can even take away more molecules than exist. The method picks the jump length so the speeds stay nearly the same, and goes back to one reaction at a time when molecules are scarce.

## The problem

**Input.** A network with $n$ species and $m$ reactions: change vectors $\nu_j$, mass action propensities $a_j(x)$, and the reactant orders of each reaction; a start state $x_0$; an end time $T$; the error control parameter $\epsilon$ (0.03 is common); the threshold $n_c$ for critical reactions (10 is common).

**Output.** An approximate sample path of the jump process $X$ on $[0, T]$: times and states, with every count $\ge 0$.

**The leap.** If in state $x$ the propensities stay at $a_j(x)$ for all of $[t, t + \tau)$, the numbers of firings $K_j$ are independent with $K_j \sim$ Poisson$(a_j(x)\tau)$, and

$$X(t + \tau) = x + \sum_{j=1}^{m} K_j\, \nu_j .$$

**The step size.** Let $\hat\mu_i = \sum_j \nu_{ij} a_j(x)$ and $\hat\sigma_i^2 = \sum_j \nu_{ij}^2 a_j(x)$, over the noncritical reactions, for each species $i$ that is a reactant somewhere. The rule of Cao, Gillespie and Petzold (2006, eq. 33) is

$$\tau' = \min_i \left\{ \frac{\max(\epsilon x_i / g_i, 1)}{|\hat\mu_i|},\ \frac{\max(\epsilon x_i / g_i, 1)^2}{\hat\sigma_i^2} \right\},$$

which bounds the expected change and the standard deviation of the change of each $x_i$ in one leap by $\epsilon x_i / g_i$ (or by 1 for small counts). The factor $g_i$ depends on the highest order reaction in which species $i$ is a reactant (eq. 27): $g_i = 1$ for first order, $g_i = 2$ for $X_i + X_k$, $g_i = 2 + 1/(x_i - 1)$ for $2X_i$, and similar values for third order. It makes the relative change of every propensity at most about $\epsilon$.

## The algorithm

A reaction is *critical* if it can fire fewer than $n_c$ more times before one of its reactants runs out.

```pseudo id=main
TAU-LEAP(x0, ν, a, T, ε, n_c)
L1  t ← 0; x ← x0; record (0, x)
L2  while t < T do
L3      compute a_j(x) and a0; if a0 = 0 then return the record
L4      mark reaction j critical if a_j(x) > 0 and it can fire fewer than n_c times
L5      τ' ← the step size of eq. 33 over the noncritical reactions
L6      if τ' < 10 / a0 then do 100 steps of the direct method and go to L2
L7      τ'' ← Exp(a0c), where a0c is the sum of the critical propensities (∞ if a0c = 0)
L8      τ ← min(τ', τ'', T - t)
L9      K_j ← Poisson(a_j(x) τ) for each noncritical j; K_j ← 0 for each critical j
L10     if τ = τ'' then pick one critical j with probability a_j / a0c and set K_j ← 1
L11     if x + Σ K_j ν_j has a negative entry then τ' ← τ' / 2 and go to L7
L12     t ← t + τ; x ← x + Σ K_j ν_j; record (t, x) if some K_j > 0
```

Line L6 is the switch to exact steps: a leap shorter than about 10 mean waiting times saves nothing, so the method runs the exact method for a while. Lines L7 and L10 let the critical reactions fire at most once per leap, at the rate of an exact step. Line L11 is a safety net, and with critical reactions it is rarely used.

## Example

**A fixed step on pure death.** Take $X \to \emptyset$ at rate 1 per molecule, $x_0 = 100$, and leap with a fixed $\tau$ (no critical reactions, no switch). A leap maps $x$ to $x - K$ with $K \sim$ Poisson$(x\tau)$, so the mean is multiplied by $1 - \tau$ per leap, and the mean at $t = 1$ is $100(1 - \tau)^{1/\tau}$. The variance follows from $V_{k+1} = (1 - \tau)^2 V_k + \tau m_k$.

| $\tau$ | leaps | mean at $t = 1$ | variance at $t = 1$ |
|---|---|---|---|
| 0.5 | 2 | 25.000 | 37.500 |
| 0.1 | 10 | 34.868 | 25.234 |
| 0.01 | 100 | 36.603 | 23.440 |
| exact | about 63 events | 36.788 | 23.254 |

The error of the mean is of order $\tau$, as for the Euler method. With $\tau = 0.01$ the leap uses more steps than the exact method uses events, so for 100 molecules leaping does not pay.

**The adaptive step on 1000 molecules.** With $x_0 = 1000$ and $\epsilon = 0.03$, line L5 gives $\tau' = \min(\epsilon, \epsilon^2 x) = 0.03$ while $x > 33$. A run to $t = 1$ takes about 34 leaps, against an average of $1000(1 - e^{-1}) = 632$ events for the exact method. The mean over 200 runs is 363.5, and the leap chain with $\tau = 0.03$ predicts $1000 \cdot 0.97^{33} \cdot 0.99 = 362.3$, against the exact 367.9: about 1.5 percent low.

**Noise is distorted too.** For immigration-death ($\emptyset \to X$ at rate $b$, $X \to \emptyset$ at rate $x$), a leap chain with a fixed $\tau$ has the right stationary mean $b$, but the stationary variance $2b/(2 - \tau)$ instead of $b$. With $\tau = 0.1$ and $b = 10$ that is 10.526; with $\tau = 0.5$ it is 13.33. With $b = 1000$, the adaptive method gives a mean near 1000 and a variance near 1340, with mean step 0.444, close to $2000/(2 - 0.444) = 1290$. The tests of the implementation check both effects.

## Correctness

Tau-leaping is not exact, so the guarantees are of another kind, proved below. A leap is exact when every propensity is constant, which holds for networks of sources only. The step of line L5 bounds the mean and the variance of the change of each reactant count in a leap by $\max(\epsilon x_i/g_i, 1)$ and its square. The method never records a negative count, because of line L11, and the repeat ends with probability 1. If every reaction with a positive propensity is critical, one step is exactly a step of the direct method, and the implementation then gives the same path as the direct method for the same seed. As $\epsilon \to 0$ the method tends to the exact process; as the counts grow with $\tau$ fixed and many firings per leap, the leap tends to an [Euler-Maruyama](/euler-maruyama-method/) step of the [chemical Langevin equation](/chemical-langevin-equation/), and then to the Euler step of the rate equations (Gillespie 2001). The bias is of order $\tau$ in the weak sense for a fixed step.

## Complexity

- **Per leap.** Line L3 costs $\Theta(m)$ propensities, line L4 $O(mn)$ for the critical test, and line L5 $O(mn)$ for the sums $\hat\mu_i$ and $\hat\sigma_i^2$ (less with a sparse stoichiometric matrix). Line L9 draws up to $m$ Poisson numbers, each in $O(1)$ expected time with a good sampler. So a leap costs $O(mn)$, and $O(m + \text{nonzeros of } S)$ with sparse loops.
- **Number of leaps.** The step $\tau'$ is about $\epsilon$ times the time scale on which the counts change, so the number of leaps over a fixed interval is about $1/\epsilon$ times the number of those time scales, independent of the counts. The exact method needs a number of events proportional to the counts. The gain grows with the system size.
- **Exact steps.** When counts are small, line L6 runs exact steps, and the cost is that of the direct method.
- **Space.** $\Theta(n + m)$, plus the record.

## Properties

- **Approximate.** The bias in the mean and the variance is of order $\tau$ for a fixed step. The adaptive rule keeps the relative change of the propensities in a step near $\epsilon$.
- **Nonnegative counts.** With critical reactions and the check of line L11, every recorded count is $\ge 0$.
- **Exact in a limit.** It is exact when the propensities are constant, and it becomes the direct method when all reactions are critical.
- **Explicit.** Like the explicit Euler method, it is unstable or very inaccurate for stiff systems: when a fast reversible pair is near equilibrium, the leap condition forces tiny steps, or a larger step makes the fast species swing too much.
- **Not one event per step.** The output holds the state after each leap, not the time of each reaction. Event-level statistics, such as the time of the first firing of a reaction, are not available.

## Variants and improvements

- **The first step rule.** Gillespie (2001) bounded the expected change of each propensity in a leap, using the derivatives of all propensities, with a cost of $O(m^2)$ per leap. The rule of eq. 33 bounds the changes of the counts instead, which is cheaper and less conservative.
- **Implicit tau-leaping.** For stiff systems, Rathinam, Petzold, Cao and Gillespie (2003) took the mean part of the leap implicitly, as the implicit Euler method does for a [stiff ODE](/stiff-ode-problem/). It allows large steps when fast reactions are near equilibrium, but it damps the fluctuations of the fast species.
- **Binomial leaping.** Draw $K_j$ from a [binomial](/binomial-distribution/) law whose number of trials is the count of the limiting reactant, so that a leap cannot remove more molecules than exist (Tian and Burrage 2004).
- **Post-leap checks.** Anderson (2008) checks after the leap whether the propensities changed too much, and if so rejects the leap and draws a shorter one conditioned on the first, which keeps the law correct.
- **Multilevel Monte Carlo.** Coupling leap paths with step $\tau$ and $\tau/2$ by shared Poisson processes lets [multilevel Monte Carlo](/multilevel-monte-carlo/) estimate means with the bias of a fine step at much lower cost, with an exact method on the finest level.
- **The Langevin limit.** When every reaction fires many times per leap, the Poisson counts can be replaced by normal ones, which is the Euler-Maruyama method for the [chemical Langevin equation](/chemical-langevin-equation/).

## When to use it

Use it when the counts of the species that react are large (hundreds or more), so that the exact method is too slow, and a bias of a few percent is acceptable. It is common in models of metabolism, of whole cells and of large epidemics. Do not use it when the quantity of interest depends on rare events at low counts, such as the extinction of a species or the switching of a [genetic toggle switch](/genetic-toggle-switch/), unless the method switches to exact steps there. For stiff systems use an implicit leap or a method that treats the fast reactions separately.

## Pitfalls

- **Negative counts.** A plain Poisson leap can remove more molecules than exist. Do not set negative counts to 0; that biases the law. Use critical reactions and reject the leap.
- **Too large a step.** A fixed $\tau$ chosen for the start of a run can be far too large later, when the counts are smaller or the propensities larger. Use an adaptive step.
- **Variance as well as mean.** A step that gives a good mean can still give a variance that is too large, by the factor $2/(2 - \tau)$ in the immigration-death example. If the noise is the object of the study, check it against an exact run.
- **The factor $g_i$ for dimerization.** For $2X_i$ the factor is $2 + 1/(x_i - 1)$, not 2. The convention $c\, x(x-1)/2$ for the propensity, with $c = 2k/(N_A V)$, must be the same in the propensities and in the rule for $g_i$.
- **The last step.** The step must be cut at $T$ (line L8), or the state at $T$ is that of a later time.
- **Poisson samplers.** For a large mean $a_j\tau$, inversion by the sum of uniforms is slow and loses accuracy. Use a sampler made for large means.

## Implementations

## History

Gillespie (2001) proposed tau-leaping and the leap condition, and showed that the Poisson leap tends to the [chemical Langevin equation](/chemical-langevin-equation/) and then to the rate equations as the counts grow. The first versions could make counts negative. Cao, Gillespie and Petzold (2005) introduced critical reactions to avoid this, and in 2006 they gave the step size rule of eq. 33, with the switch to exact steps, which is the form in most software. Rathinam, Petzold, Cao and Gillespie (2003) gave the implicit version for stiff systems, Tian and Burrage (2004) the binomial version, and Anderson (2008) the post-leap checks. Tau-leaping is in StochKit, COPASI and GillesPy2.

## References
