---
tag: D4PRR4
kind: algorithm
slug: copeland-method
name: "Copeland's method"
aliases:
- Copeland rule
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Ranks candidates by the number of pairwise majority contests they win minus those they lose. It is Condorcet consistent.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(n m^2)}
  space: {extra: O(m^2)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1951
  people: [Ramon Llull, Arthur H. Copeland]
  note: "Llull described the variant that gives a full point for a tie in the 13th century; Copeland proposed the rule in a 1951 seminar at the University of Michigan."
prereqs: [condorcet-winner, preference-profile]
see_also: [smith-set, ranked-pairs, schulze-method, slater-rule, borda-count, election-control-problem, voting-manipulation-problem, metric-distortion]
sources:
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 3 (Felix Brandt, Markus Brill and Paul Harrenstein, Tournament solutions), Section 3.3, the Copeland set and Theorem 3.2 (it can be computed in linear time)"
  - paper: "Arthur H. Copeland, A reasonable social welfare function, mimeographed notes, Seminar on Applications of Mathematics to the Social Sciences, University of Michigan, 1951"
    locator: the rule that ranks candidates by pairwise wins minus pairwise losses
  - paper: doi:10.1613/jair.2697
    title: "Piotr Faliszewski, Edith Hemaspaandra, Lane A. Hemaspaandra and Jörg Rothe, Llull and Copeland voting computationally resist bribery and constructive control, Journal of Artificial Intelligence Research 35 (2009), 275-341"
    locator: "the Copeland^alpha family, and the proof that for every rational alpha with 0 < alpha < 1 it resists all standard types of constructive control"
  - paper: doi:10.1016/j.artint.2018.07.006
    title: "Elliot Anshelevich, Onkar Bhardwaj, Edith Elkind, John Postl and Piotr Skowron, Approximating optimal social choice under metric preferences, Artificial Intelligence 264 (2018), 27-51"
    locator: the upper bound of 5 on the metric distortion of Copeland
  - paper: doi:10.1007/BF00295861
    title: "John J. Bartholdi III, Craig A. Tovey and Michael A. Trick, The computational difficulty of manipulating an election, Social Choice and Welfare 6(3) (1989), 227-241"
    locator: "the greedy algorithm that finds a manipulation by one voter, and the NP-hardness of manipulating Copeland with the second-order Copeland tie-break"
---

Copeland's method elects the candidate that wins the most head-to-head majority contests. For each pair of candidates, it asks which one more voters rank higher, and it gives the winner of the pair one point and takes one point from the loser. The candidate with the highest total wins, and sorting by the totals gives a full ranking. A candidate that beats every rival, the [Condorcet winner](/condorcet-winner/), scores $m - 1$, which no other candidate can reach, so the method is Condorcet consistent. It is easy to explain and to compute, but it often ends in a tie at the top.

## In plain words

Think of the election as a round-robin sports league. Every candidate plays every other candidate once. In each game, the voters decide: the candidate that more voters rank higher wins the game. A win earns a point, a loss costs a point, and a draw changes nothing. At the end, the candidate at the top of the league table wins. A candidate that beats all others wins every game, so it always comes first. When no such candidate exists, the table shows who wins the most games, but it does not care by how much a game was won, so two or more candidates often share the top place.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and $n$ voters, and voter $i$ has a ranking $r_i$ of all candidates, best first. For candidates $a \ne b$, let $n_P(a, b)$ be the number of voters who rank $a$ above $b$. Candidate $a$ beats $b$ when $n_P(a, b) > n_P(b, a)$, and the pair is a tie when the two counts are equal. The Copeland score of $a$ is

$$s_P(a) = |\{ b : a \text{ beats } b \}| - |\{ b : b \text{ beats } a \}|.$$

The Copeland correspondence returns $W(P) = \arg\max_a s_P(a)$, and the resolute rule returns one element of $W(P)$. Ties go to the candidate with the smallest index, as on every rule page of this area. The Copeland ranking sorts the candidates by $s_P$, highest first, with the same tie rule.

## The algorithm

```pseudo id=main
COPELAND(P, m)                            ▷ P = (r_1, ..., r_n), each ranking best first
L1  N[a][b] ← number of voters who rank a above b, for all a ≠ b
L2  s[a] ← 0 for each candidate a
L3  for each pair a < b do
L4      if N[a][b] > N[b][a] then s[a] ← s[a] + 1; s[b] ← s[b] - 1
L5      else if N[b][a] > N[a][b] then s[b] ← s[b] + 1; s[a] ← s[a] - 1
L6  W ← {a : s[a] = max over b of s[b]}   ▷ the Copeland correspondence
L7  return the smallest candidate in W    ▷ the fixed tie-breaking rule
```

Line L1 builds the pairwise count matrix with one pass over each ballot: for a ballot, every candidate is above each candidate that comes later in it. Lines L3 to L5 play each pair once. A tied pair passes both tests of lines L4 and L5 and changes no score. Line L6 finds the candidates with the best record, and line L7 applies the tie-breaking rule. The code also returns the set $W$ and the full ranking.

## Example

Take four candidates $a, b, c, d$ (indices 0 to 3) and three voters:

| voter | ranking |
|---|---|
| 1 | $d \succ a \succ b \succ c$ |
| 2 | $a \succ b \succ c \succ d$ |
| 3 | $b \succ c \succ d \succ a$ |

Line L1 gives these pairwise results, each as the count for the first candidate against the count for the second: $a$ beats $b$ by 2 to 1, $a$ beats $c$ by 2 to 1, $d$ beats $a$ by 2 to 1, $b$ beats $c$ by 3 to 0, $b$ beats $d$ by 2 to 1, and $c$ beats $d$ by 2 to 1.

| step | pair | winner | $s = (s_a, s_b, s_c, s_d)$ |
|---|---|---|---|
| L2 | | | $(0, 0, 0, 0)$ |
| L3 to L5 | $a, b$ | $a$ | $(1, -1, 0, 0)$ |
| L3 to L5 | $a, c$ | $a$ | $(2, -1, -1, 0)$ |
| L3 to L5 | $a, d$ | $d$ | $(1, -1, -1, 1)$ |
| L3 to L5 | $b, c$ | $b$ | $(1, 0, -2, 1)$ |
| L3 to L5 | $b, d$ | $b$ | $(1, 1, -2, 0)$ |
| L3 to L5 | $c, d$ | $c$ | $(1, 1, -1, -1)$ |
| L6 | | | $W = \{a, b\}$ |
| L7 | | | return $a$ |

There is no Condorcet winner: $a$ loses to $d$, and $b$ loses to $a$. The majorities form the cycle $a \to b \to d \to a$, and $c$ is on the cycle $a \to c \to d \to a$, so the [Smith set](/smith-set/) is all four candidates and gives no help. Copeland's method separates $a$ and $b$, with two wins each, from $c$ and $d$, with one win each. It cannot separate $a$ from $b$, and the tie rule elects $a$. The Copeland ranking is $a, b, c, d$.

## Correctness

After line L1, $N[a][b] = n_P(a, b)$, because each ballot adds 1 to $N[a][b]$ exactly when it ranks $a$ above $b$. The loop of lines L3 to L5 visits each unordered pair once. For the pair $\{a, b\}$ it adds 1 to the score of the candidate that wins the pair and subtracts 1 from the score of the other, and it does nothing on a tie. So at the end, $s[a]$ is the number of wins of $a$ minus the number of its losses, which is $s_P(a)$. Line L6 builds $W(P)$, which is not empty, and line L7 returns its smallest element. The proof in `proofs/correctness.md` writes this out and proves the properties below.

## Complexity

Line L1 does $O(m^2)$ work for each ballot, since a ballot of $m$ candidates has $m(m - 1)/2$ ordered pairs, so it takes $O(n m^2)$ time. Lines L3 to L5 take $O(m^2)$ time and lines L6 and L7 take $O(m)$ time. The total is $O(n m^2)$ in the [word RAM](/word-ram/) model, and the extra space is the $m \times m$ matrix. When the pairwise matrix is given, the method takes $O(m^2)$ time, which is linear in the size of the majority graph; this is Theorem 3.2 of the chapter on tournament solutions in the Handbook of Computational Social Choice.

## Properties

The proofs are in `proofs/correctness.md`, and the tests check each property by brute force over all profiles with up to 4 candidates and few voters, and on random profiles with up to 6 candidates.

- **Anonymous, and neutral as a correspondence.** The counts $n_P(a, b)$ do not depend on the order of the voters, and renaming the candidates renames the scores. The resolute rule is not neutral, because of the tie rule.
- **Condorcet consistent.** A Condorcet winner scores $m - 1$, and every other candidate loses to it and so scores at most $m - 3$.
- **Smith consistent.** Every member of the [Smith set](/smith-set/) scores strictly more than every candidate outside it. So the winners are in the Smith set, and the Copeland ranking puts the Smith set first.
- **Pareto.** If every voter ranks $a$ above $b$, then $a$ beats $b$, and $a$ does at least as well as $b$ against every third candidate, so $s_P(a) > s_P(b)$.
- **Monotone.** Raising the winner $w$ on one ballot can only turn a loss of $w$ into a tie or a win, or a tie into a win. No other score goes up.
- **Not strategyproof.** With 3 candidates and 3 voters, some voter can get a better winner by a false ranking, as the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) says must happen for some profile.
- **Many ties.** When the number of voters is odd, the majority relation is a tournament, and with 4 candidates and no Condorcet winner the top two scores are always equal. The tie rule then decides the election.
- **Metric distortion 5.** When voters and candidates are points in a metric space, the winner's total distance to the voters is at most 5 times the best possible total (Anshelevich, Bhardwaj, Elkind, Postl and Skowron, 2018). See [metric distortion](/metric-distortion/).

## Variants and improvements

- **Copeland with a parameter for ties.** Copeland$^\alpha$ gives 1 point for a win and $\alpha$ points for a tie, with $0 \le \alpha \le 1$. The score of line L4 and line L5 is $2 \cdot$ Copeland$^{1/2} - (m - 1)$, so it orders the candidates as Copeland$^{1/2}$ does. Copeland$^1$ is the rule of Ramon Llull. The choice of $\alpha$ matters only when $n$ is even, and it changes the [control](/election-control-problem/) results for adding candidates (Faliszewski, Hemaspaandra, Hemaspaandra and Rothe, 2009).
- **Second-order Copeland.** Break ties by the sum of the Copeland scores of the candidates that each tied candidate beats. Bartholdi, Tovey and Trick (1989) proved that a manipulation by one voter is NP-hard to find for this version, while plain Copeland is easy to manipulate.
- **Margin-based rules.** [Ranked pairs](/ranked-pairs/) and the [Schulze method](/schulze-method/) also use the sizes of the majorities, so they have far fewer ties.
- **Slater and Kemeny.** The [Slater rule](/slater-rule/) looks for a ranking that disagrees with the fewest majority contests. Copeland's ranking is a fast heuristic for it.

## When to use it

Use Copeland's method when you want a Condorcet method that anyone can check with a table of head-to-head results, as in a sports league, or when you need a winner in the Smith set at a low cost. Add a tie-break rule that the voters accept, such as the Borda count or second-order Copeland, because with few candidates the top place is often shared. If the size of the majorities should count, use ranked pairs or the Schulze method.

## Pitfalls

- **An unstated tie rule.** Line L7 decides many elections. Return the set $W$ of line L6 when the caller must see the ties.
- **Counting only wins.** A score of wins alone is Copeland$^0$. It treats a tie like a loss, and when $n$ is even it can elect a different candidate than wins minus losses. Say which $\alpha$ the code uses.
- **Ties in the count.** A pair with $n_P(a, b) = n_P(b, a)$ is a tie, and it must not count as a win for the candidate that comes first in the loop.
- **Partial ballots.** If a ballot does not rank every candidate, decide whether a ranked candidate is above an unranked one. Line L1 assumes full rankings.

## Implementations

## History

Ramon Llull, in the 13th century, described an election in which each pair of candidates is compared and the candidate with the most pairwise wins is elected, which is Copeland$^1$. Condorcet in 1785 argued for the candidate who wins every pairwise contest. Arthur H. Copeland proposed the rule with wins minus losses in 1951, in mimeographed notes for a seminar at the University of Michigan. In computational social choice, Bartholdi, Tovey and Trick showed in 1989 that one voter can find a manipulation in polynomial time, and Faliszewski, Hemaspaandra, Hemaspaandra and Rothe showed in 2009 that the rule resists the standard types of constructive control.

## References
