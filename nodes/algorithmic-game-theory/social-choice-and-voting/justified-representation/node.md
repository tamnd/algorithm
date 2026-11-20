---
tag: 6DVG6K
kind: definition
slug: justified-representation
name: Justified representation
aliases:
- JR
- extended justified representation
- EJR
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: Axioms for approval committees that give each cohesive group of n/k voters at least as many members as its size and cohesion warrant.
prereqs: [approval-voting, apportionment-problem]
see_also: [proportional-approval-voting, phragmen-sequential-method, method-of-equal-shares, chamberlin-courant-rule, participatory-budgeting, core-of-a-cooperative-game, dhondt-method, approval-voting]
sources:
  - paper: doi:10.1007/s00355-016-1019-3
    title: "Haris Aziz, Markus Brill, Vincent Conitzer, Edith Elkind, Rupert Freeman and Toby Walsh, Justified representation in approval-based committee voting, Social Choice and Welfare 48(2) (2017), 461-485"
    locator: "the definitions of JR and EJR, the rules that satisfy or fail them, and the coNP-completeness of checking EJR"
  - paper: doi:10.1609/aaai.v31i1.10611
    title: "Luis Sanchez-Fernandez, Edith Elkind, Martin Lackner, Norberto Fernandez, Jesus A. Fisteus, Pablo Basanta Val and Piotr Skowron, Proportional justified representation, Proceedings of AAAI 2017"
    locator: the definition of PJR
  - paper: doi:10.1609/aaai.v32i1.11478
    title: "Haris Aziz, Edith Elkind, Shenwei Huang, Martin Lackner, Luis Sanchez-Fernandez and Piotr Skowron, On the complexity of extended and proportional justified representation, Proceedings of AAAI 2018, 902-909"
    locator: "the coNP-completeness of checking PJR and two polynomial-time algorithms that output EJR committees"
  - paper: arxiv:2007.01795
    title: "Martin Lackner and Piotr Skowron, Multi-Winner Voting with Approval Preferences, arXiv 2007.01795, version of August 2022 (published by Springer, 2023)"
    locator: "Table 4.1 (which rules satisfy which axioms) and Section 4.4 (the core, Example 4.7 and the open question)"
  - paper: arxiv:2102.12305
    title: "Markus Brill, Rupert Freeman, Svante Janson and Martin Lackner, Phragmen's voting methods and justified representation, arXiv 2102.12305, version 2, February 2023 (Mathematical Programming 203 (2024), 47-76)"
    locator: "Theorem 7 (sequential Phragmen satisfies PJR) and Example 6 (it fails EJR)"
---

Justified representation (JR) and its stronger forms, proportional justified representation (PJR) and extended justified representation (EJR), are axioms of proportionality for committees elected from [approval ballots](/approval-voting/). Each says that a large enough group of voters who agree on enough candidates must be represented in the committee. They play the role that the quota plays in the [apportionment problem](/apportionment-problem/), but they need no party lists. EJR implies PJR, and PJR implies JR.

## Definition

An approval profile has $n$ voters with ballots $A_1, \ldots, A_n$, each a set of candidates among $m$ candidates, and a committee $W$ has $k$ candidates. For $1 \le \ell \le k$, a nonempty group $S$ of voters is *$\ell$-cohesive* if

$$|S| \ge \ell \cdot \frac{n}{k} \quad\text{and}\quad \Bigl|\bigcap_{i \in S} A_i\Bigr| \ge \ell,$$

that is, $S$ has at least $\ell$ times the size of one seat's share of the voters, and all its members approve the same $\ell$ candidates.

- $W$ satisfies **JR** if for every $1$-cohesive group $S$ some voter $i \in S$ has $A_i \cap W \ne \emptyset$.
- $W$ satisfies **PJR** if for every $\ell$ and every $\ell$-cohesive group $S$, $\bigl|W \cap \bigcup_{i \in S} A_i\bigr| \ge \ell$: the group as a whole approves at least $\ell$ members.
- $W$ satisfies **EJR** if for every $\ell$ and every $\ell$-cohesive group $S$ some voter $i \in S$ has $|A_i \cap W| \ge \ell$: one member of the group alone approves at least $\ell$ members.

If a voter of $S$ approves $\ell$ members, the group approves at least $\ell$ members, so EJR implies PJR. With $\ell = 1$ both say that some voter of $S$ approves a member, which is JR.

A voting rule satisfies an axiom if every committee it outputs does, on every profile and for every $k$. A rule that breaks ties must satisfy the axiom with every tie-breaking order.

**Existence and computation.** For every profile and every $k$ there is a committee with EJR: the committee of [proportional approval voting](/proportional-approval-voting/) is one (Aziz et al., 2017). The local search version of PAV and the [method of equal shares](/method-of-equal-shares/) find one in polynomial time.

**Checking.** JR is easy to check. For each candidate $c$, count the voters who approve $c$ and approve no member of $W$. Then $W$ fails JR exactly when some count is at least $n/k$, so the check takes $O(mn)$ time. Checking EJR is coNP-complete (Aziz et al., 2017), and so is checking PJR (Aziz et al., 2018). A brute force check tries every $\ell$ and every set $T$ of $\ell$ candidates and takes the voters who approve all of $T$ and fewer than $\ell$ members of $W$. For EJR the check fails when there are at least $\ell n / k$ of them. This takes time exponential in $k$.

## Examples and non-examples

Let $n = 6$ and $k = 3$, so one seat's share is $2$ voters. Four voters approve $\{a, b, c\}$ and two approve $\{d\}$, and nobody approves the candidate $e$.

- $W = \{a, b, c\}$ fails JR. The two $\{d\}$ voters form a $1$-cohesive group, and none of them approves a member. This is the committee of the $k$ candidates with the most approvals, so that rule fails JR.
- $W = \{a, d, e\}$ satisfies JR, because every voter approves a member. It fails PJR and EJR. The four $\{a, b, c\}$ voters form a $2$-cohesive group ($4 \ge 2 \cdot 6/3$), but together they approve only one member.
- $W = \{a, b, d\}$ satisfies EJR. The four voters get two members, and they are not $3$-cohesive, because that would need $6$ voters.

PJR does not imply EJR. Let $n = 4$ and $k = 2$, two voters approve $\{a, b, c\}$ and two approve $\{a, b, d\}$. All four voters form a $2$-cohesive group with the common candidates $a$ and $b$. The committee $\{c, d\}$ satisfies PJR, because the group as a whole approves both members. It fails EJR, because each voter approves only one member.

Rules on approval ballots:

| rule | JR | PJR | EJR |
|---|---|---|---|
| top $k$ by approvals | no | no | no |
| [Chamberlin-Courant](/chamberlin-courant-rule/) | yes | no | no |
| sequential PAV | no | no | no |
| proportional approval voting | yes | yes | yes |
| [sequential Phragmen](/phragmen-sequential-method/) | yes | yes | no |
| method of equal shares | yes | yes | yes |

The rows come from Aziz et al. (2017) for the top $k$ rule, sequential PAV and PAV, from Brill et al. (Theorem 7 and Example 6) for sequential Phragmen, and from Lackner and Skowron (Table 4.1) for the others.

## Related definitions

- **Party lists.** If every voter approves exactly the candidates of one party and the parties are disjoint, EJR asks that a party with at least $\ell n / k$ voters gets at least $\ell$ seats, when its list is long enough. The [D'Hondt method](/dhondt-method/) meets this, and PAV, sequential Phragmen and the method of equal shares all give the D'Hondt seats on party lists.
- **The core.** $W$ is in the core if no group $S$ and set $T$ with $|T| \le |S| \cdot k / n$ exist such that every voter of $S$ approves more members of $T$ than of $W$. This is the idea of the [core of a cooperative game](/core-of-a-cooperative-game/) applied to committees. The core implies EJR. PAV and the method of equal shares can fail it, and whether every approval profile has a committee in the core is open as of August 2022 (Lackner and Skowron, Section 4.4).
- **Proportionality degree.** The least average number of approved members, over all $\ell$-cohesive groups, as a function of $\ell$. PAV reaches $\ell - 1$ (Aziz et al., 2018), and sequential Phragmen $(\ell - 1)/2$ (Lackner and Skowron, Table 4.1).
- **Priceability and laminar proportionality.** Other proportionality axioms, satisfied by sequential Phragmen and the method of equal shares (Lackner and Skowron, Table 4.1).
- **Participatory budgeting.** In [participatory budgeting](/participatory-budgeting/) the candidates have costs, and the axioms are changed so that a group with a share of the voters can claim the same share of the money.

## References
