---
tag: 358AT6
kind: technique
slug: coordinate-compression
name: Coordinate compression
aliases:
- discretization
- value compression
area: techniques/reductions-and-transforms
level: intro
summary: Replacing large coordinate or value ranges by their ranks among the values actually present, to shrink the index space.
prereqs: [sorting-problem, binary-search, order-statistic]
see_also: [fenwick-tree, segment-tree, inversion-count-with-fenwick-tree, counting-inversions, interval-union-length, area-of-union-of-rectangles, hash-table, transform-and-conquer]
sources:
  - book: isbn:9783030393564
    title: Antti Laaksonen, Guide to Competitive Programming, second edition, Springer, 2020
    locator: Chapter 9, Range Queries (index compression)
  - paper: doi:10.1002/spe.4380240306
    title: "Peter M. Fenwick, A new data structure for cumulative frequency tables, Software: Practice and Experience 24(3) (1994), 327-336"
    locator: the binary indexed tree, whose array is indexed by the compressed values
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Problem 2-4, Inversions
---

Coordinate compression replaces each value of a set $V$ of $m$ distinct values, taken from a large or infinite ordered domain, by its [rank](/order-statistic/) in $V$: an integer from $0$ to $m - 1$ (or $1$ to $m$). The map keeps the order and the equalities of the values, so an algorithm that only compares values gets the same answer on the ranks. Its use is to make arrays indexed by value small enough to store, for example the array of a [Fenwick tree](/fenwick-tree/) or a [segment tree](/segment-tree/) over values up to $10^9$ when only $10^5$ of them occur. The cost is one sort, $O(n \log n)$ for $n$ input values.

## In plain words

Suppose a list holds a few numbers, but some are very large, such as one billion. You want an array with one cell for each possible number. An array with a billion cells is too big.

Only the order of the numbers matters for many questions: which is larger, which are equal. So give each number its place in the sorted list of the different numbers that occur. The smallest one gets place one, the next one place two, and so on. Equal numbers get the same place. Now an array with one cell for each place is small, and every comparison gives the same result as before.

The places lose the distances between the numbers. If the problem needs lengths or sums of values, keep the original numbers beside the places.

## When it applies

- The values come from a large domain (integers up to $10^9$ or $10^{18}$, reals, strings), but there are only $n$ of them.
- The algorithm needs an array indexed by value: a counting array, a Fenwick tree, a segment tree, a grid of cells.
- The algorithm uses the values only through comparisons, or it can get every other quantity it needs from the original values by rank.
- All values that the algorithm will ever look up are known before it starts (offline processing). This includes the values in the queries.

## The template

Let $V$ be the set of values that occur, with $m = |V|$ distinct values and $v_0 < v_1 < \cdots < v_{m-1}$. The compression map is $r(v_k) = k$. Equivalently, $r(x) = |\{\, v \in V : v < x \,\}|$.

**Order preservation.** For all $x, y \in V$: $x < y \iff r(x) < r(y)$, and $x = y \iff r(x) = r(y)$. *Proof.* If $x = v_i$ and $y = v_j$, then $r(x) = i$ and $r(y) = j$, and $v_i < v_j \iff i < j$ because the $v_k$ are listed in increasing order and are distinct. The case of equality follows in the same way. $\square$

So a comparison-based algorithm that runs on the ranks makes the same branches as on the values, and the answer is the same, up to mapping ranks back by $v_{r}$.

```pseudo id=main
COMPRESS(A, n)                       ▷ A[0 .. n − 1], values from an ordered domain
L1  X ← copy of A
L2  SORT(X)
L3  m ← 0
L4  for i ← 0 to n − 1 do               ▷ UNIQUE: keep the first of each run
L5      if i = 0 or X[i] ≠ X[i − 1] then
L6          X[m] ← X[i];  m ← m + 1
L7  for i ← 0 to n − 1 do
L8      R[i] ← LOWER-BOUND(X[0 .. m − 1], A[i])   ▷ the k with X[k] = A[i]
L9  return (R, X[0 .. m − 1])        ▷ ranks 0 .. m − 1, and the inverse map
```

Line L2 sorts in $O(n \log n)$ time. Lines L3 to L6 keep one copy of each value in $O(n)$ time, so $X[0 \ldots m-1]$ lists $v_0 < \cdots < v_{m-1}$. Line L8 is a [binary search](/binary-search/) for the first position $k$ with $X[k] \ge A[i]$; since $A[i] \in V$, $X[k] = A[i]$ and $k = r(A[i])$. The $n$ searches take $O(n \log m)$ time. A [hash table](/hash-table/) from $v_k$ to $k$, filled after L6, gives each rank in $O(1)$ expected time instead. In total the method takes $O(n \log n)$ time and $O(n)$ space. The array $X$ is the inverse map: rank $k$ stands for the value $X[k]$.

## Classic examples

### Counting inversions with large values

An [inversion](/inversion/) of $A$ is a pair $i < j$ with $A[i] > A[j]$. The [Fenwick tree method](/inversion-count-with-fenwick-tree/) scans $A$ from left to right, and for each $A[j]$ it counts the earlier items that are greater, with a tree indexed by value. With values up to $10^9$, the tree is indexed by rank instead.

Let $A = (10^9, 5, 300, 5, 70000, 300)$. The distinct values are $5 < 300 < 70000 < 10^9$, so with 1-based ranks $A$ becomes $(4, 1, 2, 1, 3, 2)$. The tree has $4$ cells instead of $10^9$. For each $j$, the number of earlier items greater than $A[j]$ is $j - (\text{number of earlier ranks} \le r(A[j]))$, with $j$ counted from $0$. These counts are $0, 1, 1, 2, 1, 2$, and the number of inversions is $7$. Since compression keeps every comparison, this is also the count for the original values. The total time is $O(n \log n)$. [Merge sort counting](/inversion-count-by-merge-sort/) needs no compression, but the tree method extends to queries that the merge method does not handle, such as counts of items in a value range.

### Grids over sparse coordinates

For the [area of a union of rectangles](/area-of-union-of-rectangles/) with $n$ rectangles and coordinates up to $10^9$, compress the $x$ coordinates and the $y$ coordinates separately. The plane becomes a grid of at most $(2n - 1)^2$ cells. Cell $(i, j)$ stands for the real rectangle $[x_i, x_{i+1}) \times [y_j, y_{j+1})$, and its area is $(x_{i+1} - x_i)(y_{j+1} - y_j)$ in the original coordinates. Marking the cells gives an $O(n^3)$ algorithm; a [sweep with a segment tree](/rectangle-union-sweep/) over the compressed $y$ coordinates gives $O(n \log n)$.

### Offline range queries

When a sequence of insertions and queries "how many stored values lie in $[a, b]$?" is known in advance, collect all stored values and all query endpoints, compress them together, and answer with a Fenwick tree over the ranks. The query $[a, b]$ becomes the rank range $[r(a), r(b)]$.

## Variations

- **0-based or 1-based ranks.** A Fenwick tree is usually 1-based: use $r(x) + 1$. A segment tree or a plain array is usually 0-based.
- **Ranks with ties broken.** To make all ranks distinct, sort the pairs $(A[i], i)$ and give rank $k$ to the $k$th pair. Equal values then get different ranks in input order. The ranks then form a permutation of $0, \ldots, n - 1$. A pair of equal items keeps its input order, so it is still not an inversion. But the copies of one value now occupy several cells, so a query for the items equal to $x$ becomes a range of ranks.
- **Hash map instead of binary search.** After the sort, store $v_k \mapsto k$ in a hash table. The lookups take $O(1)$ expected time each, but the sort still costs $O(n \log n)$.
- **Integer values.** For integers of $O(\log n)$ bits, a [radix sort](/radix-sort/) in line L2 makes the whole method $O(n)$.
- **Compression with gaps.** If the algorithm must tell "$x$ and $y$ are adjacent integers" from "there are integers between $x$ and $y$", insert $x + 1$ for each value $x$ before compressing, so that the gaps stay visible.

## Pitfalls

- **Lengths in rank space.** Ranks keep the order but not the distances. For the [union length](/interval-union-length/) of $[1, 4]$, $[2, 10]$ and $[20, 25]$, the endpoints $1, 2, 4, 10, 20, 25$ get ranks $0$ to $5$. The union covers the rank segments $[0, 3]$ and $[4, 5]$. Measured in ranks, its length is $3 + 1 = 4$, which is wrong. Measured with the original coordinates, each covered segment $[k, k+1]$ adds $X[k+1] - X[k]$, and the length is $9 + 5 = 14$, which is right. Use ranks to index the array and the original values to measure.
- **Values not in the compressed set.** LOWER-BOUND on a value $x \notin V$ returns the rank of the next larger value, not an error. A query endpoint that was not compressed then lands on the wrong cell. Compress the query values with the data, or treat the result of LOWER-BOUND as a boundary, with care at both ends of a range.
- **Duplicates.** Without the UNIQUE step, two copies of the same value get different ranks if found by position, or the binary search returns the first copy and the ranks have holes. Keep one copy of each value.
- **Off by one.** A Fenwick tree with index $0$ loops forever in the usual update loop $i \leftarrow i + (i \mathbin{\&} -i)$. Shift 0-based ranks by one.
- **Online data.** If the values arrive one at a time and are not known in advance, the ranks change when a new value comes. Use a balanced [binary search tree](/binary-search-tree/) or a structure over the full domain instead.
- **Float keys.** Two reals that should be equal may differ in the last bit, and then they get different ranks. Round to a fixed precision, or work with exact values, before the sort.

## Exercises

1. Compress $A = (42, -7, 42, 10^{12}, 0, -7)$ to 0-based ranks and give the inverse map.
2. Given $n$ points with integer coordinates up to $10^9$, count for each point the points that are strictly below and strictly to the left of it, in $O(n \log n)$ time.
3. Prove that if an algorithm uses its input values only in comparisons $x < y$ and $x = y$, then its output on the ranks is the image of its output on the values.
4. Given $n$ closed intervals with endpoints up to $10^9$, find a point covered by the most intervals. Explain why compressing only the endpoints is enough.
5. Give an example in which an algorithm on compressed values gives a wrong answer because a query value was not in the compressed set.

## References
