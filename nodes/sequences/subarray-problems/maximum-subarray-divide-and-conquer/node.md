---
tag: NXBA0T
kind: algorithm
slug: maximum-subarray-divide-and-conquer
name: Maximum subarray divide and conquer
aliases:
- divide-and-conquer maximum subarray
area: sequences/subarray-problems
level: core
summary: Split at the midpoint, take the best of the left, right and crossing subarrays, giving Theta(n log n) time.
solves: [maximum-subarray-problem]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(log n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: false, recursive: true}
history:
  year: 1977
  people: [Michael Shamos, Jon Bentley]
  note: Shamos designed the n log n divide-and-conquer algorithm in 1977, and Bentley published it in his Programming Pearls column of September 1984.
prereqs: [maximum-subarray-problem, divide-and-conquer-paradigm, master-theorem, induction]
see_also: [kadane-algorithm, segment-tree-maximum-subsegment-sum, recursion-tree-method, prefix-sums, bentley-column-sweep, maximum-circular-subarray-sum, all-prefix-sums, subarray]
sources:
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the divide-and-conquer algorithm and its analysis
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Section 8.3, A Divide-and-Conquer Algorithm
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 4.1, FIND-MAX-CROSSING-SUBARRAY and FIND-MAXIMUM-SUBARRAY, and their analysis
  - paper: doi:10.3390/a16110519
    title: "Joseph B. Kadane, Two Kadane Algorithms for the Maximum Sum Subarray Problem, Algorithms 16(11) (2023), 519"
    locator: the history of the problem before the linear algorithm
  - paper: doi:10.1016/s1571-0661(04)00313-5
    title: "Tadao Takaoka, Efficient Algorithms for the Maximum Subarray Problem by Distance Matrix Multiplication, Electronic Notes in Theoretical Computer Science 61 (2002), 191-200"
    locator: the divide-and-conquer algorithm for two dimensions with distance matrix multiplication for the crossing case
---

The divide-and-conquer algorithm for the [maximum subarray problem](/maximum-subarray-problem/) splits the array at its midpoint and finds three candidates: the best subarray in the left half, the best in the right half, and the best subarray that crosses the midpoint. The first two come from recursive calls. The third is the best suffix of the left half joined to the best prefix of the right half, which two linear scans find. The answer is the largest of the three. The recurrence $T(n) = 2T(n/2) + \Theta(n)$ gives $\Theta(n \log n)$ time. [Kadane's algorithm](/kadane-algorithm/) is faster, but this algorithm is the standard first example of the [divide-and-conquer paradigm](/divide-and-conquer-paradigm/) where the combine step does real work, and its $O(1)$-combine form is the basis of the [segment tree for maximum subsegment sum](/segment-tree-maximum-subsegment-sum/).

## In plain words

Cut the list in the middle. The best stretch is in one of three places. It is all in the left part, or all in the right part, or it crosses the cut.

For the first two places, solve the same problem again on each part. For the third place, start at the cut and walk left, adding numbers, and keep the best total you see. Then start at the cut and walk right in the same way. A stretch that crosses the cut is a left piece that ends at the cut and a right piece that starts there, so the best crossing stretch is the two best walks put together.

Compare the three totals and keep the largest. Each level of cutting reads every number once, and there are about as many levels as times you can halve the list.

## The problem

**Input.** An array $A[1..n]$ of numbers with $n \ge 1$.

**Output.** A value $S^*$ and indices $i \le j$ with $A[i] + \dots + A[j] = S^*$, where $S^*$ is the largest sum of a non-empty [subarray](/subarray/). The call $\text{MAXSUB}(A, 1, n)$ returns it.

## The algorithm

```pseudo id=main
MAXSUB(A, lo, hi)
L1  if lo = hi then return (A[lo], lo, lo)
L2  mid ← ⌊(lo + hi) / 2⌋
L3  (sL, iL, jL) ← MAXSUB(A, lo, mid); (sR, iR, jR) ← MAXSUB(A, mid + 1, hi)
L4  t ← 0; ls ← −∞; for i ← mid downto lo do t ← t + A[i]; if t > ls then ls ← t; ci ← i
L5  t ← 0; rs ← −∞; for j ← mid + 1 to hi do t ← t + A[j]; if t > rs then rs ← t; cj ← j
L6  sC ← ls + rs
L7  if sL ≥ sR and sL ≥ sC then return (sL, iL, jL)
L8  if sR ≥ sC then return (sR, iR, jR)
L9  return (sC, ci, cj)
```

Line L1 is the base case of one item. Line L3 solves the two halves. Line L4 finds the best suffix $A[ci..mid]$ of the left half, and line L5 the best prefix $A[mid+1..cj]$ of the right half. Both are non-empty, so their join $A[ci..cj]$ is the best subarray that contains both $A[mid]$ and $A[mid+1]$. Lines L7 to L9 return the largest of the three candidates.

## Example

$A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]$, with $n = 9$. The table lists every call with more than one item, from the bottom of the recursion up. Each candidate is written as a sum with its range.

| call $(lo, hi)$ | $mid$ | left | right | crossing | returned |
|---|---|---|---|---|---|
| $(1, 2)$ | 1 | $-2$, $[1, 1]$ | $1$, $[2, 2]$ | $-1$, $[1, 2]$ | $1$, $[2, 2]$ |
| $(1, 3)$ | 2 | $1$, $[2, 2]$ | $-3$, $[3, 3]$ | $-2$, $[2, 3]$ | $1$, $[2, 2]$ |
| $(4, 5)$ | 4 | $4$, $[4, 4]$ | $-1$, $[5, 5]$ | $3$, $[4, 5]$ | $4$, $[4, 4]$ |
| $(1, 5)$ | 3 | $1$, $[2, 2]$ | $4$, $[4, 4]$ | $2$, $[2, 4]$ | $4$, $[4, 4]$ |
| $(6, 7)$ | 6 | $2$, $[6, 6]$ | $1$, $[7, 7]$ | $3$, $[6, 7]$ | $3$, $[6, 7]$ |
| $(8, 9)$ | 8 | $-5$, $[8, 8]$ | $4$, $[9, 9]$ | $-1$, $[8, 9]$ | $4$, $[9, 9]$ |
| $(6, 9)$ | 7 | $3$, $[6, 7]$ | $4$, $[9, 9]$ | $2$, $[6, 9]$ | $4$, $[9, 9]$ |
| $(1, 9)$ | 5 | $4$, $[4, 4]$ | $4$, $[9, 9]$ | $6$, $[4, 7]$ | $6$, $[4, 7]$ |

In the top call, line L4 walks left from $A[5]$ with running sums $-1, 3, 0, 1, -1$, so $ls = 3$ at $ci = 4$. Line L5 walks right from $A[6]$ with running sums $2, 3, -2, 2$, so $rs = 3$ at $cj = 7$. The crossing sum $6$ beats both halves, which each have only $4$. The answer is $A[4..7] = [4, -1, 2, 1]$ with sum $6$, the same as Kadane's algorithm gives.

## Correctness

The proof is by [induction](/induction/) on the length $hi - lo + 1$. The claim is that $\text{MAXSUB}(A, lo, hi)$ returns $(s, i, j)$ with $lo \le i \le j \le hi$, $A[i] + \dots + A[j] = s$, and $s$ the largest sum of a subarray of $A[lo..hi]$.

*Base.* For one item, the only subarray is $A[lo..lo]$, which line L1 returns.

*Step.* Every subarray $A[i..j]$ of $A[lo..hi]$ has $j \le mid$, or $i \ge mid + 1$, or $i \le mid < j$. By the induction hypothesis, line L3 gives the best of the first two kinds. For the third kind, $A[i..j]$ is the suffix $A[i..mid]$ of the left half followed by the prefix $A[mid+1..j]$ of the right half, and the two parts can be chosen independently. So the best sum of the third kind is the best suffix sum plus the best prefix sum. Line L4 tries every suffix and line L5 every prefix, so $sC$ is that sum and $A[ci..cj]$ reaches it. The largest of the three bests is the best overall, which lines L7 to L9 return.

The halves are shorter than the whole, since $lo \le mid < hi$, so the recursion stops. The [proof page](proofs/correctness.md) writes out the details.

## Complexity

- **Time.** Lines L4 and L5 together read each of the $hi - lo + 1$ items of the call once, and the rest of the call is $O(1)$. So $T(1) = \Theta(1)$ and $T(n) = T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor) + \Theta(n)$. By the [master theorem](/master-theorem/) (case 2), $T(n) = \Theta(n \log n)$. The [recursion tree](/recursion-tree-method/) shows it directly: the calls on each level of the tree cover disjoint parts of the array, so each level costs at most $n$ additions, and there are $\lceil \lg n \rceil$ levels with more than one item. For $n$ a power of $2$, the scans do exactly $n \lg n$ additions.
- **No fast case.** The scans in lines L4 and L5 always run to the end of their halves, so the time is $\Theta(n \log n)$ on every input.
- **Space.** The recursion depth is $\lceil \lg n \rceil + 1$ and each frame holds $O(1)$ values, so $\Theta(\log n)$ extra space. The array is only read.

## Properties

- **Not online.** The first call needs the whole array, since the split depends on $n$.
- **Parallel.** The two calls in line L3 are independent. With the two scans done as parallel reductions, the span is $O(\log^2 n)$. The $O(1)$-combine form below gives span $O(\log n)$, the same as a parallel computation of [all prefix sums](/all-prefix-sums/).
- **Ties.** Lines L7 and L8 prefer the left half, then the right half, then the crossing subarray, as in CLRS. With strict tests in lines L4 and L5, $ci$ is the suffix start closest to $mid$ and $cj$ the prefix end closest to $mid$ among the best ones.

## Variants and improvements

- **Linear time by returning more.** Let each call return four values for its part: the total, the best prefix sum, the best suffix sum and the best subarray sum. For the join of a left part $X$ and a right part $Y$, the total is $X.tot + Y.tot$, the best prefix is $\max(X.pre, X.tot + Y.pre)$, the best suffix is $\max(Y.suf, Y.tot + X.suf)$, and the best subarray is $\max(X.best, Y.best, X.suf + Y.pre)$. The combine is then $O(1)$, so $T(n) = 2T(n/2) + O(1) = \Theta(n)$.
- **Segment tree.** Storing those four values in every node of a segment tree gives the [segment tree for maximum subsegment sum](/segment-tree-maximum-subsegment-sum/), which answers the best subarray inside any range, under point updates, in $O(\log n)$ time per operation.
- **Crossing case with prefix sums.** With [prefix sums](/prefix-sums/) $P$, the best crossing sum is $\max_{j > mid} P_j - \min_{i \le mid} P_{i-1}$, which is the same scan in another form.
- **Circular arrays.** On a ring, a wrapping subarray is a best suffix joined to a best prefix of the whole array, the same join as the crossing case; see [maximum circular subarray sum](/maximum-circular-subarray-sum/).
- **Two dimensions.** Splitting a matrix into halves leaves a crossing case that is a problem in its own right. Takaoka (2002) solves it with [min-plus matrix multiplication](/min-plus-matrix-multiplication/) and gets slightly subcubic time; see the [maximum sum submatrix](/maximum-sum-submatrix/). The simple cubic method is the [Bentley column sweep](/bentley-column-sweep/).

## When to use it

Use it to teach or to learn divide and conquer, and as the recurrence example for the master theorem. For the plain problem, Kadane's algorithm is simpler and faster. Use the four-value combine when the parts are computed on different processors, or when a range of a changing array is asked about many times, through the segment tree.

## Pitfalls

- **Empty crossing parts.** If line L4 or L5 allows an empty part, with $ls$ or $rs$ starting at $0$, the crossing candidate can be a subarray of one half only, and its indices are wrong. Start both at $-\infty$ so that each part has at least one item.
- **Splitting at the wrong place.** With $mid = \lceil (lo + hi)/2 \rceil$ and the halves $[lo, mid]$ and $[mid + 1, hi]$, a call on two items calls itself again and also calls an empty half. Use the floor, or split as $[lo, mid - 1]$ and $[mid, hi]$.
- **Scanning in the wrong direction.** The left scan must start at $mid$ and go down, so that it covers suffixes of the left half. Starting at $lo$ and going up gives prefixes, which do not touch the midpoint.
- **Expecting the linear time.** The plain algorithm is $\Theta(n \log n)$ on every input. Only the four-value form is linear.

## Implementations

## History

Ulf Grenander posed the problem at Brown University, and he found the quadratic algorithm for one dimension. In 1977 Grenander described the problem to Michael Shamos, who designed the $n \log n$ divide-and-conquer algorithm overnight, according to Bentley. Shamos described the problem at a seminar at Carnegie Mellon University soon after, and Joseph Kadane found the linear scan at once. Bentley gave the four algorithms, cubic, quadratic, $n \log n$ and linear, in his Programming Pearls column of September 1984. CLRS uses the divide-and-conquer algorithm as the first worked example of the method in its chapter on divide and conquer.

## References
