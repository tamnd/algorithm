---
tag: CH8C0N
kind: algorithm
slug: single-transferable-vote
name: Single transferable vote
aliases:
- STV
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Elects a committee from ranked ballots by quota, transferring surplus votes of elected candidates and votes of eliminated ones.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates, k: the number of seats, L: the total length of the ballots}
  time: {worst: O(L + m^2)}
  space: {extra: O(n + m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1857
  people: [Carl Andrae, Thomas Hare, Henry Richmond Droop]
  note: "Andrae proposed a similar rule in Denmark in 1855; Hare published his in 1857 and 1859; Droop argued for the quota floor(V/(k+1)) + 1 in 1881."
prereqs: [preference-profile, instant-runoff-voting]
see_also: [instant-runoff-voting, apportionment-problem, dhondt-method, proportional-approval-voting, justified-representation, chamberlin-courant-rule, voting-manipulation-problem, plurality-voting]
sources:
  - paper: doi:10.1257/jep.9.1.27
    title: "Nicolaus Tideman, The single transferable vote, Journal of Economic Perspectives 9(1) (1995), 27-38"
    locator: "the rules of the count, the quotas and the transfer of surpluses; footnote 1 for proportionality for solid coalitions, after Dummett (1984)"
  - paper: doi:10.2307/2339223
    title: "H. R. Droop, On methods of electing representatives, Journal of the Statistical Society of London 44(2) (1881), 141-202"
    locator: the argument for the quota that carries his name
  - paper: doi:10.1007/BF00183045
    title: "John J. Bartholdi III and James B. Orlin, Single transferable vote resists strategic voting, Social Choice and Welfare 8(4) (1991), 341-354"
    locator: the proof that it is NP-complete to decide whether a voter can manipulate the rule
---

The single transferable vote (STV) elects a committee of $k$ members from ranked ballots. A candidate is elected when its tally reaches a quota, and its surplus above the quota moves on to the next choices of its voters. When nobody reaches the quota, the weakest candidate is eliminated and its ballots move on. With one seat it is [instant-runoff voting](/instant-runoff-voting/); with more seats it gives each large enough group of like-minded voters a share of the seats. It uses quotas, but it is a voting rule on ballots, not an [apportionment](/apportionment-problem/) method for parties.

## In plain words

Each voter ranks the candidates. A candidate needs a fixed number of votes, the quota, to win a seat. Count the first choices. If a candidate has the quota or more, it wins, and the votes it does not need are passed on to the next choices on its ballots, each ballot at a reduced value. If nobody has the quota, the candidate with the fewest votes drops out, and its ballots go to their next choices at full value. Repeat until all seats are filled. Few votes are wasted: a vote helps elect one candidate, or it moves on.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$, $n$ voters and $k \ge 1$ seats. Voter $i$ gives a ballot $r_i$, a sequence of distinct candidates, best first, which may be truncated. The input is the [preference profile](/preference-profile/) $P = (r_1, \ldots, r_n)$ and $k$; the output is a list $W$ of $\min(k, m)$ winners, in the order of election.

Let $V$ be the number of nonempty ballots. The Droop quota is $q = \lfloor V/(k + 1) \rfloor + 1$, the smallest whole number such that no $k + 1$ candidates can all reach it. The Hare quota is $q = V/k$. Each ballot has a weight $w_i$, at first 1, and counts for its first candidate that is still continuing. The tally $t(a)$ is the sum of the weights of the ballots that count for $a$.

The rule of this page moves surpluses by the inclusive Gregory method: when $e$ is elected with $t(e) \ge q$, every ballot that counts for $e$ moves on with its weight multiplied by $f = (t(e) - q)/t(e)$. Ties are broken by index: the largest tally is elected with the smallest index among ties, and the smallest tally is eliminated with the largest index among ties, as on the instant-runoff page. When the continuing candidates are no more than the empty seats, they are all elected.

## The algorithm

As in instant-runoff voting, each candidate has a pile of the ballots that count for it, and each ballot has a pointer to its current entry. MOVE$(i)$ advances the pointer of ballot $i$ to its next entry that is still in $C$, puts $i$ on that pile and adds $w_i$ to that tally. If there is no such entry, the ballot is exhausted.

```pseudo id=main
SINGLE-TRANSFERABLE-VOTE(P, m, k)         ▷ P = (r_1, ..., r_n), each ballot best first
L1  V ← the number of nonempty ballots; q ← ⌊V/(k + 1)⌋ + 1
L2  C ← {0, ..., m - 1}; W ← empty list; w[i] ← 1 and ptr[i] ← 1 for each ballot i
L3  put each nonempty ballot i on pile[r_i[1]]; t(a) ← the sum of w[i] over pile[a]
L4  while |W| < k and C is not empty do
L5      if |C| ≤ k - |W| then
L6          append C to W by decreasing t, then by index; return W
L7      e ← the a in C with the largest t(a), the smallest index among ties; if t(e) ≥ q then
L8          C ← C \ {e}; append e to W
L9          f ← (t(e) - q) / t(e)
L10         for each ballot i on pile[e] do w[i] ← f · w[i]; MOVE(i)
L11     else x ← the a in C with the smallest t(a), the largest index among ties
L12         C ← C \ {x}
L13         for each ballot i on pile[x] do MOVE(i)
L14 return W
```

Lines L1 to L3 compute the quota and do the first count. Each pass of the loop is one round: line L5 fills the last seats when no choice is left, lines L7 to L10 elect a candidate and pass on its surplus, and lines L11 to L13 eliminate a candidate and pass on its ballots at full weight. All weights are exact fractions. The code also returns a log of the tallies of every round, which is how counts are published. With the Hare quota and no ballots, $q = 0$, so the code also asks $t(e) > 0$ on line L7.

## Example

Five candidates $a, b, c, d, e$ and 20 ballots compete for $k = 3$ seats, so $q = \lfloor 20/4 \rfloor + 1 = 6$.

| ballots | ranking |
|---|---|
| 9 | $a \succ b$ |
| 2 | $b \succ a$ |
| 4 | $c \succ d$ |
| 3 | $d \succ c$ |
| 2 | $e \succ d$ |

| round | $a$ | $b$ | $c$ | $d$ | $e$ | action |
|---|---|---|---|---|---|---|
| 1 | 9 | 2 | 4 | 3 | 2 | elect $a$; $f = 3/9 = 1/3$ |
| 2 | | 5 | 4 | 3 | 2 | eliminate $e$ |
| 3 | | 5 | 4 | 5 | | eliminate $c$ |
| 4 | | 5 | | 9 | | 2 left for 2 seats: elect $d$, then $b$ |

In round 1, $a$ has $9 \ge 6$ and is elected. Its surplus is $3$, so each of its 9 ballots moves to $b$ with weight $1/3$, and $b$ gets $2 + 3 = 5$. In round 2 nobody has 6, and $e$ has the fewest votes; its 2 ballots go to $d$. In round 3, $c$ is eliminated and its 4 ballots go to $d$. Then two candidates are left for two seats. The committee is $\{a, b, d\}$. The 11 voters of the $a$ and $b$ group get two seats and the 9 voters of the $c$, $d$ and $e$ group get one. If the three candidates with the most first choices won, the committee would be $\{a, c, d\}$, and the larger group would get only one seat.

## Correctness

The [proof](proofs/correctness.md) shows four things. The piles and pointers give the same tallies as a recount of all ballots in each round, because a ballot that counts for a continuing candidate keeps counting for it. The rule returns $\min(k, m)$ distinct winners. Votes are conserved: the continuing tallies, $q$ for each candidate elected by quota, and the weight of the exhausted ballots always sum to $V$, so each candidate elected by quota keeps exactly $q$ votes. And the rule has proportionality for solid coalitions: if at least $j q$ voters rank all members of a set $S$ above everyone else, with $j \le \min(k, |S|)$, then at least $j$ members of $S$ are elected. The proof of the last fact uses only conservation and $(k + 1) q > V$, which holds for both quotas.

## Complexity

Let $L$ be the total length of the ballots. Each move advances a pointer, so all moves together take $O(L)$ steps. There are at most $m$ rounds, and each one finds a largest and a smallest tally in $O(m)$ time. The total is $O(L + m^2)$ arithmetic operations and $O(n + m)$ extra space, besides the ballots. The weights are fractions, and each surplus transfer multiplies some of them by a new factor, so their bit length can grow with the number of transfers. Counting rules used in practice round the weights to a fixed number of decimals, which keeps every operation $O(1)$ on a word RAM at the cost of small errors.

## Properties

- **Proportionality for solid coalitions.** As stated above. With the Droop quota, a group of more than $V/(k + 1)$ voters who agree on the top of their ballots is sure of a seat. This is the reason the Droop quota is used.
- **One seat.** With $k = 1$ the Droop quota is a majority of all ballots, and the rule elects the winner of [instant-runoff voting](/instant-runoff-voting/).
- **Not monotone.** It inherits this from instant-runoff voting. With 6 ballots $a \succ b \succ c$, 2 ballots $b \succ a \succ c$, 4 ballots $b \succ c \succ a$, 5 ballots $c \succ a \succ b$ and one seat, $c$ is eliminated and $a$ wins. If the 2 voters of $b \succ a \succ c$ move $a$ to the top, $b$ is eliminated, its 4 ballots go to $c$, and $c$ wins.
- **Anonymity.** Only the multiset of ballots matters. The tie rule by index makes it not neutral in ties.
- **Manipulation.** It is NP-complete to decide whether one voter can make a given candidate win by a false ballot (Bartholdi and Orlin 1991). See the [voting manipulation problem](/voting-manipulation-problem/).
- **No Condorcet guarantee.** Like instant-runoff voting, it can eliminate a candidate that beats every other in pairs.

## Variants and improvements

- **The quota.** The Hare quota $V/k$ is larger. It can change who gets a surplus and so the result. With the 8 ballots $0 \succ 1 \succ 3 \succ 2$, $0 \succ 3 \succ 1 \succ 2$, $1 \succ 0 \succ 3 \succ 2$, $2 \succ 0 \succ 3 \succ 1$, twice $2 \succ 1 \succ 0 \succ 3$ and twice $2 \succ 1 \succ 3 \succ 0$, and $k = 2$, the Droop quota 3 elects 2 and then 1, and the Hare quota 4 elects 2 and then 0.
- **The surplus rule.** The inclusive Gregory method moves all ballots of the elected candidate at a reduced weight. The last-parcel rule moves only the ballots that arrived last. Some laws, as in Ireland, move whole ballots taken from the pile, so the choice of ballots can change the result. The weighted inclusive Gregory method, used for Scottish local elections, takes the weight of each ballot into account, as this page does.
- **Meek's method.** Elected candidates keep exactly $q$ by an iteration over keep factors, and eliminated or elected candidates are skipped on every ballot, also on ballots that moved before. The quota is computed again as ballots become exhausted. It needs a computer.
- **Other proportional rules.** For approval ballots, [proportional approval voting](/proportional-approval-voting/), [Phragmen's sequential method](/phragmen-sequential-method/) and the [method of equal shares](/method-of-equal-shares/) give proportionality in the sense of [justified representation](/justified-representation/). For party lists, use an apportionment method such as the [D'Hondt method](/dhondt-method/).

## When to use it

Use STV to elect several members from one district when voters rank candidates and you want proportional results without parties or lists. Groups of voters get seats in proportion to their size, and voters can rank across party lines. It needs ranked ballots and a central count, and the count is hard to check by hand when surpluses are fractional. For a single seat, use [instant-runoff voting](/instant-runoff-voting/) or a Condorcet method. If the goal is a committee that represents every voter by one member, see the [Chamberlin-Courant rule](/chamberlin-courant-rule/).

## Pitfalls

- **Which quota.** The integer Droop quota, the exact Droop quota $V/(k + 1)$ and the Hare quota give different counts. With the exact quota $V/(k + 1)$, $k + 1$ candidates can all reach it. State the quota.
- **Count the transfer weight, not the ballots.** A ballot that moved from a surplus has a weight below 1. A count of ballots instead of weights gives wrong tallies in the later rounds.
- **Exhausted ballots.** With truncated ballots, the tallies can sum to less than $k q$, and no one may reach the quota. Line L5 then fills the last seats with the continuing candidates. Without it, the count can stop with empty seats.
- **Ties.** The order of elections and the elimination ties can decide seats. Laws often look at earlier rounds or draw lots. Fix the rule and test it.
- **Rounding.** Exact fractions grow. If the law rounds weights to a fixed number of decimals, do the same, and do it at the step the law gives, or the published counts will not match.

## Implementations

## History

Carl Andrae proposed a rule of this kind in Denmark in 1855, and Thomas Hare published his in Britain in 1857 and 1859, with the quota $V/k$. Henry Droop (1881) argued for the smaller quota now named after him. The transfer of surpluses at a fraction of their value is named after J. B. Gregory. STV elects the parliaments of Ireland and Malta and the Australian Senate, and Scottish local councils since 2007. Dummett (1984) named the property of proportionality for solid coalitions, and Tideman (1995) surveys the rules and their variants. Bartholdi and Orlin (1991) showed that manipulating the count is NP-complete.

## References
