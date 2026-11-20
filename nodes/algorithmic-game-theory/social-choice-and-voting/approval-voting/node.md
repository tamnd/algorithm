---
tag: 2YTCNT
kind: algorithm
slug: approval-voting
name: Approval voting
aliases:
- approval ballot
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: Each voter approves any set of candidates, and the candidate with the most approvals wins.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates, L: the total number of approvals on all ballots}
  time: {worst: O(n + m + L)}
  space: {extra: O(m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1978
  people: [Steven J. Brams, Peter C. Fishburn]
  note: "Brams and Fishburn gave the first full analysis of approval voting, including the result that sincere approval is a dominant strategy for dichotomous preferences."
prereqs: [preference-profile]
see_also: [plurality-voting, instant-runoff-voting, borda-count, condorcet-winner, gibbard-satterthwaite-theorem, proportional-approval-voting, justified-representation, dominant-strategy]
sources:
  - paper: doi:10.2307/1955105
    title: "Steven J. Brams and Peter C. Fishburn, Approval voting, American Political Science Review 72(3) (1978), 831-847"
    locator: "the definition, the admissible and sincere strategies, and the dominance of sincere voting for dichotomous preferences"
  - paper: doi:10.1007/s00355-005-0013-y
    title: "Steven J. Brams and Peter C. Fishburn, Going from theory to practice: the mixed success of approval voting, Social Choice and Welfare 25(2-3) (2005), 457-474"
    locator: the use of approval voting by scientific societies and the reasons some of them dropped it
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 2 (William S. Zwicker, Introduction to the theory of voting)"
---

Approval voting is a single-winner voting rule in which each voter approves any set of candidates and the candidate with the most approvals wins. The ballot is a set, not a ranking, so the rule sits between [plurality voting](/plurality-voting/), where each voter approves exactly one candidate, and the rules that read a full [preference profile](/preference-profile/). The count is one pass over the ballots, and the rule is anonymous, neutral, monotone and consistent. Its main strength is strategic: a voter who only separates good candidates from bad ones can never gain by a false ballot.

## In plain words

Each voter marks every candidate that they find acceptable, one or many. A mark counts once, and the candidate with the most marks wins. A voter who likes two similar candidates can mark both, so the two do not split the votes of their supporters as they do under plurality. The hard choice for a voter is where to put the line: marking a second choice helps it against worse candidates, but it can also help it beat the first choice.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and $n$ voters. Voter $i$ casts a ballot $S_i \subseteq A$, the set of candidates that voter $i$ approves; the empty ballot and the full ballot are allowed. The input is the approval profile $(S_1, \ldots, S_n)$, and the output is one winner. The approval score of a candidate $a$ is

$$s(a) = |\{ i : a \in S_i \}|,$$

the approval correspondence returns $W = \arg\max_a s(a)$, and the resolute rule returns the smallest index in $W$, the fixed tie-breaking rule of this area.

When the voters also have rankings, a ballot $S$ is called sincere for a ranking $r$ if every approved candidate is ranked above every candidate that is not approved, that is, if $S$ is a set of the top $k$ candidates of $r$ for some $k$. The model of voter behaviour is then part of the rule: the same rankings can give different winners for different choices of $k$.

## The algorithm

```pseudo id=main
APPROVAL(S_1, ..., S_n, m)                ▷ each S_i is a set of candidates
L1  s[a] ← 0 for each candidate a = 0, ..., m - 1
L2  for each ballot S in S_1, ..., S_n do
L3      for each candidate a in S do
L4          s[a] ← s[a] + 1
L5  best ← max over a of s[a]
L6  W ← {a : s[a] = best}                 ▷ the approval correspondence
L7  return the smallest candidate in W    ▷ the fixed tie-breaking rule
```

Lines L1 to L4 count, for each candidate, the ballots that contain it. Lines L5 and L6 find all candidates with the highest count, and line L7 applies the tie-breaking rule. The code also returns $W$ from a separate function, because the resolute rule with a tie-break by index is not neutral, while the correspondence is.

## Example

Take the nine voters of the [plurality voting](/plurality-voting/) page and let each approve the candidates before the bar: 4 voters with ranking $a \succ b \succ c$ approve $\{a\}$, 3 voters with ranking $b \succ c \succ a$ approve $\{b\}$, and 2 voters with ranking $c \succ b \succ a$ approve $\{c, b\}$.

| step | state |
|---|---|
| L1 | $s = (0, 0, 0)$ |
| L2 to L4, the 4 ballots $\{a\}$ | $s = (4, 0, 0)$ |
| L2 to L4, the 3 ballots $\{b\}$ | $s = (4, 3, 0)$ |
| L2 to L4, the 2 ballots $\{c, b\}$ | $s = (4, 5, 2)$ |
| L5 and L6 | $best = 5$, $W = \{b\}$ |
| L7 | return $b$ |

Plurality elects $a$ on these voters, which is the Condorcet loser, while approval elects $b$, the [Condorcet winner](/condorcet-winner/). The two $c$-voters did not have to desert $c$ to help $b$.

Approval voting is still not Condorcet consistent. Let 3 voters with ranking $a \succ b \succ c$ approve $\{a, b\}$ and 2 voters with ranking $b \succ a \succ c$ approve $\{b\}$. Then $s = (3, 5, 0)$ and $b$ wins, but $a$ beats $b$ on 3 of the 5 rankings and is the Condorcet winner. If the three $a$-voters approve only $\{a\}$, then $a$ wins by 3 to 2. Both ballots are sincere for these voters, and the result depends on where they put the line.

## Correctness

After the loop has read the first $k$ ballots, $s[a]$ is the number of these ballots that contain $a$, for every $a$. This [loop invariant](/loop-invariant/) holds for $k = 0$ by line L1, and the inner loop of lines L3 and L4 adds 1 to the counter of each member of the new ballot and to no other counter. At the end $s[a] = s(a)$, line L6 builds $W$, and line L7 returns its smallest element. The proof in `proofs/correctness.md` also proves the properties below.

## Complexity

Line L1 takes $O(m)$ time. The outer loop runs $n$ times, and the inner loop runs once per approval, so lines L2 to L4 take $O(n + L)$ time, where $L = \sum_i |S_i| \le n m$. Lines L5 to L7 take $O(m)$ time. The total is $O(n + m + L)$ in the [word RAM](/word-ram/) model, and the extra space is the $m$ counters. If ballots are stored as bit vectors of length $m$, the scan costs $O(n m)$ instead.

## Properties

The proofs are in `proofs/correctness.md`, and the tests check each one by brute force over all approval profiles with 3 or 4 candidates and 2 or 3 voters.

- **Anonymous** and **neutral as a correspondence.** The resolute rule is not neutral, because of the tie-break by index.
- **Pareto, in the approval sense.** If the voters who approve $b$ form a strict subset of the voters who approve $a$, then $s(b) < s(a)$ and $b$ does not win.
- **Monotone.** Adding the winner to one more ballot keeps it the winner.
- **Consistent.** If two disjoint groups have winner sets with a common member, the joined group elects exactly the common members, because the scores add.
- **Sincere voting is dominant for dichotomous preferences.** A voter who only cares whether the winner is in a set $G$ cannot do better than the ballot $G$, whatever the other voters do (Brams and Fishburn 1978). This holds with the fixed tie-break too.
- **No dominant ballot for general preferences.** With 3 candidates and a ranking $a \succ b \succ c$, the only ballots that no other ballot dominates are $\{a\}$ and $\{a, b\}$, and neither one dominates the other. With 4 candidates the insincere ballot $\{a, c\}$ is also undominated. This agrees with Gibbard's theorem for general game forms, of which the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) is the special case for ranking ballots.
- **Not Condorcet consistent,** as the second example shows.
- **Plurality as a special case.** If every voter approves exactly one candidate, approval voting is plurality voting.

## Variants and improvements

- **$k$-approval.** Each voter must approve exactly $k$ candidates. This is a scoring rule on rankings and loses the free choice of the line.
- **Score and range voting.** Each voter gives every candidate a grade from a fixed scale, and the highest total or mean wins. Approval voting is the case of two grades.
- **Satisfaction approval voting.** A ballot that approves $k$ candidates gives $1/k$ to each, so every voter has the same total weight.
- **Multiwinner forms.** To elect a committee of $k$ members from approval ballots, [proportional approval voting](/proportional-approval-voting/) and the rules studied under [justified representation](/justified-representation/) give groups of voters a fair share of the seats. Taking the $k$ candidates with the most approvals does not.
- **Fallback and runoff forms.** An approval round can pick the top two for a runoff, as in the two-round system of [plurality voting](/plurality-voting/).

## When to use it

Use approval voting for a single winner when ballots must stay simple, there are several similar candidates, and vote splitting would harm the result under [plurality voting](/plurality-voting/). It suits committees, societies and straw polls in which voters can tell acceptable from unacceptable candidates. If voters have strong rankings and you want a pairwise majority winner, use a Condorcet method such as the [Copeland method](/copeland-method/) or [ranked pairs](/ranked-pairs/). If you want a majority of the remaining ballots in a last round, use [instant-runoff voting](/instant-runoff-voting/).

## Pitfalls

- **Counting an approval twice.** Store each ballot as a set. A list that repeats a candidate gives that candidate an extra point.
- **Reading a ranking as an approval ballot.** A ranking says nothing about where the line is. Converting rankings into ballots needs an explicit threshold, and the result depends on it, as the second example shows.
- **Taking the top $k$ for a committee.** With $k$ seats, the $k$ candidates with the most approvals can all come from one majority group, and a large minority gets nothing.
- **Bullet voting.** Voters who fear that a second approval will beat their first choice approve one candidate only. If most voters do this, the rule is plurality again.

## Implementations

## History

Several authors studied approval voting in the 1970s, and Brams and Fishburn (1978) gave the first full analysis of its strategic properties. Scientific societies such as the Mathematical Association of America and the Institute of Electrical and Electronics Engineers took it up for their elections in the following years, and some of them, the IEEE among them, later dropped it; Brams and Fishburn (2005) review this record. In public elections, Fargo, North Dakota, adopted approval voting for city elections by a referendum in 2018, and St. Louis adopted it for the primary round of its city elections in 2020.

## References
