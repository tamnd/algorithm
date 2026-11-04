---
tag: 1KTMX5
kind: technique
slug: h-sorting
name: h-sorting
aliases:
- h-ordering
area: sorting/comparison-sorts
level: core
summary: Rearranges an array so that every hth element forms a sorted subsequence, the building block of Shellsort.
prereqs: [insertion-sort, inversion]
see_also: [shell-sort, comb-sort, sorting-network, odd-even-transposition-sort, coin-change-problem]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Sorting by insertion (diminishing increment sort, Theorem K that an h-sorted array stays k-sorted, Lemma L, the count of inversions of 2-ordered permutations, and the bounds for the increments of Papernov and Stasevich and of Pratt)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1, Elementary Sorts (Shellsort and the definition of an h-sorted array)
---

An array $A[0 \ldots n-1]$ is *h-sorted* when $A[i] \le A[i+h]$ for each $i$ with $0 \le i < n - h$: each of the $h$ subsequences $A[r], A[r+h], A[r+2h], \ldots$ is sorted. To *h-sort* an array is to make it h-sorted, usually with [insertion sort](/insertion-sort/) on each of the $h$ subsequences. A 1-sorted array is sorted. [Shell sort](/shell-sort/) h-sorts the array with a decreasing sequence of gaps that ends with 1. The technique works because of one fact: h-sorting an array that is already k-sorted leaves it k-sorted, so each pass keeps the work of the passes before.

## In plain words

Deal a row of cards into $h$ piles, like dealing to $h$ players: card 0 to player 0, card 1 to player 1, and so on, then card $h$ to player 0 again. Let each player sort their own pile, and put the cards back in the same places. Now every $h$-th card is in order. That is an h-sorted row.

With a large $h$, each pile is short, so it is cheap to sort, and a small card can jump far to the left in one step. With $h = 1$ there is one pile, which is the whole row, and the row is fully sorted. Shell sort does a large $h$ first, then smaller ones. Each pass leaves the row closer to sorted, so the last pass with $h = 1$ has little work left.

## When it applies

- An insertion sort is too slow because items are far from their final places: an h-sort lets an item move $h$ places in one step.
- The input must be sorted in place, with small code and no recursion, as in an embedded system.
- A partial order is enough: some algorithms need only that items $h$ apart are in order, for example a check of a rough ranking.
- A fixed pattern of comparisons is wanted, as in a [sorting network](/sorting-network/): an h-sort by compare-exchange passes is oblivious when the number of passes is fixed in advance.

Signs that it does not apply: the sort must be stable, because items jump over equal items $h$ apart; or the sort must have a proved bound of $O(n \log n)$ comparisons, which no known sequence of gaps gives for Shell sort.

## The template

```pseudo id=main
H-SORT(A, h)                                     ▷ insertion sort of each subsequence with gap h
L1  for i ← h to n − 1 do
L2      x ← A[i], j ← i
L3      while j ≥ h and A[j − h] > x do
L4          A[j] ← A[j − h], j ← j − h
L5      A[j] ← x

DIMINISHING-INCREMENT-SORT(A)
L6  for each h in GAPS(n), in decreasing order, ending with 1 do   ▷ hole: the gap sequence
L7      H-SORT(A, h)                                               ▷ hole: the way to h-sort
```

The loop of line L1 runs over all indices once, and line L3 works on the subsequence of $i$ only. So the $h$ subsequences are sorted by one interleaved pass, not one after the other. The holes are the gap sequence and the way to h-sort. The rules that make the template correct and fast are these.

1. **H-SORT makes the array h-sorted.** Lines L2 to L5 are insertion sort on the subsequence $A[i \bmod h], A[i \bmod h + h], \ldots$, restricted to the items up to $i$. By the invariant of insertion sort, after the step for $i$ the items of that subsequence up to index $i$ are sorted. So at the end, all $h$ subsequences are sorted. The step for $i$ moves only items of its own subsequence.
2. **The last gap is 1.** A 1-sort is a full insertion sort, so the output is sorted whatever the gaps before. The other gaps affect only the cost.
3. **The passes keep their work (Knuth, Theorem K).** If a k-sorted array is h-sorted, it stays k-sorted. Knuth proves it from Lemma L: if $y_j \le x_{m+j}$ for $1 \le j \le r$, for two sequences $x$ and $y$, then the same relations hold after each sequence is sorted on its own. So after the passes with gaps $h_1, h_2, \ldots$, the array is $h_t$-sorted for each $h_t$ used.
4. **Sums of gaps.** If the array is h-sorted and k-sorted, then $A[i] \le A[i + ah + bk]$ for all $a, b \ge 0$, by a chain of steps. If $\gcd(h, k) = 1$, every distance of at least $(h-1)(k-1)$ is of the form $ah + bk$, the result of Sylvester on the [coin problem](/coin-change-problem/). So two items more than $(h-1)(k-1) - 1$ places apart are in order, and a later g-sort moves each item at most $(h-1)(k-1)/g$ steps.

**The cost of one h-sort.** It is insertion sort on $h$ subsequences of about $n/h$ items, so it makes at most $h \binom{\lceil n/h \rceil}{2} \approx n^2/(2h)$ moves, and about $n^2/(4h)$ on a random permutation. In general, it makes exactly as many moves as the number of [inversions](/inversion/) inside the subsequences, and at most that number plus $n - h$ comparisons.

**The cost of a 1-sort after a 2-sort.** Knuth counts the permutations that are 2-sorted: there are $\binom{n}{\lfloor n/2 \rfloor}$ of them, and together they have $\lfloor n/2 \rfloor\, 2^{n-2}$ inversions. So a 1-sort of a random 2-sorted array makes $\lfloor n/2 \rfloor 2^{n-2} / \binom{n}{\lfloor n/2 \rfloor} \sim \sqrt{\pi/128}\; n^{3/2}$ moves on average, about 4,950 for $n = 1000$, against 249,750 for a random permutation.

**An example.** Sort $A = [8, 4, 1, 5, 9, 2, 6, 3, 7, 0]$, which has 26 inversions, with the gaps 4, 3, 1.

| pass | the array after the pass | comparisons | moves | inversions left | 4-sorted | 3-sorted |
|---|---|---|---|---|---|---|
| start | 8 4 1 5 9 2 6 3 7 0 | | | 26 | no | no |
| $h = 4$ | 7 0 1 3 8 2 6 5 9 4 | 8 | 6 | 16 | yes | no |
| $h = 3$ | 3 0 1 4 5 2 6 8 9 7 | 11 | 5 | 7 | yes | yes |
| $h = 1$ | 0 1 2 3 4 5 6 7 8 9 | 15 | 7 | 0 | yes | yes |

The 4-sort sorts the subsequences at the indices $\{0, 4, 8\}$, $\{1, 5, 9\}$, $\{2, 6\}$ and $\{3, 7\}$. The array stays 4-sorted after the 3-sort, as rule 3 says. The three passes make 18 moves in total. Insertion sort alone would make 26, one for each inversion.

## Classic examples

- **[Shell sort](/shell-sort/).** The diminishing increment sort of the template. With the gaps $2^k - 1$, Papernov and Stasevich proved $O(n^{3/2})$ comparisons, by rule 4 for two consecutive gaps. With the gaps $2^p 3^q$, Pratt proved $O(n \log^2 n)$.
- **Pratt's gaps and [sorting networks](/sorting-network/).** If an array is $2h$-sorted and $3h$-sorted, then by rule 4 each item of a subsequence with gap $h$ is out of order with at most its next neighbour in the subsequence. So one pass of compare-exchange at gap $h$, in two rounds of disjoint pairs, h-sorts it. With the $\Theta(\log^2 n)$ gaps $2^p 3^q$, this gives a sorting network of depth $\Theta(\log^2 n)$.
- **[Insertion sort](/insertion-sort/).** The case $h = 1$ alone.
- **[Comb sort](/comb-sort/).** It uses the same decreasing gaps, but makes only one compare-exchange pass for each gap. So the array is not h-sorted after each pass, and the bounds of Shell sort do not carry over to it.

## Variations

- **h-sort by passes of exchanges.** Instead of insertion, run [bubble sort](/bubble-sort/) or [odd-even transposition sort](/odd-even-transposition-sort/) on each subsequence. The result is the same h-sorted array, at a higher cost, but with a fixed pattern of comparisons.
- **One subsequence at a time.** Sort the subsequence $A[r], A[r+h], \ldots$ for $r = 0, \ldots, h-1$ in turn. The moves are the same as in the interleaved form of the template, but the memory access pattern differs.
- **h-sort of a linked structure.** On a linked list, an h-sort needs $O(h)$ pointers to walk the subsequences, so it is rarely used there.
- **Partial h-sorting.** Stop the insertion of an item after a fixed number of steps. This gives an array that is only roughly h-sorted, as in the passes of comb sort.

## Pitfalls

- **Gaps that do not end with 1.** The output of a pass with $h > 1$ is not sorted in general. A sequence that stops at 2 leaves the array 2-sorted only.
- **Gaps with a common factor.** If all gaps before the last are even, the items at even indices never meet the items at odd indices before the 1-sort. The gaps $2^k$ of Shell's original paper have this flaw, and on bad inputs the 1-sort then does $\Theta(n^2)$ moves.
- **A loop bound that skips items.** The loop of line L1 must start at $h$ and run to $n - 1$. Starting at $h + 1$ leaves the first item of one subsequence unsorted against the rest.
- **Losing stability.** An item moves over the items between it and its target, including equal items in other subsequences. Two equal items can change their order, so Shell sort is not stable.

## Exercises

1. Is the array $[1, 3, 2, 4, 3, 5]$ 2-sorted? Is it 3-sorted? Which pairs are inversions? (Answer: it is 2-sorted, since $1 \le 2 \le 3$ and $3 \le 4 \le 5$. It is 3-sorted, since the pairs at distance 3 are $(1, 4)$, $(3, 3)$ and $(2, 5)$. The inversions are $(3, 2)$ at the indices 1 and 2, and $(4, 3)$ at the indices 3 and 4: both are pairs of neighbours, as exercise 2 says.)
2. Show that an array that is 2-sorted and 3-sorted has each item out of order with at most its right neighbour, and so needs at most $n - 1$ moves for a 1-sort.
3. Use Knuth's count to find the mean number of inversions of a random 2-sorted array of 6 items. (Answer: $3 \cdot 2^4 / \binom{6}{3} = 48 / 20 = 2.4$.)
4. With the gaps 4, 2, 1, show that the input $[4, 0, 5, 1, 6, 2, 7, 3]$ makes no move in the passes with gaps 4 and 2, and 10 moves in the 1-sort. Generalize it to show that Shell's gaps $n/2, n/4, \ldots, 1$, for $n$ a power of 2, can need $\Theta(n^2)$ moves. (Hint: put the $n/2$ largest items at the even indices.)

## References
