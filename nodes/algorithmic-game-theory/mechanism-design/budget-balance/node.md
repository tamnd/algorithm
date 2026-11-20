---
tag: MVM5NJ
kind: definition
slug: budget-balance
name: Budget balance
aliases:
- weak budget balance
- strong budget balance
area: algorithmic-game-theory/mechanism-design
level: core
summary: A mechanism is strongly budget balanced when the payments sum to 0, and weakly budget balanced when they sum to at least 0, so the mechanism never runs a deficit.
prereqs: [direct-revelation-mechanism]
see_also: [individual-rationality, green-laffont-theorem, agv-mechanism, myerson-satterthwaite-theorem, groves-mechanisms, cost-sharing-mechanism, moulin-mechanism, vcg-mechanism]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.3.5 (examples, with the public project whose payments do not cover the cost) and Section 9.5.5 (uniqueness of prices and its corollaries)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 10.3 (budget balance as a property of quasilinear mechanisms) and Section 10.4.4 (VCG and weak budget balance)
  - book: "Jerry Green and Jean-Jacques Laffont, Incentives in Public Decision-Making, North-Holland, 1979 (Studies in Public Economics 1)"
    locator: the impossibility of strong budget balance for Groves mechanisms
  - paper: doi:10.2307/1912822
    title: "Mark Walker, On the nonexistence of a dominant strategy mechanism for making optimal public decisions, Econometrica 48(6) (1980), 1521-1540"
    locator: no dominant-strategy mechanism for public decisions is both efficient and budget balanced
  - paper: "Leonid Hurwicz and Mark Walker, On the generic nonoptimality of dominant-strategy allocation mechanisms, a general theorem that includes pure exchange economies, Econometrica 58(3) (1990), 683-704"
    locator: the general form of the impossibility of efficient, budget-balanced dominant-strategy mechanisms
  - paper: doi:10.1145/1160633.1160790
    title: "Ruggiero Cavallo, Optimal decision-making with minimal waste, strategyproof redistribution of VCG payments, AAMAS 2006, 882-889"
    locator: the redistribution rebates that return part of the VCG surplus and keep weak budget balance
---

A mechanism with money is budget balanced when the payments of the agents add up to 0, so no money enters or leaves the system. Weak budget balance asks only that the sum is at least 0, so the mechanism never needs outside money to run. It differs from [individual rationality](/individual-rationality/), the condition it is most often paired with: budget balance is a condition on the sum of the payments, while individual rationality is a condition on each agent's utility. Together with efficiency and incentive compatibility, the two conditions lead to the main impossibility results of mechanism design.

## Definition

Let $(x, p)$ be a [direct revelation mechanism](/direct-revelation-mechanism/), with $p_i(b)$ paid by agent $i$ and a negative $p_i(b)$ paid to it. Its revenue at the reports $b$ is $\sum_i p_i(b)$.

- **Strong budget balance.** $\sum_i p_i(b) = 0$ for every profile $b$.
- **Weak budget balance.** $\sum_i p_i(b) \ge 0$ for every profile $b$. The mechanism never runs a deficit, and a surplus leaves the agents.
- **Ex ante budget balance.** With a prior on the types, $\mathbb{E}[\sum_i p_i] = 0$, or $\ge 0$ in the weak form. The budget balances on average, so a planner who runs the mechanism many times needs no outside money in the long run.

When the mechanism has a cost $C(x)$, as in cost sharing, strong budget balance means $\sum_i p_i = C(x)$. A cost-sharing method is *$\beta$-budget balanced*, for $\beta \ge 1$, when $C(x) \le \sum_i p_i \le \beta C(x)$ ([cost-sharing mechanism](/cost-sharing-mechanism/)). Some papers use the reverse fraction, so check the form.

A seller or planner can also be counted as one more agent. Then the revenue of an auction is a transfer to the seller, and a single-item auction is strongly budget balanced in the economy that includes the seller.

## Examples and non-examples

- **The Vickrey auction is weakly, not strongly, budget balanced.** With values $(10, 7, 3)$ the payments are $(7, 0, 0)$. The sum is 7. If the agents were only the three bidders, the 7 would have to leave the group.
- **Groves payments with $h_i = 0$ run a deficit.** Each agent is paid the reported welfare of the others. With the same values, the payments are $(0, -10, -10)$, so the mechanism pays out 20.
- **A public project that VCG cannot pay for.** Three citizens value a bridge of cost 300 at 150, 120 and 60, and the planner takes part as an agent with value $-300$ for building. VCG builds and the citizens pay 120, 90 and 30. The total is 240, so the planner runs a deficit of 60 (Nisan, Section 9.3.5).
- **Equal cost shares are budget balanced but not efficient.** Build the bridge if every citizen reports a value of at least $300 / 3 = 100$, and then charge each 100. The payments cover the cost exactly, and no citizen gains by a lie. With the values above the bridge is not built, since 60 is below 100, but the total value 330 is above the cost.
- **Redistribution reduces the surplus.** In the single-item case with $(10, 7, 3)$, the Cavallo rebates give each agent one $n$-th of the smallest VCG revenue that its own report can produce. The rebates are 1, 1 and $7/3$, so the net revenue is $7 - 13/3 = 8/3$. The mechanism stays DSIC and weakly budget balanced (Cavallo 2006).
- **The AGV mechanism is strongly budget balanced.** It is efficient and BIC with independent types, but not DSIC and not always IR ([AGV mechanism](/agv-mechanism/)).

## Related definitions

- **Impossibility with dominant strategies.** No [Groves mechanism](/groves-mechanisms/) is strongly budget balanced when the valuations are unrestricted and there are at least two agents (Green and Laffont 1979; Walker 1980; Hurwicz and Walker 1990). Since the Groves mechanisms are the only efficient DSIC mechanisms on that domain, no efficient DSIC mechanism is strongly budget balanced there ([Green-Laffont theorem](/green-laffont-theorem/)).
- **Impossibility with interim IR.** For bilateral trade with independent private values and overlapping supports, no mechanism is efficient, BIC, interim IR and weakly budget balanced ([Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/)).
- **Individual rationality.** Each agent's utility is at least its outside option ([individual rationality](/individual-rationality/)). The [Clarke pivot rule](/clarke-pivot-rule/) gives IR and weak budget balance for nonnegative valuations.
- **Cost sharing.** Cross-monotonic cost shares give strongly budget-balanced, group-strategyproof mechanisms that are not efficient ([Moulin mechanism](/moulin-mechanism/)).

## References
