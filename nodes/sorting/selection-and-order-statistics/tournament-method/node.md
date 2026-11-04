---
tag: RB2RMG
kind: algorithm
slug: tournament-method
name: Tournament method
aliases:
- knockout tournament selection
area: sorting/selection-and-order-statistics
level: advanced
summary: Find the maximum with a knockout tournament, then the second largest among the elements that lost only to the maximum.
solves: [small-order-statistics, selection-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1932
  people: [Józef Schreier, Hugo Steinhaus, S. S. Kislitsyn]
  note: Schreier described the knockout method for the second best player in 1932, Steinhaus conjectured that n + ⌈lg n⌉ − 2 comparisons are optimal, and Kislitsyn proved it in 1964.
prereqs: [tournament-minimum, selection-problem]
see_also: [second-largest-lower-bound, max-finding-lower-bound, small-order-statistics, tournament-tree, tournament-sort, minimum-and-maximum-finding, heap-select, adversary-argument]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the tournament for the second largest, Schreier, Steinhaus and Kislitsyn, and the bound V_2(n) = n + ceil(lg n) - 2)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.1, Minimum and maximum, exercise on the second smallest of n items with n + ceil(lg n) - 2 comparisons
  - paper: "S. S. Kislitsyn, On the selection of the k-th element of an ordered set by pairwise comparisons, Sibirskii Matematicheskii Zhurnal 5 (1964)"
    locator: pages 557 to 564 (the lower bound n + ceil(lg n) - 2 for the second largest)
  - paper: "J. Schreier, O systemach eliminacji w turniejach, Mathesis Polska 7 (1932)"
    locator: pages 154 to 160 (the knockout method for the first and second places)
---

The tournament method finds the largest and the second largest of $n$ items with $n + \lceil \lg n \rceil - 2$ comparisons in the worst case, which is the least possible. It first plays a knockout [tournament](/tournament-minimum/) to find the maximum with $n - 1$ comparisons, recording for each winner the items it beat. The second largest must have lost to the maximum and to no one else, so it is the largest of the at most $\lceil \lg n \rceil$ items that the maximum beat, and a scan of that short list finishes the job. A plain method that finds the maximum and then the maximum of the rest needs $2n - 3$ comparisons.

## In plain words

In a knockout tennis tournament, the champion is clearly the best player. But the player who loses the final is not always the second best: the second best may have met the champion in the first round and gone home early.

Still, the second best player lost only one match, and that match was against the champion, since no one else can beat them. So to find the true second best, you look only at the players the champion beat along the way, one per round, and hold a small second tournament among them. With 1024 players there are 10 rounds, so only 10 players are in the second tournament, and it takes 9 more matches.

## The problem

Given $n \ge 2$ items $a_1, \ldots, a_n$ with a [total order](/total-order/), return the largest item and the second largest, the items of rank $n$ and $n - 1$ in sorted order, using as few comparisons as possible. This is the case $k = 2$ of [small order statistics](/small-order-statistics/), in the mirror form; the same method with the order reversed gives the smallest and the second smallest.

## The algorithm

The players are indices into $A$. beaten$[w]$ lists the indices that $w$ beat, in the order of the rounds. A tie goes to the left player, so the comparison is "$A[u] \ge A[v]$".

```pseudo id=main
TOURNAMENT-SECOND(A[1 .. n])               ▷ n ≥ 2
L1  P ← [1, 2, ..., n]; beaten[i] ← an empty list, for each i
L2  while |P| > 1 do                       ▷ one round
L3      Q ← an empty list
L4      for j ← 1, 3, 5, ... while j + 1 ≤ |P| do
L5          u ← P[j]; v ← P[j + 1]
L6          if A[u] ≥ A[v] then (w, l) ← (u, v) else (w, l) ← (v, u)
L7          append l to beaten[w]; append w to Q
L8      if |P| is odd then append P[|P|] to Q    ▷ a bye
L9      P ← Q
L10 m ← P[1]                               ▷ the index of a maximum
L11 s ← beaten[m][1]
L12 for each next i in beaten[m] do if A[i] > A[s] then s ← i
L13 return (A[m], A[s])
```

Lines L1 to L9 are the [tournament template](/tournament-minimum/) for the maximum, with RECORD filled in as "append the loser to beaten of the winner". Line L10 takes the champion. Lines L11 and L12 find the largest item in beaten$[m]$, the second tournament, here a scan; beaten$[m]$ is not empty because $n \ge 2$ and $m$ won at least one match.

## Example

For $A = [7, 2, 9, 4, 1, 8, 3, 6]$:

| round | matches | winners |
|---|---|---|
| 1 | $7$ vs $2$, $9$ vs $4$, $1$ vs $8$, $3$ vs $6$ | $7, 9, 8, 6$ |
| 2 | $7$ vs $9$, $8$ vs $6$ | $9, 8$ |
| 3 | $9$ vs $8$ | $9$ |

That is $7$ comparisons, and the maximum is $9$, with beaten $= [4, 7, 8]$. Lines L11 and L12 compare $7$ with $4$ and $8$ with $7$: the second largest is $8$, after $9 = 8 + 3 - 2$ comparisons in total. Here the second largest reached the final, but the method does not rely on that. For $A = [9, 8, 1, 2, 3, 4, 5, 6]$ the item $8$ loses to $9$ in round 1, the final is $9$ against $6$, and beaten $= [8, 2, 6]$ still holds $8$.

## Correctness

The tournament part returns a maximum, by the argument of the [tournament template](/tournament-minimum/): a maximum wins each of its matches with the rule "$\ge$", and a later copy of the maximum can only lose to an item that is at least as large. So let $m$ be the champion, and let $i \neq m$ be any other index. Each player except the champion loses exactly once. Follow the chain $i, w_1, w_2, \ldots$ where each index is beaten by the next one. The chain ends at $m$, because each step goes to a player who stayed in the tournament longer. The values do not decrease along the chain, so the last index before $m$ is in beaten$[m]$ and its value is at least $A[i]$. Hence the largest value in beaten$[m]$ is at least each $A[i]$ with $i \ne m$, and it is one of them, so it is the largest item other than $A[m]$, which is the item of rank $n - 1$. The full proof is in the proof file below.

## Complexity

- **Comparisons.** The tournament makes $n - 1$ comparisons, one per knocked-out player. The champion plays at most one match per round, and there are $\lceil \lg n \rceil$ rounds, so $|\text{beaten}[m]| \le \lceil \lg n \rceil$ and the scan of line L12 makes at most $\lceil \lg n \rceil - 1$ comparisons. The total is at most $n + \lceil \lg n \rceil - 2$, and it is exactly that when $n$ is a power of two. With byes the champion can play fewer matches: for $n = 5$, if $A[5]$ is the maximum it gets a bye in rounds 1 and 2 and plays only the final, so the method makes $4$ comparisons.
- **Optimality.** No comparison algorithm can do better in the worst case: the [second largest lower bound](/second-largest-lower-bound/) shows that $n + \lceil \lg n \rceil - 2$ comparisons are needed. The plain method, a scan for the maximum and then a scan of the other $n - 1$ items, makes $2n - 3$. For $n = 1024$ that is $2045$ against $1032$.
- **Time and space.** The other work is a constant per comparison, so the time is $\Theta(n)$. The beaten lists hold $n - 1$ entries in total, so the extra space is $\Theta(n)$. Storing the full tournament tree in an array of $2n - 1$ cells is the same in bulk.

## Properties

- **Optimal in comparisons.** It meets the lower bound exactly for each $n \ge 2$.
- **Not in place.** It needs the beaten lists or the tree of matches, $\Theta(n)$ extra words.
- **Not online.** A new item can change the champion and every list, so the whole input must be known.
- **Deterministic and comparison based.** It uses only comparisons between items.

## Variants and improvements

- **Less space.** A player's list is needed only while it is still in the tournament, so lists of losers can be dropped. A recursive version that returns the pair (champion, beaten list) for each half keeps $O(\log n)$ lists of $O(\log n)$ indices on its stack, so $O(\log^2 n)$ extra space.
- **The smallest two.** Reverse the order to find the minimum and the second smallest, as in the CLRS exercise.
- **More ranks.** Keep the whole tree, remove the champion and replay its path: each further rank costs at most $\lceil \lg n \rceil$ matches. This gives the third largest and beyond, and in the limit [tournament sort](/tournament-sort/). For fixed small $k$ the method of Hadian and Sobel does better; see [small order statistics](/small-order-statistics/).
- **The maximum and the minimum.** A different use of the first round splits the items into winners and losers and gives both extremes with $\lceil 3n/2 \rceil - 2$ comparisons ([minimum and maximum finding](/minimum-and-maximum-finding/)).

## When to use it

Use it when comparisons are expensive and both of the top two items are needed, or when a ranked runner-up is needed for a contest that is played as a knockout anyway. When comparisons are cheap, two scans or a scan that keeps the two largest so far are simpler and use $O(1)$ space; on random input the scan that keeps the top two makes about $n + 2 \ln n$ comparisons on average, so it is close in practice.

## Pitfalls

- **Taking the loser of the final.** The player who lost the final is the second largest only by chance. In the second example above it is $6$, not $8$.
- **Forgetting byes.** If $n$ is not a power of two, the odd player must go on to the next round. Dropping it can drop the maximum.
- **Ties.** With repeated items, the maximum can appear twice. The method still works: the other copy is the largest item other than the champion, and the proof covers it. The comparison of line L6 must be the same rule each time.
- **Counting the scan wrong.** The second tournament has $|\text{beaten}[m]|$ players and makes one comparison fewer than that, not $\lceil \lg n \rceil$.

## Implementations

## History

Lewis Carroll complained in 1883 that the usual lawn tennis tournament gives the second prize unfairly, since the best player can knock out the second best early. In 1932 Józef Schreier described an elimination scheme that finds the first and second places with $n + \lceil \lg n \rceil - 2$ matches, and Hugo Steinhaus conjectured that no scheme can do with fewer. Schreier's proof of optimality had a gap; S. S. Kislitsyn gave the first full proof in 1964. Knuth tells this story in Section 5.3.3 of The Art of Computer Programming, which also gives the short adversary proof now standard in textbooks.

## References
