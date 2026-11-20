---
tag: EVEFGB
kind: algorithm
slug: phragmen-sequential-method
name: "Phragmen's sequential method"
aliases:
- seq-Phragmen
- "Phragmen's method"
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Elects committee members one by one. Each member costs 1, shared by its supporters, and the next member is the one that keeps the largest load on a voter as small as possible."
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates, k: the committee size}
  time: {worst: O(k m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1894
  people: [Lars Edvard Phragmen, Markus Brill, Rupert Freeman, Svante Janson, Martin Lackner]
  note: "Phragmen proposed the method in papers from 1894 to 1899 as a form of D'Hondt without party lists. Brill, Freeman, Janson and Lackner (2017) proved that it satisfies proportional justified representation."
prereqs: [approval-voting, dhondt-method, justified-representation]
see_also: [proportional-approval-voting, method-of-equal-shares, justified-representation, dhondt-method, apportionment-problem, single-transferable-vote, chamberlin-courant-rule, participatory-budgeting]
sources:
  - paper: "Edvard Phragmen, Sur une methode nouvelle pour realiser, dans les elections, la representation proportionnelle des partis, Ofversigt af Kongliga Vetenskaps-Akademiens Forhandlingar 51(3) (1894), 133-137"
    locator: "the first paper on the sequential method, as cited by Brill, Freeman, Janson and Lackner (reference 43)"
  - paper: arxiv:2102.12305
    title: "Markus Brill, Rupert Freeman, Svante Janson and Martin Lackner, Phragmen's voting methods and justified representation, arXiv 2102.12305, version 2, February 2023 (Mathematical Programming 203 (2024), 47-76)"
    locator: "Section 4 (the method and its history), Theorem 5 (running time with exact fractions), Theorem 7 (PJR) and Example 6 (EJR fails)"
  - paper: doi:10.1007/s10107-023-01926-8
    title: "Markus Brill, Rupert Freeman, Svante Janson and Martin Lackner, Phragmen's voting methods and justified representation, Mathematical Programming 203 (2024), 47-76"
    locator: the journal version of the arXiv paper above
  - paper: arxiv:2007.01795
    title: "Martin Lackner and Piotr Skowron, Multi-Winner Voting with Approval Preferences, arXiv 2007.01795, version of August 2022 (published by Springer, 2023)"
    locator: "Rule 9, Examples 2.9 and 2.12, Table 3.1, Theorem 4.1 (D'Hondt) and Table 4.1"
  - paper: doi:10.1145/3391403.3399465
    title: "Dominik Peters and Piotr Skowron, Proportionality and the limits of welfarism, Proceedings of EC 2020, 793-794"
    locator: priceability and laminar proportionality of the method, as listed in Lackner and Skowron (Table 4.1)
---

Phragmen's sequential method (seq-Phragmen) is a multiwinner voting rule for approval ballots. Each elected candidate has a cost, or load, of $1$ that its supporters share. The method elects candidates one at a time, and each time it picks the candidate whose cost can be shared so that its supporters end with the smallest possible largest load. It runs in polynomial time, adds members without removing any as the committee grows, and satisfies proportional justified representation.

## In plain words

Think of each voter as earning money at the same steady rate. A candidate costs one unit of money, and only the voters who approve it may pay. As soon as the supporters of some candidate have one unit between them, they buy that candidate for the committee and spend all their money. Voters who paid start again from zero, and the others keep their savings. A large group earns money faster, so it buys more members, but it must spend on each one. A small group saves for longer and still gets its turn. The process stops when the committee is full.

## The problem

The input is an approval profile: for each voter $i = 1, \ldots, n$ a set $A_i$ of approved candidates among $0, \ldots, m - 1$, and a committee size $k$ with $0 \le k \le m$. For a candidate $c$, $N(c)$ is the set of voters who approve $c$. The output is a committee of $k$ candidates, listed in the order of election, together with the final load $y_i$ of each voter.

Ties go to the smallest candidate index. If no unelected candidate has a supporter, the method elects the smallest unelected index, at no cost.

## The algorithm

```pseudo id=main
SEQ-PHRAGMEN(A_1, ..., A_n, m, k)
L1  y_i ← 0 for every voter i; W ← empty list
L2  for r ← 1 to k do
L3      for each c ∉ W with N(c) ≠ ∅: t(c) ← (1 + Σ_{i ∈ N(c)} y_i) / |N(c)|
L4      c_r ← the c with the least t(c), ties to the smallest index
L5      append c_r to W
L6      y_i ← t(c_r) for every i ∈ N(c_r)
L7  return W and the loads y
```

The value $t(c)$ is the load that every supporter of $c$ would carry if they shared all their loads and the new cost of $1$ equally. In the money picture, it is the first time at which the supporters of $c$ have one unit in total.

## Example

This is Example 2.12 of Lackner and Skowron. The candidates are $a, b, c, d$, $k = 3$, and eight voters have the ballots

$$3 \times \{c, d\}, \quad 2 \times \{a, b\}, \quad 2 \times \{a, c\}, \quad 1 \times \{b, d\}.$$

| round | $t(a)$ | $t(b)$ | $t(c)$ | $t(d)$ | elected |
|---|---|---|---|---|---|
| 1 | $1/4$ | $1/3$ | $1/5$ | $1/4$ | $c$ |
| 2 | $7/20$ | $1/3$ | | $2/5$ | $b$ |
| 3 | $31/60$ | | | $29/60$ | $d$ |

In round 1 the five supporters of $c$ share its cost, so each carries $1/5$. In round 2, $a$ would need $(1 + 1/5 + 1/5)/4 = 7/20$, while the three supporters of $b$ have no load yet and need only $1/3$. In round 3, $d$ needs $(1 + 3 \cdot 1/5 + 1/3)/4 = 29/60$. The committee is $\{b, c, d\}$, and the final loads $29/60, 29/60, 29/60, 1/3, 1/3, 1/5, 1/5, 29/60$ add up to $3$. The [method of equal shares](/method-of-equal-shares/) elects $\{a, c, d\}$ on the same profile.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The times $t(c_1) \le t(c_2) \le \cdots$ never decrease, every load is at most the last time, and the supporters of $c_r$ pay $1$ in total for it. So the sum of all loads is the number of elected candidates.

For PJR, suppose a group $S$ of $s \ge \ell n / k$ voters approves $\ell$ common candidates, but its members together approve fewer than $\ell$ elected members. Then $S$ paid at most $\ell - 1$ in total, and one common candidate $c$ is never elected. At the time $\ell / s$, the voters of $S$ alone could pay $s \cdot \ell / s - (\ell - 1) = 1$ for $c$, so every round ends no later than $\ell / s$. Then all voters together paid at most $(n - s) \ell / s + \ell - 1 \le k - 1$, but they paid $k$ for the $k$ members, a contradiction.

## Complexity

Line L3 adds $|N(c)|$ loads for each unelected candidate, $O(mn)$ arithmetic operations in each round, so the method takes $O(kmn)$ operations in the [word RAM](/word-ram/) model and $O(mn)$ space for the lists of supporters. With exact fractions the numbers grow: the denominators can reach $n^k$, and Brill, Freeman, Janson and Lackner bound the bit complexity by $O(k^3 m n (\log n)^2)$ (Theorem 5). Floating point is faster but can break ties wrongly.

## Properties

- **Proportional justified representation.** A group of at least $\ell n / k$ voters with $\ell$ common approved candidates approves at least $\ell$ members in total (Brill et al., Theorem 7). It follows that justified representation holds as well.
- **Not extended justified representation.** In Example 6 of Brill et al., with $n = 24$ and $k = 12$, four voters who approve $a$ and $b$ form a $2$-cohesive group, but the committee $\{c_1, \ldots, c_{12}\}$ gives each of them only one approved member.
- **Committee monotone.** The committee for $k + 1$ seats contains the committee for $k$ seats. Few proportional rules have this property; PAV and the method of equal shares do not (Lackner and Skowron, Table 3.1).
- **D'Hondt on party lists.** With disjoint party lists, the next member of a party with $v$ voters and $s$ seats costs $(s + 1)/v$, so the method is the [D'Hondt method](/dhondt-method/) (Lackner and Skowron, Theorem 4.1).
- **Priceable and laminar proportional** (Peters and Skowron, as listed in Lackner and Skowron, Table 4.1).
- **Anonymous.** The resolute rule with fixed tie-breaking is not neutral; the set of committees over all tie-breaking orders is.
- **Not Pareto efficient and not consistent** (Lackner and Skowron, Table 3.1).

## Variants and improvements

- **Leximax-Phragmen.** Choose the whole committee and a split of its costs so that the sorted vector of loads is lexicographically smallest. It is NP-hard to compute (Brill et al., Theorem 2) and also satisfies PJR.
- **Variance-Phragmen.** Minimize the variance of the loads. On party lists it gives the [Sainte-Lague method](/sainte-lague-method/).
- **Method of equal shares.** Give each voter a budget of $k/n$ at the start instead of a steady income. This small change gives extended justified representation.
- **Eneström-Phragmen.** A quota rule for approval ballots that works like the [single transferable vote](/single-transferable-vote/).
- **Validator selection.** Variants of the sequential method choose validators in nominated proof-of-stake blockchains (Brill et al., Section 1).

## When to use it

Use it to elect a committee or a ranked list from approval ballots when proportional outcomes matter, the result must be computed exactly in polynomial time, and the committee must grow in a consistent way, for example a shortlist where the top $k$ for every $k$ should make sense. If extended justified representation is required, use the method of equal shares or [proportional approval voting](/proportional-approval-voting/) instead.

## Pitfalls

- **Forgetting the old loads.** A voter who already paid for a member carries its load into later rounds. A method that resets everyone each round is a different rule.
- **Floating point ties.** Many values of $t(c)$ are equal in small instances, as in Example 2.9 of Lackner and Skowron where $b$ and $c$ tie. Use exact fractions and state the tie-breaking rule.
- **Unsupported candidates.** A candidate with no supporters has no defined $t(c)$. Elect such candidates only when no supported candidate is left.
- **Expecting EJR.** The method satisfies PJR, not EJR.

## Implementations

## History

Phragmen, a Swedish mathematician, proposed the method in a series of papers from 1894 to 1899, as a generalization of the D'Hondt method to elections without party lists, and discussed the optimization variants in 1896. Variants of his methods were used in Swedish parliamentary elections to distribute seats within parties (Brill et al.). Interest returned with the conference version of Brill, Freeman, Janson and Lackner (2017), which proved PJR for the sequential method; Peters and Skowron (2020) showed that it is priceable and introduced the method of equal shares as a variant with EJR.

## References
