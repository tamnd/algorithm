---
tag: KNJ3AG
kind: algorithm
slug: agv-mechanism
name: AGV mechanism
aliases:
- d'Aspremont-Gerard-Varet mechanism
- expected externality mechanism
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: Picks the efficient outcome and pays each agent the expected welfare of the others given its report. With independent types it is BIC and exactly budget balanced, but not always IR.
model: word-ram
complexity:
  vars: {n: the number of agents, k: the number of types of each agent, m: the number of outcomes}
  time: {worst: O((m + n) n k^n)}
  space: {extra: O(n k)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1979
  people: [Claude d'Aspremont, Louis-Andre Gerard-Varet, Kenneth J. Arrow]
  note: d'Aspremont and Gerard-Varet, and Arrow independently, gave in 1979 an efficient mechanism with balanced transfers for public decisions, incentive compatible in Bayes-Nash equilibrium.
prereqs: [quasilinear-utility, bayesian-incentive-compatibility, groves-mechanisms]
see_also: [vcg-mechanism, budget-balance, individual-rationality, myerson-satterthwaite-theorem, green-laffont-theorem, cremer-mclean-theorem, bayes-nash-equilibrium, automated-mechanism-design]
sources:
  - paper: doi:10.1016/0047-2727(79)90043-4
    title: "Claude d'Aspremont and Louis-Andre Gerard-Varet, Incentives and incomplete information, Journal of Public Economics 11(1) (1979), 25-45"
    locator: the expected externality transfers for public decisions, with independent beliefs, and the proof that they balance the budget and make truth a Bayes-Nash equilibrium
  - paper: doi:10.1016/B978-0-12-118850-4.50007-2
    title: "Kenneth J. Arrow, The property rights doctrine and demand revelation under incomplete information, in Michael J. Boskin (ed.), Economics and Human Welfare, Academic Press (1979), 23-39"
    locator: the same balanced mechanism, found independently
  - book: isbn:9780195073409
    title: Andreu Mas-Colell, Michael D. Whinston and Jerry R. Green, Microeconomic Theory, Oxford University Press, 1995
    locator: Chapter 23, Section 23.D (Bayesian implementation and the expected externality mechanism) and Section 23.E (participation constraints)
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 5 (mechanism design, efficient mechanisms and budget balance)
---

The AGV mechanism, after d'Aspremont and Gerard-Varet, picks the outcome of largest reported welfare and pays each agent the expected welfare of the other agents, where the expectation is over the others' types and the agent's own report is held fixed. The money for these payments is raised from the other agents, so the payments add up to exactly zero at every profile. With independent types, truth telling is a Bayes-Nash equilibrium, so the mechanism is [Bayesian incentive compatible](/bayesian-incentive-compatibility/) (BIC). It differs from the [VCG mechanism](/vcg-mechanism/) in what it gives up: VCG is truthful in dominant strategies and runs a surplus or a deficit, while AGV balances the budget but is truthful only in expectation and can leave an agent with negative expected utility.

## In plain words

A group must make one shared decision, such as building a road, and each member privately knows what the road is worth to them. No money may come in from outside or go out. Each member states a value, and the mechanism picks the decision that is best for the stated values. It then pays each member the average benefit that the others would get, guessed from what the member said and from what is known about the others in general. Each member pays an equal share of the amounts given to the others. A member who is paid for the others' benefit wants the group to choose well, and so tells the truth, at least when the others do. The payments cancel out, but a member with a low value can end up worse off than if it had stayed out.

## The problem

There are $n \ge 2$ agents and a finite set $O$ of $m$ outcomes. Agent $i$ has a private type $t_i$ from a finite set $T_i$, drawn from a prior $f_i$, and the types of different agents are independent. The value of agent $i$ of type $t_i$ for outcome $o$ is $v_i(t_i, o)$, which may be negative. Utility is [quasilinear](/quasilinear-utility/): if the outcome is $o$ and agent $i$ pays $p_i$, its utility is $v_i(t_i, o) - p_i$. A negative $p_i$ is a transfer to the agent.

The goal is a direct mechanism that maps reports $b = (b_1, \ldots, b_n)$ to an outcome and payments such that:

- the outcome maximizes the reported welfare $W(b, o) = \sum_j v_j(b_j, o)$ (efficiency),
- $\sum_i p_i(b) = 0$ at every profile $b$ ([strong budget balance](/budget-balance/)),
- truth telling is a [Bayes-Nash equilibrium](/bayes-nash-equilibrium/) (BIC).

By the [Green-Laffont theorem](/green-laffont-theorem/), no mechanism has all three properties with dominant-strategy truthfulness on a rich domain of valuations, so BIC is the price paid for the balanced budget.

## The algorithm

```pseudo id=main
AGV(T, f, O, v, b)
L1  h_i(t) ← 0 for each agent i and each type t in T_i
L2  for each type profile t in T_1 × ... × T_n:
L3      o ← the first outcome in O that maximizes Σ_j v_j(t_j, o)
L4      for each agent i:
L5          h_i(t_i) ← h_i(t_i) + Pr[t_-i] · Σ_{j ≠ i} v_j(t_j, o)
L6  o* ← the first outcome in O that maximizes Σ_j v_j(b_j, o)
L7  for each agent i:
L8      p_i ← (1 / (n - 1)) Σ_{j ≠ i} h_j(b_j) - h_i(b_i)
L9  return o*, p
```

Here $\Pr[t_{-i}] = \prod_{j \ne i} f_j(t_j)$. Lines L1 to L5 depend only on the prior and the valuations, not on the reports, so they can run once before any agent reports. After the loop, $h_i(s)$ is the expected externality term

$$h_i(s) = \mathbb{E}_{t_{-i}}\Big[\sum_{j \ne i} v_j\big(t_j, x^*(s, t_{-i})\big)\Big],$$

the expected welfare of the others when agent $i$ reports $s$ and the others tell the truth, where $x^*$ is the rule of line L3. Line L8 gives agent $i$ the amount $h_i(b_i)$ and charges it a $1/(n-1)$ share of what the others get. Lines L3 and L6 must break ties in the same way, here by the order of $O$; the proof below needs $h$ to be computed with the rule that is actually applied.

## Example

Three agents decide whether to build a project that costs 60. Each pays a share of 20 if it is built, so the value of agent $i$ is $v_i(t_i, \text{build}) = t_i - 20$ and $v_i(t_i, \text{no}) = 0$. Each type is 10 or 35 with probability 1/2, independently. The project has positive welfare exactly when at least two agents have type 35, because $35 + 35 + 10 = 80 > 60$ and $35 + 10 + 10 = 55 < 60$.

Lines L1 to L5 give the same table for every agent. For type 10, the others' welfare is positive only when both others have type 35: then it is $15 + 15 = 30$, so $h(10) = 30/4 = 15/2$. For type 35, the project is built when at least one other has type 35, and the others' welfare is $15 - 10 = 5$, $5$ or $30$, so $h(35) = (0 + 5 + 5 + 30)/4 = 10$.

| reports $b$ | outcome | $p_1, p_2, p_3$ | utilities |
|---|---|---|---|
| 10, 10, 10 | no | 0, 0, 0 | 0, 0, 0 |
| 10, 10, 35 | no | 5/4, 5/4, -5/2 | -5/4, -5/4, 5/2 |
| 10, 35, 35 | build | 5/2, -5/4, -5/4 | -25/2, 65/4, 65/4 |
| 35, 35, 35 | build | 0, 0, 0 | 15, 15, 15 |

For $b = (10, 35, 35)$, line L8 gives agent 1 the payment $\frac{1}{2}(10 + 10) - 15/2 = 5/2$, and agents 2 and 3 each $\frac{1}{2}(15/2 + 10) - 10 = -5/4$. The three payments add up to 0, as in every row. The other four profiles are permutations of these rows.

Averaged over the others' types, an agent of type 35 who tells the truth expects $25/2$, and $5/2$ if it reports 10. An agent of type 10 expects $-15/4$ from the truth and $-25/4$ from the report 35. So truth is the best report for both types, but the low type expects a loss. The total of the expected utilities, $3 \cdot \frac{1}{2}(25/2 - 15/4) = 105/8$, equals the expected welfare of the efficient decision, as budget balance requires. The tests check all these numbers in exact arithmetic.

## Correctness

The full proof is in proofs/correctness.md. Efficiency holds because line L6 maximizes the reported welfare. Budget balance holds because in $\sum_i \frac{1}{n-1}\sum_{j \ne i} h_j(b_j)$ each $h_j(b_j)$ appears $n - 1$ times, so the sum is $\sum_j h_j(b_j)$ and cancels the second term.

For BIC, fix agent $i$ with true type $t_i$ and let the others tell the truth. Report $r$ gives the expected utility

$$\mathbb{E}_{t_{-i}}\big[v_i(t_i, x^*(r, t_{-i}))\big] + h_i(r) - C_i = \mathbb{E}_{t_{-i}}\Big[\sum_j v_j\big(t_j, x^*(r, t_{-i})\big)\Big] - C_i,$$

where $C_i = \frac{1}{n-1}\sum_{j \ne i}\mathbb{E}[h_j(t_j)]$ does not depend on $r$. Independence is used here: the distribution of $t_{-i}$ is the same whatever $t_i$ is, so the $h_i(r)$ computed from the prior is the expectation that agent $i$ itself forms. For each $t_{-i}$ the true efficient outcome $x^*(t_i, t_{-i})$ gives the largest true welfare, so $r = t_i$ maximizes the expectation. This is the Groves idea of paying each agent the others' welfare, applied in expectation; because $h_i$ depends only on agent $i$'s own report, the payments can be recycled among the agents.

## Complexity

The table $h$ needs one pass over the $k^n$ type profiles when each agent has $k$ types. Each profile costs $O(n m)$ for line L3 and $O(n)$ per agent for lines L4 and L5 when $\Pr[t_{-i}]$ is a plain product, which is what the code does; the total is $O((m + n) n k^n)$ time and $O(n k)$ extra space for the table. Prefix and suffix products of the probabilities bring lines L4 and L5 to $O(n)$ per profile. After the table is built, each run of lines L6 to L9 costs $O(n m)$. The exponential term is the size of the type space, which the input in this form already lists through the prior; for a continuous prior, $h_i$ is an integral that must be computed or approximated for the given model. All arithmetic is exact in rationals.

## Properties

- **Efficient** at every profile of reports.
- **Strongly budget balanced** at every profile: no money comes in or goes out, even when agents lie.
- **BIC with independent types.** Truth is a Bayes-Nash equilibrium. It is not a dominant strategy: at $(10, 35, 35)$ in the example, agent 1 of type 10 gets $-25/2$ from the truth and $-10$ from the report 35, so the lie gains $5/2$ ex post.
- **Not individually rational in general.** In the example the type 10 agent expects $-15/4$, so interim IR fails, and ex post it can lose $25/2$. Shifting the payments by constants $K_i$ keeps BIC and keeps budget balance only when $\sum_i K_i = 0$. Here each agent would need $K_i \le -15/4$ (a transfer of at least $15/4$ to it), which does not sum to zero, so no shift of AGV is interim IR on this instance.
- **Payments depend only on single reports.** $p_i$ is a sum of functions of one report each, which is why the budget can balance.

## Variants and improvements

- **Arrow's version.** Arrow found the same transfers independently in 1979 for public decisions; textbooks call both the expected externality mechanism.
- **Two agents.** With $n = 2$, line L8 reads $p_1 = h_2(b_2) - h_1(b_1)$: each agent pays the other's expected externality term and receives its own.
- **Unequal sharing.** Any rule that collects the amounts $h_j(b_j)$ from agents other than $j$ in fixed shares works. The $1/(n-1)$ split is the symmetric choice.
- **Participation.** To get interim IR as well, one can shift the payments by constants when the expected welfare is large enough, or accept a subsidy. In [bilateral trade](/myerson-satterthwaite-theorem/) no efficient BIC mechanism is both budget balanced and interim IR, so some loss is unavoidable there; [automated mechanism design](/automated-mechanism-design/) can find the best compromise for a given prior by linear programming.
- **Correlated types.** If the types are correlated, $h_i$ computed from the prior is not the agent's own conditional expectation and BIC can fail. Correlation also helps, though: side bets on the others' reports, as in the [Cremer-McLean theorem](/cremer-mclean-theorem/), can give efficiency and balance with weaker trade-offs.

## When to use it

Use AGV when the decision must be efficient, no outside money is available, the prior is common knowledge and independent, and agents cannot opt out after they learn their types (or the expected gains are large enough that no type wants to). Examples are internal allocation within a firm and committee decisions with compulsory participation. If agents can walk away, check interim IR first. If the prior is not trusted, use a dominant-strategy mechanism such as [VCG](/vcg-mechanism/) and accept the budget imbalance.

## Pitfalls

- **Treating BIC as DSIC.** The equilibrium depends on everyone else reporting truthfully and on the prior being right. With a wrong prior the payments $h_i$ are computed for the wrong distribution and truth need not be optimal.
- **Ignoring participation.** A low type expects a loss, as the example shows. In bilateral trade with seller cost in $\{0, 2\}$ and buyer value in $\{1, 3\}$, each with probability 1/2, AGV gives the buyer of value 1 an expected utility of $-5/4$.
- **Different tie rules.** If the table $h$ uses one tie rule and the outcome another, BIC can fail at tie profiles. Use one rule in both lines L3 and L6.
- **Correlated priors.** The proof needs independence; with correlation, recompute the incentives before you use the mechanism.
- **One agent.** The formula divides by $n - 1$. With one agent there is no one to balance against, and the code raises an error.

## Implementations

## History

d'Aspremont and Gerard-Varet (1979) and Arrow (1979) found, independently, that the incentive problem of public decisions becomes easier when one asks only for truth telling in Bayes-Nash equilibrium. Groves and Clarke had shown earlier in the decade that dominant-strategy truthful efficient mechanisms exist, and Green and Laffont showed that such mechanisms cannot balance the budget. The expected externality payments get around this by paying each agent a function of its own report only. Myerson and Satterthwaite (1983) then showed that the remaining weakness, the lack of individual rationality, cannot be removed in bilateral trade.

## References
