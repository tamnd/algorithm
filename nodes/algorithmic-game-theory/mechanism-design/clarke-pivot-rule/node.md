---
tag: 7E94E1
kind: technique
slug: clarke-pivot-rule
name: Clarke pivot rule
aliases:
- Clarke tax
- pivot mechanism
area: algorithmic-game-theory/mechanism-design
level: core
summary: The choice of the h_i term in Groves payments as the best welfare of the others without agent i. It gives no positive transfers, and individual rationality for nonnegative valuations.
prereqs: [groves-mechanisms]
see_also: [vcg-mechanism, groves-mechanisms, individual-rationality, budget-balance, vickrey-auction, shortest-path, green-laffont-theorem]
sources:
  - paper: doi:10.1007/BF01726210
    title: "Edward H. Clarke, Multipart pricing of public goods, Public Choice 11 (1971), 17-33"
    locator: the pivot tax for a public decision, charged only to agents whose report changes the decision
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Section 9.3.4 (the Clarke pivot rule, with the lemma that it gives no positive transfers and individual rationality for nonnegative valuations) and Section 9.3.5 (examples)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Definition 10.4.4 (the Clarke tax) and Sections 10.4.2 to 10.4.4 (VCG, individual rationality and weak budget balance)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 7 (the VCG payments as externalities)
---

The Clarke pivot rule is the standard way to choose the free term $h_i$ in the payments of a [Groves mechanism](/groves-mechanisms/): set $h_i(b_{-i})$ to the best welfare that the other agents could reach if agent $i$ were absent. It differs from its two close pages in scope. The [Groves mechanisms](/groves-mechanisms/) allow any $h_i$, the Clarke pivot rule is this one choice, and the [VCG mechanism](/vcg-mechanism/) is the Groves mechanism that uses it. The choice keeps DSIC and efficiency, and adds two properties: no agent is ever paid, and with nonnegative valuations no truthful agent ends with negative utility.

## In plain words

In a Groves mechanism each agent is paid the value that the others get from the choice, and then charged an amount that its own report cannot change. The pivot rule picks that charge with one question: how well off would the others be if this agent were not here? The agent pays the difference between that and what the others actually get. An agent that does not change the choice pays nothing. An agent that tips the choice its way, the pivotal agent, pays for exactly the harm it does to the others. Nobody is ever paid, and when nobody has negative values, nobody loses by taking part.

## When it applies

- The agents have [quasilinear utilities](/quasilinear-utility/), and the mechanism chooses an outcome of maximum reported welfare, so it is a Groves mechanism.
- For each agent $i$ the best welfare of the others, $\max_{o} \sum_{j \ne i} b_j(o)$, can be computed exactly. This is one more optimization for each agent, $n + 1$ in total with the one for the outcome.
- The goal includes no positive transfers ($p_i \ge 0$) or [individual rationality](/individual-rationality/). The rule gives IR when every valuation is nonnegative, as in auctions, and it gives no positive transfers for every valuation.
- When outcomes that need agent $i$ are not available without it, as with paths that use an edge owned by $i$, replace the maximum over $O$ by the maximum over the outcomes that remain feasible without $i$. See "Variations".

## The template

Given reports $b_1, \ldots, b_n$ and the outcome $x \in \arg\max_o \sum_j b_j(o)$:

1. For each agent $i$, compute $W_{-i} = \max_{o \in O} \sum_{j \ne i} b_j(o)$, the best welfare of the others.
2. Set $h_i(b_{-i}) = W_{-i}$. It depends only on $b_{-i}$, so the mechanism stays a Groves mechanism and DSIC.
3. Charge $p_i = W_{-i} - \sum_{j \ne i} b_j(x)$, the externality of agent $i$.

The two properties follow in one line each.

- **No positive transfers.** $W_{-i}$ is a maximum over all outcomes, and $x$ is one of them, so $W_{-i} \ge \sum_{j \ne i} b_j(x)$ and $p_i \ge 0$.
- **Individual rationality for nonnegative valuations.** Let $z$ attain $W_{-i}$. For a truthful agent, $u_i = v_i(x) + \sum_{j \ne i} v_j(x) - \sum_{j \ne i} v_j(z)$. The first two terms are the welfare of $x$, which is at least the welfare of $z$, so $u_i \ge v_i(z) \ge 0$.
- **Pivotal agents only.** If $x$ also maximizes the welfare of the others, then $p_i = 0$. Only an agent whose presence changes the best choice pays.

## Classic examples

- **One item: the Vickrey auction.** With values $(10, 7, 3)$, $W_{-1} = 7$ and the others get 0 at $x$, so bidder 1 pays 7. For a loser $j$, $W_{-j} = 10$ and the others get 10, so it pays 0 ([Vickrey auction](/vickrey-auction/)).
- **$k$ identical items, unit demand.** The $k$ highest bidders win, and each pays the $(k + 1)$-st highest bid.
- **Combinatorial auction.** Bidder 1 values $\{A, B\}$ at 10, bidder 2 values $A$ at 6, and bidder 3 values $B$ at 7. Bidders 2 and 3 win. $W_{-2} = 10$ (both items to bidder 1) and the others get 7 at $x$, so bidder 2 pays 3. In the same way bidder 3 pays 4, and bidder 1 pays 0.
- **Public project (Clarke 1971).** Citizens with values 150, 120 and 60 for a bridge of cost 300, and the planner as an agent with value $-300$ for building. The bridge is built. Without the citizen of value 150, the rest have $120 + 60 - 300 = -120$ for building, so their best choice is not to build, with welfare 0, and they get $-120$ at $x$. So that citizen pays 120. In the same way the others pay 90 and 30. Each payment is the cost minus the values of the other citizens, when that is positive.

## Variations

- **Outcomes feasible without $i$.** Take $W_{-i} = \max_{o \in O_{-i}} \sum_{j \ne i} b_j(o)$ over the set $O_{-i}$ of outcomes that do not use agent $i$. In a procurement of a [shortest path](/shortest-path/) with edges owned by agents, the owner of an edge $e$ on the chosen path is paid $d(G - e) - (d(G) - c_e)$, where $d$ is the length of a shortest path and $c_e$ the reported cost of $e$ (Nisan, Section 9.3.5). Here the agents are paid, so there are positive transfers, but IR holds.
- **Cost shares plus a tax.** Clarke's original form assigns each citizen a fixed share of the cost and applies the pivot rule to the values net of the shares.
- **Redistribution.** Subtract from $W_{-i}$ a rebate that depends only on $b_{-i}$, to return part of the revenue while keeping DSIC. The rebate must be small enough that the sum of the payments stays at least 0 (Cavallo 2006, see [Groves mechanisms](/groves-mechanisms/)).
- **Over a fixed range.** The same rule over a fixed subset of outcomes gives the payments of a [maximal-in-range mechanism](/maximal-in-range-mechanism/).

## Pitfalls

- **Negative valuations break IR.** For a project, let agent 1 value "build" at 5 and agent 2 value it at $-2$. The project is built, agent 2 is not pivotal and pays 0, so its utility is $-2$. No positive transfers still holds.
- **The surplus cannot go back to the agents.** The rule is weakly but not strongly [budget balanced](/budget-balance/). Splitting the revenue equally among the agents breaks DSIC: in the single-item case with $(10, 7, 3)$, bidder 2 would get one third of a revenue equal to its own bid, so a higher losing bid pays it more.
- **An approximate $W_{-i}$.** If $W_{-i}$ comes from a heuristic, DSIC is kept, because $h_i$ still ignores the report of agent $i$. But $W_{-i}$ can fall below the welfare of the others at $x$, and then the payment is negative, so the guarantee of no positive transfers is lost. An approximate $x$ is worse, because it breaks DSIC.
- **Low revenue and collusion.** Only pivotal agents pay, so the revenue can be 0 even when the items are in demand, and losing agents can gain by joint overbids. See the pitfalls of the [VCG mechanism](/vcg-mechanism/).

## Exercises

1. In the combinatorial auction above, compute the payments with all three bidders and check that the revenue is 7, less than the bid of 10 of bidder 1. Explain why this is outside the core.
2. Show that with $k$ identical items and unit demand, the pivot rule charges each winner the $(k + 1)$-st highest bid.
3. Let the zero valuation be one of the possible types of agent $i$. Show that every ex post IR Groves mechanism has $h_i(b_{-i}) \le W_{-i}$, so the Clarke pivot rule gives the largest payments among the IR Groves mechanisms. (Hint: an agent with the zero valuation has utility $\sum_{j \ne i} b_j(x) - h_i(b_{-i})$, and $x$ then maximizes the welfare of the others.)
4. For a binary public project with values $v_1, \ldots, v_n$ of any sign and no cost, show that agent $i$ pays $|\sum_{j \ne i} v_j|$ if the sign of $\sum_{j \ne i} v_j$ differs from the sign of $\sum_j v_j$, and 0 otherwise (with a fixed rule for 0).
5. Give an example with three agents and negative values in which two agents are pivotal and one is not.

## References
