---
tag: QMZWKB
kind: algorithm
slug: library-sort
name: Library sort
aliases:
- gapped insertion sort
- pagesort
area: sorting/comparison-sorts
level: research
summary: Insertion sort into an array with deliberate gaps, giving expected O(n log n) time with few moves.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, ε: the fraction of extra slots}
  time: {worst: Θ(n²), average: O(n log n), best: Θ(n log n), comparisons: O(n log n)}
  space: {extra: Θ((1 + ε) n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: false, comparison: true, recursive: false}
history:
  year: 2004
  people: [Michael A. Bender, Martín Farach-Colton, Miguel A. Mosteiro]
  note: Bender, Farach-Colton and Mosteiro showed that insertion sort with gaps left in the array, like empty space on library shelves, runs in O(n log n) time with high probability.
prereqs: [insertion-sort, binary-search, randomized-algorithm, packed-memory-array]
see_also: [packed-memory-array, insertion-sort, shell-sort, tree-sort, patience-sorting, amortized-cost, randomized-quicksort, comparison-sort-lower-bound]
sources:
  - paper: "Michael A. Bender, Martín Farach-Colton and Miguel A. Mosteiro, Insertion sort is O(n log n), Theory of Computing Systems 39(3), 2006"
    locator: pp. 391 to 397 (library sort, its rounds of rebalancing, and the proof of O(n log n) time with high probability for a random insertion order)
  - paper: "Alon Itai, Alan G. Konheim and Michael Rodeh, A sparse table implementation of priority queues, ICALP 1981, LNCS 115"
    locator: pp. 417 to 431 (keeping a sorted array with gaps under insertions, the idea behind the packed-memory array)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Sorting by insertion (binary insertion and the cost of moving records)
---

Library sort is [insertion sort](/insertion-sort/) into an array that has empty slots between its items. A librarian who leaves some empty space on each shelf can add a new book by moving only a few neighbours, not a whole shelf. In the same way, library sort finds the place of each new item by [binary search](/binary-search/) and shifts items only up to the nearest gap. It inserts the items in a random order, and each time the number of items doubles, it spreads them out again with even gaps. Bender, Farach-Colton and Mosteiro proved that this takes $O(n \log n)$ time with high probability, where plain insertion sort takes $\Theta(n^2)$. The price is $(1 + \varepsilon) n$ slots of extra space.

## In plain words

Plain insertion sort keeps the sorted items packed together. To put a new item in the middle, it must move every item after it by one place. That is why it is slow on long lists.

Library sort leaves empty slots between the items, like gaps on a bookshelf. To add an item, it finds its place by halving the search range, as in a dictionary. If there is a gap at that place, the item goes in at once. If not, it pushes a few neighbours along to the next gap.

The gaps fill up as items arrive. So each time the number of items doubles, it spreads all of them out again with fresh gaps. It also adds the items in a random order, so that no part of the shelf fills up much faster than the rest.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, which the algorithm can only compare with $<$. The output is the same array in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm may use $\Theta(n)$ extra slots and random bits. The version on this page also keeps items with equal keys in their input order.

## The algorithm

```pseudo id=main
LIBRARY-SORT(A, ε)
L1  choose a random order π of the positions 0, …, n − 1      ▷ the insertion order
L2  k ← 1; the list of placed items is (A[π(0)])
L3  while k < n do                                            ▷ one round
L4      m ← min(2k, n); L ← ⌊(1 + ε) m⌋ + 1
L5      S ← L empty slots; put the j-th placed item in slot ⌊(2j + 1) L / (2k)⌋
L6      for t ← k to m − 1 do INSERT(S, A[π(t)], π(t))
L7      k ← m; the placed items are the filled slots of S, in order
L8  copy the placed items back to A

INSERT(S, x, p)                       ▷ (y, i) comes before (x, p) if y < x, or y = x and i < p
L9  binary search over the slots, skipping empty ones, for the boundary b: the items in slots before b
    come before (x, p), and the items in slots from b on come after it
L10 q ← the last filled slot before b, or −1; r ← the first filled slot from b on, or L
L11 if r − q > 1 then put (x, p) in slot ⌊(q + r)/2⌋, which is empty
L12 else if there is an empty slot after r: let e be the first one; shift S[r … e−1] one slot right; put (x, p) in slot r
L13 else let e be the last empty slot before q; shift S[e+1 … q] one slot left; put (x, p) in slot q
```

**The search with gaps.** Line L9 keeps a range $[lo, hi)$ of slots such that the items before $lo$ come before $(x, p)$ and the items from $hi$ on come after it. It looks at the middle slot and, if that slot is empty, at the next filled slot in the range. If there is none, every slot from the middle to $hi$ is empty, and $hi$ moves to the middle. Otherwise one comparison decides which half to keep. The range shrinks at each step, so the search makes $O(\log L)$ comparisons, plus the time to skip gaps.

**Ties.** Each item carries its input position $p$, and equal keys are ordered by it. This makes all keys distinct, which the analysis needs, and it makes the sort stable. It costs a second comparison, $x$ against $y$ the other way, each time the first one says "not less".

## Example

Sort $A = [5, 1, 4, 2, 8, 0, 3, 6]$ with $\varepsilon = 1$, and, to keep the trace short, with the input order as the insertion order. An underscore is an empty slot.

| round | $L$ | slots after spreading | insertions | slots after the round |
|---|---|---|---|---|
| 1 | 5 | `_ _ 5 _ _` | 1 goes to slot 0 | `1 _ 5 _ _` |
| 2 | 9 | `_ _ 1 _ _ _ 5 _ _` | 4 to slot 4, 2 to slot 3 | `_ _ 1 2 4 _ 5 _ _` |
| 3 | 17 | `_ _ 1 _ _ _ 2 _ _ _ 4 _ _ _ 5 _ _` | 8 to slot 15, 0 to slot 0, 3 to slot 8, 6 by a shift | `0 _ 1 _ _ _ 2 _ 3 _ 4 _ _ _ 5 6 8` |

In round 3, the item 6 belongs between 5 in slot 14 and 8 in slot 15, with no gap. The first empty slot after 15 is 16, so 8 moves to slot 16 and 6 goes into slot 15. That is the only move of the whole sort; every other item found a gap. Copying the filled slots gives $[0, 1, 2, 3, 4, 5, 6, 8]$.

## Correctness

The placed items are always in order in the slots. Spreading keeps their order, because the target slots $\lfloor (2j+1) L / (2k) \rfloor$ increase with $j$. Each insertion puts $(x, p)$ between the last item that comes before it and the first item that comes after it, and the shifts of lines L12 and L13 move a block of neighbouring items by one slot without changing their order. There is always an empty slot, because a round holds at most $m < L$ items. Each item is inserted once, so at the end the slots hold all $n$ items in the order (key, input position), which is the stable sorted order. The full proof is below.

## Complexity

**Comparisons.** Each insertion makes $O(\log L) = O(\log n)$ comparisons in line L9, so the sort makes $O(n \log n)$ comparisons on every input and for every random order. With distinct keys and no tie test, this is about $n \lg n$; the test for ties adds up to one comparison per step.

**Rebalancing.** Round $r$ costs $O(L) = O((1 + \varepsilon) 2^r)$ to spread the items, so all rounds together cost $O((1 + \varepsilon) n)$.

**Moves.** This is the hard part. In the worst case the items of a round all land in one place, and each insertion shifts $\Theta(k)$ items, so the worst case is $\Theta(n^2)$. Bender, Farach-Colton and Mosteiro proved that with a random insertion order and any constant $\varepsilon > 0$, the shifts cost $O(n \log n)$ in total with high probability. The idea is that after spreading, a run of filled slots can only grow long if many random items fall into one small range of keys, which is unlikely. In practice the search also skips few empty slots, because the gaps are spread out. So library sort takes $O(n \log n)$ time with high probability. Measured with $n = 10^5$ and $\varepsilon = 1$:

| input | comparisons | per $n \lg n$ | items moved by shifts | per item |
|---|---|---|---|---|
| random keys | 2,292,582 | 1.38 | 60,048 | 0.60 |
| sorted | 2,291,033 | 1.38 | 60,277 | 0.60 |
| reversed | 2,294,078 | 1.38 | 60,288 | 0.60 |
| 10 distinct values | 2,919,876 | 1.76 | 61,159 | 0.61 |

Because of the random insertion order, the shape of the input does not matter. More space means fewer moves. On random keys with $n = 10^5$:

| $\varepsilon$ | items moved per item |
|---|---|
| 0.25 | 2.93 |
| 0.5 | 1.41 |
| 1 | 0.60 |
| 2 | 0.26 |

Plain insertion sort moves about $n^2/4 = 2.5 \times 10^9$ items for $n = 10^5$ random keys.

**Space.** The slot array has $(1 + \varepsilon) n + 1$ slots, and each slot holds an item and its input position.

## Properties

- **Stable, in this version.** Equal keys are ordered by input position. The analysis in the paper is for distinct keys.
- **Not in place.** It needs $\Theta((1 + \varepsilon) n)$ extra slots. See [in-place algorithm](/in-place-algorithm/).
- **Randomized.** Its time bound holds with high probability over its own random choices, for every input. The output does not depend on the random choices. See [randomized algorithm](/randomized-algorithm/).
- **Not adaptive.** The random order destroys any presortedness in the input.
- **Few moves for each insertion.** The expected number of items moved per insertion is a constant that depends on $\varepsilon$, as the table shows.

## Variants and improvements

- **Packed-memory array.** Library sort is a sort built on a gapped array. The [packed-memory array](/packed-memory-array/) of Itai, Konheim and Rodeh, and of Bender, Demaine and Farach-Colton, keeps a sorted array with gaps under any sequence of insertions, not only random ones, by rebalancing windows of the array whose density gets too high. It costs $O(\log^2 n)$ amortized moves per insertion in the worst case. Using it in place of the rounds gives a sort with $O(n \log^2 n)$ moves with no randomness.
- **Online use.** Without the random order the method can take items one at a time as they arrive. Then the bounds of the paper do not hold, and the density-based rebalancing of the packed-memory array is needed for a guarantee.
- **Other ways to make insertion fast.** A balanced search tree, as in [tree sort](/tree-sort/), inserts in $O(\log n)$ worst-case time, with pointers instead of gaps. [Shell sort](/shell-sort/) speeds up insertion sort by moving items over long distances first.

## When to use it

Library sort is mainly of interest for its analysis: it shows that the cost of insertion sort comes from the shifting, and that a constant fraction of extra space removes it. In practice, a merge sort or quicksort is faster. The gapped-array idea is useful when the data must stay as a sorted array that receives insertions over time, as in an index or a database page; there the [packed-memory array](/packed-memory-array/) is the usual form.

## Pitfalls

- **Skipping the random order.** On a sorted input inserted in order, each round fills the gaps at the right end first, and later items must shift long runs. With $n = 10^4$ this costs 17,674,953 item moves, against 5,800 with a random order.
- **Ties with no tie-break.** If equal keys are not made distinct, every copy of a key goes to the same boundary, the slots there fill up, and the shifts grow long. With 10 distinct values among $10^5$ items, inserting each new copy after the existing ones costs about 66 million moves. Ordering ties by a random or input position avoids this.
- **A gap search that runs past the range.** When the middle slot is empty, the scan for a filled slot must stop at $hi$. If it goes further, it reads an item that the invariant says nothing about, and the search can go wrong.
- **No room left.** Each round must hold all its items with some gaps left, so $L$ must exceed the number of items the round ends with. Line L4 gives $L > (1 + \varepsilon) m$.

## Implementations

## History

The idea of leaving gaps in a sorted array to make insertions cheap goes back at least to the sparse tables of Itai, Konheim and Rodeh (1981). Bender, Farach-Colton and Mosteiro presented library sort in 2004 under the title "Insertion sort is $O(n \log n)$", with the journal version in Theory of Computing Systems in 2006. They compared it to a librarian who keeps gaps on the shelves, and proved its $O(n \log n)$ bound with high probability for a random insertion order.

## References
