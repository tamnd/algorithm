---
tag: WM09B3
kind: algorithm
slug: plurality-voting
name: Plurality voting
aliases:
- first past the post
- relative majority
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: Elects the candidate ranked first by the most voters. It ignores all but the top choice of each voter.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(n + m)}
  space: {extra: O(m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1784
  people: [Jean-Charles de Borda, Allan Gibbard, Mark Satterthwaite]
  note: "Borda showed that plurality can elect a candidate whom a majority ranks last; Gibbard and Satterthwaite proved in 1973 and 1975 that it can be manipulated, like every onto nondictatorial rule."
prereqs: [preference-profile]
see_also: [instant-runoff-voting, approval-voting, borda-count, condorcet-winner, gibbard-satterthwaite-theorem, may-theorem, single-transferable-vote, kemeny-rank-aggregation]
sources:
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 2 (William S. Zwicker, Introduction to the theory of voting), Section 2.2 (plurality, Copeland and Borda) and Section 2.4 (scoring rules and runoffs)"
  - paper: doi:10.1137/0128067
    title: "H. P. Young, Social choice scoring functions, SIAM Journal on Applied Mathematics 28(4) (1975), 824-838"
    locator: "the characterization of the scoring rules, of which plurality is one, by consistency with anonymity, neutrality and a continuity condition"
  - paper: "Jean-Charles de Borda, Mémoire sur les élections au scrutin, Histoire de l'Académie Royale des Sciences, année 1781 (printed 1784), 657-665"
    locator: the argument that plurality can elect a candidate whom a majority ranks last
  - paper: doi:10.2307/1914083
    title: "Allan Gibbard, Manipulation of voting schemes, a general result, Econometrica 41(4) (1973), 587-601"
    locator: "the main theorem, which applies to plurality with three or more candidates"
---

Plurality voting elects the candidate that the most voters rank first. It reads only the top entry of each ballot in a [preference profile](/preference-profile/), counts the first places of each candidate, and breaks a tie by a fixed rule. It is the rule of most single-member elections in the United Kingdom, the United States, Canada and India, where it is called "first past the post". It is the fastest rule there is, but it can elect a candidate that a majority of the voters ranks last, and it rewards voters who do not vote for their true first choice.

## In plain words

Each voter names one favourite. The candidate with the most votes wins, even when that is far less than half of the votes. A ballot says nothing about the second choice, so the rule cannot see that most voters may dislike the winner. When two similar candidates split the votes of their supporters, a third candidate that most voters like less can win. Voters know this, so many of them vote for the strongest candidate they can accept, and not for the one they like best.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and $n$ voters. Voter $i$ has a ranking $r_i$ of all candidates, a tuple with the best candidate first, and the input is the profile $P = (r_1, \ldots, r_n)$. The output is one winner in $A$. The plurality score of a candidate $a$ is

$$s_P(a) = |\{ i : r_i[1] = a \}|,$$

the number of voters who rank $a$ first. The plurality correspondence returns the set $W(P) = \arg\max_a s_P(a)$, and the resolute rule returns one element of it. Ties go to the candidate with the smallest index, as on every rule page of this area. In practice a ballot names only one candidate, and the code needs only that entry.

## The algorithm

```pseudo id=main
PLURALITY(P, m)                           ▷ P = (r_1, ..., r_n), each ranking best first
L1  s[a] ← 0 for each candidate a = 0, ..., m - 1
L2  for each ranking r in P do
L3      s[r[1]] ← s[r[1]] + 1             ▷ only the top entry is read
L4  best ← max over a of s[a]
L5  W ← {a : s[a] = best}                 ▷ the plurality correspondence
L6  return the smallest candidate in W    ▷ the fixed tie-breaking rule
```

Lines L1 to L3 are a counting pass: one counter per candidate, and one increment per voter. Lines L4 and L5 find all candidates with the highest count. Line L6 applies the tie-breaking rule. The code returns $W$ from a separate function, because the properties of the rule are cleaner on the correspondence: the tie-break by index favours candidate 0, so the resolute rule is not neutral, while the correspondence is.

## Example

Take three candidates $a, b, c$ (indices 0, 1, 2) and nine voters:

| voters | ranking |
|---|---|
| 4 | $a \succ b \succ c$ |
| 3 | $b \succ c \succ a$ |
| 2 | $c \succ b \succ a$ |

| step | state |
|---|---|
| L1 | $s = (0, 0, 0)$ |
| L2 to L3, the 4 voters $a \succ b \succ c$ | $s = (4, 0, 0)$ |
| L2 to L3, the 3 voters $b \succ c \succ a$ | $s = (4, 3, 0)$ |
| L2 to L3, the 2 voters $c \succ b \succ a$ | $s = (4, 3, 2)$ |
| L4 and L5 | $best = 4$, $W = \{a\}$ |
| L6 | return $a$ |

The winner $a$ has 4 of the 9 votes, less than half. The pairwise counts show what the ballots hide: $b$ beats $a$ by 5 to 4 and beats $c$ by 7 to 2, so $b$ is the [Condorcet winner](/condorcet-winner/), and $a$ loses to both $b$ and $c$ by 5 to 4, so $a$ is the Condorcet loser. The [Borda count](/borda-count/) gives $a$, $b$ and $c$ the scores 8, 12 and 7, and [instant-runoff voting](/instant-runoff-voting/) removes $c$ and then elects $b$ by 5 to 4. The two voters $c \succ b \succ a$ can change the result: if they report $b \succ c \succ a$, the scores become $(4, 5, 0)$ and $b$ wins, which they prefer to $a$.

With three candidates, a Condorcet loser can win alone, with no tie, only when there are 7 or more voters; the smallest case is 3 voters $a \succ b \succ c$, 2 voters $b \succ c \succ a$ and 2 voters $c \succ b \succ a$. With the tie-break, 3 voters suffice: the ballots $a \succ b \succ c$, $b \succ c \succ a$ and $c \succ b \succ a$ give one first place to each candidate, and the tie goes to $a$, which loses to $b$ and to $c$ by 2 to 1.

## Correctness

After the loop of lines L2 and L3 has read the first $k$ ballots, $s[a]$ is the number of these ballots with $a$ on top, for every $a$. This [loop invariant](/loop-invariant/) holds at the start, where all counters are 0, and each pass adds 1 to exactly one counter, the one of the top of the new ballot. At the end $s[a] = s_P(a)$, so line L5 builds $W(P)$ and line L6 returns its smallest element. The proof in `proofs/correctness.md` also proves the properties below.

## Complexity

Line L1 takes $O(m)$ time. The loop runs $n$ times, and each pass reads one entry and does one increment, so it takes $O(n)$ time when a ballot gives random access to its first entry. Lines L4 to L6 each take $O(m)$ time. The total is $O(n + m)$ in the [word RAM](/word-ram/) model, with counters of $O(\log n)$ bits, and the extra space is the $m$ counters. If the input is a full profile, it has $n m$ entries, but the rule never reads more than $n$ of them. No algorithm can do better than $\Omega(n)$ when $m \ge 2$, since any ballot that it does not read could change the winner.

## Properties

These hold for every number of candidates. The proofs are in `proofs/correctness.md`, and the tests check each one by brute force over all profiles with up to 4 candidates and few voters.

- **Anonymous.** Reordering the voters does not change any score.
- **Neutral, as a correspondence.** Renaming the candidates renames the scores and the set $W$. The resolute rule is not neutral: with one voter $a \succ b$ and one voter $b \succ a$, it elects $a$, and after the swap of the names it still elects $a$.
- **Pareto.** If every voter ranks $a$ above $b$, then no voter ranks $b$ first, so $s_P(b) = 0$, while the winner has at least $n/m > 0$ first places. So $b$ does not win when $n \ge 1$.
- **Monotone.** Raising the winner $w$ on one ballot either leaves all scores the same or moves one first place to $w$. Both keep $w$ in $W$ and keep it the smallest maximizer, since no other score goes up.
- **Consistent.** If two disjoint groups of voters have winner sets $W_1$ and $W_2$ with $W_1 \cap W_2 \neq \emptyset$, then the combined group has winner set $W_1 \cap W_2$, because the scores add. This is the consistency (reinforcement) axiom, and Young (1975) proved that, with anonymity, neutrality and a continuity condition, it characterizes the scoring rules, of which plurality is the simplest.
- **Not Condorcet consistent, and it can elect the Condorcet loser.** The example shows both failures.
- **Not strategyproof for 3 or more candidates.** The example shows a manipulation by the two voters $c \succ b \succ a$. This is forced by the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/): plurality is onto and not a dictatorship, so some profile has a profitable false ballot.
- **Majority rule for 2 candidates.** With $m = 2$ the plurality winner is the majority winner, and the rule is then strategyproof and Condorcet consistent. [May's theorem](/may-theorem/) characterizes it there.

## Variants and improvements

- **Plurality with runoff.** If no candidate has more than half of the votes, hold a second round between the top two. The two-round system of French presidential elections works this way. It is still not Condorcet consistent, and it is not monotone.
- **Instant-runoff voting.** Ask for full rankings and remove the weakest candidate one at a time. See [instant-runoff voting](/instant-runoff-voting/).
- **Approval voting.** Let each voter approve any set of candidates. See [approval voting](/approval-voting/).
- **Other scoring rules.** Plurality gives 1 point to the top place and 0 to the others. The [Borda count](/borda-count/) gives $m - j$ points to place $j$, $k$-approval gives 1 point to each of the top $k$ places, and the veto rule (anti-plurality) gives 1 point to every place except the last. All of them are consistent, and none of them is Condorcet consistent.
- **Multiwinner forms.** Single non-transferable vote and block voting elect the $k$ candidates with the most votes. The [single transferable vote](/single-transferable-vote/) is the proportional form.

## When to use it

Use plurality when ballots must be as simple as possible, the count must be done by hand or explained in one sentence, and the field has two strong candidates. Then the rule is almost majority rule. With three or more serious candidates, especially when two of them split one group of voters, use a rule that reads more of each ranking: [instant-runoff voting](/instant-runoff-voting/) if you want a majority in the last round, a Condorcet method such as the [Copeland method](/copeland-method/) or [ranked pairs](/ranked-pairs/) if you want the pairwise winner, or [approval voting](/approval-voting/) if you want a simple ballot that is safe for sincere voters.

## Pitfalls

- **An unstated tie rule.** Line L6 is part of the rule. Python's `max(range(m), key=s.__getitem__)` returns the first maximizer, which is the smallest index here, but `max` over a dictionary depends on the insertion order. State the rule, and return the set $W$ of line L5 when the caller must see the ties.
- **Plurality is not majority.** In the example the winner has 4 of 9 votes. Code that checks "more than half" to decide the winner implements a different rule, one that can return no winner.
- **Reading the wrong entry.** In line L3 the top of the ballot is `r[0]` in 0-based code. A ballot stored as a position vector (the place of each candidate) and not as a ranking gives wrong counts without any error.
- **Percentages in floating point.** Compare the integer counts of line L4, not shares such as $s[a]/n$, where two equal counts can give shares that differ in the last bit after other arithmetic.

## Implementations

## History

Plurality is the oldest and most common rule for elections. Borda, in a memoir printed in 1784, argued that it can elect a candidate whom a majority ranks last, and proposed his scoring rule in its place. Condorcet answered with the pairwise majority test. Gibbard (1973) and Satterthwaite (1975) proved that every onto rule with three or more possible winners that is not a dictatorship can be manipulated, so the strategic voting that plurality invites is not a defect of this rule alone. Young (1975) placed plurality in the family of scoring rules by the consistency axiom.

## References
