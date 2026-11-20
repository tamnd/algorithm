---
tag: EKGPRX
kind: algorithm
slug: chamberlin-courant-rule
name: Chamberlin-Courant rule
aliases:
- Chamberlin-Courant
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Elects the committee of k candidates that maximizes the total satisfaction of the voters with their favourite member. NP-hard in general, polynomial on single-peaked profiles."
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates, k: the committee size}
  time: {worst: O(m^2 (n + k))}
  space: {extra: O(m^2 + m n)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1983
  people: [John R. Chamberlin, Paul N. Courant, Ariel D. Procaccia, Tyler Lu, Craig Boutilier, Nadja Betzler, Arkadii Slinko, Johannes Uhlmann]
  note: "Chamberlin and Courant proposed the rule in 1983. Procaccia, Rosenschein and Zohar (2008) and Lu and Boutilier (2011) proved it NP-hard, and Betzler, Slinko and Uhlmann (2013) solved it in polynomial time on single-peaked profiles."
prereqs: [preference-profile, borda-count, single-peaked-preferences]
see_also: [proportional-approval-voting, justified-representation, method-of-equal-shares, max-coverage, greedy-max-coverage, submodular-function, k-median-problem, single-peaked-recognition]
sources:
  - paper: doi:10.2307/1957270
    title: "John R. Chamberlin and Paul N. Courant, Representative deliberations and representative decisions: proportional representation and the Borda rule, American Political Science Review 77(3) (1983), 718-733"
    locator: the rule that assigns each voter to its best committee member and maximizes the total Borda score
  - paper: doi:10.1007/s00355-007-0235-2
    title: "Ariel D. Procaccia, Jeffrey S. Rosenschein and Aviv Zohar, On the complexity of achieving proportional representation, Social Choice and Welfare 30(3) (2008), 353-362"
    locator: NP-completeness of winner determination with approval misrepresentation
  - paper: "Tyler Lu and Craig Boutilier, Budgeted social choice: from consensus to personalized decision making, Proceedings of IJCAI 2011, 280-286"
    locator: "Theorem 8 (NP-hardness with Borda scores) and the greedy algorithm with the 1 - 1/e guarantee"
  - paper: doi:10.1613/jair.3896
    title: "Nadja Betzler, Arkadii Slinko and Johannes Uhlmann, On the computation of fully proportional representation, Journal of Artificial Intelligence Research 47 (2013), 475-519"
    locator: "Section 5.1.1, Theorem 8 and Algorithm 2 (the dynamic program for single-peaked profiles, O(n m^2) time); Theorems 1 and 2 (W[2]-hardness in the committee size)"
  - paper: doi:10.1007/BF01588971
    title: "George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14(1) (1978), 265-294"
    locator: the greedy bound 1 - (1 - 1/k)^k for monotone submodular functions
  - paper: arxiv:2205.09092
    title: "Edith Elkind, Martin Lackner and Dominik Peters, Preference restrictions in computational social choice: a survey, arXiv 2205.09092, version 2, March 2025"
    locator: "Section 6.2.1 (Theorem 6.2 for single-peaked profiles, Proposition 6.3 for single-crossing profiles, and trees)"
  - paper: arxiv:2007.01795
    title: "Martin Lackner and Piotr Skowron, Multi-Winner Voting with Approval Preferences, arXiv 2007.01795, version of August 2022 (published by Springer, 2023)"
    locator: "Table 4.1 (CC satisfies JR, not PJR or EJR)"
---

The Chamberlin-Courant rule is a multiwinner voting rule. It elects a committee of $k$ candidates, and each voter counts as represented by the member it likes best. The rule chooses the committee that makes the total satisfaction of the voters with their representatives as large as possible, where the satisfaction is the [Borda](/borda-count/) score of the representative. Finding this committee is NP-hard, but on [single-peaked](/single-peaked-preferences/) profiles a dynamic program over the axis finds it in $O(m^2 (n + k))$ time.

## In plain words

A town elects $k$ people to a council. Each voter only cares about one council member: the one it likes best, who will speak for it. If your favourite candidate is elected, you are fully happy; if only your third choice is elected, you are less happy. The rule looks for the council that makes the voters happiest in total in this sense. A candidate who is the second choice of everyone is not needed if every voter already has someone better on the council. So the rule favours a council that covers the different groups of voters, which is a form of proportional representation.

## The problem

The input is a [preference profile](/preference-profile/) $P = (\succ_1, \ldots, \succ_n)$ of strict rankings of the candidates $0, \ldots, m - 1$ and a committee size $k$ with $1 \le k \le m$. Let $r_i(c)$ be the position of $c$ in $\succ_i$, with $0$ for the top. A committee $W$ of size $k$ has misrepresentation and satisfaction

$$\rho(W) = \sum_{i=1}^{n} \min_{c \in W} r_i(c), \qquad f(W) = \sum_{i=1}^{n} \max_{c \in W} \bigl(m - 1 - r_i(c)\bigr) = n(m - 1) - \rho(W).$$

The rule elects a committee of size $k$ with the least $\rho$, which is the same as the largest $f$. Ties go to the lexicographically first committee, written as a sorted list of candidate indices. Chamberlin and Courant used Borda scores; any scoring by positions, or approval ballots with score $1$ for an approved member, gives a version of the same rule.

In general no polynomial algorithm is known: the problem is NP-hard. The page gives the exact algorithm for profiles that are single-peaked on a known axis, and the greedy approximation for all profiles.

## The algorithm

Let the profile be single-peaked on the axis $a_0 \lhd a_1 \lhd \cdots \lhd a_{m-1}$, and let $q_i$ be the place of the peak of voter $i$. Each voter is best represented by the nearest member on the left of its peak or the nearest member on the right. So the cost of a committee splits into the cost of the voters left of the first member, the cost of the voters between each pair of consecutive members, and the cost of the voters right of the last member.

```pseudo id=main
CC-SINGLE-PEAKED(P, k, axis a_0, ..., a_{m-1})     ▷ κ_i(t) = r_i(a_t), q_i = place of the peak of voter i
L1  head[t] ← Σ_{i : q_i < t} κ_i(t); tail[t] ← Σ_{i : q_i ≥ t} κ_i(t), for t = 0, ..., m - 1
L2  seg[s][t] ← Σ_{i : s ≤ q_i < t} min(κ_i(s), κ_i(t)), for 0 ≤ s < t ≤ m - 1
L3  F[1][t] ← head[t] for every t
L4  for j ← 2 to k do
L5      for t ← j - 1 to m - 1 do
L6          F[j][t] ← min over j - 2 ≤ s < t of F[j - 1][s] + seg[s][t]; back[j][t] ← the best s
L7  t ← the place that minimizes F[k][t] + tail[t]
L8  follow back[k][t], back[k - 1][...], ... to read the places t_k > ... > t_1
L9  return {a_{t_1}, ..., a_{t_k}} and its misrepresentation
```

$F[j][t]$ is the least cost of the voters with peaks left of place $t$, over the committees with $j$ members whose rightmost member is at place $t$. Line L6 tries every place $s$ of the member just left of $t$. Line L7 adds the cost of the voters at or right of the last member.

For profiles that are not single-peaked, the exact search tries all $\binom{m}{k}$ committees. The greedy algorithm starts with the empty committee and adds, $k$ times, the candidate with the largest gain in satisfaction, ties to the smallest index.

## Example

The axis is $0 \lhd 1 \lhd 2 \lhd 3 \lhd 4$, $k = 2$, and five voters have the rankings

$$01234, \quad 10234, \quad 23140, \quad 32410, \quad 43210.$$

Each is single-peaked on the axis. With one seat, the misrepresentations $\mathrm{head}[t] + \mathrm{tail}[t]$ of the five candidates are $13, 9, 7, 8, 13$, so candidate $2$, the Borda winner, is best alone. With two seats the dynamic program gives:

| last member $t$ | best first member $s$ | $F[2][t]$ | $\mathrm{tail}[t]$ | total |
|---|---|---|---|---|
| 1 | 0 | 0 | 8 | 8 |
| 2 | 0 | 1 | 3 | 4 |
| 3 | 0 | 2 | 1 | 3 |
| 4 | 1 | 5 | 0 | 5 |

The optimum is $\{0, 3\}$ with misrepresentation $3$ and satisfaction $5 \cdot 4 - 3 = 17$. Voters 1 and 2 get candidate $0$, in positions $0$ and $1$, and voters 3, 4 and 5 get candidate $3$, in positions $1$, $0$ and $1$. The greedy algorithm first takes the Borda winner $2$ and then $0$, and $\{0, 2\}$ has misrepresentation $4$: the best single candidate need not be in the best committee.

## Correctness

The proof is in `proofs/correctness.md`. On a single-peaked ranking, among the members on one side of the peak the one nearest to the peak is best. So with the members at places $t_1 < \cdots < t_k$, a voter with peak between $t_j$ and $t_{j+1}$ is represented by one of these two, and the misrepresentation is

$$\rho = \mathrm{head}[t_1] + \sum_{j=1}^{k-1} \mathrm{seg}[t_j][t_{j+1}] + \mathrm{tail}[t_k].$$

An induction on $j$ shows that $F[j][t]$ is the least value of the first two parts over all choices with $t_j = t$, so line L7 finds the optimum. For the greedy algorithm, $f$ is monotone and submodular, and the argument of Nemhauser, Wolsey and Fisher gives $f(\text{greedy}) \ge (1 - (1 - 1/k)^k)\, f(\text{optimum}) > (1 - 1/e)\, f(\text{optimum}) \approx 0.632\, f(\text{optimum})$.

## Complexity

Line L1 takes $O(mn)$ time. Line L2 adds one term for each voter $i$ and each pair $s \le q_i < t$, $O(m^2 n)$ time in all. Lines L4 to L6 take $O(k m^2)$ time. The total is $O(m^2 (n + k))$ time in the [word RAM](/word-ram/) model and $O(m^2 + mn)$ space. Betzler, Slinko and Uhlmann state their dynamic program as $O(n m^2)$ time (Theorem 8). The axis can be found first by [single-peaked recognition](/single-peaked-recognition/) in $O(mn)$ time.

In general the exact search takes $O(\binom{m}{k} n k)$ time and the greedy algorithm $O(k m n)$. Winner determination is NP-hard with approval scores (Procaccia, Rosenschein and Zohar 2008) and with Borda scores (Lu and Boutilier 2011, Theorem 8), and W[2]-hard with the committee size $k$ as the parameter (Betzler, Slinko and Uhlmann 2013, Theorems 1 and 2). So an exact algorithm in time $f(k) \cdot \mathrm{poly}(n, m)$ is unlikely.

## Properties

- **One representative for each voter.** Only the best member counts. A committee with many members that a voter likes is no better for that voter than one with its favourite alone.
- **Anonymous.** The result depends only on the multiset of rankings.
- **Neutral as a correspondence.** The set of optimal committees is renamed with the candidates. The resolute rule with lexicographic tie-breaking is not neutral.
- **Diverse, not proportional in size.** A group of voters with the same favourite needs only that one member, whatever its size, so a large group does not get more seats than a small one. With approval ballots the rule and its greedy version satisfy [justified representation](/justified-representation/), but not the stronger proportional or extended justified representation (Lackner and Skowron, Table 4.1).
- **Approval version.** With approval scores, $f(W)$ is the number of voters who approve some member of $W$, and the rule is the [maximum coverage problem](/max-coverage/) with voters as elements and candidates as sets.

## Variants and improvements

- **Monroe's rule.** Each member represents about $n/k$ voters, so the representation is balanced in size. It stays NP-hard on single-peaked profiles (Betzler, Slinko and Uhlmann 2013).
- **Minimax versions.** Minimize the largest misrepresentation of a voter instead of the sum. On single-peaked profiles this version is solved by a greedy algorithm (Betzler, Slinko and Uhlmann 2013, Section 5.1).
- **Other domains.** On single-crossing profiles an optimal committee can be found in polynomial time, because some optimal committee represents intervals of the voter order. On profiles single-peaked on a tree the rule stays NP-complete, even with Borda scores (Elkind, Lackner and Peters, Section 6.2.1).
- **Approximation.** The greedy algorithm is the [greedy max coverage](/greedy-max-coverage/) algorithm applied to a weighted coverage function. The same structure appears in the [k-median problem](/k-median-problem/), with candidates as facilities and Borda positions as distances.

## When to use it

Use it to choose a committee or a set of options where each voter will use one of them: a set of products to stock, a panel of experts, a set of movies to show on a flight. Do not use it when seats should be shared in proportion to group sizes, as in a parliament; use [proportional approval voting](/proportional-approval-voting/), the [method of equal shares](/method-of-equal-shares/) or an [apportionment](/apportionment-problem/) method instead. For many candidates, use the dynamic program when the profile is single-peaked, and an integer program or the greedy algorithm otherwise.

## Pitfalls

- **Choosing the top $k$ Borda candidates.** That is a different rule. In the example, the two best Borda candidates are $2$ and $3$, with misrepresentation $5$, while the optimum is $3$.
- **Greedy and misrepresentation.** The guarantee $1 - 1/e$ is for satisfaction. In misrepresentation the greedy committee can be much worse in ratio: in the example it is $4$ against $3$.
- **Using the dynamic program on the wrong axis.** The cost formula holds only if every voter is single-peaked on the given axis. On other profiles the program returns some committee, not the optimum.
- **Ties.** The optimum is often not unique. State the tie-breaking rule, here the lexicographically first committee.

## Implementations

## History

Chamberlin and Courant (1983) proposed the rule as a form of proportional representation built on the Borda count: each voter is assigned to its best representative, and the assignment with the highest total Borda score wins. Monroe (1995) added a balance condition on the number of voters per representative. Procaccia, Rosenschein and Zohar (2008) proved that both rules are NP-hard to compute, Lu and Boutilier (2011) studied them as budgeted social choice and used the greedy algorithm, and Betzler, Slinko and Uhlmann (2013) mapped the parameterized complexity and gave the dynamic program for single-peaked profiles.

## References
