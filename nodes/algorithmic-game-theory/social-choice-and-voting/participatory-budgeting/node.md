---
tag: MKR4Q9
kind: problem
slug: participatory-budgeting
name: Participatory budgeting
aliases:
- PB
area: algorithmic-game-theory/social-choice-and-voting
level: research
summary: Choose a set of projects within a budget from voters' approvals or rankings so that the outcome is efficient and proportional.
see_also: [method-of-equal-shares, knapsack-problem, approval-voting, justified-representation, phragmen-sequential-method, proportional-approval-voting, core-of-a-cooperative-game, apportionment-problem]
sources:
  - paper: arxiv:2303.00621
    title: "Simon Rey, Felicia Schmidt and Jan Maly, The (computational) social choice take on indivisible participatory budgeting, arXiv 2303.00621, version 9, March 2025"
    locator: "Chapter 1 (Porto Alegre, 1989), Section 2.1 (the standard model), Section 4.1.2 (greedy rules and the rule most used in practice), Section 4.4 (MES needs a completion), Theorems 13, 14 and 16, Section 5.2 (Proposition 33 and the core with approval ballots), Table 7.1"
  - paper: "Dominik Peters, Grzegorz Pierczynski and Piotr Skowron, Proportional participatory budgeting with additive utilities, Advances in Neural Information Processing Systems 34 (NeurIPS 2021), 12726-12737"
    locator: "the method of equal shares for PB, EJR up to one project, the existence of EJR outcomes and the empty core with unit costs, as reported by Rey, Schmidt and Maly"
  - paper: arxiv:2007.01795
    title: "Martin Lackner and Piotr Skowron, Multi-Winner Voting with Approval Preferences, arXiv 2007.01795, version of August 2022 (published by Springer, 2023)"
    locator: "the unit-cost case, multiwinner voting with approval ballots, and Section 4.4 (the open question of the core)"
  - paper: "Dominik Peters and others, equalshares.net, election reports for Wieliczka (2023), Aarau (2023) and Swiecie (vote of September 2023), read in November 2026"
    locator: "the pages elections/zielony-milion, elections/aarau-2023 and elections/swiecie-2024"
---

Participatory budgeting (PB) is the problem of choosing which public projects to fund from a fixed budget, based on the votes of the residents. Each project has a cost, the chosen projects must fit in the budget, and the outcome should be good for the voters as a whole and fair to groups of voters. With equal costs it is the same as electing a committee from [approval ballots](/approval-voting/), and with one voter it is the [knapsack problem](/knapsack-problem/).

## In plain words

A city has a sum of money for local projects, such as a new park, a bike lane or a school library. Residents propose projects, the city works out what each one costs, and then the residents vote, usually by marking the projects they like. The city must choose projects whose total cost fits the money. The simple way is to fund the most popular projects first until the money runs out. But then a group with a small majority can take the whole budget, and a large minority gets nothing. Fair rules give each group of residents a part of the money in proportion to its size.

## Definition

An instance has $m$ projects $0, \ldots, m - 1$ with costs $\mathrm{cost}(p) > 0$, a budget limit $B > 0$ and $n$ voters. In the approval form, voter $i$ submits a set $A_i$ of projects. A *budget allocation* is a set $\pi$ of projects with $\sum_{p \in \pi} \mathrm{cost}(p) \le B$. It is *exhaustive* if no further project fits in the remaining money. A PB rule maps each instance and profile to a budget allocation, or to a set of them if it does not break ties.

The satisfaction of voter $i$ with $\pi$ is often additive, for example the number $|A_i \cap \pi|$ of approved funded projects, or the money $\sum_{p \in A_i \cap \pi} \mathrm{cost}(p)$ spent on them. The goals are of two kinds:

- **Welfare.** Maximize the total satisfaction of all voters over all budget allocations.
- **Proportionality.** A group of voters with a share $s/n$ of the voters can claim the same share $s B / n$ of the money. Extended [justified representation](/justified-representation/) (EJR) and the core make this precise. The core asks that no group $S$ could fund, with $|S| B / n$, a set of projects that every member of $S$ likes more than $\pi$.

The *unit-cost* case, with every cost $1$ and $B = k$, is approval-based multiwinner voting with committee size $k$.

## Variants

- **Ballots.** Besides approval ballots, PB processes use approval ballots with a limit on the number of approvals, knapsack ballots (an approved set that must fit in the budget), rankings and cumulative ballots, where each voter splits a number of points.
- **Satisfaction functions.** Counting approved projects, counting the money spent on them, and functions with diminishing returns give different welfare goals and different proportionality axioms.
- **Divisible projects.** Projects can be funded in part. This is a different model with a continuous outcome.
- **Extended models.** Several resources at once, projects that depend on each other, districts with their own budgets, and minimum or maximum spending per category.

## Examples

Let $B = 10$ and ten voters, so each voter has a share of $1$. Six voters approve $\{a, b\}$ and four approve $\{c, d\}$. The costs are $\mathrm{cost}(a) = 6$, $\mathrm{cost}(b) = 4$, $\mathrm{cost}(c) = 4$ and $\mathrm{cost}(d) = 3$.

- **Greedy by approvals.** Fund projects in decreasing order of approvals while they fit, ties to the smallest index. It funds $a$ and $b$, which use the whole budget. The four voters, $40\%$ of the voters, get nothing.
- **Method of equal shares.** In round 1 the prices per supporter are $1$ for $a$, $2/3$ for $b$, $1$ for $c$ and $3/4$ for $d$, so $b$ is funded and its six supporters keep $1/3$ each. In round 2, $a$ is not affordable ($6 \cdot 1/3 = 2 < 6$), and $d$ is funded at $3/4$ per supporter. In round 3 nothing is affordable. The outcome $\{b, d\}$ costs $7$. The majority spent $4$ of its $6$ and the minority $3$ of its $4$, and no remaining project fits in the $3$ that is left.

The greedy outcome has the larger total satisfaction for both satisfaction functions; the outcome of equal shares is proportional.

## Known algorithms

- **Welfare maximization.** With additive satisfaction this is a knapsack problem, with the cost of $p$ as weight and the total satisfaction from $p$ as value. [Dynamic programming](/knapsack-dynamic-programming/) solves it in [pseudo-polynomial time](/pseudo-polynomial-time/). If each value is the number of approvals, the values are at most $n$, so the dynamic program over values runs in polynomial time.
- **Greedy rules.** The [greedy](/greedy-algorithm/) rule that funds projects by decreasing number of approvals is the rule most used in practice (Rey, Schmidt and Maly, Section 4.1.2). Greedy by value per cost, together with the best single project, approximates the welfare within a factor $2$.
- **[Method of equal shares](/method-of-equal-shares/).** Each voter gets $B/n$, and each round funds the project whose supporters can pay for it with the least price, voters with less money paying all they have. It runs in strongly polynomial time and satisfies EJR up to one project (Peters, Pierczynski and Skowron). It often leaves money unspent, so in practice a completion method follows.
- **[Sequential Phragmen](/phragmen-sequential-method/)** extends to costs: voters earn money at a steady rate, and a project is funded when its supporters can pay its cost.
- **Greedy cohesive rules** find an allocation with EJR in exponential time.

## Bounds

- Maximizing the total satisfaction with general additive utilities is weakly NP-hard even with one voter, because that case is the knapsack problem (Rey, Schmidt and Maly, Table 7.1). An [FPTAS](/fptas/) for knapsack gives a near-optimal welfare.
- For every instance there is an allocation that satisfies EJR, but no strongly polynomial algorithm finds one unless P = NP, even with one voter (Theorems 13 and 14 in the survey). Checking EJR is coNP-complete, as in the unit-cost case.
- The core can be empty. Peters, Pierczynski and Skowron give an instance with unit costs and utilities in $\{0, 1, 2\}$ with no allocation in the core (Proposition 33 in the survey). With approval ballots the core can be empty when satisfaction counts money, as Maly showed in 2023. With satisfaction equal to the number of approved projects the question is open as of the March 2025 version of the survey, and in the unit-cost case it is the open question of multiwinner voting (Lackner and Skowron, Section 4.4).

## Reductions

- **From knapsack.** With one voter whose satisfaction is additive, PB is the knapsack problem, so hardness of knapsack carries over to welfare maximization.
- **To multiwinner voting.** With unit costs and $B = k$, PB with approval ballots is committee voting, and PB rules become committee rules: the method of equal shares, sequential Phragmen and the axioms of justified representation all start there.
- **To apportionment.** With unit costs and disjoint party lists, PB becomes the [apportionment problem](/apportionment-problem/), and the method of equal shares gives the D'Hondt seats.

## Applications

PB was first used in Porto Alegre, Brazil, in 1989, then spread to other Brazilian cities and to cities around the world (Rey, Schmidt and Maly, Chapter 1). Most cities fund projects greedily by number of approvals. The method of equal shares was first used in Wieliczka, Poland, in 2023. In the same year Aarau in Switzerland used it for its first participatory budget, and Swiecie in Poland used it in a vote in September 2023 for its 2024 budget. Data from many real PB elections is available in the PaBuLib library, which researchers use to compare rules.

## References
