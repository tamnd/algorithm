---
tag: 311MZG
kind: algorithm
slug: ford-johnson-algorithm
name: Ford-Johnson algorithm
aliases:
- merge-insertion sort
- Ford-Johnson sort
area: sorting/comparison-sorts
level: advanced
summary: Sorts with the fewest comparisons known for small n; close to the information-theoretic bound.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n²), comparisons: n lg n − Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1959
  people: [Lester R. Ford Jr., Selmer M. Johnson]
  note: Ford and Johnson published merge insertion in 1959 as the answer to a tournament problem, the question of how few matches decide a full ranking of n players.
prereqs: [insertion-sort, binary-search, comparison-sort-lower-bound, comparison-cost-model]
see_also: [insertion-sort, merge-sort, comparison-sort, decision-tree-model, information-theoretic-bound, merging-lower-bound]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1, Minimum-comparison sorting (merge insertion, its worst-case count F(n), the comparison with ⌈lg n!⌉, and the table of S(n))
  - paper: "Lester R. Ford Jr. and Selmer M. Johnson, A tournament problem, The American Mathematical Monthly 66(5), 1959"
    locator: pp. 387 to 389 (the merge insertion method)
  - paper: "Glenn K. Manacher, The Ford-Johnson sorting algorithm is not optimal, Journal of the ACM 26(3), 1979"
    locator: pp. 441 to 456 (infinitely many n for which methods based on merging beat merge insertion)
  - paper: "Marcin Peczarski, New results in minimum-comparison sorting, Algorithmica 40(2), 2004"
    locator: pp. 133 to 145 (S(14) = 38, S(15) = 42 and S(22) = 71, so merge insertion is optimal for these n)
---

The Ford-Johnson algorithm, also called merge insertion, sorts $n$ items with fewer comparisons in the worst case than any other simple method. It pairs the items, sorts the winners of the pairs recursively, and then inserts the losers into the sorted chain by binary search, in a special order that keeps each search at a power of two. Its worst case is

$$F(n) = \sum_{k=1}^{n} \left\lceil \lg \tfrac{3k}{4} \right\rceil$$

comparisons, which equals the [information-theoretic lower bound](/comparison-sort-lower-bound/) $\lceil \lg n! \rceil$ for $n \le 11$ and for $n = 20, 21$, and is never more than about $0.11\, n$ above $\lg n!$. Its other costs are high, so it matters when comparisons are expensive, and as the benchmark in the study of [minimum-comparison sorting](/comparison-cost-model/).

## In plain words

You want to rank players with as few matches as possible. First play them in pairs. Each winner is better than one loser, so you already know something about each loser.

Rank the winners by the same method. Now the winners stand in a line, and each loser belongs somewhere below the winner who beat them. The loser who lost to the lowest winner is below everyone, so put that loser at the bottom for free.

Add the other losers one at a time, finding each place by halving the range. A loser only needs to be compared with the players below their winner, so the range is short. The trick is the order of the losers: pick them so that each search covers just under a power of two places, like 3, 7 or 15, because a search of 3 places costs no more than a search of 2.

## The problem

The input is a sequence $X$ of $n$ items with a total order, compared only with $<$. The output is the items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The cost that the algorithm minimizes is the number of comparisons in the worst case. Moves and bookkeeping are not counted, as in the [comparison cost model](/comparison-cost-model/).

## The algorithm

```pseudo id=main
MERGE-INSERTION(X)                            ▷ returns the items of X in sorted order
L1  n ← |X|; if n ≤ 1 then return X
L2  for i ← 1 to ⌊n/2⌋ do                     ▷ m = ⌊n/2⌋ pairs
L3      compare X[2i − 1] and X[2i]; the larger is a_i and the smaller is b_i
L4  if n is odd then b_{m+1} ← X[n]           ▷ a loser with no winner
L5  sort the pairs (a_i, b_i) by a_i with MERGE-INSERTION, and number them again so that a_1 ≤ a_2 ≤ … ≤ a_m
L6  S ← (b_1, a_1, a_2, …, a_m)               ▷ b_1 ≤ a_1, so b_1 needs no comparison
L7  for k ← 2, 3, … while t_{k−1} < ⌈n/2⌉ do  ▷ t_k = (2^{k+1} + (−1)^k)/3: 1, 3, 5, 11, 21, 43, …
L8      for j ← min(t_k, ⌈n/2⌉) downto t_{k−1} + 1 do
L9          u ← the position of a_j in S if j ≤ m, else |S|
L10         insert b_j into S[0 … u − 1] by binary search
L11 return S
```

Line L5 makes a recursive call on $m$ items, each of which is a pair compared by its larger member, so each comparison of the call is one comparison of the input. The losers are inserted in groups: first $b_3, b_2$, then $b_5, b_4$, then $b_{11}, \ldots, b_6$, then $b_{21}, \ldots, b_{12}$, and so on. The group ends $t_k$ satisfy $t_k + t_{k-1} = 2^k$. Inside a group, the loser with the largest index goes first. Line L10 searches only the part of $S$ to the left of $a_j$, because $b_j \le a_j$.

## Example

Sort $X = [5, 1, 4, 2, 8, 0, 3]$, with $n = 7$ and $m = 3$.

**Pairs (3 comparisons).** $(5, 1)$, $(4, 2)$ and $(8, 0)$ give the winners $5, 4, 8$ with the losers $1, 2, 0$. The item 3 has no partner.

**Sort the winners (2 comparisons).** The recursive call on $5, 4, 8$ pairs $(5, 4)$, puts the loser 4 before 5, and inserts the unpaired 8 into $[4, 5]$ with one comparison $8 < 5$. Now $a_1 = 4$, $a_2 = 5$, $a_3 = 8$, with $b_1 = 2$, $b_2 = 1$, $b_3 = 0$, and $b_4 = 3$ with no partner.

**Insert the losers (7 comparisons).**

| step | inserted | searched part of $S$ | comparisons | $S$ after the step |
|---|---|---|---|---|
| L6 | $b_1 = 2$ | none, $b_1 < a_1$ | 0 | 2 4 5 8 |
| group 2 | $b_3 = 0$ | 2 4 5 (left of $a_3 = 8$) | 2 | 0 2 4 5 8 |
| group 2 | $b_2 = 1$ | 0 2 4 (left of $a_2 = 5$) | 2 | 0 1 2 4 5 8 |
| group 3 | $b_4 = 3$ | 0 1 2 4 5 8 (no partner) | 3 | 0 1 2 3 4 5 8 |

The total is $3 + 2 + 7 = 12$ comparisons. The worst case for $n = 7$ is $F(7) = 13 = \lceil \lg 7! \rceil$, since $7! = 5040$ and $2^{12} = 4096 < 5040 \le 8192 = 2^{13}$. Binary insertion sort, which is [insertion sort](/insertion-sort/) with a binary search for each place, and [merge sort](/merge-sort/) both need 14 comparisons in the worst case for $n = 7$.

## Correctness

The chain $S$ stays sorted. It starts sorted, because $b_1 \le a_1$ by line L3 and the $a_i$ are sorted by line L5. When $b_j$ is inserted, each item at or after the position of $a_j$ is at least $a_j \ge b_j$, so the correct place of $b_j$ in $S$ is in $S[0 \ldots u]$, and the binary search of line L10 finds it. Each item of $X$ is placed in $S$ exactly once: the winners at line L6, $b_1$ at line L6, and every other loser once in the groups, which cover the indices $2, \ldots, \lceil n/2 \rceil$. The recursion is on $\lfloor n/2 \rfloor < n$ items, so it ends. The full proof is below.

## Complexity

**The key bound.** Consider the group $t_{k-1} < j \le t_k$. When $b_j$ is inserted, the part of $S$ to the left of $a_j$ holds at most $a_1, \ldots, a_{j-1}$, the losers $b_1, \ldots, b_{t_{k-1}}$ of the earlier groups, and the losers $b_{j+1}, \ldots, b_{t_k}$ of this group that were inserted before it. That is at most $(j - 1) + t_{k-1} + (t_k - j) = t_k + t_{k-1} - 1 = 2^k - 1$ items. A binary search among $2^k - 1$ items has $2^k$ possible results, so it needs at most $k$ comparisons. The same count holds for the loser with no partner, which is inserted first in its group. This is why the groups have the sizes $2, 2, 6, 10, 22, \ldots$: each one is as large as it can be while every search in it stays at $k$ comparisons.

**The worst case.** Adding the $\lfloor n/2 \rfloor$ comparisons of the pairs, the recursive call and $k$ comparisons for each loser in group $k$ gives the recurrence of Knuth, Section 5.3.1, whose solution is $F(n) = \sum_{k=1}^{n} \lceil \lg (3k/4) \rceil$. The exhaustive runs for $n \le 8$ reach this worst case exactly.

| $n$ | 1 to 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 16 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\lceil \lg n! \rceil$ | 0, 1, 3, 5 | 7 | 10 | 13 | 16 | 19 | 22 | 26 | 29 | 33 | 45 | 62 | 66 | 70 |
| merge insertion $F(n)$ | 0, 1, 3, 5 | 7 | 10 | 13 | 16 | 19 | 22 | 26 | 30 | 34 | 46 | 62 | 66 | 71 |
| binary insertion | 0, 1, 3, 5 | 8 | 11 | 14 | 17 | 21 | 25 | 29 | 33 | 37 | 49 | 69 | 74 | 79 |

Merge sort has the same worst case as binary insertion for these $n$.

**Large $n$.** $F(n) = n \lg n - c(n)\, n$, where for large $n$ the factor $c(n)$ moves between about $1.329$ and $1.415$ as $n$ moves between powers of two. These are the smallest and largest values of $c(n)$ for $2^{15} \le n \le 2^{18}$. Since $\lg n! = n \lg n - 1.443\, n + O(\log n)$, merge insertion is within about $0.11\, n$ of the lower bound for every $n$. For example, $F(1000) = 8641$ and $\lg 1000! \approx 8529.4$. On 20 random permutations of 1000 items, the mean was 8558.75 comparisons.

**The other costs.** With $S$ in an array, each insertion moves up to $n$ items, so the moves take $\Theta(n^2)$ time. Finding $a_j$ in $S$ also needs bookkeeping. A balanced tree or a list with an index brings the time to $O(n \log n)$, but the constant factors stay large. The space is $\Theta(n)$ for the chain and the pairs.

## Properties

- **Comparison-optimal for small $n$.** It meets $\lceil \lg n! \rceil$ for $n \le 11$ and $n = 20, 21$. For $n = 12$ to $15$ and $n = 22$ it is still optimal, because computer searches showed that no algorithm does better there: Wells (1965) for $n = 12$, Kasai, Sawato and Iwata (1994) for $n = 13$, and Peczarski (2004) for $n = 14, 15, 22$.
- **Not optimal for all $n$.** Manacher (1979) showed that for infinitely many $n$, methods that sort parts and then merge them beat merge insertion. Peczarski (2007) showed that this kind of method does not beat it below 47 items.
- **Not stable.** On $[0_a, 1_b, 0_c, 0_d]$ the output is $[0_c, 0_d, 0_a, 1_b]$.
- **Not in place, not adaptive.** It needs $\Theta(n)$ extra space, and it makes about the same number of comparisons on sorted input.

## Variants and improvements

- **Binary insertion sort.** Insert the items one at a time by binary search. It is simpler and makes $\sum_{k=1}^{n} \lceil \lg k \rceil$ comparisons in the worst case, which is $n \lg n - n + O(\log n)$, up to about $0.44\, n$ more than merge insertion.
- **Average case.** Merge insertion is not tuned for the average. Iwama and Teruyama (2017) changed the insertion steps and got a lower average. Edelkamp and Weiß used merge insertion inside QuickXsort, a scheme that sorts the parts of a quicksort partition with another method, and reached about $n \lg n - 1.4\, n$ comparisons on average.

## When to use it

Use it when one comparison costs far more than the bookkeeping, and $n$ is small: for example, when each comparison is a human judgement, a slow query or an expensive computation, and the items are few. It is also the standard reference for the minimum-comparison problem: a new bound for $S(n)$ is compared with $F(n)$. For ordinary data in memory it is slower than [merge sort](/merge-sort/) or [quicksort](/quicksort/), because of the moves and the bookkeeping.

## Pitfalls

- **The wrong insertion order.** Inserting $b_2, b_3, b_4, \ldots$ in increasing order gives searches of sizes that are not of the form $2^k - 1$, and the worst case rises toward that of binary insertion.
- **Searching all of $S$.** Each paired loser must be searched only to the left of its winner. Searching the whole chain is still correct but costs more comparisons.
- **Losing the partner after the recursion.** The recursive call reorders the winners, and each loser must move with its winner. Carry the pairs as units, as line L5 does, or keep an index.
- **Counting the moves as free in practice.** The array chain makes the time quadratic. For large $n$, use a linked structure, or use another sort.

## Implementations

## History

Ford and Johnson (1959) gave merge insertion as the solution to a tournament problem: rank $n$ players with as few games as possible. Knuth's Section 5.3.1 gives the formula $F(n)$ and the table of the best known values $S(n)$. Wells (1965) found by computer that $S(12) = 30$, so for $n = 12$ the information-theoretic bound cannot be reached and merge insertion is optimal. Manacher (1979) showed that merge insertion is not optimal for infinitely many $n$. Later computer searches by Kasai, Sawato and Iwata (1994) and by Peczarski (2004) proved its optimality for $n = 13, 14, 15$ and $22$.

## References
