---
tag: 9MV358
kind: problem
slug: peak-finding
name: Peak finding
aliases:
- local maximum finding
- 1D peak finding
area: searching/sequential-and-binary-search
level: core
summary: Find an index whose value is at least as large as its neighbours, in O(log n) probes.
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(log n)}
prereqs: [binary-search]
see_also: [find-maximum, unimodal-maximum, lower-and-upper-bound-search, golden-section-search, local-search-problem, hill-climbing, bitonic-sequence, adversary-argument]
sources:
  - url: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
    title: Erik Demaine and Srini Devadas, MIT 6.006 Introduction to Algorithms, Fall 2011
    locator: Lecture 1, Algorithmic thinking, peak finding (the one- and two-dimensional problems)
---

Peak finding asks, for an array $A[0 \ldots n-1]$, for an index $i$ whose item is at least as large as each of its neighbours: a *local* maximum. A peak always exists, since the global maximum is one, but finding the global maximum needs $n - 1$ comparisons, while a peak can be found with about $\lg n$. The method is a [binary search](/binary-search/) on the slope: compare $A[mid]$ with $A[mid + 1]$, and go to the side that goes up. The side that goes up must hold a peak, because a walk uphill must stop somewhere. The same idea, with more care, finds a local maximum in a grid and is the simplest case of the [local search problem](/local-search-problem/).

## In plain words

You walk along a mountain path in fog, and you want to stand on any hilltop, not the highest one. You only see the height where you stand and one step ahead.

Go to the middle of the path and look one step to the right. If the path goes up there, a hilltop lies to the right: walk right and you must reach a top, since the path cannot rise for ever and at the end it stops. If it goes down, a top lies here or to the left. Throw away the other half, and repeat. Each look halves the path, so a path of a thousand steps needs about ten looks.

## Definition

**Input.** An array $A[0 \ldots n-1]$, $n \ge 1$, of items from a [total order](/total-order/).

**Output.** An index $i$ that is a *peak*: $A[i] \ge A[i-1]$ when $i > 0$, and $A[i] \ge A[i+1]$ when $i < n - 1$.

Equivalently, put $A[-1] = A[n] = -\infty$; then $i$ is a peak when $A[i - 1] \le A[i] \ge A[i + 1]$. Each index of a global maximum is a peak, so the output always exists. Any peak is a correct answer; the problem does not ask for a particular one.

The cost is the number of comparisons between items, or the number of items read (*probes*).

## Variants

- **Strict peaks.** Ask for $A[i] > A[i \pm 1]$. With equal items such a peak need not exist (all items equal), so the variant assumes distinct items.
- **Valley finding.** A local minimum, by reversing the order.
- **Two dimensions.** In an $m \times n$ grid, find a cell at least as large as its four neighbours. Halving the columns and taking the maximum of the middle column gives $O(m \log n)$. A divide and conquer on windows, which cuts the grid by a middle row and a middle column, gives $O(m + n)$, which is optimal.
- **Graphs.** On any graph with values on the vertices, find a vertex at least as large as its neighbours. This is the [local search problem](/local-search-problem/); on general graphs it can need many probes.
- **Unimodal arrays.** When the array goes up and then down, the only peak is the global maximum; see [maximum of a unimodal function](/unimodal-maximum/).

## Examples

For $A = [2, 5, 7, 4, 3, 6, 9, 8, 1]$, the peaks are the indices 2 (value 7) and 6 (value 9). Index 6 is also the global maximum.

The binary search on the slope, with $lo = 0$ and $hi = 8$:

| step | $lo$ | $hi$ | $mid$ | $A[mid]$, $A[mid + 1]$ | move |
|---|---|---|---|---|---|
| 1 | 0 | 8 | 4 | 3, 6 | up to the right: $lo = 5$ |
| 2 | 5 | 8 | 6 | 9, 8 | down: $hi = 6$ |
| 3 | 5 | 6 | 5 | 6, 9 | up to the right: $lo = 6$ |
| end | 6 | 6 | | | return 6 |

Three comparisons, against 8 for the [maximum](/find-maximum/). The search never sees the peak at index 2, which is also correct.

On an increasing array the only peak is the last index, and on a decreasing array it is the first. For these inputs the search takes exactly $\lceil \lg n \rceil$ steps: 4 for $n = 10$, 10 for $n = 1000$, 20 for $n = 10^6$.

## Known algorithms

```pseudo id=slope
PEAK(A)                                 ▷ n ≥ 1
L1  lo ← 0, hi ← n − 1                 ▷ a peak of A lies in [lo, hi]
L2  while lo < hi do
L3      mid ← lo + ⌊(hi − lo) / 2⌋      ▷ lo ≤ mid < hi, so mid + 1 ≤ hi
L4      if A[mid] < A[mid + 1] then lo ← mid + 1
L5      else hi ← mid
L6  return lo
```

The loop keeps this invariant: $lo = 0$ or $A[lo - 1] < A[lo]$, and $hi = n - 1$ or $A[hi] \ge A[hi + 1]$. It holds at the start. If $A[mid] < A[mid + 1]$, the new $lo = mid + 1$ has a smaller left neighbour; otherwise the new $hi = mid$ has a right neighbour that is not larger. Let $i$ be an index of a maximum of $A[lo \ldots hi]$. If $i > lo$, its left neighbour is in the range and not larger; if $i = lo$, the invariant gives $A[lo - 1] < A[lo]$ or $lo = 0$. The right side is the same. So $i$ is a peak of the whole array, and a peak lies in $[lo, hi]$. When $lo = hi$, that index is the peak.

- **Cost.** A range of $s$ items becomes $\lceil s/2 \rceil$ or $\lfloor s/2 \rfloor$ items, so there are at most $\lceil \lg n \rceil$ steps, each with one comparison and two reads.
- **Reusing reads.** A search that keeps three positions $a < c < b$ with $A[c]$ at least the items at $a$ and $b$, and probes one new point in the larger part, is [golden section search](/golden-section-search/) on an array. It uses one new read per step and about $\log_\varphi n \approx 1.44 \lg n$ reads in all, against $2\lceil \lg n \rceil$ for the slope search.
- **Scan.** Walk from the left until the next item is smaller: up to $n - 1$ comparisons. The [maximum](/find-maximum/) is also a peak, with $n - 1$ comparisons.

## Bounds

**Upper bound.** $\lceil \lg n \rceil$ comparisons and $2\lceil \lg n \rceil$ reads, by the slope search.

**Lower bound.** Each deterministic algorithm reads at least $\lfloor \lg n \rfloor$ items on some input.

*Proof.* An [adversary](/adversary-argument/) keeps an interval $[a, b]$ of positions that have not been read, starting with $[0, n - 1]$, and answers the $t$-th read with the value $t$. When the algorithm reads a position $p$ in $[a, b]$, the adversary replaces the interval by the longer of $[a, p - 1]$ and $[p + 1, b]$. A read outside the interval changes nothing. A range of $s$ positions keeps at least $\lfloor s/2 \rfloor$, so after $k$ reads the interval has at least $\lfloor n / 2^k \rfloor$ positions.

Each read position is outside the final interval, and a position read later is closer to the interval, because each read was inside the interval of its time and the intervals are nested. So on each side of the interval the values read so far grow toward it. The adversary can fill the other outside positions so that the values grow strictly toward the interval on both sides, and fill the interval with values larger than all of these that rise to a single peak and then fall, with the peak at any position of the interval that it likes. The whole array is then strictly unimodal. Then no position outside the interval is a peak, since its neighbour toward the interval is larger. If the algorithm stops while the interval has two or more positions, the adversary puts the peak at a position different from the output, and the output is wrong. So the algorithm must go on until $\lfloor n / 2^k \rfloor \le 1$, that is, $n < 2^{k+1}$, which needs $k \ge \lfloor \lg n \rfloor$. $\blacksquare$

So the number of reads is between $\lfloor \lg n \rfloor$ and about $1.44 \lg n$, and the number of comparisons of the slope search, $\lceil \lg n \rceil$, is $\Theta(\log n)$.

## Reductions

- **[Finding the maximum](/find-maximum/) solves it,** with $n - 1$ comparisons, since a global maximum is a peak. The converse fails: a peak need not be the maximum.
- **The maximum of a [unimodal](/unimodal-maximum/) array reduces to it.** In an array that rises and then falls, every peak is a global maximum.
- **It is a boundary search.** The test $P(i) = (A[i] \ge A[i + 1])$, with $P(n - 1)$ true, is not monotone in general, but the slope search keeps an interval that holds a point where $P$ changes from false to true, as in [lower and upper bound search](/lower-and-upper-bound-search/). The first index $i$ with $P(i)$ true after a false $P(i - 1)$, or $i = 0$, is a peak.

## Applications

- Find a local optimum of a function sampled on a grid, as a first step of [hill climbing](/hill-climbing/) or of a refinement in a finer grid.
- Find the turning point of a [bitonic sequence](/bitonic-sequence/), which goes up and then down, for example the largest value of a signal that rises and falls once.
- Find a local maximum of a 2D image or a 2D table, such as a bright spot or a locally best parameter pair, with the grid variant.
- Teach the design of algorithms: the problem shows that asking for any local answer instead of the global one can change the cost from linear to logarithmic.

## References
