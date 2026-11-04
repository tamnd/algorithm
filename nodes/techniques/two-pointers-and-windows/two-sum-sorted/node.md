---
tag: FY3CT4
kind: problem
slug: two-sum-sorted
name: Two sum on a sorted array
aliases:
- pair with given sum in sorted array
area: techniques/two-pointers-and-windows
level: intro
summary: Given a sorted array and a target, find two entries that sum to the target.
prereqs: [two-pointers, binary-search]
see_also: [two-pointer-pair-search, three-sum-two-pointer-scan, 3sum, k-sum, hash-table, adversary-argument, container-with-most-water]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2, exercises of Section 2.3 (two items of a set that sum to x, in Θ(n lg n) time)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting)
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3), 1995
    locator: pp. 165 to 185 (3SUM and its reduction to repeated pair search)
---

The two sum problem on a sorted array asks for two entries at different positions of a sorted array whose sum is a given target. The [two-pointer pair search](/two-pointer-pair-search/) solves it in $\Theta(n)$ time and $O(1)$ extra space, and an [adversary argument](/adversary-argument/) shows that each algorithm must read all $n$ entries in the worst case. It is the base case of [3SUM](/3sum/) and [k-sum](/k-sum/), and the standard first example of the [two-pointer technique](/two-pointers/).

## In plain words

You have a list of numbers in order from small to large, and a target number. Find two numbers in the list, at two different places, that add up to the target, or say that there are none.

Because the list is in order, you do not need to try every pair. Look at the smallest and the largest number together. If they add up to too little, the smallest number is useless: no partner is large enough for it. If they add up to too much, the largest number is useless. Either way you drop one number and look again. You never need to look back.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of numbers with $A[0] \le A[1] \le \cdots \le A[n-1]$, and a target $t$. The numbers are integers or reals, and the algorithm may add two of them and compare the result with $t$.

**Output (search version).** A pair of indices $(i, j)$ with $0 \le i < j \le n - 1$ and $A[i] + A[j] = t$, or NIL if no such pair exists. Two positions with equal values are allowed: $A = [5, 5]$ with $t = 10$ has the answer $(0, 1)$. One position used twice is not allowed.

**Output (decision version).** YES if such a pair exists, NO otherwise.

## Variants

- **Counting.** Return the number of index pairs $i < j$ with $A[i] + A[j] = t$. With repeated values this can be $\Theta(n^2)$, for example when all items are equal to $t/2$.
- **Listing.** Return all such pairs, or all distinct value pairs $\{A[i], A[j]\}$.
- **Unsorted input.** The array is in any order and the output must give the original indices. This is the common interview form.
- **Closest sum.** Minimize $|A[i] + A[j] - t|$.
- **Inequality.** Count the pairs with $A[i] + A[j] < t$, or $\le t$.
- **Difference.** Find $i \ne j$ with $A[j] - A[i] = t$.
- **Two arrays.** Find $a \in A$ and $b \in B$ with $a + b = t$, for two sorted arrays. Reverse $B$, or run one pointer up $A$ and one down $B$.

## Examples

**One answer.** $A = [1, 3, 4, 6, 8, 11, 14, 17]$ and $t = 22$. The only answer is $(4, 6)$, with $8 + 14 = 22$. The pair search finds it in 6 steps; its trace is on the [algorithm page](/two-pointer-pair-search/).

**No answer.** The same array with $t = 24$. No two items sum to 24, and the pair search returns NIL after $n - 1 = 7$ steps.

**Many answers.** $A = [1, 2, 2, 3, 3, 3, 4]$ and $t = 5$. The answers are $(0, 6)$ for $1 + 4$, and the $2 \cdot 3 = 6$ pairs of one 2 and one 3. So the count is 7, and there are two distinct value pairs, $\{1, 4\}$ and $\{2, 3\}$.

**Negative numbers.** $A = [-5, -1, 0, 2, 7]$ and $t = -6$. The answer is $(0, 1)$. The sorted order is all that matters, not the sign.

## Known algorithms

| algorithm | time | extra space | notes |
| --- | --- | --- | --- |
| all pairs | $\Theta(n^2)$ | $O(1)$ | needs no order |
| [binary search](/binary-search/) for $t - A[i]$, for each $i$ | $O(n \log n)$ | $O(1)$ | search in $A[i+1 \ldots n-1]$ |
| [two-pointer pair search](/two-pointer-pair-search/) | $\Theta(n)$ worst case | $O(1)$ | optimal; the full proof is on its page |
| [hash table](/hash-table/) of the items seen so far | $O(n)$ expected | $\Theta(n)$ | needs no order |

**Why the two-pointer search skips no answer.** It keeps a range $[lo, hi]$ with this invariant: if an answer exists, one answer $(i, j)$ has $lo \le i < j \le hi$. If $A[lo] + A[hi] < t$, then for each $j \le hi$ the sum $A[lo] + A[j]$ is at most $A[lo] + A[hi] < t$, so no answer in the range uses $lo$, and $lo$ can go. If $A[lo] + A[hi] > t$, the mirror argument removes $hi$. Each step shrinks the range by one, so the search ends after at most $n - 1$ steps.

## Bounds

**Upper bound.** $\Theta(n)$ time and $O(1)$ extra space in the worst case, by the two-pointer pair search, in a model where an addition and a comparison cost $O(1)$ (the [word RAM](/word-ram/) for integers, or the [real RAM](/real-ram/)).

**Lower bound: every item must be read.** Let an algorithm learn the items only by reading them, one at a time. For $n \ge 2$, each correct algorithm for the decision version reads all $n$ items on some input. Proof by an [adversary argument](/adversary-argument/). Take $A[i] = 4i$ for $0 \le i \le n-1$ and $t = 4n - 2$. Each sum $A[i] + A[j]$ is a multiple of 4 and $t$ is not, so the answer is NO. Suppose the algorithm stops without reading $A[k]$. Change only $A[k]$:

- If $2k \ne n - 1$, set $A[k] = 4k + 2$. The array stays sorted, because $4k < 4k + 2 < 4k + 4$, and $A[k] + A[n-1-k] = 4k + 2 + 4(n - 1 - k) = 4n - 2 = t$, with $n - 1 - k \ne k$.
- If $2k = n - 1$, then $n = 2k + 1 \ge 3$, so $k \ge 1$. Set $A[k] = 4k - 2$. The array stays sorted, because $4k - 4 < 4k - 2 < 4k + 4$, and $A[k] + A[k+1] = 8k + 2 = 4n - 2 = t$.

The new input has the answer YES, but every item that the algorithm reads is the same as before, so it gives the same answer, NO. This contradicts correctness. So the algorithm reads $A[k]$ for each $k$, which is at least $n$ reads, and the two-pointer search is optimal up to a constant factor. Its $n - 1$ steps read $n$ distinct items when no answer exists.

**Unsorted input.** Sorting and then the two-pointer search take $O(n \log n)$ time in the [comparison model](/comparison-model/) with additions. A hash table gives $O(n)$ expected time with a random hash function, but no worst-case linear bound.

## Reductions

- **3SUM to sorted two sum.** To decide if three items of a set sum to 0, sort once, and for each $i$ solve two sum on $A[i+1 \ldots n-1]$ with target $-A[i]$. This is $n$ instances of $\Theta(n)$ each, so $O(n^2)$ time in total. Gajentaan and Overmars took this quadratic bound as the reference point for their class of 3SUM-hard problems. See [3SUM by two-pointer scan](/three-sum-two-pointer-scan/) and [3SUM-hardness](/3sum-hardness/).
- **k-sum.** Fixing $k - 2$ items and running the pair search gives [k-sum](/k-sum/) in $O(n^{k-1})$ time.
- **Two sorted arrays.** Two sum over $A$ and $B$ reduces to the one-array form on the merged array, with a tag on each item. The direct scan with one pointer up $A$ and one down $B$ is simpler and takes $O(|A| + |B|)$ time.

## Applications

- **Inner loop of 3SUM and k-sum.** The quadratic 3SUM algorithm runs this search $n$ times.
- **Pair budgets.** Choose two items whose prices add up to a budget, or two tasks whose durations fill a time slot.
- **Teaching the two-pointer technique.** It is the simplest case where an argument about the sorted order lets a scan drop one candidate in each step.

## References
