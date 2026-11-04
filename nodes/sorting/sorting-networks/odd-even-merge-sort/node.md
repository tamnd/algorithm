---
tag: 0H3K90
kind: algorithm
slug: odd-even-merge-sort
name: Odd-even merge sort
aliases:
- Batcher's odd-even merge sort
- odd-even merging network
area: sorting/sorting-networks
level: core
summary: Batcher's network that sorts by recursively merging sorted halves with odd-even merges, with O(log^2 n) depth.
solves: [sorting-problem]
model: sorting-network
complexity:
  vars: {n: the number of items, a power of 2 in the exact counts}
  time: {worst: Θ(n log² n), average: Θ(n log² n), best: Θ(n log² n)}
  space: {extra: Θ(log n)}
  depth: {worst: Θ(log² n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1968
  people: [Kenneth E. Batcher]
  note: Batcher gave the odd-even merge and the bitonic sorter in one paper at the 1968 Spring Joint Computer Conference.
prereqs: [merging-network, merge-sort, zero-one-principle]
see_also: [bitonic-sort, pairwise-sorting-network, merging-network, network-size, network-depth, minimum-size-sorting-network, shell-sort, merge-sort]
sources:
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32 (1968)
    locator: pp. 307 to 314
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Algorithm M (merge exchange), and Section 5.3.4, Networks for sorting (Batcher's odd-even merge)
  - book: isbn:9780201314526
    title: Robert Sedgewick, Algorithms in C, Parts 1 to 4, third edition
    locator: Chapter 11, Special-purpose sorting methods (Batcher's odd-even merge)
---

Odd-even merge sort is Batcher's [sorting network](/sorting-network/) that sorts $n = 2^k$ items with $\tfrac14 n k (k - 1) + n - 1$ [comparators](/comparator/) in $\tfrac12 k (k + 1)$ layers. It has the shape of [merge sort](/merge-sort/): sort the two halves, then merge them. The merge is a [merging network](/merging-network/) that merges the items at even positions and the items at odd positions on their own, and then fixes the result with one layer of comparators. Its [depth](/network-depth/) is the same as that of [bitonic sort](/bitonic-sort/), and it uses fewer comparators. In Knuth's merge exchange form, its [size](/network-size/) is the smallest possible for each $n \le 8$.

## In plain words

Take two sorted lists of the same length, and number the places from zero. Split each list into the items at even places and the items at odd places. Merge the even items of both lists into one sorted list, and merge the odd items of both lists into one sorted list, with the same method. Now put the two results back together, one even item, then one odd item, and so on.

The result is almost sorted. An item can be out of place only by one step, so one more round that compares each odd place with the next place finishes the merge. To sort, sort each half and merge them, as in merge sort.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, where $n = 2^k$. The output is the same array in non-decreasing order. The method must be a fixed sequence of compare-exchange steps: which pairs it compares can depend on $n$, but not on the items. This is the [sorting problem](/sorting-problem/) in the [sorting network](/sorting-network/) model. Other values of $n$ are handled in [Variants and improvements](#variants-and-improvements).

## The algorithm

The call OEM-SORT$(A, 0, n)$ sorts the full array. ODD-EVEN-MERGE$(A, lo, m, r)$ works on the subsequence $A[lo], A[lo + r], A[lo + 2r], \ldots, A[lo + m - r]$ of $m / r$ items, with stride $r$. The first half and the second half of this subsequence must be sorted, and the call merges them. All of $m$, $r$ and $m / r$ are powers of 2.

```pseudo id=main
OEM-SORT(A, lo, m)                         ▷ sort A[lo .. lo + m − 1]
L1  if m ≤ 1 then return
L2  h ← m / 2
L3  OEM-SORT(A, lo, h)
L4  OEM-SORT(A, lo + h, h)
L5  ODD-EVEN-MERGE(A, lo, m, 1)

ODD-EVEN-MERGE(A, lo, m, r)                ▷ merge the two halves of A[lo], A[lo + r], .., A[lo + m − r]
L6  s ← 2r
L7  if s < m then
L8      ODD-EVEN-MERGE(A, lo, m, s)        ▷ the items at even places
L9      ODD-EVEN-MERGE(A, lo + r, m, s)    ▷ the items at odd places
L10     for i ← lo + r, lo + r + s, lo + r + 2s, .. while i + r < lo + m do COMPARE(A, i, i + r)
L11 else COMPARE(A, lo, lo + r)            ▷ two items: one comparator

COMPARE(A, i, j)                           ▷ a comparator [i:j], with i < j
L12 if A[i] > A[j] then exchange A[i] and A[j]
```

In the subsequence of a call, the items at even places are $A[lo], A[lo + 2r], \ldots$, which is the subsequence of stride $s = 2r$ from $lo$. The items at odd places are the subsequence of stride $s$ from $lo + r$. Line L10 compares place 1 with place 2, place 3 with place 4, and so on, in the subsequence of the call. The comparators of line L10 have disjoint wires, so they form one layer. All comparators put the minimum on the lower wire.

The comparators that one call makes depend only on its arguments. So the calls on any array of length $n$ give one fixed list of comparators. To get the network itself, record the pairs of line L12 instead of comparing.

## Example

Sort $A = [1, 6, 8, 3, 2, 7, 5, 4]$.

| step | the array |
|---|---|
| sort the pairs: [0:1] [2:3] [4:5] [6:7] | 1 6 3 8 2 7 4 5 |
| merge pairs into fours | 1 3 6 8 2 4 5 7 |
| merge the even places of both fours | places 0, 2, 4, 6 hold 1 6 2 5, which become 1 2 5 6 |
| merge the odd places of both fours | places 1, 3, 5, 7 hold 3 8 4 7, which become 3 4 7 8 |
| put them together | 1 3 2 4 5 7 6 8 |
| line L10: [1:2] [3:4] [5:6] | 1 2 3 4 5 6 7 8 |

The last layer exchanges 3 and 2, and 7 and 6. It does not change 4 and 5. Each merge of four items, as in the second row, is the same method on a smaller scale: it has the comparators $[0:2], [1:3], [1:2]$ for the first four places. The full network for $n = 8$ has 19 comparators in 6 layers.

## Correctness

By the [zero-one principle](/zero-one-principle/) it is enough to show that ODD-EVEN-MERGE merges each input of zeros and ones. Suppose the first half of the subsequence has $a$ zeros and the second half has $b$ zeros. Then the items at even places hold $\lceil a/2 \rceil + \lceil b/2 \rceil$ zeros, and the items at odd places hold $\lfloor a/2 \rfloor + \lfloor b/2 \rfloor$ zeros, so the even part has 0, 1 or 2 more zeros than the odd part. After the two recursive merges and the interleave, the sequence is sorted in the first two cases, and in the third case it is sorted except for one pair 1, 0 at an odd place and the next place. Line L10 compares exactly such pairs, so it fixes that pair and changes nothing else. Then OEM-SORT is correct by induction on $m$, as merge sort is. The full proof is below.

## Complexity

Let $L = m / r$ be the number of items in a call of ODD-EVEN-MERGE. Its size $M(L)$ and its depth satisfy $M(2) = 1$ and $M(L) = 2 M(L/2) + L/2 - 1$, and the depth grows by one when $L$ doubles. So

$$M(L) = \tfrac12 L (\lg L - 1) + 1, \qquad \text{depth of the merge} = \lg L.$$

The two recursive calls of lines L8 and L9 have disjoint wires, so they run at the same time. For the sort, $S(n) = 2 S(n/2) + M(n)$ and $D(n) = D(n/2) + \lg n$, with $S(1) = D(1) = 0$. With $n = 2^k$:

$$S(n) = \tfrac14 n k (k - 1) + n - 1, \qquad D(n) = \tfrac12 k (k + 1).$$

| $n$ | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|
| size | 1 | 5 | 19 | 63 | 191 | 543 |
| depth | 1 | 3 | 6 | 10 | 15 | 21 |

Bitonic sort on 16 items needs 80 comparators, and odd-even merge sort needs 63. For $n = 4$ and $n = 8$ the sizes 5 and 19 are the smallest possible ([minimum-size sorting network](/minimum-size-sorting-network/)). For $n = 16$ the best known network has 60 comparators.

- **Sequential time.** $\Theta(n \log^2 n)$ in each case, because the network makes the same $S(n)$ comparisons on each input.
- **Parallel time.** With $n/2$ processors, the time is $D(n) = \Theta(\log^2 n)$.
- **Extra space.** $\Theta(\log n)$ for the recursion.

## Properties

- **Data oblivious.** The comparisons do not depend on the items.
- **In place.** It moves items only by exchanges.
- **Not stable.** The comparators of a merge join places far apart, and an item can pass over an equal item.
- **Not adaptive.** A sorted input costs the same $S(n)$ comparisons.
- **Less regular than bitonic sort.** The last layer of each merge compares places $2t + 1$ and $2t + 2$, which are not of the form $i$ and $i \oplus h$. So the network does not map onto a hypercube as directly as bitonic sort does.

## Variants and improvements

- **Any $n$.** Build the network for the next power of 2 and drop each comparator that touches a wire $j \ge n$. Think of the missing wires as holding $+\infty$: in a network of standard comparators such a wire keeps $+\infty$, and a comparator on it changes nothing. So the result sorts $n$ items. The Python code below does this.
- **Merge exchange.** Knuth's Algorithm M in Section 5.2.2 is Batcher's method for any $n$, written as a sequence of passes that compare $A[i]$ with $A[i + d]$. For $n = 1, \ldots, 16$ it has $0, 1, 3, 5, 9, 12, 16, 19, 26, 31, 37, 41, 48, 53, 59, 63$ comparators. This is fewer than the truncated network for $n = 9, \ldots, 12$, where the truncation gives $28, 32, 38, 42$.
- **The pairwise network.** Parberry's [pairwise sorting network](/pairwise-sorting-network/) first sorts pairs and then works on the smaller and the larger items of the pairs. It has the same size and the same depth as odd-even merge sort.
- **Smaller networks for fixed $n$.** For $n \ge 9$ there are networks with fewer comparators. See [minimum-size sorting network](/minimum-size-sorting-network/).

## When to use it

Use odd-even merge sort when you need a sorting network for a size that is not small, and the number of comparators matters: in hardware, in SIMD code and in oblivious algorithms. For a fixed small $n$, use a network from the tables of optimal networks. If the layers must have the form $i$ and $i \oplus h$, as on a hypercube, use [bitonic sort](/bitonic-sort/). On a single processor, [merge sort](/merge-sort/) does $O(n \log n)$ work and is faster.

## Pitfalls

- **The last layer.** Line L10 starts at place 1 of the subsequence, not at place 0. A layer that compares places 0 and 1, 2 and 3, and so on, does not fix the merge.
- **Halves that are not sorted.** ODD-EVEN-MERGE merges only two sorted halves. Without the calls of lines L3 and L4, it does not sort.
- **$n$ not a power of 2.** The recursion needs powers of 2. Pad with $+\infty$, drop the comparators on the extra wires, or use merge exchange.
- **The cost.** The network makes $\Theta(n \log^2 n)$ comparisons, more than an $O(n \log n)$ sequential sort.

## Implementations

## History

Kenneth Batcher described the odd-even merge and the bitonic sorter in "Sorting networks and their applications" at the 1968 Spring Joint Computer Conference. Knuth presents the method as a sequential sort, Algorithm M (merge exchange), in Section 5.2.2, and as a network in Section 5.3.4.

## References
