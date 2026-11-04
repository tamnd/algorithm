---
tag: 1YRTNQ
kind: technique
slug: tournament-minimum
name: Tournament method for the minimum
aliases:
- Tournament for finding the minimum
area: sorting/selection-and-order-statistics
level: core
summary: Finding the smallest element by pairing elements in knockout rounds, so that each element loses at most once and the winner is the minimum.
prereqs: [find-maximum, comparison-model]
see_also: [tournament-method, tournament-tree, tournament-sort, minimum-and-maximum-finding, second-largest-lower-bound, max-finding-lower-bound, parallel-reduction, replacement-selection]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (knockout tournaments, and the second largest with n + ceil(lg n) - 2 comparisons), and Section 5.2.3, Sorting by selection (tree selection)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.1, Minimum and maximum, and its exercise on the second smallest with n + ceil(lg n) - 2 comparisons
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.1, Multiway merging and replacement selection (trees of winners and trees of losers)
---

The tournament method finds the minimum of $n$ items the way a knockout competition finds a champion: pair the items, keep the smaller of each pair, and repeat on the winners until one is left. It makes $n - 1$ comparisons, the least possible, in $\lceil \lg n \rceil$ rounds, and the comparisons of one round are independent of each other. Its value over a plain scan is the structure it leaves behind: each item has lost at most once, and the winner has met only $\lceil \lg n \rceil$ others, which is what makes the [second smallest](/tournament-method/) cheap to find and what [tournament trees](/tournament-tree/) and [tournament sort](/tournament-sort/) are built on.

## In plain words

In a tennis tournament, players are paired in the first round, and the winners go on to the next round. With 16 players there are 8 matches, then 4, then 2, then the final: 15 matches in total, one for each player who must be knocked out.

To find the smallest of many numbers, treat each number as a player and say that the smaller one wins a match. The champion is the smallest number. A simple scan also uses one comparison per knocked-out item, so the count is the same. But in the tournament the champion played only a few matches, about the number of rounds, and each match in a round can be played at the same time as the others.

## When it applies

- The items have a [total order](/total-order/), or any rule that picks a winner of two items so that the overall best item wins each of its matches, such as the minimum, the maximum, or the item with the best key.
- The task needs more than the minimum: the second smallest, the $k$ smallest one by one, or the items that came closest to winning. Then the record of who beat whom pays off.
- The comparisons can run in parallel, or the cost of a step is the depth of the computation, as in hardware and in a [parallel reduction](/parallel-reduction/).
- The players come from several sorted streams and the winner is replaced over and over, as in a $k$-way merge or [replacement selection](/replacement-selection/).

## The template

Each round pairs the current players in order. An odd player out gets a bye and goes to the next round without a match. The holes are what a player is, how a match is decided, and what is recorded about it.

```pseudo id=main
TOURNAMENT(A[1 .. n])                      ▷ n ≥ 1
L1  P ← [1, 2, ..., n]                     ▷ hole: a player, here an index into A
L2  while |P| > 1 do                       ▷ one round
L3      Q ← an empty list
L4      for j ← 1, 3, 5, ... while j + 1 ≤ |P| do
L5          (w, l) ← PLAY(P[j], P[j + 1])  ▷ hole: the winner w and the loser l
L6          RECORD(w, l)                   ▷ hole: for example, add l to beaten[w]
L7          append w to Q
L8      if |P| is odd then append P[|P|] to Q   ▷ a bye
L9      P ← Q
L10 return P[1]
```

For the minimum, PLAY returns the index of the smaller item as the winner, with ties broken by index, and RECORD may do nothing.

**Why it works.** The minimum wins each of its matches, since it is at most each other item, so it is never knocked out and it is the last player left. Each match knocks out exactly one player, and the tournament ends with one player, so it makes exactly $n - 1$ matches, which is $n - 1$ comparisons. No algorithm can do with fewer, by the [max-finding lower bound](/max-finding-lower-bound/): each item other than the minimum must lose at least once.

**Rounds.** A round on $m$ players leaves $\lceil m/2 \rceil$, so after $r$ rounds at most $\lceil n / 2^r \rceil$ players are left, and the loop runs $\lceil \lg n \rceil$ rounds. The winner plays at most one match per round, so it meets at most $\lceil \lg n \rceil$ players. With $n$ a power of two it meets exactly $\lg n$.

## Classic examples

**A trace.** For $A = [7, 2, 9, 4, 1, 8, 3, 6]$:

| round | matches | winners |
|---|---|---|
| 1 | $7$ vs $2$, $9$ vs $4$, $1$ vs $8$, $3$ vs $6$ | $2, 4, 1, 3$ |
| 2 | $2$ vs $4$, $1$ vs $3$ | $2, 1$ |
| 3 | $2$ vs $1$ | $1$ |

There are $4 + 2 + 1 = 7 = n - 1$ comparisons in $3 = \lg 8$ rounds. The winner $1$ beat $8$, $3$ and $2$.

**Byes.** For $A = [5, 3, 8, 1, 4]$, round 1 plays $5$ vs $3$ and $8$ vs $1$ and gives $4$ a bye; round 2 plays $3$ vs $1$ and gives $4$ a bye; round 3 plays $1$ vs $4$. That is $4 = n - 1$ comparisons in $3 = \lceil \lg 5 \rceil$ rounds.

**Uses.**

- **The second smallest.** The second smallest item lost only to the minimum, so it is among the at most $\lceil \lg n \rceil$ items in beaten[winner]. A scan of that list gives it with $\lceil \lg n \rceil - 1$ more comparisons, for $n + \lceil \lg n \rceil - 2$ in total, which is optimal by the [second largest lower bound](/second-largest-lower-bound/). In the trace above, the minimum of $8, 3, 2$ is $2$, after $2$ more comparisons: $9 = 8 + 3 - 2$ in total. This is the [tournament method](/tournament-method/).
- **The minimum and the maximum together.** A first round of $\lfloor n/2 \rfloor$ matches splits the items into winners and losers; the minimum is among the winners and the maximum among the losers. Two tournaments, or two scans, on the halves give both with $\lceil 3n/2 \rceil - 2$ comparisons ([minimum and maximum finding](/minimum-and-maximum-finding/)).
- **Sorting.** Keep the whole tournament as a tree, take out the winner, and replay only its path: each new minimum costs $\lceil \lg n \rceil$ matches, and the result is [tournament sort](/tournament-sort/) with $n \lg n + O(n)$ comparisons.
- **Merging and runs.** A [tournament tree](/tournament-tree/) over the heads of $k$ sorted streams gives the next output of a $k$-way merge in $O(\log k)$ time, and [replacement selection](/replacement-selection/) uses one to make long sorted runs for [external merge sort](/external-merge-sort/).
- **Parallel minimum.** With one processor per match, the rounds are the steps of a [parallel reduction](/parallel-reduction/): the minimum in $\lceil \lg n \rceil$ steps.

## Variations

- **Tree of winners and tree of losers.** Stored as a complete binary tree, each internal node can hold the winner of its match, or the loser. The tree of losers makes replaying a path cheaper, since each node on the path holds the item the new player must meet.
- **Other winning rules.** Any associative choice of a winner works: the maximum, the item with the best key, or the leftmost minimum.
- **Unbalanced pairings.** A scan is a tournament in which the current winner meets each new item: still $n - 1$ comparisons, but the winner meets up to $n - 1$ players and the depth is $n - 1$. The balanced pairing is what keeps both at $\lceil \lg n \rceil$.

## Pitfalls

- **Expecting fewer comparisons than a scan.** For the minimum alone, the tournament makes exactly the $n - 1$ comparisons of a scan. Its gains are in depth and in the record for later questions.
- **Byes in the wrong place.** If the odd player out is dropped instead of being sent on, the minimum can be lost. If byes always go to the same player, that player can reach the final after few matches; the bounds above still hold, but the beaten list of the winner can be shorter than $\lceil \lg n \rceil$, which is fine.
- **Storing values instead of indices.** To report where the minimum is, or to record who beat whom, the players must be indices or (value, index) pairs.
- **Ties.** With equal items, a rule such as "the smaller index wins a tie" keeps the result well defined and makes the tournament return the first minimum.

## Exercises

1. Show that in the balanced template the winner plays at most $\lceil \lg n \rceil$ matches, and give an order of matches in which the minimum plays all $n - 1$ of them.
2. Use the tournament to find the minimum and the second smallest of $[5, 3, 8, 1, 4]$, and count the comparisons.

## References
