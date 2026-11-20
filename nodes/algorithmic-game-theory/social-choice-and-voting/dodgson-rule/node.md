---
tag: 81D8GC
kind: algorithm
slug: dodgson-rule
name: "Dodgson's rule"
aliases:
- "Dodgson's method"
- "Lewis Carroll's voting rule"
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Elects the candidate that needs the fewest swaps of adjacent candidates in ballots to become a Condorcet winner. Winner finding is Theta_2^p-complete (Hemaspaandra, Hemaspaandra and Rothe 1997)."
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: "O(m^3 n (n/2 + 2)^(m - 1))"}
  space: {extra: "O(m (n/2 + 2)^(m - 1))"}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1876
  people: [Charles Lutwidge Dodgson]
  note: "Dodgson proposed the rule in a pamphlet of 1876. Bartholdi, Tovey and Trick proved in 1989 that computing the winner is NP-hard, and Hemaspaandra, Hemaspaandra and Rothe found its exact complexity in 1997."
prereqs: [condorcet-winner, preference-profile, kendall-tau-distance]
see_also: [copeland-method, kemeny-rank-aggregation, smith-set, slater-rule, condorcet-paradox, polynomial-hierarchy, fixed-parameter-tractable, lenstra-algorithm]
sources:
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 5 (Ioannis Caragiannis, Edith Hemaspaandra and Lane A. Hemaspaandra, Dodgson's rule and Young's rule): Theorem 5.1 on the Theta_2^p-completeness, Section 5.5 on the fixed-parameter results, Theorem 5.6 on the ratio H_(m-1) of the greedy and the LP algorithms, Theorem 5.10 on inapproximability, and the failure of monotonicity found by Fishburn"
  - paper: doi:10.1145/268999.269002
    title: "Edith Hemaspaandra, Lane A. Hemaspaandra and Jörg Rothe, Exact analysis of Dodgson elections: Lewis Carroll's 1876 voting system is complete for parallel access to NP, Journal of the ACM 44(6) (1997), 806-825"
    locator: "the main theorem: deciding whether a candidate is a Dodgson winner is complete for parallel access to NP"
  - paper: doi:10.1007/BF00303169
    title: "John J. Bartholdi III, Craig A. Tovey and Michael A. Trick, Voting schemes for which it can be difficult to tell who won the election, Social Choice and Welfare 6(2) (1989), 157-165"
    locator: "the NP-hardness of the Dodgson score and of the Dodgson winner"
---

Dodgson's rule elects the candidate that is closest to being a [Condorcet winner](/condorcet-winner/). The distance is the Dodgson score: the least number of swaps of two adjacent candidates on the ballots after which the candidate beats every other one by a strict majority. A Condorcet winner has score 0 and wins. When there is none, the rule picks the candidate with the smallest score. Computing the score is NP-hard, and deciding whether a candidate wins is complete for $\Theta_2^p$, the class of problems solvable in polynomial time with logarithmically many queries to an NP oracle. The algorithm below is a dynamic program over the voters. It is exact, and it runs in polynomial time when the number of candidates is fixed.

## In plain words

If one candidate beats every other one in head-to-head majority votes, that candidate should win. Often no candidate does. The rule then asks how much the ballots would have to change for a candidate to get there. The only change allowed is to swap two neighbours on one ballot, and each swap costs one. The candidate that needs the fewest swaps wins. Lewis Carroll, the author of the Alice books, proposed this rule. The idea is simple, but finding the fewest swaps is hard in general. When there are only a few candidates, the search is fast, because it only needs to track how many more voters must prefer the candidate to each rival.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and a profile $P$ of $n \ge 1$ rankings, each best first. Let $N(x, y)$ be the number of voters who rank $x$ above $y$. Candidate $c$ is a Condorcet winner when $N(c, b) > n/2$ for every $b \ne c$, that is, $N(c, b) \ge q$ with $q = \lfloor n/2 \rfloor + 1$. A swap exchanges two adjacent candidates on one ballot. The Dodgson score $\mathrm{sc}(c)$ is the least number of swaps that turn $P$ into a profile where $c$ is a Condorcet winner. The Dodgson winners are the candidates with the least score. Ties go to the candidate with the smallest index, as on every rule page of this area.

A swap that does not involve $c$ does not change any count $N(c, b)$, and a swap that moves $c$ down only lowers one. The proof shows that some optimal sequence moves $c$ up on each ballot and does nothing else. On a ballot where $c$ is in place $\ell$ (place 0 is the top), the choices are to move $c$ up by $k = 0, \ldots, \ell$ places, at cost $k$, which puts $c$ above the $k$ candidates just above it.

## The algorithm

```pseudo id=main
DODGSON-SCORE(P, c)
L1  N[x][y] ← number of voters who rank x above y; q ← ⌊n/2⌋ + 1
L2  d0[b] ← max(0, q - N[c][b]) for each b ≠ c
L3  F ← {d0 ↦ 0}
L4  for each ballot r of P do
L5      G ← empty map
L6      for each (d, cost) in F, and each k ← 0 to (number of candidates above c in r) do
L7          d' ← d with 1 subtracted, but not below 0, at the k candidates just above c in r
L8          G[d'] ← min(G[d'], cost + k)
L9      F ← G
L10 return F[(0, ..., 0)]

DODGSON(P, m)
L11 return the smallest c with the least DODGSON-SCORE(P, c)
```

The vector $d$ holds the deficit of $c$ against each rival $b$: how many more voters must put $c$ above $b$. Line L2 sets the starting deficits. After each ballot, $F$ maps every deficit vector that can be reached to the least cost that reaches it. A deficit never goes below 0, because a larger majority than needed has no value. Line L10 reads the cost of the zero vector, which is reached at least by moving $c$ to the top of every ballot. The code also returns all scores and the set of winners.

## Example

Take four candidates $a, b, c, d$ (indices 0 to 3) and 7 voters, so $q = 4$:

| voter | ranking |
|---|---|
| 1, 2 | $d \succ a \succ b \succ c$ |
| 3 | $b \succ c \succ d \succ a$ |
| 4 | $c \succ d \succ b \succ a$ |
| 5 | $d \succ a \succ c \succ b$ |
| 6 | $a \succ b \succ c \succ d$ |
| 7 | $c \succ d \succ a \succ b$ |

The majorities are $d$ over $a$ (6 to 1), $d$ over $b$ (5 to 2), $a$ over $b$ (5 to 2), $a$ over $c$ (4 to 3), $b$ over $c$ (4 to 3) and $c$ over $d$ (4 to 3). The cycle $d \succ a \succ c \succ d$ means that there is no Condorcet winner. The scores are:

- $d$ needs one more voter against $c$. On ballot 4, $c$ is just above $d$, so one swap is enough: $\mathrm{sc}(d) = 1$.
- $c$ needs one more voter against $a$ and one against $b$. On ballot 1, one swap passes $b$ and a second one passes $a$. No single swap gives both, so $\mathrm{sc}(c) = 2$.
- $a$ needs three more voters against $d$. Ballots 1, 2 and 5 each give one for one swap: $\mathrm{sc}(a) = 3$.
- $b$ needs two more voters against $a$ and two against $d$. On ballots 1 and 2, two swaps lift $b$ over both: $\mathrm{sc}(b) = 4$.

So $d$ wins. For $c$, the starting deficits against $(a, b, d)$ are $(1, 1, 0)$. On ballot 1 the candidates just above $c$ are $b$, then $a$, then $d$. The values $k = 0, 1, 2$ give $F = \{(1, 1, 0) \mapsto 0, (1, 0, 0) \mapsto 1, (0, 0, 0) \mapsto 2\}$. The value $k = 3$ also passes $d$, which gives the vector $(0, 0, 0)$ at cost 3, so it is dropped. No later ballot gives a cheaper way to $(0, 0, 0)$.

## Correctness

The proof in `proofs/correctness.md` first shows that some cheapest way to make $c$ a Condorcet winner only moves $c$ up, ballot by ballot. If an optimal sequence puts $c$ above some candidate $b$ that was above it, then every candidate between $b$ and $c$ must end below $c$ too, or the sequence pays for one more inversion. So moving $c$ up past all of them costs no more and gains at least as much. The dynamic program then tries every amount for every ballot and keeps, for each deficit vector, the cheapest way to reach it. Two partial choices with the same deficit vector can be completed in the same ways, so keeping the cheaper one is safe.

## Complexity

A deficit lies between 0 and $q \le \lfloor n/2 \rfloor + 1$, so $F$ has at most $(\lfloor n/2 \rfloor + 2)^{m - 1}$ entries. Each ballot tries at most $m$ values of $k$ for each entry, at cost $O(m)$ each for the vector. One score costs $O(m^2 n (n/2 + 2)^{m - 1})$ time, and all $m$ scores cost $O(m^3 n (n/2 + 2)^{m - 1})$ in the [word RAM](/word-ram/) model, with $O(m (n/2 + 2)^{m - 1})$ space for the maps. This is polynomial in $n$ for each fixed $m$, but exponential in $m$.

The exponent cannot be avoided by a much better general method unless P = NP: Bartholdi, Tovey and Trick proved that the score is NP-hard to compute. Deciding whether a candidate is a winner needs the scores of all candidates to be compared, and Hemaspaandra, Hemaspaandra and Rothe proved that it is complete for $\Theta_2^p$, the class $\mathrm{P}^{\mathrm{NP}[O(\log)]}$ in the [polynomial hierarchy](/polynomial-hierarchy/). The score is [fixed-parameter tractable](/fixed-parameter-tractable/) in the number of candidates, by an integer program with a fixed number of variables solved by [Lenstra's algorithm](/lenstra-algorithm/), and also in the score itself. It is W[1]-hard in the number of voters.

## Properties

The proofs are in `proofs/correctness.md`, and the tests check each property on all profiles with up to 4 candidates and few voters and on random profiles.

- **Condorcet consistent.** A candidate has score 0 exactly when it is a Condorcet winner, so a Condorcet winner is the unique winner.
- **Pareto.** If every voter ranks $a$ above $b$, then $\mathrm{sc}(a) < \mathrm{sc}(b)$, so $b$ does not win.
- **Anonymous, and neutral as a correspondence.** The resolute rule is not neutral, because of the tie rule.
- **Not homogeneous.** Copying every ballot the same number of times can change the winners, because the threshold $q$ does not scale exactly. The tests have a profile of 7 voters with winners $\{a, b, d\}$ whose triple, with 21 voters, has the single winner $b$.
- **Not monotone.** Fishburn showed that for 4 or more candidates, moving the winner up on some ballots can make it lose.
- **Manipulable.** By the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/), as for every resolute rule with at least 3 possible winners that is not a dictatorship, a voter can sometimes gain by a false ranking. The tests find such a case with 3 candidates and 3 voters.

## Variants and improvements

- **Approximation.** A greedy algorithm and an LP rounding algorithm approximate the score within the ratio $H_{m-1} = 1 + 1/2 + \cdots + 1/(m - 1)$, and a ratio much below $\ln m$ is not possible in polynomial time unless P = NP. A rule that elects the candidate with the smallest approximate score is a different voting rule.
- **Young's rule.** It counts the least number of voters to delete so that the candidate becomes a Condorcet winner.
- **Weak Dodgson.** It asks for a weak Condorcet winner, one that loses to nobody, instead of a strict one.
- **Kemeny and Slater.** [Kemeny's rule](/kemeny-rank-aggregation/) and [Slater's rule](/slater-rule/) also measure a distance to consistency with majorities, but for a whole ranking rather than for one candidate.

## When to use it

Use Dodgson's rule when a Condorcet winner should be elected whenever there is one, and the idea of the fewest changes to the ballots is the right way to settle cycles. It is exact and fast for a small number of candidates, with any number of voters. For many candidates use an approximation, or pick a Condorcet method that is easy to compute and monotone, such as [Copeland's method](/copeland-method/), [ranked pairs](/ranked-pairs/) or the [Schulze method](/schulze-method/).

## Pitfalls

- **Swaps that do not involve the candidate.** They never help, but a search over all swaps still explores them. Restrict the search to moving the candidate up.
- **Moving past the nearest candidates only.** On one ballot, $c$ can only pass the candidates just above it, in order. Treating the candidates that $c$ passes as a free choice gives scores that are too low.
- **The majority threshold.** With $n$ even, $c$ needs $n/2 + 1$ voters against each rival, not $n/2$. The threshold $q = \lfloor n/2 \rfloor + 1$ covers both cases.
- **Empty profiles.** With no voters, no candidate can become a Condorcet winner. The code returns no score and makes every candidate a winner.

## Implementations

## History

Charles Lutwidge Dodgson, the Oxford mathematician who wrote as Lewis Carroll, proposed the rule in a pamphlet of 1876. Fishburn later showed that the rule is not monotone. In 1989 Bartholdi, Tovey and Trick proved that the score and the winner are NP-hard to compute, one of the first results in computational social choice. In 1997 Hemaspaandra, Hemaspaandra and Rothe proved that the winner problem is complete for parallel access to NP, that is, for $\Theta_2^p$. Later work by Caragiannis and coauthors and by others gave approximation algorithms and parameterized algorithms.

## References
