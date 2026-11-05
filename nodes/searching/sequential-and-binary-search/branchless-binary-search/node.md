---
tag: TEM5EQ
kind: technique
slug: branchless-binary-search
name: Branchless binary search
aliases:
- conditional-move binary search
area: searching/sequential-and-binary-search
level: advanced
summary: Implement each halving step with a conditional move instead of a branch, avoiding branch mispredictions.
prereqs: [lower-bound-query, lower-and-upper-bound-search, branchless-programming]
see_also: [uniform-binary-search, eytzinger-layout, binary-search, lower-and-upper-bound-search, prefetching, speculative-execution, timing-attack, branchless-programming]
sources:
  - paper: doi:10.1145/3053370
    title: Paul-Virak Khuong and Pat Morin, Array layouts for comparison-based searching, ACM Journal of Experimental Algorithmics 22 (2017)
    locator: Article 1.3 (branch-free binary search on a sorted array, prefetching, and the Eytzinger and B-tree layouts)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1 (uniform binary search, where the steps do not depend on the data)
---

Branchless binary search is the technique of writing the halving step of a [lower bound search](/lower-and-upper-bound-search/) so that the outcome of the comparison picks a value, not a path through the code. The step becomes `base = (A[base + half] < x) ? base + half : base`, which a compiler can turn into a conditional move, and the length of the range shrinks by the same amount whatever the outcome. The loop then runs exactly $\lceil \lg n \rceil$ times for every key, with no branch that depends on the data. On a modern processor a binary search branch is taken or not taken at random, so about half of the steps are mispredicted, and each misprediction costs many cycles. Removing the branch removes that cost, and it also makes the running time independent of the key, which helps against [timing attacks](/timing-attack/). It is the [branchless programming](/branchless-programming/) idea applied to search.

## In plain words

A processor reads ahead in the program and guesses which way each "if" will go, so that it does not have to wait. In a binary search the "if" goes left or right like a coin toss, so the guess is wrong half of the time. Each wrong guess makes the processor throw away work and start again.

The fix is to never ask the processor to choose a path. Both possible next positions are computed, and the comparison only selects one of the two numbers. The loop always does the same steps in the same order. Only the numbers change.

The search then makes about one comparison more than the best plain search, but each step is fast and steady.

## When it applies

- The search runs on data in memory, many times, so a few cycles per step matter.
- The test is cheap, such as a comparison of numbers, so a mispredicted branch costs more than the test.
- The comparison can be made into a value (0 or 1) and used in arithmetic or in a select instruction.
- The array is small enough, or the search is shaped so, that memory delays do not hide the gain. For large arrays, combine it with [prefetching](/prefetching/) or the [Eytzinger layout](/eytzinger-layout/).
- The running time must not depend on the key, as in code that handles secret data.

## The template

```pseudo id=main
BRANCHLESS-LOWER-BOUND(A, x)          ▷ A[0 .. n − 1] sorted; returns the lower bound of x
L1  if n = 0 then return 0
L2  base ← 0, len ← n                  ▷ invariant: base ≤ ℓ ≤ base + len
L3  while len > 1 do
L4      half ← ⌊len / 2⌋
L5      base ← if A[base + half] < x then base + half else base   ▷ a select, no branch
L6      len ← len − half                 ▷ the same for both outcomes
L7  return base + [A[base] < x]          ▷ [true] = 1, [false] = 0
```

The holes are the test $A[\cdot] < x$, which can be any monotone predicate as in FIRST-TRUE, and the way the select of line L5 is written in the target language. The answer $\ell$ is the lower bound: the number of items less than $x$.

**Why it is correct.** The invariant on line L2 holds at the start, since $0 \le \ell \le n$. In a step, if $A[base + half] < x$, then $\ell \ge base + half + 1$, and the new range $[base + half, base + len]$ still holds $\ell$. If $A[base + half] \ge x$, then $\ell \le base + half$, and since $half \le len - half$, the new range $[base, base + len - half]$ holds $\ell$. Line L5 reads index $base + half \le base + len - 1 \le n - 1$, a real cell. When the loop stops, $len = 1$, so $\ell$ is $base$ or $base + 1$, and $\ell = base + 1$ exactly when $A[base] < x$; line L7 reads $A[base]$ with $base \le n - 1$.

**Cost.** The length goes $n \to \lceil n/2 \rceil \to \cdots \to 1$, so the loop runs exactly $\lceil \lg n \rceil$ times for every key, and with line L7 the search makes $\lceil \lg n \rceil + 1$ comparisons. The optimum is $\lceil \lg(n+1) \rceil$. The two are equal when $n$ is a power of 2, and otherwise the branchless loop makes one comparison more. A script checked the exact count for every $n < 3000$ and the result against `bisect_left` on 20000 random inputs.

| $n$ | 8 | 10 | 100 | 1000 | 1024 | $10^6$ |
|---|---|---|---|---|---|---|
| branchless, $\lceil \lg n \rceil + 1$ | 4 | 5 | 8 | 11 | 11 | 21 |
| optimum, $\lceil \lg(n+1) \rceil$ | 4 | 4 | 7 | 10 | 11 | 20 |

**A trace.** On $A = [1, 3, 3, 3, 5, 8, 8, 13]$ and $x = 3$:

| $base$ | $len$ | $half$ | probe | $A[\text{probe}] < 3$ |
|---|---|---|---|---|
| 0 | 8 | 4 | $A[4] = 5$ | false |
| 0 | 4 | 2 | $A[2] = 3$ | false |
| 0 | 2 | 1 | $A[1] = 3$ | false |
| 0 | 1 | | $A[0] = 1$ | true, return 1 |

The answer is 1, the first index of 3.

**In C.** The select of line L5 is usually written so that a compiler emits a conditional move:

```c
size_t lower_bound(const int *a, size_t n, int x) {
    if (n == 0) return 0;
    const int *base = a;
    while (n > 1) {
        size_t half = n / 2;
        base = (base[half] < x) ? base + half : base;
        n -= half;
    }
    return (size_t)(base - a) + (*base < x);
}
```

Compilers decide by themselves whether to emit a conditional move, so the result should be checked in the generated code. Some code writes the select as arithmetic, `base += half * (base[half] < x)`, to make it explicit.

## Classic examples

- **[Lower bound](/lower-bound-query/) and [upper bound](/upper-bound-query/) queries.** The template with $A[\cdot] < x$ or $A[\cdot] \le x$. Khuong and Morin measure that on a sorted array that fits in cache this loop is faster than the branchy version.
- **[Search in a sorted array](/search-in-sorted-array/).** Add the test $\ell < n$ and $A[\ell] = x$ after the loop.
- **[Uniform binary search](/uniform-binary-search/).** Its step sizes are also fixed by $n$, and with a select in its loop it is a branchless search that reaches the optimal $\lceil \lg(n+1) \rceil$ comparisons.
- **[Eytzinger layout](/eytzinger-layout/).** The search $k \gets 2k + [A[k] < x]$ in breadth-first order is branchless by nature, and its next probes are close in memory, so they can be prefetched.
- **Merging and partitioning.** The same idea removes the unpredictable branch from the inner loop of a merge, by selecting the smaller head and advancing one of two indices by a computed 0 or 1.

## Variations

- **Prefetch both children.** Before the comparison at line L5, issue a [prefetch](/prefetching/) for the two possible next probes, $base + h'$ and $base + half + h'$, where $h' = \lfloor (len - half)/2 \rfloor$ is the next half. For arrays larger than the cache this hides part of the memory delay, which then dominates the cost.
- **Several searches at once.** Run $k$ independent searches in one loop, one step of each per pass. The steps do not depend on each other, so the processor overlaps their memory reads.
- **SIMD.** Compare $x$ with several items at once and count the items that are smaller, as in a [B-tree](/b-tree/) node of 8 or 16 keys; the count is the step.
- **Upper bound.** Replace $<$ by $\le$ on lines L5 and L7.
- **Optimal count.** Start with a step of $n - 2^{\lfloor \lg n \rfloor}$ as in [uniform binary search](/uniform-binary-search/) to save the extra comparison when $n$ is not a power of 2.

## Pitfalls

- **The compiler keeps the branch.** The source code has no "if", but the compiler may still emit a branch. Check the machine code, or use arithmetic for the select.
- **Slower on large arrays.** Without a branch the processor cannot read ahead along the guessed path, so on arrays much larger than the cache the branchy version, which speculates on memory reads, can be faster. Add prefetching or use a cache-friendly layout.
- **$len \gets half$ instead of $len - half$.** The length must shrink by the same amount in both cases, and to $\lceil len/2 \rceil$, which keeps the answer in range. With $len \gets \lfloor len/2 \rfloor$ the range can lose the answer when $len$ is odd.
- **Forgetting the last test.** The loop leaves two candidates, $base$ and $base + 1$. Without line L7 the result is wrong by one for half of the keys.
- **Empty array.** Line L7 reads $A[0]$, so the case $n = 0$ must return first.
- **Constant time is not guaranteed.** The loop runs the same number of steps for every key, but memory reads still depend on the key, and caches can leak which cells were read. Code for secret data needs more than this technique.

## Exercises

1. Show that the loop makes exactly $\lceil \lg n \rceil$ passes by proving that $len$ after $t$ passes is $\lceil n / 2^t \rceil$.
2. Change the template to compute the upper bound, and test both on an array with many copies of one key.
3. Write a version that makes exactly $\lceil \lg(n+1) \rceil$ comparisons for every $n$, using a first step of $n - 2^{\lfloor \lg n \rfloor}$.
4. Write a merge of two sorted arrays whose inner loop has no data-dependent branch.

## References
