---
tag: GDXFW2
kind: definition
slug: dominant-strategy-incentive-compatibility
name: Dominant-strategy incentive compatibility
aliases:
- DSIC
- strategyproofness
- truthfulness
area: algorithmic-game-theory/mechanism-design
level: intro
summary: A direct mechanism is DSIC when truth telling is a dominant strategy for every agent, whatever the others report. Unlike BIC it needs no prior on the types.
prereqs: [direct-revelation-mechanism, dominant-strategy]
see_also: [bayesian-incentive-compatibility, vickrey-auction, vcg-mechanism, myerson-lemma, cycle-monotonicity, revelation-principle, truthful-in-expectation, gibbard-satterthwaite-theorem]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.3.2 (incentive compatible mechanisms) and Section 9.5 (characterizations of incentive compatible mechanisms)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 2 (DSIC and the Vickrey auction) and Lecture 3 (Myerson's lemma)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 10.2 (implementation in dominant strategies) and Section 10.4 (Groves and VCG mechanisms)
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the second-price sealed-bid auction, in which bidding the true value is a dominant strategy
---

A direct mechanism is dominant-strategy incentive compatible (DSIC) when reporting the true type is a [dominant strategy](/dominant-strategy/) for every agent: no false report ever gives an agent more utility, whatever the other agents report. The difference from [Bayesian incentive compatibility](/bayesian-incentive-compatibility/) (BIC) is the quantifier on the others: BIC asks only that truth is best on average over a known prior when the others tell the truth, while DSIC asks that it is best against every report of the others, with no prior. So DSIC implies BIC for every prior, and the converse fails.

## Definition

Let $(x, p)$ be a [direct revelation mechanism](/direct-revelation-mechanism/) for $n$ agents with [quasilinear utilities](/quasilinear-utility/), and let $V_i$ be the set of possible types of agent $i$. The mechanism is DSIC if for every agent $i$, every true type $v_i \in V_i$, every report $b_i \in V_i$ and every profile $b_{-i}$ of reports of the others,

$$v_i(x(v_i, b_{-i})) - p_i(v_i, b_{-i}) \ \ge\ v_i(x(b_i, b_{-i})) - p_i(b_i, b_{-i}).$$

The inequality is weak: truth must be a best response to every $b_{-i}$, and a lie may tie with it. The condition is about the mechanism, not about a game with a prior. It must hold for reports $b_{-i}$ that are not true types of anyone.

Two other forms are often used:

- **Strategyproofness without money.** For a rule $f$ from profiles of preferences to outcomes, no agent gets an outcome it strictly prefers by a false report. For voting rules this is the strategyproofness of the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/).
- **Prices on a menu.** A mechanism is DSIC if and only if, for each agent $i$ and each $b_{-i}$, the payment of $i$ depends only on the outcome, $p_i = \pi_i(x, b_{-i})$, and the truthful report gives agent $i$ an outcome that maximizes $v_i(o) - \pi_i(o, b_{-i})$ over the outcomes that $i$ can reach. The others set a menu of prices, and the mechanism picks the best item on the menu for agent $i$ (Nisan, Section 9.5).

For randomized mechanisms there are two forms. A mechanism is *universally truthful* if it is a distribution over DSIC mechanisms, and [truthful in expectation](/truthful-in-expectation/) if the inequality holds for the expected utilities. The first implies the second.

## Examples and non-examples

- **The Vickrey auction is DSIC.** One item, values $(10, 7, 3)$. With the truth, bidder 1 wins, pays 7 and has utility 3. A bid below 7 loses and gives 0, and any bid above 7 gives the same 3, because the price does not depend on its own bid. Bidder 2 has utility 0 with the truth, and a bid above 10 wins at price 10, which gives $7 - 10 = -3$. This holds against every bid of the others ([Vickrey auction](/vickrey-auction/)).
- **The first-price auction is not DSIC.** With the same bids of the others, 7 and 3, bidder 1 bids 10 and has utility 0 when it wins at its own price. A bid of 8 still wins and gives $10 - 8 = 2$.
- **VCG is DSIC.** For any outcome set and any valuations, the [VCG mechanism](/vcg-mechanism/) and every [Groves mechanism](/groves-mechanisms/) are DSIC.
- **Posted prices are DSIC.** A take-it-or-leave-it price that does not depend on the agent's report, with the agent buying exactly when its value is at least the price.
- **Single-parameter DSIC mechanisms.** When each agent has one number $v_i$ and its value is $v_i x_i$, a mechanism is DSIC (with the normalization $p_i(0, b_{-i}) = 0$) exactly when $x_i$ is nondecreasing in $b_i$ and the payment is given by the formula of [Myerson's lemma](/myerson-lemma/).
- **Non-example: VCG with an approximate optimizer.** If the outcome is only near the best welfare, an agent can gain by a report that makes the heuristic choose a better outcome for the agent. The payments of VCG are DSIC only with an exact maximizer, or with an exact maximizer over a fixed range ([maximal-in-range mechanism](/maximal-in-range-mechanism/)).
- **Non-example: groups.** DSIC is about one agent at a time. In VCG two losing bidders can both overbid and win together at price 0, so VCG is not group strategyproof.

## Related definitions

- **BIC.** Truth is a Bayes-Nash equilibrium for a given prior ([Bayesian incentive compatibility](/bayesian-incentive-compatibility/), with [Bayes-Nash equilibrium](/bayes-nash-equilibrium/)). The [AGV mechanism](/agv-mechanism/) is BIC, efficient and budget balanced. No DSIC mechanism has all three on unrestricted domains ([Green-Laffont theorem](/green-laffont-theorem/)).
- **Characterizations.** For single-parameter agents, [monotone allocation rules](/monotone-allocation-rule/) are exactly the DSIC ones ([Myerson's lemma](/myerson-lemma/)). For general types, [cycle monotonicity](/cycle-monotonicity/) is necessary and sufficient. On unrestricted domains with at least 3 outcomes, the DSIC allocation rules onto their range are the [affine maximizers](/affine-maximizer/) ([Roberts' theorem](/roberts-theorem/)).
- **Revelation principle.** Any mechanism with a dominant-strategy equilibrium gives a DSIC direct mechanism with the same outcomes ([revelation principle](/revelation-principle/)).
- **Individual rationality.** DSIC says nothing about whether an agent wants to take part. That is [individual rationality](/individual-rationality/).

## References
