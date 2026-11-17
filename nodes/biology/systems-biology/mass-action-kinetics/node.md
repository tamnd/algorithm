---
tag: QSSZE0
kind: model
slug: mass-action-kinetics
name: Mass action kinetics
aliases:
- law of mass action
area: biology/systems-biology
level: intro
summary: The rate of an elementary reaction is a rate constant times the product of the reactant concentrations, each raised to its stoichiometric coefficient.
history:
  year: 1864
  people: [C. M. Guldberg, P. Waage]
  note: Guldberg and Waage stated the law of mass action for chemical equilibrium in 1864. Horn and Jackson gave the general form for a whole network in 1972.
prereqs: [chemical-reaction-network, stoichiometric-matrix]
see_also: [michaelis-menten-kinetics, hill-equation, chemical-master-equation, deficiency-zero-theorem, detailed-balance, gillespie-algorithm, ode-initial-value-problem, stiff-ode-problem]
sources:
  - book: isbn:9783030038571
    title: Martin Feinberg, Foundations of Chemical Reaction Network Theory, Applied Mathematical Sciences 202, Springer, 2019
    locator: Chapter 2 (chemical and notational preliminaries) and Chapter 3 (reaction networks, kinetics and the induced differential equations, mass action kinetics)
  - paper: doi:10.1007/BF00251225
    title: F. Horn and R. Jackson, General mass action kinetics, Archive for Rational Mechanics and Analysis 47(2), 1972, 81-116
    locator: the mass action rate functions for a general network, and the Lyapunov function of complex balanced systems
  - paper: doi:10.1021/j100540a008
    title: Daniel T. Gillespie, Exact stochastic simulation of coupled chemical reactions, Journal of Physical Chemistry 81(25), 1977, 2340-2361
    locator: the stochastic reaction constant c, its relation to the rate constant k, and the propensities of the elementary reaction types
  - paper: doi:10.1063/1.1678692
    title: Thomas G. Kurtz, The relationship between stochastic and deterministic models for chemical reactions, Journal of Chemical Physics 57(7), 1972, 2976-2978
    locator: the mass action ODE as the large volume limit of the stochastic model
---

Mass action kinetics is the rate law of elementary reactions in a well-mixed solution. The rate of a reaction is proportional to the number of encounters of its reactant molecules per unit time, and in a dilute well-mixed solution this number is proportional to the product of the reactant concentrations. So the reaction $A + B \to C$ fires at the rate $k\,[A][B]$, and $2A \to B$ at the rate $k\,[A]^2$. With one such rate for each reaction of a [chemical reaction network](/chemical-reaction-network/), the concentrations obey the ODE $\dot x = S\, v(x)$, with $S$ the [stoichiometric matrix](/stoichiometric-matrix/). The stochastic form counts the sets of reactant molecules instead.

## The machine

**The reactions.** A network has species $X_1, \ldots, X_n$ and reactions $R_1, \ldots, R_m$. Reaction $R_j$ uses $\alpha_{ij}$ molecules of $X_i$ and makes $\beta_{ij}$, and its reaction vector $\nu_j$ (column $j$ of $S$) has entries $\beta_{ij} - \alpha_{ij}$. Each reaction is *elementary*: it happens in one step, as a collision of the reactant molecules or as the decay of one molecule. Elementary reactions have at most two reactant molecules in practice; three-body collisions are rare.

**The parameters.** Each reaction has a rate constant $k_j > 0$. The *order* of $R_j$ is $\sum_i \alpha_{ij}$, and the unit of $k_j$ depends on it: per second for order 1, L/(mol s) for order 2, and mol/(L s) for order 0 (a constant inflow).

**The rate law.** With concentrations $x \in \mathbb{R}^n_{\ge 0}$ in mol/L,
$$v_j(x) = k_j \prod_{i=1}^{n} x_i^{\alpha_{ij}}, \qquad \frac{dx}{dt} = \sum_{j=1}^{m} v_j(x)\, \nu_j = S\, v(x).$$
The exponent is the reactant coefficient $\alpha_{ij}$, not the net entry $S_{ij}$. For $2A \to A + B$ the rate is $k\,[A]^2$, while $S_{Aj} = -1$.

**The stochastic form.** With counts $X \in \mathbb{Z}^n_{\ge 0}$ in a volume $V$, the propensity of $R_j$ is the stochastic constant $c_j$ times the number of distinct sets of reactant molecules:
$$a_j(X) = c_j \prod_{i=1}^{n} \binom{X_i}{\alpha_{ij}} .$$
So $a = c$ for $\emptyset \to \cdot$, $a = c\, X_A$ for $A \to \cdot$, $a = c\, X_A X_B$ for $A + B \to \cdot$ and $a = c\, X_A (X_A - 1)/2$ for $2A \to \cdot$. With Avogadro's number $N_A$, $c = k$ for order 1, $c = k/(N_A V)$ for $A + B$, and $c = 2k/(N_A V)$ for $2A$ (Gillespie 1977). Some books put the factor $1/2$ of the binomial into $c$, and then their $c$ for $2A$ is half of this one. This page uses the convention above.

**Standing assumptions.** The solution is well mixed and dilute, the temperature and the volume are fixed, and each reaction is elementary. The rate constants do not depend on the concentrations. A crowded cell, a reaction limited by diffusion or a surface reaction can break these assumptions.

## What it counts

The rate law gives the rate of each reaction, and the ODE gives the path $x(t)$. Small cases have closed forms. Each example below was checked with a [classical Runge-Kutta](/classical-runge-kutta-4/) run with step $0.01$ s, which agrees to six digits.

**First order, reversible.** $A \rightleftharpoons B$ with $k_1 = 2$ per second forward and $k_2 = 1$ per second back. Then $\dot a = -k_1 a + k_2 b$ and $a + b$ is fixed. From $a(0) = 1$, $b(0) = 0$ (in mol/L):
$$a(t) = \frac{k_2}{k_1 + k_2} + \frac{k_1}{k_1 + k_2}\, e^{-(k_1 + k_2) t} = \tfrac{1}{3} + \tfrac{2}{3} e^{-3t}.$$
So $a(0.5\,\text{s}) = 0.482087$ and $a(1\,\text{s}) = 0.366525$. At equilibrium $b/a = k_1/k_2 = 2$. This is the law of mass action in the sense of Guldberg and Waage: at equilibrium, the ratio of the products of concentrations is the equilibrium constant $K = k_1/k_2$.

**Second order, two species.** $A + B \to C$ with $k = 0.5$ L/(mol s), $a(0) = 1$, $b(0) = 2$ and $c(0) = 0$ mol/L. Then $b - a = 1$ for all time, $\dot a = -k\, a (a + 1)$, and
$$a(t) = \frac{a_0 (b_0 - a_0)}{b_0\, e^{(b_0 - a_0) k t} - a_0} = \frac{1}{2 e^{0.5 t} - 1}.$$
So $a(1\,\text{s}) = 0.435267$, $a(2\,\text{s}) = 0.225400$ and $a(5\,\text{s}) = 0.042799$. Half of $A$ is gone at $t = 2 \ln 1.5 = 0.810930$ s.

**Second order, one species.** $2A \to P$ with rate $v = k\,[A]^2$. Each event uses two molecules, so $\dot a = -2k a^2$ and $a(t) = a_0 / (1 + 2 k a_0 t)$. For $k = 0.5$ L/(mol s) and $a_0 = 1$ mol/L, $a(1\,\text{s}) = 1/2$ and $a(2\,\text{s}) = 1/3$. Many chemistry books define the rate of $2A \to P$ as $-\frac{1}{2}\dot a$ or write $\dot a = -k a^2$; their $k$ differs from this one by the factor 2.

**Non-examples.**
- An overall reaction is not elementary in general, and its rate is not the mass action form of its overall equation. The rate of $2\,\mathrm{H_2} + \mathrm{O_2} \to 2\,\mathrm{H_2O}$ is not $k\,[\mathrm{H_2}]^2[\mathrm{O_2}]$; the reaction runs through radical steps.
- An enzyme reaction $S \to P$ with the rate $V_{\max} [S]/(K_M + [S])$ is not mass action in $[S]$. That rate law comes from the mass action network $E + S \rightleftharpoons C \to E + P$ after a reduction; see [Michaelis-Menten kinetics](/michaelis-menten-kinetics/).
- The stochastic propensity of $2A$ is not $c\, X_A^2$. A molecule cannot react with itself, so the count of pairs is $X_A (X_A - 1)/2$.

## Relation to other models

- **[Chemical reaction networks](/chemical-reaction-network/).** Mass action is the standard choice of the rate functions $v_j$ and of the propensities $a_j$. The network fixes $S$ and the $\alpha_{ij}$; mass action adds one constant per reaction.
- **[Michaelis-Menten kinetics](/michaelis-menten-kinetics/) and the [Hill equation](/hill-equation/).** These rate laws come from mass action networks of binding and catalysis, by the [quasi-steady-state approximation](/quasi-steady-state-approximation/) or by an equilibrium assumption for the binding steps.
- **The [chemical master equation](/chemical-master-equation/).** It is the stochastic model with the mass action propensities, and the [Gillespie algorithm](/gillespie-algorithm/) samples it. The mass action ODE is its limit for a large volume.
- **Power-law and other kinetics.** Models that allow non-integer exponents, or rates that are not products, are outside mass action. The deficiency theory covers mass action in full; for other kinetics only parts of it hold.

## Known results in the model

**Positivity.** If $x_i = 0$, each reaction that uses $X_i$ has rate 0, so $\dot x_i \ge 0$. So paths that start in the non-negative orthant stay there, and paths that start in the positive orthant stay positive for all finite time.

**Detailed balance and the equilibrium constants.** For a reversible network, an equilibrium $x^*$ is *detailed balanced* if each reaction and its reverse have the same rate: $k_j\, x^{*\,y_j} = k_{-j}\, x^{*\,y'_j}$, where $x^y$ means $\prod_i x_i^{y_i}$. Taking logarithms, $\nu_j \cdot \ln x^* = \ln (k_j / k_{-j})$. So a detailed balanced equilibrium exists only if the vector $\ln(k_j/k_{-j})$ lies in the row space of $S$ restricted to one column per reversible pair. These are the Wegscheider conditions: around a cycle of reactions with $\sum_j \nu_j = 0$, the product of the equilibrium constants is 1. For $A \rightleftharpoons B \rightleftharpoons C \rightleftharpoons A$ the condition is $K_1 K_2 K_3 = 1$. The same idea in Markov chains is [detailed balance](/detailed-balance/).

**A Lyapunov function.** Horn and Jackson (1972) showed that if $x^*$ is a complex balanced equilibrium (a weaker condition than detailed balance), then
$$G(x) = \sum_{i=1}^{n} \left( x_i \ln \frac{x_i}{x^*_i} - x_i + x^*_i \right)$$
does not increase along paths, and it is constant only at equilibria. This is the base of the [deficiency zero theorem](/deficiency-zero-theorem/), which gives such an equilibrium for each choice of rate constants when the network is weakly reversible with deficiency zero.

**Linear networks: the mean obeys the ODE.** If each reaction has order 0 or 1, each propensity is an affine function of $X$. Then $\frac{d}{dt} E[X(t)] = S\, E[a(X(t))] = S\, a(E[X(t)])$, so the mean of the stochastic model solves the mass action ODE exactly, for every volume. Example: immigration $\emptyset \to X$ at rate 10 per second and death $X \to \emptyset$ at rate 1 per second per molecule. The ODE $\dot x = 10 - x$ has the equilibrium 10, and the stationary law of the counts is Poisson(10), with mean 10. For a second order reaction this fails. For $2A \to \emptyset$, $E[X(X - 1)] = E[X]^2 + \operatorname{Var}(X) - E[X]$, so the mean of the counts does not follow the ODE, and the gap matters when the counts are small.

**The large volume limit.** Kurtz (1972) proved that with the scaling $c = k/(N_A V)$ of the propensities, the concentrations $X(t)/(N_A V)$ of the stochastic model converge to the solution of the mass action ODE on each bounded time interval as $V \to \infty$.

**Stiffness.** Rate constants in one model often span many orders of magnitude. Then the mass action ODE is a [stiff problem](/stiff-ode-problem/), and explicit [Runge-Kutta methods](/runge-kutta-methods/) need a step smaller than the fastest time scale, even after the fast part has settled. Implicit methods, or a reduction by the quasi-steady-state approximation, avoid this.

## References
