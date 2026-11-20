---
tag: C8QAQE
kind: definition
slug: quasilinear-utility
name: Quasilinear utility
aliases:
- quasilinear preferences
area: algorithmic-game-theory/mechanism-design
level: intro
summary: A utility of the form value of the outcome minus payment. Money then moves utility one for one between agents, and the welfare of an outcome does not depend on the payments.
see_also: [direct-revelation-mechanism, dominant-strategy-incentive-compatibility, vcg-mechanism, single-parameter-environment, transferable-utility-game, budget-balance, revenue-equivalence-theorem]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.3 (mechanisms with money and quasilinear utilities)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 10.3 (quasilinear preferences)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 2 (the quasilinear utility model in single-item auctions)
---

An agent has a quasilinear utility when its utility is the value it has for the outcome minus the money it pays. This is the standard model of mechanism design with money: the [VCG mechanism](/vcg-mechanism/), the [Vickrey auction](/vickrey-auction/) and Myerson's results all assume it. Its main effect is that money is a common measure of utility: a payment from one agent to another moves utility one for one, so the welfare of an outcome does not depend on the payments.

## Definition

Let $O$ be a set of outcomes and let agent $i$ have a valuation $v_i : O \to \mathbb{R}$, the amount of money that outcome $o$ is worth to it. When the outcome is $o$ and agent $i$ pays $p_i$ (a negative $p_i$ is a transfer to the agent), its utility is

$$u_i(o, p_i) = v_i(o) - p_i.$$

A preference of agent $i$ over pairs $(o, p_i)$ is *quasilinear* if some valuation $v_i$ represents it in this way. The utility is linear in money with coefficient 1, and only the outcome part can be nonlinear. So the amount that agent $i$ would pay to change the outcome from $o$ to $o'$ is $v_i(o') - v_i(o)$, and it does not depend on the wealth of the agent or on the payments already made.

For random outcomes and payments, the agent maximizes the expected utility $\mathbb{E}[v_i(o)] - \mathbb{E}[p_i]$, so it is risk neutral in money.

With $n$ agents, the *welfare* of an outcome is $\sum_i v_i(o)$, and the *revenue* of the mechanism is $\sum_i p_i$. The sum of the utilities is the welfare minus the revenue.

## Examples and non-examples

- **One item.** The outcomes are "agent $j$ wins" for each $j$, and possibly "nobody wins". Agent $i$ has one number $t_i$: $v_i = t_i$ if $i$ wins and $0$ otherwise. In a [Vickrey auction](/vickrey-auction/) with values $(10, 7, 3)$, agent 1 wins and pays 7, so its utility is $10 - 7 = 3$, and the losers have utility 0. This is a [single-parameter environment](/single-parameter-environment/).
- **Public project.** The outcomes are "build" and "do not build". A citizen with $v_i(\text{build}) = 150$ who pays 120 when the project is built has utility 30. A citizen hurt by the project has a negative value for "build".
- **Combinatorial valuations.** With items $M$, the outcome is an allocation, and $v_i$ depends only on the bundle that agent $i$ gets. Complements, such as $v(\{A, B\}) = 10$ and $v(\{A\}) = v(\{B\}) = 0$, are quasilinear too. Quasilinearity is about money, not about the shape of $v_i$.
- **Non-example: a budget.** A bidder with value 10 for an item and only 6 in cash has utility $10 - p$ when $p \le 6$, and cannot pay more. The utility is not of the form $v_i(o) - p_i$ for all $p_i$. In a Vickrey auction against a bid of 7, the truthful bid wins at a price the bidder cannot pay.
- **Non-example: wealth effects.** Let the utility be $\sqrt{w - p} + v(o)$ with wealth $w$, $v(\text{win}) = 1$ and $v(\text{lose}) = 0$. The highest price that the agent accepts for the item solves $\sqrt{w - p} + 1 = \sqrt{w}$. With $w = 16$ it is 7, and with $w = 25$ it is 9. The willingness to pay depends on wealth, so no valuation represents this preference.
- **Non-example over lotteries: risk aversion.** The utility $g(v_i(o) - p_i)$ with $g$ strictly increasing and strictly concave orders the sure pairs $(o, p_i)$ in the same way as $v_i(o) - p_i$. So for a deterministic mechanism it is still quasilinear. Over lotteries it is not, because the agent prefers a sure payment to a random one with the same mean. This is why the [revenue equivalence theorem](/revenue-equivalence-theorem/) fails for risk-averse bidders.

## Related definitions

- **Utility function in general.** The [utility function](/utility-function/) of decision analysis is any function that represents a preference. A quasilinear utility is a special form, separable in money.
- **Transferable utility.** In cooperative games, [transferable utility](/transferable-utility-game/) is the same assumption: a coalition has a total worth that it can split by side payments in any way.
- **Direct mechanisms and incentives.** A [direct revelation mechanism](/direct-revelation-mechanism/) asks the agents for their valuations, and [dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/) is stated with the quasilinear utility.
- **Budget balance and individual rationality.** [Budget balance](/budget-balance/) is a condition on the revenue, and [individual rationality](/individual-rationality/) asks that each utility is at least 0.

## References
