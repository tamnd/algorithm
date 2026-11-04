---
tag: A5DV6Z
kind: algorithm
slug: median-of-medians
name: Median of medians
aliases:
- BFPRT algorithm
- deterministic select
- linear-time selection
area: sorting/selection-and-order-statistics
level: core
summary: Deterministic linear-time selection that uses the median of group medians as the pivot.
solves: [selection-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1973
  people: [Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest, Robert E. Tarjan]
  note: The five authors published the method and its linear bound in "Time bounds for selection", Journal of Computer and System Sciences, 1973.
prereqs: [quickselect, selection-problem, substitution-method]
see_also: [deterministic-linear-selection, introselect, quickselect, selection-lower-bound, pivot-selection, median-finding, floyd-rivest-select, weighted-median-post-office-location]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.3, Selection in worst-case linear time (the procedure SELECT with groups of 5 and its recurrence)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (the algorithm PICK and the bound of 5.4305n comparisons)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the linear method of Blum, Floyd, Pratt, Rivest and Tarjan)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 2, Section 2.4, Medians (selection by divide and conquer)
  - paper: doi:10.1137/S0097539795288611
    title: Dorit Dor and Uri Zwick, Selecting the median, SIAM Journal on Computing 28(5) (1999)
    locator: pages 1722 to 1758
  - paper: doi:10.1007/978-3-319-21840-3_16
    title: Ke Chen and Adrian Dumitrescu, Select with groups of 3 or 4, Algorithms and Data Structures (WADS 2015), Lecture Notes in Computer Science 9214
    locator: the whole paper (linear-time variants with groups of 3 and 4)
---

Median of medians is a deterministic [selection](/selection-problem/) algorithm: it splits the items into groups of 5, takes the median of each group, finds the median $x$ of these medians by a recursive call, and uses $x$ as the pivot of a [quickselect](/quickselect/) step. The pivot $x$ always has at least about $3n/10$ items on each side, so the step throws away at least 30 percent of the items, and the total time is $\Theta(n)$ in the worst case in the [comparison model](/comparison-model/). It was the first linear-time selection method, due to Blum, Floyd, Pratt, Rivest and Tarjan in 1973. It is the proof that selection is easier than sorting, and the safe fallback of [introselect](/introselect/).

## In plain words

Quickselect is fast when its pivot lands near the middle, and slow when the pivot is near one end. Median of medians spends some work to find a pivot that is surely not near an end.

Put the items in small groups of five. In each group, find the middle item. Now you have one middle item for each group. Find the middle item of these, with the same method on the smaller list. Call it the pivot.

Half of the groups have a middle item at most the pivot, and in each of those groups three items are at most the pivot. So about three tenths of all items are at most the pivot, and in the same way about three tenths are at least it. Split around the pivot and keep the side with the answer. Each round keeps at most about seven tenths of the items.

## The problem

The input is a list $S$ of $n \ge 1$ items with a [total order](/total-order/) and a rank $k$ with $1 \le k \le n$. The output is the $k$-th smallest item of $S$. This is the [selection problem](/selection-problem/). The items may repeat. The version below does not change $S$.

## The algorithm

For a group $G$ of at most 5 items, its *lower median* is the item of rank $\lceil |G|/2 \rceil$ of $G$. The call SELECT$(S, \lceil n/2 \rceil)$ finds the lower [median](/median/).

```pseudo id=main
SELECT(S, k)                               ▷ S has n ≥ 1 items, 1 ≤ k ≤ n
L1  if n ≤ 5 then sort S by insertion sort, return its item of rank k
L2  split S into g = ⌈n/5⌉ groups of 5 consecutive items (the last may be smaller)
L3  M ← the list of the lower medians of the groups
L4  x ← SELECT(M, ⌈g/2⌉)                   ▷ the median of the medians
L5  L ← the items < x;  E ← the items = x;  G ← the items > x
L6  if k ≤ |L| then return SELECT(L, k)
L7  else if k ≤ |L| + |E| then return x
L8  else return SELECT(G, k − |L| − |E|)
```

Line L1 is the base: at most 5 items are sorted directly. Lines L2 and L3 sort each group of at most 5 items, with at most 10 comparisons each, and keep the middle item. Line L4 is the first recursive call, on $\lceil n/5 \rceil$ items. Line L5 is a three-way [partition](/partition-around-pivot/) around $x$. Lines L6 to L8 keep the part that holds rank $k$, as in quickselect: the $|L|$ smallest items are the items of $L$, the next $|E|$ are copies of $x$, and the rest are in $G$. Line L6 or line L8 is the second recursive call. The three-way split makes the method correct and fast with repeated items.

## Example

Find the median, $k = 8$, of the $n = 15$ items $S = [12, 3, 45, 7, 29, 18, 1, 33, 26, 9, 40, 15, 21, 4, 37]$.

| step | state |
|---|---|
| L2 | groups $[12, 3, 45, 7, 29]$, $[18, 1, 33, 26, 9]$, $[40, 15, 21, 4, 37]$ |
| L3 | sorted groups $[3, 7, \mathbf{12}, 29, 45]$, $[1, 9, \mathbf{18}, 26, 33]$, $[4, 15, \mathbf{21}, 37, 40]$, so $M = [12, 18, 21]$ |
| L4 | $x = $ SELECT$(M, 2) = 18$, by line L1 |
| L5 | $L = [12, 3, 7, 1, 9, 15, 4]$, $E = [18]$, $G = [45, 29, 33, 26, 40, 21, 37]$ |
| L7 | $k = 8 \le |L| + |E| = 8$ and $k > |L| = 7$, so the answer is $18$ |

For $k = 3$ the run goes on at line L6 with SELECT$(L, 3)$. The groups of $L$ are $[12, 3, 7, 1, 9]$ and $[15, 4]$, with lower medians 7 and 4, so the pivot is SELECT$([7, 4], 1) = 4$. Then $L' = [3, 1]$, $E' = [4]$ and $k = 3 \le 3$, so the answer is 4. In the sorted list $1, 3, 4, 7, 9, 12, 15, 18, \ldots$ the items of ranks 3 and 8 are 4 and 18.

In the first call, the pivot 18 has 8 items at most it and 8 items at least it. The bound below promises at least $3\lceil g/2 \rceil - 2 = 4$ on each side for $g = 3$; here the split is perfect.

## Correctness

The proof is by strong induction on $n$. Line L1 is correct for $n \le 5$. For $n \ge 6$, the list $M$ has $\lceil n/5 \rceil < n$ items, so line L4 returns an item $x$ of $S$ by the induction hypothesis. The three lists of line L5 split $S$, and the items of $L$, then $E$, then $G$ form a sorted order of $S$ when each list is sorted. So rank $k$ of $S$ is rank $k$ of $L$ when $k \le |L|$, is $x$ when $|L| < k \le |L| + |E|$, and is rank $k - |L| - |E|$ of $G$ otherwise. Both $L$ and $G$ miss $x$, so they have fewer than $n$ items and the induction hypothesis applies. The full proof is in the proof file below.

## Complexity

**The pivot is balanced.** Let $n \ge 6$ and $g = \lceil n/5 \rceil$. Then

$$ |L| \le \tfrac{7n}{10} + \tfrac12 \quad \text{and} \quad |G| \le \tfrac{7n}{10} + 2. $$

*Proof.* The item $x$ has rank $\lceil g/2 \rceil$ in $M$. So at least $\lceil g/2 \rceil$ medians are at most $x$. In a full group of 5, the median and the two items below it are at most the median, so at most $x$. The last group may have $r < 5$ items, and then at least $\lceil r/2 \rceil \ge 1$ of them are at most its median. So at least $3\lceil g/2 \rceil - 2 \ge 3n/10 - 2$ items are at most $x$, and $|G| \le 7n/10 + 2$. In the same way, at least $g - \lceil g/2 \rceil + 1 = \lfloor g/2 \rfloor + 1$ medians are at least $x$, each full group gives 3 items at least $x$, and the last group gives at least one. So at least $3\lfloor g/2 \rfloor + 1 \ge 3(n/5 - 1)/2 + 1 = 3n/10 - 1/2$ items are at least $x$, and $|L| \le 7n/10 + 1/2$. $\square$

**Time, $\Theta(n)$ in each case.** Let $T(n)$ be the largest time of SELECT on a list of at most $n$ items, so $T$ does not decrease. Lines L2, L3, L5 and the tests take at most $an$ time for a constant $a$. By the bound, for $n \ge 6$,

$$ T(n) \le T(\lceil n/5 \rceil) + T(\lfloor 7n/10 + 2 \rfloor) + an. $$

By the [substitution method](/substitution-method/), $T(n) \le cn$ for $c = \max(20a, \max_{n < 60} T(n)/n)$. For $n < 60$ this is the choice of $c$. For $n \ge 60$, the induction hypothesis gives $T(n) \le c(n/5 + 1) + c(7n/10 + 2) + an = cn - (cn/10 - 3c - an)$, and $cn/10 - an \ge cn/20 \ge 3c$ because $c \ge 20a$ and $n \ge 60$. So $T(n) = O(n)$. Each run reads each item at least once in line L5, so the time is also $\Omega(n)$, in the best, the average and the worst case. The key fact is $1/5 + 7/10 = 9/10 < 1$: the two calls together get at most nine tenths of the items, plus a constant.

**Comparisons.** Line L3 makes at most $10$ comparisons per group, so at most $2n$, and line L5 makes at most $2$ per item, so at most $2n$. The recurrence then gives a bound of about $40n$. In practice the version above makes far fewer: for the median of $10^5$ random items it makes $11.5n$ comparisons, and of $10^5$ sorted items $9.1n$. The original algorithm PICK was tuned to at most $5.4305n$ comparisons in the worst case, and the best known median algorithm, by Dor and Zwick, makes fewer than $2.95n$.

**Space, $\Theta(n)$.** This version builds the lists $M$, $L$, $E$ and $G$, of total size $O(n)$ at each level, and the list sizes along a chain of calls shrink geometrically, so the extra space is $O(n)$. The depth of the recursion is $O(\log n)$. An in-place version, as in CLRS, moves the group medians to the front of the array and partitions in place, with $O(\log n)$ space for the stack.

## Properties

- **Deterministic.** The worst case is linear on every input, with no random choices.
- **Not in place in this form.** The lists of line L5 take $\Theta(n)$ space; the in-place form needs only the stack.
- **Comparison-based.** It uses only comparisons, so it works for any total order.
- **Partition as a by-product.** The lists $L$, $E$ and $G$ split the input around the answer at the last level, so the $k$ smallest items come out at no extra cost.

## Variants and improvements

- **Other group sizes.** Groups of 7 also give linear time, since $1/7 + 5/7 < 1$. With groups of 3 the recurrence becomes $T(n) = T(n/3) + T(2n/3) + O(n)$, whose solution is $\Theta(n \log n)$, so the analysis above fails. Chen and Dumitrescu (2015) gave modified methods with groups of 3 and of 4 that do run in linear time.
- **Pivot for other methods.** The same pivot makes [quicksort](/quicksort/) run in $O(n \log n)$ time in the worst case. A fast approximate version, the median of medians of medians without full recursion, is a good pivot heuristic ([pivot selection](/pivot-selection/)).
- **Introselect.** [Introselect](/introselect/) runs quickselect and switches to median of medians only when the ranges stop shrinking. This keeps the linear worst case and the speed of quickselect.
- **Fewer comparisons.** PICK and later methods by Schönhage, Paterson and Pippenger, and by Dor and Zwick, reduce the constant for the median to below $3$. They are of theoretical interest.
- **Weighted median.** The same pivot, with weights summed in line L5, finds a [weighted median](/weighted-median-post-office-location/) in linear time.

## When to use it

Use median of medians when the worst case matters more than the speed of a typical run, for example when an adversary can choose the input, or in a proof that a method takes linear time. In practice, [quickselect](/quickselect/) with a random pivot is several times faster on typical inputs, since it makes fewer than $4n$ comparisons in expectation against the $9n$ to $12n$ above, and [introselect](/introselect/) gets both. For the median of a very large data set with few comparisons, [Floyd-Rivest selection](/floyd-rivest-select/) is the fastest.

## Pitfalls

- **Recursion on the wrong rank.** Line L4 asks for rank $\lceil g/2 \rceil$ of $M$, not rank $k$. A call SELECT$(M, k)$ is wrong for large $k$ and does not give a balanced pivot.
- **Two-way partition with repeated items.** A split into "less than $x$" and "at least $x$" can keep all items when they are all equal, and the recursion does not shrink. Line L5 uses three parts and line L7 returns $x$ directly.
- **No base case for small lists.** Without line L1, a list of 1 to 5 items makes a list $M$ of one item, and SELECT$(M, 1)$ calls itself forever. The base case must cover all $n \le 5$, or the call must stop when $|M| = 1$.
- **Forgetting the last group.** When $5 \nmid n$, the last group has fewer than 5 items. Code that takes $\lfloor n/5 \rfloor$ groups loses up to 4 items, and the answer can be wrong.

## Implementations

## History

Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan published the algorithm in "Time bounds for selection" in the Journal of Computer and System Sciences in 1973. Their version, PICK, makes at most $5.4305n$ comparisons. The paper also proved a new lower bound on the number of comparisons that selection needs. Schönhage, Paterson and Pippenger lowered the upper bound for the median to $3n + o(n)$ in 1976, and Dor and Zwick to fewer than $2.95n$ in 1999.

## References
