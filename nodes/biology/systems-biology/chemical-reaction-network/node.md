---
tag: SSMAKE
kind: model
slug: chemical-reaction-network
name: Chemical reaction network
aliases:
- reaction network
- CRN
area: biology/systems-biology
level: core
summary: A set of species and reactions with stoichiometric coefficients and rate laws, the common model of metabolism and signalling, read as an ODE or as a Markov chain.
history:
  year: 1972
  people: [F. Horn, R. Jackson, M. Feinberg, T. G. Kurtz]
  note: Horn and Jackson set up the network of complexes in 1972, Feinberg built the deficiency theory on it, and Kurtz showed in 1972 that the ODE model is the large volume limit of the Markov chain model.
prereqs: [ode-initial-value-problem, markov-chain]
see_also: [stoichiometric-matrix, mass-action-kinetics, chemical-master-equation, gillespie-algorithm, deficiency-zero-theorem, petri-net, flux-balance-analysis, gene-regulatory-network]
sources:
  - book: isbn:9783030038571
    title: Martin Feinberg, Foundations of Chemical Reaction Network Theory, Applied Mathematical Sciences 202, Springer, 2019
    locator: Chapter 2 (chemical and notational preliminaries), Chapter 3 (reaction networks, kinetics and the induced differential equations) and Chapter 6 (aspects of reaction network structure)
  - paper: doi:10.1007/BF00251225
    title: F. Horn and R. Jackson, General mass action kinetics, Archive for Rational Mechanics and Analysis 47(2), 1972, 81-116
    locator: the description of a network by its complexes and its reaction graph, and the mass action rate functions
  - paper: doi:10.1063/1.1678692
    title: Thomas G. Kurtz, The relationship between stochastic and deterministic models for chemical reactions, Journal of Chemical Physics 57(7), 1972, 2976-2978
    locator: the Markov chain model with rates scaled by the volume, and the ODE model as its infinite volume limit
  - paper: doi:10.1021/j100540a008
    title: Daniel T. Gillespie, Exact stochastic simulation of coupled chemical reactions, Journal of Physical Chemistry 81(25), 1977, 2340-2361
    locator: the stochastic reaction constants, the propensity functions and their relation to the deterministic rate constants
---

A chemical reaction network is a finite list of species and a finite list of reactions between them, such as $2A \to B$ or $E + S \to C$. Each reaction takes a fixed number of molecules of each species and makes a fixed number of molecules of each species. A rate law gives how fast each reaction fires in each state. The same network has two standard readings: a system of ordinary differential equations for the concentrations, and a continuous-time [Markov chain](/markov-chain/) for the molecule counts. Biochemical models of metabolism, signalling and gene expression are written as reaction networks, and a [Petri net](/petri-net/) is the same structure without the rates.

## The machine

**Species and reactions.** There are $n$ species $X_1, \ldots, X_n$ and $m$ reactions $R_1, \ldots, R_m$. Reaction $R_j$ is
$$\sum_{i=1}^{n} \alpha_{ij} X_i \;\longrightarrow\; \sum_{i=1}^{n} \beta_{ij} X_i,$$
with non-negative integers $\alpha_{ij}$ (the reactant coefficients) and $\beta_{ij}$ (the product coefficients). The left side $y_j = \alpha_{\cdot j}$ and the right side $y'_j = \beta_{\cdot j}$ are vectors in $\mathbb{Z}^n_{\ge 0}$, called *complexes*. The zero complex $\emptyset$ is allowed: $\emptyset \to X$ is an inflow and $X \to \emptyset$ is an outflow or a degradation. The change of the state when $R_j$ fires once is the reaction vector $\nu_j = y'_j - y_j$, and these vectors are the columns of the [stoichiometric matrix](/stoichiometric-matrix/) $S$.

**The reaction graph.** The complexes are the vertices of a directed graph, with one edge $y_j \to y'_j$ for each reaction. Its connected components (with the directions ignored) are the *linkage classes*. The network is *reversible* if each reaction has its reverse in the list, and *weakly reversible* if each edge lies on a directed cycle, that is, if each linkage class is strongly connected. These structural words are the inputs of the [deficiency zero theorem](/deficiency-zero-theorem/).

**Standing assumptions.** The molecules are in a well-mixed vessel of fixed volume $V$ at a fixed temperature. So the state is the vector of amounts of the species, and the position of a molecule does not matter. The rate of a reaction depends only on the current state. A model that breaks these assumptions (with transport in space, or with a changing volume) needs more than a reaction network.

**The deterministic reading.** The state is the vector of concentrations $x \in \mathbb{R}^n_{\ge 0}$. Each reaction has a rate function $v_j(x) \ge 0$, and
$$\frac{dx}{dt} = S\, v(x) = \sum_{j=1}^{m} v_j(x)\, \nu_j .$$
This is an [ODE initial value problem](/ode-initial-value-problem/) for a start $x(0)$. The basic rate law is [mass action](/mass-action-kinetics/), $v_j(x) = k_j \prod_i x_i^{\alpha_{ij}}$ with a rate constant $k_j > 0$. Rate laws such as [Michaelis-Menten](/michaelis-menten-kinetics/) and [Hill](/hill-equation/) come from mass action networks after a reduction by the [quasi-steady-state approximation](/quasi-steady-state-approximation/).

**The stochastic reading.** The state is the vector of counts $X \in \mathbb{Z}^n_{\ge 0}$. Reaction $R_j$ fires at the rate $a_j(X)$, the propensity, and moves the state from $X$ to $X + \nu_j$. So the state is a continuous-time Markov chain on $\mathbb{Z}^n_{\ge 0}$, and its probabilities obey the [chemical master equation](/chemical-master-equation/). The [Gillespie algorithm](/gillespie-algorithm/) samples its paths exactly. With mass action, the propensity counts the distinct sets of reactant molecules: $c$ for $\emptyset \to \cdot$, $c\, x_A$ for $A \to \cdot$, $c\, x_A x_B$ for $A + B \to \cdot$ and $c\, x_A (x_A - 1)/2$ for $2A \to \cdot$. With Avogadro's number $N_A$, the stochastic constant is $c = k / (N_A V)$ for $A + B$ and $c = 2k/(N_A V)$ for $2A$ (Gillespie 1977). Books differ by this factor 2 for $2A$, so a page that uses $2A$ states its convention. This page uses the one above.

**A worked example.** Take the dimerization $R_1: 2A \to B$ and $R_2: B \to 2A$, with species $(A, B)$, so
$$S = \begin{pmatrix} -2 & 2 \\ 1 & -1 \end{pmatrix}.$$
With mass action, $v_1 = k_1 a^2$ and $v_2 = k_2 b$, and the ODE is $\dot a = -2k_1 a^2 + 2k_2 b$, $\dot b = k_1 a^2 - k_2 b$. Each reaction keeps $a + 2b$ fixed. Take $k_1 = k_2 = 1$ per second (in units where the concentrations are in mol/L), $a(0) = 3$ and $b(0) = 0$. Then $b = (3 - a)/2$, and $\dot a = (2a + 3)(1 - a)$. This separates, and
$$\frac{2a + 3}{a - 1} = 4.5\, e^{5t}, \qquad a(t) = \frac{3 + 4.5 e^{5t}}{4.5 e^{5t} - 2}.$$
So $a(0.2\,\text{s}) = 1.488650$ and $a(1\,\text{s}) = 1.007509$, and $a \to 1$, $b \to 1$. The rate of approach is $5$ per second, the slope of $(2a + 3)(1 - a)$ at $a = 1$. A [classical Runge-Kutta](/classical-runge-kutta-4/) run with step $0.001$ s gives the same six digits at both times, and keeps $a + 2b = 3$ to nine digits.

In the stochastic reading with $c_1 = c_2 = 1$ per second and six molecules of $A$ at the start, the count $x_A + 2 x_B = 6$ is fixed. So the chain lives on the four states $x_B = 0, 1, 2, 3$ (with $x_A = 6, 4, 2, 0$). From $x_B$ to $x_B + 1$ the rate is $x_A (x_A - 1)/2$, and back the rate is $x_B + 1$. The chain is a birth-death chain, so its stationary law $\pi$ satisfies detailed balance: $\pi(1) = 15\, \pi(0)$, $\pi(2) = \frac{6}{2} \pi(1)$ and $\pi(3) = \frac{1}{3} \pi(2)$. So
$$\pi = \tfrac{1}{76}\,(1, 15, 45, 15), \qquad E[x_B] = \tfrac{150}{76} = \tfrac{75}{38} \approx 1.974.$$

## What it counts

- In the deterministic reading: the path $x(t)$, the equilibria $x^*$ with $S v(x^*) = 0$, their stability, and the long run behavior (convergence, several stable equilibria, oscillation).
- In both readings: the conservation laws $w^{\mathsf T} x$ with $w^{\mathsf T} S = 0$, which stay fixed in time.
- In the stochastic reading: the law $P(X(t) = x)$, the stationary distribution, the number $N_j(t)$ of firings of each reaction, and the time until a species dies out.
- From the network alone, with no rates: the rank of $S$, the complexes, the linkage classes and the deficiency. Some results (the deficiency zero theorem) give the qualitative behavior for every choice of rate constants from these numbers.

## Relation to other models

- **[Petri nets](/petri-net/).** A Petri net with places for species and transitions for reactions has the same structure. A marking is a count vector, and the state equation $M = M_0 + S\, N$ of the net is the identity $X(t) = X(0) + S\, N(t)$. The Petri net has no rates: it asks which states can be reached, not how likely they are. A reaction network with propensities is a stochastic Petri net (there is no page for that model here). Reachability in a Petri net is decidable but Ackermann-complete, so the same holds for the question whether a count vector can be reached in the stochastic reading.
- **[Mass action kinetics](/mass-action-kinetics/).** The standard choice of $v$ and of $a$. It is the only kinetics that the deficiency theory of Horn, Jackson and Feinberg covers in full.
- **Constraint-based models.** [Flux balance analysis](/flux-balance-analysis/) and the other [constraint-based models](/constraint-based-metabolic-modeling/) keep only $S$ and bounds on the fluxes. They ask which flux vectors satisfy $S v = 0$, and they need no rate law.
- **[Gene regulatory networks](/gene-regulatory-network/).** Gene circuits such as the [genetic toggle switch](/genetic-toggle-switch/) and the [repressilator](/repressilator/) are reaction networks of transcription, translation, binding and decay. After a reduction they are written with Hill rate laws.
- **Approximations of the stochastic reading.** The [chemical Langevin equation](/chemical-langevin-equation/), the [linear noise approximation](/linear-noise-approximation/) and [tau-leaping](/tau-leaping/) sit between the Markov chain and the ODE.

## Known results in the model

**The state stays in its compatibility class.** In both readings, $x(t) - x(0)$ is in the column space of $S$, because $x(t) = x(0) + S \int_0^t v(x(\tau))\, d\tau$ and $X(t) = X(0) + S\, N(t)$. So the path stays in $(x(0) + \operatorname{im} S) \cap \mathbb{R}^n_{\ge 0}$, the stoichiometric compatibility class. In the example, $\operatorname{im} S$ is spanned by $(-2, 1)$, and the class of $(3, 0)$ is the segment $a + 2b = 3$, $a, b \ge 0$.

**Mass action keeps the state non-negative.** With mass action, if $x_i = 0$ then each reaction that uses $X_i$ has rate 0, so each term of $\dot x_i$ is $\ge 0$. Hence the non-negative orthant is forward invariant. In the stochastic reading, the propensity is 0 when there are too few reactant molecules, so the counts never become negative.

**A positive conservation law bounds the state.** If some $w$ with all $w_i > 0$ satisfies $w^{\mathsf T} S = 0$, then $w^{\mathsf T} x(t) = w^{\mathsf T} x(0)$, so each $x_i(t) \le w^{\mathsf T} x(0) / w_i$. In the example, $w = (1, 2)$ gives $a \le 3$ and $b \le 1.5$. A network with inflows has no such law and can have unbounded paths.

**Large volume limit (Kurtz 1972).** Scale the propensities with the volume as above, and let $X^V(t)$ be the counts in volume $V$. If $X^V(0)/(N_A V) \to x(0)$, then on each bounded time interval $X^V(t)/(N_A V)$ converges in probability to the solution $x(t)$ of the mass action ODE. This is a law of large numbers: the ODE is the mean behavior of a large system, and the fluctuations are of order $V^{-1/2}$. For small counts the two readings can differ a lot. A species with a stable positive equilibrium in the ODE can still die out in the Markov chain, because $0$ can be an absorbing state of the chain.

**Structure can fix the behavior for all rate constants.** For a weakly reversible network of deficiency zero with mass action, each positive compatibility class has exactly one positive equilibrium, and it is locally asymptotically stable relative to its class, for every choice of positive rate constants. For the stochastic reading of such a network, Anderson, Craciun and Kurtz (2010) showed that the stationary law on each closed class is a product of Poisson factors $\prod_i \lambda_i^{x_i}/x_i!$, where $\lambda$ is a positive equilibrium of the ODE with the rate constants $c_j$ divided by the factorial factors of the propensities. In the example, $2A \rightleftharpoons B$ has deficiency zero and is reversible. With $c_1/2$ in place of $k_1$, the ODE equilibrium $\tfrac{1}{2}\lambda_A^2 = \lambda_B$ holds for $\lambda = (1, 0.5)$, and $\lambda_A^{x_A}/x_A!\cdot \lambda_B^{x_B}/x_B!$ for $x_B = 0, \ldots, 3$ is proportional to $(1, 15, 45, 15)$, the same law as above. See the [deficiency zero theorem](/deficiency-zero-theorem/).

**Without such structure, anything can happen.** Mass action networks with few species can have several stable equilibria (the Schlögl network $\emptyset \rightleftharpoons A$, $2A \rightleftharpoons 3A$, on the deficiency zero page), stable [limit cycles](/limit-cycle/) and chaos. The [Lotka-Volterra predator-prey model](/lotka-volterra-predator-prey/) is the mass action network $X \to 2X$, $X + Y \to 2Y$, $Y \to \emptyset$.

**Solving the ODE.** Rate constants in one network often differ by many orders of magnitude, so the ODE is often a [stiff problem](/stiff-ode-problem/). Explicit [Runge-Kutta methods](/runge-kutta-methods/) then need a very small step, and an implicit method such as [backward Euler](/backward-euler-method/) is the usual choice. The reduction by the quasi-steady-state approximation removes the fast part instead.

## References
