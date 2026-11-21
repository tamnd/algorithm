---
tag: P7TC87
kind: algorithm
slug: instant-runoff-voting
name: Instant-runoff voting
aliases:
- IRV
- alternative vote
- ranked-choice voting
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: Repeatedly eliminates the candidate with the fewest first places and transfers its ballots until one candidate has a majority.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates, L: the total length of the ballots}
  time: {worst: O(L + m^2)}
  space: {extra: O(n + m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1871
  people: [Thomas Hare, William Robert Ware]
  note: "Hare's single transferable vote of the 1850s elects several members; the single-winner form is usually credited to W. R. Ware, about 1871."
prereqs: [preference-profile, plurality-voting]
see_also: [plurality-voting, single-transferable-vote, approval-voting, condorcet-winner, borda-count, gibbard-satterthwaite-theorem, voting-manipulation-problem, copeland-method]
sources:
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 2 (William S. Zwicker, Introduction to the theory of voting), Section 2.4 (Condorcet extensions, scoring rules and run-offs)"
  - paper: "Gideon Doron and Richard Kronick, Single transferable vote: an example of a perverse social choice function, American Journal of Political Science 21(2) (1977), 303-311"
    locator: the failure of monotonicity
  - paper: doi:10.1007/BF00183045
    title: "John J. Bartholdi III and James B. Orlin, Single transferable vote resists strategic voting, Social Choice and Welfare 8(4) (1991), 341-354"
    locator: the proof that it is NP-complete to decide whether a voter can manipulate the single-winner rule
---

Instant-runoff voting (IRV) is a single-winner voting rule on ranked ballots that eliminates candidates one at a time. In each round every ballot counts for its highest-ranked candidate that is still in the race; if one candidate has more than half of these ballots it wins, and otherwise the candidate with the fewest ballots is eliminated and its ballots move to their next choices. It is the single-winner case of the [single transferable vote](/single-transferable-vote/), and it is called the alternative vote in the United Kingdom and ranked-choice voting in the United States. It fixes the vote splitting of [plurality voting](/plurality-voting/) in many cases, but it is not monotone and it can eliminate the [Condorcet winner](/condorcet-winner/).

## In plain words

Each voter ranks the candidates from best to worst. First count only the top choices. If someone has more than half, that candidate wins. If not, drop the candidate with the fewest votes, and give each of its ballots to the next candidate on that ballot who is still in the race. Count again, and repeat until someone has more than half of the ballots that still count. It works like a series of runoff elections, but the voters vote only once.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and $n$ voters. Voter $i$ gives a ballot $r_i$, a sequence of distinct candidates, best first. A full ranking lists all $m$ candidates; a truncated ballot lists fewer, and it is exhausted when none of its candidates is still in the race. The input is the [preference profile](/preference-profile/) $P = (r_1, \ldots, r_n)$ and the output is one winner.

For a set $C$ of continuing candidates, a ballot counts for its first entry in $C$. Write $t_C(a)$ for the number of ballots that count for $a$, and $T_C = \sum_{a \in C} t_C(a)$ for the number of ballots that are not exhausted. The rule starts with $C = A$. If some $a \in C$ has $2 t_C(a) > T_C$, or $C = \{a\}$, it returns $a$. Otherwise it removes from $C$ the candidate with the smallest $t_C$. Among tied candidates it removes the one with the largest index, so that the smallest index wins a final tie, as on the other rule pages of this area.

## The algorithm

The direct method recounts every ballot in each round. The method below keeps, for each candidate, the pile of ballots that count for it, and a pointer into each ballot. When a candidate is eliminated, only the ballots on its pile move, and each pointer only moves forward.

```pseudo id=main
INSTANT-RUNOFF(P, m)                      ▷ P = (r_1, ..., r_n), each ballot best first
L1  C ← {0, ..., m - 1}; ptr[i] ← 1 for each voter i
L2  put each nonempty ballot i on pile[r_i[1]]
L3  loop
L4      T ← the sum of |pile[a]| over a in C   ▷ ballots that are not exhausted
L5      if some a in C has 2 |pile[a]| > T, or C = {a} then
L6          return a
L7      x ← the a in C with the smallest |pile[a]|; the largest index among ties
L8      C ← C \ {x}
L9      for each ballot i on pile[x] do
L10         advance ptr[i] to the next entry of r_i that is in C
L11         if ptr[i] is within r_i then put i on pile[r_i[ptr[i]]], else i is exhausted
```

Lines L1 and L2 do the first count. Each pass of the loop is one round: lines L4 to L6 test for a winner, lines L7 and L8 eliminate the weakest candidate, and lines L9 to L11 transfer its ballots. The code also returns the counts of every round, which is how results are usually published.

## Example

Take the nine voters of the [plurality voting](/plurality-voting/) page:

| voters | ranking |
|---|---|
| 4 | $a \succ b \succ c$ |
| 3 | $b \succ c \succ a$ |
| 2 | $c \succ b \succ a$ |

| round | $a$ | $b$ | $c$ | $T$ | action |
|---|---|---|---|---|---|
| 1 | 4 | 3 | 2 | 9 | no one has 5 or more; eliminate $c$, its 2 ballots go to $b$ |
| 2 | 4 | 5 | out | 9 | $b$ has 5 of 9 and wins |

Plurality elects $a$ here, which loses to both other candidates in pairs. IRV elects $b$, the Condorcet winner, because the $c$-voters' second choice now counts.

IRV can still miss the Condorcet winner. With 2 voters $a \succ b \succ c$, 1 voter $b \succ a \succ c$ and 2 voters $c \succ b \succ a$, the moderate $b$ beats $a$ by 3 to 2 and $c$ by 3 to 2, but it has the fewest first places. Round 1 has counts $(2, 1, 2)$ and eliminates $b$, and $a$ then wins by 3 to 2. This is the center squeeze.

Two more failures, both with no tie for last place in any round, show that more support can hurt a candidate:

- **Not monotone.** With 6 voters $a \succ b \succ c$, 2 voters $b \succ a \succ c$, 4 voters $b \succ c \succ a$ and 5 voters $c \succ a \succ b$, the first counts are $(6, 6, 5)$, $c$ is eliminated, and $a$ wins by 11 to 6. If the 2 voters $b \succ a \succ c$ move $a$ to the top, the counts are $(8, 4, 5)$, now $b$ is eliminated, its 4 ballots go to $c$, and $c$ wins by 9 to 8. The winner lost by gaining votes.
- **No-show paradox.** With 2 voters $a \succ c \succ b$, 4 voters $b \succ c \succ a$ and 3 voters $c \succ b \succ a$, $a$ is eliminated first and $c$ wins by 5 to 4. If 2 more voters $a \succ c \succ b$ come to vote, the counts are $(4, 4, 3)$, $c$ is eliminated, and $b$ wins by 7 to 4. The two new voters prefer $c$ to $b$, so they would do better to stay at home.

## Correctness

The method computes the rule of the problem section. The proof in `proofs/correctness.md` shows two invariants at line L4: the continuing set $C$ is the same as in the direct method, and for each $a \in C$, $pile[a]$ holds exactly the ballots that count for $a$, so $|pile[a]| = t_C(a)$ and $T = T_C$. The second invariant holds because a ballot counts for $a$ exactly when its pointer is at $a$; eliminating $x$ changes the count of a ballot only if that ballot was on $pile[x]$, and line L10 moves its pointer to the next entry in $C$.

The proof also shows that stopping at a majority in line L5 does not change the winner. If $2 t_C(a) > T_C$, every other candidate in $C$ has fewer ballots than $a$, so $a$ is never the one eliminated, and $t_C(a)$ never goes down as $C$ shrinks. Eliminating to the end would also elect $a$. The tests check the method against the direct recount, against elimination to the end, and on truncated ballots.

## Complexity

Lines L1 and L2 take $O(n + m)$ time. There are at most $m$ rounds, and lines L4 to L8 take $O(m)$ time per round, so $O(m^2)$ in total. In lines L9 to L11, every step of a pointer moves it forward in its ballot, and a ballot moves to a new pile only after such a step, so all transfers of the whole count take $O(n + L)$ time, where $L = \sum_i |r_i| \le n m$. The total is $O(L + m^2)$, which is $O(n m + m^2)$ for full rankings, linear in the input when $n \ge m$. The extra space is the $n$ pointers and the piles, which together hold each ballot once: $O(n + m)$. The direct recount costs $O(n m)$ per round and $O(n m^2)$ in total.

## Properties

The tests check each claim by brute force over all profiles of full rankings with 3 candidates and up to 5 voters, or 4 candidates and up to 3 voters, and find the counterexamples by search. The proofs of the positive claims are in `proofs/correctness.md`.

- **Anonymous.** The order of the voters does not matter.
- **Neutral, as a correspondence.** The set of candidates that win under some way of breaking elimination ties (parallel-universe tie-breaking) is renamed with the candidates. The resolute rule is not neutral, because of the tie-break by index.
- **Majority criterion.** A candidate ranked first by more than half of the voters wins in round 1.
- **Condorcet loser criterion.** With full rankings, IRV never elects a candidate that loses to every other candidate in pairs. In the last round only two candidates remain, so their counts are their pairwise counts, and an early stop needs a majority of first places.
- **Pareto.** With full rankings, a candidate $b$ that every voter ranks below some $a$ has no ballots while $a$ is in the race, and is eliminated before any candidate with ballots.
- **Not Condorcet consistent.** The center squeeze above is a counterexample.
- **Not monotone.** With 3 candidates, the smallest failure by one voter raising the winner one place has 7 voters and goes through a tie. Doron and Kronick (1977) described this failure for the single transferable vote.
- **Not participation-safe.** The no-show example above is a counterexample.
- **Manipulable, but hard to manipulate.** The search finds a profile with 3 candidates and 3 voters where one voter gains by a false ranking, as the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) predicts. Bartholdi and Orlin (1991) proved that it is NP-complete to decide whether a voter can make a given candidate win, so the [voting manipulation problem](/voting-manipulation-problem/) for IRV has no known polynomial-time algorithm.
- **Majority rule for 2 candidates.** With $m = 2$ the rule elects the majority winner, ties to candidate 0.

## Variants and improvements

- **Two-round system.** Eliminate all candidates except the top two at once, and hold a second election. It needs a second trip to the polls, and the voters can change their minds.
- **Contingent vote and supplementary vote.** One count, then all but the top two are eliminated and their ballots transferred. The supplementary vote limits each ballot to two choices.
- **Batch elimination.** Eliminate at once all candidates whose combined count is below the count of the next candidate. None of them can win, so the winner does not change, and the count is shorter.
- **Coombs' method.** Eliminate the candidate ranked last by the most voters, not the one with the fewest first places.
- **Baldwin's and Nanson's methods.** Eliminate by the [Borda count](/borda-count/): the candidate with the lowest score, or all candidates below the average. Both are Condorcet consistent.
- **Single transferable vote.** For $k$ seats, a candidate is elected when it reaches a quota, and its surplus ballots are transferred too. See [single transferable vote](/single-transferable-vote/).

## When to use it

Use IRV for a single-winner election with ranked ballots when you want the winner to have a majority of the ballots that still count in the last round, and you want to avoid a second trip to the polls. It removes most spoiler effects of [plurality voting](/plurality-voting/) when one or two minor candidates are far behind. If the main concern is to elect the candidate that beats every other in pairs, use a Condorcet method such as the [Copeland method](/copeland-method/) or [ranked pairs](/ranked-pairs/). If ballots must be simple, consider [approval voting](/approval-voting/).

## Pitfalls

- **Majority of what.** With truncated ballots, "more than half" can mean half of all ballots or half of the ballots that are not exhausted. When ballots are exhausted, the first rule can find no majority and must go on to the last two candidates, while the second rule stops earlier. If the first rule then eliminates to the end, the two rules elect the same candidate, but the published rounds differ. This page uses the continuing ballots; state which rule you use.
- **The elimination tie rule.** A tie for last place decides who is eliminated and can decide the winner. Laws often use earlier rounds or a lot. Fix the rule and test it; a scan that keeps the first minimum and one that keeps the last minimum can give different winners on the same profile.
- **Recounting from scratch.** Recounting all ballots in each round costs $O(n m^2)$. With piles and pointers the work is $O(n m + m^2)$.
- **Skipping eliminated candidates once.** When a ballot moves, its next choice may already be eliminated. Line L10 must skip every eliminated candidate, not just one.
- **The name ranked-choice voting.** In the United States it means IRV, but it is also used for the single transferable vote and for any rule on ranked ballots. Say which rule you mean.

## Implementations

## History

Thomas Hare in Britain and Carl Andrae in Denmark devised the single transferable vote in the 1850s, as a rule to elect several members. The single-winner form, in which a candidate is elected by a majority and the weakest is eliminated, is usually credited to the American architect William Robert Ware, about 1871. Australia has used it for its House of Representatives since 1918, Ireland uses it to elect its president, and the American state of Maine first used it in 2018. Doron and Kronick (1977) showed that the rule is not monotone, and Bartholdi and Orlin (1991) showed that manipulating it is NP-complete, a first example of computational hardness as a barrier to strategic voting.

## References
