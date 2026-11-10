---
tag: PJZTFY
kind: concept
slug: acceptance-probability
name: Acceptance probability
aliases:
- acceptance ratio
- Metropolis ratio
- Metropolis-Hastings ratio
area: randomized/markov-chain-monte-carlo
level: intro
summary: The probability α(x, y) that a Metropolis-type sampler moves to a proposed state. min(1, r) is the largest valid choice, and by Peskun's theorem it gives the smallest asymptotic variance.
prereqs: [metropolis-hastings, detailed-balance]
see_also: [proposal-distribution, metropolis-criterion, random-walk-metropolis, metropolis-adjusted-langevin-algorithm, hamiltonian-monte-carlo, effective-sample-size]
sources:
  - paper: doi:10.1093/biomet/57.1.97
    title: W. Keith Hastings, Monte Carlo sampling methods using Markov chains and their applications, Biometrika 57(1), 1970
    locator: pages 97 to 109 (the family of acceptance functions α = s/(1 + t) and its two members of Metropolis and Barker)
  - paper: doi:10.1093/biomet/60.3.607
    title: Peter H. Peskun, Optimum Monte-Carlo sampling using Markov chains, Biometrika 60(3), 1973
    locator: pages 607 to 612 (the ordering of reversible kernels on a finite space by their off-diagonal entries, and the optimality of the Metropolis-Hastings acceptance)
  - paper: doi:10.1071/PH650119
    title: A. A. Barker, Monte Carlo calculations of the radial distribution functions for a proton-electron plasma, Australian Journal of Physics 18(2), 1965
    locator: pages 119 to 134 (the acceptance rule r/(1 + r))
  - paper: doi:10.1214/aoap/1027961031
    title: Luke Tierney, A note on Metropolis-Hastings kernels for general state spaces, Annals of Applied Probability 8(1), 1998
    locator: pages 1 to 9 (the Peskun ordering on a general state space)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 7, The Metropolis-Hastings algorithm
---

The acceptance probability $\alpha(x, y)$ of a [Metropolis-Hastings](/metropolis-hastings/) sampler is the probability that the chain moves from its state $x$ to a candidate $y$ drawn from the [proposal distribution](/proposal-distribution/) $Q(x, \cdot)$. It is chosen so that the chain satisfies [detailed balance](/detailed-balance/) with respect to the target $\pi$. The standard choice is $\min(1, r)$ with the Metropolis-Hastings ratio $r = \pi(y)Q(y, x)/(\pi(x)Q(x, y))$. This page is about the rule itself: which rules are valid, why $\min(1, r)$ is the best one (Peskun's theorem), and what the average acceptance rate says about a sampler. The algorithm that uses it is on the [Metropolis-Hastings](/metropolis-hastings/) page.

## In plain words

A Metropolis-type sampler first suggests a move and then decides if it takes the move. The acceptance probability is the chance that it takes the move. If it does not, it stays where it is and counts the current state one more time.

The rule must be fair in both directions: in the long run, the flow of probability from one state to another must equal the flow back. Many rules have this property. The usual rule accepts every move to a more likely state, and accepts a move to a less likely state with a chance equal to the ratio of the two likelihoods. An older rule, from Barker, accepts less often.

A rule that accepts more often wastes fewer steps. Peskun proved that the usual rule is the best one: no fair rule accepts more often, and it gives the most precise averages.

## The idea

Fix a target $\pi$ and a proposal $Q$, both as densities with respect to a common reference measure. For $x \ne y$ with $Q(x, y) > 0$, the chain moves with density $P(x, y) = Q(x, y)\alpha(x, y)$, and all rejected mass stays at $x$. Write

$$r(x, y) = \frac{\pi(y)Q(y, x)}{\pi(x)Q(x, y)}, \qquad r(y, x) = \frac{1}{r(x, y)}.$$

**The condition.** The chain satisfies detailed balance with respect to $\pi$ if and only if, for all $x \ne y$,

$$\pi(x)Q(x, y)\alpha(x, y) = \pi(y)Q(y, x)\alpha(y, x), \quad\text{that is,}\quad \alpha(x, y) = r(x, y)\,\alpha(y, x) \text{ when both } Q(x, y), Q(y, x) > 0.$$

The rejected mass sits on the diagonal and plays no part in detailed balance. So any $\alpha$ with values in $[0, 1]$ that meets this condition gives a kernel with $\pi$ stationary.

**Hastings' family.** Hastings (1970) wrote the valid rules as $\alpha(x, y) = s(x, y)/(1 + 1/r(x, y))$, with $s$ symmetric, $s(x, y) = s(y, x)$, and small enough that $\alpha \le 1$. Two members are standard:

| rule | $\alpha(x, y)$ | $s(x, y)$ |
|---|---|---|
| Metropolis-Hastings (1953, 1970) | $\min(1, r)$ | $1 + \min(r, 1/r)$ |
| Barker (1965) | $r/(1 + r)$ | $1$ |

Both meet the condition. For Metropolis-Hastings, $\pi(x)Q(x, y)\min(1, r) = \min(\pi(x)Q(x, y), \pi(y)Q(y, x))$ is symmetric. For Barker, $\pi(x)Q(x, y)\cdot r/(1 + r) = \pi(x)Q(x, y)\pi(y)Q(y, x)/(\pi(x)Q(x, y) + \pi(y)Q(y, x))$ is symmetric. Barker's rule is the one that a heat-bath (Gibbs) choice between the two states $x$ and $y$ gives.

**Theorem (maximality).** If $\alpha$ meets the condition and $0 \le \alpha \le 1$, then $\alpha(x, y) \le \min(1, r(x, y))$ for all $x \ne y$.

*Proof.* If $Q(y, x) = 0$ or $\pi(y) = 0$, the condition gives $\pi(x)Q(x, y)\alpha(x, y) = 0$, so $\alpha(x, y) = 0 \le \min(1, r)$ when $\pi(x)Q(x, y) > 0$. Otherwise $\alpha(x, y) = r(x, y)\alpha(y, x) \le r(x, y)$ because $\alpha(y, x) \le 1$, and $\alpha(x, y) \le 1$ by assumption. $\square$

So the Metropolis-Hastings rule accepts each single move at least as often as every other valid rule with the same proposal.

**Theorem (Peskun 1973).** Let $P_1$ and $P_2$ be transition matrices on a finite space, both reversible with respect to $\pi$, with $P_1(x, y) \ge P_2(x, y)$ for all $x \ne y$. Then for every function $f$, the asymptotic variances satisfy $v(f, P_1) \le v(f, P_2)$, where

$$v(f, P) = \lim_{T \to \infty} T\cdot\operatorname{Var}\Big(\frac{1}{T}\sum_{t=1}^{T} f(X_t)\Big) \quad\text{for the stationary chain } X_1 \sim \pi.$$

Tierney (1998) proved the same ordering on general state spaces. With the maximality theorem, it gives: for a fixed proposal, the Metropolis-Hastings rule has the smallest asymptotic variance of all rules in Hastings' family, for every $f$. The proof uses the formula $v(f, P) = \langle \bar f, (I + P)(I - P)^{-1}\bar f\rangle_\pi$ for the centered $\bar f = f - E_\pi f$ and shows that this quadratic form decreases when off-diagonal mass grows; see Peskun's paper or Robert and Casella, Chapter 7.

**The acceptance rate.** The average acceptance rate of a stationary chain is

$$\bar\alpha = \int\!\!\int \pi(x)Q(x, y)\alpha(x, y)\,dy\,dx.$$

Peskun's theorem compares rules for a *fixed* proposal. It does not say that a higher $\bar\alpha$ is better across proposals: a [random-walk](/random-walk-metropolis/) proposal with a tiny step has $\bar\alpha$ close to 1 and moves very slowly. For proposals with a scale parameter, theory gives the rate that is best in high dimension: about $0.234$ for [random-walk Metropolis](/random-walk-metropolis/) (Roberts, Gelman and Gilks 1997), about $0.574$ for [MALA](/metropolis-adjusted-langevin-algorithm/) (Roberts and Rosenthal 1998), and about $0.651$ for [HMC](/hamiltonian-monte-carlo/) (Beskos, Pillai, Roberts, Sanz-Serna and Stuart 2013). Each of these numbers holds only under the hypotheses of its theorem, which the linked pages state.

**In floating point.** Compute $\log r$, and accept when $\log r \ge 0$ or $u < e^{\log r}$ for a uniform $u \in [0, 1)$. The direct ratio overflows or underflows for targets with many factors.

## Examples

**Metropolis-Hastings against Barker.** Take three states with $\tilde\pi = (1, 2, 3)$, so $\pi = (1/6, 1/3, 1/2)$, and a proposal that picks one of the two other states with probability $1/2$ each. The two rules give

$$P_{\mathrm{MH}} = \begin{pmatrix} 0 & 1/2 & 1/2 \\ 1/4 & 1/4 & 1/2 \\ 1/6 & 1/3 & 1/2 \end{pmatrix}, \qquad P_{\mathrm{B}} = \begin{pmatrix} 7/24 & 1/3 & 3/8 \\ 1/6 & 8/15 & 3/10 \\ 1/8 & 1/5 & 27/40 \end{pmatrix}.$$

For example, $P_{\mathrm{B}}(0, 2) = \frac12\cdot\frac{3}{1 + 3} = \frac38$. Each off-diagonal entry of $P_{\mathrm{MH}}$ is at least the one of $P_{\mathrm{B}}$. For $f(x) = x$, the exact asymptotic variances, from the fundamental matrix $(I - P + \mathbf{1}\pi)^{-1}$, are $v(f, P_{\mathrm{MH}}) = 23/45 \approx 0.511$ and $v(f, P_{\mathrm{B}}) = 1$. Independent draws from $\pi$ would give $\operatorname{Var}_\pi f = 5/9 \approx 0.556$. So here the Metropolis-Hastings chain is even better than independent sampling, and the Barker chain needs about $45/23 \approx 1.96$ times as many steps for the same precision.

**The Metropolis criterion.** For a Boltzmann target $\pi(x) \propto e^{-E(x)/k_BT}$ and a symmetric proposal, $r = e^{-(E(y) - E(x))/k_BT}$. A move down in energy is always accepted. A move up by $\Delta E$ is accepted with probability $e^{-\Delta E/k_BT}$. This is the [Metropolis criterion](/metropolis-criterion/) of [simulated annealing](/simulated-annealing/).

**Always accept.** If $Q(x, \cdot) = \pi(\cdot \mid x_{-i})$, the full conditional of one coordinate, then $r = 1$ for every candidate. This is [Gibbs sampling](/gibbs-sampling/).

**The Hastings factor matters.** On a cycle of four states with a uniform target, a proposal that steps clockwise with probability $2/3$ has $r = 1/2$ for a clockwise move and $r = 2$ for the reverse. Without the factor $Q(y, x)/Q(x, y)$ the chain would still keep the uniform distribution (each row and column sums to 1), but it would not be reversible, and on a non-uniform target it would have the wrong stationary distribution.

**A non-example.** The rule $\alpha(x, y) = \min(1, \pi(y)/\pi(x))$ with an asymmetric proposal does not meet the condition. On the exponential target $\pi(x) = e^{-x}$ with the multiplicative proposal $y = x e^{\sigma Z}$, it leaves the measure with density proportional to $e^{-x}/x$ invariant, which cannot be normalized; the chain drifts toward 0.

## Where it is used

- Every [Metropolis-Hastings](/metropolis-hastings/) sampler: [random-walk Metropolis](/random-walk-metropolis/), the [independence sampler](/independence-sampler/), [MALA](/metropolis-adjusted-langevin-algorithm/), [HMC](/hamiltonian-monte-carlo/).
- The swap move of [parallel tempering](/parallel-tempering/) and the jump move of [reversible-jump MCMC](/reversible-jump-mcmc/), whose ratio has an extra Jacobian factor.
- The [Wang-Landau](/wang-landau/) walk, which uses the ratio of the current density-of-states estimates.
- Tuning: the acceptance rate is the simplest signal for the step size of a sampler, next to the [effective sample size](/effective-sample-size/).

## References
