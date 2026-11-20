---
tag: 95W632
kind: algorithm
slug: proportional-approval-voting
name: Proportional approval voting
aliases:
- PAV
- Thiele's method
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Elects the committee that maximizes the sum over voters of 1 + 1/2 + ... + 1/j, where j is the number of approved members."
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates, k: the committee size}
  time: {worst: O(k^3 m n log k)}
  space: {extra: O(m n)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1895
  people: [Thorvald N. Thiele, Haris Aziz, Edith Elkind, Martin Lackner, Piotr Skowron]
  note: "Thiele defined the rule in 1895. Aziz et al. proved that it satisfies extended justified representation, and in 2018 gave a local search version that keeps this property in polynomial time."
prereqs: [approval-voting, harmonic-series, dhondt-method]
see_also: [justified-representation, phragmen-sequential-method, method-of-equal-shares, chamberlin-courant-rule, dhondt-method, local-search, submodular-function, participatory-budgeting]
sources:
  - paper: "Thorvald N. Thiele, Om flerfoldsvalg, Oversigt over det Kongelige Danske Videnskabernes Selskabs Forhandlinger (1895), 415-441"
    locator: "the rule with the weights 1, 1/2, 1/3, ..., as reported by Lackner and Skowron (Rule 4)"
  - paper: doi:10.1007/s00355-016-1019-3
    title: "Haris Aziz, Markus Brill, Vincent Conitzer, Edith Elkind, Rupert Freeman and Toby Walsh, Justified representation in approval-based committee voting, Social Choice and Welfare 48(2) (2017), 461-485"
    locator: the definitions of JR and EJR and the proof that PAV satisfies EJR
  - paper: doi:10.1609/aaai.v32i1.11478
    title: "Haris Aziz, Edith Elkind, Shenwei Huang, Martin Lackner, Luis Sanchez-Fernandez and Piotr Skowron, On the complexity of extended and proportional justified representation, Proceedings of AAAI 2018, 902-909"
    locator: "the local search version of PAV with swap threshold n/k^2, and the proportionality degree l - 1"
  - paper: doi:10.1016/j.artint.2016.09.003
    title: "Piotr Skowron, Piotr Faliszewski and Jerome Lang, Finding a collective set of items: from proportional multirepresentation to group recommendation, Artificial Intelligence 241 (2016), 191-216"
    locator: "Theorem 5 (NP-hardness of a class of Thiele methods that includes PAV)"
  - paper: arxiv:2007.01795
    title: "Martin Lackner and Piotr Skowron, Multi-Winner Voting with Approval Preferences, arXiv 2007.01795, version of August 2022 (published by Springer, 2023)"
    locator: "Rule 4, Example 2.5, Table 3.1, Theorems 4.1 to 4.3, Section 4.4 (the core), Table 4.1, Theorem 5.3 and Table 5.1"
  - paper: "Szymon Dudycz, Pasin Manurangsi, Jan Marcinkowski and Krzysztof Sornat, Tight approximation for Proportional Approval Voting, Proceedings of IJCAI 2020, 276-282"
    locator: "the approximation ratio 0.7965, tight unless P = NP"
  - paper: arxiv:2408.02300
    title: "Sonja Kraiczy and Edith Elkind, A lower bound for local search proportional approval voting, arXiv 2408.02300, August 2024 (ESA 2024)"
    locator: "the lower bound of k^(log k) swaps for arbitrarily small thresholds, with improving swaps chosen in lexicographic order"
---

Proportional approval voting (PAV) is a multiwinner voting rule for approval ballots. A voter with $j$ approved members in the committee gets the satisfaction $1 + 1/2 + \cdots + 1/j$, and PAV elects the committee of size $k$ with the largest total satisfaction. It gives each cohesive group of voters a share of the seats in proportion to its size, which is the property called [extended justified representation](/justified-representation/). Finding a PAV committee is [NP-hard](/np-hard/), but a [local search](/local-search/) version runs in polynomial time and keeps the same proportionality guarantee.

## In plain words

Every voter marks the candidates it likes. A council of $k$ people is to be elected. Each voter is happy with each approved council member, but the second one makes it less happy than the first, the third less than the second, and so on. So the rule does not give all seats to the largest group: after that group has some seats, one more seat for a smaller group adds more happiness. The rule picks the council with the most happiness in total. The effect is that a group with a third of the voters, who agree on enough candidates, gets about a third of the seats. With parties, this is the classical method that parliaments use to share seats.

## The problem

The input is an approval profile: for each voter $i = 1, \ldots, n$, a set $A_i$ of approved candidates among $0, \ldots, m - 1$, and a committee size $k$ with $0 \le k \le m$. Let $H(j) = 1 + 1/2 + \cdots + 1/j$ be the $j$-th harmonic number, with $H(0) = 0$ (see [harmonic series](/harmonic-series/)). The PAV score of a committee $W$ is

$$\mathrm{pav}(W) = \sum_{i=1}^{n} H(|A_i \cap W|).$$

PAV elects a committee of size $k$ with the largest score. Ties go to the lexicographically first committee, written as a sorted list of candidate indices.

A committee $W$ satisfies extended justified representation (EJR) if for every $\ell$ with $1 \le \ell \le k$ and every group $S$ of at least $\ell n / k$ voters who all approve the same $\ell$ candidates, some voter in $S$ approves at least $\ell$ members of $W$. The page gives the exact rule and the local search algorithm that finds a committee with EJR in polynomial time.

## The algorithm

The local search starts from some committee, by default the output of sequential PAV. It swaps one member for one non-member while a swap raises the PAV score by at least $n / k^2$. With $x_i = |A_i \cap W|$, a voter gains $1/(x_i + 1)$ when an approved candidate joins and loses $1/x_i$ when an approved member leaves.

```pseudo id=main
LS-PAV(A_1, ..., A_n, m, k, start)     ▷ start defaults to the committee of sequential PAV
L1  W ← start, sorted; if n = 0 or k = 0 or k = m then return W
L2  ε ← n / k^2
L3  x_i ← |A_i ∩ W| for every voter i
L4  repeat
L5      for each w ∈ W and each c ∉ W, in increasing order
L6          if Σ_{i : c ∈ A_i, w ∉ A_i} 1/(x_i + 1) - Σ_{i : w ∈ A_i, c ∉ A_i} 1/x_i ≥ ε then take the swap (w, c) and end the scan
L7      if no swap was taken then return W
L8      W ← (W \ {w}) ∪ {c}
L9      x_i ← x_i - [w ∈ A_i] + [c ∈ A_i] for every voter i
```

The exact rule tries all $\binom{m}{k}$ committees and keeps the first one with the largest score. Sequential PAV starts with the empty committee and adds, $k$ times, the candidate with the largest gain $\sum_{i : c \in A_i} 1/(x_i + 1)$, ties to the smallest index. Every score is an exact fraction.

## Example

This is Example 2.5 of Lackner and Skowron. The candidates are $a, b, c, d$, $k = 2$, and $n = 23$ voters have the ballots

$$3 \times \{a, b\}, \quad 6 \times \{a, d\}, \quad 4 \times \{b\}, \quad 5 \times \{c\}, \quad 5 \times \{c, d\}.$$

The scores of the six committees are:

| committee | $\{a, b\}$ | $\{a, c\}$ | $\{a, d\}$ | $\{b, c\}$ | $\{b, d\}$ | $\{c, d\}$ |
|---|---|---|---|---|---|---|
| PAV score | $29/2$ | $19$ | $17$ | $17$ | $18$ | $37/2$ |

PAV elects $\{a, c\}$: every voter except the four $\{b\}$ voters gets one approved member. Sequential PAV first takes $d$, which has the most approvals ($11$). Then the gains are $3 + 6/2 = 6$ for $a$, $3 + 4 = 7$ for $b$ and $5 + 5/2 = 15/2$ for $c$, so it takes $c$ and elects $\{c, d\}$ with score $37/2$. Started from $\{c, d\}$, the local search tries the swaps; the best one, $d$ for $a$, gains only $1/2$, less than $\varepsilon = 23/4$, so it stops at once. Both $\{a, c\}$ and $\{c, d\}$ satisfy EJR.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The key step is a swap lemma. Suppose $W$ violates EJR for a group $S$ with $|S| \ge \ell n / k$ that approves $\ell$ common candidates. Then one of these candidates $c$ is not in $W$, and adding $c$ raises the score by $G \ge |S| / \ell \ge n / k$, because each voter of $S$ has fewer than $\ell$ approved members. In $W \cup \{c\}$, the losses of removing the $k$ members of $W$ add up to at most $n - G$, so one member $w$ costs at most $(n - G)/k$. The swap of $w$ for $c$ gains at least $G(1 + 1/k) - n/k \ge n / k^2$.

So a committee from which no swap gains $n / k^2$ satisfies EJR. The local search stops only at such a committee (line L7), and an optimal PAV committee has no improving swap at all. The score lies between $0$ and $n H(k)$, and each swap adds at least $n / k^2$, so there are at most $k^2 H(k)$ swaps.

## Complexity

Each pass of lines L5 and L6 tries at most $k(m - k)$ swaps of $O(n)$ arithmetic operations each, and there are at most $k^2 H(k) + 1$ passes. With $H(k) = O(\log k)$ this gives $O(k^3 m n \log k)$ arithmetic operations in the [word RAM](/word-ram/) model, and $O(mn)$ extra space for the ballots. Sequential PAV takes $O(kmn)$ and the exact search $O(\binom{m}{k} n k)$.

Computing a PAV committee is NP-hard (Skowron, Faliszewski and Lang 2016, Theorem 5). Sequential PAV reaches at least $1 - (1 - 1/k)^k \ge 1 - 1/e$ of the optimal score, because the score is a monotone [submodular function](/submodular-function/) (Lackner and Skowron, Theorem 5.3). Dudycz, Manurangsi, Marcinkowski and Sornat (2020) gave a $0.7965$ approximation, which is tight unless P = NP. For exact solutions, the most common method is a [binary integer program](/binary-integer-programming/) (Lackner and Skowron, Chapter 5).

## Properties

- **Extended justified representation.** Every PAV committee satisfies EJR, and so also PJR and JR (Aziz et al. 2017; Lackner and Skowron, Theorem 4.3). The local search committee satisfies EJR too.
- **Proportionality degree.** In an $\ell$-cohesive group, the average voter approves more than $\ell - 1$ members (Lackner and Skowron, Theorem 4.3). This is the best possible degree.
- **D'Hondt on party lists.** When the voters split into parties with disjoint lists, PAV gives the seat counts of the [D'Hondt method](/dhondt-method/) (Lackner and Skowron, Theorem 4.1). PAV is the only rule that extends D'Hondt and is neutral, anonymous, consistent and continuous (Theorem 4.2).
- **Anonymous, and neutral as a correspondence.** The resolute rule with lexicographic tie-breaking is not neutral.
- **Pareto efficient and consistent,** but not committee monotone: the PAV committee for $k + 1$ seats need not contain the one for $k$ seats (Lackner and Skowron, Table 3.1).
- **Not in the core.** PAV can violate the core (Lackner and Skowron, Example 4.7). Whether the core of an approval election is always nonempty is open (Lackner and Skowron, Section 4.4, version of August 2022).

## Variants and improvements

- **Thiele methods.** "Thiele's method" often means PAV, but Thiele defined a family: any nondecreasing weight function $w$ with $w(0) = 0$ gives a rule that maximizes $\sum_i w(|A_i \cap W|)$. [Approval voting](/approval-voting/) uses $w(j) = j$, the approval [Chamberlin-Courant rule](/chamberlin-courant-rule/) uses $w(j) = \min(j, 1)$, and PAV uses $w(j) = H(j)$. The weights $1, 1/3, 1/5, \ldots$ give a rule that extends the [Sainte-Lague method](/sainte-lague-method/).
- **Sequential PAV.** The greedy version is fast and also extends D'Hondt, but it fails EJR (Lackner and Skowron, Section 4.2). Reverse sequential PAV removes candidates one by one from the full set and fails EJR as well.
- **Local search threshold.** With the threshold $n / k^2$ the number of swaps is polynomial. With an arbitrarily small threshold and improving swaps chosen in lexicographic order, the search can need $\Omega(k^{\log k})$ swaps, which is not polynomial in $k$ (Kraiczy and Elkind 2024).
- **Other rules with EJR.** The [method of equal shares](/method-of-equal-shares/) satisfies EJR in polynomial time without local search, and [Phragmen's sequential method](/phragmen-sequential-method/) satisfies the weaker PJR.

## When to use it

Use PAV to elect a committee, a board or a short list from approval ballots when seats should follow the size of the groups of like-minded voters, and the number of candidates is small enough for an exact solver. When a polynomial guarantee matters, use the local search or the method of equal shares. For budgets with costs, see [participatory budgeting](/participatory-budgeting/). For one representative per voter, use the Chamberlin-Courant rule.

## Pitfalls

- **Taking sequential PAV for PAV.** In the example they elect different committees. Sequential PAV fails EJR, and the local search need not find the PAV optimum.
- **Floating point.** Sums of $1/j$ in floating point can make two equal scores look different and change the result. Use exact fractions, or multiply all weights by $\mathrm{lcm}(1, \ldots, k)$.
- **Tiny swap thresholds.** A local search that accepts every improving swap can run for a very long time. Keep the threshold $n / k^2$.
- **Ties.** Many committees can have the same score. State the tie-breaking rule, here the lexicographically first committee.

## Implementations

## History

Thiele (1895) defined PAV, together with the family of rules that now carry his name. Aziz, Brill, Conitzer, Elkind, Freeman and Walsh (2015, journal version 2017) defined justified representation and EJR, and proved that PAV satisfies EJR. Skowron, Faliszewski and Lang (2016) proved that computing it is NP-hard, and Aziz, Elkind, Huang, Lackner, Sanchez-Fernandez and Skowron (2018) gave the local search version that satisfies EJR in polynomial time. Lackner and Skowron characterized PAV as the unique extension of D'Hondt with neutrality, anonymity, consistency and continuity.

## References
