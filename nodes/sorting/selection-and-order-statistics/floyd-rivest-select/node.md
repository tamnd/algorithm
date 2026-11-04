---
tag: 4QBG0P
kind: algorithm
slug: floyd-rivest-select
name: Floyd-Rivest selection
aliases:
- SELECT (Floyd-Rivest)
area: sorting/selection-and-order-statistics
level: advanced
summary: Selection that samples the input to choose two pivots bracketing the target rank, using close to n comparisons on average.
solves: [selection-problem, median-finding]
model: comparison-model
complexity:
  vars: {n: the number of items, k: the rank sought}
  time: {worst: O(n^2), expected: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: false, comparison: true, recursive: true}
history:
  year: 1975
  people: [Robert W. Floyd, Ronald L. Rivest]
  note: Floyd and Rivest published the analysis, with n + min(k, n - k) + o(n) expected comparisons, and the in-place program SELECT, as Algorithm 489, in the same 1975 issue of the Communications of the ACM.
prereqs: [quickselect, selection-problem, random-sampling]
see_also: [quickselect, quickselect-expected-linear, median-of-medians, introselect, selection-lower-bound, multiple-selection, partition-around-pivot, las-vegas-algorithm]
sources:
  - paper: doi:10.1145/360680.360691
    title: Robert W. Floyd and Ronald L. Rivest, Expected time bounds for selection, Communications of the ACM 18(3) (1975)
    locator: pages 165 to 172 (the sampling method, the bound n + min(k, n - k) + O(n^(2/3) log^(1/3) n), and lower bounds)
  - paper: doi:10.1145/360680.360694
    title: "Robert W. Floyd and Ronald L. Rivest, Algorithm 489: The algorithm SELECT, for finding the ith smallest of n elements, Communications of the ACM 18(3) (1975)"
    locator: page 173 (the in-place program with the cutoff 600)
  - paper: doi:10.1145/62044.62047
    title: Walter Cunto and J. Ian Munro, Average case selection, Journal of the ACM 36(2) (1989)
    locator: pages 270 to 279 (the matching lower bound n + min(k, n - k) - O(1) on average)
  - paper: doi:10.1016/j.tcs.2005.06.032
    title: Krzysztof C. Kiwiel, On Floyd and Rivest's SELECT algorithm, Theoretical Computer Science 347(1-2) (2005)
    locator: pages 214 to 238 (a full analysis of the sample sizes and of the version with two pivots)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the average number of comparisons for selection)
---

Floyd-Rivest selection finds the item of rank $k$ among $n$ items by first looking at a small random sample. From the sample it picks two pivots $u \le v$ whose ranks in the sample bracket the place where rank $k$ should fall, so that with high probability the answer lies between them and only a small middle part of the input remains. The method makes $n + \min(k, n - k) + o(n)$ comparisons on average, so about $1.5n$ for the median, against about $3.39n$ for [quickselect](/quickselect/) with a random pivot, and this is optimal on average up to the lower-order term. Like quickselect, it can take quadratic time in the worst case, but with a vanishing probability.

## In plain words

Suppose you want the median height of a city's million people. Measure a random thousand first. Their median is almost surely close to the true median, so pick two heights from the sample, a little below and a little above its middle, as fences. The true median almost surely lies between the fences.

Now go through the whole city once and put each person below, between or above the fences. Only the few people between the fences are still in the running, and you count how many fell below. The median of the city is then a person of a known rank among the few in the middle, and that is a much smaller problem. Most people needed one or two comparisons with the fences, and nothing else.

## The problem

Given $n \ge 1$ items with a [total order](/total-order/) and a rank $k$ with $1 \le k \le n$, return the item of rank $k$, the $k$-th entry of the sorted order: the [selection problem](/selection-problem/). The goal is a small expected number of comparisons for every input; the randomness is in the algorithm.

## The algorithm

The algorithm below is the version with two pivots that Floyd and Rivest analyze. It works on lists, and $c \ge 2$ is a cutoff below which a list is just sorted. The sample size $m$ and the gap $g$ are one standard choice; the analysis below shows why they work.

```pseudo id=main
FR-SELECT(S, k)                            ▷ n = |S|, 1 ≤ k ≤ n
L1  if n ≤ c then return the k-th smallest of S, by sorting
L2  m ← min(n − 1, ⌈n^(2/3)⌉); R ← m items of S, drawn at random without replacement
L3  g ← √(m ln n) / 2
L4  lo ← max(1, ⌊k m / n − g⌋); hi ← min(m, ⌈k m / n + g⌉)
L5  u ← FR-SELECT(R, lo); v ← FR-SELECT(R, hi)        ▷ so u ≤ v
L6  L, M, G ← empty lists                  ▷ below u, between, above v
L7  if 2k ≤ n then for each x in S: if x > v then add x to G, else if x < u then add x to L, else add x to M
L8  else for each x in S: if x < u then add x to L, else if x > v then add x to G, else add x to M
L9  if k ≤ |L| then return FR-SELECT(L, k)
L10 if k > |L| + |M| then return FR-SELECT(G, k − |L| − |M|)
L11 if |M| = n then return the k-th smallest of S, by sorting
L12 return FR-SELECT(M, k − |L|)
```

The item of rank $k$ of $S$ is expected to have rank about $k m / n$ in the sample, so lines L4 and L5 take the sample items $g$ ranks below and above that point. Lines L7 and L8 split $S$ with the cheaper order of tests: when $k$ is in the lower half, most items are above $v$ and are settled by one comparison, and only the items not above $v$, about $k$ of them, need a second one. Line L12 is the usual case, and lines L9 and L10 handle a miss, when the answer is outside $[u, v]$. Line L11 is a guard that is almost never used: it stops the recursion when the pivots fail to remove any item, for instance when all items are equal.

## Example

Take $n = 10^6$ distinct items and the median, $k = 500000$. Line L2 draws $m = 10^4$ items, and line L3 gives $g = \sqrt{10^4 \ln 10^6}/2 \approx 185.8$. Since $k m / n = 5000$, line L4 gives $lo = 4814$ and $hi = 5186$, and line L5 selects these two ranks in the sample, a cost of a few times $10^4$ comparisons. On average a fraction $372/10^4$ of the items lies between $u$ and $v$, so line L8 leaves about $37200$ items in $M$, and the answer is in $M$ unless the sample was very unrepresentative. The split costs $10^6$ comparisons for the first tests and about $5 \cdot 10^5$ for the second ones, since about half of the items are not below $u$. The call of line L12 on $37200$ items costs about $1.5 \cdot 37200$ more.

For $k = 1000$ instead, $k m / n = 10$, so $lo = 1$ and $hi = 196$: $u$ is the minimum of the sample and $v$ its item of rank $196$. Line L7 settles about $98\%$ of the items with one comparison each.

## Correctness

Each pivot is an item of the sample, and so of $S$. After lines L7 or L8, each item of $L$ is less than $u$, each item of $M$ lies in $[u, v]$, and each item of $G$ is greater than $v$, so a sorted order of $S$ is a sorted order of $L$, then of $M$, then of $G$. Lines L9, L10 and L12 ask for the right rank in the part that holds position $k$ of this order. Each recursive call is on a smaller list: $R$ has $m < n$ items; $L$ does not hold $u$, and $G$ does not hold $v$; and $M$ is used only if it is smaller than $S$. So the recursion stops, and by induction on $n$ the result is right for every outcome of the random draws. The full proof is in the proof file below.

## Complexity

- **Expected comparisons, $n + \min(k, n - k) + O(n^{2/3} \sqrt{\log n})$.** The split makes $n$ first tests, and second tests for about $\min(k, n - k)$ items plus the $O(n g / m)$ items near the pivots. The middle part $M$ has $O(n g / m) = O(n^{2/3} \sqrt{\log n})$ items on average, and so does the work on it. The two calls on the sample cost $O(m) = O(n^{2/3})$. The answer falls outside $[u, v]$ only if the number of sample items below it is off by more than $g$ from its mean $k m / n$, and by a [Hoeffding](/hoeffding-inequality/) bound for sampling without replacement this has probability at most $2 e^{-2g^2/m} = 2 n^{-1/2}$. A miss costs $O(n)$, so it adds $O(\sqrt{n})$ to the mean.
- **Measured.** With the cutoff $c = 600$, the Python version below made on average $1.09n$ comparisons for $k = 1000$ and $1.64n$ for the median (two runs each), on random lists of $10^6$ items. For $10^5$ items the counts were $1.25n$ for $k = 100$ and $1.92n$ for the median: at that size the sorts of lists of up to $600$ items in line L1 are still a large part of the cost.
- **Lower bound.** Cunto and Munro (1989) proved that each algorithm needs $n + \min(k, n - k) - O(1)$ comparisons on average, so the leading terms are optimal. In the worst case, [the selection lower bound](/selection-lower-bound/) is $n - 1 + \min(k - 1, n - k)$, the same shape, but no deterministic method is known to come close to it.
- **Worst case, $O(n^2)$.** Every sample can be unlucky, and then each level removes only a few items. The probability is tiny, and a run can be made safe by switching to [median of medians](/median-of-medians/) after a miss, as in [introselect](/introselect/).
- **Space.** This list version uses $\Theta(n)$ extra space for the parts. Algorithm 489 works in place.

## Properties

- **Randomized, Las Vegas.** The answer is always right; only the running time depends on the draws ([Las Vegas algorithm](/las-vegas-algorithm/)).
- **Not in place** in the form above; the in-place form is below.
- **Not stable.** It returns a value, and the order of equal items is not kept.
- **Comparison based and recursive.** The recursion depth is $O(\log \log n)$ on average, since the list size goes from $n$ to about $n^{2/3}$ at each level of the recursion on the sample and on $M$.

## Variants and improvements

- **Algorithm 489, in place.** The program published with the paper keeps the array in place and uses one pivot. For a range of more than $600$ items, it first calls itself on a subrange around position $k$, of about $n^{2/3}$ items, treated as the sample. That call leaves a good pivot at position $k$, and the range is then split around $A[k]$ with a [Hoare-style partition](/partition-around-pivot/). It does not draw a random sample, so it assumes that the input is in random order, or shuffles it first.
- **Tuned sample sizes.** Floyd and Rivest chose $m$ near $n^{2/3} (\ln n)^{1/3}$ and a gap near $\sqrt{m \ln n}$, which gives the error term $O(n^{2/3} (\log n)^{1/3})$. Kiwiel (2005) studied the choices in detail and showed that the two-pivot version is also fast in practice.
- **LazySelect.** A simpler form with a sample of $n^{3/4}$ items and a gap of $\sqrt{n}$, often taught in courses on randomized algorithms. It makes $1.5n + o(n)$ comparisons for the median with high probability.
- **Many ranks.** The same sampling idea finds several ranks at once, with pairs of pivots for each rank ([multiple selection](/multiple-selection/)).

## When to use it

Use it when comparisons are expensive or $n$ is large and an average close to $n + \min(k, n - k)$ comparisons matters, as in statistics libraries and database engines that find medians and quantiles of large columns. For small $n$, the cost of the sample does not pay off, and plain [quickselect](/quickselect/) with a median of three is simpler. If a worst-case guarantee is needed, combine it with a fallback to a linear-time method.

## Pitfalls

- **A sample as large as the list.** For small $n$, $\lceil n^{2/3} \rceil$ can equal $n$, and the recursion on the sample would never shrink. The cap $m \le n - 1$ and the cutoff $c$ prevent this.
- **The wrong order of tests.** Testing $x < u$ first when $k$ is small costs two comparisons for most items, and the average rises to about $2n$.
- **Equal items.** If many items equal the answer, $u$ and $v$ can be equal and $M$ can be the whole list. Without a guard such as line L11, the recursion can repeat.
- **Assuming random order.** Algorithm 489 takes a contiguous subrange as its sample. On sorted or adversarial input that sample is biased; shuffle first or draw a true random sample.

## Implementations

## History

Robert Floyd and Ronald Rivest published "Expected time bounds for selection" in the Communications of the ACM in March 1975, together with Algorithm 489, the program SELECT. They showed that sampling gives $n + \min(k, n - k) + o(n)$ comparisons on average and proved a lower bound of the same form for a class of methods; Cunto and Munro proved the general average-case lower bound in 1989. This was two years after Floyd and Rivest, with Blum, Pratt and Tarjan, had given the first linear worst-case method. Kiwiel revisited the algorithm in 2005 and gave a full analysis of the version with two pivots.

## References
