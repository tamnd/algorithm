---
tag: MCFA67
kind: definition
slug: distribution-sort
name: Distribution sort
aliases:
- Distribution-based sorting
area: sorting/distribution-sorts
level: intro
summary: A sort that uses key values to place items directly, escaping the Ω(n log n) comparison lower bound.
prereqs: [sorting-problem, comparison-model]
see_also: [counting-sort, bucket-sort, radix-sort, msd-radix-sort, comparison-sort, comparison-sort-lower-bound, integer-sorting, sample-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2 (the classes of internal sorting methods, and Algorithm D, distribution counting) and Section 5.2.5, Sorting by Distribution
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Sorting in Linear Time (Section 8.1 for the comparison lower bound, Sections 8.2 to 8.4 for counting sort, radix sort and bucket sort)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting, the section on distribution sort (sorting by bucketing)
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988, pages 1116 to 1127
    locator: the distribution sort for external memory, with buckets bounded by sampled splitters
---

A distribution sort is a sort that moves each item to a bucket chosen from the value of its key, and then sorts the buckets one by one, instead of finding the position of an item only by comparing it with other items. When the bucket index is computed by arithmetic on the key, such as a digit or a scaled value, the sort is outside the [comparison model](/comparison-model/), and the $\Omega(n \log n)$ [lower bound for comparison sorts](/comparison-sort-lower-bound/) does not apply to it. [Counting sort](/counting-sort/), [radix sort](/radix-sort/) and [bucket sort](/bucket-sort/) are the standard examples. Knuth uses the term "sorting by distribution" as one of the main classes of internal sorting, next to insertion, exchange, selection and merging.

## Definition

Let $U$ be a set of keys with a total order $\le$, and let the input be items $a_1, \ldots, a_n$ with keys $\mathrm{key}(a_i) \in U$.

**Distribution step.** A *distribution step with $m$ buckets* is given by a function $\beta : U \to \{0, 1, \ldots, m-1\}$, the *bucket map*. The step moves each item $a$ to bucket $\beta(\mathrm{key}(a))$. It is *stable* if each bucket holds its items in their order before the step.

**Order-preserving map.** The map $\beta$ is *order-preserving* (or monotone) if $x \le y$ implies $\beta(x) \le \beta(y)$ for all $x, y \in U$.

**Distribution sort, top-down form.** A sort that applies a distribution step with an order-preserving map $\beta$, sorts each bucket by any correct method (often by the same method, with a new map), and outputs the buckets in the order $0, 1, \ldots, m-1$. Bucket sort ($\beta(x) = \lfloor n x \rfloor$ on $[0, 1)$), counting sort and pigeonhole sort ($\beta(x) = x$ on $\{0, \ldots, k-1\}$, where no bucket needs a sort), and [MSD radix sort](/msd-radix-sort/) ($\beta$ is the leading digit) have this form.

**Distribution sort, bottom-up form.** A sort that applies stable distribution steps with maps $\beta_0, \beta_1, \ldots, \beta_{d-1}$, in this order, and after each step reads the buckets in order to form the next sequence. It sorts if the order of keys is the [lexicographic order](/lexicographic-order/) of the tuples $(\beta_{d-1}(x), \ldots, \beta_0(x))$. [LSD radix sort](/radix-sort/) has this form, with $\beta_t(x)$ the digit $t$ of $x$. Here no single $\beta_t$ needs to be order-preserving.

**Why the top-down form sorts.** If $\beta$ is order-preserving and $\beta(x) < \beta(y)$, then $x < y$: otherwise $y \le x$, and then $\beta(y) \le \beta(x)$. So each item of a lower bucket is less than each item of a higher bucket, and the output is sorted as soon as each bucket is sorted.

**Narrow and wide use.** In the narrow sense, used here and by CLRS for the sorts of Chapter 8, $\beta$ is computed from the key by arithmetic or by indexing, in $O(1)$ time per item, without comparisons between keys. In a wider sense, used in [external memory](/external-memory-model/) sorting since Aggarwal and Vitter, a distribution sort also includes a method that picks $m - 1$ splitter keys from a sample and finds $\beta(x)$ by comparisons with the splitters, as in [sample sort](/sample-sort/). That method is still a comparison sort, so the lower bound applies to it.

## Examples and non-examples

**A top-down step.** Take the keys $[23, 7, 15, 31, 2]$ in $\{0, \ldots, 31\}$ and $m = 4$ buckets with $\beta(x) = \lfloor x / 8 \rfloor$, which is order-preserving. The buckets are $0: [7, 2]$, $1: [15]$, $2: [23]$ and $3: [31]$. After a sort of bucket 0, the concatenation is $[2, 7, 15, 23, 31]$.

**A map that does not preserve the order.** With $\beta(x) = x \bmod 4$, the keys $[5, 2]$ go to buckets $1: [5]$ and $2: [2]$, and the concatenation $[5, 2]$ is not sorted, although each bucket is. One step with such a map does not sort; it works only as one pass of the bottom-up form.

**The bottom-up form.** For two-digit decimal keys $[31, 12, 21, 13]$, the stable pass on the ones digit gives $[31, 21, 12, 13]$, and the stable pass on the tens digit gives $[12, 13, 21, 31]$, which is sorted. If the second pass were not stable, it could output $[13, 12, 21, 31]$.

**Distribution sorts.** [Counting sort](/counting-sort/), [pigeonhole sort](/pigeonhole-sort/), [bucket sort](/bucket-sort/), [LSD radix sort](/radix-sort/), [MSD radix sort](/msd-radix-sort/), [American flag sort](/american-flag-sort/), [radix exchange sort](/radix-exchange-sort/), [flashsort](/flashsort/), [proxmap sort](/proxmap-sort/), [spreadsort](/spreadsort/) and [burstsort](/burstsort/).

**Not distribution sorts.** [Merge sort](/merge-sort/), [heapsort](/heapsort/) and [insertion sort](/insertion-sort/) find positions only by comparisons of keys, and they never compute a bucket index from a key. [Quicksort](/quicksort/) splits the input into two parts, but the part of an item comes from a comparison with a pivot, so it is a comparison sort; it is a distribution sort only in the wide sense.

**The cost of the narrow form.** A distribution step costs $\Theta(n + m)$ time: one look at each item, and one look at each bucket. With $m = \Theta(n)$ and buckets of expected size $O(1)$, as in bucket sort on uniform keys, the whole sort takes $\Theta(n)$ expected time. With integer keys in $\{0, \ldots, n^c - 1\}$, $c$ passes of radix sort with $m = n$ take $\Theta(c n)$ time. Neither bound is possible for a comparison sort, which needs $\lg(n!) = n \lg n - \Theta(n)$ comparisons in the worst case.

## Related definitions

- **[Comparison sort](/comparison-sort/).** A sort that learns about keys only by comparing pairs. Distribution sorts in the narrow sense are the main sorts outside this class.
- **[Stable sort](/stable-sort/).** The bottom-up form needs stable steps. The top-down form is stable if each step is stable and each bucket sort is stable.
- **[Integer sorting](/integer-sorting/).** The problem where the keys are integers in a bounded range, the main setting of distribution sorts.
- **[Uniform input model](/uniform-input-model/).** The input assumption under which bucket sort runs in expected linear time.
- **[Word RAM](/word-ram/).** The usual machine model for distribution sorts, where a key fits in a word and can be used as an index.

## References
