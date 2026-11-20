---
tag: XQFZVT
kind: algorithm
slug: ranked-pairs
name: Ranked pairs
aliases:
- Tideman method
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Locks in pairwise majorities from the largest margin down, skipping any that would form a cycle, and elects the source of the result.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(n m^2 + m^3)}
  space: {extra: O(m^2)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1987
  people: [T. Nicolaus Tideman, Thomas M. Zavist]
  note: "Tideman proposed ranked pairs in 1987 as a rule that is independent of clones; Zavist and Tideman added a tie-breaking rule in 1989 that makes it completely independent of clones."
prereqs: [condorcet-winner, preference-profile, transitive-closure]
see_also: [schulze-method, copeland-method, smith-set, slater-rule, kemeny-rank-aggregation, cycle-detection, condorcet-paradox, voting-manipulation-problem]
sources:
  - paper: doi:10.1007/BF00433944
    title: "T. Nicolaus Tideman, Independence of clones as a criterion for voting rules, Social Choice and Welfare 4(3) (1987), 185-206"
    locator: the definition of the ranked pairs rule and the independence of clones criterion
  - paper: doi:10.1007/BF00303170
    title: "Thomas M. Zavist and T. Nicolaus Tideman, Complete independence of clones in the ranked pairs rule, Social Choice and Welfare 6(2) (1989), 167-173"
    locator: the tie-breaking ranking of the candidates that makes ranked pairs completely independent of clones
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 4 (Felix Fischer, Olivier Hudry and Rolf Niedermeier, Weighted tournament solutions), Section 4.5.3, the O(m^3) bound with an incremental transitive closure, Lemma 4.14 (the stack characterization) and Theorem 4.15 (NP-completeness over all tie-breaks)"
  - paper: "Markus Brill and Felix Fischer, The price of neutrality for the ranked pairs method, Proceedings of the 26th AAAI Conference on Artificial Intelligence (AAAI 2012), 1299-1305"
    locator: "the proof that deciding whether a candidate wins ranked pairs for some tie-breaking order is NP-complete"
---

Ranked pairs is a Condorcet method that builds a ranking from the strongest majorities down. It sorts the pairwise contests by the size of the winning margin, then goes down the list and locks in each result, "$x$ is above $y$", unless the results already locked put $y$ above $x$. The locked results form a ranking, and its top candidate wins. A [Condorcet winner](/condorcet-winner/) is never overruled, and when the majorities form a cycle, the weakest majority in the cycle is the one that is dropped. Tideman proposed it in 1987, and it is one of the few common rules that is independent of clones.

## In plain words

Look at every pair of candidates and see which one more voters prefer, and by how much. Sort these results from the clearest win to the narrowest. Then build the final order one result at a time, starting with the clearest. Each new result is written down unless it contradicts what is already written down, either directly or through a chain such as "A above B and B above C" against "C above A". At the end every pair is settled, and the candidate at the top is the winner. The idea is that a big majority is more reliable than a small one, so when majorities disagree in a circle, the smallest one gives way.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and $n$ voters with rankings $r_1, \ldots, r_n$, each best first. Let $n_P(a, b)$ be the number of voters who rank $a$ above $b$, and let the margin be $g(a, b) = n_P(a, b) - n_P(b, a)$, so $g(b, a) = -g(a, b)$. The output is a ranking of all candidates and its top candidate, the winner. Equal margins must be ordered by a tie-breaking rule. Here it is a tie-break ranking $t$ of the candidates, by default $0, 1, \ldots, m - 1$: among pairs with the same margin, the pair $(x, y)$ comes first when $x$ is earlier in $t$, and then when $y$ is earlier in $t$. With the default $t$, ties go to the smaller index, as on every rule page of this area.

## The algorithm

```pseudo id=main
RANKED-PAIRS(P, m, t)                     ▷ t is the tie-break ranking of the candidates
L1  g[x][y] ← n_P(x, y) - n_P(y, x) for all x ≠ y
L2  L ← the pairs (x, y) with g[x][y] ≥ 0, sorted by g[x][y] from largest to smallest, ties by t
L3  R[x][y] ← (x = y) for all x, y        ▷ R is the transitive closure of the locked pairs
L4  for each (x, y) in L, in order do
L5      if R[y][x] then skip this pair     ▷ locking x over y would close a cycle
L6      for each z with R[z][x] and not R[z][y]: R[z][w] ← true for each w with R[y][w]
L7  order ← the candidates sorted by |{w : R[x][w]}|, largest first
L8  return order, and order[1] as the winner
```

Line L2 keeps both directions of a pair with margin 0, so every pair of candidates has at least one entry in $L$. Line L5 is the cycle test: $y$ already reaches $x$ through locked pairs, so the pair $x$ over $y$ would close a cycle. Line L6 locks $x$ over $y$ and updates the [transitive closure](/transitive-closure/) at once. Every $z$ that reaches $x$ now reaches all that $y$ reaches. A row $z$ that already reaches $y$ already reaches all of that, so only the other rows are changed. This is the incremental closure of Ibaraki and Katoh that the Handbook of Computational Social Choice uses for the $O(m^3)$ bound. At the end the closure is a linear order, and line L7 reads it off: the candidate in place $k$ from the top reaches exactly $m - k + 1$ candidates, itself included.

## Example

Take four candidates $a, b, c, d$ (indices 0 to 3) and 26 voters:

| voters | ranking |
|---|---|
| 3 | $a \succ b \succ c \succ d$ |
| 6 | $c \succ d \succ a \succ b$ |
| 11 | $b \succ c \succ d \succ a$ |
| 6 | $c \succ a \succ b \succ d$ |

The positive margins are $g(c, d) = 26$, $g(c, a) = 20$, $g(b, d) = 14$, $g(d, a) = 8$, $g(a, b) = 4$ and $g(b, c) = 2$. Every candidate loses some contest, so there is no Condorcet winner, and the majorities form the cycles $a \to b \to d \to a$ and $b \to c \to a \to b$, among others.

| step | pair | margin | test of line L5 | action |
|---|---|---|---|---|
| L4 to L6 | $c$ over $d$ | 26 | $d$ does not reach $c$ | lock |
| L4 to L6 | $c$ over $a$ | 20 | $a$ does not reach $c$ | lock |
| L4 to L6 | $b$ over $d$ | 14 | $d$ does not reach $b$ | lock |
| L4 to L6 | $d$ over $a$ | 8 | $a$ does not reach $d$ | lock |
| L4 to L6 | $a$ over $b$ | 4 | $b \to d \to a$ is locked | skip |
| L4 to L6 | $b$ over $c$ | 2 | $c$ does not reach $b$ | lock |
| L7 | | | | $b$ reaches 4, $c$ reaches 3, $d$ reaches 2, $a$ reaches 1 |

The ranking is $b \succ c \succ d \succ a$, and $b$ wins. The only result that is overruled is $a$ over $b$, the weakest link of the cycle $a \to b \to d \to a$. On the same profile the [Schulze method](/schulze-method/) elects $c$: it compares $b$ and $c$ by their strongest paths, and the path $c \to a \to b$ has strength 4, more than the direct margin 2 of $b$ over $c$. Ranked pairs keeps $b$ over $c$, because that result does not contradict anything locked before it. So the two methods, which agree on most profiles, are different rules.

## Correctness

Each pass of the loop keeps two facts: the locked pairs form an acyclic graph, and $R$ is its reflexive transitive closure. Line L5 rejects exactly the pairs that would close a cycle, and line L6 adds to row $z$ the set reached by $y$ exactly when $z$ reaches $x$, which is what the new pair adds to the closure. For every two candidates $x \ne y$, at least one of $(x, y)$ and $(y, x)$ is in $L$. When it is processed, either it is locked, or line L5 finds that the other direction is already in $R$. So at the end $R$ relates every pair one way and, being acyclic, is a linear order, which line L7 lists. The proof in `proofs/correctness.md` writes this out, proves the $O(m^3)$ bound of the closure updates and proves the properties below.

## Complexity

Line L1 takes $O(n m^2)$ time. Line L2 sorts at most $m(m - 1)$ pairs in $O(m^2 \log m)$ time. Line L5 takes $O(1)$ time per pair. In line L6, the scan over $z$ takes $O(m)$ time per locked pair, which is $O(m^3)$ in all. A row $z$ is rewritten in $O(m)$ time only when $R[z][y]$ goes from false to true, and this happens at most once for each of the $m^2$ entries, which is $O(m^3)$ in all. Line L7 takes $O(m^2)$ time. The total is $O(n m^2 + m^3)$ in the [word RAM](/word-ram/) model, with $O(m^2)$ extra space for $g$, $L$ and $R$. A simpler version that tests each pair with a fresh [depth-first search](/depth-first-search/) takes $O(m^2)$ time per pair, so $O(m^4)$ in all.

## Properties

The proofs are in `proofs/correctness.md`, and the tests check each property by brute force over all profiles with up to 4 candidates and few voters, and on random profiles with up to 6 candidates.

- **Condorcet and Smith consistent.** The ranking puts the [Smith set](/smith-set/) on top, so a Condorcet winner always wins. A pair from outside the Smith set into it has a negative margin and is never in $L$, so nothing can ever lock an outsider above a member.
- **Pareto.** If every voter ranks $a$ above $b$, the margin $n$ of $a$ over $b$ is the largest possible, and a locked chain from $b$ to $a$ would need margins of $n$ all the way, which would make every voter rank $b$ above $a$.
- **Anonymous.** Only the margins are used.
- **Neutral, up to the tie-break.** Renaming the candidates and the tie-break ranking in the same way renames the result. With a fixed tie-break ranking the rule is not neutral.
- **Monotone.** Raising the winner on a ballot leaves the whole ranking the same. Every pair that was skipped is still skipped, because the chain that blocked it is locked again, and no earlier.
- **Independent of clones.** Adding a candidate that is next to an existing candidate on every ballot does not change which of the other candidates wins, with the tie-break rule of Zavist and Tideman.
- **Not strategyproof.** Some voter can gain by a false ranking with 3 candidates and 3 voters. Xia, Zuckerman, Procaccia, Conitzer and Rosenschein showed in 2009 that finding a manipulation is NP-hard for ranked pairs, even for one voter.
- **Margins and winning votes agree on full rankings.** With full rankings, $n_P(x, y) = (n + g(x, y))/2$, so sorting by the number of winning votes gives the same order of pairs as sorting by margin.

## Variants and improvements

- **Winning votes.** Many descriptions sort the pairs by $n_P(x, y)$, the number of voters on the winning side. With full rankings this is the same order. With ballots that leave candidates unranked, the two versions differ.
- **All tie-breaks.** The neutral correspondence takes every candidate that wins for some order of the tied pairs. Brill and Fischer (2012) proved that deciding whether a candidate is in this set is NP-complete. The code computes the winner for one given tie-break ranking.
- **Stack characterization.** A ranking is the ranked pairs ranking exactly when, for each pair with $x$ above $y$ in it, there is a chain from $x$ down to $y$, inside the ranking, whose links all come before the pair $(y, x)$ in the order of line L2, with the pairs of negative margin placed last. This is Lemma 4.14 in the Handbook, after Zavist and Tideman. The tests check it by brute force.
- **Strongest paths.** The [Schulze method](/schulze-method/) uses strongest paths in place of the greedy locking. The example shows that they can differ.

## When to use it

Use ranked pairs for a Condorcet method whose count is easy to explain step by step and that gives a full ranking. It suits committees and online polls with full ballots and a moderate number of candidates. It is also a good choice when clones are a concern, for example when one party can nominate several similar candidates. If the electorate already uses the Schulze method, keep it: both rules are Condorcet and clone consistent, and they rarely differ.

## Pitfalls

- **Dropping pairs with margin 0.** If line L2 keeps only positive margins, a tied pair may stay unsettled, and the locked relation is not a full ranking. Keep both directions of a tied pair, or rank the leftover pairs by another rule.
- **An unstated tie rule.** Equal margins are common with few voters, and the order of tied pairs can change the winner. State the tie-break ranking, as line L2 does.
- **Testing the wrong direction.** Line L5 must ask whether $y$ already reaches $x$. Asking whether $x$ reaches $y$ rejects the pairs that are already implied, which are harmless, and misses the ones that close a cycle.
- **Electing the candidate with no locked defeat too early.** The winner is the source of the final graph. A candidate with no locked defeat after part of the list may still get one later, so read the winner only after all pairs are processed.

## Implementations

## History

T. Nicolaus Tideman introduced ranked pairs in 1987 in a paper that also defined independence of clones: a rule should not change its winner among the other candidates when a candidate is replaced by a set of similar candidates. Ranked pairs met this condition except in some cases with ties, and Thomas M. Zavist and Tideman added a tie-break ranking of the candidates in 1989 that makes it fully independent of clones. In computational social choice, Xia and coauthors showed in 2009 that manipulation is NP-hard, and Brill and Fischer showed in 2012 that the neutral version over all tie-breaks is NP-hard to compute.

## References
