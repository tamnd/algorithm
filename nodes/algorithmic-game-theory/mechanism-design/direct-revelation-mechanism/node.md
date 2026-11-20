---
tag: 9JE165
kind: definition
slug: direct-revelation-mechanism
name: Direct revelation mechanism
aliases:
- direct mechanism
area: algorithmic-game-theory/mechanism-design
level: intro
summary: A mechanism in which each agent reports a type, and the outcome and the payments are functions of the reports. The revelation principle lets the study of incentives start from these mechanisms.
prereqs: [quasilinear-utility]
see_also: [revelation-principle, dominant-strategy-incentive-compatibility, bayesian-incentive-compatibility, vcg-mechanism, vickrey-auction, first-price-auction, english-auction, gibbard-satterthwaite-theorem]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.3 (mechanisms with money) and Section 9.4.3 (direct and indirect mechanisms and the revelation principle)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 10.2.2 (direct mechanisms and the revelation principle)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 2 (sealed-bid auctions with an allocation rule and a payment rule)
---

A direct revelation mechanism asks each agent to report its private type, usually its valuation of the outcomes, and computes the outcome and the payments from the reports. A general mechanism can let the agents send any messages, and can run in rounds, as an [English auction](/english-auction/) does. The [revelation principle](/revelation-principle/) shows that, for the question of which outcomes can be reached in equilibrium, it is enough to study direct mechanisms in which truth telling is an equilibrium.

## Definition

There are $n$ agents and a set $O$ of outcomes. Agent $i$ has a private type from a set $V_i$. In the quasilinear setting the type is a valuation $v_i : O \to \mathbb{R}$, and agent $i$ has the [quasilinear utility](/quasilinear-utility/) $v_i(o) - p_i$.

A *mechanism* gives each agent a set $M_i$ of messages and has an outcome function $g : M_1 \times \cdots \times M_n \to O \times \mathbb{R}^n$, which maps the messages to an outcome and a payment for each agent. A mechanism is *direct* if $M_i = V_i$ for each $i$: the message of an agent is a claim about its type. A direct mechanism is a pair $(x, p)$:

- the *allocation rule* $x : V_1 \times \cdots \times V_n \to O$ chooses the outcome $x(b)$ from the reports $b = (b_1, \ldots, b_n)$;
- the *payment rule* $p : V_1 \times \cdots \times V_n \to \mathbb{R}^n$ chooses the payments $p(b) = (p_1(b), \ldots, p_n(b))$. Agent $i$ pays $p_i(b)$, and a negative $p_i(b)$ is a transfer to it.

A report $b_i$ may differ from the true type $v_i$. The mechanism is *truthful* in a stated sense when truth telling is an equilibrium: [DSIC](/dominant-strategy-incentive-compatibility/) when it is a dominant strategy, and [BIC](/bayesian-incentive-compatibility/) when it is a Bayes-Nash equilibrium for a given prior. A *social choice function* $f : V_1 \times \cdots \times V_n \to O$ is *implemented* by a direct mechanism with allocation rule $f$ that is truthful.

Without money, a direct mechanism is only the rule $x$. A voting rule that takes the rankings of the voters is a direct mechanism of this kind. A randomized direct mechanism outputs a distribution over outcomes and payments.

## Examples and non-examples

- **The Vickrey auction.** Each bidder reports a value for one item. The highest report wins and pays the second-highest report. With reports $(10, 7, 3)$, bidder 1 wins and pays 7. It is direct and DSIC.
- **The first-price auction.** Each bidder reports a number, the highest wins and pays its own number. In the single-parameter model the message space is the value space, so this is a direct mechanism. It is not truthful: a bidder of value 10 that bids 10 has utility 0 when it wins, and a lower bid that still wins gives more.
- **The VCG mechanism.** Each agent reports a whole valuation $b_i : O \to \mathbb{R}$, the [VCG mechanism](/vcg-mechanism/) maximizes the reported welfare and charges each agent its externality.
- **Posted prices.** A seller posts price 5 and each buyer says whether it accepts. Seen as a direct mechanism, the buyer reports a value and buys when the report is at least 5. Truth telling is dominant.
- **Non-example: the English auction.** The price rises in rounds and a bidder signals at each price whether it stays in. The messages are strategies over time, not types. Its direct version, in which the bidder reports the price at which it would leave, is the Vickrey auction.
- **Non-example: a short bid in a combinatorial auction.** A combinatorial auction in which each bidder may name only one bundle and one price has messages that are smaller than the types, since a valuation has a number for each of the $2^m$ bundles. It is an indirect mechanism, unless the bidders are known to be [single-minded](/single-minded-bidder-mechanism/).

## Related definitions

- **Indirect mechanisms.** Any mechanism that is not direct. Ascending auctions, auctions with [demand queries](/demand-query/) and mechanisms with compact [bidding languages](/bidding-languages/) are indirect. They can use less communication than a direct mechanism.
- **Truthful direct mechanisms.** The incentive conditions are [dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/) and [Bayesian incentive compatibility](/bayesian-incentive-compatibility/). The participation condition is [individual rationality](/individual-rationality/) and the money condition is [budget balance](/budget-balance/).
- **Revelation principle.** Any equilibrium of any mechanism gives a truthful direct mechanism with the same outcomes ([revelation principle](/revelation-principle/)). The principle is about incentives only: the direct version can need far more communication or computation.

## References
