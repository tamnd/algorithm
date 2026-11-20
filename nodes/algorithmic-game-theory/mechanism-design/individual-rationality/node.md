---
tag: SQA1P2
kind: definition
slug: individual-rationality
name: Individual rationality
aliases:
- participation constraint
- voluntary participation
area: algorithmic-game-theory/mechanism-design
level: intro
summary: A mechanism is individually rational when each truthful agent gets at least the utility of staying out, usually 0. Ex post, interim and ex ante forms differ in what is averaged.
prereqs: [direct-revelation-mechanism]
see_also: [budget-balance, clarke-pivot-rule, vcg-mechanism, myerson-satterthwaite-theorem, agv-mechanism, dominant-strategy-incentive-compatibility, bayesian-incentive-compatibility]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.3.4 (individual rationality, no positive transfers, and the Clarke pivot rule)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 10.3 (properties of quasilinear mechanisms, with ex interim and ex post individual rationality) and Section 10.4.3 (VCG and individual rationality)
  - paper: "Roger B. Myerson and Mark A. Satterthwaite, Efficient mechanisms for bilateral trading, Journal of Economic Theory 29(2) (1983), 265-281"
    locator: interim individual rationality as one of the conditions of the impossibility of efficient bilateral trade
---

A mechanism is individually rational (IR) when no agent that tells the truth ends with less utility than it would have by not taking part. The utility of staying out is usually normalized to 0, so IR asks that $u_i \ge 0$. It differs from [budget balance](/budget-balance/), the condition it is most often paired with: IR protects the agents from losses, while budget balance protects the mechanism from a deficit. The two pull in opposite directions, because large transfers to the agents make IR easy and budget balance hard.

## Definition

Let $(x, p)$ be a [direct revelation mechanism](/direct-revelation-mechanism/) with [quasilinear utilities](/quasilinear-utility/), and write $u_i(v) = v_i(x(v)) - p_i(v)$ for the utility of agent $i$ when all agents report the true profile $v$. There are three forms, and a page must say which one it uses.

- **Ex post IR.** $u_i(v) \ge 0$ for every agent $i$ and every type profile $v$. This is the form that goes with [DSIC](/dominant-strategy-incentive-compatibility/). It is often stated for agent $i$ truthful and any reports $b_{-i}$ of the others: $v_i(x(v_i, b_{-i})) - p_i(v_i, b_{-i}) \ge 0$.
- **Interim IR.** With a prior $F$ on the types, $\mathbb{E}_{v_{-i}}[u_i(v_i, v_{-i})] \ge 0$ for every agent $i$ and every type $v_i$. The agent knows its own type and averages over the others. This is the form that goes with [BIC](/bayesian-incentive-compatibility/).
- **Ex ante IR.** $\mathbb{E}_v[u_i(v)] \ge 0$ for every agent $i$. The agent decides before it learns its type.

Ex post IR implies interim IR, which implies ex ante IR. When the outside option depends on the type, the condition is $u_i \ge \bar u_i(v_i)$ with a given function $\bar u_i$.

A related condition is *no positive transfers*: $p_i \ge 0$ for every report, so the mechanism never pays an agent. With no positive transfers and IR together, the payments are between 0 and the value of the outcome to the agent.

## Examples and non-examples

- **The Vickrey auction is ex post IR.** With values $(10, 7, 3)$, the utilities are 3, 0 and 0. The winner pays at most its own bid and the losers pay nothing.
- **VCG with nonnegative values is ex post IR.** The [Clarke pivot rule](/clarke-pivot-rule/) gives $u_i \ge 0$ for every agent when every valuation is nonnegative, and also no positive transfers.
- **VCG with a negative value is not.** For a project, let agent 1 value "build" at 5 and agent 2 value it at $-2$, both with value 0 for "do not build". VCG builds. Agent 1 pays 2 and agent 2 pays 0, so agent 2 has utility $-2$.
- **An entry fee separates the three forms.** Run a Vickrey auction with two bidders and charge each an entry fee of 1. Each value is 0 or 10 with probability $1/2$, independently, and ties are broken by a fair coin. A bidder of value 10 wins at price 0 when the other has value 0, and has utility 0 in the case of a tie at 10, so its interim utility is $\frac12 \cdot 10 - 1 = 4$. A bidder of value 0 has interim utility $-1$. The ex ante utility is $\frac12 \cdot 4 + \frac12 \cdot (-1) = 3/2$. So the mechanism is ex ante IR, not interim IR for the type 0, and not ex post IR for a bidder of value 10 that loses the tie.
- **IR bought with money: Groves payments with $h_i = 0$.** Each agent receives the reported welfare of the others, so its utility is the total welfare, which is at least 0 for nonnegative values. But the mechanism pays out large sums. With values $(10, 7, 3)$ for one item, each agent has utility 10, and the two losers each receive 10. IR is easy when the budget is not a concern.

## Related definitions

- **Budget balance.** The sum of the payments is 0 (strong) or at least 0 (weak) ([budget balance](/budget-balance/)). The [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/) shows that for bilateral trade with independent private values and overlapping supports, no mechanism is efficient, BIC, interim IR and weakly budget balanced at once.
- **AGV.** The [AGV mechanism](/agv-mechanism/) is efficient, BIC and strongly budget balanced, but not IR in general.
- **Clarke pivot rule.** The choice of the $h_i$ term in Groves payments that gives ex post IR and no positive transfers for nonnegative valuations ([Clarke pivot rule](/clarke-pivot-rule/)).
- **Incentive compatibility.** IR is a condition on the utility at the truthful report, while DSIC and BIC compare the truthful report with lies. A mechanism can have either property without the other.

## References
