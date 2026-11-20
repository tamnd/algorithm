---
tag: KK2YJY
kind: algorithm
slug: method-of-equal-shares
name: Method of equal shares
aliases:
- Rule X
area: algorithmic-game-theory/social-choice-and-voting
level: research
summary: Gives each voter an equal budget and buys candidates or projects whose supporters can cover the cost at the lowest share each.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates, k: the committee size}
  time: {worst: O(k m n log n)}
  space: {extra: O(m n)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 2020
  people: [Dominik Peters, Piotr Skowron, Grzegorz Pierczynski]
  note: "Peters and Skowron introduced the rule as Rule X in 2020. With Pierczynski they extended it to participatory budgeting, and cities first used it in 2023."
prereqs: [approval-voting, justified-representation, phragmen-sequential-method]
see_also: [participatory-budgeting, phragmen-sequential-method, proportional-approval-voting, justified-representation, dhondt-method, knapsack-problem, core-of-a-cooperative-game, chamberlin-courant-rule]
sources:
  - paper: doi:10.1145/3391403.3399465
    title: "Dominik Peters and Piotr Skowron, Proportionality and the limits of welfarism, Proceedings of EC 2020, 793-794"
    locator: "the introduction of Rule X, as cited by Lackner and Skowron for Rule 11 and Table 4.1"
  - paper: "Dominik Peters, Grzegorz Pierczynski and Piotr Skowron, Proportional participatory budgeting with additive utilities, Advances in Neural Information Processing Systems 34 (NeurIPS 2021), 12726-12737"
    locator: the extension of the rule to participatory budgeting with costs and additive utilities
  - paper: arxiv:2007.01795
    title: "Martin Lackner and Piotr Skowron, Multi-Winner Voting with Approval Preferences, arXiv 2007.01795, version of August 2022 (published by Springer, 2023)"
    locator: "Rule 11, Examples 2.11 and 2.12, Table 3.1, Table 4.1 and Section 4.4"
  - paper: "Dominik Peters and others, equalshares.net, election reports for Wieliczka (2023), Aarau (2023) and Swiecie (vote of September 2023), read in November 2026"
    locator: "the pages elections/zielony-milion, elections/aarau-2023 and elections/swiecie-2024"
---

The method of equal shares (MES) is a voting rule for [approval ballots](/approval-voting/) that elects a committee or chooses projects for a [participatory budget](/participatory-budgeting/). Each voter gets an equal part of the budget, and the rule buys candidates one at a time, each time the candidate whose supporters can pay for it with the smallest equal share each. It runs in polynomial time and satisfies [extended justified representation](/justified-representation/). [Proportional approval voting](/proportional-approval-voting/) also satisfies this axiom, but it is NP-hard to compute.

## In plain words

Every voter gets the same amount of money at the start. A candidate has a price, and only the voters who want it may pay. For each candidate, ask how much each supporter must pay if they split the price as equally as they can, and voters who have less money pay all that they have. Buy the candidate for which this share is smallest, take the money from its supporters, and ask again. Stop when no candidate can be paid for. A large group has more money, so it buys more, but every purchase costs it money, so a small group keeps money for its own choices. If seats are still empty at the end, a second rule fills them.

## The problem

The input is an approval profile, that is, for each voter $i = 1, \ldots, n$ a set $A_i$ of approved candidates among $0, \ldots, m - 1$, and a committee size $k$ with $0 \le k \le m$. For a candidate $c$, $N(c)$ is the set of voters who approve $c$. The output is a committee $W$ of $k$ candidates.

In the budgeting form, candidate $c$ is a project with a cost $\mathrm{cost}(c) > 0$, and the total budget is $B$. The committee form is the case where every cost is $1$ and $B = k$. In the budgeting form, the rule stops after phase 1 and returns the bought projects.

Ties go to the smallest candidate index. In the completion, a candidate that no voter approves is added only when no supported candidate is left, smallest index first.

## The algorithm

```pseudo id=main
EQUAL-SHARES(A_1, ..., A_n, m, k)
L1  x_i ← k/n for every voter i; W ← empty list
L2  repeat
L3      for each c ∉ W: ρ(c) ← the least ρ with Σ_{i ∈ N(c)} min(ρ, x_i) = 1, undefined if Σ_{i ∈ N(c)} x_i < 1
L4      c* ← the c with the least defined ρ(c), ties to the smallest index
L5      if no ρ(c) is defined then leave the loop
L6      append c* to W
L7      x_i ← x_i - min(ρ(c*), x_i) for every i ∈ N(c*)
L8  y_i ← -x_i for every voter i
L9  while |W| < k: add a candidate by sequential Phragmen started from the loads y
L10 return W
```

Lines L1 to L7 are phase 1. To compute $\rho(c)$ on line L3, sort the budgets of the supporters in increasing order. The voters with small budgets pay all they have, and the others pay an equal share of what remains. In the budgeting form, line L1 gives each voter $B/n$, and the $1$ on line L3 becomes $\mathrm{cost}(c)$.

Lines L8 and L9 are the completion of Lackner and Skowron (Rule 11). Phase 1 can leave seats empty, and the completion runs [sequential Phragmen](/phragmen-sequential-method/) where each voter starts with the load $-x_i$, so that unspent money counts as a credit.

## Example

This is Example 2.12 of Lackner and Skowron. The candidates are $a, b, c, d$, $k = 3$, and eight voters have the ballots

$$3 \times \{c, d\}, \quad 2 \times \{a, b\}, \quad 2 \times \{a, c\}, \quad 1 \times \{b, d\}.$$

Each voter starts with $3/8$.

| round | $\rho(a)$ | $\rho(b)$ | $\rho(c)$ | $\rho(d)$ | bought |
|---|---|---|---|---|---|
| 1 | $1/4$ | $1/3$ | $1/5$ | $1/4$ | $c$ |
| 2 | $13/40$ | $1/3$ | | none | $a$ |
| 3 | | none | | none | stop |

In round 1 the five supporters of $c$ pay $1/5$ each and keep $7/40$. In round 2 the two $\{a, c\}$ voters have only $7/40$ each, so they pay all of it, and the two $\{a, b\}$ voters pay $(1 - 7/20)/2 = 13/40$ each. The supporters of $d$ have $3 \cdot 7/40 + 3/8 = 9/10 < 1$ in total, so $d$ is not affordable. In round 3 neither $b$ nor $d$ is affordable, and phase 1 ends with $\{c, a\}$.

The completion starts from the loads $-7/40$ for the $\{c, d\}$ voters, $-1/20$ for the $\{a, b\}$ voters, $0$ for the $\{a, c\}$ voters and $-3/8$ for the $\{b, d\}$ voter. Then $d$ needs the time $(1 - 3 \cdot 7/40 - 3/8)/4 = 1/40$ and $b$ needs $(1 - 2/20 - 3/8)/3 = 7/40$, so $d$ is added. The committee is $\{a, c, d\}$. Sequential Phragmen elects $\{b, c, d\}$ on the same profile.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The sorted computation on line L3 gives the least price exactly, no voter ever pays more than it has, and the payments for each bought candidate add up to its cost. So phase 1 buys at most $k$ candidates, and the bought prices never decrease.

For EJR, suppose a group $S$ of $s \ge \ell n / k$ voters approves $\ell$ common candidates, but each voter of $S$ approves at most $\ell - 1$ members bought in phase 1. Some common candidate $c$ is never bought. Look at the first round that buys at a price above $1/s$ or buys nothing. Before it, each voter of $S$ paid at most $1/s$ for each of at most $\ell - 1$ members, so each still has at least $k/n - (\ell - 1)/s \ge 1/s$. Then the voters of $S$ alone can pay for $c$ at the price $1/s$, which contradicts the choice of the round. The completion only adds members, so EJR still holds.

## Complexity

Line L3 sorts the budgets of $|N(c)|$ supporters for each candidate, $O(mn \log n)$ arithmetic operations in each round. Phase 1 has at most $k + 1$ rounds, and the completion takes $O(kmn)$, so the rule takes $O(kmn \log n)$ operations in the [word RAM](/word-ram/) model and $O(mn)$ space for the lists of supporters. In the budgeting form, phase 1 has at most $m + 1$ rounds. With exact fractions the numbers can grow, so the bit cost is larger than the count of operations.

## Properties

- **Extended justified representation.** The committee after phase 1 already satisfies EJR, so it also satisfies PJR and JR (Lackner and Skowron, Table 4.1).
- **Priceable and laminar proportional** (Lackner and Skowron, Table 4.1).
- **D'Hondt on party lists.** With disjoint party lists, the rule gives the seat numbers of the [D'Hondt method](/dhondt-method/) (Lackner and Skowron, Table 4.1).
- **Not committee monotone, not Pareto efficient and not consistent** (Lackner and Skowron, Table 3.1).
- **Not in the core.** Some profiles have a group that could buy a better committee with its own share of the seats (Lackner and Skowron, Section 4.4, citing Peters and Skowron). Whether every approval profile has a committee in the [core](/core-of-a-cooperative-game/) is open as of August 2022 (same section).
- **Anonymous.** The resolute rule with fixed tie-breaking is not neutral; the set of committees over all tie-breaking orders is.

## Variants and improvements

- **Additive utilities.** If voter $i$ has utility $u_i(c)$ for project $c$, voter $i$ pays $\min(x_i, \rho \, u_i(c))$, and $\rho$ is a price per unit of utility. Peters, Pierczynski and Skowron (2021) study this form for participatory budgeting.
- **Other completions.** Phase 1 often leaves money unspent. Lackner and Skowron complete by sequential Phragmen. Another way is to raise the starting budget and run phase 1 again until the outcome is full. The choice changes the outcome but not EJR, because the completion only adds members.
- **Sequential Phragmen.** Voters earn money at a steady rate instead of getting it all at the start. This rule is committee monotone but satisfies only PJR.

## When to use it

Use it to elect a committee from approval ballots when extended justified representation is required and the committee must be computed in polynomial time, or to choose projects for a participatory budget where every group should get a share of the money in proportion to its size. If the committee must grow consistently with $k$, use sequential Phragmen. If total approval matters more than fairness to groups, the usual greedy rule, which funds the most approved projects first while money is left, or a [knapsack](/knapsack-problem/) solution is simpler.

## Pitfalls

- **Phase 1 can be short.** In Example 2.11 of Lackner and Skowron, with $k = 4$, phase 1 buys only one candidate. Always state the completion.
- **Paying more than the budget.** A voter with less than $\rho$ pays only what it has. Charging $\rho$ to every supporter can make budgets negative and gives a different rule.
- **Floating point.** Prices often tie in small instances, and rounding can change the order. Use exact fractions and state the tie-breaking rule.
- **Expecting committee monotonicity.** The committee for $k + 1$ seats can drop a member of the committee for $k$ seats, because every budget changes with $k$.

## Implementations

## History

Peters and Skowron introduced the rule as Rule X at EC 2020, in a study of proportional rules beyond welfare maximization, and showed that it satisfies EJR in polynomial time. Peters, Pierczynski and Skowron (NeurIPS 2021) extended it to participatory budgeting with additive utilities, and the rule became known as the method of equal shares. In 2023 the city of Wieliczka in Poland used it for its participatory budget, the first use in a real election. The same year Aarau in Switzerland used it for its first participatory budget, and Swiecie in Poland used it in a vote held in September 2023 for its 2024 budget.

## References
