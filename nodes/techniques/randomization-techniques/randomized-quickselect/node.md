---
tag: 3SWVRD
kind: algorithm
slug: randomized-quickselect
name: Randomized quickselect
aliases:
- randomized select
- Hoare's FIND
- random-pivot selection
area: techniques/randomization-techniques
level: intro
summary: Selects the k-th smallest element using a random pivot, with O(n) expected time.
solves: [selection-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n^2), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: false, comparison: true, in_place: true, recursive: false}
history:
  year: 1961
  people: [C. A. R. Hoare]
  note: Hoare published the selection procedure FIND as Algorithm 65 in the Communications of the ACM in 1961, next to Quicksort.
prereqs: [selection-problem, randomized-algorithm, expected-running-time, lomuto-partition]
see_also: [quickselect, randomized-quicksort, median-of-medians, floyd-rivest-select, introselect, dutch-national-flag-algorithm, order-statistic, selection-lower-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.2, Selection in expected linear time (RANDOMIZED-SELECT and the proof of its expected linear time)
  - paper: doi:10.1145/366622.366647
    title: C. A. R. Hoare, Algorithm 65, Find, Communications of the ACM 4(7) (1961)
    locator: pp. 321 to 322
  - paper: doi:10.1145/360680.360691
    title: Robert W. Floyd and Ronald L. Rivest, Expected time bounds for selection, Communications of the ACM 18(3) (1975)
    locator: pp. 165 to 172 (selection by a random sample, and the expected number of comparisons n + min(k, n - k) + o(n))
---

Randomized quickselect finds the item of rank $k$ in an unsorted array: it picks a pivot uniformly at random, partitions the array around it, and continues only in the part that holds rank $k$. It makes $\Theta(n)$ comparisons in expectation on every input, at most $4n$ three-way comparisons, and it works in place. Its worst case is $\Theta(n^2)$, but the coins and not the input decide when it happens.

## In plain words

You want the fifth smallest card in a shuffled hand, but you do not want to sort the hand. Pick one card at random. Put the smaller cards on its left, the equal cards with it, and the larger cards on its right. Now count. If the left pile has five or more cards, the answer is there, and you throw the rest away. If the left pile and the equal cards together have fewer than five, the answer is on the right. Otherwise the card you picked is the answer.

Each time, you keep only one pile. A random card is usually not near the edge, so the pile you keep is usually much smaller. Most of the work is in the first rounds, and the total is a small multiple of the number of cards.

## The problem

Given an array $A[0 \ldots n-1]$ of items from a total order and an integer $k$ with $0 \le k < n$, return the item of rank $k$: the item at index $k$ of a sorted copy of $A$. This is the [selection problem](/selection-problem/). The minimum is $k = 0$, and the lower median is $k = \lfloor (n - 1)/2 \rfloor$. Equal items are allowed. The algorithm may reorder $A$.

## The algorithm

The array range $A[lo \ldots hi - 1]$ always holds the answer. A round draws a pivot from it, splits it into three parts with a three-way partition (the [Dutch national flag](/dutch-national-flag-algorithm/) method), and keeps one part.

```pseudo id=main
RANDOMIZED-QUICKSELECT(A, k)                     ▷ 0 ≤ k < n; returns the item of rank k
L1  lo ← 0; hi ← n
L2  while true
L3      i ← a uniform random integer in [lo, hi − 1]
L4      p ← A[i]
L5      (lt, gt) ← PARTITION3(A, lo, hi, p)
L6      if k < lt then hi ← lt                   ▷ the answer is < p
L7      else if k ≥ gt then lo ← gt              ▷ the answer is > p
L8      else return A[k]                         ▷ lt ≤ k < gt, so the answer is p

PARTITION3(A, lo, hi, p)                         ▷ afterwards A[lo..lt−1] < p, A[lt..gt−1] = p, A[gt..hi−1] > p
L9  lt ← lo; i ← lo; gt ← hi
L10 while i < gt
L11     if A[i] < p then swap A[lt], A[i]; lt ← lt + 1; i ← i + 1
L12     else if A[i] > p then gt ← gt − 1; swap A[i], A[gt]
L13     else i ← i + 1
L14 return (lt, gt)
```

Each pass of the loop L10 to L13 makes one three-way comparison of $A[i]$ with $p$, so PARTITION3 makes $hi - lo$ of them. The middle part holds at least the pivot, so it is never empty, and each round that does not return removes it. With only two parts, as in the [Lomuto partition](/lomuto-partition/) of CLRS, an array of equal keys keeps all but one item in each round and costs $\Theta(n^2)$ on every run.

## Example

Let $A = [7, 2, 9, 4, 4, 1, 8, 5]$ and $k = 3$. A sorted copy is $[1, 2, 4, 4, 5, 7, 8, 9]$, so the answer is 4. Assume the random indices drawn at line L3 are 6, 0 and 2.

| round | $lo$, $hi$ | $i$ | pivot $p$ | $A$ after PARTITION3 | $lt$, $gt$ | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0, 8 | 6 | 8 | [7, 2, 5, 4, 4, 1, **8**, 9] | 6, 7 | $k < 6$: $hi \leftarrow 6$ |
| 2 | 0, 6 | 0 | 7 | [2, 5, 4, 4, 1, **7**, 8, 9] | 5, 6 | $k < 5$: $hi \leftarrow 5$ |
| 3 | 0, 5 | 2 | 4 | [2, 1, **4, 4**, 5, 7, 8, 9] | 2, 4 | $2 \le k < 4$: return 4 |

The three rounds make $8 + 6 + 5 = 19$ three-way comparisons. In round 3 the two copies of 4 go to the middle part together, and the search stops at once.

## Correctness

At the start of each round, three facts hold, as the [proof](proofs/correctness) shows. The items of $A$ are those of the input. Each item left of $lo$ is at most each item in $A[lo \ldots hi - 1]$, which is at most each item right of $hi - 1$. And $lo \le k < hi$. So the item of rank $k$ of $A$ is in the range, and its rank there is $k - lo$. After PARTITION3, the parts $< p$, $= p$ and $> p$ are in this order, so the three tests of lines L6 to L8 keep the facts true, and when $lt \le k < gt$ the item at index $k$ is $p$, the answer.

The loop stops on every run, not only with probability 1: each round that does not return removes the middle part, which holds at least one item. So there are at most $n$ rounds.

## Complexity

Count three-way comparisons; a round on a range of size $m$ makes $m$ of them.

- **Expected, every input:** at most $4n$. Sort the range by value, with ties broken by index, and let $r$ be the position of the pivot in this order. Then $r$ is uniform in $\{0, \ldots, m - 1\}$, and the kept part has at most $\max(r, m - 1 - r)$ items. Induction gives $\bar C(m) \le m + \frac{2}{m}\sum_{j = \lfloor m/2 \rfloor}^{m - 1} 4j \le m + 3m = 4m$, because the sum is at most $3m^2/8$. This is the argument of CLRS, Section 9.2.
- **Worst case:** $n + (n - 1) + \cdots + 1 = n(n + 1)/2$ comparisons, when each pivot is the item farthest from rank $k$ in its range. For distinct keys and $k = 0$, each round must pick the largest item, which has probability $1/n!$ in total.
- **Best case:** $n$ comparisons, when the first pivot has rank $k$.
- **Space:** $O(1)$ extra words. The loop replaces the tail recursion.

The bound $4n$ is not tight. For $n$ distinct keys and the classic count of $m - 1$ two-way comparisons in a round, the exact mean for rank $k$ (1-based $k_1 = k + 1$) is

$$ 2\big((n + 1)H_n - (n + 3 - k_1)H_{n + 1 - k_1} - (k_1 + 2)H_{k_1} + n + 3\big), $$

where $H_j$ is the $j$-th harmonic number. It is largest at the median, where it is $2(1 + \ln 2)n + o(n) \approx 3.386n$.

| $n$ | mean for the minimum | mean for the median | mean for the median, divided by $n$ |
| --- | --- | --- | --- |
| 10 | 14.14 | 19.27 | 1.93 |
| 100 | 189.63 | 306.94 | 3.07 |
| 1,000 | 1,985.03 | 3,336.33 | 3.34 |

Every algorithm in the [comparison model](/comparison-model/) needs at least $n - 1$ comparisons, since the comparisons must link all $n$ items into one connected graph: otherwise the values of one part could be shifted without a change in any outcome, and the item of rank $k$ would change, see [selection lower bound](/selection-lower-bound/). So randomized quickselect is optimal up to a constant factor.

## Properties

- **Las Vegas.** The answer is always correct. Only the running time depends on the coins. See [randomized algorithm](/randomized-algorithm/).
- **In place.** It moves items inside $A$ and uses $O(1)$ extra words. As a side effect, $A[k]$ holds the answer, and the items before index $k$ are at most it, and those after are at least it, so $A$ is partitioned around rank $k$.
- **Not stable**, and it does not keep the input order.
- **Input-oblivious bound.** The expected bound holds for each input, including sorted and reversed arrays and arrays of equal keys.
- **Tail.** By [Markov's inequality](/markov-inequality/), more than $40n$ comparisons happen with probability at most $1/10$. A sharper argument with the phases of the analysis gives an exponentially small tail for $cn$ with a large constant $c$.

## Variants and improvements

- **Deterministic pivot.** [Quickselect](/quickselect/) with a fixed pivot rule has the same mean on a random input order, but some inputs force $\Theta(n^2)$ on each run.
- **Median of medians.** The pivot rule of Blum, Floyd, Pratt, Rivest and Tarjan (1973) gives a worst case of $O(n)$, at a larger constant. See [median of medians](/median-of-medians/).
- **Introselect.** [Introselect](/introselect/) runs quickselect and switches to median of medians when the ranges do not shrink fast enough. It keeps the speed of the random pivot and the linear worst case. The `nth_element` of C++ libraries is of this kind.
- **Sampling, Floyd and Rivest.** [Floyd-Rivest selection](/floyd-rivest-select/) picks two pivots from a random sample so that rank $k$ falls between them with high probability, and makes $n + \min(k, n - k) + o(n)$ comparisons in expectation.
- **Median of three or a ninther.** A pivot that is the median of a few random items lowers the constant of the mean.
- **Several ranks.** To find several ranks at once, recurse into each part that holds one of them. For the $k$ smallest items in order, select rank $k - 1$ and sort the first $k$ items, which is [partial sorting](/partial-sorting/).

## When to use it

Use it when you need one [order statistic](/order-statistic/), such as a median or a percentile, of data in memory, once. It is faster in practice than median of medians and than sorting. If the same array gets many rank queries, sort it once. If an adversary can see or predict your random generator, or if you need a hard time limit, use introselect or median of medians. For a stream that does not fit in memory, use a selection method for streams instead.

## Pitfalls

- **Two-way partition and equal keys.** With a partition into $\le p$ and $> p$, an array of $n$ equal items loses one item in each round and costs $n(n + 1)/2$ comparisons on every run. The three-way partition stops after the first round.
- **Off by one in the rank.** CLRS uses $i$ from 1 to $n$, and this page uses $k$ from 0 to $n - 1$. Mixing them returns the neighbour of the answer. Check the minimum and the maximum.
- **A fixed or predictable generator.** A seed fixed in the code makes the algorithm deterministic, and an adversary can build an input that forces $\Theta(n^2)$.
- **Recursion depth.** A recursive version with a bad run of pivots can recurse $n$ times. The loop of lines L2 to L8 has no such depth.
- **The array is changed.** The input order is lost. Copy the array first if the caller still needs it.

## Implementations

## History

Hoare published FIND as Algorithm 65 in the Communications of the ACM in 1961, next to Quicksort, Algorithm 64. Blum, Floyd, Pratt, Rivest and Tarjan showed in 1973 that selection is possible in linear worst-case time. Floyd and Rivest (1975) gave the sampling method and its expected number of comparisons. Knuth computed the exact mean number of comparisons of the random-pivot version, the formula given in the complexity section. CLRS present the random-pivot version as RANDOMIZED-SELECT, with the proof of its expected linear time.

## References
