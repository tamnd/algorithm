---
tag: JC2FM9
kind: definition
slug: groves-mechanisms
name: Groves mechanisms
aliases:
- Groves scheme
area: algorithmic-game-theory/mechanism-design
level: core
summary: The mechanisms that choose an outcome of maximum reported welfare and charge each agent a term that ignores its own report, minus the reported welfare of the others. All are DSIC.
prereqs: [dominant-strategy-incentive-compatibility, quasilinear-utility]
see_also: [vcg-mechanism, clarke-pivot-rule, green-laffont-theorem, affine-maximizer, budget-balance, roberts-theorem, maximal-in-range-mechanism]
sources:
  - paper: doi:10.2307/1914085
    title: "Theodore Groves, Incentives in teams, Econometrica 41(4) (1973), 617-631"
    locator: the payment scheme that makes truth telling dominant for any welfare-maximizing decision
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.3.3 (VCG mechanisms in the Groves form) and Section 9.5.5 (uniqueness of prices on connected domains)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 10.4.1 (Groves mechanisms, Definition 10.4.1 and Theorem 10.4.2)
  - paper: doi:10.2307/1911219
    title: "Jerry Green and Jean-Jacques Laffont, Characterization of satisfactory mechanisms for the revelation of preferences for public goods, Econometrica 45(2) (1977), 427-438"
    locator: on unrestricted domains, the Groves mechanisms are the only efficient dominant-strategy mechanisms
  - paper: doi:10.1145/1160633.1160790
    title: "Ruggiero Cavallo, Optimal decision-making with minimal waste, strategyproof redistribution of VCG payments, AAMAS 2006, 882-889"
    locator: a Groves mechanism whose h term rebates part of the VCG revenue
---

A Groves mechanism is a [direct revelation mechanism](/direct-revelation-mechanism/) that chooses an outcome of maximum reported welfare and charges each agent $h_i(b_{-i}) - \sum_{j \ne i} b_j(x)$, where $h_i$ is any function of the reports of the other agents. The three close pages differ in scope. The Groves mechanisms are the whole family, one for each choice of the functions $h_i$. The [Clarke pivot rule](/clarke-pivot-rule/) is one choice of $h_i$, the best welfare of the others. The [VCG mechanism](/vcg-mechanism/) is the Groves mechanism with that choice. Every Groves mechanism is [DSIC](/dominant-strategy-incentive-compatibility/), and on unrestricted domains they are the only efficient DSIC mechanisms ([Green-Laffont theorem](/green-laffont-theorem/)).

## Definition

There are $n$ agents with [quasilinear utilities](/quasilinear-utility/), a set $O$ of outcomes, and reports $b_i : O \to \mathbb{R}$. A direct mechanism $(x, p)$ is a *Groves mechanism* if

1. the allocation rule maximizes the reported welfare: $x(b) \in \arg\max_{o \in O} \sum_j b_j(o)$, with any fixed rule for ties, and
2. for each agent $i$ there is a function $h_i$ of the others' reports $b_{-i}$ only, such that
$$p_i(b) = h_i(b_{-i}) - \sum_{j \ne i} b_j(x(b)).$$

The second term pays agent $i$ the reported welfare of the others at the chosen outcome. The first term is a charge that agent $i$ cannot change.

**Theorem (Groves 1973).** Every Groves mechanism is DSIC.

*Proof.* Let agent $i$ have true valuation $v_i$, and fix $b_{-i}$. If agent $i$ reports $b_i$ and the outcome is $y = x(b_i, b_{-i})$, its utility is
$$v_i(y) - p_i = v_i(y) + \sum_{j \ne i} b_j(y) - h_i(b_{-i}).$$
The last term does not depend on $b_i$. The first two terms are the reported welfare of $y$ with $v_i$ in place of $b_i$. If $i$ reports $v_i$, the mechanism chooses an outcome that maximizes exactly this sum, so no report $b_i$ gives more. $\square$

The proof aligns the incentive of each agent with the welfare: each agent is paid as if it owned the whole economy, up to a constant it cannot affect.

## Examples and non-examples

The examples use one item and values $(10, 7, 3)$. Bidder 1 wins in every Groves mechanism, and $\sum_{j \ne i} b_j(x)$ is 0 for bidder 1 and 10 for each loser.

- **$h_i = 0$.** The payments are $(0, -10, -10)$. Each loser is paid the winner's value, and the mechanism pays out 20. It is DSIC, but has a large deficit.
- **The Clarke pivot term.** With $h_i(b_{-i}) = \max_o \sum_{j \ne i} b_j(o)$, the best welfare of the others, the terms are 7, 10 and 10, and the payments are $(7, 0, 0)$. This is the Vickrey auction, the single-item case of the [VCG mechanism](/vcg-mechanism/).
- **Redistribution.** Take the Clarke term minus a rebate that depends only on $b_{-i}$, such as one $n$-th of the smallest VCG revenue that agent $i$ can produce by any report (Cavallo 2006). Here the rebates are 1, 1 and $7/3$, so the payments are $(6, -1, -7/3)$ and the revenue is $8/3$ instead of 7. The mechanism is still a Groves mechanism, so it is still DSIC.
- **Non-example: a term that depends on the agent's own report.** Rebate one third of the VCG revenue to every agent. The revenue is 7, the bid of bidder 2, so bidder 2 gets a rebate of $7/3$ that grows with its own bid. With a bid of 9 it still loses, and the rebate grows to 3. This is not a Groves mechanism, and it is not DSIC.
- **Non-example: weighted welfare.** An [affine maximizer](/affine-maximizer/) maximizes $\sum_i w_i b_i(o) + c_o$ with weights that are not all equal or with constants $c_o \ne 0$. With the matching payments it is DSIC, but it is not a Groves mechanism because it does not maximize the welfare.
- **Non-example: an approximate optimizer.** If $x(b)$ is only close to the best welfare, the Groves payments do not give DSIC, because the proof uses that $x$ maximizes the sum exactly. An exact maximizer over a fixed subset of outcomes does work ([maximal-in-range mechanism](/maximal-in-range-mechanism/)).

## Related definitions

- **Uniqueness.** If every valuation $O \to \mathbb{R}$ is possible, every efficient DSIC mechanism is a Groves mechanism (Green and Laffont 1977). The same holds on smoothly connected domains (Holmstrom 1979). On such domains the payments of an efficient DSIC mechanism are fixed up to the terms $h_i$ ([Green-Laffont theorem](/green-laffont-theorem/)).
- **No budget balance.** No Groves mechanism has payments that sum to 0 for every report on unrestricted domains with $n \ge 2$ ([budget balance](/budget-balance/)).
- **Affine maximizers.** The weighted generalization. By [Roberts' theorem](/roberts-theorem/), on unrestricted domains with at least 3 outcomes, every DSIC mechanism onto its range is an affine maximizer.
- **The Clarke pivot rule.** The choice of $h_i$ that gives no positive transfers and, for nonnegative valuations, individual rationality ([Clarke pivot rule](/clarke-pivot-rule/)).

## References
