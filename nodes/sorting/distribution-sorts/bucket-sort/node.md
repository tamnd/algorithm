---
tag: HHT9WC
kind: algorithm
slug: bucket-sort
name: Bucket sort
aliases:
- Bin sort
area: sorting/distribution-sorts
level: intro
summary: Scatters keys into buckets by value range, sorts each bucket, and concatenates; linear expected time on uniform input.
solves: [sorting-problem]
model: real-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n^2), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
prereqs: [insertion-sort, uniform-input-model]
see_also: [bucket-sort-expected-linear, counting-sort, radix-sort, flashsort, proxmap-sort, spreadsort, distribution-sort, balls-into-bins]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.4, Bucket sort (the procedure, Figure 8.4 and the analysis of the expected running time)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Sorting by Insertion, the subsection on multiple list insertion
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting, the section on bucket sort (distribution sort)
---

Bucket sort sorts real keys in a known interval, usually $[0, 1)$, by cutting the interval into $n$ equal parts: it puts each key into the bucket of its part, sorts each bucket with [insertion sort](/insertion-sort/), and joins the buckets in order. When the keys are independent and uniform over the interval (the [uniform input model](/uniform-input-model/)), each bucket holds about one key, and the expected time is $\Theta(n)$. In the worst case all keys fall into one bucket, and the time is $\Theta(n^2)$. It is the simplest example of a [distribution sort](/distribution-sort/) whose speed depends on the distribution of the input.

## In plain words

You must sort a thousand test scores, each a number between 0 and 1. You set up a thousand boxes. The first box is for scores from 0 up to 0.001, the next for 0.001 up to 0.002, and so on. You drop each score into its box: that needs one multiplication, not a search. Then you sort the few scores in each box by hand and read the boxes from the first to the last.

If the scores are spread evenly, most boxes get zero, one or two scores, so the sorting by hand is almost free, and the whole job takes time in proportion to the number of scores. If the scores are bunched, for example if all are close to 0.5, one box gets all of them and the hand sort does all the work.

## The problem

The input is an array $A[0 \ldots n-1]$ of real keys with $0 \le A[i] < 1$. The output is the keys in non-decreasing order: the [sorting problem](/sorting-problem/) for keys in a known interval. Keys in another interval $[lo, hi)$ map to $[0, 1)$ by $x \mapsto (x - lo)/(hi - lo)$.

## The algorithm

```pseudo id=main
BUCKET-SORT(A, n)                          ▷ each key is in [0, 1)
L1  B[0 .. n − 1] ← n empty lists
L2  for i ← 0 to n − 1 do
L3      append A[i] to the list B[⌊n · A[i]⌋]
L4  for j ← 0 to n − 1 do
L5      INSERTION-SORT(B[j])
L6  return the concatenation of B[0], B[1], ..., B[n − 1]
```

Bucket $j$ holds the keys in $[j/n, (j+1)/n)$. Line L3 finds the bucket of a key with one multiplication and one floor, in $O(1)$ time. Each bucket is sorted on its own in line L5, and line L6 joins them in order of $j$. Because the bucket index $\lfloor n x \rfloor$ does not decrease when $x$ grows, each key of bucket $j$ is less than each key of bucket $j + 1$.

The correctness proof uses only one fact about the bucket index $\beta(x) = \lfloor n x \rfloor$: it is a non-decreasing function of the key with values in $\{0, \ldots, n-1\}$. So the same procedure sorts any keys with such a map, for example integers with $\beta(x) = \lfloor n (x - \min) / (\max - \min + 1) \rfloor$, or strings with a code of their first few characters. The implementations below use these maps for keys that are not in $[0, 1)$. The expected linear time needs more: the indices must be close to uniform.

## Example

Sort $A = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]$ with $n = 10$ buckets.

| bucket $j$ | keys after lines L2 to L3 | after line L5 |
|---|---|---|
| 0 | | |
| 1 | 0.17, 0.12 | 0.12, 0.17 |
| 2 | 0.26, 0.21, 0.23 | 0.21, 0.23, 0.26 |
| 3 | 0.39 | 0.39 |
| 4, 5 | | |
| 6 | 0.68 | 0.68 |
| 7 | 0.78, 0.72 | 0.72, 0.78 |
| 8 | | |
| 9 | 0.94 | 0.94 |

The result is $[0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]$. The bucket sizes are $0, 2, 3, 1, 0, 0, 1, 2, 0, 1$, so $\sum_j n_j^2 = 4 + 9 + 1 + 1 + 4 + 1 = 20$. The insertion sorts do 1, 2 and 1 shifts in buckets 1, 2 and 7.

## Correctness

Let $x < y$ be keys in different buckets $j = \lfloor n x \rfloor$ and $j' = \lfloor n y \rfloor$. Then $j < j'$, because $\lfloor n \cdot \rfloor$ is non-decreasing. So in the concatenation, each key comes before each larger key of another bucket. Keys in the same bucket are put in order by line L5. So the result is sorted. It holds each key once, because line L3 puts each key in exactly one list. With a stable insertion sort, equal keys stay in input order: they go to the same bucket, in input order, by line L3. The full proof is below.

## Complexity

Let $n_j$ be the number of keys in bucket $j$. Lines L1 to L3 and L6 take $\Theta(n)$ time. Insertion sort on $n_j$ keys takes $O(n_j^2)$ time. So the time is

$$T(n) = \Theta(n) + \sum_{j=0}^{n-1} O(n_j^2).$$

- **Worst case.** If all keys fall into one bucket, $\sum_j n_j^2 = n^2$. With keys in decreasing order inside that bucket, insertion sort does $n(n-1)/2$ shifts, so the worst case is $\Theta(n^2)$.
- **Best case.** If each bucket gets one key, the time is $\Theta(n)$.
- **Expected case in the uniform model.** If the keys are independent and uniform on $[0, 1)$, each $n_j$ is a [binomial](/binomial-distribution/) variable with parameters $n$ and $1/n$, and $\mathbb{E}[n_j^2] = 2 - 1/n$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[T(n)] = \Theta(n) + n \cdot O(2 - 1/n) = \Theta(n)$. The proof is on the page [bucket sort expected linear time](/bucket-sort-expected-linear/). CLRS also remarks that bucket sort runs in linear time on any input for which the sum of the squares of the bucket sizes is linear in $n$, uniform or not.
- **Space.** The $n$ lists and their $n$ entries take $\Theta(n)$ extra space.

The model is the [real RAM](/real-ram/) with a floor operation, or a word RAM with floating-point keys. The floor is what lets bucket sort escape the comparison lower bound: a comparison sort cannot compute a bucket index.

## Properties

- **Stable**, if line L3 appends in input order and line L5 uses a stable sort.
- **Not in place.** The lists take $\Theta(n)$ extra space.
- **Depends on the distribution.** The bound $\Theta(n)$ is an expectation over random inputs, not over random choices of the algorithm. A bad input stays bad each time.
- **Not adaptive.** A sorted input costs the same as a random one with the same bucket sizes.

## Variants and improvements

- **A better sort in each bucket.** Use [merge sort](/merge-sort/) or another $O(m \log m)$ sort in line L5. Then the worst case is $O(n \log n)$, and the expected time stays $\Theta(n)$.
- **A known distribution function.** If the keys have a known continuous distribution function $F$, use the bucket $\lfloor n F(x) \rfloor$. Then the bucket indices are uniform, and the analysis holds for that distribution.
- **Fewer buckets.** With $m$ buckets the expected time is $\Theta(n + m + n^2/m)$, so any $m = \Theta(n)$ gives linear time. [Flashsort](/flashsort/) uses about $0.1 n$ classes and works in place.
- **Buckets from a sample.** If the distribution is unknown, take the bucket bounds from a sorted sample, as in [sample sort](/sample-sort/).
- **Recursive bucket sort.** Sort a large bucket with bucket sort again, on its own sub-interval. [Spreadsort](/spreadsort/) and [proxmap sort](/proxmap-sort/) are engineered forms of these ideas.
- **Integer keys.** For integer keys in $\{0, \ldots, k-1\}$, buckets of width 1 give [pigeonhole sort](/pigeonhole-sort/), which needs no sort inside a bucket.

## When to use it

Use bucket sort when the keys are spread close to uniformly over a known range, for example random numbers, hash values, or measurements with a known distribution. Then it beats a comparison sort, and it is simple. Do not use it for data with clusters or with an unknown range, because a few full buckets make it quadratic. In that case use a comparison sort, or a bucket sort that sorts large buckets with an $O(m \log m)$ method.

## Pitfalls

- **An index of $n$.** If the keys come from an interval $[lo, hi)$, the floating-point value of $(x - lo)/(hi - lo) \cdot n$ can round up to $n$ for $x$ just below $hi$, and line L3 then writes past the last bucket. For example $lo \approx -4.2861$, $hi \approx 1.3087$, $n = 919$ and $x$ the largest double below $hi$ give the index 919. Clamp the index to $n - 1$.
- **A key equal to the upper end.** A key $x = 1$ gives the index $n$. The interval must be half-open, or the index must be clamped.
- **Clustered keys.** Uniform keys are an assumption, not a fact. Integer-like keys, keys with a few common values, or keys that cover a small part of the range all overload a few buckets. Then the time is quadratic with insertion sort in line L5.
- **An unstable bucket sort.** Line L5 with an unstable sort makes the whole sort unstable.

## Implementations

## History

Bucket sort is the method of address calculation and multiple list insertion that Knuth describes in Section 5.2.1, where the keys are spread into many short lists by their value and each list is kept sorted. CLRS presents the form with $n$ buckets and insertion sort, and proves the expected linear time in the uniform model.

## References
