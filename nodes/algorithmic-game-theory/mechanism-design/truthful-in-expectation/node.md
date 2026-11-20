---
tag: Q1AATA
kind: definition
slug: truthful-in-expectation
name: Truthful in expectation
aliases:
- truthfulness in expectation
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "A randomized mechanism is truthful in expectation if truth telling maximizes each risk-neutral agent's expected utility over the mechanism's coins. Universal truthfulness is stronger."
prereqs: [dominant-strategy-incentive-compatibility, myerson-lemma]
see_also: [maximal-in-range-mechanism, bayesian-incentive-compatibility, monotone-allocation-rule, randomized-rounding, lp-relaxation, truthful-scheduling-unrelated-machines, facility-location-mechanism, cycle-monotonicity]
sources:
  - paper: "Ron Lavi and Chaitanya Swamy, Truthful and near-optimal mechanism design via linear programming, Journal of the ACM 58(6) (2011), Article 25 (conference version in FOCS 2005)"
    locator: truthful-in-expectation mechanisms from LP relaxations with a known integrality gap
  - paper: "Shahar Dobzinski and Shaddin Dughmi, On the power of randomization in algorithmic mechanism design, Proceedings of the 50th IEEE Symposium on Foundations of Computer Science (FOCS 2009)"
    locator: maximal-in-distributional-range mechanisms, the comparison of truthful in expectation with universally truthful mechanisms, and the FPTAS for multi-unit auctions
  - paper: "Aaron Archer and Eva Tardos, Truthful mechanisms for one-parameter agents, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001), 482-491"
    locator: the randomized 3-approximation for scheduling on related machines that is truthful in expectation
  - paper: "Ahuva Mu'alem and Michael Schapira, Setting lower bounds on truthfulness, Games and Economic Behavior 110 (2018), 174-193"
    locator: lower bounds for randomized truthful mechanisms, including scheduling on unrelated machines
  - paper: "George Christodoulou, Elias Koutsoupias and Annamaria Kovacs, A proof of the Nisan-Ronen conjecture, an overview, ACM SIGecom Exchanges 21(1) (2023), 42-48"
    locator: the conclusion, which states the open gap between the lower bound 2 and the upper bound (n+1)/2 for randomized and fractional scheduling mechanisms
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 12, Ron Lavi, Computationally efficient approximation mechanisms
---

A randomized mechanism is *truthful in expectation* if, for every agent and every report of the others, telling the truth maximizes the agent's expected utility, where the expectation is over the mechanism's own random choices. This assumes the agents are risk neutral. A stronger notion, *universal truthfulness*, asks that the mechanism be a random choice among deterministic [DSIC](/dominant-strategy-incentive-compatibility/) mechanisms, so truth telling is best for every outcome of the coins. The close page [maximal-in-range mechanism](/maximal-in-range-mechanism/) is a deterministic and fully DSIC technique. Its randomized form, maximal in distributional range, is the main way to build mechanisms that are truthful in expectation only.

## Definition

A randomized direct mechanism is a pair $(x, p)$ where, for reports $b$ and a random seed $\omega$, $x(b, \omega)$ is an outcome and $p(b, \omega) \in \mathbb{R}^n$ are payments. Agent $i$ with valuation $v_i$ has [quasilinear utility](/quasilinear-utility/) $v_i(x) - p_i$.

**Truthful in expectation.** For every agent $i$, every true valuation $v_i$, every report $b_i$ and every profile $b_{-i}$,
$$\mathbb{E}_\omega\bigl[v_i(x(v_i, b_{-i}, \omega)) - p_i(v_i, b_{-i}, \omega)\bigr] \;\ge\; \mathbb{E}_\omega\bigl[v_i(x(b_i, b_{-i}, \omega)) - p_i(b_i, b_{-i}, \omega)\bigr].$$

**Universally truthful.** For every fixed seed $\omega$, the deterministic mechanism $(x(\cdot, \omega), p(\cdot, \omega))$ is DSIC.

Every universally truthful mechanism is truthful in expectation, by taking expectations. The converse fails, as the example below shows. Since only expected payments matter for truthfulness in expectation, the payments can always be replaced by their expectations, which are deterministic.

In a [single-parameter environment](/single-parameter-environment/), [Myerson's lemma](/myerson-lemma/) applies to expectations. A randomized allocation rule is truthful in expectation with suitable payments if and only if the expected allocation $\bar{x}_i(z, b_{-i}) = \mathbb{E}_\omega[x_i(z, b_{-i}, \omega)]$ is nondecreasing in $z$, and then the expected payment is $b_i \bar{x}_i(b) - \int_0^{b_i} \bar{x}_i(z, b_{-i}) \, dz$ when a zero bid pays zero.

## Examples and non-examples

A small example that separates the two notions. One bidder bids $b \in [0, 1]$ for one item and has value $v \in [0, 1]$.

- **Mechanism A.** Give the item with probability $b$ and always charge $b^2/2$. The expected utility is $v b - b^2/2$, whose derivative $v - b$ is zero at $b = v$, and the function is concave, so the truthful bid is best. Mechanism A is truthful in expectation. Myerson's formula agrees: $b \cdot b - \int_0^b z \, dz = b^2/2$. It is not universally truthful. Write the coin as a uniform $u \in [0, 1]$ and give the item when $b \ge u$. For a fixed $u$ and a value $v > u$, the bid $b = u$ still wins and pays $u^2/2 < v^2/2$, so the truthful bid is not best. A bidder who loses also pays $b^2/2$, so its utility after the coin is negative.
- **Mechanism B.** Draw $u$ uniformly from $[0, 1]$, give the item when $b \ge u$, and charge $u$ to a winner. For each fixed $u$ this is a posted price, which is DSIC, so mechanism B is universally truthful. It has the same expected allocation $b$ and the same expected payment $\int_0^b u \, du = b^2/2$ as mechanism A.

More examples:

- **Maximal in distributional range.** Fix a set of lotteries over outcomes, pick the lottery with the largest expected reported welfare, and charge VCG payments in expectation. Dobzinski and Dughmi (2009) used this to get an FPTAS for multi-unit auctions that is truthful in expectation.
- **LP-based mechanisms.** Lavi and Swamy (2005 conference, 2011 journal) solve the [LP relaxation](/lp-relaxation/) of a packing problem with VCG payments, scale the fractional solution down by the integrality gap, and write the result as a lottery over integral solutions. The mechanism is truthful in expectation, and its approximation ratio is the integrality gap.
- **Related machines.** Archer and Tardos (2001) gave a randomized 3-approximation for makespan on related machines that is truthful in expectation.

Non-examples:

- **Risk-averse agents.** If an agent prefers a sure amount to a lottery with the same mean, a mechanism that is truthful only in expectation, such as mechanism A, can give it reasons to lie. Truthfulness in expectation assumes risk neutrality.
- **Agents who see the coins first.** If the seed is revealed before the agents report, only universal truthfulness protects the mechanism.
- **Bayesian incentive compatibility.** [BIC](/bayesian-incentive-compatibility/) takes the expectation over the other agents' types, not over the mechanism's coins. It is a different notion. Truthful in expectation implies BIC for any distribution of types, by taking a second expectation, but a BIC mechanism can fail to be truthful in expectation for some reports of the others.

## Related definitions

- **[DSIC](/dominant-strategy-incentive-compatibility/).** For deterministic mechanisms, truthful in expectation, universally truthful and DSIC are the same.
- **[Maximal-in-range mechanism](/maximal-in-range-mechanism/).** The deterministic technique whose randomized form gives truthful-in-expectation mechanisms.
- **[Monotone allocation rule](/monotone-allocation-rule/).** For one-number types, monotonicity of the expected allocation is the condition.
- **[Cycle monotonicity](/cycle-monotonicity/).** For general types, the condition applies to the lotteries chosen by the mechanism, with expected values in place of values.
- **Scheduling bounds.** For [truthful scheduling on unrelated machines](/truthful-scheduling-unrelated-machines/), the deterministic optimum ratio is $n$, while for randomized mechanisms the known bounds are a lower bound of about 2, from Mu'alem and Schapira, and an upper bound of $(n + 1)/2$, as summarized by Christodoulou, Koutsoupias and Kovacs (2023).
- **Mechanisms without money.** Randomized rules can be strategyproof in expectation without payments, for example in [strategyproof facility location](/facility-location-mechanism/).

## References
