---
tag: P97XM1
kind: definition
slug: metropolis-criterion
name: Metropolis acceptance criterion
aliases:
- Metropolis rule
- Metropolis acceptance rule
area: optimization/metaheuristics
level: intro
summary: Accept a proposed move that changes the objective by Δ with probability min(1, exp(-Δ/T)). With a symmetric proposal it makes the Boltzmann distribution stationary.
prereqs: [markov-chain, stationary-distribution]
see_also: [simulated-annealing, metropolis-hastings, detailed-balance, random-walk-metropolis, gibbs-sampling, threshold-accepting, ising-model, cooling-schedule]
sources:
  - paper: doi:10.1063/1.1699114
    title: Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, Journal of Chemical Physics 21(6), 1953
    locator: pages 1087 to 1092 (the rule and the argument for detailed balance)
  - paper: doi:10.1093/biomet/57.1.97
    title: W. Keith Hastings, Monte Carlo sampling methods using Markov chains and their applications, Biometrika 57(1), 1970
    locator: pages 97 to 109 (the general acceptance ratio for asymmetric proposals)
  - paper: doi:10.1093/biomet/60.3.607
    title: Peter H. Peskun, Optimum Monte-Carlo sampling using Markov chains, Biometrika 60(3), 1973
    locator: pages 607 to 612 (the Metropolis acceptance is the largest one with detailed balance)
  - paper: doi:10.1126/science.220.4598.671
    title: Scott Kirkpatrick, C. Daniel Gelatt and Mario P. Vecchi, Optimization by simulated annealing, Science 220(4598), 1983
    locator: pages 671 to 680 (the rule used for optimization with a falling temperature)
---

The Metropolis acceptance criterion is the rule that decides whether a [Markov chain](/markov-chain/) moves from the current state to a proposed one: accept with probability $\min(1, e^{-\Delta/T})$, where $\Delta$ is the change of the objective and $T > 0$ is a temperature. An improvement or an equal move is always accepted, and a worse move is accepted less often the larger it is. With a symmetric proposal, the rule makes the Boltzmann distribution $\pi_T(x) \propto e^{-f(x)/T}$ a [stationary distribution](/stationary-distribution/) of the chain. It is the acceptance step of [simulated annealing](/simulated-annealing/), and the special case of [Metropolis-Hastings](/metropolis-hastings/) for a symmetric proposal.

## Definition

Let $S$ be a set of states, $f : S \to \mathbb{R}$ an objective to minimize (the energy), and $T > 0$. For a current state $x$ and a proposed state $y$, let $\Delta = f(y) - f(x)$. The **Metropolis acceptance probability** is

$$A_T(x, y) = \min\left(1, e^{-\Delta/T}\right) = \begin{cases} 1 & \text{if } \Delta \le 0, \\ e^{-\Delta/T} & \text{if } \Delta > 0. \end{cases}$$

The **Metropolis criterion** accepts $y$ with probability $A_T(x, y)$, independently of the past. In code: accept if $\Delta \le 0$; else draw $u$ uniform in $[0, 1)$ and accept if $u < e^{-\Delta/T}$. For $T = 0$ the rule is read as its limit: accept if and only if $\Delta \le 0$. For a maximization problem, use $\Delta = f(x) - f(y)$.

If the proposal draws $y$ with probability $R(x, y)$ and $R$ is symmetric, $R(x, y) = R(y, x)$, the chain has the transition probabilities $P_T(x, y) = R(x, y) A_T(x, y)$ for $y \ne x$. Then **detailed balance** holds with $\pi_T(x) = e^{-f(x)/T}/Z_T$, $Z_T = \sum_{z} e^{-f(z)/T}$:

$$\pi_T(x) P_T(x, y) = \pi_T(y) P_T(y, x) \quad \text{for all } x, y.$$

*Proof.* Take $x \ne y$ with $f(x) \le f(y)$. The left side is $Z_T^{-1} e^{-f(x)/T} R(x, y) e^{-(f(y) - f(x))/T} = Z_T^{-1} R(x, y) e^{-f(y)/T}$, and the right side is $Z_T^{-1} e^{-f(y)/T} R(y, x) \cdot 1$. They are equal because $R$ is symmetric. Summing over $x$ gives $\pi_T P_T = \pi_T$. $\square$

Only the difference $f(y) - f(x)$ enters the rule, so the normalizing constant $Z_T$ is never needed. This is why the rule is useful: $Z_T$ is a sum over all states, which is usually far too large to compute.

**Maximality (Peskun 1973).** Write the acceptance as a function $a(r)$ of the ratio $r = \pi_T(y)/\pi_T(x) = e^{-\Delta/T}$. Detailed balance with a symmetric proposal says $a(r) = r \, a(1/r)$ for all $r > 0$. A probability has $a \le 1$, so $a(r) = r \, a(1/r) \le r$, and also $a(r) \le 1$. Hence $a(r) \le \min(1, r)$, and the Metropolis rule is the largest acceptance function with detailed balance. Peskun showed that a chain that rejects less often in this sense never has a larger asymptotic variance for its averages.

## Examples and non-examples

**Values of the rule.** The probability of accepting a worse move:

| $\Delta$ | $T = 5$ | $T = 2$ | $T = 1$ | $T = 0.5$ | $T = 0.25$ |
|---|---|---|---|---|---|
| 1 | 0.8187 | 0.6065 | 0.3679 | 0.1353 | 0.0183 |
| 2 | 0.6703 | 0.3679 | 0.1353 | 0.0183 | 0.0003 |
| 4 | 0.4493 | 0.1353 | 0.0183 | 0.0003 | $1.1 \times 10^{-7}$ |

Halving $T$ squares the probability, since $e^{-\Delta/(T/2)} = (e^{-\Delta/T})^2$. Doubling $\Delta$ also squares it.

**A small chain.** Take 8 states on a cycle with energies $f = (3, 1, 4, 2, 5, 0, 3, 6)$, and propose each of the two neighbors with probability $1/2$. At $T = 1$, from state 1 (energy 1) the chain moves to state 0 (energy 3) with probability $\frac12 e^{-2} = 0.0677$, to state 2 (energy 4) with probability $\frac12 e^{-3} = 0.0249$, and stays with probability $0.9074$. The Boltzmann distribution at $T = 1$ is $(0.031, 0.226, 0.011, 0.083, 0.004, 0.613, 0.031, 0.002)$, and it satisfies the detailed balance equations of this chain.

**Barker's rule (an example of another valid rule, not of this one).** Accept with probability $r/(1 + r)$, $r = e^{-\Delta/T}$. It also satisfies $a(r) = r \, a(1/r)$, so it has the same stationary distribution, but it accepts less often: for $\Delta = -1$ and $T = 1$ it accepts with probability $0.7311$ instead of 1, and for $\Delta = 1$ with $0.2689$ instead of $0.3679$.

**Non-example: a threshold.** [Threshold accepting](/threshold-accepting/) accepts $y$ if and only if $\Delta < \tau$ for a threshold $\tau$. The acceptance is 0 or 1. If two neighbors differ in energy by $\tau$ or more, the move down is always accepted and the move up never, so detailed balance holds only for a distribution that gives the upper state mass 0. The rule has no Boltzmann equilibrium.

**Non-example: $e^{-\Delta/T}$ without the minimum.** For $\Delta < 0$ this number is larger than 1, so it is not a probability. Code that tests $u < e^{-\Delta/T}$ still accepts every improvement, because $u < 1$, so the code is correct; but a formula that multiplies by $e^{-\Delta/T}$, for example to compute an expected acceptance, must take the minimum.

**Non-example: an asymmetric proposal.** If $R(x, y) \ne R(y, x)$, the Metropolis rule alone does not give $\pi_T$. The [Metropolis-Hastings](/metropolis-hastings/) rule $\min\left(1, \frac{\pi_T(y) R(y, x)}{\pi_T(x) R(x, y)}\right)$ corrects for it.

## Related definitions

- **Metropolis-Hastings acceptance.** The general rule for an arbitrary target $\pi$ and proposal $R$. The Metropolis criterion is its case $\pi = \pi_T$ and $R$ symmetric.
- **Boltzmann (Gibbs) distribution.** $\pi_T(x) \propto e^{-f(x)/T}$. Large $T$ makes it close to uniform, and $T \to 0$ concentrates it on the global minima of $f$.
- **Heat-bath rule.** Resample one coordinate from its conditional distribution under $\pi_T$. On the [Ising model](/ising-model/) this is [Gibbs sampling](/gibbs-sampling/), also called Glauber dynamics.
- **[Detailed balance](/detailed-balance/).** The reversibility condition that the rule satisfies; it implies stationarity but is stronger.
- **[Cooling schedule](/cooling-schedule/).** The sequence $T_1 \ge T_2 \ge \dots$ that [simulated annealing](/simulated-annealing/) uses in the rule.
- **Deterministic acceptance.** Threshold accepting, the [great deluge algorithm](/great-deluge-algorithm/) and record-to-record travel replace the random test by a fixed bound.

## References
