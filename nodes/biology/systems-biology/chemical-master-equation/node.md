---
tag: BBD6VD
kind: model
slug: chemical-master-equation
name: Chemical master equation
aliases:
- CME
area: biology/systems-biology
level: core
summary: The forward Kolmogorov equation for the probability of each molecule count vector of a well-mixed reaction network in continuous time.
history:
  year: 1940
  people: [Max Delbrück, Donald A. McQuarrie, Daniel T. Gillespie]
  note: Delbrück wrote a master equation for an autocatalytic reaction in 1940. McQuarrie reviewed the stochastic approach to chemical kinetics in 1967, and Gillespie derived the equation from the physics of a well-stirred gas in 1992.
prereqs: [chemical-reaction-network, mass-action-kinetics, markov-chain]
see_also: [gillespie-algorithm, finite-state-projection, chemical-langevin-equation, linear-noise-approximation, moment-closure, stoichiometric-matrix, poisson-distribution, deficiency-zero-theorem]
sources:
  - paper: doi:10.2307/3212214
    title: Donald A. McQuarrie, Stochastic approach to chemical kinetics, Journal of Applied Probability 4(3), 1967, 413-478
    locator: the review of the master equation for chemical reactions and its exact solutions for simple reactions
  - paper: doi:10.1016/0378-4371(92)90283-V
    title: Daniel T. Gillespie, A rigorous derivation of the chemical master equation, Physica A 188(1-3), 1992, 404-425
    locator: the derivation for a well-stirred gas in thermal equilibrium, and the conditions under which it holds
  - paper: doi:10.1021/j100540a008
    title: Daniel T. Gillespie, Exact stochastic simulation of coupled chemical reactions, Journal of Physical Chemistry 81(25), 1977, 2340-2361
    locator: the stochastic rate constant c and its relation to the deterministic rate constant k
  - paper: doi:10.1063/1.1750549
    title: Max Delbrück, Statistical fluctuations in autocatalytic reactions, Journal of Chemical Physics 8(1), 1940, 120-124
    locator: an early master equation for the count of one species
  - paper: doi:10.1063/1.1678692
    title: Thomas G. Kurtz, The relationship between stochastic and deterministic models for chemical reactions, Journal of Chemical Physics 57(7), 1972, 2976-2978
    locator: the rate equations as the large volume limit of the jump process
  - paper: doi:10.1007/s00285-006-0034-x
    title: Tobias Jahnke and Wilhelm Huisinga, Solving the chemical master equation for monomolecular reaction systems analytically, Journal of Mathematical Biology 54(1), 2007, 1-26
    locator: the solution for first order networks as a convolution of multinomial and product Poisson laws
  - paper: doi:10.1007/s11538-010-9517-4
    title: David F. Anderson, Gheorghe Craciun and Thomas G. Kurtz, Product-form stationary distributions for deficiency zero chemical reaction networks, Bulletin of Mathematical Biology 72(8), 2010, 1947-1970
    locator: the product of Poisson laws as the stationary distribution of a complex balanced network
  - book: isbn:9781138549289
    title: Darren J. Wilkinson, Stochastic Modelling for Systems Biology, 3rd edition, CRC Press, 2018
    locator: the chapters on chemical kinetics, the master equation and stochastic simulation
---

The chemical master equation (CME) is the stochastic model of a [chemical reaction network](/chemical-reaction-network/) in a small, well-mixed volume. The state is the vector of molecule counts, not of concentrations, and the reactions fire at random times. The CME is a system of linear differential equations, one for each possible count vector, for the probability that the system is in that state at time $t$. In the language of probability, it is the forward Kolmogorov equation of a continuous-time Markov chain on $\mathbb{N}^n$. The model matters in cell biology because many species (genes, mRNAs, transcription factors) are present in counts of 1 to 100, where the random firing of single reactions is a large part of the behavior.

## The machine

**State.** A volume $V$ holds $n$ species $X_1, \ldots, X_n$. The state is $x = (x_1, \ldots, x_n) \in \mathbb{N}^n$, the number of molecules of each species.

**Reactions.** There are $m$ reactions $R_1, \ldots, R_m$. Reaction $R_j$ changes the state from $x$ to $x + \nu_j$, where $\nu_j \in \mathbb{Z}^n$ is column $j$ of the [stoichiometric matrix](/stoichiometric-matrix/) $S$. Each reaction has a *propensity* $a_j(x) \ge 0$: given $X(t) = x$, the probability that $R_j$ fires once in $[t, t + dt)$ is $a_j(x)\, dt + o(dt)$, and the probability of two or more firings is $o(dt)$.

**Stochastic mass action.** The propensity is a stochastic rate constant $c_j$ times the number of distinct combinations of reactant molecules:

| reaction | propensity $a_j(x)$ | $c_j$ from the deterministic $k_j$ |
|---|---|---|
| $\emptyset \to \ldots$ | $c_j$ | $k_j N_A V$ |
| $A \to \ldots$ | $c_j x_A$ | $k_j$ |
| $A + B \to \ldots$ | $c_j x_A x_B$ | $k_j / (N_A V)$ |
| $2A \to \ldots$ | $c_j x_A (x_A - 1) / 2$ | $2 k_j / (N_A V)$ |

Here $N_A$ is Avogadro's number, $k_j$ is in molar units, and the deterministic rate of $2A \to \ldots$ is $k_j [A]^2$. Books differ by a factor of 2 for $2A$: some write the propensity as $c\, x_A (x_A - 1)$. All pages of this site use $c\, x_A (x_A - 1)/2$ with $c = 2k / (N_A V)$, which is the convention of Gillespie (1977) and Wilkinson (2018).

**The equation.** For every state $x$,

$$\frac{dP(x, t)}{dt} = \sum_{j=1}^{m} \Bigl[ a_j(x - \nu_j)\, P(x - \nu_j, t) - a_j(x)\, P(x, t) \Bigr],$$

with $P(y, t) = 0$ for a $y$ that has a negative entry. The first term is the flow into $x$ by reaction $j$ from the state $x - \nu_j$, and the second is the flow out of $x$. With the states in a fixed order and $P(t)$ as a column vector, this is $\dot P = A P$ with the generator $A_{xx} = -a_0(x)$, where $a_0 = \sum_j a_j$, and $A_{x + \nu_j, x} = a_j(x)$. The columns of $A$ sum to 0, so total probability is kept.

**Assumptions.** The molecules are well mixed: between two reactive collisions, each molecule moves through the whole volume many times, so the position of a molecule does not matter. The volume and the temperature are constant, and the solution is dilute. Gillespie (1992) derived the CME from these assumptions for a gas in thermal equilibrium, and the same form is used for reactions in solution. Space, crowding and delays (for example, the time to make a protein) are outside the model.

## What it counts

The CME gives the full distribution $P(x, t)$ of the counts, and from it every moment, the probability of extinction of a species, the distribution of the time to reach a state, and the stationary distribution if there is one.

**Pure death.** $X \to \emptyset$ with propensity $c x$. Each molecule dies at rate $c$ independently of the others, so $X(t)$ is Binomial$(x_0, e^{-ct})$. For $x_0 = 2$ the CME is three equations: $\dot P_2 = -2c P_2$, $\dot P_1 = 2c P_2 - c P_1$, $\dot P_0 = c P_1$. With $c = 1$ and $t = 1$ the solution is $P_2 = e^{-2} = 0.135335$, $P_1 = 2e^{-1}(1 - e^{-1}) = 0.465088$ and $P_0 = (1 - e^{-1})^2 = 0.399576$. From $x_0 = 100$, $X(1)$ has mean $100 e^{-1} = 36.787944$ and variance $100 e^{-1}(1 - e^{-1}) = 23.254416$.

**Immigration-death.** $\emptyset \to X$ with propensity $b$, and $X \to \emptyset$ with propensity $c x$. From $x_0$, $X(t)$ is the sum of a Binomial$(x_0, e^{-ct})$ count of the first molecules that are still there and an independent Poisson$((b/c)(1 - e^{-ct}))$ count of new ones. The stationary law is [Poisson](/poisson-distribution/)$(b/c)$: the Poisson probabilities satisfy $b\, P(x) = c\,(x + 1)\, P(x + 1)$ for every $x$, so the flow from $x$ to $x + 1$ equals the flow back, and the right side of the CME is 0. With $b = 10$ and $c = 1$ the stationary mean and variance are both 10, and from $x_0 = 0$, $X(1)$ is Poisson$(6.321206)$.

**A nonlinear network.** $\emptyset \to A$ with propensity $k = 10$, and $2A \to \emptyset$ with propensity $c\, x(x-1)/2$, $c = 1$. Each firing of the second reaction removes 2 molecules. The CME gives $\frac{d}{dt}\mathbb{E}[X] = k - c\,(\mathbb{E}[X^2] - \mathbb{E}[X])$: the mean depends on the second moment, and there is no closed equation for it. The stationary law, computed by solving the stationary equations on the states 0 to 30 (the probability of state 30 is below $10^{-29}$), has mean 3.295346 and variance 2.436040. The deterministic rate equation $\dot\phi = k - c \phi^2$ has the fixed point $\phi = \sqrt{10} = 3.162278$, which is 4 percent low.

## Relation to other models

- **Deterministic rate equations.** For first order networks (every reaction has at most one reactant molecule), the means solve exactly the [mass action](/mass-action-kinetics/) rate equations, because $\mathbb{E}[a_j(X)] = a_j(\mathbb{E}[X])$ for propensities that are linear. For a general network, Kurtz (1972) showed that the concentrations $X(t)/V$ converge to the solution of the rate equations as $V \to \infty$ with the concentrations fixed, on any finite time interval.
- **Approximations.** The [chemical Langevin equation](/chemical-langevin-equation/) replaces the jumps by a [stochastic differential equation](/stochastic-differential-equation/) when every reaction fires many times in a short time. The [linear noise approximation](/linear-noise-approximation/) gives Gaussian fluctuations around the rate equations. [Moment closure](/moment-closure/) cuts the chain of moment equations.
- **Exact numerical methods.** The [Gillespie algorithm](/gillespie-algorithm/), the [first reaction method](/first-reaction-method/) and the [next reaction method](/next-reaction-method/) draw exact sample paths of the process. [Finite state projection](/finite-state-projection/) solves the equation itself on a finite set of states, with a bound on the error. [Tau-leaping](/tau-leaping/) draws approximate paths faster.
- **Other jump processes.** The [stochastic SIR model](/stochastic-sir-model/) is a CME with infection as the reaction $S + I \to 2I$ and recovery as $I \to R$. [Kinetic Monte Carlo](/kinetic-monte-carlo/) in materials science uses the same master equation with other events. A [Markov chain](/markov-chain/) in discrete time is the closest page on this site; the CME is its continuous time form, with rates in place of transition probabilities.

## Known results in the model

- **Exact for well-stirred gases.** The CME is exact, not an approximation, for a well-stirred gas in thermal equilibrium, under the conditions of Gillespie (1992).
- **Finite state spaces.** If the reachable states are finite (a closed system), the solution is $P(t) = e^{At} P(0)$ with the [matrix exponential](/matrix-exponential/). The number of states grows as a power of the counts, which is the main obstacle to solving the CME directly.
- **First order networks.** Jahnke and Huisinga (2007) solved the CME of any network of reactions of order 0 and 1 in closed form: from a fixed start, the state is the sum of independent multinomial counts of the start molecules and a product Poisson count of the new ones, with parameters that solve the rate equations. Pure death and immigration-death above are the smallest cases.
- **Product form stationary laws.** If the network is complex balanced, which holds for every weakly reversible network of deficiency zero (see the [deficiency zero theorem](/deficiency-zero-theorem/)), the stationary law on each closed class of states is a product of Poisson laws, restricted to that class and normalized (Anderson, Craciun and Kurtz 2010).
- **Moment equations.** For every network, $\frac{d}{dt}\mathbb{E}[X] = S\, \mathbb{E}[a(X)]$. If some reaction has order 2 or more, the equation for moments of order $k$ involves moments of order $k + 1$, so the moment equations do not close. This is the problem that [moment closure](/moment-closure/) approximates.
- **Exact sampling.** The direct method samples the waiting time from the exponential law with rate $a_0(x)$ and the reaction from the probabilities $a_j(x)/a_0(x)$, and this gives the exact law of the process (Gillespie 1976, 1977).
- **Truncation bound.** Solving the CME on a finite set $J$ of states, with the probability that leaves $J$ thrown away, gives values that are below the true probabilities, and the L1 error equals the mass that left $J$ (Munsky and Khammash 2006; see [finite state projection](/finite-state-projection/)).

## References
